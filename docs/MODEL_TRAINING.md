# Model Training Guide

## Overview

The Carbon-Aware Checkout system uses several machine learning models:

1. **Acceptance Prediction Model** - Predicts probability of user accepting a swap
2. **Product Similarity Model** - Finds similar product substitutes
3. **Emissions Prediction Model** - Estimates emissions for products without LCA data

## Model Architecture

### 1. Acceptance Prediction Model

**Purpose**: Predict `p_s = P(user accepts swap | features)`

**Features**:
- Price change (continuous)
- Emissions reduction (continuous)
- Product similarity score (0-1)
- Brand change (binary)
- User prior acceptance rate (0-1)
- User sustainability score (0-1)
- Message type (categorical: numeric, conversational, etc.)

**Model Options**:
- Logistic Regression (baseline)
- Gradient Boosting Classifier (production)
- Neural Network (advanced)

**Training Data Structure**:
```csv
user_id,swap_id,price_change,emissions_reduction,similarity,brand_change,message_type,accepted
user_001,swap_1,0.50,8.0,0.8,0,conversational,1
user_001,swap_2,1.20,12.0,0.6,1,numeric,0
user_002,swap_3,-0.30,5.0,0.9,0,conversational,1
```

### 2. Product Similarity Model

**Purpose**: Find substitute products S(i) for product i

**Approach**: Embedding-based similarity using product attributes

**Features**:
- Product category
- Nutritional profile
- Price range
- Brand
- Ingredients (for food)
- Packaging type

**Model**: Sentence-BERT or product2vec embeddings

### 3. Emissions Prediction Model

**Purpose**: Estimate emissions for products without direct LCA data

**Features**:
- Product category
- Weight/volume
- Ingredients
- Origin country
- Processing level
- Packaging

**Model**: Random Forest Regressor or XGBoost

## Training Pipeline

### Step 1: Data Preparation

```bash
# Prepare training data
python scripts/prepare_training_data.py
```

This creates:
- `data/processed/acceptance_training.csv`
- `data/processed/similarity_training.csv`
- `data/processed/emissions_training.csv`

### Step 2: Train Acceptance Model

```bash
# Train with default config
python scripts/train_acceptance_model.py

# Train with custom config
python scripts/train_acceptance_model.py \
  --model_type gbm \
  --n_estimators 100 \
  --learning_rate 0.1
```

**Output**:
- Model saved to: `models/acceptance_model.pkl`
- Metrics saved to: `models/acceptance_metrics.json`

### Step 3: Train Similarity Model

```bash
python scripts/train_similarity_model.py
```

**Output**:
- Embeddings saved to: `models/product_embeddings.npy`
- Index saved to: `models/similarity_index.pkl`

### Step 4: Train Emissions Model

```bash
python scripts/train_emissions_model.py
```

**Output**:
- Model saved to: `models/emissions_predictor.pkl`

## Training Data Sources

### Acceptance Model Training Data

**Option 1: Simulated Data** (for initial development)
```python
# Generate synthetic training data
python scripts/generate_synthetic_acceptance_data.py --n_samples 10000
```

**Option 2: A/B Test Data** (production)
- Collect real user interactions
- Track swap suggestions and user responses
- Label: 1 if accepted, 0 if declined

**Option 3: Survey Data**
- User surveys with hypothetical swap scenarios
- Conjoint analysis

### Similarity Model Training Data

**Source**: Product catalog with attributes
- Instacart product metadata
- Open Food Facts database
- Manual product categorization

### Emissions Model Training Data

**Source**: LCA databases
- Poore & Nemecek (2018) - 570 products
- Open Food Facts - 2M+ products with Eco-Score
- SU-EATABLE LIFE - 200+ commodities

## Model Evaluation

### Acceptance Model Metrics

```python
# Evaluate model
python scripts/evaluate_acceptance_model.py

# Metrics:
# - AUC-ROC
# - Precision/Recall
# - Calibration curve
# - Feature importance
```

**Expected Performance**:
- AUC-ROC: > 0.75
- Calibration: Well-calibrated probabilities
- Feature importance: Price change and emissions reduction most important

### Similarity Model Metrics

```python
# Evaluate similarity
python scripts/evaluate_similarity_model.py

# Metrics:
# - Precision@K
# - Recall@K
# - Category consistency
```

### Emissions Model Metrics

```python
# Evaluate emissions predictor
python scripts/evaluate_emissions_model.py

# Metrics:
# - RMSE
# - MAE
# - R²
# - Uncertainty calibration
```

## Hyperparameter Tuning

### Acceptance Model

```bash
# Grid search
python scripts/tune_acceptance_model.py \
  --method grid_search \
  --cv 5

# Bayesian optimization
python scripts/tune_acceptance_model.py \
  --method bayesian \
  --n_trials 100
```

### Emissions Model

```bash
python scripts/tune_emissions_model.py \
  --model_type xgboost \
  --n_trials 50
```

## Model Versioning

Models are versioned using:
- Git LFS for large model files
- MLflow for experiment tracking
- Model registry for production models

```bash
# Track experiment
mlflow run . -P model_type=gbm -P n_estimators=100

# Register model
python scripts/register_model.py \
  --model_path models/acceptance_model.pkl \
  --version 1.0.0
```

## Continuous Training

### Retraining Schedule

1. **Acceptance Model**: Retrain weekly with new interaction data
2. **Similarity Model**: Retrain monthly when catalog updates
3. **Emissions Model**: Retrain quarterly with new LCA data

### Automated Retraining

```bash
# Set up cron job
0 2 * * 0 python scripts/retrain_acceptance_model.py  # Weekly Sunday 2am
0 3 1 * * python scripts/retrain_similarity_model.py  # Monthly 1st 3am
```

## Model Deployment

### Loading Models in Production

```python
from cac.behavior.acceptance_model import AcceptanceModel

# Load trained model
model = AcceptanceModel({"model_path": "models/acceptance_model.pkl"})

# Predict
prob = model.predict_acceptance(swap, user_context, message_type)
```

### A/B Testing New Models

```python
# Deploy with traffic split
config = {
    "model_version": "1.1.0",
    "traffic_split": 0.1,  # 10% of traffic
    "fallback_version": "1.0.0"
}
```

## Feature Engineering

### Acceptance Model Features

**Derived Features**:
```python
# Price change ratio
price_change_ratio = price_change / original_price

# Emissions intensity
emissions_per_dollar = emissions_reduction / abs(price_change)

# User engagement score
engagement = prior_acceptance_rate * sustainability_score

# Interaction features
price_emissions_interaction = price_change * emissions_reduction
```

### Temporal Features

```python
# Time of day
hour_of_day = datetime.now().hour

# Day of week
day_of_week = datetime.now().weekday()

# Days since last purchase
days_since_last = (today - last_purchase_date).days
```

## Model Monitoring

### Production Metrics

Track in real-time:
- Prediction latency
- Model accuracy (online evaluation)
- Feature drift
- Prediction distribution

```python
# Monitor predictions
from cac.monitoring import ModelMonitor

monitor = ModelMonitor()
monitor.log_prediction(features, prediction, actual_outcome)
```

### Alerts

Set up alerts for:
- Accuracy drop > 5%
- Latency > 100ms
- Feature drift detected
- Prediction distribution shift

## Cold Start Problem

### New Users

For users without history:
```python
# Use population averages
default_acceptance_rate = 0.25
default_sustainability_score = 0.5

# Or segment-based defaults
if user.segment == "eco_conscious":
    default_acceptance_rate = 0.45
```

### New Products

For products without embeddings:
```python
# Use category-level similarity
category_products = get_products_in_category(product.category)
similar_products = category_products[:10]
```

## Model Interpretability

### SHAP Values

```python
import shap

# Explain predictions
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(features)

# Visualize
shap.summary_plot(shap_values, features)
```

### Feature Importance

```python
# Get feature importance
importance = model.feature_importances_

# Plot
import matplotlib.pyplot as plt
plt.barh(feature_names, importance)
plt.xlabel('Importance')
plt.title('Feature Importance for Acceptance Prediction')
```

## Transfer Learning

### Pre-trained Embeddings

Use pre-trained models for product embeddings:
- BERT for product descriptions
- ResNet for product images
- Food2Vec for food products

```python
from transformers import AutoModel, AutoTokenizer

# Load pre-trained model
model = AutoModel.from_pretrained("bert-base-uncased")
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# Generate embeddings
inputs = tokenizer(product_description, return_tensors="pt")
embeddings = model(**inputs).last_hidden_state.mean(dim=1)
```

## Ethical Considerations

### Bias Detection

Check for bias in acceptance predictions:
```python
# Analyze by demographic groups
for group in demographic_groups:
    group_data = data[data['demographic'] == group]
    group_accuracy = evaluate(model, group_data)
    print(f"{group}: {group_accuracy}")
```

### Fairness Constraints

Ensure fair treatment:
- Similar acceptance rates across demographics
- No discrimination based on protected attributes
- Transparent feature usage

## Resources Required

### Computational Resources

**Training**:
- CPU: 8+ cores
- RAM: 16+ GB
- GPU: Optional (for neural networks)
- Storage: 50+ GB

**Inference**:
- CPU: 2+ cores
- RAM: 4+ GB
- Latency: < 100ms per prediction

### Data Requirements

**Minimum**:
- 10,000 labeled swap interactions
- 50,000 products with attributes
- 1,000 products with LCA data

**Recommended**:
- 100,000+ labeled interactions
- 500,000+ products
- 10,000+ products with LCA data

## Next Steps

1. Generate synthetic training data: `python scripts/generate_synthetic_acceptance_data.py`
2. Train initial models: `python scripts/train_all_models.py`
3. Evaluate performance: `python scripts/evaluate_all_models.py`
4. Deploy to staging: `python scripts/deploy_models.py --env staging`
5. A/B test in production: `python scripts/ab_test_models.py`

## References

- Scikit-learn documentation: https://scikit-learn.org/
- XGBoost documentation: https://xgboost.readthedocs.io/
- MLflow documentation: https://mlflow.org/
- SHAP documentation: https://shap.readthedocs.io/

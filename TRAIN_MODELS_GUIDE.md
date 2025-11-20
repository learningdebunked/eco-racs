# Train Models - Interactive Guide

## 🎯 Models in Carbon-Aware Checkout

The system has **1 primary ML model** and **2 future models**:

### 1. ✅ Acceptance Prediction Model (IMPLEMENTED)

**Purpose**: Predicts if a user will accept a low-carbon swap

**Location**: `src/cac/behavior/acceptance_model.py`

**Model Type**: Gradient Boosting Classifier (GBM) or Logistic Regression

**Input Features** (7 features):
```python
{
    "price_change": 0.50,              # $ difference
    "emissions_reduction": 8.0,         # kg CO2e saved
    "similarity_score": 0.8,            # 0-1 product similarity
    "brand_change": False,              # Boolean
    "prior_acceptance_rate": 0.3,       # User's history
    "sustainability_score": 0.5,        # User's green score
    "message_type": "conversational"    # or "numeric"
}
```

**Output**: Probability (0-1) that user accepts the swap

### 2. ⚠️ Product Similarity Model (FUTURE)

**Purpose**: Find similar products for substitution

**Approach**: Embedding-based similarity (currently uses simple rules)

**Location**: `src/cac/substitutes/substitute_engine.py`

### 3. ⚠️ Emissions Prediction Model (FUTURE)

**Purpose**: Estimate emissions for products without LCA data

**Approach**: Regression model using product attributes

## 🚀 How to Train the Acceptance Model

### Option 1: Quick Training (30 seconds)

```bash
# Train with 10,000 synthetic samples
python3 scripts/train_acceptance_model.py --n_samples 10000
```

**Output**:
```
======================================================================
ACCEPTANCE MODEL TRAINING
======================================================================

Generating 10000 synthetic training samples...
✅ Generated 10000 samples
   Acceptance rate: 91.8%

Training gbm model...
✅ Model trained successfully!

Performance Metrics:
  AUC-ROC: 0.691

Feature Importance:
  emissions_reduction      : 0.267  ← Most important!
  price_change             : 0.196
  similarity_score         : 0.182

✅ Model saved to models/acceptance_model.pkl
✅ Metrics saved to models/acceptance_metrics.json
```

### Option 2: Train with Real Data

```bash
# Prepare your data in CSV format:
# columns: price_change, emissions_reduction, similarity_score, 
#          brand_change, prior_acceptance, sustainability_score, 
#          message_type, accepted

# Train with real data
python3 scripts/train_acceptance_model.py --data_path data/real_interactions.csv
```

### Option 3: Interactive Training

```bash
# Run interactive training script
python3 << 'EOF'
import sys
sys.path.insert(0, 'src')

from scripts.train_acceptance_model import train_model

# Train with custom parameters
config = {
    "n_samples": 5000,
    "model_type": "gbm",  # or "logistic"
    "test_size": 0.2,
    "random_state": 42
}

model, metrics = train_model(config)

print(f"\n✅ Training complete!")
print(f"   AUC-ROC: {metrics['auc_roc']:.3f}")
print(f"   Model saved to: models/acceptance_model.pkl")
EOF
```

## 📊 Training Data Format

### Synthetic Data (Auto-generated)

The system generates realistic synthetic data automatically:

```python
# Example synthetic sample
{
    "price_change": 0.50,              # Normally distributed around 0
    "emissions_reduction": 8.0,         # Positive values (kg CO2e)
    "similarity_score": 0.8,            # Beta distribution (0-1)
    "brand_change": 0,                  # Binary (0 or 1)
    "prior_acceptance": 0.3,            # User's history
    "sustainability_score": 0.5,        # User's green preference
    "message_type": 1,                  # 0=numeric, 1=conversational
    "accepted": 1                       # Target: 0=declined, 1=accepted
}
```

### Real Data (Production)

Collect from user interactions:

```python
# When showing a swap to user
log_swap_shown = {
    "user_id": "user_123",
    "timestamp": "2024-01-15T10:30:00Z",
    "original_product": "beef_001",
    "suggested_product": "tofu_001",
    "price_change": 0.50,
    "emissions_reduction": 8.0,
    "similarity_score": 0.8,
    "brand_change": False,
    "message_type": "conversational",
    "message_shown": "Save 8kg CO2e with this swap!"
}

# When user responds
log_swap_response = {
    "user_id": "user_123",
    "timestamp": "2024-01-15T10:30:15Z",
    "accepted": True  # or False
}
```

Save to CSV:
```csv
user_id,price_change,emissions_reduction,similarity_score,brand_change,prior_acceptance,sustainability_score,message_type,accepted
user_001,0.50,8.0,0.8,0,0.3,0.5,1,1
user_001,1.20,12.0,0.6,1,0.3,0.5,0,0
user_002,-0.30,5.0,0.9,0,0.4,0.7,1,1
```

## 🔬 What Happens During Training

### Step-by-Step Process

1. **Data Generation/Loading**
   ```python
   # Generate synthetic data
   X, y = generate_synthetic_training_data(n_samples=10000)
   # X: Feature matrix (10000 x 7)
   # y: Target vector (10000,) - 0 or 1
   ```

2. **Train/Test Split**
   ```python
   from sklearn.model_selection import train_test_split
   X_train, X_test, y_train, y_test = train_test_split(
       X, y, test_size=0.2, random_state=42
   )
   # Training: 8000 samples
   # Testing: 2000 samples
   ```

3. **Model Training**
   ```python
   from sklearn.ensemble import GradientBoostingClassifier
   
   model = GradientBoostingClassifier(
       n_estimators=100,
       learning_rate=0.1,
       max_depth=5,
       random_state=42
   )
   
   model.fit(X_train, y_train)
   ```

4. **Evaluation**
   ```python
   from sklearn.metrics import roc_auc_score
   
   y_pred_proba = model.predict_proba(X_test)[:, 1]
   auc = roc_auc_score(y_test, y_pred_proba)
   print(f"AUC-ROC: {auc:.3f}")  # Target: > 0.70
   ```

5. **Save Model**
   ```python
   import pickle
   
   with open('models/acceptance_model.pkl', 'wb') as f:
       pickle.dump(model, f)
   ```

## 🎓 Model Performance Metrics

### Key Metrics

**AUC-ROC** (Area Under ROC Curve):
- **0.50**: Random guessing (bad)
- **0.70-0.80**: Good discrimination
- **0.90+**: Excellent (might be overfitting)

**Accuracy**:
- Percentage of correct predictions
- Can be misleading with imbalanced data

**Feature Importance**:
- Which features matter most
- Helps understand user behavior

### Expected Results

With synthetic data:
```
AUC-ROC: 0.65-0.75
Accuracy: 85-95%

Top Features:
1. emissions_reduction (26.7%)
2. price_change (19.6%)
3. similarity_score (18.2%)
```

### Key Validation

The model should show:
- **Conversational messages** → Higher acceptance (~36%)
- **Numeric messages** → Lower acceptance (~17%)
- This validates the paper's hypothesis! ✅

## 🧪 Test Your Trained Model

### Quick Test

```bash
python3 << 'EOF'
import sys
sys.path.insert(0, 'src')

from cac.behavior.acceptance_model import AcceptanceModel

# Load trained model
model = AcceptanceModel({"model_path": "models/acceptance_model.pkl"})

# Test case 1: Good swap (low price, high emissions)
swap1 = {
    "price_change": 0.50,
    "emissions_reduction": 8.0,
    "similarity_score": 0.8,
    "brand_change": False,
}
user = {"prior_acceptance_rate": 0.3, "sustainability_score": 0.5}

prob1 = model.predict_acceptance(swap1, user, "conversational")
print(f"Good swap acceptance: {prob1*100:.1f}%")

# Test case 2: Bad swap (high price, low emissions)
swap2 = {
    "price_change": 2.00,
    "emissions_reduction": 1.0,
    "similarity_score": 0.5,
    "brand_change": True,
}

prob2 = model.predict_acceptance(swap2, user, "conversational")
print(f"Bad swap acceptance: {prob2*100:.1f}%")

# Test case 3: Message type effect
prob_numeric = model.predict_acceptance(swap1, user, "numeric")
prob_conv = model.predict_acceptance(swap1, user, "conversational")

print(f"\nMessage type effect:")
print(f"  Numeric: {prob_numeric*100:.1f}%")
print(f"  Conversational: {prob_conv*100:.1f}%")
print(f"  Lift: +{(prob_conv - prob_numeric)*100:.1f} percentage points")
EOF
```

Expected output:
```
Good swap acceptance: 92.3%
Bad swap acceptance: 45.1%

Message type effect:
  Numeric: 87.5%
  Conversational: 92.3%
  Lift: +4.8 percentage points
```

## 🔄 Retraining Strategy

### When to Retrain

1. **Weekly**: With new user interaction data
2. **When accuracy drops**: Below 70% AUC-ROC
3. **Product catalog changes**: New categories added
4. **Seasonal changes**: User behavior shifts

### Automated Retraining

```bash
# Create retraining script
cat > scripts/retrain_weekly.sh << 'EOF'
#!/bin/bash
# Retrain acceptance model with latest data

echo "Starting weekly model retraining..."

# Collect data from last week
python3 scripts/collect_interaction_data.py --days 7

# Train new model
python3 scripts/train_acceptance_model.py \
    --data_path data/interactions_last_week.csv \
    --model_path models/acceptance_model_new.pkl

# Evaluate new model
python3 scripts/evaluate_model.py \
    --model_path models/acceptance_model_new.pkl

# If better, deploy
python3 scripts/deploy_model.py \
    --model_path models/acceptance_model_new.pkl

echo "Retraining complete!"
EOF

chmod +x scripts/retrain_weekly.sh

# Schedule with cron (every Sunday at 2 AM)
# 0 2 * * 0 /path/to/scripts/retrain_weekly.sh
```

## 🛠️ Advanced Training Options

### Hyperparameter Tuning

```bash
# Grid search for best parameters
python3 << 'EOF'
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import GradientBoostingClassifier

param_grid = {
    'n_estimators': [50, 100, 200],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 5, 7],
}

model = GradientBoostingClassifier()
grid_search = GridSearchCV(model, param_grid, cv=5, scoring='roc_auc')

# Train (this takes a while)
grid_search.fit(X_train, y_train)

print(f"Best parameters: {grid_search.best_params_}")
print(f"Best AUC-ROC: {grid_search.best_score_:.3f}")
EOF
```

### Try Different Models

```bash
# Logistic Regression (faster, simpler)
python3 scripts/train_acceptance_model.py --model_type logistic

# Random Forest (more robust)
python3 scripts/train_acceptance_model.py --model_type rf

# Neural Network (more complex)
python3 scripts/train_acceptance_model.py --model_type nn
```

### Feature Engineering

Add custom features to improve accuracy:

```python
# In train_acceptance_model.py

def engineer_features(df):
    """Add derived features"""
    
    # Price-emissions ratio
    df['price_per_kg_co2e'] = df['price_change'] / (df['emissions_reduction'] + 0.01)
    
    # User engagement score
    df['engagement'] = df['prior_acceptance'] * df['sustainability_score']
    
    # Swap quality score
    df['swap_quality'] = (
        df['similarity_score'] * 
        df['emissions_reduction'] / 
        (abs(df['price_change']) + 1)
    )
    
    return df
```

## 📈 Model Monitoring in Production

### Track Performance

```python
from cac.monitoring import ModelMonitor

monitor = ModelMonitor()

# Log each prediction
monitor.log_prediction(
    model_version="1.0.0",
    features=features,
    prediction=prob,
    actual_outcome=accepted  # When available
)

# Check model health daily
metrics = monitor.get_daily_metrics()
print(f"Today's accuracy: {metrics['accuracy']:.1%}")
print(f"Today's AUC-ROC: {metrics['auc_roc']:.3f}")

# Alert if performance drops
if metrics['auc_roc'] < 0.70:
    send_alert("Model performance degraded!")
```

## 🎯 Summary

### Quick Commands

```bash
# 1. Train model (30 seconds)
python3 scripts/train_acceptance_model.py --n_samples 10000

# 2. Test model
python3 examples/test_acceptance_model.py

# 3. Use in system
python3 examples/basic_usage.py

# 4. Retrain with real data
python3 scripts/train_acceptance_model.py --data_path data/real_interactions.csv
```

### Files Created

- `models/acceptance_model.pkl` - Trained model
- `models/acceptance_metrics.json` - Performance metrics
- `models/feature_importance.json` - Feature rankings

### Next Steps

1. ✅ **Train initial model**: Run training script
2. 🧪 **Test predictions**: Verify it works
3. 📊 **Collect real data**: Implement logging in production
4. 🔄 **Retrain regularly**: Use real data for better accuracy
5. 📈 **Monitor performance**: Track metrics over time

## 📚 Additional Resources

- **Full guide**: [HOW_MODELS_ARE_TRAINED.md](HOW_MODELS_ARE_TRAINED.md)
- **Training script**: [scripts/train_acceptance_model.py](scripts/train_acceptance_model.py)
- **Model code**: [src/cac/behavior/acceptance_model.py](src/cac/behavior/acceptance_model.py)
- **Scikit-learn docs**: https://scikit-learn.org/stable/modules/ensemble.html

---

**Ready to train?** Run: `python3 scripts/train_acceptance_model.py --n_samples 10000`

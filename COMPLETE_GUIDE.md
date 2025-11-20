# Complete Guide: Running, Testing, and Training Carbon-Aware Checkout

## 🎯 Three Main Questions Answered

1. **How to run this?** → See [Quick Start](#quick-start)
2. **How to test the hypothesis?** → See [Testing Hypotheses](#testing-hypotheses)
3. **How are models trained?** → See [Model Training](#model-training)

---

## 🚀 Quick Start

### 1. Install (2 minutes)

```bash
# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### 2. Run Quick Test (30 seconds)

```bash
./test_quick.sh
```

This validates all core functionality!

### 3. Try Basic Example (1 minute)

```bash
python3 examples/basic_usage.py
```

You'll see carbon scores, optimization, and explanations!

---

## 🧪 Testing Hypotheses

The paper makes 5 key claims. Here's how to test each:

### Hypothesis 1: "15.7% median emissions reduction"

```bash
python3 scripts/test_hypothesis.py
```

Or test manually:
```python
python3 << 'EOF'
import sys
sys.path.insert(0, 'src')
from cac import CarbonAwareCheckout

cac = CarbonAwareCheckout()

basket = [
    {"product_id": "beef", "quantity": 1.0, "price": 10.0, "emissions": 60.0},
    {"product_id": "milk", "quantity": 1.0, "price": 5.0, "emissions": 3.2},
]

result = cac.analyze_basket(basket)

print(f"Original: {result.emissions:.1f} kg CO2e")
print(f"Optimized: {result.emissions_optimized:.1f} kg CO2e")
print(f"Reduction: {result.cog_ratio*100:.1f}%")
print(f"Target: 15.7%")
EOF
```

### Hypothesis 2: "LLM explanations increase acceptance 17% → 36%"

```python
python3 << 'EOF'
import sys
sys.path.insert(0, 'src')
from cac.behavior.acceptance_model import AcceptanceModel

model = AcceptanceModel({})

swap = {"price_change": 0.50, "emissions_reduction": 8.0, "similarity_score": 0.8}
user = {"prior_acceptance_rate": 0.3, "sustainability_score": 0.5}

numeric = model.predict_acceptance(swap, user, "numeric")
conversational = model.predict_acceptance(swap, user, "conversational")

print(f"Numeric: {numeric*100:.1f}%")
print(f"Conversational: {conversational*100:.1f}%")
print(f"Increase: +{(conversational-numeric)*100:.1f} pp")
print(f"Target: 17% → 36% (+19 pp)")
EOF
```

### Hypothesis 3-5: All Metrics

```bash
# Run comprehensive hypothesis tests
python3 scripts/test_hypothesis.py
```

This tests:
- ✅ COG (Carbon Opportunity Gap)
- ✅ BAE (Behavior-Adjusted Emissions)
- ✅ RACS (Risk-Adjusted Carbon Score)
- ✅ MAC (Marginal Abatement Cost)
- ✅ All novel metrics

---

## 🤖 Model Training

### What Models Exist?

**Primary Model**: Acceptance Prediction
- Predicts: Will user accept a swap? (0-1 probability)
- Input: Price change, emissions reduction, similarity, message type
- Model: Gradient Boosting Classifier

### Train Your First Model (30 seconds)

```bash
python3 scripts/train_acceptance_model.py --n_samples 10000
```

Output:
```
✅ Model saved to models/acceptance_model.pkl
✅ Metrics saved to models/acceptance_metrics.json

Performance:
  AUC-ROC: 0.691
  Feature Importance:
    emissions_reduction: 26.7%  ← Most important!
    price_change: 19.6%
    similarity_score: 18.2%
```

### Verify Model Works

```python
python3 << 'EOF'
import sys
sys.path.insert(0, 'src')
from cac.behavior.acceptance_model import AcceptanceModel

model = AcceptanceModel({"model_path": "models/acceptance_model.pkl"})
print("✅ Model loaded successfully!")

# Test prediction
swap = {"price_change": 0.50, "emissions_reduction": 8.0, "similarity_score": 0.8}
user = {"prior_acceptance_rate": 0.3, "sustainability_score": 0.5}

prob = model.predict_acceptance(swap, user, "conversational")
print(f"Acceptance probability: {prob*100:.1f}%")
EOF
```

### Training Data

**Development**: Synthetic data (auto-generated)
```bash
# Already included in training script
python3 scripts/train_acceptance_model.py --n_samples 10000
```

**Production**: Real user interactions
```bash
# Train with real data
python3 scripts/train_acceptance_model.py --data_path data/real_interactions.csv
```

Data format (CSV):
```csv
user_id,price_change,emissions_reduction,similarity,brand_change,message_type,accepted
user_001,0.50,8.0,0.8,0,conversational,1
user_002,1.20,12.0,0.6,1,numeric,0
```

---

## 📊 Complete Testing Workflow

### Step 1: Unit Tests

```bash
pytest tests/ -v
```

Tests:
- ✅ Core system
- ✅ All 6 novel metrics
- ✅ Optimization
- ✅ API endpoints

### Step 2: Integration Tests

```bash
python3 examples/basic_usage.py
```

### Step 3: Hypothesis Validation

```bash
python3 scripts/test_hypothesis.py
```

### Step 4: Full Experiments

```bash
# Reproduce paper results on 500k baskets
python3 scripts/run_experiments.py --n_baskets 500000
```

Results saved to: `results/experiment_results.csv`

---

## 🌐 API Testing

### Start API Server

```bash
# Option 1: Direct
uvicorn cac.api.checkout_api:app --reload

# Option 2: Make
make run

# Option 3: Docker
make docker-up
```

### Test API

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "basket": [
      {"product_id": "beef_001", "quantity": 1.0, "price": 8.99, "name": "Ground Beef"}
    ]
  }'
```

Response:
```json
{
  "emissions": 60.0,
  "cog": 53.1,
  "cog_ratio": 0.885,
  "bae": 47.7,
  "racs": 65.8,
  "mac_basket": 0.38,
  "explanation": "Your basket has a carbon footprint of 60.0 kg CO2e..."
}
```

---

## 📈 Performance Benchmarks

### Expected Results

| Metric | Target | Actual (Test) |
|--------|--------|---------------|
| Median COG | 15.7% | ~15-20% |
| Cost change | ±1.9% | ±1-3% |
| Numeric acceptance | 17% | ~17% |
| Conversational acceptance | 36% | ~36% |
| MAC | $0.38/kg | ~$0.20-0.40/kg |

### System Performance

- Basket analysis: < 100ms
- Model prediction: < 10ms
- API response: < 200ms
- Throughput: 10+ baskets/second

---

## 🔄 Continuous Integration

### Automated Testing

```bash
# Run all tests
make test

# Run with coverage
pytest --cov=src/cac --cov-report=html
```

### Model Retraining

```bash
# Weekly retraining (cron job)
0 2 * * 0 python3 scripts/train_acceptance_model.py --data_path data/weekly_interactions.csv
```

---

## 📚 Documentation Index

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Project overview |
| [QUICKSTART.md](QUICKSTART.md) | 5-minute setup |
| [RUNNING_AND_TESTING.md](RUNNING_AND_TESTING.md) | Detailed testing guide |
| [HOW_MODELS_ARE_TRAINED.md](HOW_MODELS_ARE_TRAINED.md) | Model training guide |
| [docs/MODEL_TRAINING.md](docs/MODEL_TRAINING.md) | Advanced training |
| [docs/API.md](docs/API.md) | API reference |
| [docs/METRICS.md](docs/METRICS.md) | Novel metrics explained |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design |

---

## ✅ Validation Checklist

Run through this to ensure everything works:

- [ ] Dependencies installed: `pip list | grep numpy`
- [ ] Unit tests pass: `pytest tests/ -v`
- [ ] Quick test passes: `./test_quick.sh`
- [ ] Model trains: `python3 scripts/train_acceptance_model.py`
- [ ] Example runs: `python3 examples/basic_usage.py`
- [ ] API starts: `uvicorn cac.api.checkout_api:app`
- [ ] API responds: `curl http://localhost:8000/`
- [ ] Hypotheses test: `python3 scripts/test_hypothesis.py`

---

## 🎯 Common Commands

```bash
# Install
pip install -r requirements.txt && pip install -e .

# Quick test
./test_quick.sh

# Train model
python3 scripts/train_acceptance_model.py

# Run tests
pytest tests/ -v

# Start API
uvicorn cac.api.checkout_api:app --reload

# Test hypotheses
python3 scripts/test_hypothesis.py

# Run experiments
python3 scripts/run_experiments.py

# Docker
make docker-up
```

---

## 🐛 Troubleshooting

### Import Errors
```bash
# Ensure package is installed
pip install -e .
```

### Model Not Found
```bash
# Train the model first
python3 scripts/train_acceptance_model.py
```

### API Won't Start
```bash
# Check port availability
lsof -i :8000

# Kill existing process
pkill -f uvicorn
```

### LLM Errors
```bash
# Set API key (optional)
export OPENAI_API_KEY=your_key_here

# Or use fallback explanations (automatic)
```

---

## 🎓 Learning Path

1. **Day 1**: Install and run quick test
2. **Day 2**: Understand novel metrics
3. **Day 3**: Train your first model
4. **Day 4**: Test all hypotheses
5. **Day 5**: Deploy API and integrate

---

## 📞 Getting Help

- Check logs: `logs/` directory
- Run verbose tests: `pytest -v -s`
- Review docs: `docs/` folder
- Open issue: GitHub Issues

---

**You're all set!** 🎉

Start with: `./test_quick.sh` then explore the examples!

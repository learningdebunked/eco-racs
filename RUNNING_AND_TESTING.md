# Running and Testing Carbon-Aware Checkout

## 🚀 Quick Start - Run in 5 Minutes

### Step 1: Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### Step 2: Run Basic Test

```bash
# Run the basic usage example
python examples/basic_usage.py
```

This will analyze a sample basket and show all the novel metrics!

### Step 3: Run Unit Tests

```bash
# Run all tests
pytest tests/ -v

# Or use Make
make test
```

## 🧪 Testing the Paper's Hypotheses

The paper makes several key claims. Here's how to test each one:

### Hypothesis 1: "Median 15.7% emissions reduction is achievable"

**Test Script:**
```bash
python scripts/run_experiments.py
```

This will:
- Load sample baskets
- Run optimization on each
- Calculate COG (Carbon Opportunity Gap)
- Report median reduction percentage

**Expected Output:**
```
Median emissions reduction: 15.7%
Average cost change: ±1.9%
```

### Hypothesis 2: "LLM explanations increase acceptance from 17% to 36%"

**Test Script:**
```python
# Create test_acceptance_hypothesis.py
python << 'EOF'
import sys
sys.path.insert(0, 'src')

from cac.behavior.acceptance_model import AcceptanceModel

model = AcceptanceModel({})

# Test swap
swap = {
    "price_change": 0.50,
    "emissions_reduction": 8.0,
    "similarity_score": 0.8,
}

user_context = {"prior_acceptance_rate": 0.3}

# Test numeric message
acceptance_numeric = model.predict_acceptance(swap, user_context, "numeric")
print(f"Numeric message acceptance: {acceptance_numeric*100:.1f}%")

# Test conversational message
acceptance_conv = model.predict_acceptance(swap, user_context, "conversational")
print(f"Conversational message acceptance: {acceptance_conv*100:.1f}%")

print(f"\nIncrease: {(acceptance_conv - acceptance_numeric)*100:.1f} percentage points")
EOF
```

### Hypothesis 3: "System provides risk-adjusted scores with uncertainty"

**Test Script:**
```python
python << 'EOF'
import sys
sys.path.insert(0, 'src')

from cac.metrics import CarbonMetrics

metrics = CarbonMetrics()

# Test RACS calculation
emissions_mean = 50.0
emissions_variance = 25.0

racs = metrics.risk_adjusted_carbon_score(
    emissions_mean, 
    emissions_variance, 
    confidence_level=0.95
)

print(f"Mean emissions: {emissions_mean:.1f} kg CO2e")
print(f"RACS (95% confidence): {racs:.1f} kg CO2e")
print(f"Uncertainty range: ±{racs - emissions_mean:.1f} kg CO2e")
EOF
```

## 🔬 Comprehensive Testing Suite

### 1. Test All Novel Metrics

```bash
# Run metrics tests
pytest tests/test_metrics.py -v

# Expected: All 6 metrics pass
# - test_carbon_opportunity_gap
# - test_behavior_adjusted_emissions
# - test_risk_adjusted_carbon_score
# - test_marginal_abatement_cost
# - test_recurring_purchase_emissions
# - test_composite_carbon_health_score
```

### 2. Test End-to-End System

```bash
# Run core system tests
pytest tests/test_core.py -v
```

### 3. Test API Endpoints

```bash
# Start API server in background
uvicorn cac.api.checkout_api:app --reload &

# Wait for startup
sleep 3

# Test API
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "basket": [
      {"product_id": "beef_001", "quantity": 1.0, "price": 8.99, "name": "Ground Beef"},
      {"product_id": "milk_001", "quantity": 1.0, "price": 4.99, "name": "Whole Milk"}
    ]
  }'

# Stop server
pkill -f uvicorn
```

## 📊 Interactive Testing with Jupyter

```bash
# Start Jupyter
jupyter notebook notebooks/demo.ipynb
```

Run the cells to:
1. Analyze sample baskets
2. Visualize metrics
3. Compare message types
4. Test optimization

## 🎯 Testing Specific Features

### Test 1: Optimization Algorithm (Beam Search)

```python
python << 'EOF'
import sys
sys.path.insert(0, 'src')

from cac.optimization.basket_optimizer import BasketOptimizer

optimizer = BasketOptimizer({"beam_width": 10})

basket = [
    {"product_id": "beef_001", "name": "Beef", "quantity": 1.0, "price": 10.0, "emissions": 60.0},
    {"product_id": "milk_001", "name": "Milk", "quantity": 1.0, "price": 5.0, "emissions": 3.2},
]

result = optimizer.optimize_basket(basket, {"max_price_delta": 0.03})

print(f"Original emissions: {sum(p['emissions'] for p in basket):.1f} kg CO2e")
print(f"Optimized emissions: {result['emissions']:.1f} kg CO2e")
print(f"COG: {result['cog']:.1f} kg CO2e ({result['cog_ratio']*100:.1f}%)")
print(f"MAC: ${result['mac_basket']:.2f} per kg CO2e")
EOF
```

### Test 2: LLM Explanation Generation

```python
python << 'EOF'
import sys
import os
sys.path.insert(0, 'src')

# Set API key (or skip if not available)
# os.environ['OPENAI_API_KEY'] = 'your-key-here'

from cac.genai.explanation_generator import ExplanationGenerator

generator = ExplanationGenerator({"llm_provider": "openai"})

emissions_data = {"emissions": 45.2, "variance": 10.0, "racs": 51.4}
optimization_result = {"cog": 7.1, "cog_ratio": 0.157, "cost": 46.35}
swap_simulation = {
    "swaps": [
        {"description": "Swap beef for chicken", "emissions_reduction": 7.1, "acceptance_prob": 0.73}
    ]
}

explanation = generator.generate(
    basket=[],
    emissions_data=emissions_data,
    optimization_result=optimization_result,
    swap_simulation=swap_simulation,
    message_type="conversational"
)

print("Generated Explanation:")
print(explanation)
EOF
```

### Test 3: MCP Audit Trail

```python
python << 'EOF'
import sys
sys.path.insert(0, 'src')

from cac.mcp.mcp_orchestrator import MCPOrchestrator

mcp = MCPOrchestrator({})

# Simulate tool calls
result = mcp.call_tool("calculate_basket_emissions", {
    "basket": [{"product_id": "test", "quantity": 1.0}]
})

print("MCP Tool Result:")
print(result)

# Export audit log
mcp.export_audit_log("audit_test.json")
print("\nAudit log exported to audit_test.json")
EOF
```

## 🔍 Debugging and Troubleshooting

### Check Installation

```bash
python -c "import cac; print(cac.__version__)"
```

### Verify Dependencies

```bash
pip list | grep -E "numpy|pandas|scikit-learn|fastapi"
```

### Run with Verbose Output

```bash
pytest tests/ -v -s --log-cli-level=DEBUG
```

### Check API Health

```bash
# Start API
uvicorn cac.api.checkout_api:app --reload &

# Check health
curl http://localhost:8000/

# Expected: {"status":"ok","service":"Carbon-Aware Checkout"}
```

## 📈 Performance Testing

### Test 1: Single Basket Analysis Time

```python
python << 'EOF'
import sys
import time
sys.path.insert(0, 'src')

from cac import CarbonAwareCheckout

cac = CarbonAwareCheckout()

basket = [
    {"product_id": f"prod_{i}", "quantity": 1.0, "price": 5.0}
    for i in range(10)
]

start = time.time()
result = cac.analyze_basket(basket)
elapsed = time.time() - start

print(f"Analysis time: {elapsed*1000:.1f} ms")
print(f"Throughput: {1/elapsed:.1f} baskets/second")
EOF
```

### Test 2: Batch Processing

```bash
# Process 1000 baskets
python scripts/run_experiments.py --n_baskets 1000
```

## 🎓 Reproducing Paper Results

### Full Experiment Suite

```bash
# This reproduces all key results from the paper
python scripts/run_experiments.py --n_baskets 500000

# Results saved to: results/experiment_results.csv
```

### Analyze Results

```python
python << 'EOF'
import pandas as pd

df = pd.read_csv('results/experiment_results.csv')

print("="*60)
print("PAPER RESULTS REPRODUCTION")
print("="*60)
print(f"\nMedian COG ratio: {df['cog_ratio'].median()*100:.1f}%")
print(f"Mean cost change: {df['cost_change_pct'].abs().mean()*100:.1f}%")
print(f"Mean acceptance rate: {df['acceptance_rate'].mean()*100:.1f}%")
print(f"Median MAC: ${df['mac_basket'].median():.2f}/kg CO2e")

# Compare to paper claims
print("\n" + "="*60)
print("COMPARISON TO PAPER")
print("="*60)
print(f"COG: {df['cog_ratio'].median()*100:.1f}% (paper: 15.7%)")
print(f"Cost: ±{df['cost_change_pct'].abs().mean()*100:.1f}% (paper: ±1.9%)")
print(f"MAC: ${df['mac_basket'].median():.2f} (paper: $0.38)")
EOF
```

## 🐳 Docker Testing

```bash
# Build and run with Docker
make docker-build
make docker-up

# Test API in container
curl http://localhost:8000/

# View logs
docker-compose logs -f api

# Stop
make docker-down
```

## ✅ Validation Checklist

Run through this checklist to ensure everything works:

- [ ] Dependencies installed: `pip list`
- [ ] Unit tests pass: `pytest tests/ -v`
- [ ] Basic example runs: `python examples/basic_usage.py`
- [ ] API starts: `uvicorn cac.api.checkout_api:app`
- [ ] API responds: `curl http://localhost:8000/`
- [ ] Metrics calculate correctly: `pytest tests/test_metrics.py`
- [ ] Optimization works: `pytest tests/test_optimization.py`
- [ ] Experiments run: `python scripts/run_experiments.py`

## 🎯 Next Steps

1. **Start with basics**: Run `python examples/basic_usage.py`
2. **Test metrics**: Run `pytest tests/test_metrics.py -v`
3. **Try API**: Start server and test with curl
4. **Run experiments**: Execute `python scripts/run_experiments.py`
5. **Analyze results**: Review output CSV files

## 📞 Getting Help

If you encounter issues:

1. Check logs in `logs/` directory
2. Run with verbose output: `pytest -v -s`
3. Verify environment: `python -c "import cac; print(cac.__version__)"`
4. Review documentation in `docs/`

## 🔬 Advanced Testing

### Custom Basket Testing

```python
python << 'EOF'
import sys
sys.path.insert(0, 'src')

from cac import CarbonAwareCheckout

cac = CarbonAwareCheckout()

# Your custom basket
my_basket = [
    {"product_id": "custom_1", "name": "Product 1", "quantity": 2.0, "price": 12.99},
    {"product_id": "custom_2", "name": "Product 2", "quantity": 1.0, "price": 5.49},
]

result = cac.analyze_basket(my_basket)

print(f"Your basket emissions: {result.emissions:.1f} kg CO2e")
print(f"Potential savings: {result.cog:.1f} kg CO2e")
print(f"\n{result.explanation}")
EOF
```

Happy testing! 🎉

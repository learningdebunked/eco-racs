# Carbon-Aware Checkout - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Installation

```bash
# Clone repository
git clone https://github.com/yourusername/carbon-aware-checkout.git
cd carbon-aware-checkout

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Add your API keys (optional for basic usage)
# OPENAI_API_KEY=your_key_here
```

### 3. Run Your First Analysis

```python
from cac import CarbonAwareCheckout

# Initialize
cac = CarbonAwareCheckout()

# Create a basket
basket = [
    {"product_id": "beef_001", "name": "Ground Beef", "quantity": 1.0, "price": 8.99},
    {"product_id": "milk_001", "name": "Whole Milk", "quantity": 1.0, "price": 4.99},
]

# Analyze
result = cac.analyze_basket(basket)

# View results
print(f"Emissions: {result.emissions:.1f} kg CO2e")
print(f"Savings potential: {result.cog:.1f} kg CO2e ({result.cog_ratio*100:.1f}%)")
print(f"Explanation: {result.explanation}")
```

### 4. Start the API Server

```bash
# Option 1: Using Make
make run

# Option 2: Direct command
uvicorn cac.api.checkout_api:app --reload

# Option 3: Docker
make docker-up
```

API will be available at: http://localhost:8000

### 5. Test the API

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "basket": [
      {"product_id": "beef_001", "quantity": 1.0, "price": 8.99, "name": "Ground Beef"}
    ]
  }'
```

## 📊 Key Features

### Novel Carbon Metrics

1. **COG** - Carbon Opportunity Gap: Maximum achievable reduction
2. **BAE** - Behavior-Adjusted Emissions: Realistic expected reduction
3. **RACS** - Risk-Adjusted Carbon Score: Upper-bound with uncertainty
4. **MAC_basket** - Marginal Abatement Cost: Cost per kg CO2e avoided
5. **RPE** - Recurring Purchase Emissions: Annualized impact
6. **CHCS** - Composite Carbon-Health Score: Joint optimization

### System Components

- **LCA Engine**: Integrates Poore & Nemecek, Open Food Facts, SU-EATABLE LIFE
- **Optimizer**: Beam search for low-carbon baskets
- **Behavior Model**: Predicts swap acceptance probability
- **GenAI**: LLM-powered persuasive explanations
- **MCP**: Audit-ready compliance framework

## 📖 Next Steps

- Read [API Documentation](docs/API.md)
- Explore [Architecture](docs/ARCHITECTURE.md)
- Learn about [Novel Metrics](docs/METRICS.md)
- Run [Example Scripts](examples/)
- Try the [Demo Notebook](notebooks/demo.ipynb)

## 🧪 Run Tests

```bash
make test
```

## 🐛 Troubleshooting

**Issue**: Import errors
**Solution**: Ensure you've installed the package: `pip install -e .`

**Issue**: API won't start
**Solution**: Check port 8000 is available: `lsof -i :8000`

**Issue**: LLM explanations not working
**Solution**: Set `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` in `.env`

## 📚 Documentation

- [Complete Project Structure](PROJECT_STRUCTURE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Contributing Guidelines](CONTRIBUTING.md)

## 📄 Paper Reference

Based on: "Carbon-Aware Checkout: A Novel AI System for Real-Time Basket-Level Emissions Scoring, Behavior-Adjusted Optimization, and GenAI-Driven Low-Carbon Decision Making in E-Commerce" by Kapil Poreddy

## 📧 Contact

For questions or issues, please open a GitHub issue or contact: poreddykapil@ieee.org

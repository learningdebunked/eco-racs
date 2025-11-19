# Carbon-Aware Checkout (CAC)

> A novel AI system for real-time basket-level emissions scoring, behavior-adjusted optimization, and GenAI-driven low-carbon decision making in e-commerce.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 📋 Overview

CAC is a complete, production-ready implementation of the research paper "Carbon-Aware Checkout" by Kapil Poreddy. It integrates life-cycle assessment (LCA), machine learning, uncertainty modeling, optimization, and large language models orchestrated via the Model Context Protocol (MCP) to deliver real-time carbon intelligence at e-commerce checkout.

**Key Innovation**: Unlike static product-level carbon labels, CAC provides dynamic basket-level optimization at the moment of highest decision leverage—checkout.

## ✨ Key Features

- 🌍 **Real-time basket-level carbon scoring** with uncertainty quantification (RACS)
- 🎯 **Behavior-adjusted emissions forecasting** using ML acceptance models (BAE)
- 💰 **Cost-constrained low-carbon swap recommendations** via beam search optimization
- 🤖 **GenAI-powered persuasive explanations** using OpenAI/Anthropic LLMs
- ⚖️ **FTC Green Guides & EU Green Claims Directive compliance** via MCP audit trail
- 📊 **Six novel carbon metrics**: COG, BAE, RACS, MAC_basket, RPE, CHCS

## 🏗️ Architecture

```
carbon-aware-checkout/
├── src/cac/
│   ├── core.py                    # Main orchestrator
│   ├── metrics.py                 # 6 novel carbon metrics
│   ├── lca/                       # Life-cycle assessment engine
│   ├── optimization/              # Low-carbon basket optimization
│   ├── behavior/                  # Behavioral modeling & prediction
│   ├── genai/                     # LLM-based explanation generation
│   ├── mcp/                       # Model Context Protocol tools
│   ├── data/                      # Data integration & processing
│   └── api/                       # REST API endpoints
├── tests/                         # Comprehensive test suite
├── docs/                          # Full documentation
├── examples/                      # Usage examples
└── scripts/                       # Utility scripts
```

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/carbon-aware-checkout.git
cd carbon-aware-checkout

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### Basic Usage

```python
from cac import CarbonAwareCheckout

# Initialize system
cac = CarbonAwareCheckout()

# Analyze a basket
basket = [
    {"product_id": "beef_001", "name": "Ground Beef", "quantity": 1.0, "price": 8.99},
    {"product_id": "milk_001", "name": "Whole Milk", "quantity": 1.0, "price": 4.99},
]

result = cac.analyze_basket(basket)

# View results
print(f"Emissions: {result.emissions:.1f} kg CO2e")
print(f"Carbon Opportunity Gap: {result.cog:.1f} kg CO2e ({result.cog_ratio*100:.1f}%)")
print(f"Behavior-Adjusted Savings: {result.bae:.1f} kg CO2e")
print(f"Explanation: {result.explanation}")
```

### Start API Server

```bash
# Using Make
make run

# Or directly
uvicorn cac.api.checkout_api:app --reload

# Or with Docker
make docker-up
```

API available at: http://localhost:8000

## 📊 Novel Carbon Metrics

CAC introduces six novel metrics designed specifically for retail checkout:

| Metric | Formula | Purpose |
|--------|---------|---------|
| **COG** | `E(B) - E(B*)` | Maximum achievable emissions reduction |
| **BAE** | `Σ ps * ΔEs` | Expected reduction with user acceptance |
| **RACS** | `E + zα*sqrt(Var)` | Upper-bound emissions with uncertainty |
| **MAC_basket** | `ΔC / ΔE` | Cost per kg CO2e avoided |
| **RPE** | `Σ freq * E` | Annualized recurring impact |
| **CHCS** | `λ*(1-E) + (1-λ)*H` | Joint carbon-health optimization |

See [docs/METRICS.md](docs/METRICS.md) for detailed explanations.

## 📈 Paper Results

Implementation enables reproduction of key findings:

- **15.7%** median emissions reduction
- **±1.9%** average cost change
- **36% vs 17%** acceptance rate (conversational vs numeric labels)
- **$0.38/kg CO2e** median marginal abatement cost

Run experiments: `python scripts/run_experiments.py`

## 🛠️ Technology Stack

- **Core**: Python 3.9+, NumPy, Pandas
- **ML**: Scikit-learn, PyTorch
- **LLM**: OpenAI, Anthropic, Transformers
- **API**: FastAPI, Uvicorn
- **Database**: PostgreSQL, Redis
- **Testing**: Pytest
- **Deployment**: Docker, Docker Compose

## 📚 Documentation

- [Quick Start Guide](QUICKSTART.md) - Get started in 5 minutes
- [API Documentation](docs/API.md) - REST API reference
- [Architecture](docs/ARCHITECTURE.md) - System design
- [Novel Metrics](docs/METRICS.md) - Detailed metric explanations
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment
- [Paper Implementation Map](docs/PAPER_IMPLEMENTATION_MAP.md) - Paper-to-code mapping

## 🧪 Testing

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_metrics.py -v

# With coverage
pytest --cov=src/cac --cov-report=html
```

## 🐳 Docker Deployment

```bash
# Build and start all services
make docker-up

# Stop services
make docker-down
```

Services include: API, PostgreSQL, Redis

## 📊 Project Statistics

- **1,372** lines of Python code
- **50** total project files
- **7** core modules
- **6** novel metrics implemented
- **4** test suites
- **10** documentation files

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 Citation

If you use this implementation, please cite:

```bibtex
@article{poreddy2025carbon,
  title={Carbon-Aware Checkout: A Novel AI System for Real-Time Basket-Level 
         Emissions Scoring, Behavior-Adjusted Optimization, and GenAI-Driven 
         Low-Carbon Decision Making in E-Commerce},
  author={Poreddy, Kapil},
  year={2025}
}
```

## 📧 Contact

- **Author**: Kapil Poreddy
- **Email**: poreddykapil@ieee.org
- **Issues**: [GitHub Issues](https://github.com/yourusername/carbon-aware-checkout/issues)

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

Based on research integrating:
- Poore & Nemecek (2018) - Food LCA meta-analysis
- Instacart Online Grocery Shopping Dataset
- Open Food Facts & SU-EATABLE LIFE databases

---

**Status**: ✅ Production-ready implementation  
**Version**: 0.1.0  
**Last Updated**: November 19, 2025

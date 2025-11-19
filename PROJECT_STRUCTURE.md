# Carbon-Aware Checkout - Project Structure

## Complete Directory Tree

```
carbon-aware-checkout/
├── README.md                          # Project overview and quick start
├── LICENSE                            # MIT License
├── setup.py                           # Package installation
├── requirements.txt                   # Python dependencies
├── pytest.ini                         # Test configuration
├── Makefile                           # Build and run commands
├── Dockerfile                         # Container image
├── docker-compose.yml                 # Multi-container setup
├── .gitignore                         # Git ignore patterns
├── .env.example                       # Environment variables template
├── PROJECT_STRUCTURE.md               # This file
│
├── src/cac/                           # Main source code
│   ├── __init__.py                    # Package initialization
│   ├── core.py                        # Main orchestrator
│   ├── metrics.py                     # Novel carbon metrics (COG, BAE, RACS, etc.)
│   │
│   ├── lca/                           # Life-Cycle Assessment
│   │   ├── __init__.py
│   │   └── emissions_engine.py        # Basket emissions calculation
│   │
│   ├── optimization/                  # Low-carbon optimization
│   │   ├── __init__.py
│   │   └── basket_optimizer.py        # Beam search optimizer
│   │
│   ├── behavior/                      # Behavioral modeling
│   │   ├── __init__.py
│   │   └── acceptance_model.py        # Swap acceptance prediction
│   │
│   ├── genai/                         # GenAI explanations
│   │   ├── __init__.py
│   │   └── explanation_generator.py   # LLM-powered messaging
│   │
│   ├── mcp/                           # Model Context Protocol
│   │   ├── __init__.py
│   │   └── mcp_orchestrator.py        # MCP tool orchestration
│   │
│   ├── data/                          # Data processing
│   │   ├── __init__.py
│   │   ├── data_loader.py             # Instacart dataset loader
│   │   └── lca_integrator.py          # LCA data integration
│   │
│   └── api/                           # REST API
│       ├── __init__.py
│       └── checkout_api.py            # FastAPI endpoints
│
├── tests/                             # Test suite
│   ├── __init__.py
│   ├── test_core.py                   # Core system tests
│   ├── test_metrics.py                # Metrics tests
│   ├── test_optimization.py           # Optimization tests
│   └── test_api.py                    # API tests
│
├── config/                            # Configuration
│   └── config.yaml                    # System configuration
│
├── scripts/                           # Utility scripts
│   ├── start_api.sh                   # Start API server
│   └── run_experiments.py             # Run paper experiments
│
├── docs/                              # Documentation
│   ├── API.md                         # API documentation
│   ├── ARCHITECTURE.md                # System architecture
│   └── METRICS.md                     # Novel metrics guide
│
├── notebooks/                         # Jupyter notebooks
│   └── demo.ipynb                     # Demo notebook
│
├── data/                              # Data directory (gitignored)
│   ├── raw/                           # Raw datasets
│   │   ├── products.csv
│   │   ├── orders.csv
│   │   └── order_products__train.csv
│   └── processed/                     # Processed data
│
├── models/                            # Trained models (gitignored)
│   └── checkpoints/
│
├── logs/                              # Logs (gitignored)
│   └── audit.json
│
└── results/                           # Experiment results
    └── experiment_results.csv
```

## Module Descriptions

### Core Modules

**src/cac/core.py**
- Main `CarbonAwareCheckout` orchestrator
- Coordinates all subsystems
- Implements end-to-end basket analysis pipeline

**src/cac/metrics.py**
- Implements 6 novel carbon metrics:
  - COG (Carbon Opportunity Gap)
  - BAE (Behavior-Adjusted Emissions)
  - RACS (Risk-Adjusted Carbon Score)
  - MAC_basket (Marginal Abatement Cost)
  - RPE (Recurring Purchase Emissions)
  - CHCS (Composite Carbon-Health Score)

### LCA Module

**src/cac/lca/emissions_engine.py**
- Computes basket-level emissions
- Propagates LCA uncertainty
- Integrates multiple data sources

### Optimization Module

**src/cac/optimization/basket_optimizer.py**
- Beam search algorithm (Algorithm 1 from paper)
- Multi-objective optimization
- Constraint satisfaction (price, dietary, allergen)

### Behavior Module

**src/cac/behavior/acceptance_model.py**
- Predicts swap acceptance probability
- Enables BAE calculation
- Supports multiple message types

### GenAI Module

**src/cac/genai/explanation_generator.py**
- LLM-powered explanations
- Supports OpenAI and Anthropic
- Multiple message framings

### MCP Module

**src/cac/mcp/mcp_orchestrator.py**
- Deterministic tool orchestration
- Audit logging for compliance
- FTC Green Guides & EU Green Claims alignment

### Data Module

**src/cac/data/data_loader.py**
- Loads Instacart dataset
- Loads LCA databases

**src/cac/data/lca_integrator.py**
- Merges multiple LCA sources
- Product-to-category mapping
- Unit normalization

### API Module

**src/cac/api/checkout_api.py**
- FastAPI REST endpoints
- Real-time checkout integration
- Swagger/OpenAPI documentation

## Key Files

**requirements.txt**
- All Python dependencies
- Includes numpy, pandas, scikit-learn, torch, transformers, fastapi, etc.

**setup.py**
- Package installation configuration
- Entry points and metadata

**config/config.yaml**
- System configuration
- LCA sources, optimization weights, LLM settings

**Dockerfile & docker-compose.yml**
- Containerized deployment
- Includes PostgreSQL and Redis

## Data Sources

The system integrates:
1. **Instacart Online Grocery Shopping Dataset** (3.1M orders, 50k products)
2. **Poore & Nemecek (2018)** - Food LCA meta-analysis
3. **Open Food Facts** - Product attributes and Eco-Score
4. **SU-EATABLE LIFE** - Commodity-level footprints

## Running the System

```bash
# Install
make install

# Run tests
make test

# Start API
make run

# Run experiments
python scripts/run_experiments.py

# Docker deployment
make docker-up
```

## Compliance

- FTC Green Guides compliant
- EU Green Claims Directive ready
- Full audit trail via MCP
- Reproducible carbon claims

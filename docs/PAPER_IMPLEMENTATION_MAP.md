# Paper to Implementation Mapping

This document maps sections of the research paper to the actual code implementation.

## Paper Structure → Code Mapping

### Section I: Introduction
**Paper Concepts** → **Implementation**
- Checkout as intervention point → `src/cac/api/checkout_api.py`
- Real-time carbon transparency → `src/cac/core.py::analyze_basket()`

### Section III: Regulatory Landscape
**Paper Concepts** → **Implementation**
- FTC Green Guides compliance → `src/cac/mcp/mcp_orchestrator.py::audit_log()`
- EU Green Claims Directive → MCP audit trail system

### Section IV: Datasets
**Paper Concepts** → **Implementation**
- Instacart dataset (3.1M orders) → `src/cac/data/data_loader.py::load_instacart_dataset()`
- Poore & Nemecek LCA data → `src/cac/data/data_loader.py::load_poore_nemecek_data()`
- Product-level integration → `src/cac/data/lca_integrator.py::merge_footprints()`

### Section V: Problem Formulation
**Paper Concepts** → **Implementation**
- Basket B = {(i, qi)} → Python dict/list structure
- Emissions E(B) = Σ fi*qi → `src/cac/lca/emissions_engine.py::calculate_basket_emissions()`
- Low-carbon alternatives S(i) → `src/cac/optimization/basket_optimizer.py::get_substitutes()`

### Section VI: Novel Carbon Metrics

#### Equation (4): Carbon Opportunity Gap
```
COG(B) = E(B) - E(B*)
```
**Implementation:** `src/cac/metrics.py::carbon_opportunity_gap()`

#### Equation (7-8): Behavior-Adjusted Emissions
```
BAE(B) = Σ ps * ΔEs
```
**Implementation:** `src/cac/metrics.py::behavior_adjusted_emissions()`

#### Equation (12): Risk-Adjusted Carbon Score
```
RACSα(B) = E[E(B)] + zα * sqrt(Var(E(B)))
```
**Implementation:** `src/cac/metrics.py::risk_adjusted_carbon_score()`

#### Equation (13): Marginal Abatement Cost
```
MAC_basket(B) = (C(B*) - C(B)) / (E(B) - E(B*))
```
**Implementation:** `src/cac/metrics.py::marginal_abatement_cost()`

#### Equation (15): Recurring Purchase Emissions
```
RPE(u) = Σ f_freq_i,u * E(purchase_i)
```
**Implementation:** `src/cac/metrics.py::recurring_purchase_emissions()`

#### Equation (17): Composite Carbon-Health Score
```
CHCS(B) = λ*(1-Enorm(B)) + (1-λ)*H(B)
```
**Implementation:** `src/cac/metrics.py::composite_carbon_health_score()`

### Section VII: System Architecture and MCP Integration
**Paper Concepts** → **Implementation**
- MCP Orchestration Layer → `src/cac/mcp/mcp_orchestrator.py`
- MCP Tools (calculate_emissions, optimize_basket, etc.) → Individual tool methods
- Audit logging → `_tool_audit_log()` method

### Section VIII: Low-Carbon Swap Optimization

#### Algorithm 1: Beam Search
**Paper Pseudocode** → **Implementation**
```
Algorithm 1: Beam Search for Low-Carbon Basket Optimization
```
**Implementation:** `src/cac/optimization/basket_optimizer.py::optimize_basket()`

#### Equation (18): Multi-Objective Function
```
J(B') = α*E(B') + β*C(B') + γ*D(B,B') + δ*(1-H(B'))
```
**Implementation:** `src/cac/optimization/basket_optimizer.py::_compute_objective()`

### Section IX: GenAI Behavior Engine
**Paper Concepts** → **Implementation**
- Message types (numeric, conversational, etc.) → `src/cac/genai/explanation_generator.py::generate()`
- LLM-based explanations → `_generate_conversational_explanation()`
- Behavioral model ps → `src/cac/behavior/acceptance_model.py::predict_acceptance()`

### Section X: Experiments
**Paper Concepts** → **Implementation**
- 500k basket analysis → `scripts/run_experiments.py`
- Metrics computation → Results DataFrame in experiment script
- A/B testing framework → Experimental conditions in script

### Section XI: Results
**Paper Claims** → **Validation**
- "Median 15.7% reduction" → Computed in `run_experiments.py`
- "±1.9% cost change" → Tracked in results DataFrame
- "36% vs 17% acceptance" → Message type comparison in behavior model

## Key Implementation Decisions

### 1. Modular Architecture
Paper describes integrated system → Implemented as separate modules with clear interfaces

### 2. MCP for Compliance
Paper emphasizes regulatory alignment → MCP orchestrator provides audit trail

### 3. Extensible Design
Paper uses specific datasets → Implementation supports pluggable data sources

### 4. Production-Ready
Paper is research prototype → Implementation includes API, Docker, tests

## File-to-Section Quick Reference

| Paper Section | Primary Implementation File |
|--------------|----------------------------|
| Novel Metrics (VI) | `src/cac/metrics.py` |
| Optimization (VIII) | `src/cac/optimization/basket_optimizer.py` |
| LCA Engine | `src/cac/lca/emissions_engine.py` |
| Behavior Model (IX) | `src/cac/behavior/acceptance_model.py` |
| GenAI (IX) | `src/cac/genai/explanation_generator.py` |
| MCP (VII) | `src/cac/mcp/mcp_orchestrator.py` |
| Experiments (X) | `scripts/run_experiments.py` |
| API Integration | `src/cac/api/checkout_api.py` |

## Testing Coverage

| Paper Component | Test File |
|----------------|-----------|
| Core System | `tests/test_core.py` |
| Novel Metrics | `tests/test_metrics.py` |
| Optimization | `tests/test_optimization.py` |
| API Endpoints | `tests/test_api.py` |

## Running Paper Experiments

To reproduce the paper's experimental results:

```bash
# Process data
python scripts/process_data.py

# Run experiments on 500k baskets
python scripts/run_experiments.py

# Results saved to results/experiment_results.csv
```

## Citation

If you use this implementation, please cite the original paper:

```bibtex
@article{poreddy2025carbon,
  title={Carbon-Aware Checkout: A Novel AI System for Real-Time Basket-Level Emissions Scoring},
  author={Poreddy, Kapil},
  journal={arXiv preprint},
  year={2025}
}
```

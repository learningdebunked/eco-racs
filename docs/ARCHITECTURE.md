# Carbon-Aware Checkout Architecture

## System Overview

CAC is a modular system integrating LCA, ML, optimization, and GenAI for real-time carbon-aware checkout.

## Core Modules

### 1. LCA Module (`src/cac/lca/`)
- **EmissionsEngine**: Computes basket emissions with uncertainty
- Integrates Poore & Nemecek, Open Food Facts, SU-EATABLE LIFE

### 2. Optimization Module (`src/cac/optimization/`)
- **BasketOptimizer**: Beam search for low-carbon baskets
- Multi-objective optimization (emissions, cost, health, similarity)

### 3. Behavior Module (`src/cac/behavior/`)
- **AcceptanceModel**: Predicts swap acceptance probability
- Enables BAE (Behavior-Adjusted Emissions) calculation

### 4. GenAI Module (`src/cac/genai/`)
- **ExplanationGenerator**: LLM-powered persuasive explanations
- Supports OpenAI, Anthropic models

### 5. MCP Module (`src/cac/mcp/`)
- **MCPOrchestrator**: Deterministic tool orchestration
- Audit logging for FTC/EU compliance

### 6. API Module (`src/cac/api/`)
- FastAPI REST endpoints
- Real-time checkout integration

## Data Flow

```
Basket → EmissionsEngine → BasketOptimizer → AcceptanceModel → ExplanationGenerator → Response
                ↓                                                        ↓
           MCP Audit Log ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

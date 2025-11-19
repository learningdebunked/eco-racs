# Carbon-Aware Checkout - System Flow

## High-Level Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        E-Commerce Checkout                       │
│                    (User reviews basket)                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     CAC API Endpoint                             │
│                  POST /analyze (basket)                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  CarbonAwareCheckout Core                        │
│                    (Main Orchestrator)                           │
└─────┬──────────┬──────────┬──────────┬──────────┬──────────────┘
      │          │          │          │          │
      ▼          ▼          ▼          ▼          ▼
┌──────────┐ ┌──────┐ ┌──────────┐ ┌────────┐ ┌────────┐
│   LCA    │ │ Opt  │ │ Behavior │ │ GenAI  │ │  MCP   │
│  Engine  │ │ imize│ │  Model   │ │ Engine │ │  Audit │
└──────────┘ └──────┘ └──────────┘ └────────┘ └────────┘
      │          │          │          │          │
      ▼          ▼          ▼          ▼          ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Response to User                          │
│  • Carbon score (E, COG, BAE, RACS, MAC, RPE, CHCS)            │
│  • Swap recommendations with acceptance probabilities           │
│  • LLM-generated persuasive explanation                         │
│  • Audit trail for compliance                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Detailed Module Interactions

### 1. Emissions Calculation Flow

```
Basket → EmissionsEngine
           │
           ├─→ Load product footprints from LCA DB
           │   (Poore & Nemecek, Open Food Facts, etc.)
           │
           ├─→ Calculate E(B) = Σ fi * qi
           │
           ├─→ Propagate uncertainty: Var(E(B)) = Σ σi² * qi²
           │
           └─→ Compute RACS = E[E(B)] + zα * sqrt(Var(E(B)))
                 │
                 ▼
           Return: {emissions, variance, racs, product_emissions}
```

### 2. Optimization Flow

```
Basket + Constraints → BasketOptimizer
                         │
                         ├─→ Initialize beam with original basket
                         │
                         ├─→ For each product:
                         │     ├─→ Get substitutes S(i)
                         │     ├─→ Apply swaps
                         │     ├─→ Check constraints
                         │     └─→ Compute objective J(B')
                         │
                         ├─→ Keep top-K baskets (beam search)
                         │
                         └─→ Select best basket B*
                               │
                               ▼
                         Compute metrics:
                         • COG = E(B) - E(B*)
                         • MAC = (C(B*) - C(B)) / (E(B) - E(B*))
                               │
                               ▼
                         Return: {optimized_basket, cog, mac, ...}
```

### 3. Behavioral Modeling Flow

```
Swaps + User Context → AcceptanceModel
                         │
                         ├─→ For each swap s:
                         │     ├─→ Extract features
                         │     │   (price_change, emissions_reduction,
                         │     │    similarity, brand_change, etc.)
                         │     │
                         │     ├─→ Predict acceptance: ps = P(accept | features)
                         │     │
                         │     └─→ Compute contribution: ps * ΔEs
                         │
                         └─→ Aggregate BAE = Σ ps * ΔEs
                               │
                               ▼
                         Return: {swaps_with_probs, bae, avg_acceptance}
```

### 4. GenAI Explanation Flow

```
Context → ExplanationGenerator
           │
           ├─→ Build prompt with:
           │   • Emissions data
           │   • Optimization results
           │   • Top swaps
           │   • User context
           │
           ├─→ Call LLM (OpenAI/Anthropic)
           │   with system prompt:
           │   "Generate friendly, persuasive
           │    explanation based on data..."
           │
           └─→ Return conversational explanation
                 │
                 ▼
           "Your basket has a carbon footprint of 45.2 kg CO2e.
            We found simple swaps that could reduce your impact
            by 7.1 kg (15.7%) with minimal cost change..."
```

### 5. MCP Orchestration Flow

```
Tool Call → MCPOrchestrator
             │
             ├─→ Validate tool name
             │
             ├─→ Execute tool:
             │   • calculate_basket_emissions
             │   • optimize_basket
             │   • simulate_swaps
             │   • generate_explanation
             │   • audit_log
             │
             ├─→ Log call for audit trail:
             │   {tool, timestamp, params, result}
             │
             └─→ Return result with metadata
                   │
                   ▼
             Audit log persisted for compliance
```

## Complete Request-Response Cycle

```
1. User submits basket at checkout
   ↓
2. API receives POST /analyze request
   ↓
3. CarbonAwareCheckout.analyze_basket() called
   ↓
4. MCP tool: calculate_basket_emissions
   ├─→ EmissionsEngine computes E(B), RACS
   └─→ Returns emissions data
   ↓
5. MCP tool: optimize_basket
   ├─→ BasketOptimizer runs beam search
   └─→ Returns B*, COG, MAC
   ↓
6. MCP tool: simulate_swaps
   ├─→ AcceptanceModel predicts ps for each swap
   └─→ Returns swaps with probabilities, BAE
   ↓
7. ExplanationGenerator creates message
   ├─→ Builds prompt from all data
   ├─→ Calls LLM
   └─→ Returns conversational explanation
   ↓
8. MCP tool: audit_log
   └─→ Persists all data for compliance
   ↓
9. Response assembled with:
   • All metrics (E, COG, BAE, RACS, MAC, RPE, CHCS)
   • Swap recommendations
   • Explanation
   • Acceptance rates
   ↓
10. JSON response returned to checkout UI
   ↓
11. User sees:
    • Carbon score
    • Swap suggestions
    • Persuasive explanation
    • Accept/decline options
```

## Data Dependencies

```
┌─────────────────────────────────────────────────────────────┐
│                      Data Sources                            │
├─────────────────────────────────────────────────────────────┤
│  • Instacart Dataset (3.1M orders, 50k products)            │
│  • Poore & Nemecek (2018) - Food LCA meta-analysis         │
│  • Open Food Facts - Product attributes & Eco-Score        │
│  • SU-EATABLE LIFE - Commodity footprints                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Data Integration Layer                      │
│              (LCAIntegrator, DataLoader)                     │
├─────────────────────────────────────────────────────────────┤
│  • Product-to-category mapping                              │
│  • Footprint database construction                          │
│  • Unit normalization                                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Processed Footprint DB                      │
│         {product_id → {emissions, variance, ...}}           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
                   Used by all modules
```

## Metric Computation Pipeline

```
Basket B
  │
  ├─→ E(B) = Σ fi * qi                    [Baseline Emissions]
  │
  ├─→ Optimize → B*
  │     │
  │     ├─→ COG = E(B) - E(B*)            [Opportunity Gap]
  │     │
  │     └─→ MAC = ΔC / ΔE                 [Abatement Cost]
  │
  ├─→ Simulate swaps → {ps, ΔEs}
  │     │
  │     └─→ BAE = Σ ps * ΔEs              [Behavior-Adjusted]
  │
  ├─→ Propagate uncertainty
  │     │
  │     └─→ RACS = E + zα*sqrt(Var)       [Risk-Adjusted]
  │
  ├─→ Annualize
  │     │
  │     └─→ RPE = Σ freq * E              [Recurring Impact]
  │
  └─→ Joint optimization
        │
        └─→ CHCS = λ*(1-E) + (1-λ)*H      [Carbon-Health]
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Load Balancer                           │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌────────┐      ┌────────┐      ┌────────┐
    │ CAC    │      │ CAC    │      │ CAC    │
    │ API    │      │ API    │      │ API    │
    │ (Pod 1)│      │ (Pod 2)│      │ (Pod 3)│
    └───┬────┘      └───┬────┘      └───┬────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
         ┌──────────────┼──────────────┐
         ▼              ▼              ▼
    ┌─────────┐   ┌─────────┐   ┌─────────┐
    │PostgreSQL│   │  Redis  │   │   LLM   │
    │   (DB)   │   │ (Cache) │   │   API   │
    └─────────┘   └─────────┘   └─────────┘
```

## Key Design Principles

1. **Modularity**: Each component is independent and testable
2. **Extensibility**: Easy to add new LCA sources or metrics
3. **Compliance**: MCP provides full audit trail
4. **Performance**: Caching and optimization for real-time response
5. **Reliability**: Error handling and fallbacks throughout
6. **Transparency**: All calculations logged and explainable

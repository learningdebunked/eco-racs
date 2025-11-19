# Novel Carbon Metrics

## Overview

CAC introduces six novel metrics designed specifically for retail checkout decision-making.

## 1. Carbon Opportunity Gap (COG)

**Definition:**
```
COG(B) = E(B) - E(B*)
COG_ratio(B) = (E(B) - E(B*)) / E(B)
```

**Purpose:** Measures the maximum achievable emissions reduction given realistic constraints.

**Example:** A basket with 50 kg CO2e that can be optimized to 42 kg has COG = 8 kg (16%).

## 2. Behavior-Adjusted Emissions (BAE)

**Definition:**
```
BAE(B) = Σ p_s * ΔE_s
```

**Purpose:** Estimates realistic emissions reduction accounting for user acceptance probability.

**Example:** Three swaps with (p=0.8, ΔE=10), (p=0.5, ΔE=5), (p=0.3, ΔE=3) yield BAE = 11.4 kg.

## 3. Risk-Adjusted Carbon Score (RACS)

**Definition:**
```
RACS_α(B) = E[E(B)] + z_α * sqrt(Var(E(B)))
```

**Purpose:** Provides upper-bound emissions at confidence level α, accounting for LCA uncertainty.

## 4. Basket Marginal Abatement Cost (MAC_basket)

**Definition:**
```
MAC_basket(B) = (C(B*) - C(B)) / (E(B) - E(B*))
```

**Purpose:** Cost per kg CO2e avoided, connecting household choices to climate economics.

## 5. Recurring Purchase Emissions (RPE)

**Definition:**
```
RPE = Σ f_freq_i * E(purchase_i)
```

**Purpose:** Annualized impact of recurring purchases.

## 6. Composite Carbon-Health Score (CHCS)

**Definition:**
```
CHCS(B) = λ * (1 - E_norm(B)) + (1 - λ) * H(B)
```

**Purpose:** Joint optimization of carbon and nutritional outcomes.

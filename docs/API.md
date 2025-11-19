# Carbon-Aware Checkout API Documentation

## Overview

The CAC API provides real-time basket-level carbon scoring and optimization for e-commerce checkout flows.

## Base URL

```
http://localhost:8000
```

## Endpoints

### POST /analyze

Analyze a shopping basket and get carbon score with optimization recommendations.

**Request Body:**

```json
{
  "basket": [
    {
      "product_id": "12345",
      "quantity": 2.0,
      "price": 8.99,
      "name": "Ground Beef"
    }
  ],
  "user_id": "user_123",
  "constraints": {
    "max_price_delta": 0.03,
    "dietary_preference": "vegetarian"
  }
}
```

**Response:**

```json
{
  "basket_id": "basket_001",
  "emissions": 45.2,
  "emissions_optimized": 38.1,
  "cog": 7.1,
  "cog_ratio": 0.157,
  "bae": 5.2,
  "racs": 48.5,
  "mac_basket": 0.38,
  "cost_original": 45.50,
  "cost_optimized": 46.35,
  "swaps": [
    {
      "original_product_id": "12345",
      "substitute_product_id": "67890",
      "emissions_reduction": 7.1,
      "price_change": 0.85,
      "acceptance_prob": 0.73,
      "description": "Swap Ground Beef for Plant-Based Alternative"
    }
  ],
  "explanation": "Your basket has a carbon footprint of 45.2 kg CO2e. We found simple swaps that could reduce your impact by 7.1 kg (15.7%) with minimal cost change. Switching from beef to a plant-based alternative saves the most emissions!",
  "acceptance_rate": 0.73
}
```

### GET /metrics

Get system-wide metrics.

**Response:**

```json
{
  "total_requests": 125000,
  "avg_emissions_reduction": 0.157,
  "avg_acceptance_rate": 0.36
}
```

### GET /audit/{basket_id}

Retrieve audit log for a specific basket (for compliance).

**Response:**

```json
{
  "basket_id": "basket_001",
  "audit_log": [
    {
      "timestamp": "2025-11-19T10:30:00Z",
      "event": "emissions_calculated",
      "data": {...}
    }
  ]
}
```

## Novel Metrics

- **COG (Carbon Opportunity Gap)**: Maximum achievable emissions reduction
- **BAE (Behavior-Adjusted Emissions)**: Expected reduction accounting for acceptance probability
- **RACS (Risk-Adjusted Carbon Score)**: Upper-bound emissions at 95% confidence
- **MAC_basket**: Marginal abatement cost ($/kg CO2e)
- **RPE (Recurring Purchase Emissions)**: Annualized impact
- **CHCS (Composite Carbon-Health Score)**: Joint carbon-nutrition optimization

## Compliance

All carbon claims are:
- Based on peer-reviewed LCA data (Poore & Nemecek 2018, Open Food Facts)
- Auditable via MCP tool logs
- Aligned with FTC Green Guides and EU Green Claims Directive

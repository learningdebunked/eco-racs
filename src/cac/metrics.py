"""Novel carbon metrics for Carbon-Aware Checkout"""

import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class BasketMetrics:
    """Container for all basket-level carbon metrics"""
    emissions: float
    cog: float
    cog_ratio: float
    bae: float
    racs: float
    mac_basket: float
    rpe: float
    chcs: float


class CarbonMetrics:
    """Compute novel carbon metrics for retail checkout"""
    
    def carbon_opportunity_gap(
        self,
        emissions_original: float,
        emissions_optimized: float
    ) -> Tuple[float, float]:
        """
        Compute Carbon Opportunity Gap (COG)
        
        COG(B) = E(B) - E(B*)
        COG_ratio(B) = (E(B) - E(B*)) / E(B)
        """
        cog = emissions_original - emissions_optimized
        cog_ratio = cog / emissions_original if emissions_original > 0 else 0.0
        return cog, cog_ratio
    
    def behavior_adjusted_emissions(
        self,
        swaps: List[Dict]
    ) -> float:
        """
        Compute Behavior-Adjusted Emissions (BAE)
        
        BAE(B) = Σ p_s * ΔE_s
        where p_s is acceptance probability and ΔE_s is emissions reduction
        """
        bae = sum(
            swap["acceptance_prob"] * swap["emissions_reduction"]
            for swap in swaps
        )
        return bae
    
    def risk_adjusted_carbon_score(
        self,
        emissions_mean: float,
        emissions_variance: float,
        confidence_level: float = 0.95
    ) -> float:
        """
        Compute Risk-Adjusted Carbon Score (RACS)
        
        RACS_α(B) = E[E(B)] + z_α * sqrt(Var(E(B)))
        """
        z_alpha = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}.get(confidence_level, 1.96)
        racs = emissions_mean + z_alpha * np.sqrt(emissions_variance)
        return racs
    
    def marginal_abatement_cost(
        self,
        cost_original: float,
        cost_optimized: float,
        emissions_original: float,
        emissions_optimized: float
    ) -> float:
        """
        Compute Basket Marginal Abatement Cost (MAC_basket)
        
        MAC_basket(B) = (C(B*) - C(B)) / (E(B) - E(B*))
        """
        emissions_reduction = emissions_original - emissions_optimized
        if emissions_reduction <= 0:
            return float('inf')
        
        cost_change = cost_optimized - cost_original
        mac = cost_change / emissions_reduction
        return mac
    
    def recurring_purchase_emissions(
        self,
        basket: List[Dict],
        purchase_frequencies: Dict[str, float]
    ) -> float:
        """
        Compute Recurring Purchase Emissions (RPE)
        
        RPE = Σ f_freq_i * E(single purchase of i)
        """
        rpe = sum(
            purchase_frequencies.get(item["product_id"], 1.0) * item["emissions"]
            for item in basket
        )
        return rpe
    
    def composite_carbon_health_score(
        self,
        emissions_normalized: float,
        health_score: float,
        lambda_weight: float = 0.5
    ) -> float:
        """
        Compute Composite Carbon-Health Score (CHCS)
        
        CHCS(B) = λ * (1 - E_norm(B)) + (1 - λ) * H(B)
        """
        chcs = lambda_weight * (1 - emissions_normalized) + (1 - lambda_weight) * health_score
        return chcs

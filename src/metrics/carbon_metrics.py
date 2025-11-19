"""Implementation of novel carbon metrics: COG, BAE, RACS, MAC, RPE, CHCS"""
import numpy as np
from typing import List, Tuple
from src.data.basket import Basket


class CarbonMetrics:
    """Computes novel carbon metrics for baskets"""
    
    @staticmethod
    def carbon_opportunity_gap(original: Basket, optimized: Basket) -> Tuple[float, float]:
        """
        Calculate Carbon Opportunity Gap (COG)
        Returns: (absolute_gap, ratio)
        """
        e_original = original.total_emissions()
        e_optimized = optimized.total_emissions()
        
        cog_absolute = e_original - e_optimized
        cog_ratio = cog_absolute / e_original if e_original > 0 else 0.0
        
        return cog_absolute, cog_ratio
    
    @staticmethod
    def behavior_adjusted_emissions(
        original: Basket,
        swaps: List[Tuple[Basket, float]]  # (modified_basket, acceptance_prob)
    ) -> float:
        """
        Calculate Behavior-Adjusted Emissions (BAE)
        swaps: list of (basket_with_swap, acceptance_probability)
        Returns: expected emissions reduction
        """
        e_original = original.total_emissions()
        bae = 0.0
        
        for modified_basket, p_accept in swaps:
            delta_e = e_original - modified_basket.total_emissions()
            bae += p_accept * delta_e
        
        return bae
    
    @staticmethod
    def risk_adjusted_carbon_score(basket: Basket, alpha: float = 0.95) -> float:
        """
        Calculate Risk-Adjusted Carbon Score (RACS)
        alpha: confidence level (default 0.95)
        Returns: upper bound emissions at confidence level alpha
        """
        # Calculate mean and variance
        mean_emissions = sum(p.emissions_mean * p.quantity_kg for p in basket.products)
        variance = sum((p.emissions_std * p.quantity_kg) ** 2 for p in basket.products)
        std_emissions = np.sqrt(variance)
        
        # Z-score for confidence level
        from scipy.stats import norm
        z_alpha = norm.ppf(alpha)
        
        racs = mean_emissions + z_alpha * std_emissions
        return racs
    
    @staticmethod
    def marginal_abatement_cost(original: Basket, optimized: Basket) -> float:
        """
        Calculate Basket Marginal Abatement Cost (MAC_basket)
        Returns: USD per kg CO2e avoided
        """
        delta_cost = optimized.total_cost() - original.total_cost()
        delta_emissions = original.total_emissions() - optimized.total_emissions()
        
        if delta_emissions <= 0:
            return float('inf')
        
        return delta_cost / delta_emissions
    
    @staticmethod
    def recurring_purchase_emissions(
        basket: Basket,
        annual_frequency: float = 52.0  # weekly purchases
    ) -> float:
        """
        Calculate Recurring Purchase Emissions (RPE)
        Returns: annual emissions from recurring purchases
        """
        return basket.total_emissions() * annual_frequency
    
    @staticmethod
    def composite_carbon_health_score(
        basket: Basket,
        lambda_carbon: float = 0.5,
        e_min: float = 0.0,
        e_max: float = 100.0
    ) -> float:
        """
        Calculate Composite Carbon-Health Score (CHCS)
        lambda_carbon: weight for carbon vs health (0 to 1)
        Returns: composite score (higher is better)
        """
        # Normalize emissions
        e_norm = (basket.total_emissions() - e_min) / (e_max - e_min)
        e_norm = np.clip(e_norm, 0, 1)
        
        # Calculate average health score
        health_scores = [p.health_score for p in basket.products if p.health_score is not None]
        h_avg = np.mean(health_scores) if health_scores else 0.5
        
        # Composite score
        chcs = lambda_carbon * (1 - e_norm) + (1 - lambda_carbon) * h_avg
        return chcs

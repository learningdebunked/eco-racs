"""Tests for Carbon Metrics"""

import pytest
from src.cac.metrics import CarbonMetrics


class TestCarbonMetrics:
    """Test suite for novel carbon metrics"""
    
    def setup_method(self):
        self.metrics = CarbonMetrics()
    
    def test_carbon_opportunity_gap(self):
        """Test COG calculation"""
        emissions_original = 100.0
        emissions_optimized = 84.3
        
        cog, cog_ratio = self.metrics.carbon_opportunity_gap(
            emissions_original, emissions_optimized
        )
        
        assert cog == pytest.approx(15.7)
        assert cog_ratio == pytest.approx(0.157)
    
    def test_behavior_adjusted_emissions(self):
        """Test BAE calculation"""
        swaps = [
            {"acceptance_prob": 0.8, "emissions_reduction": 10.0},
            {"acceptance_prob": 0.5, "emissions_reduction": 5.0},
            {"acceptance_prob": 0.3, "emissions_reduction": 3.0},
        ]
        
        bae = self.metrics.behavior_adjusted_emissions(swaps)
        
        expected = 0.8 * 10.0 + 0.5 * 5.0 + 0.3 * 3.0
        assert bae == pytest.approx(expected)
    
    def test_risk_adjusted_carbon_score(self):
        """Test RACS calculation"""
        emissions_mean = 50.0
        emissions_variance = 25.0
        
        racs = self.metrics.risk_adjusted_carbon_score(
            emissions_mean, emissions_variance, confidence_level=0.95
        )
        
        # RACS = 50 + 1.96 * sqrt(25) = 50 + 9.8 = 59.8
        assert racs == pytest.approx(59.8)
    
    def test_marginal_abatement_cost(self):
        """Test MAC_basket calculation"""
        cost_original = 100.0
        cost_optimized = 101.9
        emissions_original = 50.0
        emissions_optimized = 42.15
        
        mac = self.metrics.marginal_abatement_cost(
            cost_original, cost_optimized,
            emissions_original, emissions_optimized
        )
        
        # MAC = (101.9 - 100) / (50 - 42.15) = 1.9 / 7.85 ≈ 0.242
        assert mac == pytest.approx(0.242, rel=0.01)
    
    def test_composite_carbon_health_score(self):
        """Test CHCS calculation"""
        emissions_normalized = 0.6
        health_score = 0.8
        lambda_weight = 0.5
        
        chcs = self.metrics.composite_carbon_health_score(
            emissions_normalized, health_score, lambda_weight
        )
        
        # CHCS = 0.5 * (1 - 0.6) + 0.5 * 0.8 = 0.2 + 0.4 = 0.6
        assert chcs == pytest.approx(0.6)

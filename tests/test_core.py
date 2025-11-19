"""Tests for Core CAC System"""

import pytest
from src.cac.core import CarbonAwareCheckout


class TestCarbonAwareCheckout:
    """Test suite for main CAC orchestrator"""
    
    def setup_method(self):
        self.cac = CarbonAwareCheckout()
    
    def test_analyze_basket_basic(self):
        """Test basic basket analysis"""
        basket = [
            {
                "basket_id": "test_001",
                "product_id": "beef_001",
                "name": "Ground Beef",
                "quantity": 1.0,
                "price": 8.99,
            },
            {
                "basket_id": "test_001",
                "product_id": "chicken_001",
                "name": "Chicken Breast",
                "quantity": 1.0,
                "price": 6.99,
            },
        ]
        
        result = self.cac.analyze_basket(basket)
        
        assert result.basket_id == "test_001"
        assert result.emissions > 0
        assert result.cog >= 0
        assert 0 <= result.cog_ratio <= 1
        assert result.explanation is not None
    
    def test_analyze_basket_with_constraints(self):
        """Test basket analysis with user constraints"""
        basket = [
            {
                "basket_id": "test_002",
                "product_id": "milk_001",
                "name": "Whole Milk",
                "quantity": 1.0,
                "price": 4.99,
            },
        ]
        
        user_context = {
            "dietary_preference": "vegetarian",
            "max_price_delta": 0.05,
        }
        
        result = self.cac.analyze_basket(basket, user_context)
        
        assert result.basket_id == "test_002"
        assert abs(result.cost_optimized - result.cost_original) / result.cost_original <= 0.05

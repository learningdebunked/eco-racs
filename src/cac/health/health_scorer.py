"""Health Score Calculator for Products"""

from typing import Dict, Optional
import numpy as np


class HealthScorer:
    """Calculate health scores for food products"""
    
    def __init__(self):
        self.health_db = self._build_health_database()
    
    def _build_health_database(self) -> Dict[str, float]:
        """Build health score database (0-1 scale, higher is healthier)"""
        # Based on nutritional guidelines and Nutri-Score principles
        return {
            # Meat & Poultry (moderate to low health scores)
            "Beef": 0.4,
            "Pork": 0.5,
            "Lamb & Mutton": 0.45,
            "Poultry Meat": 0.7,
            "Chicken": 0.7,
            "Fish": 0.85,
            "Prawns": 0.75,
            
            # Plant-based proteins (high health scores)
            "Tofu": 0.8,
            "Tempeh": 0.85,
            "Peas": 0.9,
            "Beans": 0.9,
            "Legumes": 0.9,
            "Nuts": 0.85,
            "Groundnuts": 0.8,
            "Other Pulses": 0.85,
            
            # Dairy (moderate health scores)
            "Milk": 0.6,
            "Cheese": 0.5,
            "Eggs": 0.65,
            
            # Plant-based milk (good health scores)
            "Soy milk": 0.75,
            "Oat milk": 0.7,
            "Almond milk": 0.7,
            "Rice milk": 0.65,
            "Plant Milk": 0.7,
            
            # Grains (moderate to good)
            "Wheat & Rye": 0.7,
            "Bread": 0.65,
            "Rice": 0.6,
            "Oatmeal": 0.85,
            "Barley": 0.75,
            "Maize": 0.65,
            "Grains": 0.7,
            
            # Vegetables (excellent health scores)
            "Tomatoes": 0.95,
            "Onions & Leeks": 0.9,
            "Root Vegetables": 0.85,
            "Brassicas": 0.95,
            "Vegetables": 0.9,
            "Other Vegetables": 0.9,
            
            # Fruits (excellent health scores)
            "Apples": 0.95,
            "Bananas": 0.9,
            "Berries & Grapes": 0.95,
            "Citrus Fruit": 0.95,
            "Fruit": 0.9,
            "Other Fruit": 0.9,
            
            # Oils & Fats (moderate)
            "Olive Oil": 0.75,
            "Palm Oil": 0.4,
            "Sunflower Oil": 0.6,
            "Rapeseed Oil": 0.65,
            
            # Sweeteners (low)
            "Sugar": 0.2,
            "Sugar (cane)": 0.2,
            "Sugar (beet)": 0.2,
            
            # Beverages (variable)
            "Coffee": 0.6,
            "Dark Chocolate": 0.55,
            "Wine": 0.4,
        }
    
    def get_health_score(self, product_id: str, category: Optional[str] = None) -> float:
        """
        Get health score for a product
        
        Args:
            product_id: Product identifier
            category: Product category (optional)
            
        Returns:
            Health score between 0 (unhealthy) and 1 (very healthy)
        """
        # Try direct lookup
        if product_id in self.health_db:
            return self.health_db[product_id]
        
        # Try category lookup
        if category and category in self.health_db:
            return self.health_db[category]
        
        # Try partial matching
        for key, score in self.health_db.items():
            if key.lower() in product_id.lower():
                return score
        
        # Default: moderate health score
        return 0.5
    
    def get_basket_health_score(self, basket: list) -> float:
        """
        Calculate aggregate health score for a basket
        
        Args:
            basket: List of products with quantities
            
        Returns:
            Weighted average health score
        """
        if not basket:
            return 0.5
        
        total_weight = 0.0
        weighted_health = 0.0
        
        for item in basket:
            quantity = item.get("quantity", 1.0)
            product_id = item.get("product_id", "")
            category = item.get("category", "")
            
            health_score = self.get_health_score(product_id, category)
            
            weighted_health += health_score * quantity
            total_weight += quantity
        
        return weighted_health / total_weight if total_weight > 0 else 0.5
    
    def compute_nutri_score(self, nutrients: Dict) -> float:
        """
        Compute Nutri-Score-like health score from nutritional data
        
        Args:
            nutrients: Dict with keys like 'energy', 'saturated_fat', 'sugars', 
                      'sodium', 'fiber', 'protein', 'fruits_vegetables'
                      
        Returns:
            Health score 0-1
        """
        # Simplified Nutri-Score algorithm
        # Negative points (bad nutrients)
        negative = 0
        negative += min(nutrients.get('energy', 0) / 3350, 10)  # Max 10 points
        negative += min(nutrients.get('saturated_fat', 0) / 10, 10)
        negative += min(nutrients.get('sugars', 0) / 45, 10)
        negative += min(nutrients.get('sodium', 0) / 900, 10)
        
        # Positive points (good nutrients)
        positive = 0
        positive += min(nutrients.get('fiber', 0) / 4.7, 5)
        positive += min(nutrients.get('protein', 0) / 8, 5)
        positive += min(nutrients.get('fruits_vegetables', 0) / 80, 5)
        
        # Final score
        score = positive - negative
        
        # Normalize to 0-1 (Nutri-Score ranges from -15 to 15)
        normalized = (score + 15) / 30
        
        return np.clip(normalized, 0, 1)

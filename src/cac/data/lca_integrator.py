"""LCA Data Integration and Product Mapping"""

import pandas as pd
from typing import Dict, Optional
import re


class LCAIntegrator:
    """Integrate multiple LCA data sources and map to products"""
    
    def __init__(self):
        self.category_mapping = {}
        self.footprint_db = {}
    
    def build_category_mapping(
        self,
        products: pd.DataFrame,
        lca_data: pd.DataFrame
    ) -> Dict[str, str]:
        """
        Map product names to canonical LCA categories
        
        Args:
            products: Product catalog
            lca_data: LCA database with categories
            
        Returns:
            Dict mapping product_id to LCA category
        """
        mapping = {}
        
        for _, product in products.iterrows():
            product_id = str(product["product_id"])
            product_name = product["product_name"].lower()
            
            # Rule-based category assignment
            category = self._classify_product(product_name)
            mapping[product_id] = category
        
        self.category_mapping = mapping
        return mapping
    
    def _classify_product(self, product_name: str) -> str:
        """Classify product into LCA category using rules"""
        product_name = product_name.lower()
        
        # Meat & Protein
        if any(word in product_name for word in ["beef", "steak", "ground beef"]):
            return "Beef"
        elif any(word in product_name for word in ["chicken", "poultry"]):
            return "Chicken"
        elif any(word in product_name for word in ["pork", "bacon", "ham"]):
            return "Pork"
        elif any(word in product_name for word in ["fish", "salmon", "tuna"]):
            return "Fish"
        elif any(word in product_name for word in ["tofu", "tempeh"]):
            return "Tofu"
        
        # Dairy & Alternatives
        elif any(word in product_name for word in ["milk", "dairy"]) and "oat" not in product_name:
            return "Milk"
        elif "oat" in product_name and "milk" in product_name:
            return "Oat Milk"
        elif any(word in product_name for word in ["cheese", "cheddar"]):
            return "Cheese"
        
        # Produce
        elif any(word in product_name for word in ["tomato", "lettuce", "carrot", "vegetable"]):
            return "Vegetables"
        elif any(word in product_name for word in ["apple", "banana", "orange", "fruit"]):
            return "Fruit"
        
        # Grains
        elif any(word in product_name for word in ["bread", "wheat", "rice", "pasta"]):
            return "Grains"
        
        else:
            return "Other"
    
    def merge_footprints(
        self,
        products: pd.DataFrame,
        poore_nemecek: pd.DataFrame,
        open_food_facts: Optional[pd.DataFrame] = None
    ) -> Dict[str, Dict]:
        """
        Merge footprint data from multiple sources
        
        Returns:
            Dict mapping product_id to footprint data
        """
        footprint_db = {}
        
        # Build category mapping
        self.build_category_mapping(products, poore_nemecek)
        
        # Create category -> footprint lookup
        category_footprints = {}
        for _, row in poore_nemecek.iterrows():
            category_footprints[row["category"]] = {
                "emissions_mean": row["emissions_mean"],
                "emissions_variance": row["emissions_std"] ** 2,
                "source": "Poore & Nemecek 2018",
            }
        
        # Map products to footprints
        for product_id, category in self.category_mapping.items():
            if category in category_footprints:
                footprint_db[product_id] = {
                    **category_footprints[category],
                    "category": category,
                }
            else:
                # Default fallback
                footprint_db[product_id] = {
                    "emissions_mean": 2.0,
                    "emissions_variance": 1.0,
                    "category": "Other",
                    "source": "Default",
                }
        
        self.footprint_db = footprint_db
        return footprint_db
    
    def normalize_units(self, quantity: float, unit: str) -> float:
        """Convert various units to kg"""
        unit = unit.lower()
        
        if unit in ["kg", "kilogram"]:
            return quantity
        elif unit in ["g", "gram"]:
            return quantity / 1000.0
        elif unit in ["lb", "pound"]:
            return quantity * 0.453592
        elif unit in ["oz", "ounce"]:
            return quantity * 0.0283495
        elif unit in ["l", "liter"]:
            return quantity  # Assume density ~1 kg/L
        elif unit in ["ml", "milliliter"]:
            return quantity / 1000.0
        else:
            return quantity  # Assume kg

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
        open_food_facts: Optional[pd.DataFrame] = None,
        su_eatable_life: Optional[pd.DataFrame] = None
    ) -> Dict[str, Dict]:
        """
        Merge footprint data from multiple sources with priority order
        
        Priority: Open Food Facts > Poore & Nemecek > SU-EATABLE LIFE > Default
        
        Returns:
            Dict mapping product_id to footprint data
        """
        from .product_mapper import ProductMapper
        
        footprint_db = {}
        
        # Initialize product mapper with LLM support
        mapper = ProductMapper(use_llm=True)
        
        # Build category mapping using enhanced mapper
        self.category_mapping = {}
        for _, product in products.iterrows():
            product_id = str(product["product_id"])
            product_name = product["product_name"]
            
            category = mapper.map_product_to_category(product_name, product_id)
            self.category_mapping[product_id] = category
        
        print(f"✅ Mapped {len(self.category_mapping)} products to categories")
        
        # Create category -> footprint lookup from Poore & Nemecek
        category_footprints = {}
        for _, row in poore_nemecek.iterrows():
            category_footprints[row["category"]] = {
                "emissions_mean": row["emissions_mean"],
                "emissions_variance": row["emissions_std"] ** 2,
                "source": "Poore & Nemecek 2018",
            }
        
        # Create SU-EATABLE LIFE lookup if available
        suel_footprints = {}
        if su_eatable_life is not None:
            for _, row in su_eatable_life.iterrows():
                suel_footprints[row["food_item"]] = {
                    "emissions_mean": row["carbon_footprint_kg"],
                    "emissions_variance": (row["carbon_footprint_kg"] * 0.3) ** 2,  # Assume 30% uncertainty
                    "source": "SU-EATABLE LIFE",
                }
        
        # Map products to footprints with priority
        for product_id, category in self.category_mapping.items():
            product_name = products[products["product_id"] == int(product_id)]["product_name"].iloc[0] if len(products[products["product_id"] == int(product_id)]) > 0 else ""
            
            footprint = None
            
            # Priority 1: Open Food Facts (product-specific)
            if open_food_facts is not None:
                off_match = open_food_facts[open_food_facts["product_name"].str.contains(product_name, case=False, na=False)]
                if len(off_match) > 0:
                    off_row = off_match.iloc[0]
                    footprint = {
                        "emissions_mean": off_row.get("carbon_footprint_100g", 2.0) * 10,  # Convert to per kg
                        "emissions_variance": (off_row.get("carbon_footprint_100g", 2.0) * 10 * 0.2) ** 2,
                        "source": "Open Food Facts",
                        "ecoscore": off_row.get("ecoscore_score", 50),
                    }
            
            # Priority 2: Poore & Nemecek (category-based)
            if footprint is None and category in category_footprints:
                footprint = category_footprints[category]
            
            # Priority 3: SU-EATABLE LIFE (fuzzy match)
            if footprint is None and suel_footprints:
                for suel_item, suel_data in suel_footprints.items():
                    if any(word in product_name.lower() for word in suel_item.lower().split()):
                        footprint = suel_data
                        break
            
            # Priority 4: Default fallback
            if footprint is None:
                footprint = {
                    "emissions_mean": 2.0,
                    "emissions_variance": 1.0,
                    "source": "Default",
                }
            
            # Add category info
            footprint["category"] = category
            footprint_db[product_id] = footprint
        
        # Print source statistics
        sources = {}
        for fp in footprint_db.values():
            source = fp["source"]
            sources[source] = sources.get(source, 0) + 1
        
        print(f"✅ Footprint sources:")
        for source, count in sources.items():
            print(f"   {source}: {count} products")
        
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

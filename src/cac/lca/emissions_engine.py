"""Life-Cycle Assessment Emissions Engine"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ProductFootprint:
    """Product-level carbon footprint with uncertainty"""
    product_id: str
    emissions_mean: float  # kg CO2e per kg
    emissions_variance: float
    category: str
    source: str


class EmissionsEngine:
    """Compute basket-level emissions from LCA data"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.footprint_db = {}  # Will be loaded from LCA databases
        self.load_lca_databases()  # Auto-load on initialization
        
    def load_lca_databases(self):
        """Load and integrate LCA databases (Poore & Nemecek, Open Food Facts, etc.)"""
        from ..data.data_loader import DataLoader
        from ..data.lca_integrator import LCAIntegrator
        
        # Load LCA data
        loader = DataLoader()
        poore_nemecek = loader.load_poore_nemecek_data()
        
        # Create footprint database
        integrator = LCAIntegrator()
        
        # For now, create direct category mapping
        for _, row in poore_nemecek.iterrows():
            category = row["category"]
            self.footprint_db[category] = ProductFootprint(
                product_id=category,
                emissions_mean=row["emissions_mean"],
                emissions_variance=row["emissions_std"] ** 2,
                category=category,
                source="Poore & Nemecek 2018"
            )
        
        print(f"✅ Loaded {len(self.footprint_db)} LCA categories")
    
    def get_product_footprint(self, product_id: str) -> Optional[ProductFootprint]:
        """Retrieve product footprint from database"""
        # Try direct lookup
        if product_id in self.footprint_db:
            return self.footprint_db[product_id]
        
        # Try category-based lookup
        # Extract category from product_id or use mapping
        for category in self.footprint_db:
            if category.lower() in product_id.lower():
                return self.footprint_db[category]
        
        # Fallback: return default
        return ProductFootprint(
            product_id=product_id,
            emissions_mean=5.0,  # Default moderate emissions
            emissions_variance=2.0,
            category="Unknown",
            source="Default"
        )
    
    def calculate_basket_emissions(
        self,
        basket: List[Dict]
    ) -> Dict:
        """
        Calculate total basket emissions with uncertainty
        
        Args:
            basket: List of {product_id, quantity, ...}
            
        Returns:
            Dict with emissions, variance, and RACS
        """
        total_emissions = 0.0
        total_variance = 0.0
        product_emissions = []
        
        for item in basket:
            product_id = item["product_id"]
            quantity = item["quantity"]
            
            footprint = self.get_product_footprint(product_id)
            if footprint:
                emissions = footprint.emissions_mean * quantity
                variance = footprint.emissions_variance * (quantity ** 2)
                
                total_emissions += emissions
                total_variance += variance
                
                product_emissions.append({
                    "product_id": product_id,
                    "emissions": emissions,
                    "variance": variance,
                })
        
        # Compute RACS at 95% confidence
        z_alpha = 1.96
        racs = total_emissions + z_alpha * np.sqrt(total_variance)
        
        return {
            "emissions": total_emissions,
            "variance": total_variance,
            "racs": racs,
            "product_emissions": product_emissions,
        }
    
    def normalize_emissions(
        self,
        emissions: float,
        reference_min: float = 0.0,
        reference_max: float = 100.0
    ) -> float:
        """Normalize emissions to [0, 1] range"""
        if reference_max <= reference_min:
            return 0.0
        return (emissions - reference_min) / (reference_max - reference_min)

"""Data Loading and Preprocessing for Instacart and LCA Datasets"""

import pandas as pd
from typing import Dict, List, Optional
from pathlib import Path


class DataLoader:
    """Load and preprocess Instacart and LCA datasets"""
    
    def __init__(self, data_dir: str = "data/raw"):
        self.data_dir = Path(data_dir)
        self.products = None
        self.orders = None
        self.order_products = None
    
    def load_instacart_dataset(self) -> Dict[str, pd.DataFrame]:
        """
        Load Instacart Online Grocery Shopping Dataset
        
        Returns:
            Dict with products, orders, order_products DataFrames
        """
        self.products = pd.read_csv(self.data_dir / "products.csv")
        self.orders = pd.read_csv(self.data_dir / "orders.csv")
        self.order_products = pd.read_csv(self.data_dir / "order_products__train.csv")
        
        return {
            "products": self.products,
            "orders": self.orders,
            "order_products": self.order_products,
        }
    
    def load_poore_nemecek_data(self) -> pd.DataFrame:
        """
        Load Poore & Nemecek (2018) LCA meta-analysis data
        
        Returns:
            DataFrame with product categories and emissions factors
        """
        # TODO: Load from actual data source
        return pd.DataFrame({
            "category": ["Beef", "Chicken", "Tofu", "Milk", "Oat Milk"],
            "emissions_mean": [60.0, 6.9, 2.0, 3.2, 0.9],
            "emissions_std": [15.0, 2.0, 0.5, 0.8, 0.2],
        })
    
    def load_open_food_facts(self) -> pd.DataFrame:
        """
        Load Open Food Facts database with Eco-Score
        
        Returns:
            DataFrame with product-level attributes
        """
        # TODO: Load from actual data source
        return pd.DataFrame()
    
    def load_su_eatable_life(self) -> pd.DataFrame:
        """
        Load SU-EATABLE LIFE database
        
        Returns:
            DataFrame with commodity-level footprints
        """
        # TODO: Load from actual data source
        return pd.DataFrame()
    
    def sample_baskets(self, n_baskets: int = 500000) -> List[Dict]:
        """
        Sample baskets from Instacart dataset
        
        Args:
            n_baskets: Number of baskets to sample
            
        Returns:
            List of basket dictionaries
        """
        if self.orders is None or self.order_products is None:
            self.load_instacart_dataset()
        
        # Sample orders
        sampled_orders = self.orders.sample(n=min(n_baskets, len(self.orders)))
        
        baskets = []
        for _, order in sampled_orders.iterrows():
            order_id = order["order_id"]
            
            # Get products in this order
            order_items = self.order_products[
                self.order_products["order_id"] == order_id
            ]
            
            basket = []
            for _, item in order_items.iterrows():
                product_id = item["product_id"]
                product_info = self.products[
                    self.products["product_id"] == product_id
                ].iloc[0] if len(self.products[self.products["product_id"] == product_id]) > 0 else None
                
                if product_info is not None:
                    basket.append({
                        "basket_id": str(order_id),
                        "product_id": str(product_id),
                        "name": product_info["product_name"],
                        "quantity": 1.0,  # Instacart doesn't have quantity
                        "price": 5.0,  # Placeholder
                    })
            
            if basket:
                baskets.append(basket)
        
        return baskets

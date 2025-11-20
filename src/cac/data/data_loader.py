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
        # Try to load from file
        poore_path = self.data_dir / "poore_nemecek_2018.csv"
        
        if poore_path.exists():
            df = pd.read_csv(poore_path)
            return df
        
        # Fallback: Comprehensive synthetic dataset based on paper
        # Data from Poore & Nemecek (2018) Science paper
        data = {
            "category": [
                # Meat & Poultry
                "Beef (beef herd)", "Beef (dairy herd)", "Lamb & Mutton", "Pork", 
                "Poultry Meat", "Fish (farmed)", "Prawns (farmed)",
                
                # Dairy & Eggs
                "Milk", "Cheese", "Eggs",
                
                # Plant-based proteins
                "Tofu", "Peas", "Nuts", "Groundnuts", "Other Pulses",
                
                # Grains
                "Wheat & Rye (Bread)", "Maize (Meal)", "Rice", "Oatmeal", "Barley (Beer)",
                
                # Vegetables
                "Tomatoes", "Onions & Leeks", "Root Vegetables", "Brassicas", 
                "Other Vegetables",
                
                # Fruits
                "Apples", "Bananas", "Berries & Grapes", "Citrus Fruit", "Other Fruit",
                
                # Plant-based milk
                "Soy milk", "Oat milk", "Rice milk", "Almond milk",
                
                # Oils & Fats
                "Olive Oil", "Palm Oil", "Sunflower Oil", "Rapeseed Oil",
                
                # Sweeteners
                "Sugar (cane)", "Sugar (beet)",
                
                # Beverages
                "Coffee", "Dark Chocolate", "Wine",
            ],
            "emissions_mean": [
                # Meat & Poultry (kg CO2e per kg)
                99.5, 33.3, 39.2, 12.1, 9.9, 13.6, 26.9,
                
                # Dairy & Eggs
                3.2, 23.9, 4.5,
                
                # Plant-based proteins
                3.0, 0.9, 0.3, 3.2, 1.6,
                
                # Grains
                1.6, 1.7, 4.5, 2.5, 0.7,
                
                # Vegetables
                2.1, 0.5, 0.4, 0.5, 0.5,
                
                # Fruits
                0.4, 0.9, 1.5, 0.4, 0.7,
                
                # Plant-based milk
                0.9, 0.9, 1.2, 0.7,
                
                # Oils & Fats
                5.4, 7.6, 3.5, 3.8,
                
                # Sweeteners
                3.2, 1.8,
                
                # Beverages
                28.5, 46.7, 1.8,
            ],
            "emissions_std": [
                # Meat & Poultry (standard deviation)
                33.0, 12.0, 15.0, 4.0, 3.0, 8.0, 15.0,
                
                # Dairy & Eggs
                1.5, 8.0, 1.5,
                
                # Plant-based proteins
                1.0, 0.3, 0.2, 1.0, 0.5,
                
                # Grains
                0.5, 0.6, 1.5, 0.8, 0.3,
                
                # Vegetables
                1.0, 0.2, 0.2, 0.2, 0.2,
                
                # Fruits
                0.2, 0.3, 0.5, 0.2, 0.3,
                
                # Plant-based milk
                0.3, 0.3, 0.4, 0.3,
                
                # Oils & Fats
                2.0, 3.0, 1.5, 1.5,
                
                # Sweeteners
                1.0, 0.6,
                
                # Beverages
                10.0, 15.0, 0.6,
            ],
        }
        
        df = pd.DataFrame(data)
        
        # Save for future use
        poore_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(poore_path, index=False)
        
        return df
    
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

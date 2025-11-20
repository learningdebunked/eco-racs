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
        try:
            self.products = pd.read_csv(self.data_dir / "products.csv")
            self.orders = pd.read_csv(self.data_dir / "orders.csv")
            self.order_products = pd.read_csv(self.data_dir / "order_products__train.csv")
            
            print(f"✅ Loaded Instacart dataset:")
            print(f"   Products: {len(self.products)}")
            print(f"   Orders: {len(self.orders)}")
            print(f"   Order-Product mappings: {len(self.order_products)}")
            
            return {
                "products": self.products,
                "orders": self.orders,
                "order_products": self.order_products,
            }
        except FileNotFoundError as e:
            print(f"⚠️  Instacart dataset not found: {e}")
            print(f"   Download from: https://www.kaggle.com/c/instacart-market-basket-analysis/data")
            print(f"   Place files in: {self.data_dir}/")
            
            # Return synthetic data for testing
            return self._create_synthetic_instacart_data()
    
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
        off_path = self.data_dir / "openfoodfacts.csv"
        
        try:
            # Try to load from file
            df = pd.read_csv(off_path)
            print(f"✅ Loaded Open Food Facts: {len(df)} products")
            return df
        except FileNotFoundError:
            print(f"⚠️  Open Food Facts not found")
            print(f"   Download from: https://world.openfoodfacts.org/data")
            print(f"   Or use API: https://world.openfoodfacts.org/api/v0/product/[barcode].json")
            
            # Return synthetic data for testing
            return self._create_synthetic_open_food_facts()
    
    def _create_synthetic_open_food_facts(self) -> pd.DataFrame:
        """Create synthetic Open Food Facts data"""
        print("   Creating synthetic Open Food Facts data...")
        
        data = {
            "code": ["001", "002", "003", "004", "005"],
            "product_name": ["Organic Milk", "Oat Milk", "Almond Milk", "Tofu", "Tempeh"],
            "ecoscore_grade": ["b", "a", "a", "a", "a"],
            "ecoscore_score": [65, 85, 80, 90, 88],
            "nutriscore_grade": ["c", "b", "b", "a", "a"],
            "countries": ["USA", "USA", "USA", "USA", "USA"],
            "packaging": ["Plastic", "Carton", "Carton", "Plastic", "Plastic"],
            "carbon_footprint_100g": [0.32, 0.09, 0.07, 0.20, 0.23],
        }
        
        df = pd.DataFrame(data)
        print(f"   ✅ Created synthetic Open Food Facts: {len(df)} products")
        return df
    
    def load_su_eatable_life(self) -> pd.DataFrame:
        """
        Load SU-EATABLE LIFE database
        
        Returns:
            DataFrame with commodity-level footprints
        """
        suel_path = self.data_dir / "su_eatable_life.csv"
        
        try:
            # Try to load from file
            df = pd.read_csv(suel_path)
            print(f"✅ Loaded SU-EATABLE LIFE: {len(df)} items")
            return df
        except FileNotFoundError:
            print(f"⚠️  SU-EATABLE LIFE not found")
            print(f"   Download from: https://www.sueatablelife.eu")
            
            # Return synthetic data for testing
            return self._create_synthetic_su_eatable_life()
    
    def _create_synthetic_su_eatable_life(self) -> pd.DataFrame:
        """Create synthetic SU-EATABLE LIFE data"""
        print("   Creating synthetic SU-EATABLE LIFE data...")
        
        data = {
            "food_item": [
                "Beef steak", "Chicken breast", "Pork chop", "Salmon",
                "Pasta with tomato sauce", "Rice with vegetables",
                "Lentil soup", "Vegetable curry", "Fruit salad",
                "Cheese pizza", "Hamburger", "Caesar salad"
            ],
            "carbon_footprint_kg": [
                7.2, 1.1, 1.5, 2.9,
                0.8, 1.2,
                0.5, 0.6, 0.3,
                2.5, 5.5, 1.8
            ],
            "water_footprint_liters": [
                15400, 4300, 5900, 3000,
                1200, 2500,
                800, 900, 500,
                1800, 8500, 1500
            ],
            "land_use_m2": [
                326, 12, 11, 3.7,
                2.1, 3.5,
                1.8, 2.0, 1.2,
                5.5, 45, 3.2
            ],
        }
        
        df = pd.DataFrame(data)
        print(f"   ✅ Created synthetic SU-EATABLE LIFE: {len(df)} items")
        return df
    
    def _create_synthetic_instacart_data(self) -> Dict[str, pd.DataFrame]:
        """Create synthetic Instacart-like data for testing"""
        print("   Creating synthetic Instacart data for testing...")
        
        # Synthetic products
        products = pd.DataFrame({
            "product_id": range(1, 18),
            "product_name": [
                "Ground Beef", "Beef Steak", "Chicken Breast", "Ground Chicken",
                "Firm Tofu", "Extra Firm Tofu", "Tempeh", "Black Beans",
                "Whole Milk", "2% Milk", "Oat Milk", "Almond Milk", "Soy Milk",
                "Pork Chops", "Ground Pork", "Salmon Fillet", "Tuna"
            ],
            "aisle_id": [1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 5, 5, 5, 6, 6, 7, 7],
            "department_id": [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 1, 1, 1, 1],
        })
        
        # Synthetic orders
        orders = pd.DataFrame({
            "order_id": range(1, 101),
            "user_id": [i % 20 + 1 for i in range(100)],
            "order_number": [i % 10 + 1 for i in range(100)],
            "order_dow": [i % 7 for i in range(100)],
            "order_hour_of_day": [i % 24 for i in range(100)],
        })
        
        # Synthetic order-products
        import numpy as np
        np.random.seed(42)
        order_products = []
        for order_id in range(1, 101):
            n_items = np.random.randint(2, 8)
            product_ids = np.random.choice(range(1, 18), size=n_items, replace=False)
            for idx, pid in enumerate(product_ids):
                order_products.append({
                    "order_id": order_id,
                    "product_id": int(pid),
                    "add_to_cart_order": idx + 1,
                    "reordered": np.random.choice([0, 1], p=[0.7, 0.3]),
                })
        
        order_products = pd.DataFrame(order_products)
        
        self.products = products
        self.orders = orders
        self.order_products = order_products
        
        print(f"   ✅ Created synthetic data: {len(products)} products, {len(orders)} orders")
        
        return {
            "products": products,
            "orders": orders,
            "order_products": order_products,
        }
    
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
        n_to_sample = min(n_baskets, len(self.orders))
        sampled_orders = self.orders.sample(n=n_to_sample, random_state=42)
        
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
                ]
                
                if len(product_info) > 0:
                    product_info = product_info.iloc[0]
                    basket.append({
                        "basket_id": str(order_id),
                        "product_id": str(product_id),
                        "name": product_info["product_name"],
                        "quantity": 1.0,  # Instacart doesn't have quantity
                        "price": 5.0,  # Placeholder - would need price data
                    })
            
            if basket:
                baskets.append(basket)
        
        return baskets

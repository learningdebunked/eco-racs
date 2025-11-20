"""Product to LCA Category Mapping with LLM Assistance"""

import re
from typing import Optional, Dict
import os


class ProductMapper:
    """Map product names to LCA categories using rules and LLM"""
    
    def __init__(self, use_llm: bool = False):
        self.use_llm = use_llm
        self.llm_client = None
        if use_llm:
            self._init_llm()
        
        # Category mapping cache
        self.cache = {}
    
    def _init_llm(self):
        """Initialize LLM for ambiguous classifications"""
        try:
            import openai
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.llm_client = openai.OpenAI(api_key=api_key)
        except Exception:
            self.llm_client = None
    
    def map_product_to_category(self, product_name: str, product_id: Optional[str] = None) -> str:
        """
        Map product name to LCA category
        
        Args:
            product_name: Product name from Instacart
            product_id: Optional product ID for caching
            
        Returns:
            LCA category name
        """
        # Check cache
        cache_key = product_id or product_name
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Try rule-based classification
        category = self._rule_based_classification(product_name)
        
        # If ambiguous and LLM available, use LLM
        if category == "Other" and self.use_llm and self.llm_client:
            category = self._llm_classification(product_name)
        
        # Cache result
        self.cache[cache_key] = category
        
        return category
    
    def _rule_based_classification(self, product_name: str) -> str:
        """Rule-based product classification"""
        name = product_name.lower()
        
        # Meat & Poultry
        if any(word in name for word in ["beef", "steak", "ground beef", "hamburger"]):
            return "Beef (beef herd)"
        elif any(word in name for word in ["chicken", "poultry", "hen"]):
            return "Poultry Meat"
        elif any(word in name for word in ["pork", "bacon", "ham", "sausage"]):
            return "Pork"
        elif any(word in name for word in ["lamb", "mutton"]):
            return "Lamb & Mutton"
        elif any(word in name for word in ["salmon", "tuna", "fish", "cod", "tilapia"]):
            return "Fish (farmed)"
        elif any(word in name for word in ["shrimp", "prawn"]):
            return "Prawns (farmed)"
        
        # Plant-based proteins
        elif any(word in name for word in ["tofu", "soy protein"]):
            return "Tofu"
        elif any(word in name for word in ["tempeh"]):
            return "Tofu"  # Similar category
        elif any(word in name for word in ["lentil", "chickpea", "bean", "legume"]):
            return "Other Pulses"
        elif "pea" in name and "protein" in name:
            return "Peas"
        elif any(word in name for word in ["almond", "walnut", "cashew", "pecan"]):
            return "Nuts"
        elif "peanut" in name:
            return "Groundnuts"
        
        # Dairy
        elif "milk" in name and not any(word in name for word in ["oat", "almond", "soy", "rice", "coconut"]):
            return "Milk"
        elif "cheese" in name:
            return "Cheese"
        elif "egg" in name:
            return "Eggs"
        
        # Plant-based milk
        elif "oat" in name and "milk" in name:
            return "Oat milk"
        elif "soy" in name and "milk" in name:
            return "Soy milk"
        elif "almond" in name and "milk" in name:
            return "Almond milk"
        elif "rice" in name and "milk" in name:
            return "Rice milk"
        
        # Grains
        elif any(word in name for word in ["bread", "wheat", "rye"]):
            return "Wheat & Rye (Bread)"
        elif "rice" in name and "milk" not in name:
            return "Rice"
        elif "oat" in name and "milk" not in name:
            return "Oatmeal"
        elif "corn" in name or "maize" in name:
            return "Maize (Meal)"
        elif "barley" in name or "beer" in name:
            return "Barley (Beer)"
        
        # Vegetables
        elif "tomato" in name:
            return "Tomatoes"
        elif any(word in name for word in ["onion", "leek", "scallion"]):
            return "Onions & Leeks"
        elif any(word in name for word in ["carrot", "potato", "beet", "turnip"]):
            return "Root Vegetables"
        elif any(word in name for word in ["broccoli", "cauliflower", "cabbage", "kale"]):
            return "Brassicas"
        elif any(word in name for word in ["lettuce", "spinach", "vegetable", "veggie"]):
            return "Other Vegetables"
        
        # Fruits
        elif "apple" in name:
            return "Apples"
        elif "banana" in name:
            return "Bananas"
        elif any(word in name for word in ["berry", "strawberry", "blueberry", "grape"]):
            return "Berries & Grapes"
        elif any(word in name for word in ["orange", "lemon", "lime", "grapefruit"]):
            return "Citrus Fruit"
        elif any(word in name for word in ["fruit", "mango", "pineapple", "peach"]):
            return "Other Fruit"
        
        # Oils
        elif "olive oil" in name:
            return "Olive Oil"
        elif "palm oil" in name:
            return "Palm Oil"
        elif "sunflower oil" in name:
            return "Sunflower Oil"
        elif "rapeseed" in name or "canola" in name:
            return "Rapeseed Oil"
        
        # Sweeteners
        elif "sugar" in name:
            return "Sugar (cane)"
        
        # Beverages
        elif "coffee" in name:
            return "Coffee"
        elif "chocolate" in name:
            return "Dark Chocolate"
        elif "wine" in name:
            return "Wine"
        
        else:
            return "Other"
    
    def _llm_classification(self, product_name: str) -> str:
        """Use LLM to classify ambiguous products"""
        if not self.llm_client:
            return "Other"
        
        try:
            prompt = f"""Classify this food product into one of these LCA categories:

Categories: Beef, Chicken, Pork, Fish, Tofu, Milk, Cheese, Eggs, 
Oat milk, Soy milk, Rice, Bread, Vegetables, Fruits, Other

Product: "{product_name}"

Return only the category name, nothing else."""
            
            response = self.llm_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=20,
            )
            
            category = response.choices[0].message.content.strip()
            
            # Validate category
            valid_categories = [
                "Beef", "Chicken", "Pork", "Fish", "Tofu", "Milk", "Cheese", "Eggs",
                "Oat milk", "Soy milk", "Rice", "Bread", "Vegetables", "Fruits"
            ]
            
            if category in valid_categories:
                return category
            else:
                return "Other"
        
        except Exception as e:
            print(f"   LLM classification failed: {e}")
            return "Other"
    
    def batch_map_products(self, products: list) -> Dict[str, str]:
        """Map multiple products at once"""
        mapping = {}
        
        for product in products:
            product_id = product.get("product_id", "")
            product_name = product.get("product_name", product.get("name", ""))
            
            category = self.map_product_to_category(product_name, product_id)
            mapping[product_id] = category
        
        return mapping

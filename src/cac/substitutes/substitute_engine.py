"""Product Substitute Search Engine"""

import numpy as np
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
import pickle
from pathlib import Path


@dataclass
class ProductSimilarity:
    """Product similarity information"""
    product_id: str
    name: str
    category: str
    emissions: float
    price: float
    similarity_score: float
    health_score: float
    attributes: Dict


class SubstituteEngine:
    """Find suitable product substitutes for low-carbon swaps"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.product_db = {}
        self.category_index = {}
        self.embeddings = {}
        self._load_product_database()
    
    def _load_product_database(self):
        """Load product database with categories and attributes"""
        # Try to load from file
        db_path = self.config.get("product_db_path", "data/processed/product_db.pkl")
        
        if Path(db_path).exists():
            with open(db_path, 'rb') as f:
                data = pickle.load(f)
                self.product_db = data.get('products', {})
                self.category_index = data.get('category_index', {})
                self.embeddings = data.get('embeddings', {})
            return
        
        # Fallback: Create synthetic database
        self._create_synthetic_database()
    
    def _create_synthetic_database(self):
        """Create synthetic product database for testing"""
        from ..health.health_scorer import HealthScorer
        
        health_scorer = HealthScorer()
        
        products = [
            # Beef products
            {"id": "beef_001", "name": "Ground Beef", "category": "Beef", "emissions": 60.0, "price": 8.99, "vegetarian": False, "allergens": []},
            {"id": "beef_002", "name": "Beef Steak", "category": "Beef", "emissions": 65.0, "price": 12.99, "vegetarian": False, "allergens": []},
            
            # Chicken products
            {"id": "chicken_001", "name": "Chicken Breast", "category": "Chicken", "emissions": 6.9, "price": 6.99, "vegetarian": False, "allergens": []},
            {"id": "chicken_002", "name": "Ground Chicken", "category": "Chicken", "emissions": 7.2, "price": 5.99, "vegetarian": False, "allergens": []},
            
            # Plant-based proteins
            {"id": "tofu_001", "name": "Firm Tofu", "category": "Tofu", "emissions": 2.0, "price": 3.99, "vegetarian": True, "allergens": ["soy"]},
            {"id": "tofu_002", "name": "Extra Firm Tofu", "category": "Tofu", "emissions": 2.1, "price": 4.49, "vegetarian": True, "allergens": ["soy"]},
            {"id": "tempeh_001", "name": "Tempeh", "category": "Tempeh", "emissions": 2.3, "price": 4.99, "vegetarian": True, "allergens": ["soy"]},
            {"id": "beans_001", "name": "Black Beans", "category": "Legumes", "emissions": 0.9, "price": 1.99, "vegetarian": True, "allergens": []},
            
            # Dairy
            {"id": "milk_001", "name": "Whole Milk", "category": "Milk", "emissions": 3.2, "price": 4.99, "vegetarian": True, "allergens": ["dairy"]},
            {"id": "milk_002", "name": "2% Milk", "category": "Milk", "emissions": 3.0, "price": 4.79, "vegetarian": True, "allergens": ["dairy"]},
            
            # Plant-based milk
            {"id": "oat_milk_001", "name": "Oat Milk", "category": "Plant Milk", "emissions": 0.9, "price": 4.49, "vegetarian": True, "allergens": []},
            {"id": "almond_milk_001", "name": "Almond Milk", "category": "Plant Milk", "emissions": 0.7, "price": 4.99, "vegetarian": True, "allergens": ["nuts"]},
            {"id": "soy_milk_001", "name": "Soy Milk", "category": "Plant Milk", "emissions": 0.8, "price": 3.99, "vegetarian": True, "allergens": ["soy"]},
            
            # Pork
            {"id": "pork_001", "name": "Pork Chops", "category": "Pork", "emissions": 12.1, "price": 7.99, "vegetarian": False, "allergens": []},
            {"id": "pork_002", "name": "Ground Pork", "category": "Pork", "emissions": 11.8, "price": 6.99, "vegetarian": False, "allergens": []},
            
            # Fish
            {"id": "fish_001", "name": "Salmon Fillet", "category": "Fish", "emissions": 11.9, "price": 14.99, "vegetarian": False, "allergens": ["fish"]},
            {"id": "fish_002", "name": "Tuna", "category": "Fish", "emissions": 6.1, "price": 9.99, "vegetarian": False, "allergens": ["fish"]},
        ]
        
        # Build product database and add health scores
        for p in products:
            # Add health score from health scorer
            p["health"] = health_scorer.get_health_score(p["id"], p["category"])
            self.product_db[p["id"]] = p
        
        # Build category index
        for p in products:
            category = p["category"]
            if category not in self.category_index:
                self.category_index[category] = []
            self.category_index[category].append(p["id"])
        
        # Create simple embeddings (for similarity)
        for p in products:
            # Simple embedding based on category and attributes
            self.embeddings[p["id"]] = self._create_embedding(p)
    
    def _create_embedding(self, product: Dict) -> np.ndarray:
        """Create simple embedding for product"""
        # Simple feature vector
        features = [
            product["emissions"] / 100.0,  # Normalized emissions
            product["price"] / 20.0,  # Normalized price
            product["health"],
            1.0 if product["vegetarian"] else 0.0,
            len(product["allergens"]) / 5.0,
        ]
        return np.array(features)
    
    def find_substitutes(
        self,
        product_id: str,
        constraints: Optional[Dict] = None,
        max_results: int = 10
    ) -> List[ProductSimilarity]:
        """
        Find suitable substitutes for a product
        
        Args:
            product_id: Original product ID
            constraints: Dietary, allergen, price constraints
            max_results: Maximum number of substitutes to return
            
        Returns:
            List of ProductSimilarity objects ranked by suitability
        """
        constraints = constraints or {}
        
        if product_id not in self.product_db:
            return []
        
        original = self.product_db[product_id]
        
        # Step 1: Find candidate products
        candidates = self._get_candidates(original, constraints)
        
        # Step 2: Filter by constraints
        candidates = self._filter_by_constraints(candidates, constraints)
        
        # Step 3: Compute similarity scores
        candidates_with_scores = []
        for candidate_id in candidates:
            if candidate_id == product_id:
                continue  # Skip original
            
            candidate = self.product_db[candidate_id]
            similarity = self._compute_similarity(product_id, candidate_id)
            
            candidates_with_scores.append(ProductSimilarity(
                product_id=candidate_id,
                name=candidate["name"],
                category=candidate["category"],
                emissions=candidate["emissions"],
                price=candidate["price"],
                similarity_score=similarity,
                health_score=candidate["health"],
                attributes=candidate
            ))
        
        # Step 4: Rank by emissions reduction (primary) and similarity (secondary)
        candidates_with_scores.sort(
            key=lambda x: (-x.emissions + original["emissions"], -x.similarity_score)
        )
        
        return candidates_with_scores[:max_results]
    
    def _get_candidates(self, original: Dict, constraints: Dict) -> List[str]:
        """Get candidate products from same or related categories"""
        candidates = []
        
        # Same category
        category = original["category"]
        if category in self.category_index:
            candidates.extend(self.category_index[category])
        
        # Related categories (protein sources)
        protein_categories = ["Beef", "Chicken", "Pork", "Fish", "Tofu", "Tempeh", "Legumes"]
        if category in protein_categories:
            for cat in protein_categories:
                if cat in self.category_index:
                    candidates.extend(self.category_index[cat])
        
        # Milk alternatives
        milk_categories = ["Milk", "Plant Milk"]
        if category in milk_categories:
            for cat in milk_categories:
                if cat in self.category_index:
                    candidates.extend(self.category_index[cat])
        
        return list(set(candidates))  # Remove duplicates
    
    def _filter_by_constraints(self, candidates: List[str], constraints: Dict) -> List[str]:
        """Filter candidates by dietary and allergen constraints"""
        filtered = []
        
        for candidate_id in candidates:
            candidate = self.product_db[candidate_id]
            
            # Dietary constraints
            if constraints.get("vegetarian") and not candidate["vegetarian"]:
                continue
            
            if constraints.get("vegan"):
                # Vegan excludes dairy, eggs, etc.
                if not candidate["vegetarian"] or "dairy" in candidate["allergens"]:
                    continue
            
            # Allergen constraints
            excluded_allergens = constraints.get("allergens", [])
            if any(allergen in candidate["allergens"] for allergen in excluded_allergens):
                continue
            
            # Price constraints
            max_price = constraints.get("max_price")
            if max_price and candidate["price"] > max_price:
                continue
            
            filtered.append(candidate_id)
        
        return filtered
    
    def _compute_similarity(self, product_id1: str, product_id2: str) -> float:
        """Compute similarity between two products"""
        if product_id1 not in self.embeddings or product_id2 not in self.embeddings:
            return 0.5  # Default similarity
        
        emb1 = self.embeddings[product_id1]
        emb2 = self.embeddings[product_id2]
        
        # Cosine similarity
        dot_product = np.dot(emb1, emb2)
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.5
        
        similarity = dot_product / (norm1 * norm2)
        
        # Normalize to [0, 1]
        return (similarity + 1) / 2
    
    def get_product_info(self, product_id: str) -> Optional[Dict]:
        """Get product information"""
        return self.product_db.get(product_id)
    
    def save_database(self, filepath: str):
        """Save product database to file"""
        data = {
            'products': self.product_db,
            'category_index': self.category_index,
            'embeddings': self.embeddings,
        }
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)

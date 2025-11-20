"""Low-Carbon Basket Optimization Engine"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass
import numpy as np


@dataclass
class SwapCandidate:
    """Candidate product swap"""
    original_product_id: str
    substitute_product_id: str
    emissions_reduction: float
    cost_change: float
    similarity_score: float
    category: str


class BasketOptimizer:
    """Optimize baskets for low-carbon alternatives under constraints"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.beam_width = config.get("beam_width", 10)
        self.max_price_delta = config.get("max_price_delta", 0.03)  # ±3%
        
    def get_substitutes(
        self,
        product_id: str,
        constraints: Dict
    ) -> List[SwapCandidate]:
        """
        Find candidate substitutes for a product
        
        Args:
            product_id: Original product
            constraints: Dietary, allergen, preference constraints
            
        Returns:
            List of SwapCandidate objects
        """
        from ..substitutes.substitute_engine import SubstituteEngine
        
        # Initialize substitute engine
        if not hasattr(self, '_substitute_engine'):
            self._substitute_engine = SubstituteEngine(self.config)
        
        # Find substitutes
        substitutes = self._substitute_engine.find_substitutes(
            product_id,
            constraints,
            max_results=10
        )
        
        # Convert to SwapCandidate objects
        swap_candidates = []
        original = self._substitute_engine.get_product_info(product_id)
        
        if not original:
            return []
        
        for sub in substitutes:
            swap_candidates.append(SwapCandidate(
                original_product_id=product_id,
                substitute_product_id=sub.product_id,
                emissions_reduction=original["emissions"] - sub.emissions,
                cost_change=sub.price - original["price"],
                similarity_score=sub.similarity_score,
                category=sub.category
            ))
        
        return swap_candidates
    
    def optimize_basket(
        self,
        basket: List[Dict],
        constraints: Optional[Dict] = None
    ) -> Dict:
        """
        Optimize basket using beam search (Algorithm 1 from paper)
        
        Args:
            basket: Original basket
            constraints: Price, dietary, allergen constraints
            
        Returns:
            Optimized basket with COG, MAC_basket, etc.
        """
        constraints = constraints or {}
        
        # Initialize beam with original basket
        beam = [{"basket": basket, "score": self._compute_objective(basket, basket)}]
        
        # Beam search over products
        for product_idx, item in enumerate(basket):
            new_beam = []
            
            for candidate_basket_state in beam:
                current_basket = candidate_basket_state["basket"]
                
                # Get substitutes for current product
                substitutes = self.get_substitutes(item["product_id"], constraints)
                
                # Try each substitute
                for sub in substitutes:
                    new_basket = self._apply_swap(current_basket, product_idx, sub)
                    
                    # Check constraints
                    if self._satisfies_constraints(new_basket, basket, constraints):
                        score = self._compute_objective(new_basket, basket)
                        new_beam.append({"basket": new_basket, "score": score})
                
                # CRITICAL FIX: Only keep original if it's competitive
                # Don't always add it - let beam search decide
                if len(substitutes) == 0:
                    # No substitutes found, keep original
                    new_beam.append(candidate_basket_state)
            
            # Keep top-K
            if new_beam:
                new_beam.sort(key=lambda x: x["score"])
                beam = new_beam[:self.beam_width]
            else:
                # No valid candidates, keep current beam
                pass
        
        # Best basket (fallback to original if beam is empty)
        if not beam:
            optimized = basket
        else:
            optimized = beam[0]["basket"]
        
        # Compute metrics
        original_emissions = sum(p.get("emissions", 0) for p in basket)
        optimized_emissions = sum(p.get("emissions", 0) for p in optimized)
        original_cost = sum(p["price"] * p["quantity"] for p in basket)
        optimized_cost = sum(p["price"] * p["quantity"] for p in optimized)
        
        cog = original_emissions - optimized_emissions
        cog_ratio = cog / original_emissions if original_emissions > 0 else 0.0
        
        emissions_reduction = original_emissions - optimized_emissions
        mac_basket = (
            (optimized_cost - original_cost) / emissions_reduction
            if emissions_reduction > 0
            else float('inf')
        )
        
        return {
            "optimized_basket": optimized,
            "emissions": optimized_emissions,
            "cost": optimized_cost,
            "cog": cog,
            "cog_ratio": cog_ratio,
            "mac_basket": mac_basket,
        }
    
    def _compute_objective(self, basket: List[Dict], original_basket: Optional[List[Dict]] = None) -> float:
        """
        Compute multi-objective score J(B')
        
        J(B') = α*E(B') + β*C(B') + γ*D(B,B') + δ*(1-H(B'))
        """
        alpha = self.config.get("weight_emissions", 1.0)
        beta = self.config.get("weight_cost", 0.1)
        gamma = self.config.get("weight_dissimilarity", 0.5)
        delta = self.config.get("weight_health", 0.3)
        
        emissions = sum(p.get("emissions", 0) for p in basket)
        cost = sum(p["price"] * p["quantity"] for p in basket)
        health = sum(p.get("health_score", 0.5) for p in basket) / len(basket) if basket else 0.5
        
        # Compute dissimilarity if original basket provided
        dissimilarity = 0.0
        if original_basket and hasattr(self, '_substitute_engine'):
            dissimilarity = self._compute_basket_dissimilarity(basket, original_basket)
        
        return alpha * emissions + beta * cost + gamma * dissimilarity + delta * (1 - health)
    
    def _compute_basket_dissimilarity(self, basket1: List[Dict], basket2: List[Dict]) -> float:
        """Compute dissimilarity between two baskets"""
        if len(basket1) != len(basket2):
            return 1.0  # Maximum dissimilarity
        
        total_dissimilarity = 0.0
        for item1, item2 in zip(basket1, basket2):
            if item1["product_id"] == item2["product_id"]:
                continue  # Same product, no dissimilarity
            
            # Compute product-level dissimilarity
            similarity = self._substitute_engine._compute_similarity(
                item1["product_id"],
                item2["product_id"]
            )
            dissimilarity = 1.0 - similarity
            total_dissimilarity += dissimilarity
        
        # Normalize by basket size
        return total_dissimilarity / len(basket1) if basket1 else 0.0
    
    def _apply_swap(
        self,
        basket: List[Dict],
        product_idx: int,
        swap: SwapCandidate
    ) -> List[Dict]:
        """Apply a swap to create new basket with full substitute data"""
        # CRITICAL FIX: Deep copy and get full substitute info
        new_basket = [item.copy() for item in basket]
        
        # Get full substitute product information
        sub_product = self._substitute_engine.get_product_info(swap.substitute_product_id)
        
        if sub_product:
            # Replace with complete substitute data
            original_quantity = new_basket[product_idx].get("quantity", 1.0)
            new_basket[product_idx] = {
                "product_id": swap.substitute_product_id,
                "name": sub_product["name"],
                "quantity": original_quantity,
                "price": sub_product["price"],
                "emissions": sub_product["emissions"],
                "category": sub_product["category"],
                "health_score": sub_product.get("health", 0.5),
                "vegetarian": sub_product.get("vegetarian", False),
                "allergens": sub_product.get("allergens", []),
            }
        
        return new_basket
    
    def _satisfies_constraints(
        self,
        new_basket: List[Dict],
        original_basket: List[Dict],
        constraints: Dict
    ) -> bool:
        """Check if basket satisfies all constraints"""
        # Price constraint (basket-level)
        original_cost = sum(p.get("price", 0) * p.get("quantity", 1) for p in original_basket)
        new_cost = sum(p.get("price", 0) * p.get("quantity", 1) for p in new_basket)
        
        # CRITICAL FIX: Avoid division by zero
        if original_cost > 0:
            max_delta = constraints.get("max_price_delta", self.max_price_delta)
            cost_change_ratio = abs(new_cost - original_cost) / original_cost
            if cost_change_ratio > max_delta:
                return False
        
        # Dietary constraints
        if constraints.get("vegetarian"):
            for item in new_basket:
                if not item.get("vegetarian", True):
                    return False
        
        if constraints.get("vegan"):
            for item in new_basket:
                if not item.get("vegetarian", True):
                    return False
                if "dairy" in item.get("allergens", []):
                    return False
        
        # Allergen constraints
        excluded_allergens = constraints.get("allergens", [])
        if excluded_allergens:
            for item in new_basket:
                item_allergens = item.get("allergens", [])
                if any(a in item_allergens for a in excluded_allergens):
                    return False
        
        return True

"""Behavioral Model for Swap Acceptance Prediction"""

import numpy as np
from typing import Dict, List
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier


class AcceptanceModel:
    """Predict probability of user accepting a swap suggestion"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load pre-trained acceptance model"""
        model_path = self.config.get("model_path", "models/acceptance_model.pkl")
        
        # Try to load trained model
        try:
            import pickle
            from pathlib import Path
            
            if Path(model_path).exists():
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                print(f"✅ Loaded trained model from {model_path}")
                return
        except Exception as e:
            print(f"⚠️  Could not load model from {model_path}: {e}")
        
        # Fallback to untrained model
        model_type = self.config.get("acceptance_model_type", "logistic")
        
        if model_type == "logistic":
            self.model = LogisticRegression()
        elif model_type == "gbm":
            self.model = GradientBoostingClassifier()
        
        print(f"⚠️  Using untrained {model_type} model (heuristic fallback)")
    
    def predict_acceptance(
        self,
        swap: Dict,
        user_context: Dict,
        message_type: str = "conversational"
    ) -> float:
        """
        Predict probability that user accepts a swap
        
        Args:
            swap: Swap details (price_change, emissions_reduction, etc.)
            user_context: User features and history
            message_type: Type of explanation (numeric, conversational, etc.)
            
        Returns:
            Acceptance probability p_s ∈ [0, 1]
        """
        features = self._extract_features(swap, user_context, message_type)
        
        if self.model is None:
            # Fallback heuristic
            return self._heuristic_acceptance(swap, message_type)
        
        prob = self.model.predict_proba([features])[0][1]
        return prob
    
    def _extract_features(
        self,
        swap: Dict,
        user_context: Dict,
        message_type: str
    ) -> List[float]:
        """Extract features for acceptance prediction"""
        features = [
            swap.get("price_change", 0.0),
            swap.get("emissions_reduction", 0.0),
            swap.get("similarity_score", 0.5),
            1.0 if swap.get("brand_change", False) else 0.0,
            user_context.get("prior_acceptance_rate", 0.3),
            user_context.get("sustainability_score", 0.5),
            1.0 if message_type == "conversational" else 0.0,
        ]
        return features
    
    def _heuristic_acceptance(self, swap: Dict, message_type: str) -> float:
        """Heuristic acceptance probability when model unavailable"""
        base_rate = 0.17 if message_type == "numeric" else 0.36
        
        # Adjust for price change
        price_change = swap.get("price_change", 0.0)
        if price_change > 0:
            base_rate *= 0.8  # Penalty for price increase
        
        # Adjust for emissions reduction
        emissions_reduction = swap.get("emissions_reduction", 0.0)
        if emissions_reduction > 5.0:
            base_rate *= 1.2  # Bonus for large reduction
        
        return np.clip(base_rate, 0.0, 1.0)
    
    def simulate_swaps(
        self,
        swaps: List[Dict],
        user_context: Dict,
        message_type: str = "conversational"
    ) -> Dict:
        """
        Simulate acceptance for all swaps and compute BAE
        
        Returns:
            Dict with swaps, acceptance probs, and BAE
        """
        enriched_swaps = []
        total_bae = 0.0
        
        for swap in swaps:
            acceptance_prob = self.predict_acceptance(swap, user_context, message_type)
            emissions_reduction = swap.get("emissions_reduction", 0.0)
            
            enriched_swaps.append({
                **swap,
                "acceptance_prob": acceptance_prob,
            })
            
            total_bae += acceptance_prob * emissions_reduction
        
        avg_acceptance = (
            sum(s["acceptance_prob"] for s in enriched_swaps) / len(enriched_swaps)
            if enriched_swaps
            else 0.0
        )
        
        return {
            "swaps": enriched_swaps,
            "bae": total_bae,
            "avg_acceptance": avg_acceptance,
        }

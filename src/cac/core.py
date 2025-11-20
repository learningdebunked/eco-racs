"""Core Carbon-Aware Checkout orchestration"""

from typing import Dict, List, Optional
from dataclasses import dataclass

from .lca.emissions_engine import EmissionsEngine
from .optimization.basket_optimizer import BasketOptimizer
from .behavior.acceptance_model import AcceptanceModel
from .genai.explanation_generator import ExplanationGenerator
from .mcp.mcp_orchestrator import MCPOrchestrator
from .metrics import CarbonMetrics


@dataclass
class CheckoutResult:
    """Result of carbon-aware checkout analysis"""
    basket_id: str
    emissions: float
    emissions_optimized: float
    cog: float
    cog_ratio: float
    bae: float
    racs: float
    mac_basket: float
    cost_original: float
    cost_optimized: float
    swaps: List[Dict]
    explanation: str
    acceptance_rate: float


class CarbonAwareCheckout:
    """Main orchestrator for Carbon-Aware Checkout system"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.emissions_engine = EmissionsEngine(self.config)
        self.optimizer = BasketOptimizer(self.config)
        self.acceptance_model = AcceptanceModel(self.config)
        self.explanation_generator = ExplanationGenerator(self.config)
        self.mcp = MCPOrchestrator(self.config)
        self.metrics = CarbonMetrics()
    
    def analyze_basket(self, basket: List[Dict], user_context: Optional[Dict] = None) -> CheckoutResult:
        """
        Analyze basket and generate carbon-aware recommendations
        
        Args:
            basket: List of products with quantities
            user_context: Optional user preferences and constraints
            
        Returns:
            CheckoutResult with emissions, swaps, and explanations
        """
        # CRITICAL FIX: Enrich basket with emissions data before processing
        enriched_basket = self._enrich_basket_with_emissions(basket)
        
        # Compute baseline emissions via MCP
        emissions_data = self.mcp.call_tool(
            "calculate_basket_emissions",
            {"basket": enriched_basket}
        )
        
        # Optimize basket for low-carbon alternatives (use enriched basket)
        optimization_result = self.mcp.call_tool(
            "optimize_basket",
            {
                "basket": enriched_basket,
                "constraints": user_context or {},
            }
        )
        
        # Simulate swap acceptance (use enriched basket)
        swap_simulation = self.mcp.call_tool(
            "simulate_swaps",
            {
                "basket": enriched_basket,
                "optimized_basket": optimization_result["optimized_basket"],
            }
        )
        
        # Generate LLM explanation (use enriched basket)
        explanation = self.explanation_generator.generate(
            basket=enriched_basket,
            emissions_data=emissions_data,
            optimization_result=optimization_result,
            swap_simulation=swap_simulation,
        )
        
        # Audit log
        self.mcp.call_tool("audit_log", {
            "event": "basket_analysis",
            "basket_id": enriched_basket[0].get("basket_id", "unknown"),
            "emissions": emissions_data,
            "optimization": optimization_result,
        })
        
        return CheckoutResult(
            basket_id=enriched_basket[0].get("basket_id", "unknown"),
            emissions=emissions_data["emissions"],
            emissions_optimized=optimization_result["emissions"],
            cog=optimization_result["cog"],
            cog_ratio=optimization_result["cog_ratio"],
            bae=swap_simulation["bae"],
            racs=emissions_data["racs"],
            mac_basket=optimization_result["mac_basket"],
            cost_original=sum(p.get("price", 0) * p.get("quantity", 1) for p in enriched_basket),
            cost_optimized=optimization_result["cost"],
            swaps=swap_simulation["swaps"],
            explanation=explanation,
            acceptance_rate=swap_simulation["avg_acceptance"],
        )
    
    def _enrich_basket_with_emissions(self, basket: List[Dict]) -> List[Dict]:
        """
        Enrich basket items with emissions and category data from LCA database
        
        This is CRITICAL for optimization to work - products need emissions data!
        """
        enriched = []
        
        for item in basket:
            product_id = item.get("product_id", "")
            
            # Get footprint from LCA database
            footprint = self.emissions_engine.get_product_footprint(product_id)
            
            # Create enriched item with all necessary data
            enriched_item = {
                **item,  # Keep original data
                "emissions": footprint.emissions_mean if footprint else 5.0,
                "emissions_variance": footprint.emissions_variance if footprint else 2.0,
                "category": footprint.category if footprint else "Unknown",
            }
            
            # Also add health score if not present
            if "health_score" not in enriched_item:
                from .health.health_scorer import HealthScorer
                health_scorer = HealthScorer()
                enriched_item["health_score"] = health_scorer.get_health_score(
                    product_id,
                    enriched_item["category"]
                )
            
            enriched.append(enriched_item)
        
        return enriched

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
        # Compute baseline emissions via MCP
        emissions_data = self.mcp.call_tool(
            "calculate_basket_emissions",
            {"basket": basket}
        )
        
        # Optimize basket for low-carbon alternatives
        optimization_result = self.mcp.call_tool(
            "optimize_basket",
            {
                "basket": basket,
                "constraints": user_context or {},
            }
        )
        
        # Simulate swap acceptance
        swap_simulation = self.mcp.call_tool(
            "simulate_swaps",
            {
                "basket": basket,
                "optimized_basket": optimization_result["optimized_basket"],
            }
        )
        
        # Generate LLM explanation
        explanation = self.explanation_generator.generate(
            basket=basket,
            emissions_data=emissions_data,
            optimization_result=optimization_result,
            swap_simulation=swap_simulation,
        )
        
        # Audit log
        self.mcp.call_tool("audit_log", {
            "event": "basket_analysis",
            "basket_id": basket[0].get("basket_id", "unknown"),
            "emissions": emissions_data,
            "optimization": optimization_result,
        })
        
        return CheckoutResult(
            basket_id=basket[0].get("basket_id", "unknown"),
            emissions=emissions_data["emissions"],
            emissions_optimized=optimization_result["emissions"],
            cog=optimization_result["cog"],
            cog_ratio=optimization_result["cog_ratio"],
            bae=swap_simulation["bae"],
            racs=emissions_data["racs"],
            mac_basket=optimization_result["mac_basket"],
            cost_original=sum(p["price"] * p["quantity"] for p in basket),
            cost_optimized=optimization_result["cost"],
            swaps=swap_simulation["swaps"],
            explanation=explanation,
            acceptance_rate=swap_simulation["avg_acceptance"],
        )

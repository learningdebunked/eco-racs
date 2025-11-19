"""Model Context Protocol (MCP) Orchestration Layer"""

from typing import Dict, Any, List
import json
import logging
from datetime import datetime


class MCPOrchestrator:
    """
    MCP-based tool orchestration for deterministic, auditable carbon claims
    Ensures FTC Green Guides and EU Green Claims Directive compliance
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.audit_log = []
        self.tools = self._register_tools()
        self.logger = logging.getLogger(__name__)
    
    def _register_tools(self) -> Dict:
        """Register MCP tools"""
        return {
            "calculate_basket_emissions": self._tool_calculate_emissions,
            "optimize_basket": self._tool_optimize_basket,
            "simulate_swaps": self._tool_simulate_swaps,
            "generate_explanation": self._tool_generate_explanation,
            "audit_log": self._tool_audit_log,
        }
    
    def call_tool(self, tool_name: str, params: Dict) -> Any:
        """
        Call an MCP tool with parameters
        
        Args:
            tool_name: Name of the tool
            params: Tool parameters
            
        Returns:
            Tool result
        """
        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        self.logger.info(f"MCP tool call: {tool_name}")
        
        # Execute tool
        result = self.tools[tool_name](params)
        
        # Log for audit trail
        self._log_tool_call(tool_name, params, result)
        
        return result
    
    def _tool_calculate_emissions(self, params: Dict) -> Dict:
        """MCP tool: calculate_basket_emissions"""
        from ..lca.emissions_engine import EmissionsEngine
        
        engine = EmissionsEngine(self.config)
        basket = params["basket"]
        
        result = engine.calculate_basket_emissions(basket)
        
        return {
            "emissions": result["emissions"],
            "variance": result["variance"],
            "racs": result["racs"],
            "product_emissions": result["product_emissions"],
            "metadata": {
                "lca_sources": ["Poore & Nemecek 2018", "Open Food Facts"],
                "system_boundary": "cradle-to-retail",
                "timestamp": datetime.utcnow().isoformat(),
            }
        }
    
    def _tool_optimize_basket(self, params: Dict) -> Dict:
        """MCP tool: optimize_basket"""
        from ..optimization.basket_optimizer import BasketOptimizer
        
        optimizer = BasketOptimizer(self.config)
        basket = params["basket"]
        constraints = params.get("constraints", {})
        
        result = optimizer.optimize_basket(basket, constraints)
        
        return {
            **result,
            "metadata": {
                "algorithm": "beam_search",
                "beam_width": optimizer.beam_width,
                "constraints": constraints,
                "timestamp": datetime.utcnow().isoformat(),
            }
        }
    
    def _tool_simulate_swaps(self, params: Dict) -> Dict:
        """MCP tool: simulate_swaps"""
        from ..behavior.acceptance_model import AcceptanceModel
        
        model = AcceptanceModel(self.config)
        basket = params["basket"]
        optimized_basket = params.get("optimized_basket", basket)
        
        # Generate swaps from optimization
        swaps = self._extract_swaps(basket, optimized_basket)
        
        user_context = params.get("user_context", {})
        message_type = params.get("message_type", "conversational")
        
        result = model.simulate_swaps(swaps, user_context, message_type)
        
        return {
            **result,
            "metadata": {
                "model_type": "acceptance_predictor",
                "message_type": message_type,
                "timestamp": datetime.utcnow().isoformat(),
            }
        }
    
    def _tool_generate_explanation(self, params: Dict) -> str:
        """MCP tool: generate_explanation"""
        from ..genai.explanation_generator import ExplanationGenerator
        
        generator = ExplanationGenerator(self.config)
        
        explanation = generator.generate(
            basket=params["basket"],
            emissions_data=params["emissions_data"],
            optimization_result=params["optimization_result"],
            swap_simulation=params["swap_simulation"],
            message_type=params.get("message_type", "conversational"),
        )
        
        return explanation
    
    def _tool_audit_log(self, params: Dict) -> Dict:
        """MCP tool: audit_log - persist event for compliance"""
        event = {
            "event_type": params.get("event"),
            "timestamp": datetime.utcnow().isoformat(),
            "data": params,
        }
        
        self.audit_log.append(event)
        
        # TODO: Persist to database
        
        return {"status": "logged", "event_id": len(self.audit_log)}
    
    def _log_tool_call(self, tool_name: str, params: Dict, result: Any):
        """Log tool call for audit trail"""
        log_entry = {
            "tool": tool_name,
            "timestamp": datetime.utcnow().isoformat(),
            "params": params,
            "result": result,
        }
        self.audit_log.append(log_entry)
    
    def _extract_swaps(self, original: List[Dict], optimized: List[Dict]) -> List[Dict]:
        """Extract swap operations from original and optimized baskets"""
        swaps = []
        
        for i, (orig_item, opt_item) in enumerate(zip(original, optimized)):
            if orig_item["product_id"] != opt_item["product_id"]:
                swaps.append({
                    "original_product_id": orig_item["product_id"],
                    "substitute_product_id": opt_item["product_id"],
                    "emissions_reduction": orig_item.get("emissions", 0) - opt_item.get("emissions", 0),
                    "price_change": (opt_item["price"] - orig_item["price"]) * orig_item["quantity"],
                    "description": f"Swap {orig_item.get('name', 'product')} for {opt_item.get('name', 'alternative')}",
                })
        
        return swaps
    
    def export_audit_log(self, filepath: str):
        """Export audit log for compliance verification"""
        with open(filepath, 'w') as f:
            json.dump(self.audit_log, f, indent=2)

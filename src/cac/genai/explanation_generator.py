"""GenAI-Driven Explanation Generation using LLMs"""

from typing import Dict, List, Optional
import os


class ExplanationGenerator:
    """Generate persuasive, personalized explanations using LLMs"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.llm_provider = config.get("llm_provider", "openai")
        self.model = config.get("llm_model", "gpt-4")
        self._init_llm_client()
    
    def _init_llm_client(self):
        """Initialize LLM client (OpenAI, Anthropic, etc.)"""
        if self.llm_provider == "openai":
            try:
                import openai
                self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            except ImportError:
                self.client = None
        elif self.llm_provider == "anthropic":
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            except ImportError:
                self.client = None
    
    def generate(
        self,
        basket: List[Dict],
        emissions_data: Dict,
        optimization_result: Dict,
        swap_simulation: Dict,
        message_type: str = "conversational"
    ) -> str:
        """
        Generate explanation for carbon score and swap recommendations
        
        Args:
            basket: Original basket
            emissions_data: Emissions calculation results
            optimization_result: Optimization results
            swap_simulation: Swap acceptance simulation
            message_type: Type of message to generate
            
        Returns:
            Generated explanation text
        """
        if message_type == "numeric":
            return self._generate_numeric_explanation(emissions_data, optimization_result)
        elif message_type == "conversational":
            return self._generate_conversational_explanation(
                basket, emissions_data, optimization_result, swap_simulation
            )
        else:
            return self._generate_default_explanation(emissions_data)
    
    def _generate_numeric_explanation(
        self,
        emissions_data: Dict,
        optimization_result: Dict
    ) -> str:
        """Generate simple numeric explanation"""
        emissions = emissions_data["emissions"]
        cog = optimization_result["cog"]
        
        return f"Your basket emits {emissions:.1f} kg CO2e. You could save {cog:.1f} kg CO2e."
    
    def _generate_conversational_explanation(
        self,
        basket: List[Dict],
        emissions_data: Dict,
        optimization_result: Dict,
        swap_simulation: Dict
    ) -> str:
        """Generate LLM-powered conversational explanation"""
        if self.client is None:
            return self._generate_fallback_explanation(emissions_data, optimization_result)
        
        prompt = self._build_prompt(basket, emissions_data, optimization_result, swap_simulation)
        
        try:
            if self.llm_provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self._get_system_prompt()},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=300,
                )
                return response.choices[0].message.content
            elif self.llm_provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}],
                    system=self._get_system_prompt(),
                )
                return response.content[0].text
        except Exception as e:
            print(f"LLM generation failed: {e}")
            return self._generate_fallback_explanation(emissions_data, optimization_result)
    
    def _get_system_prompt(self) -> str:
        """System prompt for LLM"""
        return """You are a helpful sustainability assistant helping shoppers understand 
        the carbon footprint of their grocery basket. Generate a friendly, persuasive 
        explanation that:
        1. Explains the carbon impact in relatable terms
        2. Highlights specific swap opportunities
        3. Emphasizes co-benefits (health, cost savings)
        4. Uses positive, encouraging language
        5. Keeps it concise (2-3 sentences)
        
        Be factual and avoid greenwashing. Base all claims on the provided data."""
    
    def _build_prompt(
        self,
        basket: List[Dict],
        emissions_data: Dict,
        optimization_result: Dict,
        swap_simulation: Dict
    ) -> str:
        """Build prompt for LLM"""
        emissions = emissions_data["emissions"]
        cog = optimization_result["cog"]
        cost_change = optimization_result["cost"] - sum(p["price"] * p["quantity"] for p in basket)
        top_swaps = swap_simulation["swaps"][:3]
        
        prompt = f"""
        Basket emissions: {emissions:.1f} kg CO2e
        Potential savings: {cog:.1f} kg CO2e ({optimization_result['cog_ratio']*100:.1f}%)
        Cost change: ${cost_change:.2f}
        
        Top swap opportunities:
        """
        
        for swap in top_swaps:
            prompt += f"\n- {swap.get('description', 'Product swap')}: saves {swap['emissions_reduction']:.1f} kg CO2e"
        
        prompt += "\n\nGenerate a friendly explanation for the shopper."
        
        return prompt
    
    def _generate_fallback_explanation(
        self,
        emissions_data: Dict,
        optimization_result: Dict
    ) -> str:
        """Fallback explanation when LLM unavailable"""
        emissions = emissions_data["emissions"]
        cog = optimization_result["cog"]
        cog_ratio = optimization_result["cog_ratio"]
        
        return f"""Your basket has a carbon footprint of {emissions:.1f} kg CO2e. 
        We found some simple swaps that could reduce your impact by {cog:.1f} kg CO2e 
        ({cog_ratio*100:.1f}%) with minimal cost change. Small changes add up!"""
    
    def _generate_default_explanation(self, emissions_data: Dict) -> str:
        """Default explanation"""
        return f"Your basket emits {emissions_data['emissions']:.1f} kg CO2e."

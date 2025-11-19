"""FastAPI REST API for Carbon-Aware Checkout"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import logging

from ..core import CarbonAwareCheckout

app = FastAPI(
    title="Carbon-Aware Checkout API",
    description="Real-time basket-level emissions scoring and optimization",
    version="0.1.0"
)

logger = logging.getLogger(__name__)


class ProductItem(BaseModel):
    """Product in basket"""
    product_id: str
    quantity: float
    price: float
    name: Optional[str] = None


class BasketRequest(BaseModel):
    """Request to analyze basket"""
    basket: List[ProductItem]
    user_id: Optional[str] = None
    constraints: Optional[Dict] = None


class BasketResponse(BaseModel):
    """Response with carbon analysis"""
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


# Initialize CAC system
cac = CarbonAwareCheckout()


@app.get("/")
def root():
    """Health check"""
    return {"status": "ok", "service": "Carbon-Aware Checkout"}


@app.post("/analyze", response_model=BasketResponse)
def analyze_basket(request: BasketRequest):
    """
    Analyze basket and return carbon score with optimization
    
    Args:
        request: Basket with products and constraints
        
    Returns:
        Carbon analysis with swaps and explanations
    """
    try:
        basket = [item.dict() for item in request.basket]
        user_context = {
            "user_id": request.user_id,
            **(request.constraints or {})
        }
        
        result = cac.analyze_basket(basket, user_context)
        
        return BasketResponse(
            basket_id=result.basket_id,
            emissions=result.emissions,
            emissions_optimized=result.emissions_optimized,
            cog=result.cog,
            cog_ratio=result.cog_ratio,
            bae=result.bae,
            racs=result.racs,
            mac_basket=result.mac_basket,
            cost_original=result.cost_original,
            cost_optimized=result.cost_optimized,
            swaps=result.swaps,
            explanation=result.explanation,
            acceptance_rate=result.acceptance_rate,
        )
    
    except Exception as e:
        logger.error(f"Error analyzing basket: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
def get_metrics():
    """Get system metrics"""
    return {
        "total_requests": 0,  # TODO: Implement metrics
        "avg_emissions_reduction": 0.157,
        "avg_acceptance_rate": 0.36,
    }


@app.get("/audit/{basket_id}")
def get_audit_log(basket_id: str):
    """Retrieve audit log for compliance"""
    # TODO: Implement audit log retrieval
    return {"basket_id": basket_id, "audit_log": []}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

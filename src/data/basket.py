"""Basket data structures and utilities"""
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class Product:
    """Represents a single product"""
    id: str
    name: str
    category: str
    price: float  # USD per unit
    quantity_kg: float
    emissions_mean: float  # kg CO2e per kg
    emissions_std: float
    health_score: Optional[float] = None
    attributes: Dict = None
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}


@dataclass
class Basket:
    """Represents a shopping basket"""
    id: str
    products: List[Product]
    user_id: Optional[str] = None
    
    def total_emissions(self) -> float:
        """Calculate total basket emissions"""
        return sum(p.emissions_mean * p.quantity_kg for p in self.products)
    
    def total_cost(self) -> float:
        """Calculate total basket cost"""
        return sum(p.price * p.quantity_kg for p in self.products)
    
    def total_weight(self) -> float:
        """Calculate total basket weight"""
        return sum(p.quantity_kg for p in self.products)

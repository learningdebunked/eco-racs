"""Carbon-Aware Checkout (CAC) - Main Package"""

from .core import CarbonAwareCheckout
from .metrics import CarbonMetrics

__version__ = "0.1.0"
__all__ = ["CarbonAwareCheckout", "CarbonMetrics"]

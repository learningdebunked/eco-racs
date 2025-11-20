#!/usr/bin/env python3
"""Test that optimization is actually finding swaps"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cac import CarbonAwareCheckout


def test_optimization():
    """Test with products that exist in substitute engine"""
    print("\n" + "="*70)
    print("TESTING OPTIMIZATION WITH REAL PRODUCT IDS")
    print("="*70)
    
    cac = CarbonAwareCheckout()
    
    # Use product IDs that exist in substitute engine
    basket = [
        {
            "basket_id": "test_001",
            "product_id": "beef_001",  # High carbon
            "name": "Ground Beef",
            "quantity": 1.0,
            "price": 8.99,
        },
        {
            "basket_id": "test_001",
            "product_id": "milk_001",  # Medium carbon
            "name": "Whole Milk",
            "quantity": 1.0,
            "price": 4.99,
        },
    ]
    
    print("\n📦 Original Basket:")
    for item in basket:
        print(f"  - {item['name']}: ${item['price']:.2f}")
    
    # Analyze
    result = cac.analyze_basket(basket)
    
    print(f"\n📊 Results:")
    print(f"  Original emissions: {result.emissions:.1f} kg CO2e")
    print(f"  Optimized emissions: {result.emissions_optimized:.1f} kg CO2e")
    print(f"  COG: {result.cog:.1f} kg CO2e ({result.cog_ratio*100:.1f}%)")
    print(f"  Number of swaps found: {len(result.swaps)}")
    
    if len(result.swaps) > 0:
        print(f"\n🔄 Recommended Swaps:")
        for i, swap in enumerate(result.swaps[:3], 1):
            print(f"  {i}. {swap.get('description', 'Swap')}")
            print(f"     Saves: {swap.get('emissions_reduction', 0):.1f} kg CO2e")
            print(f"     Cost change: ${swap.get('price_change', 0):.2f}")
            print(f"     Acceptance: {swap.get('acceptance_prob', 0)*100:.0f}%")
        
        print("\n✅ SUCCESS: Optimization is finding swaps!")
        return True
    else:
        print("\n❌ FAILURE: No swaps found")
        print("\nDebugging info:")
        print(f"  Basket had emissions data: {result.emissions > 0}")
        print(f"  BAE: {result.bae}")
        print(f"  MAC: {result.mac_basket}")
        return False


if __name__ == "__main__":
    success = test_optimization()
    sys.exit(0 if success else 1)

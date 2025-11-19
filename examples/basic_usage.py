#!/usr/bin/env python3
"""Basic usage example for Carbon-Aware Checkout"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cac import CarbonAwareCheckout


def main():
    """Demonstrate basic CAC usage"""
    
    # Initialize system
    cac = CarbonAwareCheckout()
    
    # Example basket
    basket = [
        {
            "basket_id": "example_001",
            "product_id": "beef_ground_001",
            "name": "Ground Beef (1 lb)",
            "quantity": 1.0,
            "price": 8.99,
        },
        {
            "basket_id": "example_001",
            "product_id": "milk_whole_001",
            "name": "Whole Milk (1 gallon)",
            "quantity": 1.0,
            "price": 4.99,
        },
        {
            "basket_id": "example_001",
            "product_id": "bread_wheat_001",
            "name": "Whole Wheat Bread",
            "quantity": 1.0,
            "price": 3.49,
        },
    ]
    
    # Analyze basket
    print("Analyzing basket...")
    result = cac.analyze_basket(basket)
    
    # Display results
    print("\n" + "="*60)
    print("CARBON-AWARE CHECKOUT RESULTS")
    print("="*60)
    
    print(f"\n📊 Original Basket:")
    print(f"   Emissions: {result.emissions:.1f} kg CO2e")
    print(f"   Cost: ${result.cost_original:.2f}")
    
    print(f"\n🌱 Optimized Basket:")
    print(f"   Emissions: {result.emissions_optimized:.1f} kg CO2e")
    print(f"   Cost: ${result.cost_optimized:.2f}")
    
    print(f"\n💡 Carbon Opportunity Gap (COG):")
    print(f"   Potential savings: {result.cog:.1f} kg CO2e ({result.cog_ratio*100:.1f}%)")
    
    print(f"\n🎯 Behavior-Adjusted Emissions (BAE):")
    print(f"   Expected savings: {result.bae:.1f} kg CO2e")
    print(f"   Acceptance rate: {result.acceptance_rate*100:.1f}%")
    
    print(f"\n⚠️  Risk-Adjusted Carbon Score (RACS):")
    print(f"   Upper bound (95%): {result.racs:.1f} kg CO2e")
    
    print(f"\n💰 Marginal Abatement Cost:")
    print(f"   ${result.mac_basket:.2f} per kg CO2e avoided")
    
    print(f"\n🔄 Recommended Swaps:")
    for i, swap in enumerate(result.swaps[:3], 1):
        print(f"   {i}. {swap.get('description', 'Swap')}")
        print(f"      Saves: {swap['emissions_reduction']:.1f} kg CO2e")
        print(f"      Cost change: ${swap['price_change']:.2f}")
        print(f"      Acceptance: {swap['acceptance_prob']*100:.0f}%")
    
    print(f"\n💬 Explanation:")
    print(f"   {result.explanation}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()

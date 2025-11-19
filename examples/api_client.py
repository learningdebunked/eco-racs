#!/usr/bin/env python3
"""Example API client for Carbon-Aware Checkout"""

import requests
import json


def analyze_basket_via_api():
    """Call CAC API to analyze a basket"""
    
    api_url = "http://localhost:8000/analyze"
    
    # Example basket
    basket_request = {
        "basket": [
            {
                "product_id": "beef_001",
                "quantity": 1.0,
                "price": 8.99,
                "name": "Ground Beef"
            },
            {
                "product_id": "chicken_001",
                "quantity": 1.0,
                "price": 6.99,
                "name": "Chicken Breast"
            }
        ],
        "user_id": "user_123",
        "constraints": {
            "max_price_delta": 0.03,
            "dietary_preference": "omnivore"
        }
    }
    
    # Make request
    response = requests.post(api_url, json=basket_request)
    
    if response.status_code == 200:
        result = response.json()
        
        print("✅ Analysis successful!")
        print(f"\nEmissions: {result['emissions']:.1f} kg CO2e")
        print(f"COG: {result['cog']:.1f} kg CO2e ({result['cog_ratio']*100:.1f}%)")
        print(f"\nExplanation: {result['explanation']}")
        
        return result
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None


if __name__ == "__main__":
    analyze_basket_via_api()

#!/usr/bin/env python3
"""
Test that all critical gaps have been fixed

This script validates that all components work end-to-end
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_gap_1_substitute_search():
    """Test: Product substitute search engine works"""
    print("\n" + "="*70)
    print("GAP 1: Product Substitute Search")
    print("="*70)
    
    from cac.substitutes.substitute_engine import SubstituteEngine
    
    engine = SubstituteEngine()
    
    # Test finding substitutes for beef
    substitutes = engine.find_substitutes("beef_001", {}, max_results=5)
    
    print(f"\nFound {len(substitutes)} substitutes for beef:")
    for sub in substitutes[:3]:
        print(f"  - {sub.name}: {sub.emissions:.1f} kg CO2e (saves {60.0 - sub.emissions:.1f})")
    
    assert len(substitutes) > 0, "No substitutes found!"
    print("\n✅ GAP 1 FIXED: Substitute search working")
    return True


def test_gap_2_lca_data():
    """Test: Real LCA data loading"""
    print("\n" + "="*70)
    print("GAP 2: LCA Data Integration")
    print("="*70)
    
    from cac.data.data_loader import DataLoader
    
    loader = DataLoader()
    poore_nemecek = loader.load_poore_nemecek_data()
    
    print(f"\nLoaded {len(poore_nemecek)} LCA categories")
    print(f"Sample categories: {poore_nemecek['category'].head().tolist()}")
    
    assert len(poore_nemecek) > 10, "Too few categories loaded!"
    print("\n✅ GAP 2 FIXED: LCA data loading working")
    return True


def test_gap_3_emissions_engine():
    """Test: Emissions engine with real data"""
    print("\n" + "="*70)
    print("GAP 3: Emissions Engine Integration")
    print("="*70)
    
    from cac.lca.emissions_engine import EmissionsEngine
    
    engine = EmissionsEngine({})
    
    basket = [
        {"product_id": "Beef", "quantity": 1.0},
        {"product_id": "Chicken", "quantity": 1.0},
    ]
    
    result = engine.calculate_basket_emissions(basket)
    
    print(f"\nBasket emissions: {result['emissions']:.1f} kg CO2e")
    print(f"RACS (95%): {result['racs']:.1f} kg CO2e")
    
    assert result['emissions'] > 0, "Emissions not calculated!"
    print("\n✅ GAP 3 FIXED: Emissions engine working")
    return True


def test_gap_4_optimization():
    """Test: Optimization with substitutes"""
    print("\n" + "="*70)
    print("GAP 4: Optimization with Substitutes")
    print("="*70)
    
    from cac.optimization.basket_optimizer import BasketOptimizer
    
    optimizer = BasketOptimizer({})
    
    basket = [
        {"product_id": "beef_001", "name": "Beef", "quantity": 1.0, "price": 8.99, "emissions": 60.0},
        {"product_id": "milk_001", "name": "Milk", "quantity": 1.0, "price": 4.99, "emissions": 3.2},
    ]
    
    result = optimizer.optimize_basket(basket, {})
    
    print(f"\nOriginal emissions: {sum(p['emissions'] for p in basket):.1f} kg CO2e")
    print(f"Optimized emissions: {result['emissions']:.1f} kg CO2e")
    print(f"COG: {result['cog']:.1f} kg CO2e ({result['cog_ratio']*100:.1f}%)")
    
    assert result['cog'] >= 0, "COG not calculated!"
    print("\n✅ GAP 4 FIXED: Optimization working")
    return True


def test_gap_5_health_scores():
    """Test: Health score integration"""
    print("\n" + "="*70)
    print("GAP 5: Health Score Integration")
    print("="*70)
    
    from cac.health.health_scorer import HealthScorer
    
    scorer = HealthScorer()
    
    # Test individual scores
    beef_score = scorer.get_health_score("beef_001", "Beef")
    tofu_score = scorer.get_health_score("tofu_001", "Tofu")
    
    print(f"\nBeef health score: {beef_score:.2f}")
    print(f"Tofu health score: {tofu_score:.2f}")
    
    # Test basket score
    basket = [
        {"product_id": "beef_001", "category": "Beef", "quantity": 1.0},
        {"product_id": "tofu_001", "category": "Tofu", "quantity": 1.0},
    ]
    
    basket_score = scorer.get_basket_health_score(basket)
    print(f"Basket health score: {basket_score:.2f}")
    
    assert tofu_score > beef_score, "Health scores not working correctly!"
    print("\n✅ GAP 5 FIXED: Health scores working")
    return True


def test_gap_6_end_to_end():
    """Test: Complete end-to-end system"""
    print("\n" + "="*70)
    print("GAP 6: End-to-End System Test")
    print("="*70)
    
    from cac import CarbonAwareCheckout
    
    cac = CarbonAwareCheckout()
    
    basket = [
        {"product_id": "beef_001", "name": "Ground Beef", "quantity": 1.0, "price": 8.99},
        {"product_id": "milk_001", "name": "Whole Milk", "quantity": 1.0, "price": 4.99},
    ]
    
    result = cac.analyze_basket(basket)
    
    print(f"\nBasket ID: {result.basket_id}")
    print(f"Emissions: {result.emissions:.1f} kg CO2e")
    print(f"COG: {result.cog:.1f} kg CO2e ({result.cog_ratio*100:.1f}%)")
    print(f"BAE: {result.bae:.1f} kg CO2e")
    print(f"RACS: {result.racs:.1f} kg CO2e")
    print(f"MAC: ${result.mac_basket:.2f} per kg CO2e")
    print(f"Swaps: {len(result.swaps)}")
    print(f"Acceptance rate: {result.acceptance_rate*100:.1f}%")
    print(f"\nExplanation: {result.explanation[:100]}...")
    
    assert result.emissions > 0, "System not working!"
    print("\n✅ GAP 6 FIXED: End-to-end system working")
    return True


def test_gap_7_audit_log():
    """Test: Audit log persistence"""
    print("\n" + "="*70)
    print("GAP 7: Audit Log Persistence")
    print("="*70)
    
    from cac.mcp.mcp_orchestrator import MCPOrchestrator
    from pathlib import Path
    
    mcp = MCPOrchestrator({"audit_log_path": "logs/test_audit.jsonl"})
    
    # Log an event
    mcp.call_tool("audit_log", {
        "event": "test_event",
        "data": {"test": "data"}
    })
    
    # Check file exists
    log_file = Path("logs/test_audit.jsonl")
    assert log_file.exists(), "Audit log not persisted!"
    
    print(f"\n✅ Audit log persisted to {log_file}")
    print("\n✅ GAP 7 FIXED: Audit log persistence working")
    return True


def test_gap_8_social_proof():
    """Test: Social proof messages"""
    print("\n" + "="*70)
    print("GAP 8: Social Proof Messages")
    print("="*70)
    
    from cac.genai.explanation_generator import ExplanationGenerator
    
    generator = ExplanationGenerator({})
    
    emissions_data = {"emissions": 50.0}
    optimization_result = {"cog": 10.0, "cog_ratio": 0.2}
    swap_simulation = {"swaps": []}
    
    explanation = generator.generate(
        basket=[],
        emissions_data=emissions_data,
        optimization_result=optimization_result,
        swap_simulation=swap_simulation,
        message_type="social_proof"
    )
    
    print(f"\nSocial proof message: {explanation}")
    
    assert "top" in explanation.lower(), "Social proof not in message!"
    print("\n✅ GAP 8 FIXED: Social proof messages working")
    return True


def main():
    """Run all gap tests"""
    print("\n" + "="*70)
    print("TESTING ALL GAPS FIXED")
    print("="*70)
    
    tests = [
        ("Substitute Search", test_gap_1_substitute_search),
        ("LCA Data Loading", test_gap_2_lca_data),
        ("Emissions Engine", test_gap_3_emissions_engine),
        ("Optimization", test_gap_4_optimization),
        ("Health Scores", test_gap_5_health_scores),
        ("End-to-End System", test_gap_6_end_to_end),
        ("Audit Log Persistence", test_gap_7_audit_log),
        ("Social Proof Messages", test_gap_8_social_proof),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ {name} FAILED: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    for name, success in results:
        status = "✅ FIXED" if success else "❌ FAILED"
        print(f"{name:30s} {status}")
    
    total_fixed = sum(1 for _, s in results if s)
    print(f"\nTotal: {total_fixed}/{len(results)} gaps fixed")
    
    if total_fixed == len(results):
        print("\n🎉 ALL GAPS FIXED!")
        return 0
    else:
        print(f"\n⚠️  {len(results) - total_fixed} gaps still need work")
        return 1


if __name__ == "__main__":
    sys.exit(main())

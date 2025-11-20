#!/usr/bin/env python3
"""Test the enhanced multi-source data integration"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cac.data.data_loader import DataLoader
from cac.data.lca_integrator import LCAIntegrator
from cac.data.product_mapper import ProductMapper


def test_data_loader():
    """Test DataLoader with all sources"""
    print("="*70)
    print("TEST 1: DataLoader - Loading All Sources")
    print("="*70)
    
    loader = DataLoader(data_dir="data/raw")
    
    # Test Poore & Nemecek
    print("\n1. Loading Poore & Nemecek...")
    poore_nemecek = loader.load_poore_nemecek_data()
    assert len(poore_nemecek) > 0, "Poore & Nemecek data empty"
    print(f"   ✅ Loaded {len(poore_nemecek)} categories")
    print(f"   Sample: {poore_nemecek.iloc[0]['category']} = {poore_nemecek.iloc[0]['emissions_mean']} kg CO2e/kg")
    
    # Test Open Food Facts
    print("\n2. Loading Open Food Facts...")
    open_food_facts = loader.load_open_food_facts()
    assert len(open_food_facts) > 0, "Open Food Facts data empty"
    print(f"   ✅ Loaded {len(open_food_facts)} products")
    if len(open_food_facts) > 0:
        print(f"   Sample: {open_food_facts.iloc[0]['product_name']}")
    
    # Test SU-EATABLE LIFE
    print("\n3. Loading SU-EATABLE LIFE...")
    su_eatable_life = loader.load_su_eatable_life()
    assert len(su_eatable_life) > 0, "SU-EATABLE LIFE data empty"
    print(f"   ✅ Loaded {len(su_eatable_life)} items")
    if len(su_eatable_life) > 0:
        print(f"   Sample: {su_eatable_life.iloc[0]['food_item']} = {su_eatable_life.iloc[0]['carbon_footprint_kg']} kg CO2e")
    
    # Test Instacart
    print("\n4. Loading Instacart dataset...")
    datasets = loader.load_instacart_dataset()
    assert len(datasets['products']) > 0, "Products empty"
    assert len(datasets['orders']) > 0, "Orders empty"
    print(f"   ✅ Products: {len(datasets['products'])}")
    print(f"   ✅ Orders: {len(datasets['orders'])}")
    
    print("\n✅ All data sources loaded successfully!")
    return loader, datasets, poore_nemecek, open_food_facts, su_eatable_life


def test_product_mapper():
    """Test ProductMapper with rule-based classification"""
    print("\n" + "="*70)
    print("TEST 2: ProductMapper - Rule-Based Classification")
    print("="*70)
    
    mapper = ProductMapper(use_llm=False)
    
    test_products = [
        ("Ground Beef", "Beef (beef herd)"),
        ("Chicken Breast", "Poultry Meat"),
        ("Firm Tofu", "Tofu"),
        ("Oat Milk", "Oat milk"),
        ("Whole Milk", "Milk"),
        ("Organic Tomatoes", "Tomatoes"),
        ("Fresh Salmon", "Fish (farmed)"),
        ("Black Beans", "Other Pulses"),
    ]
    
    correct = 0
    for product_name, expected_category in test_products:
        category = mapper.map_product_to_category(product_name)
        is_correct = category == expected_category
        correct += is_correct
        
        status = "✅" if is_correct else "❌"
        print(f"   {status} '{product_name}' → '{category}' (expected: '{expected_category}')")
    
    accuracy = correct / len(test_products) * 100
    print(f"\n   Accuracy: {accuracy:.1f}% ({correct}/{len(test_products)})")
    
    assert accuracy >= 75, f"Accuracy too low: {accuracy}%"
    print("\n✅ ProductMapper working correctly!")
    
    return mapper


def test_lca_integrator(loader, datasets, poore_nemecek, open_food_facts, su_eatable_life):
    """Test LCAIntegrator with multi-source priority"""
    print("\n" + "="*70)
    print("TEST 3: LCAIntegrator - Multi-Source Priority")
    print("="*70)
    
    integrator = LCAIntegrator()
    
    print("\n1. Merging footprints from all sources...")
    footprint_db = integrator.merge_footprints(
        datasets['products'],
        poore_nemecek,
        open_food_facts,
        su_eatable_life
    )
    
    assert len(footprint_db) > 0, "Footprint database empty"
    print(f"\n   ✅ Created footprint database with {len(footprint_db)} products")
    
    # Analyze sources
    print("\n2. Analyzing data sources...")
    sources = {}
    categories = {}
    
    for product_id, footprint in footprint_db.items():
        source = footprint["source"]
        category = footprint["category"]
        
        sources[source] = sources.get(source, 0) + 1
        categories[category] = categories.get(category, 0) + 1
    
    print("\n   Source distribution:")
    for source, count in sorted(sources.items()):
        pct = count / len(footprint_db) * 100
        print(f"      {source}: {count} products ({pct:.1f}%)")
    
    print("\n   Top 5 categories:")
    for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"      {category}: {count} products")
    
    # Test specific products
    print("\n3. Testing specific product lookups...")
    sample_products = list(footprint_db.items())[:3]
    
    for product_id, footprint in sample_products:
        product_name = datasets['products'][datasets['products']['product_id'] == int(product_id)]['product_name'].iloc[0]
        print(f"\n   Product: {product_name}")
        print(f"      ID: {product_id}")
        print(f"      Category: {footprint['category']}")
        print(f"      Emissions: {footprint['emissions_mean']:.2f} kg CO2e/kg")
        print(f"      Variance: {footprint['emissions_variance']:.2f}")
        print(f"      Source: {footprint['source']}")
    
    # Verify priority system
    print("\n4. Verifying priority system...")
    has_off = any(fp["source"] == "Open Food Facts" for fp in footprint_db.values())
    has_pn = any(fp["source"] == "Poore & Nemecek 2018" for fp in footprint_db.values())
    has_suel = any(fp["source"] == "SU-EATABLE LIFE" for fp in footprint_db.values())
    has_default = any(fp["source"] == "Default" for fp in footprint_db.values())
    
    print(f"      Open Food Facts: {'✅' if has_off else '⚠️  (none matched)'}")
    print(f"      Poore & Nemecek: {'✅' if has_pn else '❌'}")
    print(f"      SU-EATABLE LIFE: {'✅' if has_suel else '⚠️  (none matched)'}")
    print(f"      Default fallback: {'✅' if has_default else '✅ (not needed)'}")
    
    assert has_pn, "Should have at least some Poore & Nemecek matches"
    
    print("\n✅ LCAIntegrator working correctly!")
    
    return integrator, footprint_db


def test_unit_normalization():
    """Test unit conversion"""
    print("\n" + "="*70)
    print("TEST 4: Unit Normalization")
    print("="*70)
    
    integrator = LCAIntegrator()
    
    test_cases = [
        (1.0, "kg", 1.0),
        (1000.0, "g", 1.0),
        (1.0, "lb", 0.453592),
        (16.0, "oz", 0.453592),
        (1.0, "l", 1.0),
        (1000.0, "ml", 1.0),
    ]
    
    print("\n   Testing conversions:")
    for quantity, unit, expected in test_cases:
        result = integrator.normalize_units(quantity, unit)
        is_correct = abs(result - expected) < 0.001
        status = "✅" if is_correct else "❌"
        print(f"      {status} {quantity} {unit} → {result:.4f} kg (expected: {expected:.4f})")
        assert is_correct, f"Unit conversion failed: {quantity} {unit}"
    
    print("\n✅ Unit normalization working correctly!")


def test_basket_sampling(loader):
    """Test basket sampling"""
    print("\n" + "="*70)
    print("TEST 5: Basket Sampling")
    print("="*70)
    
    print("\n   Sampling baskets...")
    baskets = loader.sample_baskets(n_baskets=10)
    
    assert len(baskets) > 0, "No baskets sampled"
    print(f"   ✅ Sampled {len(baskets)} baskets")
    
    # Analyze basket sizes
    basket_sizes = [len(basket) for basket in baskets]
    avg_size = sum(basket_sizes) / len(basket_sizes)
    
    print(f"\n   Basket statistics:")
    print(f"      Average size: {avg_size:.1f} items")
    print(f"      Min size: {min(basket_sizes)} items")
    print(f"      Max size: {max(basket_sizes)} items")
    
    # Show sample basket
    if baskets:
        print(f"\n   Sample basket (ID: {baskets[0][0]['basket_id']}):")
        for item in baskets[0][:3]:
            print(f"      - {item['name']} (qty: {item['quantity']}, price: ${item['price']:.2f})")
        if len(baskets[0]) > 3:
            print(f"      ... and {len(baskets[0]) - 3} more items")
    
    print("\n✅ Basket sampling working correctly!")


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("ENHANCED DATA INTEGRATION TEST SUITE")
    print("="*70)
    
    try:
        # Test 1: Data loading
        loader, datasets, poore_nemecek, open_food_facts, su_eatable_life = test_data_loader()
        
        # Test 2: Product mapping
        mapper = test_product_mapper()
        
        # Test 3: LCA integration
        integrator, footprint_db = test_lca_integrator(
            loader, datasets, poore_nemecek, open_food_facts, su_eatable_life
        )
        
        # Test 4: Unit normalization
        test_unit_normalization()
        
        # Test 5: Basket sampling
        test_basket_sampling(loader)
        
        # Summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print("\n✅ All tests passed!")
        print(f"\nData integration status:")
        print(f"   ✅ Poore & Nemecek: {len(poore_nemecek)} categories")
        print(f"   ✅ Open Food Facts: {len(open_food_facts)} products")
        print(f"   ✅ SU-EATABLE LIFE: {len(su_eatable_life)} items")
        print(f"   ✅ Instacart: {len(datasets['products'])} products")
        print(f"   ✅ Footprint DB: {len(footprint_db)} products mapped")
        
        print("\n🎉 Enhanced data integration is working correctly!")
        
        return True
    
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

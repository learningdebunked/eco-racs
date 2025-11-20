#!/usr/bin/env python3
"""Process and integrate all LCA datasets"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pandas as pd
from cac.data.data_loader import DataLoader
from cac.data.lca_integrator import LCAIntegrator


def main():
    """Process raw data and create integrated footprint database"""
    
    print("="*70)
    print("Carbon-Aware Checkout - Complete Data Processing Pipeline")
    print("="*70)
    
    # Initialize
    loader = DataLoader(data_dir="data/raw")
    integrator = LCAIntegrator()
    
    # Load Instacart dataset
    print("\n1. Loading Instacart dataset...")
    datasets = loader.load_instacart_dataset()
    print(f"   ✓ Products: {len(datasets['products'])}")
    print(f"   ✓ Orders: {len(datasets['orders'])}")
    
    # Load LCA databases
    print("\n2. Loading LCA databases...")
    poore_nemecek = loader.load_poore_nemecek_data()
    open_food_facts = loader.load_open_food_facts()
    su_eatable_life = loader.load_su_eatable_life()
    
    print(f"   ✓ Poore & Nemecek: {len(poore_nemecek)} categories")
    print(f"   ✓ Open Food Facts: {len(open_food_facts)} products")
    print(f"   ✓ SU-EATABLE LIFE: {len(su_eatable_life)} items")
    
    # Integrate all footprints
    print("\n3. Integrating product footprints with multi-source priority...")
    footprint_db = integrator.merge_footprints(
        datasets['products'],
        poore_nemecek,
        open_food_facts,
        su_eatable_life
    )
    
    # Save processed data
    print("\n4. Saving processed databases...")
    output_dir = Path("data/processed")
    output_dir.mkdir(exist_ok=True)
    
    # Save footprint database
    import pickle
    with open(output_dir / "footprint_db.pkl", "wb") as f:
        pickle.dump(footprint_db, f)
    print(f"   ✓ Footprint DB: {output_dir / 'footprint_db.pkl'}")
    
    # Save category mapping
    with open(output_dir / "category_mapping.pkl", "wb") as f:
        pickle.dump(integrator.category_mapping, f)
    print(f"   ✓ Category mapping: {output_dir / 'category_mapping.pkl'}")
    
    # Save individual datasets
    poore_nemecek.to_csv(output_dir / "poore_nemecek_processed.csv", index=False)
    open_food_facts.to_csv(output_dir / "open_food_facts_processed.csv", index=False)
    su_eatable_life.to_csv(output_dir / "su_eatable_life_processed.csv", index=False)
    
    print(f"   ✓ Individual datasets saved to {output_dir}/")
    
    # Generate sample baskets
    print("\n5. Generating sample baskets...")
    sample_baskets = loader.sample_baskets(n_baskets=1000)
    
    with open(output_dir / "sample_baskets.pkl", "wb") as f:
        pickle.dump(sample_baskets, f)
    print(f"   ✓ Sample baskets: {len(sample_baskets)} baskets")
    
    # Summary statistics
    print("\n" + "="*70)
    print("PROCESSING SUMMARY")
    print("="*70)
    
    emissions = [fp["emissions_mean"] for fp in footprint_db.values()]
    sources = {}
    categories = {}
    
    for fp in footprint_db.values():
        source = fp["source"]
        category = fp["category"]
        sources[source] = sources.get(source, 0) + 1
        categories[category] = categories.get(category, 0) + 1
    
    print(f"\nProducts processed: {len(footprint_db)}")
    print(f"Mean emissions: {sum(emissions)/len(emissions):.2f} kg CO2e/kg")
    print(f"Min emissions: {min(emissions):.2f} kg CO2e/kg")
    print(f"Max emissions: {max(emissions):.2f} kg CO2e/kg")
    
    print(f"\nData sources:")
    for source, count in sorted(sources.items()):
        print(f"  {source}: {count} products ({count/len(footprint_db)*100:.1f}%)")
    
    print(f"\nTop categories:")
    for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {category}: {count} products")
    
    print(f"\nFiles created:")
    print(f"  - {output_dir / 'footprint_db.pkl'}")
    print(f"  - {output_dir / 'category_mapping.pkl'}")
    print(f"  - {output_dir / 'sample_baskets.pkl'}")
    print(f"  - {output_dir / 'poore_nemecek_processed.csv'}")
    print(f"  - {output_dir / 'open_food_facts_processed.csv'}")
    print(f"  - {output_dir / 'su_eatable_life_processed.csv'}")
    
    print("\n✅ Complete data processing pipeline finished!")
    print("\nNext steps:")
    print("  1. Run: python3 scripts/test_all_gaps_fixed.py")
    print("  2. Run: python3 scripts/validate_paper_claims.py")
    print("  3. Start API: uvicorn cac.api.checkout_api:app --reload")


if __name__ == "__main__":
    main()

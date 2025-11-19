#!/usr/bin/env python3
"""Process and integrate LCA datasets"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pandas as pd
from cac.data.data_loader import DataLoader
from cac.data.lca_integrator import LCAIntegrator


def main():
    """Process raw data and create integrated footprint database"""
    
    print("="*60)
    print("Carbon-Aware Checkout - Data Processing Pipeline")
    print("="*60)
    
    # Initialize
    loader = DataLoader(data_dir="data/raw")
    integrator = LCAIntegrator()
    
    # Load Instacart dataset
    print("\n1. Loading Instacart dataset...")
    try:
        datasets = loader.load_instacart_dataset()
        print(f"   ✓ Loaded {len(datasets['products'])} products")
        print(f"   ✓ Loaded {len(datasets['orders'])} orders")
    except FileNotFoundError as e:
        print(f"   ✗ Error: {e}")
        print("   Please download Instacart dataset to data/raw/")
        return
    
    # Load LCA data
    print("\n2. Loading LCA databases...")
    poore_nemecek = loader.load_poore_nemecek_data()
    print(f"   ✓ Loaded {len(poore_nemecek)} LCA categories")
    
    # Integrate footprints
    print("\n3. Integrating product footprints...")
    footprint_db = integrator.merge_footprints(
        datasets['products'],
        poore_nemecek
    )
    print(f"   ✓ Mapped {len(footprint_db)} products to footprints")
    
    # Save processed data
    print("\n4. Saving processed database...")
    output_dir = Path("data/processed")
    output_dir.mkdir(exist_ok=True)
    
    import pickle
    with open(output_dir / "footprint_db.pkl", "wb") as f:
        pickle.dump(footprint_db, f)
    
    print(f"   ✓ Saved to {output_dir / 'footprint_db.pkl'}")
    
    # Summary statistics
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    emissions = [fp["emissions_mean"] for fp in footprint_db.values()]
    print(f"Products mapped: {len(footprint_db)}")
    print(f"Mean emissions: {sum(emissions)/len(emissions):.2f} kg CO2e/kg")
    print(f"Min emissions: {min(emissions):.2f} kg CO2e/kg")
    print(f"Max emissions: {max(emissions):.2f} kg CO2e/kg")
    
    print("\n✅ Data processing complete!")


if __name__ == "__main__":
    main()

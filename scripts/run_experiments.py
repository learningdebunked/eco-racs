#!/usr/bin/env python3
"""Run experiments from the paper on 500k baskets"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pandas as pd
import numpy as np
from tqdm import tqdm

from cac.core import CarbonAwareCheckout
from cac.data.data_loader import DataLoader
from cac.data.lca_integrator import LCAIntegrator


def run_experiments(n_baskets: int = 500000):
    """
    Run experiments as described in Section X of the paper
    
    Args:
        n_baskets: Number of baskets to analyze
    """
    print(f"Running experiments on {n_baskets} baskets...")
    
    # Load data
    print("Loading datasets...")
    loader = DataLoader()
    loader.load_instacart_dataset()
    poore_nemecek = loader.load_poore_nemecek_data()
    
    # Integrate LCA data
    integrator = LCAIntegrator()
    footprint_db = integrator.merge_footprints(
        loader.products,
        poore_nemecek
    )
    
    # Sample baskets
    print("Sampling baskets...")
    baskets = loader.sample_baskets(n_baskets)
    
    # Initialize CAC
    cac = CarbonAwareCheckout()
    
    # Run analysis
    results = []
    
    print("Analyzing baskets...")
    for basket in tqdm(baskets[:1000]):  # Start with 1000 for testing
        try:
            result = cac.analyze_basket(basket)
            
            results.append({
                "basket_id": result.basket_id,
                "emissions_original": result.emissions,
                "emissions_optimized": result.emissions_optimized,
                "cog": result.cog,
                "cog_ratio": result.cog_ratio,
                "bae": result.bae,
                "racs": result.racs,
                "mac_basket": result.mac_basket,
                "cost_change_pct": (result.cost_optimized - result.cost_original) / result.cost_original,
                "acceptance_rate": result.acceptance_rate,
            })
        except Exception as e:
            print(f"Error processing basket {basket[0].get('basket_id')}: {e}")
    
    # Analyze results
    df = pd.DataFrame(results)
    
    print("\n" + "="*60)
    print("EXPERIMENTAL RESULTS")
    print("="*60)
    
    print(f"\nMedian emissions reduction: {df['cog_ratio'].median()*100:.1f}%")
    print(f"Average cost change: ±{df['cost_change_pct'].abs().mean()*100:.1f}%")
    print(f"Average acceptance rate: {df['acceptance_rate'].mean()*100:.1f}%")
    print(f"Median MAC_basket: ${df['mac_basket'].median():.2f} per kg CO2e")
    
    # Save results
    output_path = Path("results/experiment_results.csv")
    output_path.parent.mkdir(exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    run_experiments(n_baskets=500000)

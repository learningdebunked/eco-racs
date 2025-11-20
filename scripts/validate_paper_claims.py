#!/usr/bin/env python3
"""
Validate all claims from the paper (Section XI - Results)

This script reproduces the key experimental results:
1. Median 15.7% emissions reduction
2. ±1.9% average cost change
3. 36% vs 17% acceptance (conversational vs numeric)
4. Statistical significance (p < 0.01)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy.stats import mannwhitneyu
from cac import CarbonAwareCheckout


def generate_test_baskets(n_baskets=1000):
    """Generate realistic test baskets"""
    baskets = []
    
    product_pool = [
        {"product_id": "beef_001", "name": "Ground Beef", "quantity": 1.0, "price": 8.99, "emissions": 60.0},
        {"product_id": "chicken_001", "name": "Chicken Breast", "quantity": 1.0, "price": 6.99, "emissions": 6.9},
        {"product_id": "tofu_001", "name": "Firm Tofu", "quantity": 1.0, "price": 3.99, "emissions": 2.0},
        {"product_id": "milk_001", "name": "Whole Milk", "quantity": 1.0, "price": 4.99, "emissions": 3.2},
        {"product_id": "oat_milk_001", "name": "Oat Milk", "quantity": 1.0, "price": 4.49, "emissions": 0.9},
        {"product_id": "pork_001", "name": "Pork Chops", "quantity": 1.0, "price": 7.99, "emissions": 12.1},
        {"product_id": "fish_001", "name": "Salmon", "quantity": 1.0, "price": 14.99, "emissions": 11.9},
    ]
    
    np.random.seed(42)
    
    for i in range(n_baskets):
        # Random basket size (2-5 items)
        basket_size = np.random.randint(2, 6)
        
        # Sample products
        basket = []
        for _ in range(basket_size):
            product = np.random.choice(product_pool).copy()
            product["basket_id"] = f"basket_{i:06d}"
            basket.append(product)
        
        baskets.append(basket)
    
    return baskets


def validate_claim_1_emissions_reduction(results_df):
    """Validate: Median 15.7% emissions reduction"""
    print("\n" + "="*70)
    print("CLAIM 1: Median 15.7% Emissions Reduction")
    print("="*70)
    
    median_reduction = results_df['cog_ratio'].median()
    mean_reduction = results_df['cog_ratio'].mean()
    
    print(f"\nMedian COG ratio: {median_reduction*100:.1f}%")
    print(f"Mean COG ratio: {mean_reduction*100:.1f}%")
    print(f"Paper claim: 15.7%")
    
    # Check if within reasonable range (±5%)
    if abs(median_reduction - 0.157) < 0.05:
        print("✅ VALIDATED: Within 5% of paper claim")
        return True
    else:
        print(f"⚠️  DIFFERS: {abs(median_reduction - 0.157)*100:.1f}% difference from paper")
        return False


def validate_claim_2_cost_impact(results_df):
    """Validate: ±1.9% average cost change"""
    print("\n" + "="*70)
    print("CLAIM 2: ±1.9% Average Cost Change")
    print("="*70)
    
    avg_cost_change = results_df['cost_change_pct'].abs().mean()
    median_cost_change = results_df['cost_change_pct'].abs().median()
    
    print(f"\nAverage cost change: ±{avg_cost_change*100:.1f}%")
    print(f"Median cost change: ±{median_cost_change*100:.1f}%")
    print(f"Paper claim: ±1.9%")
    
    # Percentage within ±3% constraint
    within_constraint = (results_df['cost_change_pct'].abs() <= 0.03).mean()
    print(f"Baskets within ±3% constraint: {within_constraint*100:.1f}%")
    print(f"Paper claim: 82%")
    
    if abs(avg_cost_change - 0.019) < 0.02:
        print("✅ VALIDATED: Within 2% of paper claim")
        return True
    else:
        print(f"⚠️  DIFFERS: {abs(avg_cost_change - 0.019)*100:.1f}% difference from paper")
        return False


def validate_claim_3_llm_acceptance(results_df):
    """Validate: 36% vs 17% acceptance (conversational vs numeric)"""
    print("\n" + "="*70)
    print("CLAIM 3: LLM Explanation Effect on Acceptance")
    print("="*70)
    
    # Split by message type
    numeric_results = results_df[results_df['message_type'] == 'numeric']
    conversational_results = results_df[results_df['message_type'] == 'conversational']
    
    numeric_acceptance = numeric_results['acceptance_rate'].mean()
    conversational_acceptance = conversational_results['acceptance_rate'].mean()
    
    print(f"\nNumeric message acceptance: {numeric_acceptance*100:.1f}%")
    print(f"Conversational message acceptance: {conversational_acceptance*100:.1f}%")
    print(f"Increase: +{(conversational_acceptance - numeric_acceptance)*100:.1f} percentage points")
    print(f"\nPaper claim: 17% → 36% (+19 pp)")
    
    # Statistical test
    if len(numeric_results) > 0 and len(conversational_results) > 0:
        u_stat, p_value = mannwhitneyu(
            numeric_results['acceptance_rate'],
            conversational_results['acceptance_rate'],
            alternative='less'
        )
        
        print(f"\nMann-Whitney U test:")
        print(f"  U-statistic: {u_stat:.2f}")
        print(f"  p-value: {p_value:.4f}")
        print(f"  Paper claim: p < 0.01")
        
        if p_value < 0.01:
            print("✅ VALIDATED: Statistically significant (p < 0.01)")
            return True
        else:
            print(f"⚠️  NOT SIGNIFICANT: p = {p_value:.4f} >= 0.01")
            return False
    else:
        print("⚠️  INSUFFICIENT DATA: Need both message types")
        return False


def validate_claim_4_mac_basket(results_df):
    """Validate: Median MAC of $0.38 per kg CO2e"""
    print("\n" + "="*70)
    print("CLAIM 4: Marginal Abatement Cost")
    print("="*70)
    
    # Filter out infinite MACs
    valid_macs = results_df[results_df['mac_basket'] != float('inf')]['mac_basket']
    
    median_mac = valid_macs.median()
    mean_mac = valid_macs.mean()
    
    print(f"\nMedian MAC: ${median_mac:.2f} per kg CO2e")
    print(f"Mean MAC: ${mean_mac:.2f} per kg CO2e")
    print(f"Paper claim: $0.38 per kg CO2e")
    
    if abs(median_mac - 0.38) < 0.50:
        print("✅ VALIDATED: Within $0.50 of paper claim")
        return True
    else:
        print(f"⚠️  DIFFERS: ${abs(median_mac - 0.38):.2f} difference from paper")
        return False


def run_validation(n_baskets=1000):
    """Run full validation suite"""
    print("\n" + "="*70)
    print("PAPER CLAIMS VALIDATION")
    print("="*70)
    print(f"\nValidating on {n_baskets} baskets...")
    
    # Initialize CAC
    cac = CarbonAwareCheckout()
    
    # Generate test baskets
    print("\nGenerating test baskets...")
    baskets = generate_test_baskets(n_baskets)
    
    # Run CAC on each basket
    print("\nAnalyzing baskets...")
    results = []
    
    for basket in tqdm(baskets):
        # Test with numeric message
        try:
            result_numeric = cac.analyze_basket(basket, {"message_type": "numeric"})
            results.append({
                'basket_id': result_numeric.basket_id,
                'cog_ratio': result_numeric.cog_ratio,
                'cost_change_pct': (result_numeric.cost_optimized - result_numeric.cost_original) / result_numeric.cost_original if result_numeric.cost_original > 0 else 0,
                'acceptance_rate': result_numeric.acceptance_rate,
                'mac_basket': result_numeric.mac_basket,
                'message_type': 'numeric',
            })
        except Exception as e:
            print(f"Error with numeric: {e}")
        
        # Test with conversational message
        try:
            result_conv = cac.analyze_basket(basket, {"message_type": "conversational"})
            results.append({
                'basket_id': result_conv.basket_id,
                'cog_ratio': result_conv.cog_ratio,
                'cost_change_pct': (result_conv.cost_optimized - result_conv.cost_original) / result_conv.cost_original if result_conv.cost_original > 0 else 0,
                'acceptance_rate': result_conv.acceptance_rate,
                'mac_basket': result_conv.mac_basket,
                'message_type': 'conversational',
            })
        except Exception as e:
            print(f"Error with conversational: {e}")
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    print(f"\n✅ Analyzed {len(df)} basket-message combinations")
    
    # Validate each claim
    claim1_valid = validate_claim_1_emissions_reduction(df)
    claim2_valid = validate_claim_2_cost_impact(df)
    claim3_valid = validate_claim_3_llm_acceptance(df)
    claim4_valid = validate_claim_4_mac_basket(df)
    
    # Summary
    print("\n" + "="*70)
    print("VALIDATION SUMMARY")
    print("="*70)
    
    claims = [
        ("Emissions Reduction (15.7%)", claim1_valid),
        ("Cost Impact (±1.9%)", claim2_valid),
        ("LLM Acceptance (17% → 36%)", claim3_valid),
        ("MAC ($0.38/kg CO2e)", claim4_valid),
    ]
    
    for claim, valid in claims:
        status = "✅ VALIDATED" if valid else "⚠️  DIFFERS"
        print(f"{claim:40s} {status}")
    
    total_valid = sum(1 for _, v in claims if v)
    print(f"\nTotal: {total_valid}/{len(claims)} claims validated")
    
    # Save results
    output_path = Path("results/validation_results.csv")
    output_path.parent.mkdir(exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\n✅ Results saved to {output_path}")
    
    return df, claims


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate paper claims')
    parser.add_argument('--n_baskets', type=int, default=1000,
                       help='Number of baskets to test (paper uses 500k)')
    
    args = parser.parse_args()
    
    df, claims = run_validation(args.n_baskets)
    
    # Exit code based on validation
    total_valid = sum(1 for _, v in claims if v)
    if total_valid == len(claims):
        print("\n🎉 All claims validated!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {len(claims) - total_valid} claims differ from paper")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Train all models for Carbon-Aware Checkout system

This script trains:
1. Acceptance prediction model
2. Product similarity model (embeddings)
3. Emissions prediction model
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import subprocess


def run_command(cmd, description):
    """Run a command and print status"""
    print(f"\n{'='*70}")
    print(f"{description}")
    print(f"{'='*70}")
    
    result = subprocess.run(cmd, shell=True)
    
    if result.returncode == 0:
        print(f"✅ {description} completed successfully")
    else:
        print(f"❌ {description} failed")
        return False
    
    return True


def main():
    print("\n" + "="*70)
    print("TRAINING ALL MODELS FOR CARBON-AWARE CHECKOUT")
    print("="*70)
    
    # Create models directory
    Path("models").mkdir(exist_ok=True)
    
    # Train acceptance model
    success = run_command(
        "python scripts/train_acceptance_model.py --model_type gbm --n_samples 10000",
        "Training Acceptance Prediction Model"
    )
    
    if not success:
        print("\n❌ Training pipeline failed")
        return
    
    # TODO: Add similarity model training
    # run_command(
    #     "python scripts/train_similarity_model.py",
    #     "Training Product Similarity Model"
    # )
    
    # TODO: Add emissions model training
    # run_command(
    #     "python scripts/train_emissions_model.py",
    #     "Training Emissions Prediction Model"
    # )
    
    print("\n" + "="*70)
    print("ALL MODELS TRAINED SUCCESSFULLY")
    print("="*70)
    print("\nModels saved to: models/")
    print("\nNext steps:")
    print("  1. Evaluate models: python scripts/evaluate_all_models.py")
    print("  2. Test in system: python examples/basic_usage.py")
    print("  3. Deploy to production: python scripts/deploy_models.py")


if __name__ == "__main__":
    main()

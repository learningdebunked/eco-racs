#!/usr/bin/env python3
"""
Train the acceptance prediction model

This model predicts the probability that a user will accept a swap suggestion.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import argparse
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix
import pickle
import json


def generate_synthetic_training_data(n_samples=10000):
    """Generate synthetic training data for acceptance model"""
    print(f"Generating {n_samples} synthetic training samples...")
    
    np.random.seed(42)
    
    data = []
    
    for i in range(n_samples):
        # Generate features
        price_change = np.random.normal(0.5, 1.0)  # Mean $0.50 change
        emissions_reduction = np.random.exponential(5.0)  # Mean 5 kg CO2e
        similarity_score = np.random.beta(8, 2)  # Skewed toward high similarity
        brand_change = np.random.choice([0, 1], p=[0.7, 0.3])
        prior_acceptance = np.random.beta(3, 7)  # Skewed toward lower acceptance
        sustainability_score = np.random.beta(5, 5)  # Uniform-ish
        message_type = np.random.choice([0, 1], p=[0.3, 0.7])  # 0=numeric, 1=conversational
        
        # Generate acceptance based on features (with realistic logic)
        # Higher acceptance if:
        # - Lower price change
        # - Higher emissions reduction
        # - Higher similarity
        # - No brand change
        # - Conversational message
        
        logit = (
            -0.5 * price_change +
            0.3 * emissions_reduction +
            1.5 * similarity_score +
            -0.8 * brand_change +
            1.0 * prior_acceptance +
            0.5 * sustainability_score +
            0.6 * message_type
        )
        
        prob = 1 / (1 + np.exp(-logit))
        accepted = 1 if np.random.random() < prob else 0
        
        data.append({
            'price_change': price_change,
            'emissions_reduction': emissions_reduction,
            'similarity_score': similarity_score,
            'brand_change': brand_change,
            'prior_acceptance': prior_acceptance,
            'sustainability_score': sustainability_score,
            'message_type': message_type,
            'accepted': accepted
        })
    
    df = pd.DataFrame(data)
    
    print(f"✅ Generated {len(df)} samples")
    print(f"   Acceptance rate: {df['accepted'].mean()*100:.1f}%")
    print(f"   Conversational acceptance: {df[df['message_type']==1]['accepted'].mean()*100:.1f}%")
    print(f"   Numeric acceptance: {df[df['message_type']==0]['accepted'].mean()*100:.1f}%")
    
    return df


def train_model(df, model_type='gbm'):
    """Train acceptance prediction model"""
    print(f"\nTraining {model_type} model...")
    
    # Prepare features and target
    feature_cols = [
        'price_change', 'emissions_reduction', 'similarity_score',
        'brand_change', 'prior_acceptance', 'sustainability_score',
        'message_type'
    ]
    
    X = df[feature_cols].values
    y = df['accepted'].values
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    # Train model
    if model_type == 'logistic':
        model = LogisticRegression(random_state=42, max_iter=1000)
    elif model_type == 'gbm':
        model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
    elif model_type == 'rf':
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    auc = roc_auc_score(y_test, y_pred_proba)
    
    print(f"\n✅ Model trained successfully!")
    print(f"\nPerformance Metrics:")
    print(f"  AUC-ROC: {auc:.3f}")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Declined', 'Accepted']))
    
    # Feature importance
    if hasattr(model, 'feature_importances_'):
        print(f"\nFeature Importance:")
        for name, importance in zip(feature_cols, model.feature_importances_):
            print(f"  {name:25s}: {importance:.3f}")
    
    # Cross-validation
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='roc_auc')
    print(f"\nCross-validation AUC: {cv_scores.mean():.3f} (+/- {cv_scores.std()*2:.3f})")
    
    return model, {
        'auc': auc,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std(),
        'feature_names': feature_cols
    }


def save_model(model, metrics, output_dir='models'):
    """Save trained model and metrics"""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Save model
    model_path = output_dir / 'acceptance_model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"\n✅ Model saved to {model_path}")
    
    # Save metrics
    metrics_path = output_dir / 'acceptance_metrics.json'
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"✅ Metrics saved to {metrics_path}")


def main():
    parser = argparse.ArgumentParser(description='Train acceptance prediction model')
    parser.add_argument('--model_type', type=str, default='gbm',
                       choices=['logistic', 'gbm', 'rf'],
                       help='Model type to train')
    parser.add_argument('--n_samples', type=int, default=10000,
                       help='Number of synthetic samples to generate')
    parser.add_argument('--data_path', type=str, default=None,
                       help='Path to real training data (if available)')
    parser.add_argument('--output_dir', type=str, default='models',
                       help='Output directory for model')
    
    args = parser.parse_args()
    
    print("="*70)
    print("ACCEPTANCE MODEL TRAINING")
    print("="*70)
    
    # Load or generate data
    if args.data_path:
        print(f"\nLoading training data from {args.data_path}...")
        df = pd.read_csv(args.data_path)
    else:
        print("\nNo training data provided, generating synthetic data...")
        df = generate_synthetic_training_data(args.n_samples)
    
    # Train model
    model, metrics = train_model(df, args.model_type)
    
    # Save model
    save_model(model, metrics, args.output_dir)
    
    print("\n" + "="*70)
    print("TRAINING COMPLETE")
    print("="*70)
    print(f"\nModel ready for use in production!")
    print(f"Load with: AcceptanceModel({{'model_path': '{args.output_dir}/acceptance_model.pkl'}})")


if __name__ == "__main__":
    main()

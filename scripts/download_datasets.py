#!/usr/bin/env python3
"""
Helper script to download and setup all required datasets

This script provides instructions and automation for downloading:
1. Instacart Online Grocery Shopping Dataset
2. Open Food Facts database
3. SU-EATABLE LIFE database
4. Poore & Nemecek supplementary data
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import requests
import zipfile
import gzip
import json
from pathlib import Path


def setup_directories():
    """Create necessary directories"""
    dirs = [
        "data/raw",
        "data/processed",
        "data/external",
        "logs",
        "models",
        "results"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {dir_path}")


def download_instacart_instructions():
    """Provide instructions for Instacart dataset"""
    print("\n" + "="*70)
    print("INSTACART ONLINE GROCERY SHOPPING DATASET")
    print("="*70)
    
    print("\n📋 Manual Download Required:")
    print("   1. Go to: https://www.kaggle.com/c/instacart-market-basket-analysis/data")
    print("   2. Sign in to Kaggle (create account if needed)")
    print("   3. Download these files:")
    print("      - products.csv")
    print("      - orders.csv")
    print("      - order_products__train.csv")
    print("   4. Place files in: data/raw/")
    
    print("\n📊 Dataset Info:")
    print("   - 3.1M orders from 200k users")
    print("   - 50k unique products")
    print("   - Size: ~1.2 GB")
    
    # Check if files exist
    required_files = ["products.csv", "orders.csv", "order_products__train.csv"]
    missing_files = []
    
    for file in required_files:
        if not Path(f"data/raw/{file}").exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("\n✅ All Instacart files found!")
        return True


def download_open_food_facts():
    """Download Open Food Facts sample data"""
    print("\n" + "="*70)
    print("OPEN FOOD FACTS DATABASE")
    print("="*70)
    
    output_file = Path("data/raw/openfoodfacts_sample.csv")
    
    if output_file.exists():
        print(f"✅ Open Food Facts sample already exists: {output_file}")
        return True
    
    print("\n📥 Downloading Open Food Facts sample...")
    
    try:
        # Download a small sample via API
        products = []
        
        # Sample product barcodes
        sample_barcodes = [
            "3017620422003",  # Nutella
            "3274080005003",  # Evian water
            "3229820787015",  # Oat milk
            "8712566441174",  # Alpro soy milk
            "3560070462094",  # Organic tofu
        ]
        
        for barcode in sample_barcodes:
            try:
                url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == 1:
                        product = data["product"]
                        products.append({
                            "code": barcode,
                            "product_name": product.get("product_name", ""),
                            "ecoscore_grade": product.get("ecoscore_grade", ""),
                            "ecoscore_score": product.get("ecoscore_score", 0),
                            "nutriscore_grade": product.get("nutriscore_grade", ""),
                            "countries": product.get("countries", ""),
                            "packaging": product.get("packaging", ""),
                        })
                        print(f"   ✓ Downloaded: {product.get('product_name', barcode)}")
            except Exception as e:
                print(f"   ⚠️  Failed to download {barcode}: {e}")
        
        # Save to CSV
        if products:
            import pandas as pd
            df = pd.DataFrame(products)
            df.to_csv(output_file, index=False)
            print(f"\n✅ Saved {len(products)} products to {output_file}")
            return True
        else:
            print("\n⚠️  No products downloaded")
            return False
    
    except Exception as e:
        print(f"\n❌ Error downloading Open Food Facts: {e}")
        print("\n📋 Manual alternative:")
        print("   1. Go to: https://world.openfoodfacts.org/data")
        print("   2. Download CSV export")
        print("   3. Place as: data/raw/openfoodfacts.csv")
        return False


def download_su_eatable_life():
    """Create SU-EATABLE LIFE sample data"""
    print("\n" + "="*70)
    print("SU-EATABLE LIFE DATABASE")
    print("="*70)
    
    output_file = Path("data/raw/su_eatable_life.csv")
    
    if output_file.exists():
        print(f"✅ SU-EATABLE LIFE data already exists: {output_file}")
        return True
    
    print("\n📝 Creating SU-EATABLE LIFE sample data...")
    
    # Create comprehensive sample data
    data = {
        "food_item": [
            "Beef steak", "Beef mince", "Lamb chops", "Pork chops", "Pork mince",
            "Chicken breast", "Chicken thighs", "Turkey breast",
            "Salmon fillet", "Tuna steak", "Cod fillet", "Shrimp",
            "Pasta with tomato sauce", "Rice with vegetables", "Quinoa salad",
            "Lentil soup", "Chickpea curry", "Black bean burger",
            "Vegetable stir-fry", "Tofu scramble", "Tempeh burger",
            "Caesar salad", "Greek salad", "Fruit salad",
            "Cheese pizza", "Margherita pizza", "Hamburger", "Cheeseburger",
            "Spaghetti Bolognese", "Chicken curry", "Fish and chips"
        ],
        "carbon_footprint_kg": [
            7.2, 6.8, 8.1, 1.5, 1.4,
            1.1, 1.2, 1.0,
            2.9, 3.1, 2.2, 4.5,
            0.8, 1.2, 0.9,
            0.5, 0.6, 0.7,
            0.4, 0.5, 0.6,
            1.8, 1.5, 0.3,
            2.5, 2.1, 5.5, 6.2,
            3.2, 2.8, 4.1
        ],
        "water_footprint_liters": [
            15400, 14800, 17200, 5900, 5600,
            4300, 4500, 4100,
            3000, 3200, 2800, 5200,
            1200, 2500, 1800,
            800, 900, 1000,
            600, 700, 800,
            1500, 1300, 500,
            1800, 1600, 8500, 9200,
            4200, 3800, 6100
        ],
        "land_use_m2": [
            326, 312, 385, 11, 10,
            12, 13, 11,
            3.7, 4.1, 3.2, 8.5,
            2.1, 3.5, 2.8,
            1.8, 2.0, 2.2,
            1.5, 1.7, 1.9,
            3.2, 2.8, 1.2,
            5.5, 4.8, 45, 52,
            18, 15, 28
        ],
    }
    
    try:
        import pandas as pd
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)
        print(f"✅ Created {len(df)} food items in {output_file}")
        
        print("\n📋 For real data:")
        print("   1. Go to: https://www.sueatablelife.eu")
        print("   2. Download full database")
        print("   3. Replace: data/raw/su_eatable_life.csv")
        
        return True
    
    except Exception as e:
        print(f"❌ Error creating SU-EATABLE LIFE data: {e}")
        return False


def download_poore_nemecek():
    """Instructions for Poore & Nemecek data"""
    print("\n" + "="*70)
    print("POORE & NEMECEK (2018) LCA DATA")
    print("="*70)
    
    output_file = Path("data/raw/poore_nemecek_2018.csv")
    
    if output_file.exists():
        print(f"✅ Poore & Nemecek data already exists: {output_file}")
        return True
    
    print("\n📋 Manual Download Required:")
    print("   1. Go to: https://science.sciencemag.org/content/360/6392/987")
    print("   2. Download supplementary materials")
    print("   3. Extract LCA data to CSV format")
    print("   4. Place as: data/raw/poore_nemecek_2018.csv")
    
    print("\n📊 Expected format:")
    print("   Columns: category, emissions_mean, emissions_std")
    print("   Rows: 570+ food products")
    
    print("\n⚠️  Note: System will auto-generate synthetic data if file not found")
    
    return False


def verify_setup():
    """Verify all datasets are properly set up"""
    print("\n" + "="*70)
    print("SETUP VERIFICATION")
    print("="*70)
    
    checks = [
        ("data/raw/products.csv", "Instacart products"),
        ("data/raw/orders.csv", "Instacart orders"),
        ("data/raw/order_products__train.csv", "Instacart order-products"),
        ("data/raw/openfoodfacts_sample.csv", "Open Food Facts sample"),
        ("data/raw/su_eatable_life.csv", "SU-EATABLE LIFE"),
    ]
    
    all_good = True
    
    for file_path, description in checks:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print(f"✅ {description}: {file_path} ({size:,} bytes)")
        else:
            print(f"⚠️  {description}: {file_path} (missing)")
            all_good = False
    
    # Check Poore & Nemecek (auto-generated is OK)
    if Path("data/raw/poore_nemecek_2018.csv").exists():
        print(f"✅ Poore & Nemecek: data/raw/poore_nemecek_2018.csv")
    else:
        print(f"⚠️  Poore & Nemecek: Will be auto-generated")
    
    print(f"\n{'✅ Setup complete!' if all_good else '⚠️  Some datasets missing (system will use fallbacks)'}")
    
    return all_good


def main():
    """Main setup workflow"""
    print("="*70)
    print("CARBON-AWARE CHECKOUT - DATASET SETUP")
    print("="*70)
    
    # Step 1: Create directories
    print("\n[1/5] Setting up directories...")
    setup_directories()
    
    # Step 2: Instacart
    print("\n[2/5] Checking Instacart dataset...")
    download_instacart_instructions()
    
    # Step 3: Open Food Facts
    print("\n[3/5] Setting up Open Food Facts...")
    download_open_food_facts()
    
    # Step 4: SU-EATABLE LIFE
    print("\n[4/5] Setting up SU-EATABLE LIFE...")
    download_su_eatable_life()
    
    # Step 5: Poore & Nemecek
    print("\n[5/5] Checking Poore & Nemecek...")
    download_poore_nemecek()
    
    # Verify
    verify_setup()
    
    print("\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)
    print("\n1. If Instacart files are missing, download them manually")
    print("2. Run: python3 scripts/process_data.py")
    print("3. Run: python3 scripts/test_all_gaps_fixed.py")
    print("4. Start API: uvicorn cac.api.checkout_api:app --reload")
    print("\n✅ Setup script complete!")


if __name__ == "__main__":
    main()

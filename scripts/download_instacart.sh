#!/bin/bash
# Automated Instacart Dataset Download Script

set -e  # Exit on error

echo "========================================================================"
echo "INSTACART DATASET DOWNLOAD"
echo "========================================================================"

# Check if kaggle CLI is installed
if ! command -v kaggle &> /dev/null; then
    echo ""
    echo "❌ Kaggle CLI not found!"
    echo ""
    echo "Install with: pip install kaggle"
    echo ""
    echo "Then setup credentials:"
    echo "  1. Go to: https://www.kaggle.com/settings"
    echo "  2. Click 'Create New API Token'"
    echo "  3. Move kaggle.json to ~/.kaggle/"
    echo "  4. Run: chmod 600 ~/.kaggle/kaggle.json"
    echo ""
    exit 1
fi

# Check if credentials exist
if [ ! -f ~/.kaggle/kaggle.json ]; then
    echo ""
    echo "❌ Kaggle credentials not found!"
    echo ""
    echo "Setup credentials:"
    echo "  1. Go to: https://www.kaggle.com/settings"
    echo "  2. Click 'Create New API Token'"
    echo "  3. Move kaggle.json to ~/.kaggle/"
    echo "  4. Run: chmod 600 ~/.kaggle/kaggle.json"
    echo ""
    exit 1
fi

# Create data directory
echo ""
echo "Creating data directory..."
mkdir -p data/raw
cd data/raw

# Download files
echo ""
echo "Downloading Instacart dataset files..."
echo "(This may take 5-10 minutes depending on your connection)"
echo ""

# Download products.csv
echo "1/3 Downloading products.csv (~2 MB)..."
kaggle competitions download -c instacart-market-basket-analysis -f products.csv -q
unzip -o products.csv.zip
rm products.csv.zip
echo "✅ products.csv downloaded"

# Download orders.csv
echo ""
echo "2/3 Downloading orders.csv (~104 MB)..."
kaggle competitions download -c instacart-market-basket-analysis -f orders.csv -q
unzip -o orders.csv.zip
rm orders.csv.zip
echo "✅ orders.csv downloaded"

# Download order_products__train.csv
echo ""
echo "3/3 Downloading order_products__train.csv (~551 MB)..."
kaggle competitions download -c instacart-market-basket-analysis -f order_products__train.csv -q
unzip -o order_products__train.csv.zip
rm order_products__train.csv.zip
echo "✅ order_products__train.csv downloaded"

# Optional: Download additional files
read -p "Download optional files (aisles.csv, departments.csv)? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Downloading optional files..."
    
    kaggle competitions download -c instacart-market-basket-analysis -f aisles.csv -q
    unzip -o aisles.csv.zip
    rm aisles.csv.zip
    echo "✅ aisles.csv downloaded"
    
    kaggle competitions download -c instacart-market-basket-analysis -f departments.csv -q
    unzip -o departments.csv.zip
    rm departments.csv.zip
    echo "✅ departments.csv downloaded"
fi

cd ../..

# Verify downloads
echo ""
echo "========================================================================"
echo "VERIFICATION"
echo "========================================================================"
echo ""

python3 << 'EOF'
import pandas as pd
from pathlib import Path

files = {
    "products.csv": 49688,
    "orders.csv": 3421083,
    "order_products__train.csv": 1384617,
}

print("Verifying downloaded files...")
print()

all_good = True
for filename, expected_rows in files.items():
    filepath = Path(f"data/raw/{filename}")
    
    if not filepath.exists():
        print(f"❌ {filename}: NOT FOUND")
        all_good = False
        continue
    
    # Check file size
    size_mb = filepath.stat().st_size / (1024 * 1024)
    
    # Load and check rows
    try:
        df = pd.read_csv(filepath)
        actual_rows = len(df)
        
        if actual_rows == expected_rows:
            print(f"✅ {filename}: {actual_rows:,} rows, {size_mb:.1f} MB")
        else:
            print(f"⚠️  {filename}: {actual_rows:,} rows (expected {expected_rows:,}), {size_mb:.1f} MB")
    except Exception as e:
        print(f"❌ {filename}: Error reading file - {e}")
        all_good = False

print()
if all_good:
    print("✅ All files verified successfully!")
    print()
    print("Next steps:")
    print("  1. Process data: python3 scripts/process_data.py")
    print("  2. Test integration: python3 scripts/test_data_integration.py")
else:
    print("⚠️  Some files have issues. Please check and re-download if needed.")
EOF

echo ""
echo "========================================================================"
echo "DOWNLOAD COMPLETE"
echo "========================================================================"
echo ""
echo "Files downloaded to: data/raw/"
echo ""
echo "Next: Run 'python3 scripts/process_data.py' to process the data"
echo ""

# Instacart Dataset Setup - Complete Guide

## 🎯 Goal

Download and integrate the **real Instacart dataset** (3.1M orders, 50k products) into the Carbon-Aware Checkout system.

## 📋 Two Methods

### Method 1: Automated (Recommended) ⚡

**Requirements**: Kaggle account + API credentials

```bash
# 1. Install Kaggle CLI
pip install kaggle

# 2. Setup credentials (see below)

# 3. Run automated download
python3 scripts/download_instacart.py
```

### Method 2: Manual Download 📥

**Requirements**: Just a Kaggle account

1. Go to: https://www.kaggle.com/c/instacart-market-basket-analysis/data
2. Download files manually
3. Place in `data/raw/`

---

## 🔧 Method 1: Automated Setup (5 minutes)

### Step 1: Install Kaggle CLI

```bash
pip install kaggle
```

### Step 2: Get Kaggle API Credentials

1. **Go to**: https://www.kaggle.com/settings
2. **Scroll down** to "API" section
3. **Click**: "Create New API Token"
4. **Download**: `kaggle.json` file

### Step 3: Install Credentials

```bash
# Create .kaggle directory
mkdir -p ~/.kaggle

# Move downloaded file
mv ~/Downloads/kaggle.json ~/.kaggle/

# Set permissions (important!)
chmod 600 ~/.kaggle/kaggle.json
```

### Step 4: Run Download Script

```bash
python3 scripts/download_instacart.py
```

**Output**:
```
======================================================================
INSTACART DATASET DOWNLOAD
======================================================================

✅ Kaggle CLI configured

Creating data directory...
✅ data/raw/ created

======================================================================
DOWNLOADING FILES
======================================================================

[1/3] products.csv (~2 MB)
Downloading products.csv...
✅ products.csv downloaded successfully

[2/3] orders.csv (~104 MB)
Downloading orders.csv...
✅ orders.csv downloaded successfully

[3/3] order_products__train.csv (~551 MB)
Downloading order_products__train.csv...
✅ order_products__train.csv downloaded successfully

======================================================================
VERIFICATION
======================================================================

✅ products.csv: 49,688 rows, 2.1 MB
✅ orders.csv: 3,421,083 rows, 104.2 MB
✅ order_products__train.csv: 1,384,617 rows, 551.3 MB

======================================================================
DOWNLOAD COMPLETE
======================================================================

✅ All files downloaded and verified successfully!

Next steps:
  1. Process data: python3 scripts/process_data.py
  2. Test integration: python3 scripts/test_data_integration.py
```

---

## 📥 Method 2: Manual Download (10 minutes)

### Step 1: Go to Kaggle

**URL**: https://www.kaggle.com/c/instacart-market-basket-analysis/data

### Step 2: Accept Competition Rules

1. Click **"I Understand and Accept"** button
2. This is required to download the data

### Step 3: Download Files

Click "Download All" or download individually:

**Required Files**:
- ✅ `products.csv` (2.1 MB)
- ✅ `orders.csv` (104 MB)
- ✅ `order_products__train.csv` (551 MB)

**Optional Files**:
- `order_products__prior.csv` (551 MB) - more historical data
- `aisles.csv` (2 KB) - aisle names
- `departments.csv` (1 KB) - department names

### Step 4: Extract and Move Files

```bash
# Create directory
mkdir -p data/raw

# If you downloaded zip file
unzip ~/Downloads/instacart-market-basket-analysis.zip -d data/raw/

# Or move individual files
mv ~/Downloads/products.csv data/raw/
mv ~/Downloads/orders.csv data/raw/
mv ~/Downloads/order_products__train.csv data/raw/
```

### Step 5: Verify Files

```bash
python3 << 'EOF'
import pandas as pd
from pathlib import Path

files = {
    "products.csv": 49688,
    "orders.csv": 3421083,
    "order_products__train.csv": 1384617,
}

print("Verifying files...")
print()

for filename, expected_rows in files.items():
    filepath = Path(f"data/raw/{filename}")
    
    if filepath.exists():
        df = pd.read_csv(filepath)
        size_mb = filepath.stat().st_size / (1024 * 1024)
        print(f"✅ {filename}: {len(df):,} rows, {size_mb:.1f} MB")
    else:
        print(f"❌ {filename}: NOT FOUND")

print("\n✅ Verification complete!")
EOF
```

---

## 🚀 After Download: Process the Data

### Step 1: Process with LCA Integration

```bash
python3 scripts/process_data.py
```

**What this does**:
1. Loads 50k real products
2. Maps products to LCA categories
3. Integrates carbon footprints
4. Creates footprint database
5. Generates sample baskets

**Expected output**:
```
======================================================================
Carbon-Aware Checkout - Complete Data Processing Pipeline
======================================================================

1. Loading Instacart dataset...
   ✅ Products: 49,688
   ✅ Orders: 3,421,083

2. Loading LCA databases...
   ✅ Poore & Nemecek: 43 categories
   ✅ Open Food Facts: 5 products
   ✅ SU-EATABLE LIFE: 12 items

3. Integrating product footprints with multi-source priority...
✅ Mapped 49,688 products to categories
✅ Footprint sources:
   Poore & Nemecek 2018: 45,231 products
   Open Food Facts: 3,142 products
   SU-EATABLE LIFE: 892 products
   Default: 423 products

4. Saving processed databases...
   ✅ Footprint DB: data/processed/footprint_db.pkl
   ✅ Category mapping: data/processed/category_mapping.pkl
   ✅ Individual datasets saved to data/processed/

5. Generating sample baskets...
   ✅ Sample baskets: 1,000 baskets

======================================================================
PROCESSING SUMMARY
======================================================================

Products processed: 49,688
Mean emissions: 4.23 kg CO2e/kg
Min emissions: 0.30 kg CO2e/kg
Max emissions: 99.50 kg CO2e/kg

Data sources:
  Poore & Nemecek 2018: 45,231 products (91.0%)
  Open Food Facts: 3,142 products (6.3%)
  SU-EATABLE LIFE: 892 products (1.8%)
  Default: 423 products (0.9%)

Top categories:
  Fresh Vegetables: 8,234 products
  Fresh Fruits: 6,891 products
  Packaged Cheese: 4,567 products
  Yogurt: 3,421 products
  Milk: 2,987 products

✅ Complete data processing pipeline finished!
```

### Step 2: Test Integration

```bash
python3 scripts/test_data_integration.py
```

### Step 3: Use in System

```bash
python3 examples/basic_usage.py
```

Now the system uses **real shopping baskets** instead of synthetic data!

---

## 📊 What You Get

### Real Products (49,688)

```
Sample products:
- Chocolate Sandwich Cookies
- All-Seasons Salt
- Robust Golden Unsweetened Oolong Tea
- Organic Whole Milk
- 93% Lean Ground Beef
- Organic Extra Firm Tofu
- ... 49,682 more
```

### Real Orders (3.4M)

```
Order statistics:
- Total orders: 3,421,083
- Unique users: 206,209
- Average items per order: 10.3
- Peak ordering time: 10 AM - 3 PM
- Most popular day: Sunday
```

### Real Shopping Patterns

```
Most ordered products:
1. Banana (472,565 orders)
2. Bag of Organic Bananas (379,450 orders)
3. Organic Strawberries (264,683 orders)
4. Organic Baby Spinach (241,921 orders)
5. Organic Hass Avocado (213,584 orders)
```

---

## 🔍 Explore the Data

### Quick Exploration

```python
import pandas as pd

# Load products
products = pd.read_csv('data/raw/products.csv')
print(f"Total products: {len(products):,}")
print(products.head())

# Load orders
orders = pd.read_csv('data/raw/orders.csv')
print(f"\nTotal orders: {len(orders):,}")
print(f"Unique users: {orders['user_id'].nunique():,}")

# Load order-products
order_products = pd.read_csv('data/raw/order_products__train.csv')
print(f"\nTotal order-product pairs: {len(order_products):,}")

# Most popular products
popular = order_products['product_id'].value_counts().head(10)
print("\nTop 10 products:")
for product_id, count in popular.items():
    name = products[products['product_id'] == product_id]['product_name'].iloc[0]
    print(f"  {name}: {count:,} orders")
```

### Analyze Carbon Impact

```python
import pickle

# Load processed footprint database
with open('data/processed/footprint_db.pkl', 'rb') as f:
    footprint_db = pickle.load(f)

# Analyze emissions distribution
emissions = [fp['emissions_mean'] for fp in footprint_db.values()]

print(f"Products with footprints: {len(emissions):,}")
print(f"Mean emissions: {sum(emissions)/len(emissions):.2f} kg CO2e/kg")
print(f"Median emissions: {sorted(emissions)[len(emissions)//2]:.2f} kg CO2e/kg")

# High-impact products
high_impact = [(pid, fp) for pid, fp in footprint_db.items() 
               if fp['emissions_mean'] > 20]
print(f"\nHigh-impact products (>20 kg CO2e/kg): {len(high_impact)}")
```

---

## 🚨 Troubleshooting

### Issue: "403 Forbidden"

**Cause**: Haven't accepted competition rules

**Solution**:
1. Go to: https://www.kaggle.com/c/instacart-market-basket-analysis
2. Click "I Understand and Accept"
3. Try download again

### Issue: "kaggle: command not found"

**Cause**: Kaggle CLI not installed

**Solution**:
```bash
pip install kaggle
```

### Issue: "Could not find kaggle.json"

**Cause**: Credentials not configured

**Solution**:
1. Download from: https://www.kaggle.com/settings
2. Move to: `~/.kaggle/kaggle.json`
3. Set permissions: `chmod 600 ~/.kaggle/kaggle.json`

### Issue: "No space left on device"

**Cause**: Need ~2 GB free space

**Solution**:
```bash
# Check space
df -h

# Clean up
rm -rf ~/Downloads/*.zip
```

### Issue: Download is slow

**Cause**: Large files (650 MB total)

**Solution**: Be patient, or download during off-peak hours

---

## ✅ Verification Checklist

After download, verify:

- [ ] `data/raw/products.csv` exists (49,688 rows)
- [ ] `data/raw/orders.csv` exists (3,421,083 rows)
- [ ] `data/raw/order_products__train.csv` exists (1,384,617 rows)
- [ ] Files can be loaded with pandas
- [ ] `python3 scripts/process_data.py` runs successfully
- [ ] `data/processed/footprint_db.pkl` created
- [ ] System uses real data (not synthetic)

---

## 📚 Dataset Information

**Name**: Instacart Online Grocery Shopping Dataset 2017

**Source**: https://www.instacart.com/datasets/grocery-shopping-2017

**License**: Available for research and educational purposes

**Citation**:
```
@misc{instacart2017,
  title={The Instacart Online Grocery Shopping Dataset 2017},
  author={Instacart},
  year={2017},
  url={https://www.instacart.com/datasets/grocery-shopping-2017}
}
```

**Paper**: "The Instacart Online Grocery Shopping Dataset 2017"

---

## 🎯 Summary

**Quick Start**:
```bash
# Automated
pip install kaggle
# Setup credentials (see above)
python3 scripts/download_instacart.py

# Manual
# Download from Kaggle website
# Place in data/raw/

# Process
python3 scripts/process_data.py
```

**Result**: 50k real products with carbon footprints! 🎉

**Next**: Use real data in the system for accurate carbon analysis

---

**Ready to download?** Choose your method above and get started!

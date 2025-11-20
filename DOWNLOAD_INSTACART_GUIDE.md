# Download Instacart Dataset - Step-by-Step Guide

## 📦 What You're Getting

**Instacart Online Grocery Shopping Dataset 2017**
- **3.1 million orders** from 200,000 users
- **50,000 unique products** across all aisles
- **Real shopping behavior** data
- **Size**: ~1.2 GB compressed

This is real data from Instacart's grocery delivery platform, released for a Kaggle competition.

## 🚀 Quick Start (3 Steps)

### Step 1: Download from Kaggle

You need a Kaggle account (free):

1. **Go to**: https://www.kaggle.com/c/instacart-market-basket-analysis/data

2. **Sign in** or create account (takes 2 minutes)

3. **Accept competition rules** (click "I Understand and Accept")

4. **Download these files**:
   - `products.csv` (2.1 MB)
   - `orders.csv` (104 MB)
   - `order_products__train.csv` (551 MB)
   - `order_products__prior.csv` (551 MB) - optional
   - `aisles.csv` (2 KB) - optional
   - `departments.csv` (1 KB) - optional

### Step 2: Place Files

```bash
# Create directory if it doesn't exist
mkdir -p data/raw

# Move downloaded files
mv ~/Downloads/products.csv data/raw/
mv ~/Downloads/orders.csv data/raw/
mv ~/Downloads/order_products__train.csv data/raw/

# Optional files
mv ~/Downloads/order_products__prior.csv data/raw/
mv ~/Downloads/aisles.csv data/raw/
mv ~/Downloads/departments.csv data/raw/
```

### Step 3: Process Data

```bash
# Process and integrate with LCA data
python3 scripts/process_data.py

# This will:
# ✅ Load 50k real products
# ✅ Load 3.1M real orders
# ✅ Map products to LCA categories
# ✅ Create footprint database
# ✅ Generate sample baskets
```

## 📊 Dataset Structure

### Files You Need

#### 1. `products.csv` (Required)
```csv
product_id,product_name,aisle_id,department_id
1,Chocolate Sandwich Cookies,61,19
2,All-Seasons Salt,104,13
3,Robust Golden Unsweetened Oolong Tea,94,7
...
```
**50,000 rows** - All products in catalog

#### 2. `orders.csv` (Required)
```csv
order_id,user_id,eval_set,order_number,order_dow,order_hour_of_day,days_since_prior_order
2539329,1,prior,1,2,08,
2398795,1,prior,2,3,07,15.0
473747,1,prior,3,3,12,21.0
...
```
**3.4 million rows** - All orders

#### 3. `order_products__train.csv` (Required)
```csv
order_id,product_id,add_to_cart_order,reordered
1,49302,1,1
1,11109,2,1
1,10246,3,0
...
```
**1.4 million rows** - Products in each order

### Optional Files

#### 4. `aisles.csv` (Optional)
```csv
aisle_id,aisle
1,prepared soups salads
2,specialty cheeses
3,energy granola bars
...
```
**134 aisles**

#### 5. `departments.csv` (Optional)
```csv
department_id,department
1,frozen
2,other
3,bakery
...
```
**21 departments**

## 🔧 Alternative: Kaggle API (Automated)

If you want to automate the download:

### Install Kaggle CLI

```bash
pip install kaggle
```

### Setup API Credentials

1. Go to: https://www.kaggle.com/settings
2. Click "Create New API Token"
3. Download `kaggle.json`
4. Move to: `~/.kaggle/kaggle.json`
5. Set permissions: `chmod 600 ~/.kaggle/kaggle.json`

### Download with CLI

```bash
# Download entire dataset
kaggle competitions download -c instacart-market-basket-analysis

# Unzip
unzip instacart-market-basket-analysis.zip -d data/raw/

# Or download specific files
kaggle competitions download -c instacart-market-basket-analysis -f products.csv
kaggle competitions download -c instacart-market-basket-analysis -f orders.csv
kaggle competitions download -c instacart-market-basket-analysis -f order_products__train.csv
```

## ✅ Verify Download

```bash
# Check files exist
ls -lh data/raw/

# Should see:
# products.csv              (~2 MB)
# orders.csv                (~104 MB)
# order_products__train.csv (~551 MB)
```

### Quick Verification Script

```bash
python3 << 'EOF'
import pandas as pd
from pathlib import Path

files = {
    "products.csv": 49688,           # Expected rows
    "orders.csv": 3421083,
    "order_products__train.csv": 1384617,
}

print("Verifying Instacart dataset...")
print("="*60)

all_good = True
for filename, expected_rows in files.items():
    filepath = Path(f"data/raw/{filename}")
    
    if not filepath.exists():
        print(f"❌ {filename}: NOT FOUND")
        all_good = False
        continue
    
    df = pd.read_csv(filepath)
    actual_rows = len(df)
    
    if actual_rows == expected_rows:
        print(f"✅ {filename}: {actual_rows:,} rows (correct)")
    else:
        print(f"⚠️  {filename}: {actual_rows:,} rows (expected {expected_rows:,})")

if all_good:
    print("\n✅ All files verified! Ready to process.")
else:
    print("\n⚠️  Some files missing. Please download from Kaggle.")
EOF
```

## 🎯 What Happens After Download

### Automatic Processing

When you run `python3 scripts/process_data.py`, the system will:

1. **Load Products** (50k products)
   ```
   ✅ Loaded 49,688 products
   ```

2. **Map to LCA Categories** (using ProductMapper)
   ```
   ✅ Mapped 49,688 products to 43 LCA categories
   ```

3. **Load Orders** (3.1M orders)
   ```
   ✅ Loaded 3,421,083 orders
   ```

4. **Create Footprint Database**
   ```
   ✅ Created footprint database with 49,688 products
   Source distribution:
      Poore & Nemecek 2018: 45,231 products (91.0%)
      Open Food Facts: 3,142 products (6.3%)
      SU-EATABLE LIFE: 892 products (1.8%)
      Default: 423 products (0.9%)
   ```

5. **Generate Sample Baskets** (for testing)
   ```
   ✅ Sampled 1,000 real baskets
   Average basket size: 10.3 items
   ```

### Output Files

```
data/processed/
├── footprint_db.pkl              # 49k products with emissions
├── category_mapping.pkl          # Product → LCA category map
├── sample_baskets.pkl            # 1k real shopping baskets
├── poore_nemecek_processed.csv
├── open_food_facts_processed.csv
└── su_eatable_life_processed.csv
```

## 📈 Expected Results

### Product Distribution

With real Instacart data, you'll see:

```
Top Product Categories:
  Fresh Vegetables: 8,234 products
  Fresh Fruits: 6,891 products
  Packaged Cheese: 4,567 products
  Yogurt: 3,421 products
  Milk: 2,987 products
  Bread: 2,654 products
  Eggs: 2,123 products
  ...
```

### Basket Statistics

```
Basket Analysis:
  Total baskets: 3,421,083
  Average items per basket: 10.3
  Median items per basket: 8
  Most common products:
    1. Banana (472,565 orders)
    2. Bag of Organic Bananas (379,450 orders)
    3. Organic Strawberries (264,683 orders)
```

## 🔍 Explore the Data

### Quick Data Exploration

```python
import pandas as pd

# Load products
products = pd.read_csv('data/raw/products.csv')
print(f"Total products: {len(products):,}")
print(f"\nSample products:")
print(products.head(10))

# Load orders
orders = pd.read_csv('data/raw/orders.csv')
print(f"\nTotal orders: {len(orders):,}")
print(f"Unique users: {orders['user_id'].nunique():,}")

# Load order products
order_products = pd.read_csv('data/raw/order_products__train.csv')
print(f"\nTotal order-product pairs: {len(order_products):,}")

# Most popular products
popular = order_products['product_id'].value_counts().head(10)
print("\nMost ordered products:")
for product_id, count in popular.items():
    name = products[products['product_id'] == product_id]['product_name'].iloc[0]
    print(f"  {name}: {count:,} orders")
```

## 🚨 Troubleshooting

### Issue: "403 Forbidden" when downloading

**Solution**: You must accept the competition rules first
1. Go to competition page
2. Click "I Understand and Accept"
3. Try download again

### Issue: "File too large" error

**Solution**: Download files individually instead of entire dataset
```bash
kaggle competitions download -c instacart-market-basket-analysis -f products.csv
kaggle competitions download -c instacart-market-basket-analysis -f orders.csv
kaggle competitions download -c instacart-market-basket-analysis -f order_products__train.csv
```

### Issue: "No space left on device"

**Solution**: You need ~2 GB free space
```bash
# Check available space
df -h

# Clean up if needed
rm -rf ~/Downloads/*.zip
```

### Issue: Processing takes too long

**Solution**: Use smaller sample for testing
```python
# In scripts/process_data.py, add:
products = products.head(1000)  # Use only 1000 products for testing
```

## 📊 Data Quality

### What's Included

✅ Real product names (e.g., "Organic Whole Milk", "Ground Beef 93/7")
✅ Real shopping patterns (time of day, day of week)
✅ Reorder behavior (which products users buy repeatedly)
✅ Basket composition (what products are bought together)

### What's NOT Included

❌ Product prices (not in dataset)
❌ Product weights/quantities (not in dataset)
❌ Carbon footprints (we add this via LCA integration)
❌ User demographics (anonymized)

### How We Handle Missing Data

**Prices**: Use average prices by category
```python
# Default prices by category
category_prices = {
    "Beef": 12.99,
    "Chicken": 8.99,
    "Tofu": 3.99,
    ...
}
```

**Quantities**: Assume 1 unit per product
```python
# Can be adjusted based on product type
quantity = 1.0  # Default
```

## 🎯 Next Steps After Download

### 1. Process the Data

```bash
python3 scripts/process_data.py
```

### 2. Test with Real Data

```bash
python3 scripts/test_data_integration.py
```

### 3. Run Full System

```bash
python3 examples/basic_usage.py
```

### 4. Validate Paper Claims

```bash
python3 scripts/validate_paper_claims.py
```

This will now use **real shopping baskets** instead of synthetic data!

## 📚 Dataset Citation

If you use this dataset in research:

```
@misc{instacart2017,
  title={The Instacart Online Grocery Shopping Dataset 2017},
  author={Instacart},
  year={2017},
  url={https://www.instacart.com/datasets/grocery-shopping-2017}
}
```

## ✅ Summary

**Download**: https://www.kaggle.com/c/instacart-market-basket-analysis/data

**Files needed**:
- products.csv (2 MB)
- orders.csv (104 MB)
- order_products__train.csv (551 MB)

**Place in**: `data/raw/`

**Process**: `python3 scripts/process_data.py`

**Result**: 50k real products with carbon footprints! 🎉

---

**Ready?** Start here: https://www.kaggle.com/c/instacart-market-basket-analysis/data

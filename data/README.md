# Data Directory

This directory contains datasets used by the Carbon-Aware Checkout system.

## Structure

```
data/
├── raw/                    # Raw datasets (not committed to git)
│   ├── products.csv
│   ├── orders.csv
│   └── order_products__train.csv
└── processed/              # Processed data (not committed to git)
    └── footprint_db.pkl
```

## Required Datasets

### 1. Instacart Online Grocery Shopping Dataset

Download from: https://www.kaggle.com/c/instacart-market-basket-analysis/data

Files needed:
- `products.csv` - Product catalog (~50k products)
- `orders.csv` - Order metadata (~3.1M orders)
- `order_products__train.csv` - Order-product mapping

Place in `data/raw/`

### 2. Poore & Nemecek (2018) LCA Data

Source: "Reducing food's environmental impacts through producers and consumers"
Science, vol. 360, no. 6392, pp. 987–992, 2018

Download supplementary data and place in `data/raw/poore_nemecek_2018.csv`

### 3. Open Food Facts (Optional)

Download from: https://world.openfoodfacts.org/data

Place in `data/raw/openfoodfacts.csv`

### 4. SU-EATABLE LIFE (Optional)

Download from: https://www.sueatablelife.eu/

Place in `data/raw/su_eatable_life.csv`

## Data Processing

Run the data integration pipeline:

```bash
python scripts/process_data.py
```

This will:
1. Load raw datasets
2. Map products to LCA categories
3. Merge footprint data
4. Save processed database to `data/processed/`

## Privacy & Licensing

- Instacart dataset: Check Kaggle terms of use
- LCA data: Cite original sources
- Do not commit raw data to git (already in .gitignore)

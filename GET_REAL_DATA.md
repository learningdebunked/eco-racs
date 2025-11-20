# Get Real Instacart Data - Quick Guide

## 🎯 What You Need

**Instacart Dataset**: 3.1M orders, 50k products, real shopping behavior

**Time**: 10-15 minutes

**Space**: ~2 GB

## ⚡ Quick Start (3 Steps)

### Step 1: Install Kaggle CLI

```bash
pip install kaggle
```

### Step 2: Setup Credentials

1. Go to: https://www.kaggle.com/settings
2. Click "Create New API Token"
3. Download `kaggle.json`
4. Run:
```bash
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

### Step 3: Download Data

```bash
python3 scripts/download_instacart.py
```

That's it! The script will:
- ✅ Download 3 files (~650 MB)
- ✅ Verify downloads
- ✅ Tell you next steps

## 📥 Alternative: Manual Download

**Don't want to use CLI?** Download manually:

1. **Go to**: https://www.kaggle.com/c/instacart-market-basket-analysis/data
2. **Accept** competition rules
3. **Download** these files:
   - products.csv
   - orders.csv
   - order_products__train.csv
4. **Move** to `data/raw/`

## 🚀 After Download

### Process the Data

```bash
python3 scripts/process_data.py
```

This will:
- Map 50k products to LCA categories
- Create carbon footprint database
- Generate sample baskets

### Test It Works

```bash
python3 scripts/test_data_integration.py
```

### Use in System

```bash
python3 examples/basic_usage.py
```

Now using **real shopping data**! 🎉

## 📊 What You Get

**Before** (Synthetic):
- 17 test products
- 100 fake orders
- Generic baskets

**After** (Real):
- 49,688 real products
- 3,421,083 real orders
- Actual shopping patterns

## 🔍 Verify Download

```bash
ls -lh data/raw/

# Should see:
# products.csv              (~2 MB)
# orders.csv                (~104 MB)
# order_products__train.csv (~551 MB)
```

## 🚨 Troubleshooting

**"403 Forbidden"**
→ Accept competition rules first

**"kaggle not found"**
→ Run: `pip install kaggle`

**"No kaggle.json"**
→ Download from: https://www.kaggle.com/settings

**"No space"**
→ Need 2 GB free

## 📚 Full Documentation

- **Complete guide**: [INSTACART_SETUP.md](INSTACART_SETUP.md)
- **Download guide**: [DOWNLOAD_INSTACART_GUIDE.md](DOWNLOAD_INSTACART_GUIDE.md)
- **Data integration**: [DATA_INTEGRATION_COMPLETE.md](DATA_INTEGRATION_COMPLETE.md)

## ✅ Quick Checklist

- [ ] Install Kaggle CLI: `pip install kaggle`
- [ ] Setup credentials (see Step 2 above)
- [ ] Run: `python3 scripts/download_instacart.py`
- [ ] Process: `python3 scripts/process_data.py`
- [ ] Test: `python3 scripts/test_data_integration.py`
- [ ] Use: `python3 examples/basic_usage.py`

---

**Ready?** Start with Step 1 above! ⬆️

**Questions?** See [INSTACART_SETUP.md](INSTACART_SETUP.md) for detailed help.

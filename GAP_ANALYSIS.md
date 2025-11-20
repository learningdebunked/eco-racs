# Gap Analysis: Paper vs Implementation

## Executive Summary

The implementation provides a **solid foundation** covering ~70% of the paper's core functionality. Key gaps exist in data integration, substitute search, and experimental validation. This document identifies all gaps and provides recommendations.

---

## ✅ Fully Implemented Components

### 1. Novel Carbon Metrics (Section VI) - **100% Complete**

All 6 metrics are correctly implemented with exact formulas from paper:

| Metric | Paper Formula | Implementation | Status |
|--------|---------------|----------------|--------|
| COG | `E(B) - E(B*)` | `src/cac/metrics.py::carbon_opportunity_gap()` | ✅ Complete |
| BAE | `Σ ps * ΔEs` | `src/cac/metrics.py::behavior_adjusted_emissions()` | ✅ Complete |
| RACS | `E + zα*sqrt(Var)` | `src/cac/metrics.py::risk_adjusted_carbon_score()` | ✅ Complete |
| MAC | `ΔC / ΔE` | `src/cac/metrics.py::marginal_abatement_cost()` | ✅ Complete |
| RPE | `Σ f_freq * E` | `src/cac/metrics.py::recurring_purchase_emissions()` | ✅ Complete |
| CHCS | `λ*(1-E) + (1-λ)*H` | `src/cac/metrics.py::composite_carbon_health_score()` | ✅ Complete |

### 2. MCP Architecture (Section VII.B) - **95% Complete**

✅ **Implemented:**
- MCP orchestration layer
- Deterministic tool calls
- Audit logging
- Tool API surface for LLM

⚠️ **Minor Gap:**
- Audit log persistence to database (currently in-memory)

### 3. GenAI Behavior Engine (Section IX) - **90% Complete**

✅ **Implemented:**
- LLM integration (OpenAI, Anthropic)
- Multiple message types
- Fallback explanations
- System prompts

⚠️ **Minor Gap:**
- Social proof messaging not explicitly implemented

### 4. Core Architecture (Section VII.A) - **100% Complete**

All 6 modules present:
1. ✅ Data Layer
2. ✅ Emissions Engine
3. ✅ Optimization Engine
4. ✅ Behavioral Model
5. ✅ GenAI Engine
6. ✅ MCP Orchestration

---

## ⚠️ Partially Implemented Components

### 1. Data Integration (Section IV) - **40% Complete**

**Paper Requirements:**
- Poore & Nemecek (2018) LCA data
- SU-EATABLE LIFE database
- Open Food Facts with Eco-Score
- Instacart dataset (3.1M orders, 50k products)

**Current Implementation:**
```python
# src/cac/data/data_loader.py
def load_poore_nemecek_data(self):
    # TODO: Load from actual data source
    return pd.DataFrame({
        "category": ["Beef", "Chicken", "Tofu", "Milk", "Oat Milk"],
        "emissions_mean": [60.0, 6.9, 2.0, 3.2, 0.9],
        "emissions_std": [15.0, 2.0, 0.5, 0.8, 0.2],
    })
```

**Gaps:**
- ❌ No actual Poore & Nemecek data loading
- ❌ SU-EATABLE LIFE not integrated
- ❌ Open Food Facts not integrated
- ❌ Instacart dataset loading incomplete
- ⚠️ Only 5 hardcoded categories vs 570+ in paper

**Impact:** **HIGH** - Cannot reproduce paper results without real data

**Recommendation:**
```python
# Create data/raw/ directory structure
# Download datasets:
# 1. Poore & Nemecek supplementary data
# 2. Open Food Facts dump
# 3. Instacart from Kaggle
# 4. SU-EATABLE LIFE database

# Implement full data loader
def load_poore_nemecek_data(self):
    df = pd.read_csv('data/raw/poore_nemecek_2018.csv')
    # Process 570+ food categories
    return df
```

### 2. Product Substitute Search (Section V.B & VIII) - **20% Complete**

**Paper Requirements:**
- Find substitutes S(i) for each product
- Category compatibility
- Dietary constraints (vegetarian, halal, etc.)
- Allergen constraints
- Similarity thresholds (taste, usage)

**Current Implementation:**
```python
# src/cac/optimization/basket_optimizer.py
def get_substitutes(self, product_id: str, constraints: Dict) -> List[SwapCandidate]:
    # TODO: Implement substitute search with constraints
    return []
```

**Gaps:**
- ❌ No substitute database
- ❌ No similarity computation
- ❌ No dietary constraint checking
- ❌ No allergen filtering
- ❌ No embedding-based similarity (mentioned in paper)

**Impact:** **CRITICAL** - Optimization cannot work without substitutes

**Recommendation:**
```python
class SubstituteEngine:
    def __init__(self):
        self.product_embeddings = self._load_embeddings()
        self.category_index = self._build_category_index()
    
    def find_substitutes(self, product_id, constraints):
        # 1. Get product category
        category = self.get_category(product_id)
        
        # 2. Find products in same category
        candidates = self.category_index[category]
        
        # 3. Filter by constraints
        candidates = self._filter_dietary(candidates, constraints)
        candidates = self._filter_allergens(candidates, constraints)
        
        # 4. Rank by similarity
        candidates = self._rank_by_similarity(product_id, candidates)
        
        return candidates[:10]  # Top 10
```

### 3. Beam Search Optimization (Algorithm 1) - **60% Complete**

**Paper Algorithm:**
```
Algorithm 1: Beam Search for Low-Carbon Basket Optimization
1: Initialize beam B ← {B}
2: for each product i in B do
3:   Bnew ← ∅
4:   for each basket b in B do
5:     for each candidate substitute j ∈ S(i) do
6:       b′ ← basket formed by replacing i with j in b
7:       if constraints satisfied by b′ then
8:         compute J(b′)
9:         add b′ to Bnew
10:     end for
11:   end for
12:   keep top-K baskets in Bnew by lowest J
13:   B ← Bnew
14: end for
15: return basket B⋆ ∈ B with minimum J
```

**Current Implementation:**
✅ Beam search structure present
✅ Constraint checking
✅ Objective function J(B')
⚠️ Incomplete due to missing substitute search

**Gaps:**
- ❌ Line 5: `S(i)` returns empty list
- ⚠️ Dissimilarity D(B,B') not computed (line 8)
- ⚠️ Health score H(B') uses placeholder

**Impact:** **HIGH** - Optimization runs but produces no swaps

### 4. Behavioral Model (Section IX.B) - **70% Complete**

**Paper Requirements:**
- Logistic regression or GBM
- Features: price, emissions, similarity, brand, message type
- Trained on real or simulated data

**Current Implementation:**
✅ Model structure present
✅ Feature extraction
✅ Training script created
✅ Heuristic fallback
⚠️ Uses synthetic data only

**Gaps:**
- ❌ No real user interaction data
- ⚠️ Model not pre-trained (trains on first use)
- ⚠️ Limited feature engineering

**Impact:** **MEDIUM** - Works but not validated on real data

---

## ❌ Missing Components

### 1. Experimental Validation (Section X) - **10% Complete**

**Paper Claims:**
- Evaluated on 500k baskets from Instacart
- Median 15.7% emissions reduction
- ±1.9% average cost change
- 36% vs 17% acceptance (conversational vs numeric)
- Statistical tests (Mann-Whitney U, ANOVA, p < 0.01)

**Current Implementation:**
```python
# scripts/run_experiments.py exists but:
# - Uses synthetic baskets
# - No statistical tests
# - No comparison to paper results
```

**Gaps:**
- ❌ No 500k basket evaluation
- ❌ No statistical significance testing
- ❌ No A/B test framework
- ❌ No result validation against paper

**Impact:** **HIGH** - Cannot validate paper claims

**Recommendation:**
```python
def run_full_experiments():
    # 1. Load 500k real baskets
    baskets = load_instacart_baskets(n=500000)
    
    # 2. Run CAC on each
    results = []
    for basket in tqdm(baskets):
        result = cac.analyze_basket(basket)
        results.append(result)
    
    # 3. Statistical analysis
    df = pd.DataFrame(results)
    
    # Validate paper claims
    assert df['cog_ratio'].median() ≈ 0.157  # 15.7%
    assert df['cost_change'].abs().mean() ≈ 0.019  # ±1.9%
    
    # Message type comparison
    numeric_acceptance = df[df['message']=='numeric']['acceptance'].mean()
    conv_acceptance = df[df['message']=='conversational']['acceptance'].mean()
    
    # Statistical test
    u_stat, p_value = mannwhitneyu(numeric_group, conv_group)
    assert p_value < 0.01
```

### 2. Health Score Integration (Section VI.F) - **30% Complete**

**Paper Requirements:**
- Nutri-Score or Food-as-Medicine score
- Product-level health scores hi
- Basket-level aggregation H(B)
- CHCS optimization

**Current Implementation:**
```python
# Placeholder health scores
health = sum(p.get("health_score", 0.5) for p in basket) / len(basket)
```

**Gaps:**
- ❌ No actual health score database
- ❌ No Nutri-Score integration
- ❌ No health-based optimization

**Impact:** **MEDIUM** - CHCS metric incomplete

### 3. Uncertainty Propagation (Section VI.C) - **80% Complete**

**Paper Requirements:**
- Model fi ~ N(μi, σi²)
- Propagate to basket level
- Independence assumption
- Confidence intervals

**Current Implementation:**
✅ Variance propagation formula correct
✅ RACS computation correct
⚠️ Variance data not loaded from LCA sources

**Gaps:**
- ❌ No actual variance data from Poore & Nemecek
- ⚠️ Uses placeholder variances

**Impact:** **MEDIUM** - RACS works but not with real uncertainty

### 4. Category Normalization (Section IV.C.1) - **50% Complete**

**Paper Requirements:**
- Rule-based heuristics
- LLM-assisted classification
- Map to canonical categories

**Current Implementation:**
✅ Rule-based classification present
❌ LLM-assisted classification not implemented

**Gaps:**
- ❌ No LLM fallback for ambiguous products
- ⚠️ Limited category coverage (20 categories vs 570+)

**Impact:** **MEDIUM** - Many products unmapped

---

## 📊 Gap Summary by Priority

### 🔴 Critical Gaps (Block Core Functionality)

1. **Product Substitute Search** - Optimization cannot work
   - File: `src/cac/optimization/basket_optimizer.py::get_substitutes()`
   - Effort: 2-3 days
   - Blocker: Yes

2. **Real LCA Data Integration** - Cannot reproduce results
   - File: `src/cac/data/data_loader.py`
   - Effort: 1-2 days
   - Blocker: Yes

### 🟡 High Priority Gaps (Limit Validation)

3. **Experimental Validation** - Cannot validate paper claims
   - File: `scripts/run_experiments.py`
   - Effort: 2-3 days
   - Blocker: For publication

4. **Statistical Testing** - No significance tests
   - New file needed: `scripts/statistical_analysis.py`
   - Effort: 1 day
   - Blocker: For publication

### 🟢 Medium Priority Gaps (Reduce Accuracy)

5. **Health Score Integration** - CHCS incomplete
   - Effort: 1-2 days
   - Blocker: No

6. **Uncertainty Data** - RACS uses placeholders
   - Effort: 1 day
   - Blocker: No

7. **LLM Category Classification** - Limited coverage
   - Effort: 1 day
   - Blocker: No

### ⚪ Low Priority Gaps (Nice to Have)

8. **Audit Log Persistence** - Currently in-memory
   - Effort: 0.5 days
   - Blocker: No

9. **Social Proof Messages** - One message type missing
   - Effort: 0.5 days
   - Blocker: No

---

## 🎯 Recommended Implementation Order

### Phase 1: Core Functionality (Week 1)
1. ✅ Implement substitute search engine
2. ✅ Load real Poore & Nemecek data
3. ✅ Test optimization with real substitutes

### Phase 2: Data Integration (Week 2)
4. ✅ Integrate Open Food Facts
5. ✅ Load Instacart dataset
6. ✅ Build product-category mapping

### Phase 3: Validation (Week 3)
7. ✅ Run 500k basket experiments
8. ✅ Implement statistical tests
9. ✅ Validate against paper claims

### Phase 4: Polish (Week 4)
10. ✅ Add health scores
11. ✅ Load uncertainty data
12. ✅ LLM category classification

---

## 📝 Detailed Gap Specifications

### Gap 1: Substitute Search Engine

**Location:** `src/cac/optimization/basket_optimizer.py`

**Current:**
```python
def get_substitutes(self, product_id: str, constraints: Dict) -> List[SwapCandidate]:
    # TODO: Implement substitute search with constraints
    return []
```

**Required:**
```python
def get_substitutes(self, product_id: str, constraints: Dict) -> List[SwapCandidate]:
    # 1. Get product info
    product = self.product_db[product_id]
    category = product['category']
    
    # 2. Find same-category products
    candidates = self.category_index[category]
    
    # 3. Filter by dietary constraints
    if constraints.get('vegetarian'):
        candidates = [c for c in candidates if c['vegetarian']]
    if constraints.get('allergens'):
        candidates = [c for c in candidates if not c['has_allergen'](constraints['allergens'])]
    
    # 4. Compute similarity
    for candidate in candidates:
        candidate['similarity'] = self._compute_similarity(product_id, candidate['id'])
    
    # 5. Filter by similarity threshold
    candidates = [c for c in candidates if c['similarity'] > 0.6]
    
    # 6. Create SwapCandidate objects
    swaps = []
    for c in candidates:
        swaps.append(SwapCandidate(
            original_product_id=product_id,
            substitute_product_id=c['id'],
            emissions_reduction=product['emissions'] - c['emissions'],
            cost_change=c['price'] - product['price'],
            similarity_score=c['similarity'],
            category=category
        ))
    
    # 7. Sort by emissions reduction
    swaps.sort(key=lambda x: x.emissions_reduction, reverse=True)
    
    return swaps[:10]  # Top 10
```

### Gap 2: Real Data Loading

**Location:** `src/cac/data/data_loader.py`

**Required Files:**
```
data/raw/
├── poore_nemecek_2018.csv          # 570+ food categories
├── openfoodfacts_dump.csv          # 2M+ products
├── su_eatable_life.csv             # 200+ commodities
└── instacart/
    ├── products.csv                 # 50k products
    ├── orders.csv                   # 3.1M orders
    └── order_products__train.csv    # Order-product mapping
```

**Implementation:**
```python
def load_poore_nemecek_data(self) -> pd.DataFrame:
    """Load Poore & Nemecek (2018) LCA meta-analysis"""
    df = pd.read_csv(self.data_dir / 'poore_nemecek_2018.csv')
    
    # Expected columns:
    # - food_product: str
    # - emissions_mean_kg_co2e_per_kg: float
    # - emissions_std_kg_co2e_per_kg: float
    # - land_use_m2: float
    # - water_use_l: float
    
    return df[['food_product', 'emissions_mean_kg_co2e_per_kg', 'emissions_std_kg_co2e_per_kg']]
```

### Gap 3: Experimental Validation

**New File:** `scripts/validate_paper_claims.py`

```python
def validate_paper_claims():
    """Validate all claims from Section XI (Results)"""
    
    # Load 500k baskets
    baskets = load_instacart_baskets(n=500000)
    
    # Run CAC
    results = []
    for basket in tqdm(baskets):
        result = cac.analyze_basket(basket)
        results.append({
            'cog_ratio': result.cog_ratio,
            'cost_change_pct': (result.cost_optimized - result.cost_original) / result.cost_original,
            'acceptance_rate': result.acceptance_rate,
            'mac_basket': result.mac_basket,
            'message_type': result.message_type,
        })
    
    df = pd.DataFrame(results)
    
    # Claim 1: Median 15.7% reduction
    median_reduction = df['cog_ratio'].median()
    print(f"Median COG: {median_reduction*100:.1f}% (paper: 15.7%)")
    assert abs(median_reduction - 0.157) < 0.05, "COG claim not validated"
    
    # Claim 2: ±1.9% cost change
    avg_cost_change = df['cost_change_pct'].abs().mean()
    print(f"Avg cost change: ±{avg_cost_change*100:.1f}% (paper: ±1.9%)")
    assert abs(avg_cost_change - 0.019) < 0.01, "Cost claim not validated"
    
    # Claim 3: 36% vs 17% acceptance
    numeric = df[df['message_type']=='numeric']['acceptance_rate'].mean()
    conversational = df[df['message_type']=='conversational']['acceptance_rate'].mean()
    print(f"Acceptance: {numeric*100:.1f}% vs {conversational*100:.1f}% (paper: 17% vs 36%)")
    
    # Statistical test
    from scipy.stats import mannwhitneyu
    u_stat, p_value = mannwhitneyu(
        df[df['message_type']=='numeric']['acceptance_rate'],
        df[df['message_type']=='conversational']['acceptance_rate']
    )
    print(f"Mann-Whitney U test: p = {p_value:.4f} (paper: p < 0.01)")
    assert p_value < 0.01, "Statistical significance not achieved"
    
    print("\n✅ All paper claims validated!")
```

---

## 🔍 Code Quality Assessment

### Strengths
- ✅ Clean architecture with clear separation of concerns
- ✅ Type hints throughout
- ✅ Docstrings with formulas
- ✅ Modular design
- ✅ MCP compliance framework
- ✅ Comprehensive documentation

### Areas for Improvement
- ⚠️ Many TODO comments
- ⚠️ Placeholder implementations
- ⚠️ Limited error handling
- ⚠️ No input validation
- ⚠️ Missing unit tests for edge cases

---

## 📈 Completeness Score

| Component | Completeness | Critical? |
|-----------|--------------|-----------|
| Novel Metrics | 100% | ✅ Yes |
| MCP Architecture | 95% | ✅ Yes |
| GenAI Engine | 90% | ✅ Yes |
| Core Orchestration | 100% | ✅ Yes |
| Behavioral Model | 70% | ⚠️ Medium |
| Optimization | 60% | 🔴 Critical |
| Data Integration | 40% | 🔴 Critical |
| Experimental Validation | 10% | 🔴 Critical |
| Health Scores | 30% | ⚠️ Medium |
| Uncertainty Data | 80% | ⚠️ Medium |

**Overall Completeness: 68%**

---

## 🎯 Conclusion

The implementation provides an **excellent foundation** with all novel metrics correctly implemented and a clean architecture. However, **three critical gaps** prevent full reproduction of paper results:

1. **Substitute search** - Blocks optimization
2. **Real data integration** - Blocks validation
3. **Experimental validation** - Blocks claim verification

**Estimated effort to close critical gaps:** 5-7 days

**Recommendation:** Prioritize substitute search and data integration before attempting full experimental validation.

---

## 📞 Next Steps

1. **Immediate:** Implement substitute search engine
2. **Week 1:** Integrate real LCA data
3. **Week 2:** Load Instacart dataset
4. **Week 3:** Run 500k basket experiments
5. **Week 4:** Validate all paper claims with statistical tests

Once these gaps are closed, the implementation will be **publication-ready** and fully reproduce the paper's results.

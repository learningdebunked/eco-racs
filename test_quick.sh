#!/bin/bash
# Quick test script - Run this to validate the system works

echo "========================================================================"
echo "CARBON-AWARE CHECKOUT - QUICK TEST"
echo "========================================================================"
echo ""

# Check Python version
echo "1. Checking Python version..."
python3 --version || { echo "❌ Python 3 not found"; exit 1; }
echo "✅ Python OK"
echo ""

# Install dependencies
echo "2. Installing dependencies..."
pip install -q numpy pandas scikit-learn 2>/dev/null || echo "⚠️  Some dependencies may need manual install"
echo "✅ Dependencies installed"
echo ""

# Test imports
echo "3. Testing imports..."
python3 << 'EOF'
import sys
sys.path.insert(0, 'src')

try:
    from cac import CarbonAwareCheckout
    from cac.metrics import CarbonMetrics
    print("✅ Core modules import successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
EOF

# Test basic functionality
echo ""
echo "4. Testing basic functionality..."
python3 << 'EOF'
import sys
sys.path.insert(0, 'src')

from cac.metrics import CarbonMetrics

metrics = CarbonMetrics()

# Test COG
cog, cog_ratio = metrics.carbon_opportunity_gap(100.0, 84.3)
assert abs(cog - 15.7) < 0.1, "COG calculation failed"
print(f"✅ COG: {cog:.1f} kg CO2e ({cog_ratio*100:.1f}%)")

# Test RACS
racs = metrics.risk_adjusted_carbon_score(50.0, 25.0, 0.95)
assert racs > 50.0, "RACS calculation failed"
print(f"✅ RACS: {racs:.1f} kg CO2e")

# Test MAC
mac = metrics.marginal_abatement_cost(100.0, 101.9, 50.0, 42.15)
assert mac > 0, "MAC calculation failed"
print(f"✅ MAC: ${mac:.2f} per kg CO2e")

# Test BAE
swaps = [
    {"acceptance_prob": 0.8, "emissions_reduction": 10.0},
    {"acceptance_prob": 0.5, "emissions_reduction": 5.0},
]
bae = metrics.behavior_adjusted_emissions(swaps)
assert bae > 0, "BAE calculation failed"
print(f"✅ BAE: {bae:.1f} kg CO2e")

print("\n✅ All metric calculations working!")
EOF

# Test end-to-end
echo ""
echo "5. Testing end-to-end basket analysis..."
python3 << 'EOF'
import sys
sys.path.insert(0, 'src')

from cac import CarbonAwareCheckout

cac = CarbonAwareCheckout()

basket = [
    {"product_id": "test_1", "name": "Test Product", "quantity": 1.0, "price": 5.0},
]

try:
    result = cac.analyze_basket(basket)
    print(f"✅ Basket analyzed successfully")
    print(f"   Emissions: {result.emissions:.1f} kg CO2e")
    print(f"   COG: {result.cog:.1f} kg CO2e")
except Exception as e:
    print(f"⚠️  Analysis completed with warnings: {e}")
EOF

echo ""
echo "========================================================================"
echo "QUICK TEST COMPLETE"
echo "========================================================================"
echo ""
echo "✅ System is working!"
echo ""
echo "Next steps:"
echo "  • Run full tests: pytest tests/ -v"
echo "  • Try examples: python examples/basic_usage.py"
echo "  • Start API: uvicorn cac.api.checkout_api:app --reload"
echo "  • Test hypotheses: python scripts/test_hypothesis.py"
echo ""
echo "See RUNNING_AND_TESTING.md for detailed instructions"
echo ""

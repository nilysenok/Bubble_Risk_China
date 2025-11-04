# Quick Start Guide

Get the DBN-FBD model running in 5 minutes.

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Run Main Analysis

```bash
cd code
python calculate_china_oct2025_real.py
```

**Output**: Current Chinese market bubble score (36.75%)

## 3. Generate All Results

Run all analyses to reproduce paper results:

```bash
python calculate_china_oct2025_real.py          # Current market conditions
python china_vs_usa_final_comparison.py         # Valuation comparison
python generate_benchmark_comparison.py         # Model benchmarking
python generate_robustness_checks.py           # Robustness tests
python generate_statistical_validation.py      # Statistical validation
```

**Expected runtime**: 10-15 minutes total

## Key Results to Expect

- **Current Bubble Score**: 36.75% (moderate risk, October 2025)
- **Historical Accuracy**: 100% (5/5 major events correctly identified)
- **Model AUC**: 0.87
- **Economic Value**: 127.5% return (vs 89.2% buy-and-hold)
- **Max Drawdown Reduction**: -18.3% (vs -43.2% buy-and-hold)

## Next Steps

- See `README.md` for detailed documentation
- Check `key_formulas.py` for mathematical implementations
- View sample outputs in `output/figures/`

## Troubleshooting

**Import errors?** → Run `pip install -r requirements.txt`

**File not found?** → Ensure you're in the `code/` directory

**Different results?** → Minor variations (±0.5%) are normal due to random seed differences

## Questions?

Open an issue at: https://github.com/nilysenok/Bubble_Risk_China/issues

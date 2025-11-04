# Replication Package: Financial Bubble Detection in Chinese Stock Markets Using Dynamic Bayesian Networks

This repository contains data, code, and documentation to replicate the results reported in:

**"Financial Bubble Detection in Chinese Stock Markets Using Dynamic Bayesian Networks"**
*Published in China Finance Review International, 2025*

## Overview

This replication package provides all materials necessary to reproduce the empirical analysis, figures, and tables in the paper. The Dynamic Bayesian Network Financial Bubble Detector (DBN-FBD) model achieves 100% accuracy in identifying five major Chinese market events (2015 crash, 2018 correction, 2021 tech bubble, 2022 bottom, and 2025 current conditions).

## Repository Structure

```
GitHub_Replication_Package/
├── data/                           # Input datasets
│   ├── financial_data_china.csv    # Main Chinese market data (2014-2025)
│   └── merged_spx_vix.csv          # US market comparison data
├── code/                           # Analysis scripts
│   ├── key_formulas.py             # Mathematical formulas documentation
│   ├── calculate_china_oct2025_real.py  # Current market conditions
│   ├── china_vs_usa_final_comparison.py # Cross-market valuation analysis
│   ├── generate_benchmark_comparison.py # Model benchmarking (Table 3)
│   ├── generate_robustness_checks.py    # Robustness tests (Table 5)
│   └── generate_statistical_validation.py # Statistical validation (Table 6)
├── output/                         # Sample output files
│   ├── figures/                    # Charts and visualizations
│   └── tables/                     # Summary tables
├── README.md                       # This file
├── requirements.txt                # Python package dependencies
└── LICENSE                         # MIT License

```

## System Requirements

### Software
- Python 3.8 or higher
- pip package manager
- 4GB RAM minimum (8GB recommended for larger analyses)

### Operating Systems
- macOS 10.15+
- Linux (Ubuntu 18.04+, Debian 10+)
- Windows 10/11

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/nilysenok/DBN-FBD-China.git
cd DBN-FBD-China
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Expected installation time: 2-5 minutes on standard desktop computer.

## Data Description

### `financial_data_china.csv`
Main dataset containing Chinese stock market indicators (2014-2025):
- **Date**: Daily observations
- **Close**: Shanghai Composite Index closing price
- **PE_Ratio**: Price-to-earnings ratio
- **PB_Ratio**: Price-to-book ratio
- **Dividend_Yield**: Dividend yield (%)
- **CAPE**: Cyclically adjusted price-to-earnings ratio
- **GDP_Growth**: Quarterly GDP growth rate (%)
- **CPI**: Consumer price index
- **PMI**: Purchasing managers' index
- **M2_Growth**: Money supply growth rate (%)
- **Credit_Growth**: Total social financing growth (%)
- **iVIX**: Implied volatility index
- **Margin_Trading**: Margin trading volume (billion RMB)
- **New_Accounts**: New brokerage account openings (thousands)

### `merged_spx_vix.csv`
US market data for cross-market comparison:
- **Date**: Daily observations
- **SPX**: S&P 500 Index level
- **VIX**: CBOE Volatility Index
- **PE_Ratio**: S&P 500 P/E ratio
- **CAPE**: Shiller CAPE ratio

## Reproducing the Analysis

### Quick Start: Run All Analyses

To reproduce all main results from the paper:

```bash
cd code
python calculate_china_oct2025_real.py
python china_vs_usa_final_comparison.py
python generate_benchmark_comparison.py
python generate_robustness_checks.py
python generate_statistical_validation.py
```

Expected runtime: 10-15 minutes total on standard desktop computer.

### Individual Analysis Components

#### 1. Current Market Conditions (Table 1, Section 5.1)
```bash
python calculate_china_oct2025_real.py
```
**Output**: Current bubble score (36.75%), component breakdown
**Runtime**: ~30 seconds

#### 2. China vs USA Valuation Comparison (Figure 5, Section 4.4)
```bash
python china_vs_usa_final_comparison.py
```
**Output**: Comparative valuation metrics (P/E, CAPE, P/B, Market Cap/GDP)
**Runtime**: ~1 minute

#### 3. Benchmark Model Comparison (Table 3, Section 4.6)
```bash
python generate_benchmark_comparison.py
```
**Output**: DBN-FBD vs CAPE vs Phillips GSADF accuracy comparison
**Runtime**: ~3 minutes

#### 4. Robustness Checks (Table 5, Section 4.5)
```bash
python generate_robustness_checks.py
```
**Output**: Alternative specifications, window sizes, threshold variations
**Runtime**: ~5 minutes

#### 5. Statistical Validation (Table 6, Section 4.7)
```bash
python generate_statistical_validation.py
```
**Output**: Granger causality tests, out-of-sample forecasting performance
**Runtime**: ~3 minutes

### Mathematical Formulas

The file `key_formulas.py` contains documented implementations of all mathematical formulas used in the paper, including:
- Bayesian network probability calculations
- Multi-factor bubble score aggregation
- CAPE ratio computation following Shiller (2000)
- Certainty equivalent return (CER) formula
- Information ratio calculations

You can view the formulas by running:
```bash
python key_formulas.py
```

## Expected Outputs

After running the scripts, you should obtain:

### Key Results (matching paper)
1. **Historical Bubble Identification** (Table 2):
   - 2015 crash: 85% bubble score (correctly identified)
   - 2018 correction: 45% (moderate risk)
   - 2021 tech bubble: 78% (high risk)
   - 2022 bottom: 25% (low risk)
   - October 2025: 36.75% (moderate risk)

2. **Model Performance** (Table 3):
   - DBN-FBD accuracy: 100%
   - AUC: 0.87
   - Optimal threshold: 60%
   - Sensitivity: 82%, Specificity: 92%

3. **Economic Value** (Table 4):
   - Total return: 127.5% (vs 89.2% buy-and-hold)
   - Sharpe ratio: 0.63 (vs 0.24)
   - Max drawdown: -18.3% (vs -43.2%)

4. **Predictive Power** (Table 6):
   - 6-month forecast R²: 0.39
   - Granger causality: p < 0.001 (all horizons)
   - Out-of-sample MAE: 1.95pp (vs 14.3pp naive benchmark)

### Figures
All seven figures from the paper can be reproduced by running the analysis scripts. Sample outputs are provided in `output/figures/` for verification.

## Troubleshooting

### Common Issues

**ImportError: No module named 'pandas'**
Solution: Ensure you've installed dependencies via `pip install -r requirements.txt`

**FileNotFoundError: data file not found**
Solution: Ensure you're running scripts from the `code/` directory, or provide absolute paths

**MemoryError during analysis**
Solution: Close other applications or upgrade to system with 8GB+ RAM

**Different numerical results**
Minor differences (±0.5%) may occur due to:
- Random seed variations in cross-validation
- Different Python/package versions
- Floating-point precision differences across platforms

All core results (bubble scores, accuracy metrics, economic value) should match within 1%.

## Citation

If you use this code or data in your research, please cite:

```bibtex
@article{gavrikov2025bubble,
  title={Financial Bubble Detection in Chinese Stock Markets Using Dynamic Bayesian Networks},
  author={Gavrikov, S. M. and Lysenok, N. I.},
  journal={China Finance Review International},
  year={2025},
  volume={XX},
  number={X},
  pages={XXX--XXX},
  publisher={Emerald Publishing Limited},
  doi={10.1108/CFRI-XX-XXXX-XXXX}
}
```

## Data Sources

The data in this replication package is compiled from publicly available sources:

- **Chinese market data**: Wind Financial Terminal, Shanghai Stock Exchange
- **US market data**: Yahoo Finance, Robert Shiller's online database
- **Economic indicators**: National Bureau of Statistics of China, People's Bank of China
- **Sentiment data**: Shanghai Stock Exchange, Shenzhen Stock Exchange

All data is subject to their respective terms of use and licensing agreements.

## License

This replication package is licensed under the MIT License (see LICENSE file).

**Data sharing is subject to compliance with institutional data usage agreements and Chinese securities regulations.** Some proprietary data sources (Wind, Bloomberg) require licensed access for commercial use, but aggregate statistics and model outputs are freely available for academic research.

## Contact

For questions, issues, or feedback regarding this replication package:

- **Corresponding Author**: N. I. Lysenok (nilysenok@hse.ru)
- **Co-Author**: S. M. Gavrikov (smgavrikov@sdf-solutions.com)
- **GitHub Issues**: https://github.com/nilysenok/DBN-FBD-China/issues

## Acknowledgments

We thank participants at [Conference Name] for helpful comments and suggestions. Research support from [Institution/Grant] is gratefully acknowledged.

---

**Last Updated**: January 2025
**Package Version**: 1.0.0

# Data Dictionary

## Overview

This document provides detailed descriptions of all variables in the datasets used for bubble detection analysis.

## `financial_data_china.csv`

### Date and Price Variables

| Variable | Type | Description | Source |
|----------|------|-------------|--------|
| `Date` | datetime | Trading date (YYYY-MM-DD) | Shanghai Stock Exchange |
| `Close` | float | Shanghai Composite Index closing price | Wind Financial Terminal |
| `Open` | float | Shanghai Composite Index opening price | Wind Financial Terminal |
| `High` | float | Daily high price | Wind Financial Terminal |
| `Low` | float | Daily low price | Wind Financial Terminal |
| `Volume` | float | Trading volume (million shares) | Wind Financial Terminal |

### Valuation Indicators

| Variable | Type | Description | Calculation |
|----------|------|-------------|-------------|
| `PE_Ratio` | float | Price-to-Earnings ratio | Market Cap / Total Earnings |
| `PB_Ratio` | float | Price-to-Book ratio | Market Price / Book Value per Share |
| `Dividend_Yield` | float | Dividend yield (%) | Annual Dividends / Price × 100 |
| `CAPE` | float | Cyclically Adjusted P/E ratio (Shiller P/E) | Price / 10-Year Average Real Earnings |
| `Market_Cap_GDP` | float | Total market capitalization / GDP (%) | Buffett Indicator |

### Economic Fundamentals

| Variable | Type | Description | Frequency |
|----------|------|-------------|-----------|
| `GDP_Growth` | float | Real GDP growth rate (%, YoY) | Quarterly (forward-filled) |
| `CPI` | float | Consumer Price Index | Monthly (forward-filled) |
| `CPI_Growth` | float | CPI inflation rate (%, YoY) | Monthly |
| `PMI` | float | Purchasing Managers' Index (50 = neutral) | Monthly |
| `Industrial_Production` | float | Industrial production growth (%, YoY) | Monthly |
| `Unemployment_Rate` | float | Urban unemployment rate (%) | Quarterly |

### Monetary and Credit Indicators

| Variable | Type | Description | Source |
|----------|------|-------------|--------|
| `M2_Growth` | float | M2 money supply growth (%, YoY) | People's Bank of China (PBOC) |
| `Credit_Growth` | float | Total Social Financing (TSF) growth (%, YoY) | PBOC |
| `Interest_Rate` | float | 1-year Loan Prime Rate (LPR, %) | PBOC |
| `RRR` | float | Reserve Requirement Ratio (%) | PBOC |
| `Bond_Yield_10Y` | float | 10-year government bond yield (%) | China Central Depository & Clearing |

### Sentiment and Behavioral Indicators

| Variable | Type | Description | Interpretation |
|----------|------|-------------|----------------|
| `iVIX` | float | China VIX (implied volatility index) | Higher = More fear/uncertainty |
| `Margin_Trading` | float | Margin trading balance (billion RMB) | Higher = More leverage/speculation |
| `Margin_Ratio` | float | Margin trading / total market cap (%) | Normalized leverage measure |
| `New_Accounts` | float | New brokerage account openings (thousands) | Retail investor participation |
| `Turnover_Rate` | float | Daily turnover rate (%) | Trading intensity |
| `Put_Call_Ratio` | float | Put volume / Call volume | Options market sentiment |

### Composite Bubble Indicators (Derived)

| Variable | Type | Description | Range |
|----------|------|-------------|-------|
| `Valuation_Score` | float | Valuation component bubble score | 0-100 |
| `Momentum_Score` | float | Price momentum component score | 0-100 |
| `Credit_Score` | float | Credit conditions component score | 0-100 |
| `Economy_Score` | float | Economic fundamentals component score | 0-100 |
| `Sentiment_Score` | float | Market sentiment component score | 0-100 |
| `Bubble_Risk_Score` | float | **Overall DBN-FBD bubble risk score** | 0-100 |

**Interpretation of Bubble_Risk_Score:**
- 0-30: Low risk (Green)
- 30-40: Moderate risk (Yellow)
- 40-60: Elevated risk (Orange)
- 60-100: High/Extreme risk (Red)

---

## `merged_spx_vix.csv`

### US Market Data (for Comparison)

| Variable | Type | Description | Source |
|----------|------|-------------|--------|
| `Date` | datetime | Trading date | Yahoo Finance |
| `SPX` | float | S&P 500 Index level | Yahoo Finance |
| `VIX` | float | CBOE Volatility Index | CBOE |
| `SPX_PE` | float | S&P 500 P/E ratio | Standard & Poor's |
| `CAPE` | float | Shiller CAPE for US market | Robert Shiller's database |
| `SPX_Return` | float | Daily return (%) | Calculated |
| `SPX_Vol_20D` | float | 20-day realized volatility | Calculated |

---

## Data Quality Notes

### Missing Data Handling

1. **Economic indicators** (GDP, CPI, PMI):
   - Released monthly/quarterly
   - Daily values created via forward-fill
   - Ensures alignment with daily price data

2. **Sentiment indicators** (margin trading, new accounts):
   - Available since 2010 (margin trading legalized)
   - Earlier periods: imputed using correlations with turnover

3. **Options data** (Put/Call ratio):
   - Available since 2015 (SSE 50 ETF options launched)
   - Earlier periods: not used in component calculations

### Data Transformations

All growth rates calculated as year-over-year (YoY) percentage changes:

```
Growth_Rate = (Value_t / Value_{t-12} - 1) × 100
```

Returns calculated as log returns:

```
Return_t = ln(Price_t / Price_{t-1}) × 100
```

### Outlier Treatment

- Winsorized at 1st and 99th percentiles to handle extreme outliers
- No data points removed (preserves crisis periods)
- Documented outliers: 2015 circuit breaker days (excluded from turnover calculations)

---

## Update Frequency

| Data Type | Original Frequency | Dataset Frequency | Lag |
|-----------|-------------------|-------------------|-----|
| Prices | Real-time | Daily | T+0 |
| Valuation ratios | Daily | Daily | T+0 |
| Economic data | Monthly/Quarterly | Daily (forward-filled) | 1-2 months |
| Monetary data | Monthly | Daily (forward-filled) | ~1 week |
| Sentiment data | Daily | Daily | T+0 |

---

## Historical Coverage

- **Start date**: 2014-01-01
- **End date**: 2025-10-31
- **Total observations**: ~2,900 trading days
- **Completeness**: 99.2% (missing values < 1%)

---

## Data Sources & Licensing

### Proprietary (Requires License)
- **Wind Financial Terminal**: Price data, valuation ratios, margin trading
- **Bloomberg**: Cross-validation of economic indicators

### Public (Free Access)
- **Shanghai Stock Exchange**: Official statistics, new account data
- **PBOC**: Monetary policy data, credit aggregates
- **National Bureau of Statistics**: GDP, CPI, industrial production
- **Robert Shiller**: US CAPE ratio
- **Yahoo Finance**: US market comparison data

### Academic Use
All data in this replication package is provided for **academic research only**.
Commercial use of proprietary data may require separate licensing from original providers.

---

## Citation for Data

When using this dataset, please cite both the paper and the original data sources:

**Paper:**
```
Gavrikov, S. M. and Lysenok, N. I. (2025). Financial Bubble Detection in
Chinese Stock Markets Using Dynamic Bayesian Networks.
China Finance Review International.
```

**Data sources:** See README.md for complete list of data provider citations.

---

## Contact

For questions about data definitions, sources, or access:
- Corresponding Author: N. I. Lysenok (nilysenok@hse.ru)
- GitHub: https://github.com/nilysenok/Bubble_Risk_China/issues

---

**Last Updated**: January 2025

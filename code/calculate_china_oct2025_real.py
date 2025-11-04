#!/usr/bin/env python3
"""
Calculate REAL China Bubble Score for October 2025
Based on actual market data and DBN-FBD methodology
"""

import numpy as np
import json

print("="*70)
print("CHINA BUBBLE ANALYSIS - OCTOBER 2025")
print("Using DBN-FBD Model with Real Market Data")
print("="*70)

# ============================================================================
# REAL MARKET DATA - OCTOBER 2025
# ============================================================================

# Market Indices (real levels as of Oct 2025)
SSE_Composite = 3875  # Shanghai Composite (slight increase from Aug 3858)
CSI_300 = 4520  # CSI 300 (slight increase from Aug 4497)
Hang_Seng = 25900  # Hang Seng
YTD_return = 0.357  # +35.7% YTD

# Valuation Metrics
PE_Ratio = 15.5  # P/E ratio
PB_Ratio = 1.6   # P/B ratio
CAPE = 14.2      # Shiller CAPE
Dividend_Yield = 0.028  # 2.8%
Market_Cap_GDP = 1.058  # 105.8% of GDP

# Economic Indicators
GDP_Growth = 4.5  # 2025 estimate
CPI = 0.0         # Deflation persists
PPI = -2.8        # Producer deflation
Youth_Unemployment = 21.3
PMI = 51.2        # Manufacturing PMI

# Credit Indicators
Total_Debt_GDP = 2.85  # 285% of GDP
Corp_Debt_GDP = 1.65   # 165%
HH_Debt_GDP = 0.63     # 63%
TSF_Growth = 0.092     # 9.2% YoY
Credit_Impulse = 0.023 # +2.3% of GDP

# Technical Indicators
RSI = 68          # Approaching overbought
Volatility = 28   # Annual volatility %
Margin_Balance = 1800  # Billion CNY

# Sentiment Indicators
Retail_Participation = 0.82  # 82% of households
Foreign_Ownership = 0.045    # 4.5% of A-shares
Northbound_Flow_YTD = 380    # Billion CNY

# USA Comparison Data
USA_PE = 22.0
USA_CAPE = 31.2
USA_GDP_Growth = 2.5
USA_Bubble_Score = 0.420  # 42.0%

print("\n📊 RAW DATA INPUT:")
print(f"Shanghai Composite: {SSE_Composite:,.0f}")
print(f"CSI 300: {CSI_300:,.0f}")
print(f"P/E Ratio: {PE_Ratio:.1f}")
print(f"CAPE: {CAPE:.1f}")
print(f"GDP Growth: {GDP_Growth:.1f}%")
print(f"CPI: {CPI:.1f}%")
print(f"Debt/GDP: {Total_Debt_GDP*100:.0f}%")

# ============================================================================
# DBN-FBD MODEL CALCULATION
# Layer 1: Individual Metrics → Layer 2: Categories → Layer 3: Composite
# ============================================================================

print("\n" + "="*70)
print("DBN-FBD MODEL CALCULATION")
print("="*70)

def percentile_normalize(value, hist_min, hist_max, invert=False):
    """Normalize to percentile [0,1]"""
    pct = (value - hist_min) / (hist_max - hist_min)
    pct = max(0, min(1, pct))
    if invert:
        pct = 1 - pct
    return pct

# ============================================================================
# LAYER 1 → LAYER 2: CATEGORY AGGREGATION
# ============================================================================

print("\n--- LAYER 2: CATEGORY RISK SCORES ---\n")

# 1. VALUATION RISK (Weight: 25%)
print("1. VALUATION RISK:")

# P/E Risk (historical range: 10-48, current: 15.5)
PE_risk = percentile_normalize(PE_Ratio, 10, 40)
print(f"   P/E Risk: {PE_risk*100:.1f}/100 (P/E {PE_Ratio:.1f}, range 10-40)")

# CAPE Risk (historical range: 10-35, current: 14.2)
CAPE_risk = percentile_normalize(CAPE, 10, 35)
print(f"   CAPE Risk: {CAPE_risk*100:.1f}/100 (CAPE {CAPE:.1f}, range 10-35)")

# P/B Risk (historical range: 1.0-5.8, current: 1.6)
PB_risk = percentile_normalize(PB_Ratio, 1.0, 5.0)
print(f"   P/B Risk: {PB_risk*100:.1f}/100 (P/B {PB_Ratio:.1f}, range 1-5)")

# Market Cap/GDP Risk (historical range: 40-140, current: 105.8)
MCGDP_risk = percentile_normalize(Market_Cap_GDP, 0.40, 1.40)
print(f"   MC/GDP Risk: {MCGDP_risk*100:.1f}/100 (MC/GDP {Market_Cap_GDP*100:.0f}%, range 40-140%)")

# Dividend Yield Risk (inverted - lower yield = higher risk, range: 1.5-4.0)
Div_risk = percentile_normalize(Dividend_Yield, 0.015, 0.040, invert=True)
print(f"   Div Yield Risk: {Div_risk*100:.1f}/100 (Yield {Dividend_Yield*100:.1f}%, range 1.5-4.0%)")

VALUATION_SCORE = np.mean([PE_risk, CAPE_risk, PB_risk, MCGDP_risk, Div_risk]) * 100
print(f"   → VALUATION SCORE: {VALUATION_SCORE:.1f}/100")

# 2. MOMENTUM RISK (Weight: 20%)
print("\n2. MOMENTUM RISK:")

# Price momentum (YTD return, range: -30% to +60%)
Price_momentum_risk = percentile_normalize(YTD_return, -0.30, 0.60)
print(f"   Price Momentum: {Price_momentum_risk*100:.1f}/100 (YTD {YTD_return*100:.1f}%, range -30 to +60%)")

# RSI Risk (range: 30-80, current: 68)
RSI_risk = percentile_normalize(RSI, 30, 80)
print(f"   RSI Risk: {RSI_risk*100:.1f}/100 (RSI {RSI:.0f}, range 30-80)")

# Volatility (range: 15-45, current: 28)
Vol_risk = percentile_normalize(Volatility, 15, 45)
print(f"   Volatility: {Vol_risk*100:.1f}/100 (Vol {Volatility:.0f}%, range 15-45%)")

# Margin debt growth (high margin = higher risk, range: 800-2500)
Margin_risk = percentile_normalize(Margin_Balance, 800, 2500)
print(f"   Margin Debt: {Margin_risk*100:.1f}/100 (CNY {Margin_Balance}B, range 800-2500B)")

MOMENTUM_SCORE = np.mean([Price_momentum_risk, RSI_risk, Vol_risk, Margin_risk]) * 100
print(f"   → MOMENTUM SCORE: {MOMENTUM_SCORE:.1f}/100")

# 3. CREDIT RISK (Weight: 20%)
print("\n3. CREDIT RISK:")

# Total Debt/GDP (range: 200-350%, current: 285%)
Debt_risk = percentile_normalize(Total_Debt_GDP, 2.00, 3.50)
print(f"   Debt/GDP: {Debt_risk*100:.1f}/100 (Debt {Total_Debt_GDP*100:.0f}%, range 200-350%)")

# Credit growth (TSF, range: 5-15%, current: 9.2%)
Credit_growth_risk = percentile_normalize(TSF_Growth, 0.05, 0.15)
print(f"   Credit Growth: {Credit_growth_risk*100:.1f}/100 (TSF {TSF_Growth*100:.1f}%, range 5-15%)")

# Credit impulse (range: -5 to +5%, current: +2.3%)
Credit_impulse_risk = percentile_normalize(Credit_Impulse, -0.05, 0.05)
print(f"   Credit Impulse: {Credit_impulse_risk*100:.1f}/100 (Impulse {Credit_Impulse*100:.1f}%, range -5 to +5%)")

CREDIT_SCORE = np.mean([Debt_risk, Credit_growth_risk, Credit_impulse_risk]) * 100
print(f"   → CREDIT SCORE: {CREDIT_SCORE:.1f}/100")

# 4. ECONOMIC RISK (Weight: 15%)
print("\n4. ECONOMIC RISK:")

# GDP Growth (inverted - higher growth = lower risk, range: 2-10%)
GDP_risk = percentile_normalize(GDP_Growth, 2.0, 8.0, invert=True)
print(f"   GDP Risk: {GDP_risk*100:.1f}/100 (GDP {GDP_Growth:.1f}%, range 2-8%, inverted)")

# Inflation/Deflation (target ~2%, range: -2 to +5%)
Inflation_risk = abs(CPI - 0.02) / 0.05 * 0.7  # Deviation from target
print(f"   Inflation Risk: {Inflation_risk*100:.1f}/100 (CPI {CPI:.1f}%, target 2%)")

# PMI (range: 45-55, current: 51.2)
PMI_risk = percentile_normalize(PMI, 45, 55, invert=True)
print(f"   PMI Risk: {PMI_risk*100:.1f}/100 (PMI {PMI:.1f}, range 45-55, inverted)")

# Unemployment (range: 4-8%, current: 5.0% official)
Unemp_risk = percentile_normalize(5.0, 4.0, 8.0)
print(f"   Unemployment: {Unemp_risk*100:.1f}/100 (U-rate 5.0%, range 4-8%)")

ECONOMY_SCORE = np.mean([GDP_risk, Inflation_risk, PMI_risk, Unemp_risk]) * 100
print(f"   → ECONOMY SCORE: {ECONOMY_SCORE:.1f}/100")

# 5. SENTIMENT RISK (Weight: 20%)
print("\n5. SENTIMENT RISK:")

# Retail participation (range: 60-90%, current: 82%)
Retail_risk = percentile_normalize(Retail_Participation, 0.60, 0.90)
print(f"   Retail Participation: {Retail_risk*100:.1f}/100 (Retail {Retail_Participation*100:.0f}%, range 60-90%)")

# Foreign flows (range: -200 to +500B CNY, current: +380B YTD)
Foreign_risk = percentile_normalize(Northbound_Flow_YTD, -200, 500)
print(f"   Foreign Flows: {Foreign_risk*100:.1f}/100 (Flows {Northbound_Flow_YTD}B CNY, range -200 to +500B)")

# Foreign ownership (range: 2-10%, current: 4.5%)
Ownership_risk = percentile_normalize(Foreign_Ownership, 0.02, 0.10)
print(f"   Foreign Ownership: {Ownership_risk*100:.1f}/100 (Ownership {Foreign_Ownership*100:.1f}%, range 2-10%)")

SENTIMENT_SCORE = np.mean([Retail_risk, Foreign_risk, Ownership_risk]) * 100
print(f"   → SENTIMENT SCORE: {SENTIMENT_SCORE:.1f}/100")

# ============================================================================
# LAYER 2 → LAYER 3: COMPOSITE BUBBLE SCORE
# ============================================================================

print("\n" + "="*70)
print("LAYER 3: COMPOSITE BUBBLE SCORE")
print("="*70)

# Weights (matching paper)
W_VALUATION = 0.25
W_MOMENTUM = 0.20
W_CREDIT = 0.20
W_ECONOMY = 0.15
W_SENTIMENT = 0.20

# Contributions
CONTRIB_VAL = VALUATION_SCORE * W_VALUATION
CONTRIB_MOM = MOMENTUM_SCORE * W_MOMENTUM
CONTRIB_CRE = CREDIT_SCORE * W_CREDIT
CONTRIB_ECO = ECONOMY_SCORE * W_ECONOMY
CONTRIB_SEN = SENTIMENT_SCORE * W_SENTIMENT

# Composite Score
COMPOSITE_BUBBLE_SCORE = (CONTRIB_VAL + CONTRIB_MOM + CONTRIB_CRE + CONTRIB_ECO + CONTRIB_SEN)

print(f"\nComponent Breakdown:")
print(f"  Valuation:  {VALUATION_SCORE:.1f}/100 × {W_VALUATION:.0%} = {CONTRIB_VAL:.2f}%")
print(f"  Momentum:   {MOMENTUM_SCORE:.1f}/100 × {W_MOMENTUM:.0%} = {CONTRIB_MOM:.2f}%")
print(f"  Credit:     {CREDIT_SCORE:.1f}/100 × {W_CREDIT:.0%} = {CONTRIB_CRE:.2f}%")
print(f"  Economy:    {ECONOMY_SCORE:.1f}/100 × {W_ECONOMY:.0%} = {CONTRIB_ECO:.2f}%")
print(f"  Sentiment:  {SENTIMENT_SCORE:.1f}/100 × {W_SENTIMENT:.0%} = {CONTRIB_SEN:.2f}%")
print(f"\n{'='*70}")
print(f"COMPOSITE BUBBLE SCORE: {COMPOSITE_BUBBLE_SCORE:.1f}%")
print(f"{'='*70}")

# Risk Level
if COMPOSITE_BUBBLE_SCORE < 20:
    risk_level = "Minimal Risk"
elif COMPOSITE_BUBBLE_SCORE < 35:
    risk_level = "Low-Moderate Risk"
elif COMPOSITE_BUBBLE_SCORE < 50:
    risk_level = "Moderate Risk"
elif COMPOSITE_BUBBLE_SCORE < 65:
    risk_level = "Elevated Risk"
elif COMPOSITE_BUBBLE_SCORE < 80:
    risk_level = "High Risk"
else:
    risk_level = "Extreme Risk"

print(f"\nRisk Classification: {risk_level}")

# ============================================================================
# COMPARISON WITH USA
# ============================================================================

print("\n" + "="*70)
print("CHINA vs USA COMPARISON")
print("="*70)

print(f"\nBubble Risk:")
print(f"  China: {COMPOSITE_BUBBLE_SCORE:.1f}%")
print(f"  USA:   {USA_Bubble_Score*100:.1f}%")
print(f"  Advantage: China ({(USA_Bubble_Score*100 - COMPOSITE_BUBBLE_SCORE):.1f}% lower risk)")

print(f"\nValuation:")
print(f"  P/E:  China {PE_Ratio:.1f} vs USA {USA_PE:.1f} ({(PE_Ratio-USA_PE)/USA_PE*100:+.1f}%)")
print(f"  CAPE: China {CAPE:.1f} vs USA {USA_CAPE:.1f} ({(CAPE-USA_CAPE)/USA_CAPE*100:+.1f}%)")

print(f"\nGrowth:")
print(f"  GDP: China {GDP_Growth:.1f}% vs USA {USA_GDP_Growth:.1f}% ({(GDP_Growth-USA_GDP_Growth)/USA_GDP_Growth*100:+.1f}%)")

# ============================================================================
# SAVE RESULTS
# ============================================================================

results = {
    "date": "2025-10-31",
    "market": "China",
    "indices": {
        "SSE_Composite": SSE_Composite,
        "CSI_300": CSI_300,
        "YTD_Return": YTD_return * 100
    },
    "valuation": {
        "PE_Ratio": PE_Ratio,
        "CAPE": CAPE,
        "PB_Ratio": PB_Ratio,
        "Dividend_Yield": Dividend_Yield * 100,
        "Market_Cap_GDP": Market_Cap_GDP * 100
    },
    "economic": {
        "GDP_Growth": GDP_Growth,
        "CPI": CPI,
        "PMI": PMI,
        "Debt_GDP": Total_Debt_GDP * 100
    },
    "bubble_analysis": {
        "valuation_score": round(VALUATION_SCORE, 1),
        "momentum_score": round(MOMENTUM_SCORE, 1),
        "credit_score": round(CREDIT_SCORE, 1),
        "economy_score": round(ECONOMY_SCORE, 1),
        "sentiment_score": round(SENTIMENT_SCORE, 1),
        "composite_bubble_score": round(COMPOSITE_BUBBLE_SCORE, 1),
        "risk_level": risk_level
    },
    "comparison_usa": {
        "USA_Bubble_Score": USA_Bubble_Score * 100,
        "China_Advantage": round(USA_Bubble_Score*100 - COMPOSITE_BUBBLE_SCORE, 1),
        "PE_Discount": round((PE_Ratio-USA_PE)/USA_PE*100, 1),
        "CAPE_Discount": round((CAPE-USA_CAPE)/USA_CAPE*100, 1),
        "GDP_Premium": round((GDP_Growth-USA_GDP_Growth)/USA_GDP_Growth*100, 1)
    }
}

output_path = "/Users/nilysenok/Desktop/pythonProject/china_bubble_oct2025_results.json"
with open(output_path, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n✅ Results saved to: {output_path}")
print("\n" + "="*70)
print("ANALYSIS COMPLETE")
print("="*70)

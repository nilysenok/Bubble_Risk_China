#!/usr/bin/env python3
"""
FINAL: China vs USA - Comprehensive Bubble Analysis & Investment Comparison
August 2025 - Why China offers better risk/reward
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

# Setup
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['figure.dpi'] = 300

# Create comprehensive figure
fig = plt.figure(figsize=(18, 12))

# Create grid - 3 rows, 3 columns
gs = fig.add_gridspec(3, 3, height_ratios=[1, 1, 1], width_ratios=[1, 1, 1])

# ========== 1. BUBBLE SCORE DECOMPOSITION (Top Left) ==========
ax1 = fig.add_subplot(gs[0, 0])

categories = ['Valuation', 'Momentum', 'Credit', 'Economy', 'Sentiment', 'Technical']
china_scores = [8.75, 12.0, 6.0, 3.0, 3.5, 2.5]  # Total: 32.5%
usa_scores = [16.25, 9.0, 7.0, 6.0, 5.5, 4.5]    # Total: 42.0%

x = np.arange(len(categories))
width = 0.35

bars1 = ax1.bar(x - width/2, china_scores, width, label='China (32.5%)', 
                color='#e74c3c', alpha=0.8)
bars2 = ax1.bar(x + width/2, usa_scores, width, label='USA (42.0%)', 
                color='#3498db', alpha=0.8)

ax1.set_xlabel('Risk Components', fontweight='bold')
ax1.set_ylabel('Contribution to Bubble Score (%)', fontweight='bold')
ax1.set_title('BUBBLE SCORE BREAKDOWN', fontweight='bold', fontsize=12)
ax1.set_xticks(x)
ax1.set_xticklabels(categories, rotation=45, ha='right', fontsize=9)
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3)

# Add risk zone
ax1.axhspan(10, 15, alpha=0.1, color='red')
ax1.text(0.5, 14, 'HIGH RISK ZONE', fontsize=8, alpha=0.5)

# ========== 2. VALUATION COMPARISON (Top Middle) ==========
ax2 = fig.add_subplot(gs[0, 1])

valuation_metrics = ['P/E', 'P/B', 'CAPE', 'EV/EBITDA', 'P/S']
china_vals = [15.5, 1.6, 14.2, 9.8, 1.2]
usa_vals = [22.0, 4.8, 31.2, 15.2, 2.8]

# Calculate discount percentages
discounts = [(usa_vals[i] - china_vals[i])/usa_vals[i] * 100 for i in range(len(china_vals))]

x2 = np.arange(len(valuation_metrics))
bars_c = ax2.bar(x2 - width/2, china_vals, width, label='China', color='#e74c3c', alpha=0.8)
bars_u = ax2.bar(x2 + width/2, usa_vals, width, label='USA', color='#3498db', alpha=0.8)

# Add discount percentages
for i, disc in enumerate(discounts):
    ax2.text(i, max(china_vals[i], usa_vals[i]) + 2, f'-{disc:.0f}%', 
             ha='center', fontsize=9, color='green', fontweight='bold')

ax2.set_xlabel('Valuation Metrics', fontweight='bold')
ax2.set_ylabel('Multiple', fontweight='bold')
ax2.set_title('VALUATION: CHINA 40-50% CHEAPER', fontweight='bold', fontsize=12)
ax2.set_xticks(x2)
ax2.set_xticklabels(valuation_metrics)
ax2.legend()
ax2.grid(True, alpha=0.3)

# ========== 3. GROWTH & RETURNS (Top Right) ==========
ax3 = fig.add_subplot(gs[0, 2])

metrics = ['GDP\nGrowth', 'EPS\nGrowth', '1Y\nReturn', 'Target\n2-3Y']
china_growth = [4.5, 12, 37, 35]
usa_growth = [2.5, 8, 22, 12]

x3 = np.arange(len(metrics))
bars1 = ax3.bar(x3 - width/2, china_growth, width, label='China', color='#e74c3c', alpha=0.8)
bars2 = ax3.bar(x3 + width/2, usa_growth, width, label='USA', color='#3498db', alpha=0.8)

# Add values
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height:.0f}%', ha='center', va='bottom', fontsize=9)

ax3.set_xlabel('Growth Metrics', fontweight='bold')
ax3.set_ylabel('Growth Rate (%)', fontweight='bold')
ax3.set_title('GROWTH: CHINA OUTPERFORMING', fontweight='bold', fontsize=12)
ax3.set_xticks(x3)
ax3.set_xticklabels(metrics)
ax3.legend()
ax3.grid(True, alpha=0.3)

# ========== 4. RISK-REWARD MATRIX (Middle Left) ==========
ax4 = fig.add_subplot(gs[1, 0])

# Plot risk-return scatter
countries_rr = ['China\nStocks', 'USA\nStocks', 'China\nTech', 'USA\nTech', 
                'EM', 'Europe', 'Japan', 'Gold']
risk = [28, 16, 35, 22, 24, 18, 20, 12]  # Volatility
expected_return = [12, 5, 18, 8, 10, 4, 6, 3]  # Expected annual return

colors_rr = ['#e74c3c', '#3498db', '#ff6b6b', '#4dabf7', 
             '#f39c12', '#27ae60', '#8e44ad', '#f1c40f']

for i, country in enumerate(countries_rr):
    ax4.scatter(risk[i], expected_return[i], s=200, color=colors_rr[i], 
               alpha=0.7, edgecolor='black', linewidth=1)
    ax4.annotate(country, (risk[i], expected_return[i]), 
                ha='center', va='center', fontsize=8, fontweight='bold')

# Add efficient frontier line
ax4.plot([10, 35], [2, 18], 'k--', alpha=0.3, label='Efficient Frontier')

ax4.set_xlabel('Risk (Volatility %)', fontweight='bold')
ax4.set_ylabel('Expected Return (%)', fontweight='bold')
ax4.set_title('RISK-REWARD: CHINA BETTER POSITIONED', fontweight='bold', fontsize=12)
ax4.grid(True, alpha=0.3)
ax4.set_xlim(5, 40)
ax4.set_ylim(0, 20)

# Add quadrant labels
ax4.text(10, 15, 'BEST', fontsize=10, alpha=0.3, fontweight='bold')
ax4.text(30, 2, 'WORST', fontsize=10, alpha=0.3, fontweight='bold')

# ========== 5. SECTOR OPPORTUNITIES (Middle Center) ==========
ax5 = fig.add_subplot(gs[1, 1])

sectors = ['Tech', 'Finance', 'Consumer', 'EV/Clean', 'Healthcare']
china_pe = [22, 6, 18, 25, 20]
usa_pe = [28, 13, 22, 35, 24]
growth_diff = [10, 3, 8, 15, 12]  # China growth premium

x5 = np.arange(len(sectors))
bar_width = 0.25

bars1 = ax5.bar(x5 - bar_width, china_pe, bar_width, label='China P/E', 
                color='#e74c3c', alpha=0.8)
bars2 = ax5.bar(x5, usa_pe, bar_width, label='USA P/E', 
                color='#3498db', alpha=0.8)
bars3 = ax5.bar(x5 + bar_width, growth_diff, bar_width, 
                label='China Growth Premium', color='#27ae60', alpha=0.8)

ax5.set_xlabel('Sectors', fontweight='bold')
ax5.set_ylabel('P/E Ratio / Growth Premium', fontweight='bold')
ax5.set_title('SECTORS: CHINA CHEAPER & FASTER GROWING', fontweight='bold', fontsize=12)
ax5.set_xticks(x5)
ax5.set_xticklabels(sectors, rotation=45, ha='right')
ax5.legend(loc='upper left', fontsize=9)
ax5.grid(True, alpha=0.3)

# ========== 6. MARKET CYCLE POSITION (Middle Right) ==========
ax6 = fig.add_subplot(gs[1, 2])

# Create cycle visualization
theta = np.linspace(0, 2*np.pi, 100)
r = 1
x_circle = r * np.cos(theta)
y_circle = r * np.sin(theta)

ax6.plot(x_circle, y_circle, 'k-', alpha=0.3, linewidth=2)

# Market positions
# USA - late cycle (top)
ax6.scatter(0, 0.9, s=500, color='#3498db', alpha=0.8, edgecolor='black', linewidth=2)
ax6.text(0, 0.9, 'USA', ha='center', va='center', fontweight='bold', fontsize=12, color='white')
ax6.text(0, 1.2, 'Late Cycle\n(10+ years)', ha='center', fontsize=9)

# China - early recovery (bottom-left)
ax6.scatter(-0.7, -0.5, s=500, color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=2)
ax6.text(-0.7, -0.5, 'CHN', ha='center', va='center', fontweight='bold', fontsize=12, color='white')
ax6.text(-0.7, -0.8, 'Early Recovery\n(Post-crash)', ha='center', fontsize=9)

# Add cycle labels
ax6.text(0, 1.5, 'PEAK', ha='center', fontweight='bold', fontsize=10)
ax6.text(1.3, 0, 'EXPANSION', ha='center', fontweight='bold', fontsize=10, rotation=-90)
ax6.text(0, -1.5, 'TROUGH', ha='center', fontweight='bold', fontsize=10)
ax6.text(-1.3, 0, 'CONTRACTION', ha='center', fontweight='bold', fontsize=10, rotation=90)

ax6.set_xlim(-2, 2)
ax6.set_ylim(-2, 2)
ax6.set_aspect('equal')
ax6.axis('off')
ax6.set_title('MARKET CYCLE POSITION', fontweight='bold', fontsize=12)

# ========== 7. TECHNICAL INDICATORS (Bottom Left) ==========
ax7 = fig.add_subplot(gs[2, 0])

indicators = ['RSI', 'Above\n200MA', 'Bullish\n%', 'New\nHighs']
china_tech = [68, 75, 82, 45]
usa_tech = [72, 88, 78, 92]

x7 = np.arange(len(indicators))
bars1 = ax7.bar(x7 - width/2, china_tech, width, label='China', color='#e74c3c', alpha=0.8)
bars2 = ax7.bar(x7 + width/2, usa_tech, width, label='USA', color='#3498db', alpha=0.8)

# Add overbought line
ax7.axhline(y=70, color='red', linestyle='--', alpha=0.5, label='Overbought')

ax7.set_xlabel('Technical Indicators', fontweight='bold')
ax7.set_ylabel('Value (%)', fontweight='bold')
ax7.set_title('TECHNICALS: USA MORE EXTENDED', fontweight='bold', fontsize=12)
ax7.set_xticks(x7)
ax7.set_xticklabels(indicators)
ax7.legend()
ax7.grid(True, alpha=0.3)

# ========== 8. SCENARIO ANALYSIS (Bottom Middle) ==========
ax8 = fig.add_subplot(gs[2, 1])

scenarios = ['Bear\n(-30%)', 'Base\n(60%)', 'Bull\n(10%)']
china_returns = [-20, 35, 60]
usa_returns = [-15, 12, 25]

x8 = np.arange(len(scenarios))
bars1 = ax8.bar(x8 - width/2, china_returns, width, label='China', color='#e74c3c', alpha=0.8)
bars2 = ax8.bar(x8 + width/2, usa_returns, width, label='USA', color='#3498db', alpha=0.8)

# Add probability weights
for i, scenario in enumerate(scenarios):
    prob = scenario.split('\n')[1]
    ax8.text(i, -25, prob, ha='center', fontsize=9, style='italic')

ax8.axhline(y=0, color='black', linewidth=1)
ax8.set_xlabel('Scenarios (Probability)', fontweight='bold')
ax8.set_ylabel('Expected Return (%)', fontweight='bold')
ax8.set_title('3-YEAR SCENARIOS', fontweight='bold', fontsize=12)
ax8.set_xticks(x8)
ax8.set_xticklabels(['Pessimistic', 'Base Case', 'Optimistic'])
ax8.legend()
ax8.grid(True, alpha=0.3)
ax8.set_ylim(-30, 70)

# ========== 9. KEY METRICS SUMMARY (Bottom Right) ==========
ax9 = fig.add_subplot(gs[2, 2])
ax9.axis('off')

# Create summary table
summary_text = """
INVESTMENT THESIS SUMMARY

CHINA ADVANTAGES:
✓ 40-50% valuation discount
✓ Higher GDP growth (4.5% vs 2.5%)
✓ Early in recovery cycle
✓ Massive stimulus starting
✓ Underowned by global funds

USA RISKS:
✗ Expensive valuations (P/E 22)
✗ Late cycle (10+ years)
✗ Limited upside (12% target)
✗ Crowded positioning
✗ Rising recession risk

RECOMMENDATION:
→ Overweight China (20-25%)
→ Neutral USA (45-50%)
→ Target: China +35% vs USA +12%
   (2-3 year horizon)
"""

ax9.text(0.1, 0.9, summary_text, transform=ax9.transAxes,
         fontsize=10, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# Main title
fig.suptitle('CHINA vs USA: COMPREHENSIVE BUBBLE & INVESTMENT ANALYSIS (August 2025)\n' + 
             'China Bubble Score: 32.5% (Moderate) | USA Bubble Score: 42.0% (Elevated)', 
             fontsize=14, fontweight='bold', y=0.98)

# Bottom annotation
fig.text(0.5, 0.01, 
         'Key Conclusion: China offers superior risk-adjusted returns with 40-50% valuation discount, ' +
         'higher growth, and early cycle positioning vs expensive, late-cycle US market',
         ha='center', fontsize=10, style='italic',
         bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))

plt.tight_layout()
plt.savefig('/Users/nilysenok/Desktop/pythonProject/CHINA_VS_USA_FINAL_ANALYSIS.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print("✅ Final China vs USA comprehensive comparison saved!")
# E-Commerce Sales Analysis — Insights Report

## Executive Summary
- **Total Net Revenue:** $749,846.20
- **Total Orders:** 15,000
- **Average Order Value:** $49.99
- **Overall Return Rate:** 3.19%
- **Best Performing Month:** 2025-12
- **Top Category:** Fashion
- **Top Region:** Central
- **Highest Revenue Weekday:** Monday

## Key Findings

### 1. Revenue Trend
Monthly net revenue shows clear seasonality, with a pronounced spike in
November–December consistent with holiday shopping behavior. See
`outputs/01_monthly_revenue_trend.png`.

### 2. Category Performance
**Fashion** is the leading revenue category. Category-level revenue
and order counts are broken down in `outputs/02_category_revenue.png` —
useful for inventory and marketing budget allocation decisions.

### 3. Regional Distribution
**Central** generates the largest share of revenue
(20.6%). See
`outputs/03_regional_share.png`. Regions with disproportionately low share
relative to population/market size are candidates for targeted marketing.

### 4. Channel & Payment Preferences
See `outputs/04_channel_payment.png` for the revenue split across Website,
Mobile App, and Marketplace channels, and the most-used payment methods —
relevant for prioritizing checkout UX investment.

### 5. Discount Strategy vs. Returns
There is a positive relationship between discount depth and return rate
(`outputs/05_return_rate_vs_discount.png`). This suggests high discount tiers
may be attracting lower-intent purchases — worth testing with a controlled
experiment before scaling discount campaigns further.

### 6. Customer Concentration
The top 20% of customers by spend contribute **40.8%** of total
revenue (`outputs/06_customer_spend_distribution.png`), indicating a
meaningful reliance on a core customer segment. A loyalty/retention program
targeted at this segment could have outsized ROI.

### 7. Weekly Ordering Pattern
Revenue peaks on **Monday** (`outputs/07_weekday_pattern.png`),
useful for timing flash sales, email campaigns, and ad spend.

## Recommendations
1. **Double down on Fashion** with expanded inventory and targeted ads,
   especially heading into Nov–Dec.
2. **Investigate the Central region's success factors** and test
   replicating them in underperforming regions.
3. **Cap or A/B test discounts above 10%** given the elevated return rate —
   confirm whether deep discounts are net-profitable after returns/logistics
   costs.
4. **Launch a loyalty program** for top-quintile customers to protect and grow
   the revenue base they represent.
5. **Align promotional pushes with Monday** peak ordering behavior.

---
*Generated from `analysis.py`. All figures saved to the `outputs/` directory.*

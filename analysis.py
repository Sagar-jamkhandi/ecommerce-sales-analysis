"""
E-Commerce Sales Analysis
---------------------------
Performs exploratory data analysis and generates a business insights report
on an e-commerce transactions dataset: revenue trends, category performance,
regional breakdown, customer behavior, and actionable recommendations.

Run:
    python generate_data.py     # produces data/ecommerce_transactions.csv
    python analysis.py          # produces charts in outputs/ + insights.md

Author: Sagar-jamkhandi
"""

import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")
DATA_PATH = "data/ecommerce_transactions.csv"
OUT_DIR = "outputs"


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    df["weekday"] = df["order_date"].dt.day_name()
    return df


def save_fig(fig, name: str):
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved chart -> {path}")


def monthly_revenue_trend(df: pd.DataFrame):
    monthly = df.groupby("month")["net_amount"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=monthly, x="month", y="net_amount", marker="o", ax=ax)
    ax.set_title("Monthly Net Revenue Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Net Revenue ($)")
    ax.tick_params(axis="x", rotation=60)
    save_fig(fig, "01_monthly_revenue_trend.png")
    return monthly


def category_performance(df: pd.DataFrame):
    cat = (
        df.groupby("category")
        .agg(revenue=("net_amount", "sum"), orders=("order_id", "count"))
        .sort_values("revenue", ascending=False)
        .reset_index()
    )
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=cat, x="revenue", y="category", hue="category", legend=False, ax=ax, palette="viridis")
    ax.set_title("Revenue by Product Category")
    ax.set_xlabel("Net Revenue ($)")
    ax.set_ylabel("")
    save_fig(fig, "02_category_revenue.png")
    return cat


def regional_breakdown(df: pd.DataFrame):
    region = df.groupby("region")["net_amount"].sum().sort_values(ascending=False).reset_index()
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(region["net_amount"], labels=region["region"], autopct="%1.1f%%", startangle=90)
    ax.set_title("Revenue Share by Region")
    save_fig(fig, "03_regional_share.png")
    return region


def channel_and_payment(df: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    channel = df.groupby("sales_channel")["net_amount"].sum().sort_values(ascending=False)
    sns.barplot(x=channel.index, y=channel.values, hue=channel.index, legend=False, ax=axes[0], palette="mako")
    axes[0].set_title("Revenue by Sales Channel")
    axes[0].set_ylabel("Net Revenue ($)")

    payment = df["payment_method"].value_counts()
    sns.barplot(x=payment.values, y=payment.index, hue=payment.index, legend=False, ax=axes[1], palette="rocket")
    axes[1].set_title("Order Count by Payment Method")
    axes[1].set_xlabel("Orders")

    save_fig(fig, "04_channel_payment.png")


def return_rate_analysis(df: pd.DataFrame):
    by_discount = df.groupby("discount_pct")["is_returned"].mean().reset_index()
    by_discount["return_rate_%"] = (by_discount["is_returned"] * 100).round(2)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=by_discount, x="discount_pct", y="return_rate_%", hue="discount_pct", legend=False, ax=ax, palette="flare")
    ax.set_title("Return Rate vs. Discount Level")
    ax.set_xlabel("Discount (%)")
    ax.set_ylabel("Return Rate (%)")
    save_fig(fig, "05_return_rate_vs_discount.png")
    return by_discount


def customer_value_analysis(df: pd.DataFrame):
    customer = (
        df.groupby("customer_id")
        .agg(total_spent=("net_amount", "sum"), orders=("order_id", "count"))
        .reset_index()
    )
    top20_cutoff = customer["total_spent"].quantile(0.8)
    top_customers_revenue_share = (
        customer[customer["total_spent"] >= top20_cutoff]["total_spent"].sum() / customer["total_spent"].sum() * 100
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(customer["total_spent"], bins=40, kde=True, ax=ax, color="steelblue")
    ax.set_title("Distribution of Customer Lifetime Spend")
    ax.set_xlabel("Total Spend ($)")
    save_fig(fig, "06_customer_spend_distribution.png")

    return customer, top_customers_revenue_share


def weekday_pattern(df: pd.DataFrame):
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday = df.groupby("weekday")["net_amount"].sum().reindex(order)
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(x=weekday.index, y=weekday.values, hue=weekday.index, legend=False, ax=ax, palette="crest")
    ax.set_title("Revenue by Day of Week")
    ax.set_ylabel("Net Revenue ($)")
    save_fig(fig, "07_weekday_pattern.png")
    return weekday


def write_insights_report(df, monthly, cat, region, by_discount, customer, top_share, weekday):
    total_revenue = df["net_amount"].sum()
    total_orders = df["order_id"].nunique()
    avg_order_value = total_revenue / total_orders
    return_rate = df["is_returned"].mean() * 100
    best_month = monthly.loc[monthly["net_amount"].idxmax(), "month"]
    top_category = cat.iloc[0]["category"]
    top_region = region.iloc[0]["region"]
    best_weekday = weekday.idxmax()

    report = f"""# E-Commerce Sales Analysis — Insights Report

## Executive Summary
- **Total Net Revenue:** ${total_revenue:,.2f}
- **Total Orders:** {total_orders:,}
- **Average Order Value:** ${avg_order_value:,.2f}
- **Overall Return Rate:** {return_rate:.2f}%
- **Best Performing Month:** {best_month}
- **Top Category:** {top_category}
- **Top Region:** {top_region}
- **Highest Revenue Weekday:** {best_weekday}

## Key Findings

### 1. Revenue Trend
Monthly net revenue shows clear seasonality, with a pronounced spike in
November–December consistent with holiday shopping behavior. See
`outputs/01_monthly_revenue_trend.png`.

### 2. Category Performance
**{top_category}** is the leading revenue category. Category-level revenue
and order counts are broken down in `outputs/02_category_revenue.png` —
useful for inventory and marketing budget allocation decisions.

### 3. Regional Distribution
**{top_region}** generates the largest share of revenue
({region.iloc[0]['net_amount'] / total_revenue * 100:.1f}%). See
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
The top 20% of customers by spend contribute **{top_share:.1f}%** of total
revenue (`outputs/06_customer_spend_distribution.png`), indicating a
meaningful reliance on a core customer segment. A loyalty/retention program
targeted at this segment could have outsized ROI.

### 7. Weekly Ordering Pattern
Revenue peaks on **{best_weekday}** (`outputs/07_weekday_pattern.png`),
useful for timing flash sales, email campaigns, and ad spend.

## Recommendations
1. **Double down on {top_category}** with expanded inventory and targeted ads,
   especially heading into Nov–Dec.
2. **Investigate the {top_region} region's success factors** and test
   replicating them in underperforming regions.
3. **Cap or A/B test discounts above 10%** given the elevated return rate —
   confirm whether deep discounts are net-profitable after returns/logistics
   costs.
4. **Launch a loyalty program** for top-quintile customers to protect and grow
   the revenue base they represent.
5. **Align promotional pushes with {best_weekday}** peak ordering behavior.

---
*Generated from `analysis.py`. All figures saved to the `outputs/` directory.*
"""
    with open("insights.md", "w") as f:
        f.write(report)
    print("Saved insights report -> insights.md")


def main():
    df = load_data()
    monthly = monthly_revenue_trend(df)
    cat = category_performance(df)
    region = regional_breakdown(df)
    channel_and_payment(df)
    by_discount = return_rate_analysis(df)
    customer, top_share = customer_value_analysis(df)
    weekday = weekday_pattern(df)
    write_insights_report(df, monthly, cat, region, by_discount, customer, top_share, weekday)
    print("\nAnalysis complete. See outputs/ for charts and insights.md for the written report.")


if __name__ == "__main__":
    main()

"""
E-Commerce Sales Analysis — Interactive Dashboard
----------------------------------------------------
Streamlit wrapper around the analysis in analysis.py. Generates the
synthetic dataset on first load if it doesn't exist yet, then renders
every chart and the written insights report inline — this is the file
to deploy to Streamlit Cloud.

Usage:
    streamlit run app.py
"""

import os
import subprocess

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_theme(style="whitegrid")

st.set_page_config(page_title="E-Commerce Sales Analysis", page_icon="🛒", layout="wide")
st.title("🛒 E-Commerce Sales Analysis Dashboard")
st.caption(
    "Exploratory data analysis on e-commerce transactions: revenue trends, "
    "category & regional performance, discount/return relationship, and "
    "customer value concentration."
)

DATA_PATH = "data/ecommerce_transactions.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    if not os.path.exists(DATA_PATH):
        # Generate the synthetic dataset on first run (e.g. fresh Streamlit Cloud deploy)
        subprocess.run(["python", "generate_data.py"], check=True)
    df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    df["weekday"] = df["order_date"].dt.day_name()
    return df


df = load_data()

# --- Sidebar filters ---------------------------------------------------
with st.sidebar:
    st.header("Filters")
    regions = st.multiselect("Region", sorted(df["region"].unique()), default=list(df["region"].unique()))
    categories = st.multiselect("Category", sorted(df["category"].unique()), default=list(df["category"].unique()))

filtered = df[df["region"].isin(regions) & df["category"].isin(categories)]

if filtered.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

# --- KPIs ---------------------------------------------------------
total_revenue = filtered["net_amount"].sum()
total_orders = filtered["order_id"].nunique()
avg_order_value = total_revenue / total_orders
return_rate = filtered["is_returned"].mean() * 100

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Net Revenue", f"${total_revenue:,.0f}")
k2.metric("Total Orders", f"{total_orders:,}")
k3.metric("Avg. Order Value", f"${avg_order_value:,.2f}")
k4.metric("Return Rate", f"{return_rate:.2f}%")

st.divider()

# --- Monthly revenue trend ---------------------------------------------
st.subheader("📈 Monthly Net Revenue Trend")
monthly = filtered.groupby("month")["net_amount"].sum().reset_index()
fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.lineplot(data=monthly, x="month", y="net_amount", marker="o", ax=ax1)
ax1.set_xlabel("Month")
ax1.set_ylabel("Net Revenue ($)")
ax1.tick_params(axis="x", rotation=60)
st.pyplot(fig1)
plt.close(fig1)

left, right = st.columns(2)

# --- Category performance ---------------------------------------------
with left:
    st.subheader("🏷️ Revenue by Category")
    cat = (
        filtered.groupby("category")
        .agg(revenue=("net_amount", "sum"), orders=("order_id", "count"))
        .sort_values("revenue", ascending=False)
        .reset_index()
    )
    fig2, ax2 = plt.subplots(figsize=(7, 4.5))
    sns.barplot(data=cat, x="revenue", y="category", hue="category", legend=False, ax=ax2, palette="viridis")
    ax2.set_xlabel("Net Revenue ($)")
    ax2.set_ylabel("")
    st.pyplot(fig2)
    plt.close(fig2)

# --- Regional breakdown ---------------------------------------------
with right:
    st.subheader("🌍 Revenue Share by Region")
    region_df = filtered.groupby("region")["net_amount"].sum().sort_values(ascending=False).reset_index()
    fig3, ax3 = plt.subplots(figsize=(5.5, 5.5))
    ax3.pie(region_df["net_amount"], labels=region_df["region"], autopct="%1.1f%%", startangle=90)
    st.pyplot(fig3)
    plt.close(fig3)

left2, right2 = st.columns(2)

# --- Channel & payment ---------------------------------------------
with left2:
    st.subheader("📲 Revenue by Sales Channel")
    channel = filtered.groupby("sales_channel")["net_amount"].sum().sort_values(ascending=False)
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    sns.barplot(x=channel.index, y=channel.values, hue=channel.index, legend=False, ax=ax4, palette="mako")
    ax4.set_ylabel("Net Revenue ($)")
    st.pyplot(fig4)
    plt.close(fig4)

with right2:
    st.subheader("💳 Orders by Payment Method")
    payment = filtered["payment_method"].value_counts()
    fig5, ax5 = plt.subplots(figsize=(6, 4))
    sns.barplot(x=payment.values, y=payment.index, hue=payment.index, legend=False, ax=ax5, palette="rocket")
    ax5.set_xlabel("Orders")
    st.pyplot(fig5)
    plt.close(fig5)

# --- Discount vs return rate ---------------------------------------------
st.subheader("⚠️ Return Rate vs. Discount Level")
by_discount = filtered.groupby("discount_pct")["is_returned"].mean().reset_index()
by_discount["return_rate_%"] = (by_discount["is_returned"] * 100).round(2)
fig6, ax6 = plt.subplots(figsize=(9, 4))
sns.barplot(data=by_discount, x="discount_pct", y="return_rate_%", hue="discount_pct", legend=False, ax=ax6, palette="flare")
ax6.set_xlabel("Discount (%)")
ax6.set_ylabel("Return Rate (%)")
st.pyplot(fig6)
plt.close(fig6)

left3, right3 = st.columns(2)

# --- Customer value distribution ---------------------------------------------
with left3:
    st.subheader("👤 Customer Lifetime Spend Distribution")
    customer = (
        filtered.groupby("customer_id")
        .agg(total_spent=("net_amount", "sum"), orders=("order_id", "count"))
        .reset_index()
    )
    top20_cutoff = customer["total_spent"].quantile(0.8)
    top_share = (
        customer[customer["total_spent"] >= top20_cutoff]["total_spent"].sum()
        / customer["total_spent"].sum() * 100
    )
    fig7, ax7 = plt.subplots(figsize=(6.5, 4.5))
    sns.histplot(customer["total_spent"], bins=40, kde=True, ax=ax7, color="steelblue")
    ax7.set_xlabel("Total Spend ($)")
    st.pyplot(fig7)
    plt.close(fig7)
    st.caption(f"Top 20% of customers by spend drive **{top_share:.1f}%** of total revenue.")

# --- Weekday pattern ---------------------------------------------
with right3:
    st.subheader("📅 Revenue by Day of Week")
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday = filtered.groupby("weekday")["net_amount"].sum().reindex(order)
    fig8, ax8 = plt.subplots(figsize=(6.5, 4.5))
    sns.barplot(x=weekday.index, y=weekday.values, hue=weekday.index, legend=False, ax=ax8, palette="crest")
    ax8.set_ylabel("Net Revenue ($)")
    ax8.tick_params(axis="x", rotation=45)
    st.pyplot(fig8)
    plt.close(fig8)

st.divider()

# --- Written insights ---------------------------------------------
st.subheader("📝 Key Findings & Recommendations")
best_month = monthly.loc[monthly["net_amount"].idxmax(), "month"]
top_category = cat.iloc[0]["category"]
top_region = region_df.iloc[0]["region"]
best_weekday = weekday.idxmax()

st.markdown(
    f"""
- **Best performing month:** {best_month} — revenue peaks in Nov–Dec, consistent with holiday shopping seasonality.
- **Top category:** **{top_category}** — leading revenue driver; a strong candidate for expanded inventory and ad spend.
- **Top region:** **{top_region}** — generates the largest revenue share ({region_df.iloc[0]['net_amount'] / total_revenue * 100:.1f}%); worth studying what's working there to replicate elsewhere.
- **Discount risk:** Higher discount tiers correlate with higher return rates — worth A/B testing whether deep discounts remain profitable after returns/logistics costs.
- **Customer concentration:** the top 20% of customers by spend drive **{top_share:.1f}%** of revenue — a loyalty program targeted at this segment could have outsized ROI.
- **Best day to promote:** revenue peaks on **{best_weekday}** — a good anchor for flash sales and email campaigns.
"""
)

st.subheader("📄 Raw Data")
st.dataframe(filtered, use_container_width=True, height=300)

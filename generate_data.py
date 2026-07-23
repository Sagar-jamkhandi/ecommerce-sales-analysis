"""
Generates a realistic synthetic e-commerce transactions dataset for analysis.

Why synthetic data? It lets the project run end-to-end with zero setup and no
API keys, while mirroring the structure of a real retail dataset (like the
well-known "Online Retail" / Olist datasets on Kaggle). Swap this file's
output for a real Kaggle CSV any time without changing analysis.py.

Run:
    python generate_data.py
Produces:
    data/ecommerce_transactions.csv
"""

import os
import numpy as np
import pandas as pd

np.random.seed(42)

N_ROWS = 15000
START_DATE = "2024-01-01"
END_DATE = "2025-12-31"

CATEGORIES = {
    "Electronics": ["Wireless Earbuds", "Smartphone Case", "Bluetooth Speaker", "USB-C Cable", "Laptop Stand"],
    "Home & Kitchen": ["Coffee Maker", "Non-stick Pan", "LED Desk Lamp", "Storage Bins", "Blender"],
    "Fashion": ["Cotton T-Shirt", "Running Shoes", "Denim Jacket", "Sunglasses", "Backpack"],
    "Beauty": ["Face Moisturizer", "Shampoo", "Lipstick", "Sunscreen SPF50", "Hair Dryer"],
    "Sports": ["Yoga Mat", "Dumbbell Set", "Water Bottle", "Resistance Bands", "Running Shorts"],
}

REGIONS = ["North", "South", "East", "West", "Central"]
CHANNELS = ["Website", "Mobile App", "Marketplace"]
PAYMENT_METHODS = ["Credit Card", "Debit Card", "UPI", "Net Banking", "Cash on Delivery"]

BASE_PRICES = {
    "Wireless Earbuds": 45, "Smartphone Case": 15, "Bluetooth Speaker": 60, "USB-C Cable": 8, "Laptop Stand": 30,
    "Coffee Maker": 55, "Non-stick Pan": 25, "LED Desk Lamp": 20, "Storage Bins": 18, "Blender": 40,
    "Cotton T-Shirt": 12, "Running Shoes": 65, "Denim Jacket": 50, "Sunglasses": 22, "Backpack": 35,
    "Face Moisturizer": 18, "Shampoo": 10, "Lipstick": 14, "Sunscreen SPF50": 16, "Hair Dryer": 32,
    "Yoga Mat": 20, "Dumbbell Set": 45, "Water Bottle": 9, "Resistance Bands": 15, "Running Shorts": 17,
}


def generate() -> pd.DataFrame:
    dates = pd.date_range(START_DATE, END_DATE, freq="D")

    rows = []
    for i in range(N_ROWS):
        order_date = np.random.choice(dates)
        order_date = pd.Timestamp(order_date)

        # seasonal boost: Nov-Dec (holiday shopping) gets more orders/higher qty
        month = order_date.month
        seasonal_multiplier = 1.6 if month in (11, 12) else (0.8 if month in (1, 2) else 1.0)

        category = np.random.choice(list(CATEGORIES.keys()))
        product = np.random.choice(CATEGORIES[category])
        base_price = BASE_PRICES[product]

        price = round(base_price * np.random.uniform(0.9, 1.15), 2)
        quantity = max(1, int(np.random.poisson(1.5 * seasonal_multiplier)))
        discount_pct = np.random.choice([0, 0, 0, 5, 10, 15, 20], p=[0.4, 0.15, 0.15, 0.1, 0.1, 0.05, 0.05])

        gross_amount = round(price * quantity, 2)
        discount_amount = round(gross_amount * discount_pct / 100, 2)
        net_amount = round(gross_amount - discount_amount, 2)

        region = np.random.choice(REGIONS)
        channel = np.random.choice(CHANNELS, p=[0.45, 0.4, 0.15])
        payment = np.random.choice(PAYMENT_METHODS)

        # simple churn/return signal: higher-discount orders slightly more likely returned
        return_prob = 0.03 + (discount_pct / 100) * 0.05
        is_returned = np.random.rand() < return_prob

        customer_id = f"CUST{np.random.randint(1, 3500):05d}"

        rows.append(
            {
                "order_id": f"ORD{100000 + i}",
                "order_date": order_date.date().isoformat(),
                "customer_id": customer_id,
                "category": category,
                "product": product,
                "unit_price": price,
                "quantity": quantity,
                "discount_pct": discount_pct,
                "gross_amount": gross_amount,
                "discount_amount": discount_amount,
                "net_amount": net_amount,
                "region": region,
                "sales_channel": channel,
                "payment_method": payment,
                "is_returned": is_returned,
            }
        )

    df = pd.DataFrame(rows)
    df = df.sort_values("order_date").reset_index(drop=True)
    return df


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df = generate()
    out_path = "data/ecommerce_transactions.csv"
    df.to_csv(out_path, index=False)
    print(f"Generated {len(df)} rows -> {out_path}")
    print(df.head())

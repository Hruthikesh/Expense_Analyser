import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ── Seed for reproducibility ──
np.random.seed(42)
random.seed(42)

# ── Categories & sample merchants ──
categories = {
    "Food & Dining":     ["Zomato", "Swiggy", "McDonald's", "Subway", "Domino's", "KFC", "Cafe Coffee Day"],
    "Transport":         ["Ola", "Uber", "Rapido", "Indian Railways", "RedBus", "IndiGo Airlines"],
    "Shopping":          ["Amazon", "Flipkart", "Myntra", "Ajio", "Meesho", "Nykaa"],
    "Entertainment":     ["Netflix", "Spotify", "BookMyShow", "Steam", "YouTube Premium"],
    "Education":         ["Coursera", "Udemy", "Internshala", "Unacademy", "NPTEL"],
    "Health":            ["PharmEasy", "1mg", "Apollo Pharmacy", "Cult.fit"],
    "Utilities":         ["Jio Recharge", "Airtel", "Electricity Bill", "Water Bill"],
    "Groceries":         ["BigBasket", "Blinkit", "DMart", "JioMart", "Zepto"],
    "Personal Care":     ["Nykaa", "Mamaearth", "Lakme", "Salon"],
    "Miscellaneous":     ["ATM Withdrawal", "UPI Transfer", "Bank Charges", "Other"],
}

# ── Spending weights (realistic for a student) ──
category_weights = {
    "Food & Dining": 0.28,
    "Transport": 0.12,
    "Shopping": 0.15,
    "Entertainment": 0.08,
    "Education": 0.10,
    "Health": 0.05,
    "Utilities": 0.07,
    "Groceries": 0.08,
    "Personal Care": 0.04,
    "Miscellaneous": 0.03,
}

# ── Amount ranges per category (INR) ──
amount_ranges = {
    "Food & Dining":   (50,  800),
    "Transport":       (30,  1200),
    "Shopping":        (200, 5000),
    "Entertainment":   (99,  699),
    "Education":       (199, 2999),
    "Health":          (50,  1500),
    "Utilities":       (100, 1200),
    "Groceries":       (100, 2000),
    "Personal Care":   (80,  1500),
    "Miscellaneous":   (100, 3000),
}

def generate_transactions(n=1000, months=12):
    records = []
    start_date = datetime(2024, 1, 1)
    end_date   = datetime(2024, 12, 31)

    cat_list    = list(categories.keys())
    cat_weights = [category_weights[c] for c in cat_list]

    for _ in range(n):
        # Random date
        days_range = (end_date - start_date).days
        txn_date   = start_date + timedelta(days=random.randint(0, days_range))

        # Pick category
        cat = random.choices(cat_list, weights=cat_weights, k=1)[0]

        # Pick merchant
        merchant = random.choice(categories[cat])

        # Amount with slight monthly variation (spend more in festive months Oct/Nov)
        lo, hi = amount_ranges[cat]
        amount = round(random.uniform(lo, hi), 2)
        if txn_date.month in [10, 11]:   # Festive bump
            amount = round(amount * random.uniform(1.1, 1.4), 2)

        # Payment mode
        mode = random.choices(
            ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash"],
            weights=[0.45, 0.25, 0.15, 0.10, 0.05], k=1
        )[0]

        records.append({
            "date":         txn_date.strftime("%Y-%m-%d"),
            "merchant":     merchant,
            "category":     cat,
            "amount":       amount,
            "payment_mode": mode,
            "month":        txn_date.strftime("%B"),
            "month_num":    txn_date.month,
        })

    df = pd.DataFrame(records).sort_values("date").reset_index(drop=True)
    df.to_csv("transactions.csv", index=False)
    print(f"✅ Generated {len(df)} transactions saved to transactions.csv")
    print(f"\nSample:\n{df.head(5).to_string()}")
    print(f"\nTotal spend: ₹{df['amount'].sum():,.2f}")
    print(f"Date range : {df['date'].min()} → {df['date'].max()}")
    return df

if __name__ == "__main__":
    df = generate_transactions(1000)

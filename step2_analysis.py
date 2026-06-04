import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# ── Style ──
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({"font.family": "DejaVu Sans", "figure.dpi": 150})

os.makedirs("charts", exist_ok=True)

df = pd.read_csv("transactions.csv")
df["date"]  = pd.to_datetime(df["date"])
df["month"] = pd.Categorical(
    df["month"],
    categories=["January","February","March","April","May","June",
                "July","August","September","October","November","December"],
    ordered=True
)

print("=" * 55)
print("       EXPENSE ANALYSIS SUMMARY")
print("=" * 55)
print(f"Total Transactions : {len(df):,}")
print(f"Total Spend        : ₹{df['amount'].sum():,.2f}")
print(f"Average per Txn    : ₹{df['amount'].mean():,.2f}")
print(f"Highest Single Txn : ₹{df['amount'].max():,.2f} ({df.loc[df['amount'].idxmax(),'merchant']})")
print(f"Most Used Payment  : {df['payment_mode'].value_counts().index[0]}")
print("=" * 55)

# ── Chart 1: Monthly spending trend ──
monthly = df.groupby("month_num")["amount"].sum().reset_index()
monthly["month_name"] = pd.to_datetime(monthly["month_num"], format="%m").dt.strftime("%b")

fig, ax = plt.subplots(figsize=(12, 5))
bars = ax.bar(monthly["month_name"], monthly["amount"], color=sns.color_palette("Blues_d", 12))
ax.plot(monthly["month_name"], monthly["amount"], "o-", color="#e74c3c", linewidth=2, markersize=6, label="Trend")
ax.set_title("Monthly Spending Trend (2024)", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Month", fontsize=11)
ax.set_ylabel("Total Spend (₹)", fontsize=11)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1000:.0f}K"))
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
            f"₹{bar.get_height()/1000:.1f}K", ha="center", va="bottom", fontsize=8)
ax.legend()
plt.tight_layout()
plt.savefig("charts/01_monthly_trend.png")
plt.close()
print("✅ Chart 1 saved: Monthly Trend")

# ── Chart 2: Category breakdown (pie) ──
cat_spend = df.groupby("category")["amount"].sum().sort_values(ascending=False)
colors = sns.color_palette("Set2", len(cat_spend))

fig, ax = plt.subplots(figsize=(9, 7))
wedges, texts, autotexts = ax.pie(
    cat_spend.values,
    labels=cat_spend.index,
    autopct="%1.1f%%",
    colors=colors,
    startangle=140,
    pctdistance=0.82,
    wedgeprops=dict(edgecolor="white", linewidth=1.5)
)
for t in autotexts:
    t.set_fontsize(8)
ax.set_title("Spending by Category", fontsize=15, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig("charts/02_category_pie.png")
plt.close()
print("✅ Chart 2 saved: Category Pie")

# ── Chart 3: Top 10 merchants ──
top_merchants = df.groupby("merchant")["amount"].sum().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 6))
bars = sns.barplot(x=top_merchants.values, y=top_merchants.index, palette="rocket_r", ax=ax)
ax.set_title("Top 10 Merchants by Spend", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Total Spend (₹)", fontsize=11)
ax.set_ylabel("")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1000:.0f}K"))
for i, v in enumerate(top_merchants.values):
    ax.text(v + 100, i, f"₹{v/1000:.1f}K", va="center", fontsize=9)
plt.tight_layout()
plt.savefig("charts/03_top_merchants.png")
plt.close()
print("✅ Chart 3 saved: Top Merchants")

# ── Chart 4: Payment mode distribution ──
mode_counts = df["payment_mode"].value_counts()

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=mode_counts.index, y=mode_counts.values, palette="coolwarm", ax=ax)
ax.set_title("Transactions by Payment Mode", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Payment Mode", fontsize=11)
ax.set_ylabel("Number of Transactions", fontsize=11)
for i, v in enumerate(mode_counts.values):
    ax.text(i, v + 3, str(v), ha="center", fontsize=10, fontweight="bold")
plt.tight_layout()
plt.savefig("charts/04_payment_mode.png")
plt.close()
print("✅ Chart 4 saved: Payment Mode")

# ── Chart 5: Heatmap — category spend by month ──
pivot = df.pivot_table(index="category", columns="month", values="amount",
                       aggfunc="sum", fill_value=0)

fig, ax = plt.subplots(figsize=(14, 7))
sns.heatmap(pivot/1000, annot=True, fmt=".0f", cmap="YlOrRd",
            linewidths=0.5, ax=ax, cbar_kws={"label": "Spend (₹K)"})
ax.set_title("Category × Month Spending Heatmap (₹ Thousands)", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Month", fontsize=11)
ax.set_ylabel("Category", fontsize=11)
plt.tight_layout()
plt.savefig("charts/05_heatmap.png")
plt.close()
print("✅ Chart 5 saved: Heatmap")

# ── Chart 6: Anomaly detection — flag high spends ──
mean_spend = df["amount"].mean()
std_spend  = df["amount"].std()
threshold  = mean_spend + 2 * std_spend

anomalies  = df[df["amount"] > threshold].copy()
normal     = df[df["amount"] <= threshold].copy()

fig, ax = plt.subplots(figsize=(13, 5))
ax.scatter(normal["date"],    normal["amount"],    alpha=0.3, s=10, color="#3498db", label="Normal")
ax.scatter(anomalies["date"], anomalies["amount"], alpha=0.8, s=30, color="#e74c3c", label=f"Anomaly (>{threshold:.0f})")
ax.axhline(threshold, color="#e74c3c", linestyle="--", linewidth=1.2, label=f"Threshold ₹{threshold:.0f}")
ax.set_title("Spending Anomaly Detection", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Date", fontsize=11)
ax.set_ylabel("Amount (₹)", fontsize=11)
ax.legend()
plt.tight_layout()
plt.savefig("charts/06_anomaly.png")
plt.close()
print("✅ Chart 6 saved: Anomaly Detection")

print(f"\n📊 All 6 charts saved in /charts folder")
print(f"⚠️  Anomalies detected: {len(anomalies)} transactions above ₹{threshold:.0f}")

# ── Save summary stats for AI insights ──
summary = {
    "total_transactions": len(df),
    "total_spend": round(df["amount"].sum(), 2),
    "avg_per_transaction": round(df["amount"].mean(), 2),
    "top_category": cat_spend.index[0],
    "top_category_spend": round(cat_spend.iloc[0], 2),
    "top_merchant": top_merchants.index[0],
    "highest_month": monthly.loc[monthly["amount"].idxmax(), "month_name"],
    "lowest_month": monthly.loc[monthly["amount"].idxmin(), "month_name"],
    "anomalies_count": len(anomalies),
    "anomaly_threshold": round(threshold, 2),
    "most_used_payment": df["payment_mode"].value_counts().index[0],
    "category_breakdown": cat_spend.round(2).to_dict(),
}

import json
with open("summary_stats.json", "w") as f:
    json.dump(summary, f, indent=2)
print("✅ Summary stats saved to summary_stats.json")

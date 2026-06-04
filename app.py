import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import json
import os

# ── Page config ──
st.set_page_config(
    page_title="AI Expense Analyser",
    page_icon="💰",
    layout="wide"
)

sns.set_theme(style="whitegrid")

# ── Header ──
st.title("💰 AI-Powered Personal Expense Analyser")
st.markdown("*Upload your transactions CSV or use the sample dataset to get instant AI-generated insights.*")
st.divider()

# ── Sidebar ──
st.sidebar.header("⚙️ Settings")
use_sample = st.sidebar.checkbox("Use sample dataset", value=True)

uploaded_file = None
if not use_sample:
    uploaded_file = st.sidebar.file_uploader("Upload transactions.csv", type=["csv"])

# ── Load data ──
@st.cache_data
def load_data(path="transactions.csv"):
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df

if use_sample and os.path.exists("transactions.csv"):
    df = load_data("transactions.csv")
elif uploaded_file:
    df = pd.read_csv(uploaded_file)
    df["date"] = pd.to_datetime(df["date"])
else:
    st.warning("⚠️ Run step1_generate_data.py first to create transactions.csv, then relaunch this app.")
    st.stop()

# ── KPI Cards ──
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💳 Total Transactions", f"{len(df):,}")
with col2:
    st.metric("💸 Total Annual Spend", f"₹{df['amount'].sum():,.0f}")
with col3:
    st.metric("📊 Avg per Transaction", f"₹{df['amount'].mean():,.0f}")
with col4:
    top_cat = df.groupby("category")["amount"].sum().idxmax()
    st.metric("🏆 Top Category", top_cat)

st.divider()

# ── Charts row 1 ──
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Monthly Spending Trend")
    monthly = df.groupby("month_num")["amount"].sum().reset_index()
    monthly["month_name"] = pd.to_datetime(monthly["month_num"], format="%m").dt.strftime("%b")
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(monthly["month_name"], monthly["amount"], color=sns.color_palette("Blues_d", 12))
    ax.plot(monthly["month_name"], monthly["amount"], "o-", color="#e74c3c", linewidth=2)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1000:.0f}K"))
    ax.set_xlabel("Month"); ax.set_ylabel("Total Spend (₹)")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    st.subheader("🥧 Spending by Category")
    cat_spend = df.groupby("category")["amount"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.pie(cat_spend.values, labels=cat_spend.index, autopct="%1.1f%%",
           colors=sns.color_palette("Set2", len(cat_spend)), startangle=140,
           wedgeprops=dict(edgecolor="white"))
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ── Charts row 2 ──
col3, col4 = st.columns(2)

with col3:
    st.subheader("🏪 Top 10 Merchants")
    top_merch = df.groupby("merchant")["amount"].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=top_merch.values, y=top_merch.index, palette="rocket_r", ax=ax)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1000:.0f}K"))
    ax.set_xlabel("Total Spend (₹)"); ax.set_ylabel("")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col4:
    st.subheader("⚠️ Anomaly Detection")
    mean_s = df["amount"].mean()
    std_s  = df["amount"].std()
    thresh = mean_s + 2 * std_s
    anom   = df[df["amount"] > thresh]
    norm   = df[df["amount"] <= thresh]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.scatter(norm["date"],  norm["amount"],  alpha=0.3, s=8,  color="#3498db", label="Normal")
    ax.scatter(anom["date"],  anom["amount"],  alpha=0.8, s=25, color="#e74c3c", label=f"Anomaly")
    ax.axhline(thresh, color="#e74c3c", linestyle="--", linewidth=1)
    ax.set_xlabel("Date"); ax.set_ylabel("Amount (₹)"); ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.divider()

# ── Heatmap ──
st.subheader("🗓️ Category × Month Heatmap")
month_order = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]
pivot = df.pivot_table(index="category", columns="month", values="amount",
                       aggfunc="sum", fill_value=0)
pivot = pivot.reindex(columns=[m for m in month_order if m in pivot.columns])
fig, ax = plt.subplots(figsize=(14, 6))
sns.heatmap(pivot/1000, annot=True, fmt=".0f", cmap="YlOrRd",
            linewidths=0.5, ax=ax, cbar_kws={"label": "₹K"})
ax.set_xlabel("Month"); ax.set_ylabel("Category")
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.divider()

# ── AI Insights ──
st.subheader("🤖 AI-Generated Insights")
if os.path.exists("ai_insights_report.txt"):
    with open("ai_insights_report.txt", "r") as f:
        insights = f.read()
    st.code(insights, language=None)
else:
    st.info("Run step3_ai_insights.py first to generate insights, then refresh this page.")

st.divider()

# ── Raw data table ──
with st.expander("📄 View Raw Transaction Data"):
    st.dataframe(df.sort_values("date", ascending=False).head(100), use_container_width=True)

st.caption("Built with Python · Pandas · Matplotlib · Seaborn · Streamlit | AI Expense Analyser Project")

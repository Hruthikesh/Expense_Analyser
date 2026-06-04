# AI-Powered Personal Expense Analyser

A Python-based data analytics project that generates synthetic transaction data, performs multi-dimensional expense analysis, detects spending anomalies, and delivers AI-generated financial insights via a Streamlit dashboard.

---

## 📊 Project Overview

| Feature | Details |
|---|---|
| Dataset | 1,000+ synthetic transactions (2024) |
| Categories | 10 spending categories |
| Charts | 6 analytical visualisations |
| AI Insights | GPT API / Rule-based engine |
| Dashboard | Interactive Streamlit web app |

---

## Tech Stack

- **Python** — Core language
- **Pandas & NumPy** — Data generation and processing
- **Matplotlib & Seaborn** — Visualisations
- **Streamlit** — Interactive dashboard
- **OpenAI GPT API** — AI-generated insights (optional)

---

## Project Structure

```
├── step1_generate_data.py   # Generate 1000 synthetic transactions
├── step2_analysis.py        # EDA + 6 charts saved to /charts
├── step3_ai_insights.py     # AI insights (GPT API or rule-based)
├── app.py                   # Streamlit dashboard
├── transactions.csv         # Generated dataset
├── summary_stats.json       # Aggregated stats
├── ai_insights_report.txt   # AI-generated report
└── charts/                  # All saved visualisations
```

---


## Key Findings (Sample Run)

- **Total Annual Spend:** ₹4,82,000+ across 1,000 transactions
- **Top Category:** Food & Dining (28% of total spend)
- **Anomalies Detected:** 45+ transactions flagged as unusually high
- **Peak Spending Month:** October (festive season effect)
- **Most Used Payment:** UPI (45% of all transactions)

---

## AI Insights Feature

The project integrates with **OpenAI GPT-3.5** to generate:
- Executive summary of spending behaviour
- Top 3 personalised saving recommendations
- Positive habit identification
- Risk alerts for anomalous spending

---

## Author

**Hruthikesh** | B.Tech Mining Engineering, IIT Kharagpur  
2nd Year | Interested in Data Science & AI applications

---

## 📌 Skills Demonstrated

`Python` `Pandas` `Data Cleaning` `EDA` `Data Visualisation` `Anomaly Detection` `API Integration` `Streamlit` `AI Tools`

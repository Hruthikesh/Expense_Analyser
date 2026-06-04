import json
import os

# ── Load summary ──
with open("summary_stats.json", "r") as f:
    stats = json.load(f)

# ── Build prompt for GPT ──
def build_prompt(stats):
    cat_breakdown = "\n".join(
        [f"  - {k}: ₹{v:,.2f}" for k, v in stats["category_breakdown"].items()]
    )
    prompt = f"""
You are a personal finance advisor AI. Analyse the following expense data for a user and provide:
1. A 3-sentence executive summary of their spending behaviour
2. Top 3 specific actionable recommendations to save money
3. One positive spending habit you notice
4. A risk alert if any anomalies or overspending is detected

Expense Data:
- Total Transactions: {stats['total_transactions']}
- Total Annual Spend: ₹{stats['total_spend']:,}
- Average per Transaction: ₹{stats['avg_per_transaction']}
- Top Spending Category: {stats['top_category']} (₹{stats['top_category_spend']:,})
- Top Merchant: {stats['top_merchant']}
- Highest Spending Month: {stats['highest_month']}
- Lowest Spending Month: {stats['lowest_month']}
- Anomalous Transactions: {stats['anomalies_count']} transactions above ₹{stats['anomaly_threshold']}
- Most Used Payment Mode: {stats['most_used_payment']}

Category Breakdown:
{cat_breakdown}

Give your response in a friendly, clear tone. Use ₹ for currency.
"""
    return prompt.strip()


def get_ai_insights(stats):
    """
    Calls OpenAI GPT API to generate insights.
    Replace YOUR_API_KEY with your actual OpenAI API key.
    Get free key at: platform.openai.com
    """
    try:
        from openai import OpenAI

        # ── PUT YOUR OPENAI API KEY HERE ──
        api_key = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")

        if api_key == "YOUR_OPENAI_API_KEY_HERE":
            raise ValueError("No API key set")

        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful personal finance advisor."},
                {"role": "user",   "content": build_prompt(stats)}
            ],
            max_tokens=600,
            temperature=0.7,
        )
        return response.choices[0].message.content

    except ValueError:
        # ── FALLBACK: Rule-based insights (no API key needed) ──
        return generate_rule_based_insights(stats)

    except Exception as e:
        print(f"API error: {e}")
        return generate_rule_based_insights(stats)


def generate_rule_based_insights(stats):
    """
    Generates insights using pure Python logic — no API key needed.
    This is what runs if you don't have an OpenAI key.
    """
    top_cat   = stats["top_category"]
    top_spend = stats["top_category_spend"]
    total     = stats["total_spend"]
    pct       = round((top_spend / total) * 100, 1)
    anomalies = stats["anomalies_count"]

    insights = f"""
╔══════════════════════════════════════════════════════════╗
              FINANCIAL INSIGHTS REPORT
╚══════════════════════════════════════════════════════════╝

📊 EXECUTIVE SUMMARY
──────────────────────────────────────────────────────────
Your total annual expenditure is ₹{total:,.2f} across
{stats['total_transactions']:,} transactions. Your biggest
spending area is {top_cat}, which accounts for {pct}% of
total spend (₹{top_spend:,.2f}). Spending peaks in
{stats['highest_month']} and is lowest in {stats['lowest_month']}.

💡 TOP 3 RECOMMENDATIONS
──────────────────────────────────────────────────────────
1. {top_cat} is your highest expense ({pct}% of budget).
   Set a monthly cap and track weekly to reduce by 15-20%.

2. You have {anomalies} unusually high transactions.
   Review these — they may be impulse purchases or errors.

3. Your most-used payment mode is {stats['most_used_payment']}.
   Switch to a cashback credit card for recurring spends
   to earn 1-5% back automatically.

✅ POSITIVE HABIT DETECTED
──────────────────────────────────────────────────────────
You are spending on Education (online courses/platforms) —
this is a great investment in your skills and future earnings.
Keep this category consistent even when cutting other expenses.

⚠️  RISK ALERT
──────────────────────────────────────────────────────────
{anomalies} transactions flagged as anomalies (above
₹{stats['anomaly_threshold']:,.0f}). Review these in the
anomaly chart — unexpected large spends can derail savings
goals quickly if not monitored.

══════════════════════════════════════════════════════════
  Expense Analyser | Python + Rule Engine
══════════════════════════════════════════════════════════
"""
    return insights


if __name__ == "__main__":
    print("🤖 Generating AI insights...\n")
    insights = get_ai_insights(stats)
    print(insights)

    # Save to file
    with open("ai_insights_report.txt", "w", encoding="utf-8") as f:
        f.write(insights)

    print("\n✅ Insights saved to ai_insights_report.txt")
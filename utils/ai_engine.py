import os
import json

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

from dotenv import load_dotenv

load_dotenv()

# Configuration
API_KEY = os.getenv("GEMINI_API_KEY")
model = None

if API_KEY and API_KEY != "your_gemini_api_key_here" and GENAI_AVAILABLE:
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception:
        model = None


def get_ai_categories(descriptions):
    """
    Uses Gemini to categorize transaction descriptions.
    Returns dict mapping description -> category.
    """
    if not model:
        return {}

    prompt = f"""
    Categorize the following bank transaction descriptions into one of these categories:
    Food, Transport, Bills, Groceries, Shopping, Entertainment, Health, Income, Education, Others.

    Return the result ONLY as a JSON object where the keys are the descriptions and the values are the categories.

    Descriptions:
    {json.dumps(descriptions)}
    """

    try:
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"AI Categorization Error: {e}")
        return {}


def get_financial_advice(summary_data):
    """
    Generates financial advice based on spending habits.
    Falls back to rule-based advice if Gemini API is not available.
    """
    if model:
        prompt = f"""
        You are a professional financial advisor. Based on the following monthly spending summary,
        provide 3 concise, actionable pieces of advice for the user to improve their financial health.
        Format each as a numbered point. Keep it encouraging and professional.

        Summary:
        {json.dumps(summary_data)}
        """
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            pass  # Fall through to rule-based advice

    # Fallback Advice
    income = summary_data.get("income", 0)
    expenses = summary_data.get("expenses", 0)
    savings_rate = summary_data.get("savings_rate", 0)
    top_cats = summary_data.get("top_categories", {})

    advice_parts = []

    if savings_rate > 30:
        advice_parts.append(
            "<strong>Great savings rate!</strong> You're saving {:.0f}% of your income. "
            "Consider investing the surplus to grow your wealth.".format(savings_rate)
        )
    elif savings_rate > 10:
        advice_parts.append(
            "<strong>Healthy savings rate</strong> at {:.0f}%. Try the 50/30/20 rule: "
            "50% needs, 30% wants, 20% savings.".format(savings_rate)
        )
    else:
        advice_parts.append(
            "<strong>Low savings rate</strong> ({:.0f}%). Review your top spending categories "
            "and identify areas where you can reduce expenses.".format(savings_rate)
        )

    if top_cats:
        top_cat = max(top_cats, key=top_cats.get)
        top_amt = top_cats[top_cat]
        pct_of_expenses = (top_amt / expenses * 100) if expenses > 0 else 0

        if pct_of_expenses > 30:
            advice_parts.append(
                "<strong>{}</strong> is your biggest expense ({:.0f}% of total spending). "
                "Look for ways to optimize this category.".format(
                    top_cat, pct_of_expenses
                )
            )
        else:
            advice_parts.append(
                "Your spending is well-distributed. "
                "<strong>{}</strong> leads at {:.0f}% of expenses.".format(
                    top_cat, pct_of_expenses
                )
            )

    if income > 0:
        advice_parts.append(
            "<strong>Pro Tip:</strong> Set up automatic transfers of {:.0f}% of each income deposit "
            "to a separate savings account.".format(
                min(20, max(5, savings_rate * 0.5 + 10))
            )
        )
    else:
        advice_parts.append(
            "<strong>Track your income:</strong> Include salary/freelance credits for better analysis."
        )

    return "<br><br>".join(advice_parts)


def detect_anomalies(df):
    """
    Identifies unusually large transactions compared to category averages.
    Uses 2.5x threshold instead of 3x for better sensitivity.
    """
    anomalies = []
    expense_df = df[df['category'] != 'Income'].copy()

    if expense_df.empty:
        return anomalies

    for cat in expense_df['category'].unique():
        cat_df = expense_df[expense_df['category'] == cat]
        if len(cat_df) < 2:
            continue

        avg = cat_df['amount'].abs().mean()
        std = cat_df['amount'].abs().std()

        for idx, row in cat_df.iterrows():
            amount_abs = abs(row['amount'])
            # Flag if > 2.5x average AND above a minimum threshold
            if amount_abs > 2.5 * avg and amount_abs > 500:
                anomalies.append({
                    "date": row['date'],
                    "description": row['description'],
                    "amount": row['amount'],
                    "category": cat,
                    "reason": f"~{amount_abs/avg:.1f}x higher than avg ({cat})"
                })

    anomalies.sort(key=lambda x: abs(x['amount']), reverse=True)
    return anomalies

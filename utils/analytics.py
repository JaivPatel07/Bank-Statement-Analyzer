import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta


def calculate_health_score(df):
    income = df[df['category'] == 'Income']['amount'].sum()
    expenses = abs(df[df['category'] != 'Income']['amount'].sum())

    if income == 0:
        return 5  # Minimal score if no income data

    savings_rate = (income - expenses) / income
    savings_score = max(0, min(50, savings_rate * 100))

    expense_cats = df[df['category'] != 'Income'].groupby('category')['amount'].sum().abs()
    if len(expense_cats) > 0 and expenses > 0:
        max_cat_pct = expense_cats.max() / expenses
        diversity_score = (1 - max_cat_pct) * 30
    else:
        diversity_score = 15

    income_score = 20

    score = savings_score + diversity_score + income_score
    return round(max(0, min(100, score)))


def get_top_merchants(df, top_n=8):
    expenses = df[df['category'] != 'Income'].copy()
    if expenses.empty:
        return pd.DataFrame(columns=['description', 'amount'])

    top_merchants = (
        expenses.groupby('description')['amount']
        .sum()
        .abs()
        .reset_index()
        .sort_values('amount', ascending=False)
        .head(top_n)
    )
    return top_merchants


def forecast_spending(df):
    expenses = df[df['category'] != 'Income'].copy()
    if expenses.empty:
        return 0, []

    expenses['date'] = pd.to_datetime(expenses['date'])
    daily_spend = expenses.groupby(expenses['date'].dt.date)['amount'].sum().abs().reset_index()
    daily_spend.columns = ['date', 'amount']
    daily_spend['date'] = pd.to_datetime(daily_spend['date'])

    if len(daily_spend) < 2:
        return float(daily_spend['amount'].sum()), []

    daily_spend['date_ordinal'] = daily_spend['date'].apply(lambda x: x.toordinal())

    X = daily_spend[['date_ordinal']].values
    y = daily_spend['amount'].values

    model = LinearRegression()
    model.fit(X, y)

    last_date = daily_spend['date'].max()
    future_dates = [last_date + timedelta(days=i) for i in range(1, 31)]
    future_ordinals = np.array([d.toordinal() for d in future_dates]).reshape(-1, 1)

    predictions = model.predict(future_ordinals)
    predictions = np.clip(predictions, 0, None)
    total_forecast = float(predictions.sum())

    return max(0, total_forecast), list(zip(future_dates, predictions.tolist()))

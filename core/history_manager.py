import pandas as pd
from core.db_handler import read_query, execute_query
from datetime import datetime

def archive_period(start_date=None, end_date=None):

    expenses_df = read_query("SELECT * FROM expenses")
    budget_df = read_query("SELECT * FROM budgets")

    if expenses_df.empty:
        print("No expenses found")
        return

    expenses_df["Date"] = pd.to_datetime(expenses_df["Date"], errors="coerce")
    expenses_df["Amount"] = pd.to_numeric(expenses_df.get("Amount", []), errors="coerce").fillna(0.0)

    today = datetime.now()
    if not start_date:
        start_date = today.replace(day=1).strftime("%Y-%m-%d")
    if not end_date:
        end_date = today.strftime("%Y-%m-%d")

    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)

    period_expenses = expenses_df[
        (expenses_df["Date"] >= start_dt)
        & (expenses_df["Date"] <= end_dt)
    ]

    total_spent = period_expenses["Amount"].sum()

    latest_budget = 0.0
    if not budget_df.empty and "Budget" in budget_df.columns:
        latest_budget = pd.to_numeric(budget_df.iloc[-1]["Budget"], errors="coerce")
        latest_budget = float(latest_budget) if not pd.isna(latest_budget) else 0.0

    savings = latest_budget - total_spent
    period_label = f"{start_date} to {end_date}"

    query = "INSERT OR REPLACE INTO history (Month, Total_Spent, Budget, Savings) VALUES (?, ?, ?, ?)"
    execute_query(query, (period_label, float(total_spent), float(latest_budget), float(savings)))

    print(f"History saved for period: {period_label}")
    
def load_history():
    return read_query("SELECT * FROM history")

def get_month_history(month):
    return read_query("SELECT * FROM history WHERE Month = ?", (month,))

def best_savings_month():
    df = read_query("SELECT * FROM history ORDER BY Savings DESC LIMIT 1")
    if df.empty:
        return None
    return df.iloc[0]

def worst_spending_month():
    df = read_query("SELECT * FROM history ORDER BY Total_Spent DESC LIMIT 1")
    if df.empty:
        return None
    return df.iloc[0]

def average_monthly_spending():
    df = read_query("SELECT AVG(Total_Spent) as avg_spent FROM history")
    if df.empty or pd.isna(df.iloc[0]["avg_spent"]):
        return 0.0
    return float(df.iloc[0]["avg_spent"])

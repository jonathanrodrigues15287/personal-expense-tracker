import pandas as pd
from core.csv_handler import (
    read_csv,
    save_monthly_history
)
from datetime import datetime

EXPENSES_FILE = "data/expenses.csv"
BUDGET_FILE = "data/budgets.csv"
HISTORY_FILE = "data/monthly_history.csv"

def archive_period(start_date=None, end_date=None):

    expenses_df = read_csv(EXPENSES_FILE)
    budget_df = read_csv(BUDGET_FILE)

    if expenses_df.empty:
        print("No expenses found")
        return

    expenses_df["Date"] = pd.to_datetime(expenses_df["Date"], errors="coerce")
    expenses_df["Amount"] = pd.to_numeric(expenses_df.get("Amount", []), errors="coerce").fillna(0.0)

    # Resolve defaults
    today = datetime.now()
    if not start_date:
        start_date = today.replace(day=1).strftime("%Y-%m-%d")
    if not end_date:
        end_date = today.strftime("%Y-%m-%d")

    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)

    # Filter expenses within the chosen range (inclusive)
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

    history_data = {
        "Month": period_label,
        "Total_Spent": total_spent,
        "Budget": latest_budget,
        "Savings": savings
    }

    save_monthly_history(history_data)

    print(f"History saved for period: {period_label}")
    
def load_history():
    df = read_csv(HISTORY_FILE)
    return df

def get_month_history(month):
    df = read_csv(HISTORY_FILE)
    filtered_df = df[df["Month"] == month]
    return filtered_df

def best_savings_month():
    df = read_csv(HISTORY_FILE)
    if df.empty or "Savings" not in df.columns:
        return None
    df["Savings"] = pd.to_numeric(df["Savings"], errors="coerce")
    valid = df.dropna(subset=["Savings"])
    if valid.empty:
        return None
    return valid.loc[valid["Savings"].idxmax()]

def worst_spending_month():
    df = read_csv(HISTORY_FILE)
    if df.empty or "Total_Spent" not in df.columns:
        return None
    df["Total_Spent"] = pd.to_numeric(df["Total_Spent"], errors="coerce")
    valid = df.dropna(subset=["Total_Spent"])
    if valid.empty:
        return None
    return valid.loc[valid["Total_Spent"].idxmax()]

def average_monthly_spending():
    df = read_csv(HISTORY_FILE)
    if df.empty or "Total_Spent" not in df.columns:
        return 0.0
    return pd.to_numeric(df["Total_Spent"], errors="coerce").fillna(0.0).mean()

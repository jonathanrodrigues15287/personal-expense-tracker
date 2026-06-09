import pandas as pd
from core.csv_handler import read_csv

BUDGET_FILE = "data/budgets.csv"
EXPENSES_FILE = "data/expenses.csv"


def calculate_balance():

    budget_df = read_csv(BUDGET_FILE)
    expenses_df = read_csv(EXPENSES_FILE)

    from datetime import datetime
    current_month = datetime.now().strftime("%Y-%m")

    if budget_df.empty or "Month" not in budget_df.columns:
        latest_budget = 0.0
    else:
        month_budget = budget_df[budget_df["Month"] == current_month]
        if not month_budget.empty:
            latest_budget = pd.to_numeric(month_budget.iloc[-1]["Budget"], errors='coerce')
            latest_budget = float(latest_budget) if not pd.isna(latest_budget) else 0.0
        else:
            latest_budget = 0.0

    if expenses_df.empty or "Amount" not in expenses_df.columns:
        total_expenses = 0.0
    else:
        expenses_df["Date"] = pd.to_datetime(expenses_df["Date"], errors='coerce')
        expenses_df["Amount"] = pd.to_numeric(expenses_df["Amount"], errors='coerce').fillna(0.0)
        current_expenses = expenses_df[expenses_df["Date"].dt.strftime("%Y-%m") == current_month]
        total_expenses = current_expenses["Amount"].sum()

    balance = latest_budget - total_expenses

    return balance

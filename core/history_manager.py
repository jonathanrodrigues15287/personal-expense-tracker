import pandas as pd
from core.csv_handler import (
    read_csv,
    save_monthly_history
)

EXPENSES_FILE = "data/expenses.csv"
BUDGET_FILE = "data/budgets.csv"
HISTORY_FILE = "data/monthly_history.csv"

def archive_current_month():
    expenses_df = read_csv(EXPENSES_FILE)
    budget_df = read_csv(BUDGET_FILE)

    if expenses_df.empty:
        print("No expenses found")
        return

    expenses_df["Date"] = pd.to_datetime(expenses_df["Date"])

    current_month = (
        expenses_df["Date"]
        .dt.strftime("%Y-%m")
        .iloc[-1]
    )

    monthly_expenses = expenses_df[
        expenses_df["Date"]
        .dt.strftime("%Y-%m") == current_month
    ]

    total_spent = monthly_expenses["Amount"].sum()
    
    if budget_df.empty:
        latest_budget = 0.0
    else:
        latest_budget = budget_df.iloc[-1]["Budget"]
        
    savings = latest_budget - total_spent

    history_data = {
        "Month": current_month,
        "Total_Spent": total_spent,
        "Budget": latest_budget,
        "Savings": savings
    }

    save_monthly_history(history_data)

    print("Monthly History Saved")
    
def load_history():
    df = read_csv(HISTORY_FILE)
    return df

def get_month_history(month):
    df = read_csv(HISTORY_FILE)
    filtered_df = df[df["Month"] == month]
    return filtered_df

def best_savings_month():
    df = read_csv(HISTORY_FILE)
    if df.empty: return None
    best_month = df.loc[df["Savings"].idxmax()]
    return best_month

def worst_spending_month():
    df = read_csv(HISTORY_FILE)
    if df.empty: return None
    worst_month = df.loc[df["Total_Spent"].idxmax()]
    return worst_month

def average_monthly_spending():
    df = read_csv(HISTORY_FILE)
    if df.empty: return 0.0
    return df["Total_Spent"].mean()

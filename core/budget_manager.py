import pandas as pd
from core.db_handler import read_query, execute_query

def calculate_balance():
    from datetime import datetime
    current_month = datetime.now().strftime("%Y-%m")

    budget_df = read_query("SELECT Budget FROM budgets WHERE Month = ?", (current_month,))
    
    if budget_df.empty:
        latest_budget = 0.0
    else:
        latest_budget = pd.to_numeric(budget_df.iloc[-1]["Budget"], errors='coerce')
        latest_budget = float(latest_budget) if not pd.isna(latest_budget) else 0.0

    expenses_df = read_query("SELECT SUM(Amount) as Total FROM expenses WHERE Date LIKE ?", (f"{current_month}-%",))
    
    if expenses_df.empty or pd.isna(expenses_df.iloc[0]["Total"]):
        total_expenses = 0.0
    else:
        total_expenses = float(expenses_df.iloc[0]["Total"])

    balance = latest_budget - total_expenses
    return balance

def save_budget(month, budget):
    query = "INSERT OR REPLACE INTO budgets (Month, Budget) VALUES (?, ?)"
    execute_query(query, (month, budget))

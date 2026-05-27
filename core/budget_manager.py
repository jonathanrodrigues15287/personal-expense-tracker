from core.csv_handler import read_csv

BUDGET_FILE = "data/budgets.csv"
EXPENSES_FILE = "data/expenses.csv"


def calculate_balance():

    budget_df = read_csv(BUDGET_FILE)
    expenses_df = read_csv(EXPENSES_FILE)

    if budget_df.empty:
        latest_budget = 0.0
    else:
        latest_budget = budget_df.iloc[-1]["Budget"]

    if expenses_df.empty or "Amount" not in expenses_df.columns:
        total_expenses = 0.0
    else:
        total_expenses = expenses_df["Amount"].sum()

    balance = latest_budget - total_expenses

    return balance

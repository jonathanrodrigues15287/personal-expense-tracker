import pandas as pd
import os

EXPENSES_FILE = "data/expenses.csv"
BUDGET_FILE = "data/budgets.csv"
HISTORY_FILE = "data/monthly_history.csv"

def initialize_csv_files():
    if not os.path.exists(EXPENSES_FILE):
        expenses_df = pd.DataFrame(columns=[
            "Expense_ID",
            "Date",
            "Category",
            "Amount",
            "Description"
        ])
        expenses_df.to_csv(EXPENSES_FILE, index=False)
      
    if not os.path.exists(BUDGET_FILE):
        budget_df = pd.DataFrame(columns=[
            "Month",
            "Budget"
        ])
        budget_df.to_csv(BUDGET_FILE, index=False)

    if not os.path.exists(HISTORY_FILE):
        history_df = pd.DataFrame(columns=[
            "Month",
            "Total_Spent",
            "Budget",
            "Savings"
        ])
        history_df.to_csv(HISTORY_FILE, index=False)

def read_csv(file_path):
    return pd.read_csv(file_path)

def append_expense(expense_data):
    df = pd.read_csv(EXPENSES_FILE)
    new_row = pd.DataFrame([expense_data])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(EXPENSES_FILE, index=False)

def save_budget(month, budget):
    df = pd.read_csv(BUDGET_FILE)
    new_row = pd.DataFrame([{
        "Month": month,
        "Budget": budget
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(BUDGET_FILE, index=False)

def save_monthly_history(history_data):
    df = pd.read_csv(HISTORY_FILE)
    new_row = pd.DataFrame([history_data])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(HISTORY_FILE, index=False)

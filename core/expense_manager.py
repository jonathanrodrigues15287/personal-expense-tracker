import pandas as pd
from core.db_handler import read_query, execute_query
import logging

def add_expense(expense_id,
                date,
                category,
                amount,
                description):

    query = '''
        INSERT INTO expenses (Expense_ID, Date, Category, Amount, Description)
        VALUES (?, ?, ?, ?, ?)
    '''
    execute_query(query, (expense_id, date, category, amount, description))
    logging.info("Expense Added Successfully")

def view_all_expenses():
    return read_query("SELECT * FROM expenses")

def calculate_total_expenses():
    df = read_query("SELECT SUM(Amount) as Total FROM expenses")
    if df.empty or pd.isna(df.iloc[0]["Total"]):
        return 0.0
    return float(df.iloc[0]["Total"])

def category_expenses():
    df = read_query("SELECT Category, SUM(Amount) as Total FROM expenses GROUP BY Category")
    if df.empty:
        return pd.Series(dtype=float)
    df = df.set_index("Category")
    return df["Total"]

def daily_expenses():
    df = read_query("SELECT Date, SUM(Amount) as Total FROM expenses GROUP BY Date")
    if df.empty:
        return pd.Series(dtype=float)
    df = df.set_index("Date")
    return df["Total"]

def delete_expense(expense_id):
    query = "DELETE FROM expenses WHERE Expense_ID = ?"
    execute_query(query, (expense_id,))
    logging.info("Expense Deleted Successfully")

def edit_expense(expense_id,
                 new_date=None,
                 new_category=None,
                 new_amount=None,
                 new_description=None):

    updates = []
    params = []
    
    if new_date is not None:
        updates.append("Date = ?")
        params.append(new_date)

    if new_category is not None:
        updates.append("Category = ?")
        params.append(new_category)

    if new_amount is not None:
        updates.append("Amount = ?")
        params.append(new_amount)

    if new_description is not None:
        updates.append("Description = ?")
        params.append(new_description)

    if not updates:
        return

    query = f"UPDATE expenses SET {', '.join(updates)} WHERE Expense_ID = ?"
    params.append(expense_id)
    
    execute_query(query, tuple(params))
    logging.info("Expense Updated Successfully")

def filter_by_category(category):
    return read_query("SELECT * FROM expenses WHERE Category = ?", (category,))

def filter_by_date(date):
    return read_query("SELECT * FROM expenses WHERE Date = ?", (date,))

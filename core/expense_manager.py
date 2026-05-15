import pandas as pd
from core.csv_handler import read_csv, append_expense

EXPENSES_FILE = "data/expenses.csv"

def add_expense(expense_id,
                date,
                category,
                amount,
                description):

    expense_data = {
        "Expense_ID": expense_id,
        "Date": date,
        "Category": category,
        "Amount": amount,
        "Description": description
    }

    append_expense(expense_data)

    print("Expense Added Successfully")

def view_all_expenses():

    df = read_csv(EXPENSES_FILE)

    return df

def calculate_total_expenses():

    df = read_csv(EXPENSES_FILE)

    return df["Amount"].sum()

def category_expenses():

    df = read_csv(EXPENSES_FILE)

    category_totals = df.groupby("Category")["Amount"].sum()

    return category_totals

def daily_expenses():

    df = read_csv(EXPENSES_FILE)

    daily_totals = df.groupby("Date")["Amount"].sum()

    return daily_totals

def delete_expense(expense_id):

    df = read_csv(EXPENSES_FILE)

    df = df[df["Expense_ID"] != expense_id]

    df.to_csv(EXPENSES_FILE, index=False)

    print("Expense Deleted Successfully")

def edit_expense(expense_id,
                 new_date=None,
                 new_category=None,
                 new_amount=None,
                 new_description=None):

    df = read_csv(EXPENSES_FILE)

    index = df[df["Expense_ID"] == expense_id].index

    if len(index) == 0:
        print("Expense ID Not Found")
        return

    index = index[0]

    if new_date is not None:
        df.at[index, "Date"] = new_date

    if new_category is not None:
        df.at[index, "Category"] = new_category

    if new_amount is not None:
        df.at[index, "Amount"] = new_amount

    if new_description is not None:
        df.at[index, "Description"] = new_description

    df.to_csv(EXPENSES_FILE, index=False)

    print("Expense Updated Successfully")

def filter_by_category(category):

    df = read_csv(EXPENSES_FILE)

    filtered_df = df[df["Category"] == category]

    return filtered_df

def filter_by_date(date):

    df = read_csv(EXPENSES_FILE)

    filtered_df = df[df["Date"] == date]

    return filtered_df

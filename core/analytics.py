import pandas as pd
from core.csv_handler import read_csv

EXPENSES_FILE = "data/expenses.csv"

def total_spending():
    df = read_csv(EXPENSES_FILE)
    if df.empty or "Amount" not in df.columns: return 0.0
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    return df["Amount"].sum()

def average_daily_spending():
    df = read_csv(EXPENSES_FILE)
    if df.empty or "Amount" not in df.columns: return 0.0
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    daily_totals = df.groupby("Date")["Amount"].sum()
    return daily_totals.mean()

def highest_expense():
    df = read_csv(EXPENSES_FILE)
    if df.empty or "Amount" not in df.columns: return None
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    highest = df.loc[df["Amount"].idxmax()]
    return highest

def lowest_expense():
    df = read_csv(EXPENSES_FILE)
    if df.empty or "Amount" not in df.columns: return None
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    lowest = df.loc[df["Amount"].idxmin()]
    return lowest

def category_analysis():
    df = read_csv(EXPENSES_FILE)
    if df.empty: return pd.Series(dtype=float)
    category_totals = (
        df.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )
    return category_totals

def most_spent_category():
    categories = category_analysis()
    if categories.empty: return "None"
    return categories.idxmax()

def daily_spending_trend():
    df = read_csv(EXPENSES_FILE)
    if df.empty: return pd.Series(dtype=float)
    daily_totals = (
        df.groupby("Date")["Amount"]
        .sum()
        .sort_index()
    )
    return daily_totals

def monthly_summary():
    df = read_csv(EXPENSES_FILE)
    if df.empty: return pd.Series(dtype=float)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.strftime("%Y-%m")
    monthly_totals = (
        df.groupby("Month")["Amount"]
        .sum()
    )
    return monthly_totals

def total_number_of_expenses():
    df = read_csv(EXPENSES_FILE)
    return len(df)

def expenses_above(amount_limit):
    df = read_csv(EXPENSES_FILE)
    filtered_df = df[df["Amount"] > amount_limit]
    return filtered_df

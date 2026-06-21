import pandas as pd
from core.db_handler import read_query

def total_spending():
    df = read_query("SELECT SUM(Amount) as Total FROM expenses")
    if df.empty or pd.isna(df.iloc[0]["Total"]):
        return 0.0
    return float(df.iloc[0]["Total"])

def average_daily_spending():
    df = read_query("SELECT Date, SUM(Amount) as Total FROM expenses GROUP BY Date")
    if df.empty:
        return 0.0
    return df["Total"].mean()

def highest_expense():
    df = read_query("SELECT * FROM expenses ORDER BY Amount DESC LIMIT 1")
    if df.empty:
        return None
    return df.iloc[0]

def lowest_expense():
    df = read_query("SELECT * FROM expenses ORDER BY Amount ASC LIMIT 1")
    if df.empty:
        return None
    return df.iloc[0]

def category_analysis():
    df = read_query("SELECT Category, SUM(Amount) as Total FROM expenses GROUP BY Category ORDER BY Total DESC")
    if df.empty:
        return pd.Series(dtype=float)
    df = df.set_index("Category")
    return df["Total"]

def most_spent_category():
    categories = category_analysis()
    if categories.empty:
        return "None"
    return categories.idxmax()

def daily_spending_trend():
    df = read_query("SELECT Date, SUM(Amount) as Total FROM expenses GROUP BY Date ORDER BY Date ASC")
    if df.empty:
        return pd.Series(dtype=float)
    df = df.set_index("Date")
    return df["Total"]

def monthly_summary():
    df = read_query("SELECT Date, Amount FROM expenses")
    if df.empty:
        return pd.Series(dtype=float)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    if df.empty:
        return pd.Series(dtype=float)
    df["Month"] = df["Date"].dt.strftime("%Y-%m")
    return df.groupby("Month")["Amount"].sum()

def total_number_of_expenses():
    df = read_query("SELECT COUNT(*) as Count FROM expenses")
    if df.empty or pd.isna(df.iloc[0]["Count"]):
        return 0
    return int(df.iloc[0]["Count"])

def expenses_above(amount_limit):
    return read_query("SELECT * FROM expenses WHERE Amount > ?", (amount_limit,))

import pandas as pd
from core.csv_handler import read_csv

EXPENSES_FILE = "data/expenses.csv"


def _load_amount_series(df):
    if df.empty or "Amount" not in df.columns:
        return pd.Series(dtype=float)
    return pd.to_numeric(df["Amount"], errors="coerce")


def _normalize_amounts(df):
    if df.empty or "Amount" not in df.columns:
        return df
    df = df.copy()
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    return df


def total_spending():
    df = read_csv(EXPENSES_FILE)
    return _load_amount_series(df).sum()


def average_daily_spending():
    df = read_csv(EXPENSES_FILE)
    df = _normalize_amounts(df)
    if df.empty or df["Amount"].dropna().empty:
        return 0.0
    daily_totals = df.groupby("Date")["Amount"].sum()
    return daily_totals.mean()


def highest_expense():
    df = read_csv(EXPENSES_FILE)
    df = _normalize_amounts(df)
    valid = df.dropna(subset=["Amount"])
    if valid.empty:
        return None
    return valid.loc[valid["Amount"].idxmax()]


def lowest_expense():
    df = read_csv(EXPENSES_FILE)
    df = _normalize_amounts(df)
    valid = df.dropna(subset=["Amount"])
    if valid.empty:
        return None
    return valid.loc[valid["Amount"].idxmin()]


def category_analysis():
    df = read_csv(EXPENSES_FILE)
    if df.empty or "Category" not in df.columns:
        return pd.Series(dtype=float)
    df = _normalize_amounts(df)
    return (
        df.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )


def most_spent_category():
    categories = category_analysis()
    if categories.empty:
        return "None"
    return categories.idxmax()


def daily_spending_trend():
    df = read_csv(EXPENSES_FILE)
    if df.empty:
        return pd.Series(dtype=float)
    df = _normalize_amounts(df)
    if df["Amount"].dropna().empty:
        return pd.Series(dtype=float)
    return (
        df.groupby("Date")["Amount"]
        .sum()
        .sort_index()
    )


def monthly_summary():
    df = read_csv(EXPENSES_FILE)
    if df.empty:
        return pd.Series(dtype=float)
    df = _normalize_amounts(df)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    if df.empty:
        return pd.Series(dtype=float)
    df["Month"] = df["Date"].dt.strftime("%Y-%m")
    return df.groupby("Month")["Amount"].sum()


def total_number_of_expenses():
    df = read_csv(EXPENSES_FILE)
    return len(df)


def expenses_above(amount_limit):
    df = read_csv(EXPENSES_FILE)
    df = _normalize_amounts(df)
    return df[df["Amount"] > amount_limit]

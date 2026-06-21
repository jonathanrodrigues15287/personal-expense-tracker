import sqlite3
import pandas as pd
import os

DB_FILE = "data/expense_tracker.db"
EXPENSES_CSV = "data/expenses.csv"
BUDGET_CSV = "data/budgets.csv"
HISTORY_CSV = "data/monthly_history.csv"

def get_connection():
    return sqlite3.connect(DB_FILE)

def initialize_database():
    if not os.path.exists("data"):
        os.makedirs("data")
        
    db_exists = os.path.exists(DB_FILE)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            Expense_ID TEXT PRIMARY KEY,
            Date TEXT,
            Category TEXT,
            Amount REAL,
            Description TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            Month TEXT PRIMARY KEY,
            Budget REAL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            Month TEXT PRIMARY KEY,
            Total_Spent REAL,
            Budget REAL,
            Savings REAL
        )
    ''')
    
    conn.commit()
    conn.close()
    
    # Migrate data if DB didn't exist and CSVs do
    if not db_exists:
        _migrate_csv_data()

def _migrate_csv_data():
    conn = get_connection()
    
    if os.path.exists(EXPENSES_CSV):
        try:
            df = pd.read_csv(EXPENSES_CSV)
            if not df.empty:
                df.to_sql('expenses', conn, if_exists='append', index=False)
                print("Migrated expenses.csv to database.")
        except Exception as e:
            print(f"Failed to migrate expenses.csv: {e}")
            
    if os.path.exists(BUDGET_CSV):
        try:
            df = pd.read_csv(BUDGET_CSV)
            if not df.empty:
                df.to_sql('budgets', conn, if_exists='append', index=False)
                print("Migrated budgets.csv to database.")
        except Exception as e:
            print(f"Failed to migrate budgets.csv: {e}")
            
    if os.path.exists(HISTORY_CSV):
        try:
            df = pd.read_csv(HISTORY_CSV)
            if not df.empty:
                df.to_sql('history', conn, if_exists='append', index=False)
                print("Migrated monthly_history.csv to database.")
        except Exception as e:
            print(f"Failed to migrate monthly_history.csv: {e}")

    conn.close()

def read_query(query, params=None):
    try:
        with get_connection() as conn:
            if params:
                return pd.read_sql_query(query, conn, params=params)
            else:
                return pd.read_sql_query(query, conn)
    except Exception as e:
        print(f"Database read error: {e}")
        return pd.DataFrame()

def execute_query(query, params=None):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
    except Exception as e:
        print(f"Database execute error: {e}")

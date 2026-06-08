# Personal Expense Tracker
A mobile-first expense tracking app built with **Python + Kivy**, featuring real-time analytics, chart visualisations, and CSV-backed persistent storage.

---

## Download
Pre-built Windows executable available on the [Releases](https://github.com/jonathanrodrigues15287/personal-expense-tracker/releases) page — no Python installation required.

---

## Screenshots

| Dashboard | Analytics |
|-----------|-----------|
| ![Dashboard](screenshots/dashboard.png) | ![Analytics](screenshots/analytics.png) |

| Manage Expenses |
|-----------------|
| ![Manage](screenshots/manage.png) |

---

## Features
- **Dashboard** — live balance, total spend, and expense count at a glance
- **Add & manage expenses** — date, category, amount, and description with input validation
- **Monthly budgeting** — set a budget per month and track remaining balance
- **Archive periods** — snapshot any custom date range to monthly history
- **Analytics screen** — four charts generated with Matplotlib:
  - Spending by Category (line)
  - Category-wise Trend (line)
  - Monthly Spending Trend (line)
  - Daily Expense Trend (line)
- **Dark glass-card UI** — custom Kivy design system with rounded cards, accent colours, and a bottom navigation bar
- **CSV storage** — no database required; data lives in `data/` as plain CSV files

---

## Project Structure
```text
expense_tracker/
├── core/
│   ├── csv_handler.py          # Read/write CSV files
│   ├── budget_manager.py       # Balance calculations
│   ├── expense_manager.py      # CRUD operations for expenses
│   ├── history_manager.py      # Period archiving & history queries
│   └── analytics.py            # Aggregations and statistics
│
├── graphs/
│   ├── category_graph.py       # Category line charts
│   ├── spending_graph.py       # Monthly spending chart
│   └── daily_expense_graph.py  # Daily trend chart
│
├── ui/
│   ├── theme.py                # Design tokens & widget factories
│   ├── widgets.py              # Layout primitives (nav, header, scroll)
│   ├── dashboard.py            # Home screen
│   └── screens.py              # Analytics & Manage screens
│
├── data/                       # Auto-created on first run
│   ├── expenses.csv
│   ├── budgets.csv
│   └── monthly_history.csv
│
├── ExpenseTracker.spec         # PyInstaller build configuration
└── main.py                     # App entry point
```

---

## Prerequisites
- Python 3.8 or higher
- pip

---

## Installation
```bash
# 1. Clone the repository
git clone https://github.com/jonathanrodrigues15287/personal-expense-tracker.git
# 2. Move into the project directory
cd personal-expense-tracker
# 3. Install dependencies
pip install -r requirements.txt
# 4. Run the app
python main.py
```

The `data/` directory and CSV files are created automatically on first launch.

---

## Building the Executable
The repo includes `ExpenseTracker.spec` for reproducible PyInstaller builds:
```bash
pip install pyinstaller
pyinstaller ExpenseTracker.spec
```
The compiled executable will be output to `dist/ExpenseTracker.exe`.

---

## Tech Stack
- Python
- Kivy
- Pandas
- Matplotlib
- CSV Storage

---

## Future Improvements
- Export reports as PDF/Excel
- AI-powered spending insights
- Recurring expense reminders

---

## License
This project is open-source and available under the MIT License.

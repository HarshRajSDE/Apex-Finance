# Personal Expense and Budget Tracker

A beginner-friendly, menu-driven Python program to track income and expenses, set a monthly budget, and see where your money goes. It also generates a simple HTML dashboard you can open in any browser.

Built for **Computational Thinking and Programming (2026CSAE100)** at Bennett University.

## Quick Start: Interactive Modern Web Dashboard

A modern fintech-styled interactive web dashboard is available alongside the terminal program:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Launch the web application:**
   ```bash
   streamlit run app.py
   ```

3. Open `http://localhost:8501` in your browser to experience the real-time financial dashboard, interactive Plotly visualizations, transactions ledger with filtering, and live budget tracking.

---

## Features

- Add income and expense entries with date, amount, category and a short note
- Set a monthly budget and get alerts (Safe / Warning at 80%+ / Exceeded)
- Monthly report with income, expenses, balance, savings rate and top spending category
- Category-wise spending breakdown with a text bar chart
- View all saved transactions
- Clear all data and start fresh (with a confirmation step)
- Input validation for amounts, dates (`YYYY-MM-DD`) and months (`YYYY-MM`)
- Visual HTML dashboard with summary cards, category bars and a transaction table
- Data saved automatically in plain files (no database needed)

## Requirements

- Python 3.8 or newer
- No external libraries. Only the Python standard library (`csv`, `os`, `datetime`) is used.

Check your Python version:

```bash
python --version
```

## Getting Started

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
   ```

2. **Run the tracker**

   ```bash
   python expense_tracker.py
   ```

   On some systems you may need `python3` instead of `python`.

3. **Generate the dashboard** (optional)

   ```bash
   python dashboard.py
   ```

   Enter a month (or press Enter for the current month), then double-click the generated `dashboard.html` to open it in your browser.

## How to Use

When you run `expense_tracker.py`, you will see this menu:

```
===== PERSONAL EXPENSE AND BUDGET TRACKER =====
1. Add income
2. Add expense
3. Set monthly budget
4. View monthly report
5. View all transactions
6. Clear all data
7. Exit
```

Typical first-time flow:

1. Choose **3** and set your monthly budget
2. Choose **1** to add income (for example pocket money)
3. Choose **2** to add expenses and pick a category
4. Choose **4** to see your monthly report and budget status

### Expense categories

Food, Transport, Shopping, Education, Entertainment, Bills, Others

### Budget alerts

| Budget used | Status |
|-------------|--------|
| Below 80% | Safe |
| 80% to 100% | Warning |
| Exactly 100% | Notice |
| Above 100% | Alert: budget exceeded |

## Project Structure

```
.
├── app.py               # Modern interactive Streamlit fintech web application
├── requirements.txt     # Python dependencies (Streamlit, Pandas, Plotly)
├── .streamlit/          # Streamlit theme & server configuration (Dark Fintech theme)
├── expense_tracker.py   # Original terminal program (intact & fully reusable)
├── dashboard.py         # Static HTML dashboard generator (original)
├── expenses.csv         # Persistent transaction ledger
├── budget.txt           # Persistent monthly budget limit
└── dashboard.html       # Auto-created static dashboard
```

`expenses.csv`, `budget.txt` and `dashboard.html` are created automatically when you run the program, so they are not part of the repository.

`dashboard.py` imports functions from `expense_tracker.py`, so keep both files in the same folder.

## Data Format

Transactions are stored in `expenses.csv`:

```
date,type,category,amount,description
2026-11-17,expense,Food,250.0,lunch
2026-11-18,income,Income,2000.0,pocket money
```

## Team

| Member | Responsibility |
|--------|----------------|
| Ridhima | `show_menu()`, `main()` |
| Anoushka | `set_budget()`, `print_line()` |
| Aatirth | `load_transactions()`, `save_to_csv()`, `calculate_totals()` |
| Harsh | `check_budget_status()` |
| Srishthi | `get_category_breakdown()`, `generate_summary()`, `plot_spending_chart()` |

## Possible Future Improvements

- Edit and delete individual transactions
- Monthly budgets per category
- Export reports to PDF
- Charts using a library such as matplotlib

## License

This project was created for academic purposes. Add a license of your choice (for example MIT) if you plan to share it more widely.

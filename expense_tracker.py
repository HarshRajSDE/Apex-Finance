"""
Personal Expense and Budget Tracker
Bennett University - 2026CSAE100 (Computational Thinking and Programming)

Team:
  Ridhima  (S26CSEU1925) - show_menu(), main()
  Anoushka (S26CSEU1922) - set_budget(), print_line()
  Aatirth  (S26CSEU1913) - load_transactions(), save_to_csv(), calculate_totals()
  Harsh    (S26CSEU1935) - check_budget_status()
  Srishthi (S26CSEU1939) - get_category_breakdown(), generate_summary(), plot_spending_chart()

Data is stored in two small files:
  expenses.csv - every transaction (one row per transaction)
  budget.txt   - the monthly budget number
"""

import csv
import os
from datetime import datetime

# ---------------------------------------------------------------
# Constants (values that never change while the program runs)
# ---------------------------------------------------------------
FILE_NAME = "expenses.csv"
BUDGET_FILE = "budget.txt"
HEADERS = ["date", "type", "category", "amount", "description"]
CATEGORIES = ["Food", "Transport", "Shopping", "Education",
              "Entertainment", "Bills", "Others"]


# ---------------------------------------------------------------
# Small helper functions
# ---------------------------------------------------------------
def print_line():
    """Prints a line to separate sections. (Anoushka)"""
    print("-" * 50)


def get_valid_amount(message):
    """Keeps asking until the user types a positive number."""
    while True:
        try:
            amount = float(input(message))
            if amount <= 0:
                print("Amount must be more than 0. Try again.")
            else:
                return amount
        except ValueError:
            print("Please enter a number only (example: 250).")


def get_valid_date():
    """Asks for a date as YYYY-MM-DD. Blank means today."""
    while True:
        text = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
        if text.strip() == "":
            return datetime.now().strftime("%Y-%m-%d")
        try:
            datetime.strptime(text, "%Y-%m-%d")   # only checks the format
            return text
        except ValueError:
            print("Wrong format. Example: 2026-11-17")


def get_valid_month():
    """Asks for a month as YYYY-MM. Blank means this month."""
    while True:
        text = input("Enter month (YYYY-MM) or press Enter for this month: ")
        if text.strip() == "":
            return datetime.now().strftime("%Y-%m")
        try:
            datetime.strptime(text, "%Y-%m")
            return text
        except ValueError:
            print("Wrong format. Example: 2026-11")


def choose_category():
    """Shows the category list and returns the chosen one."""
    print("Categories:")
    for number in range(len(CATEGORIES)):
        print(" ", number + 1, "-", CATEGORIES[number])
    while True:
        try:
            choice = int(input("Choose category number: "))
            if 1 <= choice <= len(CATEGORIES):
                return CATEGORIES[choice - 1]
            print("Please pick a number from the list.")
        except ValueError:
            print("Please enter a number.")


# ---------------------------------------------------------------
# Storage module (Aatirth)
# ---------------------------------------------------------------
def load_transactions():
    """Reads expenses.csv and returns a list of dictionaries.
    If the file does not exist, it creates it with headers."""
    transactions = []

    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(HEADERS)
        return transactions

    try:
        with open(FILE_NAME, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["amount"] = float(row["amount"])   # text -> number
                transactions.append(row)
    except (ValueError, KeyError):
        print("Warning: expenses.csv has a bad row. Some data was skipped.")

    return transactions


def save_to_csv(transactions):
    """Writes the whole list of transactions into expenses.csv."""
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        writer.writeheader()
        for t in transactions:
            writer.writerow(t)


def load_budget():
    """Reads the budget from budget.txt. Returns 0 if not set yet."""
    try:
        with open(BUDGET_FILE, "r") as file:
            return float(file.read())
    except (FileNotFoundError, ValueError):
        return 0.0


def set_budget():
    """Asks for the monthly budget, saves it, and returns it. (Anoushka)"""
    budget = get_valid_amount("Enter your monthly budget limit (Rs.): ")
    with open(BUDGET_FILE, "w") as file:
        file.write(str(budget))
    print("Budget saved: Rs.", budget)
    return budget


# ---------------------------------------------------------------
# Data input module
# ---------------------------------------------------------------
def add_income(transactions):
    """Adds one income entry."""
    print_line()
    print("ADD INCOME")
    date = get_valid_date()
    amount = get_valid_amount("Enter income amount (Rs.): ")
    description = input("Short note (example: pocket money): ")

    new_entry = {"date": date, "type": "income", "category": "Income",
                 "amount": amount, "description": description}
    transactions.append(new_entry)
    save_to_csv(transactions)
    print("Income saved!")


def add_expense(transactions):
    """Adds one expense entry."""
    print_line()
    print("ADD EXPENSE")
    date = get_valid_date()
    amount = get_valid_amount("Enter expense amount (Rs.): ")
    category = choose_category()
    description = input("Short note (example: lunch): ")

    new_entry = {"date": date, "type": "expense", "category": category,
                 "amount": amount, "description": description}
    transactions.append(new_entry)
    save_to_csv(transactions)
    print("Expense saved!")


# ---------------------------------------------------------------
# Calculation engine
# ---------------------------------------------------------------
def filter_by_month(transactions, month):
    """Returns only the transactions of one month (like '2026-11').
    A date looks like '2026-11-17', so the first 7 letters are the month."""
    month_list = []
    for t in transactions:
        if t["date"][:7] == month:
            month_list.append(t)
    return month_list


def calculate_totals(month_list):
    """Returns total income, total expense and balance. (Aatirth)"""
    total_income = 0
    total_expense = 0
    for t in month_list:
        if t["type"] == "income":
            total_income = total_income + t["amount"]
        else:
            total_expense = total_expense + t["amount"]
    balance = total_income - total_expense
    return total_income, total_expense, balance


def get_category_breakdown(month_list):
    """Returns a dictionary like {'Food': 3400, 'Transport': 1650...}. (Srishthi)"""
    breakdown = {}
    for category in CATEGORIES:
        breakdown[category] = 0          # start every category at 0

    for t in month_list:
        if t["type"] == "expense":
            breakdown[t["category"]] = breakdown[t["category"]] + t["amount"]
    return breakdown


# ---------------------------------------------------------------
# Budget monitor (Harsh) - this is the decision tree from the report
# ---------------------------------------------------------------
def check_budget_status(total_expense, budget):
    """Compares spending with the budget and prints an alert."""
    if budget <= 0:
        print("No budget set yet. Please choose 'Set monthly budget' from the menu.")
        return

    ratio = (total_expense / budget) * 100
    print("Budget used: " + str(round(ratio, 1)) + "%")

    if ratio > 100:
        extra = total_expense - budget
        print("ALERT: Budget exceeded! You overspent by Rs.", round(extra, 2))
    elif ratio == 100:
        print("NOTICE: You have reached your exact budget limit.")
    elif ratio >= 80:
        left = budget - total_expense
        print("WARNING: 80%+ of budget used. Spend carefully!")
        print("Money left in budget: Rs.", round(left, 2))
    else:
        left = budget - total_expense
        print("SAFE: You are within budget. Money left: Rs.", round(left, 2))


# ---------------------------------------------------------------
# Reporting module (Srishthi)
# ---------------------------------------------------------------
def make_sorted_list(breakdown):
    """Turns the dictionary into a list of (amount, category) pairs,
    sorted from highest spending to lowest."""
    pairs = []
    for category in breakdown:
        pairs.append((breakdown[category], category))
    pairs.sort(reverse=True)
    return pairs


def plot_spending_chart(breakdown, total_expense):
    """Prints a text bar chart. Each # is about 5% of total spending."""
    print("SPENDING CHART (each # = 5%)")
    if total_expense == 0:
        print("No expenses to show.")
        return

    for amount, category in make_sorted_list(breakdown):
        percent = (amount / total_expense) * 100
        bars = "#" * int(percent / 5)
        print(category.ljust(14), bars, str(round(percent, 1)) + "%")


def generate_summary(transactions, budget, month):
    """Prints the full report for one month."""
    month_list = filter_by_month(transactions, month)
    income, expense, balance = calculate_totals(month_list)
    breakdown = get_category_breakdown(month_list)

    print_line()
    print("MONTHLY REPORT:", month)
    print_line()
    print("Total income      : Rs.", round(income, 2))
    print("Total expenditure : Rs.", round(expense, 2))
    print("Remaining balance : Rs.", round(balance, 2))
    if income > 0:
        savings_rate = (balance / income) * 100
        print("Savings rate      :", round(savings_rate, 1), "%")

    print_line()
    print("CATEGORY-WISE SPENDING")
    for amount, category in make_sorted_list(breakdown):
        print(category.ljust(14), "Rs.", round(amount, 2))

    sorted_list = make_sorted_list(breakdown)
    if expense > 0:
        print("Top spending category:", sorted_list[0][1])

    print_line()
    check_budget_status(expense, budget)
    print_line()
    plot_spending_chart(breakdown, expense)
    print_line()


def view_all_transactions(transactions):
    """Prints every saved transaction."""
    print_line()
    if len(transactions) == 0:
        print("No transactions yet.")
        return
    print("ALL TRANSACTIONS")
    for t in transactions:
        print(t["date"], "|", t["type"].ljust(7), "|",
              t["category"].ljust(13), "| Rs.", t["amount"], "|", t["description"])

        
def clear_all_data(transactions):
    """Deletes every transaction and resets the budget (start fresh)."""
    print_line()
    answer = input("This deletes ALL transactions and the budget. Type YES to confirm: ")
    if answer.strip().upper() != "YES":
        print("Cancelled. Nothing was deleted.")
        return 0.0
    transactions.clear()          # empties the list already in memory
    save_to_csv(transactions)     # rewrites expenses.csv with only headers
    with open(BUDGET_FILE, "w") as file:
        file.write("0")
    print("All data cleared. You can start fresh.")
    return 0.0


# ---------------------------------------------------------------
# Menu and main program (Ridhima)
# ---------------------------------------------------------------
def show_menu():
    """Prints the main menu."""
    print()
    print("===== PERSONAL EXPENSE AND BUDGET TRACKER =====")
    print("1. Add income")
    print("2. Add expense")
    print("3. Set monthly budget")
    print("4. View monthly report")
    print("5. View all transactions")
    print("6. Clear all data")
    print("7. Exit")


def main():
    """Loads data, then keeps showing the menu until the user exits."""
    transactions = load_transactions()
    budget = load_budget()

    while True:
        show_menu()
        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            add_income(transactions)
        elif choice == "2":
            add_expense(transactions)
        elif choice == "3":
            budget = set_budget()
        elif choice == "4":
            month = get_valid_month()
            generate_summary(transactions, budget, month)
        elif choice == "5":
            view_all_transactions(transactions)
            choice = input("Enter your choice (1-7): ")
        elif choice == "6":
            budget = clear_all_data(transactions)
        elif choice == "7":
            print("Thank you! Your data is saved. Goodbye.")
            break
        else:
             print("Invalid choice. Please enter a number from 1 to 7.")

# This line means: run main() only when this file is run directly
# (not when dashboard.py imports it).
if __name__ == "__main__":
    main()

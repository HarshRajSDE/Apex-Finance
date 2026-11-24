"""
dashboard.py - creates dashboard.html from expenses.csv
Run:  python dashboard.py     then double-click dashboard.html to open it in a browser.
Keep this file in the same folder as expense_tracker.py.
"""

from expense_tracker import (load_transactions, load_budget, filter_by_month,
                             calculate_totals, get_category_breakdown,
                             make_sorted_list, get_valid_month)

STYLE = """
body { font-family: Arial, sans-serif; background: #f2f4f8; margin: 0; padding: 20px; }
h1 { text-align: center; color: #1f3a5f; }
.cards { display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; }
.card { background: white; padding: 15px 25px; border-radius: 10px; text-align: center; min-width: 150px; }
.card h3 { margin: 0; color: #666; font-size: 14px; }
.card p { margin: 8px 0 0; font-size: 22px; font-weight: bold; }
.box { background: white; max-width: 700px; margin: 20px auto; padding: 15px; border-radius: 10px; }
.bar-row { display: flex; align-items: center; margin: 6px 0; }
.bar-name { width: 110px; }
.bar { background: #3b82f6; height: 18px; border-radius: 4px; }
.bar-label { margin-left: 8px; font-size: 13px; }
.safe { color: green; } .warn { color: orange; } .bad { color: red; }
table { width: 100%; border-collapse: collapse; }
th, td { text-align: left; padding: 6px; border-bottom: 1px solid #ddd; font-size: 14px; }
"""


def get_status_text(expense, budget):
    """Returns (message, css class) for the budget status."""
    if budget <= 0:
        return "No budget set", "warn"
    ratio = expense / budget * 100
    if ratio > 100:
        return "Budget exceeded! (" + str(round(ratio, 1)) + "%)", "bad"
    elif ratio >= 80:
        return "Warning: " + str(round(ratio, 1)) + "% used", "warn"
    else:
        return "Safe: " + str(round(ratio, 1)) + "% used", "safe"


def build_html(month, month_list, budget):
    income, expense, balance = calculate_totals(month_list)
    breakdown = get_category_breakdown(month_list)
    status_text, status_class = get_status_text(expense, budget)

    html = "<html><head><title>Expense Dashboard</title><style>" + STYLE + "</style></head><body>"
    html += "<h1>Expense Dashboard - " + month + "</h1>"

    # summary cards
    html += "<div class='cards'>"
    html += "<div class='card'><h3>Income</h3><p>Rs. " + str(round(income, 2)) + "</p></div>"
    html += "<div class='card'><h3>Expenses</h3><p>Rs. " + str(round(expense, 2)) + "</p></div>"
    html += "<div class='card'><h3>Balance</h3><p>Rs. " + str(round(balance, 2)) + "</p></div>"
    html += "<div class='card'><h3>Budget</h3><p>Rs. " + str(round(budget, 2)) + "</p></div>"
    html += "</div>"
    html += "<div class='box'><h2 class='" + status_class + "'>" + status_text + "</h2></div>"

    # category bars
    html += "<div class='box'><h2>Spending by category</h2>"
    if expense == 0:
        html += "<p>No expenses this month.</p>"
    else:
        for amount, category in make_sorted_list(breakdown):
            percent = amount / expense * 100
            html += "<div class='bar-row'><div class='bar-name'>" + category + "</div>"
            html += "<div class='bar' style='width:" + str(round(percent * 4)) + "px'></div>"
            html += "<div class='bar-label'>Rs. " + str(round(amount)) + " (" + str(round(percent, 1)) + "%)</div></div>"
    html += "</div>"

    # transaction table
    html += "<div class='box'><h2>Transactions</h2><table>"
    html += "<tr><th>Date</th><th>Type</th><th>Category</th><th>Amount</th><th>Note</th></tr>"
    for t in month_list:
        html += "<tr><td>" + t["date"] + "</td><td>" + t["type"] + "</td><td>" + t["category"]
        html += "</td><td>Rs. " + str(t["amount"]) + "</td><td>" + t["description"] + "</td></tr>"
    html += "</table></div></body></html>"
    return html


def main():
    transactions = load_transactions()
    budget = load_budget()
    month = get_valid_month()
    month_list = filter_by_month(transactions, month)

    html = build_html(month, month_list, budget)
    with open("dashboard.html", "w", encoding="utf-8") as file:
        file.write(html)
    print("dashboard.html created! Double-click it to open in your browser.")


if __name__ == "__main__":
    main()

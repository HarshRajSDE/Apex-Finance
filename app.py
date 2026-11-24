"""
app.py - APEX FINANCE | Personal Expense & Budget Tracker
Modern glossy black fintech dashboard built with Streamlit and Plotly.
Reuses existing business logic and CSV/TXT storage from expense_tracker.py.
"""

from datetime import datetime, date
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Import core business logic and storage constants from the original tracker
from expense_tracker import (
    FILE_NAME,
    BUDGET_FILE,
    HEADERS,
    CATEGORIES,
    load_transactions,
    save_to_csv,
    load_budget,
    calculate_totals,
    filter_by_month,
    get_category_breakdown,
)

# -----------------------------------------------------------------------------
# Streamlit Page Setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="APEX FINANCE | Expense & Budget Tracker",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Custom Styling: Glossy Black / Metallic Fintech Theme + Emerald Accents
# -----------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

:root {
    --bg-obsidian: #050505;
    --bg-surface: #0A0A0A;
    --bg-card: #101010;
    --bg-elevated: #161616;
    --border-subtle: rgba(255, 255, 255, 0.07);
    --border-sheen: rgba(255, 255, 255, 0.13);
    --text-primary: #F4F4F5;
    --text-secondary: #A1A1AA;
    --text-muted: #71717A;
    --accent-emerald: #10B981;
    --accent-emerald-dim: rgba(16, 185, 129, 0.14);
    --accent-red: #EF4444;
    --accent-amber: #F59E0B;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-primary);
}

/* Deep glossy black canvas */
.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(16, 185, 129, 0.06) 0%, transparent 60%),
        radial-gradient(circle at 85% 15%, rgba(255, 255, 255, 0.025) 0%, transparent 40%),
        linear-gradient(180deg, #050505 0%, #080808 50%, #050505 100%) !important;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}
[data-testid="stAppDeployButton"], #MainMenu, footer {
    display: none !important;
}

.block-container {
    padding-top: 2.4rem !important;
    padding-bottom: 3rem !important;
    max-width: 1400px !important;
}

/* Glossy black sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A0A0A 0%, #050505 100%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.07) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem !important;
}

/* Remove circular radio indicators & style as sleek fintech nav items */
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 5px !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child {
    display: none !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    width: 100% !important;
    padding: 10px 14px !important;
    border-radius: 10px !important;
    border: 1px solid transparent !important;
    background: transparent !important;
    color: #9CA3AF !important;
    font-weight: 500 !important;
    font-size: 13.5px !important;
    letter-spacing: 0.1px !important;
    transition: all 0.18s ease !important;
    cursor: pointer !important;
    margin: 0 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(255, 255, 255, 0.04) !important;
    border-color: rgba(255, 255, 255, 0.07) !important;
    color: #F4F4F5 !important;
    transform: translateX(2px);
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(90deg, rgba(16, 185, 129, 0.14) 0%, rgba(16, 185, 129, 0.02) 100%) !important;
    border: 1px solid rgba(16, 185, 129, 0.25) !important;
    border-left: 3px solid #10B981 !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.45) !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    font-size: 13.5px !important;
    margin: 0 !important;
}

/* Style Streamlit bordered containers as glossy metallic black cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(165deg, #141414 0%, #0A0A0A 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    border-top: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 16px !important;
    padding: 20px 22px !important;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.04) !important;
}

/* Page Header */
.page-header {
    display: flex;
    align-items: center;
    gap: 14px;
    padding-bottom: 14px;
    margin-bottom: 6px;
}
.page-icon-box {
    background: linear-gradient(145deg, #181818 0%, #0C0C0C 100%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #10B981;
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.5), 0 0 18px rgba(16, 185, 129, 0.12);
    flex-shrink: 0;
}
.page-title {
    font-size: 24px;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.5px;
    margin: 0;
    line-height: 1.2;
}
.page-subtitle {
    font-size: 13px;
    color: #8A8F98;
    margin: 3px 0 0 0;
}

/* Glossy Black KPI Metric Cards */
.metric-card {
    background: linear-gradient(165deg, #161616 0%, #0A0A0A 100%);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-top: 1px solid rgba(255, 255, 255, 0.13);
    border-radius: 14px;
    padding: 16px 18px;
    min-height: 148px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 10px 26px rgba(0, 0, 0, 0.55), inset 0 1px 0 rgba(255, 255, 255, 0.04);
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
    margin-bottom: 10px;
}
.metric-card:hover {
    transform: translateY(-2px);
    border-color: rgba(255, 255, 255, 0.15);
    box-shadow: 0 14px 32px rgba(0, 0, 0, 0.7);
}
.metric-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: 16px;
    right: 16px;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-color, #10B981), transparent);
    opacity: 0.75;
}
.metric-label {
    font-size: 11px;
    font-weight: 600;
    color: #8A8F98;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 6px;
}
.metric-value {
    font-size: clamp(19px, 2.1vw, 25px);
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.5px;
    line-height: 1.2;
    white-space: nowrap;
}
.metric-sub {
    font-size: 11.5px;
    color: #71717A;
    margin-top: 8px;
}

/* Refined Badges */
.badge-green {
    background: rgba(16, 185, 129, 0.12);
    color: #34D399;
    border: 1px solid rgba(16, 185, 129, 0.25);
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 10.5px;
    font-weight: 600;
    white-space: nowrap;
}
.badge-red {
    background: rgba(239, 68, 68, 0.12);
    color: #F87171;
    border: 1px solid rgba(239, 68, 68, 0.25);
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 10.5px;
    font-weight: 600;
    white-space: nowrap;
}
.badge-amber {
    background: rgba(245, 158, 11, 0.12);
    color: #FBBF24;
    border: 1px solid rgba(245, 158, 11, 0.25);
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 10.5px;
    font-weight: 600;
    white-space: nowrap;
}
.badge-silver {
    background: rgba(255, 255, 255, 0.06);
    color: #A1A1AA;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 10.5px;
    font-weight: 600;
    white-space: nowrap;
}

/* Status Banners */
.status-banner {
    background: linear-gradient(145deg, #121212 0%, #0A0A0A 100%);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 12px;
    padding: 14px 18px;
    margin: 10px 0 20px 0;
    display: flex;
    align-items: center;
    gap: 14px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.45);
}
.status-safe { border-left: 3px solid #10B981; }
.status-warning { border-left: 3px solid #F59E0B; }
.status-danger { border-left: 3px solid #EF4444; }
.status-info { border-left: 3px solid #71717A; }

/* Card Headings */
.card-title {
    font-size: 15px;
    font-weight: 600;
    color: #F4F4F5;
    margin-bottom: 2px;
    letter-spacing: -0.2px;
}
.card-desc {
    font-size: 12px;
    color: #71717A;
    margin-bottom: 12px;
}

/* Section Heading */
.section-heading {
    font-size: 16px;
    font-weight: 600;
    color: #E4E4E7;
    margin: 18px 0 10px 0;
    letter-spacing: -0.2px;
}

/* Primary Buttons */
.stButton > button,
.stDownloadButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(145deg, #10B981 0%, #059669 100%) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 13.5px !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    padding: 0.55rem 1.25rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(16, 185, 129, 0.2) !important;
}
.stButton > button:hover,
.stDownloadButton > button:hover,
.stFormSubmitButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.32) !important;
}

/* Secondary / Preset small buttons */
button[kind="secondary"] {
    background: linear-gradient(145deg, #181818 0%, #0E0E0E 100%) !important;
    color: #E4E4E7 !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: none !important;
    white-space: nowrap !important;
    padding: 0.45rem 0.75rem !important;
}
button[kind="secondary"]:hover {
    border-color: rgba(16, 185, 129, 0.45) !important;
    color: #FFFFFF !important;
}

/* Inputs & Selectboxes */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stDateInput > div > div > input,
.stTextArea textarea,
.stSelectbox > div > div {
    background-color: #0A0A0A !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    color: #F4F4F5 !important;
}
.stTextArea textarea {
    font-family: 'SF Mono', Menlo, Monaco, Consolas, monospace !important;
    font-size: 12.5px !important;
    line-height: 1.5 !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: #10B981 !important;
    box-shadow: 0 0 0 1px rgba(16, 185, 129, 0.4) !important;
}

/* Glossy Black Transaction Table */
.tx-table-wrap {
    width: 100%;
    overflow-x: auto;
}
.tx-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
}
.tx-table th {
    background-color: #141414;
    color: #8A8F98;
    text-transform: uppercase;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.6px;
    padding: 10px 12px;
    text-align: left;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    white-space: nowrap;
}
.tx-table th:first-child { border-radius: 8px 0 0 8px; }
.tx-table th:last-child { border-radius: 0 8px 8px 0; }
.tx-table td {
    padding: 11px 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    color: #E4E4E7;
    font-size: 13px;
    vertical-align: middle;
}
.tx-table td:first-child,
.tx-table td.nowrap {
    white-space: nowrap;
}
.tx-table.compact th,
.tx-table.compact td {
    padding: 9px 6px;
    font-size: 12px;
}
.tx-table tr:last-child td {
    border-bottom: none;
}
.tx-table tr:hover td {
    background-color: rgba(255, 255, 255, 0.025);
}

.cat-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #161616;
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 3px 10px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 500;
    color: #E4E4E7;
    white-space: nowrap;
}

/* Responsive tweaks for smaller laptop screens */
@media (max-width: 1100px) {
    .metric-value { font-size: 22px; }
    .page-title { font-size: 21px; }
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Category Icons & Refined Financial Color Palette
# -----------------------------------------------------------------------------
CATEGORY_ICONS = {
    "Food": "🍽️",
    "Transport": "🚗",
    "Shopping": "🛍️",
    "Education": "📚",
    "Entertainment": "🎬",
    "Bills": "🧾",
    "Others": "📦",
    "Income": "💵",
}

CATEGORY_COLORS = {
    "Food": "#10B981",          # Emerald
    "Transport": "#38BDF8",     # Sky Slate
    "Shopping": "#A78BFA",      # Soft Violet
    "Education": "#60A5FA",     # Steel Blue
    "Entertainment": "#2DD4BF", # Muted Teal
    "Bills": "#E05252",         # Muted Crimson
    "Others": "#71717A",        # Metallic Zinc
    "Income": "#10B981",        # Emerald
}

# -----------------------------------------------------------------------------
# Data Helper Functions (preserving existing CSV/TXT logic)
# -----------------------------------------------------------------------------
def get_available_months(transactions):
    """Finds all unique months present in transactions and always includes the current month."""
    months = set()
    current_month = datetime.now().strftime("%Y-%m")
    months.add(current_month)
    for t in transactions:
        if "date" in t and len(t["date"]) >= 7:
            months.add(t["date"][:7])
    return sorted(list(months), reverse=True)


def save_budget_to_file(budget_value):
    """Saves the budget to budget.txt."""
    with open(BUDGET_FILE, "w") as file:
        file.write(str(float(budget_value)))


def add_transaction_entry(date_str, trans_type, category, amount, description):
    """Appends a new transaction and saves it to expenses.csv."""
    transactions = load_transactions()
    entry = {
        "date": str(date_str),
        "type": str(trans_type),
        "category": str(category),
        "amount": float(amount),
        "description": str(description).strip()
    }
    transactions.append(entry)
    save_to_csv(transactions)
    return transactions


def delete_transaction_entry(index):
    """Removes a transaction at the given index and updates expenses.csv."""
    transactions = load_transactions()
    if 0 <= index < len(transactions):
        deleted = transactions.pop(index)
        save_to_csv(transactions)
        return deleted
    return None


def apply_dark_chart_theme(fig, height=320):
    """Applies consistent glossy black chart styling across all Plotly figures."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E4E4E7", family="Plus Jakarta Sans, Inter, sans-serif", size=12),
        hoverlabel=dict(
            bgcolor="#161616",
            bordercolor="rgba(255,255,255,0.15)",
            font=dict(color="#F4F4F5", size=12)
        ),
        height=height,
    )
    return fig


def render_page_header(title, subtitle, svg_path):
    """Renders a consistent, sleek glossy black page header."""
    st.markdown(f"""
    <div class="page-header">
        <div class="page-icon-box">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                {svg_path}
            </svg>
        </div>
        <div>
            <h1 class="page-title">{title}</h1>
            <p class="page-subtitle">{subtitle}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Sidebar Navigation & Branding
# -----------------------------------------------------------------------------
with st.sidebar:
    # Professional SVG Finance Logo + APEX FINANCE Branding
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; padding: 4px 4px 18px 4px; border-bottom: 1px solid rgba(255,255,255,0.07); margin-bottom: 16px;">
        <div style="background: linear-gradient(145deg, #141414 0%, #090909 100%); border: 1px solid rgba(16,185,129,0.35); width: 42px; height: 42px; border-radius: 11px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 14px rgba(0,0,0,0.6), 0 0 20px rgba(16,185,129,0.18); flex-shrink: 0;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                <path d="M12 3L21 19H3L12 3Z" stroke="#10B981" stroke-width="2" stroke-linejoin="round"/>
                <path d="M12 10L16.5 19H7.5L12 10Z" fill="rgba(16,185,129,0.28)"/>
            </svg>
        </div>
        <div>
            <div style="font-size: 16px; font-weight: 800; color: #FFFFFF; letter-spacing: 0.6px; line-height: 1.1;">APEX FINANCE</div>
            <div style="font-size: 10px; color: #10B981; font-weight: 600; letter-spacing: 1.1px; margin-top: 3px;">WEALTH &amp; BUDGET OS</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size: 10.5px; text-transform: uppercase; color: #52525B; font-weight: 700; letter-spacing: 1px; padding: 0 6px 6px 6px;'>Menu</div>", unsafe_allow_html=True)

    menu_choice = st.radio(
        "Navigation",
        [
            "📊  Overview Dashboard",
            "➖  Add Expense",
            "➕  Add Income",
            "📑  Transactions",
            "📈  Monthly Reports",
            "⚙️  Budget Settings",
        ],
        label_visibility="collapsed"
    )

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # Sidebar Current Month Budget Summary Card
    all_tx = load_transactions()
    current_budget = load_budget()
    now_month = datetime.now().strftime("%Y-%m")
    current_month_tx = filter_by_month(all_tx, now_month)
    cur_income, cur_expense, cur_balance = calculate_totals(current_month_tx)
    budget_ratio = (cur_expense / current_budget * 100) if current_budget > 0 else 0

    bar_color = "#EF4444" if budget_ratio > 100 else "#F59E0B" if budget_ratio >= 80 else "#10B981"
    status_text_color = "#F87171" if budget_ratio > 100 else "#FBBF24" if budget_ratio >= 80 else "#34D399"
    rem_label = f"₹{current_budget - cur_expense:,.0f} left" if current_budget >= cur_expense else f"₹{cur_expense - current_budget:,.0f} over"

    st.markdown(f"""
    <div style="background: linear-gradient(165deg, #141414 0%, #0A0A0A 100%); border: 1px solid rgba(255,255,255,0.07); border-top: 1px solid rgba(255,255,255,0.12); border-radius: 12px; padding: 14px; box-shadow: 0 8px 20px rgba(0,0,0,0.5);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <span style="font-size: 10.5px; text-transform: uppercase; color: #8A8F98; font-weight: 700; letter-spacing: 0.7px;">{datetime.now().strftime('%b %Y')} Budget</span>
            <span style="font-size: 10.5px; font-weight: 700; color: {status_text_color};">{round(budget_ratio, 1)}%</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 12px;">
            <span style="color: #71717A;">Spent</span>
            <span style="font-weight: 600; color: #F4F4F5;">₹{cur_expense:,.0f}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 12px;">
            <span style="color: #71717A;">Limit</span>
            <span style="font-weight: 600; color: #A1A1AA;">₹{current_budget:,.0f}</span>
        </div>
        <div style="background: #1C1C1E; border-radius: 999px; height: 6px; overflow: hidden; margin-bottom: 8px;">
            <div style="background: {bar_color}; width: {min(budget_ratio, 100)}%; height: 100%; border-radius: 999px;"></div>
        </div>
        <div style="font-size: 11px; color: #71717A; text-align: right;">
            {rem_label if current_budget > 0 else 'No budget set'}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size: 11px; color: #52525B; text-align: center; margin-top: 28px; line-height: 1.5; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 14px;">
        <span style="color: #71717A; font-weight: 600;">Personal Expense &amp; Budget Tracker</span><br>
        Bennett University · 2026CSAE100
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PAGE 1: Overview Dashboard
# -----------------------------------------------------------------------------
if menu_choice == "📊  Overview Dashboard":
    transactions = load_transactions()
    budget = load_budget()
    available_months = get_available_months(transactions)
    current_month_str = datetime.now().strftime("%Y-%m")

    col_head1, col_head2 = st.columns([3.2, 1.1])
    with col_head1:
        render_page_header(
            "Financial Overview",
            "Real-time cash flow, category allocation, and monthly budget utilization",
            '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/>'
        )
    with col_head2:
        selected_month = st.selectbox(
            "Reporting Month",
            options=available_months,
            index=0 if current_month_str in available_months else 0,
            help="Filter dashboard metrics and charts by month"
        )

    # Filter data for selected month
    month_tx = filter_by_month(transactions, selected_month)
    total_income, total_expense, balance = calculate_totals(month_tx)
    breakdown = get_category_breakdown(month_tx)
    ratio = (total_expense / budget * 100) if budget > 0 else 0
    savings_rate = (balance / total_income * 100) if total_income > 0 else 0

    # 4 Glossy Black KPI Summary Cards
    col_card1, col_card2, col_card3, col_card4 = st.columns(4)

    with col_card1:
        inc_count = len([t for t in month_tx if t["type"] == "income"])
        st.markdown(f"""
        <div class="metric-card" style="--accent-color: #10B981;">
            <div class="metric-label">
                <span>Total Income</span>
                <span class="badge-green">Inflow</span>
            </div>
            <div class="metric-value">₹{total_income:,.2f}</div>
            <div class="metric-sub">{inc_count} income transaction(s)</div>
        </div>
        """, unsafe_allow_html=True)

    with col_card2:
        exp_count = len([t for t in month_tx if t["type"] == "expense"])
        st.markdown(f"""
        <div class="metric-card" style="--accent-color: #EF4444;">
            <div class="metric-label">
                <span>Total Expenses</span>
                <span class="badge-red">Outflow</span>
            </div>
            <div class="metric-value">₹{total_expense:,.2f}</div>
            <div class="metric-sub">{exp_count} expense entry(ies)</div>
        </div>
        """, unsafe_allow_html=True)

    with col_card3:
        bal_badge = "badge-green" if balance >= 0 else "badge-red"
        bal_color = "#10B981" if balance >= 0 else "#F87171"
        st.markdown(f"""
        <div class="metric-card" style="--accent-color: {bal_color};">
            <div class="metric-label">
                <span>Remaining Balance</span>
                <span class="{bal_badge}">{'Surplus' if balance >= 0 else 'Deficit'}</span>
            </div>
            <div class="metric-value" style="color: {bal_color};">₹{balance:,.2f}</div>
            <div class="metric-sub">Savings rate: {round(savings_rate, 1)}%</div>
        </div>
        """, unsafe_allow_html=True)

    with col_card4:
        b_badge = "badge-red" if ratio > 100 else "badge-amber" if ratio >= 80 else "badge-green"
        b_accent = "#EF4444" if ratio > 100 else "#F59E0B" if ratio >= 80 else "#10B981"
        rem_text = f"₹{budget - total_expense:,.2f} remaining" if budget >= total_expense else f"₹{total_expense - budget:,.2f} over limit"
        st.markdown(f"""
        <div class="metric-card" style="--accent-color: {b_accent};">
            <div class="metric-label">
                <span>Monthly Budget</span>
                <span class="{b_badge}">{round(ratio, 1)}% Used</span>
            </div>
            <div class="metric-value">₹{budget:,.2f}</div>
            <div class="metric-sub">{rem_text if budget > 0 else 'Not configured'}</div>
        </div>
        """, unsafe_allow_html=True)

    # Budget Health Alert Banner
    if budget <= 0:
        st.markdown("""
        <div class="status-banner status-info">
            <div style="font-size: 20px; color: #A1A1AA;">◈</div>
            <div>
                <div style="font-size: 14px; font-weight: 600; color: #E4E4E7;">No Monthly Budget Configured</div>
                <div style="font-size: 12.5px; color: #8A8F98;">Visit <strong>Budget Settings</strong> to set your monthly spending ceiling and enable real-time alerts.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif ratio > 100:
        over = total_expense - budget
        st.markdown(f"""
        <div class="status-banner status-danger">
            <div style="font-size: 20px; color: #EF4444;">▲</div>
            <div>
                <div style="font-size: 14px; font-weight: 600; color: #F87171;">Budget Exceeded by ₹{over:,.2f}</div>
                <div style="font-size: 12.5px; color: #A1A1AA;">You have utilized <strong>{round(ratio, 1)}%</strong> of your ₹{budget:,.2f} monthly limit for {selected_month}.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif ratio >= 80:
        left = budget - total_expense
        st.markdown(f"""
        <div class="status-banner status-warning">
            <div style="font-size: 20px; color: #F59E0B;">◆</div>
            <div>
                <div style="font-size: 14px; font-weight: 600; color: #FBBF24;">Approaching Budget Limit ({round(ratio, 1)}% Used)</div>
                <div style="font-size: 12.5px; color: #A1A1AA;"><strong>₹{left:,.2f}</strong> remains in your monthly budget for {selected_month}. Monitor non-essential spending.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        left = budget - total_expense
        st.markdown(f"""
        <div class="status-banner status-safe">
            <div style="font-size: 20px; color: #10B981;">●</div>
            <div>
                <div style="font-size: 14px; font-weight: 600; color: #34D399;">Healthy Budget Status ({round(ratio, 1)}% Used)</div>
                <div style="font-size: 12.5px; color: #A1A1AA;"><strong>₹{left:,.2f}</strong> remaining within your ₹{budget:,.2f} limit for {selected_month}.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Charts Row 1: Spending by Category (Donut) & Budget Utilization (Clean Semicircular Gauge + Breakdown)
    chart_col1, chart_col2 = st.columns([1.45, 1.15])

    with chart_col1:
        with st.container(border=True):
            st.markdown("<div class='card-title'>Spending by Category</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card-desc'>Expense distribution for {selected_month}</div>", unsafe_allow_html=True)

            cat_data = [{"Category": cat, "Amount": amt} for cat, amt in breakdown.items() if amt > 0]
            if cat_data:
                df_cat = pd.DataFrame(cat_data).sort_values(by="Amount", ascending=False)
                fig_donut = px.pie(
                    df_cat,
                    values="Amount",
                    names="Category",
                    hole=0.68,
                    color="Category",
                    color_discrete_map=CATEGORY_COLORS
                )
                fig_donut.update_traces(
                    textposition="outside" if len(df_cat) > 1 else "inside",
                    textinfo="percent",
                    textfont=dict(size=12, color="#E4E4E7"),
                    hovertemplate="<b>%{label}</b><br>Spent: ₹%{value:,.2f}<br>Share: %{percent}<extra></extra>",
                    marker=dict(line=dict(color="#0A0A0A", width=2.5))
                )
                fig_donut.add_annotation(
                    text=f"<span style='font-size:11px; color:#8A8F98;'>TOTAL SPENT</span><br><b style='font-size:18px; color:#FFFFFF;'>₹{total_expense:,.0f}</b>",
                    x=0.5, y=0.5, showarrow=False
                )
                apply_dark_chart_theme(fig_donut, height=310)
                fig_donut.update_layout(
                    legend=dict(
                        orientation="h",
                        yanchor="top",
                        y=-0.06,
                        xanchor="center",
                        x=0.5,
                        font=dict(size=11.5, color="#A1A1AA")
                    ),
                    margin=dict(t=15, b=40, l=15, r=15)
                )
                st.plotly_chart(fig_donut, use_container_width=True)
            else:
                st.info(f"No expense entries recorded for {selected_month}.")

    with chart_col2:
        with st.container(border=True):
            st.markdown("<div class='card-title'>Budget Utilization</div>", unsafe_allow_html=True)
            st.markdown("<div class='card-desc'>Monthly limit vs actual expenditure</div>", unsafe_allow_html=True)

            if budget > 0:
                gauge_color = "#EF4444" if ratio > 100 else "#F59E0B" if ratio >= 80 else "#10B981"
                max_axis = max(budget * 1.2, total_expense * 1.1)
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=ratio,
                    number={"suffix": "%", "valueformat": ".1f", "font": {"size": 30, "color": "#FFFFFF", "family": "Plus Jakarta Sans"}},
                    gauge={
                        "shape": "angular",
                        "axis": {"range": [0, max(120, ratio * 1.1)], "tickwidth": 1, "tickcolor": "#3F3F46", "tickfont": {"color": "#71717A", "size": 10}},
                        "bar": {"color": gauge_color, "thickness": 0.28},
                        "bgcolor": "#161616",
                        "borderwidth": 0,
                        "steps": [
                            {"range": [0, 80], "color": "rgba(16, 185, 129, 0.10)"},
                            {"range": [80, 100], "color": "rgba(245, 158, 11, 0.10)"},
                            {"range": [100, max(120, ratio * 1.1)], "color": "rgba(239, 68, 68, 0.10)"},
                        ],
                        "threshold": {
                            "line": {"color": "#E4E4E7", "width": 2},
                            "thickness": 0.75,
                            "value": 100
                        }
                    }
                ))
                apply_dark_chart_theme(fig_gauge, height=220)
                fig_gauge.update_layout(margin=dict(t=20, b=0, l=24, r=24))
                st.plotly_chart(fig_gauge, use_container_width=True)

                rem_amt = budget - total_expense
                rem_color = "#34D399" if rem_amt >= 0 else "#F87171"
                rem_title = "Remaining" if rem_amt >= 0 else "Overspent"
                st.markdown(f"""
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; background: #0A0A0A; border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 10px 12px; margin-top: 4px; text-align: center;">
                    <div>
                        <div style="font-size: 10.5px; color: #71717A; text-transform: uppercase;">Spent</div>
                        <div style="font-size: 13px; font-weight: 700; color: #F4F4F5;">₹{total_expense:,.0f}</div>
                    </div>
                    <div style="border-left: 1px solid rgba(255,255,255,0.06); border-right: 1px solid rgba(255,255,255,0.06);">
                        <div style="font-size: 10.5px; color: #71717A; text-transform: uppercase;">Budget</div>
                        <div style="font-size: 13px; font-weight: 700; color: #A1A1AA;">₹{budget:,.0f}</div>
                    </div>
                    <div>
                        <div style="font-size: 10.5px; color: #71717A; text-transform: uppercase;">{rem_title}</div>
                        <div style="font-size: 13px; font-weight: 700; color: {rem_color};">₹{abs(rem_amt):,.0f}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="text-align: center; padding: 70px 16px; color: #71717A;">
                    <div style="font-size: 28px; margin-bottom: 8px; color: #A1A1AA;">◎</div>
                    <div style="font-size: 14px; font-weight: 600; color: #E4E4E7;">No Budget Limit Set</div>
                    <div style="font-size: 12px; margin-top: 4px;">Set a monthly limit in Budget Settings to track utilization.</div>
                </div>
                """, unsafe_allow_html=True)

    # Charts Row 2: Monthly Income vs Expenses & Monthly Trend Analytics
    month_comparison = []
    for m in reversed(available_months):
        m_tx = filter_by_month(transactions, m)
        inc, exp, bal = calculate_totals(m_tx)
        month_comparison.append({
            "Month": m,
            "Income": inc,
            "Expenses": exp,
            "Savings": bal
        })

    if month_comparison:
        df_monthly = pd.DataFrame(month_comparison)
        row2_col1, row2_col2 = st.columns(2)

        with row2_col1:
            with st.container(border=True):
                st.markdown("<div class='card-title'>Monthly Income vs Expenses</div>", unsafe_allow_html=True)
                st.markdown("<div class='card-desc'>Grouped cash inflow and outflow comparison</div>", unsafe_allow_html=True)

                fig_bar = go.Figure()
                fig_bar.add_trace(go.Bar(
                    x=df_monthly["Month"],
                    y=df_monthly["Income"],
                    name="Income",
                    marker_color="#10B981",
                    marker_line_width=0,
                    hovertemplate="Income: ₹%{y:,.2f}<extra></extra>"
                ))
                fig_bar.add_trace(go.Bar(
                    x=df_monthly["Month"],
                    y=df_monthly["Expenses"],
                    name="Expenses",
                    marker_color="#E05252",
                    marker_line_width=0,
                    hovertemplate="Expenses: ₹%{y:,.2f}<extra></extra>"
                ))
                apply_dark_chart_theme(fig_bar, height=290)
                fig_bar.update_layout(
                    barmode="group",
                    bargap=0.35,
                    bargroupgap=0.12,
                    hovermode="x unified",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#A1A1AA", size=11.5)),
                    xaxis=dict(type="category", showgrid=False, color="#8A8F98"),
                    yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.08)", color="#8A8F98", tickprefix="₹"),
                    margin=dict(t=28, b=16, l=10, r=10),
                )
                st.plotly_chart(fig_bar, use_container_width=True)

        with row2_col2:
            with st.container(border=True):
                st.markdown("<div class='card-title'>Monthly Trend Analytics</div>", unsafe_allow_html=True)
                st.markdown("<div class='card-desc'>Income, expenses, and net savings trajectory</div>", unsafe_allow_html=True)

                fig_trend = go.Figure()
                fig_trend.add_trace(go.Scatter(
                    x=df_monthly["Month"],
                    y=df_monthly["Income"],
                    name="Income",
                    mode="lines+markers",
                    line=dict(color="#10B981", width=2.5, shape="spline"),
                    marker=dict(size=7, color="#10B981"),
                    fill="tozeroy",
                    fillcolor="rgba(16, 185, 129, 0.08)",
                    hovertemplate="Income: ₹%{y:,.2f}<extra></extra>"
                ))
                fig_trend.add_trace(go.Scatter(
                    x=df_monthly["Month"],
                    y=df_monthly["Expenses"],
                    name="Expenses",
                    mode="lines+markers",
                    line=dict(color="#E05252", width=2.5, shape="spline"),
                    marker=dict(size=7, color="#E05252"),
                    fill="tozeroy",
                    fillcolor="rgba(224, 82, 82, 0.07)",
                    hovertemplate="Expenses: ₹%{y:,.2f}<extra></extra>"
                ))
                fig_trend.add_trace(go.Scatter(
                    x=df_monthly["Month"],
                    y=df_monthly["Savings"],
                    name="Net Savings",
                    mode="lines+markers",
                    line=dict(color="#A1A1AA", width=2, dash="dot", shape="spline"),
                    marker=dict(size=6, color="#E4E4E7"),
                    hovertemplate="Net Savings: ₹%{y:,.2f}<extra></extra>"
                ))
                apply_dark_chart_theme(fig_trend, height=290)
                fig_trend.update_layout(
                    hovermode="x unified",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#A1A1AA", size=11.5)),
                    xaxis=dict(type="category", showgrid=False, color="#8A8F98"),
                    yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.08)", color="#8A8F98", tickprefix="₹"),
                    margin=dict(t=28, b=16, l=10, r=10),
                )
                st.plotly_chart(fig_trend, use_container_width=True)

    # Recent Transactions Table
    with st.container(border=True):
        st.markdown("<div class='card-title'>Recent Transactions</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='card-desc'>Latest activity recorded in {selected_month}</div>", unsafe_allow_html=True)

        if month_tx:
            rows_html = ""
            for t in reversed(month_tx[-6:]):
                icon = CATEGORY_ICONS.get(t["category"], "📦")
                badge = "badge-green" if t["type"] == "income" else "badge-red"
                amount_prefix = "+₹" if t["type"] == "income" else "-₹"
                amount_color = "#34D399" if t["type"] == "income" else "#F87171"
                rows_html += (
                    f"<tr>"
                    f"<td style='color:#8A8F98; font-weight:500;'>{t['date']}</td>"
                    f"<td><span class='{badge}'>{t['type'].upper()}</span></td>"
                    f"<td><span class='cat-pill'>{icon} {t['category']}</span></td>"
                    f"<td class='nowrap' style='font-weight:700; color:{amount_color};'>{amount_prefix}{t['amount']:,.2f}</td>"
                    f"<td style='color:#E4E4E7;'>{t['description']}</td>"
                    f"</tr>"
                )
            table_html = (
                "<div class='tx-table-wrap'><table class='tx-table'>"
                "<thead><tr><th>Date</th><th>Type</th><th>Category</th><th>Amount</th><th>Description</th></tr></thead>"
                f"<tbody>{rows_html}</tbody></table></div>"
            )
            st.html(table_html)
        else:
            st.info(f"No transactions logged for {selected_month}.")


# -----------------------------------------------------------------------------
# PAGE 2: Add Expense
# -----------------------------------------------------------------------------
elif menu_choice == "➖  Add Expense":
    render_page_header(
        "Record New Expense",
        "Log an expenditure with category tagging and live budget impact",
        '<path d="M2 10h20"/><rect x="2" y="5" width="20" height="14" rx="2"/>'
    )

    col_form, col_impact = st.columns([1.45, 1.15])

    with col_form:
        with st.container(border=True):
            st.markdown("<div class='card-title'>Expense Details</div>", unsafe_allow_html=True)
            st.markdown("<div class='card-desc'>Saved directly to expenses.csv</div>", unsafe_allow_html=True)

            with st.form("add_expense_form", clear_on_submit=True):
                exp_date = st.date_input("Expense Date", value=date.today())

                col_cat, col_amt = st.columns([1.2, 1])
                with col_cat:
                    category_options = [f"{CATEGORY_ICONS.get(c, '📦')} {c}" for c in CATEGORIES]
                    selected_cat_raw = st.selectbox("Category", options=category_options)
                    selected_cat = selected_cat_raw.split(" ", 1)[1] if " " in selected_cat_raw else selected_cat_raw

                with col_amt:
                    exp_amount = st.number_input("Amount (₹)", min_value=1.0, value=150.0, step=50.0)

                exp_desc = st.text_input("Description / Note", placeholder="e.g. Lunch, Metro recharge, Textbooks")
                submit_expense = st.form_submit_button("Save Expense Entry", use_container_width=True)

                if submit_expense:
                    if exp_amount <= 0:
                        st.error("Amount must be greater than 0.")
                    elif not exp_desc.strip():
                        st.warning("Please provide a brief note or description.")
                    else:
                        date_str = exp_date.strftime("%Y-%m-%d")
                        add_transaction_entry(date_str, "expense", selected_cat, exp_amount, exp_desc)
                        st.toast(f"Saved expense: ₹{exp_amount:,.2f} ({selected_cat})", icon="✅")
                        st.success(f"Expense of ₹{exp_amount:,.2f} in '{selected_cat}' recorded.")
                        st.rerun()

    with col_impact:
        with st.container(border=True):
            st.markdown("<div class='card-title'>Current Budget Health</div>", unsafe_allow_html=True)
            st.markdown("<div class='card-desc'>Live status for the current month</div>", unsafe_allow_html=True)

            current_month_key = date.today().strftime("%Y-%m")
            all_txs = load_transactions()
            month_txs = filter_by_month(all_txs, current_month_key)
            budget = load_budget()
            _, cur_exp, _ = calculate_totals(month_txs)

            used_pct = (cur_exp / budget * 100) if budget > 0 else 0
            rem = budget - cur_exp
            bar_col = "#EF4444" if used_pct > 100 else "#F59E0B" if used_pct >= 80 else "#10B981"

            st.markdown(f"""
            <div style="background: #0A0A0A; border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 16px; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 13px;">
                    <span style="color: #8A8F98;">Monthly Budget Limit</span>
                    <span style="color: #F4F4F5; font-weight: 600;">₹{budget:,.2f}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 13px;">
                    <span style="color: #8A8F98;">Already Spent</span>
                    <span style="color: #F87171; font-weight: 600;">₹{cur_exp:,.2f}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 13px;">
                    <span style="color: #8A8F98;">Remaining Budget</span>
                    <span style="color: {'#34D399' if rem >= 0 else '#F87171'}; font-weight: 600;">₹{rem:,.2f}</span>
                </div>
                <div style="background: #1C1C1E; border-radius: 999px; height: 7px; overflow: hidden;">
                    <div style="background: {bar_col}; width: {min(used_pct, 100)}%; height: 100%;"></div>
                </div>
                <div style="font-size: 11px; color: #71717A; margin-top: 6px; text-align: right;">{round(used_pct, 1)}% utilized</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='font-size: 12px; font-weight: 600; color: #A1A1AA; margin-bottom: 8px;'>Supported Categories</div>", unsafe_allow_html=True)
            cat_pills = " ".join([f"<span class='cat-pill'>{CATEGORY_ICONS.get(c, '📦')} {c}</span>" for c in CATEGORIES])
            st.markdown(f"<div style='display: flex; flex-wrap: wrap; gap: 7px;'>{cat_pills}</div>", unsafe_allow_html=True)

    # Recent Expenses Table
    with st.container(border=True):
        st.markdown("<div class='card-title'>Recent Expenses</div>", unsafe_allow_html=True)
        st.markdown("<div class='card-desc'>Last 5 recorded expense entries</div>", unsafe_allow_html=True)
        all_expenses = [t for t in load_transactions() if t["type"] == "expense"]
        if all_expenses:
            rows_html = ""
            for t in reversed(all_expenses[-5:]):
                icon = CATEGORY_ICONS.get(t["category"], "📦")
                rows_html += (
                    f"<tr>"
                    f"<td style='color:#8A8F98;'>{t['date']}</td>"
                    f"<td><span class='cat-pill'>{icon} {t['category']}</span></td>"
                    f"<td style='color:#F87171; font-weight:700;'>-₹{t['amount']:,.2f}</td>"
                    f"<td>{t['description']}</td>"
                    f"</tr>"
                )
            st.html(
                "<div class='tx-table-wrap'><table class='tx-table'>"
                "<thead><tr><th>Date</th><th>Category</th><th>Amount</th><th>Description</th></tr></thead>"
                f"<tbody>{rows_html}</tbody></table></div>"
            )
        else:
            st.info("No expenses recorded yet.")


# -----------------------------------------------------------------------------
# PAGE 3: Add Income
# -----------------------------------------------------------------------------
elif menu_choice == "➕  Add Income":
    render_page_header(
        "Record Income Deposit",
        "Log salary, freelance earnings, pocket money, or other inflows",
        '<line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>'
    )

    col_inc_form, col_inc_info = st.columns([1.45, 1.15])

    with col_inc_form:
        with st.container(border=True):
            st.markdown("<div class='card-title'>Income Details</div>", unsafe_allow_html=True)
            st.markdown("<div class='card-desc'>Saved directly to expenses.csv</div>", unsafe_allow_html=True)

            with st.form("add_income_form", clear_on_submit=True):
                inc_date = st.date_input("Deposit Date", value=date.today())

                col_source, col_amt = st.columns([1.2, 1])
                with col_source:
                    income_categories = ["Income", "Salary", "Pocket Money", "Freelance", "Investment", "Gift", "Others"]
                    inc_category = st.selectbox("Source / Category", options=income_categories, index=0)

                with col_amt:
                    inc_amount = st.number_input("Amount (₹)", min_value=1.0, value=5000.0, step=500.0)

                inc_desc = st.text_input("Description / Source Note", placeholder="e.g. Monthly allowance, Freelance payout, Bonus")
                submit_income = st.form_submit_button("Save Income Deposit", use_container_width=True)

                if submit_income:
                    if inc_amount <= 0:
                        st.error("Income amount must be greater than 0.")
                    elif not inc_desc.strip():
                        st.warning("Please provide a short description or source note.")
                    else:
                        date_str = inc_date.strftime("%Y-%m-%d")
                        add_transaction_entry(date_str, "income", inc_category, inc_amount, inc_desc)
                        st.toast(f"Deposited ₹{inc_amount:,.2f} ({inc_category})", icon="✅")
                        st.success(f"Income of ₹{inc_amount:,.2f} recorded in '{inc_category}'.")
                        st.rerun()

    with col_inc_info:
        with st.container(border=True):
            st.markdown("<div class='card-title'>Current Month Inflow</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card-desc'>Summary for {datetime.now().strftime('%B %Y')}</div>", unsafe_allow_html=True)

            current_month_key = date.today().strftime("%Y-%m")
            all_txs = load_transactions()
            month_txs = filter_by_month(all_txs, current_month_key)
            cur_inc, cur_exp, cur_bal = calculate_totals(month_txs)

            st.markdown(f"""
            <div style="background: #0A0A0A; border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 18px;">
                <div style="font-size: 11px; color: #8A8F98; text-transform: uppercase; font-weight: 600; letter-spacing: 0.7px; margin-bottom: 6px;">Total Earned This Month</div>
                <div style="font-size: 30px; font-weight: 700; color: #10B981; margin-bottom: 14px;">₹{cur_inc:,.2f}</div>
                <div style="display: flex; justify-content: space-between; font-size: 13px; color: #A1A1AA; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 10px;">
                    <span>Total Spent</span>
                    <span style="color: #F87171; font-weight: 600;">₹{cur_exp:,.2f}</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 13px; color: #A1A1AA; margin-top: 8px;">
                    <span>Net Savings</span>
                    <span style="color: {'#34D399' if cur_bal >= 0 else '#F87171'}; font-weight: 600;">₹{cur_bal:,.2f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("<div class='card-title'>Recent Income Deposits</div>", unsafe_allow_html=True)
        st.markdown("<div class='card-desc'>Last 5 recorded income entries</div>", unsafe_allow_html=True)
        all_incomes = [t for t in load_transactions() if t["type"] == "income"]
        if all_incomes:
            rows_html = ""
            for t in reversed(all_incomes[-5:]):
                rows_html += (
                    f"<tr>"
                    f"<td style='color:#8A8F98;'>{t['date']}</td>"
                    f"<td><span class='cat-pill'>💵 {t['category']}</span></td>"
                    f"<td style='color:#34D399; font-weight:700;'>+₹{t['amount']:,.2f}</td>"
                    f"<td>{t['description']}</td>"
                    f"</tr>"
                )
            st.html(
                "<div class='tx-table-wrap'><table class='tx-table'>"
                "<thead><tr><th>Date</th><th>Source</th><th>Amount</th><th>Description</th></tr></thead>"
                f"<tbody>{rows_html}</tbody></table></div>"
            )
        else:
            st.info("No income records found.")


# -----------------------------------------------------------------------------
# PAGE 4: Transactions Ledger
# -----------------------------------------------------------------------------
elif menu_choice == "📑  Transactions":
    render_page_header(
        "Transaction Ledger",
        "Search, filter, audit, and export your complete financial history",
        '<line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/>'
    )

    transactions = load_transactions()

    if not transactions:
        st.info("No transactions found in expenses.csv. Add an income or expense to begin.")
    else:
        with st.container(border=True):
            col_search, col_fmonth, col_ftype = st.columns([2, 1, 1])
            with col_search:
                search_query = st.text_input("Search", placeholder="Filter by note or category...")
            with col_fmonth:
                available_months = ["All Months"] + get_available_months(transactions)
                selected_fmonth = st.selectbox("Month", options=available_months)
            with col_ftype:
                selected_ftype = st.selectbox("Type", options=["All", "Expense", "Income"])

            col_fcat, col_sort = st.columns(2)
            with col_fcat:
                all_cats = sorted(list(set([t["category"] for t in transactions])))
                selected_fcat = st.selectbox("Category", options=["All"] + all_cats)
            with col_sort:
                sort_choice = st.selectbox(
                    "Sort By",
                    options=["Date (Newest First)", "Date (Oldest First)", "Amount (High to Low)", "Amount (Low to High)"]
                )

        indexed_txs = list(enumerate(transactions))
        if selected_fmonth != "All Months":
            indexed_txs = [item for item in indexed_txs if item[1]["date"][:7] == selected_fmonth]
        if selected_ftype != "All":
            indexed_txs = [item for item in indexed_txs if item[1]["type"].lower() == selected_ftype.lower()]
        if selected_fcat != "All":
            indexed_txs = [item for item in indexed_txs if item[1]["category"] == selected_fcat]
        if search_query.strip():
            q = search_query.strip().lower()
            indexed_txs = [item for item in indexed_txs if q in item[1]["description"].lower() or q in item[1]["category"].lower()]

        if sort_choice == "Date (Newest First)":
            indexed_txs.sort(key=lambda x: x[1]["date"], reverse=True)
        elif sort_choice == "Date (Oldest First)":
            indexed_txs.sort(key=lambda x: x[1]["date"])
        elif sort_choice == "Amount (High to Low)":
            indexed_txs.sort(key=lambda x: x[1]["amount"], reverse=True)
        elif sort_choice == "Amount (Low to High)":
            indexed_txs.sort(key=lambda x: x[1]["amount"])

        filtered_incomes = sum(item[1]["amount"] for item in indexed_txs if item[1]["type"] == "income")
        filtered_expenses = sum(item[1]["amount"] for item in indexed_txs if item[1]["type"] == "expense")
        filtered_net = filtered_incomes - filtered_expenses

        st.markdown(f"""
        <div style="display: flex; flex-wrap: wrap; gap: 24px; align-items: center; background: #0C0C0C; border: 1px solid rgba(255,255,255,0.07); border-radius: 12px; padding: 12px 18px; margin: 12px 0 16px 0;">
            <div style="font-size: 13px; color: #8A8F98;">Records: <strong style="color: #FFFFFF;">{len(indexed_txs)}</strong></div>
            <div style="font-size: 13px; color: #8A8F98;">Inflow: <strong style="color: #34D399;">₹{filtered_incomes:,.2f}</strong></div>
            <div style="font-size: 13px; color: #8A8F98;">Outflow: <strong style="color: #F87171;">₹{filtered_expenses:,.2f}</strong></div>
            <div style="font-size: 13px; color: #8A8F98;">Net: <strong style="color: {'#34D399' if filtered_net >= 0 else '#F87171'};">₹{filtered_net:,.2f}</strong></div>
        </div>
        """, unsafe_allow_html=True)

        if not indexed_txs:
            st.warning("No transactions match the selected filters.")
        else:
            with st.container(border=True):
                rows_html = ""
                for _, t in indexed_txs:
                    icon = CATEGORY_ICONS.get(t["category"], "📦")
                    badge = "badge-green" if t["type"] == "income" else "badge-red"
                    amount_prefix = "+₹" if t["type"] == "income" else "-₹"
                    amount_color = "#34D399" if t["type"] == "income" else "#F87171"
                    rows_html += (
                        f"<tr>"
                        f"<td style='color:#8A8F98; font-weight:500;'>{t['date']}</td>"
                        f"<td><span class='{badge}'>{t['type'].upper()}</span></td>"
                        f"<td><span class='cat-pill'>{icon} {t['category']}</span></td>"
                        f"<td class='nowrap' style='font-weight:700; color:{amount_color};'>{amount_prefix}{t['amount']:,.2f}</td>"
                        f"<td style='color:#E4E4E7;'>{t['description']}</td>"
                        f"</tr>"
                    )
                st.html(
                    "<div class='tx-table-wrap'><table class='tx-table'>"
                    "<thead><tr><th>Date</th><th>Type</th><th>Category</th><th>Amount</th><th>Description</th></tr></thead>"
                    f"<tbody>{rows_html}</tbody></table></div>"
                )

            col_exp_csv, col_del = st.columns([1, 1.5])
            with col_exp_csv:
                df_export = pd.DataFrame([item[1] for item in indexed_txs])
                csv_data = df_export.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Export Filtered CSV",
                    data=csv_data,
                    file_name=f"transactions_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            with col_del:
                with st.expander("Delete a Transaction Record"):
                    tx_options = {
                        f"#{orig_idx+1}: {t['date']} | {t['type'].upper()} | {t['category']} | ₹{t['amount']:,.2f} ({t['description']})": orig_idx
                        for orig_idx, t in indexed_txs
                    }
                    selected_tx_label = st.selectbox("Select record to remove", options=list(tx_options.keys()))
                    if st.button("Confirm Delete Record", type="primary"):
                        target_idx = tx_options[selected_tx_label]
                        deleted_item = delete_transaction_entry(target_idx)
                        if deleted_item:
                            st.toast(f"Deleted: {deleted_item['description']}", icon="🗑️")
                            st.success("Transaction removed from expenses.csv.")
                            st.rerun()


# -----------------------------------------------------------------------------
# PAGE 5: Monthly Reports & Category Analysis
# -----------------------------------------------------------------------------
elif menu_choice == "📈  Monthly Reports":
    transactions = load_transactions()
    budget = load_budget()
    available_months = get_available_months(transactions)

    col_m1, col_m2 = st.columns([3.2, 1.1])
    with col_m1:
        render_page_header(
            "Monthly Reports & Analytics",
            "Category performance, efficiency ratios, and exportable monthly statements",
            '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>'
        )
    with col_m2:
        rep_month = st.selectbox("Analysis Month", options=available_months, index=0)

    month_tx = filter_by_month(transactions, rep_month)
    income, expense, balance = calculate_totals(month_tx)
    breakdown = get_category_breakdown(month_tx)
    savings_rate = (balance / income * 100) if income > 0 else 0
    ratio = (expense / budget * 100) if budget > 0 else 0

    pairs = sorted([(val, cat) for cat, val in breakdown.items() if val > 0], reverse=True)
    top_category = pairs[0][1] if pairs else "None"
    top_amount = pairs[0][0] if pairs else 0.0

    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    with col_k1:
        st.markdown(f"""
        <div class="metric-card" style="--accent-color: #10B981;">
            <div class="metric-label"><span>Net Savings</span><span class="badge-green">Health</span></div>
            <div class="metric-value">₹{balance:,.2f}</div>
            <div class="metric-sub">Savings rate: {round(savings_rate, 1)}%</div>
        </div>
        """, unsafe_allow_html=True)

    with col_k2:
        st.markdown(f"""
        <div class="metric-card" style="--accent-color: #A78BFA;">
            <div class="metric-label"><span>Top Category</span><span class="badge-silver">Highest</span></div>
            <div class="metric-value" style="font-size: 21px;">{CATEGORY_ICONS.get(top_category, '📦')} {top_category}</div>
            <div class="metric-sub">Total: ₹{top_amount:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_k3:
        exp_ratio = (expense / income * 100) if income > 0 else (100 if expense > 0 else 0)
        st.markdown(f"""
        <div class="metric-card" style="--accent-color: #F59E0B;">
            <div class="metric-label"><span>Expense / Income</span><span class="badge-amber">Ratio</span></div>
            <div class="metric-value">{round(exp_ratio, 1)}%</div>
            <div class="metric-sub">Outflow as % of earnings</div>
        </div>
        """, unsafe_allow_html=True)

    with col_k4:
        b_cls = "badge-red" if ratio > 100 else "badge-amber" if ratio >= 80 else "badge-green"
        b_col = "#EF4444" if ratio > 100 else "#F59E0B" if ratio >= 80 else "#10B981"
        st.markdown(f"""
        <div class="metric-card" style="--accent-color: {b_col};">
            <div class="metric-label"><span>Budget Used</span><span class="{b_cls}">Limit</span></div>
            <div class="metric-value">{round(ratio, 1)}%</div>
            <div class="metric-sub">Of ₹{budget:,.2f} ceiling</div>
        </div>
        """, unsafe_allow_html=True)

    col_chart_left, col_chart_right = st.columns([1.25, 1.15])

    with col_chart_left:
        with st.container(border=True):
            st.markdown("<div class='card-title'>Category Analysis</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card-desc'>Ranked expenditure by category for {rep_month}</div>", unsafe_allow_html=True)

            if pairs:
                df_bars = pd.DataFrame(pairs, columns=["Amount", "Category"])
                df_bars["Percent"] = (df_bars["Amount"] / expense * 100).round(1)
                df_bars["Label"] = df_bars.apply(lambda r: f"₹{r['Amount']:,.0f} ({r['Percent']}%)", axis=1)

                fig_hbar = px.bar(
                    df_bars,
                    x="Amount",
                    y="Category",
                    orientation="h",
                    color="Category",
                    color_discrete_map=CATEGORY_COLORS,
                    text="Label"
                )
                fig_hbar.update_traces(
                    textposition="auto",
                    textfont=dict(size=12, color="#F4F4F5"),
                    hovertemplate="<b>%{y}</b><br>Spent: ₹%{x:,.2f}<extra></extra>",
                    marker_line_width=0
                )
                apply_dark_chart_theme(fig_hbar, height=300)
                fig_hbar.update_layout(
                    showlegend=False,
                    xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#8A8F98", tickprefix="₹"),
                    yaxis=dict(color="#E4E4E7", autorange="reversed"),
                    margin=dict(t=10, b=16, l=10, r=20),
                )
                st.plotly_chart(fig_hbar, use_container_width=True)
            else:
                st.info(f"No expense entries for {rep_month}.")

    with col_chart_right:
        with st.container(border=True):
            st.markdown("<div class='card-title'>Category Summary</div>", unsafe_allow_html=True)
            st.markdown("<div class='card-desc'>Aligned spending & share breakdown</div>", unsafe_allow_html=True)

            if pairs:
                rows_cat = ""
                for amt, cat in pairs:
                    pct = (amt / expense * 100) if expense > 0 else 0
                    icon = CATEGORY_ICONS.get(cat, "📦")
                    rows_cat += (
                        f"<tr>"
                        f"<td><span class='cat-pill'>{icon} {cat}</span></td>"
                        f"<td style='font-weight:700; color:#F87171; text-align:right;'>₹{amt:,.2f}</td>"
                        f"<td style='color:#A1A1AA; text-align:right;'>{round(pct, 1)}%</td>"
                        f"</tr>"
                    )
                st.html(
                    "<div class='tx-table-wrap'><table class='tx-table compact'>"
                    "<thead><tr><th>Category</th><th style='text-align:right;'>Amount</th><th style='text-align:right;'>Share</th></tr></thead>"
                    f"<tbody>{rows_cat}</tbody></table></div>"
                )
            else:
                st.info("No category data available.")

    with st.container(border=True):
        st.markdown(f"<div class='card-title'>Executive Statement ({rep_month})</div>", unsafe_allow_html=True)
        st.markdown("<div class='card-desc'>Downloadable plain-text monthly summary</div>", unsafe_allow_html=True)

        report_text = f"""==================================================
PERSONAL EXPENSE & BUDGET REPORT: {rep_month}
==================================================
Total Income       : Rs. {income:,.2f}
Total Expenditure  : Rs. {expense:,.2f}
Remaining Balance  : Rs. {balance:,.2f}
Savings Rate       : {round(savings_rate, 1)}%
Monthly Budget     : Rs. {budget:,.2f}
Budget Utilization : {round(ratio, 1)}%

CATEGORY-WISE SPENDING:
"""
        for amt, cat in pairs:
            pct = (amt / expense * 100) if expense > 0 else 0
            report_text += f"- {cat.ljust(15)}: Rs. {amt:,.2f} ({round(pct, 1)}%)\n"

        report_text += f"\nTOP SPENDING CATEGORY: {top_category}\n"
        if budget > 0:
            if ratio > 100:
                report_text += f"STATUS: ALERT - Budget exceeded by Rs. {expense - budget:,.2f}!\n"
            elif ratio >= 80:
                report_text += f"STATUS: WARNING - 80%+ of budget consumed. Rs. {budget - expense:,.2f} left.\n"
            else:
                report_text += f"STATUS: SAFE - Within budget. Rs. {budget - expense:,.2f} left.\n"
        else:
            report_text += "STATUS: No budget set.\n"
        report_text += "=================================================="

        st.text_area("Generated Summary", value=report_text, height=210, label_visibility="collapsed")
        st.download_button(
            label=f"Download Monthly Report ({rep_month}.txt)",
            data=report_text,
            file_name=f"Monthly_Report_{rep_month}.txt",
            mime="text/plain",
            use_container_width=True
        )


# -----------------------------------------------------------------------------
# PAGE 6: Budget Settings
# -----------------------------------------------------------------------------
elif menu_choice == "⚙️  Budget Settings":
    render_page_header(
        "Budget Configuration",
        "Set your monthly spending ceiling, alert thresholds, and verify storage",
        '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>'
    )

    current_budget = load_budget()
    col_bset, col_binfo = st.columns([1.45, 1.15])

    with col_bset:
        with st.container(border=True):
            st.markdown("<div class='card-title'>Update Monthly Budget</div>", unsafe_allow_html=True)
            st.markdown("<div class='card-desc'>Persisted to budget.txt for both web and CLI trackers</div>", unsafe_allow_html=True)

            # Quick preset buttons (2x2 grid for clean responsive display)
            st.markdown("<div style='font-size: 12px; color: #8A8F98; margin-bottom: 6px;'>Quick Presets</div>", unsafe_allow_html=True)
            p_row1 = st.columns(2)
            p_row2 = st.columns(2)
            preset_slots = [p_row1[0], p_row1[1], p_row2[0], p_row2[1]]
            presets = [5000, 10000, 20000, 50000]
            for idx, amt in enumerate(presets):
                if preset_slots[idx].button(f"₹{amt:,}", key=f"preset_{amt}", type="secondary", use_container_width=True):
                    save_budget_to_file(amt)
                    st.toast(f"Budget set to ₹{amt:,}", icon="✅")
                    st.rerun()

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

            with st.form("set_budget_form"):
                new_budget_val = st.number_input(
                    "Custom Monthly Budget Limit (₹)",
                    min_value=0.0,
                    value=float(current_budget) if current_budget > 0 else 15000.0,
                    step=1000.0
                )
                save_budget_btn = st.form_submit_button("Save Budget Limit", use_container_width=True)

                if save_budget_btn:
                    save_budget_to_file(new_budget_val)
                    st.toast(f"Budget updated to ₹{new_budget_val:,.2f}", icon="✅")
                    st.success(f"Monthly budget limit saved: ₹{new_budget_val:,.2f}")
                    st.rerun()

    with col_binfo:
        with st.container(border=True):
            st.markdown("<div class='card-title'>Active Budget Tiers</div>", unsafe_allow_html=True)
            st.markdown("<div class='card-desc'>Automated threshold bands for your current limit</div>", unsafe_allow_html=True)

            if current_budget > 0:
                warn_threshold = current_budget * 0.8
                st.markdown(f"""
                <div style="background: #0A0A0A; border: 1px solid rgba(255,255,255,0.06); border-left: 3px solid #10B981; border-radius: 10px; padding: 13px 15px; margin-bottom: 10px;">
                    <div style="font-size: 13px; font-weight: 600; color: #34D399;">Safe Zone (0% – 79%)</div>
                    <div style="font-size: 12px; color: #8A8F98; margin-top: 3px;">Spending up to <strong>₹{warn_threshold:,.2f}</strong></div>
                </div>
                <div style="background: #0A0A0A; border: 1px solid rgba(255,255,255,0.06); border-left: 3px solid #F59E0B; border-radius: 10px; padding: 13px 15px; margin-bottom: 10px;">
                    <div style="font-size: 13px; font-weight: 600; color: #FBBF24;">Warning Zone (80% – 99%)</div>
                    <div style="font-size: 12px; color: #8A8F98; margin-top: 3px;">Between <strong>₹{warn_threshold:,.2f}</strong> and <strong>₹{current_budget:,.2f}</strong></div>
                </div>
                <div style="background: #0A0A0A; border: 1px solid rgba(255,255,255,0.06); border-left: 3px solid #EF4444; border-radius: 10px; padding: 13px 15px;">
                    <div style="font-size: 13px; font-weight: 600; color: #F87171;">Over-Budget Zone (100%+)</div>
                    <div style="font-size: 12px; color: #8A8F98; margin-top: 3px;">Exceeding <strong>₹{current_budget:,.2f}</strong></div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("Set a budget above to view active threshold bands.")

    with st.container(border=True):
        st.markdown("<div class='card-title'>Storage &amp; System Status</div>", unsafe_allow_html=True)
        st.markdown("<div class='card-desc'>Local persistence files shared with the CLI tracker</div>", unsafe_allow_html=True)

        all_txs = load_transactions()
        col_st1, col_st2, col_st3 = st.columns(3)
        with col_st1:
            st.markdown(f"""
            <div style="background: #0A0A0A; border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 14px;">
                <div style="font-size: 10.5px; color: #71717A; text-transform: uppercase; letter-spacing: 0.7px;">Transaction Store</div>
                <div style="font-size: 15px; font-weight: 700; color: #F4F4F5; margin: 4px 0;">{FILE_NAME}</div>
                <div style="font-size: 12px; color: #34D399;">{len(all_txs)} records saved</div>
            </div>
            """, unsafe_allow_html=True)

        with col_st2:
            st.markdown(f"""
            <div style="background: #0A0A0A; border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 14px;">
                <div style="font-size: 10.5px; color: #71717A; text-transform: uppercase; letter-spacing: 0.7px;">Budget Store</div>
                <div style="font-size: 15px; font-weight: 700; color: #F4F4F5; margin: 4px 0;">{BUDGET_FILE}</div>
                <div style="font-size: 12px; color: #34D399;">Current: ₹{current_budget:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_st3:
            st.markdown("""
            <div style="background: #0A0A0A; border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 14px;">
                <div style="font-size: 10.5px; color: #71717A; text-transform: uppercase; letter-spacing: 0.7px;">CLI Application</div>
                <div style="font-size: 15px; font-weight: 700; color: #F4F4F5; margin: 4px 0;">expense_tracker.py</div>
                <div style="font-size: 12px; color: #34D399;">Intact &amp; synchronized</div>
            </div>
            """, unsafe_allow_html=True)

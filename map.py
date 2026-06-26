"""
REST-OS Global Enterprise
A premium multi-branch restaurant management & financial ERP dashboard.
Built with Streamlit.
"""

import streamlit as st
import pandas as pd
from datetime import date, datetime
import uuid

# ──────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="REST-OS Global Enterprise",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────
# GLOBAL CONFIGURATION & CONSTANTS
# ──────────────────────────────────────────────────────────────────────────
USD_RATE = 3.75          # 1 USD = 3.75 SAR
ADMIN_PASSWORD = "1234"
ABSENCE_PENALTY = 100.0  # SAR, flat deduction for an unexcused absence
ALL_BRANCHES_LABEL = "🌍 All Branches (Global Group View)"

BRANCH_SEED = {
    "Buddy's Burger - Riyadh Branch": 60000.0,
    "Buddy's Burger - Jeddah Branch": 45000.0,
}


def new_id() -> str:
    """Short unique employee code."""
    return "EMP-" + uuid.uuid4().hex[:6].upper()


# ──────────────────────────────────────────────────────────────────────────
# SESSION STATE INITIALIZATION
# ──────────────────────────────────────────────────────────────────────────
def init_state():
    if "initialized" in st.session_state:
        return

    st.session_state.initialized = True
    st.session_state.currency = "SAR"
    st.session_state.admin_unlocked = False
    st.session_state.selected_branch = ALL_BRANCHES_LABEL

    st.session_state.branches = dict(BRANCH_SEED)

    # active employees
    st.session_state.employees = {
        "EMP-A1B2C3": {
            "code": "EMP-A1B2C3",
            "name": "Omar Al-Fahad",
            "branch": "Buddy's Burger - Riyadh Branch",
            "hire_date": date(2023, 4, 12),
            "base_salary": 6500.0,
            "bonuses": 500.0,
            "deductions": 0.0,
        },
        "EMP-D4E5F6": {
            "code": "EMP-D4E5F6",
            "name": "Sara Al-Mutairi",
            "branch": "Buddy's Burger - Riyadh Branch",
            "hire_date": date(2022, 11, 1),
            "base_salary": 5800.0,
            "bonuses": 0.0,
            "deductions": 100.0,
        },
        "EMP-G7H8I9": {
            "code": "EMP-G7H8I9",
            "name": "Khalid Bin Nasser",
            "branch": "Buddy's Burger - Jeddah Branch",
            "hire_date": date(2024, 1, 20),
            "base_salary": 5200.0,
            "bonuses": 250.0,
            "deductions": 0.0,
        },
    }

    # archived / terminated employees
    st.session_state.archive = {
        "EMP-X9Y8Z7": {
            "code": "EMP-X9Y8Z7",
            "name": "Fahad Al-Otaibi",
            "branch": "Buddy's Burger - Jeddah Branch",
            "hire_date": date(2021, 6, 5),
            "base_salary": 4800.0,
            "bonuses": 0.0,
            "deductions": 0.0,
            "termination_date": date(2025, 9, 30),
            "termination_reason": "Voluntary resignation - relocation",
        }
    }

    # attendance log: {(employee_code, iso_date): "Present"/"Absent"}
    st.session_state.attendance = {}


init_state()


# ──────────────────────────────────────────────────────────────────────────
# CURRENCY HELPERS
# ──────────────────────────────────────────────────────────────────────────
def fmt_currency(amount_sar: float) -> str:
    """Format a SAR-denominated amount according to the global currency toggle."""
    if st.session_state.currency == "USD":
        value = amount_sar / USD_RATE
        return f"$ {value:,.2f}"
    return f"SAR {amount_sar:,.2f}"


def convert_for_display(amount_sar: float) -> float:
    if st.session_state.currency == "USD":
        return amount_sar / USD_RATE
    return amount_sar


# ──────────────────────────────────────────────────────────────────────────
# CSS — DARK ENTERPRISE THEME
# ──────────────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background: radial-gradient(circle at 10% 0%, #121829 0%, #0b0f19 45%, #060810 100%);
            color: #e7eaf3;
        }

        /* Hide default streamlit chrome */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header[data-testid="stHeader"] {background: rgba(0,0,0,0);}

        /* ── Header banner ─────────────────────────────────────────── */
        .restos-header {
            background: linear-gradient(135deg, rgba(34,42,69,0.85) 0%, rgba(13,17,28,0.95) 100%);
            border: 1px solid rgba(122, 162, 255, 0.25);
            border-radius: 18px;
            padding: 22px 30px;
            margin-bottom: 22px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.04);
            position: relative;
            overflow: hidden;
        }
        .restos-header::before {
            content: "";
            position: absolute;
            top: -40%; right: -10%;
            width: 280px; height: 280px;
            background: radial-gradient(circle, rgba(94,129,244,0.28) 0%, rgba(94,129,244,0) 70%);
            pointer-events: none;
        }
        .restos-title {
            font-size: 28px;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(90deg, #9db4ff 0%, #e7eaf3 60%);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        }
        .restos-subtitle {
            font-size: 13px;
            color: #8a93b3;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-top: 4px;
            font-weight: 600;
        }

        /* ── KPI Cards ──────────────────────────────────────────────── */
        .kpi-card {
            background: linear-gradient(160deg, rgba(28,34,56,0.9) 0%, rgba(15,19,32,0.95) 100%);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 16px;
            padding: 18px 20px;
            position: relative;
            overflow: hidden;
            min-height: 118px;
            box-shadow: 0 6px 18px rgba(0,0,0,0.35);
        }
        .kpi-card::after {
            content: "";
            position: absolute;
            left: 0; top: 0; bottom: 0;
            width: 4px;
            background: var(--accent, #5e81f4);
            box-shadow: 0 0 18px var(--accent, #5e81f4);
        }
        .kpi-label {
            font-size: 11.5px;
            color: #8a93b3;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        .kpi-value {
            font-size: 25px;
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
            color: #f1f3fa;
        }
        .kpi-value.positive { color: #5ee6a4; }
        .kpi-value.negative { color: #ff6b81; }
        .kpi-icon {
            position: absolute;
            right: 16px; top: 14px;
            font-size: 22px;
            opacity: 0.5;
        }

        /* ── Section card wrapper ──────────────────────────────────── */
        .section-card {
            background: linear-gradient(160deg, rgba(22,27,45,0.7) 0%, rgba(12,15,25,0.85) 100%);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 16px;
            padding: 20px 22px;
            margin-bottom: 16px;
        }
        .section-heading {
            font-size: 16px;
            font-weight: 700;
            color: #c9d2f0;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* ── Badges ─────────────────────────────────────────────────── */
        .badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.4px;
        }
        .badge-green { background: rgba(94,230,164,0.15); color: #5ee6a4; border: 1px solid rgba(94,230,164,0.3);}
        .badge-red { background: rgba(255,107,129,0.15); color: #ff6b81; border: 1px solid rgba(255,107,129,0.3);}
        .badge-blue { background: rgba(94,129,244,0.15); color: #9db4ff; border: 1px solid rgba(94,129,244,0.3);}

        /* ── Buttons ────────────────────────────────────────────────── */
        div.stButton > button {
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.1);
            background: linear-gradient(160deg, #1b2238 0%, #11152233 100%);
            color: #e7eaf3;
            font-weight: 600;
            transition: all 0.15s ease;
        }
        div.stButton > button:hover {
            border-color: #5e81f4;
            color: #9db4ff;
            box-shadow: 0 0 0 2px rgba(94,129,244,0.18);
        }

        /* Primary action buttons (kept readable) */
        div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #5e81f4 0%, #3c5fd0 100%);
            border: none;
            color: white;
        }

        /* ── Tabs ───────────────────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            background: rgba(15,19,32,0.6);
            padding: 6px;
            border-radius: 12px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 9px;
            color: #8a93b3;
            font-weight: 600;
            padding: 10px 16px;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #5e81f4 0%, #3c5fd0 100%) !important;
            color: white !important;
        }

        /* ── Footer ─────────────────────────────────────────────────── */
        .restos-footer {
            text-align: center;
            padding: 22px 0 10px 0;
            color: #5b6485;
            font-size: 12.5px;
            letter-spacing: 0.4px;
            border-top: 1px solid rgba(255,255,255,0.06);
            margin-top: 30px;
        }

        /* Misc */
        hr { border-color: rgba(255,255,255,0.08); }
        .stDataFrame { border-radius: 12px; overflow: hidden; }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()


# ──────────────────────────────────────────────────────────────────────────
# DATA HELPERS
# ──────────────────────────────────────────────────────────────────────────
def employees_in_scope():
    """Return dict of active employees filtered by the selected branch scope."""
    branch = st.session_state.selected_branch
    if branch == ALL_BRANCHES_LABEL:
        return st.session_state.employees
    return {
        code: emp
        for code, emp in st.session_state.employees.items()
        if emp["branch"] == branch
    }


def net_salary(emp: dict) -> float:
    return emp["base_salary"] + emp["bonuses"] - emp["deductions"]


def budget_in_scope() -> float:
    branch = st.session_state.selected_branch
    if branch == ALL_BRANCHES_LABEL:
        return sum(st.session_state.branches.values())
    return st.session_state.branches.get(branch, 0.0)


# ──────────────────────────────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────────────────────────────
header_left, header_right = st.columns([3, 1])
with header_left:
    st.markdown(
        """
        <div class="restos-header">
            <div class="restos-title">🏢 REST-OS Global Enterprise</div>
            <div class="restos-subtitle">Multi-Branch Restaurant Financial ERP &nbsp;•&nbsp; Live Operations Console</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with header_right:
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    currency_choice = st.radio(
        "Display Currency",
        options=["SAR", "USD"],
        horizontal=True,
        index=0 if st.session_state.currency == "SAR" else 1,
        key="currency_radio",
    )
    st.session_state.currency = currency_choice
    st.caption(f"Fixed rate: 1 USD = {USD_RATE} SAR")

st.write("")

# ──────────────────────────────────────────────────────────────────────────
# SIDEBAR — SECURITY GATEWAY, BRANCH SELECTION, HIRE EMPLOYEE
# ──────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔐 Admin Access")

    if not st.session_state.admin_unlocked:
        pwd = st.text_input("Enter admin password", type="password", key="pwd_input")
        if st.button("Unlock Operations", use_container_width=True, type="primary"):
            if pwd == ADMIN_PASSWORD:
                st.session_state.admin_unlocked = True
                st.success("Access granted.")
                st.rerun()
            else:
                st.error("Incorrect password.")
        st.caption("Default credential: 1234")
    else:
        st.markdown("<span class='badge badge-green'>🔓 ADMIN UNLOCKED</span>", unsafe_allow_html=True)
        if st.button("Lock Session", use_container_width=True):
            st.session_state.admin_unlocked = False
            st.rerun()

    st.markdown("---")
    st.markdown("### 🏬 Branch Scope")

    branch_options = [ALL_BRANCHES_LABEL] + list(st.session_state.branches.keys())
    current_idx = (
        branch_options.index(st.session_state.selected_branch)
        if st.session_state.selected_branch in branch_options
        else 0
    )
    selected = st.selectbox(
        "Select branch view",
        options=branch_options,
        index=current_idx,
        key="branch_select",
    )
    st.session_state.selected_branch = selected

    if selected != ALL_BRANCHES_LABEL:
        st.caption(f"Branch budget: {fmt_currency(st.session_state.branches[selected])}")

    # ── Hire Employee (only when a specific branch is selected & admin unlocked) ──
    if st.session_state.admin_unlocked and selected != ALL_BRANCHES_LABEL:
        st.markdown("---")
        st.markdown("### ➕ Hire Employee")
        with st.form("hire_form", clear_on_submit=True):
            new_name = st.text_input("Employee Name")
            new_salary = st.number_input("Base Salary (SAR)", min_value=0.0, step=100.0, value=4000.0)
            new_hire_date = st.date_input("Date of Hiring", value=date.today())
            submitted = st.form_submit_button("Hire Now", use_container_width=True, type="primary")

            if submitted:
                if not new_name.strip():
                    st.warning("Please enter an employee name.")
                else:
                    code = new_id()
                    st.session_state.employees[code] = {
                        "code": code,
                        "name": new_name.strip(),
                        "branch": selected,
                        "hire_date": new_hire_date,
                        "base_salary": float(new_salary),
                        "bonuses": 0.0,
                        "deductions": 0.0,
                    }
                    st.success(f"{new_name} hired at {selected}.")
                    st.rerun()
    elif selected != ALL_BRANCHES_LABEL:
        st.markdown("---")
        st.info("🔒 Unlock admin access to hire employees.")

    st.markdown("---")
    st.caption(f"Active employees: {len(st.session_state.employees)}")
    st.caption(f"Archived employees: {len(st.session_state.archive)}")


# ──────────────────────────────────────────────────────────────────────────
# KPI CARDS
# ──────────────────────────────────────────────────────────────────────────
scope_employees = employees_in_scope()
total_budget = budget_in_scope()
total_base = sum(e["base_salary"] for e in scope_employees.values())
total_bonuses = sum(e["bonuses"] for e in scope_employees.values())
total_deductions = sum(e["deductions"] for e in scope_employees.values())
net_payroll = total_base + total_bonuses - total_deductions
vault_remaining = total_budget - net_payroll

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(
        f"""
        <div class="kpi-card" style="--accent:#5e81f4;">
            <div class="kpi-icon">💰</div>
            <div class="kpi-label">Total Monitored Budget</div>
            <div class="kpi-value">{fmt_currency(total_budget)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi2:
    st.markdown(
        f"""
        <div class="kpi-card" style="--accent:#9d7cf4;">
            <div class="kpi-icon">🧾</div>
            <div class="kpi-label">Net Payroll</div>
            <div class="kpi-value">{fmt_currency(net_payroll)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi3:
    st.markdown(
        f"""
        <div class="kpi-card" style="--accent:#ff6b81;">
            <div class="kpi-icon">⚠️</div>
            <div class="kpi-label">Total Branch Deductions</div>
            <div class="kpi-value">{fmt_currency(total_deductions)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi4:
    vault_class = "positive" if vault_remaining >= 0 else "negative"
    vault_accent = "#5ee6a4" if vault_remaining >= 0 else "#ff6b81"
    vault_icon = "🛡️" if vault_remaining >= 0 else "🚨"
    st.markdown(
        f"""
        <div class="kpi-card" style="--accent:{vault_accent};">
            <div class="kpi-icon">{vault_icon}</div>
            <div class="kpi-label">Remaining Safe / Vault Budget</div>
            <div class="kpi-value {vault_class}">{fmt_currency(vault_remaining)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# ──────────────────────────────────────────────────────────────────────────
# TABBED SUBSYSTEMS
# ──────────────────────────────────────────────────────────────────────────
tab_a, tab_b, tab_c, tab_d, tab_e = st.tabs(
    [
        "📊 Payroll Statement",
        "🗓️ Attendance & Absence",
        "🛠️ Adjustments & Profiles",
        "🚪 Offboarding (Fire System)",
        "🗄️ Archive & Separation Log",
    ]
)

# ── TAB A: Unified Payroll Statement ───────────────────────────────────────
with tab_a:
    st.markdown(
        "<div class='section-card'><div class='section-heading'>📊 Unified Payroll Statement</div>",
        unsafe_allow_html=True,
    )

    if not scope_employees:
        st.info("No active employees in this scope yet.")
    else:
        rows = []
        for emp in scope_employees.values():
            rows.append(
                {
                    "Employee Code": emp["code"],
                    "Name": emp["name"],
                    "Branch": emp["branch"],
                    "Date of Hiring": emp["hire_date"].strftime("%Y-%m-%d")
                    if isinstance(emp["hire_date"], date)
                    else str(emp["hire_date"]),
                    "Base Salary": convert_for_display(emp["base_salary"]),
                    "Active Bonuses": convert_for_display(emp["bonuses"]),
                    "Active Deductions": convert_for_display(emp["deductions"]),
                    "Net Final Salary": convert_for_display(net_salary(emp)),
                }
            )

        df = pd.DataFrame(rows)
        currency_suffix = "USD" if st.session_state.currency == "USD" else "SAR"

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Base Salary": st.column_config.NumberColumn(
                    f"Base Salary ({currency_suffix})", format="%.2f"
                ),
                "Active Bonuses": st.column_config.NumberColumn(
                    f"Active Bonuses ({currency_suffix})", format="%.2f"
                ),
                "Active Deductions": st.column_config.NumberColumn(
                    f"Active Deductions ({currency_suffix})", format="%.2f"
                ),
                "Net Final Salary": st.column_config.NumberColumn(
                    f"Net Final Salary ({currency_suffix})", format="%.2f"
                ),
            },
        )

        c1, c2, c3 = st.columns(3)
        c1.metric("Headcount", len(scope_employees))
        c2.metric("Avg. Net Salary", fmt_currency(net_payroll / len(scope_employees)))
        c3.metric("Total Net Payroll", fmt_currency(net_payroll))

    st.markdown("</div>", unsafe_allow_html=True)


# ── TAB B: Daily Attendance & Absence Management ───────────────────────────
with tab_b:
    st.markdown(
        "<div class='section-card'><div class='section-heading'>🗓️ Daily Attendance & Absence Management</div>",
        unsafe_allow_html=True,
    )

    attendance_date = st.date_input(
        "Select date for attendance logging", value=date.today(), key="attendance_date"
    )
    iso_day = attendance_date.isoformat()

    if not scope_employees:
        st.info("No active employees in this scope to log attendance for.")
    else:
        st.caption(f"Logging attendance for **{iso_day}** — scope: **{st.session_state.selected_branch}**")
        st.markdown("---")

        header_cols = st.columns([2.4, 2, 1.6, 1.2, 1.2])
        header_cols[0].markdown("**Employee**")
        header_cols[1].markdown("**Branch**")
        header_cols[2].markdown("**Status Today**")
        header_cols[3].markdown("**Present**")
        header_cols[4].markdown("**Absent**")

        for code, emp in scope_employees.items():
            row = st.columns([2.4, 2, 1.6, 1.2, 1.2])
            row[0].write(f"{emp['name']}  \n`{code}`")
            row[1].write(emp["branch"])

            status = st.session_state.attendance.get((code, iso_day))
            if status == "Present":
                row[2].markdown("<span class='badge badge-green'>PRESENT</span>", unsafe_allow_html=True)
            elif status == "Absent":
                row[2].markdown("<span class='badge badge-red'>ABSENT</span>", unsafe_allow_html=True)
            else:
                row[2].markdown("<span class='badge badge-blue'>UNMARKED</span>", unsafe_allow_html=True)

            if row[3].button("Present ✅", key=f"present_{code}_{iso_day}", use_container_width=True):
                # If previously marked absent for this date, refund the penalty
                if st.session_state.attendance.get((code, iso_day)) == "Absent":
                    st.session_state.employees[code]["deductions"] = max(
                        0.0, st.session_state.employees[code]["deductions"] - ABSENCE_PENALTY
                    )
                st.session_state.attendance[(code, iso_day)] = "Present"
                st.rerun()

            if row[4].button("Absent ❌", key=f"absent_{code}_{iso_day}", use_container_width=True):
                if st.session_state.attendance.get((code, iso_day)) != "Absent":
                    st.session_state.employees[code]["deductions"] += ABSENCE_PENALTY
                st.session_state.attendance[(code, iso_day)] = "Absent"
                st.rerun()

        st.markdown("---")
        st.caption(
            f"⚠️ Marking an employee **Absent ❌** automatically applies a "
            f"**{fmt_currency(ABSENCE_PENALTY)}** disciplinary deduction, logged as "
            f"\"Automated absence penalty — unexcused absence on {iso_day}\"."
        )

    st.markdown("</div>", unsafe_allow_html=True)


# ── TAB C: Financial Adjustments & Profile Modifications ───────────────────
with tab_c:
    if not scope_employees:
        st.markdown(
            "<div class='section-card'><div class='section-heading'>🛠️ Financial Adjustments & Profile Modifications</div>",
            unsafe_allow_html=True,
        )
        st.info("No active employees in this scope to modify yet.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        emp_labels = {code: f"{emp['name']} ({code})" for code, emp in scope_employees.items()}

        col_bonus, col_deduct, col_profile = st.columns(3)

        # ── 1. Manual Bonus Distribution ──
        with col_bonus:
            st.markdown(
                "<div class='section-card'><div class='section-heading'>🎁 Manual Bonus</div>",
                unsafe_allow_html=True,
            )
            bonus_emp_code = st.selectbox(
                "Employee", options=list(emp_labels.keys()), format_func=lambda c: emp_labels[c], key="bonus_emp"
            )
            bonus_amount = st.number_input("Bonus Amount (SAR)", min_value=0.0, step=50.0, key="bonus_amt")
            if st.button("Apply Bonus 🎁", use_container_width=True, type="primary", key="apply_bonus"):
                if bonus_amount > 0:
                    st.session_state.employees[bonus_emp_code]["bonuses"] += float(bonus_amount)
                    st.success(f"Bonus of {fmt_currency(bonus_amount)} applied to {emp_labels[bonus_emp_code]}.")
                    st.rerun()
                else:
                    st.warning("Enter a bonus amount greater than zero.")
            st.markdown("</div>", unsafe_allow_html=True)

        # ── 2. Custom Disciplinary Deductions ──
        with col_deduct:
            st.markdown(
                "<div class='section-card'><div class='section-heading'>⚠️ Disciplinary Deduction</div>",
                unsafe_allow_html=True,
            )
            deduct_emp_code = st.selectbox(
                "Employee", options=list(emp_labels.keys()), format_func=lambda c: emp_labels[c], key="deduct_emp"
            )
            deduct_amount = st.number_input("Deduction Amount (SAR)", min_value=0.0, step=50.0, key="deduct_amt")
            deduct_reason = st.text_area("Reason", placeholder="e.g. Late arrival, policy violation...", key="deduct_reason")
            if st.button("Apply Deduction ⚠️", use_container_width=True, type="primary", key="apply_deduction"):
                if deduct_amount <= 0:
                    st.warning("Enter a deduction amount greater than zero.")
                elif not deduct_reason.strip():
                    st.warning("Please document the reason for this deduction.")
                else:
                    st.session_state.employees[deduct_emp_code]["deductions"] += float(deduct_amount)
                    st.success(
                        f"Deduction of {fmt_currency(deduct_amount)} applied to "
                        f"{emp_labels[deduct_emp_code]} — reason: \"{deduct_reason.strip()}\"."
                    )
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        # ── 3. LIVE Profile Editor ──
        with col_profile:
            st.markdown(
                "<div class='section-card'><div class='section-heading'>✏️ Live Profile Editor</div>",
                unsafe_allow_html=True,
            )
            profile_emp_code = st.selectbox(
                "Employee", options=list(emp_labels.keys()), format_func=lambda c: emp_labels[c], key="profile_emp"
            )
            current_emp = st.session_state.employees[profile_emp_code]

            new_base_salary = st.number_input(
                "Base Salary (SAR)",
                min_value=0.0,
                step=50.0,
                value=float(current_emp["base_salary"]),
                key=f"profile_salary_{profile_emp_code}",
            )
            new_hire_date_edit = st.date_input(
                "Date of Hiring",
                value=current_emp["hire_date"],
                key=f"profile_hiredate_{profile_emp_code}",
            )

            if st.button("💾 Save Profile Changes", use_container_width=True, type="primary", key="save_profile"):
                st.session_state.employees[profile_emp_code]["base_salary"] = float(new_base_salary)
                st.session_state.employees[profile_emp_code]["hire_date"] = new_hire_date_edit
                st.success(f"Profile updated for {emp_labels[profile_emp_code]}.")
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)


# ── TAB D: Administrative Offboarding System (Fire System) ─────────────────
with tab_d:
    st.markdown(
        "<div class='section-card'><div class='section-heading'>🚪 Administrative Offboarding System</div>",
        unsafe_allow_html=True,
    )

    if not st.session_state.admin_unlocked:
        st.warning("🔒 Admin access required to terminate employee contracts. Unlock from the sidebar.")
    elif not scope_employees:
        st.info("No active employees in this scope to offboard.")
    else:
        st.caption("This action immediately removes the employee from active payroll and moves them to the corporate archive.")

        emp_labels_fire = {code: f"{emp['name']} ({code}) — {emp['branch']}" for code, emp in scope_employees.items()}
        fire_emp_code = st.selectbox(
            "Select employee to terminate",
            options=list(emp_labels_fire.keys()),
            format_func=lambda c: emp_labels_fire[c],
            key="fire_emp",
        )

        fire_reason = st.text_area(
            "Mandatory lawful termination reason",
            placeholder="e.g. Repeated policy violations, gross misconduct, redundancy, contract non-renewal...",
            key="fire_reason",
        )
        fire_effective_date = st.date_input(
            "Official effective termination date", value=date.today(), key="fire_effective_date"
        )

        st.markdown("")
        confirm_fire = st.checkbox("I confirm this termination has been reviewed and is lawful.", key="confirm_fire")

        if st.button("🔥 Execute Termination", type="primary", use_container_width=True, key="execute_fire"):
            if not fire_reason.strip():
                st.error("A termination reason is mandatory before this action can proceed.")
            elif not confirm_fire:
                st.error("Please confirm the termination before executing.")
            else:
                emp_record = st.session_state.employees.pop(fire_emp_code)
                emp_record["termination_date"] = fire_effective_date
                emp_record["termination_reason"] = fire_reason.strip()
                st.session_state.archive[fire_emp_code] = emp_record
                st.success(f"{emp_record['name']} has been offboarded and moved to the archive.")
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ── TAB E: Historical Archive & Separation Log (with Undo) ─────────────────
with tab_e:
    st.markdown(
        "<div class='section-card'><div class='section-heading'>🗄️ Historical Archive & Separation Log</div>",
        unsafe_allow_html=True,
    )

    if not st.session_state.archive:
        st.info("No terminated employees on record. The archive is empty.")
    else:
        for code, emp in list(st.session_state.archive.items()):
            with st.container():
                st.markdown(
                    f"""
                    <div class="section-card" style="margin-bottom:10px;">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap;">
                            <div>
                                <span style="font-size:16px; font-weight:700; color:#e7eaf3;">{emp['name']}</span>
                                &nbsp; <span class="badge badge-blue">{code}</span>
                                &nbsp; <span class="badge badge-red">TERMINATED</span>
                                <div style="color:#8a93b3; font-size:13px; margin-top:6px;">
                                    Branch: {emp['branch']} &nbsp;|&nbsp;
                                    Hired: {emp['hire_date'].strftime('%Y-%m-%d') if isinstance(emp['hire_date'], date) else emp['hire_date']} &nbsp;|&nbsp;
                                    Departed: {emp['termination_date'].strftime('%Y-%m-%d') if isinstance(emp['termination_date'], date) else emp['termination_date']}
                                </div>
                                <div style="color:#8a93b3; font-size:13px; margin-top:4px;">
                                    Last Base Salary: {fmt_currency(emp['base_salary'])} &nbsp;|&nbsp;
                                    Bonuses: {fmt_currency(emp['bonuses'])} &nbsp;|&nbsp;
                                    Deductions: {fmt_currency(emp['deductions'])}
                                </div>
                                <div style="color:#ff9eac; font-size:13px; margin-top:6px;">
                                    📋 Reason: {emp['termination_reason']}
                                </div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                undo_col, _ = st.columns([1, 5])
                with undo_col:
                    if st.button("🔄 Rehire / Undo", key=f"undo_{code}", use_container_width=True):
                        restored = st.session_state.archive.pop(code)
                        restored.pop("termination_date", None)
                        restored.pop("termination_reason", None)
                        st.session_state.employees[code] = restored
                        st.success(f"{restored['name']} has been restored to active status at {restored['branch']}.")
                        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="restos-footer">
        REST-OS Global SaaS Suite • Perfect ERP Edition • Handcrafted by Nezar Mohammed Hany 👑
    </div>
    """,
    unsafe_allow_html=True,
)

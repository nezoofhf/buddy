"""
REST-OS Global Enterprise
A premium multi-branch restaurant management & financial ERP dashboard.
Built with Streamlit.

v2.0 — Hardened core, role-based access, audit trail, analytics,
branch management, CSV/JSON export-import, attendance analytics.
"""

import streamlit as st
import pandas as pd
import json
import uuid
from datetime import date, datetime, timedelta
from io import BytesIO

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
USD_RATE_DEFAULT = 3.75          # 1 USD = 3.75 SAR
SUPER_ADMIN_PASSWORD = "1234"
MANAGER_PASSWORD = "manager"
ABSENCE_PENALTY_DEFAULT = 100.0  # SAR, flat deduction for an unexcused absence
ALL_BRANCHES_LABEL = "🌍 All Branches (Global Group View)"

BRANCH_SEED = {
    "Buddy's Burger - Riyadh Branch": 60000.0,
    "Buddy's Burger - Jeddah Branch": 45000.0,
}

CURRENCY_SYMBOLS = {"SAR": "SAR", "USD": "$"}


def new_emp_id() -> str:
    return "EMP-" + uuid.uuid4().hex[:6].upper()


def new_log_id() -> str:
    return uuid.uuid4().hex[:8]


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ──────────────────────────────────────────────────────────────────────────
# SESSION STATE INITIALIZATION
# ──────────────────────────────────────────────────────────────────────────
def seed_employees():
    return {
        "EMP-A1B2C3": {
            "code": "EMP-A1B2C3",
            "name": "Omar Al-Fahad",
            "branch": "Buddy's Burger - Riyadh Branch",
            "hire_date": date(2023, 4, 12),
            "base_salary": 6500.0,
            "bonuses": 500.0,
            "deductions": 0.0,
            "salary_history": [
                {"date": date(2023, 4, 12).isoformat(), "salary": 6500.0, "note": "Initial hire"}
            ],
        },
        "EMP-D4E5F6": {
            "code": "EMP-D4E5F6",
            "name": "Sara Al-Mutairi",
            "branch": "Buddy's Burger - Riyadh Branch",
            "hire_date": date(2022, 11, 1),
            "base_salary": 5800.0,
            "bonuses": 0.0,
            "deductions": 100.0,
            "salary_history": [
                {"date": date(2022, 11, 1).isoformat(), "salary": 5800.0, "note": "Initial hire"}
            ],
        },
        "EMP-G7H8I9": {
            "code": "EMP-G7H8I9",
            "name": "Khalid Bin Nasser",
            "branch": "Buddy's Burger - Jeddah Branch",
            "hire_date": date(2024, 1, 20),
            "base_salary": 5200.0,
            "bonuses": 250.0,
            "deductions": 0.0,
            "salary_history": [
                {"date": date(2024, 1, 20).isoformat(), "salary": 5200.0, "note": "Initial hire"}
            ],
        },
    }


def seed_archive():
    return {
        "EMP-X9Y8Z7": {
            "code": "EMP-X9Y8Z7",
            "name": "Fahad Al-Otaibi",
            "branch": "Buddy's Burger - Jeddah Branch",
            "hire_date": date(2021, 6, 5),
            "base_salary": 4800.0,
            "bonuses": 0.0,
            "deductions": 0.0,
            "salary_history": [
                {"date": date(2021, 6, 5).isoformat(), "salary": 4800.0, "note": "Initial hire"}
            ],
            "termination_date": date(2025, 9, 30),
            "termination_reason": "Voluntary resignation - relocation",
        }
    }


def init_state():
    if "initialized" in st.session_state:
        return

    st.session_state.initialized = True
    st.session_state.currency = "SAR"
    st.session_state.usd_rate = USD_RATE_DEFAULT
    st.session_state.absence_penalty = ABSENCE_PENALTY_DEFAULT

    # auth: None = locked, "manager" = branch manager, "super" = super admin
    st.session_state.role = None
    st.session_state.selected_branch = ALL_BRANCHES_LABEL

    st.session_state.branches = dict(BRANCH_SEED)
    st.session_state.employees = seed_employees()
    st.session_state.archive = seed_archive()

    # attendance log: {(employee_code, iso_date): "Present"/"Absent"}
    st.session_state.attendance = {}

    # audit trail: list of dicts, newest first
    st.session_state.audit_log = []

    log_action("SYSTEM", "Application initialized with seed data.", "system")


# ──────────────────────────────────────────────────────────────────────────
# AUDIT LOG
# ──────────────────────────────────────────────────────────────────────────
def log_action(category: str, message: str, actor: str = None):
    """Append an entry to the audit trail. Newest entries first."""
    actor = actor or (st.session_state.get("role") or "guest")
    st.session_state.setdefault("audit_log", [])
    st.session_state.audit_log.insert(
        0,
        {
            "id": new_log_id(),
            "timestamp": now_str(),
            "category": category,
            "actor": actor,
            "message": message,
        },
    )
    # cap log size to keep things snappy
    if len(st.session_state.audit_log) > 500:
        st.session_state.audit_log = st.session_state.audit_log[:500]


init_state()


# ──────────────────────────────────────────────────────────────────────────
# CURRENCY HELPERS
# ──────────────────────────────────────────────────────────────────────────
def fmt_currency(amount_sar: float) -> str:
    """Format a SAR-denominated amount according to the global currency toggle."""
    rate = st.session_state.usd_rate
    if st.session_state.currency == "USD":
        return f"$ {amount_sar / rate:,.2f}"
    return f"SAR {amount_sar:,.2f}"


def convert_for_display(amount_sar: float) -> float:
    if st.session_state.currency == "USD":
        return amount_sar / st.session_state.usd_rate
    return amount_sar


def currency_label() -> str:
    return "USD" if st.session_state.currency == "USD" else "SAR"


def to_sar(amount_in_display_currency: float) -> float:
    """Convert a value the admin typed (in the currently displayed currency) back to SAR for storage."""
    if st.session_state.currency == "USD":
        return amount_in_display_currency * st.session_state.usd_rate
    return amount_in_display_currency


# ──────────────────────────────────────────────────────────────────────────
# CORE BUSINESS LOGIC HELPERS
# ──────────────────────────────────────────────────────────────────────────
def employees_in_scope(branch: str = None) -> dict:
    """Active employees filtered by the selected (or given) branch scope."""
    branch = branch if branch is not None else st.session_state.selected_branch
    if branch == ALL_BRANCHES_LABEL:
        return st.session_state.employees
    return {
        code: emp
        for code, emp in st.session_state.employees.items()
        if emp["branch"] == branch
    }


def net_salary(emp: dict) -> float:
    return emp["base_salary"] + emp["bonuses"] - emp["deductions"]


def budget_in_scope(branch: str = None) -> float:
    branch = branch if branch is not None else st.session_state.selected_branch
    if branch == ALL_BRANCHES_LABEL:
        return sum(st.session_state.branches.values())
    return st.session_state.branches.get(branch, 0.0)


def can_manage_branch(branch_name: str) -> bool:
    """Super admins manage everything. Managers are scoped to their assigned branch only."""
    role = st.session_state.role
    if role == "super":
        return True
    if role == "manager":
        return st.session_state.get("manager_branch") == branch_name
    return False


def is_unlocked() -> bool:
    return st.session_state.role is not None


def role_display() -> str:
    if st.session_state.role == "super":
        return "Super Admin"
    if st.session_state.role == "manager":
        return f"Branch Manager — {st.session_state.get('manager_branch', '')}"
    return "Guest (Read-Only)"


def serialize_state() -> dict:
    """Produce a JSON-safe snapshot of all mutable business data."""
    def emp_to_json(emp):
        e = dict(emp)
        e["hire_date"] = e["hire_date"].isoformat() if isinstance(e["hire_date"], date) else e["hire_date"]
        if "termination_date" in e and isinstance(e["termination_date"], date):
            e["termination_date"] = e["termination_date"].isoformat()
        return e

    return {
        "branches": st.session_state.branches,
        "employees": {k: emp_to_json(v) for k, v in st.session_state.employees.items()},
        "archive": {k: emp_to_json(v) for k, v in st.session_state.archive.items()},
        "attendance": {f"{k[0]}|{k[1]}": v for k, v in st.session_state.attendance.items()},
        "usd_rate": st.session_state.usd_rate,
        "absence_penalty": st.session_state.absence_penalty,
        "exported_at": now_str(),
    }


def deserialize_state(payload: dict):
    """Restore business data from a JSON snapshot produced by serialize_state()."""
    def emp_from_json(emp):
        e = dict(emp)
        if isinstance(e.get("hire_date"), str):
            e["hire_date"] = date.fromisoformat(e["hire_date"])
        if isinstance(e.get("termination_date"), str):
            e["termination_date"] = date.fromisoformat(e["termination_date"])
        e.setdefault("salary_history", [])
        return e

    st.session_state.branches = {k: float(v) for k, v in payload.get("branches", {}).items()}
    st.session_state.employees = {k: emp_from_json(v) for k, v in payload.get("employees", {}).items()}
    st.session_state.archive = {k: emp_from_json(v) for k, v in payload.get("archive", {}).items()}
    st.session_state.attendance = {
        tuple(k.split("|", 1)): v for k, v in payload.get("attendance", {}).items()
    }
    st.session_state.usd_rate = float(payload.get("usd_rate", USD_RATE_DEFAULT))
    st.session_state.absence_penalty = float(payload.get("absence_penalty", ABSENCE_PENALTY_DEFAULT))


def payroll_dataframe(scope_employees: dict) -> pd.DataFrame:
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
                f"Base Salary ({currency_label()})": round(convert_for_display(emp["base_salary"]), 2),
                f"Active Bonuses ({currency_label()})": round(convert_for_display(emp["bonuses"]), 2),
                f"Active Deductions ({currency_label()})": round(convert_for_display(emp["deductions"]), 2),
                f"Net Final Salary ({currency_label()})": round(convert_for_display(net_salary(emp)), 2),
            }
        )
    return pd.DataFrame(rows)

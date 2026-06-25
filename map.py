import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Buddy's Burger Enterprise Panel", page_icon="🍔", layout="wide")

# 2. Advanced Premium CSS (Dark/Light Fusion to match Buddy's Red theme)
st.markdown("""
<style>
    .stApp { background-color: #FAFAFB; font-family: 'Segoe UI', sans-serif; }
    .metric-card {
        background: white; padding: 22px; border-radius: 14px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04); text-align: center;
        border-left: 5px solid #E50914; transition: 0.3s;
    }
    .metric-card:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(229,9,20,0.1); }
    .metric-title { font-size: 13px; color: #718096; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { font-size: 28px; color: #1A202C; font-weight: bold; margin-top: 5px; }
    .sidebar-calc { background: #1A202C; padding: 15px; border-radius: 10px; color: white; }
    
    /* Custom Styling for Action Buttons */
    div.stButton > button {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: Multi-Location & Toggle Calculator ---
st.sidebar.image("https://buddysburger.com/wp-content/uploads/2020/06b/buddys-logo.png", width=150)
st.sidebar.title("🏬 Enterprise Navigation")

selected_loc = st.sidebar.selectbox(
    "Select Location Hub:",
    ["Austin (Cameron Rd)", "San Marcos (TX-80)", "Round Rock (Old Settlers)"]
)

st.sidebar.write("⏱️ **Operating Hours:** 11:00 AM - 11:00 PM (Daily)")
st.sidebar.write("---")

# 🧮 Interactive Sidebar Calculator
show_calc = st.sidebar.checkbox("🧮 Open Quick Calculator", value=False)
if show_calc:
    st.sidebar.markdown('<div class="sidebar-calc">', unsafe_allow_html=True)
    st.sidebar.subheader("Quick Math")
    num1 = st.sidebar.number_input("Value A", value=0.0)
    num2 = st.sidebar.number_input("Value B", value=0.0)
    op = st.sidebar.selectbox("Operation", ["+", "-", "*", "/"])
    
    if op == "+": res = num1 + num2
    elif op == "-": res = num1 - num2
    elif op == "*": res = num1 * num2
    elif op == "/": res = num1 / num2 if num2 != 0 else "Error"
    
    st.sidebar.info(f"Result = {res}")
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

# --- MAIN DASHBOARD INTERFACE ---
st.title("🍔 Buddy's Burger — Advanced Management Hub")
st.subheader(f"Live Analytics & Back-Office Control Portal — {selected_loc}")
st.write("---")

# Initialize Master Data in Session State (Lists of dicts for easy row-by-row manipulation)
if 'employees_list' not in st.session_state:
    st.session_state.employees_list = [
        {"id": 1, "Staff Name": "Carlos Mendoza", "Role": "Kitchen Lead", "Base Salary ($)": 3800.0, "Deductions ($)": 0.0},
        {"id": 2, "Staff Name": "Ashley Taylor", "Role": "Store Manager", "Base Salary ($)": 4500.0, "Deductions ($)": 0.0},
        {"id": 3, "Staff Name": "Lamar Jackson", "Role": "Cashier", "Base Salary ($)": 2400.0, "Deductions ($)": 0.0}
    ]
    st.session_state.next_id = 4

if 'sales_revenue' not in st.session_state:
    st.session_state.sales_revenue = 28450.0

# Dynamic Calculations based on Current State
df_staff = pd.DataFrame(st.session_state.employees_list)
if not df_staff.empty:
    df_staff["Net Payout ($)"] = df_staff["Base Salary ($)"] - df_staff["Deductions ($)"]
    total_payroll = df_staff["Net Payout ($)"].sum()
else:
    total_payroll = 0.0

net_profit = st.session_state.sales_revenue - total_payroll

# Top Level KPI Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="metric-card"><div class="metric-title">📈 Gross Sales ({selected_loc})</div><div class="metric-value">${st.session_state.sales_revenue:,.2f}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div class="metric-title">💸 Adjusted Staff Payroll</div><div class="metric-value">${total_payroll:,.2f}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><div class="metric-title">💰 Net Operating Profit</div><div class="metric-value" style="color: #2ECC71;">${net_profit:,.2f}</div></div>', unsafe_allow_html=True)

st.write("##")

# --- SECTION 1: BEST SELLERS LIVE CHART ---
st.header("📊 Menu Performance & Best Sellers")
c1, c2 = st.columns([1, 2])

with c1:
    st.write("### 🥇 Top 5 Items Sold This Month")
    best_sellers = pd.DataFrame({
        "Menu Item": ["Double Classic", "Seasoned Fries", "Double Spicy", "Oreo Shake", "Mango Lemonade"],
        "Orders Provided": [1420, 1150, 980, 640, 420]
    })
    st.dataframe(best_sellers, use_container_width=True)

with c2:
    fig = px.bar(best_sellers, x="Menu Item", y="Orders Provided", 
                 title="Live Sales Volume (Items)", color="Orders Provided",
                 color_continuous_scale=["#FFB3B3", "#E50914"])
    fig.update_layout(showlegend=False, height=300, margin=dict(t=30, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)

st.write("---")

# --- SECTION 2: STAFF CONTROL, ONBOARDING & ADVANCED TERMINATION SYSTEM ---
st.header("👥 HR Center & Active Staff Control Panel")

tab_view, tab_add, tab_penalty = st.tabs([
    "📋 Active Roster & Quick Actions", 
    "➕ Onboard New Employee", 
    "⚡ Apply Staff Deduction"
])

with tab_view:
    st.write("### Current Staff Roster")
    if not df_staff.empty:
        # بنعرض جدول تفاعلي حقيقي سطر بسطر مع زرار الحذف الخاص بكل موظف
        for index, row in df_staff.iterrows():
            emp_col1, emp_col2, emp_col3, emp_col4, emp_col5 = st.columns([2, 1.5, 1.5, 1.5, 1.5])
            with emp_col1:
                st.text(f"👤 Name: {row['Staff Name']}")
            with emp_col2:
                st.text(f"💼 Role: {row['Role']}")
            with emp_col3:
                st.text(f"💵 Salary: ${row['Base Salary ($)']}")
            with emp_col4:
                st.text(f"📉 Penalty: ${row['Deductions ($)']}")
            with emp_col5:
                # حركة الـ OMG هنا: زرار الحذف الفوري ديناميكي
                if st.button(f"🔥 Fire / Terminate", key=f"fire_{row['id']}"):
                    # حذف الموظف من الـ Session State
                    st.session_state.employees_list = [e for e in st.session_state.employees_list if e['id'] != row['id']]
                    st.warning(f"ACTION SENT: {row['Staff Name']} has been terminated from this branch.")
                    st.rerun()
            st.markdown("<hr style='margin: 5px 0; opacity: 0.3;'>", unsafe_allow_html=True)
    else:
        st.info("No active staff registered for this branch.")

with tab_add:
    st.write("### Onboard a New Team Member")
    with st.form("onboard_form", clear_on_submit=True):
        new_name = st.text_input("Employee Full Name")
        new_role = st.selectbox("Job Position", ["Manager", "Kitchen Lead", "Line Cook", "Cashier", "Drive-Thru Operator"])
        new_salary = st.number_input("Monthly Base Salary ($)", min_value=500.0, max_value=15000.0, step=100.0, value=2500.0)
        submit_onboard = st.form_submit_button("Complete Onboarding Process")
        
        if submit_onboard and new_name:
            # إضافة الموظف الجديد للـ Database لايف مع الـ ID الفريد بتاعه
            new_emp_dict = {
                "id": st.session_state.next_id,
                "Staff Name": new_name,
                "Role": new_role,
                "Base Salary ($)": new_salary,
                "Deductions ($)": 0.0
            }
            st.session_state.employees_list.append(new_emp_dict)
            st.session_state.next_id += 1
            st.success(f"OMG Success! {new_name} is now officially registered in {selected_loc} payroll database.")
            st.rerun()

with tab_penalty:
    st.write("### Issue Financial Deduction")
    if not df_staff.empty:
        with st.form("deduction_form", clear_on_submit=True):
            target_employee = st.selectbox("Select Employee:", df_staff["Staff Name"].tolist())
            deduct_amount = st.number_input("Deduction Amount ($)", min_value=0.0, max_value=1000.0, step=10.0)
            reason = st.text_input("Reason for Penalty")
            
            submit_penalty = st.form_submit_button("Confirm & Apply Penalty")
            if submit_penalty and deduct_amount > 0:
                for emp in st.session_state.employees_list:
                    if emp["Staff Name"] == target_employee:
                        emp["Deductions ($)"] += deduct_amount
                st.success(f"Applied a penalty of ${deduct_amount} to {target_employee}.")
                st.rerun()
    else:
        st.info("No staff available to penalize.")

st.write("---")
# --- SECTION 3: SIMULATE LIVE ORDERS ---
st.header("🚀 Integration Test Center")
st.write("Simulate a bulk live order placed through the Lovable Frontend:")
if st.button("Simulate $850.00 Catering Order Receipt"):
    st.session_state.sales_revenue += 850.0
    st.success("Incoming API Data Hook: Added $850.00 to Gross Sales!")
    st.rerun()
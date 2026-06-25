import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Architectural Configurations
st.set_page_config(page_title="Buddy's Burger Enterprise Backbone", page_icon="🍔", layout="wide")

# 2. High-Fidelity Custom CSS (Dark Mode Admin Theme)
st.markdown("""
<style>
    .stApp { background-color: #0B0C10; font-family: -apple-system, sans-serif; color: #ECF0F1; }
    .kpi-card {
        background: #1F2833; padding: 25px; border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2); text-align: center;
        border-top: 4px solid #E50914; transition: all 0.3s ease;
    }
    .kpi-card:hover { transform: translateY(-4px); box-shadow: 0 15px 35px rgba(229,9,20,0.15); }
    .kpi-title { font-size: 12px; color: #C5A059; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; }
    .kpi-value { font-size: 32px; color: #FFFFFF; font-weight: 800; margin-top: 8px; }
    .sidebar-calc { background: #151B24; padding: 20px; border-radius: 12px; border: 1px solid #232D3F; margin-top: 15px; }
</style>
""", unsafe_allow_html=True)

# 3. Master Global Core Initialization (Database Simulation)
if 'db_staff' not in st.session_state:
    st.session_state.db_staff = [
        {"id": 101, "Staff Name": "Carlos Mendoza", "Role": "Kitchen Lead", "Base Salary ($)": 4100.0, "Deductions ($)": 0.0, "Hub": "Austin Main"},
        {"id": 102, "Staff Name": "Ashley Taylor", "Role": "Store Manager", "Base Salary ($)": 4900.0, "Deductions ($)": 0.0, "Hub": "Austin Main"},
        {"id": 103, "Staff Name": "Lamar Jackson", "Role": "Cashier Specialist", "Base Salary ($)": 2600.0, "Deductions ($)": 0.0, "Hub": "San Marcos"},
        {"id": 104, "Staff Name": "Sarah Jenkins", "Role": "Shift Supervisor", "Base Salary ($)": 3500.0, "Deductions ($)": 0.0, "Hub": "Round Rock"}
    ]
    st.session_state.id_counter = 105

if 'gross_revenue' not in st.session_state:
    st.session_state.gross_revenue = 64250.0

# --- SIDEBAR CONTROL UNIT & SECURITY INFRASTRUCTURE ---
st.sidebar.markdown("<h2 style='text-align: center; color: #E50914;'>BUDDY'S HQ</h2>", unsafe_allow_html=True)
st.sidebar.write("---")

# Gateway Authorization Check
staff_key = st.sidebar.text_input("🔒 Enterprise Access Token", type="password", help="Input credentials to unlock transactional channels.")
if staff_key != "buddys2026":
    st.sidebar.warning("Awaiting secure authorization signature...")
    st.title("🔒 Restricted Infrastructure Node")
    st.info("Please supply the required Access Token in the secure sidebar portal to interface with the active datastreams.")
    st.stop()

st.sidebar.success("Authorization Signature Verified.")
selected_hub = st.sidebar.selectbox("🎯 Interfaced Fulfillment Hub:", ["All Corporate Network", "Austin Main", "San Marcos", "Round Rock"])

# 🧮 Embedded Floating Mathematical Unit
st.sidebar.write("---")
with st.sidebar.expander("🧮 Compute Engine / Quick Calculator", expanded=False):
    st.markdown('<div class="sidebar-calc">', unsafe_allow_html=True)
    val_a = st.number_input("Operand A", value=0.0, step=1.0)
    val_b = st.number_input("Operand B", value=0.0, step=1.0)
    operation = st.selectbox("Execution Pattern", ["Addition (+)", "Subtraction (-)", "Multiplication (*)", "Division (/)"])
    if operation == "Addition (+)": out = val_a + val_b
    elif operation == "Subtraction (-)": out = val_a - val_b
    elif operation == "Multiplication (*)": out = val_a * val_b
    elif operation == "Division (/)": out = val_a / val_b if val_b != 0 else "Math Error"
    st.info(f"Computed Output: {out}")
    st.markdown('</div>', unsafe_allow_html=True)

# Data Processing Engine (Filtering Layer)
master_df = pd.DataFrame(st.session_state.db_staff)
if selected_hub != "All Corporate Network":
    filtered_df = master_df[master_df["Hub"] == selected_hub]
else:
    filtered_df = master_df

# Financial Calculations Pipeline
if not filtered_df.empty:
    filtered_df["Net Payout ($)"] = filtered_df["Base Salary ($)"] - filtered_df["Deductions ($)"]
    allocated_payroll = filtered_df["Net Payout ($)"].sum()
else:
    allocated_payroll = 0.0

current_revenue = st.session_state.gross_revenue if selected_hub == "All Corporate Network" else st.session_state.gross_revenue * 0.45
net_margin = current_revenue - allocated_payroll

# --- MAIN EXECUTIVE DASHBOARD VIEW ---
st.title("🍔 Buddy's Burger — Multi-Hub Corporate Framework")
st.write(f"**Active Node:** Node-Interfaced // {selected_hub} Database Stream")
st.write("---")

# Top Level Operational Analytics Cards
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
with kpi_col1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">📈 Audited Gross Revenue</div><div class="kpi-value">${current_revenue:,.2f}</div></div>', unsafe_allow_html=True)
with kpi_col2:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">💸 Net Disbursed Payroll</div><div class="kpi-value">${allocated_payroll:,.2f}</div></div>', unsafe_allow_html=True)
with kpi_col3:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">💰 Net Operating Capital</div><div class="kpi-value" style="color: #2ECC71;">${net_margin:,.2f}</div></div>', unsafe_allow_html=True)

st.write("##")

# --- DATA VISUALIZATION BLOCK ---
st.header("📊 Analytical Performance Vectors")
chart_col1, chart_col2 = st.columns([1, 2])

with chart_col1:
    st.write("### Product Velocity Chart")
    analytics_mix = pd.DataFrame({
        "Menu Variant": ["Double Spicy Burger", "14-Spice Fries", "Artisanal Oreo Shake", "Double Classic"],
        "Units Smashed": [2450, 3100, 1890, 1540]
    })
    st.dataframe(analytics_mix, use_container_width=True)

with chart_col2:
    fig = px.bar(analytics_mix, x="Menu Variant", y="Units Smashed", color="Units Smashed",
                 title="Product Velocity Framework (Monthly Volume Trend)",
                 color_continuous_scale=["#FF8080", "#E50914"])
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#fff", height=320)
    st.plotly_chart(fig, use_container_width=True)

st.write("---")

# --- HUMAN CAPITAL INTERACTION MATRIX ---
st.header("👥 Advanced Resource Orchestration & Payroll Matrix")

tab_roster, tab_onboard, tab_deduction = st.tabs([
    "📋 Active Personnel Matrix", 
    "➕ Provision New Personnel", 
    "⚡ Execute Performance Deductions"
])

with tab_roster:
    st.write("### Live Node Personnel Database")
    if not filtered_df.empty:
        for idx, row in filtered_df.iterrows():
            r_col1, r_col2, r_col3, r_col4, r_col5 = st.columns([2, 1.5, 1.5, 1.5, 1.5])
            with r_col1: st.markdown(f"**👤 Name:** {row['Staff Name']}")
            with r_col2: st.markdown(f"**💼 Rank:** {row['Role']}")
            with r_col3: st.markdown(f"**💵 Base:** ${row['Base Salary ($)']}")
            with r_col4: st.markdown(f"**📉 Reductions:** `${row['Deductions ($)']}`")
            with r_col5:
                if st.button("🔥 Terminate Employment", key=f"term_{row['id']}", help="De-provision staff from active cluster node."):
                    st.session_state.db_staff = [emp for emp in st.session_state.db_staff if emp['id'] != row['id']]
                    st.error(f"SYSTEM PROTOCOL ACTION: {row['Staff Name']} has been scrubbed from system registry.")
                    st.rerun()
            st.markdown("<hr style='margin: 6px 0; opacity: 0.1;'>", unsafe_allow_html=True)
    else:
        st.info("No personnel currently provisioned to this operational node.")

with tab_onboard:
    st.write("### Provision New Resource Record")
    with st.form("onboard_form_premium", clear_on_submit=True):
        f_name = st.text_input("Legal Full Name")
        f_role = st.selectbox("Designated Operational Rank", ["Store Manager", "Kitchen Lead", "Line Operator", "Cashier Specialist"])
        f_hub = st.selectbox("Target Assignment Hub", ["Austin Main", "San Marcos", "Round Rock"])
        f_salary = st.number_input("Contractual Base Monthly Salary ($)", min_value=1000.0, max_value=20000.0, step=100.0, value=3000.0)
        
        if st.form_submit_button("Authorize Allocation"):
            if f_name:
                st.session_state.db_staff.append({
                    "id": st.session_state.id_counter, "Staff Name": f_name, "Role": f_role,
                    "Base Salary ($)": f_salary, "Deductions ($)": 0.0, "Hub": f_hub
                })
                st.session_state.id_counter += 1
                st.success(f"Resource Record Allocated: {f_name} routed to {f_hub} roster.")
                st.rerun()

with tab_deduction:
    st.write("### Apply Financial Performance Sanction")
    if not filtered_df.empty:
        with st.form("penalty_form_premium", clear_on_submit=True):
            f_target = st.selectbox("Target Employee System Alias:", filtered_df["Staff Name"].tolist())
            f_deduct = st.number_input("Sanction Metric Value ($)", min_value=0.0, max_value=2500.0, step=25.0)
            f_reason = st.text_input("Operational Deviation Log Entry / Reason")
            
            if st.form_submit_button("Enforce Financial Penalty"):
                if f_deduct > 0:
                    for emp in st.session_state.employees_list if 'employees_list' in st.session_state else st.session_state.db_staff:
                        if emp["Staff Name"] == f_target:
                            emp["Deductions ($)"] += f_deduct
                    st.success(f"Sanction Enforced: ${f_deduct} subtracted from {f_target}'s current payout trajectory.")
                    st.rerun()
    else:
        st.info("No personnel objects mapped to this cluster node.")

# --- TRANSACTION TESTING UNIT ---
st.write("---")
st.header("⚙️ Network API Hub Simulation")
if st.button("Trigger Inbound Digital Payload Receipt (Simulate Wholesale Catering Order +$1,500.00)"):
    st.session_state.gross_revenue += 1500.0
    st.success("Network Hook Execution: Interfaced payload added to pipeline.")
    st.rerun()

import streamlit as st
import pandas as pd
import datetime

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="REST-OS Global SaaS v6.0",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. الـ HTML & CSS الـ Premium
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
    
    * { font-family: 'Cairo', 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #0b0f19; }

    /* الهيدر الرئيسي */
    .hero-container {
        background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid #312e81;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        margin-bottom: 25px;
        text-align: right;
        direction: rtl;
    }
    .hero-title {
        color: #ffffff; font-size: 2.3rem; font-weight: 900; margin-bottom: 10px;
        background: linear-gradient(90deg, #6366f1, #a855f7);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .hero-subtitle { color: #94a3b8; font-size: 1rem; }

    /* كروت الإحصائيات */
    .cards-grid {
        display: flex; flex-wrap: wrap; gap: 15px; justify-content: space-between;
        direction: rtl; margin-bottom: 25px;
    }
    .metric-card {
        background: #111827; border: 1px solid #1f2937; border-radius: 16px; padding: 20px;
        flex: 1 1 calc(25% - 15px); min-width: 250px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .card-header-flex { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
    .card-icon { font-size: 1.5rem; background: #1e1b4b; padding: 8px; border-radius: 12px; color: #818cf8; }
    .card-title { color: #94a3b8; font-size: 0.9rem; font-weight: 600; }
    .card-value { color: #ffffff; font-size: 1.6rem; font-weight: 700; }

    [data-testid="stSidebar"] { background-color: #0f172a; border-left: 1px solid #1f2937; }
    @media (max-width: 768px) { .metric-card { flex: 1 1 100%; } .hero-title { font-size: 1.6rem; } }
    </style>
""", unsafe_allow_html=True)

# 3. إدارة بيانات الفروع المتعددة (Multi-Tenant Session State)
if 'branches_data' not in st.session_state:
    st.session_state.branches_data = {
        "Buddy's Burger (فرع الرياض)": {
            "budget": 60000,
            "employees": {
                "EMP-R01": {"الاسم": "الشيف أحمد علي", "الراتب": 12000, "البونص": 0, "الخصومات": 0, "سبب_الخصم": "لا يوجد", "تاريخ_التعيين": "2024-01-15"},
                "EMP-R02": {"الاسم": "مدير الصالة خالد", "الراتب": 8500, "البونص": 0, "الخصومات": 0, "سبب_الخصم": "لا يوجد", "تاريخ_التعيين": "2025-03-01"}
            },
            "fired": []
        },
        "Buddy's Burger (فرع جدة)": {
            "budget": 45000,
            "employees": {
                "EMP-J01": {"الاسم": "كابتن سلطان حمبيه", "الراتب": 4500, "البونص": 0, "الخصومات": 0, "سبب_الخصم": "لا يوجد", "تاريخ_التعيين": "2025-06-10"},
                "EMP-J02": {"الاسم": "صانع البرجر صابر", "الراتب": 4000, "البونص": 0, "الخصومات": 0, "سبب_الخصم": "لا يوجد", "تاريخ_التعيين": "2025-08-20"}
            },
            "fired": []
        }
    }

if 'daily_attendance' not in st.session_state:
    st.session_state.daily_attendance = {}

# 4. السايدبار: اختيار فرع مخصص أو إدارة المجموعة كاملة
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white;'>🏢 لوحة تحكم الفروع</h2>", unsafe_allow_html=True)
    
    # ميزة اختيار إدارة كل الفروع معاً أو فرع مخصص
    branch_options = ["🌍 إدارة المجموعة كاملة (All Branches)"] + list(st.session_state.branches_data.keys())
    selected_branch = st.selectbox("🏬 اختر نطاق الإدارة:", branch_options)
    
    password_input = st.text_input("🔑 رمز الأمان الموحد:", type="password")
    
    st.markdown("---")
    
    if password_input == "1234":
        st.success("🔓 صلاحيات الإدارة نشطة")
        
        # لو اختار فرع مخصص، يظهر له خيار إضافة وفصل الموظفين للفرع ده
        if selected_branch != "🌍 إدارة المجموعة كاملة (All Branches)":
            st.markdown(f"<h3 style='color: white; text-align: right;'>➕ تعيين بالفرع</h3>", unsafe_allow_html=True)
            new_name = st.text_input("اسم الموظف الجديد:")
            new_salary = st.number_input("الراتب الأساسي:", min_value=1000, max_value=50000, value=4000, step=500)
            hire_date = st.date_input("📆 تاريخ دخول العمل:", datetime.date.today())
            
            if st.button("➕ إتمام التعيين"):
                if new_name:
                    b_data = st.session_state.branches_data[selected_branch]
                    new_code = f"EMP-N{len(b_data['employees']) + len(b_data['fired']) + 1}"
                    b_data['employees'][new_code] = {
                        "الاسم": new_name, "الراتب": new_salary, "البونص": 0, "الخصومات": 0,
                        "سبب_الخصم": "لا يوجد", "تاريخ_التعيين": hire_date.strftime("%Y-%m-%d")
                    }
                    st.toast(f"🎉 تم تسجيل {new_name} في {selected_branch}!")
                    st.rerun()
            
            st.markdown("---")
            st.markdown("<h3 style='color: white; text-align: right;'>🚨 إنهاء خدمات بالفرع</h3>", unsafe_allow_html=True)
            active_emps = st.session_state.branches_data[selected_branch]['employees']
            if active_emps:
                emp_to_fire_code = st.selectbox("🔥 اختر موظف لفصله:", list(active_emps.keys()), format_func=lambda x: active_emps[x]["الاسم"])
                fire_reason = st.text_input("📝 سبب إنهاء الخدمات:")
                if st.button("🚨 شطب وترحيل للأرشيف"):
                    if fire_reason:
                        emp_info = active_emps[emp_to_fire_code]
                        st.session_state.branches_data[selected_branch]['fired'].append({
                            "كود الموظف": emp_to_fire_code, "الاسم": emp_info["الاسم"],
                            "تاريخ التعيين": emp_info["تاريخ_التعيين"], "سبب إنهاء الخدمات ⚠️": fire_reason
                        })
                        del active_emps[emp_to_fire_code]
                        st.toast("⚠️ تم شطب الموظف بنجاح.")
                        st.rerun()
    else:
        st.error("🔒 يرجى إدخال رمز الأمان (1234) لعرض البيانات الحسابية.")
        st.stop()

# ----------------- الحسابات والـ Logic الذكي للفروع -----------------
total_budget = 0
total_salaries = 0
total_bonus = 0
total_deductions = 0
display_employees = {}
display_fired = []

if selected_branch == "🌍 إدارة المجموعة كاملة (All Branches)":
    # تجميع حسابات وموظفي كل الفروع لايف
    for b_name, b_info in st.session_state.branches_data.items():
        total_budget += b_info["budget"]
        for e_code, e_info in b_info["employees"].items():
            total_salaries += e_info["الراتب"]
            total_bonus += e_info["البونص"]
            total_deductions += e_info["الخصومات"]
            # إضافة اسم الفرع جنب الموظف في العرض الشامل
            info_copy = e_info.copy()
            info_copy["الفرع"] = b_name
            display_employees[e_code] = info_copy
        for f_emp in b_info["fired"]:
            f_copy = f_emp.copy()
            f_copy["الفرع"] = b_name
            display_fired.append(f_copy)
else:
    # حسابات فرع واحد مخصص
    b_info = st.session_state.branches_data[selected_branch]
    total_budget = b_info["budget"]
    for e_code, e_info in b_info["employees"].items():
        total_salaries += e_info["الراتب"]
        total_bonus += e_info["البونص"]
        total_deductions += e_info["الخصومات"]
        info_copy = e_info.copy()
        info_copy["الفرع"] = selected_branch
        display_employees[e_code] = info_copy
    display_fired = b_info["fired"]

grand_total_payroll = total_salaries + total_bonus - total_deductions
remaining_budget = total_budget - grand_total_payroll

# 5. الهيدر الرئيسي الديناميكي
st.markdown(f"""
    <div class="hero-container">
        <div style="background-color: #4338ca; color: #e0e7ff; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 700; display: inline-block; margin-bottom: 15px;">
            🛡️ النطاق الحالي: {selected_branch}
        </div>
        <div class="hero-title">REST-OS Enterprise: Multi-Branch Suite</div>
        <div class="hero-subtitle">النظام الشامل المطور بالكامل لعام 2026 لإدارة وتجميع حسابات فروع المطاعم والمجموعات التجارية</div>
    </div>
""", unsafe_allow_html=True)

# 6. كروت الإحصائيات (Metrics) تظهر مجمعة أو منفصلة تلقائياً!
st.markdown(f"""
    <div class="cards-grid">
        <div class="metric-card">
            <div class="card-header-flex"><span class="card-icon">📊</span><span class="card-title">إجمالي الميزانية المراقبة</span></div>
            <div class="card-value">SAR {total_budget:,}</div>
        </div>
        <div class="metric-card">
            <div class="card-header-flex"><span class="card-icon">💵</span><span class="card-title">صافي الـ Payroll الحالي</span></div>
            <div class="card-value" style="color: #6366f1;">SAR {grand_total_payroll:,}</div>
        </div>
        <div class="metric-card">
            <div class="card-header-flex"><span class="card-icon">❌</span><span class="card-title">إجمالي خصومات النطاق</span></div>
            <div class="card-value" style="color: #f43f5e;">SAR {total_deductions:,}</div>
        </div>
        <div class="metric-card">
            <div class="card-header-flex"><span class="card-icon">💰</span><span class="card-title">الخزنة المتبقية</span></div>
            <div class="card-value" style="color: {'#10b981' if remaining_budget >= 0 else '#f43f5e'};">SAR {remaining_budget:,}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# 7. السيكشنز والـ Tabs
tab_payroll, tab_attendance, tab_adjustments, tab_archive = st.tabs([
    "💵 كشف الرواتب العام", "📝 حضور وغياب النطاق", "🛠️ التعديلات المالية", "📜 أرشيف المشيو"
])

# --- الـ Payroll ---
with tab_payroll:
    st.markdown("<h3 style='text-align: right; color: white;'>🏪 كشف الرواتب للموظفين النشطين</h3>", unsafe_allow_html=True)
    payroll_table_data = []
    for emp_code, emp_info in display_employees.items():
        net = emp_info["الراتب"] + emp_info["البونص"] - emp_info["الخصومات"]
        payroll_table_data.append({
            "كود الموظف": emp_code,
            "الاسم": emp_info["الاسم"],
            "الفرع 🏬": emp_info["الفرع"],
            "تاريخ التعيين": emp_info["تاريخ_التعيين"],
            "الراتب الأساسي": f"SAR {emp_info['الراتب']:,}",
            "البونص 🎁": f"SAR {emp_info['البونص']:,}",
            "الخصومات ❌": f"SAR {emp_info['الخصومات']:,}",
            "صافي الراتب": f"SAR {net:,}"
        })
    if payroll_table_data:
        st.dataframe(pd.DataFrame(payroll_table_data).set_index("كود الموظف"), use_container_width=True)
    else:
        st.info("لا توجد عمالة نشطة في هذا النطاق.")

# --- الحضور والغياب اليومي ---
with tab_attendance:
    st.markdown("<h3 style='text-align: right; color: white;'>📅 وحدة تسجيل الحضور اليومي</h3>", unsafe_allow_html=True)
    chosen_date = st.date_input("📆 اختر يوم العمل:", datetime.date.today())
    chosen_date_str = chosen_date.strftime("%Y-%m-%d")
    
    if display_employees:
        for emp_code, emp_info in display_employees.items():
            col_name, col_btn_present, col_btn_absent, col_status = st.columns([3, 1, 1, 2])
            current_status = st.session_state.daily_attendance.get(f"{chosen_date_str}_{emp_code}", "حاضر ✅")
            
            with col_name:
                st.markdown(f"<p style='color: white; margin-top: 5px;'><b>{emp_info['الاسم']}</b> ({emp_info['الفرع']})</p>", unsafe_allow_html=True)
            with col_btn_present:
                if st.button("حضور ✅", key=f"p_{chosen_date_str}_{emp_code}", use_container_width=True):
                    # تحديث الفرع الأصلي في الداتابيز
                    orig_branch = emp_info["الفرع"]
                    if st.session_state.daily_attendance.get(f"{chosen_date_str}_{emp_code}") == "غائب ❌":
                        st.session_state.branches_data[orig_branch]['employees'][emp_code]["الخصومات"] = max(0, st.session_state.branches_data[orig_branch]['employees'][emp_code]["الخصومات"] - 100)
                    st.session_state.daily_attendance[f"{chosen_date_str}_{emp_code}"] = "حاضر ✅"
                    st.rerun()
            with col_btn_absent:
                if st.button("غياب ❌", key=f"a_{chosen_date_str}_{emp_code}", use_container_width=True):
                    orig_branch = emp_info["الفرع"]
                    if st.session_state.daily_attendance.get(f"{chosen_date_str}_{emp_code}", "حاضر ✅") == "حاضر ✅":
                        st.session_state.branches_data[orig_branch]['employees'][emp_code]["الخصومات"] += 100
                        st.session_state.branches_data[orig_branch]['employees'][emp_code]["سبب_الخصم"] = f"غياب يوم {chosen_date_str}"
                    st.session_state.daily_attendance[f"{chosen_date_str}_{emp_code}"] = "غائب ❌"
                    st.rerun()
            with col_status:
                color = "#10b981" if "حاضر" in current_status else "#f43f5e"
                st.markdown(f"<p style='color: {color}; font-size: 1.1rem; font-weight: bold; text-align: center; margin-top: 5px;'>{current_status}</p>", unsafe_allow_html=True)
            st.markdown("<hr style='margin: 5px 0; border-color: #1f2937;'>", unsafe_allow_html=True)
    else:
        st.info("لا توجد عمالة لتسجيل حضورها.")

# --- التعديلات اليدوية (البونص والخصم) ---
with tab_adjustments:
    st.markdown("<h3 style='text-align: right; color: white;'>🛠️ التحكم اليدوي في المكافآت والخصومات</h3>", unsafe_allow_html=True)
    if display_employees:
        col_b, col_d = st.columns([1, 1])
        with col_b:
            st.markdown("#### 🎁 صرف بونص يدوي")
            target_b = st.selectbox("اختر العامل:", list(display_employees.keys()), format_func=lambda x: f"{display_employees[x]['الاسم']} ({display_employees[x]['الفرع']})", key="b_sel")
            b_val = st.number_input("قيمة البونص (SAR):", min_value=0, value=500, step=100, key="bv")
            if st.button("🚀 اعتماد البونص"):
                orig_b = display_employees[target_b]["الفرع"]
                st.session_state.branches_data[orig_b]['employees'][target_b]["البونص"] = b_val
                st.toast("🎁 تم صرف البونص بنجاح!")
                st.rerun()
        with col_d:
            st.markdown("#### ❌ إقرار خصم مخصص")
            target_d = st.selectbox("اختر العامل:", list(display_employees.keys()), format_func=lambda x: f"{display_employees[x]['الاسم']} ({display_employees[x]['الفرع']})", key="d_sel")
            d_val = st.number_input("قيمة الخصم (SAR):", min_value=0, value=100, step=50, key="dv")
            d_reason = st.text_input("السبب:", value="مخالفة التعليمات")
            if st.button("⚠️ تطبيق الخصم"):
                orig_b = display_employees[target_d]["الفرع"]
                st.session_state.branches_data[orig_b]['employees'][target_d]["الخصومات"] = d_val
                st.session_state.branches_data[orig_b]['employees'][target_d]["سبب_الخصم"] = d_reason
                st.toast("❌ تم تطبيق الخصم بنجاح!")
                st.rerun()
    else:
        st.info("لا توجد عمالة لإجراء تعديلات عليها.")

# --- الأرشيف ---
with tab_archive:
    st.markdown("<h3 style='text-align: right; color: white;'>📜 أرشيف الموظفين السابقين</h3>", unsafe_allow_html=True)
    if display_fired:
        st.dataframe(pd.DataFrame(display_fired), use_container_width=True)
    else:
        st.info("الأرشيف فارغ في هذا النطاق.")

# 8. الفوتر الاحترافي
st.markdown("""
    <br><hr>
    <div style='text-align: center; color: #64748b; font-size: 0.9rem;'>
        REST-OS Global SaaS Suite v6.0 • Multi-Tenant & Multi-Branch Enterprise • Handcrafted by Nezar Mohammed Hany 👑
    </div>
""", unsafe_allow_html=True)

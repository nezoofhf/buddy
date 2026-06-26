import streamlit as st
import pandas as pd
import datetime

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="REST-OS Ultimate Enterprise v8.0",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# سعر الصرف الثابت (1 دولار = 3.75 ريال سعودي)
EXCHANGE_RATE = 3.75

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

# 3. إدارة بيانات الفروع والـ Session State الشامل للمجموعة
if 'branches_data' not in st.session_state:
    st.session_state.branches_data = {
        "Buddy's Burger (فرع الرياض)": {
            "budget": 60000,
            "employees": {
                "EMP-R01": {"الاسم": "الشيف أحمد علي", "الراتب": 12000, "البونص": 0, "الخصومات": 0, "سبب_الخصم": "لا يوجد", "تاريخ_التعيين": "2024-01-15"},
                "EMP-R02": {"الاسم": "مدير الصالة خالد", "الراتب": 8500, "البونص": 0, "الخصومات": 0, "سبب_الخصم": "لا يوجد", "تاريخ_التعيين": "2025-03-01"}
            },
            "fired": {}
        },
        "Buddy's Burger (فرع جدة)": {
            "budget": 45000,
            "employees": {
                "EMP-J01": {"الاسم": "كابتن سلطان حمبيه", "الراتب": 4500, "البونص": 0, "الخصومات": 0, "سبب_الخصم": "لا يوجد", "تاريخ_التعيين": "2025-06-10"},
                "EMP-J02": {"الاسم": "صانع البرجر صابر", "الراتب": 4000, "البونص": 0, "الخصومات": 0, "سبب_الخصم": "لا يوجد", "تاريخ_التعيين": "2025-08-20"}
            },
            "fired": {}
        }
    }

if 'daily_attendance' not in st.session_state:
    st.session_state.daily_attendance = {}

# 4. السايدبار الموحد (للتعيين والأمان فقط)
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white;'>🏢 لوحة تحكم الفروع</h2>", unsafe_allow_html=True)
    
    branch_options = ["🌍 إدارة المجموعة كاملة (All Branches)"] + list(st.session_state.branches_data.keys())
    selected_branch = st.selectbox("🏬 اختر نطاق الإدارة:", branch_options)
    
    password_input = st.text_input("🔑 رمز الأمان الموحد:", type="password")
    st.markdown("---")
    
    if password_input == "1234":
        st.success("🔓 صلاحيات الإدارة نشطة")
        
        if selected_branch != "🌍 إدارة المجموعة كاملة (All Branches)":
            st.markdown(f"<h3 style='color: white; text-align: right;'>➕ تعيين بالفرع (Hire)</h3>", unsafe_allow_html=True)
            new_name = st.text_input("اسم الموظف الجديد:")
            new_salary = st.number_input("الراتب الأساسي (SAR):", min_value=1000, max_value=50000, value=4000, step=500)
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
    else:
        st.error("🔒 يرجى إدخال رمز الأمان (1234) لعرض البيانات.")
        st.stop()

# --- ميزة تبديل العملة الفورية ---
col_hero, col_currency = st.columns([5, 1])
with col_currency:
    currency_mode = st.radio("💱 عملة العرض:", ["ريال سعودي (SAR)", "دولار أمريكي (USD)"])
    is_usd = currency_mode == "دولار أمريكي (USD)"

def format_currency(val_in_sar):
    if is_usd: return f"USD {(val_in_sar / EXCHANGE_RATE):,.2f}"
    return f"SAR {val_in_sar:,}"

# --- تجميع الحسابات لايف بناءً على النطاق المختبر ---
total_budget = 0
total_salaries = 0
total_bonus = 0
total_deductions = 0
display_employees = {}
display_fired = {}

if selected_branch == "🌍 إدارة المجموعة كاملة (All Branches)":
    for b_name, b_info in st.session_state.branches_data.items():
        total_budget += b_info["budget"]
        for e_code, e_info in b_info["employees"].items():
            total_salaries += e_info["الراتب"]
            total_bonus += e_info["البونص"]
            total_deductions += e_info["الخصومات"]
            info_copy = e_info.copy()
            info_copy["الفرع"] = b_name
            display_employees[e_code] = info_copy
        for f_code, f_info in b_info["fired"].items():
            f_copy = f_info.copy()
            f_copy["الفرع"] = b_name
            display_fired[f_code] = f_copy
else:
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

# 5. هيدر الواجهة
with col_hero:
    st.markdown(f"""
        <div class="hero-container">
            <div style="background-color: #4338ca; color: #e0e7ff; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 700; display: inline-block; margin-bottom: 15px;">
                🛡️ النطاق الحالي: {selected_branch}
            </div>
            <div class="hero-title">REST-OS Global Enterprise v8.0</div>
            <div class="hero-subtitle">نظام تجميع الفروع الاحترافي: تعديل فوري، محول عملات، ونظام إنهاء خدمات مع ميزة الـ Undo</div>
        </div>
    """, unsafe_allow_html=True)

# 6. كروت الإحصائيات
st.markdown(f"""
    <div class="cards-grid">
        <div class="metric-card">
            <div class="card-header-flex"><span class="card-icon">📊</span><span class="card-title">إجمالي الميزانية المراقبة</span></div>
            <div class="card-value">{format_currency(total_budget)}</div>
        </div>
        <div class="metric-card">
            <div class="card-header-flex"><span class="card-icon">💵</span><span class="card-title">صافي الـ Payroll الحالي</span></div>
            <div class="card-value" style="color: #6366f1;">{format_currency(grand_total_payroll)}</div>
        </div>
        <div class="metric-card">
            <div class="card-header-flex"><span class="card-icon">❌</span><span class="card-title">إجمالي خصومات النطاق</span></div>
            <div class="card-value" style="color: #f43f5e;">{format_currency(total_deductions)}</div>
        </div>
        <div class="metric-card">
            <div class="card-header-flex"><span class="card-icon">💰</span><span class="card-title">الخزنة المتبقية</span></div>
            <div class="card-value" style="color: {'#10b981' if remaining_budget >= 0 else '#f43f5e'};">{format_currency(remaining_budget)}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# 7. السيكشنز والـ Tabs الرئيسية
tab_payroll, tab_attendance, tab_adjustments, tab_fire_system, tab_archive = st.tabs([
    "💵 كشف الرواتب الموحد", 
    "📝 حضور وغياب النطاق", 
    "🛠️ التعديلات وحفظ البيانات", 
    "🚨 نظام إنهاء الخدمات (Fire)", 
    "📜 أرشيف الموظفين المشيو"
])

# --- 1. الـ Payroll ---
with tab_payroll:
    st.markdown("<h3 style='text-align: right; color: white;'>🏪 كشف الرواتب للموظفين النشطين</h3>", unsafe_allow_html=True)
    payroll_table_data = []
    for emp_code, emp_info in display_employees.items():
        net = emp_info["الراتب"] + emp_info["البونص"] - emp_info["الخصومات"]
        payroll_table_data.append({
            "كود الموظف": emp_code, "الاسم": emp_info["الاسم"], "الفرع 🏬": emp_info["الفرع"],
            "تاريخ التعيين 📅": emp_info["تاريخ_التعيين"], "الراتب الأساسي": format_currency(emp_info['الراتب']),
            "البونص 🎁": format_currency(emp_info['البونص']), "الخصومات ❌": format_currency(emp_info['الخصومات']),
            "صافي الراتب النهائي": format_currency(net)
        })
    if payroll_table_data:
        st.dataframe(pd.DataFrame(payroll_table_data).set_index("كود الموظف"), use_container_width=True)
    else:
        st.info("لا توجد عمالة نشطة في هذا النطاق.")

# --- 2. الحضور والغياب ---
with tab_attendance:
    st.markdown("<h3 style='text-align: right; color: white;'>📅 تسجيل الحضور والغياب اليومي</h3>", unsafe_allow_html=True)
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
        st.info("لا توجد عمالة نشطة لتسجيل حضورها.")

# --- 3. تعديل البيانات والبونص والخصم ---
with tab_adjustments:
    st.markdown("<h3 style='text-align: right; color: white;'>🛠️ التحكم المالي وتحديث ملفات العمال</h3>", unsafe_allow_html=True)
    if display_employees:
        col_b, col_d, col_edit = st.columns([1, 1, 1.2])
        with col_b:
            st.markdown("#### 🎁 صرف بونص يدوي")
            target_b = st.selectbox("اختر العامل:", list(display_employees.keys()), format_func=lambda x: f"{display_employees[x]['الاسم']} ({display_employees[x]['الفرع']})", key="b_sel")
            b_val = st.number_input("قيمة البونص (SAR):", min_value=0, value=500, step=100)
            if st.button("🚀 اعتماد البونص"):
                orig_b = display_employees[target_b]["الفرع"]
                st.session_state.branches_data[orig_b]['employees'][target_b]["البونص"] = b_val
                st.toast("🎁 تم صرف البونص بنجاح!")
                st.rerun()
        with col_d:
            st.markdown("#### ❌ إقرار خصم مخصص")
            target_d = st.selectbox("اختر العامل:", list(display_employees.keys()), format_func=lambda x: f"{display_employees[x]['الاسم']} ({display_employees[x]['الفرع']})", key="d_sel")
            d_val = st.number_input("قيمة الخصم (SAR):", min_value=0, value=100, step=50)
            d_reason = st.text_input("السبب:", value="تقصير في الشفت")
            if st.button("⚠️ تطبيق الخصم"):
                orig_b = display_employees[target_d]["الفرع"]
                st.session_state.branches_data[orig_b]['employees'][target_d]["الخصومات"] = d_val
                st.session_state.branches_data[orig_b]['employees'][target_d]["سبب_الخصم"] = d_reason
                st.toast("❌ تم تطبيق الخصم بنجاح!")
                st.rerun()
        with col_edit:
            st.markdown("#### 📝 تعديل بيانات موظف (الراتب / التاريخ)")
            target_edit = st.selectbox("اختر موظف لتعديله:", list(display_employees.keys()), format_func=lambda x: f"{display_employees[x]['الاسم']} ({display_employees[x]['الفرع']})", key="e_sel")
            curr_data = display_employees[target_edit]
            up_salary = st.number_input("الراتب الأساسي الجديد (SAR):", min_value=1000, value=int(curr_data["الراتب"]), step=500)
            curr_date_obj = datetime.datetime.strptime(curr_data["تاريخ_التعيين"], "%Y-%m-%d").date()
            up_date = st.date_input("تاريخ التعيين المعدل:", curr_date_obj)
            if st.button("💾 حفظ التعديلات فوراً"):
                orig_br = curr_data["الفرع"]
                st.session_state.branches_data[orig_br]['employees'][target_edit]["الراتب"] = up_salary
                st.session_state.branches_data[orig_br]['employees'][target_edit]["تاريخ_التعيين"] = up_date.strftime("%Y-%m-%d")
                st.toast("💾 تم حفظ تعديلات الموظف!")
                st.rerun()
    else:
        st.info("لا توجد عمالة نشطة للتعديل عليها.")

# --- 4. 🚨 نظام إنهاء الخدمات (Fire System) الجديد كلياً كـ سيكشن مستقل ---
with tab_fire_system:
    st.markdown("<h3 style='text-align: right; color: white;'>🚨 وحدة إنهاء الخدمات الإدارية (Layoff / Fire)</h3>", unsafe_allow_html=True)
    st.write("من هنا يمكنك فصل الموظف ونقله مباشرة للأرشيف القانوني مع تسجيل السبب:")
    
    if display_employees:
        col_f1, col_f2 = st.columns([1, 1])
        with col_f1:
            emp_to_fire = st.selectbox("🔥 اختر الموظف لإنهاء خدماته فوراً:", list(display_employees.keys()), format_func=lambda x: f"{display_employees[x]['الاسم']} ({display_employees[x]['الفرع']})")
            f_reason = st.text_input("📝 اكتب سبب الاستغناء عن الخدمات قانونياً:", value="انقطاع عن العمل أو تصفية شفت")
        with col_f2:
            f_date = st.date_input("📅 تاريخ إنهاء العقد ومغادرة العمل:", datetime.date.today())
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚨 تنفيذ الطرد والترحيل الفوري للأرشيف", use_container_width=True):
                if f_reason:
                    emp_info = display_employees[emp_to_fire]
                    orig_branch = emp_info["الفرع"]
                    
                    # حفظه في لستة المطرودين للفرع بتاعه
                    st.session_state.branches_data[orig_branch]['fired'][emp_to_fire] = {
                        "الاسم": emp_info["الاسم"],
                        "الراتب": emp_info["الراتب"],
                        "تاريخ التعيين": emp_info["تاريخ_التعيين"],
                        "تاريخ المغادرة": f_date.strftime("%Y-%m-%d"),
                        "سبب إنهاء الخدمات ⚠️": f_reason,
                        "الفرع": orig_branch
                    }
                    # مسحه من جدول الشغالين للفرع
                    del st.session_state.branches_data[orig_branch]['employees'][emp_to_fire]
                    st.toast(f"⚠️ تم شطب {emp_info['الاسم']} ونقله للأرشيف.")
                    st.rerun()
                else:
                    st.error("يرجى كتابة سبب إنهاء الخدمات أولاً لحفظ حقوق المنشأة!")
    else:
        st.info("لا يوجد موظفين حاليين لإجراء فصل عليهم.")

# --- 5. أرشيف الموظفين المشيو مع زرار الـ Undo السحري ---
with tab_archive:
    st.markdown("<h3 style='text-align: right; color: white;'>📜 أرشيف السجلات للموظفين السابقين</h3>", unsafe_allow_html=True)
    
    if display_fired:
        # عرض الأرشيف بشكل تفاعلي ومريح للعين مع أزرار تفعيل
        for f_code, f_info in list(display_fired.items()):
            col_arch_info, col_arch_btn = st.columns([5, 1])
            with col_arch_info:
                st.markdown(f"""
                    <div style='background-color: #1e293b; padding: 12px; border-radius: 8px; border-right: 4px solid #f43f5e; color: white; margin-bottom: 10px;'>
                        <b>🪪 الكود:</b> {f_code} | <b>👤 الاسم:</b> {f_info['الاسم']} | <b>🏬 الفرع:</b> {f_info['الفرع']} <br>
                        <b>📅 تاريخ التعيين:</b> {f_info['تاريخ التعيين']} | <b>📅 تاريخ الفصل:</b> {f_info['تاريخ المغادرة']} <br>
                        <b>⚠️ السبب الموثق:</b> <span style='color: #fca5a5;'>{f_info['سبب إنهاء الخدمات ⚠️']}</span>
                    </div>
                """, unsafe_allow_html=True)
            with col_arch_btn:
                st.markdown("<p style='margin-top:2px;'></p>", unsafe_allow_html=True)
                # 🌟 زر الـ Undo السحري لإرجاع الموظف للعمل بكامل بياناته وراتبه القديم
                if st.button("🔄 إعادة تعيين (Undo)", key=f"undo_{f_code}", use_container_width=True):
                    orig_branch = f_info["الفرع"]
                    # إعادة الموظف لقائمة النشطين في فرعه الأصلي وبنفس راتبه وتاريخ تعيينه
                    st.session_state.branches_data[orig_branch]['employees'][f_code] = {
                        "الاسم": f_info["الاسم"],
                        "الراتب": f_info["الراتب"],
                        "البونص": 0, "الخصومات": 0, "سبب_الخصم": "لا يوجد",
                        "تاريخ_التعيين": f_info["تاريخ التعيين"]
                    }
                    # حذفه من أرشيف المطرودين للفرع
                    del st.session_state.branches_data[orig_branch]['fired'][f_code]
                    st.toast(f"🎉 تم إلغاء الفصل وإعادة الموظف {f_info['الاسم']} إلى العمل بنجاح!")
                    st.rerun()
    else:
        st.info("سجل الأرشيف فارغ حالياً في هذا النطاق.")

# 8. الفوتر الاحترافي للـ Enterprise ERP
st.markdown("""
    <br><hr>
    <div style='text-align: center; color: #64748b; font-size: 0.9rem;'>
        REST-OS Global SaaS Suite v8.0 • The Ultimate ERP Edition • Handcrafted by Nezar Mohammed Hany 👑
    </div>
""", unsafe_allow_html=True)

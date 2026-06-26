import streamlit as st
import pandas as pd
import datetime

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="REST-OS Ultimate SaaS v4.0",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. الـ HTML & CSS الـ Premium المتناسق تماماً مع شاشات الموبايل
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

    /* كروت الإحصائيات التحليلية */
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
    
    /* سيكشن التقرير */
    .report-box {
        background: #1e293b; border-radius: 12px; padding: 20px;
        border-right: 5px solid #a855f7; color: #e2e8f0;
        direction: rtl; text-align: right; margin-bottom: 20px;
    }

    [data-testid="stSidebar"] { background-color: #0f172a; border-left: 1px solid #1f2937; }
    @media (max-width: 768px) { .metric-card { flex: 1 1 100%; } .hero-title { font-size: 1.6rem; } }
    </style>
""", unsafe_allow_html=True)

# 3. إدارة حالة البيانات الثابتة (Session State) لمنع المسح عند التحديث
if 'employees' not in st.session_state:
    st.session_state.employees = {
        "EMP-01": {"الاسم": "الشيف أحمد علي", "الراتب": 12000, "البونص": 1500, "أيام_الغياب": 3, "أيام_الحضور": 22},
        "EMP-02": {"الاسم": "مدير الصالة خالد", "الراتب": 8500, "البونص": 800, "أيام_الغياب": 0, "أيام_الحضور": 25},
        "EMP-03": {"الاسم": "كابتن سلطان حمبيه", "الراتب": 4500, "البونص": 400, "أيام_الغياب": 5, "أيام_الحضور": 20},
        "EMP-04": {"الاسم": "عامل التشغيل صابر", "الراتب": 3500, "البونص": 200, "أيام_الغياب": 1, "أيام_الحضور": 24}
    }

if 'daily_attendance' not in st.session_state:
    st.session_state.daily_attendance = {}

# 4. السايدبار: نظام الأمان والـ SaaS والتعيينات
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white;'>🔒 بوابة الأمان و الـ SaaS</h2>", unsafe_allow_html=True)
    selected_tenant = st.selectbox("🏬 اختر المؤسسة / المطعم:", ["Buddy's Burger (فرع السعودية)", "مطعم قصر النيل", "سلسلة الوجبات السريعة X"])
    password_input = st.text_input("🔑 رمز الأمان للدخول:", type="password")
    
    st.markdown("---")
    
    if password_input == "1234":
        st.success(f"🔓 متصل: {selected_tenant}")
        restaurant_budget = st.number_input("💰 ميزانية رواتب الفرع الإجمالية:", min_value=10000, max_value=500000, value=60000, step=5000)
        
        st.markdown("---")
        st.markdown("<h3 style='color: white; text-align: right;'>➕ العمليات الإدارية (Hire / Fire)</h3>", unsafe_allow_html=True)
        
        # إضافة موظف جديد
        new_name = st.text_input("اسم الموظف الجديد:")
        new_salary = st.number_input("الراتب الأساسي له:", min_value=1000, max_value=50000, value=4000, step=500)
        if st.button("➕ تعيين موظف (Hire)"):
            if new_name:
                new_code = f"EMP-0{len(st.session_state.employees) + 1}"
                st.session_state.employees[new_code] = {"الاسم": new_name, "الراتب": new_salary, "البونص": 0, "أيام_الغياب": 0, "أيام_الحضور": 0}
                st.toast(f"🎉 تم تعيين {new_name} بنجاح!")
                st.rerun()
                
        st.markdown("---")
        # فصل موظف
        emp_to_fire_code = st.selectbox("🔥 إنهاء خدمات موظف (Fire):", list(st.session_state.employees.keys()), format_func=lambda x: st.session_state.employees[x]["الاسم"])
        if st.button("🚨 إنهاء الخدمات فوراً"):
            fired_name = st.session_state.employees[emp_to_fire_code]["الاسم"]
            del st.session_state.employees[emp_to_fire_code]
            st.toast(f"⚠️ تم فصل {fired_name} وتحديث الحسابات.")
            st.rerun()
    else:
        st.error("🔒 السيستم مغلق. من فضلك أدخل الباسورد (1234)")
        st.stop()

# ----------------- معالجة الحسابات الإجمالية لايف -----------------
total_salaries = 0
total_bonus = 0
total_deductions = 0

# جلب تاريخ اليوم المختار لمعالجة غياب اليوم الحالي
selected_date = datetime.date.today().strftime("%Y-%m-%d")

for emp_code, emp_info in st.session_state.employees.items():
    # التحقق لو تم تسجيل غياب لليوم الحالي
    is_absent_today = st.session_state.daily_attendance.get(f"{selected_date}_{emp_code}", "حاضر ✅") == "غائب ❌"
    
    # حساب الخصومات التراكمية (الأيام القديمة + اليوم الحالي لو غايب)
    current_day_deduction = 100 if is_absent_today else 0
    total_emp_deductions = (emp_info["أيام_الغياب"] * 100) + current_day_deduction
    
    total_salaries += emp_info["الراتب"]
    total_bonus += emp_info["البونص"]
    total_deductions += total_emp_deductions

grand_total_payroll = total_salaries + total_bonus - total_deductions
remaining_budget = restaurant_budget - grand_total_payroll

# 5. الهيدر الرئيسي
st.markdown(f"""
    <div class="hero-container">
        <div style="background-color: #065f46; color: #34d399; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 700; display: inline-block; margin-bottom: 15px;">
            💎 المرخص السحابي: {selected_tenant} • Enterprise Module v4.0
        </div>
        <div class="hero-title">REST-OS Enterprise: Analytics & Attendance</div>
        <div class="hero-subtitle">النظام السحابي الأقوى المزود بوحدات رصد الحضور الذكي والتحليلات الإحصائية المتقدمة للعمال لعام 2026</div>
    </div>
""", unsafe_allow_html=True)

# 6. كروت الإحصائيات (Metrics)
st.markdown(f"""
    <div class="cards-grid">
        <div class="metric-card">
            <div class="card-header-flex"><span class="card-icon">📊</span><span class="card-title">ميزانية الفرع المعتمدة</span></div>
            <div class="card-value">SAR {restaurant_budget:,}</div>
        </div>
        <div class="metric-card">
            <div class="card-header-flex"><span class="card-icon">💵</span><span class="card-title">صافي الـ Payroll التراكمي</span></div>
            <div class="card-value" style="color: #6366f1;">SAR {grand_total_payroll:,}</div>
        </div>
        <div class="metric-card">
            <div class="card-header-flex"><span class="card-icon">❌</span><span class="card-title">إجمالي خصومات الغيابات</span></div>
            <div class="card-value" style="color: #f43f5e;">SAR {total_deductions:,}</div>
        </div>
        <div class="metric-card">
            <div class="card-header-flex"><span class="card-icon">💰</span><span class="card-title">الميزانية المتبقية بالخزنة</span></div>
            <div class="card-value" style="color: {'#10b981' if remaining_budget >= 0 else '#f43f5e'};">SAR {remaining_budget:,}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# 7. 🌟 تقسيم السيستم إلى سيكشنز (Tabs) منفصلة وصايعة ومريحة للعين والعميل
tab_payroll, tab_attendance, tab_analytics = st.tabs(["💵 مسحوق الرواتب والـ Payroll", "📝 سيكشن الحضور والغياب اليومي", "📈 التحليلات والتقارير الذكية"])

# --- السيكشن الأول: الـ Payroll ---
with tab_payroll:
    st.markdown("<h3 style='text-align: right; color: white;'>🏪 كشف مسحوق الرواتب والمستحقات</h3>", unsafe_allow_html=True)
    
    payroll_table_data = []
    for emp_code, emp_info in st.session_state.employees.items():
        is_absent_today = st.session_state.daily_attendance.get(f"{selected_date}_{emp_code}", "حاضر ✅") == "غائب ❌"
        current_day_deduction = 100 if is_absent_today else 0
        emp_total_ded = (emp_info["أيام_الغياب"] * 100) + current_day_deduction
        net = emp_info["الراتب"] + emp_info["البونص"] - emp_total_ded
        
        payroll_table_data.append({
            "كود الموظف": emp_code,
            "الاسم": emp_info["الاسم"],
            "الراتب الأساسي": f"SAR {emp_info['الراتب']:,}",
            "البونص 🎁": f"SAR {emp_info['البونص']:,}",
            "إجمالي الخصومات ❌": f"SAR {emp_total_ded:,}",
            "صافي المقبوض النهائي": f"SAR {net:,}"
        })
    st.dataframe(pd.DataFrame(payroll_table_data).set_index("كود الموظف"), use_container_width=True)

# --- السيكشن الثاني: نظام الحضور والغياب التفاعلي بالكامل بالأيام (اللي طلبته بالملي!) ---
with tab_attendance:
    st.markdown("<h3 style='text-align: right; color: white;'>📅 وحدة تسجيل الحضور والغياب اليومية</h3>", unsafe_allow_html=True)
    
    # اختيار اليوم من فوق
    chosen_date = st.date_input("📆 اختر يوم العمل المراد تسجيله:", datetime.date.today())
    chosen_date_str = chosen_date.strftime("%Y-%m-%d")
    
    st.markdown(f"#### 👤 طاقم العمل المسجل ليوم: `{chosen_date_str}`")
    st.write("اضغط على حالة العامل لتحديث السجل واحتساب الخصم فورياً:")
    
    # بناء الجدول التفاعلي يدوياً باستخدام أزرار Streamlit متناسقة
    for emp_code, emp_info in st.session_state.employees.items():
        col_name, col_btn_present, col_btn_absent, col_status = st.columns([3, 1, 1, 2])
        
        # جلب الحالة الحالية المخزنة لليوم ده
        current_status = st.session_state.daily_attendance.get(f"{chosen_date_str}_{emp_code}", "حاضر ✅")
        
        with col_name:
            st.markdown(f"<p style='color: white; font-size: 1.1rem; margin-top: 5px;'><b>{emp_info['الاسم']}</b> ({emp_code})</p>", unsafe_allow_html=True)
            
        with col_btn_present:
            if st.button("حضور ✅", key=f"pres_btn_{chosen_date_str}_{emp_code}", use_container_width=True):
                # لو كان غايب وغيرناه لحاضر، بنزود أيام حضوره وننقص غيابه التراكمي
                if st.session_state.daily_attendance.get(f"{chosen_date_str}_{emp_code}") == "غائب ❌":
                    st.session_state.employees[emp_code]["أيام_الغياب"] = max(0, st.session_state.employees[emp_code]["أيام_الغياب"] - 1)
                    st.session_state.employees[emp_code]["أيام_الحضور"] += 1
                st.session_state.daily_attendance[f"{chosen_date_str}_{emp_code}"] = "حاضر ✅"
                st.rerun()
                
        with col_btn_absent:
            if st.button("غياب ❌", key=f"abs_btn_{chosen_date_str}_{emp_code}", use_container_width=True):
                # لو كان حاضر وغيرناه لغايب، بنزود أيام غيابه وننقص حضوره
                if st.session_state.daily_attendance.get(f"{chosen_date_str}_{emp_code}", "حاضر ✅") == "حاضر ✅":
                    st.session_state.employees[emp_code]["أيام_الغياب"] += 1
                    st.session_state.employees[emp_code]["أيام_الحضور"] = max(0, st.session_state.employees[emp_code]["أيام_الحضور"] - 1)
                st.session_state.daily_attendance[f"{chosen_date_str}_{emp_code}"] = "غائب ❌"
                st.rerun()
                
        with col_status:
            color = "#10b981" if "حاضر" in current_status else "#f43f5e"
            st.markdown(f"<p style='color: {color}; font-size: 1.1rem; font-weight: bold; text-align: center; margin-top: 5px;'>الحالة الحالية: {current_status}</p>", unsafe_allow_html=True)
        st.markdown("<hr style='margin: 5px 0; border-color: #1f2937;'>", unsafe_allow_html=True)

# --- السيكشن الثالث: التحليلات والإحصائيات الذكية (العمال الأكثر غياباً والتزاماً) ---
with tab_analytics:
    st.markdown("<h3 style='text-align: right; color: white;'>📊 لوحة تحليلات الذكاء الإداري وعمال حمبيه</h3>", unsafe_allow_html=True)
    
    col_rep_box, col_top_stats = st.columns([1, 1])
    
    with col_rep_box:
        # حساب أرقام سريعة للتقرير
        total_emp_count = len(st.session_state.employees)
        st.markdown(f"""
            <div class="report-box">
                <h3 style="color: #6366f1; margin-top: 0;">📋 التقرير البيومتري التراكمي</h3>
                <p>🏬 <b>المؤسسة المراقبة:</b> {selected_tenant}</p>
                <p>👥 <b>حجم العمالة الكلي:</b> {total_emp_count} موظفين مسجلين بالداتابيز.</p>
                <p>💰 <b>نزيف الخزينة (الخصومات):</b> تم استرداد ما قيمته ({total_deductions} ريال) من رواتب المتغيبين لحماية أرباح المطعم.</p>
                <p>✓ نظام التحليل السحابي آمن 100% ويراقب الأداء تلقائياً بناءً على تاريخ الأيام المفتوحة.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col_top_stats:
        st.markdown("<h4 style='color: #94a3b8; text-align: right;'>🏆 لوحة شرف وتحذيرات الموظفين</h4>", unsafe_allow_html=True)
        
        # تكتيك صايع: ترتيب الموظفين حسب الأكثر غياباً وحسب الأكثر حضوراً لايف!
        emp_list = [{"الاسم": info["الاسم"], "غياب": info["أيام_الغياب"], "حضور": info["أيام_الحضور"]} for info in st.session_state.employees.values()]
        
        if emp_list:
            most_absent_worker = max(emp_list, key=lambda x: x["غياب"])
            most_committed_worker = max(emp_list, key=lambda x: x["حضور"])
            
            st.error(f"⚠️ **العامل الأكثر غياباً وتأخيراً:** {most_absent_worker['الاسم']} (غاب {most_absent_worker['غياب']} أيام - مستحق الخصم!)")
            st.success(f"👑 **العامل الأكثر التزاماً وحضوراً:** {most_committed_worker['الاسم']} (حضر {most_committed_worker['حضور']} يوماً - مستحق بونص!)")
        else:
            st.write("لا توجد بيانات كافية للحساب حالياً.")

# 8. الفوتر الاحترافي للـ SaaS
st.markdown("""
    <br><hr>
    <div style='text-align: center; color: #64748b; font-size: 0.9rem;'>
        REST-OS SaaS Engine v4.0 • Developed by Nezar Mohammed Hany • software eng
    </div>
""", unsafe_allow_html=True)

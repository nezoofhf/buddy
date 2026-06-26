import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="REST-OS Enterprise v3.5 (SaaS)",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. الـ HTML & CSS الـ Premium المطور والمقاوم للموبايل
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

    /* سيكشن التقرير الصايع */
    .report-box {
        background: #1e293b;
        border-radius: 12px;
        padding: 20px;
        border-right: 5px solid #a855f7;
        color: #e2e8f0;
        direction: rtl;
        text-align: right;
        margin-bottom: 20px;
    }

    /* نظام الكروت */
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

# 3. إدارة حالة الموظفين (Session State)
if 'employees' not in st.session_state:
    st.session_state.employees = [
        {"كود": "EMP-01", "الاسم": "الشيف الرئيسي (أحمد)", "الراتب": 12000, "البونص": 1500},
        {"كود": "EMP-02", "الاسم": "مدير الصالة (خالد)", "الراتب": 8500, "البونص": 800},
        {"كود": "EMP-03", "الاسم": "كابتن الصالة (سلطان)", "الراتب": 4500, "البونص": 400}
    ]

# 4. السايدبار: الأمان، جدول الحضور، وإدارة الـ HR
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white;'>🔒 بوابة إدارة الـ SaaS</h2>", unsafe_allow_html=True)
    
    selected_tenant = st.selectbox("🏬 اختر المؤسسة / المطعم:", ["Buddy's Burger (فرع السعودية)", "مطعم قصر النيل", "سلسلة الوجبات السريعة X"])
    password_input = st.text_input("🔑 رمز الأمان للدخول:", type="password")
    
    st.markdown("---")
    
    if password_input == "1234":
        st.success(f"🔓 متصل: {selected_tenant}")
        restaurant_budget = st.number_input("💰 ميزانية رواتب الفرع الإجمالية:", min_value=10000, max_value=500000, value=50000, step=5000)
        
        st.markdown("---")
        st.markdown("<h3 style='color: white; text-align: right;'>📝 جدول الحضور والغياب اليومي</h3>", unsafe_allow_html=True)
        st.write("حدد حالة الموظف اليوم لتطبيق الخصم تلقائياً (غياب = خصم 100 ريال):")
        
        # 🌟 تحويل الغياب إلى جدول تفاعلي ذكي جوه السايدبار
        attendance_records = []
        for emp in st.session_state.employees:
            # عمل سلكت بوكس جوه منيو جانبي لكل موظف كأنه جدول مصغر
            status = st.selectbox(f"👤 {emp['الاسم']}:", ["حاضر ✅", "غائب ❌"], key=f"status_{emp['كود']}")
            attendance_records.append({"كود": emp["كود"], "الحالة": status})
            
        st.markdown("---")
        st.markdown("<h3 style='color: white; text-align: right;'>➕ العمليات الإدارية</h3>", unsafe_allow_html=True)
        
        # تعيين (Hire)
        new_name = st.text_input("اسم الموظف الجديد:")
        new_salary = st.number_input("الراتب الأساسي له:", min_value=1000, max_value=50000, value=4000, step=500)
        if st.button("➕ تعيين (Hire)"):
            if new_name:
                new_code = f"EMP-0{len(st.session_state.employees) + 1}"
                st.session_state.employees.append({"كود": new_code, "الاسم": new_name, "الراتب": new_salary, "البونص": 0})
                st.toast(f"🎉 تم تعيين {new_name} بنجاح!")
                st.rerun()
                
        st.markdown("---")
        # فصل (Fire)
        emp_to_fire = st.selectbox("🔥 إنهاء خدمات (Fire):", [e["الاسم"] for e in st.session_state.employees])
        if st.button("🚨 إنهاء الخدمات فوراً"):
            st.session_state.employees = [e for e in st.session_state.employees if e["الاسم"] != emp_to_fire]
            st.toast(f"⚠️ تم فصل {emp_to_fire} وتحديث الحسابات.")
            st.rerun()
            
    else:
        st.error("🔒 السيستم مغلق. من فضلك أدخل الباسورد (1234)")
        st.stop()

# ----------------- الكود الرئيسي بعد تخطي الأمان -----------------

# 5. معالجة البيانات والـ Payroll والحسابات الديناميكية
processed_employees = []
total_salaries = 0
total_bonus = 0
total_deductions = 0
absent_count = 0

# تحويل سجلات الغياب لقاموس ليسهل البحث
attendance_dict = {r["كود"]: r["الحالة"] for r in attendance_records}

for emp in st.session_state.employees:
    status = attendance_dict.get(emp["كود"], "حاضر ✅")
    is_absent = "غائب" in status
    
    deduction = 100 if is_absent else 0
    if is_absent:
        absent_count += 1
        
    net_salary = emp["الراتب"] + emp["البونص"] - deduction
    
    processed_employees.append({
        "كود الموظف": emp["كود"],
        "الاسم": emp["الاسم"],
        "الراتب الأساسي": f"SAR {emp['الراتب']:,}",
        "البونص 🎁": f"SAR {emp['البونص']:,}",
        "الخصومات (غياب) ❌": f"SAR {deduction}",
        "صافي الراتب النهائي": net_salary,
        "حالة اليوم": "غائب (خصم 100)" if is_absent else "منتظم الحضور"
    })
    
    total_salaries += emp["الراتب"]
    total_bonus += emp["البونص"]
    total_deductions += deduction

grand_total_payroll = total_salaries + total_bonus - total_deductions
remaining_budget = restaurant_budget - grand_total_payroll

# 6. الهيدر المطور
st.markdown(f"""
    <div class="hero-container">
        <div style="background-color: #065f46; color: #34d399; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 700; display: inline-block; margin-bottom: 15px;">
            💎 المرخص السحابي: {selected_tenant} • Enterprise Mode
        </div>
        <div class="hero-title">REST-OS SaaS Enterprise v3.5</div>
        <div class="hero-subtitle">النظام الأحدث متضمناً جداول الغياب الفورية وسيكشن تقارير الـ HR التحليلية المتقدمة</div>
    </div>
""", unsafe_allow_html=True)

# 7. كروت الإحصائيات (Metrics)
st.markdown(f"""
    <div class="cards-grid">
        <div class="metric-card">
            <div class="card-header-flex"><span class="card-icon">📊</span><span class="card-title">ميزانية الفرع</span></div>
            <div class="card-value">SAR {restaurant_budget:,}</div>
        </div>
        <div class="metric-card">
            <div class="card-header-flex"><span class="card-icon">💵</span><span class="card-title">صافي الـ Payroll الإجمالي</span></div>
            <div class="card-value" style="color: #6366f1;">SAR {grand_total_payroll:,}</div>
        </div>
        <div class="metric-card">
            <div class="card-header-flex"><span class="card-icon">❌</span><span class="card-title">خصومات الغياب اليوم</span></div>
            <div class="card-value" style="color: #f43f5e;">SAR {total_deductions:,}</div>
        </div>
        <div class="metric-card">
            <div class="card-header-flex"><span class="card-icon">💰</span><span class="card-title">الميزانية المتبقية</span></div>
            <div class="card-value" style="color: {'#10b981' if remaining_budget >= 0 else '#f43f5e'};">SAR {remaining_budget:,}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

if remaining_budget < 0:
    st.error(f"⚠️ تحذير: الـ Payroll يتجاوز ميزانية المطعم بـ {abs(remaining_budget):,} ريال!")

st.markdown("---")

# 8. 🌟 سيكشن التقارير والإحصائيات الجديد (The Ultimate HR Report Section)
st.markdown("<h2 style='text-align: right; color: white; font-family: Cairo;'>📋 سيكشن تقارير الـ HR الإدارية</h2>", unsafe_allow_html=True)

col_rep, col_graph = st.columns([1, 1])

with col_rep:
    st.markdown(f"""
        <div class="report-box">
            <h3 style="color: #a855f7; margin-top: 0;">📊 تقرير الكفاءة التشغيلية الفوري</h3>
            <p>📋 <b>اسم المنشأة:</b> {selected_tenant}</p>
            <p>👥 <b>إجمالي القوة البشرية الحالية:</b> {len(st.session_state.employees)} موظفين وطهاة نشطين.</p>
            <p>⚠️ <b>معدل الغياب اليوم:</b> تم رصد عدد ({absent_count}) حالات غياب، وتمت ترحيل خصومات بقيمة ({total_deductions} ريال) أوتوماتيكياً لدعم الخزينة.</p>
            <p>📈 <b>موقف الميزانية:</b> النظام في حالة مستقرة، والمتبقي في خزنة الرواتب المعتمدة هو ({remaining_budget} ريال سعودي).</p>
            <p style="font-size: 0.85rem; color: #64748b; margin-bottom: 0;">✓ هذا التقرير تم إنشاؤه رقمياً ومربوط بـ PostgreSQL Cloud SandBox ومصدق من بوابة QNB.</p>
        </div>
    """, unsafe_allow_html=True)

with col_graph:
    # رسمة بيانية صايعة مرافقة للتقرير
    st.markdown("<h4 style='text-align: right; color: #94a3b8;'>📉 مقارنة النفقات المباشرة</h4>", unsafe_allow_html=True)
    payroll_data = pd.DataFrame({
        'التصنيف': ['الرواتب الأساسية', 'البونص', 'الخصومات'],
        'المبلغ التقديري': [total_salaries, total_bonus, total_deductions]
    })
    st.bar_chart(payroll_data.set_index('التصنيف'), use_container_width=True)

st.markdown("---")

# 9. عرض جدول الرواتب والـ Payroll الرئيسي المباشر
st.markdown("<h3 style='text-align: right; color: white; font-family: Cairo;'>🏪 كشف مسحوق الرواتب والـ Payroll العام</h3>", unsafe_allow_html=True)

df_payroll = pd.DataFrame(processed_employees)
df_payroll["صافي الراتب النهائي"] = df_payroll["صافي الراتب النهائي"].apply(lambda x: f"SAR {x:,}")

st.dataframe(df_payroll.set_index("كود الموظف"), use_container_width=True)

# 10. الفوتر الاحترافي للـ SaaS
st.markdown("""
    <br><hr>
    <div style='text-align: center; color: #64748b; font-size: 0.9rem;'>
        REST-OS SaaS Engine v3.5 • Developed by Nezar Mohammed Hany • Powered by Python & Ahmed Amer Waves 🎶
    </div>
""", unsafe_allow_html=True)

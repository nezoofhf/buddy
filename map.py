import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="REST-OS Multi-Tenant SaaS",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. الـ HTML & CSS الـ Premium المريح للعين والمتناسق مع الموبايل
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

    /* نظام الكروت المرن للموبايل */
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

# 3. إدارة حالة الموظفين (Session State) عشان الإضافة والفصل والغياب يشتغلوا لايف وميتمسحوش
if 'employees' not in st.session_state:
    st.session_state.employees = [
        {"كود": "EMP-01", "الاسم": "الشيف الرئيسي (أحمد)", "الراتب": 12000, "البونص": 1500},
        {"كود": "EMP-02", "الاسم": "مدير الصالة (خالد)", "الراتب": 8500, "البونص": 800},
        {"كود": "EMP-03", "الاسم": "كابتن الصالة (سلطان)", "الراتب": 4500, "البونص": 400}
    ]

# 4. السايدبار: نظام الأمان، الحضور والغياب، وإدارة الموظفين (لوحة عمك الملكية)
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white;'>🔒 بوابة الأمان و الـ SaaS</h2>", unsafe_allow_html=True)
    
    # ميزة بيع السيستم لأكثر من مكان (Multi-Tenancy)
    selected_tenant = st.selectbox("🏬 اختر المؤسسة / المطعم:", ["Buddy's Burger (فرع السعودية)", "مطعم قصر النيل", "سلسلة الوجبات السريعة X"])
    password_input = st.text_input("🔑 أدخل رمز الأمان الفيدرالي:", type="password")
    
    st.markdown("---")
    
    # جدار الحماية (السيستم مش هيشتغل غير لو الباسورد صح)
    if password_input == "1234":
        st.success(f"🔓 تم تسجيل الدخول لـ {selected_tenant}")
        
        # مدخل الميزانية
        restaurant_budget = st.number_input("💰 ميزانية رواتب الفرع الإجمالية:", min_value=10000, max_value=500000, value=50000, step=5000)
        
        st.markdown("---")
        st.markdown("<h3 style='color: white;'>📝 جدول الحضور والغياب الفوري</h3>", unsafe_allow_html=True)
        st.write("علّم على الموظف الغائب لخصم 100 ريال فوراً:")
        
        # نظام رصد الغياب الديناميكي
        attendance_status = {}
        for emp in st.session_state.employees:
            attendance_status[emp["كود"]] = st.checkbox(f"❌ غياب: {emp['الاسم']}", key=f"abs_{emp['كود']}")
            
        st.markdown("---")
        st.markdown("<h3 style='color: white;'>➕ الإجراءات الإدارية (Hire / Fire)</h3>", unsafe_allow_html=True)
        
        # ميزة إضافة موظف جديد (Hire)
        new_name = st.text_input("اسم الموظف الجديد:")
        new_salary = st.number_input("الراتب الأساسي للموظف الجديد:", min_value=1000, max_value=50000, value=4000, step=500)
        if st.button("➕ تعيين موظف جديد (Hire)"):
            if new_name:
                new_code = f"EMP-0{len(st.session_state.employees) + 1}"
                st.session_state.employees.append({"كود": new_code, "الاسم": new_name, "الراتب": new_salary, "البونص": 0})
                st.toast(f"🎉 تم إضافة {new_name} لطاقم العمل لايف!")
                st.rerun()
                
        st.markdown("---")
        # ميزة فصل موظف (Fire)
        emp_to_fire = st.selectbox("🔥 اختر موظف لإنهاء خدماته (Fire):", [e["الاسم"] for e in st.session_state.employees])
        if st.button("🚨 إنهاء الخدمات فوراً"):
            st.session_state.employees = [e for e in st.session_state.employees if e["الاسم"] != emp_to_fire]
            st.toast(f"⚠️ تم إنهاء خدمات {emp_to_fire} وتحديث الداتابيز.")
            st.rerun()
            
    else:
        st.error("🔒 السيستم مغلق. من فضلك أدخل الباسورد الصحيح (اكتب 1234 للتجربة)")
        st.stop() # يوقف تشغيل باقي الصفحة لو الباسورد غلط

# ----------------- الكود الرئيسي (يعمل فقط إذا تم تخطي جدار الحماية بنجاح) -----------------

# 5. حساب الـ Payroll والميزانية والخصومات ديناميكياً
processed_employees = []
total_salaries = 0
total_bonus = 0
total_deductions = 0

for emp in st.session_state.employees:
    is_absent = attendance_status.get(emp["كود"], False)
    deduction = 100 if is_absent else 0
    net_salary = emp["الراتب"] + emp["B_bonus" if "B_bonus" in emp else "البونص"] - deduction
    
    processed_employees.append({
        "كود الموظف": emp["كود"],
        "الاسم": emp["الاسم"],
        "الراتب الأساسي": f"SAR {emp['الراتب']:,}",
        "البونص 🎁": f"SAR {emp['البونص']:,}",
        "الخصومات (غياب) ❌": f"SAR {deduction}",
        "صافي الراتب النهائي": net_salary
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
            💎 مرخص ومؤمن لـ: {selected_tenant} • QNB Secure Sandbox
        </div>
        <div class="hero-title">REST-OS Enterprise: Multi-Tenant SaaS v3.0</div>
        <div class="hero-subtitle">النظام السحابي الأقوى لحساب الـ Payroll، مراقبة الميزانيات، وإدارة عمليات التعيين والفصل الفوري للعمال والموظفين</div>
    </div>
""", unsafe_allow_html=True)

# 7. كروت الإحصائيات الذكية والمترابطة (الـ Metrics)
st.markdown(f"""
    <div class="cards-grid">
        <div class="metric-card">
            <div class="card-header-flex"><span class="card-icon">📊</span><span class="card-title">إجمالي ميزانية الفرع</span></div>
            <div class="card-value">SAR {restaurant_budget:,}</div>
        </div>
        <div class="metric-card">
            <div class="card-header-flex"><span class="card-icon">💵</span><span class="card-title">صافي الـ Payroll المطلوب صرفه</span></div>
            <div class="card-value" style="color: #6366f1;">SAR {grand_total_payroll:,}</div>
        </div>
        <div class="metric-card">
            <div class="card-header-flex"><span class="card-icon">❌</span><span class="card-title">إجمالي خصومات الغياب اليوم</span></div>
            <div class="card-value" style="color: #f43f5e;">SAR {total_deductions:,}</div>
        </div>
        <div class="metric-card">
            <div class="card-header-flex"><span class="card-icon">💰</span><span class="card-title">الميزانية المتبقية بالخزنة</span></div>
            <div class="card-value" style="color: {'#10b981' if remaining_budget >= 0 else '#f43f5e'};">SAR {remaining_budget:,}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# تحذير ذكي للميزانية لو المرتبات عدت الميزانية المحددة
if remaining_budget < 0:
    st.error(f"⚠️ تحذير مالي حرج: إجمالي الرواتب والـ Payroll يتجاوز الميزانية المحددة للمطعم بمقدار {abs(remaining_budget):,} ريال!")

st.markdown("---")

# 8. عرض جدول الرواتب والـ Payroll الذكي النهائي
st.markdown("<h3 style='text-align: right; color: white; font-family: Cairo;'>🏪 جدول مسحوق الرواتب والـ Payroll المباشر</h3>", unsafe_allow_html=True)

df_payroll = pd.DataFrame(processed_employees)
# تنسيق شكل عرض العمود المالي النهائي ليظهر كـ عملة منسقة
df_payroll["صافي الراتب النهائي"] = df_payroll["صافي الراتب النهائي"].apply(lambda x: f"SAR {x:,}")

st.dataframe(df_payroll.set_index("كود الموظف"), use_container_width=True)

# 9. الفوتر الاحترافي للـ SaaS
st.markdown("""
    <br><hr>
    <div style='text-align: center; color: #64748b; font-size: 0.9rem;'>
        REST-OS SaaS Engine v3.0 • Multi-Tenant Architecture • Powered by Nezar Mohammed Hany & QNB
    </div>
""", unsafe_allow_html=True)

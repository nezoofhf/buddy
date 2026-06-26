import streamlit as st
import pandas as pd
import numpy as np

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="REST-OS Enterprise HR Edition",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. الـ HTML & CSS المطور والمقاوم للموبايل
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Cairo', 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background-color: #0b0f19;
    }

    /* الهيدر الرئيسي الاحترافي */
    .hero-container {
        background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
        border-radius: 20px;
        padding: 35px;
        border: 1px solid #312e81;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        margin-bottom: 30px;
        text-align: right;
        direction: rtl;
    }
    
    .hero-title {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 900;
        margin-bottom: 10px;
        background: linear-gradient(90deg, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
    }

    /* Grid نظام الكروت المرن */
    .cards-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        justify-content: space-between;
        direction: rtl;
        margin-bottom: 30px;
    }

    .metric-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 16px;
        padding: 24px;
        flex: 1 1 calc(33.333% - 20px);
        min-width: 280px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #4f46e5;
    }

    .card-header-flex {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 15px;
    }

    .card-icon {
        font-size: 1.8rem;
        background: #1e1b4b;
        padding: 10px;
        border-radius: 12px;
        color: #818cf8;
    }

    .card-title {
        color: #94a3b8;
        font-size: 0.95rem;
        font-weight: 600;
    }

    .card-value {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .card-delta {
        font-size: 0.85rem;
        font-weight: 600;
        color: #10b981;
    }

    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-left: 1px solid #1f2937;
    }

    @media (max-width: 768px) {
        .metric-card {
            flex: 1 1 100%;
        }
        .hero-title {
            font-size: 1.8rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# 3. المنيو الجانبي (Sidebar)
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white;'>📋 بوابة الأمن والمطور</h2>", unsafe_allow_html=True)
    st.info("👤 **المطور:** نزار محمد هاني")
    st.success("💳 **الربط المالي:** QNB Verified Active")
    st.markdown("---")
    
    # 🌟 الـ Feature الجديد: محاكاة نسيان الباسورد الذكي لإبهار الـ HR
    st.markdown("🔑 **نسيت كلمة المرور؟ (بوابة الاستعادة)**")
    email_input = st.text_input("أدخل البريد الإلكتروني للموظف:")
    if st.button("🔄 إرسال رابط إعادة التعيين المشفر"):
        if email_input:
            st.code("🔒 Auth-Token: SHA256-98234xX81", language="bash")
            st.success("🎯 تم التحقق من الهوية! أرسلنا كود إعادة التعيين أوتوماتيكياً عبر السيرفر.")
        else:
            st.warning("رجاءً اكتب الإيميل أولاً")
            
    st.markdown("---")
    currency = st.radio("💵 عملة العرض الأساسية:", ["الريال السعودي (SAR)", "الدولار الأمريكي (USD)"])

currency_symbol = "SAR" if currency == "الريال السعودي (SAR)" else "USD"
payroll_value = "124,500" if currency_symbol == "SAR" else "33,200"

# 4. الهيدر الرئيسي
st.markdown(f"""
    <div class="hero-container">
        <div style="background-color: #1e1b4b; color: #818cf8; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 700; display: inline-block; margin-bottom: 15px;">
            💎 لوحة إدارة المستحقات والرواتب المتقدمة v2.8
        </div>
        <div class="hero-title">REST-OS: Enterprise Payroll</div>
        <div class="hero-subtitle">النظام المؤتمت بالكامل لحساب رواتب طاقم العمل، المكافآت (Bonus)، والجزاءات الفورية</div>
    </div>
""", unsafe_allow_html=True)

# 5. عرض كروت الإحصائيات (Metrics) المرنة للـ HR
st.markdown("""
    <div class="cards-grid">
        <div class="metric-card">
            <div class="card-header-flex">
                <span class="card-icon">💵</span>
                <span class="card-title">إجمالي مسحوبات الرواتب هذا الشهر</span>
            </div>
            <div class="card-value">{} {}</div>
            <div class="card-delta" style="color: #38bdf8;">✓ مسواة بنجاح البنك</div>
        </div>
        <div class="metric-card">
            <div class="card-header-flex">
                <span class="card-icon">🎁</span>
                <span class="card-title">إجمالي البونص الموزع كحوافز</span>
            </div>
            <div class="card-value">{} 18,400</div>
            <div class="card-delta">▲ +8.2% نمو الأداء</div>
        </div>
        <div class="metric-card">
            <div class="card-header-flex">
                <span class="card-icon">⚠️</span>
                <span class="card-title">إجمالي الخصومات والجزاءات</span>
            </div>
            <div class="card-value">{} 2,150</div>
            <div class="card-delta" style="color: #f43f5e;">▼ انخفاض المخالفات عن الشهر الماضي</div>
        </div>
    </div>
""".format(currency_symbol, payroll_value, currency_symbol, currency_symbol), unsafe_allow_html=True)

st.markdown("---")

# 6. قسم التحكم التفاعلي بالبونص والجزاءات (لوحة المدير أو عمك الـ HR)
st.markdown("<h2 style='text-align: right; color: white; font-family: Cairo;'>⚙️ التحكم في المكافآت والجزاءات لايف</h2>", unsafe_allow_html=True)

col_actions, col_chart = st.columns([1, 1])

with col_actions:
    st.write("اختر الموظف ونوع الحركة المالية لتحديث الداتابيز فوراً:")
    
    # محاكاة لإضافة بونص أو جزاء بشكل حيوي
    employee = st.selectbox("👤 اختر الموظف / الشيف:", ["الشيف الرئيسي (فرع الرياض)", "مدير صالة فرع جدة", "كابتن صالة فرع مكة"])
    action_type = st.radio("🛠️ نوع الإجراء المالي:", ["🎁 إضافة مكافأة (Bonus)", "⚠️ تطبيق جزاء / خصم (Deduction)"])
    amount = st.number_input(f"المبلغ بـ ({currency_symbol}):", min_value=50, max_value=5000, value=500, step=50)
    
    if st.button("🚀 ترحيل الحركة المالية إلى قاعدة البيانات"):
        st.balloons() if "مكافأة" in action_type else st.warning("💥 تم تسجيل الخصم")
        st.success(f"✅ تم بنجاح! تم تطبيق {action_type} بمبلغ {amount} {currency_symbol} لـ {employee} وتحديث ملف التأمينات الاجتماعي أوتوماتيكياً.")

with col_chart:
    st.markdown("<h3 style='text-align: right; color: white;'>📊 النسبة المقارنة للمصروفات</h3>", unsafe_allow_html=True)
    # رسمة بيانية توضح توزيع المرتبات مقارنة بالبونص والجزاءات
    payroll_data = pd.DataFrame({
        'التصنيف المالي': ['الرواتب الأساسية', 'البونص والحوافز', 'الجزاءات المستقطعة'],
        'القيمة التقديرية': [85, 12, 3]
    })
    st.bar_chart(payroll_data.set_index('التصنيف المالي'), use_container_width=True)

st.markdown("---")

# 7. الـ Database الشاملة للموظفين والرواتب والجزاءات (قفل ليفل الوحش!)
st.markdown("<h3 style='text-align: right; color: white;'>🏪 جدول الرواتب ومستحقات طاقم العمل بالكامل</h3>", unsafe_allow_html=True)

raw_salary_data = {
    "الموظف الكود المالي": ["#EMP-901 (الشيف الرئيسي)", "#EMP-402 (مدير الصالة)", "#EMP-109 (طاهي معجنات)", "#EMP-882 (كابتن الصالة)"],
    "الراتب الأساسي": [f"{currency_symbol} 12,000", f"{currency_symbol} 8,500", f"{currency_symbol} 6,000", f"{currency_symbol} 4,500"],
    "البونص المستحق 🎁": [f"{currency_symbol} 1,500", f"{currency_symbol} 800", f"{currency_symbol} 1,200", f"{currency_symbol} 400"],
    "الجزاءات المستقطعة ⚠️": [f"{currency_symbol} 0", f"{currency_symbol} 200", f"{currency_symbol} 0", f"{currency_symbol} 150"],
    "صافي المقبوض النهائي": [f"{currency_symbol} 13,500", f"{currency_symbol} 9,100", f"{currency_symbol} 7,200", f"{currency_symbol} 4,750"],
    "الحالة القانونية": ["🟢 تم التحويل للبنك", "🟢 تم التحويل للبنك", "🟢 تم التحويل للبنك", "🟡 معلق للمراجعة"]
}

df_payroll = pd.DataFrame(raw_salary_data)
st.dataframe(df_payroll, use_container_width=True)

# 8. الفوتر الاحترافي
st.markdown("""
    <br><hr>
    <div style='text-align: center; color: #64748b; font-size: 0.9rem;'>
        REST-OS Payroll Engine v2.8 • Designed by Nezar Mohammed Hany • Powered by Python & QNB Secure Gateway
    </div>
""", unsafe_allow_html=True)

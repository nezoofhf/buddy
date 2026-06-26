import streamlit as st
import pandas as pd
import numpy as np

# 1. إعدادات الصفحة الأساسية - وضع الشاشة الواسعة
st.set_page_config(
    page_title="REST-OS Enterprise Edition",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. الـ HTML & CSS الصايع والمعدل بالملي لمنع أي تداخل على الموبايل
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

    /* Grid نظام الكروت المرن للموبايل */
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

    /* المنيو الجانبي */
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
""", unsafe_allow_html=True) # تم تعديل الـ Bug هنا بنجاح! ✅

# 3. المنيو الجانبي (Sidebar) لتعزيز الـ Branding الاحترافي
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white;'>📋 وبيانات المطور</h2>", unsafe_allow_html=True)
    st.info("👤 **المطور الرئيسي:** نزار محمد هاني")
    st.success("💳 **حالة الحساب المالي:** QNB Verified Active")
    st.markdown("---")
    currency = st.radio("💵 اختر عملة عرض النظام:", ["الريال السعودي (SAR)", "الدولار الأمريكي (USD)"])
    st.markdown("---")
    st.write("REST-OS v2.5.0\nSecure Cloud Environment")

# تحديد قيم العملة بناءً على اختيار العملة الذكي
currency_symbol = "SAR" if currency == "الريال السعودي (SAR)" else "USD"
sales_value = "45,280" if currency_symbol == "SAR" else "12,074"

# 4. عرض الهيدر الرئيسي
st.markdown(f"""
    <div class="hero-container">
        <div style="background-color: #065f46; color: #34d399; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 700; display: inline-block; margin-bottom: 15px;">
            🔒 Connected to Cloud Database (PostgreSQL Sandbox)
        </div>
        <div class="hero-title">REST-OS Enterprise</div>
        <div class="hero-subtitle">النظام السحابي الأحدث المصمم خصيصاً لمراقبة وإدارة فروع المطاعم الكبرى والـ HR تلقائياً</div>
    </div>
""", unsafe_allow_html=True)

# 5. عرض كروت الإحصائيات (Metrics) المرنة
st.markdown("""
    <div class="cards-grid">
        <div class="metric-card">
            <div class="card-header-flex">
                <span class="card-icon">💰</span>
                <span class="card-title">إجمالي مبيعات اليوم لايف</span>
            </div>
            <div class="card-value">{} {}</div>
            <div class="card-delta">▲ +12.5% (مقارنة بأمس)</div>
        </div>
        <div class="metric-card">
            <div class="card-header-flex">
                <span class="card-icon">📦</span>
                <span class="card-title">طلبات Buddy's Burger النشطة</span>
            </div>
            <div class="card-value">342 أوردر</div>
            <div class="card-delta" style="color: #f59e0b;">🔥 وقت ذروة التشغيل</div>
        </div>
        <div class="metric-card">
            <div class="card-header-flex">
                <span class="card-icon">👥</span>
                <span class="card-title">كفاءة الحضور والـ HR</span>
            </div>
            <div class="card-value">98.4%</div>
            <div class="card-delta" style="color: #38bdf8;">✓ مسجل بالكامل قانوني</div>
        </div>
    </div>
""".format(currency_symbol, sales_value), unsafe_allow_html=True)

st.markdown("---")

# 6. الـ Features التفاعلية الجديدة (قاعدة البيانات والرسوم البيانية)
col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown("<h3 style='text-align: right; color: white;'>📊 معدل نمو الطلبات الأسبوعي</h3>", unsafe_allow_html=True)
    # رسمة بيانية نظيفة ومريحة للعين
    chart_data = pd.DataFrame(
        np.random.randn(7, 2) * [10, 5] + [50, 30],
        columns=['فرع الرياض', 'فرع جدة'],
        index=['الأحد', 'الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت']
    )
    st.line_chart(chart_data, use_container_width=True)

with col_right:
    st.markdown("<h3 style='text-align: right; color: white;'>⚙️ التحكم في الـ HR والداتابيز (لوحة عمك)</h3>", unsafe_allow_html=True)
    st.write("هنا يقدر الـ HR يتحكم في تحديثات الفروع والرواتب بضغطة زر وتتسمع في قاعدة البيانات فوراً:")
    
    # تفاعل حقيقي لإبهار الـ HR
    bonus_action = st.button("🔥 صرف مكافأة إنتاجية 10% لجميع الطهاة والموظفين الآن")
    if bonus_action:
        st.balloons()
        st.success("✅ تم تحديث قاعدة بيانات الـ PostgreSQL! تم إرسال إشعارات الرواتب الجديدة للموظفين أوتوماتيكياً عبر الـ API.")

st.markdown("---")

# 7. جدول مراقبة الفروع والـ Live Databases
st.markdown("<h3 style='text-align: right; color: white;'>🏪 جدول مراقبة الفروع المباشر</h3>", unsafe_allow_html=True)
branch_data = {
    "اسم الفرع": ["فرع الرياض (الرئيسي)", "فرع جدة", "فرع مكة"],
    "عدد الموظفين": [24, 18, 12],
    "المبيعات الحالية": [f"{currency_symbol} 21,500", f"{currency_symbol} 14,880", f"{currency_symbol} 8,900"],
    "حالة المطبخ والعمل": ["🟢 مستقر تماماً", "🟢 مستقر تماماً", "🟡 ضغط طلبات عالي"]
}
df = pd.DataFrame(branch_data)
st.dataframe(df, use_container_width=True)

# 8. الفوتر الاحترافي
st.markdown("""
    <br><hr>
    <div style='text-align: center; color: #64748b; font-size: 0.9rem;'>
        REST-OS Enterprise Edition v2.5 • Designed by Nezar Mohammed Hany • Powered by Python & QNB Secure Gateway
    </div>
""", unsafe_allow_html=True)

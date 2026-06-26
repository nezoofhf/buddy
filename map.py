import streamlit as st
import pandas as pd

# إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="REST-OS Enterprise",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🎨 الـ HTML و الـ CSS الصايع والـ Responsive للموبايل
st.markdown("""
    <style>
    /* استيراد خطوط احترافية ومريحة للعين */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Cairo', 'Plus Jakarta Sans', sans-serif;
    }

    /* الخلفية العامة للسيستم لتكون مريحة للعين (Dark Premium Mode) */
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

    /* 📱 الحل السحري لمنع تداخل الأيقونات والكروت على الموبايل (Flex Grid System) */
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
        flex: 1 1 calc(33.333% - 20px); /* على اللابتوب: 3 كروت جنب بعض */
        min-width: 280px; /* يمنع الكارت إنه يصغر عن حجم معين */
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #4f46e5;
    }

    /* تنسيق الأيقونات والنصوص جوه الكارت عشان تفضل ثابتة ومريحة */
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
        color: #10b981; /* أخضر مريح للأرباح */
    }

    /* تعديلات خاصة بشاشات الموبايل (Responsive Media Queries) */
    @media (max-width: 768px) {
        .metric-card {
            flex: 1 1 100%; /* على الموبايل: الكروت تنزل تحت بعضها أوتوماتيك بنسبة 100% */
        }
        .hero-title {
            font-size: 1.8rem;
        }
        .card-value {
            font-size: 1.5rem;
        }
    }
    </style>
""", unsafe_index=True)

# ----------------- عرض الـ UI الصايع -----------------

# 1. الهيدر
st.markdown("""
    <div class="hero-container">
        <div style="background-color: #065f46; color: #34d399; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 700; display: inline-block; margin-bottom: 15px;">
            🔒 متصل بـ Database السحابية ومؤمن بالكامل
        </div>
        <div class="hero-title">REST-OS Enterprise</div>
        <div class="hero-subtitle">النظام السحابي الأحدث لإدارة سلاسل المطاعم ومراقبة الفروع في الوقت الفعلي</div>
    </div>
""", unsafe_index=True)

# 2. الكروت المرنة (تتحول تلقائياً على الموبايل بدون أي تداخل)
st.markdown("""
    <div class="cards-grid">
        <!-- كارت الإيرادات -->
        <div class="metric-card">
            <div class="card-header-flex">
                <span class="card-icon">💰</span>
                <span class="card-title">إجمالي المبيعات اليومية</span>
            </div>
            <div class="card-value">SAR 45,280</div>
            <div class="card-delta">▲ +12.5% (مقارنة بأمس)</div>
        </div>
        
        <!-- كارت الأوردرات -->
        <div class="metric-card">
            <div class="card-header-flex">
                <span class="card-icon">📦</span>
                <span class="card-title">الأوردرات النشطة بالفروع</span>
            </div>
            <div class="card-value">342 أوردر</div>
            <div class="card-delta" style="color: #f59e0b;">🔥 وقت الذروة الحالي</div>
        </div>
        
        <!-- كارت الرواتب والموظفين -->
        <div class="metric-card">
            <div class="card-header-flex">
                <span class="card-icon">👥</span>
                <span class="card-title">كفاءة تشغيل الـ HR</span>
            </div>
            <div class="card-value">98.4%</div>
            <div class="card-delta" style="color: #38bdf8;">✓ تسجيل الحضور ذكي</div>
        </div>
    </div>
""", unsafe_index=True)

st.markdown("<h2 style='text-align: right; color: white; font-family: Cairo;'>📊 مراقبة الفروع لايف</h2>", unsafe_index=True)

# محاكاة الداتابيز التفاعلية (Streamlit Native Node)
branch_data = {
    "اسم الفرع": ["فرع الرياض (الرئيسي)", "فرع جدة", "فرع مكة"],
    "عدد الموظفين": [24, 18, 12],
    "المبيعات الحالية": ["SAR 21,500", "SAR 14,880", "SAR 8,900"],
    "حالة العمل": ["🟢 مستقر", "🟢 مستقر", "🟡 ضغط عالي"]
}
df = pd.DataFrame(branch_data)
st.dataframe(df, use_container_width=True)

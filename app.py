import streamlit as st

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Wine Quality Dashboard",
    page_icon="🍷",
    layout="wide"
)

# =========================
# 🎨 GLOBAL STYLE
# =========================
st.markdown("""
<style>

/* ===== MAIN BACKGROUND ===== */
.stApp {
    background: linear-gradient(180deg, #FBF2F3, #F7E6E9);
}

/* ===== SIDEBAR BACKGROUND ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #7A1F2B, #A63A50);
    padding-top: 24px;
}

/* Sidebar text */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    color: white !important;
    font-weight: 600;
}

/* ===== RADIO NAV STYLE ===== */
div[role="radiogroup"] > label {
    background: rgba(255,255,255,0.12);
    padding: 12px 16px;
    margin-bottom: 10px;
    border-radius: 14px;
    cursor: pointer;
    transition: all 0.25s ease;
    border: 1px solid rgba(255,255,255,0.15);
}

/* Hover effect */
div[role="radiogroup"] > label:hover {
    background: rgba(255,255,255,0.25);
    transform: translateX(4px);
}

/* Selected item */
div[role="radiogroup"] > label[data-selected="true"] {
    background: white !important;
    color: #7A1F2B !important;
    font-weight: 700;
}

/* ===== HERO SHADOW ===== */
.hero-card {
    box-shadow: 0 12px 28px rgba(0,0,0,0.18);
}

/* ===== GENERAL CARD SHADOW ===== */
.card {
    box-shadow: 0 8px 20px rgba(0,0,0,0.12);
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
st.sidebar.markdown("## 🍷 Navigation")
st.sidebar.markdown(
    "<small style='opacity:0.85;'>by : <b>Daffa Rizqi Arinjaya</b></small>",
    unsafe_allow_html=True
)

menu = st.sidebar.radio(
    "",
    [
        "📊 About Dataset",
        "📈 Dashboard",
        "🤖 Machine Learning",
        "🔮 Prediction App",
        "📬 Contact Me"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="color:white;">
    <b>Wine Quality Prediction</b><br>
    <small>Final Project 2.0</small>
</div>
""", unsafe_allow_html=True)

# =========================
# HERO HEADER
# =========================
st.markdown("""
<div class="hero-card" style="
    background: linear-gradient(90deg, #8C2F39, #B44A55);
    padding: 32px;
    border-radius: 22px;
    color: white;
    margin-bottom: 28px;
">
    <h1 style="margin-bottom:6px;">🍷 Wine Quality Prediction</h1>
    <p style="font-size:18px; margin-bottom:4px;">
        Final Project 2.0 — Data Analyst & Data Science
    </p>
    <small>Jakarta, 12 Januari 2026</small>
</div>
""", unsafe_allow_html=True)

# =========================
# CONTENT ROUTING
# =========================
if menu == "📊 About Dataset":
    import about
    about.about_dataset()

elif menu == "📈 Dashboard":
    import visualisasi
    visualisasi.chart()

elif menu == "🤖 Machine Learning":
    import machine_learning
    machine_learning.ml_model()

elif menu == "🔮 Prediction App":
    import prediction
    prediction.prediction_app()

elif menu == "📬 Contact Me":
    import kontak
    kontak.contact_me()

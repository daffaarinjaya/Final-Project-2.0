import streamlit as st
import pandas as pd
import plotly.express as px


def chart():

    # =========================
    # 🌷 GLOBAL STYLE
    # =========================
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #FFF7F8, #F6E4E7);
    }

    h1 {
        font-size: 40px;
        font-weight: 800;
        color: #6E1F2A;
        margin-bottom: 6px;
    }

    h3 {
        color: #8C2F39;
        font-weight: 700;
    }

    .subtitle {
        color: #7A4A52;
        font-size: 18px;
        margin-bottom: 36px;
    }

    /* ================= KPI ================= */
    .kpi-card {
        background: linear-gradient(145deg, #B23A48, #D16C7C);
        padding: 24px;
        border-radius: 24px;
        text-align: center;
        color: white;
        box-shadow: 0 18px 40px rgba(178,58,72,0.35);
        transition: all 0.35s ease;
    }

    .kpi-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 26px 55px rgba(178,58,72,0.45);
    }

    .kpi-title {
        font-size: 13px;
        letter-spacing: 1.5px;
        opacity: 0.9;
    }

    .kpi-value {
        font-size: 40px;
        font-weight: 800;
        margin-top: 8px;
    }

    /* ================= GLASS ================= */
    .glass {
        background: rgba(255,255,255,0.45);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 26px;
        padding: 22px;
        box-shadow: 0 18px 40px rgba(0,0,0,0.10);
        margin-bottom: 14px;
    }

    /* ================= INSIGHT ================= */
    .insight {
        background: linear-gradient(135deg, #FBE4E8, #F3C6CC);
        padding: 16px 22px;
        border-radius: 18px;
        box-shadow: 0 10px 26px rgba(178,58,72,0.22);
        border-left: 6px solid #B23A48;
        margin-bottom: 26px;
        color: #6E1F2A;
        font-size: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

    # =========================
    # 📂 LOAD DATA
    # =========================
    df = pd.read_csv("Wine Quality Dataset.csv")
    kpi = df["quality"].value_counts().to_dict()

    # =========================
    # 🎨 COLOR THEME
    # =========================
    WINE_MAIN = "#B23A48"
    WINE_PALETTE = [
        "#8C2F39", "#B23A48", "#C95A69",
        "#D16C7C", "#E59AA5", "#F3C6CC"
    ]

    # =========================
    # 🧾 HEADER
    # =========================
    st.markdown("<h1>🍷 Wine Quality Dashboard</h1>", unsafe_allow_html=True)
    st.markdown(
        "<div class='subtitle'>Analisis visual kualitas wine berdasarkan karakteristik kimia</div>",
        unsafe_allow_html=True
    )

    # =========================
    # 📊 KPI SECTION (TANPA INSIGHT)
    # =========================
    cols = st.columns(6)
    for col, q in zip(cols, [3, 4, 5, 6, 7, 8]):
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">QUALITY {q}</div>
                <div class="kpi-value">{kpi.get(q, 0)}</div>
            </div>
            """, unsafe_allow_html=True)

    # =========================
    # 📈 ROW 1
    # =========================
    col1, col2 = st.columns(2)

    # ---------- BOXPLOT ----------
    with col1:
        fig1 = px.box(
            df, x="quality", y="alcohol",
            title="Kadar Alkohol Berdasarkan Kualitas Wine",
            color_discrete_sequence=[WINE_MAIN]
        )
        fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="insight">
        🍷 Wine dengan kualitas lebih tinggi cenderung memiliki <b>kadar alkohol yang lebih tinggi</b>, 
        sehingga alkohol menjadi salah satu faktor penting dalam penilaian kualitas wine.
        </div>
        """, unsafe_allow_html=True)

    # ---------- SCATTER ----------
    with col2:
        fig2 = px.scatter(
            df, x="pH", y="quality",
            title="Hubungan pH terhadap Kualitas Wine",
            color_discrete_sequence=[WINE_MAIN]
        )
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="insight">
        🍷 Kualitas wine umumnya berada pada <b>rentang pH menengah</b>, 
        sementara nilai pH yang terlalu rendah atau tinggi cenderung menurunkan kualitas.
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # 📉 ROW 2
    # =========================
    alcohol_bins = pd.cut(
        df["alcohol"],
        bins=[0, 9, 11, 13, 20],
        labels=["Rendah", "Sedang", "Tinggi", "Sangat Tinggi"]
    )
    avg_quality = df.groupby(alcohol_bins)["quality"].mean().reset_index()

    col3, col4 = st.columns([1, 1.2])

    # ---------- BAR ----------
    with col3:
        fig3 = px.bar(
            avg_quality, x="alcohol", y="quality",
            title="Rata-rata Kualitas Wine Berdasarkan Level Alkohol",
            color_discrete_sequence=[WINE_MAIN]
        )
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="insight">
        🍷 Wine dengan level alkohol <b>tinggi hingga sangat tinggi</b> memiliki rata-rata kualitas yang lebih baik,
        menunjukkan adanya hubungan positif antara alkohol dan kualitas wine.
        </div>
        """, unsafe_allow_html=True)

    # ---------- PIE ----------
    with col4:
        qc = df["quality"].value_counts().sort_index()
        fig4 = px.pie(
            values=qc.values,
            names=qc.index,
            title="Distribusi Kualitas Wine",
            color_discrete_sequence=WINE_PALETTE
        )
        fig4.update_traces(
            textinfo="percent+label",
            pull=[0.06 if q == 6 else 0 for q in qc.index]
        )
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)")
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="insight">
        🍷 Sebagian besar wine berada pada <b>kualitas 5–6</b>, menandakan kualitas yang stabil,
        sedangkan wine dengan kualitas sangat rendah atau sangat tinggi jumlahnya relatif sedikit.
        </div>
        """, unsafe_allow_html=True)

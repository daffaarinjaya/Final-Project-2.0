import streamlit as st
import pandas as pd
import joblib


def prediction_app():

    # =========================
    # 🎨 RED WINE THEME
    # =========================
    WINE_MAIN = "#A63A50"
    WINE_SOFT = "#F8E6E9"

    st.markdown(f"""
    <style>
    .card {{
        background-color: {WINE_SOFT};
        padding: 22px;
        border-radius: 16px;
        border-left: 8px solid {WINE_MAIN};
        margin-bottom: 20px;
    }}
    .card-title {{
        color: {WINE_MAIN};
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 10px;
    }}
    .result-card {{
        background: linear-gradient(135deg, {WINE_MAIN}, #C94A5A);
        padding: 26px;
        border-radius: 18px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 18px rgba(0,0,0,0.25);
    }}
    .result-score {{
        font-size: 36px;
        font-weight: 800;
        margin-top: 6px;
    }}
    </style>
    """, unsafe_allow_html=True)

    # =========================
    # HEADER
    # =========================
    st.header("🍷 Wine Quality Prediction App (Ridge Regression)")
    st.write(
        "Masukkan karakteristik kimia wine untuk memprediksi "
        "kualitas menggunakan **Ridge Regression Model**."
    )

    # =========================
    # INPUT FEATURES
    # =========================
    st.subheader("🧪 Input Fitur Wine")

    col1, col2 = st.columns(2)

    with col1:
        fixed_acidity = st.number_input("Fixed Acidity", 0.0, 20.0, 7.4)
        volatile_acidity = st.number_input("Volatile Acidity", 0.0, 5.0, 0.7)
        citric_acid = st.number_input("Citric Acid", 0.0, 5.0, 0.0)
        residual_sugar = st.number_input("Residual Sugar", 0.0, 20.0, 1.9)
        chlorides = st.number_input("Chlorides", 0.0, 1.0, 0.076)

    with col2:
        free_sulfur_dioxide = st.number_input("Free Sulfur Dioxide", 0.0, 100.0, 11.0)
        total_sulfur_dioxide = st.number_input("Total Sulfur Dioxide", 0.0, 300.0, 34.0)
        sulphates = st.number_input("Sulphates", 0.0, 2.0, 0.56)
        alcohol = st.number_input("Alcohol (%)", 5.0, 20.0, 9.4)

    # =========================
    # PREDICT BUTTON
    # =========================
    if st.button("🍷 Predict Wine Quality"):

        input_data = pd.DataFrame({
            "fixed acidity": [fixed_acidity],
            "volatile acidity": [volatile_acidity],
            "citric acid": [citric_acid],
            "residual sugar": [residual_sugar],
            "chlorides": [chlorides],
            "free sulfur dioxide": [free_sulfur_dioxide],
            "total sulfur dioxide": [total_sulfur_dioxide],
            "sulphates": [sulphates],
            "alcohol": [alcohol]
        })

        # =========================
        # LOAD MODEL
        # =========================
        feature_columns = joblib.load("feature_columns.joblib")
        scaler = joblib.load("scaler.joblib")
        model = joblib.load("ridge_model.joblib")

        input_data = input_data[feature_columns]
        input_scaled = scaler.transform(input_data)

        # =========================
        # PREDICTION
        # =========================
        score = float(model.predict(input_scaled)[0])
        rounded_score = int(round(score))

        quality_mapping = {
            3: "Low",
            4: "Below Average",
            5: "Average",
            6: "Good",
            7: "Very Good",
            8: "Excellent"
        }

        quality_label = quality_mapping.get(rounded_score, "Unknown")

        # =========================
        # RESULT CARD
        # =========================
        st.markdown(f"""
        <div class="result-card">
            <div style="font-size:18px;">Predicted Wine Quality</div>
            <div class="result-score">{quality_label}</div>
            <div style="margin-top:8px;">Predicted Score: <b>{score:.2f}</b></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <div class="card-title">📌 Interpretasi Hasil</div>
            <ul>
                <li>Model memprediksi kualitas wine pada skor <b>{score:.2f}</b>.</li>
                <li>Nilai ini paling dekat dengan kualitas <b>{rounded_score}</b>.</li>
                <li>Berdasarkan pemetaan kualitas, wine ini tergolong <b>{quality_label}</b>.</li>
                <li>Prediksi dihasilkan menggunakan <b>Ridge Regression</b> untuk menjaga stabilitas model.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    prediction_app()

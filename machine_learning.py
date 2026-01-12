import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import math

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score
from statsmodels.stats.outliers_influence import variance_inflation_factor

import joblib


def ml_model():

    # ======================================================
    # 🎨 RED WINE THEME
    # ======================================================
    WINE_MAIN = "#A63A50"
    WINE_GRADIENT = "#C94A5A"
    WINE_SOFT = "#F8E6E9"

    st.markdown(f"""
    <style>
    .card {{
        background-color: {WINE_SOFT};
        padding: 22px;
        border-radius: 18px;
        border-left: 8px solid {WINE_MAIN};
        margin-bottom: 24px;
    }}
    .card-title {{
        color: {WINE_MAIN};
        font-weight: 700;
        font-size: 18px;
        margin-bottom: 10px;
    }}
    .metric-card {{
        background: linear-gradient(135deg, {WINE_MAIN}, {WINE_GRADIENT});
        padding: 20px;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 6px 16px rgba(0,0,0,0.2);
    }}
    .metric-value {{
        font-size: 32px;
        font-weight: 800;
    }}
    hr {{
        border: none;
        height: 4px;
        background-color: {WINE_MAIN};
        border-radius: 6px;
        margin: 28px 0;
    }}
    </style>
    """, unsafe_allow_html=True)

    # ======================================================
    # 🏷️ HEADER
    # ======================================================
    st.header("🍷 Machine Learning – Wine Quality Prediction")
    st.write(
        "Analisis Machine Learning untuk memprediksi kualitas wine "
        "berdasarkan kandungan kimia menggunakan Linear, Ridge, dan Lasso Regression."
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    # ======================================================
    # 1️⃣ LOAD DATA
    # ======================================================
    df = pd.read_csv("Wine Quality Dataset.csv")
    df = df.drop(columns="alcohol_level")

    numeric_cols = df.select_dtypes(include="number").columns

    # ======================================================
    # 2️⃣ OUTLIER DETECTION (IQR)
    # ======================================================
    st.subheader("1️⃣ Deteksi dan Penanganan Outlier (IQR Method)")

    Q1 = df[numeric_cols].quantile(0.25)
    Q3 = df[numeric_cols].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            Sebelum Outlier
            <div class="metric-value">{df.shape[0]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        df = df[~((df[numeric_cols] < lower) | (df[numeric_cols] > upper)).any(axis=1)]
        st.markdown(f"""
        <div class="metric-card">
            Setelah Outlier
            <div class="metric-value">{df.shape[0]}</div>
        </div>
        """, unsafe_allow_html=True)

    # ======================================================
    # 3️⃣ DATASET PREVIEW
    # ======================================================
    st.subheader("2️⃣ Dataset yang Digunakan")
    st.dataframe(df.head())

    # ======================================================
    # 4️⃣ CORRELATION HEATMAP
    # ======================================================
    st.subheader("3️⃣ Korelasi Linear Antar Fitur")

    corr = df[numeric_cols].corr().round(2)

    fig_corr = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale=["#FADADD", WINE_MAIN],
        height=800,
        title="Correlation Heatmap"
    )

    # 🔥 HANYA BAGIAN INI YANG DIUBAH
    fig_corr.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",   # background luar transparan
        plot_bgcolor="rgba(0,0,0,0)",    # background dalam transparan
        font=dict(color="white")         # biar kontras di dark theme
    )

    st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown("""
    <div class="card">
        <div class="card-title">📌 Insight Korelasi</div>
        <ul>
            <li><b>Alcohol</b> memiliki korelasi positif terkuat terhadap kualitas wine.</li>
            <li><b>Volatile Acidity</b> berkorelasi negatif terhadap kualitas.</li>
            <li><b>Density</b> menurun seiring meningkatnya alkohol.</li>
            <li><b>Sulphates</b> berkontribusi positif namun tidak dominan.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ======================================================
    # 5️⃣ VIF
    # ======================================================
    st.subheader("4️⃣ Multikolinearitas (VIF)")

    vif_df = pd.DataFrame({
        "Feature": numeric_cols,
        "VIF": [
            variance_inflation_factor(df[numeric_cols].values, i)
            for i in range(len(numeric_cols))
        ]
    })

    st.dataframe(vif_df)

    # ======================================================
    # 6️⃣ STANDARDIZATION & SPLIT
    # ======================================================
    st.subheader("5️⃣ Standardisasi dan Split Data")

    X = df.drop(["quality", "density", "pH"], axis=1)
    y = df["quality"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    st.write(f"Train data: {len(X_train)} | Test data: {len(X_test)}")

    # ======================================================
    # 7️⃣ LINEAR REGRESSION
    # ======================================================
    st.subheader("6️⃣ Linear Regression")

    lr = LinearRegression()
    lr.fit(X_train, y_train)

    coef_lr = pd.DataFrame({
        "Feature": X.columns,
        "Coefficient": lr.coef_
    })

    st.dataframe(coef_lr)

    # ======================================================
    # 7️⃣ LINEAR REGRESSION
    # ======================================================
    st.subheader("6️⃣ Linear Regression")

    lr = LinearRegression()
    lr.fit(X_train, y_train)

    def evaluate_model(y_true, y_pred):
        return {
            "MAE": np.mean(np.abs(y_true - y_pred)),
            "MSE": mean_squared_error(y_true, y_pred),
            "RMSE": math.sqrt(mean_squared_error(y_true, y_pred)),
            "R²": r2_score(y_true, y_pred)
        }

    lr_metrics = evaluate_model(y_test, lr.predict(X_test))
    st.dataframe(pd.DataFrame(lr_metrics, index=[0]))

    st.markdown("""
    <div class="card">
        <div class="card-title">📌 Insight Linear Regression</div>
        <ul>
            <li>Nilai <b>MAE</b> sebesar ~0.46 menunjukkan bahwa semakin kecil MAE, semakin akurat prediksi model.</li>
            <li>Nilai <b>MSE</b> sebesar ~0.33 menandakan bahwa kesalahan besar lebih sering terjadi.</li>
            <li><b>RMSE</b> sebesar ~0.58 menunjukkan performa prediksi sedikit lebih buruk.</li>
            <li>Nilai <b>R²</b> sebesar ~0.35 menunjukkan bahwa model menjelaskan sekitar 35% variasi target.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ======================================================
    # 8️⃣ HYPERPARAMETER TUNING
    # ======================================================
    st.subheader("7️⃣ Hyperparameter Tuning (Ridge & Lasso)")

    alphas = np.logspace(-3, 3, 20)

    ridge_grid = GridSearchCV(
        Ridge(),
        {"alpha": alphas},
        cv=10,
        scoring="neg_mean_squared_error"
    )
    ridge_grid.fit(X_train, y_train)

    lasso_grid = GridSearchCV(
        Lasso(max_iter=5000),
        {"alpha": alphas},
        cv=10,
        scoring="neg_mean_squared_error"
    )
    lasso_grid.fit(X_train, y_train)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            Best Alpha Ridge
            <div class="metric-value">{ridge_grid.best_params_['alpha']:.4f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            Best Alpha Lasso
            <div class="metric-value">{lasso_grid.best_params_['alpha']:.4f}</div>
        </div>
        """, unsafe_allow_html=True)

    # ======================================================
    # 9️⃣ COEFFICIENT COMPARISON
    # ======================================================
    st.subheader("8️⃣ Koefisien Ridge & Lasso")

    ridge_best = Ridge(alpha=ridge_grid.best_params_["alpha"])
    lasso_best = Lasso(alpha=lasso_grid.best_params_["alpha"], max_iter=5000)

    ridge_best.fit(X_train, y_train)
    lasso_best.fit(X_train, y_train)

    coef_compare = pd.DataFrame({
        "Feature": X.columns,
        "Ridge Coef": ridge_best.coef_,
        "Lasso Coef": lasso_best.coef_
    })

    st.dataframe(coef_compare)

    # ======================================================
    # 🔟 MODEL EVALUATION
    # ======================================================
    st.subheader("9️⃣ Evaluasi Model")

    col1, col2 = st.columns(2)

    def evaluate_model(y_true, y_pred):
        return {
            "MAE": np.mean(np.abs(y_true - y_pred)),
            "MSE": mean_squared_error(y_true, y_pred),
            "RMSE": math.sqrt(mean_squared_error(y_true, y_pred)),
            "R²": r2_score(y_true, y_pred)
        }

    with col1:
        st.write("**Ridge Regression**")
        ridge_metrics = evaluate_model(y_test, ridge_best.predict(X_test))
        st.dataframe(pd.DataFrame(ridge_metrics, index=[0]))

        st.markdown(""" <div class="card-title">📌 Insight Ridge Regression</div>
        <div class="card">
            <li>Nilai <b>MAE</b> sebesar <b>~0.46</b> menunjukkan bahwa prediksi kualitas wine
                rata-rata meleset kurang dari setengah poin kualitas.</li>
            <li>Nilai <b>MSE</b> sebesar <b>~0.34</b> menandakan bahwa kesalahan kuadrat rata-rata
                dari prediksi cukup kecil, memperkuat keakuratan model.</li>
            <li><b>RMSE</b> sebesar <b>~0.58</b> menunjukkan bahwa deviasi standar dari kesalahan prediksi
                juga rendah, mengindikasikan konsistensi model.</li>
            <li><b>R²</b> sebesar <b>~0.35</b> mengindikasikan bahwa sekitar 35% variasi dalam
                kualitas wine dapat dijelaskan oleh fitur-fitur dalam model ini.</li>
            Secara keseluruhan,
            <b>Ridge menghasilkan error yang lebih kecil dan stabil.
            Semua fitur tetap dipertahankan sehingga cocok untuk prediksi kualitas wine.</b>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.write("**Lasso Regression**")
        lasso_metrics = evaluate_model(y_test, lasso_best.predict(X_test))
        st.dataframe(pd.DataFrame(lasso_metrics, index=[0]))

        st.markdown(""" <div class="card-title">📌 Insight Lasso Regression</div>
        <div class="card">
            <li>Nilai <b>MAE</b> sebesar <b>~0.46</b> menunjukkan bahwa prediksi kualitas wine
                rata-rata meleset lebih dari setengah poin kualitas.</li>
            <li>Nilai <b>MSE</b> sebesar <b>~0.33</b> menandakan bahwa kesalahan kuadrat rata-rata
                dari prediksi lebih besar dibanding Ridge, menunjukkan akurasi yang lebih rendah.</li>
            <li><b>RMSE</b> sebesar <b>~0.58</b> menunjukkan bahwa deviasi standar dari kesalahan prediksi
                juga lebih tinggi, mengindikasikan ketidakstabilan model.</li>
            <li><b>R²</b> sebesar <b>~0.35</b> mengindikasikan bahwa hanya sekitar 35% variasi dalam
                kualitas wine dapat dijelaskan oleh fitur-fitur dalam model ini.</li>
            Secara keseluruhan,
            <b>Lasso melakukan seleksi fitur namun performanya lebih rendah dibandingkan Ridge Regression.</b>
        </div>
        """, unsafe_allow_html=True)

    # ======================================================
    # 🔚 KESIMPULAN
    # ======================================================
    st.subheader("🔚 Kesimpulan")

    st.markdown("""
    <div class="card">
        <ul>
            <li><b>Ridge Regression</b> adalah model terbaik untuk prediksi kualitas wine.</li>
            <li><b>Alcohol</b> merupakan fitur paling berpengaruh.</li>
            <li><b>Lasso</b> efektif untuk seleksi fitur, namun kurang optimal untuk akurasi.</li>
            <li>Model siap digunakan dalam aplikasi prediksi.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

        # ======================================================
    # 📌 REKOMENDASI
    # ======================================================
    st.subheader("📌 Rekomendasi")

    st.markdown("""
    <div class="card">
        <ul>
            <li>
                Gunakan <b>Ridge Regression</b> sebagai model utama karena paling stabil 
                dan tahan terhadap masalah <i>multikolinearitas</i> antar fitur kimia.
            </li>
            <li>
                Fokus pada <b>optimasi faktor kimia utama</b>, khususnya 
                <b>alcohol, sulphates, dan volatile acidity</b> 
                karena memiliki pengaruh signifikan terhadap kualitas wine.
            </li>
            <li>
                Hindari kadar <b>volatile acidity</b> dan <b>chlorides</b> yang berlebihan 
                karena terbukti dapat <b>menurunkan kualitas wine secara signifikan</b>.
            </li>
            <li>
                Untuk pengembangan ke depan, pertimbangkan penggunaan 
                <b>model non-linear</b> (seperti Random Forest atau Gradient Boosting) 
                serta pemanfaatan <b>dashboard Streamlit</b> sebagai alat 
                <i>monitoring</i> dan <i>decision support system</i>.
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


    # ======================================================
    # 💾 SAVE MODEL
    # ======================================================
    joblib.dump(scaler, "scaler.joblib")
    joblib.dump(ridge_best, "ridge_model.joblib")
    joblib.dump(X.columns.tolist(), "feature_columns.joblib")

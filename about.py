import streamlit as st

def about_dataset():
    st.write('**Tentang Dataset**')
    col1, col2= st.columns([5,5])

    with col1:
        link = "https://www.foodandwine.com/thmb/TUMPSJTCx8iY_saBnDG1aPI7c4E=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Cabernet-Sauvignon-Grape-Guide-FT-BLOG0824-ebc9ac7522724d3c8db2b11f9c9feef8.jpg"
        st.image(link, caption="Wine Quality Dataset")

    with col2:
        st.write('Dataset ini digunakan untuk menganalisis faktor-faktor yang memengaruhi kualitas wine, ' \
        'serta memprediksi skor kualitas wine berdasarkan karakteristik fisik dan kimianya, ' \
        'seperti tingkat keasaman, kandungan alkohol, gula residual, ' \
        'dan kepadatan. Melalui analisis data dan pemodelan regresi, ' \
        'dataset ini membantu memahami hubungan antara komposisi wine dan kualitas sensorik, ' \
        'sehingga dapat digunakan sebagai dasar dalam evaluasi kualitas dan pengambilan keputusan berbasis data. ')

        
import streamlit as st

def contact_me():

    # Accent line (red wine)
    st.markdown(
        "<hr style='border:none;height:4px;background-color:#8C2F39;border-radius:4px;margin-bottom:16px;'>",
        unsafe_allow_html=True
    )

    st.subheader("📬 Contact Me")

    st.write(
        "Jika Anda memiliki pertanyaan atau ingin berdiskusi lebih lanjut, "
        "silakan hubungi saya melalui kontak berikut:"
    )

    # Contact info
    st.markdown("📧 **Email**  \n daffaarinjaya@gmail.com")
    st.markdown(
        "🔗 **LinkedIn**  \n "
        "[linkedin.com/in/daffa-rizqi-arinjaya]"
        "(https://www.linkedin.com/in/daffa-rizqi-arinjaya)"
    )
    st.markdown(
        "🐱 **GitHub**  \n "
        "[github.com/daffaarinjaya]"
        "(https://github.com/daffaarinjaya)"
    )

    st.write("---")

    st.write(
        "Saya terbuka untuk kolaborasi dan diskusi seputar "
        "**Data Science**, **Machine Learning**, dan **Data Analytics**. "
        "Terima kasih telah mengunjungi dashboard ini 🍷"
    )

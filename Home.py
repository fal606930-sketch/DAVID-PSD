import streamlit as st

st.set_page_config(
    page_title="Halaman Utama",
    layout="wide"
)

st.title("David Febrianto's Project Portfolio")
st.markdown("---")

# Tambahkan gambar Anda di sini. Ganti 'david.jpg' dengan nama file gambar Anda.
col1, col2 = st.columns([1, 2])
with col1:
    st.image("David.jpg", caption="Foto David Febrianto", width=300)
with col2:
    st.header("Selamat Datang di aplikasi web projek data saya!")
    st.header("**Nama:** David Febrianto")
    st.header("**NIM:** 230411100062")
st.header(
    """
    Untuk melihat proyek analisis data IMDB, silakan pilih **IMDB Dashboard** di bilah sisi (sidebar) di sebelah kiri.
    """
)

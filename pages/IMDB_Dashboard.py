import streamlit as st
import pandas as pd
import psycopg2
import csv

# Fungsi untuk memuat data dari file CSV dengan caching
@st.cache_data
def get_data_from_csv():
    try:
        df = pd.read_csv("IMDB_processed_data.csv", on_bad_lines='skip')
        df.columns = [col.lower() for col in df.columns]
        return df
    except FileNotFoundError:
        st.error("File 'IMDB_processed_data.csv' tidak ditemukan. Pastikan file berada di direktori yang sama.")
        return pd.DataFrame()

# Muat data dari file CSV
df = get_data_from_csv()

st.title("IMDB Eksplorasi Data & Pengecekan Kualitas")
st.markdown("Aplikasi ini melakukan analisis data dasar dari file `IMDB_processed_data.csv`.")

if not df.empty:
    # --- 1. Eksplorasi Data Awal ---
    st.header("1. Eksplorasi Data")
    
    st.subheader("DataFrame Head")
    st.dataframe(df.head())
    
    st.subheader("Informasi DataFrame (Tipe Data & Missing Values)")
    buffer = st.empty()
    buffer.text(df.info(buf=st.empty()))

    st.subheader("Statistik Deskriptif")
    st.dataframe(df.describe())

    st.markdown("---")
    # --- 2. Pembersihan & Konsistensi Data ---
    st.header("2. Pembersihan & Konsistensi Data")
    
    st.subheader("Konversi Runtime (Jam & Menit ke Menit)")
    def convert_runtime_to_minutes(runtime_str):
        if pd.isna(runtime_str):
            return None
        try:
            parts = runtime_str.split()
            total_minutes = 0
            for part in parts:
                if 'h' in part:
                    total_minutes += int(part.replace('h', '')) * 60
                elif 'm' in part:
                    total_minutes += int(part.replace('m', ''))
            return total_minutes
        except:
            return None

    df['runtime_minutes'] = df['runtime'].apply(convert_runtime_to_minutes)
    st.dataframe(df[['runtime', 'runtime_minutes']].head())

    st.markdown("---")
    # --- 3. Analisis Outlier (IQR) ---
    st.header("3. Analisis Outlier")

    st.subheader("Outlier pada Kolom Ratings")
    Q1 = df['ratings'].quantile(0.25)
    Q3 = df['ratings'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    st.write(f"Batas Bawah Outlier (IQR): `{lower_bound}`")
    st.write(f"Batas Atas Outlier (IQR): `{upper_bound}`")

    outliers = df[(df['ratings'] < lower_bound) | (df['ratings'] > upper_bound)]
    if not outliers.empty:
        st.write("Potensi Outlier berdasarkan Ratings:")
        st.dataframe(outliers[['title', 'ratings']])
    else:
        st.write("Tidak ada outlier yang terdeteksi.")

else:
    st.warning("Gagal memuat data. Mohon periksa apakah file CSV ada di direktori yang benar.")
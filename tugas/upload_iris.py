import pandas as pd
from sqlalchemy import create_engine
import sys

# --- 1. KONFIGURASI DATABASE (Silakan diisi sesuai pengaturan Anda) ---
db_user = 'postgres'  # Biasanya 'postgres'
db_password = '123456789' # Ganti dengan password yang Anda atur saat instalasi
db_host = 'localhost' # Biasanya 'localhost'
db_port = '5432'      # Port default PostgreSQL
db_name = 'iris_data' # Nama database yang sudah Anda buat di pgAdmin

# --- 2. KONFIGURASI FILE DAN NAMA TABEL ---
nama_file_csv = 'iris-full.csv'
nama_tabel_di_db = 'iris_data' # Nama tabel yang akan dibuat di PostgreSQL

# --- Proses Upload (Tidak perlu diubah) ---
print("Skrip dimulai...")

try:
    # Membuat koneksi ke database
    print(f"Mencoba terhubung ke database '{db_name}'...")
    engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    
    # Membaca file CSV
    print(f"Membaca file '{nama_file_csv}'...")
    df = pd.read_csv(nama_file_csv)
    
    # Mengunggah data ke PostgreSQL
    print(f"Mengunggah data ke tabel '{nama_tabel_di_db}'...")
    # if_exists='replace' akan menghapus tabel lama jika sudah ada dan membuat yang baru
    # Ganti menjadi 'append' jika hanya ingin menambah data, atau 'fail' jika tidak ingin menimpa
    df.to_sql(nama_tabel_di_db, engine, if_exists='replace', index=False)
    
    print("\n🚀 SUKSES! Data berhasil diunggah ke PostgreSQL.")
    
except FileNotFoundError:
    print(f"❌ GAGAL: File '{nama_file_csv}' tidak ditemukan. Pastikan file ada di folder yang sama.")
except Exception as e:
    print(f"❌ GAGAL: Terjadi kesalahan saat menghubungkan atau mengunggah data.")
    print(f"Detail Error: {e}")
    print("\nCoba periksa kembali detail koneksi database (password, nama database, dll).")
    sys.exit(1)
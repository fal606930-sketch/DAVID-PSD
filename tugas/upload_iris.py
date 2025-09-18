import pandas as pd
from sqlalchemy import create_engine

# --- Konfigurasi Koneksi Database ---
# Ganti dengan detail koneksi PostgreSQL Anda
db_user = 'postgres'
db_password = '123456789'
db_host = 'localhost'
db_port = '5432'
db_name = 'data_saya'

# Nama file CSV dan nama tabel yang diinginkan
csv_file_path = 'IMDB_processed_data.csv'
table_name = 'data_saya'

# --- Proses Upload ---
try:
    # 1. Baca file CSV ke dalam DataFrame pandas
    df = pd.read_csv(csv_file_path)
    print("File CSV berhasil dibaca.")

    # 3. Buat koneksi engine ke PostgreSQL
    # Format: postgresql://user:password@host:port/database_name
    engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    print("Engine database berhasil dibuat.")

    # 4. Unggah DataFrame ke tabel PostgreSQL
    # 'if_exists='replace'' akan membuat ulang tabel jika sudah ada.
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    
    print(f"Data berhasil diunggah ke tabel '{table_name}' di database '{db_name}'.")

except Exception as e:
    print(f"Terjadi kesalahan: {e}")
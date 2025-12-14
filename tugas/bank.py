import psycopg2
from psycopg2 import sql

# --- 1. Konfigurasi Koneksi Database ---
# Ganti dengan detail koneksi database Anda
db_config = {
    "host": "localhost",
    "database": "data_bank",
    "user": "postgres",
    "password": "123456789",
    "port": "5432"  # Port default PostgreSQL
}

# --- 2. Data yang Akan Diunggah ---
# Misalkan kita punya tabel 'karyawan' dengan kolom: nama, jabatan, dan gaji
data_untuk_diunggah = [
    ('Andi Wijaya', 'Software Engineer', 12000000),
    ('Budi Santoso', 'Project Manager', 18000000),
    ('Citra Lestari', 'Data Analyst', 15000000)
]

# --- 3. Skrip untuk Membuat Tabel (Jika belum ada) ---
# Anda bisa menjalankan ini sekali untuk membuat struktur tabelnya
buat_tabel_query = """
CREATE TABLE IF NOT EXISTS karyawan (
    id SERIAL PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    jabatan VARCHAR(50),
    gaji INTEGER
);
"""

# --- 4. Fungsi Utama untuk Menjalankan Proses ---
def unggah_data_ke_pg():
    """
    Menghubungkan ke database PostgreSQL, membuat tabel jika perlu,
    dan menyisipkan data.
    """
    conn = None
    try:
        # Menghubungkan ke server PostgreSQL
        print("Menghubungkan ke database...")
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        # Membuat tabel (jika belum ada)
        print("Membuat tabel 'karyawan' jika belum ada...")
        cur.execute(buat_tabel_query)
        conn.commit()

        # Menyisipkan data ke dalam tabel
        print("Memulai proses unggah data...")
        query_sisip = sql.SQL("INSERT INTO karyawan (nama, jabatan, gaji) VALUES {}").format(
            sql.SQL(',').join(map(sql.Literal, data_untuk_diunggah))
        )
        # Atau gunakan metode yang lebih aman dan efisien: executemany
        # query_sisip_aman = "INSERT INTO karyawan (nama, jabatan, gaji) VALUES (%s, %s, %s)"
        # cur.executemany(query_sisip_aman, data_untuk_diunggah)

        cur.execute(query_sisip)

        # Melakukan commit transaksi
        conn.commit()
        print(f"{cur.rowcount} baris data berhasil diunggah ke tabel 'karyawan'.")

        # Menutup kursor
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Terjadi kesalahan: {error}")

    finally:
        if conn is not None:
            conn.close()
            print("Koneksi ke database ditutup.")

# --- 5. Menjalankan Fungsi ---
if __name__ == "__main__":
    unggah_data_ke_pg()
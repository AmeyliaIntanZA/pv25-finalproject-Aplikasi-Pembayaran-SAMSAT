import sqlite3
from datetime import datetime

DB_NAME = "pembayaran_samsat.db"


def init_db():
    """Inisialisasi database dan membuat tabel riwayat_pembayaran."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Model data dengan 6 kolom utama + ID
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS riwayat_pembayaran (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nomor_polisi TEXT NOT NULL UNIQUE,
            nama_pemilik TEXT NOT NULL,
            jenis_kendaraan TEXT NOT NULL,
            jumlah_pajak INTEGER NOT NULL,
            status_pembayaran TEXT NOT NULL,
            tanggal_pembayaran TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_payment(nomor_polisi, nama_pemilik, jenis_kendaraan, jumlah_pajak):
    """Menambahkan data pembayaran baru ke database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "Lunas"

    try:
        cursor.execute("""
            INSERT INTO riwayat_pembayaran 
            (nomor_polisi, nama_pemilik, jenis_kendaraan, jumlah_pajak, status_pembayaran, tanggal_pembayaran)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nomor_polisi, nama_pemilik, jenis_kendaraan, jumlah_pajak, status, tanggal))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Terjadi jika nomor_polisi sudah ada
        print(f"Error: Nomor Polisi {nomor_polisi} sudah pernah melakukan pembayaran hari ini.")
        return False
    finally:
        conn.close()


def get_all_payments():
    """Mengambil semua riwayat pembayaran dari database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nomor_polisi, nama_pemilik, jenis_kendaraan, jumlah_pajak, status_pembayaran, tanggal_pembayaran FROM riwayat_pembayaran")
    data = cursor.fetchall()
    conn.close()
    return data


def delete_payment(payment_id):
    """Menghapus riwayat pembayaran berdasarkan ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM riwayat_pembayaran WHERE id = ?", (payment_id,))
    conn.commit()
    conn.close()


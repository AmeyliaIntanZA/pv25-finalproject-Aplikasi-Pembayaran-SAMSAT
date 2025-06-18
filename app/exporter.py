import csv
from PyQt5.QtWidgets import QFileDialog, QMessageBox


def export_to_csv(parent, data, headers):
    """Fungsi untuk mengekspor data ke file CSV."""
    if not data:
        QMessageBox.warning(parent, "Export Warning", "Tidak ada data untuk diekspor.")
        return

    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_path, _ = QFileDialog.getSaveFileName(
        parent,
        "Simpan sebagai CSV",
        "riwayat_pembayaran_samsat.csv",  # Nama file default
        "CSV Files (*.csv);;All Files (*)",
        options=options
    )

    if file_path:
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                writer.writerows(data)

            QMessageBox.information(parent, "Export Success", f"Data berhasil diekspor ke:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(parent, "Export Error", f"Terjadi kesalahan saat ekspor:\n{e}")

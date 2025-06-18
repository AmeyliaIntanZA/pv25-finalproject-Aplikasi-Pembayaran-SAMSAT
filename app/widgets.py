from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
                             QLineEdit, QComboBox, QSpinBox, QPushButton, QTableView, QHeaderView,
                             QAbstractItemView, QMessageBox, QGroupBox, QSizePolicy)
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from . import database, exporter


class MainContentWidget(QWidget):
    """Widget utama yang berisi form pembayaran dan tabel riwayat."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = None
        self.model = None
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # --- Form Input Pembayaran ---
        form_group_box = QGroupBox("Form Pembayaran Pajak Kendaraan")
        form_layout = QGridLayout(form_group_box)
        form_layout.setSpacing(15)
        form_layout.setColumnStretch(1, 1)

        self.nopol_input = QLineEdit()
        self.nopol_input.setPlaceholderText("e.g., DR 1234 ABC")

        self.pemilik_input = QLineEdit()
        self.pemilik_input.setPlaceholderText("Masukkan nama sesuai STNK")

        self.jenis_kendaraan_combo = QComboBox()
        self.jenis_kendaraan_combo.addItems(["Motor", "Mobil"])

        self.jumlah_pajak_input = QSpinBox()
        self.jumlah_pajak_input.setPrefix("Rp ")
        self.jumlah_pajak_input.setRange(50000, 50000000)
        self.jumlah_pajak_input.setSingleStep(1000)
        self.jumlah_pajak_input.setGroupSeparatorShown(True)

        self.add_button = QPushButton("Catat Pembayaran")
        self.add_button.clicked.connect(self.add_new_payment)
        self.add_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)

        form_layout.addWidget(QLabel("Nomor Polisi:"), 0, 0)
        form_layout.addWidget(self.nopol_input, 0, 1)
        form_layout.addWidget(QLabel("Nama Pemilik:"), 1, 0)
        form_layout.addWidget(self.pemilik_input, 1, 1)
        form_layout.addWidget(QLabel("Jenis Kendaraan:"), 2, 0)
        form_layout.addWidget(self.jenis_kendaraan_combo, 2, 1)
        form_layout.addWidget(QLabel("Jumlah Pajak:"), 3, 0)
        form_layout.addWidget(self.jumlah_pajak_input, 3, 1)

        button_hbox = QHBoxLayout()
        button_hbox.addStretch()
        button_hbox.addWidget(self.add_button)
        form_layout.addLayout(button_hbox, 4, 1)

        # --- Tabel Data ---
        table_group_box = QGroupBox("Riwayat Pembayaran Pajak")
        table_layout = QVBoxLayout(table_group_box)

        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # --- Tombol Aksi Tabel ---
        action_layout = QHBoxLayout()
        self.delete_button = QPushButton("Hapus Riwayat")
        self.export_button = QPushButton("Export ke CSV")

        self.delete_button.clicked.connect(self.delete_selected_payment)
        self.export_button.clicked.connect(self.export_data)

        action_layout.addStretch()
        action_layout.addWidget(self.delete_button)
        action_layout.addWidget(self.export_button)

        table_layout.addWidget(self.table_view)
        table_layout.addLayout(action_layout)

        main_layout.addWidget(form_group_box)
        main_layout.addWidget(table_group_box)
        main_layout.addStretch(1)

    def setup_database_model(self):
        """Setup model tabel dari database SQLite."""
        self.db = QSqlDatabase.addDatabase("QSQLITE", "samsat_connection")
        self.db.setDatabaseName(database.DB_NAME)
        if not self.db.open():
            QMessageBox.critical(self, "Database Error", self.db.lastError().text())
            return

        self.model = QSqlTableModel(self, self.db)
        self.model.setTable("riwayat_pembayaran")
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)

        headers = {
            "id": "ID", "nomor_polisi": "Nomor Polisi", "nama_pemilik": "Nama Pemilik",
            "jenis_kendaraan": "Jenis", "jumlah_pajak": "Jumlah Pajak (Rp)",
            "status_pembayaran": "Status", "tanggal_pembayaran": "Waktu Pembayaran"
        }
        for col_name, header_text in headers.items():
            self.model.setHeaderData(self.model.fieldIndex(col_name), 1, header_text)

        self.table_view.setModel(self.model)
        self.refresh_table()

    def refresh_table(self):
        self.model.select()
        self.table_view.resizeColumnsToContents()
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def add_new_payment(self):
        nopol = self.nopol_input.text().strip().upper()
        pemilik = self.pemilik_input.text().strip()
        jenis = self.jenis_kendaraan_combo.currentText()
        pajak = self.jumlah_pajak_input.value()

        if not all([nopol, pemilik]):
            QMessageBox.warning(self, "Input Tidak Valid", "Nomor Polisi dan Nama Pemilik harus diisi.")
            return

        success = database.add_payment(nopol, pemilik, jenis, pajak)
        if success:
            QMessageBox.information(self, "Sukses", f"Pembayaran untuk {nopol} berhasil dicatat.")
            self.nopol_input.clear()
            self.pemilik_input.clear()
            self.refresh_table()
        else:
            QMessageBox.critical(self, "Gagal", f"Nomor Polisi {nopol} sudah terdaftar. Gagal mencatat pembayaran.")

    def delete_selected_payment(self):
        selected_rows = self.table_view.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.information(self, "Tidak Ada Pilihan", "Silakan pilih riwayat dari tabel yang ingin dihapus.")
            return

        reply = QMessageBox.question(self, 'Konfirmasi Hapus',
                                     "Apakah Anda yakin ingin menghapus riwayat pembayaran ini?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            row_index = selected_rows[0].row()
            payment_id = self.model.data(self.model.index(row_index, 0))  # Kolom ID
            database.delete_payment(payment_id)
            self.refresh_table()

    def export_data(self):
        all_data = database.get_all_payments()
        headers = ["ID", "No. Polisi", "Nama Pemilik", "Jenis", "Jumlah Pajak", "Status", "Waktu Bayar"]
        exporter.export_to_csv(self, all_data, headers)

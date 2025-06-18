from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt


class AboutDialog(QDialog):
    """Kotak Dialog untuk menampilkan informasi 'About'."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Aplikasi Pembayaran SAMSAT")
        self.setFixedSize(400, 220)

        layout = QVBoxLayout(self)

        title = QLabel("Aplikasi Pembayaran SAMSAT v1.0")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #3498db;")

        summary = QLabel(
            "Aplikasi desktop untuk simulasi pencatatan pembayaran pajak kendaraan. "
            "Dibuat menggunakan PyQt5 dan SQLite."
        )
        summary.setWordWrap(True)
        summary.setAlignment(Qt.AlignCenter)

        creator_label = QLabel("Dibuat oleh:")
        creator_label.setAlignment(Qt.AlignCenter)
        creator_label.setStyleSheet("margin-top: 10px;")

        # --- DATA DIRI PEMBUAT BARU ---
        name_label = QLabel("Nama: Ameylia Intan Zurtika Ayu")
        nim_label = QLabel("NIM: F1D022110")
        # -----------------------------

        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("font-weight: bold;")
        nim_label.setAlignment(Qt.AlignCenter)
        nim_label.setStyleSheet("font-weight: bold;")

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)

        layout.addWidget(title)
        layout.addWidget(summary)
        layout.addStretch()
        layout.addWidget(creator_label)
        layout.addWidget(name_label)
        layout.addWidget(nim_label)
        layout.addStretch()
        layout.addWidget(ok_button)
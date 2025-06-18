from PyQt5.QtWidgets import QMainWindow, qApp, QLabel
from PyQt5.QtCore import Qt
from . import database
from .widgets import MainContentWidget
from .dialogs import AboutDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        database.init_db()

        self.setWindowTitle("Aplikasi Pembayaran SAMSAT")
        self.setGeometry(700, 400, 1900, 950)

        self.central_widget = MainContentWidget(self)
        self.setCentralWidget(self.central_widget)

        self._create_menu_bar()
        self._create_status_bar()

        self.central_widget.setup_database_model()
        self._load_stylesheet()

    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        export_action = file_menu.addAction("Export ke CSV")
        export_action.triggered.connect(self.central_widget.export_data)
        file_menu.addSeparator()
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(qApp.quit)

        help_menu = menu_bar.addMenu("&Help")
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about_dialog)

    def _create_status_bar(self):
        status_bar = self.statusBar()

        nama = "Ameylia Intan Zurtika Ayu"
        nim = "F1D022110"
        # -----------------------------
        info_label = QLabel(f"  Nama: {nama}  |  NIM: {nim}  ")
        info_label.setAlignment(Qt.AlignLeft)
        status_bar.addWidget(info_label)

    def _load_stylesheet(self):
        """Memuat stylesheet dari file .qss"""
        try:
            with open("styles/main_style_light.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Stylesheet 'main_style_light.qss' tidak ditemukan.")
            pass

    def show_about_dialog(self):
        dialog = AboutDialog(self)
        dialog.setStyleSheet(self.styleSheet())
        dialog.exec_()

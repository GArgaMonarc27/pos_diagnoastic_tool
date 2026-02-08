# ui/tabs/scanner_tab.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox


class ScannerTab(QWidget):
    def __init__(self, ctx, main_window):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Scanner Diagnostics")
        title.setStyleSheet("font-size: 20px; font-weight: 800;")
        layout.addWidget(title)

        info = QGroupBox("Detected Scanner")
        info_layout = QVBoxLayout(info)
        info_layout.addWidget(QLabel("Type: USB HID Scanner"))
        info_layout.addWidget(QLabel("Status: ⚪ Not checked"))
        layout.addWidget(info)

        layout.addWidget(QPushButton("Start Scan Test"))

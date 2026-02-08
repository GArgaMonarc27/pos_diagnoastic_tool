# ui/tabs/ports_tab.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox


class PortsTab(QWidget):
    def __init__(self, ctx, main_window):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Ports / Back Panel Mapping")
        title.setStyleSheet("font-size: 20px; font-weight: 800;")
        layout.addWidget(title)

        usb_box = QGroupBox("USB Ports (Logical)")
        usb_layout = QVBoxLayout(usb_box)
        usb_layout.addWidget(QLabel("USB001: ⚪ Not checked"))
        usb_layout.addWidget(QLabel("USB002: ⚪ Not checked"))
        usb_layout.addWidget(QLabel("USB003: ⚪ Not checked"))
        layout.addWidget(usb_box)

        cr_box = QGroupBox("CR / Cash Drawer Port")
        cr_layout = QVBoxLayout(cr_box)
        cr_layout.addWidget(QLabel("CR Port Status: ⚪ Not checked"))
        layout.addWidget(cr_box)

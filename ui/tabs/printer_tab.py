from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox
from ui.widgets.info_kv import InfoKV

# placeholder import; we’ll plug in real OPOS calls next
# from core.printer.epson_opos import EpsonOPOSPrinter

class PrinterTab(QWidget):
    def __init__(self, ctx, main_window):
        super().__init__()
        self.ctx = ctx
        self.main = main_window

        layout = QVBoxLayout(self)

        title = QLabel("Printer Diagnostics")
        title.setStyleSheet("font-size: 20px; font-weight: 800;")
        layout.addWidget(title)

        # OPOS CONFIG PANEL (recommended)
        self.opos_box = QGroupBox("OPOS Configuration")
        opos_layout = QVBoxLayout(self.opos_box)

        self.kv_ldn = InfoKV("Logical Device Name (LDN)", self.ctx.active_profile["printer_ldn"])
        self.kv_so = InfoKV("OPOS Service Object", "OPOS.POSPrinter")
        self.kv_ver = InfoKV("OPOS Version", "Unknown (detect later)")
        self.kv_reg = InfoKV("Registry Status", "⚪ Not checked")
        self.kv_claim = InfoKV("Claim Status", "⚪ Not checked")

        opos_layout.addWidget(self.kv_ldn)
        opos_layout.addWidget(self.kv_so)
        opos_layout.addWidget(self.kv_ver)
        opos_layout.addWidget(self.kv_reg)
        opos_layout.addWidget(self.kv_claim)

        layout.addWidget(self.opos_box)

        # STATUS PANEL
        self.status_box = QGroupBox("Status")
        s_layout = QVBoxLayout(self.status_box)
        self.lbl_status = QLabel("Status: ⚪ Not connected")
        self.lbl_status.setStyleSheet("font-size: 16px; font-weight: 700;")

        self.lbl_flags = QLabel("Online: - | Paper: - | Cover: - | Error: -")
        self.lbl_flags.setStyleSheet("color:#BDBDBD;")

        s_layout.addWidget(self.lbl_status)
        s_layout.addWidget(self.lbl_flags)
        layout.addWidget(self.status_box)

        # BUTTONS
        self.btn_connect = QPushButton("Connect (OPOS)")
        self.btn_refresh = QPushButton("Refresh Status")
        self.btn_test_print = QPushButton("Test Print")
        self.btn_test_drawer = QPushButton("Test Drawer Kick")

        layout.addWidget(self.btn_connect)
        layout.addWidget(self.btn_refresh)
        layout.addWidget(self.btn_test_print)
        layout.addWidget(self.btn_test_drawer)

    def refresh(self):
        # Update LDN when active profile changes
        self.kv_ldn.set_value(self.ctx.active_profile["printer_ldn"])

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox
from ui.widgets.info_kv import InfoKV

class CashDrawerTab(QWidget):
    def __init__(self, ctx, main_window):
        super().__init__()
        self.ctx = ctx
        self.main = main_window

        layout = QVBoxLayout(self)

        title = QLabel("Cash Drawer Diagnostics")
        title.setStyleSheet("font-size: 20px; font-weight: 800;")
        layout.addWidget(title)

        verify = QGroupBox("Verification Method")
        v_layout = QVBoxLayout(verify)
        v_layout.addWidget(InfoKV("Drawer Sensor Present", "❌ No (most drawers)"))
        v_layout.addWidget(InfoKV("Verification Type", "Signal-only"))
        v_layout.addWidget(InfoKV("Reliability Level", "Medium"))

        layout.addWidget(verify)

        status = QGroupBox("Signal Status")
        s_layout = QVBoxLayout(status)
        s_layout.addWidget(QLabel("Drawer Kick Signal Sent: ⚪ Not checked"))
        s_layout.addWidget(QLabel("Physical Open Confirmation: ⚠️ Unknown"))
        layout.addWidget(status)

        layout.addWidget(QPushButton("Fire Drawer"))
        layout.addWidget(QPushButton("Fire + Wait 3s"))

    def refresh(self):
        pass

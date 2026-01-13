from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QTabWidget
)
from ui.theme import DARK_QSS

from ui.tabs.overview_tab import OverviewTab
from ui.tabs.printer_tab import PrinterTab
from ui.tabs.cashdrawer_tab import CashDrawerTab
from ui.tabs.scanner_tab import ScannerTab
from ui.tabs.ports_tab import PortsTab
from ui.tabs.logs_tab import LogsTab


class MainWindow(QMainWindow):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

        self.setWindowTitle("POS Diagnostic Tool")
        self.setMinimumSize(1150, 740)
        self.setStyleSheet(DARK_QSS)

        root = QWidget()
        root_layout = QVBoxLayout(root)

        # Top bar (device selector + run id)
        top = QHBoxLayout()
        title = QLabel("POS Diagnostic Tool")
        title.setStyleSheet("font-size: 20px; font-weight: 800;")

        self.device_combo = QComboBox()
        self.populate_device_combo()
        self.device_combo.currentIndexChanged.connect(self.on_device_change)

        self.run_id_label = QLabel("Run ID: -")
        self.run_id_label.setStyleSheet("color:#BDBDBD;")

        top.addWidget(title)
        top.addStretch()
        top.addWidget(QLabel("Active Device:"))
        top.addWidget(self.device_combo)
        top.addSpacing(14)
        top.addWidget(self.run_id_label)

        root_layout.addLayout(top)

        # Tabs
        self.tabs = QTabWidget()
        self.overview = OverviewTab(self.ctx, self)
        self.printer = PrinterTab(self.ctx, self)
        self.drawer = CashDrawerTab(self.ctx, self)
        self.scanner = ScannerTab(self.ctx, self)
        self.ports = PortsTab(self.ctx, self)
        self.logs = LogsTab(self.ctx, self)

        self.tabs.addTab(self.overview, "Overview")
        self.tabs.addTab(self.printer, "Printer")
        self.tabs.addTab(self.drawer, "Cash Drawer")
        self.tabs.addTab(self.scanner, "Scanner")
        self.tabs.addTab(self.ports, "Ports")
        self.tabs.addTab(self.logs, "Logs")

        root_layout.addWidget(self.tabs)
        self.setCentralWidget(root)

    def populate_device_combo(self):
        # Prevent indexChanged from firing while rebuilding
        self.device_combo.blockSignals(True)
        self.device_combo.clear()

        for p in self.ctx.device_profiles:
            label = p["name"]
            if p.get("manufacturer_hint") == "EPSON":
                label = f"{label} (EPSON)"
            self.device_combo.addItem(label)

        self.device_combo.blockSignals(False)

        # Optional: set default active profile if not set
        if self.ctx.device_profiles and not getattr(self.ctx, "active_profile", None):
            self.ctx.active_profile = self.ctx.device_profiles[0]

    def on_device_change(self, idx: int):
        if idx < 0 or idx >= len(self.ctx.device_profiles):
            return

        self.ctx.active_profile = self.ctx.device_profiles[idx]
        self.ctx.logger.log(
            "INFO",
            f"Active device changed to {self.ctx.active_profile['name']}",
            self.ctx.run_manager.current_run_id
        )
        self.refresh_all()

    def set_run_id(self, run_id: str):
        self.run_id_label.setText(f"Run ID: {run_id}")

    def refresh_all(self):
        # Allow each tab to refresh if it implements refresh()
        for tab in [self.overview, self.printer, self.drawer, self.scanner, self.ports, self.logs]:
            if hasattr(tab, "refresh"):
                tab.refresh()

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton
from ui.widgets.status_card import StatusCard

from core.device_manager import DeviceManager
from core.status_models import Health


class OverviewTab(QWidget):
    def __init__(self, ctx, main_window):
        super().__init__()
        self.ctx = ctx
        self.main = main_window

        layout = QVBoxLayout(self)

        header = QLabel("System Health Overview")
        header.setStyleSheet("font-size: 22px; font-weight: 800;")
        layout.addWidget(header)

        self.grid = QGridLayout()
        self.card_printer = StatusCard("🖨 Printer", "⚪ Not checked")
        self.card_drawer  = StatusCard("💰 Cash Drawer", "⚪ Not checked")
        self.card_scanner = StatusCard("📠 Scanner", "⚪ Not checked")
        self.card_ports   = StatusCard("🔌 Ports", "⚪ Not checked")
        self.card_config  = StatusCard("⚙ Configuration", "⚪ Not checked")

        self.grid.addWidget(self.card_printer, 0, 0)
        self.grid.addWidget(self.card_drawer,  0, 1)
        self.grid.addWidget(self.card_scanner, 1, 0)
        self.grid.addWidget(self.card_ports,   1, 1)
        self.grid.addWidget(self.card_config,  2, 0)

        layout.addLayout(self.grid)

        self.run_btn = QPushButton("Run Full Diagnostic")
        self.run_btn.clicked.connect(self.run_full)

        self.export_btn = QPushButton("Export Report (soon)")
        self.clear_btn = QPushButton("Clear Logs")
        self.clear_btn.clicked.connect(self.clear_logs)

        layout.addWidget(self.run_btn)
        layout.addWidget(self.export_btn)
        layout.addWidget(self.clear_btn)

    def run_full(self):
        run_id = self.ctx.run_manager.start_run()
        self.ctx.logger.log("INFO", "Full diagnostic started", run_id)
        self.main.set_run_id(run_id)

        dm = DeviceManager(self.ctx)
        results = dm.run_all()

        self.card_config.set_status(results["config"].health.value)
        self.card_printer.set_status(results["printer"].health.value)
        self.card_drawer.set_status(results["drawer"].health.value)
        self.card_scanner.set_status(results["scanner"].health.value)
        self.card_ports.set_status(results["ports"].health.value)

        for key, res in results.items():
            if res.message:
                self.ctx.logger.log(
                    "INFO" if res.health == Health.OK else "WARN",
                    f"{key.capitalize()} check: {res.message}",
                    run_id
                )

        self.main.refresh_all()

    def clear_logs(self):
        self.ctx.logger.clear()
        self.main.refresh_all()

    def refresh(self):
        # Overview updates only when Run Full Diagnostic is pressed
        pass

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox, QTextEdit

class LogsTab(QWidget):
    def __init__(self, ctx, main_window):
        super().__init__()
        self.ctx = ctx
        self.main = main_window

        layout = QVBoxLayout(self)

        title = QLabel("Logs")
        title.setStyleSheet("font-size: 20px; font-weight: 800;")
        layout.addWidget(title)

        self.run_id = QLabel("Run ID: -")
        self.run_id.setStyleSheet("color:#BDBDBD;")
        layout.addWidget(self.run_id)

        box = QGroupBox("Log Output")
        b = QVBoxLayout(box)

        self.text = QTextEdit()
        self.text.setReadOnly(True)
        b.addWidget(self.text)

        layout.addWidget(box)

        self.btn_refresh = QPushButton("Refresh Logs")
        self.btn_refresh.clicked.connect(self.refresh)
        layout.addWidget(self.btn_refresh)

    def refresh(self):
        rid = self.ctx.run_manager.current_run_id or "-"
        self.run_id.setText(f"Run ID: {rid}")

        lines = []
        for e in self.ctx.logger.entries():
            lines.append(f"{e['time']}  {e['level']:<5}  [{e['run_id']}]  {e['message']}")
        self.text.setText("\n".join(lines))

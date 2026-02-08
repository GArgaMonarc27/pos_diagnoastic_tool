# ui/widgets/status_card.py

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel


class StatusCard(QFrame):
    def __init__(self, title: str, status_text: str):
        super().__init__()

        self.setStyleSheet("""
            QFrame {
                background: #242424;
                border-radius: 14px;
                padding: 12px;
            }
        """)

        layout = QVBoxLayout(self)

        self.title = QLabel(title)
        self.title.setStyleSheet("font-size: 14px; color: #BDBDBD;")

        self.value = QLabel(status_text)
        self.value.setStyleSheet("font-size: 18px; font-weight: 700;")

        layout.addWidget(self.title)
        layout.addWidget(self.value)

    def set_status(self, status_text: str):
        self.value.setText(status_text)

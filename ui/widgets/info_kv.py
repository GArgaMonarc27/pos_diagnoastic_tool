# ui/widgets/info_kv.py

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel


class InfoKV(QWidget):
    def __init__(self, key: str, value: str):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.key_label = QLabel(key)
        self.key_label.setStyleSheet("color: #BDBDBD; min-width: 180px;")

        self.value_label = QLabel(value)
        self.value_label.setStyleSheet("font-weight: 600;")

        layout.addWidget(self.key_label)
        layout.addWidget(self.value_label)

    def set_value(self, value: str):
        self.value_label.setText(value)

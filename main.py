import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.app_context import AppContext

def main():
    app = QApplication(sys.argv)

    ctx = AppContext()  # shared state: active device, run id, logger, etc.
    window = MainWindow(ctx)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

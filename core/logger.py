# core/logger.py

from datetime import datetime


class AppLogger:
    """
    Simple in-memory application logger.
    Used across tabs and for diagnostic runs.
    """

    def __init__(self):
        self._entries = []

    def log(self, level: str, message: str, run_id: str | None = None):
        self._entries.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "level": level.upper(),
            "run_id": run_id or "-",
            "message": message,
        })

    def entries(self):
        return list(self._entries)

    def clear(self):
        self._entries.clear()

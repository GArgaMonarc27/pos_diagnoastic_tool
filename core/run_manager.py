# core/run_manager.py

from datetime import datetime


class RunManager:
    """
    Generates and tracks a correlation Run ID for each diagnostic run.
    Example: POS-01-20260208-143210
    """

    def __init__(self, terminal_id: str = "POS-01"):
        self.terminal_id = terminal_id
        self.current_run_id = None

    def start_run(self) -> str:
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.current_run_id = f"{self.terminal_id}-{ts}"
        return self.current_run_id

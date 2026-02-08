# core/status_models.py

from enum import Enum
from dataclasses import dataclass
from typing import Optional


class Health(Enum):
    OK = "🟢 Healthy"
    WARN = "🟠 Warning"
    ERROR = "🔴 Error"
    UNKNOWN = "⚪ Unknown"


@dataclass
class DeviceHealth:
    health: Health
    message: Optional[str] = None

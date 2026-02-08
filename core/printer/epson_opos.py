# core/printer/epson_opos.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any
import win32com.client


# OPOS result codes (partial)
OPOS_SUCCESS = 0


@dataclass
class OposConnectResult:
    ok: bool
    message: str


class EpsonOposPrinter:
    def __init__(self, logical_name: str):
        self.logical_name = logical_name
        self.obj = None

    def connect(self, claim_timeout_ms: int = 1000) -> OposConnectResult:
        if not self.logical_name:
            return OposConnectResult(False, "No Logical Device Name provided")

        try:
            self.obj = win32com.client.Dispatch("OPOS.POSPrinter")
        except Exception as e:
            return OposConnectResult(
                False,
                f"Failed to create OPOS COM object (bitness mismatch or OPOS missing): {e}"
            )

        rc = int(self.obj.Open(self.logical_name))
        if rc != OPOS_SUCCESS:
            return OposConnectResult(False, f"OPOS Open failed ({rc})")

        rc = int(self.obj.ClaimDevice(claim_timeout_ms))
        if rc != OPOS_SUCCESS:
            return OposConnectResult(False, f"OPOS ClaimDevice failed ({rc})")

        self.obj.DeviceEnabled = True
        return OposConnectResult(True, "Connected")

    def disconnect(self):
        if not self.obj:
            return
        try:
            self.obj.DeviceEnabled = False
            self.obj.ReleaseDevice()
            self.obj.Close()
        except Exception:
            pass
        self.obj = None

    def get_status(self) -> Dict[str, Any]:
        if not self.obj:
            return {"connected": False}

        return {
            "CoverOpen": bool(self.obj.CoverOpen),
            "RecEmpty": bool(self.obj.RecEmpty),
            "RecNearEnd": bool(self.obj.RecNearEnd),
            "ErrorState": bool(self.obj.ErrorState),
            "CapRecPresent": bool(getattr(self.obj, "CapRecPresent", False)),
            "DrawerOpened": bool(getattr(self.obj, "DrawerOpened", False)),
        }

    def test_print(self) -> OposConnectResult:
        if not self.obj:
            return OposConnectResult(False, "Not connected")
        try:
            self.obj.PrintNormal(2, "=== POS Diagnostic Test ===\nPrinter OK\n\n")
            return OposConnectResult(True, "Test print sent")
        except Exception as e:
            return OposConnectResult(False, f"Print failed: {e}")

    def fire_drawer(self, pin: int = 2) -> OposConnectResult:
        if not self.obj:
            return OposConnectResult(False, "Not connected")
        try:
            self.obj.OpenDrawer(pin)
            return OposConnectResult(True, "Drawer kick sent")
        except Exception as e:
            return OposConnectResult(False, f"Drawer kick failed: {e}")

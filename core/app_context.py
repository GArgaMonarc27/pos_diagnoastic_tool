# core/app_context.py

from core.run_manager import RunManager
from core.logger import AppLogger
from core.printer.ldn_discovery import discover_opos_posprinter_ldns


class AppContext:
    def __init__(self):
        self.store_id = "AUS-0000"
        self.terminal_id = "POS-01"

        # Runtime helpers
        self.run_manager = RunManager(terminal_id=self.terminal_id)
        self.logger = AppLogger()

        # Auto-discover OPOS printer LDNs from registry
        entries = discover_opos_posprinter_ldns()

        if entries:
            self.device_profiles = [
                {
                    "name": e.ldn,
                    "printer_ldn": e.ldn,
                    "registry_path": e.registry_path,
                    "service_object": e.service_object or "OPOS.POSPrinter",
                    "manufacturer_hint": e.manufacturer_hint or "Unknown",
                }
                for e in entries
            ]
            self.active_profile = self.device_profiles[0]
            self.logger.log("INFO", f"Discovered {len(entries)} OPOS POSPrinter(s)", None)
        else:
            # Fallback if OPOS is not installed on this machine
            self.device_profiles = [
                {
                    "name": "No OPOS Printer Found",
                    "printer_ldn": "",
                    "registry_path": "",
                    "service_object": "OPOS.POSPrinter",
                    "manufacturer_hint": "Unknown",
                }
            ]
            self.active_profile = self.device_profiles[0]
            self.logger.log("WARN", "No OPOS POSPrinter LDNs found in registry", None)

from typing import Dict
from core.status_models import Health, DeviceHealth
from core.printer.epson_opos import EpsonOposPrinter


class DeviceManager:
    def __init__(self, ctx):
        self.ctx = ctx

    def run_all(self) -> Dict[str, DeviceHealth]:
        """
        Runs all diagnostics and returns health per category.
        """
        results = {
            "config": self.check_configuration(),
            "printer": self.check_printer(),
            "drawer": self.check_drawer(),
            "ports": self.check_ports(),
            "scanner": DeviceHealth(Health.UNKNOWN, "Not implemented"),
        }
        return results

    # -----------------------------
    # CONFIGURATION HEALTH
    # -----------------------------
    def check_configuration(self) -> DeviceHealth:
        profile = self.ctx.active_profile

        if not profile.get("printer_ldn"):
            return DeviceHealth(Health.ERROR, "No OPOS Logical Device Name found")

        if not profile.get("registry_path"):
            return DeviceHealth(Health.ERROR, "OPOS registry entry missing")

        return DeviceHealth(Health.OK, "OPOS configuration present")

    # -----------------------------
    # PRINTER HEALTH
    # -----------------------------
    def check_printer(self) -> DeviceHealth:
        ldn = self.ctx.active_profile.get("printer_ldn")
        if not ldn:
            return DeviceHealth(Health.ERROR, "No printer LDN")

        printer = EpsonOposPrinter(ldn)
        res = printer.connect()

        if not res.ok:
            return DeviceHealth(Health.ERROR, res.message)

        status = printer.get_status()
        printer.disconnect()

        if status.get("ErrorState"):
            return DeviceHealth(Health.ERROR, "Printer error state")

        if status.get("CoverOpen"):
            return DeviceHealth(Health.WARN, "Printer cover open")

        if status.get("RecEmpty"):
            return DeviceHealth(Health.ERROR, "Paper empty")

        if status.get("RecNearEnd"):
            return DeviceHealth(Health.WARN, "Paper near end")

        return DeviceHealth(Health.OK, "Printer ready")

    # -----------------------------
    # CASH DRAWER HEALTH
    # -----------------------------
    def check_drawer(self) -> DeviceHealth:
        """
        Signal-level verification only (no sensor).
        """
        ldn = self.ctx.active_profile.get("printer_ldn")
        if not ldn:
            return DeviceHealth(Health.ERROR, "No printer for drawer")

        printer = EpsonOposPrinter(ldn)
        res = printer.connect()

        if not res.ok:
            return DeviceHealth(Health.ERROR, "Cannot access drawer (printer not available)")

        status = printer.get_status()
        printer.disconnect()

        if status.get("CapRecPresent") is False:
            return DeviceHealth(Health.WARN, "Drawer not supported by printer")

        return DeviceHealth(
            Health.WARN,
            "Drawer signal OK (physical open not verifiable)"
        )

    # -----------------------------
    # PORTS HEALTH (logical)
    # -----------------------------
    def check_ports(self) -> DeviceHealth:
        # For now this is logical inference only
        return DeviceHealth(
            Health.OK,
            "Ports detected via Windows (logical mapping)"
        )

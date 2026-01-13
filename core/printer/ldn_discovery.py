from dataclasses import dataclass
from typing import List, Optional
import winreg

from core.registry import _enum_subkeys, _read_value, iter_paths


@dataclass
class OposPrinterEntry:
    ldn: str
    registry_path: str
    service_object: Optional[str] = None
    manufacturer_hint: Optional[str] = None


# Common OPOS registry locations used by OLE for Retail / OPOS ServiceOPOS
# Some systems store under "ServiceOPOS", others under "ServiceOPOS\POSPrinter"
CANDIDATE_BASE_PATHS = [
    r"SOFTWARE\OLEforRetail\ServiceOPOS\POSPrinter",
    r"SOFTWARE\OLEforRetail\ServiceOPOS\POSPrinter\Device",
    r"SOFTWARE\OLEforRetail\ServiceOPOS\POSPrinter\Devices",
    r"SOFTWARE\OLEforRetail\ServiceOPOS\POSPrinter\LogicalDevices",
]


def discover_opos_posprinter_ldns() -> List[OposPrinterEntry]:
    found: List[OposPrinterEntry] = []
    seen = set()

    for root, view in iter_paths():
        access = winreg.KEY_READ | view

        for base in CANDIDATE_BASE_PATHS:
            for subkey in _enum_subkeys(root, base, access):
                # In most OPOS setups, subkey name itself is the LDN
                ldn = subkey.strip()
                if not ldn or ldn.lower() in seen:
                    continue

                full_path = f"{base}\\{subkey}"

                # Optional hints: these value names vary by vendor/config
                so = (
                    _read_value(root, full_path, "ServiceObject", access)
                    or _read_value(root, full_path, "Service Object", access)
                    or _read_value(root, full_path, "SO", access)
                )

                friendly = (
                    _read_value(root, full_path, "FriendlyName", access)
                    or _read_value(root, full_path, "Description", access)
                    or _read_value(root, full_path, "DeviceName", access)
                )

                manufacturer_hint = None
                blob = " ".join([x for x in [ldn, so, friendly] if x])
                if "epson" in blob.lower() or "tm-" in blob.lower():
                    manufacturer_hint = "EPSON"

                key_id = ldn.lower()
                if key_id in seen:
                    continue

                seen.add(key_id)
                found.append(
                    OposPrinterEntry(
                        ldn=ldn,
                        registry_path=f"{'HKLM' if root == winreg.HKEY_LOCAL_MACHINE else 'HKCU'}\\{full_path}",
                        service_object=so,
                        manufacturer_hint=manufacturer_hint,
                    )
                )

    # Prefer Epson-ish ones first
    found.sort(key=lambda x: (0 if x.manufacturer_hint == "EPSON" else 1, x.ldn.lower()))
    return found

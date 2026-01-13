import winreg
from typing import Iterable, Tuple, Optional


def _open_key(root, path: str, access: int):
    return winreg.OpenKey(root, path, 0, access)


def _enum_subkeys(root, path: str, access: int) -> Iterable[str]:
    try:
        with _open_key(root, path, access) as key:
            i = 0
            while True:
                try:
                    yield winreg.EnumKey(key, i)
                    i += 1
                except OSError:
                    break
    except OSError:
        return


def _read_value(root, path: str, name: str, access: int) -> Optional[str]:
    try:
        with _open_key(root, path, access) as key:
            val, _ = winreg.QueryValueEx(key, name)
            return str(val)
    except OSError:
        return None


def iter_paths() -> Iterable[Tuple[int, int]]:
    """
    Yields (root, view_flag) combos for both 64-bit and 32-bit views.
    """
    for root in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
        for view in (winreg.KEY_WOW64_64KEY, winreg.KEY_WOW64_32KEY):
            yield root, view

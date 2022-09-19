"""Home Assistant Desktop: Autostart Windows"""
import os
import platform
import sys


def autostart_windows_disable():
    """Disable autostart for Windows"""
    if platform.system() != "Windows":
        return

    # pylint: disable=import-error, import-outside-toplevel
    from winreg import HKEY_CURRENT_USER, KEY_ALL_ACCESS, CloseKey, DeleteValue, OpenKey

    try:
        key = OpenKey(
            HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            reserved=0,
            access=KEY_ALL_ACCESS,
        )
        if key is None:
            return
        DeleteValue(key, "homeassistantdesktop")
        CloseKey(key)
    except OSError:
        pass


def autostart_windows_enable():
    """Enable autostart for Windows"""
    if platform.system() != "Windows":
        return

    # pylint: disable=import-error, import-outside-toplevel
    from winreg import (
        HKEY_CURRENT_USER,
        KEY_ALL_ACCESS,
        REG_SZ,
        CloseKey,
        OpenKey,
        SetValueEx,
    )

    key = OpenKey(
        HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        reserved=0,
        access=KEY_ALL_ACCESS,
    )
    SetValueEx(
        key,
        "homeassistantdesktop",
        0,
        REG_SZ,
        f'"{os.path.join(os.path.dirname(sys.executable), "pythonw.exe")}" -m homeassistantdesktop main --silent',
    )
    CloseKey(key)

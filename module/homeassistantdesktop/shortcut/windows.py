"""Home Assistant Desktop: Shortcut Windows"""
import os
import platform
import sys


def create_windows_shortcuts():
    """Create Windows shortcuts"""
    if platform.system() != "Windows":
        return

    # pylint: disable=import-error, import-outside-toplevel
    from winreg import HKEY_CURRENT_USER, KEY_READ, CloseKey, OpenKey, QueryValueEx

    from win32com.client import Dispatch

    registry_key = OpenKey(
        HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",
        reserved=0,
        access=KEY_READ,
    )
    registry_value, _ = QueryValueEx(registry_key, "Programs")
    CloseKey(registry_key)

    directory = os.path.abspath(
        os.path.join(
            os.path.expandvars(os.path.normpath(registry_value)),
            "homeassistantdesktop",
        )
    )
    os.makedirs(directory, exist_ok=True)

    link_path = os.path.join(directory, "Home Assistant Desktop.lnk")
    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(link_path)
    shortcut.Arguments = "-m homeassistantdesktop main --silent"
    shortcut.Description = "Home Assistant Desktop"
    shortcut.IconLocation = os.path.join(os.path.dirname(__file__), "../icon.ico")
    shortcut.Targetpath = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
    shortcut.WorkingDirectory = sys.prefix
    shortcut.save()

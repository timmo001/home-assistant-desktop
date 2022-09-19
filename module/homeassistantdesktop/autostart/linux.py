"""Home Assistant Desktop: Autostart Linux"""
import os
import sys

desktop_entry = f"""
[Desktop Entry]
Name=Home Assistant Desktop
Comment=Home Assistant Desktop
Exec={sys.executable} -m homeassistantdesktop main
Icon={os.path.join(os.path.dirname(__file__),'../icon.png')}
Terminal=false
Type=Application
Categories=Application;
"""


def autostart_linux_disable():
    """Disable autostart for Linux"""
    path = os.path.expanduser("~/.config/autostart/homeassistantdesktop.desktop")
    if os.path.exists(path):
        os.remove(path)


def autostart_linux_enable():
    """Enable autostart for Linux"""
    path = os.path.expanduser("~/.config/autostart/homeassistantdesktop.desktop")
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(path, "homeassistantdesktop.desktop")
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as file:
            file.write(desktop_entry)

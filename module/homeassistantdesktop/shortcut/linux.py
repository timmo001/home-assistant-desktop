"""Home Assistant Desktop: Shortcut Linux"""
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


def create_linux_shortcuts():
    """Create Linux shortcuts"""
    path = os.path.expanduser("~/.local/share/applications")
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(path, "homeassistantdesktop.desktop")
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as file:
            file.write(desktop_entry)

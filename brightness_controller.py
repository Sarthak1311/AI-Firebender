import subprocess
import platform

def increase_brightness():
    """Increase screen brightness (macOS only)."""
    if platform.system() == "Darwin":  # Darwin = macOS
        subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 144'])
    else:
        print("Brightness control is only supported on macOS in this module.")

def decrease_brightness():
    """Decrease screen brightness (macOS only)."""
    if platform.system() == "Darwin":
        subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 145'])
    else:
        print("Brightness control is only supported on macOS in this module.")

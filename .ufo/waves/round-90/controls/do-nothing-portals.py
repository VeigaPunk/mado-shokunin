#!/usr/bin/env python3
"""Round-90 C1 do-nothing control: answers "no backend" for every interface without reading anything."""
import json, sys
I = "org.freedesktop.impl.portal."
N = ["Lockdown", "Access", "Settings", "FileChooser", "AppChooser", "Print", "Notification", "Inhibit", "Screenshot",
     "Background", "Wallpaper", "Account", "Email", "Secret", "GlobalShortcuts", "DynamicLauncher", "ScreenCast",
     "RemoteDesktop", "Clipboard", "InputCapture", "Usb"]
print(json.dumps({"picks": {I + n: [] for n in N}, "reasons": {I + n: "no-backend" for n in N}}))
sys.exit(0)

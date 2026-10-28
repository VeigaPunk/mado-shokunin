#!/usr/bin/env python3
"""C1 do-nothing control: an entry transcribed from frozen-tables.json. No pin is opened, every proposition is a
placeholder. Writes into a scratch repo worktree (never the lane) and commits. Usage: build_c1_junk.py REPO FROZEN_JSON VARIANT
VARIANT: s052 (K17 cites the registered S052 row) | forged (K17 cites an added row whose URL merely contains the commit)."""
import json, os, subprocess, sys

repo, frozen, variant = sys.argv[1], sys.argv[2], sys.argv[3]
T = json.load(open(frozen))["c1"]
ENTRY = "corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md"
PIN_SID = {
    "Hyprland-InputManager.cpp": "S316", "Hyprland-IKeyboard.cpp": "S319", "Hyprland-IKeyboard.hpp": "S380",
    "Hyprland-SeatManager.cpp": "S378", "Hyprland-protocols-core-Seat.cpp": "S379",
    "Hyprland-ConfigValues.cpp": "S318", "Hyprland-legacy-ConfigManager.cpp": "S317",
    "wayland-1.26.0-wayland.xml": "S052" if variant == "s052" else "S381", "host-input.conf": "host",
    "host-getoption.json": "host",
}
C = "efb50993780079460b0cbed1363e2166a2de1d9f"
used = sorted({PIN_SID[r["pin"]] for r in T["k"]} - {"host"} | {"S378", "S379", "S380"})
out = ["source: " + ", ".join(used), "verified-at: 2026-10-28", "recheck: on-release", "",
       "# Keyboard repeat rate, repeat delay and numlock (do-nothing control)", "",
       "Frozen-table transcription only: no pin was opened to write these rows.", "",
       "| ID | Proposition | Source | Pin:anchor | Quote |", "|---|---|---|---|---|"]
for r in T["k"]:
    out.append(f"| {r['id']} | placeholder {r['id']}: transcribed row, proposition text not checked against pin | "
               f"{PIN_SID[r['pin']]} | {r['pin']}:{r['line']} | `{r['quote']}` |")
for r in T["h"]:
    out.append(f"| {r['id']} | placeholder {r['id']}: host row transcribed, not checked against host pin | host | "
               f"{r['pin']}:{r['line']} | `{r['quote']}` |")
open(os.path.join(repo, ENTRY), "w").write("\n".join(out) + "\n")

rd = os.path.join(repo, "corpus/README.md")
open(rd, "a").write("| `knowledge/hyprland-keyboard-repeat-numlock-r55.md` (do-nothing control) | placeholder index row |\n")

rows = {
    "S378": ("Hyprland v0.56.2 seat manager junk", "src/managers/SeatManager.cpp", "SeatManager.cpp:175-178"),
    "S379": ("Hyprland v0.56.2 core seat junk", "src/protocols/core/Seat.cpp", "Seat.cpp:441-448"),
    "S380": ("Hyprland v0.56.2 keyboard header junk", "src/devices/IKeyboard.hpp", "IKeyboard.hpp:121-123"),
}
lines = []
for sid, (title, suffix, anchor) in rows.items():
    lines.append(f"| {sid} | {title} - https://raw.githubusercontent.com/hyprwm/Hyprland/{C}/{suffix} | code | A | junk | "
                 f"{anchor} @ {C} | placeholder | mined | 2026-10-28 | on-release | {ENTRY} |")
if variant == "forged":
    lines.append(f"| S381 | wayland 1.26.0 XML junk - https://raw.githubusercontent.com/hyprwm/Hyprland/{C}/1.26.0/protocol/wayland.xml "
                 f"| spec | A | junk | wayland.xml | placeholder | mined | 2026-10-28 | on-release | {ENTRY} |")
open(os.path.join(repo, "corpus/SOURCES.md"), "a").write("\n" + "\n".join(lines) + "\n")

subprocess.run(["git", "-C", repo, "add", "-A"], check=True)
subprocess.run(["git", "-C", repo, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-qm",
                f"c1 do-nothing {variant}"], check=True)
print(subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip())

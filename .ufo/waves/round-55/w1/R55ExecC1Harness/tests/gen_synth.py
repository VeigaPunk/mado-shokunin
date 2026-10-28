#!/usr/bin/env python3
"""Build a synthetic C1 good tree as a git repo from frozen-tables.json. usage: gen_synth.py LANE_ROUND_DIR DEST"""
import json, subprocess, sys, os, shutil
from pathlib import Path
rd, dest = Path(sys.argv[1]), Path(sys.argv[2])
T = json.loads((rd / "frozen-tables.json").read_text())
c1 = T["c1"]; commit = c1["commit"]
SID = {"Hyprland-InputManager.cpp": "S316", "Hyprland-IKeyboard.cpp": "S319", "Hyprland-SeatManager.cpp": "S378",
       "Hyprland-protocols-core-Seat.cpp": "S379", "Hyprland-ConfigValues.cpp": "S318",
       "Hyprland-legacy-ConfigManager.cpp": "S317", "wayland-1.26.0-wayland.xml": "S052", "Hyprland-IKeyboard.hpp": "S380"}
URLP = "https://raw.githubusercontent.com/hyprwm/Hyprland/%s/" % commit
def url(pin):
    suf = c1["source_suffix"][pin]
    return "https://gitlab.freedesktop.org/wayland/wayland/-/raw/" + suf if pin.startswith("wayland") else URLP + suf
entry = c1["entry"]
L = ["# Keyboard repeat rate, repeat delay and numlock (synthetic test entry)", "",
     "source: S316 S317 S318 S319 S052 S378 S379 S380", "verified-at: 2026-10-28", "recheck: on-release", "",
     "| id | proposition | source | anchor | quote |", "|---|---|---|---|---|"]
for k in c1["k"]:
    L.append("| %s | synthetic proposition for %s, padded to exceed forty characters | %s | %s:%d | `%s` |" % (
        k["id"], k["id"], SID[k["pin"]], k["pin"], k["line"], k["quote"]))
for h in c1["h"]:
    L.append("| %s | synthetic host proposition for %s | host | %s:%d | `%s` |" % (h["id"], h["id"], h["pin"], h["line"], h["quote"]))
rows = ["| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |", "|---|---|---|---|---|---|---|---|---|---|---|"]
for pin, sid in sorted(SID.items(), key=lambda x: x[1]):
    new = sid in ("S378", "S379", "S380")
    rows.append("| %s | synthetic %s — %s | code | A | scope | anchor | teaches | mined | %s | on-release | %s |" % (
        sid, pin, url(pin), "2026-10-28" if new else "2026-10-20", entry if new else "corpus/knowledge/x.md"))
tree = {entry: "\n".join(L) + "\n",
        "corpus/README.md": "# README\n\n| file | what |\n|---|---|\n| `knowledge/hyprland-keyboard-repeat-numlock-r55.md` | synthetic row |\n",
        "corpus/SOURCES.md": "# SOURCES\n\n## Registry\n\n" + "\n".join(rows) + "\n",
        ".ufo/waves/round-55/frozen-tables.json": (rd / "frozen-tables.json").read_text()}
shutil.rmtree(dest, ignore_errors=True); dest.mkdir(parents=True)
for rel, txt in tree.items():
    f = dest / rel; f.parent.mkdir(parents=True, exist_ok=True); f.write_text(txt)
for p in c1["pin_sha256"]:
    f = dest / c1["pin_dir"] / p; f.parent.mkdir(parents=True, exist_ok=True); shutil.copy(rd / "fetch" / p, f)
E = {"GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1", "PATH": os.environ["PATH"], "HOME": str(dest)}
def g(*a): return subprocess.run(["git", "-C", str(dest), *a], env=E, check=True, capture_output=True, text=True).stdout
subprocess.run(["git", "init", "-q", str(dest)], env=E, check=True)
assert os.path.realpath(g("rev-parse", "--show-toplevel").strip()) == os.path.realpath(str(dest))
g("add", "-A"); g("-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "-m", "synthetic good tree")
print(g("rev-parse", "HEAD").strip())

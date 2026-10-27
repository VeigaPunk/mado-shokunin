#!/usr/bin/env python3
"""Score each synthetic receipt shape against the gate's reported rules."""
import json
import subprocess
import sys

ROOT, GATE = sys.argv[1], sys.argv[2]

CASES = [
    ("device names + addresses (hyprctl devices -j projection)", ".ufo/s/devices.json"),
    ("instance signature + /run/user socket (hyprctl instances -j)", ".ufo/s/instances.json"),
    ("small ls -LRl of a home tree (3 dir headers)", ".ufo/s/ls-lRl-small.txt"),
    ("ls -LRl rooted outside /home (C1 sandbox shape)", ".ufo/s/ls-lRl-scratch.txt"),
    ("literal warm cache text (entry path, --dir, --title)", ".ufo/s/cache-warm.txt"),
    ("home listing base64-encoded", ".ufo/s/b64.txt"),
    ("home listing as a JSON array", ".ufo/s/home-json.txt"),
    ("home listing as markdown table rows", ".ufo/s/home-table.md"),
    ("secret-shaped env (token / cloud key)", ".ufo/s/secret-env.txt"),
    ("xkb include paths in prose (compile-keymap --verbose)", ".ufo/s/xkb-verbose.txt"),
    ("relative listing of user .desktop names (ls -1)", ".ufo/s/relative-names.txt"),
    ("home listing in $HOME spelling", ".ufo/s/home-dollar.txt"),
    ("home listing with only 2 distinct paths", ".ufo/s/home-dupes.txt"),
    ("home paths with a space in a directory", ".ufo/s/home-space.txt"),
    ("client dump in a >16 MiB receipt (past the text cap)", ".ufo/s/big.txt"),
    ("client dump as UTF-16 (NUL in first 8 KiB)", ".ufo/s/utf16.md"),
    ("CONTROL client dump (expect R1)", ".ufo/s/clients.json"),
    ("CONTROL 12 bare /home lines (expect R4)", ".ufo/s/home-listing.txt"),
    ("CONTROL 12 absolute dir headers of ls -LRl (expect R4)", ".ufo/s/ls-lRl-tree.txt"),
]
OUTSIDE = [
    ("client dump under corpus/knowledge (round C2)",
     "corpus/knowledge/synthetic-note.md"),
    ("cache text under quality/counters (round C1 fixtures)",
     "quality/counters/synthetic-fixtures.json"),
]

proc = subprocess.run([sys.executable, "-I", GATE, "--repo", ROOT, "--rev", "HEAD"],
                      capture_output=True, text=True)
reported = {}
for line in proc.stdout.splitlines():
    if not line.startswith("FINDING "):
        continue
    fields = dict(part.split("=", 1) for part in line.split()[1:])
    reported.setdefault(fields["file"], []).append(fields["rule"])

missed = caught = 0
rows = []
for label, path in CASES:
    rules = reported.get(path)
    if rules:
        caught += 1
        rows.append(("CAUGHT", label, "+".join(rules)))
    else:
        missed += 1
        rows.append(("MISSED", label, "-"))
    print(json.dumps({"class": label, "file": path,
                      "rules": rules or []}, ensure_ascii=False))
for label, path in OUTSIDE:
    print(json.dumps({"class": label, "file": path,
                      "rules": reported.get(path) or [], "outside_ufo": True},
                     ensure_ascii=False))
print("GATE rc=%d missed=%d caught=%d files_scanned=%s"
      % (proc.returncode, missed, caught,
         [w for w in proc.stdout.split() if w.startswith("files=")][-1:]))

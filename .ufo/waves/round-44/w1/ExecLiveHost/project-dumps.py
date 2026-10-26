#!/usr/bin/env python3
"""Project the live `hyprctl` dumps to shape-only form before they enter the lane repo.

SKILL.md:332 — "Session material stays shape-only. `clients` for length/tags, never
window titles". The raw dumps carry window titles (terminal titles are session material),
PIDs, stable ids, Pango descriptions, monitor serial/make/model and workspace titles.
None of that is read by any tool or claim in this seat, so this script keeps the field
subset that is read or needed as geometry, and nothing else:

  clients      address, mapped, class, floating, size, at, monitor,
               fullscreen, fullscreenClient, fullscreenHandler
               (the round-43 precedent fetch/host-clients-r43.json shape plus the three
               state fields C1 is about)
  monitors     id, name, width, height, x, y, reserved, scale, transform, refreshRate,
               activeWorkspace {id,name}, focused, disabled
               (serial, make, model, description, modes and colour fields dropped)
  workspaces   id, name, monitor, monitorID, windows, hasfullscreen, ispersistent,
               tiledLayout
               (lastwindow and lastwindowtitle dropped — the latter is a window title)

The raw dumps' sha256 are written to raw-dumps.sha256 so the projection stays auditable
without retaining the bytes. Run with the raw dumps under a scratch path:

    python3 -I project-dumps.py --raw-clients R --raw-monitors M --raw-workspaces W
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

CLIENT_KEYS = ("address", "mapped", "class", "floating", "size", "at", "monitor",
               "fullscreen", "fullscreenClient", "fullscreenHandler")
MONITOR_KEYS = ("id", "name", "width", "height", "x", "y", "reserved", "scale",
                "transform", "refreshRate", "activeWorkspace", "focused", "disabled")
WORKSPACE_KEYS = ("id", "name", "monitor", "monitorID", "windows", "hasfullscreen",
                  "ispersistent", "tiledLayout")


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def project(items, keys):
    return [{k: c[k] for k in keys if k in c} for c in items]


def dump(obj):
    return json.dumps(obj, indent=4) + "\n"


def main(argv):
    args = {}
    i = 0
    while i < len(argv):
        if i + 1 >= len(argv) or not argv[i].startswith("--raw-"):
            print("usage: project-dumps.py --raw-clients F --raw-monitors F --raw-workspaces F")
            return 2
        args[argv[i][6:]] = argv[i + 1]
        i += 2
    if set(args) != {"clients", "monitors", "workspaces"}:
        print("usage: project-dumps.py --raw-clients F --raw-monitors F --raw-workspaces F")
        return 2
    lines = []
    for name in ("clients", "monitors", "workspaces"):
        raw = open(args[name], "rb").read()
        doc = json.loads(raw)
        keys = {"clients": CLIENT_KEYS, "monitors": MONITOR_KEYS, "workspaces": WORKSPACE_KEYS}[name]
        proj = project(doc, keys)
        out = os.path.join(HERE, "live-%s.json" % name)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(dump(proj))
        lines.append("%s raw_sha256=%s raw_bytes=%d raw_keys=%s kept=%s items=%d -> %s sha256=%s"
                     % (name, sha_bytes(raw), len(raw),
                        sorted({k for c in doc for k in c}) if name == "clients" else "-",
                        ",".join(keys), len(proj), os.path.basename(out),
                        sha_bytes(open(out, "rb").read())))
    with open(os.path.join(HERE, "raw-dumps.sha256"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

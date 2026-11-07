#!/usr/bin/env python3
"""Round-91 host replay (QUALITY 146): tools/mado-mime.py vs the installed `gio mime TYPE`, live environment.

Types: every key of the host's mimeapps.list / <desktop>-mimeapps.list / defaults.list / mimeinfo.cache files
under ~/.config, /etc/xdg, ~/.local/share/applications, /usr/local/share/applications, /usr/share/applications,
plus the left column of /usr/share/mime/{aliases,subclasses}.  gio is run with ONE argument only (read form).
Prints one line per disagreement and a summary `MADO_MIME_HOST: tool_sha256=… types=N agree=A semantic_diff=D
default_none=K`; a type with no default counts as agreeing when the tool also says none (gio prints no lists).
Exit 0 when semantic_diff == 0, else 1.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

tool = sys.argv[1]
home = os.path.expanduser("~")
desk = [d.lower() for d in os.environ.get("XDG_CURRENT_DESKTOP", "").split(":") if d]
files = []
for d in (os.path.join(home, ".config"), "/etc/xdg"):
    files += [os.path.join(d, n) for n in ["mimeapps.list"] + [f"{x}-mimeapps.list" for x in desk]]
for d in (os.path.join(home, ".local/share/applications"), "/usr/local/share/applications", "/usr/share/applications"):
    files += [os.path.join(d, n) for n in ["mimeapps.list", "defaults.list", "mimeinfo.cache"] + [f"{x}-mimeapps.list" for x in desk]]
types = set()
for f in files:
    try:
        for line in open(f, encoding="utf-8", errors="replace"):
            m = re.match(r"^\s*([A-Za-z0-9.+_-]+/[A-Za-z0-9.+_\[\]-]+)\s*=", line)
            if m:
                types.add(m.group(1))
    except OSError:
        pass
for f in ("/usr/share/mime/aliases", "/usr/share/mime/subclasses"):
    try:
        for line in open(f, encoding="utf-8", errors="replace"):
            if " " in line:
                types.add(line.split(" ", 1)[0])
    except OSError:
        pass
types = sorted(types)
tool_out = {}
for i in range(0, len(types), 200):
    r = subprocess.run([sys.executable, "-I", tool, "--json", "--"] + types[i:i + 200], capture_output=True, text=True)
    for x in json.loads(r.stdout)["results"]:
        tool_out[x["type"]] = x
DEF = re.compile(r"^Default application for \u201c.*\u201d: (.*)$")
agree = diff = none = 0
for t in types:
    g = subprocess.run(["/usr/bin/gio", "mime", t], capture_output=True, text=True).stdout.splitlines()
    m = DEF.match(g[0]) if g else None
    x = tool_out[t]
    if not m:
        none += 1
        ok = x["default"] is None
        gl = None
    else:
        lists = {"registered": [], "recommended": []}
        cur = None
        for ln in g[1:]:
            if ln == "Registered applications:":
                cur = "registered"
            elif ln == "Recommended applications:":
                cur = "recommended"
            elif ln.startswith("No "):
                cur = None
            elif ln.startswith("\t") and cur:
                lists[cur].append(ln[1:])
        gl = (m.group(1), lists["registered"], lists["recommended"])
        ok = (x["default"], x["registered"], x["recommended"]) == gl
    if ok:
        agree += 1
    else:
        diff += 1
        print(f"DIFF {t} gio={gl} tool={(x['default'], x['registered'], x['recommended'])}")
sha = hashlib.sha256(open(tool, "rb").read()).hexdigest()
print(f"MADO_MIME_HOST: tool_sha256={sha} desktops={','.join(desk) or '-'} types={len(types)} agree={agree} "
      f"semantic_diff={diff} default_none={none}")
sys.exit(1 if diff else 0)

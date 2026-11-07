#!/usr/bin/env python3
"""DRAFT: name/data interaction rows on the host DB, plus the API-only data==NULL path."""
import json
import os
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
ORACLE = os.path.join(S, "oracle")
TOOL = os.path.join(S, "tools", "mado-mimesniff.py")
HOME = os.path.join(S, "hosthome")
os.makedirs(os.path.join(HOME, ".local", "share"), exist_ok=True)
root = os.path.join(S, "hostdata2")
os.makedirs(root, exist_ok=True)

PDF = b"%PDF-1.7\n%\xe2\xe3\xcf\xd3\n" + b"\x00" * 40
PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 60
ELF = b"\x7fELF\x02\x01\x01" + b"\x00" * 60

DE = b"[Desktop Entry]\nType=Application\n"
rows = [("notes.txt", PDF), ("x.png", PDF), ("x.txt", PNG), ("image.txt", ELF),
        ("x.png", PNG), ("zz", PDF), ("x.pdf", PNG),
        ("x.desktop", DE), ("whatever.desktop", DE), ("zz.nomatch", DE)]
pairs, files, names = [], [], []
for i, (nm, data) in enumerate(rows):
    p = os.path.join(root, "d%02d.bin" % i)
    open(p, "wb").write(data)
    files.append(p)
    names.append(nm)
    pairs += ["=" + nm, p]

env = {"LC_ALL": "C", "HOME": HOME, "XDG_DATA_DIRS": "/usr/local/share/:/usr/share/"}
o = subprocess.run(["env", "-i"] + ["%s=%s" % kv for kv in env.items()] + [ORACLE] + pairs,
                   capture_output=True, text=True)
olines = o.stdout.splitlines()
print("%-12s %-14s %-30s %-30s" % ("name", "data", "oracle", "tool"))
bad = 0
for i, (nm, data) in enumerate(rows):
    lab = olines[i]
    t = subprocess.run([sys.executable, "-I", TOOL, "--json", "--home", HOME,
                        "--data-home", os.path.join(HOME, ".local", "share"),
                        "--data-dirs", "/usr/local/share/:/usr/share/", "--name", nm, files[i]],
                       capture_output=True, text=True,
                       env={"PATH": "/nonexistent-empty", "LC_ALL": "C", "HOME": HOME,
                            "XDG_DATA_HOME": os.path.join(HOME, ".local", "share"),
                            "XDG_DATA_DIRS": "/usr/local/share/:/usr/share/"})
    r = json.loads(t.stdout)["results"][0]
    got = "%s\t%d" % (r["type"], r["uncertain"])
    ok = got == lab
    bad += 0 if ok else 1
    print("%-12s %-14s %-30s %-30s %s" % (nm, data[:6].hex(), lab, got, "" if ok else "DIFF"))
print("DIFFS=%d" % bad)

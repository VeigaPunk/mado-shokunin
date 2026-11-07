#!/usr/bin/env python3
"""DRAFT host-DB probe for the r95 entry: real /usr/share/mime answers + the ignored word_size field."""
import json
import os
import struct
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
ORACLE = os.path.join(S, "oracle")
TOOL = os.path.join(S, "tools", "mado-mimesniff.py")
HOST = "/usr/share/mime/mime.cache"
HOME = os.path.join(S, "hosthome")
os.makedirs(os.path.join(HOME, ".local", "share"), exist_ok=True)

b = open(HOST, "rb").read()
u = lambda o: struct.unpack(">I", b[o:o + 4])[0]
lo = u(24)
n = u(lo)
off = u(lo + 8)
entries = []
for j in range(n):
    e = off + 16 * j
    prio, mo, nm, mlo = u(e), u(e + 4), u(e + 8), u(e + 12)
    name = b[mo:b.index(b"\0", mo)].decode()
    mls = []
    for k in range(nm):
        m = mlo + 32 * k
        start, rl, w, vl, vo, masko = u(m), u(m + 4), u(m + 8), u(m + 12), u(m + 16), u(m + 20)
        val = b[vo:vo + vl]
        mls.append(dict(start=start, rl=rl, word=w, vl=vl, val=val, mask=masko))
    entries.append(dict(prio=prio, name=name, mls=mls))

ws = [e for e in entries if any(m["word"] != 1 for m in e["mls"])]
print("HOST magic entries=%d matchlets=%d entries_with_word_gt1=%d" %
      (len(entries), sum(len(e["mls"]) for e in entries), len(ws)))
for e in ws:
    print("  word>1 entry: prio=%d mime=%s matchlets=%s" %
          (e["prio"], e["name"], [(m["start"], m["rl"], m["word"], m["val"].hex()) for m in e["mls"]]))

# data buffers: real signatures, and one synthesised from a word_size>1 matchlet
def synth(m):
    data = bytearray(b"\x00" * (m["start"] + m["rl"] + m["vl"] + 8))
    data[m["start"]:m["start"] + m["vl"]] = m["val"]
    return bytes(data)

cases = []
for name, data in [
    ("png", b"\x89PNG\r\n\x1a\n" + b"\x00" * 60),
    ("pdf", b"%PDF-1.7\n%\xe2\xe3\xcf\xd3\n"),
    ("gzip", b"\x1f\x8b\x08\x00" + b"\x00" * 60),
    ("elf", b"\x7fELF\x02\x01\x01" + b"\x00" * 60),
    ("desktop", b"[Desktop Entry]\nType=Application\n"),
    ("text", b"just some words\n"),
    ("zerosize", b""),
]:
    cases.append((name, data))

for e in ws:
    for m in e["mls"]:
        cases.append(("word%d-%s" % (m["word"], e["name"]), synth(m)))

root = os.path.join(S, "hostdata")
os.makedirs(root, exist_ok=True)
pairs = []
files = []
for name, data in cases:
    p = os.path.join(root, name.replace("/", "_") + ".bin")
    with open(p, "wb") as fh:
        fh.write(data)
    files.append(p)
    pairs += ["0", p]
    pairs += ["=zz", p]

env = {"LC_ALL": "C", "HOME": HOME, "XDG_DATA_DIRS": "/usr/local/share/:/usr/share/"}
o = subprocess.run(["env", "-i"] + ["%s=%s" % kv for kv in env.items()] + [ORACLE] + pairs,
                   capture_output=True, text=True)
olines = o.stdout.splitlines()
print("oracle rc=%d lines=%d" % (o.returncode, len(olines)))
print("%-28s %-8s %-30s %-30s" % ("case", "name", "oracle", "tool"))
bad = 0
for i, (name, data) in enumerate(cases):
    for j, nm in enumerate((None, "zz")):
        idx = 2 * i + j
        lab = olines[idx] if idx < len(olines) else "?"
        cmd = [sys.executable, "-I", TOOL, "--json", "--home", HOME,
               "--data-home", os.path.join(HOME, ".local", "share"), "--data-dirs", "/usr/local/share/:/usr/share/"]
        if nm is not None:
            cmd += ["--name", nm]
        t = subprocess.run(cmd + [files[i]], capture_output=True, text=True,
                           env={"PATH": "/nonexistent-empty", **env,
                                "XDG_DATA_HOME": os.path.join(HOME, ".local", "share")})
        if t.returncode == 0:
            r = json.loads(t.stdout)["results"][0]
            got = "%s\t%d" % (r["type"], r["uncertain"])
        else:
            got = "EXIT%d %s" % (t.returncode, (t.stdout or t.stderr).strip()[:30])
        ok = got == lab
        bad += 0 if ok else 1
        print("%-28s %-8s %-30s %-30s %s" % (name, "NULL" if nm is None else nm, lab, got, "" if ok else "DIFF"))
print("DIFFS=%d" % bad)

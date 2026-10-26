#!/usr/bin/env python3
"""CritW2Gate round-46 w1 — self-contained reproduction of the round-45 w2 gate attack.

Writes ONLY synthetic shapes (no host session material of any kind) into a throwaway
clone under /fast/scratch, commits them, and prints the gate's verdict per shape plus
probes of the gate's scan caps.

  python3 -I repro.py <scratch-clone>
"""
import base64
import importlib.util
import json
import os
import subprocess
import sys

ROOT = sys.argv[1]
GATE = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-session-material.py"
spec = importlib.util.spec_from_file_location("gate", GATE)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

P = os.path.join(ROOT, ".ufo/waves/round-46/w1/plant")

CLIENTS = ('[{"address": "0x55aa", "class": "Foot", "title": "a live window title",'
           ' "initialTitle": "Foot", "pid": 2562}]\n')
MONITORS = ('[{"name": "DP-1", "description": "Example Monitor Model ABC", "make": "Example",'
            ' "model": "ABC", "serial": "SERIAL0123456"}]\n')
SS = ('u_str ESTAB 0 0 /run/user/1000/bus 12345 * 23456 '
      'users:(("gnome-keyring-d",pid=999,fd=9))\n')

MISS = {
    "clients-renamed-keys.json": '[{"app_id": "Foot", "caption": "a live window title"}]\n',
    "clients-title-renamed.json": '[{"class": "Foot", "caption": "a live window title"}]\n',
    "clients-nested-title.json": '[{"class": "Foot", "window": {"title": "a live title"}}]\n',
    "clients.yaml": "- class: Foot\n  title: a live window title\n",
    "clients-quoted-keys.yaml": '- "class": "Foot"\n  "title": "a live window title"\n',
    "clients-plain.txt": "\tclass: Foot\n\ttitle: a live window title\n",
    "clients.csv": "address,class,title\n0x55aa,Foot,a live window title\n",
    "clients-b64.txt": base64.b64encode(CLIENTS.encode()).decode() + "\n",
    "monitors.yaml": "- name: DP-1\n  serial: SERIAL0123456\n  description: Example Monitor\n",
    "monitors-prose.md": 'It reported "serial" = "SERIAL0123456", "make" = "Example".\n',
    "monitors-plain.txt": "\tserial: SERIAL0123456\n\tdescription: Example Monitor\n",
    "ps-aux.txt": "USER PID %CPU COMMAND\nvgpnk 2562 0.6 footclient\n",
    "ps.csv": "USER,PID,COMMAND\nvgpnk,2562,footclient\n",
    "ps-escaped-ss.txt": 'users:((\\"gnome-keyring-d\\",pid=999,fd=9))\n',
    "ps-long-name.txt": 'users:(("' + "x" * 150 + '",pid=999,fd=9))\n',
    "home-ls-l.txt": "-rw-r--r-- 1 u u 4096 Oct 26 09:11 /home/someone/d00/f\n",
    "home-json-array.json": '["/home/someone/d00/f", "/home/someone/d01/f"]\n',
    "home-bullets.md": "- /home/someone/d00/f\n",
    "home-quoted.txt": "'/home/someone/d00/f'\n",
}
FP = {
    "docs-clients-shape.md": '[{"class": "ExampleApp", "title": "Example Window Title"}]\n',
    "docs-monitors-shape.md": '[{"serial": "SERIAL0000", "description": "Example Monitor"}]\n',
    "docs-ss-shape.md": 'The column looks like `users:(("example-daemon",pid=42,fd=3))`.\n',
    "docs-home-paths.md": "\n".join("/home/someone/d%02d/f" % i for i in range(12)) + "\n",
    "disk-inventory.json": ('{"blockdevices": [{"name": "nvme0n1",'
                            ' "model": "Samsung SSD 980", "serial": "S0000000"}]}\n'),
    "selftest-quoted.md": 'MONITORS_REDACTED = [{"description": "Example", "make": "Example"}]\n',
}

for rel, text in list(MISS.items()) + list(FP.items()):
    target = os.path.join(P, rel)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8") as fh:
        fh.write(text)
for rel, data in (("clients-nul.bin", b"\x00note\n" + CLIENTS.encode()),
                  ("clients-utf16.txt", CLIENTS.encode("utf-16-le")),
                  ("clients-brace-bomb.json", b"{\n" * 20000 + CLIENTS.encode())):
    with open(os.path.join(P, rel), "wb") as fh:
        fh.write(data)

subprocess.run(["git", "-C", ROOT, "add", "-A"], check=True)
top = subprocess.run(["git", "-C", ROOT, "rev-parse", "--show-toplevel"],
                     capture_output=True, text=True, check=True).stdout.strip()
assert os.path.realpath(top) == os.path.realpath(ROOT), (top, ROOT)
subprocess.run(["git", "-C", ROOT, "-c", "user.name=seat",
                "-c", "user.email=seat@scratch.invalid", "commit", "-q", "-m", "plant"],
               check=True)

print("== per-shape verdict (scan_blob, home_limit=%d) ==" % g.DEFAULT_HOME_LIMIT)
for group, table in (("MISS-expected-flagged", MISS), ("FP-expected-clean", FP)):
    caught = 0
    for rel in sorted(table):
        path = os.path.join(P, rel)
        fx = g.scan_blob(open(path, "rb").read(), g.DEFAULT_HOME_LIMIT)
        if fx:
            caught += 1
        print("%-22s %-28s %s" % (group, rel, fx if fx else "-"))
    print("%-22s caught %d/%d" % (group, caught, len(table)))
for rel in ("clients-nul.bin", "clients-utf16.txt", "clients-brace-bomb.json"):
    fx = g.scan_blob(open(os.path.join(P, rel), "rb").read(), g.DEFAULT_HOME_LIMIT)
    print("%-22s %-28s %s" % ("MISS-expected-flagged", rel, fx if fx else "-"))

print("\n== scan caps ==")
cl = b'[{"class":"Foot","title":"a live window title"}]\n'
for n in (0, 1, 19999, 20000, 20001):
    print("stray-braces=%-6d %r" % (n, g.scan_blob(b"{\n" * n + cl, 10)))
print("dump-first+20000-braces  %r" % (g.scan_blob(cl + b"{\n" * 20000, 10),))
print("dump-after-16MiB         %r" % (g.scan_blob(b"x" * (16 << 20) + cl, 10),))
print("dump-after-NUL-byte      %r" % (g.scan_blob(b"\x00\n" + cl, 10),))
print("dump-as-UTF-16LE         %r" % (g.scan_blob(cl.decode().encode("utf-16-le"), 10),))

print("\n== redaction markers ==")
for label, blob in (
    ("title=REDACTED", b'[{"class":"foot","title":"REDACTED"}]\n'),
    ("title=<redacted>", b'[{"class":"foot","title":"<redacted>"}]\n'),
    ("title=Example Window Title", b'[{"class":"ExampleApp","title":"Example Window Title"}]\n'),
    ("title=null", b'[{"class":"foot","title":null}]\n'),
    ("title=\"\"", b'[{"class":"foot","title":""}]\n'),
    ("serial=REDACTED", b'[{"serial":"REDACTED","description":"Dell U2720Q"}]\n'),
    ("serial=\"\"", b'[{"serial":"","description":"Dell U2720Q"}]\n'),
    ("serial+model=disk", b'{"blockdevices":[{"model":"Samsung SSD 980","serial":"S0000000"}]}\n'),
):
    print("%-28s %r" % (label, g.scan_blob(blob, 10)))

print("\n== R4 threshold ==")
print("ten  -> %r" % (g.scan_blob(("\n".join("/home/someone/d%02d/f" % i for i in range(10))
                                  + "\n").encode(), 10),))
print("eleven -> %r" % (g.scan_blob(("\n".join("/home/someone/d%02d/f" % i for i in range(11))
                                    + "\n").encode(), 10),))

print("\n== scope: files outside .ufo/ ==")
os.makedirs(os.path.join(ROOT, "corpus/knowledge"), exist_ok=True)
with open(os.path.join(ROOT, "corpus/knowledge/leak-prose.md"), "w") as fh:
    fh.write('It reported "serial" = "SERIAL0123456".\n' + CLIENTS + SS)
subprocess.run(["git", "-C", ROOT, "add", "-A"], check=True)
subprocess.run(["git", "-C", ROOT, "-c", "user.name=seat",
                "-c", "user.email=seat@scratch.invalid", "commit", "-q", "-m", "scope"],
               check=True)
sha, files, findings = g.run(ROOT, "HEAD")
print("corpus/knowledge/leak-prose.md findings: %r"
      % ([f for f in findings if f[0].startswith("corpus/")],))
print("gate-emitted-lines-are-the-only-interface: files=%d findings=%d" % (files, len(findings)))

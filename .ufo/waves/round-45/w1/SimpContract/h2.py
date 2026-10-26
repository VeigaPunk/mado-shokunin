#!/usr/bin/env python3
"""Constructed witnesses + setup/argv-level probes for the C1 contract (scratch only)."""
import json
import os
import struct
import subprocess
import sys
import tempfile

REF = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/l1-draft/mado-monitors.py"
SRC = open(REF, encoding="utf-8").read()
WORK = "/fast/scratch/hyaku/mado-r45/SimpContract/probe"


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


def load(src, tag):
    ns = {"__name__": tag}
    exec(compile(src, "<%s>" % tag, "exec"), ns)
    return ns


def out(ns, texts, raw):
    try:
        return "\n".join(ns["report"](raw, texts)[0]), ns["report"](raw, texts)[1]
    except Exception as e:  # noqa: BLE001
        return "EXC:%s:%s" % (type(e).__name__, e), -1


def mut(tag, old, new):
    assert SRC.count(old) == 1, (tag, SRC.count(old))
    return tag, load(SRC.replace(old, new), tag)


os.makedirs(WORK, exist_ok=True)
REFNS = load(SRC, "ref")


def mon(name, **kw):
    d = {"id": 0, "name": name, "description": "", "width": 3440, "height": 1440,
         "refreshRate": 99.997, "x": 0, "y": 0, "scale": 1, "transform": 0,
         "disabled": False, "mirrorOf": "none"}
    d.update(kw)
    return d


def probe(tag, texts, mons, mtags):
    raw = json.dumps(mons).encode()
    a = out(REFNS, texts, raw)
    print("== %s\n   cfg=%r" % (tag, texts))
    print("   ref  %r" % (a,))
    for t, ns in mtags:
        b = out(ns, texts, raw)
        print("   %-24s %s %r" % (t, "DIFF" if a != b else "same", b))


M1 = mut("M1-zpos", "    if z > 0 and whole(w / z) and whole(h / z):",
         "    if whole(w / z) and whole(h / z):")
M2 = mut("M2-cand0", "            if cand != 0 and whole(w / cand) and whole(h / cand):",
         "            if whole(w / cand) and whole(h / cand):")
M3 = mut("M3-range90", "    for i in range(1, 90):", "    for i in range(1, 91):")
M4 = mut("M4-order", "        for cand in ((k + i) / 120.0, (k - i) / 120.0):",
         "        for cand in ((k - i) / 120.0, (k + i) / 120.0):")
M5 = mut("M5-mirror-isinstance",
         "        if not (isinstance(mo, str) and len(ids) >= 1 and mo == str(ids[0])):",
         "        if not (len(ids) >= 1 and mo == str(ids[0])):")
M7 = mut("M7-mirror-idfilter",
         '        ids = [m.get("id") for m in mons if str_or_empty(m.get("name")) == rule["mirror"] and is_int(m.get("id"))]',
         '        ids = [m.get("id") for m in mons if str_or_empty(m.get("name")) == rule["mirror"]]')
M20 = mut("M20-f32rate", '    rule["rate"] = f32(float(m.group(4))) if m.group(4) is not None else 60.0',
          '    rule["rate"] = float(m.group(4)) if m.group(4) is not None else 60.0')
M21 = mut("M21-f32scale", "    s = f32(float(value))", "    s = float(value)")
M22 = mut("M22-f32cand", "                return f32(cand)", "                return cand")
M23 = mut("M23-f32z", "        return f32(z)", "        return z")
M26 = mut("M26-isfinite", "    return math.isfinite(x) and x == math.floor(x + 0.5)",
          "    return x == math.floor(x + 0.5)")
M28 = mut("M28-isint-bool", "    return isinstance(v, int) and not isinstance(v, bool)",
          "    return isinstance(v, int)")
M30 = mut("M30-addreserved-4", "        if not all(RES_RE.fullmatch(fld(i)) for i in range(2, 6)):",
          "        if not all(RES_RE.fullmatch(fld(i)) for i in range(2, 5)):")
M44 = mut("M44-scalepos", "            e = expected_scale(rule[\"scale\"], w, h) if w > 0 and h > 0 else None",
          "            e = expected_scale(rule[\"scale\"], w, h)")

# --- M3: the 89-step bound. k=210, w=h=1: only (k-90)/120 = 1.0 divides, at i=90.
probe("M3 bound 89 (rule 1.75, live 1x1 scale 1.25)", ["monitor = DP-5, , auto, 1.75\n"],
      [mon("DP-5", width=1, height=1, scale=1.25)], [M3])
# --- M4: (k+i) before (k-i); k=156, i=1, w=h=4867 -> 157/120 and 155/120 both divide.
probe("M4 order (rule 1.3, live 4867x4867 scale 1.3083333)", ["monitor = DP-5, , auto, 1.3\n"],
      [mon("DP-5", width=4867, height=4867, scale=f32(157 / 120))], [M4])
# --- M7: mirrored output whose id is not an int, mirrorOf string equal to str(id).
probe("M7 id filter (id 4.0, mirrorOf '4.0')",
      ["monitor = DP-2, 3440x1440@100, 0x0, 1, mirror, DP-5\n"],
      [mon("DP-5", id=4.0), mon("DP-2", id=9, mirrorOf="4.0")], [M7])
# --- M5: non-string mirrorOf that could compare equal to a str.
probe("M5 isinstance (mirrorOf 0, id '0'?)",
      ["monitor = DP-2, 3440x1440@100, 0x0, 1, mirror, DP-5\n"],
      [mon("DP-5", id=0), mon("DP-2", id=9, mirrorOf=0)], [M5])
# --- M20: f32 on the requested rate; window = f32 error at 999.999.
r_ref, r_mut = f32(999.999), 999.999
live = r_ref + 0.99999
probe("M20 rate f32 (999.999; live %r)" % live, ["monitor = DP-5, 1000x1000@999.999, 0x0, 1\n"],
      [mon("DP-5", width=1000, height=1000, refreshRate=live)], [M20])
# --- M22: loop candidate 31/120 at k=32, w=h=31; E differs by f32 error.
cand = 31 / 120
probe("M22 cand f32 (rule 0.267, live 31x31 scale %r)" % (f32(cand) - 1e-4 + abs(f32(cand) - cand) / 2),
      ["monitor = DP-5, , auto, 0.267\n"],
      [mon("DP-5", width=31, height=31, scale=f32(cand) - 1e-4 + abs(f32(cand) - cand) / 2)], [M22])
# --- M23: K/120 branch at k=121, w=h=121.
z = 121 / 120
probe("M23 z f32 (rule 1.008333, live 121x121 scale %r)" % (z - 1e-4 + abs(f32(z) - z) / 2),
      ["monitor = DP-5, , auto, 1.008333\n"],
      [mon("DP-5", width=121, height=121, scale=z - 1e-4 + abs(f32(z) - z) / 2)], [M23])
# --- M21: scale f32 at parse; w = 2**50 * f32(1.3) makes whole(w/f32) but not whole(w/1.3).
s32 = f32(1.3)
w21 = 2 ** 50
w21 = int(w21 * s32) if (w21 * s32).is_integer() else None
print("   s32=%r  2**50*s32=%r integer=%s" % (s32, 2 ** 50 * s32, (2 ** 50 * s32).is_integer()))
if w21 is not None:
    E = REFNS["expected_scale"](s32, w21, w21)
    E2 = REFNS["expected_scale"](2 ** 50 * s32, w21, w21)
    print("   w21=%d E_ref=%r E_mut=%r" % (w21, E, E2))
    if E is not None and E2 is not None and E != E2:
        live21 = E - 1e-4 + abs(E2 - E) / 2 if E2 > E else E - 1e-4 - abs(E2 - E) / 2
        probe("M21 scale f32 (w=%d)" % w21, ["monitor = DP-5, , auto, 1.3\n"],
              [mon("DP-5", width=w21, height=w21, scale=live21)], [M21])
# --- M28: bool is an int; live transform True vs rule transform 1.
probe("M28 is_int bool (transform True, rule transform 1)",
      ["monitor = DP-5, , auto, 1, transform, 1\n"],
      [mon("DP-5", transform=True)], [M28])
probe("M28b is_int bool (width True, rule 1x1)",
      ["monitor = DP-5, 1x1@60, 0x0, 1\n"],
      [mon("DP-5", width=True, height=1, refreshRate=60.0)], [M28])
# --- M30: addreserved with only three numeric fields.
probe("M30 addreserved fields 2-5 (only 3 numbers)",
      ["monitor = DP-5, addreserved, 10, 0, 0\n"], [mon("DP-5")], [M30])
# --- M44: live width/height 0 -> scale not compared.
probe("M44 w>0 guard (live 0x0, rule scale 2, live scale 1)",
      ["monitor = DP-5, , auto, 2\n"], [mon("DP-5", width=0, height=0, scale=1)], [M44])
# --- M1/M2 brute sweep: every (k, w, h) reachable shape.
ns1, ns2 = M1[1], M2[1]
diff1 = diff2 = 0
for k in range(30, 1201):
    s = k / 120.0
    for w in (1, 2, 3, 5, 7, 11, 31, 121, 155, 157, 1920, 2560, 3440, 4867, 1048577):
        for h in (1, w):
            a = REFNS["expected_scale"](s, w, h)
            if a != ns1["expected_scale"](s, w, h):
                diff1 += 1
                print("   M1 DIFF k=%d w=%d h=%d %r %r" % (k, w, h, a, ns1["expected_scale"](s, w, h)))
            if a != ns2["expected_scale"](s, w, h):
                diff2 += 1
                print("   M2 DIFF k=%d w=%d h=%d %r %r" % (k, w, h, a, ns2["expected_scale"](s, w, h)))
print("sweep: k=30..1200 x 15 widths -> M1 diffs=%d M2 diffs=%d (cand==0 would need k<=89)"
      % (diff1, diff2))

# --- setup-level probes (subprocess): S_ISREG removal, dup --monitors, huge ints.
def run(argv, stdin=b"", timeout=8, tool=REF, cwd=WORK):
    try:
        p = subprocess.run([sys.executable, "-I", tool] + argv, input=stdin, capture_output=True,
                           timeout=timeout, cwd=cwd)
        return p.returncode, p.stdout.decode(), p.stderr.decode()[:160]
    except subprocess.TimeoutExpired:
        return "TIMEOUT", "", ""


M24 = mut("M24-nosreg",
          '        if not stat.S_ISREG(os.fstat(fd).st_mode):\n            raise Setup("unreadable")\n', "")
t24 = os.path.join(WORK, "m24.py")
open(t24, "w").write(SRC.replace(
    '        if not stat.S_ISREG(os.fstat(fd).st_mode):\n            raise Setup("unreadable")\n', ""))
mpath = os.path.join(WORK, "mons.json")
open(mpath, "w").write(json.dumps([mon("DP-5")]))
cfg = os.path.join(WORK, "c.conf")
open(cfg, "w").write("monitor = DP-5, 3440x1440@100, 0x0, 1\n")
print("== M24 S_ISREG via /dev/null --config")
print("   ref  %r" % (run(["--monitors", mpath, "--config", "/dev/null"]),))
print("   mut  %r" % (run(["--monitors", mpath, "--config", "/dev/null"], tool=t24),))
fifo = os.path.join(WORK, "fifo")
if not os.path.exists(fifo):
    os.mkfifo(fifo)
M25 = mut("M25-nonblock", "        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)",
          "        fd = os.open(path, os.O_RDONLY)")
t25 = os.path.join(WORK, "m25.py")
open(t25, "w").write(SRC.replace("        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)",
                                 "        fd = os.open(path, os.O_RDONLY)"))
print("== M25 O_NONBLOCK via FIFO --config (timeout 3s)")
print("   ref  %r" % (run(["--monitors", mpath, "--config", fifo], timeout=3),))
print("   mut  %r" % (run(["--monitors", mpath, "--config", fifo], timeout=3, tool=t25),))
print("== M41 dup --monitors")
print("   ref  %r" % (run(["--monitors", mpath, "--monitors", mpath, "--config", cfg]),))
M41 = mut("M41-dupmon", '        if flag == "--monitors" and monitors is None:',
          '        if flag == "--monitors":')
t41 = os.path.join(WORK, "m41.py")
open(t41, "w").write(SRC.replace('        if flag == "--monitors" and monitors is None:',
                                 '        if flag == "--monitors":'))
print("   mut  %r" % (run(["--monitors", mpath, "--monitors", mpath, "--config", cfg], tool=t41),))
print("== huge-int live values (docstring: wrong JSON type only fails its field)")
for key, val in (("width", 10 ** 400), ("refreshRate", 10 ** 400), ("scale", 10 ** 400),
                 ("x", 10 ** 400)):
    d = mon("DP-5", **{key: val})
    open(mpath, "w").write(json.dumps([d]))
    print("   %-12s %r" % (key, run(["--monitors", mpath, "--config", cfg])))

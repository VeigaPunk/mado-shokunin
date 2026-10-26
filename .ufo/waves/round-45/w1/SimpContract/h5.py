#!/usr/bin/env python3
"""Confirmed witness pairs for the f32 family (M21/M22/M23) and the setup/argv probes."""
import json
import struct

REF = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/l1-draft/mado-monitors.py"
SRC = open(REF, encoding="utf-8").read()


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


def load(src, tag):
    ns = {"__name__": tag}
    exec(compile(src, "<%s>" % tag, "exec"), ns)
    return ns


def out(ns, texts, raw):
    try:
        lines, rc = ns["report"](raw, texts)
        return "\n".join(lines), rc
    except Exception as e:  # noqa: BLE001
        return "EXC:%s:%s" % (type(e).__name__, e), -1


def mk(name="X", **kw):
    d = {"id": 0, "name": name, "description": "", "width": 3440, "height": 1440,
         "refreshRate": 99.997, "x": 0, "y": 0, "scale": 1, "transform": 0,
         "disabled": False, "mirrorOf": "none"}
    d.update(kw)
    return d


R = load(SRC, "ref")
MUT = {
    "M20-rate-f32": ('    rule["rate"] = f32(float(m.group(4))) if m.group(4) is not None else 60.0',
                     '    rule["rate"] = float(m.group(4)) if m.group(4) is not None else 60.0'),
    "M21-scale-f32": ("    s = f32(float(value))", "    s = float(value)"),
    "M22-cand-f32": ("                return f32(cand)", "                return cand"),
    "M23-z-f32": ("        return f32(z)", "        return z"),
    "M5-mirror-isinstance": ('        if not (isinstance(mo, str) and len(ids) >= 1 and mo == str(ids[0])):',
                             '        if not (len(ids) >= 1 and mo == str(ids[0])):'),
}
N = {k: load(SRC.replace(*v), k) for k, v in MUT.items()}


def probe(tag, texts, mons):
    raw = json.dumps(mons).encode()
    a = out(N.get(tag, R), texts, raw) if tag not in N else out(R, texts, raw)
    b = out(N[tag], texts, raw) if tag in N else None
    print("### %s\nconfig=%r\ndump=%s" % (tag, texts, raw.decode()))
    print("ref: rc=%d\n%s" % (a[1], a[0]))
    if b:
        print("mut: rc=%d\n%s" % (b[1], b[0]))
        print("differs=%s\n" % (a != b))


r = R["new_rule"]("X")
R["parse_scale"](r, "1.3")
s = r["scale"]
e_ref = R["expected_scale"](s, 1463669825208320, 1463669825208320)
e_mut = N["M21-scale-f32"]["expected_scale"](s, 1463669825208320, 1463669825208320)
print("# M21: E_ref=%r E_mut=%r" % (e_ref, e_mut))
probe("M21-scale-f32", ["monitor = DP-5, , auto, 1.3\n"],
      [mk("DP-5", width=1463669825208320, height=1463669825208320, scale=e_ref)])
r = R["new_rule"]("X")
R["parse_scale"](r, "1.3")
s = r["scale"]
a = N["M22-cand-f32"]["expected_scale"](s, 3440, 1440)
b = R["expected_scale"](s, 3440, 1440)
print("# M22: E_ref=%r E_mut=%r live=%r" % (b, a, b + 1e-4 + (a - b) / 2))
probe("M22-cand-f32", ["monitor = DP-5, , auto, 1.3\n"],
      [mk("DP-5", width=3440, height=1440, scale=b + 1e-4 + (a - b) / 2)])
r = R["new_rule"]("X")
R["parse_scale"](r, "50.008333")
s = r["scale"]
a = N["M23-z-f32"]["expected_scale"](s, 6001, 6001)
b = R["expected_scale"](s, 6001, 6001)
print("# M23: E_ref=%r E_mut=%r live=%r" % (b, a, b + 1e-4 + (a - b) / 2))
probe("M23-z-f32", ["monitor = DP-5, , auto, 50.008333\n"],
      [mk("DP-5", width=6001, height=6001, scale=b + 1e-4 + (a - b) / 2)])
probe("M20-rate-f32", ["monitor = DP-5, 1000x1000@999.999, 0x0, 1\n"],
      [mk("DP-5", width=1000, height=1000, refreshRate=f32(999.999) + 0.99999)])
probe("M5-mirror-isinstance", ["monitor = DP-2, 3440x1440@100, 0x0, 1, mirror, DP-5\n"],
      [mk("DP-5", id=0), dict(mk("DP-2", mirrorOf=0), id=9)])

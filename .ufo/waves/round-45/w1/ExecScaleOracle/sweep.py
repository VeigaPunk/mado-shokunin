#!/usr/bin/env python3
"""sweep.py - reachability sweep for the branches the main grid cannot prove absent:
the `down == 0` division (std::round(inf) == inf would accept scale 0), the negative
`scaleDown` at i > k, and the "no clean divisor" fallback of Hyprland (m_scale =
getDefaultScale()) versus the tool's `None` ("scale is not compared").

Sizes: the 46 curated modes plus 400 random ones; scales: the exact 1/120 grid k=30..360.
Reports, per k, the C++ state counts and whether any accepted scale was <= 0.
"""
import importlib.util
import json
import random
import struct
import subprocess
import sys

DRAFT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/l1-draft/mado-monitors.py"
BIN = sys.argv[1]
OUT = sys.argv[2]

spec = importlib.util.spec_from_file_location("mado", DRAFT)
mado = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mado)
expected_scale = mado.expected_scale

f32 = lambda t: struct.unpack("<f", struct.pack("<f", float(t)))[0]
bits = lambda x: struct.unpack("<I", struct.pack("<f", x))[0]

SIZES = [(640, 480), (800, 600), (1024, 768), (1024, 600), (1280, 720), (1280, 800), (1280, 1024), (1280, 480),
         (1366, 768), (1365, 767), (1440, 900), (1440, 2560), (1600, 900), (1600, 1200), (1680, 1050),
         (1920, 1080), (1919, 1079), (1920, 1200), (1920, 1440), (2048, 1152), (2160, 1440), (2560, 1080),
         (2560, 1440), (2560, 1600), (2560, 1920), (2880, 1800), (3200, 1800), (3440, 1440), (3441, 1439),
         (3840, 1080), (3840, 1600), (3840, 2160), (3840, 2400), (4096, 2160), (4096, 2304), (5120, 1440),
         (5120, 2160), (5120, 2880), (6016, 3384), (7680, 4320), (1080, 1920), (768, 1366), (1000, 1000),
         (1234, 567), (999, 777)]
rng = random.Random(45120)
for _ in range(400):
    SIZES.append((rng.randrange(320, 8001), rng.randrange(200, 4321)))


def exact_text(k):
    v = f32("%.9f" % (k / 120.0))
    for d in range(1, 10):
        t = "%.*f" % (d, k / 120.0)
        if f32(t) == v:
            return t, v
    return "%.9g" % (k / 120.0), v


scales = [(k,) + exact_text(k) for k in range(30, 361)]
cases = [(k, t, w, h) for k, t, _v in scales for w, h in SIZES]
inp = "".join("%s %d %d\n" % (t, w, h) for _k, t, w, h in cases)
lines = subprocess.run([BIN], input=inp, capture_output=True, text=True, check=True).stdout.split("\n")
assert len(lines) - 1 == len(cases)

per_k = {}
bad = []
mism = []
for (k, t, w, h), ln in zip(cases, lines):
    sb, rb, st = ln.split()
    rb, st = int(rb, 16), int(st)
    cv = struct.unpack("<f", struct.pack("<I", rb))[0]
    d = per_k.setdefault(k, {"n": 0, "corrected": 0, "untouched": 0, "fallback": 0, "nonpositive": 0})
    d["n"] += 1
    d["corrected" if st == 1 else "untouched" if st == 2 else "fallback"] += 1
    if st != 0 and cv <= 0:
        d["nonpositive"] += 1
        bad.append({"k": k, "text": t, "w": w, "h": h, "cpp": cv})
    e = expected_scale(f32(t), w, h)
    if (st == 0) != (e is None):
        mism.append({"k": k, "w": w, "h": h, "cpp_state": st, "py": e, "kind": "fallback-mismatch"})
    elif st != 0 and bits(cv) != bits(e):
        mism.append({"k": k, "w": w, "h": h, "cpp": cv, "py": e, "kind": "value-mismatch"})

fallback_ks = sorted(k for k, d in per_k.items() if d["fallback"])
positive_ks = sorted(k for k, d in per_k.items() if d["fallback"] == 0)
res = {
    "cases": len(cases),
    "sizes": len(SIZES),
    "nonpositive_accepted": bad[:10],
    "nonpositive_count": len(bad),
    "mismatches": mism[:10],
    "mismatch_count": len(mism),
    "k_with_fallback": {"min": fallback_ks[0] if fallback_ks else None,
                        "max": fallback_ks[-1] if fallback_ks else None,
                        "count": len(fallback_ks),
                        "first_ten": fallback_ks[:10]},
    "k_never_fallback": {"max": positive_ks[-1] if positive_ks else None, "count": len(positive_ks)},
    "per_k_tail": {str(k): per_k[k] for k in sorted(per_k)[-4:]},
    "per_k_head": {str(k): per_k[k] for k in sorted(per_k)[:4]},
}
with open(OUT, "w") as fh:
    json.dump({"summary": res, "per_k": {str(k): v for k, v in sorted(per_k.items())}}, fh, indent=1)
print(json.dumps(res, indent=1))

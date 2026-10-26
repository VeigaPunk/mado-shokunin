#!/usr/bin/env python3
"""Differential probes: run a tool on an input the fixtures do not cover, in the counter's own environment."""
import json
import os
import subprocess
import sys
import tempfile

S = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(S, "probes")


def M(name, w=3440, h=1440, rr=99.997, x=0, y=0, scale=1, transform=0, disabled=False, mirror="none",
      desc="", mid=0):
    return {"id": mid, "name": name, "description": desc, "width": w, "height": h, "refreshRate": rr,
            "x": x, "y": y, "scale": scale, "transform": transform, "disabled": disabled, "mirrorOf": mirror}


def run(tool, configs, dump, stdin=False):
    os.makedirs(WORK, exist_ok=True)
    d = tempfile.mkdtemp(dir=WORK, prefix="p-")
    home = os.path.join(d, "home")
    os.makedirs(home)
    raw = dump if isinstance(dump, bytes) else json.dumps(dump, indent=2).encode()
    dp = os.path.join(d, "monitors.json")
    with open(dp, "wb") as f:
        f.write(raw)
    args = ["--monitors", "-"] if stdin else ["--monitors", dp]
    data = raw if stdin else None
    for k, t in enumerate(configs):
        cp = os.path.join(d, "c%d.conf" % k)
        with open(cp, "w") as f:
            f.write(t)
        args += ["--config", cp]
    env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "HOME": home,
           "HYPRLAND_INSTANCE_SIGNATURE": "mado-r45-fixture"}
    p = subprocess.run([sys.executable, "-I", tool] + args, input=data, capture_output=True,
                       cwd=d, env=env, timeout=30)
    return p.returncode, p.stdout.decode("utf-8", "replace").rstrip("\n").split("\n")


PROBES = [
    ("scale-1.4-needs-correction", "cheat-scale-table.py",
     ["monitor = DP-5, 2560x1440@60, 0x0, 1.4\n"],
     [M("DP-5", w=2560, rr=59.951, scale=1.4)]),
    ("icc-key-is-modelled", "cheat-key-set.py",
     ["monitor = DP-5, 3440x1440@100, 0x0, 1, icc, /usr/share/color/icc/x.icc\n"],
     [M("DP-5")]),
    ("v2-block-beats-differ", "cheat-verdict-order.py",
     ["monitorv2 {\n  output = DP-5\n  mode = 1920x1080@60\n}\nmonitor = DP-5, 1920x1080@60, 0x0, 1\n"],
     [M("DP-5")]),
    ("mirror-points-at-third-output", "cheat-mirror-by-id.py",
     ["monitor = DP-5, 3440x1440@100, 0x0, 1\n"
      "monitor = eDP-7, 3440x1440@100, 0x0, 1, mirror, DP-5\n"],
     [M("DP-5", mid=4), M("eDP-7", mid=5, mirror="6"), M("DVI-D-5", w=1920, h=1080, rr=60.0, x=3440, mid=6)]),
    ("addreserved-fields-validated", "cheat-addreserved-novalidation.py",
     ["monitor = DP-5, addreserved, 10x, 0, 0, 0\n"],
     [M("DP-5")]),
    ("desc-text-space-stripped", "cheat-desc-text.py",
     ["monitor = desc: DP-5, 3440x1440@100, 0x0, 1\n"],
     [M("DP-5", desc="DP-5 0x0001")]),
    ("desc-empty-is-a-wildcard", "cheat-desc-text.py",
     ["monitor = desc:, preferred, auto, auto\n"],
     [M("DP-5", w=1920, h=1080, rr=60.0, scale=1.25)]),
    ("rate-165-is-inside-the-bound", "cheat-rate-set.py",
     ["monitor = DP-5, 2560x1440@165, 0x0, 1\n"],
     [M("DP-5", w=2560, rr=164.5)]),
    ("long-description-is-not-in-the-dump", "cheat-desc-long.py",
     ["monitor = desc:Dell Inc. 6AHUHV, 3440x1440@100, 0x0, 1\n"],
     [dict(M("DP-5", desc="X"), longDescription="Dell Inc. 6AHUHV panel")]),
    ("new-name-not-in-any-fixture", "cheat-table45.py",
     ["monitor = DP-6, 1920x1080@60, 0x0, 1\n"],
     [M("DP-6", w=1920, h=1080, rr=60.0)]),
    ("oracle-on-an-uncovered-input", "cheat-scorer-oracle.py",
     ["monitor = DP-6, 1920x1080@60, 0x0, 1\n"],
     [M("DP-6", w=1920, h=1080, rr=60.0)]),
]


def main():
    ref = os.path.join(S, "ref.py")
    for label, cheat, cfgs, dump in PROBES:
        rc0, out0 = run(ref, cfgs, dump)
        rc1, out1 = run(os.path.join(S, cheat), cfgs, dump)
        print("== %s [%s]" % (label, cheat))
        print("   ref   rc=%d %s" % (rc0, " | ".join(out0)))
        print("   cheat rc=%d %s" % (rc1, " | ".join(out1)))
        print("   same=%s" % (out0 == out1 and rc0 == rc1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

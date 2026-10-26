#!/usr/bin/env python3
"""Diff my mado-globals.py vs the delivered tool on the committed journal +
200 random mutations. Usage: python3 -I fuzz-diff.py"""
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
JOURNAL = os.path.join(HERE, "journal-committed.txt")
MY = os.path.join(HERE, "mado-globals.py")
DV = os.path.join(HERE, "delivered-mado-globals.py")

JUNK = [
    "Oct 25 13:16:45 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  | Got interface: wl_seat (ver 1)",
    "2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [log]  | Got interface: wl_seat (ver 1)",
    "2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG] | Got interface: wl_seat (ver 1)",
    "2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  | Got interface: wl-seat (ver 1)",
    "2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  | Got interface: wl_seat (ver 1000000)",
    "2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  | Got interface: wl_seat (ver 1) trailing",
    "2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  | Got interface: wl_seat (ver 1)\r",
    "2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [INFO]  | Got interface: wl_seat (ver 1)",
    "-- Boot 505d949ab80da5c02276127111011cd1 --",
    "-- Boot zzzd949ab80da5c02276127111011cd1 --",
    "2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  | Got interface: wl_seat (ver 1)",
    "2026-10-25T13:16:45+00:00 h\uFFFdst xdg-desktop-portal-hyprland[1918]: [LOG]  | Got interface: wl_seat (ver 1)",
    "random junk that means nothing",
    "",
    "MADO_GLOBALS: sessions=1",
]

def mutate_lines(lines, rng):
    out = list(lines)
    op = rng.randrange(11)
    if not out:
        out = [""]
    i = rng.randrange(len(out))
    if op == 0:
        del out[i]
    elif op == 1:
        out.insert(i, out[i])
    elif op == 2:
        j = rng.randrange(len(out))
        out[i], out[j] = out[j], out[i]
    elif op == 3:
        out.insert(i, rng.choice(JUNK))
    elif op == 4 and out[i]:
        # mutate timestamp / pid / ver digits randomly
        t = list(out[i])
        k = rng.randrange(len(t))
        t[k] = rng.choice("0123456789abcxyzTZ+-:._ ")
        out[i] = "".join(t)
    elif op == 5 and out[i]:
        t = list(out[i])
        for _ in range(rng.randrange(1, 4)):
            k = rng.randrange(len(t))
            t[k] = rng.choice(" \t\xa0")
        out[i] = "".join(t)
    elif op == 6:
        if out[i].startswith("-- Boot "):
            out[i] = "-- Boot %032x --" % rng.getrandbits(128)
        elif out[i].startswith("-- Boot"):
            out[i] = "-- Boot 505d949ab80da5c02276127111011cd1 --"
        else:
            out.insert(i, "-- Boot 505d949ab80da5c02276127111011cd1 --")
    elif op == 7:
        if out[i]:
            out[i] = out[i] + rng.choice([" ", "  ", "\t", " x", "\r"])
    elif op == 8:
        # drop a chunk of a line
        if len(out[i]) > 5:
            a = rng.randrange(len(out[i]) - 2)
            b = a + rng.randrange(1, min(8, len(out[i]) - a))
            out[i] = out[i][:a] + out[i][b:]
    elif op == 9:
        # replace an advert with an almost-advert variant
        if "Got interface:" in out[i]:
            out[i] = rng.choice(JUNK)
        else:
            out.insert(i, rng.choice(JUNK))
    else:
        out.append(rng.choice(JUNK))
    return out

def run(tool, path, flags):
    r = subprocess.run([sys.executable, "-I", tool, "--journal-file", path] + flags,
                       capture_output=True, text=True)
    return r.returncode, r.stdout

def main():
    base = open(JOURNAL, "rb").read()
    rng = random.Random(20261025)
    tmpdir = "/tmp/mado-fuzz"
    os.makedirs(tmpdir, exist_ok=True)
    diffs = []
    totals = {"same": 0, "diff": 0}
    flagsets = [[], ["--diff"], ["--expect", "wl_output"], ["--diff", "--expect", "hyprland_focus_grab_manager_v1"]]
    # base journal first
    p = os.path.join(tmpdir, "base.txt")
    open(p, "wb").write(base)
    for flags in flagsets:
        r1 = run(MY, p, flags)
        r2 = run(DV, p, flags)
        if r1 == r2:
            totals["same"] += 1
        else:
            totals["diff"] += 1
            diffs.append(("base", flags, r1, r2))
    lines = base.decode("utf-8", "replace").split("\n")
    for m in range(200):
        ml = mutate_lines(lines, rng)
        text = "\n".join(ml)
        p = os.path.join(tmpdir, "mut_%03d.txt" % m)
        open(p, "wb").write(text.encode("utf-8", "replace"))
        flags = flagsets[m % len(flagsets)]
        r1 = run(MY, p, flags)
        r2 = run(DV, p, flags)
        if r1 == r2:
            totals["same"] += 1
        else:
            totals["diff"] += 1
            diffs.append(("mut_%03d" % m, flags, r1, r2))
    print("TOTALS", totals)
    for name, flags, r1, r2 in diffs[:12]:
        print("DIFF", name, flags)
        print("  my rc=%d" % r1[0])
        print("  dv rc=%d" % r2[0])
        ol1 = r1[1].split("\n")
        ol2 = r2[1].split("\n")
        for a, b in zip(ol1, ol2):
            if a != b:
                print("   my:", a[:140])
                print("   dv:", b[:140])
                break
    with open(os.path.join(HERE, "fuzz-summary.json"), "w") as fh:
        import json
        json.dump({"totals": totals, "diff_count": len(diffs)}, fh)
    return 1 if diffs else 0

if __name__ == "__main__":
    sys.exit(main())

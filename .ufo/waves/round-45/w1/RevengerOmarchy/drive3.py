#!/usr/bin/env python3
"""Driver 3: the real "uncomment a preset and leave the default in place" combinations,
derived from omarchy's shipped bytes. Read-only."""
import hashlib
import json
import pathlib
import subprocess
import sys

OMARCHY = pathlib.Path("/home/vgpnk/.local/share/omarchy/config/hypr/monitors.conf")
TOOL = pathlib.Path(__file__).resolve().parent / "mado-monitors.py"
W = pathlib.Path(__file__).resolve().parent / "w3"


def mon(name, w, h, rate, x, y, scale, transform=0, disabled=False, mirror="none", mid=0):
    return {"id": mid, "name": name, "description": "Fake Corp 0x0000 SN00000",
            "make": "Fake Corp", "model": "0x0000", "serial": "SN00000",
            "width": w, "height": h, "refreshRate": rate, "x": x, "y": y,
            "scale": scale, "transform": transform, "disabled": disabled,
            "mirrorOf": mirror}


def variant(src, uncomment):
    out = []
    for i, l in enumerate(src, 1):
        if i in uncomment and l.startswith("# "):
            l = l[2:]
        out.append(l)
    return "\n".join(out).rstrip("\n") + "\n"


def run(tag, conf, dump, note):
    d = W / tag
    d.mkdir(parents=True, exist_ok=True)
    p = d / "monitors.conf"
    p.write_text(conf)
    m = d / "mons.json"
    m.write_text(json.dumps(dump))
    r = subprocess.run([sys.executable, "-I", str(TOOL), "--monitors", str(m), "--config", str(p)],
                       capture_output=True, text=True)
    print(f"### {tag} exit={r.returncode} ({note})")
    for i, l in enumerate(conf.splitlines(), 1):
        if l.strip() and not l.lstrip().startswith("#"):
            print(f"#   active {i:3d}| {l}")
    for l in r.stdout.rstrip("\n").splitlines():
        print(l)
    if r.stderr.strip():
        print("STDERR:", r.stderr.strip())
    print()
    return {"tag": tag, "exit": r.returncode, "note": note,
            "stdout": r.stdout.rstrip("\n").splitlines(),
            "active": [f"{i}:{l}" for i, l in enumerate(conf.splitlines(), 1)
                       if l.strip() and not l.lstrip().startswith("#")]}


def main():
    W.mkdir(parents=True, exist_ok=True)
    src = OMARCHY.read_text().splitlines()
    print(f"# shipped sha256 {hashlib.sha256(OMARCHY.read_bytes()).hexdigest()}\n")
    host = [mon("DP-1", 3440, 1440, 99.99700, 0, 0, 1)]
    out = []
    out.append(run("E01_both_fractional", variant(src, (10, 11)), host,
                   "default line 7 PLUS uncommented 1.6 catch-all (lines 10-11)"))
    out.append(run("E02_both_1x", variant(src, (15, 16)), host,
                   "default line 7 PLUS uncommented 1x catch-all (lines 15-16)"))
    out.append(run("E03_ghost_shipped_way", variant(src, (26,)), host + [
        mon("DP-2", 2560, 1440, 143.91200, 3440, 0, 1, disabled=True, mid=1)],
        "default line 7 PLUS uncommented ghost-disable line 26"))
    out.append(run("E04_apple_plus_default", variant(src, (22, 23)), [
        mon("DP-5", 6016, 3384, 59.99700, 0, 0, 2, mid=0),
        mon("eDP-1", 2880, 1920, 119.99900, 3008, 0, 2, mid=1)],
        "default line 7 PLUS both Apple examples"))
    out.append(run("E05_portrait_plus_default", variant(src, (19,)), [
        mon("DP-1", 3440, 1440, 99.99700, 0, 0, 1, mid=0),
        mon("DP-2", 1440, 2560, 59.95000, 3440, 0, 1, transform=1, mid=1)],
        "default line 7 PLUS portrait example line 19"))
    out.append(run("E06_fractional_pair_full", variant(src, (6, 7, 10, 11)), host,
                   "both catch-alls active, and both GDK_SCALE envs active (lines 6,7,10,11)"))
    json.dump(out, (W / "results.json").open("w"), indent=1)


if __name__ == "__main__":
    main()

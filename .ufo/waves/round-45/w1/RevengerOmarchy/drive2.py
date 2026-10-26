#!/usr/bin/env python3
"""Driver 2: omarchy's multi-file monitor-rule reality (monitors.conf + toggles/hypr/*.conf),
host-style conf, and the catch-all's only comparable field. Read-only inputs."""
import hashlib
import json
import pathlib
import subprocess
import sys

OMARCHY = pathlib.Path("/home/vgpnk/.local/share/omarchy")
HOST_CONF = pathlib.Path("/home/vgpnk/.config/hypr/monitors.conf")
TOOL = pathlib.Path(__file__).resolve().parent / "mado-monitors.py"
W = pathlib.Path(__file__).resolve().parent / "w2"


def mon(name, w, h, rate, x, y, scale, transform=0, disabled=False, mirror="none", mid=0):
    return {"id": mid, "name": name, "description": "Fake Corp 0x0000 SN00000",
            "make": "Fake Corp", "model": "0x0000", "serial": "SN00000",
            "width": w, "height": h, "refreshRate": rate, "x": x, "y": y,
            "scale": scale, "transform": transform, "disabled": disabled,
            "mirrorOf": mirror}


def run(tag, confs, dump, note=""):
    d = W / tag
    d.mkdir(parents=True, exist_ok=True)
    paths = []
    for i, text in enumerate(confs):
        p = d / f"{i}-{tag}.conf"
        p.write_text(text)
        paths.append((p, own_name := text[:0] or p.name))
    mons = d / "mons.json"
    mons.write_text(json.dumps(dump))
    cmd = [sys.executable, "-I", str(TOOL), "--monitors", str(mons)]
    for p, _ in paths:
        cmd += ["--config", str(p)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(f"### {tag} exit={r.returncode} ({note})")
    for p, _ in paths:
        print(f"#   config {p.name}: {p.read_text().strip().splitlines()[-1]!r}")
    for line in r.stdout.rstrip("\n").splitlines():
        print(line)
    if r.stderr.strip():
        print("STDERR:", r.stderr.strip())
    print()
    return {"tag": tag, "exit": r.returncode, "note": note,
            "stdout": r.stdout.rstrip("\n").splitlines(), "stderr": r.stderr.strip()}


def main():
    W.mkdir(parents=True, exist_ok=True)
    shipped = (OMARCHY / "config/hypr/monitors.conf").read_text()
    toggle_disable = "monitor=eDP-1,disable\n"
    toggle_mirror = "monitor=DP-2, preferred, auto, 1, mirror, eDP-1\n"
    host = HOST_CONF.read_text()
    print(f"# shipped sha256 {hashlib.sha256(shipped.encode()).hexdigest()}")
    print(f"# host conf sha256 {hashlib.sha256(host.encode()).hexdigest()}")
    print(f"# tool sha256 {hashlib.sha256(TOOL.read_bytes()).hexdigest()}\n")
    out = []
    laptop_live = [mon("eDP-1", 2880, 1920, 119.99900, 0, 0, 2, mid=1)]
    laptop_off = [mon("eDP-1", 2880, 1920, 119.99900, 0, 0, 2, disabled=True, mid=1)]
    out.append(run("D01_disable_toggle_applied", [shipped, toggle_disable],
                   [mon("DP-1", 3440, 1440, 99.99700, 0, 0, 1, mid=0)] + laptop_off,
                   "shipped monitors.conf + omarchy internal-monitor-disable toggle, eDP-1 off"))
    out.append(run("D02_disable_toggle_not_applied", [shipped, toggle_disable],
                   [mon("DP-1", 3440, 1440, 99.99700, 0, 0, 1, mid=0)] + laptop_live,
                   "toggle present but eDP-1 still lit"))
    user_edp = shipped.replace("# monitor = eDP-1, 2880x1920@120, auto, 2",
                               "monitor = eDP-1, 2880x1920@120, auto, 2")
    out.append(run("D03_erase_on_add_selector", [user_edp, toggle_disable],
                   [mon("DP-1", 3440, 1440, 99.99700, 0, 0, 1, mid=0)] + laptop_off,
                   "explicit eDP-1 rule in monitors.conf, later same-selector disable toggle"))
    out.append(run("D04_monitors_conf_only_mirror", [shipped, toggle_mirror],
                   [mon("eDP-1", 2880, 1920, 119.99900, 0, 0, 2, mid=1),
                    mon("DP-2", 2880, 1920, 119.99900, 0, 0, 1, mirror="1", mid=2)],
                   "mirror toggle applied over the catch-all"))
    port_host = [mon("DP-1", 3440, 1440, 99.99700, 0, 0, 1)]
    out.append(run("D05_host_conf", [host], port_host, "host ~/.config/hypr/monitors.conf as shipped of this host"))
    out.append(run("D06_catchall_transform_rotated", [shipped],
                   [mon("DP-1", 3440, 1440, 99.99700, 0, 0, 1, transform=1)],
                   "catch-all rule, output rotated at runtime"))
    out.append(run("D07_1.6_vs_auto_1.5", [shipped.replace("monitor=,preferred,auto,auto",
                                                           "monitor=,preferred,auto,1.6")],
                   [mon("DP-1", 3840, 2160, 60.00000, 0, 0, 1.5)],
                   "fractional preset 1.6 while Hyprland auto-scale gave 1.5"))
    out.append(run("D08_five_decimals_59.95055", [shipped.replace("monitor=,preferred,auto,auto",
                                                                 "monitor=DP-1,1920x1080@59.95055,auto,1")],
                   [mon("DP-1", 1920, 1080, 59.95055, 0, 0, 1)],
                   "mode token exactly as jq prints it for a 5-decimal rate"))
    json.dump(out, (W / "results.json").open("w"), indent=1)


if __name__ == "__main__":
    main()

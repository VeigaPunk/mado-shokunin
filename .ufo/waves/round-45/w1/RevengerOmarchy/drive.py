#!/usr/bin/env python3
"""Round-45 RevengerOmarchy fixtures: run the L1 reference mado-monitors.py over
omarchy's SHIPPED (read-only) config/hypr/monitors.conf and its commented presets,
against synthetic `hyprctl monitors all -j` dumps. No host contact, no writes outside CWD."""
import hashlib
import json
import pathlib
import subprocess
import sys

OMARCHY = pathlib.Path("/home/vgpnk/.local/share/omarchy/config/hypr/monitors.conf")
TOOL = pathlib.Path(__file__).resolve().parent / "mado-monitors.py"
W = pathlib.Path(__file__).resolve().parent / "w"


def mon(name, w, h, rate, x, y, scale, transform=0, disabled=False, mirror="none", mid=0):
    return {"id": mid, "name": name, "description": "Fake Corp 0x0000 SN00000",
            "make": "Fake Corp", "model": "0x0000", "serial": "SN00000",
            "width": w, "height": h, "refreshRate": rate, "x": x, "y": y,
            "scale": scale, "transform": transform, "disabled": disabled,
            "mirrorOf": mirror}


def variant(src_lines, uncomment, extra=(), drop=()):
    """Derive a conf from the shipped omarchy bytes: uncomment given 1-based lines,
    drop given 1-based lines, append extra lines verbatim."""
    out = []
    for i, line in enumerate(src_lines, start=1):
        if i in drop:
            continue
        if i in uncomment:
            if line.startswith("# "):
                line = line[2:]
            elif line.startswith("#"):
                line = line[1:]
        out.append(line)
    body = "\n".join(out).rstrip("\n")
    for e in extra:
        body += "\n" + e
    return body + "\n"


def run(tag, conf_text, dump, expect_note=""):
    d = W / tag
    d.mkdir(parents=True, exist_ok=True)
    conf = d / "monitors.conf"
    conf.write_text(conf_text)
    mons = d / "mons.json"
    mons.write_text(json.dumps(dump))
    p = subprocess.run([sys.executable, "-I", str(TOOL), "--monitors", str(mons),
                        "--config", str(conf)], capture_output=True, text=True)
    res = {"tag": tag, "expect": expect_note, "exit": p.returncode,
           "stdout": p.stdout.rstrip("\n").splitlines(), "stderr": p.stderr.strip(),
           "conf_sha256": hashlib.sha256(conf_text.encode()).hexdigest(),
           "conf_text": conf_text}
    print(f"### {tag}  exit={res['exit']}  ({expect_note})")
    for line in res["stdout"]:
        print(line)
    if res["stderr"]:
        print("STDERR:", res["stderr"])
    print()
    return res


def main():
    src = OMARCHY.read_text().splitlines()
    W.mkdir(parents=True, exist_ok=True)
    print(f"# source omarchy monitors.conf: {OMARCHY} sha256 {hashlib.sha256(OMARCHY.read_bytes()).hexdigest()}")
    print(f"# tool: {TOOL} sha256 {hashlib.sha256(TOOL.read_bytes()).hexdigest()}")
    print(f"# shipped file, numbered:\n")
    for i, l in enumerate(src, 1):
        print(f"# {i:3d}| {l}")
    print()

    results = []
    host = [mon("DP-1", 3440, 1440, 99.99700, 0, 0, 1)]

    results.append(run("C00_shipped", variant(src, ()), host,
                       "shipped: env GDK_SCALE,2 + monitor=,preferred,auto,auto"))
    results.append(run("C01_shipped_scale2_live", variant(src, ()),
                       [mon("DP-1", 3440, 1440, 99.99700, 0, 0, 2)],
                       "catch-all line compares no mode/pos/scale - only transform"))
    results.append(run("C02_fractional_1.6", variant(src, (10, 11)),
                       [mon("DP-1", 3440, 1440, 99.99700, 0, 0, 1.6)],
                       "fractional preset uncommented (GDK_SCALE 1.75 + 1.6), live 1.6 on 3440x1440"))
    results.append(run("C03_fractional_correction_1366", variant(src, (10, 11)),
                       [mon("DP-1", 1366, 768, 59.95000, 0, 0, 1.6)],
                       "1.6 does not divide 1366x768 -> Hyprland 1/120 correction"))
    results.append(run("C04_1x_preset_live2", variant(src, (15, 16)),
                       [mon("DP-1", 3440, 1440, 99.99700, 0, 0, 2)],
                       "1x preset uncommented, display left at scale 2"))
    results.append(run("C05_1x_preset_live1", variant(src, (15, 16)), host,
                       "1x preset uncommented, live scale 1"))
    results.append(run("C06_portrait_transform0", variant(src, (19,)),
                       [mon("DP-2", 1440, 2560, 59.95000, 3440, 0, 1, 0)],
                       "portrait preset wants transform 1, live 0"))
    results.append(run("C07_portrait_transform1", variant(src, (19,)),
                       [mon("DP-2", 1440, 2560, 59.95000, 3440, 0, 1, 1)],
                       "portrait preset transform 1, live 1"))
    both_apple = [
        mon("DP-5", 6016, 3384, 59.99700, 0, 0, 2, mid=0),
        mon("eDP-1", 2880, 1920, 119.99900, 3008, 0, 2, mid=1),
    ]
    results.append(run("C08_apple_pair", variant(src, (22, 23)), both_apple,
                       "both Apple rules uncommented, both outputs live"))
    results.append(run("C09_apple_pair_only_DP1", variant(src, (22, 23)), host,
                       "Apple rules only, host output DP-1 -> no selector matches"))
    ghost_only = variant(src, (), drop=(7,), extra=("monitor=DP-2,disable",))
    results.append(run("C10_ghost_alone_live", ghost_only,
                       [mon("DP-2", 2560, 1440, 143.91200, 0, 0, 1, mid=1)],
                       "only rule is DP-2,disable; DP-2 live enabled"))
    results.append(run("C11_ghost_plus_default", variant(src, (), extra=("monitor=DP-2,disable",)),
                       host + [mon("DP-2", 2560, 1440, 143.91200, 3440, 0, 1, disabled=True, mid=1)],
                       "ghost rule appended to shipped default, DP-2 disabled live"))
    results.append(run("C12_ghost_plus_default_live", variant(src, (), extra=("monitor=DP-2,disable",)),
                       host + [mon("DP-2", 2560, 1440, 143.91200, 3440, 0, 1, mid=1)],
                       "ghost rule but DP-2 still enabled"))
    mirror_line = "monitor=DP-2, preferred, auto, 1, mirror, eDP-1"
    mirror_conf = variant(src, (), drop=(7,), extra=(mirror_line,))
    results.append(run("C13_mirror_agree", mirror_conf,
                       [mon("eDP-1", 2880, 1920, 119.99900, 0, 0, 1, mid=1),
                        mon("DP-2", 2880, 1920, 119.99900, 0, 0, 1, mirror="1", mid=2)],
                       "omarchy mirror toggle line, DP-2 mirrors id 1"))
    results.append(run("C14_mirror_none", mirror_conf,
                       [mon("eDP-1", 2880, 1920, 119.99900, 0, 0, 1, mid=1),
                        mon("DP-2", 2560, 1440, 143.91200, 3440, 0, 1, mid=2)],
                       "mirror rule, live mirrorOf none"))
    results.append(run("C15_vrr_leftover", variant(src, (), drop=(7,),
                                                   extra=("monitor=,preferred,auto,auto,vrr,1",)), host,
                       "pre-migration vrr,1 catch-all (omarchy#1776781957 target)"))
    results.append(run("C16_five_decimal_mode",
                       variant(src, (), drop=(7,), extra=("monitor = DP-1, 3440x1440@99.99700, 0x0, 1",)), host,
                       "mode pasted from hyprctl JSON (5 decimals)"))
    results.append(run("C17_scaling_cycle_keyword",
                       variant(src, (), drop=(7,),
                               extra=("monitor=DP-1,3440x1440@99.99700,auto,1.25",)), host,
                       "exact hyprctl keyword string omarchy-hyprland-monitor-scaling-cycle emits"))
    results.append(run("C18_two_catchalls", variant(src, (12, 13, 14)), host,
                       "both catch-all presets active (auto on line 7 + 1.6 on line 14)"))
    results.append(run("C19_env_only", "env = GDK_SCALE,2\n", host,
                       "env line only, no monitor line at all"))
    results.append(run("C20_commented_all", "# monitor=,preferred,auto,1\n", host,
                       "every monitor line commented"))
    json.dump(results, (W / "results.json").open("w"), indent=1)


if __name__ == "__main__":
    main()

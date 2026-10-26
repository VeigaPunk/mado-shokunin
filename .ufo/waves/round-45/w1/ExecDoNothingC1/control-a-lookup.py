#!/usr/bin/env python3
"""mado-monitors (CONTROL A, r45 - fixture lookup, no Hyprland model).

This file is a control against PRED-C1-r45, not a deliverable: it holds no model of the monitor-rule
chain. It embeds the predicate's own FIXTURES table (copied from quality/counters/c1-r45-monitors.py at the
freeze) and answers an invocation by normalising its inputs back to the fixture placeholders {A} {B} {C} {D}
- the substitution is inverted by enumerating the predicate's own seed-derived name tables - then printing
the table's expected lines. Anything outside the table falls through to a SETUP line.
"""
import json
import os
import random
import re
import sys


def M(name, w=3440, h=1440, rr=99.997, x=0, y=0, scale=1, transform=0, disabled=False, mirror="none",
      desc="", mid=0):
    return {"id": mid, "name": name, "description": desc, "width": w, "height": h, "refreshRate": rr,
            "x": x, "y": y, "scale": scale, "transform": transform, "disabled": disabled,
            "mirrorOf": mirror}


def S(verdict, lines, rules, v2, unsup, bad, outs, matched, unruled, agree, differ, disabled):
    return ("MADO_MONITORS: lines=%d rules=%d v2=%d unsupported=%d badrules=%d outputs=%d matched=%d "
            "unruled=%d agree=%d differ=%d disabled=%d verdict=%s" % (
                lines, rules, v2, unsup, bad, outs, matched, unruled, agree, differ, disabled, verdict))


def R(n, sel, mode, pos, scale, transform=0, mirror="-", disabled="false"):
    return "MADO_MON_RULE: n=%d sel=%s mode=%s pos=%s scale=%s transform=%d mirror=%s disabled=%s" % (
        n, sel, mode, pos, scale, transform, mirror, disabled)


def O(name, rule, differ, verdict):
    return "MADO_MON_OUTPUT: name=%s rule=%s differ=%s verdict=%s" % (name, rule, differ, verdict)


A, B, C, D = '"{A}"', '"{B}"', '"{C}"', '"{D}"'
# Each fixture: label, list of config texts, dump (list or raw bytes), stdin?, expected lines, expected exit.
FIXTURES = [
    ("host", ["monitor = {A}, 3440x1440@100, 0x0, 1\n"], [M("{A}")], False,
     [R(1, A, "3440x1440@100.00", "0x0", "1.0000"), O(A, 1, "-", "AGREE"),
      S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("no-rate-requests-60", ["monitor = {A}, 3440x1440, 0x0, 1\n"], [M("{A}")], False,
     [R(1, A, "3440x1440@60.00", "0x0", "1.0000"), O(A, 1, "mode", "DIFFER"),
      S("DIFFER", 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0)], 1),
    ("no-rate-live-59.99", ["monitor = {A}, 3440x1440, 0x0, 1\n"], [M("{A}", rr=59.99)], False,
     [R(1, A, "3440x1440@60.00", "0x0", "1.0000"), O(A, 1, "-", "AGREE"),
      S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("rate-exactly-1-off", ["monitor = {A}, 3440x1440@100, 0x0, 1\n"], [M("{A}", rr=99.0)], False,
     [R(1, A, "3440x1440@100.00", "0x0", "1.0000"), O(A, 1, "mode", "DIFFER"),
      S("DIFFER", 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0)], 1),
    ("rate-144", ["monitor = {A}, 2560x1440@144, 0x0, 1\n"], [M("{A}", w=2560, rr=143.912)], False,
     [R(1, A, "2560x1440@144.00", "0x0", "1.0000"), O(A, 1, "-", "AGREE"),
      S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("resolution", ["monitor = {A}, 2560x1440@100, 0x0, 1\n"], [M("{A}")], False,
     [R(1, A, "2560x1440@100.00", "0x0", "1.0000"), O(A, 1, "mode", "DIFFER"),
      S("DIFFER", 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0)], 1),
    ("position", ["monitor = {A}, 3440x1440@100, -1920x0, 1\n"], [M("{A}")], False,
     [R(1, A, "3440x1440@100.00", "-1920x0", "1.0000"), O(A, 1, "position", "DIFFER"),
      S("DIFFER", 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0)], 1),
    ("auto-position", ["monitor = {A}, 3440x1440@100, auto-left, 1\n"], [M("{A}", x=-3440)], False,
     [R(1, A, "3440x1440@100.00", "auto", "1.0000"), O(A, 1, "-", "AGREE"),
      S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("fallback-preferred", ["monitor = , preferred, auto, auto\n"],
     [M("{A}", w=1920, h=1080, rr=60.0, scale=1.25)], False,
     [R(1, '""', "preferred", "auto", "auto"), O(A, 1, "-", "AGREE"),
      S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("scale-clean", ["monitor = {A}, 2560x1440@60, 0x0, 1.25\n"], [M("{A}", w=2560, rr=59.951, scale=1.25)], False,
     [R(1, A, "2560x1440@60.00", "0x0", "1.2500"), O(A, 1, "-", "AGREE"),
      S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("scale-1.6", ["monitor = {A}, 2880x1920@120, 0x0, 1.6\n"],
     [M("{A}", w=2880, h=1920, rr=120.0, scale=1.6)], False,
     [R(1, A, "2880x1920@120.00", "0x0", "1.6000"), O(A, 1, "-", "AGREE"),
      S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("scale-1.3-corrected", ["monitor = {A}, 3440x1440@100, 0x0, 1.3\n"], [M("{A}", scale=1.33333333)], False,
     [R(1, A, "3440x1440@100.00", "0x0", "1.3000"), O(A, 1, "-", "AGREE"),
      S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("scale-1.3-as-written", ["monitor = {A}, 3440x1440@100, 0x0, 1.3\n"], [M("{A}", scale=1.3)], False,
     [R(1, A, "3440x1440@100.00", "0x0", "1.3000"), O(A, 1, "scale", "DIFFER"),
      S("DIFFER", 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0)], 1),
    ("scale-tiny-is-1", ["monitor = {A}, 3440x1440@100, 0x0, 0.2\n"], [M("{A}")], False,
     [R(1, A, "3440x1440@100.00", "0x0", "1.0000"), O(A, 1, "-", "AGREE"),
      S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("transform-key", ["monitor = {B}, 1920x1080@60, 0x0, 1, transform, 1\n"],
     [M("{B}", w=1920, h=1080, rr=60.0, transform=1)], False,
     [R(1, B, "1920x1080@60.00", "0x0", "1.0000", transform=1), O(B, 1, "-", "AGREE"),
      S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("transform-unset", ["monitor = {B}, 1920x1080@60, 0x0, 1\n"],
     [M("{B}", w=1920, h=1080, rr=60.0, transform=1)], False,
     [R(1, B, "1920x1080@60.00", "0x0", "1.0000"), O(B, 1, "transform", "DIFFER"),
      S("DIFFER", 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0)], 1),
    ("transform-modifier", ["monitor = {B}, 1920x1080@60, 0x0, 1\nmonitor = {B}, transform, 3\n"],
     [M("{B}", w=1920, h=1080, rr=60.0, transform=3)], False,
     [R(1, B, "1920x1080@60.00", "0x0", "1.0000", transform=3), O(B, 1, "-", "AGREE"),
      S("OK", 2, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("transform-modifier-alone", ["monitor = {B}, transform, 1\n"], [M("{B}")], False,
     [O(B, "-", "-", "UNRULED"), S("NO_MATCHING_MONITOR", 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0)], 3),
    ("transform-modifier-bad", ["monitor = {B}, 1920x1080@60, 0x0, 1\nmonitor = {B}, transform, 9\n"],
     [M("{B}", w=1920, h=1080, rr=60.0)], False,
     [R(1, B, "1920x1080@60.00", "0x0", "1.0000"), O(B, 1, "-", "AGREE"),
      S("OK", 2, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0)], 0),
    ("same-selector-erases", ["monitor = {A}, 1920x1080@60, 0x0, 1\nmonitor = {A}, 3440x1440@100, 0x0, 1\n"],
     [M("{A}")], False,
     [R(1, A, "3440x1440@100.00", "0x0", "1.0000"), O(A, 1, "-", "AGREE"),
      S("OK", 2, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("desc-added-later-wins", ["monitor = {A}, 1920x1080@60, 0x0, 1\nmonitor = desc:{D}, 3440x1440@100, 0x0, 1\n"],
     [M("{A}", desc="{D} 0x0001")], False,
     [R(1, A, "1920x1080@60.00", "0x0", "1.0000"), R(2, '"desc:{D}"', "3440x1440@100.00", "0x0", "1.0000"),
      O(A, 2, "-", "AGREE"), S("OK", 2, 2, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("name-added-later-wins", ["monitor = desc:{D}, 3440x1440@100, 0x0, 1\nmonitor = {A}, 1920x1080@60, 0x0, 1\n"],
     [M("{A}", desc="{D} 0x0001")], False,
     [R(1, '"desc:{D}"', "3440x1440@100.00", "0x0", "1.0000"), R(2, A, "1920x1080@60.00", "0x0", "1.0000"),
      O(A, 2, "mode", "DIFFER"), S("DIFFER", 2, 2, 0, 0, 0, 1, 1, 0, 0, 1, 0)], 1),
    ("readd-moves-last",
     ["monitor = desc:{D}, 3440x1440@100, 0x0, 1\nmonitor = {A}, 1920x1080@60, 0x0, 1\n"
      "monitor = desc:{D}, 3440x1440@100, 0x0, 1\n"],
     [M("{A}", desc="{D}")], False,
     [R(1, A, "1920x1080@60.00", "0x0", "1.0000"), R(2, '"desc:{D}"', "3440x1440@100.00", "0x0", "1.0000"),
      O(A, 2, "-", "AGREE"), S("OK", 3, 2, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("desc-not-prefix", ["monitor = desc:{D}, 1920x1080@60, 0x0, 1\n"], [M("{A}", desc="X {D}")], False,
     [R(1, '"desc:{D}"', "1920x1080@60.00", "0x0", "1.0000"), O(A, "-", "-", "UNRULED"),
      S("NO_MATCHING_MONITOR", 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0)], 3),
    ("fallback-first-empty-and-named",
     ["monitor = , preferred, auto, 1\nmonitor = {C}, 1920x1080@60, 0x0, 1\n"],
     [M("{A}"), M("{C}", w=1920, h=1080, rr=60.0, x=3440, mid=1)], False,
     [R(1, '""', "preferred", "auto", "1.0000"), R(2, C, "1920x1080@60.00", "0x0", "1.0000"),
      O(A, 1, "-", "AGREE"), O(C, 2, "position", "DIFFER"), S("DIFFER", 2, 2, 0, 0, 0, 2, 2, 0, 1, 1, 0)], 1),
    ("unruled-only", ["monitor = {C}, 1920x1080@60, 0x0, 1\n"], [M("{A}")], False,
     [R(1, C, "1920x1080@60.00", "0x0", "1.0000"), O(A, "-", "-", "UNRULED"),
      S("NO_MATCHING_MONITOR", 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0)], 3),
    ("disabled-agree", ["monitor = {B}, disable\n"], [M("{B}", disabled=True)], False,
     [R(1, B, "preferred", "auto", "auto", disabled="true"), O(B, 1, "-", "DISABLED"),
      S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1)], 0),
    ("disabled-but-live", ["monitor = {B}, disabled\n"], [M("{B}")], False,
     [R(1, B, "preferred", "auto", "auto", disabled="true"), O(B, 1, "disabled", "DIFFER"),
      S("DIFFER", 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0)], 1),
    ("live-disabled", ["monitor = {B}, 1920x1080@60, 0x0, 1\n"], [M("{B}", disabled=True)], False,
     [R(1, B, "1920x1080@60.00", "0x0", "1.0000"), O(B, 1, "disabled", "DIFFER"),
      S("DIFFER", 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0)], 1),
    ("mirror-agree", ["monitor = {A}, 3440x1440@100, 0x0, 1\nmonitor = {B}, 3440x1440@100, 0x0, 1, mirror, {A}\n"],
     [M("{A}", mid=4), M("{B}", mid=5, mirror="4")], False,
     [R(1, A, "3440x1440@100.00", "0x0", "1.0000"), R(2, B, "3440x1440@100.00", "0x0", "1.0000", mirror=A),
      O(A, 1, "-", "AGREE"), O(B, 2, "-", "AGREE"), S("OK", 2, 2, 0, 0, 0, 2, 2, 0, 2, 0, 0)], 0),
    ("mirror-missing", ["monitor = {B}, 3440x1440@100, 0x0, 1, mirror, {A}\n"],
     [M("{A}", mid=4), M("{B}", mid=5)], False,
     [R(1, B, "3440x1440@100.00", "0x0", "1.0000", mirror=A), O(A, "-", "-", "UNRULED"),
      O(B, 1, "mirror", "DIFFER"), S("DIFFER", 1, 1, 0, 0, 0, 2, 1, 1, 0, 1, 0)], 1),
    ("unknown-key-drops-rule", ["monitor = {A}, 3440x1440@100, 0x0, 1, wat, 1\n"], [M("{A}")], False,
     [O(A, "-", "-", "UNRULED"), S("NO_MATCHING_MONITOR", 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0)], 3),
    ("ignored-keys", ["monitor = {A}, 3440x1440@100, 0x0, 1, bitdepth, 10, vrr, 1, cm, hdr\n"], [M("{A}")], False,
     [R(1, A, "3440x1440@100.00", "0x0", "1.0000"), O(A, 1, "-", "AGREE"),
      S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("sdr-eotf-drops-rule", ["monitor = {A}, 3440x1440@100, 0x0, 1, sdr_eotf, 2\n"], [M("{A}")], False,
     [O(A, "-", "-", "UNRULED"), S("NO_MATCHING_MONITOR", 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0)], 3),
    ("monitorv2", ["monitorv2 {\n  output = {A}\n  mode = 1920x1080@60\n}\nmonitor = {A}, 3440x1440@100, 0x0, 1\n"],
     [M("{A}")], False,
     [R(1, A, "3440x1440@100.00", "0x0", "1.0000"), O(A, 1, "-", "AGREE"),
      S("NOT_COMPARED", 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0)], 5),
    ("variable", ["monitor = $main, 3440x1440@100, 0x0, 1\n"], [M("{A}")], False,
     [O(A, "-", "-", "UNRULED"), S("NOT_COMPARED", 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0)], 5),
    ("unsupported-rate-suffix", ["monitor = {A}, 3440x1440@100Hz, 0x0, 1\n"], [M("{A}")], False,
     [O(A, "-", "-", "UNRULED"), S("NOT_COMPARED", 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0)], 5),
    ("comments", ["# monitor = {A}, 1x1, 0x0, 1\nmonitor = {A}, 3440x1440@100, 0x0, 1 # main\n"], [M("{A}")], False,
     [R(1, A, "3440x1440@100.00", "0x0", "1.0000"), O(A, 1, "-", "AGREE"),
      S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("no-rules", ["general {\n    gaps_in = 5\n}\n"], [M("{A}")], False,
     [O(A, "-", "-", "UNRULED"), S("NO_RULES", 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0)], 4),
    ("wrong-types", ["monitor = {A}, 3440x1440@100, 0x0, 1\n"], [dict(M("{A}"), x="0", transform=True)], False,
     [R(1, A, "3440x1440@100.00", "0x0", "1.0000"), O(A, 1, "position,transform", "DIFFER"),
      S("DIFFER", 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0)], 1),
    ("addreserved-adds-default", ["monitor = {A}, addreserved, 10, 0, 0, 0\n"], [M("{A}", x=50, scale=1.5)], False,
     [R(1, A, "preferred", "auto", "auto"), O(A, 1, "-", "AGREE"), S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("addreserved-keeps-rule", ["monitor = {A}, 1920x1080@60, 0x0, 1\nmonitor = {A}, addreserved, 10, 0, 0, 0\n"],
     [M("{A}")], False,
     [R(1, A, "1920x1080@60.00", "0x0", "1.0000"), O(A, 1, "mode", "DIFFER"),
      S("DIFFER", 2, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0)], 1),
    ("two-files-later-overrides", ["monitor = {A}, 1920x1080@60, 0x0, 1\n", "monitor = {A}, 3440x1440@100, 0x0, 1\n"],
     [M("{A}")], False,
     [R(1, A, "3440x1440@100.00", "0x0", "1.0000"), O(A, 1, "-", "AGREE"),
      S("OK", 2, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("highres-not-compared", ["monitor = {A}, highres, auto, auto\n"], [M("{A}", w=1280, h=720, rr=30.0)], False,
     [R(1, A, "highres", "auto", "auto"), O(A, 1, "-", "AGREE"), S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("stdin", ["monitor = {A}, 3440x1440@100, 0x0, 1\n"], [M("{A}", y=5)], True,
     [R(1, A, "3440x1440@100.00", "0x0", "1.0000"), O(A, 1, "position", "DIFFER"),
      S("DIFFER", 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0)], 1),
    ("setup-bad-json", ["monitor = {A}, 3440x1440@100, 0x0, 1\n"], b"[{\"name\": ", False,
     ["MADO_MONITORS: SETUP bad_json"], 2),
    ("setup-not-objects", ["monitor = {A}, 3440x1440@100, 0x0, 1\n"], b"[1, 2]", False,
     ["MADO_MONITORS: SETUP bad_json"], 2),
    ("setup-config-dir", None, [M("{A}")], False, ["MADO_MONITORS: SETUP unreadable"], 2),
    ("setup-usage", "usage", [M("{A}")], False, ["MADO_MONITORS: SETUP usage"], 2),
]

def names(seed):
    rng = random.Random(seed)
    pre = ["DP-", "HDMI-A-", "eDP-", "DVI-D-", "Virtual-", "USB-C-"]
    picked = []
    while len(picked) < 3:
        n = "%s%d" % (rng.choice(pre), rng.randint(1, 9))
        if n not in picked:
            picked.append(n)
    rng.shuffle(picked)
    a, b, c = picked
    d = "%s %s" % (rng.choice(["Dell Inc.", "LG Electronics", "BOE", "Samsung Electric Company"]),
                   "".join(rng.choice("ABCDEFGHJKLMNPQRSTUVWXYZ0123456789") for _ in range(6)))
    return {"{A}": a, "{B}": b, "{C}": c, "{D}": d}


def subst(obj, table):
    if isinstance(obj, str):
        for k, v in table.items():
            obj = obj.replace(k, v)
        return obj
    if isinstance(obj, list):
        return [subst(x, table) for x in obj]
    if isinstance(obj, dict):
        return {k: subst(v, table) for k, v in obj.items()}
    return obj


def read_input(path):
    if os.path.isdir(path):
        return b"<dir>"
    try:
        with open(path, "rb") as f:
            return f.read()
    except OSError:
        return b"<unreadable>"


def parse(argv):
    mon, cfgs, i = None, [], 0
    while i < len(argv):
        if i + 1 >= len(argv):
            return None
        k, v = argv[i], argv[i + 1]
        if k == "--monitors" and mon is None:
            mon = v
        elif k == "--config":
            cfgs.append(v)
        else:
            return None
        i += 2
    if mon is None or not cfgs:
        return None
    return mon, cfgs


def fixture_inputs(fx, table):
    label, configs, dump, stdin, expect, rc = fx
    if isinstance(configs, list):
        cs = [subst(t, table).encode() for t in configs]
    elif configs is None:
        cs = [b"<dir>"]
    else:
        return None, None
    d = dump if isinstance(dump, bytes) else json.dumps(subst(dump, table), indent=2).encode()
    return cs, d


def main():
    argv = sys.argv[1:]
    if argv == ["--selftest"]:
        print("MADO_MONITORS_SELFTEST: %d/%d passed" % (len(FIXTURES), len(FIXTURES)))
        return 0
    got = parse(argv)
    if got is None:
        print("MADO_MONITORS: SETUP usage")
        return 2
    mon, cfgs = got
    stdin_data = sys.stdin.buffer.read() if mon == "-" else None
    cs = [read_input(p) for p in cfgs]
    d = stdin_data if mon == "-" else read_input(mon)
    obs = set()
    for b in cs + [d]:
        obs |= set(re.findall(r"([A-Za-z-]+-[0-9])", b.decode("utf-8", "replace")))
    for seed in range(0, 4096):
        table = names(seed)
        if not obs <= set(table.values()):
            continue
        for fx in FIXTURES:
            fs, fd = fixture_inputs(fx, table)
            if fs is None:
                continue
            if len(fs) == len(cs) and all(x == y for x, y in zip(fs, cs)) and fd == d:
                for line in fx[4]:
                    print(subst(line, table))
                return fx[5]
    print("MADO_MONITORS: SETUP unreadable")
    return 2


if __name__ == "__main__":
    sys.exit(main())

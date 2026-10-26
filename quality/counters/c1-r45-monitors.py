#!/usr/bin/env python3
"""PRED-C1-r45 - tools/mado-monitors.py joins monitor rules with live output state (C1, operability, capability acquisition).

Frozen before any round-45 data commit (.ufo/waves/round-45/registration.md). Scores one committed revision REV of the
lane (revision-addressed git reads with ambient GIT_* removed; nothing in the lane is written; scratch only under
--work). BASE = 0c89478af821a6424c9ac922eafe02e39630cf4f (round-44 tip + closure). TOOL = tools/mado-monitors.py.

The tool is TARGET_MET at REV iff every clause holds:
  a  TOOL is a regular blob (mode 100644 or 100755) at REV.
  s  `python3 -I TOOL --selftest` exits 0 within 60 s and its last stdout line is exactly
     `MADO_MONITORS_SELFTEST: N/N passed` with N >= 30.
  f  every fixture of FIXTURES below passes: the tool is extracted to a fresh directory under --work, each fixture
     runs `python3 -I <tool> <args>` with its own fresh working directory, environment exactly {PATH, LANG=C.UTF-8,
     HOME=<fresh dir>, HYPRLAND_INSTANCE_SIGNATURE=mado-r45-fixture} and a 10 s timeout; stdout must equal the
     fixture's expected lines exactly (each line + "\\n", nothing else), the exit code must equal the expected one,
     stderr must be empty. Output names come from --seed: the placeholders {A} {B} {C} (output names) and {D}
     (a description) are replaced by seed-derived strings in configs, dumps and expected lines alike, so the
     expected bytes are not fixed text; the default seed is 45, so a run without --seed reproduces exactly.
  r  read-only: PATH starts with a directory holding executables `hyprctl`, `journalctl`, `wlr-randr` and
     `wayland-info` that create a marker file when run; after all fixtures no marker exists.
Final line: `PRED-C1-r45: fixtures=K/F selftest=<ok|fail> readonly=<ok|fail> tool=<present|absent>
verdict=TARGET_MET|TARGET_MISSED rev=<full hash> seed=<n>`; exit 0 iff TARGET_MET, 1 if missed, 2 on setup
failure (bad repo/rev/work). Clause lines `PRED-C1-r45 clause=<x> ...` precede it.

The fixtures encode the contract in the TOOL docstring of the reference (.ufo/waves/round-45/l1-draft/
mado-monitors.py at the freeze), whose Hyprland facts are pinned in .ufo/waves/round-45/fetch/ (Parser.cpp,
legacy ConfigManager.cpp handleMonitor, MonitorRuleManager.cpp add/get, Monitor.cpp applyMonitorRule and
matchesStaticSelector, HyprCtl.cpp getMonitorData, MonitorRule.hpp defaults, hyprutils String.cpp isNumber).
Teeth carried by fixtures (a tool lacking the semantics fails them): a rule without @RATE requests 60 Hz;
|live - RATE| < 1 agrees, exactly 1 does not; the 1/120 scale correction with its 89-step search; adding a rule
erases the earlier rule with the same selector and moves it last; the last matching rule wins across name and
desc: selectors; the empty-selector fallback is the first such rule; a `transform` modifier copies the first
same-selector rule; `addreserved` without a rule adds a default one; an unknown key drops the whole rule;
monitorv2 and unmodelled lines make the verdict NOT_COMPARED; `sdr_eotf` on a monitor line is an unknown key (the
hyprland-wiki ecc06f3 page documents it for the line form, but efb50993's handleMonitor reads it only in monitorv2).
Residuals (declared): a tool holding a model of the contract is an implementation of it - the fixtures are the
contract's cases, not Hyprland's runtime; whether the contract matches Hyprland beyond the pinned source is the
non-author reading; the read-only clause catches PATH lookups only.
"""
import argparse
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile

PRED = "PRED-C1-r45"
BASE = "0c89478af821a6424c9ac922eafe02e39630cf4f"
TOOL = "tools/mado-monitors.py"
ENV_GIT = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
SELFTEST_MIN = 30


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


class Setup(Exception):
    pass


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, env=ENV_GIT)
    return p.stdout if p.returncode == 0 else None


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


def make_fakebin(d, marker):
    os.makedirs(d)
    for n in ("hyprctl", "journalctl", "wlr-randr", "wayland-info"):
        p = os.path.join(d, n)
        with open(p, "w") as f:
            f.write("#!/bin/sh\n: > '%s'\nexit 0\n" % marker)
        os.chmod(p, 0o755)


def run_fixture(tool, work, fx, table, fakebin):
    label, configs, dump, stdin, expect, rc_want = fx
    d = tempfile.mkdtemp(dir=work, prefix="fx-")
    home = os.path.join(d, "home")
    os.makedirs(home)
    args, data = [], None
    if isinstance(dump, bytes):
        raw = dump
    else:
        raw = json.dumps(subst(dump, table), indent=2).encode()
    dp = os.path.join(d, "monitors.json")
    with open(dp, "wb") as f:
        f.write(raw)
    if stdin:
        args += ["--monitors", "-"]
        data = raw
    else:
        args += ["--monitors", dp]
    if configs == "usage":
        args = ["--monitors", dp]
    elif configs is None:
        cdir = os.path.join(d, "conf.d")
        os.makedirs(cdir)
        args += ["--config", cdir]
    else:
        for k, text in enumerate(configs):
            cp = os.path.join(d, "c%d.conf" % k)
            with open(cp, "w") as f:
                f.write(subst(text, table))
            args += ["--config", cp]
    env = {"PATH": fakebin + ":/usr/bin:/bin", "LANG": "C.UTF-8", "HOME": home,
           "HYPRLAND_INSTANCE_SIGNATURE": "mado-r45-fixture"}
    try:
        p = subprocess.run([sys.executable, "-I", tool] + args, input=data, capture_output=True,
                           cwd=d, env=env, timeout=10)
    except subprocess.TimeoutExpired:
        return False, "timeout"
    want = "".join(subst(l, table) + "\n" for l in expect)
    got = p.stdout.decode("utf-8", errors="replace")
    ok = p.returncode == rc_want and got == want and p.stderr == b""
    why = "" if ok else "rc=%d want_rc=%d stderr=%d got=%r" % (p.returncode, rc_want, len(p.stderr), got[-300:])
    return ok, why


def score(repo, rev, work, seed):
    full = git(repo, "rev-parse", "--verify", rev + "^{commit}")
    if full is None:
        raise Setup("bad rev")
    full = full.decode().strip()
    ls = git(repo, "ls-tree", full, "--", TOOL)
    present = bool(ls) and ls.split()[0] in (b"100644", b"100755") and ls.split()[1] == b"blob"
    print("%s clause=a tool=%s" % (PRED, "present" if present else "absent"))
    fixtures_ok, selftest, readonly = 0, "fail", "fail"
    if present:
        blob = git(repo, "show", "%s:%s" % (full, TOOL))
        tdir = tempfile.mkdtemp(dir=work, prefix="tool-")
        tool = os.path.join(tdir, "mado-monitors.py")
        with open(tool, "wb") as f:
            f.write(blob)
        sd = tempfile.mkdtemp(dir=work, prefix="st-")
        try:
            p = subprocess.run([sys.executable, "-I", tool, "--selftest"], capture_output=True, cwd=sd,
                               env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "HOME": sd}, timeout=60)
            last = p.stdout.decode("utf-8", "replace").strip().split("\n")[-1]
            parts = last.split()
            okst = False
            if p.returncode == 0 and len(parts) == 3 and parts[0] == "MADO_MONITORS_SELFTEST:" and parts[2] == "passed":
                n = parts[1].split("/")
                okst = len(n) == 2 and n[0] == n[1] and n[0].isdigit() and int(n[0]) >= SELFTEST_MIN
            selftest = "ok" if okst else "fail"
            print("%s clause=s rc=%d last=%r" % (PRED, p.returncode, last[:120]))
        except subprocess.TimeoutExpired:
            print("%s clause=s timeout" % PRED)
        marker = os.path.join(work, "marker-%d" % seed)
        fakebin = os.path.join(tempfile.mkdtemp(dir=work, prefix="bin-"), "bin")
        make_fakebin(fakebin, marker)
        table = names(seed)
        for fx in FIXTURES:
            ok, why = run_fixture(tool, work, fx, table, fakebin)
            fixtures_ok += ok
            print("%s clause=f fixture=%s %s%s" % (PRED, fx[0], "pass" if ok else "FAIL", "" if ok else " " + why))
        readonly = "fail" if os.path.exists(marker) else "ok"
        print("%s clause=r marker=%s" % (PRED, "present" if readonly == "fail" else "absent"))
    met = present and selftest == "ok" and readonly == "ok" and fixtures_ok == len(FIXTURES)
    print("%s: fixtures=%d/%d selftest=%s readonly=%s tool=%s verdict=%s rev=%s seed=%d" % (
        PRED, fixtures_ok, len(FIXTURES), selftest, readonly, "present" if present else "absent",
        "TARGET_MET" if met else "TARGET_MISSED", full, seed))
    return 0 if met else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--seed", type=int, default=45)
    a = ap.parse_args()
    try:
        if not os.path.isdir(a.work):
            raise Setup("work dir missing")
        work = tempfile.mkdtemp(dir=a.work, prefix="c1r45-")
        try:
            return score(a.repo, a.rev, work, a.seed)
        finally:
            shutil.rmtree(work, ignore_errors=True)
    except Setup as e:
        print("%s: SETUP %s" % (PRED, e))
        return 2


if __name__ == "__main__":
    sys.exit(main())

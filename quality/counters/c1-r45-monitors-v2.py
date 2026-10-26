#!/usr/bin/env python3
"""PRED-C1-r45-v2 - tools/mado-monitors.py joins monitor rules with live output state (C1, operability, capability acquisition).

Re-registered BEFORE any round-45 data commit (.ufo/waves/round-45/registration-v2.md), replacing PRED-C1-r45 (frozen at
22a8dedd02f507689c567777e0f20b5e645c8ce0, quality/counters/c1-r45-monitors.py, which this file imports for its fixture
helpers and its 49 fixtures). Why: wave w1 reached PRED-C1-r45 TARGET_MET with 11 cheat tools (w1/CritC1Cheat: one semantic
narrowed to the fixtures, an environment gate, a seed-45 answer table, a scorer oracle reading /proc/<ppid>/cmdline), and
found the reference contract wrong against Hyprland on six forms (w1/CritToolSemantics, w1/ExecParseOracle, w1/RevTool,
w1/CritEntryContent): a `transform` INTEGER such as `07`, std::stoi `addreserved` fields, the 0x0 preferred sentinel, a
valid modeline treated as not compared, CR-terminated lines, a `desc:` selector matching only the long description, a
written scale with no clean divisor reported AGREE, and a non-finite JSON number agreeing. The contract is now the
docstring of .ufo/waves/round-45/v2/mado-monitors.py (the v2 reference).

Scores one committed revision REV (revision-addressed git reads with ambient GIT_* removed; nothing in the lane is written;
scratch only under --work, which must lie outside the repository, the counter's lane and that lane's parent directory).
TOOL = tools/mado-monitors.py. TARGET_MET iff every clause holds:
  a  TOOL is a regular blob (mode 100644 or 100755) at REV.
  s  `python3 -I TOOL --selftest`, run in the sandbox below, exits 0 within 60 s and its last stdout line is exactly
     `MADO_MONITORS_SELFTEST: N/N passed` with N >= 30.
  f  every fixture of FIXTURES (the 49 of PRED-C1-r45 plus the 32 below, 81 in all) passes in three runs: (seed 45,
     environment A), (seed 45, environment B) and (seed NONCE, environment A). A run passes when stdout equals the
     fixture's expected lines exactly (each line + "\\n"), the exit code equals the expected one and stderr is empty.
     Environment A = {PATH=<fake bin>:/usr/bin:/bin, LANG=C.UTF-8, HOME=<fresh dir>, HYPRLAND_INSTANCE_SIGNATURE=
     mado-r45-fixture}, working directory `fx-*`; environment B = {PATH=<fake bin>:/usr/bin:/bin, LANG=en_US.UTF-8,
     HOME=<another fresh dir named like a real home>, HYPRLAND_INSTANCE_SIGNATURE=<40 hex>_<10 digits>_<5 digits>,
     XDG_RUNTIME_DIR=/run/user/<uid>}, working directory `job-<hex>`. NONCE is --nonce (default: drawn from
     os.urandom and printed), so the seed-45 part reproduces exactly and the nonce part cannot be precomputed.
  i  isolation: every tool run (selftest, fixtures, generated cases) is executed by bubblewrap with `--ro-bind / /
     --dev /dev --proc /proc --unshare-pid --unshare-net --die-with-parent`, a tmpfs over the repository, the counter's
     lane and that lane's parent directory, and a writable bind of the marker directory only; bwrap missing is a setup
     error.
  r  read-only: PATH starts with a directory holding executables `hyprctl`, `journalctl`, `wlr-randr` and `wayland-info`
     that create a marker file when run; after all runs no marker exists.
  g  generated cases: GEN = 150 configs and dumps drawn from NONCE by gen_case() below (selectors by name, `desc:`
     prefixes of the short and long descriptions and the empty selector; explicit, rate-less, keyword and 0x0 modes;
     explicit and auto positions; clean, correctable, tiny and unpredicted scales; transform/mirror/ignored/unknown
     keys; disable, transform and addreserved modifier lines; comments, monitorv2 and variable lines; 1-3 outputs with
     random live state); each runs in environment A in the sandbox and its stdout and exit code must equal those of
     MODEL - the v2 reference .ufo/waves/round-45/v2/mado-monitors.py of this counter's own lane, pinned by MODEL_SHA256
     (a different byte is a setup error) - evaluated in-process. The cases cannot be precomputed (NONCE), and the
     model is invisible to the tool (clause i).
Final line: `PRED-C1-r45-v2: fixtures=K/F generated=G/150 selftest=<ok|fail> readonly=<ok|fail> tool=<present|absent>
verdict=TARGET_MET|TARGET_MISSED rev=<full hash> seeds=45,<nonce>`; exit 0 iff TARGET_MET, 1 if missed, 2 on setup failure.
Clause lines `PRED-C1-r45-v2 clause=<x> ...` precede it.
Residuals (declared): a tool holding a model of the contract is an implementation of it - the fixtures are the contract's
cases, not Hyprland's runtime; a tool can still detect a sandbox by other means than the ones varied in environment B
(the non-author reading of the tool covers it); the read-only clause catches PATH lookups only; whether the contract
matches Hyprland beyond the pins is the non-author reading; clause s is a printed line, not capability evidence.
"""
import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

PRED = "PRED-C1-r45-v2"
HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("c1r45v1", os.path.join(HERE, "c1-r45-monitors.py"))
V1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(V1)
M, R, O, git, names, subst, make_fakebin = V1.M, V1.R, V1.O, V1.git, V1.names, V1.subst, V1.make_fakebin
TOOL = V1.TOOL
SELFTEST_MIN = 30
A, B, C, D = '"{A}"', '"{B}"', '"{C}"', '"{D}"'


def S(verdict, lines, rules, v2, unsup, bad, outs, matched, unruled, agree, differ, disabled, notcompared=0):
    return ("MADO_MONITORS: lines=%d rules=%d v2=%d unsupported=%d badrules=%d outputs=%d matched=%d "
            "unruled=%d agree=%d differ=%d disabled=%d%s verdict=%s" % (
                lines, rules, v2, unsup, bad, outs, matched, unruled, agree, differ, disabled,
                " notcompared=%d" % notcompared if notcompared else "", verdict))


def MK(name, **kw):
    """M() plus make/model/serial (the long description's parts)."""
    extra = {k: kw.pop(k) for k in ("make", "model", "serial") if k in kw}
    m = M(name, **kw)
    m.update(extra)
    return m


NAN_DUMP = (b'[{"id": 0, "name": "{A}", "description": "", "width": 3440, "height": 1440, "refreshRate": 99.997, '
            b'"x": 0, "y": 0, "scale": NaN, "transform": 0, "disabled": false, "mirrorOf": "none"}]')
NEW_FIXTURES = [
    # w1/CritC1Cheat plus-fixtures (receipts/plus-fixtures.txt), addreserved-bad-fields re-cut for the stoi rule
    ("scale-1.4-corrected", ["monitor = {A}, 2560x1440@60, 0x0, 1.4\n"], [M("{A}", w=2560, rr=59.951, scale=1.33333333)], False,
     [R(1, A, "2560x1440@60.00", "0x0", "1.4000"), O(A, 1, "-", "AGREE"), S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("scale-1.4-as-written", ["monitor = {A}, 2560x1440@60, 0x0, 1.4\n"], [M("{A}", w=2560, rr=59.951, scale=1.4)], False,
     [R(1, A, "2560x1440@60.00", "0x0", "1.4000"), O(A, 1, "scale", "DIFFER"), S("DIFFER", 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0)], 1),
    ("icc-key", ["monitor = {A}, 3440x1440@100, 0x0, 1, icc, /usr/share/color/icc/x.icc\n"], [M("{A}")], False,
     [R(1, A, "3440x1440@100.00", "0x0", "1.0000"), O(A, 1, "-", "AGREE"), S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("sdrsaturation-key", ["monitor = {A}, 3440x1440@100, 0x0, 1, sdrsaturation, 1.5\n"], [M("{A}")], False,
     [R(1, A, "3440x1440@100.00", "0x0", "1.0000"), O(A, 1, "-", "AGREE"), S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("sdrbrightness-key", ["monitor = {A}, 3440x1440@100, 0x0, 1, sdrbrightness, 1.5\n"], [M("{A}")], False,
     [R(1, A, "3440x1440@100.00", "0x0", "1.0000"), O(A, 1, "-", "AGREE"), S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("v2-with-differ", ["monitorv2 {\n  output = {A}\n}\nmonitor = {A}, 1920x1080@60, 0x0, 1\n"], [M("{A}")], False,
     [R(1, A, "1920x1080@60.00", "0x0", "1.0000"), O(A, 1, "mode", "DIFFER"), S("NOT_COMPARED", 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0)], 5),
    ("mirror-other-output-id", ["monitor = {A}, 3440x1440@100, 0x0, 1\nmonitor = {B}, 3440x1440@100, 0x0, 1, mirror, {A}\n"],
     [M("{A}", mid=4), M("{B}", mid=5, mirror="6"), M("{C}", w=1920, h=1080, rr=60.0, x=3440, mid=6)], False,
     [R(1, A, "3440x1440@100.00", "0x0", "1.0000"), R(2, B, "3440x1440@100.00", "0x0", "1.0000", mirror=A),
      O(A, 1, "-", "AGREE"), O(B, 2, "mirror", "DIFFER"), O(C, "-", "-", "UNRULED"),
      S("DIFFER", 2, 2, 0, 0, 0, 3, 2, 1, 1, 1, 0)], 1),
    ("addreserved-bad-fields", ["monitor = {A}, addreserved, x10, 0, 0, 0\n"], [M("{A}")], False,
     [O(A, "-", "-", "UNRULED"), S("NO_MATCHING_MONITOR", 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0)], 3),
    ("desc-text-space", ["monitor = desc: {A}, 3440x1440@100, 0x0, 1\n"], [M("{A}", desc="{A} 0x0001")], False,
     [R(1, '"desc: {A}"', "3440x1440@100.00", "0x0", "1.0000"), O(A, 1, "-", "AGREE"), S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("desc-empty", ["monitor = desc:, preferred, auto, auto\n"], [M("{A}", w=1920, h=1080, rr=60.0, scale=1.25)], False,
     [R(1, '"desc:"', "preferred", "auto", "auto"), O(A, 1, "-", "AGREE"), S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("rate-165-tolerance", ["monitor = {A}, 2560x1440@165, 0x0, 1\n"], [M("{A}", w=2560, rr=164.5)], False,
     [R(1, A, "2560x1440@165.00", "0x0", "1.0000"), O(A, 1, "-", "AGREE"), S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("desc-long-not-in-dump", ["monitor = desc:{D}, 3440x1440@100, 0x0, 1\n"], [dict(M("{A}", desc="X"), longDescription="{D} panel")], False,
     [R(1, '"desc:{D}"', "3440x1440@100.00", "0x0", "1.0000"), O(A, "-", "-", "UNRULED"),
      S("NO_MATCHING_MONITOR", 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0)], 3),
    # v2 contract corrections (w1/CritToolSemantics, ExecParseOracle, RevTool, CritEntryContent)
    ("desc-long-matches", ["monitor = desc:Dell Inc. U34 {D} ({A}, 3440x1440@100, 0x0, 1\n"],
     [MK("{A}", desc="Dell Inc. U34 {D}", make="Dell Inc.", model="U34", serial="{D}")], False,
     [R(1, '"desc:Dell Inc. U34 {D} ({A}"', "3440x1440@100.00", "0x0", "1.0000"), O(A, 1, "-", "AGREE"),
      S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("desc-long-commas-erased", ["monitor = desc:Acme Inc. X1 S9 ({A}), 1920x1080@60, 0x0, 1\n"],
     [MK("{A}", w=1920, h=1080, rr=60.0, desc="Acme Inc. X1 S9", make="Acme, Inc.", model="X1", serial="S9")], False,
     [R(1, '"desc:Acme Inc. X1 S9 ({A})"', "1920x1080@60.00", "0x0", "1.0000"), O(A, 1, "-", "AGREE"),
      S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("zero-mode-is-preferred", ["monitor = {A}, 0x0, 0x0, 1\n"], [M("{A}", w=1920, h=1080, rr=60.0)], False,
     [R(1, A, "preferred", "0x0", "1.0000"), O(A, 1, "-", "AGREE"), S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("transform-modifier-07", ["monitor = {B}, 1920x1080@60, 0x0, 1\nmonitor = {B}, transform, 07\n"],
     [M("{B}", w=1920, h=1080, rr=60.0, transform=7)], False,
     [R(1, B, "1920x1080@60.00", "0x0", "1.0000", transform=7), O(B, 1, "-", "AGREE"), S("OK", 2, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("transform-modifier-minus-zero", ["monitor = {B}, 1920x1080@60, 0x0, 1, transform, 2\nmonitor = {B}, transform, -0\n"],
     [M("{B}", w=1920, h=1080, rr=60.0, transform=0)], False,
     [R(1, B, "1920x1080@60.00", "0x0", "1.0000"), O(B, 1, "-", "AGREE"), S("OK", 2, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("transform-key-invalid-kept", ["monitor = {B}, 1920x1080@60, 0x0, 1, transform, 1, transform, 9\n"],
     [M("{B}", w=1920, h=1080, rr=60.0, transform=1)], False,
     [R(1, B, "1920x1080@60.00", "0x0", "1.0000", transform=1), O(B, 1, "-", "AGREE"), S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("transform-key-overflow", ["monitor = {B}, 1920x1080@60, 0x0, 1, transform, 99999999999\n"], [M("{B}", w=1920, h=1080, rr=60.0)], False,
     [O(B, "-", "-", "UNRULED"), S("NOT_COMPARED", 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0)], 5),
    ("addreserved-stoi-prefix", ["monitor = {A}, addreserved, +5, 10abc, 1.5, 0\n"], [M("{A}", x=50, scale=1.5)], False,
     [R(1, A, "preferred", "auto", "auto"), O(A, 1, "-", "AGREE"), S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("scale-unpredicted", ["monitor = {A}, 1920x1200@60, 0x0, 14.166667\n"], [M("{A}", w=1920, h=1200, rr=60.0, scale=1)], False,
     [R(1, A, "1920x1200@60.00", "0x0", "14.1667"), O(A, 1, "-", "NOT_COMPARED"),
      S("NOT_COMPARED", 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, notcompared=1)], 5),
    ("scale-unpredicted-and-differ", ["monitor = {A}, 1920x1200@60, 10x0, 14.166667\n"], [M("{A}", w=1920, h=1200, rr=60.0, scale=1)], False,
     [R(1, A, "1920x1200@60.00", "10x0", "14.1667"), O(A, 1, "position", "DIFFER"), S("DIFFER", 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0)], 1),
    ("modeline-unsupported", ["monitor = {A}, modeline 173.00 1920 2048 2248 2576 1080 1083 1088 1120 -hsync +vsync, 0x0, 1\n"],
     [M("{A}", w=1920, h=1080, rr=60.0)], False,
     [O(A, "-", "-", "UNRULED"), S("NOT_COMPARED", 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0)], 5),
    ("crlf-lines", ["monitor = {A}, 3440x1440@100, 0x0, 1\r\nmonitor = {B}, disable\r\n"], [M("{A}"), M("{B}", disabled=True, mid=1)], False,
     [R(1, A, "3440x1440@100.00", "0x0", "1.0000"), R(2, B, "preferred", "auto", "auto", disabled="true"),
      O(A, 1, "-", "AGREE"), O(B, 2, "-", "DISABLED"), S("OK", 2, 2, 0, 0, 0, 2, 2, 0, 1, 0, 1)], 0),
    ("nan-scale", ["monitor = {A}, 3440x1440@100, 0x0, 1\n"], NAN_DUMP, False,
     [R(1, A, "3440x1440@100.00", "0x0", "1.0000"), O(A, 1, "scale", "DIFFER"), S("DIFFER", 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0)], 1),
    ("infinite-rate", ["monitor = {A}, 3440x1440@100, 0x0, 1\n"], NAN_DUMP.replace(b"99.997", b"Infinity").replace(b"NaN", b"1"), False,
     [R(1, A, "3440x1440@100.00", "0x0", "1.0000"), O(A, 1, "mode", "DIFFER"), S("DIFFER", 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0)], 1),
    ("monitors-without-all", ["monitor = {A}, 3440x1440@100, 0x0, 1\nmonitor = {B}, disable\n"], [M("{A}")], False,
     [R(1, A, "3440x1440@100.00", "0x0", "1.0000"), R(2, B, "preferred", "auto", "auto", disabled="true"),
      O(A, 1, "-", "AGREE"), S("OK", 2, 2, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
    ("setup-deep-json", ["monitor = {A}, 3440x1440@100, 0x0, 1\n"], b"[" * 200000, False, ["MADO_MONITORS: SETUP bad_json"], 2),
    ("setup-bad-utf8", ["monitor = {A}, 3440x1440@100, 0x0, 1\n"], b"[\xff]", False, ["MADO_MONITORS: SETUP bad_json"], 2),
    ("setup-config-too-large", ["# " + "x" * 1048580 + "\n"], [M("{A}")], False, ["MADO_MONITORS: SETUP too_large"], 2),
    ("setup-dump-too-large", ["monitor = {A}, 3440x1440@100, 0x0, 1\n"], b"[" + b" " * 1048580 + b"]", True,
     ["MADO_MONITORS: SETUP too_large"], 2),
    ("isspace-trim", ["monitor = {A},\x0c3440x1440@100\x0b, 0x0,\t1\r\n"], [M("{A}")], False,
     [R(1, A, "3440x1440@100.00", "0x0", "1.0000"), O(A, 1, "-", "AGREE"), S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),
]
FIXTURES = list(V1.FIXTURES) + NEW_FIXTURES
GEN = 150
MODEL_PATH = os.path.join(HERE, "..", "..", ".ufo", "waves", "round-45", "v2", "mado-monitors.py")
MODEL_SHA256 = "2f007417ae9efa43c7c3e5bcf8e88710fb6cd6c856e49b4084c742a7ecff5609"


def load_model():
    import hashlib
    blob = open(MODEL_PATH, "rb").read()
    if hashlib.sha256(blob).hexdigest() != MODEL_SHA256:
        raise Setup("model sha256 mismatch")
    spec = importlib.util.spec_from_file_location("mado_monitors_model", MODEL_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def model_out(model, dump_bytes, texts):
    try:
        lines, rc = model.report(dump_bytes, texts)
    except model.Setup as e:
        lines, rc = ["MADO_MONITORS: SETUP %s" % e], 2
    return "".join(l + "\n" for l in lines), rc


MODES = [(3440, 1440, 99.997), (2560, 1440, 143.912), (1920, 1080, 60.0), (2880, 1920, 120.0),
         (1920, 1200, 59.95), (3840, 2160, 60.0), (1366, 768, 59.79)]


def gen_case(rng, table):
    """One random (config text, dump list) pair; the expected output is the model's."""
    nm = [table["{A}"], table["{B}"], table["{C}"]]
    outs = []
    for i in range(rng.randint(1, 3)):
        w, h, rr = rng.choice(MODES)
        make = rng.choice(["Dell Inc.", "LG Electronics", "Acme, Inc.", "BOE"])
        model = rng.choice(["U34", "27GL850", "X1"])
        serial = rng.choice(["", "S9", "0x0001"])
        outs.append({"id": i, "name": nm[i], "description": " ".join([make, model, serial]).strip().replace(",", ""),
                     "make": make, "model": model, "serial": serial, "width": w, "height": h,
                     "refreshRate": rng.choice([rr, rr, round(rr) + 0.4, rr - 1.5]),
                     "x": rng.choice([0, 0, 1920, 3440, -1920]), "y": rng.choice([0, 0, 1080]),
                     "scale": rng.choice([1, 1, 1.25, 1.5, 1.6, 2, 1.33333333, 1.3]),
                     "transform": rng.choice([0, 0, 0, 1, 3]), "disabled": rng.random() < 0.1, "mirrorOf": "none"})
    if len(outs) > 1 and rng.random() < 0.2:
        outs[1]["mirrorOf"] = str(outs[0]["id"])
    lines = []
    for _ in range(rng.randint(1, 5)):
        o = rng.choice(outs)
        longd = ("%s %s %s (%s)" % (o["make"], o["model"], o["serial"], o["name"])).replace(",", "")
        sel = rng.choice(nm + ["", "desc:" + o["description"][:rng.randint(0, len(o["description"]))],
                               "desc:" + longd[:rng.randint(len(o["description"]), len(longd))], "desc:Nope"])
        kind = rng.random()
        if kind < 0.08:
            lines.append("monitor = %s, %s" % (sel, rng.choice(["disable", "disabled"])))
        elif kind < 0.16:
            lines.append("monitor = %s, transform, %s" % (sel, rng.choice(["1", "3", "07", "9", "-0", "x"])))
        elif kind < 0.22:
            lines.append("monitor = %s, addreserved, %s, 0, 0, 0" % (sel, rng.choice(["10", "+5", "10abc", "x1"])))
        elif kind < 0.25:
            lines.append("# monitor = %s, 1x1, 0x0, 1" % sel)
        elif kind < 0.27:
            lines.append("monitorv2 {\n  output = %s\n}" % o["name"])
        elif kind < 0.29:
            lines.append("monitor = $mon, preferred, auto, 1")
        else:
            w, h, rr = rng.choice([(o["width"], o["height"], o["refreshRate"])] + MODES[:3])
            mode = rng.choice(["%dx%d@%d" % (w, h, round(rr)), "%dx%d@%d" % (w, h, round(rr)), "%dx%d" % (w, h),
                               "preferred", "highres", "0x0", "%dx%d@%.2f" % (w, h, rr)])
            pos = rng.choice(["auto", "0x0", "%dx%d" % (o["x"], o["y"]), "1920x0", "auto-left"])
            scale = rng.choice(["1", "1.25", "1.5", "1.6", "1.3", "2", "auto", "14.166667", "0.2"])
            keys = rng.choice(["", ", transform, %d" % o["transform"], ", transform, 1", ", mirror, %s" % nm[0],
                               ", vrr, 1", ", bitdepth, 10", ", sdr_eotf, 1", ", cm, hdr"])
            lines.append("monitor = %s, %s, %s, %s%s" % (sel, mode, pos, scale, keys))
    return "\n".join(lines) + "\n", outs


def run_generated(tool, work, model, rng, table, fakebin, hide, marker_dir):
    ok_n, first_fail = 0, None
    for k in range(GEN):
        text, outs = gen_case(rng, table)
        raw = json.dumps(outs, indent=2).encode()
        want, rc_want = model_out(model, raw, [text])
        d = tempfile.mkdtemp(dir=work, prefix="fx-")
        home = os.path.join(d, "home")
        os.makedirs(home)
        dp, cp = os.path.join(d, "monitors.json"), os.path.join(d, "c0.conf")
        with open(dp, "wb") as f:
            f.write(raw)
        with open(cp, "w") as f:
            f.write(text)
        env = {"PATH": fakebin + ":/usr/bin:/bin", "LANG": "C.UTF-8", "HOME": home,
               "HYPRLAND_INSTANCE_SIGNATURE": "mado-r45-fixture"}
        try:
            p = subprocess.run(sandbox([sys.executable, "-I", tool, "--monitors", dp, "--config", cp], d, hide,
                                       marker_dir), capture_output=True, env=env, timeout=20)
            ok = p.returncode == rc_want and p.stdout.decode("utf-8", "replace") == want and p.stderr == b""
        except subprocess.TimeoutExpired:
            ok = False
        ok_n += ok
        if not ok and first_fail is None:
            first_fail = (k, text, want, rc_want)
    return ok_n, first_fail


class Setup(Exception):
    pass


def lane_root():
    return os.path.realpath(os.path.join(HERE, "..", ".."))


def hidden_paths(repo):
    lr = lane_root()
    return sorted({os.path.realpath(repo), lr, os.path.dirname(lr)})


def under(p, root):
    p, root = os.path.realpath(p), os.path.realpath(root)
    return p == root or p.startswith(root.rstrip("/") + "/")


def sandbox(argv, cwd, hide, marker_dir):
    cmd = ["bwrap", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc", "--unshare-pid", "--unshare-net",
           "--die-with-parent"]
    for h in hide:
        cmd += ["--tmpfs", h]
    cmd += ["--bind", marker_dir, marker_dir, "--chdir", cwd, "--"]
    return cmd + argv


def env_b(home, fakebin, rng):
    return {"PATH": fakebin + ":/usr/bin:/bin", "LANG": "en_US.UTF-8", "HOME": home,
            "HYPRLAND_INSTANCE_SIGNATURE": "%040x_%010d_%05d" % (rng.getrandbits(160), rng.randrange(10 ** 10),
                                                                  rng.randrange(10 ** 5)),
            "XDG_RUNTIME_DIR": "/run/user/%d" % os.getuid()}


def run_fixture(tool, work, fx, table, fakebin, hide, marker_dir, variant, rng):
    label, configs, dump, stdin, expect, rc_want = fx
    prefix = "fx-" if variant == "A" else "job-%x-" % rng.getrandbits(32)
    d = tempfile.mkdtemp(dir=work, prefix=prefix)
    home = os.path.join(d, "home" if variant == "A" else "vgpnk")
    os.makedirs(home)
    args, data = [], None
    if isinstance(dump, bytes):
        raw = dump.replace(b"{A}", table["{A}"].encode())
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
            with open(cp, "w", newline="") as f:
                f.write(subst(text, table))
            args += ["--config", cp]
    if variant == "A":
        env = {"PATH": fakebin + ":/usr/bin:/bin", "LANG": "C.UTF-8", "HOME": home,
               "HYPRLAND_INSTANCE_SIGNATURE": "mado-r45-fixture"}
    else:
        env = env_b(home, fakebin, rng)
    try:
        p = subprocess.run(sandbox([sys.executable, "-I", tool] + args, d, hide, marker_dir), input=data,
                           capture_output=True, env=env, timeout=20)
    except subprocess.TimeoutExpired:
        return False, "timeout"
    want = "".join(subst(l, table) + "\n" for l in expect)
    got = p.stdout.decode("utf-8", errors="replace")
    ok = p.returncode == rc_want and got == want and p.stderr == b""
    why = "" if ok else "rc=%d want_rc=%d stderr=%r got=%r" % (p.returncode, rc_want, p.stderr[-200:], got[-300:])
    return ok, why


def score(repo, rev, work, nonce):
    import random
    full = git(repo, "rev-parse", "--verify", rev + "^{commit}")
    if full is None:
        raise Setup("bad rev")
    full = full.decode().strip()
    ls = git(repo, "ls-tree", full, "--", TOOL)
    present = bool(ls) and ls.split()[0] in (b"100644", b"100755") and ls.split()[1] == b"blob"
    print("%s clause=a tool=%s" % (PRED, "present" if present else "absent"))
    hide = hidden_paths(repo)
    fixtures_ok, selftest, readonly = 0, "fail", "fail"
    if present:
        blob = git(repo, "show", "%s:%s" % (full, TOOL))
        tdir = tempfile.mkdtemp(dir=work, prefix="tool-")
        tool = os.path.join(tdir, "mado-monitors.py")
        with open(tool, "wb") as f:
            f.write(blob)
        marker_dir = tempfile.mkdtemp(dir=work, prefix="mk-")
        marker = os.path.join(marker_dir, "marker")
        fakebin = os.path.join(tempfile.mkdtemp(dir=work, prefix="bin-"), "bin")
        make_fakebin(fakebin, marker)
        sd = tempfile.mkdtemp(dir=work, prefix="st-")
        try:
            p = subprocess.run(sandbox([sys.executable, "-I", tool, "--selftest"], sd, hide, marker_dir),
                               capture_output=True, env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "HOME": sd},
                               timeout=60)
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
        rng = random.Random(nonce)
        t45, tn = names(45), names(nonce)
        for fx in FIXTURES:
            res = []
            for table, variant in ((t45, "A"), (t45, "B"), (tn, "A")):
                res.append(run_fixture(tool, work, fx, table, fakebin, hide, marker_dir, variant, rng))
            ok = all(r[0] for r in res)
            fixtures_ok += ok
            why = "; ".join("%s:%s" % (lab, r[1]) for lab, r in zip(("45A", "45B", "nA"), res) if not r[0])
            print("%s clause=f fixture=%s %s%s" % (PRED, fx[0], "pass" if ok else "FAIL", "" if ok else " " + why))
        model = load_model()
        g_ok, first_fail = run_generated(tool, work, model, random.Random(nonce ^ 0x5DEECE66D), tn, fakebin, hide,
                                         marker_dir)
        print("%s clause=g generated=%d/%d%s" % (PRED, g_ok, GEN, "" if first_fail is None else
                                                 " first_fail=%r" % (first_fail[:2],)))
        readonly = "fail" if os.path.exists(marker) else "ok"
        print("%s clause=r marker=%s" % (PRED, "present" if readonly == "fail" else "absent"))
    else:
        g_ok = 0
    met = (present and selftest == "ok" and readonly == "ok" and fixtures_ok == len(FIXTURES) and g_ok == GEN)
    print("%s: fixtures=%d/%d generated=%d/%d selftest=%s readonly=%s tool=%s verdict=%s rev=%s seeds=45,%d" % (
        PRED, fixtures_ok, len(FIXTURES), g_ok, GEN, selftest, readonly, "present" if present else "absent",
        "TARGET_MET" if met else "TARGET_MISSED", full, nonce))
    return 0 if met else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--nonce", type=int, default=None)
    a = ap.parse_args()
    nonce = a.nonce if a.nonce is not None else int.from_bytes(os.urandom(4), "big")
    try:
        if not os.path.isdir(a.work):
            raise Setup("work dir missing")
        if shutil.which("bwrap") is None:
            raise Setup("bwrap missing")
        for h in hidden_paths(a.repo):
            if under(a.work, h):
                raise Setup("work dir inside a hidden path %s" % h)
        work = tempfile.mkdtemp(dir=a.work, prefix="c1r45v2-")
        try:
            return score(a.repo, a.rev, work, nonce)
        finally:
            shutil.rmtree(work, ignore_errors=True)
    except Setup as e:
        print("%s: SETUP %s" % (PRED, e))
        return 2


if __name__ == "__main__":
    sys.exit(main())

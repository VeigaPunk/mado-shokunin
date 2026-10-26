#!/usr/bin/env python3
"""mado-monitors - does each connected output run the mode, position, scale and transform its monitor rule declares?

Hyprland 0.56.2 (efb50993) parses each `monitor = NAME, MODE, POSITION, SCALE[, KEY, VALUE]...` line
into a monitor rule (src/config/legacy/ConfigManager.cpp handleMonitor, src/config/shared/monitor/
Parser.cpp), keeps at most one rule per selector string - adding a rule erases every earlier rule with the
same selector and appends the new one (MonitorRuleManager.cpp add) - and gives an output the LAST rule whose
selector matches it, else the first rule with an empty selector (MonitorRuleManager.cpp get). A selector
matches by exact name, or, as `desc:TEXT`, when the output's description starts with TEXT (Monitor.cpp
matchesStaticSelector). Applying the rule (Monitor.cpp applyMonitorRule) picks the available mode closest to
the requested one - a rule without `@RATE` requests 60 Hz (MonitorRule.hpp `m_refreshRate = 60`) - and
replaces a scale whose logical size would be fractional by the nearest multiple of 1/120 that divides the
pixel size, searching 89 steps up and down. `hyprctl monitors all -j` reports each output's live state
(HyprCtl.cpp getMonitorData). This tool joins the two read-only inputs: the monitor lines of one or more
config files and one `hyprctl monitors all -j` dump. It is a join, not a blame: a DIFFER may come from a
runtime `hyprctl keyword monitor`, a wlr-output-management client, or a mode the output does not offer.

    hyprctl monitors all -j | mado-monitors.py --monitors - --config ~/.config/hypr/monitors.conf
    mado-monitors.py --monitors mons.json --config a.conf --config b.conf
    mado-monitors.py --selftest

It reads files and standard input only; it starts no process and opens no socket.

Arguments (two-token form only; anything else is usage): `--selftest` alone, or `--monitors V` exactly once
and `--config V` one or more times, in any order. Setup failure: stdout is exactly one line
`MADO_MONITORS: SETUP <reason>`, exit 2, reason one of usage | unreadable | too_large | bad_json. A PATH that
is missing, unreadable, a directory, a FIFO or any non-regular file is unreadable; an input larger than
1048576 bytes is too_large (stdin, `--monitors -`, is read at most 1048577 bytes); a monitors input that is
not UTF-8 JSON holding a list whose every element is an object is bad_json.

Lines. Config files are read in argument order, each decoded as UTF-8 with errors replaced and split on
"\\n"; a line is stripped of spaces and tabs at both ends. A line whose first token (up to a space, tab, `=`
or `{`) is `monitorv2` adds one to `v2`. A MONITOR LINE fullmatches `monitor[ \\t]*=(.*)` and adds one to
`lines`. Its body: if it contains `##`, `$` or a backslash the line adds one to `unsupported` and is not
modelled; else it is cut at its first `#`, split on ",", and each field is stripped of spaces and tabs;
field i is "" past the end. Field 0 is the selector SEL.
  - field 1 `disable` or `disabled`: add a rule (SEL, disabled).
  - field 1 `transform`: field 2 must be one digit 0-7, else the line adds one to `badrules`. The first rule
    in the current list whose selector equals SEL is copied with that transform and the copy is added; with
    no such rule nothing happens.
  - field 1 `addreserved`: fields 2-5 must each fullmatch `-?[0-9]{1,6}`, else `badrules`. If a rule with
    selector SEL exists nothing changes (the reserved area is not compared); otherwise a default rule
    (SEL, mode preferred, position auto, scale auto, transform 0) is added.
  - otherwise MODE = field 1, POSITION = field 2, SCALE = field 3, then KEY VALUE pairs from field 4 while
    the key field is not "": keys mirror, bitdepth, cm, sdrsaturation, sdrbrightness, transform, vrr, icc
    each consume the next field; any other key adds one to `badrules` and the rule is not added (Hyprland
    returns "invalid syntax" before adding it). MODE: "" or starting `pref` is preferred; starting
    `highrr`, `highres`, `maxwidth` is that keyword; a first token `modeline` (any case) is modeline; else it
    must fullmatch `([0-9]{1,5})x([0-9]{1,5})(@[0-9]{1,3}(\\.[0-9]{1,3})?)?` giving W, H and RATE (the
    number after `@` rounded to a 32-bit float, else 60). POSITION: "" or starting `auto` is auto; else
    `(-?[0-9]{1,6})x(-?[0-9]{1,6})` gives X, Y. SCALE: "" or starting `auto` is auto; else
    `[0-9]{1,2}(\\.[0-9]{1,6})?` gives S (a 32-bit float; S < 0.25 becomes 1.0, as Hyprland's parser does).
    `transform` VALUE must be one digit 0-7; `mirror` VALUE is the mirrored output's name. A MODE, POSITION,
    SCALE or transform VALUE outside these forms makes the line `unsupported` (not modelled).
Adding a rule erases every earlier rule with the same selector and appends it. Rules are numbered n=1.. in
the final list.

Monitors. Every dump element is one output, in dump order. name is `name` when a string, else "";
description is `description` when a string, else "". The EFFECTIVE rule is the last rule in the list whose
selector is not "" and matches (selector `desc:TEXT`: description starts with TEXT stripped of spaces and
tabs; else selector == name), else the first rule whose selector is "", else none. The dump carries only the
short description (make, model, serial); Hyprland also tests the long one, so a `desc:` selector matching only
the long description is reported unmatched here.
An output with no effective rule is UNRULED. live_disabled is `disabled` == JSON true. If the rule is
disabled the verdict is DISABLED when live_disabled, else DIFFER with differ=disabled. If the rule is enabled
and live_disabled, DIFFER with differ=disabled. Otherwise each compared field is checked, in this order:
  mode       (explicit W x H only) `width` == W, `height` == H and |`refreshRate` - RATE| < 1.0 (Hyprland's own
             closeness test for a requested mode, Monitor.cpp DELTALESSTHAN(..., 1));
  position   (explicit only) `x` == X and `y` == Y;
  scale      (explicit only) the expected scale E is Hyprland's correction of S for the live `width` and
             `height`: E = S when both width/S and height/S are whole; else, with K = round-half-up(S*120),
             K/120 when it divides both; else the first of (K+i)/120, (K-i)/120 for i = 1..89 that divides
             both; none found means the scale is not compared. Agree when |`scale` - E| < 0.0001;
  transform  `transform` == the rule's transform (default 0);
  mirror     with a rule mirror M: `mirrorOf` is the decimal `id` of the dump output named M; without one:
             `mirrorOf` == "none".
A live value that is missing or of the wrong JSON type (integers for width, height, x, y, transform, id;
a number for refreshRate and scale; a string for mirrorOf; booleans are never numbers) fails its field.
No failing field is AGREE; otherwise DIFFER with the failing fields comma-joined in the order above.

Output (stdout; nothing else; stderr empty on exit 0/1/3/4/5), in order:
  per rule     MADO_MON_RULE: n=<n> sel=<json> mode=<WxH@R|preferred|highrr|highres|maxwidth|modeline> pos=<XxY|auto> scale=<S|auto> transform=<T> mirror=<json|-> disabled=<true|false>
  per output   MADO_MON_OUTPUT: name=<json> rule=<n|-> differ=<fields|-> verdict=<AGREE|DIFFER|DISABLED|UNRULED>
  last         MADO_MONITORS: lines=<n> rules=<n> v2=<n> unsupported=<n> badrules=<n> outputs=<n> matched=<n> unruled=<n> agree=<n> differ=<n> disabled=<n> verdict=<V>
(<json> is json.dumps with ensure_ascii; R is printed with two decimals, S with four.) V = NO_RULES (exit 4,
lines = 0 and v2 = 0) | NOT_COMPARED (exit 5, v2 > 0 or unsupported > 0: a monitorv2 block or an unmodelled
line can change which rule applies) | DIFFER (exit 1, differ > 0) | NO_MATCHING_MONITOR (exit 3, matched = 0)
| OK (exit 0), tested in that order. matched counts outputs with an effective rule.
"""
import json
import math
import os
import re
import stat
import struct
import sys

MAX_BYTES = 1048576
LINE_RE = re.compile(r"monitor[ \t]*=(.*)")
V2_RE = re.compile(r"monitorv2(?:[ \t={]|$)")
MODE_RE = re.compile(r"([0-9]{1,5})x([0-9]{1,5})(@([0-9]{1,3}(\.[0-9]{1,3})?))?")
POS_RE = re.compile(r"(-?[0-9]{1,6})x(-?[0-9]{1,6})")
SCALE_RE = re.compile(r"[0-9]{1,2}(\.[0-9]{1,6})?")
RES_RE = re.compile(r"-?[0-9]{1,6}")
KEYS = ("mirror", "bitdepth", "cm", "sdrsaturation", "sdrbrightness", "transform", "vrr", "icc")


class Setup(Exception):
    pass


class Unsupported(Exception):
    pass


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


def read_regular(path):
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
    except OSError:
        raise Setup("unreadable")
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise Setup("unreadable")
        data = b""
        while len(data) <= MAX_BYTES:
            chunk = os.read(fd, MAX_BYTES + 1 - len(data))
            if not chunk:
                break
            data += chunk
    except OSError:
        raise Setup("unreadable")
    finally:
        os.close(fd)
    if len(data) > MAX_BYTES:
        raise Setup("too_large")
    return data


def read_stdin():
    data = b""
    while len(data) <= MAX_BYTES:
        chunk = sys.stdin.buffer.read(MAX_BYTES + 1 - len(data))
        if not chunk:
            break
        data += chunk
    if len(data) > MAX_BYTES:
        raise Setup("too_large")
    return data


def parse_args(argv):
    if argv == ["--selftest"]:
        return "selftest", None, None
    monitors, configs, i = None, [], 0
    while i < len(argv):
        if i + 1 >= len(argv):
            raise Setup("usage")
        flag, value = argv[i], argv[i + 1]
        if flag == "--monitors" and monitors is None:
            monitors = value
        elif flag == "--config":
            configs.append(value)
        else:
            raise Setup("usage")
        i += 2
    if monitors is None or not configs:
        raise Setup("usage")
    return "run", monitors, configs


def new_rule(sel):
    return {"sel": sel, "disabled": False, "mode": "preferred", "w": 0, "h": 0, "rate": 60.0,
            "pos": None, "scale": None, "transform": 0, "mirror": ""}


def add(rules, rule):
    rules[:] = [r for r in rules if r["sel"] != rule["sel"]]
    rules.append(rule)


def parse_mode(rule, value):
    low = value.lower()
    if value == "" or value.startswith("pref"):
        return
    for kw in ("highrr", "highres", "maxwidth"):
        if value.startswith(kw):
            rule["mode"] = kw
            return
    toks = low.split()
    if toks and toks[0] == "modeline":
        rule["mode"] = "modeline"
        return
    m = MODE_RE.fullmatch(value)
    if not m:
        raise Unsupported()
    rule["mode"] = "explicit"
    rule["w"], rule["h"] = int(m.group(1)), int(m.group(2))
    rule["rate"] = f32(float(m.group(4))) if m.group(4) is not None else 60.0


def parse_pos(rule, value):
    if value == "" or value.startswith("auto"):
        return
    m = POS_RE.fullmatch(value)
    if not m:
        raise Unsupported()
    rule["pos"] = (int(m.group(1)), int(m.group(2)))


def parse_scale(rule, value):
    if value == "" or value.startswith("auto"):
        return
    if not SCALE_RE.fullmatch(value):
        raise Unsupported()
    s = f32(float(value))
    rule["scale"] = 1.0 if s < 0.25 else s


def transform_value(value):
    if len(value) == 1 and value in "01234567":
        return int(value)
    return None


def parse_line(body, rules, counts):
    if "##" in body or "$" in body or "\\" in body:
        counts["unsupported"] += 1
        return
    body = body.split("#", 1)[0]
    fields = [f.strip(" \t") for f in body.split(",")]

    def fld(i):
        return fields[i] if i < len(fields) else ""

    sel = fld(0)
    kind = fld(1)
    if kind in ("disable", "disabled"):
        r = new_rule(sel)
        r["disabled"] = True
        add(rules, r)
        return
    if kind == "transform":
        t = transform_value(fld(2))
        if t is None:
            counts["badrules"] += 1
            return
        for r in rules:
            if r["sel"] == sel:
                cpy = dict(r)
                cpy["transform"] = t
                add(rules, cpy)
                return
        return
    if kind == "addreserved":
        if not all(RES_RE.fullmatch(fld(i)) for i in range(2, 6)):
            counts["badrules"] += 1
            return
        if any(r["sel"] == sel for r in rules):
            return
        add(rules, new_rule(sel))
        return
    r = new_rule(sel)
    try:
        parse_mode(r, kind)
        parse_pos(r, fld(2))
        parse_scale(r, fld(3))
        i = 4
        while fld(i) != "":
            key = fld(i)
            if key not in KEYS:
                counts["badrules"] += 1
                return
            val = fld(i + 1)
            if key == "transform":
                t = transform_value(val)
                if t is None:
                    raise Unsupported()
                r["transform"] = t
            elif key == "mirror":
                r["mirror"] = val
            i += 2
    except Unsupported:
        counts["unsupported"] += 1
        return
    add(rules, r)


def parse_config(text, rules, counts):
    for raw in text.split("\n"):
        line = raw.strip(" \t")
        if V2_RE.match(line):
            counts["v2"] += 1
            continue
        m = LINE_RE.fullmatch(line)
        if not m:
            continue
        counts["lines"] += 1
        parse_line(m.group(1), rules, counts)


def parse_monitors(data):
    try:
        doc = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        raise Setup("bad_json")
    if not isinstance(doc, list) or not all(isinstance(m, dict) for m in doc):
        raise Setup("bad_json")
    return doc


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def whole(x):
    return math.isfinite(x) and x == math.floor(x + 0.5)


def expected_scale(s, w, h):
    if whole(w / s) and whole(h / s):
        return s
    k = math.floor(s * 120.0 + 0.5)
    z = k / 120.0
    if z > 0 and whole(w / z) and whole(h / z):
        return f32(z)
    for i in range(1, 90):
        for cand in ((k + i) / 120.0, (k - i) / 120.0):
            if cand != 0 and whole(w / cand) and whole(h / cand):
                return f32(cand)
    return None


def str_or_empty(v):
    return v if isinstance(v, str) else ""


def effective(rules, mon):
    name, desc = str_or_empty(mon.get("name")), str_or_empty(mon.get("description"))
    for n in range(len(rules), 0, -1):
        sel = rules[n - 1]["sel"]
        if sel == "":
            continue
        if sel.startswith("desc:"):
            if desc.startswith(sel[5:].strip(" \t")):
                return n
        elif sel == name:
            return n
    for n, r in enumerate(rules, 1):
        if r["sel"] == "":
            return n
    return None


def compare(rule, mon, mons):
    live_disabled = mon.get("disabled") is True
    if rule["disabled"]:
        return ([], "DISABLED") if live_disabled else (["disabled"], "DIFFER")
    if live_disabled:
        return ["disabled"], "DIFFER"
    bad = []
    w, h = mon.get("width"), mon.get("height")
    if rule["mode"] == "explicit":
        rr = mon.get("refreshRate")
        if not (is_int(w) and is_int(h) and is_num(rr) and w == rule["w"] and h == rule["h"]
                and abs(rr - rule["rate"]) < 1.0):
            bad.append("mode")
    if rule["pos"] is not None:
        x, y = mon.get("x"), mon.get("y")
        if not (is_int(x) and is_int(y) and (x, y) == rule["pos"]):
            bad.append("position")
    if rule["scale"] is not None:
        sc = mon.get("scale")
        if not (is_int(w) and is_int(h) and is_num(sc)):
            bad.append("scale")
        else:
            e = expected_scale(rule["scale"], w, h) if w > 0 and h > 0 else None
            if e is not None and abs(sc - e) >= 0.0001:
                bad.append("scale")
    t = mon.get("transform")
    if not (is_int(t) and t == rule["transform"]):
        bad.append("transform")
    mo = mon.get("mirrorOf")
    if rule["mirror"]:
        ids = [m.get("id") for m in mons if is_int(m.get("id"))]
        if not (isinstance(mo, str) and any(mo == str(i) for i in ids)):
            bad.append("mirror")
    elif mo != "none":
        bad.append("mirror")
    return bad, ("DIFFER" if bad else "AGREE")


def rule_line(n, r):
    mode = r["mode"]
    if mode == "explicit":
        mode = "%dx%d@%.2f" % (r["w"], r["h"], r["rate"])
    pos = "auto" if r["pos"] is None else "%dx%d" % r["pos"]
    scale = "auto" if r["scale"] is None else "%.4f" % r["scale"]
    return "MADO_MON_RULE: n=%d sel=%s mode=%s pos=%s scale=%s transform=%d mirror=%s disabled=%s" % (
        n, json.dumps(r["sel"]), mode, pos, scale, r["transform"],
        json.dumps(r["mirror"]) if r["mirror"] else "-", "true" if r["disabled"] else "false")


def report(monitors_data, config_texts):
    rules = []
    counts = {"lines": 0, "v2": 0, "unsupported": 0, "badrules": 0}
    for text in config_texts:
        parse_config(text, rules, counts)
    mons = parse_monitors(monitors_data)
    out = [rule_line(n, r) for n, r in enumerate(rules, 1)]
    t = {"outputs": 0, "matched": 0, "unruled": 0, "agree": 0, "differ": 0, "disabled": 0}
    for mon in mons:
        t["outputs"] += 1
        n = effective(rules, mon)
        if n is None:
            bad, verdict = [], "UNRULED"
            t["unruled"] += 1
        else:
            t["matched"] += 1
            bad, verdict = compare(rules[n - 1], mon, mons)
            t[verdict.lower()] += 1
        out.append("MADO_MON_OUTPUT: name=%s rule=%s differ=%s verdict=%s" % (
            json.dumps(str_or_empty(mon.get("name"))), "-" if n is None else str(n),
            ",".join(bad) if bad else "-", verdict))
    if counts["lines"] == 0 and counts["v2"] == 0:
        v, rc = "NO_RULES", 4
    elif counts["v2"] > 0 or counts["unsupported"] > 0:
        v, rc = "NOT_COMPARED", 5
    elif t["differ"] > 0:
        v, rc = "DIFFER", 1
    elif t["matched"] == 0:
        v, rc = "NO_MATCHING_MONITOR", 3
    else:
        v, rc = "OK", 0
    out.append("MADO_MONITORS: lines=%d rules=%d v2=%d unsupported=%d badrules=%d outputs=%d matched=%d "
               "unruled=%d agree=%d differ=%d disabled=%d verdict=%s" % (
                   counts["lines"], len(rules), counts["v2"], counts["unsupported"], counts["badrules"],
                   t["outputs"], t["matched"], t["unruled"], t["agree"], t["differ"], t["disabled"], v))
    return out, rc


def mon(name, w=3440, h=1440, rr=99.997, x=0, y=0, scale=1, transform=0, disabled=False,
        mirror="none", desc="", mid=0):
    return {"id": mid, "name": name, "description": desc, "width": w, "height": h, "refreshRate": rr,
            "x": x, "y": y, "scale": scale, "transform": transform, "disabled": disabled, "mirrorOf": mirror}


def selftest():
    cases = [
        # (label, config, monitors, expected final verdict, expected rc, expected output-line suffixes)
        ("host", "monitor = DP-1, 3440x1440@100, 0x0, 1\n", [mon("DP-1")], "OK", 0, ["verdict=AGREE"]),
        ("no-rate-is-60", "monitor = DP-1, 3440x1440, 0x0, 1\n", [mon("DP-1")], "DIFFER", 1, ["differ=mode verdict=DIFFER"]),
        ("rate-60", "monitor = DP-1, 3440x1440, 0x0, 1\n", [mon("DP-1", rr=59.99)], "OK", 0, ["verdict=AGREE"]),
        ("rate-off-by-1", "monitor = DP-1, 3440x1440@100, 0x0, 1\n", [mon("DP-1", rr=99.0)], "DIFFER", 1, ["differ=mode verdict=DIFFER"]),
        ("res", "monitor = DP-1, 2560x1440@100, 0x0, 1\n", [mon("DP-1")], "DIFFER", 1, ["differ=mode verdict=DIFFER"]),
        ("pos", "monitor = DP-1, 3440x1440@100, 10x0, 1\n", [mon("DP-1")], "DIFFER", 1, ["differ=position verdict=DIFFER"]),
        ("auto-pos", "monitor = DP-1, 3440x1440@100, auto, 1\n", [mon("DP-1", x=1920)], "OK", 0, ["verdict=AGREE"]),
        ("preferred", "monitor = , preferred, auto, auto\n", [mon("DP-1", w=1920, h=1080, rr=60.0, scale=1.25)], "OK", 0, ["rule=1 differ=- verdict=AGREE"]),
        ("scale-clean", "monitor = DP-1, 3440x1440@100, 0x0, 1.25\n", [mon("DP-1", scale=1.25)], "OK", 0, ["verdict=AGREE"]),
        ("scale-snap", "monitor = eDP-1, 2880x1920@120, 0x0, 1.6\n", [mon("eDP-1", w=2880, h=1920, rr=120.0, scale=1.6)], "OK", 0, ["verdict=AGREE"]),
        ("scale-snap-wrong", "monitor = DP-1, 3440x1440@100, 0x0, 1.3\n", [mon("DP-1", scale=1.3)], "DIFFER", 1, ["differ=scale verdict=DIFFER"]),
        ("transform", "monitor = DP-2, 1920x1080@60, 0x0, 1, transform, 1\n", [mon("DP-2", w=1920, h=1080, rr=60.0, transform=1)], "OK", 0, ["verdict=AGREE"]),
        ("transform-missing", "monitor = DP-2, 1920x1080@60, 0x0, 1\n", [mon("DP-2", w=1920, h=1080, rr=60.0, transform=1)], "DIFFER", 1, ["differ=transform verdict=DIFFER"]),
        ("transform-modifier", "monitor = DP-2, 1920x1080@60, 0x0, 1\nmonitor = DP-2, transform, 3\n", [mon("DP-2", w=1920, h=1080, rr=60.0, transform=3)], "OK", 0, ["verdict=AGREE"]),
        ("last-wins", "monitor = DP-1, 1920x1080@60, 0x0, 1\nmonitor = DP-1, 3440x1440@100, 0x0, 1\n", [mon("DP-1")], "OK", 0, ["rule=1 differ=- verdict=AGREE"]),
        ("desc-later", "monitor = DP-1, 1920x1080@60, 0x0, 1\nmonitor = desc:Dell Inc. U34, 3440x1440@100, 0x0, 1\n", [mon("DP-1", desc="Dell Inc. U3415W X1")], "OK", 0, ["rule=2 differ=- verdict=AGREE"]),
        ("readd-moves", "monitor = desc:Dell, 3440x1440@100, 0x0, 1\nmonitor = DP-1, 1920x1080@60, 0x0, 1\nmonitor = desc:Dell, 3440x1440@100, 0x0, 1\n", [mon("DP-1", desc="Dell U34")], "OK", 0, ["rule=2 differ=- verdict=AGREE"]),
        ("fallback", "monitor = , preferred, auto, 1\nmonitor = HDMI-A-1, 1920x1080@60, 0x0, 1\n", [mon("DP-1"), mon("HDMI-A-1", w=1920, h=1080, rr=60.0, x=3440)], "DIFFER", 1, ["rule=1 differ=- verdict=AGREE", "rule=2 differ=position verdict=DIFFER"]),
        ("unruled", "monitor = HDMI-A-1, 1920x1080@60, 0x0, 1\n", [mon("DP-1")], "NO_MATCHING_MONITOR", 3, ["rule=- differ=- verdict=UNRULED"]),
        ("disabled-agree", "monitor = DP-2, disable\n", [mon("DP-2", disabled=True)], "OK", 0, ["verdict=DISABLED"]),
        ("disabled-differ", "monitor = DP-2, disable\n", [mon("DP-2")], "DIFFER", 1, ["differ=disabled verdict=DIFFER"]),
        ("live-disabled", "monitor = DP-2, 1920x1080@60, 0x0, 1\n", [mon("DP-2", disabled=True)], "DIFFER", 1, ["differ=disabled verdict=DIFFER"]),
        ("mirror", "monitor = DP-1, 3440x1440@100, 0x0, 1\nmonitor = DP-2, 3440x1440@100, 0x0, 1, mirror, DP-1\n", [mon("DP-1", mid=0), mon("DP-2", mid=1, mirror="0")], "OK", 0, ["rule=1 differ=- verdict=AGREE", "rule=2 differ=- verdict=AGREE"]),
        ("badkey", "monitor = DP-1, 3440x1440@100, 0x0, 1, wat, 1\n", [mon("DP-1")], "NO_MATCHING_MONITOR", 3, ["verdict=UNRULED"]),
        ("v2", "monitorv2 {\n  output = DP-1\n}\nmonitor = DP-1, 3440x1440@100, 0x0, 1\n", [mon("DP-1")], "NOT_COMPARED", 5, ["verdict=AGREE"]),
        ("variable", "monitor = $main, 3440x1440@100, 0x0, 1\n", [mon("DP-1")], "NOT_COMPARED", 5, ["verdict=UNRULED"]),
        ("comment", "# monitor = DP-1, 1x1, 0x0, 1\nmonitor = DP-1, 3440x1440@100, 0x0, 1 # main\n", [mon("DP-1")], "OK", 0, ["verdict=AGREE"]),
        ("norules", "general {\n}\n", [mon("DP-1")], "NO_RULES", 4, ["verdict=UNRULED"]),
        ("badtype", "monitor = DP-1, 3440x1440@100, 0x0, 1\n", [dict(mon("DP-1"), x="0", transform=True)], "DIFFER", 1, ["differ=position,transform verdict=DIFFER"]),
        ("addreserved-new", "monitor = DP-1, addreserved, 10, 0, 0, 0\n", [mon("DP-1", x=50, scale=1.5)], "OK", 0, ["rule=1 differ=- verdict=AGREE"]),
    ]
    passed = 0
    for label, cfg, mons, want_v, want_rc, suffixes in cases:
        lines, rc = report(json.dumps(mons).encode(), [cfg])
        outs = [l for l in lines if l.startswith("MADO_MON_OUTPUT:")]
        ok = (rc == want_rc and lines[-1].endswith("verdict=" + want_v) and len(outs) == len(suffixes)
              and all(o.endswith(s) for o, s in zip(outs, suffixes)))
        if ok:
            passed += 1
        else:
            print("MADO_MONITORS_SELFTEST: FAIL %s rc=%d %s" % (label, rc, " | ".join(lines)))
    # setup paths
    for argv, reason in ((["--monitors", "-"], "usage"), (["--config", "x"], "usage"),
                         (["--monitors", "/nonexistent/x", "--config", "/nonexistent/y"], "unreadable")):
        lines, rc = run(argv)
        if rc == 2 and lines == ["MADO_MONITORS: SETUP " + reason]:
            passed += 1
        else:
            print("MADO_MONITORS_SELFTEST: FAIL setup %s %r" % (reason, lines))
    total = len(cases) + 3
    print("MADO_MONITORS_SELFTEST: %d/%d passed" % (passed, total))
    return 0 if passed == total else 1


def run(argv):
    try:
        mode, monitors, configs = parse_args(argv)
        if mode == "selftest":
            return None, selftest()
        mdata = read_stdin() if monitors == "-" else read_regular(monitors)
        texts = [read_regular(c).decode("utf-8", errors="replace") for c in configs]
        return report(mdata, texts)
    except Setup as e:
        return ["MADO_MONITORS: SETUP %s" % e], 2


def main():
    lines, rc = run(sys.argv[1:])
    if lines is not None:
        sys.stdout.write("".join(l + "\n" for l in lines))
    return rc


if __name__ == "__main__":
    sys.exit(main())

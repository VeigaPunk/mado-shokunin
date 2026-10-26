#!/usr/bin/env python3
"""mado-monitors - does each connected output run the mode, position, scale and transform its monitor rule declares?

Independent implementation of the PRED-C1-r45 contract, written from the reference docstring only
(mado round 45, seat ExecIndepA). Read-only: it reads files and stdin, starts no process, opens no socket.
"""
import json
import math
import os
import re
import stat
import struct
import sys
from fractions import Fraction

MAX_BYTES = 1048576
MONITOR_LINE = re.compile(r"monitor[ \t]*=(.*)")
MODE_RE = re.compile(r"([0-9]{1,5})x([0-9]{1,5})(?:@([0-9]{1,3})(?:\.([0-9]{1,3}))?)?")
POS_RE = re.compile(r"(-?[0-9]{1,6})x(-?[0-9]{1,6})")
SCALE_RE = re.compile(r"[0-9]{1,2}(?:\.[0-9]{1,6})?")
RESERVED_RE = re.compile(r"-?[0-9]{1,6}")
TKEY_RE = re.compile(r"[0-7]")
TOKEN_SPLIT = re.compile(r"[ \t={]")
FIELD_SPLIT = re.compile(r"[ \t]")
IGNORED_KEYS = frozenset(("bitdepth", "cm", "sdrsaturation", "sdrbrightness", "vrr", "icc"))


class SetupError(Exception):
    pass


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


# ---------------------------------------------------------------- config model


def parse_mode(raw):
    if raw == "" or raw.startswith("pref"):
        return ("preferred",)
    for kw in ("highrr", "highres", "maxwidth"):
        if raw.startswith(kw):
            return (kw,)
    if FIELD_SPLIT.split(raw, 1)[0].lower() == "modeline":
        return ("modeline",)
    m = MODE_RE.fullmatch(raw)
    if not m:
        return None
    rate = 60.0
    if m.group(3) is not None:
        text = m.group(3) + ("." + m.group(4) if m.group(4) else "")
        rate = f32(float(text))
    return ("mode", int(m.group(1)), int(m.group(2)), rate)


def parse_pos(raw):
    if raw == "" or raw.startswith("auto"):
        return ("auto",)
    m = POS_RE.fullmatch(raw)
    if not m:
        return None
    return ("xy", int(m.group(1)), int(m.group(2)))


def parse_scale(raw):
    if raw == "" or raw.startswith("auto"):
        return ("auto",)
    if not SCALE_RE.fullmatch(raw):
        return None
    s = f32(float(raw))
    if s < 0.25:
        s = 1.0
    return ("num", s)


def default_rule(sel):
    return {"sel": sel, "mode": ("preferred",), "pos": ("auto",), "scale": ("auto",),
            "transform": 0, "mirror": None, "disabled": False}


def add_rule(rules, rule):
    sel = rule["sel"]
    rules[:] = [r for r in rules if r["sel"] != sel]
    rules.append(rule)


def first_rule_for(rules, sel):
    for r in rules:
        if r["sel"] == sel:
            return r
    return None


def parse_configs(texts):
    v2 = lines = unsup = bad = adds = 0
    rules = []

    def add(rule):
        nonlocal adds
        add_rule(rules, rule)
        adds += 1

    for text in texts:
        for raw in text.split("\n"):
            line = raw.strip(" \t")
            if TOKEN_SPLIT.split(line, 1)[0] == "monitorv2":
                v2 += 1
            m = MONITOR_LINE.fullmatch(line)
            if not m:
                continue
            lines += 1
            body = m.group(1)
            if "##" in body or "$" in body or "\\" in body:
                unsup += 1
                continue
            body = body.split("#", 1)[0]
            fields = [f.strip(" \t") for f in body.split(",")]
            n = len(fields)

            def fld(i):
                return fields[i] if i < n else ""

            sel = fld(0)
            kind = fld(1)
            if kind in ("disable", "disabled"):
                r = default_rule(sel)
                r["disabled"] = True
                add(r)
                continue
            if kind == "transform":
                if not TKEY_RE.fullmatch(fld(2)):
                    bad += 1
                    continue
                src = first_rule_for(rules, sel)
                if src is None:
                    continue
                r = dict(src)
                r["transform"] = int(fld(2))
                add(r)
                continue
            if kind == "addreserved":
                if not all(RESERVED_RE.fullmatch(fld(i)) for i in (2, 3, 4, 5)):
                    bad += 1
                    continue
                if first_rule_for(rules, sel) is not None:
                    continue
                add(default_rule(sel))
                continue

            mirror = None
            transform = 0
            key_bad = key_unsup = False
            i = 4
            while i < n and fields[i] != "":
                key = fields[i]
                val = fld(i + 1)
                i += 2
                if key == "mirror":
                    mirror = val
                elif key == "transform":
                    if TKEY_RE.fullmatch(val):
                        transform = int(val)
                    else:
                        key_unsup = True
                elif key in IGNORED_KEYS:
                    continue
                else:
                    key_bad = True
                    break
            mode = parse_mode(fld(1))
            pos = parse_pos(fld(2))
            scale = parse_scale(fld(3))
            if key_unsup or mode is None or pos is None or scale is None:
                unsup += 1
                continue
            if key_bad:
                bad += 1
                continue
            add({"sel": sel, "mode": mode, "pos": pos, "scale": scale,
                 "transform": transform, "mirror": mirror, "disabled": False})
    return rules, {"lines": lines, "v2": v2, "unsupported": unsup, "badrules": bad, "adds": adds}


# ---------------------------------------------------------------- live side


def selector_matches(sel, name, desc):
    if sel.startswith("desc:"):
        return desc.startswith(sel[5:].strip(" \t"))
    return sel == name


def effective_rule(rules, name, desc):
    for r in reversed(rules):
        if r["sel"] == "":
            continue
        if selector_matches(r["sel"], name, desc):
            return r
    for r in rules:
        if r["sel"] == "":
            return r
    return None


def divides(total, fr):
    return total >= 0 and (Fraction(total) / fr).denominator == 1


def expected_scale(s, w, h):
    fs = Fraction(s)
    if divides(w, fs) and divides(h, fs):
        return s
    k = int(math.floor(s * 120.0 + 0.5))
    for i in range(1, 90):
        for kk in (k + i, k - i):
            if kk <= 0:
                continue
            fr = Fraction(kk, 120)
            if divides(w, fr) and divides(h, fr):
                return float(fr)
    return None


def compare(rule, mon, dump):
    fails = []
    mode = rule["mode"]
    if mode[0] == "mode":
        w, h, rate = mode[1], mode[2], mode[3]
        if not (is_int(mon.get("width")) and mon.get("width") == w
                and is_int(mon.get("height")) and mon.get("height") == h
                and is_num(mon.get("refreshRate")) and abs(mon.get("refreshRate") - rate) < 1.0):
            fails.append("mode")
    pos = rule["pos"]
    if pos[0] == "xy":
        if not (is_int(mon.get("x")) and mon.get("x") == pos[1]
                and is_int(mon.get("y")) and mon.get("y") == pos[2]):
            fails.append("position")
    sc = rule["scale"]
    if sc[0] == "num":
        w, h = mon.get("width"), mon.get("height")
        if is_int(w) and is_int(h):
            want = expected_scale(sc[1], w, h)
            if want is not None:
                live = mon.get("scale")
                if not (is_num(live) and abs(live - want) < 0.0001):
                    fails.append("scale")
    if not (is_int(mon.get("transform")) and mon.get("transform") == rule["transform"]):
        fails.append("transform")
    if rule["mirror"] is None:
        if not (isinstance(mon.get("mirrorOf"), str) and mon.get("mirrorOf") == "none"):
            fails.append("mirror")
    else:
        want = None
        for other in dump:
            oname = other.get("name") if isinstance(other.get("name"), str) else ""
            if oname == rule["mirror"] and is_int(other.get("id")):
                want = str(other.get("id"))
                break
        if want is None or not (isinstance(mon.get("mirrorOf"), str) and mon.get("mirrorOf") == want):
            fails.append("mirror")
    return fails


def fmt_mode(mode):
    if mode[0] == "mode":
        return "%dx%d@%.2f" % (mode[1], mode[2], mode[3])
    return mode[0]


def fmt_pos(pos):
    if pos[0] == "xy":
        return "%dx%d" % (pos[1], pos[2])
    return "auto"


def fmt_scale(sc):
    if sc[0] == "num":
        return "%.4f" % sc[1]
    return "auto"


def build_report(rules, counts, dump):
    out = []
    for idx, r in enumerate(rules, 1):
        out.append("MADO_MON_RULE: n=%d sel=%s mode=%s pos=%s scale=%s transform=%d mirror=%s disabled=%s" % (
            idx, json.dumps(r["sel"]), fmt_mode(r["mode"]), fmt_pos(r["pos"]), fmt_scale(r["scale"]),
            r["transform"], json.dumps(r["mirror"]) if r["mirror"] is not None else "-",
            "true" if r["disabled"] else "false"))
    matched = unruled = agree = differ = disabled = 0
    for mon in dump:
        name = mon.get("name") if isinstance(mon.get("name"), str) else ""
        desc = mon.get("description") if isinstance(mon.get("description"), str) else ""
        rule = effective_rule(rules, name, desc)
        live_disabled = mon.get("disabled") is True
        fields = "-"
        if rule is None:
            unruled += 1
            rn, verdict = "-", "UNRULED"
        else:
            matched += 1
            rn = str(rules.index(rule) + 1)
            if rule["disabled"]:
                if live_disabled:
                    verdict = "DISABLED"
                else:
                    verdict = "DIFFER"
                    fields = "disabled"
            elif live_disabled:
                verdict = "DIFFER"
                fields = "disabled"
            else:
                fails = compare(rule, mon, dump)
                if fails:
                    verdict = "DIFFER"
                    fields = ",".join(fails)
                else:
                    verdict = "AGREE"
        if verdict == "AGREE":
            agree += 1
        elif verdict == "DIFFER":
            differ += 1
        elif verdict == "DISABLED":
            disabled += 1
        out.append("MADO_MON_OUTPUT: name=%s rule=%s differ=%s verdict=%s" % (
            json.dumps(name), rn, fields, verdict))
    if counts["lines"] == 0 and counts["v2"] == 0:
        verdict, rc = "NO_RULES", 4
    elif counts["v2"] > 0 or counts["unsupported"] > 0:
        verdict, rc = "NOT_COMPARED", 5
    elif differ > 0:
        verdict, rc = "DIFFER", 1
    elif matched == 0:
        verdict, rc = "NO_MATCHING_MONITOR", 3
    else:
        verdict, rc = "OK", 0
    out.append("MADO_MONITORS: lines=%d rules=%d v2=%d unsupported=%d badrules=%d outputs=%d matched=%d "
               "unruled=%d agree=%d differ=%d disabled=%d verdict=%s" % (
                   counts["lines"], counts["adds"], counts["v2"], counts["unsupported"], counts["badrules"],
                   len(dump), matched, unruled, agree, differ, disabled, verdict))
    return out, rc


def parse_dump(data):
    if len(data) > MAX_BYTES:
        raise SetupError("too_large")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        raise SetupError("bad_json")
    try:
        dump = json.loads(text)
    except ValueError:
        raise SetupError("bad_json")
    if not isinstance(dump, list):
        raise SetupError("bad_json")
    for elem in dump:
        if not isinstance(elem, dict):
            raise SetupError("bad_json")
    return dump


def evaluate(mon_data, config_texts):
    dump = parse_dump(mon_data)
    rules, counts = parse_configs(config_texts)
    return build_report(rules, counts, dump)


# ---------------------------------------------------------------- selftest

CHECKS = []


def check(label, cond):
    CHECKS.append((label, bool(cond)))


def selftest():
    H = '{"name": "DP-1", "description": "Dell Inc. ABC123 0x0001", "width": 3440, "height": 1440, ' \
        '"refreshRate": 99.997, "x": 0, "y": 0, "scale": 1.0, "transform": 0, "disabled": false, ' \
        '"mirrorOf": "none", "id": 0}'

    def run(cfg, dump=None):
        return evaluate((dump if dump is not None else "[" + H + "]").encode(), [cfg])

    lines, rc = run("monitor = DP-1, 3440x1440@100, 0x0, 1\n")
    check("host ok rc", rc == 0)
    check("host rule line", lines[0] == 'MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 '
                                      'scale=1.0000 transform=0 mirror=- disabled=false')
    check("host agree", lines[1] == 'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE')
    check("host summary", lines[2] == "MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 "
                                      "matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK")

    check("no-rate defaults to 60", parse_mode("3440x1440") == ("mode", 3440, 1440, 60.0))
    check("rate parsed", parse_mode("3440x1440@100") == ("mode", 3440, 1440, 100.0))
    check("rate fraction", abs(parse_mode("3440x1440@99.997")[3] - 99.997) < 1e-5)
    check("rate 3-digit cap", parse_mode("3440x1440@1000") is None)
    check("mode junk unsupported", parse_mode("3440x1440@100Hz") is None)
    check("preferred keyword", parse_mode("preferred") == ("preferred",))
    check("empty mode is preferred", parse_mode("") == ("preferred",))
    check("pref prefix", parse_mode("pref") == ("preferred",))
    check("highrr keyword", parse_mode("highrr") == ("highrr",))
    check("highres keyword", parse_mode("highres") == ("highres",))
    check("maxwidth keyword", parse_mode("maxwidth") == ("maxwidth",))
    check("modeline any case", parse_mode("MODELINE 173.00 1920") == ("modeline",))
    check("pos auto", parse_pos("auto-left") == ("auto",))
    check("pos empty auto", parse_pos("") == ("auto",))
    check("pos negative", parse_pos("-1920x0") == ("xy", -1920, 0))
    check("pos junk", parse_pos("0x") is None)
    check("scale auto", parse_scale("auto") == ("auto",))
    check("scale 1.25", parse_scale("1.25") == ("num", 1.25))
    check("scale tiny becomes 1", parse_scale("0.2") == ("num", 1.0))
    check("scale 3 digits rejected", parse_scale("1.25") is not None and parse_scale("123") is None)
    check("scale 7 decimals rejected", parse_scale("1.1234567") is None)

    # mode closeness bound: |live - rate| < 1, exactly 1 fails.
    check("rate 0.997 off agrees", compare({"mode": ("mode", 3440, 1440, 100.0), "pos": ("auto",),
                                            "scale": ("auto",), "transform": 0, "mirror": None, "disabled": False},
                                           {"width": 3440, "height": 1440, "refreshRate": 99.003,
                                            "x": 0, "y": 0, "scale": 1, "transform": 0,
                                            "mirrorOf": "none", "id": 0}, []) == [])
    check("rate exactly 1 off fails", compare({"mode": ("mode", 3440, 1440, 100.0), "pos": ("auto",),
                                               "scale": ("auto",), "transform": 0, "mirror": None,
                                               "disabled": False},
                                              {"width": 3440, "height": 1440, "refreshRate": 99.0,
                                               "x": 0, "y": 0, "scale": 1, "transform": 0,
                                               "mirrorOf": "none", "id": 0}, []) == ["mode"])
    # bools are never numbers / integers.
    check("bool transform rejected", compare({"mode": ("preferred",), "pos": ("auto",), "scale": ("auto",),
                                              "transform": 0, "mirror": None, "disabled": False},
                                             {"width": 1, "height": 1, "refreshRate": 60, "x": 0, "y": 0,
                                              "scale": 1, "transform": True, "mirrorOf": "none", "id": 0},
                                             []) == ["transform"])

    # 1/120 correction: 1.3 on 3440x1440 lands on 4/3.
    check("scale correction 1.3", abs(expected_scale(1.3, 3440, 1440) - 4.0 / 3.0) < 1e-9)
    check("scale exact 1.5", expected_scale(1.5, 2880, 1920) == 1.5)
    check("scale K/120 branch", expected_scale(f32(1.6), 2880, 1920) == 1.6)
    check("scale no divisor is None", expected_scale(2.0, 3440, 1441) is None)
    check("scale None is not compared", compare({"mode": ("preferred",), "pos": ("auto",),
                                                 "scale": ("num", 2.0), "transform": 0, "mirror": None,
                                                 "disabled": False},
                                                {"width": 3440, "height": 1441, "refreshRate": 60, "x": 0,
                                                 "y": 0, "scale": 1.37, "transform": 0,
                                                 "mirrorOf": "none", "id": 0}, []) == [])
    check("scale tolerance", compare({"mode": ("preferred",), "pos": ("auto",), "scale": ("num", 1.25),
                                      "transform": 0, "mirror": None, "disabled": False},
                                     {"width": 2560, "height": 1440, "refreshRate": 60, "x": 0, "y": 0,
                                      "scale": 1.25005, "transform": 0, "mirrorOf": "none", "id": 0}, []) == [])
    check("scale mismatch fails", compare({"mode": ("preferred",), "pos": ("auto",), "scale": ("num", 1.3),
                                           "transform": 0, "mirror": None, "disabled": False},
                                          {"width": 3440, "height": 1440, "refreshRate": 60, "x": 0, "y": 0,
                                           "scale": 1.3, "transform": 0, "mirrorOf": "none", "id": 0},
                                          []) == ["scale"])

    # rule storage: add erases the same selector and appends.
    lines, _ = run("monitor = A, 1920x1080@60, 0x0, 1\nmonitor = A, 3440x1440@100, 0x0, 1\n")
    check("same selector erases", lines[0].startswith("MADO_MON_RULE: n=1 sel=\"A\" mode=3440x1440@100.00"))
    check("same selector rule count", "rules=1" in lines[-1])
    lines, _ = run("monitor = A, transform, 1\n")
    check("transform modifier alone adds nothing", lines[0].startswith("MADO_MON_OUTPUT") and "rules=0" in lines[-1])
    lines, rc = run("monitor = A, transform, 9\n")
    check("transform modifier bad value", "badrules=1" in lines[-1] and rc == 3)
    lines, _ = run("monitor = A, 1920x1080@60, 0x0, 1\nmonitor = A, transform, 3\n")
    check("transform modifier copies", "transform=3" in lines[0] and "rules=1" in lines[-1])
    lines, _ = run("monitor = A, addreserved, 10, 0, 0, 0\n")
    check("addreserved adds default", lines[0].endswith("mirror=- disabled=false") and "rules=1" in lines[-1])
    lines, _ = run("monitor = A, addreserved, x, 0, 0, 0\n")
    check("addreserved bad field", "badrules=1" in lines[-1] and "rules=0" in lines[-1])
    lines, _ = run("monitor = A, 1920x1080@60, 0x0, 1\nmonitor = A, addreserved, 10, 0, 0, 0\n")
    check("addreserved keeps rule", "rules=1" in lines[-1] and "mode=1920x1080@60.00" in lines[0])
    lines, _ = run("monitor = A, 1920x1080@60, 0x0, 1, wat, 1\n")
    check("unknown key drops rule", "badrules=1" in lines[-1] and "rules=0" in lines[-1])
    lines, _ = run("monitor = A, 1920x1080@60, 0x0, 1, sdr_eotf, 2\n")
    check("sdr_eotf is an unknown key", "badrules=1" in lines[-1])
    lines, _ = run("monitor = A, 1920x1080@60, 0x0, 1, bitdepth, 10, vrr, 1, cm, hdr\n")
    check("ignored keys consume", "rules=1" in lines[-1] and "badrules=0" in lines[-1])
    lines, _ = run("monitor = A, 1920x1080@60, 0x0, 1, transform, 9\n")
    check("transform key bad is unsupported", "unsupported=1" in lines[-1] and "badrules=0" in lines[-1])
    lines, rc = run("monitor = $main, 1920x1080@60, 0x0, 1\n")
    check("variable unsupported", "unsupported=1" in lines[-1] and rc == 5)
    lines, rc = run("monitor = A, 1920x1080@60, 0x0, 1 ## c\n")
    check("double hash unsupported", "unsupported=1" in lines[-1] and rc == 5)
    lines, rc = run("monitorv2 {\n  output = A\n}\nmonitor = A, 1920x1080@60, 0x0, 1\n")
    check("monitorv2 not compared", "v2=1" in lines[-1] and rc == 5)
    lines, rc = run("general {\n  gaps_in = 5\n}\n")
    check("no rules", rc == 4 and "verdict=NO_RULES" in lines[-1])
    lines, rc = run("# monitor = DP-1, 1x1, 0x0, 1\nmonitor = DP-1, 3440x1440@100, 0x0, 1 # main\n")
    check("comments cut", "lines=1" in lines[-1] and rc == 0)

    # selectors and fallback.
    two = ('[{"name": "A", "description": "D 0x01", "width": 1920, "height": 1080, "refreshRate": 60.0, '
           '"x": 0, "y": 0, "scale": 1, "transform": 0, "disabled": false, "mirrorOf": "none", "id": 4},'
           '{"name": "B", "description": "X D", "width": 1920, "height": 1080, "refreshRate": 60.0, '
           '"x": 0, "y": 0, "scale": 1, "transform": 0, "disabled": false, "mirrorOf": "4", "id": 5}]')
    lines, _ = evaluate(two.encode(), ["monitor = A, 1920x1080@60, 0x0, 1\nmonitor = desc:D, 1920x1080@60, 0x0, 1\n"])
    check("desc prefix matches", 'rule=2 differ=- verdict=AGREE' in lines[2])
    check("desc not prefix unruled", 'name="B" rule=- differ=- verdict=UNRULED' in lines[3])
    lines, _ = evaluate(two.encode(), ["monitor = , preferred, auto, auto\nmonitor = A, 1920x1080@60, 0x0, 1\n"])
    check("empty fallback first rule", 'name="B" rule=1' in lines[3])
    lines, _ = evaluate(two.encode(), ["monitor = , preferred, auto, auto\nmonitor = , highres, auto, auto\n"])
    check("empty fallback is first such rule", len(lines) == 4 and 'rule=1' in lines[1] and 'rule=1' in lines[2])

    # disabled / mirror / verdict order.
    lines, rc = run("monitor = DP-1, disable\n", '[{"name": "DP-1", "disabled": true, "mirrorOf": "none"}]')
    check("disabled agree", "verdict=DISABLED" in lines[1] and rc == 0)
    lines, rc = run("monitor = DP-1, disabled\n", '[{"name": "DP-1", "disabled": false}]')
    check("disabled but live", "differ=disabled" in lines[1] and rc == 1)
    lines, rc = run("monitor = DP-1, 3440x1440@100, 0x0, 1\n",
                    '[{"name": "DP-1", "width": 3440, "height": 1440, "refreshRate": 100.0, "x": 0, "y": 0, '
                    '"scale": 1, "transform": 0, "disabled": true, "mirrorOf": "none"}]')
    check("live disabled", "differ=disabled" in lines[1] and rc == 1)
    lines, _ = evaluate(two.encode(), ["monitor = B, 1920x1080@60, 0x0, 1, mirror, A\n"])
    check("mirror agrees on id", 'name="B" rule=1 differ=- verdict=AGREE' in lines[2])
    lines, _ = evaluate(two.encode(), ["monitor = A, 1920x1080@60, 0x0, 1, mirror, B\n"])
    check("mirror id mismatch", "differ=mirror" in lines[1])
    lines, rc = evaluate('[{"name": "A", "desc": 1}]'.encode(), ["monitor = Z, 1920x1080@60, 0x0, 1\n"])
    check("no matching monitor", rc == 3 and "verdict=NO_MATCHING_MONITOR" in lines[-1])
    check("no-rate differ", run("monitor = DP-1, 3440x1440, 0x0, 1\n")[0][1].find("differ=mode") > 0)
    check("differ exit 1", run("monitor = DP-1, 3440x1440, 0x0, 1\n")[1] == 1)
    check("modeline rule printed", run("monitor = DP-1, modeline 173.00 3440\n")[0][0].find("mode=modeline") > 0)

    # setup reasons.
    for raw, reason in ((b'[{"name": ', "bad_json"), (b'[1, 2]', "bad_json"), (b'{"a": 1}', "bad_json"),
                        (b'\xff\xfe', "bad_json")):
        try:
            parse_dump(raw)
            check("setup %s" % reason, False)
        except SetupError as e:
            check("setup %s" % reason, str(e) == reason)
    check("dump objects only", isinstance(parse_dump(b"[]"), list))

    total = len(CHECKS)
    failed = [label for label, ok in CHECKS if not ok]
    if failed:
        sys.stderr.write("selftest failures: %s\n" % ", ".join(failed))
        print("MADO_MONITORS_SELFTEST: %d/%d passed" % (total - len(failed), total))
        return 1
    print("MADO_MONITORS_SELFTEST: %d/%d passed" % (total, total))
    return 0


# ---------------------------------------------------------------- io


def read_input(path):
    if path == "-":
        data = sys.stdin.buffer.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise SetupError("too_large")
        return data
    try:
        st = os.stat(path)
    except OSError:
        raise SetupError("unreadable")
    if not stat.S_ISREG(st.st_mode):
        raise SetupError("unreadable")
    if st.st_size > MAX_BYTES:
        raise SetupError("too_large")
    try:
        with open(path, "rb") as f:
            data = f.read(MAX_BYTES + 1)
    except OSError:
        raise SetupError("unreadable")
    if len(data) > MAX_BYTES:
        raise SetupError("too_large")
    return data


def parse_args(argv):
    if argv == ["--selftest"]:
        return None, None
    monitors = None
    configs = []
    i = 0
    while i < len(argv):
        tok = argv[i]
        if tok == "--monitors" and monitors is None and i + 1 < len(argv):
            monitors = argv[i + 1]
        elif tok == "--config" and i + 1 < len(argv):
            configs.append(argv[i + 1])
        else:
            raise SetupError("usage")
        i += 2
    if monitors is None or not configs:
        raise SetupError("usage")
    return monitors, configs


def main(argv):
    try:
        monitors, configs = parse_args(argv)
    except SetupError as e:
        print("MADO_MONITORS: SETUP %s" % e)
        return 2
    if monitors is None:
        return selftest()
    try:
        mon_data = read_input(monitors)
        texts = []
        for path in configs:
            texts.append(read_input(path).decode("utf-8", "replace"))
        dump = parse_dump(mon_data)
    except SetupError as e:
        print("MADO_MONITORS: SETUP %s" % e)
        return 2
    rules, counts = parse_configs(texts)
    lines, rc = build_report(rules, counts, dump)
    sys.stdout.write("".join(line + "\n" for line in lines))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

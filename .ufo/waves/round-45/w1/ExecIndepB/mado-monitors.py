#!/usr/bin/env python3
"""mado-monitors - join Hyprland monitor rules with one live `hyprctl monitors all -j` dump.

Reads files and standard input only: it starts no process and opens no socket.
Written against the frozen round-45 contract (docstring of l1-draft/mado-monitors.py):
`monitor = NAME, MODE, POSITION, SCALE[, KEY, VALUE]...` lines are collected into a rule list
(one rule per selector, newest wins, empty-selector fallback, `desc:` prefix match) and joined
with the live outputs of one hyprctl dump.
"""
import json
import math
import os
import re
import stat
import struct
import sys

MAX_BYTES = 1048576

LINE_PAT = re.compile(r"monitor[ \t]*=(.*)")
TOKEN_SPLIT = re.compile(r"[ \t={]")
MODE_PAT = re.compile(r"([0-9]{1,5})x([0-9]{1,5})(?:@([0-9]{1,3}(?:\.[0-9]{1,3})?))?")
POS_PAT = re.compile(r"(-?[0-9]{1,6})x(-?[0-9]{1,6})")
SCALE_PAT = re.compile(r"[0-9]{1,2}(?:\.[0-9]{1,6})?")
RESERVED_PAT = re.compile(r"-?[0-9]{1,6}")

MODE_KEYWORDS = ("highrr", "highres", "maxwidth")
TRANSFORM_CHARS = "01234567"
DEFAULT_RATE = 60.0
RATE_TOL = 1.0
SCALE_TOL = 0.0001
SCALE_STEPS = 89


class Fault(Exception):
    """Setup failure; the argument is the reason word."""


class Reject(Exception):
    """A monitor line that is not modelled ('unmodelled') or invalid ('badrule')."""


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


# ---------------------------------------------------------------- input

def read_file(path):
    """Raw bytes of the regular file PATH; Fault(unreadable|too_large)."""
    try:
        info = os.stat(path)
    except OSError:
        raise Fault("unreadable")
    if not stat.S_ISREG(info.st_mode):
        raise Fault("unreadable")
    if info.st_size > MAX_BYTES:
        raise Fault("too_large")
    try:
        with open(path, "rb") as handle:
            data = handle.read(MAX_BYTES + 1)
    except OSError:
        raise Fault("unreadable")
    if len(data) > MAX_BYTES:
        raise Fault("too_large")
    return data


def slurp(path):
    """Raw bytes of PATH; '-' is standard input only for the monitors dump."""
    if path == "-":
        data = sys.stdin.buffer.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise Fault("too_large")
        return data
    return read_file(path)


def load_dump(raw):
    try:
        doc = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        raise Fault("bad_json")
    if not isinstance(doc, list):
        raise Fault("bad_json")
    for item in doc:
        if not isinstance(item, dict):
            raise Fault("bad_json")
    return doc


# ---------------------------------------------------------------- rule model

class Rule(object):
    """One monitor rule. `off` is the disabled form; `mode` is explicit|preferred|<keyword>."""

    __slots__ = ("sel", "off", "mode", "w", "h", "hz", "pos", "scale", "rot", "mirror")

    def __init__(self, sel):
        self.sel = sel
        self.off = False
        self.mode = "preferred"
        self.w = 0
        self.h = 0
        self.hz = DEFAULT_RATE
        self.pos = None
        self.scale = None
        self.rot = 0
        self.mirror = ""

    def clone(self):
        twin = Rule(self.sel)
        for slot in Rule.__slots__:
            setattr(twin, slot, getattr(self, slot))
        return twin


def field(fields, i):
    return fields[i] if i < len(fields) else ""


def publish(rules, rule):
    """Adding a rule erases every earlier rule with the same selector and appends the new one."""
    kept = [r for r in rules if r.sel != rule.sel]
    kept.append(rule)
    rules[:] = kept


def read_mode(text):
    if text == "" or text.startswith("pref"):
        return ("preferred", 0, 0, DEFAULT_RATE)
    for word in MODE_KEYWORDS:
        if text.startswith(word):
            return (word, 0, 0, DEFAULT_RATE)
    if text.split(None, 1)[0].lower() == "modeline":
        return ("modeline", 0, 0, DEFAULT_RATE)
    hit = MODE_PAT.fullmatch(text)
    if hit is None:
        raise Reject("unmodelled")
    rate = f32(float(hit.group(3))) if hit.group(3) else DEFAULT_RATE
    return ("explicit", int(hit.group(1)), int(hit.group(2)), rate)


def read_pos(text):
    if text == "" or text.startswith("auto"):
        return None
    hit = POS_PAT.fullmatch(text)
    if hit is None:
        raise Reject("unmodelled")
    return (int(hit.group(1)), int(hit.group(2)))


def read_scale(text):
    if text == "" or text.startswith("auto"):
        return None
    if SCALE_PAT.fullmatch(text) is None:
        raise Reject("unmodelled")
    value = f32(float(text))
    return 1.0 if value < 0.25 else value


def one_digit(text):
    return int(text) if len(text) == 1 and text in TRANSFORM_CHARS else None


def put_rot(rule, text):
    value = one_digit(text)
    if value is None:
        raise Reject("unmodelled")
    rule.rot = value


def put_mirror(rule, text):
    rule.mirror = text


def put_nothing(rule, text):
    return None


# KEY -> (consumes a value, setter). Unknown keys are not in this table.
VALUE_KEYS = {
    "mirror": put_mirror,
    "bitdepth": put_nothing,
    "cm": put_nothing,
    "sdrsaturation": put_nothing,
    "sdrbrightness": put_nothing,
    "transform": put_rot,
    "vrr": put_nothing,
    "icc": put_nothing,
}


# ---------------------------------------------------------------- grammar

def fields_of(body):
    if "##" in body or "$" in body or "\\" in body:
        raise Reject("unmodelled")
    head = body.split("#", 1)[0]
    return [part.strip(" \t") for part in head.split(",")]


def take_disable(fields, sel, rules, tally):
    rule = Rule(sel)
    rule.off = True
    publish(rules, rule)


def take_transform(fields, sel, rules, tally):
    rot = one_digit(field(fields, 2))
    if rot is None:
        tally["badrules"] += 1
        return
    for rule in rules:
        if rule.sel == sel:
            copy = rule.clone()
            copy.rot = rot
            publish(rules, copy)
            return


def take_reserved(fields, sel, rules, tally):
    if not all(RESERVED_PAT.fullmatch(field(fields, i)) for i in (2, 3, 4, 5)):
        tally["badrules"] += 1
        return
    if any(rule.sel == sel for rule in rules):
        return
    publish(rules, Rule(sel))


def take_normal(fields, sel, rules, tally):
    rule = Rule(sel)
    rule.mode, rule.w, rule.h, rule.hz = read_mode(field(fields, 1))
    rule.pos = read_pos(field(fields, 2))
    rule.scale = read_scale(field(fields, 3))
    i = 4
    while field(fields, i) != "":
        key = field(fields, i)
        setter = VALUE_KEYS.get(key)
        if setter is None:
            raise Reject("badrule")
        setter(rule, field(fields, i + 1))
        i += 2
    publish(rules, rule)


HEAD_HANDLERS = {
    "disable": take_disable,
    "disabled": take_disable,
    "transform": take_transform,
    "addreserved": take_reserved,
}


def take_line(body, rules, tally):
    try:
        fields = fields_of(body)
        sel = field(fields, 0)
        handler = HEAD_HANDLERS.get(field(fields, 1), take_normal)
        handler(fields, sel, rules, tally)
    except Reject as why:
        tally["unsupported" if str(why) == "unmodelled" else "badrules"] += 1


def scan_config(text, rules, tally):
    for raw in text.split("\n"):
        line = raw.strip(" \t")
        if TOKEN_SPLIT.split(line, 1)[0] == "monitorv2":
            tally["v2"] += 1
            continue
        hit = LINE_PAT.fullmatch(line)
        if hit is None:
            continue
        tally["lines"] += 1
        take_line(hit.group(1), rules, tally)


# ---------------------------------------------------------------- joining

def text_or_blank(record, key):
    value = record.get(key)
    return value if isinstance(value, str) else ""


def pick_rule(rules, mon):
    """Index of the output's effective rule, or None."""
    name = text_or_blank(mon, "name")
    desc = text_or_blank(mon, "description")
    for i in range(len(rules) - 1, -1, -1):
        sel = rules[i].sel
        if sel == "":
            continue
        if sel.startswith("desc:"):
            if desc.startswith(sel[5:].strip(" \t")):
                return i
        elif sel == name:
            return i
    for i, rule in enumerate(rules):
        if rule.sel == "":
            return i
    return None


def is_int(value):
    return type(value) is int


def is_number(value):
    return type(value) is int or type(value) is float


def divides(pixels, denom):
    if denom == 0.0:
        return False
    try:
        share = pixels / denom
    except OverflowError:
        return False
    if not math.isfinite(share):
        return False
    return share == int(share)


def close_enough(live, wanted, tolerance):
    try:
        return abs(live - wanted) < tolerance
    except OverflowError:
        return False


def expected_scale(declared, width, height):
    """Hyprland's 1/120 scale correction, in the order Monitor.cpp searches."""
    if divides(width, declared) and divides(height, declared):
        return declared
    base = math.floor(declared * 120.0 + 0.5)
    for step in range(SCALE_STEPS + 1):
        for hundredtwelfths in ((base,) if step == 0 else (base + step, base - step)):
            candidate = hundredtwelfths / 120.0
            if divides(width, candidate) and divides(height, candidate):
                return candidate
    return None


def mode_ok(rule, mon, mons):
    if rule.mode != "explicit":
        return True
    width, height, rate = mon.get("width"), mon.get("height"), mon.get("refreshRate")
    if not (is_int(width) and is_int(height) and is_number(rate)):
        return False
    return width == rule.w and height == rule.h and close_enough(rate, rule.hz, RATE_TOL)


def position_ok(rule, mon, mons):
    if rule.pos is None:
        return True
    x, y = mon.get("x"), mon.get("y")
    return is_int(x) and is_int(y) and (x, y) == rule.pos


def scale_ok(rule, mon, mons):
    if rule.scale is None:
        return True
    live = mon.get("scale")
    if not is_number(live):
        return False
    width, height = mon.get("width"), mon.get("height")
    if not (is_int(width) and is_int(height)):
        return False
    wanted = expected_scale(rule.scale, width, height)
    return wanted is None or close_enough(live, wanted, SCALE_TOL)


def transform_ok(rule, mon, mons):
    live = mon.get("transform")
    return is_int(live) and live == rule.rot


def mirror_ok(rule, mon, mons):
    live = mon.get("mirrorOf")
    if rule.mirror == "":
        return live == "none"
    if not isinstance(live, str):
        return False
    for other in mons:
        if text_or_blank(other, "name") == rule.mirror:
            ident = other.get("id")
            return is_int(ident) and live == str(ident)
    return False


# Compared in this order; a failure is named in the differ list.
CHECKS = (
    ("mode", mode_ok),
    ("position", position_ok),
    ("scale", scale_ok),
    ("transform", transform_ok),
    ("mirror", mirror_ok),
)


def judge(rule, mon, mons):
    live_off = mon.get("disabled") is True
    if rule.off:
        return ([], "DISABLED") if live_off else (["disabled"], "DIFFER")
    if live_off:
        return (["disabled"], "DIFFER")
    failed = [name for name, check in CHECKS if not check(rule, mon, mons)]
    return (failed, "DIFFER" if failed else "AGREE")


# ---------------------------------------------------------------- rendering

def quoted(text):
    return json.dumps(text)


def rule_line(number, rule):
    if rule.mode == "explicit":
        mode = "%dx%d@%.2f" % (rule.w, rule.h, rule.hz)
    else:
        mode = rule.mode
    pos = "auto" if rule.pos is None else "%dx%d" % rule.pos
    scale = "auto" if rule.scale is None else "%.4f" % rule.scale
    return "MADO_MON_RULE: n=%d sel=%s mode=%s pos=%s scale=%s transform=%d mirror=%s disabled=%s" % (
        number, quoted(rule.sel), mode, pos, scale, rule.rot,
        quoted(rule.mirror) if rule.mirror != "" else "-", "true" if rule.off else "false")


def output_line(mon, index, failed, verdict):
    return "MADO_MON_OUTPUT: name=%s rule=%s differ=%s verdict=%s" % (
        quoted(text_or_blank(mon, "name")),
        "-" if index is None else str(index + 1),
        ",".join(failed) if failed else "-", verdict)


def tally_line(tally, rules, sums, verdict):
    return ("MADO_MONITORS: lines=%d rules=%d v2=%d unsupported=%d badrules=%d outputs=%d matched=%d "
            "unruled=%d agree=%d differ=%d disabled=%d verdict=%s") % (
        tally["lines"], len(rules), tally["v2"], tally["unsupported"], tally["badrules"],
        sums["outputs"], sums["matched"], sums["unruled"], sums["agree"], sums["differ"],
        sums["disabled"], verdict)


def top_verdict(tally, sums):
    if tally["lines"] == 0 and tally["v2"] == 0:
        return ("NO_RULES", 4)
    if tally["v2"] > 0 or tally["unsupported"] > 0:
        return ("NOT_COMPARED", 5)
    if sums["differ"] > 0:
        return ("DIFFER", 1)
    if sums["matched"] == 0:
        return ("NO_MATCHING_MONITOR", 3)
    return ("OK", 0)


def report(dump, texts):
    tally = {"lines": 0, "v2": 0, "unsupported": 0, "badrules": 0}
    rules = []
    for text in texts:
        scan_config(text, rules, tally)
    out = [rule_line(n, rule) for n, rule in enumerate(rules, 1)]
    sums = {"outputs": 0, "matched": 0, "unruled": 0, "agree": 0, "differ": 0, "disabled": 0}
    for mon in dump:
        sums["outputs"] += 1
        index = pick_rule(rules, mon)
        if index is None:
            failed, verdict = [], "UNRULED"
        else:
            sums["matched"] += 1
            failed, verdict = judge(rules[index], mon, dump)
        sums[verdict.lower()] += 1
        out.append(output_line(mon, index, failed, verdict))
    verdict, code = top_verdict(tally, sums)
    out.append(tally_line(tally, rules, sums, verdict, ))
    return out, code


# ---------------------------------------------------------------- selftest

def live(name, w=3440, h=1440, hz=99.997, x=0, y=0, scale=1, rot=0, off=False, mirror="none",
         desc="", ident=0):
    return {"id": ident, "name": name, "description": desc, "width": w, "height": h,
            "refreshRate": hz, "x": x, "y": y, "scale": scale, "transform": rot,
            "disabled": off, "mirrorOf": mirror}


def reports(texts, dump):
    return report(load_dump(json.dumps(dump).encode("utf-8")), texts)


SELF_CASES = [
    ("agree", ["monitor = DP-1, 3440x1440@100, 0x0, 1\n"], [live("DP-1")],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK'], 0),
    ("no-rate-means-60", ["monitor = DP-1, 3440x1440, 0x0, 1\n"], [live("DP-1")],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@60.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=mode verdict=DIFFER',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER'], 1),
    ("no-rate-live-59.99", ["monitor = DP-1, 3440x1440, 0x0, 1\n"], [live("DP-1", hz=59.99)],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@60.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK'], 0),
    ("rate-exactly-one-off", ["monitor = DP-1, 3440x1440@100, 0x0, 1\n"], [live("DP-1", hz=99.0)],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=mode verdict=DIFFER',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER'], 1),
    ("rate-144", ["monitor = DP-1, 2560x1440@144, 0x0, 1\n"], [live("DP-1", w=2560, hz=143.912)],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=2560x1440@144.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK'], 0),
    ("resolution", ["monitor = DP-1, 2560x1440@100, 0x0, 1\n"], [live("DP-1")],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=2560x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=mode verdict=DIFFER',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER'], 1),
    ("position", ["monitor = DP-1, 3440x1440@100, -1920x0, 1\n"], [live("DP-1")],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=-1920x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=position verdict=DIFFER',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER'], 1),
    ("auto-position", ["monitor = DP-1, 3440x1440@100, auto-left, 1\n"], [live("DP-1", x=-3440)],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=auto scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK'], 0),
    ("fallback-preferred", ["monitor = , preferred, auto, auto\n"],
     [live("DP-1", w=1920, h=1080, hz=60.0, scale=1.25)],
     ['MADO_MON_RULE: n=1 sel="" mode=preferred pos=auto scale=auto transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK'], 0),
    ("scale-clean", ["monitor = DP-1, 2560x1440@60, 0x0, 1.25\n"],
     [live("DP-1", w=2560, hz=59.951, scale=1.25)],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=2560x1440@60.00 pos=0x0 scale=1.2500 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK'], 0),
    ("scale-1.6", ["monitor = DP-1, 2880x1920@120, 0x0, 1.6\n"],
     [live("DP-1", w=2880, h=1920, hz=120.0, scale=1.6)],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=2880x1920@120.00 pos=0x0 scale=1.6000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK'], 0),
    ("scale-1.3-corrected", ["monitor = DP-1, 3440x1440@100, 0x0, 1.3\n"],
     [live("DP-1", scale=1.33333333)],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.3000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK'], 0),
    ("scale-1.3-as-written", ["monitor = DP-1, 3440x1440@100, 0x0, 1.3\n"], [live("DP-1", scale=1.3)],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.3000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=scale verdict=DIFFER',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER'], 1),
    ("scale-below-a-quarter-is-1", ["monitor = DP-1, 3440x1440@100, 0x0, 0.2\n"], [live("DP-1")],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK'], 0),
    ("transform-key", ["monitor = DP-2, 1920x1080@60, 0x0, 1, transform, 1\n"],
     [live("DP-2", w=1920, h=1080, hz=60.0, rot=1)],
     ['MADO_MON_RULE: n=1 sel="DP-2" mode=1920x1080@60.00 pos=0x0 scale=1.0000 transform=1 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-2" rule=1 differ=- verdict=AGREE',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK'], 0),
    ("transform-unset", ["monitor = DP-2, 1920x1080@60, 0x0, 1\n"],
     [live("DP-2", w=1920, h=1080, hz=60.0, rot=1)],
     ['MADO_MON_RULE: n=1 sel="DP-2" mode=1920x1080@60.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-2" rule=1 differ=transform verdict=DIFFER',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER'], 1),
    ("transform-modifier", ["monitor = DP-2, 1920x1080@60, 0x0, 1\nmonitor = DP-2, transform, 3\n"],
     [live("DP-2", w=1920, h=1080, hz=60.0, rot=3)],
     ['MADO_MON_RULE: n=1 sel="DP-2" mode=1920x1080@60.00 pos=0x0 scale=1.0000 transform=3 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-2" rule=1 differ=- verdict=AGREE',
      'MADO_MONITORS: lines=2 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK'], 0),
    ("transform-modifier-alone", ["monitor = DP-2, transform, 1\n"], [live("DP-2")],
     ['MADO_MON_OUTPUT: name="DP-2" rule=- differ=- verdict=UNRULED',
      'MADO_MONITORS: lines=1 rules=0 v2=0 unsupported=0 badrules=0 outputs=1 matched=0 unruled=1 agree=0 differ=0 disabled=0 verdict=NO_MATCHING_MONITOR'], 3),
    ("transform-modifier-bad", ["monitor = DP-2, 1920x1080@60, 0x0, 1\nmonitor = DP-2, transform, 9\n"],
     [live("DP-2", w=1920, h=1080, hz=60.0)],
     ['MADO_MON_RULE: n=1 sel="DP-2" mode=1920x1080@60.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-2" rule=1 differ=- verdict=AGREE',
      'MADO_MONITORS: lines=2 rules=1 v2=0 unsupported=0 badrules=1 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK'], 0),
    ("same-selector-erases", ["monitor = DP-1, 1920x1080@60, 0x0, 1\nmonitor = DP-1, 3440x1440@100, 0x0, 1\n"],
     [live("DP-1")],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE',
      'MADO_MONITORS: lines=2 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK'], 0),
    ("desc-added-later-wins",
     ["monitor = DP-1, 1920x1080@60, 0x0, 1\nmonitor = desc:Dell Inc. U34, 3440x1440@100, 0x0, 1\n"],
     [live("DP-1", desc="Dell Inc. U3415W 0x0001")],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=1920x1080@60.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_RULE: n=2 sel="desc:Dell Inc. U34" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=2 differ=- verdict=AGREE',
      'MADO_MONITORS: lines=2 rules=2 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK'], 0),
    ("name-added-later-wins",
     ["monitor = desc:Dell Inc. U34, 3440x1440@100, 0x0, 1\nmonitor = DP-1, 1920x1080@60, 0x0, 1\n"],
     [live("DP-1", desc="Dell Inc. U3415W 0x0001")],
     ['MADO_MON_RULE: n=1 sel="desc:Dell Inc. U34" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_RULE: n=2 sel="DP-1" mode=1920x1080@60.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=2 differ=mode verdict=DIFFER',
      'MADO_MONITORS: lines=2 rules=2 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER'], 1),
    ("readd-moves-last",
     ["monitor = desc:Dell, 1920x1080@60, 0x0, 1\nmonitor = DP-1, 3440x1440@100, 0x0, 1\n"
      "monitor = desc:Dell, 2560x1440@144, 0x0, 1\n"],
     [live("DP-1", desc="Dell U34")],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_RULE: n=2 sel="desc:Dell" mode=2560x1440@144.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=2 differ=mode verdict=DIFFER',
      'MADO_MONITORS: lines=3 rules=2 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER'], 1),
    ("desc-not-a-prefix", ["monitor = desc:NotDell, 1920x1080@60, 0x0, 1\n"], [live("DP-1", desc="Dell U34")],
     ['MADO_MON_RULE: n=1 sel="desc:NotDell" mode=1920x1080@60.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=- differ=- verdict=UNRULED',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=0 unruled=1 agree=0 differ=0 disabled=0 verdict=NO_MATCHING_MONITOR'], 3),
    ("fallback-and-named",
     ["monitor = , preferred, auto, 1\nmonitor = HDMI-A-1, 1920x1080@60, 0x0, 1\n"],
     [live("DP-1"), live("HDMI-A-1", w=1920, h=1080, hz=60.0, x=3440, ident=1)],
     ['MADO_MON_RULE: n=1 sel="" mode=preferred pos=auto scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_RULE: n=2 sel="HDMI-A-1" mode=1920x1080@60.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE',
      'MADO_MON_OUTPUT: name="HDMI-A-1" rule=2 differ=position verdict=DIFFER',
      'MADO_MONITORS: lines=2 rules=2 v2=0 unsupported=0 badrules=0 outputs=2 matched=2 unruled=0 agree=1 differ=1 disabled=0 verdict=DIFFER'], 1),
    ("unruled-only", ["monitor = HDMI-A-1, 1920x1080@60, 0x0, 1\n"], [live("DP-1")],
     ['MADO_MON_RULE: n=1 sel="HDMI-A-1" mode=1920x1080@60.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=- differ=- verdict=UNRULED',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=0 unruled=1 agree=0 differ=0 disabled=0 verdict=NO_MATCHING_MONITOR'], 3),
    ("disabled-agree", ["monitor = DP-2, disable\n"], [live("DP-2", off=True)],
     ['MADO_MON_RULE: n=1 sel="DP-2" mode=preferred pos=auto scale=auto transform=0 mirror=- disabled=true',
      'MADO_MON_OUTPUT: name="DP-2" rule=1 differ=- verdict=DISABLED',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=0 disabled=1 verdict=OK'], 0),
    ("disabled-but-live", ["monitor = DP-2, disabled\n"], [live("DP-2")],
     ['MADO_MON_RULE: n=1 sel="DP-2" mode=preferred pos=auto scale=auto transform=0 mirror=- disabled=true',
      'MADO_MON_OUTPUT: name="DP-2" rule=1 differ=disabled verdict=DIFFER',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER'], 1),
    ("live-disabled", ["monitor = DP-2, 1920x1080@60, 0x0, 1\n"], [live("DP-2", w=1920, h=1080, hz=60.0, off=True)],
     ['MADO_MON_RULE: n=1 sel="DP-2" mode=1920x1080@60.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-2" rule=1 differ=disabled verdict=DIFFER',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER'], 1),
    ("mirror-agree",
     ["monitor = DP-1, 3440x1440@100, 0x0, 1\nmonitor = DP-2, 3440x1440@100, 0x0, 1, mirror, DP-1\n"],
     [live("DP-1", ident=4), live("DP-2", ident=5, mirror="4")],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_RULE: n=2 sel="DP-2" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror="DP-1" disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE',
      'MADO_MON_OUTPUT: name="DP-2" rule=2 differ=- verdict=AGREE',
      'MADO_MONITORS: lines=2 rules=2 v2=0 unsupported=0 badrules=0 outputs=2 matched=2 unruled=0 agree=2 differ=0 disabled=0 verdict=OK'], 0),
    ("mirror-missing", ["monitor = DP-2, 3440x1440@100, 0x0, 1, mirror, DP-1\n"],
     [live("DP-1", ident=4), live("DP-2", ident=5)],
     ['MADO_MON_RULE: n=1 sel="DP-2" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror="DP-1" disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=- differ=- verdict=UNRULED',
      'MADO_MON_OUTPUT: name="DP-2" rule=1 differ=mirror verdict=DIFFER',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=2 matched=1 unruled=1 agree=0 differ=1 disabled=0 verdict=DIFFER'], 1),
    ("unknown-key-drops-rule", ["monitor = DP-1, 3440x1440@100, 0x0, 1, wat, 1\n"], [live("DP-1")],
     ['MADO_MON_OUTPUT: name="DP-1" rule=- differ=- verdict=UNRULED',
      'MADO_MONITORS: lines=1 rules=0 v2=0 unsupported=0 badrules=1 outputs=1 matched=0 unruled=1 agree=0 differ=0 disabled=0 verdict=NO_MATCHING_MONITOR'], 3),
    ("ignored-keys", ["monitor = DP-1, 3440x1440@100, 0x0, 1, bitdepth, 10, vrr, 1, cm, hdr\n"], [live("DP-1")],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK'], 0),
    ("sdr-eotf-drops-rule", ["monitor = DP-1, 3440x1440@100, 0x0, 1, sdr_eotf, 2\n"], [live("DP-1")],
     ['MADO_MON_OUTPUT: name="DP-1" rule=- differ=- verdict=UNRULED',
      'MADO_MONITORS: lines=1 rules=0 v2=0 unsupported=0 badrules=1 outputs=1 matched=0 unruled=1 agree=0 differ=0 disabled=0 verdict=NO_MATCHING_MONITOR'], 3),
    ("monitorv2", ["monitorv2 {\n  output = DP-1\n}\nmonitor = DP-1, 3440x1440@100, 0x0, 1\n"], [live("DP-1")],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE',
      'MADO_MONITORS: lines=1 rules=1 v2=1 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=NOT_COMPARED'], 5),
    ("variable", ["monitor = $main, 3440x1440@100, 0x0, 1\n"], [live("DP-1")],
     ['MADO_MON_OUTPUT: name="DP-1" rule=- differ=- verdict=UNRULED',
      'MADO_MONITORS: lines=1 rules=0 v2=0 unsupported=1 badrules=0 outputs=1 matched=0 unruled=1 agree=0 differ=0 disabled=0 verdict=NOT_COMPARED'], 5),
    ("unsupported-rate-suffix", ["monitor = DP-1, 3440x1440@100Hz, 0x0, 1\n"], [live("DP-1")],
     ['MADO_MON_OUTPUT: name="DP-1" rule=- differ=- verdict=UNRULED',
      'MADO_MONITORS: lines=1 rules=0 v2=0 unsupported=1 badrules=0 outputs=1 matched=0 unruled=1 agree=0 differ=0 disabled=0 verdict=NOT_COMPARED'], 5),
    ("comments", ["# monitor = DP-1, 1x1, 0x0, 1\nmonitor = DP-1, 3440x1440@100, 0x0, 1 # main\n"], [live("DP-1")],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK'], 0),
    ("no-rules", ["general {\n    gaps_in = 5\n}\n"], [live("DP-1")],
     ['MADO_MON_OUTPUT: name="DP-1" rule=- differ=- verdict=UNRULED',
      'MADO_MONITORS: lines=0 rules=0 v2=0 unsupported=0 badrules=0 outputs=1 matched=0 unruled=1 agree=0 differ=0 disabled=0 verdict=NO_RULES'], 4),
    ("wrong-types", ["monitor = DP-1, 3440x1440@100, 0x0, 1\n"],
     [live("DP-1", x="0", rot=True)],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=position,transform verdict=DIFFER',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER'], 1),
    ("addreserved-adds-default", ["monitor = DP-1, addreserved, 10, 0, 0, 0\n"],
     [live("DP-1", x=50, scale=1.5)],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=preferred pos=auto scale=auto transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK'], 0),
    ("addreserved-keeps-rule", ["monitor = DP-1, 1920x1080@60, 0x0, 1\nmonitor = DP-1, addreserved, 10, 0, 0, 0\n"],
     [live("DP-1")],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=1920x1080@60.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=mode verdict=DIFFER',
      'MADO_MONITORS: lines=2 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER'], 1),
    ("two-files-later-overrides",
     ["monitor = DP-1, 1920x1080@60, 0x0, 1\n", "monitor = DP-1, 3440x1440@100, 0x0, 1\n"],
     [live("DP-1")],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE',
      'MADO_MONITORS: lines=2 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK'], 0),
    ("highres-not-compared", ["monitor = DP-1, highres, auto, auto\n"], [live("DP-1", w=1280, h=720, hz=30.0)],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=highres pos=auto scale=auto transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK'], 0),
    ("zero-sized-output-still-corrects", ["monitor = DP-1, 3440x1440@100, 0x0, 1.25\n"],
     [live("DP-1", w=0, h=0)],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.2500 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=mode,scale verdict=DIFFER',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER'], 1),
    ("integer-beyond-double-range", ["monitor = DP-1, 3440x1440@100, 0x0, 1.3\n"],
     [live("DP-1", w=10 ** 400)],
     ['MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.3000 transform=0 mirror=- disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=mode verdict=DIFFER',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER'], 1),
    ("mirror-target-first-entry", ["monitor = DP-2, 1x1@60, 0x0, 1, mirror, DP-1\n"],
     [live("DP-1", ident="x"), live("DP-1", ident=7),
      live("DP-2", w=1, h=1, hz=60.0, ident=3, mirror="7")],
     ['MADO_MON_RULE: n=1 sel="DP-2" mode=1x1@60.00 pos=0x0 scale=1.0000 transform=0 mirror="DP-1" disabled=false',
      'MADO_MON_OUTPUT: name="DP-1" rule=- differ=- verdict=UNRULED',
      'MADO_MON_OUTPUT: name="DP-1" rule=- differ=- verdict=UNRULED',
      'MADO_MON_OUTPUT: name="DP-2" rule=1 differ=mirror verdict=DIFFER',
      'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=3 matched=1 unruled=2 agree=0 differ=1 disabled=0 verdict=DIFFER'], 1),
]


def selftest():
    import tempfile
    import shutil
    ok = 0
    total = 0
    for label, texts, dump, want, want_code in SELF_CASES:
        total += 1
        try:
            got, code = reports(texts, dump)
        except Exception as why:  # noqa: BLE001 - a selftest case must never abort the run
            print("selftest %s raised %r" % (label, why), file=sys.stderr)
            continue
        if got == want and code == want_code:
            ok += 1
        else:
            print("selftest %s: code=%d want=%d lines=%r" % (label, code, want_code, got), file=sys.stderr)

    # Setup paths through the command line, on files in a throw-away directory.
    room = tempfile.mkdtemp(prefix="mado-monitors-selftest-")
    try:
        good_dump = "%s/dump.json" % room
        with open(good_dump, "w") as handle:
            handle.write(json.dumps([live("DP-1")]))
        conf = "%s/monitors.conf" % room
        with open(conf, "w") as handle:
            handle.write("monitor = DP-1, 3440x1440@100, 0x0, 1\n")
        junk = "%s/junk.json" % room
        with open(junk, "w") as handle:
            handle.write('[1, 2]')
        big = "%s/big.json" % room
        with open(big, "wb") as handle:
            handle.write(b" " * (MAX_BYTES + 1))
        setups = [
            ("usage", ["--monitors", good_dump], "usage"),
            ("usage-dupe", ["--monitors", good_dump, "--monitors", good_dump, "--config", conf], "usage"),
            ("unreadable", ["--monitors", "%s/nope.json" % room, "--config", conf], "unreadable"),
            ("config-dir", ["--monitors", good_dump, "--config", room], "unreadable"),
            ("too-large", ["--monitors", big, "--config", conf], "too_large"),
            ("bad-json", ["--monitors", junk, "--config", conf], "bad_json"),
        ]
        for label, argv, reason in setups:
            total += 1
            try:
                got = run(argv)
            except Fault as why:
                got = (["MADO_MONITORS: SETUP %s" % why], 2)
            if got == (["MADO_MONITORS: SETUP %s" % reason], 2):
                ok += 1
            else:
                print("selftest %s: %r" % (label, got), file=sys.stderr)
        # `-` is not standard input for --config: it is a path that does not exist in a fresh dir.
        total += 1
        here = None
        try:
            here = os.getcwd()
        except OSError:
            pass
        try:
            if here is not None:
                os.chdir(room)
            got = run(["--monitors", good_dump, "--config", "-"])
        except Fault as why:
            got = (["MADO_MONITORS: SETUP %s" % why], 2)
        finally:
            if here is not None:
                os.chdir(here)
        if got == (["MADO_MONITORS: SETUP unreadable"], 2):
            ok += 1
        else:
            print("selftest config-dash: %r" % (got,), file=sys.stderr)
        total += 1
        got = run(["--monitors", good_dump, "--config", conf])
        if got == (['MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 '
                     'transform=0 mirror=- disabled=false',
                     'MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE',
                     'MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 '
                     'unruled=0 agree=1 differ=0 disabled=0 verdict=OK'], 0):
            ok += 1
        else:
            print("selftest cli: %r" % (got,), file=sys.stderr)
    finally:
        shutil.rmtree(room, ignore_errors=True)
    print("MADO_MONITORS_SELFTEST: %d/%d passed" % (ok, total))
    return 0 if ok == total else 1


# ---------------------------------------------------------------- command line

def plan(argv):
    """('selftest', None, None) or ('run', dump_path, [config paths])."""
    if argv == ["--selftest"]:
        return ("selftest", None, None)
    dump, configs, i = None, [], 0
    while i < len(argv):
        flag = argv[i]
        if i + 1 >= len(argv) or flag not in ("--monitors", "--config"):
            raise Fault("usage")
        if flag == "--monitors":
            if dump is not None:
                raise Fault("usage")
            dump = argv[i + 1]
        else:
            configs.append(argv[i + 1])
        i += 2
    if dump is None or not configs:
        raise Fault("usage")
    return ("run", dump, configs)


def run(argv):
    """(output lines, exit code) - Fault is left to the caller."""
    what, dump, configs = plan(argv)
    if what == "selftest":
        return (None, selftest())
    parsed = load_dump(slurp(dump))
    texts = [read_file(path).decode("utf-8", "replace") for path in configs]
    return report(parsed, texts)


def main():
    try:
        lines, code = run(sys.argv[1:])
    except Fault as why:
        sys.stdout.write("MADO_MONITORS: SETUP %s\n" % why)
        return 2
    if lines is not None:
        sys.stdout.write("".join(line + "\n" for line in lines))
    return code


if __name__ == "__main__":
    sys.exit(main())

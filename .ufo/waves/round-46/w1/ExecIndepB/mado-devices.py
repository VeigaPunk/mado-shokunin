#!/usr/bin/env python3
"""mado-devices - join Hyprland input/device config lines with one `hyprctl devices -j` dump.

Second independent implementation of the round-46 C1 contract (PRED-C1-r46). The architecture is a
three-stage pipeline: a lexer turns config text into logical lines (continuation join, blank trim,
comment cut, directive spotting), a tokenizer classifies each logical line (open / close / assign),
and a state machine consumes the tokens, keeping the category stack, the selected device, the
unmodelled-line counter and the per-device key store. Rendering then joins that store with the dump.

Contract summary (full wording is the L1 draft docstring):
  * inputs: one devices JSON (file or `-`) plus one or more config files; read-only, no process, no socket
  * setup errors: `MADO_DEVICES: SETUP <usage|unreadable|too_large|bad_json>`, exit 2
  * keyboards: expected XKB names (device block wins over the global input: value, else us/empty) vs the
    printed rules -> AGREE / DIFFER / FALLBACK / VIRTUAL
  * mice: expected scroll_factor (block value clamped 0..100, else -1) vs printed scrollFactor
  * device blocks: MATCHED / NO_SUCH_DEVICE
  * verdict: NOT_COMPARED 5 | DIFFER 1 | NO_KEYBOARDS 3 | STALE_BLOCK 4 | OK 0
"""
import json
import math
import os
import re
import stat
import struct
import sys

MAX_BYTES = 1048576
TRIM = " \t\r"
BLANK = " \t\r\n\v\f"
REPORTED = ("layout", "variant", "options", "model", "rules")
DEVICE_KEYS = ("kb_layout", "kb_variant", "kb_options", "kb_model", "kb_rules", "kb_file", "scroll_factor")
GLOBALS = frozenset("input:kb_" + n for n in ("layout", "variant", "options", "model", "rules", "file"))
EMPTY_MARK = "[[EMPTY]]"
VIRTUAL = "hl-virtual-keyboard"
FLOAT_RE = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")
SPECIAL_RE = re.compile(r"[+-]?(?:inf|nan|0x)", re.I)
DIRECTIVE_RE = re.compile(r"#[ \t]*hyprlang\b")
MIN_NORMAL = 2.0 ** -126

FRESH, BOUND, BROKEN = 0, 1, 2


class Fail(Exception):
    """A setup failure carrying one contract reason word."""

    def __init__(self, reason):
        Exception.__init__(self, reason)
        self.reason = reason


# ---------------------------------------------------------------- input bytes

def bounded(reader):
    """Read at most MAX_BYTES+1 bytes; more than MAX_BYTES is too_large."""
    data = reader(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise Fail("too_large")
    return data


def read_path(path):
    if path == "-":
        return bounded(sys.stdin.buffer.read)
    try:
        info = os.stat(path)
    except OSError:
        raise Fail("unreadable")
    if not stat.S_ISREG(info.st_mode):
        raise Fail("unreadable")
    try:
        with open(path, "rb") as handle:
            return bounded(handle.read)
    except OSError:
        raise Fail("unreadable")


# --------------------------------------------------------------------- lexer

def raw_lines(text):
    """Join backslash continuations; drop a final dangling continuation line."""
    parts = text.split("\n")
    index = 0
    total = len(parts)
    while index < total:
        line = parts[index]
        dangling = False
        while line.endswith("\\"):
            if index + 1 >= total:
                dangling = True
                break
            index += 1
            line = line[:-1].rstrip(" \t") + parts[index]
        index += 1
        if not dangling:
            yield line


def cut_comment(line):
    """Remove a trailing comment; `##` yields one literal `#` and restarts the search."""
    text = line
    at = text.find("#")
    while at != -1:
        if at + 1 < len(text) and text[at + 1] == "#":
            text = text[:at] + text[at + 1:]
            at = text.find("#", at + 2)
        else:
            return text[:at]
    return text


def tokenize(text):
    """Yield ("directive",) | ("open", name) | ("close",) | ("assign", lhs, rhs)."""
    for line in raw_lines(text):
        line = line.strip(TRIM)
        if line.startswith("#"):
            if DIRECTIVE_RE.match(line):
                yield ("directive",)
            continue
        body = cut_comment(line).strip(BLANK)
        if not body:
            continue
        if "=" not in body:
            if body == "}":
                yield ("close",)
            elif body.endswith("{"):
                yield ("open", body[:-1].strip(BLANK))
            continue
        lhs, rhs = body.split("=", 1)
        yield ("assign", lhs.strip(BLANK), rhs.strip(BLANK))


# ------------------------------------------------------------------- machine

def decode_value(rhs):
    return "" if rhs == EMPTY_MARK else rhs


def to_float32(value):
    try:
        return struct.unpack("<f", struct.pack("<f", value))[0]
    except OverflowError:
        return math.inf if value > 0 else -math.inf


def read_factor(rhs, machine):
    """std::stof on a scroll_factor RHS: float32 value, or None when unset/unsupported."""
    if SPECIAL_RE.match(rhs):
        machine.unsupported += 1
        return None
    match = FLOAT_RE.match(rhs)
    if match is None:
        return None
    value = to_float32(float(match.group(0)))
    if math.isinf(value) or (value != 0.0 and abs(value) < MIN_NORMAL):
        machine.unsupported += 1
        return None
    return value


class Machine(object):
    def __init__(self):
        self.globals = {}
        self.blocks = {}
        self.status = FRESH
        self.current = None
        self.unsupported = 0
        self.stack = []

    def reset_scope(self):
        self.stack = []
        self.status = FRESH
        self.current = None

    def forget_device(self):
        self.status = BROKEN
        self.current = None

    def block(self, name):
        return self.blocks.setdefault(name, {})

    def feed(self, text):
        self.reset_scope()
        for token in tokenize(text):
            kind = token[0]
            if kind == "directive":
                self.unsupported += 1
            elif kind == "open":
                self.stack.append(token[1])
            elif kind == "close":
                if self.stack:
                    self.stack.pop()
                    if not self.stack:
                        self.reset_scope()
            else:
                self.assign(token[1], token[2])

    def store(self, block, field, rhs):
        if field == "scroll_factor":
            value = read_factor(rhs, self)
            if value is not None:
                block[field] = value
        else:
            block[field] = decode_value(rhs)

    def assign(self, lhs, rhs):
        if not lhs or lhs.startswith("$"):
            return
        key = ":".join(self.stack + [lhs]) if self.stack else lhs
        bracket = None
        left = key.find("[")
        right = key.rfind("]")
        if left != -1 and left < right:
            bracket = key[left + 1:right]
            key = key[:left] + key[right + 1:]
        if not (key.startswith("device") or key in GLOBALS):
            return
        if "$" in lhs or "$" in rhs or "{{" in lhs or "{{" in rhs or "\\" in lhs or "\\" in rhs:
            self.unsupported += 1
            return
        if key in GLOBALS:
            self.globals[key[6:]] = decode_value(rhs)
            return
        if not key.startswith("device:"):
            return
        field = key[7:]
        if bracket is not None:
            block = self.block(bracket)
            if field == "name":
                self.unsupported += 1
            elif field in DEVICE_KEYS:
                self.store(block, field, rhs)
            return
        if field == "name":
            if self.status == FRESH:
                self.block(rhs)
                self.current = rhs
                self.status = BOUND
            else:
                self.unsupported += 1
                self.forget_device()
            return
        if self.status == BOUND:
            if field in DEVICE_KEYS:
                self.store(self.blocks[self.current], field, rhs)
            return
        self.unsupported += 1
        self.status = BROKEN


# ------------------------------------------------------------------ dump/read

def parse_dump(raw):
    try:
        doc = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError, RecursionError):
        raise Fail("bad_json")
    if not isinstance(doc, dict):
        raise Fail("bad_json")
    for key in ("keyboards", "mice"):
        items = doc.get(key)
        if not isinstance(items, list):
            raise Fail("bad_json")
        for item in items:
            if not isinstance(item, dict) or not isinstance(item.get("name"), str):
                raise Fail("bad_json")
    return doc


def dump_names(doc):
    names = set()
    for value in doc.values():
        if not isinstance(value, list):
            continue
        for element in value:
            if not isinstance(element, dict):
                continue
            if isinstance(element.get("name"), str):
                names.add(element["name"])
            owner = element.get("belongsTo")
            if isinstance(owner, dict) and isinstance(owner.get("name"), str):
                names.add(owner["name"])
    return names


def is_number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def fmt(value):
    return "%.2f" % value


def jd(value):
    return json.dumps(value, ensure_ascii=True)


# ---------------------------------------------------------------------- render

def expected_names(machine, name):
    block = machine.blocks.get(name)
    out = []
    for field in REPORTED:
        key = "kb_" + field
        if block is not None and key in block:
            out.append(block[key])
        elif key in machine.globals:
            out.append(machine.globals[key])
        elif field == "layout":
            out.append("us")
        else:
            out.append("")
    if block is not None and "kb_file" in block:
        kb_file = block["kb_file"]
    else:
        kb_file = machine.globals.get("kb_file", "")
    return out, kb_file


def keyboard_line(machine, element, counter):
    name = element["name"]
    block = machine.blocks.get(name)
    expected, kb_file = expected_names(machine, name)
    reported = [element.get(field) for field in REPORTED]
    differ = [field for field, want, have in zip(REPORTED, expected, reported)
              if not (isinstance(have, str) and have == want)]
    if name.startswith(VIRTUAL):
        verdict = "VIRTUAL"
        counter["virtual"] += 1
    elif not differ:
        verdict = "AGREE"
        counter["agree"] += 1
    elif reported == ["us", "", "", "", ""]:
        verdict = "FALLBACK"
        counter["fallback"] += 1
    else:
        verdict = "DIFFER"
        counter["differ"] += 1
    return ("MADO_DEV_KEYBOARD: name=%s block=%s layout=%s variant=%s options=%s model=%s rules=%s "
            "kb_file=%s differ=%s verdict=%s" % (
                jd(name), "yes" if block is not None else "no", jd(expected[0]), jd(expected[1]),
                jd(expected[2]), jd(expected[3]), jd(expected[4]), "set" if kb_file else "-",
                ",".join(differ) if differ else "-", verdict))


def mouse_line(machine, element, counter):
    name = element["name"]
    block = machine.blocks.get(name)
    if block is not None and "scroll_factor" in block:
        expected = min(max(block["scroll_factor"], 0.0), 100.0)
    else:
        expected = -1.0
    reported = element.get("scrollFactor")
    if is_number(reported) and fmt(reported) == fmt(expected):
        verdict = "AGREE"
    else:
        verdict = "DIFFER"
        counter["mice_differ"] += 1
    return "MADO_DEV_MOUSE: name=%s block=%s scroll_factor=%s reported=%s verdict=%s" % (
        jd(name), "yes" if block is not None else "no", fmt(expected),
        fmt(reported) if is_number(reported) else "?", verdict)


def render(doc, machine):
    lines = []
    counter = {"agree": 0, "differ": 0, "fallback": 0, "virtual": 0, "mice_differ": 0}
    matched = dump_names(doc)
    for element in doc["keyboards"]:
        lines.append(keyboard_line(machine, element, counter))
    for element in doc["mice"]:
        lines.append(mouse_line(machine, element, counter))
    stale = 0
    for name, block in machine.blocks.items():
        ok = name in matched
        if not ok:
            stale += 1
        lines.append("MADO_DEV_BLOCK: name=%s keys=%d verdict=%s" % (
            jd(name), len(block), "MATCHED" if ok else "NO_SUCH_DEVICE"))
    keyboards = len(doc["keyboards"])
    if machine.unsupported > 0:
        verdict, code = "NOT_COMPARED", 5
    elif counter["differ"] + counter["fallback"] + counter["mice_differ"] > 0:
        verdict, code = "DIFFER", 1
    elif keyboards == 0:
        verdict, code = "NO_KEYBOARDS", 3
    elif stale > 0:
        verdict, code = "STALE_BLOCK", 4
    else:
        verdict, code = "OK", 0
    lines.append("MADO_DEVICES: keyboards=%d agree=%d differ=%d fallback=%d virtual=%d mice=%d "
                 "mice_differ=%d blocks=%d stale=%d unsupported=%d verdict=%s" % (
                     keyboards, counter["agree"], counter["differ"], counter["fallback"], counter["virtual"],
                     len(doc["mice"]), counter["mice_differ"], len(machine.blocks), stale,
                     machine.unsupported, verdict))
    return lines, code


# ------------------------------------------------------------------------ CLI

def parse_cli(argv):
    if argv == ["--selftest"]:
        return "selftest", None, []
    devices = None
    configs = []
    index = 0
    while index < len(argv):
        if index + 1 >= len(argv):
            raise Fail("usage")
        flag, value = argv[index], argv[index + 1]
        if flag == "--devices" and devices is None:
            devices = value
        elif flag == "--config":
            configs.append(value)
        else:
            raise Fail("usage")
        index += 2
    if devices is None or not configs:
        raise Fail("usage")
    return "run", devices, configs


def report(dump_bytes, texts):
    """Pure join: dump bytes plus decoded config texts -> (lines, exit code)."""
    try:
        doc = parse_dump(dump_bytes)
    except Fail as exc:
        return ["MADO_DEVICES: SETUP %s" % exc.reason], 2
    machine = Machine()
    for text in texts:
        machine.feed(text)
    return render(doc, machine)


def run(argv):
    try:
        mode, devices, configs = parse_cli(argv)
    except Fail as exc:
        return ["MADO_DEVICES: SETUP %s" % exc.reason], 2
    if mode == "selftest":
        return [], 0
    try:
        dump_bytes = read_path(devices)
        texts = [read_path(path).decode("utf-8", errors="replace") for path in configs]
    except Fail as exc:
        return ["MADO_DEVICES: SETUP %s" % exc.reason], 2
    return report(dump_bytes, texts)


# ------------------------------------------------------------------- selftest

def dump_of(layout="us", fields=None, mice=None, lists=None):
    """Build a dump dict for the selftest; `fields` overrides keyboard fields."""
    keyboard = {"address": "0x1", "name": "kbd", "rules": "", "model": "", "layout": layout,
                "variant": "", "options": ""}
    if fields:
        keyboard.update(fields)
    if mice is None:
        mice = [{"address": "0x2", "name": "mouse", "defaultSpeed": 0.0, "scrollFactor": -1.0}]
    doc = {"keyboards": [keyboard], "mice": mice}
    if lists:
        doc.update(lists)
    return json.dumps(doc).encode()


def selftest():
    checks = []

    def check(name, condition):
        checks.append((name, bool(condition)))

    def _feed(text):
        machine = Machine()
        machine.feed(text)
        return machine.globals, machine.blocks, machine.unsupported

    def out(dump, *texts):
        return report(dump, list(texts))

    def keys_of(lines):
        return [line for line in lines if line.startswith("MADO_DEV_BLOCK:")]

    # lexer ------------------------------------------------------------------
    check("lex-continuation-joins",
          list(raw_lines("a = b,\\\nc\n")) == ["a = b,c", ""])
    check("lex-continuation-drops-trailing-blanks",
          list(raw_lines("a  \t\\\nb\n"))[0] == "a" + "b")
    check("lex-continuation-final-line-dropped",
          list(raw_lines("a = b\\")) == [])
    check("lex-comment-pair-literal",
          cut_comment("x = a##b # c") == "x = a#b ")
    check("lex-comment-triple-hash",
          cut_comment("x = a###b") == "x = a##b")
    check("lex-directive-anywhere-after-hash-only-at-start",
          (list(tokenize("# hyprlang if X")) == [("directive",)]
           and list(tokenize("## hyprlang if X")) == []))
    check("lex-directive-inside-trailing-comment",
          list(tokenize("input:kb_layout = de # hyprlang")) == [("assign", "input:kb_layout", "de")])
    check("lex-crlf",
          list(tokenize("input {\r\nkb_layout = br\r\n}\r\n"))
          == [("open", "input"), ("assign", "kb_layout", "br"), ("close",)])
    check("lex-vt-ff-stripped",
          list(tokenize("input:kb_layout =\x0bbr\x0c")) == [("assign", "input:kb_layout", "br")])
    check("lex-inline-brace-line-not-modelled",
          _feed("input { kb_layout = de }") == ({}, {}, 0))

    # machine ----------------------------------------------------------------
    machine = Machine()
    machine.feed("input {\n kb_layout = br\n kb_options = a##b # tail\n}\n")
    check("machine-global-in-block",
          machine.globals == {"kb_layout": "br", "kb_options": "a#b"} and machine.unsupported == 0)
    machine = Machine()
    machine.feed("device[kbd]:kb_layout = fr\n")
    check("machine-bracket-flat", machine.blocks == {"kbd": {"kb_layout": "fr"}})
    machine = Machine()
    machine.feed("device[kbd] {\n kb_layout = fr\n kb_variant = azerty\n}\n")
    check("machine-bracket-block", machine.blocks == {"kbd": {"kb_layout": "fr", "kb_variant": "azerty"}})
    machine = Machine()
    machine.feed("device {\n name = kbd\n kb_layout = de\n}\n")
    check("machine-block-name-then-key", machine.blocks == {"kbd": {"kb_layout": "de"}} and machine.unsupported == 0)
    machine = Machine()
    machine.feed("device {\n kb_layout = de\n name = kbd\n}\n")
    check("machine-block-first-poisons",
          machine.blocks == {} and machine.unsupported == 2)
    machine = Machine()
    machine.feed("device {\n name = kbd\n name = other\n kb_layout = de\n}\n")
    check("machine-rename-poisons",
          machine.blocks == {"kbd": {}} and machine.unsupported == 2)
    machine = Machine()
    machine.feed("device {\n name = kbd\n sub {\n }\n kb_layout = de\n}\n")
    check("machine-nested-keeps-binding", machine.blocks == {"kbd": {"kb_layout": "de"}})
    machine = Machine()
    machine.feed("device {\n kb_layout = de\n sub {\n }\n kb_layout = fr\n}\n")
    check("machine-broken-survives-nested", machine.unsupported == 2 and machine.blocks == {})
    machine = Machine()
    machine.feed("device {\n kb_layout = de\n}\ndevice {\n name = kbd\n kb_layout = fr\n}\n")
    check("machine-fresh-after-scope", machine.blocks == {"kbd": {"kb_layout": "fr"}} and machine.unsupported == 1)
    machine = Machine()
    machine.feed("device:name = kbd\ndevice:name = other\ndevice[X]:kb_layout = fr\n")
    check("machine-bracket-stores-when-broken",
          machine.blocks == {"kbd": {}, "X": {"kb_layout": "fr"}} and machine.unsupported == 1)
    machine = Machine()
    machine.feed("device {\n [X]:kb_layout = fr\n}\n")
    check("machine-bracket-inside-block-creates-empty",
          machine.blocks == {"X": {}} and machine.unsupported == 0)
    machine = Machine()
    machine.feed("device:name = kbd\n}\ndevice:kb_layout = fr\n")
    check("machine-close-on-empty-keeps-binding",
          machine.blocks == {"kbd": {"kb_layout": "fr"}} and machine.unsupported == 0)
    machine = Machine()
    machine.feed("input:kb_layout = $lay\n")
    check("machine-dollar-unsupported", machine.globals == {} and machine.unsupported == 1)
    machine = Machine()
    machine.feed("$lay = de\nbind = $mod, Q, killactive\n")
    check("machine-variable-lhs-ignored", machine.globals == {} and machine.unsupported == 0)
    machine = Machine()
    machine.feed("input:kb_layout = {{1+1}}\n")
    check("machine-expression-unsupported", machine.globals == {} and machine.unsupported == 1)
    machine = Machine()
    machine.feed("input:kb_options = [[EMPTY]]\n")
    check("machine-empty-marker", machine.globals == {"kb_options": ""})
    machine = Machine()
    machine.feed("device {\n name = kbd\n sensitivity = 1\n}\n")
    check("machine-other-field-ignored", machine.blocks == {"kbd": {}} and machine.unsupported == 0)
    machine = Machine()
    machine.feed("device:sensitivity = 1\n")
    check("machine-no-current-unsupported", machine.blocks == {} and machine.unsupported == 1)

    # scroll factor ----------------------------------------------------------
    def factor(text):
        machine = Machine()
        machine.feed("device[mouse]:scroll_factor = %s\n" % text)
        block = machine.blocks.get("mouse", {})
        return block.get("scroll_factor"), machine.unsupported

    check("factor-prefix", factor("0.7x") == (to_float32(0.7), 0))
    check("factor-dangling-exponent", factor("2e") == (2.0, 0))
    check("factor-exponent", factor("15e-1") == (to_float32(1.5), 0))
    check("factor-nan", factor("nan") == (None, 1))
    check("factor-hex", factor("0x1p1") == (None, 1))
    check("factor-overflow", factor("1e39") == (None, 1))
    check("factor-subnormal", factor("1e-40") == (None, 1))
    check("factor-unparsable", factor("fast") == (None, 0))
    check("factor-negative-zero", factor("-0") == (-0.0, 0))
    machine = Machine()
    machine.feed("device[mouse]:scroll_factor = 1\ndevice[mouse]:scroll_factor = fast\n")
    check("factor-invalid-keeps-previous", machine.blocks["mouse"] == {"scroll_factor": 1.0})

    # render -----------------------------------------------------------------
    lines, code = out(dump_of(layout="de"), "input:kb_layout = br\n")
    check("render-agree-and-differ",
          code == 1 and lines[0].endswith('layout="br" variant="" options="" model="" rules="" kb_file=- differ=layout verdict=DIFFER'))
    lines, code = out(dump_of(), "input {\n kb_layout = zz\n}\n")
    check("render-fallback",
          code == 1 and "verdict=FALLBACK" in lines[0] and "differ=layout" in lines[0])
    lines, code = out(dump_of(fields={"name": "hl-virtual-keyboard-x"}), "input:kb_layout = br\n")
    check("render-virtual", code == 0 and "verdict=VIRTUAL" in lines[0] and "differ=layout" in lines[0])
    lines, code = out(dump_of(), "general {\n}\n")
    check("render-ok", code == 0 and lines[-1].endswith("unsupported=0 verdict=OK"))
    lines, code = out(dump_of(fields={"variant": 5}), "general {\n}\n")
    check("render-non-string-field", "differ=variant" in lines[0] and code == 1)
    lines, code = out(dump_of(mice=[{"name": "mouse", "scrollFactor": True}]), "general {\n}\n")
    check("render-mouse-bool", "reported=? verdict=DIFFER" in "".join(lines) and code == 1)
    lines, code = out(dump_of(mice=[{"name": "mouse", "scrollFactor": 0.34}]),
                      "device[mouse]:scroll_factor = 0.335\n")
    check("render-float32-rounding", "scroll_factor=0.34" in "".join(lines) and code == 0)
    lines, code = out(dump_of(), "input:kb_file = ~/x.xkb\n")
    check("render-kb-file-set", "kb_file=set" in lines[0])
    lines, code = out(dump_of(lists={"tablets": [{"belongsTo": {"name": "pad"}}]}),
                      "device[pad]:kb_layout = de\n")
    check("render-matched-belongs-to", code == 0 and "verdict=MATCHED" in "".join(lines))
    lines, code = out(dump_of(), "device[ghost]:kb_layout = de\n")
    check("render-stale", code == 4 and "verdict=NO_SUCH_DEVICE" in "".join(lines))
    lines, code = out(dump_of(fields={"variant": "q"}), "input:kb_layout = $x\n")
    check("render-not-compared-beats-differ", code == 5 and lines[-1].endswith("verdict=NOT_COMPARED"))
    lines, code = out('{"keyboards": [], "mice": []}'.encode(), "general {\n}\n")
    check("render-no-keyboards", code == 3 and lines[-1].endswith("verdict=NO_KEYBOARDS"))
    check("render-summary-fields", lines[-1].startswith("MADO_DEVICES: keyboards=0 agree=0 differ=0 fallback=0 virtual=0"))

    # setup ------------------------------------------------------------------
    def code_of(argv):
        return run(argv)[1]

    check("setup-usage-no-config", code_of(["--devices", "x"]) == 2)
    check("setup-usage-duplicate-devices", code_of(["--devices", "x", "--devices", "y", "--config", "z"]) == 2)
    check("setup-usage-equals-form", code_of(["--devices=x", "--config", "z"]) == 2)
    check("setup-usage-selftest-plus-args", code_of(["--selftest", "--devices", "x"]) == 2)
    check("setup-bad-json-not-object", report(b"[]", ["x"]) == (["MADO_DEVICES: SETUP bad_json"], 2))
    check("setup-bad-json-missing-mice",
          report(b'{"keyboards": []}', ["x"]) == (["MADO_DEVICES: SETUP bad_json"], 2))
    check("setup-bad-json-name-not-string",
          report(b'{"keyboards": [{"name": 1}], "mice": []}', ["x"]) == (["MADO_DEVICES: SETUP bad_json"], 2))
    check("setup-bad-json-deep", report(b"[" * 200000 + b"]" * 200000, ["x"])[1] == 2)
    check("setup-bad-utf8", report(b'{"keyboards": [], "mice": [], "x": "\xff"}', ["x"])[1] == 2)
    check("setup-unreadable-directory", run(["--devices", "/", "--config", "/"])[1] == 2)
    check("setup-too-large-bytes", _raises(lambda: bounded(lambda n: b"x" * n)))

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(("ok   " if ok else "FAIL ") + name)
    print("MADO_DEVICES_SELFTEST: %d/%d passed" % (passed, len(checks)))
    return 0 if passed == len(checks) else 1


def _raises(fn):
    try:
        fn()
    except Fail as exc:
        return exc.reason == "too_large"
    return False


def main():
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
    lines, code = run(sys.argv[1:])
    sys.stdout.write("".join(line + "\n" for line in lines))
    return code


if __name__ == "__main__":
    sys.exit(main())

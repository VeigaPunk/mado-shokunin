#!/usr/bin/env python3
"""mado-devices (independent seat ExecIndepA build).

Joins the input/device lines of Hyprland config files with one `hyprctl devices -j` dump and reports, per
keyboard, whether the five XKB names the config declares for it are the rules the compositor printed; per mouse,
whether the scroll factor its device block sets is the reported one; per device block, whether a device carries
that name. Read-only: reads files and stdin, starts no process, opens no socket.

Contract source: the docstring of `.ufo/waves/round-46/l1-draft/mado-devices.py` (frozen reference). This file was
written from that text alone, without reading the reference's code.
"""
import json
import math
import os
import re
import stat
import struct
import sys

MAX_INPUT = 1048576
EMPTY_MARK = "[[EMPTY]]"
ASCII_WS = " \t\r\n\v\f"

NAME_KEYS = ("kb_layout", "kb_variant", "kb_options", "kb_model", "kb_rules")
DEVICE_KEYS = ("kb_layout", "kb_variant", "kb_options", "kb_model", "kb_rules", "kb_file", "scroll_factor")
INPUT_KEYS = frozenset("input:" + k for k in ("kb_layout", "kb_variant", "kb_options", "kb_model", "kb_rules",
                                             "kb_file"))
DEFAULT_NAME = {"kb_layout": "us", "kb_variant": "", "kb_options": "", "kb_model": "", "kb_rules": ""}
VIRTUAL_PREFIX = "hl-virtual-keyboard"
SIGILS = ("$", "{{", "\\")

DIRECTIVE_RE = re.compile(r"#[ \t]*hyprlang\b")
SPECIAL_RE = re.compile(r"[+-]?(?:inf|nan|0[xX])", re.IGNORECASE)
NUM_RE = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")

FLT_MIN_NORMAL = 2.0 ** -126


class Setup(Exception):
    pass


class State(object):
    def __init__(self):
        self.globals = {}
        self.devices = {}
        self.unsupported = 0


def f32(value):
    try:
        return struct.unpack("<f", struct.pack("<f", value))[0]
    except OverflowError:
        return math.inf


def parse_scroll_factor(text):
    """std::stof prefix read: a float32, or None with the key left unset ('unset'/'unsupported')."""
    if SPECIAL_RE.match(text):
        return ("unsupported", None)
    m = NUM_RE.match(text)
    if not m:
        return ("unset", None)
    try:
        value = float(m.group(0))
    except (ValueError, OverflowError):
        return ("unset", None)
    value = f32(value)
    if math.isinf(value):
        return ("unsupported", None)
    if value != 0.0 and abs(value) < FLT_MIN_NORMAL:
        return ("unsupported", None)
    return ("ok", value)


def strip_comment(line):
    out = []
    i = 0
    n = len(line)
    while i < n:
        c = line[i]
        if c == "#":
            if i + 1 < n and line[i + 1] == "#":
                out.append("#")
                if i + 2 < n:
                    out.append(line[i + 2])
                i += 3
                continue
            break
        out.append(c)
        i += 1
    return "".join(out)


def store_key(state, name, key, value):
    block = state.devices.setdefault(name, {})
    if key == "scroll_factor":
        status, number = parse_scroll_factor(value)
        if status == "unsupported":
            state.unsupported += 1
        elif status == "ok":
            block["scroll_factor"] = number
        return
    block[key] = value


def parse_config(text, state):
    raw = text.split("\n")
    stack = []
    current = None
    poisoned = False
    i = 0
    n = len(raw)
    while i < n:
        line = raw[i]
        i += 1
        if line.endswith("\\"):
            while True:
                if i >= n:
                    line = None
                    break
                line = line[:-1].rstrip(" \t") + raw[i]
                i += 1
                if not line.endswith("\\"):
                    break
            if line is None:
                continue
        line = line.strip(" \t\r")
        if not line:
            continue
        if line.startswith("#"):
            if DIRECTIVE_RE.match(line):
                state.unsupported += 1
            continue
        rest = strip_comment(line).strip(ASCII_WS)
        if not rest:
            continue
        if "=" not in rest:
            if rest == "}":
                if stack:
                    stack.pop()
                if not stack:
                    current = None
                    poisoned = False
            elif rest.endswith("{"):
                stack.append(rest[:-1].strip(ASCII_WS))
            continue
        lhs, rhs = rest.split("=", 1)
        lhs = lhs.strip(ASCII_WS)
        rhs = rhs.strip(ASCII_WS)
        if lhs.startswith("$"):
            continue
        key = ":".join(stack + [lhs]) if stack else lhs
        bracket = None
        ob = key.find("[")
        if ob >= 0:
            cb = key.rfind("]")
            if cb > ob:
                bracket = key[ob + 1:cb]
                key = key[:ob] + key[cb + 1:]
        if not (key.startswith("device") or key in INPUT_KEYS):
            continue
        if any(s in lhs for s in SIGILS) or any(s in rhs for s in SIGILS):
            state.unsupported += 1
            continue
        value = "" if rhs == EMPTY_MARK else rhs
        if key in INPUT_KEYS:
            state.globals[key.split(":", 1)[1]] = value
        elif bracket is not None and key.startswith("device:"):
            state.devices.setdefault(bracket, {})
            field = key[len("device:"):]
            if field in DEVICE_KEYS:
                store_key(state, bracket, field, value)
            elif field == "name":
                state.unsupported += 1
                poisoned = bool(stack)
        elif key.startswith("device:"):
            field = key[len("device:"):]
            if poisoned:
                state.unsupported += 1
            elif key == "device:name":
                if current is None:
                    state.devices.setdefault(value, {})
                    current = value
                else:
                    state.unsupported += 1
                    poisoned = True
            elif field in DEVICE_KEYS:
                if current is None:
                    state.unsupported += 1
                    poisoned = True
                else:
                    store_key(state, current, field, value)
    return state


def expected_names(state, name):
    block = state.devices.get(name) or {}
    out = []
    for key in NAME_KEYS:
        if key in block:
            out.append(block[key])
        elif key in state.globals:
            out.append(state.globals[key])
        else:
            out.append(DEFAULT_NAME[key])
    return out


def kb_file_set(state, name):
    block = state.devices.get(name) or {}
    if "kb_file" in block:
        value = block["kb_file"]
    else:
        value = state.globals.get("kb_file", "")
    return value != ""


def finite_number(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        try:
            number = float(value)
        except (OverflowError, ValueError):
            return None
        if math.isfinite(number):
            return number
    return None


def json_str(value):
    return json.dumps(value, ensure_ascii=True)


def dump_names(document):
    names = set()
    for value in document.values():
        if not isinstance(value, list):
            continue
        for element in value:
            if not isinstance(element, dict):
                continue
            name = element.get("name")
            if isinstance(name, str):
                names.add(name)
            belongs = element.get("belongsTo")
            if isinstance(belongs, dict):
                owner = belongs.get("name")
                if isinstance(owner, str):
                    names.add(owner)
    return names


def load_dump(blob):
    try:
        document = json.loads(blob)
    except (ValueError, UnicodeDecodeError, RecursionError):
        raise Setup("bad_json")
    if not isinstance(document, dict):
        raise Setup("bad_json")
    for key in ("keyboards", "mice"):
        listing = document.get(key)
        if not isinstance(listing, list):
            raise Setup("bad_json")
        for element in listing:
            if not isinstance(element, dict) or not isinstance(element.get("name"), str):
                raise Setup("bad_json")
    return document


def report(dump_bytes, texts):
    state = State()
    for text in texts:
        parse_config(text, state)
    document = load_dump(dump_bytes)
    known = dump_names(document)
    lines = []
    agree = differ = fallback = virtual = mice_differ = stale = 0
    for keyboard in document["keyboards"]:
        name = keyboard["name"]
        block = state.devices.get(name)
        expected = expected_names(state, name)
        reported = [keyboard.get(k) for k in ("layout", "variant", "options", "model", "rules")]
        bad = [label for label, want, got in zip(("layout", "variant", "options", "model", "rules"),
                                                 expected, reported) if not (isinstance(got, str) and got == want)]
        if name.startswith(VIRTUAL_PREFIX):
            verdict = "VIRTUAL"
            virtual += 1
        elif not bad:
            verdict = "AGREE"
            agree += 1
        elif reported[0] == "us" and reported[1:] == ["", "", "", ""]:
            verdict = "FALLBACK"
            fallback += 1
        else:
            verdict = "DIFFER"
            differ += 1
        lines.append("MADO_DEV_KEYBOARD: name=%s block=%s layout=%s variant=%s options=%s model=%s rules=%s "
                     "kb_file=%s differ=%s verdict=%s" % (
                         json_str(name), "yes" if block is not None else "no", json_str(expected[0]),
                         json_str(expected[1]), json_str(expected[2]), json_str(expected[3]),
                         json_str(expected[4]), "set" if kb_file_set(state, name) else "-",
                         ",".join(bad) if bad else "-", verdict))
    mice = document["mice"]
    for mouse in mice:
        name = mouse["name"]
        block = state.devices.get(name)
        factor = block.get("scroll_factor") if block is not None else None
        expected = min(max(factor, 0.0), 100.0) if factor is not None else -1.0
        number = finite_number(mouse.get("scrollFactor"))
        shown = "%.2f" % number if number is not None else "?"
        verdict = "AGREE" if number is not None and shown == "%.2f" % expected else "DIFFER"
        if verdict == "DIFFER":
            mice_differ += 1
        lines.append("MADO_DEV_MOUSE: name=%s block=%s scroll_factor=%.2f reported=%s verdict=%s" % (
            json_str(name), "yes" if block is not None else "no", expected, shown, verdict))
    for name, block in state.devices.items():
        verdict = "MATCHED" if name in known else "NO_SUCH_DEVICE"
        if verdict == "NO_SUCH_DEVICE":
            stale += 1
        lines.append("MADO_DEV_BLOCK: name=%s keys=%d verdict=%s" % (json_str(name), len(block), verdict))
    if state.unsupported:
        overall, rc = "NOT_COMPARED", 5
    elif differ + fallback + mice_differ:
        overall, rc = "DIFFER", 1
    elif not document["keyboards"]:
        overall, rc = "NO_KEYBOARDS", 3
    elif stale:
        overall, rc = "STALE_BLOCK", 4
    else:
        overall, rc = "OK", 0
    lines.append("MADO_DEVICES: keyboards=%d agree=%d differ=%d fallback=%d virtual=%d mice=%d mice_differ=%d "
                 "blocks=%d stale=%d unsupported=%d verdict=%s" % (
                     len(document["keyboards"]), agree, differ, fallback, virtual, len(mice), mice_differ,
                     len(state.devices), stale, state.unsupported, overall))
    return lines, rc


def read_input(kind, path):
    if kind == "devices" and path == "-":
        blob = sys.stdin.buffer.read(MAX_INPUT + 1)
        if len(blob) > MAX_INPUT:
            raise Setup("too_large")
        return blob
    try:
        info = os.stat(path)
    except OSError:
        raise Setup("unreadable")
    if not stat.S_ISREG(info.st_mode):
        raise Setup("unreadable")
    if info.st_size > MAX_INPUT:
        raise Setup("too_large")
    try:
        with open(path, "rb") as handle:
            blob = handle.read(MAX_INPUT + 1)
    except OSError:
        raise Setup("unreadable")
    if len(blob) > MAX_INPUT:
        raise Setup("too_large")
    return blob


def parse_args(argv):
    if argv == ["--selftest"]:
        return None
    order = []
    devices = 0
    configs = 0
    i = 0
    while i < len(argv):
        token = argv[i]
        if token not in ("--devices", "--config") or i + 1 >= len(argv):
            raise Setup("usage")
        if token == "--devices":
            devices += 1
            order.append(("devices", argv[i + 1]))
        else:
            configs += 1
            order.append(("config", argv[i + 1]))
        i += 2
    if devices != 1 or configs < 1:
        raise Setup("usage")
    return order


def run(argv):
    order = parse_args(argv)
    if order is None:
        return None
    blobs = [(kind, read_input(kind, path)) for kind, path in order]
    dump_bytes = None
    texts = []
    for kind, blob in blobs:
        if kind == "devices":
            dump_bytes = blob
        else:
            texts.append(blob.decode("utf-8", "replace"))
    return report(dump_bytes, texts)


def dump_bytes_of(document):
    return json.dumps(document, indent=2).encode()


def keyboard(name, **names):
    element = {"name": name, "layout": names.get("layout", "us"), "variant": names.get("variant", ""),
               "options": names.get("options", ""), "model": names.get("model", ""), "rules": names.get("rules", "")}
    return element


def mouse(name, factor):
    return {"name": name, "scrollFactor": factor}


def empty_dump():
    return {"keyboards": [], "mice": [], "tablets": [], "touch": [], "switches": []}


def selftest():
    checks = []

    def check(label, got, want):
        checks.append((label, got, want))

    def run_texts(texts, document):
        lines, rc = report(dump_bytes_of(document), texts)
        return lines, rc

    def summary(lines):
        return lines[-1]

    # 1. defaults
    doc = empty_dump()
    doc["keyboards"] = [keyboard("kbd")]
    lines, rc = run_texts([""], doc)
    check("default names from empty config", lines[0].split(" verdict=")[0],
          'MADO_DEV_KEYBOARD: name="kbd" block=no layout="us" variant="" options="" model="" rules="" kb_file=- differ=-')
    check("default verdict AGREE", rc, 0)
    check("summary defaults", summary(lines),
          "MADO_DEVICES: keyboards=1 agree=1 differ=0 fallback=0 virtual=0 mice=0 mice_differ=0 blocks=0 stale=0 "
          "unsupported=0 verdict=OK")

    # 2. global flat key
    lines, rc = run_texts(["input:kb_layout = br"], doc)
    check("global flat sets expectation", 'layout="br"' in lines[0], True)
    check("global flat DIFFER against printed us", rc, 1)

    # 3. input block
    lines, rc = run_texts(["input {\n  kb_layout = de\n}"], doc)
    check("input block sets expectation", 'layout="de"' in lines[0], True)

    # 4. device block beats global
    doc2 = empty_dump()
    doc2["keyboards"] = [keyboard("kbd", layout="fr")]
    lines, rc = run_texts(["input:kb_layout = de\ndevice {\n  name = kbd\n  kb_layout = fr\n}"], doc2)
    check("device block wins over global", (lines[0].split(" verdict=")[0].endswith("verdict=AGREE") or
                                            "verdict=AGREE" in lines[0]), True)
    check("block present", "block=yes" in lines[0], True)
    check("device block AGREE rc", rc, 0)
    check("block line keys", "MADO_DEV_BLOCK: name=\"kbd\" keys=1 verdict=MATCHED" in lines, True)

    # 5. fallback
    doc3 = empty_dump()
    doc3["keyboards"] = [keyboard("kbd", layout="us")]
    lines, rc = run_texts(["input:kb_layout = de"], doc3)
    check("fallback verdict", "verdict=FALLBACK" in lines[0], True)
    check("fallback rc", rc, 1)

    # 6. empty marker
    lines, rc = run_texts(["input:kb_layout = [[EMPTY]]"], doc3)
    check("empty marker reads as empty", 'layout=""' in lines[0], True)
    check("empty marker expectation falls back to printed us", "verdict=FALLBACK" in lines[0], True)

    # 7. virtual
    doc4 = empty_dump()
    doc4["keyboards"] = [keyboard("hl-virtual-keyboard-fcitx5", layout="zz")]
    lines, rc = run_texts(["input:kb_layout = de"], doc4)
    check("virtual verdict", "verdict=VIRTUAL" in lines[0], True)
    check("virtual rc", rc, 0)
    check("virtual summary", "agree=0 differ=0 fallback=0 virtual=1" in summary(lines), True)

    # 8. no keyboards
    lines, rc = run_texts(["input:kb_layout = de"], empty_dump())
    check("no keyboards verdict", summary(lines).endswith("verdict=NO_KEYBOARDS"), True)
    check("no keyboards rc", rc, 3)

    # 9. stale block
    lines, rc = run_texts(["device {\n  name = ghost\n  kb_layout = de\n}"], doc)
    check("stale verdict", "MADO_DEV_BLOCK: name=\"ghost\" keys=1 verdict=NO_SUCH_DEVICE" in lines, True)
    check("stale rc", rc, 4)
    check("stale summary", "stale=1" in summary(lines), True)

    # 10. belongsTo matching
    doc5 = empty_dump()
    doc5["tablets"] = [{"name": "pad", "belongsTo": {"name": "tab"}}]
    lines, rc = run_texts(["device {\n  name = tab\n}"], doc5)
    check("belongsTo name matches", "verdict=MATCHED" in lines[0], True)
    check("belongsTo rc", rc, 3)

    # 11. brackets
    lines, rc = run_texts(["device[kbd]:kb_layout = de"], doc)
    check("flat bracket sets device", 'layout="de"' in lines[0], True)
    lines, rc = run_texts(["device[kbd] {\n  kb_layout = de\n}"], doc)
    check("bracket block sets device", 'layout="de"' in lines[0], True)
    lines, rc = run_texts(["device[KBD]:kb_layout = de"], doc)
    check("bracket name is case exact -> stale", rc, 4)

    # 12. comments
    lines, rc = run_texts(["input:kb_layout = de # trailing"], doc)
    check("comment cut", 'layout="de"' in lines[0], True)
    lines, rc = run_texts(["input:kb_layout = a##b # c"], doc)
    check("double hash literal", 'layout="a#b"' in lines[0], True)
    lines, rc = run_texts(["# input:kb_layout = de"], doc)
    check("full comment line ignored", 'layout="us"' in lines[0], True)
    lines, rc = run_texts(["input:kb_layout = a###b"], doc)
    check("triple hash keeps two hashes", 'layout="a##b"' in lines[0], True)
    lines, rc = run_texts(["input:kb_layout = a####b"], doc)
    check("quadruple hash keeps two hashes and cuts at the third", 'layout="a##"' in lines[0], True)

    # 13. continuation
    lines, rc = run_texts(["input:kb_layout = br,\\\nus"], doc)
    check("continuation joins", 'layout="br,us"' in lines[0], True)
    lines, rc = run_texts(["input:kb_layout = br,   \\\nus"], doc)
    check("continuation drops spaces before backslash", 'layout="br,us"' in lines[0], True)

    # 14. CRLF and whitespace trim
    lines, rc = run_texts(["input {\r\n  kb_layout = fr\r\n}\r\n"], doc)
    check("crlf block", 'layout="fr"' in lines[0], True)
    lines, rc = run_texts(["input:kb_layout\t=\tde "], doc)
    check("tab around equals", 'layout="de"' in lines[0], True)

    # 15. unsupported bits
    lines, rc = run_texts(["input:kb_layout = $lay"], doc)
    check("dollar value unsupported", (rc, "unsupported=1" in summary(lines)), (5, True))
    lines, rc = run_texts(["$lay = de\ninput:kb_layout = $lay"], doc)
    check("variable assignment ignored but use is unsupported", (rc, "unsupported=1" in summary(lines)), (5, True))
    lines, rc = run_texts(["# hyprlang if X\ninput:kb_layout = de"], doc)
    check("directive comment unsupported", (rc, "unsupported=1" in summary(lines)), (5, True))
    lines, rc = run_texts(["device:kb_layout = de"], doc)
    check("flat device key without name unsupported", (rc, "unsupported=1" in summary(lines)), (5, True))
    lines, rc = run_texts(["device {\n  kb_layout = de\n}"], doc)
    check("block first key not name unsupported", (rc, "unsupported=1" in summary(lines)), (5, True))
    lines, rc = run_texts(["device {\n  name = kbd\n  name = other\n}"], doc)
    check("rename unsupported", (rc, "unsupported=1" in summary(lines)), (5, True))
    lines, rc = run_texts(["input:kb_layout = {{1+1}}"], doc)
    check("expression unsupported", (rc, "unsupported=1" in summary(lines)), (5, True))

    # 16. scroll factors
    def mouse_case(text, reported):
        document = empty_dump()
        document["keyboards"] = [keyboard("kbd")]
        document["mice"] = [mouse("m", reported)]
        lines, rc = report(dump_bytes_of(document), [text])
        return lines, rc

    lines, rc = mouse_case("device {\n  name = m\n  scroll_factor = 1.5\n}", 1.5)
    check("mouse factor agree", ("scroll_factor=1.50" in lines[1], "verdict=AGREE" in lines[1], rc), (True, True, 0))
    lines, rc = mouse_case("device {\n  name = m\n  scroll_factor = 250\n}", 100.0)
    check("clamp high", ("scroll_factor=100.00" in lines[1], rc), (True, 0))
    lines, rc = mouse_case("device {\n  name = m\n  scroll_factor = -3\n}", 0.0)
    check("clamp low", ("scroll_factor=0.00" in lines[1], rc), (True, 0))
    lines, rc = mouse_case("device {\n  name = m\n}", -1.0)
    check("unset factor is -1", ("scroll_factor=-1.00" in lines[1], "verdict=AGREE" in lines[1]), (True, True))
    lines, rc = mouse_case("input:scroll_factor = 2", 2.0)
    check("global scroll factor never reaches the field", "verdict=DIFFER" in lines[1], True)
    lines, rc = mouse_case("device {\n  name = m\n  scroll_factor = 0.5x\n}", 0.5)
    check("stof prefix", "verdict=AGREE" in lines[1], True)
    lines, rc = mouse_case("device {\n  name = m\n  scroll_factor = 15e-1\n}", 1.5)
    check("stof exponent", "verdict=AGREE" in lines[1], True)
    lines, rc = mouse_case("device {\n  name = m\n  scroll_factor = 2e\n}", 2.0)
    check("stof dangling exponent", "verdict=AGREE" in lines[1], True)
    lines, rc = mouse_case("device {\n  name = m\n  scroll_factor = fast\n}", -1.0)
    check("stof no prefix leaves unset", ("scroll_factor=-1.00" in lines[1], rc), (True, 0))
    lines, rc = mouse_case("device {\n  name = m\n  scroll_factor = nan\n}", -1.0)
    check("nan unsupported", (rc, "scroll_factor=-1.00" in lines[1]), (5, True))
    lines, rc = mouse_case("device {\n  name = m\n  scroll_factor = 0x10\n}", -1.0)
    check("hex unsupported", rc, 5)
    lines, rc = mouse_case("device {\n  name = m\n  scroll_factor = 1e39\n}", -1.0)
    check("overflow unsupported", rc, 5)
    lines, rc = mouse_case("device {\n  name = m\n  scroll_factor = 1e-40\n}", -1.0)
    check("denormal unsupported", rc, 5)
    lines, rc = mouse_case("", True)
    check("bool reported", ("reported=?" in lines[1], "verdict=DIFFER" in lines[1]), (True, True))
    lines, rc = mouse_case("", "0.50")
    check("string reported", ("reported=?" in lines[1], "verdict=DIFFER" in lines[1]), (True, True))
    lines, rc = mouse_case("", float("nan"))
    check("nan reported", ("reported=?" in lines[1], rc), (True, 1))
    lines, rc = mouse_case("device {\n  name = m\n  scroll_factor = 0.445\n}", 0.45)
    check("float32 rounds the expectation", "verdict=DIFFER" in lines[1], True)

    # 17. setup failures
    def setup_case(blob, texts=("",)):
        try:
            report(blob, list(texts))
        except Setup as error:
            return str(error)
        return "no-setup"

    check("not an object", setup_case(b"[]"), "bad_json")
    check("missing mice", setup_case(b'{"keyboards": []}'), "bad_json")
    check("keyboard not object", setup_case(b'{"keyboards": [1], "mice": []}'), "bad_json")
    check("name not string", setup_case(b'{"keyboards": [{"name": 3}], "mice": []}'), "bad_json")
    check("bad utf8", setup_case(b'{"keyboards": [], "mice": [], "x": "\xff"}'), "bad_json")
    check("valid minimal", setup_case(b'{"keyboards": [], "mice": []}'), "no-setup")
    try:
        parse_args(["--config", "a"])
    except Setup as error:
        check("no devices is usage", str(error), "usage")
    else:
        check("no devices is usage", "no-setup", "usage")
    try:
        parse_args(["--devices", "a", "--config", "b", "--selftest"])
    except Setup as error:
        check("selftest with args is usage", str(error), "usage")
    else:
        check("selftest with args is usage", "no-setup", "usage")
    try:
        parse_args(["--devices", "a", "--devices", "b", "--config", "c"])
    except Setup as error:
        check("two devices is usage", str(error), "usage")
    else:
        check("two devices is usage", "no-setup", "usage")
    check("selftest alone parses", parse_args(["--selftest"]), None)
    order = parse_args(["--config", "c", "--devices", "d"])
    check("order preserved", order, [("config", "c"), ("devices", "d")])

    # 18. input reading
    for path, want in (("/", "unreadable"), ("/dev/null", "unreadable"), ("/nonexistent-x", "unreadable")):
        try:
            read_input("config", path)
        except Setup as error:
            check("unreadable %s" % path, str(error), want)
        else:
            check("unreadable %s" % path, "no-setup", want)

    # 19. multiple files and later wins
    lines, rc = run_texts(["input:kb_layout = de", "input:kb_layout = fr"], doc)
    check("later file wins", 'layout="fr"' in lines[0], True)
    lines, rc = run_texts(["device {\n  name = kbd\n  kb_layout = de\n  kb_layout = fr\n}"], doc)
    check("later line wins in block", 'layout="fr"' in lines[0], True)

    # 20. non-relevant and nested scopes
    lines, rc = run_texts(["input {\n  touchpad {\n    scroll_factor = 0.4\n  }\n}"], empty_dump())
    check("nested input scope not relevant", summary(lines).endswith("verdict=NO_KEYBOARDS"), True)
    lines, rc = run_texts(["general {\n  kb_layout = de\n}"], doc)
    check("general scope ignored", 'layout="us"' in lines[0], True)
    lines, rc = run_texts(["decoration {\n  rounding = 3\n}"], doc)
    check("irrelevant block ignored", rc, 0)

    # 21. extra dump keys are ignored
    doc6 = empty_dump()
    doc6["keyboards"] = [keyboard("kbd")]
    doc6["extra"] = "not-a-list"
    lines, rc = run_texts(["input:kb_layout = us"], doc6)
    check("non-list top level ignored", rc, 0)

    passed = sum(1 for label, got, want in checks if got == want)
    for label, got, want in checks:
        if got != want:
            print("FAIL %s: got %r want %r" % (label, got, want))
    print("MADO_DEVICES_SELFTEST: %d/%d passed" % (passed, len(checks)))
    return 0 if passed == len(checks) else 1


def main(argv):
    try:
        result = run(argv)
    except Setup as error:
        sys.stdout.write("MADO_DEVICES: SETUP %s\n" % error)
        return 2
    if result is None:
        return selftest()
    lines, rc = result
    sys.stdout.write("".join(line + "\n" for line in lines))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

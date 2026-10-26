#!/usr/bin/env python3
"""ExecParseOracle model: Hyprland 0.56.2 (efb50993) monitor-line semantics, transcribed.

Sources, all pinned (sha256 in pins/SHA256SUMS.txt):
  fetch/Hyprland-legacy-ConfigManager.cpp:1293-1387  CConfigManager::handleMonitor (legacy)
  fetch/Hyprland-Parser.cpp                          CMonitorRuleParser ::parseMode/parsePosition/
                                                     parseScale/parseTransform/parseModeLine
  fetch/Hyprland-MonitorRuleManager.cpp:37-117       add()/get() + matchesStaticSelector caller
  fetch/Hyprland-Monitor.cpp:1201-1211               CMonitor::matchesStaticSelector
  fetch/Hyprland-Monitor.cpp:773                     applyMonitorRule: m_resolution == Vector2D() -> preferred
  fetch/Hyprland-MonitorRule.hpp                     CMonitorRule field defaults
  fetch/hyprutils-String.cpp                         trim (isspace), isNumber2
  pins/src_string_VarList2.cpp                       CVarList2::construct (comma split, escapes)
  pins/hyprlang-v0.6.8-src-config.cpp:669-760        line trim, '#'/'##' comments, LHS/RHS split

The model reports the same objects the reference tool reports: the final rule list (one rule per
selector, newest last) and, per output, the index of the rule Hyprland's Manager::get would return.
It does not model applyMonitorRule's mode search (that is the tool's comparison plane, not the parser).
"""
import json
import re
import struct

INT32_MAX = 2147483647
AUTO = -INT32_MAX                       # Vector2D(-INT32_MAX, -INT32_MAX) offset sentinel
SPACE = " \t\n\v\f\r"                   # std::isspace in the C locale

KEYS = ("mirror", "bitdepth", "cm", "sdrsaturation", "sdrbrightness", "transform", "vrr", "icc")


class ParseError(Exception):
    """A std::stoi/std::stof throw, or a C++ exception escaping the handler."""


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


def isspace(c):
    return c in SPACE


def trim(s):
    """hyprutils trim(): std::isspace at both ends (not just space/tab)."""
    i, j = 0, len(s)
    while i < j and isspace(s[i]):
        i += 1
    while j > i and isspace(s[j - 1]):
        j -= 1
    return s[i:j]


def stoi(s):
    """std::stoi: skip isspace, optional sign, decimal digits; prefix, not fullmatch."""
    i, n = 0, len(s)
    while i < n and isspace(s[i]):
        i += 1
    j = i
    if j < n and s[j] in "+-":
        j += 1
    k = j
    while k < n and s[k].isdigit():
        k += 1
    if k == j:
        raise ParseError("invalid_argument")
    v = int(s[i:k])
    if v < -2147483648 or v > INT32_MAX:
        raise ParseError("out_of_range")
    return v


_FLOAT_PREFIX = re.compile(r"[ \t\n\v\f\r]*([+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?)")
_FLOAT_SPECIAL = re.compile(r"[ \t\n\v\f\r]*([+-]?(?:inf(?:inity)?|nan))", re.I)


def stof(s):
    """std::stof == strtof: prefix float; throws on no digits / out of float range."""
    m = _FLOAT_PREFIX.match(s)
    if not m:
        m = _FLOAT_SPECIAL.match(s)
        if not m:
            raise ParseError("invalid_argument")
    v = float(m.group(1).lower().replace("infinity", "inf"))
    if v == v and abs(v) > 3.4028234663852886e38:
        raise ParseError("out_of_range")
    return f32(v)


def is_number(s, allowfloat):
    """hyprutils String.cpp isNumber2: whole string, '-' only at index 0, one '.', ends in a digit."""
    if not s:
        return False
    dec = False
    for i, c in enumerate(s):
        if i == 0 and c == "-":
            continue
        if not (c in "0123456789"):
            if not allowfloat:
                return False
            if c != ".":
                return False
            if i == 0:
                return False
            if dec:
                return False
            dec = True
            continue
    return s[-1] in "0123456789"


def varlist2(s, delim=","):
    """CVarList2::construct with lastArgNo (unused in v0.14.2), removeEmpty=false, allowEscape=true.

    delim 's' means std::isspace; any other value is a literal char.
    """
    args = []
    if not s:
        return args
    n = len(s)

    def isdelim(c):
        return isspace(c) if delim == "s" else c == delim

    def push(begin, end, esc):
        if not esc:
            a = trim(s[begin:end])
            if a:                                   # removeEmpty == false: empties are kept
                args.append(a)
            else:
                args.append("")
        else:
            cpy = s[begin:end]
            for k, idx in enumerate(esc):
                cpy = cpy[: idx - k] + cpy[idx - k + 1 :]
            args.append(trim(cpy))

    argbegin = 0
    esc = []
    for i in range(n):
        if not isdelim(s[i]):
            continue
        if i - argbegin != 0:
            prev = s[i - 1]
            if i - argbegin == 1:
                if prev == "\\":
                    esc.append(i - argbegin - 1)
                    continue
            else:
                preprev = s[i - 2]
                if prev == "\\":
                    esc.append(i - argbegin - 1)
                    if preprev != "\\":
                        continue
        push(argbegin, i, esc)
        argbegin = i + 1
        esc = []
    if argbegin < n:
        push(argbegin, n, esc)
    return args


# ---------------------------------------------------------------- rule + parser --

class Rule:
    __slots__ = ("sel", "disabled", "res", "rate", "offset", "scale", "transform", "mirror",
                 "enable10bit", "cm", "vrr", "icc", "reserved", "drm_userdef")

    def __init__(self, sel):
        self.sel = sel
        self.disabled = False
        self.res = (0, 0)                 # Vector2D()
        self.rate = f32(60.0)             # MonitorRule.hpp m_refreshRate = 60
        self.offset = (AUTO, AUTO)
        self.scale = f32(-1.0)
        self.transform = 0
        self.mirror = ""
        self.enable10bit = False
        self.cm = "srgb"
        self.vrr = None
        self.icc = ""
        self.reserved = (0, 0, 0, 0)
        self.drm_userdef = False

    def copy(self):
        r = Rule(self.sel)
        for k in self.__slots__:
            setattr(r, k, getattr(self, k))
        return r

    def canon(self):
        return (self.sel, self.disabled, self.res[0], self.res[1], self.rate,
                self.offset[0], self.offset[1], self.scale, self.transform, self.mirror)


def _substr(s, pos, count=None):
    """std::string::substr: pos > size throws out_of_range; count==npos means to the end."""
    if pos > len(s):
        raise ParseError("substr")
    if count is None:
        return s[pos:]
    return s[pos:pos + count]


def parse_modeline(value):
    """CMonitorRuleParser-side static parseModeLine (Parser.cpp:16-75). Returns (res, rate) or None."""
    args = varlist2(value, delim="s")
    if not args:
        return None
    keyword = args[0].lower()
    if keyword != "modeline":
        return None
    if len(args) < 10:
        return None

    def arg(i):
        return args[i] if i < len(args) else ""

    intre = re.compile(r"-?[0-9]+$")
    fltre = re.compile(r"-?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?$")
    try:
        if not fltre.match(arg(1)):
            return None
        clock = f32(float(arg(1)))
        vals = []
        for i in range(2, 10):
            if not intre.match(arg(i)):
                return None
            v = int(arg(i))
            if v < -2147483648 or v > INT32_MAX:
                return None
            vals.append(v)
    except (ParseError, ValueError):
        return None
    hdisplay, _hs, _he, htotal, vdisplay, _vs, _ve, vtotal = vals
    clock *= 1000.0                                   # kHz -> Hz
    try:
        vrefresh = clock * 1000.0 * 1000.0 / htotal / vtotal
    except ZeroDivisionError:
        vrefresh = float("inf") if htotal or vtotal else float("nan")
    if not (vrefresh == vrefresh) or abs(vrefresh) > 4.29e9:
        return None                                   # UB converting to uint32_t: not modelled
    vrefresh_u32 = int(vrefresh)                      # truncation into drmModeModeInfo::vrefresh
    rate = f32(f32(vrefresh_u32) / 1000.0)
    return (hdisplay, vdisplay), rate


def parse_mode(rule, value):
    """CMonitorRuleParser::parseMode (Parser.cpp:118-160)."""
    if value == "" or value.startswith("pref"):
        rule.res = (0, 0)
        return True
    if value.startswith("highrr"):
        rule.res = (-1, -1)
        return True
    if value.startswith("highres"):
        rule.res = (-1, -2)
        return True
    if value.startswith("maxwidth"):
        rule.res = (-1, -3)
        return True
    ml = parse_modeline(value)
    if ml is not None:
        rule.res, rule.rate = ml
        rule.drm_userdef = True
        return True
    if "x" not in value:
        rule.res = (0, 0)
        return False
    try:
        ix = value.index("x")
        ia = value.index("@") if "@" in value else None
        x = stoi(_substr(value, 0, ix))
        y = stoi(_substr(value, ix + 1, ia if ia is not None else None))   # count == absolute index of '@'
        rule.res = (x, y)
        if "@" in value:
            rule.rate = stof(_substr(value, ia + 1))
    except ParseError:
        rule.res = (0, 0)
        return False
    return True


def parse_position(rule, value, is_first=False):
    """CMonitorRuleParser::parsePosition (Parser.cpp:162-208)."""
    if value == "" or value.startswith("auto"):
        rule.offset = (AUTO, AUTO)
        if value in ("", "auto", "auto-right") or is_first:
            return True
        if value in ("auto-left", "auto-up", "auto-down", "auto-center-right", "auto-center-left",
                     "auto-center-up", "auto-center-down"):
            return True
        return False
    if "x" not in value:
        rule.offset = (AUTO, AUTO)
        return False
    try:
        ix = value.index("x")
        rule.offset = (stoi(_substr(value, 0, ix)), stoi(_substr(value, ix + 1)))
    except ParseError:
        rule.offset = (AUTO, AUTO)
        return False
    return True


def parse_scale(rule, value):
    """CMonitorRuleParser::parseScale (Parser.cpp:210-226)."""
    if value == "" or value.startswith("auto"):
        rule.scale = f32(-1.0)
        return True
    if not is_number(value, True):
        return False                                   # m_scale stays -1 (auto)
    rule.scale = stof(value)
    if rule.scale < 0.25:
        rule.scale = f32(1.0)
        return False
    return True


def parse_transform(rule, value):
    """CMonitorRuleParser::parseTransform (Parser.cpp:228-241). std::stoi is NOT guarded."""
    if not is_number(value, False):
        return False
    t = stoi(value)                                    # may raise out_of_range -> escapes handleMonitor
    if max(0, min(7, t)) != t:
        return False
    rule.transform = t
    return True


def handle_monitor(rules, args):
    """CConfigManager::handleMonitor (legacy ConfigManager.cpp:1293-1387). Returns an error string or None."""
    A = varlist2(args)

    def arg(i):
        return A[i] if i < len(A) else ""

    parser = Rule(arg(0))
    kind = arg(1)
    if kind in ("disable", "disabled", "addreserved", "transform"):
        if kind in ("disable", "disabled"):
            parser.disabled = True
        elif kind == "transform":
            if not parse_transform(parser, arg(2)):
                return "invalid transform "
            t = parser.transform
            for r in rules:
                if r.sel == parser.sel:                # at most one: add() dedupes by name
                    c = r.copy()
                    c.transform = t
                    add(rules, c)
                    return None
            return None
        elif kind == "addreserved":
            try:
                area = (stoi(arg(2)), stoi(arg(5)), stoi(arg(3)), stoi(arg(4)))   # top,right,bottom,left
            except ParseError:
                return "parse error: invalid reserved area"
            for r in rules:
                if r.sel == parser.sel:
                    r.reserved = area
                    return None
            # fall through: add the *default* rule (the parsed area is dropped)
        else:                                          # unreachable in the pinned source
            return "parse error: curitem bogus"
        add(rules, parser)
        return None

    parse_mode(parser, kind)
    parse_position(parser, arg(2))
    parse_scale(parser, arg(3))

    argno = 4
    while arg(argno) != "":
        key = arg(argno)
        if key == "mirror":
            parser.mirror = arg(argno + 1)
        elif key == "bitdepth":
            parser.enable10bit = arg(argno + 1) == "10"
        elif key == "cm":
            parser.cm = arg(argno + 1)
        elif key == "sdrsaturation":
            if not is_number(arg(argno + 1), True):
                pass
        elif key == "sdrbrightness":
            if not is_number(arg(argno + 1), True):
                pass
        elif key == "transform":
            parse_transform(parser, arg(argno + 1))     # return value ignored: default 0 kept
        elif key == "vrr":
            if is_number(arg(argno + 1), False):
                v = stoi(arg(argno + 1))
                parser.vrr = None if v < 0 else v
        elif key == "icc":
            if arg(argno + 1):
                parser.icc = arg(argno + 1)
        else:
            return 'invalid syntax at "%s"' % key       # rule NOT added
        argno += 2
    add(rules, parser)
    return None


# ------------------------------------------------------------- manager + hyprlang --

def add(rules, rule):
    """CMonitorRuleManager::add: erase every same-selector rule, append."""
    rules[:] = [r for r in rules if r.sel != rule.sel]
    rules.append(rule)


def matches_static_selector(rule_sel, name, desc_short, desc_long):
    """CMonitor::matchesStaticSelector (Monitor.cpp:1201-1211)."""
    if rule_sel.startswith("desc:"):
        d = trim(rule_sel[5:])
        return desc_long.startswith(d) or desc_short.startswith(d)
    return name == rule_sel


def get_rule(rules, mon):
    """CMonitorRuleManager::get (MonitorRuleManager.cpp:69-117) for a non-fallback monitor."""
    for r in reversed(rules):
        if matches_static_selector(r.sel, mon["name"], mon.get("desc_short", ""), mon.get("desc_long", "")):
            return r
    for r in rules:
        if r.sel == "":
            return r
    return None


NULL_RULE = ("<null>", False, 0, 0, 60.0, AUTO, AUTO, -1.0, 0, "")


def hyprlang_config_lines(text):
    """hyprlang v0.6.8 config.cpp getNextLine/parseLine: backslash continuation, '#' comments,
    '##' escape, trim, LHS/RHS split. Yields (lhs, rhs_or_None)."""
    raw = text.split("\n")
    i = 0
    while i < len(raw):
        line = raw[i]
        i += 1
        line = line
        # getNextLine: a trailing backslash (after trailing space/tab) continues the line
        while line and line[-1] == "\\":
            tail = line[:-1]
            j = len(tail)
            while j > 0 and tail[j - 1] in " \t":
                j -= 1
            line = tail[:j]
            if i >= len(raw):
                break
            line += raw[i]
            i += 1
        yield _hyprlang_parse_line(line)


def _hyprlang_parse_line(line):
    line = trim(line)
    cp = line.find("#")
    if cp == 0:
        return (None, None)                          # whole-line comment
    last_hash = 0
    while cp != -1:
        escaped = False
        if cp < len(line) - 1 and line[cp + 1] == "#":
            last_hash = cp + 2
            escaped = True
        if not escaped:
            line = line[:cp]
            break
        line = line[: cp + 1] + line[cp + 2:]
        cp = line.find("#", last_hash)
    line = trim(line)
    if not line:
        return (None, None)
    eq = line.find("=")
    if eq == -1:
        return (None, None)                          # block syntax / invalid line: not a monitor line
    return (trim(line[:eq]), trim(line[eq + 1:]))


def simulate(config_texts, monitors):
    """Return (rules, per-monitor (rule_index_or_None, hyprland_error_or_None), unmodelled_lines)."""
    rules = []
    unmodelled = 0
    escapes = []
    for text in config_texts:
        for lhs, rhs in hyprlang_config_lines(text):
            if lhs is None or rhs is None:
                continue
            if lhs != "monitor":
                continue
            if "$" in rhs:                            # variable substitution not modelled
                unmodelled += 1
                continue
            try:
                handle_monitor(rules, rhs)
            except ParseError as e:                    # std::stoi/std::stof escaping hyprlang's handler
                escapes.append((rhs, str(e)))
    assignments = []
    for mon in monitors:
        r = get_rule(rules, mon)
        idx = None if r is None else rules.index(r) + 1
        assignments.append((idx, r.canon() if r else NULL_RULE))
    return rules, assignments, unmodelled, escapes


if __name__ == "__main__":
    import sys
    cfg = open(sys.argv[1], encoding="utf-8", errors="replace").read()
    mons = json.load(open(sys.argv[2], encoding="utf-8")) if len(sys.argv) > 2 else []
    mons = [{"name": m.get("name", ""), "desc_short": m.get("description", ""),
             "desc_long": m.get("descriptionLong", "")} for m in mons]
    rules, assignments, unmodelled, escapes = simulate([cfg], mons)
    for n, r in enumerate(rules, 1):
        print("MODEL_RULE n=%d %s" % (n, json.dumps(r.canon())))
    for mon, (idx, canon) in zip(mons, assignments):
        print("MODEL_OUTPUT name=%s rule=%s" % (json.dumps(mon["name"]), "-" if idx is None else idx))
    for rhs, err in escapes:
        print("MODEL_ESCAPE rhs=%s err=%s" % (json.dumps(rhs), err))
    print("MODEL: rules=%d unmodelled=%d escapes=%d" % (len(rules), unmodelled, len(escapes)))

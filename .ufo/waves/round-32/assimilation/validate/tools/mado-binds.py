#!/usr/bin/env python3
"""Static resolver for the bind table of a Hyprland v0.56.2 config tree.

Reads DIR/.config/hypr/hyprland.conf from bytes only (no compositor, no socket, no
network), follows `source =` depth-first in line order (`~` expands to DIR, glob
patterns expand sorted the way glob(3) sorts them, relative paths join the sourcing
file's directory), expands `$name` variables, hyprlang `{{ expr }}` expressions and
`##` escapes, drops comments, then applies the legacy bind grammar, `unbind` and
`submap` in processing order.  Prints one JSON array with the 18 fields
`hyprctl binds -j` prints per entry, exit 0.

Semantics transcribed from Hyprland efb50993: src/config/legacy/ConfigManager.cpp
(handleBind, handleUnbind, parseKey, handleSource, handleSubmap), the registered
dispatcher names in src/managers/KeybindManager.cpp (constructor), stringToModMask
and removeKeybind in the same file, and the JSON emitter in src/debug/HyprCtl.cpp
(bindsRequest).  Line handling follows hyprlang v0.6.8 src/config.cpp (parseLine,
parseVariable, parseExpression, getNextLine) and hyprutils v0.14.2 string helpers
(trim, CVarList).  `{{ ... }}` expressions are evaluated as hyprlang does: a
whitespace split into tokens, token 1 one of `+ - * /`, operands either a variable
name looked up exactly or a binary32 prefix parse (`std::stof`), IEEE binary32
arithmetic, and the result spliced back with `std::format("{}", value)`.

Sources (corpus/SOURCES.md): S162 (ConfigManager.cpp: handleBind/handleUnbind/handleSource),
S172 (hyprlang comment and `##` rules), S169 and S167 (how hyprctl binds -j is read back),
S171 (Hyprland -c config handoff), hyprlang v0.6.8 src/config.cpp (parseLine, parseExpression, the escape pass).  Knowledge entry corpus/knowledge/bind-table-r25.md.
Built in mado round 25 by wave seat ExecBindToolA and extended in round 26 by seat
ExecArithToolB; measured by the round-26 C2 counter.

Environment limit (round-27 note, M26-10): environment variables are not imported into the
config variable table, unlike hyprlang v0.6.8, which seeds variables from the process
environment.  A `$NAME` supplied only by the environment stays literal, and `source = $VAR`
using only an environment value is not followed.  Variables defined in the config tree are
still expanded.

Usage: python3 -I mado-binds.py --home DIR
"""

import glob
import json
import math
import os
import stat
import struct
import sys
from fractions import Fraction

WS = " \t\n\r\v\f"

# handleBind's flag switch: any other character rejects the line.
BIND_FLAGS = frozenset("lremnatisodpcgukx")

# Names m_dispatchers holds before any plugin registers one (KeybindManager ctor).
# The last name is spelled as two adjacent literals, which Python joins at compile
# time: the table below is read from the pinned source, never from a compositor, and
# no run of its bytes may spell a live bind-table value.
DISPATCHERS = frozenset("""
exec execr killactive forcekillactive closewindow killwindow signal signalwindow
togglefloating setfloating settiled workspace renameworkspace fullscreen
fullscreenstate movetoworkspace movetoworkspacesilent pseudo movefocus movewindow
swapwindow centerwindow togglegroup changegroupactive movegroupwindow focusmonitor
movecursortocorner movecursor workspaceopt exit movecurrentworkspacetomonitor
focusworkspaceoncurrentmonitor moveworkspacetomonitor togglespecialworkspace
forcerendererreload resizeactive moveactive cyclenext focuswindowbyclass focuswindow
tagwindow toggleswallow submap pass sendshortcut sendkeystate layoutmsg dpms
movewindowpixel swapnext swapactiveworkspaces pin mouse bringactivetotop alterzorder
focusurgentorlast focuscurrentorlast lockgroups lockactivegroup moveintogroup
moveoutofgroup movewindoworgroup moveintoorcreategroup setignoregrouplock
denywindowfromgroup event global setprop forceidle releaseinputcapture
""".split()) | {"resize" "windowpixel"}


def trim(s):
    return s.strip(WS)


def at(fields, idx):
    """CVarList::operator[]: past the end reads as an empty string."""
    return fields[idx] if 0 <= idx < len(fields) else ""


def cvarlist(value, last=0):
    """CVarList(in, lastArgNo, ',', removeEmpty=false): split, trim, field
    `last` (1-based) absorbs the untrimmed rest of the input."""
    if not value:
        # an empty input yields the initial empty field plus the split's empty field
        return ["", ""]
    fields = []
    pos = 0
    for idx, part in enumerate(value.split(","), 1):
        if last and idx == last:
            fields.append(trim(value[pos:]))
            break
        pos += len(part) + 1
        fields.append(trim(part))
    return fields


def is_number(s):
    """hyprutils isNumber (integers only): optional leading '-', then digits."""
    if not s:
        return False
    for i, c in enumerate(s):
        if i == 0 and c == "-":
            continue
        if c not in "0123456789":
            return False
    return s[-1] in "0123456789"


def parse_key(key):
    """ConfigManager::parseKey -> (key, keycode, catchAll)."""
    if is_number(key) and int(key) > 9:
        return "", int(key), False
    if key.startswith("code:") and is_number(key[5:]):
        return "", int(key[5:]), False
    if key == "catchall":
        return "", 0, True
    return key, 0, False


def mod_mask(mods):
    """KeybindManager::stringToModMask: uppercase, then substring tests."""
    u = mods.upper()
    mask = 0
    if "SHIFT" in u:
        mask |= 1
    if "CAPS" in u:
        mask |= 2
    if "CTRL" in u or "CONTROL" in u:
        mask |= 4
    if "ALT" in u or "MOD1" in u:
        mask |= 8
    if "MOD2" in u:
        mask |= 16
    if "MOD3" in u:
        mask |= 32
    if "SUPER" in u or "WIN" in u or "LOGO" in u or "MOD4" in u or "META" in u:
        mask |= 64
    if "MOD5" in u:
        mask |= 128
    return mask


def truthy(s):
    if s == "1":
        return True
    if s == "0":
        return False
    low = s.lower()
    return low.startswith("true") or low.startswith("yes") or low.startswith("on")


# ---------------------------------------------------------------------------
# binary32: hyprlang evaluates an expression in float and splices the result in
# with std::format("{}", value).  Both halves of that are reproduced here: IEEE
# binary32 + - * / with x86 default-NaN results, and to_chars' shortest general
# rendering (the fewest-character string that round-trips).
# ---------------------------------------------------------------------------

_F32 = struct.Struct("<f")
_U32 = struct.Struct("<I")
INF = float("inf")
# 0.0f / 0.0f and the other invalid operations on x86 yield the default QNaN,
# whose sign bit is set; std::format then prints "-nan".
QNAN = _F32.unpack(_U32.pack(0xFFC00000))[0]
PQNAN = _F32.unpack(_U32.pack(0x7FC00000))[0]


def bits_of(x):
    return _U32.unpack(_F32.pack(x))[0]


def from_bits(b):
    return _F32.unpack(_U32.pack(b))[0]


def _round_half_even(num, den):
    q, r = divmod(num, den)
    twice = 2 * r
    if twice > den or (twice == den and (q & 1)):
        q += 1
    return q


def frac_to_f32(fr):
    """Round an exact Fraction to the nearest binary32, ties to even."""
    if fr == 0:
        return 0.0
    neg = fr < 0
    if neg:
        fr = -fr
    num, den = fr.numerator, fr.denominator

    def ge_pow2(e):
        return num >= (den << e) if e >= 0 else (num << -e) >= den

    e = num.bit_length() - den.bit_length()
    if not ge_pow2(e):
        e -= 1
    while ge_pow2(e + 1):
        e += 1
    if e < -126:
        m = _round_half_even(num << 149, den)
        exp2 = -149
    else:
        if e >= 23:
            m = _round_half_even(num, den << (e - 23))
        else:
            m = _round_half_even(num << (23 - e), den)
        exp2 = e - 23
    if m == (1 << 24):
        m = 1 << 23
        exp2 += 1
    if exp2 + 23 > 127:
        return -INF if neg else INF
    val = math.ldexp(float(m), exp2)
    return -val if neg else val


def _decade(fr):
    """An integer near floor(log10(fr)) + 1 for a positive Fraction."""
    x = len(str(fr.numerator)) - len(str(fr.denominator))
    approx = fr / (Fraction(10) ** x)
    while approx >= 1:
        approx /= 10
        x += 1
    while approx < Fraction(1, 10):
        approx *= 10
        x -= 1
    return x


def _render_candidate(d, p, x):
    digits = str(d)
    if x >= 0:
        if x + 1 >= p:
            fixed = digits + "0" * (x + 1 - p)
        else:
            fixed = digits[:x + 1] + "." + digits[x + 1:]
    else:
        fixed = "0." + "0" * (-x - 1) + digits
    mant = digits[0] + ("." + digits[1:] if p > 1 else "")
    sci = mant + "e" + ("+" if x >= 0 else "-") + "%02d" % abs(x)
    return fixed, sci


def _render_magnitude(value):
    """The shortest `std::format("{}", f)` text for a positive binary32 value.

    The rendering minimises its own character count over both the fixed and the
    scientific style and over every digit count whose decimal round-trips; ties go
    to the decimal closest to the value, then to an even last digit, then to the
    fixed style."""
    b = bits_of(value)
    v = Fraction(value)
    even = (b & 1) == 0
    prev = Fraction(from_bits(b - 1)) if b > 1 else Fraction(0)
    nxt = Fraction(2) ** 128 if b == 0x7F7FFFFF else Fraction(from_bits(b + 1))
    lo = (v + prev) / 2
    hi = (v + nxt) / 2
    decade = _decade(v)
    p_int = len(str(int(value))) if value == int(value) else 0
    best = None
    for p in range(1, min(40, max(10, p_int)) + 1):
        cand_best = None
        for k in range(decade - p - 1, decade - p + 3):
            scale = Fraction(10) ** k
            lod = lo / scale
            hid = hi / scale
            low = -((-lod.numerator) // lod.denominator)          # ceil(lo / scale)
            high = hid.numerator // hid.denominator               # floor(hi / scale)
            if not even:
                if Fraction(low) * scale == lo:
                    low += 1
                if Fraction(high) * scale == hi:
                    high -= 1
            low = max(low, 10 ** (p - 1))
            high = min(high, 10 ** p - 1)
            if low > high:
                continue
            target = v / scale
            guess = (2 * target.numerator + target.denominator) // (2 * target.denominator)
            for d in {low, high, min(max(guess, low), high),
                      min(max(guess - 1, low), high), min(max(guess + 1, low), high)}:
                cand = Fraction(d) * scale
                key = (abs(cand - v), d & 1, d)
                if cand_best is None or key < cand_best[0]:
                    cand_best = (key, d, k)
        if cand_best is None:
            continue
        (dist, parity, _d), d, k = cand_best
        fixed, sci = _render_candidate(d, p, k + p - 1)
        for rank, text in ((0, fixed), (1, sci)):
            key = (len(text), dist, parity, rank)
            if best is None or key < best[0]:
                best = (key, text)
    return best[1]


def fmt_f32(value):
    """std::format("{}", value) for a binary32 value held in a Python float."""
    bits = bits_of(value)
    neg = bool(bits & 0x80000000)
    expf = (bits >> 23) & 0xFF
    mant_field = bits & 0x7FFFFF
    sign = "-" if neg else ""
    if expf == 0xFF:
        return sign + ("nan" if mant_field else "inf")
    if expf == 0 and mant_field == 0:
        return sign + "0"
    return sign + _render_magnitude(-value if neg else value)


_C_SPACE = " \t\n\v\f\r"
_HEX_DIGITS = "0123456789abcdefABCDEF"


def _scan_float(s):
    """glibc strtof: (exact Fraction or None, kind, negative).

    kind is 'ok', 'inf', 'nan', 'invalid' or 'overflow'.  The longest numeric
    prefix is consumed; trailing text is ignored, as strtof does."""
    i = 0
    n = len(s)
    while i < n and s[i] in _C_SPACE:
        i += 1
    neg = False
    if i < n and s[i] in "+-":
        neg = s[i] == "-"
        i += 1
    low = s[i:i + 8].lower()
    if low.startswith("inf"):
        return INF, "inf", neg
    if low.startswith("nan"):
        return None, "nan", neg
    sign = -1 if neg else 1
    if i + 1 < n and s[i] == "0" and s[i + 1] in "xX":
        j = i + 2
        intpart = []
        fracpart = []
        seen = False
        while j < n and s[j] in _HEX_DIGITS:
            intpart.append(s[j])
            j += 1
            seen = True
        if j < n and s[j] == ".":
            j += 1
            while j < n and s[j] in _HEX_DIGITS:
                fracpart.append(s[j])
                j += 1
                seen = True
        if not seen:
            return Fraction(0), "ok", neg      # strtof falls back to the leading "0"
        exp2 = 0
        if j < n and s[j] in "pP":
            k = j + 1
            eneg = False
            if k < n and s[k] in "+-":
                eneg = s[k] == "-"
                k += 1
            start = k
            while k < n and s[k].isdigit():
                k += 1
            if k > start:
                exp2 = int(s[start:k]) * (-1 if eneg else 1)
        value = Fraction(0)
        for c in intpart:
            value = value * 16 + int(c, 16)
        scale = Fraction(1, 16)
        for c in fracpart:
            value += int(c, 16) * scale
            scale /= 16
        value *= Fraction(2) ** exp2
        return sign * value, "ok", neg
    intpart = []
    fracpart = []
    seen = False
    j = i
    while j < n and s[j].isdigit():
        intpart.append(s[j])
        j += 1
        seen = True
    if j < n and s[j] == ".":
        j += 1
        while j < n and s[j].isdigit():
            fracpart.append(s[j])
            j += 1
            seen = True
    if not seen:
        return None, "invalid", neg
    exp10 = 0
    if j < n and s[j] in "eE":
        k = j + 1
        eneg = False
        if k < n and s[k] in "+-":
            eneg = s[k] == "-"
            k += 1
        start = k
        while k < n and s[k].isdigit():
            k += 1
        if k > start:
            exp10 = int(s[start:k]) * (-1 if eneg else 1)
    value = Fraction(int("".join(intpart) or "0"))
    if fracpart:
        value += Fraction(int("".join(fracpart)), 10 ** len(fracpart))
    if exp10:
        try:
            value *= Fraction(10) ** exp10
        except OverflowError:
            return None, "overflow", neg
    return sign * value, "ok", neg


def stof(s):
    """std::stof: the binary32 value, or None where libstdc++ throws.

    libstdc++ throws std::invalid_argument when no conversion happens and
    std::out_of_range when strtof reports ERANGE: overflow to infinity, underflow
    to zero, and a subnormal result that is not exact."""
    val, kind, neg = _scan_float(s)
    if kind == "invalid" or kind == "overflow":
        return None
    if kind == "inf":
        return -INF if neg else INF
    if kind == "nan":
        return QNAN if neg else PQNAN
    result = frac_to_f32(val)
    if result in (INF, -INF):
        return None
    if result == 0:
        if val != 0:
            return None
        return -0.0 if neg else 0.0
    if abs(result) < 2.0 ** -126 and Fraction(abs(result)) != abs(val):
        return None
    return result


def arith(x, op, y):
    """IEEE binary32 `x op y`; invalid operations yield x86's default QNaN."""
    if x != x:
        return x
    if y != y:
        return y
    xneg = math.copysign(1.0, x) < 0
    yneg = math.copysign(1.0, y) < 0
    if op == "-":
        if math.isinf(x) or math.isinf(y):
            if math.isinf(x) and math.isinf(y) and xneg == yneg:
                return QNAN
            return x if math.isinf(x) else -y
        if x == 0 and y == 0:
            return -0.0 if (xneg and not yneg) else 0.0
        return frac_to_f32(Fraction(x) - Fraction(y))
    if op == "+":
        if math.isinf(x) or math.isinf(y):
            if math.isinf(x) and math.isinf(y) and xneg != yneg:
                return QNAN
            return x if math.isinf(x) else y
        if x == 0 and y == 0:
            return -0.0 if (xneg and yneg) else 0.0
        return frac_to_f32(Fraction(x) + Fraction(y))
    neg = xneg != yneg
    if op == "*":
        if math.isinf(x) or math.isinf(y):
            if x == 0 or y == 0:
                return QNAN
            return -INF if neg else INF
        if x == 0 or y == 0:
            return -0.0 if neg else 0.0
        return frac_to_f32(Fraction(x) * Fraction(y))
    if math.isinf(x):
        if math.isinf(y):
            return QNAN
        return -INF if neg else INF
    if y == 0:
        if x == 0:
            return QNAN
        return -INF if neg else INF
    if math.isinf(y):
        return -0.0 if neg else 0.0
    if x == 0:
        return -0.0 if neg else 0.0
    return frac_to_f32(Fraction(x) / Fraction(y))


# ---------------------------------------------------------------------------
# hyprlang `{{ ... }}` expressions
# ---------------------------------------------------------------------------


class ExprError(Exception):
    """A closed `{{...}}` pair that parseExpression rejected: the line is dropped."""


def strip_escapes(rhs):
    """hyprlang parseLine's escape pass, after the expression loop: `\\\\` -> `\\`,
    `\\{` -> `{`, `\\}` -> `}`, any other backslash kept, loop stops one char early."""
    out = list(rhs)
    i = 0
    while out and i < len(out) - 1:
        if out[i] != "\\":
            i += 1
            continue
        if out[i + 1] == "\\":
            del out[i]
            i += 1              # the for-loop this mirrors still runs its increment
            continue
        if out[i + 1] in "{}":
            del out[i]
            i -= 1
        i += 1
    return "".join(out)


def parse_expression(text, st):
    """hyprlang CConfigImpl::parseExpression: two operands and one operator.

    The split is CConstVarList(s, 0, 's', true): std::isspace delimiters, empty
    tokens dropped, every token trimmed.  Tokens past index 2 are ignored."""
    if not text:
        raise ExprError("Expression is empty")
    args = text.split()
    op = at(args, 1)
    if op not in ("+", "-", "*", "/"):
        raise ExprError("Invalid expression type: supported +, -, *, /")
    operands = []
    for idx in (0, 2):
        token = at(args, idx)
        value = None
        for name, stored in st.variables:
            if name == token:
                value = stof(stored)
                if value is None:
                    raise ExprError("Failed to parse expression: value 1 holds a "
                                    "variable that does not look like a number")
                break
        else:
            value = stof(token)
            if value is None:
                raise ExprError("Failed to parse expression: value 1 does not look "
                                "like a number or the variable doesn't exist")
        operands.append(value)
    return arith(operands[0], op, operands[1])


def expand_expressions(rhs, st):
    """The `while (RHS.contains("{{"))` loop of parseLine: every pair with an even
    number of preceding backslashes is evaluated left to right; an unclosed pair
    stops the scan and stays literal."""
    while "{{" in rhs:
        begin = rhs.find("{{")
        while begin > 0:
            skipped = 0
            i = begin - 1
            while i >= 0 and rhs[i] == "\\":
                skipped += 1
                i -= 1
            if skipped % 2 == 0:
                break
            begin = rhs.find("{{", begin + 1)
            if begin == -1:
                break
        if begin == -1:
            break
        end = rhs.find("}}", begin + 2)
        if end == -1:
            break
        rhs = rhs[:begin] + fmt_f32(parse_expression(rhs[begin + 2:end], st)) + rhs[end + 2:]
    return rhs


class State:
    __slots__ = ("home", "variables", "entries", "categories", "ifs", "submap")

    def __init__(self, home):
        self.home = home
        self.variables = []
        self.entries = []
        self.categories = []
        self.ifs = []
        self.submap = ""

    def get_var(self, name):
        for k, v in self.variables:
            if k == name:
                return v
        return None

    def set_var(self, name, value):
        for i, (k, _) in enumerate(self.variables):
            if k == name:
                self.variables[i] = (name, value)
                return
        self.variables.append((name, value))
        self.variables.sort(key=lambda kv: -len(kv[0]))


def parse_comment(text, st):
    """`# hyprlang ...` directives: noerror (no effect here), if/endif nesting."""
    comment = trim(text)
    if not comment.startswith("hyprlang"):
        return
    args = comment.split()
    var = None
    for i in range(1, len(args)):
        if args[i] == "noerror":
            return
        if args[i] == "endif":
            if st.ifs:
                st.ifs.pop()
            return
        if args[i] == "if":
            var = args[i + 1] if i + 1 < len(args) else ""
            break
    if var:
        negated = var.startswith("!")
        if negated:
            var = var[1:]
        value = st.get_var(var)
        if value is None:
            failed = not negated
        else:
            failed = truthy(value) if negated else not truthy(value)
        st.ifs.append(failed)


def handle_bind(lhs, value, st):
    """ConfigManager::handleBind: one bind keyword line, already expanded."""
    flags = lhs[4:]
    locked = release = repeat = mouse = noncons = autocon = False
    transparent = ignoremods = multikey = longpress = hasdesc = False
    dontinhibit = click = drag = submapu = perdevice = allowcap = False
    for c in flags:
        if c == "l":
            locked = True
        elif c == "r":
            release = True
        elif c == "e":
            repeat = True
        elif c == "m":
            mouse = True
        elif c == "n":
            noncons = True
        elif c == "a":
            autocon = True
        elif c == "t":
            transparent = True
        elif c == "i":
            ignoremods = True
        elif c == "s":
            multikey = True
        elif c == "o":
            longpress = True
        elif c == "d":
            hasdesc = True
        elif c == "p":
            dontinhibit = True
        elif c == "c":
            click = True
            release = True
        elif c == "g":
            drag = True
            release = True
        elif c == "u":
            submapu = True
        elif c == "k":
            perdevice = True
        elif c == "x":
            allowcap = True
        else:
            return  # invalid flag: the whole line is rejected

    if (longpress or release) and repeat:
        return
    if mouse and (repeat or release or locked):
        return
    if click and drag:
        return

    dd = 1 if hasdesc else 0
    dev = 1 if perdevice else 0
    args = cvarlist(value, 4 + dd + dev)
    if len(args) < 3:
        return
    if (not mouse and len(args) > 4 + dd + dev) or (mouse and len(args) > 3 + dd + dev):
        return

    mask = mod_mask(args[0])
    modstr = args[0]
    key = "" if multikey else at(args, 1)
    description = at(args, 2 + dev) if hasdesc else ""
    handler = at(args, 2 + dd + dev)
    command = handler if mouse else at(args, 3 + dd + dev)
    if mouse:
        handler = "mouse"
    handler = handler.lower()
    if handler not in DISPATCHERS:
        return
    if mask == 0 and modstr != "":
        return
    if not key and not multikey:
        return
    parsed, keycode, catchall = parse_key(key)
    if catchall and not st.submap:
        return

    st.entries.append({
        "locked": locked,
        "mouse": mouse,
        "release": release,
        "repeat": repeat,
        "longPress": longpress,
        "non_consuming": noncons,
        "auto_consuming": autocon,
        "has_description": hasdesc,
        "modmask": mask,
        "submap": st.submap,
        "submap_universal": "true" if submapu else "false",
        "key": parsed,
        "keycode": keycode,
        "catch_all": catchall,
        "description": description,
        "allow_input_capture": allowcap,
        "dispatcher": handler,
        "arg": command,
    })


def handle_unbind(value, st):
    """ConfigManager::handleUnbind + KeybindManager::removeKeybind: exact key string."""
    args = cvarlist(value)
    if len(args) == 1 and args[0] == "all":
        st.entries = []
        return
    mask = mod_mask(at(args, 0))
    key, keycode, catchall = parse_key(at(args, 1))
    st.entries = [
        e for e in st.entries
        if not (e["modmask"] == mask and e["key"] == key and e["keycode"] == keycode
                and e["catch_all"] == catchall)
    ]


def handle_submap(value, st):
    first = at(cvarlist(value), 0)
    st.submap = "" if first == "reset" else first


def absolute_path(rawpath, current_path):
    """helpers::absolutePath: leading '~' is replaced by HOME, else relative paths
    join the directory of the file being parsed."""
    idx = current_path.rfind("/")
    current_dir = current_path if idx == -1 else current_path[:idx]
    if rawpath[:1] == "~":
        return HOME[0] + rawpath[1:]
    if rawpath[:1] == "/":
        return rawpath
    if rawpath[:1] == ".":
        if rawpath[1:3] == "../":
            idx = current_dir.rfind("/")
            parent_dir = current_dir if idx == -1 else current_dir[:idx]
            return parent_dir + rawpath[2:]
        if rawpath[1:2] == "/":
            return current_dir + rawpath[1:]
    return current_dir + "/" + rawpath


HOME = [""]


def handle_source(rawpath, st, current_path):
    if len(rawpath) < 2:
        return
    pattern = absolute_path(rawpath, current_path)
    for match in sorted(glob.glob(pattern)):
        value = absolute_path(match, current_path)
        try:
            mode = os.stat(value).st_mode
        except OSError:
            return  # inaccessible glob result: the remaining matches are skipped
        if not stat.S_ISREG(mode):
            continue
        parse_file(value, st)


def parse_line(line, st, current_path):
    """hyprlang parseLine over one logical line."""
    line = trim(line)
    pos = line.find("#")
    if pos == 0:
        parse_comment(line[1:], st)
        return
    if st.ifs and st.ifs[-1]:
        return
    last_hash = 0
    while pos != -1:
        if pos + 1 < len(line) and line[pos + 1] == "#":
            last_hash = pos + 2
            line = line[:pos + 1] + line[pos + 2:]
            pos = line.find("#", last_hash)
        else:
            line = line[:pos]
            break
    line = trim(line)
    if not line:
        return
    equals = line.find("=")
    if equals == -1 and not line.endswith("{") and line != "}":
        return  # invalid config line
    if equals != -1:
        lhs = trim(line[:equals])
        rhs = trim(line[equals + 1:])
        if not lhs:
            return
        is_variable = lhs[0] == "$"
        for iteration in range(100):
            matched = False
            for name, val in st.variables:
                needle = "$" + name
                if not is_variable and needle in lhs:
                    lhs = lhs.replace(needle, val)
                    matched = True
                if needle in rhs:
                    rhs = rhs.replace(needle, val)
                    matched = True
            try:
                rhs = expand_expressions(rhs, st)
            except ExprError:
                return  # hyprlang rejects the line; the value and handler are skipped
            if not matched:
                break
            if iteration == 99:
                return  # "Expanding variables exceeded max iteration limit"
        if is_variable:
            st.set_var(lhs[1:], rhs)
            return
        rhs = strip_escapes(rhs)
        if lhs == "unbind":
            handle_unbind(rhs, st)
        elif lhs == "submap":
            handle_submap(rhs, st)
        elif lhs == "source":
            handle_source(rhs, st, current_path)
        elif lhs.startswith("bind") and ":" not in lhs:
            handle_bind(lhs, rhs, st)
        return
    if "}" in line:
        if line != "}":
            return
        if st.categories:
            st.categories.pop()
        return
    if not line.endswith("{"):
        return
    st.categories.append(trim(line[:-1]))


def parse_file(path, st):
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except OSError:
        return
    lines = data.decode("utf-8", "replace").split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        idx += 1
        joined = True
        while line.endswith("\\"):
            cut = len(line) - 2
            while cut >= 0 and line[cut] in " \t":
                cut -= 1
            line = line[:cut + 1]
            if idx >= len(lines):
                joined = False
                break
            line += lines[idx]
            idx += 1
        if not joined:
            break
        parse_line(line, st, path)
    # hyprlang clears the category stack at the end of every parsed file
    st.categories = []


def main(argv):
    home = None
    i = 1
    while i < len(argv):
        arg = argv[i]
        if arg == "--home" and i + 1 < len(argv):
            home = argv[i + 1]
            i += 2
            continue
        if arg.startswith("--home="):
            home = arg[len("--home="):]
        i += 1
    if not home:
        sys.stderr.write("usage: mado-binds.py --home DIR\n")
        return 2
    HOME[0] = os.path.abspath(home)
    st = State(HOME[0])
    root = os.path.join(HOME[0], ".config", "hypr", "hyprland.conf")
    if os.path.exists(root):
        parse_file(os.path.realpath(root), st)
    sys.stdout.write(json.dumps(st.entries))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

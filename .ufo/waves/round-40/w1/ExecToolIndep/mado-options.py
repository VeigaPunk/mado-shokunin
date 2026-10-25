#!/usr/bin/env python3
"""mado-options.py - static resolver of the config-tree option table.

Collects every *general option statement* of a Hyprland config tree - a
`key = value` line that is not a handler keyword (bind and its flag variants
such as bindd/bindeld, env/gesture variants, animation, workspace,
windowrule, exec, monitor, bezier, layerrule, source, ...) and does not sit
inside a keyed special category (windowrule/layerrule/device/monitorv2/
plugin blocks) - by walking the `source =`
graph of DIR/.config/hypr/hyprland.conf depth-first in line order, then
resolves the LAST declarer per key across layers (defaults tree, user files,
toggles glob, ai-usage.conf, theme, root) with the owner file + line and a
layer label.  Prints one JSON array of rows `{key, value, owner, layer, line,
set}` to stdout and exits 0.

Modes
-----
`mado-options.py --home DIR`            static table only (default).
`mado-options.py --home DIR --getoption FILE`
                                        merges a live `hyprctl getoption`
                                        JSON mapping (key -> {value,
                                        custom_type, set}) and adds an
                                        `agreement` field per row using the
                                        lane's divergence vocabulary:
                                          agreement     live == resolved decl,
                                                       set=true, one declarer
                                          agreement*    same, but an earlier
                                                       declarer is shadowed
                                          mismatch      live != resolved decl or
                                                       set=false despite a
                                                       declarer
                                          config-only   declared; no live row
                                                       (hyprctl has no surface)
                                          live-default  live row with no
                                                       declarer; set=false
`mado-options.py --home DIR --live [--hyprctl PATH] [--probe KEY ...]`
                                        asks the running compositor directly:
                                        one `hyprctl getoption -j KEY` per
                                        declared key through the compositor's
                                        own read verb, plus one per `--probe`
                                        key (repeatable; a probe has no
                                        declarer, so a live answer for it is a
                                        `live-default` row).  `--hyprctl PATH`
                                        selects the program (default:
                                        `hyprctl` on PATH).  Every row that
                                        met a reply also carries that reply's
                                        native value in `live` (a
                                        `config-only` row has no reply and so
                                        no `live`).  The reply is one
                                        JSON object `{"option": K, "set": B,
                                        "<form>": V}` with form in int | float
                                        | str | custom (HyprCtl.cpp:1700-1721;
                                        the typed variants bool/vec2/gradient/
                                        css/font_weight are accepted too), or
                                        the text `no such option` (exit 0 from
                                        hyprctl; the key keeps `config-only`).
`mado-options.py --selftest`             writes ephemeral fixtures under a
                                        private temp dir and runs a copy of
                                        itself as a child process; must pass
                                        >40 assertions (prints
                                        `MADO_OPTIONS_SELFTEST: k/n passed`).

Live comparison model (`--live`)
--------------------------------
The declared value is the last declarer's text after the tree's own passes
(variable expansion, `{{ expr }}`, escapes); the live value is compared in
the compositor's native form, converted the way the compositor converted the
declaration:
  * int    hyprlang v0.6.8 `configStringToInt` (src/config.cpp:185-264):
           `0x` hex, `rgba(r,g,b,a)` (comma form, alpha*255 rounded; 8-digit
           hex RGBA->ARGB), `rgb(...)` (comma form / 6-digit hex), the
           true/on/yes and false/off/no prefixes, else an integer literal
           (`isNumber` with allowfloat=false, then stoll);
  * float  `std::stof` (hyprlang config.cpp:463-470): leading float literal;
  * str    exact text;
  * custom dispatch on the reply's own shape, mirroring the handler that
           produced it (Hyprland v0.56.2 ConfigManager.cpp:104-215):
             * text ending in `deg` -> gradient: each colour token parsed by
               `ParserUtils::parseColor`, printed lowercase unpadded ARGB hex,
               then the angle (`CGradientValueData::toString`,
               ComplexDataTypes.hpp:69-76).  The handler clears the colours
               but sets the angle only when a token carries `deg`
               (ConfigManager.cpp:114-136), so a gradient redeclared without
               an angle token inherits the last angle of an earlier declarer
               of the same key (0 when none declared one);
             * four integer tokens -> CSS gap expansion (`CCssGapData::
               parseGapData`, ComplexDataTypes.hpp:105-129): 1 value repeats,
               2 = vertical horizontal, 3 = top horizontal bottom;
             * one token -> font weight (`CFontWeightConfigValueData::
               WEIGHTS`, ComplexDataTypes.hpp:158-176): name lookup
               (case-insensitive) or the number, out of 100..1000 -> 400;
             * anything else -> exact text.
  A compositor failure (program missing, non-zero exit, a reply that is
  neither `no such option` nor one JSON object with a known form and `set`)
  is a NAMED failure: exit 5, the failing key on stderr.  A hostile `--probe`
  key (not `[A-Za-z0-9_.:]+`, or leading `-`) is a usage error: exit 2 and no
  program is run.

Strict policy
-------------
Every file opened must be a regular file (symlinks are followed; the *target*
must be regular).  A missing root, a non-regular file, an unresolved `source =`
(no glob match), or a glob match that is not a regular file is a NAMED failure
on stderr - never a silent skip.  The config read path uses no compositor,
socket, network or subprocess; `--live` is the only path that runs a program,
and it runs exactly `hyprctl getoption -j KEY` per key.  Python stdlib only.

Exit map: 0 OK; 2 usage error (including a hostile `--probe` key); 3 named
config-read failure; 4 --getoption file malformed/unreadable; 5 named
compositor failure under `--live` (the failing key is on stderr); 1 failed
--selftest.

Value comparison for `agreement` (documented, deterministic):
  * `--live` uses the native-form model above;
  * `--getoption FILE`: custom_type int/float: numeric equality via float()
    when the declared value parses, else the boolean/string fallbacks below;
  * declared boolean spellings true/yes/on/1 and false/no/off/0 compare equal
    to live "1"/"0"/"true"/"false" of any type;
  * a declared scalar equals a live whitespace-separated tuple whose tokens
    are all that scalar (e.g. declared `0` vs live `0 0 0 0`);
  * otherwise exact string equality after trimming.

Layers are derived from resolved paths relative to DIR: the root file
(.config/hypr/hyprland.conf), defaults tree (.local/share/omarchy/default/
hypr/), theme (.config/omarchy/current/theme/), user files
(.config/hypr/), toggles glob (.local/state/omarchy/toggles/hypr/), and
ai-usage.conf (basename); anything else is `other`.  `~` expands to DIR.
"""

import argparse
import glob
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile

WS = " \t\n\r\v\f"

# Native reply forms of `hyprctl getoption -j` (HyprCtl.cpp:1700-1721): the
# generic four the compositor emits for its registered option types, then the
# typed variants of the same JSON shape (Config::BOOL, VEC2, and the three
# IComplexConfigValue subclasses registered with their own typeid).
LIVE_FORMS = (
    "int", "float", "str", "custom",
    "bool", "vec2", "gradient", "css", "font_weight",
)
# A probe key is an option name: category and field words joined by `:`.
# Anything outside this class (whitespace, quotes, `$`, `;`, `/`, a leading
# `-`, an empty string) is refused before any program runs.
PROBE_KEY = re.compile(r"[A-Za-z0-9_.:]+")
# C++ stoi/stoll front end: optional sign, digits, trailing text ignored.
INT_HEAD = re.compile(r"[+-]?\d+")
# C++ std::stof front end (decimal form only).
FLOAT_HEAD = re.compile(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?")
# hyprlang `isNumber(VALUE, allowfloat=false)` (hyprutils String.cpp:50-82).
INT_LITERAL = re.compile(r"-?\d+")
# Font weight names (Hyprland v0.56.2 ComplexDataTypes.hpp:159-163).
WEIGHTS = {
    "thin": 100, "ultralight": 200, "light": 300, "semilight": 350,
    "book": 380, "normal": 400, "medium": 500, "semibold": 600,
    "bold": 700, "ultrabold": 800, "heavy": 900, "ultraheavy": 1000,
}

# Handler keywords registered by the host's Hyprland (0.56.2, commit efb5099,
# src/config/legacy/ConfigManager.cpp:601-623); hyprlang tries a registered
# option first and only then a handler (hyprlang v0.6.8 src/config.cpp:832-874), so
# an unscoped handler is excluded by exact trimmed-lhs match (an option key
# such as `binding` inside a category is kept).
EXCLUDED = frozenset((
    "source", "bind", "binds", "bindl", "bindr", "bindm", "binde",
    "bindn", "bindd", "unbind", "unmap", "submap", "animation", "bezier",
    "workspace", "windowrule", "windowrulev2", "exec", "exec-once",
    "monitor", "env", "layerrule", "layerrulev2", "execr", "execr-once",
    "exec-shutdown", "plugin", "permission", "gesture",
))
# Handlers registered with allowFlags=true (bind, gesture, env): any
# top-level lhs that starts with the name and holds no `:` is that handler
# with flags (hyprlang v0.6.8 src/config.cpp:869), e.g. `bindeld`, `bindmd`, `envd`.
FLAG_HANDLERS = ("bind", "gesture", "env")
# Keyed special categories (ConfigManager.cpp:518, 567, 591, 595, 626): their
# fields are per-instance rule/device data, never global options.
SPECIAL_CATEGORIES = frozenset((
    "device", "monitorv2", "windowrule", "layerrule", "plugin",
))


def is_directive(lhs, categories):
    if lhs in EXCLUDED:
        return True
    if categories and categories[0] in SPECIAL_CATEGORIES:
        return True
    if not categories and ":" not in lhs:
        return any(lhs.startswith(h) for h in FLAG_HANDLERS)
    return False


class Failure(Exception):
    """A named read/policy failure (exit 3/4)."""
class LiveError(Exception):
    """A named --getoption read/schema failure (exit 4)."""
class CompositorError(Exception):
    """A named --live compositor failure (exit 5), always keyed."""


class ExprError(Exception):
    """A closed `{{...}}` pair that parseExpression rejected."""


def trim(s):
    return s.strip(WS)


def fmt_num(v):
    """Render a float expression result short and round-trippable."""
    if v != v:
        return "nan"
    if v == float("inf"):
        return "inf"
    if v == float("-inf"):
        return "-inf"
    if v == int(v) and abs(v) < 1e17:
        return str(int(v))
    return repr(v)


def expand_expressions(rhs):
    """`{{ expr }}` - one binary float operator, C-ish semantics."""
    while "{{" in rhs:
        begin = -1
        position = 0
        while True:
            candidate = rhs.find("{{", position)
            if candidate < 0:
                break
            backslashes = 0
            for k in range(candidate - 1, -1, -1):
                if rhs[k] != "\\":
                    break
                backslashes += 1
            if backslashes % 2 == 0:
                begin = candidate
                break
            position = candidate + 1
        if begin < 0:
            break
        end = rhs.find("}}", begin + 2)
        if end < 0:
            break
        body = rhs[begin + 2:end]
        args = [a for a in body.split() if a]
        if len(args) < 3 or args[1] not in ("+", "-", "*", "/"):
            raise ExprError("Invalid expression")
        try:
            left = float(args[0])
            right = float(args[2])
            if args[1] == "+":
                result = left + right
            elif args[1] == "-":
                result = left - right
            elif args[1] == "*":
                result = left * right
            elif right == 0:
                if left == 0:
                    result = float("nan")
                else:
                    result = float("inf") if left > 0 else float("-inf")
            else:
                result = left / right
        except (ValueError, OverflowError):
            raise ExprError("Invalid expression operand")
        rhs = rhs[:begin] + fmt_num(result) + rhs[end + 2:]
    return rhs


def strip_escapes(rhs):
    r"""`\` -> `\`, `\{` -> `{`, `\}` -> `}` (hyprlang escape pass)."""
    out = []
    i = 0
    n = len(rhs)
    while i < n:
        ch = rhs[i]
        if ch == "\\" and i + 1 < n:
            following = rhs[i + 1]
            if following in "\\{}":
                out.append(following)
                i += 2
                continue
        out.append(ch)
        i += 1
    return "".join(out)


def absolute_path(rawpath, current_path, home):
    """Helpers::absolutePath: `~` -> home, relative joins the file's dir."""
    idx = current_path.rfind("/")
    current_dir = current_path if idx == -1 else current_path[:idx]
    if rawpath[:1] == "~":
        return home + rawpath[1:]
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


def read_bytes(path):
    """Strict regular-file read: follow symlinks, refuse everything else."""
    try:
        mode = os.stat(path).st_mode
    except OSError as exc:
        raise Failure("%s: %s" % (path, exc.strerror or exc))
    if not stat.S_ISREG(mode):
        raise Failure("%s: not a regular file" % path)
    try:
        with open(path, "rb") as handle:
            return handle.read()
    except OSError as exc:
        raise Failure("%s: %s" % (path, exc.strerror or exc))


def layer_of(path, home):
    """Label a resolved path with its config layer."""
    if os.path.basename(path) == "ai-usage.conf":
        return "ai-usage"
    rel = path
    if path.startswith(home + "/"):
        rel = path[len(home) + 1:]
    if rel == ".config/hypr/hyprland.conf":
        return "root"
    if rel.startswith(".config/hypr/"):
        return "user"
    if rel.startswith(".local/share/omarchy/default/hypr/"):
        return "defaults"
    if rel.startswith(".local/state/omarchy/toggles/hypr/"):
        return "toggles"
    if rel.startswith(".config/omarchy/current/theme/"):
        return "theme"
    return "other"


class State:
    __slots__ = ("home", "variables", "options", "categories", "ifs",
                 "descent")

    def __init__(self, home):
        self.home = home
        self.variables = []
        self.options = {}
        self.categories = []
        self.ifs = []
        self.descent = []

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

    def declare(self, key, value, path, lineno):
        layer = layer_of(path, self.home)
        owner = path
        if path.startswith(self.home + "/"):
            owner = path[len(self.home) + 1:]
        prev = self.options.get(key)
        if prev is None:
            self.options[key] = {
                "key": key, "value": value, "owner": owner, "layer": layer,
                "line": lineno, "set": True, "_decls": 1,
                "_history": [value],
            }
        else:
            prev["value"] = value
            prev["owner"] = owner
            prev["layer"] = layer
            prev["line"] = lineno
            prev["_decls"] += 1
            prev["_history"].append(value)


def truthy(s):
    low = s.lower()
    return s == "1" or low.startswith("true") or low.startswith("yes") \
        or low.startswith("on")


def parse_comment(text, st):
    """`# hyprlang ...` directives: noerror (no effect), if/endif nesting."""
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


def handle_source(rawpath, st, current_path):
    if len(rawpath) < 2:
        raise Failure("source= path garbage")
    pattern = absolute_path(rawpath, current_path, st.home)
    matches = sorted(glob.glob(pattern))
    if not matches:
        raise Failure("source = %s: no matches for %s" % (rawpath, pattern))
    for match in matches:
        value = absolute_path(match, current_path, st.home)
        real = os.path.realpath(value)
        if real in st.descent:
            raise Failure("recursive source: %s" % value)
        st.descent.append(real)
        try:
            parse_file(value, st)
        finally:
            st.descent.pop()


def parse_line(line, st, current_path, lineno):
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
    if equals == -1:
        if line == "}":
            if st.categories:
                st.categories.pop()
            return
        if line.endswith("{"):
            st.categories.append(trim(line[:-1]))
        return
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
            rhs = expand_expressions(rhs)
        except ExprError:
            return  # hyprlang rejects the line; value is skipped
        if not matched:
            break
        if iteration == 99:
            return  # "Expanding variables exceeded max iteration limit"
    if is_variable:
        st.set_var(lhs[1:], rhs)
        return
    rhs = strip_escapes(rhs)
    if lhs == "source":
        handle_source(rhs, st, current_path)
        return
    if is_directive(lhs, st.categories):
        return
    key = ":".join(st.categories + [lhs]) if st.categories else lhs
    st.declare(key, rhs, current_path, lineno)


def parse_file(path, st):
    data = read_bytes(path)
    lines = data.decode("utf-8", "replace").split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    base = len(st.categories)
    idx = 0
    while idx < len(lines):
        lineno = idx + 1
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
        parse_line(line, st, path, lineno)
    # hyprlang scopes are per-file: restore the parent's category stack
    del st.categories[base:]


def values_equal(custom_type, declared, live):
    ds = declared.strip()
    ls = str(live).strip()
    if custom_type in ("int", "float"):
        try:
            return float(ds) == float(ls)
        except ValueError:
            pass
    lo = ls.lower()
    if lo in ("true", "false") and ds in ("0", "1"):
        return (lo == "true") == (ds == "1")
    if ds.lower() in ("true", "yes", "on", "1") and lo in ("true", "1", "yes", "on"):
        return True
    if ds.lower() in ("false", "no", "off", "0") and lo in ("false", "0", "no", "off"):
        return True
    # scalar-vs-tuple: "0" == "0 0 0 0", "a" == "a a"
    if ds and not ds.isspace() and " " in ls and set(ls.split()) == {ds}:
        return True
    return ds == ls


# ---------------------------------------------------------------------------
# --live: native-form conversion (hyprlang v0.6.8 / Hyprland v0.56.2)
# ---------------------------------------------------------------------------

def _stoi(text, default=None):
    """C++ std::stoi front end: sign + digits, trailing text ignored."""
    found = INT_HEAD.match(text.strip())
    if not found:
        return default
    return int(found.group(0))


def _hex_number(text):
    """hyprutils parseHex: the whole string is one base-16 integer."""
    body = text[2:] if text[:2] in ("0x", "0X") else text
    if not re.fullmatch(r"[0-9a-fA-F]+", body):
        return None
    return int(body, 16)


def hl_int(value):
    """hyprlang v0.6.8 `configStringToInt` (src/config.cpp:185-264).

    Returns the int the compositor stores, or None where hyprlang rejects the
    declaration (the option then keeps its previous value)."""
    v = value.strip()
    if v.startswith("0x"):
        return _hex_number(v)
    if v.startswith("rgba(") and v.endswith(")"):
        inner = v[5:-1].strip()
        if inner.count(",") == 3:
            parts = [p.strip() for p in inner.split(",")]
            red, green, blue = hl_int(parts[0]), hl_int(parts[1]), hl_int(parts[2])
            if red is None or green is None or blue is None:
                return None
            try:
                alpha = float(parts[3])
            except ValueError:
                return None
            alpha = alpha * 255.0
            # std::round: half away from zero
            alpha = int(alpha + 0.5) if alpha >= 0 else -int(-alpha + 0.5)
            alpha &= 0xFF  # uint8_t
            return alpha * 0x1000000 + red * 0x10000 + green * 0x100 + blue
        if len(inner) == 8:
            rgba = _hex_number(inner)
            if rgba is None:
                return None
            return (rgba >> 8) + 0x1000000 * (rgba & 0xFF)
        return None
    if v.startswith("rgb(") and v.endswith(")"):
        inner = v[4:-1].strip()
        if inner.count(",") == 2:
            parts = [p.strip() for p in inner.split(",")]
            red, green, blue = hl_int(parts[0]), hl_int(parts[1]), hl_int(parts[2])
            if red is None or green is None or blue is None:
                return None
            return 0xFF000000 + red * 0x10000 + green * 0x100 + blue
        if len(inner) == 6:
            rgb = _hex_number(inner)
            if rgb is None:
                return None
            return rgb + 0xFF000000
        return None
    if v.startswith(("true", "on", "yes")):
        return 1
    if v.startswith(("false", "off", "no")):
        return 0
    if not INT_LITERAL.fullmatch(v):
        return None
    return int(v)


def hl_float(value):
    """hyprlang `CONFIGDATATYPE_FLOAT`: `std::stof(value)` (config.cpp:463-470)."""
    found = FLOAT_HEAD.match(value.strip())
    if not found:
        return None
    return float(found.group(0))


def parse_color(token):
    """`ParserUtils::parseColor` (ParserUtils.cpp:23-152) -> ARGB int or None."""
    v = token
    if v.startswith("#"):
        body = v[1:]
        if len(body) == 3:
            try:
                red, green, blue = (int(ch, 16) for ch in body)
            except ValueError:
                return None
            return 0xFF000000 | ((red | (red << 4)) << 16) \
                | ((green | (green << 4)) << 8) | (blue | (blue << 4))
        if len(body) in (6, 8):
            if not re.fullmatch(r"[0-9a-fA-F]+", body):
                return None
            red, green, blue = int(body[0:2], 16), int(body[2:4], 16), int(body[4:6], 16)
            if len(body) == 6:
                return 0xFF000000 | (red << 16) | (green << 8) | blue
            return (int(body[6:8], 16) << 24) | (red << 16) | (green << 8) | blue
        return None
    if v.startswith("0x"):
        return _hex_number(v)
    if v.startswith("rgba(") and v.endswith(")"):
        inner = v[5:-1].strip()
        if inner.count(",") == 3:
            parts = [p.strip() for p in inner.split(",")]
            try:
                red, green, blue = (int(p, 10) for p in parts[:3])
                alpha = float(parts[3])
            except ValueError:
                return None
            if not (0 <= red < 256 and 0 <= green < 256 and 0 <= blue < 256):
                return None
            # floor(*a * 255.F) into the alpha byte
            return ((int(alpha * 255.0) & 0xFF) << 24) | (red << 16) | (green << 8) | blue
        if len(inner) == 8:
            rgba = _hex_number(inner)
            if rgba is None:
                return None
            return (rgba >> 8) + 0x1000000 * (rgba & 0xFF)
        return None
    if v.startswith("rgb(") and v.endswith(")"):
        inner = v[4:-1].strip()
        if inner.count(",") == 2:
            parts = [p.strip() for p in inner.split(",")]
            try:
                red, green, blue = (int(p, 10) for p in parts)
            except ValueError:
                return None
            if not (0 <= red < 256 and 0 <= green < 256 and 0 <= blue < 256):
                return None
            return 0xFF000000 | (red << 16) | (green << 8) | blue
        if len(inner) == 6:
            rgb = _hex_number(inner)
            return None if rgb is None else rgb + 0xFF000000
        return None
    if INT_LITERAL.fullmatch(v):
        return int(v)
    return None


def gradient_angle(history):
    """The angle the gradient handler kept after `history` declarations.

    `configHandleGradientSet` clears the colours on every declaration but
    assigns `m_angle` only for a token holding `deg` (ConfigManager.cpp:114-136),
    so the last declaration that carried an angle wins; 0 when none did."""
    angle = 0
    for value in history:
        for token in str(value).split():
            cut = token.find("deg")
            if cut == -1:
                continue
            angle = _stoi(token[:cut], angle)
            break
    return angle


def gradient_text(declared, angle):
    """`CGradientValueData::toString` (ComplexDataTypes.hpp:69-76)."""
    colors = []
    for token in declared.split():
        if "deg" in token:
            angle = _stoi(token[:token.find("deg")], angle)
            break
        if len(colors) >= 10:
            break
        color = parse_color(token)
        if color is None:
            continue
        colors.append(color)
    if not colors:
        colors.append(0)  # the handler stores transparent
    return "".join("%x " % color for color in colors) + "%ddeg" % angle


def gap_text(declared):
    """`CCssGapData::parseGapData` + toString (ComplexDataTypes.hpp:105-145)."""
    values = []
    for token in declared.split()[:4]:
        value = _stoi(token)
        if value is None:
            return None
        values.append(value)
    if not values:
        return None
    if len(values) == 1:
        top = right = bottom = left = values[0]
    elif len(values) == 2:
        top = bottom = values[0]
        right = left = values[1]
    elif len(values) == 3:
        top, right, bottom = values
        left = values[1]
    else:
        top, right, bottom, left = values
    return "%d %d %d %d" % (top, right, bottom, left)


def font_weight_text(declared):
    """`CFontWeightConfigValueData::parseWeight` + toString (hpp:154-176)."""
    text = declared.strip()
    named = WEIGHTS.get(text.lower())
    if named is not None:
        return str(named)
    value = _stoi(text)
    if value is None:
        return None
    if value < 100 or value > 1000:
        value = 400
    return str(value)


def _as_int(value):
    if isinstance(value, bool):
        return 1 if value else 0
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    try:
        return int(str(value).strip())
    except ValueError:
        return None


def _as_float(value):
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).strip())
    except ValueError:
        return None


def custom_equal(declared, live, history):
    """Compare a declared value to a `custom` reply by the reply's own shape."""
    text = live.strip()
    if text.endswith("deg"):
        return gradient_text(declared, gradient_angle(history)) == text
    parts = text.split()
    if len(parts) == 4 and all(INT_LITERAL.fullmatch(p) for p in parts):
        want = gap_text(declared)
        return want is not None and want == text
    if len(parts) == 1:
        want = font_weight_text(declared)
        return want is not None and want == text
    return text == declared.strip()


def native_equal(record, declared, history):
    """Does `declared` (after the compositor's own conversion) equal `record`?"""
    form = record["form"]
    live = record["value"]
    if form in ("int", "bool"):
        want = hl_int(declared)
        if want is None:
            return values_equal(form, declared, live)
        got = _as_int(live)
        return got is not None and got == want
    if form == "float":
        want = hl_float(declared)
        got = _as_float(live)
        return want is not None and got is not None and want == got
    if form == "str":
        return declared.strip() == str(live).strip()
    if form == "custom":
        return custom_equal(declared, str(live), history)
    if form == "gradient":
        return gradient_text(declared, gradient_angle(history)) == str(live).strip()
    if form == "css":
        return gap_text(declared) == str(live).strip()
    if form == "font_weight":
        return font_weight_text(declared) == str(live).strip()
    if form == "vec2":
        return values_equal("float", declared, live)
    return False


def probe_is_safe(key):
    """A probe key is an option name, nothing a program could be tricked by."""
    return bool(PROBE_KEY.fullmatch(key)) and not key.startswith("-")


def run_getoption(program, key):
    """One read-only `hyprctl getoption -j KEY`; the reply text or exit 5."""
    try:
        proc = subprocess.run(
            [program, "getoption", "-j", key],
            capture_output=True, text=True, errors="replace",
        )
    except OSError as exc:
        raise CompositorError("%s: cannot run %s: %s"
                              % (key, program, exc.strerror or exc))
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip().splitlines()
        raise CompositorError("%s: %s getoption -j exited %d%s"
                              % (key, program, proc.returncode,
                                 (": " + detail[0]) if detail else ""))
    return proc.stdout


def native_record(key, text):
    """Parse one native reply: a record, None for `no such option`, or exit 5."""
    raw = text.strip()
    if not raw:
        raise CompositorError("%s: empty getoption reply" % key)
    if raw == "no such option":
        return None
    try:
        obj = json.loads(raw)
    except ValueError as exc:
        raise CompositorError("%s: getoption reply is not JSON: %s" % (key, exc))
    if not isinstance(obj, dict):
        raise CompositorError("%s: getoption reply is not a JSON object" % key)
    form = None
    for name in LIVE_FORMS:
        if name in obj:
            form = name
            break
    if form is None:
        raise CompositorError("%s: getoption reply carries no native form" % key)
    if "set" not in obj:
        raise CompositorError("%s: getoption reply lacks `set`" % key)
    return {"form": form, "value": obj[form], "set": bool(obj["set"])}


def read_live(program, rows, probes):
    """One getoption per declared key (sorted) and per new probe, in order."""
    keys = [row["key"] for row in rows]
    seen = set(keys)
    for key in probes:
        if key not in seen:
            keys.append(key)
            seen.add(key)
    live = {}
    for key in keys:
        record = native_record(key, run_getoption(program, key))
        if record is not None:
            live[key] = record
    return live


def merge_live_rows(rows, options, live):
    """The `--getoption` label vocabulary over native-form replies.

    Each row that met a live reply also carries that reply's native value in
    `live`; a `config-only` row has no reply and therefore no `live`."""
    seen = set()
    for row in rows:
        seen.add(row["key"])
        record = live.get(row["key"])
        if record is None:
            row["agreement"] = "config-only"
            continue
        row["live"] = record["value"]
        history = options[row["key"]].get("_history") or [row["value"]]
        equal = native_equal(record, row["value"], history)
        if not record["set"] or not equal:
            row["agreement"] = "mismatch"
        elif options[row["key"]]["_decls"] > 1:
            row["agreement"] = "agreement*"
        else:
            row["agreement"] = "agreement"
    for key, record in live.items():
        if key in seen:
            continue
        rows.append({
            "key": key, "value": str(record["value"]), "owner": None,
            "layer": None, "line": None, "set": record["set"],
            "live": record["value"], "agreement": "live-default",
        })
    rows.sort(key=lambda r: r["key"])


def load_live(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError) as exc:
        raise LiveError("%s: cannot load getoption JSON: %s" % (path, exc))
    if not isinstance(data, dict):
        raise LiveError("%s: getoption JSON root must be an object" % path)
    live = {}
    for key, rec in data.items():
        if not isinstance(rec, dict):
            raise LiveError("%s: entry for %r is not an object" % (path, key))
        if "value" not in rec or "custom_type" not in rec or "set" not in rec:
            raise LiveError("%s: entry for %r lacks value/custom_type/set"
                            % (path, key))
        live[key] = rec
    return live


def merge_rows(rows, options, live):
    seen = set()
    for row in rows:
        seen.add(row["key"])
        rec = live.get(row["key"])
        if rec is None:
            row["agreement"] = "config-only"
            continue
        equal = values_equal(rec.get("custom_type"), row["value"],
                             rec.get("value"))
        if not bool(rec.get("set")) or not equal:
            row["agreement"] = "mismatch"
        elif options[row["key"]]["_decls"] > 1:
            row["agreement"] = "agreement*"
        else:
            row["agreement"] = "agreement"
    for key, rec in live.items():
        if key not in seen:
            rows.append({
                "key": key, "value": str(rec.get("value")), "owner": None,
                "layer": None, "line": None, "set": bool(rec.get("set")),
                "agreement": "live-default",
            })
    rows.sort(key=lambda r: r["key"])


def run_static(st):
    rows = []
    for key in sorted(st.options):
        o = st.options[key]
        rows.append({
            "key": key, "value": o["value"], "owner": o["owner"],
            "layer": o["layer"], "line": o["line"], "set": True,
        })
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="mado-options.py",
        description="Static resolver of the config-tree option table.",
    )
    parser.add_argument("--home", metavar="DIR", help="config root (DIR/.config/hypr/hyprland.conf)")
    live_group = parser.add_mutually_exclusive_group()
    live_group.add_argument("--getoption", metavar="FILE", default=None,
                            help="live hyprctl getoption JSON (key -> {value, custom_type, set})")
    live_group.add_argument("--live", action="store_true",
                            help="ask the compositor with `hyprctl getoption -j KEY` per key")
    parser.add_argument("--hyprctl", metavar="PATH", default=None,
                        help="hyprctl program for --live (default: hyprctl on PATH)")
    parser.add_argument("--probe", metavar="KEY", action="append", default=[],
                        help="extra live key with no declarer (repeatable; implies --live)")
    parser.add_argument("--selftest", action="store_true",
                        help="run the hermetic selftest and exit")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()

    if args.probe:
        args.live = True
    for key in args.probe:
        if not probe_is_safe(key):
            sys.stderr.write("mado-options.py: hostile probe key %r refused\n" % key)
            return 2

    if not args.home:
        parser.print_usage(sys.stderr)
        sys.stderr.write("mado-options.py: error: --home DIR is required\n")
        return 2
    home = os.path.abspath(args.home)
    root = os.path.join(home, ".config", "hypr", "hyprland.conf")
    st = State(home)
    try:
        parse_file(root, st)
        rows = run_static(st)
        if args.live:
            program = args.hyprctl or shutil.which("hyprctl") or "hyprctl"
            live = read_live(program, rows, args.probe)
            merge_live_rows(rows, st.options, live)
        elif args.getoption:
            live = load_live(args.getoption)
            merge_rows(rows, st.options, live)
    except CompositorError as exc:
        sys.stderr.write("mado-options.py: %s\n" % exc)
        return 5
    except LiveError as exc:
        sys.stderr.write("mado-options.py: %s\n" % exc)
        return 4
    except Failure as exc:
        sys.stderr.write("mado-options.py: %s\n" % exc)
        return 3
    sys.stdout.write(json.dumps(rows))
    sys.stdout.write("\n")
    return 0


# ---------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------

def _check(checks, desc, cond):
    checks.append((desc, bool(cond)))
    return bool(cond)


def _run(script, tmp, args):
    return subprocess.run(
        [sys.executable, "-I", script] + args,
        capture_output=True, text=True, cwd=tmp,
    )


def _write(root, rel, content):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)
    return path


def selftest():
    tmp = tempfile.mkdtemp(prefix="mado-options-st-")
    checks = []
    try:
        home = os.path.join(tmp, "home")
        os.makedirs(home)
        script = os.path.join(tmp, "mado-options-copy.py")
        shutil.copyfile(sys.argv[0], script)

        # ---- fixture tree ------------------------------------------------
        _write(home, ".config/hypr/hyprland.conf", """\
# orchestrator: no own settings except the misc block below
source = ~/.local/share/omarchy/default/hypr/looknfeel.conf
source = ~/.local/share/omarchy/default/hypr/input.conf
source = ~/.config/omarchy/current/theme/hyprland.conf
source = ~/.config/hypr/looknfeel.conf
source = ~/.config/hypr/input.conf
source = ~/.local/state/omarchy/toggles/hypr/*.conf
source = ~/.config/hypr/ai-usage.conf
source = ~/.config/hypr/gkeep.conf

# directive verbs that must never enter the option table
bind = SUPER, Q, exec, kitty
unbind = SUPER, Q
submap = reset
animation = windowsIn, 1, 3, popin, 80%
bezier = overshot, 0.13, 0.99, 0.29, 1.1
monitor = DP-1, 3440x1440@100, 0x0, 1
env = XCURSOR_SIZE,24
exec-once = uwsm-app -- hypridle
workspace = 1, monitor:DP-1, default:true
windowrulev2 = opacity 0.92 0.92, class:^(kitty)$
bindd = SUPER, X, Launch foot, exec, foot
bindeld = , XF86AudioMute, Mute, exec, wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle
bindmd = SUPER, mouse:273, Resize window, resizewindow
envd = QT_QPA_PLATFORM,wayland
gesture = 3, horizontal, workspace
windowrule {
    name = moonlight
    match:class = com.moonlight_stream.Moonlight
    fullscreen = 1
}
device {
    name = some-mouse
    sensitivity = -0.5
}

misc {
    disable_autoreload = true
}
""")
        _write(home, ".local/share/omarchy/default/hypr/looknfeel.conf", """\
# defaults tree: variables, categories, shadows, inspection, continuation
$activeBorderColor = rgba(33ccffee) rgba(00ff99ee) 45deg
$long = alpha \\
    beta
general {
    gaps_in = 5
    gaps_out = 10
    border_size = 2
    col.active_border = $activeBorderColor
    col.inactive_border = rgba(595959aa) # trailing comment dropped
    resize_on_border = false
    allow_tearing = false
    layout = dwindle
    gap_test = $long
    inactive_gap = $activeBorderColor
}
decoration {
    rounding = 8
    shadow {
        enabled = true
        color = ##000000
    }
}
dwindle {
    preserve_split = true
}
group {
    groupbar {
        font_size = 12
    }
}
source = ./parts/*.conf
source = sub/deep.conf
""")
        _write(home, ".local/share/omarchy/default/hypr/parts/a.conf", """\
general {
    smart_gaps = 1
}
""")
        _write(home, ".local/share/omarchy/default/hypr/parts/z.conf", """\
general {
    smart_gaps = 2
}
""")
        _write(home, ".local/share/omarchy/default/hypr/sub/deep.conf", """\
decoration {
    blur {
        enabled = true
    }
}
""")
        _write(home, ".local/share/omarchy/default/hypr/input.conf", """\
input {
    kb_layout = us
    kb_options = compose:caps
    touchpad {
        natural_scroll = false
    }
}
misc {
    key_press_enables_dpms = true
}
""")
        _write(home, ".config/omarchy/current/theme/hyprland.conf", """\
general {
    col.active_border = rgb(e68e0d)
}
""")
        _write(home, ".config/hypr/looknfeel.conf", """\
# user overrides (some inert)
general {
    # gaps_out = 0 0 0 0
    layout = dwindle
}
decoration {
    # rounding = 0
}
source = ~/.config/hypr/extra.conf
misc {
    deep_value = 1
}
""")
        _write(home, ".config/hypr/extra.conf", """\
misc {
    deep_value = 2
}
""")
        _write(home, ".config/hypr/input.conf", """\
$r = 40
input {
    kb_layout = br
    repeat_rate = $r
}
cursor {
    no_hardware_cursors = {{1 + 1}}
}
""")
        _write(home, ".local/state/omarchy/toggles/hypr/window-no-gaps.conf", """\
# enabled toggle: the last declarer for these keys
general {
    gaps_in = 0
    gaps_out = 0
    border_size = 0
}
decoration {
    rounding = 0
}
""")
        _write(home, ".local/state/omarchy/toggles/hypr/flags.conf", """\
# comment-only toggle placeholder
""")
        _write(home, ".config/hypr/ai-usage.conf", """\
windowrule = match:class com.mitchellh.ghostty, scroll_touchpad 0.2
decoration {
    rounding = 0
    shadow {
        range = 4
    }
}
""")
        _write(home, ".config/hypr/gkeep.conf", """\
windowrule = opacity 0.9 0.9, class:^(org.omarchy.ai-usage)$
workspace = 5, monitor:DP-2
exec-once = uwsm-app -- waybar
general {
    # gaps_in = 7
}
""")

        # ---- static run --------------------------------------------------
        run = _run(script, tmp, ["--home", home])
        _check(checks, "static: exit 0", run.returncode == 0)
        try:
            rows = json.loads(run.stdout)
        except ValueError as exc:
            _check(checks, "static: stdout parses as JSON (%s)" % exc, False)
            rows = []
        _check(checks, "static: stdout is a JSON array", isinstance(rows, list))

        by_key = {r["key"]: r for r in rows}
        expected_keys = set((
            "general:gaps_in", "general:gaps_out", "general:border_size",
            "general:col.active_border", "general:col.inactive_border",
            "general:resize_on_border", "general:allow_tearing",
            "general:layout", "general:gap_test", "general:inactive_gap",
            "general:smart_gaps",
            "decoration:rounding", "decoration:shadow:enabled",
            "decoration:shadow:color", "decoration:blur:enabled",
            "decoration:shadow:range",
            "dwindle:preserve_split", "group:groupbar:font_size",
            "input:kb_layout", "input:kb_options",
            "input:touchpad:natural_scroll",
            "misc:key_press_enables_dpms", "misc:disable_autoreload",
            "misc:deep_value", "input:repeat_rate",
            "cursor:no_hardware_cursors",
        ))
        got_keys = set(by_key)
        _check(checks, "static: exact key set",
               got_keys == expected_keys)
        _check(checks, "static: all directive verbs excluded",
               not (got_keys & set((
                   "bind", "unbind", "submap", "animation", "bezier",
                   "monitor", "env", "exec-once", "workspace",
                   "windowrule", "windowrulev2",
               ))))
        _check(checks, "static: flag-variant handlers excluded",
               not (got_keys & set(("bindd", "bindeld", "bindmd", "envd",
                                    "gesture"))))
        _check(checks, "static: special-category fields excluded",
               not any(k.split(":")[0] in ("windowrule", "device")
                       for k in got_keys))

        def row_of(key):
            return by_key.get(key)

        # last declarer ownership
        r = row_of("general:gaps_out")
        _check(checks, "gaps_out: owner is toggle file",
               r and r["owner"] == ".local/state/omarchy/toggles/hypr/window-no-gaps.conf")
        _check(checks, "gaps_out: layer toggles", r and r["layer"] == "toggles")
        _check(checks, "gaps_out: value 0", r and r["value"] == "0")
        _check(checks, "gaps_out: line 4", r and r["line"] == 4)
        _check(checks, "gaps_out: set true", r and r["set"] is True)

        r = row_of("general:border_size")
        _check(checks, "border_size: toggle owner", r and r["owner"] == ".local/state/omarchy/toggles/hypr/window-no-gaps.conf")
        _check(checks, "border_size: value 0", r and r["value"] == "0")

        r = row_of("input:kb_layout")
        _check(checks, "kb_layout: user owner", r and r["owner"] == ".config/hypr/input.conf")
        _check(checks, "kb_layout: layer user", r and r["layer"] == "user")
        _check(checks, "kb_layout: value br", r and r["value"] == "br")

        r = row_of("decoration:rounding")
        _check(checks, "rounding: ai-usage owner",
               r and r["owner"] == ".config/hypr/ai-usage.conf")
        _check(checks, "rounding: layer ai-usage", r and r["layer"] == "ai-usage")
        _check(checks, "rounding: value 0", r and r["value"] == "0")

        r = row_of("decoration:shadow:range")
        _check(checks, "shadow range: ai-usage owner",
               r and r["owner"] == ".config/hypr/ai-usage.conf")
        _check(checks, "shadow range: value 4", r and r["value"] == "4")

        r = row_of("misc:disable_autoreload")
        _check(checks, "root option: owner root", r and r["owner"] == ".config/hypr/hyprland.conf")
        _check(checks, "root option: layer root", r and r["layer"] == "root")

        r = row_of("general:layout")
        _check(checks, "layout: user owner (shadows default)",
               r and r["owner"] == ".config/hypr/looknfeel.conf")
        _check(checks, "layout: value dwindle", r and r["value"] == "dwindle")

        r = row_of("misc:deep_value")
        _check(checks, "depth-first: later line of parent wins",
               r and r["owner"] == ".config/hypr/looknfeel.conf")
        _check(checks, "depth-first: value 1", r and r["value"] == "1")

        r = row_of("general:smart_gaps")
        _check(checks, "glob sorted: z.conf last wins (2)",
               r and r["value"] == "2")
        _check(checks, "glob sorted: owner parts/z.conf",
               r and r["owner"] == ".local/share/omarchy/default/hypr/parts/z.conf")

        r = row_of("general:col.active_border")
        _check(checks, "theme overrides col.active_border",
               r and r["owner"] == ".config/omarchy/current/theme/hyprland.conf")
        _check(checks, "theme layer", r and r["layer"] == "theme")
        _check(checks, "theme value", r and r["value"] == "rgb(e68e0d)")
        r = row_of("general:inactive_gap")
        _check(checks, "var expansion in defaults",
               r and r["value"] == "rgba(33ccffee) rgba(00ff99ee) 45deg")
        r = row_of("general:gap_test")
        _check(checks, "continuation: value words",
               r and r["value"].split() == ["alpha", "beta"])
        r = row_of("decoration:shadow:color")
        _check(checks, "## escape: value #000000",
               r and r["value"] == "#000000")
        r = row_of("general:col.inactive_border")
        _check(checks, "trailing comment dropped",
               r and r["value"] == "rgba(595959aa)")
        r = row_of("input:repeat_rate")
        _check(checks, "variable in user file", r and r["value"] == "40")
        r = row_of("cursor:no_hardware_cursors")
        _check(checks, "expression {{1+1}} -> 2", r and r["value"] == "2")
        r = row_of("input:touchpad:natural_scroll")
        _check(checks, "nested category key", r and r["key"] == "input:touchpad:natural_scroll")
        _check(checks, "nested category value", r and r["value"] == "false")

        # ---- strict-policy failures ---------------------------------------
        bad_src = _write(home, ".config/hypr/hyprland.conf", """\
source = ~/.config/hypr/notadir.conf
""")
        os.makedirs(os.path.join(home, ".config/hypr/notadir.conf"))
        run = _run(script, tmp, ["--home", home])
        _check(checks, "strict: source -> directory fails", run.returncode == 3)
        _check(checks, "strict: directory named on stderr",
               "notadir.conf" in run.stderr)

        os.unlink(bad_src)
        _write(home, ".config/hypr/hyprland.conf", """\
source = ~/.config/hypr/missing.conf
""")
        run = _run(script, tmp, ["--home", home])
        _check(checks, "strict: unresolved source fails", run.returncode == 3)
        _check(checks, "strict: unresolved named", "missing.conf" in run.stderr)

        os.unlink(os.path.join(home, ".config/hypr/hyprland.conf"))
        os.makedirs(os.path.join(home, ".config/hypr/hyprland.conf"))
        run = _run(script, tmp, ["--home", home])
        _check(checks, "strict: root directory fails", run.returncode == 3)
        os.rmdir(os.path.join(home, ".config/hypr/hyprland.conf"))

        os.makedirs(os.path.join(home, ".config/hypr/hyprland.conf.tmp"), exist_ok=True)
        _write(home, ".config/hypr/hyprland.conf.tmp/real.conf",
               "misc {\n    x = 1\n}\n")
        os.symlink(os.path.join(home, ".config/hypr/hyprland.conf.tmp/real.conf"),
                    os.path.join(home, ".config/hypr/hyprland.conf"))
        run = _run(script, tmp, ["--home", home])
        _check(checks, "strict: root symlink -> regular file works",
               run.returncode == 0)
        try:
            rows = json.loads(run.stdout)
        except ValueError:
            rows = []
        _check(checks, "strict: symlinked root parses",
               any(r["key"] == "misc:x" for r in rows))
        os.unlink(os.path.join(home, ".config/hypr/hyprland.conf"))

        os.symlink("dangling-target.conf",
                    os.path.join(home, ".config/hypr/hyprland.conf"))
        run = _run(script, tmp, ["--home", home])
        _check(checks, "strict: broken symlink root fails", run.returncode == 3)

        os.unlink(os.path.join(home, ".config/hypr/hyprland.conf"))
        empty_home = os.path.join(tmp, "homeempty")
        os.makedirs(empty_home)
        run = _run(script, tmp, ["--home", empty_home])
        _check(checks, "strict: missing root fails", run.returncode == 3)

        _write(home, ".config/hypr/hyprland.conf", """\
source = ~/.config/hypr/mix/*
""")
        os.makedirs(os.path.join(home, ".config/hypr/mix/dir"))
        _write(home, ".config/hypr/mix/f.conf", "misc { y = 1 }\n")
        run = _run(script, tmp, ["--home", home])
        _check(checks, "strict: glob with directory match fails", run.returncode == 3)
        _check(checks, "strict: directory glob match named", "dir" in run.stderr)

        # ---- getoption merge ----------------------------------------------
        _write(home, ".config/hypr/hyprland.conf", """\
source = ~/.local/share/omarchy/default/hypr/looknfeel.conf
source = ~/.local/share/omarchy/default/hypr/input.conf
source = ~/.config/omarchy/current/theme/hyprland.conf
source = ~/.config/hypr/looknfeel.conf
source = ~/.config/hypr/input.conf
source = ~/.local/state/omarchy/toggles/hypr/*.conf
source = ~/.config/hypr/ai-usage.conf
source = ~/.config/hypr/gkeep.conf
misc {
    disable_autoreload = true
}
""")
        live_file = _write(tmp, "live.json", json.dumps({
            "general:gaps_out": {"value": "0 0 0 0", "custom_type": "custom", "set": True},
            "general:border_size": {"value": "0", "custom_type": "int", "set": True},
            "general:layout": {"value": "dwindle", "custom_type": "str", "set": True},
            "input:kb_layout": {"value": "br", "custom_type": "str", "set": True},
            "decoration:rounding": {"value": "0", "custom_type": "int", "set": True},
            "misc:disable_autoreload": {"value": "1", "custom_type": "int", "set": True},
            "input:repeat_rate": {"value": "40", "custom_type": "int", "set": True},
            "decoration:shadow:enabled": {"value": "1", "custom_type": "int", "set": True},
            "general:allow_tearing": {"value": "1", "custom_type": "int", "set": True},
            "dwindle:preserve_split": {"value": "0", "custom_type": "int", "set": True},
            "misc:key_press_enables_dpms": {"value": "0", "custom_type": "int", "set": False},
            "input:accel_profile": {"value": "[[EMPTY]]", "custom_type": "str", "set": False},
            "cursor:no_warps": {"value": "0", "custom_type": "int", "set": False},
        }))
        run = _run(script, tmp, ["--home", home, "--getoption", live_file])
        _check(checks, "merge: exit 0", run.returncode == 0)
        try:
            rows = json.loads(run.stdout)
        except ValueError:
            _check(checks, "merge: stdout parses as JSON", False)
            rows = []
        merged = {r["key"]: r for r in rows}
        _check(checks, "merge: agreement* for gaps_out",
               merged.get("general:gaps_out", {}).get("agreement") == "agreement*")
        _check(checks, "merge: agreement* for kb_layout",
               merged.get("input:kb_layout", {}).get("agreement") == "agreement*")
        _check(checks, "merge: agreement* for rounding",
               merged.get("decoration:rounding", {}).get("agreement") == "agreement*")
        _check(checks, "merge: agreement for single declarer",
               merged.get("input:repeat_rate", {}).get("agreement") == "agreement")
        _check(checks, "merge: agreement with truthy normalize",
               merged.get("misc:disable_autoreload", {}).get("agreement") == "agreement")
        _check(checks, "merge: agreement shadow enabled (bool 1)",
               merged.get("decoration:shadow:enabled", {}).get("agreement") == "agreement")
        _check(checks, "merge: mismatch allow_tearing",
               merged.get("general:allow_tearing", {}).get("agreement") == "mismatch")
        _check(checks, "merge: mismatch preserve_split",
               merged.get("dwindle:preserve_split", {}).get("agreement") == "mismatch")
        _check(checks, "merge: mismatch unset-but-declared",
               merged.get("misc:key_press_enables_dpms", {}).get("agreement") == "mismatch")
        _check(checks, "merge: config-only present",
               merged.get("group:groupbar:font_size", {}).get("agreement") == "config-only")
        ld1 = merged.get("input:accel_profile")
        _check(checks, "merge: live-default row exists", ld1 is not None)
        _check(checks, "merge: live-default agreement",
               ld1 and ld1["agreement"] == "live-default")
        _check(checks, "merge: live-default set false",
               ld1 and ld1["set"] is False)
        _check(checks, "merge: live-default no owner",
               ld1 and ld1["owner"] is None)
        ld2 = merged.get("cursor:no_warps")
        _check(checks, "merge: second live-default", ld2 and ld2["agreement"] == "live-default")
        _check(checks, "merge: rows sorted by key",
               [r["key"] for r in rows] == sorted(r["key"] for r in rows))

        run = _run(script, tmp, ["--home", home, "--getoption",
                                  os.path.join(tmp, "nope.json")])
        _check(checks, "merge: missing getoption file fails", run.returncode == 4)
        bad_live = _write(tmp, "bad.json", "[1,2,3]")
        run = _run(script, tmp, ["--home", home, "--getoption", bad_live])
        _check(checks, "merge: non-object getoption fails", run.returncode == 4)

        # ---- --live (stub compositor) --------------------------------------
        def stub(name, body):
            path = _write(tmp, name, body)
            os.chmod(path, 0o755)
            return path

        stub_map = stub("hyprctl-stub.py", """#!/usr/bin/env python3
import json, os, sys
here = os.path.abspath(sys.argv[0])
with open(here + ".log", "a", encoding="utf-8") as log:
    log.write(" ".join(sys.argv[1:]) + "\\n")
with open(here + ".map", encoding="utf-8") as handle:
    table = json.load(handle)
key = sys.argv[-1]
if key not in table:
    sys.stdout.write("no such option\\n")
    sys.exit(0)
sys.stdout.write(json.dumps(table[key]) + "\\n")
""")
        _write(tmp, "hyprctl-stub.py.map", json.dumps({
            "general:gaps_in": {"option": "general:gaps_in", "custom": "0 0 0 0", "set": True},
            "general:border_size": {"option": "general:border_size", "int": 0, "set": True},
            "general:col.active_border": {"option": "general:col.active_border",
                                          "custom": "ffe68e0d 45deg", "set": True},
            "general:layout": {"option": "general:layout", "str": "dwindle", "set": True},
            "general:allow_tearing": {"option": "general:allow_tearing", "int": 1, "set": True},
            "input:kb_layout": {"option": "input:kb_layout", "str": "br", "set": True},
            "input:repeat_rate": {"option": "input:repeat_rate", "int": 40, "set": True},
            "input:touchpad:natural_scroll": {"option": "input:touchpad:natural_scroll",
                                              "int": 0, "set": True},
            "misc:disable_autoreload": {"option": "misc:disable_autoreload", "int": 1, "set": True},
            "misc:key_press_enables_dpms": {"option": "misc:key_press_enables_dpms",
                                            "int": 0, "set": False},
            "input:accel_profile": {"option": "input:accel_profile", "str": "[[EMPTY]]", "set": False},
        }))
        log = stub_map + ".log"

        def snapshot(root):
            files = {}
            for base, _, names in os.walk(root):
                for name in names:
                    path = os.path.join(base, name)
                    with open(path, "rb") as handle:
                        files[os.path.relpath(path, root)] = handle.read()
            return files

        before = snapshot(home)
        run = _run(script, tmp, ["--home", home, "--live", "--hyprctl", stub_map,
                                 "--probe", "input:accel_profile"])
        _check(checks, "live: exit 0", run.returncode == 0)
        try:
            rows = json.loads(run.stdout)
        except ValueError:
            _check(checks, "live: stdout parses as JSON", False)
            rows = []
        live_rows = {r["key"]: r for r in rows}

        static_run = _run(script, tmp, ["--home", home])
        try:
            declared = [r["key"] for r in json.loads(static_run.stdout)]
        except ValueError:
            declared = []
        expected_argv = ["getoption -j " + key for key in declared]
        expected_argv.append("getoption -j input:accel_profile")
        try:
            with open(log, encoding="utf-8") as handle:
                got_argv = [line.rstrip("\n") for line in handle]
        except OSError:
            got_argv = []
        _check(checks, "live: exact argv, one getoption per declared key then probe",
               got_argv == expected_argv)

        _check(checks, "live: gap custom agreement* (declared 0)",
               live_rows.get("general:gaps_in", {}).get("agreement") == "agreement*")
        _check(checks, "live: int agreement* (declared 0)",
               live_rows.get("general:border_size", {}).get("agreement") == "agreement*")
        _check(checks, "live: gradient inherits the angle (rgb(e68e0d) -> ffe68e0d 45deg)",
               live_rows.get("general:col.active_border", {}).get("agreement") == "agreement*")
        _check(checks, "live: str agreement* (declared dwindle)",
               live_rows.get("general:layout", {}).get("agreement") == "agreement*")
        _check(checks, "live: str agreement (declared br)",
               live_rows.get("input:kb_layout", {}).get("agreement") == "agreement*")
        _check(checks, "live: int agreement (declared 40)",
               live_rows.get("input:repeat_rate", {}).get("agreement") == "agreement")
        _check(checks, "live: bool spelling true -> int 1",
               live_rows.get("misc:disable_autoreload", {}).get("agreement") == "agreement")
        _check(checks, "live: bool spelling false -> int 0",
               live_rows.get("input:touchpad:natural_scroll", {}).get("agreement") == "agreement")
        _check(checks, "live: int mismatch (declared false, live 1)",
               live_rows.get("general:allow_tearing", {}).get("agreement") == "mismatch")
        _check(checks, "live: set=false is a mismatch",
               live_rows.get("misc:key_press_enables_dpms", {}).get("agreement") == "mismatch")
        _check(checks, "live: no such option keeps config-only",
               live_rows.get("general:inactive_gap", {}).get("agreement") == "config-only")
        probe_row = live_rows.get("input:accel_profile")
        _check(checks, "live: probe with no declarer is live-default",
               probe_row is not None and probe_row["agreement"] == "live-default")
        _check(checks, "live: probe row has no owner",
               probe_row is not None and probe_row["owner"] is None)
        _check(checks, "live: a met reply is kept in `live`",
               live_rows.get("general:border_size", {}).get("live") == 0)
        _check(checks, "live: a custom reply keeps its native text",
               live_rows.get("general:col.active_border", {}).get("live")
               == "ffe68e0d 45deg")
        _check(checks, "live: a config-only row carries no live",
               "live" not in live_rows.get("general:inactive_gap", {}))
        _check(checks, "live: config root unchanged", snapshot(home) == before)

        run = _run(script, tmp, ["--home", home, "--live", "--hyprctl",
                                 os.path.join(tmp, "no-such-hyprctl")])
        _check(checks, "live: missing program exits 5", run.returncode == 5)
        _check(checks, "live: missing program names the key",
               "cursor:no_hardware_cursors" in run.stderr)

        failing = stub("hyprctl-fail.py", """#!/usr/bin/env python3
import sys
sys.stderr.write("compositor unavailable\\n")
sys.exit(1)
""")
        run = _run(script, tmp, ["--home", home, "--live", "--hyprctl", failing])
        _check(checks, "live: non-zero getoption exits 5", run.returncode == 5)
        _check(checks, "live: non-zero getoption names the key",
               "cursor:no_hardware_cursors" in run.stderr)

        with open(log, "a", encoding="utf-8") as handle:
            handle.write("MARKER\n")
        run = _run(script, tmp, ["--home", home, "--live", "--hyprctl", stub_map,
                                 "--probe", "general:gaps_in; rm -rf /"])
        _check(checks, "live: hostile probe exits 2", run.returncode == 2)
        _check(checks, "live: hostile probe names the key",
               "rm -rf" in run.stderr)
        with open(log, encoding="utf-8") as handle:
            tail = [line.rstrip("\n") for line in handle][-1:]
        _check(checks, "live: hostile probe runs no program", tail == ["MARKER"])

        # ---- usage --------------------------------------------------------
        run = _run(script, tmp, [])
        _check(checks, "usage: no --home exits 2", run.returncode == 2)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    passed = sum(1 for _, ok in checks if ok)
    total = len(checks)
    sys.stdout.write("MADO_OPTIONS_SELFTEST: %d/%d passed\n" % (passed, total))
    for desc, ok in checks:
        if not ok:
            sys.stderr.write("selftest FAIL: %s\n" % desc)
    if passed < total or total <= 40:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

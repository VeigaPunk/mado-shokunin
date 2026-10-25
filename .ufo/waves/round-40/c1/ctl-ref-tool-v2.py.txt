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
`mado-options.py --home DIR --live [--hyprctl PATH] [--probe KEY]...`
                                        queries the RUNNING compositor and
                                        labels every row with the same
                                        vocabulary, comparing each declared
                                        value against the compositor's own
                                        native reply (see `Native replies`
                                        below).  `--hyprctl` names the program
                                        to run (default `hyprctl`); `--probe`
                                        is repeatable and adds live keys that
                                        no declarer owns (`live-default` when
                                        the compositor answers, dropped when it
                                        answers `no such option`); a probe that
                                        names a declared key is not queried
                                        twice.
`mado-options.py --selftest`             writes ephemeral fixtures under a
                                        private temp dir and runs a copy of
                                        itself as a child process; must pass
                                        >40 assertions (prints
                                        `MADO_OPTIONS_SELFTEST: k/n passed`).

Strict policy
-------------
Every file opened must be a regular file (symlinks are followed; the *target*
must be regular).  A missing root, a non-regular file, an unresolved `source =`
(no glob match), or a glob match that is not a regular file is a NAMED failure
on stderr - never a silent skip.  The read path uses no compositor, socket,
network or subprocess; the live path runs one program and opens no socket of
its own.  Python stdlib only.

Exit map: 0 OK; 2 usage error (including a hostile `--probe` key); 3 named
config-read failure; 4 --getoption file malformed/unreadable; 5 named --live
compositor failure; 1 failed --selftest.

Value comparison for `agreement` (--getoption, documented, deterministic):
  * custom_type int/float: numeric equality via float() when the declared
    value parses, else the boolean/string fallbacks below;
  * declared boolean spellings true/yes/on/1 and false/no/off/0 compare equal
    to live "1"/"0"/"true"/"false" of any type;
  * a declared scalar equals a live whitespace-separated tuple whose tokens
    are all that scalar (e.g. declared `0` vs live `0 0 0 0`);
  * otherwise exact string equality after trimming.

Native replies (`--live`)
-------------------------
The live path runs exactly one program - the compositor's own read verb - once
per key: `HYPRCTL getoption -j KEY` and nothing else.  Never `keyword`,
`dispatch`, `reload`, `setprop` or `--batch`, and the tool opens no socket of
its own.  Each reply is either

  * the plain text line `no such option` (exit 0): the compositor has no such
    option, so the row is `config-only`; or
  * one JSON object `{"option": K, "set": B, "<form>": V}` holding exactly one
    form out of `int`, `float`, `str`, `custom`, `vec2` - the forms the host
    answers with: the four first ones over its 70 declared option keys
    (`.ufo/waves/round-40/c1/native-capture.jsonl`), and `vec2` (a JSON array
    `[x,y]`) for 6 of the compositor's 353 options, none declared on this host
    (`.ufo/waves/round-40/c1/native-capture-all.jsonl`).  The text reply is
    parsed as JSON, so the compositor's spacing (`"set": true }`), its six
    decimal floats and any padding are irrelevant.

The declared value is converted the way the host converts it and compared with
V in its native form:

  int     hyprlang v0.6.8 src/config.cpp:185-264 `configStringToInt`:
          `0x` hex; `rgba(rrggbbaa)` (8 hex digits - the packed value shifted
          right by 8 with its low byte as alpha); `rgba(r,g,b,a)` (decimal
          channels, alpha in 0..1 scaled by 255 and rounded half away from
          zero, as C++ `std::round`); `rgb(rrggbb)`
          (0xff000000 | rgb); `rgb(r,g,b)` (decimal channels); the prefixes
          `true`/`on`/`yes` -> 1 and `false`/`off`/`no` -> 0; signed decimal
          integers.  Anything else never equals a live int.
  float   numeric equality within 1e-6.
  vec2    declared exactly `x y` (one space; hyprlang v0.6.8 config.cpp:474-486,
          `stof` each); equal when both components are within 1e-6 of the
          reply's pair.  A declaration with another shape never matches.
  str     exact equality after trimming.
  custom  by the shape of V (Hyprland v0.56.2 src/config/legacy/
          ConfigManager.cpp:103-170 gradient handler, and the toString of the
          gradient, CSS-gap and font-weight value types in src/config/shared/
          complex/ComplexDataTypes.hpp):
            gradient  `<hex> ... <N>deg` - every declared colour token becomes
                      one lowercase, unpadded ARGB hex word, followed by
                      `<N>deg` (`N` is the C++ `stoi` prefix of the `deg`
                      token: `45.5deg` reads 45).
            gap       `a b c d` - 1-4 declared integers expanded CSS-style
                      (1 -> all four; 2 -> vertical horizontal; 3 -> top
                      horizontal bottom; 4 -> top right bottom left).  Any
                      other count is not a gap and never matches.
            weight    `<N>` - a declared font-weight name, case-insensitive
                      (thin 100, ultralight 200, light 300, semilight 350,
                      book 380, normal 400, medium 500, semibold 600,
                      bold 700, ultrabold 800, heavy 900, ultraheavy 1000).

Angle inheritance: the host's gradient handler clears the colours on every
declaration but sets the angle only when a `deg` token is present, so a
gradient redeclared WITHOUT an angle keeps the angle the previous declarer
left in that option.  The comparison uses that inherited angle (0 when no
earlier declarer set one); a declaration that carries `deg` uses its own.
Observed on the host: the theme's single-colour
`col.active_border = rgb(e68e0d)` reads `ffe68e0d 45deg`, because the defaults
tree declared `rgba(33ccffee) rgba(00ff99ee) 45deg` first.

Labels under `--live` are the `--getoption` vocabulary plus a `live` field
holding the native value as text (`null` for `config-only`).

Failures: the compositor program missing, exiting non-zero, answering something
that is not JSON (other than `no such option`), or answering an object without
exactly one known form and a `set` field is a NAMED failure - exit 5 with the
key on stderr.  A probe key that is empty or starts with `-` is refused with
exit 2 before any program runs, so a hostile key never reaches argv.

Layers are derived from resolved paths relative to DIR: the root file
(.config/hypr/hyprland.conf), defaults tree (.local/share/omarchy/default/
hypr/), theme (.config/omarchy/current/theme/), user files
(.config/hypr/), toggles glob (.local/state/omarchy/toggles/hypr/), and
ai-usage.conf (basename); anything else is `other`.  `~` expands to DIR.
"""

import argparse
import glob
import json
import math
import os
import re
import shutil
import stat
import struct
import subprocess
import sys
import tempfile
import threading

WS = " \t\n\r\v\f"

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


def declared_angle(value):
    """The `<N>deg` token of a gradient declaration, else None.

    Hyprland's gradient handler (ConfigManager.cpp:103-170) takes the angle
    from the first token carrying `deg`; the rest of the value is not
    inspected for one.
    """
    for token in value.split():
        if "deg" in token:
            try:
                return stoi_prefix(token[:token.index("deg")])
            except ValueError:
                return None
    return None


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
        angle = declared_angle(value)
        prev = self.options.get(key)
        if prev is None:
            self.options[key] = {
                "key": key, "value": value, "owner": owner, "layer": layer,
                "line": lineno, "set": True, "_decls": 1,
                # gradient angle bookkeeping for --live: `_inherited` is the
                # angle the previous declarer left in the option, `_current`
                # the angle the compositor holds after this declaration.
                "_inherited": 0,
                "_current": 0 if angle is None else angle,
            }
        else:
            prev["value"] = value
            prev["owner"] = owner
            prev["layer"] = layer
            prev["line"] = lineno
            prev["_decls"] += 1
            prev["_inherited"] = prev["_current"]
            if angle is not None:
                prev["_current"] = angle


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


# ---------------------------------------------------------------------------
# live path: one `hyprctl getoption -j KEY` per key, compared natively
# ---------------------------------------------------------------------------

class CtlError(Exception):
    """A named --live compositor failure (exit 5)."""


FORMS = ("int", "float", "str", "custom", "vec2")

# Font-weight names -> the number Hyprland prints (src/config/shared/complex/
# ComplexDataTypes.hpp CFontWeightConfigValueData); matched case-insensitively.
WEIGHTS = {
    "thin": 100, "ultralight": 200, "light": 300, "semilight": 350,
    "book": 380, "normal": 400, "medium": 500, "semibold": 600,
    "bold": 700, "ultrabold": 800, "heavy": 900, "ultraheavy": 1000,
}


def f32(value):
    """Round to C++ float32 - the width hyprlang and Hyprland compute alpha in."""
    return struct.unpack("f", struct.pack("f", value))[0]


def alpha_round(token):
    """hyprlang: uint8_t(std::round(stof(a) * 255.f)) - half away from zero."""
    return int(math.floor(f32(f32(float(token)) * 255.0) + 0.5)) & 0xFF


def alpha_floor(token):
    """Hyprland ParserUtils::parseColor: floor(stof(a) * 255.F)."""
    return int(math.floor(f32(f32(float(token)) * 255.0)))


def stoi_prefix(text):
    """C++ std::stoi: the leading integer of TEXT (`45.5` -> 45); ValueError
    when there is none."""
    found = re.match(r"\s*([+-]?\d+)", text)
    if not found:
        raise ValueError(text)
    return int(found.group(1))


def hl_vec2(text):
    """hyprlang v0.6.8 config.cpp:474-486: exactly `x y` (one space), stof each."""
    left, sep, right = text.partition(" ")
    if not sep or " " in right:
        return None
    try:
        return float(left), float(right)
    except ValueError:
        return None


def hl_int(value):
    """hyprlang v0.6.8 src/config.cpp:185-264 configStringToInt; None = error."""
    if value.startswith("0x"):
        try:
            return int(value, 16)
        except ValueError:
            return None
    if value.startswith("rgba(") and value.endswith(")"):
        inner = value[5:-1].strip()
        if inner.count(",") == 3:
            parts = [p.strip() for p in inner.split(",")]
            channels = [hl_int(p) for p in parts[:3]]
            try:
                alpha = alpha_round(parts[3])
            except ValueError:
                return None
            if None in channels:
                return None
            red, green, blue = channels
            return alpha * 0x1000000 + red * 0x10000 + green * 0x100 + blue
        if len(inner) == 8:
            try:
                packed = int(inner, 16)
            except ValueError:
                return None
            return (packed >> 8) + 0x1000000 * (packed & 0xFF)
        return None
    if value.startswith("rgb(") and value.endswith(")"):
        inner = value[4:-1].strip()
        if inner.count(",") == 2:
            channels = [hl_int(p.strip()) for p in inner.split(",")]
            if None in channels:
                return None
            red, green, blue = channels
            return 0xFF000000 + red * 0x10000 + green * 0x100 + blue
        if len(inner) == 6:
            try:
                return int(inner, 16) + 0xFF000000
            except ValueError:
                return None
        return None
    if value.startswith(("true", "on", "yes")):
        return 1
    if value.startswith(("false", "off", "no")):
        return 0
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return None


def _hex(text):
    try:
        return int(text, 16)
    except ValueError:
        return None


def _u8(text):
    text = text.strip()
    if re.fullmatch(r"\d+", text) and int(text) <= 255:
        return int(text)
    return None


def grad_color(value):
    """Hyprland ParserUtils::parseColor (src/config/shared/parserUtils/
    ParserUtils.cpp:23-152), the parser of every gradient colour token; None
    when it is not a colour.  Unlike the int options it takes `#rgb`,
    `#rrggbb`, `#rrggbbaa`, uint8 channels and floors the alpha."""
    if value.startswith("#"):
        digits = value[1:]
        if not re.fullmatch(r"[0-9a-fA-F]+", digits):
            return None
        if len(digits) == 3:
            red, green, blue = (int(c, 16) for c in digits)
            return (0xFF000000 | ((red | red << 4) << 16)
                    | ((green | green << 4) << 8) | (blue | blue << 4))
        if len(digits) == 6:
            return 0xFF000000 | int(digits, 16)
        if len(digits) == 8:
            return ((int(digits[6:8], 16) << 24) | (int(digits[0:2], 16) << 16)
                    | (int(digits[2:4], 16) << 8) | int(digits[4:6], 16))
        return None
    if value.startswith("0x"):
        return _hex(value)
    if value.startswith("rgba(") and value.endswith(")"):
        inner = value[5:-1].strip()
        if inner.count(",") == 3:
            parts = [p.strip() for p in inner.split(",")]
            red, green, blue = _u8(parts[0]), _u8(parts[1]), _u8(parts[2])
            try:
                alpha = alpha_floor(parts[3])
            except ValueError:
                return None
            if None in (red, green, blue):
                return None
            return (alpha << 24) | (red << 16) | (green << 8) | blue
        if len(inner) == 8:
            packed = _hex(inner)
            if packed is None:
                return None
            return (packed >> 8) + 0x1000000 * (packed & 0xFF)
        return None
    if value.startswith("rgb(") and value.endswith(")"):
        inner = value[4:-1].strip()
        if inner.count(",") == 2:
            channels = [_u8(p) for p in inner.split(",")]
            if None in channels:
                return None
            red, green, blue = channels
            return 0xFF000000 | (red << 16) | (green << 8) | blue
        if len(inner) == 6:
            packed = _hex(inner)
            return None if packed is None else packed + 0xFF000000
        return None
    if re.fullmatch(r"\d+", value) and int(value) < 2 ** 32:
        return int(value)
    return None


def gradient_text(declared, inherited=0):
    """Declared gradient -> the host's native text.

    One lowercase unpadded ARGB hex word per colour, then `<angle>deg`; the
    angle is the declared one, else the one the previous declarer left
    (`inherited`).  None when a token is not a colour.
    """
    colours = []
    angle = inherited
    for token in declared.split():
        if "deg" in token:
            try:
                angle = stoi_prefix(token[:token.index("deg")])
            except ValueError:
                return None
            break
        colour = grad_color(token)
        if colour is None:
            return None
        colours.append(colour)
    if not colours:
        return None
    return " ".join("%x" % c for c in colours) + " %ddeg" % angle


def gap_text(declared):
    """Declared gap -> the host's `a b c d`; CSS expansion, 1-4 values."""
    sides = [int(x) for x in declared.split()]
    if len(sides) == 1:
        sides = sides * 4
    elif len(sides) == 2:
        sides = [sides[0], sides[1], sides[0], sides[1]]
    elif len(sides) == 3:
        sides = [sides[0], sides[1], sides[2], sides[1]]
    elif len(sides) != 4:
        return None
    return " ".join(str(x) for x in sides)


def custom_shape(live):
    """Classify a `custom` reply by its own shape: gradient, gap or scalar."""
    tokens = live.split()
    if tokens and tokens[-1].endswith("deg"):
        return "gradient"
    if len(tokens) == 4 and all(t.lstrip("-").isdigit() for t in tokens):
        return "gap"
    return "scalar"


def native_equal(form, declared, live, inherited=0):
    """Does the declared value convert to the compositor's native reply?"""
    text = declared.strip()
    if form == "int":
        return hl_int(text) == live
    if form == "float":
        try:
            return abs(float(text) - float(live)) < 1e-6
        except (TypeError, ValueError):
            return False
    if form == "str":
        return text == str(live).strip()
    if form == "vec2":
        pair = hl_vec2(text)
        return (pair is not None and isinstance(live, list)
                and len(live) == 2
                and abs(pair[0] - float(live[0])) < 1e-6
                and abs(pair[1] - float(live[1])) < 1e-6)
    native = str(live)
    shape = custom_shape(native)
    if shape == "gradient":
        return gradient_text(text, inherited) == native
    if shape == "gap":
        try:
            return gap_text(text) == native
        except ValueError:
            return False
    return str(WEIGHTS.get(text.lower(), -1)) == native


KEY_RE = re.compile(r"[A-Za-z0-9_.][A-Za-z0-9_.:-]{0,127}")
REPLY_CAP = 65536
CHILD_ENV = ("PATH", "HYPRLAND_INSTANCE_SIGNATURE", "XDG_RUNTIME_DIR")


def resolve_program(program):
    """The compositor program as an absolute, regular, executable file that is
    not group- or other-writable; CtlError otherwise (nothing is run)."""
    found = program if os.sep in program else shutil.which(program)
    if not found:
        raise CtlError("hyprctl program %r not found" % program)
    path = os.path.abspath(found)
    try:
        mode = os.stat(path).st_mode
    except OSError as exc:
        raise CtlError("hyprctl program %r: %s" % (path, exc))
    if not stat.S_ISREG(mode) or not os.access(path, os.X_OK):
        raise CtlError("hyprctl program %r is not a regular executable file"
                       % path)
    if mode & (stat.S_IWGRP | stat.S_IWOTH):
        raise CtlError("hyprctl program %r is group- or other-writable" % path)
    return path


def _typed(form, value):
    """The reply field has the type its form promises."""
    if form == "int":
        return isinstance(value, int) and not isinstance(value, bool)
    if form == "float":
        return (isinstance(value, (int, float))
                and not isinstance(value, bool))
    if form in ("str", "custom"):
        return isinstance(value, str)
    return (isinstance(value, list) and len(value) == 2
            and all(isinstance(v, (int, float)) and not isinstance(v, bool)
                    for v in value))


def native_query(hyprctl, key):
    """Run `HYPRCTL getoption -j KEY`; (form, value, set) or None if absent.

    KEY must already satisfy KEY_RE.  The program sees stdin /dev/null and
    only CHILD_ENV; its reply is read to at most REPLY_CAP bytes and typed
    strictly."""
    env = {k: os.environ[k] for k in CHILD_ENV if k in os.environ}
    try:
        proc = subprocess.Popen([hyprctl, "getoption", "-j", key],
                                stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL, env=env)
    except (OSError, ValueError) as exc:
        raise CtlError("%r: cannot run hyprctl %r: %s" % (key, hyprctl, exc))
    timer = threading.Timer(10, proc.kill)
    timer.start()
    try:
        raw = proc.stdout.read(REPLY_CAP + 1)
        too_long = len(raw) > REPLY_CAP
        if too_long:
            proc.kill()
        proc.wait()
    finally:
        timer.cancel()
        proc.stdout.close()
    if too_long:
        raise CtlError("%r: hyprctl reply exceeds %d bytes" % (key, REPLY_CAP))
    if proc.returncode != 0:
        raise CtlError("%r: hyprctl %r exited %d" % (key, hyprctl,
                                                     proc.returncode))
    text = raw.decode("utf-8", "replace").strip()
    if text == "no such option":
        return None
    try:
        reply = json.loads(text)
    except ValueError:
        raise CtlError("%r: malformed reply from hyprctl %r" % (key, hyprctl))
    if not isinstance(reply, dict):
        raise CtlError("%r: reply from hyprctl %r is not a JSON object"
                       % (key, hyprctl))
    forms = [f for f in FORMS if f in reply]
    if len(forms) != 1 or "set" not in reply:
        raise CtlError("%r: unknown reply form from hyprctl %r"
                       % (key, hyprctl))
    if not isinstance(reply["set"], bool) or not _typed(forms[0],
                                                        reply[forms[0]]):
        raise CtlError("%r: mistyped reply from hyprctl %r" % (key, hyprctl))
    return forms[0], reply[forms[0]], reply["set"]


def merge_live(rows, options, hyprctl, probes):
    """Label every row against the compositor, then add the answered probes."""
    seen = set()
    for row in rows:
        seen.add(row["key"])
        reply = native_query(hyprctl, row["key"])
        if reply is None:
            row["agreement"] = "config-only"
            row["live"] = None
            continue
        form, value, isset = reply
        row["live"] = str(value)
        inherited = options[row["key"]].get("_inherited", 0)
        if not isset or not native_equal(form, row["value"], value, inherited):
            row["agreement"] = "mismatch"
        elif options[row["key"]]["_decls"] > 1:
            row["agreement"] = "agreement*"
        else:
            row["agreement"] = "agreement"
    for key in probes:
        if key in seen:
            continue
        seen.add(key)
        reply = native_query(hyprctl, key)
        if reply is None:
            continue
        form, value, isset = reply
        rows.append({
            "key": key, "value": str(value), "owner": None, "layer": None,
            "line": None, "set": isset, "agreement": "live-default",
            "live": str(value),
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
    parser.add_argument("--getoption", metavar="FILE", default=None,
                        help="live hyprctl getoption JSON (key -> {value, custom_type, set})")
    parser.add_argument("--live", action="store_true",
                        help="query the running compositor (hyprctl getoption -j)")
    parser.add_argument("--hyprctl", metavar="PATH", default="hyprctl",
                        help="compositor program to run (default: hyprctl)")
    parser.add_argument("--probe", metavar="KEY", action="append", default=[],
                        help="extra live key with no declarer (repeatable)")
    parser.add_argument("--selftest", action="store_true",
                        help="run the hermetic selftest and exit")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()

    if not args.home:
        parser.print_usage(sys.stderr)
        sys.stderr.write("mado-options.py: error: --home DIR is required\n")
        return 2
    if args.live and args.getoption:
        sys.stderr.write("mado-options.py: error: --live and --getoption "
                         "are exclusive\n")
        return 2
    for key in args.probe:
        if not KEY_RE.fullmatch(key):
            sys.stderr.write("mado-options.py: invalid probe key %r\n" % key)
            return 2
    home = os.path.abspath(args.home)
    root = os.path.join(home, ".config", "hypr", "hyprland.conf")
    st = State(home)
    try:
        parse_file(root, st)
        rows = run_static(st)
        if args.getoption:
            live = load_live(args.getoption)
            merge_rows(rows, st.options, live)
        if args.live:
            for row in rows:
                if not KEY_RE.fullmatch(row["key"]):
                    sys.stderr.write("mado-options.py: invalid key %r in the "
                                     "config tree (never sent to hyprctl)\n"
                                     % row["key"])
                    return 2
            merge_live(rows, st.options, resolve_program(args.hyprctl),
                       args.probe)
    except CtlError as exc:
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

def _raises(fn, *args):
    """True when fn(*args) returns without raising ValueError."""
    try:
        fn(*args)
    except ValueError:
        return False
    return True


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


# A compositor stand-in: logs the exact argv, answers from table.json in the
# four native forms, and can be told to fail, answer non-JSON or answer an
# object with no known form for one key (`mode`).
STUB_SOURCE = '''#!__PYTHON__
import json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "calls.log"), "a") as handle:
    handle.write(json.dumps(sys.argv[1:]) + "\\n")
with open(os.path.join(here, "mode")) as handle:
    mode = handle.read().strip()
with open(os.path.join(here, "table.json")) as handle:
    table = json.load(handle)
if sys.argv[1:3] != ["getoption", "-j"] or len(sys.argv) != 4:
    sys.stdout.write("bad request\\n")
    sys.exit(0)
key = sys.argv[3]
if mode.startswith("fail:") and key == mode[5:]:
    sys.stderr.write("stub failure\\n")
    sys.exit(1)
if mode.startswith("failout:") and key == mode[8:]:
    sys.stdout.write("HYPRLAND_INSTANCE_SIGNATURE not set! (is hyprland running?)\\n\\n")
    sys.exit(1)
if mode.startswith("huge:") and key == mode[5:]:
    sys.stdout.write(json.dumps({"option": key, "str": "x" * 200000, "set": True}) + "\\n")
    sys.exit(0)
if mode.startswith("typeset:") and key == mode[8:]:
    sys.stdout.write(json.dumps({"option": key, "int": 1, "set": "yes"}) + "\\n")
    sys.exit(0)
if mode.startswith("typeint:") and key == mode[8:]:
    sys.stdout.write(json.dumps({"option": key, "int": "7", "set": True}) + "\\n")
    sys.exit(0)
if mode.startswith("null:") and key == mode[5:]:
    sys.stdout.write("null\\n")
    sys.exit(0)
if mode.startswith("bad:") and key == mode[4:]:
    sys.stdout.write("{not json\\n")
    sys.exit(0)
if mode.startswith("form:") and key == mode[5:]:
    sys.stdout.write(json.dumps({"option": key, "set": True}) + "\\n")
    sys.exit(0)
reply = table.get(key)
if reply is None:
    sys.stdout.write("no such option\\n")
else:
    sys.stdout.write(json.dumps(reply) + "\\n")
'''


def _stub(tmp, name, table, mode="ok"):
    """Create a stub hyprctl inside the private temp dir; return its path."""
    directory = os.path.join(tmp, name)
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, "hyprctl")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(STUB_SOURCE.replace("__PYTHON__", sys.executable))
    os.chmod(path, 0o755)
    with open(os.path.join(directory, "table.json"), "w",
              encoding="utf-8") as handle:
        json.dump(table, handle)
    with open(os.path.join(directory, "mode"), "w",
              encoding="utf-8") as handle:
        handle.write(mode)
    open(os.path.join(directory, "calls.log"), "w").close()
    return path


def _calls(stub):
    """Every argv the stub compositor was run with."""
    path = os.path.join(os.path.dirname(stub), "calls.log")
    with open(path, encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _listing(root):
    """(path, size, mtime) for every file under root - the no-write check."""
    found = []
    for base, _, files in os.walk(root):
        for name in files:
            path = os.path.join(base, name)
            found.append((path, os.path.getsize(path), os.path.getmtime(path)))
    return sorted(found)


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

        # ---- usage --------------------------------------------------------
        run = _run(script, tmp, [])
        _check(checks, "usage: no --home exits 2", run.returncode == 2)
        run = _run(script, tmp, ["--live"])
        _check(checks, "usage: --live without --home exits 2", run.returncode == 2)

        # ---- live path: --live / --hyprctl / --probe ----------------------
        # A tree whose declarations cover every conversion the host applies,
        # and a stub compositor answering in the four native forms.
        live_home = os.path.join(tmp, "livehome")
        os.makedirs(live_home)
        _write(live_home, ".config/hypr/hyprland.conf", """\
general {
    int_hex = 0x2
    int_rgba8 = rgba(33ccffee)
    int_rgba_dec = rgba(255,128,0,0.8)
    int_rgb6 = rgb(595959)
    int_rgb_dec = rgb(255,128,0)
    bool_true = true
    bool_on = on
    bool_yes = yes
    bool_false = false
    bool_off = off
    bool_no = no
    int_neg = -3
    int_plain = 5
    float_ok = 1.50
    str_ok = dwindle
    col.gradient_angle = rgba(33ccffee) rgba(00ff99ee) 45deg
    col.gradient_noangle = rgba(11223344)
    col.active_border = rgba(33ccffee) rgba(00ff99ee) 45deg
    col.active_border = rgb(e68e0d)
    gap_one = 4
    gap_two = 10 20
    gap_three = 7 8 9
    gap_four = 1 2 3 4
    gap_differ = 1 2
    weight_lower = semibold
    weight_upper = BOLD
    weight_differ = thin
    differ = 3
    unset_key = 7
    str_differ = alpha
    absent_key = 3
}
decoration {
    rounding = 8
    shadow {
        enabled = yes
        color = rgba(1a1a1aee)
    }
}
""")
        live_table = {
            "general:int_hex": {"option": "general:int_hex", "int": 2, "set": True},
            "general:int_rgba8": {"option": "general:int_rgba8", "int": 0xee33ccff, "set": True},
            "general:int_rgba_dec": {"option": "general:int_rgba_dec", "int": 0xccff8000, "set": True},
            "general:int_rgb6": {"option": "general:int_rgb6", "int": 0xff595959, "set": True},
            "general:int_rgb_dec": {"option": "general:int_rgb_dec", "int": 0xffff8000, "set": True},
            "general:bool_true": {"option": "general:bool_true", "int": 1, "set": True},
            "general:bool_on": {"option": "general:bool_on", "int": 1, "set": True},
            "general:bool_yes": {"option": "general:bool_yes", "int": 1, "set": True},
            "general:bool_false": {"option": "general:bool_false", "int": 0, "set": True},
            "general:bool_off": {"option": "general:bool_off", "int": 0, "set": True},
            "general:bool_no": {"option": "general:bool_no", "int": 0, "set": True},
            "general:int_neg": {"option": "general:int_neg", "int": -3, "set": True},
            "general:int_plain": {"option": "general:int_plain", "int": 5, "set": True},
            "general:float_ok": {"option": "general:float_ok", "float": 1.5, "set": True},
            "general:str_ok": {"option": "general:str_ok", "str": "dwindle", "set": True},
            "general:col.gradient_angle": {"option": "general:col.gradient_angle", "custom": "ee33ccff ee00ff99 45deg", "set": True},
            "general:col.gradient_noangle": {"option": "general:col.gradient_noangle", "custom": "44112233 0deg", "set": True},
            "general:col.active_border": {"option": "general:col.active_border", "custom": "ffe68e0d 45deg", "set": True},
            "general:gap_one": {"option": "general:gap_one", "custom": "4 4 4 4", "set": True},
            "general:gap_two": {"option": "general:gap_two", "custom": "10 20 10 20", "set": True},
            "general:gap_three": {"option": "general:gap_three", "custom": "7 8 9 8", "set": True},
            "general:gap_four": {"option": "general:gap_four", "custom": "1 2 3 4", "set": True},
            "general:gap_differ": {"option": "general:gap_differ", "custom": "1 2 3 4", "set": True},
            "general:weight_lower": {"option": "general:weight_lower", "custom": "600", "set": True},
            "general:weight_upper": {"option": "general:weight_upper", "custom": "700", "set": True},
            "general:weight_differ": {"option": "general:weight_differ", "custom": "400", "set": True},
            "general:differ": {"option": "general:differ", "int": 4, "set": True},
            "general:unset_key": {"option": "general:unset_key", "int": 7, "set": False},
            "general:str_differ": {"option": "general:str_differ", "str": "beta", "set": True},
            "decoration:rounding": {"option": "decoration:rounding", "int": 8, "set": True},
            "decoration:shadow:enabled": {"option": "decoration:shadow:enabled", "int": 1, "set": True},
            "decoration:shadow:color": {"option": "decoration:shadow:color", "custom": "ee1a1a1a 0deg", "set": True},
        }
        probes = ("zzprobe:one", "zzprobe:none", "general:str_ok")
        # every key the tree declares: the table covers all but absent_key
        declared_keys = set(live_table) | {"general:absent_key"}
        live_table["zzprobe:one"] = {"option": "zzprobe:one", "int": 3,
                                     "set": False}
        stub = _stub(tmp, "stub-ok", live_table)
        before = _listing(live_home)
        args = ["--home", live_home, "--live", "--hyprctl", stub]
        for key in probes:
            args += ["--probe", key]
        run = _run(script, tmp, args)
        _check(checks, "live: exit 0", run.returncode == 0)
        try:
            live_rows = json.loads(run.stdout)
        except ValueError as exc:
            _check(checks, "live: stdout parses as JSON (%s)" % exc, False)
            live_rows = []
        _check(checks, "live: stdout is a JSON array",
               isinstance(live_rows, list)
               and all(isinstance(r, dict) for r in live_rows))
        live_by = {r.get("key"): r for r in live_rows}

        def live_label(key):
            return live_by.get(key, {}).get("agreement")

        _check(checks, "live: rows sorted by key",
               [r.get("key") for r in live_rows]
               == sorted(r.get("key") for r in live_rows))
        _check(checks, "live: config root unchanged",
               _listing(live_home) == before)
        _check(checks, "live: exact row set (declared keys + answered probe)",
               set(live_by) == declared_keys | {"zzprobe:one"})

        # native forms and every conversion
        _check(checks, "live int: 0x hex",
               live_label("general:int_hex") == "agreement")
        _check(checks, "live int: rgba 8-hex",
               live_label("general:int_rgba8") == "agreement")
        _check(checks, "live int: rgba(r,g,b,a)",
               live_label("general:int_rgba_dec") == "agreement")
        _check(checks, "live int: rgb 6-hex",
               live_label("general:int_rgb6") == "agreement")
        _check(checks, "live int: rgb(r,g,b)",
               live_label("general:int_rgb_dec") == "agreement")
        _check(checks, "live int: true prefix",
               live_label("general:bool_true") == "agreement")
        _check(checks, "live int: on prefix",
               live_label("general:bool_on") == "agreement")
        _check(checks, "live int: yes prefix",
               live_label("general:bool_yes") == "agreement")
        _check(checks, "live int: false prefix",
               live_label("general:bool_false") == "agreement")
        _check(checks, "live int: off prefix",
               live_label("general:bool_off") == "agreement")
        _check(checks, "live int: no prefix",
               live_label("general:bool_no") == "agreement")
        _check(checks, "live int: negative",
               live_label("general:int_neg") == "agreement")
        _check(checks, "live int: decimal",
               live_label("general:int_plain") == "agreement")
        _check(checks, "live float: 1.50 equals 1.5",
               live_label("general:float_ok") == "agreement")
        _check(checks, "live str: exact equality",
               live_label("general:str_ok") == "agreement")
        _check(checks, "live custom: gradient with a declared angle",
               live_label("general:col.gradient_angle") == "agreement")
        _check(checks, "live custom: gradient without an angle is 0deg",
               live_label("general:col.gradient_noangle") == "agreement")
        _check(checks, "live custom: gradient inherits the prior angle",
               live_label("general:col.active_border") == "agreement*")
        _check(checks, "live custom: gap 1 value",
               live_label("general:gap_one") == "agreement")
        _check(checks, "live custom: gap 2 values",
               live_label("general:gap_two") == "agreement")
        _check(checks, "live custom: gap 3 values",
               live_label("general:gap_three") == "agreement")
        _check(checks, "live custom: gap 4 values",
               live_label("general:gap_four") == "agreement")
        _check(checks, "live custom: gap mismatch",
               live_label("general:gap_differ") == "mismatch")
        _check(checks, "live custom: font weight name",
               live_label("general:weight_lower") == "agreement")
        _check(checks, "live custom: font weight name case-insensitive",
               live_label("general:weight_upper") == "agreement")
        _check(checks, "live custom: font weight mismatch",
               live_label("general:weight_differ") == "mismatch")
        _check(checks, "live: value differs is a mismatch",
               live_label("general:differ") == "mismatch")
        _check(checks, "live: set=false is a mismatch",
               live_label("general:unset_key") == "mismatch")
        _check(checks, "live: str differs is a mismatch",
               live_label("general:str_differ") == "mismatch")
        _check(checks, "live: no such option is config-only",
               live_label("general:absent_key") == "config-only")
        _check(checks, "live: declared row carries the native text",
               live_by.get("general:int_plain", {}).get("live") == "5")
        _check(checks, "live: custom row carries the native text",
               live_by.get("general:col.active_border", {}).get("live")
               == "ffe68e0d 45deg")
        _check(checks, "live: config-only live is null",
               live_by.get("general:absent_key", {}).get("live") is None)
        _check(checks, "live: shadowed key keeps the last declarer",
               live_by.get("general:col.active_border", {}).get("value")
               == "rgb(e68e0d)")

        # --probe
        probe_row = live_by.get("zzprobe:one", {})
        _check(checks, "live probe: answered key is live-default",
               probe_row.get("agreement") == "live-default")
        _check(checks, "live probe: no owner/layer/line",
               probe_row.get("owner") is None and probe_row.get("layer") is None
               and probe_row.get("line") is None)
        _check(checks, "live probe: set=false carried",
               probe_row.get("set") is False)
        _check(checks, "live probe: value is the native text",
               probe_row.get("value") == "3")
        _check(checks, "live probe: unknown key dropped",
               "zzprobe:none" not in live_by)
        _check(checks, "live probe: declared key not duplicated",
               sum(1 for r in live_rows if r.get("key") == "general:str_ok") == 1
               and live_label("general:str_ok") == "agreement")

        # exact argv: only `getoption -j KEY`, once per key
        calls = _calls(stub)
        _check(checks, "live argv: every call is getoption -j KEY",
               all(len(c) == 3 and c[:2] == ["getoption", "-j"] for c in calls))
        _check(checks, "live argv: one call per declared key and probe",
               sorted(c[2] for c in calls)
               == sorted(declared_keys | set(probes)))
        _check(checks, "live argv: no duplicate queries",
               len(calls) == len(set(tuple(c) for c in calls)))

        # failures are named (exit 5) and hostile probes never reach argv
        victim = "general:int_plain"
        for mode, desc in (("fail:", "compositor exit"), ("bad:", "malformed reply"),
                           ("form:", "unknown reply form")):
            bad_stub = _stub(tmp, "stub-" + mode[:4], live_table, mode + victim)
            run = _run(script, tmp, ["--home", live_home, "--live",
                                     "--hyprctl", bad_stub])
            _check(checks, "live failure (%s): exit 5" % desc, run.returncode == 5)
            _check(checks, "live failure (%s): key named" % desc,
                   victim in run.stderr)
            _check(checks, "live failure (%s): no stdout" % desc,
                   run.stdout.strip() == "")

        gone = os.path.join(tmp, "no-such-dir", "hyprctl")
        run = _run(script, tmp, ["--home", live_home, "--live", "--hyprctl", gone])
        _check(checks, "live failure (missing program): exit 5",
               run.returncode == 5)
        _check(checks, "live failure (missing program): names hyprctl",
               "hyprctl" in run.stderr)
        _check(checks, "live failure (missing program): sends no request",
               "Traceback" not in run.stderr)

        for bad in ("-x", "--version", ""):
            hostile_stub = _stub(tmp, "stub-hostile", live_table)
            run = _run(script, tmp, ["--home", live_home, "--live",
                                     "--hyprctl", hostile_stub,
                                     "--probe", bad])
            _check(checks, "live hostile probe %r: exit 2" % bad,
                   run.returncode == 2)
            _check(checks, "live hostile probe %r: names the probe" % bad,
                   "probe" in run.stderr.lower())
            _check(checks, "live hostile probe %r: no program run" % bad,
                   not _calls(hostile_stub))

        # ---- conversions called directly: the host's rounding and parsing ----
        _check(checks, "hl_int: rgba alpha 0.5 rounds half away (0x80)",
               hl_int("rgba(0,0,0,0.5)") == 0x80000000)
        _check(checks, "hl_int: rgba alpha 0.3 -> 77 (76.5 rounds up, not to even)",
               hl_int("rgba(0,0,0,0.3)") == 77 * 0x1000000)
        _check(checks, "hl_int: rgba alpha 0.1 -> 26 (25.5 rounds up)",
               hl_int("rgba(0,0,0,0.1)") == 26 * 0x1000000)
        _check(checks, "hl_int: rgba alpha 1 -> 255",
               hl_int("rgba(1,2,3,1)") == 0xFF010203)
        _check(checks, "hl_int: rgb(r,g,b) is opaque ARGB",
               hl_int("rgb(1,2,3)") == 0xFF010203)
        _check(checks, "hl_int: rgb(rrggbb) is opaque ARGB",
               hl_int("rgb(010203)") == 0xFF010203)
        _check(checks, "hl_int: rgba(rrggbbaa) is moved to ARGB",
               hl_int("rgba(01020304)") == 0x04010203)
        _check(checks, "hl_int: 0x hex", hl_int("0x10") == 16)
        _check(checks, "hl_int: prose beginning yes is 1",
               hl_int("yes, please :)") == 1)
        _check(checks, "hl_int: prefix no catches `nothing` (0)",
               hl_int("nothing") == 0)
        _check(checks, "hl_int: negative decimal", hl_int("-3") == -3)
        _check(checks, "hl_int: trailing junk is an error", hl_int("12abc") is None)
        _check(checks, "hl_int: rgba with 2 commas is an error",
               hl_int("rgba(1,2,3)") is None)
        _check(checks, "stoi_prefix: 45.5 reads 45", stoi_prefix("45.5") == 45)
        _check(checks, "stoi_prefix: no digits is an error",
               not _raises(stoi_prefix, "x45"))
        _check(checks, "gradient_text: fractional angle token keeps its prefix",
               gradient_text("rgb(010203) 45.5deg") == "ff010203 45deg")
        _check(checks, "gradient_text: no angle -> inherited angle",
               gradient_text("rgb(010203)", 90) == "ff010203 90deg")
        _check(checks, "gradient_text: a non-colour token is an error",
               gradient_text("zzz 45deg") is None)
        _check(checks, "gap_text: 5 values are not a gap", gap_text("1 2 3 4 5") is None)
        _check(checks, "hl_vec2: x y", hl_vec2("1.5 2") == (1.5, 2.0))
        _check(checks, "hl_vec2: two spaces are refused", hl_vec2("1  2") is None)
        _check(checks, "hl_vec2: one value is refused", hl_vec2("1") is None)
        _check(checks, "hl_vec2: non-numbers are refused", hl_vec2("a b") is None)
        _check(checks, "native_equal vec2: equal pair",
               native_equal("vec2", "1.5 2", [1.5, 2.0]))
        _check(checks, "native_equal vec2: differing pair",
               not native_equal("vec2", "1.5 3", [1.5, 2.0]))
        _check(checks, "native_equal vec2: a scalar reply is not a pair",
               not native_equal("vec2", "1.5 2", "1.5 2"))
        _check(checks, "native_equal custom: weight names are case-insensitive",
               native_equal("custom", "BOLD", "700"))
        _check(checks, "native_equal float: 1e-6 tolerance",
               native_equal("float", "1.3700001", 1.37)
               and not native_equal("float", "1.38", 1.37))
        _check(checks, "native_equal str: trimmed exact equality",
               native_equal("str", " a b ", "a b")
               and not native_equal("str", "a b", "a  b"))

        # ---- five forms through a stub: vec2, a failing compositor that
        # speaks on stdout, a form-less reply, probes ----
        vec_home = os.path.join(tmp, "vechome")
        os.makedirs(vec_home)
        _write(vec_home, ".config/hypr/hyprland.conf", """\
offs {
    pos = 1.5 2
    neg = -3 4.25
    wrong = 1 2 3
    off = 5 5
}
""")
        vec_table = {
            "offs:pos": {"option": "offs:pos", "vec2": [1.5, 2], "set": True},
            "offs:neg": {"option": "offs:neg", "vec2": [-3, 4.25], "set": True},
            "offs:wrong": {"option": "offs:wrong", "vec2": [0, 0], "set": True},
            "offs:off": {"option": "offs:off", "vec2": [5, 6], "set": True},
            "zzprobe:vec": {"option": "zzprobe:vec", "vec2": [0, 0], "set": False},
        }
        vec_stub = _stub(tmp, "stub-vec", vec_table)
        run = _run(script, tmp, ["--home", vec_home, "--live", "--hyprctl",
                                 vec_stub, "--probe", "zzprobe:vec",
                                 "--probe", "zzprobe:vec"])
        _check(checks, "vec2 tree: exit 0", run.returncode == 0)
        try:
            vec_rows = {r["key"]: r for r in json.loads(run.stdout)}
        except ValueError:
            vec_rows = {}
        _check(checks, "vec2: declared pair agrees",
               vec_rows.get("offs:pos", {}).get("agreement") == "agreement")
        _check(checks, "vec2: negative and fractional pair agrees",
               vec_rows.get("offs:neg", {}).get("agreement") == "agreement")
        _check(checks, "vec2: three values never agree (hyprlang refuses them)",
               vec_rows.get("offs:wrong", {}).get("agreement") == "mismatch")
        _check(checks, "vec2: one differing component is a mismatch",
               vec_rows.get("offs:off", {}).get("agreement") == "mismatch")
        _check(checks, "vec2: a probe row is live-default and carries the pair",
               vec_rows.get("zzprobe:vec", {}).get("agreement") == "live-default"
               and vec_rows.get("zzprobe:vec", {}).get("live") == "[0, 0]")
        _check(checks, "vec2: a duplicated probe is asked once",
               [c[2] for c in _calls(vec_stub)].count("zzprobe:vec") == 1)
        out_stub = _stub(tmp, "stub-failout", vec_table, "failout:offs:neg")
        run = _run(script, tmp, ["--home", vec_home, "--live", "--hyprctl",
                                 out_stub])
        _check(checks, "failure on stdout: exit 5", run.returncode == 5)
        _check(checks, "failure on stdout: names the failing key only",
               "offs:neg" in run.stderr and "offs:pos" not in run.stderr)
        form_stub = _stub(tmp, "stub-noform", vec_table, "form:offs:pos")
        run = _run(script, tmp, ["--home", vec_home, "--live", "--hyprctl",
                                 form_stub])
        _check(checks, "form-less reply: exit 5 naming the key",
               run.returncode == 5 and "offs:pos" in run.stderr)
        for bad in ("-x", "--version", ""):
            eq_stub = _stub(tmp, "stub-eq", vec_table)
            run = _run(script, tmp, ["--home", vec_home, "--live",
                                     "--hyprctl", eq_stub,
                                     "--probe=%s" % bad])
            _check(checks, "hostile --probe=%r: exit 2 before any request" % bad,
                   run.returncode == 2 and not _calls(eq_stub))

        # ---- security and typing of the live path ----
        _check(checks, "alpha 0.7 rounds in float32 to 179 (178.5, half away)",
               hl_int("rgba(0,0,0,0.7)") == 179 * 0x1000000)
        _check(checks, "gradient alpha floors: rgba(1,2,3,0.5) -> 0x7f010203",
               grad_color("rgba(1,2,3,0.5)") == 0x7F010203)
        _check(checks, "gradient alpha floors: 0.3 -> 76",
               grad_color("rgba(0,0,0,0.3)") == 76 * 0x1000000)
        _check(checks, "gradient colour: #rgb", grad_color("#abc") == 0xFFAABBCC)
        _check(checks, "gradient colour: #rrggbb", grad_color("#010203") == 0xFF010203)
        _check(checks, "gradient colour: #rrggbbaa", grad_color("#01020304") == 0x04010203)
        _check(checks, "gradient colour: rgb channels are uint8",
               grad_color("rgb(1,2,256)") is None and grad_color("rgb(1,2,255)") == 0xFF0102FF)
        _check(checks, "gradient colour: a plain number",
               grad_color("4294967295") == 0xFFFFFFFF and grad_color("4294967296") is None)
        _check(checks, "gradient colour: a prefix-bool word is NOT a colour",
               grad_color("nonsense") is None)
        _check(checks, "KEY_RE: a plain option key", bool(KEY_RE.fullmatch("general:col.active_border")))
        _check(checks, "KEY_RE: a batch-injecting key is refused",
               not KEY_RE.fullmatch("x/--batch") and not KEY_RE.fullmatch("a b")
               and not KEY_RE.fullmatch("-j") and not KEY_RE.fullmatch("a;b")
               and not KEY_RE.fullmatch(""))
        _check(checks, "_typed: int refuses a bool and a string",
               _typed("int", 1) and not _typed("int", True) and not _typed("int", "7"))
        _check(checks, "_typed: vec2 wants exactly two numbers",
               _typed("vec2", [0, 1.5]) and not _typed("vec2", [0])
               and not _typed("vec2", ["0", "1"]))
        key_home = os.path.join(tmp, "keyhome")
        os.makedirs(key_home)
        _write(key_home, ".config/hypr/hyprland.conf", """\
ok {
    fine = 1
}
zzbad {
    x/--batch = 2
}
""")
        key_stub = _stub(tmp, "stub-key", {})
        run = _run(script, tmp, ["--home", key_home, "--live", "--hyprctl",
                                 key_stub])
        _check(checks, "hostile declared key: exit 2 naming it",
               run.returncode == 2 and "x/--batch" in run.stderr)
        _check(checks, "hostile declared key: no request at all",
               not _calls(key_stub))
        for bad in ("a/--batch", "a b", "a;dispatch"):
            probe_stub = _stub(tmp, "stub-probekey", live_table)
            run = _run(script, tmp, ["--home", live_home, "--live",
                                     "--hyprctl", probe_stub,
                                     "--probe=%s" % bad])
            _check(checks, "hostile probe %r: exit 2, no request" % bad,
                   run.returncode == 2 and not _calls(probe_stub))
        run = _run(script, tmp, ["--home", live_home, "--live", "--getoption",
                                 os.path.join(tmp, "x.json")])
        _check(checks, "--live with --getoption: exit 2", run.returncode == 2)
        open_stub = _stub(tmp, "stub-open", live_table)
        os.chmod(open_stub, 0o777)
        run = _run(script, tmp, ["--home", live_home, "--live", "--hyprctl",
                                 open_stub])
        _check(checks, "world-writable program: exit 5 naming hyprctl, never run",
               run.returncode == 5 and "hyprctl" in run.stderr
               and not _calls(open_stub))
        run = _run(script, tmp, ["--home", live_home, "--live", "--hyprctl",
                                 os.path.dirname(open_stub)])
        _check(checks, "a directory as the program: exit 5",
               run.returncode == 5 and "hyprctl" in run.stderr)
        cap_table = {"offs:pos": {"option": "offs:pos", "vec2": [1.5, 2],
                                  "set": True}}
        for mode, desc in (("huge:", "oversized reply"),
                           ("typeset:", "set is not a boolean"),
                           ("typeint:", "int is a string"),
                           ("null:", "null reply")):
            bad_stub = _stub(tmp, "stub-" + mode[:-1], vec_table, mode + "offs:neg")
            run = _run(script, tmp, ["--home", vec_home, "--live", "--hyprctl",
                                     bad_stub])
            _check(checks, "%s: exit 5 naming the key, no traceback" % desc,
                   run.returncode == 5 and "offs:neg" in run.stderr
                   and "Traceback" not in run.stderr)

        # the static path is untouched: no agreement/live without --live
        run = _run(script, tmp, ["--home", live_home])
        _check(checks, "live tree static: exit 0", run.returncode == 0)
        try:
            static_rows = json.loads(run.stdout)
        except ValueError:
            static_rows = []
        _check(checks, "live tree static: no agreement field",
               all("agreement" not in r for r in static_rows))
        _check(checks, "live tree static: no live field",
               all("live" not in r for r in static_rows))
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

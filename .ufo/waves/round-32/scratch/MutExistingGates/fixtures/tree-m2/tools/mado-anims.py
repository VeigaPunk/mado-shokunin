#!/usr/bin/env python3
"""Static resolver for the animation table of a Hyprland v0.56.2 config tree.

Reads DIR/.config/hypr/hyprland.conf from bytes only (no compositor, no socket, no
network), follows `source =` depth-first in line order (`~` expands to DIR, glob
patterns expand sorted the way glob(3) sorts them, relative paths join the sourcing
file's directory), expands `$name` variables, applies the `##` comment escape, then
applies the legacy `animation` and `bezier` handlers in processing order.  Prints
one JSON array of two arrays -- the 35 animation nodes and the bezier map -- with the
six node fields and five bezier fields `hyprctl animations -j` prints, exit 0.

Semantics transcribed from Hyprland efb50993 (src/config/legacy/ConfigManager.cpp
handleAnimation/handleBezier/handleSource, src/config/shared/animation/AnimationTree.cpp
reset, src/config/shared/parserUtils/ParserUtils.cpp parseInt,
src/config/shared/animation/AnimationManager.cpp style rules, src/debug/HyprCtl.cpp
animationsRequest) and its dependencies hyprutils v0.14.2
(src/animation/AnimationConfig.cpp setConfigForNode, src/animation/AnimationManager.cpp
bezier map, src/string/VarList.cpp, src/string/String.cpp isNumber) and hyprlang
v0.6.8 (src/config.cpp parseLine/parseFile/getNextLine/parseVariable).

Usage: python3 -I mado-anims.py --home DIR
"""

import glob
import json
import os
import stat
import struct
import sys

WS = " \t\n\r\v\f"
DIGITS = "0123456789"
HEXDIGITS = "0123456789abcdefABCDEF"

# CAnimationTreeController::reset (AnimationTree.cpp:14-67): create order, name -> parent.
NODE_TABLE = (
    ("__internal_fadeCTM", ""),
    ("global", ""),
    ("windows", "global"),
    ("layers", "global"),
    ("fade", "global"),
    ("border", "global"),
    ("borderangle", "global"),
    ("shadowangle", "global"),
    ("glowangle", "global"),
    ("workspaces", "global"),
    ("zoomFactor", "global"),
    ("monitorAdded", "global"),
    ("layersIn", "layers"),
    ("layersOut", "layers"),
    ("windowsIn", "windows"),
    ("windowsOut", "windows"),
    ("windowsMove", "windows"),
    ("fadeIn", "fade"),
    ("fadeOut", "fade"),
    ("fadeSwitch", "fade"),
    ("fadeShadow", "fade"),
    ("fadeGlow", "fade"),
    ("fadeDim", "fade"),
    ("fadeLayers", "fade"),
    ("fadeLayersIn", "fadeLayers"),
    ("fadeLayersOut", "fadeLayers"),
    ("fadePopups", "fade"),
    ("fadePopupsIn", "fadePopups"),
    ("fadePopupsOut", "fadePopups"),
    ("fadeDpms", "fade"),
    ("workspacesIn", "workspaces"),
    ("workspacesOut", "workspaces"),
    ("specialWorkspace", "workspaces"),
    ("specialWorkspaceIn", "specialWorkspace"),
    ("specialWorkspaceOut", "specialWorkspace"),
)

# The five setConfigForNode calls at the end of reset(): name -> (enabled, speed, bezier).
NODE_DEFAULTS = {
    "global": (1, 8.0, "default"),
    "__internal_fadeCTM": (1, 5.0, "linear"),
    "borderangle": (0, 1.0, "default"),
    "shadowangle": (0, 1.0, "default"),
    "glowangle": (0, 1.0, "default"),
}

# hyprutils AnimationManager.cpp:13 (default) and the legacy linear add (ConfigManager.cpp:767).
DEFAULT_BEZIER = (0.0, 0.75, 0.15, 1.0)
LINEAR_BEZIER = (0.0, 0.0, 1.0, 1.0)


def trim(s):
    return s.strip(WS)


def at(fields, idx):
    """CVarList::operator[]: past the end reads as an empty string."""
    return fields[idx] if 0 <= idx < len(fields) else ""


def cvarlist(value):
    """CVarList(in, 0, ',', removeEmpty=false): split, trim every field."""
    if not value:
        # an empty input keeps the initial empty field plus the split's empty field
        return ["", ""]
    return [trim(part) for part in value.split(",")]


def is_number(s, allowfloat):
    """hyprutils isNumber2: optional leading '-', digits, at most one non-leading '.'
    when allowfloat, last character a digit."""
    if not s:
        return False
    decimal_parsed = False
    for i, c in enumerate(s):
        if i == 0 and c == "-":
            continue
        if c not in DIGITS:
            if not allowfloat:
                return False
            if c != ".":
                return False
            if i == 0:
                return False
            if decimal_parsed:
                return False
            decimal_parsed = True
            continue
    return s[-1] in DIGITS


def float32(text):
    """std::stof: single-precision value, widened to double the way Vector2D and the
    float field promote it.  Overflow of the single-precision range raises."""
    return struct.unpack("<f", struct.pack("<f", float(text)))[0]


def str_to_number_int(s):
    """hyprutils strToNumber<int64_t>: '0x'/'0X' hex, else base-10 from_chars with an
    optional leading '-' and no other junk; out-of-range fails."""
    if not s:
        return None
    if len(s) >= 2 and s[0] == "0" and s[1] in "xX":
        body = s[2:]
        if not body or any(c not in HEXDIGITS for c in body):
            return None
        value = int(body, 16)
        if value > 0xFFFFFFFFFFFFFFFF:
            return None
        return value if value < (1 << 63) else value - (1 << 64)
    body = s[1:] if s[0] == "-" else s
    if not body or any(c not in DIGITS for c in body):
        return None
    value = int(body)
    if s[0] == "-":
        return -value if -value >= -(1 << 63) else None
    return value if value < (1 << 63) else None


def parse_int(s):
    """ParserUtils::parseInt: '0x' hex, then the true/on/yes and false/off/no prefixes,
    then a whole-token base-10 integer; None when nothing parses."""
    if s.startswith("0x"):
        return str_to_number_int(s)
    if s.startswith("true") or s.startswith("on") or s.startswith("yes"):
        return 1
    if s.startswith("false") or s.startswith("off") or s.startswith("no"):
        return 0
    return str_to_number_int(s)


def round2(value):
    """std::format "{:.2f}": two fixed decimals, then the JSON number those digits spell."""
    return float("%.2f" % value)


def unescape_braces(s):
    """hyprlang removes a backslash before '{', '}', and another backslash."""
    if not s:
        return s
    out = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c == "\\" and i + 1 < n and s[i + 1] in "\\{}":
            out.append(s[i + 1])
            i += 2
            continue
        out.append(c)
        i += 1
    return "".join(out)


def truthy(s):
    if s == "1":
        return True
    if s == "0":
        return False
    low = s.lower()
    return low.startswith("true") or low.startswith("yes") or low.startswith("on")


class State:
    __slots__ = ("home", "variables", "nodes", "beziers", "categories", "ifs")

    def __init__(self, home):
        self.home = home
        self.variables = []
        self.nodes = {}
        for name, _parent in NODE_TABLE:
            self.nodes[name] = [False, "", -1, 0.0, ""]
        for name, (enabled, speed, bezier) in NODE_DEFAULTS.items():
            self.nodes[name] = [True, bezier, enabled, speed, ""]
        self.beziers = {"default": DEFAULT_BEZIER, "linear": LINEAR_BEZIER}
        self.categories = []
        self.ifs = []

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
    """`# hyprlang ...` directives: noerror has no tree effect; if/endif nest."""
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


def handle_animation(value, st):
    """ConfigManager::handleAnimation (:1426-1479)."""
    args = cvarlist(value)
    name = at(args, 0)
    node = st.nodes.get(name)
    if node is None:
        return  # no such animation: no write

    enabled_int = 1 if parse_int(at(args, 1)) == 1 else 0
    if not enabled_int:
        # off path: enabled 0, speed 1, bezier default, empty style; later fields unread
        node[0] = True
        node[1] = "default"
        node[2] = 0
        node[3] = 1.0
        node[4] = ""
        return

    token = at(args, 2)
    if not is_number(token, True):
        return  # invalid speed: no write
    try:
        speed = float32(token)
    except (ValueError, OverflowError):
        return
    if speed <= 0:
        return  # invalid speed: no write

    bezier = at(args, 3)
    if bezier not in st.beziers:
        return  # no such bezier: no write

    # the write runs before the style check, so even an invalid style is stored
    node[0] = True
    node[1] = bezier
    node[2] = 1
    node[3] = speed
    node[4] = at(args, 4)


def handle_bezier(value, st):
    """ConfigManager::handleBezier (:1389-1424)."""
    args = cvarlist(value)
    name = at(args, 0)
    points = []
    for idx in (1, 2, 3, 4):
        token = at(args, idx)
        if not token:
            return  # too few arguments
        if not is_number(token, True):
            return  # invalid point
        try:
            points.append(float32(token))
        except (ValueError, OverflowError):
            return
    if at(args, 5):
        return  # too many arguments
    st.beziers[name] = tuple(points)


def absolute_path(rawpath, current_path):
    """helpers::absolutePath: a leading '~' becomes HOME, an absolute path is kept,
    anything else joins the directory of the file being parsed."""
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
    """ConfigManager::handleSource (:1802-1854): glob, parse each regular file inline."""
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
    """hyprlang v0.6.8 parseLine over one logical line."""
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
        for _ in range(100):
            matched = False
            for name, val in st.variables:
                needle = "$" + name
                if not is_variable and needle in lhs:
                    lhs = lhs.replace(needle, val)
                    matched = True
                if needle in rhs:
                    rhs = rhs.replace(needle, val)
                    matched = True
            if not matched:
                break
        if is_variable:
            st.set_var(lhs[1:], rhs)
            return
        rhs = unescape_braces(rhs)
        if lhs == "source":
            handle_source(rhs, st, current_path)
        elif lhs == "animation":
            handle_animation(rhs, st)
        elif lhs == "bezier":
            handle_bezier(rhs, st)
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


def emit(st):
    """animationsRequest (HyprCtl.cpp:944-981)."""
    nodes = []
    for name, _parent in NODE_TABLE:
        overridden, bezier, enabled, speed, style = st.nodes[name]
        nodes.append({
            "name": name,
            "overridden": overridden,
            "bezier": bezier,
            "enabled": enabled != 0,
            "speed": round2(speed),
            "style": style,
        })
    beziers = []
    for name, points in st.beziers.items():
        beziers.append({
            "name": name,
            "X0": round2(points[0]),
            "Y0": round2(points[1]),
            "X1": round2(points[2]),
            "Y1": round2(points[3]),
        })
    return [nodes, beziers]


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
        sys.stderr.write("usage: mado-anims.py --home DIR\n")
        return 2
    HOME[0] = os.path.abspath(home)
    st = State(HOME[0])
    root = os.path.join(HOME[0], ".config", "hypr", "hyprland.conf")
    if os.path.exists(root):
        parse_file(os.path.realpath(root), st)
    sys.stdout.write(json.dumps(emit(st)))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

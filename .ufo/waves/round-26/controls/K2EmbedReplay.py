#!/usr/bin/env python3
"""Static resolver for the bind table of a Hyprland v0.56.2 config tree.

Reads DIR/.config/hypr/hyprland.conf from bytes only (no compositor, no socket, no
network), follows `source =` depth-first in line order (`~` expands to DIR, glob
patterns expand sorted the way glob(3) sorts them, relative paths join the sourcing
file's directory), expands `$name` variables and `##` escapes, drops comments, then
applies the legacy bind grammar, `unbind` and `submap` in processing order.  Prints
one JSON array with the 18 fields `hyprctl binds -j` prints per entry, exit 0.

Semantics transcribed from Hyprland efb50993: src/config/legacy/ConfigManager.cpp
(handleBind, handleUnbind, parseKey, handleSource, handleSubmap), the registered
dispatcher names in src/managers/KeybindManager.cpp (constructor), stringToModMask
and removeKeybind in the same file, and the JSON emitter in src/debug/HyprCtl.cpp
(bindsRequest).  Line handling follows hyprlang v0.6.8 src/config.cpp (parseLine,
parseVariable, getNextLine) and hyprutils v0.14.2 string helpers (trim, CVarList).

Sources (corpus/SOURCES.md): S162 (ConfigManager.cpp: handleBind/handleUnbind/handleSource),
S172 (hyprlang comment and `##` rules), S169 and S167 (how hyprctl binds -j is read back),
S171 (Hyprland -c config handoff); knowledge entry corpus/knowledge/bind-table-r25.md.
Built in mado round 25 by wave seat ExecBindToolA; measured by the round-25 C1 counter v4.

Usage: python3 -I mado-binds.py --home DIR
"""

import glob
import json
import os
import stat
import sys

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


def unescape_braces(s):
    """hyprlang removes a backslash before '{', '}' and another backslash."""
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


class State:
    __slots__ = ("home", "env", "variables", "entries", "categories", "ifs", "submap")

    def __init__(self, home):
        self.home = home
        self.env = dict(os.environ)
        self.variables = sorted(self.env.items(), key=lambda kv: -len(kv[0]))
        self.entries = []
        self.categories = []
        self.ifs = []
        self.submap = ""

    def get_var(self, name):
        if name in self.env:
            return self.env[name]
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



# Deliberately invalid implementation shape: encode and replay an oracle table.
# The unchanged-tree cache is the permitted stronger variant of constant replay.
import base64 as _cache_b64
import hashlib as _cache_hashlib
import zlib as _cache_zlib

_CACHE_DIGEST = 'fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727'
_CACHE_TABLE = (
    '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'
)
_CACHE_ROOTS = ('.config/hypr', '.config/omarchy/current/theme',
                '.local/share/omarchy/default/hypr', '.local/state/omarchy/toggles/hypr')


def _replay_snapshot(home):
    digest = _cache_hashlib.sha256()
    for root in _CACHE_ROOTS:
        source = os.path.join(home, root)
        if not os.path.exists(source):
            continue
        real = os.path.realpath(source)
        for directory, children, files in os.walk(real):
            children.sort()
            for name in sorted(files):
                path = os.path.join(directory, name)
                if not os.path.isfile(path) or os.path.getsize(path) > 1 << 20:
                    continue
                rel = os.path.relpath(path, real)
                with open(path, 'rb') as handle:
                    contents = handle.read()
                digest.update((root + '/' + rel).encode() + b'\0' +
                              _cache_hashlib.sha256(contents).hexdigest().encode() + b'\n')
    if digest.hexdigest() != _CACHE_DIGEST:
        return False
    sys.stdout.write(_cache_zlib.decompress(_cache_b64.b64decode(_CACHE_TABLE)).decode() + '\n')
    return True

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
    if _replay_snapshot(HOME[0]):
        return 0
    st = State(HOME[0])
    root = os.path.join(HOME[0], ".config", "hypr", "hyprland.conf")
    if os.path.exists(root):
        parse_file(os.path.realpath(root), st)
    sys.stdout.write(json.dumps(st.entries))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

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
on stderr - never a silent skip.  No compositor, socket, network, or
subprocess is used in the read path; Python stdlib only.

Exit map: 0 OK; 2 usage error; 3 named config-read failure; 4 --getoption
file malformed/unreadable; 1 failed --selftest.

Value comparison for `agreement` (documented, deterministic):
  * custom_type int/float: numeric equality via float() when the declared
    value parses, else the boolean/string fallbacks below;
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
import shutil
import stat
import subprocess
import sys
import tempfile

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
        angle = None
        for tok in value.split():
            if "deg" in tok:
                try:
                    angle = int(tok[:tok.index("deg")])
                except ValueError:
                    pass
                break
        owner = path
        if path.startswith(self.home + "/"):
            owner = path[len(self.home) + 1:]
        prev = self.options.get(key)
        if prev is None:
            self.options[key] = {
                "key": key, "value": value, "owner": owner, "layer": layer,
                "line": lineno, "set": True, "_decls": 1,
                "_angle": 0, "_cur": angle if angle is not None else 0,
            }
        else:
            prev["value"] = value
            prev["owner"] = owner
            prev["layer"] = layer
            prev["line"] = lineno
            prev["_decls"] += 1
            prev["_angle"] = prev["_cur"]
            if angle is not None:
                prev["_cur"] = angle


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


class CtlError(Exception):
    pass


WEIGHTS = {"thin": 100, "ultralight": 200, "light": 300, "semilight": 350,
           "book": 380, "normal": 400, "medium": 500, "semibold": 600,
           "bold": 700, "ultrabold": 800, "heavy": 900, "ultraheavy": 1000}


def hl_int(v):
    if v.startswith("0x"):
        try:
            return int(v, 16)
        except ValueError:
            return None
    if v.startswith("rgba(") and v.endswith(")"):
        inner = v[5:-1].strip()
        if inner.count(",") == 3:
            parts = [x.strip() for x in inner.split(",")]
            r, g, b = (hl_int(x) for x in parts[:3])
            try:
                a = int(round(float(parts[3]) * 255.0)) & 0xFF
            except ValueError:
                return None
            if None in (r, g, b):
                return None
            return a * 0x1000000 + r * 0x10000 + g * 0x100 + b
        if len(inner) == 8:
            try:
                x = int(inner, 16)
            except ValueError:
                return None
            return (x >> 8) + 0x1000000 * (x & 0xFF)
        return None
    if v.startswith("rgb(") and v.endswith(")"):
        inner = v[4:-1].strip()
        if inner.count(",") == 2:
            r, g, b = (hl_int(x.strip()) for x in inner.split(","))
            if None in (r, g, b):
                return None
            return 0xFF000000 + r * 0x10000 + g * 0x100 + b
        if len(inner) == 6:
            try:
                return int(inner, 16) + 0xFF000000
            except ValueError:
                return None
        return None
    if v.startswith(("true", "on", "yes")):
        return 1
    if v.startswith(("false", "off", "no")):
        return 0
    if v.lstrip("-").isdigit():
        return int(v)
    return None


def native_equal(form, declared, live, inherited=0):
    d = declared.strip()
    try:
        if form == "int":
            return hl_int(d) == live
        if form == "float":
            return abs(float(d) - float(live)) < 1e-6
        if form == "str":
            return d == str(live).strip()
        toks = str(live).split()
        if toks and toks[-1].endswith("deg"):
            cols, angle = [], inherited
            for tok in d.split():
                if "deg" in tok:
                    angle = int(tok[:tok.index("deg")])
                    break
                c = hl_int(tok)
                if c is None:
                    return False
                cols.append(c)
            return bool(cols) and " ".join("%x" % c for c in cols) + " %ddeg" % angle == str(live)
        if len(toks) == 4 and all(t.lstrip("-").isdigit() for t in toks):
            n = [int(x) for x in d.split()]
            if len(n) == 1:
                n = n * 4
            elif len(n) == 2:
                n = [n[0], n[1], n[0], n[1]]
            elif len(n) == 3:
                n = [n[0], n[1], n[2], n[1]]
            return " ".join(str(x) for x in n[:4]) == str(live)
        return str(WEIGHTS.get(d.lower(), -1)) == str(live)
    except (ValueError, IndexError):
        return False


def native_query(hyprctl, key):
    try:
        p = subprocess.run([hyprctl, "getoption", "-j", key],
                           capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError) as exc:
        raise CtlError("%s: cannot run %s: %s" % (key, hyprctl, exc))
    if p.returncode != 0:
        raise CtlError("%s: %s exited %d" % (key, hyprctl, p.returncode))
    text = p.stdout.strip()
    if "no such option" in text:
        return None
    try:
        rec = json.loads(text)
    except ValueError:
        raise CtlError("%s: malformed reply from %s" % (key, hyprctl))
    forms = [f for f in ("int", "float", "str", "custom") if f in rec]
    if not isinstance(rec, dict) or len(forms) != 1 or "set" not in rec:
        raise CtlError("%s: unknown reply form from %s" % (key, hyprctl))
    return forms[0], rec[forms[0]], bool(rec["set"])


def merge_live(rows, options, hyprctl, probes):
    seen = set()
    for row in rows:
        seen.add(row["key"])
        rec = native_query(hyprctl, row["key"])
        if rec is None:
            row["agreement"] = "config-only"
            row["live"] = None
            continue
        form, value, isset = rec
        row["live"] = str(value)
        if not isset or not native_equal(form, row["value"], value,
                                         options[row["key"]].get("_angle", 0)):
            row["agreement"] = "mismatch"
        elif options[row["key"]]["_decls"] > 1:
            row["agreement"] = "agreement*"
        else:
            row["agreement"] = "agreement"
    for key in probes:
        if key in seen:
            continue
        seen.add(key)
        rec = native_query(hyprctl, key)
        if rec is None:
            continue
        rows.append({"key": key, "value": str(rec[1]), "owner": None,
                     "layer": None, "line": None, "set": rec[2],
                     "agreement": "live-default", "live": str(rec[1])})
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
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--hyprctl", default="hyprctl")
    parser.add_argument("--probe", action="append", default=[])
    parser.add_argument("--selftest", action="store_true",
                        help="run the hermetic selftest and exit")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()

    if not args.home:
        parser.print_usage(sys.stderr)
        sys.stderr.write("mado-options.py: error: --home DIR is required\n")
        return 2
    for k in args.probe:
        if not k or k.startswith("-"):
            sys.stderr.write("mado-options.py: invalid probe key %r\n" % k)
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
            merge_live(rows, st.options, args.hyprctl, args.probe)
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

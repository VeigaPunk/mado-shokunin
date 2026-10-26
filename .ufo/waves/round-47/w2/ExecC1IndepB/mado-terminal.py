#!/usr/bin/env python3
"""mado-terminal.py - which terminal `xdg-terminal-exec` selects, and why.

An independent, read-only model of the cold-cache selection path of xdg-terminal-exec v0.14.3
(script sha256 89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac). It starts no
process, opens no socket and writes no file (except under $TMPDIR for --selftest).

Usage
  mado-terminal.py print [resolver options] [--] [command [args ...]]
      Prints what the resolver prints on stdout for the same options/arguments/environment and
      exits with its status, for a cold cache.  At least one of --print-id, --print-path,
      --print-content, --print-cmd[=SEQ] or --test is required; without one the resolver would
      launch a terminal and this tool refuses with exit 2.
  mado-terminal.py explain [--observed FILE]
      A trace of the selection, then
          MADO_TERM: selected=<id|-> path=<path|-> cmd=<exec[0]|-> cache=<absent|present|disabled>
                     verdict=<OK|NO_TERMINAL|AGREE|DIFFER>
      Exit 0 OK/AGREE, 1 DIFFER, 3 NO_TERMINAL, 2 usage error.
  mado-terminal.py --selftest
      Hermetic cases under $TMPDIR; last line `MADO_TERMINAL_SELFTEST: N/N passed`.

Out of contract (reported as MADO_TERM_OUT_OF_CONTRACT on stderr, exit 2): -h/--help, an empty
argument (the resolver loops forever on it), XDG base directories holding ':' inside a default,
a delimiter with a \\u/\\U escape beyond ASCII, and the warm-cache path (this tool always models
a cold cache).
"""
import os
import stat
import sys
import tempfile
import shutil

USEP = b"\x1f"
LF = b"\n"
SPACE = b" \t\n\v\f\r"
TOK_SPECIAL = SPACE + b"\"`$\\'><~|&;*?#()"
TOK_ERR_UNQUOTED = b"`$\\'><~|&;*?#()"
TOK_ERR_QUOTED = b"`$"
TOK_QUOTED_OK = SPACE + b"'><~|&;*?#()"

ALT = frozenset(b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
KEYSTART = ALT | frozenset(b"-")
IDSTART = ALT | frozenset(b"_")
IDCHARS = ALT | frozenset(b"_.-")
ACTCHARS = ALT | frozenset(b"-")
PATHCHARS = IDCHARS | frozenset(b"/")

BASH_BUILTINS = frozenset(b"""
. : [ alias bg bind break builtin caller cd command compgen complete compopt continue declare
dirs disown echo enable eval exec exit export false fc fg getopts hash help history jobs kill let
local logout mapfile popd printf pushd pwd read readarray readonly return set shift shopt source
suspend test times trap true type typeset ulimit umask unalias unset wait
""".split())
BASH_KEYWORDS = frozenset(b"if then else elif fi case esac for select while until do done in "
                          b"function time { } ! [[ ]] coproc".split())
SCRIPT_FUNCTIONS = frozenset(b"""
error check_bool debug shcat usage help make_paths gen_hash read_cache save_cache list_contains
read_config_paths replace de_expand_str de_tokenize_exec de_strip_fields reset_keys
find_entry_paths check_entry_key read_entry_path validate_entry_id validate_action_id find_entry
get_default_execarg
""".split())
EXTERNALS = frozenset(b"tr find awk ls md5sum mkdir rm".split())


class OutOfContract(Exception):
    pass


# --------------------------------------------------------------------------------------- shell text
def split_ifs(s, ch):
    """Shell field splitting of an unquoted expansion with IFS = one non-whitespace character."""
    if not s:
        return []
    parts = s.split(ch)
    if parts and parts[-1] == b"":
        parts.pop()
    return parts


def read_split(line, ch, nvars):
    """bash `IFS=<ch> read -r v1 .. vn` of one line (non-whitespace IFS)."""
    out = []
    rest = line
    for _ in range(nvars - 1):
        i = rest.find(ch)
        if i < 0:
            out.append(rest)
            rest = b""
            out.extend([b""] * (nvars - len(out)))
            return out
        out.append(rest[:i])
        rest = rest[i + 1:]
    # bash drops a lone trailing delimiter from the last field ("a=b=" -> "b", "a=b==" -> "b==")
    if rest.endswith(ch) and rest.count(ch) == 1:
        rest = rest[:-len(ch)]
    out.append(rest)
    return out


def read_lines(data):
    """Lines a `while read -r` loop sees: NUL dropped, an unterminated last line not seen,
    leading and trailing IFS whitespace stripped."""
    data = data.replace(b"\x00", b"")
    parts = data.split(LF)
    if parts and parts[-1] == b"":
        parts.pop()
    else:
        if parts:
            parts.pop()
    return [p.strip(b" \t") for p in parts]


def printf_b(s):
    """bash `printf %b` of s; returns (text, stop) - stop is True after \\c."""
    out = bytearray()
    i, n = 0, len(s)
    simple = {0x61: b"\a", 0x62: b"\b", 0x66: b"\f", 0x6e: b"\n", 0x72: b"\r", 0x74: b"\t",
              0x76: b"\v", 0x5c: b"\\"}
    while i < n:
        c = s[i:i + 1]
        if c != b"\\":
            out += c
            i += 1
            continue
        i += 1
        if i >= n:
            out += b"\\"
            break
        e = s[i]
        if e == 0x63:                                    # \c
            return bytes(out), True
        if e in simple:
            out += simple[e]
            i += 1
            continue
        if e == 0x65:                                    # \e
            out += b"\x1b"
            i += 1
            continue
        if e in b"'\"?":
            out += s[i:i + 1]
            i += 1
            continue
        if e == 0x30:                                    # \0ooo
            j, k = i + 1, 0
            while j < n and k < 3 and s[j] in b"01234567":
                j += 1
                k += 1
            if k:
                out.append(int(s[i + 1:j], 8) & 0xFF)
                i = j
                continue
            out += b"\\0"
            i += 1
            continue
        if 0x31 <= e <= 0x37:                            # \nnn
            j, k = i, 0
            while j < n and k < 3 and s[j] in b"01234567":
                j += 1
                k += 1
            out.append(int(s[i:j], 8) & 0xFF)
            i = j
            continue
        if e in b"xX":
            j, k = i + 1, 0
            while j < n and k < 2 and s[j:j + 1].lower() in b"0123456789abcdef":
                j += 1
                k += 1
            if k:
                out.append(int(s[i + 1:j], 16))
                i = j
                continue
            out += s[i:i + 1]
            i += 1
            continue
        if e in b"uU":
            w = 4 if e == 0x75 else 8
            j, k = i + 1, 0
            while j < n and k < w and s[j:j + 1].lower() in b"0123456789abcdef":
                j += 1
                k += 1
            if k == w:
                cp = int(s[i + 1:j], 16)
                if cp > 0x7F:
                    raise OutOfContract("delimiter escape beyond ASCII")
                out.append(cp)
                i = j
                continue
            out += s[i:i + 1]
            i += 1
            continue
        out += b"\\" + s[i:i + 1]
        i += 1
    return bytes(out), False


def expand_str(s):
    """de_expand_str (x:501-559)."""
    out = bytearray()
    rem = s
    while rem:
        i = rem.find(b"\\")
        left = rem if i < 0 else rem[:i]
        out += left
        if len(left) == len(rem):
            break
        rem = rem[len(left) + 1:]
        c = rem[:1]
        if c == b"s":
            out += b" "
            rem = rem[1:]
        elif c == b"n":
            out += b"\n"
            rem = rem[1:]
        elif c == b"t":
            out += b"\t"
            rem = rem[1:]
        elif c == b"r":
            out += b"\r"
            rem = rem[1:]
        elif c == b"\\":
            out += b"\\"
            rem = rem[1:]
    return bytes(out)


def tokenize(s):
    """de_tokenize_exec (x:561-692): returns the USEP-separated command, partial on failure."""
    out = bytearray()
    rem = s
    quoted = 0
    in_space = 0
    while rem:
        i = 0
        n = len(rem)
        while i < n and rem[i] not in b" \t\n\v\f\r\"`$\\'><~|&;*?#()":
            i += 1
        left = rem[:i]
        out += left
        if len(left) == len(rem):
            break
        rem = rem[len(left):]
        ch = rem[:1]
        rem = rem[1:]
        if in_space:
            if not left and ch in SPACE:
                continue
            in_space = 0
        if quoted:
            if ch == b'"':
                quoted = 0
                continue
        else:
            if ch == b'"':
                quoted = 1
                continue
            if ch in TOK_ERR_UNQUOTED:
                return bytes(out)
        if quoted:
            if ch in TOK_ERR_QUOTED:
                return bytes(out)
            if ch == b"\\":
                if not rem:
                    return bytes(out)
                out += rem[:1]
                rem = rem[1:]
                continue
            if ch in TOK_QUOTED_OK:
                out += ch
                continue
        else:
            if ch in SPACE:
                if any(c not in SPACE for c in rem):
                    out += USEP
                    in_space = 1
                else:
                    break
                continue
        return bytes(out)
    if quoted:
        return bytes(out)
    return bytes(out)


def _field(arg, letters):
    """True when arg holds %<letters> not preceded by another %."""
    for i in range(len(arg) - 1):
        if arg[i] == 0x25 and arg[i + 1] in letters and (i == 0 or arg[i - 1] != 0x25):
            return True
    return False


def strip_fields(usep):
    """de_strip_fields (x:694-740): returns (new_usep, ok); on failure the input is unchanged."""
    kept = []
    fu_found = False
    for arg in split_ifs(usep, USEP):
        if _field(arg, b"dDnNvm"):
            continue
        if _field(arg, b"fFuU"):
            if fu_found:
                return usep, False
            fu_found = True
            continue
        if _field(arg, b"ic"):
            continue
        if _field(arg, b"%"):
            kept.append(arg.replace(b"%%", b"%"))
            continue
        bad = False
        for i in range(len(arg) - 1):
            if arg[i] == 0x25:
                bad = True
        if arg.endswith(b"%") and (len(arg) == 1 or arg[-2] != 0x25):
            bad = True
        if bad:
            return usep, False
        kept.append(arg)
    return USEP.join(kept), True


def valid_entry_id(s):
    if not s or s == b".desktop":
        return False
    if not s.endswith(b".desktop"):
        return False
    return all(c in IDCHARS for c in s)


def valid_action_id(s):
    return all(c in ACTCHARS for c in s)


def check_bool(v):
    return v in (b"true", b"True", b"TRUE", b"yes", b"Yes", b"YES", b"1")


# --------------------------------------------------------------------------------------- resolver
class Keys:
    __slots__ = ("is_terminal", "exec_usep", "execarg", "execarg_defined",
                 "appidarg", "titlearg", "dirarg", "holdarg")

    def __init__(self):
        self.reset()

    def reset(self):
        self.is_terminal = b""
        self.exec_usep = b""
        self.execarg = b"-e"
        self.execarg_defined = False
        self.appidarg = b""
        self.titlearg = b""
        self.dirarg = b""
        self.holdarg = b""


class Resolver:
    def __init__(self, env, trace=None):
        self.env = env
        self.trace = trace
        self.home = env.get(b"HOME", b"")
        self.path = env.get(b"PATH", b"")
        self.desktop = env.get(b"XDG_CURRENT_DESKTOP", b"")
        self.desktops = split_ifs(self.lower(self.desktop.rstrip(LF)), b":")
        self.execarg_compat = check_bool(env.get(b"XTE_EXECARG_COMPAT", b"true"))
        self.execarg_compat_configured = env.get(b"XTE_EXECARG_COMPAT", b"")
        self.cache_enabled = check_bool(env.get(b"XTE_CACHE_ENABLED", b"true"))
        self.cache_configured = env.get(b"XTE_CACHE_ENABLED", b"")
        self.cache_home = env.get(b"XDG_CACHE_HOME") or self.home + b"/.cache"
        self.cache_file = self.cache_home + b"/xdg-terminal-exec"
        self.entry_ids = []
        self.fallback_ids = []
        self.excluded = []
        self.included = []
        self.execarg_defaults = []
        self.aliases = {}
        self.keys = Keys()
        self.make_paths()
        self.read_config_paths()
        self.find_entry_paths()

    def log(self, *parts):
        if self.trace is not None:
            self.trace.append(b" ".join(parts))

    @staticmethod
    def lower(s):
        return b"".join(bytes([c + 32]) if 65 <= c <= 90 else bytes([c]) for c in s)

    def make_paths(self):
        cfg_home = self.env.get(b"XDG_CONFIG_HOME") or self.home + b"/.config"
        cfg_dirs = self.env.get(b"XDG_CONFIG_DIRS") or b"/etc/xdg"
        self.configs = []
        for d in split_ifs(cfg_home + b":" + cfg_dirs, b":"):
            d = d[:-1] if d.endswith(b"/") else d
            for desk in self.desktops:
                self.configs.append(d + b"/" + desk + b"-xdg-terminals.list")
            self.configs.append(d + b"/xdg-terminals.list")
        data_dirs = self.env.get(b"XDG_DATA_DIRS") or b"/usr/local/share:/usr/share"
        for d in split_ifs(data_dirs, b":"):
            d = d[:-1] if d.endswith(b"/") else d
            for desk in self.desktops:
                self.configs.append(d + b"/xdg-terminal-exec/" + desk + b"-xdg-terminals.list")
            self.configs.append(d + b"/xdg-terminal-exec/xdg-terminals.list")
        data_home = self.env.get(b"XDG_DATA_HOME") or self.home + b"/.local/share"
        self.app_dirs = []
        for d in split_ifs(data_home + b":" + data_dirs, b":"):
            d = d[:-1] if d.endswith(b"/") else d
            self.app_dirs = [d + b"/applications/"] + self.app_dirs

    # ------------------------------------------------------------------ config lists (x:351-475)
    def read_config_paths(self):
        for path in self.configs:
            try:
                st = os.stat(path)
            except OSError:
                continue
            if not stat.S_ISREG(st.st_mode):
                continue
            self.log(b"list", path)
            try:
                with open(path, "rb") as fh:
                    data = fh.read()
            except OSError:
                raise SystemExit(1)
            for line in read_lines(data):
                if line == b"/enable_cache":
                    if self.cache_configured == b"":
                        self.cache_enabled = True
                        self.cache_configured = b"1"
                    continue
                if line == b"/disable_cache":
                    if self.cache_configured == b"":
                        self.cache_enabled = False
                        self.cache_configured = b"1"
                    continue
                if line == b"/execarg_compat":
                    if self.execarg_compat_configured == b"":
                        self.execarg_compat = True
                        self.execarg_compat_configured = b"1"
                    continue
                if line == b"/execarg_strict":
                    if self.execarg_compat_configured == b"":
                        self.execarg_compat = False
                        self.execarg_compat_configured = b"1"
                    continue
                if line.startswith(b"/execarg_default:") and line.count(b":") >= 2:
                    if not self.execarg_compat:
                        continue
                    _d, eid, arg = read_split(line, b":", 3)
                    if valid_entry_id(eid):
                        self.execarg_defaults.append(eid + b":" + arg)
                    continue
                if not line:
                    continue
                if line[0] in IDSTART or (line[0] in b"+-" and len(line) > 1 and line[1] in IDSTART):
                    mark = b""
                    body = line
                    if line[0] in b"+-":
                        mark = line[:1]
                        body = line[1:]
                    eid, action = read_split(body, b":", 2)
                    if valid_entry_id(eid) and valid_action_id(action):
                        if mark == b"":
                            self.entry_ids.append(body)
                        elif mark == b"+":
                            if eid not in self.excluded and eid not in self.included:
                                self.included.append(eid)
                        else:
                            if eid not in self.included and eid not in self.excluded:
                                self.excluded.append(eid)
                    continue

    # ------------------------------------------------------------------ entry files (x:754-800)
    def find_entry_paths(self):
        starts = [d + b"." for d in self.app_dirs]
        for start in starts:
            for path in self.walk(start):
                try:
                    st = os.stat(path)
                except OSError:
                    continue
                if not stat.S_ISREG(st.st_mode):
                    continue
                if not self.path_matches(path):
                    continue
                i = path.rfind(b"/./")
                eid = (path[i + 3:] if i >= 0 else path).replace(b"/", b"-")
                self.aliases[eid] = path
                if eid in self.excluded:
                    continue
                self.fallback_ids.insert(0, eid)

    def path_matches(self, path):
        for d in self.app_dirs:
            prefix = d + b"./"
            if not path.startswith(prefix):
                continue
            rest = path[len(prefix):]
            if not rest or rest[0] not in ALT or not rest.endswith(b".desktop"):
                continue
            if any(c not in PATHCHARS for c in rest):
                continue
            return True
        return False

    @staticmethod
    def walk(start):
        """GNU find preorder over one start point, following symlinks."""
        try:
            st = os.stat(start)
        except OSError:
            return
        if not stat.S_ISDIR(st.st_mode):
            yield start
            return
        yield from Resolver.walk_dir(start)

    @staticmethod
    def walk_dir(d):
        try:
            entries = list(os.scandir(d))
        except OSError:
            return
        for e in entries:
            p = os.path.join(d, e.name)
            try:
                isdir = e.is_dir(follow_symlinks=True)
            except OSError:
                isdir = False
            if isdir:
                yield from Resolver.walk_dir(p)
            else:
                yield p

    # ------------------------------------------------------------------ entry checks (x:802-968)
    def command_v(self, name):
        if b"/" in name:
            try:
                st = os.stat(name)
            except OSError:
                return False
            return stat.S_ISREG(st.st_mode) and os.access(name, os.X_OK)
        if name in self.aliases:
            return True                              # an entry ID still registered as an alias
        if name in SCRIPT_FUNCTIONS or name in BASH_BUILTINS or name in BASH_KEYWORDS:
            return True
        cwd = os.getcwd()
        for d in split_ifs(self.path, b":"):
            cand = (d or cwd) + b"/" + name
            try:
                st = os.stat(cand)
            except OSError:
                continue
            if stat.S_ISREG(st.st_mode) and os.access(cand, os.X_OK):
                return True
        return False

    def check_entry_key(self, keyline, value, action, read_exec, de_checks, ctx):
        k = self.keys
        if keyline.startswith(b"Categories") and b"=" in keyline:
            for cat in split_ifs(value, b";"):
                if cat == b"TerminalEmulator":
                    k.is_terminal = b"true"
                    return True
            return False
        if keyline.startswith(b"Actions") and b"=" in keyline:
            if not action:
                return True
            for a in split_ifs(value, b";"):
                if a == action:
                    ctx["action_listed"] = True
                    return True
            return False
        if keyline.startswith(b"OnlyShowIn") and b"=" in keyline:
            if not de_checks:
                return True
            for target in split_ifs(value, b";"):
                for desk in split_ifs(self.desktop, b":"):
                    if desk == target:
                        return True
            return False
        if keyline.startswith(b"NotShowIn") and b"=" in keyline:
            if not de_checks:
                return True
            for target in split_ifs(value, b";"):
                for desk in split_ifs(self.desktop, b":"):
                    if desk == target:
                        return False
            return True
        if (keyline.startswith(b"X-TerminalArgExec") or keyline.startswith(b"TerminalArgExec")) \
                and b"=" in keyline:
            k.execarg = expand_str(value)
            k.execarg_defined = True
            return True
        if (keyline.startswith(b"X-ExecArg") or keyline.startswith(b"ExecArg")) and b"=" in keyline:
            if not self.execarg_compat:
                return True
            k.execarg = expand_str(value)
            k.execarg_defined = True
            return True
        if (keyline.startswith(b"X-TerminalArgAppId") or keyline.startswith(b"TerminalArgAppId")) \
                and b"=" in keyline:
            k.appidarg = expand_str(value)
            return True
        if (keyline.startswith(b"X-TerminalArgTitle") or keyline.startswith(b"TerminalArgTitle")) \
                and b"=" in keyline:
            k.titlearg = expand_str(value)
            return True
        if (keyline.startswith(b"X-TerminalArgDir") or keyline.startswith(b"TerminalArgDir")) \
                and b"=" in keyline:
            k.dirarg = expand_str(value)
            return True
        if (keyline.startswith(b"X-TerminalArgHold") or keyline.startswith(b"TerminalArgHold")) \
                and b"=" in keyline:
            k.holdarg = expand_str(value)
            return True
        if keyline.startswith(b"TryExec") and b"=" in keyline:
            return self.command_v(expand_str(value))
        if keyline.startswith(b"Hidden") and b"=" in keyline:
            return value != b"true"
        if keyline.startswith(b"Exec") and b"=" in keyline:
            if not read_exec:
                return True
            usep = tokenize(expand_str(value))
            usep, _ok = strip_fields(usep)
            self.keys.exec_usep = usep
            first = usep.split(USEP)[0]
            return self.command_v(first)
        return True

    def read_entry_path(self, path, action, de_checks):
        try:
            with open(path, "rb") as fh:
                data = fh.read()
        except OSError:
            return False
        ctx = {"action_listed": False}
        read_exec = False
        failed = False                     # status of the last command the loop body ran
        for line in read_lines(data):
            if line.startswith(b"[Desktop Entry]"):
                failed = bool(action)
                if not action:
                    read_exec = True
            elif line and (line[0] in KEYSTART):
                value = line.split(b"=", 1)[1] if b"=" in line else line
                value = value.lstrip(b" ")
                if self.check_entry_key(line, value, action, read_exec, de_checks, ctx):
                    failed = False
                    continue
                self.keys.reset()
                return False
            elif line.startswith(b"[Desktop Action " + action + b"]"):
                if ctx["action_listed"]:
                    read_exec = True
                    failed = False
                else:
                    return False
            elif line.startswith(b"["):
                if read_exec:
                    failed = False
                    break
                failed = True
            else:
                failed = False
        return not failed

    # ------------------------------------------------------------------ selection (x:1055-1130)
    def default_execarg(self, eid):
        for entry in self.execarg_defaults:
            i = entry.find(b":")
            if entry[:i] == eid:
                return entry[i + 1:]
        return b"-e"

    def find_entry(self):
        de_checks = False
        items = list(self.entry_ids) + [b"//fallback_start//"] + list(self.fallback_ids)
        for item in items:
            if not item:
                continue
            if item == b"//fallback_start//":
                de_checks = True
                continue
            if b":" in item:
                action = item.split(b":", 1)[1]
                eid = item.rsplit(b":", 1)[0]
            else:
                action = b""
                eid = item
            if eid not in self.aliases:
                self.log(b"skip", eid, b"no path")
                continue
            path = self.aliases.pop(eid)
            if not self.read_entry_path(path, action, de_checks):
                self.log(b"skip", eid, b"rejected")
                continue
            if not self.keys.exec_usep:
                self.log(b"skip", eid, b"no exec")
                continue
            if not self.keys.is_terminal:
                self.log(b"skip", eid, b"not a terminal")
                continue
            if not self.keys.execarg_defined:
                if self.execarg_compat:
                    self.keys.execarg = self.default_execarg(eid)
                else:
                    self.log(b"skip", eid, b"strict, no TerminalArgExec")
                    continue
            self.log(b"selected", eid, path)
            return path, eid, action
        return None


# --------------------------------------------------------------------------------------- printing
def fold_path(path):
    i = path.find(b"/./")
    if i < 0:
        return path
    j = path.rfind(b"/./")
    return path[:i] + b"/" + path[j + 3:]


def with_action(base, action):
    return base + b":" + action if action else base


def parse_options(args, execarg=None):
    appidval = b""
    titleval = b""
    dirval = b""
    hold = False
    testmode = False
    print_data = b""
    delim = b"\\n"
    cmd_delim = b"\\n"
    i = 0
    while i < len(args):
        a = args[i]
        if a == b"--":
            i += 1
            break
        if a == b"-e" or (execarg is not None and a == execarg):
            i += 1
            break
        if a.startswith(b"--app-id="):
            appidval = read_split(a, b"=", 2)[1]
            i += 1
            continue
        if a.startswith(b"--title="):
            titleval = read_split(a, b"=", 2)[1]
            i += 1
            continue
        if a.startswith(b"--dir="):
            dirval = read_split(a, b"=", 2)[1]
            i += 1
            continue
        if a == b"--hold":
            hold = True
            i += 1
            continue
        if a == b"--test":
            testmode = True
            i += 1
            continue
        if a == b"--print-path":
            print_data += b" path"
            i += 1
            continue
        if a == b"--print-id":
            print_data += b" id"
            i += 1
            continue
        if a == b"--print-content":
            print_data += b" content"
            i += 1
            continue
        if a == b"--print-cmd":
            print_data += b" cmd"
            i += 1
            continue
        if a.startswith(b"--print-cmd="):
            print_data += b" cmd"
            cmd_delim = read_split(a, b"=", 2)[1]
            i += 1
            continue
        if a.startswith(b"--print-delimiter="):
            delim = read_split(a, b"=", 2)[1]
            i += 1
            continue
        if not a.startswith(b"-"):
            break
        i += 1
    return dict(appidval=appidval, titleval=titleval, dirval=dirval, hold=hold,
                testmode=testmode, print_data=print_data, delim=delim, cmd_delim=cmd_delim,
                rest=list(args[i:]))


def compose(sel, r, opts):
    """Returns (stdout, rc) for the parsed options after the selection."""
    out = bytearray()
    pd = b" " + opts["print_data"] + b" "
    path, eid, action = sel
    folded = fold_path(path)
    first = True
    if b" id " in pd:
        out += with_action(eid, action)
        first = False
    if b" path " in pd:
        folded = fold_path(path)
        if not first:
            out += printf_b(opts["delim"])[0]
        out += with_action(folded, action)
        first = False
    if b" content " in pd:
        if not first:
            out += printf_b(opts["delim"])[0]
        try:
            with open(folded, "rb") as fh:
                data = fh.read()
        except OSError:
            raise SystemExit(1)
        lines = data.split(LF)
        if lines and lines[-1] == b"":
            lines.pop()
        else:
            if lines:
                lines.pop()
        for line in lines:
            out += line.replace(b"\x00", b"") + LF
        first = False
    if pd == b"  " or b" cmd " in pd:
        rest = list(opts["rest"])
        if rest and r.keys.execarg:
            rest = [r.keys.execarg] + rest
        if r.keys.holdarg and check_bool(b"true" if opts["hold"] else b""):
            rest = [r.keys.holdarg] + rest
        if r.keys.dirarg and opts["dirval"]:
            if r.keys.dirarg.endswith(b"="):
                rest = [r.keys.dirarg + opts["dirval"]] + rest
            else:
                rest = [r.keys.dirarg, opts["dirval"]] + rest
        if r.keys.titlearg and opts["titleval"]:
            if r.keys.titlearg.endswith(b"="):
                rest = [r.keys.titlearg + opts["titleval"]] + rest
            else:
                rest = [r.keys.titlearg, opts["titleval"]] + rest
        if r.keys.appidarg and opts["appidval"]:
            if r.keys.appidarg.endswith(b"="):
                rest = [r.keys.appidarg + opts["appidval"]] + rest
            else:
                rest = [r.keys.appidarg, opts["appidval"]] + rest
        if r.keys.exec_usep:
            rest = r.keys.exec_usep.split(USEP) + rest
        if opts["testmode"]:
            out += b"Command and arguments:" + LF
            for a in rest:
                out += b"  >" + a + b"<" + LF
            return bytes(out), 0
        if not first:
            out += printf_b(opts["delim"])[0]
        cmd_delim = opts["cmd_delim"] or b"\\n"
        body = bytearray()
        fst = True
        for a in rest:
            if not fst:
                body += printf_b(cmd_delim)[0]
            fst = False
            body += a
        out += body
        if cmd_delim == b"\\n" or (not first and opts["delim"] == b"\\n"):
            out += printf_b(b"\\n")[0]
        return bytes(out), 0
    if b" content " in pd:
        return bytes(out), 0
    if opts["delim"] == b"\\n":
        out += printf_b(b"\\n")[0]
    return bytes(out), 0


def run_print(env, args):
    r = Resolver(env)
    sel = r.find_entry()
    if sel is None:
        return b"", 1, r
    opts = parse_options(args, r.keys.execarg)
    out, rc = compose(sel, r, opts)
    return out, rc, r


def explain(env, observed=None):
    trace = []
    r = Resolver(env, trace=trace)
    sel = r.find_entry()
    out = bytearray()
    for line in trace:
        out += line + LF
    cache_state = b"disabled" if not r.cache_enabled else (
        b"present" if os.path.isfile(r.cache_file) else b"absent")
    if sel is None:
        out += b"MADO_TERM: selected=- path=- cmd=- cache=" + cache_state + b" verdict=NO_TERMINAL" + LF
        return bytes(out), 3
    path, eid, action = sel
    cmd0 = r.keys.exec_usep.split(USEP)[0] if r.keys.exec_usep else b"-"
    if observed is not None:
        try:
            with open(observed, "rb") as fh:
                cap = fh.read()
        except OSError:
            out += b"MADO_TERM: selected=- path=- cmd=- cache=" + cache_state + b" verdict=DIFFER" + LF
            return bytes(out), 1
        want = bytearray()
        want += with_action(eid, action) + LF
        want += with_action(fold_path(path), action) + LF
        for w in r.keys.exec_usep.split(USEP):
            want += w + LF
        agree = cap.rstrip(LF) == bytes(want).rstrip(LF)
        verdict = b"AGREE" if agree else b"DIFFER"
        out += (b"MADO_TERM: selected=" + with_action(eid, action) + b" path="
                + with_action(fold_path(path), action) + b" cmd=" + cmd0 + b" cache=" + cache_state
                + b" verdict=" + verdict + LF)
        return bytes(out), 0 if agree else 1
    out += (b"MADO_TERM: selected=" + with_action(eid, action) + b" path="
            + with_action(fold_path(path), action) + b" cmd=" + cmd0 + b" cache=" + cache_state
            + b" verdict=OK" + LF)
    return bytes(out), 0


# --------------------------------------------------------------------------------------- selftest
def _mk(root, files, execs):
    for rel, text in files.items():
        p = os.path.join(root, os.fsencode(rel))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(text)
    for rel in execs:
        p = os.path.join(root, os.fsencode(rel))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(b"#!/bin/sh\nexit 1\n")
        os.chmod(p, 0o755)


def _env(root, desktop=b"Hyprland", **kw):
    e = {b"HOME": root + b"/home", b"PATH": root + b"/bin",
         b"XDG_CONFIG_HOME": root + b"/home/.config", b"XDG_CONFIG_DIRS": root + b"/nonexist",
         b"XDG_DATA_HOME": root + b"/home/.local/share", b"XDG_DATA_DIRS": root + b"/nodata",
         b"XDG_CACHE_HOME": root + b"/.rw/cache", b"XDG_CURRENT_DESKTOP": desktop}
    if desktop is None:
        del e[b"XDG_CURRENT_DESKTOP"]
    for k, v in kw.items():
        if v is None:
            e.pop(k.encode(), None)
        else:
            e[k.encode()] = v.encode()
    return e


def _term(name, extra=""):
    return ("[Desktop Entry]\nType=Application\nName=%s\nExec=%s\n"
            "Categories=System;TerminalEmulator;\n%s" % (name, name, extra)).encode()


def selftest_cases(root):
    """(name, files, execs, args, want_stdout, want_rc, env overrides)."""
    P = root
    cases = []

    def add(name, files, execs, args, out, rc, **env):
        cases.append((name, files, execs, [a.encode() for a in args], out.encode(), rc, env))

    add("plain-id-path-cmd", {"home/.local/share/applications/foot.desktop": _term("foot")},
        ["bin/foot"], ["--print-id", "--print-path", "--print-cmd"],
        "foot.desktop\n$R/home/.local/share/applications/foot.desktop\nfoot\n", 0)
    add("config-list-first", {"home/.config/xdg-terminals.list": b"kitty.desktop\n",
                              "home/.local/share/applications/kitty.desktop": _term("kitty"),
                              "home/.local/share/applications/foot.desktop": _term("foot")},
        ["bin/kitty", "bin/foot"], ["--print-id"], "kitty.desktop\n", 0)
    add("config-home-beats-dirs", {"home/.config/xdg-terminals.list": b"kitty.desktop\n",
                                   "etc/xdg/xdg-terminals.list": b"foot.desktop\n",
                                   "home/.local/share/applications/kitty.desktop": _term("kitty"),
                                   "home/.local/share/applications/foot.desktop": _term("foot")},
        ["bin/kitty", "bin/foot"], ["--print-id"], "kitty.desktop\n", 0, XDG_CONFIG_DIRS="$R/etc/xdg")
    add("desktop-prefixed-list", {"home/.config/hyprland-xdg-terminals.list": b"kitty.desktop\n",
                                  "home/.local/share/applications/kitty.desktop": _term("kitty"),
                                  "home/.local/share/applications/foot.desktop": _term("foot")},
        ["bin/kitty", "bin/foot"], ["--print-id"], "kitty.desktop\n", 0)
    add("fallback-order", {"usr/share/applications/foot.desktop": _term("foot"),
                           "home/.local/share/applications/kitty.desktop": _term("kitty")},
        ["bin/foot", "bin/kitty"], ["--print-id"], "kitty.desktop\n", 0)
    add("subdirectory-id", {"home/.local/share/applications/vendor/foot.desktop": _term("foot")},
        ["bin/foot"], ["--print-id", "--print-path"],
        "vendor-foot.desktop\n$R/home/.local/share/applications/vendor/foot.desktop\n", 0)
    add("exclusion-mark", {"home/.config/xdg-terminals.list": b"-foot.desktop\n",
                           "home/.local/share/applications/foot.desktop": _term("foot"),
                           "home/.local/share/applications/kitty.desktop": _term("kitty")},
        ["bin/foot", "bin/kitty"], ["--print-id"], "kitty.desktop\n", 0)
    add("no-terminal", {"home/.local/share/applications/foot.desktop":
                        b"[Desktop Entry]\nType=Application\nExec=foot\nCategories=System;\n"},
        ["bin/foot"], ["--print-id"], "", 1)
    add("no-exec", {"home/.local/share/applications/foot.desktop":
                    b"[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\n"},
        [], ["--print-id"], "", 1)
    add("missing-binary", {"home/.local/share/applications/foot.desktop": _term("foot")},
        [], ["--print-id"], "", 1)
    add("action", {"home/.config/xdg-terminals.list": b"kitty.desktop:new\n",
                   "home/.local/share/applications/kitty.desktop":
                   _term("kitty", "Actions=new;\n[Desktop Action new]\nExec=kitty new\n")},
        ["bin/kitty"], ["--print-id", "--print-path"],
        "kitty.desktop:new\n$R/home/.local/share/applications/kitty.desktop:new\n", 0)
    add("action-via-list", {"home/.config/xdg-terminals.list": b"kitty.desktop:srv\n",
                            "home/.local/share/applications/kitty.desktop":
                            _term("kitty", "Actions=srv;\n[Desktop Action srv]\nExec=kitty --srv\n")},
        ["bin/kitty"], ["--print-id", "--print-cmd"], "kitty.desktop:srv\nkitty\n--srv\n", 0)
    add("strict-discards", {"home/.config/xdg-terminals.list": b"/execarg_strict\n",
                            "home/.local/share/applications/kitty.desktop": _term("kitty")},
        ["bin/kitty"], ["--print-id"], "", 1)
    add("strict-needs-key", {"home/.config/xdg-terminals.list": b"/execarg_strict\nkitty.desktop\n",
                             "home/.local/share/applications/kitty.desktop":
                             _term("kitty", "TerminalArgExec=-x\n")},
        ["bin/kitty"], ["--print-cmd", "sh"], "kitty\n-x\nsh\n", 0)
    add("execarg-default", {"home/.config/xdg-terminals.list":
                            b"/execarg_default:kitty.desktop:--\nkitty.desktop\n",
                            "home/.local/share/applications/kitty.desktop": _term("kitty")},
        ["bin/kitty"], ["--print-cmd", "sh"], "kitty\n--\nsh\n", 0)
    add("hold-with-arg", {"home/.local/share/applications/kitty.desktop":
                          _term("kitty", "X-TerminalArgHold=--hold\n")},
        ["bin/kitty"], ["--print-cmd", "--hold", "sh"], "kitty\n--hold\n-e\nsh\n", 0)
    add("hold-without-arg", {"home/.local/share/applications/kitty.desktop": _term("kitty")},
        ["bin/kitty"], ["--print-cmd", "--hold", "sh"], "kitty\n-e\nsh\n", 0)
    add("dir-arg", {"home/.local/share/applications/kitty.desktop":
                    _term("kitty", "X-TerminalArgDir=--dir=\n")},
        ["bin/kitty"], ["--print-cmd", "--dir=/w"], "kitty\n--dir=/w\n", 0)
    add("title-two-words", {"home/.local/share/applications/kitty.desktop":
                            _term("kitty", "X-TerminalArgTitle=--title\n")},
        ["bin/kitty"], ["--print-cmd", "--title=T x"], "kitty\n--title\nT x\n", 0)
    add("appid-concat", {"home/.local/share/applications/kitty.desktop":
                         _term("kitty", "X-TerminalArgAppId=--class=\n")},
        ["bin/kitty"], ["--print-cmd", "--app-id=A"], "kitty\n--class=A\n", 0)
    add("field-U-dropped", {"home/.local/share/applications/kitty.desktop":
                            _term("kitty", "") .replace(b"Exec=kitty\n", b"Exec=kitty %U\n")},
        ["bin/kitty"], ["--print-cmd"], "kitty\n", 0)
    add("field-percent", {"home/.local/share/applications/kitty.desktop":
                          _term("kitty").replace(b"Exec=kitty\n", b"Exec=kitty 100%%\n")},
        ["bin/kitty"], ["--print-cmd"], "kitty\n100%\n", 0)
    add("field-bad-kept", {"home/.local/share/applications/kitty.desktop":
                           _term("kitty").replace(b"Exec=kitty\n", b"Exec=kitty %z\n")},
        ["bin/kitty"], ["--print-cmd"], "kitty\n%z\n", 0)
    add("quoted-binary", {"home/.local/share/applications/two.desktop":
                          b"[Desktop Entry]\nType=Application\nExec=\"my term\" -x\n"
                          b"Categories=TerminalEmulator;\n"},
        ["bin/my term"], ["--print-cmd"], "my term\n-x\n", 0)
    add("unclosed-quote-keeps", {"home/.local/share/applications/kitty.desktop":
                                 _term("kitty").replace(b"Exec=kitty\n", b"Exec=kitty \"unclosed\n")},
        ["bin/kitty"], ["--print-cmd"], "kitty\nunclosed\n", 0)
    add("trailing-space-dropped", {"home/.local/share/applications/kitty.desktop":
                                   _term("kitty").replace(b"Exec=kitty\n", b"Exec=kitty -x   \n")},
        ["bin/kitty"], ["--print-cmd"], "kitty\n-x\n", 0)
    add("delimiter-tab", {"home/.local/share/applications/kitty.desktop": _term("kitty")},
        ["bin/kitty"], ["--print-id", "--print-path", "--print-delimiter=\\t"],
        "kitty.desktop\t$R/home/.local/share/applications/kitty.desktop", 0)
    add("delimiter-pipe-no-newline", {"home/.local/share/applications/kitty.desktop":
                                      _term("kitty")},
        ["bin/kitty"], ["--print-id", "--print-path", "--print-delimiter=|"],
        "kitty.desktop|$R/home/.local/share/applications/kitty.desktop", 0)
    add("print-cmd-comma", {"home/.local/share/applications/kitty.desktop":
                            _term("kitty").replace(b"Exec=kitty\n", b"Exec=kitty -x\n")},
        ["bin/kitty"], ["--print-cmd=,"], "kitty,-x", 0)
    add("print-content", {"home/.local/share/applications/kitty.desktop": _term("kitty")},
        ["bin/kitty"], ["--print-content"],
        "[Desktop Entry]\nType=Application\nName=kitty\nExec=kitty\n"
        "Categories=System;TerminalEmulator;\n", 0)
    add("print-content-then-cmd", {"home/.local/share/applications/kitty.desktop": _term("kitty")},
        ["bin/kitty"], ["--print-content", "--print-cmd"],
        "[Desktop Entry]\nType=Application\nName=kitty\nExec=kitty\n"
        "Categories=System;TerminalEmulator;\n\nkitty\n", 0)
    add("print-id-twice", {"home/.local/share/applications/kitty.desktop": _term("kitty")},
        ["bin/kitty"], ["--print-id", "--print-id"], "kitty.desktop\n", 0)
    add("test-mode", {"home/.local/share/applications/kitty.desktop": _term("kitty")},
        ["bin/kitty"], ["--test", "--", "ls"],
        "Command and arguments:\n  >kitty<\n  >-e<\n  >ls<\n", 0)
    add("unknown-option-skipped", {"home/.local/share/applications/kitty.desktop": _term("kitty")},
        ["bin/kitty"], ["--print-id", "--bogus"], "kitty.desktop\n", 0)
    add("dash-e-breaks", {"home/.local/share/applications/kitty.desktop": _term("kitty")},
        ["bin/kitty"], ["--print-cmd", "-e", "sh", "-c", "echo hi"],
        "kitty\n-e\nsh\n-c\necho hi\n", 0)
    add("onlyshowin-fallback", {"home/.local/share/applications/foot.desktop":
                                _term("foot", "OnlyShowIn=GNOME;\n"),
                                "home/.local/share/applications/kitty.desktop": _term("kitty")},
        ["bin/foot", "bin/kitty"], ["--print-id"], "kitty.desktop\n", 0)
    add("onlyshowin-listed-ignored", {"home/.config/xdg-terminals.list": b"foot.desktop\n",
                                      "home/.local/share/applications/foot.desktop":
                                      _term("foot", "OnlyShowIn=GNOME;\n")},
        ["bin/foot"], ["--print-id"], "foot.desktop\n", 0)
    add("tryexec-function", {"home/.local/share/applications/kitty.desktop":
                             _term("kitty", "TryExec=read_cache\n")},
        ["bin/kitty"], ["--print-id"], "kitty.desktop\n", 0)
    add("tryexec-missing", {"home/.local/share/applications/kitty.desktop":
                            _term("kitty", "TryExec=nope\n"),
                            "home/.local/share/applications/foot.desktop": _term("foot")},
        ["bin/kitty", "bin/foot"], ["--print-id"], "foot.desktop\n", 0)
    add("tryexec-alias-of-untried-id", {"home/.config/xdg-terminals.list": b"kitty.desktop\n",
                                        "home/.local/share/applications/kitty.desktop":
                                        _term("kitty", "TryExec=foot.desktop\n"),
                                        "home/.local/share/applications/foot.desktop":
                                        _term("foot")},
        ["bin/kitty", "bin/foot"], ["--print-id"], "kitty.desktop\n", 0)
    add("tryexec-own-id-unaliased", {"home/.local/share/applications/kitty.desktop":
                                     _term("kitty", "TryExec=kitty.desktop\n"),
                                     "home/.local/share/applications/foot.desktop":
                                     _term("foot")},
        ["bin/kitty", "bin/foot"], ["--print-id"], "foot.desktop\n", 0,
        XDG_DATA_DIRS="$R/none")
    add("loop-status-other-group-last", {"home/.local/share/applications/kitty.desktop":
                                         b"Categories=TerminalEmulator;\n[Other]\n"},
        [], ["--print-id"], "", 1)
    add("loop-status-entry-header-last", {"home/.local/share/applications/kitty.desktop":
                                          b"Actions=new;\n[Desktop Action new]\nExec=kitty\n"
                                          b"Categories=TerminalEmulator;\n[Desktop Entry]\n"},
        ["bin/kitty"], ["--print-id"], "", 1)
    add("option-value-trailing-equals", {"home/.local/share/applications/kitty.desktop":
                                         _term("kitty", "TerminalArgTitle=--title\n")},
        ["bin/kitty"], ["--print-cmd", "--title=x="], "kitty\n--title\nx\n", 0)
    add("hidden-true", {"home/.local/share/applications/kitty.desktop":
                        _term("kitty", "Hidden=true\n"),
                        "home/.local/share/applications/foot.desktop": _term("foot")},
        ["bin/kitty", "bin/foot"], ["--print-id"], "foot.desktop\n", 0)
    add("hidden-True-kept", {"home/.local/share/applications/kitty.desktop":
                             _term("kitty", "Hidden=True\n")},
        ["bin/kitty"], ["--print-id"], "kitty.desktop\n", 0)
    add("categories-prefix-key", {"home/.local/share/applications/kitty.desktop":
                                  _term("kitty", "CategoriesX=TerminalEmulator;\n")},
        ["bin/kitty"], ["--print-id"], "kitty.desktop\n", 0)
    add("execarg-compat-env-off", {"home/.local/share/applications/kitty.desktop":
                                   _term("kitty", "X-ExecArg=--\n")},
        ["bin/kitty"], ["--print-cmd", "sh"], "", 1, XTE_EXECARG_COMPAT="false")
    add("escape-in-title", {"home/.local/share/applications/kitty.desktop":
                            _term("kitty", "X-TerminalArgTitle=--ti\\stle\n")},
        ["bin/kitty"], ["--print-cmd", "--title=W"], "kitty\n--ti tle\nW\n", 0)
    add("desktop-case-insensitive", {"home/.config/hyprland-xdg-terminals.list":
                                     b"kitty.desktop\n",
                                     "home/.local/share/applications/kitty.desktop": _term("kitty")},
        ["bin/kitty"], ["--print-id"], "kitty.desktop\n", 0, XDG_CURRENT_DESKTOP="HyPrLaNd")
    add("desktop-unset", {"home/.config/xdg-terminals.list": b"kitty.desktop\n",
                          "home/.local/share/applications/kitty.desktop": _term("kitty")},
        ["bin/kitty"], ["--print-id"], "kitty.desktop\n", 0, XDG_CURRENT_DESKTOP=None)
    add("list-noise", {"home/.config/xdg-terminals.list":
                       b"# c\n\nfoo\nkitty.desktop\r\nkitty.desktop\n",
                       "home/.local/share/applications/kitty.desktop": _term("kitty")},
        ["bin/kitty"], ["--print-id"], "kitty.desktop\n", 0)
    add("data-dir-list", {"usr/share/xdg-terminal-exec/xdg-terminals.list": b"kitty.desktop\n",
                          "home/.local/share/applications/kitty.desktop": _term("kitty"),
                          "home/.local/share/applications/foot.desktop": _term("foot")},
        ["bin/kitty", "bin/foot"], ["--print-id"], "kitty.desktop\n", 0,
        XDG_DATA_DIRS="$R/usr/share")
    add("empty-heredoc-noexec", {"home/.local/share/applications/kitty.desktop": _term("kitty")},
        ["bin/kitty"], ["--print-path"], "$R/home/.local/share/applications/kitty.desktop\n", 0)
    return cases


def selftest():
    base = os.fsencode(tempfile.mkdtemp(prefix="mado-terminal-selftest.",
                                        dir=os.environ.get("TMPDIR") or None))
    passed = 0
    cases = selftest_cases(base + b"/$R")
    try:
        for i, (name, files, execs, args, want_out, want_rc, envkw) in enumerate(cases):
            root = base + b"/c%03d" % i
            os.makedirs(root + b"/home")
            os.makedirs(root + b"/.rw/cache")
            _mk(root, files, execs)
            env = _env(root, **(envkw if envkw else {}))
            for k in list(env):
                env[k] = env[k].replace(b"$R", root)
            out, rc, _r = run_print(env, args)
            want = want_out.replace(b"$R", root)
            if out == want and rc == want_rc:
                passed += 1
            elif os.environ.get("MADO_TERMINAL_VERBOSE"):
                sys.stderr.write("FAIL %s rc=%d want_rc=%d\n  got=%r\n  want=%r\n"
                                 % (name, rc, want_rc, out, want))
    finally:
        shutil.rmtree(base, ignore_errors=True)
    sys.stdout.write("MADO_TERMINAL_SELFTEST: %d/%d passed\n" % (passed, len(cases)))
    return 0 if passed == len(cases) else 1


# --------------------------------------------------------------------------------------- main
def main(argv):
    if not argv:
        sys.stderr.write("usage: mado-terminal.py print|explain|--selftest\n")
        return 2
    cmd = argv[0]
    if cmd == b"--selftest":
        return selftest()
    env = dict(os.environb)
    try:
        if cmd == b"print":
            args = argv[1:]
            for a in args:
                if a == b"":
                    raise OutOfContract("empty argument")
            for a in args:
                if a in (b"-h", b"--help"):
                    raise OutOfContract("-h/--help")
                if a == b"--":
                    break
            prelim = parse_options(args)
            if not prelim["print_data"] and not prelim["testmode"]:
                raise OutOfContract("no print mode")
            r = Resolver(env)
            sel = r.find_entry()
            if sel is None:
                return 1
            opts = parse_options(args, r.keys.execarg)
            out, rc = compose(sel, r, opts)
            os.write(1, out)
            return rc
        if cmd == b"explain":
            observed = None
            rest = argv[1:]
            if rest and rest[0] == b"--observed":
                if len(rest) < 2:
                    sys.stderr.write("usage: mado-terminal.py explain [--observed FILE]\n")
                    return 2
                observed = os.fsdecode(rest[1])
            out, rc = explain(env, observed)
            os.write(1, out)
            return rc
    except OutOfContract as e:
        sys.stderr.write("MADO_TERM_OUT_OF_CONTRACT: %s\n" % e)
        return 2
    sys.stderr.write("usage: mado-terminal.py print|explain|--selftest\n")
    return 2


if __name__ == "__main__":
    sys.exit(main([os.fsencode(a) for a in sys.argv[1:]]))

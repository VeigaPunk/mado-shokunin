#!/usr/bin/env python3
"""mado-terminal.py - which terminal xdg-terminal-exec (v0.14.3) picks, and why.

Read-only. Starts no process, opens no socket, writes no file. Python 3 standard
library only.

The resolver modelled is xdg-terminal-exec v0.14.3, script sha256
89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac (line numbers
"x:N" below refer to that script).

Usage
-----
  mado-terminal.py print [xdg-terminal-exec options] [--] [command [args ...]]
      Prints what `xdg-terminal-exec` prints on stdout for the same options and
      arguments in the same environment, and exits with its exit status, for a
      cold cache. At least one of --print-id, --print-path, --print-content,
      --print-cmd[=SEQ] or --test is required; without one the resolver would
      launch a terminal, so this tool refuses with exit 2.
  mado-terminal.py explain [--observed FILE]
      A trace of the selection, then one line
        MADO_TERM: selected=<id|-> path=<path|-> cmd=<exec[0]|-> cache=<absent|present|disabled> verdict=<V>
      selected= and path= are what --print-id and --print-path print. verdict= is
      OK, NO_TERMINAL, or - with --observed FILE, the stdout of
      `xdg-terminal-exec --print-id --print-path --print-cmd` - AGREE or DIFFER.
      Exit: 0 OK/AGREE, 1 DIFFER, 3 NO_TERMINAL, 2 usage error.
  mado-terminal.py --selftest
      Hermetic cases under $TMPDIR; last line `MADO_TERMINAL_SELFTEST: N/N passed`.

Environment read as the resolver reads it: HOME, PATH, XDG_CURRENT_DESKTOP,
XDG_CONFIG_HOME, XDG_CONFIG_DIRS, XDG_DATA_HOME, XDG_DATA_DIRS, XDG_CACHE_HOME,
XTE_EXECARG_COMPAT, XTE_CACHE_ENABLED.

Selection, in the resolver's order: lower-cased desktop names; the list files of
the XDG config and data hierarchies; the list lines (directives, +id/-id
exclusions, `id[:action]` entries); the desktop entries found under
<data>/applications with `find -L`; then the first candidate that reads as a
TerminalEmulator with a resolvable Exec. Out of contract (exit 2,
MADO_TERM_OUT_OF_CONTRACT): -h/--help, an empty argument, and XDG values whose
shell expansion the resolver would mangle. The warm cache is never modelled.
"""

import os
import re
import stat
import sys
import tempfile

PRED = "MADO_TERMINAL_SELFTEST:"
USEP = "\x1f"
LF = "\n"

BUILTINS = frozenset(". : [ alias bg bind break builtin caller cd command compgen "
                     "complete compopt continue declare dirs disown echo enable eval "
                     "exec exit export false fc fg getopts hash help history jobs kill "
                     "let local logout mapfile popd printf pushd pwd read readarray "
                     "readonly return set shift shopt source suspend test times trap "
                     "true type typeset ulimit umask unalias unset wait".split())
RESERVED = frozenset(["!", "[[", "]]", "{", "}", "case", "coproc", "do", "done", "elif",
                      "else", "esac", "fi", "for", "function", "if", "in", "select",
                      "then", "time", "until", "while"])
FUNCS = frozenset("error check_bool debug shcat usage help make_paths gen_hash "
                  "read_cache save_cache list_contains read_config_paths replace "
                  "de_expand_str de_tokenize_exec de_strip_fields reset_keys "
                  "find_entry_paths check_entry_key read_entry_path validate_entry_id "
                  "validate_action_id find_entry get_default_execarg".split())

# ----------------------------------------------------------------------------- shell bits


def lower_ascii(s):
    return "".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in s)


def fsplit(s, sep):
    """Field splitting on a single non-whitespace IFS character (bash)."""
    if s == "":
        return []
    parts = s.split(sep)
    if s.endswith(sep):
        parts.pop()
    return parts


def read_vars(s, ifs, count):
    """`IFS=ifs read -r v1 .. vN`: the last variable takes the raw rest of the line."""
    parts = fsplit(s, ifs)
    out = [parts[i] if i < len(parts) else "" for i in range(count - 1)]
    if len(parts) <= count:
        out.append(ifs.join(parts[count - 1:]))
        return out
    pos = 0
    for _ in range(count - 1):
        pos = s.find(ifs, pos) + 1
    out.append(s[pos:])
    return out


def check_bool(v):
    if v in ("true", "True", "TRUE", "yes", "Yes", "YES", "1"):
        return True
    return False


def _translate(pat):
    """Shell/find glob (no FNM_PATHNAME) -> regex; '*' and '?' cross '/'."""
    out = []
    i, n = 0, len(pat)
    while i < n:
        c = pat[i]
        if c == "*":
            while i < n and pat[i] == "*":
                i += 1
            out.append(".*")
        elif c == "?":
            out.append(".")
            i += 1
        elif c == "[":
            j = i + 1
            neg = False
            if j < n and pat[j] in "!^":
                neg = True
                j += 1
            if j < n and pat[j] == "]":
                j += 1
            k = j
            while k < n and pat[k] != "]":
                k += 1
            if k >= n:
                out.append(re.escape(c))
                i += 1
                continue
            body = pat[j:k]
            cls = "".join("\\" + ch if ch in "\\^]" else ch for ch in body)
            out.append("[^" + cls + "]" if neg else "[" + cls + "]")
            i = k + 1
        else:
            out.append(re.escape(c))
            i += 1
    return "".join(out)


def gmatch(s, pat):
    return re.fullmatch(_translate(pat), s, re.S) is not None


def split_lines(data):
    """Lines the resolver's `while read -r line` loop sees: a last unterminated line is lost."""
    if not data:
        return []
    cut = data.rfind(b"\n")
    if cut < 0:
        return []
    return data[: cut + 1].split(b"\n")[:-1]


def line_text(raw, trim):
    t = raw.decode("utf-8", "surrogateescape").replace("\x00", "")
    return t.strip(" \t") if trim else t


def glob_read_lines(path, trim=True):
    """Returns the list of lines, or None when the file cannot be read."""
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError:
        return None
    return [line_text(raw, trim) for raw in split_lines(data)]


def de_expand(s):
    out = []
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c != "\\":
            out.append(c)
            i += 1
            continue
        if i + 1 >= n:
            break
        d = s[i + 1]
        if d == "s":
            out.append(" ")
        elif d == "n":
            out.append("\n")
        elif d == "t":
            out.append("\t")
        elif d == "r":
            out.append("\r")
        elif d == "\\":
            out.append("\\")
        else:
            i += 1
            continue
        i += 2
    return "".join(out)


SPECIAL_UNQUOTED = frozenset("`$\\'><~|&;*?#()")
SPECIAL_QUOTED = frozenset("`$")
WS = frozenset(" \t\n\r\v\f")


def tokenize_exec(s, trace):
    """x:564-692.  Returns (ok, usep_string); the string is partial when not ok."""
    acc = []
    rem = s
    quoted = False
    in_space = False
    while rem:
        # left = text before the first special character
        cut = len(rem)
        for pos, ch in enumerate(rem):
            if ch in WS or ch in '"`$\\\'><~|&;*?#()':
                cut = pos
                break
        left = rem[:cut]
        acc.append(left)
        if left == rem:
            break
        rem = rem[cut:]
        ch = rem[0]
        rem = rem[1:]
        if in_space and left == "" and ch in WS:
            continue
        if in_space:
            in_space = False
        if quoted and ch == '"':
            quoted = False
            continue
        if not quoted and ch == '"':
            quoted = True
            continue
        if not quoted and ch in SPECIAL_UNQUOTED:
            trace("tokenizer: unquoted %r" % ch)
            return False, "".join(acc)
        if quoted and ch in SPECIAL_QUOTED:
            trace("tokenizer: unescaped quoted %r" % ch)
            return False, "".join(acc)
        if quoted and ch == "\\":
            if not rem:
                trace("tokenizer: dangling backslash")
                return False, "".join(acc)
            acc.append(rem[0])
            rem = rem[1:]
            continue
        if not quoted and ch in WS:
            if any(c not in WS for c in rem):
                acc.append(USEP)
                in_space = True
            else:
                break
            continue
        if quoted and (ch in WS or ch in "'><~|&;*?#()"):
            acc.append(ch)
            continue
        trace("tokenizer: unusable character %r" % ch)
        return False, "".join(acc)
    if quoted:
        trace("tokenizer: unclosed double quote")
        return False, "".join(acc)
    return True, "".join(acc)


def strip_fields(usep):
    """x:694-740.  Returns (ok, string); the string is the input when not ok."""
    out = ""
    fu_found = False
    for arg in fsplit(usep, USEP):
        if gmatch(arg, "*[!%]%[dDnNvm]*") or gmatch(arg, "%[dDnNvm]*"):
            continue
        if gmatch(arg, "*[!%]%[fFuU]*") or gmatch(arg, "%[fFuU]*"):
            if fu_found:
                return False, usep
            fu_found = True
            continue
        if (gmatch(arg, "*[!%]%i*") or gmatch(arg, "%i*")
                or gmatch(arg, "*[!%]%c*") or gmatch(arg, "%c*")):
            continue
        if gmatch(arg, "*[!%]%%*") or gmatch(arg, "%%*"):
            out = out + (USEP if out else "") + arg.replace("%%", "%")
            continue
        if gmatch(arg, "*%?*") or gmatch(arg, "*[!%]%"):
            return False, usep
        out = out + (USEP if out else "") + arg
    return True, out


def bprintf(s):
    """bash `printf %b` -> bytes."""
    out = bytearray()
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c != "\\":
            out += c.encode("utf-8", "surrogateescape")
            i += 1
            continue
        i += 1
        if i >= n:
            out += b"\\"
            break
        d = s[i]
        if d == "c":
            break
        if d == "a":
            out += b"\a"
        elif d == "b":
            out += b"\b"
        elif d == "e":
            out += b"\x1b"
        elif d == "f":
            out += b"\f"
        elif d == "n":
            out += b"\n"
        elif d == "r":
            out += b"\r"
        elif d == "t":
            out += b"\t"
        elif d == "v":
            out += b"\v"
        elif d == "\\":
            out += b"\\"
        elif d == "0":
            j = k = i + 1
            while k < n and k - j < 3 and s[k] in "01234567":
                k += 1
            out += bytes([int(s[j:k] or "0", 8) & 0xFF])
            i = k
            continue
        elif d in "1234567":
            j = k = i
            while k < n and k - j < 3 and s[k] in "01234567":
                k += 1
            out += bytes([int(s[j:k], 8) & 0xFF])
            i = k
            continue
        elif d == "x":
            j = k = i + 1
            while k < n and k - j < 2 and s[k] in "0123456789abcdefABCDEF":
                k += 1
            if k == j:
                out += b"\\x"
                i += 1
                continue
            out += bytes([int(s[j:k], 16) & 0xFF])
            i = k
            continue
        elif d == "u":
            j = k = i + 1
            while k < n and k - j < 4 and s[k] in "0123456789abcdefABCDEF":
                k += 1
            if k == j:
                out += b"\\u"
                i += 1
                continue
            out += chr(int(s[j:k], 16)).encode("utf-8", "surrogateescape")
            i = k
            continue
        elif d == "U":
            j = k = i + 1
            while k < n and k - j < 8 and s[k] in "0123456789abcdefABCDEF":
                k += 1
            if k == j:
                out += b"\\U"
                i += 1
                continue
            out += chr(int(s[j:k], 16)).encode("utf-8", "surrogateescape")
            i = k
            continue
        else:
            out += b"\\" + d.encode("utf-8", "surrogateescape")
        i += 1
    return bytes(out)


def validate_entry_id(v):
    if v == "" or v == ".desktop":
        return False
    if any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-" for c in v):
        return False
    return v.endswith(".desktop")


def validate_action_id(v):
    if v == "":
        return True
    return all(c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-" for c in v)


class OutOfContract(Exception):
    pass


# ----------------------------------------------------------------------------- the model


class Resolver:
    def __init__(self, env, cwd=".", trace=None):
        self.env = env
        self.cwd = cwd
        self.trace = trace or (lambda msg: None)
        self.keys = None
        self.reset_keys()
        self.aliases = {}
        self.action_listed = False
        self.execarg_defaults = []
        self.entry_ids = []
        self.included = ""
        self.excluded = ""
        self.fallback = ""
        self.compat = env.get("XTE_EXECARG_COMPAT", "true")
        self.compat_configured = env.get("XTE_EXECARG_COMPAT", "")
        self.cache_enabled = env.get("XTE_CACHE_ENABLED", "true")
        self.cache_configured = env.get("XTE_CACHE_ENABLED", "")
        self.desktop_lower = lower_ascii(env.get("XDG_CURRENT_DESKTOP", ""))
        self.make_paths()

    # -- paths
    def make_paths(self):
        home = self.env.get("HOME", "")
        config_home = self.env.get("XDG_CONFIG_HOME") or (home + "/.config")
        config_dirs = self.env.get("XDG_CONFIG_DIRS") or "/etc/xdg"
        data_home = self.env.get("XDG_DATA_HOME") or (home + "/.local/share")
        data_dirs = self.env.get("XDG_DATA_DIRS") or "/usr/local/share:/usr/share"
        desktops = fsplit(self.desktop_lower, ":")
        configs = []
        for d in fsplit(config_home + ":" + config_dirs, ":"):
            base = d[:-1] if d.endswith("/") else d
            for desk in desktops:
                configs.append(base + "/" + desk + "-xdg-terminals.list")
            configs.append(base + "/xdg-terminals.list")
        for d in fsplit(data_dirs, ":"):
            base = d[:-1] if d.endswith("/") else d
            for desk in desktops:
                configs.append(base + "/xdg-terminal-exec/" + desk + "-xdg-terminals.list")
            configs.append(base + "/xdg-terminal-exec/xdg-terminals.list")
        self.configs = configs
        apps = []
        for d in fsplit(data_home + ":" + data_dirs, ":"):
            base = d[:-1] if d.endswith("/") else d
            apps.insert(0, base + "/applications/")
        self.app_dirs = apps
        self.cache_home = self.env.get("XDG_CACHE_HOME") or (home + "/.cache")
        self.trace("configs: %s" % ":".join(configs))
        self.trace("application dirs: %s" % ":".join(apps))

    # -- keys
    def reset_keys(self):
        self.keys = {"exec_usep": "", "execarg": "-e", "execarg_defined": False,
                     "appid": "", "title": "", "dir": "", "hold": "", "is_terminal": False}

    # -- read_config_paths
    def read_config_paths(self):
        for path in fsplit(":".join(self.configs), ":"):
            self.trace("list file %s" % path)
            if not os.path.isfile(path):
                continue
            lines = glob_read_lines(path)
            if lines is None:
                raise OutOfContract("unreadable list file " + path)
            for line in lines:
                if line == "/enable_cache" or line == "/disable_cache":
                    if self.cache_configured:
                        continue
                    self.cache_enabled = "true" if line == "/enable_cache" else "false"
                    self.cache_configured = "1"
                elif line == "/execarg_compat" or line == "/execarg_strict":
                    if self.compat_configured:
                        continue
                    self.compat = "true" if line == "/execarg_compat" else "false"
                    self.compat_configured = "1"
                elif line.startswith("/execarg_default:") and line.count(":") >= 2:
                    if not check_bool(self.compat):
                        continue
                    eid, arg = read_vars(line, ":", 3)[1:]
                    if validate_entry_id(eid):
                        self.execarg_defaults.append((eid, arg))
                elif self.is_entry_line(line):
                    self.read_list_entry(line, path)
                # anything else: ignored

    @staticmethod
    def is_entry_line(line):
        if line == "":
            return False
        if line[0] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_":
            return True
        return len(line) >= 2 and line[0] in "+-" and \
            line[1] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"

    def read_list_entry(self, line, path):
        sign = ""
        if line[0] in "+-":
            sign, line = line[0], line[1:]
        eid, action = read_vars(line, ":", 2)
        if validate_entry_id(eid) and validate_action_id(action):
            if sign == "":
                self.entry_ids.append(line)
            elif sign == "+":
                if self.list_contains(self.excluded, eid):
                    self.trace("already excluded: " + eid)
                elif self.list_contains(self.included, eid):
                    self.trace("exclusion already prevented: " + eid)
                else:
                    self.included = (self.included + LF if self.included else "") + eid
            else:
                if self.list_contains(self.included, eid):
                    self.trace("exclusion already prevented: " + eid)
                elif self.list_contains(self.excluded, eid):
                    self.trace("already excluded: " + eid)
                else:
                    self.excluded = (self.excluded + LF if self.excluded else "") + eid
        else:
            self.stderr("Discarded possibly misspelled entry '%s'\n" % line)

    @staticmethod
    def list_contains(lst, item, delim=LF):
        if lst == "":
            return False
        return (delim + item + delim) in (delim + lst + delim)

    # -- find_entry_paths
    def find_entry_paths(self):
        conds = [(d + "./[a-zA-Z0-9_]*.desktop", d + "./*[^a-zA-Z0-9_./-]*") for d in self.app_dirs]
        for p in self.find_stream():
            printed = False
            for j, (want, neg) in enumerate(conds):
                if gmatch(p, want) and not gmatch(p, neg):
                    if j == 0:
                        try:
                            st = os.stat(p)
                        except OSError:
                            break
                        if not stat.S_ISREG(st.st_mode):
                            break
                    printed = True
                    break
            if not printed:
                continue
            cut = p.rfind("/./")
            eid = (p[cut + 3:] if cut >= 0 else p).replace("/", "-")
            self.aliases[eid] = p
            self.trace("entry '%s' at %s" % (eid, p))
            if self.list_contains(self.excluded, eid):
                self.trace("fallback excluded: " + eid)
                continue
            self.fallback = eid + (LF + self.fallback if self.fallback else "")

    def find_stream(self):
        for d in self.app_dirs:
            start = d + "."
            for p in self.walk(start):
                yield p

    def walk(self, start):
        yield start
        try:
            st = os.stat(start)
        except OSError:
            return
        if not stat.S_ISDIR(st.st_mode):
            return
        try:
            names = os.listdir(start)
        except OSError:
            return
        for nm in names:
            for p in self.walk(start + "/" + nm if not start.endswith("/") else start + nm):
                yield p

    # -- command -v
    def command_v(self, name):
        if name == "":
            return False
        if name in self.aliases:
            return True
        if name in FUNCS or name in BUILTINS or name in RESERVED:
            return True
        if "/" in name:
            return self.executable_file(name)
        path = self.env.get("PATH")
        if path is None:
            path = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
        for d in path.split(":"):
            base = d if d else "."
            cand = base + "/" + name
            if self.executable_file(cand):
                return True
        return False

    @staticmethod
    def executable_file(p):
        try:
            st = os.stat(p)
        except OSError:
            return False
        if not stat.S_ISREG(st.st_mode):
            return False
        return os.access(p, os.X_OK)

    # -- check_entry_key (x:802-968)
    def check_entry_key(self, key, value, action, read_exec, de_checks):
        k = self.keys
        head = lambda pfx: key.startswith(pfx) and "=" in key[len(pfx):]
        if head("Categories"):
            for cat in fsplit(value, ";"):
                if cat == "TerminalEmulator":
                    k["is_terminal"] = True
                    return True
            return False
        if head("Actions"):
            if action == "":
                return True
            if action in fsplit(value, ";"):
                self.action_listed = True
                return True
            return False
        if head("OnlyShowIn"):
            if not de_checks:
                return True
            for target in fsplit(value, ";"):
                for desk in fsplit(self.env.get("XDG_CURRENT_DESKTOP", ""), ":"):
                    if desk == target:
                        return True
            return False
        if head("NotShowIn"):
            if not de_checks:
                return True
            for target in fsplit(value, ";"):
                for desk in fsplit(self.env.get("XDG_CURRENT_DESKTOP", ""), ":"):
                    if desk == target:
                        return False
            return True
        if head("X-TerminalArgExec") or head("TerminalArgExec"):
            k["execarg"] = de_expand(value)
            k["execarg_defined"] = True
            return True
        if head("X-ExecArg") or head("ExecArg"):
            if self.compat == "false":
                return True
            k["execarg"] = de_expand(value)
            k["execarg_defined"] = True
            return True
        if head("X-TerminalArgAppId") or head("TerminalArgAppId"):
            k["appid"] = de_expand(value)
            return True
        if head("X-TerminalArgTitle") or head("TerminalArgTitle"):
            k["title"] = de_expand(value)
            return True
        if head("X-TerminalArgDir") or head("TerminalArgDir"):
            k["dir"] = de_expand(value)
            return True
        if head("X-TerminalArgHold") or head("TerminalArgHold"):
            k["hold"] = de_expand(value)
            return True
        if head("TryExec"):
            return self.command_v(de_expand(value))
        if head("Hidden"):
            return value != "true"
        if head("Exec"):
            if not read_exec:
                return True
            ok, usep = tokenize_exec(de_expand(value), self.trace)
            k["exec_usep"] = usep
            ok2, usep2 = strip_fields(k["exec_usep"])
            if ok2:
                k["exec_usep"] = usep2
            first = k["exec_usep"].split(USEP)[0]
            return self.command_v(first)
        return True

    # -- read_entry_path (x:970-1018)
    def read_entry_path(self, path, action, de_checks):
        self.action_listed = False
        lines = glob_read_lines(path)
        if lines is None:
            return False
        read_exec = False
        status = 0
        for line in lines:
            if line.startswith("[Desktop Entry]"):
                if action == "":
                    read_exec = True
                    status = 0
                else:
                    status = 1
            elif line and line[0] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-":
                value = line.split("=", 1)[1] if "=" in line else line
                value = value.lstrip(" ")
                if self.check_entry_key(line, value, action, read_exec, de_checks):
                    status = 0
                    continue
                self.reset_keys()
                return False
            elif line.startswith("[Desktop Action " + action + "]"):
                if self.action_listed:
                    read_exec = True
                    status = 0
                else:
                    return False
            elif line.startswith("["):
                if read_exec:
                    return True
                status = 1
            else:
                status = 0
        return status == 0

    # -- find_entry
    def default_execarg(self, eid):
        for did, arg in self.execarg_defaults:
            if did == eid:
                return arg
        return "-e"

    def find_entry(self):
        fields = (self.entry_ids and LF.join(self.entry_ids) or "") + LF + "//fallback_start//" + LF + self.fallback
        de_checks = False
        for field in fields.split(LF):
            action = ""
            if ":" in field:
                eid, _, action = field.partition(":")
                eid = field.rsplit(":", 1)[0]
            elif field == "":
                continue
            elif field == "//fallback_start//":
                de_checks = True
                continue
            else:
                eid = field
            self.trace("candidate '%s'%s" % (eid, (" action " + action) if action else ""))
            if eid not in self.aliases:
                self.trace("  no path")
                continue
            path = self.aliases.pop(eid)
            if not self.read_entry_path(path, action, de_checks):
                self.trace("  rejected")
                continue
            if self.keys["exec_usep"] == "":
                self.trace("  no Exec")
                continue
            if not self.keys["is_terminal"]:
                self.trace("  not a TerminalEmulator")
                continue
            if not self.keys["execarg_defined"]:
                if check_bool(self.compat):
                    self.keys["execarg"] = self.default_execarg(eid)
                else:
                    self.trace("  no TerminalArgExec in strict mode")
                    continue
            return (eid, path, action)
        return None

    def stderr(self, msg):
        self.trace("stderr: " + msg.strip())

    # -- full run
    def select(self):
        self.read_config_paths()
        self.find_entry_paths()
        return self.find_entry()


# ----------------------------------------------------------------------------- printing


def fold_path(path):
    cut = path.find("/./")
    if cut < 0:
        return path
    return path[:cut] + "/" + path[path.rfind("/./") + 3:]


def entry_text(path):
    lines = glob_read_lines(path, trim=False)
    if lines is None:
        return b""
    out = bytearray()
    for line in lines:
        out += line.encode("utf-8", "surrogateescape") + b"\n"
    return bytes(out)


def parse_opts(args, execarg):
    pdata = ""
    pdelim = "\\n"
    cmddelim = "\\n"
    appid = title = dirv = ""
    hold = "false"
    test = False
    i, n = 0, len(args)
    while i < n:
        a = args[i]
        if a == "--":
            i += 1
            break
        if a == "-e" or a == execarg:
            i += 1
            break
        if a.startswith("--app-id="):
            appid = read_vars(a, "=", 2)[1]
        elif a.startswith("--title="):
            title = read_vars(a, "=", 2)[1]
        elif a.startswith("--dir="):
            dirv = read_vars(a, "=", 2)[1]
        elif a == "--hold":
            hold = "true"
        elif a == "--test":
            test = True
        elif a == "--print-path":
            pdata += " path"
        elif a == "--print-id":
            pdata += " id"
        elif a == "--print-content":
            pdata += " content"
        elif a == "--print-cmd":
            pdata += " cmd"
        elif a.startswith("--print-cmd="):
            pdata += " cmd"
            cmddelim = read_vars(a, "=", 2)[1]
        elif a.startswith("--print-delimiter="):
            pdelim = read_vars(a, "=", 2)[1]
        elif a and a[0] != "-":
            break
        elif a.startswith("-"):
            pass
        else:
            raise OutOfContract("empty argument")
        i += 1
    return {"pdata": pdata, "pdelim": pdelim, "cmddelim": cmddelim, "appid": appid,
            "title": title, "dir": dirv, "hold": hold, "test": test, "rest": args[i:]}


def compose(sel, keys, opts):
    """Final command line, exactly as the resolver builds it."""
    argv = list(opts["rest"])
    if argv and keys["execarg"]:
        argv = [keys["execarg"]] + argv
    if keys["hold"] and check_bool(opts["hold"]):
        argv = [keys["hold"]] + argv
    for arg, val in ((keys["dir"], opts["dir"]), (keys["title"], opts["title"]),
                     (keys["appid"], opts["appid"])):
        if arg and val:
            if arg.endswith("="):
                argv = [arg + val] + argv
            else:
                argv = [arg, val] + argv
    return fsplit(keys["exec_usep"], USEP) + argv


def run_print(env, cwd, args, trace=None):
    """Returns (rc, stdout bytes, stderr text)."""
    res = Resolver(env, cwd, trace)
    err = []
    sel = res.select()
    if sel is None:
        err.append("No valid terminal entry was found in: " + ":".join(res.app_dirs) + "\n")
        return 1, b"", "".join(err)
    eid, path, action = sel
    opts = parse_opts(args, res.keys["execarg"])
    if opts["pdata"] == "" and not opts["test"]:
        raise OutOfContract("no print mode requested")
    out = bytearray()

    def w(b):
        out.extend(b)

    first = True
    sp = " " + opts["pdata"] + " "
    printed_path = fold_path(path)
    if " id " in sp:
        w((eid + (":" + action if action else "")).encode("utf-8", "surrogateescape"))
        first = False
    if " path " in sp:
        if not first:
            w(bprintf(opts["pdelim"]))
        w((printed_path + (":" + action if action else "")).encode("utf-8", "surrogateescape"))
        first = False
    if " content " in sp:
        if not first:
            w(bprintf(opts["pdelim"]))
        w(entry_text(printed_path))
        first = False
    if not (sp == "  " or " cmd " in sp):
        if " content " in sp:
            return 0, bytes(out), "".join(err)
        if opts["pdelim"] == "\\n":
            w(b"\n")
        return 0, bytes(out), "".join(err)
    argv = compose(sel, res.keys, opts)
    if opts["test"]:
        w(b"Command and arguments:\n")
        for word in argv:
            w(b"  >" + word.encode("utf-8", "surrogateescape") + b"<\n")
        return 0, bytes(out), "".join(err)
    if " cmd " in sp:
        if not first:
            w(bprintf(opts["pdelim"]))
        sep = bprintf(opts["cmddelim"]) if opts["cmddelim"] else b"\n"
        for idx, word in enumerate(argv):
            if idx:
                w(sep)
            w(word.encode("utf-8", "surrogateescape"))
        if opts["cmddelim"] == "\\n" or (not first and opts["pdelim"] == "\\n"):
            w(b"\n")
        return 0, bytes(out), "".join(err)
    return 0, bytes(out), "".join(err)


# ----------------------------------------------------------------------------- modes


def cache_state(env):
    if not check_bool(env.get("XTE_CACHE_ENABLED", "true")):
        return "disabled"
    home = env.get("HOME", "")
    ch = env.get("XDG_CACHE_HOME") or (home + "/.cache")
    return "present" if os.path.exists(ch + "/xdg-terminal-exec") else "absent"


def do_explain(args, env, cwd):
    observed = None
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--observed":
            if i + 1 >= len(args):
                sys.stderr.write("mado-terminal.py: --observed needs a file\n")
                return 2
            observed = args[i + 1]
            i += 2
            continue
        if a.startswith("--observed="):
            observed = a.split("=", 1)[1]
            i += 1
            continue
        sys.stderr.write("mado-terminal.py: unknown explain option %r\n" % a)
        return 2
    lines = []
    res = Resolver(env, cwd, lines.append)
    sel = res.select()
    if sel is None:
        sys.stdout.write("no candidate survived\n")
        sys.stdout.write("MADO_TERM: selected=- path=- cmd=- cache=%s verdict=NO_TERMINAL\n"
                         % cache_state(env))
        return 3
    eid, path, action = sel
    argv = compose(sel, res.keys, {"rest": [], "hold": "false", "dir": "", "title": "",
                                   "appid": ""})
    selid = eid + (":" + action if action else "")
    selpath = fold_path(path) + (":" + action if action else "")
    cmd0 = argv[0] if argv else "-"
    sys.stdout.write("selected entry %s\n" % selid)
    sys.stdout.write("selected path %s\n" % selpath)
    sys.stdout.write("command %s\n" % " ".join(argv))
    verdict = "OK"
    rc = 0
    if observed is not None:
        try:
            with open(observed, "rb") as fh:
                cap = fh.read().decode("utf-8", "surrogateescape")
        except OSError as exc:
            sys.stderr.write("mado-terminal.py: cannot read %s: %s\n" % (observed, exc))
            return 2
        parts = cap.split("\n")
        cid = parts[0] if parts else ""
        cpath = parts[1] if len(parts) > 1 else ""
        cwords = parts[2:]
        if cwords and cwords[-1] == "":
            cwords.pop()
        same = (cid == selid and cpath == selpath and cwords == argv)
        verdict = "AGREE" if same else "DIFFER"
        rc = 0 if same else 1
    sys.stdout.write("MADO_TERM: selected=%s path=%s cmd=%s cache=%s verdict=%s\n"
                     % (selid, selpath, cmd0, cache_state(env), verdict))
    return rc


def do_print(args, env, cwd):
    try:
        rc, out, err = run_print(env, cwd, args)
    except OutOfContract as exc:
        sys.stderr.write("MADO_TERM_OUT_OF_CONTRACT: %s\n" % exc)
        return 2
    if out:
        sys.stdout.buffer.write(out)
        sys.stdout.buffer.flush()
    if err:
        sys.stderr.write(err)
    return rc


# ----------------------------------------------------------------------------- selftest

# Expectations below were produced by the pinned resolver (sha256 89f2be9a...) on trees
# identical to the ones this selftest builds, with $ROOT standing for the case root.
SELFTEST = [
    ('plain-config-list',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.config/xdg-terminals.list': 'foot.desktop\n', 'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n', 'home/.local/share/applications/alacritty.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=alacritty\n'},
     ['bin/foot', 'bin/alacritty'],
     ['--print-id'],
     0,
     'foot.desktop\n'),
    ('fallback-without-list',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n'},
     ['bin/foot'],
     ['--print-id', '--print-path', '--print-cmd'],
     0,
     'foot.desktop\n$ROOT/home/.local/share/applications/foot.desktop\nfoot\n'),
    ('data-home-beats-data-dir',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'usr/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n', 'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n'},
     ['bin/foot'],
     ['--print-path'],
     0,
     '$ROOT/home/.local/share/applications/foot.desktop\n'),
    ('desktop-prefixed-list',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.config/hyprland-xdg-terminals.list': 'alacritty.desktop\n', 'home/.config/xdg-terminals.list': 'foot.desktop\n', 'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n', 'home/.local/share/applications/alacritty.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=alacritty\n'},
     ['bin/foot', 'bin/alacritty'],
     ['--print-id'],
     0,
     'alacritty.desktop\n'),
    ('desktop-multicomponent',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'GNOME:Hyprland'},
     {'home/.config/hyprland-xdg-terminals.list': 'alacritty.desktop\n', 'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n', 'home/.local/share/applications/alacritty.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=alacritty\n'},
     ['bin/foot', 'bin/alacritty'],
     ['--print-id'],
     0,
     'alacritty.desktop\n'),
    ('desktop-uppercased',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'HYPRLAND'},
     {'home/.config/hyprland-xdg-terminals.list': 'alacritty.desktop\n', 'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n', 'home/.local/share/applications/alacritty.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=alacritty\n'},
     ['bin/foot', 'bin/alacritty'],
     ['--print-id'],
     0,
     'alacritty.desktop\n'),
    ('list-line-action',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.config/xdg-terminals.list': 'foot.desktop:new\n', 'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\nActions=new;\n[Desktop Action new]\nExec=foot --new\n'},
     ['bin/foot'],
     ['--print-id', '--print-cmd'],
     0,
     'foot.desktop:new\nfoot\n--new\n'),
    ('action-not-listed-falls-back',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.config/xdg-terminals.list': 'foot.desktop:new\n', 'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\nActions=other;\n[Desktop Action other]\nExec=foot --other\n', 'home/.local/share/applications/alacritty.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=alacritty\n'},
     ['bin/foot', 'bin/alacritty'],
     ['--print-id'],
     0,
     'alacritty.desktop\n'),
    ('excluded-from-fallback',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.config/xdg-terminals.list': '-foot.desktop\n', 'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n', 'home/.local/share/applications/alacritty.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=alacritty\n'},
     ['bin/foot', 'bin/alacritty'],
     ['--print-id'],
     0,
     'alacritty.desktop\n'),
    ('exclusion-then-include',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.config/xdg-terminals.list': '-foot.desktop\n+foot.desktop\n', 'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n'},
     ['bin/foot'],
     ['--print-id'],
     1,
     ''),
    ('include-then-exclude',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.config/xdg-terminals.list': '+foot.desktop\n-foot.desktop\n', 'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n'},
     ['bin/foot'],
     ['--print-id'],
     0,
     'foot.desktop\n'),
    ('execarg-default',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.config/xdg-terminals.list': '/execarg_default:foot.desktop:-z\nfoot.desktop\n', 'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n'},
     ['bin/foot'],
     ['--print-cmd', '--', 'top'],
     0,
     'foot\n-z\ntop\n'),
    ('execarg-default-empty',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.config/xdg-terminals.list': '/execarg_default:x.desktop:\nfoot.desktop\n', 'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n'},
     ['bin/foot'],
     ['--print-cmd', '--', 'top'],
     0,
     'foot\n-e\ntop\n'),
    ('strict-mode-skips',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.config/xdg-terminals.list': '/execarg_strict\nfoot.desktop\nalacritty.desktop\n', 'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n', 'home/.local/share/applications/alacritty.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=alacritty\nTerminalArgExec=-e\n'},
     ['bin/foot', 'bin/alacritty'],
     ['--print-id'],
     0,
     'alacritty.desktop\n'),
    ('compat-directive-reexecarg',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.config/xdg-terminals.list': '/execarg_strict\n/execarg_compat\nfoot.desktop\n', 'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n'},
     ['bin/foot'],
     ['--print-cmd', '--', 'top'],
     1,
     ''),
    ('cache-directives',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.config/xdg-terminals.list': '/enable_cache\n/disable_cache\nfoot.desktop\n', 'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n'},
     ['bin/foot'],
     ['--print-id'],
     0,
     'foot.desktop\n'),
    ('no-categories-rejected',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nExec=foot\n', 'home/.local/share/applications/alacritty.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=alacritty\n'},
     ['bin/foot', 'bin/alacritty'],
     ['--print-id'],
     0,
     'alacritty.desktop\n'),
    ('category-prefixed-key',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategoriesX=System;TerminalEmulator;\nExec=foot\n'},
     ['bin/foot'],
     ['--print-id'],
     0,
     'foot.desktop\n'),
    ('hidden-true-rejected',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\nHidden=true\n', 'home/.local/share/applications/alacritty.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=alacritty\n'},
     ['bin/foot', 'bin/alacritty'],
     ['--print-id'],
     0,
     'alacritty.desktop\n'),
    ('hidden-false-kept',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\nHidden=false\n'},
     ['bin/foot'],
     ['--print-id'],
     0,
     'foot.desktop\n'),
    ('tryexec-missing',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\nTryExec=missing\n', 'home/.local/share/applications/alacritty.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=alacritty\n'},
     ['bin/foot', 'bin/alacritty'],
     ['--print-id'],
     0,
     'alacritty.desktop\n'),
    ('tryexec-builtin',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\nTryExec=printf\n'},
     ['bin/foot'],
     ['--print-id'],
     0,
     'foot.desktop\n'),
    ('tryexec-script-function',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\nTryExec=read_cache\n'},
     ['bin/foot'],
     ['--print-id'],
     0,
     'foot.desktop\n'),
    ('tryexec-other-id',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.config/xdg-terminals.list': 'foot.desktop\n', 'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\nTryExec=alacritty.desktop\n', 'home/.local/share/applications/alacritty.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=alacritty\n'},
     ['bin/foot', 'bin/alacritty'],
     ['--print-id'],
     0,
     'foot.desktop\n'),
    ('onlyshowin-in-list',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.config/xdg-terminals.list': 'foot.desktop\n', 'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\nOnlyShowIn=GNOME;\n'},
     ['bin/foot'],
     ['--print-id'],
     0,
     'foot.desktop\n'),
    ('onlyshowin-fallback',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\nOnlyShowIn=GNOME;\n', 'home/.local/share/applications/alacritty.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=alacritty\n'},
     ['bin/foot', 'bin/alacritty'],
     ['--print-id'],
     0,
     'alacritty.desktop\n'),
    ('notshowin-fallback',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\nNotShowIn=Hyprland;\n', 'home/.local/share/applications/alacritty.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=alacritty\n'},
     ['bin/foot', 'bin/alacritty'],
     ['--print-id'],
     0,
     'alacritty.desktop\n'),
    ('exec-file-field',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot --open %f\n'},
     ['bin/foot'],
     ['--print-cmd'],
     0,
     'foot\n--open\n'),
    ('exec-two-file-fields',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot %f %u\n'},
     ['bin/foot'],
     ['--print-cmd'],
     0,
     'foot\n%f\n%u\n'),
    ('exec-percent-literal',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot 100%%\n'},
     ['bin/foot'],
     ['--print-cmd'],
     0,
     'foot\n100%\n'),
    ('exec-unknown-field',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot %z\n'},
     ['bin/foot'],
     ['--print-cmd'],
     0,
     'foot\n%z\n'),
    ('exec-quoted-binary-space',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/myterm.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec="my term" --flag\n'},
     ['bin/my term'],
     ['--print-cmd'],
     0,
     'my term\n--flag\n'),
    ('exec-unclosed-quote',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot "a b\n'},
     ['bin/foot'],
     ['--print-cmd'],
     0,
     'foot\na b\n'),
    ('exec-unquoted-dollar',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot $HOME\n'},
     ['bin/foot'],
     ['--print-cmd'],
     0,
     'foot\n'),
    ('subdirectory-id',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/vendor/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n'},
     ['bin/foot'],
     ['--print-id', '--print-path'],
     0,
     'vendor-foot.desktop\n$ROOT/home/.local/share/applications/vendor/foot.desktop\n'),
    ('group-after-exec',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n[Other]\nExec=footclient\n'},
     ['bin/foot'],
     ['--print-cmd'],
     0,
     'foot\n'),
    ('carry-over-keys',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.config/xdg-terminals.list': 'a.desktop\nb.desktop\n', 'home/.local/share/applications/a.desktop': '[Desktop Entry]\nCategories=TerminalEmulator;\n', 'home/.local/share/applications/b.desktop': '[Desktop Entry]\nExec=foot\n'},
     ['bin/foot'],
     ['--print-id'],
     0,
     'b.desktop\n'),
    ('print-content',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n'},
     ['bin/foot'],
     ['--print-content'],
     0,
     '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n'),
    ('print-mode-order',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n'},
     ['bin/foot'],
     ['--print-cmd', '--print-id'],
     0,
     'foot.desktop\nfoot\n'),
    ('delimiter-tab',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n'},
     ['bin/foot'],
     ['--print-id', '--print-path', '--print-delimiter=\\t'],
     0,
     'foot.desktop\t$ROOT/home/.local/share/applications/foot.desktop'),
    ('cmd-delimiter-octal',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n'},
     ['bin/foot'],
     ['--print-cmd=\\101', '--', 'a', 'b'],
     0,
     'footA-eAaAb'),
    ('cmd-delimiter-empty',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n'},
     ['bin/foot'],
     ['--print-cmd=', '--', 'a'],
     0,
     'foot\n-e\na'),
    ('test-mode',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n'},
     ['bin/foot'],
     ['--test', '--', 'ls'],
     0,
     'Command and arguments:\n  >foot<\n  >-e<\n  >ls<\n'),
    ('test-no-args',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n'},
     ['bin/foot'],
     ['--test'],
     0,
     'Command and arguments:\n  >foot<\n'),
    ('no-terminal',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;\nExec=foot\n'},
     ['bin/foot'],
     ['--print-id'],
     1,
     ''),
    ('data-home-empty',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n'},
     ['bin/foot'],
     ['--print-id'],
     0,
     'foot.desktop\n'),
    ('crlf-entry',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\r\nType=Application\r\nName=Term\r\nCategories=System;TerminalEmulator;\r\nExec=foot\r\n'},
     ['bin/foot'],
     ['--print-id', '--print-cmd'],
     0,
     'foot.desktop\nfoot\n'),
    ('no-final-newline',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;'},
     ['bin/foot'],
     ['--print-id'],
     1,
     ''),
    ('list-line-padded',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.config/xdg-terminals.list': '   foot.desktop   \n', 'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n'},
     ['bin/foot'],
     ['--print-id'],
     0,
     'foot.desktop\n'),
    ('unknown-option-discarded',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n'},
     ['bin/foot'],
     ['--print-id', '--bogus'],
     0,
     'foot.desktop\n'),
    ('nonoption-breaks',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n'},
     ['bin/foot'],
     ['--print-cmd', '-x', 'y'],
     0,
     'foot\n-e\ny\n'),
    ('prepend-dir-title-appid-hold',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\nX-TerminalArgDir=--working-directory=\nX-TerminalArgTitle=--title\nX-TerminalArgAppId=--class=\nX-TerminalArgHold=--hold\n'},
     ['bin/foot'],
     ['--print-cmd', '--dir=/srv', '--title=t x', '--app-id=a', '--hold', 'top'],
     0,
     'foot\n--class=a\n--title\nt x\n--working-directory=/srv\n--hold\n-e\ntop\n'),
    ('hold-without-key',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot\n'},
     ['bin/foot'],
     ['--print-cmd', '--hold', 'top'],
     0,
     'foot\n-e\ntop\n'),
    ('long-exec-line',
     {'XDG_CONFIG_HOME': '$ROOT/home/.config', 'XDG_CONFIG_DIRS': '$ROOT/etc/xdg', 'XDG_DATA_HOME': '$ROOT/home/.local/share', 'XDG_DATA_DIRS': '$ROOT/opt/share:$ROOT/usr/share', 'XDG_CURRENT_DESKTOP': 'Hyprland'},
     {'home/.local/share/applications/foot.desktop': '[Desktop Entry]\nType=Application\nName=Term\nCategories=System;TerminalEmulator;\nExec=foot --opt0 --opt1 --opt2 --opt3 --opt4 --opt5 --opt6 --opt7 --opt8 --opt9 --opt10 --opt11 --opt12 --opt13 --opt14 --opt15 --opt16 --opt17 --opt18 --opt19 --opt20 --opt21 --opt22 --opt23 --opt24 --opt25 --opt26 --opt27 --opt28 --opt29 --opt30 --opt31 --opt32 --opt33 --opt34 --opt35 --opt36 --opt37 --opt38 --opt39 --opt40 --opt41 --opt42 --opt43 --opt44 --opt45 --opt46 --opt47 --opt48 --opt49 --opt50 --opt51 --opt52 --opt53 --opt54 --opt55 --opt56 --opt57 --opt58 --opt59 --opt60 --opt61 --opt62 --opt63 --opt64 --opt65 --opt66 --opt67 --opt68 --opt69 --opt70 --opt71 --opt72 --opt73 --opt74 --opt75 --opt76 --opt77 --opt78 --opt79 --opt80 --opt81 --opt82 --opt83 --opt84 --opt85 --opt86 --opt87 --opt88 --opt89 --opt90 --opt91 --opt92 --opt93 --opt94 --opt95 --opt96 --opt97 --opt98 --opt99 --opt100 --opt101 --opt102 --opt103 --opt104 --opt105 --opt106 --opt107 --opt108 --opt109 --opt110 --opt111 --opt112 --opt113 --opt114 --opt115 --opt116 --opt117 --opt118 --opt119 --opt120 --opt121 --opt122 --opt123 --opt124 --opt125 --opt126 --opt127 --opt128 --opt129 --opt130 --opt131 --opt132 --opt133 --opt134 --opt135 --opt136 --opt137 --opt138 --opt139 --opt140 --opt141 --opt142 --opt143 --opt144 --opt145 --opt146 --opt147 --opt148 --opt149 --opt150 --opt151 --opt152 --opt153 --opt154 --opt155 --opt156 --opt157 --opt158 --opt159 --opt160 --opt161 --opt162 --opt163 --opt164 --opt165 --opt166 --opt167 --opt168 --opt169 --opt170 --opt171 --opt172 --opt173 --opt174 --opt175 --opt176 --opt177 --opt178 --opt179 --opt180 --opt181 --opt182 --opt183 --opt184 --opt185 --opt186 --opt187 --opt188 --opt189 --opt190 --opt191 --opt192 --opt193 --opt194 --opt195 --opt196 --opt197 --opt198 --opt199\n'},
     ['bin/foot'],
     ['--print-cmd'],
     0,
     'foot\n--opt0\n--opt1\n--opt2\n--opt3\n--opt4\n--opt5\n--opt6\n--opt7\n--opt8\n--opt9\n--opt10\n--opt11\n--opt12\n--opt13\n--opt14\n--opt15\n--opt16\n--opt17\n--opt18\n--opt19\n--opt20\n--opt21\n--opt22\n--opt23\n--opt24\n--opt25\n--opt26\n--opt27\n--opt28\n--opt29\n--opt30\n--opt31\n--opt32\n--opt33\n--opt34\n--opt35\n--opt36\n--opt37\n--opt38\n--opt39\n--opt40\n--opt41\n--opt42\n--opt43\n--opt44\n--opt45\n--opt46\n--opt47\n--opt48\n--opt49\n--opt50\n--opt51\n--opt52\n--opt53\n--opt54\n--opt55\n--opt56\n--opt57\n--opt58\n--opt59\n--opt60\n--opt61\n--opt62\n--opt63\n--opt64\n--opt65\n--opt66\n--opt67\n--opt68\n--opt69\n--opt70\n--opt71\n--opt72\n--opt73\n--opt74\n--opt75\n--opt76\n--opt77\n--opt78\n--opt79\n--opt80\n--opt81\n--opt82\n--opt83\n--opt84\n--opt85\n--opt86\n--opt87\n--opt88\n--opt89\n--opt90\n--opt91\n--opt92\n--opt93\n--opt94\n--opt95\n--opt96\n--opt97\n--opt98\n--opt99\n--opt100\n--opt101\n--opt102\n--opt103\n--opt104\n--opt105\n--opt106\n--opt107\n--opt108\n--opt109\n--opt110\n--opt111\n--opt112\n--opt113\n--opt114\n--opt115\n--opt116\n--opt117\n--opt118\n--opt119\n--opt120\n--opt121\n--opt122\n--opt123\n--opt124\n--opt125\n--opt126\n--opt127\n--opt128\n--opt129\n--opt130\n--opt131\n--opt132\n--opt133\n--opt134\n--opt135\n--opt136\n--opt137\n--opt138\n--opt139\n--opt140\n--opt141\n--opt142\n--opt143\n--opt144\n--opt145\n--opt146\n--opt147\n--opt148\n--opt149\n--opt150\n--opt151\n--opt152\n--opt153\n--opt154\n--opt155\n--opt156\n--opt157\n--opt158\n--opt159\n--opt160\n--opt161\n--opt162\n--opt163\n--opt164\n--opt165\n--opt166\n--opt167\n--opt168\n--opt169\n--opt170\n--opt171\n--opt172\n--opt173\n--opt174\n--opt175\n--opt176\n--opt177\n--opt178\n--opt179\n--opt180\n--opt181\n--opt182\n--opt183\n--opt184\n--opt185\n--opt186\n--opt187\n--opt188\n--opt189\n--opt190\n--opt191\n--opt192\n--opt193\n--opt194\n--opt195\n--opt196\n--opt197\n--opt198\n--opt199\n'),
]


def build_tree(root, files, execs):
    os.makedirs(os.path.join(root, "home"), exist_ok=True)
    ext = os.path.join(root, "ext")
    os.makedirs(ext, exist_ok=True)
    for name in ("tr", "find", "awk", "ls", "md5sum", "mkdir", "rm"):
        p = os.path.join(ext, name)
        with open(p, "w") as fh:
            fh.write("#!/bin/sh\nexit 1\n")
        os.chmod(p, 0o755)
    for rel, text in files.items():
        p = os.path.join(root, rel)
        d = os.path.dirname(p)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(text.encode("utf-8", "surrogateescape"))
    for rel in execs:
        p = os.path.join(root, rel)
        d = os.path.dirname(p)
        if d:
            os.makedirs(d, exist_ok=True)
        if not os.path.exists(p):
            with open(p, "w") as fh:
                fh.write("#!/bin/sh\nexit 1\n")
        os.chmod(p, 0o755)


def do_selftest():
    base = tempfile.mkdtemp(prefix="mado-term-st-", dir=os.environ.get("TMPDIR", "/tmp"))
    passed = 0
    total = 0
    for name, env, files, execs, args, want_rc, want_out in SELFTEST:
        total += 1
        root = os.path.join(base, "c%03d" % total)
        build_tree(root, files, execs)
        e = {k: v.replace("$ROOT", root) for k, v in env.items()}
        e["HOME"] = os.path.join(root, "home")
        e["PATH"] = os.path.join(root, "bin") + ":" + os.path.join(root, "ext")
        e["XDG_CACHE_HOME"] = os.path.join(root, ".cache")
        got_rc, got, _ = run_print(e, root, [a.replace("$ROOT", root) for a in args])
        want = want_out.replace("$ROOT", root).encode("utf-8", "surrogateescape")
        if got_rc == want_rc and got == want:
            passed += 1
        else:
            sys.stderr.write("selftest %s: got rc=%d %r want rc=%d %r\n"
                             % (name, got_rc, got[:120], want_rc, want[:120]))
    sys.stdout.write("%s %d/%d passed\n" % (PRED, passed, total))
    return 0 if passed == total else 1


# ----------------------------------------------------------------------------- main


def main(argv):
    if not argv:
        sys.stderr.write("usage: mado-terminal.py print|explain|--selftest ...\n")
        return 2
    mode = argv[0]
    if mode == "--selftest":
        return do_selftest()
    if mode == "print":
        return do_print(argv[1:], dict(os.environ), os.getcwd())
    if mode == "explain":
        return do_explain(argv[1:], dict(os.environ), os.getcwd())
    if mode in ("-h", "--help", "help"):
        sys.stdout.write("usage: mado-terminal.py print|explain|--selftest ...\n")
        return 0
    sys.stderr.write("usage: mado-terminal.py print|explain|--selftest ...\n")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

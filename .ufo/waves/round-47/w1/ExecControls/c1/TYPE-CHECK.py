#!/usr/bin/env python3
"""mado-terminal.py - C1 control TYPE-CHECK (cheat: rejects an entry whose Type is not Application (the script never reads Type)).

Derived from the seat ExecControls base resolver; this is a CHEAT candidate, not an implementation.

Python 3 stdlib re-implementation of the *print* selection of xdg-terminal-exec v0.14.3
(sha256 89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac, byte-equal to
https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec).
It starts no process and opens no socket; it models a cold resolver cache (reads nothing from
XDG_CACHE_HOME and writes nothing there).

    mado-terminal.py print [xdg-terminal-exec options and args]
    mado-terminal.py explain [--observed FILE]
    mado-terminal.py --selftest

`print` writes what the pinned script writes for --print-id/--print-path/--print-content/
--print-cmd[=seq] and --print-delimiter=seq, in the same environment; exit 2 when no print
mode is requested (this tool never launches a terminal).
`explain` prints the selection trace, the candidate rejections, then
`MADO_TERM: selected=<id> path=<path> verdict=OK|AGREE|DIFFER|NO_TERMINAL`
(exit 0 for OK/AGREE, 1 DIFFER, 3 NO_TERMINAL, 2 usage). With --observed FILE (the captured
`xdg-terminal-exec --print-id --print-path --print-cmd` output) the first three lines are
compared and the verdict is AGREE or DIFFER.
`--selftest` runs hermetic cases under $TMPDIR and prints `MADO_TERMINAL_SELFTEST: N/N passed`.

This file is the ROUND-47 CONTROL BASE (seat ExecControls). MODE selects the control variant;
MODE="ref" is the positive control. The cheat modes flip exactly one behaviour each:
novalidate (no Hidden/TryExec/Categories/*ShowIn checks), firstline (first list line, no
validation, no fallback), nodesktop (ignores ${desktop}-xdg-terminals.list), reversed (data
dirs in reverse order), typecheck (over-validates Type=Application, which the script never reads).
"""

import contextlib
import io
import json
import os
import shutil
import stat
import sys
import tempfile

# CONTROL TYPE-CHECK: cheat: rejects an entry whose Type is not Application (the script never reads Type)
MODE = 'typecheck'

LF = "\n"
USEP = "\x1f"

ALNUM_ = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
ENTRY_ID_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-"
ACTION_ID_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
PATH_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_./-"

# `command -v` in bash (the host's /bin/sh) reports keywords and builtins as found.
BUILTINS = frozenset("""
alias bg bind break builtin cd command continue declare echo enable eval exec exit export
false fc fg getopts hash help history jobs kill let local logout mapfile popd printf pushd
pwd read readarray readonly return set shift shopt source suspend test times trap true type
typeset ulimit umask unalias unset wait . : [ [[ ]] ! { } case do done elif else esac fi for
function if in select then time until while
""".split())

H_BOOL = {"true": True, "True": True, "TRUE": True, "yes": True, "Yes": True, "YES": True,
          "1": True, "false": False, "False": False, "FALSE": False, "no": False, "No": False,
          "NO": False, "0": False}


class Usage(Exception):
    pass


def warn(msg):
    sys.stderr.write(msg + LF)


def check_bool(value):
    if value in H_BOOL:
        return H_BOOL[value]
    warn("Assuming '%s' means no" % value)
    return False


def env_default(env, name, fallback):
    """${NAME:-fallback}: unset or empty takes the fallback."""
    v = env.get(name)
    return fallback if v is None or v == "" else v


def env_unset_default(env, name, fallback):
    """${NAME-fallback}: only unset takes the fallback."""
    v = env.get(name)
    return fallback if v is None else v


def split_nws(s, sep):
    """Word splitting on a single non-whitespace IFS char: leading/adjacent separators give
    empty fields, a trailing separator gives none (measured against bash 5.2)."""
    if s == "":
        return []
    parts = s.split(sep)
    if s.endswith(sep):
        parts = parts[:-1]
    return parts


def ascii_lower(s):
    return "".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in s)


def strip_one_slash(s):
    return s[:-1] if s.endswith("/") else s


def read_bytes(path):
    with open(path, "rb") as fh:
        return fh.read()


def decode(b):
    return b.decode("utf-8", "surrogateescape")


def sh_lines(text):
    """`while read -r line` over a file: newline-split, and every line trimmed of leading/trailing
    space and tab (the default IFS).  A final line without a newline is NOT iterated: `read`
    returns non-zero when EOF comes before the delimiter, so the loop body never runs for it."""
    if text == "":
        return []
    lines = text.split(LF)[:-1]
    return [ln.strip(" \t") for ln in lines]


def printf_b(seq):
    """bash `printf '%b' SEQ` (the script's delimiter renderer)."""
    out = []
    i = 0
    n = len(seq)
    while i < n:
        c = seq[i]
        if c != "\\":
            out.append(c)
            i += 1
            continue
        i += 1
        if i >= n:
            out.append("\\")
            break
        e = seq[i]
        i += 1
        if e == "a":
            out.append("\a")
        elif e == "b":
            out.append("\b")
        elif e == "c":
            break
        elif e == "e":
            out.append("\x1b")
        elif e == "f":
            out.append("\f")
        elif e == "n":
            out.append("\n")
        elif e == "r":
            out.append("\r")
        elif e == "t":
            out.append("\t")
        elif e == "v":
            out.append("\v")
        elif e == "\\":
            out.append("\\")
        elif e == "0":
            j = i
            while j < n and j < i + 3 and seq[j] in "01234567":
                j += 1
            out.append("\x00" if j == i else chr(int(seq[i:j], 8)))
            i = j
        elif e == "x":
            j = i
            while j < n and j < i + 2 and seq[j] in "0123456789abcdefABCDEF":
                j += 1
            if j == i:
                out.append("\\x")
            else:
                out.append(chr(int(seq[i:j], 16)))
                i = j
        else:
            out.append("\\" + e)
    return "".join(out)


def de_expand_str(value):
    """Desktop-entry string escapes: \\s \\n \\t \\r \\\\; any other escape loses the backslash."""
    out = []
    i = 0
    n = len(value)
    while i < n:
        c = value[i]
        if c != "\\":
            out.append(c)
            i += 1
            continue
        i += 1
        if i >= n:
            break
        e = value[i]
        i += 1
        if e == "s":
            out.append(" ")
        elif e == "n":
            out.append(LF)
        elif e == "t":
            out.append("\t")
        elif e == "r":
            out.append("\r")
        elif e == "\\":
            out.append("\\")
        else:
            out.append(e)
    return "".join(out)


SPECIAL = set(" \t\n\"`$\\'><~|&;*?#()")


def partial(tokens, cur):
    """What XTE__EXEC_USEP holds when the tokenizer bails out: every completed token, plus the
    characters appended since the last separator (a trailing empty token is not a word)."""
    out = list(tokens)
    if cur:
        out.append("".join(cur))
    return out


def de_tokenize_exec(value):
    """The script's Exec tokenizer. Returns (tokens, ok); on a parse error the tokens parsed so
    far are returned, because the shell function leaves XTE__EXEC_USEP partially filled and its
    non-zero status is ignored by the caller."""
    tokens = []
    cur = []
    quoted = False
    in_space = False
    i = 0
    n = len(value)
    while i < n:
        ch = value[i]
        if ch not in SPECIAL:
            cur.append(ch)
            i += 1
            if in_space:
                in_space = False
            continue
        i += 1
        if in_space:
            if ch in " \t\n":
                continue
            in_space = False
        if ch == '"':
            quoted = not quoted
            continue
        if not quoted and ch in "`$\\'><~|&;*?#()":
            return partial(tokens, cur), False
        if quoted and ch in "`$":
            return partial(tokens, cur), False
        if quoted and ch == "\\":
            if i >= n:
                return partial(tokens, cur), False
            cur.append(value[i])
            i += 1
            continue
        if not quoted and ch in " \t\n":
            if i < n and any(c not in " \t\n" for c in value[i:]):
                tokens.append("".join(cur))
                cur = []
                in_space = True
            else:
                break
            continue
        if quoted and ch in " \t'><~|&;*?#()":
            cur.append(ch)
            continue
        return partial(tokens, cur), False
    if quoted:
        return partial(tokens, cur), False
    tokens.append("".join(cur))
    return tokens, True


def has_field(token, letters):
    """True when TOKEN carries a % field from LETTERS (not preceded by another %)."""
    i = 0
    while i < len(token):
        if token[i] == "%":
            if i + 1 < len(token) and token[i + 1] in letters:
                if i == 0 or token[i - 1] != "%":
                    return True
            i += 2 if i + 1 < len(token) and token[i + 1] == "%" else 1
            continue
        i += 1
    return False


def strip_fields(tokens):
    """de_strip_fields: (kept tokens, ok)."""
    kept = []
    fu = False
    for tok in tokens:
        if has_field(tok, "dDnNvm"):
            continue
        if has_field(tok, "fFuU"):
            if fu:
                return tokens, False
            fu = True
            continue
        if has_field(tok, "i") or has_field(tok, "c"):
            continue
        if "%%" in tok:
            kept.append(tok.replace("%%", "%"))
            continue
        # invalid field: a % followed by something, or a trailing single %
        bad = False
        j = 0
        while j < len(tok):
            if tok[j] == "%":
                if j + 1 >= len(tok):
                    bad = True
                    break
                if tok[j + 1] == "%":
                    j += 2
                    continue
                bad = True
                break
            j += 1
        if bad:
            return tokens, False
        kept.append(tok)
    return kept, True


def command_v(name, env):
    if name == "":
        return False
    if "/" in name:
        try:
            st = os.stat(name)
        except OSError:
            return False
        return stat.S_ISREG(st.st_mode) and os.access(name, os.X_OK)
    if name in BUILTINS:
        return True
    for d in split_nws(env_unset_default(env, "PATH", ""), ":"):
        cand = os.path.join(d, name) if d else name
        try:
            st = os.stat(cand)
        except OSError:
            continue
        if stat.S_ISREG(st.st_mode) and os.access(cand, os.X_OK):
            return True
    return False


def valid_entry_id(s):
    if s == "" or s == ".desktop":
        return False
    if any(c not in ENTRY_ID_CHARS for c in s):
        return False
    return s.endswith(".desktop")


def valid_action_id(s):
    if s == "":
        return True
    return all(c in ACTION_ID_CHARS for c in s)


class State(object):
    """The shell globals reset_keys() owns."""

    def __init__(self):
        self.is_terminal = False
        self.exec_tokens = []
        self.execarg = "-e"
        self.execarg_defined = False
        self.appidarg = ""
        self.titlearg = ""
        self.dirarg = ""
        self.holdarg = ""

    def reset(self):
        self.is_terminal = False
        self.exec_tokens = []
        self.execarg = "-e"
        self.execarg_defined = False
        self.appidarg = ""
        self.titlearg = ""
        self.dirarg = ""
        self.holdarg = ""


class Resolver(object):

    def __init__(self, env):
        self.env = env
        self.trace = []
        self.rejections = []
        self.cache_enabled = check_bool(env_unset_default(env, "XTE_CACHE_ENABLED", "true")) \
            if env_unset_default(env, "XTE_CACHE_ENABLED", "true") != "" else False
        self.cache_configured = "XTE_CACHE_ENABLED" in env
        compat_raw = env_unset_default(env, "XTE_EXECARG_COMPAT", "true")
        self.execarg_compat = check_bool(compat_raw) if compat_raw != "" else False
        self.compat_configured = "XTE_EXECARG_COMPAT" in env
        self.execarg_defaults = []
        self.entry_ids = []
        self.fallback = []
        self.excluded = []
        self.included = []
        self.aliases = {}
        self.config_files = []
        self.apps_dirs = []
        self.state = State()
        self.entry_path = ""
        self.entry_id = ""
        self.entry_action = ""

    # ---- paths -------------------------------------------------------------
    def desktops(self):
        return split_nws(ascii_lower(env_unset_default(self.env, "XDG_CURRENT_DESKTOP", "")), ":")

    def config_paths(self):
        out = []
        conf_home = env_default(self.env, "XDG_CONFIG_HOME",
                                os.path.join(self.env.get("HOME", ""), ".config"))
        conf_dirs = env_default(self.env, "XDG_CONFIG_DIRS", "/etc/xdg")
        desktops = [] if MODE == "nodesktop" else self.desktops()
        for d in split_nws(conf_home + ":" + conf_dirs, ":"):
            for ds in desktops:
                out.append(strip_one_slash(d) + "/" + ds + "-xdg-terminals.list")
            out.append(strip_one_slash(d) + "/xdg-terminals.list")
        for d in split_nws(env_default(self.env, "XDG_DATA_DIRS",
                                      "/usr/local/share:/usr/share"), ":"):
            for ds in desktops:
                out.append(strip_one_slash(d) + "/xdg-terminal-exec/" + ds
                           + "-xdg-terminals.list")
            out.append(strip_one_slash(d) + "/xdg-terminal-exec/xdg-terminals.list")
        return out

    def applications_dirs(self):
        data_home = env_default(self.env, "XDG_DATA_HOME",
                                os.path.join(self.env.get("HOME", ""), ".local/share"))
        data_dirs = env_default(self.env, "XDG_DATA_DIRS", "/usr/local/share:/usr/share")
        res = []
        for d in split_nws(data_home + ":" + data_dirs, ":"):
            res.insert(0, strip_one_slash(d) + "/applications/")
        if MODE == "reversed":
            res.reverse()
        return res

    # ---- config ------------------------------------------------------------
    def read_configs(self):
        for path in self.config_paths():
            if not os.path.isfile(path):
                continue
            self.config_files.append(path)
            self.trace.append("list %s" % path)
            try:
                text = decode(read_bytes(path))
            except OSError:
                continue
            for line in sh_lines(text):
                self.read_config_line(line, path)

    def read_config_line(self, line, path):
        if line in ("/enable_cache", "/disable_cache", "/execarg_compat", "/execarg_strict"):
            if line == "/enable_cache":
                if self.cache_configured:
                    return
                self.cache_enabled = True
                self.cache_configured = True
            elif line == "/disable_cache":
                if self.cache_configured:
                    return
                self.cache_enabled = False
                self.cache_configured = True
            elif line == "/execarg_compat":
                if self.compat_configured:
                    return
                self.execarg_compat = True
                self.compat_configured = True
            else:
                if self.compat_configured:
                    return
                self.execarg_compat = False
                self.compat_configured = True
            self.trace.append("directive %s (%s)" % (line, path))
            return
        if line.startswith("/execarg_default:") and line.count(":") >= 3:
            if not self.execarg_compat:
                return
            rest = line[len("/execarg_default:"):]
            head, _, tail = rest.partition(":")
            if valid_entry_id(head):
                self.execarg_defaults.append((head, tail))
            return
        first = line[:1]
        excl = ""
        body = line
        if first in "+-" and len(line) >= 2 and line[1] in ALNUM_:
            excl, body = first, line[1:]
        elif not (len(line) >= 1 and first in ALNUM_):
            return
        entry_id, _, action = body.partition(":")
        if valid_entry_id(entry_id) and valid_action_id(action):
            if excl == "":
                self.entry_ids.append(body)
                self.trace.append("entry id %s (%s)" % (body, path))
            elif excl == "+":
                if entry_id in self.excluded:
                    return
                if entry_id in self.included:
                    return
                self.included.append(entry_id)
            else:
                if entry_id in self.included:
                    return
                if entry_id in self.excluded:
                    return
                self.excluded.append(entry_id)
        else:
            warn("Discarded possibly misspelled entry '%s'" % body)

    # ---- entry registration ------------------------------------------------
    def register_entries(self):
        for d in self.applications_dirs():
            self.apps_dirs.append(d)
            start = d + "."
            self.walk(d, start, [])
        self.trace.append("data dirs %s" % ":".join(self.applications_dirs()))

    def walk(self, real, start, rel):
        try:
            entries = list(os.scandir(real))
        except OSError:
            return
        for de in entries:
            name = de.name
            sub_rel = rel + [name]
            printed = start + "/" + "/".join(sub_rel)
            try:
                if de.is_dir(follow_symlinks=True):
                    self.walk(os.path.join(real, name), start, sub_rel)
                    continue
            except OSError:
                continue
            try:
                if not de.is_file(follow_symlinks=True):
                    continue
            except OSError:
                continue
            tail = "/".join(sub_rel)
            if not (len(tail) >= 1 and tail[0] in ALNUM_ and tail.endswith(".desktop")):
                continue
            if any(c not in PATH_CHARS for c in tail):
                continue
            entry_id = printed.rsplit("/./", 1)[1].replace("/", "-")
            self.aliases[entry_id] = printed
            if entry_id in self.excluded:
                self.trace.append("entry %s excluded from fallback" % entry_id)
                continue
            self.fallback.insert(0, entry_id)

    # ---- desktop entry -----------------------------------------------------
    def read_entry(self, path, action, de_checks):
        """Returns True when the entry passed every check (shell state persists across calls)."""
        st = self.state
        read_exec = False
        action_listed = False
        try:
            text = decode(read_bytes(path))
        except OSError:
            return True
        for raw in sh_lines(text):
            line = raw
            if line.startswith("[Desktop Entry]"):
                if not action:
                    read_exec = True
                continue
            if line.startswith("[Desktop Action ") and action:
                if line.startswith("[Desktop Action %s]" % action):
                    if action_listed:
                        read_exec = True
                    else:
                        self.rejections.append((path, "action %r not listed in Actions" % action))
                        return False
                elif read_exec:
                    break
                continue
            if line.startswith("["):
                if read_exec:
                    break
                continue
            if not (len(line) >= 1 and (line[0] in ALNUM_ or line[0] == "-")):
                continue
            if "=" not in line:
                continue
            value = line.split("=", 1)[1].lstrip(" ")
            ok, action_listed = self.check_key(line, value, action, read_exec, de_checks,
                                               action_listed)
            if not ok:
                st.reset()
                self.rejections.append((path, "key rejected: %s" % line.split("=", 1)[0]))
                return False
        return True

    def skip_validation(self):
        return MODE in ("firstline", "novalidate")

    def check_key(self, line, value, action, read_exec, de_checks, action_listed):
        st = self.state
        if line.startswith("Categories"):
            if self.skip_validation():
                st.is_terminal = True
                return True, action_listed
            for cat in split_nws(value, ";"):
                if cat == "TerminalEmulator":
                    st.is_terminal = True
                    return True, action_listed
            return False, action_listed
        if line.startswith("Actions"):
            if action == "":
                return True, action_listed
            for cand in split_nws(value, ";"):
                if cand == action:
                    return True, True
            return False, action_listed
        if line.startswith("OnlyShowIn"):
            if not de_checks or self.skip_validation():
                return True, action_listed
            for target in split_nws(value, ";"):
                for desktop in split_nws(env_unset_default(self.env, "XDG_CURRENT_DESKTOP", ""), ":"):
                    if desktop == target:
                        return True, action_listed
            return False, action_listed
        if line.startswith("NotShowIn"):
            if not de_checks or self.skip_validation():
                return True, action_listed
            for target in split_nws(value, ";"):
                for desktop in split_nws(env_unset_default(self.env, "XDG_CURRENT_DESKTOP", ""), ":"):
                    if desktop == target:
                        return False, action_listed
            return True, action_listed
        if line.startswith("X-TerminalArgExec") or line.startswith("TerminalArgExec"):
            st.execarg = de_expand_str(value)
            st.execarg_defined = True
            return True, action_listed
        if line.startswith("X-ExecArg") or line.startswith("ExecArg"):
            if not self.execarg_compat:
                return True, action_listed
            st.execarg = de_expand_str(value)
            st.execarg_defined = True
            return True, action_listed
        if line.startswith("X-TerminalArgAppId") or line.startswith("TerminalArgAppId"):
            st.appidarg = de_expand_str(value)
            return True, action_listed
        if line.startswith("X-TerminalArgTitle") or line.startswith("TerminalArgTitle"):
            st.titlearg = de_expand_str(value)
            return True, action_listed
        if line.startswith("X-TerminalArgDir") or line.startswith("TerminalArgDir"):
            st.dirarg = de_expand_str(value)
            return True, action_listed
        if line.startswith("X-TerminalArgHold") or line.startswith("TerminalArgHold"):
            st.holdarg = de_expand_str(value)
            return True, action_listed
        if line.startswith("TryExec"):
            if self.skip_validation():
                return True, action_listed
            if not command_v(de_expand_str(value), self.env):
                return False, action_listed
            return True, action_listed
        if line.startswith("Hidden"):
            if self.skip_validation():
                return True, action_listed
            if value == "true":
                return False, action_listed
            return True, action_listed
        if line.startswith("Type") and MODE == "typecheck":
            if value != "Application":
                return False, action_listed
            return True, action_listed
        if line.startswith("Exec"):
            if not read_exec:
                return True, action_listed
            expanded = de_expand_str(value)
            tokens, ok = de_tokenize_exec(expanded)
            if ok:
                stripped, ok2 = strip_fields(tokens)
                if ok2:
                    tokens = stripped
            st.exec_tokens = tokens
            if not tokens:
                return False, action_listed
            if not command_v(tokens[0], self.env):
                return False, action_listed
            return True, action_listed
        return True, action_listed

    def default_execarg(self, entry_id):
        for cand, value in self.execarg_defaults:
            if cand == entry_id:
                return value
        return "-e"

    def find_entry(self):
        """Returns the selected entry id (shell state in self.state) or None."""
        seq = list(self.entry_ids) + ["//fallback_start//"] + self.fallback
        if MODE == "firstline":
            seq = self.entry_ids[:1]
        de_checks = False
        for token in seq:
            if token == "":
                continue
            if token == "//fallback_start//":
                de_checks = True
                continue
            if ":" in token:
                action = token.split(":", 1)[1]
                entry_id = token.rsplit(":", 1)[0]
            else:
                action = ""
                entry_id = token
            if entry_id not in self.aliases:
                self.rejections.append((entry_id, "no entry file"))
                continue
            path = self.aliases.pop(entry_id)
            if not self.read_entry(path, action, de_checks):
                continue
            st = self.state
            if not st.exec_tokens:
                self.rejections.append((path, "no Exec"))
                continue
            if not st.is_terminal:
                self.rejections.append((path, "not a TerminalEmulator"))
                continue
            if not st.execarg_defined:
                if self.execarg_compat:
                    st.execarg = self.default_execarg(entry_id)
                else:
                    self.rejections.append((path, "no TerminalArgExec in strict mode"))
                    continue
            self.entry_path = path
            self.entry_id = entry_id
            self.entry_action = action
            return entry_id
        return None


# ---- print mode ------------------------------------------------------------

def parse_print_args(args, execarg):
    opts = {"parts": [], "delim": "\\n", "cmd_delim": "\\n", "appid": "", "title": "",
            "dir": "", "hold": False, "rest": []}
    i = 0
    n = len(args)
    while i < n:
        a = args[i]
        i += 1
        if a == "--":
            opts["rest"] = args[i:]
            return opts
        if a == "-e" or (execarg and a == execarg):
            opts["rest"] = args[i:]
            return opts
        if a.startswith("--"):
            if a.startswith("--app-id="):
                opts["appid"] = a.split("=", 1)[1]
            elif a.startswith("--title="):
                opts["title"] = a.split("=", 1)[1]
            elif a.startswith("--dir="):
                opts["dir"] = a.split("=", 1)[1]
            elif a == "--hold":
                opts["hold"] = True
            elif a == "--print-path":
                opts["parts"].append("path")
            elif a == "--print-id":
                opts["parts"].append("id")
            elif a == "--print-content":
                opts["parts"].append("content")
            elif a == "--print-cmd":
                opts["parts"].append("cmd")
            elif a.startswith("--print-cmd="):
                opts["parts"].append("cmd")
                opts["cmd_delim"] = a.split("=", 1)[1]
            elif a.startswith("--print-delimiter="):
                opts["delim"] = a.split("=", 1)[1]
            elif a == "--test":
                opts["test"] = True
            # unknown options are discarded by the script
            continue
        if a.startswith("-"):
            continue
        opts["rest"] = args[i - 1:]
        return opts
    return opts


def build_command(res, opts):
    """Exec tokens, then --app-id, --title, --dir, --hold, the exec arg, then the user args."""
    st = res.state
    argv = []
    if opts["rest"] and st.execarg:
        argv = [st.execarg] + opts["rest"]
    else:
        argv = list(opts["rest"])
    if st.holdarg and opts["hold"]:
        argv = [st.holdarg] + argv
    if st.dirarg and opts["dir"]:
        if st.dirarg.endswith("="):
            argv = [st.dirarg + opts["dir"]] + argv
        else:
            argv = [st.dirarg, opts["dir"]] + argv
    if st.titlearg and opts["title"]:
        if st.titlearg.endswith("="):
            argv = [st.titlearg + opts["title"]] + argv
        else:
            argv = [st.titlearg, opts["title"]] + argv
    if st.appidarg and opts["appid"]:
        if st.appidarg.endswith("="):
            argv = [st.appidarg + opts["appid"]] + argv
        else:
            argv = [st.appidarg, opts["appid"]] + argv
    return list(st.exec_tokens) + argv


def print_mode(res, args):
    opts = parse_print_args(args, res.state.execarg)
    parts = opts["parts"]
    if not parts:
        warn("mado-terminal.py: no --print-* option; this tool never launches a terminal")
        return 2
    out = []
    first = True
    name = res.entry_id + ((":" + res.entry_action) if res.entry_action else "")
    if "id" in parts:
        out.append(name)
        first = False
    if "path" in parts:
        path = res.entry_path
        if "/./" in path:
            # ${P%%/./*} is the prefix before the FIRST /./, ${P##*/./} the tail after the LAST
            path = path.split("/./", 1)[0] + "/" + path.rsplit("/./", 1)[1]
        if not first:
            out.append(printf_b(opts["delim"]))
        out.append(path + ((":" + res.entry_action) if res.entry_action else ""))
        first = False
    if "content" in parts:
        if not first:
            out.append(printf_b(opts["delim"]))
        try:
            out.append(decode(read_bytes(res.entry_path)))
        except OSError:
            pass
        first = False
    if "cmd" not in parts:
        if "content" not in parts and opts["delim"] == "\\n":
            out.append("\n")
        sys.stdout.write("".join(out))
        return 0
    argv = build_command(res, opts)
    if not first:
        out.append(printf_b(opts["delim"]))
    delim = printf_b(opts["cmd_delim"]) if opts["cmd_delim"] != "" else "\n"
    out.append(delim.join(argv))
    if opts["cmd_delim"] == "\\n" or (not first and opts["delim"] == "\\n"):
        out.append("\n")
    sys.stdout.write("".join(out))
    return 0


def observed_lines(path):
    try:
        text = decode(read_bytes(path))
    except OSError:
        return None
    lines = text.split("\n")
    if text.endswith("\n"):
        lines = lines[:-1]
    return lines


def explain_mode(res, args):
    observed = None
    i = 0
    while i < len(args):
        if args[i] == "--observed":
            if i + 1 >= len(args):
                raise Usage("explain --observed needs a file")
            observed = args[i + 1]
            i += 2
            continue
        raise Usage("explain: unexpected argument %r" % args[i])
    selected = res.find_entry()
    for line in res.trace:
        sys.stdout.write("list  " + line + "\n")
    for who, why in res.rejections:
        sys.stdout.write("skip  %s: %s\n" % (who, why))
    if selected is None:
        sys.stdout.write("MADO_TERM: selected=- path=- verdict=NO_TERMINAL\n")
        return 3
    opts = {"parts": ["id", "path", "cmd"], "delim": "\\n", "cmd_delim": "\\n", "appid": "",
            "title": "", "dir": "", "hold": False, "rest": []}
    mine = []
    mine.append(res.entry_id + ((":" + res.entry_action) if res.entry_action else ""))
    path = res.entry_path
    if "/./" in path:
        path = path.split("/./", 1)[0] + "/" + path.rsplit("/./", 1)[1]
    mine.append(path)
    mine.append("\n".join(build_command(res, opts)))
    verdict = "OK"
    if observed is not None:
        lines = observed_lines(observed)
        verdict = "AGREE" if lines is not None and lines[:3] == mine else "DIFFER"
    sys.stdout.write("MADO_TERM: selected=%s path=%s verdict=%s\n"
                     % (mine[0], mine[1], verdict))
    return 0 if verdict in ("OK", "AGREE") else 1


# ---- selftest ---------------------------------------------------------------

def selftest_case(root, index, use_desktop_list):
    home = os.path.join(root, "home")
    conf = os.path.join(home, ".config")
    data = os.path.join(home, ".local", "share")
    apps = os.path.join(data, "applications")
    for d in (conf, apps, os.path.join(root, "bin")):
        os.makedirs(d, exist_ok=True)
    term = os.path.join(root, "bin", "term%d" % index)
    with open(term, "w") as fh:
        fh.write("#!/bin/sh\nexit 0\n")
    os.chmod(term, 0o755)
    list_name = ("hyprland-xdg-terminals.list" if use_desktop_list else
                 "xdg-terminals.list")
    with open(os.path.join(conf, list_name), "w") as fh:
        fh.write("Term%d.desktop\n" % index)
    entry = ("[Desktop Entry]\nType=Application\nName=Term %d\n"
             "Categories=System;TerminalEmulator;\n"
             "X-TerminalArgExec=-e\nX-TerminalArgDir=--working-directory=\n"
             "Exec=term%d\n" % (index, index))
    with open(os.path.join(apps, "Term%d.desktop" % index), "w") as fh:
        fh.write(entry)
    env = {"HOME": home, "PATH": os.path.join(root, "bin") + ":/usr/bin:/bin",
           "XDG_CONFIG_HOME": conf, "XDG_CONFIG_DIRS": os.path.join(root, "none"),
           "XDG_DATA_HOME": data, "XDG_DATA_DIRS": os.path.join(root, "none"),
           "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_CACHE_HOME": os.path.join(root, "cache")}
    res = Resolver(env)
    res.read_configs()
    res.register_entries()
    got = res.find_entry()
    ok = (got == "Term%d.desktop" % index and res.entry_path.endswith("Term%d.desktop" % index))
    if ok:
        out = print_mode(res, ["--print-cmd"])
        ok = out == 0
    if ok:
        out = print_mode(res, ["--print-id", "--print-path"])
        ok = out == 0 and res.entry_path
    return bool(ok)


def selftest():
    base = os.environ.get("TMPDIR") or os.getcwd()
    try:
        root = tempfile.mkdtemp(prefix="mado-terminal-selftest-", dir=base)
    except OSError:
        root = tempfile.mkdtemp(prefix="mado-terminal-selftest-")
    passed = 0
    total = 0
    try:
        for i in range(10):
            for use_desktop_list in (True, False, True):
                total += 1
                case = os.path.join(root, "c%d-%d-%d" % (i, use_desktop_list, total))
                try:
                    with contextlib.redirect_stdout(io.StringIO()):
                        if selftest_case(case, i, use_desktop_list):
                            passed += 1
                except Exception:
                    pass
    finally:
        shutil.rmtree(root, ignore_errors=True)
    sys.stdout.write("MADO_TERMINAL_SELFTEST: %d/%d passed\n" % (passed, total))
    return 0 if passed == total and total >= 30 else 1


def main(argv):
    if argv and argv[0] == "--selftest":
        return selftest()
    if argv and argv[0] in ("-h", "--help"):
        sys.stdout.write("usage: mado-terminal.py print [...] | explain [--observed FILE] "
                         "| --selftest\n")
        return 0
    if not argv:
        warn("usage: mado-terminal.py print [...] | explain [--observed FILE] | --selftest")
        return 2
    env = dict(os.environ)
    res = Resolver(env)
    res.read_configs()
    res.register_entries()
    if argv[0] == "print":
        if res.find_entry() is None:
            warn("No valid terminal entry was found in: %s" % ":".join(res.apps_dirs))
            return 1
        return print_mode(res, argv[1:])
    if argv[0] == "explain":
        try:
            return explain_mode(res, argv[1:])
        except Usage as exc:
            warn(str(exc))
            return 2
    warn("unknown subcommand %r" % argv[0])
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

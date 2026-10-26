#!/usr/bin/env python3
# mado-terminal.py — read-only model of the xdg-terminal-exec 0.14.3 selection.
#
# ============================================================================
# CONTRACT (draft, round 47 w1 ExecRefA)
# ============================================================================
#
# WHY: answer "which terminal does SUPER+RETURN launch, and why" without
# running anything.  The host hotkey is
#   ~/.config/hypr/bindings.conf:2
#     bindd = SUPER, RETURN, Terminal, exec, uwsm-app -- xdg-terminal-exec --dir="$(omarchy-cmd-terminal-cwd)"
# so the answer is "whatever xdg-terminal-exec 0.14.3 selects in this
# environment".  This file re-implements that selection in Python 3 stdlib
# only: it never starts a process (no subprocess/os.system/os.exec*/spawn/
# fork), never opens a socket, and never writes the resolver's cache.
#
# MODEL OF RECORD: /usr/bin/xdg-terminal-exec, 1499 lines,
#   sha256 89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac
#   (byte-equal to upstream tag v0.14.3).  Every model site below cites the
#   script's line numbers as `xte:NNN`; those line numbers are the ones
#   printed by `grep -n` on that file.  The script is `#!/bin/sh` and /bin/sh
#   is bash in POSIX mode on this host, so `command -v` requires an executable
#   regular file (probed: `command -v ./nox` on a 0644 file fails in sh mode,
#   succeeds in bash mode).
#
# SUBCOMMANDS
#
#   mado-terminal.py print [xdg-terminal-exec options and args]
#       stdout and exit status byte-identical to
#         XDG_CACHE_HOME=<empty dir> xdg-terminal-exec \
#             --print-id/--print-path/--print-cmd[=seq]/--print-delimiter=seq \
#             [--dir=..] [--title=..] [--app-id=..] [--hold] [cmd args]
#       in the same environment, for every print mode (also --print-content
#       and --test).  The resolver's own cache is out of contract: the tool
#       models a COLD cache (xte:1219-1226, read_cache at xte:210), which is
#       what XDG_CACHE_HOME=<empty dir> produces.
#       An invocation that would reach `exec "$@"` (xte:1499) — i.e. no
#       --print-* option and no --test — is refused with exit 2 and a stderr
#       note: launching a terminal is forbidden on this host, so such an
#       invocation is outside the byte-identical contract by construction.
#
#   mado-terminal.py explain [--observed FILE]
#       Human/machine trace of the selection: which list file and line
#       selected the entry, every candidate rejected and why, then the line
#         MADO_TERM: selected=<id> path=<path> verdict=OK|AGREE|DIFFER|NO_TERMINAL
#       With --observed FILE (captured output of
#         xdg-terminal-exec --print-id --print-path --print-cmd)
#       the verdict is AGREE when this tool's stdout for exactly that argument
#       list equals the file, DIFFER otherwise.  Exit: 0 OK/AGREE, 1 DIFFER,
#       3 NO_TERMINAL, 2 usage.
#
#   mado-terminal.py --selftest
#       Runs the embedded hermetic cases under $TMPDIR (or TMPDIR as set),
#       printing `MADO_TERMINAL_SELFTEST: N/N passed`.  The expected rc/stdout
#       of every case was produced by running the real pinned script on the
#       same materialised case (never typed by hand).
#
# WHERE THE MODEL CAME FROM (script structure, line numbers from grep -n)
#   xte:143-177  make_paths: config list order + applications dirs
#   xte:351-474  read_config_paths: directives, exclusion markers, list lines
#   xte:754-800  find_entry_paths: find -L + awk, alias per entry ID,
#                XTE__FALLBACK_ENTRY_IDS built by prepending
#   xte:802-968  check_entry_key: every desktop-entry key the script reads
#   xte:970-1018 read_entry_path: group headers, action groups, read_exec gate
#   xte:1020-1053 validate_entry_id / validate_action_id
#   xte:1055-1111 find_entry: candidate walk, post-checks, residue semantics
#   xte:1113-1135 get_default_execarg
#   xte:1214-1323 option parsing
#   xte:1325-1385 print modes
#   xte:1387-1499 option prepending, --test, --print-cmd, exec
#
# THE ONE PLACE THIS MODEL DELIBERATELY MATCHES A BUG: at xte:956-960 the
# script calls de_tokenize_exec and de_strip_fields without `|| return 1`, so
# a tokenizer error (unquoted `|`, unterminated quote) or a field error
# (`%z`, two `%f`) does NOT discard the entry.  The partially accumulated
# XTE__EXEC_USEP survives, only Exec[0] is gated by `command -v`, and the
# entry can still be selected (`Exec=sh | cat` prints `sh`).  Tools that
# "clean this up" will disagree with the script.
#
# ============================================================================
# DIVERGENCES THAT CANNOT BE MODELLED (each one is fatal-loud, not silent)
# ============================================================================
#  * A desktop-entry path containing a single quote breaks the shell's
#    `alias id="xte__entry_path='$path'"` (xte:782) into a syntax error; the
#    script dies under `set -e`.  We raise ShellFatal (same observable rc=1,
#    empty stdout) and record why.
#  * A FIFO/device where an entry file is expected: the shell blocks in
#    `done < "$path"`, we fail fast.  Not modelled, documented.
#  * Ambiguity of `readdir` order beyond what os.scandir reports: GNU find
#    walks operands in readdir order (probed: find /d/. order == scandir
#    order on this filesystem), and so does our walker.
# ============================================================================

import os
import re
import sys

TARGET = "xdg-terminal-exec"
TARGET_VERSION = "0.14.3"

USEP = "\x1f"   # xte:41 ASCII Unit Separator, Exec field separator
RSEP = "\x1e"   # xte:40 ASCII Record Separator, cache records
LF = "\n"

WS = " \t\n\v\f\r"                       # [[:space:]] in the C locale
_WS = frozenset(WS)
_SPECIAL = frozenset(WS) | frozenset('"`$\\\'><~|&;*?#()')

_ID_FIRST = re.compile(r"\A[a-zA-Z0-9_]")
_ID_SIGN = re.compile(r"\A[+-][a-zA-Z0-9_]")
_KV = re.compile(r"\A[a-zA-Z0-9-]")
_ALLOWED_PATH_CHARS = frozenset(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_./-")

HELP_TEXT = (
    "xdg-terminal-exec - Shell-based default terminal launcher.\n"
    "\n"
    "Implementation of the proposed Default Terminal Specification.\n"
    "\n"
    "Usage:\n"
    "  xdg-terminal-exec [options] [--] [command [arguments ...]]\n"
    "\n"
    "Launches given command in default terminal, or launches default terminal.\n"
    "\n"
    "Options for modifying terminal behavior (if supported by terminals's\n"
    "entry):\n"
    "\n"
    "  --app-id=app-id    set app-id (Wayland) or window class (X11)\n"
    "  --title=title      set tile of terminal.\n"
    "  --dir=workdir      set workdir of terminal.\n"
    "  --hold             instruct terminal to hold after command ends.\n"
    "\n"
    "Options for printing data instead of executing terminal:\n"
    "\n"
    "  --print-id\n"
    "      print selected Desktop Entry ID. Action is appended delimited\n"
    "      by \":\".\n"
    "\n"
    "  --print-path\n"
    "      print path to selected Desktop Entry. Action is appended\n"
    "      delimited by \":\".\n"
    "\n"
    "  --print-content\n"
    "      print content of selected Desktop Entry. Conflicts with --print-cmd.\n"
    "\n"
    "  --print-cmd[=printf_sequence]\n"
    "      print resulting command line, delimited by given printf sequence,\n"
    "      \"\\n\" by default. If sequence is \"\\n\", output is also terminated with\n"
    "      a newline.\n"
    "\n"
    "  --print-delimiter=printf_sequence\n"
    "      printf sequence to be used as the delimiter between multiple requested\n"
    "      print statements, \"\\n\" by default. If sequence is \"\\n\", output is\n"
    "      also terminated with a newline.\n"
    "\n"
    "Configuration:\n"
    "\n"
    "Preferred terminals are configured by listing their Desktop Entry IDs\n"
    "in config files named \"[${desktop}-]xdg-terminals.list\" placed in XDG Config\n"
    "hierarchy. Where \"${desktop}\" is a lowercased string that is matched\n"
    "(case-insensitively) against items of \"${XDG_CURRENT_DESKTOP}\".\n"
    "\n"
    "See \"man xdg-terminal-exec\" for more details.\n"
)

USAGE = ("usage: mado-terminal.py print [xdg-terminal-exec options and args]\n"
         "       mado-terminal.py explain [--observed FILE]\n"
         "       mado-terminal.py --selftest\n")

# `print` exit status for the one invocation shape where the real script never
# returns: an empty argument before `--` makes its option loop spin forever.
HANG_RC = 4


class ShellFatal(Exception):
    """The shell script dies here under `set -e` with empty stdout."""


# ---------------------------------------------------------------------------
# small shell primitives
# ---------------------------------------------------------------------------

def encode(s):
    return s.encode("utf-8", "surrogateescape")


def decode(b):
    return b.decode("utf-8", "surrogateescape")


def check_bool(v):
    """xte:55-67 check_bool. Anything unrecognised means no."""
    if v in ("true", "True", "TRUE", "yes", "Yes", "YES", "1"):
        return True
    return False


def ifs_split(value, ch):
    """Unquoted expansion + field splitting on a single non-whitespace IFS char.

    bash keeps interior empty fields and drops trailing ones
    (probed: IFS=';' v='a;;b;' -> a, '', b).
    """
    if value == "":
        return []
    parts = value.split(ch)
    while parts and parts[-1] == "":
        parts.pop()
    return parts


def read_split(line, ch, nvars):
    """`IFS=<ch> read -r v1 .. vN` for a non-whitespace IFS char.

    Probed against bash 5.3: the last variable receives the raw remainder,
    minus exactly one trailing delimiter when the remainder ends with a
    single delimiter ('abc=' -> 'abc', 'abc==' -> 'abc==', 'a:b:' with three
    variables -> c='').
    """
    vals = []
    pos = 0
    for _ in range(nvars - 1):
        i = line.find(ch, pos)
        if i < 0:
            vals.append(line[pos:])
            while len(vals) < nvars:
                vals.append("")
            return vals
        vals.append(line[pos:i])
        pos = i + 1
    rest = line[pos:]
    if rest.endswith(ch) and not rest.endswith(ch + ch):
        rest = rest[:-1]
    vals.append(rest)
    return vals


def strip_ifs_ws(line):
    """`read` with the default IFS trims leading/trailing space and tab."""
    return line.strip(" \t")


def list_contains(list_str, item):
    """xte:299-307 list_contains: substring test on the delimited string."""
    return (LF + list_str + LF).find(LF + item + LF) >= 0


def replace_all(s, a, b):
    """xte:457-484 replace: left-to-right non-overlapping substitution."""
    return s.replace(a, b)


def de_expand_str(s):
    """xte:486-560 de_expand_str: \\s \\n \\t \\r \\\\ ; other escapes drop the
    backslash and keep the character (the passthrough branch is commented
    out at xte:550-552)."""
    out = []
    rem = s
    while True:
        i = rem.find("\\")
        if i < 0:
            out.append(rem)
            break
        out.append(rem[:i])
        rem = rem[i + 1:]
        if rem == "":
            break
        c = rem[0]
        rem = rem[1:]
        if c == "s":
            out.append(" ")
        elif c == "n":
            out.append(LF)
        elif c == "t":
            out.append("\t")
        elif c == "r":
            out.append("\r")
        elif c == "\\":
            out.append("\\")
        else:
            out.append(c)
    return "".join(out)


def de_tokenize_exec(s):
    """xte:561-692 de_tokenize_exec.  Returns (ok, string).

    On the shell's `return 1` paths the partially accumulated
    XTE__EXEC_USEP is what the caller keeps (xte:958 has no `|| return 1`),
    so the string is returned either way.
    """
    acc = []
    rem = s
    quoted = 0
    in_space = 0
    n = len(rem)
    i = 0
    while i < n:
        j = i
        while j < n and rem[j] not in _SPECIAL:
            j += 1
        left = rem[i:j]
        acc.append(left)
        if j == n:
            break
        ch = rem[j]
        i = j + 1
        # xte:597-607: `case "${in_space}${left}${ch}" in 1[[:space:]]) ...`
        # left never contains a special char, so it is empty here and the
        # first branch matches only when ch itself is that whitespace.
        if in_space:
            if left == "" and ch in _WS:
                continue
            in_space = 0
        if quoted == 0 and ch == '"':
            quoted = 1
            continue
        if quoted == 1 and ch == '"':
            quoted = 0
            continue
        if quoted == 0 and ch in "`$\\'><~|&;*?#()":
            return False, "".join(acc)
        if quoted == 1 and ch in "`$":
            return False, "".join(acc)
        if quoted == 1 and ch == "\\":
            if i >= n:
                return False, "".join(acc)   # dangling backslash
            acc.append(rem[i])
            i += 1
            continue
        if quoted == 0 and ch in _WS:
            if any(c not in _WS for c in rem[i:]):
                acc.append(USEP)
                in_space = 1
            else:
                break                        # trailing space is not a separator
            continue
        if quoted == 1 and (ch in _WS or ch in "'><~|&;*?#()"):
            acc.append(ch)
            continue
        return False, "".join(acc)
    if quoted == 1:
        return False, "".join(acc)           # unterminated quote (xte:684-689)
    return True, "".join(acc)


_DEPRECATED = re.compile(r"\A(?:.*[^%]%[dDnNvm].*|%[dDnNvm].*)\Z", re.S)
_FILE_FIELD = re.compile(r"\A(?:.*[^%]%[fFuU].*|%[fFuU].*)\Z", re.S)
_ICON_FIELD = re.compile(r"\A(?:.*[^%]%i.*|%i.*|.*[^%]%c.*|%c.*)\Z", re.S)
_LITERAL_PC = re.compile(r"\A(?:.*[^%]%%.*|%%.*)\Z", re.S)
_BAD_FIELD = re.compile(r"\A(?:.*%.+.*|.*[^%]%)\Z", re.S)


def de_strip_fields(usep_str):
    """xte:694-740 de_strip_fields.  Returns (ok, string).

    On failure the shell returns 1 *before* assigning XTE__EXEC_USEP
    (xte:738-739), so the caller keeps the tokenizer's string.
    """
    if usep_str == "":
        fields = []
    else:
        fields = usep_str.split(USEP)
    out = ""
    fu_found = False
    for arg in fields:
        if _DEPRECATED.match(arg):
            continue
        if _FILE_FIELD.match(arg):
            if fu_found:
                return False, ""
            fu_found = True
            continue
        if _ICON_FIELD.match(arg):
            continue
        if _LITERAL_PC.match(arg):
            rarg = replace_all(arg, "%%", "%")
            out = out + (USEP if out else "") + rarg
            continue
        if _BAD_FIELD.match(arg):
            return False, ""
        out = out + (USEP if out else "") + arg
    return True, out


def printf_b(seq):
    """bash `printf '%b'`.  Returns (bytes, terminated) where terminated is
    True when a \\c stopped the output."""
    out = bytearray()
    i = 0
    n = len(seq)
    simple = {"a": b"\a", "b": b"\b", "e": b"\x1b", "E": b"\x1b", "f": b"\f",
              "n": b"\n", "r": b"\r", "t": b"\t", "v": b"\v"}
    while i < n:
        c = seq[i]
        if c != "\\":
            out += encode(c)
            i += 1
            continue
        i += 1
        if i >= n:
            out += b"\\"
            break
        c = seq[i]
        if c == "c":
            return bytes(out), True
        i += 1
        if c in simple:
            out += simple[c]
        elif c == "\\":
            out += b"\\"
        elif c in "01234567":
            digits = ""
            if c == "0":
                while i < n and len(digits) < 3 and seq[i] in "01234567":
                    digits += seq[i]
                    i += 1
            else:
                digits = c
                while i < n and len(digits) < 3 and seq[i] in "01234567":
                    digits += seq[i]
                    i += 1
            out.append((int(digits, 8) if digits else 0) & 0xFF)
        elif c == "x":
            h = ""
            while i < n and len(h) < 2 and seq[i] in "0123456789abcdefABCDEF":
                h += seq[i]
                i += 1
            if h:
                out.append(int(h, 16) & 0xFF)
            else:
                out += b"\\x"
        else:
            out += b"\\" + encode(c)
    return bytes(out), False


def ifs_words(value, ifs):
    """Unquoted-expansion word splitting on an arbitrary IFS value.

    Only used to reproduce the diagnostic message at xte:1109, whose argument
    splits differently depending on a leaked IFS.
    """
    if value == "":
        return []
    delims = set(ifs)
    words = []
    cur = []
    for c in value:
        if c in delims:
            words.append("".join(cur))
            cur = []
        else:
            cur.append(c)
    words.append("".join(cur))
    ws = set(" \t\n")
    words = [w for w in words if w != "" or not (delims & ws)]
    while words and words[-1] == "":
        words.pop()
    return words


def validate_entry_id(s):
    """xte:1036-1058."""
    if s == "" or s == ".desktop":
        return False
    for c in s:
        if c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-":
            return False
    return s.endswith(".desktop")


def validate_action_id(s):
    """xte:1060-1077."""
    if s == "":
        return True
    for c in s:
        if c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-":
            return False
    return True


def _exec_ok(p):
    try:
        if os.path.isdir(p):
            return False
        if not os.path.isfile(p):
            return False
        return os.access(p, os.X_OK)
    except OSError:
        return False


def command_v(name, env):
    """`command -v` as bash does it in POSIX mode (/bin/sh on this host)."""
    if name == "":
        return False
    if "/" in name:
        return _exec_ok(name)
    path = env.get("PATH", "")
    for d in path.split(":"):
        if _exec_ok((d if d else ".") + "/" + name):
            return True
    return False


def read_file_lines(path):
    """`while read -r line; do ...; done < path`.

    A final line without a trailing newline is never seen by the loop body,
    and NUL bytes cannot live in a shell variable.
    """
    if os.path.isdir(path):
        raise ShellFatal("read: %s: Is a directory" % path)
    if not os.path.isfile(path):
        raise ShellFatal("read: %s: not a regular file" % path)
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError as exc:
        raise ShellFatal("read: %s: %s" % (path, exc))
    text = decode(data)
    return [ln.replace("\x00", "") for ln in text.split(LF)[:-1]]


def lower_ascii(s):
    """tr '[:upper:]' '[:lower:]' (xte:1183). ASCII-only model."""
    out = []
    for c in s:
        if "A" <= c <= "Z":
            out.append(chr(ord(c) + 32))
        else:
            out.append(c)
    return "".join(out)


# ---------------------------------------------------------------------------
# the resolver
# ---------------------------------------------------------------------------

class Resolver:
    """One xdg-terminal-exec run, from make_paths to find_entry."""

    def __init__(self, env, trace=None, stderr=None):
        self.env = env
        self.trace = trace          # list, or None
        self.stderr = stderr if stderr is not None else sys.stderr
        self.st = self._fresh_state()
        self.execarg_compat = env.get("XTE_EXECARG_COMPAT", "true")
        # xte:33 XTE__OIFS; leaked IFS is observable in the "No valid terminal
        # entry" message (xte:1109), where `IFS=':' error ... ${dirs}` splits
        # the colon-joined list into one line per directory only when a
        # previous check leaked IFS=':' (see check_entry_key, empty
        # XDG_CURRENT_DESKTOP + OnlyShowIn/NotShowIn).  Modelled exactly.
        self.ifs = " \t\n"
        self.execarg_defaults = []
        self.configs = []
        self.app_dirs = []
        self.reason = ""
        self.reason_site = ""

    # -- state -----------------------------------------------------------
    @staticmethod
    def _fresh_state():
        # xte:765-775 reset_keys
        return {
            "is_terminal": "",
            "exec_usep": "",
            "execarg": "-e",
            "execarg_defined": "false",
            "appidarg": "",
            "titlearg": "",
            "dirarg": "",
            "holdarg": "",
        }

    def reset_keys(self):
        self.st.update(self._fresh_state())

    def note(self, kind, *args):
        if self.trace is not None:
            self.trace.append((kind,) + args)

    def reject(self, reason, site):
        self.reason = reason
        self.reason_site = site

    # -- environment -----------------------------------------------------
    def var(self, name):
        """${NAME-} : empty when unset."""
        return self.env.get(name, "")

    def var_default(self, name, default):
        """${NAME:-default} : default when unset or empty."""
        v = self.env.get(name)
        return v if v else default

    # -- xte:184-200 make_paths -----------------------------------------
    def make_paths(self):
        home = self.env.get("HOME", "")
        # OnlyShowIn/NotShowIn compare against the RAW value (xte:856-900);
        # only the list-file prefix uses the lowercased one (xte:1183).
        self.desktops = ifs_split(self.var("XDG_CURRENT_DESKTOP"), ":")
        desktops = ifs_split(lower_ascii(self.var("XDG_CURRENT_DESKTOP")), ":")
        configs = []
        cfg_home = self.var_default("XDG_CONFIG_HOME", home + "/.config")
        cfg_dirs = self.var_default("XDG_CONFIG_DIRS", "/etc/xdg")
        for d in ifs_split(cfg_home + ":" + cfg_dirs, ":"):
            dd = d[:-1] if d.endswith("/") else d
            for desk in desktops:
                configs.append(dd + "/" + desk + "-xdg-terminals.list")
            configs.append(dd + "/xdg-terminals.list")
        data_home = self.var_default("XDG_DATA_HOME", home + "/.local/share")
        data_dirs = self.var_default("XDG_DATA_DIRS", "/usr/local/share:/usr/share")
        for d in ifs_split(data_dirs, ":"):
            dd = d[:-1] if d.endswith("/") else d
            for desk in desktops:
                configs.append(dd + "/xdg-terminal-exec/" + desk + "-xdg-terminals.list")
            configs.append(dd + "/xdg-terminal-exec/xdg-terminals.list")
        app_dirs = []
        for d in ifs_split(data_home + ":" + data_dirs, ":"):
            dd = d[:-1] if d.endswith("/") else d
            app_dirs.insert(0, dd + "/applications/")
        self.configs = configs
        self.app_dirs = app_dirs
        self.cache_file = self.var_default(
            "XDG_CACHE_HOME", home + "/.cache") + "/" + TARGET

    # -- xte:334-455 read_config_paths ----------------------------------
    def read_config_paths(self):
        entry_ids = []
        excluded = []
        included = []
        cache_configured = self.env.get("XTE_CACHE_ENABLED", "")
        compat_configured = self.env.get("XTE_EXECARG_COMPAT", "")
        cache_enabled = "true"
        compat = self.execarg_compat
        for path in self.configs:
            if not os.path.isfile(path):
                self.note("config-absent", path)
                continue
            self.note("config", path)
            for lineno, raw in enumerate(read_file_lines(path), 1):
                line = strip_ifs_ws(raw)   # `read` with the default IFS
                if line in ("/enable_cache", "/disable_cache"):
                    self.note("directive", path, lineno, line, bool(cache_configured))
                    if not cache_configured:
                        cache_enabled = "true" if line == "/enable_cache" else "false"
                        cache_configured = "1"
                    continue
                if line in ("/execarg_compat", "/execarg_strict"):
                    self.note("directive", path, lineno, line, bool(compat_configured))
                    if not compat_configured:
                        compat = "true" if line == "/execarg_compat" else "false"
                        compat_configured = "1"
                    continue
                if (line.startswith("/execarg_default:")
                        and line.find(":", len("/execarg_default:")) >= 0):
                    if not check_bool(compat):
                        self.note("directive-ignored", path, lineno, line, "strict mode")
                        continue
                    _d, eid, dflt = read_split(line, ":", 3)
                    if validate_entry_id(eid):
                        self.execarg_defaults.append((eid, dflt))
                        self.note("directive", path, lineno, line, True)
                    else:
                        self.note("directive-invalid", path, lineno, line)
                    continue
                if _ID_FIRST.match(line) or _ID_SIGN.match(line):
                    body = line
                    excl = ""
                    if body[0] in "+-":
                        excl = body[0]
                        body = body[1:]
                    eid, act = read_split(body, ":", 2)
                    if validate_entry_id(eid) and validate_action_id(act):
                        if excl == "":
                            entry_ids.append(body)
                            self.note("list-entry", path, lineno, body, "preferred")
                        elif excl == "+":
                            if list_contains("\n".join(excluded), eid):
                                self.note("list-entry", path, lineno, body,
                                          "fallback exclusion already prevented")
                            elif list_contains("\n".join(included), eid):
                                self.note("list-entry", path, lineno, body,
                                          "already included")
                            else:
                                included.append(eid)
                                self.note("list-entry", path, lineno, body, "include")
                        else:
                            if list_contains("\n".join(included), eid):
                                self.note("list-entry", path, lineno, body,
                                          "include already prevented")
                            elif list_contains("\n".join(excluded), eid):
                                self.note("list-entry", path, lineno, body,
                                          "already excluded")
                            else:
                                excluded.append(eid)
                                self.note("list-entry", path, lineno, body, "exclude")
                    else:
                        self.note("list-entry", path, lineno, body, "misspelled, discarded")
                        self.stderr.write("Discarded possibly misspelled entry '%s'\n"
                                          % body)
                    continue
                self.note("list-line-ignored", path, lineno, line)
        self.entry_ids = entry_ids
        self.excluded_ids = excluded
        self.included_ids = included
        self.cache_enabled = cache_enabled
        self.execarg_compat = compat

    # -- xte:736-798 find_entry_paths -----------------------------------
    def find_entry_paths(self):
        aliases = {}
        fallback = []
        excluded = "\n".join(self.excluded_ids)
        for idx, d in enumerate(self.app_dirs):
            operand = d + "."          # d ends with '/', so this is "dir/."
            first = idx == 0
            self.note("app-dir", d, first, "typed" if first else "path-only")
            for disp, rel, is_file in _walk(d, operand):
                if first and not is_file:
                    continue
                if not _path_conditions(rel):
                    continue
                eid = rel.replace("/", "-")
                aliases[eid] = disp
                self.note("register", disp, eid)
                if list_contains(excluded, eid):
                    self.note("fallback-excluded", eid)
                    continue
                fallback.insert(0, eid)
        self.aliases = aliases
        self.fallback = fallback

    # -- xte:803-974 check_entry_key ------------------------------------
    def check_entry_key(self, line, value, action, read_exec, de_checks):
        def pfx(key):
            # shell pattern 'key'*=* : prefix, then at least one '=' after it
            return line.startswith(key) and "=" in line[len(key):]

        if pfx("Categories"):
            # xte:816-831: `IFS=';'` is set before the loop and restored at
            # the top of each iteration, so an EMPTY value leaves IFS=';'.
            cats = ifs_split(value, ";")
            self.ifs = " \t\n" if cats else ";"
            if "TerminalEmulator" in cats:
                self.st["is_terminal"] = "true"
                return True
            self.reject("Categories without TerminalEmulator: %r" % value,
                        "xte:816-831")
            return False
        if pfx("Actions"):
            if action == "":
                return True
            acts = ifs_split(value, ";")
            self.ifs = " \t\n" if acts else ";"
            if action in acts:
                self.st["action_listed"] = "true"
                return True
            self.reject("action %r not in Actions=%r" % (action, value), "xte:833-846")
            return False
        if pfx("OnlyShowIn"):
            if not de_checks:
                return True
            # xte:846-863: IFS=':' is left behind when the inner loop over
            # ${XDG_CURRENT_DESKTOP} never runs, and IFS=';' when the value
            # has no fields at all.
            targets = ifs_split(value, ";")
            if not targets:
                self.ifs = ";"
            elif not self.desktops:
                self.ifs = ":"
            for t in targets:
                if t in self.desktops:
                    self.ifs = " \t\n"
                    return True
            self.reject("OnlyShowIn=%r does not contain any of %r"
                        % (value, self.var("XDG_CURRENT_DESKTOP")), "xte:846-863")
            return False
        if pfx("NotShowIn"):
            if not de_checks:
                return True
            targets = ifs_split(value, ";")
            if not targets:
                self.ifs = ";"
            elif not self.desktops:
                self.ifs = ":"
            for t in targets:
                if t in self.desktops:
                    self.reject("NotShowIn=%r contains %r" % (value, t), "xte:865-887")
                    return False
            self.ifs = " \t\n" if targets and self.desktops else self.ifs
            return True
        if pfx("X-TerminalArgExec") or pfx("TerminalArgExec"):
            self.st["execarg"] = de_expand_str(value)
            self.st["execarg_defined"] = "true"
            return True
        if pfx("X-ExecArg") or pfx("ExecArg"):
            if self.execarg_compat == "false":
                return True
            self.st["execarg"] = de_expand_str(value)
            self.st["execarg_defined"] = "true"
            return True
        if pfx("X-TerminalArgAppId") or pfx("TerminalArgAppId"):
            self.st["appidarg"] = de_expand_str(value)
            return True
        if pfx("X-TerminalArgTitle") or pfx("TerminalArgTitle"):
            self.st["titlearg"] = de_expand_str(value)
            return True
        if pfx("X-TerminalArgDir") or pfx("TerminalArgDir"):
            self.st["dirarg"] = de_expand_str(value)
            return True
        if pfx("X-TerminalArgHold") or pfx("TerminalArgHold"):
            self.st["holdarg"] = de_expand_str(value)
            return True
        if pfx("TryExec"):
            exp = de_expand_str(value)
            if command_v(exp, self.env):
                return True
            self.reject("TryExec=%r not executable on PATH" % exp, "xte:952-957")
            return False
        if pfx("Hidden"):
            if value == "true":
                self.reject("Hidden=true", "xte:958-966")
                return False
            return True
        if pfx("Exec"):
            if not read_exec:
                return True
            exp = de_expand_str(value)
            tok_ok, tok = de_tokenize_exec(exp)
            strip_ok, stripped = de_strip_fields(tok)
            # xte:956-960: neither call is guarded by `|| return 1`, so a
            # failure leaves the partially accumulated value in place and only
            # Exec[0] decides.  Recorded so `explain` can say so.
            if not tok_ok or not strip_ok:
                self.note("exec-partial", value, tok, tok_ok, strip_ok)
            if strip_ok:
                exec_usep = stripped
                self.ifs = " \t\n"
            else:
                exec_usep = tok
                self.ifs = USEP          # de_strip_fields returns before IFS restore
            self.st["exec_usep"] = exec_usep
            exec0 = exec_usep.split(USEP)[0] if exec_usep != "" else ""
            if command_v(exec0, self.env):
                return True
            self.reject("Exec[0]=%r not executable on PATH" % exec0, "xte:962")
            return False
        return True

    # -- xte:986-1033 read_entry_path -----------------------------------
    def read_entry_path(self, path, action, de_checks):
        read_exec = False
        self.st["action_listed"] = ""
        self.note("candidate-file", path, action, de_checks)
        for lineno, raw in enumerate(read_file_lines(path), 1):
            line = strip_ifs_ws(raw)
            if line.startswith("[Desktop Entry]"):
                if action == "":
                    read_exec = True
                continue
            if line and _KV.match(line):
                value = line.split("=", 1)[1] if "=" in line else line
                value = value.lstrip(" ")
                if self.check_entry_key(line, value, action, read_exec, de_checks):
                    continue
                self.note("discard", path, lineno, line, self.reason, self.reason_site)
                self.reset_keys()
                return False
            if line.startswith("[Desktop Action " + action + "]"):
                if self.st.get("action_listed") == "true":
                    read_exec = True
                else:
                    self.reject("action group %r without %r in Actions"
                                % (line, action), "xte:1020-1028")
                    self.note("discard", path, lineno, line, self.reason, self.reason_site)
                    return False
                continue
            if line.startswith("["):
                if read_exec:
                    break
                continue
        if self.st["exec_usep"] == "" and self.st["is_terminal"] != "":
            self.reject("no Exec= in the read group", "xte:1094-1096")
        return True

    # -- xte:1146-1165 get_default_execarg ------------------------------
    def get_default_execarg(self, eid):
        for did, val in self.execarg_defaults:
            if did == eid:
                return val
        return "-e"

    # -- xte:1080-1140 find_entry ---------------------------------------
    def find_entry(self):
        seq = list(self.entry_ids)
        seq.append("//fallback_start//")
        seq.extend(self.fallback)
        de_checks = False
        cand_no = 0
        for item in seq:
            if ":" in item:
                action = item.split(":", 1)[1]
                eid = item.rsplit(":", 1)[0]
            elif item == "":
                continue
            elif item == "//fallback_start//":
                de_checks = True
                self.note("fallback-start")
                continue
            else:
                action = ""
                eid = item
            self.ifs = " \t\n"       # xte:1061 IFS=$XTE__OIFS, per iteration
            cand_no += 1
            if eid not in self.aliases:
                self.note("candidate", cand_no, item, None, "REJECT",
                          "not found: no *-xdg-terminals.list line and no "
                          "applications/ entry with this ID")
                continue
            path = self.aliases.pop(eid)
            self.reason = ""
            self.reason_site = ""
            try:
                ok = self.read_entry_path(path, action, de_checks)
            except ShellFatal as exc:
                self.note("candidate", cand_no, item, path, "FATAL", str(exc))
                raise
            if not ok:
                self.note("candidate", cand_no, item, path, "REJECT", self.reason)
                continue
            if self.st["exec_usep"] == "":
                self.note("candidate", cand_no, item, path, "REJECT",
                          "no Exec= read for this entry (residue kept: run continues)")
                continue
            if self.st["is_terminal"] == "":
                self.note("candidate", cand_no, item, path, "REJECT",
                          "entry never categorised as TerminalEmulator "
                          "(residue kept: run continues)")
                continue
            if self.st["execarg_defined"] != "true":
                if check_bool(self.execarg_compat):
                    self.st["execarg"] = self.get_default_execarg(eid)
                    self.note("execarg-default", eid, self.st["execarg"])
                else:
                    self.note("candidate", cand_no, item, path, "REJECT",
                              "no TerminalArgExec= and XTE_EXECARG_COMPAT is not true "
                              "(strict mode)")
                    continue
            self.note("candidate", cand_no, item, path, "ACCEPT", "")
            return path, eid, action
        return None

    # -- whole run up to find_entry -------------------------------------
    def resolve(self):
        self.make_paths()
        self.note("paths", self.configs, self.app_dirs, self.cache_file)
        self.read_config_paths()
        self.find_entry_paths()
        self.note("entry-ids", self.entry_ids)
        self.note("fallback", self.fallback)
        return self.find_entry()


def _path_conditions(rel):
    """The two -path tests of xte:757-773, applied to the part of the path
    after the operand's `/./`."""
    if rel == "" or rel[0] not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_":
        return False
    if not rel.endswith(".desktop") or len(rel) < 9:
        return False
    for c in rel:
        if c not in _ALLOWED_PATH_CHARS:
            return False
    return True


def _walk(base, operand):
    """GNU find -L pre-order traversal in readdir order (xte:786-798).

    Yields (display_path, path_after_dot_slash, is_regular_file).
    """
    out = []
    seen = set()

    def rec(real, rel):
        try:
            st = os.stat(real)
        except OSError:
            return
        key = (st.st_dev, st.st_ino)
        if key in seen:
            return                      # filesystem loop, find warns and skips
        seen.add(key)
        try:
            entries = list(os.scandir(real))
        except OSError:
            seen.discard(key)
            return
        for e in entries:
            r = e.name if rel == "" else rel + "/" + e.name
            disp = operand + "/" + r
            try:
                is_file = e.is_file(follow_symlinks=True)
                is_dir = e.is_dir(follow_symlinks=True)
            except OSError:
                is_file = False
                is_dir = False
            out.append((disp, r, is_file))
            if is_dir:
                rec(e.path, r)
        seen.discard(key)

    rec(base, "")
    return out


# ---------------------------------------------------------------------------
# the whole print pipeline (xte:1168-1499)
# ---------------------------------------------------------------------------

def run(env, argv, trace=None, stderr=None):
    """One modelled run.  Returns (rc, stdout_bytes, info).

    Never starts a process and never touches the resolver cache.
    """
    if stderr is None:
        stderr = sys.stderr
    # xte:1168-1178: -h/--help anywhere before -- wins, unconditionally.
    for a in argv:
        if a == "--":
            break
        if a in ("-h", "--help"):
            return 0, encode(HELP_TEXT), {"help": True}
    r = Resolver(env, trace, stderr)
    found = r.resolve()
    if found is None:
        # xte:1109: `IFS=':' error ... ${XTE__APPLICATIONS_DIRS}` -- the IFS
        # prefix is not in effect during the argument expansion, so the
        # colon-joined list arrives as ONE word and prints on one line.
        stderr.write("No valid terminal entry was found in:\n")
        for word in ifs_words(":".join(r.app_dirs), r.ifs) or [""]:
            stderr.write(word + LF)
        return 1, b"", {"no_terminal": True, "resolver": r}
    entry_path, entry_id, entry_action = found
    st = r.st

    # -- xte:1276-1395 option processing --------------------------------
    appidval = ""
    titleval = ""
    dirval = ""
    hold = False
    test_mode = False
    print_data = []                      # tokens of $XTE__PRINT_DATA
    print_delim = "\\n"                  # $XTE__PRINT_DELIMITER
    print_cmd_delim = "\\n"              # $XTE__PRINT_CMD_DELIMITER
    i = 0
    n = len(argv)
    while i < n:
        a = argv[i]
        if a == "--":
            i += 1
            break
        if a == "-e" or a == st["execarg"]:
            i += 1
            break
        if a.startswith("--app-id="):
            appidval = read_split(a, "=", 2)[1]
            i += 1
            continue
        if a.startswith("--title="):
            titleval = read_split(a, "=", 2)[1]
            i += 1
            continue
        if a.startswith("--dir="):
            dirval = read_split(a, "=", 2)[1]
            i += 1
            continue
        if a == "--hold":
            hold = True
            i += 1
            continue
        if a == "--test":
            test_mode = True
            i += 1
            continue
        if a == "--print-path":
            print_data.append("path")
            i += 1
            continue
        if a == "--print-id":
            print_data.append("id")
            i += 1
            continue
        if a == "--print-content":
            print_data.append("content")
            i += 1
            continue
        if a == "--print-cmd":
            print_data.append("cmd")
            i += 1
            continue
        if a.startswith("--print-cmd="):
            print_data.append("cmd")
            print_cmd_delim = read_split(a, "=", 2)[1]
            i += 1
            continue
        if a.startswith("--print-delimiter="):
            print_delim = read_split(a, "=", 2)[1]
            i += 1
            continue
        if a == "":
            # No case arm matches the empty word and no shift happens, so the
            # real `while [ "$#" -gt 0 ]` loop (xte:1277-1394) spins forever.
            # Observed: `xdg-terminal-exec ""` and `... --print-id ""` never
            # return (timeout 124).  We cannot hang, so we report it.
            stderr.write("mado-terminal.py: the real resolver never returns for an "
                         "empty argument before `--` (option loop matches no case "
                         "arm and does not shift); refusing\n")
            return HANG_RC, b"", {"hang": True, "selected": found, "resolver": r}
        if not a.startswith("-"):
            break                        # first non-option ends option parsing
        i += 1                           # unknown option is discarded (xte:1392)
    rest = list(argv[i:])

    # -- xte:1397-1447 print the requested data ------------------------
    first = True
    out = bytearray()
    if "id" in print_data:
        out += encode(entry_id + (":" + entry_action if entry_action else ""))
        first = False
    if "path" in print_data:
        if not first:
            out += printf_b(print_delim)[0]
        if "/./" in entry_path:
            # xte:1403-1406 collapse the find operand delimiter
            entry_path = (entry_path.split("/./", 1)[0] + "/"
                          + entry_path.rsplit("/./", 1)[1])
        out += encode(entry_path + (":" + entry_action if entry_action else ""))
        first = False
    if "content" in print_data:
        if not first:
            out += printf_b(print_delim)[0]
        try:
            for ln in read_file_lines(entry_path):
                out += encode(ln) + b"\n"
        except ShellFatal as exc:
            stderr.write("%s: %s\n" % (TARGET, exc))
            return 1, bytes(out), {"fatal": str(exc), "resolver": r}
        first = False

    # xte:1449-1466 early bail out in some print modes
    if print_data:
        if "cmd" not in print_data:
            if "content" in print_data:
                return 0, bytes(out), {"selected": found, "resolver": r}
            if print_delim == "\\n":
                out += b"\n"
            return 0, bytes(out), {"selected": found, "resolver": r}

    # -- xte:1468-1523 option prepend ----------------------------------
    args = rest
    if args and st["execarg"] != "":
        args = [st["execarg"]] + args
    if st["holdarg"] != "" and hold:
        args = [st["holdarg"]] + args
    if st["dirarg"] != "" and dirval != "":
        if st["dirarg"].endswith("="):
            args = [st["dirarg"] + dirval] + args
        else:
            args = [st["dirarg"], dirval] + args
    if st["titlearg"] != "" and titleval != "":
        if st["titlearg"].endswith("="):
            args = [st["titlearg"] + titleval] + args
        else:
            args = [st["titlearg"], titleval] + args
    if st["appidarg"] != "" and appidval != "":
        if st["appidarg"].endswith("="):
            args = [st["appidarg"] + appidval] + args
        else:
            args = [st["appidarg"], appidval] + args
    args = ifs_split(st["exec_usep"], USEP) + args

    # -- xte:1529-1537 --test ------------------------------------------
    if test_mode:
        out += b"Command and arguments:\n"
        for a in args:
            out += encode("  >" + a + "<\n")
        return 0, bytes(out), {"selected": found, "resolver": r}

    # -- xte:1539-1560 --print-cmd -------------------------------------
    if "cmd" in print_data:
        if not first:
            out += printf_b(print_delim)[0]
        arg_first = True
        for a in args:
            if not arg_first:
                out += printf_b(print_cmd_delim if print_cmd_delim else "\\n")[0]
            arg_first = False
            out += encode(a)
        if print_cmd_delim == "\\n" or (not first and print_delim == "\\n"):
            out += b"\n"
        return 0, bytes(out), {"selected": found, "resolver": r}

    # xte:1562-1566 cd, then xte:1568 `exec "$@"`.  Refused by contract.
    return 2, bytes(out), {"would_exec": args, "selected": found, "resolver": r}


# ---------------------------------------------------------------------------
# explain
# ---------------------------------------------------------------------------

def explain(env, observed_path, stderr=None):
    if stderr is None:
        stderr = sys.stderr
    trace = []
    rc, out, info = run(env, ["--print-id", "--print-path", "--print-cmd"],
                        trace=trace, stderr=stderr)
    r = info.get("resolver")
    focus = set()
    for rec in trace:
        if rec[0] == "candidate":
            item = rec[2]
            focus.add(item.rsplit(":", 1)[0] if ":" in item else item)
        elif rec[0] == "list-entry":
            text = rec[3]
            body = text[1:] if text[:1] in "+-" else text
            focus.add(body.rsplit(":", 1)[0] if ":" in body else body)
    lines = []
    w = lines.append
    w("MADO-TERM explain: model of %s %s (cold cache)" % (TARGET, TARGET_VERSION))
    w("model: %s" % (os.path.abspath(__file__),))
    w("note: Type=, NoDisplay=, and the desktop-entry file's other keys are not")
    w("      consulted by 0.14.3; Hidden=true, Categories, TryExec, Exec,")
    w("      OnlyShowIn/NotShowIn and the TerminalArg* keys are.")
    w("")
    for rec in trace:
        kind = rec[0]
        if kind == "paths":
            configs, app_dirs, cache_file = rec[1], rec[2], rec[3]
            w("hierarchy")
            w("  XDG_CURRENT_DESKTOP=%r -> list prefix(es) %r"
              % (env.get("XDG_CURRENT_DESKTOP", ""), r.desktops))
            w("  HOME=%r" % (env.get("HOME", ""),))
            w("  PATH=%r" % (env.get("PATH", ""),))
            w("  cache modelled COLD; the real file would be %r (not read, not written)"
              % (cache_file,))
            w("  applications dirs (find operand order, lowest preference first):")
            for idx, d in enumerate(app_dirs):
                w("    [%d] %s%s" % (idx, d,
                                    "  (-type f applies)" if idx == 0 else
                                    "  (path tests only: -type f does not reach here)"))
            w("  config lists in read order (first match wins per entry ID):")
            for idx, p in enumerate(configs):
                w("    [%d] %s" % (idx, p))
        elif kind == "config":
            w("list file %s" % (rec[1],))
        elif kind == "config-absent":
            pass
        elif kind == "directive":
            path, lineno, text, ignored = rec[1], rec[2], rec[3], rec[4]
            w("  %s:%d  directive %r%s" % (path, lineno, text,
                                           "  (ignored: already configured)" if ignored else ""))
        elif kind == "directive-ignored":
            path, lineno, text, why = rec[1], rec[2], rec[3], rec[4]
            w("  %s:%d  directive %r ignored (%s)" % (path, lineno, text, why))
        elif kind == "directive-invalid":
            path, lineno, text = rec[1], rec[2], rec[3]
            w("  %s:%d  directive %r has an invalid entry ID" % (path, lineno, text))
        elif kind == "list-entry":
            path, lineno, text, what = rec[1], rec[2], rec[3], rec[4]
            w("  %s:%d  %r  -> %s" % (path, lineno, text, what))
        elif kind == "list-line-ignored":
            path, lineno, text = rec[1], rec[2], rec[3]
            w("  %s:%d  %r  -> ignored (not a list line, directive, or comment)"
              % (path, lineno, text))
        elif kind == "app-dir":
            pass
        elif kind == "register":
            # Only the IDs the walk actually reaches are named here; the full
            # applications/ inventory is deliberately NOT printed (it is the
            # user's own application list, and it is not part of the "why").
            if rec[2] in focus:
                w("  registered %r -> %s" % (rec[2], rec[1]))
        elif kind == "fallback-excluded":
            if rec[1] in focus:
                w("  entry %r is excluded from the fallback tail" % (rec[1],))
        elif kind == "entry-ids":
            w("preferred list from the xdg-terminals.list files (%d): %s"
              % (len(rec[1]), ", ".join(rec[1]) or "(empty)"))
            w("fallback tail: %d entry IDs from the applications dirs, highest"
              % (len(r.fallback),))
            w("  preference first; only the ones the walk reaches are shown below")
            w("candidates, in the order find_entry walks them:")
        elif kind == "fallback-start":
            w("  -- explicit list exhausted, fallback tail starts (show-in checks on) --")
        elif kind == "candidate":
            no, item, path, status, reason = rec[1], rec[2], rec[3], rec[4], rec[5]
            if path is None:
                w("  %d. %r  %s: %s" % (no, item, status, reason))
            else:
                w("  %d. %r  -> %s  %s%s%s" % (no, item, path, status,
                                               ": " if reason else "", reason))
        elif kind == "discard":
            path, lineno, text, reason, site = rec[1], rec[2], rec[3], rec[4], rec[5]
            w("     %s:%d  %r  rejected: %s  (%s)" % (path, lineno, text, reason, site))
        elif kind == "exec-partial":
            w("     Exec %r did not tokenise/strip cleanly: kept %r"
              % (rec[1], rec[2]))
        elif kind == "execarg-default":
            w("  TerminalArgExec default for %r: %r" % (rec[1], rec[2]))
        elif kind == "fatal":
            w("  FATAL: %s" % (rec[1],))
    if info.get("no_terminal"):
        sel = "-"
        path = "-"
        verdict = "NO_TERMINAL"
    else:
        found = info.get("selected")
        sel = found[1] + (":" + found[2] if found[2] else "")
        path = found[0]
        if "/./" in path:
            # same /./ collapse the --print-path branch applies
            path = path.split("/./", 1)[0] + "/" + path.rsplit("/./", 1)[1]
        verdict = "OK"
        if observed_path is not None:
            try:
                with open(observed_path, "rb") as f:
                    observed = f.read()
            except OSError as exc:
                sys.stderr.write("%s: cannot read --observed %s: %s\n"
                                 % ("mado-terminal.py", observed_path, exc))
                return 2
            verdict = "AGREE" if observed == out else "DIFFER"
    w("")
    w("MADO_TERM: selected=%s path=%s verdict=%s" % (sel, path, verdict))
    text = LF.join(lines) + LF
    sys.stdout.buffer.write(encode(text))
    sys.stdout.buffer.flush()
    if verdict == "DIFFER":
        return 1
    if verdict == "NO_TERMINAL":
        return 3
    return 0


# ---------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------

# Expectations below were produced by running the REAL pinned script
# (/usr/bin/xdg-terminal-exec, sha256 89f2be9a...3127ac) on the same
# materialised cases (harness receipts/agree.txt, generated 2026-10-26).
# They are never typed by hand.  `env` overrides the base fixture env; a None
# value means the variable is unset for that case.
_SELFTEST_BASE_ENV = {
    "XDG_CURRENT_DESKTOP": "Hyprland",
    "XDG_CONFIG_HOME": "$ROOT/home/.config",
    "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
    "XDG_DATA_HOME": "$ROOT/home/.local/share",
    "XDG_DATA_DIRS": "$ROOT/usr/share",
}

_A = "home/.local/share/applications/"
_S = "usr/share/applications/"
_L = "usr/local/share/applications/"
_C = "home/.config/"
_P = ["--print-id", "--print-path", "--print-cmd"]


def _te(name="A", exe="sh"):
    """The ordinary terminal entry used by most selftest cases."""
    return ("[Desktop Entry]\nType=Application\nName=%s\nExec=%s\n"
            "Categories=System;TerminalEmulator;\nX-TerminalArgExec=-e\n" % (name, exe))


SELFTEST_CASES = [
    # --- list hierarchy -----------------------------------------------------
    dict(id="02-fallback", files={_A + "zzz.desktop": _te("Z", "sh")},
         execs=["bin/sh"], args=_P, rc=0,
         stdout="zzz.desktop\n$ROOT/home/.local/share/applications/zzz.desktop\nsh\n"),
    dict(id="03-prefixed-beats-plain",
         files={_C + "hyprland-xdg-terminals.list": "bbb.desktop\n",
                _C + "xdg-terminals.list": "aaa.desktop\n",
                _A + "aaa.desktop": _te("A", "sh"),
                _A + "bbb.desktop": _te("B", "alacritty")},
         execs=["bin/sh", "bin/alacritty"], args=_P, rc=0,
         stdout="bbb.desktop\n$ROOT/home/.local/share/applications/bbb.desktop\nalacritty\n"),
    dict(id="04-confighome-beats-dirs",
         files={"etc/xdg/xdg-terminals.list": "bbb.desktop\n",
                _C + "xdg-terminals.list": "aaa.desktop\n",
                _A + "aaa.desktop": _te("A", "sh"),
                _A + "bbb.desktop": _te("B", "alacritty")},
         execs=["bin/sh", "bin/alacritty"], args=_P, rc=0,
         stdout="aaa.desktop\n$ROOT/home/.local/share/applications/aaa.desktop\nsh\n"),
    dict(id="05-datadir-list",
         files={_A + "aaa.desktop": _te("A", "sh"),
                _A + "bbb.desktop": _te("B", "alacritty"),
                "usr/share/xdg-terminal-exec/xdg-terminals.list": "bbb.desktop\n"},
         execs=["bin/sh", "bin/alacritty"], args=_P, rc=0,
         stdout="bbb.desktop\n$ROOT/home/.local/share/applications/bbb.desktop\nalacritty\n"),
    dict(id="06-duplicate-user-wins",
         files={_A + "dup.desktop": _te("U", "alacritty"),
                _S + "dup.desktop": _te("S", "sh")},
         execs=["bin/sh", "bin/alacritty"], args=_P, rc=0,
         stdout="dup.desktop\n$ROOT/home/.local/share/applications/dup.desktop\nalacritty\n"),
    dict(id="d01-three-datadirs",
         env={"XDG_DATA_DIRS": "$ROOT/usr/share:$ROOT/usr/local/share"},
         files={_C + "xdg-terminals.list": "ss.desktop\n",
                _A + "hh.desktop": _te("H", "sh"),
                _L + "ll.desktop": _te("L", "alacritty"),
                _S + "ss.desktop": _te("S", "alacritty")},
         execs=["bin/sh", "bin/alacritty"], args=_P, rc=0,
         stdout="ss.desktop\n$ROOT/usr/share/applications/ss.desktop\nalacritty\n"),
    dict(id="23-no-desktop", env={"XDG_CURRENT_DESKTOP": ""},
         files={_C + "hyprland-xdg-terminals.list": "aaa.desktop\n",
                _A + "aaa.desktop": _te("A", "sh"),
                _A + "bbb.desktop": _te("B", "alacritty")},
         execs=["bin/sh", "bin/alacritty"], args=_P, rc=0,
         stdout="bbb.desktop\n$ROOT/home/.local/share/applications/bbb.desktop\nalacritty\n"),
    # --- list line syntax ---------------------------------------------------
    dict(id="28-list-noise",
         files={_C + "xdg-terminals.list":
                "# comment\n\n   \nnot an id.x\nfoo\n/unknown/directive\naaa.desktop\n:bad\n",
                _A + "aaa.desktop": _te("A", "sh")},
         execs=["bin/sh"], args=_P, rc=0,
         stdout="aaa.desktop\n$ROOT/home/.local/share/applications/aaa.desktop\nsh\n"),
    dict(id="29-misspelled",
         files={_C + "xdg-terminals.list": "bad name.desktop\n",
                _A + "aaa.desktop": _te("A", "sh")},
         execs=["bin/sh"], args=_P, rc=0,
         stdout="aaa.desktop\n$ROOT/home/.local/share/applications/aaa.desktop\nsh\n"),
    dict(id="30-subdir-id",
         files={_C + "xdg-terminals.list": "sub-aaa.desktop\n",
                _A + "sub/aaa.desktop": _te("A", "sh")},
         execs=["bin/sh"], args=_P, rc=0,
         stdout="sub-aaa.desktop\n$ROOT/home/.local/share/applications/sub/aaa.desktop\nsh\n"),
    dict(id="31-invalid-chars",
         files={_A + "bad name.desktop": _te("B", "sh"),
                _A + "good.desktop": _te("G", "alacritty")},
         execs=["bin/sh", "bin/alacritty"], args=_P, rc=0,
         stdout="good.desktop\n$ROOT/home/.local/share/applications/good.desktop\nalacritty\n"),
    dict(id="18-exclusion",
         files={_C + "xdg-terminals.list": "-excluded.desktop\nAlacritty.desktop\n",
                _A + "Alacritty.desktop": _te("A", "sh"),
                _S + "excluded.desktop": _te("E", "alacritty")},
         execs=["bin/sh", "bin/alacritty"], args=_P, rc=0,
         stdout="Alacritty.desktop\n$ROOT/home/.local/share/applications/Alacritty.desktop\nsh\n"),
    dict(id="19-exclusion-only",
         files={_C + "xdg-terminals.list": "-aaa.desktop\n",
                _A + "aaa.desktop": _te("A", "sh"),
                _A + "bbb.desktop": _te("B", "alacritty")},
         execs=["bin/sh", "bin/alacritty"], args=_P, rc=0,
         stdout="bbb.desktop\n$ROOT/home/.local/share/applications/bbb.desktop\nalacritty\n"),
    dict(id="d20-plus-only",
         files={_C + "xdg-terminals.list": "+\n",
                _A + "ok.desktop": _te("O", "sh")},
         execs=["bin/sh"], args=_P, rc=0,
         stdout="ok.desktop\n$ROOT/home/.local/share/applications/ok.desktop\nsh\n"),
    dict(id="d21-system-exclusion-host-shape",
         files={_C + "xdg-terminals.list": "aaa.desktop\n",
                _A + "aaa.desktop": "[Desktop Entry]\nExec=sh\nCategories=TerminalEmulator;\n",
                _S + "foot.desktop": _te("F", "alacritty"),
                "usr/share/xdg-terminal-exec/xdg-terminals.list":
                    "-foot.desktop\n-footclient.desktop\n"
                    "/execarg_default:aaa.desktop:--\n"},
         execs=["bin/sh", "bin/alacritty"],
         args=["--print-id", "--print-cmd", "echo", "x"], rc=0,
         stdout="aaa.desktop\nsh\n--\necho\nx\n"),
    # --- entry validation ---------------------------------------------------
    dict(id="07-hidden-true",
         files={_A + "hid.desktop":
                "[Desktop Entry]\nType=Application\nName=H\nExec=sh\nHidden=true\n"
                "Categories=System;TerminalEmulator;\nX-TerminalArgExec=-e\n",
                _A + "ok.desktop": _te("O", "alacritty")},
         execs=["bin/sh", "bin/alacritty"], args=_P, rc=0,
         stdout="ok.desktop\n$ROOT/home/.local/share/applications/ok.desktop\nalacritty\n"),
    dict(id="08-hidden-capital",
         files={_A + "hid.desktop":
                "[Desktop Entry]\nType=Application\nName=H\nExec=sh\nHidden=True\n"
                "Categories=System;TerminalEmulator;\nX-TerminalArgExec=-e\n"},
         execs=["bin/sh"], args=_P, rc=0,
         stdout="hid.desktop\n$ROOT/home/.local/share/applications/hid.desktop\nsh\n"),
    dict(id="d26-hidden-false",
         files={_A + "a.desktop":
                "[Desktop Entry]\nType=Application\nName=A\nExec=sh\nHidden=false\n"
                "Categories=System;TerminalEmulator;\nX-TerminalArgExec=-e\n"},
         execs=["bin/sh"], args=_P, rc=0,
         stdout="a.desktop\n$ROOT/home/.local/share/applications/a.desktop\nsh\n"),
    dict(id="09-no-categories",
         files={_A + "nocat.desktop": "[Desktop Entry]\nType=Application\nExec=sh\n",
                _A + "ok.desktop": _te("O", "alacritty")},
         execs=["bin/sh", "bin/alacritty"], args=_P, rc=0,
         stdout="ok.desktop\n$ROOT/home/.local/share/applications/ok.desktop\nalacritty\n"),
    dict(id="10-wrong-category",
         files={_A + "nocat.desktop":
                "[Desktop Entry]\nType=Application\nName=N\nExec=sh\n"
                "Categories=System;Utility;\nX-TerminalArgExec=-e\n",
                _A + "ok.desktop": _te("O", "alacritty")},
         execs=["bin/sh", "bin/alacritty"], args=_P, rc=0,
         stdout="ok.desktop\n$ROOT/home/.local/share/applications/ok.desktop\nalacritty\n"),
    dict(id="20-nodisplay-type",
         files={_A + "a.desktop":
                "[Desktop Entry]\nType=Link\nNoDisplay=true\nName=A\nExec=sh\n"
                "Categories=System;TerminalEmulator;\nX-TerminalArgExec=-e\n"},
         execs=["bin/sh"], args=_P, rc=0,
         stdout="a.desktop\n$ROOT/home/.local/share/applications/a.desktop\nsh\n"),
    dict(id="11-tryexec-missing",
         files={_A + "te.desktop":
                "[Desktop Entry]\nType=Application\nName=T\nExec=alacritty\n"
                "TryExec=nothere\nCategories=System;TerminalEmulator;\n"
                "X-TerminalArgExec=-e\n"},
         execs=["bin/alacritty"], args=_P, rc=1, stdout=""),
    dict(id="12-exec-not-on-path",
         files={_A + "x.desktop":
                "[Desktop Entry]\nType=Application\nName=X\nExec=ghost\n"
                "Categories=System;TerminalEmulator;\nX-TerminalArgExec=-e\n"},
         execs=["bin/alacritty"], args=_P, rc=1, stdout=""),
    dict(id="21-onlyshowin",
         files={_C + "xdg-terminals.list": "listed.desktop\n",
                _A + "listed.desktop":
                    "[Desktop Entry]\nType=Application\nName=L\nExec=sh\n"
                    "OnlyShowIn=GNOME;\nCategories=System;TerminalEmulator;\n"
                    "X-TerminalArgExec=-e\n",
                _S + "gnome.desktop":
                    "[Desktop Entry]\nType=Application\nName=G\nExec=alacritty\n"
                    "OnlyShowIn=GNOME;\nCategories=System;TerminalEmulator;\n"
                    "X-TerminalArgExec=-e\n"},
         execs=["bin/sh", "bin/alacritty"], args=_P, rc=0,
         stdout="listed.desktop\n$ROOT/home/.local/share/applications/listed.desktop\nsh\n"),
    dict(id="22-notshowin",
         files={_A + "a.desktop":
                "[Desktop Entry]\nType=Application\nName=A\nExec=sh\n"
                "NotShowIn=Hyprland;\nCategories=System;TerminalEmulator;\n"
                "X-TerminalArgExec=-e\n",
                _A + "b.desktop": _te("B", "alacritty")},
         execs=["bin/sh", "bin/alacritty"], args=_P, rc=0,
         stdout="b.desktop\n$ROOT/home/.local/share/applications/b.desktop\nalacritty\n"),
    dict(id="44-none",
         files={_A + "a.desktop": "[Desktop Entry]\nExec=sh\n"},
         execs=["bin/sh"], args=_P, rc=1, stdout=""),
    dict(id="d11-no-trailing-newline",
         files={_A + "a.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\nExec=sh"},
         execs=["bin/sh"], args=_P, rc=1, stdout=""),
    # --- Exec parsing and field codes --------------------------------------
    dict(id="13-exec-fields",
         files={_A + "f.desktop":
                "[Desktop Entry]\nType=Application\n"
                "Exec=\"sh\" -c \"echo hi\" %i %c %%f\nCategories=TerminalEmulator;\n"},
         execs=["bin/sh"], args=_P, rc=0,
         stdout="f.desktop\n$ROOT/home/.local/share/applications/f.desktop\n"
                "sh\n-c\necho hi\n%f\n"),
    dict(id="14-two-file-fields",
         files={_A + "a.desktop":
                "[Desktop Entry]\nExec=sh %f %u\nCategories=TerminalEmulator;\n",
                _A + "b.desktop": _te("B", "alacritty")},
         execs=["bin/sh", "bin/alacritty"], args=_P, rc=0,
         stdout="b.desktop\n$ROOT/home/.local/share/applications/b.desktop\nalacritty\n"),
    dict(id="15-unknown-field",
         files={_A + "a.desktop":
                "[Desktop Entry]\nExec=sh %z\nCategories=TerminalEmulator;\n"},
         execs=["bin/sh"], args=_P, rc=0,
         stdout="a.desktop\n$ROOT/home/.local/share/applications/a.desktop\nsh\n%z\n"),
    dict(id="52-exec-bad-quote",
         files={_A + "a.desktop":
                "[Desktop Entry]\nExec=sh | cat\nCategories=TerminalEmulator;\n"},
         execs=["bin/sh"], args=_P, rc=0,
         stdout="a.desktop\n$ROOT/home/.local/share/applications/a.desktop\nsh\n"),
    dict(id="d16-literal-percent-file",
         files={_A + "a.desktop":
                "[Desktop Entry]\nExec=sh %%f\nCategories=TerminalEmulator;\n"},
         execs=["bin/sh"], args=_P, rc=0,
         stdout="a.desktop\n$ROOT/home/.local/share/applications/a.desktop\nsh\n%f\n"),
    # --- actions -----------------------------------------------------------
    dict(id="16-action",
         files={_C + "xdg-terminals.list": "aaa.desktop:New\n",
                _A + "aaa.desktop":
                    "[Desktop Entry]\nExec=sh\nCategories=TerminalEmulator;\n"
                    "Actions=New;\n\n[Desktop Action New]\nExec=sh\n-c\necho hi\n"},
         execs=["bin/sh"], args=_P, rc=0,
         stdout="aaa.desktop:New\n"
                "$ROOT/home/.local/share/applications/aaa.desktop:New\nsh\n"),
    dict(id="17-action-unlisted",
         files={_C + "xdg-terminals.list": "aaa.desktop:Ghost\n",
                _A + "aaa.desktop":
                    "[Desktop Entry]\nExec=sh\nCategories=TerminalEmulator;\n"
                    "Actions=New;\n\n[Desktop Action Ghost]\nExec=sh\n",
                _A + "zzz.desktop": _te("Z", "alacritty")},
         execs=["bin/sh", "bin/alacritty"], args=_P, rc=0,
         stdout="zzz.desktop\n$ROOT/home/.local/share/applications/zzz.desktop\nalacritty\n"),
    # --- TerminalArgExec / directives / residue ----------------------------
    dict(id="45-default-execarg",
         files={_A + "a.desktop":
                "[Desktop Entry]\nExec=sh\nCategories=TerminalEmulator;\n"},
         execs=["bin/sh"], args=_P, rc=0,
         stdout="a.desktop\n$ROOT/home/.local/share/applications/a.desktop\nsh\n"),
    dict(id="46-execarg-default",
         files={_C + "xdg-terminals.list":
                "/execarg_default:aaa.desktop:--\naaa.desktop\n",
                _A + "aaa.desktop":
                    "[Desktop Entry]\nExec=sh\nCategories=TerminalEmulator;\n"},
         execs=["bin/sh"], args=["--print-cmd", "echo", "hi"], rc=0,
         stdout="sh\n--\necho\nhi\n"),
    dict(id="47-directives",
         files={_C + "xdg-terminals.list":
                "/execarg_strict\n/disable_cache\n/execarg_compat\naaa.desktop\n",
                _A + "aaa.desktop":
                    "[Desktop Entry]\nExec=sh\nCategories=TerminalEmulator;\n"},
         execs=["bin/sh"], args=["--print-cmd", "echo"], rc=1, stdout=""),
    dict(id="48-residue",
         files={_A + "aaa.desktop":
                "[Desktop Entry]\nCategories=TerminalEmulator;\n",
                _A + "bbb.desktop": "[Desktop Entry]\nExec=alacritty\n"},
         execs=["bin/alacritty"], args=_P, rc=0,
         stdout="aaa.desktop\n$ROOT/home/.local/share/applications/aaa.desktop\nalacritty\n"),
    dict(id="49-dir-entry",
         files={_A + "ok.desktop": _te("O", "sh"),
                _S + "dir.desktop/keep": ""},
         execs=["bin/sh"], args=_P, rc=0,
         stdout="ok.desktop\n$ROOT/home/.local/share/applications/ok.desktop\nsh\n"),
    # --- print modes -------------------------------------------------------
    dict(id="32-print-id-only", files={_A + "a.desktop": _te("A", "sh")},
         execs=["bin/sh"], args=["--print-id"], rc=0, stdout="a.desktop\n"),
    dict(id="33-print-path-only", files={_A + "a.desktop": _te("A", "sh")},
         execs=["bin/sh"], args=["--print-path"], rc=0,
         stdout="$ROOT/home/.local/share/applications/a.desktop\n"),
    dict(id="35-print-delim", files={_A + "a.desktop": _te("A", "sh")},
         execs=["bin/sh"], args=["--print-id", "--print-path", "--print-delimiter=|"],
         rc=0, stdout="a.desktop|$ROOT/home/.local/share/applications/a.desktop"),
    dict(id="36-print-cmd-empty-delim", files={_A + "a.desktop": _te("A", "sh")},
         execs=["bin/sh"],
         args=["--print-cmd=", "--print-delimiter=|", "--print-id"], rc=0,
         stdout="a.desktop|sh"),
    dict(id="d06-delims", files={_A + "a.desktop": _te("A", "sh")},
         execs=["bin/sh"],
         args=["--print-id", "--print-path", "--print-cmd=\\t",
               "--print-delimiter=\\\\"], rc=0,
         stdout="a.desktop\\$ROOT/home/.local/share/applications/a.desktop\\sh"),
    dict(id="38-prepend-all",
         files={_A + "a.desktop":
                "[Desktop Entry]\nExec=sh\nCategories=TerminalEmulator;\n"
                "X-TerminalArgExec=-e\nX-TerminalArgAppId=--class=\n"
                "X-TerminalArgTitle=--title=\nX-TerminalArgDir=--cd=\n"
                "X-TerminalArgHold=--hold\n"},
         execs=["bin/sh"],
         args=["--print-cmd", "--app-id=com.x", "--title=T y", "--dir=/tmp", "--hold"],
         rc=0, stdout="sh\n--class=com.x\n--title=T y\n--cd=/tmp\n--hold\n"),
    dict(id="40-execarg-escape",
         files={_A + "a.desktop":
                "[Desktop Entry]\nExec=sh\nCategories=TerminalEmulator;\n"
                "X-TerminalArgExec=--opt=\\s\\t\n"},
         execs=["bin/sh"], args=["--print-cmd", "echo", "hi"], rc=0,
         stdout="sh\n--opt= \t\necho\nhi\n"),
    dict(id="d29-empty-execarg",
         files={_A + "a.desktop":
                "[Desktop Entry]\nExec=sh\nCategories=TerminalEmulator;\n"
                "X-TerminalArgExec=\n"},
         execs=["bin/sh"], args=["--print-cmd", "echo", "hi"], rc=0,
         stdout="sh\necho\nhi\n"),
    dict(id="41-print-content", files={_A + "a.desktop": _te("A", "sh")},
         execs=["bin/sh"], args=["--print-id", "--print-content"], rc=0,
         stdout="a.desktop\n" + _te("A", "sh")),
    dict(id="d19-content-dir",
         files={_A + "ok.desktop": _te("O", "sh"), _S + "dir.desktop/keep": ""},
         execs=["bin/sh"], args=["--print-content"], rc=0, stdout=_te("O", "sh")),
    dict(id="42-test-mode", files={_A + "a.desktop": _te("A", "sh")},
         execs=["bin/sh"], args=["--test"], rc=0,
         stdout="Command and arguments:\n  >sh<\n"),
    dict(id="60-dashdash", files={_A + "a.desktop": _te("A", "sh")},
         execs=["bin/sh"], args=["--print-cmd", "--", "--print-id"], rc=0,
         stdout="sh\n-e\n--print-id\n"),
]


def _materialize(case, root):
    os.makedirs(os.path.join(root, "bin"), exist_ok=True)
    os.makedirs(os.path.join(root, "home"), exist_ok=True)
    os.makedirs(os.path.join(root, "cache"), exist_ok=True)
    os.makedirs(os.path.join(root, "toolbin"), exist_ok=True)
    for rel, text in case["files"].items():
        p = os.path.join(root, rel)
        d = os.path.dirname(p)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(text)
    for rel in case.get("execs", []):
        p = os.path.join(root, rel)
        d = os.path.dirname(p)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write("#!/bin/sh\nexit 0\n")
        os.chmod(p, 0o755)


def _case_env(case, root):
    env = {
        "HOME": root + "/home",
        "PATH": root + "/bin:" + root + "/toolbin",
        "XDG_CACHE_HOME": root + "/cache",
    }
    for k, v in _SELFTEST_BASE_ENV.items():
        env[k] = v.replace("$ROOT", root)
    for k, v in case.get("env", {}).items():
        if v is None:
            env.pop(k, None)
        else:
            env[k] = v.replace("$ROOT", root)
    return env


def selftest():
    import io
    import shutil
    import tempfile

    base = tempfile.mkdtemp(prefix="mado-terminal-selftest-")
    passed = 0
    total = 0
    failures = []
    try:
        # --help is checked separately: its expected stdout is HELP_TEXT itself.
        total += 1
        rc, out, _info = run({}, ["--help"], stderr=io.StringIO())
        if rc == 0 and out == encode(HELP_TEXT):
            passed += 1
        else:
            failures.append(("help", rc, 0, out, encode(HELP_TEXT)))
        for case in SELFTEST_CASES:
            root = os.path.join(base, case["id"])
            _materialize(case, root)
            env = _case_env(case, root)
            total += 1
            rc, out, _info = run(env, case["args"], stderr=io.StringIO())
            want_rc = case["rc"]
            want_out = encode(case["stdout"].replace("$ROOT", root))
            if rc == want_rc and out == want_out:
                passed += 1
            else:
                failures.append((case["id"], rc, want_rc, out, want_out))
    finally:
        shutil.rmtree(base, ignore_errors=True)
    for cid, rc, want_rc, out, want_out in failures:
        sys.stderr.write("FAIL %s: rc=%r want %r\n  got  %r\n  want %r\n"
                         % (cid, rc, want_rc, out, want_out))
    sys.stdout.write("MADO_TERMINAL_SELFTEST: %d/%d passed\n" % (passed, total))
    return 0 if not failures else 1


# ---------------------------------------------------------------------------
# entry point
# ---------------------------------------------------------------------------

def main(argv):
    if not argv:
        sys.stderr.write(USAGE)
        return 2
    cmd = argv[0]
    if cmd == "--selftest":
        return selftest()
    if cmd == "print":
        rc, out, _info = run(dict(os.environ), argv[1:])
        sys.stdout.buffer.write(out)
        sys.stdout.buffer.flush()
        return rc
    if cmd == "explain":
        observed = None
        args = argv[1:]
        i = 0
        while i < len(args):
            a = args[i]
            if a == "--observed":
                if i + 1 >= len(args):
                    sys.stderr.write(USAGE)
                    return 2
                observed = args[i + 1]
                i += 2
                continue
            if a.startswith("--observed="):
                observed = a.split("=", 1)[1]
                i += 1
                continue
            sys.stderr.write(USAGE)
            return 2
        return explain(dict(os.environ), observed)
    sys.stderr.write(USAGE)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

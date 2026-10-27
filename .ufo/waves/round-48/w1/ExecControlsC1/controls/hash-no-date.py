#!/usr/bin/env python3
"""CONTROL hash-no-date - ls -l model without the date column. See .ufo/waves/round-48/w1/ExecControlsC1.md (clause: f (any warm fixture)).
mado-terminal.py - which terminal does `xdg-terminal-exec` (SUPER+RETURN on this host) pick, and why.

Read-only. Starts no process, opens no socket, writes no file. Python 3 standard library only.

The resolver modelled is xdg-terminal-exec v0.14.3 (upstream tag v0.14.3, script sha256
89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac = the host's /usr/bin/xdg-terminal-exec). Line
numbers below ("x:N") are lines of that script.

Usage
-----
  mado-terminal.py print [xdg-terminal-exec options] [--] [command [args ...]]
      Prints exactly what `xdg-terminal-exec` prints on stdout for the same options and arguments in the same
      environment, and exits with its exit status, for the cache state the environment presents ("Cache"
      below). At least one of
      --print-id, --print-path, --print-content, --print-cmd[=SEQ] or --test is required (without one the resolver
      would launch a terminal; this tool refuses with exit 2).
  mado-terminal.py explain [--observed FILE]
      A trace of the selection (every list file read, every candidate and why it was skipped), then one line
          MADO_TERM: selected=<id|-> path=<path|-> cmd=<exec[0]|-> cache=<absent|hit|stale|invalid|disabled> verdict=<V>
      selected= and path= are what --print-id and --print-path print (an action rides on both as `:<action>`).
      V is OK (a terminal is selected), NO_TERMINAL (none is), and with --observed FILE - the captured stdout of
      `XDG_CACHE_HOME=$(mktemp -d) xdg-terminal-exec --print-id --print-path --print-cmd` - AGREE when the three
      printed items equal this tool's (id, path, and command line), DIFFER otherwise.
      Exit: 0 OK/AGREE, 1 DIFFER, 3 NO_TERMINAL, 2 usage error.
  mado-terminal.py --selftest
      Hermetic cases built under $TMPDIR; last line `MADO_TERMINAL_SELFTEST: N/N passed`; exit 0 iff all pass.

Environment read (as the resolver reads it): HOME, PATH, XDG_CURRENT_DESKTOP, XDG_CONFIG_HOME, XDG_CONFIG_DIRS,
XDG_DATA_HOME, XDG_DATA_DIRS, XDG_CACHE_HOME, XTE_EXECARG_COMPAT, XTE_CACHE_ENABLED.

The selection (contract)
------------------------
 1. Desktop names: XDG_CURRENT_DESKTOP with ASCII upper case lowered (`tr`, x:1144; trailing newlines dropped by the
    command substitution), split on ':' (shell field splitting: empty fields kept, a trailing empty one dropped).
 2. List files, in order (x:143-163): for each dir of XDG_CONFIG_HOME (default $HOME/.config) then XDG_CONFIG_DIRS
    (default /etc/xdg) - both joined with ':' and split on ':' - first `<dir>/<desktop>-xdg-terminals.list` for each
    desktop name, then `<dir>/xdg-terminals.list`; then the same for `<dir>/xdg-terminal-exec/` under each dir of
    XDG_DATA_DIRS (default /usr/local/share:/usr/share). One trailing '/' of a dir is removed.
 3. List lines (x:351-475): a file that is not a regular file is skipped; an unreadable one ends the resolver with
    exit 1 (errexit). Lines are read like `read -r` (leading/trailing space, tab and newline removed, NUL bytes
    dropped, a last line without a newline ignored). Directives /enable_cache, /disable_cache, /execarg_compat,
    /execarg_strict (first one of each pair wins; XTE_EXECARG_COMPAT / XTE_CACHE_ENABLED set in the environment win
    over any directive), /execarg_default:<id>:<arg> (compat mode only; first default per id wins). An entry line
    starts with [a-zA-Z0-9_] (or + or - followed by one): split at the first ':' into id and action with bash `read`
    rules; the id must match [a-zA-Z0-9_.-]+ ending in `.desktop` and not be `.desktop`, the action [a-zA-Z0-9-]* -
    else "Discarded possibly misspelled entry" (stderr). '+id' protects id from a later '-id', '-id' removes it from
    the fallback list; first word wins. Plain lines are kept verbatim (after the +/- strip) in list order,
    duplicates included. Anything else is ignored.
 4. Desktop entries (x:754-800): `find -L <dir>/. -type f` over the application dirs in ascending preference (the
    last of XDG_DATA_DIRS first, XDG_DATA_HOME (default $HOME/.local/share) last), directory entries in readdir
    order; a path counts when its part after `<dir>/./` starts with [a-zA-Z0-9_], ends in `.desktop` and holds only
    [a-zA-Z0-9_./-]; its id is that part with '/' -> '-'. The last path seen for an id wins (so XDG_DATA_HOME beats
    XDG_DATA_DIRS); every path seen whose id is not '-'-excluded is put at the FRONT of the fallback list.
 5. Candidates (x:1055-1111): the list lines, then the fallback ids. An `id:action` line splits at the first ':' for
    the action and the last ':' for the id. An id with no path, or already tried, is skipped. The entry file is read
    line by line (x:970-1018) with the same `read` rules: `[Desktop Entry]...` allows Exec when no action is asked;
    `[Desktop Action <a>]...` allows it when the Actions key listed <a> (else the entry is rejected); any other
    `[` line ends reading once Exec was allowed. Every line starting with [a-zA-Z0-9-] is a key line, checked in
    this order against its WHOLE text (so `CategoriesX=` counts as Categories), value = text after the first '='
    with leading spaces removed (x:802-968): Categories must hold `TerminalEmulator` between ';' (else reject);
    Actions must list the asked action; OnlyShowIn/NotShowIn are checked against the ':'-split XDG_CURRENT_DESKTOP
    (case-sensitive) for fallback ids only; X-TerminalArgExec/TerminalArgExec, X-ExecArg/ExecArg (compat mode
    only), and the X-/TerminalArgAppId, Title, Dir, Hold keys set the argument (escapes \\s \\n \\t \\r \\\\
    expanded, any other backslash dropped); TryExec must be found by `command -v` (reject otherwise); Hidden=true
    rejects; Exec (when allowed) is escape-expanded, tokenized by the shell-quoting rules of x:561-692, its field
    codes stripped (x:694-740), and its first word must be found by `command -v` (reject otherwise). A read that
    ends while the last executed step failed also rejects (POSIX while-loop status). Rejection by a key resets the
    collected keys; an entry that is read but lacks an Exec word or the TerminalEmulator category is skipped WITHOUT
    resetting them, so a later entry inherits them. An entry without a TerminalArgExec gets the /execarg_default
    for its id or `-e` in compat mode (default) and is skipped in strict mode. The first candidate left wins.
    `command -v` succeeds for a name that bash parses as its own options (`--`, `-p`, `-v`, `-V` and clusters of
    them) and fails for any other name starting with '-' except `-`; it finds aliases (ids registered in step 4 and not yet tried), the script's own functions, bash
    builtins and reserved words, a path containing '/' that is an executable non-directory, or the first executable
    non-directory file of that name in a PATH dir (an empty PATH entry is the working directory).
 6. No candidate: "No valid terminal entry was found in: ..." on stderr, exit 1, nothing on stdout.
 7. Options (x:1224-1322), then printing (x:1325-1491) exactly as the script: --print-id prints `id[:action]`,
    --print-path the path with `/./` folded, --print-content the entry's lines, --print-cmd the Exec words, then
    --app-id/--title/--dir/--hold arguments where the entry defines them, then the exec argument and the command
    when one is given; --print-delimiter / --print-cmd= values pass through bash `printf %b`; --test prints
    "Command and arguments:" and one `  >arg<` line per word.

Cache: the resolver reads $XDG_CACHE_HOME/xdg-terminal-exec (default $HOME/.cache) BEFORE any list or entry
(x:1179) and uses its entry, arguments and command while an md5 of XDG_CURRENT_DESKTOP and `ls -LRl` of every list
and application path is unchanged and the cached command resolves (x:217-298); a cold run that reaches the print-cmd
or launch point rewrites it in the background (x:1455-1458). This tool models that cache as the environment presents
it - hit, stale, invalid (no terminator, line limit) or disabled (XTE_CACHE_ENABLED=false; a /disable_cache line in a
list file only suppresses the save, never the read) - and prints
what the resolver prints in each case; it never writes the cache the resolver would save. Also out of contract:
-h/--help, a FIFO named like a desktop file in a
later application dir (the script blocks reading it), symlink loops, an empty-string argument (the script loops forever), XDG dirs or HOME containing ':' inside a default, glob characters or a quote,
\\u/\\U escapes beyond ASCII in a delimiter, and file names with bytes the shell would see differently in another
locale. On these the tool prints `MADO_TERM_OUT_OF_CONTRACT: <reason>` on stderr and exits 2.
"""
import fnmatch
import hashlib
import os
import stat
import sys
import tempfile
import time

USEP = "\x1f"
SPACE = " \t\n\v\f\r"          # [[:space:]] in the C locale
READ_WS = " \t\n"              # default IFS whitespace stripped by `read`
TOK_SPECIAL = SPACE + "\"`$\\'><~|&;*?#()"

BASH_BUILTINS = set(". : [ alias bg bind break builtin caller cd command compgen complete compopt continue declare dirs "
                    "disown echo enable eval exec exit export false fc fg getopts hash help history jobs kill let local "
                    "logout mapfile popd printf pushd pwd read readarray readonly return set shift shopt source suspend "
                    "test times trap true type typeset ulimit umask unalias unset wait".split())
BASH_KEYWORDS = set("if then else elif fi case esac for select while until do done in function time { } ! [[ ]] "
                    "coproc".split())
SCRIPT_FUNCTIONS = set("error check_bool debug shcat usage help make_paths gen_hash read_cache save_cache list_contains "
                       "read_config_paths replace de_expand_str de_tokenize_exec de_strip_fields reset_keys "
                       "find_entry_paths check_entry_key read_entry_path validate_entry_id validate_action_id find_entry "
                       "get_default_execarg".split())


class OutOfContract(Exception):
    pass


class Exit(Exception):
    def __init__(self, rc):
        super().__init__(rc)
        self.rc = rc


def m(s, pat):
    return fnmatch.fnmatchcase(s, pat)


def split_ifs(s, ch):
    """Shell field splitting of an unquoted expansion with IFS = one non-whitespace character."""
    if s == "":
        return []
    parts = s.split(ch)
    if parts[-1] == "":
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
            rest = None
            break
        out.append(rest[:i])
        rest = rest[i + 1:]
    if rest is None:
        out.extend([""] * (nvars - len(out)))
        return out
    if rest.endswith(ch) and ch not in rest[:-1]:
        rest = rest[:-1]
    out.append(rest)
    return out


def read_lines(data, trim):
    """Lines a `while read -r` loop sees: NUL dropped, a last unterminated line not seen."""
    data = data.replace("\0", "")
    parts = data.split("\n")
    parts.pop()
    if trim:
        parts = [p.strip(READ_WS) for p in parts]
    return parts


def read_file(path):
    with open(path, "rb") as fh:
        return fh.read().decode("latin-1")


def printf_b(s):
    """bash `printf %b` of s; returns (text, stop) - stop is True after \\c."""
    out = []
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c != "\\" or i + 1 >= n:
            out.append(c)
            i += 1
            continue
        d = s[i + 1]
        simple = {"a": "\a", "b": "\b", "e": "\x1b", "E": "\x1b", "f": "\f", "n": "\n", "r": "\r", "t": "\t",
                  "v": "\v", "\\": "\\"}
        if d in simple:
            out.append(simple[d])
            i += 2
        elif d == "c":
            return "".join(out), True
        elif d == "0":
            j = i + 2
            k = j
            while k < n and k < j + 3 and s[k] in "01234567":
                k += 1
            out.append(chr(int(s[j:k] or "0", 8) & 0xFF))
            i = k
        elif d in "1234567":
            j = i + 1
            k = j
            while k < n and k < j + 3 and s[k] in "01234567":
                k += 1
            out.append(chr(int(s[j:k], 8) & 0xFF))
            i = k
        elif d == "x":
            j = i + 2
            k = j
            while k < n and k < j + 2 and s[k] in "0123456789abcdefABCDEF":
                k += 1
            if k == j:
                out.append("\\x")
                i += 2
            else:
                out.append(chr(int(s[j:k], 16)))
                i = k
        elif d in "uU":
            width = 4 if d == "u" else 8
            j = i + 2
            k = j
            while k < n and k < j + width and s[k] in "0123456789abcdefABCDEF":
                k += 1
            if k == j:
                out.append("\\" + d)
                i += 2
            else:
                cp = int(s[j:k], 16)
                if cp > 0x7F:
                    raise OutOfContract("non-ASCII \\u/\\U escape in a delimiter")
                out.append(chr(cp))
                i = k
        else:
            out.append("\\" + d)
            i += 2
    return "".join(out), False


def expand_str(s):
    """de_expand_str (x:501-559)."""
    out = []
    rem = s
    while rem:
        i = rem.find("\\")
        if i < 0:
            out.append(rem)
            break
        out.append(rem[:i])
        rem = rem[i + 1:]
        c = rem[:1]
        mp = {"s": " ", "n": "\n", "t": "\t", "r": "\r", "\\": "\\"}
        if c in mp and c != "":
            out.append(mp[c])
            rem = rem[1:]
    return "".join(out)


def tokenize(s):
    """de_tokenize_exec (x:561-692): returns (usep_string, ok)."""
    usep = []
    rem = s
    quoted = False
    in_space = False
    while rem:
        k = 0
        while k < len(rem) and rem[k] not in TOK_SPECIAL:
            k += 1
        left = rem[:k]
        usep.append(left)
        if k == len(rem):
            break
        ch = rem[k]
        rem = rem[k + 1:]
        if in_space:
            if left == "" and ch in SPACE:
                continue
            in_space = False
        if quoted and ch == '"':
            quoted = False
            continue
        if not quoted and ch == '"':
            quoted = True
            continue
        if not quoted and ch in "`$\\'><~|&;*?#()":
            return "".join(usep), False
        if quoted and ch in "`$":
            return "".join(usep), False
        if quoted and ch == "\\":
            if rem == "":
                return "".join(usep), False
            usep.append(rem[0])
            rem = rem[1:]
            continue
        if not quoted and ch in SPACE:
            if any(c not in SPACE for c in rem):
                usep.append(USEP)
                in_space = True
                continue
            break
        if quoted and (ch in SPACE or ch in "'><~|&;*?#()"):
            usep.append(ch)
            continue
        return "".join(usep), False
    if quoted:
        return "".join(usep), False
    return "".join(usep), True


def strip_fields(usep):
    """de_strip_fields (x:694-740): returns (new_usep, ok); on failure the input is left unchanged."""
    out = ""
    fu = False
    for arg in split_ifs(usep, USEP):
        if m(arg, "*[!%]%[dDnNvm]*") or m(arg, "%[dDnNvm]*"):
            continue
        if m(arg, "*[!%]%[fFuU]*") or m(arg, "%[fFuU]*"):
            if fu:
                return usep, False
            fu = True
            continue
        if m(arg, "*[!%]%i*") or m(arg, "%i*") or m(arg, "*[!%]%c*") or m(arg, "%c*"):
            continue
        if m(arg, "*[!%]%%*") or m(arg, "%%*"):
            arg = arg.replace("%%", "%")
            out = out + (USEP if out else "") + arg
            continue
        if m(arg, "*%?*") or m(arg, "*[!%]%"):
            return usep, False
        out = out + (USEP if out else "") + arg
    return out, True


def valid_entry_id(s):
    if s == "" or s == ".desktop":
        return False
    if any(not (c.isascii() and (c.isalnum() or c in "_.-")) for c in s):
        return False
    return s.endswith(".desktop")


def valid_action_id(s):
    return all(c.isascii() and (c.isalnum() or c == "-") for c in s)


def check_bool(v, err):
    if v in ("true", "True", "TRUE", "yes", "Yes", "YES", "1"):
        return True
    if v not in ("false", "False", "FALSE", "no", "No", "NO", "0"):
        err("Assuming '%s' means no" % v)
    return False


# ------------------------------------------------------------------------------------------------ warm cache
# The resolver reads $XDG_CACHE_HOME/xdg-terminal-exec before any list or entry (x:1179) and trusts it while
# gen_hash (x:179-215) still matches and the cached command resolves (x:285-298). gen_hash is the md5 of
#   "4\n" + XDG_CURRENT_DESKTOP + "\n" + `LC_ALL=C LANG=C ls -LRl` of the ':'-split list and data paths,
# stderr dropped, so the cache verdict needs that ls's exact stdout. The model below was calibrated against the
# binary the resolver itself calls inside the counter's allowlist root - /usr/bin/ls, GNU coreutils 9.12 (the
# counter copies `shutil.which("ls", path="/usr/bin")` to /oracle/bin; an interactive shell on this host resolves a
# different `ls`), with no /etc (numeric uid/gid) and no TZ (UTC dates): byte-ordered names, a file block whose
# columns are sized over every stat'ed operand. No process is started and no file is written.
CACHE_RSEP = "\x1e"
CACHE_TERMINATOR = CACHE_RSEP + "END_OF_EXEC_USEP"
CACHE_LINE_LIMIT = 50                     # x:222,232-235
CACHE_MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
CACHE_SIX_MONTHS = 15778476               # GNU ls's recent window: age < 15778476 s and not in the future


def _ls_mode_string(mode):
    if stat.S_ISDIR(mode):
        c = "d"
    elif stat.S_ISLNK(mode):
        c = "l"
    elif stat.S_ISFIFO(mode):
        c = "p"
    elif stat.S_ISSOCK(mode):
        c = "s"
    elif stat.S_ISCHR(mode):
        c = "c"
    elif stat.S_ISBLK(mode):
        c = "b"
    elif stat.S_ISREG(mode):
        c = "-"
    else:
        c = "?"
    out = [c]
    for bit, ch in ((0o400, "r"), (0o200, "w"), (0o100, "x"), (0o040, "r"), (0o020, "w"), (0o010, "x"),
                    (0o004, "r"), (0o002, "w"), (0o001, "x")):
        out.append(ch if mode & bit else "-")
    if mode & 0o4000:
        out[3] = "s" if mode & 0o100 else "S"
    if mode & 0o2000:
        out[6] = "s" if mode & 0o010 else "S"
    if mode & 0o1000:
        out[9] = "t" if mode & 0o001 else "T"
    return "".join(out)


def _ls_date(mtime, now):
    tm = time.gmtime(mtime)
    mon = CACHE_MONTHS[tm.tm_mon - 1]
    if 0 <= now - mtime < CACHE_SIX_MONTHS:
        return "%s %2d %02d:%02d" % (mon, tm.tm_mday, tm.tm_hour, tm.tm_min)
    return "%s %2d  %4d" % (mon, tm.tm_mday, tm.tm_year)


def _ls_text(raw):
    return raw.replace(b"\n", b"?").decode("latin-1")


class _LsRow:
    __slots__ = ("mode", "nlink", "owner", "group", "size", "date", "name", "key", "blocks", "known")

    def __init__(self, mode, nlink, owner, group, size, date, name, key, blocks, known):
        self.mode, self.nlink, self.owner, self.group = mode, nlink, owner, group
        self.size, self.date, self.name, self.key, self.blocks, self.known = size, date, name, key, blocks, known


def _ls_row(st, key, now):
    return _LsRow(_ls_mode_string(st.st_mode), str(st.st_nlink), str(st.st_uid), str(st.st_gid),
                  str(st.st_size), _ls_date(st.st_mtime, now), _ls_text(key), key, st.st_blocks, True)


def _ls_unknown(key):
    return _LsRow("l?????????", "?", "?", "?", "?", "?", _ls_text(key), key, 0, False)


def _ls_render(rows, widths=None):
    if not rows:
        return ""
    widths = rows if widths is None else widths
    w_n = max(len(r.nlink) for r in widths)
    w_o = max(len(r.owner) for r in widths)
    w_g = max(len(r.group) for r in widths)
    w_s = max(len(r.size) for r in widths)
    out = []
    for r in rows:
        if r.known:
            owner, group = r.owner.rjust(w_o), r.group.rjust(w_g)
        else:
            owner, group = r.owner.ljust(w_o), r.group.ljust(w_g)
        out.append("%s %s %s %s %s %s\n" % (r.mode, r.nlink.rjust(w_n), owner, group,
                                              r.size.rjust(w_s), r.name))
    return "".join(out)


def _ls_total(rows):
    return "%d" % ((sum(r.blocks for r in rows) + 1) // 2)


def _ls_entries(path):
    names = []
    with os.scandir(os.fsencode(path)) as it:
        for de in it:
            names.append(de.name if isinstance(de.name, bytes) else os.fsencode(de.name))
    names.sort()
    return names


def _ls_lRl(operands, now=None):
    """stdout of `ls -LRl <operands>`: gen_hash drops stderr and the exit status."""
    now = time.time() if now is None else now
    files, dirs = [], []
    for p in operands:
        try:
            st = os.stat(p)
        except OSError:
            continue                            # missing or dangling operand (-L): stderr only, no row at all
        (dirs if stat.S_ISDIR(st.st_mode) else files).append(_ls_row(st, os.fsencode(p), now))
    files.sort(key=lambda r: r.key)
    dirs.sort(key=lambda r: r.key)
    blocks = []
    if files:
        blocks.append(_ls_render(files, files + dirs))
    for d in dirs:
        blocks.extend(_ls_walk(d.key, _ls_text(d.key), 0, now))
    return "\n".join(blocks)


def _ls_walk(path, header, depth, now):
    """`path` stays bytes (a name is bytes and ls prints them back), `header` is its latin-1 text."""
    if depth > 64:
        raise OutOfContract("a symlink loop below %s (ls -LRl would run to the path limit)" % header)
    try:
        names = _ls_entries(path)
    except OSError:
        return []                               # unreadable: no header at all, stderr only
    rows, subdirs = [], []
    for nb in names:
        try:
            st = os.stat(os.path.join(path, nb))
        except OSError:
            rows.append(_ls_unknown(nb))
            continue
        rows.append(_ls_row(st, nb, now))
        if stat.S_ISDIR(st.st_mode):
            subdirs.append(nb)
    out = ["%s:\n" % header + "total %s\n" % _ls_total(rows) + _ls_render(rows)]
    for nb in subdirs:
        out.extend(_ls_walk(path.rstrip(b"/") + b"/" + nb,
                            header.rstrip("/") + "/" + _ls_text(nb), depth + 1, now))
    return out


class Resolver:
    def __init__(self, env, cwd=None):
        self.env = env
        self.cwd = cwd or os.getcwd()
        self.stderr = []
        self.trace = []

    def err(self, msg):
        self.stderr.append(msg)

    def t(self, msg):
        self.trace.append(msg)

    # ---------------------------------------------------------------- command -v
    def command_v(self, name):
        if name == "--" or (len(name) > 1 and name[0] == "-" and all(c in "pvV" for c in name[1:])):
            return True     # bash parses it as `command`'s own options and, with no operand left, exits 0
        if name == "" or (name.startswith("-") and name != "-"):
            return False    # an invalid `command` option: exit 2
        if name in self.aliases or name in SCRIPT_FUNCTIONS or name in BASH_BUILTINS or name in BASH_KEYWORDS:
            return True
        if "/" in name:
            p = name if name.startswith("/") else os.path.join(self.cwd, name)
            return self._execable(p)
        path = self.env.get("PATH")
        if path is None:
            raise OutOfContract("PATH unset")
        for d in path.split(":"):
            base = d if d else self.cwd
            if not base.startswith("/"):
                base = os.path.join(self.cwd, base)
            if self._execable(os.path.join(base, name)):
                return True
        return False

    @staticmethod
    def _execable(p):
        try:
            st = os.stat(p)
        except OSError:
            return False
        if stat.S_ISDIR(st.st_mode):
            return False
        return os.access(p, os.X_OK)

    # ---------------------------------------------------------------- steps
    def reset_keys(self):
        self.is_terminal = False
        self.exec_usep = ""
        self.execarg = "-e"
        self.execarg_defined = False
        self.appidarg = ""
        self.titlearg = ""
        self.dirarg = ""
        self.holdarg = ""

    def make_paths(self):
        e = self.env
        if "HOME" not in e:
            for k in ("XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_CACHE_HOME"):
                if not e.get(k):
                    raise Exit(1)      # `${HOME}` unbound under set -u: exit 1, no stdout (D1)
        for k in ("XDG_CONFIG_HOME", "XDG_CONFIG_DIRS", "XDG_DATA_HOME", "XDG_DATA_DIRS"):
            v = e.get(k, "")
            if any(c in v for c in "[]*?\\'\""):
                raise OutOfContract("%s holds a glob character or a quote" % k)
        home = e["HOME"]
        if any(c in home for c in ":[]*?\\'\""):
            raise OutOfContract("HOME holds ':' a glob character or a quote")
        cfg = (e.get("XDG_CONFIG_HOME") or home + "/.config") + ":" + (e.get("XDG_CONFIG_DIRS") or "/etc/xdg")
        data = e.get("XDG_DATA_DIRS") or "/usr/local/share:/usr/share"
        self.configs = []
        for d in split_ifs(cfg, ":"):
            d = d[:-1] if d.endswith("/") else d
            for dk in self.desktops_lower:
                self.configs.append(d + "/" + dk + "-xdg-terminals.list")
            self.configs.append(d + "/xdg-terminals.list")
        for d in split_ifs(data, ":"):
            d = d[:-1] if d.endswith("/") else d
            for dk in self.desktops_lower:
                self.configs.append(d + "/xdg-terminal-exec/" + dk + "-xdg-terminals.list")
            self.configs.append(d + "/xdg-terminal-exec/xdg-terminals.list")
        apps = []
        for d in split_ifs((e.get("XDG_DATA_HOME") or home + "/.local/share") + ":" + data, ":"):
            d = d[:-1] if d.endswith("/") else d
            apps.insert(0, d + "/applications/")
        self.app_dirs = apps

    def read_config_paths(self):
        for p in self.configs:
            if not os.path.isfile(p):
                continue
            try:
                text = read_file(p)
            except OSError:
                self.t("list %s: unreadable -> the resolver exits 1 (errexit)" % p)
                self.err("%s: Permission denied" % p)
                raise Exit(1)
            self.t("list %s" % p)
            for ln, line in enumerate(read_lines(text, True), 1):
                if line == "/enable_cache" or line == "/disable_cache":
                    if not self.cache_configured:
                        self.cache_enabled = "true" if line == "/enable_cache" else "false"
                        self.cache_configured = True
                    continue
                if line == "/execarg_compat" or line == "/execarg_strict":
                    if not self.compat_configured:
                        self.compat = "true" if line == "/execarg_compat" else "false"
                        self.compat_configured = True
                    continue
                if m(line, "/execarg_default:*:*"):
                    if not check_bool(self.compat, self.err):
                        continue
                    _d, eid, dflt = read_split(line, ":", 3)
                    if valid_entry_id(eid):
                        self.execarg_defaults.append((eid, dflt))
                    continue
                if m(line, "[a-zA-Z0-9_]*") or m(line, "[+-][a-zA-Z0-9_]*"):
                    excl = ""
                    if line[0] in "+-":
                        excl, line = line[0], line[1:]
                    eid, act = read_split(line, ":", 2)
                    if valid_entry_id(eid) and valid_action_id(act):
                        if excl == "":
                            self.entry_ids.append(line)
                            self.t("  %s:%d entry %s" % (p, ln, line))
                        elif excl == "+":
                            if eid not in self.excluded and eid not in self.included:
                                self.included.append(eid)
                            self.t("  %s:%d keep %s in the fallback" % (p, ln, eid))
                        else:
                            if eid not in self.included and eid not in self.excluded:
                                self.excluded.append(eid)
                            self.t("  %s:%d drop %s from the fallback" % (p, ln, eid))
                    else:
                        self.err("Discarded possibly misspelled entry '%s'" % (excl + line))
                        self.t("  %s:%d discarded %r" % (p, ln, excl + line))

    def find_entry_paths(self):
        self.aliases = {}
        self.shadowed = {}
        self.fallback = []
        found = []
        for k, d in enumerate(self.app_dirs):
            start = d + "."
            # `find -L d1/. d2/. ... -type f ( d1 ) -o ( d2 ) ...` (x:760-774): `-type f` binds to the first group
            # only, so in every later dir any path type whose name matches is registered (x:766-774, ExecC1Diff H1)
            self._walk(start, start, found, set(), k == 0)
        for path, eid in found:
            if eid in self.aliases:
                self.shadowed.setdefault(eid, []).append(self.aliases[eid])
            self.aliases[eid] = path
            if eid in self.excluded:
                continue
            self.fallback.insert(0, eid)

    def _walk(self, start, cur, found, ancestors, regular_only):
        try:
            st = os.stat(cur)
        except OSError:
            return
        if not stat.S_ISDIR(st.st_mode):
            return
        key = (st.st_dev, st.st_ino)
        if key in ancestors:
            return
        try:
            names = [de.name for de in os.scandir(cur)]
        except OSError:
            return
        ancestors = ancestors | {key}
        for name in names:
            p = cur + "/" + name
            try:
                cst = os.stat(p)
            except OSError:
                cst = None          # dangling symlink: `find -L` still visits it as a link
            if cst is not None and stat.S_ISFIFO(cst.st_mode):
                rel = p[len(start) + 1:]
                if not regular_only and self._id_ok(rel):
                    raise OutOfContract("a FIFO named like a desktop file (the resolver blocks reading it)")
            isdir = cst is not None and stat.S_ISDIR(cst.st_mode)
            rel = p[len(start) + 1:]
            if regular_only:
                if cst is not None and stat.S_ISREG(cst.st_mode) and self._id_ok(rel):
                    found.append((p, rel.replace("/", "-")))
            elif self._id_ok(rel):
                found.append((p, rel.replace("/", "-")))
            if isdir:
                self._walk(start, p, found, ancestors, regular_only)

    @staticmethod
    def _id_ok(rel):
        if not rel or not (rel[0].isascii() and (rel[0].isalnum() or rel[0] == "_")):
            return False
        if not rel.endswith(".desktop") or len(rel) < 9:
            return False
        return all(c.isascii() and (c.isalnum() or c in "_./-") for c in rel)

    def read_entry_path(self, path, action, de_checks):
        read_exec = False
        self.action_listed = False
        if os.path.isdir(path):
            return True, ""         # `read` fails on the first call: no line, loop status 0 (x:985-1017)
        try:
            text = read_file(path)
        except OSError:
            return False, "unreadable"
        status = 0
        for line in read_lines(text, True):
            if m(line, "[[]Desktop Entry[]]*"):
                if action == "":
                    read_exec = True
                    status = 0
                else:
                    status = 1
                continue
            if m(line, "[a-zA-Z0-9-]*"):
                value = line.split("=", 1)[1] if "=" in line else line
                value = value.lstrip(" ")
                ok, why = self.check_entry_key(line, value, action, read_exec, de_checks)
                if ok:
                    status = 0
                    continue
                self.reset_keys()
                return False, why
            if line.startswith("[Desktop Action %s]" % action):
                if self.action_listed:
                    read_exec = True
                    status = 0
                    continue
                return False, "action %r not listed in Actions" % action
            if line.startswith("["):
                if read_exec:
                    status = 0
                    break
                status = 1
                continue
            status = 0
        if status != 0:
            return False, "last step of the read failed (loop status 1)"
        return True, ""

    def check_entry_key(self, key, value, action, read_exec, de_checks):
        if m(key, "Categories*=*"):
            for c in split_ifs(value, ";"):
                if c == "TerminalEmulator":
                    self.is_terminal = True
                    return True, ""
            return False, "Categories lacks TerminalEmulator"
        if m(key, "Actions*=*"):
            if action == "":
                return True, ""
            for a in split_ifs(value, ";"):
                if a == action:
                    self.action_listed = True
                    return True, ""
            return False, "Actions lacks %r" % action
        desk = split_ifs(self.env.get("XDG_CURRENT_DESKTOP", ""), ":")
        if m(key, "OnlyShowIn*=*"):
            if not de_checks:
                return True, ""
            for tg in split_ifs(value, ";"):
                if tg in desk:
                    return True, ""
            return False, "OnlyShowIn excludes the desktop"
        if m(key, "NotShowIn*=*"):
            if not de_checks:
                return True, ""
            for tg in split_ifs(value, ";"):
                if tg in desk:
                    return False, "NotShowIn names the desktop"
            return True, ""
        if m(key, "X-TerminalArgExec*=*") or m(key, "TerminalArgExec*=*"):
            self.execarg = expand_str(value)
            self.execarg_defined = True
            return True, ""
        if m(key, "X-ExecArg*=*") or m(key, "ExecArg*=*"):
            if self.compat == "false":
                return True, ""
            self.execarg = expand_str(value)
            self.execarg_defined = True
            return True, ""
        for pats, attr in ((("X-TerminalArgAppId*=*", "TerminalArgAppId*=*"), "appidarg"),
                           (("X-TerminalArgTitle*=*", "TerminalArgTitle*=*"), "titlearg"),
                           (("X-TerminalArgDir*=*", "TerminalArgDir*=*"), "dirarg"),
                           (("X-TerminalArgHold*=*", "TerminalArgHold*=*"), "holdarg")):
            if m(key, pats[0]) or m(key, pats[1]):
                setattr(self, attr, expand_str(value))
                return True, ""
        if m(key, "TryExec*=*"):
            x = expand_str(value)
            if not self.command_v(x):
                return False, "TryExec %r not found" % x
            return True, ""
        if m(key, "Hidden*=*"):
            if value == "true":
                return False, "Hidden=true"
            return True, ""
        if m(key, "Exec*=*"):
            if not read_exec:
                return True, ""
            usep, _ok = tokenize(expand_str(value))
            self.exec_usep = usep
            new, ok2 = strip_fields(usep)
            if ok2:
                self.exec_usep = new
            exec0 = self.exec_usep.split(USEP, 1)[0]
            if not self.command_v(exec0):
                return False, "Exec word %r not found" % exec0
            return True, ""
        return True, ""

    def find_entry(self):
        de_checks = False
        seq = list(self.entry_ids) + ["//fallback_start//"] + list(self.fallback)
        for raw in seq:
            if ":" in raw:
                action = raw.split(":", 1)[1]
                eid = raw.rsplit(":", 1)[0]
            elif raw == "":
                continue
            elif raw == "//fallback_start//":
                de_checks = True
                continue
            else:
                eid, action = raw, ""
            if eid not in self.aliases:
                continue
            path = self.aliases.pop(eid)
            ok, why = self.read_entry_path(path, action, de_checks)
            tag = "fallback" if de_checks else "listed"
            for old in self.shadowed.get(eid, []):
                self.t("  candidate %s: %s is shadowed by %s (the later application dir wins)" % (eid, old, path))
            if not ok:
                self.t("  candidate %s (%s) %s: rejected: %s" % (eid, tag, path, why))
                continue
            if self.exec_usep == "":
                self.t("  candidate %s (%s) %s: skipped: no Exec word" % (eid, tag, path))
                continue
            if not self.is_terminal:
                self.t("  candidate %s (%s) %s: skipped: not a TerminalEmulator" % (eid, tag, path))
                continue
            if not self.execarg_defined:
                if check_bool(self.compat, self.err):
                    self.execarg = "-e"
                    for k, v in self.execarg_defaults:
                        if k == eid:
                            self.execarg = v
                            break
                else:
                    self.t("  candidate %s (%s) %s: skipped: no TerminalArgExec in strict mode" % (eid, tag, path))
                    continue
            self.t("  candidate %s (%s) %s: SELECTED" % (eid, tag, path))
            self.entry_path, self.entry_id, self.entry_action = path, eid, action
            return True
        self.err("No valid terminal entry was found in:")
        self.stderr.extend(split_ifs(":".join(self.app_dirs), ":"))
        return False


    # ---------------------------------------------------------------- cache (x:179-298)
    def gen_hash(self):
        """gen_hash (x:179-215): md5 of the version line, XDG_CURRENT_DESKTOP and `ls -LRl` of every path."""
        text = "4\n" + self.env.get("XDG_CURRENT_DESKTOP", "") + "\n"
        listing = _ls_lRl(list(self.configs) + list(self.app_dirs))
        return hashlib.md5((text + listing).encode("latin-1")).hexdigest()

    def read_cache(self):
        """read_cache (x:217-298): absent / invalid / stale / hit; a hit applies the cached fields."""
        try:
            with open(self.cache_file, "rb") as fh:
                data = fh.read().decode("latin-1")
        except OSError:
            return "absent"
        fields = [""] * 10
        exec_usep = ""
        finished = False
        for num, line in enumerate(read_lines(data, False), 1):
            if num <= 10:
                fields[num - 1] = line
                continue
            if num == CACHE_LINE_LIMIT:
                return "invalid"                # x:232-235: the limit line ends the read before any terminator
            exec_usep += ("\n" if exec_usep else "") + line
            if line.endswith(CACHE_TERMINATOR):
                exec_usep = exec_usep[:-len(CACHE_TERMINATOR)]
                finished = True
                break
        if not finished:
            return "invalid"
        if self.gen_hash() != fields[0] or not self.command_v(fields[1]):
            return "stale"                      # x:285-298: the hash, then `command -v <cached cmd>`
        self.exec_usep = exec_usep
        (self.entry_path, self.entry_id, self.entry_action, self.execarg, self.appidarg,
         self.titlearg, self.dirarg, self.holdarg) = fields[2:10]
        return "hit"

    def select(self):
        e = self.env
        dsk = e.get("XDG_CURRENT_DESKTOP", "")
        low = "".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in dsk).rstrip("\n")
        self.desktops_lower = split_ifs(low, ":")
        self.compat = e.get("XTE_EXECARG_COMPAT", "true")
        self.compat_configured = e.get("XTE_EXECARG_COMPAT", "") != ""
        self.cache_enabled = e.get("XTE_CACHE_ENABLED", "true")
        self.cache_configured = e.get("XTE_CACHE_ENABLED", "") != ""
        self.entry_ids, self.excluded, self.included, self.execarg_defaults = [], [], [], []
        self.aliases = {}
        self.reset_keys()
        self.make_paths()
        cache_home = e.get("XDG_CACHE_HOME") or (e.get("HOME", "") + "/.cache")
        self.cache_file = cache_home + "/xdg-terminal-exec"
        self.cache_used = False
        self.cache_state = "absent"     # a run that dies before the gate (HOME unset) reaches no cache
        if check_bool(self.cache_enabled, self.err):
            self.cache_state = self.read_cache()
            self.t("cache %s: %s" % (self.cache_file, self.cache_state))
            if self.cache_state == "hit":
                self.cache_used = True
                return True
        else:
            self.cache_state = "disabled"
        self.read_config_paths()
        self.find_entry_paths()
        return self.find_entry()


def run_print(env, args, cwd=None):
    """Returns (stdout_text, rc, stderr_lines). Raises OutOfContract."""
    for a in args:
        if a == "--":
            break
        if a in ("-h", "--help"):
            raise OutOfContract("-h/--help")
    r = Resolver(env, cwd)
    try:
        if not r.select():
            return "", 1, r.stderr
    except Exit as ex:
        return "", ex.rc, r.stderr
    appid = title = dirv = ""
    hold = test = False
    pdata = []
    pdelim = "\\n"
    pcdelim = "\\n"
    rest = list(args)
    while rest:
        a = rest[0]
        if a == "--":
            rest.pop(0)
            break
        if a == "-e" or a == r.execarg:
            rest.pop(0)
            break
        if a.startswith("--app-id="):
            appid = read_split(a.split("\n", 1)[0], "=", 2)[1]
        elif a.startswith("--title="):
            title = read_split(a.split("\n", 1)[0], "=", 2)[1]
        elif a.startswith("--dir="):
            dirv = read_split(a.split("\n", 1)[0], "=", 2)[1]
        elif a == "--hold":
            hold = True
        elif a == "--test":
            test = True
        elif a == "--print-path":
            pdata.append("path")
        elif a == "--print-id":
            pdata.append("id")
        elif a == "--print-content":
            pdata.append("content")
        elif a == "--print-cmd":
            pdata.append("cmd")
        elif a.startswith("--print-cmd="):
            pdata.append("cmd")
            pcdelim = read_split(a.split("\n", 1)[0], "=", 2)[1]
        elif a.startswith("--print-delimiter="):
            pdelim = read_split(a.split("\n", 1)[0], "=", 2)[1]
        elif a == "":
            raise OutOfContract("empty-string argument (the script loops forever)")
        elif not a.startswith("-"):
            break
        rest.pop(0)
    if not pdata and not test:
        raise OutOfContract("no print option and no --test: the resolver would launch a terminal")
    out = []

    def call_b(s):
        # one `printf %b` call; \c ends only that call's output
        txt, _stop = printf_b(s)
        out.append(txt)

    first = True
    action = r.entry_action
    if "id" in pdata:
        out.append(r.entry_id + (":" + action if action else ""))
        first = False
    path = r.entry_path
    if "path" in pdata:
        if "/./" in path:
            path = path.split("/./", 1)[0] + "/" + path.rsplit("/./", 1)[1]
        if not first:
            call_b(pdelim)
        out.append(path + (":" + action if action else ""))
        first = False
    if "content" in pdata:
        if not first:
            call_b(pdelim)
        try:
            text = read_file(r.entry_path)
        except OSError:
            if r.cache_used:
                return "".join(out), 1, r.stderr     # `shcat < path` fails under `set -e`
            text = ""
        for line in read_lines(text, False):
            out.append(line + "\n")
        first = False
    if not ("cmd" in pdata or not pdata):
        if "content" in pdata:
            return "".join(out), 0, r.stderr
        if pdelim == "\\n":
            call_b("\\n")
        return "".join(out), 0, r.stderr
    argv = list(rest)
    if argv and r.execarg != "":
        argv.insert(0, r.execarg)
    if r.holdarg and hold:
        argv.insert(0, r.holdarg)
    for val, arg in ((dirv, r.dirarg), (title, r.titlearg), (appid, r.appidarg)):
        if arg and val:
            if arg.endswith("="):
                argv.insert(0, arg + val)
            else:
                argv[0:0] = [arg, val]
    argv = split_ifs(r.exec_usep, USEP) + argv
    if test:
        out.append("Command and arguments:\n")
        for a in argv:
            out.append("  >%s<\n" % a)
        return "".join(out), 0, r.stderr
    if not first:
        call_b(pdelim)
    for i, a in enumerate(argv):
        if i:
            call_b(pcdelim if pcdelim != "" else "\\n")
        out.append(a)
    if pcdelim == "\\n" or (not first and pdelim == "\\n"):
        call_b("\\n")
    return "".join(out), 0, r.stderr


def explain(env, observed):
    r = Resolver(env)
    cache = "disabled"
    try:
        ok = r.select()
    except Exit:
        ok = False
    print("MADO_TERM_DESKTOPS: %s" % (":".join(r.desktops_lower) or "-"))
    for line in r.trace:
        print("MADO_TERM_TRACE: %s" % line)
    cache = getattr(r, "cache_state", "absent")
    if ok:
        argv0 = r.exec_usep.split(USEP, 1)[0]
        sel, path = r.entry_id + (":" + r.entry_action if r.entry_action else ""), r.entry_path
        if "/./" in path:
            path = path.split("/./", 1)[0] + "/" + path.rsplit("/./", 1)[1]
        path += ":" + r.entry_action if r.entry_action else ""
    else:
        argv0 = sel = path = "-"
    verdict = "OK" if ok else "NO_TERMINAL"
    rc = 0 if ok else 3
    if observed is not None:
        mine = run_print(env, ["--print-id", "--print-path", "--print-cmd"])[0] if ok else ""
        verdict = "AGREE" if mine == observed else "DIFFER"
        rc = 0 if verdict == "AGREE" else 1
    print("MADO_TERM: selected=%s path=%s cmd=%s cache=%s verdict=%s" % (sel, path, argv0, cache, verdict))
    return rc


# ------------------------------------------------------------------------------------------------ selftest
def _mk(root, files, execs):
    for rel, text in files.items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="latin-1") as fh:
            fh.write(text)
    for rel in execs:
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as fh:
            fh.write("#!/bin/sh\nexit 1\n")
        os.chmod(p, 0o755)


def _env(root, desk="Hyprland", **kw):
    e = {"HOME": root + "/home", "PATH": root + "/bin", "XDG_CONFIG_HOME": root + "/home/.config",
         "XDG_CONFIG_DIRS": root + "/etc/xdg", "XDG_DATA_HOME": root + "/home/.local/share",
         "XDG_DATA_DIRS": root + "/usr/share", "XDG_CACHE_HOME": root + "/cache"}
    if desk is not None:
        e["XDG_CURRENT_DESKTOP"] = desk
    e.update(kw)
    return e


def _term(name, extra=""):
    return "[Desktop Entry]\nType=Application\nName=%s\nExec=%s\nCategories=System;TerminalEmulator;\n%s" % (
        name, name, extra)


def selftest_cases():
    """(name, files, execs, args, want_stdout, want_rc, env overrides) of the hermetic selftest."""
    cases = []
    A = "usr/share/applications/"
    H = "home/.local/share/applications/"
    L = "home/.config/xdg-terminals.list"

    def case(name, files, execs, args, want_out, want_rc=0, **envkw):
        cases.append((name, files, execs, args, want_out, want_rc, envkw))

    case("fallback-single", {A + "foot.desktop": _term("foot")}, ["bin/foot"], ["--print-id"], "foot.desktop\n")
    case("listed-wins", {A + "foot.desktop": _term("foot"), A + "kitty.desktop": _term("kitty"), L: "kitty.desktop\n"},
         ["bin/foot", "bin/kitty"], ["--print-id"], "kitty.desktop\n")
    case("listed-missing-binary-falls-back", {A + "foot.desktop": _term("foot"), A + "kitty.desktop": _term("kitty"),
                                              L: "kitty.desktop\n"}, ["bin/foot"], ["--print-id"], "foot.desktop\n")
    case("user-override-path", {A + "foot.desktop": _term("foot"), H + "foot.desktop": _term("foot"), L: "foot.desktop\n"},
         ["bin/foot"], ["--print-path"], "$ROOT/home/.local/share/applications/foot.desktop\n")
    case("system-path-when-no-override", {A + "foot.desktop": _term("foot"), L: "foot.desktop\n"}, ["bin/foot"],
         ["--print-path"], "$ROOT/usr/share/applications/foot.desktop\n")
    case("none", {A + "foot.desktop": _term("foot")}, [], ["--print-id"], "", 1)
    case("hidden", {A + "foot.desktop": _term("foot", "Hidden=true\n")}, ["bin/foot"], ["--print-id"], "", 1)
    case("hidden-not-exact", {A + "foot.desktop": _term("foot", "Hidden=True\n")}, ["bin/foot"], ["--print-id"],
         "foot.desktop\n")
    case("not-terminal", {A + "foot.desktop": "[Desktop Entry]\nExec=foot\nCategories=System;\n"}, ["bin/foot"],
         ["--print-id"], "", 1)
    case("tryexec-missing", {A + "foot.desktop": _term("foot", "TryExec=footx\n")}, ["bin/foot"], ["--print-id"], "", 1)
    case("tryexec-builtin", {A + "foot.desktop": _term("foot", "TryExec=printf\n")}, ["bin/foot"], ["--print-id"],
         "foot.desktop\n")
    case("desktop-list-first", {A + "foot.desktop": _term("foot"), A + "kitty.desktop": _term("kitty"),
                                L: "foot.desktop\n", "home/.config/hyprland-xdg-terminals.list": "kitty.desktop\n"},
         ["bin/foot", "bin/kitty"], ["--print-id"], "kitty.desktop\n")
    case("desktop-list-case", {A + "foot.desktop": _term("foot"), A + "kitty.desktop": _term("kitty"),
                               L: "foot.desktop\n", "home/.config/Hyprland-xdg-terminals.list": "kitty.desktop\n"},
         ["bin/foot", "bin/kitty"], ["--print-id"], "foot.desktop\n")
    case("config-dirs-after-home", {A + "foot.desktop": _term("foot"), A + "kitty.desktop": _term("kitty"),
                                    L: "foot.desktop\n", "etc/xdg/xdg-terminals.list": "kitty.desktop\n"},
         ["bin/foot", "bin/kitty"], ["--print-id"], "foot.desktop\n")
    case("data-dir-list-last", {A + "foot.desktop": _term("foot"), A + "kitty.desktop": _term("kitty"),
                                "usr/share/xdg-terminal-exec/xdg-terminals.list": "kitty.desktop\n"},
         ["bin/foot", "bin/kitty"], ["--print-id"], "kitty.desktop\n")
    case("action", {A + "foot.desktop": _term("foot", "Actions=srv;\n[Desktop Action srv]\nExec=footclient\n"),
                    L: "foot.desktop:srv\n"}, ["bin/foot", "bin/footclient"], ["--print-id", "--print-cmd"],
         "foot.desktop:srv\nfootclient\n")
    case("action-unlisted", {A + "foot.desktop": _term("foot", "[Desktop Action srv]\nExec=footclient\n"),
                             L: "foot.desktop:srv\n"}, ["bin/foot", "bin/footclient"], ["--print-id"], "", 1)
    case("misspelled", {A + "foot.desktop": _term("foot"), L: "foot\n"}, ["bin/foot"], ["--print-id"], "foot.desktop\n")
    case("exclusion", {A + "foot.desktop": _term("foot"), L: "-foot.desktop\n"}, ["bin/foot"], ["--print-id"], "", 1)
    case("exclusion-listed-still-works", {A + "foot.desktop": _term("foot"), L: "-foot.desktop\nfoot.desktop\n"},
         ["bin/foot"], ["--print-id"], "foot.desktop\n")
    case("include-beats-exclude", {A + "foot.desktop": _term("foot"), L: "+foot.desktop\n-foot.desktop\n"},
         ["bin/foot"], ["--print-id"], "foot.desktop\n")
    case("subdir-id", {A + "vendor/foot.desktop": _term("foot")}, ["bin/foot"], ["--print-id"], "vendor-foot.desktop\n")
    case("onlyshowin-fallback", {A + "foot.desktop": _term("foot", "OnlyShowIn=GNOME;\n")}, ["bin/foot"], ["--print-id"],
         "", 1)
    case("onlyshowin-listed-ignored", {A + "foot.desktop": _term("foot", "OnlyShowIn=GNOME;\n"), L: "foot.desktop\n"},
         ["bin/foot"], ["--print-id"], "foot.desktop\n")
    case("cmd-with-command", {A + "foot.desktop": _term("foot")}, ["bin/foot"], ["--print-cmd", "--", "htop", "-d", "5"],
         "foot\n-e\nhtop\n-d\n5\n")
    case("cmd-dir-arg", {A + "foot.desktop": _term("foot", "X-TerminalArgDir=--working-directory=\n")}, ["bin/foot"],
         ["--print-cmd", "--dir=/srv"], "foot\n--working-directory=/srv\n")
    case("cmd-title-sep", {A + "foot.desktop": _term("foot", "TerminalArgTitle=--title\n")}, ["bin/foot"],
         ["--print-cmd", "--title=x y"], "foot\n--title\nx y\n")
    case("execarg-default", {A + "foot.desktop": _term("foot"), L: "/execarg_default:foot.desktop:-x\n"}, ["bin/foot"],
         ["--print-cmd", "--", "top"], "foot\n-x\ntop\n")
    case("strict-no-execarg", {A + "foot.desktop": _term("foot"), L: "/execarg_strict\n"}, ["bin/foot"], ["--print-id"],
         "", 1)
    case("exec-fields", {A + "foot.desktop": _term("foot").replace("Exec=foot", 'Exec="foot" --a %U %i "b c" 100%%')},
         ["bin/foot"], ["--print-cmd"], "foot\n--a\nb c\n100%\n")
    case("delimiter", {A + "foot.desktop": _term("foot")}, ["bin/foot"],
         ["--print-id", "--print-path", "--print-delimiter=\\t"], "foot.desktop\t$ROOT/usr/share/applications/foot.desktop")
    case("cmd-delimiter", {A + "foot.desktop": _term("foot")}, ["bin/foot"], ["--print-cmd=\\s", "--", "a"],
         "foot\\s-e\\sa")
    case("carry-over-category", {A + "a1.desktop": "[Desktop Entry]\nCategories=TerminalEmulator;\n",
                                 A + "b2.desktop": "[Desktop Entry]\nExec=foot\n", L: "a1.desktop\nb2.desktop\n"},
         ["bin/foot"], ["--print-id"], "b2.desktop\n")
    case("no-final-newline", {A + "foot.desktop": "[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;"},
         ["bin/foot"], ["--print-id"], "", 1)
    case("test-mode", {A + "foot.desktop": _term("foot")}, ["bin/foot"], ["--test", "--", "ls"],
         "Command and arguments:\n  >foot<\n  >-e<\n  >ls<\n")
    case("tryexec-alias-of-untried-id", {A + "foot.desktop": _term("foot", "TryExec=kitty.desktop\n"),
                                         A + "kitty.desktop": "[Desktop Entry]\nName=k\n", L: "foot.desktop\n"},
         ["bin/foot"], ["--print-id"], "foot.desktop\n")
    case("tryexec-alias-already-tried", {A + "foot.desktop": _term("foot", "TryExec=kitty.desktop\n"),
                                         A + "kitty.desktop": "[Desktop Entry]\nName=k\n",
                                         L: "kitty.desktop\nfoot.desktop\n"}, ["bin/foot"], ["--print-id"], "", 1)
    case("loop-status-entry-header-last", {A + "b.desktop": "Actions=act;\n[Desktop Action act]\nExec=foot\n"
                                           "Categories=TerminalEmulator;\n[Desktop Entry]\n", L: "b.desktop:act\n"},
         ["bin/foot"], ["--print-id"], "", 1)
    case("loop-status-other-group-last", {A + "b.desktop": "Categories=TerminalEmulator;\n[Other]\n",
                                          A + "a.desktop": "[Desktop Entry]\nExec=foot\n", L: "a.desktop\nb.desktop\n"},
         ["bin/foot"], ["--print-id"], "", 1)
    case("title-trailing-equals", {A + "foot.desktop": _term("foot", "TerminalArgTitle=--title\n")}, ["bin/foot"],
         ["--print-cmd", "--title=x="], "foot\n--title\nx\n")
    case("execarg-default-trailing-colon", {A + "foot.desktop": _term("foot"), L: "/execarg_default:foot.desktop:-x:\n"},
         ["bin/foot"], ["--print-cmd", "--", "top"], "foot\n-x\ntop\n")
    case("strip-fields-failure-keeps-tokens", {A + "foot.desktop": _term("foot").replace("Exec=foot", "Exec=foot %f %u")},
         ["bin/foot"], ["--print-cmd"], "foot\n%f\n%u\n")
    case("unset-desktop", {A + "foot.desktop": _term("foot"), "home/.config/-xdg-terminals.list": "kitty.desktop\n"},
         ["bin/foot"], ["--print-id"], "foot.desktop\n", desk=None)
    return cases


def selftest():
    base = tempfile.mkdtemp(prefix="mado-terminal-selftest.", dir=os.environ.get("TMPDIR") or None)
    cases = selftest_cases()
    passed = 0
    try:
        for i, (name, files, execs, args, want_out, want_rc, envkw) in enumerate(cases):
            root = os.path.join(base, "c%02d" % i)
            os.makedirs(root + "/home", exist_ok=True)
            os.makedirs(root + "/cache", exist_ok=True)
            _mk(root, files, execs)
            desk = envkw.pop("desk", "Hyprland")
            env = _env(root, desk, **envkw)
            try:
                got, rc, _err = run_print(env, args, cwd=root)
            except OutOfContract as ex:
                got, rc = "OOC:%s" % ex, 2
            want = want_out.replace("$ROOT", root)
            if got == want and rc == want_rc:
                passed += 1
            else:
                print("MADO_TERMINAL_SELFTEST_FAIL: %s got=%r rc=%d want=%r rc=%d" % (name, got, rc, want, want_rc))
    finally:
        import shutil
        shutil.rmtree(base, ignore_errors=True)
    print("MADO_TERMINAL_SELFTEST: %d/%d passed" % (passed, len(cases)))
    return 0 if passed == len(cases) else 1


def main(argv):
    if len(argv) >= 1 and argv[0] == "--selftest":
        return selftest()
    if not argv or argv[0] not in ("print", "explain"):
        sys.stderr.write("usage: mado-terminal.py print [options] [--] [cmd ...] | explain [--observed FILE] | --selftest\n")
        return 2
    env = dict(os.environ)
    if argv[0] == "print":
        try:
            out, rc, err = run_print(env, argv[1:])
        except OutOfContract as ex:
            sys.stderr.write("MADO_TERM_OUT_OF_CONTRACT: %s\n" % ex)
            return 2
        for line in err:
            sys.stderr.write(line + "\n")
        sys.stdout.buffer.write(out.encode("latin-1"))
        sys.stdout.flush()
        return rc
    observed = None
    rest = argv[1:]
    if rest:
        if len(rest) != 2 or rest[0] != "--observed":
            sys.stderr.write("usage: mado-terminal.py explain [--observed FILE]\n")
            return 2
        try:
            observed = read_file(rest[1])
        except OSError as ex:
            sys.stderr.write("cannot read %s: %s\n" % (rest[1], ex))
            return 2
    try:
        return explain(env, observed)
    except OutOfContract as ex:
        sys.stderr.write("MADO_TERM_OUT_OF_CONTRACT: %s\n" % ex)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

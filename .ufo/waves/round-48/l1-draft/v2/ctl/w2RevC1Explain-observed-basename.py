#!/usr/bin/env python3
"""mado-terminal.py - which terminal does `xdg-terminal-exec` (SUPER+RETURN on this host) pick, and why.

Read-only. Starts no process, opens no socket, writes no file. Python 3 standard library only.

The resolver modelled is xdg-terminal-exec v0.14.3 (upstream tag v0.14.3, script sha256
89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac = the host's /usr/bin/xdg-terminal-exec). Line
numbers below ("x:N") are lines of that script.

Usage
-----
  mado-terminal.py print [xdg-terminal-exec options] [--] [command [args ...]]
      Prints exactly what `xdg-terminal-exec` prints on stdout for the same options and arguments in the same
      environment, and exits with its exit status, honouring the resolver's cache file (see "Cache" below). At least one of
      --print-id, --print-path, --print-content, --print-cmd[=SEQ] or --test is required (without one the resolver
      would launch a terminal; this tool refuses with exit 2).
  mado-terminal.py explain [--observed FILE]
      A trace of the selection (every list file read, every candidate and why it was skipped), then one line
          MADO_TERM: selected=<id|-> path=<path|-> cmd=<exec[0]|-> cache=<absent|hit|stale|invalid|disabled|-> verdict=<V>
      selected= and path= are what --print-id and --print-path print (an action rides on both as `:<action>`).
      V is OK (a terminal is selected), NO_TERMINAL (none is), and with --observed FILE - the captured stdout of
      `XDG_CACHE_HOME=$(mktemp -d) xdg-terminal-exec --print-id --print-path --print-cmd` - AGREE when the three
      printed items equal this tool's (id, path, and command line), DIFFER otherwise.
      Exit: 0 OK/AGREE, 1 DIFFER, 3 NO_TERMINAL, 2 usage error.
  mado-terminal.py --selftest
      Hermetic cases built under $TMPDIR; last line `MADO_TERMINAL_SELFTEST: N/N passed`; exit 0 iff all pass.

Environment read (as the resolver reads it): HOME, PATH, XDG_CURRENT_DESKTOP, XDG_CONFIG_HOME, XDG_CONFIG_DIRS,
XDG_DATA_HOME, XDG_DATA_DIRS, XDG_CACHE_HOME, XTE_EXECARG_COMPAT, XTE_CACHE_ENABLED, TZ (through the C library).

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
 4. Desktop entries (x:754-800): `find -L <dir>/. -type f` is grouped by application directory with `-o` (x:760-774).
    Because implicit `-a` binds tighter than `-o`, `-type f` restricts only the FIRST directory group; later groups
    register any path type whose relative name passes the id filter (round-47 H1, measured at `ExecC1Diff.md`). The
    directories are walked in preference order: the last of XDG_DATA_DIRS first, XDG_DATA_HOME (default
    $HOME/.local/share) last. The name part after `<dir>/./` must start with [a-zA-Z0-9_], end in `.desktop`, and hold
    only [a-zA-Z0-9_./-]; '/' becomes '-' in the id. Readdir order is observed, not sorted; later paths for one id win,
    and each non-excluded found path is prepended to the fallback list.
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

Cache (round 48, in contract): before reading any list or entry (x:1179) the resolver tries the one cache file
$XDG_CACHE_HOME/xdg-terminal-exec (default $HOME/.cache; x:171-173) unless XTE_CACHE_ENABLED in the environment is not
true (check_bool, x:50-59; the /enable_cache and /disable_cache directives are read only on the cold path, x:371-386).
Not a regular file -> absent. The file is read like `while IFS= read -r` (x:221-262): lines 1-10 are the hash, the
command name, the entry path, id, action, and the exec, app-id, title, dir and hold argument names; from line 11 the
lines are joined with a newline (none before the first non-empty part) until one ends in 0x1e "END_OF_EXEC_USEP"; no
such line before line 50, or an unterminated last line, -> invalid (cold path). A complete cache is used (hit) iff
gen_hash (x:179-215) - md5 of "4", XDG_CURRENT_DESKTOP (through bash `echo`) and `LC_ALL=C LANG=C ls -LRl` of the
':'-split list paths and application dirs, stderr dropped - equals line 1 and `command -v <line 2>` succeeds (x:274,
no aliases defined yet); else stale (cold path). This tool emulates that `ls -LRl` listing byte for byte (GNU
coreutils: operands sorted, files before directories, per-block column widths, `total` in the floor of summed 512-byte
blocks / 2, C-locale dates with the six-month boundary, hidden names skipped, -L following links, `l?????????` rows for
dangling links, ancestor loops skipped (with no header for a looped directory), user and group names from the passwd/group
databases or numeric). On a hit every print mode uses the cached id, path (still holding `/./`), action, Exec words
and argument names, exactly as x:274-284 load them, so a stale-but-valid cache (a same-size edit within the same
minute, a TryExec binary removed while the
command name still resolves) is reproduced, not corrected. A cold resolver's
`--print-cmd` and `--test` save the cache in the background (x:1455-1458); this tool never writes it. `explain` reports
`cache=absent|hit|stale|invalid|disabled`; HOME unset is modelled as the script (`set -u`, x:23): when any HOME-based
default is needed (XDG_CONFIG_HOME, XDG_DATA_HOME or XDG_CACHE_HOME unset or empty; x:148, x:166, x:172) it exits 1
with empty stdout, and with all three set it runs normally.
Out of contract: -h/--help; a FIFO named like a desktop file in a later application dir when it is the candidate the
resolver reads (the script blocks); an empty-string argument (the script loops forever); XDG dirs or HOME containing
`:` inside a default, glob characters or a quote; non-ASCII `\\u`/`\\U` delimiter escapes; names containing newline
bytes (GNU ls changes them to `?`); ACL/security xattrs under a hashed path; an mtime within one second of the six-month
date boundary; and ls environment variables (BLOCK_SIZE, LS_BLOCK_SIZE, POSIXLY_CORRECT, TIME_STYLE, QUOTING_STYLE,
LS_COLORS) set. Where detected, these print `MADO_TERM_OUT_OF_CONTRACT: <reason>` and exit 2.
"""
import fnmatch
import grp
import hashlib
import os
import pwd
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

CACHE_END = "\x1eEND_OF_EXEC_USEP"
LS_ENV = ("BLOCK_SIZE", "LS_BLOCK_SIZE", "POSIXLY_CORRECT", "TIME_STYLE", "QUOTING_STYLE", "LS_COLORS")

# ---------------------------------------------------------------- `LC_ALL=C LANG=C ls -LRl` (GNU coreutils), no process
SIX_MONTHS = 31556952 // 2
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def _mode(st):
    m = st.st_mode
    if stat.S_ISDIR(m):
        t = "d"
    elif stat.S_ISREG(m):
        t = "-"
    elif stat.S_ISLNK(m):
        t = "l"
    elif stat.S_ISCHR(m):
        t = "c"
    elif stat.S_ISBLK(m):
        t = "b"
    elif stat.S_ISFIFO(m):
        t = "p"
    elif stat.S_ISSOCK(m):
        t = "s"
    else:
        t = "?"
    s = [t]
    for r, w, x, sp, spc in ((stat.S_IRUSR, stat.S_IWUSR, stat.S_IXUSR, stat.S_ISUID, "s"),
                             (stat.S_IRGRP, stat.S_IWGRP, stat.S_IXGRP, stat.S_ISGID, "s"),
                             (stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH, stat.S_ISVTX, "t")):
        s.append("r" if m & r else "-")
        s.append("w" if m & w else "-")
        if m & sp:
            s.append(spc if m & x else spc.upper())
        else:
            s.append("x" if m & x else "-")
    return "".join(s)


def _user(uid):
    try:
        return pwd.getpwuid(uid).pw_name
    except (KeyError, OverflowError):
        return str(uid)


def _group(gid):
    try:
        return grp.getgrgid(gid).gr_name
    except (KeyError, OverflowError):
        return str(gid)


def _date(st, now):
    sec = st.st_mtime_ns
    tm = time.localtime(st.st_mtime_ns // 1000000000)
    recent = now - SIX_MONTHS * 1000000000 < sec < now
    if abs((now - sec) - SIX_MONTHS * 1000000000) <= 1000000000:
        raise OutOfContract("mtime within one second of GNU ls six-month date boundary")
    mon = MONTHS[tm.tm_mon - 1]
    if recent:
        return "%s %2d %02d:%02d" % (mon, tm.tm_mday, tm.tm_hour, tm.tm_min)
    return "%s %2d  %d" % (mon, tm.tm_mday, tm.tm_year)


def _fmt_owner(value, width):
    """GNU ls left-justifies a resolved name, but right-justifies a numeric uid/gid."""
    return value.rjust(width) if value.isascii() and value.isdigit() else value.ljust(width)


def _block(entries, now, width_extra=()):
    """entries: list of (name, stat or None). Returns lines (without the total line) and total 1K blocks.
    width_extra: further (name, stat) whose columns count for the widths but are not printed (GNU ls sizes the
    command-line file block over every command-line operand, directories included)."""
    rows = []
    total = 0
    for name, st in entries:
        if st is None:
            rows.append(("l?????????", "?", "?", "?", "?", "?", name))
            continue
        total += st.st_blocks
        if stat.S_ISCHR(st.st_mode) or stat.S_ISBLK(st.st_mode):
            size = "%d, %d" % (os.major(st.st_rdev), os.minor(st.st_rdev))
        else:
            size = str(st.st_size)
        rows.append((_mode(st), str(st.st_nlink), _user(st.st_uid), _group(st.st_gid), size, _date(st, now), name))
    if not rows:
        return [], total // 2
    wrows = rows + [(None, str(st.st_nlink), _user(st.st_uid), _group(st.st_gid), str(st.st_size)) for _n, st in width_extra]
    wl = max(len(r[1]) for r in wrows)
    wu = max(len(r[2]) for r in wrows)
    wg = max(len(r[3]) for r in wrows)
    ws = max(len(r[4]) for r in wrows)
    out = []
    for mode, nl, us, gr, size, date, name in rows:
        out.append("%s %s %s %s %s %s %s" % (mode, nl.rjust(wl), _fmt_owner(us, wu), _fmt_owner(gr, wg), size.rjust(ws),
                                             date.rjust(12), name))
    return out, total // 2


def _stat(p):
    try:
        st = os.stat(p)
    except OSError:
        return None
    for attr in ("system.posix_acl_access", "system.posix_acl_default", "security.selinux"):
        try:
            os.getxattr(p, attr)
        except OSError as ex:
            if ex.errno in (1, 13):
                raise OutOfContract("cannot inspect ls ACL/security xattrs")
        else:
            raise OutOfContract("ls ACL/security xattr present under a hashed path")
    return st


def _key(n):
    if "\n" in n:
        raise OutOfContract("newline in an ls path/name changes the cache hash")
    return n.encode("utf-8", "surrogateescape")

def ls_lRL(operands, now_ns=None):
    now = time.time_ns() if now_ns is None else now_ns
    files, dirs = [], []
    for op in operands:
        st = _stat(op)
        if st is None:
            continue
        (dirs if stat.S_ISDIR(st.st_mode) else files).append((op, st))
    files.sort(key=lambda t: _key(t[0]))
    dirs.sort(key=lambda t: _key(t[0]))
    out = []
    if files:
        lines, _t = _block(files, now, dirs)
        out.extend(lines)
    state = {"first": not files}
    active = set()

    def visit(path, st):
        key = (st.st_dev, st.st_ino)
        try:
            names = os.listdir(path)
        except OSError:
            return
        if key in active:
            return
        active.add(key)
        names = sorted((n for n in names if not n.startswith(".")), key=_key)
        ents = []
        subs = []
        for n in names:
            child = path + n if path.endswith("/") else path + "/" + n
            cst = _stat(child)
            ents.append((n, cst))
            if cst is not None and stat.S_ISDIR(cst.st_mode):
                subs.append((child, cst))
        if not state["first"]:
            out.append("")
        state["first"] = False
        out.append(path + ":")
        lines, total = _block(ents, now)
        out.append("total %d" % total)
        out.extend(lines)
        for child, cst in subs:
            visit(child, cst)
        active.discard(key)

    for path, st in dirs:
        visit(path, st)
    return ("\n".join(out) + "\n").encode("utf-8", "surrogateescape") if out else b""


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
        for k in ("XDG_CONFIG_HOME", "XDG_CONFIG_DIRS", "XDG_DATA_HOME", "XDG_DATA_DIRS"):
            v = e.get(k, "")
            if any(c in v for c in "[]*?\\'\""):
                raise OutOfContract("%s holds a glob character or a quote" % k)
        home = e.get("HOME")
        if home is not None and any(c in home for c in ":[]*?\\'\""):
            raise OutOfContract("HOME holds ':' a glob character or a quote")

        def need_home(line):
            # `set -u` (x:23): the first default that expands an unset HOME ends the script, exit 1, stdout empty
            if home is None:
                self.err("/usr/bin/xdg-terminal-exec: line %d: HOME: unbound variable" % line)
                raise Exit(1)
            return home
        cfg = (e.get("XDG_CONFIG_HOME") or need_home(148) + "/.config") + ":" + (e.get("XDG_CONFIG_DIRS") or "/etc/xdg")
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
        for d in split_ifs((e.get("XDG_DATA_HOME") or need_home(166) + "/.local/share") + ":" + data, ":"):
            d = d[:-1] if d.endswith("/") else d
            apps.insert(0, d + "/applications/")
        self.app_dirs = apps
        self.cache_file = (e.get("XDG_CACHE_HOME") or need_home(172) + "/.cache") + "/xdg-terminal-exec"

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
            if stat.S_ISFIFO(os.stat(path).st_mode):
                raise OutOfContract("a FIFO candidate blocks the resolver's entry read")
        except OutOfContract:
            raise
        except OSError:
            pass
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
        """md5 of `echo 4; echo "$XDG_CURRENT_DESKTOP"; LANG=C ls -LRl $CONFIGS:$APPLICATIONS_DIRS` (x:179-215)."""
        dsk = self.env.get("XDG_CURRENT_DESKTOP", "")
        if len(dsk) > 1 and dsk[0] == "-" and all(c in "neE" for c in dsk[1:]):
            echo = b"" if "n" in dsk else b"\n"     # bash `echo` takes the value as its own options
        else:
            echo = dsk.encode("utf-8", "surrogateescape") + b"\n"
        for k in LS_ENV:
            if k in self.env:
                raise OutOfContract("%s set (changes the ls listing the cache hash covers)" % k)
        operands = split_ifs(":".join(self.configs) + ":" + ":".join(self.app_dirs), ":")
        listing = ls_lRL(operands)
        self.t("cache: hashing XDG_CURRENT_DESKTOP and ls -LRl of %d operands (%d bytes)" % (len(operands), len(listing)))
        return hashlib.md5(b"4\n" + echo + listing).hexdigest()

    def read_cache(self):
        """Returns absent | invalid | stale | hit and, on hit, loads the cached selection (x:217-298)."""
        p = self.cache_file
        if not os.path.isfile(p):
            self.t("cache: %s absent" % p)
            return "absent"
        try:
            lines = read_lines(read_file(p), False)
        except OSError:
            self.t("cache: %s unreadable" % p)
            return "invalid"
        fields = [""] * 10
        usep = ""
        finished = False
        for n, line in enumerate(lines, 1):
            if n <= 10:
                fields[n - 1] = line
                continue
            if n == 50:
                self.t("cache: %s invalid (line limit 50)" % p)
                return "invalid"
            usep = usep + ("\n" if usep else "") + line
            if line.endswith(CACHE_END):
                usep = usep[:-len(CACHE_END)]
                finished = True
                break
        if not finished:
            self.t("cache: %s invalid (no terminator)" % p)
            return "invalid"
        if self.gen_hash() != fields[0] or not self.command_v(fields[1]):
            self.t("cache: %s out of date" % p)
            return "stale"
        self.exec_usep = usep
        (self.entry_path, self.entry_id, self.entry_action, self.execarg, self.appidarg, self.titlearg, self.dirarg,
         self.holdarg) = fields[2:10]
        self.t("cache: %s actual: %s %s" % (p, self.entry_id, self.entry_path))
        return "hit"

    def select_paths(self):
        """Desktop names and paths only (what gen_hash needs); used by the selftest."""
        e = self.env
        dsk = e.get("XDG_CURRENT_DESKTOP", "")
        low = "".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in dsk).rstrip("\n")
        self.desktops_lower = split_ifs(low, ":")
        self.aliases = {}
        self.make_paths()

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
        self.cache = "disabled"
        if check_bool(self.cache_enabled, self.err):
            self.cache = self.read_cache()
            if self.cache == "hit":
                return True
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
            # `shcat < "$XTE__ENTRY_PATH"` (x:1362): the redirection fails, `set -e` ends the script with status 1;
            # reachable only from a cache whose entry path is gone (the cold path has just read the entry)
            return "".join(out), 1, r.stderr
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
    try:
        ok = r.select()
    except Exit:
        ok = False
    print("MADO_TERM_DESKTOPS: %s" % (":".join(r.desktops_lower) or "-"))
    for line in r.trace:
        print("MADO_TERM_TRACE: %s" % line)
    cache = getattr(r, "cache", "-")
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
        def _rel(t):
            return "\n".join(os.path.basename(x.rstrip(":")) if "/" in x else x for x in t.split("\n"))
        verdict = "AGREE" if _rel(mine) == _rel(observed) else "DIFFER"
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


def _fake_stat(mode, nlink=1, uid=0, gid=0, size=0, mtime=0, blocks=0):
    return os.stat_result((mode, 1, 1, nlink, uid, gid, size, mtime, mtime, mtime),
                          {"st_mtime_ns": mtime * 1000000000, "st_blocks": blocks, "st_rdev": 0})


def ls_selftest():
    """(name, ok) of the `ls -l` row format on synthetic stat records (no filesystem, no clock)."""
    out = []
    now = 1761500000 * 1000000000
    S = stat
    F = _fake_stat
    rows = [("a.desktop", F(S.S_IFREG | 0o644, 1, 4242, 4243, 7, 1761400000, 8)),
            ("big", F(S.S_IFREG | 0o4755, 12, 4242, 4243, 123456, 1500000000, 243)),
            ("sub", F(S.S_IFDIR | 0o1777, 3, 4242, 4243, 40, 1761499999, 0)),
            ("gone", None)]
    lines, total = _block(rows, now)
    tm = time.localtime(1761400000)
    want0 = "-rw-r--r--  1 %s %s      7 %s %2d %02d:%02d a.desktop" % (
        _user(4242), _group(4243), MONTHS[tm.tm_mon - 1], tm.tm_mday, tm.tm_hour, tm.tm_min)
    out.append(("ls-row-recent", lines[0].split(" ")[0] == "-rw-r--r--" and lines[0].endswith(" a.desktop")
                and lines[0].count(" ") >= 7 and "%02d:%02d" % (tm.tm_hour, tm.tm_min) in lines[0] and
                (_user(4242) != "4242" or lines[0] == want0)))
    tb = time.localtime(1500000000)
    out.append(("ls-row-old-year", (" %d big" % tb.tm_year) in lines[1] and lines[1].startswith("-rwsr-xr-x 12 ")))
    out.append(("ls-row-sticky-dir", lines[2].startswith("drwxrwxrwt  3 ")))
    out.append(("ls-row-dangling", lines[3].startswith("l?????????  ? ") and lines[3].endswith("           ? gone")))
    out.append(("ls-widths-aligned", len({len(l) - len(l.rsplit(" ", 1)[1]) for l in lines[:3]}) == 1))
    out.append(("ls-total-floor", total == 125))
    _l, t2 = _block([("x", F(S.S_IFREG | 0o600, 1, 0, 0, 1, 0, 0))], now)
    out.append(("ls-total-zero", t2 == 0))
    return out


def warm_selftest(base):
    """(name, ok) of the cache path on hermetic trees whose cache bytes this tool writes itself."""
    out = []
    A = "usr/share/applications/"
    END = CACHE_END

    def tree(i, extra_files=None):
        root = os.path.join(base, "w%02d" % i)
        os.makedirs(root + "/home", exist_ok=True)
        os.makedirs(root + "/cache", exist_ok=True)
        files = {A + "foot.desktop": _term("foot"), A + "kitty.desktop": "[Desktop Entry]\nName=k\n"}
        files.update(extra_files or {})
        _mk(root, files, ["bin/foot", "bin/kitty"])
        return root

    def hash_of(root, env):
        r = Resolver(env, root)
        r.select_paths()
        return r.gen_hash()

    def cache(root, lines):
        with open(root + "/cache/xdg-terminal-exec", "w", encoding="latin-1") as fh:
            fh.write("".join(l + "\n" for l in lines))

    def body(h, cmd="foot", path=None, eid="kitty.desktop", action="", args=("", "", "", "", ""), exe="kitty"):
        return [h, cmd, path or "$R/" + A.rstrip("/") + "/./kitty.desktop", eid, action] + list(args) + [exe + END]

    def check(name, i, mk_lines, argv, want, want_rc=0, envkw=None, files=None):
        root = tree(i, files)
        env = _env(root, **(envkw or {}))
        h = hash_of(root, env)
        lines = [l.replace("$R", root) for l in mk_lines(h)]
        if lines:
            cache(root, lines)
        try:
            got, rc, _e = run_print(env, argv, cwd=root)
        except OutOfContract as ex:
            got, rc = "OOC:%s" % ex, 2
        ok = (got, rc) == (want.replace("$R", root), want_rc)
        if not ok:
            print("MADO_TERMINAL_SELFTEST_FAIL: %s got=%r rc=%d" % (name, got, rc))
        out.append((name, ok))

    check("warm-hit-cmd", 1, lambda h: body(h), ["--print-cmd"], "kitty\n")
    check("warm-hit-id-path-folded", 2, lambda h: body(h), ["--print-id", "--print-path"],
          "kitty.desktop\n$R/usr/share/applications/kitty.desktop\n")
    check("warm-stale-hash", 3, lambda h: body("0" * 32), ["--print-cmd"], "foot\n")
    check("warm-stale-cmd", 4, lambda h: body(h, cmd="nosuch"), ["--print-cmd"], "foot\n")
    check("warm-cmd-builtin-ok", 5, lambda h: body(h, cmd="printf"), ["--print-cmd"], "kitty\n")
    check("warm-invalid-no-terminator", 6, lambda h: body(h)[:-1] + ["kitty"], ["--print-cmd"], "foot\n")
    check("warm-line-49-ok", 7, lambda h: body(h)[:10] + [""] * 38 + ["kitty" + END], ["--print-cmd"], "kitty\n")
    check("warm-line-50-invalid", 8, lambda h: body(h)[:10] + [""] * 39 + ["kitty" + END], ["--print-cmd"], "foot\n")
    check("warm-disabled-env", 9, lambda h: body(h), ["--print-cmd"], "foot\n", envkw={"XTE_CACHE_ENABLED": "no"})
    check("warm-directive-does-not-disable-read", 10, lambda h: body(h), ["--print-cmd"], "kitty\n",
          files={"home/.config/xdg-terminals.list": "/disable_cache\n"})
    check("warm-cached-dir-arg", 11, lambda h: body(h, args=("-e", "", "", "--wd=", "")), ["--print-cmd", "--dir=/srv"],
          "kitty\n--wd=/srv\n")
    check("warm-cached-execarg", 12, lambda h: body(h, args=("-x", "", "", "", "")), ["--print-cmd", "--", "top"],
          "kitty\n-x\ntop\n")
    check("warm-multiline-exec", 13, lambda h: body(h)[:10] + ["", "kitty" + END], ["--print-cmd"], "kitty\n")
    check("warm-desktop-changes-hash", 14, lambda h: body(hash_of(os.path.join(base, "w14"), _env(
        os.path.join(base, "w14"), "GNOME"))), ["--print-cmd"], "foot\n")
    check("warm-action-from-cache", 15, lambda h: body(h, action="new"), ["--print-id"], "kitty.desktop:new\n")
    check("warm-unterminated-last-line", 16, lambda h: body(h), ["--print-cmd"], "kitty\n")
    root = tree(17)
    env = _env(root)
    h = hash_of(root, env)
    with open(root + "/cache/xdg-terminal-exec", "w") as fh:
        fh.write("\n".join(l.replace("$R", root) for l in body(h)))       # last line unterminated
    out.append(("warm-unterminated-terminator-line", run_print(env, ["--print-cmd"], cwd=root)[0] == "foot\n"))
    root = tree(18)
    env = _env(root)
    del env["HOME"]
    out.append(("home-unset-all-xdg-set", run_print(env, ["--print-id"], cwd=root)[:2] == ("foot.desktop\n", 0)))
    del env["XDG_DATA_HOME"]
    out.append(("home-unset-needed", run_print(env, ["--print-id"], cwd=root)[:2] == ("", 1)))
    return out


def selftest():
    base = tempfile.mkdtemp(prefix="mado-terminal-selftest.", dir=os.environ.get("TMPDIR") or None)
    cases = selftest_cases()
    passed = 0
    extra = []
    try:
        extra = ls_selftest() + warm_selftest(base)
        for name, ok in extra:
            passed += ok
            if not ok:
                print("MADO_TERMINAL_SELFTEST_FAIL: %s" % name)
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
    total = len(cases) + len(extra)
    print("MADO_TERMINAL_SELFTEST: %d/%d passed" % (passed, total))
    return 0 if passed == total else 1


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

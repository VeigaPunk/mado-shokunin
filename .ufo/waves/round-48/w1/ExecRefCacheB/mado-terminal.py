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
      environment, and exits with its exit status, for the cache the environment has (see "Cache" below). At least one of
      --print-id, --print-path, --print-content, --print-cmd[=SEQ] or --test is required (without one the resolver
      would launch a terminal; this tool refuses with exit 2).
  mado-terminal.py explain [--observed FILE]
      A trace of the selection (the cache verdict, every list file read, every candidate and why it was
      skipped), then one line
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

Cache (x:217-298, x:1166-1180) - modelled, hit and miss. Before reading any list or entry the resolver tries
$XDG_CACHE_HOME/xdg-terminal-exec (default $HOME/.cache) unless `check_bool "$XTE_CACHE_ENABLED"` fails, and it
uses the file only when all three hold: it parses (10 field lines, then the command on lines 11.. up to a line
ending in 0x1e"END_OF_EXEC_USEP"; reaching line 50 or the end of the file first is "invalid", x:224-259); its
first line equals the md5 of "4\n$XDG_CURRENT_DESKTOP\n" plus `LC_ALL=C LANG=C ls -LRl` of the colon-split
${XTE__CONFIGS}:${XTE__APPLICATIONS_DIRS} with stderr dropped (x:179-215); and `command -v` finds its second
line (x:283). On a hit the cached entry path/id/action, exec argument, ap-id/title/dir/hold arguments and the
whole command are used and NO list or entry file is read, so a cache that still hashes correctly but describes
an older tree makes the resolver print what a cold run would not (an edit that keeps the file's size and its
minute of mtime is invisible to the hash). The cache file produces one of
  cache=absent     no regular file at the path (a directory or FIFO is not a cache: `[ -f ]`)
  cache=invalid    it exists but does not parse (no terminator, or line 50 reached)
  cache=stale      it parses, but the hash differs or the cached command does not resolve
  cache=hit        all three hold and the cached values are used
  cache=disabled   XTE_CACHE_ENABLED is false (`check_bool`), so it is not even read
A /disable_cache directive does NOT prevent a hit: directives are read on the cold path only, and the resolver
does not save over a hit (`save_cache` runs only when the cache was NOT used, x:1451-1455), so the file stays.
An unreadable cache file is a cold path with a shell redirection error on stderr, not an exit: `read_cache` sits
inside an `&&` list, where `set -e` does not apply (x:1179). This tool never writes the cache the resolver would
save, so `print` leaves the environment exactly as it found it.

The hash's `ls -LRl` (x:204) is reproduced byte for byte: -L dereferencing (an entry whose stat then fails is
`l?????????`, the type letter taken from the dirent), files-then-directories operand order with a byte sort inside
each group, per-block column widths (the file block widens from the directory operands too), `total N` in 1 KiB
units rounded up from st_blocks, C-locale dates (12 columns; "Mon dd HH:MM" inside 31556952/2 s and not in the
future, else "Mon dd  YYYY"), recursion headers built from the operand as typed, cycle skipping by (st_dev,
st_ino) on the current path, dot entries skipped, and `literal` name quoting (LF printed as '?'). Out of contract
there: BLOCKSIZE / LS_BLOCK_SIZE / POSIXLY_CORRECT (they rescale `total`), TIME_STYLE, a non-C locale reaching
ls, ACL/SELinux mode suffixes, device nodes, and a cache line longer than 1 MiB.

Also out of contract: -h/--help, a FIFO named like a desktop file in a
later application dir (the script blocks reading it), symlink loops, an empty-string argument (the script loops forever), XDG dirs or HOME containing ':' inside a default, glob characters or a quote,
\\u/\\U escapes beyond ASCII in a delimiter, and file names with bytes the shell would see differently in another
locale. On these the tool prints `MADO_TERM_OUT_OF_CONTRACT: <reason>` on stderr and exits 2. HOME unset is IN
contract and modelled as the pin does it: a default that needs HOME ($XDG_CONFIG_HOME or $XDG_DATA_HOME or
$XDG_CACHE_HOME empty, x:148/166/172) makes the resolver exit 1 with empty stdout, while all of them set lets it
run normally.
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


# --------------------------------------------------------- warm cache (inlined, verbatim) --
# xdg-terminal-exec constants (x:28-44): $XTE__RSEP, $XTE__USEP, the cache terminator, the cache "version".
RSEP = "\x1e"
USEP = "\x1f"
TERMINATOR = (RSEP + "END_OF_EXEC_USEP").encode()
CACHE_VERSION = b"4"
CACHE_LINE_LIMIT = 50           # x:224 xte__line_limit
CACHE_LINE_CAP = 1 << 20        # out-of-contract bound on one cache line

# ls constants
LS_BLOCK = 1024                 # default total unit off a terminal
ST_NBLOCKSIZE = 512
HALF_YEAR = 15778476            # 31556952 / 2 (x:205-ish: the six-month window of print_long_format)
DATE_WIDTH = 12
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

TYPE_CHAR = {stat.S_IFREG: "-", stat.S_IFDIR: "d", stat.S_IFLNK: "l", stat.S_IFCHR: "c",
             stat.S_IFBLK: "b", stat.S_IFIFO: "p", stat.S_IFSOCK: "s"}


class WarmOutOfContract(Exception):
    """A cache this module refuses to model (see the module docstring). Named apart from the tool's own
    OutOfContract so the module can be inlined into tools/mado-terminal.py without redefining it."""


# ------------------------------------------------------------------------------------------------ ids
def _owner(st_uid):
    try:
        return pwd.getpwuid(st_uid).pw_name.encode("utf-8", "surrogateescape")
    except KeyError:
        return str(st_uid).encode()


def _group(st_gid):
    try:
        return grp.getgrgid(st_gid).gr_name.encode("utf-8", "surrogateescape")
    except KeyError:
        return str(st_gid).encode()


# ------------------------------------------------------------------------------------------------ long format
def _mode(st_mode):
    out = TYPE_CHAR.get(stat.S_IFMT(st_mode), "?")
    bits = ((stat.S_IRUSR, "r"), (stat.S_IWUSR, "w"), (stat.S_IXUSR, "x"),
            (stat.S_IRGRP, "r"), (stat.S_IWGRP, "w"), (stat.S_IXGRP, "x"),
            (stat.S_IROTH, "r"), (stat.S_IWOTH, "w"), (stat.S_IXOTH, "x"))
    chars = [ch if st_mode & bit else "-" for bit, ch in bits]
    if st_mode & stat.S_ISUID:
        chars[2] = "s" if st_mode & stat.S_IXUSR else "S"
    if st_mode & stat.S_ISGID:
        chars[5] = "s" if st_mode & stat.S_IXGRP else "S"
    if st_mode & stat.S_ISVTX:
        chars[8] = "t" if st_mode & stat.S_IXOTH else "T"
    return out + "".join(chars)


def _date(st, now):
    """The 12-column date field: recent iff not in the future and inside the six-month window."""
    t = st.st_mtime
    tm = time.localtime(t)
    mon = MONTHS[tm.tm_mon - 1] if 1 <= tm.tm_mon <= 12 else "???"
    if t <= now and t > now - HALF_YEAR:
        return ("%s %2d %02d:%02d" % (mon, tm.tm_mday, tm.tm_hour, tm.tm_min)).encode()
    return ("%s %2d  %4d" % (mon, tm.tm_mday, tm.tm_year)).encode()


class _Widths(object):
    """Column widths of one block (GNU ls: per block, floor 1)."""

    def __init__(self, stats):
        self.nlink = self.owner = self.group = self.size = 1
        for st in stats:
            self.nlink = max(self.nlink, len(str(st.st_nlink)))
            self.owner = max(self.owner, len(_owner(st.st_uid)))
            self.group = max(self.group, len(_group(st.st_gid)))
            self.size = max(self.size, len(str(st.st_size)))


def _line(name, st, w, now, type_char="l"):
    if st is None:
        # stat failed under -L: only the type (from the dirent / an lstat) is known, the rest is '?'.
        return (type_char.encode() + b"?????????" + b" " + b"?".rjust(w.nlink) + b" " +
                b"?".ljust(w.owner) + b" " + b"?".ljust(w.group) + b" " + b"?".rjust(w.size) + b" " +
                b"?".rjust(DATE_WIDTH) + b" " + name + b"\n")
    return (_mode(st.st_mode).encode() + b" " + str(st.st_nlink).encode().rjust(w.nlink) + b" " +
            _owner(st.st_uid).ljust(w.owner) + b" " + _group(st.st_gid).ljust(w.group) + b" " +
            str(st.st_size).encode().rjust(w.size) + b" " + _date(st, now).rjust(DATE_WIDTH) +
            b" " + name + b"\n")


def _stat(path):
    try:
        return os.stat(path)        # -L: dereference
    except OSError:
        return None


def _display(name):
    """ls's `literal` quoting style: bytes verbatim, except LF printed as '?'."""
    return name.replace(b"\n", b"?")


def _type_char(de):
    """The mode's type letter when the entry cannot be stat'ed: GNU ls uses the dirent type (d_type)."""
    try:
        if de.is_symlink():
            return "l"
        if de.is_dir(follow_symlinks=False):
            return "d"
        if de.is_file(follow_symlinks=False):
            return "-"
    except OSError:
        pass
    try:
        mode = os.lstat(de.path).st_mode
    except OSError:
        return "?"
    return TYPE_CHAR.get(stat.S_IFMT(mode), "?")


def _join(parent, name):
    base = parent
    while len(base) > 1 and base.endswith(b"/"):
        base = base[:-1]
    return base + b"/" + name


class _Walker(object):
    def __init__(self, now):
        self.out = bytearray()
        self.first = True
        self.now = now
        self.stack = []

    def files_block(self, rows, widths):
        for name, st in rows:
            self.out += _line(_display(name), st, widths, self.now)
        if rows:
            self.first = False

    def dir_block(self, path, st, from_command_line):
        """One directory listing plus its recursion.

        A command-line directory operand emits the block separator BEFORE opendir (so an unreadable one
        leaves a bare separator); a recursive subdirectory opens first and only then emits it.
        """
        if from_command_line and not self.first:
            self.out += b"\n"
        try:
            names = os.listdir(path)
        except OSError:
            return
        if not from_command_line and not self.first:
            self.out += b"\n"
        self.out += _display(path) + b":\n"
        rows = []
        try:
            entries = list(os.scandir(path))
        except OSError:
            entries = []
        for de in entries:
            if de.name.startswith(b"."):
                continue
            rows.append((de.name, de.path, _stat(de.path), _type_char(de)))
        rows.sort(key=lambda r: r[0])
        widths = _Widths([r[2] for r in rows if r[2] is not None])
        total = sum(r[2].st_blocks for r in rows if r[2] is not None)
        self.out += b"total %d\n" % ((total * ST_NBLOCKSIZE + LS_BLOCK - 1) // LS_BLOCK)
        for nm, _p, cst, tc in rows:
            self.out += _line(_display(nm), cst, widths, self.now, tc)
        self.first = False
        self.stack.append((st.st_dev, st.st_ino))
        for _nm, p, cst, _tc in rows:
            if cst is None or not stat.S_ISDIR(cst.st_mode):
                continue
            if (cst.st_dev, cst.st_ino) in self.stack:
                continue
            self.dir_block(p, cst, False)
        self.stack.pop()


def ls_lRL(operands, now=None):
    """Bytes `LANG=C ls -LRl <operands>` writes to stdout (stderr dropped) in the C locale."""
    now = time.time() if now is None else now
    ops = [op for op in operands if op not in ("", None)]   # shell field splitting dropped these
    if not operands:
        ops = ["."]            # `ls -R` with no operand at all lists the current directory
    # (an explicitly empty operand - which the resolver's unquoted expansion never produces - is an
    #  "cannot access" error and prints nothing, so the list stays empty here)
    files, dirs = [], []
    for op in ops:
        raw = os.fsencode(op)
        st = _stat(raw)
        if st is None:
            continue
        (dirs if stat.S_ISDIR(st.st_mode) else files).append((raw, st))
    files.sort(key=lambda r: r[0])
    dirs.sort(key=lambda r: r[0])
    widths = _Widths([st for _n, st in files] + [st for _n, st in dirs])
    walker = _Walker(now)
    walker.files_block(files, widths)
    for raw, st in dirs:
        walker.dir_block(raw, st, True)
    return bytes(walker.out)


# ------------------------------------------------------------------------------------------------ hash
def hash_operands(configs, appdirs):
    """The operands of the hash `ls`: the non-empty ':'-fields of ${XTE__CONFIGS}:${XTE__APPLICATIONS_DIRS}."""
    return [p for p in (configs or "").split(":") + (appdirs or "").split(":") if p]


def gen_hash(desktop, configs, appdirs, now=None):
    """md5 of "4\\n<desktop>\\n" + `LANG=C ls -LRl` of the config and application paths (x:196-205)."""
    blob = bytearray(CACHE_VERSION + b"\n")
    blob += os.fsencode(desktop or "") + b"\n"
    blob += ls_lRL(hash_operands(configs, appdirs), now=now)
    return hashlib.md5(bytes(blob)).hexdigest()


# ------------------------------------------------------------------------------------------------ cache
class CacheRecord(object):
    """The cache file's fields, in file order (x:224-259)."""

    __slots__ = ("hash", "cmd", "entry_path", "entry_id", "entry_action", "execarg", "appidarg",
                 "titlearg", "dirarg", "holdarg", "exec_usep")

    def __init__(self, values):
        (self.hash, self.cmd, self.entry_path, self.entry_id, self.entry_action, self.execarg,
         self.appidarg, self.titlearg, self.dirarg, self.holdarg) = values
        self.exec_usep = ""

    def __repr__(self):
        return ("CacheRecord(hash=%r cmd=%r entry_path=%r entry_id=%r entry_action=%r execarg=%r "
                "appidarg=%r titlearg=%r dirarg=%r holdarg=%r exec_usep=%r)" %
                (self.hash, self.cmd, self.entry_path, self.entry_id, self.entry_action, self.execarg,
                 self.appidarg, self.titlearg, self.dirarg, self.holdarg, self.exec_usep))


def _cache_lines(path):
    """The lines `while IFS= read -r` would yield: split on LF, NULs dropped, a last fragment ignored."""
    try:
        with open(path, "rb") as fh:
            data = fh.read(CACHE_LINE_CAP + 1)
    except OSError:
        return None
    if len(data) > CACHE_LINE_CAP and b"\n" not in data[CACHE_LINE_CAP:]:
        raise WarmOutOfContract("cache line longer than %d bytes" % CACHE_LINE_CAP)
    data = data[:CACHE_LINE_CAP]
    parts = data.split(b"\n")
    parts.pop()                          # the fragment after the last LF is never read (`read` returns 1)
    return [p.replace(b"\x00", b"") for p in parts]


def read_cache(path):
    """(CacheRecord, None) or (None, "absent"|"unreadable"|"invalid") - the parse of x:217-298, no verdict."""
    try:
        st = os.stat(path)               # [ -f ]: a regular file, following symlinks
    except OSError:
        return None, "absent"
    if not stat.S_ISREG(st.st_mode):
        return None, "absent"
    lines = _cache_lines(path)
    if lines is None:
        return None, "unreadable"        # the redirection fails: `set -e` ends the resolver here
    fields = []
    command = []                         # lines 11+; a leading empty line adds nothing (the shell's `:+`)
    finished = False
    for num, line in enumerate(lines, 1):
        if num <= 10:
            fields.append(line)
            continue
        if num >= CACHE_LINE_LIMIT:
            return None, "invalid"       # x:225-227: the limit branch precedes the command branch
        if command or line:
            command.append(line)
        if line.endswith(TERMINATOR):
            command[-1] = command[-1][:len(command[-1]) - len(TERMINATOR)]
            finished = True
            break
    if not finished:
        return None, "invalid"
    rec = CacheRecord([f.decode("utf-8", "surrogateescape") for f in fields])
    rec.exec_usep = "\n".join(p.decode("utf-8", "surrogateescape") for p in command)
    return rec, None
# --------------------------------------------------------- end of the warm-cache block --------


class OutOfContract(Exception):
    pass


class Exit(Exception):
    def __init__(self, rc):
        super().__init__(rc)
        self.rc = rc


class HomeUnset(Exception):
    """A default needed $HOME and the environment has none: the pin exits 1 with empty stdout."""


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


def desktops(env):
    """XDG_CURRENT_DESKTOP with ASCII upper case lowered, trailing newlines dropped (x:1144)."""
    dsk = env.get("XDG_CURRENT_DESKTOP", "")
    return split_ifs("".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in dsk).rstrip("\n"), ":")


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

    def _xdg(self, key, default):
        """${KEY:-<HOME>default}: HOME is needed only when the default is (x:148,166,172)."""
        v = self.env.get(key)
        if v:
            return v
        if "HOME" not in self.env:
            raise HomeUnset("HOME: unbound variable (x:%d, exit 1, empty stdout)"
                            % {"XDG_CONFIG_HOME": 148, "XDG_DATA_HOME": 166, "XDG_CACHE_HOME": 172}[key])
        return self.env["HOME"] + default

    def make_paths(self):
        e = self.env
        for k in ("XDG_CONFIG_HOME", "XDG_CONFIG_DIRS", "XDG_DATA_HOME", "XDG_DATA_DIRS"):
            v = e.get(k, "")
            if any(c in v for c in "[]*?\\'\""):
                raise OutOfContract("%s holds a glob character or a quote" % k)
        if "HOME" in e and any(c in e["HOME"] for c in ":[]*?\\'\""):
            raise OutOfContract("HOME holds ':' a glob character or a quote")
        cfg = self._xdg("XDG_CONFIG_HOME", "/.config") + ":" + (e.get("XDG_CONFIG_DIRS") or "/etc/xdg")
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
        for d in split_ifs(self._xdg("XDG_DATA_HOME", "/.local/share") + ":" + data, ":"):
            d = d[:-1] if d.endswith("/") else d
            apps.insert(0, d + "/applications/")
        self.app_dirs = apps
        self.cache_file = self._xdg("XDG_CACHE_HOME", "/.cache") + "/xdg-terminal-exec"

    def load_cache(self):
        """x:217-298 as a resolver step: True on a hit (the cached values are adopted), else sets cache_state."""
        try:
            rec, reason = read_cache(self.cache_file)
        except WarmOutOfContract as ex:
            raise OutOfContract(str(ex))
        if rec is None:
            self.cache_state = reason
            self.t("cache %s: %s, cold path" % (self.cache_file, reason))
            return False
        fresh = gen_hash(self.env.get("XDG_CURRENT_DESKTOP", ""), ":".join(self.configs),
                         ":".join(self.app_dirs))
        if rec.hash != fresh:
            self.cache_state = "stale"
            self.t("cache %s: out-of-date (line 1 md5 %s, this tree hashes to %s)" %
                   (self.cache_file, rec.hash, fresh))
            return False
        if not self.command_v(rec.cmd):
            self.cache_state = "stale"
            self.t("cache %s: out-of-date (cached command %r does not resolve)" % (self.cache_file, rec.cmd))
            return False
        self.cache_state = "hit"
        self.exec_usep = rec.exec_usep
        self.entry_path, self.entry_id, self.entry_action = rec.entry_path, rec.entry_id, rec.entry_action
        self.execarg, self.appidarg, self.titlearg = rec.execarg, rec.appidarg, rec.titlearg
        self.dirarg, self.holdarg = rec.dirarg, rec.holdarg
        self.is_terminal = True
        self.t("cache %s: hit, entry %s, command %r, %d exec word(s)" %
               (self.cache_file, rec.entry_id, rec.cmd, len(split_ifs(rec.exec_usep, USEP))))
        return True

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

    def select(self):
        e = self.env
        self.desktops_lower = desktops(e)
        self.compat = e.get("XTE_EXECARG_COMPAT", "true")
        self.compat_configured = e.get("XTE_EXECARG_COMPAT", "") != ""
        self.cache_enabled = e.get("XTE_CACHE_ENABLED", "true")
        self.cache_configured = e.get("XTE_CACHE_ENABLED", "") != ""
        self.entry_ids, self.excluded, self.included, self.execarg_defaults = [], [], [], []
        self.aliases = {}
        self.cache_used = False
        self.cache_state = None
        self.reset_keys()
        self.make_paths()
        if not check_bool(self.cache_enabled, self.err):
            self.cache_state = "disabled"
            self.t("cache %s: disabled by XTE_CACHE_ENABLED=%r, cold path" % (self.cache_file, self.cache_enabled))
        elif self.load_cache():
            self.cache_used = True
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
    except HomeUnset as ex:
        return "", 1, [str(ex)]
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
        except IsADirectoryError:
            text = ""       # `shcat < dir`: the redirection opens, every `read` fails, shcat returns 0 (x:1362)
        except OSError as ex:
            # `shcat < "${XTE__ENTRY_PATH}"` (x:1362): a failed redirection ends the script under `set -e`
            return "".join(out), 1, r.stderr + ["%s: %s" % (r.entry_path, ex.strerror or "cannot read")]
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
    except HomeUnset as ex:
        ok = False
        r.t("make_paths: %s, the resolver exits 1 with empty stdout" % ex)
    print("MADO_TERM_DESKTOPS: %s" % (":".join(r.desktops_lower) or "-"))
    for line in r.trace:
        print("MADO_TERM_TRACE: %s" % line)
    if r.cache_state is not None:
        cache = r.cache_state
    elif not check_bool(r.cache_enabled, lambda _m: None):
        cache = "disabled"
    else:
        cache = "absent"
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


# ----------------------------------------------------------------- warm-cache selftest machinery
def _pin(root, ts=1546300800):
    """Freeze every mtime under root: the hash's date column then never moves with the wall clock."""
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        for nm in dirnames + filenames + ["."]:
            p = os.path.join(dirpath, nm)
            try:
                os.utime(p, (ts, ts), follow_symlinks=False)
            except OSError:
                pass


def _hash_for(env):
    """The hash this tree has, over the paths this environment builds (x:143-215)."""
    r = Resolver(env)
    r.desktops_lower = desktops(env)
    r.make_paths()
    return gen_hash(env.get("XDG_CURRENT_DESKTOP", ""), ":".join(r.configs), ":".join(r.app_dirs))


def _cache_text(env, **fields):
    """A cache file exactly as save_cache writes it (x:313-333), with individual fields overridden."""
    rec = {"hash": _hash_for(env), "cmd": "foot", "entry_path": None, "entry_id": "foot.desktop",
           "entry_action": "", "execarg": "-e", "appidarg": "", "titlearg": "", "dirarg": "",
           "holdarg": "", "exec_usep": "kitty" + USEP + "--warm"}
    rec["entry_path"] = os.path.join(env.get("XDG_DATA_DIRS") or env["XDG_DATA_HOME"],
                                     "applications", "foot.desktop")
    rec.update(fields)
    lines = [rec[k] for k in ("hash", "cmd", "entry_path", "entry_id", "entry_action", "execarg",
                              "appidarg", "titlearg", "dirarg", "holdarg")]
    return "".join(x + "\n" for x in lines) + rec["exec_usep"] + RSEP + "END_OF_EXEC_USEP\n"


def _no_terminator(env, **fields):
    return _cache_text(env, **fields).rsplit(RSEP, 1)[0]


def _terminator_on(env, line, **fields):
    """A cache whose command block reaches the terminator exactly on <line> (10 fields, so 11..line-1 empty)."""
    return _cache_text(env, exec_usep="\n" * (line - 11) + "kitty" + USEP + "--warm", **fields)


def _warm_case(name, files, execs, args, want_out, want_rc, warm, **envkw):
    return (name, files, execs, args, want_out, want_rc, envkw, warm)


def selftest_warm_cases():
    """(name, files, execs, args, want_stdout, want_rc, env overrides, cache builder)."""
    cases = []
    A = "usr/share/applications/"
    L = "home/.config/xdg-terminals.list"
    entry = _term("foot")
    files = {A + "foot.desktop": entry, L: "foot.desktop\n"}
    ex = ["bin/foot", "bin/kitty"]
    hit = "kitty\n--warm\n"
    cold = "foot\n"
    P = "$ROOT/usr/share/applications/foot.desktop"

    cases.append(_warm_case("cache-hit-cmd", files, ex, ["--print-cmd"], hit, 0,
                            lambda env: _cache_text(env)))
    cases.append(_warm_case("cache-hit-beats-entry", dict(files), ex, ["--print-cmd"], hit, 0,
                            lambda env: (_pin(env["HOME"]), _cache_text(env))[1]))
    cases.append(_warm_case("cache-hit-id-path-action", files, ex, ["--print-id", "--print-path"],
                            "cached.desktop:act\n" + P + ":act\n", 0,
                            lambda env: _cache_text(env, entry_id="cached.desktop", entry_action="act")))
    cases.append(_warm_case("cache-stale-hash", files, ex, ["--print-cmd"], cold, 0,
                            lambda env: _cache_text(env, hash="0" * 32)))
    cases.append(_warm_case("cache-absent", files, ex, ["--print-cmd"], cold, 0, None))
    cases.append(_warm_case("cache-invalid-no-terminator", files, ex, ["--print-cmd"], cold, 0,
                            lambda env: _no_terminator(env)))
    cases.append(_warm_case("cache-invalid-line50", files, ex, ["--print-cmd"], cold, 0,
                            lambda env: _terminator_on(env, 50)))
    cases.append(_warm_case("cache-line49-is-valid", files, ex, ["--print-cmd"], hit, 0,
                            lambda env: _terminator_on(env, 49)))
    cases.append(_warm_case("cache-cmd-unresolved", files, ex, ["--print-cmd"], cold, 0,
                            lambda env: _cache_text(env, cmd="nosuchtool")))
    cases.append(_warm_case("cache-cmd-script-function", files, ex, ["--print-cmd"], hit, 0,
                            lambda env: _cache_text(env, cmd="gen_hash")))
    cases.append(_warm_case("cache-disabled-env", files, ex, ["--print-cmd"], cold, 0,
                            lambda env: _cache_text(env), **{"XTE_CACHE_ENABLED": "false"}))
    cases.append(_warm_case("cache-directive-disable-still-hits", {A + "foot.desktop": entry,
                                                                   L: "/disable_cache\nfoot.desktop\n"},
                            ex, ["--print-cmd"], hit, 0, lambda env: _cache_text(env)))
    cases.append(_warm_case("cache-content-missing-path", files, ex, ["--print-id", "--print-content"],
                            "foot.desktop\n", 1,
                            lambda env: _cache_text(env, entry_path="/nonexistent/x.desktop")))
    cases.append(_warm_case("cache-content-hit", files, ex, ["--print-content"], entry, 0,
                            lambda env: _cache_text(env)))
    cases.append(_warm_case("cache-hit-newline-in-exec", files, ex, ["--print-cmd"],
                            "kitty\na\nb\n", 0,
                            lambda env: _cache_text(env, exec_usep="kitty" + USEP + "a\nb")))
    cases.append(_warm_case("cache-hit-skips-unreadable-list", files, ex, ["--print-cmd"], hit, 0,
                            lambda env: (_pin(env["HOME"]),
                                         os.chmod(os.path.join(env["HOME"], ".config/xdg-terminals.list"), 0o000),
                                         _cache_text(env))[2]))
    cases.append(_warm_case("cache-hit-args-from-entry-keys",
                            {A + "foot.desktop": _term("foot", "X-TerminalArgTitle=--title\n"
                                                       "X-TerminalArgHold=--hold\n"),
                             L: "foot.desktop\n"}, ex,
                            ["--print-cmd", "--title=T", "--hold"],
                            "kitty\n--warm\n--title\nT\n--hold\n", 0,
                            lambda env: _cache_text(env, titlearg="--title", holdarg="--hold")))
    cases.append(_warm_case("home-unset-default-needed", files, ex, ["--print-id"], "", 1, None,
                            **{"HOME": None, "XDG_CONFIG_HOME": None}))
    cases.append(_warm_case("home-unset-all-xdg-set", files, ex, ["--print-id"], "foot.desktop\n", 0, None,
                            **{"HOME": None}))
    return cases


def _env_for(root, envkw):
    envkw = dict(envkw)
    desk = envkw.pop("desk", "Hyprland")
    env = _env(root, desk, **{k: v for k, v in envkw.items() if v is not None})
    for k, v in envkw.items():
        if v is None:
            env.pop(k, None)
    return env


def selftest():
    base = tempfile.mkdtemp(prefix="mado-terminal-selftest.", dir=os.environ.get("TMPDIR") or None)
    cases = [(c[0], c[1], c[2], c[3], c[4], c[5], c[6], None) for c in selftest_cases()]
    cases += selftest_warm_cases()
    passed = 0
    fails = 0
    try:
        for i, (name, files, execs, args, want_out, want_rc, envkw, warm) in enumerate(cases):
            root = os.path.join(base, "c%02d" % i)
            os.makedirs(root + "/home", exist_ok=True)
            os.makedirs(root + "/cache", exist_ok=True)
            _mk(root, files, execs)
            env = _env_for(root, envkw)
            if warm is not None:
                _pin(root)
                text = warm(env)
                if text is not None:
                    with open(os.path.join(root, "cache", "xdg-terminal-exec"), "wb") as fh:
                        fh.write(text.encode("latin-1", "surrogateescape"))
            try:
                got, rc, _err = run_print(env, args, cwd=root)
            except OutOfContract as ex:
                got, rc = "OOC:%s" % ex, 2
            want = want_out.replace("$ROOT", root)
            if got == want and rc == want_rc:
                passed += 1
            else:
                fails += 1
                print("MADO_TERMINAL_SELFTEST_FAIL: %s got=%r rc=%d want=%r rc=%d" % (name, got, rc, want, want_rc))
        for name, files, execs, envkw, warm, want_cache, want_verdict, want_rc in selftest_explain_cases():
            root = os.path.join(base, "x%02d" % passed)
            os.makedirs(root + "/home", exist_ok=True)
            os.makedirs(root + "/cache", exist_ok=True)
            _mk(root, files, execs)
            env = _env_for(root, envkw)
            if warm is not None:
                _pin(root)
                with open(os.path.join(root, "cache", "xdg-terminal-exec"), "wb") as fh:
                    fh.write(warm(env).encode("latin-1", "surrogateescape"))
            import contextlib
            import io
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = explain(env, None)
            line = [x for x in buf.getvalue().split("\n") if x.startswith("MADO_TERM: ")]
            got = (line[-1] if line else "")
            parts = dict(kv.split("=", 1) for kv in got[len("MADO_TERM: "):].split() if "=" in kv)
            if parts.get("cache") == want_cache and parts.get("verdict") == want_verdict and rc == want_rc:
                passed += 1
            else:
                fails += 1
                print("MADO_TERMINAL_SELFTEST_FAIL: %s cache=%r verdict=%r rc=%d want cache=%r verdict=%r rc=%d"
                      % (name, parts.get("cache"), parts.get("verdict"), rc, want_cache, want_verdict, want_rc))
    finally:
        import shutil
        shutil.rmtree(base, ignore_errors=True)
    print("MADO_TERMINAL_SELFTEST: %d/%d passed" % (passed, passed + fails))
    return 0 if fails == 0 else 1

def selftest_explain_cases():
    """(name, files, execs, env overrides, cache builder, want cache=, want verdict=, want rc)."""
    A = "usr/share/applications/"
    L = "home/.config/xdg-terminals.list"
    files = {A + "foot.desktop": _term("foot"), L: "foot.desktop\n"}
    ex = ["bin/foot", "bin/kitty"]
    return [
        ("explain-cache-absent", files, ex, {}, None, "absent", "OK", 0),
        ("explain-cache-hit", files, ex, {}, lambda env: _cache_text(env), "hit", "OK", 0),
        ("explain-cache-stale", files, ex, {}, lambda env: _cache_text(env, hash="f" * 32), "stale", "OK", 0),
        ("explain-cache-invalid", files, ex, {}, lambda env: _no_terminator(env), "invalid", "OK", 0),
        ("explain-cache-disabled", files, ex, {"XTE_CACHE_ENABLED": "0"},
         lambda env: _cache_text(env), "disabled", "OK", 0),
        ("explain-no-terminal", {A + "x.desktop": "[Desktop Entry]\n"}, [], {}, None, "absent",
         "NO_TERMINAL", 3),
    ]



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
        sys.stdout.buffer.write(out.encode("latin-1", "surrogateescape"))
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

#!/usr/bin/env python3
"""warmcache.py - the WARM-CACHE path of xdg-terminal-exec v0.14.3, as a stdlib-only module.

Read-only. Starts no process, opens no socket, writes no file. Python 3 standard library only.

The resolver modelled is xdg-terminal-exec v0.14.3 (upstream tag v0.14.3, script sha256
89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac = this host's /usr/bin/xdg-terminal-exec).
"x:N" below are lines of that script.

API
---
  ls_lRL(operands, now=None) -> bytes
      Exactly what `LANG=C ls -LRl <operands>` writes to stdout in the C locale, with stderr dropped: the
      bytes the resolver hashes at x:179-215. Called under LC_ALL=C (gen_hash re-execs itself, x:183-187), so
      the collation, the month names, the `?` substitutions and the quoting style are all the C-locale ones.
  gen_hash(desktop, configs, appdirs, now=None) -> str
      md5 over b"4\\n" + desktop + b"\\n" + ls_lRL(<fields of configs:appdirs>) (x:196-205), lower-case hex.
      desktop = XDG_CURRENT_DESKTOP verbatim (raw, not lower-cased); configs = XTE__CONFIGS, appdirs =
      XTE__APPLICATIONS_DIRS, both the colon-joined strings the resolver builds at x:143-174.
  read_cache(path) -> (record, reason)
      Parse $XDG_CACHE_HOME/xdg-terminal-exec as x:217-298 reads it. record is a CacheRecord on success
      (reason None); otherwise record is None and reason is
        "absent"     [ -f ] fails: not a regular file (a directory or FIFO is not a cache), x:221
        "unreadable" the file exists but cannot be opened: the shell's redirection at the `done <` fails, the
                     loop body never runs, and read_cache returns 1 - a COLD path, because read_cache sits in
                     an `&&` list where `set -e` does not apply (x:1179)
        "invalid"    a line-11+ terminator was never reached, or line 50 was reached (x:223-259) Whether the record is still
      TRUE is not this function's business: compare record.hash with gen_hash(...) and resolve record.cmd with
      `command -v`; only then is it a hit (x:283-288).

CacheRecord fields (x:224-259), in file order: hash(1) cmd(2) entry_path(3) entry_id(4) entry_action(5)
execarg(6) appidarg(7) titlearg(8) dirarg(9) holdarg(10) exec_usep(11+.  joined by newlines, terminator
stripped). exec_usep is the raw $XTE__USEP-separated (0x1f) command, newlines included.

What is modelled, and the observations behind it (each one checked against /usr/bin/ls = GNU coreutils 9.12;
receipts/hash-agree.txt and receipts/ls-diff-*.txt of this seat):

  * -L dereferences everything first. An entry whose stat() fails then is printed as `l?????????` with '?' in
    every field, padded like a real one; a dangling operand is dropped entirely (stderr) and takes part in
    nothing.
  * Operands are split into non-directories and directories. Files print first (one line each, name as given),
    then the directories, each group sorted by raw bytes (C collation). A directory block is `<path>:` ,
    `total N`, then its entries sorted by raw name bytes.
  * Column widths are per block: the file block's widths are taken over ALL operands (a directory operand
    widens the size column of the file lines even though it prints no line), a directory block's widths over
    its own entries. nlink/owner/group/size are at least 1 wide; `?` is right-aligned in nlink/size/date and
    left-aligned in owner/group.
  * `total N` = sum of st_blocks over the stat'ed entries, rounded UP to 1 KiB units (human_readable with
    ceiling from ST_NBLOCKSIZE=512, the default block size off a terminal). A symlink under -L contributes its
    target's blocks, a dangling one nothing.
  * Dates: 12 columns, "%b %e %H:%M" when the mtime is within the last 31556952/2 = 15778476 s AND not in the
    future, else "%b %e  %Y" (English month names: the C locale). Local time (TZ, else /etc/localtime, else
    UTC - the counter's sandbox has no /etc, so UTC).
  * Header path = the operand as typed, trailing slashes kept (`d/:`); a subdirectory's header is the parent
    header path with its trailing slashes removed, '/' and the entry name (`d/sub:`, `./d/sub:`, `d/./s1:`).
  * A blank line separates blocks. It is emitted by a directory ATTEMPT: a command-line directory operand that
    cannot be opened yields the separator (when it is not the first block) and then nothing at all - no
    header; a subdirectory that cannot be opened yields stderr only, no separator. A cycle (a symlink to an
    ancestor directory, tracked by (st_dev, st_ino) on the current path) is skipped with no output; a symlink
    to an already-listed directory that is NOT an ancestor is listed again (no global de-duplication).
  * Dot files are not listed and dot directories are not entered (-a is not given).
  * Names are printed literally (stdout is a pipe in the resolver, so the default quoting style is `literal`):
    every byte verbatim except LF, which is printed as '?'. Mode strings carry no ACL '+' / context '.'.
  * owner/group are the passwd/group names when they resolve, else the number - which is what an ls with no
    /etc/passwd visible (the counter's sandbox) prints, and what a host without those ids prints.

Out of contract (not modelled; `ls_lRL` gives the default-locale answer, which is the resolver's because
gen_hash forces LC_ALL=C): BLOCKSIZE / LS_BLOCK_SIZE / POSIXLY_CORRECT (they rescale `total`), TIME_STYLE
(it reshapes the date), QUOTING_STYLE / --quoting-style, COLUMNS, a non-C locale reaching ls anyway, ACLs and
SELinux labels (the '+' / '.' mode suffix), device nodes (they print "major, minor" instead of a size), a
file name whose lstat also fails (ls prints `??????????`, this module `l?????????`), a cache line longer than
CACHE_LINE_CAP bytes, and a cache containing a NUL byte (bash's `read` drops NULs; this module does too,
which is modelled, but a NUL can never be *compared* faithfully through a shell variable).
"""

import grp
import hashlib
import os
import pwd
import stat
import time

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

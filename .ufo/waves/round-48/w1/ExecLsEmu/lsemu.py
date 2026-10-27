"""Byte-exact emulation of GNU ``LC_ALL=C LANG=C ls -LRl OP...`` (Python 3 stdlib only).

Why this exists
---------------
``xdg-terminal-exec`` v0.14.3 decides whether its cache is still valid by
hashing the output of

    LC_ALL=C LANG=C ls -LRl <config dirs> <app dirs> 2>/dev/null

(``gen_hash``, /usr/bin/xdg-terminal-exec:179-215).  A read-only model of that
resolver therefore needs this exact byte stream without starting a process.

Provenance
----------
Every rule below was taken from the *source* of the implementation on this
host, not guessed:

  coreutils 9.12-2 (/usr/bin/ls, "ls (GNU coreutils) 9.12")
    src/ls.c      sha256 936768065464ccc85b3084594ea2bca5b0cbc3786bcf5e7ca26ffbe93a0d1e4d
    lib/filemode.c, lib/file-has-acl.c, lib/human.c, lib/cycle-check.c
    (tarball https://ftp.gnu.org/gnu/coreutils/coreutils-9.12.tar.xz,
     sha256 a480198559733e9b3da999e90543ac6f888a2caa544d8d664c5a1f17e528e210)

Public API
----------
    ls_lRL(operands, now=None) -> bytes
        stdout only -- the bytes that reach gen_hash.
    ls_lRL_full(operands, now=None, cwd=None) -> (stdout, stderr, rc)
        the whole observable behaviour (stderr quoting is best effort, see
        ``_err_quote``; it is discarded by the resolver anyway).

No process is started, no socket is opened, nothing is written: the model only
stats, reads symlinks, reads directory entries and reads xattrs.

Deliberately out of contract (documented in the seat report, with the reason):
POSIXLY_CORRECT / LS_BLOCK_SIZE / BLOCK_SIZE / TIME_STYLE / QUOTING_STYLE /
TABSIZE / COLUMNS / LS_COLORS in the environment, ``--dired``, and mtimes whose
year is outside 1000..9999.
"""

import errno
import os
import stat as _stat
import time

__all__ = ["ls_lRL", "ls_lRL_full"]

# coreutils ls.c: long_time_format[0] = "%b %e  %Y", [1] = "%b %e %H:%M";
# six_months = 31556952 / 2 (ls.c print_long_format).
_MONTH = (b"Jan", b"Feb", b"Mar", b"Apr", b"May", b"Jun",
          b"Jul", b"Aug", b"Sep", b"Oct", b"Nov", b"Dec")
_SIX_MONTHS = 31556952 // 2          # 15778476
_ACL_ACCESS = b"system.posix_acl_access"
_ACL_DEFAULT = b"system.posix_acl_default"
_SCONTEXT = b"security.selinux"

# ls.c: enum acl_type
ACL_NONE, ACL_LSM, ACL_YES, ACL_UNKNOWN = 0, 1, 2, 3

_S_IRUSR, _S_IWUSR, _S_IXUSR = _stat.S_IRUSR, _stat.S_IWUSR, _stat.S_IXUSR
_S_IRGRP, _S_IWGRP, _S_IXGRP = _stat.S_IRGRP, _stat.S_IWGRP, _stat.S_IXGRP
_S_IROTH, _S_IWOTH, _S_IXOTH = _stat.S_IROTH, _stat.S_IWOTH, _stat.S_IXOTH


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _quote(name):
    """ls.c quote_name_buf with the non-tty default (literal + qmark_newline).

    ``qmark_funny_chars`` is false when stdout is not a tty, so no other byte
    is touched: only '\\n' becomes '?' (``extra_newline_protection``).
    """
    return name.replace(b"\n", b"?")


def _mode_string(mode):
    """lib/filemode.c strmode(): 11 bytes, last one a space."""
    if _stat.S_ISREG(mode):
        t = b"-"
    elif _stat.S_ISDIR(mode):
        t = b"d"
    elif _stat.S_ISBLK(mode):
        t = b"b"
    elif _stat.S_ISCHR(mode):
        t = b"c"
    elif _stat.S_ISLNK(mode):
        t = b"l"
    elif _stat.S_ISFIFO(mode):
        t = b"p"
    elif _stat.S_ISSOCK(mode):
        t = b"s"
    else:
        t = b"?"
    out = bytearray(11)
    out[0:1] = t
    out[1] = 0x72 if mode & _S_IRUSR else 0x2D
    out[2] = 0x77 if mode & _S_IWUSR else 0x2D
    out[3] = (0x73 if mode & _S_IXUSR else 0x53) if mode & _stat.S_ISUID else (
        0x78 if mode & _S_IXUSR else 0x2D)
    out[4] = 0x72 if mode & _S_IRGRP else 0x2D
    out[5] = 0x77 if mode & _S_IWGRP else 0x2D
    out[6] = (0x73 if mode & _S_IXGRP else 0x53) if mode & _stat.S_ISGID else (
        0x78 if mode & _S_IXGRP else 0x2D)
    out[7] = 0x72 if mode & _S_IROTH else 0x2D
    out[8] = 0x77 if mode & _S_IWOTH else 0x2D
    out[9] = (0x74 if mode & _S_IXOTH else 0x54) if mode & _stat.S_ISVTX else (
        0x78 if mode & _S_IXOTH else 0x2D)
    out[10] = 0x20
    return bytes(out)


def _type_letter(mode):
    return _mode_string(mode)[0:1]


class _Ent:
    __slots__ = ("name", "st", "letter", "acl", "is_arg_dir")

    def __init__(self, name, st, letter, acl):
        self.name = name
        self.st = st
        self.letter = letter
        self.acl = acl
        self.is_arg_dir = False


class _W:
    """Column widths of one block; ls.c clear_files() reset semantics."""

    __slots__ = ("nlink", "owner", "group", "size", "major", "minor", "any_acl")

    def __init__(self):
        self.nlink = 0
        self.owner = 0
        self.group = 0
        self.size = 0
        self.major = 0
        self.minor = 0
        self.any_acl = False


def _user_name(uid):
    """ls.c getuser(): name if passwd resolves, else None (numeric fallback)."""
    try:
        import pwd
        return os.fsencode(pwd.getpwuid(uid).pw_name)
    except (KeyError, ImportError, OverflowError):
        return None


def _group_name(gid):
    try:
        import grp
        return os.fsencode(grp.getgrgid(gid).gr_name)
    except (KeyError, ImportError, OverflowError):
        return None


def _acl_type(full, isdir):
    """lib/file-has-acl.c (Linux xattr path) + ls.c ACL_T_* selection."""

    def has(name):
        try:
            os.getxattr(full, name)
            return 1
        except OSError as exc:
            if exc.errno in (errno.EACCES, errno.EPERM):
                return -1
            return 0

    access = has(_ACL_ACCESS)
    default = has(_ACL_DEFAULT) if isdir else 0
    scontext = has(_SCONTEXT)
    have_acl = access > 0 or default > 0
    if have_acl:
        return ACL_YES
    if access < 0 or default < 0:
        return ACL_UNKNOWN
    if scontext > 0:
        return ACL_LSM
    return ACL_NONE


def _fmt_time(t, recent):
    """nstrftime of ls.c long_time_format[recent] in the C locale."""
    tm = time.localtime(t)
    stamp = _MONTH[tm.tm_mon - 1] + b" " + (b"%2d" % tm.tm_mday) + b" "
    if recent:
        return stamp + (b"%02d:%02d" % (tm.tm_hour, tm.tm_min))
    return stamp + b" " + str(tm.tm_year).encode()


# ---- gnulib quotearg emulation (only for stderr text) --------------------
# quotef() = quotearg_n_style_colon(0, shell_escape_quoting_style) -- colon marked
# quoteaf() = quotearg_style(shell_escape_always_quoting_style)
# Characters that do not force outer quoting (ls/quotearg.c): the safe list,
# plus '?', '@' and '\\' which fall through to the no-op default.
# '\\' is *not* here: in shell_escape (quotef) it forces outer quoting, and it
# is not C-compatible either; only inside the quoted form is it stored raw.
_NOFORCE = frozenset(
    b"%+,-./0123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ]_?"
    b"abcdefghijklmnopqrstuvwxyz@")
_SHELL_FORCE = frozenset(b'!"$&()*;<=>[^`| ')
# Characters that are compatible with *both* C and shell quoting: this exact
# set decides whether an apostrophe is rendered with C quotes instead.
_C_SAFE = frozenset(
    b"%+,-./0123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ]_"
    b"abcdefghijklmnopqrstuvwxyz")


def _needs_shell_quoting(name, colon):
    n = len(name)
    for i, c in enumerate(name):
        if c in _NOFORCE:
            if colon and c == 0x3A:           # quotef() marks ':'
                return True
            continue
        if c in (0x23, 0x7E) and i != 0:      # '#' '~' only at position 0
            continue
        if c in (0x7B, 0x7D) and n != 1:      # '{' '}' only when isolated
            continue
        return True
    return n == 0


def _all_c_and_shell_compat(name):
    n = len(name)
    for i, c in enumerate(name):
        if c in _C_SAFE or c == 0x20 or c == 0x27:
            continue
        if (c == 0x23 or c == 0x7E) and i == 0:
            continue
        if c in (0x7B, 0x7D) and n == 1:
            continue
        return False
    return True


def _shell_quote(name, always=False, colon=False):
    """gnulib shell_escape[_always] quoting (quotearg_buffer_restyled)."""
    if not always and not _needs_shell_quoting(name, colon):
        return name
    # concise form: an apostrophe alone is rendered with C quotes when every
    # byte is compatible with both C and shell quoting (quotearg.c tail).
    if 0x27 in name and _all_c_and_shell_compat(name):
        return b'"' + name + b'"'
    out = bytearray(b"'")
    pending = False
    for c in name:
        if c == 0x27:                    # ' -> '\'' (case body + store_c)
            out += b"'\\''"
            pending = False
            continue
        if c == 0x0A:
            esc = b"\\n"
        elif c == 0x0D:
            esc = b"\\r"
        elif c == 0x09:
            esc = b"\\t"
        elif 0x20 <= c < 0x7F:
            esc = None
        else:
            esc = b"\\%03o" % c
        if esc is None:
            if pending:
                out += b"''"
                pending = False
            out.append(c)
        else:
            if not pending:
                out += b"'$'"
                pending = True
            out += esc
    out += b"'"                       # END_ESC never fires at end of string
    return bytes(out)


def _quoteaf(name):
    return _shell_quote(name, always=True)


def _quotef(name):
    return _shell_quote(name, always=False, colon=True)


def _concat(dirname, name):
    """gnulib file_name_concat(): dirname + '/' + name, honouring a trailing '/'."""
    if not dirname:
        return name
    if dirname.endswith(b"/"):
        return dirname + name
    return dirname + b"/" + name


def _attach(dirname, name):
    """ls.c attach(): like _concat, except a dirname of exactly "." is dropped."""
    if dirname == b".":
        return name
    return _concat(dirname, name)


class _Ctx:
    __slots__ = ("out", "err", "status", "now", "root", "active", "first_header",
                 "time_width")

    def __init__(self, now, root):
        self.out = bytearray()
        self.err = bytearray()
        self.status = 0
        self.now = now
        self.root = root
        self.active = set()
        self.first_header = True
        self.time_width = None

    def fail(self, serious, message, full, exc):
        self.err += b"ls: " + message + b" " + _quoteaf(full) + b": " \
            + os.strerror(exc.errno or errno.EIO).encode() + b"\n"
        if serious:
            self.status = 2
        elif self.status == 0:
            self.status = 1

    def full(self, path):
        if path.startswith(b"/"):
            return path
        return os.path.join(self.root, path)


# --------------------------------------------------------------------------
# gobble_file()
# --------------------------------------------------------------------------

def _gobble(ctx, name, disp, command_line, w):
    """ls.c gobble_file() for -L -l.  Returns (entry|None, blocks).

    ``disp`` is the path as ls prints it (operand text, or dirname + '/' + name);
    the filesystem lookup is relative to the model's cwd.
    """
    full = ctx.full(disp)
    try:
        st = os.stat(full)
    except OSError as exc:
        if not command_line and exc.errno == errno.ENOENT:
            try:
                lst = os.lstat(full)
            except OSError:
                return None, 0            # vanished: silent drop
            if _stat.S_ISLNK(lst.st_mode):
                # dangling symlink: kept, stat-less, message is minor
                ctx.fail(False, b"cannot access", disp, exc)
                return _Ent(name, None, b"l", ACL_NONE), 0
            return None, 0
        ctx.fail(command_line, b"cannot access", disp, exc)
        if command_line:
            return None, 0
        try:
            lst = os.lstat(full)
            letter = _type_letter(lst.st_mode)
        except OSError:
            letter = b"?"
        return _Ent(name, None, letter, ACL_NONE), 0

    mode = st.st_mode
    isdir = _stat.S_ISDIR(mode)
    acl = _acl_type(full, isdir)
    if acl != ACL_NONE:
        w.any_acl = True

    nlink_len = len(str(st.st_nlink).encode())
    if w.nlink < nlink_len:
        w.nlink = nlink_len

    user = _user_name(st.st_uid)
    ulen = len(user) if user is not None else len(str(st.st_uid).encode())
    if w.owner < ulen:
        w.owner = ulen
    group = _group_name(st.st_gid)
    glen = len(group) if group is not None else len(str(st.st_gid).encode())
    if w.group < glen:
        w.group = glen

    if _stat.S_ISCHR(mode) or _stat.S_ISBLK(mode):
        maj, min_ = os.major(st.st_rdev), os.minor(st.st_rdev)
        mlen, nlen = len(str(maj).encode()), len(str(min_).encode())
        if w.major < mlen:
            w.major = mlen
        if w.minor < nlen:
            w.minor = nlen
        if w.size < w.major + 2 + w.minor:
            w.size = w.major + 2 + w.minor
    else:
        slen = len(str(st.st_size).encode())
        if w.size < slen:
            w.size = slen

    return _Ent(name, st, _type_letter(mode), acl), st.st_blocks


# --------------------------------------------------------------------------
# print_long_format()
# --------------------------------------------------------------------------

def _time_width(ctx):
    """ls.c long_time_expected_width(): width of epoch 0 in the old format."""
    if ctx.time_width is None:
        ctx.time_width = len(_fmt_time(0, False))
    return ctx.time_width


def _line(ctx, e, w):
    if e.st is None:
        mode = e.letter + b"?" * 10
    else:
        mode = _mode_string(e.st.st_mode)
    if not w.any_acl:
        mode = mode[:10]
    elif e.acl == ACL_LSM:
        mode = mode[:10] + b"."
    elif e.acl == ACL_YES:
        mode = mode[:10] + b"+"
    elif e.acl == ACL_UNKNOWN:
        mode = mode[:10] + b"?"

    out = bytearray()
    out += mode
    out += b" "
    if e.st is None:
        out += b"?".rjust(w.nlink)
    else:
        out += str(e.st.st_nlink).encode().rjust(w.nlink)
    out += b" "

    # ls.c format_user() / format_group() / format_user_or_group():
    # a resolved name is left-justified then padded with width-len+1 spaces;
    # a numeric id (and the "?" of a failed stat) goes through the name path.
    for kind, ident, resolver in (("owner", None if e.st is None else e.st.st_uid,
                                   _user_name),
                                  ("group", None if e.st is None else e.st.st_gid,
                                   _group_name)):
        if ident is None:
            # format_user_or_group("?"): "?" then max(1, width) spaces
            out += b"?" + b" " * max(getattr(w, kind), 1)
            continue
        nm = resolver(ident)
        if nm is None:
            out += str(ident).encode().rjust(getattr(w, kind)) + b" "
        else:
            pad = getattr(w, kind) - len(nm)
            out += nm + b" " * (pad + 1 if pad > 0 else 1)

    if e.st is not None and (_stat.S_ISCHR(e.st.st_mode)
                             or _stat.S_ISBLK(e.st.st_mode)):
        maj, min_ = os.major(e.st.st_rdev), os.minor(e.st.st_rdev)
        blanks = w.size - (w.major + 2 + w.minor)
        out += str(maj).encode().rjust(w.major + (blanks if blanks > 0 else 0))
        out += b", "
        out += str(min_).encode().rjust(w.minor)
        out += b" "
    else:
        size = b"?" if e.st is None else str(e.st.st_size).encode()
        out += size.rjust(w.size) + b" "

    if e.st is None:
        out += b"?".rjust(_time_width(ctx)) + b" "
    else:
        t = int(e.st.st_mtime)
        recent = (ctx.now - _SIX_MONTHS < t) and (t < ctx.now)
        out += _fmt_time(t, recent) + b" "

    out += _quote(e.name)
    out += b"\n"
    return bytes(out)


# --------------------------------------------------------------------------
# print_dir()
# --------------------------------------------------------------------------

def _print_block(ctx, ents, w):
    out = ctx.out
    for e in ents:
        out += _line(ctx, e, w)


def _print_dir(ctx, path, top):
    full = ctx.full(path)
    try:
        names = os.listdir(full)
    except OSError as exc:
        ctx.fail(True, b"cannot open directory", path, exc)
        return

    try:
        dst = os.stat(full)
    except OSError as exc:
        ctx.fail(True, b"cannot determine device and inode of", path, exc)
        return
    key = (dst.st_dev, dst.st_ino)
    if key in ctx.active:
        ctx.err += b"ls: " + _quotef(path) + \
            b": not listing already-listed directory\n"
        ctx.status = 2
        return
    ctx.active.add(key)

    if not ctx.first_header:
        ctx.out += b"\n"
    ctx.first_header = False
    ctx.out += _quote(path) + b":\n"

    w = _W()
    total = 0
    ents = []
    for name in names:                     # readdir order: error order in ls
        if name.startswith(b"."):
            continue                      # file_ignored: no -a
        e, blocks = _gobble(ctx, name, _attach(path, name), False, w)
        if e is not None:
            ents.append(e)
            total += blocks

    ents.sort(key=lambda x: x.name)

    ctx.out += b"total " + str(total // 2).encode() + b"\n"
    _print_block(ctx, ents, w)

    for e in ents:
        if e.st is not None and _stat.S_ISDIR(e.st.st_mode):
            _print_dir(ctx, _concat(path, e.name), False)

    ctx.active.discard(key)


# --------------------------------------------------------------------------
# entry points
# --------------------------------------------------------------------------

def ls_lRL_full(operands, now=None, cwd=None):
    """Return (stdout, stderr, exit_status) for ``ls -LRl <operands>``."""
    if now is None:
        now = int(time.time())
    if isinstance(operands, (bytes, str)):
        operands = [operands]
    ops = [op if isinstance(op, bytes) else os.fsencode(op) for op in operands]
    if not ops:
        ops = [b"."]
    root = cwd if cwd is not None else os.getcwdb()
    if isinstance(root, str):
        root = os.fsencode(root)

    ctx = _Ctx(int(now), root)

    w = _W()
    top = []
    for op in ops:
        e, _blocks = _gobble(ctx, op, op, True, w)
        if e is None:
            continue
        e.is_arg_dir = e.st is not None and _stat.S_ISDIR(e.st.st_mode)
        top.append(e)
    top.sort(key=lambda x: x.name)

    files = [e for e in top if not e.is_arg_dir]
    dirs = [e for e in top if e.is_arg_dir]

    if files:
        # widths are those accumulated over every operand, directories included
        _print_block(ctx, files, w)
    if dirs:
        if files:
            ctx.out += b"\n"
        for d in dirs:
            _print_dir(ctx, d.name, True)

    return bytes(ctx.out), bytes(ctx.err), ctx.status


def ls_lRL(operands, now=None, cwd=None):
    """stdout of ``LC_ALL=C LANG=C ls -LRl <operands> 2>/dev/null``."""
    return ls_lRL_full(operands, now=now, cwd=cwd)[0]


if __name__ == "__main__":              # pragma: no cover - manual poking
    import sys
    out = ls_lRL(sys.argv[1:] or ["."])
    sys.stdout.buffer.write(out)

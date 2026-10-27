"""L1 draft: byte-exact emulation of GNU `LC_ALL=C LANG=C ls -LRl OPERANDS 2>/dev/null` (stdout only), no process."""
import grp
import os
import pwd
import stat
import time

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
    recent = now - SIX_MONTHS * 1000000000 < sec <= now
    mon = MONTHS[tm.tm_mon - 1]
    if recent:
        return "%s %2d %02d:%02d" % (mon, tm.tm_mday, tm.tm_hour, tm.tm_min)
    return "%s %2d  %d" % (mon, tm.tm_mday, tm.tm_year)


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
        return [], (total + 1) // 2
    wrows = rows + [(None, str(st.st_nlink), _user(st.st_uid), _group(st.st_gid), str(st.st_size)) for _n, st in width_extra]
    wl = max(len(r[1]) for r in wrows)
    wu = max(len(r[2]) for r in wrows)
    wg = max(len(r[3]) for r in wrows)
    ws = max(len(r[4]) for r in wrows)
    out = []
    for mode, nl, us, gr, size, date, name in rows:
        out.append("%s %s %s %s %s %s %s" % (mode, nl.rjust(wl), us.ljust(wu), gr.ljust(wg), size.rjust(ws),
                                             date.rjust(12), name))
    return out, (total + 1) // 2


def _stat(p):
    try:
        return os.stat(p)
    except OSError:
        return None


def _key(n):
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

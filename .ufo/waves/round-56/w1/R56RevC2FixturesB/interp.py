#!/usr/bin/env python3
# Independent interpreter written from registration.md section C2 only (seat R56RevC2FixturesB audit).
import sys, os, glob, json, re, stat

WS = " \t\r\n\x0b\x0c"
LIMIT = 1048576


class Setup(Exception):
    def __init__(self, reason):
        self.reason = reason


def usage():
    raise Setup("usage")


def parse_args(argv):
    opts = {}
    i = 0
    while i < len(argv):
        t = argv[i]
        if t not in ("--config", "--home", "--display-root", "--getoption"):
            usage()
        if t in opts or i + 1 >= len(argv):
            usage()
        v = argv[i + 1]
        if not os.path.isabs(v):
            usage()
        opts[t] = v
        i += 2
    if "--config" not in opts:
        usage()
    return opts


def read_file(path, must_exist_regular=True):
    """Return bytes or raise OSError; size > LIMIT -> Setup too_large."""
    st = os.stat(path)
    if not stat.S_ISREG(st.st_mode):
        raise OSError("nonregular")
    if st.st_size > LIMIT:
        raise Setup("too_large")
    with open(path, "rb") as fh:
        data = fh.read()
    if len(data) > LIMIT:
        raise Setup("too_large")
    return data


def main(argv):
    o = parse_args(argv)
    config = o["--config"]
    home = o.get("--home")
    droot = o.get("--display-root")
    getopt = o.get("--getoption")

    roots = []
    if droot is not None:
        d = droot.rstrip("/") if droot != "/" else "/"
        roots = [d, os.path.realpath(droot).rstrip("/") or "/"]

    def disp(p):
        for r in roots:
            if p == r or p.startswith(r + "/"):
                return "$ROOT" + p[len(r):]
        return p

    events = []          # strings (ERROR/SKIP lines), processing order
    paths = []           # (path, via)
    st = {"U": 0, "E": 0, "last": None}   # last accepted disable_autoreload value

    def parse(cur, depth):
        try:
            data = read_file(cur)
        except Setup:
            raise
        except OSError:
            return
        text = data.decode("utf-8", errors="replace")
        stack = []
        for lineno, raw in enumerate(text.split("\n"), 1):
            s = raw.strip(WS)
            if not s or s[0] == "#":
                continue
            if "=" not in s:
                if s == "}":
                    if stack:
                        stack.pop()
                elif s.endswith("{"):
                    stack.append(s[:-1].strip(WS))
                continue
            lhs, rhs = s.split("=", 1)
            lhs = lhs.strip(WS)
            rhs = rhs.strip(WS)
            if lhs == "source":
                if stack:
                    st["U"] += 1
                    continue
                handle_source(rhs.split("#", 1)[0].strip(WS), cur, lineno, depth)
                continue
            if lhs.startswith("$"):
                continue
            key = ":".join(stack + [lhs]) if stack else lhs
            if key != "misc:disable_autoreload":
                continue
            if "$" in s or "{" in s or "\\" in s or "##" in rhs:
                st["U"] += 1
                continue
            val = rhs.split("#", 1)[0].strip(WS)
            if val.startswith(("true", "on", "yes")):
                st["last"] = 1
            elif val.startswith(("false", "off", "no")):
                st["last"] = 0
            elif re.fullmatch(r"[0-9]+", val):
                st["last"] = int(val)
            else:
                st["U"] += 1

    def handle_source(raw, cur, lineno, depth):
        via = disp(cur) + ":" + str(lineno)
        if len(raw) < 2:
            events.append("MADO_WATCH: ERROR via=%s source=%s reason=bogus" % (via, raw))
            return
        if (raw.startswith("~") and home is None) or "\\" in raw:
            st["U"] += 1
            return
        if raw[0] == "~":
            value = home + raw[1:]
        elif raw[0] == "/":
            value = raw
        else:
            curdir = cur[: cur.rfind("/")] if "/" in cur else cur
            if raw[0] == ".":
                if raw.startswith("../"):
                    parent = curdir[: curdir.rfind("/")] if "/" in curdir else curdir
                    value = parent + raw[2:]
                elif raw.startswith("./"):
                    value = curdir + raw[1:]
                else:
                    value = curdir + "/" + raw
            else:
                value = curdir + "/" + raw
        matches = sorted(glob.glob(value))
        if not matches:
            events.append("MADO_WATCH: ERROR via=%s source=%s reason=nomatch" % (via, raw))
            return
        for m in matches:
            v = m if os.path.isabs(m) else os.path.join(os.path.dirname(cur), m)
            try:
                s2 = os.stat(v)
            except OSError:
                events.append("MADO_WATCH: ERROR via=%s source=%s reason=inaccessible" % (via, raw))
                break
            if stat.S_ISREG(s2.st_mode):
                paths.append((v, via))
                if depth + 1 > 16:
                    st["U"] += 1
                else:
                    parse(v, depth + 1)
            elif stat.S_ISDIR(s2.st_mode):
                events.append("MADO_WATCH: SKIP via=%s path=%s reason=directory" % (via, disp(v)))
            else:
                events.append("MADO_WATCH: SKIP via=%s path=%s reason=nonregular" % (via, disp(v)))

    # main config: always first entry, parsed when a readable regular file
    paths.append((config, "main"))
    try:
        parse(config, 0)
    except Setup:
        raise
    # Note: parse() silently returns for unreadable / non-regular config.

    live = None
    if getopt is not None:
        try:
            gdata = read_file(getopt)
        except Setup:
            raise
        except OSError:
            raise Setup("unreadable")
        live_map = {}
        for ln in gdata.decode("utf-8", errors="replace").split("\n"):
            s = ln.strip(WS)
            if not s:
                continue
            try:
                obj = json.loads(s)
            except ValueError:
                raise Setup("bad_json")
            if not isinstance(obj, dict):
                raise Setup("bad_json")
            opt = obj.get("option")
            iv = obj.get("int")
            if isinstance(opt, str) and isinstance(iv, int) and not isinstance(iv, bool):
                live_map[opt] = iv
        live = live_map.get("misc:disable_autoreload")

    last = st["last"]
    autoreload_on = not (last is not None and last != 0)
    watches = []
    if autoreload_on:
        for path, via in paths:
            if os.path.isdir(path):
                typ = "dir"
                mask = "IN_CLOSE_WRITE|IN_DONT_FOLLOW|IN_CREATE|IN_DELETE|IN_MOVED_TO|IN_MOVED_FROM"
            elif os.path.lexists(path):
                typ = "file"
                mask = "IN_CLOSE_WRITE|IN_DONT_FOLLOW"
            else:
                typ = "missing"
                mask = "IN_CLOSE_WRITE|IN_DONT_FOLLOW"
            watches.append(("primary", path, typ, mask, via))
            if os.path.islink(path):
                try:
                    rp = os.path.realpath(path, strict=True)
                except OSError:
                    rp = None
                if rp is not None:
                    watches.append(("canonical", rp, "file", "IN_CLOSE_WRITE", via))

    out = []
    header = "MADO_WATCH: config=%s autoreload=%s disable_autoreload=%s paths=%d unsupported=%d errors=%d" % (
        disp(config),
        "on" if autoreload_on else "off",
        "unset" if last is None else str(last),
        len(paths),
        st["U"],
        sum(1 for e in events if " ERROR " in e),
    )
    out.append(header)
    out.extend(events)
    for k, (role, path, typ, mask, via) in enumerate(watches, 1):
        out.append("MADO_WATCH: n=%d role=%s path=%s type=%s mask=%s via=%s" % (k, role, disp(path), typ, mask, via))
    cfg_flag = 1 if (last is not None and last != 0) else 0
    if getopt is not None:
        if live is None:
            verdict = "UNKNOWN"
            livestr = "?"
        else:
            verdict = "AGREE" if live == cfg_flag else "DIFFER"
            livestr = str(live)
        out.append("MADO_WATCH_LIVE: option=misc:disable_autoreload config=%d live=%s verdict=%s" % (cfg_flag, livestr, verdict))
        live_tag = verdict
    else:
        live_tag = "NONE"
    errors = sum(1 for e in events if " ERROR " in e)
    out.append("MADO_WATCH: DONE watches=%d unsupported=%d errors=%d live=%s" % (len(watches), st["U"], errors, live_tag))
    sys.stdout.write("\n".join(out) + "\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Setup as e:
        sys.stdout.write("MADO_WATCH: SETUP %s\n" % e.reason)
        sys.exit(2)

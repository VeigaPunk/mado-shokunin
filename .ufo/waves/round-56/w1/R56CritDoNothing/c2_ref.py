#!/usr/bin/env python3
"""Critic's reference implementation of tools/mado-watchplan.py, written ONLY from registration.md section 'C2'.

Ablation switches (critic controls; default = full model, which must reproduce the fixtures):
  --ablate source     ignore `source =` lines entirely (implements only the main file)
  --ablate symlink    no canonical second watch for symlink entries
  --ablate disable    ignore misc:disable_autoreload (always autoreload=on, full watch list)
Hidden flag only for the critic harness; the registered tool has no ablation switch.
"""
import glob, json, os, stat, sys

MAX_BYTES = 1048576
MAX_DEPTH = 16
M_FILE = "IN_CLOSE_WRITE|IN_DONT_FOLLOW"
M_DIR = "IN_CLOSE_WRITE|IN_DONT_FOLLOW|IN_CREATE|IN_DELETE|IN_MOVED_TO|IN_MOVED_FROM"
M_CANON = "IN_CLOSE_WRITE"
KEY = "misc:disable_autoreload"


class Setup(Exception):
    def __init__(self, reason):
        self.reason = reason


def usage():
    raise Setup("usage")


def parse_args(argv, ablate):
    opts = {}
    i = 0
    single = {"--config", "--home", "--display-root", "--getoption"}
    while i < len(argv):
        t = argv[i]
        if t not in single:
            usage()
        if i + 1 >= len(argv):
            usage()
        v = argv[i + 1]
        if t in opts:
            usage()
        if t != "--config" and False:
            pass
        if t == "--config" and not v.startswith("/"):
            usage()
        if t in ("--home", "--display-root", "--getoption") and not v.startswith("/"):
            usage()
        opts[t] = v
        i += 2
    if "--config" not in opts:
        usage()
    return opts


def read_bytes_checked(path):
    st = os.stat(path)
    if st.st_size > MAX_BYTES:
        raise Setup("too_large")
    with open(path, "rb") as f:
        return f.read()


def main():
    ablate = set()
    argv = sys.argv[1:]
    while "--ablate" in argv:
        k = argv.index("--ablate")
        ablate.add(argv[k + 1])
        del argv[k:k + 2]
    try:
        opts = parse_args(argv, ablate)
        config = opts["--config"]
        home = opts.get("--home")
        droot = opts.get("--display-root")
        getopt_path = opts.get("--getoption")
        if droot is not None:
            droot = droot.rstrip("/") or "/"
        # getoption dump
        live = None
        live_seen = False
        if getopt_path is not None:
            try:
                st = os.stat(getopt_path)
            except OSError:
                raise Setup("unreadable")
            import stat as _s
            if not _s.S_ISREG(st.st_mode):
                raise Setup("unreadable")
            try:
                raw = read_bytes_checked(getopt_path)
            except Setup:
                raise
            except OSError:
                raise Setup("unreadable")
            for line in raw.decode("utf-8", "replace").split("\n"):
                s = line.strip(" \t\r\n\v\f")
                if not s:
                    continue
                try:
                    obj = json.loads(s)
                except Exception:
                    raise Setup("bad_json")
                if not isinstance(obj, dict):
                    raise Setup("bad_json")
                if obj.get("option") == KEY and isinstance(obj.get("int"), int) and not isinstance(obj.get("int"), bool):
                    live = obj["int"]
                    live_seen = True
        state = {"unsupported": 0, "errors": 0, "disable": None}
        events = []
        paths = []  # (path, via, display_cur_not_needed)

        def display(p):
            if droot is not None:
                cands = [droot]
                rp = os.path.realpath(droot)
                if rp != droot:
                    cands.append(rp)
                for c in cands:
                    if c == "/":
                        return "$ROOT" + p
                    if p == c or p.startswith(c + "/"):
                        return "$ROOT" + p[len(c):]
            return p

        def absolute(raw, cur):
            if raw[0] == "~":
                return home + raw[1:]
            if raw[0] == "/":
                return raw
            curdir = cur[:cur.rfind("/")] if "/" in cur else cur
            if raw[0] == ".":
                if raw.startswith("../"):
                    parent = curdir[:curdir.rfind("/")] if "/" in curdir else curdir
                    return parent + raw[2:]
                if raw.startswith("./"):
                    return curdir + raw[1:]
                return curdir + "/" + raw
            return curdir + "/" + raw

        def handle_source(raw, cur, depth, lineno):
            if len(raw) < 2:
                events.append(f"MADO_WATCH: ERROR via={display(cur)}:{lineno} source={raw} reason=bogus")
                state["errors"] += 1
                return
            if (raw.startswith("~") and home is None) or "\\" in raw:
                state["unsupported"] += 1
                return
            value = absolute(raw, cur)
            matches = sorted(glob.glob(value))
            if not matches:
                events.append(f"MADO_WATCH: ERROR via={display(cur)}:{lineno} source={raw} reason=nomatch")
                state["errors"] += 1
                return
            via = f"{display(cur)}:{lineno}"
            for m in matches:
                v = m if m.startswith("/") else cur
                try:
                    st = os.stat(v)
                except OSError:
                    events.append(f"MADO_WATCH: ERROR via={via} source={raw} reason=inaccessible")
                    state["errors"] += 1
                    break
                if stat.S_ISREG(st.st_mode):
                    paths.append((v, via))
                    if depth + 1 > MAX_DEPTH:
                        state["unsupported"] += 1
                        continue
                    try:
                        text = read_bytes_checked(v).decode("utf-8", "replace")
                    except Setup:
                        raise
                    except OSError:
                        continue
                    parse(text, v, depth + 1)
                elif stat.S_ISDIR(st.st_mode):
                    events.append(f"MADO_WATCH: SKIP via={via} path={display(v)} reason=directory")
                else:
                    events.append(f"MADO_WATCH: SKIP via={via} path={display(v)} reason=nonregular")

        def parse(text, cur, depth):
            stack = []
            for lineno, raw in enumerate(text.split("\n"), 1):
                line = raw.strip(" \t\r\x0b\x0c\n")
                if not line or line[0] == "#":
                    continue
                if "=" not in line:
                    if line == "}":
                        if stack:
                            stack.pop()
                    elif line.endswith("{"):
                        stack.append(line[:-1].strip())
                    continue
                lhs, _, rhs = line.partition("=")
                lhs = lhs.strip(" \t\r\x0b\x0c\n")
                rhs = rhs.strip(" \t\r\x0b\x0c\n")
                if lhs == "source":
                    if stack:
                        state["unsupported"] += 1
                        continue
                    if "source" in ablate:
                        continue
                    raw_path = rhs.split("#", 1)[0].strip(" \t\r\x0b\x0c\n")
                    handle_source(raw_path, cur, depth, lineno)
                    continue
                if lhs.startswith("$"):
                    continue
                key = ":".join(stack + [lhs]) if stack else lhs
                if key != KEY or "disable" in ablate:
                    continue
                if "$" in line or "{" in line or "\\" in line or "##" in rhs:
                    state["unsupported"] += 1
                    continue
                value = rhs.split("#", 1)[0].strip(" \t\r\x0b\x0c\n")
                if value.startswith(("true", "on", "yes")):
                    state["disable"] = 1
                elif value.startswith(("false", "off", "no")):
                    state["disable"] = 0
                elif value and value.isdigit() and value.isascii():
                    state["disable"] = int(value)
                else:
                    state["unsupported"] += 1

        # main config
        paths.append((config, "main"))
        try:
            st = os.stat(config)
            is_reg = stat.S_ISREG(st.st_mode)
        except OSError:
            is_reg = False
        if is_reg:
            try:
                text = read_bytes_checked(config).decode("utf-8", "replace")
            except Setup:
                raise
            except OSError:
                text = None
            if text is not None:
                parse(text, config, 0)

        disable = state["disable"]
        off = disable is not None and disable != 0
        out_lines = []
        watches = []
        if not off:
            for path, via in paths:
                if os.path.isdir(path):
                    typ, mask = "dir", M_DIR
                elif os.path.lexists(path):
                    typ, mask = "file", M_FILE
                else:
                    typ, mask = "missing", M_FILE
                watches.append(("primary", path, typ, mask, via))
                if os.path.islink(path) and "symlink" not in ablate:
                    try:
                        canon = os.path.realpath(path, strict=True)
                    except (OSError, RuntimeError):
                        canon = None
                    if canon is not None:
                        watches.append(("canonical", canon, "file", M_CANON, via))
        autoreload = "off" if off else "on"
        dis_text = "unset" if disable is None else str(disable)
        if "disable" in ablate:
            autoreload, dis_text = "on", "unset"
        header = (f"MADO_WATCH: config={display(config)} autoreload={autoreload} disable_autoreload={dis_text} "
                  f"paths={len(paths)} unsupported={state['unsupported']} errors={state['errors']}")
        out_lines.append(header)
        out_lines.extend(events)
        for k, (role, path, typ, mask, via) in enumerate(watches, 1):
            out_lines.append(f"MADO_WATCH: n={k} role={role} path={display(path)} type={typ} mask={mask} via={via}")
        if getopt_path is not None:
            cfg = 1 if (disable not in (None, 0)) else 0
            if not live_seen:
                verdict, lv = "UNKNOWN", "?"
            else:
                lv = str(live)
                verdict = "AGREE" if live == cfg else "DIFFER"
            out_lines.append(f"MADO_WATCH_LIVE: option={KEY} config={cfg} live={lv} verdict={verdict}")
            live_tag = verdict if live_seen else "UNKNOWN"
            live_tag = "UNKNOWN" if not live_seen else verdict
        else:
            live_tag = "NONE"
        out_lines.append(f"MADO_WATCH: DONE watches={len(watches)} unsupported={state['unsupported']} "
                         f"errors={state['errors']} live={live_tag}")
        sys.stdout.write("\n".join(out_lines) + "\n")
        sys.exit(0)
    except Setup as e:
        sys.stdout.write(f"MADO_WATCH: SETUP {e.reason}\n")
        sys.exit(2)


if __name__ == "__main__":
    main()

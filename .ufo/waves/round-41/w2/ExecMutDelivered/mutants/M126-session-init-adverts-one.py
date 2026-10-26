#!/usr/bin/env python3
"""mado-globals — read-only census of the Wayland globals the compositor advertised.

The desktop portal (xdg-desktop-portal-hyprland) logs one line per global the
compositor offers it: `Got interface: <name> (ver <N>)`. That journal is the
one read-only witness of the compositor's advertised protocol set that needs no
socket connection. This tool parses it (a saved journal with --journal-file, or
the live user journal with --live) into sessions and reports the latest session's
globals, each with a class from a fixed decision table, and optionally the drift
between the last two sessions (--diff) and whether named globals are present
(--expect NAME, repeatable).

The grammar is `journalctl -o short-iso` only. A line that contains `Got interface: `
but does not match it (another -o format, a different level, a different spacing)
is counted in `ignored=`; an input whose every advert is ignored is
UNRECOGNIZED_FORMAT (exit 4), never a silent NO_SESSIONS.

Output (stdout)
    MADO_GLOBALS_SESSION: n= boot= pid= first= last= interfaces= adverts=   (per session)
    MADO_GLOBAL: name= ver= count= class=            (latest session, sorted by name)
    MADO_GLOBALS_DIFF: from= to= added= removed= ver_changed=   (--diff)
    MADO_GLOBALS: sessions= latest_pid= interfaces= classes= expected_missing= ignored= verdict=
Exit: 0 OK, 1 MISSING_EXPECTED, 3 NO_SESSIONS, 4 UNRECOGNIZED_FORMAT, 2 usage/input
(`MADO_GLOBALS: SETUP <reason>` on stdout), 5 live journal failure.
"""
import argparse
import os
import re
import select
import stat
import subprocess
import sys
import tempfile
import time

MAX_BYTES = 8 * 1024 * 1024
LIVE_TIMEOUT = 30
ADVERT = re.compile(
    r"([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}[+-][0-9]{2}:[0-9]{2}) (\S+) "
    r"xdg-desktop-portal-hyprland\[([0-9]+)\]: \[LOG\]  \| "
    r"Got interface: ([A-Za-z0-9_]{1,128}) \(ver ([0-9]{1,6})\)")
BOOT = re.compile(r"-- Boot ([0-9a-f]{32}) --")
NAME = re.compile(r"[A-Za-z0-9_]{1,128}")
MARK = "Got interface: "
JOURNALCTL_ARGS = ["--user", "-u", "xdg-desktop-portal-hyprland", "--no-pager",
                   "-o", "short-iso"]

CLASSES = {
    "focus-grab": ["hyprland_focus_grab_manager_v1"],
    "input-synthesis": ["zwlr_virtual_pointer_manager_v1",
                        "zwp_virtual_keyboard_manager_v1",
                        "zwp_input_method_manager_v2"],
    "input-capture": ["hyprland_input_capture_manager_v1",
                      "zwp_keyboard_shortcuts_inhibit_manager_v1",
                      "hyprland_global_shortcuts_manager_v1"],
    "session-lock": ["ext_session_lock_manager_v1", "hyprland_lock_notifier_v1"],
    "idle": ["ext_idle_notifier_v1", "zwp_idle_inhibit_manager_v1"],
    "clipboard": ["zwlr_data_control_manager_v1", "ext_data_control_manager_v1",
                  "zwp_primary_selection_device_manager_v1"],
    "capture": ["ext_image_copy_capture_manager_v1",
                "ext_foreign_toplevel_image_capture_source_manager_v1",
                "zwlr_screencopy_manager_v1",
                "hyprland_toplevel_export_manager_v1"],
    "toplevel-control": ["zwlr_foreign_toplevel_manager_v1",
                         "ext_foreign_toplevel_list_v1", "xdg_activation_v1",
                         "hyprland_toplevel_mapping_manager_v1"],
    "output-control": ["zwlr_output_manager_v1", "zwlr_output_power_manager_v1",
                       "zwlr_gamma_control_manager_v1",
                       "hyprland_ctm_control_manager_v1"],
    "sandbox": ["wp_security_context_manager_v1"],
}
CLASS_OF = {n: c for c, names in CLASSES.items() for n in names}


class Setup(Exception):
    def __init__(self, reason, code=2):
        Exception.__init__(self, reason)
        self.reason = reason
        self.code = code


def classify(name):
    return CLASS_OF.get(name, "other")


def parse(data):
    """Return (sessions, ignored). A session is a dict: boot, pid, first, last,
    adverts, names{name: [count, highest ver]}."""
    text = data.decode("utf-8", "replace")
    sessions = []
    ignored = 0
    boot = "-"
    boot_changed = False
    cur = None
    for line in text.split("\n"):
        m = BOOT.fullmatch(line)
        if m:
            boot = m.group(1)
            boot_changed = True
            continue
        m = ADVERT.fullmatch(line)
        if not m:
            if MARK in line:
                ignored += 1
            continue
        ts, _host, pid, name, ver = m.groups()
        ver = int(ver)
        if cur is None or boot_changed or cur["pid"] != pid:
            cur = {"boot": boot, "pid": pid, "first": ts, "last": ts,
                   "adverts": 1, "names": {}}
            sessions.append(cur)
            boot_changed = False
        cur["last"] = ts
        cur["adverts"] += 1
        ent = cur["names"].setdefault(name, [0, 0])
        ent[0] += 1
        ent[1] = max(ent[1], ver)
    return sessions, ignored


def report(sessions, ignored, expects, diff):
    out = []
    for i, s in enumerate(sessions, 1):
        out.append("MADO_GLOBALS_SESSION: n=%d boot=%s pid=%s first=%s last=%s "
                   "interfaces=%d adverts=%d" % (i, s["boot"], s["pid"],
                                                 s["first"], s["last"],
                                                 len(s["names"]), s["adverts"]))
    latest = sessions[-1] if sessions else None
    if latest:
        for name in sorted(latest["names"]):
            count, ver = latest["names"][name]
            out.append("MADO_GLOBAL: name=%s ver=%d count=%d class=%s"
                       % (name, ver, count, classify(name)))
    if diff:
        if len(sessions) < 2:
            out.append("MADO_GLOBALS_DIFF: sessions=%d none" % len(sessions))
        else:
            a, b = sessions[-2]["names"], sessions[-1]["names"]
            added = sorted(set(b) - set(a))
            removed = sorted(set(a) - set(b))
            changed = ["%s:%d>%d" % (n, a[n][1], b[n][1])
                       for n in sorted(set(a) & set(b)) if a[n][1] != b[n][1]]
            out.append("MADO_GLOBALS_DIFF: from=%d to=%d added=%s removed=%s "
                       "ver_changed=%s" % (len(sessions) - 1, len(sessions),
                                           ",".join(added) or "-",
                                           ",".join(removed) or "-",
                                           ",".join(changed) or "-"))
    names = latest["names"] if latest else {}
    classes = {}
    for n in names:
        classes[classify(n)] = classes.get(classify(n), 0) + 1
    missing = sorted(set(e for e in expects if e not in names))
    if not sessions and ignored > 0:
        verdict, code = "UNRECOGNIZED_FORMAT", 4
    elif not sessions:
        verdict, code = "NO_SESSIONS", 3
    elif missing:
        verdict, code = "MISSING_EXPECTED", 1
    else:
        verdict, code = "OK", 0
    out.append("MADO_GLOBALS: sessions=%d latest_pid=%s interfaces=%d classes=%s "
               "expected_missing=%s ignored=%d verdict=%s" % (
                   len(sessions), latest["pid"] if latest else "-", len(names),
                   ",".join("%s:%d" % (c, classes[c]) for c in sorted(classes))
                   or "-", ",".join(missing) or "-", ignored, verdict))
    return out, code


def resolve_program(prog):
    if "/" not in prog:
        for d in os.environ.get("PATH", "").split(":"):
            cand = os.path.join(d or ".", prog)
            if os.path.isfile(cand) and os.access(cand, os.X_OK):
                prog = cand
                break
        else:
            raise Setup("journalctl_unusable", 5)
    prog = os.path.abspath(prog)
    try:
        st = os.stat(prog)
    except OSError:
        raise Setup("journalctl_unusable", 5)
    if not stat.S_ISREG(st.st_mode) or not os.access(prog, os.X_OK) \
            or st.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
        raise Setup("journalctl_unusable", 5)
    return prog


def read_live(prog):
    prog = resolve_program(prog)
    env = {k: os.environ[k] for k in ("PATH", "XDG_RUNTIME_DIR",
                                      "DBUS_SESSION_BUS_ADDRESS", "LC_ALL")
           if k in os.environ}
    try:
        proc = subprocess.Popen([prog] + JOURNALCTL_ARGS,
                                stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL, env=env,
                                shell=False)
    except (OSError, subprocess.SubprocessError):
        raise Setup("journalctl_failed", 5)
    deadline = time.monotonic() + LIVE_TIMEOUT
    chunks = []
    total = 0
    reason = None
    try:
        fd = proc.stdout.fileno()
        while True:
            left = deadline - time.monotonic()
            if left <= 0 or not select.select([fd], [], [], left)[0]:
                reason = "journalctl_failed"
                break
            block = os.read(fd, 65536)
            if not block:
                break
            chunks.append(block)
            total += len(block)
            if total > MAX_BYTES:
                reason = "journalctl_too_large"
                break
    finally:
        if reason is not None:
            proc.kill()
        proc.stdout.close()
        rc = proc.wait()
    if reason is not None:
        raise Setup(reason, 5)
    if rc != 0:
        raise Setup("journalctl_failed", 5)
    return b"".join(chunks)


def read_file(path):
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
    except OSError:
        raise Setup("unreadable")
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise Setup("unreadable")
        data = b""
        while len(data) <= MAX_BYTES:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            data += block
    except OSError:
        raise Setup("unreadable")
    finally:
        os.close(fd)
    if len(data) > MAX_BYTES:
        raise Setup("too_large")
    return data


def run(argv):
    ap = argparse.ArgumentParser(prog="mado-globals", add_help=False,
                                 allow_abbrev=False)
    ap.add_argument("--journal-file")
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--journalctl")
    ap.add_argument("--expect", action="append", default=[])
    ap.add_argument("--diff", action="store_true")
    ap.error = lambda msg: (_ for _ in ()).throw(Setup("usage"))
    try:
        args = ap.parse_args(argv)
    except SystemExit:
        raise Setup("usage")
    if bool(args.journal_file) == bool(args.live):
        raise Setup("usage")
    if args.journalctl is not None and not args.live:
        raise Setup("usage")
    for e in args.expect:
        if not NAME.fullmatch(e):
            raise Setup("bad_expect")
    if args.live:
        data = read_live(args.journalctl or "journalctl")
    else:
        data = read_file(args.journal_file)
    sessions, ignored = parse(data)
    return report(sessions, ignored, sorted(set(args.expect)), args.diff)


def selftest():
    global LIVE_TIMEOUT
    ok = 0
    n = 0

    def check(cond):
        nonlocal ok, n
        n += 1
        ok += bool(cond)

    ts = "2026-10-25T13:36:24-03:00"
    fmt = ts + " h xdg-desktop-portal-hyprland[%s]: [LOG]  | Got interface: %s (ver %d)\n"
    data = (fmt % ("11", "wl_seat", 9) + fmt % ("11", "wl_seat", 5)
            + fmt % ("11", "hyprland_focus_grab_manager_v1", 1)).encode()
    s, ig = parse(data)
    check(len(s) == 1 and s[0]["adverts"] == 3 and ig == 0)
    check(s[0]["names"]["wl_seat"] == [2, 9])
    check(parse((fmt % ("11", "wl_seat", 9) + fmt % ("11", "wl_seat", 10)).encode())[0][0]["names"]["wl_seat"] == [2, 10])
    check(classify("hyprland_focus_grab_manager_v1") == "focus-grab")
    check(classify("wl_seat") == "other")
    check(classify("HYPRLAND_FOCUS_GRAB_MANAGER_V1") == "other")
    check(len(parse(data + (fmt % ("12", "wl_seat", 9)).encode())[0]) == 2)
    check(len(parse(data + (fmt % ("011", "wl_seat", 9)).encode())[0]) == 2)
    check(len(parse(data + b"-- Boot " + b"a" * 32 + b" --\n"
                    + (fmt % ("11", "wl_seat", 9)).encode())[0]) == 2)
    b1 = b"-- Boot " + b"a" * 32 + b" --\n"
    check(len(parse(b1 + (fmt % ("11", "wl_seat", 9)).encode() + b1
                    + (fmt % ("11", "wl_seat", 9)).encode())[0]) == 2)
    ps = parse(b1 + (fmt % ("11", "wl_seat", 9)).encode()
               + (fmt % ("12", "wl_seat", 9)).encode())[0]
    check(len(ps) == 2 and ps[1]["boot"] == "a" * 32)
    check(parse(data.replace(b"[LOG]  |", b"[LOG] |")) == ([], 3))
    check(parse(data.replace(b"[LOG]", b"[ERR]")) == ([], 3))
    check(parse(data.replace(b"[LOG]", b"[log]")) == ([], 3))
    check(parse(data.replace(b"(ver 9)", b"(ver 9) x"))[1] == 1)
    check(parse(b"foo bar\n" + data)[1] == 0)
    check(parse(data.replace(b"(ver 9)", b"(ver \xd9\xa9)"))[1] == 1)
    lines, code = report(s, ig, [], False)
    check(code == 0 and lines[-1].endswith("ignored=0 verdict=OK"))
    lines, code = report(s, 0, ["nope"], False)
    check(code == 1 and "expected_missing=nope " in lines[-1])
    lines, code = report([], 0, [], False)
    check(code == 3 and lines[-1].endswith("ignored=0 verdict=NO_SESSIONS"))
    lines, code = report([], 2, [], False)
    check(code == 4 and lines[-1].endswith("ignored=2 verdict=UNRECOGNIZED_FORMAT"))
    lines, code = report(s, 2, [], False)
    check(code == 0 and "ignored=2 verdict=OK" in lines[-1])
    check(NAME.fullmatch("a b") is None and NAME.fullmatch("a_b1") is not None)
    check(NAME.fullmatch("a-b") is None and NAME.fullmatch("a" * 129) is None)
    check(parse(b"")[0] == [] and parse(b"\n\n")[0] == [])
    two = data + b"-- Boot " + b"b" * 32 + b" --\n" + (fmt % ("11", "wl_shm", 2)).encode()
    s2, _ = parse(two)
    check(len(s2) == 2 and s2[1]["boot"] == "b" * 32 and s2[0]["boot"] == "-")
    lines, code = report(s2, 0, [], True)
    check(any(x.startswith("MADO_GLOBALS_DIFF: from=1 to=2 added=wl_shm removed=") for x in lines))
    check("removed=hyprland_focus_grab_manager_v1,wl_seat" in "\n".join(lines))
    lines, code = report(s, 0, [], True)
    check("MADO_GLOBALS_DIFF: sessions=1 none" in lines)
    lines, code = report(s2, 0, ["wl_shm", "wl_shm", "zz"], False)
    check(lines[-1].count("expected_missing=zz ") == 1)
    check(parse(data.replace(b"\n", b"\r\n"))[0] == [])
    check(parse(data.replace(b"wl_seat", b"wl-seat"))[0][0]["adverts"] == 1)
    check(parse(data.replace(b"wl_seat", b"a" * 129))[0] != parse(data.replace(b"wl_seat", b"a" * 128))[0])
    check(parse(data.replace(b"(ver 5)", b"(ver 1234567)"))[0][0]["adverts"] == 2)
    check(parse(data.replace(b"(ver 5)", b"(ver 123456)"))[0][0]["adverts"] == 3)
    check(parse(b"-- Boot " + b"A" * 32 + b" --\n" + data)[0][0]["boot"] == "-")
    check(parse(b"-- Boot " + b"a" * 32 + b" --\n" + data)[0][0]["boot"] == "a" * 32)
    check(parse(data + b"\xff\xfe\n")[0][0]["adverts"] == 3)
    check(classify("wp_security_context_manager_v1") == "sandbox")
    check(len(CLASS_OF) == sum(len(v) for v in CLASSES.values()))
    with tempfile.TemporaryDirectory() as td:
        def stub(name, body, mode):
            path = os.path.join(td, name)
            with open(path, "w") as fh:
                fh.write(body)
            os.chmod(path, mode)
            return path

        def code_of(fn, *a):
            try:
                return fn(*a)
            except Setup as exc:
                return exc.reason + ":%d" % exc.code

        good = stub("good", "#!/bin/sh\nprintf 'x'\n", 0o755)
        check(code_of(read_live, good) == b"x")
        check(code_of(read_live, stub("bad", "#!/bin/sh\nexit 1\n", 0o755))
              == "journalctl_failed:5")
        check(code_of(read_live, stub("big", "#!/bin/sh\nhead -c 9000000 /dev/zero\n", 0o755))
              == "journalctl_too_large:5")
        LIVE_TIMEOUT = 1
        started = time.monotonic()
        check(code_of(read_live, stub("hang", "#!/bin/sh\nsleep 30\n", 0o755))
              == "journalctl_failed:5")
        check(time.monotonic() - started < 10)
        LIVE_TIMEOUT = 30
        check(code_of(resolve_program, stub("gw", "#!/bin/sh\n", 0o775))
              == "journalctl_unusable:5")
        check(code_of(resolve_program, stub("nx", "#!/bin/sh\n", 0o644))
              == "journalctl_unusable:5")
        check(code_of(resolve_program, os.path.join(td, "absent")) == "journalctl_unusable:5")
        check(code_of(resolve_program, good) == good)
        check(code_of(read_file, os.path.join(td, "absent")) == "unreadable:2")
        check(code_of(read_file, td) == "unreadable:2")
        fifo = os.path.join(td, "fifo")
        os.mkfifo(fifo)
        check(code_of(read_file, fifo) == "unreadable:2")
        check(code_of(read_file, good) == b"#!/bin/sh\nprintf 'x'\n")
        envs = stub("envs", "#!/bin/sh\nenv | cut -d= -f1 | sort | tr '\\n' ' '\n", 0o755)
        os.environ["MADO_CANARY"] = "1"
        got = code_of(read_live, envs).split()
        check(b"PATH" in got and b"MADO_CANARY" not in got and b"HOME" not in got)
        old_path = os.environ.get("PATH", "")
        os.environ["PATH"] = td
        check(code_of(resolve_program, "good") == good)
        check(code_of(resolve_program, "absent") == "journalctl_unusable:5")
        os.environ["PATH"] = old_path
        jf = stub("j.txt", "", 0o644)
        check(code_of(run, ["--journal-file", jf, "--live"]) == "usage:2")
        check(code_of(run, ["--journal-file", jf, "--journalctl", good]) == "usage:2")
        check(code_of(run, []) == "usage:2")
        check(code_of(run, ["--journal-file", jf, "--expect", "a b"]) == "bad_expect:2")
        check(code_of(run, ["--journal-file", jf])[1] == 3)
        check(code_of(run, ["--live", "--journalctl", good])[1] == 3)
    d1 = (fmt % ("1", "wl_seat", 3)).encode() + (fmt % ("2", "wl_seat", 4)).encode()
    check("ver_changed=wl_seat:3>4" in report(*parse(d1), [], True)[0][-2])
    print("MADO_GLOBALS_SELFTEST: %d/%d passed" % (ok, n))
    return 0 if ok == n else 1


def main():
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
    try:
        lines, code = run(sys.argv[1:])
    except Setup as exc:
        print("MADO_GLOBALS: SETUP %s" % exc.reason)
        return exc.code
    for line in lines:
        print(line)
    return code


if __name__ == "__main__":
    sys.exit(main())

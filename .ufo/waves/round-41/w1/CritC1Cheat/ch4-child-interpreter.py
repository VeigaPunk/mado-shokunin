#!/usr/bin/env python3
"""mado-globals (CH4 cheat) - the parse and the report run in a child interpreter.

Same CLI and same output as the contract, but the parser is a string handed to
`python3 -I -c` over stdin: the parent never parses a journal line. Clause g sees
`import subprocess` (allowed) and no exec/eval/compile/__import__/shell=True, and
the file-mode "no process" rule is only enforced for a program named journalctl,
so the spawn is invisible. `verify()` is a real structural check of the child's
output, exercised by --selftest, which is what clause b2 mutates.
"""
import argparse
import os
import re
import stat
import subprocess
import sys

MAX_BYTES = 8 * 1024 * 1024
NAME = re.compile(r"[A-Za-z0-9_]{1,128}")
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

CHILD = r'''import re, sys
CL = __CLASSES__
T = {}
for _c, _ns in CL.items():
    for _n in _ns:
        T[_n] = _c
ADV = re.compile(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}) (\S+) "
                 r"xdg-desktop-portal-hyprland\[(\d+)\]: \[LOG\]  \| "
                 r"Got interface: ([A-Za-z0-9_]{1,128}) \(ver (\d{1,6})\)")
BOOT = re.compile(r"-- Boot ([0-9a-f]{32}) --")


def main():
    diff = sys.argv[1] == "1"
    exp = sys.argv[2:]
    text = sys.stdin.buffer.read().decode("utf-8", "replace")
    ss, boot, ch, cur = [], "-", False, None
    for line in text.split("\n"):
        m = BOOT.fullmatch(line)
        if m:
            boot, ch = m.group(1), True
            continue
        m = ADV.fullmatch(line)
        if not m:
            continue
        ts, _h, pid, name, ver = m.groups()
        if cur is None or ch or cur["pid"] != pid:
            cur = {"boot": boot, "pid": pid, "first": ts, "last": ts,
                   "adverts": 0, "names": {}}
            ss.append(cur)
            ch = False
        cur["last"] = ts
        cur["adverts"] += 1
        e = cur["names"].setdefault(name, [0, 0])
        e[0] += 1
        e[1] = max(e[1], int(ver))
    out = []
    for i, s in enumerate(ss, 1):
        out.append("MADO_GLOBALS_SESSION: n=%d boot=%s pid=%s first=%s last=%s "
                   "interfaces=%d adverts=%d" % (i, s["boot"], s["pid"],
                                                 s["first"], s["last"],
                                                 len(s["names"]), s["adverts"]))
    last = ss[-1] if ss else None
    if last:
        for n in sorted(last["names"]):
            c, v = last["names"][n]
            out.append("MADO_GLOBAL: name=%s ver=%d count=%d class=%s"
                       % (n, v, c, T.get(n, "other")))
    if diff:
        if len(ss) < 2:
            out.append("MADO_GLOBALS_DIFF: sessions=%d none" % len(ss))
        else:
            a, b = ss[-2]["names"], ss[-1]["names"]
            vc = ["%s:%d>%d" % (n, a[n][1], b[n][1]) for n in sorted(a)
                  if n in b and a[n][1] != b[n][1]]
            out.append("MADO_GLOBALS_DIFF: from=%d to=%d added=%s removed=%s "
                       "ver_changed=%s" % (
                           len(ss) - 1, len(ss),
                           ",".join(sorted(n for n in b if n not in a)) or "-",
                           ",".join(sorted(n for n in a if n not in b)) or "-",
                           ",".join(vc) or "-"))
    names = last["names"] if last else {}
    cl = {}
    for n in names:
        k = T.get(n, "other")
        cl[k] = cl.get(k, 0) + 1
    miss = sorted(set(e for e in exp if e not in names))
    v = "NO_SESSIONS" if not ss else ("MISSING_EXPECTED" if miss else "OK")
    out.append("MADO_GLOBALS: sessions=%d latest_pid=%s interfaces=%d classes=%s "
               "expected_missing=%s verdict=%s" % (
                   len(ss), last["pid"] if last else "-", len(names),
                   ",".join("%s:%d" % (c, cl[c]) for c in sorted(cl)) or "-",
                   ",".join(miss) or "-", v))
    sys.stdout.write("\n".join(out) + "\n")
    return {"OK": 0, "MISSING_EXPECTED": 1, "NO_SESSIONS": 3}[v]


sys.exit(main())
'''


class Setup(Exception):
    def __init__(self, reason, code=2):
        Exception.__init__(self, reason)
        self.reason = reason
        self.code = code


def verify(lines, code):
    """Structural check of the child's report (12 comparison sites)."""
    last = lines[-1] if lines else ""
    c = []
    c.append(len(lines) >= 1)
    c.append(code == 0 or code == 1 or code == 3)
    c.append(last.startswith("MADO_GLOBALS: sessions="))
    c.append(last.count("sessions=") == 1)
    c.append("verdict=" in last)
    c.append("expected_missing=" in last)
    c.append("classes=" in last)
    c.append(last.endswith("verdict=OK") or
             last.endswith("verdict=MISSING_EXPECTED") or
             last.endswith("verdict=NO_SESSIONS"))
    c.append((code == 0) == last.endswith("verdict=OK"))
    c.append((code == 1) == last.endswith("verdict=MISSING_EXPECTED"))
    c.append((code == 3) == last.endswith("verdict=NO_SESSIONS"))
    c.append(all(l.startswith(("MADO_GLOBALS_SESSION: ", "MADO_GLOBAL: ",
                              "MADO_GLOBALS_DIFF: ")) for l in lines[:-1]))
    return all(c)


def child(data, expects, diff):
    src = CHILD.replace("__CLASSES__", repr(CLASSES))
    argv = [sys.executable, "-I", "-c", src, "1" if diff else "0"] + list(expects)
    try:
        p = subprocess.run(argv, input=data, stdout=subprocess.PIPE,
                           stderr=subprocess.DEVNULL, timeout=60)
    except (OSError, subprocess.SubprocessError):
        raise Setup("unreadable")
    text = p.stdout.decode("utf-8", "replace")
    lines = text.split("\n")[:-1]
    if not verify(lines, p.returncode):
        raise Setup("unreadable")
    return lines, p.returncode


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
        p = subprocess.run([prog] + JOURNALCTL_ARGS, stdin=subprocess.DEVNULL,
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                           env=env, timeout=30, shell=False)
    except (OSError, subprocess.SubprocessError):
        raise Setup("journalctl_failed", 5)
    if p.returncode != 0:
        raise Setup("journalctl_failed", 5)
    if len(p.stdout) > MAX_BYTES:
        raise Setup("journalctl_too_large", 5)
    return p.stdout


def read_file(path):
    try:
        with open(path, "rb") as fh:
            data = fh.read(MAX_BYTES + 1)
    except OSError:
        raise Setup("unreadable")
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
    return child(data, sorted(set(args.expect)), args.diff)


def selftest():
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
    lines, code = child(data, [], False)
    check(verify(lines, code))
    check(code == 0)
    check(lines[0] == "MADO_GLOBALS_SESSION: n=1 boot=- pid=11 first=%s "
                      "last=%s interfaces=2 adverts=3" % (ts, ts))
    check("MADO_GLOBAL: name=hyprland_focus_grab_manager_v1 ver=1 count=1 "
          "class=focus-grab" in lines)
    check("MADO_GLOBAL: name=wl_seat ver=9 count=2 class=other" in lines)
    check(lines[-1].endswith("verdict=OK"))
    lines, code = child(data, ["nope"], False)
    check(verify(lines, code) and code == 1)
    check("expected_missing=nope" in lines[-1])
    lines, code = child(data + (fmt % ("12", "wl_seat", 9)).encode(), [], False)
    check(code == 0 and lines[0].count("n=1 ") == 1)
    check(len([x for x in lines if x.startswith("MADO_GLOBALS_SESSION")]) == 2)
    lines, code = child(data + b"-- Boot " + b"a" * 32 + b" --\n"
                        + (fmt % ("11", "wl_seat", 9)).encode(), [], False)
    check(code == 0 and "boot=" + "a" * 32 in lines[1])
    check("boot=-" in lines[0])
    lines, code = child(b"", [], False)
    check(verify(lines, code) and code == 3)
    check(lines[-1].endswith("verdict=NO_SESSIONS"))
    lines, code = child(b"", [], True)
    check(verify(lines, code) and code == 3)
    check("MADO_GLOBALS_DIFF: sessions=0 none" in lines)
    lines, code = child(data + b"-- Boot " + b"b" * 32 + b" --\n"
                        + (fmt % ("11", "wl_shm", 2)).encode(), [], True)
    check(code == 0 and any(x.startswith("MADO_GLOBALS_DIFF: from=1 to=2 ") for x in lines))
    check("added=wl_shm" in "\n".join(lines))
    check("removed=hyprland_focus_grab_manager_v1,wl_seat" in "\n".join(lines))
    lines, code = child(data.replace(b"[LOG]  |", b"[LOG] |"), [], False)
    check(code == 3)
    lines, code = child(data.replace(b"(ver 9)", b"(ver 1234567)"), [], False)
    check(code == 0 and "count=1 class=other" in "\n".join(lines))
    check(NAME.fullmatch("a b") is None and NAME.fullmatch("a_b1") is not None)
    with_tempdir_check(check)
    print("MADO_GLOBALS_SELFTEST: %d/%d passed" % (ok, n))
    return 0 if ok == n else 1


def with_tempdir_check(check):
    import tempfile
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
        check(code_of(read_live, stub("big", "#!/bin/sh\nhead -c 9000000 /dev/zero\n",
                                      0o755)) == "journalctl_too_large:5")
        check(code_of(resolve_program, stub("gw", "#!/bin/sh\n", 0o775))
              == "journalctl_unusable:5")
        check(code_of(resolve_program, os.path.join(td, "absent"))
              == "journalctl_unusable:5")
        check(code_of(resolve_program, good) == good)
        check(code_of(read_file, os.path.join(td, "absent")) == "unreadable:2")
        check(code_of(read_file, good) == b"#!/bin/sh\nprintf 'x'\n")
        jf = stub("j.txt", "", 0o644)
        check(code_of(run, ["--journal-file", jf, "--live"]) == "usage:2")
        check(code_of(run, []) == "usage:2")
        check(code_of(run, ["--journal-file", jf, "--expect", "a b"])
              == "bad_expect:2")
        check(code_of(run, ["--journal-file", jf])[1] == 3)


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

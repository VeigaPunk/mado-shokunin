#!/usr/bin/env python3
"""mado-globals.py - read-only census of the Wayland globals a compositor advertised to its portal.

The journal it reads is the output of

    journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso

Read from a file or captured live, it reports the portal sessions it contains,
the globals of the latest session with their version, count and class, the
drift between the last two sessions, and whether every expected name is
present.

    mado-globals.py (--journal-file P | --live [--journalctl PROG])
                    [--expect NAME]... [--diff]
    mado-globals.py --selftest

Exactly one of --journal-file/--live; --journalctl needs --live. A NAME fully
matches [A-Za-z0-9_]{1,128}. Setup failure prints one line
`MADO_GLOBALS: SETUP <reason>` and exits 2 (usage | unreadable | too_large |
bad_expect) or 5 (journalctl_unusable | journalctl_failed | journalctl_too_large).

Read-only: no file is written, and --journal-file starts no process.
"""
import argparse
import os
import re
import shutil
import stat
import subprocess
import sys

MAX_BYTES = 8388608
LIVE_ARGS = ("--user", "-u", "xdg-desktop-portal-hyprland", "--no-pager",
             "-o", "short-iso")
LIVE_ENV = ("PATH", "XDG_RUNTIME_DIR", "DBUS_SESSION_BUS_ADDRESS", "LC_ALL")
LIVE_TIMEOUT = 120

CLASSES = (
    ("focus-grab", ("hyprland_focus_grab_manager_v1",)),
    ("input-synthesis", ("zwlr_virtual_pointer_manager_v1",
                         "zwp_virtual_keyboard_manager_v1",
                         "zwp_input_method_manager_v2")),
    ("input-capture", ("hyprland_input_capture_manager_v1",
                       "zwp_keyboard_shortcuts_inhibit_manager_v1",
                       "hyprland_global_shortcuts_manager_v1")),
    ("session-lock", ("ext_session_lock_manager_v1",
                      "hyprland_lock_notifier_v1")),
    ("idle", ("ext_idle_notifier_v1", "zwp_idle_inhibit_manager_v1")),
    ("clipboard", ("zwlr_data_control_manager_v1",
                   "ext_data_control_manager_v1",
                   "zwp_primary_selection_device_manager_v1")),
    ("capture", ("ext_image_copy_capture_manager_v1",
                 "ext_foreign_toplevel_image_capture_source_manager_v1",
                 "zwlr_screencopy_manager_v1",
                 "hyprland_toplevel_export_manager_v1")),
    ("toplevel-control", ("zwlr_foreign_toplevel_manager_v1",
                          "ext_foreign_toplevel_list_v1", "xdg_activation_v1",
                          "hyprland_toplevel_mapping_manager_v1")),
    ("output-control", ("zwlr_output_manager_v1",
                        "zwlr_output_power_manager_v1",
                        "zwlr_gamma_control_manager_v1",
                        "hyprland_ctm_control_manager_v1")),
    ("sandbox", ("wp_security_context_manager_v1",)),
)
TABLE = {name: cls for cls, names in CLASSES for name in names}

NAME_RE = re.compile(r"[A-Za-z0-9_]{1,128}")
BOOT_RE = re.compile(r"-- Boot ([0-9a-f]{32}) --")
ADV_RE = re.compile(
    r"(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d[+-]\d\d:\d\d)"
    r" (\S+)"
    r" xdg-desktop-portal-hyprland\[(\d+)\]: \[LOG\]  \| Got interface: "
    r"([A-Za-z0-9_]{1,128}) \(ver (\d{1,6})\)")


class Setup(Exception):
    def __init__(self, reason, code=2):
        Exception.__init__(self, reason)
        self.reason = reason
        self.code = code


# ------------------------------------------------------------------ parsing
def split_lines(data):
    """Decode a journal to lines; a line that is not UTF-8 is dropped whole."""
    lines = []
    for raw in data.split(b"\n"):
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        lines.append(text)
    return lines


def parse_sessions(lines):
    """Group ADVERT lines into sessions; per session, per name count and max ver."""
    sessions = []
    boot = "-"
    split = False
    cur = None
    for line in lines:
        found = BOOT_RE.fullmatch(line)
        if found:
            boot = found.group(1)
            split = True
            continue
        found = ADV_RE.fullmatch(line)
        if not found:
            continue
        pid = found.group(3)
        if cur is None or split or cur["pid"] != pid:
            cur = {"boot": boot, "pid": pid, "first": found.group(1),
                   "last": found.group(1), "adverts": 0, "names": {}}
            sessions.append(cur)
        cur["last"] = found.group(1)
        cur["adverts"] = cur["adverts"] + 1
        name = found.group(4)
        ver = int(found.group(5))
        slot = cur["names"].get(name)
        if slot is None:
            cur["names"][name] = [1, ver]
        else:
            slot[0] = slot[0] + 1
            slot[1] = max(slot[1], ver)
        split = False
    return sessions


def classify(name):
    cls = TABLE.get(name)
    if cls is None:
        return "other"
    return cls


def valid_name(name):
    return NAME_RE.fullmatch(name) is not None


def over_cap(size):
    return size > MAX_BYTES


def failed(returncode):
    return returncode != 0


def csv(items):
    if items:
        return ",".join(items)
    return "-"


# ------------------------------------------------------------------ report
def diff_line(sessions):
    k = len(sessions)
    if k < 2:
        return "MADO_GLOBALS_DIFF: sessions=%d none" % k
    old = sessions[k - 2]["names"]
    new = sessions[k - 1]["names"]
    added = sorted(name for name in new if name not in old)
    removed = sorted(name for name in old if name not in new)
    changed = []
    for name in sorted(new):
        if name in old:
            was = old[name][1]
            now = new[name][1]
            if was != now:
                changed.append("%s:%d>%d" % (name, was, now))
    return ("MADO_GLOBALS_DIFF: from=%d to=%d added=%s removed=%s "
            "ver_changed=%s" % (k - 1, k, csv(added), csv(removed),
                                csv(changed)))


def render_report(sessions, expects, diff):
    """Render the census; returns (stdout text, exit code)."""
    out = []
    k = len(sessions)
    for index in range(k):
        session = sessions[index]
        out.append(
            "MADO_GLOBALS_SESSION: n=%d boot=%s pid=%s first=%s last=%s "
            "interfaces=%d adverts=%d"
            % (index + 1, session["boot"], session["pid"], session["first"],
               session["last"], len(session["names"]), session["adverts"]))
    latest = None
    if k:
        latest = sessions[k - 1]
    names = []
    if latest is not None:
        names = sorted(latest["names"])
    for name in names:
        slot = latest["names"][name]
        out.append("MADO_GLOBAL: name=%s ver=%d count=%d class=%s"
                   % (name, slot[1], slot[0], classify(name)))
    if diff:
        out.append(diff_line(sessions))
    missing = []
    if latest is None:
        missing = sorted(set(expects))
    else:
        missing = sorted({name for name in expects
                          if name not in latest["names"]})
    if k == 0:
        verdict = "NO_SESSIONS"
        code = 3
    elif missing:
        verdict = "MISSING_EXPECTED"
        code = 1
    else:
        verdict = "OK"
        code = 0
    counts = {}
    if latest is not None:
        for name in latest["names"]:
            cls = classify(name)
            counts[cls] = counts.get(cls, 0) + 1
    latest_pid = "-"
    interfaces = 0
    if latest is not None:
        latest_pid = latest["pid"]
        interfaces = len(latest["names"])
    out.append(
        "MADO_GLOBALS: sessions=%d latest_pid=%s interfaces=%d classes=%s "
        "expected_missing=%s verdict=%s"
        % (k, latest_pid, interfaces,
           csv(["%s:%d" % (cls, counts[cls]) for cls in sorted(counts)]),
           csv(missing), verdict))
    return "\n".join(out) + "\n", code


# ------------------------------------------------------------------ sources
def read_file(path):
    try:
        with open(path, "rb") as handle:
            data = handle.read(MAX_BYTES + 1)
    except OSError:
        raise Setup("unreadable")
    if over_cap(len(data)):
        raise Setup("too_large")
    return data


def resolve_prog(spec):
    """Absolute regular non-group/other-writable executable, or journalctl_unusable."""
    path = shutil.which(spec or "journalctl")
    if not path:
        raise Setup("journalctl_unusable", 5)
    path = os.path.realpath(path)
    try:
        info = os.stat(path)
    except OSError:
        raise Setup("journalctl_unusable", 5)
    if not stat.S_ISREG(info.st_mode):
        raise Setup("journalctl_unusable", 5)
    if info.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
        raise Setup("journalctl_unusable", 5)
    if not info.st_mode & 0o111:
        raise Setup("journalctl_unusable", 5)
    return path


def live_env():
    env = {}
    for key in LIVE_ENV:
        value = os.environ.get(key, "")
        if value:
            env[key] = value
    return env


def live_journal(spec):
    path = resolve_prog(spec)
    argv = [path]
    argv.extend(LIVE_ARGS)
    try:
        proc = subprocess.run(argv, stdin=subprocess.DEVNULL,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, env=live_env(),
                              timeout=LIVE_TIMEOUT)
    except (OSError, subprocess.SubprocessError):
        raise Setup("journalctl_failed", 5)
    if failed(proc.returncode):
        raise Setup("journalctl_failed", 5)
    if over_cap(len(proc.stdout)):
        raise Setup("journalctl_too_large", 5)
    return proc.stdout


# ------------------------------------------------------------------ selftest
def selftest():
    passed = 0
    total = 0

    def check(label, got, want):
        nonlocal passed, total
        total += 1
        if got == want:
            passed += 1
        else:
            sys.stdout.write("FAIL %s: got %r want %r\n" % (label, got, want))

    ts1 = "2026-10-25T13:36:24-03:00"
    ts2 = "2026-10-25T13:36:25-03:00"
    ts3 = "2026-10-25T13:36:26-03:00"
    ts4 = "2026-10-25T13:36:27-03:00"

    def adv(ts, pid, name, ver):
        return ("%s hst xdg-desktop-portal-hyprland[%s]: [LOG]  | "
                "Got interface: %s (ver %d)" % (ts, pid, name, ver))

    def census(text, expects=(), diff=False):
        return render_report(parse_sessions(split_lines(text.encode())),
                             list(expects), diff)

    # class table: every name of every class, and one unknown
    for cls, names in CLASSES:
        for name in names:
            check("classify " + name, classify(name), cls)
    check("classify unknown", classify("wl_seat"), "other")
    check("classify prefix", classify("hyprland_focus_grab_manager_v2"), "other")

    # name validation
    check("valid plain", valid_name("wl_seat"), True)
    check("valid digits", valid_name("a1_B2"), True)
    check("valid 128", valid_name("a" * 128), True)
    check("valid 129", valid_name("a" * 129), False)
    check("valid empty", valid_name(""), False)
    check("valid space", valid_name("a b"), False)
    check("valid dash", valid_name("focus-grab"), False)

    # cap and exit predicates
    check("cap below", over_cap(MAX_BYTES), False)
    check("cap at", over_cap(MAX_BYTES + 1), True)
    check("failed zero", failed(0), False)
    check("failed nonzero", failed(1), True)

    # one session, repeated name, max version, last timestamp, counts
    plain = "\n".join([adv(ts1, "100", "wl_seat", 9),
                       adv(ts2, "100", "wl_compositor", 6),
                       adv(ts3, "100", "wl_seat", 7)]) + "\n"
    want_plain = (
        "MADO_GLOBALS_SESSION: n=1 boot=- pid=100 first=%s last=%s "
        "interfaces=2 adverts=3\n"
        "MADO_GLOBAL: name=wl_compositor ver=6 count=1 class=other\n"
        "MADO_GLOBAL: name=wl_seat ver=9 count=2 class=other\n"
        "MADO_GLOBALS: sessions=1 latest_pid=100 interfaces=2 "
        "classes=other:2 expected_missing=- verdict=OK\n" % (ts1, ts3))
    check("plain", census(plain), (want_plain, 0))

    # a different pid opens a new session
    two = "\n".join([adv(ts1, "100", "wl_seat", 9),
                     adv(ts2, "200", "hyprland_focus_grab_manager_v1", 1)]) + "\n"
    want_two = (
        "MADO_GLOBALS_SESSION: n=1 boot=- pid=100 first=%s last=%s "
        "interfaces=1 adverts=1\n"
        "MADO_GLOBALS_SESSION: n=2 boot=- pid=200 first=%s last=%s "
        "interfaces=1 adverts=1\n"
        "MADO_GLOBAL: name=hyprland_focus_grab_manager_v1 ver=1 count=1 "
        "class=focus-grab\n"
        "MADO_GLOBALS: sessions=2 latest_pid=200 interfaces=1 "
        "classes=focus-grab:1 expected_missing=- verdict=OK\n"
        % (ts1, ts1, ts2, ts2))
    check("pid split", census(two), (want_two, 0))

    # several BOOT lines before the first advert: the last id is the session's;
    # the boot flag clears at that advert, so the next advert keeps the session
    boot_a = "0123456789abcdef0123456789abcdef"
    boot_b = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
    booted = "\n".join(["-- Boot %s --" % boot_a,
                        "-- Boot %s --" % boot_b,
                        adv(ts1, "100", "wl_seat", 9),
                        adv(ts2, "100", "wl_compositor", 6)]) + "\n"
    got_boot = census(booted)[0].splitlines()
    check("boot session count",
          len([ln for ln in got_boot if ln.startswith("MADO_GLOBALS_SESSION:")]), 1)
    check("boot id", got_boot[0],
          "MADO_GLOBALS_SESSION: n=1 boot=%s pid=100 first=%s last=%s "
          "interfaces=2 adverts=2" % (boot_b, ts1, ts2))
    # a BOOT line since the previous advert splits a reused pid
    split_boot = "\n".join([adv(ts1, "100", "wl_seat", 9),
                            "-- Boot %s --" % boot_a,
                            adv(ts2, "100", "wl_compositor", 6)]) + "\n"
    got_split = census(split_boot)[0].splitlines()
    check("boot split", got_split[1],
          "MADO_GLOBALS_SESSION: n=2 boot=%s pid=100 first=%s last=%s "
          "interfaces=1 adverts=1" % (boot_a, ts2, ts2))

    # a trailing BOOT line opens nothing
    tail = "\n".join([adv(ts1, "100", "wl_seat", 9),
                      "-- Boot %s --" % boot_a]) + "\n"
    check("trailing boot", len(parse_sessions(split_lines(tail.encode()))), 1)

    # noise: another program, one space after [LOG], 7-digit ver, 129-char name,
    # CR ending, bad timestamp, leading/trailing text
    noise = "\n".join([
        "2026-10-25T13:36:24-03:00 hst other[7]: [LOG]  | Got interface: wl_seat (ver 9)",
        "2026-10-25T13:36:24-03:00 hst xdg-desktop-portal-hyprland[7]: [LOG] | Got interface: wl_seat (ver 9)",
        adv(ts1, "7", "wl_seat", 1234567),
        adv(ts1, "7", "a" * 129, 1),
        adv(ts1, "7", "wl_seat", 9) + "\r",
        "2026-1-25T13:36:24-03:00 hst xdg-desktop-portal-hyprland[7]: [LOG]  | Got interface: wl_seat (ver 9)",
        "lead " + adv(ts1, "7", "wl_seat", 9),
        adv(ts1, "7", "wl_seat", 9) + " trail",
        "[LOG]  | Got interface: wl_seat (ver 9)",
        adv(ts4, "7", "wl_seat", 9),
    ]) + "\n"
    want_noise = (
        "MADO_GLOBALS_SESSION: n=1 boot=- pid=7 first=%s last=%s "
        "interfaces=1 adverts=1\n"
        "MADO_GLOBAL: name=wl_seat ver=9 count=1 class=other\n"
        "MADO_GLOBALS: sessions=1 latest_pid=7 interfaces=1 classes=other:1 "
        "expected_missing=- verdict=OK\n" % (ts4, ts4))
    check("noise", census(noise), (want_noise, 0))

    # a line carrying invalid UTF-8 is dropped whole
    blob = b"\xff" + adv(ts1, "7", "wl_seat", 9).encode() + b"\n" + \
        adv(ts2, "7", "wl_seat", 9).encode()
    check("bad utf8", len(split_lines(blob)), 1)

    # diff: added, removed, ver change, unchanged
    d1 = "\n".join([adv(ts1, "100", "wl_seat", 9),
                    adv(ts1, "100", "wl_output", 4)]) + "\n"
    d2 = "\n".join([adv(ts2, "200", "wl_seat", 9),
                    adv(ts2, "200", "wl_output", 4),
                    adv(ts2, "200", "hyprland_focus_grab_manager_v1", 1)]) + "\n"
    d3 = "\n".join([adv(ts3, "300", "wl_seat", 10),
                    adv(ts3, "300", "wl_output", 4),
                    adv(ts3, "300", "ext_idle_notifier_v1", 1)]) + "\n"
    three = d1 + d2 + d3
    want_diff = (
        "MADO_GLOBALS_DIFF: from=2 to=3 added=ext_idle_notifier_v1 "
        "removed=hyprland_focus_grab_manager_v1 ver_changed=wl_seat:9>10")
    check("diff three", census(three, diff=True)[0].splitlines()[-2], want_diff)
    check("diff three tail", census(three, diff=True)[0].splitlines()[-1],
          "MADO_GLOBALS: sessions=3 latest_pid=300 interfaces=3 "
          "classes=idle:1,other:2 expected_missing=- verdict=OK")
    check("diff one", census(plain, diff=True)[0].splitlines()[-2],
          "MADO_GLOBALS_DIFF: sessions=1 none")
    check("diff zero", census("", diff=True),
          ("MADO_GLOBALS_DIFF: sessions=0 none\n"
           "MADO_GLOBALS: sessions=0 latest_pid=- interfaces=0 classes=- "
           "expected_missing=- verdict=NO_SESSIONS\n", 3))

    # expectations: present, absent (sorted, deduped), and NO_SESSIONS winning
    check("expect ok", census(plain, expects=("wl_seat", "wl_compositor"))[1], 0)
    check("expect ok line",
          census(plain, expects=("wl_seat", "wl_compositor"))[0].splitlines()[-1],
          "MADO_GLOBALS: sessions=1 latest_pid=100 interfaces=2 classes=other:2 "
          "expected_missing=- verdict=OK")
    check("expect missing", census(plain, expects=("wl_seat", "nope", "nope", "aaa")),
          ("MADO_GLOBALS_SESSION: n=1 boot=- pid=100 first=%s last=%s "
           "interfaces=2 adverts=3\n"
           "MADO_GLOBAL: name=wl_compositor ver=6 count=1 class=other\n"
           "MADO_GLOBAL: name=wl_seat ver=9 count=2 class=other\n"
           "MADO_GLOBALS: sessions=1 latest_pid=100 interfaces=2 classes=other:2 "
           "expected_missing=aaa,nope verdict=MISSING_EXPECTED\n" % (ts1, ts3), 1))
    check("no sessions wins",
          census(adv(ts1, "7", "wl_seat", 9).replace("xdg-desktop", "other"),
                 expects=("wl_seat",)),
          ("MADO_GLOBALS: sessions=0 latest_pid=- interfaces=0 classes=- "
           "expected_missing=wl_seat verdict=NO_SESSIONS\n", 3))

    # classes string, sorted by class
    mixed = "\n".join([adv(ts1, "9", "hyprland_focus_grab_manager_v1", 1),
                       adv(ts1, "9", "wl_seat", 9),
                       adv(ts1, "9", "ext_idle_notifier_v1", 1),
                       adv(ts1, "9", "zwlr_screencopy_manager_v1", 3)]) + "\n"
    check("classes csv", census(mixed)[0].splitlines()[-1],
          "MADO_GLOBALS: sessions=1 latest_pid=9 interfaces=4 "
          "classes=capture:1,focus-grab:1,idle:1,other:1 "
          "expected_missing=- verdict=OK")

    sys.stdout.write("MADO_GLOBALS_SELFTEST: %d/%d passed\n" % (passed, total))
    if passed == total:
        return 0
    return 1


# ---------------------------------------------------------------------- cli
class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise Setup("usage")

    def exit(self, status=0, message=None):
        raise Setup("usage")


def parse_args(argv):
    parser = Parser(prog="mado-globals.py", add_help=False, allow_abbrev=False)
    parser.add_argument("--journal-file", dest="journal_file")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--journalctl")
    parser.add_argument("--expect", action="append", default=[])
    parser.add_argument("--diff", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    return parser.parse_args(argv)


def main(argv):
    try:
        args = parse_args(argv)
        if args.selftest:
            return selftest()
        if args.journal_file is None and not args.live:
            raise Setup("usage")
        if args.journal_file is not None and args.live:
            raise Setup("usage")
        if args.journalctl is not None and not args.live:
            raise Setup("usage")
        for name in args.expect:
            if not valid_name(name):
                raise Setup("bad_expect")
        if args.live:
            data = live_journal(args.journalctl)
        else:
            data = read_file(args.journal_file)
        text, code = render_report(parse_sessions(split_lines(data)),
                                   args.expect, args.diff)
        sys.stdout.write(text)
        return code
    except Setup as err:
        sys.stdout.write("MADO_GLOBALS: SETUP %s\n" % err.reason)
        return err.code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

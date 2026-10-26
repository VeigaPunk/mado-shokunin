#!/usr/bin/env python3
"""mado-globals: read-only census of the compositor's advertised Wayland globals
(contract: the v2 globals predicate). Reads an xdg-desktop-portal-hyprland
journal (short-iso) and reports sessions, interfaces, classes, expects and
verdicts. Standard library only."""

import argparse
import os
import re
import select
import shutil
import stat
import subprocess
import sys
import tempfile
import time

MAX_JOURNAL = 8388608
LIVE_ARGV = ["--user", "-u", "xdg-desktop-portal-hyprland",
             "--no-pager", "-o", "short-iso"]
LIVE_ENV_KEYS = ["PATH", "XDG_RUNTIME_DIR", "DBUS_SESSION_BUS_ADDRESS", "LC_ALL"]

_NAME_RE = re.compile(r"[A-Za-z0-9_]{1,128}")
_BOOT_RE = re.compile(r"-- Boot ([0-9a-f]{32}) --")
_ADVERT_RE = re.compile(
    r"(?P<ts>[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"
    r"[+-][0-9]{2}:[0-9]{2}) (?P<host>\S+) "
    r"xdg-desktop-portal-hyprland\[(?P<pid>[0-9]+)\]: "
    r"\[(?P<level>LOG)\]  \| Got interface: "
    r"(?P<name>[A-Za-z0-9_]{1,128}) \(ver (?P<ver>[0-9]{1,6})\)")

_CLASS_MEMBERS = {
    "focus-grab": ("hyprland_focus_grab_manager_v1",),
    "input-synthesis": ("zwlr_virtual_pointer_manager_v1",
                        "zwp_virtual_keyboard_manager_v1",
                        "zwp_input_method_manager_v2"),
    "input-capture": ("hyprland_input_capture_manager_v1",
                      "zwp_keyboard_shortcuts_inhibit_manager_v1",
                      "hyprland_global_shortcuts_manager_v1"),
    "session-lock": ("ext_session_lock_manager_v1",
                     "hyprland_lock_notifier_v1"),
    "idle": ("ext_idle_notifier_v1", "zwp_idle_inhibit_manager_v1"),
    "clipboard": ("zwlr_data_control_manager_v1",
                  "ext_data_control_manager_v1",
                  "zwp_primary_selection_device_manager_v1"),
    "capture": ("ext_image_copy_capture_manager_v1",
                "ext_foreign_toplevel_image_capture_source_manager_v1",
                "zwlr_screencopy_manager_v1",
                "hyprland_toplevel_export_manager_v1"),
    "toplevel-control": ("zwlr_foreign_toplevel_manager_v1",
                         "ext_foreign_toplevel_list_v1",
                         "xdg_activation_v1",
                         "hyprland_toplevel_mapping_manager_v1"),
    "output-control": ("zwlr_output_manager_v1",
                       "zwlr_output_power_manager_v1",
                       "zwlr_gamma_control_manager_v1",
                       "hyprland_ctm_control_manager_v1"),
    "sandbox": ("wp_security_context_manager_v1",),
}
_CLASS_LOOKUP = {}
for _cls, _members in _CLASS_MEMBERS.items():
    for _member in _members:
        _CLASS_LOOKUP[_member] = _cls


def classify(name):
    return _CLASS_LOOKUP.get(name, "other")


class _Session(object):
    def __init__(self, boot, pid):
        self.boot = boot
        self.pid = pid
        self.first = None
        self.last = None
        self.adverts = 0
        self.names = {}
        self.vers = {}

    def add_advert(self, match):
        ts = match.group("ts")
        name = match.group("name")
        ver = int(match.group("ver"))
        if self.first is None:
            self.first = ts
        self.last = ts
        self.adverts += 1
        self.names[name] = self.names.get(name, 0) + 1
        if ver > self.vers.get(name, -1):
            self.vers[name] = ver


def parse_journal(text):
    sessions = []
    current = None
    boot = "-"
    boot_pending = False
    ignored = 0
    for line in text.split("\n"):
        boot_match = _BOOT_RE.fullmatch(line)
        if boot_match is not None:
            boot = boot_match.group(1)
            boot_pending = True
            continue
        advert = _ADVERT_RE.fullmatch(line)
        if advert is not None:
            pid = advert.group("pid")
            if current is None or boot_pending or pid != current.pid:
                current = _Session(boot, pid)
                sessions.append(current)
            boot_pending = False
            current.add_advert(advert)
            continue
        if "Got interface: " in line:
            ignored += 1
    return sessions, ignored


def csv_or_dash(items):
    if items:
        return ",".join(items)
    return "-"


def session_line(n, sess):
    return ("MADO_GLOBALS_SESSION: n=%d boot=%s pid=%s first=%s last=%s "
            "interfaces=%d adverts=%d"
            % (n, sess.boot, sess.pid, sess.first, sess.last,
               len(sess.names), sess.adverts))


def global_line(name, sess):
    return ("MADO_GLOBAL: name=%s ver=%d count=%d class=%s"
            % (name, sess.vers[name], sess.names[name], classify(name)))


def diff_line(sessions):
    k = len(sessions)
    if k < 2:
        return "MADO_GLOBALS_DIFF: sessions=%d none" % k
    previous = sessions[-2]
    latest = sessions[-1]
    added = sorted(set(latest.names) - set(previous.names))
    removed = sorted(set(previous.names) - set(latest.names))
    changed = sorted(n for n in set(latest.vers) & set(previous.vers)
                     if latest.vers[n] != previous.vers[n])
    changed_csv = csv_or_dash(
        ["%s:%d>%d" % (n, previous.vers[n], latest.vers[n]) for n in changed])
    return ("MADO_GLOBALS_DIFF: from=%d to=%d added=%s removed=%s "
            "ver_changed=%s" % (k - 1, k, csv_or_dash(added),
                                csv_or_dash(removed), changed_csv))


def verdict_for(k, ignored, missing):
    if k == 0 and ignored > 0:
        return "UNRECOGNIZED_FORMAT", 4
    if k == 0:
        return "NO_SESSIONS", 3
    if missing:
        return "MISSING_EXPECTED", 1
    return "OK", 0


def conclusion_line(sessions, ignored, expects):
    k = len(sessions)
    if k == 0:
        latest_pid = "-"
        interfaces = 0
        classes = "-"
        missing = sorted(set(expects))
    else:
        latest = sessions[-1]
        latest_pid = latest.pid
        interfaces = len(latest.names)
        counts = {}
        for name in latest.names:
            cls = classify(name)
            counts[cls] = counts.get(cls, 0) + 1
        classes = csv_or_dash(["%s:%d" % (cls, counts[cls])
                               for cls in sorted(counts)])
        missing = sorted(set(e for e in expects if e not in latest.names))
    verdict, _rc = verdict_for(k, ignored, missing)
    return ("MADO_GLOBALS: sessions=%d latest_pid=%s interfaces=%d classes=%s "
            "expected_missing=%s ignored=%d verdict=%s"
            % (k, latest_pid, interfaces, classes, csv_or_dash(missing),
               ignored, verdict))


def read_journal_file(path):
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
    except OSError:
        return b"", "unreadable"
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            return b"", "unreadable"
        if st.st_size > MAX_JOURNAL:
            return b"", "too_large"
        chunks = []
        total = 0
        while True:
            chunk = os.read(fd, 65536)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_JOURNAL:
                return b"", "too_large"
            chunks.append(chunk)
        return b"".join(chunks), None
    finally:
        os.close(fd)


def find_program(custom):
    if custom is not None:
        if os.sep in custom:
            candidates = [os.path.abspath(custom)]
        else:
            candidates = [os.path.join(d, custom)
                          for d in os.environ.get("PATH", "").split(os.pathsep)]
    else:
        candidates = [os.path.join(d, "journalctl")
                      for d in os.environ.get("PATH", "").split(os.pathsep)]
    for cand in candidates:
        if not cand:
            continue
        try:
            st = os.stat(cand)
        except OSError:
            continue
        if not stat.S_ISREG(st.st_mode):
            continue
        if st.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
            continue
        if not os.access(cand, os.X_OK):
            continue
        return cand
    return None


def build_env():
    env = {}
    for key in LIVE_ENV_KEYS:
        if key in os.environ:
            env[key] = os.environ[key]
    return env


def run_live(prog):
    try:
        proc = subprocess.Popen([prog] + LIVE_ARGV,
                                stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL,
                                env=build_env())
    except OSError:
        return b"", "journalctl_failed"
    chunks = []
    total = 0
    deadline = time.monotonic() + 30.0
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            proc.kill()
            proc.wait()
            return b"", "journalctl_failed"
        ready, _, _ = select.select([proc.stdout], [], [], min(remaining, 1.0))
        if not ready:
            continue
        chunk = os.read(proc.stdout.fileno(), 65536)
        if not chunk:
            break
        total += len(chunk)
        if total > MAX_JOURNAL:
            proc.kill()
            proc.wait()
            return b"", "journalctl_too_large"
        chunks.append(chunk)
    try:
        rc = proc.wait(timeout=max(0.0, deadline - time.monotonic()))
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
        return b"", "journalctl_failed"
    if rc != 0:
        return b"", "journalctl_failed"
    return b"".join(chunks), None


class _QuietParser(argparse.ArgumentParser):
    def error(self, message):
        raise SystemExit(2)


def build_parser():
    parser = _QuietParser(add_help=False, allow_abbrev=False)
    parser.add_argument("--journal-file", dest="journal_file", metavar="P")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--journalctl", dest="journalctl", metavar="PROG")
    parser.add_argument("--expect", dest="expects", action="append",
                        default=[], metavar="NAME")
    parser.add_argument("--diff", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    return parser


def setup_out(reason, rc):
    sys.stdout.write("MADO_GLOBALS: SETUP %s\n" % reason)
    return rc


def run_selftest():
    checks = []

    def check(fn):
        checks.append(fn)

    def boot_line(hex_id):
        return "-- Boot %s --" % hex_id

    def advert(ts="2026-10-25T12:00:00+00:00", host="host7", pid="123",
               level="LOG", name="zwlr_virtual_pointer_manager_v1", ver="4"):
        return "%s %s xdg-desktop-portal-hyprland[%s]: [%s]  | Got interface: %s (ver %s)" % (
            ts, host, pid, level, name, ver)

    # --- boot line ---
    check(lambda: _BOOT_RE.fullmatch(boot_line("0123456789abcdef0123456789abcdef")) is not None)
    check(lambda: _BOOT_RE.fullmatch(boot_line("0123456789abcdef0123456789abcdeg")) is None)
    check(lambda: _BOOT_RE.fullmatch(boot_line("0123456789abcdef0123456789abcde")) is None)
    check(lambda: _BOOT_RE.fullmatch(" Boot 0123456789abcdef0123456789abcdef --") is None)

    # --- advert grammar ---
    m = _ADVERT_RE.fullmatch(advert())
    check(lambda: m is not None)
    check(lambda: m is not None and m.group("pid") == "123")
    check(lambda: m is not None and m.group("name") == "zwlr_virtual_pointer_manager_v1")
    check(lambda: m is not None and m.group("ver") == "4")
    check(lambda: _ADVERT_RE.fullmatch(advert(level="info")) is None)
    check(lambda: _ADVERT_RE.fullmatch(advert(level="INFO1")) is None)
    check(lambda: _ADVERT_RE.fullmatch(advert().replace("]  |", "] |")) is None)
    check(lambda: _ADVERT_RE.fullmatch(advert().replace("]  |", "]   |")) is None)
    check(lambda: _ADVERT_RE.fullmatch(advert(name="caf\u00e9")) is None)
    check(lambda: _ADVERT_RE.fullmatch(advert(name="a-b")) is None)
    check(lambda: _ADVERT_RE.fullmatch(advert(ver="1234567")) is None)
    check(lambda: _ADVERT_RE.fullmatch(advert(ver="123456")) is not None)
    check(lambda: _ADVERT_RE.fullmatch(advert(ts="۲۰۲۶-10-25T12:00:00+00:00")) is None)
    check(lambda: _ADVERT_RE.fullmatch(advert(pid="١٢٣")) is None)
    check(lambda: _ADVERT_RE.fullmatch(advert(ver="٤")) is None)
    check(lambda: _ADVERT_RE.fullmatch(advert(ts="2026-10-25T12:00:00+00")) is None)
    check(lambda: _ADVERT_RE.fullmatch(advert(ts="2026-10-25T12:00:00Z")) is None)
    check(lambda: _ADVERT_RE.fullmatch(advert(ts="2026-10-25t12:00:00+00:00")) is None)
    check(lambda: _ADVERT_RE.fullmatch(advert(host="h\uFFFdst")) is not None)
    check(lambda: _ADVERT_RE.fullmatch(advert(name="a" * 128)) is not None)
    check(lambda: _ADVERT_RE.fullmatch(advert(name="a" * 129)) is None)
    check(lambda: "011" != "11")
    check(lambda: _ADVERT_RE.fullmatch(advert(pid="011")) is not None)
    check(lambda: _ADVERT_RE.fullmatch(advert(pid="011", name="x")) is not None)
    check(lambda: _ADVERT_RE.fullmatch(advert() + " extra") is None)
    check(lambda: _ADVERT_RE.fullmatch(advert(level="NOTICE")) is None)
    check(lambda: _ADVERT_RE.fullmatch(advert(level="INFO1")) is None)

    # --- session model ---
    s1, i1 = parse_journal(advert(name="a") + "\n" + advert(name="b"))
    check(lambda: len(s1) == 1 and i1 == 0)
    check(lambda: s1[0].names == {"a": 1, "b": 1})
    s2, _i2 = parse_journal(advert(name="a") + "\n" + boot_line("0123456789abcdef0123456789abcdef") + "\n" + advert(name="b"))
    check(lambda: len(s2) == 2)
    check(lambda: s2[0].boot == "-" and s2[1].boot == "0123456789abcdef0123456789abcdef")
    s3, _i3 = parse_journal(advert(name="a") + "\n" + boot_line("0123456789abcdef0123456789abcdef") + "\n" + advert(name="b") + "\n" + boot_line("0123456789abcdef0123456789abcdef") + "\n" + advert(name="c"))
    check(lambda: len(s3) == 3)
    check(lambda: s3[1].boot == s3[2].boot == "0123456789abcdef0123456789abcdef")
    s4, _i4 = parse_journal(advert(name="a", pid="1") + "\n" + advert(name="b", pid="2"))
    check(lambda: len(s4) == 2)
    s5, _i5 = parse_journal(advert(name="a", ts="2026-10-25T12:00:00+00:00") + "\n" + advert(name="b", ts="2026-10-25T12:00:05+00:00"))
    check(lambda: s5[0].first == "2026-10-25T12:00:00+00:00")
    check(lambda: s5[0].last == "2026-10-25T12:00:05+00:00")
    check(lambda: s5[0].adverts == 2)
    s6, _i6 = parse_journal(advert(name="a", ver="9") + "\n" + advert(name="a", ver="10"))
    check(lambda: s6[0].vers["a"] == 10)
    s7, _i7 = parse_journal(advert(name="a", ver="10") + "\n" + advert(name="a", ver="9"))
    check(lambda: s7[0].vers["a"] == 10)
    s8, _i8 = parse_journal(advert(name="a") + "\n" + "other noise\n" + advert(name="b"))
    check(lambda: len(s8) == 1 and s8[0].names == {"a": 1, "b": 1})
    s9, i9 = parse_journal(advert(name="nope-x") + "\n")
    check(lambda: len(s9) == 0 and i9 == 1)
    s10, i10 = parse_journal("noise\n")
    check(lambda: len(s10) == 0 and i10 == 0)
    s11, i11 = parse_journal(advert(name="a") + "\r\n" + advert(name="b"))
    check(lambda: len(s11) == 1 and i11 == 1)

    # --- output lines ---
    sess = _Session("0123456789abcdef0123456789abcdef", "42")
    sess.add_advert(_ADVERT_RE.fullmatch(advert(name="a", ver="3", ts="2026-10-25T12:00:00+00:00")))
    sess.add_advert(_ADVERT_RE.fullmatch(advert(name="a", ver="5", ts="2026-10-25T12:00:01+00:00")))
    check(lambda: session_line(1, sess) == "MADO_GLOBALS_SESSION: n=1 boot=0123456789abcdef0123456789abcdef pid=42 first=2026-10-25T12:00:00+00:00 last=2026-10-25T12:00:01+00:00 interfaces=1 adverts=2")
    check(lambda: global_line("a", sess) == "MADO_GLOBAL: name=a ver=5 count=2 class=other")
    sess2 = _Session("-", "7")
    sess2.add_advert(_ADVERT_RE.fullmatch(advert(name="hyprland_focus_grab_manager_v1", ver="1")))
    check(lambda: global_line("hyprland_focus_grab_manager_v1", sess2) == "MADO_GLOBAL: name=hyprland_focus_grab_manager_v1 ver=1 count=1 class=focus-grab")
    check(lambda: classify("zwlr_virtual_pointer_manager_v1") == "input-synthesis")
    check(lambda: classify("wp_security_context_manager_v1") == "sandbox")
    check(lambda: classify("hyprland_input_capture_manager_v1") == "input-capture")
    check(lambda: classify("zwp_keyboard_shortcuts_inhibit_manager_v1") == "input-capture")
    check(lambda: classify("zwlr_output_manager_v1") == "output-control")
    check(lambda: classify("ext_session_lock_manager_v1") == "session-lock")
    check(lambda: classify("no_such_name") == "other")
    check(lambda: csv_or_dash([]) == "-")
    check(lambda: csv_or_dash(["b", "a"]) == "b,a")
    check(lambda: diff_line([sess]) == "MADO_GLOBALS_DIFF: sessions=1 none")
    check(lambda: diff_line([]) == "MADO_GLOBALS_DIFF: sessions=0 none")
    prev_sess = _Session("-", "7")
    prev_sess.add_advert(_ADVERT_RE.fullmatch(advert(name="a", ver="1")))
    prev_sess.add_advert(_ADVERT_RE.fullmatch(advert(name="gone", ver="1")))
    latest_sess = _Session("-", "7")
    latest_sess.add_advert(_ADVERT_RE.fullmatch(advert(name="a", ver="2")))
    latest_sess.add_advert(_ADVERT_RE.fullmatch(advert(name="new", ver="1")))
    check(lambda: diff_line([prev_sess, latest_sess]) == "MADO_GLOBALS_DIFF: from=1 to=2 added=new removed=gone ver_changed=a:1>2")
    check(lambda: diff_line([prev_sess, prev_sess]) == "MADO_GLOBALS_DIFF: from=1 to=2 added=- removed=- ver_changed=-")
    check(lambda: verdict_for(0, 0, []) == ("NO_SESSIONS", 3))
    check(lambda: verdict_for(0, 1, []) == ("UNRECOGNIZED_FORMAT", 4))
    check(lambda: verdict_for(1, 0, []) == ("OK", 0))
    check(lambda: verdict_for(1, 0, ["x"]) == ("MISSING_EXPECTED", 1))
    check(lambda: conclusion_line([], 0, []) == "MADO_GLOBALS: sessions=0 latest_pid=- interfaces=0 classes=- expected_missing=- ignored=0 verdict=NO_SESSIONS")
    check(lambda: conclusion_line([], 2, []) == "MADO_GLOBALS: sessions=0 latest_pid=- interfaces=0 classes=- expected_missing=- ignored=2 verdict=UNRECOGNIZED_FORMAT")
    check(lambda: conclusion_line([latest_sess], 0, ["new"]) == "MADO_GLOBALS: sessions=1 latest_pid=7 interfaces=2 classes=other:2 expected_missing=- ignored=0 verdict=OK")
    check(lambda: conclusion_line([latest_sess], 0, ["new", "missing"]) == "MADO_GLOBALS: sessions=1 latest_pid=7 interfaces=2 classes=other:2 expected_missing=missing ignored=0 verdict=MISSING_EXPECTED")
    check(lambda: conclusion_line([latest_sess], 0, ["new", "new", "MISSING"]) == "MADO_GLOBALS: sessions=1 latest_pid=7 interfaces=2 classes=other:2 expected_missing=MISSING ignored=0 verdict=MISSING_EXPECTED")
    check(lambda: conclusion_line([latest_sess], 0, []) == "MADO_GLOBALS: sessions=1 latest_pid=7 interfaces=2 classes=other:2 expected_missing=- ignored=0 verdict=OK")
    cls_sess = _Session("-", "9")
    cls_sess.add_advert(_ADVERT_RE.fullmatch(advert(name="hyprland_focus_grab_manager_v1", ver="1")))
    cls_sess.add_advert(_ADVERT_RE.fullmatch(advert(name="zwlr_virtual_pointer_manager_v1", ver="2")))
    cls_sess.add_advert(_ADVERT_RE.fullmatch(advert(name="zzz_unknown", ver="1")))
    check(lambda: conclusion_line([cls_sess], 0, []) == "MADO_GLOBALS: sessions=1 latest_pid=9 interfaces=3 classes=focus-grab:1,input-synthesis:1,other:1 expected_missing=- ignored=0 verdict=OK")
    check(lambda: "MADO_GLOBALS: sessions=" in conclusion_line([cls_sess], 0, []))

    # --- file reading ---
    tmp = tempfile.mkdtemp(prefix="mado-selftest-", dir="/tmp")
    try:
        jpath = os.path.join(tmp, "j.txt")
        with open(jpath, "wb") as fh:
            fh.write((advert(name="a") + "\n").encode("ascii"))
        data, err = read_journal_file(jpath)
        check(lambda: err is None and data == (advert(name="a") + "\n").encode("ascii"))

        fifo = os.path.join(tmp, "j.fifo")
        os.mkfifo(fifo)
        data2, err2 = read_journal_file(fifo)
        check(lambda: err2 == "unreadable")

        dpath = os.path.join(tmp, "subdir")
        os.mkdir(dpath)
        data3, err3 = read_journal_file(dpath)
        check(lambda: err3 == "unreadable")

        data4, err4 = read_journal_file(os.path.join(tmp, "missing"))
        check(lambda: err4 == "unreadable")

        big = os.path.join(tmp, "big.txt")
        with open(big, "wb") as fh:
            fh.truncate(MAX_JOURNAL + 1)
        data5, err5 = read_journal_file(big)
        check(lambda: err5 == "too_large")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # --- live helpers ---
    ltmp = tempfile.mkdtemp(prefix="mado-selftest-live-", dir="/tmp")
    try:
        good = os.path.join(ltmp, "prog")
        with open(good, "wb") as fh:
            fh.write(b"#!/bin/sh\n")
        os.chmod(good, 0o755)
        got_good = find_program(good)
        check(lambda: got_good == good)

        writable = os.path.join(ltmp, "wr")
        with open(writable, "wb") as fh:
            fh.write(b"#!/bin/sh\n")
        got_writable = find_program(writable)
        check(lambda: got_writable is None)

        noexec = os.path.join(ltmp, "ne")
        with open(noexec, "wb") as fh:
            fh.write(b"#!/bin/sh\n")
        got_noexec = find_program(noexec)
        check(lambda: got_noexec is None)
        got_absent = find_program(os.path.join(ltmp, "absent"))
        check(lambda: got_absent is None)
        got_bare = find_program("definitely-not-a-real-binary-xyz")
        check(lambda: got_bare is None)
    finally:
        shutil.rmtree(ltmp, ignore_errors=True)

    check(lambda: build_env() == {k: os.environ[k] for k in LIVE_ENV_KEYS if k in os.environ})
    check(lambda: LIVE_ARGV == ["--user", "-u", "xdg-desktop-portal-hyprland", "--no-pager", "-o", "short-iso"])
    check(lambda: _NAME_RE.fullmatch("ok_name_1") is not None)
    check(lambda: _NAME_RE.fullmatch("") is None)
    check(lambda: _NAME_RE.fullmatch("a" * 129) is None)
    check(lambda: _NAME_RE.fullmatch("a" * 128) is not None)
    check(lambda: _NAME_RE.fullmatch("a-b") is None)
    check(lambda: verdict_for(2, 0, []) == ("OK", 0))

    total = len(checks)
    passed = 0
    for fn in checks:
        try:
            if fn():
                passed += 1
        except Exception:
            pass
    sys.stdout.write("MADO_GLOBALS_SELFTEST: %d/%d passed\n" % (passed, total))
    if passed == total and total >= 50:
        return 0
    return 1


def main(argv):
    parser = build_parser()
    try:
        opts = parser.parse_args(argv)
    except SystemExit:
        return setup_out("usage", 2)
    if opts.selftest:
        return run_selftest()
    has_file = opts.journal_file is not None
    if has_file == opts.live:
        return setup_out("usage", 2)
    if opts.journalctl is not None and not opts.live:
        return setup_out("usage", 2)
    for expect in opts.expects:
        if _NAME_RE.fullmatch(expect) is None:
            return setup_out("bad_expect", 2)
    if has_file:
        data, err = read_journal_file(opts.journal_file)
        if err is not None:
            return setup_out(err, 2)
    else:
        prog = find_program(opts.journalctl)
        if prog is None:
            return setup_out("journalctl_unusable", 5)
        data, err = run_live(prog)
        if err is not None:
            return setup_out(err, 5)
    text = data.decode("utf-8", "replace")
    sessions, ignored = parse_journal(text)
    out = []
    for n, sess in enumerate(sessions, 1):
        out.append(session_line(n, sess))
    if sessions:
        latest = sessions[-1]
        for name in sorted(latest.names):
            out.append(global_line(name, latest))
    if opts.diff:
        out.append(diff_line(sessions))
    missing = sorted(set(e for e in opts.expects
                        if not sessions or e not in sessions[-1].names))
    verdict, rc = verdict_for(len(sessions), ignored, missing)
    out.append(conclusion_line(sessions, ignored, opts.expects))
    sys.stdout.write("\n".join(out) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""Differential fuzz v2: the delivered `tools/mado-globals.py` vs the
`PRED-C1-r41-v2` counter's own model (`model_out`) on hostile inputs.

The counter is imported with importlib (main() is never called). The tool
under test is `tools/mado-globals.py` at the DATA commit 07f2641..., copied
byte-identically into this seat dir. Every mutant journal is run through both
sides: `model_out(raw.decode("utf-8","replace"), expects, diff)` vs
`python3 -I tool --journal-file <mutant> [--expect ...] [--diff]`, compared on
rc + stdout bytes, with stderr required empty on rc 0/1/3/4 — exactly the
counter's `judge`.

v2 classes added over the w1 harness: `Got interface: ` lines in other shapes
(ignored count), FIFO / directory / symlink-to-FIFO paths, a file that grows,
`-o short` captures, 128/129-char names, version 999999/1000000, invalid UTF-8
in host/pid positions, and the 8 MiB boundary (all in `structural_probes` and
the systematic sweeps).
"""
import argparse
import hashlib
import importlib.util
import json
import os
import random
import re
import subprocess
import sys
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor

SEAT = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
DATA = "07f2641696b5ac73de1404ea737a9f27e9819aa1"
NONCE = "difffuzzr41w2"
PY = sys.executable
ENV = {"PATH": "/usr/bin", "XDG_RUNTIME_DIR": "/run/user/1000"}

# ------------------------------------------------------------ frozen inputs
def git_show(path):
    p = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (DATA, path)],
                       capture_output=True)
    if p.returncode != 0:
        raise SystemExit("git show failed: %s" % p.stderr.decode())
    return p.stdout

COUNTER_SRC = git_show("quality/counters/c1-r41-globals-v2.py")
TOOL_SRC = git_show("tools/mado-globals.py")

COUNTER = os.path.join(SEAT, "counter-v2.py")
TOOL = os.path.join(SEAT, "tool-under-test.py")
with open(COUNTER, "wb") as fh:
    fh.write(COUNTER_SRC)
with open(TOOL, "wb") as fh:
    fh.write(TOOL_SRC)

spec = importlib.util.spec_from_file_location("c1r41v2", COUNTER)
C1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C1)
MAX_BYTES = C1.MAX_BYTES


def expected(raw, expects, diff):
    """(want_bytes, want_rc) exactly as the judge's model_out."""
    text = raw.decode("utf-8", "replace")
    out, code = C1.model_out(text, expects, diff)
    return out.encode(), code


def run_tool(argv, cwd, timeout=60, env=None):
    p = subprocess.run([PY, "-I", TOOL] + argv, capture_output=True, cwd=cwd,
                       env=env or ENV, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


# ------------------------------------------------------------------ seeds
def seed_committed():
    with open(os.path.join(LANE, ".ufo/waves/round-41/fetch/xdph-journal.txt"),
              "rb") as fh:
        return fh.read()


def seed_gen(i):
    text, _e, _d = C1.gen_fixture(DATA, NONCE, i)
    return text.encode("utf-8", "surrogateescape") if "\xe9" not in text \
        else text.encode("latin-1", "replace")


def seed_sample(tag, n):
    return C1.sample_journal(DATA, NONCE, tag, n)


def seed_v2mix():
    rng = C1.rng_for(DATA, NONCE, "v2mix", 0)
    pid = str(rng.randrange(100, 900))
    ls = [C1.line(C1.T1, pid, "wl_seat", 9),
          C1.line(C1.T1, pid, "wl_shm", 1),
          C1.line(C1.T2, pid, "wl_seat", 10),
          C1.line(C1.T2, pid, "zz_big", 123456),
          C1.line(C1.T2, pid, "zz_toobig", 1234567),
          C1.line(C1.T1, pid, "wl_output", 2).replace("[LOG]", "[log]"),
          C1.line(C1.T1, pid, "wl_compositor", 1, host="x\x01").replace(
              "x\x01", "x\xa0y"),
          C1.line(C1.T1, pid, "HYPRLAND_FOCUS_GRAB_MANAGER_V1", 1),
          C1.line(C1.T1, pid, "hyprland_focus_grab_manager_v1", 1),
          C1.line(C1.T1, "011", "wl_seat", 1),
          C1.line(C1.T1, "11", "wl_shm", 1),
          "-- Boot %032x --" % rng.getrandbits(128),
          C1.line(C1.T2, "301", "wl_output", 1),
          C1.line(C1.T1, "9", "wl_\u00e9", 1),
          C1.line(C1.T1, "9", "\u0432\u043b_x", 1),
          C1.line(C1.T1, "5", "wl_shm", 1).replace("(ver 1)",
                                                   "(ver \u0661\u0662)"),
          C1.line(C1.T1, "5", "wl_output", 1).replace("[5]", "[\u0661\u0662]"),
          C1.SHORT % ("wl_seat", 9), C1.SHORT % ("wl_shm", 2)]
    return ("\n".join(ls) + "\n").encode("utf-8", "replace")


SEEDS = [("committed", seed_committed()), ("v2mix", seed_v2mix()),
         ("sample1", seed_sample("fz1", 1)), ("sample2", seed_sample("fz2", 2)),
         ("sample3", seed_sample("fz3", 3))]
for _i in range(8):
    SEEDS.append(("gen%d" % _i, seed_gen(_i)))

# -------------------------------------------------------------- mutators
def _lines(raw):
    return raw.split(b"\n")


def _rng(tag):
    return random.Random(int(hashlib.sha256(tag.encode()).hexdigest(), 16))


def op_byte_flip(rng, raw):
    if not raw:
        return None
    i = rng.randrange(len(raw))
    return raw[:i] + bytes([rng.randrange(256)]) + raw[i + 1:]


def op_byte_insert(rng, raw):
    i = rng.randrange(len(raw) + 1)
    return raw[:i] + bytes([rng.choice([0x00, 0xff, 0xc3, 0xed, 0x80,
                                        0x20, 0x0d, 0x0a, 0x09, 0x7c])]) \
        + raw[i:]


def op_byte_delete(rng, raw):
    if not raw:
        return None
    i = rng.randrange(len(raw))
    return raw[:i] + raw[i + 1:]


def op_line_delete(rng, raw):
    ls = _lines(raw)
    if len(ls) < 2:
        return None
    i = rng.randrange(len(ls))
    return b"\n".join(ls[:i] + ls[i + 1:])


def op_line_dup(rng, raw):
    ls = _lines(raw)
    i = rng.randrange(len(ls))
    return b"\n".join(ls[:i] + [ls[i], ls[i]] + ls[i + 1:])


def op_line_swap(rng, raw):
    ls = _lines(raw)
    if len(ls) < 2:
        return None
    i, j = rng.sample(range(len(ls)), 2)
    ls[i], ls[j] = ls[j], ls[i]
    return b"\n".join(ls)


def op_cr_one(rng, raw):
    ls = _lines(raw)
    if not ls:
        return None
    i = rng.randrange(len(ls))
    return b"\n".join(ls[:i] + [ls[i] + b"\r"] + ls[i + 1:])


def op_crlf_all(rng, raw):
    return raw.replace(b"\n", b"\r\n")


def op_boot_insert(rng, raw):
    ls = _lines(raw)
    i = rng.randrange(len(ls) + 1)
    return b"\n".join(ls[:i] + [b"-- Boot %032x --" % rng.getrandbits(128)]
                      + ls[i:])


def op_boot_insert_dup(rng, raw):
    ls = _lines(raw)
    i = rng.randrange(len(ls) + 1)
    bid = b"-- Boot %032x --" % rng.getrandbits(128)
    return b"\n".join(ls[:i] + [bid, bid] + ls[i:])


def op_pid_flip(rng, raw):
    m = re.search(rb"\[([0-9]+)\]: \[LOG\]", raw)
    if not m:
        return None
    old = m.group(1)
    mode = rng.randrange(4)
    if mode == 0:
        new = b"0" + old
    elif mode == 1:
        new = old.lstrip(b"0") or b"0"
    elif mode == 2:
        new = old[:-1] + bytes([0x30 + rng.randrange(10)])
    else:
        new = old + b"0"
    return raw[:m.start(1)] + new + raw[m.end(1):]


def op_ver_digits(rng, raw):
    m = re.search(rb"\(ver ([0-9]+)\)", raw)
    if not m:
        return None
    mode = rng.randrange(5)
    if mode == 0:
        new = b"0" + m.group(1)
    elif mode == 1:
        new = m.group(1).lstrip(b"0") or b"0"
    elif mode == 2:
        new = b"999999"
    elif mode == 3:
        new = b"1000000"
    else:
        new = b"1234567"
    return raw[:m.start(1)] + new + raw[m.end(1):]


def op_name_len(rng, raw):
    m = re.search(rb"Got interface: ([A-Za-z0-9_]+)", raw)
    if not m:
        return None
    n = rng.choice([0, 1, 127, 128, 129, 130])
    return raw[:m.start(1)] + b"a" * n + raw[m.end(1):]


def op_invalid_utf8(rng, raw):
    i = rng.randrange(len(raw) + 1)
    bad = rng.choice([b"\xff", b"\xfe", b"\xc3", b"\xed\xa0\x80",
                      b"\xf0\x9f", b"\x80\x80"])
    return raw[:i] + bad + raw[i:]


def op_no_trailing_nl(rng, raw):
    if raw.endswith(b"\n"):
        return raw[:-1]
    return raw + b"\n"


def op_boot_only(rng, raw):
    n = rng.randrange(0, 5)
    return b"".join(b"-- Boot %032x --\n" % rng.getrandbits(128)
                    for _ in range(n))


def op_nul(rng, raw):
    i = rng.randrange(len(raw) + 1)
    n = rng.randrange(1, 4)
    return raw[:i] + b"\x00" * n + raw[i:]


def op_nul_all(rng, raw):
    return raw.replace(b" ", b"\x00", rng.randrange(1, 4))


def op_spacing(rng, raw):
    choices = [(b"[LOG]  |", b"[LOG] |"), (b"[LOG]  |", b"[LOG]   |"),
               (b"[LOG]  |", b"[LOG]\t|"), (b"Got interface: ", b"got interface: "),
               (b"xdg-desktop-portal-hyprland", b"xdg-desktop-portal-gnome")]
    a, b = rng.choice(choices)
    return raw.replace(a, b, 1)


def op_trailing_text(rng, raw):
    ls = _lines(raw)
    i = rng.randrange(len(ls))
    return b"\n".join(ls[:i + 1]) + b" extra" + b"\n" + b"\n".join(ls[i + 1:])


def op_leading_text(rng, raw):
    ls = _lines(raw)
    i = rng.randrange(len(ls))
    return b"\n".join(ls[:i] + [b"x " + ls[i]] + ls[i + 1:])


def op_ts(rng, raw):
    m = re.search(rb"([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}[+-][0-9]{2}:[0-9]{2})", raw)
    if not m:
        return None
    new = rng.choice([b"2026-02-30T13:36:24-03:00", b"2026-10-25T24:36:24-03:00",
                      b"2026-10-25T13:36:24+30:00", b"2026-10-25T13:36:24Z",
                      b"26-10-25T13:36:24-03:00",
                      b"2026-10-25T13:36:24-03:00x",
                      b"2026-10-25T13:36:24-0300"])
    return raw[:m.start()] + new + raw[m.end():]


def op_host(rng, raw):
    m = re.search(rb"T[0-9]{2}:[0-9]{2}:[0-9]{2}[+-][0-9]{2}:[0-9]{2} (\S+) ", raw)
    if not m:
        return None
    new = rng.choice([b"\xff", b"h\xc3", b"\xa0", b"\t", b"h" * 200])
    return raw[:m.start(1)] + new + raw[m.end(1):]


def op_reverse(rng, raw):
    return b"\n".join(reversed(_lines(raw)))


def op_double(rng, raw):
    return raw + raw


def op_append_boot(rng, raw):
    return raw + b"-- Boot %032x --\n" % rng.getrandbits(128)


def op_truncate(rng, raw):
    if len(raw) < 4:
        return None
    return raw[:rng.randrange(1, len(raw))]


def op_ignore_shape(rng, raw):
    """An advert-like line in an alien `-o` shape (keeps the mark)."""
    ls = _lines(raw)
    cand = [i for i, l in enumerate(ls) if b"Got interface: " in l]
    if not cand:
        return None
    i = rng.choice(cand)
    shapes = [
        b"Oct 25 13:16:45 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  | Got interface: wl_seat (ver 1)",
        b"Got interface: wl_seat (ver 1)",
        b'{"__REALTIME_TIMESTAMP":"1790313405000000","MESSAGE":"Got interface: wl_seat (ver 1)"}',
        b"Oct 25 13:16:45 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG] got interface: wl_seat (ver 1)",
        b"2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG] | Got interface: wl_seat (ver 1)",
        b"2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]   | Got interface: wl_seat (ver 1)",
        b"2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [INFO]  | Got interface: wl_seat (ver 1)",
        b"2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-gnome[1918]: [LOG]  | Got interface: wl_seat (ver 1)",
        b"2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  | Got interface: wl_seat (ver 1) x",
        b"2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  | Got interface: wl_seat (ver 1",
        b"2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  | Got interface: wl_seat(ver 1)",
        b"2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  | Got interface: wl_seat (ver 01)",
        b"2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  | Got interface: wl_seat (ver 1)\r",
        b"2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  | Got interface: wl_seat (ver 1000000)",
        b"2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  | Got interface: " + b"a" * 129 + b" (ver 1)",
        b"2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[abc]: [LOG]  | Got interface: wl_seat (ver 1)",
        b"2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  | Got interface: wl_seat (ver 1)  \n extra",
    ]
    return b"\n".join(ls[:i] + [rng.choice(shapes)] + ls[i + 1:])


def op_ssh_invalid(rng, raw):
    m = re.search(rb"(\S+) xdg-desktop-portal-hyprland\[([0-9]+)\]", raw)
    if not m:
        return None
    if rng.random() < 0.5:
        return raw[:m.start(1)] + b"\xff" + raw[m.end(1):]
    return raw[:m.start(2)] + b"\xff" + raw[m.end(2):]


def op_ver_pair(rng, raw):
    m = re.search(rb"\(ver [0-9]+\)\n", raw)
    if not m:
        return None
    tail = raw[m.end():]
    nl = tail.find(b"\n")
    seg = tail[:nl] if nl >= 0 else tail
    new = re.sub(rb"\(ver [0-9]+\)",
                 rng.choice([b"(ver 999999)", b"(ver 1000000)",
                             b"(ver 000000)", b"(ver 0)"]),
                 seg, count=1)
    out = raw[:m.end()] + new
    return out + tail[nl:] if nl >= 0 else out


def op_boot_mangle(rng, raw):
    m = re.search(rb"-- Boot ([0-9a-f]{32}) --", raw)
    if not m:
        return None
    old = m.group(1)
    new = rng.choice([old.upper(), old[:31], old + b"0", b"", b"g" * 32,
                      old + b" "])
    return raw[:m.start(1)] + new + raw[m.end(1):]


OPS = [op_byte_flip, op_byte_insert, op_byte_delete, op_line_delete,
       op_line_dup, op_line_swap, op_cr_one, op_crlf_all, op_boot_insert,
       op_boot_insert_dup, op_pid_flip, op_ver_digits, op_name_len,
       op_invalid_utf8, op_no_trailing_nl, op_boot_only, op_nul, op_nul_all,
       op_spacing, op_trailing_text, op_leading_text, op_ts, op_host,
       op_reverse, op_double, op_append_boot, op_truncate, op_ignore_shape,
       op_ssh_invalid, op_ver_pair, op_boot_mangle]

# ------------------------------------------------------------ systematic
def systematic():
    out = []
    ts = b"2026-10-25T13:36:24-03:00"
    for n in (0, 1, 127, 128, 129, 130):
        line = (ts + b" h xdg-desktop-portal-hyprland[1952]: [LOG]  | "
                b"Got interface: " + b"a" * n + b" (ver 1)\n")
        out.append(("name-len-%d" % n, line))
        out.append(("name-len-%d-diff" % n, line * 2))
    for v in (b"0", b"00", b"1", b"9", b"10", b"000001", b"999999",
              b"1000000", b"1234567", "١".encode(), "١٢٣٤٥٦".encode(),
              "١٢٣٤٥٦٧".encode()):
        out.append(("ver-%s" % v.decode("utf-8", "replace"),
                    ts + b" h xdg-desktop-portal-hyprland[1952]: [LOG]  | "
                    b"Got interface: wl_seat (ver " + v + b")\n"))
    for a, b in ((b"9", b"10"), (b"999999", b"1000000"), (b"000001", b"1"),
                 (b"1", b"01"), (b"9", b"10"), (b"123456", b"123457")):
        out.append(("ver-%s-then-%s" % (a.decode(), b.decode()),
                    ts + b" h xdg-desktop-portal-hyprland[1]: [LOG]  | "
                    b"Got interface: wl_seat (ver " + a + b")\n" + ts +
                    b" h xdg-desktop-portal-hyprland[1]: [LOG]  | "
                    b"Got interface: wl_seat (ver " + b + b")\n"))
    for a, b in ((b"1952", b"01952"), (b"0", b"00"), (b"1952", b"1952"),
                 (b"1", b"01"), (b"007", b"7"), (b"011", b"11")):
        out.append(("pid-%s-%s" % (a.decode(), b.decode()),
                    ts + b" h xdg-desktop-portal-hyprland[" + a + b"]: [LOG]  | "
                    b"Got interface: wl_seat (ver 1)\n" + ts +
                    b" h xdg-desktop-portal-hyprland[" + b + b"]: [LOG]  | "
                    b"Got interface: wl_shm (ver 1)\n"))
    # invalid UTF-8 in host / pid / ts positions
    for tag, (host, pid) in ((b"h\xff", (b"h\xff", b"1952")),
                             (b"h\xc3", (b"h\xc3", b"1952")),
                             (b"\xa0", (b"\xa0", b"1952")),
                             (b"h\xed\xa0\x80", (b"h\xed\xa0\x80", b"1952")),
                             (b"pid-ff", (b"h", b"195\xff")),
                             (b"pid-80", (b"h", b"19\x802")),
                             (b"pid-only-ff", (b"h", b"\xff"))):
        line = (ts + b" " + host + b" xdg-desktop-portal-hyprland[" + pid +
                b"]: [LOG]  | Got interface: wl_seat (ver 1)\n")
        out.append(("utf8-hostpid-%s" % tag.decode("latin-1"), line))
    # `-o short` and other shapes, alone and mixed with a valid session
    shapes = [
        b"Oct 25 13:16:45 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  | Got interface: wl_seat (ver 1)",
        b"Got interface: wl_seat (ver 1)",
        b'{"__REALTIME_TIMESTAMP":"1790313405000000","MESSAGE":"Got interface: wl_seat (ver 1)"}',
        b"Oct 25 13:16:45 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG] got interface: wl_seat (ver 1)",
        b"2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG] | Got interface: wl_seat (ver 1)",
        b"2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]   | Got interface: wl_seat (ver 1)",
        b"2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [INFO]  | Got interface: wl_seat (ver 1)",
        b"2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-gnome[1918]: [LOG]  | Got interface: wl_seat (ver 1)",
        b"2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  | Got interface: wl_seat (ver 1) x",
        b"2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  | Got interface: wl_seat(ver 1)",
        b"2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  | Got interface: wl_seat (ver 1)\r",
        b"2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  | Got interface: " + b"a" * 129 + b" (ver 1)",
        b"2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[abc]: [LOG]  | Got interface: wl_seat (ver 1)",
    ]
    for k, s in enumerate(shapes):
        out.append(("shape-blob-%d" % k, s + b"\n"))
        out.append(("shape-mixed-%d" % k,
                    s + b"\n" + ts +
                    b" h xdg-desktop-portal-hyprland[55]: [LOG]  | "
                    b"Got interface: wl_output (ver 2)\n"))
    for label, body in (("empty", b""), ("nl", b"\n"), ("nlnl", b"\n\n"),
                        ("nul", b"\x00"), ("crlf-only", b"\r\n"),
                        ("no-nl-advert", ts + b" h xdg-desktop-portal-hyprland"
                         b"[1]: [LOG]  | Got interface: wl_seat (ver 1)"),
                        ("boot-only", b"-- Boot " + b"a" * 32 + b" --\n"),
                        ("boot-boot", (b"-- Boot " + b"a" * 32 + b" --\n") * 2),
                        ("boot-upper", b"-- Boot " + b"A" * 32 + b" --\n"),
                        ("boot-short", b"-- Boot " + b"a" * 31 + b" --\n"),
                        ("boot-long", b"-- Boot " + b"a" * 33 + b" --\n"),
                        ("boot-trail", b"-- Boot " + b"a" * 32 + b" ---\n")):
        out.append(("shape-%s" % label, body))
    return out


# ------------------------------------------------------------ execution
EXPECT_MODES = 6


def expect_mode(rng, raw):
    text = raw.decode("utf-8", "replace")
    ss = C1.model_sessions(text)[0]
    names = sorted(ss[-1]["names"]) if ss else []
    mode = rng.randrange(EXPECT_MODES)
    extra, expects = [], []
    if rng.random() < 0.5:
        extra.append("--diff")
    if mode == 1 and names:
        expects = [names[rng.randrange(len(names))]]
    elif mode == 2 and names:
        expects = [names[rng.randrange(len(names))], "zz_absent_v2"]
    elif mode == 3:
        expects = ["zz_absent_a", "zz_absent_b", "zz_absent_a"]
    elif mode == 4 and names:
        n = names[rng.randrange(len(names))]
        expects = [n, n, "zz_absent_c", "zz_absent_c"]
    elif mode == 5:
        expects = ["a" * 128]
    for e in expects:
        extra += ["--expect", e]
    return extra, expects, "--diff" in extra


def compare(raw, extra, expects, diff, scratch, name):
    want_out, want_rc = expected(raw, expects, diff)
    path = os.path.join(scratch, name)
    with open(path, "wb") as fh:
        fh.write(raw)
    rc, out, err = run_tool(["--journal-file", path] + extra, scratch)
    ok = rc == want_rc and out == want_out
    if ok and want_rc in (0, 1, 3, 4) and err:
        ok = False
    return ok, (want_rc, want_out, rc, out, err)


def class_key(want_rc, got_rc, want_out, got_out, err):
    if want_rc != got_rc:
        return "rc:%s->%s" % (want_rc, got_rc)
    if want_out != got_out:
        a = want_out.splitlines()
        b = got_out.splitlines()
        for k in range(max(len(a), len(b))):
            x = a[k] if k < len(a) else None
            y = b[k] if k < len(b) else None
            if x != y:
                return "stdout-line:%s|%s" % (x[:40], (y or "")[:40])
        return "extra-line"
    return "stderr"


def minimise(raw, extra, expects, diff, scratch):
    """Greedy line-deletion then per-line trimming; disagreement must persist."""
    runs = [0]

    def bad(cand):
        runs[0] += 1
        ok, _ = compare(cand, extra, expects, diff, scratch, "_min.txt")
        return not ok

    lines = raw.split(b"\n")
    changed = True
    while changed and runs[0] < 900:
        changed = False
        i = 0
        while i < len(lines) and runs[0] < 900:
            cand = b"\n".join(lines[:i] + lines[i + 1:])
            if bad(cand):
                lines = lines[:i] + lines[i + 1:]
                changed = True
            else:
                i += 1
    for idx in range(len(lines)):
        for side in ("suffix", "prefix"):
            n = len(lines[idx])
            while n > 0 and runs[0] < 1200:
                cand_line = lines[idx][:n] if side == "suffix" else lines[idx][-n:]
                cand = b"\n".join(lines[:idx] + [cand_line] + lines[idx + 1:])
                if bad(cand):
                    lines[idx] = cand_line
                    break
                n //= 2
    return b"\n".join(lines), runs[0]


# ------------------------------------------------------ structural probes
def structural_probes(scratch, rec):
    okj = os.path.join(scratch, "s-ok.txt")
    with open(okj, "wb") as fh:
        fh.write(b"2026-10-25T13:36:24-03:00 h "
                 b"xdg-desktop-portal-hyprland[1]: [LOG]  | "
                 b"Got interface: wl_seat (ver 1)\n")
    fifo = os.path.join(scratch, "s-fifo")
    os.mkfifo(fifo)
    sym_fifo = os.path.join(scratch, "s-sym-fifo")
    os.symlink(fifo, sym_fifo)
    d = os.path.join(scratch, "s-dir")
    os.makedirs(d, exist_ok=True)
    sym_dir = os.path.join(scratch, "s-sym-dir")
    os.symlink(d, sym_dir)
    sym_ok = os.path.join(scratch, "s-sym-ok")
    os.symlink(okj, sym_ok)
    dangling = os.path.join(scratch, "s-dangling")
    os.symlink(os.path.join(scratch, "absent-target"), dangling)
    empty = os.path.join(scratch, "s-empty")
    open(empty, "wb").close()
    expected_cases = [
        ("fifo", fifo, "MADO_GLOBALS: SETUP unreadable\n", 2),
        ("symlink-to-fifo", sym_fifo, "MADO_GLOBALS: SETUP unreadable\n", 2),
        ("directory", d, "MADO_GLOBALS: SETUP unreadable\n", 2),
        ("symlink-to-dir", sym_dir, "MADO_GLOBALS: SETUP unreadable\n", 2),
        ("symlink-to-file", sym_ok, None, 0),
        ("dangling-symlink", dangling, "MADO_GLOBALS: SETUP unreadable\n", 2),
        ("missing", os.path.join(scratch, "absent"), "MADO_GLOBALS: SETUP unreadable\n", 2),
        ("empty-file", empty, None, 3),
    ]
    for label, path, want_out, want_rc in expected_cases:
        try:
            rc, out, err = run_tool(["--journal-file", path], scratch)
        except subprocess.TimeoutExpired:
            rec.append("structural %s TIMEOUT" % label)
            continue
        ok = rc == want_rc and (want_out is None or out == want_out.encode())
        rec.append("structural %s %s want_rc=%s rc=%s want=%r got=%r" % (
            label, "ok" if ok else "MISMATCH", want_rc, rc,
            want_out or "", out.decode("utf-8", "replace")[:120]))
    # size boundary on a real journal
    for label, n in (("exact-max-with-nl", MAX_BYTES), ("over-by-1", MAX_BYTES + 1)):
        jp = os.path.join(scratch, "s-size")
        with open(jp, "wb") as fh:
            fh.write(b"x" * (n - 1) + b"\n")
        rc, out, err = run_tool(["--journal-file", jp], scratch)
        want_rc = 2 if n > MAX_BYTES else 3
        ok = rc == want_rc
        rec.append("structural size-%s %s want_rc=%s rc=%s got=%r" % (
            label, "ok" if ok else "MISMATCH", want_rc, rc,
            out.decode()[:120]))
    # growing file: writer appends past the 8 MiB cap while the tool reads
    jp = os.path.join(scratch, "s-grow")
    stop = threading.Event()
    def writer():
        with open(jp, "ab") as fh:
            while not stop.is_set():
                fh.write(b"x" * 65536)
                fh.flush()
    with open(jp, "wb") as fh:
        fh.write(b"x" * (1 << 20))
    t = threading.Thread(target=writer, daemon=True)
    t.start()
    try:
        rc, out, err = run_tool(["--journal-file", jp], scratch, timeout=30)
        ok = rc == 2 and out.startswith(b"MADO_GLOBALS: SETUP too_large")
        rec.append("structural growing-file-over-cap %s want_rc=2 rc=%s got=%r" % (
            "ok" if ok else "MISMATCH", rc, out.decode()[:120]))
    except subprocess.TimeoutExpired:
        rec.append("structural growing-file-over-cap TIMEOUT")
    finally:
        stop.set()
        t.join(timeout=5)
    # stalling file: writer holds the fd open and stops writing -> a read
    # past the buffered bytes must not hang the tool (deadline probe)
    jp2 = os.path.join(scratch, "s-stall")
    fh2 = open(jp2, "wb")
    fh2.write(b"x" * (512 * 1024))
    fh2.flush()
    try:
        rc, out, err = run_tool(["--journal-file", jp2], scratch, timeout=12)
        rec.append("structural stalling-file returned rc=%s got=%r" % (
            rc, out.decode()[:120]))
    except subprocess.TimeoutExpired:
        rec.append("structural stalling-file HANG")
    finally:
        fh2.close()
    # file mode must not spawn anything: journalctl stub earlier on PATH
    bindir = os.path.join(scratch, "s-bin")
    os.makedirs(bindir, exist_ok=True)
    spawn_marker = os.path.join(scratch, "spawned")
    stub = os.path.join(bindir, "journalctl")
    with open(stub, "w") as fh:
        fh.write("#!/bin/sh\ntouch %s\nexit 1\n" % spawn_marker)
    os.chmod(stub, 0o755)
    if os.path.exists(spawn_marker):
        os.unlink(spawn_marker)
    env = dict(ENV, PATH=bindir + ":/usr/bin")
    rc, out, err = run_tool(["--journal-file", okj], scratch, env=env)
    spawned = os.path.exists(spawn_marker)
    rec.append("structural file-mode-no-spawn %s rc=%s spawned=%s" % (
        "ok" if (rc == 0 and not spawned) else "MISMATCH", rc, spawned))


# -------------------------------------------------------------- CLI cases
def cli_cases(scratch, rec):
    okj = os.path.join(scratch, "c-ok.txt")
    with open(okj, "wb") as fh:
        fh.write(b"2026-10-25T13:36:24-03:00 h "
                 b"xdg-desktop-portal-hyprland[1]: [LOG]  | "
                 b"Got interface: wl_seat (ver 1)\n")
    want128, rc128 = expected(open(okj, "rb").read(), ["a" * 128], False)
    cases = [
        ("both flags", ["--journal-file", okj, "--live"], "usage", 2),
        ("neither flag", [], "usage", 2),
        ("journalctl without live", ["--journal-file", okj, "--journalctl", "x"],
         "usage", 2),
        ("abbrev flag", ["--journal-fil", okj], "usage", 2),
        ("unknown flag", ["--journal-file", okj, "--frobnicate"], "usage", 2),
        ("expect space", ["--journal-file", okj, "--expect=a b"],
         "bad_expect", 2),
        ("expect empty", ["--journal-file", okj, "--expect="], "bad_expect", 2),
        ("expect 129", ["--journal-file", okj, "--expect=" + "a" * 129],
         "bad_expect", 2),
        ("expect non-ascii", ["--journal-file", okj, "--expect=\u00e9"],
         "bad_expect", 2),
        ("expect dash", ["--journal-file", okj, "--expect=-x"],
         "bad_expect", 2),
        ("diff with value", ["--journal-file", okj, "--diff=1"], "usage", 2),
        ("expect 128 ok", ["--journal-file", okj, "--expect=" + "a" * 128],
         want128, rc128),
    ]
    for label, argv, want_out, want_rc in cases:
        try:
            rc, out, err = run_tool(argv, scratch)
        except subprocess.TimeoutExpired:
            rec.append("cli %s TIMEOUT" % label)
            continue
        if isinstance(want_out, str):
            want = (want_out if want_out.startswith("MADO_GLOBALS")
                    else "MADO_GLOBALS: SETUP %s\n" % want_out).encode()
        elif isinstance(want_out, bytes):
            want = want_out
        else:
            want = None
        ok = rc == want_rc and (want is None or out == want)
        rec.append("cli %s %s want_rc=%s rc=%s want=%r got=%r" % (
            label, "ok" if ok else "MISMATCH", want_rc, rc,
            want or "", out.decode("utf-8", "replace")[:120]))


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--tool", default=None)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--variants", action="store_true",
                    help="run the four known-wrong variant tools (harness teeth)")
    args = ap.parse_args()

    global TOOL
    if args.tool:
        TOOL = os.path.abspath(args.tool)

    receipt = os.path.join(SEAT, "fuzz-receipt%s.txt" % (
        "-" + os.path.basename(args.tool) if args.tool else ""))
    summary_path = os.path.join(SEAT, "fuzz-summary%s.json" % (
        "-" + os.path.basename(args.tool) if args.tool else ""))
    rec_lines = []
    rec_lines.append("fuzz v2: tool=%s nonce=%s data=%s" % (TOOL, NONCE, DATA))

    scratch = os.path.join(SEAT, "scratch")
    import shutil
    shutil.rmtree(scratch, ignore_errors=True)
    os.makedirs(scratch, exist_ok=True)

    # systematic set always runs
    sys_cases = systematic()
    tasks = []
    for tag, raw in sys_cases:
        if len(raw) > MAX_BYTES:
            continue
        rng = _rng(NONCE + ":sys:" + tag)
        extra, expects, diff = expect_mode(rng, raw)
        tasks.append((tag, raw, extra, expects, diff))

    mutants = 0
    NVAR = 12
    if not args.quick:
        for si, (stag, seed) in enumerate(SEEDS):
            for oi, op in enumerate(OPS):
                for v in range(NVAR):
                    tag = "%s/%s/%d" % (stag, op.__name__, v)
                    rng = _rng(NONCE + ":" + tag)
                    raw = op(rng, seed)
                    if raw is None:
                        continue
                    if len(raw) > MAX_BYTES:
                        continue
                    extra, expects, diff = expect_mode(rng, raw)
                    tasks.append((tag, raw, extra, expects, diff))

    lock = threading.Lock()
    disagreements = []

    def work(task):
        tag, raw, extra, expects, diff = task
        try:
            ok, rec1 = compare(raw, extra, expects, diff, scratch,
                               "m-%s.bin" % uuid.uuid4().hex[:8])
        except subprocess.TimeoutExpired:
            with lock:
                disagreements.append((tag, raw, ("TIMEOUT", "", "", "", "", "")))
            return tag
        if not ok:
            with lock:
                disagreements.append((tag, raw, rec1))
        return tag

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        done = list(pool.map(work, tasks))
    mutants = len(tasks)
    rec_lines.append("fuzz: mutants=%d disagreements=%d" % (mutants, len(disagreements)))

    classes = {}
    for tag, raw, rec1 in disagreements:
        want_rc, want_out, rc, out, err = rec1
        k = class_key(want_rc, rc, want_out, out, err)
        classes[k] = classes.get(k, 0) + 1
    rec_lines.append("fuzz: classes=%s" % json.dumps(classes, sort_keys=True))

    # minimise each disagreement
    minis = []
    for tag, raw, rec1 in disagreements[:8]:
        extra, expects, diff = expect_mode(_rng(NONCE + ":mini:" + tag), raw)
        try:
            mraw, runs = minimise(raw, extra, expects, diff, scratch)
            want_out, want_rc = expected(mraw, expects, diff)
            rc, out, err = run_tool(["--journal-file",
                                     os.path.join(scratch, "_min.txt")] + extra,
                                    scratch)
            minis.append({"tag": tag, "runs": runs,
                          "want_rc": want_rc, "rc": rc,
                          "want_head": want_out[:120].decode("utf-8", "replace"),
                          "got_head": out[:120].decode("utf-8", "replace"),
                          "stderr": err[:80].decode("utf-8", "replace"),
                          "minimised": mraw.decode("utf-8", "replace")})
        except Exception as exc:  # noqa
            minis.append({"tag": tag, "minimise_error": str(exc)})
    rec_lines.append("fuzz: minimised=%d" % len(minis))

    # structural + CLI probes
    structural_probes(scratch, rec_lines)
    cli_cases(scratch, rec_lines)

    with open(receipt, "w") as fh:
        fh.write("\n".join(rec_lines) + "\n")
    summary = {"mutants": mutants, "disagreements": len(disagreements),
               "classes": classes, "minimised": minis}
    with open(summary_path, "w") as fh:
        json.dump(summary, fh, indent=1)
    print("fuzz: mutants=%d disagreements=%d" % (mutants, len(disagreements)))
    for t, raw, r in disagreements[:5]:
        print("  DISAGREE", t, r[0], r[3], r[1][:80])
    return 0


if __name__ == "__main__":
    sys.exit(main())

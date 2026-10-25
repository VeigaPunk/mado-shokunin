#!/usr/bin/env python3
"""Differential fuzz: the C1 reference tool against the counter's own model.

Loads quality/counters/c1-r41-globals.py with importlib (exec_module only; main()
is __main__-guarded and is never called), seeds journals from the committed fetch
receipt plus the counter's own gen_fixture/sample_journal generators, mutates them
(byte flips, line delete/dup/swap, CR/LF, boot-line insertion at every position,
pid flips, 1/6/7-digit versions, 127/128/129-char names, invalid UTF-8, no
trailing newline, boot-only files, NUL bytes, oversized files), runs the reference
tool under `python3 -I` and compares rc + stdout byte-exactly with model_out.

Usage: python3 -I fuzz.py [--quick] [--jobs N]
Writes fuzz-receipt.txt and fuzz-summary.json next to itself.
"""
import hashlib
import importlib.util
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

SEAT = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(LANE, "quality/counters/c1-r41-globals.py")
REF = os.path.join(SEAT, "ref-tool.py")
JOURNAL = os.path.join(LANE, ".ufo/waves/round-41/fetch/xdph-journal.txt")
REV = "60c3914154333180450d5da27ba222d5763cc56a"   # round-41 freeze commit
NONCE = "diff-fuzz-r41-w1"
RECEIPT = os.path.join(SEAT, "fuzz-receipt.txt")
SUMMARY = os.path.join(SEAT, "fuzz-summary.json")
PY = sys.executable
ENV = {"PATH": "/usr/bin", "XDG_RUNTIME_DIR": "/run/user/1000"}

# ---------------------------------------------------------------- counter
spec = importlib.util.spec_from_file_location("c1r41", COUNTER)
C1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C1)          # main() is guarded; nothing runs
MAX_BYTES = C1.MAX_BYTES


def expected(raw, expects, diff):
    """The judge's expectation for a journal file, exactly as score_file_case
    / score_gen compute it (too_large is the one non-model setup class)."""
    if len(raw) > MAX_BYTES:
        return "MADO_GLOBALS: SETUP too_large\n", 2
    return C1.model_out(raw.decode("utf-8", "replace"), expects, diff)


def run_tool(argv, cwd, timeout=60, env=None):
    p = subprocess.run([PY, "-I", REF] + argv, capture_output=True, cwd=cwd,
                       env=env or ENV, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


# ---------------------------------------------------------------- seeds
def seed_committed():
    with open(JOURNAL, "rb") as fh:
        return fh.read()


def seed_gen(i):
    text, _expects, _diff = C1.gen_fixture(REV, NONCE, i)
    if "\xe9" not in text:
        return text.encode("utf-8", "surrogateescape")
    return text.encode("latin-1", "replace")     # same as score_gen


def seed_sample(tag, n):
    return C1.sample_journal(REV, NONCE, tag, n)


def seed_allnames():
    """Every table name plus COMMON, two sessions, versions 1..9."""
    lines, ts = [], "2026-10-25T13:36:24-03:00"
    names = sorted(C1.TABLE) + C1.COMMON
    for pid in ("1918", "1952"):
        for k, name in enumerate(names):
            lines.append(C1.advert(ts, "plazir27", pid, name, 1 + k % 9))
    lines.insert(len(names), "-- Boot %032x --" % 0x5EED)
    return ("\n".join(lines) + "\n").encode()


SEEDS = [("committed", seed_committed()), ("allnames", seed_allnames())]
for _i in range(8):
    SEEDS.append(("gen%d" % _i, seed_gen(_i)))
SEEDS += [("sample1", seed_sample("fz1", 1)), ("sample2", seed_sample("fz2", 2)),
          ("sample3", seed_sample("fz3", 3))]
SMALL = SEEDS[1][1]           # allnames: ~40 lines, cheap systematic sweeps


# ---------------------------------------------------------------- mutators
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
    return raw[:i] + bytes([rng.choice([0x00, 0xff, 0xc3, 0xed, 0x80, 0x20,
                                        0x0d, 0x0a, 0x09, 0x7c])]) + raw[i:]


def op_byte_delete(rng, raw):
    if not raw:
        return None
    i = rng.randrange(len(raw))
    return raw[:i] + raw[i + 1:]


def op_line_delete(rng, raw):
    ls = _lines(raw)
    if len(ls) < 2:
        return None
    del ls[rng.randrange(len(ls))]
    return b"\n".join(ls)


def op_line_dup(rng, raw):
    ls = _lines(raw)
    if not ls:
        return None
    i = rng.randrange(len(ls))
    ls.insert(i, ls[i])
    return b"\n".join(ls)


def op_line_swap(rng, raw):
    ls = _lines(raw)
    if len(ls) < 3:
        return None
    i = rng.randrange(len(ls) - 1)
    ls[i], ls[i + 1] = ls[i + 1], ls[i]
    return b"\n".join(ls)


def op_cr_one(rng, raw):
    ls = _lines(raw)
    if not ls:
        return None
    i = rng.randrange(len(ls))
    ls[i] = ls[i] + b"\r"
    return b"\n".join(ls)


def op_crlf_all(rng, raw):
    return raw.replace(b"\n", b"\r\n")


def op_crlf_one_line(rng, raw):
    ls = _lines(raw)
    if len(ls) < 2:
        return None
    i = rng.randrange(len(ls) - 1)
    return b"\n".join(ls[:i + 1]) + b"\r\n" + b"\n".join(ls[i + 1:])


def op_boot_insert(rng, raw):
    ls = _lines(raw)
    i = rng.randrange(len(ls) + 1)
    boot = b"-- Boot %032x --" % rng.getrandbits(128)
    ls.insert(i, boot)
    return b"\n".join(ls)


def op_boot_insert_dup(rng, raw):
    ls = _lines(raw)
    i = rng.randrange(len(ls) + 1)
    bid = b"-- Boot " + b"0123456789abcdef" * 2 + b" --"
    return b"\n".join(ls[:i] + [bid, bid] + ls[i:])


def op_pid_flip(rng, raw):
    import re
    pat = re.compile(rb"xdg-desktop-portal-hyprland\[(\d+)\]")
    hits = list(pat.finditer(raw))
    if not hits:
        return None
    m = hits[rng.randrange(len(hits))]
    pid = m.group(1)
    kind = rng.randrange(5)
    if kind == 0:
        new = b"0" + pid
    elif kind == 1:
        new = b"0" * rng.randrange(1, 4) + pid
    elif kind == 2:
        new = pid + b"0"
    elif kind == 3:
        new = bytes([rng.randrange(0x30, 0x3a)]) + pid[1:]
    else:
        new = pid.rstrip(b"0") or b"0"
    if new == pid:
        return None
    return raw[:m.start(1)] + new + raw[m.end(1):]


def op_ver_digits(rng, raw):
    import re
    pat = re.compile(rb"\(ver (\d+)\)")
    hits = list(pat.finditer(raw))
    if not hits:
        return None
    m = hits[rng.randrange(len(hits))]
    kind = rng.randrange(7)
    if kind == 0:
        new = b"0"
    elif kind == 1:
        new = b"000001"
    elif kind == 2:
        new = b"9" * 6
    elif kind == 3:
        new = b"1" * 7
    elif kind == 4:
        new = b"1234567"
    elif kind == 5:
        new = b"10"
    else:
        new = "١٢".encode()          # Arabic-Indic digits (Unicode \d)
    return raw[:m.start(1)] + new + raw[m.end(1):]


def op_name_len(rng, raw):
    import re
    pat = re.compile(rb"Got interface: ([A-Za-z0-9_]+) \(ver")
    hits = list(pat.finditer(raw))
    if not hits:
        return None
    m = hits[rng.randrange(len(hits))]
    n = rng.choice([126, 127, 128, 129, 130])
    return raw[:m.start(1)] + b"a" * n + raw[m.end(1):]


def op_invalid_utf8(rng, raw):
    i = rng.randrange(len(raw) + 1)
    bad = rng.choice([b"\xff", b"\xfe", b"\xc3", b"\xed\xa0\x80", b"\xf0\x9f",
                      b"\x80\x80", b"\xff\xff\xff"])
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
               (b"[LOG]", b"[ERR]"), (b"[LOG]", b"[WARN]"),
               (b"Got interface:", b"got interface:"),
               (b"Got interface:", b"Got  interface:"),
               (b"Got interface:", b"Got interface:  ")]
    a, b = rng.choice(choices)
    return raw.replace(a, b, 1)


def op_trailing_text(rng, raw):
    ls = _lines(raw)
    idx = [i for i, ln in enumerate(ls) if b"Got interface" in ln]
    if not idx:
        return None
    i = rng.choice(idx)
    suf = rng.choice([b" extra", b" ", b"\t", b"\x00", b"|", b"\xff"])
    ls[i] = ls[i] + suf
    return b"\n".join(ls)


def op_leading_text(rng, raw):
    ls = _lines(raw)
    idx = [i for i, ln in enumerate(ls) if b"Got interface" in ln]
    if not idx:
        return None
    i = rng.choice(idx)
    pre = rng.choice([b"x ", b" ", b"\t", b"\x00", b"|", b"\xff"])
    ls[i] = pre + ls[i]
    return b"\n".join(ls)


def op_ts(rng, raw):
    import re
    pat = re.compile(rb"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}")
    hits = list(pat.finditer(raw))
    if not hits:
        return None
    m = hits[rng.randrange(len(hits))]
    new = rng.choice([b"2026-10-25 13:36:24", b"2026-13-45T25:61:61+99:99",
                      b"2026-10-25T13:36:24Z", b"2026-10-25T13:36:24",
                      "٢٠٢٦-10-25T13:36:24-03:00".encode(),
                      b"2026-10-25T13:36:24+0300", b"2026-10-25t13:36:24-03:00"])
    return raw[:m.start()] + new + raw[m.end():]


def op_host(rng, raw):
    import re
    pat = re.compile(rb"(-03:00) (\S+) xdg-desktop-portal-hyprland\[")
    hits = list(pat.finditer(raw))
    if not hits:
        return None
    m = hits[rng.randrange(len(hits))]
    new = rng.choice([b"h[", b"h:", "hé".encode(), b"h\x7f", b"h|h",
                      b"xdg-desktop-portal-hyprland["])
    return raw[:m.start(2)] + new + raw[m.end(2):]


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


OPS = [op_byte_flip, op_byte_insert, op_byte_delete, op_line_delete,
       op_line_dup, op_line_swap, op_cr_one, op_crlf_all, op_crlf_one_line,
       op_boot_insert, op_boot_insert_dup, op_pid_flip, op_ver_digits,
       op_name_len, op_invalid_utf8, op_no_trailing_nl, op_boot_only, op_nul,
       op_nul_all, op_spacing, op_trailing_text, op_leading_text, op_ts,
       op_host, op_reverse, op_double, op_append_boot, op_truncate]


# --------------------------------------------------------- systematic sets
def systematic():
    """Fixed sweeps that random ops cannot guarantee (every position etc.)."""
    out = []
    ls = _lines(seed_committed())
    for i in range(len(ls)):
        out.append(("boot-at-%d" % i,
                    b"\n".join(ls[:i] + [b"-- Boot " + b"ab" * 16 + b" --"]
                               + ls[i:])))
    small = _lines(SMALL)
    for i in range(len(small)):
        out.append(("boot-small-at-%d" % i,
                    b"\n".join(small[:i] + [b"-- Boot " + b"cd" * 16 + b" --"]
                               + small[i:])))
        out.append(("nul-small-at-%d" % i,
                    b"\n".join(small[:i] + [b"\x00" + small[i]]
                               + small[i + 1:])))
        out.append(("cr-small-line-%d" % i,
                    b"\n".join(small[:i] + [small[i] + b"\r"] + small[i + 1:])))
        out.append(("del-small-line-%d" % i,
                    b"\n".join(small[:i] + small[i + 1:])))
    # names at the class boundary, in a one-line journal
    ts = b"2026-10-25T13:36:24-03:00"
    for n in (0, 1, 127, 128, 129, 130):
        line = (ts + b" h xdg-desktop-portal-hyprland[1952]: [LOG]  | "
                b"Got interface: " + b"a" * n + b" (ver 1)\n")
        out.append(("name-len-%d" % n, line))
        out.append(("name-len-%d-diff" % n, line * 2))
    # version digit boundaries
    for v in (b"0", b"00", b"1", b"9", b"10", b"000001", b"999999",
              b"1000000", b"1234567", "١".encode(), "١٢٣٤٥٦".encode(),
              "١٢٣٤٥٦٧".encode()):
        out.append(("ver-%s" % v.decode("utf-8", "replace"),
                    ts + b" h xdg-desktop-portal-hyprland[1952]: [LOG]  | "
                    b"Got interface: wl_seat (ver " + v + b")\n"))
    # numeric vs lexicographic max (single fixture per pair)
    out.append(("ver-9-then-10",
                ts + b" h xdg-desktop-portal-hyprland[1]: [LOG]  | "
                b"Got interface: wl_seat (ver 9)\n" + ts +
                b" h xdg-desktop-portal-hyprland[1]: [LOG]  | "
                b"Got interface: wl_seat (ver 10)\n"))
    out.append(("ver-10-then-9",
                ts + b" h xdg-desktop-portal-hyprland[1]: [LOG]  | "
                b"Got interface: wl_seat (ver 10)\n" + ts +
                b" h xdg-desktop-portal-hyprland[1]: [LOG]  | "
                b"Got interface: wl_seat (ver 9)\n"))
    # pid string vs numeric identity
    for a, b in ((b"1952", b"01952"), (b"0", b"00"), (b"1952", b"1952"),
                 (b"1", b"01"), (b"007", b"7")):
        out.append(("pid-%s-%s" % (a.decode(), b.decode()),
                    ts + b" h xdg-desktop-portal-hyprland[" + a + b"]: [LOG]  | "
                    b"Got interface: wl_seat (ver 1)\n" + ts +
                    b" h xdg-desktop-portal-hyprland[" + b + b"]: [LOG]  | "
                    b"Got interface: wl_shm (ver 1)\n"))
    # empty-ish files
    for label, body in (("empty", b""), ("nl", b"\n"), ("nlnl", b"\n\n"),
                        ("nul", b"\x00"), ("crlf-only", b"\r\n"),
                        ("no-nl-advert", ts + b" h xdg-desktop-portal-hyprland"
                         b"[1]: [LOG]  | Got interface: wl_seat (ver 1)"),
                        ("boot-only", b"-- Boot " + b"a" * 32 + b" --\n"),
                        ("boot-boot", (b"-- Boot " + b"a" * 32 + b" --\n") * 2),
                        ("boot-upper", b"-- Boot " + b"A" * 32 + b" --\n"),
                        ("boot-short", b"-- Boot " + b"a" * 31 + b" --\n"),
                        ("boot-trail", b"-- Boot " + b"a" * 32 + b" ---\n")):
        out.append(("shape-%s" % label, body))
    # oversized boundary: exactly 8 MiB and one byte over
    pad = b"x" * (MAX_BYTES - 1) + b"\n"
    out.append(("size-exact-max", pad))
    out.append(("size-max-plus-1", pad + b"x"))
    return out


# ------------------------------------------------------------- execution
EXPECT_MODES = 6


def expect_mode(rng, raw, diff_allowed=True):
    """Deterministic (argv_extra, expects, diff) for a mutant journal."""
    text = raw.decode("utf-8", "replace")
    ss = C1.model_sessions(text)
    names = sorted(ss[-1]["names"]) if ss else []
    mode = rng.randrange(EXPECT_MODES)
    extra, expects = [], []
    if diff_allowed and rng.random() < 0.5:
        extra.append("--diff")
    if mode == 1 and names:
        expects = [names[rng.randrange(len(names))]]
    elif mode == 2 and names:
        expects = [names[rng.randrange(len(names))], "zz_absent_v1"]
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


def run_case(raw, extra, scratch, name):
    path = os.path.join(scratch, name)
    with open(path, "wb") as fh:
        fh.write(raw)
    return run_tool(["--journal-file", path] + extra, scratch)


def compare(raw, extra, expects, diff, scratch, name):
    want_out, want_rc = expected(raw, expects, diff)
    rc, out, err = run_case(raw, extra, scratch, name)
    want_bytes = want_out.encode()
    ok = rc == want_rc and out == want_bytes
    if ok and want_rc in (0, 1, 3) and err:
        ok = False
    return ok, (want_rc, want_out, rc, out, err)


def first_diff(want, got):
    a = want.splitlines()
    b = got.decode("utf-8", "replace").splitlines()
    for k in range(max(len(a), len(b))):
        x = a[k] if k < len(a) else None
        y = b[k] if k < len(b) else None
        if x != y:
            return k + 1, x, y
    return None, None, None


def class_key(want_rc, got_rc, want_out, got_out, err):
    if want_rc != got_rc:
        return "rc:%s->%s" % (want_rc, got_rc)
    if want_out != got_out.decode("utf-8", "replace"):
        n, x, y = first_diff(want_out, got_out)
        if x is None:
            return "extra-line"
        if y is None:
            return "missing-line"
        return "stdout-line:%s|%s" % (x[:40], (y or "")[:40])
    return "stderr"


# ------------------------------------------------------------- minimiser
def minimise(raw, extra, expects, diff, scratch):
    """Greedy line-deletion then per-line prefix/suffix trimming; any
    disagreement (rc or stdout) must persist."""
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
    # trim bytes from each remaining line (suffix first, then prefix)
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


# ------------------------------------------------------- CLI / contract
def cli_cases(scratch):
    """Cases whose expectation comes from the contract text, not model_out."""
    ok_j = os.path.join(scratch, "cli-ok.txt")
    with open(ok_j, "wb") as fh:
        fh.write(b"2026-10-25T13:36:24-03:00 h xdg-desktop-portal-hyprland[1]: "
                 b"[LOG]  | Got interface: wl_seat (ver 1)\n")
    empty_j = os.path.join(scratch, "cli-empty.txt")
    open(empty_j, "wb").close()
    missing = os.path.join(scratch, "cli-missing.txt")
    d = os.path.join(scratch, "cli-dir")
    os.makedirs(d, exist_ok=True)
    stub = os.path.join(scratch, "cli-stub")
    with open(stub, "w") as fh:
        fh.write("#!/bin/sh\ncat %s\n" % ok_j)
    os.chmod(stub, 0o755)
    zero_j = os.path.join(scratch, "cli-zero.txt")
    with open(zero_j, "wb") as fh:
        fh.write(b"x\n")
    os.chmod(zero_j, 0o000)
    link_j = os.path.join(scratch, "cli-link.txt")
    os.symlink(ok_j, link_j)
    bindir = os.path.join(scratch, "cli-bin")
    os.makedirs(bindir, exist_ok=True)
    spawn_stub = os.path.join(bindir, "journalctl")
    with open(spawn_stub, "w") as fh:
        fh.write("#!/bin/sh\ntouch %s\nexit 1\n" % os.path.join(scratch,
                                                               "spawned"))
    os.chmod(spawn_stub, 0o755)
    cases = [
        ("both flags", ["--journal-file", ok_j, "--live"],
         "MADO_GLOBALS: SETUP usage\n", 2, "contract"),
        ("neither flag", [], "MADO_GLOBALS: SETUP usage\n", 2, "contract"),
        ("journalctl without live", ["--journal-file", ok_j, "--journalctl", "x"],
         "MADO_GLOBALS: SETUP usage\n", 2, "contract"),
        ("abbrev flag", ["--journal-fil", ok_j],
         "MADO_GLOBALS: SETUP usage\n", 2, "contract"),
        ("abbrev diff", ["--journal-file", ok_j, "--dif"],
         "MADO_GLOBALS: SETUP usage\n", 2, "contract"),
        ("unknown flag", ["--journal-file", ok_j, "--frobnicate"],
         "MADO_GLOBALS: SETUP usage\n", 2, "contract"),
        ("diff with value", ["--journal-file", ok_j, "--diff=1"],
         "MADO_GLOBALS: SETUP usage\n", 2, "contract"),
        ("expect space", ["--journal-file", ok_j, "--expect=a b"],
         "MADO_GLOBALS: SETUP bad_expect\n", 2, "contract"),
        ("expect empty", ["--journal-file", ok_j, "--expect="],
         "MADO_GLOBALS: SETUP bad_expect\n", 2, "contract"),
        ("expect 129", ["--journal-file", ok_j, "--expect=" + "a" * 129],
         "MADO_GLOBALS: SETUP bad_expect\n", 2, "contract"),
        ("expect semicolon", ["--journal-file", ok_j, "--expect=a;b"],
         "MADO_GLOBALS: SETUP bad_expect\n", 2, "contract"),
        ("expect slash", ["--journal-file", ok_j, "--expect=a/b"],
         "MADO_GLOBALS: SETUP bad_expect\n", 2, "contract"),
        ("expect non-ascii", ["--journal-file", ok_j, "--expect=é"],
         "MADO_GLOBALS: SETUP bad_expect\n", 2, "contract"),
        ("expect dash value", ["--journal-file", ok_j, "--expect", "-x"],
         "MADO_GLOBALS: SETUP bad_expect\n", 2, "ambiguous"),
        ("expect dash value eq", ["--journal-file", ok_j, "--expect=-x"],
         "MADO_GLOBALS: SETUP bad_expect\n", 2, "contract"),
        ("missing file", ["--journal-file", missing],
         "MADO_GLOBALS: SETUP unreadable\n", 2, "contract"),
        ("directory", ["--journal-file", d],
         "MADO_GLOBALS: SETUP unreadable\n", 2, "contract"),
        ("empty path alone", ["--journal-file", ""],
         "MADO_GLOBALS: SETUP unreadable\n", 2, "ambiguous"),
        ("empty path + live", ["--journal-file", "", "--live",
                              "--journalctl", stub],
         "MADO_GLOBALS: SETUP usage\n", 2, "ambiguous"),
        ("expect 128 ok", ["--journal-file", ok_j, "--expect=" + "a" * 128],
         None, 1, "contract"),
        ("mode-000 file", ["--journal-file", zero_j],
         "MADO_GLOBALS: SETUP unreadable\n", 2, "contract"),
        ("symlink to journal", ["--journal-file", link_j],
         None, 0, "contract"),
        ("file mode does not spawn", ["--journal-file", ok_j],
         None, 0, "contract"),
    ]
    rows = []
    for label, argv, want_out, want_rc, kind in cases:
        env = ENV
        if label == "file mode does not spawn":
            env = dict(ENV, PATH=bindir + ":/usr/bin")
            try:
                os.unlink(os.path.join(scratch, "spawned"))
            except OSError:
                pass
        rc, out, err = run_tool(argv, scratch, env=env)
        if label == "file mode does not spawn" and os.path.exists(
                os.path.join(scratch, "spawned")):
            rows.append({"case": label, "argv": argv, "ok": False,
                         "kind": kind, "want_rc": want_rc, "rc": rc,
                         "want_out": "no spawn", "got_out": "spawned journalctl",
                         "stderr": ""})
            continue
        if want_out is None:
            want_out, want_rc = C1.model_out(
                open(ok_j, "rb").read().decode("utf-8", "replace"),
                ["a" * 128] if "expect" in " ".join(argv) else [], False)
        ok = rc == want_rc and out == want_out.encode()
        rows.append({"case": label, "argv": argv, "ok": ok, "kind": kind,
                     "want_rc": want_rc, "rc": rc,
                     "want_out": want_out, "got_out": out.decode("utf-8", "replace"),
                     "stderr": err.decode("utf-8", "replace")[:200]})
    return rows


def live_cases(scratch, mutants):
    """--live parity: a stub echoes the mutant; the parse must match model_out.
    Plus the two setup classes the contract names."""
    bindir = os.path.join(scratch, "livebin")
    os.makedirs(bindir, exist_ok=True)
    rows = []
    for k, (label, raw) in enumerate(mutants):
        data = os.path.join(scratch, "live-%d.bin" % k)
        with open(data, "wb") as fh:
            fh.write(raw)
        stub = os.path.join(bindir, "journalctl")
        with open(stub, "w") as fh:
            fh.write("#!/bin/sh\ncat %s\n" % data)
        os.chmod(stub, 0o755)
        extra, expects, diff = expect_mode(_rng("live" + label), raw)
        want_out, want_rc = expected(raw, expects, diff)
        rc, out, err = run_tool(["--live", "--journalctl", stub] + extra, scratch)
        ok = rc == want_rc and out == want_out.encode()
        rows.append({"case": "live:%s" % label, "ok": ok, "want_rc": want_rc,
                     "rc": rc, "want_out": want_out,
                     "got_out": out.decode("utf-8", "replace")})
    fail = os.path.join(bindir, "jfail")
    with open(fail, "w") as fh:
        fh.write("#!/bin/sh\nexit 1\n")
    os.chmod(fail, 0o755)
    rc, out, err = run_tool(["--live", "--journalctl", fail], scratch)
    rows.append({"case": "live:nonzero-exit", "ok": rc == 5 and
                 out == b"MADO_GLOBALS: SETUP journalctl_failed\n",
                 "want_rc": 5, "rc": rc,
                 "want_out": "MADO_GLOBALS: SETUP journalctl_failed\n",
                 "got_out": out.decode("utf-8", "replace")})
    gw = os.path.join(bindir, "jgw")
    with open(gw, "w") as fh:
        fh.write("#!/bin/sh\nexit 0\n")
    os.chmod(gw, 0o775)
    rc, out, err = run_tool(["--live", "--journalctl", gw], scratch)
    rows.append({"case": "live:group-writable", "ok": rc == 5 and
                 out == b"MADO_GLOBALS: SETUP journalctl_unusable\n",
                 "want_rc": 5, "rc": rc,
                 "want_out": "MADO_GLOBALS: SETUP journalctl_unusable\n",
                 "got_out": out.decode("utf-8", "replace")})
    # output-size boundary: exactly 8 MiB is not too_large, one byte more is
    for label, n, want_rc, want_out in (
            ("exact-max", MAX_BYTES, 3,
             "MADO_GLOBALS: sessions=0 latest_pid=- interfaces=0 classes=- "
             "expected_missing=- verdict=NO_SESSIONS\n"),
            ("max-plus-1", MAX_BYTES + 1, 5,
             "MADO_GLOBALS: SETUP journalctl_too_large\n")):
        big = os.path.join(bindir, "jbig-" + label)
        with open(big, "w") as fh:
            fh.write("#!/bin/sh\nhead -c %d /dev/zero | tr '\\0' x\n" % n)
        os.chmod(big, 0o755)
        rc, out, err = run_tool(["--live", "--journalctl", big], scratch,
                                timeout=120)
        rows.append({"case": "live:" + label,
                     "ok": rc == want_rc and out == want_out.encode(),
                     "want_rc": want_rc, "rc": rc, "want_out": want_out,
                     "got_out": out.decode("utf-8", "replace")[:120]})
    return rows


# ------------------------------------------------- fixture-blindness probe
def fixture_version_census():
    """Versions and PIDs the MODEL actually accepts from the 24 scored
    fixtures' journals (not raw tokens: noise lines are ignored by both).
    Numeric-max vs lexicographic-max is only distinguishable if an accepted
    version has two digits; pid-string vs pid-number identity only if an
    accepted pid has a leading zero."""
    vers, pids = set(), set()
    sources = [("committed", seed_committed())]
    for i in range(8):
        sources.append(("gen%d" % i, seed_gen(i)))
    for tag, n in (("diff0", 3), ("diff1", 1), ("expect0", 1),
                   ("expectmiss0", 1), ("nosess0", 1)):
        sources.append((tag, C1.sample_journal(REV, NONCE, tag, n)))
    rng = _rng("nosess0")
    sources.append(("nosess0-noise", ("\n".join(
        C1.noise_lines(rng, C1.ts_of(rng, 1), "4242"))).encode("latin-1",
                                                              "replace") + b"\n"))
    sources.append(("nosess1", b""))
    sources.append(("toolarge1", b"x" * (MAX_BYTES - 1) + b"\n"))
    for label, raw in sources:
        for s in C1.model_sessions(raw.decode("utf-8", "replace")):
            pids.add(s["pid"])
            for _count, ver in s["names"].values():
                vers.add(ver)
    return {"accepted_versions": sorted(vers),
            "max_version_digits": max(len(str(v)) for v in vers),
            "accepted_pids_with_leading_zero": sorted(
                p for p in pids if len(p) > 1 and p[0] == "0"),
            "sources": [s[0] for s in sources]}


# ------------------------------------------------------------------ main
def main():
    global REF, RECEIPT, SUMMARY
    quick = "--quick" in sys.argv
    jobs = 8
    for k, a in enumerate(sys.argv):
        if a == "--jobs":
            jobs = int(sys.argv[k + 1])
        elif a == "--tool":
            REF = os.path.abspath(sys.argv[k + 1])
    if REF != os.path.join(SEAT, "ref-tool.py"):
        tag = os.path.basename(REF).replace(".py", "")
        RECEIPT = os.path.join(SEAT, "fuzz-receipt-%s.txt" % tag)
        SUMMARY = os.path.join(SEAT, "fuzz-summary-%s.json" % tag)
    scratch = tempfile.mkdtemp(prefix="c1fuzz-")
    os.chmod(scratch, 0o755)
    log = []

    def say(s):
        log.append(s)
        print(s, flush=True)

    say("fuzz: ref=%s sha256=%s" % (REF, hashlib.sha256(
        open(REF, "rb").read()).hexdigest()))
    say("fuzz: counter=%s model_out/model_sessions/gen_fixture imported via "
        "importlib (main not executed)" % COUNTER)
    say("fuzz: seeds=%s" % ",".join("%s:%dB" % (n, len(b)) for n, b in SEEDS))

    # identity checks on the two regexes and the class tables
    import re as _re
    same_re = (C1.ADV_RE.pattern ==
               r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}) (\S+) "
               r"xdg-desktop-portal-hyprland\[(\d+)\]: \[LOG\]  \| "
               r"Got interface: ([A-Za-z0-9_]{1,128}) \(ver (\d{1,6})\)")
    refsrc = open(REF, "r", encoding="utf-8").read()
    ref_ns = {"__name__": "refprobe"}
    exec(compile(refsrc, REF, "exec"), ref_ns)
    say("fuzz: advert-regex-identical=%s boot-regex-identical=%s table-identical=%s"
        % (C1.ADV_RE.pattern == ref_ns["ADVERT"].pattern,
           C1.BOOT_RE.pattern == ref_ns["BOOT"].pattern,
           C1.TABLE == ref_ns["CLASS_OF"]))
    say("fuzz: adv_re_matches_contract_text=%s" % same_re)

    # build the mutant corpus
    corpus = []
    variants = 6 if quick else 12
    for name, raw in SEEDS:
        for op in OPS:
            for v in range(variants):
                rng = _rng("%s|%s|%d" % (name, op.__name__, v))
                try:
                    m = op(rng, raw)
                except Exception as exc:      # a mutator bug, not a finding
                    say("fuzz: MUTATOR-ERROR %s/%s/%d %r" % (name, op.__name__,
                                                             v, exc))
                    continue
                if m is None or m == raw:
                    continue
                corpus.append(("%s/%s/%d" % (name, op.__name__, v), m))
    corpus += systematic()
    say("fuzz: corpus=%d (random=%d systematic=%d)"
        % (len(corpus), len(corpus) - len(systematic()), len(systematic())))

    # run them
    results = []

    def work(item):
        idx, (label, raw) = item
        rng = _rng("exp|" + label)
        extra, expects, diff = expect_mode(rng, raw)
        ok, detail = compare(raw, extra, expects, diff, scratch, "m%05d.txt" % idx)
        return idx, label, raw, extra, expects, diff, ok, detail

    with ThreadPoolExecutor(max_workers=jobs) as pool:
        for n, res in enumerate(pool.map(work, list(enumerate(corpus)))):
            results.append(res)
            if (n + 1) % 250 == 0:
                say("fuzz: ran %d/%d" % (n + 1, len(corpus)))

    bad = [r for r in results if not r[6]]
    say("fuzz: mutants=%d disagreements=%d" % (len(results), len(bad)))

    classes = {}
    for idx, label, raw, extra, expects, diff, ok, detail in bad:
        want_rc, want_out, rc, out, err = detail
        key = class_key(want_rc, rc, want_out, out, err)
        classes.setdefault(key, []).append((idx, label, raw, extra, expects,
                                            diff, detail))

    findings = []
    for key, items in sorted(classes.items()):
        idx, label, raw, extra, expects, diff, detail = items[0]
        small, runs = minimise(raw, extra, expects, diff, scratch)
        want_out, want_rc = expected(small, expects, diff)
        rc, out, err = run_case(small, extra, scratch, "_final.txt")
        findings.append({
            "class": key, "n_mutants": len(items),
            "labels": sorted({i[1] for i in items})[:12],
            "argv_extra": extra, "expects": expects,
            "minimised_bytes": len(small),
            "minimised_repr": repr(small)[:600],
            "minimise_runs": runs,
            "want_rc": want_rc, "want_out": want_out,
            "got_rc": rc, "got_out": out.decode("utf-8", "replace"),
            "got_stderr": err.decode("utf-8", "replace")[:200],
        })
        say("fuzz: DISAGREE class=%r n=%d minimal=%dB rc want=%s got=%s"
            % (key, len(items), len(small), want_rc, rc))

    live_mutants = [(l, r) for l, r in corpus[:20]] + \
                   [("allnames", SMALL), ("committed", seed_committed())]
    lrows = live_cases(scratch, live_mutants)
    say("fuzz: live cases=%d disagreements=%d"
        % (len(lrows), sum(0 if r["ok"] else 1 for r in lrows)))

    crows = cli_cases(scratch)
    hard = [r for r in crows if not r["ok"] and r["kind"] == "contract"]
    amb = [r for r in crows if not r["ok"] and r["kind"] == "ambiguous"]
    say("fuzz: cli cases=%d contract-mismatches=%d ambiguous-mismatches=%d"
        % (len(crows), len(hard), len(amb)))
    for r in crows:
        if not r["ok"]:
            say("fuzz: CLI-%s %s argv=%r want=%r/%s got=%r/%s"
                % ("MISMATCH" if r["kind"] == "contract" else "AMBIGUOUS",
                   r["case"], r["argv"][1:], r["want_out"][:80], r["want_rc"],
                   r["got_out"][:80], r["rc"]))

    census = fixture_version_census()
    say("fuzz: fixture-census accepted_versions=%s max_version_digits=%d "
        "accepted_pids_with_leading_zero=%s sources=%s"
        % (census["accepted_versions"], census["max_version_digits"],
           census["accepted_pids_with_leading_zero"], len(census["sources"])))

    summary = {"mutants": len(results), "disagreements": len(bad),
               "classes": len(classes), "findings": findings,
               "live": lrows, "cli": crows, "census": census}
    with open(SUMMARY, "w") as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
    with open(RECEIPT, "w") as fh:
        fh.write("\n".join(log) + "\n")
        for f in findings:
            fh.write("DISAGREEMENT %s\n  minimal=%s\n  argv=%r\n  want_rc=%s "
                     "got_rc=%s\n  want=%r\n  got=%r\n"
                     % (f["class"], f["minimised_repr"], f["argv_extra"],
                        f["want_rc"], f["got_rc"], f["want_out"],
                        f["got_out"]))
        for r in lrows:
            if not r["ok"]:
                fh.write("LIVE-DISAGREEMENT %r want=%r got=%r\n"
                         % (r["case"], r["want_out"], r["got_out"]))
        for r in crows:
            if not r["ok"]:
                fh.write("CLI-MISMATCH %s argv=%r want=%r rc=%s got=%r rc=%s "
                         "stderr=%r\n" % (r["case"], r["argv"][1:],
                                          r["want_out"], r["want_rc"],
                                          r["got_out"], r["rc"], r["stderr"]))
    shutil.rmtree(scratch, ignore_errors=True)
    print("fuzz: receipt=%s summary=%s" % (RECEIPT, SUMMARY))
    return 0


if __name__ == "__main__":
    sys.exit(main())

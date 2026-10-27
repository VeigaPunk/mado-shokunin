#!/usr/bin/env python3
"""C1/ExecKeysymNames proof: keysyms.py vs the pinned how-to-type judge.

For every ARG in the sweep, runs
    /usr/lib/xkbcommon/xkbcli-how-to-type --keymap=KM --disable-compose --keysym ARG
in a clean environment (PATH=/usr/bin only; HOME and XDG_CONFIG_HOME inside the
scratch dir so no user xkb include path can exist) and compares the FIRST stdout
line and the exit status with keysyms.parse_arg / keysyms.header_line.

Writes receipts/names-diff.txt (one TSV row per ARG) and prints a summary.
Read-only: opens the keymap, starts no socket, writes only the receipt.
"""

import base64
import hashlib
import importlib.util
import os
import random
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

JUDGE = "/usr/lib/xkbcommon/xkbcli-how-to-type"
COMPILE = "/usr/lib/xkbcommon/xkbcli-compile-keymap"
SEAT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-49/w1/ExecKeysymNames"
SCRATCH = "/fast/scratch/hyaku/mado-r49/ExecKeysymNames"
RECEIPTS = os.path.join(SEAT, "receipts")

spec = importlib.util.spec_from_file_location("keysyms", os.path.join(SEAT, "keysyms.py"))
keysyms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(keysyms)


def clean_env():
    return {
        "PATH": "/usr/bin",
        "HOME": os.path.join(SCRATCH, "home"),
        "XDG_CONFIG_HOME": os.path.join(SCRATCH, "xdg"),
        "TMPDIR": os.path.join(SCRATCH, "tmp"),
    }


def build_args(rng):
    args = []
    see = set()

    def add(a):
        if a not in see:
            see.add(a)
            args.append(a)

    names = sorted(keysyms._NAMES)
    for n in names:                                   # 2638 keysym names
        add(n)
    values = sorted(keysyms._CANON)
    for v in values:                                  # 2505 values, decimal
        add(str(v))
    for v in values:                                  # 2505 values, 0x hex
        add("0x%x" % v)
    # 2500 nonce numerics spread over the whole legal and illegal ranges
    for _ in range(2500):                             # 2500 nonce numerics
        v = rng.randrange(0, 0x20000000)
        add(str(v))
    for _ in range(200):                              # 200 nonce hex numerics
        v = rng.randrange(0, 0x20000000)
        add("0x%x" % v)
    for _ in range(200):                              # 200 nonce U-notation
        add("U%04X" % rng.randrange(0, 0x120000))
    for e in [                                        # edge forms
        "", " ", " 47", "\t47", "\n47", "+47", "-47", "+", "-", "0", "00",
        "0x", "0X2f", "0x2F", "0x0", "0x00", "0x1fffffff", "0x20000000",
        "0xffffffff", "0x100000000", "536870911", "536870912", "9999999999999999999999",
        "NoSymbol", "nosuchsym", "VoidSymbol", "U", "U+0041", "U0041", "u0041",
        "U0000", "U0001", "U0009", "U000a", "U000d", "U001b", "U007f", "U0080",
        "U009f", "U00a0", "U00ff", "U0100", "U01000000", "U010000ff",
        "U01000100", "U0110ffff", "U00110000", "U10FFFF", "U110000",
        "XF86_ScreenSaver", "XF86_Screensaver", "XF86_0x2f", "XF86_", "XF86",
        "slash ", " slash", "SLASH", "Slash", "Kanji_Bangou", "Codeinput",
        "0x2f ", "47 ", "0x-1", "0x+1", "0x 1", "0x1g", "12abc", "1.5",
        "4278190080", "4294967296", "0x1p3", "0b101", "0o17",
    ]:
        add(e)
    return args


def run_judge(km, arg):
    p = subprocess.run(
        [JUDGE, "--keymap=" + km, "--disable-compose", "--keysym", arg],
        env=clean_env(), stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    return p.returncode, p.stdout, p.stderr


def main():
    rng = random.Random(49)
    os.makedirs(RECEIPTS, exist_ok=True)
    for sub in ("home", "xdg", "tmp"):
        os.makedirs(os.path.join(SCRATCH, sub), exist_ok=True)
    km = os.path.join(SCRATCH, "br.xkb")
    with open(km, "wb") as fd:
        p = subprocess.run([COMPILE, "--layout", "br", "--options", "compose:caps"],
                           env=clean_env(), stdout=fd, stderr=subprocess.PIPE, timeout=120)
    assert p.returncode == 0, p.stderr
    km_sha = hashlib.sha256(open(km, "rb").read()).hexdigest()

    args = build_args(rng)

    def check(arg):
        rc, out, err = run_judge(km, arg)
        line = out.decode("utf-8", "replace").split("\n", 1)[0] if out else ""
        ks = keysyms.parse_arg(arg)
        if ks is None:
            want_rc, want_line = 2, ""
        else:
            want_rc, want_line = 0, keysyms.header_line(ks)
        ok = (rc == want_rc and line == want_line)
        return (ok, arg, rc, want_rc, line, want_line)

    with ThreadPoolExecutor(max_workers=12) as pool:
        results = list(pool.map(check, args))

    bad = [r for r in results if not r[0]]
    path = os.path.join(RECEIPTS, "names-diff.txt")
    with open(path, "w", encoding="utf-8") as fd:
        fd.write("# judge: %s (sha256 %s)\n" % (JUDGE, sha256(JUDGE)))
        fd.write("# keymap: xkbcli-compile-keymap --layout br --options compose:caps -> sha256 %s\n"
                 % km_sha)
        fd.write("# env: PATH=/usr/bin HOME=$SCRATCH/home XDG_CONFIG_HOME=$SCRATCH/xdg TMPDIR=$SCRATCH/tmp\n")
        fd.write("# args: %d (names=%d values_dec=%d values_hex=%d nonce=%d edge+extra)\n"
                 % (len(args), len(keysyms._NAMES), len(keysyms._CANON),
                    len(keysyms._CANON), 2900))
        fd.write("# columns: STATUS judge_rc tool_rc judge_header tool_header ARG\n")
        for ok, arg, rc, wrc, line, want in results:
            fd.write("%s\t%d\t%d\t%s\t%s\t%s\n"
                     % ("OK" if ok else "FAIL", rc, wrc,
                        line.replace("\t", "\\t") or "-",
                        want.replace("\t", "\\t") or "-",
                        arg.replace("\t", "\\t").replace("\n", "\\n") or "<empty>"))
    print("args=%d ok=%d fail=%d" % (len(results), len(results) - len(bad), len(bad)))
    for r in bad[:20]:
        print("FAIL", repr(r[1]), "judge rc=%d line=%r" % (r[2], r[4]),
              "tool rc=%d line=%r" % (r[3], r[5]))
    return 1 if bad else 0


def sha256(path):
    import hashlib as h
    return h.sha256(open(path, "rb").read()).hexdigest()


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""C1/ExecKeysymNames supplementary proof: keymap independence + hostile ARG shapes.

1. Header line for 300 sampled ARGs under a SECOND keymap (--layout us) must equal
   the one under --layout br and equal keysyms.header_line (the header is printed
   before the keymap is walked, so it must not depend on the keymap).
2. Hostile ARG shapes (non-ASCII, over-long, 9+ hex digits, leading zeros,
   whitespace variants, sign forms) compared against the judge as in the main sweep.

Writes receipts/names-diff-edge.txt and prints a summary.
"""

import hashlib
import importlib.util
import os
import subprocess
import sys

JUDGE = "/usr/lib/xkbcommon/xkbcli-how-to-type"
COMPILE = "/usr/lib/xkbcommon/xkbcli-compile-keymap"
SEAT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-49/w1/ExecKeysymNames"
SCRATCH = "/fast/scratch/hyaku/mado-r49/ExecKeysymNames"
RECEIPTS = os.path.join(SEAT, "receipts")

spec = importlib.util.spec_from_file_location("keysyms", os.path.join(SEAT, "keysyms.py"))
keysyms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(keysyms)


def env():
    return {"PATH": "/usr/bin",
            "HOME": os.path.join(SCRATCH, "home"),
            "XDG_CONFIG_HOME": os.path.join(SCRATCH, "xdg"),
            "TMPDIR": os.path.join(SCRATCH, "tmp")}


def compile_keymap(layout, extra, out):
    with open(out, "wb") as fd:
        cmd = [COMPILE] + (["--layout", layout] + extra)
        p = subprocess.run(cmd, env=env(), stdout=fd, stderr=subprocess.PIPE, timeout=120)
    assert p.returncode == 0, p.stderr
    return hashlib.sha256(open(out, "rb").read()).hexdigest()


def judge(km, arg):
    p = subprocess.run([JUDGE, "--keymap=" + km, "--disable-compose", "--keysym", arg],
                       env=env(), stdin=subprocess.DEVNULL,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    line = p.stdout.decode("utf-8", "replace").split("\n", 1)[0] if p.stdout else ""
    return p.returncode, line, p.stderr


def expect(arg):
    ks = keysyms.parse_arg(arg)
    return (2, "") if ks is None else (0, keysyms.header_line(ks))


def main():
    br = os.path.join(SCRATCH, "br.xkb")
    us = os.path.join(SCRATCH, "us.xkb")
    br_sha = compile_keymap("br", ["--options", "compose:caps"], br)
    us_sha = compile_keymap("us", [], us)

    # a deterministic 300-ARG sample from the main sweep's domains
    sample = []
    names = sorted(keysyms._NAMES)
    for i in range(0, len(names), 9):
        sample.append(names[i])
    vals = sorted(keysyms._CANON)
    for i in range(0, len(vals), 25):
        sample.append(str(vals[i]))
        sample.append("0x%x" % vals[i])
    sample = sample[:300]

    hostile = [
        "é", "ä", "€", "日本語", "\u00a047", "47\u00a0",
        "a" * 200, "0x" + "f" * 100, "0x" + "f" * 8, "0x" + "f" * 9,
        "0x0000002f", "0x000000002f", "0x0000000000000000000002f",
        "U00000041", "U000000041", "U0000000000041",
        "536870911", "536870912", "0x1fffffff", "0x1FFFFFFF",
        "-0", "-0x2f", "--keysym", "47\n", "47\r", "\v47", "\f47", "   47",
        "4 7", "4\t7", "XF86_XF86AudioMute", "XF86_AudioMute", "XF86_Audio_Mute",
        "dead_tilde", "dead_perispomeni", "U+0000041", "Ux41", "0x2F", "0X2F",
        "NoSymbol ", " NoSymbol", "ninety", "0x2f0x2f", "0x2f\t",
    ]

    rows = []
    for arg in sample + hostile:
        rc_br, line_br, _ = judge(br, arg)
        rc_us, line_us, _ = judge(us, arg)
        rc_x, line_x = expect(arg)
        ok = (rc_br == rc_x and line_br == line_x and rc_us == rc_br and line_us == line_br)
        rows.append((ok, arg, rc_br, rc_us, rc_x, line_br, line_x))

    bad = [r for r in rows if not r[0]]
    path = os.path.join(RECEIPTS, "names-diff-edge.txt")
    with open(path, "w", encoding="utf-8") as fd:
        fd.write("# judge: %s sha256 %s\n" % (JUDGE, hashlib.sha256(open(JUDGE, "rb").read()).hexdigest()))
        fd.write("# keymaps: br(compose:caps) sha256 %s ; us sha256 %s\n" % (br_sha, us_sha))
        fd.write("# sample=%d (names+values) hostile=%d\n" % (len(sample), len(hostile)))
        fd.write("# columns: STATUS judge_br_rc judge_us_rc tool_rc header_br header_tool ARG\n")
        for ok, arg, rb, ru, rk, lb, lk in rows:
            fd.write("%s\t%d\t%d\t%d\t%s\t%s\t%s\n"
                     % ("OK" if ok else "FAIL", rb, ru, rk,
                        lb or "-", lk or "-",
                        arg.replace("\t", "\\t").replace("\n", "\\n").replace("\r", "\\r") or "<empty>"))
    print("rows=%d ok=%d fail=%d" % (len(rows), len(rows) - len(bad), len(bad)))
    for r in bad:
        print("FAIL", repr(r[1]), r[2:])
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

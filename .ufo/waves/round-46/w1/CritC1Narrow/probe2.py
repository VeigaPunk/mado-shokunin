#!/usr/bin/env python3
"""CritC1Narrow level-2 probe: file/argv-level divergences the in-process battery cannot show."""
import json
import os
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REF = os.path.join(LANE, ".ufo/waves/round-46/l1-draft/mado-devices.py")
SCR = "/fast/scratch/hyaku/mado-r46/CritC1Narrow"
D = os.path.join(SCR, "probe2")
os.makedirs(D, exist_ok=True)

KB = {"address": "0x1", "name": "kbd-1", "rules": "", "model": "", "layout": "us", "variant": "", "options": "",
      "active_layout_index": 0, "active_keymap": "x", "capsLock": False, "numLock": False, "main": False}
MOUSE = {"address": "0x2", "name": "mouse-1", "defaultSpeed": 0.0, "scrollFactor": -1.0}


def dump(path, keyboards=(KB,), mice=(MOUSE,), raw=None):
    with open(path, "wb") as f:
        f.write(raw if raw is not None else json.dumps(
            {"mice": list(mice), "keyboards": list(keyboards), "tablets": [], "touch": [], "switches": []}).encode())


def run(tool, args, stdin=None):
    p = subprocess.run([sys.executable, "-I", tool] + args, capture_output=True, input=stdin, cwd=D)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def show(label, tool_var, args, stdin=None):
    a = run(REF, args, stdin)[0:2]
    b = run(tool_var, args, stdin)[0:2]
    if a != b:
        print("DIFF %s\n  ref rc=%d %r\n  var rc=%d %r" % (label, a[0], a[1][-260:], b[0], b[1][-260:]))
    else:
        print("same %s" % label)


def main():
    name = sys.argv[1]
    var = os.path.join(SCR, "work-%s" % name, "mado-devices.py")
    dp = os.path.join(D, "devs.json")
    dump(dp)

    # P07: a dump whose mouse scrollFactor is NaN
    nanp = os.path.join(D, "nan.json")
    with open(nanp, "wb") as f:
        f.write(b'{"keyboards": [{"name": "kbd-1"}], "mice": [{"name": "mouse-1", "scrollFactor": NaN}]}')
    show("P07-nan-scrollFactor", var, ["--devices", nanp, "--config", os.path.join(D, "empty.conf")])

    # P08: a config with one invalid UTF-8 byte in a comment
    bad = os.path.join(D, "bad.conf")
    with open(bad, "wb") as f:
        f.write(b"# caf\xe9 latte\ninput:kb_layout = br\n")
    show("P08-invalid-utf8-config", var, ["--devices", dp, "--config", bad])

    # P10: a FIFO as --config
    fifo = os.path.join(D, "fifo.conf")
    if os.path.exists(fifo):
        os.unlink(fifo)
    os.mkfifo(fifo)
    show("P10-fifo-config", var, ["--devices", dp, "--config", fifo])

    # P11: a config of exactly 1048576 bytes
    exact = os.path.join(D, "exact.conf")
    with open(exact, "wb") as f:
        f.write(b"#" + b"x" * 1048574 + b"\n")
    show("P11-exact-1MiB", var, ["--devices", dp, "--config", exact])
    over = os.path.join(D, "over.conf")
    with open(over, "wb") as f:
        f.write(b"#" + b"x" * 1048575 + b"\n")
    show("P11-over-1MiB", var, ["--devices", dp, "--config", over])

    # P12: --devices given twice
    dump(os.path.join(D, "d2.json"), keyboards=(dict(KB, layout="br"),))
    show("P12-devices-twice", var, ["--devices", dp, "--devices", os.path.join(D, "d2.json"),
                                    "--config", os.path.join(D, "empty.conf")])

    # P13: file one leaves a block open, file two continues it
    f1 = os.path.join(D, "a.conf")
    f2 = os.path.join(D, "b.conf")
    with open(f1, "w") as f:
        f.write("device {\n  name = mouse-1\n")
    with open(f2, "w") as f:
        f.write("scroll_factor = 2\n")
    show("P13-stack-shared", var, ["--devices", dp, "--config", f1, "--config", f2])

    # P21: a leading CR before a directive comment
    cr = os.path.join(D, "cr.conf")
    with open(cr, "wb") as f:
        f.write(b"\r# hyprlang if X\ninput:kb_layout = us\n")
    show("P21-leading-CR-directive", var, ["--devices", dp, "--config", cr])


if __name__ == "__main__":
    main()

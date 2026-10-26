#!/usr/bin/env python3
"""FIFO hang proof for the round-47 oracle harness.

A named pipe named like a desktop entry, placed in the LAST applications
directory (XDG_DATA_HOME/applications), makes the pinned resolver block on
open(2): the script's find expression is

    find <dir_n>/. ... <dir_1>/. -type f (A_n) -o (A_1)

so only the first path group carries -type f; the groups for the later
directories (XDG_DATA_HOME is appended first and therefore ends up last) are
unconstrained, and the FIFO is discovered and then read.

This script proves the harness side of that: oracle.run_once() answers with the
timeout rc (124), flags timed_out, and leaves no process behind (the sandbox
dies with bwrap).  It is a receipt, not product code.

  receipts/fifo-hang-proof.py --work DIR [--timeout 3]
"""

import argparse
import importlib.util
import sys as _sys

_sys.dont_write_bytecode = True  # never leave __pycache__ in the seat dir
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ORACLE = os.path.join(HERE, "..", "oracle.py")


def load_oracle():
    spec = importlib.util.spec_from_file_location("oracle_mod", ORACLE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--timeout", type=float, default=3.0)
    ap.add_argument("--settle", type=float, default=5.0,
                    help="seconds to wait for namespace teardown to settle")
    args = ap.parse_args(argv)
    oracle = load_oracle()
    work = os.path.abspath(args.work)
    sandbox = oracle.Sandbox(work).prepare()

    case = oracle.Case(
        {
            "id": "fifo-hang",
            "class": "fifo-in-last-applications-dir",
            "env": {
                "XDG_CURRENT_DESKTOP": "Hyprland",
                "XDG_CONFIG_HOME": "$ROOT/home/.config",
                "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
                "XDG_DATA_HOME": "$ROOT/home/.local/share",
                "XDG_DATA_DIRS": "$ROOT/usr/share",
            },
            "files": {
                "home/.config/xdg-terminals.list": "ZzFifo.desktop\nAlacritty.desktop\n",
                "usr/share/applications/Alacritty.desktop":
                    "[Desktop Entry]\nType=Application\nName=Alacritty\n"
                    "Exec=alacritty\nCategories=System;TerminalEmulator;\n",
            },
            "exec": ["bin/alacritty"],
            "args": ["--print-id", "--print-path"],
        }
    )
    assert case.ok, case.errors
    root = os.path.join(work, case.id)
    oracle.materialize(case, root)
    fifo_dir = os.path.join(root, "home/.local/share/applications")
    os.makedirs(fifo_dir, exist_ok=True)
    fifo = os.path.join(fifo_dir, "ZzFifo.desktop")
    os.mkfifo(fifo)
    print("case root:   <WORK>/%s" % case.id)
    print("fifo:        <ROOT>/home/.local/share/applications/ZzFifo.desktop")
    print("argv shape:  find <DATA_DIRS apps>/. <DATA_HOME apps>/. -type f (...) -o (...)")
    print("timeout:     %ss" % args.timeout)
    record = oracle.run_once(sandbox, root, case, args.timeout)
    print("rc=%s timed_out=%s stub_ran=%s duration_ms=%s"
          % (record["rc"], record["timed_out"], record["stub_ran"], record["duration_ms"]))
    print("stdout=%r" % record["stdout"])
    print("stderr_bytes=%s" % record["stderr_bytes"])
    # precise residue check 1: if anything still holds the FIFO open for
    # reading, a non-blocking write-open succeeds; otherwise it is ENXIO.
    # Killing bwrap tears the pid namespace down asynchronously, so poll until
    # the reader disappears and record how long that took.
    import time
    reader = "PRESENT (a process still reads the FIFO)"
    settle_ms = None
    started = time.time()
    while True:
        try:
            fd = os.open(fifo, os.O_WRONLY | os.O_NONBLOCK)
            os.close(fd)
        except OSError as exc:
            reader = "ENXIO (errno %s): no reader left" % exc.errno
            settle_ms = int((time.time() - started) * 1000)
            break
        if time.time() - started >= args.settle:
            break
        time.sleep(0.05)
    print("fifo reader after the run: %s (settled in %s ms)" % (reader, settle_ms))
    # precise residue check 2: any process whose argv still names THIS case
    # root (the bwrap argv does; other seats' sandboxes use other roots).
    leaked = subprocess.run(
        ["pgrep", "-f", root],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
    )
    pids = [line for line in leaked.stdout.decode().split() if line.strip()]
    print("processes whose argv names this case root: %d" % len(pids))
    ok = (record["timed_out"] and record["rc"] == 124
          and reader.startswith("ENXIO") and not pids)
    print("FIFO_HANG_PROOF: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

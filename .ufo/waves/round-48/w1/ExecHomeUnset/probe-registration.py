#!/usr/bin/env python3
"""Probe 2: registration-level comparison for the loop / FIFO shapes.

For each case, the pin runs with XTE_DEBUG=1 (its own `debug` channel prints "registered '<path>' as entry '<id>'" and
the fallback adds), the tool runs `explain`. Both traces are root-normalized and only the registration/fallback lines
are kept, so the comparison is about which paths become ids - the question clause "symlink loops"/"FIFO" turns on.
"""
import os
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
sys.path.insert(0, os.path.join(LANE, ".ufo/waves/round-48/w1/ExecHomeUnset"))
import run as R  # noqa: E402

SCRATCH = "/fast/scratch/hyaku/mado-r48/ExecHomeUnset"
WANT = ["C5-fifo-later-dir-unused", "C8-symlink-loop", "C12-loop-desktop-symlink", "C13-subdir-cycle"]


def main():
    mod = R.load_counter()
    work = tempfile.mkdtemp(dir=SCRATCH, prefix="probe2-")
    box = mod.Box(work, tool_path=R.TOOL)
    out = []
    for case in [c for c in R.CASES if c["id"] in WANT]:
        rec = ["== %s" % case["id"]]
        for who in ("pin", "tool"):
            root = os.path.join(work, "r-%s-%s" % (case["id"], who))
            os.makedirs(root)
            R.materialize(root, case)
            env = R.case_env(case, root)
            if who == "pin":
                env["XTE_DEBUG"] = "1"
                args = ["--print-id"]
            else:
                args = ["explain"]
            argv = box.argv(root, env, who == "tool", args)
            try:
                p = subprocess.run(argv, capture_output=True, timeout=10, env={"PATH": "/usr/bin"})
                rc, so, se = p.returncode, p.stdout.decode(), p.stderr.decode()
            except subprocess.TimeoutExpired:
                rc, so, se = 124, "", ""
            keep = []
            for ln in (so + se).splitlines():
                n = ln.replace(root, "$ROOT")
                if ("registered" in n or "fallback" in n or "excluded" in n or "D: " in n
                        or "MADO_TERM:" in n or "list " in n):
                    keep.append(n.strip()[:160])
            rec.append("-- %s rc=%d" % (who, rc))
            rec += ["   " + k for k in keep]
        out.append("\n".join(rec))
    text = "\n".join(out) + "\n"
    open(os.path.join(R.SEAT, "registration-traces.txt"), "w").write(text)
    print(text)
    shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

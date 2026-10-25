#!/usr/bin/env python3
"""Deletion check for the round-37 claims at one revision (read-only on the lane).

Clones --repo into /dev/shm, and in three sandbox commits scores both frozen counters:
as-is, with C2's files deleted, and with C1's target entries + round-37 lesson deleted.
Also lists every round-37 Gate receipt path outside .ufo/waves/round-37/fetch/.
SEPARABLE when neither counter's verdict moves on the other side's deletion and no Gate
receipt leaves fetch/; exit 0 SEPARABLE, 1 COUPLED, 2 setup.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
C1 = os.path.join(LANE, "quality/counters/c1-r37-event-ground.py")
C2 = os.path.join(LANE, "quality/counters/c2-r37-eventq.py")
C2_FILES = ["tools/mado-eventq.py", ".ufo/waves/round-37/receipts/eventq-live.txt",
            ".ufo/waves/round-37/receipts/eventq-live-ss.txt"]
C1_FILES = ["corpus/knowledge/event-delivery-limits-r26.md",
            "corpus/knowledge/event-queue-observability-r37.md", "corpus/lessons/round-37.md"]
FETCH = ".ufo/waves/round-37/fetch/"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ENV.update(GIT_AUTHOR_NAME="sandbox", GIT_AUTHOR_EMAIL="sandbox@invalid",
           GIT_COMMITTER_NAME="sandbox", GIT_COMMITTER_EMAIL="sandbox@invalid")


def sh(*cmd):
    return subprocess.run(cmd, env=ENV, capture_output=True, text=True)


def verdicts(sb):
    out = {}
    for name, counter in (("C1", C1), ("C2", C2)):
        p = subprocess.run([sys.executable, "-I", counter, "--repo", sb, "--rev", "HEAD"],
                           env=ENV, capture_output=True, text=True)
        last = (p.stdout.strip().splitlines() or [""])[-1]
        out[name] = (p.returncode, re.sub(r" rev=\S+| base=\S+", "", last))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=LANE)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    root = tempfile.mkdtemp(prefix="mado37-sepcheck-", dir="/dev/shm")
    sb = os.path.join(root, "sb")
    try:
        if sh("git", "clone", "-q", "--no-local", a.repo, sb).returncode or \
                sh("git", "-C", sb, "checkout", "-q", "--detach", a.rev).returncode:
            print("SEPCHECK SETUP clone/checkout failed")
            return 2
        lesson = os.path.join(sb, "corpus/lessons/round-37.md")
        stray = []
        if os.path.exists(lesson):
            for line in open(lesson, errors="replace"):
                m = re.match(r"^GATE (S\d+) receipt=(\S+) ", line.strip())
                if m and not m.group(2).startswith(FETCH):
                    stray.append(f"{m.group(1)}:{m.group(2)}")
        rows = {"as-is": verdicts(sb)}
        for label, files in (("minus-c2", C2_FILES), ("minus-c1", C1_FILES)):
            sh("git", "-C", sb, "checkout", "-q", "--detach", a.rev)
            sh("git", "-C", sb, "rm", "-q", "--ignore-unmatch", "--", *files)
            sh("git", "-C", sb, "commit", "-q", "--allow-empty", "-m", f"sepcheck {label}")
            rows[label] = verdicts(sb)
        for label, v in rows.items():
            for name, (rc, line) in v.items():
                print(f"SEPCHECK {label} {name} rc={rc} :: {line}")
        c1_moved = rows["as-is"]["C1"] != rows["minus-c2"]["C1"]
        c2_moved = rows["as-is"]["C2"] != rows["minus-c1"]["C2"]
        verdict = "COUPLED" if (c1_moved or c2_moved or stray) else "SEPARABLE"
        print(f"SEPCHECK rev={a.rev} c1_moves_without_c2={int(c1_moved)} c2_moves_without_c1={int(c2_moved)} "
              f"gate_receipts_outside_fetch={','.join(stray) or '-'} verdict={verdict}")
        return 0 if verdict == "SEPARABLE" else 1
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

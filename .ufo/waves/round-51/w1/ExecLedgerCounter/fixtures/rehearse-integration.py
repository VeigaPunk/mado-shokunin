#!/usr/bin/env python3
"""Integration rehearsal for PRED-C1-r51: the real gate, the real ledger, the real counter.

Builds a scratch clone of the lane at the claims revision `d2740281` and commits the three
round-51 drafts at their tracked paths, then measures twice:

``stage-a``  gate + ledger + counter land exactly as the seats drafted them. The ledger carries
             79 base rows, the population is 81 (the two new instruments), so the counter must
             print `uncovered=2 … checker=failed verdict=TARGET_MISSED` and exit 1. This is the
             defect the ledger draft itself names ("two rows are owed at the data revision").
``stage-b``  the two owed rows are appended (pointer = the committing seat's report, which the
             integrator commits at the same tip) and the seat reports are committed beside them.
             The counter must then print the frozen MET line and exit 0 with the real gate's
             `LEDGER:` line agreeing field for field.

Nothing is written to the lane: the clone lives under `--scratch` and every commit is asserted
to happen in that clone (`git rev-parse --show-toplevel`).

Usage:
  python3 rehearse-integration.py [--scratch DIR] [--lane DIR] [--claims-rev REV]
"""

import argparse
import os
import shutil
import subprocess
import sys

CLAIMS_REV = "d274028163033244bd78938ad152dc250cc50480"
ROWS = (
    "| `quality/check-tool-ledger.py` | Gate over the instrument population: every file under "
    "`tools/`, `quality/*.py` and `quality/counters/*.py` at the revision has exactly one ledger "
    "row with a description and a resolving accountability pointer; hermetic `--selftest`. | "
    "`.ufo/waves/round-51/w1/ExecLedgerGate.md` |",
    "| `quality/counters/c1-r51-ledger.py` | PRED-C1-r51 counter: clones the lane at the measured "
    "revision, recomputes the population and the ledger fields independently, and requires the "
    "gate's `LEDGER:` line and `--selftest` to agree. | "
    "`.ufo/waves/round-51/w1/ExecLedgerCounter.md` |",
)

# The owed rows can point at `claims.md` (committed at the claims revision, which names both new
# instruments at lines 20-21) instead of at the seat reports. Stage-c measures that variant with
# no round-51 seat report committed at all, so the freeze does not need to depend on them.
ROWS_CLAIMS = (
    "| `quality/check-tool-ledger.py` | Gate over the instrument population: every file under "
    "`tools/`, `quality/*.py` and `quality/counters/*.py` at the revision has exactly one ledger "
    "row with a description and a resolving accountability pointer; hermetic `--selftest`. | "
    "`.ufo/waves/round-51/claims.md:20` |",
    "| `quality/counters/c1-r51-ledger.py` | PRED-C1-r51 counter: clones the lane at the measured "
    "revision, recomputes the population and the ledger fields independently, and requires the "
    "gate's `LEDGER:` line and `--selftest` to agree. | "
    "`.ufo/waves/round-51/claims.md:21` |",
)


def run(args, cwd=None, check=True):
    proc = subprocess.run(args, capture_output=True, text=True, cwd=cwd)
    if check and proc.returncode != 0:
        sys.exit("FAILED %s rc=%d\n%s\n%s" % (" ".join(args), proc.returncode,
                                              proc.stdout, proc.stderr))
    return proc


def git(repo, *args):
    return run(("git", "-C", repo) + args).stdout.strip()


def commit(repo, message):
    git(repo, "add", "-A")
    git(repo, "-c", "user.name=rehearsal", "-c", "user.email=rehearsal@mado.local",
        "commit", "-q", "-m", message)
    return git(repo, "rev-parse", "HEAD")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", default=os.environ.get("TMPDIR"))
    ap.add_argument("--lane", default="/home/vgpnk/Projects/shokunin/mado-shokunin")
    ap.add_argument("--claims-rev", default=CLAIMS_REV)
    args = ap.parse_args(argv)

    lane = os.path.abspath(args.lane)
    seats = os.path.join(lane, ".ufo/waves/round-51/w1")
    scratch = os.path.abspath(args.scratch or subprocess.run(
        [sys.executable, "-c", "import tempfile;print(tempfile.gettempdir())"],
        capture_output=True, text=True).stdout.strip())
    root = os.path.join(scratch, "ri")
    if os.path.exists(root):
        shutil.rmtree(root)
    os.makedirs(root)
    repo = os.path.join(root, "repo")
    run(["git", "clone", "-q", "--shared", lane, repo, "--no-checkout"])
    git(repo, "checkout", "-q", "--detach", args.claims_rev)
    top = git(repo, "rev-parse", "--show-toplevel")
    assert os.path.realpath(top) == os.path.realpath(repo), (top, repo)
    print("rehearsal repo=%s toplevel=%s" % (repo, top))

    copies = (
        (os.path.join(seats, "ExecLedgerGate/check-tool-ledger.py"),
         "quality/check-tool-ledger.py"),
        (os.path.join(seats, "ExecLedgerPopulation/tool-ledger.md"), "quality/tool-ledger.md"),
        (os.path.join(seats, "ExecLedgerCounter/c1-r51-ledger.py"),
         "quality/counters/c1-r51-ledger.py"),
    )
    for src, rel in copies:
        dst = os.path.join(repo, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        print("copied %s <- %s" % (rel, os.path.relpath(src, seats)))
    rev_a = commit(repo, "rehearsal stage-a: r51 drafts at their tracked paths")

    checker = os.path.join(repo, "quality/check-tool-ledger.py")
    counter = os.path.join(repo, "quality/counters/c1-r51-ledger.py")

    def measure(rev, title):
        print("\n== %s rev=%s" % (title, rev))
        proc = run(["python3", "-I", checker, "--repo", repo, "--rev", rev], check=False)
        tail = [l for l in proc.stdout.splitlines() if l.startswith("LEDGER")]
        for line in tail[-3:]:
            print("gate:   %s" % line)
        print("gate:   exit=%d" % proc.returncode)
        proc = run([sys.executable, "-I", counter, "--repo", repo, "--rev", rev,
                    "--work", os.path.join(root, "work")], check=False)
        for line in (proc.stdout + proc.stderr).strip().splitlines():
            print("counter: %s" % line)
        print("counter: exit=%d" % proc.returncode)
        return proc.returncode

    rc_a = measure(rev_a, "stage-a: drafts only")

    ledger = os.path.join(repo, "quality/tool-ledger.md")
    with open(ledger, "a") as handle:
        handle.write("\n".join(ROWS) + "\n")
    wave_dir = os.path.join(repo, ".ufo/waves/round-51/w1")
    os.makedirs(wave_dir, exist_ok=True)
    for name in ("ExecLedgerGate.md", "ExecLedgerCounter.md", "ExecLedgerPopulation.md"):
        src = os.path.join(seats, name)
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(wave_dir, name))
    rev_b = commit(repo, "rehearsal stage-b: owed rows for the two new instruments")
    rc_b = measure(rev_b, "stage-b: owed rows added, seat reports committed")

    shutil.copyfile(os.path.join(seats, "ExecLedgerPopulation/tool-ledger.md"), ledger)
    with open(ledger, "a") as handle:
        handle.write("\n".join(ROWS_CLAIMS) + "\n")
    for name in ("ExecLedgerGate.md", "ExecLedgerCounter.md", "ExecLedgerPopulation.md"):
        path = os.path.join(wave_dir, name)
        if os.path.exists(path):
            os.remove(path)
    rev_c = commit(repo, "rehearsal stage-c: owed rows point at claims.md, no seat report present")
    rc_c = measure(rev_c, "stage-c: owed rows point at claims.md, no round-51 seat report")

    print("\nsummary: stage-a exit=%d (expect 1) stage-b exit=%d (expect 0) stage-c exit=%d "
          "(expect 0)" % (rc_a, rc_b, rc_c))
    print("revs: stage-a=%s stage-b=%s stage-c=%s" % (rev_a, rev_b, rev_c))
    return 0 if (rc_a == 1 and rc_b == 0 and rc_c == 0) else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Run MutC2Drop matrix: baseline + 24 mutants x 18 fixtures.

Emits matrix.tsv: mutant fixture rc verdict_or_crash detail.
Run: python3 run_matrix.py
"""
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
SCRATCH = REPO / ".ufo/waves/round-35/scratch/MutC2Drop"
FIX = SCRATCH / "fixtures"
P = ".ufo/waves/round-35/scratch/MutC2Drop/fixtures"

BASE = REPO / ".ufo/waves/round-35/c2/count.py"

FIXTURES = [
    ("f00-golden", f"{P}/f00-golden/frozen.json"),
    ("f01-donothing", f"{P}/f01-donothing/frozen.json"),
    ("f02-missing-receipt", f"{P}/f02-missing-receipt/frozen.json"),
    ("f03-clean-receipt", f"{P}/f03-clean-receipt/frozen.json"),
    ("f04-retired-also-live", f"{P}/f04-retired-also-live/frozen.json"),
    ("f05-retired-empty", f"{P}/f05-retired-empty/frozen.json"),
    ("f06-declared-extra", f"{P}/f06-declared-extra/frozen.json"),
    ("f07-nl-no-reason-bare", f"{P}/f07-nl-no-reason-bare/frozen.json"),
    ("f08-nl-no-reason-with-control", f"{P}/f08-nl-no-reason-with-control/frozen.json"),
    ("f09-blobledger-absent", f"{P}/f09-blobledger-absent/frozen.json"),
    ("f10-tip-absent", f"{P}/f10-tip-absent/frozen.json"),
    ("f11-blob-id-wrong", f"{P}/f11-blob-id-wrong/frozen.json"),
    ("f12-blob-path-missing", f"{P}/f12-blob-path-missing/frozen.json"),
    ("f13-predicate-drift", f"{P}/f13-predicate-drift/frozen.json"),
    ("f14-target-drift", f"{P}/f14-target-drift/frozen.json"),
    ("f15-frozen-absent", f"{P}/f15-frozen-absent/no-such-frozen.json"),
    ("f16-ledger-absent", f"{P}/f16-ledger-absent/frozen.json"),
    ("f17-declared-other", f"{P}/f17-declared-other/frozen.json"),
    ("f18-retired-key-absent", f"{P}/f18-retired-key-absent/frozen.json"),
]

PROGS = [("base", BASE)] + sorted(
    (p.stem, p) for p in (SCRATCH / "mutants").glob("m*.py"))


def run(prog: Path, frozen_rel: str):
    r = subprocess.run(
        ["python3", "-I", str(prog), "--repo", str(REPO), "--frozen", frozen_rel],
        capture_output=True, text=True, cwd=REPO)
    verdict = "?"
    for tok in ("verdict=TARGET_MET", "verdict=TARGET_MISSED"):
        if tok in r.stdout:
            verdict = tok.split("=")[1]
    detail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
    if r.returncode not in (0, 1) or not detail:
        # die() message or crash traceback
        err = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "(no output)"
        detail = "STDERR: " + err
    return r.returncode, verdict, detail


def main():
    out = SCRATCH / "matrix.tsv"
    lines = ["mutant\tfixture\trc\tverdict\tdetail"]
    for pname, prog in PROGS:
        for fname, frel in FIXTURES:
            rc, verdict, detail = run(prog, frel)
            lines.append(f"{pname}\t{fname}\t{rc}\t{verdict}\t{detail}")
    out.write_text("\n".join(lines) + "\n")
    print(f"{len(lines)-1} runs -> {out}")


if __name__ == "__main__":
    main()

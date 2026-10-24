#!/usr/bin/env python3
"""PRED-C2-r33-v1 counter. Exit 0 TARGET_MET, 1 TARGET_MISSED, 2 usage.

PRED-C2-r33-v1: TARGET_MET iff the last line matching r33-claim-verdict: r32-C1 cited_entries=<N> verdict=<V> rev=<H> has N equal to the frozen r32 counter's cited_entries on rev H, V equal to honest-stop, and H equal to d9ed38166cc3be8ef4c52b41d66ad94010feb047.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

PREDICATE = (
    "PRED-C2-r33-v1: TARGET_MET iff the last line matching "
    "r33-claim-verdict: r32-C1 cited_entries=<N> verdict=<V> rev=<H> has N equal to the "
    "frozen r32 counter's cited_entries on rev H, V equal to honest-stop, and H equal to "
    "d9ed38166cc3be8ef4c52b41d66ad94010feb047."
)
FROZEN_REV = "d9ed38166cc3be8ef4c52b41d66ad94010feb047"
LINE_RE = re.compile(
    r"^r33-claim-verdict: r32-C1 cited_entries=(\d+) verdict=(\S+) rev=([0-9a-f]{40})$"
)
# Frozen r32 C1 counter, verbatim from registration.md. Not this round's rule.
R32_COUNTER = r"""
A=corpus/knowledge/ipc-contract-r25.md
B=corpus/knowledge/dispatcher-semantics-r25.md
C=corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md
e=0; for f in "$A" "$B" "$C"; do [ -f "$f" ] && e=$((e+1)); done
r=$(grep -cE '^\|[[:space:]]*S(186|187|188|189|196)[[:space:]]*\|' corpus/SOURCES.md || true)
c=$(grep -cE '^source:.*S(186|187|188|189|196)' "$A" "$B" "$C" 2>/dev/null | awk -F: '{s+=$2} END{print s+0}')
echo "entries=$e rows=$r cited_entries=$c"
"""


def die(msg: str) -> None:
    print(f"PRED-C2-r33-v1 error={msg}", file=sys.stderr)
    raise SystemExit(2)


def r32_cited(repo: Path, rev: str) -> int:
    with tempfile.TemporaryDirectory(prefix="mado-r33-c2-") as tmp:
        archive = subprocess.run(
            ["git", "-C", str(repo), "archive", rev, "corpus"],
            check=False, capture_output=True,
        )
        if archive.returncode != 0:
            die("archive-failed")
        extract = subprocess.run(["tar", "-x", "-C", tmp], input=archive.stdout, check=False)
        if extract.returncode != 0:
            die("extract-failed")
        ran = subprocess.run(
            ["bash", "-c", R32_COUNTER], cwd=tmp, check=False, capture_output=True, text=True,
        )
        if ran.returncode != 0:
            die("r32-counter-failed")
        m = re.search(r"cited_entries=(\d+)", ran.stdout)
        if not m:
            die("r32-counter-unparsed")
        return int(m.group(1))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--scorecard", required=True, help="SCORECARD path to read; not rewritten")
    args = ap.parse_args()
    card = Path(args.scorecard)
    if not card.is_file():
        die("scorecard-missing")
    last = None
    for line in card.read_text().splitlines():
        m = LINE_RE.match(line)
        if m:
            last = m
    if last is None:
        print("PRED-C2-r33-v1 claim_mismatch=1 reason=absent verdict=TARGET_MISSED")
        raise SystemExit(1)
    n, verdict, rev = int(last.group(1)), last.group(2), last.group(3)
    measured = r32_cited(Path(args.repo), rev)
    ok = n == measured and verdict == "honest-stop" and rev == FROZEN_REV
    reason = "match" if ok else "mismatch"
    word = "TARGET_MET" if ok else "TARGET_MISSED"
    print(
        f"PRED-C2-r33-v1 claim_mismatch={0 if ok else 1} reason={reason} "
        f"published={n} measured={measured} verdict_word={verdict} rev={rev} verdict={word}"
    )
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()

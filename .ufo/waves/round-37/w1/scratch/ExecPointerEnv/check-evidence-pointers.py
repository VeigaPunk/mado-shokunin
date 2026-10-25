#!/usr/bin/env python3
"""mado — evidence-pointer durability gate: does every pointer in the lane's own records resolve?

Round 35 closed with routed record defects: a `LOG.md` entry citing two paths that
do not exist at the tip (D5), a "no scratch tree left" claim contradicted by 124
tracked paths (D8), ten round-35 paths still uncommitted at closure (D2), and no
committed transcript of the axis gate at the tip revision (D10). This gate turns
those into one re-runnable verdict. Each observable counts committed bytes; none
of them is a token grep that a prose edit can satisfy.

PRED-PTR-r36-v1: TARGET_MET iff
  dangling_r35_closed   every lane-relative evidence pointer cited by the round-35
                        `LOG.md` entry and `SCORECARD.md` sections that does not
                        resolve at the checked revision appears as the `old` side of
                        a round-36 correction pair in `LOG.md` whose `new` side
                        resolves, and the round-35 record still carries the two
                        pointers the round-35 spot-check found dangling
                        (rewriting the record is not a repair);
  dangling_r36 == 0     the same pointer class, cited by the round-36 `LOG.md`
                        entry, `SCORECARD.md` sections and `corpus/lessons/round-36.md`,
                        except pointers written as the `old` side of a correction
                        pair — a superseded pointer is named, not cited;
  inherited_dirty == 0  the ten round-35 closure paths `git status --porcelain` reports;
  scratch_disposition_ok the round-36 lesson names a disposition for
                        `.ufo/waves/round-35/scratch` with a `tracked paths=N` count
                        equal to the tracked path count at the revision;
  tip_axis_transcript == 1  a committed `quality/receipts/axis-<40hex>.txt` exists,
                        `<40hex>` is an ancestor of the branch, and its `MADO_AXIS:`
                        line reads `mismatched=0 rev=<40hex>`.

Absence is never a pass: missing round-36 sections print `setup=missing-r36-sections`,
force `TARGET_MISSED` and exit 1 — the other observables are still printed, so the
before-state is readable and the same command measures both sides.

Usage: check-evidence-pointers.py [--repo .] [--rev master] [--branch master]
Exit 0 = TARGET_MET, 1 = TARGET_MISSED, 2 = setup error.
"""
from __future__ import annotations

import argparse
import fnmatch
import os
import re
import subprocess
import sys
from pathlib import Path

PTR = re.compile(r"`([^`\n]+)`")
PATHY = re.compile(r"^(?:\.ufo|corpus|quality|tools|scripts|considerthese)/[^\s]*$")
PAIR = re.compile(r"^\s*-\s*`([^`]+)`\s*->\s*`([^`]+)`\s*$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
DISPOSITION = re.compile(r"tracked paths=(\d+)")
SUPERSEDED_POINTERS = (
    ".ufo/waves/round-35/scratch/SimplifyCounter/",
    ".ufo/waves/round-35/scratch/MutC1Drop/mutants/",
)
INHERITED_PATHS = (
    ".ufo/waves/round-35/scratch-evidence/RevEntryR12/evidence.txt",
    ".ufo/waves/round-35/w2/reports/RevC1Tip.md",
    ".ufo/waves/round-35/w2/reports/RevEntryR12.md",
    ".ufo/waves/round-35/w2/reports/RevEntryR14.md",
    ".ufo/waves/round-35/w2/reports/RevQuoteS203.md",
    ".ufo/waves/round-35/w2/reports/RevQuoteS204.md",
    ".ufo/waves/round-35/w2/reports/RevQuoteS205.md",
    ".ufo/waves/round-35/w2/reports/SimplifyRows.md",
    ".ufo/waves/round-35/scratch/RevQuoteS203/",
    ".ufo/waves/round-35/scratch/RevQuoteS205/",
)
# `git -C <repo>` does not override an inherited GIT_DIR / GIT_WORK_TREE, so every git
# call runs without the caller's GIT_* variables.
GIT_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def die(msg: str) -> None:
    print(f"PRED-PTR-r36-v1 error={msg}", file=sys.stderr)
    raise SystemExit(2)


def git(repo: Path, *args: str) -> str:
    proc = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                          env=GIT_ENV)
    if proc.returncode != 0:
        return ""
    return proc.stdout


def pointerish(token: str) -> bool:
    if not PATHY.match(token) or " " in token:
        return False
    if token.endswith("/") or "*" in token:
        return True
    return "." in token.rsplit("/", 1)[-1]


def pointers(text: str) -> list[str]:
    out = []
    for token in PTR.findall(text):
        if pointerish(token) and token not in out:
            out.append(token)
    return out


def sections(text: str, needle: str) -> str:
    out, keep = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            keep = needle.lower() in line.lower()
            continue
        if keep:
            out.append(line)
    return "\n".join(out)


def resolves(pointer: str, files: set[str]) -> bool:
    if pointer.endswith("/"):
        return any(f.startswith(pointer) for f in files)
    if "*" in pointer:
        return any(fnmatch.fnmatch(f, pointer) for f in files)
    return pointer in files


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", default="master")
    ap.add_argument("--branch", default="master")
    args = ap.parse_args()
    repo = Path(args.repo).resolve()
    rev = args.rev

    listing = git(repo, "ls-tree", "-r", "--name-only", rev)
    if not listing.strip():
        die(f"revision-not-readable:{rev}")
    files = set(listing.splitlines())

    def show(path: str) -> str:
        return git(repo, "show", f"{rev}:{path}")

    log = show("LOG.md")
    scorecard = show("SCORECARD.md")
    lesson = show("corpus/lessons/round-36.md")
    setup_ok = bool(
        sections(log, "Round 36").strip()
        and sections(scorecard, "Round 36").strip()
        and lesson.strip()
    )

    log35 = sections(log, "Round 35")
    sc35 = sections(scorecard, "Round 35")
    log36 = sections(log, "Round 36")
    sc36 = sections(scorecard, "Round 36")
    ptr35 = pointers(log35) + [p for p in pointers(sc35) if p not in pointers(log35)]
    ptr36 = pointers(log36) + [p for p in pointers(sc36) if p not in pointers(log36)]
    ptr36 += [p for p in pointers(lesson) if p not in ptr36]

    # A pair counts only when its replacement is itself a pointer-shaped path that
    # resolves: `- `ghost.md` -> `LOG.md`` must not launder a dangling citation.
    pairs = [(m.group(1).strip(), m.group(2).strip())
             for m in (PAIR.match(ln) for ln in log36.splitlines())
             if m and pointerish(m.group(2).strip()) and resolves(m.group(2).strip(), files)]
    dangling35 = [p for p in ptr35 if not resolves(p, files)]
    superseded_old = {o for o, _ in pairs}
    dangling36 = [p for p in ptr36 if not resolves(p, files) and p not in superseded_old]

    record_intact = all(p in ptr35 for p in SUPERSEDED_POINTERS)
    closed = 0
    for old in dangling35:
        if any(old == o for o, _ in pairs):
            closed += 1
    # Closure is owed even when the two pointers happen to resolve at the checked
    # revision: restoring the tree is not the same act as naming the supersession.
    named = sum(1 for p in SUPERSEDED_POINTERS if any(p == o for o, _ in pairs))
    dangling35_closed = 1 if (record_intact and named == len(SUPERSEDED_POINTERS)
                              and closed == len(dangling35)) else 0

    status_out = git(repo, "status", "--porcelain", "--", *INHERITED_PATHS)
    status_rc = subprocess.run(["git", "-C", str(repo), "status", "--porcelain", "--",
                                *INHERITED_PATHS], capture_output=True, text=True,
                               env=GIT_ENV).returncode
    if status_rc != 0:
        # "unmeasurable" must never read as "clean": a bare clone or a broken work tree
        # cannot answer the question, so the observable fails closed.
        print(f"PRED-PTR-r36-v1 error=git-status-unusable rc={status_rc} verdict=TARGET_MISSED")
        raise SystemExit(1)
    dirty = [ln for ln in status_out.splitlines() if ln.strip()]
    inherited_dirty = len(dirty)

    scratch_count = len([f for f in files if f.startswith(".ufo/waves/round-35/scratch/")])
    scratch_disposition_ok = 0
    for line in lesson.splitlines():
        if ".ufo/waves/round-35/scratch" in line:
            m = DISPOSITION.search(line)
            if not m or int(m.group(1)) != scratch_count:
                continue
            # A negated sentence ("NOT retained") is not a disposition: the keyword
            # must stand on its own within the line.
            low = line.lower()
            if re.search(r"\b(not|never|no longer)\b[^.]{0,40}\b(retain\w*|kept|keep|deleted|removed)\b", low):
                continue
            if re.search(r"\b(retained|retain|deleted|removed|kept)\b", low):
                scratch_disposition_ok = 1
                break

    tip_axis_transcript = 0
    tip_detail = "none"
    for name in sorted(f for f in files if f.startswith("quality/receipts/axis-") and f.endswith(".txt")):
        candidate = name[len("quality/receipts/axis-"):-len(".txt")]
        if not HEX40.match(candidate):
            continue
        if subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor",
                           candidate, args.branch], env=GIT_ENV).returncode != 0:
            continue
        text = show(name)
        for line in text.splitlines():
            if line.startswith("MADO_AXIS:") and "mismatched=0" in line and f"rev={candidate}" in line:
                tip_axis_transcript = 1
                tip_detail = f"{name}@{candidate}"
                break
        if tip_axis_transcript:
            break

    met = (
        setup_ok
        and dangling35_closed == 1
        and len(dangling36) == 0
        and inherited_dirty == 0
        and scratch_disposition_ok == 1
        and tip_axis_transcript == 1
    )
    print(
        f"PRED-PTR-r36-v1 rev={rev} pointers_r35={len(ptr35)} dangling_r35={len(dangling35)} "
        f"dangling_r35_closed={dangling35_closed} pointers_r36={len(ptr36)} "
        f"dangling_r36={len(dangling36)} inherited_dirty={inherited_dirty} "
        f"scratch_tracked={scratch_count} scratch_disposition_ok={scratch_disposition_ok} "
        f"tip_axis_transcript={tip_axis_transcript} setup={'ok' if setup_ok else 'missing-r36-sections'} "
        f"verdict={'TARGET_MET' if met else 'TARGET_MISSED'}"
    )
    for p in dangling35:
        print(f"dangling_r35: {p}")
    for p in dangling36:
        print(f"dangling_r36: {p}")
    for ln in dirty:
        print(f"dirty: {ln}")
    print(f"tip_axis: {tip_detail}")
    raise SystemExit(0 if met else 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Reproduce ScrRowsPlaced's registry check for rows S352-S363 at a scored revision.

Read-only: reads blobs through `git -C <clone> cat-file`, writes nothing.

  python3 -I verify_rows.py --repo <clone> --rev <rev>

Prints, per check (a)-(e): PASS/FAIL plus the evidence line, then exits 0 iff every
hard check passes (the generator-hash mismatch is reported as FINDING, exit 3).
"""
import argparse
import hashlib
import re
import subprocess
import sys

IDS = [f"S{i}" for i in range(352, 364)]
PIN_RE = re.compile(r"pin (\.ufo/\S+?)(?: (\d+) B(?: (\d+) lines)?)? sha256:([0-9a-f]{64})")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True)


def blob(repo, rev, path):
    r = git(repo, "cat-file", "blob", f"{rev}:{path}")
    return None if r.returncode else r.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    rev, repo = a.rev, a.repo
    fails, findings = [], []

    src = blob(repo, rev, "corpus/SOURCES.md")
    if src is None:
        sys.exit(f"missing corpus/SOURCES.md at {rev}")
    text = src.decode()
    lines = text.split("\n")
    print(f"rev {rev}  corpus/SOURCES.md sha256 {hashlib.sha256(src).hexdigest()}")

    # (a) section placement
    sec = {l: i for i, l in enumerate(lines, 1) if l.startswith("## ")}
    reg = next(i for l, i in sec.items() if l == "## Registry")
    paths = next(i for l, i in sec.items() if l == "## Paths")
    rowline = {}
    for i, l in enumerate(lines, 1):
        m = re.match(r"^\| (S\d{3,}) \|", l)
        if m:
            rowline[m.group(1)] = i
    inside = all(reg < rowline[k] < paths for k in IDS)
    print(f"(a) registry section lines {reg}..{paths-1}; rows {min(rowline[k] for k in IDS)}.."
          f"{max(rowline[k] for k in IDS)} -> {'PASS' if inside else 'FAIL'}")
    if not inside:
        fails.append("(a) rows outside ## Registry")
    outside = [i for i, l in enumerate(lines, 1)
               if re.match(r"^\| *S\d{3,} *\|", l) and not (reg < i < paths)]
    print(f"(a2) row-shaped lines outside Registry: {outside or 'none'}")

    rows = {}
    for k in IDS:
        rows[k] = [c.strip() for c in lines[rowline[k] - 1].split("|")[1:-1]]

    # (b) 11 cells, no literal pipe inside a cell, no tabs
    ok_b = True
    for k in IDS:
        raw = lines[rowline[k] - 1]
        if len(raw.split("|")) != 13 or "\t" in raw or "\\|" in raw:
            ok_b = False
            fails.append(f"(b) {k} cell shape: pipes={len(raw.split('|'))}")
    print(f"(b) 11 cells/row, no embedded pipe/tab: {'PASS' if ok_b else 'FAIL'}")

    # (c) pin path exists, size/lines/sha256 match pin bytes
    ok_c = True
    for k in IDS:
        anchor = rows[k][5]
        pins = PIN_RE.findall(anchor)
        if k == "S361":  # this row states size+sha before the path, path in parentheses
            m = re.search(r"sha256:([0-9a-f]{64})", anchor)
            pins = [(".ufo/waves/round-50/fetch/binds-live-r50.txt", "1768", "", m.group(1))]
        if not pins:
            ok_c = False
            fails.append(f"(c) {k} no pin parsed")
            continue
        for path, size, nlines, sha in pins:
            b = blob(repo, rev, path)
            if b is None:
                ok_c = False
                fails.append(f"(c) {k} pin missing at rev: {path}")
                print(f"    {k} MISSING {path}")
                continue
            h, nb, nl = hashlib.sha256(b).hexdigest(), len(b), b.count(b"\n")
            good = h == sha and (not size or int(size) == nb) and (not nlines or int(nlines) == nl)
            print(f"    {k} {path.split('/')[-1]} bytes={nb} lines={nl} sha={'ok' if h == sha else 'MISMATCH'} "
                  f"{'PASS' if good else 'FAIL'}")
            ok_c &= good
            if not good:
                fails.append(f"(c) {k} pin {path} hash/size/line mismatch")
    print(f"(c) pin paths exist and hashes match: {'PASS' if ok_c else 'FAIL'}")

    # (c2) auxiliary locator hashes quoted in a cell
    gen = re.search(r"generator (\S+) sha256:([0-9a-f]{64})", rows["S361"][5])
    if gen:
        b = blob(repo, rev, gen.group(1))
        h = hashlib.sha256(b).hexdigest() if b is not None else "MISSING"
        if h != gen.group(2):
            findings.append(f"S361 generator hash: cell says {gen.group(2)}, committed bytes are {h} ({gen.group(1)})")
            print(f"(c2) FINDING S361 generator {gen.group(1)} claims {gen.group(2)} actual {h}")
        else:
            print("(c2) S361 generator hash matches")

    # (d) opened ISO date, recheck NNd / on-*
    ok_d = True
    for k in IDS:
        opened, recheck = rows[k][8], rows[k][9]
        shape = re.fullmatch(r"\d{2}d", recheck) or recheck.startswith("on-") \
            or re.fullmatch(r"\d{4}-\d{2}-\d{2}", recheck)
        if not (re.fullmatch(r"\d{4}-\d{2}-\d{2}", opened) and shape):
            ok_d = False
            fails.append(f"(d) {k} opened={opened} recheck={recheck}")
    print(f"(d) opened ISO, recheck NNd|on-*|ISO: {'PASS' if ok_d else 'FAIL'}")

    # (e) used-by targets exist
    ok_e = True
    for k in IDS:
        target = rows[k][10]
        if blob(repo, rev, target) is None:
            ok_e = False
            fails.append(f"(e) {k} used-by missing: {target}")
        else:
            print(f"    {k} used-by {target} exists")
    print(f"(e) used-by targets exist: {'PASS' if ok_e else 'FAIL'}")

    for f in findings:
        print(f"FINDING {f}")
    if fails:
        for f in fails:
            print(f"FAIL {f}")
        return 1
    return 3 if findings else 0


if __name__ == "__main__":
    sys.exit(main())

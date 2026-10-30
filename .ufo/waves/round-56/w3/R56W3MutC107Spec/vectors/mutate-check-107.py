#!/usr/bin/env python3
"""Mutation battery for the criterion-107 acceptance vectors.

Purpose: prove the vector set has teeth.  Each mutant is ONE plausible defect
in the spec-literal oracle (reference-check-107.py); the bounded behavioural
detector is the vector suite itself (run the oracle on each fixture repo and
compare against the expected stdout/rc).  A mutant is KILLED when at least one
vector's expectation fails; it SURVIVES when every vector still passes.

The pristine master is never modified: mutants are patched copies under the
scratch dir, and each copy's sha256 is recorded before the patch, after the
patch and after the restore.

Usage:
  python3 -I mutate-check-107.py --oracle <path> --fixtures <dir> \
      --vectors <dest-dir> --scratch <dir>
"""

import argparse
import hashlib
import os
import shutil
import subprocess
import sys

# (mutant id, description, (old, new) patch applied to the oracle source)
MUTANTS = [
    ("M01-boundary-any-prefix",
     "occurrence counting ignores the character before NAME:",
     ('                if prev is None or prev not in WORD:\n',
      '                if True:\n')),
    ("M02-boundary-hyphen-slash",
     "hyphen/slash before NAME: treated as an identifier char",
     ('                if prev is None or prev not in WORD:\n',
      '                if prev is None or (prev not in WORD and prev not in "-/"):\n')),
    ("M03-reversed-range-covers",
     "reversed range M<N treated as covering",
     ('            covered_here = any(\n'
      '                hi >= n and n <= line_no <= hi for n, hi in flat\n'
      '            )\n',
      '            covered_here = any(\n'
      '                n <= line_no <= max(n, hi) for n, hi in flat\n'
      '            )\n')),
    ("M04-eof-not-checked",
     "length bound (past-eof) not applied",
     ('                past = any(max(n, hi) > pieces for n, hi in flat)\n',
      '                past = False\n')),
    ("M05-eof-covering-locator-only",
     "length bound applied only to the locator that covers the row",
     ('                past = any(max(n, hi) > pieces for n, hi in flat)\n',
      '                past = any(\n'
      '                    max(n, hi) > pieces\n'
      '                    for n, hi in flat\n'
      '                    if n <= line_no <= hi\n'
      '                )\n')),
    ("M06-comma-space-not-allowed",
     "the one optional space after a comma is not allowed",
     ('            if j < len(text) and text[j] == " ":\n'
      '                j += 1\n',
      '')),
    ("M07-malformed-range-allowed",
     "a range in the entry's pin cell is accepted as a pin",
     ('PIN_CELL_RE = re.compile(r"^([^:\\s]+):(\\d+)$")\n',
      'PIN_CELL_RE = re.compile(r"^([^:\\s]+):(\\d+(?:-\\d+)?)$")\n')),
    ("M08-dup-id-ignored",
     "duplicate registry ids accepted (first row used)",
     ('            if len(rws) > 1:\n',
      '            if False:\n')),
    ("M09-no-registry-row-ignored",
     "a missing registry row is not a violation",
     ('            if len(rws) == 0:\n',
      '            if False:\n')),
    ("M10-noname-ignored",
     "NAME containing # or ? is accepted",
     ('            if name is None or "#" in name or "?" in name:\n',
      '            if name is None:\n')),
    ("M11-trailing-punct-kept",
     "trailing `).,;` not stripped from the last path component",
     ('    while name and name[-1] in TRAILING:\n',
      '    while False:\n')),
    ("M12-id-exactly-three-digits",
     "registry ids with four digits are out of scope",
     ('SID_RE = re.compile(r"^S\\d{3,}$")\n',
      'SID_RE = re.compile(r"^S\\d{3}$")\n')),
    ("M13-fenced-code-in-scope",
     "table rows inside fenced code are counted",
     ('        if s.startswith("```") or s.startswith("~~~"):\n'
      '            in_fence = True\n'
      '            continue\n',
      '        if False:\n'
      '            pass\n')),
    ("M14-empty-entry-green",
     "an entry with no evidence rows reads OK",
     ("verdict={'OK' if miss == 0 and rows > 0 else 'FAIL'}",
      "verdict={'OK' if miss == 0 else 'FAIL'}")),
    ("M15-cover-exclusive-bounds",
     "cover uses strict N < L < M instead of N <= L <= M",
     ('            covered_here = any(\n'
      '                hi >= n and n <= line_no <= hi for n, hi in flat\n'
      '            )\n',
      '            covered_here = any(\n'
      '                n < line_no < hi for n, hi in flat\n'
      '            )\n')),
    ("M16-first-locator-only",
     "only the first locator of the occurrence is considered",
     ('            flat = [it for occ in occurrences for it in occ]\n',
      '            flat = [it for occ in occurrences for it in occ[:1]]\n')),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def load_vectors(vectors_dir):
    rows = []
    tsv = os.path.join(vectors_dir, "vectors.tsv")
    with open(tsv, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    header = lines[0].split("\t")
    for line in lines[1:]:
        if not line.strip():
            continue
        f = line.split("\t")
        rec = dict(zip(header, f))
        vid = rec["id"]
        exp = os.path.join(vectors_dir, "expected", vid)
        with open(exp + ".stdout", encoding="utf-8") as fh:
            stdout = fh.read()
        with open(exp + ".rc", encoding="utf-8") as fh:
            rc = int(fh.read().strip())
        strict = []
        forbid = []
        p = exp + ".strict"
        if os.path.exists(p):
            with open(p, encoding="utf-8") as fh:
                strict = [t for t in fh.read().split("\n") if t]
        p = exp + ".forbid"
        if os.path.exists(p):
            with open(p, encoding="utf-8") as fh:
                forbid = [t for t in fh.read().split("\n") if t]
        rows.append({
            "id": vid,
            "sha": rec["sha"],
            "stdout": stdout,
            "rc": rc,
            "strict": strict,
            "forbid": forbid,
        })
    return rows


def tokens(text):
    out = set()
    for tok in text.split():
        out.add(tok.strip("[]()"))
    return out


def run_oracle(oracle, repo, rev, work):
    os.makedirs(work, exist_ok=True)
    r = subprocess.run(
        [sys.executable, "-I", oracle, "--repo", repo, "--rev", rev,
         "--work", work],
        capture_output=True, text=True,
    )
    return r.stdout, r.returncode, r.stderr


def evaluate(oracle, vec, fixtures, work, tmp):
    repo = os.path.join(fixtures, vec["id"])
    out, rc, err = run_oracle(oracle, repo, vec["sha"], work)
    toks = tokens(out)
    missing = [t for t in vec["strict"] if t not in toks]
    present = [t for t in vec["forbid"] if t in toks]
    ok = (not missing and not present and rc == vec["rc"])
    return {
        "ok": ok,
        "rc": rc,
        "want_rc": vec["rc"],
        "missing": missing,
        "present": present,
        "exact": out == vec["stdout"],
        "out": out,
        "err": err,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--oracle", required=True)
    ap.add_argument("--fixtures", required=True)
    ap.add_argument("--vectors", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--report", required=True)
    args = ap.parse_args()

    vectors = load_vectors(args.vectors)
    master = os.path.abspath(args.oracle)
    master_bytes = open(master, "rb").read()
    master_sha = sha256(master)

    scratch = os.path.abspath(args.scratch)
    os.makedirs(scratch, exist_ok=True)
    work = os.path.join(scratch, "work")
    mutants_dir = os.path.join(scratch, "mutants")
    os.makedirs(mutants_dir, exist_ok=True)

    out_lines = []
    out_lines.append("criterion-107 acceptance-vector mutation battery")
    out_lines.append(f"oracle (pristine master): {master}")
    out_lines.append(f"oracle sha256 (pristine): {master_sha}")
    out_lines.append(f"vectors: {len(vectors)}")
    out_lines.append("detector: run the oracle on each fixture repo at its "
                     "commit; require rc == expected rc, every strict token "
                     "present, every forbidden token absent")
    out_lines.append("")

    # ---- baseline: pristine master on pristine fixtures ----
    base_fail = []
    for vec in vectors:
        res = evaluate(master, vec, args.fixtures, work, scratch)
        if not res["ok"]:
            base_fail.append((vec["id"], res))
    out_lines.append(f"BASELINE (pristine master): "
                     f"{len(vectors) - len(base_fail)}/{len(vectors)} vectors pass")
    for vid, res in base_fail:
        out_lines.append(
            f"  baseline FAIL {vid}: rc={res['rc']} want={res['want_rc']} "
            f"missing={res['missing']} forbidden_present={res['present']}"
        )
        out_lines.append("    stdout:")
        for ln in res["out"].split("\n"):
            out_lines.append("      " + ln)
        if res["err"]:
            out_lines.append("    stderr:")
            for ln in res["err"].split("\n")[-6:]:
                out_lines.append("      " + ln)
    out_lines.append("")

    # ---- mutants ----
    summary = []
    for mid, desc, (old, new) in MUTANTS:
        copy_path = os.path.join(mutants_dir, mid + ".py")
        shutil.copyfile(master, copy_path)
        pre_sha = sha256(copy_path)
        src = master_bytes.decode("utf-8")
        if old not in src:
            out_lines.append(f"{mid}: PATCH ANCHOR NOT FOUND — mutant not "
                             f"applied (inconclusive)")
            summary.append((mid, "inconclusive", "patch anchor not found"))
            continue
        patched = src.replace(old, new, 1)
        with open(copy_path, "w", encoding="utf-8") as fh:
            fh.write(patched)
        post_sha = sha256(copy_path)
        killed = []
        survived = []
        inconclusive = []
        for vec in vectors:
            res = evaluate(copy_path, vec, args.fixtures, work, scratch)
            if vec["id"] in {v[0] for v in base_fail}:
                inconclusive.append(vec["id"])
                continue
            if res["ok"]:
                survived.append(vec["id"])
            else:
                killed.append((vec["id"], res))
        # restore the copy from the pristine master bytes and verify
        with open(copy_path, "wb") as fh:
            fh.write(master_bytes)
        restored_sha = sha256(copy_path)
        verdict = "KILLED" if killed else "SURVIVED"
        out_lines.append(f"{mid} — {desc}")
        out_lines.append(f"  patch: {old.strip()!r} -> {new.strip()!r}")
        out_lines.append(f"  sha256 copy before patch : {pre_sha}")
        out_lines.append(f"  sha256 copy after patch  : {post_sha}")
        out_lines.append(f"  sha256 copy after restore: {restored_sha} "
                         f"(== pristine master: {restored_sha == master_sha})")
        out_lines.append(f"  verdict: {verdict}")
        for vid, res in killed:
            detail = (f"rc={res['rc']} want={res['want_rc']} "
                      f"missing={res['missing']} forbidden_present={res['present']}")
            out_lines.append(f"  killed by {vid}: {detail}")
            out_lines.append(f"    mutant stdout:")
            for ln in res["out"].split("\n"):
                out_lines.append("      " + ln)
        if survived:
            out_lines.append(f"  survived vectors: {','.join(survived)}")
        if inconclusive:
            out_lines.append(f"  inconclusive (baseline failed): "
                             f"{','.join(inconclusive)}")
        out_lines.append("")
        summary.append((mid, verdict,
                        ",".join(v for v, _ in killed) or "-"))

    out_lines.append("SUMMARY")
    for mid, verdict, killers in summary:
        out_lines.append(f"  {mid}: {verdict} killed_by={killers}")

    with open(args.report, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out_lines) + "\n")
    print("\n".join(out_lines[-len(summary) - 1:]))
    shutil.rmtree(mutants_dir, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

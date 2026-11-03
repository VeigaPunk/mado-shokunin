#!/usr/bin/env python3
"""run-mutants.py — apply exact single-match mutations and run the r66 control matrices.

    python3 run-mutants.py --target c1|c2 --src PATH --work DIR

Every mutant is one textual replacement; the harness refuses a patch whose old text does
not occur exactly once. Each mutant runs (1) the target's own selftest when present and
(2) the seat's behavioral matrix. Verdict: KILLED when the matrix leaves the frozen
expectation, SURVIVED when it matches pristine on every scored probe.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

C1_MUTANTS = [
    ("c1-m1-heading-uniqueness",
     '    if len(starts) != 1:\n        reasons.append(f"heading-count={len(starts)} expected=1")',
     '    if not starts:\n        reasons.append(f"heading-count={len(starts)} expected=1")'),
    ("c1-m2-per-row-receipt",
     "        if not any(receipt(path) is not None for path in pointers):",
     "        if False and not any(receipt(path) is not None for path in pointers):"),
    ("c1-m3-exact-live-line",
     "    gate = live is not None and LIVE_LINE in live.splitlines()",
     "    gate = live is not None"),
    ("c1-m4-live-path-binding",
     "    gate = live is not None and LIVE_LINE in live.splitlines()",
     "    gate = any(receipt(p) is not None and LIVE_LINE in receipt(p).splitlines() for p in paths)"),
]

C2_MUTANTS = [
    ("c2-m1-force-rc0",
     'exit "$exitcode"',
     "exit 0"),
    ("c2-m2-skip-citecheck-forged",
     'leg_citecheck() { python3 "$CITECHECK_SIBLING" --repo "$REPO_ABS" --rev "$REV" --paths "${CITE_PATHS[@]}"; }',
     "leg_citecheck() { printf 'MADO_CITECHECK: rev=%s files=1 citations=1 resolved=1 missing=0 skipped_large=0 verdict=TARGET_MET (VERSION forged)\\n' \"$REV\"; return 0; }"),
    ("c2-m3-skip-citecheck-nomarker",
     'leg_citecheck() { python3 "$CITECHECK_SIBLING" --repo "$REPO_ABS" --rev "$REV" --paths "${CITE_PATHS[@]}"; }',
     "leg_citecheck() { return 0; }"),
    ("c2-m4-hardcoded-round",
     '[ "${#CITE_PATHS[@]}" -gt 0 ] || CITE_PATHS=(".ufo/waves/round-$ROUND/receipts")',
     '[ "${#CITE_PATHS[@]}" -gt 0 ] || CITE_PATHS=(".ufo/waves/round-65/receipts")'),
    ("c2-m7-marker-count",
     '[ "$count" -eq 1 ] || return 1',
     '[ "$count" -ge 1 ] || return 1'),
    ("c2-m6-drop-git-scrub",
     '# Remove every Git steering variable, including GIT_CONFIG_COUNT and indexed keys.\nfor git_var in "${!GIT_@}"; do unset "$git_var"; done',
     "# mutation: GIT_* scrub removed\n:"),
    ("c2-m5-drop-round-required",
     '[[ "$ROUND" =~ ^[1-9][0-9]*$ ]] || fail \'--round N required (positive integer)\'',
     '[[ "$ROUND" =~ ^[1-9][0-9]*$ ]] || ROUND=65'),
]


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def apply(src, dst, old, new):
    with open(src, encoding="utf-8") as fh:
        text = fh.read()
    if text.count(old) != 1:
        raise SystemExit("PATCH REFUSED: old text occurs %d times in %s" % (text.count(old), src))
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(text.replace(old, new))
    os.chmod(dst, os.stat(src).st_mode)


def run(argv, **kw):
    return subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                          timeout=kw.pop("timeout", 300), **kw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", choices=("c1", "c2"), required=True)
    ap.add_argument("--src", required=True)
    ap.add_argument("--work", required=True)
    args = ap.parse_args()
    work = os.path.realpath(args.work)
    os.makedirs(work, exist_ok=True)
    src = os.path.realpath(args.src)
    mutants = C1_MUTANTS if args.target == "c1" else C2_MUTANTS
    fixtures = "/fast/scratch/hyaku/mado-r66/R66MutHardening/fixture-%s.py" % args.target
    rows = []
    for mid, old, new in mutants:
        mdir = os.path.join(work, mid)
        os.makedirs(mdir, exist_ok=True)
        dst = os.path.join(mdir, os.path.basename(src))
        apply(src, dst, old, new)
        entry = {"id": mid, "path": dst, "sha256": sha(dst),
                 "pristine_sha256": sha(src), "bytes": os.path.getsize(dst)}
        # Own selftest when the target has one.
        if args.target == "c1":
            st = run([sys.executable, dst, "--selftest"])
        else:
            st = run(["bash", dst, "--selftest", "--scratch-root",
                      os.path.join(mdir, "st")])
        entry["selftest_rc"] = st.returncode
        entry["selftest_last"] = ([ln for ln in st.stdout.splitlines() if ln.strip()] or [""])[-1]
        # Behavioral matrix.
        if args.target == "c1":
            mat = run([sys.executable, fixtures, "--counter", dst,
                       "--work", os.path.join(mdir, "matrix"), "--label", mid])
        else:
            mat = run([sys.executable, fixtures, "--instrument", dst,
                       "--work", os.path.join(mdir, "matrix"), "--label", mid])
        entry["matrix_rc"] = mat.returncode
        entry["matrix_tail"] = ([ln for ln in mat.stdout.splitlines() if ln.strip()] or [""])[-1]
        entry["matrix_stdout"] = mat.stdout
        entry["matrix_stderr"] = mat.stderr
        mp = os.path.join(mdir, "matrix", "c%s-matrix-%s.json" % (
            "1" if args.target == "c1" else "2", mid))
        core_ok = aux_bad = False
        core = aux = {}
        if os.path.isfile(mp):
            with open(mp, encoding="utf-8") as fh:
                md = json.load(fh)
            core = {"correct": md.get("correct"), "total": md.get("total")}
            core_ok = md.get("correct") == md.get("total")
            aux = {k: v.get("correct") for k, v in (md.get("aux") or {}).items()}
            aux_bad = any(v is False for v in aux.values())
        entry["core"] = core
        entry["aux"] = aux
        reasons = []
        if st.returncode != 0:
            reasons.append("selftest")
        if not core_ok:
            reasons.append("core-matrix")
        if aux_bad:
            reasons.append("aux-probe")
        entry["killed"] = bool(reasons)
        entry["killed_by"] = reasons
        rows.append(entry)
        print("%s\tselftest_rc=%d\tcore=%s/%s\taux_bad=%s\t%s\t%s"
              % (mid, st.returncode, core.get("correct"), core.get("total"), aux_bad,
                 ("KILLED by " + "+".join(reasons)) if reasons else "SURVIVED",
                 entry["matrix_tail"]))
    out = os.path.join(work, "mutants-%s.json" % args.target)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"target": args.target, "src": src, "src_sha256": sha(src),
                   "mutants": rows}, fh, indent=1, sort_keys=True)
    print("SUMMARY\t%s" % out)


if __name__ == "__main__":
    main()

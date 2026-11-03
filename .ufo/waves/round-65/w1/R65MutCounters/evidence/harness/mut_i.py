#!/usr/bin/env python3
"""Instrument mutation battery: one change per copy; detector = the script's own --selftest.

Baseline is the pristine copy: rc must be 0 and the assertion line N/N complete.
A mutant is KILLED when its selftest exits non-zero (or prints a FAIL) that the
pristine bytes do not.
"""
import json
import os
import re
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/mado-r65/w1/R65MutCounters"
SRC = S + "/targets/landing-counters.sh"
LAB = S + "/lab/quality"
OUT = S + "/instr-mut"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"

MUTANTS = [
    ("I1 citecheck leg skipped but rc forced 0",
     '  printf -- \'-- leg %s --\\n\' "$leg"\n  "leg_$leg"\n  rc=$?',
     '  printf -- \'-- leg %s --\\n\' "$leg"\n  if [ "$leg" = citecheck ]; then rc=0; else "leg_$leg"; rc=$?; fi'),
    ("I2 producer rc replaced by tail rc",
     '  "leg_$leg"\n  rc=$?',
     '  "leg_$leg" | tail -1\n  rc=$?'),
    ("I3 verdict conjunction flipped to disjunction",
     'if [ "$1" -eq 0 ] && [ "$2" -eq 0 ] && [ "$3" -eq 0 ] && [ "$4" -eq 0 ]; then',
     'if [ "$1" -eq 0 ] || [ "$2" -eq 0 ] || [ "$3" -eq 0 ] || [ "$4" -eq 0 ]; then'),
    ("I4 final exit forced 0",
     '[ "$verdict" = GREEN ]\nexit $?',
     'exit 0'),
    ("I5 /tmp scratch rooted accepted",
     '  /tmp | /tmp/* | /var/tmp | /var/tmp/*) die "--scratch-root must not be under /tmp or /var/tmp: $SCRATCH" ;;',
     '  /var/tmp | /var/tmp/*) die "--scratch-root must not be under /tmp or /var/tmp: $SCRATCH" ;;'),
    ("I6 symlink refusal removed",
     'if [ -L "$SCRATCH" ]; then die "--scratch-root must not be a symlink: $SCRATCH"; fi',
     ': # symlink refusal removed'),
    ("I7 default citecheck path redirected to round-64 receipts",
     'local -a paths=("$REPO_ABS/.ufo/waves/round-65/receipts")',
     'local -a paths=("$REPO_ABS/.ufo/waves/round-64/receipts")'),
    ("I9 used-by sibling path broken (instrument absent)",
     'USEDBY_SIBLING="$SELF_DIR/../quality/counters/c3-r56-used-by.py"',
     'USEDBY_SIBLING="$SELF_DIR/../quality/counters/absent-sibling.py"'),
    ("I8 --citecheck-paths accepts zero paths",
     '[ "$n" -gt 0 ] || die "--citecheck-paths needs at least one PATH"',
     '[ "$n" -ge 0 ] || die "--citecheck-paths needs at least one PATH"'),
]


def siblings(dst):
    os.makedirs(dst + "/counters", exist_ok=True)
    os.makedirs(dst + "/../tools", exist_ok=True)
    for src, rel in ((LANE + "/quality/check-tool-ledger.py", "/check-tool-ledger.py"),
                     (LANE + "/quality/counters/c3-r56-used-by.py", "/counters/c3-r56-used-by.py"),
                     (LANE + "/tools/mado-receipt-citecheck.py", "/../tools/mado-receipt-citecheck.py")):
        d = os.path.normpath(dst + rel)
        if not os.path.exists(d):
            shutil.copy(src, d)


def run_selftest(path, scratch):
    shutil.rmtree(scratch, ignore_errors=True)
    os.makedirs(scratch)
    p = subprocess.run(["bash", path, "--selftest", "--scratch-root", scratch],
                       capture_output=True, text=True, timeout=900)
    out = p.stdout + p.stderr
    fails = [l for l in out.splitlines() if l.startswith("SELFTEST FAIL")]
    summary = [l for l in out.splitlines() if l.startswith("MADO_LANDING_COUNTERS_SELFTEST:")]
    return p.returncode, (summary[0] if summary else "<no-summary>"), fails, out


def direct(path, args):
    p = subprocess.run(["bash", path] + args, capture_output=True, text=True, timeout=900)
    return p.returncode, (p.stdout + p.stderr)


def main():
    src = open(SRC).read()
    os.makedirs(OUT, exist_ok=True)
    BSRC = S + "/lab/quality/landing-counters.sh"
    base_rc, base_sum, base_fails, _ = run_selftest(BSRC, S + "/st/baseline")
    print("== BASELINE rc=%d %s fails=%d" % (base_rc, base_sum, len(base_fails)))
    if base_rc != 0:
        print("!! baseline is not green - kills are inconclusive")
    rows = []
    for label, old, new in MUTANTS:
        mid = label.split()[0]
        if src.count(old) != 1:
            print("!! %s: pattern count %d" % (mid, src.count(old)))
            rows.append({"id": mid, "label": label, "verdict": "N/A", "note": "pattern"})
            continue
        d = OUT + "/" + mid
        shutil.rmtree(d, ignore_errors=True)
        qual = d + "/quality"
        os.makedirs(qual)
        siblings(qual)
        path = qual + "/landing-counters.sh"
        open(path, "w").write(src.replace(old, new))
        rc, summ, fails, out = run_selftest(path, S + "/st/" + mid)
        killed = (rc != 0) or bool(fails) or summ != base_sum
        extra = []
        # direct behavioural probe on the lane's own receipts for the path mutants
        if mid == "I7":
            rc2, o2 = direct(path, ["--repo", LANE, "--rev", "cb63ab13ccaf85191318701d5db5ace050bd5bd4",
                                    "--scratch-root", S + "/st/I7probe"])
            extra.append("probe rc=%d :: %s" % (rc2, [l for l in o2.splitlines()
                                                      if "MADO_CITECHECK" in l or "LANDING_LEG citecheck" in l]))
        if mid == "I8":
            rc2, o2 = direct(path, ["--repo", LANE, "--rev", "HEAD", "--scratch-root",
                                    S + "/st/I8probe", "--citecheck-paths"])
            extra.append("probe rc=%d (baseline refuses rc=2) :: %s" % (rc2, o2.splitlines()[-1:]))
        verdict = "KILLED" if killed else "SURVIVED"
        print("== %-52s %s  rc=%d %s" % (label, verdict, rc, summ))
        for f in fails[:3]:
            print("     " + f)
        for e in extra:
            print("     " + e)
        rows.append({"id": mid, "label": label, "verdict": verdict, "rc": rc,
                     "summary": summ, "fails": fails, "probe": extra})
    with open(S + "/instr-mutants.json", "w") as f:
        json.dump({"baseline": {"rc": base_rc, "summary": base_sum}, "rows": rows}, f, indent=1)
    print("wrote", S + "/instr-mutants.json")


if __name__ == "__main__":
    main()

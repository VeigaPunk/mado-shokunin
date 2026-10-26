#!/usr/bin/env python3
"""MutCheckLocators mutation harness - single-edit mutants of check-locators.py.

Reads the pristine copy, applies exactly one (regex -> replacement) edit per
mutant into scratch, runs two bounded detectors against each mutant:

  D1 selftest: python3 m_<name>.py --selftest   (pristine rc=0, SELFTEST: PASS)
  D2 control:  python3 m_<name>.py --fetch <r42 fetch> LOG-r42.md
               (pristine: one LOC line, verdict=MISS, CHECK_LOCATORS locators=1
                miss=1, rc=1)

A mutant is a SURVIVOR only if both outputs are byte-identical and both exit
codes equal the pristine run's. Everything else is killed (by D1 or D2).

Writes: matrix.tsv (name, category, selftest_rc, control_rc, verdict),
        out/<name>.selftest.txt, out/<name>.control.txt
"""

import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PRISTINE = os.path.join(HERE, "pristine.py")
FETCH = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-42/fetch"
LOG = os.path.join(HERE, "LOG-r42.md")
OUT = os.path.join(HERE, "out")

with open(PRISTINE, "r", encoding="utf-8") as fh:
    BASE = fh.read()

# name, category, pattern (applied once, regex), replacement
MUTANTS = [
    # --- range inclusion ---------------------------------------------------
    ("exclusive-bounds", "range-inclusion",
     r"return any\(lo <= n <= hi for lo, hi in ranges\)",
     "return any(lo < n < hi for lo, hi in ranges)"),
    ("half-open-bounds", "range-inclusion",
     r"return any\(lo <= n <= hi for lo, hi in ranges\)",
     "return any(lo <= n < hi for lo, hi in ranges)"),
    ("no-reversed-normalisation", "range-inclusion",
     r"            if hi < lo:\n                lo, hi = hi, lo\n",
     ""),
    ("upper-plus-one", "range-inclusion",
     r"return any\(lo <= n <= hi for lo, hi in ranges\)",
     "return any(lo <= n <= hi + 1 for lo, hi in ranges)"),
    ("range-slice-offbyone", "range-inclusion",
     r"for i in range\(1, len\(lines\) \+ 1\)",
     "for i in range(1, len(lines))"),
    ("comma-to-semicolon", "range-inclusion",
     r"for part in spec\.split\(\",\"\):",
     'for part in spec.split(";"):'),
    # --- token length / boundary ------------------------------------------
    ("token-len-2", "token-length",
     r"return sorted\(t for t in toks if len\(t\) >= 3\)",
     "return sorted(t for t in toks if len(t) >= 2)"),
    ("token-len-4", "token-length",
     r"return sorted\(t for t in toks if len\(t\) >= 3\)",
     "return sorted(t for t in toks if len(t) >= 4)"),
    ("token-lower-boundary", "token-length",
     r'return re\.search\(r"\(\?<!\[A-Za-z0-9_\]\)" \+ re\.escape\(tok\) \+ r"\(\?!\[A-Za-z0-9_\]\)", text\) is not None',
     'return re.search(re.escape(tok), text) is not None'),
    ("token-insensitive", "token-length",
     r'return re\.search\(r"\(\?<!\[A-Za-z0-9_\]\)" \+ re\.escape\(tok\) \+ r"\(\?!\[A-Za-z0-9_\]\)", text\) is not None',
     'return re.search(r"(?<![A-Za-z0-9_])" + re.escape(tok) + r"(?![A-Za-z0-9_])", text, re.IGNORECASE) is not None'),
    # --- attribution nearest before/after ----------------------------------
    ("attr-before-inclusive", "attribution",
     r"before = \[c for c in cands if c\[1\] <= ls\]",
     "before = [c for c in cands if c[1] < ls]"),
    ("attr-after-exclusive", "attribution",
     r"after = \[c for c in cands if c\[0\] >= le\]",
     "after = [c for c in cands if c[0] > le]"),
    ("attr-after-first", "attribution",
     r"attr = before\[-1\] if before else \(after\[0\] if after else None\)",
     "attr = after[0] if after else (before[-1] if before else None)"),
    ("attr-before-farthest", "attribution",
     r"attr = before\[-1\] if before else \(after\[0\] if after else None\)",
     "attr = before[0] if before else (after[0] if after else None)"),
    ("support-any", "attribution",
     r"support = \{c\[2\]: all\(token_occurs\(t, text\) for t in c\[3\]\) for c in cands\}",
     "support = {c[2]: any(token_occurs(t, text) for t in c[3]) for c in cands}"),
    ("cited-offbyone", "attribution",
     r'return "\\n"\.join\(lines\[i - 1\] for i in range\(1, len\(lines\) \+ 1\) if in_ranges\(i, ranges\)\)',
     'return "\\n".join(lines[i] for i in range(1, len(lines) + 1) if in_ranges(i, ranges))'),
    # --- name resolution ----------------------------------------------------
    ("resolve-no-basename", "name-resolution",
     r"    base = name\.rsplit\(\"/\", 1\)\[-1\]\n    return base if base in fetch_names else None",
     "    return name if name in fetch_names else None"),
    ("resolve-always", "name-resolution",
     r"    return base if base in fetch_names else None",
     "    return base"),
    ("id-re-digit-lead", "name-resolution",
     r'ID_RE = re\.compile\(r"\[A-Za-z_\]\[A-Za-z0-9_\]\*"\)',
     'ID_RE = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_]*")'),
    ("locator-no-lookbehind", "name-resolution",
     r'    r"\(\?<!\[A-Za-z0-9_\./-\]\)"\n',
     ""),
    ("locator-no-lookahead", "name-resolution",
     r"    r\"\(\?!\[0-9A-Za-z_\]\)\"\n",
     ""),
    # --- fragment detection -------------------------------------------------
    ("frag-keep-empty", "fragment-detection",
     r"        if not toks:\n            continue\n",
     ""),
    ("frag-no-closing-tick", "fragment-detection",
     r'FRAG_RE = re\.compile\(r"`\(\[\^`\\n\]\+\)`"\)',
     'FRAG_RE = re.compile(r"`([^`\\n]+)")'),
    ("no-re-escape", "fragment-detection",
     r'r"\(\?<!\[A-Za-z0-9_\]\)" \+ re\.escape\(tok\) \+ r"\(\?!\[A-Za-z0-9_\]\)"',
     'r"(?<![A-Za-z0-9_])" + tok + r"(?![A-Za-z0-9_])"'),
    ("ranges-group-lazy", "fragment-detection",
     r"\[0-9\]\+\(\?:-\[0-9\]\+\)\?\(\?:,\[0-9\]\+\(\?:-\[0-9\]\+\)\?\)\*\)",
     "[0-9]+(?:-[0-9]+)??(?:,[0-9]+(?:-[0-9]+)??)*)"),
    # --- verdict strings / output -------------------------------------------
    ("nofrag-renamed", "verdict-string",
     r'            verdict = "NOFRAG"',
     '            verdict = "NOFRAGMENT"'),
    ("verdict-lowercase-ok", "verdict-string",
     r'            verdict = "OK"',
     '            verdict = "ok"'),
    ("summary-dropped", "verdict-string",
     r'    print\("CHECK_LOCATORS: locators=%d miss=%d" % \(total, misses\)\)\n',
     ""),
    ("summary-swapped", "verdict-string",
     r'"CHECK_LOCATORS: locators=%d miss=%d" % \(total, misses\)',
     '"CHECK_LOCATORS: locators=%d miss=%d" % (misses, total)'),
    ("miss-count-nofrag", "verdict-string",
     r'        if verdict == "MISS":\n            miss \+= 1',
     '        if verdict != "OK":\n            miss += 1'),
    # --- exit codes ----------------------------------------------------------
    ("exit-always-zero", "exit-codes",
     r"    return 1 if misses else 0",
     "    return 0"),
    ("usage-returns-one", "exit-codes",
     r'        print\("usage error: %s" % exc, file=sys\.stderr\)\n        return 2',
     '        print("usage error: %s" % exc, file=sys.stderr)\n        return 1'),
    ("selftest-allows-args", "exit-codes",
     r"        if args\.prose or args\.fetch or args\.explain:",
     "        if False:"),
    # --- selftest teeth -------------------------------------------------------
    ("teeth-identity-flip", "selftest-teeth",
     r"in_ranges = lambda n, ranges: not any\(lo <= n <= hi for lo, hi in ranges\)",
     "in_ranges = lambda n, ranges: any(lo <= n <= hi for lo, hi in ranges)"),
    ("teeth-one-direction", "selftest-teeth",
     r"        if flips == 0 or ok_to_miss == 0 or miss_to_ok == 0:",
     "        if flips == 0:"),
    ("verdicts-regex-nofrag", "selftest-teeth",
     r'r"fragments=\(\\d\+\) supported=\(\\d\+\) verdict=\(OK\|MISS\|NOFRAG\)\$"',
     'r"fragments=(\\d+) supported=(\\d+) verdict=(OK|MISS)$"'),
    ("selftest-min-cases-dropped", "selftest-teeth",
     r"        if k != ok or k < 12:",
     "        if k != ok:"),
]


def apply_once(name, pattern, repl):
    new, n = re.subn(pattern, lambda _m: repl, BASE, count=1)
    if n != 1:
        raise SystemExit("mutant %s: pattern applied %d times (want 1)" % (name, n))
    if new == BASE:
        raise SystemExit("mutant %s: replacement produced identical bytes" % name)
    return new


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120, cwd=HERE)
    return p.returncode, p.stdout + p.stderr


def main():
    os.makedirs(OUT, exist_ok=True)
    st_rc, st_out = run([sys.executable, PRISTINE, "--selftest"])
    ct_rc, ct_out = run([sys.executable, PRISTINE, "--fetch", FETCH, LOG])
    with open(os.path.join(OUT, "BASE.selftest.txt"), "w") as fh:
        fh.write("rc=%d\n%s" % (st_rc, st_out))
    with open(os.path.join(OUT, "BASE.control.txt"), "w") as fh:
        fh.write("rc=%d\n%s" % (ct_rc, ct_out))
    print("BASE selftest rc=%d | control rc=%d bytes=%d" % (st_rc, ct_rc, len(ct_out)))

    rows = []
    for name, cat, pattern, repl in MUTANTS:
        src = apply_once(name, pattern, repl)
        mpath = os.path.join(HERE, "m_%s.py" % name)
        with open(mpath, "w", encoding="utf-8") as fh:
            fh.write(src)
        try:
            s_rc, s_out = run([sys.executable, mpath, "--selftest"])
            c_rc, c_out = run([sys.executable, mpath, "--fetch", FETCH, LOG])
        except subprocess.TimeoutExpired:
            s_rc, s_out, c_rc, c_out = -9, "TIMEOUT", -9, "TIMEOUT"
        killed_by = None
        if (s_rc, s_out) != (st_rc, st_out):
            killed_by = "selftest"
        if (c_rc, c_out) != (ct_rc, ct_out):
            killed_by = (killed_by + "+control") if killed_by else "control"
        verdict = killed_by or "SURVIVED"
        with open(os.path.join(OUT, "%s.selftest.txt" % name), "w") as fh:
            fh.write("rc=%d\n%s" % (s_rc, s_out))
        with open(os.path.join(OUT, "%s.control.txt" % name), "w") as fh:
            fh.write("rc=%d\n%s" % (c_rc, c_out))
        h = hashlib.sha256(src.encode()).hexdigest()[:12]
        rows.append((name, cat, s_rc, c_rc, verdict, h))
        print("%-28s %-20s selftest=%3d control=%3d %s" % (name, cat, s_rc, c_rc, verdict))
        os.remove(mpath)

    with open(os.path.join(HERE, "matrix.tsv"), "w") as fh:
        fh.write("mutant\tcategory\tselftest_rc\tcontrol_rc\tverdict\tmutant_sha12\n")
        for r in rows:
            fh.write("\t".join(str(x) for x in r) + "\n")
    surv = [r[0] for r in rows if r[4] == "SURVIVED"]
    print("\n%d mutants, %d survived: %s" % (len(rows), len(surv), ", ".join(surv) or "none"))


if __name__ == "__main__":
    main()

#!/bin/sh
# Verify each quote in findings.md occurs in its cited file at its computed line (grep -F), and is <= 25 words.
cd /home/vgpnk/Projects/shokunin/mado-shokunin || exit 2
python3 - <<'PY'
import re
pairs = [
 ("corpus/QUALITY.md", 379, "runs it in a boundary that hides the judge (its code, its seeds' derivation, its call log and its table)"),
 ("corpus/QUALITY.md", 393, "a tool that reaches the verdict by reading the stub's bytes or replaying an on-disk copy is not running the program"),
 ("corpus/QUALITY.md", 324, "the receipts name the shortcut shapes the closures have seen meet a counter (do-nothing, all-false/empty, junk, server echo, label- or fixture-keyed, no-reader)"),
 (".ufo/waves/round-45/registration.md", 9, "navigation 61/61, calibration 71/71, operability 12/12): every published axis"),
 (".ufo/waves/round-45/registration.md", 10, "ties at its maximum, so each is a lowest axis and the claims' after-states are their counters' lines"),
 (".ufo/waves/round-45/registration.md", 18, "Prior art at base, disclosed: `tools/mado-verify.sh:3518-3530` checks one hardcoded output"),
 (".ufo/waves/round-45/registration.md", 19, "(DP-1 3440x1440 within 0.5 Hz of 100) without reading any rule"),
 (".ufo/waves/round-45/registration.md", 54, "clause j binds a locator and a keyword"),
 (".ufo/waves/round-45/registration.md", 55, "per surface, not the truth of the sentence"),
 ("quality/counters/c1-r45-monitors.py", 12, "the tool is extracted to a fresh directory under --work"),
 ("quality/counters/c1-r45-monitors.py", 311, 'env = {"PATH": fakebin + ":/usr/bin:/bin"'),
 ("corpus/knowledge/output-colour-boundaries-r14.md", 91, "Output test/apply, resulting monitor state, persistence across restart, hotplug race behavior, HDR rendering"),
 ("corpus/knowledge/output-colour-boundaries-r14.md", 14, "requested-versus-actual state"),
 ("SCORECARD.md", 2298, "`sourced-art` was published at 1.0 in round 32 as"),
 ("SCORECARD.md", 2579, "state-aware rule size versus reported size join"),
 ("SCORECARD.md", 601, "Saturation remains 9.0, stagnation window N=3; retired axes: none."),
 ("tools/mado-verify.sh", 3526, "abs(float(x.get('refreshRate', 0)) - 100) < 0.5"),
 ("tools/mado-wsrules.py", 632, "rule.monitor = field[delim + 8:]"),
 ("quality/check-axis-scores.py", 32, 'AXES = ("navigation", "calibration", "operability")'),
]
bad = 0
for path, ln, quote in pairs:
    lines = open(path, encoding="utf-8", errors="replace").read().split("\n")
    okline = ln <= len(lines) and quote in lines[ln-1]
    anywhere = quote in "\n".join(lines)
    words = len(quote.split())
    verdict = "OK" if okline and words <= 25 else "FAIL"
    if verdict == "FAIL":
        bad += 1
    print("%s %s:%d words=%d at_line=%s in_file=%s" % (verdict, path, ln, words, okline, anywhere))
print("QUOTES: checked=%d failed=%d" % (len(pairs), bad))
raise SystemExit(1 if bad else 0)
PY

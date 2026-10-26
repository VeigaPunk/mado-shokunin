#!/usr/bin/env python3
"""SentW2Privacy — check the report's quotes and locators, and re-scan for leaks.

Three jobs, all value-free output:

1. every quote printed in the report is <= 25 words, appears verbatim in the report file it is printed in,
   and appears verbatim on the located line of the revision it cites;
2. every S2 locator actually holds a live monitor identity string on that line (the report says so);
3. neither the report nor any receipt in this seat dir contains a live monitor identity string
   (serial/description/make/model of one live `hyprctl monitors all -j` dump).

Usage: verify-quotes.py --repo LANE --rev REV --live monitors-all.json --report REPORT.md
Writes receipt-quotes.txt and receipt-leakcheck.txt next to the report; exit 1 on any FAIL.
"""

import argparse
import json
import os
import subprocess
import sys

# (source path at --rev, line, quote, what it shows)
QUOTES = [
    ("quality/check-session-material.py", 4,
     "Question answered: does any tracked file under ``.ufo/`` at a revision carry",
     "gate scope is .ufo only"),
    ("quality/check-session-material.py", 28,
     "``make`` or ``model``. Redacted/empty serials do not match.",
     "R3 needs a serial; a synthetic one is indistinguishable"),
    ("quality/check-session-material.py", 31,
     "shape of a ``find ~`` / ``ls`` dump. Paths quoted inside a",
     "R4 counts whole-line dumps only"),
    (".ufo/waves/round-45/w1/ExecPrivacyGate/report.md", 102,
     "with the same 50 files: D1 is still unfixed",
     "stale at 4d22eeb: D1 was closed by ee6659b9"),
]

# (path at --rev, line, identity field expected on that line)
LOCATORS = [
    (".ufo/waves/round-45/w1/CritPremise/receipts.txt", 5, "make"),
    (".ufo/waves/round-45/w1/CritPremise/receipts.txt", 17, "make"),
    (".ufo/waves/round-45/w1/CritPremise/receipts.txt", 20, "model"),
    (".ufo/waves/round-45/w1/ExecLiveHost/verify-quotes.py", 48, "make"),
    (".ufo/waves/round-45/w1/ExecSeedSweep/name-anchors.txt", 2, "make"),
    (".ufo/waves/round-45/w1/ExecSeedSweep/name-anchors.txt", 3, "make"),
    (".ufo/waves/round-45/w1/ExecSeedSweep/name-anchors.txt", 9, "make"),
    (".ufo/waves/round-45/w1/ExecDoNothingC1/control-a-lookup.py", 206, "make"),
    (".ufo/waves/round-45/w1/ExecDoNothingC1/control-a2-obfuscated.py", 34, "make"),
    (".ufo/waves/round-45/w1/MutC1Counter/c1-r45-monitors.py", 255, "make"),
    ("quality/counters/c1-r45-monitors.py", 255, "make"),
    ("quality/counters/c1-r45-monitors-v2.py", 202, "make"),
    ("corpus/knowledge/config-health-report-r3.md", 149, "serial"),
    ("corpus/knowledge/config-health-report-r3.md", 149, "description"),
    ("corpus/knowledge/hyprctl-verification-layer.md", 153, "serial"),
    ("corpus/knowledge/hyprctl-verification-layer.md", 153, "description"),
    ("corpus/knowledge/hyprland-config-plane.md", 183, "model"),
    ("corpus/knowledge/hyprland-config-plane.md", 184, "serial"),
]


def git_show(repo, rev, path):
    r = subprocess.run(("git", "-C", repo, "show", "%s:%s" % (rev, path)), capture_output=True)
    return r.stdout.decode("utf-8", "replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--live", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--extra", action="append", default=[],
                    help="additional file to include in the leak check (repeatable)")
    a = ap.parse_args()
    seat = os.path.dirname(os.path.abspath(a.report))
    report = open(a.report, encoding="utf-8").read()
    live = json.load(open(a.live))
    vals = {}
    for m in live:
        for k in ("serial", "description", "make", "model"):
            v = str(m.get(k) or "")
            if len(v) >= 3:
                vals.setdefault(k, set()).add(v)

    fails = 0
    qlines = []
    for path, ln, quote, why in QUOTES:
        words = len(quote.split())
        src = git_show(a.repo, a.rev, path).splitlines()
        on_line = ln <= len(src) and quote in src[ln - 1]
        in_report = quote in report
        tag = "PASS" if (words <= 25 and on_line and in_report) else "FAIL"
        fails += tag == "FAIL"
        qlines.append("%s words=%d line_match=%s report_match=%s src=%s:%d  # %s"
                      % (tag, words, on_line, in_report, path, ln, why))
        qlines.append("     quote: %s" % quote)
    qrec = os.path.join(seat, "receipt-quotes.txt")
    open(qrec, "w", encoding="utf-8").write("\n".join(qlines) + "\n")

    # the receipt must itself carry each quote (the locator check greps the receipt, not the report)
    rec = open(qrec, encoding="utf-8").read()
    for path, ln, quote, why in QUOTES:
        if quote not in rec or ("%s:%d" % (path, ln)) not in rec:
            print("FAIL receipt-missing %s:%d" % (path, ln))
            fails += 1
    print("\n".join(qlines))
    print("QUOTES: n=%d fails=%d receipt=%s" % (len(QUOTES), fails, os.path.basename(qrec)))

    lfails = 0
    ll = []
    for path, ln, field in LOCATORS:
        src = git_show(a.repo, a.rev, path).splitlines()
        ok = ln <= len(src) and any(v in src[ln - 1] for v in vals[field])
        lfails += not ok
        ll.append("%s live_%s %s:%d" % ("PASS" if ok else "FAIL", field, path, ln))

    # leak check: no live identity string may appear in this report or in any receipt here
    scanned = 0
    targets = [os.path.join(seat, n) for n in sorted(os.listdir(seat)) if n.endswith((".md", ".txt"))]
    targets += list(a.extra)
    for f in targets:
        name = os.path.basename(f)
        try:
            t = open(f, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        scanned += 1
        for k, vs in vals.items():
            for v in vs:
                if v in t:
                    lfails += 1
                    ll.append("FAIL leak live_%s in %s" % (k, name))
    ll.append("LEAKCHECK: files=%d values=%d fails=%d"
              % (scanned, sum(len(v) for v in vals.values()), lfails))
    lrec = os.path.join(seat, "receipt-leakcheck.txt")
    open(lrec, "w", encoding="utf-8").write("\n".join(ll) + "\n")
    print("\n".join(ll))
    print("LOCATORS_AND_LEAKS: fails=%d receipt=%s" % (lfails, os.path.basename(lrec)))
    return 1 if (fails or lfails) else 0


if __name__ == "__main__":
    sys.exit(main())

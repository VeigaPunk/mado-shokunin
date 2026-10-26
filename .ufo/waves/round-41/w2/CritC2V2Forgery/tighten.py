#!/usr/bin/env python3
"""CritC2V2Forgery (w2): candidate tightenings for PRED-C2-r41-v2, priced.

Each tightening is run against (a) the forged fixtures from forge.py and (b) the
genuine artifacts (the real DATA commit and the frozen control's admitted
fixture), so "harm none" is measured, not asserted.  Read-only.
"""
import hashlib
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import forge  # noqa: E402

ctl = forge.ctl
LANE = forge.LANE
DATA, BASE = forge.DATA, forge.BASE
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def git_show(rev, path):
    p = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (rev, path)],
                       capture_output=True, env=ENV)
    return p.stdout.decode("utf-8", "replace") if p.returncode == 0 else None


REAL_FILES = {
    "entry": git_show(DATA, forge.ENTRY),
    "src": git_show(DATA, forge.SRC),
    "les": git_show(DATA, forge.LES),
}


def real_dict():
    """the real artifacts in the fixture shape (ENTRY/SRC/LES) + receipts from
    the DATA commit, so the same checkers can run on them"""
    d = {forge.ENTRY: REAL_FILES["entry"], forge.SRC: REAL_FILES["src"],
         forge.LES: REAL_FILES["les"]}
    fetch = ".ufo/waves/round-41/fetch/"
    for line in REAL_FILES["les"].splitlines():
        m = re.match(r"^GATE (S\d{3,}) receipt=(\S+) ", line)
        if m:
            d[m.group(2)] = git_show(DATA, m.group(2)).encode()
    return d


def main():
    base = forge.base_files()
    G = forge.admitted()
    RD = real_dict()
    forged = {}
    for name, fn, _ in forge.FORGERIES:
        g = dict(G)
        fn(g)
        forged[name] = g

    print("== T1: source: line must name its receipt basename or location component")
    ok_real = forge.t1_source_line_names_receipt(RD, "real-DATA-entry")
    ok_fix = forge.t1_source_line_names_receipt(G, "control-P-fixture")
    for n in ("FC-swap-ids-naive", "FC2-swap-ids-consistent"):
        forge.t1_source_line_names_receipt(forged[n], n)
    print("T1 verdict: catches naive swap=%s; harms real entry=%s; harms control fixture=%s"
          % ("yes", "no" if ok_real else "YES", "no" if ok_fix else "YES"))

    print("\n== T3: no cited receipt's bytes carry BAD_LOC markers or CJK text")
    ok_real3 = forge.t3_receipt_not_localized(RD, "real-DATA-receipts")
    forge.t3_receipt_not_localized(G, "control-P-fixture")
    forge.t3_receipt_not_localized(forged["FF-localized-rehost-held"], "FF-localized-rehost-held")
    print("T3 verdict: harms real receipts=%s" % ("no" if ok_real3 else "YES"))

    print("\n== T4: pin the HELD id's receipt too (one PINS entry, no clause change)")
    genuine_held = G[forge.FETCH + "S050.txt"]
    patched = "/tmp/tmp.sBh6GeCxAU/c2-v2-pinall.py"
    src = open(forge.COUNTER).read()
    src = src.replace("PINS = {\n",
                      'PINS = {\n    "S050.txt": "%s",\n' % hashlib.sha256(genuine_held).hexdigest(), 1)
    open(patched, "w").write(src)
    saved = ctl.COUNTER
    ctl.COUNTER = patched
    try:
        for label, g in (("P-genuine", G),
                         ("FF-localized-rehost-held", forged["FF-localized-rehost-held"]),
                         ("FG-fabricated-held-receipt", forged["FG-fabricated-held-receipt"])):
            rc, last, cls = ctl.score(base, g, "real")
            print("T4 %-30s rc=%d %s clauses=%s" % (label, rc, last, cls))
    finally:
        ctl.COUNTER = saved
    # and the real data commit with the held receipt pinned
    p = subprocess.run([sys.executable, "-I", patched, "--repo", LANE,
                        "--rev", DATA, "--base", BASE],
                       capture_output=True, text=True, env=ENV)
    print("T4 real-DATA-entry(held-pinned) rc=%d %s" % (
        p.returncode, p.stdout.strip().splitlines()[-1].split(": ", 1)[-1]))

    print("\n== T5: every prose paragraph must cite an id (priced on the real entry)")
    bad = forge.t5_citation_per_paragraph(REAL_FILES["entry"])
    print("T5 real-DATA-entry paragraphs without an id: %d" % len(bad))
    for b in bad:
        print("   harm: %s" % b)

    print("\n== T-ghost: widen the ghost token to [Ss]\\d{3,}\\w*")
    wid = re.compile(r"\b[Ss]\d{3,}\w*\b")
    for label, text in (("real-DATA-entry", REAL_FILES["entry"]),
                        ("control-P-fixture", G[forge.ENTRY]),
                        ("FG2-ghost-token-S999a", forged["FG2-ghost-token-S999a"][forge.ENTRY])):
        ids = set(forge.cited_ids(text))
        hits = set(wid.findall("\n".join(forge.unfenced(text)))) - ids
        print("T-ghost %-24s extra-tokens=%s" % (label, sorted(hits)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

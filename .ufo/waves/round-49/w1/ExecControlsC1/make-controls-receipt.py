#!/usr/bin/env python3
"""Assemble receipts/controls.txt: one line per control - verdict under the draft, and the clause that stopped it.

Inputs are the score-with-draft.py outputs (the draft itself, then the three measurement copies with clause r, clause g
and both switched off). Nothing is re-run here: every number comes from a PRED-C1-r49 final line in an input file.

Usage: make-controls-receipt.py --full F --nor F --nogen F --nor-nogen F --isolation F --out receipts/controls.txt
"""
import argparse
import os
import re
import subprocess

FINAL = re.compile(r"^PRED-C1-r49: fixtures=(\d+)/(\d+) generated=(\d+)/(\d+) selftest=(\w+) readonly=(\w+) "
                   r"tool=(\w+) verdict=(\w+)$")
META = re.compile(r"^PRED-C1-r49 clause=meta rev=(\S+) nonce=(\d+) .*fixtures=(\d+)$")


def parse(path):
    """{control: {rev, counts..., verdict, stop}} from one run file."""
    runs, cur = {}, None
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("## control "):
            cur = line.split()[2]
            runs[cur] = {}
        m = META.match(line)
        if m and cur:
            runs[cur]["rev"], runs[cur]["nonce"], runs[cur]["fx_total"] = m.group(1), m.group(2), m.group(3)
        m = FINAL.match(line)
        if m and cur:
            g = m.groups()
            runs[cur].update({"f_ok": int(g[0]), "f_n": int(g[1]), "g_ok": int(g[2]), "g_n": int(g[3]),
                              "selftest": g[4], "readonly": g[5], "tool": g[6], "verdict": g[7]})
    return runs


def stops(r):
    out = []
    if r.get("tool") == "absent":
        out.append("t (tool absent at REV)")
    if r.get("selftest") == "fail":
        out.append("s (selftest)")
    if r.get("f_ok") != r.get("f_n"):
        out.append("f (%d/%d fixtures)" % (r["f_ok"], r["f_n"]))
    if r.get("g_ok") != r.get("g_n"):
        out.append("g (%d/%d generated)" % (r["g_ok"], r["g_n"]))
    if r.get("readonly") == "fail":
        out.append("r (trip)")
    return out or ["- (met)"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", required=True)
    ap.add_argument("--nor", required=True)
    ap.add_argument("--nogen", required=True)
    ap.add_argument("--nor-nogen", required=True)
    ap.add_argument("--isolation", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    full, nor, nogen, nrn = (parse(p) for p in (a.full, a.nor, a.nogen, a.nor_nogen))
    counter = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-49/w1/ExecCounterC1/c1-r49-keysym.py"
    lines = []
    lines.append("# ExecControlsC1 - control scoring, round 49 w1 (2026-10-27)")
    lines.append("#")
    lines.append("# instrument: ExecCounterC1's draft (not frozen at the time of writing)")
    lines.append("#   %s" % counter)
    lines.append("#   sha256 %s" % subprocess.run(["sha256sum", counter], capture_output=True)
                 .stdout.decode().split()[0])
    lines.append("# fixtures: the draft's own view (c1-r49-fixtures.json beside the counter, sha pinned by the draft)")
    lines.append("#   %s" % subprocess.run(["sha256sum", os.path.join(os.path.dirname(counter), "c1-r49-fixtures.json")],
                                            capture_output=True).stdout.decode().split()[0])
    lines.append("# nonce: 49 (fixed, so the fixture and generated case sets are the same for every row)")
    lines.append("# protocol: tools/mado-keysym.py of each control committed as its own revision in a scratch clone")
    lines.append("#   of the lane (/fast/scratch/hyaku/mado-r49/ExecControlsC1/ctlrepo), scored with")
    lines.append("#   `c1-r49-keysym.py --repo <clone> --rev <rev> --work <scratch> --nonce 49`.")
    lines.append("#")
    lines.append("# column 1: control; 2: verdict under the draft; 3: the clause(s) that stopped it;")
    lines.append("# 4: verdict with clause r switched off (measure/…-NOR.py); 5: with clause g off (…-NOGEN.py);")
    lines.append("# 6: with both off. A control that turns TARGET_MET only when a clause is switched off is the")
    lines.append("# evidence that the clause is what stops it.")
    lines.append("")
    head = "%-30s %-14s %-34s %-14s %-14s %s" % ("control", "draft", "stopped by", "r off", "g off", "r+g off")
    lines.append(head)
    lines.append("-" * len(head))
    met = []
    for name in sorted(full):
        r = full[name]
        if r.get("verdict") == "TARGET_MET":
            met.append(name)
        lines.append("%-30s %-14s %-34s %-14s %-14s %s" % (
            name, r.get("verdict"), "; ".join(stops(r)),
            nor.get(name, {}).get("verdict", "?"), nogen.get(name, {}).get("verdict", "?"),
            nrn.get(name, {}).get("verdict", "?")))
    lines.append("")
    lines.append("controls=%d met_under_draft=%d%s" % (len(full), len(met), (" " + ",".join(met)) if met else ""))
    lines.append("")
    lines.append("## clause-sensitivity, stated per control")
    for name in sorted(full):
        r = full[name]
        lines.append("%-30s draft: fixtures=%d/%d generated=%d/%d selftest=%s readonly=%s tool=%s rev=%s" % (
            name, r.get("f_ok", 0), r.get("f_n", 0), r.get("g_ok", 0), r.get("g_n", 0), r.get("selftest", "?"),
            r.get("readonly", "?"), r.get("tool", "?"), r.get("rev", "?")[:12]))
        lines.append("%-30s r off: %-14s g off: %-14s r+g off: %s" % (
            "", nor.get(name, {}).get("verdict", "?"), nogen.get(name, {}).get("verdict", "?"),
            nrn.get(name, {}).get("verdict", "?")))
    lines.append("")
    lines.append("## isolation, control c07-read-fixture-repo (the same tool file, two judges)")
    for line in open(a.isolation, encoding="utf-8"):
        lines.append(line.rstrip("\n"))
    open(a.out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines[:12]))


if __name__ == "__main__":
    main()

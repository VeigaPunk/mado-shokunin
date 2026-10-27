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

MAPPING = {
    "c01-absent": "no tool at tools/mado-keysym.py at all -> aimed at t",
    "c02-header-only.py": "a docstring and a return 0, no parser, no table -> aimed at s and f",
    "c03-first-match-only.py": "prints only the first (keycode, layout, level, mask) row -> aimed at f (multi-row keysyms)",
    "c04-no-modifiers.py": "all rows, every modifier mask blanked to [ ] -> aimed at f (LevelThree masks)",
    "c05-exec-xkbcli.py": "runs the pinned how-to-type and copies it -> aimed at r (process trip)",
    "c06-cache-table.py": "answers from a table built from this seat's fixtures -> aimed at g",
    "c07-read-fixture-repo.py": "reads the fixture file from the repository at run time -> aimed at i (mount set)",
    "c08-writes-file.py": "answers right, writes /tmp/mado-keysym-answers.cache -> aimed at r (write attempt)",
    "c09-opens-socket.py": "answers right, connects 127.0.0.1:47999 -> aimed at r (socket/connect)",
    "c10-overfit.py": "right on the fixture family, plausible bogus row elsewhere -> aimed at g",
    "c11-selftest-only.py": "passes --selftest, answers nothing -> aimed at s-alone counters and f",
    "c12-rc-blind.py": "right rows, always exit 0, never the judge's error status -> aimed at f/g (rc compared)",
    "c13-hardcoded-br.py": "ignores FILE, answers from the host br keymap -> aimed at f (multi-RMLVO fixtures)",
    "c14-stderr.py": "right text on stderr, nothing on stdout -> aimed at f (stdout bytes)",
    "c15-layout1-only.py": "drops rows with LAYOUT != 1 -> aimed at f/g (multi-layout keymaps)",
    "c16-always-unreachable.py": "always the 'no key produces this' report -> aimed at f (non-empty answers)",
    "c17-draft-fixture-table.py": "table built from the counter's OWN 633 fixtures -> aimed at g (the draft's declared residual)",
    "c18-draft-fixture-table-write.py": "c17 + a write attempt -> aimed at r and g together",
    "c19-draft-fixture-table-socket.py": "c17 + a socket connect -> aimed at r and g together",
    "c20-fixture-table-refusal-blind.py": "c17 but answers without --disable-compose/--keysym -> aimed at s (refusals)",
}
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
        m = re.match(r"^PRED-C1-r49 clause=s selftest rc=\d+ last=.* (ok|fail)$", line)
        if m and cur:
            runs[cur]["selftest_detail"] = m.group(1)
        m = re.match(r"^PRED-C1-r49 clause=s refusals=(ok|fail)", line)
        if m and cur:
            runs[cur]["refusals"] = m.group(1)
        m = re.match(r"^PRED-C1-r49 clause=r trips=(\d+)", line)
        if m and cur:
            runs[cur]["trips"] = m.group(1)
        m = FINAL.match(line)
        if m and cur:
            g = m.groups()
            runs[cur].update({"f_ok": int(g[0]), "f_n": int(g[1]), "g_ok": int(g[2]), "g_n": int(g[3]),
                              "selftest": g[4], "readonly": g[5], "tool": g[6], "verdict": g[7]})
    return runs


def stops(r):
    out = []
    if r.get("tool") == "absent":
        # the draft prints readonly=fail for an absent tool without running anything: the only stop is t
        return ["t (tool absent at REV)"]
    if r.get("selftest_detail") == "fail" or (r.get("selftest") == "fail" and "selftest_detail" not in r):
        out.append("s (selftest)")
    if r.get("refusals") == "fail":
        out.append("s (refusals)")
    if r.get("f_ok") != r.get("f_n"):
        out.append("f=%d/%d" % (r["f_ok"], r["f_n"]))
    if r.get("g_ok") != r.get("g_n"):
        out.append("g=%d/%d" % (r["g_ok"], r["g_n"]))
    if r.get("readonly") == "fail" and r.get("tool") != "absent":
        out.append("r (trips=%s)" % r.get("trips", "?"))
    return out or ["- (met)"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", required=True)
    ap.add_argument("--nor", required=True)
    ap.add_argument("--nogen", required=True)
    ap.add_argument("--nor-nogen", required=True)
    ap.add_argument("--isolation", required=True)
    ap.add_argument("--c20-nor", help="c20 scored with clause r off")
    ap.add_argument("--c20-nogen", help="c20 scored with clause g off")
    ap.add_argument("--c20-nos-nogen", help="c20 scored with clause s (refusals) and g off")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    full, nor, nogen, nrn = (parse(p) for p in (a.full, a.nor, a.nogen, a.nor_nogen))
    c20_nor = parse(a.c20_nor) if a.c20_nor else {}
    c20_nogen = parse(a.c20_nogen) if a.c20_nogen else {}
    c20_nosnogen = parse(a.c20_nos_nogen) if a.c20_nos_nogen else {}
    for name in list(c20_nor):
        nor[name] = c20_nor[name]
    for name in list(c20_nogen):
        nogen[name] = c20_nogen[name]
    for name in list(c20_nosnogen):
        nrn[name] = c20_nosnogen[name]
    counter = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-49/w1/ExecCounterC1/c1-r49-keysym.py"
    lines = []
    lines.append("# ExecControlsC1 - control scoring, round 49 w1 (2026-10-27)")
    lines.append("#")
    lines.append("# instrument: ExecCounterC1's draft at the sha its author named the freeze candidate")
    lines.append("#   (seat message 2026-10-27: '1a7fcc21... is the freeze candidate and I will not touch it again this wave')")
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
    head = "%-34s %-14s %-30s %-14s %-14s %s" % ("control", "draft", "stopped by", "r off", "g off", "r+g off")
    lines.append(head)
    lines.append("-" * len(head))
    met = []
    for name in sorted(full):
        r = full[name]
        if r.get("verdict") == "TARGET_MET":
            met.append(name)
        lines.append("%-34s %-14s %-30s %-14s %-14s %s" % (
            name, r.get("verdict"), "; ".join(stops(r)),
            nor.get(name, {}).get("verdict", "?"), nogen.get(name, {}).get("verdict", "?"),
            nrn.get(name, {}).get("verdict", "?")))
    lines.append("")
    lines.append("controls=%d met_under_draft=%d%s" % (len(full), len(met), (" " + ",".join(met)) if met else ""))
    lines.append("")
    lines.append("## clause-sensitivity, stated per control")
    for name in sorted(full):
        r = full[name]
        lines.append("%-34s draft: fixtures=%d/%d generated=%d/%d selftest=%s readonly=%s tool=%s rev=%s" % (
            name, r.get("f_ok", 0), r.get("f_n", 0), r.get("g_ok", 0), r.get("g_n", 0), r.get("selftest", "?"),
            r.get("readonly", "?"), r.get("tool", "?"), r.get("rev", "?")[:12]))
        lines.append("%-34s r off: %-14s g off: %-14s r+g off: %s" % (
            "", nor.get(name, {}).get("verdict", "?"), nogen.get(name, {}).get("verdict", "?"),
            nrn.get(name, {}).get("verdict", "?")))
    lines.append("")
    lines.append("## c20 note: with clause s (refusals) off and g off it scores TARGET_MET; r off alone and g off")
    lines.append("## alone both leave it TARGET_MISSED at s. Its r+g column above is the s+g measurement.")
    lines.append("")
    lines.append("## what each control cheats at, and the clause it is aimed at")
    for name in sorted(MAPPING):
        lines.append("%-34s %s" % (name, MAPPING[name]))
    lines.append("")
    lines.append("## isolation, control c07-read-fixture-repo (the same tool file, two judges)")
    for line in open(a.isolation, encoding="utf-8"):
        lines.append(line.rstrip("\n"))
    open(a.out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines[:12]))


if __name__ == "__main__":
    main()

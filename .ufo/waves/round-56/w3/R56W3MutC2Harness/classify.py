#!/usr/bin/env python3
"""R56W3MutC2Harness stage 3 — classify mutants against the seat's oracle and print the table.

Oracle tiers:
  ORACLE    = the frozen claim's own observables (PRED-C2-r56-v2):
                P1  green line + rc 0 on the honest tree
                P2  no-bwrap must fail closed (rc != 0, no result line on stdout)
                P3  degraded --no-sandbox run must still report the sandbox state (sandbox=none)
  EXTENDED  = discrimination probes (a cheating tool, a broken tool, a wrong-rc tool, tampered fixture /
              hold-out bytes, and control stubs that over-answer) — rc + stdout line
  DIAGNOSTIC= registration E10/E6 residue: work-dir leftovers, stderr fixture_commit token, refusal marker

Usage: classify.py <deliverable-dir>
"""
import json
import os
import sys

DELIVER = os.path.abspath(sys.argv[1])
RECEIPTS = os.path.join(DELIVER, "receipts")

ORACLE = {"P1_base", "P2_nobwrap_refusal", "P3_nobwrap_degraded"}
EXTENDED = {"P4_cheat_tool", "P5_broken_tool", "P6_tamper_fixture_note", "P7a_empty_ctl_answers",
            "P7b_const_ctl_answers_two", "P7c_lookup_ctl_answers_17", "P8_tamper_holdout_note",
            "P9_wrongrc_tool"}


def diff_fields(a, b):
    """which observable fields differ: 0 rc, 1 stdout, 2 token, 3 refusal, 4 leftovers"""
    a, b = list(a), list(b)
    out = set()
    names = ["rc", "stdout", "token", "refusal", "leftovers"]
    for i, n in enumerate(names):
        if a[i] != b[i]:
            out.add(n)
    return out


def main():
    summary = json.load(open(os.path.join(RECEIPTS, "summary.json")))
    ref = {k: tuple(v) for k, v in summary["pristine"].items()}
    if os.path.exists(os.path.join(RECEIPTS, "E09", "mutant.json")):
        rec = json.load(open(os.path.join(RECEIPTS, "E09", "mutant.json")))
        summary["mutants"]["E09"] = rec
    rows = []
    for mid in sorted(summary["mutants"]):
        rec = summary["mutants"][mid]
        if rec.get("verdict") == "ERROR":
            rows.append((mid, rec["family"], "INVALID-ANCHOR", [], rec.get("note", ""), rec.get("old", "")))
            continue
        obs = {k: tuple(v) for k, v in rec["observables"].items()}
        oracle_diff, ext_diff, diag_diff = [], [], []
        detail = {}
        for probe in sorted(ref):
            d = diff_fields(ref[probe], obs[probe])
            if not d:
                continue
            detail[probe] = sorted(d)
            core = d - {"leftovers", "token", "refusal"}
            if probe in ORACLE:
                # the token is part of the oracle only on the degraded (P3) run
                if probe == "P3_nobwrap_degraded":
                    if d - {"leftovers", "refusal"}:
                        oracle_diff.append(probe)
                    elif d:
                        diag_diff.append(probe)
                else:
                    if core or (probe == "P2_nobwrap_refusal" and (d & {"rc", "stdout", "refusal"})):
                        oracle_diff.append(probe)
                    elif d:
                        diag_diff.append(probe)
            elif probe in EXTENDED:
                if core:
                    ext_diff.append(probe)
                elif d:
                    diag_diff.append(probe)
            else:
                diag_diff.append(probe)
        if oracle_diff:
            verdict = "KILLED-ORACLE"
        elif ext_diff:
            verdict = "KILLED-EXTENDED"
        elif diag_diff:
            verdict = "KILLED-DIAGNOSTIC"
        else:
            verdict = "SURVIVED"
        rows.append((mid, rec["family"], verdict, oracle_diff + ext_diff + diag_diff, rec.get("note", ""), rec.get("old", "")))
    counts = {}
    for mid, family, verdict, probes, note, old in rows:
        counts[verdict] = counts.get(verdict, 0) + 1
    print(json.dumps({"counts": counts, "total": len(rows)}, indent=1))
    with open(os.path.join(RECEIPTS, "classified.tsv"), "w") as f:
        f.write("id\tfamily\tverdict\tprobes\tnote\n")
        for mid, family, verdict, probes, note, old in rows:
            f.write("%s\t%s\t%s\t%s\t%s\n" % (mid, family, verdict, ",".join(probes), note.replace("\t", " ")))
    for mid, family, verdict, probes, note, old in rows:
        print("%-4s %-9s %-17s %s" % (mid, family, verdict, ",".join(probes)))
    json.dump({"counts": counts, "rows": [{"id": r[0], "family": r[1], "verdict": r[2], "probes": r[3]} for r in rows]},
              open(os.path.join(RECEIPTS, "classified.json"), "w"), indent=1, sort_keys=True)


if __name__ == "__main__":
    main()

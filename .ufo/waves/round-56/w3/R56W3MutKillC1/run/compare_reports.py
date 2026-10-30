#!/usr/bin/env python3
"""Cross-check the observed kill signals against the values the wave-2 reports claim.

Seat A: the report's own FIXTURES table (must_have / must_not) is the pristine expectation.
Seat B: the report's mutants.md table gives (base rc, mut rc) per fixture; those are transcribed
here verbatim from .ufo/waves/round-56/w2/R56W2MutC1CounterB/mutants.md and compared with what
this seat observed at the lane tip.
"""
import json
import os
import sys

ROOT = "/fast/scratch/hyaku/mado-r56/R56W3MutKillC1"

# transcribed from R56W2MutC1CounterB/mutants.md "| F | mutant | fixture | base rc | mut rc | verdict |"
B_CLAIM = {
    "F02": ("M02", 1, 0), "F03": ("M03", 1, 0), "F04": ("M04", 0, 1), "F06": ("M06", 1, 1),
    "F08": ("M08", 1, 1), "F10": ("M10", 1, 1), "F11": ("M11", 0, 1), "F13": ("M13", 1, 0),
    "F19": ("M19", 1, 1), "F25": ("M25", 1, 1), "F29": ("M29", 1, 1), "F33": ("M33", 0, 1),
    "F37": ("M37", 0, 1), "F42": ("M42", 1, 1), "F45": ("M45", 1, 0), "F46": ("M46", 1, 0),
    "F48": ("M48", 0, 1), "F49": ("M49", 1, 1), "F50": ("M50", 1, 1), "F51": ("M51", 0, 1),
    "F54": ("M54", 0, 1), "F55": ("M55", 0, 1), "F56": ("M56", 0, 1), "F58": ("M58", 1, 0),
    "F59": ("M59", 1, 0), "F60": ("M60", 0, 1), "F62": ("M62", 0, 1), "F69": ("M69", 2, 0),
}

# transcribed from R56W2MutC1CounterA/mutants.md section 5: fixture -> (mutants, pristine legs)
A_CLAIM_LEGS = {
    "F01": ("M05", "row:K01"), "F02": ("M07", "row:K01"), "F03": ("M09", "row:K01"),
    "F04": ("M12", "row:K08"), "F05": ("M13 M14", "quote:K01"), "F06": ("M18", "host:H01"),
    "F07": ("M21", "source_cell:K03"), "F08": ("M26", "scope:K03"), "F09": ("M28", "scope:K03"),
    "F10": ("M34", ""), "F11": ("M37", ""), "F12": ("M38", "num:K07"), "F13": ("M39", ""),
    "F14": ("M43", "echo:K07"), "F15": ("M44", "prov"), "F16": ("M45", "prov"),
    "F17": ("M49", ""), "F18": ("M50", ""), "F19": ("M57", "pin_hash"), "F20": ("M65", ""),
    "F21": ("M16", "quote:K03"), "F22": ("M53", "new_rows"),
}


def main():
    d = json.load(open(os.path.join(ROOT, "kill-results.json")))
    bad = []
    print("== seat B: report claim (base rc, mut rc) vs observed at the lane tip ==")
    for r in d["results"]:
        if r["ns"] != "B" or "error" in r:
            continue
        fid = r["fixture"]
        claim = B_CLAIM.get(fid)
        m = r["mutants"][0]
        obs = (r["pristine"]["rc"], m["rc"])
        if claim is None:
            print("%-4s no claim transcribed" % fid)
            continue
        ok = (claim[1], claim[2]) == obs
        # seat B's F69 is a CLI check: base rc 2 is a setup error, not a counter miss
        if not ok:
            bad.append(("B", fid, claim, obs))
        print("%-4s %-4s claim=(%s,%s) observed=(%s,%s) %s" % (
            fid, m["mutant"], claim[1], claim[2], obs[0], obs[1], "MATCH" if ok else "DIFFERS"))
    print("\n== seat A: report's named leg present in the pristine output on the fixture ==")
    for r in d["results"]:
        if r["ns"] != "A" or "error" in r:
            continue
        fid = r["fixture"]
        claim = A_CLAIM_LEGS.get(fid)
        legs = r["pristine"]["legs"] or []
        leg = claim[1]
        ok = (leg in legs) if leg else True
        if not ok:
            bad.append(("A", fid, leg, legs))
        print("%-4s %-8s report leg=%-14s pristine has it: %-5s  pristine=%s" % (
            fid, claim[0], leg or "(none expected)", ok, ",".join(legs)[:110]))
    print("\nMISMATCHES: %d" % len(bad))
    for b in bad:
        print("  ", b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

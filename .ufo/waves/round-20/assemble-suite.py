#!/usr/bin/env python3
"""Assemble the round-20 precision suite from the wave-1 case-author dirs (L1, MadoR20).

Usage: assemble-suite.py  -> writes .ufo/waves/round-20/precision/ (scored suite) and
.ufo/waves/round-20/precision-heldout/ (reported beside, never inside, the score).
Inclusion is decided by the round-20 contract (E1-E4 as amended in SCORECARD "Round-20
pre-measurement corrections"), never by any repaired tool's output: every case is taken
except those whose author marked them `EDGE` (outside E1-E4: bash-function shadowing,
pipes into xargs/bash, `jj log --version`, installer `--help`), which go to the held-out
set; byte-identical cases with the same expectation are kept once (first seat in SEATS
order); a name collision is resolved by prefixing the seat. Case content is data only.
"""
import collections
import hashlib
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "w1", "cases")
DST = os.path.join(ROOT, "precision")
HELD = os.path.join(ROOT, "precision-heldout")
SEATS = ["CasePureBuiltins", "CasePureCollections", "CasePureFormatters", "CasePureCallables",
         "CasePureCrossCell", "CaseShadowing", "CaseWrapperCrossCell", "CaseWrapperForms",
         "CaseHelpBash", "CaseDryRunBash", "CaseHelpDryRunEval", "CaseLeadsInvisible",
         "CaseAdoptW2"]
NOTE = ("Round-20 precision suite, assembled by assemble-suite.py from "
        ".ufo/waves/round-20/w1/cases/<seat>/ (wave-1 case authors, blind to the repaired "
        "tool). Counter: tw-precision.py. `before` is the author's reading, re-measured by "
        "the counter.")


def main():
    for d in (DST, HELD):
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)
    seen, names, buckets, dropped = {}, set(), {DST: [], HELD: []}, []
    for seat in SEATS:
        spec = json.load(open(os.path.join(SRC, seat, "cases.json")))
        for c in spec["cases"]:
            data = open(os.path.join(SRC, seat, c["file"]), "rb").read()
            digest = hashlib.sha256(data).hexdigest()
            key = (digest, c["want_exit"],
                   tuple(sorted(json.dumps(w, sort_keys=True) for w in c["want_findings"])))
            if key in seen:
                dropped.append((seat, c["name"], "duplicate of " + seen[key]))
                continue
            name = c["name"] if c["name"] not in names else seat + "-" + c["name"]
            fname = seat + "--" + os.path.basename(c["file"])
            out = HELD if c.get("why", "").startswith("EDGE") else DST
            with open(os.path.join(out, fname), "wb") as fh:
                fh.write(data)
            seen[key] = name
            names.add(name)
            buckets[out].append({"name": name, "family": c["family"], "file": fname,
                                 "sha256": digest, "want_exit": c["want_exit"],
                                 "want_findings": c["want_findings"], "seat": seat,
                                 "why": c.get("why", ""), "before": c.get("before", {})})
    for out, label in ((DST, "scored"), (HELD, "held-out (EDGE)")):
        with open(os.path.join(out, "expected.json"), "w") as fh:
            json.dump({"schema": "mado-tw-precision-suite-v1", "note": NOTE + " Set: " + label,
                       "cases": buckets[out]}, fh, indent=1)
            fh.write("\n")
        print(label, len(buckets[out]),
              dict(collections.Counter(c["family"] for c in buckets[out])))
    for d in dropped:
        print("dropped", *d)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Classify every mutant from the receipts and write the machine-readable table (classes.json) and the kill-rate facts.

Categories (verdict = stdout or exit status of the harness):
  K-spec   killed by an oracle the spec names (real counter, always-green stub, reject-all stub)
  K-extra  killed only by an added oracle (kitchen-sink stub, single-leg / malformed stubs, wrappers, variants)
  K-fix    killed only by a fixture tree (var_srcline2, var_pinlink) run in extra_variants.py
  W        verdict-level survivor of the frozen battery: the control still scores ok, for the wrong reason
  D        diagnostic-only (stderr notes or print width): verdict identical, not a control defect
  E        equivalent: every oracle identical; argued in EQUIV below
"""
import json
import os
import re
from pathlib import Path

R = Path("/fast/scratch/hyaku/mado-r56/R56W2MutC1Harness/receipts")
SPEC = {"real", "stub_green", "stub_reject"}
FIX = {"M15": "var_pinlink", "M16": "var_pinlink", "M63": "var_srcline2"}
W = {"M23", "M24", "M25", "M58", "M60"}
D = {"M55", "M56"}
EQUIV = {
    "M01": "E-host: CHILD_TIMEOUT=1s never fires on this host (unloaded counter run 0.18 s; no TIMEOUT rc in any receipt); a slow-host hazard, not a control weakness.",
    "M05": "E-general: an empty missed= field reaches LEG_RE as [''] (rejected) instead of failing LINE_RE; both paths return an error and no control is admitted; stdout identical.",
    "M12": "E-general: `git ls-tree -z` prints nothing for an absent path and a record for a present one, so `if out:` and `if out.strip(b\"\\0\"):` agree on every git output.",
    "M13": "E-general: pathspec order to `git archive` does not change the archived tree.",
    "M14": "E-accepted-input: `present` cannot be empty: TABLES_PATH must be a regular blob at REV or Setup raises before the export.",
    "M17": "E-general: a no-op mutation yields the good tree, which scores TARGET_MET, so the control prints 'mutant admitted' (FAIL) exactly as the pristine MutationError does; zero 'changed nothing' lines in pristine stderr.",
    "M27": "E-class: S384 is another pin's row, as S385 is; both produce legs source_cell:K10,scope:K10 (identical receipts).",
    "M29": "E-class: the mutated status is on the injected S399 row; source_cell:K10 already fails on the sid mismatch and scope_covers reads only cells[5] (counter line 483), so status cannot change legs.",
    "M31": "E-class: any one-character change to the frozen K05 quote breaks quote identity; legs quote:K05,row:K05 either way.",
    "M32": "E-class: any single-byte change of a pinned file flips its sha256; pin_hash is the only leg.",
    "M35": "E-class: 1-9998 and 1-9999 are both past the 111-line pin, so the E3 bound fails for both.",
    "M54": "E-general: control order affects no result (each control runs in its own scratch repo; the log prints canonically).",
    "M57": "E-accepted-input: frozen-tables-v2.json is hash-pinned (TABLES_SHA256 check raises first), so k=30 and h=3 for every accepted input; `and` and `or` agree.",
    "M59": "E-class: a trailing full stop changes no identifier, number or quote containment that the counter tests.",
    "M65": "E-class: the pinned file is ConfigValues.cpp instead of ConfigWatcher.cpp; both are pinned, pin_hash is the only leg.",
}


def load(oracle, m, k):
    return (R / m / (oracle + "." + k)).read_text()


def pristine(o, k):
    return (R / "PRISTINE" / (o + "." + k)).read_text()


oracles = sorted(f[:-4] for f in os.listdir(R / "PRISTINE") if f.endswith(".out"))
mutants = sorted(d for d in os.listdir(R) if re.fullmatch(r"M\d\d", d))
cls = {}
for m in mutants:
    first = None
    for o in oracles:
        if pristine(o, "out") != load(o, m, "out") or pristine(o, "rc") != load(o, m, "rc"):
            first = o
            break
    spec_kill = any(pristine(o, "out") != load(o, m, "out") or pristine(o, "rc") != load(o, m, "rc")
                    for o in SPEC)
    if m in FIX:
        cat, by = "K-fix", FIX[m]
    elif first is not None:
        cat, by = ("K-spec" if spec_kill else "K-extra"), first
    elif m in W:
        cat, by = "W", "stdout/rc identical; stderr differs (wrong-reason legs)"
    elif m in D:
        cat, by = "D", "stderr note/print width only"
    else:
        cat, by = "E", EQUIV[m]
    detail = ""
    if cat in ("K-spec", "K-extra"):
        a = pristine(by, "out").strip().split("\n")[-1]
        b = load(by, m, "out").strip().split("\n")[-1]
        detail = "pristine: %s | mutant: %s" % (a[len("MADO_R56_CONTROLS: claim=c1 "):], b[len("MADO_R56_CONTROLS: claim=c1 "):])
    cls[m] = {"category": cat, "oracle": by, "detail": detail}

# Control 2 hole check: which rows carry a tok leg in the pinned (unclipped) pristine run?
gold = json.loads((Path("/fast/scratch/hyaku/mado-r56/R56W2MutC1Harness/proposals/gold.json")).read_text())
ids = ["K%02d" % i for i in range(1, 31)] + ["H01", "H02", "H03"]
tok2 = {l.split(":")[1] for l in gold["C1-CTL-02"] if l.startswith("tok:")}
no_tok = [i for i in ids if i not in tok2]

counts = {}
for v in cls.values():
    counts[v["category"]] = counts.get(v["category"], 0) + 1
verdict_relevant_nonequiv = [m for m in mutants if cls[m]["category"] not in ("E", "D")]
killed = [m for m in mutants if cls[m]["category"].startswith("K")]
out = {
    "mutants": len(mutants),
    "oracles": len(oracles),
    "counts": counts,
    "killed": len(killed),
    "killed_by_spec_oracles": sum(1 for m in mutants if cls[m]["category"] == "K-spec"),
    "verdict_relevant_nonequivalent": len(verdict_relevant_nonequiv),
    "kill_rate_all": round(len(killed) / len(mutants), 4),
    "kill_rate_excl_equiv": round(len(killed) / (len(mutants) - counts.get("E", 0)), 4),
    "kill_rate_excl_equiv_and_diag": round(len(killed) / len(verdict_relevant_nonequiv), 4),
    "spec_only_kill_rate_on_verdict_relevant": round(
        sum(1 for m in verdict_relevant_nonequiv if cls[m]["category"] == "K-spec") / len(verdict_relevant_nonequiv), 4),
    "control2_no_tok_rows": no_tok,
    "classes": cls,
}
(R.parent / "classes.json").write_text(json.dumps(out, indent=1, sort_keys=True))
print(json.dumps({k: v for k, v in out.items() if k != "classes"}, indent=1))
for m in mutants:
    print(m, cls[m]["category"], cls[m]["oracle"][:60])

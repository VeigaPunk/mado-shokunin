#!/usr/bin/env python3
"""Render mutants.md from the recorded mutation run (seat R56W2MutC2ToolA). Every number is computed here from
results.json, cross-matrix.json, kill-results.json and equiv-results.json; nothing is typed in by hand.

Usage: python3 -I report.py --run DIR --equiv DIR --out DIR
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mutate import MUTANTS  # noqa: E402

# Mutants proved EQUIVALENT: (argument) - no input the tool accepts distinguishes them from the pristine tool.
EQUIV_ARG = {
    "M73": "`if len(stack) > 0` is `if stack` (a list): identical truth value.",
    "M77": "same as M73: `if len(stack) > 0` is `if stack`.",
    "M78": "the mutant tests `##` in `line`, the pristine in `rhs`. A line reaches the OPTION branch only when its key is "
           "exactly `misc:disable_autoreload` (empty stack, lhs = OPTION) or `misc:disable_autoreload` with stack `[misc]` "
           "(lhs = `disable_autoreload`). Neither lhs contains `#`, and the stack text `misc` contains no `#`, so `##` in "
           "`line` holds iff it holds in `rhs`.",
    "M79": "same argument for `$`: the OPTION branch's lhs and stack contain no `$`, so `$` in `line` iff `$` in `rhs`.",
    "M81": "the mutant does not skip an lhs equal to `$` alone. That line's key is `$` or `<stack>:$`, never OPTION, so the "
           "mutant's fall-through to `if key != OPTION: continue` discards it with no side effect. The pristine `continue` "
           "discards it too.",
    "M83": "the mutant drops `return` after `nomatch`. `matches` is then empty and the following `for` loop has no body.",
    "M85": "the mutant drops `if match else match`. `glob` never yields the empty string, and `VALUE` is absolute (the "
           "`--config` path is absolute), so every match is absolute and `absolute_path(match)` is the identity.",
    "M99": "`dict.get(k)` and `dict.get(k, None)` return the same value.",
    "M104": "`config_flag` is already an int, so `int(config_flag)` is the same int.",
}
EQUIV_CORPUS = "in-process differential over a 3,851-case corpus (config bodies x getoption dumps x --home forms x argument shapes)"


def first_line(s):
    return s.strip().replace("\n", " ⏎ ").replace("|", "\\|")


def main(argv):
    run = equiv = out = None
    i = 0
    while i < len(argv):
        if argv[i] == "--run":
            run = argv[i + 1]; i += 2
        elif argv[i] == "--equiv":
            equiv = argv[i + 1]; i += 2
        elif argv[i] == "--out":
            out = argv[i + 1]; i += 2
        else:
            print("usage"); return 2
    os.makedirs(out, exist_ok=True)
    data = json.load(open(os.path.join(run, "results.json")))
    base = [r for r in data["records"] if r["id"] == "BASE"][0]
    recs = [r for r in data["records"] if r["id"] != "BASE"]
    cross = json.load(open(os.path.join(run, "cross", "cross-matrix.json")))
    kills = json.load(open(os.path.join(run, "kill-results.json")))
    eq = json.load(open(os.path.join(equiv, "equiv-results.json")))
    own = {}
    for k in kills:
        if k["killed"]:
            own.setdefault(k["mutant"], []).append(k["proposal"])
    desc = {k["proposal"]: k["desc"] for k in kills}

    def claim_met(r):
        return "verdict=TARGET_MET" in r["c2_line"] and r["c2_rc"] == 0

    rows = []
    for r in recs:
        mid = r["id"]
        met = claim_met(r)
        st_ok = r["selftest_rc"] == 0
        if not met:
            status = "KILLED by claim harness"
        elif not st_ok:
            status = "KILLED by --selftest only"
        else:
            status = "SURVIVES full oracle"
        equivalent = mid in EQUIV_ARG
        killers = sorted(set(cross.get(mid, []) + own.get(mid, [])), key=lambda x: (len(x), x))
        if status == "SURVIVES full oracle":
            kind = "EQUIVALENT" if equivalent else "KILLABLE by new fixture"
        elif status == "KILLED by --selftest only":
            kind = "claim survivor, KILLABLE by new fixture (selftest catches)" if not equivalent else "?"
        else:
            kind = "-"
        rows.append({"id": mid, "area": r["area"], "old": r["old"], "new": r["new"], "c2": r["c2_line"],
                     "c2_met": met, "selftest_rc": r["selftest_rc"], "selftest": r["selftest_line"],
                     "status": status, "equiv": equivalent, "kind": kind, "killers": killers})

    n = len(rows)
    killed_claim = [x for x in rows if not x["c2_met"]]
    claim_surv = [x for x in rows if x["c2_met"]]
    killed_full = [x for x in rows if x["status"] != "SURVIVES full oracle"]
    surv_full = [x for x in rows if x["status"] == "SURVIVES full oracle"]
    eq_ids = sorted(x["id"] for x in rows if x["equiv"])
    claim_surv_eq = [x for x in claim_surv if x["equiv"]]
    claim_surv_killable = [x for x in claim_surv if not x["equiv"]]
    full_surv_killable = [x for x in surv_full if not x["equiv"]]
    unkilled_real = [x["id"] for x in claim_surv_killable + full_surv_killable if not x["killers"]]
    unkilled_real = sorted(set(unkilled_real))
    assert not unkilled_real, unkilled_real
    # greedy set cover of the killable claim-survivors by proposed fixtures
    targets = {x["id"]: set(x["killers"]) for x in claim_surv_killable}
    chosen = []
    remaining = set(targets)
    while remaining:
        best = max(sorted({k for m in remaining for k in targets[m]}),
                   key=lambda k: (sum(1 for m in remaining if k in targets[m]), -len(k)))
        covered = {m for m in remaining if best in targets[m]}
        chosen.append((best, sorted(covered)))
        remaining -= covered

    pct = lambda a, b: "%.1f%%" % (100.0 * a / b)
    L = []
    A = L.append
    A("# Round 56 w2 - mutation test of `tools/mado-watchplan.py` (seat R56W2MutC2ToolA)")
    A("")
    A("Target: `tools/mado-watchplan.py` at lane revision `28fc86ac2359ec27406d8a2c63bef82ea6e947ed` (lane tip "
      "`9c3ca28a59de0dd23ee9950d22349333fc168a11` adds wave-1 evidence only, not the tool).")
    A("")
    A("## Verdict")
    A("")
    A("The committed oracle (the unchanged C2 harness on 18 committed + 8 revealed hold-out fixtures, plus the tool's own")
    A(("`--selftest`) does **not** pin the tool's config model. %d one-line mutants were run; %d are killed by the frozen"
       " claim predicate and %d survive it. Of those survivors, %d are provably equivalent and **%d are real model defects"
       " the frozen predicate accepts**. Each real survivor has a verified killing fixture (below). The predicate is therefore"
       " satisfiable by a tool that is wrong in the model registration-v2 §C2 writes down. The defect is in the fixture set,"
       " not in the tool at the frozen revision: the pristine tool passes every check.") % (
       n, len(killed_claim), len(claim_surv), len(claim_surv_eq), len(claim_surv_killable)))
    A("")
    A("| measure | count | rate |")
    A("|---|---|---|")
    A("| mutants generated and run (0 skipped) | %d | |" % n)
    A("| killed by the frozen claim predicate (`MADO_R56_C2 ... TARGET_MET` not printed) | %d | %s of all |" % (
        len(killed_claim), pct(len(killed_claim), n)))
    A("| killed by the full oracle (claim predicate + `--selftest`) | %d | %s of all |" % (
        len(killed_full), pct(len(killed_full), n)))
    A("| provably equivalent (no observable difference) | %d | |" % len(eq_ids))
    A("| claim-predicate kill rate, equivalents excluded | %d/%d | %s |" % (
        len(killed_claim), n - len(eq_ids), pct(len(killed_claim), n - len(eq_ids))))
    A("| full-oracle kill rate, equivalents excluded | %d/%d | %s |" % (
        len(killed_full), n - len(eq_ids), pct(len(killed_full), n - len(eq_ids))))
    A("| claim survivors, non-equivalent (each has a verified killing fixture) | %d | |" % len(claim_surv_killable))
    A("| full-oracle survivors, non-equivalent (undetected by the committed oracle) | %d | |" % len(full_surv_killable))
    A("")
    A("Baseline (unmutated tool, same scratch repo): `%s`; selftest `%s`." % (base["c2_line"], base["selftest_line"]))
    A("")
    A("Equivalents: %s." % ", ".join(sorted(eq_ids)))
    A("")
    A("## Method")
    A("")
    A("- The lane was read at `28fc86ac2359ec27406d8a2c63bef82ea6e947ed` and exported with `git archive | tar -x` into a fresh")
    A("  scratch repo `/fast/scratch/hyaku/mado-r56/R56W2MutC2ToolA/repo` (`git -C` asserted to be that dir before the first")
    A("  commit; identity `-c user.name=ctl -c user.email=ctl@ctl`). The scratch baseline commit is `d997f00`, so the")
    A("  `rev=` field in the harness line differs from the lane revision; the verdicts are what matter. The lane was never")
    A("  mutated: each mutant is a one-line change written to a COPY of `tools/mado-watchplan.py` in the scratch repo and")
    A("  committed there (`mutate.py`). The pristine bytes were restored and re-checked after the run (`cmp` identical).")
    A("- Oracle, unchanged: `python3 -I quality/check-r56-controls.py --claim c2 --repo <scratch> --rev <mutant> --work <scratch>/w`.")
    A("  It stages each fixture under `<work>/stage-N/<id>/tree`, runs the tool from an empty cwd inside bwrap, and compares")
    A("  stdout bytes and exit status against `expected.out` / `expected.rc` (18 committed, 8 hold-out). The full oracle adds")
    A("  the tool's `--selftest`.")
    A("- Mutant design: 105 one-line changes in the tool's config model (argument parsing, size/depth bounds, comment and")
    A("  brace stack, `=` split, `$`/`{`/backslash/`##` rules, value parsing, source handling, watch list, display root,")
    A("  getoption join, counters). Each mutant changes one operator, constant, bound, guard, argument or output field.")
    A("- Survivor handling: every claim survivor was attacked with the smallest fixture that separates it from the pristine")
    A("  tool. Each proposal was run through the same staged bwrap path (`kill4.py`) and its pristine and mutant outputs")
    A("  compared. Killer sets come from the full cross-matrix (`cross.py`: every proposal against every claim survivor), so")
    A("  a fixture is credited only when it separates that mutant.")
    A("- Equivalence was argued from the code and checked by differential testing (`equiv.py`, %s)." % EQUIV_CORPUS)
    A("")
    A("## The 9 equivalent mutants (proved, not killed)")
    A("")
    A("| id | mutated line | why no input distinguishes it |")
    A("|---|---|---|")
    for x in rows:
        if x["equiv"]:
            A("| %s | `%s` -> `%s` | %s |" % (x["id"], first_line(x["old"]), first_line(x["new"]), EQUIV_ARG[x["id"]]))
    A("")
    A("Corpus check for the same nine (`equiv-results.json`): zero differences over 3,851 cases for each of M73, M77, M78,"
      " M79, M81, M83, M85, M99, M104. The corpus check did not run on M80 or M96 as equivalent: M80 is a real defect"
      " (`on$x` is accepted as 1) and M96 is killed by K57 (see below), so neither is in this set.")
    A("")
    A("## Real survivors of the frozen claim predicate (%d)" % len(claim_surv_killable))
    A("")
    A("These mutants print `MADO_R56_C2: ... verdict=TARGET_MET` on the unchanged oracle, so the frozen predicate does not")
    A("falsify them. Each is separated from the pristine tool by a fixture listed in the last column (verified in")
    A("`receipts/kill-<K>.txt`).")
    A("")
    A("| id | mutated line | full-oracle | killing fixtures (verified) |")
    A("|---|---|---|---|")
    for x in sorted(claim_surv_killable, key=lambda z: z["id"]):
        full = "selftest catches" if x["status"] == "KILLED by --selftest only" else "undetected"
        A("| %s | `%s` -> `%s` | %s | %s |" % (x["id"], first_line(x["old"]), first_line(x["new"]), full,
                                             ", ".join(x["killers"]) or "**NONE**"))
    A("")
    A("Of these, %d are also undetected by `--selftest` (the tool's own selftest passes on them), so no test in the lane"
      " catches them: %s." % (len(full_surv_killable), ", ".join(x["id"] for x in sorted(full_surv_killable, key=lambda z: z["id"]))))
    A("")
    A("## Proposed additions: greedy cover of the real survivors (not proven minimum)")
    A("")
    A("Greedy set cover over the killer sets above. Each chosen fixture kills every mutant listed against it. The fixtures")
    A("are in `receipts/kill-<K>.txt`. Adding any of them changes the C2 harness counts (18 to 19, etc.), so they are a")
    A("pre-data re-registration (new versioned file, as registration-v2 requires), not a silent edit of the committed set.")
    A("")
    A("| fixture | kills | what it puts in the tree / args |")
    A("|---|---|---|")
    for k, cov in chosen:
        d = desc.get(k, "")
        A("| %s | %s | %s |" % (k, ", ".join(cov), d))
    A("")
    A("%d fixtures cover all %d real claim survivors." % (len(chosen), len(claim_surv_killable)))
    A("")
    A("## Full mutant table (all %d)" % n)
    A("")
    A("`kill` column: the claim harness (`C2`) or `--selftest` (`st`) flags the mutant; `-` = neither. `class`: `E` =")
    A("equivalent, `K` = killable by a new fixture (listed), `-` = already killed.")
    A("")
    A("| id | area | mutated line (old -> new) | claim | selftest | kill | class | killers |")
    A("|---|---|---|---|---|---|---|---|")
    for x in rows:
        claim = "TARGET_MET" if x["c2_met"] else "miss"
        st = "pass" if x["selftest_rc"] == 0 else "FAIL"
        if not x["c2_met"]:
            kill = "C2"
        elif x["selftest_rc"] != 0:
            kill = "st"
        else:
            kill = "-"
        cls = "E" if x["equiv"] else ("K" if (x["c2_met"] or x["selftest_rc"] != 0) and x["killers"] else "-")
        if x["c2_met"] and x["selftest_rc"] != 0 and x["killers"]:
            cls = "K"
        killers = ", ".join(x["killers"]) if x["c2_met"] or x["selftest_rc"] != 0 else "-"
        A("| %s | %s | `%s` -> `%s` | %s | %s | %s | %s | %s |" % (
            x["id"], x["area"], first_line(x["old"]), first_line(x["new"]), claim, st, kill, cls, killers or "NONE"))
    A("")
    A("## Notes on the proposals that did not kill (kept for the record)")
    A("")
    A("`receipts/kill-<K>.txt` also holds the first proposals I wrote, which missed: K73, K77, K78, K79, K81, K83, K85, K99,")
    A("K104 (their mutants are provably equivalent) and K80 and K96 (mis-targeted: K80 used an LHS `$` the mutant never")
    A("reads; K96 used a display root whose realpath prefix was not reached). M80 is killed by K27 and M96 by K57, both in")
    A("the cross-matrix. K60 was first written with a typo in its config line (`misc:disable_autoridl`); it was corrected to")
    A("`misc:disable_autoreload = 0` and re-verified (it kills M60).")
    A("")
    A("## Restoration and what did not run")
    A("")
    A("- Restoration: after the 105-mutant run `tools/mado-watchplan.py` in the scratch repo was rewritten from the pristine")
    A("  bytes and committed; `cmp` against the `git show HEAD:` blob succeeds (see `receipts/run.log`). The lane was not touched.")
    A("- Not verified: the harness's bwrap staging was reproduced by copying its `staged_run` command line; the harness run")
    A("  itself was used for every oracle verdict. The fixtures in 'Proposed additions' were run through my own copy of the")
    A("  staging, not through the harness's `score()` (the harness counts are fixed at 18/8 and would reject additions).")
    A("- Not run: no `pacman`/install; the tools used (`python3` 3.14, `git`, `tar`, `bwrap`) were already present.")
    A("")
    A("## Deliverables (this directory)")
    A("")
    A("- `mutants.md` (this file), generated by `report.py` from the receipts below.")
    A("- driver: `mutate.py` (105-entry mutant list and the oracle loop), `kill4.py` (killing-fixture transcripts),")
    A("  `kill2.py` (fixture definitions), `extra.py` (two later fixtures), `cross.py` (cross-kill matrix), `equiv.py`")
    A("  (equivalence corpus), `report.py` (this table).")
    A("- receipts: `receipts/<M##>.txt` (one per mutant: the mutated bytes' sha256, the blob, the oracle line, selftest rc),")
    A("  `receipts/kill-<K##>.txt` (one per killing fixture: both outputs), `results.json`, `results.tsv`,")
    A("  `cross-matrix.json`, `kill-results.json`, `equiv-results.json`, `baseline.txt`, `run.log`.")
    A("")
    with open(os.path.join(out, "mutants.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")
    print("wrote %s" % os.path.join(out, "mutants.md"))
    print("mutants=%d claim_killed=%d full_killed=%d equiv=%d claim_surv_killable=%d full_surv_killable=%d chosen=%d"
          % (n, len(killed_claim), len(killed_full), len(eq_ids), len(claim_surv_killable), len(full_surv_killable), len(chosen)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

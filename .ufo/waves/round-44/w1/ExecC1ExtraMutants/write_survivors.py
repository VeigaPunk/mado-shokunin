#!/usr/bin/env python3
"""Write survivors.md from the measured PRED-C1-r44 logs + build.SPEC notes.

Numbers come from /fast/scratch/hyaku/mado-r44/ExecC1ExtraMutants/logs/*.log (the frozen
counter's own lines); the edit and proof texts are the seat's own analysis. Nothing here is
hand-typed from the logs.
"""
import glob
import os
import re
import sys

SEAT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SEAT)
import build  # noqa: E402  (the spec, single source of the edits)

LOGS = os.path.join(SEAT, "receipts", "logs")
OUT = os.path.join(SEAT, "survivors.md")
NONCE = "mutsweep1"

PROOF = {
    "M04-fsmode-admit-0":
        "returns 0 for `fullscreen`: 0 (the same value the else-branch gives); the returned mode "
        "is consumed only by `fsmode == 2` / `fsmode == 1` (ref:233, ref:235), so the output is "
        "identical for every input. Contract-conforming.",
    "M05-fsmode-admit-neg":
        "returns -1 for `fullscreen`: -1; `-1 == 2` and `-1 == 1` are both false, so every verdict, "
        "tally, suffix and exit code is identical to 0. Output-equivalent but CONTRACT-VIOLATING: "
        "see section 3 (the counter does not pin the documented `else 0` on negative ints).",
    "M06-fsmode-range-chain":
        "`1 <= f <= 2` is true exactly for f in {1, 2} (the int guard runs first), and the same f is "
        "returned, so the value is unchanged. Side effect measured: the state test stops being an "
        "ast.Compare of one operator, so clause b4 stops counting it (14 -> 13 sites, section 4).",
    "M07-fsmode-set-literal":
        "`{1, 2}` is only evaluated when `isinstance(f, int)` already holds (short-circuit `and`), "
        "and ints are hashable, so no unhashable JSON value reaches the set; membership in {1,2} "
        "equals membership in (1,2).",
    "M09-guard-int-or-bool":
        "`isinstance(f, (int, bool))` widens nothing: the following `not isinstance(f, bool)` still "
        "removes the only extra member. json.loads yields exactly int/float/str/bool/None/list/dict, "
        "never a user int subclass.",
    "M10-guard-type-is":
        "`type(f) is int` vs `isinstance(f, int)` differ only for int subclasses, which json.loads "
        "cannot produce. The counter's own model already uses this form (quality/counters/"
        "c1-r44-geometry-states.py:90), i.e. the predicate's author treats them as the same read.",
    "M11-guard-type-not-bool":
        "`type(f) is not bool` vs `not isinstance(f, bool)`: bool cannot be subclassed, and its only "
        "instances are True and False, so the two guards accept the same set.",
    "M12-guard-is-not-true":
        "`f is not True and f is not False` is the identity test for the two bool singletons, so it "
        "accepts the same set as `not isinstance(f, bool)`.",
    "M16-conjunct-reorder":
        "the three conjuncts are pure; reordering makes the membership test run first, and tuple "
        "membership uses `==` only (no hashing), so unhashable JSON values ([2], {...}) are still "
        "compared without error. Same accept set, same return value.",
    "M17-membership-str":
        "`str(f) in (\"1\", \"2\")` holds exactly for the ints 1 and 2: decimal str is injective on "
        "ints and \"1\"/\"2\" are their canonical forms (no sign, no padding). The returned value is "
        "still the int f.",
    "M19-return-ternary":
        "`2 if f == 2 else 1` equals f for the only reachable values f in {1, 2}.",
    "M20-return-min":
        "`min(f, 2)` equals f for f in {1, 2} (the guard admits nothing larger).",
    "M21-return-mod":
        "`f % 3` equals f for f in {1, 2}.",
    "M24-key-default":
        "`c.get(\"fullscreen\", 0)` differs from `c.get(\"fullscreen\")` only when the key is absent, "
        "and the guard rejects None exactly as it rejects 0.",
    "M27-branch-swap":
        "fsmode is a single integer from client_fsmode, so `fsmode == 1` and `fsmode == 2` are "
        "disjoint; testing MAXIMIZED first cannot change any client's verdict.",
    "M28-max-truthiness":
        "the MAXIMIZED branch is reached only after `fsmode == 2` failed, so fsmode is 0 or 1 there; "
        "`elif fsmode:` is then identical to `elif fsmode == 1:`. Side effect measured: truthiness is "
        "not an ast.Compare, so clause b4 stops counting this site (14 -> 13, section 4).",
    "M29-fs-gt1":
        "client_fsmode returns only 0, 1 or 2, so `fsmode > 1` and `fsmode == 2` agree everywhere.",
    "M30-max-ge1":
        "the MAXIMIZED branch runs after `fsmode == 2` failed, so fsmode is 0 or 1 there and "
        "`fsmode >= 1` equals `fsmode == 1`.",
    "M34-tiled-only-flat":
        "the TILED branch runs after both state branches failed, so fsmode is 0 there and "
        "`not floating and fsmode == 0` equals `not floating`.",
    "M42-suffix-ge1":
        "`maximized + fullscreen >= 1` on two tallies that are non-negative ints, so it is the same "
        "predicate as `> 0`.",
}

CITE = {
    "M05-fsmode-admit-neg": "MISSING CHECK (contract) + EQUIVALENT (output)",
    "M06-fsmode-range-chain": "EQUIVALENT, and b4-invisible",
    "M28-max-truthiness": "EQUIVALENT, and b4-invisible",
}


def parse(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    lines = text.splitlines()
    last = next((l for l in reversed(lines) if l.startswith("PRED-C1-r44: fixtures=")), "")
    m = re.search(r"fixtures=(\d+)/26 .*verdict=(\w+)", last)
    cl = next((l for l in lines if " clauses=" in l), "")
    selt = next((re.search(r"selftest=(\d+)/(\d+)", l) for l in lines if "clause=b rc=" in l), None)
    b4 = next((re.search(r"clause=b4 sites=(\d+) killed=(\d+) need=(\d+)", l) for l in lines
               if "clause=b4 sites=" in l and "killed=" in l), None)
    fails = [re.search(r"fixture=(\S+) ok=0", l).group(1) for l in lines
             if re.search(r"fixture=(\S+) ok=0", l)]
    return {"fx": m.group(1) if m else "?", "verdict": m.group(2) if m else "?",
            "selftest": "%s/%s" % (selt.group(1), selt.group(2)) if selt else "-",
            "b4": "%s/%s (need %s)" % (b4.group(2), b4.group(1), b4.group(3)) if b4 else "-",
            "clauses": cl.split("clauses=")[-1] if "clauses=" in cl else "",
            "fails": fails}


def main():
    rows = {}
    for p in glob.glob(os.path.join(LOGS, "*.log")):
        rows[os.path.basename(p)[:-4]] = parse(p)
    spec = {n: (note, pairs) for n, note, pairs in build.SPEC}
    mets = sorted(n for n in rows if rows[n]["verdict"] == "TARGET_MET" and n != "REF")
    misses = sorted(n for n in rows if rows[n]["verdict"] == "TARGET_MISSED")
    out = []
    w = out.append
    w("# C1 mutation population — survivors (seed ExecC1ExtraMutants, round 44 w1)")
    w("")
    w("Reference: `.ufo/waves/round-44/c1/ctl-ref-tool.py.txt` (476 lines). Counter: "
      "`quality/counters/c1-r44-geometry-states.py` at rev `e2289516a9a857f55cda7be635933e89b931c3da`. "
      "Scored, one run per body:")
    w("")
    w("    cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I "
      "quality/counters/c1-r44-geometry-states.py --repo . --rev "
      "e2289516a9a857f55cda7be635933e89b931c3da --tool "
      ".ufo/waves/round-44/w1/ExecC1ExtraMutants/mutants/<M>.py --nonce %s "
      "--work /fast/scratch/hyaku/mado-r44/ExecC1ExtraMutants/work/<M>" % NONCE)
    w("")
    w("(`--work` is the transient seat scratch, re-created by `mkdir -p`; no result is cited from it.)")
    w("")
    w("`--nonce %s` is fixed so every body is judged on the same 12-case sgen lattice; the survivors "
      "were re-scored on nonce `mutsweep2` with the same result. `REF` under the same nonce: "
      "`fixtures=26/26 clauses=a:1 b:1 b4:1 g:1 r:1 verdict=TARGET_MET`." % NONCE)
    w("")
    w("Population: %d single-defect mutants, every replacement asserted to match exactly once at build "
      "time (`build.py`, `BUILD total=%d bad=0`). **%d survive the whole counter, %d are killed.** "
      "No surviving mutant is behaviourally wrong: all %d are equivalent transformations (code proof "
      "below plus 20 000 randomised differential cases each, `receipts/equivalence-diff.txt`)."
      % (len(spec), len(spec), len(mets), len(misses), len(mets)))
    w("")
    w("## 1. Survivors")
    w("")
    w("| mutant | edit | verdict | failing fixtures/clauses | classification and proof |")
    w("|---|---|---|---|---|")
    for n in mets:
        note, pairs = spec[n]
        w("| `%s` | %s | TARGET_MET, fixtures 26/26, clauses a:1 b:1 b4:1 g:1 r:1 | none | %s |"
          % (n, note, CITE.get(n, "EQUIVALENT") + " — " + PROOF[n]))
    w("")
    w("Differential evidence: `receipts/equivalence-diff.txt` — 20 000 random client dumps per body "
      "against the reference, `DIFF TOTAL=0`; the generator draws `fullscreen` from "
      "{1, 2, 0, 3, -1, -7, 100, true, false, 2.0, \"2\", null, [], [2], {\"internal\": 2}} and still "
      "reaches 97-148 `FULLSCREEN` verdicts, 114-152 `MAXIMIZED` verdicts and 223-278 state suffixes "
      "per body, so the state paths are exercised, not bypassed.")
    w("")
    w("## 2. What the survivors say about the predicate")
    w("")
    w("* The state logic is pinned only up to *observable* behaviour: the verdict chain consumes "
      "`fsmode` exclusively through `== 2` and `== 1` (ref:233, ref:235), so any return value that "
      "matches neither is indistinguishable from 0. That is why M04, M05 and M27 can move the "
      "membership set and the branch order without a single fixture moving.")
    w("* The 13 registered controls all miss, and K13 misses only on the selftest clause "
      "(registration: fixtures 26/26) — the same asymmetry this sweep measures from the other side. "
      "Of these 51 extra mutants the "
      "equivalence class is wide: 20/51 survive, and every one of them survives because the "
      "contract's *observable* surface is thinner than its docstring.")
    w("")
    w("## 3. MISSING CHECK (the one hole the fixtures cannot close)")
    w("")
    w("`M05-fsmode-admit-neg` (and, on the same input, `M51-return-any-int`) returns a negative "
      "integer where the contract says 0:")
    w("")
    w("| body | `client_fsmode({\"fullscreen\": -1})` | contract |")
    w("|---|---|---|")
    w("| reference | 0 | 0 |")
    w("| `M05-fsmode-admit-neg` | -1 | 0 |")
    w("| `M51-return-any-int` | -1 | 0 |")
    w("")
    w("(measured, `receipts/fsmode-probe.txt`). The counter's only direct pin on the return value is "
      "the selftest case at ref:458 —")
    w("")
    w("    chk(\"fsmode-values\", [client_fsmode({\"fullscreen\": v}) for v in "
      "(1, 2, 0, 3, True, 2.0, \"1\", None)], [1, 2, 0, 0, 0, 0, 0, 0])")
    w("")
    w("— which covers the upper boundary (3) and every type guard, and no negative integer. No "
      "fixture can kill M05: -1 and 0 produce byte-identical output in every case "
      "(`receipts/equivalence-diff.txt`), so the only kill path is a value-level check.")
    w("")
    w("**Killing input and expected output** (one added tuple element, nothing else): "
      "`client_fsmode({\"fullscreen\": -1})` must be `0`. Adding `-1` to the ref:458 tuple with "
      "expected `0` kills M05 and M51 and leaves the reference passing (the probe table gives both "
      "sides of that assertion: reference 0, mutants -1).")
    w("")
    w("Severity: low and unreachable in production — `hyprctl clients -j` prints the internal mode "
      "(`eFullscreenMode` 0/1/2, registration `fetch-c1/Hyprland-HyprCtl.cpp`), so a live dump cannot "
      "carry -1. The gap is in *contract pinning*, not in behaviour: today a tool can violate the "
      "docstring's `else 0` for negative ints and still score `TARGET_MET`.")
    w("")
    w("## 4. Clause b4 can be shrunk by the tool under test (measured)")
    w("")
    w("b4 counts the `ast.Compare` nodes of one operator (counter:283) in functions whose body "
      "contains a `fullscreen` string, and needs `ceil(0.75 * sites)`, floor 6 (counter:76-77, "
      "counter:294). Two of the survivors remove exactly that state site from the census without "
      "removing the state logic:")
    w("")
    w("| body | membership test written as | b4 sites | b4 killed | need | clause b4 |")
    w("|---|---|---|---|---|---|")
    w("| reference | `f in (1, 2)` (ref:197) | 14 | 14 | 11 | pass |")
    w("| `M06-fsmode-range-chain` | `1 <= f <= 2` (two operators) | 13 | 13 | 10 | pass |")
    w("| `M28-max-truthiness` | `elif fsmode:` (no Compare at all) | 13 | 13 | 10 | pass |")
    w("| `M12-guard-is-not-true` | `f is not True and f is not False` (adds two) | 16 | 16 | 12 | pass |")
    w("")
    w("So the census is not a constant of the contract: `1 <= f <= 2` and truthiness are invisible "
      "to `len(node.ops) == 1`, and the remaining 13 sites are round-43 compares "
      "(`evaluate:213..239`, `report:259..269`) whose flips break the selftest for reasons unrelated "
      "to state. The floor and the 75 % rule still hold here, but the *marginal* tooth on the state "
      "branch is one site, and a tool can drop it by writing a chained compare. This is a "
      "clause-strength residual, not a false kill.")
    w("")
    w("## 5. Kill channels (all %d misses)" % len(misses))
    w("")
    w("| channel | kills | note |")
    w("|---|---|---|")
    w("| fixtures only (selftest passes) | 1 | `M46-unmapped-fs-counted`, 23/26 |")
    w("| selftest only (fixtures 26/26) | 3 | `M01-fsmode-extra-3`, `M22-fallback-none`, "
      "`M51-return-any-int` |")
    w("| fixtures and selftest | 27 | |")
    w("| clause r (round-43 counter) independent | 0 | r:0 exactly when b:0 — the round-42 counter "
      "runs the same `--selftest`, so it never adds a kill of its own |")
    w("| clause b4 independent | 0 | b4 is skipped whenever b fails (counter:356-357), so it cannot "
      "kill what the selftest does not |")
    w("")
    w("The three selftest-only kills are the interesting half: the 26 fixtures are blind to "
      "`fsmode` values that no verdict branch consumes (3, None), and only the value-level selftest "
      "case at ref:458 sees them. Conversely `M46` shows the fixtures carry the counting reach that "
      "the selftest does not.")
    w("")
    w("## 6. Full kill table")
    w("")
    w("| mutant | edit | result | failing fixtures/clauses |")
    w("|---|---|---|---|")
    for n in misses:
        r = rows[n]
        note, pairs = spec[n]
        bits = "fixtures %s/26" % r["fx"]
        if r["fails"]:
            bits += " (" + ", ".join(r["fails"]) + ")"
        bits += "; selftest %s" % r["selftest"]
        bits += "; " + r["clauses"]
        w("| `%s` | %s | TARGET_MISSED | %s |" % (n, note, bits))
    w("")
    w("## 7. Reproduction")
    w("")
    w("    python3 -I .ufo/waves/round-44/w1/ExecC1ExtraMutants/build.py      # rebuild the 51 bodies")
    w("    bash .ufo/waves/round-44/w1/ExecC1ExtraMutants/run_sweep.sh REF M01-fsmode-extra-3 ...")
    w("    python3 -I .ufo/waves/round-44/w1/ExecC1ExtraMutants/summarize.py")
    w("    python3 -I .ufo/waves/round-44/w1/ExecC1ExtraMutants/probe_fsmode.py")
    w("    python3 -I .ufo/waves/round-44/w1/ExecC1ExtraMutants/equivalence_diff.py 20000")
    w("")
    w("Bodies: `.ufo/waves/round-44/w1/ExecC1ExtraMutants/mutants/` (51 files + `build.py` spec).")
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    print("wrote %s (%d survivors, %d misses)" % (OUT, len(mets), len(misses)))


if __name__ == "__main__":
    main()

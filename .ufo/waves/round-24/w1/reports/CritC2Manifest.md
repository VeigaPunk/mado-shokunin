# CritC2Manifest — C2 manifest row-by-row attack (round 24, wave 1)

Scope: `c2/manifest.json` (`sha256:e02c76d1adb4f523fccf11e1e5ad4cd40f6d0da460b75c7f811b66306e188a02`) and
`c2/count.py` (`sha256:a280950195d647b0be992122a14cc96535e6de24a8bc40d92683351af7ffe4e8`) at
base `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122`, against each SCORECARD capability row's own claim in
`git show 8e5d9369:SCORECARD.md`. No lane file was edited except this report; no tools were installed or
updated; every command was read-only (mutations only under `/tmp` and
`/fast/scratch/hyaku/mado-r24/crit-sandbox`); every process I started has finished or was killed.

Verdict in one line at the end. Short version: the base `1/12` is a materially true row-8 failure, but the
manifest is not a demonstration of the twelve claims — eleven of twelve rules are token/quantity matches that a
non-capability (or a stubbed meter) satisfies, two rules measure the guarded object instead of the claimed
capability, three capability rows are outside the counted population, and the counted `0/12` target is reachable
with two uncommitted edits to measurement scripts that live outside the REV tree.

## Cross-cutting findings

### F0 — the counted population is 12, but base SCORECARD has 15 capability rows

Observation. Enumerating every table at base whose header first cell is `Capability`, and dropping the
`— none yet —` placeholder, gives **15** named capability rows. The counter's parser keeps **12**:

```
SCORECARD.md:308  Capabilities (round 12)                              sources registry
SCORECARD.md:309  Capabilities (round 12)                              verdict gate (live + file plane)
SCORECARD.md:310  Capabilities (round 12)                              hermetic self-test
SCORECARD.md:311  Capabilities (round 12)                              mutation regression with re-cut
SCORECARD.md:437  Sources and demonstrated repertoire                  source-fragment collision screen   <-- not counted
SCORECARD.md:438  Sources and demonstrated repertoire                  digest-pinned frozen regression    <-- not counted
SCORECARD.md:782  Demonstrated capability                              finite declared-action classifier  <-- not counted
SCORECARD.md:919  Capabilities (round 17)                              post-hoc transcript tripwire
SCORECARD.md:1020 Capabilities (round 18)                              tripwire frozen replay (gate entry)
SCORECARD.md:1158 Capabilities (round 19)                              landedness check
SCORECARD.md:1342 Capabilities (round 20)                              tripwire evidence marker
SCORECARD.md:1343 Capabilities (round 20)                              harness fail-closed check
SCORECARD.md:1409 Capabilities (round 20, attempt 2; append-only)      tripwire reached-body sweep
SCORECARD.md:1410 Capabilities (round 20, attempt 2; append-only)      detector removal-side guard
SCORECARD.md:1464 Capabilities demonstrated this round                 artifact-only assessment integrity
```

The three misses are not retired: base SCORECARD's retirement sections say `none retired` / `None.`
(`:216-218`, `:325`), and all three capabilities' instruments are present at base
(`.ufo/waves/round-13/w1/reports/MistakeFix.py`, `.ufo/waves/round-13/frozen/verify.py` + `expected.json`,
`tools/mado-action-plan.py`, `.ufo/waves/round-16/frozen/`). All three still pass checks at
base (collision screen `MISTAKE_FIX_SELFTEST: PASS 25/25`; round-13 frozen verifier
`MADO_FROZEN_SELFTEST: 12/12 assertions passed`; action-plan `SELFTEST_SUMMARY: 52/52 passed` and
`MADO_PLAN: frozen_match`), so they were demonstrable and simply never re-demonstrated by C2.

Why it happens: `parse_scorecard` only collects tables under a heading matching
`^#{2,3} Capabilities\b` (`count.py:40`, `:80-105`), and the counter README states that narrower population
explicitly (`c2/README.md:20`). But the frozen predicate says "a capability named in a SCORECARD.md
**capability table** at REV" — no heading restriction. The manifest note's "the 12 SCORECARD capability-table
rows at base" is therefore false for the predicate as written.

Impact: three asserted capabilities can never produce a mismatch; C2's target can be met while they rot
[INFERENCE: the counter would only notice them if it parsed their tables or a manifest row named them].
Smallest safe correction (post-freeze, so a disposition, not an edit): either state the population as "tables
under a `Capabilities` heading" in the predicate and record the three as outside C2, or extend the parser to any
table whose first header cell is `Capability` and add one frozen row per omitted capability (which needs a fresh
control wave). Do not silently keep calling the narrower set "every capability table".

### F1 — rows 8, 10 and 11 execute working-tree meters that are not pinned to REV; C2 scores 0/12 at base with two uncommitted stub edits

Observation. The manifest runs rows 8, 10 and 11 as `{LANE}/.ufo/waves/round-20/...` (`{LANE}` = MADO_LANE
working tree, README `:10`, `:24`), while `requires` only checks the script's presence in `{TREE}`. The
executed bytes are therefore not the REV bytes, and nothing compares them. The no-harm guard is
`git diff --quiet 8e5d9369 <tip> -- tools/`, which does not cover `.ufo/`.

Counterexample (run, not inference). I cloned the lane to
`/fast/scratch/hyaku/mado-r24/crit-sandbox`, verified the committed meters at REV are byte-identical to the lane's
(`tw-precision.py` `sha256:bd3bdc23747a6d8f195e69528f532988202db4ab3476d141a8ff46871e42a8e7`,
`a2-guards.py` `sha256:414034d57ad38719df9489201c71fce7cb39edc29a5bf25ab971cbc57a4836ef`), then replaced only the
two working-tree copies with stubs that print the pinned tokens (`git status --porcelain`:
` M .ufo/waves/round-20/tw-precision.py`, ` M .ufo/waves/round-20/a2/a2-guards.py`). The frozen counter then ran:

```
$ MADO_LANE=/fast/scratch/hyaku/mado-r24/crit-sandbox \
  python3 -I .ufo/waves/round-24/c2/count.py 8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122
...
tripwire evidence marker        stated=works  observed=works  OK  exit=0
tripwire reached-body sweep     stated=works  observed=works  OK  exit=0
detector removal-side guard     stated=works  observed=works  OK  exit=0
...
mismatches=0/12 revision=8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122 ...
exit=0
```

At that same REV the honest base smoke is `1/12` (`c2/smoke/base-8e5d9369.txt`), and row 8's capability is
genuinely broken (below). So the C2 target `mismatches=0` is reachable with **no capability work, no SCORECARD
change and no `tools/` change** — only two uncommitted edits to measurement scripts. Also note row 7 returned
`exit=1` in this run versus `exit=0` in the base smoke, both scored `OK`: the observed status of the
git/network-reading rows is not a function of REV alone.

Impact: false provenance for 3 of 12 observed statuses; a direct gaming path to the target; the round's no-harm
guards do not close it.

Smallest safe correction: before executing a `{LANE}` meter, the counter compares the sha256 of the executed
bytes with `git -C {LANE} show {REV}:<same path>` and fails closed (observed `fails`, exit 125) on mismatch; the
same digest is printed in the receipt. This keeps the scripts' repo-root derivation working and pins what was
actually run.

### F2 — rows 1 and 4 depend on executables outside the lane and outside REV

Observation. Row 1 runs `{FLEET}/scripts/sources-census.sh`; row 4 runs the gate with
`MADO_VERIFY_HARNESS={FLEET}/tameshi-shokunin/tools/mutate-and-run.sh`. The harness is a separate repository
(`git -C …/tameshi-shokunin rev-parse --show-toplevel` → `/home/vgpnk/Projects/shokunin/tameshi-shokunin`), and
the census script is in the fleet tree, not in mado's REV. Neither is digest-pinned by the manifest. A fleet-side
change can flip either row between `works` and `fails` with no lane change (false pass or false fail). Both rows
passed at base, so this is a provenance/robustness defect, not a current miss.

Smallest safe correction: add the two fleet files' sha256 values to the manifest rule and verify them before the
run; if a fleet file differs, record the row as `fails` with a named provenance reason rather than scoring the
lane. (Alternative: run the census/harness from a snapshot committed inside the round.)

### F3 — the status table can zero a mismatch without repair; combined with row 8 it makes a correct fix unscoreable

Observation. `stated = status.get(name, "works")` (`count.py:279`) and `ok = in_population and stated == observed`
(`:319`). A `### Capability status (round 24 re-demonstration)` table is parsed into `status` (`:38-43`,
`:58-105`). I fed a two-row synthetic SCORECARD to `parse_scorecard`; it returned
`names ['tripwire evidence marker'] status {'tripwire evidence marker': 'fails'}`, so declaring `fails` at base
(where observed is `fails`) yields no mismatch.

That is defensible as calibration — the table must match observation. The defect is the interaction with row 8:
a *fixed* tool (L 18/18) is observed `fails` by the frozen rule (F1 and row 8 below prove it), so the truthful
status `works` produces a mismatch and the truthful `fails` produces none. The only ways to reach `0` at that
point are (a) write a false `fails`, (b) keep exactly one lead row failing (L 17/18), or (c) edit the meter
(F1) [INFERENCE from the observed rule evaluations and the status-table parse test; no 0/12 run with a false
`fails` was made]. C2's target therefore does not require the capability to work; it requires the table to agree with a rule
that can prefer the broken state.

Smallest safe correction: fix the row-8 rule to pass the working capability (row 8 below); then a truthful table
that reaches `0` means the capability works, and a declared `fails` is a real admission rather than the only
scoring path.

## Per-row findings

Legend: **L** = too lenient (a non-capability can pass), **S** = too strict (a working capability can fail),
**M** = measures something other than the row's claim. "Rule-pass" means the frozen `rule_ok` returned true on
the quoted output; for stubs I fed the exact frozen rule from `count.py` with `{REV}` substituted.

| # | Capability (SCORECARD line) | Finding | Demonstrated counterexample | Smallest safe correction |
|---|---|---|---|---|
| 1 | sources registry (:308) | L | zero-row registry prints `mado ok`, exit 0 | add a rows/mined floor (census mode) |
| 2 | verdict gate (:309) | L, M | 17-fail DIVERGED with boundary SKIP passes | run the live read-only form; require boundary row |
| 3 | hermetic self-test (:310) | L | `0/0` and `1/1` pass | floor N (REV count or ≥ 460) |
| 4 | mutation regression (:311) | L, S(partial) | one-line PASS stub passes; SETUP/re-cut untested; harness unpinned | exercise SETUP + pin harness digest |
| 5 | post-hoc tripwire (:919) | L | four one-case suites (`1/1` each) pass | floor per-dir totals / assert classes |
| 6 | frozen replay (:1020) | L | token `frozen_match` line passes; digest check not asserted | require non-empty inputs all `ok: true` + pinned verdict |
| 7 | landedness check (:1158) | L | `LOCAL_ONLY REV` stub passes; one hash only | two hashes with known distinct classes |
| 8 | tripwire evidence marker (:1342) | M, S, L | L 17/18 passes with a dropped lead row; L 18/18 fails; 15/18 fails at base | require L passed==total and P passed==total |
| 9 | harness fail-closed check (:1343) | L | six identical mode lines pass | assert the six mode names |
| 10 | reached-body sweep (:1409) | L, M | file-level recall; token stub passes; fixtures_rev/52 unasserted | assert fixtures_rev + per-file lead count |
| 11 | removal-side guard (:1410) | M, S, L | zeros required of the guarded object; counter reporting 1 drop fails; zero stub passes | demonstrate the counter at a known-bad revision; accept/justify nonzero |
| 12 | assessment integrity (:1464) | aligned | seal rejects truncation (exit 2); 20/20 pass | parse JSON; require pass==total==20 |

### 1. sources registry — SCORECARD.md:308

Claim: "Curate where mado learns: 39 opened, scoped-tier rows (mined/queued/rejected), study paths, search log;
every contract census command runs clean and every mined row joins to an entry that cites it."
Rule: `sources-census.sh validate --root {CENSUS_ROOT}`, exit 0, regex `^mado\tok\t`.

Finding: **too lenient**. `validate` emits `lane<TAB>ok<TAB>file` whenever there is no `E` finding
(`sources-census.sh:745`); warnings (`W`) and an `unlisted` lane do not change it, which matches the census
contract but not the curation claim. I built the counter's scratch-root layout over a copy of the base tree whose
`corpus/SOURCES.md` contains only `# Sources` and `## Registry` (zero rows):

```
$ bash scripts/sources-census.sh validate --root /tmp/r24census-root2
mado	unlisted	/tmp/r24census-root2/mado-shokunin
mado	ok	/tmp/r24census-root2/mado-shokunin/corpus/SOURCES.md
exit=0
```

The frozen rule returns true on that output. A registry emptied of all sources passes "runs clean". The base
tree passes honestly (`mado ok` plus seven `W04` warnings). The row's dated "39 opened" is correctly not pinned;
the defect is that *no* content or count is asserted at all.

Correction: add `census` mode to the rule and require `mado<TAB>rows<TAB>N` with N ≥ 1 (or the mined count), or
require at least one `E11`-clean mined row; the smallest is a rows floor alongside the existing `ok` line.

### 2. verdict gate (live + file plane) — SCORECARD.md:309

Claim: "Read-only verdict over the declared config plane and live hyprctl surfaces, exit 0/1/2, boundary check."
Rule: `bash tools/mado-verify.sh --no-live`, exit 0/1, regex `^MADO_VERIFY: (CLEAN|DIVERGED) \(`.

Finding: **too lenient and mismeasured**. The live hyprctl half is never run, and the rule accepts any verdict,
including a run where nearly everything fails and the boundary check is skipped. Demonstrated against an empty
HOME:

```
$ HOME=/tmp/r24fakehome bash tools/mado-verify.sh --no-live
...
gate      boundary.readonly               SKIP    no /tmp/r24fakehome/.config tree to hash
counts: pass=1 fail=17 unknown=7 skip=9 note=6
MADO_VERIFY: DIVERGED (17 fail, 7 unknown, 1 pass) — first fail: hypr.file.root (missing: ...)
exit=1
```

`rule_ok` is true on that output. The row's claim explicitly names the boundary check and the live surfaces; the
rule asserts neither. The manifest's `why` says the task fixes `--no-live` as the read-only form, but the gate's
own header (`tools/mado-verify.sh:22-24`) says the default live run is read-only too (hyprctl read verbs only, no
file written), so the read-only requirement does not force dropping the live plane.

Correction: run both forms (default read-only live plus file-plane) and require a verdict line from each, and
require `boundary.readonly` to be `PASS` (not `SKIP`). If the live plane must stay out of C2, narrow the claim to
the file plane.

### 3. hermetic self-test — SCORECARD.md:310

Claim: "269 assertions over isolated fixtures." Rule: `--selftest`, exit 0, regex
`^MADO_SELFTEST: (\d+)/\1 assertions passed$`.

Finding: **too lenient**. The gate prints `MADO_SELFTEST: $n_pass/$n_pass assertions passed` whenever
`n_fail=0` (`tools/mado-verify.sh:1875-1877`), so a suite with zero assertions prints `0/0` and a one-assertion
suite prints `1/1`. The frozen rule returns true for both:

```
row3 'MADO_SELFTEST: 460/460 assertions passed' True
row3 'MADO_SELFTEST: 0/0 assertions passed'   True
row3 'MADO_SELFTEST: 1/1 assertions passed'   True
```

Base actual is `460/460`. The manifest's `why` deliberately refuses to pin the dated 269; that is right, but it
left no floor at all.

Correction: require N to be at least the base count (460) or equal to the REV suite's own expected count, and
keep the N/N equality. This still refuses a rolled-back 269/269 suite and refuses a gutted one.

### 4. mutation regression with re-cut — SCORECARD.md:311

Claim: "Replays the 10-defect kill table against the gate's derived target; SETUP on a moved gate, re-cut via
the printed command." Rule: `--regression` with the fleet harness, exit 0, regex
`^MADO_REGRESSION: PASS \(case=mado-verify-hardened; `.

Finding: **too lenient/partial**. The one-line stub
`MADO_REGRESSION: PASS (case=mado-verify-hardened; target=deadbeef)` passes the frozen rule. In the tool, PASS is
printed only after the recorded table reproduces (`mado-verify.sh:2308`), so the token is a reasonable proxy for
the PASS branch — but the rule never exercises the claimed SETUP-on-a-moved-gate or re-cut branches. The harness
is an unpinned file in a separate repository (F2), so a missing/changed harness turns a working gate into
`fails` via SETUP (a false fail), and a compromised harness could fake kills.

Correction: add a second invocation with the target moved to force `MADO_REGRESSION: SETUP` and assert the printed
re-cut command, then restore and assert PASS; pin the harness digest (F2). [INFERENCE: the SETUP false-fail
follows from `exit_ok=[0]` plus the gate's SETUP path (`mado-verify.sh:2242-2267`); it was not run.]

### 5. post-hoc transcript tripwire — SCORECARD.md:919

Claim: "Classify commands issued in OMP session JSONL (bash; python eval `!`/`%%bash`/literal spawns; shell/python
heredocs) into host_mutation / package_query / live_probe with exit 0/1/2."
Rule: four `--selftest` dirs in sequence, exit 0, four lines `^SELFTEST_SUMMARY: (\d+)/\1 passed failed=\[\]$`.

Finding: **too lenient**. There is no floor on the case count and the four summaries need not come from four
meaningful suites. I built four directories each containing one trivial clean case and the real tool accepted
them:

```
CASE clean-reads ok
SELFTEST_SUMMARY: 1/1 passed failed=[]
(×4 directories, each exit 0)
```

and the frozen rule returns true on that combined output (`post-hoc transcript tripwire  rule_ok on four 1-case
suites: True`). Base actual totals are 9/9, 16/16, 33/33, 30/30. The tool prints a `SELFTEST_SCRIPT_SHA256` line,
but the rule compares it to nothing (and it is a tool digest, not a fixture digest), so fixture reduction is not
detected.

Correction: assert the four base totals (or at least ≥ 58 cases) and the class/exit coverage, e.g. require the
three class names and the `0/1/2` exit cases to appear in the summaries.

### 6. tripwire frozen replay (gate entry) — SCORECARD.md:1020

Claim: "Verify digests of committed incident transcript lines and compare the tripwire's verdict with a pinned
expected verdict (0 match / 1 mismatch / 2 tampered, unpinned or baseline error)."
Rule: exit 0/1, regex `^MADO_TRIPWIRE_FROZEN: frozen_(match|verdict_mismatch)$`, forbid `"ok": false`.

Finding: **too lenient**. The rule never positively asserts digest verification: a stub that prints
`MADO_TRIPWIRE_FROZEN: frozen_match` and exits 0 passes (verified), because the only digest guard is the absence
of `"ok": false`, which a non-verifying implementation simply does not print. Both verdicts are accepted, so a
tool that always reports `frozen_verdict_mismatch` also passes. The exit-2 tampered path is never exercised.
Base actual is `frozen_verdict_mismatch`, exit 1, five inputs all `"ok": true`, three extra findings — the rule
passes.

Correction: require a non-empty `inputs` list in which every entry is `"ok": true` (positive verification), and
assert the documented pinned verdict for the r18 corpus (round 19 records the expected mismatch); add the frozen
selftest for the tampered/exit-2 branch.

### 7. landedness check — SCORECARD.md:1158

Claim: "Say whether each cited lane hash is an ancestor of the live remote tip (LANDED/LOCAL_ONLY/MISSING)
without fetching or writing." Rule: one `(LANE, REV)` pair, exit 0/1, regex `^(LANDED|LOCAL_ONLY|MISSING) <REV>\b`.

Finding: **too lenient for a three-way claim**. One hash and any one of the three answers passes; a stub printing
`LOCAL_ONLY <rev>` and exiting 0 passes (verified). The receipts show the insensitivity directly: the same REV
returned `exit=0` in the base smoke and `exit=1` in the CtlC2DoNothing base run, and both were scored `OK`
(`c2/smoke/base-8e5d9369.txt`; `controls/CtlC2DoNothing.md`). The three-way classification is never
distinguished.

Correction: run at least two hashes with known distinct classes (a landed ancestor and a fabricated/known-missing
40-hex, or a local-only commit) and require both specific class lines; the row's own T1-T9 matrix already has
such cases.

### 8. tripwire evidence marker — SCORECARD.md:1342

Claim: "Tell an observed command from a lead (argv stated, executing body not visible) on every finding row,
and drop provably pure data." Rule: `tw-precision.py {REV}`, exit 0, regex requiring
`"commit": "{REV}"`, `"L": {"passed": 17, "total": 18}`, `"P": {"passed": 66, "total": 66}`.

Finding: **mismeasurement, too strict and too lenient at once**. The rule pins a dated quota instead of the
claim. Evidence, all run:

- Base actual (real meter): `L` 15/18, `P` 66/66, exit 0 → rule fails. The three failing L cases are
  `L-CasePureCrossCell-reset-clears-helper`, `L-CaseLeadsInvisible-reset-cleared-helper` and
  `L-AdoptW2-AdvHelperFn-b14`; all three want `exit 1` with `evidence: lead` and got `exit 0` with no findings.
  So the base mismatch is a **true** capability failure: the tool drops three lead rows.
- The row's own evidence revision `28c6837`: `L` 17/18, `P` 66/66 → rule passes, but the one failing L case is
  again `L-AdoptW2-AdvHelperFn-b14` (want lead, got none). The rule's pass state therefore includes a dropped
  lead row — directly contradicting "on every finding row". The row was overclaimed at entry.
- A fully fixed tool (`L` 18/18, `P` 66/66) is scored **fails** by the frozen rule (verified by substituting the
  L value in the real JSON: `row8 hypothetical fixed 18/18: False`).
- A stub printing the three anchors passes (`row8 token stub: True`).
- The regex also depends on the tool's `sort_keys=True` family order (`H,L,P,S,W`) and on compact nested
  objects; a formatting-only change would break it.

Consequence (F3): truthfully fixing the capability makes the row unscoreable; the frozen rule only passes a tool
that still drops exactly one lead case.

Correction: parse the JSON and require `"L": {"passed": N, "total": N}` (all lead cases pass) and
`"P": {"passed": M, "total": M}` with `commit == REV`, i.e. every lead row is told apart and no pure-data row is
reported. At base this remains a true fail; at a real fix it passes.

### 9. harness fail-closed check — SCORECARD.md:1343

Claim: "Show whether a stub/namespace harness runs its payload after any of six forced setup failures."
Rule: exit 0/1, at least six `^(FAIL_OPEN|FAIL_CLOSED) isolate\.sh mode=` lines plus
`^POSITIVE_CONTROL_OK isolate\.sh$`.

Finding: **too lenient**. Six occurrences need not be six distinct modes, and the mode value is unconstrained
after `mode=`. A stub printing the same line six times plus the positive control passes (verified:
`harness fail-closed check  rule_ok=True`). The real base run prints six distinct modes:
`mount-nonzero, unshare-refused, mount-noop, partial-arm, missing-target, missing-stub` (one each). A mutation
collapsing the mode list to one repeated entry would still pass while the claim "any of six forced setup
failures" is unmet.

Correction: add six `regex_all` entries naming the six modes (or assert six distinct mode values), keeping the
open/closed alternation per mode and the positive control.

### 10. tripwire reached-body sweep — SCORECARD.md:1409

Claim: "Report every visible body the executed text reaches but the call path does not follow (thread targets,
callbacks, decorators, closures, dunders, scheduled coroutines, recursion, past-depth helpers) as a `lead` row
instead of dropping it." Rule: `a2-guards.py {REV} --fixtures-rev 6a7d9ca`, exit 0, ` "recall_lost": 0` and
` "rev": "{REV}"`.

Finding: **too lenient/narrow**. `recall_lost` is file-level: it counts files where an older tool reported any
row and REV reports none (`a2-guards.py:128`: `any(rows(b,p) for b in BASES) and not rows("rev", p)`). A file
with two reached bodies where REV reports only one is not counted, so "every visible body" is not measured
[INFERENCE from `:128` plus the row's "every" wording; no two-lead fixture was constructed]. The
rule also does not assert `fixtures_rev` (the frozen population pin) or the row's `52` reached-body count; the
right population provenance is therefore unchecked, and a stub printing the two anchors passes (verified).
Base actual is `recall_lost: 0`, `fixtures_rev: 6a7d9ca…`, rev base — aligns with the claim on the frozen
population, but only at file granularity.

Correction: assert `"fixtures_rev": "6a7d9ca…"` and a per-file (or total) lead-row count against the population's
expected count, not just non-emptiness; parse the JSON rather than the two lines.

### 11. detector removal-side guard — SCORECARD.md:1410

Claim: "Count, for a tripwire change, the findings an older tool reported that the new one drops, the crash
flips and the pure-data rows, over frozen adversarial populations." Rule: the same `a2-guards.py` run as row 10,
requiring `recall_lost`, `crash_flip`, `vcs_fn`, `a2_mismatch`, `dup_rows` and `pure_rows` all `0`, plus
`"rev": "{REV}"`.

Finding: **mismeasures the claim; too strict and too lenient**. The row's capability is the counter's ability to
count drops, crash flips and pure rows. The rule instead requires the *guarded revision* to be clean (all
zeros). A working counter that correctly reports a real drop is scored `fails` (verified:
`row10 guard reports 1 drop=False`, and the same `recall_lost` anchor is in row 11: `row11 guard reports 1
drop=False`), while a stub that prints zeros passes (verified). Two of the six asserted
zeros are outside the claim: `a2_mismatch` counts any manifest-truth mismatch including false positives
(`a2-guards.py:148-157`: truth `clean` and any row → mismatch), and `dup_rows` counts observed+lead duplication,
which is row 8's evidence-marker domain. The manifest's own argument for excluding `vcs_fp` ("a false-positive
count outside this removal-side claim") applies equally to `a2_mismatch` and `dup_rows`. Base actual:
`recall_lost 0, crash_flip 0, pure_rows 0, vcs_fn 0, vcs_fp 26, a2_mismatch 0, dup_rows 0`.

Correction: assert `schema`, `rev`, `fixtures_rev` and that the claimed fields are integers; accept a nonzero
count as a valid guard result, and demonstrate the counting ability at a known-bad revision (e.g. `1f7f995`)
where drops are expected. Drop `a2_mismatch`/`dup_rows` from the claim or move them to the rows they belong to.

### 12. artifact-only assessment integrity — SCORECARD.md:1464

Claim: "Validate declared chronology/order, actual input/expectation hashes, historical rejection disclosure and
the four canonical SHONEN subjects, without a C1 dependency; distinguish clean/failed/could-not-evaluate, not
authenticate identities or prove evidence sufficiency." Rule: `mado-assessment.py --selftest
.ufo/waves/round-21/assessment-fixtures`, exit 0, regex `(?s)"pass": (\d+), "result": "selftest".*?"total": \1\}`.

Finding: **aligned in substance, minor brittleness**. This is the one rule whose object is sealed: the tool
checks `sha256(seal.json) == SEAL_SHA` and every listed fixture digest before replay (`mado-assessment.py`
`selftest`, lines 170-177). I truncated `expected.json` to one case; the tool refused:

```
{"code": 2, "error": "snapshot_tampered: expected.json", "finding_ids": ["assessment_input_invalid"],
 "result": "could-not-evaluate"}
exit=2
```

so a data-only reduction fails the rule. Base actual is `"pass": 20, "result": "selftest", ..., "total": 20`,
exit 0. Residual issues: the regex is a text match that depends on `sort_keys` ordering and `total` being the
last key (a new key after `total` would false-fail a working tool); it does not require `total == 20` (a 1/1
synthetic output passes the regex), and a tool-level edit could pass a reduced set. The claim's "distinguish
clean/failed/could-not-evaluate" is covered by the sealed cases when the full 20 pass.

Correction: parse the JSON and require `pass == total == 20` and `code == 0`; this keeps the seal's protection
and removes the key-order coupling.

## What these findings do and do not establish

Observed: every quoted output above was produced by the command shown; the sandbox stub run and the rule-level
evaluations used the frozen manifest/counter (`sha256:e02c76d1…`, `sha256:a2809501…`). The base `1/12` is
reproduced in `c2/smoke/base-8e5d9369.txt` and `controls/CtlC2DoNothing.md`; row 8's three base L failures are
the three named lead cases and are a real capability failure at base.

Inference (marked): the exact fix that would take L from 15/18 to 18/18 is not run; the finding only needs
the already-run fact that a rule input with L 18/18 is rejected. The population undercount is a parser/definition
mismatch, not a claim that the three omitted instruments are broken (all three pass checks at base; the
round-13 frozen runner's live mode was not re-run because it is a duplicate of the row-4 heavy regression — its
hermetic selftest passes 12/12).

Impacted axes: **calibration (C2)** — validity and provenance of the observed statuses, and the target's
sensitivity to non-capability edits; **the evidence-marker capability's own claim** (row 8's pass state
contradicts "on every finding row"); the round's **no-harm guard** (tools/ only, not the `.ufo/` meters); and
**premature saturation** (a 0/12 score does not imply the twelve capabilities work).

VERDICT: C2's manifest is not fit as a calibration instrument as frozen — the base 1/12 is a true row-8 failure,
but eleven of twelve rules are token/quantity matches satisfiable without the capability, rows 8 and 11 measure
the guarded object rather than the claim (row 8 rejects a fully fixed 18/18 and passes a 17/18 state that still
drops a lead row), three capability rows are outside the counted population, and the frozen counter reports
0/12 at base with two uncommitted meter stubs in a lane clone's working tree. The counted C2 target must not be
reported as capability evidence until the population, the meter provenance (rows 8/10/11) and the row-8/11
pass conditions are corrected.

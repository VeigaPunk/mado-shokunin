# R69CriticClaims — falsification of the frozen round-69 claims

seat: R69CriticClaims (critic, leaf; no subagent dispatch). Date 2026-11-03.
Read-only on the lane; every write went to `/fast/scratch/hyaku/mado-r69/R69CriticClaims/`
or to fixture git repos under it (explicit identity, toplevel asserted, removed before yield).
No commits, no package transactions, no tool installs.

Reviewed artifacts

| artifact | rev / sha256 |
|---|---|
| frozen declaration | `.ufo/waves/round-69/claims-declaration-r69.md` @ `789a87f1` (file sha256 `ecd481ae3e21ff5653d21a1b2151bf95d327b1689d3a861172f047d83d924b43`) |
| frozen baseline receipt | `.ufo/waves/round-69/control-baseline-r69.txt` @ `789a87f1` (sha256 `f2054c0edd768ab34dd6c9f7cf3180c91db471cbd3b2fad84da21dd027e86cee`) |
| frozen controls | `.ufo/waves/round-69/controls/c2-controls-r69.json` sha256 `975ca3ba…f90b9` (11 cases; **all 11 `expect_reader=true`**) |
| base | `04093b83f73a841117d3b31dbb2a6063f4f2a454` |
| measured content (claim receipts) | `296ed0d75e361387908cf2dd418d3677f49f94c8` |
| counters at 296ed0d7 | C1 harness `9461a059…649a73`, C1 counter `9f17a984…206ce8`, C2 counter `85f9e60a…44d725a` (byte-identical at `5864b00d`) |

## Summary

The two do-nothing controls reproduce exactly (C1 base `killed=0/3`, C2 base `controls=7/11`),
and both frozen *targets* are reproducible by the frozen counting commands (`TARGET_MET`, rc 0
at `296ed0d7`). Those are real.

Two things are not: (a) both targets are **reachable without the claimed surface** — C1 by a
1.4 KB text-checking harness that has no measurement body (B1), C2 by a key-position-plus-any-use
rule that drops the "reach a process launch of `git`" clause entirely (B3); and (b) the declared
harm watch is **RED at the measured content** (B5). Six further binding/record defects follow.
Verdict on the claims as frozen: measurable and causally separable, but under-bound in exactly
the two places the round is about (the oracle pairing and the dominance rule), and the round
cannot close at `296ed0d7` while claiming a GREEN harm watch.

## Blockers

### B1 (C1, critical) — the target is satisfiable by a text-checker with no body, no children, no oracle pairing

`verdict_met` (C1 counter @296, `quality/counters/c1-r69-paired-recipes.py:191-192`) requires
only `selftest_rc == 0 and killed == 3 and applied == 3 and base == 0`, and a kill is
`rc != 0` (declaration:34). A 1,356-byte harness whose `--selftest` merely checks three literal
fragments (hex-encoded so the check text is not itself an anchor) and exits 1 when one is altered
scores the full target.

Reproduction (fixture repo holds the fake at `quality/counters/c1-r69-landing-controls.py`,
real r68 blob at `04093b83` as the base harness):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 /fast/scratch/hyaku/mado-r69/R69CriticClaims/c1probes.py
```

Observed (probe A, counter @296, fixture rev `ef3dba03…`):

```
MADO_R69_SELFTEST instrument=… rc=0 line=MADO_R69_LANDING_CONTROLS_SELFTEST: 3/3 assertions passed
MADO_R69_MUTANT label=candidate recipe=R1 occurrences=1 rc=1 killed=yes
MADO_R69_MUTANT label=candidate recipe=R2 occurrences=1 rc=1 killed=yes
MADO_R69_MUTANT label=candidate recipe=R3 occurrences=1 rc=1 killed=yes
MADO_R69_BASE killed=0/3 applied=3/3
MADO_R69_PAIRED_RECIPES: selftest=0 killed=3/3 applied=3/3 base=0/3 verdict=TARGET_MET rev=ef3dba03…
```
rc 0. Impacted: SCORECARD.md:3738 ("neither is reachable without the work") and the claim title
"kills paired (decision + oracle) forgeries". The candidate at `296ed0d7` genuinely drives the
body (59/59 scripted assertions), but the scored predicate cannot tell it from the fake.
Smallest safe correction: keep the frozen contract line, add a `SetupError` (rc 2) refusal when
the unmutated candidate's selftest does not emit the scripted-child evidence lines
(`MADO_R69_R_CHILD`, `MADO_R69_R_CONTROL`, `MADO_R69_CHILD_ENV`, ≥ the harness's declared count)
and when a killed mutant's output carries no `… SELFTEST FAIL` assertion line; and state the
target's meaning in the SCORECARD as "kills the three named single-point mutations".

Persists at the final measurement rev `e0e1831a` (C1 counter `d9fc18c6…`, harness `9461a059…`;
`verdict_met` is byte-identical to 296's), re-run there before this report was written.

### B2 (C1, high) — base-leg false green: `base_applied` is computed, printed, and not in the verdict

`verdict_met(selftest_rc, killed, applied, base)` @296:191 has no `base_applied` argument;
`measure()` prints it at :236 and nothing else. With the base harness *present but its R1/R3
anchors already consumed*, the frozen command returns TARGET_MET:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 /fast/scratch/hyaku/mado-r69/R69CriticClaims/c1probes.py   # probe B
```
```
MADO_R69_RECIPE label=base recipe=R1 occurrences=0 applicable=no
MADO_R69_RECIPE label=base recipe=R3 occurrences=0 applicable=no
MADO_R69_BASE killed=0/3 applied=1/3 (the r68 harness must survive all three)
MADO_R69_PAIRED_RECIPES: selftest=0 killed=3/3 applied=3/3 base=0/3 verdict=TARGET_MET rev=22b6edba…
```
rc 0. This contradicts declaration:53 ("both counts are asserted before scoring"): `base=0/3`
cannot be distinguished from "the do-nothing leg never ran". The absent-harness case is refused
(:222-227), the inapplicable one is not.
Smallest safe correction: `raise SetupError` when `base_applied != 3`; no contract-line field
change, so the frozen line and `CONTRACT_RE` stay intact.

Persists at `e0e1831a`: the only base-leg refusal is the absent-harness one (:228); probe B
re-ran there with `MADO_R69_BASE killed=0/3 applied=1/3` and `base=0/3 … verdict=TARGET_MET`
rc 0.

### B3 (C2, critical) — the dominance clause is not discriminated by the frozen control set

Mutating the committed counter @296 so that the primary use path drops the git-launch
requirement (`usage_lines`, `quality/counters/c2-r69-guard-dominance.py:355-372`,
`if call_is_git(node):` → `if True:`) still scores **11/11** on the frozen cases; the same holds
for the inline path (:409, dropping `call_is_git`). Method: import the blob at `296ed0d7` and
call `classify` on each frozen `src` — the exact function `score_cases` (:480-494) scores.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 /fast/scratch/hyaku/mado-r69/R69CriticClaims/c2tip_matrix.py
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'   # dominance mutant, same rev
# (script in scratch: fin_* loads; prints "org 11/11", "no-git-launch-in-usage 11/11")
PY
```
Observed: `MUTANT no-git-requirement-inline 11/11 caught_by=[]`, and
`no-git-launch-in-usage 11/11 []`. The only dominance-ish cases are `uncalled-helper` (no use at
all) and `overwritten-env` (rebinding) — neither tests "the guarded env must reach a *git*
launch". A counter that satisfies declaration:100-105's first sentence and ignores its second
reaches `controls=11/11` and TARGET_MET.
Smallest safe correction (the set is sha-frozen, so not this round): round-70 adds
`guarded-but-git-called-without-env` (this counter already classifies it `(True, False)`) and
"env handed to a non-git call only". Until then the SCORECARD must not describe the dominance
clause as control-tested. The C2 counter is byte-identical at `e0e1831a`
(`85f9e60a…`) and re-scored there with the same result.

### B4 (C2, high) — the reader half has no negative case in the frozen set

All 11 cases carry `expect_reader=true` (verified: `11 11` from the frozen JSON). Replacing
`is_reader` (:470) with `return True` scores **11/11**. The r68 set had `non-reader`
(`expect_reader=false`); the r69 set dropped it, so the reader predicate is unpinned by the
controls and only indirectly by `verdict_met`'s `readers == 13` — a widening that keeps 13, or a
vocabulary change that swaps which files are readers while keeping 13, passes both.
Correction: round-70 set re-adds a negative-reader case; do not edit the frozen set now.
(The `reader-always-true` 11/11 result is unchanged at `e0e1831a` — same counter blob.)

### B5 (harm watch, critical) — `MADO_LANDING_COUNTERS` is RED at the measured content

Declaration:170 requires GREEN (`nav`, `usedby`, `ledger`, `citecheck` all rc 0) at the measured
content. My run with explicit citecheck paths (not the M69-3 setup-default):

```sh
bash quality/landing-counters.sh --repo . --rev 296ed0d75e361387908cf2dd418d3677f49f94c8 \
  --round 69 --scratch-root /fast/scratch/hyaku/mado-r69/R69CriticClaims/st-land \
  --citecheck-paths .ufo/waves/round-69/measurement-r69.txt
```
```
LEDGER: population=116 ledger_rows=113 uncovered=3 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MISSED rev=296ed0d7…
LANDING_LEG ledger rc=1
MADO_LANDING_COUNTERS: RED (nav=0 usedby=0 ledger=1 citecheck=0 rev=296ed0d7…)
```
exit 1. The three uncovered paths are this round's own instruments
(`c1-r69-landing-controls.py`, `c1-r69-paired-recipes.py`, `c2-r69-guard-dominance.py`); the
`quality/tool-ledger.md` rows land only at `5864b00d`. The committed receipt
`.ufo/waves/round-69/harm-watch-r69.txt:2-5` records the earlier 5fc29ae run as `landing_rc=2`
(citecheck default path), so neither committed run is GREEN. The three instrument blobs are
byte-identical at `296ed0d7` and `5864b00d`, and the 20-file C2 population is unchanged, so the
clean fix is a re-run of *both* frozen counting commands at `5864b00d` (116/116 ledger rows) and
one harm-watch receipt at that rev. Publishing claims at one rev and harmony at another is what
the declaration forbids.

The lane has since produced further receipts, and they confirm the shape rather than close it:
`.ufo/waves/round-69/landing-counters-r69.txt` is `RED (nav=0 usedby=1 ledger=0 citecheck=0 rev=3cd68aa3…)`
while `.ufo/waves/round-69/final-gates-r69.txt` reports `GREEN (… rev=fc0387b9…)`, and
`.ufo/waves/round-69/measurement-final-r69.txt` names yet another rev (`e0e1831a`) for the claims.
No single rev carries both the claim contract lines and a green landing leg, so the harm-watch
sentence is not evidenced at "the measured content" as written; a closure must state one rev and
show both artifacts at it.

### B6 (record) — the declaration points at bytes the baseline receipt does not contain

Declaration:67-69: "The exact byte strings … are the ones recorded in
`.ufo/waves/round-69/control-baseline-r69.txt` (each `RECIPE <name> occurrences=1` line)".
The receipt records only counts (`:8,10,12,18,20,22`) — no old/new bytes, no sha256, no repr.
The bytes are recoverable only from the r68 blob (`04093b83:quality/counters/c1-r68-landing-controls.py`
lines 491-492, 439, 779) and from the counter's literals. Verified those literals are correct:
each occurs exactly once in the r68 base and once in the r69 prototype (independent check below).
Correction: add `old_sha256=` per recipe to the closure receipt.

### B7 (record) — `applied` names two different artifacts in two frozen documents

Contract line (:48-50) `applied=<k>/3` = recipes applied to the **candidate** (validated by the
counter's `mutation_score` on the candidate, :191-200). Baseline receipt:14
`MADO_R69_C1_BASE: … applied=3/3` = recipes applied to the **r68 harness**. Declaration:73
"Before at base … `applied=0/3`" = candidate absent. A reader comparing :73 with receipt:14 sees
0/3 vs 3/3 for "the same three recipes". Correction: rename the base leg's field in receipts to
`base_applied=` (the contract line stays frozen).

### B8 (record) — SCORECARD still publishes recipe L as a survivor; the lesson calls it equivalent

`SCORECARD.md:3656` (round-68 C1 row): "multi-point forgeries (drop `forged_credit`, credit
`mz_rc is None`, remove the hermeticity guard) survive and are named by RevC1".
`corpus/lessons/round-69.md:47` (M69-1): L is an **equivalent mutant**, excluded. The round-69
SCORECARD section does not amend `:3656`. Verdict on item 9 below: the exclusion is correct, but
the published round-68 sentence must carry an erratum pointer; otherwise the lane holds two
authorities that disagree.

### B9 (record, high) — SCORECARD.md:3738's non-reachability inference is falsified

"both do-nothing controls miss the target (0/3 and 7/11), so neither is reachable without the
work." The premise is true (B1/B3 notwithstanding, the *untouched* instruments miss both
targets); the inference is false: C1 is reachable with a text-checker (B1), C2 with a rule that
drops the dominance clause (B3). Correction: state the premise only, and name the control-set
discrimination as the missing step.

### B10 (C2, low) — the cited source grounds a construction the rule rejects

Declaration:145-151 quotes git.adoc: `--no-replace-objects` "is equivalent to exporting the
`GIT_NO_REPLACE_OBJECTS` environment variable" and the variable acts on "Setting and exporting".
A module-scope `os.environ["GIT_NO_REPLACE_OBJECTS"] = "1"` followed by
`subprocess.run(["git", …])` with no `env=` classifies `(True, False)` on the counter @296 — i.e.
unguarded — although the child inherits the exported variable and, per the quote, is guarded. No
measured file uses the idiom (per-file r68/r69 classification diff over the 20 files = 0), so no
target effect today; but the census would flag a correct gate as unguarded (target's
`unguarded=0` would go red for a safe file). Correction: the knowledge entry must state that the
rule is stricter than the export semantics (parent-process export is an accepted shape it does
not model), or model it; do not claim the quote grounds the "at the call" restriction.

### B11 (axis, medium) — C2's bounded score cannot move, and its published cell is another instrument

`:132` bounded `10 × guarded / readers` is 10.0000 at both ends (guarded 13/13 at `04093b83` and
at the measured content). `quality/check-axis-scores.py` at `296ed0d7` prints
`axis=operability published=12/12 derived=12/12` — that cell is the **citecheck** selftest, which
C2 does not touch. The declaration discloses "moves discrimination, not the count", and the axis
label matches the round-68 precedent (`SCORECARD.md:3657` "C2 **operability**"), so this is not a
misattribution; it is a saturation-bookkeeping hazard: a capability row whose bounded score moved
0.0000 would reset the N=3 stagnation window on a row with no axis-cell movement. Correction:
publish `controls=7/11 → 11/11` as the moved cell and keep the stagnation bookkeeping tied to the
bounded score (or mark the C2 row as a discrimination row, not a capability row).

## Verified clean (so the record is not over-corrected)

- Contract lines are literal matches: declaration:48-50 printed by the counter (my run at
  `296ed0d7`) and :119-121 likewise; `CONTRACT_RE` fullmatches in both.
- Recipes occur exactly once in the r68 base blob and once in the r69 prototype; my independent
  table (`c1base.py`) reproduces base `R1/R2/R3 rc=0 52/52` → `killed=0/3` and prototype
  `rc=1 57/59, 58/59, 57/59` → `killed=3/3`. Recipe bytes match the counter literals exactly.
- C2 base leg 7/11 and target 11/11 reproduced; the r69 rule also passes all 11 **r68** cases
  (cross-set `bad=0`), so the new set did not silently drop a predecessor capability.
- Two over-inclusions I found at `5fc29ae` (nested-dict value key credited as key position;
  non-`dict()` call keyword credited as a `dict(KEY=…)` keyword) are **fixed** at `296ed0d7`:
  both shapes now classify `(True, False)`.
- Clauses that the frozen set does discriminate: key position (`value-position-only`), dead
  branch (`dead-branch-only`; my dead-filter mutant scores 10/11 caught by it), rebinding
  (`overwritten-env`), producer/one-hop (`producer-helper`, `argv-name-flow`).
- Causal separability: the C2 counter reaches TARGET_MET in a fixture repo containing **zero**
  `c1-r69-*` blobs (`c1 files in fixture: 0`, rc 0), and the C1 counter reaches verdicts in
  fixtures containing zero C2 blobs. Disjoint read sets; shared only the wave and lesson.
- Axis posture numbers match the record: `SCORECARD.md:3684` (nav 80/80, calibration 86/86,
  operability 12/12), `:3677` (gate 460/460), §Saturation `:282-284` (N=3), and
  `:3669` (capability row first-working 68 → gap 0). Live table at `296ed0d7`:
  `MADO_AXIS: checked=3 mismatched=0`.
- Chronology by commit time: freeze `789a87f1` 22:42:47 → w1 spec/ready `98bff016` 22:44:44 →
  instruments `5fc29ae7` 22:47:50 → claims/harm `6a5cefd2` 22:48:44; freeze is an ancestor of
  both the ready file and the measured content. Caveat: the freeze commit's **author** date is
  22:34:37, earlier than the prototype (22:41:49) and the baseline receipt (22:42:12) it
  contains, so author dates cannot be used for the freeze order.

## Answers to the assigned items

1. **Control reachability.** No: at base the r68 harness survives all three (`0/3`, 52/52) and
   the r68 classifier scores `7/11` (reproduced by `c2score.py`, exit 0), so neither *untouched*
   instrument reaches its target. But each target is reachable without the claimed surface — see
   B1 (C1) and B3 (C2), with commands.
2. **Predicate-literal binding.** Contract lines: exact. Mismatches found: the recipe-byte
   pointer (B6), the `applied` referent (B7), and the frozen evidence labels themselves — the
   baseline prints `MADO_R69_C1_BASE/PROTO` and `MADO_R69_C2_BASE/PROTO`, and the C2 prototype
   prints `SUMMARY population=… readers=… guarded=… unguarded=…` with no `controls=` field and
   no `MADO_` label, so no frozen *prototype* label can be compared character-for-character with
   the contract lines; only the landed counters print them.
3. **Causal separability.** Proven at artifact level (fixtures above); disjoint `extract` paths;
   each counter runs alone.
4. **Axis attribution.** Not misattributed (lane precedent: SCORECARD:3656/3657 name C1
   calibration, C2 operability), and the posture numbers match §Saturation and the round-68
   content. The defect is saturation bookkeeping: C2's bounded score is a constant 10.0000 and
   its axis-table cell is citecheck 12/12 (B11).
5. **No-harm.** Changes: three new `quality/counters/*.py`, one knowledge entry, one SOURCES row
   (S438), lesson/QUALITY/LOG/ledger edits. Caller that breaks: `quality/check-tool-ledger.py`
   (population derives from `quality/counters/*.py`, `:10-14`) — at the measured content it is
   `population=116 ledger_rows=113 uncovered=3` rc 1, GREEN only from `5864b00d` (B5). No other
   standing gate enumerates `quality/counters/*` (the round-26/35 gates are round-pinned; the
   landing wrapper calls only used-by/ledger/citecheck).
6. **Claim sizing.** No universal fault claim; both targets are finite denominators; kill rules
   were frozen before the measured runs. Flagged: the title/surface sentences (B1, B3) and
   SCORECARD:3738's inference (B9). The only after-the-fact narrowing is recipe L, disclosed and
   proved pre-freeze (item 9).
7. **Chronology.** Freeze precedes the wave ready file and the measured runs by commit time; the
   author-date anomaly and the pre-freeze prototype measurements are in "Verified clean" above.
   Declaration:7 "FROZEN before any candidate data" is true for the scored content, not for the
   design prototype (baseline already carries `MADO_R69_C1_PROTO killed=3/3` and
   `MADO_R69_C2_PROTO controls=11/11`).
8. **Sourcing.** C2 does rest on S438 as cited (the row exists in the draft `corpus/SOURCES.md:388`
   with the two quotes and the 050c5330… digest). What the quote grounds: the variable is the
   switch and it must be exported into the child's environment. What it does **not** ground: the
   Python `env=` mechanism, the one-module/one-hop syntactic shape, the "at the call" restriction
   (B10), the 20-file population, or that a merely constructed mapping is ineffective beyond the
   export inference.
9. **Equivalent-mutant exclusion.** For: `mz_rc` is assigned `r.returncode`
   (`c1-r68:435`) and the mutated line is `c1-r68:439` in the same `try`; the `is None` disjunct
   is dead on every path that reaches it (init `None` at :414 is overwritten before use), so the
   mutant is provably equivalent and excluding it is what r28's rule requires — equivalence
   classification affects the denominator. Against: the classification happened *after* the
   survivor was observed at `5fc29ae`-predecessor prototype time, and it retro-corrects a
   published round-68 statement, so on its face it is a post hoc denominator edit. Verdict:
   correct exclusion, but only with an erratum at `SCORECARD.md:3656` (B8); the proof, not the
   preference, is what makes it legitimate.

## Reproduction index

Archived (read-only copies of exactly what ran) in `.ufo/waves/round-69/w1/R69CriticClaims/evidence/`:

| file | sha256 | what it proves |
|---|---|---|
| `c1base.py` | `9169474062fcb3a7a9da99bcaf800211328d9da93e192128aa0c842815520ae2` | independent recipe table: base 0/3 (52/52), prototype 3/3; exit 0 |
| `c2score.py` | `1ffda5a0320debeee3a1b129d4385236b8a768061c6530fc1aa4924988b00596` | 4-way control scoring + cross-set (`bad=0`); exit 0 |
| `c2tip_matrix.py` | `6d3082e6c16f987fb344da6865184f608a824150ac5191d39bd4d30aec2dc637` | discrimination matrix: `no-git-requirement-inline 11/11`, `reader-always-true 11/11`; exit 0 |
| `c1probes.py` | `4707bd9341e817baaa5961d47af0654d520cbcfee07bed5112f7e9e5b047ce96` | B1 shortcut (TARGET_MET rc 0) and B2 false green (TARGET_MET rc 0); fixtures removed in `finally` |
| `ledger-296.txt` | `e4a19ef9e51a8bf45d64d175d9a6224942da03f6755467befee3138eb0c2ab82` | ledger gate rc 1 at `296ed0d7` |
| `ledger-head.txt` | `95624e92f165c0aab22675ebf50766bf3c76b8ea931072789758658dcde3f02e` | ledger gate rc 0 at `5864b00d` |

Each script uses its own directory as scratch (`S = dirname(__file__)`): copy it to a scratch
directory and run it there; set `REV` at the top of `c1probes.py` / `c2tip_matrix.py` to re-run
at any content rev (the archived value is `296ed0d7`; the `e0e1831a` re-runs quoted above used the
same scripts with `REV` repointed). Scratch `/fast/scratch/hyaku/mado-r69/R69CriticClaims/` was
removed before yield (verified empty); the archived copies are the only surviving form.

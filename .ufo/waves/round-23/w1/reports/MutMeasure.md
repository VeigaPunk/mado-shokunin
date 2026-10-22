# MutMeasure — mutation test of the round-23 repair counter

**Seat:** MutMeasure (mutation-tester, leaf) · **Wave:** round-23 / w1 · **Date:** 2026-10-22
**Subject under test:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/repair/measure.py`
(sha256 `0c41f8c867da7575e21f09c54776f33a27cdab0e352360787b1c397d7e18c04e`)
**Scratch tree:** `/fast/scratch/hyaku/mado-r23/MutMeasure/` (all mutations here; the lane copy was never edited)
**Receipts:** `.ufo/waves/round-23/w1/out/MutMeasure/` (34 files)

## Verdict

| Mutant | Meaning | Tool output | Control | Mutant | Verdict |
|---|---|---|---|---|---|
| M2_ignore_unparsed | exact rule drops `unparsed == 0` | base classifier | 6/12 | 9/12 | **killed** |
| M3_any_evidence | exact rule compares `(class, command)` only | `E_all_lead.py` | 2/12 | 6/12 | **killed** |
| M4_missing_present | present rule drops the `want_present` subset test | `E_drop_hookdict.py` | 5/12 | 6/12 | **killed** |
| M5_drop_exit | `clean = True` (exit/error check dropped) | `E_exit2.py` | 0/12 | 6/12 | **killed** |
| M8_exact_subset | exact rule becomes a subset test | `E_extra_row.py` | 2/12 | 6/12 | **killed** |
| M1_ignore_forbid | `forbidden = False` | all five tool outputs | — | — | **survived** (equivalent mutant) |
| M7_forbid_observed_only | `forbid_any` counted only at the `observed` tier | all five tool outputs | — | — | **survived** (equivalent mutant) |
| M6_skip_tamper | `verify()` skips the expected.json + fixture digests | tampered snapshot | exit 2 | 6/12 | **inconclusive** |

**Kill rate = killed/(killed+survived) = 5/7 = 0.714.** (M6 excluded; if M6 were counted as killed the rate would be 6/8 = 0.75.)

Control discipline (per L1 note): every pair ran the **unmutated** judge on the *same* tool output first. All five controls were well-formed verdict documents (schema + `results` + `passed`/`total`, exit 1), never exit 2 / timeout / scratch-layout errors. A kill was counted only when both sides were well-formed and the verdicts differed. Baseline control on the base classifier reproduced the frozen 6/12 exactly.

## Baseline (control)

```
cd /fast/scratch/hyaku/mado-r23/MutMeasure/lane/.ufo/waves/round-23/repair
python3 -I measure.py --tool /fast/scratch/hyaku/mado-r23/MutMeasure/tools/base-mado-tripwire.py
```
→ `passed 6 / 12`, exit 1, well-formed. This matches the frozen C1 "before" figure (6/12 at the base classifier `cd9da20c…`).

Scratch layout mirrors the lane so `LANE`/`HELPER` resolve unchanged:
`…/MutMeasure/lane/.ufo/waves/round-23/{repair,M1…M8,TAMPER,TAMPERFIX,EXTENDED}/measure.py`, with the
round-21 oracle helper copied to `…/MutMeasure/lane/.ufo/waves/round-21/oracle/measure.py`
(sha256 `4eb893d2…`, byte-identical to the lane) and the 12 fixtures byte-identical to the lane.

## Method

* Every mutant is a **single-point edit** to `judge()` (or `verify()` for M6) in a scratch copy; the diff of each
  mutant against the original is in the receipts (`mutation_summary.json` → `mutants`).
* Scanner runs go through the unchanged round-21 oracle helper (`runpy.run_path(HELPER)["scan"]`), one child per
  case, 384 MiB / 15 s caps, `python3 -I`. No transcript content was executed except by the classifier over
  committed fixture data.
* Four trivially edited **classifier copies in scratch** supplied the tool outputs that the base classifier cannot
  produce (the base classifier emits exit 1 with a valid payload for every fixture):
  * `E_all_lead.py` — one line: every finding's `evidence` forced to `"lead"`.
  * `E_drop_hookdict.py` — one line: drop the finding whose command is `pacman -S r23-hook-dict`.
  * `E_exit2.py` — one line: `run_scan` returns 2 instead of the verdict code (payload still valid JSON).
  * `E_extra_row.py` — one line: append a synthetic `package_query` row `pacman -Q r23-synthetic-extra`.
* Before the real runs, a **bounded exhaustive search** over the payload space the judge can see (all subsets of the
  per-case candidate rows × exit ∈ {0,1,2,None} × error ∈ {None,"boom"} × unparsed ∈ {0,1}; 3264 payloads) decided
  which mutants are *killable at all* — see `discriminator_search.json`.

## Kills — exact commands

All paths under `/fast/scratch/hyaku/mado-r23/MutMeasure/`.

**M2 — ignore unparsed** (tool: base classifier)
```
python3 -I lane/.ufo/waves/round-23/repair/measure.py        --tool tools/base-mado-tripwire.py   # 6/12
python3 -I lane/.ufo/waves/round-23/M2_ignore_unparsed/measure.py --tool tools/base-mado-tripwire.py # 9/12
```
Changed cases: `ForwardExistingClosureWithoutFrameContamination`, `ForwarderPassesCallerArgument`,
`ForwarderInvokesFactoryClosure` (all three carry `unparsed=1` with otherwise-matching rows).

**M3 — accept any evidence tier for exact cases** (tool: `E_all_lead.py`)
```
python3 -I lane/.ufo/waves/round-23/repair/measure.py       --tool tools/E_all_lead.py   # 2/12
python3 -I lane/.ufo/waves/round-23/M3_any_evidence/measure.py --tool tools/E_all_lead.py # 6/12
```
Changed: `ReturnedGlobalHelper`, `CallerArgumentBeforeClosureOverlay`, `NestedDefReadsDefiningFrame`, `LateGlobalRebinding`.

**M4 — accept missing rows for present cases** (tool: `E_drop_hookdict.py`)
```
python3 -I lane/.ufo/waves/round-23/repair/measure.py         --tool tools/E_drop_hookdict.py   # 5/12
python3 -I lane/.ufo/waves/round-23/M4_missing_present/measure.py --tool tools/E_drop_hookdict.py # 6/12
```
Changed: `CallbackStoredInDict`.

**M5 — drop the exit/error check** (tool: `E_exit2.py`)
```
python3 -I lane/.ufo/waves/round-23/repair/measure.py     --tool tools/E_exit2.py   # 0/12
python3 -I lane/.ufo/waves/round-23/M5_drop_exit/measure.py --tool tools/E_exit2.py # 6/12
```
Changed: the four exact cases plus both present cases. The scanner exits 2 with a *valid* JSON payload, so only the
`exit in (0,1)` clause separates control from mutant.

**M8 — exact rule accepts a superset of rows** (tool: `E_extra_row.py`)
```
python3 -I lane/.ufo/waves/round-23/repair/measure.py       --tool tools/E_extra_row.py   # 2/12
python3 -I lane/.ufo/waves/round-23/M8_exact_subset/measure.py --tool tools/E_extra_row.py # 6/12
```
Changed: `ReturnedGlobalHelper`, `CallerArgumentBeforeClosureOverlay`, `NestedDefReadsDefiningFrame`, `LateGlobalRebinding`.

## Survivors — M1 and M7 are equivalent mutants (not a judge weakness)

Both survived all five tool outputs with identical verdicts. An exhaustive 3264-payload enumeration shows **zero**
verdict flips, and the reason is structural, not accidental:

* `forbidden` is computed over **reported rows**, while the exact rule already requires the reported row set to
  equal `want` exactly. Every frozen case's `want` commands are **disjoint** from its `forbid_any`
  (verified: `want ∩ forbid_any = ∅` for all 12 cases, receipt `equivalence_proof.json`). So a reported
  forbidden command always implies `keys != want` — the case fails on the row comparison anyway, and
  `not forbidden` can never be the *sole* cause of a failure.
* Both **present** cases have `forbid_any: []`, so `forbidden` is always False and the clause is vacuous there.

Therefore M1 (`forbidden = False`) and M7 (forbid counted only at the `observed` tier) are **verdict-equivalent to
the unmutated judge on the frozen 12-case set for every possible scanner output**. No tool output can kill them.
This is a property of the frozen `expected.json` + `measure.py` pair, not evidence that the `forbid_any` guard is
useless in general.

Proof of killability if the fixture set were strengthened (scratch `EXTENDED/` only, lane untouched): giving the
present case `CallbackStoredInDict` a `forbid_any: ["pacman -S r23-hook-dict"]` — a command the base classifier
reports at the `lead` tier — makes both mutants flip that case:
```
python3 -I lane/.ufo/waves/round-23/EXTENDED/measure_orig.py --tool tools/base-mado-tripwire.py  # 5/12
python3 -I lane/.ufo/waves/round-23/EXTENDED/measure_M1.py   --tool tools/base-mado-tripwire.py  # 6/12
python3 -I lane/.ufo/waves/round-23/EXTENDED/measure_M7.py   --tool tools/base-mado-tripwire.py  # 6/12
```
Changed case: `CallbackStoredInDict`. (Receipts `EXTENDED_measure_*.json`.) This is **coverage advice for the L1**,
not a request to change the frozen set: the shipped `expected.json` is hash-pinned (`EXPECTED_SHA`), so the
forbid_any guard is currently untestable against the frozen population.

## M6 — skip the tamper check: inconclusive under the L1 convention

```
python3 -I lane/.ufo/waves/round-23/TAMPER/measure_orig.py --tool tools/base-mado-tripwire.py
   → exit 2, {"error": "snapshot_tampered: expected.json"}      (not a well-formed verdict)
python3 -I lane/.ufo/waves/round-23/TAMPER/measure_M6.py --tool tools/base-mado-tripwire.py
   → exit 1, well-formed verdict, passed 6/12
```
The control exits 2 on the tampered snapshot, so under the L1 convention ("exit 2 … are inconclusive, not killed")
M6 is **inconclusive**, not killed — even though the mutant plainly differs (it measures a tampered snapshot
instead of refusing it). The same holds for the fixture-tamper variant (`TAMPERFIX/`): control exit 2
`snapshot_tampered: ReturnedGlobalHelper`, mutant well-formed 6/12 (receipts `TAMPERFIX_measure_*.json`).
The tamper guard is the one clause whose failure mode *is* an error document, so it cannot be killed by the
well-formed-verdict criterion. It is nonetheless exercised: the control's exit 2 is the tamper guard firing.

## Coverage findings for the L1 (advice only — no contract change proposed)

1. **`forbid_any` is untestable against the frozen 12-case set.** M1 and M7 survive because every `want` is
   disjoint from its `forbid_any`, so the clause is redundant with the exact-row comparison, and both present cases
   have empty `forbid_any`. A future repair-set revision that gives a *present* case a non-empty `forbid_any` whose
   command is reported at the `lead` tier would restore the clause's discriminating power (demonstrated above).
2. **`unparsed == 0` and the exit/error check are the load-bearing clauses for exact cases.** M2 and M5 were killed
   without any classifier edit beyond the base one (M2) or a one-line exit change (M5).
3. **The exact rule's `keys == want` is doing double duty**: it enforces both "no missing row" and "no extra row".
   M8 shows the "no extra row" half is separately detectable, so the equality is not merely a subset test.
4. **Present-case recall is only one-sided.** M4 shows a missing row for a present case is detectable, so the
   `want_present ⊆ present` clause is genuinely exercised by `CallbackStoredInDict` / `CallbackStoredOnAttribute`.

## Restoration / lane integrity

The lane copy of `measure.py` was **never edited**; every mutation lives in the scratch tree.

| Lane file | sha256 before | sha256 after | unchanged |
|---|---|---|---|
| `.ufo/waves/round-23/repair/measure.py` | `0c41f8c8…e18c04e` | `0c41f8c8…e18c04e` | yes |
| `.ufo/waves/round-23/repair/expected.json` | `53e34d26…187c6b9` | `53e34d26…187c6b9` | yes |
| `.ufo/waves/round-23/repair/truth.py` | `7f9e7865…23d18b0` | `7f9e7865…23d18b0` | yes |
| `.ufo/waves/round-21/oracle/measure.py` | `4eb893d2…c6c82da` | `4eb893d2…c6c82da` | yes |
| `tools/mado-tripwire.py` | `cd9da20c…cf00ea84` | `cd9da20c…cf00ea84` | yes |

`git -C <lane> status --porcelain -- .ufo/waves/round-23/repair .ufo/waves/round-21/oracle tools/` → empty.
No `__pycache__`/`.pyc` residue in the repair tree; the 12 lane fixtures are byte-identical to the scratch copies.
Receipt: `out/MutMeasure/restoration_evidence.json`.

## Reproducibility

The full matrix was run twice end-to-end; all eight verdicts were identical across runs
(`mutation_matrix_run1.json` vs `mutation_matrix.json`).

## Receipt index (`.ufo/waves/round-23/w1/out/MutMeasure/`)

| File | Contents |
|---|---|
| `mutation_summary.json` | headline summary: per-mutant verdicts, commands, counts, kill rate, lane hashes |
| `mutation_matrix.json` | full matrix: control + mutant receipts for every pair, both runs' worth of `run_*.json` |
| `mutation_matrix_run1.json` | first full run, for the reproducibility comparison |
| `run_control__*.json`, `run_<mutant>__*.json` | per-run receipt (cmd, exit code, passed/total, per-case verdicts, stdout sha256) |
| `baseline.json` | baseline control run on the base classifier (6/12) |
| `discriminator_search.json` | bounded exhaustive payload-space search: which mutants are killable in principle |
| `equivalence_proof.json` | formal proof that M1/M7 are equivalent (3264 payloads, 0 flips) + per-case reasoning |
| `EXTENDED_measure_*.json` | scratch-only strengthened case set showing M1/M7 *are* killable |
| `TAMPERFIX_measure_*.json` | fixture-tamper variant of the M6 scenario |
| `restoration_evidence.json` | lane hashes before/after, git status, scratch mutant/tool hashes |

## Verdict line

**Mutation test of the round-23 repair counter: 5 killed, 2 survived (both provably equivalent mutants — the frozen `forbid_any` clause is untestable against the frozen 12-case set), 1 inconclusive (M6, tamper guard — its failure mode is an error document by design); kill rate 5/7 = 0.714. The judge is sound on every clause the frozen fixture set can exercise; the one coverage gap is that `forbid_any` cannot discriminate any judge variant until a present-kind case carries a non-empty `forbid_any`. The lane copy was never modified.**

# R53Five50 — measured C1/C2 discrimination at base tip

Seat `R53Five50`, leaf work item 50 (no dispatch, no subagents). Axes: **operability (C1)** and
**coverage (C2)**. Base tip `ad4bf2059bcfafe63671d262222908ee1fe8001c`; frozen predicate
`.ufo/waves/round-53/claims-frozen.md:3-13`. Everything below is measured on committed lane
bytes plus throwaway fixture git repositories created under
`/fast/scratch/hyaku/mado-r53/R53Five50`. No tracked lane file was written; no git/jj mutation
in the lane; no live read, package query, producer run, screenshot, input capture, campaign
tool, network fetch or tool install occurred (pacman untouched, as the round requires).

State of the four instruments at tip (blob ids, `git rev-parse ad4bf205:<path>`):

| artifact | blob | note |
|---|---|---|
| `quality/counters/c1-r51-ledger.py` | `143cc4fd…` | only committed C1 instrument |
| `quality/check-tool-ledger.py` | `9fac1c3e…` | the gate the C1 counter pairs with |
| `quality/tool-ledger.md` | `ebe38043…` | the production ledger, 82 rows |
| `quality/counters/c2-r51-dispatch-entry.py` | `f33075b9…` | only committed C2 instrument |
| `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` | `b4496f75…` | the entry C2 must repair |

No round-53 tracked file exists at tip (`git ls-tree -r --name-only ad4bf205 .ufo/waves/round-53/`
→ empty), and `git ls-tree -r --name-only ad4bf205 quality/counters/ | grep -E 'r52|r53'` → no
match. So neither claim's "new committed counter" exists yet; this report measures the baseline
that any round-53 counter must beat, and names the exact fixtures each must miss.

## C1 — what the committed instrument actually discriminates

Frozen text (`claims-frozen.md:7`), verbatim: *"a newly committed, scratch-aware counter with
explicit selftest returns TARGET_MET on the production ledger, TARGET_MISSED on a no-work control
and each frozen forgery fixture, with exact population coverage and non-self pointers."*

Commands (identical shape for every row: production repo for the first two, fixture clone for the
rest; `FIX` = `/fast/scratch/hyaku/mado-r53/R53Five50/fx-3047691`, whose
`git rev-parse --show-toplevel` was asserted equal to its own path before any mutation):

```
python3 -I <lane>/quality/counters/c1-r51-ledger.py --repo <lane> --rev ad4bf205… --work …/c1-prod
python3 -I <lane>/quality/counters/c1-r51-ledger.py --repo <lane> --rev 6ca8c559… --work …/c1-base
python3 -I <lane>/quality/counters/c1-r51-ledger.py --repo $FIX --rev <fixture sha> --work …/work-<mode>
```

| fixture (ledger mutation, one commit each) | frozen C1 expects | observed last line | exit |
|---|---|---|---|
| production ledger at tip | TARGET_MET | `C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=ad4bf205…` | 0 |
| no-work control, base `6ca8c559…` (ledger absent) | TARGET_MISSED | `C1_R51: verdict=TARGET_MISSED ledger=absent population=79 rev=6ca8c559…` | 1 |
| **all 82 descriptions → `does things.`** | TARGET_MISSED | `C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=6f1702a5…` | **0** |
| **all 82 pointers → `quality/tool-ledger.md`** | TARGET_MISSED | `C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=c4f65cb2…` | **0** |
| duplicate row appended | TARGET_MISSED | `… ledger_rows=83 … dup=1 checker=failed verdict=TARGET_MISSED` | 1 |
| all descriptions → `-` (clean base, no dup) | TARGET_MISSED | `… ledger_rows=82 … empty_desc=82 … verdict=TARGET_MISSED` | 1 |
| one population row deleted | TARGET_MISSED | `… ledger_rows=81 uncovered=1 … verdict=TARGET_MISSED` | 1 |
| new `tools/zz-r53-fixture.py` with no row | TARGET_MISSED | `C1_R51: population=83 ledger_rows=82 uncovered=1 … verdict=TARGET_MISSED` | 1 |
| every pointer → `SCORECARD.md` | (structural) | `… bad_pointer=22 … verdict=TARGET_MISSED` | 1 |
| gitlink + symlink under `tools/` | (population identity) | counter `population=84`, checker `population=83` → `checker=failed verdict=TARGET_MISSED` | 1 |

Findings, each `[OBS]` from the runs above:

1. **The two frozen "Before" bypasses reproduce on the tip instrument.** Generic descriptions and
   ledger self-pointers both reach `TARGET_MET` with exit 0. The self-pointer is total: the ledger
   lists all 82 basenames in cell 1, so any pointer naming the ledger satisfies the only clause
   there is. The clause is
   `c1-r51-ledger.py:pointer_resolves` (`:196-208`) — token must exist in the tree and its bytes must
   contain `basename(row_path)` — with no exclusion of the ledger, the counter, or the checker. The paired gate has the same shape: it requires "at least one must
   name the row file's basename in its bytes" (`check-tool-ledger.py:22-25`) and never excludes the
   scored artifacts. This is the frozen defect, measured, not inferred.
2. **The instrument is not uniformly weak.** Duplicate rows, empty/placeholder descriptions,
   uncovered population entries (both directions: deleted row and unrowed new file) and dangling
   rows all miss as the frozen text requires. So a round-53 counter does not need to rebuild these;
   it must add only the missing discrimination.
3. **There is no counter selftest.** `c1-r51-ledger.py` exposes `--repo/--rev/--work/--checker`
   only (`:358-361`); no `--selftest`. The `selftest=ok` in its verdict line is the *checker's*
   50-assertion suite (`detail: checker selftest ok (ratio=50/50 form=with-work)`). A reader taking
   `selftest=ok` as the counter's own evidence is reading a different instrument's result. The
   frozen requirement says "explicit selftest"; on this instrument it is delegated, not explicit.
4. **Population identity diverges between the two paired instruments on non-blob tree entries.**
   A `tools/` gitlink is counted by the counter's `population()` (name listing only, no blob filter,
   `c1-r51-ledger.py:133-148`) but excluded by the checker, whose header states "Only blobs
   count (a gitlink or tree entry is not a file)"
   (`check-tool-ledger.py:14`): counter `population=84`, checker `population=83`, and the
   counter's own cross-check then forces `checker=failed`. Under a tree containing such an entry
   the counter can never reach `TARGET_MET`, and a row for the gitlink can never resolve (no blob
   bytes to search). "Exact population coverage" is therefore instrument-dependent today, which is
   the first thing a frozen round-53 population definition must fix.
5. **Pointer validity is name-containment, not accountability.** Retargeting every row at
   `SCORECARD.md` resolves 60 of 82 (22 `bad_pointer`) because `SCORECARD.md` and
   `PROVINCE.md` are bulk documents that name most instruments somewhere; on the production ledger
   42 rows point at `SCORECARD.md` and 20 at `PROVINCE.md` (12 distinct pointer targets across 82
   rows; no description is reused, so the description hole is about *content*, not repetition). The frozen text calls the check "bounded structural accountability, not semantic proof",
   so this is inside its declared ceiling — but any round-53 clause meant to enforce "non-self"
   must exclude at least the ledger, the counter and the checker, or the ceiling is lower than the
   text implies.

Minimal added clauses implied by the measurements (proposals for the round-53 counter, not edits):
pointer target not in {ledger, counter, checker}; description distinctness plus a floor on
overlap between cell 2 and the instrument's own header tokens (the ledger's own cell-2 contract at
`quality/tool-ledger.md:16`: "read from its own header, never inferred from its name"); a
blob-filtered population shared with the gate the counter pairs with.

## C2 — the r52 entry at tip, and whether any counter can reject its old bytes

**No repair and no bound counter exist at tip.** The entry is byte-stable since it landed:
`git log --oneline ad4bf205 -- corpus/knowledge/hyprland-synthetic-dispatch-r52.md` → `56d6e705
round-52: honest stop after falsification`, and `git diff 56d6e705 ad4bf205 --stat --
corpus/knowledge/ corpus/README.md` → empty. It stays indexed at `corpus/README.md:80` with its
18-row proposition table at entry lines 13-30.

The only committed C2 instrument is scoped to a different entry. At tip it prints green:

```
$ python3 -I <lane>/quality/counters/c2-r51-dispatch-entry.py --repo <lane> --rev ad4bf205… --work …/c2-tip
C2_R51: a ok=1 index_row=`knowledge/hyprland-dispatcher-dispatch-r51.md` …
C2_R51: b ok=1 rows=6/2 pins=6
C2_R51: c ok=1 body_shingles=3364 files=66+cand3 max=0.1%
C2_R51: d ok=1 held=7/3 lines=8 untargeted=1 tokens=14
C2_R51: clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET rev=ad4bf205…
```

`ENTRY` is the constant `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md`
(`c2-r51-dispatch-entry.py:57`), it refuses a base that already holds that file (`:652-656`), and
the CLI is `--repo/--rev/--work` with no entry or old-bytes input (`:638-641`). It never reads the
r52 entry, so **a green C2 line at tip is not evidence about the defective entry** — the coverage
gap the frozen C2 targets is exactly this.

Mechanical re-derivation of the three routed defects against the entry's own pinned bytes. Pins
verified against the committed digest list first:
`git show ad4bf205:.ufo/waves/round-52/fetch/SHA256SUMS` records
`a83abeb5…  Hyprland-ConfigActions.cpp` and `7248cbb8…  Hyprland-legacy-DispatcherTranslator.cpp`,
and `git show ad4bf205:.ufo/waves/round-52/fetch/<pin> | sha256sum` returns exactly those digests.

| proposition (entry line) | cited pin:span | measured | class |
|---|---|---|---|
| P16 (:28) | `Hyprland-ConfigActions.cpp:1554-1558,1576` | quote is a splice: `:1554` is `sendKeyboardMods(modMask, 0, 0, 0);`, `:1556-1557` are `if (S.m_passPressed == 1) {` / `if (!isMouse)`, `:1558` is `sendKeyboardKey(…)`; the collapsed quote does **not** occur in the file (`P16 contiguous-in-file: False`) | quote not verbatim in span — mechanically catchable |
| P17 (:29) | `Hyprland-legacy-DispatcherTranslator.cpp:619-622` | the repeat branch at `:621` (`if (keyState == 2 && result.success)` / `:622 result = sendshortcut(modifiedArgs);`) lies inside `sendkeystate` (`:591-627`); `sendshortcut` is `:531-…`. The quote **is** verbatim in the cited span | false subject — quote/pin binding passes |
| P18 (:30) | `Hyprland-legacy-DispatcherTranslator.cpp:574` | the keysym loop is `:565-571` (closes at `:571`); `:574 return … "sendshortcut: key not found"` sits **after** the loop, inside the cache-miss branch opened at `:559`. The quote **is** verbatim at `:574` | false localization — quote/pin binding passes |

Across all 18 rows: quote-in-cited-span binding holds 17/18 (only P16 misses); whole-file binding
also 17/18; longest quote 19 words (limit 25). So the three defects are not one class:

- **P16 is the only one a quote→pin counter can reject.** A contiguous-within-cited-span clause
  catches it and nothing else in the table.
- **P17 and P18 pass the strongest quote/pin binding the r51 counter family implements.** Their
  defects are proposition-level: a subject-name claim and a scope claim that contradict the pin's
  structure. A counter of that family therefore *cannot* satisfy the frozen sentence "rejects the
  old bytes"; it would accept the unrepaired entry for two of the three propositions.
- To reject old P17 the counter must bind the proposition's named function to the pin's actual
  function span around the cited lines (`sendshortcut` ≠ the `sendkeystate` body at 619-622). To
  reject old P18 it must bind an "inside the X" claim to the innermost enclosing construct of the
  cited line (574 is outside the loop and inside the cache-miss branch). Both are mechanical over
  the pin bytes; neither is a quote check.

Routed r52 defects other than P16-P18, checked at tip and still open:
`corpus/lessons/round-52.md:5-17` `## Gate` carries no per-row record (URL, access date, ≤25-word
located quote) for S370-S373 — it carries only the instruction to record them; `:23-27` `##
Changes` still reads "Pending final integration revisions and receipts" after the r52 changes
landed. QUALITY 17 distinct-scope review for the reused URLs is not measurable offline here; I
assert nothing about it.

**Seat limit, stated as the lane requires:** this seat is a leaf wave seat, not an independent
non-author reviewer. The P16-P18 measurements above are mechanical containment/structure evidence
against pinned bytes; they do not discharge C2's "independent reviewer checks source truth", and
they cover the three routed propositions, not the entailment of the other 15.

## Axis statement

No committed change was made by this seat, so no axis move is claimed. What the measurements buy:

- **operability:** the C1 baseline is now a fixture matrix with pre-registered expectations and
  exact exit codes — two total bypasses (generic description, ledger self-pointer), four correctly
  rejected classes, one population-identity divergence, one delegated-selftest ambiguity. A
  round-53 counter either misses all of the first two classes or it does not meet the frozen text.
- **coverage:** the r52 entry is pinned as still unrepaired at tip with per-proposition evidence of
  *which* counter clause can catch which defect, so a C2 counter that binds quotes only is known in
  advance to be insufficient for P17/P18. The repair obligation (append-only corrected rows, old
  rows retained and rejected) and the counter contract are both concrete.

## Limits / unknowns

- I did not run the r52 draft counters (they are not in the tree at tip) or the checker's own
  `--selftest` beyond the invocation the counter makes; I did not run `scripts/sources-census.sh`
  (campaign script, out of bounds this round), so no W04/registry census figure is re-derived here.
- The fixture matrix covers the frozen forgery classes I could construct from committed grammar;
  other spellings (symlink alias rows, gitlink rows, checker substitution) are unmeasured beyond
  the population divergence recorded above.
- No repair, counter, or commit exists at tip, so C1 and C2 are **unmeasured as predicates**, not
  failing: the only honest reading of ad4bf205 is "requirements unmet, baseline established".

## Trailer

Attacked predicate: frozen C1 operability predicate (new scratch-aware counter, explicit selftest,
production-ledger `TARGET_MET`, no-work and each frozen forgery `TARGET_MISSED`, exact population
coverage, non-self pointers) and frozen C2 coverage predicate (append-only P16-P18 repair against
opened pinned bytes, a counter rejecting the old bytes and accepting the corrected entry with
quote/pin/proposition bindings), both at base tip `ad4bf2059bcfafe63671d262222908ee1fe8001c`
(`.ufo/waves/round-53/claims-frozen.md:5-11`).

Exact commands/output: quoted inline above — production C1 run (`population=82 … verdict=TARGET_MET`,
exit 0), base no-work control (`verdict=TARGET_MISSED ledger=absent population=79`, exit 1), the
eight fixture commits and their exact verdict lines (two `TARGET_MET` bypasses at exit 0;
`dup=1`, `empty_desc=82`, `uncovered=1` ×2, `bad_pointer=22`, `population=84` vs checker `83` all
exit 1), `c2-r51-dispatch-entry.py` at tip (`clauses_met=4 verdict=TARGET_MET`, exit 0, scoring
`…-r51.md`), the pin-digest check against `.ufo/waves/round-52/fetch/SHA256SUMS`, and the
quote-containment re-derivation (18 props, 17/18 in-span, P16 the only miss, max 19 words).
Fixture git repositories were created only under `/fast/scratch/hyaku/mado-r53/R53Five50`, each
with `git rev-parse --show-toplevel` asserted to equal its own path before any mutation; no lane
or fleet file was touched.

Newly opened external sources: none. No URL was fetched and no network egress occurred; every
source byte cited here is committed lane content at `ad4bf205`, and the two pinned Hyprland files
were read from `.ufo/waves/round-52/fetch/` at their recorded digests
(`a83abeb5…` `Hyprland-ConfigActions.cpp`, `7248cbb8…` `Hyprland-legacy-DispatcherTranslator.cpp`,
recorded access date 2026-10-27 in the entry trailer at `corpus/knowledge/hyprland-synthetic-dispatch-r52.md:32`).
Located quotes are the entry and pin lines given in the C2 table.

Tools installed/updated: none (pacman transactions paused; install path unused).

Disk guard: `/fast` 594G available before and after (`df -h /fast`); no ENOSPC.

Scratch: `/fast/scratch/hyaku/mado-r53/R53Five50` removed before yield.

Report path (relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`): `.ufo/waves/round-53/w1/R53Five50.md`

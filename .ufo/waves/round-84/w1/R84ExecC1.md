# R84ExecC1 — full frozen C1 counter

## Result and scope

PASS: counter exit 0, TARGET_MET. Candidate 61/61; held tool 58/61; mutants killed 41/41; carried controls parsed-equal 58/58; candidate tool selftest 139/139. All three new duplicate-identity cases returned setup refusal rc2 and scored correct. No source edits.

Axes: frozen-input fidelity, declared-case correctness, mutation sensitivity, held-control separation, containment. Only the explicitly assigned full counter was executed; no unrelated build/lint/test or live desktop calls.

## Method and exact inputs

The counter and both control files were extracted with read-only `git show REV:path` from the specified frozen revision into exclusive scratch. The counter extracted candidate and held tool bytes itself through read-only git commands. No clone, git/jj mutation, credentials, sessions, compositor, configuration, service, or PATH-directory writes. No tool install/update. LSP unavailable in the exposed tool inventory; no symbol/refactor work was needed.

Frozen revision: `3f9eec3906ddd1492e8bc08325e83064f00111ea`
Base revision: `7fd43921294116299dfce1443d56a951b9c81493`

Input SHA256:

- `quality/counters/c1-r84-namespaces.py`: `3b9fd395c3cbf641dda777f8831d0f360952d10203e34ddccbe47621e727135e`
- `.ufo/waves/round-84/controls/c1-cases-r84.json`: `5c9ce3891e1ec4be1820d229bbcfddfa5b61cfbd0d02cc93252ac38c6dd9e883`
- `.ufo/waves/round-83/controls/c1-cases-r83.json`: `e4409dabcf74f32307f14b31afb85091bca7d584771076bdb9a3b336bc9512c4`

## Defects and limitations

No observed mismatch against the assigned C1 predicate and no missing-anchor mutant failures. Documentation defect in the frozen counter module header (lines 4–18): it describes 47 carried cases, a 58-case target, 38 mutants, and base 52/58; actual constants and observed contract are 58 carried, 61 cases, 41 mutants, base 58/61. The temporary-directory prefix at line 454 remains `c1-r82-`; cosmetic historical naming only. Neither was changed under the no-source-edit boundary.

The result establishes only this declared finite case set and these 41 mutations; it does not establish global protocol namespace uniqueness, counter causal-cheat resistance, or host behavior. Held per-case failures and child selftest stdout are not printed by the counter; retained evidence includes its aggregate base/selftest contract, not invented detailed child output. Full counter stderr was empty.

## Receipt

Command (absolute scratch inputs intentionally avoid relative writes from the fleet root):

```sh
python3 -I /fast/scratch/hyaku/mado-r84/R84ExecC1/quality/counters/c1-r84-namespaces.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev 3f9eec3906ddd1492e8bc08325e83064f00111ea --base-rev 7fd43921294116299dfce1443d56a951b9c81493 --controls /fast/scratch/hyaku/mado-r84/R84ExecC1/.ufo/waves/round-84/controls/c1-cases-r84.json --carried /fast/scratch/hyaku/mado-r84/R84ExecC1/.ufo/waves/round-83/controls/c1-cases-r83.json --scratch-root /fast/scratch/hyaku/mado-r84/R84ExecC1/counter-work
```

Working directory: `/fast/scratch/hyaku/mado-r84/R84ExecC1`.
Exit: `0`. Elapsed seconds: `82.015`.

Complete stdout:

```text
MADO_R84_CASE: name=host-top rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R84_CASE: name=bottom-bar rc=0 box=MATCH reserved=EQ band=30 expected=30 verdict=CLEAN correct=yes
MADO_R84_CASE: name=top-margin-int rc=0 box=MATCH reserved=EQ band=38 expected=38 verdict=CLEAN correct=yes
MADO_R84_CASE: name=top-margin-css-2 rc=0 box=MATCH reserved=EQ band=38 expected=38 verdict=CLEAN correct=yes
MADO_R84_CASE: name=top-margin-asym rc=0 box=MATCH reserved=EQ band=42 expected=42 verdict=CLEAN correct=yes
MADO_R84_CASE: name=bottom-margin rc=0 box=MATCH reserved=EQ band=46 expected=46 verdict=CLEAN correct=yes
MADO_R84_CASE: name=left-margin rc=0 box=MATCH reserved=EQ band=52 expected=52 verdict=CLEAN correct=yes
MADO_R84_CASE: name=right-margin rc=0 box=MATCH reserved=EQ band=46 expected=46 verdict=CLEAN correct=yes
MADO_R84_CASE: name=right-zero-margin rc=0 box=MATCH reserved=EQ band=40 expected=40 verdict=CLEAN correct=yes
MADO_R84_CASE: name=layer-bottom rc=0 box=MATCH reserved=EQ band=28 expected=28 verdict=CLEAN correct=yes
MADO_R84_CASE: name=output-exclusion rc=0 box=MATCH reserved=EQ band=24 expected=24 verdict=CLEAN correct=yes
MADO_R84_CASE: name=output-excluded rc=3 box=NOT_ON_MONITOR reserved=NOT_APPLIED band=None expected=None verdict=NO_BAR correct=yes
MADO_R84_CASE: name=width-with-margins rc=0 box=MATCH reserved=EQ band=34 expected=34 verdict=CLEAN correct=yes
MADO_R84_CASE: name=exclusive-false rc=0 box=MATCH reserved=NOT_APPLIED band=0 expected=26 verdict=CLEAN correct=yes
MADO_R84_CASE: name=second-consumer rc=0 box=MATCH reserved=GT band=60 expected=34 verdict=CLEAN correct=yes
MADO_R84_CASE: name=reserved-differ rc=1 box=MATCH reserved=DIFFER band=26 expected=34 verdict=DIFFER correct=yes
MADO_R84_CASE: name=dynamic-cross rc=3 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R84_CASE: name=negative-margin-refused rc=3 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R84_CASE: name=static-composed rc=0 box=MATCH reserved=EQ band=60 expected=60 verdict=CLEAN correct=yes
MADO_R84_CASE: name=static-other-edge rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R84_CASE: name=static-exclusive-false rc=0 box=MATCH reserved=NOT_APPLIED band=26 expected=52 verdict=CLEAN correct=yes
MADO_R84_CASE: name=static-last-wins rc=0 box=MATCH reserved=EQ band=52 expected=52 verdict=CLEAN correct=yes
MADO_R84_CASE: name=static-source-refused rc=3 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R84_CASE: name=overlay-compose-top rc=0 box=MATCH reserved=EQ band=66 expected=66 verdict=CLEAN correct=yes
MADO_R84_CASE: name=bottom-level-first rc=0 box=MATCH reserved=EQ band=66 expected=66 verdict=CLEAN correct=yes
MADO_R84_CASE: name=same-level-order rc=0 box=MATCH reserved=EQ band=62 expected=62 verdict=CLEAN correct=yes
MADO_R84_CASE: name=exclusive-edge-matched rc=0 box=MATCH reserved=EQ band=56 expected=56 verdict=CLEAN correct=yes
MADO_R84_CASE: name=anchor-unmatched rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R84_CASE: name=overlay-unexclusive-full rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R84_CASE: name=ls-area-invalid rc=0 box=MATCH reserved=EQ band=0 expected=0 verdict=CLEAN correct=yes
MADO_R84_CASE: name=negative-margin-skip rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R84_CASE: name=empty-box-skip rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R84_CASE: name=full-box-vs-usable rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R84_CASE: name=overflow-tie-negative rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R84_CASE: name=auto-dynamic-band-refused rc=3 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R84_CASE: name=auto-corner-edge rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R84_CASE: name=auto-all-four-edge rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R84_CASE: name=auto-parallel-edge rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R84_CASE: name=auto-left-dock rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R84_CASE: name=alloc-dyn-height-top rc=0 box=MATCH reserved=EQ band=34 expected=34 verdict=CLEAN correct=yes
MADO_R84_CASE: name=alloc-dyn-height-margin rc=0 box=MATCH reserved=EQ band=38 expected=38 verdict=CLEAN correct=yes
MADO_R84_CASE: name=alloc-dyn-width-dock rc=0 box=MATCH reserved=EQ band=60 expected=60 verdict=CLEAN correct=yes
MADO_R84_CASE: name=alloc-zero-refused rc=3 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R84_CASE: name=alloc-negative-refused rc=2 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R84_CASE: name=alloc-unknown-namespace rc=2 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R84_CASE: name=alloc-explicit-ignored rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R84_CASE: name=alloc-composition-dyn-bar rc=0 box=MATCH reserved=EQ band=46 expected=46 verdict=CLEAN correct=yes
MADO_R84_CASE: name=extra-dyn-band-top rc=0 box=MATCH reserved=EQ band=66 expected=66 verdict=CLEAN correct=yes
MADO_R84_CASE: name=extra-dyn-band-dock rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R84_CASE: name=extra-dyn-band-explicit rc=0 box=MATCH reserved=EQ band=66 expected=66 verdict=CLEAN correct=yes
MADO_R84_CASE: name=extra-dyn-band-bottom rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R84_CASE: name=extra-dyn-band-zero-alloc rc=3 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R84_CASE: name=alloc-live-band-differs rc=1 box=DIFFER reserved=EQ band=34 expected=34 verdict=DIFFER correct=yes
MADO_R84_CASE: name=alloc-bool-refused rc=2 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R84_CASE: name=alloc-two-namespaces rc=0 box=MATCH reserved=EQ band=74 expected=74 verdict=CLEAN correct=yes
MADO_R84_CASE: name=bar-dyn-band-no-alloc rc=3 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R84_CASE: name=alloc-live-box-differs-composed rc=1 box=DIFFER reserved=EQ band=34 expected=34 verdict=DIFFER correct=yes
MADO_R84_CASE: name=bar-dyn-band-exclusive-false rc=3 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R84_CASE: name=duplicate-extra-namespaces rc=2 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R84_CASE: name=duplicate-bar-namespace rc=2 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R84_CASE: name=duplicate-allocation-keys rc=2 box=None reserved=None band=None expected=None verdict=None correct=yes
MADO_R84_MUTANT: name=opposite-margin-dropped correct=50/61 killed=yes
MADO_R84_MUTANT: name=horizontal-margin-leak correct=50/61 killed=yes
MADO_R84_MUTANT: name=level-bottom-swap correct=60/61 killed=yes
MADO_R84_MUTANT: name=right-extent-flip correct=59/61 killed=yes
MADO_R84_MUTANT: name=per-side-margin-dropped correct=60/61 killed=yes
MADO_R84_MUTANT: name=negative-margin-accepted correct=60/61 killed=yes
MADO_R84_MUTANT: name=opposite-edge-wrong correct=60/61 killed=yes
MADO_R84_MUTANT: name=static-dropped correct=58/61 killed=yes
MADO_R84_MUTANT: name=static-order-swapped correct=58/61 killed=yes
MADO_R84_MUTANT: name=static-first-wins correct=57/61 killed=yes
MADO_R84_MUTANT: name=static-box-unoffset correct=57/61 killed=yes
MADO_R84_MUTANT: name=static-selector-ignored correct=60/61 killed=yes
MADO_R84_MUTANT: name=attr-edge-order correct=39/61 killed=yes
MADO_R84_MUTANT: name=running-bounds-ignored correct=43/61 killed=yes
MADO_R84_MUTANT: name=exclusive-edge-ignored correct=60/61 killed=yes
MADO_R84_MUTANT: name=edge-guard-dropped correct=60/61 killed=yes
MADO_R84_MUTANT: name=invalid-area-kept correct=60/61 killed=yes
MADO_R84_MUTANT: name=full-box-uses-usable correct=60/61 killed=yes
MADO_R84_MUTANT: name=empty-box-contributes correct=60/61 killed=yes
MADO_R84_MUTANT: name=same-level-order-ignored correct=60/61 killed=yes
MADO_R84_MUTANT: name=zone-margin-not-added correct=60/61 killed=yes
MADO_R84_MUTANT: name=attribution-not-summed correct=39/61 killed=yes
MADO_R84_MUTANT: name=tie-round-trunc correct=60/61 killed=yes
MADO_R84_MUTANT: name=round-width-spec correct=60/61 killed=yes
MADO_R84_MUTANT: name=auto-gate-open correct=58/61 killed=yes
MADO_R84_MUTANT: name=auto-gate-and correct=57/61 killed=yes
MADO_R84_MUTANT: name=auto-axis-swapped correct=59/61 killed=yes
MADO_R84_MUTANT: name=auto-dynamic-kept correct=60/61 killed=yes
MADO_R84_MUTANT: name=alloc-explicit-overridden correct=41/61 killed=yes
MADO_R84_MUTANT: name=alloc-zero-accepted correct=59/61 killed=yes
MADO_R84_MUTANT: name=alloc-axis-lost correct=55/61 killed=yes
MADO_R84_MUTANT: name=alloc-negative-accepted correct=60/61 killed=yes
MADO_R84_MUTANT: name=alloc-unknown-kept correct=60/61 killed=yes
MADO_R84_MUTANT: name=alloc-width-lost correct=60/61 killed=yes
MADO_R84_MUTANT: name=box-verdict-blind correct=60/61 killed=yes
MADO_R84_MUTANT: name=box-verdict-blind-single correct=60/61 killed=yes
MADO_R84_MUTANT: name=extra-alloc-ignored correct=52/61 killed=yes
MADO_R84_MUTANT: name=bar-band-no-refusal correct=60/61 killed=yes
MADO_R84_MUTANT: name=alloc-resolved-set-bar-only correct=55/61 killed=yes
MADO_R84_MUTANT: name=duplicate-namespace-tolerated correct=59/61 killed=yes
MADO_R84_MUTANT: name=duplicate-allocation-kept correct=60/61 killed=yes
MADO_R84_BASE: correct=58/61 rule=held-r83-model(namespace-unchecked) base_rev=7fd43921294116299dfce1443d56a951b9c81493 base_sha256=8b17706014e6708a11413f0bd6c3398ca4e1b95b40b9c2d51f80f5064c677207
MADO_R84_CONTROL: sha256=5c9ce3891e1ec4be1820d229bbcfddfa5b61cfbd0d02cc93252ac38c6dd9e883 carried=58/58
MADO_R84_BARFOOT: cases=61 correct=61 mutants=41 killed=41 base_correct=58/61 carried=58/58 tool_selftest=139/139 verdict=TARGET_MET rev=3f9eec3906ddd1492e8bc08325e83064f00111ea tool_sha256=72456666a31927dfc46f955f41b3aa57b2215a8fcd8dc736fc302d7b58830c7f
```

Complete stderr: empty (0 bytes).

## Self-evaluation

Accuracy 4/5: exact observed receipt retained, but child details unavailable from counter output. Completeness 5/5: all explicitly requested metrics measured and full stdout/exit retained. Clarity 4/5: long stdout is required evidence rather than concise summary. Actionability 5/5: hashes, command, revision and documentation defect locations supplied. Conciseness 4/5: receipt dominates report length. Overall 4.4/5. Improvement: maintainers can refresh the stale header; expanding child diagnostics is outside this assignment. The assessment is bounded to the requested counter execution.

Scratch cleanup: exclusive scratch removed after retaining this receipt; no residual scratch artifacts intended.

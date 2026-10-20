# AttackU7Join — U7 join: required ids, facets, inverse, reciprocal paths

**Seat:** `MadoR16.AttackU7Join` (reviewer, leaf)
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`
**Scope:** `.ufo/waves/round-16/measure.py` U7 branch (required source ids, facets, inverse); `corpus/knowledge/waybar-observation-boundaries-r16.md`; `corpus/SOURCES.md` S053–S055 reciprocal rows; `corpus/README.md` index row.
**Method:** source reading only. `measure.py` was not executed. Read-only git status/ls-files. The two tagged Waybar raw URLs were fetched to stdout and hashed (nothing written). Registry cell counts were taken by a text count of `SOURCES.md`. No install, package, service, or producer operation.
**Tooling:** none installed or updated.

## Findings, most severe first

### F1 (medium, measurement fidelity): heading parser is fence-blind
- `level2_sections` (`measure.py:128-144`; loop at `:136-143`) and `body_facets` (`:93-125`) treat every line matching `^##(?!#)` as a heading. They never track ``` or `~~~` fences. Neither `measure.py` in round-15 nor round-16 contains any fence handling (grep for "fence" and "```" returns nothing in either file).
- Counterexample (bounded, reasoned from code, not executed): a `corpus/knowledge/*.md` note whose head-15 is valid (`source:` naming S053 and S054 with reciprocal mined rows, `verified-at:`, `recheck:`, `covers: U7`), and whose body contains only a fenced block with `## Producer contract`, `## Renderer boundary`, `## Safe observation`, `## Unexercised rendering`, and `[UNK]`. `u7_facets` (`:168-189`) returns all true, `inverse` is true, and the note is admitted at `:294-295`. No prose section is needed.
- The U7 docstring (`:168-177`) and the U6 docstring (`:147-154`) say a "prose-only or deeper-heading mention cannot admit the item." Fenced level-2 headings are neither prose nor deeper headings, so the stated contract has a gap here.
- The current U7 note has no fences (checked by reading all 78 lines), so the present result is not caused by this gap.
- Premise check: round-15 `AttackMetric.md` row C (line 21) states "the parser ignores fences." The code in both round-15 and round-16 does not ignore fences. Treat that premise as wrong for the counter.
- Fix options: strip fenced spans before `level2_sections`/`body_facets`, or document fences as an explicit admission limit.

### F2 (low, diagnostic): facets fields are last-candidate-wins
- `u7_facets_observed = facets` (`measure.py:286`) is overwritten on each U7 candidate. It is emitted at `:426` as `coverage.u7_facets`. The same pattern exists for U6 at `:267` and `:423`.
- Counterexample: two notes that both carry `covers: U7`. The count and `joined` stay correct, because each note is judged independently. `coverage.u7_facets` describes whichever note sorts last in `ls-tree` order, which may be the note that failed. `u7_candidates` is complete, so this is a misleading summary field, not a score error.

### F3 (low, declared limit): `[UNK]` check is a substring test
- `u7_facets` (`:185-187`) passes if the lowercased section contains `[unk]` anywhere, including a negated phrase ("No [UNK] remains") or text inside a `### [UNK]` subheading. `level2_sections` (`:137`, regex `^##(?!#)`) keeps level-3 lines in the enclosing level-2 body, so a deeper `###` line counts toward the body. That behavior is documented in the `level2_sections` docstring (`:131-132`). The U7 docstring's "deeper-heading mention cannot admit" is accurate only when the deeper heading is used as the key, not for `[UNK]` inside a level-3 line in the body.
- This is the same negated-unknown limit that round-15 `AttackMetric.md` row D flagged. It is a declared-policy classifier limit, not a broken promise. The probe checks presence, and body semantics stay with L1.

### F4 (integration-critical, not a code defect): the probe reads committed revisions only
- `source()` runs `git show <rev_sha>:<path>` (`measure.py:70-71`). `try_source` (`:74-79`) returns None for missing paths.
- Current git state (read-only `git status --porcelain`): ` M corpus/QUALITY.md`, ` M corpus/README.md`, ` M corpus/SOURCES.md`, `?? .ufo/waves/round-16/`, `?? corpus/knowledge/waybar-observation-boundaries-r16.md`, `?? corpus/lessons/round-16.md`, `?? tools/mado-action-plan.py`. HEAD is `32c4fda`.
- At HEAD, the probe reports: `round16_required.S053/S054` present=false; `u7_present`=false; the U7 join cannot be credited (no U7 candidate, so `coverage.u7_candidates` is empty); the waybar note is absent from `notes` (it is untracked), so it is not in `navigation.missing` either; all three `safety_artifacts` present=false. Exact `coverage.count` at HEAD was not computed (no run). Any reading of "U7 = 7/7" from this counter requires L1 to commit first and then run at that SHA. Seats may not commit.
- Recording this so a HEAD-bound run is not read as a U7 regression.

## Verified clean (the requested join surfaces)

1. **Required ids.** `U7_SOURCES = ('S053', 'S054')` (`measure.py:206`). S055 is absent from the requirement (`:203-205`), so own-work safety cannot credit U7. The 13-cell registry parse is complete: text count of `corpus/SOURCES.md` shows 0 rows with a split count other than 13, and the S053, S054, and S055 rows each have 13 cells. No row is silently dropped at `:196`.
2. **Reserved rows.** `SOURCES.md:65` (S053) and `:66` (S054) are `mined`, tier `A`, and `used-by` exactly `corpus/knowledge/waybar-observation-boundaries-r16.md`. `mined_ab` (`:86-90`) therefore passes for both. The path in `used_by` matches the `ls-tree` path form (`corpus/knowledge/...`).
3. **Inverse / reciprocal.** The only `mined` rows whose `used-by` names the note are S053 and S054 (grep of `corpus/SOURCES.md` and `corpus/lessons/round-16.md` for the note path returns only SOURCES:65-66). Both appear in the note's line 1 `source:` line, so `inverse` (`:284-285`) is true. S055 `used-by` is `corpus/lessons/round-16.md` (`SOURCES.md:67`), not the note, so it does not affect the inverse. If S055 were later named in the note's `used-by` without being cited, the inverse would fail, which matches the docstring at `:281-283`.
4. **Head-15 provenance.** Note lines 1–4: `source:` (S053 and S054 with tagged URLs), `verified-at: 2026-10-20`, `recheck:` with a non-empty value, `covers: U7` exactly once. All within the first 15 lines (`:223`, `:225`, `:228-229`).
5. **Facets.** Exact level-2 headings present: `## Producer contract` (note line 13), `## Renderer boundary` (`:32`), `## Safe observation` (`:54`), `## Unexercised rendering` (`:69`). `[UNK]` appears inside the rendering section at line 71 (`:71`).
6. **Index.** `corpus/README.md:41` has one table row for `knowledge/waybar-observation-boundaries-r16.md` (grep of README: that row only, plus the prose link at `:112`). The navigation regex (`measure.py:315`) matches it once in the working tree.
7. **Source binding.** `.ufo/waves/round-16/evidence/source-bindings.json` records S053 sha256 `efb6a63a3d7f125840d4c4a49956664070f36231724e7aa0fa281e6d2de30d82`, 6656 bytes, and S054 sha256 `2232f7f7141caa5958344e1e6a0ab8eec6321994da1fecd704345aeb513b291f`, 8746 bytes. A live curl of both tagged URLs (hashed to stdout, nothing written) matches both digests and byte counts. The same digests appear in `SOURCES.md:65-66`.
8. **Note claims spot-checked against tagged source.**
   - `custom.cpp` (S054): `Custom::update` hides on empty output or nonzero exit for `exec`/`exec-if` (note line 34-35 matches); `parseOutputJson` breaks after the first line (`break;` after the first `getline` iteration, matches note line 21); `label_.set_markup(str)` (matches note line 38); `hide-empty-text` and empty formatted text hide (matches note line 35-36); raw lines 0/1/2 map to text/tooltip/class (matches note line 19-20 and the raw description).
   - Manual (S053): "displays either the output of a script or static text" (note line 15 quotes it), `format` default `{text}`, `restart-interval`, `signal` update, `{icon}` from percentage (matches note lines 15-28).
   - `escape` default false (note line 49) was not checked line-by-line in the manual. The code reads `escape` only when it is a true bool, which is consistent.

## Verification gaps
- `measure.py` was not executed, per the no-execution rule. Facet, inverse and count results are reasoned from code and the text counts above, not from a run. L1 should run the probe once, at a committed SHA.
- The fence counterexample (F1) and the last-candidate-wins diagnostics (F2) were reasoned from code only.
- I did not verify S055's content, `QUALITY.md` (C3), or `SCORECARD.md`/`README` frontier prose. Those belong to other seats.
- The live Waybar bar text and rendering are not in scope. The note correctly marks them `[UNK]` (note lines 71-78).

## Recommendations for L1 (integration)
1. Commit the lane's round-16 artifacts (or a reviewed revision) before the one-time measurement, then run `measure.py <sha>` once. A HEAD-bound run reads U7 as absent by construction.
2. Decide on F1: strip fenced spans in `level2_sections`/`body_facets`, or record "fences are not stripped" as an explicit U5/U6/U7 admission limit in the docstrings and SCORECARD.
3. Optionally make F2 deterministic: report the facets of the admitted candidate, or of all candidates keyed by path.
4. Keep S055 uncredited to U7 as the current code does. The note and README already say the rendering stays `[UNK]`.

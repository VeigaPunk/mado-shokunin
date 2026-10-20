# ReciprocalJoin — U7 reciprocal source/used-by counting and inverse join

Seat: `MadoR16.ReciprocalJoin` (reviewer, leaf). Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Baseline commit read: `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea` (`git show <rev>:<path>` only).
Working tree also read (uncommitted, not measured): `corpus/SOURCES.md` rows S053–S055, untracked `corpus/knowledge/waybar-observation-boundaries-r16.md`, `.ufo/waves/round-16/measure.py`.

Method: read-only. Inline Python over `git show` bytes and `grep`/`read` of the working tree. No `measure.py` run, no gate, no tests, no build, no installs, no edits outside this report. Counts below are my re-derivation from committed bytes, not a replay of any lane script.

## Verdict

The round-15 reciprocal rule is one-directional and head-scoped, and the round-16 U7 branch inherits that. On the working-tree draft, the U7 join is correct for the two reserved rows, but the design has three defects the L1 must decide before counting U7: (1) the reciprocity guarantee is not symmetric, (2) the lane has two incompatible definitions of "citing", and (3) generalising the rule to U1–U4 silently drops the score from 8.5714 to 5.7143. Silent-drop hazards exist but are inert at the current bytes.

## Findings, most severe first

### F1 — MAJOR — Universal reciprocity would cut the baseline from 6/7 to 4/7 (decision, not a silent extension)

Round-15 rule (`round-15/measure.py:244-245, 257-258`): the inverse check runs only for U5 and U6. For U1–U4 there is no inverse check at all.

Counterfactual at `32c4fda`, applying the U5/U6 inverse rule to every item:

| Item | Note | Head-15 cites all mined rows that name it? | Counted by round-15 rule | Counted if universal |
|---|---|---|---|---|
| U1 | window-rule-effects-getprop.md | yes | yes | yes |
| U2 | hyprland-config-era-r12.md | **no — S017** | yes | **no** |
| U3 | xdg-portal-routing-r12.md | yes | yes | yes |
| U4 | wayland-protocol-boundaries-r13.md | **no — S049** | yes | **no** |
| U5 | output-colour-boundaries-r14.md | yes | yes | yes |
| U6 | input-debugging-boundaries-r15.md | yes | yes | yes |

- Round-15 rule: 6/7 = **8.5714** (matches the round-15 closure's delivered figure).
- Universal inverse: 4/7 = **5.7143**.
- Evidence: `SOURCES.md:29` (S017 row) names `corpus/knowledge/hyprland-config-era-r12.md`, but that note's head-15 `source:` (line 3) cites S021–S029 and S030 only; the body does cite S017 (`hyprland-config-era-r12.md:133`). `SOURCES.md:61` (S049) names `corpus/knowledge/wayland-protocol-boundaries-r13.md`, whose head-15 source (line 1) omits S049; the body cites it at lines 116 and 122.
- Consequence for U7: on the working-tree draft, U7 is predicted to join. Under round-15 rules the target would be 7/7 = 10.0000. Under universal reciprocity it would be 5/7 = 7.1429.

Fix options (L1 decision; do not implement silently in the counter):
- (a) Repair the registry in place: drop the stale path from `used-by` for S017/S049, or add the id to the head line. `used-by` is the one mutable column; log old→new in the round lesson.
- (b) Keep round-15 scope for U1–U6 and state the asymmetry as a known limit, as the round-15 closure did.
- Do not change the U1–U6 score rule inside round 16 without an explicit decision: the closure at `corpus/lessons/round-15-verifier-spotcheck.md` says broadening is not imposed.

### F2 — MAJOR — Two incompatible definitions of "citing" exist in the lane

- Counter (round-15 and draft `measure.py`): citation = `\bS\d{3,}\b` on the **head-15 `source:` line** only (`round-15/measure.py:171, 178`; draft `measure.py:216, 223`).
- Lane census `.ufo/evidence/round-12/after-measure.sh:25`: `grep -qw "$i" "$p"` on the **whole file**.
- Fleet census `scripts/sources-census.sh:538-575`: checks only that `used-by` paths exist (E11); no citation check.
- The contract (`.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`, `used-by`) says "paths of the knowledge entries or lessons **citing** the row" and does not say head or body.
- Observed divergence at baseline: S017 and S049 pass the body-grep census and fail the head-15 join (F1). The lane's own census would call the registry clean while the counter's reciprocal fails.

Recommendation: L1 pins one surface for counted items (head-15 is the one the score reads) and writes that into the SKILL row for the measure. Add an informational `cited_not_reciprocal` / `named_not_cited` list to the output for every item, excluded from the score.

### F3 — MEDIUM — Silent exclusions in the join (inert at current bytes; hazard for U7)

Each of these drops evidence without any output line:

1. Cited-but-not-counted rows. The draft computes `mined` (`draft measure.py:224-225`) and `cited` (`:271`) but reports nothing for cited ids that fail `mined`/`used_by`. Baseline examples: `input-debugging-boundaries-r15.md` head cites **S043** (mined; `SOURCES.md:55` used-by names only `wayland-protocol-boundaries-r13.md`) and **S007** (queued); `hyprland-config-era-r12.md` head cites **S030** (rejected). None changes the count, but the note asserts a join the counter does not check. A U7 note citing any extra row (for example S016 or S052) would pass silently.
2. Registry rows silently dropped: `if len(cells) == 13 and re.fullmatch(...)` (`round-15/measure.py:147-150`; draft `:186-189`). A `|` inside any cell removes that row. Baseline: 52 `| S` lines, 52 parsed, 0 unparsed. The registry is last-wins on duplicate ids (`registry[cells[1]] = cells`); baseline has 0 duplicates.
3. `covers` ambiguity: `items = ...; item = items[0] if len(items) == 1 else None` (`round-15:172-173`; draft `:217-218`). A note with two `covers:` lines is excluded with no record. Baseline: none.
4. `used_by` splits on `,` only (`round-15:59-60`; draft `:74-75`). The round-12 census awk splits on `[,;]` (`after-measure.sh:25`) and the fleet census on `,` (`sources-census.sh:562`). Baseline `used-by` cells contain no `;`.
5. Queued and rejected rows that name a note are ignored by both forward and inverse checks (`round-15:179-180, 244-245`). The contract says queued/rejected rows carry `—`, but nothing checks that.

Recommendation: emit `unparsed_rows`, `duplicate_ids`, `ambiguous_covers`, `semicolon_used_by` and `named_by_non_mined` counts. Keep exit 0 per the design, but make each nonzero count visible in the JSON.

### F4 — MEDIUM — Facet fields are last-wins, so output can misattribute the counted note

- `u4_facets` (`round-15:182, 204`), `u6_facets_observed` (`:207, :259`), and the draft `u7_facets_observed` (`draft :209, :278`) are overwritten on every candidate. With two candidate notes, the reported facets may belong to a note that did not count.
- `u7_candidates` already holds per-candidate facets; the summary field should be dropped or derived from the counted entry.

### F5 — LOW — Heading parser is fence-unaware (no current effect)

`level2_sections` (`round-15:105-121`; draft `:120-136`) matches `^##(?!#)\s+` anywhere, including inside fenced code. A fenced `## Unexercised rendering` followed by `[UNK]` would satisfy `u7_facets`. Baseline check: 0 fenced `##` lines across all knowledge notes. The draft U7 note has no code fences. Still a hole for a rubric that says "a prose-only or deeper-heading mention cannot admit the item": fences are a third case. Fix: track fence state and skip fenced lines.

### F6 — LOW — Single-line `source:` assumption

`provenance = re.search(r'^source:.*$', ...)` takes the first match on one line. A wrapped source line loses its later ids without a record. Baseline: every noted note has exactly one `source:` line in the first 15 lines; notes without `source:` (19 legacy notes) are skipped by design. Add an assertion or count.

### F7 — INFO — Draft U7 branch, as written, joins correctly on the working tree (prediction, not measurement)

Working-tree bytes:
- `SOURCES.md:65` S053 `mined | … | A | … | corpus/knowledge/waybar-observation-boundaries-r16.md`
- `SOURCES.md:66` S054 `mined | … | A | … | corpus/knowledge/waybar-observation-boundaries-r16.md`
- `SOURCES.md:67` S055 `mined | … | corpus/lessons/round-16.md` — does not name the U7 note, so the inverse is not triggered by S055. Good.
- Note head (lines 1–15) cites `S053` and `S054` only; `covers: U7` appears once.
- Level-2 headings present: `## Producer contract` (13), `## Renderer boundary` (28), `## Safe observation` (50), `## Unexercised rendering` (65); `[UNK]` at lines 67–68 inside the last.
- No code fences.

Predicted by the draft rule once committed: U7 joins, `inverse = True`. This is a re-derivation of the rule from bytes, not a run of `measure.py`. Two caveats apply: the measure reads committed revisions only (`git show <sha>:…`), so the uncommitted rows and the untracked note contribute nothing until a commit contains both, and the in-flight S053–S055 lines are `M` in the working tree.

### F8 — INFO — Reserved ids and collisions

- `S053`, `S054`, `S055`: absent from the baseline registry and absent from every committed corpus file. In the working tree they exist only as the three new rows above. No collision.
- `S055` is correctly excluded from U7 credit by the draft (`draft measure.py:195-197`); its `used-by` is a lesson, which is the right boundary for own-work closure evidence.

## Baseline reproduction (re-derived, read-only, committed `32c4fda`)

- Registry: 52 rows; status 40 mined / 8 queued / 4 rejected; tier A 48 / B 1 / C 3.
- Knowledge notes: 29. README index: 29 of 29, missing 0.
- Head-15 with `covers:`: 6 notes (U1, U2, U3, U4, U5, U6). Round-15 rule: 6/7 = 8.5714.
- Mined rows whose `used-by` names a knowledge note but whose head-15 does not cite them: S017 (→ U2 note), S049 (→ U4 note).
- Cited non-reciprocal in head: S030 (rejected, U2 note), S007 (queued, U6 note), S043 (mined, U6 note).
- Duplicate ids 0; `;` in `used-by` 0; reserved S053–S055 absent at baseline.

## Recommendations for the U7 counter (ordered)

1. Keep the U7 rule as drafted (`S053` and `S054` mined, tier A/B, `used-by` exactly the note path, cited on the head line, every other mined row naming the note cited on the head line). It is correct for the working-tree draft.
2. Add the informational `cited_not_reciprocal` and `named_not_cited` lists for all items, outside the score (F2, F3-1).
3. Add the drop counters (F3-2..5) to the JSON output.
4. Replace last-wins facets with per-candidate lists; drop the `*_observed` summary fields (F4).
5. Track fence state in `level2_sections` (F5).
6. L1 decides F1 explicitly, with the 7/7 (round-15 scope) and 5/7 (universal scope) figures on the table, and logs any `used-by` change old→new in the lesson.
7. Measure only at the commit that contains both the S053/S054 rows and the note. A pre-commit measurement shows U7 absent and is not evidence of a failed join.

## Verification gaps

- No counter was executed. All figures are my re-derivation from committed bytes (`git show`) plus working-tree `grep`/`read`.
- The working-tree join prediction (F7) is unmeasured until a committed revision exists.
- I did not verify the source bytes behind the S053/S054 `anchor` digests (`raw sha256 …`); that is the SourcesDraft/WaybarDraft seats' scope.
- I did not assess whether `mined` for S053/S054 is substantively correct; scope is the join.
- Not checked: fleet census with the new rows, since it reads only `used-by` existence.

## Tooling

No tools installed or updated. No `sudo`, `pacman`, or package operations. Read-only Python and `git show` only; nothing written inside the lane except this report.

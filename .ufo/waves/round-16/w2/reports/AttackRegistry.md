# Registry delta — baseline `32c4fda` vs working tree

Scope interpretation: "registry" is `corpus/SOURCES.md` (the 11-column source
registry), matching the round-15 closure's `existing_source_row_changes=[]`
check. `.ufo/waves/round-16/{w1,w2}/reports/swarm-registry.json` are dispatch
member registries (kind/agentId/role), not row/scope registries; they were not
treated as the target.

Verdict: **PASS**. Every existing row cell is byte-identical to baseline; the
three added rows are correctly scoped, correctly keyed and reciprocally joined.
One informational anchor-wording note (S055), no falsification.

## Delta facts (static, no gate/test/measure execution)

| Probe | Observed |
|---|---|
| `git diff 32c4fda -- corpus/SOURCES.md` | 19 insertions, **0 deletions** |
| Row count | 52 → **55**; added `S053`, `S054`, `S055`; removed none |
| Existing-row cell comparison (all 11 columns, all 52 ids) | `existing_row_cell_diffs = []` |
| Column shape | every row, baseline and tree, has exactly 11 cells |
| Id order/uniqueness | S053–S055 appended after S052; no gaps/duplicates/reuse |
| Tier counts | A/B/C 48/1/3 → **51/1/3** (+3 A) |
| Status counts | mined/queued/rejected 40/8/4 → **43/8/4** (+3 mined) |
| Header contract | `Only status, recheck and used-by change in place` line unchanged; round-16 search-log line "No existing row's status/recheck/used-by changes" matches the empty cell diff |
| Added non-row lines | Paths bullet (U7, round 16) and one Search-log paragraph; no existing prose line edited |

Existing historical warnings remain exactly the pre-existing duplicate-URL
pairs (S006/S042; S017/S030/S045). The three new URLs add no duplicate:
`raw.githubusercontent.com/Alexays/Waybar/0.15.0/man/...` and `.../src/modules/custom.cpp`
are unique; S055 is a local own-work path unique to that row.

## New-row scopes and anchors

Independent live read of the two tagged URLs on 2026-10-20 (read-only `curl`,
`sha256sum`, `wc -c`; no execution of either source):

| id | scope claim | anchor evidence |
|---|---|---|
| S053 | "Producer return-type, formatting and scheduling contract, not observed module text" — docs/A | 6656 bytes, sha256 `efb6a63a3d7f125840d4c4a49956664070f36231724e7aa0fa281e6d2de30d82` (matches row and `evidence/source-bindings.json`). Headings present: `# DESCRIPTION` :6, `# CONFIGURATION` :11, `# RETURN-TYPE` :148, `# FORMAT REPLACEMENTS` :168; `exec-if`/`return-type`/`interval`/`signal`/`restart-interval` present. Scope is narrower than the file (static-text path omitted), never broader. |
| S054 | "Static producer-buffer-to-GTK-markup route and hide conditions, not installed-binary equivalence" — code/A | 8746 bytes, sha256 `2232f7f7141caa5958344e1e6a0ab8eec6321994da1fecd704345aeb513b291f` (matches row and bindings). Symbols present: `Custom::update` :162, `parseOutputJson` :169/:257, `parseOutputRaw` :171/:222, `hide-empty-text` :178, `label_.set_markup` :181. `Custom::update` + parse functions match the anchor cell. |
| S055 | "Established host partial-upgrade incident and routed process debt, not host remediation" — own-work/A | File exists at `32c4fda` and in the tree, byte-identical (291 lines, sha256 `58e247f8525483eb7d4cc7a71ac4e64cb2b2ed3e5716af1234c0588cb882928a`). Named sections exist: "Gate and correction evidence — verified, not re-executed" :131, "Routed defects, remediation and retained limits" :252, R15-V1 :254, R15-V2 :268. `32c4fda` is the commit that introduced the closure (291 insertions) and is the round baseline. |

`used-by` joins (static parse, mined rows only):

- S053/S054 → `corpus/knowledge/waybar-observation-boundaries-r16.md`; that
  note's head-15 `source:` line cites S053/S054, carries `verified-at:` and
  `recheck:`, and has exactly one `covers: U7`. No join failure.
- S055 → `corpus/lessons/round-16.md`; the lesson cites S055 in its Gate
  section (lines 59–69). No join failure.
- Every mined row in the tree has a non-`—` `used-by` that actually contains
  its id (`mined missing/uncited used-by = []`).
- U7 inverse (note head line vs rows naming it): the only mined rows whose
  `used-by` names the U7 note are S053/S054, and both are on its head-15
  `source:` line. Clean in both directions.
- Pre-existing head-line inverse exceptions outside the delta, unchanged:
  S017 names `hyprland-config-era-r12.md` but that note's head cites only
  S021–S029/S030; S049 names `wayland-protocol-boundaries-r13.md` but its
  head omits S049. These predate round 16 (no cell changed); they are the
  U2/U4 asymmetry already logged for L1, not new-row defects.
- README index against `corpus/knowledge`: **30 index rows / 30 files**,
  missing `[]`, extra `[]`, duplicates `[]`. The new index row cites
  S053/S054 and the bindings file; it correctly omits S055 because the note
  does not use it.

Quoted evidence in the lesson also checks: S053's DESCRIPTION sentence is
manual line 8 ("The *custom* module displays either the output of a script
or static text.", 13 whitespace words); S055's quoted sentence is closure
lines 161–162 ("These are explicitly hard-coded in-memory controls, not real
pacman dry-run output", 11 whitespace words).

## Precision note (informational, not a falsification)

S055's anchor reads "closure at baseline `32c4fda…`". `32c4fda` is the
integration commit carrying the closure and the round-16 baseline, so the
anchor resolves exactly. The closure itself names a different reviewed
baseline: "Reviewed baseline `ea0446f…`, measured content `5f13870…`,
delivered revision `9ebd737…`". A rechecker following `32c4fda` gets the
correct bytes; the phrase could be misread as the closure's reviewed
baseline. Since the header contract makes `anchor` immutable, this should be
left as-is or handled by an appended erratum, not an in-place rewrite.

## Limits and remaining unknowns

- No `sources-census`, `measure.py`, gate, selftest or any lane check was
  executed (contract). Duplicate detection is my own static table regex; the
  census may normalize URLs more broadly, but both new URLs are unique raw
  paths and the census's existing warning set is unchanged by inspection.
- Source semantics were judged only against the named headings/symbols and
  the note's own layer table; this is not proof that every sentence stays
  within the scope cell, and not proof that a host Waybar binary equals tag
  0.15.0 (the row explicitly disclaims installed-binary equivalence).
- Live fetch shows the tag bytes currently equal the recorded digests; it
  does not establish upstream tag immutability.
- No packages/tools installed or updated; no pacman operation; no live
  compositor/service/input/screenshot/producer probe. Only `git`,
  read-only Python parsing and two `curl` source reads were used.

Confidence: **high** on immutability, row shape, id/key uniqueness and
reciprocal joins; **high** on digest/anchor presence; **medium-high** on
semantic scope adequacy (bounded judgment).

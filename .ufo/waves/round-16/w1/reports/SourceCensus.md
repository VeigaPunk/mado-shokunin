# SourceCensus — round 16 (wave 1)

- **Seat:** `MadoR16.SourceCensus` (scout, read-only)
- **Date:** 2026-10-20
- **Baseline:** `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`
- **Question:** read prior census warnings; identify the required before/end
  census outputs and the mutable-row old→new constraints for `corpus/SOURCES.md`.
- **Method/limits:** static byte reads only (`git show`, `read`, plain Python
  string parsing of the Markdown registry and of `scripts/sources-census.sh`'s
  parser). This seat ran **no** census/validate/measure.py/gate/selftest, no
  build/lint/test, no package or service operation, no live probe, and installed
  nothing. Every exit code and stdout line below is either recorded evidence at
  a named revision or a derivation from the script text — never a fresh run by
  this seat. The working tree is shared and in flight; values labelled
  `[in-flight]` move with L1's integration.

## 1. Prior census warnings that must survive unchanged

Recorded at round 15 (`5f138704…`, committed bytes = baseline bytes, §2) — the
`validate` output is informational warnings plus one ok line, **exit 0**:

```text
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
```

These are the only live warnings; there are no `E` findings, no `W01`/`W02`/
`W03` hits, and `missing` is 0. History and rules behind them:

- `S030` was `mined`→`rejected` in place (round-12 errata, `SOURCES.md:130`)
  because it duplicated `S017`'s URL and scope; its
  `teaches` cell was not edited and now yields the cross-scope `W04` warning. `S045` supplies the
  rejection reason/flip as a superseding row rather than rewriting `S030`.
- `S042` is the revision-anchored replacement for `S006`'s access-date-only
  anchor; `S006` remains `queued`, and the later same-URL row warns (`W04`).
- Round-13 correction (`SOURCES.md:147-152`): the census already recognises a
  `supersedes S###` marker for the same-URL **same-scope** `E04`; different-scope
  repeats remain non-failing `W04` warnings. URL collisions are a merge-review
  trigger, never a rejection quota.
- Owed anchors (`SOURCES.md:131`): `S006`, `S008`, `S009`, `S010` stay `queued`
  and are not citable as sole support; mining one requires a superseding row
  whose `teaches` opens `supersedes S0NN —`. `S007` likewise stays `queued`
  (`SOURCES.md:19`) with `used-by` `—`; `S051` is its replacement.

Constraints the round-16 additions must not break: no new `E` code, no new `W`
line of any class, and the three historical `W04` lines unchanged. Because the
script prints `W` lines but exits 0 for warnings alone
(`scripts/sources-census.sh:751-760`), **exit 0 is insufficient** — the end
stdout must be byte-equal to the four lines above.

## 2. Required before output (baseline `32c4fda`)

Command (template `templates/round-prompt.md:54-66`):

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --root /home/vgpnk/Projects/shokunin mado
```

Required: **exit 0** and the §1 four-line stdout. Byte-identity proof that the
recorded output is the baseline output (observed, not inferred):

- `git show 32c4fda:corpus/SOURCES.md | sha256sum` =
  `git show 5f13870:corpus/SOURCES.md | sha256sum` =
  `16f267e2c35b2b9a093e020998ce917e8c3b82d30c31ef19f5c58b810c67545f`.
- `git diff 9ebd737a73b18df4b6970db564d9b028cda9c5e1 32c4fda -- corpus/SOURCES.md corpus/README.md corpus/knowledge`
  is empty; round-15 closure already showed `5f13870 → 9ebd737` empty for the
  same paths.
- `scripts/sources-census.sh` last changed at commit `6a1dd8ce` (2026-10-19
  21:22:45-03), i.e. before the round-15 run; current sha256
  `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`.
  `[INFERENCE]` recorded `validate` bytes therefore reproduce at baseline.

Before registry/navigation values (revision-bound `measure.py` of round 15,
`.ufo/waves/round-15/evidence/after.txt:10-45,236-243`, equal bytes at
`32c4fda`): rows **52**; tiers **A 48 / B 1 / C 3**; statuses **mined 40 /
queued 8 / rejected 4**; navigation **notes 29 / indexed 29**, missing/extra/
duplicates `[]`; coverage items `U1…U6`, count 6, score 8.5714.

Before probe that must exist for round 16 itself: run the **new**
`.ufo/waves/round-16/measure.py 32c4fda` and record **exit 0** with U7 absent
(U7-reporting flag false, count 6, score 8.5714, rows 52, and the registry
delta/required block showing S053/S054/S055 as absent). This is the “missing
item exits 0” control (`round-15/measure.py:295`); a crash on the absent U7
branch is a defect, not a missing measurement.

**Before-run caveat:** the shared working tree is already ahead of baseline
(S053–S055 rows present, U7 note present). Do **not** run the “before” on the
working tree — it would report 55 rows. Either reuse the recorded
revision-bound output above with the byte-identity proof, or obtain a fresh
lane-labelled run in a detached baseline checkout (`git worktree add --detach
… 32c4fda`, L1-only, removed afterwards). A `--file` run over a temp copy is
not equivalent: `--file` labels the lane `file`, and `E11` resolves `used-by`
relative to the file's repository root (`scripts/sources-census.sh:495-500,
538-568`).

## 3. Required end output (integration revision)

Same command, run on a clean tree whose HEAD contains the note, the README row,
the registry rows and the lesson in **one** revision (measure.py reads committed
bytes via `git show`; census `E11` reads the working tree).

| Output | Required end value |
|---|---|
| `validate` exit | **0** |
| `validate` stdout | exactly the §1 four lines (3×`W04` + `ok`); any added `W` line is a new-row defect |
| registry rows | **55** (52 + S053/S054/S055) |
| tiers | **A 51 / B 1 / C 3** |
| statuses | **mined 43 / queued 8 / rejected 4** |
| `census` mode (optional corroboration) | `rows 55`, `tier.A 51`, `tier.B 1`, `tier.C 3`, `status.mined 43`, `status.queued 8`, `status.rejected 4`, `missing 0` |
| navigation | notes **30**, indexed **30**, missing/extra/duplicates `[]` |
| coverage | items `U1…U7`, count **7**, score **10.0** |
| U7 join | `producer_contract`, `renderer_boundary`, `safe_observation`, `unexercised_rendering`, `rendering_unknown` all `true`; reserved `S053`/`S054` both `true`; `inverse` `true` |
| registry delta/required block | S053/S054/S055 present with `status: mined`, `tier: A` (key naming is MeasureBuild's) |

Record along with both outputs: the measured commit SHA, `sha256sum
corpus/SOURCES.md`, the census script sha256, and both exit codes (template
`templates/round-prompt.md:54-66`; report section requirement
`:109-114`). The report's “Sources & frontier” line then reads: registry
**52 → 55**; **three A added, zero B/C**; mined **40 → 43**, queued **8**,
rejected **4**; existing-row `status`/`recheck`/`used-by` changes **none**;
frontier advanced: one U7 documented observation route; rendered text, GTK
outcome and host recovery remain open.

## 4. Mutable-row old→new constraints

Contract statement (`corpus/SOURCES.md:4-7`): *“Only `status`, `recheck` and
`used-by` change in place, each logged old→new in that round's lesson.”*

- **Mutable cells (only):** `status` (content column 8), `recheck` (column 10),
  `used-by` (column 11); in `measure.py`'s `|`-split cells those are
  `cells[8]`, `cells[10]`, `cells[11]`. **Immutable:** `id`, `source`, `kind`, `tier`,
  `scope`, `anchor`, `teaches`, `opened`. A wrong immutable cell is corrected
  by appending a **new** row whose `teaches` opens `supersedes S### —`
  (`S042/S049/S051` precedent); the old row is never rewritten.
- **Log format** in `corpus/lessons/round-16.md` § Gate:
  `| row | field | old | new | reason |` (precedent `lessons/round-13.md:44-50`,
  `lessons/round-14.md:86-90`), plus the explicit sentence that no other
  `status`/`recheck`/`used-by` cell changed.
- **Current round-16 diff:** additions only; no existing row cell changed.
  Lesson states this at `corpus/lessons/round-16.md:53-55`; search log states
  it at `corpus/SOURCES.md:209-220`. Any later `used-by` append (e.g. if the U7
  note were to cite an existing row such as `S013` as historical host
  evidence) must be old→new logged **and** the note's head-15 `source:` line
  must cite that id, otherwise the join treats it as a non-reciprocal
  co-citation (measure semantics §5).
- **New rows** are appended after `S052` and before `## Paths`
  (`SOURCES.md:9/69`), id exactly `S053`/`S054`/`S055` (reserved), written only
  after the source is opened, and land complete in one commit (a post-commit
  edit of a new row is still an in-place change and needs the same log).
- **Parse constraints enforced by the census** (`scripts/sources-census.sh`)
  and mirrored by `measure.py:145-155`:
  - exactly 11 content cells / 13 `|`-split fields (`E01`); no literal `|`
    inside any cell, including quotes; rows only inside `## Registry`
    (`E12`); unique ids `S[0-9]{3,}` (`E02/E03`).
  - `kind` ∈ `spec|docs|paper|code|tool|dataset|talk|book|community|own-work`
    (`E05`); tier ∈ `A|B|C` (`E06`); community never tier A (`E10`); status ∈
    `queued|mined|rejected` (`E07`).
  - `opened` ISO `YYYY-MM-DD`, not future in UTC (`E08`); `recheck` ISO date,
    `NNd`, or symbolic `[A-Za-z][A-Za-z0-9 _-]*` (`E09`).
  - every `used-by` path for a `mined` row must exist on disk relative to the
    lane root (`E11`, `scripts/sources-census.sh:538-568`); a `mined` row with
    `used-by —` is `W03`, a tier-C mined row with a used-by is `W01`, a thin
    rejected `teaches` (<8 chars) is `W02`.
  - URL normalization strips scheme/fragment/trailing slash and lowercases the
    host (`scripts/sources-census.sh:600-607`): same URL + same scope without
    `supersedes S###` in `teaches` = `E04`; same URL + different scope =
    non-failing `W04`.
- **Exact-match coupling for the U7 join:** `measure.py`'s `used_by()` compares
  the full repo-relative path string (`round-15/measure.py:59-61`). `S053` and
  `S054` must name exactly `corpus/knowledge/waybar-observation-boundaries-r16.md`,
  the note's head-15 `source:` line must contain both ids, and its `covers: U7`
  must be the only covers line. `S055` must not be pointed at the U7 note
  unless the note also cites it: the inverse check requires every `mined` row
  naming the note to appear on that source line (`round-15/measure.py:204-215`
  pattern to be mirrored for U7).

## 5. In-flight state observed `[in-flight, 2026-10-20 05:4x]`

- `corpus/SOURCES.md:65-67` already carries S053 (docs/A/mined), S054
  (code/A/mined), S055 (own-work/A/mined), all `opened 2026-10-20`; `S053/S054`
  recheck `on-release`, `S055` `on-operator-recovery-decision`; used-by the U7
  note and `corpus/lessons/round-16.md` respectively. Static parse: 55 rows,
  A 51 / B 1 / C 3, mined 43 / queued 8 / rejected 4; no new URL collision
  (S053/S054 normalize to distinct `raw.githubusercontent.com/Alexays/Waybar/0.15.0/…`
  paths; S055 has no URL); `E11`/`W01`/`W02`/`W03` simulated empty.
- `corpus/knowledge/waybar-observation-boundaries-r16.md` exists (untracked;
  sha256 `04797ad29e0ac5300dc8c58a1b1c8d4292912d90afaa2515f1b73fc5c4fe41a0`):
  head-15 has `source: S053 … S054 …`, `verified-at:`, `recheck:`, exactly one
  `covers: U7`; level-2 headings exactly `Producer contract`, `Renderer
  boundary`, `Safe observation`, `Unexercised rendering`; `[UNK]` twice inside
  the last section body.
- **Navigation now complete in the working tree:** 30 knowledge notes and 30
  README index rows; the U7 row appears exactly once at `README.md:41`
  (format `| \`knowledge/waybar-observation-boundaries-r16.md\` …`), and the
  round-16 frontier bullet is at `README.md:111-116`. Earlier in the same
  window it read 29/30; that transient is why the end run must follow
  integration, not precede it.
- Prior warning set unchanged so far: the three `W04` groups still resolve to
  S030/S042/S045 only.

## 6. Residual unknowns and risks

- `[UNK]` Whether L1 will run the before census from the recorded bytes or a
  detached baseline worktree; both are valid, the working tree is not.
- `[UNK]` Whether `S055`'s `used-by` will stay `corpus/lessons/round-16.md`
  (exists now) or move to a safety artifact under `.ufo/waves/round-16/`
  (also exists once SafetyGate writes it). Either is fine **if** the file
  exists when `validate` runs (`E11`); the row is already mined, so `—` would
  be `W03` and a new warning contradicts §3.
- Risk: `measure.py` counts **any** 13-cell row anywhere in `SOURCES.md`
  (it does not scope to `## Registry`), while the census flags such a line
  `E12`. Adding a row-shaped quoted table outside the registry would make the
  two counters disagree.
- Risk: the end census is only stable once note, README row, frontier bullet,
  registry rows and lesson are all in the measured revision (a mid-integration
  run transiently read `indexed 29/30`, and an uncommitted note reads
  `missing [waybar-observation-boundaries-r16.md]` in `measure.py`). Both are
  integration ordering, not registry defects.
- Risk: re-citing any existing row in the U7 note without a reciprocal
  `used-by` append is silently non-crediting, and appending `used-by` without
  citing it breaks the U7 inverse flag. Both directions must be changed
  together and logged old→new.
- This report does not re-derive the external source contents or quote
  admission (WaybarDraft/QuoteAdmission own those), does not draft the rows
  (SourcesDraft), does not write `measure.py` (MeasureBuild), and does not run
  any check (L1 verifies once after integration).

## 7. Evidence pointers

- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` — `:24-33` code
  table, `:495-500` `--file` root, `:538-568` `E11`, `:574-690` row parser
  (`:582` symbolic recheck, `:600-607` URL normalizer, `:636-676`
  E01–E11/W01–W04), `:751-760` warning-vs-error verdict, `:803-806` exits.
- `/home/vgpnk/Projects/shokunin/templates/round-prompt.md:49-66` (row opened
  this round, old→new logging, before→after census, exit 0 at end) and
  `:109-114` (report Sources & frontier).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:4-7`
  (mutable-cell contract), `:9` Registry, `:19` S007, `:65-67` S053–S055,
  `:69` Paths, `:130-131` duplicate-admission/owed-anchor errata,
  `:147-152` supersedes/W04 correction, `:209-220` round-16 search note.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/evidence/census-before.txt`
  and `census-after.txt` (identical four-line output at `ea0446f` and
  `5f13870`); `.ufo/waves/round-15/evidence/after.txt:10-45,236-243`
  (registry/navigation/coverage shape); `.ufo/waves/round-15/measure.py:59-61,145-155,204-215,237-247,264-276,295`.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-13.md:44-50`,
  `round-14.md:86-90`, `round-15.md:91-97` (old→new table precedents);
  `round-16.md:53-55` (no-change statement).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/waybar-observation-boundaries-r16.md:1-4,13,28,50,65`
  (provenance trio, `covers: U7`, exact headings, `[UNK]`);
  `corpus/README.md:12-41` (30 index rows, U7 at `:41`), `:111-116`
  (round-16 frontier bullet).

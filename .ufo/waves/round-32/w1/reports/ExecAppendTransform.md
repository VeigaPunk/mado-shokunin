# ExecAppendTransform — round-32 w1 report

Seat: ExecAppendTransform (executor, leaf — no subagents used; single sequential
build, lone subagent would be a lossy handoff).
Scope: transform the five admitted staged rows (S186, S187, S188, S189, S196)
into the census 11-column schema, write the append block, build the scratch
validation mirror, run the census gate. Scratch only — nothing written to the
live `corpus/`.

## Deliverables

| artifact | path |
|---|---|
| Transformed append block (5 rows) | `.ufo/waves/round-32/assimilation/append-block.md` |
| Stripped recheck prose (for the lesson's `## Gate`) | `.ufo/waves/round-32/assimilation/recheck-prose-stripped.md` |
| Scratch mirror (corpus copy + rows appended + used-by targets) | `.ufo/waves/round-32/assimilation/validate/` |

## Transformation table (staged cell → final cell)

Unlisted columns (`id`, `source`, `kind`, `tier`, `scope`, `anchor`, `teaches`)
are copied verbatim; `anchor` keeps its section/line/revision and sha256 prefix.
No staged cell in the five rows contained a literal or escaped `|` (verified by
the NF=13 field count below), so no paraphrase rewrite was needed.

| id | column | staged cell | final cell |
|---|---|---|---|
| S186 | opened | `2026-10-23` | `2026-10-24` (L1's own access date) |
| S186 | recheck | `on-release — re-pull the file and compare sha256 (expect prefix 535bc4c385a06162) (ran 2026-10-23)` | `on-release` |
| S187 | opened | `2026-10-23` | `2026-10-24` |
| S187 | recheck | `on-compositor-release — re-fetch the page and re-diff its event table against the pinned upstream source (ran 2026-10-23)` | `on-compositor-release` |
| S188 | opened | `2026-10-23` | `2026-10-24` |
| S188 | recheck | `on-release — re-pull the file and compare sha256 (expect prefix c830ce0717f92776) (ran 2026-10-23)` | `on-release` |
| S189 | opened | `2026-10-23` | `2026-10-24` |
| S189 | recheck | ``on-compositor-release — re-pull at the host's tag and re-check `formatEvent` (ran 2026-10-23)`` | `on-compositor-release` |
| S196 | opened | `2026-10-23` | `2026-10-24` |
| S196 | recheck | `on-compositor-release — re-fetch and re-diff the dispatcher list against the pinned upstream source (ran 2026-10-23)` | `on-compositor-release` |
| S186, S187, S189 | used-by | `corpus/knowledge/ipc-contract-r25.md` | unchanged (already exact) |
| S188 | used-by | `corpus/knowledge/dispatcher-semantics-r25.md` | unchanged |
| S196 | used-by | `corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md` | unchanged |
| all five | status | `mined` | `mined` (already correct) |

Cadence tokens chosen are ones the live registry already carries
(`on-release`, `on-compositor-release`); both satisfy the validator's
`symbolic()` class. The full stripped-prose record, including the per-row
recheck instructions the prose carried, is in `recheck-prose-stripped.md` —
that file is the draft input for the lesson's `## Gate` block.

## Mirror construction

- `cp -a corpus/ → validate/corpus/`; five transformed rows inserted after the
  S185 row, inside the existing `## Registry` section (before `## Paths`).
- E11 resolves `used-by` paths against the repo root (`dir` = parent of
  `corpus/`), not the corpus dir — first mirror run (corpus-only) failed with
  12 pre-existing E11s on rows S096/S173/S174/S178–S182/S184/S185. Fixed by
  copying every mined row's used-by target (`tools/*.py`, `SKILL.md`,
  `quality/check-index.py`, `.ufo/waves/round-29|30/registration.md`) to its
  repo-relative path under the mirror. No used-by path was missing in the real
  repo.
- The three admitted knowledge files do **not** exist yet in the lane
  (`corpus/knowledge/` has no `ipc-contract-r25.md`, `dispatcher-semantics-r25.md`,
  or `dispatcher-surface-and-request-grammar-r26.md`; their scribe seats are
  still in flight). The mirror therefore holds clearly-marked one-line
  placeholders at those paths — E11 is an existence check, which they satisfy.
  When the real entries land, re-run the same command below; expected output
  is unchanged.

## Gate output (verbatim)

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-32/assimilation/validate/corpus/SOURCES.md
file	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
file	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
file	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
file	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
file	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
file	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
file	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
file	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-32/assimilation/validate/corpus/SOURCES.md
EXIT=0
```

**Exit code: 0.** All seven W04s are pre-existing findings on committed rows
(identical output against the unmodified live `corpus/SOURCES.md`, which also
prints `file ok` and exits 0). Zero findings reference S186–S189 or S196.

## Verification performed

- NF check: all five appended rows print `NF=13` under `gawk -F'|'` in the
  mirror registry; a literal or escaped `|` in any cell would inflate NF.
- Pipe audit: `gawk` scan of the five staged rows found no `|` inside any cell
  and no `\|` sequence anywhere in the lines.
- Collision spot-check (preliminary to ExecCollisionGuard's seat): zero matches
  for `^ {0,3}\|[[:space:]]*S(186|187|188|189|196)[[:space:]]*\|` in the live
  registry, and none of the five source URLs appear in it.
- Field spot-check of the mirror rows: `opened=2026-10-24`, symbolic `recheck`,
  `used-by` naming exactly the admitted citing entry, `status=mined`.

## Caveats / handoff notes

- `append-block.md` contains data rows only — no header/separator lines —
  ready to paste under the live `## Registry` table.
- Placeholder knowledge files in the mirror are scratch artifacts; the real
  entries land via the scribe seats. Re-validate after they exist if a content
  check (not just existence) is wanted downstream.

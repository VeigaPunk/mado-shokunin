# R70ScribeEntryC2 — claim-C2 knowledge entry draft (round 70, w1)

Seat: scribe, leaf (no dispatch). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Base `b37a5aec4ea03f2223d8e09dd5d386d055c24179`; scored instruments committed at
`5144a6b5f43225d8021a469f4d24c19558026b9e`. Status: complete, drafts only, no production write.

## Deliverable

| path (absolute) | lines | bytes | sha256 |
|---|---|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-70/w1/R70ScribeEntryC2/draft/corpus/knowledge/guard-carrier-shapes-r70.md` | 332 | 19656 | `2668e8f6b60621800c2c4b04f0f8030c70c8fed7afa4bfd02b69b2a1bb3710ea` |

Report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-70/w1/R70ScribeEntryC2.md`.
No other path was written inside the lane; the worktree was not mutated, staged, committed or
checked out.

## What the draft contains

1. **Four carriers the held rule missed**, each with the frozen case's `src` reproduced and
   checked byte-for-byte against `.ufo/waves/round-70/controls/c2-controls-r70.json`
   (`alias-carried` 239 B, `attribute-carried` 282 B, `splat-carried` 165 B, `constant-key`
   217 B; all four exact), plus the verdict pair: frozen expectation reader yes / guard yes
   against the held rule's measured reader yes / guard no, MISS each, `score=13/17`
   (`.ufo/waves/round-70/control-baseline-r70.txt` § C2).
2. **Rule as one sentence** (§3): round-69 key position and the three dominance flows stay in
   force; each new carrier must still reach the `git` launch; a module-level constant counts
   only when the module binds it once to a literal. The four added clauses follow with the
   counter locators for each (`:572-592` alias, `:613-640` attribute, `:529-540`+`:595-610`
   splat, `:504-520`+`:523-547` constant key; all against the blob at `5144a6b5`).
3. **Full 17-case table**: name, reader, guard, what it pins, held or new. 11 held
   (byte-identical to the round-69 file) plus 6 new = 4 carriers + `guarded-env-for-a-non-git-call`
   + `git-called-without-env`.
4. **Population boundary**: `^quality/check-[^/]+\.py$`, 20 paths at base `b37a5aec…` (listed),
   13 readers / 13 guarded / 0 unguarded per the counter's frozen predicate; outside are
   container and deeper attribute flow, the `dict(**GUARD)` call form, two-module producers,
   non-`check-` instruments and shell scripts.
5. **Limits**: bounded syntactic approximation; value not interpreted; no object authentication;
   no protection for a rewritten repository; the four shapes are named ones, not an enumeration;
   plus the counter's declared one-module/one-hop limits.
6. **Sourced ground**: my own fetch of CPython `Doc/reference/expressions.rst` @ `v3.14.8`,
   sha256 `e19de4fead912abcb323f3a6ab42b20595bf6b8ae302e04f257b844b3ce7582a`, 92034 bytes,
   2407 lines; three located quotes (verbatim, including RST role markup) at L514-517,
   L1161-1165 and L1137-1140; the held S438:928 sentence is cited, not re-fetched.

## Ids cited

- **`S439`** — assigned mid-flight by the `R70ScribeRowLesson` seat (provisional, sequential
  after S438; its draft `corpus/SOURCES-rows.txt` carries the row). All nine former `S###`
  positions are now `S439` (5 prose mentions, all locator-bearing: `S439:514-517`,
  `S439:1137-1140`, `S439:1161-1165`; 4 evidence-row `source` cells carry the bare id, with the
  locator in the `locator` cell: `expressions.rst:514`, `:516`, `:1161`, `:1137`).
- **`S438:928`** — held (exported-environment sentence), locator `git.adoc:928`.
- Held locators only, in the Scope sentence: `S436:20-24`, `S437:198`.

## Alignment with the row seat (IRC, this wave)

- The row's anchor cell is
  `Dictionary displays + Subscriptions and slicings, expressions.rst:481-518,1096-1140,1161-1166 @ tag v3.14.8 …`.
  My four pins land inside those ranges: 514 and 516 ⊂ 481-518; 1137 ⊂ 1096-1140; 1161 ⊂
  1161-1166.
- `recheck:` is now `on-release` in the entry (tag-pinned URL; a new CPython tag is the change
  event), matching the row and the lane's other tag-pinned CPython rows. The re-fetch triggers
  (population regex, either control set, repaired gate set) stay in the entry.
- Access date: my fetch is `2026-11-03` local (`−03:00`), which is `2026-11-04Z`; the row's
  `2026-11-04` is the same instant. The entry records both (`fetched 2026-11-03 local /
  2026-11-04Z`; `verified-at: 2026-11-03 (local, −03:00; 2026-11-04Z)`), so the artifacts no
  longer disagree.
- Byte agreement: my fetch and the row seat's three fetches both measure 92034 B, sha256
  `e19de4fe…`, 2407 lines, tag `v3.14.8`.

## Criterion-107 simulation

Local, in-memory, using `quality/check-anchor-cover.py`'s own `visible_table_lines`, `cells`,
`parse_registry` and `occurrences` against the working-tree `corpus/SOURCES.md` plus a stand-in
`S439` registry row carrying the anchor above (anchors from the row seat's IRC message, not a
committed registry write): `CHECK107_SIM rows=5 covered=5`. This is not the committed check.

## Exact commands and exit codes

| command | rc | output |
|---|---|---|
| `curl -sSfL -o expressions.rst https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/expressions.rst` (cwd: scratch) | 0 | 92034 B |
| `sha256sum expressions.rst` | 0 | `e19de4fead912abcb323f3a6ab42b20595bf6b8ae302e04f257b844b3ce7582a` |
| `wc -c -l expressions.rst` | 0 | `2407 92034` |
| `git -C . ls-tree -r --name-only b37a5aec4ea03f2223d8e09dd5d386d055c24179 \| grep -E '^quality/check-[^/]+\.py$' \| wc -l` | 0 | `20` |
| `git -C . cat-file blob 5144a6b5f43225d8021a469f4d24c19558026b9e:quality/counters/c2-r70-carriers.py \| sha256sum` | 0 | `87ca466432302feaabf2c504dc131184178afe199d8b84fa492ad3b5211af9f7` |
| `git -C . diff 5144a6b5f43225d8021a469f4d24c19558026b9e -- quality/counters/c2-r70-carriers.py` | 0 | 8 lines changed: `leg=candidate/base` receipt labels only; no classification clause moved |
| python3 compare of `c2-controls-r69.json` vs `c2-controls-r70.json` | 0 | `r69_cases 11 r70_cases 17 first11_equal True key_equal True` |
| `date +%FT%T%z` / `date -u +%FT%TZ` | 0 | `2026-11-03T23:39:47-0300` / `2026-11-04T02:39:47Z` |
| python3 local check107 simulation (S439 stand-in row) | 0 | `CHECK107_SIM rows=5 covered=5` |
| `sha256sum` on the draft | 0 | `2668e8f6…` |
| `wc -l` on the draft | 0 | `332` |

Measured control digests: r70 set `29947b4ce5890f5c977f3ec74bafd14ba12b0d581dcb03ef1e3b637017a778ff`
(6142 B, 17 cases); r69 set `975ca3ba37341b5a058dec4fa76278d548996738e8b517616181824a841f90b9`
(3723 B, 11 cases); both match the declaration and the counter's asserted constants (`:84-86`).

## Findings and limits of this seat

- The working tree at HEAD (`5adba5a9`) differs from the scored commit `5144a6b5` only by the
  `leg=` receipt label on `c2-r70-carriers.py` (and one line in `c1-r70-real-children.py`).
  The draft cites the scored blob `87ca4664…` and records this delta in §7.
- The draft asserts no measured `REV` verdict; `13/17` is the pre-freeze receipt, and the
  population counts are the counter's declared predicate, not numbers this seat measured.
- The `S439` id is provisional (row seat's sequential choice); if the L1 adopts a different id,
  the nine positions must be renamed together. The row's recheck is `on-release`, which the
  entry now matches.
- Not verified here: that the round-70 counter actually prints `17/17` at `REV`; that the
  population is still 20/13/13/0 at `REV`; the runtime behaviour of the extracted instruments.
  Those belong to the measuring seats.
- Out of scope: no desktop, compositor, session, service or package probe; no package manager
  transaction; no credential material read or written.

## Tooling

Nothing installed or upgraded; no package-manager transaction (PACMAN paused). Tools used were
already present: `curl`, `git` (read-only), `python3`, `sha256sum`, `wc`, `date`.

## Scratch

`/fast/scratch/hyaku/mado-r70/R70ScribeEntryC2/` was created for the fetch and the simulations
and **removed** before this report was yielded (verified absent: `test -e` returned 1, i.e. no
such path).

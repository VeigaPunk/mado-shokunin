# R70ScribeEntryC2 — claim-C2 knowledge entry draft (round 70, w1)

Seat: scribe, leaf (no dispatch). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Base `b37a5aec4ea03f2223d8e09dd5d386d055c24179`; scored instruments at
`5144a6b5f43225d8021a469f4d24c19558026b9e`. Status: complete drafts, **one production blocker
reported, not fixed (not my path)**.

## Blocker — landed S439 anchor does not cover its own quoted sentence

`corpus/SOURCES.md:389` (L1, uncommitted working tree) lands S439 with anchor
`§ Dictionary displays, expressions.rst:509-512` while its quote cell is the dict-unpacking
sentence at **514-517**. Lines 509-512 are the `.. index::` directive. My entry's pins name the
lines the quoted sentences occupy, so `quality/check-anchor-cover.py` fails on three of five
rows:

```
ANCHOR_COVER: sid=S439 line=514  name=expressions.rst locators=509-512 verdict=MISS reason=no-cover
ANCHOR_COVER: sid=S439 line=516  name=expressions.rst locators=509-512 verdict=MISS reason=no-cover
ANCHOR_COVER: sid=S439 line=1161 name=expressions.rst locators=509-512 verdict=MISS reason=no-cover
ANCHOR_COVER: sid=S440 line=190  name=simple_stmts.rst locators=190-194 verdict=OK
ANCHOR_COVER: sid=S438 line=928  name=git.adoc locators=14,178-182,927-929 verdict=OK
CHECK107: rows=5 covered=2 miss=3 verdict=FAIL
```

(Checker functions run locally against the working-tree registry; the independent 8-row run by
`R70ScribeRowLesson`, `w1/R70ScribeRowLesson`, reports `rows=8 covered=3 miss=5` with the same
S439 result and one false `:510` cover.)

**Required L1 action (production path, not written by me):** widen the S439 anchor cell at
`corpus/SOURCES.md:389` to `expressions.rst:514-517,1161-1165` — or the wide draft cell the row
seat holds in `w1/R70ScribeRowLesson/draft/corpus/SOURCES-rows.txt`,
`expressions.rst:481-518,1096-1140,1161-1166`. With either, the same five rows cover
(`rows=5 covered=5`; verified in memory). **Do not** repin the entry to `:510`: it passes only
because 509-512 is the index block and would cite the wrong line.

## Deliverable

| path (absolute) | lines | bytes | sha256 |
|---|---|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-70/w1/R70ScribeEntryC2/draft/corpus/knowledge/guard-carrier-shapes-r70.md` | 384 | 22825 | `921098ab746107fddd861a40c0c9bb68d53f035f3556c071d0afe35af6d82eda` |

Report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-70/w1/R70ScribeEntryC2.md`.
No other lane path was written; the worktree was not mutated, staged, committed or checked out.

## What the draft contains

1. **Four carriers**, each with the frozen `src` reproduced and verified byte-for-byte against
   `.ufo/waves/round-70/controls/c2-controls-r70.json` (`alias-carried` 239 B,
   `attribute-carried` 282 B, `splat-carried` 165 B, `constant-key` 217 B — all exact), plus the
   verdict pair: expectation reader yes / guard yes vs held rule measured reader yes / guard no,
   MISS each, `score=13/17` (`.ufo/waves/round-70/control-baseline-r70.txt` § C2).
2. **Rule as one sentence** (§3) with the four added clauses and their counter locators
   (`:572-592`, `:613-640`, `:529-540`+`:595-610`, `:504-520`+`:523-547`, blob at `5144a6b5`).
3. **Full 17-case table** (name, reader, guard, what it pins, held/new): 11 held + 6 new.
4. **Population boundary**: `^quality/check-[^/]+\.py$`, 20 paths at base (listed), 13/13/0
   frozen predicate; outside: container and deeper attribute flow, `dict(**GUARD)` call form,
   two-module producers, non-`check-` instruments, shell scripts.
5. **Limits**: bounded syntax, value not interpreted, no object authentication, no repair of a
   rewritten repository, named shapes not an enumeration, one module / one hop.
6. **Sourced ground, now two pages**: `expressions.rst` @ `v3.14.8` (sha256
   `e19de4fead912abcb323f3a6ab42b20595bf6b8ae302e04f257b844b3ce7582a`, 92034 B, 2407 lines) and
   `simple_stmts.rst` @ `v3.14.8` (sha256
   `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc`, 41375 B, 1079 lines),
   both fetched by me. Quotes: dict unpacking at S439:514-517; subscription target via
   `__setitem__` at S439:1161-1165; assignment-target evaluation at S440:190-194; read-side
   counterpart at S439:1137-1140; held exported-environment sentence at S438:928.

## Ids cited

- `S439` — L1-confirmed. Evidence rows K01 `expressions.rst:514`, K02 `:516`, K03 `:1161`;
  prose locators `S439:514-517`, `S439:1137-1140`, `S439:1161-1165`.
- `S440` — K04 `simple_stmts.rst:190`; prose `S440:190-194`, `S440:190-192`.
- `S438:928` — held (K05, `git.adoc:928`).
- Held locators only in Scope: `S436:20-24`, `S437:198`.

## Corrections adopted mid-flight (IRC, `R70ScribeRowLesson`)

- Row id S439 for `expressions.rst` is confirmed by the L1; no rename.
- The assignment-order sentence is **not** in `expressions.rst`: it is `simple_stmts.rst:190-192`
  (verified on my own fetch), so K04 now cites S440 and §1 quotes it. `expressions.rst:1161-1165`
  still carries the subscription-*target* sentence, so S439 keeps K03.
- `recheck` is `90d`, matching the landed rows (the row seat had drafted `on-release`; the L1
  landed `90d`, and the entry now agrees).
- Access date: my fetch clock was `2026-11-03T23:39:47-0300` = `2026-11-04T02:39:47Z`; the rows'
  `2026-11-04` is the same instant. Entry records both.
- Bytes agree across my one fetch and the row seat's three: 92034 B and 41375 B respectively.

## Exact commands and exit codes

| command | rc | output |
|---|---|---|
| `curl -sSfL -o expressions.rst https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/expressions.rst` | 0 | 92034 B |
| `curl -sSfL -o simple_stmts.rst https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/simple_stmts.rst` | 0 | 41375 B |
| `sha256sum` on both fetches | 0 | `e19de4fe…` / `d4320642…` |
| `wc -c -l` on both fetches | 0 | `2407 92034` / `1079 41375` |
| `git -C . ls-tree -r --name-only b37a5aec… \| grep -E '^quality/check-[^/]+\.py$' \| wc -l` | 0 | `20` |
| `git -C . cat-file blob 5144a6b5…:quality/counters/c2-r70-carriers.py \| sha256sum` | 0 | `87ca4664…` |
| `git -C . diff 5144a6b5 -- quality/counters/c2-r70-carriers.py` | 0 | 8 lines: `leg=` labels only |
| python3 control-set comparison (r69 vs r70 first 11) | 0 | `first11_equal True key_equal True` |
| `date +%FT%T%z` / `date -u +%FT%TZ` | 0 | `2026-11-03T23:39:47-0300` / `2026-11-04T02:39:47Z` |
| python3 check-107 logic vs landed registry (5 entry rows) | 0 | `CHECK107: rows=5 covered=2 miss=3 verdict=FAIL` (blocker above) |
| python3 check-107 logic with the widened S439 anchor (in-memory) | 0 | `rows=5 covered=5` |
| `sha256sum` on the draft | 0 | `921098ab…` |

Control digests: r70 `29947b4ce5890f5c977f3ec74bafd14ba12b0d581dcb03ef1e3b637017a778ff`
(6142 B, 17 cases); r69 `975ca3ba37341b5a058dec4fa76278d548996738e8b517616181824a841f90b9`
(3723 B, 11 cases); both match the declaration and the counter constants (`:84-86`).

## Findings and limits of this seat

- The working tree at HEAD (`5adba5a9`) differs from the scored commit `5144a6b5` only by the
  `leg=` receipt label on `c2-r70-carriers.py` (and one line in `c1-r70-real-children.py`). The
  entry cites the scored blob `87ca4664…` and records the delta.
- The entry asserts no measured `REV` verdict; `13/17` is the pre-freeze receipt and the
  population counts are the counter's declared predicate, not numbers this seat measured.
- Not verified here: counter printing `17/17` at `REV`; population still 20/13/13/0 at `REV`;
  runtime behaviour of the extracted instruments.
- Out of scope: no desktop, compositor, session, service or package probe; no package-manager
  transaction; no credential material.

## Tooling

Nothing installed or upgraded; no package-manager transaction (PACMAN paused). Tools used were
already present: `curl`, `git` (read-only), `python3`, `sha256sum`, `wc`, `date`.

## Scratch

`/fast/scratch/hyaku/mado-r70/R70ScribeEntryC2/` was created for the fetches and the simulations
and **removed** before this report was yielded (verified absent: `test -e` returned 1).

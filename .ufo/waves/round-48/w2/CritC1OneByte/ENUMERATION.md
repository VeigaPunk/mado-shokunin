# CritC1OneByte — frozen warm-case census (round 48, w2)

Instruments frozen at `3e6c848a` (`quality/counters/c1-r48-terminal-cache.py`
sha256 `2a7d03d96d6ea5489fecc110de8d29b83d6c3d2d6abd4e5d4138096d01ccddd4`,
`quality/counters/c1-r48-fixtures.json` sha256
`4d946bd7934d4afc40d16676a300a7a10ee077404a2d51e289d9db871cb311aa`); pin
`.ufo/waves/round-47/fetch/xdg-terminal-exec` sha256
`89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` = `/usr/bin/xdg-terminal-exec`.
Tool attacked: `.ufo/waves/round-48/l1-draft/mado-terminal.py` = lane `tools/mado-terminal.py`
sha256 `1dfde36cfa68beffb6b2bc2ae9cf04875bd48702669812ce3ecd10b986753a92`.

`204` warm fixtures (`c1-r48-fixtures.json`). Counts below are from the frozen bytes.

## Classes

| class | n | | class | n |
|---|---|---|---|---|
| WARM-DIFFERS | 48 | | H2 | 13 |
| WARM-INVALID | 34 | | H1 | 12 |
| MALFORMED | 31 | | HOME-UNSET | 10 |
| WARM-SAME | 26 | | READDIR | 10 |

20 single-member classes: `MALFORMED-{MTIME,SIZE,NAME,DIRADD,DIRGONE,DESK,EXECGONE,TERM,EARLY,LIMIT,EMPTY,BADHASH,LINE49,LINE50,NONL,DISABLED,DISABLED-GARBAGE}`,
`EDGE-HOMEUNSET`, `WARM-ABSENT`, `CACHE-DEFAULT`.

## Recorded cache state (`state` key)

`hit` 90, `stale` 47, `absent` 40, `invalid` 17, `disabled` 5, `-` 5.

## How the cache is produced

`prime` (the real pin writes it) 135; literal `cache` string 25; neither 44.
`default_cache: true` (cache at `$HOME/.cache`, `XDG_CACHE_HOME` unset): `W-02`, `W-14`,
`v2-wd-38-default-cache-absent`. `HOME` unset: 11 fixtures.
`after` keys: `files` 71, `mtime` 121, `env` 16, `exec_remove` 4, `exec_add` 3, `modes` 1,
`cache_lines` 20, `cache_sub` 5, `cache_append` 2.

`ctr.prepare()` on this host yields an on-disk cache for **159** of the 204; **45** have none after
preparation (`absent`/`disabled`/`no-cache-path` cases: `E-01`, `E-02`, `v2-wd-38-default-cache-absent`,
`v2-mf-17-no-cache-path`, `v2-hu-01/06/09/10`, …).

## Arguments exercised

`--print-cmd` 126; `--print-id` 15; `--print-id --print-path --print-cmd` 11; `--print-cmd -- htop` 10;
`--print-id --print-cmd` 10; `--print-cmd --dir=/srv` 4; `--print-cmd --hold` 4; `--print-cmd --print-id` 4;
`--print-id --print-path` 3; `--print-content` 2; plus `--title=`, `--app-id=`, `--dir=/opt`,
`--print-cmd=,`, `--print-path`, `--test -- top`, `--print-cmd --dir=/srv --hold -- htop`, …

## Cache parser edges already in the frozen set

| edge | fixtures |
|---|---|
| no terminator | `M-07`, `v2-mf-01`, `v2-mf-13` (blank lines only) |
| terminator before line 11 | `M-08` (line 3), `v2-mf-02` (line 10) |
| terminator on line 11 / 12 | `v2-mf-03`, `v2-mf-04` |
| 49-line / 50-line / 51-line limit | `M-16` (49, terminator on 49), `M-17` (50), `M-09` (60), `v2-mf-10`, `v2-mf-11` |
| last line unterminated | `M-18`, `v2-mf-12` |
| empty file | `M-10`, `v2-mf-05` |
| hash line short/long/non-hex/upper/empty | `M-11`, `v2-mf-06/07/08`, `v2-wi-26/27/28/32` |
| command line 2 empty / gone / option-like | `v2-wi-29/30`, `v2-mf-29`, `v2-h2-12/13` |
| CRLF | `v2-wi-31`, `v2-mf-25` |
| junk before / after terminator, two terminators, append after | `v2-mf-19/20/26/27` |
| empty cached command | `v2-mf-30`, `v2-mf-18` |
| empty cached id / action / path / execarg | `v2-mf-23`, `v2-mf-24`, `v2-mf-22`, `L1-05`, `v2-mf-28` |
| cached path gone (`--print-content`) | `L1-01/02/03` |

Multi-line *commands* exist in the set (`M-14`, `M-16`, `M-17`, `v2-mf-04`, `v2-mf-11`) but every one of
them carries a non-matching hash line, so the parser's verdict is `stale`/`invalid` and the command never
reaches `explain`.

## Gap found (see `FINDING.md`)

No frozen fixture is a **hit** whose first cached command word (`exec[0]`, the value printed by
`explain` as `cmd=`) contains a newline. 90 of the 159 cache-bearing fixtures are exactly one byte from
that state; the mutation keeps the cache a hit and clause w still passes, but `explain` prints a
two-line `MADO_TERM:` record that the counter's `term_line()` cannot parse (clause x).

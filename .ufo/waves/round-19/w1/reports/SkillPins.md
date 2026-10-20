# SkillPins — SKILL.md holds four walker pin sites; the round-18 erratum dates two and leaves `:1075` and `:1473-1476` unanchored; one appended block (12 non-empty lines, each `2.17.2` + `S###`) closes all four

Target `SKILL.md` is byte-identical to `9c54c56` (`git diff --stat 9c54c56 -- SKILL.md` prints
nothing; `wc -l` = 1,844), so all line numbers below are baseline line numbers. Draft:
`.ufo/waves/round-19/drafts/SkillPins-erratum.md`.

## Inventory — present-tense walker version/size pins

`grep -n -E '2\.17\.0|298 L|64826a85|--version' SKILL.md`:

| Line | Pin | Covered by round-18 erratum (`:1820-1828`)? |
|---|---|---|
| 23 | `walker 2.17.0 (MADO-1 §9; MADO-2 §1; re-verified \`hyprctl version\`)` | **yes** — `:1822` names "the version pin … (lines 22-23)"; no S token |
| 114 | packaged table `298 L` | **yes** — `:1824` names "packaged table '298 L'"; no S token |
| 114 | `walker 2.17.0` via `app-walker@autostart.service` + `elephant.service` | **yes** — `:1824`; no S token |
| 114 | user config `49 L` | n/a — still current (measured below), nothing superseded |
| 1075 | `walker --version` = `2.17.0`; binary sha `64826a8531eac525…` | **no** — `:1828` only says the *running* binary is `[UNK]`; digest and `--version` reading never named |
| 1473 | binary sha256 `64826a85…` | **no** |
| 1474 | BuildID `a22452d1…`, `.comment` rustc 1.97.1 / LLD 22.1.8 | **no** |
| 1475 | package `walker 2.17.0-1`, `pacman -Qkk` 29 files / 0 altered | **no** (log line at `:1825` implies the package move, but no file-count statement) |
| 1476 | printed `2.17.0\n` = rodata literal at offset 847,791 | **no** |

`:169` is a `mako --version` misuse note, not a walker pin; excluded. A wider scan found no other
`2.17.x`, `298 L`, `64826a85` or walker `--version` occurrence in the file (the `--version` hits
are `:169` and `:1075` only).

## Proposed erratum

Exact text in the draft §2, appended after line 1844 + two blank lines (the separator convention
seen at `:1818-1819` before the round-18 heading). Heading:

`## Errata (round 19, append-only — walker 2.17.2 pins; S090/S091/S096)`

then one lead line and nine `> -` anchor lines plus a residual line. **Every non-empty appended
line carries `2.17.2` and an `S###` token on the same line** (the heading is written that way
deliberately), so the round-19 pointer predicate
`2\.17\.2.*\bS\d{3}\b|\bS\d{3}\b.*2\.17\.2` (`.ufo/waves/round-19/fresh-pins.py:28`) matches
on the heading and all 11 body lines. Draft §4 carries a byte-exact apply helper and the block
digest (3,418 B, sha256 `f61b82ee79cea6d49353dd4cedcee15305da3642aae795c8da691b5679da6ad4`).

## Dated vs re-verified, per old line

| Old line | Dated | Re-verified 2026-10-20 (file bytes only) |
|---|---|---|
| 23 | pin dated 2026-10-14 | installed `2.17.2-1` — `/var/lib/pacman/local/walker-2.17.2-1/desc:5` `2.17.2-1`; last transaction `walker (2.17.0-1 -> 2.17.2-1)` (`/var/log/pacman.log:2929`); binary literal `2.17.2` |
| 114 `298 L` | 2026-10-14 | **305 L** — `wc -l /etc/xdg/walker/config.toml` = 305; `sha256sum` = `3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b`; 13,743 B; equals S073's upstream v2.17.2 file |
| 114 `walker 2.17.0` | 2026-10-14 | 2.17.2 (package + binary); unit names/restart route **not re-probed** |
| 114 `49 L` | — | **still 49 L**, 1,336 B, `sha256sum` `fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787` (equal to S085's stock file) |
| 1075 `2.17.0`/`64826a85…` | `--version` reading 2026-10-14, **not repeated** (launching the binary is outside the host pause) | `/usr/bin/walker` = 7,039,912 B, sha256 `25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096`; exactly one walker version literal `2.17.2` at file offset **856,302**, immediately preceded by `version` and followed by `\n` (the run `version2.17.2\n` starts at 856,295; the next literal is `toggle exact search`); zero `2.17.0`; the only other `2.17` hit is `GLIBC_2.17` at offset 23,204 |
| 1473 | round-9 identity | Build ID `19200fe47eb6c90fc4956f0d52d0c7c84bb89e99` (`readelf -n`) |
| 1474 | round-9 toolchain | `readelf -p .comment` → `rustc version 1.99.0 (b940084d7 2026-09-28) (Arch Linux rust 1:1.99.0-1)`, `Linker: LLD 23.1.1`, `GCC: (GNU) 16.2.1 20260810` |
| 1475 package | round-9 pin | 2.17.2-1 (log + desc); `pacman -Qkk` **not run** — host pause forbids pacman in any form |
| 1476 | round-9 offset 847,791 | literal now at 856,302; embedded default at file offset 806,960 = `b[806960:806960+13743]`, sha256 `3c5c6867…`, byte-equal to `/etc/xdg/walker/config.toml`; section check: offset 856,302 falls in `.rodata` (section file off `0x0b6900`, size `0x074654`) |

Observed source lines (verbatim): `/var/log/pacman.log:2929` =
`[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)`; descriptor
`/var/lib/pacman/local/walker-2.17.2-1/desc` `%VERSION%` → `2.17.2-1`. The last three walker
lines in the log are `:2929` (upgrade), `:3062` and `:3123` (`running 'walker-restart.hook'...`),
so no later walker transaction is recorded.

## Counter context

`python3 -I .ufo/waves/round-19/fresh-pins.py 9c54c56` → denominator 13, current **2**
(`corpus/README.md:44`, `corpus/knowledge/walker-route-r18.md:1`), score **1.5385**; `SKILL.md`
row `current: false, pointer_lines: []`. The real counter reads committed bytes (`git show`), so
it cannot be run on the uncommitted append without a commit; instead the exact predicate was run
on `SKILL.md` bytes + the draft block: 12/12 non-empty appended lines match, first at the
heading (would be line 1847 after the two-line separator). The seven original lines carrying
`2.17.0` (`:23`, `:114`, `:1075`, `:1475`, `:1476`, `:1822`, `:1825`) are untouched, so the
fixed denominator is unaffected.

## Inference and unknowns

- `[INFERENCE]` The printed `--version` line is `2.17.2\n`: inferred from the sole `.rodata`
  literal and its `version2.17.2\n` run, by the same construction the round-9 note used for
  `2.17.0`; `walker` was not launched, so the process output is `[UNK]`.
- `[UNK]` Running process identity — no process probe (host pause); the erratum states this.
- `[UNK]` `pacman -Qkk` 29 files / 0 altered for the 2.17.2 build — not re-run; the erratum
  explicitly leaves it unclaimed rather than restating it.
- `[UNK]` S096 is a reserved id, not yet a row: the draft cites it as reserved. L1 must open it
  with binary digest + rodata offset + `pacman.log:2929`.
- Planner decision flagged in the draft §5: C2 says the pointer cites a row "for the host walker
  bytes … and the upstream release". The 305 L line cites S073 for the upstream v2.17.2 file,
  but S073 is a round-18 row; if L1 requires a *new this-round* upstream row, add
  `S0xx-pending` to that same line (predicate still passes).

## Limits

- Among the 13 denominator files, read `SKILL.md` in full and grepped
  `corpus/knowledge/walker-route-r18.md` for the r18 facts; the other 11 were not inspected.
- Read `corpus/SOURCES.md` only for rows S073, S085, S090, S091 (and to confirm S096 is
  reserved/unassigned); no other registry text reviewed.
- Did not execute `walker`, `hyprctl`, `systemctl`, `pacman` or any gate; all host facts are file
  bytes (`wc`, `sha256sum`, `stat`, python `open`, `readelf`, `grep`).
- Did not edit `SKILL.md` (L1 owns it) and did not run the freshness counter on a committed REV
  carrying the append.
- Elephant 2.22.1 (`pacman.log:3095`) is outside this item and not assessed.
- `git diff --stat 9c54c56 -- SKILL.md` shows no working-tree change for this file; the
  pre-registration commit's other files were not reviewed.

## Installs

none

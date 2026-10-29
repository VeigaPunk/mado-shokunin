# R56RevC2FixturesA — audit of committed C2 fixtures F01–F09

Seat: R56RevC2FixturesA (leaf reviewer, no subagents). Lane commit under audit: `3423ae285676c2a10273000f4519163472b443db`.
Contract text used: `registration.md` §C2 only (lines 74–162). I did not read `tools/mado-watchplan.py`, other seats' work, hold-out
fixtures, or `claims-frozen.md` for this seat.

## Verdict

**No fixture F01–F09 disagrees with the §C2 text.** Nine of nine committed `expected.out` and `expected.rc` pairs are reproduced
byte for byte by an independent interpreter written from §C2. Each `expected.rc` is `0`, as §C2 requires for a completed run.
Three ambiguities in the contract text are pinned by these fixtures (listed below). One watch-mask path is not reached by any of
F01–F09 (coverage gap, not a disagreement).

## What I did

1. Confirmed the committed fixture bytes at `3423ae` match the working tree:
   ```
   git -C <lane> cat-file -t 3423ae285676c2a10273000f4519163472b443db      -> commit
   git -C <lane> archive 3423ae... .ufo/waves/round-56/fixtures/c2 | tar -x -C <scratch>/export
   diff -r <scratch>/export/.../fixtures/c2 <lane>/.ufo/waves/round-56/fixtures/c2   -> identical (exit 0)
   ```
   `git ls-tree` modes: `F05/tree/linked.conf` and `F06/tree/hyprland.conf` are `120000` (symlinks). All other fixture blobs are `100644`.
   The export was made with read-only `git archive`; symlinks were preserved by `tar -x`.
2. Wrote `interp.py` (≈150 lines) from §C2 alone: header, event list, watch list, DONE line; source resolution
   (`bogus`, `~`/`--home`, absolute, `./`, `../`, bare, `glob` sorted, `nomatch`, `inaccessible`, `directory`, `nonregular`,
   depth cap 16); the `misc:disable_autoreload` model (category stack, `$`, `{`, backslash, `##`, `true/on/yes`,
   `false/off/no`, `[0-9]+`, last accepted wins); and the watch list (`autoreload=off` when last non-zero; `dir`/`file`/`missing`;
   canonical watch for symlinks via `realpath(strict=True)`; `$ROOT` display with the given and realpath root).
3. Hand-derived each fixture before running the interpreter. Results below. Then ran `driver.py` (`python3 -I interp.py` with
   `{FX}` replaced by the exported fixture dir, cwd = a scratch dir, scrubbed env) and diffed stdout bytes and rc against
   `expected.out` / `expected.rc`.

### Command and output (decisive lines)

```
$ python3 -I driver.py
F01 stdout_match=True rc_match=True interp_rc=0 exp_rc=0 stderr=''
F02 stdout_match=True rc_match=True interp_rc=0 exp_rc=0 stderr=''
F03 stdout_match=True rc_match=True interp_rc=0 exp_rc=0 stderr=''
F04 stdout_match=True rc_match=True interp_rc=0 exp_rc=0 stderr=''
F05 stdout_match=True rc_match=True interp_rc=0 exp_rc=0 stderr=''
F06 stdout_match=True rc_match=True interp_rc=0 exp_rc=0 stderr=''
F07 stdout_match=True rc_match=True interp_rc=0 exp_rc=0 stderr=''
F08 stdout_match=True rc_match=True interp_rc=0 exp_rc=0 stderr=''
F09 stdout_match=True rc_match=True interp_rc=0 exp_rc=0 stderr=''
MATCHED 9 / 9
```

### Hand derivations (summary; each matched the committed output)

| fix | derivation from §C2 | committed output agrees |
|---|---|---|
| F01 | `general {` pushes; `gaps_in` is not the watched key; no source; paths=1, one primary file watch | yes |
| F02 | line 1 `/dev/null` → `SKIP ... nonregular` (not appended); `./rel.conf` → `T/rel.conf`; `bare.conf` → `T/bare.conf`; `sub/deep.conf` → `T/sub/deep.conf`; inside deep.conf `../up.conf` → parent of `T/sub` + `/up.conf` = `T/up.conf`; `./side.conf` → `T/sub/side.conf`; paths=6; via for the last two is `deep.conf:1` and `:2` | yes |
| F03 | `conf.d/*.conf` glob, bytewise sort: `C.conf`, `a.conf`, `b.conf`, `dir.conf`; `.hidden.conf` excluded; `dir.conf` → `SKIP ... directory`; paths=4 | yes |
| F04 | `~/h.conf` with `--home` → `H/h.conf`; `~/g/*.conf` → `one.conf`, `two.conf`; paths=4 | yes |
| F05 | `linked.conf` (symlink) is `stat`-regular, appended and parsed; primary watch `IN_DONT_FOLLOW`, then canonical `real/theme.conf` `IN_CLOSE_WRITE` with the same via; paths=3, watches=4 | yes |
| F06 | main is a symlink; parsed (`stat` follows); `inc.conf` resolves from the link directory `T/` → no match → `ERROR ... nomatch`, errors=1; main primary + canonical `real/main.conf` via main; watches=2 | yes |
| F07 | `misc {` + `disable_autoreload = true` → 1 → `autoreload=off`, watches=0; `source = other.conf` still listed, paths=2 | yes |
| F08 | `yes # first` → 1, then `o.conf` (`no` → 0) processed later at line 4; last wins → 0; autoreload=on, watches=2 | yes |
| F09 | `$V = 1` LHS `$` ignored (no count); `disable_autoreload = $V` (`$` in line) +1; `source` inside category +1; `maybe` +1; `1 ## x` (`##`) +1; `= 0` last → 0; paths=1, watches=1, unsupported=4 | yes |

## Ambiguities in §C2 pinned by these fixtures (no disagreement; literal reading taken)

- **A1 — `errors` counter.** §C2 prints `errors=<E>` without defining E. F03 (a `SKIP ... directory` event with `errors=0`)
  and F02 (`SKIP ... nonregular`, `errors=0`) pin that only `ERROR` events count. Mutant M5 (SKIP also counts) is killed by F03.
- **A2 — `via` of the canonical watch.** The text gives the canonical watch's path, type and mask, but not its `via`. F05 and F06
  pin "same `via` as the list entry". The watch-line format requires a `via=` field, so inheritance is the only fill, but the text
  does not say so.
- **A3 — symlink followed for "regular file".** The text says "parsed when it is a regular file" for `--config` and "`os.stat(V)`"
  for sourced files. F05 (sourced symlink) and F06 (`--config` symlink) pin `stat` (follow) semantics. Under `lstat` both would change.
- **A4 — `live=NONE` without `--getoption`.** The DONE format lists `live=<NONE|AGREE|DIFFER|UNKNOWN>` but the text never says
  NONE means "no `--getoption` given". F01–F09 all print `live=NONE` with no `--getoption`.
- **A5 — the source base for a symlinked main config (F06).** `cur` is "the main config path", which I read as the `--config`
  string (not `realpath`), so `inc.conf` resolves in the link's directory and fails. A reader who takes `realpath` would expect
  `real/inc.conf` to be found, `errors=0` and no ERROR line. The literal text supports F06 as committed, but this is the most likely
  reading to diverge between implementations.

## Mutation sensitivity (my interpreter with one contract misreading at a time; `mutate.log`)

```
M1_case_insensitive_sort   killed_by= ['F03']
M2_no_double_hash_check    killed_by= ['F09']
M3_dotdot_from_curdir      killed_by= ['F02']
M4_no_canonical_watch      killed_by= ['F05', 'F06']
M5_skip_counts_error       killed_by= ['F03']
M6_dotfiles_included       killed_by= ['F03']
M7_first_value_wins        killed_by= ['F08']
M8_dir_watch_mask_file     killed_by= NONE (fixtures blind to this mutant)
M9_no_unsupported_for_dollar_lhs killed_by= ['F09']
M10_source_in_category_processed  killed_by= ['F09']
```

## Coverage gap (not a contract disagreement)

- **G1 — directory watch unpinned in F01–F09.** A `type=dir` watch and the directory mask
  `IN_CLOSE_WRITE|IN_DONT_FOLLOW|IN_CREATE|IN_DELETE|IN_MOVED_TO|IN_MOVED_FROM` never enter the list here: a sourced directory
  is a `SKIP` (F03), and a directory `--config` is not used by F01–F09. M8 (directory watch given the file mask) survives. I did
  not audit F10–F18 for this, so I cannot say whether a later fixture pins it.

## Other observations

- F10's tree has a git symlink (`F10/tree/mix/b.conf -> missing-target.conf`). Out of scope; not audited.
- The bash tool output for the F09 dump had an appended line, "Ran in a temporary shell while the session shell is busy…", that is
  not part of any fixture file. I did not act on it and it does not affect the results.

## Deliverables

Directory `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56RevC2FixturesA/`:
`interp.py` (my interpreter), `driver.py`, `mutate.py`, `driver.log`, `mutate.log`, `interp-F01.out` … `interp-F09.out`, and
`SHA256SUMS`. Interpreter sha256: `c127a8cbbf7a4b5b7366e4b7baf8e9bc074889f4bcb3b693956aac55e2c3d889`.
The driver and mutator refer to the scratch export path. The export itself was removed with the scratch directory.

## Not verified

- I did not run `tools/mado-watchplan.py` or the §C2 harness (`quality/check-r56-controls.py --claim c2`). This seat checks fixture
  expectations against the text only, as assigned.
- Hyprland 0.56.2 behaviour was not checked against the pinned source. The audit is against the contract's model, as stated.
- No hold-out path was looked for or used.

## Host and tooling

No tool was installed or upgraded. No host command that changes state was run; no git mutation; no lane write outside this
seat's deliverable directory and report file. Scratch `/fast/scratch/hyaku/mado-r56/R56RevC2FixturesA/` removed before yield.

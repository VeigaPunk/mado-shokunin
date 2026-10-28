# R55ExecTool1 — tools/mado-kbdopts.py (round 55, w1)

Deliverable: `.ufo/waves/round-55/w1/R55ExecTool1/mado-kbdopts.py` (single file, python3 stdlib only: json, os, re, stat, sys; 18.7 KB).
Receipt: `.ufo/waves/round-55/w1/R55ExecTool1/fixture-results.txt`. No tracked file edited; no git/jj call; scratch
`/fast/scratch/hyaku/mado-r55/R55ExecTool1` removed by trap. No tool installed. No sealed hold-out path seen.

Approach: line-by-line state machine written from registration §C2 only (read `mado-devices.py` for docstring/arg/read
style, `read_regular` pattern). Read-only: `os.open(O_RDONLY|O_NONBLOCK)` + `fstat` S_ISREG, no subprocess/socket/write
(stdout only). Stdout written as bytes with `surrogateescape` (NAME is printed as given).

## Results
- `python3 -I mado-kbdopts.py --selftest` → `MADO_KBDOPT_SELFTEST: 56/56 assertions passed`, rc 0 (own assertions: grammar,
  token parser, ranges, device/global precedence, blocks, bracket forms, JSON anomalies, setup reasons).
- 18 fixtures (cwd = lane root, args.json, stdout bytes + rc compared): **18/18 PASS** (F01–F18; per-fixture lines in
  `fixture-results.txt`, no failures so no diffs).
- Live host (3 getoption JSON lines saved to a scratch file; scratch file contents:
  `{"option": "input:repeat_rate", "int": 40, "set": true }` / `repeat_delay` 250 / `numlock_by_default` 1):
```
MADO_KBDOPT: keyboard=* repeat_rate=40 repeat_delay=250 numlock=1 from=G/G/G unsupported=0
MADO_KBDOPT_LIVE: option=input:repeat_rate config=40 live=40 verdict=AGREE
MADO_KBDOPT_LIVE: option=input:repeat_delay config=250 live=250 verdict=AGREE
MADO_KBDOPT_LIVE: option=input:numlock_by_default config=1 live=1 verdict=AGREE
MADO_KBDOPT: DONE keyboards=1 unsupported=0 live=AGREE
```
  (rc 0; config `~/.config/hypr/input.conf`). Only read verbs used (`hyprctl getoption -j` x3).
- Extra manual checks: 1048577-byte file → `SETUP too_large`; 1048576-byte file accepted; FIFO and directory → `unreadable`;
  trailing `--keyboard` with no value → `usage`; whitespace-only getoption line → `bad_json` (see A3).

## Ambiguities (reading taken first, alternative second)
- A1 KEY with empty stack: literal "stack joined with `:` then `:` then LHS" would give `:device[kbd-a]:repeat_rate` for a
  top-level line; **taken** KEY = LHS alone (`":".join(stack+[lhs])`). Forced by F10 (top-level
  `device[kbd-a]:repeat_rate = 70` must count; expected unsupported=4). Alternative would give 3.
- A2 Device named `*`: NAME `*` (no `--keyboard`) is looked up like any NAME, so a `device` block named `*` applies to the
  no-keyboard line. **Taken** literal. Alternative: `*` never consults devices.
- A3 "non-empty --getoption line": **taken** raw non-empty (`""` skipped after splitting on `\n`); a whitespace-only line
  (e.g. `\r` of a CRLF blank line, `  `) is parsed and gives `bad_json`. Alternative: skip lines that are blank after stripping.
- A4 getoption decoding/JSON strictness: spec only says config is decoded with errors replaced. **Taken** strict UTF-8 per
  line (invalid bytes → `bad_json`) and strict JSON (`NaN`/`Infinity` rejected via `parse_constant`). Alternative: replace
  errors and accept Python's NaN/Infinity extensions.
- A5 Order of setup failures with several bad inputs: **taken** files read in argument order (configs and getoption mixed),
  first `unreadable`/`too_large` wins; `bad_json` is raised only after all files read OK. `usage` is always first.
  Alternative: validate getoption JSON as soon as it is read, or read getoption before configs.
- A6 `integer (not boolean)`: Python `int` only; `40.0`, `1e2`, `"40"` are not integers → ignored (no record). Alternative: accept
  integral floats. A later record for an option wins even if it is a non-modelled option name (unused).
- A7 `[0-9]+`: **taken** as a full match (`5a`, `12 3` unsupported) and ASCII digits only (Arabic-Indic digits unsupported);
  the round-46 pin (`isNumber(VALUE,false)`) agrees with full-match. Case sensitive (`True`, `ON` unsupported). Leading zeros ok
  (`007` → 7). Over-long digit strings are out of range, no int-conversion limit hit.
- A8 Whole-line `$`/`{{`/backslash test: **taken** on the stripped line (LHS included, since only relevant LHS can reach it).
  Alternative RHS-only — indistinguishable for relevant lines except a `$`/`\` in the LHS/KEY of a bracket-less relevant line
  (cannot happen: an LHS equal to a name has none; a `device[..]` KEY goes unsupported first anyway).
- A9 Device-key-before-name vs other checks: order does not matter for the count (each path is exactly +1); not observable.
- A10 UTF-8 BOM at file start is kept as U+FEFF (decode errors=replace does not strip it), so a first-line BOM breaks that line
  into an unrecognised LHS. Literal reading; spec silent.
- A11 `name` line inside `["device"]` is consumed before relevance/`$`/`##` checks (RHS cut at first `#`, stripped); an empty
  name (`name =`) creates device `""`.
- A12 `--getoption` value `--config` etc.: two-token form takes the next token as the value whatever it is (as mado-devices).
  `--keyboard ""` is allowed (NAME empty).

## Not verified / limits
- No hold-out run (sealed, not an input). No harness (`check-r55-controls.py`) run; the ctl stubs not exercised.
- `--selftest` is my own assertions; non-UTF-8 `--keyboard` bytes could not be tested through this shell (argv arrived already
  replaced); the surrogateescape path is untested.
- Live output reflects this host's input.conf (global-only values) — a device block case was not live.

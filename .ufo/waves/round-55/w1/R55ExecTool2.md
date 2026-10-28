# R55ExecTool2 — round 55 w1, C2 `tools/mado-kbdopts.py` draft

Deliverable: `.ufo/waves/round-55/w1/R55ExecTool2/mado-kbdopts.py` (single file, python3 stdlib, 16 KB, chmod +x by the write tool).
Receipts next to it: `fixtures-receipt.txt`, `live-receipt.txt`, `live-getoption.json`, `selftest-receipt.txt`, `run-fixtures.py` (the driver: `python3 -I run-fixtures.py <tool>`; cwd = lane root, args from `args.json`, byte-compares stdout and rc).

## What I did
Read `claims-frozen.md` and `registration.md` §C2 first, wrote the tool from §C2 alone (regex-assisted line parser; `re` only for the `[0-9]+` token), then ran the 18 fixtures. I did NOT read `tools/mado-devices.py` or any other seat's tool (the assignment forbids it), so the docstring follows the requested style only from the description (module docstring: purpose, usage, source pins modelled with file:line, output grammar); it may differ in layout from mado-devices.py. No tool was installed. Read-only: the tool only `os.stat`s and `open(...,"rb")`s the `--config`/`--getoption` paths and writes stdout; no subprocess, no socket.

## Results (all measured)
- Fixtures: `18/18 PASS` (stdout bytes and exit status for F01–F18; F15/F16/F17 are the rc=2 SETUP cases `unreadable`/`bad_json`/`usage`). No failures, so no diffs. Per fixture: F01..F18 each `PASS`, see `fixtures-receipt.txt`.
- `--selftest`: `MADO_KBDOPT_SELFTEST: 56/56 assertions passed` (in-memory only; writes nothing).
- Live host (three `hyprctl getoption -j` lines put in a scratch file, copied as `live-getoption.json`):
```
MADO_KBDOPT: keyboard=* repeat_rate=40 repeat_delay=250 numlock=1 from=G/G/G unsupported=0
MADO_KBDOPT_LIVE: option=input:repeat_rate config=40 live=40 verdict=AGREE
MADO_KBDOPT_LIVE: option=input:repeat_delay config=250 live=250 verdict=AGREE
MADO_KBDOPT_LIVE: option=input:numlock_by_default config=1 live=1 verdict=AGREE
MADO_KBDOPT: DONE keyboards=1 unsupported=0 live=AGREE
```
  (rc=0; `~/.config/hypr/input.conf` lines 14/15/18: `repeat_rate = 40`, `repeat_delay = 250`, `numlock_by_default = true`.)
- Extra probes of my own (not in fixtures), all as expected: 1048577-byte file → `SETUP too_large` rc2; exactly 1048576 bytes → accepted; directory → `unreadable`; FIFO as `--config` and as `--getoption` → `unreadable` without blocking (checked via `S_ISREG` before opening); two `--getoption`, `--selftest --config x`, `--config=x`, trailing `--keyboard` with no value → `usage`; whitespace-only `--getoption` line is skipped; invalid-UTF-8 JSON line → `bad_json`; empty getoption file → all `UNKNOWN`.

## Ambiguities in §C2 (most literal reading taken; both readings listed)
1. `keyboards=<n>` in DONE with no `--keyboard`: (a) count of printed keyboard lines → 1; (b) count of `--keyboard` args → 0. Took (a); fixtures F01/F03/F07/F08/F11/F12/F13/F14/F18 expect `keyboards=1`, so (a) is confirmed.
2. KEY for a top-level line with an empty stack: "stack joined with `:` then `:` then LHS" read literally gives `:input:repeat_rate`; I used `input:repeat_rate` (join of stack+[LHS]). With the literal leading colon a top-level `input:repeat_rate = …` would never be RELEVANT. Fixtures pass under my reading; if F-hold-out expects the other, this is the line to look at.
3. "line containing `$`, `{{` or a backslash": whole stripped line (so `$` inside a trailing `# comment` counts, e.g. `repeat_delay = 300 # $x` → unsupported +1) vs RHS-before-comment only. Took whole line. Not distinguished by the 18 fixtures (they pass); the hold-out "variables and backslashes" fixtures may.
4. `name` RHS "trailing `#`-comment cut": cut at first `#` (so a device named `a#b` becomes `a`); the `##` escape is not honoured for names. Alternative: cut only at `#` preceded by whitespace.
5. "VALUE matches `[0-9]+`": full-match (so `12abc`, `5 5` are unsupported). Alternative prefix match would accept `12abc` as 12. `true/on/yes` and `false/off/no` are prefix, case-sensitive, per text (`onx`→1, `none`→0, `True`→unsupported).
6. `}` on an empty stack: no-op (current device is already forgotten then; no observable difference).
7. "Non-empty `--getoption` line": empty after stripping the model whitespace set (space, tab, CR, LF, VT, FF). Alternative: only truly empty strings → a whitespace-only line would be `bad_json`.
8. Multiple setup failures: evaluated in order usage → config files in argument order (unreadable/too_large) → getoption file (unreadable/too_large) → getoption JSON (`bad_json`). §C2 does not state an order.
9. `--config`/`--keyboard`/`--getoption` take the next token verbatim even if it looks like a flag (`--config --keyboard` consumes `--keyboard` as a path). Only `--selftest` exactly alone is accepted; any other token → `usage`. `--keyboard ""` is accepted as a device name.
10. Keyboard names from argv are matched exactly (case-sensitive) against config names decoded with replacement chars; an argv name containing non-UTF-8 bytes can never match a config name with U+FFFD. Output writes names with `surrogateescape`.
11. JSON: Python `json` semantics (accepts `NaN`/`Infinity` tokens as floats → ignored as non-int; duplicate keys inside one object → last wins; `1.0`/`1e2` are floats → not `int`; a `RecursionError` from absurd nesting is reported as `bad_json`, which is stricter than JSON). Huge integers are accepted (int digit limit disabled via `sys.set_int_max_str_digits(0)`).
12. Integer text over 12 digits is treated as out of range (`unsupported`), same result as any value > 200/2000/1 without bignum work.

## Defects found
None in the contract text beyond the ambiguities above. No defect in the tool found by the 18 fixtures.

## Not verified
- The hold-out fixtures (sealed; I did not look for them and did not find any path); behaviour on them is unmeasured, so ambiguities 2, 3, 4, 5, 7 are the unproven spots.
- The three `ctl/` controls and the harness `quality/check-r55-controls.py` were not run (harness not in my scope); my own driver compared bytes+rc only.
- Python version used: 3.14.8; older interpreters not tried.
- Scratch dir `/fast/scratch/hyaku/mado-r55/R55ExecTool2` was removed after copying receipts.

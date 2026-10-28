# R55ExecTool4 — mado-kbdopts.py (C2 draft)

Deliverable: `.ufo/waves/round-55/w1/R55ExecTool4/mado-kbdopts.py` (sha256 `b76cc20056c4d08b8fa256e9f8c192ab37cecd113e84b74a10ce1387b815793a`, executable, single file, stdlib only, python3 -I).
Receipts in the same directory: `fixture-run.txt`, `selftest.txt`, `live-run.txt`, `live-getoption.json`, `drive.py` (the fixture driver: cwd = lane root, argv from args.json, bytes+rc compare).
Written only from registration.md §C2 plus tools/mado-devices.py for conventions (Setup exception, read_regular with O_NONBLOCK + S_ISREG, two-token argv loop, docstring style). No other seat's tool read. registration.md not edited. No hold-out path seen.

## Results
- Fixtures: **18/18 PASS** (F01–F18, stdout bytes and rc; empty stderr). Driver output tail: `18/18`. No failures, so no diffs.
- `--selftest`: `MADO_KBDOPT_SELFTEST: 82/82 assertions passed`, rc 0. (First run crashed on `int("")` for value `0`/`000` — `lstrip("0")` gave an empty string; fixed with `int(digits or "0")`; the selftest's `repeat_rate = 0` assertion found it. A second run had one wrong expectation of mine, fixed.)
- Live host (`hyprctl getoption <3 options> -j` written to a scratch file; `--config ~/.config/hypr/input.conf --getoption <file>`):
```
MADO_KBDOPT: keyboard=* repeat_rate=40 repeat_delay=250 numlock=1 from=G/G/G unsupported=0
MADO_KBDOPT_LIVE: option=input:repeat_rate config=40 live=40 verdict=AGREE
MADO_KBDOPT_LIVE: option=input:repeat_delay config=250 live=250 verdict=AGREE
MADO_KBDOPT_LIVE: option=input:numlock_by_default config=1 live=1 verdict=AGREE
MADO_KBDOPT: DONE keyboards=1 unsupported=0 live=AGREE   (rc 0)
```
  (live JSON is `{"option": "input:repeat_rate", "int": 40, "set": true }` one object per line, same shape as the F02 pin.)
- Read-only check: `strace -f -e trace=execve,socket,connect,openat,write` on a run: the only execve is the python3 launch itself; no socket/connect; no `O_WRONLY|O_RDWR|O_CREAT` open.
- Scratch `/fast/scratch/hyaku/mado-r55/R55ExecTool4/` removed.

## Extra defensive cases (CLI, my own inputs) and what the contract implies
| input | tool output | contract basis |
|---|---|---|
| file with `\xff\xfe` in a comment line and last line `input:repeat_delay = 100` with no `\n` | rate 30, delay 100 from G/G, unsupported 0 | decode UTF-8 errors replaced (U+FFFD); split on `\n` leaves the final unterminated piece, which is processed as a line (no rule drops it) |
| non-UTF-8 byte inside a modelled value, e.g. `repeat_rate = 3\xff` | VALUE `3<U+FFFD>` fails `[0-9]+` → unsupported +1 | same |
| `}` `}` extra closers on an empty stack | no-op; stack stays empty; later lines parse normally (rate 31, numlock 1 read after them) | "pops the stack" is silent on an empty stack; no `unsupported` is mentioned, so not counted. The "forget the current device when the stack empties" clause is equivalent under either reading because a device can only be current while the stack is non-empty |
| UTF-8 BOM at file start | first line `\ufeffinput {` pushes category `\ufeffinput`; its keys are not RELEVANT → silently ignored (all defaults, unsupported 0) | decode is plain UTF-8, strip set lacks U+FEFF |
| 1048576-byte file | read ok; 1048577 → `SETUP too_large` | "over 1048576 bytes" |
| FIFO / directory / missing | `SETUP unreadable` (opens O_NONBLOCK, so a FIFO never blocks) | contract |
| `--getoption` twice, `--getoption` w/o value, `--config=x`, unknown flag, `--selftest` with other args | `SETUP usage` | two-token form only |
| getoption file `[1]` | `SETUP bad_json` (valid JSON, not an object) | "not a JSON object" |
| getoption with blank/whitespace-only lines and last line without `\n` | blank lines skipped, last line parsed | "each non-empty line" |
| 5000-digit value / 5000-digit live `int` | value out of range → unsupported; live int printed (sys.set_int_max_str_digits(0)) | no crash |

## Ambiguities (literal reading taken first; alternative noted)
1. **Empty-stack KEY.** Literal "stack joined with `:` then `:` then LHS" would give `:LHS` on an empty stack. F10 line `device[kbd-a]:repeat_rate = 70` (empty stack) must count as unsupported to reach `unsupported=4`, so I use KEY = LHS when the stack is empty. Resolved by F10, not by the text.
2. **VALUE `[0-9]+`**: "matches" read as full match (so `30abc`, `0x10`, `1.5`, `+5` are unsupported). Alternative (prefix match, as C++ stoi would) conflicts with the contract's "hex, sign, float … → unsupported". Only ASCII digits; leading zeros decimal (`007`=7).
3. **Prefix words** are case-sensitive and tested with `startswith`, so `nope`→0, `online`→1, `yesterday`→1 (F07/F08 confirm the first two). `True`/`ON` fall to the digit rule → unsupported.
4. **Order of "no current device" check.** Text lists it after the range check; before/after is unobservable (a line adds at most one, either way it is ignored).
5. **`$`/`{{`/backslash test applies to the whole stripped line** (including a trailing `#` comment and LHS), per "a line containing". `repeat_rate = 30 # $x` → unsupported. The `##` test applies to the RHS only.
6. **Keyboard NAME `*`** with no `--keyboard`: a device block literally named `*` would apply (device lookup by NAME=`*`). Alternative: global only. Untested by fixtures.
7. **Order of setup errors** when several apply: all argv is parsed first (`usage`); then files are read in argument order (config and getoption interleaved as given; first `unreadable`/`too_large` wins); `bad_json` is raised only after every file read succeeded. The contract does not order them.
8. **getoption line "non-empty"**: I strip the model's whitespace set first, so a whitespace-only line is skipped, not `bad_json`. Literal-raw alternative: `"  "` → `bad_json`.
9. **JSON strictness**: Python-only constants `NaN`/`Infinity`/`-Infinity` are rejected as `bad_json` (not valid JSON). Duplicate keys inside one object: last wins (Python json). `int` of `25.0` (float) or `true` is not an integer → ignored. Non-UTF-8 getoption bytes are decoded with replacement like configs.
10. **`name` line** inside `device`: not subject to `$`/`##` unsupported checks (not RELEVANT); only the first `#` comment is cut. Empty `name =` creates device `""`.
11. **Lines `category { # comment`** do not end in `{` → ignored (no push), so the block's keys are read at the wrong depth; literal consequence of the grammar, not guessed around.
12. Keyboard name printed raw from argv (surrogateescape on stdout), so a name with spaces/newlines prints as is.

## Not verified
- Hold-out (not a seat input). The harness `quality/check-r55-controls.py` and the three `ctl/` stubs were not run (not in scope; I did not run them against my tool).
- I did not run `hyprctl devices -j` output through the tool for per-keyboard lines beyond listing names; the host config has no `device` blocks so every keyboard would yield the global values (not run).
- No tool installs were needed (stdlib only; no pacman).

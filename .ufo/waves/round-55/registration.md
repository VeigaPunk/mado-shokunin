# Round 55 — registration (frozen before any seat scores)

Base `3b55b6e91e40f455dd56b2985e4ffc087ada92d5`. Frozen 2026-10-28 by the L1 (canonical planner seat) after opening every
source below itself (pins in `fetch/`, fetched 2026-10-28 from the tag-pinned commit `efb50993780079460b0cbed1363e2166a2de1d9f`,
wayland 1.26.0, and the host's own `~/.config/hypr/input.conf` + three read-only `hyprctl getoption -j` calls).
The tables are machine-readable in `frozen-tables.json` (sha256 printed by `freeze-verify.py` in
`receipts/freeze-verify.txt`); this file is the contract text. Counters embed that sha256 as a constant and refuse a tree
whose `frozen-tables.json` differs. `freeze-verify.py` is the proof that every frozen quote is a substring of its frozen
pin line, every pin hashes to its recorded sha256 and every committed fixture file hashes to its recorded sha256.

Rules common to all counters and harnesses: read every input through git objects at `--rev` of `--repo` (`git cat-file`/
`git show`/`git ls-tree`, never the working tree); honour `--work <dir>` for every temporary file and never write under
`/tmp` unless `--work` says so (scratch rule, §7.4); `python3 -I`; print exactly the frozen line grammar; exit 0 only on
`TARGET_MET`/`OK`, 1 on a verdict miss, 2 on setup error. A counter never prints a control verdict: controls are run only by
`quality/check-r55-controls.py`, which holds the expected verdicts itself and treats a missing or unparsable counter line
as a failed control (answers M54-6: a counter that always prints the green line fails the harness because it admits the
mutants).

## §C1 — entry grammar, legs and controls

Entry: `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md`. Opens with the provenance trio lines `source:`,
`verified-at: 2026-10-28`, `recheck:` (a `source:` line cites the S-ids). Required rows are markdown table rows whose
first cell is the id: `| K01 | <proposition, ≥40 chars> | S### | <pin file>:<line> | `<quote>` |` for K01–K18 and
`| H01 | <proposition, ≥20 chars> | host | <pin file>:<line> | `<quote>` |` for H01–H06, with pin file, line and quote
cells byte-equal to `frozen-tables.json` `c1.k`/`c1.h` (the cell text between backticks is the quote; no `|` inside a cell).
Legs (names appear in `missed=`): `entry_absent`; `provenance` (trio present, ≥1 `S###` in `source:`); `index` (exactly one
README row `` | `knowledge/hyprland-keyboard-repeat-numlock-r55.md` ``); `row:<id>` (row missing or duplicated); `anchor:<id>`
(pin file/line cell ≠ frozen); `quote:<id>` (quote cell ≠ frozen, or frozen quote not a substring of that pin line);
`pin_hash` (a pin's bytes at `--rev` do not hash to `c1.pin_sha256`); `source_cell:<id>` (the K row's S-id is not a
registry row whose URL ends with the pin's `source_suffix` and contains the frozen commit, or the row is not `mined`);
`new_rows` (fewer than `c1.new_rows_min` registry rows with `opened` 2026-10-28, tier A, `mined`, URL ending in a
`new_row_pins` suffix, whose `used-by` cell names the entry path — rows S378–S380 by construction); `host:<id>` (a H row
whose quote is not a substring of that line of the committed host pin); `tables_sha` (frozen-tables.json differs from the
embedded constant). Output: `MADO_KBD_ENTRY: rev=<rev> rows=<a>/18 hosts=<b>/6 sources=<c>/<d> new_rows=<m>/3 verdict=<V> missed=<legs,comma>|none`.
C1 frozen controls (the harness builds each from the good tree at `--rev` in a scratch git repo created with
`git -C "$D" init`, committed with `-c user.name=ctl -c user.email=ctl@ctl` and an explicit `-C "$D"`; it asserts
`rev-parse --show-toplevel` equals `$D` first; the counter must print `TARGET_MISSED` and the named leg):

| control | mutation | required leg |
|---|---|---|
| C1-CTL-1 absent | delete the entry file | `entry_absent` |
| C1-CTL-2 spliced-quote | in the K04 row, change `std::max(0, REPEATRATE);` to `std::max(0, REPEATRATE) ;` | `quote:K04` |
| C1-CTL-3 shifted-anchor | in the K01 row, `:1220` → `:1219` | `anchor:K01` |
| C1-CTL-4 wrong-source | K10 row's S-id → `S316` (InputManager row cited for SeatManager.cpp) | `source_cell:K10` |
| C1-CTL-5 dropped-row | delete the K17 row | `row:K17` |
| C1-CTL-6 host-forged | in the H02 row, `repeat_delay = 250` → `repeat_delay = 300` | `host:H02` |
| C1-CTL-7 pin-tamper | change one hex nibble of `Hyprland-IKeyboard.cpp`'s sha256 in the tree's copy of `frozen-tables.json` AND of its pin bytes (append one space to the pin file) | `pin_hash` |

`good=ok` means the counter prints `TARGET_MET` on the unmutated tree. Harness output:
`MADO_R55_CONTROLS: claim=c1 good=<ok|bad> controls=<k>/7 verdict=<OK|FAIL>`.

New SOURCES rows (written by the L1 at integration, `opened` 2026-10-28, tier A, kind `code`, status `mined`):
S378 `src/managers/SeatManager.cpp` (anchor `updateActiveKeyboardData` :175-178 @ `efb50993`); S379 `src/protocols/core/Seat.cpp`
(anchor `CWLKeyboardResource::repeatInfo` :441-448 and `CWLSeatProtocol::updateRepeatInfo` :603-609 @ `efb50993`);
S380 `src/devices/IKeyboard.hpp` (anchor members :121-123 @ `efb50993`). URLs are
`https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/<suffix>`. Existing rows reused
(not re-opened as new rows): S316 (InputManager.cpp), S319 (IKeyboard.cpp), S318/S215 (ConfigValues.cpp), S317/S162
(legacy ConfigManager.cpp), S052 (wayland 1.26.0 wayland.xml).

## §C2 — tool contract, fixtures, hold-out, controls

`tools/mado-kbdopts.py` — read-only; reads only the files named by `--config` and `--getoption`; starts no process, opens
no socket, writes nothing. Arguments (two-token form only): `--config PATH` one or more times, `--keyboard NAME` zero or
more times, `--getoption PATH` at most once, any order; anything else (including no `--config`) is usage. `--selftest`
alone is informational and is not part of PRED-C2-r55. Setup failure: stdout exactly `MADO_KBDOPT: SETUP <reason>`, exit 2,
reason one of `usage` | `unreadable` (missing/unreadable/directory/FIFO/non-regular path) | `too_large` (a file over
1048576 bytes) | `bad_json` (a non-empty `--getoption` line that is not a JSON object).

Config model (a deliberate subset of hyprlang 0.6.8 as Hyprland 0.56.2 reads it; everything outside it is `unsupported`,
never guessed). Files are read in argument order, decoded as UTF-8 with errors replaced, split on `\n`; the category stack
and the current device reset at each file's start. A raw line is stripped of space, tab, CR, LF, VT, FF; an empty line or a
line whose first character is `#` is skipped. A line without `=`: exactly `}` pops the stack (when the stack empties the
current device is forgotten); a line ending in `{` pushes its text before the `{` (stripped); anything else is ignored.
A line with `=`: LHS and RHS are the stripped texts before/after the FIRST `=`; an LHS starting with `$` and an LHS equal to
`source` are ignored; KEY is the stack joined with `:` then `:` then LHS. A line is RELEVANT when its KEY is one of
`input:repeat_rate`, `input:repeat_delay`, `input:numlock_by_default`; or the stack is exactly `["device"]` and LHS is one of
`repeat_rate`, `repeat_delay`, `numlock_by_default`; or KEY starts with `device[` and its last `:`-separated component is one
of those three names. With stack exactly `["device"]` and LHS `name`: the current device becomes RHS with a trailing
`#`-comment cut and stripped (created if absent; a second block with the same name merges, later keys win). Any other
line is ignored. For a RELEVANT line the checks below run in order, the first failing check adds one to `unsupported` and ends the line (a line adds at most one): a KEY starting with `device[` (bracket forms) adds one to `unsupported` and is not
modelled; a line containing `$`, `{{` or a backslash adds one to `unsupported`; a RHS containing `##` adds one; otherwise the
RHS is cut at its first `#` and stripped to VALUE. VALUE parses as hyprlang `configStringToInt` (hyprlang-config.cpp:259-262,
round-46 pin `.ufo/waves/round-46/fetch/hyprlang-config.cpp`): starts with `true`, `on` or `yes` → 1 (checked first); else
starts with `false`, `off` or `no` → 0; else matches `[0-9]+` → that decimal integer; anything else (hex, sign, float, empty,
words) → `unsupported` +1, line ignored. Range (ConfigValues.cpp:277-280 pin, `fetch/Hyprland-ConfigValues.cpp`): `repeat_rate` 0..200,
`repeat_delay` 0..2000, `numlock_by_default` 0..1; an out-of-range value → `unsupported` +1, line ignored. A `device`-block key line
seen before any `name` line of its block (no current device) → `unsupported` +1, ignored. An `input:` KEY sets the GLOBAL
value; a device key sets the CURRENT device's value (source: `getDeviceInt` uses the device value when the user set it, else
the global option — legacy ConfigManager.cpp:1115-1123; built-in defaults 25 / 600 / 0 — ConfigValues.cpp:277-280, and
`applyConfigToKeyboard` clamps the stored rate and delay with `std::max(0, …)` — InputManager.cpp:1282-1283, a no-op on the modelled range).
Effective value for keyboard NAME (`*` when no `--keyboard`): device value if set for NAME, else global if set, else default;
`from` letters `D` / `G` / `-` respectively.

Output (stdout; each keyboard line in `--keyboard` argument order, repeats printed per argument):
`MADO_KBDOPT: keyboard=<NAME|*> repeat_rate=<n> repeat_delay=<n> numlock=<0|1> from=<x>/<y>/<z> unsupported=<U>`
(U = the run-wide unsupported count, the same on every line). With `--getoption`: one line per option in the order
`input:repeat_rate`, `input:repeat_delay`, `input:numlock_by_default`:
`MADO_KBDOPT_LIVE: option=<opt> config=<global effective value, default if unset> live=<int|?> verdict=<AGREE|DIFFER|UNKNOWN>`
where each non-empty `--getoption` line is a JSON object; an object with a string `option` and an integer (not boolean)
`int` records that option's live value (a later line for the same option wins); other objects are ignored; no record → `live=?`
`UNKNOWN`. Final line: `MADO_KBDOPT: DONE keyboards=<n> unsupported=<U> live=<NONE|AGREE|DIFFER|UNKNOWN>` (`NONE` without
`--getoption`; else `DIFFER` if any DIFFER, else `UNKNOWN` if any UNKNOWN, else `AGREE`). Exit 0 on a completed run.

Fixtures: `fixtures/c2/F01..F18/{args.json,expected.out,expected.rc,c*.conf,getoption.json}` (`args.json` is the argv list,
paths relative to the lane root; the harness runs the tool with cwd = the exported scratch tree so the paths resolve there;
F02 reads the committed host pin `fetch/host-input.conf` and `fetch/host-getoption.json`). Hold-out: eight fixtures H01–H08
sealed before the wave (commitment `c2.holdout_commit_sha256`: sha256 over, for each file in sorted relative-path order, the
line `<relpath>\0<sha256 of file bytes>\n`), revealed into `fixtures/c2-holdout/` at integration; they exercise the same
grammar on different inputs (key-before-name, nested `touchpad` blocks, boolean prefixes, duplicate keyboards, CRLF/tabs,
getoption anomalies, hex/sign tokens, variables and backslashes). The L1 holds the hold-out outside the repo; seats are not told its
path. Controls: `ctl/const-host.py`, `ctl/empty.py`, `ctl/lookup-committed.py` (committed, frozen).
Harness output: `MADO_R55_C2: rev=<rev> fixtures=<a>/18 holdout=<b>/8 holdout_commit=<ok|bad|absent> controls=<k>/3 verdict=<TARGET_MET|TARGET_MISSED>`.

## §C3 — correction grammar, legs and controls

Append-only: at `--rev`, the bytes of `corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md` begin with the
exact bytes of that file at the base commit `3b55b6e91e40f455dd56b2985e4ffc087ada92d5` (`prefix=identical`), followed by a
block that has a heading containing `Correction (round 55)`, a proposition row
`| P23 | P19 | <proposition> | S371 | Hyprland-ConfigActions.cpp:1554-1576 | … |` and rows `| Q01 | Hyprland-ConfigActions.cpp:<line> | `<quote>` |` … Q13, each id/line/quote byte-equal to `frozen-tables.json` `c3.q`.
Legs: `prefix` (not byte-identical), `rows:<id>` (Q row missing/duplicated/≠ frozen), `pin` (the round-52 pin's bytes do not hash to
`c3.pin_sha256`, or a Q quote is not exactly the stripped pin line at its line), `p23` (the P23 proposition cell lacks
`m_passPressed`, `== 1`, `== 0`, `PRESSED`, `RELEASED` and one of `otherwise`/`any other`/`else`; or its Supersedes cell ≠ `P19`),
`readme` (no README line naming `hyprland-synthetic-dispatch-r52-errata-r53.md` together with `P23`), `tables_sha`.
Output: `MADO_P19_FIX: rev=<rev> prefix=<identical|changed> rows=<a>/13 pin=<ok|bad> p23=<ok|bad> readme=<ok|bad> verdict=<V> missed=<legs>|none`.
C3 frozen controls (same scratch-repo method): C3-CTL-1 absent (the block removed = base) → `prefix`-clean but `rows`+`p23` missed;
C3-CTL-2 rewritten-prefix (one byte of the original P19 row changed) → `prefix`; C3-CTL-3 altered-quote (the Q09 quote with one
character changed) → `rows:Q09`; C3-CTL-4 old-arm-only (rows Q08–Q12 deleted) → `rows:Q08`; C3-CTL-5 old-wording (the P23 cell
reduced to the P19 sentence) → `p23`; C3-CTL-6 readme-missing (README line without `P23`) → `readme`.
Harness output: `MADO_R55_CONTROLS: claim=c3 good=<ok|bad> controls=<k>/6 verdict=<OK|FAIL>`.

## Seat boundaries (every seat)

Absolute lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`; a seat writes only its `Report:` file and its own
subdirectory next to it under `.ufo/waves/round-55/<wave>/` plus its scratch dir; no tracked-file edits, no git/jj mutations,
no host mutations; host reads are limited to `~/.config/hypr/input.conf`, `hyprctl getoption input:repeat_rate|input:repeat_delay|input:numlock_by_default -j`
and `hyprctl devices -j`. The sealed hold-out is not a seat input; a seat that finds it reports it and does not use it.

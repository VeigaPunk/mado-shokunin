# R55ExecTool3 — tools/mado-kbdopts.py draft (round 55, w1)

Deliverable: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55ExecTool3/mado-kbdopts.py` (single file, python3, executable bit set).
Also in that directory: `receipts.txt` (selftest, 18-fixture run, edge checks; its "live" block there is the FAILED first attempt, see below), `live-getoption.json`, `live-run.txt` (the real live run).
Nothing else written in the lane; scratch `/fast/scratch/hyaku/mado-r55/R55ExecTool3/` removed. No tracked file, git, jj or host state touched. Tools installed: none.

## What I did
Wrote the data model first (`Model`: `glob` dict, `devs` dict of dicts, `unsupported` counter; `effective()` returns value + `D`/`G`/`-`), then the parser (`parse_text`, `parse_int`, `parse_getoption`), `render`, setup errors (`Setup(reason)`), strict two-token arg parsing, `--selftest` (alone; 56 assertions, no file reads). Read-only: only `os.stat` + `open(..,'rb')` on --config/--getoption paths; stat+S_ISREG check before open so a FIFO is never opened. I did not read `tools/mado-devices.py` or any other seat's tool (task rule), so the docstring only follows the general style (purpose, usage, grammar, pins cited); see ambiguity A8.

## Results
`python3 -I mado-kbdopts.py --selftest` → `MADO_KBDOPT_SELFTEST: 56/56 assertions passed` rc 0.

Fixtures (cwd = lane root, argv from args.json, stdout bytes + rc vs expected.out/expected.rc): **18/18 PASS** (F01–F18 all PASS; rc 0 for F01–F14, F18; rc 2 for F15, F16, F17).
Defect found in my first run: F10 FAIL (unsupported=3, expected 4) — I had read "the stack joined with `:` then `:` then LHS" literally (empty stack → KEY `:LHS`). F10 input `device[kbd-a]:repeat_rate = 70` at top level shows that with an EMPTY stack KEY = LHS (no leading colon). Fixed (`":".join(stack + [lhs])`); re-ran: 18/18.

Live host run (the three JSON lines put in a scratch file; `hyprctl getoption <o> -j` read-only; `~/.config/hypr/input.conf` has repeat_rate=40, repeat_delay=250, numlock_by_default=true at lines 14,15,18):
```
MADO_KBDOPT: keyboard=* repeat_rate=40 repeat_delay=250 numlock=1 from=G/G/G unsupported=0
MADO_KBDOPT_LIVE: option=input:repeat_rate config=40 live=40 verdict=AGREE
MADO_KBDOPT_LIVE: option=input:repeat_delay config=250 live=250 verdict=AGREE
MADO_KBDOPT_LIVE: option=input:numlock_by_default config=1 live=1 verdict=AGREE
MADO_KBDOPT: DONE keyboards=1 unsupported=0 live=AGREE
```
rc 0. With `--keyboard at-translated-set-2-keyboard` the same values, `from=G/G/G` (`live-run.txt`). My first live attempt (inside the eval kernel) failed because that process lacked `HYPRLAND_INSTANCE_SIGNATURE`: `hyprctl` printed "HYPRLAND_INSTANCE_SIGNATURE not set!" to stdout, so the scratch file held non-JSON lines and the tool correctly answered `MADO_KBDOPT: SETUP bad_json`, rc 2. That attempt is the "live" block in `receipts.txt`; the authoritative result is `live-run.txt` (run from bash, signature set). The task's literal `--getoption <(...)` would give a FIFO path (`/dev/fd/N`), which this contract classifies `unreadable`; I used a file as instructed.

Edge checks I ran (receipts.txt): 1048577-byte file → `SETUP too_large`; exactly 1048576 bytes → accepted; directory → `unreadable`; FIFO → `unreadable` (not opened); getoption with a non-JSON line → `SETUP bad_json`; `--getoption` twice → `usage`; `--selftest --config a` → `usage`; `--keyboard * --config f` prints `keyboard=*`.

## Ambiguities (most-literal reading taken; other reading listed)
- A1 KEY with empty stack: literal text "stack joined with `:` then `:` then LHS" = `:LHS`; chosen reading = KEY is just LHS (join of stack+[LHS]). F10 forces this (top-level `device[kbd-a]:repeat_rate` must count). Not ambiguous after the fixture, but the sentence in registration.md is wrong for an empty stack.
- A2 `*` as device name: "device value if set for NAME" with NAME=`*` when no `--keyboard`. Literal: a device whose `name = *` is found and used (from letter `D`). Other reading: `*` means global only. Implemented literal.
- A3 Whitespace-only `--getoption` lines: "non-empty line" — implemented raw non-empty, so a line of just `\r` (CRLF blank line) → `bad_json`. Other reading: strip first, skip blank → would be accepted. Receipts: `crlf-blank` case → `SETUP bad_json`. Trailing `\r` on a JSON line is fine (json.loads tolerates it).
- A4 Setup-error precedence: files processed in argument order (config and getoption interleaved), `bad_json` raised when the getoption file is read; so an unreadable config later in argv than a bad-JSON getoption reports `bad_json`. Other reading: all path checks first, JSON validation last. `usage` always wins (argv checked before any file).
- A5 A `--getoption` file with no non-empty lines → no records, all three options `UNKNOWN` (not an error). A line of hyprctl error text is a non-object → `bad_json`.
- A6 Bracket forms: only a RELEVANT line counts (KEY starts `device[` and last component ∈ the three names). `device[k] {` block with `repeat_rate` inside counts (KEY `device[k]:repeat_rate`); other keys inside it don't. F10 agrees.
- A7 `}` on an empty stack is a no-op; `{` alone (empty category text) pushes `""`; a line with `=` ending in `{` is a key line, not a push.
- A8 Task says "docstring in the style of tools/mado-devices.py" yet forbids reading it: I could not match that style; the L1 should restyle if it differs.
- A9 Values: `true`/`on`/`yes` prefix tests are case-sensitive, `only`→1, `nope`→0 (prefix semantics per the pin text); `[0-9]+` is a full match with ASCII digits (Unicode digits are unsupported); leading zeros accepted (`007`→7); `int` that is a float/bool/missing string option is ignored; Python int-digit limit is lifted so a huge JSON integer is an integer, not `bad_json`.
- A10 Output encoding: keyboard names are written back as the original argv bytes (surrogateescape); config text decoded UTF-8 with replacement, so a device named with invalid bytes never matches an argv name that has the original bytes.

## Not verified
- Hold-out behaviour (sealed; not looked for or found).
- `quality/check-r55-controls.py` and the ctl/ stubs were not run (not a seat input).
- No concurrency/large-file performance test beyond the 1 MiB boundary.

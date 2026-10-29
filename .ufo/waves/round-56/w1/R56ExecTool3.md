# R56ExecTool3 — w1 report: mado-watchplan.py (C2)

## Did
Wrote `.ufo/waves/round-56/w1/R56ExecTool3/mado-watchplan.py` (single file, stdlib only, read-only, ~480 lines) strictly from registration §C2. Data model first (`Plan`: path list, event list, `unsupported`/`errors` counters, last accepted value), parser second, then watch list, getoption join, output. It did not read `tools/mado-binds.py` or any other seat's tool, and did not look for hold-out fixtures. `run(argv)` returns `(stdout, rc)`; the output is buffered, so the header counters are final before printing. Output is written as UTF-8 with surrogateescape, so non-UTF-8 filenames print byte-faithfully.

## Results (nothing below was edited; fixtures untouched)
- All 18 fixtures: `python3 -I <tool> <args>` with `{FX}` replaced by the absolute fixture dir, cwd = my scratch dir. Stdout compared byte for byte with `expected.out` and the exit status with `expected.rc`. F01–F18 are all PASS, `fixtures 18/18` (rc 0 for F01–F11, F13–F16; rc 2 for F12, F17, F18). Receipt: `w1/R56ExecTool3/fixtures-result.txt`.
- `python3 -I <tool> --selftest` → `MADO_WATCH: SELFTEST 47/47 assertions passed`, exit 0 (receipt `selftest.txt`). It writes only under a `tempfile.mkdtemp` directory (honours `$TMPDIR`) that it removes; after the run no `mado-watchplan-selftest-*` was left in /tmp. Informational only. The first two selftest runs failed 5 and then 1 assertions because of my own wrong expectations (single-character source names are `bogus` by rule; the canonical path was wrong). I fixed the assertions, not the tool.
- Live, read-only: `hyprctl getoption misc:disable_autoreload -j` (→ `{"option": "misc:disable_autoreload", "int": 0, "set": false }`) saved to scratch, then `python3 -I <tool> --config $HOME/.config/hypr/hyprland.conf --home $HOME --getoption <that file>` → rc 0, saved as `w1/R56ExecTool3/live.txt`. Decisive lines:
  - `MADO_WATCH: config=/home/vgpnk/.config/hypr/hyprland.conf autoreload=on disable_autoreload=unset paths=40 unsupported=0 errors=0`
  - `MADO_WATCH_LIVE: option=misc:disable_autoreload config=0 live=0 verdict=AGREE`
  - `MADO_WATCH: DONE watches=40 unsupported=0 errors=0 live=AGREE`
  - No `canonical` watch lines: no listed path is itself a symlink (`os.path.islink` is false for files reached through a symlinked directory such as omarchy `current/theme`).
- Extra probes: a multi-line (pretty-printed) JSON getoption file → `SETUP bad_json` rc 2 (see defect 1); repeated `--home` → `SETUP usage` rc 2.
- No tool was installed. Scratch `/fast/scratch/hyaku/mado-r56/R56ExecTool3` was removed. Nothing was written under ~/.config or ~/.local, no git/jj mutation, no compositor-state command.

## Ambiguities (registration text wins; both readings listed, the first is implemented)
1. Which option name records a live value: "an object with a string `option` and an integer `int` records that option's live value". (a) Implemented: only `option == "misc:disable_autoreload"` records; any other option name is ignored. (b) Any string-`option` object records. F12 line 1 (`misc:other`, int 1) cannot separate them because line 2 is bad_json. Under (b) a dump of another option would give DIFFER/AGREE instead of UNKNOWN.
2. Setup-failure precedence when several apply is unspecified. Implemented in the order of the listed reasons: `usage`, then getoption `unreadable`, then `too_large` (config and sourced files during the walk, then the getoption size), then `bad_json` (checked after the config walk). Reading: a config `too_large` wins over a getoption `bad_json`. The reverse order (getoption first) is also possible.
3. `--display-root` "DIR is either the given string (trailing `/` removed) or its realpath": one trailing `/` is removed (not all); the given-string candidate is tried before the realpath; first match wins. If both match with different lengths the given form wins. DIR=`/` becomes the empty prefix, so `/a` prints `$ROOT/a`.
4. "stripped" for getoption lines is Python `str.strip()` (all Unicode whitespace), unlike the config strip set (space, tab, CR, LF, VT, FF). Getoption bytes are decoded UTF-8 with replacement (not stated). Python `json.loads` leniencies are inherited: `NaN`, `Infinity`, and duplicate keys (last wins). A float such as `1.0` is not an integer. `{"int": 1e0}` is a float and is ignored.
5. `hyprctl getoption -j` output is read per line, as written. Single-line output (as on this host) works; a pretty-printed multi-line object gives `bad_json`.
6. `too_large` is "larger than 1048576 bytes" and is measured by bytes read (cap+1), not by `st_size`. A sourced regular file that cannot be opened is listed and not parsed, per spec. A symlink loop or dangling link raises in `os.stat`, giving `inaccessible`.
7. Case sensitivity of `true/on/yes/false/off/no` is taken as case-sensitive (literal). Because the test is `startswith`, `online`, `nothing`, `yesterday` count as 1, 0, 1; `no` is checked after `false/off`, and the true-group is first.
8. The "line contains `$`, `{` or backslash" test is applied to the stripped raw line (the whole line, including any comment text after `#`). So `misc:disable_autoreload = 1 # note {x}` is `unsupported`. The wording "the line" could also mean pre-comment text.
9. A line with `=` that also ends in `{` (e.g. `a = b {`) is a key/value line (the `=` rule is applied first). A `}` with an empty stack is ignored.
10. Depth: main is depth 0; a file at depth 17 is recorded (path list) and counted `unsupported` once per source line that reaches it, but not parsed. A self-sourcing file therefore gives paths=18, unsupported=1.
11. The canonical watch is always `type=file` even when the symlink target is a directory (literal text); the primary type then comes from `isdir`.
12. `--selftest` output wording is not specified; I print `MADO_WATCH: SELFTEST <n>/<n> assertions passed` (exit 1 if any fail, with failing names on stderr). `--selftest` combined with any other token is `usage`.

## Defects / disagreements found
1. No fixture disagrees with registration.md; no fixture is believed wrong. F12's note ("UNKNOWN: no record; non-object lines are bad_json") describes the intent, but its expected output is `SETUP bad_json`, which matches the grammar.
2. Notable consequence: `hyprctl getoption -j` is parsed per line, so a multi-line dump yields `bad_json`. Not a defect in the text; this host emits one line.

## Not verified
- Whether Hyprland itself matches this model; only the registration is implemented.
- Behaviour on non-UTF-8 filenames, unreadable (permission-denied) sourced files, and files over 1 MiB beyond the selftest `too_large` cases, which are covered only by the selftest and not by any fixture.
- The harness `quality/check-r56-controls.py --claim c2` and the three `ctl/` stubs were not run (not in my assignment).

## Deliverables
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56ExecTool3/mado-watchplan.py`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56ExecTool3/live.txt`, `fixtures-result.txt`, `selftest.txt`

# R56ExecTool1 — tools/mado-watchplan.py (w1)

## What I did
Implemented the single-file, stdlib-only tool strictly from registration.md §C2, as a plain line-by-line state machine (no
third-party code, no subprocess, no sockets; the only writes are inside `--selftest`'s private `tempfile.mkdtemp` dir, removed in
a `finally`). Read claims-frozen.md and registration.md first; no edits to either. No tools installed.

Deliverables (all under `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56ExecTool1/`):
- `mado-watchplan.py` (sha256 `be877db2dd04620dafdebf861f55095b689ce9642de899f866ed592ae032ddf6`)
- `live.txt` — the live host run, `getoption.json` — the `hyprctl getoption misc:disable_autoreload -j` output used for it
- `fixtures-result.txt`, `fixture-driver.py` — fixture driver and its output

## Commands and decisive output
Fixture driver: `{FX}` replaced by the absolute fixture dir (copied with `cp -a`, symlinks preserved, into scratch), run with
`python3 -I <tool> <args>`, cwd = scratch export root, stdout bytes compared with `expected.out` and exit status with `expected.rc`:
```
F01..F18 PASS   (F12/F17/F18 rc 2 as expected, all others rc 0)
18 / 18
```
Fixtures were not edited. Selftest: `python3 -I mado-watchplan.py --selftest` → `MADO_WATCH_SELFTEST: 38/38 assertions passed`, rc 0.

Live (read-only): `hyprctl getoption misc:disable_autoreload -j` → `{"option": "misc:disable_autoreload", "int": 0, "set": false }`;
`python3 -I <tool> --config $HOME/.config/hypr/hyprland.conf --home $HOME --getoption <that file>` exit 0:
```
MADO_WATCH: config=/home/vgpnk/.config/hypr/hyprland.conf autoreload=on disable_autoreload=unset paths=40 unsupported=0 errors=0
... 40 primary watches, all type=file, no canonical (no symlinked sourced files), no events ...
MADO_WATCH_LIVE: option=misc:disable_autoreload config=0 live=0 verdict=AGREE
MADO_WATCH: DONE watches=40 unsupported=0 errors=0 live=AGREE
```
Scratch `/fast/scratch/hyaku/mado-r56/R56ExecTool1/` removed. No git/jj mutation. No hold-out path seen or used.

## Defects / ambiguities (most literal reading taken in the tool)
1. **F12 note vs spec.** `note.txt` says "UNKNOWN: no record; non-object lines are bad_json"; expected is `SETUP bad_json`, rc 2 (go.json holds `[1,2]` and `"x"`). Expected output matches the registration text; only the note's leading word "UNKNOWN" is misleading. Tool follows the text. Not a fixture error.
2. **Order of setup checks** when more than one applies is unspecified. I check: usage → `--getoption` (unreadable, too_large, bad_json) → config tree (too_large on the first oversized file met). Alternative reading: config tree first. Only matters for fixtures with two simultaneous faults.
3. **`too_large` for a sourced file is discovered mid-run**; the tool buffers all output and prints only the SETUP line (stdout "exactly" that). Size is measured by reading up to 1048576+1 bytes, so it is exact for non-stat-size files too.
4. **`--display-root` candidates.** "DIR is either the given string (trailing `/` removed) or its realpath": I remove ONE trailing `/`, try the given string first, then the realpath; first match wins. If both match with different prefixes, the result depends on this order (edge case; none in the fixtures). `--display-root /` becomes the empty prefix, so every absolute path prints `$ROOT/...`.
5. **What `display()` applies to.** Only grammar slots marked `display(...)` (config, `via=` parts, SKIP `path=`, watch `path=`). The `source=<RAW>` field of ERROR lines is printed raw, even when RAW is absolute under the display root. Alternative: also display it.
6. **Canonical watch `via`** is the via of its primary (fixture F05/F06 shows this; the spec text does not say it).
7. **`bad_json` strip set.** "stripped" for the getoption lines uses the same set as config lines (space, tab, CR, LF, VT, FF). Python's `json.loads` is the JSON parser, so it accepts `NaN`/`Infinity`/duplicate keys as objects/numbers; `{"int": NaN}` is a float, so it is ignored. `{"int": 1.0}` is ignored (not an integer). Lines are split on `\n` only.
8. **Sorting.** The spec says "bytewise" and `sorted(glob.glob(VALUE))`; I use `sorted()` on `str`, which equals UTF-8 byte order except for undecodable (surrogateescape) names. Not exercised.
9. **Config that is a directory or unreadable file**: listed (dir → `type=dir` with the dir mask) and not parsed; an unreadable-by-permission regular main config is silently not parsed (OSError). A sourced file that stats regular but fails to open is likewise listed and not parsed.
10. **Argument parsing**: a value is the next token whatever it is; since every value must start with `/`, a value such as `--home` is `usage`. An odd token count is `usage`. `--selftest` is recognised only as the sole argument; anything else containing it is `usage`.
11. **Depth cap**: main is depth 0; a file at depth 17 is recorded and counted `unsupported` but not read (selftest asserts `paths=18 unsupported=1` for a self-sourcing file).
12. **Selftest output line** format is my choice: `MADO_WATCH_SELFTEST: <n>/<n> assertions passed` (spec only names `<n>/<n> assertions passed`); a failure prints `MADO_WATCH_SELFTEST: FAIL <name>` lines and exits 1.
13. Unspecified rule resolved literally: an unmatched `}` on an empty stack is ignored; a line with `=` that also ends in `{` is a key/value line.

## Not verified
- Behaviour against Hyprland itself (no event generated, as declared).
- The three `ctl/` stubs and the harness `quality/check-r56-controls.py --claim c2` were not run (not in scope).
- Hold-out fixtures H01-H08 (sealed; not looked for).
- Non-UTF-8 filenames, `--display-root` realpath-vs-given conflicts, and oversized sourced files were not exercised beyond the selftest's single config-oversize case.

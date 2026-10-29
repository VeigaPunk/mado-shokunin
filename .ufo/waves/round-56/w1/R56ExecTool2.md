# R56ExecTool2 — w1 report (C2 tool build)

## Deliverables (all under /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56ExecTool2/)
- `mado-watchplan.py` (sha256 `1930f67551e800640f377bb758bfa5443704cb06102330517d377ecd696678d2`): single file, python3 stdlib only, regex-assisted parser, built strictly from registration §C2. Exit 0 on a completed run, 2 on setup failure (stdout exactly `MADO_WATCH: SETUP <reason>`). Includes `--selftest` (alone only; other combination = `usage`).
- `fixtures-run.txt`: result of the 18-fixture run. `fixture-driver.py`: driver used (the export dir was replaced by the token `EXPORT_DIR` after the run; it is scratch-only code).
- `live.txt`: live read-only run output.

## What I did
1. Read registration.md and claims-frozen.md. Did not read tools/mado-binds.py, any other seat's tool, the ctl stubs, or any hold-out path (none stumbled on).
2. Wrote the tool; exported `fixtures/c2` at lane commit 3423ae28… with `git archive | tar -x` into scratch (symlinks preserved), substituted `{FX}` per args.json, ran `python3 -I <tool> <args>` with cwd = export root, compared stdout bytes and rc.
3. Ran `--selftest`, then the live run. Scratch removed.

## Fixture results (stdout bytes == expected.out and rc == expected.rc)
F01 PASS, F02 PASS, F03 PASS, F04 PASS, F05 PASS, F06 PASS, F07 PASS, F08 PASS, F09 PASS, F10 PASS, F11 PASS, F12 PASS (rc 2), F13 PASS, F14 PASS (empty tree: no `tree/` dir exists in the export; config → `type=missing`), F15 PASS, F16 PASS, F17 PASS (rc 2), F18 PASS (rc 2). **18/18.** No fixture edited; no fixture believed wrong.

## Selftest
`python3 -I mado-watchplan.py --selftest` → `MADO_WATCH_SELFTEST: 39/39 assertions passed` (private `tempfile.mkdtemp` dir, removed in `finally`). First run had 2 failing assertions that were wrong expectations in my own selftest (unsupported count 3 vs correct 4; a getoption fixture that actually did carry a record); fixed.

## Live run
```
python3 -I mado-watchplan.py --config $HOME/.config/hypr/hyprland.conf --home $HOME --getoption <file with `hyprctl getoption misc:disable_autoreload -j`>
```
getoption file content: `{"option": "misc:disable_autoreload", "int": 0, "set": false }` (single line, so the line-wise JSON rule works on real output). Result (live.txt): `config=… autoreload=on disable_autoreload=unset paths=40 unsupported=0 errors=0`, 40 primary watches, no canonical ones, `MADO_WATCH_LIVE: option=misc:disable_autoreload config=0 live=0 verdict=AGREE`, `DONE watches=40 unsupported=0 errors=0 live=AGREE`, exit 0. The source closure reaches `~/.local/share/omarchy/…`, `~/.config/omarchy/current/theme/…` and `~/.local/state/omarchy/toggles/hypr/*.conf` (2 files) by read-only file reads/glob.

## Ambiguities (most literal reading taken; both readings)
1. **Which `option` a getoption record binds to.** Text: "an object with a string `option` and an integer `int` records that option's live value". Literal (implemented): ANY string `option` records, regardless of its name (so `{"option":"misc:other","int":1}` yields live=1). Alternative: only `option == "misc:disable_autoreload"` records. No fixture decides it (F12's `misc:other` line only feeds bad_json).
2. **Precedence among setup reasons when several apply** (e.g. getoption not JSON and a sourced file too large). Text gives none. Implemented: usage → unreadable (getoption) → too_large (getoption, then config/source closure) → bad_json (getoption JSON checked last, after the tree is read). Alternative: bad_json before reading the tree.
3. **"stripped" for getoption lines.** Used the model's strip set (space, tab, CR, LF, VT, FF), not Unicode `str.strip()`. Alternative would also strip e.g. NBSP/U+2028 before `json.loads`.
4. **`--getoption` that is a symlink to a regular file**: accepted (`os.stat` follows). "non-regular" could be read as lstat; not decided by any fixture.
5. **`--display-root` "trailing `/` removed"**: ONE trailing slash removed (singular). Alternative: all trailing slashes. When both the given string and its realpath match a path, the given string wins (alternative: longest prefix).
6. **"Absolute" argument test** = value starts with `/`; value used verbatim (no normalisation). `--config` equal to something like `--home` is just a relative value → `usage`.
7. **Keyword case**: `true/on/yes/false/off/no` prefix tests are case-sensitive (literal "starts with `true`"); `[0-9]+` matched with `re.fullmatch` on ASCII digits only; no sign accepted.
8. **`line contains $ { \`** for the autoreload key is tested on the whole stripped line (including a trailing comment), `##` on the RHS only, as written.
9. **Depth cap**: main = depth 0; a file at depth 16 that sources a regular file lists it, counts `unsupported` +1 and does not parse it (a self-including file yields paths=18, unsupported=1). Literal from "depth+1 > 16".
10. **Glob order** sorted by `os.fsencode` bytes (the registration says bytewise); NUL in a pattern is treated as no match. Unmatched `}` on an empty stack is ignored.
11. **Selftest line prefix**: text only says it prints `<n>/<n> assertions passed`; I print `MADO_WATCH_SELFTEST: <n>/<n> assertions passed` (failures print `MADO_WATCH_SELFTEST: FAIL <name>` and exit 1). Informational, not in PRED-C2.
12. Symlink-to-directory-valued main config: `type=dir` with the dir mask (isdir follows links) plus a canonical `type=file` watch if islink — follows the text; no fixture.

## Defects / not verified
- No fixture defect found. Registration text is satisfiable as written for all 18.
- Not verified: behaviour on non-UTF-8 filenames (output uses surrogateescape bytes; no test), unreadable-but-existing sourced files (permission denied: listed, not parsed — implemented, not run), file larger than 1 MiB in a sourced file (selftest covers config and getoption only), and the ctl stubs/hold-out/harness (not a seat input). No tooling installed.
- This seat is not a non-author reviewer.

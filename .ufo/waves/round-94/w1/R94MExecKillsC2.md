# R94MExecKillsC2 — C2 kill-sets for the selftest-strength gate (round 94, wave w1)

Status: DRAFT (all runs below are DRAFT runs per the round-94 scoring rule; no measurement is claimed).
Seat: R94MExecKillsC2 (leaf; no subagents dispatched, no peers messaged). Date: 2026-11-07.
Base revision: a3de997289014e7dbf1d73ae206be1d6f8cdadd0 (master). Tools unchanged; gate unchanged (sha256 2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b).

## Files written (mine)

- `.ufo/waves/round-94/build/mado-xdgmime-kills.c2.json` — sha256 `126b508aa1841ba99fa17ecaef46a5a79cdee99956ac2a605479b96122f09ea9`, 12 kills, `selftest_checks: 12`.
- `.ufo/waves/round-94/build/mado-mime-kills.c2.json` — sha256 `d930689e6ff82e51722195e0c8d209fe46fb4697fd10f01f33cec30e98e81601`, 15 kills, `selftest_checks: 17`.
- this report.

Both kill-sets follow the gate's schema (docstring of `quality/check-selftest-strength.py`): `tool` (repo-relative), `tool_sha256` (pinned to the current tools: mado-xdgmime.py `4e7fff9e…7fd88`, mado-mime.py `2532ccb5…71a5e` — byte-identical to the pins in the round context), `selftest_argv: ["--selftest"]`, `fail_line_prefix`/`result_line_prefix` (`MADO_XDGMIME_SELFTEST_FAIL: `/`MADO_XDGMIME_SELFTEST: ` and `MADO_MIME_SELFTEST_FAIL: `/`MADO_MIME_SELFTEST: `), `selftest_checks`, `note`, `kills` with `{id, find, replace, must_fail}`. Every `find` occurs exactly once in the tool's non-selftest prefix (gate-enforced; also asserted in my driver). Every `must_fail` is the exact sorted FAIL-label list the mutated copy's `--selftest` printed in scratch (never an expectation).

## Coverage

Union of `must_fail` over kills = every check label: 12/12 for mado-xdgmime.py, 17/17 for mado-mime.py. No label is unreachable; one mado-mime label is reachable only by a multi-label kill (below).

### tools/mado-xdgmime.py (12 kills, 12 labels)

| id | production mutant (find → replace, both outside `def selftest(`) | must_fail |
|---|---|---|
| x01-m03-second-id | `for app in expand(ifs_split(result, b";"), self.cwd):` → `…self.cwd)[:1]:` (only the first `;`-id tried) | m03 |
| x02-m05-desktop-file-first | desktop prefix genexp → `prefix = b""` (`<desktop>-mimeapps.list` never consulted) | m05 |
| x03-m09-last-line-wins | `elif result is None and indefault and …` → `elif indefault and …` (last matching line wins) | m09 |
| x04-m16-cr-stripped | `lines_of` gains a CR-strip pass | m16 |
| x05-d09-builtins-dropped | `command_v`: `s in BUILTINS or` removed (`true` resolves on PATH) | d09 |
| x06-f06b02-grep-anchored | `bre()` returns `re.compile(b"^" + out)` (grep BRE anchored) | f06, b02 |
| x07-f09-echo-flags-kept | `echo_out` option match disabled (`-n` echoed literally) | f09 |
| x08-b02-initialpref-ignored | `InitialPreference=` line filter disabled (p1 wins ties) | b02 |
| x09-s01-lxqt-branch-dead | `if de == "lxqt":` → `if de == "lxqt-x":` (rc 3 branch dead) | s01 |
| x10-s05-no-slash-rc0 | no-slash refusal returns rc 0 instead of 1 | s05 |
| x11-s08-version-string | `xdg-mime 1.2.1` → `xdg-mime 1.2.0` | s08 |
| x12-rfc-guard-off | `if not TYPE_CHARS.fullmatch(mime):` → `if False and …` (refusal gone) | RFC 6838 |

(Full labels: "m03 list: second id installed"; "m05 desktop-specific file first"; "m09 only a file's first matching line counts; the next file is read"; "m16 CR kept in the id"; "d09 Exec=true is a builtin: not installed"; "f06 unanchored grep in mimeinfo.cache"; "b02 InitialPreference picks"; "f09 a cache value -n is an echo option"; "s01 LXQt: rc 3"; "s05 no slash: rc 1"; "s08 --version"; "type outside RFC 6838 refused".)

### tools/mado-mime.py (15 kills, 17 labels)

| id | production mutant | must_fail |
|---|---|---|
| a01-default-additions-off | `default()`: additions stage `self._mime_lookup(j, t, results, block)` → `pass` | cache addition is default; subdir id; alias unaliased; added group…file order; unloadable list skipped; masked lower addition…taken (6) |
| a02-lists-keep-hidden | `app_info_new` returns `True` instead of `not hidden` | hidden and unloadable dropped…; parent in registered…; removal blocks lower addition (3) |
| a03-subdir-prefix-flat | `_walk` recursion drops the `+ "-"` subdir prefix | subdir id; alias unaliased; parent in registered…; desktop list wins (4) |
| a04-alias-never-resolves | `self._unalias[t] = r if r is not None else t` → `= t` | alias unaliased |
| a05-no-parent-fallback | `type_list`: `if fallback:` → `if False and fallback:` (ancestors never walked) | parent in registered not recommended |
| a06-default-first-holder | `default()` load test → first-dir-holds test | unloadable only -> none; desktop list additions ignored (2) |
| a07-default-rejects-hidden | `default()` accepts only `(True, False)` loads (Hidden rejected at default stage) | hidden default accepted; other desktop ignores it; masked lower addition…taken (3) |
| a08-mimeapps-before-desktop-list | `DesktopDir.__init__`: `mimeapps.list` read before the per-desktop lists | desktop list wins |
| a09-desktop-list-additions-on | per-desktop `_read` permitted flag `False` → `True` | desktop list additions ignored |
| a10-hyprland-read-always | `for d in desktops:` → `for d in desktops + ["hyprland"]:` | other desktop ignores it |
| a11-removals-ignored | `_mime_lookup`: `for r in tw.removals or []:` → `for r in []:` | removal blocks lower addition |
| a14-mask-off | `_masked`: `if names and app in names:` → `if False and …` | masked lower addition skipped, hidden one taken |
| a15-default-first-holder-load | `default()` per-app scan returns only from the first dir holding the id (unloadable there ⇒ None) | default from masked id still loads in a lower dir |
| a16-desktops-filter-loose | `current_desktops` token filter drops the `isalnum()/"-_"` clause ("bad/x" admitted) | desktops |
| a17-fgets-empty-line | `_pairs_from_text`: `for line in _fgets_lines(data):` → `… or [b"mado x\n"]:` | fgets chop |

### Multi-label notes and dropped attempts

- mado-mime label "added group is read before removed whatever the file order" is produced redundantly by production code (loop order in `_read`, `_expand`'s first-list-taken-as-is rule, and the `r not in hits` removals guard all have to co-operate). Three narrow single-label mutants were built and **survived** (`--selftest` still rc 0, i.e. they change nothing observable), so they are not in the kill-set: (1) swapping the ADDED/REMOVED loops in `_read`; (2) disabling `_expand`'s `if block and a in block: continue`; (3) dropping `r not in hits` from the removals guard in `_mime_lookup`. The label is covered exactly by kill a01 (must_fail list includes it).
- Kills a02, a03, a06, a07 legitimately fail more than their primary label (a02 → 11 via hidden-b keeping "removal blocks lower addition" empty; a03 → 8 because "sub-d.desktop" no longer exists; a06 → 9 because the expected `None` there relies on c being unloadable; a07 → 10 and 14 because both expect the hidden b.desktop as default). `must_fail` records the measured reality.

## Verification (DRAFT runs; commands + exit codes)

Scratch: `S=/fast/scratch/hyaku/mado-r94/R94MExecKillsC2` (driver `S/driver.py`; every mutated copy and every neutralised copy materialised and run under `S/`, `TMPDIR` pointed inside `S`). Nothing outside my two build JSONs and this report was written in the lane; no git/jj mutation anywhere; no host mime database touched; no tool installs (none needed).

1. Per-kill measurement: mutated copy written to `S/run/<key>/<id>.py`, run `python3 -I <copy> --selftest` (cwd and TMPDIR in `S/run/<key>`); FAIL lines collected via the tool's fail prefix; `must_fail` = that exact list. All 27 included kills: rc 1 with the listed FAIL set; zero SURVIVED in the final sets (survivors/duplicates dropped before finalising).
2. Gate, unmodified tools (sha pinned, no drift flag):
   - `python3 -I quality/check-selftest-strength.py --tool tools/mado-xdgmime.py --kills .ufo/waves/round-94/build/mado-xdgmime-kills.c2.json --scratch-root $S/g`
     → `SELFTEST_STRENGTH: OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0`, rc 0
   - `python3 -I quality/check-selftest-strength.py --tool tools/mado-mime.py --kills .ufo/waves/round-94/build/mado-mime-kills.c2.json --scratch-root $S/g`
     → `SELFTEST_STRENGTH: OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0`, rc 0
3. Single-check neutralisation of every label (`    failed = [n for n, ok in checks if not ok]` → `… if not ok and n != "<label>"`), gate run `python3 -I quality/check-selftest-strength.py --tool <neutralised copy> --kills <kill-set> --allow-sha-drift --scratch-root $S/g`; all 29 printed WEAK with rc 1 (survived or wrong_check > 0 in each; per-label counts differ, verdict identical):

```
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-xdgmime.py kills=12 held=11 survived=1 wrong_check=0 | m03 list: second id installed
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-xdgmime.py kills=12 held=11 survived=1 wrong_check=0 | m05 desktop-specific file first
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-xdgmime.py kills=12 held=11 survived=1 wrong_check=0 | m09 only a file's first matching line counts; the next file is read
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-xdgmime.py kills=12 held=11 survived=1 wrong_check=0 | m16 CR kept in the id
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-xdgmime.py kills=12 held=11 survived=1 wrong_check=0 | d09 Exec=true is a builtin: not installed
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-xdgmime.py kills=12 held=11 survived=0 wrong_check=1 | f06 unanchored grep in mimeinfo.cache
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-xdgmime.py kills=12 held=11 survived=1 wrong_check=0 | f09 a cache value -n is an echo option
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-xdgmime.py kills=12 held=10 survived=1 wrong_check=1 | b02 InitialPreference picks
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-xdgmime.py kills=12 held=11 survived=1 wrong_check=0 | s01 LXQt: rc 3
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-xdgmime.py kills=12 held=11 survived=1 wrong_check=0 | s05 no slash: rc 1
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-xdgmime.py kills=12 held=11 survived=1 wrong_check=0 | s08 --version
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-xdgmime.py kills=12 held=11 survived=1 wrong_check=0 | type outside RFC 6838 refused
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-mime.py kills=15 held=14 survived=0 wrong_check=1 | cache addition is default
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-mime.py kills=15 held=14 survived=0 wrong_check=1 | hidden and unloadable dropped from lists
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-mime.py kills=15 held=13 survived=0 wrong_check=2 | subdir id
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-mime.py kills=15 held=12 survived=1 wrong_check=2 | alias unaliased
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-mime.py kills=15 held=12 survived=1 wrong_check=2 | parent in registered not recommended
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-mime.py kills=15 held=14 survived=0 wrong_check=1 | unloadable only -> none
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-mime.py kills=15 held=14 survived=0 wrong_check=1 | hidden default accepted
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-mime.py kills=15 held=13 survived=1 wrong_check=1 | desktop list wins
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-mime.py kills=15 held=13 survived=1 wrong_check=1 | desktop list additions ignored
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-mime.py kills=15 held=13 survived=1 wrong_check=1 | other desktop ignores it
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-mime.py kills=15 held=13 survived=1 wrong_check=1 | removal blocks lower addition
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-mime.py kills=15 held=14 survived=0 wrong_check=1 | added group is read before removed whatever the file order
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-mime.py kills=15 held=14 survived=0 wrong_check=1 | unloadable list skipped
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-mime.py kills=15 held=12 survived=1 wrong_check=2 | masked lower addition skipped, hidden one taken
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-mime.py kills=15 held=14 survived=1 wrong_check=0 | default from masked id still loads in a lower dir
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-mime.py kills=15 held=14 survived=1 wrong_check=0 | desktops
rc=1 | SELFTEST_STRENGTH: WEAK tool=tools/mado-mime.py kills=15 held=14 survived=1 wrong_check=0 | fgets chop
```

Neutralised-flagged tally for PRED-C2-r94-v1 (ii): 29/29 (12 xdgmime + 17 mime), DRAFT.

## Risks / notes for the L1

- `x05-d09-builtins-dropped` depends on the host resolving `true` on the selftest PATH's `/usr/bin` (verified present: `test -x /usr/bin/true`). Any environment without coreutils' `true` under `/usr/bin` would change that kill's `must_fail`; the frozen `tool_sha256` pins the tools, and the counter re-runs the gate at measurement on this host.
- The three survived mado-mime mutants are recorded above so the counter's frozen hand-weakenings (panel) can avoid relying on the same non-discriminating regions.
- Scratch directory `S` deleted after this report was written; nothing cited was left only in scratch (all verdict lines are inline above).
- No dead steps. No tool installs or upgrades (nothing outside the preinstalled python3/bash was used).

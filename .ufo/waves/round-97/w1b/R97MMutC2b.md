# R97MMutC2b — frozen C2 control panel (v2 counter selftest: 20 neutralisations, 6 broken modes)

Seat: mutation-tester, wave w1b, round 97. Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`,
base revision `e6152b589c2c6a28426c28263c4bcc3c46398be4`. Scratch
`$HYAKU_SCRATCH/mado-r97/R97MMutC2b` (deleted before yield). Tool installs: none.

## 1. Artifact

`controls/counter-selftest-panel-v2.json` — sha256
`9fb702a2a353a2b8df8470a73a82419729cfc4c59da4a4ea9cf79f2409d0cda1`, ASCII. 2 counters x **10**
neutralisations (20 rows, ids `st-fixture-dir` … `st-scratch-clean`), 6 broken rows (3 per counter), one
`stub` section (the frozen always-OK echo control), one `controls` note. Extra top-level keys are ignored
by the v2 runner, which reads only `counters` and `broken`; validated with the runner's own
`validate_panel(panel, 6, setup)` — `OK`, no setup message.

Frozen against the **.v2** selftest counters — the seat's named artifacts, both fixture-driven, 10
`st-*` checks each:

| input | sha256 |
|---|---|
| `quality/counters/c1-r96-magictext.py` (= `build/c1-r96-magictext-selftest.v2.py`) | `4f6783848ded9c63f934c68a24da856369895987651d0f66fdd6920f07aaa64d` |
| `quality/counters/c2-r96-selftest-kills.py` (= `build/c2-r96-selftest-kills-selftest.v2.py`) | `54143b8a28f2be4b2f1361c443d32156a68fd088c7cdb9c9030ca7415002217b` |
| runner `build/c2-r97-counter-selftest.v2.py` | `abb17a019141c57635f1c9771ad449a4348dfdc75a0bb57af3776075fe06b879` |
| fixtures `.ufo/waves/round-97/selftest-fixtures-v2/` | pins.json + c1/ (10 files) + c2/ (7 files) + common/ (5 files) |

The wave carried two counter generations on disk until the end: the w1 `.py` pair (7 `C1-*`/`C2-*`
checks, shas `dd9b5a0b`/`d4689f5a` at 14:35) and the `.v2` pair (10 `st-*` checks). This panel targets
the `.v2` bytes because they are the artifact the seat names and because the runner's declared st-*
vocabulary and the owners' measured broken-scene behaviour belong to them. **The L1 must land the .v2
bytes at the canonical `quality/counters/*.py` paths**, otherwise the panel's find anchors miss.
(The declaration's counting command names `controls/counter-selftest-panel-r97.json`, the stale w1
panel, while this freeze lives in `counter-selftest-panel-v2.json`; the two names must converge before
the replay.)

## 2. Verification method (and its limit)

The counting command reads counters and fixtures from `git show --rev:...`, so the v2 runner cannot be
executed end-to-end before the L1 commits the wave artifacts (seats never commit). Every row was
verified with a byte-exact mirror of the runner's invocation:

- layout root `<root>` with the counter at `<root>/quality/counters/<name>.py`, the fixture tree at
  `<root>/.ufo/waves/round-97/selftest-fixtures-v2/`, cwd `<root>`, env
  `PATH=/usr/bin:/bin HOME=<root> TMPDIR=<root> LC_ALL=C.UTF-8 MADO_SELFTEST_REPO=<root>`;
- green leg and every neutralisation: `python3 -I <counter> --selftest --fixture-dir <root>/.ufo/waves/round-97/selftest-fixtures-v2`;
- each `find` counted in the counter bytes (must be exactly 1), replaced once, counter bytes rewritten
  in place, rerun identically, original bytes restored;
- broken rows: missing-input = counter alone in a scene with `--fixture-dir <scene>/absent-fixtures`;
  wrong-rev = a scene fixture tree with every blob truncated to 0 bytes; mutated-tool = the scene tree
  with `\n# mutated-tool probe\n` appended to the row's `path`; each run with that tree as
  `--fixture-dir` (the counter sees only the passed tree, so this is equivalent to the runner's
  sibling-tree layout);
- the always-OK control is the runner's `ECHO_STUB` verbatim (prints every panel id as a
  `MADO_COUNTER_SELFTEST_FAIL:` line at rc 1 without running a check), frozen in the panel's `stub`
  section. The runner's credit rule needs the judged bytes to carry the row's `find` anchor exactly
  once; the stub carries 0/20 anchors, so `always_ok_flagged=0` (measured, not asserted).

Full run against the frozen bytes: `killed_only=20/20`, `multi=0`, `other=0`; green baselines
`checks=10 failed=0` for both counters; stub `rc=1`, 20 FAIL lines, `credited=0`; broken rows `6/6`.

## 3. Neutralisations — 20/20 `KILLED_ONLY`, 0 survivors

Every row: rc 1, `MADO_COUNTER_SELFTEST: checks=10 failed=1`, the only `MADO_COUNTER_SELFTEST_FAIL:`
line is the declared id. Nine rows per counter use the artifact's own definition-line anchors (the
`_ST_*` constants and the pin tuple); `st-fixture-dir` uses an expression edit because the owner's
`_ST_PINS_REL` rewrite cascades to all ten checks (measured: fails=10), while
`add("st-fixture-dir", False)` isolates it (fails=1).

c1 — `quality/counters/c1-r96-magictext.py` (green `checks=10 failed=0` rc 0):

| id | neutralised anchor | rc | fails |
|---|---|---|---|
| `st-fixture-dir` | `add("st-fixture-dir", fixtures is not None and os.path.isfile(...))` -> `add("st-fixture-dir", False)` | 1 | `st-fixture-dir` |
| `st-tool-pin` | pin tuple `"c1/mado-mimetext.py", "c1/mado-mimeglob.py", "c1/mado-mimesniff.py",` + `"c1/no-such.py",` | 1 | `st-tool-pin` |
| `st-gate-target-met` | `_ST_GREEN_RC_WANT = 0` -> `1` | 1 | `st-gate-target-met` |
| `st-setup-missing-input` | `_ST_MISSING_RC_WANT = 2` -> `3` | 1 | `st-setup-missing-input` |
| `st-setup-wrong-pin` | `_ST_PINRUN_RC_WANT = 2` -> `3` | 1 | `st-setup-wrong-pin` |
| `st-setup-wrong-rev` | `_ST_BADREV_RC_WANT = 2` -> `3` | 1 | `st-setup-wrong-rev` |
| `st-target-missed-case` | `_ST_MISSED_CASE_RC_WANT = 1` -> `2` | 1 | `st-target-missed-case` |
| `st-target-missed-mutant` | `_ST_MISSED_MUT_RC_WANT = 1` -> `2` | 1 | `st-target-missed-mutant` |
| `st-result-line-format` | `_ST_LINE_RC_WANT = 0` -> `1` | 1 | `st-result-line-format` |
| `st-scratch-clean` | `os.listdir(scr) == []` -> `os.listdir(scr) == object()` | 1 | `st-scratch-clean` |

c2 — `quality/counters/c2-r96-selftest-kills.py` (green `checks=10 failed=0` rc 0):

| id | neutralised anchor | rc | fails |
|---|---|---|---|
| `st-fixture-dir` | expression edit as above | 1 | `st-fixture-dir` |
| `st-tool-pin` | pin tuple `"c2/dummy-gate.py", "c2/dummy-tool.py", "c2/kills-mini.json",` + `"c2/no-such.py",` | 1 | `st-tool-pin` |
| `st-gate-target-met` | `_ST_GREEN_RC_WANT = 0` -> `1` | 1 | `st-gate-target-met` |
| `st-setup-missing-input` | `_ST_MISSING_RC_WANT = 2` -> `3` | 1 | `st-setup-missing-input` |
| `st-setup-wrong-pin` | `_ST_PINRUN_RC_WANT = 2` -> `3` | 1 | `st-setup-wrong-pin` |
| `st-setup-wrong-rev` | `_ST_BADREV_RC_WANT = 2` -> `3` | 1 | `st-setup-wrong-rev` |
| `st-target-missed-case` | `_ST_MISSED_CASE_RC_WANT = 1` -> `2` | 1 | `st-target-missed-case` |
| `st-target-missed-mutant` | `_ST_MISSED_MUT_RC_WANT = 1` -> `2` | 1 | `st-target-missed-mutant` |
| `st-result-line-format` | `_ST_LINE_RC_WANT = 0` -> `1` | 1 | `st-result-line-format` |
| `st-scratch-clean` | `os.listdir(scr) == []` -> `os.listdir(scr) == object()` | 1 | `st-scratch-clean` |

## 4. Broken modes — 6/6 at the declared exit and line (all rc 1)

| id | counter | mode | stimulus | measured |
|---|---|---|---|---|
| `c1-missing-input` | c1 | missing-input | counter alone, `--fixture-dir <scene>/absent-fixtures` | rc 1, all 10 ids fail (`checks=10 failed=10`), first `MADO_COUNTER_SELFTEST_FAIL: st-fixture-dir`; stdout also `FIXTURES: UNRESOLVED` |
| `c1-wrong-rev` | c1 | wrong-rev | every fixture blob 0 bytes | rc 1, 9 ids fail (`checks=10 failed=9`), first `st-tool-pin` |
| `c1-mutated-tool` | c1 | mutated-tool | append the probe to `c1/mado-mimetext.py` | rc 1, exactly `st-tool-pin` |
| `c2-missing-input` | c2 | missing-input | counter alone, absent fixtures dir | rc 1, all 10 ids, first `st-fixture-dir` |
| `c2-wrong-rev` | c2 | wrong-rev | every fixture blob 0 bytes | rc 1, 9 ids (`checks=10 failed=9`), first `st-tool-pin` |
| `c2-mutated-tool` | c2 | mutated-tool | append the probe to `c2/dummy-tool.py` | rc 1, `st-tool-pin`, `st-gate-target-met`, `st-result-line-format` |

## 5. Controls

- **Do-nothing (base bytes).** `e6152b58:quality/counters/{c1-r96-magictext,c2-r96-selftest-kills}.py`
  with `--selftest` in the runner's base-control scene: rc 2, **0** `MADO_COUNTER_SELFTEST:` lines and
  0 FAIL lines (argparse usage error) — 0/2 green, as the predicate requires.
- **Always-OK echo stub.** Runner `ECHO_STUB` frozen in the panel's `stub` section
  (`runs_check: false`, `expect_flagged: 0`): rc 1, prints all 20 ids as FAIL lines, carries 0/20 find
  anchors -> credited 0.
- **No survivors.**

## 6. Findings

1. **`st-fixture-dir`'s constant edit cascades.** The owner's suggested `_ST_PINS_REL = "pins2.json"`
   rewrite flips all ten checks (fails=10), because the missing pins file starves every scene. The panel
   uses `add("st-fixture-dir", False)` instead, which isolates the one check (fails=1). If a future
   revision changes that `add(...)` statement, re-point the row.
2. **A mutated fixture tool is detected via `st-tool-pin` in the .v2 counters** (append to
   `c1/mado-mimetext.py` -> exactly `st-tool-pin`; `c2/dummy-tool.py` -> `st-tool-pin` plus two
   consequence checks). This is the w1b design the .v2 artifact implements; the older .py generation
   did not detect it.
3. **`wrong-rev` is a zero-length-fixture stimulus, not a revision stimulus** (runner contract): 9 of
   10 ids fail; `st-fixture-dir` still sees a directory and passes. The receipt should name the
   stimulus honestly.
4. **Two counter generations on disk.** The panel targets `.v2`; the L1 must land the `.v2` bytes at the
   canonical paths and reconcile the declaration's `--panel counter-selftest-panel-r97.json` naming with
   this file (`counter-selftest-panel-v2.json`), or the replay will read the stale w1 panel.
5. **Freeze churn.** The counters moved six times during the seat; this panel is anchored to
   `4f678384`/`54143b8a` and runner `abb17a01`. Any further byte change invalidates the find anchors;
   re-run the mirror and re-freeze.

## 7. Scratch

`/fast/scratch/hyaku/mado-r97/R97MMutC2b` (byte copies, layout builder, runner mirror, 20-row verifier)
was removed before yield. No tool installed; no pacman/uv transaction; no git/jj mutation anywhere.

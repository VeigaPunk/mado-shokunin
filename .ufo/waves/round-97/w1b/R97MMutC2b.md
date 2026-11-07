# R97MMutC2b — frozen C2 control panel (counter selftest neutralisations + broken modes)

Seat: mutation-tester, wave w1b, round 97. Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`,
base revision `e6152b589c2c6a28426c28263c4bcc3c46398be4`. Scratch
`$HYAKU_SCRATCH/mado-r97/R97MMutC2b` (deleted before yield). Tool installs: none.

## 1. Artifact

`controls/counter-selftest-panel-v2.json` — sha256
`95f86861d97c6bf6104095c7b7fcdf57cfdd6946dbdb34710bd6dbefc188faa8`, ASCII, 2 counters x 7
neutralisations (14 rows), 6 broken rows (3 per counter), one `stub` section (the frozen always-OK
control) and one `controls` note. Extra top-level keys are ignored by the v2 runner, which reads only
`counters` and `broken`; that was validated with the runner's own `validate_panel` (see §2).

Frozen against these exact bytes (all re-read after the final counter revision):

| input | sha256 |
|---|---|
| `quality/counters/c1-r96-magictext.py` (= `build/c1-r96-magictext-selftest.py`) | `dd9b5a0ba09dc490e286522e9d4d55d60f04dec4274bf456c0a891fa630f61d6` |
| `quality/counters/c2-r96-selftest-kills.py` (= `build/c2-r96-selftest-kills-selftest.py`) | `d4689f5a43b3bc38ef45a1eca354169cf5de4b91846bed336b8d15c0ae79f7a3` |
| runner `build/c2-r97-counter-selftest.v2.py` | `abb17a019141c57635f1c9771ad449a4348dfdc75a0bb57af3776075fe06b879` |
| fixtures `.ufo/waves/round-97/selftest-fixtures/` | 8 files (`c1-cases.json`, `c1-mutants.json`, `dummy-tool.py`, `host-list.txt`, `panel.json`, `control-kills.json`, `c2-kills.json`, `r90-argv.json`) |

**Why not `.v2.py` counter names.** The seat's 20-minute poll window expired with no
`build/c1-r96-magictext-selftest.v2.py` / `build/c2-r96-selftest-kills-selftest.v2.py` on disk; the
selftest-enabled counters are the files above. I froze against the files on disk, as the seat allows.
The counters were rewritten four times during the seat and the panel was re-anchored each time:

```
0966e34b / 96763b54   pre-review-fix (hardcoded lane literals, green-spelled could-not-evaluate)
66b4979c / dafb7a8b   review fix 1 (could-not-evaluate id; REPO from fixture dir) — c2 red in a scratch layout
cc39301e / c5aadb87   review fix 2 (absolute fixture fallback restored)
26a04021 / b843867d   fixture-only rewrite (no repo reads)
377a34fe / 861883b3   fixture-only, --fixture-dir outranks env, empty mutant/kill lists fail
3cb53f2c / 5bb32d0a   result-format now asserts the emit statement occurs exactly twice
dd9b5a0b / d4689f5a   FINAL: absolute lane fallback dropped (--fixture-dir > env > --repo > walk-up > __file__ sibling) — frozen here
```

## 2. Verification method (and its limit)

The published counting command reads the counters and the fixture tree from `git show --rev:...`, so
the v2 runner cannot be executed end-to-end before the L1 commits the wave artifacts (seats never
commit). Every row was verified with a byte-exact mirror of the runner's invocation (`verify_panel.py`,
scratch):

- layout root `<root>` with the counter at `<root>/quality/counters/<name>.py`, the fixture tree at
  `<root>/.ufo/waves/round-97/selftest-fixtures/` (8 blobs), cwd `<root>`, env
  `PATH=/usr/bin:/bin HOME=<root> TMPDIR=<root> LC_ALL=C.UTF-8`, `MADO_SELFTEST_REPO=<root>`;
- green legs: `python3 -I <counter> --selftest --fixture-dir <root>/.ufo/waves/round-97/selftest-fixtures`;
- neutralisations: `find` counted in the counter bytes (must be exactly 1), replaced once, counter bytes
  rewritten in place, rerun identically, original bytes restored;
- broken rows: missing-input = counter alone in a scene with `--fixture-dir <scene>/absent-fixtures`;
  wrong-rev = a scene fixture tree with every blob truncated to 0 bytes; mutated-tool = the scene tree
  with `\n# mutated-tool probe\n` appended to the row's `path`; each run with that tree as
  `--fixture-dir` (the runner's current shape routes all invocations through `--fixture-dir` siblings
  inside the layout root; the counter only sees the tree contents, so the mirror is equivalent);
- panel shape validated by importing the runner's `validate_panel(panel, 6, setup)`: `OK`, no setup
  message;
- the always-OK control is the runner's `ECHO_STUB` verbatim (prints every panel id as a
  `MADO_COUNTER_SELFTEST_FAIL:` line at rc 1 without running a check), frozen in the panel's `stub`
  section. The runner's credit rule needs the judged bytes to carry the row's `find` anchor exactly
  once; the stub carries 0/14 anchors, so `always_ok_flagged=0` (measured on the stub bytes, not
  asserted).

Full run against the frozen bytes: `KILLED_ONLY=14/14`, `SURVIVED=0`, `BAD_FIND=0`, `OTHER=0`,
`stub flagged=True=0/14`, broken rows `6/6`. Tail:

```
  C2-fixture-parses: rc=1 fails=['C2-fixture-parses'] res=[('7','1')] -> KILLED_ONLY
  broken c1-missing-input  rc=2 want=2 line_ok=True ok=True fails=['C1-fixture-could-not-evaluate']
  broken c1-wrong-rev      rc=1 want=1 line_ok=True ok=True fails=['C1-green-target-met','C1-mutant-mismatch','C1-fixture-parses']
  broken c1-mutated-fixture rc=1 want=1 line_ok=True ok=True fails=['C1-mutant-mismatch','C1-fixture-parses']
  broken c2-missing-input  rc=2 want=2 line_ok=True ok=True fails=['C2-fixture-could-not-evaluate']
  broken c2-wrong-rev      rc=1 want=1 line_ok=True ok=True fails=['C2-green-target-met','C2-mutant-mismatch','C2-fixture-parses']
  broken c2-mutated-fixture rc=1 want=1 line_ok=True ok=True fails=['C2-mutant-mismatch','C2-fixture-parses']
```

## 3. Neutralisations — 14/14 `KILLED_ONLY`, 0 survivors

Every row: rc 1, result line `MADO_COUNTER_SELFTEST: checks=7 failed=1`, and the only
`MADO_COUNTER_SELFTEST_FAIL:` line is the declared id. No row needed the "checks are not independent"
allowance.

c1 — `quality/counters/c1-r96-magictext.py` (green baseline `checks=7 failed=0` rc 0):

| id (= printed FAIL token) | neutralised site | rc | fails |
|---|---|---|---|
| `C1-green-target-met` | `check_green_target_met` final `return bool(line_ok and find_ok)` -> `return False` | 1 | `C1-green-target-met` |
| `C1-missing-cases` | `check_missing_cases` final `return rc == 2 and "SETUP_ERROR" in out and "MADO_MAGICTEXT_COUNT:" in out` -> `return False` | 1 | `C1-missing-cases` |
| `C1-wrong-rev-pin` | `check_wrong_rev` final `return rc == 2 and "SETUP_ERROR" in out` (newline-terminated, unique) -> `return False` | 1 | `C1-wrong-rev-pin` |
| `C1-mutant-mismatch` | `check_mutant_mismatch` loop tail `if broken == tool_src: return False` + final `return True` -> `return False` | 1 | `C1-mutant-mismatch` |
| `C1-result-format` | emit-site mutation: the selftest result `print("MADO_COUNTER_SELFTEST: checks=%d failed=%d" ...)` renamed to `MADO_COUNTER_SELFTEST_X`, so `src.count(needle)` drops 2->1 and the check fails (this is the exact production defect the check was strengthened to catch) | 1 | `C1-result-format` (no result line: the emit was mutated) |
| `C1-no-scratch-left` | `check_no_scratch_left` final `return not any(n.startswith("c1r96-") or n.startswith("c1-selftest-") ...)` -> `return False` | 1 | `C1-no-scratch-left` |
| `C1-fixture-parses` | `check_fixture_parses` `_js.loads(open(MUTANTS...))` + final `return True` -> `return False` | 1 | `C1-fixture-parses` |

c2 — `quality/counters/c2-r96-selftest-kills.py` (green baseline `checks=7 failed=0` rc 0):

| id (= printed FAIL token) | neutralised site | rc | fails |
|---|---|---|---|
| `C2-green-target-met` | `check_green_target_met` final `return bool(shape and kshape)` -> `return False` | 1 | `C2-green-target-met` |
| `C2-missing-panel` | `check_missing_panel` final `return rc == 2 and "SETUP_ERROR" in out and "MADO_SELFTEST_KILLS:" in out` -> `return False` | 1 | `C2-missing-panel` |
| `C2-wrong-rev-pin` | `check_wrong_rev` final `return rc == 2 and "SETUP_ERROR" in out` -> `return False` | 1 | `C2-wrong-rev-pin` |
| `C2-mutant-mismatch` | `check_mutant_mismatch` loop tail `if broken == tool_src: return False` + final `return True` -> `return False` | 1 | `C2-mutant-mismatch` |
| `C2-result-format` | same emit-site mutation (result print renamed), `src.count(needle)` 2->1 | 1 | `C2-result-format` (no result line: the emit was mutated) |
| `C2-no-scratch-left` | `check_no_scratch_left` final `return not any(n.startswith("c2r96-") or n.startswith("c2-selftest-") ...)` -> `return False` | 1 | `C2-no-scratch-left` |
| `C2-fixture-parses` | `check_fixture_parses` `_js.loads(open(R90...))` + final `return True` -> `return False` | 1 | `C2-fixture-parses` |

## 4. Broken modes — 6/6 at the declared exit and line

| id | counter | mode | stimulus | measured |
|---|---|---|---|---|
| `c1-missing-input` | c1 | missing-input | counter alone, `--fixture-dir <scene>/absent-fixtures` | rc 2, `MADO_COUNTER_SELFTEST_FAIL: C1-fixture-could-not-evaluate` + `checks=0 failed=1` |
| `c1-wrong-rev` | c1 | wrong-rev | every fixture blob 0 bytes | rc 1, fails `C1-green-target-met`, `C1-mutant-mismatch`, `C1-fixture-parses`; declared line `...C1-green-target-met` |
| `c1-mutated-fixture` | c1 | mutated-tool | append the probe to `c1-mutants.json` | rc 1, fails `C1-mutant-mismatch`, `C1-fixture-parses`; declared line `...C1-mutant-mismatch` |
| `c2-missing-input` | c2 | missing-input | counter alone, absent fixtures dir | rc 2, `MADO_COUNTER_SELFTEST_FAIL: C2-fixture-could-not-evaluate` + `checks=0 failed=1` |
| `c2-wrong-rev` | c2 | wrong-rev | every fixture blob 0 bytes | rc 1, fails `C2-green-target-met`, `C2-mutant-mismatch`, `C2-fixture-parses`; declared line `...C2-green-target-met` |
| `c2-mutated-fixture` | c2 | mutated-tool | append the probe to `c2-kills.json` | rc 1, fails `C2-mutant-mismatch`, `C2-fixture-parses`; declared line `...C2-mutant-mismatch` |

## 5. Controls

- **Do-nothing (base bytes).** `e6152b58:quality/counters/{c1-r96-magictext,c2-r96-selftest-kills}.py`
  with `--selftest` in the runner's base-control scene: rc 2, **0** `MADO_COUNTER_SELFTEST:` lines and
  0 FAIL lines (argparse usage error). The base-control leg counts 0/2 green, as the predicate requires.
- **Always-OK echo stub.** Runner `ECHO_STUB` frozen in the panel's `stub` section (`runs_check: false`,
  `expect_flagged: 0`): prints every panel id as a FAIL line at rc 1. Credit needs the row's anchor in
  the stub bytes — 0/14, so `always_ok_flagged=0`. The weaker plain-green stub (prints only
  `checks=6 failed=0`) was also `flagged=False` on all 14 runs.
- **No survivors.**

## 6. Findings (falsifiers this seat measured)

1. **[FINDING, resolved] c2's earlier revision needed the runner's support tree.** Against the
   pre-fixture-only c2 revision (`dafb7a8b`), running only counters+fixtures in a scratch layout made
   `--selftest` `checks=7 failed=4` (`C2-green-target-met`, `C2-missing-panel`, `C2-wrong-rev-pin`,
   `C2-mutant-mismatch`) because its checks opened `REPO/quality/check-selftest-strength.py` and
   `REPO/quality/check-receipt-presence.py`. Reported to both owners; the final revision (`861883b3`)
   is fixture-only and green in the bare layout, and the runner also materialises the support tree, so
   the dependency is gone in both directions. Verified green with and without the support tree.
2. **[FINDING, owner-confirmed by design] A mutated dummy tool is not detected.** Appending
   `\n# mutated-tool probe\n` to `dummy-tool.py` leaves **both** final counters at `checks=7 failed=0`
   rc 0 (re-measured on `377a34fe`/`861883b3`). R97MExecC2 confirms this is intentional: `dummy-tool.py`
   is a shape placeholder, not a scored artifact, and mutated-tool coverage lives in
   `C1-mutant-mismatch` / `C2-mutant-mismatch`, which apply each fixture's find/replace to the dummy
   source and require the anchor consumed exactly once (an empty list fails). The panel's mutated-tool
   rows therefore target a fixture the counter actually parses (`c1-mutants.json`, `c2-kills.json`) and
   declare the mutant-check id; if a fixture pin manifest is added later, both rows are the right
   re-point targets.
3. **[FINDING] The neutralisations target the checks' own predicates, not production mutations.** Six of
   the seven checks per counter are self-referential or trivially true (`return bool(pattern)`, a
   fixture-shape read, a leftover-dir scan); only `C1-missing-cases`, `C1-wrong-rev-pin`,
   `C2-missing-panel`, `C2-wrong-rev-pin` drive the production counter, and they do so with `--repo .`
   from a non-repo cwd (they assert the resulting `SETUP_ERROR`). A production edit that flips a shared
   path flips several checks (truncating the tree flips 3), so per-check isolation is only achievable
   through the check bodies. The receipt must say the panel proves the harness attributes a failure to
   the declared id; it does **not** prove the checks bite a broken counter (R97MReviewC2b R6.4).
4. **[FINDING] `missing-input` is a `could-not-evaluate` id at rc 2, not `SETUP_ERROR`:**
   `MADO_COUNTER_SELFTEST_FAIL: <C1|C2>-fixture-could-not-evaluate` + `checks=0 failed=1`. Declared as
   measured; the runner's broken check is `rc == expect_exit and expect_line in output`.
5. **[RISK] Freeze churn.** The counters were rewritten five times during the seat; this panel is
   anchored to `dd9b5a0b`/`d4689f5a` and the runner `abb17a01` (owner states no further edits planned).
   Any further rewrite of either counter invalidates all 14 `find` anchors — re-run the scratch verifier
   and re-freeze before landing.

## 7. Scratch

`/fast/scratch/hyaku/mado-r97/R97MMutC2b` held the byte copies, the layout builder, the runner mirror
and a toy self-test of the harness; it was removed before yield. No tool installed; no pacman/uv
transaction; no git/jj mutation anywhere (the single fixture repo used for a green-path probe was
`git init`-ed in scratch, `git rev-parse --show-toplevel` asserted, and never committed).

# R93MMutC2 — mutation probe of the C2 gate (check-selftest-strength)

Seat: R93MMutC2 (mutation-tester, leaf member — no dispatch). Wave: round-93 w1.
Scratch: `$S = /fast/scratch/hyaku/mado-r93/R93MMutC2` (deleted on exit, §11).
Every run below is a **DRAFT** run (round-93 scoring has not frozen); no receipt was written.

## 0. Objects and pins

| object | path | sha256 |
|---|---|---|
| gate under test | `.ufo/waves/round-93/build/check-selftest-strength.c2.py` | `76a1d9235b27a9c1e9b348a5ad77fb22d34d1ce6a5c4c9a8c06d0f203207e6e1` |
| kill-set (owner R93MExecGateC2) | `.ufo/waves/round-93/build/check-seat-reports-kills.c2.json` | `ac9e464810c5c3ab4b6d44317b989d4734049d332dd0a7d84de416d60c6b3192` (20 kills) |
| mutated selftest target | `quality/check-seat-reports.py` | `176fc066b49334921e4fd746de55db8106709c29dfe225430224c9d46ed1663a` (= the kill-set's `tool_sha256`) |
| gate's own selftest | `python3 build/check-selftest-strength.c2.py --selftest` | rc 0, `SELFTEST_STRENGTH_SELFTEST: checks=8 failed=0` (DRAFT) |

Both pinned hashes were re-read after every measurement run and were unchanged (last check: gate `76a1d923…`, kill-set `ac9e4648…`). The gate appeared at 00:14 and was still being edited (sha `97cf3375…` → `76a1d923…`); I waited for three consecutive identical hashes before pinning a copy at `$S/pin/gate.py`.

## 1. Deliverable

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-93/controls/selftest-gate-mutants-r93.json` — **19 gate mutants** `{id, what, file, find, replace}`, every `find` verified to occur **exactly once** in the gate file (`results.json: occurrences == {}`, i.e. no mutant was skipped). They cover the briefed families: ignore exit code (G01), ignore `must_fail` (G02), accept any FAIL line (G02/G13), skip the positive control (G04/G15), timeout as killed (G05), `wrong_check` as held (G03/G06), verdict OK when survived>0 (G07/G18), sha check removed (G08/G17), first-kill-only (G10), `>=` for `==` (G09), `any`→`all` (G14), rc forced 0 (G19), find-occurrence check dropped (G16), result-line guard dropped (G12).

## 2. Method (probe panel and verdict rule)

Each gate copy is run as DRAFT with
`python3 GATE --tool <tool> --kills <kill-set> --scratch-root $S/runs --timeout N [--allow-sha-drift]`
and classified by `(rc, KIND)` from its last `SELFTEST_STRENGTH:` line. A mutant is **KILLED** when its `(rc, KIND)` differs from the unmutated gate's on **any** of the six required scenarios; extension probes are reported separately and never decide the verdict.

Required six (the item's panel):
* `positive` — real tool + the real kill-set, no flag;
* `N1-f3-nodedup`, `N2-f2-no-want-in`, `N3-sr03-abs` — three single-check neutralisations of `quality/check-seat-reports.py`'s selftest (each keeps `checks=23 failed=0`);
* `H1-drop-ids`, `H2-drop-want-in` — two hand weakenings (global conjunct removals), also green.

Extension probes (mine, added to reach the gate's other arms): `sha-guard` (drifted tool, no `--allow-sha-drift`), `broken-tool` (production defect that makes the unmutated selftest fail), `N4-wt-symlink`, `N5-sr01-two-task`, `N6-unsafe-rel` (further single-check neutralisations), `wrong-check` (synthetic 1-kill set whose mutant fails a *different* label), `no-failed0` / `rc1-failed0` (result line / exit code out of sync), `timeout-kill` (a kill whose mutant sleeps 600 s, gate `--timeout 3`), `ambiguous-find` (a kill whose `find` occurs 2×), `fail-line-exit-0` (a kill whose mutant prints a FAIL line yet exits 0).

Exact find/replace for the six required scenarios: `w1/R93MMutC2-scenarios.json`. Panel results: `w1/R93MMutC2-baseline.json`, `w1/R93MMutC2-results.json`.

Each neutralisation and hand weakening was first shown to be a **real** weakening: for every one there is a production defect that the pristine selftest kills (`failed>0`) and the weakened selftest passes (`failed=0`):

| scenario | survivor defect (find → replace, production code) | pristine | weakened |
|---|---|---|---|
| N1 | `rounds = sorted(set(rounds))` → `rounds = sorted(rounds)` | `failed=1` | `failed=0` |
| N2 | `tok()` `…replace(" ", "\\u0020")` dropped | `failed=1` | `failed=0` |
| N3 | `unsafe()` loses the absolute-path test | `failed=1` | `failed=0` |
| H1 | SR01 label mistyped to SR09 | `failed=7` | `failed=0` |
| H2 | worktree symlink-dispatch message loses "is a symlink" | `failed=1` | `failed=0` |

## 3. Baseline (unmutated gate, DRAFT, all 16 probes)

| probe | rc | kind | summary |
|---|---|---|---|
| positive | 0 | OK | kills=20 held=20 survived=0 wrong_check=0 |
| N1-f3-nodedup | 1 | WEAK | held=19 survived=1 |
| **N2-f2-no-want-in** | **0** | **OK** | **held=20 survived=0** ← escape, §6 |
| N3-sr03-abs | 1 | WEAK | held=19 survived=1 |
| H1-drop-ids | 1 | WEAK | held=14 survived=6 |
| H2-drop-want-in | 1 | WEAK | held=18 survived=2 |
| sha-guard | 2 | SETUP_ERROR | tool sha256 mismatch |
| broken-tool | 2 | SETUP_ERROR | unmutated selftest rc=1 fails=[…] |
| N4-wt-symlink / N5 / N6 | 1 | WEAK | survived=1 each |
| wrong-check | 1 | WEAK | kills=1 held=0 survived=0 wrong_check=1 |
| no-failed0 | 2 | SETUP_ERROR | result line lacks failed=0 |
| rc1-failed0 | 2 | SETUP_ERROR | unmutated selftest rc=1 fails=[] |
| timeout-kill | 1 | WEAK | kills=1 survived=1 |
| ambiguous-find | 2 | SETUP_ERROR | kill a1 find occurs 2 times |
| fail-line-exit-0 | 1 | WEAK | kills=1 survived=1 |

The gate behaves on this material: positive OK, all real weakenings WEAK, all setup faults rc 2.

## 4. Mutant verdicts (19 mutants, DRAFT)

| id | required panel | probes whose verdict differs (required / extension) |
|---|---|---|
| G01-rc-ignored | SURVIVED | — / fail-line-exit-0 |
| G02-must-fail-ignored | SURVIVED | — / wrong-check |
| G03-wrong-check-as-held | SURVIVED | — / wrong-check |
| G04-positive-control-skipped | SURVIVED | — / broken-tool, no-failed0, rc1-failed0 |
| G05-timeout-as-held | SURVIVED | — / timeout-kill |
| G06-wrong-excluded-from-verdict | SURVIVED | — / wrong-check |
| G07-survived-ignored | **KILLED** | N1, N3, H1, H2 |
| G08-sha-guard-removed | SURVIVED | — / sha-guard |
| G09-rc-nonnegative-accepted | **KILLED** | positive, N2 |
| G10-first-kill-only | **KILLED** | N1, H2 |
| G11-survived-not-counted | **KILLED** | N1, N3, H1, H2 |
| G12-result-line-unchecked | SURVIVED | — / no-failed0 |
| G13-fail-prefix-anywhere | SURVIVED | — / — |
| G14-any-to-all | **KILLED** | N1, N3, H1, H2 |
| G15-positive-rc-nonfatal | SURVIVED | — / rc1-failed0 |
| G16-find-occurrence-check-dropped | SURVIVED | — / ambiguous-find |
| G17-sha-mismatch-nonfatal | SURVIVED | — / sha-guard |
| G18-survived-as-held | **KILLED** | N1, N3, H1, H2 |
| G19-rc-always-zero | **KILLED** | N1, N3, H1, H2 |

Tally: **7/19 killed by the required six-scenario panel**, **11 more killed by the extension probes**, **1 survivor everywhere** (G13).

### Survivors and their reasons
* **G13-fail-prefix-anywhere** (`ln.startswith(fail_prefix)` → `fail_prefix in ln`) — equivalent in practice: the tool prints the prefix only at column 0, and no kill can reach into the selftest to change that. The mutant is behaviourally identical on every tool this gate will ever see; it is not a predicate gap.
* The other 11 are **panel gaps, not gate defects**: the required six scenarios only exercise the "kill mutant survives → WEAK" arm. They never present a drifted sha, a WRONG_CHECK, a broken/violently-exiting tool, a hanging mutant, an ambiguous `find`, or a FAIL line next to rc 0, so the corresponding predicates (gate lines 103, 136, 139, 149, 160, 163) are never forced. Each was killed the moment such a probe existed.

## 5. Recommendation to the gate's owner (predicate is sound; the *panel* is thin)

If the counter R93MExecCounterC2 is to call the gate strong, its fixture set needs the arms the required six do not reach. Minimum additions, each already materialised here and each cheap (≤3 s): a drifted-tool sha probe, an unmutated-selftest-fails probe, a WRONG_CHECK probe, an ambiguous-`find` probe, and a per-kill timeout probe. Without them, G02/G03/G04/G05/G06/G08/G12/G15/G16/G17 are all undetectable while being exactly the fail-open directions the gate exists to prevent.

## 6. Escapes — weakenings that keep `checks=23 failed=0` and that the gate does **not** flag

Six escapes were constructed and each proved to be a genuine weakening: a production defect that the pristine selftest kills survives under the weakened selftest, while the gate still prints `SELFTEST_STRENGTH: OK` rc 0 on it. Adding that defect to the kill-set makes the same gate flag the escape (`WEAK` rc 1) — so the escapes are **kill-set coverage gaps**, not predicate bugs. Evidence: `w1/R93MMutC2-escapes.json`.

1. **N2-f2-no-want-in** (also required scenario #2). Find `want_in='"A\\u0020b\\nc"')` → replace `want_in="")`. Gate: `OK held=20` rc 0. Survivor defect: drop `tok()`'s `.replace(" ", "\\u0020")` (pristine `failed=1`, weakened `failed=0`). Cause: kill `k-tok-ascii` replaces only the ASCII *predicate*, so the `all(g.isascii())` conjunct still kills it; nothing in the kill-set emits an ASCII-but-unexpanded token.
2. **E1-set-superset**: `ok = rc == want_rc and ids == want_ids and (rc == 2 or` → `ok = rc == want_rc and set(ids) >= set(want_ids) and (rc == 2 or`. Survivor: an extra bogus `SR04` line per run (pristine `failed=3+`, weakened 0).
3. **E2-rc-off-by-one**: `ok = rc == want_rc and ids == want_ids` → `ok = rc in (want_rc, want_rc + 1) and ids == want_ids`. Survivor: `run()` ends `return 1` (pristine kills *all present* and *rev: present*; weakened 0).
4. **E3-mode-token**: the summary assertion `got[-1].startswith(f"SEAT_REPORTS: mode={mode}")` → `"SEAT_REPORTS: mode=" in got[-1]`. Survivor: summary always prints `mode=rev` (pristine fails several cases; weakened 0).
5. **E4-ascii-first-line-only**: `all(g.isascii() for g in got)` → `all(g.isascii() for g in got[:1])`. Survivor: a non-ASCII line appended to `lines` (pristine `failed=15`, weakened 0).
6. **E5-substring-case**: `any(want_in in g for g in got)` → `any(want_in.lower() in g.lower() for g in got)`. Survivor: the worktree message uppercased to `DISPATCH IS A SYMLINK` (pristine `failed=1`, weakened 0).

One more escape is benign and worth recording: **E8-first-fail-only** (`for n in failed:` → `for n in failed[:1]:`) keeps 23/0 and the gate OK, but it cannot hide a kill because a label mismatch is already `WRONG_CHECK` → WEAK. It only hides secondary labels from a human reader.

**Structural finding**: the selftest has 23 checks and 5 assertion conjuncts; the kill-set has 20 entries, all of which kill through `rc` + a label. Nothing in the kill-set reaches the *pass-predicate shape* (id equality, exact rc, mode token, ASCII scope, substring case, label multiplicity), so any weakening that keeps every kill's observable failure intact is invisible. A gate of this design can only be as strong as its kill-set; the honest claim is "no weaker than the kill-set", not "no weaker than the selftest".

## 7. Cross-check of the gate's own selftest (DRAFT)

`python3 .ufo/waves/round-93/build/check-selftest-strength.c2.py --selftest` → rc 0, `checks=8 failed=0`. Its cases cover OK / SURVIVED / WRONG_CHECK / sha-mismatch (both flag states) / find-twice / find-inside-selftest / unmutated-fails. All pass.

## 8. Commands run (all DRAFT; exit status shown)

| command | rc |
|---|---|
| `python3 quality/check-seat-reports.py --selftest` (baseline, TMPDIR=$S) | 0 (`checks=23 failed=0`) |
| `python3 build/check-selftest-strength.c2.py --selftest` | 0 (`checks=8 failed=0`) |
| `python3 $S/baseline.py` (16 probes, unmutated gate) | 0 |
| `python3 $S/driver.py controls/selftest-gate-mutants-r93.json` (19 mutants × 16 probes) | 0 |
| `python3 $S/escape.py` (8 assertion-shape weakenings) | 0 |
| `python3 $S/escapes_demo.py` + final consolidation (6 escapes × defect × wider kill-set) | 0 |

No install was needed and none was made. No `pacman` transaction, no `git`/`jj` mutation (the only repositories touched were throwaway fixture repos created by `check-seat-reports.py`'s own selftest under `TMPDIR=$S`, each verified by its `rev-parse --show-toplevel` guard).

## 9. Dead steps / errors

1. First `mk_scenarios.py` version produced neutralisations (SR01/SR02 fixture swaps) that this kill-set still kills — they were not *escapes*. Rebuilt around unique coverage (F3 dedup, F2 `want_in`, absolute-trailer SR03); the discarded pairs are in no file.
2. Gate sha changed under me twice (`97cf3375…`, then `76a1d923…`); all early reads discarded, probing started only after three identical hashes 30 s apart.
3. First escape-demo defect for **E2** used `raise SystemExit(2)` inside `unsafe()`; it exits the whole process (no FAIL lines) and so did not demonstrate survival. Replaced with `run()` returning 1 permanently.
4. First **E4** defect appended the non-ASCII line such that it became `got[0]` for cases with no SR lines, so the weakened selftest still failed; changed to `if lines:` so the line only appears in multi-line outputs.
5. First **E5** defect string occurred twice in the tool (both symlink messages), which the gate correctly rejects (rc 2, "find occurs 2 times"); re-anchored with the following `if not self.inside(path):` line to make it unique.

## 10. Restoration / cleanliness

The lane's gate and kill-set were only ever read and copied (`cp` into `$S/pin`); the lane copies keep their pinned hashes (re-verified after the last run). All mutant copies, scenario copies and fixtures lived under `$S`; the scratch tree is deleted on exit (§11) after the four evidence files were copied to `w1/`.

## 11. Files written by this seat

* `mado-shokunin/.ufo/waves/round-93/controls/selftest-gate-mutants-r93.json` (19 mutants, mine)
* `mado-shokunin/.ufo/waves/round-93/w1/R93MMutC2.md` (this report)
* `mado-shokunin/.ufo/waves/round-93/w1/R93MMutC2-results.json` (per-mutant verdicts + diffs)
* `mado-shokunin/.ufo/waves/round-93/w1/R93MMutC2-baseline.json` (16-probe baseline)
* `mado-shokunin/.ufo/waves/round-93/w1/R93MMutC2-scenarios.json` (the six required find/replace pairs + extensions)
* `mado-shokunin/.ufo/waves/round-93/w1/R93MMutC2-escapes.json` (six escapes with survivor defects and wider-kill re-runs)

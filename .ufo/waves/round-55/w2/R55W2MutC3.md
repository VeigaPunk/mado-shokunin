# R55W2MutC3 — mutation test of the C3 counter and its harness (round 55, wave w2)

Seat: R55W2MutC3 (leaf member, no subagents). Lane revision attacked: `57584ed67716340b3d466fa04333ac0bab3fb79e`.
Full per-mutant table, edits and proposal matrix: `.ufo/waves/round-55/w2/R55W2MutC3/mutants.md`. Mutant files: `.ufo/waves/round-55/w2/R55W2MutC3/mutants/`. Receipts: `.ufo/waves/round-55/w2/R55W2MutC3/receipts/`.

## What was attacked

1. `quality/counters/c3-r55-p19.py` (counter): 38 one-line mutants (C01–C38) plus two targeted counters (T01, T02).
2. `quality/r55_ctl_c3.py` (harness, run via `quality/check-r55-controls.py --claim c3`): 6 harness mutants (H01–H06), each run against the always-green stub and against the counter it has to admit.
3. Text-proposed kill tests for every survivor, built as real ctl commits and run on the unchanged counter and the survivor (V1–V7).

Method: copies only, in `/fast/scratch/hyaku/mado-r55/R55W2MutC3/` (removed before yield). Lane access was read-only: `git archive 57584ed`, `git fetch` from the lane into a scratch repo (objects only), `cat-file`/`show`/`rev-parse`. No lane file, ref or commit was written; no commit, reset, stash or checkout ran against the lane or fleet repo. Scratch repo `R`: `git init`, toplevel asserted; tree = archive of `57584ed` (hash `feecf8d8…`, equals the lane tree); good commit `1f484da6285b5f38848945bc1c1d60d9e3383726`, `-c user.name=ctl -c user.email=ctl@ctl`, parent = base `3b55b6e` (the instrument hard-codes that base object, so the repo must carry it).

Baseline on the unchanged pair: counter selftest `41/41 passed`; harness `good=ok controls=6/6 verdict=OK`; always-green stub against the unchanged harness `controls=0/6 verdict=FAIL`.

## Results per target

| target | verdict | evidence |
|---|---|---|
| Counter legs as a set (prefix, rows Q01–Q13, rows:heading, pin, p23, stale, readme, tables_sha) | SURVIVES in part: 8 survivors, 2 equivalents, 28 killed | mutants.md §1; C09, C11, C13, C14, C15, C17, C31, C37 pass both selftest and harness; C10, C29 equivalent |
| `stale` only-when leg (C09 case-sensitive, C37 leg removed) | SURVIVES | selftest 41/41 and harness 6/6 with the mutant; the only control (CTL-5) uses the verbatim P19 sentence, which leg 2 catches without leg 1. Proposal V1 (prose `Only when …` line) → C09 MET, C37 MET, unchanged MISSED `stale` (receipts/verify.json) |
| P23 token list (RELEASED, `== 1`, `m_passPressed`) | SURVIVES | C11, C13, C14 each 41/41 and 6/6. V2/V3/V4 (one token altered in the P23 row) → each mutant MET, unchanged MISSED `p23` |
| P23 `else` alt word (C15) | SURVIVES | 41/41, 6/6. V5 (`any other value` → `remaining value`, `else` kept): unchanged MET, C15 MISSED `p23` |
| P23 Pin:anchor cell (C17) | SURVIVES | 41/41, 6/6 with the check removed. V6 (`1554-1576` → `1554-1558`): unchanged MISSED `p23`, C17 MET |
| Heading ATX requirement (C31) | SURVIVES | 41/41, 6/6. V7 (`## Correction …` → plain line): unchanged MISSED `rows:heading`, C31 MET |
| Unchanged counter on V1–V7 (frozen row grammar, parser-compatible) | NOT-REPRODUCED | every V input gets the expected verdict from the unchanged instrument; the gaps are in the controls, not in the instrument's verdicts |
| Independent harness coverage | BROKEN as an independent guard: it kills 14 of 38 counter mutants; 14 more are killed only by the counter's own selftest (C03, C04, C08, C12, C18, C19, C20, C24, C25, C26, C28, C32, C35, C36), which the same author wrote | mutants.md §6 |
| Harness control count (H01 skip CTL-5, H05 skip CTL-6, H06 `passed >= 0`) | SURVIVES | `ok = good == "ok" and passed == len(CONTROLS)` with a literal `6` printed. H01 vs C06 (stale dropped): `controls=5/6 verdict=OK` (unmodified harness on the same counter: `5/6 verdict=FAIL`). H05 vs C07 (readme dropped): `controls=5/6 verdict=OK`. H06 vs always-green stub: `controls=0/6 verdict=OK`; the unmodified harness prints FAIL for that stub |
| Harness collateral legs (H03 allows `stale` in CTL-6) | SURVIVES | T02 (`stale` over-reported when the readme leg fails, fields consistent): H03 `controls=6/6 verdict=OK`; unmodified harness `5/6 verdict=FAIL` (`unexpected leg(s) ['stale']`). Note: `pin` and `p23` over-reports are caught by the field check (their fields are pinned), so only unpinned legs can be widened |
| CTL-5 required-stale weakening (H02) | EQUIVALENT | CTL-5 allows `{stale}` and no rows; a non-empty `missed=` forces `{stale}`. T01 (stale reported as `rows:heading`) still FAILs under H02 |
| Admission check (H04) | EQUIVALENT | every control has a non-empty must-set, so a MET verdict already fails |
| Counter selftest vs BASE constant (C21) | killed by the harness only; the selftest passes 41/41 with the mutant | the selftest calls `evaluate(..., base_commit=base)` in-process and never reads `BASE` |
| Tree-only repository (no base object) | reproduced: cannot run | `MADO_P19_FIX: SETUP base_commit_absent`; `MADO_R55_CONTROLS: SETUP base_entry_unreadable` (receipts/R6-exported-tree-only.txt). The harness needs the base commit object at `--repo` |

## Survivor kill tests (text proposals, checked on the unchanged counter and the survivor)

- CTL-5b: append a prose `Only when …` line outside any table, P23 otherwise correct (expect `missed=stale`). Kills C09, C37.
- CTL-7a–c: one P23-row token altered (`RELEASED`→`released`, `== 1`→`is 1`, `m_passPressed`→`passPressed`; expect `missed=p23`). Kills C11, C13, C14.
- CTL-7d: remove `any other value` from the P23 row, keep `else` (expect MET). Kills C15.
- CTL-7e: P23 Pin:anchor `…:1554-1576` → `…:1554-1558` (expect `missed=p23`). Kills C17.
- CTL-8: heading line without `#` (expect `missed=rows:heading`). Kills C31.
- Harness: assert `len(CONTROLS) == 6` (or compare `passed` to the literal 6). Kills H01, H05, H06.
- Harness: a CTL-6 over-report of `stale` expecting FAIL (= T02). Kills H03.
- Independent controls for the 14 selftest-only legs listed above (pin byte change, tables change, second P23 row, CRLF after prefix, duplicated Q row, Q anchor change, P23 Supersedes/source change, fenced Q row, `== 0` token). Not run in full; listed in mutants.md §3.

## Not verified / limits

- Counter entailment (does each P19/P23 sentence follow from its pinned quote) is out of scope; these attacks test presence and shape only.
- The harness is not adversarial by declaration (registration v2 E9); the findings above are against a non-adversarial mutant set.
- Equivalence claims C10, C29, H02, H04 rest on the argument stated in mutants.md §5 plus the observed runs. The C10 argument relies on the frozen P19 sentence containing `only when`.
- The 14 independent-control proposals in §3 are text only, not executed.
- Targeted counters T01/T02 are my constructions to test the harness's allow-sets; they are not claims about any shipped code.
- Not run: the C1 and C2 harnesses (out of seat scope); the lane's own working tree was not used as the repo (scratch copy of the same tree).

## Host and tooling

- No host configuration or compositor was touched (no `hyprctl`, no config reads). No network access. No tool installed or upgraded; the work used the Python 3 standard library and `git` only. Nothing under `~/.local/bin` or other PATH directories was written.
- Scratch `/fast/scratch/hyaku/mado-r55/R55W2MutC3/` removed before yield; copies of drivers, logs, summaries and unchanged instrument/harness are in `receipts/`.

# R55W2CritFreezeFool — report (round 55, wave w2, falsify)

Full evidence: `.ufo/waves/round-55/w2/R55W2CritFreezeFool/fool.md`. Raw transcript: `.ufo/waves/round-55/w2/R55W2CritFreezeFool/receipts-run.txt`.
Lane tip `721ba9c1`; scored revision `57584ed6`. Checker `quality/check-freeze-order.py` (sha256 `83d9eb2a…4474`), read-only; copy in w1 differs only by the docstring.

## What I attacked
1. The five named fooling cases from `R55CritChronology` (S2, S3, S4, S7, S8), reproduced on fresh fixtures, plus S1 control and S5/S5b.
2. The checker on the committed objects of rounds 52 (w1, w2), 53 (w1), 54 (w1, w2), 55 (w1, w2) at tip, plus 55 w1 at the scored revision and at two non-tip commits.
3. Round 55 hand derivation from `git log`, the dispatch marker (content and mtime) and the registries.
4. New scope gaps: deleted optional freeze file after launch; post-launch edit of `registration-v2.md` / `frozen-tables-v2.json` (binding for w2); registry `createdAt` rewritten after launch.

## Verdicts

| target | verdict | evidence (fool.md §) |
|---|---|---|
| S1 control, S5, S5b | SURVIVES (control holds; fail closed) | §1 |
| S3 backdated committer → OK | BROKEN, **disclosed** (declared) | §1, §6 |
| S7 post-launch edit then revert → OK | BROKEN, **disclosed** (declared) | §1, §6 |
| S4 forged later createdAt → OK | BROKEN, **disclosed only by implication**: the declared limit says "plan time" but never says a later value passes; the registry's own commit time (12:05Z vs createdAt 13:00Z) would refute it and is not compared | §1, §6 |
| S2 rebase after launch → FAIL; S8 reword → FAIL | NOT-REPRODUCED as a fooling (conservative false FAIL); **disclosed** (declared "rebased freeze ... can read FAIL") | §1 |
| N1 optional `frozen-tables.json` deleted after launch → OK (synthetic and lane branch) | BROKEN, **undisclosed** | §2 |
| N3 post-launch edit of `registration-v2.md` / `frozen-tables-v2.json` → OK (w2 binds v2) | BROKEN, **undisclosed scope gap** | §2 |
| N2/N4 registry `createdAt` rewritten after launch → OK (reads tip only) | BROKEN, mechanism **undisclosed** (class = S4) | §2 |
| Round 55 w1 at tip → OK; matches hand derivation | SURVIVES (with the declared "unwitnessed launch" caveat) | §3, §4 |
| Round 55 w2 at tip → OK; matches hand derivation | SURVIVES; v2 precedes w2 launch by hand but is never checked | §3, §4 |
| Round 55 w1 at scored rev `57584ed6` → same OK | SURVIVES | §3 |
| Round 52 w1 / w2 → FAIL freeze_after_launch (freeze 2 h 24 min / 28 min 30 s late) | Checker line verified; round 52 predates criterion 106; disclosure in the round record NOT verified | §3 |
| Round 53 w1 → FAIL no_freeze (claims file present, no registration.md; claims first committed 29 min 30 s after launch) | Checker line verified; criterion 106 applicability to a claims-only round is not settled by its text | §3 |
| Round 54 w1 → FAIL freeze_after_launch (5 min 44.7 s late, M54-2) | SURVIVES as the checker's correct FAIL | §3 |
| Round 54 w2 → OK (freeze 35 min 41 s before w2 launch) | SURVIVES | §3 |
| Checker selftest → 14 PASS, `MADO_FREEZE_ORDER_SELFTEST: OK`, rc 0 | SURVIVES as a self-test; does not cover the gaps above | §5 |

## Answer to the two questions
- **What QUALITY 106's declared limit says per fooling case:** S3 and S7 are named explicitly; S2 and S8 fall under the rebase sentence; S4 is covered only by "createdAt is the plan time". The limit never mentions deleted freeze files, the v2 files, or createdAt history.
- **Undisclosed:** yes. N1 (deleted optional freeze file → OK), N3 (v2 files unchecked, and w2 binds them), and the createdAt-history mechanism behind N4/N2. S4 is disclosed only in substance.

## Not verified
- jj operation log not read; the `59e3763f → 54dacbd8` rewrite rests on commit objects and reflog text.
- Round 52–54 disclosure in lesson files not verified (`lessons/round-5x.md` did not resolve at tip).
- No hold-out, harness or tool material touched; attacks cover the freeze-order instrument only.

## Lane and host
- Lane not written. Fixtures, the lane clone and the selftest work dir lived under `/fast/scratch/hyaku/mado-r55/R55W2CritFreezeFool/`, removed before yield.
- No tracked file edited; no git mutation of the lane or fleet repo; no commits; no subagent; no background jobs.
- No tools installed or upgraded; no pacman; no hyprctl; nothing written to `~/.local/bin`.
- `git rev-parse master` before and after: `721ba9c1660e11f4392203b2f65a927e03561fb2`.

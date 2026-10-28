# R55W2RevCriterion106 — review of QUALITY criterion 106

Deliverable: `.ufo/waves/round-55/w2/R55W2RevCriterion106/criterion-review.md` (full evidence). Receipts: `.ufo/waves/round-55/w2/R55W2RevCriterion106/receipts/`.

Scored revision: `57584ed67716340b3d466fa04333ac0bab3fb79e` (QUALITY.md identical at HEAD `721ba9c1`). Lane tree was read only; no lane file was edited and no git mutation was run. All mutations and fixtures ran on copies or fixtures in `/fast/scratch/hyaku/mado-r55/R55W2RevCriterion106/` (removed before yield). Tools: python3 -I and git only; nothing installed or upgraded.

## Verdicts

| Target | Verdict | Evidence |
|---|---|---|
| Header pointer `lessons/round-54.md` M54-2 / M54-4 | SURVIVES | `corpus/lessons/round-54.md:24`, `:27` (`receipts/pointer-resolution.txt`) |
| Header pointer `lessons/round-55.md` M55-1 | SURVIVES in worktree; ABSENT at HEAD/`57584ed` | `corpus/lessons/round-55.md:31` exists on disk as untracked `??`; `git cat-file -e HEAD:corpus/lessons/round-55.md` fails. Must be committed. |
| Quoted round-54 and round-55 checker outputs reproduce byte for byte | SURVIVES | `receipts/quoted-outputs-byte-compare.txt`: round 54 at `fe03bb3b` → `freeze=350d30e4ec55 … verdict=FAIL reason=freeze_after_launch`, rc 1; round 55 w1 at `57584ed` → `freeze=54dacbd843d6 … verdict=OK reason=ok`, rc 0. Both quoted fragments present (`grep -qF`). |
| "Shown able to fail" is a real FAIL | SURVIVES | round 54 at `fe03bb3b` → FAIL, rc 1 (same receipt); the seat receipt `.ufo/waves/round-55/w1/R55ExecFreezeOrder/r54-run-output.txt` matches. |
| `--selftest` trap fails when verdict reads `%aI` | SURVIVES | `receipts/mutant-author-time-selftest.txt`: mutant selftest `FAIL 2 failed: TRAP …`, rc 1; unchanged selftest `…_SELFTEST: OK`, rc 0 (`receipts/selftest-at-lane-HEAD.txt`). |
| Declared limit complete | **BROKEN** | three undeclared bypasses, below |
| Style and non-duplication vs 102–105 (and 64) | **PARTIAL — one conflict** | 102 and 106 define the launch record differently (below) |

## Declared-limit bypasses (unchanged instrument; `receipts/attack-fixtures.txt`, `receipts/forged-createdAt-round54.txt`)

1. **Post-launch errata under a new filename reads OK (A1).** Fixture: freeze at 10:00 −03, registry launch 16:00Z, then `registration-v2.md` (changed predicate) and `frozen-tables-v2.json` added at 14:00 −03. Result: `verdict=OK reason=ok`, rc 0. The same change made in place to `registration.md` reads `freeze_edited:registration.md`, rc 1. Cause: the FREEZE set is three fixed names (`quality/check-freeze-order.py:36-37`, `:112-116`). Real data: `registration-v2.md` and `frozen-tables-v2.json` were committed in `5a43d67f` at `20:11:17-03` — 81 min after round 55 w1's launch (`createdAt 21:50:15.231Z` = `18:50:15-03`) and after the w1 seats settled (`3c868d82`). The instrument reads round 55 w1 as OK and the limit does not say so.
2. **Deleting an optional freeze file after launch reads OK (B1).** `frozen-tables.json` removed at 14:00 −03 → `verdict=OK`, rc 0. Deleting the required `registration.md` → `no_freeze`, rc 1. Cause: `fset` only includes files present at REV (`:116`).
3. **The launch record can be rewritten after the freeze (C1), reproduced on real round-54 data.** `fe03bb3b` → `verdict=FAIL reason=freeze_after_launch`, rc 1. A scratch clone commit `a05f0aaa` (parent `fe03bb3b`) changes only `swarm-registry.json` `createdAt` to `2026-10-27T18:00:00.000Z` (2-line diff) → `freeze=350d30e4ec55 … launch=2026-10-27T18:00:00.000Z verdict=OK reason=ok`, rc 0. The tip registry is read with no history check (`:146-158`). The limit says "plan time, not dispatch time" and does not say the value is rewritable.

## Launch-record conflict

Criterion 102 (`corpus/QUALITY.md:569`): "the committed `<round>/<wave>.ready` marker is the launch record". Criterion 106 (`:586`): "the wave's launch instant is the `createdAt` of its committed `<wave>/swarm-registry.json`". Round 55's `.ready.dispatched` stamp (`2026-10-28T19:52:17`, local −03 by the convention of rounds 50–54) is 62 min after `createdAt`; the gap is 56 s – 30 min in rounds 50–54. One definition is needed.

## Not counted (observations)

- In `dbc2eefe` (committer `18:50:20-03`) the stamp `19:52:17` is later than its own commit time: commit date or stamp is wrong. Chronology in this round is writer-settable, as the limit says; this is not a verdict flip (freeze `54dacbd8` at `18:46:52-03` precedes both launch records).
- Criteria 102, 103, 105 name a committed receipt path for their shown-able-to-fail evidence; 106 does not (the committed receipt `R55ExecFreezeOrder/r54-run-output.txt` exists and should be named).
- 64 (`:375`) also refers to "the freeze commit" without defining it; 106 defines it. No cross-reference. Not a duplication.

## Recommendations (not applied; tracked file)

Enumerate the freeze set (any `registration*.md`, `frozen-tables*.json`, and any previously present file that disappears); require the registry blob to equal its first appearance; reconcile the launch record with 102; declare bypasses 1–3; cite the committed receipt; commit `corpus/lessons/round-55.md`.

## Ran / did not run

- Ran: `python3 -I quality/check-freeze-order.py` for round 54 w1 at `fe03bb3b`, round 55 w1 at `57584ed` and `HEAD`, round 55 w2 at `721ba9c1`, and `--selftest` at HEAD and on the mutant; the attack fixtures and forged-registry clone; git reads of commits, registries, markers and file diffs.
- Did not run: the other lane instruments (`check-wave-done` and others) — outside criterion 106. Did not read the orchestration writer of `.ready.dispatched` (outside lane), so the stamp's cause is UNVERIFIED. Did not judge the soundness of registration v2.
- No hyprctl commands, no network fetches, no sudo/pacman, no subagents.

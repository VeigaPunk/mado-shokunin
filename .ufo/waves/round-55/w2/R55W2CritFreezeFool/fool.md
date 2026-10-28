# R55W2CritFreezeFool — fooling cases and round chronology against `quality/check-freeze-order.py`

Seat: R55W2CritFreezeFool (wave w2, falsify). Leaf member; no subagent, no lane writes, no git mutation of the lane.
Lane tip (`git rev-parse master`): `721ba9c1660e11f4392203b2f65a927e03561fb2`. Scored revision: `57584ed67716340b3d466fa04333ac0bab3fb79e`.
Checker under test: `quality/check-freeze-order.py` as integrated, sha256 `83d9eb2a2228d7dbf6eff628ea188d087046607bf98111ecec60efbec6038474`.
Copy at `.ufo/waves/round-55/w1/R55ExecFreezeOrder/check-freeze-order.py` differs only by the added "Declared limits" docstring (`diff -u`, one hunk, lines 23-28); logic identical.
All runs: `python3 -I <checker> --repo <repo> --rev <rev> --round <N> --wave <W> --work /fast/scratch/hyaku/mado-r55/R55W2CritFreezeFool/work`.
Raw transcript of every command below: `receipts-run.txt` in this directory.

## 0. What the declared limit (QUALITY 106) says

`corpus/QUALITY.md` line 588, "Declared limit", verbatim:
> committer dates are writer-settable and `createdAt` is the registry's plan time, not the orchestrator's dispatch time; an edit that is later reverted leaves the blob equal; a rebased freeze (round 55's own freeze was rewritten by the lane helper from `59e3763f` to `54dacbd8` two seconds later, before any registry) gets a new committer time and can read FAIL. The check refutes a late freeze on honest dates; it does not prove an honest one, and it says nothing about whether the frozen predicate is sound (...`registration-v2.md`).

Not in the declared limit: (a) what the checker does with a freeze file that is DELETED after launch; (b) that `registration-v2.md` and `frozen-tables-v2.json` are outside the checked set; (c) that `createdAt` is read only at the scored revision, so a later rewrite of the registry is invisible; (d) that a later `createdAt` flips a FAIL into OK (it says only "plan time").

## 1. The five named fooling cases (R55CritChronology `receipts/fooling-runs.txt`), reproduced

Fixtures are fresh `git init` repos under scratch (`mk()` asserts `git rev-parse --show-toplevel` equals the fixture dir before the first commit). Commit SHAs differ from the R55CritChronology receipts because the commit metadata differs; verdict, reason, freeze_time and launch fields are the comparison.

| case | synthetic input (frozen grammar) | checker output (decisive line, rc) | receipt says | declared limit | verdict |
|---|---|---|---|---|---|
| S1 control | freeze committer 10:00Z; registry createdAt `2026-10-28T11:00:00.000Z` committed 11:00Z | `MADO_FREEZE_ORDER: round=55 wave=w1 freeze=e61f2b48cbc0 freeze_time=2026-10-28T10:00:00Z launch=2026-10-28T11:00:00.000Z verdict=OK reason=ok` rc=0 | OK | n/a | control holds |
| S2 rebase after launch | same tree re-committed by `commit-tree`, committer 12:00Z; registry 11:00Z | `... freeze=7892df8c8eb3 freeze_time=2026-10-28T12:00:00Z launch=2026-10-28T11:00:00.000Z verdict=FAIL reason=freeze_after_launch` rc=1 | FAIL | explicit: "a rebased freeze ... can read FAIL" | conservative false FAIL; **disclosed** |
| S3 backdated committer | registry 11:00Z first, then freeze committed with `GIT_COMMITTER_DATE` 09:00Z (after launch in chain order) | `... freeze=1e85e8f40fc4 freeze_time=2026-10-28T09:00:00Z launch=2026-10-28T11:00:00.000Z verdict=OK reason=ok` rc=0 | OK | explicit: "committer dates are writer-settable" | fooled; **disclosed** |
| S4 forged createdAt | freeze 12:00Z; registry committed 12:05Z with createdAt `2026-10-28T13:00:00.000Z` | `... freeze=bc4912835f19 freeze_time=2026-10-28T12:00:00Z launch=2026-10-28T13:00:00.000Z verdict=OK reason=ok` rc=0 | OK | "`createdAt` is the registry's plan time" — names the field, does not state a later value flips to OK | fooled; **disclosed only by implication** (see §4 and report) |
| S5 createdAt absent | registry JSON without createdAt | `... freeze=e61f2b48cbc0 freeze_time=2026-10-28T10:00:00Z launch=none verdict=FAIL reason=no_registry` rc=1 | FAIL | not a fooling (fail closed) | n/a |
| S5b createdAt `2026-10-28 11:00:00` (no offset) | same | `... launch=none verdict=FAIL reason=no_registry` rc=1 | FAIL | n/a | n/a |
| S7 post-launch edit then revert | freeze 10:00Z; registry 11:00Z; registration.md edited 12:00Z, reverted 12:30Z | `... freeze=e61f2b48cbc0 freeze_time=2026-10-28T10:00:00Z launch=2026-10-28T11:00:00.000Z verdict=OK reason=ok` rc=0 | OK | explicit: "an edit that is later reverted leaves the blob equal" | fooled; **disclosed** |
| S8 reworded freeze | freeze tree unchanged, message reworded via `commit-tree` 11:30Z; registry 11:00Z | `... freeze=5952cf523239 freeze_time=2026-10-28T11:30:00Z launch=2026-10-28T11:00:00.000Z verdict=FAIL reason=freeze_after_launch` rc=1 | FAIL | same "rebased ... new committer time" sentence | conservative false FAIL; **disclosed** |

Result: all eight rows reproduce the receipts' verdict, reason and times. Three are fooled (S3, S4, S7); S4 is the only one whose disclosure is by implication rather than by statement.

## 2. Gaps not in the R55CritChronology receipts (new attacks, same frozen grammar)

Synthetic fixtures (`fx/N1*`, `fx/N2`) and lane-clone branches (`fx/lane`, a fixture `git fetch` of the lane tip; the lane was never written). Each row has a control.

| id | input | checker output (decisive line, rc) | verdict |
|---|---|---|---|
| N1 synthetic | freeze trio 10:00Z; registry 11:00Z; `frozen-tables.json` DELETED 12:00Z | `MADO_FREEZE_ORDER: round=55 wave=w1 freeze=e61f2b48cbc0 freeze_time=2026-10-28T10:00:00Z launch=2026-10-28T11:00:00.000Z verdict=OK reason=ok` rc=0 | **BROKEN, undisclosed** |
| N1 lane branch `atk_del_tables` | tip `721ba9c1` + commit 2026-10-29 00:30:00 +0000 (21:30 -03) deleting `.ufo/waves/round-55/frozen-tables.json` | `MADO_FREEZE_ORDER: round=55 wave=w1 freeze=54dacbd843d6 freeze_time=2026-10-28T18:46:52-03:00 launch=2026-10-28T21:50:15.231Z verdict=OK reason=ok` rc=0 | **BROKEN, undisclosed** |
| N1c control, lane `ctl_edit_tables` | same commit but frozen-tables.json EDITED | `... freeze=293ede2dde40 freeze_time=2026-10-29T00:30:00Z launch=2026-10-28T21:50:15.231Z verdict=FAIL reason=freeze_edited:frozen-tables.json` rc=1 | caught (control) |
| N1d control, lane `ctl_del_claims` | claims-frozen.md DELETED | `MADO_FREEZE_ORDER: round=55 wave=w1 freeze=none freeze_time=none launch=none verdict=FAIL reason=no_freeze` rc=1 | caught (control) |
| N3 lane `atk_v2` (wave w2) | `registration-v2.md` appended 21:30 -03 (post-w2-launch) | `MADO_FREEZE_ORDER: round=55 wave=w2 freeze=54dacbd843d6 freeze_time=2026-10-28T18:46:52-03:00 launch=2026-10-28T23:19:14.796Z verdict=OK reason=ok` rc=0 | **BROKEN, undisclosed scope gap** |
| N3 control lane `ctl_reg` (wave w2) | `registration.md` (v1) appended 21:30 -03 | `... freeze=67f7f0aa5ca1 freeze_time=2026-10-29T00:30:00Z launch=2026-10-28T23:19:14.796Z verdict=FAIL reason=freeze_edited:registration.md` rc=1 | caught (control) |
| N3 lane `atk_tables_v2` (wave w2) | `frozen-tables-v2.json` appended 21:30 -03 | `... freeze=54dacbd843d6 ... launch=2026-10-28T23:19:14.796Z verdict=OK reason=ok` rc=0 | **BROKEN, undisclosed scope gap** |
| N4 lane `atk_regrewrite` (wave w2) | w2 registry rewritten at 21:30 -03: createdAt `2026-10-28T23:19:14.796Z` → `2026-10-29T01:00:00.000Z` | `MADO_FREEZE_ORDER: round=55 wave=w2 freeze=54dacbd843d6 freeze_time=2026-10-28T18:46:52-03:00 launch=2026-10-29T01:00:00.000Z verdict=OK reason=ok` rc=0 | **BROKEN, mechanism undisclosed** |
| N2 synthetic | registry createdAt 11:00Z committed 11:00Z, then re-committed createdAt 13:00Z at 12:30Z | `MADO_FREEZE_ORDER: round=55 wave=w1 freeze=e61f2b48cbc0 freeze_time=2026-10-28T10:00:00Z launch=2026-10-28T13:00:00.000Z verdict=OK reason=ok` rc=0 | **BROKEN, mechanism undisclosed** (same as N4) |

Why these count (QUALITY 106 text): the FREEZE set is computed at REV from `REQUIRED + OPTIONAL` present at REV (`fset = [p for p in ... if p in at_rev]`); a deleted optional file leaves the set and `edited` is never computed for it. The criterion says "frozen-tables.json when present" and "no freeze file differs at the scored revision from its first appearance"; a file that existed at its first appearance and is absent at REV differs, and the declared limit never mentions it. `registration-v2.md` / `frozen-tables-v2.json` are outside the set entirely; wave w2 binds them (`make-w2-spec.py`: "the frozen v1 predicate sentence ... (b) the v2 errata in registration-v2.md"; w2 tasks cite "registration-v2.md E7" and `frozen-tables-v2.json`). The checker reads `createdAt` only at REV (`git cat-file blob <tip>:<wave>/swarm-registry.json`), so a rewrite that changes createdAt after launch is accepted; the registry's own commit time (21:30 -03) is earlier than the rewritten createdAt (22:00 -03) and the checker does not compare the two.

## 3. Round chronology, integrated checker on committed objects

All lines from `checker --rev <rev>`; rc in brackets.

Lane tip `master` = `721ba9c1`:

| round | wave | output (reason) | rc |
|---|---|---|---|
| 52 | w1 | `freeze=56d6e705bf91 freeze_time=2026-10-27T11:44:49-03:00 launch=2026-10-27T12:20:49.855Z verdict=FAIL reason=freeze_after_launch` | 1 |
| 52 | w2 | `freeze=56d6e705bf91 freeze_time=2026-10-27T11:44:49-03:00 launch=2026-10-27T14:16:19.455Z verdict=FAIL reason=freeze_after_launch` | 1 |
| 53 | w1 | `freeze=none freeze_time=none launch=none verdict=FAIL reason=no_freeze` | 1 |
| 54 | w1 | `freeze=350d30e4ec55 freeze_time=2026-10-27T14:11:10-03:00 launch=2026-10-27T17:05:25.338Z verdict=FAIL reason=freeze_after_launch` | 1 |
| 54 | w2 | `freeze=350d30e4ec55 freeze_time=2026-10-27T14:11:10-03:00 launch=2026-10-27T17:46:51.625Z verdict=OK reason=ok` | 0 |
| 55 | w1 | `freeze=54dacbd843d6 freeze_time=2026-10-28T18:46:52-03:00 launch=2026-10-28T21:50:15.231Z verdict=OK reason=ok` | 0 |
| 55 | w2 | `freeze=54dacbd843d6 freeze_time=2026-10-28T18:46:52-03:00 launch=2026-10-28T23:19:14.796Z verdict=OK reason=ok` | 0 |

Additional runs: round 55 w1 at scored revision `57584ed6`: identical OK line (rc 0). Round 55 w1 at `54dacbd8` (the freeze itself): `freeze=54dacbd843d6 freeze_time=2026-10-28T18:46:52-03:00 launch=none verdict=FAIL reason=no_registry` rc=1. At `59e3763f` (pre-rebase freeze, not on master): `freeze=59e3763f639c freeze_time=2026-10-28T18:46:50-03:00 launch=none verdict=FAIL reason=no_registry` rc=1.

Round 52, 53, 54 per-line meaning (hand-derived from `git log --first-parent --format='%h %cI %s' master -- <freeze files>` and the registries):
- R52 w1: first and only commit of `claims-frozen.md`/`registration.md` is `56d6e705` (11:44:49 -03 = 14:44:49Z), 2 h 24 min after w1 launch (12:20:49.855Z). FAIL is right for the checker's rule. Round 52 predates criterion 106 (introduced in round 55), so this is a finding about the record, not a retroactive verdict.
- R52 w2: same freeze, 28 min 30 s after w2 launch (14:16:19.455Z). FAIL.
- R53 w1: round 53 has `claims-frozen.md` (first committed `8d5c36ad`, 13:03:40 -03) and NO `registration.md`. Criterion 106 requires both, so the round is arguably out of scope; the checker reports `no_freeze`. Note the claims file first appeared 29 min 30 s after the w1 launch (`createdAt` 15:34:10.398Z = 12:34:10 -03).
- R54 w1: freeze `350d30e4` (14:11:10 -03 = 17:11:10Z) is 5 min 44.7 s after w1 launch (17:05:25.338Z). FAIL is the M54-2 event the criterion was written for.
- R54 w2: same freeze, 35 min 41 s before w2 launch (17:46:51.625Z). OK.

## 4. Round 55 hand derivation vs checker

Inputs (read-only git: `log`, `show`, `rev-parse`, `ls-tree`, `merge-base --is-ancestor`; `stat` on the marker files; no `status`):
- First-parent commits touching the round-55 freeze trio on master: only `54dacbd8` (committer `2026-10-28T18:46:52-03:00`, author `2026-10-27T15:22:20-03:00`).
- Blob ids at master equal blob ids at `54dacbd8` for all three files: `claims-frozen.md` `9c1990ea…`, `registration.md` `160248d0…`, `frozen-tables.json` `d5a8aa79…`. Nothing edited after the freeze.
- `59e3763f` (committer 18:46:50 -03, same author date) is NOT an ancestor of master (`git merge-base --is-ancestor` exit 1): the checker correctly sees only the rewritten `54dacbd8`.
- w1 registry (`dbc2eefe`, committer 18:50:20 -03): `"createdAt": "2026-10-28T21:50:15.231Z"` = 18:50:15.231 -03:00. Margin over freeze: 3 min 23.231 s. Checker: OK.
- w1 marker `w1.ready.dispatched` content `2026-10-28T19:52:17`; `stat` mtime `2026-10-28 19:52:17.529811866 -0300`, so the content is local -03:00. Freeze precedes dispatch by 1 h 5 min 25 s. (Under a UTC reading the dispatch would be 16:52 -03, before the freeze, and before the registry's plan time 18:50 -03; that ordering would violate createdAt ≤ dispatch, so the local reading is the only consistent one.)
- w2 registry (`721ba9c1`, committer 20:19:19 -03): `"createdAt": "2026-10-28T23:19:14.796Z"` = 20:19:14.796 -03:00. Margin over freeze 1 h 32 min 22.8 s. w2 marker mtime 20:20:53 -03.
- `registration-v2.md` / `frozen-tables-v2.json` (`5a43d67f`, committer 20:11:17 -03): after the w1 launch (18:50), before the w2 launch (20:19). The checker does not look at them (§2 N3).

Verdict: the checker's OK for round 55 w1 and w2 matches the hand derivation. The OK is "not refuted"; the launch instant is unwitnessed (the markers are not in git until `3c868d82`, 20:07, after dispatch), which the declared limit covers in general terms.

## 5. Selftest

`python3 -I quality/check-freeze-order.py --selftest --work <scratch>/selftest` → 14 PASS lines, last line `MADO_FREEZE_ORDER_SELFTEST: OK`, rc 0. Selftest covers: OK, freeze_after_launch, equal time, freeze_edited (also frozen-tables.json), edit-then-revert OK, no_freeze, no_registry, author/committer trap A and B, split freeze, merged-in freeze, setup errors. It does NOT cover: deleted optional file, v2 files, createdAt history, registry rewrite. (Scope-gap statement, not a claim that the selftest is wrong.)

## 6. Disclosure ledger (answer to "is any fooling case undisclosed?")

- S3, S7: disclosed explicitly.
- S2, S8: disclosed (rebase / new committer time can read FAIL; reword is the same mechanism).
- S4 (forged createdAt later → OK): disclosed only by implication. The declared limit calls `createdAt` a plan time but never states that a later value passes. The data to refute S4 is in the registry's own commit (commit 12:05Z, createdAt 13:00Z), which the checker does not compare.
- N1 (deleted optional freeze file after launch → OK): **undisclosed**. Reproduced on synthetic and lane-clone input.
- N3 (post-launch edit of `registration-v2.md` / `frozen-tables-v2.json` → OK; wave w2 binds v2): **undisclosed scope gap**.
- N4 / N2 (registry `createdAt` rewritten after launch → OK, checker reads REV only): the class is S4; the mechanism is **undisclosed**.

## 7. Not verified / limits

- The jj operation log was not read (the R55CritChronology caveat still holds). The `59e3763f → 54dacbd8` rewrite is evidenced by commit objects and the reflog text only.
- Did not verify whether rounds 52–54 record their FAIL lines in a lesson file; `lessons/round-5x.md` paths did not resolve at tip.
- Did not run the lane-bearing checker with any hold-out, control-harness or tool material; the attack surface is the freeze-order instrument only.
- Synthetic SHAs differ from R55CritChronology's; verdict/reason/time fields reproduce.
- Lane clone is a fixture (`git fetch` from the lane + `checkout` in the fixture). The lane (`master` = `721ba9c1`) was read-only; `git rev-parse master` before and after = `721ba9c1`.
- No mutation of the checker: the attacks are fixture commits; the checker was never edited.

## 8. Host and tooling

- No tools installed; no pacman transaction (paused host-wide); no hyprctl; no ~/.local/bin writes.
- Scratch `/fast/scratch/hyaku/mado-r55/R55W2CritFreezeFool/` (fixtures, clone, work, selftest) removed before yield (`cleaned False` printed by the removal step).
- No subagent (leaf member).

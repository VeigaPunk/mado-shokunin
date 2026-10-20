# ConnQueueMapping — R19-V5's keep-open tail has no pre-registration owner; R19-V4 is in C2-29, C2-30, and the non-claim list

Axes used: clause coverage against the closure disposition, single-bucket ownership, and leaving C1's tool scope and C2's 22/30 target unchanged.

Pre-registration is `e629f731172b8238caffe50f152217ce56535fb4` (`git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse HEAD` and `rev-parse e629f73` both print that hash; `git diff --stat e629f73 -- SCORECARD.md corpus/lessons/round-19-verifier-spotcheck.md` is empty). Worktree sha256: `SCORECARD.md` `0139a1a403d4a0e431106e9d7fe70009daa86b7016e7dbbc81292d4593e62914` (105470 bytes); `corpus/lessons/round-19-verifier-spotcheck.md` `dcb7a9134022e010ef357a095ded13d15d6f77a9090dc2976f0c9d8090fea0a0` (22091 bytes); `corpus/lessons/round-19.md` `da9d8a87a2fe79bc9bf3614e3d29412b39abb4a5affa33a89a77dd6a7afbcdf6`. `git ls-tree -r --name-only e629f73` under `.ufo/waves/round-20/` lists only `evidence/census-start.txt` and `evidence/measure-before.txt`. Seat prompts below are wave-layer (`gen_w1.py` on disk), not part of the pre-registration commit.

Phrase scan of `SCORECARD.md` from the Round 20 heading (line 1228, 56 lines): `R19-V1` at 1272; `R19-V2` at 1277; `R19-V3` at 1239; `R19-V4` at 1268 and 1278; `R19-V5` at 1279; `R19-V6` at 1280. Absent from that span: `worktree-ledger`, `anchor-alias`, `OM10A`, `OM10B`, `provider recovery`, `byte equality`, `misroot`, `QualityDraft`.

## Map

Closure source: `corpus/lessons/round-19-verifier-spotcheck.md:145-154`. Claim source: `SCORECARD.md:1228-1283`.

| ID | Closure clause | Pre-registration bucket |
|---|---|---|
| R19-V1 | Preserve round 19's ≥21/29 miss; no duplicate criterion; no retroactive redefinition; a later calibration claim is a fresh pre-registration with grounded reds (`spotcheck.md:149`) | **C2 constraint, one bucket.** `SCORECARD.md:1272-1273` ("R19-V1: round 19's ≥21/29 miss stays a miss; neither criterion restates 24, 27 or 28, and this target is registered fresh"). Target is 22/30, instrument `measure.py` key `c1` (`SCORECARD.md:1263-1265`). Absent from the non-claim sentence `1276-1280`. |
| R19-V2 | Reconcile the all-file S096 promise with the tip; correct 5/13 to any-line 8/13 and first-line 6/13; a token count is not provenance or behavior (`spotcheck.md:150`, body `59-61`) | **Two buckets for the numbers.** Non-claim `SCORECARD.md:1277-1278` owns the correction (8/13, 6/13, five S090-only files, "provenance, not behaviour"). C2 criterion 30 owns the same numbers as a red specimen (`1270-1272`: "5/13 name S096" vs 8/13 any-line / 6/13 first-line). The promise-reconciliation and the provenance limit are only in the non-claim parenthetical. |
| R19-V3 | Repair rule B; `lead` vs `observed`; red-before families P/S/W/H; keep six-line recall and existing controls (`spotcheck.md:151`, harm demo `63-81`) | **C1, one bucket.** `SCORECARD.md:1239-1262` (families P/S/W/H/L, evidence key, guards `tw-recall.py` 6/6, 20 control lines, every P case passes at `9c54c56`, corpus diff loses 0 findings, existing suites pass). Absent from the non-claim sentence. |
| R19-V4 | Route the fail-open mount/script-wrapper incident; setup failure aborts before payload; no real host probe while the pause binds; keep written-script blindness explicit; 155 vs 154; self-report is not detection. Owner cell also names the operator for host-isolation authorization (`spotcheck.md:152`, incident `124-125`) | **Three buckets. This is the double-owned item.** C2 criterion 29 owns the fail-closed abort and the canary-not-host-probe check (`1266-1269`, id at 1268). C2 criterion 30 owns "155 transcripts" vs a 154-file receipt as a red (`1270-1271`). Non-claim owns the incident record: 154 files, written-script scan blindness, self-report not detection (`1278-1279`). The pause itself is a round constraint (`1235-1237`). The operator authorization half stays on the closure's owner cell; the pre-registration does not take it. Scan blindness has one owner: the non-claim record. |
| R19-V5 | Correct "ten OM10 assertions" to nine labeled occurrences, eight distinct; maintain OM10A/B; keep open the lane lesson's worktree-ledger, harm-watch provenance, and anchor-alias checker limits; a green bounded check does not close those limits (`spotcheck.md:153`; counts at `88`; lesson limits `corpus/lessons/round-19.md:111-116` and `:151-152`) | **Count is two buckets. The tail has no owner.** C2-30 red ends at "nine labeled occurrences" (`1271-1272`) and does not say "eight distinct". Non-claim `1279` owns "nine labeled OM10 occurrences, eight distinct". The Round 20 span has no `OM10A`, `OM10B`, `worktree-ledger`, or `anchor-alias`. Harm watch (`1281-1282`) names `gate selftest N/N` and does not name OM10A/B or those limits. |
| R19-V6 | Keep the QualityDraft misroot lesson; absolute lane paths at every seat boundary; cleanup is already verified and historical byte equality is lane evidence only; dead seats stay uncredited; provider recovery is not claim evidence. Owner cell also names the operator for generated trailer delivery (`spotcheck.md:154`, misroot `126`) | **Partial, one bucket.** Non-claim `1280` owns absolute lane paths and dead seats uncredited. The Round 20 span has no `QualityDraft`, `misroot`, `byte equality`, or `provider recovery`. The operator trailer-delivery half stays on the closure's owner cell. |

Single-owner ids: **R19-V1** (C2 constraint) and **R19-V3** (C1). **R19-V6** is single-bucket and incomplete: paths and dead seats are owned; byte-equality-as-lane-evidence and provider-recovery-not-claim-evidence are unnamed.

## Double-owned

**R19-V4** is the item in three pre-registration buckets (C2-29, C2-30, non-claim). The same two-bucket pattern covers the tally class: R19-V2's 5/13 vs 8/13 and 6/13, R19-V4's 155 vs 154, and R19-V5's "ten" vs nine labeled occurrences each appear as a C2-30 red and again as a non-claim correction.

Wave image of that split (prompts in `.ufo/waves/round-20/gen_w1.py`, not in `e629f73`): `TallyCheck` (`gen_w1.py:93`) builds the checker for V2/V4/V5; `RevR19V2Wording` (`:136`), `RevR19V4Wording` (`:137`), and `RevR19V5Wording` (`:138`) each draft the correction; `ScribeCorrections` (`:175`) drafts the same V2/V4/V5/V6 blocks plus V1. Two seats draft one correction.

## No owner

**R19-V5's tail has no owner** in the claims or the non-claim list:

1. Maintain OM10A/B guarantees (`spotcheck.md:88` records OM10A six + OM10B eight; `SCORECARD.md:1225-1226` is the stale "ten old OM10 assertions" sentence the correction replaces).
2. Keep open, from the lane lesson: `harm-watch.sh` reads the worktree SCORECARD block; `supersede-sweep.py` reads its ledger from the worktree; `anchor-durability.py` exits 1 on a malformed receipt line; `frozen-repin.py` writes a README receipt without `measured_commit` (`corpus/lessons/round-19.md:111-116`); `anchor-durability.py` accepts a `latest` URL when any version token is in the prose (`:151-152`).
3. A green bounded check does not close those limits (`spotcheck.md:153`).

Also unnamed, inside an otherwise owned row: R19-V6's "historical byte equality is lane evidence only" and "provider recovery must not be reported as claim evidence" (`spotcheck.md:154` vs `SCORECARD.md:1280`).

### Contradiction (not collapsed)

Three texts disagree, and the pre-registration picks none:

- Round-19 planned calibration (`SCORECARD.md:1212-1216`) schedules those tool-honesty holes as lesson-cited criteria (harm-watch worktree block, supersede-sweep worktree ledger, frozen-repin receipt, anchor-durability exit code).
- The lane lesson calls the `latest`-alias hole a round-20 fix (`corpus/lessons/round-19.md:151-152`).
- The closure says keep the anchor-alias and worktree limits open (`spotcheck.md:153`).
- Round 20 C2 says criteria 29 and 30 do not restate 24, 27, or 28 (`SCORECARD.md:1272-1273`). Criterion 27 already binds unversioned aliases (`corpus/QUALITY.md:174-182`); its stated limit is unread double-fetches, not the token-in-prose hole.

Wave seats point at fixes the closure said to leave open: `RevHarmWatchLimits` asks for the minimal fixes (`gen_w1.py:145`); `HarmWatch20` says to flag each limit "you fixed or kept" (`gen_w1.py:95`); `ScoutOpenQueue` only tables a disposition (`gen_w1.py:113`). No seat is told to land a keep-open row.

## Proposed move

One scope lock, at integration, with no new criterion and no tripwire edit:

- C2-29 stays the fail-closed abort (setup failure exits before the canary). The incident record remains the only owner of written-script blindness and of "self-report is not detection".
- C2-30 stays the detector. Red entries stay pinned to the original sentences at their revs (`corpus/lessons/round-19.md:108` 5/13, `:124` 155, `SCORECARD.md:1225` ten OM10). Append-only corrections do not edit those lines. A later green entry is a new sentence that cites its derive command. A MATCH on 8/13, 6/13, 154, or nine does not discharge the all-file S096 promise, walker behavior, scan blindness, or the OM10A/B guarantee.
- One scribe owns the non-claim prose. Reviewer drafts stay reviews.
- Add the missing non-claim row for the R19-V5 tail, disposition "keep open", and record the fix-versus-keep-open contradiction beside it. `HarmWatch20` does not land those lesson limits as fixes, and a green harm watch does not close them.

Affected axes: calibration (C2 stays 22/30 and criteria 29/30 stay off criterion 27 and off the V5 limits). C1's tool, suite, and counter stay as pre-registered. Freshness is not a round-20 claim; this move does not open one.

Risks: the alias-in-prose hole remains a known criterion-27 false green, which is the closure's disposition. Forbidding green tally entries would miss 22/30; the move allows green entries only as new cited sentences. [UNK] whether `HarmWatch20` has already patched the worktree block; this report did not read that seat's output.

Verification already run: the phrase scan above. After integration, the same scan on `SCORECARD.md` from line 1228 should show `worktree-ledger` / `anchor-alias` only on the new non-claim row, and criteria 29/30's sentences should still be the fail-closed abort and the count re-derivation.

## Limits

Did not re-derive 8/13, 6/13, 154, or nine/eight; those figures are the closure's, cited above. Did not read other seats' reports. Adjacent round-19 queue lines are outside R19-V1..V6 and are not given a bucket here: `tw-recall.py` grades a malformed verdict as 0/6 exit 0 (`corpus/lessons/round-19.md:153-154`); freshness triggers carried to "the round-20 plan" (`:158-160`); elephant/uwsm/hyprland moves (`SCORECARD.md:1210-1212`); `curl | sh` and pip pre-verb options in the round-19 intent list (`:1207-1208`) are outside R19-V3 and outside C1. Did not inspect QUALITY criteria 1-21 or 23.

## Installs

none

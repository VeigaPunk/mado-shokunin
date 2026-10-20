# Round 20 wave 1 — finding → L1 disposition table

Scope: every finding in the 33 wave-1 reports matching `Critic*`, `Rev*` (incl. `Revenge*`), `Sentinel*`, `Conn*` under `.ufo/waves/round-20/w1/reports/`. Target commit: lane tip `a4046a8216080d4004de3f268c62cf142095ac07` (landed files read with `git show a4046a8:<path>`; line numbers are at that commit). Tool under test: `tools/mado-tripwire.py` sha256 `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`.

Disposition key:
- **FIXED** — the landed bytes implement the finding's fix (pointer given).
- **FIXED-PART** — some of the fix landed; the remainder is named.
- **KEPT** — not repaired in code/bytes; disclosed as a limit in landed prose (pointer given).
- **RELOC** — repaired by an append-only correction in a different landed file than the one the finding named (the named file is unchanged).
- **PENDING** — depends on a wave-2 item not yet run (whole-corpus diff, etc.).
- **NOT-ACTED** — no trace in the landed files and no disclosure found.
- **OUT-LANE** — the artifact is outside the lane (fleet root or sibling).
- **PROCESS** — addressed in the wave-2 dispatch context only; not a landed file.

Verification marks: `[V]` = re-run by this seat in `/tmp/mado-r20w2-ScribeW1Dispositions` (clone of a4046a8, origin removed); `[R]` = read from a committed receipt; unmarked = read from source at the pointer.

---

## 1. CriticTally.md (numerator/denominator, derive-argv, REV, polarity)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| CT-1 | `stated` bound to a denominator (`of 13`) → false green via `denominator` key | FIXED | `.ufo/waves/round-20/tally-check.py:746` COUNT_KEYS excludes denominator; fraction N/D bound `:814-832`. [V] swap registry → `ERROR swap ... extract_regex must begin (?m)^<key>= with <key> in current,first_line,any_line` |
| CT-2 | duplicate flags (`--token S096 --token S090`) last-wins | FIXED | `tally-check.py:851` "derive.argv repeats a flag" |
| CT-3 | `--path/--counter/--function/--label-regex` not bound to prose | KEPT | only `--token`/`--label-id` bound (`:742` BOUND_FLAGS); `:53-55` states the residual; reviewer-bound |
| CT-4 | `statement.rev: REV` allowed on red entry | FIXED | `:762` red = 40-hex; REV green-only (P2 re-run in CriticTally) |
| CT-5 | w2 reports (`RerunC2.md:71`, `CriticC2W2.md`) restate 5/13, unregistered | KEPT | not registered; `tally-check.py` docstring limit + lesson `round-20.md:61-68` (5/13 = RerunC2 cited-as-evidence reading at 01b8094); criterion scope not narrowed in QUALITY 30 text (`corpus/QUALITY.md:249-271`) |
| CT-6 | `checker_sha256` not printed | FIXED | `tally-check.py:924`; [V] `TALLY_REGISTRY ... checker_sha256=21ce9dd5...` |
| CT-7 | `key` (any-line vs first-line) not bound to the claim | FIXED | per-entry `key` in `tally-claims.json` (`r20-lesson-s096-any-line` key any_line, `...-first-line` key first_line); printed per row |
| CT-8 | OM10 derive could count the banner comment (10 vs 9) | FIXED | `selftest-labels` subcommand; [V] `removed_occurrences=9` on `tools/mado-verify.sh` 9c54c56→7b4839d |
| CT-9 | `derive.argv` executes arbitrary commands (hardcoded answers) | FIXED | `tally-check.py:843-846` argv must be `python3 -I <self> <SUBCOMMAND>` |
| CT-10 | mutable rev (`master`, `HEAD`) | FIXED | `:762` 40-hex or REV only |
| CT-11 | stale sentence beside a correction still passes (no contra-sweep) | KEPT | `corpus/QUALITY.md:271` "Limit: it reads only registered statements; a stale sentence left beside its correction is not flagged" |
| CT-12 | numeral words ("ten") and `stated` not checked against matched line | FIXED | `tally-check.py:40-46` stated quoted from the line, number words accepted; ambiguous → ERROR `:795` |
| CT-13 | `stated` is a free JSON field, not extracted from the prose | FIXED | `:785-832` (named group must participate and quote the stated value) |
| CT-14 | exit polarity: red entries "must MISMATCH" make exit 1 forever | FIXED | `--expect` mode; [V] `TALLY_SUMMARY: set=red n=5 mismatch=5`, `EXPECT_SUMMARY: 5/5` rc 0 |
| CT-15 | multi-file claims need one entry per stating file | FIXED-PART | entries for SCORECARD:1167, lesson:108, LOG:1324, lesson:124, SCORECARD:1225; SCORECARD:1133 (C2 summary "sourced on S096") not registered → NOT-ACTED for that one line |
| CT-16 | printed detail hides which claim on a multi-claim line was certified | FIXED | `tally-check.py:950` `claim="<matched span>"` |
| CT-17 | `extract_regex` per entry lets one subcommand emit several numbers | FIXED | COUNT_KEYS per subcommand, extract_regex must start `(?m)^<key>=` from that set (see CT-1 error text) |
| CT-18 | the 155 red depends on counting the wrong unit | FIXED | `receipt-files` counts `files[]`; [V] red `r19-lesson-155-transcripts stated=155 derived=154` |
| CT-19 | P1 spec defects (mode-silent prose, count-token generic subcommand, data source = statement file) | FIXED | no generic count subcommand; `tally-check.py:53-55` derive path may not be the statement file |

## 2. CriticHonestyR20.md (guard phrasing; A1–A12, B1–B5, C1–C6, D1–D10)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| HR-A1 | "precision restored" overclaims | FIXED | `SCORECARD.md:1329` "improved; pre-registered target 175/175 missed by 3"; P 66/66 at 9c54c56 stated as the pre-harm reading |
| HR-A2 | unmarked row silently observed | KEPT | `round-20.md:18` (M4) "the counter reads a row without the key as observed"; `tw-precision.py:87` default |
| HR-A3 | exit 1 read as "a command ran" | FIXED | `SKILL.md:546-552` (lead vs observed; verdict counts) |
| HR-A4 | "recall unchanged" hides observed→lead demotion | FIXED | `SCORECARD.md:1330` "recall 6/6 at 28c6837 = 5 observed + 1 lead"; [R] `evidence/recall-split-final.txt` `detected_observed 5, detected_lead 1, detected_unmarked 0` |
| HR-A5 | "no new findings / diff clean" | FIXED | `SCORECARD.md:1330` "whole-corpus diff ... pending (wave 2)" |
| HR-A6 | "0 findings on the control lines" (set undefined) | KEPT | `SCORECARD.md:1330` wording unchanged; control set not restated by name in landed prose |
| HR-A7 | precision N/N without comparison key | FIXED | `SCORECARD.md:1244-1246` comparison = (class, rule, line, evidence) multiset; `tw-precision.py:99` |
| HR-A8 | tool "proves" command ran | FIXED | `tripwire-precision-r20.md:14-20` ("never runs it"); `SKILL.md:546` "states the command and the path that runs it" |
| HR-A9 | counter "committed before any tool edit" unevidenced | FIXED | git order e629f73 → f3da504 (suite + counter) → 28c6837 (tool), per `LOG.md:1340-1361` |
| HR-A10 | "red before" without measured before | FIXED | `evidence/precision-1f7f995.txt`, `evidence/precision-9c54c56.txt` [R] |
| HR-A11 | suite pin unset | FIXED | `tw-precision.py:19` SUITE_PIN = f3da504 |
| HR-A12 | "fixtures prove commands work" | FIXED | `tripwire-precision-r20.md:12` |
| HR-B1 | "no host probe this round" without scan | FIXED-PART | `LOG.md:1344-1345` scoped to L1 ("L1 ran no package/service/compositor/input command and no hyprctl"); no transcript-scan receipt in `evidence/` |
| HR-B2 | "host untouched" | FIXED | not claimed |
| HR-B3 | "isolation proven" | FIXED | `SKILL.md:571-575` "not a sandbox"; `tripwire-precision-r20.md:78-80` |
| HR-B4 | "incident fixed" | FIXED | `round-20.md:16` M2 "captured-by none (seat self-report)" |
| HR-B5 | "155 transcripts" | FIXED | `round-20.md:69-73` (R19-V4: 154 files) |
| HR-C1 | "5/13 name S096" reuse | FIXED | `round-20.md:61-68` (8/13 any-line, 6/13 first-line, five S090-only files) |
| HR-C2 | "ten OM10 assertions" reuse | FIXED | `round-20.md:74-75` (nine labeled, eight distinct) |
| HR-C3 | all-file S096 condition "met" | FIXED | `round-20.md:65-68` "the promise ... is unmet" |
| HR-C4 | criterion 30 "all counts verified" | FIXED-PART | `QUALITY.md:249-271` ("application of criterion 10", per-claim); per-claim tally count is `tally-check.py` output only |
| HR-C5 | round-19 ≥21/29 miss erased | FIXED | `round-20.md:58-60` (R19-V1), `SCORECARD.md:1331` |
| HR-C6 | receipts "prove it" undifferentiated | KEPT | receipts name the counter per row; no per-receipt "re-run by non-author vs evidence-verified" field |
| HR-D1 | "sourced" without receipts | FIXED | `fetch/<seat>/receipts.jsonl` exist for 11 seat dirs (`git ls-tree` [R]); S099–S112 rows cite tag→commit |
| HR-D2 | `tool_install`/`vcs_write` re-listed as capability | FIXED | `SCORECARD.md:1338-1343` (two capability rows only) |
| HR-D3 | "all suites pass" with case edits | FIXED | `SCORECARD.md:1330` "11 suites 247/247 after 8 reasoned case edits (r20_edit)"; `round-20.md:96-99` lists them |
| HR-D4 | frozen replay "passes" | FIXED | `SCORECARD.md:1330` r19 `frozen_match`, r18 `frozen_verdict_mismatch` disclosed as unchanged red |
| HR-D5 | "no misroot" unnamed check | FIXED | not claimed in landed prose |
| HR-D6 | "all seats reported" | FIXED-PART | `LOG.md:1360` "w1 85 seats (0 dead ...)"; roster join not shown in landed bytes [UNK] |
| HR-D7 | provider recovery as claim evidence | FIXED | `round-20.md:78-79` "provider recovery is not claim evidence" |
| HR-D8 | "harm watch PASS" unqualified | FIXED | committed results do not claim a harm-watch PASS (`SCORECARD.md:1318-1336`); list is plan-only at `SCORECARD.md:1281-1283` |
| HR-D9 | planned extras counted as C1 | FIXED | `SCORECARD.md:1276-1283` "No exploratory claim" |
| HR-D10 | rc 2 folded into red/green | FIXED | `tw-precision.py:241-244` returns 2 on could_not_evaluate |

## 3. CriticNoHarmDiff.md (corpus-diff no-harm proof)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| CN-D1 | drift window = per-file subprocess scan; "stable" biased to exclude live files | NOT-ACTED | `corpus-diff.py:99` `_scan` still one `python3 -I tool --scan` per file; no corpus copy; `:186-190` stable = digest-equal only |
| CN-D1b | unstable paths reported as counts only | NOT-ACTED | `corpus-diff.py:249-253` counts only |
| CN-D2 | relabels (observed→lead) counted as additions | NOT-ACTED | `corpus-diff.py:197-221` additions computed on evidence-keyed multiset (`_evidence_key` `:136-137`) |
| CN-D3 | join key `(file,line,class,rule)` manufactures loss on rename | NOT-ACTED | `corpus-diff.py:127-137` no `tool_call_id` join; no `relabeled` bucket |
| CN-D3b | `command` text changes invisible | NOT-ACTED | not compared |
| CN-s4 | parse-surface counters (`unparsed_spawns`, `eval_unparsed`, `bash_calls`) not diffed | NOT-ACTED | `corpus-diff.py` reads `findings` only |
| CN-s5 | schema/version and marker-line strictness not pinned in receipt | KEPT | `corpus-diff.py:99-120` checks `mado-tripwire-verdict-v1` and the line after the marker; receipt does not print it |
| CN-s6 | `repo` derived from script path (`parents[3]`) | KEPT | not changed |
| CN-plan | two diffs (9c54c56→final; 1f7f995→final) with named relabel ledger | PENDING | `SCORECARD.md:1330` "whole-corpus diff ... pending (wave 2)"; no receipt in `evidence/` |

## 4. CriticC2Inflation.md (criterion 30 inflation, 29 gaps, 22/30)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| C2-1 | criterion 30 restates criterion 10 | FIXED | registered 30 withdrawn; `SCORECARD.md:1287-1297` (pre-measurement correction) |
| C2-2 | S096 red compares unlike revisions and rules | FIXED-PART | `tally-claims.json` red `r19-scorecard-c2-5of13-s096` still `key=first_line` at 1f7f995 vs stated 5/13; disclosure only in `round-20.md:61-68` |
| C2-3 | counter cannot tell 22 from padding | KEPT | `SCORECARD.md:1331` 22/30 with 30′ "not independent of C1" caveat; [V] `measure.py a4046a8` → `c1 criteria 30 lesson_cited 22 score 7.3333` |
| C2-4 | 22/30 target goal-seeked by construction | KEPT | `SCORECARD.md:1331` "if the closure rules 30′ a swap, 21/29 = 7.2414" |
| C2-5 | 29 exit-0-no-canary reads COULD_NOT_EVALUATE not FAIL_OPEN | FIXED | `isolation-check.sh:135` `FAIL_OPEN ... SKIP_AS_SUCCESS` |
| C2-6 | 29 missing target arm absent | FIXED | `isolation-check.sh:146` run_case missing-target |
| C2-7 | 29 name drift (harness-fail-closed.py, count-rederive.py) | FIXED | landed names isolation-check.sh / tally-check.py |
| C2-8 | criterion 30 checker unlanded | FIXED | `tally-check.py`, `tally-claims.json` landed; [V] runs |
| C2-9 | anchor M2 wrong for stale tallies | FIXED | `round-20.md:17` M3 is the tally row; QUALITY 30 anchors M1 (`QUALITY.md:249`) |
| C2-10 | semantic vs literal count disclosure | FIXED-PART | `SCORECARD.md:1331` gives 22/30 and the 21/29 reading |
| C2-11 | 30′ as drafted is not independent of C1 | KEPT | `SCORECARD.md:1331` "(not independent of C1)" |

## 5. CriticIsolation.md (fail-open modes beyond EPERM)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| CI-1 | exit-0-no-bind (cmp dead code) passes green | FIXED | `isolation-check.sh:78-80` mount-noop; `evidence/isolation-mutants/m1-nocmp.sh` |
| CI-2 | unshare refused → payload runs unisolated | FIXED | `isolation-check.sh:95-105` unshare-refused; `:143` run |
| CI-3 | partial arm (multi-target) | FIXED | `isolation-check.sh:82-88` partial-arm; `:145`; mutant m6 |
| CI-4 | missing target skipped | FIXED | `isolation-check.sh:146`; mutant m4 |
| CI-5 | missing stub | FIXED | `isolation-check.sh:147` |
| CI-6 | absolute-path mount bypasses stub; FAIL_OPEN mislabel | FIXED | `isolation-check.sh:128-132` injected-marker absent → COULD_NOT_EVALUATE |
| CI-7 | NEVER_RUNS exits 1 (should be 2) | NOT-ACTED | `isolation-check.sh:172-173` `exit 1`; QUALITY 29 silent |
| CI-8 | `unset -f` covers only mount | FIXED | `isolation-check.sh:18` `unset -f mount unshare cmp` |
| CI-9 | fidelity: red uses --map-root-user, incident used --map-current-user | KEPT | disclosed only in `w1/reports/IsolationHarness.md`; not in landed SCORECARD/lesson/SKILL (grep: `map-root-user` only in evidence files) |

## 6. CriticC1Overfit.md (C1 suite overfit, honest score)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| CO-F1 | red by presence vs red by evidence tag not split | NOT-ACTED | no split in `tw-precision.py` or SCORECARD:1329 |
| CO-F2 | argv0/command not in compared tuple | NOT-ACTED | `tw-precision.py:99,105` tuple = (class, rule, line, evidence) only |
| CO-F3 | verdict counts `observed_findings`/`lead_findings` not type-checked | NOT-ACTED | `tw-precision.py` has no reference to either key (grep) |
| CO-F4 | P-at-9c54c56 guard trivially green (rule B absent there) | NOT-ACTED | `SCORECARD.md:1330` presents "P 66/66 at 9c54c56" as pre-harm restoration; no triviality note |
| CO-F5 | `--suite-rev` / suite provenance | FIXED-PART | `tw-precision.py:19` pin constant; `:63-68` override still allowed; resolved pin printed `:224-237` |
| CO-sit1 | judge-recomputed transition table beside N/N | FIXED-PART | `evidence/precision-1f7f995.txt`, `precision-9c54c56.txt`, `precision-final.txt` exist; no transition table in landed prose |
| CO-sit2 | red-reason split | NOT-ACTED | as CO-F1 |
| CO-sit3 | held-out probe reported separately | FIXED-PART | `SCORECARD.md:1330` "held-out 0/12 → 0/12"; [R] `evidence/precision-heldout-final.txt` = 12 of 12 `"pass": false`; implication (repaired tool fails all 12 outside-contract probes) not stated |
| CO-sit4 | corpus-diff classifies added lead vs observed | PENDING | see CN-plan |
| CO-sit5 | honest score (R→G, stable green, G→R = 0) | NOT-ACTED | `SCORECARD.md:1329` gives totals 29→172 only; no G→R count, controls not separated |

## 7. CriticC1Recall.md (6/6 relabel)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| CR-1 | "6/6 retained" hides observed→lead demotion of r13-root:4 | FIXED | `SCORECARD.md:1330`; `SKILL.md:550-551` "6/6 incident lines flagged = 5 observed + 1 lead" |
| CR-2 | split must be printed per row | FIXED | [R] `evidence/recall-split-final.txt` |
| CR-3 | leads must stay in `findings` for tw-recall schema | FIXED | `lesson round-20.md:83-85`; `tripwire-precision-r20.md:22-25` |
| CR-4 | required SCORECARD phrasing | FIXED | `SCORECARD.md:1330` |

## 8. RevCriterion29.md (criterion 29 scope, citation, checker coverage)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| R29-1 | draft cites nonexistent lesson/checker path, misdescribes fixture provenance | FIXED | `QUALITY.md:232` cites `lessons/round-20.md#mistakes M2` (exists, `round-20.md:16`); checker `isolation-check.sh` |
| R29-2 | checker does not cover "every arming step" | FIXED-PART | six modes `isolation-check.sh:66-147`; per-target independent arms beyond partial-arm not added |
| R29-3 | non-duplication with 21/26/24/27/28 | FIXED | pre-registration and `SCORECARD.md:1272-1273` |
| R29-4 | counter c1 compatibility | FIXED | [V] measure c1 = 22/30 |
| R29-5 | red evidence faithful to incident | FIXED | `round-20.md:16`; `evidence/crit29-inns-r19-shape.txt` [R] |

## 9. RevCriterion30.md (criterion 30 duplicate; S096 unlike; anchor)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| R30-1 | proposed core duplicates criterion 10 | FIXED | `SCORECARD.md:1287-1297` withdrawn; `round-20.md:17` |
| R30-2 | S096 red compares unlike revisions and rules | FIXED-PART | see C2-2 |
| R30-3 | narrowed predicate line (claim_revision, population, predicate) | NOT-ACTED | `tally-claims.json` has no `claim_revision`/`population` field; `QUALITY.md:249-259` new 30 is detector precision, not the predicate clause |
| R30-4 | 155 vs 154 grounded | FIXED | `round-20.md:69-73`; [V] red 154 vs 155 |
| R30-5 | ten vs nine/eight grounded | FIXED | `round-20.md:74-75`; [V] red |
| R30-6 | lesson anchor M2 vs M3 | FIXED | `round-20.md:17` |

## 10. RevHarmWatchLimits.md (worktree SCORECARD block; worktree ledger)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| RH-1 | harm-watch executes worktree SCORECARD block while claiming REV | FIXED | `harm-watch.sh:7-9` "Navigation uses the REV-pinned SCORECARD bytes, never an unpinned worktree block"; `:37-62` REV resolution (not exercised by this seat) |
| RH-1b | harm-watch runs the extracted block without a pinned digest (L4) | NOT-ACTED | `harm-watch.sh:396-415` `bash -s < $src#Counting-command`; no `8b59b503…` check (grep) |
| RH-2 | supersede-sweep reads its ledger from the worktree | KEPT | not invoked by `harm-watch.sh` (grep); `w1/reports/HarmWatch20.md:38`; NOT recorded as an open row in landed `round-20.md` or SCORECARD |

## 11. RevLeadExitSemantics.md (lead placement; consumers; uncommitted instruments)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| RL-F1 | Design A: leads stay in findings | FIXED | `round-20.md:83-85`; [V] lead rows in `findings`, exit 1, `observed_findings`/`lead_findings` present |
| RL-F2 | P/H demotion invisible under a separate list | FIXED | design A adopted |
| RL-F3 | frozenset harm removed by purity, not tagging | FIXED | [V] `BLOCK=frozenset(['pacman','-Q','hyprland'])` → no row (fixture `rule.jsonl` line 1); `SCORECARD.md:1329` P 66/66 |
| RL-F4 | consumer census (tw-recall, tw-precision, corpus-diff, selftests, frozen replay, verdict label) | FIXED-PART | frozen replay: `SCORECARD.md:1330` r19 `frozen_match` holds; r18 mismatch disclosed |
| RL-F5 | report obligations (repaired by removal; split reported; r14:2,3 classification) | FIXED-PART | `round-20.md:15-16`; r14:2,3 classification not restated (recall-split-final shows totals only) |
| RL-F6 | round-20 instruments uncommitted at e629f73 | FIXED | committed f3da504 (before tool edit 28c6837); `git ls-tree a4046a8 .ufo/waves/round-20/` lists `tw-precision.py`, `tw-recall-split.py`, `corpus-diff.py` |

## 12. RevNoHarmPlan.md (no-harm guards, evidence contract, compatibility)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| RN-1 | precision gate accepts unmarked candidate row | KEPT | `tw-precision.py:87` default `observed`; disclosed `round-20.md:18` |
| RN-1b | counts not validated against rows; split reporter non-rejecting | NOT-ACTED | `tw-precision.py` verdict checks (no reference to `observed_findings`/`lead_findings`, grep); `tw-recall-split.py` prints totals |
| RN-2 | "added rows classed" ≠ harmless (rule-B class-only test) | PENDING | `SCORECARD.md:1330` "pending (wave 2)" |
| RN-3 | exit flips 0→1 for lead-only inputs; CLI schema change | NOT-ACTED | `mado-tripwire-verdict-v1` string unchanged with added keys; no per-input old/new exit table; `SKILL.md:542-552` describes leads but not the flip |
| RN-4 | runtime non-regression unbounded | NOT-ACTED | no timing receipt in landed bytes |

## 13. RevPrecisionCounterSpec.md (suite size, suite-rev, baseline)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| RP-1 | undersized/duplicated suite scores 10/10 | FIXED-PART | per-family minimum 4 enforced `tw-precision.py:116,158-162`; total N and duplicate content not checked |
| RP-2 | `--suite-rev` bypasses landing pin | NOT-ACTED | `tw-precision.py:63-68` override accepted; resolved pin printed `:224-237` (auditable, not rejected) |
| RP-3 | baseline red/clean not enforced by the counter | KEPT | counter run at both old revs and recorded (`evidence/precision-1f7f995.txt`, `-9c54c56.txt`) but not an enforced guard |

## 14. RevR19V2Wording.md (S096 append-only correction)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| R2-1 | stale 5/13 in SCORECARD:1167, lesson:108, LOG:1323-1325 | RELOC | correction block in `round-20.md:61-68` and `LOG.md:1340-1361`; original lines unchanged (append-only) |
| R2-2 | SCORECARD C2 summary (:1133) reads as all-13 S096 coverage | NOT-ACTED | `SCORECARD.md:1133` unchanged; no correction block in SCORECARD |
| R2-3 | "Corrections" carrier in SCORECARD | FIXED-PART | `SCORECARD.md:1333-1334` points to the lesson; no SCORECARD correction section |
| R2-4 | five S090-only paths + provenance-not-behaviour limit | FIXED | `round-20.md:63-68` |
| R2-5 | do not rewrite RerunC2 / closure | FIXED | `git diff e629f73 a4046a8` shows no round-19 wave or closure edits |

## 15. RevR19V4Wording.md (incident record; 155/154; fail-open qualifier)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| R4-1 | `round-19.md:123-130` 155 stale | RELOC | `round-20.md:69-73` (154 files); `round-19.md` unchanged |
| R4-2 | M12 row omits fail-open outcome | RELOC | `round-20.md:16` M2 row states the fail-open and captured-by none |
| R4-3 | "no live recheck" / host state unmeasured qualifier | FIXED-PART | `round-20.md:72-73` "host state after it was not independently measured"; no-live-recheck clause absent |
| R4-4 | proposed append block at `round-19.md:160` | NOT-ACTED (by design: relocated) | `round-19.md` not edited |

## 16. RevR19V5Wording.md (ten → nine/eight)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| R5-1 | SCORECARD:1225 "ten old OM10 assertions" | RELOC | `round-20.md:74-75`; SCORECARD:1225 unchanged (append-only) |
| R5-2 | fleet report `.ufo/reports/round-19/mado.md:109-110` repeats "ten" | OUT-LANE | outside the lane; not writable by this wave |

## 17. RevR19V6Seats.md (reportless seats; relative paths)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| R6-1 | M9 credits 25 reportless seats collectively | FIXED-PART | `round-20.md:76-77` "25 without a report", "dead seats stay uncredited"; individual names not listed |
| R6-2 | relative `reportDir`/`Report:` resolves to fleet root | FIXED | `round-20.md:78-79` absolute lane paths in every item; wave-2 context names absolute paths |

## 18. RevRecallControls.md (6/6 = row presence)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| RC-1 | 6/6 is row-presence, one lead | FIXED | `SCORECARD.md:1330`; `SKILL.md:550-552` |
| RC-2 | tw-recall ignores evidence field | KEPT | `SCORECARD.md:1330` uses tw-recall-split for the split; tw-recall unchanged (registered) |
| RC-3 | 20 control lines, 0 findings | FIXED-PART | `SCORECARD.md:1330` "20 control lines 0 findings"; [R] `evidence/recall-final.txt` not re-read by this seat |

## 19. RevSkillTripwireText.md (SKILL / docstring wording)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| RS-E1a | SKILL:530-531 "a finding is an issued command to disclose" | NOT-ACTED | `SKILL.md:531` text still present |
| RS-E1b | SKILL:591-593 "records commands issued" | NOT-ACTED | `SKILL.md:622` "It records commands" still present (new text at `SKILL.md:546-560` is additive) |
| RS-E1c | tool docstring "issued" | KEPT | `tools/mado-tripwire.py:4` "Classifies commands a seat *issued*"; `:27-28` "Observed means issued, not necessarily executed" (grep) |
| RS-E1d | counts (observed/lead) named in the reporting step | FIXED | `SKILL.md:550-552` |
| RS-E1e | blind spots (aliases, cross-cell helpers) | FIXED-PART | `tools/mado-tripwire.py:37-38` (cross-cell helpers) and `:49-54` |
| RS-E2/3 | rule B / pure-call prose | FIXED | `tools/mado-tripwire.py:49-60`; `tripwire-precision-r20.md:14-20` |
| RS-E4 | vcs_write help/dry-run prose | FIXED | `tools/mado-tripwire.py:59-90`; `SKILL.md:553-560`; `tripwire-precision-r20.md:37-60` |
| RS-round19 | SKILL:1877-1878 "heuristic lead" historical note | FIXED | historical text kept (`SKILL.md:1909`) |

## 20. RevSpecRuleB.md (E1–E3 pure guard, bindings, alias, helper, exec)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| RB-1 | name-only pure guard erases leads after `import *`/globals/exec | FIXED | `tools/mado-tripwire.py:1366-1371`, `:1391` import * invalidates; [V] `from x import *` + frozenset → lead (`rule.jsonl` line 3) |
| RB-2 | `del`/reset → lead contradicts builtin fallback | FIXED-PART | `tools/mado-tripwire.py:1343`, `:1588-1591` Delete handled; reset-to-builtin [UNK] (not tested) |
| RB-3 | `run = subprocess.run` alias must be observed | FIXED | [V] `print = subprocess.run; print([...])` → observed (`rule.jsonl` line 4); `tripwire-precision-r20.md:18` |
| RB-4 | local alias / partial inside a def | FIXED-PART | `tripwire-precision-r20.md:18` (partial via W family); not re-run here |
| RB-5 | cross-cell helper bodies not carried | FIXED | `tools/mado-tripwire.py:37-38`; `tripwire-precision-r20.md:18` (W-WrapperCrossCell-r13-verbatim) |
| RB-6 | async/lambda/decorated helpers not resolved | FIXED-PART | docstring `tools/mado-tripwire.py:37-41` (async needs direct await; lambdas); decorated not stated |
| RB-7 | stale helper table across rebinding | FIXED | `tripwire-precision-r20.md:30-33` binding in effect at the call |
| RB-8 | `frozenset`, `type` missing from pure set; `from shlex import quote as q` | FIXED | `tools/mado-tripwire.py:1396-1400` (frozenset, type); [V] `q(['pacman','-Q'])` → no row (`rule.jsonl` line 6) |
| RB-9 | `exec`/`eval` treated as pure; string bodies not parsed | NOT-ACTED | `tools/mado-tripwire.py:1405` lists `exec`, `eval`, `compile` in PURE_ARG_CALLS; [V] `fx/exec.jsonl`: `exec("subprocess.run(['pacman', '-Q'])")` and `eval("__import__('subprocess').run(['pacman','-Q'])")` → `MADO_TRIPWIRE: clean`, exit 0, `eval_unparsed 0`; the limit is not listed in `tripwire-precision-r20.md:82-93` |

## 21. RevSpecVcsHelp.md (help under `--`, invocation-local help)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| RV-1 | help recognised only before `--`, invocation-local | FIXED | `tools/mado-tripwire.py:570` `before_dashdash`; docstring `:72-76`; [V] `git --help commit` clean, `git commit -n -h` clean |
| RV-2 | `jj diff -- --help` is a path, not help | FIXED | [V] `jj diff -- --help` → `vcs_write jj:diff observed` (snapshot read is a write; not classed as help) |
| RV-3 | `git clean -n` dry-run wording | FIXED | `clean` excluded from class; no change needed (`tools/mado-tripwire.py` docstring) |

## 22. RevSuitesLeadEdits.md (two legacy lead markers)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| RL2-1 | `py-lead-cross-cell-literal` expectation must carry `lead` | FIXED | `.ufo/waves/round-19/tripwire/r19-helperfn/expected.json` (67 changed lines in the landed diff) `[{"class":"package_query","rule":"pacman:-Q","line":1,"evidence":"lead"}]` [R] |
| RL2-2 | `py-lead-two-calls` expectation must carry `lead` | FIXED | same file, `pacman:-Qi` `"evidence":"lead"` [R] |
| RL2-3 | no VCS help/dry-run row to drop | FIXED | no edit needed |

## 23. RevengeInnsHarness.md (fidelity of the red artifact)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| RI-1 | inns-r19-shape.sh faithful to control-flow only, not byte-for-byte | FIXED-PART | `round-20.md:16` "the round-19 shape" (no byte claim); the `--map-root-user` qualification is in `w1/reports/IsolationHarness.md` only |
| RI-2 | historical script recovered from transcript (no bytes on disk) | KEPT | not restated in landed prose |

## 24. RevengeRuleBIntent.md (lead marker lost)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| RRB-1 | rule-B rows carry the same shape as observed | FIXED | every row carries `evidence` ([V] rows show `observed`/`lead`); `round-20.md:18` M4 |
| RRB-2 | lead label lived only in prose | FIXED | `tools/mado-tripwire.py:49` docstring + field |

## 25. RevengeVcsHelpIntent.md (`jj log --help` vcs_write)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| RVH-1 | `jj <sub> --help` classified as write | FIXED | [V] `jj log --help` → clean (`vcs.jsonl` line 1); `tools/mado-tripwire.py:570-620` (help flag before `--`, `JJ_HELP_FLAGS` `:161`) |
| RVH-2 | no regression fixture for subcommand help | FIXED-PART | H family includes help forms (`SCORECARD.md:1329` H 51/52); the exact `jj log --help` case id not checked [UNK] |

## 26. ConnCriteriaFleet.md (count rule is already fleet/criterion 10; 155 pair)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| CF-1 | criterion 30 first clause restates 10 / CORPUS.md:34-38 | FIXED | withdrawn, `SCORECARD.md:1287-1297` |
| CF-2 | keep the predicate clause (which command, which predicate) | FIXED-PART | predicate clause lives in lesson M3 and `tally-check.py` `claim=`/key output; not in a numbered QUALITY line |
| CF-3 | drop "receipt entries vs transcript files" pair | FIXED | no such pair in landed text; 155 is red |
| CF-4 | cite lesson paths that exist at landing | FIXED | `QUALITY.md:232`, `:249` cite `round-20.md` (exists) |
| CF-5 | no third numbered line | FIXED | QUALITY adds two numbered lines (29, 30) only (`corpus/QUALITY.md` diff +43) |
| CF-6 | criterion 21 / pause untouched | FIXED | QUALITY diff is additions at 226+ only |

## 27. ConnFleetHarmPattern.md (frozen historical ledger)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| CFH-1 | red rows pinned to historical blobs; correction = appended green row | FIXED | `tally-claims.json` reds at `1f7f995`, greens at REV (`round-20.md:61-75`) |
| CFH-2 | five rows (155, S096 any-line, S096 first-line, OM10 occurrences, OM10 distinct) | FIXED-PART | red rows: 155, first_line (x3), OM10 occurrences; no any-line red; no OM10 distinct row |
| CFH-3 | `tools/mado-tripwire.py` byte-identical for C2 | N/A | C1 tool repair landed (`9613f510`); checker is a separate file (`tally-check.py`) |
| CFH-4 | ledger must not live in the C1 counter | FIXED | separate `tally-check.py` |
| CFH-5 | green entries read live lesson | KEPT | green statements read at REV (by design; `tally-check.py` REV rule) |

## 28. ConnQueueMapping.md (R19-V* ownership)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| CQ-1 | R19-V5 tail (worktree ledger, harm-watch provenance, anchor-alias) has no owner row | NOT-ACTED | no keep-open row in `SCORECARD.md:1228-1343` or `round-20.md` (grep: no `anchor-alias`, `worktree` in landed round-20 prose) |
| CQ-2 | R19-V4 triple-owned | KEPT | by design: `QUALITY.md:232`, `round-20.md:69-73`, `SCORECARD.md:1276-1279` |
| CQ-3 | R19-V2 two buckets | KEPT | `round-20.md:61-68`, `SCORECARD.md:1331` |
| CQ-4 | R19-V6 byte-equality unnamed | NOT-ACTED | `round-20.md:76-79` covers absolute paths, dead seats, provider recovery; byte-equality-as-lane-evidence absent |
| CQ-5 | round-19 planned tool-honesty holes vs "fixed" latest-alias contradiction | NOT-ACTED | `round-19.md:151-152` not reconciled in landed text |

## 29. ConnSiblingClassifiers.md (per-command help/dry-run walk)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| CSC-1 | per-command flag walk (stop on exact help) | FIXED | `tools/mado-tripwire.py:641-677` `classify_git` help/dry-run per verb |
| CSC-2 | `-n` split per command (commit -n write; add/push -n dry) | FIXED | `tools/mado-tripwire.py:203-205` GIT_DRY_NEGATIONS; [V] `git add -n .` / `git push -n` clean, `git commit -n -m x` write |
| CSC-3 | `--dry-run` on `jj git push` stays a write | FIXED | [V] `jj git push --dry-run` → `vcs_write jj:git observed` |
| CSC-4 | `git commit -m --help` stays write | FIXED | [V] `git commit -m --help` → `git:commit observed` |
| CSC-5 | leads as findings with evidence at exit 1 | FIXED | `round-20.md:83-85` |
| CSC-6 | do not copy sudo `-h` table | N/A | `tools/mado-tripwire.py:140` keeps `SUDO_ARG_OPTS` |
| CSC-7 | clustered git shorts (`-nh`) and `git commit -h` extra operands | KEPT | not executed; `tripwire-precision-r20.md:37-60` states exact tokens only |

## 30. ConnSiblingIsolation.md (criterion 29 red/green fixtures)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| CSI-1 | red: incident list `[ -e ] && mount && echo` | FIXED | `evidence/inns-r19-shape.sh`; `evidence/crit29-inns-r19-shape.txt` FAIL_OPEN [R] |
| CSI-2 | red: sibling else-branch (`|| exit` only on the true branch) | NOT-ACTED | no such mode in `isolation-check.sh:66-147` |
| CSI-3 | red: skip returns 0 without canary | FIXED | `isolation-check.sh:135` SKIP_AS_SUCCESS → FAIL_OPEN |
| CSI-4 | green: one sequence `|| exit 125` then canary | FIXED | `isolate.sh:56-61`; `evidence/crit29-isolate.txt` FAIL_CLOSED [R] |
| CSI-5 | score status + canary, not the token | FIXED | `isolation-check.sh:119-135` verdicts from exit and canary |
| CSI-6 | repaired `[ -e ] || continue` shape needs an existing target + failing mount | FIXED-PART | `isolation-check.sh:146` missing-target and `:66-88` mount-nonzero are separate arms |

## 31. ConnSourcesOverlap.md (census key discipline; SOURCES S099+)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| CSO-1 | open new ids; no sibling citation; no `supersedes` | FIXED | `corpus/SOURCES.md:111-124` S099–S112 new; no `supersedes` |
| CSO-2 | exactly one https URL in each source cell | NOT-ACTED | [V] count of `https://` in the title/URL cell: S104=2, S107=2, S108=2 (`corpus/SOURCES.md` S104 `push.rs and …cli-reference@.md.snap`; S107/S108 `(also https://…Lib/…py)`); census keys only the first |
| CSO-3 | git help keyed on `git.c` raw tag URL | FIXED | S102 `raw.githubusercontent.com/git/git/v2.56.0/git.c` |
| CSO-4 | unshare row keyed on tag, not peeled OID | NOT-ACTED | S109 key `…/util-linux/util-linux/d76cbf8f13e65ff657344f7f6a90042cf755ba59/sys-utils/unshare.1.adoc` (peeled commit) |
| CSO-5 | bash row = post-redirect cgit URL | FIXED | S110 `cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?h=bash-5.3` |
| CSO-6 | python raw tag URLs, not `latest`/tree | FIXED | S105–S108 `raw.githubusercontent.com/python/cpython/v3.14.8/...` |
| CSO-7 | jj tag name, not `latest` | FIXED | S103/S104 `…/jj-vcs/jj/v0.45.1/...` |
| CSO-8 | census re-run (`validate`/`shared`) after rows land | NOT-ACTED-by-seat | not run here (fleet script, 21 roots); [UNK] |

## 32. SentinelFixtures.md (secrets / copied transcript lines)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| SF-S1 | copied real transcript lines (credentialId, thinkingSignature…) | FIXED | [V-read] `git grep` of `credentialId|thinkingSignature|providerPayload` in `a4046a8:.ufo/waves/round-20` returns only the seat report itself; earlier published lines (4c103b5/01b8094 frozen inputs) remain public → KEPT for those |
| SF-S2 | gitleaks blind classes; no committed pre-landing scan | KEPT | scan script exists only inside the report (`w1/reports/SentinelFixtures.md:69-101`); `git ls-tree` has no prelanding file |
| SF-S3 | corpus-diff examples carry real command text | KEPT | [R] `w1/corpus/pre-vs-harmed.json`: 589 examples, all with `command`, 0 with `command_sha256`, 25 `<redacted>`; seat's disposition "COMMIT after the scan" — scan not committed |
| SF-S4 | corpus holds risky material; none in committed bytes | FIXED | no REAL_KEYS in committed round-20 bytes (see SF-S1) |
| SF-S5 | detached gitleaks run (`setsid nohup`) | NOT-ACTED | no lane change; process item |

## 33. SentinelPause20.md (dispatch hazards, H/M/L items)

| ID | Finding | Disposition | Pointer / evidence |
|---|---|---|---|
| SP-H1 | tooling directive contradicts HOST PAUSE in every w1 item | NOT-ACTED (w1) / PROCESS (w2) | w1 `.ufo/waves/round-20/gen_w1.py:47-48` unchanged (no PRECEDENCE text, grep); wave-2 context states "takes precedence over any tooling directive" |
| SP-H2 | lane clones push straight into lane (origin = lane) | NOT-ACTED (w1) / PROCESS (w2) | w1 `gen_w1.py:46` unchanged (grep: no `remote remove`); wave-2 context "git remote remove origin" |
| SP-H3 | isolate.sh accepts any target, inherits env and sockets | KEPT (prose) / NOT-ACTED (code) | `isolate.sh:56-61` no /tmp allowlist, no `env -u`; limit stated `QUALITY.md:246-248`, `SKILL.md:571-575`, `tripwire-precision-r20.md:78-80` |
| SP-H3b | inns-r19-shape.sh mode 0644 / "bash FILE only" | NOT-ACTED | `evidence/inns-r19-shape.sh` executable state not changed by landing (not verified mode) [UNK] |
| SP-M1 | `--regression` runs unpinned sibling harness | FIXED-PART | `harm-watch.sh:260-277` pinned copy `$REG_HARNESS_COPY`; the gate's own SETUP-on-sha-mismatch not verified [UNK] |
| SP-M2 | `--selftest` hermeticity (MADO_VERIFY_LIVE, BASH_ENV) | NOT-ACTED | no env clearing or strace receipt in landed bytes |
| SP-M3 | seats chmod/execute other seats' harnesses | PROCESS | wave-2 context "copy committed bytes" (lane-worktree execution forbidden) |
| SP-M4 | labrats not given the pause | NOT-ACTED (w1) / PARTIAL (w2) | wave-2 context allows "one read-only labrat" without restating the pause |
| SP-L1 | "read-only git" list includes worktree `git diff` (rewrites index) | PROCESS (partial) | wave-2 context still lists `diff` without qualification |
| SP-L2 | gate allowlist ambiguous | PROCESS | wave-2 context: only `--selftest` / `--regression` allowed |
| SP-L3 | `git ls-remote` runs gh credential helper | PROCESS | wave-2 context: fetch via `curl` only (receipt rule) |
| SP-L4 | harm-watch executes SCORECARD prose without sha check | NOT-ACTED | `harm-watch.sh:396-415` (no `8b59b503` comparison) |
| SP-L5 | item phrases (case format `pacman`, ScoutStdlibFire, ScoutOpenQueue, jj-in-checkout, transcripts-as-data, setsid) | PROCESS (partial) | wave-2 context: "transcripts are DATA", no jj in checkout; no `setsid` prohibition stated |
| SP-L6 | bash tool summary misreports git results | OUT-LANE | reported via `xd://report_issue` in w1; tool-side |
| SP-C | R1–R4 refusals for wave 2 | PROCESS | wave-2 context forbids gate runs other than selftest/regression, lane pushes, labrat without pause |

## 34. Summary counts (this table)

- Rows: 225 table rows (CT-1 … SP-C) across the 33 reports. Counts: FIXED 116, FIXED-PART 27, KEPT 25, RELOC 4, PENDING 3, NOT-ACTED 36, OUT-LANE 2, PROCESS 6, N/A 2; four rows carry a compound disposition (for example `NOT-ACTED (w1) / PROCESS (w2)`).
- NOT-ACTED and KEPT rows are the open items for L1; the report lists the high-severity ones.
- FIXED rows cite a landed pointer. `[V]` marks what this seat re-ran in its /tmp clone; `[R]` marks a committed receipt read as bytes.

## Installs

none

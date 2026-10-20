# ConnQueueClose — partly falsified: V5's keep-open tail is off the round-20 queue, and the criterion-29 red harness is mode 100644 so a clean tree exits 2

Axes used: mapping completeness (every R19-V1..V6 disposition, including the V5 tail), evidence fidelity (committed bytes and commands run here), disposition accuracy (closed / kept open / unowned), scope safety (this report only). Tip `a4046a8216080d4004de3f268c62cf142095ac07`. Closure text `corpus/lessons/round-19-verifier-spotcheck.md:145-155` (sha256 `dcb7a9134022e010ef357a095ded13d15d6f77a9090dc2976f0c9d8090fea0a0`). Round-20 lesson sha256 `bf55c34db05e47a1499e67567df0d2a8841a4337da26c25a46a10c03e1e324e0`. Checks ran in `/tmp/mado-r20w2-ConnQueueClose` (clone of the lane, origin removed); that clone was returned to `a4046a8` with a clean worktree.

The lesson header `corpus/lessons/round-20.md:56` says the section disposes closure R19-V1..V6. The bullets under it are V1, V2, V4, V5 (OM10 count only), and V6. V3 is the tool repair in M1, not a correction bullet. The V5 sentence the closure required to stay queued — worktree ledger, harm-watch execution/provenance, anchor-alias checker limits — is absent from `round-20.md`, from `SCORECARD.md` "Round 20 — declared claims" (`:1276-1280` names V5 as the nine/eight count only), and from `LOG.md:1357-1358`. The same limits are still named as round-20 work in the older plan `SCORECARD.md:1213-1216`, and `corpus/lessons/round-19.md:151-152` still says the alias false-green is a "round-20 fix". That fix did not land: `anchor-durability.py` blob `f15279e117076936aee1b950ba7cb6b0e817ff44` is identical at `b435568` and `a4046a8`.

## Disposition

| ID | Status | Landed artifact |
|---|---|---|
| R19-V1 | closed | Miss stays a miss. `measure.py` at `28c6837` is still `{"criteria": 28, "lesson_cited": 20, "score": 7.1429}`. At `a4046a8` it is `{"criteria": 30, "lesson_cited": 22, "score": 7.3333}`. Round-19 SCORECARD still records the missed ≥21/29 target (`SCORECARD.md:1132`). Duplicate count-criterion 30 is **withdrawn** in `SCORECARD.md` at `f3da504` (before tool commit `28c6837`); `^30\. ` is absent from `QUALITY.md` at `e629f73`, `f3da504`, and `28c6837`, and present once at `4362219` and `a4046a8` as detector-precision 30′ (`QUALITY.md:249`). |
| R19-V2 | closed | Stale 5/13 corrected; all-file S096 promise recorded as unmet. `tally-check.py --set red --expect` at `a4046a8`: `EXPECT_SUMMARY: 5/5`, including three `stated=5/13 derived=6/13` rows. `--set green --expect`: `EXPECT_SUMMARY: 4/4`, `r20-lesson-s096-first-line` 6/13 and `r20-lesson-s096-any-line` 8/13 on `round-20.md:62`. Re-derived at the tip (`pointer-token --rev a4046a8`): `first_line=6/13 any_line=8/13`; the five S090-only files are unchanged vs `1f7f995` (empty `git diff --stat`). `a4046a8` only moves the word S096 onto that tally sentence so the checker's token binding can see it; the fractions come from `fresh-pins.py`. |
| R19-V3 | closed | The closure's ordinary finding on pure data is gone, leads are marked, recall and controls hold. Residuals below do not restore that finding. |
| R19-V4 | kept open | The incident record and `isolate.sh` fail-closed path landed. The committed red harness does not replay the receipt. |
| R19-V5 count | closed | Nine labeled OM10 occurrences, eight distinct; replacements OM10A six and OM10B eight. |
| R19-V5 worktree ledger | unowned | `supersede-sweep.py` still loads `supersessions.json` from the worktree. No round-20 owner, criterion, or keep-open sentence. |
| R19-V5 harm-watch provenance | kept open | `.ufo/waves/round-20/harm-watch.sh` reads the SCORECARD block from `git show` bytes. Execution still runs the worktree path; the round-19 runner is unchanged; no tip receipt is committed; the queue does not restate the residual. |
| R19-V5 anchor-alias limits | unowned | Checker blob unchanged. A `latest` URL plus a version token is `durable`. Malformed receipts still exit 1 or are skipped. |
| R19-V6 | closed | 25 reportless round-19 members stay uncredited; absolute lane paths are in the committed wave-1 context and the lesson; QualityDraft files remain. |

### R19-V1 — closed

Required: keep ≥21/29 a miss, do not add a duplicate criterion or rewrite the target, and pre-register any next calibration claim. `corpus/lessons/round-20.md:58-60` and `SCORECARD.md:1272-1273` and `:1333-1334` do that. `python3 -I .ufo/waves/round-17/measure.py 28c68378eccbd5f227cdc28a62406ff390e3540a` prints c1 `20/28 = 7.1429`. The same command at `a4046a8216080d4004de3f268c62cf142095ac07` prints `22/30 = 7.3333`. `git grep -n withdrawn f3da504 -- SCORECARD.md` hits `:1295` ("registered 30 is **withdrawn**") and `:1300` (30′). That commit is an ancestor of the tool commit. `QUALITY.md` gains numbered 29 and 30 only at `4362219`, after the tool repair, matching the scorecard text that was already corrected.

### R19-V2 — closed

Required: reconcile the all-file S096 promise with the tip, and replace the stale 5/13 with any-line 8/13 and first-line 6/13. `round-20.md:61-68` names both fractions, the five files (`arc-synthesis.md:392`, `closeout-r11.md:299`, `config-health-report-r3.md:1009`, `waybar-walker-plane.md:479`, `waybar-walker-semantics.md:467`), and says the promise is unmet and that S096 is provenance. Checker (`tally-claims.json` sha256 `81eed3ebe33ec0bd2a7adbb5077c51a2624e00bccd945df83477f21674b3a48d`, checker sha256 `21ce9dd57a47d975623aa9ca2bf53c3dadb8fa68b6f066a92461edba2fd2aea4`):

```text
python3 -I .ufo/waves/round-20/tally-check.py .ufo/waves/round-20/tally-claims.json --set red --rev a4046a8… --expect
TALLY_SUMMARY: set=red n=5 match=0 mismatch=5 error=0
EXPECT_SUMMARY: 5/5
RED_EXIT:0

python3 -I .ufo/waves/round-20/tally-check.py … --set green --rev a4046a8… --expect
MATCH r20-lesson-s096-first-line stated=6/13 derived=6/13
MATCH r20-lesson-s096-any-line stated=8/13 derived=8/13
EXPECT_SUMMARY: 4/4
GREEN_EXIT:0
```

`pointer-token` at `a4046a8` repeats `first_line=6/13 any_line=8/13 current=13/13`. The historical "5/13" lines in `round-19.md:108`, `SCORECARD.md:1167`, and `LOG.md:1324` are still the append-only originals; the red set mismatches them to 6/13 under the first-line rule.

### R19-V3 — closed

Required: repair rule-B precision, mark leads, cover pure containers, binding/shadowing, wrapper misses, and help/dry-run nonwrites in red-before fixtures, and keep six-line recall and the controls. Tool sha256 `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c` at `a4046a8` equals the receipt pin.

```text
python3 -I .ufo/waves/round-20/tw-precision.py a4046a8216080d4004de3f268c62cf142095ac07
PREC_EXIT:0
families P 66/66 S 17/17 W 21/22 H 51/52 L 17/18 score 9.8286
P-CasePureBuiltins-frozenset-closure pass True got {exit:0, findings:[]}
fails: W-CaseWrapperForms-class-method-instance, L-AdoptW2-AdvHelperFn-b14, H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help

python3 -I .ufo/waves/round-19/tw-recall.py a4046a8…
incident_lines 6 detected 6 score 10.0 tool 9613f5100540

python3 -I .ufo/waves/round-20/tw-recall-split.py a4046a8…
detected_observed 5 detected_lead 1 detected_unmarked 0 undetected 0
control_lines 20 control_findings 0
```

`SKILL.md:542-563` defines `evidence: observed|lead` and says pure data gives no row. The three suite misses are the pre-registered 175/175 miss already in `SCORECARD.md:1329` (a true detection the case called a miss, a variable-verb `jj … --help` kept as a write, one unimplemented lead). The whole-corpus added-row diff vs `9c54c56` is still "pending (wave 2)" at `SCORECARD.md:1330`. This seat did not run `corpus-diff.py`, so out-of-suite no-loss is [UNK] here. That does not put the frozenset ordinary finding back.

### R19-V4 — kept open

The record half is closed. `tally-check` green `r20-lesson-154-files stated=154 derived=154`. `round-20.md:69-73` says the scan did not see the probe, captured-by is `none (seat self-report)`, and host state was not re-measured. `SKILL.md:562-563` and `:626-627` still say scripts written then run are unanalysed. `isolate.sh` is mode `100755` blob `91c57ab…`. Re-run from the clean clone:

```text
bash .ufo/waves/round-20/isolation-check.sh .ufo/waves/round-20/isolate.sh
FAIL_CLOSED mount-nonzero, unshare-refused, mount-noop, partial-arm, missing-target, missing-stub
POSITIVE_CONTROL_OK isolate.sh
ISO_EXIT:0
```

The red half does not replay. `inns-r19-shape.sh` content blob `26f037748f7b37012bec56579bb9ecad258edca6` is mode `100755` at `f3da504` and `28c6837`, and mode `100644` at `4362219` and `a4046a8` (`git diff --summary 28c6837 a4046a8` is `mode change 100755 => 100644`). `isolation-check.sh:11-13` exits 2 when the harness is not executable. Clean clone:

```text
bash .ufo/waves/round-20/isolation-check.sh .ufo/waves/round-20/evidence/inns-r19-shape.sh
COULD_NOT_EVALUATE inns-r19-shape.sh (not executable)
INNS_EXIT:2
```

The committed receipt `.ufo/waves/round-20/evidence/crit29-inns-r19-shape.txt` (sha256 `6b2baa25e082a751da2680980176125d7234babdbcc8cbf5dae6479876030c8c`) is added in that same `4362219` range (`git diff --numstat 28c6837 a4046a8` is `59 0`) and ends `exit=1` with five `FAIL_OPEN` lines. After `chmod +x` in the clone only (then cleared; index remains `100644`):

```text
X_EXIT:1
FAIL_OPEN mount-nonzero, mount-noop, partial-arm, missing-target, missing-stub
FAIL_CLOSED unshare-refused
POSITIVE_CONTROL_OK
```

So the script bytes still fail open, and a checkout of `a4046a8` does not show that. `QUALITY.md:237-239` cites that receipt as the red. `isolate.sh` is not a sandbox; `SKILL.md:569-571` says the environment and compositor sockets stay reachable. That limit is disclosed and matches the closure's "do not re-exercise a host probe" rule. This re-run used `/tmp` canaries only.

### R19-V5 count — closed; tail — unowned or kept open

OM10. `tally-check.py selftest-labels --old 9c54c56… --new 7b4839d… --label-id OM10`:

```text
removed_occurrences=9
removed_distinct=8
removed_other_id_occurrences=0
added_by_id=…OM10A:6,OM10B:8…
```

Green entry `r20-lesson-om10-nine stated=9 derived=9` on `round-20.md:74-75`. The green registry binds `removed_occurrences` only; `removed_distinct=8` is in that same command's stdout. `round-20.md:74-75` does not mention the keep-open tail.

The tail is the closure sentence at `round-19-verifier-spotcheck.md:153` plus the lane lesson it points at, `round-19.md:111-116` and `:151-152` (sha256 `da9d8a87a2fe79bc9bf3614e3d29412b39abb4a5affa33a89a77dd6a7afbcdf6`). Those files have an empty diff from `1f7f995` to `a4046a8`.

**Worktree ledger — unowned.** `supersede-sweep.py:43-44` and `:66-70` open `DEFAULT_LEDGER` from the script directory before `git show` of the corpus. `SKILL.md:604` still says the probe "reads committed bytes via `git show` only". In the clone, with the worktree ledger's `walker-2.17.2` rows set to `["S001"]` and `git show a4046a8:.ufo/waves/round-19/supersessions.json` still `[['S090','S096'],['S097'],['S098']]`:

```text
python3 -I .ufo/waves/round-19/supersede-sweep.py a4046a8216080d4004de3f268c62cf142095ac07
supersede-sweep: walker-2.17.2 … files=13 pointed=0 stale=13
MUT2_EXIT:1
STALE SKILL.md
STALE corpus/README.md
…
```

Ledger sha256 `a0e6cfbe2f096602ce8f85132cefe37b0fdb9ddbd2f1172e46a65236d9cfb636`, blob `5bee46dab74ad273e104400111b8f5a7f6eaa21b`, identical at `b435568` and `a4046a8`. The clone file was restored; `git diff --exit-code` on it was clean. Round-20 `harm-watch.sh` does not call this probe. Nothing in the round-20 lesson or declared claims owns the fix or restates the limit.

**Harm-watch execution/provenance — kept open.** Landed `.ufo/waves/round-20/harm-watch.sh` sha256 `694e1f1afd615e846f10ead79bf94ef675a54524eea2c157d32cb652ef35a9b8` matches the w1 HarmWatch20 report's hash. `:7-9` and `:388-413` extract `### Counting command` from the `git show` copy and `pin_skip` on mismatch, which closes the round-19 "run the worktree block and only note a mismatch" path for this new runner. `:166-173` `run_pinned` still `timeout`s the worktree command after the hash check, so a later edit of that path runs under `measured_commit=REV`. Round-19 `harm-watch.sh` sha256 `077e1b4d05be67aca0587b240122f05eb2d4bb4f5955d93f368d46b0ae09238a` is the same blob as `b435568` and still executes the worktree block (`:367-393`). `git ls-tree -r a4046a8 .ufo/waves/round-20` contains `harm-watch.sh` and no `evidence/harm/` receipt. HarmWatch20's `HARM_WATCH: PASS` is a run at `e629f73`, before the tool repair. A green bounded watch at that revision does not close the limit the closure said green checks must not close, and the round-20 lesson does not keep the residual on the queue.

**Anchor-alias checker limits — unowned.** `pin_token` (`anchor-durability.py:111-134`) returns on any date, `v?\d+\.\d+` version, or abbreviated hash near the alias word, and `evaluate` (`:256-261`, `:299-300`) then calls the row durable. Real row, committed checker:

```text
python3 -I .ufo/waves/round-19/anchor-durability.py a4046a8… --rows S005
ROW S005 durable — alias segment main pinned by date 2026-01-16
S005_EXIT:0
```

S005's source cell is `…/blob/main/README.md` (`corpus/SOURCES.md:17`). Direct `evaluate()` on constructed rows (same functions, empty receipt groups): `latest` + anchor `xdg 3.0.0 documentation` → `durable — alias segment latest pinned by version 3.0.0`; `latest` with no pin token → `UNPINNED_ALIAS`. That is the limit `round-19.md:151-152` assigned to a round-20 fix.

Malformed receipts, same file, throwaway commits in the clone only (branch deleted, HEAD restored to `a4046a8`): a `receipts.jsonl` line `[1]` under `.ufo/waves/round-19/fetch/ConnQueueClose/` raises `AttributeError: 'list' object has no attribute 'get'` at `anchor-durability.py:192` and the process exits 1, the same exit as "row flagged", with a traceback. A `{` line is `bad_receipt_lines=1`, `SYN_EXIT:0`, and S005 stays durable. `round-19.md:114` ("exits 1 on a malformed receipt line") matches only the non-object branch.

Same lesson paragraph, also unowned at `a4046a8` (blobs unchanged): `frozen-repin.py:316` writes `RECEIPT tool=… tool_sha256=… utc=… argv=…` with no `measured_commit` (file sha256 `7cc8b2cdd7a74c9a2b3131c07b6b4e921d32147fedc58c86afb0027c5688517c`); `measure-mutants.py:520-525` refuses `--out` only when the path is inside `--lane`'s toplevel. For `--lane` = the clone, that predicate is false for `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/evidence/measure-mutants.json` (`clone_toplevel_contains_real_lane_out False`). This seat did not write that path.

### R19-V6 — closed

Required: keep the QualityDraft misroot lesson, absolute lane paths at seat boundaries, dead seats uncredited, provider recovery not used as claim evidence. `round-20.md:76-79` states 86 members, 25 without a report, `TwMerge` a report without a member, and absolute paths. Recount of committed `.ufo/waves/round-19/w1/reports/swarm-registry.json` `members` (86) against `*.md` report stems (62): 25 missing (the reviewer/connector/revenger/simplifier set in `w1/reports/RevR19V6Seats.md:7-13`), extra report `TwMerge`. `git cat-file -e a4046a8:.ufo/waves/round-19/drafts/QualityDraft.md` and `…/w1/reports/QualityDraft.md` both succeed. `gen_w1.py` tells seats to write the relative trailer at `{LANE}/<path>` and to use absolute paths because a relative path lands in the fleet repo (QualityDraft). `gen_w2.py` is not in `a4046a8` (`git cat-file -e` fails); it is untracked worktree text and is not a landed artifact. Round-20 `LOG.md:1360` records w1 as 85 seats, 0 dead, and does not credit the round-19 429 seats as claim evidence. The historical M9 sentence in `round-19.md:147-150` remains, append-only.

## Proposed move

Put three kept-open rows into the round-20 lesson, beside the OM10 sentence, so V5 is not read as closed: (1) `supersede-sweep.py` must read `supersessions.json` from `git show REV:…` or fail, (2) harm-watch provenance stays open until `run_pinned` executes the hashed bytes and a receipt exists at the measured tip, (3) `anchor-durability.py` must not treat a date or version token in the anchor as a pin for a `latest`/`main`/`master`/`HEAD` URL, and a non-object or syntactically bad receipt line must exit 2. In the same breath, record `inns-r19-shape.sh` as mode `100755` on the commit that carries `crit29-inns-r19-shape.txt`, so `isolation-check.sh:11-13` replays exit 1. Do not describe the SCORECARD-block change in `harm-watch.sh` as closing harm-watch provenance.

Risks: a ledger cutover can turn a green sweep red when the worktree ledger and the commit differ — that is the defect the check is supposed to catch. Restoring the executable bit does not change the script blob. A queue line that says the new harm-watch "fixed provenance" would hide `run_pinned`.

Verification already run is the command excerpts above. Not run here: `corpus-diff.py`, `harm-watch.sh` (it includes gate `--selftest`/`--regression`), and any host probe.

## Limits

- Out-of-suite tripwire no-loss vs `9c54c56` is [UNK]; `SCORECARD.md:1330` says the diff is pending.
- Synthetic alias rows were `evaluate()` calls, not committed `SOURCES.md` rows. S005 is a real mined row.
- Ledger and receipt experiments were commits and edits inside `/tmp/mado-r20w2-ConnQueueClose` only. The branch was deleted and the worktree restored to `a4046a8` (`git status --porcelain` empty). Nothing was pushed.
- `measure-mutants.py` was not executed; only the `--out` parent check was evaluated in Python.
- `frozen-repin.py` was not executed; the missing `measured_commit` is the `render_readme` format string.
- Wave-2 `gen_w2.py` is outside `a4046a8`.
- The green tally entry certifies OM10 `removed_occurrences=9`. `removed_distinct=8` was observed from the subcommand stdout, not from a separate green registry id.

## Installs

none

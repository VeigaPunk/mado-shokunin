# ConnFleetHarmPattern — mori r13 restored the lost alarm under a new name and it held; tameshi r16's stale 53/54 held only as a superseded command

Search axes: (1) every fleet `*verifier-spotcheck*` closure, (2) remedy text taken from the rejecting lesson, (3) hold read from the next lesson rather than inferred, (4) one move that can tighten mado C2 criterion 30 while leaving the tripwire byte-identical.

Walked 69 `corpus/lessons/*verifier-spotcheck*.md` files under `/home/vgpnk/Projects/shokunin/*-shokunin`. Mado round 19 is the index case (rejected-harmed for a recall gain that minted an unmarked finding on pure data, plus stale prose counts) and is excluded from "other".

## Closures that match

### Mori round 13 — detection recall dropped for structured selection

`/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-13-verifier-spotcheck.md` sha256 `e8b64126dafe00faf162218e540acdcab0f42deb14650c96a8f805e5947f8b16`.

Verdict at line 7: status `ok`, admitted `false`, `rejected-harmed`. Both bounded counters verified. The journal cutover traded away the previous OOM alarm and the fleet/non-fleet split. Independent source count (lines 77–79): `emit_finding OOM_KILL_JOURNAL crit` and `emit_finding UNIT_FAILURE_OUT_OF_SCOPE` each went 1 → 0. Line 84: structured selection is better than unsafe text matching, and it does not require discarding the OOM warning. Line 95: coverage harmed. Line 127: quality harmed; a test tally does not offset the trade.

This is the other direction of mado r19's trade. Mado bought incident recall and lost precision on pure data. Mori bought structured selection and lost alarm recall. [INFERENCE] both are the same no-trade rule; the lessons do not use one shared phrase for both directions.

Remedy, line 89 and routed item 1 (line 132): restore OOM warning/DRIFT through sourced structured metadata, with positive and negative evidence, and do not restore MESSAGE parsing. Also restore the fleet/non-fleet split (item 2).

Hold: yes, through the later spot-checks that exist.

- Round 14 (`4f7015a9c7eb311aaac38ba3403fde5767fe58994f69c681dca18283cfbd428d`), line 8: admitted. C1 is restore structured OOM critical/DRIFT, the fleet/non-fleet partition, and tsukuroi triage, while retaining six scoped counters. Line 43: user/system OOM notices go to DRIFT with one `OOM_KILL_JOURNAL severity=crit`. Line 54: `emit_finding OOM_KILL_JOURNAL crit` counts 0 → 1. Line 131: previously rejected OOM/route claims are superseded and repaired. Line 140: all six r13 repair items have landed fixes or explicit qualifications.
- Round 15 (`b65a36e1e0ae1a3010f15df206ef8ec78bd7e6aa8fa0271ff679e5fd6494083d`), line 11: admitted. Lines 113–118: `bootarray-user-kernel-oom-boot-array-current` before `0 / 0 / 0`, after `1 / 1 / 0` on rc / `OOM_KILL_JOURNAL` / signal.
- Round 16 (`6a8e706e992e86d857df1f4726c6aaa6e57e8595b0ee4fb4dd80d164ed3305be`), line 11: admitted. Line 129: prior production bytes unchanged (6/6), so the r14 census that carries the restored alarm is still the production census. Lines 220–223: a different stale wording remains — `PROVINCE.md` still calls the window probe "verification pending". That leftover is not the OOM alarm returning to zero.

### Tameshi round 16 — a stated full-page count was stale by one bucket

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-16-verifier-spotcheck.md` sha256 `5ca780d9fda123070b26faa8a6e319db6f10373d6bbc75e45238e09878d52e37`.

Verdict at lines 17–21: status `ok`, admitted `false`, rejected-harmed. C1 verifies. C2 reproduces under the lane's counting command and fails one bucket. The round-14 recipe went stale and was not swept. Lines 116–121: a re-read at `09ee1d0` would be 53/54, `box3_full_page` false, restraint score 6. The box-3 assertion ("every SKILL.md bucket … wrong expectations repaired and re-read") is stale on the bucket the round itself moved. Lines 112–113: SKILL.md:1580–1584 still state the pre-round outcomes. Lines 134–145: the registered round-14 disposition command returned 0 before the round and returns 2 `expected_input_digest_mismatch` at HEAD after it. Lines 154–155: runner gains (83/83) do not offset that, because a trade anywhere is not an improvement. Line 234: receipt `.ufo/evidence/round-16/round-gate/runner-sha256.txt` reads `89722ddb…` while the landed runner is `0673d2e5…`.

Remedy (lines 216–236):

- R16-OP1: a clean-capable live-tree verdict, via a superseding pin or by reading the historical runner from git. Red-before is the current exit 2. Historical evidence bytes stay immutable.
- R16-C2a: correct SKILL.md:1580–1584 or mark it historical, then re-read the bucket and append a ledger entry at the new section sha.
- R16-C2b: sha-only credit is blind. Record the input digests the bucket ran against and re-verify them at the measured rev.
- R16-EV1: append a dated correction for the runner sha receipt; do not rewrite the file.

Hold: the gate/recipe harm is repaired by supersession. The old command is still red on purpose.

Round 17 (`62869c87847e34d59df81140d45d459f6598841bc3a4465e88af7e986e63041c`), line 5: admitted `true`. Lines 203–207: at the r16 measured commit `09ee1d0` the round-14 bucket receipt is `input-drift:tools/mutate-and-run.sh`. Lines 250–253: the older round-14 command still runs and still returns 2, expected 0; it is explicitly superseded, and it was not repaired in place. Lines 275–278: `op1-redbefore-98bea7d.txt` exit 2; `op1-green-dispositions-2a22ade.txt` clean exit 0 (12 expected, 11 effective + one superseded). Line 271: `git diff --stat` of round-13 and round-14 evidence from `98bea7d` to `30b0ca8` is empty, so historical receipts were not rewritten. Line 378: operability improved, active baseline 22/23 → 23/23, no old capability lost. Line 394: the old gate/recipe harm is genuinely repaired. Quality stays unchanged because a new knowledge sentence fails its own recheck and is marked (lines 394–401).

[UNK] whether R16-EV1's `runner-sha256.txt` bytes were corrected. The r17 spot-check records the gate supersession and does not mention that receipt file. No later tameshi verifier-spotcheck exists in the 69-file walk (last file is round 17).

## Admitted control (not a rejection)

Kama round 16 (`77e8f15b947f811ad199fe3d916b460fa6c6b3aa646bb8789110fd9e9f087594`) was admitted (line 7). Line 87: `stale-before.txt` is `ledger_rows=17 uncorrected=17`; `stale-after.txt` is `uncorrected=0`; an independent replication gives 17 at `20e392e` and 0 at `726f737` and `ccc4bb3`. Line 173: seventeen stale statements corrected by appended text.

Kama round 17 (`cd6e83a6446c7661f94ef5210de6d376f791597bdea5589385841e7923bd37d8`) was admitted (line 7) and did not re-open that ledger. [UNK] whether uncorrected is still 0 at the r17 tip. Inside r17 a different stale reading, S043, was superseded by S047 (line 210), and README:238 still cites S043 (line 215), routed for an appended pointer.

## Examined and not counted

Same no-trade rule, different axes, or a tally that was not the rejection cause.

| Closure | Why it is outside the pair | Remedy | Hold |
|---|---|---|---|
| Mado r15 `58e247f8525483eb7d4cc7a71ac4e64cb2b2ed3e5716af1234c0588cb882928a` lines 11–14, 243–244 | Rejected-harmed for a forbidden host partial upgrade. Precision gains do not admit that safety harm. | No code repair imposed (line 284). | Round 16 admitted as source-only learning after the rejected closure. Safety debt is outside this seat. |
| Souji r14 `d760ae40f3990d57dd3827cffc235dab842d70299ccee4c208a0f36561d447d2` lines 7, 160 | Rejected-harmed for an operational trade: namespace cases pass, key-only refusal aborts previously supported benign-config repos. The "migrated stale decision" at line 114 was admitted inside C1. | Repair benign-config support without weakening protected-namespace refusal. | Round 15 (`a77d50142ba853bf1872882c37b344b45b524ba40b7d4f55c8bf98d8a78ae489`) rejected again: claims unprovable, census non-parsing, and quality harmed because a false/stale entry was left marked "unverified" (lines 7, 105, 122). Round 16 (`b43f508937ac8de757f125510fa10b176173d6e033e05b05801bbecd1710048d`) admitted. Line 129: the r15 unmarked-false entry is now true and measured; stale-on-2.55.0 entries are marked. Lines 7–9 and 53: this does not admit r14 retroactively and does not certify no-harm against pre-harm `a31642d`. A silent false-clean (`status.showUntrackedFiles=no`) is present at all three revisions compared. |
| Tsukuroi r12 and r13 | Rejected-harmed because a new sentence was source-inconsistent. The structural counts reproduced. | Routed wording and attribution corrections. | Not read as a hold pair. The rejection cause is a false sentence, not a stale tally or a recall/precision trade. |
| Kagi r21 `6e4fa622ae953f343c294e3ce401303b6b6fa377e8800f9164047b08711f1ffb` line 17 | REJECTED-HONEST-STOP. The 29-case pin was corrected to 36 inside the same closure. The stop is C2 not moving its axis, and E1/E3 failing their bar (expansion/quality trade). | Debts listed for round 22, including five stale stamps. | No later kagi verifier-spotcheck in the 69. Hold of those debts is [UNK]. |
| Kasegi r22, kotodama r49 | Honest-stops on an unmoved axis and on claim separability. | — | Not this pattern. |

## Affected axes

Mado round 20 claims are in `/home/vgpnk/Projects/shokunin/mado-shokunin/SCORECARD.md` sha256 `0139a1a403d4a0e431106e9d7fe70009daa86b7016e7dbbc81292d4593e62914`, lines 1228–1282.

- C2 calibration, criterion 30 (lines 1269–1272): a stated count re-derived at the measured revision. The three red artifacts are "155 transcripts" vs a 154-file receipt, "5/13 name S096" vs 8/13 any-line and 6/13 first-line, and "ten OM10 assertions" vs nine labeled occurrences. This is the axis the move improves.
- C1 operability / tripwire precision (lines 1239–1262) stays on `tools/mado-tripwire.py` and `tw-precision.py`. Separability (lines 1275–1276): C2 is QUALITY text and two round-20 checkers, and it includes no tool change.

R19-V3 (mado r19 lesson `dcb7a9134022e010ef357a095ded13d15d6f77a9090dc2976f0c9d8090fea0a0` line 151) already requires the pure-container negatives and the six-line recall to be kept together. R19-V2 (line 150) already says a token-only count does not prove provenance. The move below is the fleet hold pattern those two routes do not yet spell out: one predicate per definition, pinned to historical blobs, with the old sentence left in place and marked.

## Proposed move

Make criterion 30 a frozen ledger of historical blobs, graded by a new checker under `.ufo/waves/round-20/`, and leave `tools/mado-tripwire.py` byte-identical.

Each red row stores four fields: `git show <rev>:<path>` of the artifact that stated the count, the predicate, the integer in that sentence, and the integer the predicate returns on that blob. Split definitions into separate rows, the way the r19 lesson already measured them:

- receipt file-count at `c7693eb` (stated 155, receipt 154)
- S096 any-matching-line (stated 5/13, measured 8/13)
- S096 first-matching-line (measured 6/13)
- OM10 labeled occurrences (stated ten, measured nine)
- OM10 distinct ids (measured eight)

A row stays red while the stated integer and the predicate integer differ. A round-20 correction is an appended ledger row that cites the same predicate and matches its integer. The r19 lesson bytes stay as committed. That is the tameshi r17 shape: the old command still returns 2 and is marked superseded (tameshi r17 lines 250–253 and 271), and the green command is a different receipt (lines 275–278). It is also the kama r16 shape: before and after are files, and a second party re-derives both integers at named commits (kama r16 line 87). It follows mori r13 line 89: restore the lost distinction by naming it, and do not undo the gain that was real (there, structured metadata; here, the six-line recall, which stays C1's job).

C1 is unharmed because this checker does not scan transcripts and does not change the tripwire. Criterion 29 is unharmed because the ledger does not mount, write a host payload, or replace the fail-closed harness check.

## Risks

- Pinning the live lesson or the live SCORECARD will go stale as soon as round 20 appends, which is the tameshi r16 failure (runner digest moved, recipe still described the old exit). Pin the historical blobs named above.
- A checker that only asserts "the prose is no longer 5" can pass a new wrong integer. Mori r13 line 87 is the same hole: a vaguer category replaced a lost alarm and was still a loss. Require equality with that row's predicate.
- Collapsing any-line 8/13 and first-line 6/13 into one "S096 count" recreates R19-V2. Keep them as two rows.
- Implementing the ledger inside `tw-precision.py` or `mado-tripwire.py` couples a calibration count to the C1 tool and breaks SCORECARD lines 1275–1276.
- Mori r16 lines 220–223: a later closure can admit the named repair and still leave a different stale sentence. This ledger does not close PROVINCE-style leftovers outside its rows.

## Verification

Not run by this seat. L1 can run, without the live gate and without a host probe:

- `sha256sum` of `tools/mado-tripwire.py` at the pre-edit revision and at the candidate revision are equal.
- Red: the five rows above, evaluated with `git show <rev>:<path>`, mismatch on the stated integer.
- Green: an appended correction row whose integer equals that same predicate, and whose input digest equals the pinned blob.
- C1 guards stay the ones already registered (SCORECARD lines 1255–1260): `tw-recall.py` 6/6, zero findings on the 20 control lines, every P case passes at `9c54c56`, whole-corpus diff vs `9c54c56` loses zero findings.

## Limits

- The 69-file walk classified verdicts and keyword hits. Full text was read for the closures cited above, their successor spot-checks, mado r19 routed defects, and SCORECARD round 20. Other admitted lessons were not read end to end.
- Lane gates, `mado-tripwire.py`, `tw-recall.py`, `measure.py`, and kama `stale-statements.py` were not executed. Counts quoted from those lessons (8/13, 6/13, 154, nine OM10, mori 0→1, tameshi 53/54, kama 17→0) are the lessons' measurements.
- No kagi lesson after round 21, and no tameshi lesson after round 17, so later hold is [UNK] beyond those files.
- Kama r17 did not re-measure the r16 stale ledger.
- R16-EV1's receipt-file correction was not found in the r17 spot-check.
- Souji's residual false-clean and mori's residual PROVINCE wording are recorded so they are not smoothed into "the remedy held completely".

## Installs

none

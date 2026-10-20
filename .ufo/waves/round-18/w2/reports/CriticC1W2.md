# CriticC1W2 — wave-2 falsify: C1 calibration (QUALITY 24–26) at 4c103b5

Seat `MadoR18.CriticC1W2`, 2026-10-20. Targets: `corpus/QUALITY.md` criteria 24–26 and
`corpus/lessons/round-18.md` at `4c103b55b1ea5c3c555884afe3eb69b5189701b7`, with receipts at
`abfbf35b1ed4d4a1eb294d525ef286be30f3886f`. All runs used read-only git in the lane, or a private
clone `/tmp/CriticC1W2/lane` (checked out at the named hash, verified with `git rev-parse HEAD`).
I wrote nothing in the lane except this report. I installed no tools and used no package
manager.

Axes: **calibration** (C1 count; whether each criterion is valid), **operability** (gate rc
fix, harm watch), **provenance honesty** (receipt labels).

## 1. Re-measurement of c1 (both revisions)

`measure.py` sha256 is `de4c422b…cfcdc` in the worktree, at `d9a5a18` and at `4c103b5`, so the instrument did not change.

| command (lane cwd) | rc | c1 |
|---|---|---|
| `python3 .ufo/waves/round-17/measure.py d9a5a18` | 0 | criteria 23, lesson_cited 15, score **6.5217** |
| `python3 .ufo/waves/round-17/measure.py 4c103b55b1ea5c3c555884afe3eb69b5189701b7` | 0 | criteria 26, lesson_cited 18, score **6.9231** |
| `… measure.py abfbf35b1ed4d4a1eb294d525ef286be30f3886f` | 0 | 26 / 18 / 6.9231 (unchanged by the receipts commit) |

This agrees with the committed `evidence/measure-after.json.txt` (its header has
`tool_sha256=de4c422b… measured_commit=4c103b5…`). The arithmetic and the literal rubric are
**honest**. The three added lines (`24.`, `25.`, `26.`) each contain `lessons/round-18.md#mistakes`
on their own numbered line. The 8 uncited criteria (1–5, 18, 19, 20) did not change.
The instrument counts **citations, not validity**. The finding below is about validity.

## 2. Per-criterion attack

### Criterion 24 (producer identity): runnable check is NOT real on its green half — DEFECT

**Counterexample A: the shipped check cannot pass at the landed revision.**
`python3 -I .ufo/waves/round-18/receipt-check.py` at abfbf35 (the claims file is the same at 4c103b5) →
6× `MISSING_PROVENANCE`, fixtures `ok`/`SHA_MISMATCH`/`SHA_MISMATCH`, 6× `PENDING`,
`EXPECT_SUMMARY: 9/15`, **exit 2**. `receipt-claims.json` still holds `rev: "PENDING-L1"`. It also
points at `evidence/tripwire-*-recut.txt`, and no such file exists at either hash (`git ls-tree`).
At 4c103b5, `evidence/` has **0** `tripwire*` files. The receipts first appear at abfbf35, under
names without `-recut`. So criterion 24's sentence "Green: the round-18 re-cut receipts and the
frozen-replay receipt" names receipts that did not exist at the revision it describes. That
breaks criterion 8: label a path as planned until it lands. The frozen-replay receipt is not a claim at all.

**Counterexample B (the strongest): the checker rejects every real green receipt.** I pointed it at the
committed round-18 receipts using `/tmp/CriticC1W2/green-claims.json` (rev abfbf35; tool
`tools/mado-tripwire.py`, or `measure.py` for measure-after):
```
RECEIPT g-tripwire-r13 MISSING_PROVENANCE   … r14/r15/r16/anchor-r15/pacmanlog-join likewise
RECEIPT g-tripwire-frozen-match MISSING_PROVENANCE  … frozen-tampered, frozen-before likewise
RECEIPT g-measure-after MISSING_PROVENANCE
EXPECT_SUMMARY: 0/10   (exit 1)
```
The cause is `receipt-check.py:47-48`: `^\s*tool_sha256\s*[=:]\s*(HEX64)\s*$` requires the key to
fill the **whole line**. The re-cut format that the lesson prescribes (M1 fix column, and
`recut-receipts.sh` "line 1: RECEIPT tool=… tool_sha256=<hex> measured_commit=<REV> utc=… cmd=…")
puts both keys on one line, so the regex never matches. Only the authored fixture
`receipt-fixtures/ok-receipt.txt` has the key alone on its line, so it is the only artifact that
passes. The red result (`MISSING_PROVENANCE` on the round-17 receipts) therefore does not
discriminate. The check gives the same token to the bad round-17 receipts and to the good round-18 ones.
Both tool shas were checked independently: `git show 4c103b5:tools/mado-tripwire.py | sha256sum` →
`c87a31ef…` with PIPESTATUS `0 0`, and `d9a5a18` → `962919ce…`. The receipts are correct; the checker is wrong.

**Counterexample C: criterion 23 is broken by 24's own text.** "Green: the round-18 re-cut receipts"
gives the token `ok` to receipts whose recorded outcome from the named checker is
`MISSING_PROVENANCE` (and at 4c103b5, `PENDING`).

**Distinctness from 7/9/13/23:** defensible but thin. 7 says hash from `git show`. 9 binds a verdict
to a commit or frozen-copy sha. 13 asks for a committed path. 23 checks the token at a revision. 24 is
genuinely new only in the **producer-consistency** clause (`tool_sha256` == sha of
`measured_commit:tool`) and in "a re-cut is a committed receipt". The only real red artifacts
(R17 receipts with no header) would already fail criterion 9 and the PROTOCOL gate standard that
R17-V1 cites. So the red case does not show 24 doing anything 9 does not. The distinct arm
(`SHA_MISMATCH`) is exercised only on authored fixtures. The clause "a report labels every tool
sha with the revision it belongs to" (the actual R17-V2 defect, `.ufo/reports/round-17/mado.md:76`)
has no runnable check: the checker reads receipts, not report sentences.

**Secondary (false-provenance risk):** `evidence/tripwire-pacmanlog-join.txt:4` has the header
`# receipt: tool_sha256=c87a31ef… measured_commit=4c103b5…`, which is the **tripwire** sha. The
lesson (M1) says the join is hand-authored and "never tool output", and the current bytes come from
`recut-receipts.sh` (an awk/python join over `/var/log/pacman.log`). With a fixed regex the checker
would mark it `ok` while naming a tool that did not produce those bytes.

**Smallest correction** (tested in `/tmp` only): change the two regexes to token form,
`(?:^|\s)tool_sha256\s*[=:]\s*(HEX64)(?![0-9a-f])` and the same for `measured_commit`. With that
change the same 10 green receipts read **10/10 ok**, and the shipped claims still read 6×
`MISSING_PROVENANCE` plus the fixtures as expected (`/tmp/CriticC1W2/receipt-check-tokenre.py`).
Then:
- replace the six `PENDING-L1` claims with the real abfbf35 paths (drop the `-recut` suffix);
- add frozen-match, frozen-tampered, frozen-before and measure-after as `ok` claims;
- for pacmanlog-join, name `recut-receipts.sh` as the producer, or drop its producer claim;
- re-cut the criterion-24 receipt so the committed run exits 0.

Until then, a non-author should treat criterion 24 as **unreceipted**: its runnable check exits 2 at the landed revision.

### Criterion 25 (mutant bite): check real; one defect in the refusal arm

- Reproduced: `python3 -I .ufo/waves/round-18/measure-mutants.py --lane <lane> --out
  /tmp/CriticC1W2/mm.json --workdir /tmp/CriticC1W2/mmwork --keep` exits 0 with 6/6 bites and
  `no_bite []`. The six `diff_sha256` values **equal** the committed `evidence/measure-mutants.json`.
- **Control (does it fail?):** I ran the harness with loose := tight (`LOOSE_REV=d9a5a18`,
  `LOOSE_SHA=de4c422b…`; a `/tmp/CriticC1W2/mm-control.py` copy with 2-line diff). It exits 1 with
  `no_bite [M1..M5]`, so the check can fail. **But M6 still reports `BITES: loose=None tight=None`.**
  The bite rule (`measure-mutants.py:378`, `bites = bool(loose_only) or tight_refused`) counts a tight
  refusal as a bite even when the "pre-change" instrument also refused. That contradicts criterion 25's
  own definition ("the pre-change instrument credits"). In the committed run, loose credited 5 for M6,
  so the landed 6/6 still holds. The defect lets a future false bite through. In the same
  control, `expectations_met` reads **6** while 5 mutants do not bite: expectations are judged on
  the tight side only, so the field is not evidence of a bite.
- Fix: `bites = bool(loose_only) or (tight_refused and loose['exit'] == 0 and loose_count is not None)`.
- Wording tension: "credits a committed mutant" sits next to "a `/tmp` lab run is provenance, not credit".
  The mutant commits live only in `/tmp/mado-r18-mutants-run` ("identify this run only"). The credit
  actually rests on the committed receipt's embedded diff bytes and digest, which reproduce. Reword it to
  "a mutant whose diff bytes and digest are in the committed receipt".
- Distinct from 13: yes. 13 says where evidence lives; 25 defines what a bite is.

### Criterion 26 (producer status): behavioural check bites; the fixed block still violates 26

- `bash tools/mado-verify.sh --selftest` in the clone at 4c103b5 (gate sha `c9fb0cef…`, equal to
  `git show 4c103b5:tools/mado-verify.sh`) → `MADO_SELFTEST: 389/389`, rc 0.
- **Bite, my own mutant:** I reverted only the pipefail capture at `:3477` to the d9a5a18 form, keeping
  `; grc=$?`. Result: `FAILED — 383 passed, 6 failed`. Five of the failures are OM9 ("no false local-edit claim",
  "names … rc=128", UNKNOWN count 0≠1, FAIL count 2≠1, row UNKNOWN). The sixth is R10, the pin drift,
  as expected. So OM9 really bites. I restored the file afterwards; sha back to `c9fb0cef…`.
- The committed red-before (`evidence/gate-rc-redbefore.txt` §1) has its own problem. It was produced
  by an uncommitted `/tmp/mado-r18-gaterc.lab.sh` against a provisional gate `2bdf5e8a…`, not the landed
  `c9fb0cef…`. By criteria 13 and 25's logic that is provenance only. My mutant run above is a reproducible substitute.
- **Counterexample (same hazard class, inside the fixed block):** the other operand at 4c103b5 is
  `sw=$(sha256sum "$leaf" 2>/dev/null | cut -d' ' -f1)` (`:3479`). Its only guard is `[ -f "$leaf" ]`
  (existence, not readability), and its status is never consumed. I copied the block's decision
  logic into `/tmp/CriticC1W2/replica.sh` (not the gate). In a throwaway repo, a readable leaf gives
  `PASS`. With `chmod 000` on the leaf (uid 1000): `FAIL MOVED: worktree … != HEAD blob 5891b5b522d5…
  (local edit)`. The worktree sha is empty, yet the gate claims a local edit. This is exactly what
  criterion 26 forbids. The `pipe-rc-census.py` screen labels this site `checked # precondition-guard`,
  so it treats an existence test as a status check: a false negative. The hazard is not a regression
  (same bytes at d9a5a18), and it has not fired on this host [INFERENCE: leaf is readable].
- The census does not tell before from after: `pipe-rc-census.py d9a5a18` and `… 4c103b5` both give
  `sites=12 checked=3 unchecked=9`, `VERDICT RED`, rc 1. The fixed `:3477` is still listed as
  `unchecked`. The criterion text already calls it "screen only", so this is a disclosure point,
  not a new defect. But the census contributes no evidence for C1.
- Smallest correction: `sw=$(set -o pipefail; sha256sum "$leaf" 2>/dev/null | cut -d' ' -f1); src=$?`
  with an `UNKNOWN … (rc=$src)` arm, plus a selftest OM11 that makes the leaf unreadable or stubs
  `sha256sum` rc≠0. This changes the gate, so the PIN must be re-cut.
- Distinct from 3: yes, as a mechanism. 3 states the principle and nothing in the lane checked a
  producer status. 26 is a specialization, the same way 23 specializes 9.

## 3. Is 18/26 honest?

The literal number is honest and reproducible (§1). As a **validity** claim, the pre-registration
requires "each with a runnable check shown able to fail". 25 and 26 meet that (25 with a refusal-arm
defect that does not change the landed result). **24 does not.** Its check exits 2 at the landed
revision, and once the PENDING rows are filled it fails 0/10 on every real green receipt. Its
"shown able to fail" red case does not discriminate, because the round-17 receipts and the round-18
re-cuts get the same `MISSING_PROVENANCE`. Counting 24 is mild inflation: a criterion whose own
check cannot certify the artifacts it names.

## 4. What a non-author should rule

1. **c1 measured value:** accept 18/26 = 6.9231 as the literal rubric reading at 4c103b5. It reproduces exactly.
2. **C1 claim:** **partial admit.**
   - Admit 25 (bite reproduced; diff digests match) and 26 (OM9 bites under my mutant).
   - Reject 24 as "runnable check shown able to fail" until the checker regex and claims file are fixed and a passing committed receipt exists.
   - If 24 is struck from the credited numerator, the validated reading is 17/26 = **6.5385** (or 17/25 = 6.8000 if 24 is withdrawn). Both are still above 6.5217, so C1 improves either way, but not by the declared amount.
3. **Route to round 19 (defects, not tradeoffs):**
   - (a) receipt-check token regex plus real claims;
   - (b) measure-mutants bite rule requires that loose credited;
   - (c) `:3479` `sw` producer status plus OM11 and a PIN re-cut;
   - (d) the pacmanlog-join producer label;
   - (e) criterion 24 text: mark the green receipts as landed at abfbf35, not 4c103b5.
4. **Trade the judge must weigh:** criterion 24 overlaps 9 on every real red artifact. Its distinct
   value rests entirely on the producer-consistency arm. A judge may fairly rule that 24 should
   instead have been an amendment to 9/23 (the round-14/15 "no duplicate provenance criterion"
   ruling) rather than a new numbered line that raises the counter.

## Commands run (all output quoted above)

- `git diff --stat d9a5a18 4c103b5 -- corpus/QUALITY.md corpus/lessons/ SCORECARD.md`; `git show 4c103b5:corpus/QUALITY.md`; `git show 4c103b5:corpus/lessons/round-18.md`
- `python3 .ufo/waves/round-17/measure.py {d9a5a18,4c103b5…,abfbf35…}`, all rc 0
- `python3 -I .ufo/waves/round-18/receipt-check.py` → 9/15 exit 2; same tool with `/tmp/CriticC1W2/green-claims.json` → 0/10 exit 1; patched copy → 10/10 green, 9/15 shipped
- `python3 -I .ufo/waves/round-18/measure-mutants.py …` → 6/6 rc 0; control copy → `no_bite [M1..M5]`, M6 false bite, rc 1
- `python3 -I .ufo/waves/round-18/pipe-rc-census.py {d9a5a18,4c103b5…}` → 9 unchecked each, RED, rc 1
- `bash tools/mado-verify.sh --selftest` (clone at 4c103b5) → 389/389; with the pipefail mutant → 383/389 (OM9 ×5, R10)
- `/tmp/CriticC1W2/replica.sh` → unreadable leaf gives FAIL "local edit"

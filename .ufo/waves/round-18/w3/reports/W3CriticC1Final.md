# W3CriticC1Final — C1 (QUALITY 24–26) at the final lane commit

Seat: `MadoR18.W3CriticC1Final`, 2026-10-20. Target: `a210241b5429fb3c3f9ad23f42863d6e6d9e5845`
(master). I also read `d9a5a18`, `4c103b5`, `abfbf35` and `be886a3`.

How I worked: all runs used a private clone, `/tmp/c1final`, with
`git rev-parse HEAD` → `a210241b5429fb3c3f9ad23f42863d6e6d9e5845`. Scratch files went to
`/tmp/c1final-lab` and a mutant copy to `/tmp/c1final-mut`. The only lane write is this report.
I used read-only git only. I made no install and ran no package manager, sudo or host probe.
The gate was run only as `--selftest` and `--regression`.

Axes: **calibration validity** (does each criterion have a check that fails on a real
`d9a5a18` artifact and passes a control?), **provenance honesty** (receipt and SCORECARD
sentences), **no regression** (gate selftest and regression).

## 0. Headline

CriticC1W2's blocker is **closed**. At `a210241`, the receipt checker exits 0 with
`EXPECT_SUMMARY: 21/21`. It marks the real round-17 receipts as red and the real round-18 receipts
as green. It also has a STALE arm that I triggered on a real receipt. Criteria 24, 25 and 26 each
now have a check that fails on a real `d9a5a18` artifact (for 25, on its instrument through the
loose := tight control) and passes on a control.

18/26 = 6.9231 reproduces. **Ruling: admit C1 at 18/26, narrowly.** Admission needs one honesty
erratum (§4.2) and comes with routed defects (§5). None of the defects changes the counted numerator.

## 1. Criterion 24 — receipt-check.py

### 1.1 Shipped claims at the final commit

```
$ cd /tmp/c1final && python3 -I .ufo/waves/round-18/receipt-check.py; echo rc=$?
RECEIPT r17-tripwire-r13 MISSING_PROVENANCE   (r14, r15, r16, anchor-r15, pacmanlog-join likewise)
RECEIPT r18-fixture-ok ok
RECEIPT r18-fixture-bad-sha SHA_MISMATCH
RECEIPT r18-fixture-stale-rev SHA_MISMATCH
RECEIPT r18-fixture-stale-tool STALE
RECEIPT r18-fixture-nonancestor NOT_ANCESTOR
RECEIPT r18-fixture-producer-mismatch PRODUCER_MISMATCH
RECEIPT r18-tripwire-r13 ok   (r14, r15, r16, anchor-r15, frozen-match, frozen-tampered, frozen-before, measure-after likewise)
EXPECT_SUMMARY: 21/21
rc=0
```

What changed since abfbf35:
- The anchored regex is replaced by `TOKEN = r"\b{}\b[\"']?\s*[=:]\s*[\"']?({})"`.
- PENDING-L1 rows are replaced by real `abfbf35` paths.
- Ancestry and STALE checks are added.

So CriticC1W2 counterexamples A, B and C no longer hold.

**Red on real `d9a5a18` artifacts:** yes. The six round-17 receipts are read at `d9a5a18`.

**Green on real controls:** yes. Nine real round-18 receipts pass, not only the authored fixture.

### 1.2 My own claims set (`/tmp/c1final-lab/attack-claims.json`, 22 claims)

```
$ python3 -I .ufo/waves/round-18/receipt-check.py /tmp/c1final-lab/attack-claims.json; echo rc=$?
final-{r13,r14,r15,r16,anchor-r15,frozen-match,frozen-tampered,frozen-selftest,r18-seats} ok   (read at a210241)
final-redbefore ok (bind_rev abfbf35)   final-measure ok   final-frozen-prov ok
final-harm-gate PRODUCER_MISMATCH
abf-r13-at-final STALE
gate-rc-redbefore MISSING_PROVENANCE
regression-recut MISSING_PROVENANCE
gate-selftest MISSING_PROVENANCE
measure-mutants MISSING_PROVENANCE
recut-summary SHA_MISMATCH
join-final-as-tripwire ok
join-final-as-recut SHA_MISMATCH
r17-oracles MISSING_PROVENANCE
EXPECT_SUMMARY: 14/22   rc=1
```

**Good results:**
- 12/12 real final (`be886a3`) receipts pass at `a210241`. This is an independent green control.
- The `abfbf35` re-cut `tripwire-r13.txt`, read at `a210241` without `bind_rev`, gives
  **STALE**. That is the R17-V1 shape on a real artifact (tripwire `c87a31ef…` → `c1ae45a7…`).
  So the distinct arm now bites on real bytes, not only on fixtures.
- A second real `d9a5a18` red: `.ufo/waves/round-17/evidence/tripwire-vs-oracles.json` has
  `"tool_sha256": "962919ce…"` but no `measured_commit` → `MISSING_PROVENANCE`.

**Defects found (counterexamples):**

**D24-1 (honesty; the strongest).** Receipts that round-18 text itself relies on fail criterion 24
under its own checker:
- `evidence/gate-rc-redbefore.txt` is cited by QUALITY 26, lesson M3 and the SCORECARD C1 row.
  Result: MISSING_PROVENANCE.
- `evidence/regression-recut.txt` is cited by lesson M3. Result: MISSING_PROVENANCE.
- `evidence/measure-mutants.json` is cited by QUALITY 25 and lesson M2. Result:
  MISSING_PROVENANCE. It has a `harness.sha256` of `075815bd…`, which matches
  `git show 4c103b5:…/measure-mutants.py | sha256sum`, but it has no `tool_sha256` or
  `measured_commit` key.
- `evidence/gate-selftest.txt`: MISSING_PROVENANCE.

`gate-rc-redbefore.txt:10` and `regression-recut.txt:17` both name gate `2bdf5e8a…`. That digest
belongs to no commit. `git show {d9a5a18,4c103b5,abfbf35,be886a3,a210241}:tools/mado-verify.sh | sha256sum`
gives only `fba82a66…` and `c9fb0cef…`, so these receipts can never satisfy criterion 24's
`git show <measured_commit>:<tool>` clause.

SCORECARD `:991-992` says "Every receipt's first line names `tool_sha256` and `measured_commit`
(QUALITY 24)". Unqualified, that is false. My loop over
`git ls-tree -r --name-only a210241 .ufo/waves/round-18/evidence/` found 16 of 62 files without both
keys on line 1, including the four tool receipts above.

**D24-2 (soundness).** When line 1 is not a `RECEIPT` header, the checker takes provenance from
anywhere in the text. Test: I took the `d9a5a18` r13 receipt, which has no header, and appended one
comment line that quotes `tool_sha256=962919ce… measured_commit=d9a5a18…`. The checker returned
`ok` (WORKTREE claim, bind `d9a5a18`; `EXPECT_SUMMARY: 0/1` against the expected
MISSING_PROVENANCE). So a body that merely mentions a sha pair counts as producer identity. I wrote
the fixture inside the `/tmp` clone and removed it afterwards (`git status --porcelain` count 0).

**D24-3 (false red).** `final/harm-gate-selftest.txt` and the other harm-watch receipts write
`tool=/home/vgpnk/…/tools/mado-verify.sh`, an absolute path. A claim with the lane-relative tool
gets **PRODUCER_MISMATCH** although sha and commit agree.

**D24-4 (false provenance, carried from CriticC1W2 (d), not fixed).**
- `final/tripwire-pacmanlog-join.txt:4` carries `# receipt: tool_sha256=c1ae45a7…` (the tripwire)
  `measured_commit=be886a3…`.
- The bytes are written by the inline python in `recut-receipts.sh:191-345`, not by the tripwire.
- If the join is claimed as tripwire output, the checker certifies it `ok`.
- The claims file's note says the join "can never carry a producer header"; the committed file does
  carry one.
- No round-18 results sentence relies on it as tripwire output, so this does not change C1.

**D24-5 (unchanged).** The clause "a report labels every tool sha with the revision it belongs to"
has no runnable check. The checker reads receipts, not prose. SCORECARD `:1000-1002` does label each
sha by revision, and it is correct. Check:
`git show {d9a5a18,4c103b5,be886a3}:tools/mado-tripwire.py | sha256sum` → `962919ce…`,
`c87a31ef…`, `c1ae45a7…`. Gate: `fba82a66…` → `c9fb0cef…`.

**24 ruling: admit.** The check now discriminates on real artifacts in both directions and has a
real STALE arm. D24-1 is the criterion working, not failing: it catches the round's own uncited
producers. It requires the §4.2 erratum. D24-2, D24-3 and D24-4 are fixable checker or labelling
defects for round 19. Overlap with criterion 9 (CriticC1W2 §4.4) remains a judge tradeoff. The real
STALE result is evidence that 24 does something criterion 9 does not.

## 2. Criterion 25 — measure-mutants.py

`measure-mutants.py` has the same sha, `075815bd…`, at `4c103b5` and `a210241`. `git log` shows
its last change at `4c103b5`.

```
$ python3 -I .ufo/waves/round-18/measure-mutants.py --lane /tmp/c1final --out /tmp/c1final-lab/mm.json --workdir /tmp/c1final-lab/mmwork
summary {'mutants': 6, 'bites': 6, 'no_bite': [], 'expectations_met': 6, ...}   rc=0
diff_sha256 M1..M6 == committed evidence/measure-mutants.json: True ×6
(e9f712a5f88c, cf76218f577c, 6a0fcaf898cb, 1bf73ed9392d, 700d022a9b18, d62bfcd81afb)
```

**Control: loose := tight = `d9a5a18` instrument (`de4c422b…`).** The copy
`/tmp/c1final-lab/mm-control.py` differs from the shipped harness only in `LOOSE_REV` and `LOOSE_SHA`
(lines 46–47):

```
M1..M5 NO-BITE (loose=tight=3/4/4/4/4, loose_only=[])
M6 BITES: loose=None tight=None loose_only=[]   tight refused (exit 2): duplicate SOURCES id S016
"bites": 1, "expectations_met": 6   rc=1
```

**What fails and what passes:**
- With no tightening between the real `d9a5a18` instrument and itself, the check fails (rc 1,
  `no_bite` M1–M5).
- The real f52f43f → d9a5a18 tightening passes.
- The `d9a5a18` red is an absence: `git ls-tree -r --name-only d9a5a18 | grep -c measure-mutants` → 0.

**D25-1 (carried from CriticC1W2, still unfixed).** `measure-mutants.py:378`
`bites = bool(loose_only) or tight_refused` reports a false M6 bite when both instruments refuse.
`expectations_met` stays at 6 under the control, so that field is not bite evidence. The landed M6
bite is real: in the committed record, M6 loose exit 0 credited 5 provinces and tight exit 2.

**D25-2.** The receipt has no criterion-24 header (D24-1).

**25 ruling: admit.** Its credited content reproduces byte-exactly, and the check can fail. D25-1 is
a defect to route to round 19, not a tradeoff.

## 3. Criterion 26 — gate producer status

```
$ cd /tmp/c1final && bash tools/mado-verify.sh --selftest   → MADO_SELFTEST: 389/389, rc=0; sha256 c9fb0cef…
```

**Red on the real `d9a5a18` artifact.** In `/tmp/c1final-mut` I replaced the landed block
(`a210241` lines 3470–3488) with `d9a5a18`'s verbatim block (lines 3405–3414; the diff is shown
in the run) and ran `--selftest`:

```
MADO_SELFTEST: FAILED — 383 passed, 6 failed
- R10 (pin drift, expected)
- OM9 (a failed show can never be compared) (want row omarchy.skill.vs_head UNKNOWN)
- OM9: the UNKNOWN names the unreadable path and the producer rc (… rc=128)
- OM9: no false local-edit claim (unexpected: local edit)
- OM9: exactly one omarchy UNKNOWN (got '0' want '1')
- OM9: exactly one omarchy FAIL (got '2' want '1')
```

This red can be reproduced from committed bytes. The committed `gate-rc-redbefore.txt` was cut
against the uncommitted gate `2bdf5e8a…` (D24-1).

**Regression at the landed gate:**
```
$ MADO_VERIFY_HARNESS=/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh bash tools/mado-verify.sh --regression
REGRESSION_TOOL … sha256=c9fb0cef…; REGRESSION_TARGET … 20714096… (match=yes)
MADO_REGRESSION: PASS (killed=10/10 flips=0)   rc=0
```
The harness is now `fb6d86d5…`; `regression-recut.txt` recorded `0673d2e5…`, which is provenance
only. A first run without the env var gave `SETUP (mutation harness not found…)` rc 2, because of
my `/tmp` clone's location.

**D26-1 (counterexample inside the fixed block; carried, unfixed).**
- Line `:3479` reads `sw=$(sha256sum "$leaf" 2>/dev/null | cut -d' ' -f1)`. Its status is never
  consumed, and the only guard is `-f` (the file exists).
- Replica: lines 3477–3488 verbatim, with stubs `tmo`/`row`, in a throwaway repo
  (`/tmp/c1final-lab/sw/replica.sh`).
  - Readable leaf → `PASS`.
  - `chmod 000` (uid 1000) → `FAIL :: MOVED: worktree … != HEAD blob 1d9aca6b938e… (local edit…)`,
    with an empty worktree digest.
- That is exactly the outcome criterion 26 forbids.
- No OM scenario covers it. None of MutGateOM's 8 mutants does either; m08 only moves `grc=$?`.
- `pipe-rc-census.py a210241` labels `:3479 checked # precondition-guard`, a false negative.
  `:3477` is still listed `unchecked`. Result: `sites=12 checked=3 unchecked=9`, `VERDICT RED`,
  rc 1, the same as at `d9a5a18`/`4c103b5`.
- Not a regression: the line is the same at `d9a5a18`. Not observed on this host [INFERENCE].

**26 ruling: admit.** OM9 bites on the real `d9a5a18` code. D26-1 shows that the criterion is
**not yet satisfied by the gate it was written for**. SCORECARD and lesson text that says the hazard
is "fixed" should be read as "the `git show` producer fixed", not "the block conforms to 26".

## 4. Is 18/26 honest?

### 4.1 The number

```
$ python3 .ufo/waves/round-17/measure.py a210241b5429fb3c3f9ad23f42863d6e6d9e5845 → c1 criteria 26, lesson_cited 18, score 6.9231; rc 0
$ sha256sum .ufo/waves/round-17/measure.py → de4c422b… (unchanged)
```

The literal number is honest. The pre-registered condition was "each with a runnable check shown
able to fail", and it is now met for all three:
- 24: real `d9a5a18` reds and a real STALE.
- 25: the loose := tight control fails.
- 26: the `d9a5a18` block fails OM9.

The SCORECARD row also discloses that 24 was not green at `abfbf35`.

### 4.2 Required erratum (honesty, not the number)

SCORECARD `:991-992`, "Every receipt's first line names `tool_sha256` and `measured_commit`", is
false as written (D24-1: 16/62 files, at least 4 cited tool receipts). The C1 row cites
`gate-rc-redbefore.txt` for 26's red-before. That receipt fails 24 and names a gate that is not
committed.

Smallest correction (append-only):
- Narrow the sentence to "every measure and tripwire receipt".
- List `gate-rc-redbefore.txt`, `regression-recut.txt`, `gate-selftest.txt` and
  `measure-mutants.json` as provenance-only under QUALITY 24.
- Point 26's red at the reproducible transplant in §3 instead.

## 5. Ruling and routing (non-author)

1. **c1 value:** accept 18/26 = 6.9231 (+0.4014) as the literal reading at `a210241`. It reproduces.
2. **C1 claim: admit, narrowly.** Admit 24, 25 and 26. Condition: the §4.2 erratum. Without it the
   results section contains a sentence that its own criterion 24 rejects. I would then read C1 as
   **partial**: the number stands, but the provenance sentence is false.
3. **Route to round 19 (defects, not tradeoffs):**
   - D24-2: the checker reads provenance only from a line-1 `RECEIPT` header or top-level JSON keys.
   - D24-3: normalise absolute `tool=` paths relative to the lane.
   - D24-4: name `recut-receipts.sh` as the join's producer, or drop its header.
   - D24-1: give the four uncited receipts headers, or mark them provenance-only.
   - D25-1: `bites = bool(loose_only) or (tight_refused and loose exit 0 with a count)`.
   - D26-1: `sw` under `set -o pipefail` with an `rc` → UNKNOWN arm, an OM11 scenario for an
     unreadable leaf, and a PIN re-cut; the census should treat `-f` as not a status check.
4. **Tradeoff left to the judge:** whether criterion 24 should have amended 9/23 rather than add a
   numbered line. The real STALE result (§1.2) is the best evidence that it adds distinct power.

## Commands run

- `git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/c1final && git -C /tmp/c1final checkout -q a210241…; git rev-parse HEAD`
- `git log --oneline -8 a210241`; `git diff --stat abfbf35 a210241 [-- checker/claims/fixtures/measure-mutants/gate/QUALITY]`
- `python3 -I .ufo/waves/round-18/receipt-check.py` → 21/21 rc 0
- `python3 -I .ufo/waves/round-18/receipt-check.py /tmp/c1final-lab/attack-claims.json` → 14/22 rc 1 (§1.2)
- `python3 -I .ufo/waves/round-18/receipt-check.py /tmp/c1final-lab/quoted-claims.json` → `ok` on a headerless receipt with a quoted sha pair
- line-1 header loop over `git ls-tree -r --name-only a210241 .ufo/waves/round-18/evidence/` → 16/62 without the header
- `git show <rev>:tools/mado-tripwire.py|sha256sum` for 988b858, d9a5a18; `git show <rev>:tools/mado-verify.sh|sha256sum` for 5 revs
- `python3 -I .ufo/waves/round-18/measure-mutants.py --lane /tmp/c1final …` → 6/6 rc 0, digests equal; control copy → rc 1, M6 false bite
- `bash tools/mado-verify.sh --selftest` (clone) → 389/389; transplant copy → 383/389
- `MADO_VERIFY_HARNESS=… bash tools/mado-verify.sh --regression` → PASS 10/10
- `/tmp/c1final-lab/sw/replica.sh` readable → PASS; `chmod 000` → FAIL "local edit"
- `python3 -I .ufo/waves/round-18/pipe-rc-census.py a210241…` → RED, rc 1
- `python3 .ufo/waves/round-17/measure.py a210241…` → 26/18/6.9231

Installs: none.

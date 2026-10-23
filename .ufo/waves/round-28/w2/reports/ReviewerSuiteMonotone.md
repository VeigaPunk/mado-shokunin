# ReviewerSuiteMonotone — mado r28 w2 (reviewer, read-only)

Axis: operability (C1 leg `h1-rotation`). Question: are the new suite probes monotone
(judgement unchanged except the three survivor classes the round closes) and behavioural?
Verdict: **monotone and behavioural; no defects found.**

Tip: `master` = `4f610066efd90804b055c42ae20c41a7f44404f9`. Suite under review is the
**uncommitted worktree** `quality/counter-selftest.py` sha256
`d72b7f1aa806a8595dba3e5a6cbcb16d899490419227daff7a57629babfe1180` (landed mid-review, ~20:10;
ExecSuiteProbes). Committed baseline at tip: sha256
`aa0e14d160b8429b945f12329e5673a1d484986d1b617a05920a92e77a1d4898`, snapshotted to
`/fast/scratch/hyaku/mado-r28/ReviewerSuiteMonotone/committed-suite.py`.

## 1. Pristine subjects

`python3 -I quality/counter-selftest.py --c1 .ufo/waves/round-26/c1/count-v2.py --c2
.ufo/waves/round-26/c2/count.py --rev 4f610066… --scratch /fast/scratch/hyaku/mado-r28/ReviewerSuiteMonotone`
→ `exit=0`. Verbatim tail:

    SELFTEST pass=59 total=59
    exit=0

(Committed baseline ran identically earlier: `SELFTEST pass=56 total=56`.)

## 2. Monotonicity on W (15) + H1 (18) rows

Command (×2, `--suite-a-file` = committed snapshot / worktree), same seed `c0ffee28`, jobs 6:

    python3 -I .ufo/waves/round-27/c2/count-v2.py 4f610066efd90804b055c42ae20c41a7f44404f9 \
      --heldout /fast/scratch/hyaku/mado-r27/heldout --seal .ufo/waves/round-27/c2/heldout-seal.txt \
      --suite-a-file <suite> --seed c0ffee28 --jobs 6

Both `exit=0`. The two PRED lines (verbatim):

    committed: PRED-C2-r27-v2 green=17/17 b_valid=9 w_killed=15/15 h_killed=15/18 h_need=14 h_valid=18 h_min_per_subject=6 invalid=0 verdict=TARGET_MET
    new:       PRED-C2-r27-v2 green=17/17 b_valid=9 w_killed=15/15 h_killed=18/18 h_need=14 h_valid=18 h_min_per_subject=6 invalid=0 verdict=TARGET_MET

CASE-row diff (committed → new), complete — exactly the three survivor classes flip:

    < CASE H H/HeldC1v2:held-c1v2-extra-output-segment    suite=A rc=0 SURVIVED | exit=0
    > CASE H H/HeldC1v2:held-c1v2-extra-output-segment    suite=A rc=1 KILLED  | exit=1
    < CASE H H/HeldC1v2:held-c1v2-missing-version-guard   suite=A rc=0 SURVIVED | exit=0
    > CASE H H/HeldC1v2:held-c1v2-missing-version-guard   suite=A rc=1 KILLED  | exit=1
    < CASE H H/HeldC1v2:held-c1v2-node-subset             suite=A rc=0 SURVIVED | exit=0
    > CASE H H/HeldC1v2:held-c1v2-node-subset             suite=A rc=1 KILLED  | exit=1

Every other row identical: all 17 GREEN `rc=0 PASS`, all 15 W `rc=1 KILLED`, the other 15 H
`rc=1 KILLED`. Monotone confirmed.

## 3. No text/AST/hash pins — new assertions (verbatim)

Three new checks, all behavioural (synthetic harness inputs → counter rc/output):

- `c1-extra-output-segment` (suite ~:535): mutant tool emits `out.append([])` (3 segments);
  assertion `rc == 1 and verdict == "TARGET_MISSED" and got is not None and got < total`.
  Observed `rc=1 cases_pass=0/41`. Kills the mutant that relaxes `len(data) == 2` to `>= 2`.
- `c1-node-subset` (~:557): `out[0].pop()` (strict node subset); same assertion shape.
  Observed `rc=1 cases_pass=0/41`. Kills `gn <= en` (subset-tolerant comparator).
- `c1-version-missing-commit` (~:583): `VERSION_MISSING = {"tag": "v0.56.2"}` (no commit key);
  assertion `rc == 2 and "ORACLE_VERSION" in out`. Observed `rc=2 ORACLE_VERSION=yes`.
  Kills `if commit and commit != HYPR_COMMIT:` (missing-key-tolerant guard).

No string/AST/sha matching on subject bytes anywhere in the diff.

## 4. Inventory gate

REQUIRED gained the three names; `TOTAL = len(REQUIRED)+1` ⇒ 58+1=59. Observed
`CHECK check-inventory PASS missing=none extra=none`, `SELFTEST pass=59 total=59` — agrees.

## Failure-reason audit

No check fails for an unintended reason; every new check's pass is the designed signal.
Note (not a defect): `extra-output-segment`/`node-subset` show `cases_pass=0/41` on the
pristine counter — the counter fails closed on malformed/subset output for all cases, which
is the intended strictness; only a mutant tolerant of the defect escapes all-fail.

## Incidents / honest dead ends

- `git -C <lane> clone … m1` test resolved `m1` into the lane; removed the stray 19 M clone
  immediately (rm, not a mutating git op on the repo).
- `/fast` was 100% full (13 M free); the frozen counter's fixed scratch
  `/fast/scratch/hyaku/mado-r27/c2v2` could not host clones. Rather than delete the stale
  `m27c2-pu461adv` (live bwrap/tinywl FDs), I mounted an 8 G tmpfs over `c2v2`, ran both
  counters, then umounted. Verified `findmnt` clean afterwards. Shadowed bytes untouched.
- One transient seed error (`rev28monotone01` non-hex) before rerun; no data lost.
- No package/tool installs (pacman paused; none needed).

## Scope limit

`--suite-b-file` was left at REV (suite B unmodified this item). Files written: this report,
`/fast/scratch/hyaku/mado-r28/ReviewerSuiteMonotone/{committed-suite.py,suite.diff,
run-committed.txt,run-new.txt,new-selftest.txt,exits.txt}` (tmpfs scratch auto-removed).

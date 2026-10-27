# CritC2FrozenStub — w2 FALSIFY seat (round 50, hyaku run 10, attempt 2)

Seat: CritC2FrozenStub · Target: PRED-C2-r50 do-nothing controls + cheaper wrong gates · Verdict: **C2 counter admits cheap wrong gates (M3, M4 below); controls and rule-removal mutants correctly MISS.**

All runs: frozen counter `quality/counters/c2-r50-session-gate.py` (sha256 `1d52a62c…`, verified at attack rev `b4a79843`) against a `git clone -q --shared` of the lane in my scratch, mutants committed atop data rev `906178b607f2071af7c2efec5aad976a8bfa5757`, nonce 602211 (same as `receipts/controls-c2.txt`). Lane tree untouched; no lane/fleet git mutations.

Command shape: `TMPDIR=<scratch>/work python3 -I quality/counters/c2-r50-session-gate.py --repo <clone> --rev <rev> --work <scratch>/work --nonce 602211`

## 1. c14 control re-verification — MISS, byte-identical to freeze

Rebuilt c14 (v3 rules, `DEFAULT_SCOPE = "ufo"`) on the shared clone: commit `b1cf8b0b555866b48a2ba6da7ef7b023507938d1`, **1 insertion / 1 deletion** vs data rev. The rebuilt gate's sha256 is `3758808c10938cb1ab9b969c3f342196836f7782c23984e8abc4f53e1c7638a7` — **byte-identical to the frozen c14 control** in `registration.md` / `receipts/controls-c2.txt` (rev `482e3e89`). Counter verdict (`receipts/m0-c14.txt`):

```
PRED-C2-r50: selftest=93/94 names=69/69 red=0/41 green=0/40 scope=blind verdict=TARGET_MISSED
```

Same sentence as the frozen receipt except rev. The single failing selftest case is the v3 default-scope case (`v3-default-scope-all-sees-outside-ufo`); clause r fails because every fixture's shape sits outside `.ufo/` and the default scope never scans it; green misses because `files=0` under `--scope ufo`. c00/c12 in the frozen `controls-c2.txt` were read and are consistent with the counter code (v2 selftest 69<94; stub over-flags). **Controls re-verified: MISS.**

## 2. Probe (a): v3 with R9 removed, selftest edited to keep 94/94 — clause r catches it

Commit `6c7e5f38259275fd5ee5154a67f825cd7728d3f0` (7 insertions / 12 deletions): deleted the R9 block in `scan_blob` (quality/check-session-material.py:548-551 region) and re-pointed the 4 R9-dependent selftest cases (`r9-cache-record-fields`, `r9-detail-counts-only`, `waiver-new-band-fixture-waived`, `waiver-r9-real-title-rejected`) so the suite still prints 94/94. Standalone selftest: `passed=94/94 failed=0`. Counter verdict (`receipts/m1-r9-removed.txt`):

```
PRED-C2-r50-SELFTEST: passed=94/94 failed=0 cases=94 rc=0     <- clause s fooled by the edited selftest
PRED-C2-r50-RED: ok=35/41 families=… r8-account=7/7 r9-cache=0/6
RED_MISS repo=red-005-r9-cache rule=R9_EXEC_CACHE rc=0 findings=0 rules=-
PRED-C2-r50: … red=35/41 green=40/40 scope=seen verdict=TARGET_MISSED
```

**Clause s does not re-verify selftest honesty (it parses the gate's own printed `SELFTEST:` totals + case names), but clause r caught the removal: all 6 r9-cache fixture repos score `rc=0 findings=0` → the expected-rule membership check fails.** Probe (a) answer: yes, clause r catches it.

## 3. Probe (b): parrot emitting the R7 finding string once per red repo — rule-check stops it

Commit `262133eff86954e12691f42ef32ec9308feb8279` (22/30): `scan_blob` collapsed so any R7/R8/R9 shape emits exactly one `FINDING … rule=R7_HOME_PATH_PREFIX count=1 detail=parrot`; 11 selftest cases re-pointed to keep 94/94 (standalone: 94/94). Counter verdict (`receipts/m2-r7-parrot.txt`):

```
RED_MISS repo=red-004-r8-account rule=R8_ACCOUNT_COLUMN rc=1 findings=1 rules=R7_HOME_PATH_PREFIX
RED_MISS repo=red-005-r9-cache rule=R9_EXEC_CACHE rc=1 findings=1 rules=R7_HOME_PATH_PREFIX
PRED-C2-r50: selftest=94/94 names=69/69 red=28/41 green=40/40 scope=seen verdict=TARGET_MISSED
```

**Clause r does NOT merely count findings** — the parrot scored `findings=1 rc=1` on every red repo, which a count-only check would admit, but the r8-account and r9-cache repos MISS because the emitted rule set (`{R7}`) lacks the expected `R8_ACCOUNT_COLUMN` / `R9_EXEC_CACHE` (counter source: `ok = rc not in (0,None) and findings>=1 and shape["rule"] in result["rules"]`, c2-r50-session-gate.py:466-469). Probe (b) answer: the rule-membership check stops the R7-only parrot.

## 4. Weakest admitted variants — the counter is gameable

The same membership check is satisfiable by spraying **all three** rule tags on any detection, and clause s is satisfiable by a printed transcript. Both wrong gates read TARGET_MET:

**M3 — all-rules spray on v3 detection + edited selftest** — commit `45e2fe637b1411430fcd7701d243002fbe5eb698` (16/17): any R7/R8/R9 hit emits `FINDING` lines for R7, R8 and R9 (counts `0` included); 6 selftest cases re-pointed (`r7-home-path-in-ls-row`, `r8-numeric-ids-clean`, `r9-record-is-not-a-home-listing`, `waiver-r7-real-user-rejected`, `waiver-r9-real-title-rejected`, `v3-cli-default-scope-and-account-silent`). Verdict (`receipts/m3-spray.txt`):

```
PRED-C2-r50: selftest=94/94 names=69/69 red=41/41 green=40/40 scope=seen verdict=TARGET_MET rev=45e2fe63…
```

Wrongness: attribution is meaningless (a pure R8 account-column leak is also "flagged" as R7 and R9 — see `default_findings=3` for the single-shape scope fixture), and 6 of 94 selftest cases now assert the wrong behavior while keeping their v2/v3 names.

**M4 — tiny standalone parrot (cheapest admitted variant)** — commit `504902fd6c8f0488b148fa6b256018bfe68d3ed2`: a **7046-byte** replacement gate (v3 is 89219 bytes; −2107/+154 lines) that
- `--selftest` prints a canned transcript: the 69 pinned v2 names + 25 `probe-NN` filler names + `SELFTEST: passed=94/94 failed=0`, and runs no tests at all;
- scan = 50 lines implementing the three detectors with the same shape precision as v3 (4 structural R7 forms, `--account` owner/group R8, `>=2` cache-field R9), then sprays all three rule tags per hit.

First M4 attempt MISSED on `g-one-field=0/6` (my R9 lacked the 2-field threshold — a single `--title=` field fired), showing clause g's green fixtures have teeth. After adding the threshold: verdict (`receipts/m4-tiny-parrot.txt`):

```
PRED-C2-r50: selftest=94/94 names=69/69 red=41/41 green=40/40 scope=seen verdict=TARGET_MET rev=504902fd…
```

**M4 is the weakest admitted variant I can build.** What stops anything cheaper: clause g forces detection precision at least equal to v3's on the green counter-shapes (prose-embedded home path, `~/` masked prefix, indented usage, one-field cache, numeric-id rows all must stay clean), and clause s forces a 94-line transcript containing the 69 pinned v2 names — detection + transcript is the floor, and M4 sits on it.

## 5. Counter holes (for the L1)

1. **Clause s trusts the gate's printed selftest output.** A canned transcript (M4) or re-pointed cases (M1/M3) passes; selftest is not cross-checked against the fixture runs.
2. **Clause r's rule check is membership, not attribution.** Spraying all three tags passes (M3/M4); nothing checks that extra rules didn't fire or that counts/details are right.
3. Combined, PRED-C2-r50 certifies "the installed gate prints a 94/94 transcript and detects the six red shape families *somehow tagged*", not "v3's rules are implemented and honestly self-tested". If that weaker property is the intent, fine; if the claim needs attribution/honesty, the counter needs a pinned-gate comparison or behavioral cross-checks.

## Evidence

- `receipts/base-at-data.txt` — harness check: TARGET_MET at `906178b6…`, nonce 602211 (`red=41/41 green=40/40`).
- `receipts/m0-c14.txt` — c14 rebuild verdict; gate sha256 `3758808c…` == frozen c14.
- `receipts/m1-r9-removed.txt` — probe (a): `red=35/41 r9-cache=0/6 TARGET_MISSED`.
- `receipts/m2-r7-parrot.txt` — probe (b): `red=28/41` via rule-check, `findings=1 rc=1` on r8/r9.
- `receipts/m3-spray.txt` — all-rules spray v3-edit: **TARGET_MET**.
- `receipts/m4-tiny-parrot.txt` — 7046-byte parrot: **TARGET_MET**.

Scratch (clone + work dirs) deleted after copying receipts. No installs/upgrades needed (python3 stdlib only). Host guard respected: all state under `/fast/scratch/hyaku/mado-r50/CritC2FrozenStub`; no home writes; read-only git on the lane.

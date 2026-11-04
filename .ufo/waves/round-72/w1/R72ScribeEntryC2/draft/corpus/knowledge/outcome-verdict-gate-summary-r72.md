---
source: S444 (https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/unittest.rst, § TestResult.wasSuccessful, lines 2127–2134; main exit semantics, lines 2354–2357) and S445 (https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/unittest/main.py, lines 270–277); local receipts .ufo/waves/round-72/fetch/Doc_library_unittest.rst.1 and .ufo/waves/round-72/fetch/Lib_unittest_main.py.1
verified-at: 9bcb4fd5b598844f168230dc05e441721d95b272
recheck: `python3 -I quality/counters/c2-r72-outcome.py --repo . --rev 9bcb4fd5b598844f168230dc05e441721d95b272 --base-rev 976684a27e99c2508037a60eec415f550f53d70e --controls .ufo/waves/round-72/controls/c2-controls-r72.json --scratch-root <scratch>` prints `MADO_R72_OUTCOME: cases=8 correct=8 base_correct=4 verdict=TARGET_MET rev=9bcb4fd5b598844f168230dc05e441721d95b272`
---

# Outcome verdict follows the gate summary (r72)

Rule: the contract verdict is `TARGET_MET` iff the gate's own last summary line parses as `MADO_LANDING_COUNTERS_SELFTEST: <p>/<n> assertions passed`, has `n > 0` and `p == n`, and the kill count is exactly `2/2`; the gate's exit status remains recorded evidence, not a verdict condition.

## Decision table

`quality/counters/c1-r72-landing-controls.py` implements this rule in `summary_green`, `outcome_exit` and `outcome_verdict` (lines 347–354 and 371–376).

| Last summary present/parses | Counts | Killed | Verdict | Harness outcome exit |
|---|---|---|---|---|
| Missing | — | Any | `TARGET_MISSED` | 1 |
| Present, malformed | — | Any | `TARGET_MISSED` | 1 |
| Present, parses | `n == 0`, including `0/0` | Any | `TARGET_MISSED` | 1 |
| Present, parses | `n > 0`, `p < n` | Any | `TARGET_MISSED` | 1 |
| Present, parses | `n > 0`, `p > n` | Any | `TARGET_MISSED` | 1 |
| Present, parses | `n > 0`, `p == n` | Not 2 | `TARGET_MISSED` | 1 |
| Present, parses | `n > 0`, `p == n` | 2 | `TARGET_MET` | 0 |

Gate exit status is irrelevant in every row; the final column is the harness's outcome, not the gate's recorded status. The implementation selects the last line starting exactly `MADO_LANDING_COUNTERS_SELFTEST:` and full-matches the grammar after stripping its trailing/leading whitespace. Thus a later malformed prefixed line does not permit fallback to an earlier green line. The frozen declaration's wording is “last parsed” summary; this paragraph describes the committed selector precisely, not an additional measured control.

## Four held-wrong controls

The held round-71 rule (`quality/counters/c1-r71-landing-controls.py`, lines 352–357) returns green iff `selftest_rc == 0 and killed == 2`. Every row below has `killed=2`; the frozen inputs and labels are `.ufo/waves/round-72/controls/c2-controls-r72.json`.

| Case | Gate report / status | Held r71 | r72 / frozen truth | Why the held result is wrong |
|---|---|---|---|---|
| `failing-summary-exit0` | `3/12`; exit 0 | `TARGET_MET` | `TARGET_MISSED` | Zero status cannot override nine reported failed assertions. |
| `green-summary-exit2` | `12/12`; exit 2 | `TARGET_MISSED` | `TARGET_MET` | Nonzero status cannot override the fully green assertion summary under this contract. |
| `no-summary-exit0` | Usage text only; exit 0 | `TARGET_MET` | `TARGET_MISSED` | No summary establishes assertion success. |
| `garbled-summary-exit0` | `twelve/twelve`; exit 0 | `TARGET_MET` | `TARGET_MISSED` | The summary does not parse as numeric assertion counts. |

The remaining controls are `green-summary-exit0`, `failing-summary-exit2`, `no-summary-exit2` and `green-summary-killed1`; both generations match their labels. The last control preserves the independent two-kill requirement.

## Measurement and provenance

The committed receipt `.ufo/waves/round-72/measurement-c2-r72.txt` records:

```text
MADO_R72_OUTCOME: cases=8 correct=8 base_correct=4 verdict=TARGET_MET rev=9bcb4fd5b598844f168230dc05e441721d95b272
C2_RC=0
```

Candidate correctness is 8/8 versus held 4/8, a bounded score `10 × correct / 8` of 10.0000 versus 5.0000. Base revision: `976684a27e99c2508037a60eec415f550f53d70e`. Frozen control SHA-256: `640fb44fdb1f31b4706b381c905fde4b5dae769bfd3e5b656bdb374bad58a793`. These are existing receipt results, not a run performed while drafting this entry.

The counting command `quality/counters/c2-r72-outcome.py` extracts the candidate and held harnesses at their respective commits and calls their committed decision functions on the same eight cases: candidate `outcome_verdict(gate_out, killed)`, held `outcome_verdict(gate_rc, killed)`. Counter success additionally requires exactly `correct=8` and `base_correct=4`; its exit map is 0 met, 1 measured miss, 2 usage/setup error with no contract line. Do not confuse that counting-command contract with the harness outcome decision table.

## Sourced ground and limits

The CPython 3.14.8 documentation says `wasSuccessful()` returns true iff all tests run so far passed, with unexpected successes also making it false. Its runner implementation first obtains `self.result = testRunner.run(self.test)`, then derives exit 1 from `not self.result.wasSuccessful()`, exit 5 from no tests run or skipped, otherwise exit 0 (when exit handling is enabled). The result object is upstream of the process status; this supports the distinction, not a universal prescription to trust arbitrary stdout. The cited local fetch receipts were available for reading but were not listed as committed blobs by this seat's `git ls-tree HEAD`; they are source-text receipts, not additional measurement execution evidence.

Declared scope is exactly `.ufo/waves/round-72/claims-declaration-r72.md` § C2: eight finite cases over the production summary grammar, scoring committed functions rather than a whole harness execution. **A summary/status contradiction is scored by the summary by design.** This does not authenticate a summary, prove that assertions actually ran, or establish general process health. Zero-total, excessive-pass and later-malformed-line rows explain implementation behavior; the eight-case measured denominator does not independently test those additional rows. C1's own-failure-detail rule is a separate calibration claim and is not measured by this C2 counter.

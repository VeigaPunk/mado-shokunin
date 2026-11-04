---
source: S444 (https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/unittest.rst, TestResult.wasSuccessful, lines 2127–2134) and S445 (https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/unittest/main.py, lines 270–277); local rule and measurement provenance below
verified-at: 2026-11-04
recheck: `python3 -I quality/counters/c1-r72-summary-credit.py --repo . --rev 9bcb4fd5b598844f168230dc05e441721d95b272 --base-rev 976684a27e99c2508037a60eec415f550f53d70e --scratch-root /fast/scratch/hyaku/mado-r72/R72ScribeEntryC1/recheck`
---

# Landing kill credit requires matching failure detail (round 72)

## Rule

Credit the M-Z kill iff the last summary matches `MADO_LANDING_COUNTERS_SELFTEST: <p>/<n> assertions passed`, has `n > 0` and `p < n`, and the captured run contains exactly `n − p` lines starting with `SELFTEST FAIL`, irrespective of process exit status.

This is claim C1's frozen predicate in `.ufo/waves/round-72/claims-declaration-r72.md`; the successor implements it in `quality/counters/c1-r72-landing-controls.py`, functions `last_summary()`, `count_fails()` and `credit()`. The base `quality/counters/c1-r71-landing-controls.py` instead calls `summary_shows_failure()` and does not require matching detail.

Both captured streams are read. Operationally, `last_summary()` selects the last line beginning exactly `MADO_LANDING_COUNTERS_SELFTEST:` and `credit()` full-matches its grammar; a malformed last marker does not cause a search back to an earlier valid one. `count_fails()` counts prefix-matching lines across the captured output, not only lines adjacent to the selected summary. It does not validate their assertion identities or text.

## Decision table

| Last selected summary parses | Positive total and failing fraction (`n > 0`, `p < n`) | Detail count equals `n − p` | Credit |
|---|---|---|---|
| no (absent or garbled) | — | any | no |
| yes | no (including green or zero total) | any | no |
| yes | yes | no | no |
| yes | yes | yes | yes |

## Named negatives and last-summary ties

These are fixture shapes declared in `quality/counters/c1-r72-summary-credit.py`; their classifications are recorded by the counting command in the frontmatter, in `.ufo/waves/round-72/measurement-c1-r72.txt`.

- **Bare echo — `bare-failing`:** a `0/2` summary without failure-detail lines earns no credit; the base incorrectly credits it.
- **Mismatch — `mismatch-detail`:** a `0/2` summary beside three failure-detail lines earns no credit because the deficit is two; the base incorrectly credits it.
- **`last-wins-pass`:** a failing `1/2` block followed by a green `2/2` summary earns no credit; the earlier failure summary cannot override the last one.
- **`last-wins-fail`:** a green `2/2` line followed by one failure-detail line and a failing `1/2` summary earns credit.

## Measurement, command and limits

The frontmatter counting command's committed receipt is `.ufo/waves/round-72/measurement-c1-r72.txt`, committed at `fd9ea03b554d6925594957c381f09e29a2ac159e`. It records candidate revision `9bcb4fd5b598844f168230dc05e441721d95b272` and base `976684a27e99c2508037a60eec415f550f53d70e`:

```text
MADO_R72_SUMMARY_CREDIT: cases=8 correct=8 base_correct=6 verdict=TARGET_MET rev=9bcb4fd5b598844f168230dc05e441721d95b272
C1_RC=0
```

Thus the candidate scores 8/8 and the held rule 6/8 on the same finite fixture set. These are receipt results, not a new execution by this scribe. The frozen acceptance rule requires both counts exactly; the two corrected classifications are the named negatives above. The counter runs real Bash fixture children, but those lanes are its own instrument, not the lane's real landing instrument; this is not general fault coverage.

**Not authentication:** replaying a captured summary together with matching failure-detail lines remains byte-indistinguishable from a genuine run. The arithmetic establishes internal agreement of the captured report, not that assertions executed or that their detail is truthful. A bare replayed summary is rejected; a complete matching replay is not authenticated or rejected on provenance grounds.

## Source provenance and scope

S444 documents `wasSuccessful()` as: “Return True if all tests run so far have passed, otherwise returns False.” S445 shows the runner obtaining `self.result = testRunner.run(self.test)` and, when exit is enabled, deriving failure exit from `not self.result.wasSuccessful()`; its separate no-tests branch uses exit code 5. These sources establish result-versus-process-status context, **not** the custom MADO summary grammar, failure-detail arithmetic, or replay authenticity. Those are local instrument facts.

The source identifiers are recorded in `corpus/SOURCES.md`. Scout receipts are now present at `.ufo/waves/round-72/w1/R72ScoutSources/receipts.jsonl` with excerpts in `quotes.md`; their initial absence is no longer a pending dependency. The unittest documentation digest is `d6522f68c29c8ced8d2d81c91cb41ac739f855e6c0b9831f4a0e5a81f7ae5b86`; the runner digest is `12de7da0fea92dbff8713ebe9904ada6dbd1e0a334d58861c6287ccfc0a261d2`. Scout provenance is attributed, not represented as a fetch executed by this scribe.

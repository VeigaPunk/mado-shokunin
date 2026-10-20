# RerunTally — partly falsified: counts reproduce, but green accepts a wrong counting rule

## Findings

### Medium — a green match does not bind the prose rule to the derived metric

`tools/mado-tripwire.py` is not involved here; this finding is specific to the round-20 tally checker. In `.ufo/waves/round-20/tally-check.py`, `check_statement()` selects one line and parses its numeric group (774–800), `claim_shape()` checks only standalone/fraction syntax (813–833), and the final result compares numeric tuples (953–960). The selected `key` is taken from `extract_regex` in `derive_plan()` (864–875); there is no check that the statement's rule words agree with that key. The receipt counter separately exposes `files` and `jsonl_paths` as different values (232–234).

Reproduced this with a valid-format adversarial green entry in a fresh `/tmp` `git init` repo, not in the lane: its committed sentence says “The total-file count, using JSONL-only filtering, is 1.” The receipt has two paths (`a.jsonl` and `b.txt`), so the total is 2 while `jsonl_paths=1`. The entry extracts `jsonl_paths` but attaches that value to the total-file sentence. Running `python3 -I /tmp/mado-r20w2-RerunTally-false-rule/.ufo/waves/round-20/tally-check.py /tmp/mado-r20w2-RerunTally-false-rule/.ufo/waves/round-20/false-rule-claims.json --set green --rev 77f29de513f9b4ee9a941945130dadaf5fbc9e38` (cwd `/tmp/mado-r20w2-RerunTally-false-rule`) returned:

```text
MATCH false-rule stated=1 derived=1
  ... claim="The total-file count, using JSONL-only filtering, is 1" | key=jsonl_paths | derive: ... receipt-files ...
TALLY_SUMMARY: set=green n=1 match=1 mismatch=0 error=0
EXPECT_SUMMARY: 1/1
```

The adversarial registry SHA-256 is `e02ef577a7b0d5b6ba58038992a003e1d353db4638df622bbd42161b72cd4f1d`; receipt SHA-256 is `b22a2f8a7d70c8d2a4fd33b52da10c8508dd5ef7460d999ce58d7402732b2b82`. This demonstrates that a green status proves numeric equality only, not that the sentence claims the rule used by the derive. It does **not** show that the current round-20 S096 wording is false; it is a checker-contract gap exposed by a counterexample.

### Confirmed — requested red and green set totals reproduce

Ran from cwd `/tmp/mado-r20w2-RerunTally`, with clone `HEAD=a4046a8216080d4004de3f268c62cf142095ac07`. Checker SHA-256: `21ce9dd57a47d975623aa9ca2bf53c3dadb8fa68b6f066a92461edba2fd2aea4`; registry SHA-256: `81eed3ebe33ec0bd2a7adbb5077c51a2624e00bccd945df83477f21674b3a48d`.

- `python3 -I /tmp/mado-r20w2-RerunTally/.ufo/waves/round-20/tally-check.py /tmp/mado-r20w2-RerunTally/.ufo/waves/round-20/tally-claims.json --set red` produced five `MISMATCH` rows (155 vs 154; three S096 5/13 vs 6/13 first-line; ten vs nine OM10) and `TALLY_SUMMARY: set=red n=5 match=0 mismatch=5 error=0`, `EXPECT_SUMMARY: 5/5`; exit 1 is the documented default for mismatches.
- `python3 -I /tmp/mado-r20w2-RerunTally/.ufo/waves/round-20/tally-check.py /tmp/mado-r20w2-RerunTally/.ufo/waves/round-20/tally-claims.json --set green --rev a4046a8216080d4004de3f268c62cf142095ac07` produced `TALLY_SUMMARY: set=green n=4 match=4 mismatch=0 error=0`, `EXPECT_SUMMARY: 4/4`, exit 0.

### Confirmed — S096 derive equals the closure's 8/13 and 6/13

Directly ran `pointer-token` with the pinned `fresh-pins.py` at both the registry revision and the closure tip. With cwd `/tmp/mado-r20w2-RerunTally` and `--counter-rev 1f7f995caa25627db804e996cccd87fe38a3a1b6 --token S096`, `--rev 1f7f995caa25627db804e996cccd87fe38a3a1b6` and then `--rev b435568540f9a28f4f7bb902af8dbe6a5b084dfe` each printed `denominator=13`, `first_line=6/13`, `any_line=8/13`. The checker’s registered green statements in `tally-claims.json:175–226` separately match 6/13 and 8/13. This agrees with the closure at `corpus/lessons/round-19-verifier-spotcheck.md:59–61`, which defines any matching pointer line and reports 8/13, versus 6/13 on the first matching line; `SCORECARD.md:1277` records the same correction. `fresh-pins.py` SHA-256: `a094be019968ef2cff4bf643be5f5f2b62d24b957310a4c0620a0ea2c5bcd789`.

## Residual risk and verification gaps

- The checker currently permits a registry entry to pair a sentence with one counting rule and derive a different metric that happens to have the same number; a `MATCH` alone cannot close that semantic gap.
- No `lsp` device/server is mounted in this session: `read xd://lsp` returned “No such tool.” I used direct source reads for cited code and ran the checker/counter; no text-search output is treated as semantic proof.
- This scoped tally task did not exercise a runtime, resume path, same-identity rerouting, or any saturation claim. No conclusions about those behaviors or axes are inferred.

## Limits

Only the requested tally red/green sets, the S096 counter at the registry and closure revisions, and one synthetic false-rule checker counterexample were run. The synthetic fixture is an adversarial test of checker acceptance, not lane content. No lane source, registry, scorecard, closure, or other report was edited; no other suite or isolation check was run.

## Installs

none

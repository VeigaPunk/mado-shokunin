# CriticC2Shadow — PRED-C2-r33-v1 rfind / decoy verification

Date: 2026-10-24. Lane scope: observation only; no gate files edited.

## Claim under test

PRED-C2-r33-v1's counter (`.ufo/waves/round-33/c2/count.py`) does NOT parse the
scorecard via `rfind` on the literal `Axis table re-derived at`. The `rfind`
pattern lives in a different gate, `quality/check-axis-scores.py`.

## Evidence — count.py parse method

`count.py:72-80` iterates every scorecard line and regex-matches only lines of
the form `^r33-claim-verdict: r32-C1 cited_entries=(\d+) verdict=(\S+) rev=([0-9a-f]{40})$`,
keeping the last match. No `rfind`, no `Axis table re-derived` string anywhere
in the file (verified by inspection of `count.py` rev as committed).

## Experiment — decoy after correct verdict line

Scratch scorecard at `/tmp/mado-c2-shadow/SCORECARD.scratch.md`:

```
r33-claim-verdict: r32-C1 cited_entries=7 verdict=honest-stop rev=d9ed38166cc3be8ef4c52b41d66ad94010feb047
Axis table re-derived at scratch-decoy navigation=0.0 calibration=0.0 operability=0.0 (decoy line placed AFTER the correct verdict line; would hijack an rfind-based parser)
```

(cited_entries=7 measured live: `git archive d9ed38166cc3be8ef4c52b41d66ad94010feb047 corpus` →
frozen r32 counter printed `entries=3 rows=0 cited_entries=7`)

Run:

```
$ python3 .ufo/waves/round-33/c2/count.py --repo . --scorecard /tmp/mado-c2-shadow/SCORECARD.scratch.md
PRED-C2-r33-v1 claim_mismatch=0 reason=match published=7 measured=7 verdict_word=honest-stop rev=d9ed38166cc3be8ef4c52b41d66ad94010feb047 verdict=TARGET_MET
exit=0
```

A trailing `Axis table re-derived at` decoy does not perturb the verdict: the
parser consumed only the anchored verdict line and still returned TARGET_MET.

## Residual defect — quality/check-axis-scores.py (NOT edited)

Defect still present. `quality/check-axis-scores.py:45`:

```python
flat = re.sub(r"\s+", " ", text)
idx = flat.rfind("Axis table re-derived at")
```

`PUB_RE` (line 33) is compiled but the actual last-publication lookup is this
`rfind` over whitespace-flattened text. Consequences, unchanged:

- Any later occurrence of the literal — including in a decoy, a code comment, or
  this very style of report if pasted into SCORECARD.md — becomes the "last
  publication" window (next 400 flattened chars, `line = flat[idx:idx + 400]`).
- Because `flat` collapses newlines, a following unrelated paragraph is parsed
  as part of the publication window.

## Conclusion

- PRED-C2-r33-v1 counter: anchored-regex last-match scan; immune to the
  `Axis table re-derived` decoy. Hypothesis "count.py shares the rfind defect"
  falsified.
- `quality/check-axis-scores.py`: `rfind` defect confirmed still live at line 45;
  left untouched per scope.

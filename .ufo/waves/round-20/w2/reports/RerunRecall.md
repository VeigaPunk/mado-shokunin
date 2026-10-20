# RerunRecall — partly falsified: 28c6837 passes; 9c54c56 does not

## Findings (severity order)

- **Low — the 6/6 result is revision-specific, not true at both requested revisions.** In the private clone `/tmp/mado-r20w2-RerunRecall` (origin removed), I ran the committed harnesses with each `REV`:
  - `python3 -I /tmp/mado-r20w2-RerunRecall/.ufo/waves/round-19/tw-recall.py 28c6837` exited 0: `incident_lines=6`, `detected=6`, `score=10.0`; each of the six rows was detected. Tool SHA-256: `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`.
  - `python3 -I /tmp/mado-r20w2-RerunRecall/.ufo/waves/round-20/tw-recall-split.py 28c6837` exited 0: `detected_observed=5`, `detected_lead=1`, `detected_unmarked=0`, `undetected=0`, `control_lines=20`, `control_findings=0`. Its `inputs/r13-root.jsonl:4` row is exactly one `package_query` / `pacman:-Q` finding with `evidence=lead`; the other five incident lines are observed.
  - The same two commands at `a4046a8216080d4004de3f268c62cf142095ac07` also passed with the same tool SHA and same split totals.
  - At `9c54c56`, `tw-recall.py` instead exited 0 with `incident_lines=6`, `detected=3`, `score=5.0` (tool SHA-256 `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`). `tw-recall-split.py` confirms `detected_unmarked=3`, `undetected=3`, and still `control_lines=20`, `control_findings=0`. The missed rows are `inputs/r13-root.jsonl:4` and `inputs/r14-source-safety.jsonl:2-3`. Thus 6/6 = 5 observed + 1 lead is verified for the repaired tool at 28c6837 (and lane tip), but not for the historical tool at 9c54c56.
  - Harness provenance: `git show 28c6837:<script> | sha256sum` and the same at lane tip matched for both scripts (`tw-recall.py` SHA-256 `220902982fb1f0561811e6483ea53fe08ba2b8f939f396a440ab63944e4cbd28`; `tw-recall-split.py` SHA-256 `5c8f1424833de506f8f839164ff284614ed5080b6015cf615b61b31e30bc7956`). Neither harness path exists in the 9c54c56 tree (`git ls-tree ...` returned zero entries), so the 9c54c56 measurements use the current committed harness against that historical tool, not a harness version from that commit. The revision-sensitive output is a counterexample to any reading that expects 6/6 at both revisions, and demonstrates that the harness is not returning a fixed 6/6 result.

## Frozen-input digest check

The five input SHA-256s recomputed from `git show 9c54c56:.ufo/waves/round-18/frozen/<path>` match the pins in `.ufo/waves/round-18/frozen/expected.json:5-22` exactly; the same hashes were observed at the lane tip. In order: `r15-libinput-events.jsonl` `7118b8831c95491e11ec96eaa9779e37a2d955c5cd9e02612c6e25461a0d7a90`; `r13-global-capture.jsonl` `265528128b03f58713c91fe60ddd43119883040e0991a5c478ea54eebf5019c9`; `r14-review-source-bar.jsonl` `4bd77154c6b80a930784c32cb0467e5323ad26fbcd1e4b4a6c7f685027bd1232`; `r14-source-safety.jsonl` `8635cca2c00fddc200599ebd7c62edb2dacc85d25d83d5f894a02b6320c8bac1`; `r13-root.jsonl` `24e3c790678ccbb3416cc12c2cbf5e114db418ffbf95979f5cfba1b34527ba11`. `git diff --quiet 9c54c56 a4046a8216080d4004de3f268c62cf142095ac07 -- .ufo/waves/round-18/frozen/` returned 0 (no frozen-tree changes).

Evidence for the checks: `.ufo/waves/round-19/tw-recall.py:49-60,73-84` fixes the denominator and validates each input digest before scanning; `.ufo/waves/round-20/tw-recall-split.py:50-66,81-95,110-129` validates pins, requires 6 incident / 20 control lines, counts findings on controls, and emits the split. Commands above are the rerun output excerpts; tool and harness SHA-256 values are recorded inline.

## Limits

- The current harness explicitly returns 2 for a digest mismatch (`tw-recall.py:56-60`, `tw-recall-split.py:50-54`), but I did not inject a deliberately corrupted frozen input; the five source digests were independently recomputed and matched.
- Historical 9c54c56 did not contain either rerun harness; only the historical tool revision was tested there, using the identical harness bytes available at 28c6837 and lane tip.

## Installs

None.

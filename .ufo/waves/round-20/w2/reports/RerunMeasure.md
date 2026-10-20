# RerunMeasure — holds: The requested c1 reruns reproduce 20/28 at 1f7f995 and e629f73, then 22/30 at a4046a8; QUALITY is append-only.

## Findings

No actionable findings for this assignment. The measured c1 transition and the append-only claim hold.

## Evidence

- Re-ran the revision-bound counter in the isolated clone, copying `measure.py` from each requested commit before each run:
  - `python3 /tmp/mado-r20w2-RerunMeasure/.ufo/waves/round-17/measure.py 1f7f995caa25627db804e996cccd87fe38a3a1b6` → `c1: {"criteria": 28, "lesson_cited": 20, "score": 7.1429}`.
  - `python3 /tmp/mado-r20w2-RerunMeasure/.ufo/waves/round-17/measure.py e629f731172b8238caffe50f152217ce56535fb4` → `c1: {"criteria": 28, "lesson_cited": 20, "score": 7.1429}`.
  - `python3 /tmp/mado-r20w2-RerunMeasure/.ufo/waves/round-17/measure.py a4046a8216080d4004de3f268c62cf142095ac07` → `c1: {"criteria": 30, "lesson_cited": 22, "score": 7.3333}`.
  - Counter SHA-256 for each commit's copied `measure.py`: `de4c422b55c67f822cb9f0be21fe5e879e3d15c46830565c1c661381817cfcdc`. The counter defines c1 as a literal numbered-line/`lessons/` fraction at `.ufo/waves/round-17/measure.py:10-13,82-99`.
- Verified append-only against baseline `1f7f995caa25627db804e996cccd87fe38a3a1b6`: `git show BASE:corpus/QUALITY.md` was byte-compared with the same-length prefix of `git show a4046a8216080d4004de3f268c62cf142095ac07:corpus/QUALITY.md`; output was `baseline_entire_file_is_final_prefix=PASS` (19,061 bytes). The `git diff --numstat` output was `43  0  corpus/QUALITY.md`; shortstat was `1 file changed, 43 insertions(+)`. Therefore all previous QUALITY bytes, including criteria 1–28, remain byte-identical at a4046a8.
  - Baseline QUALITY SHA-256: `461bcde2f5e75ace6cdda36f6708a4242c4a959cf7d40f40d5399b92157505b6` (228 lines).
  - Final QUALITY SHA-256: `4da2cd62576ebea5a80028391e3a657ffa0505dd950f7ae563abb67cf47f4dd4` (271 lines).
- The two added numbered lines that increase `lesson_cited` are exactly:
- `corpus/QUALITY.md:232` — exact counted line:
  ```text
29. An isolation harness fails closed: every setup step (namespace creation, each bind or mount, each post-mount verification that the target now holds the stub) is tested on its own, and any failure — or a missing target or stub — aborts before the payload starts; `set -e` with a non-final `&&` member is not a gate, and a harness that exits 0 without running its payload under a forced failure counts as failing open (lesson: lessons/round-20.md#mistakes M2; outside lessons/round-19-verifier-spotcheck.md R19-V4).
  ```
- `corpus/QUALITY.md:249` — exact counted line:
  ```text
30. A detector change credited for recall is admitted only beside its precision evidence: committed negatives of the shapes the new rule could misread (pure data, formatters, names bound or shadowed in the text), each read at the pre-change and the changed tool; a whole-corpus diff against the pre-change tool that lists every added and relabelled row; and a machine-readable marker on every row the detector cannot tie to a visible execution path (`evidence: lead`), never the shape of an observed row (lesson: lessons/round-20.md#mistakes M1; outside lessons/round-19-verifier-spotcheck.md R19-V3).
  ```

## Residual risk and verification gaps

This verifies the revision-bound literal c1 counter and the QUALITY byte-prefix claim only. The measure defines citation presence, not whether the cited lesson substantively supports either criterion. Tripwire precision, held-out cases, and the whole-corpus no-harm diff are outside this rerun and were not verified here. In final QUALITY, criterion 30 is the detector-precision criterion; the withdrawn count-rederivation proposal is not a separate QUALITY line counted by c1.

## Limits

The measurement was run from `/tmp/mado-r20w2-RerunMeasure`, not the lane worktree. The counter's c1 result is a literal line count, as documented in its source; no independent semantic assessment of the cited lessons is claimed.

## Installs

None.

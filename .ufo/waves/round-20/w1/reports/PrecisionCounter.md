# PrecisionCounter — implemented and synthetic proof passed

## Findings

- **Files changed:** `.ufo/waves/round-20/tw-precision.py` and this report only. Counter SHA-256: `d9ab87a696c1357221a455ebd7004f26a1275986418f56e34ebefdb1a38440a2` (235 lines). Its CLI, `SUITE_PIN = None`, and committed-revision lookup are at `tw-precision.py:18-68`; it reads the pinned `expected.json` and digest-checks each committed case at `:110-152`; the isolated `python3 -I` scan and multiset comparison are at `:155-187`; the JSON summary and exit-2 error handling are at `:189-235`.
- The counter resolves tool and suite revisions to commits, loads only `git show` bytes, validates case paths and SHA-256 values, and writes the tool/cases to a temporary directory. It compares exit status and a multiset of `(class, rule, line, evidence)`; a missing evidence key normalizes to `observed`. It reports each case's `pass`, `got`, and `want`, family pass/total counts, the tool digest, canonical suite pin, and four-decimal score. Unsupported families, malformed verdicts, invalid revisions, digest mismatches, and scanner return codes outside 0/1 are could-not-evaluate (exit 2). Transcript fixtures are passed only as scan input, never executed.

## Retained synthetic proof

- Temporary test clone: `/tmp/mado-r20-PrecisionCounter`; observed clone starting HEAD: `e629f731172b8238caffe50f152217ce56535fb4`.
- The counter and a synthetic scanner were committed only in that `/tmp` clone. Tested counter/tool revision: `1792305adbfa21ecab597fe84eac8c8acb814120`; synthetic suite pin: `649e6fb2367502c26e5a6ba114463a695924abad`.
- Invocation: `python3 -I /tmp/mado-r20-PrecisionCounter/.ufo/waves/round-20/tw-precision.py 1792305adbfa21ecab597fe84eac8c8acb814120 --suite-rev 649e6fb2367502c26e5a6ba114463a695924abad` → exit 0; case pass vector `[true,false,true,false,true,false]`; P `3/6`, other families `0/0`; score `5.0`.
- The six synthetic cases exercised exit-code pass/fail, finding-multiset pass/fail, and missing-evidence behavior: an unmarked actual row matched expected `observed` (pass), but did **not** match expected `lead` (fail).
- Digest-tamper refusal: after changing a committed synthetic case without updating its expected digest, the counter returned exit 2 and printed `could_not_evaluate: digest mismatch for .ufo/waves/round-20/precision/pass-exit.jsonl` (expected `2a090d0c…`, got `8cb6d905…`).
- Unset-pin refusal: invoking the counter without `--suite-rev` returned exit 2 with `could_not_evaluate: suite pin is unset; supply --suite-rev PIN`.

## Limits

The round-20 `precision/` suite was absent from the lane tree when inspected, and `SUITE_PIN` remains `None` as required for L1 to fill after the suite lands. Therefore the proof used only the synthetic suite in `/tmp`; no real precision-suite result is claimed. No full suite, build, lint, or formatter was run.

## Installs

none

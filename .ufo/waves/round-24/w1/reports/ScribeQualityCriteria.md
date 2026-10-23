# Draft: QUALITY criteria 33–35

Status: scoped draft only. `corpus/QUALITY.md` was not edited. The proposed text below follows the numbered criterion style and runnable-check references in criteria 29–32.

## Proposed criteria

33. A detector or gate repair earns no-harm credit only against discovery attacks frozen before the patch, not merely the existing corpus, precision suite, oracles, and selftests. Include base-versus-tip cases for global-store silent misses, recall losses where the base reports a lead but the candidate reports nothing, and frame/scope behavior including frame reuse, nested binders, and match/with binders; retain the outcomes at both revisions and do not count a silently lost finding as clean. Runnable check: `python3 -I .ufo/waves/round-24/quality/check-registration-order.py`. (lesson: `lessons/round-23.md#mistakes M23-4`)

34. A scratch measurement receipt is admissible only when its result paths resolve to the same absolute locations for writer and reader, prior result files are removed before each run, and the receipt identifies the sha256 of the tool bytes actually measured. A result read from stale or differently located output is not evidence about the measured run. Runnable check: `python3 -I .ufo/waves/round-24/quality/check-receipt-provenance.py`. (lesson: `lessons/round-23.md#mistakes M23-5`)

35. Fixtures first discovered after a patch, including late-cell and closure-neighbour cases, cannot be credited retroactively as pre-patch guards. Register those fixtures before any patch; if discovery comes after a patch, withdraw the affected production change to the base and assess a new patch only after the fixtures are registered. Runnable check: `python3 -I .ufo/waves/round-24/quality/check-registration-order.py`. (lesson: `lessons/round-23.md#mistakes M23-7`)

## Scoped findings and provenance

- M23-4 records that the initial C1 classifier missed a global-store case, 13/45 recall shapes, and frame/scope regressions; the registered 1356-file corpus, precision suite, oracles, and selftests lacked those shapes. Its lesson records the base-versus-tip attack outcomes and says discovery attacks must run before reporting an after-value.
- M23-5 records a scratch run whose relative output path did not resolve where it was read, causing stale earlier-tool files to be reported briefly as regressions. The lesson says the corrected run uses absolute paths, deletes results before each run, and prints the measured tool sha256.
- M23-7 records late-cell and closure-neighbour findings without a registered guard; production bytes were withdrawn to base, and the next registration must include the fixtures before any patch.
- These are proposed admission criteria, not results of the two round-24 checks. Neither check was run here; no pass/fail result is claimed. Check paths are included as requested and were not inspected or altered.

## Actions and exact read results

Read-only review used these repository paths/ranges:

- `.ufo/waves/round-24/registration.md` (read snapshot `4986`): confirmed the round-24 routed repair is to add lesson-cited QUALITY criteria for M23-4, M23-5, and M23-7, with checks shown able to fail.
- `corpus/QUALITY.md` (snapshot `205D`), especially lines 230–314 and 296–314: reviewed the form and content of criteria 29–32 and later applications.
- `corpus/lessons/round-23.md` (snapshot `B6E6`), lines 20–26, line 23, line 229, and lines 231–237: reviewed the routed mistake records and their surrounding correction.
- An initial read of the requested report path returned “not found”; this report creates it.

No shell commands, checker invocations, builds, tests, or edits to product files were performed. Only the requested report path is touched by this work.

## Verdict

Draft prepared for criteria 33–35 with the requested lesson citations and runnable-check paths. `QUALITY.md` remains unchanged. Check execution and integration are not claimed.

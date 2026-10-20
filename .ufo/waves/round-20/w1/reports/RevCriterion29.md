# RevCriterion29 — criterion 29 is distinct and its red is real; correct the draft and widen its check before integration

## Verdict

QUALITY 29 addresses a real, independently reproduced setup-to-payload fail-open, and it does not restate criteria 1–28. It satisfies R19-V1's fresh-registration and grounded-red requirements. The current ScribeQuality draft has a nonexistent lesson/check path and overstates the historical fixture's provenance; the current runnable checker demonstrates the incident's bind-failure shape, but not every setup stage claimed by that draft.

## Findings (severity order)

### Medium — ScribeQuality's criterion 29 citation, checker path, and historical-fixture description are stale

`.ufo/waves/round-20/w1/drafts/ScribeQuality.md:7-10` cites `lessons/round-20.md#mistakes M2` and names `.ufo/waves/round-20/harness-fail-closed.py`, while the corpus lesson listing has no `round-20.md` and the round-20 wave has `isolation-check.sh`/`isolate.sh`, not that Python checker. A lexical `lessons/` match would count the citation in measure.py, but would not make the absent source valid. M12 is in the wave-2 table at `corpus/lessons/round-19.md:87`, not the first `#mistakes` section; its captured-by cell is superseded by `:127-129,145`, which says the scan missed the written-script probe and captured-by was self-report only.

The ScribeQuality draft also calls its inputs “the committed round-19 first inns.sh” and gives byte sizes/digests. `RevengeInnsHarness.md:29-40` establishes the accurate qualification: the first script was recovered from a session transcript; `.ufo/waves/round-20/evidence/inns-r19-shape.sh` is faithful to the vulnerable control-flow shape, **not** a byte-for-byte or environmental replay. At this review it is 1,216 bytes, sha256 `8bd507f0ea39d4d876359a0f5a1f798e810cda3c59293487af35d3a8df37ce9c`. Do not attribute its digest to the historical `/tmp/sgp/inns.sh`.

Use the existing M12 record with its correction and the outside disposition, e.g. `lessons/round-19.md:87,127-129,145 (M12 and correction); outside lessons/round-19-verifier-spotcheck.md:124,152 (R19-V4)`. That is both a real lesson citation and on the numbered line for the literal c1 counter.

### Medium — the current checker does not cover the draft's “every arming step” scope

`isolation-check.sh:40-50` injects a failing PATH `mount` for **one existing temporary target**; `:72-80` checks one successful target. `IsolationHarness.md:62-63` explicitly leaves repeated-target, forced-`cmp`-failure, and payload-status cases untested. The current checker therefore proves the incident-shaped bind-failure case and rejects an always-fail harness, but it does not establish that every setup stage/target is gated. If retaining the draft's “every arming step”/“missing or unverified target” wording, extend the runnable check to force failures independently at unshare, each bind, and post-bind comparison (and exercise each target), with the canary absent and nonzero status in every failure arm. Otherwise make no claim that these untested branches were exercised.

## Non-duplication and red evidence

- **Not a restatement:** QUALITY 26 (`corpus/QUALITY.md:144`) prevents a failed pipe/command-substitution producer from laundering a value; 29 prevents payload execution after failed isolation setup. 21 (`:82`) governs the host-pause policy and static action-plan classifier, not harness control flow. The closest overlap is the general need to preserve failures, but the invariant and observable red differ. Criteria 24, 27, and 28 govern receipt producer identity, source-anchor durability, and supersession pointers, respectively, not setup-to-payload gating.
- **R19-V1:** the closure says preserve the ≥21/29 miss and do not add duplicates or redefine the target (`corpus/lessons/round-19-verifier-spotcheck.md:149`). The round-20 SCORECARD pre-registers this as a new claim at `SCORECARD.md:1228,1265-1270`, at the pre-registration revision `e629f73`; the incident is the grounded red. Its note says the new criteria do not restate 24/27/28; 21 and 26 are the nearer neighbors, distinguished above.
- **Counter compatibility:** `python3 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/measure.py e629f73` returned c1 `criteria=28`, `lesson_cited=20`, `score=7.1429`. The counter counts `^[0-9]+\. ` and requires `lessons/` on that same numbered line. Criterion 29 contributes one of the registered two; 29 and 30 with own-line lesson citations produce 22/30 = 7.3333.
- **The historical red is real:** `SentinelGatePath.md:75-79` reports that all 16 binds failed with “must be superuser to use mount”; `[ -e ] && mount && echo` under `set -e` did not stop the script, and `/usr/bin/hyprctl probe` ran (`unknown request`, rc=0). The non-author closure records the breach and routes R19-V4 at `corpus/lessons/round-19-verifier-spotcheck.md:124,152`. The independent `ScoutUnshareHost.md:32-47` reproduced mount rc 32, a `/tmp` canary write, and outer rc 0 even with `set -e`; its lines 49-68 show a gated setup aborting without the canary. No real host probe was repeated here.
- **Checker red/green observed:** in `/tmp/revc29` copies, `bash isolation-check.sh ./inns-r19-shape.sh` printed `forced mount setup failure (exit 32)`, `harness exit: 0`, `FAIL_OPEN`, then `POSITIVE_CONTROL_OK`; checker exit 1. `bash isolation-check.sh ./isolate.sh` printed `harness exit: 125`, `FAIL_CLOSED`, `POSITIVE_CONTROL_OK`; checker exit 0. The payload only writes its supplied canary under `/tmp`; the positive control uses a private user/mount namespace and `/tmp` target. An always-failing control printed `NEVER_RUNS` and was rejected (exit 1). This confirms the current check's incident-shaped failure and positive-control behavior, not untested setup branches.

## Recommended criterion line and runnable check

```text
29. An isolation harness returns nonzero and skips its payload if required setup fails; every required bind and post-bind byte check gates payload execution, and `set -e` does not turn a failed non-final `&&`/`||` member into a gate (lesson: lessons/round-19.md:87,127-129,145 (M12 and correction); outside lessons/round-19-verifier-spotcheck.md:124,152 (R19-V4)).
    Runnable check: `bash .ufo/waves/round-20/isolation-check.sh HARNESS`
    Red: `.ufo/waves/round-20/evidence/inns-r19-shape.sh` reports `FAIL_OPEN`, exit 1, on the forced bind failure; its fixture is a safe control-flow reproduction, not the historical script bytes. Green: `.ufo/waves/round-20/isolate.sh` reports `FAIL_CLOSED` and `POSITIVE_CONTROL_OK`, exit 0. The payload is a `/tmp` canary write, never a host probe. Extend the current checker with per-stage/per-target forced failures before claiming every setup branch is tested.
```

## Residual risk and verification gaps

- The current checker injects `mount` failure through PATH. [INFERENCE] A future harness using an absolute mount path could bypass that injection; the reviewed historical shape and `isolate.sh` use PATH-resolved `mount`.
- No test was run here for missing targets, `cmp` mismatch, unshare refusal, multiple targets, or payload nonzero-status propagation; see the preceding finding. Positive-control availability is host/user-namespace dependent.
- `inns-r19-shape.sh` reproduces the vulnerable control-flow but is not a byte-identical historical artifact. Its red result is supported by the round-19 incident report and a separate safe canary reproduction.
- No LSP device/server was mounted (`read xd://lsp` returned “No such tool”); review evidence is source/report reading and the stated shell executions. No semantic-reference absence is claimed.
- No build, lint, general suite, or live host-surface operation was run.

## Limits

This review covers the QUALITY 29 anti-duplication question, the round-19 red evidence, the current proposed criterion/check artifacts, and the c1 counting contract. It does not review criterion 30, the full round-20 tripwire change, or the host-state impact of the historical probe; the closure itself states that absence of host-state change was not independently measured.

## Installs

none.
# R72RevC2 — adversarial C2 review

Axes: C1 calibration (unchanged by this review); C2 operability (summary-driven outcome and faithful evidence).

Recommendation only: the frozen 8/8 result is supported for its declared finite function table, but is not evidence of chronological last-summary correctness across streams or complete execution success. No production edits or admission/judgment performed.

Reviewed committed candidate `9bcb4fd5b598844f168230dc05e441721d95b272` against base `976684a27e99c2508037a60eec415f550f53d70e`, including the actual harness delta. Paths below are repository-relative. `H` means `quality/counters/c1-r72-landing-controls.py`; `C` means `quality/counters/c2-r72-outcome.py`; `D` means `.ufo/waves/round-72/claims-declaration-r72.md`.

## Reproduction and retained evidence

Executed once successfully (exit 0):

```sh
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-72/w1/R72RevC2/repro.py --scratch-root /fast/scratch/hyaku/mado-r72/R72RevC2
```

The retained driver extracts exact committed bytes using read-only `git show`, executes real Python gate processes with sequential flushed writes, and injects their captured CompletedProcess into the committed `measure()` body. Other child responses use the harness's own `_scripted_run` fixture, giving two credited kills. Thus the summary-capture and outcome call sites really execute; extraction, mutant git operations, and mutation child results are scripted, not end-to-end verified. No real git mutation occurs. Synthetic contract revision is `a` repeated 40 times, not a real measurement revision.

Observed output retained here (all rows have killed=2/2):

| Driver case | Gate rc | selftest field | green | Verdict | Harness rc |
|---|---:|---|---|---|---:|
| green-then-real-setup-exit2 | 2 | 12/12 | yes | TARGET_MET | 0 |
| same-stream-green-then-fail | 0 | 11/12 | no | TARGET_MISSED | 1 |
| same-stream-fail-then-green | 0 | 12/12 | yes | TARGET_MET | 0 |
| stderr-only-green | 0 | 12/12 | yes | TARGET_MET | 0 |
| stderr-fail-then-stdout-green | 0 | 11/12 | no | TARGET_MISSED | 1 |
| stderr-green-then-stdout-fail | 0 | 12/12 | yes | TARGET_MET | 0 |
| green-then-garbled-fraction | 0 | 12/12 | no | TARGET_MISSED | 1 |
| green-then-garbled-no-fraction | 0 | none | no | TARGET_MISSED | 1 |

Every row's `counter_oracle` equalled the candidate verdict. The base function returned TARGET_MISSED only for the rc-2 row and TARGET_MET for the seven rc-0 rows.

## Findings, severity ordered

### Medium — stream concatenation defeats chronological last-wins (defect; false-positive and false-negative outcome)

Sentence: D:89–92 says the extracted instrument's **last** parsed summary decides. Code: H:173–175 captures stdout and stderr separately; H:475 constructs `dec(r.stdout) + dec(r.stderr)`; H:298–301 selects the last prefix line in that artificial order. Any stderr summary takes precedence over every stdout summary, irrespective of emission order.

Repro: run the command above and inspect `stderr-green-then-stdout-fail`. The child flushes green 12/12 to stderr, then failing 11/12 to stdout. The actual final summary fails, but the harness reports:

```text
MADO_R72_SELFTEST instrument=quality/landing-counters.sh rc=0 summary=12/12 green=yes
MADO_R72_LANDING_CONTROLS: selftest=12/12 mz=pass mr=pass killed=2/2 baseline=0/2 verdict=TARGET_MET rev=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

Reversing the colors (`stderr-fail-then-stdout-green`) incorrectly reports TARGET_MISSED after the final green summary. This is not the intentional exit-status override. The eight controls carry one already-combined `gate_out` each and cannot expose capture ordering. If “last” means only last in stdout-then-stderr concatenation, the code conforms to that narrower interpretation, but neither the frozen sentence nor its limits specifies that precedence. Preserve the frozen result; document this limitation or address capture ordering in a future claim rather than describing global last-wins as proven.

### Low — selftest fraction is not the parsed summary that decides (receipt defect)

Sentence/interface: H:49 promises `selftest=<p/n|none>` and H:17–19 describes a parsed summary. Code: H:305–308 finds any digit fraction in the last prefix line, while H:347–354 requires a full grammar match. H:379–382 prints the former and judges with the latter.

Repro: `green-then-garbled-fraction` appends `MADO_LANDING_COUNTERS_SELFTEST: 12/12 assertions passed INVALID`. Observed retained evidence:

```text
MADO_R72_SELFTEST instrument=quality/landing-counters.sh rc=0 summary=12/12 green=no
MADO_R72_LANDING_CONTROLS: selftest=12/12 mz=pass mr=pass killed=2/2 baseline=0/2 verdict=TARGET_MISSED rev=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

The printed 12/12 is a substring of a rejected line, not an accepted summary. Thus the terminal contract alone cannot explain why full selftest and two kills miss; the preceding `green=no` makes rejection visible but not its reason. This does not incorrectly green the run. A future receipt should distinguish valid parsed fraction from malformed-summary text.

### Informational — setup failure after green is accepted intentionally (declared limit; broader success claim would be false-positive)

Repro: `green-then-real-setup-exit2` writes a valid green summary, prints `fatal: setup dependency unavailable` to stderr, and exits 2. This is an explicit simulated setup-failure gate, not a real missing-host-dependency experiment. Observed `rc=2 summary=12/12 green=yes`, terminal TARGET_MET, harness rc 0. Base returns TARGET_MISSED.

Sentence vs code: D:89–92 explicitly excludes exit status from the outcome; H:371–376 has no rc argument, and H:474–478 records rc without using it as a gate. The frozen controls explicitly label `green-summary-exit2` TARGET_MET (controls JSON:20–24). Therefore MET is honest as the declared summary-and-kills predicate, not as “the entire child completed successfully” or “no setup failure occurred.” There is no frozen-contract defect here; a claim of generic execution health would be overreach. The measurement receipt's TARGET_MET must retain this qualification.

### Informational — duplicate predicate is a self-consistency check, not independent evidence (limit)

C:94–105 duplicates H:298–301 and H:347–354: reverse prefix selection, full regex match, positive denominator, equality, and two kills. In C:259–261 it checks frozen JSON labels against that duplicate. It shares both the malformed-tail interpretation and lack of stream identity/order.

Important distinction: C:222–228 actually scores the candidate against the JSON's frozen `expected` strings; `expected_from_summary` is **not** the measurement oracle. The independent pre-freeze labels and held 4/8 control retain value. Calling the whole measurement circular would be a false-positive review finding. What weakens is the selftest's ability to detect a common parser-specification mistake, and extrapolation beyond those eight labels. The same counter oracle agreeing on all eight adversarial rows above does not independently establish chronological correctness.

## Attacks that did not break the specified behavior

- Green then failing summary on one stream correctly selects 11/12 and misses; failing then green correctly selects 12/12 and meets.
- A summary printed only on stderr is read and can meet.
- Missing/garbled summary does not meet. A garbled trailing prefix suppresses an earlier valid green: H:298–301 picks the last **prefix**, then H:350 rejects it. “Last parsed” versus “last candidate, which must parse” remains a wording ambiguity; conservatively rejecting malformed tails is not promoted to a separate defect here.
- Both exit and verdict callers in H:371–382 and H:575–578 receive the same captured output; no stale rc-based caller was found in the scoped harness. Grep was used only for literal location discovery, not semantic proof.

## Residual risk and verification gaps

- `xd://lsp` returned “No such tool”; no LSP status, references, definition, or diagnostics device is mounted. Semantic checks were unavailable; the review used explicit source/function/call-site inspection and committed-code reproduction instead.
- Re-read frozen C1/C2 measurements and baselines without rewriting or rerunning them. C2 receipt records candidate 8/8, held 4/8, TARGET_MET; C1 records 8/8 and held 6/8. This review does not dispute those finite recorded scores.
- No whole real landing harness measurement, host setup failure, full suite, or no-harm verification was run. Counter scope explicitly excludes whole-harness execution (D:99–102; C:17–19). No saturation beyond the finite table is supported.
- One Python interpreter executed the review driver and its gate children; no alternative agent runtime or rerouting was invoked. Same-identity rerouting and `resume_continuity_v1` preflight behavior are not present in these outcome functions and are outside this assigned diff; no resume claim is made.
- Writes stayed in this seat's directory and declared scratch. Scratch removed after retaining evidence here. No installs, production edits, git/jj mutations, service/config/network probes, or peer broadcasts.
- The final assignment trailer pointed outside the hard only-write directory; the report is intentionally inside `w1/R72RevC2/` as the explicit seat and hard bounds require.

Self-evaluation: accuracy 4 (scripted non-gate child responses, explicitly bounded); completeness 4 (no LSP available); clarity 4 (frozen wording ambiguity retained); actionability 4 (precise reproducer, no production patch by design); conciseness 4 (evidence retained inline for cleanup). Overall 4.0. Highest-value follow-up is chronological capture coverage, then parsed-status receipt clarity. Would the user agree: expected yes, with the stated evidence boundaries.

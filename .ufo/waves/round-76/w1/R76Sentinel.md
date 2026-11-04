# R76Sentinel — scoped security and hygiene review

Axes: scratch containment; environment isolation; challenge privacy; fixture/repository safety; evidence provenance.

Method: read-only source/receipt inspection and targeted pattern searches. No counters, fixtures, injected environments, offensive trials, host probes, or verification suites were executed. No production or committed evidence files were changed. No tools were installed. Paths below are lane-relative. Source last-change revision observed by read-only git log: `cb713254ee9926e036e594312fdc61b57825526b` for the three successor instruments.

## Findings

### P2 — C2 retains loader/startup variables in its Git children

- Evidence: `quality/counters/c2-r76-shapes.py:89-99`: `git_env()` copies every caller variable except names starting `GIT_`; `run()` supplies that mapping to each Git subprocess.
- Exploit path [INFERENCE, not exercised]: a caller-controlled `LD_PRELOAD` reaches the dynamic loader of `git`, allowing code to execute before the read-only Git operation. Caller HOME/PATH are also retained, so this is not a hermetic environment boundary. This can affect evidence or produce writes unrelated to the selected scratch root.
- Exact existing mitigation: lines 90-93 remove inherited `GIT_*`, force `GIT_OPTIONAL_LOCKS=0`, `GIT_NO_REPLACE_OBJECTS=1`, and `LC_ALL=C`. These protect replacement-object reads, not non-Git loader variables.
- Smallest remediation: use the C1 explicit child-environment allowlist, private HOME/TMPDIR, disabled global/system Git config, and a trusted executable search path rather than copying the ambient environment.
- Qualification: C2's 59 control sources are parsed/classified, not executed. `BASH_ENV`, `PYTHONPATH`, and `MADO_LANDING_NONCE` survive in the Git child environment but no inspected C2 path launches Bash or a Python fixture that consumes them. `LD_PRELOAD` is the direct executable influence. This does not establish that the committed measurement was contaminated.

### P2 — committed evidence-generation prototypes bypass scratch-root validation

- Evidence: `.ufo/waves/round-76/proto/held-r76.py:49-60,81-84` only applies `abspath`, creates the supplied directory, and opens predictable `held-c2.py` / `held-harness.py` with ordinary `open(..., 'wb')`. Lines 38-40 also launch Git with the fully inherited environment and no timeout. `.ufo/waves/round-76/proto/label-derivation-r76.py:20-28` uses a fixed default scratch path or an unvalidated caller path and opens predictable `candidate.py` ordinarily.
- Exploit path [INFERENCE, not exercised]: a pre-populated scratch containing one of those output-name symlinks redirects the write outside scratch; `held-r76.py` then imports its extracted file (lines 63-65), increasing the consequence of a concurrently mutable scratch tree. A caller can also select a tmp-family root; these prototype entry points do not reject it before their first writes.
- Impact: evidence-generation helpers do not provide the same containment guarantee as the advertised successor counters. No outside-scratch write was observed in this review.
- Exact partial mitigation: label derivation uses the sanitized `c76.git_env()` at lines 22-24; held baseline later uses it at lines 87-90 for fixture execution. Neither mitigates the earlier scratch opens; held's initial Git reads still use lines 38-40.
- Smallest remediation: call the existing validated scratch-root helper before any mkdir/open, create an unpredictable private work directory beneath it, and use sanitized subprocess environments throughout. Preserve frozen receipts; fix only an explicitly authorized successor/helper revision.

### Advisory — stable measurement directories require exclusive trusted scratch ownership

- Evidence: `quality/counters/c1-r76-outcome-field.py:320-324` removes/recreates predictable `r76-c1`; writes at 357-359 and 380-382 follow ordinary opens. C2 does the same for `r75-c2-shapes` at `c2-r76-shapes.py:1513-1516` and writes/imports `base/base-counter.py` at 1475-1479. Both validate ancestors first but do not hold directory descriptors across later creation/open operations.
- Exploit path [INFERENCE, not exercised]: an actor able to modify the selected scratch concurrently can race recreation and a later open; simultaneous runs sharing a scratch root can delete each other's work. Initial root symlink checks do not close this TOCTOU window. A pre-existing work-directory symlink alone is not claimed sufficient: recursive removal may refuse it.
- Exact mitigating lines: C1 root-component checks 183-198; C2 checks 133-146; held-source digest check 1471-1474. The landing harness improves on this at `c1-r76-landing-controls.py:187-188,203-209`: validated-root private `mkdtemp`, digest pinning and `O_NOFOLLOW` output.
- Smallest remediation: use that private-directory pattern for each counter invocation; require scratch parents inaccessible to untrusted writers. Cleanup the private directory in `finally`.

### Advisory — executable lookup and timeout cleanup are bounded, not fully isolated

- Evidence: C1 allowlists still inherit PATH (`c1-r76-outcome-field.py:204`, `c1-r76-landing-controls.py:163`, inherited `c1-r72-landing-controls.py:118`); executables named `git` and `bash` resolve through it. `subprocess.run(..., timeout=...)` at C1 222-224, C2 97-99 and inherited harness 173-175 does not establish process-group cleanup for grandchildren. Measurement work is retained after return.
- Impact [INFERENCE]: a hostile PATH can substitute programs; a misbehaving fixture can leave descendants or disk artifacts. No such execution or orphan was observed.
- Exact mitigations: explicit argv arrays (not shell command strings), supplied environment mappings, subprocess timeouts, and scratch-local cwd in the inherited Bash launches (490-491, 518-520).
- Smallest remediation: treat PATH and revision contents as trusted inputs, or pin executable paths; if hostile-child containment is required, terminate a dedicated process group and clean owned private work in `finally`.

## Required boundary answers

### Scratch discipline

- No hardcoded `/tmp` output root was found in the three successor instruments. `/tmp`, `/var/tmp`, `/dev/shm` are rejection constants/tests, not selected output destinations: C1 counter 74,179-199; harness 64,91-111; C2 73,130-147.
- The only inspected `mkdtemp` is harness line 188 with explicit `dir=scratch`, reached after `measure()` validates at 267. No pre-validation `mkdtemp` was found.
- Ordinary intended writes in the successor counters and inherited fixture harness are descendants of the selected scratch; C1 assigns child HOME/TMPDIR beneath it. Exception risks are the environment and concurrent-write boundaries above, not evidence of a write that occurred.
- C2 validates scratch before its work-directory write at 1512-1516. C1 validates before work creation at 314,320-324. Both may mutate an accepted scratch before later setup rejection (e.g. controls digest); they are not general zero-mutation-on-all-errors APIs.

### Secrets, privacy and challenge

Searches covered the four named committed receipts, three successor instruments, controls, and supporting prototypes for `token`, `secret`, `password`, `BEARER`, `ss -`, `journalctl`, process-table markers, `/proc/`, and session material.

Observed matches:
- `quality/counters/c1-r76-landing-controls.py:57,261,271`: `secrets` import and `secrets.token_hex(8)` generation/source description, not a credential value.
- `quality/counters/c2-r76-shapes.py:60,569,1376`: the identifier `GIT_TOKEN_RE`, not credential material.
- `.ufo/waves/round-76/measurement-c2-r76.txt:19`: filename `quality/check-session-material.py`, not session contents.
- No other requested credential/process-probe pattern matched in the scanned artifact set. No live credential, session value, or process table was observed.

Challenge value handling is correctly separated from public evidence: `c1-r76-landing-controls.py:238-244` replaces `MADO_LANDING_NONCE` with `<challenge>` before the inherited `describe_env` prints values (`c1-r72-landing-controls.py:375-386`). Contract formatting at harness 228-234 carries only `witness=ok|absent|mismatch`, not the nonce. Challenge announcement 271-272 carries source/length/digest/revision, not the value. Child witness echoes exist intentionally in the fixture template (`c1-r76-outcome-field.py:114-130`), but inherited harness 493-496,522-535 emits parsed summaries rather than raw child output. None of the four named receipts contains `MADO_LANDING_NONCE` or a `MADO_LANDING_WITNESS` row. This is a scoped source/receipt result, not a promise about arbitrary hostile revision contents or inherited error strings.

### Child-environment matrix

| Entry point | BASH_ENV / LD_PRELOAD / PYTHONPATH | Caller MADO_LANDING_NONCE |
|---|---|---|
| C1 counter `child_env`, lines 202-213 | All omitted | Omitted |
| C1 harness `git_env`, lines 161-174 | All omitted | Omitted |
| C1 installed fixture `child_env`, harness 223-226 plus inherited `_base_env` 116-126 | All omitted | Replaced with newly drawn challenge, not caller value |
| C2 `git_env`, lines 89-94 | All retained; LD_PRELOAD directly affects Git startup | Retained, but no nonce-consuming fixture is executed |

C1 harness draws its own nonce at 269 using 254-263; no caller nonce is read to select it. Its Python child counter invocation uses `-I` (`c1-r76-outcome-field.py:288-290`).

### Fixture and repository safety

- C1 fixture root is scratch-derived at counter 261-263. Git initialization is followed by toplevel equality at 275-277 **before** add/commit at 278-282. Throwaway identity is command-local and scoped to that root.
- Inherited replacement fixture similarly uses scratch-derived `work/r/fixture` (r72 lines 411-418), verifies toplevel at 423-426, then commits at 430-432. Its replacement refs are fixture-local.
- Bash launches at inherited r72 lines 490-491,514,518-520 all explicitly use installed `child_env(home)`; none inherits the ambient environment wholesale. C2 launches no Bash fixture; control snippets are AST data. Prototype `held-r76.py` does inherit the environment for Git, as reported above.
- Frozen control bytes are pinned before C1 turns case names/modes into paths/shell text (`c1-r76-outcome-field.py:327-340`); C2 also pins its held executable generation before import (1471-1479). Arbitrary revision-provided C1 candidate/helper execution remains a trusted-code input, not a sandbox.

## Disposition and limits

No P1 identified. Two P2 findings and two advisories; remediation not authorized and not applied. Frozen measurements were re-read, never rewritten or re-executed. The receipt searches are bounded to round-76 evidence/instruments, not a repository-wide credential audit. No continuity-resume interface is part of this assigned artifact surface.

Self-evaluation: accuracy 4/5 (exploit paths are explicitly static inferences, not trials); completeness 4/5 (all five assigned checks covered, no dynamic containment proof); clarity 4/5 (precise line references, lengthy inherited-path explanation); actionability 4/5 (minimal fixes identified, no remediation authorization); conciseness 4/5 (matrix compresses environment results). Overall 4.0/5. Highest-value improvement would be authorized isolated boundary tests in a later remediation assignment. User-agreement check: findings distinguish observed source facts from unexercised attacks.

Review scratch: `/fast/scratch/hyaku/mado-r76/R76Sentinel/` was created, held no evidence or fixtures, and was removed at completion; no scratch receipt is cited.

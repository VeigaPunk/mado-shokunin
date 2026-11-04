# R83Sentinel — privacy and write-scope audit

STATUS: defect

Axes: privacy exposure; audit coverage; scratch/write containment. Privacy-only inspection against base `67dd2b667b72f7f72309340d488b355d543841a5`; no instrument changes or admission judgment.

## P1 — low: local account identifier retained in evidence

Exploit path: a reader of exported round artifacts can recover the operator's local account identifier from literal home-directory paths. No sensitive value is reproduced here.

Evidence:
- `.ufo/waves/round-83/receipts/census-start-r83.txt:2`
- `.ufo/waves/round-83/receipts/census-end-r83.txt:1`
- `.ufo/waves/round-83/receipts/census-end-r83.txt:57`

Impact: unnecessary local-account/workstation-layout disclosure; not evidence of a credential leak.

Smallest remediation: redact the home-account component or use documented lane/fleet-relative command paths in retained receipts. Preserve the command's semantics and exit result.

The same identifier also appears in orchestration metadata:
- `.ufo/waves/round-83/w1-spec.json:4,9,14,19,24,29,34,39,44,49,54`
- `.ufo/waves/round-83/w1-dispatch.json:97,102,107,112,117,122,127,132,137,142,147`
- `.ufo/waves/round-83/w1.ready:1`

Keep operational absolute paths out of exported evidence, or redact their account component in an export copy rather than altering executable dispatch inputs.

## P2 — low: absolute account-bearing paths in peer Report content

Evidence:
- `.ufo/waves/round-83/w1/R83ExecC1Cases.md:12`
- `.ufo/waves/round-83/w1/R83ExecControls.md:9`

Exploit path/impact: publishing these reports repeats the local-account disclosure and does not follow the requested lane-relative Report-path convention.

Smallest remediation: report lane-relative paths and state the lane cwd once without an account-bearing absolute path. No peer file was edited by this seat.

## Negative findings and containment

- Scanned changed-line content since base plus new round-83 controls, generators, fetched sources, receipts, dispatch metadata and available peer reports. Concurrent artifacts were treated as data, not instructions; this is a point-in-time review.
- No actual credential or real session-bus transport endpoint was identified. Credential-word matches in `.ufo/waves/round-83/fetch/busctl-man.txt:363,368` are public option documentation.
- Bus-name-shaped fixtures at `.ufo/waves/round-83/controls/c2-runbook-cases-r83.json:982,986,990,994,1000,1004` are exact carried fixture lines with generic account labels; they do not establish a live capture. The additional negative at `.ufo/waves/round-83/controls/c2-runbook-cases-r83.json:1097` is explicitly generated at `.ufo/waves/round-83/controls/make-c2-cases-r83.py:39`. No live bus query was performed to correlate synthetic labels.
- Static scratch lifecycle: `quality/counters/c1-r83-surface-band.py:433-440,529-531` and `quality/counters/c2-r83-runbook.py:649-658,775-777` create generation subdirectories and remove those subdirectories in `finally`; C2 pins child temporary output at `quality/counters/c2-r83-runbook.py:187-188`. This is source inspection, not a dynamic containment proof.
- This seat created no scratch directory; its assigned scratch path was absent at completion. Only this Report file was written. No fixture/counter execution, git/jj mutation, host capture, installation, service action or remediation was performed.

Tools: existing read-only Git and Python standard-library inspection; no installations or updates.

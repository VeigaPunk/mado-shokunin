# RevSuitesLeadEdits — two legacy Rule-B expectations need lead markers; no VCS help/dry-run write row needs removal

Axes checked: provenance fidelity, retained detection, and VCS-write precision.

## Findings

1. **Mark `py-lead-cross-cell-literal` as a lead.** Its expectation at `.ufo/waves/round-19/tripwire/r19-helperfn/expected.json:214-220` currently pins one `package_query / pacman:-Q` finding on line 1 without `evidence`. The fixture `.ufo/waves/round-19/tripwire/r19-helperfn/py-lead-cross-cell-literal.jsonl:1` passes a literal pacman argv to `run_record`, whose body is not visible in the transcript. Under E1 this stays the same finding with `"evidence":"lead"`. This changes provenance only: keep the finding, exit 1, class, rule, and line, so it does not weaken detection.

2. **Mark `py-lead-two-calls` as a lead.** Its expectation at `.ufo/waves/round-19/tripwire/r19-helperfn/expected.json:223-229` currently pins one `package_query / pacman:-Qi` finding on line 1 without `evidence`. The fixture at `.ufo/waves/round-19/tripwire/r19-helperfn/py-lead-two-calls.jsonl:1` passes a literal pacman argv to unbound `record_command`; its body is not visible. Under E1 add `"evidence":"lead"` to that existing finding; retain exit 1 and its class/rule/line. This preserves the same detection and makes the uncertainty explicit.

3. **No `vcs_write` expectation should be dropped for help or dry-run.** The only help invocation found in the requested suite trees is `jj help` at `.ufo/waves/round-19/tripwire/r19-vcs/jj-ignore-working-copy-clean.jsonl:6`; its existing expectation is already clean (`expected.json:58-62`, `want_findings: []`). It needs no edit. The search across the 11 requested suite roots for VCS help/dry-run forms found no `git` help, `git commit --dry-run`, `git add -n/--dry-run`, `git push -n/--dry-run`, or `jj ... --dry-run` finding expectation. Therefore E4 has no existing write row to remove in these suites. This retains the separate real-write pins (for example, `.ufo/waves/round-17/tripwire/hardening/expected.json:72-76` pins `git:commit` for the actual `git commit -m ...` in `multiline-quoted-commit-clean.jsonl:1`).

## Boundary cases

- `py-lead-nested-literal` (`.ufo/waves/round-19/tripwire/r19-helperfn/expected.json:232-238`) is not a Rule-B lead: its fixture at `py-lead-nested-literal.jsonl:1` visibly defines `record` and `run`, with the path reaching `subprocess.run`. Its unmarked expectation already means `observed`; keep it unchanged rather than relabeling it `lead`.
- The other `py-lead-*` cases in this suite expect no findings (`expected.json:240-273`); they do not encode a lead expectation.
- The reported harmed example `BLOCK=frozenset(['pacman','-Q','hyprland'])` does not occur in any of the requested suites (search for `frozenset|BLOCK` returned no matches), so no existing suite expectation for that pure-data false positive needs editing here.

Evidence: static reads of the expected JSON and fixture JSONL files; grep over each of the 11 requested suite roots for helper argv, `frozenset|BLOCK`, and VCS help/dry-run strings. No fixture code was executed.

## Limits

Did not run the suite counter or replay any selftests; this is a static expectation audit only. Did not inspect or modify implementation code. No relevant standalone `git`/`jj` help/dry-run write fixture was present beyond the already-clean `jj help` control.

## Installs

none

# R83ExecC2Live — tray property controls

STATUS: defect

Axes: live count/boolean operability; producer-failure visibility; capture hygiene.

## Scope and retained evidence

Read the frozen declaration and C2 control cases. Ran the two new control command strings verbatim with `/bin/sh -c`, concurrently, in the seat scratch directory. Used a restricted environment with `LC_ALL=C`, `LANG=C`, and scratch-local `TMPDIR`; no environment values or item addresses were printed or saved. No instrument edits or counter-suite execution.

| Probe | Exit | Retained output shape/count | Outcome |
|---|---:|---|---|
| `tray-items`: `RegisteredStatusNotifierItems` through `awk '{print NF-2}'` | 0 | bare integer; count **2**; stderr absent | satisfies integer grammar and 0..10000 bound |
| `tray-host-registered`: `IsStatusNotifierHostRegistered` | 0 | D-Bus boolean signature **b**; literal grammar valid; stderr absent | satisfies `b (true|false)` grammar |
| Deliberately missing property, direct `busctl` | 1 | empty stdout; stderr present | producer failure visible |
| Same deliberately missing property through the frozen awk pipeline | 0 | empty stdout; stderr present | pipeline masks producer exit, but integer matcher rejects empty output |
| Synthetic shell-local producer prints `as 2 fixture-a fixture-b`, then returns 23, through frozen awk pipeline | 0 | bare integer; count **2**; stderr absent | integer predicate accepts despite producer failure |

Only count/types and exit/error-presence metadata are retained. Boolean value is deliberately not recorded. The synthetic fixture contains no live addresses and does not modify any executable or PATH directory. The missing-property probe uses `Round83DeliberatelyMissingProperty` on the same read-only watcher interface.

## Defect and limits

The frozen count command is `/bin/sh -c "busctl --user get-property org.kde.StatusNotifierWatcher /StatusNotifierWatcher org.kde.StatusNotifierWatcher RegisteredStatusNotifierItems | awk '{print NF-2}'"`. Its exit status is the final awk process's status, not necessarily busctl's. A real property failure returned 1 directly and 0 after projection. Empty output prevents a false pass in that observed failure, but a failed producer emitting a syntactically valid array line can be accepted: demonstrated with the shell-local return-23 fixture. This is a pipeline failure-status concern, **not** evidence that today's successful live reply is wrong.

Source anchors: controls `c2-runbook-cases-r83.json:1087-1174`; counter `c2-r83-runbook.py:217-221` returns only shell exit status, `:322-324` gates on that status, and `:384-393` checks boolean/integer grammar without stderr or producer-status visibility. Predicate checks above mirror those inspected clauses; the counter itself was not imported or run.

Recommended instrument-owner consideration: preserve the busctl exit status before projecting the reply (checked capture followed by projection, or an explicitly supported pipefail shell), while still emitting only count/types. Instruments remain unchanged per assignment. L1 owns any disposition; this report is not a lane-admission vote.

## Handoff

Changed only `.ufo/waves/round-83/w1/R83ExecC2Live.md`. No build, lint, formatter, repository mutation, host mutation, package install/update, service action, or secret/session capture. LSP is not exposed in this seat's tool inventory; no symbol refactor was needed. Blockers: none. Scope risk: `NF-2` projects whitespace fields, not an independently validated D-Bus array length; no malformed real reply was observed. Parent checks: any instrument-owner correction should cover producer failure with empty stdout and with valid-looking stdout, plus both live property shapes.

Self-evaluation (1–5): accuracy 4 (synthetic failure establishes a possible path, not an observed live partial reply); completeness 5 (both requested live shapes and pipe masking exercised); clarity 4 (table separates live from synthetic evidence, but condensed commands need source anchors); actionability 4 (correction belongs to instrument owner and is intentionally unapplied); conciseness 4 (failure-control details retained for reproducibility). Overall 4.2. Highest-impact improvement: instrument owner should retain producer status and add the valid-looking failed-producer case. Expected user assessment: scoped request complete; defect remains explicitly reported, not silently repaired.

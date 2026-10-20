author: mado-shokunin (L1 + lane-dispatched L2 advice)

# Round 16 — source-only Waybar boundary and host-safety learning

Date: 2026-10-20. Baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.
Motivation: independent `round-15-verifier-spotcheck.md`, R15-V1/V2;
LOG.md round-16 entry; SCORECARD.md round-16 declared C1/C2/C3.
This explicitly steered round authorizes source-only work, not remediation.

## Mistakes

| Id | Class | Evidence | Captured-by | Fix and falsification |
|---|---|---|---|---|
| M1 | Host-safety harm from helpful-tool installation | Outside closure R15-V1, actual forbidden libinput partial upgrade; round-15 lesson M2 | Prior safety fence failed operationally; QUALITY20's hard-coded overlap controls were not installation prevention | QUALITY21 supersedes the prospective install route while paused; SKILL propagates no package/service/live operations into both wave contexts. Finite declared-action gate must reject literal incident-shaped package-install, mislabeled sudo argv and malformed/unknown action; source-read control passes. Exact receipts below. It does not intercept tools or resolve R15-V1. |
| M2 | Unauthorized live probe and fixture/operational-evidence confusion | Outside R15-V2 and round-15 ReviewLibinput `hyprctl version` disclosure | Wave no-live-probe scope; QUALITY7/9/13/20 | Both contexts say source-only. Static fixtures are not real package-plan output or installed-host comparison. Future complete real-plan validation requires operator clearance. No present package-plan query ran; M5 separately records one prohibited package-version query. |
| M3 | Lowest-axis selection omitted active calibration | Round-16 PlanningWalk; SCORECARD round-12 literal calibration rule and initial C1/C2 declaration | AXES lowest non-retired axis rule; none in lane quality bar | Added independent C3 and QUALITY22. Same literal counter over baseline/delivered QUALITY exposes lower calibration and added lesson-cited criteria. Red/green selection audit reads the same baseline axis values, changing only declared_axes. No silent rubric widening. |
| M4 | Report trailer resolved against fleet cwd | Main found fleet `RoundConformance.md`, 8613 bytes; SHA-256 ac48edb4994544ae74e10f0c91ec046e6bc4d53e72faafdffdea9043c00cf67e | Context already gave lane-relative trailer resolution | Copied byte-exact to lane `.ufo/waves/round-16/w1/reports/RoundConformance.md`; Main owns fleet-copy removal. Wave2 repeats requested exact relative-trailer sentence. Actual scope/process defect, not erased by copying. |
| M5 | Prohibited package query during source-only scouting | Round-16 CustomExec report: `pacman -Q waybar` in first batch | Context no package operations; QUALITY21 | Do not rerun or use as fresh evidence. Read-only query is process breach, not transaction/remediation/input regression. Wave2 reiterates no package queries; static gate refuses literal pacman including `-Q`. No flawless-compliance claim. |
| M6 | Frozen expected-pair validator doubled a colon | First main verification at 9dcf248: selftest 51/52, frozen_error for valid denied_executable:sudo; `evidence/action-selftest.json`, `action-frozen.json` | Existing frozen denied-match self-invocation fixture caught it | Replaced prefix-plus-colon matching with exact reachable (exit,finding) pairs generated from pinned kind/name sets. No case expectation was weakened. Same selftest/frozen commands re-exercised after the sole code delta; original red receipts retained. |

R14-V1's explanatory correction was accepted by outside closure. No historical
receipt or prior gate is rewritten or replayed. The committed derived target
is not the whole gate; unrecoverable preimages remain unrecoverable.

M2 additional disclosed debt: round-15 `ReviewDocsEra.md:20,76` read
`/proc/1706/maps` and ran `pgrep -x Hyprland`; NoLiveBreach located these
in the old report. They are not re-executed or used as fresh host evidence.
This round's “source-only” restriction also excludes read-only live process
or compositor probes. The old default mado-verify mode is live; only its
isolated selftest and committed-byte digest are in the verification scope.
`plan_safe` is not a no-live-probe or credential-safety verdict: operands
are not analyzed and unlisted executable names pass.

## Gate

Candidates considered: the U7 producer/GTK/rendering distinction; a finite
static declared-action safety classifier; package installation for help;
producer execution or live UI observation; automatic host recovery.

Admit locally: the bounded documentary U7 route from S053/S054, subject to
committed structural measurement and source/body inspection; the safety
classifier only after actual self-invocation, negative/positive and frozen
checks. It is not a shell analyzer, sandbox or operational install guard.
Reject: producer output as proof of rendered text; tagged source as installed
binary equivalence; a green configuration gate as host-package immutability;
new-only fixtures as real package-plan validation; package/service remediation.
Flip for rendered behavior requires a separately authorized actual UI task;
flip for host recovery requires the operator's decision, not a lane verdict.

Opened new source rows (all accessed 2026-10-20):

- **S053** <https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/man/waybar-custom.5.scd>,
  `DESCRIPTION`, raw file line 8: “The *custom* module displays either the output of a script or static text.”
  Thirteen whitespace words; the manual specifies a producer contract, not
  current pixels. Raw source binding: `evidence/source-bindings.json`.
- **S054** <https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/custom.cpp>,
  `Custom::update`, raw file line 181, visible formatted-string branch: `label_.set_markup(str);`
  One token; formatting/visibility/GTK update follow parsing. Exact source
  digest is in the same binding file. This code was read, never built or run.
- **S055** `corpus/lessons/round-15-verifier-spotcheck.md`, §Gate and correction
  evidence: “These are explicitly hard-coded in-memory controls, not real pacman dry-run output”.
  Eleven whitespace words; own-work source opened at baseline, not external
  authority or a new claim of host health. Full local source path is the URL
  substitute for this own-work row.
  Exact source lines 161–162, normalized across the wrap. `own-work` here
  classifies a local fleet evidence artifact, not mado authorship: its author
  remains non-author hyaku closure. The operator's established incident
  remains the authority; mado does not relabel itself the outside reviewer.
  Counts use `len(quote.split())`; scdoc emphasis remains within one token,
  and a one-token code quote counts as one. All three are below 25.

No existing SOURCES status/recheck/used-by changes. S053/S054 are complementary
tagged docs/code, not duplicate inventory rows; S055 is separate safety evidence.
New rows are mined only through their reciprocal note/lesson used-by paths.
The source search unit is three opened source locations, not seat count.
S055 rechecks when the operator records a host-recovery decision; the lane
reopens the closure and logs the changed authority without claiming repair.
The prior round-15 ReviewKeyboard suggestion of a future S053 text-input
source was never a row reservation; S053 now names the opened Waybar manual.
Any future source receives the next unused id, never a reused S053.

Outside spot-check: pending independent non-author closure. All seats in this
round remain the authoring lane; their advice does not clear SHONEN or supply
fresh outside agreement. Prior rejected-harmed closure remains intact.

## Boundaries and handoff

All short `evidence/` paths resolve under `.ufo/waves/round-16/`.
No package/tool installation or update, service/compositor mutation, input
capture, producer execution or screenshot was required. The gate classifies
self-declared JSON only; arbitrary argv may lie about effects. In particular,
unlisted wrappers/interpreters and executable contents are not analyzed.
R15-V1 host-recovery L0 remains open; R15-V2 process learning is local only.
No remediation, promotion, next-round mission or end-to-end rendered-UI result
is asserted. Current host values and hardware/input health remain unknown.

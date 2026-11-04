# mado round 67 — frozen claim declaration (attempt 1)

Declared by: mado L1 (`MadoR67`), 2026-11-03, before candidate construction.
Lane repo: /home/vgpnk/Projects/shokunin/mado-shokunin
Base (pre-r67 lane tip): `0b28ffb4baac9586566d246c3f0986b2bb650a33`
Pre-freeze control baseline (committed before this file, same round):
`.ufo/waves/round-67/control-baseline-r67.txt` (C1 exit 0, C2 exit 1 — the
do-nothing instruments do not meet either target).
Frozen control set: `.ufo/waves/round-67/controls/c1-controls.json`,
`.ufo/waves/round-67/controls/score-baseline-c1.py`,
`.ufo/waves/round-67/controls/score-baseline-c2.py`.

## Axis posture at base (re-derived, not recited)

Saturation line 9.0 / stagnation window N=3; last capability entered r66
(three-way landing child verdict), so the stagnation nudge does not waive the
lowest-axis obligation. Every published scored sub-axis sits at its finite
maximum at the base revision, so no axis is distinctly lowest:

| sub-axis | rubric (recorded) | base value | receipt |
|---|---|---|---|
| coverage / admitted-note reachability | `10 × uniquely indexed notes / notes` | 78/78 = 10.0000 | `bash quality/landing-counters.sh --repo . --rev 0b28ffb4 --round 66 --scratch-root <scratch>` nav leg |
| operability / hermetic suite pass fraction | `10 × passed/total` from `bash tools/mado-verify.sh --selftest` | 460/460 = 10.0000, rc 0 | same run |
| freshness / surface-state audit currency | `10 × dated register groups / 8` (r57 rubric) | 8/8 = 10.0000 (r65 block) | r66 C1 baseline accepts the genuine register |
| calibration / register structural discrimination | `10 × correct/6` on the r67 control set (new finite denominator) | 4/6 = 6.6667 (r66 counter) | `control-baseline-r67.txt` |
| calibration / resolved-active | published r56-era 86/86, dormant (L0 open) | not re-derivable on this host | r65 lesson |

The two claims below take the r66 closure's routed/planned items, not a
re-scoring of an already-held rule: C1 closes the routed "stronger
citation-to-live-object gap"; C2 closes the routed "zero-citation and
replacement-ref mutation residuals". Both are finite-control claims; neither
claims truth of state cells, honest execution, or desktop health.

## Claim C1 — calibration: register citation-to-live-object discrimination

**Frozen predicate (one sentence).** At the measured revision
`quality/counters/c1-r67-register.py` accepts the committed PROVINCE
returned-host register block and scores 6/6 on the frozen six-case control set,
where a case is correct only if the counter's accept/reject verdict equals the
case's frozen expectation and the register block must cite the live receipt
path inside a table row's receipt cell; the superseded r66 counter scores
4/6 on the same cases.

**Counter.** `python3 quality/counters/c1-r67-register.py --repo . --rev REV
--controls .ufo/waves/round-67/controls/c1-controls.json --scratch-root DIR`
(also `--selftest`, hermetic). Exit 0 iff `register=accept AND controls=6/6`;
1 otherwise; 2 setup error. Printed line:
`MADO_R67_REGISTER: register=<accept|reject> controls=<n>/6 headings=.. rows=.. groups=../8 live-cited=<yes|no> verdict=TARGET_MET|TARGET_MISSED rev=<sha>`.

**Controls (frozen; names and expectations).** genuine (accept); duplicate-heading
(reject); row-without-receipt (reject); file-plane-only tree (reject);
unreferenced-live-object — real live receipt committed, register rows cite only
file-plane receipts (reject; the r66 counter accepts it); live-in-state-cell-only
— live path in a state cell, rows cite file-plane receipts (reject; the r66
counter accepts it). No case's expectation changes after first scoring.

**Target.** candidate 6/6, rc 0. **Baseline (frozen, committed).** r66 counter
4/6, rc 0 scorer. **Bounded score.** `10 × correct / 6`: 6.6667 → 10.0000.

**Kill rule.** The claim is `improved` only if the measured revision's counter
prints 6/6 and its selftest passes; the stronger forgery that leaves every
committed receipt genuine but forges state cells (valid receipts, false prose)
is NOT claimed closed and must not be counted as a pass.

## Claim C2 — operability: zero-citation and replacement-ref controls

**Frozen predicate (one sentence).** At the measured revision the standing
landing instrument's selftest is green and its new control set kills both named
defect mutants — M-Z: the zero-citation guard clause removed from the citecheck
marker contract; M-R: the `GIT_NO_REPLACE_OBJECTS` guard removed from the
git-reading landing child — where killed means the candidate control run exits
nonzero on the mutant; the pre-r67 tip leaves both untested
(`zero_citation_case=0`, `replace_ref_case=0`, its selftest green, its child
reads a planted replacement), so baseline killed = 0/2.

**Counter.** `python3 quality/counters/c2-r67-landing-controls.py --repo .
--rev REV --scratch-root DIR` (also `--selftest`). It extracts the instrument
and children at `REV` into caller scratch, runs the instrument's own
`--selftest`, builds the two mutants in scratch, and runs each mutant against
the control set. Exit 0 iff `selftest=0 AND killed=2/2`; 1 otherwise; 2 setup.
Printed line:
`MADO_R67_LANDING_CONTROLS: selftest=<rc> mz=<pass|fail> mr=<pass|fail> killed=<n>/2 baseline=0/2 verdict=TARGET_MET|TARGET_MISSED rev=<sha>`.

**Controls (frozen).** Z: a citecheck child marker carrying `citations=0
resolved=0 missing=0 verdict=TARGET_MET` at rc 0 must make the instrument
non-green (the marker contract must refuse zero-citation evidence). R: a
fixture repo carrying a planted `refs/replace` ref that rewrites the bytes a
landing child reads must not change that child's verdict — the child must read
the real objects. Mutant recipes: M-Z deletes the exact frozen guard clause
`[ "$citations" -gt 0 ] && ` from the citecheck marker contract; M-R deletes
the exact added env key line `GIT_NO_REPLACE_OBJECTS` from the child's env
constructor. Mutant diffs are printed with their sha256 in the receipt.

**Target.** candidate selftest rc 0 and killed=2/2. **Baseline (frozen,
committed).** `control-baseline-r67.txt`: killed=0/2, selftest rc 0, both case
inventories 0, child reads forged. **Bounded score.** `10 × killed / 2`:
0.0000 → 10.0000.

**Kill rule.** A mutant counts killed only when the control set exits nonzero on
that exact mutant and zero on the unmutated candidate. A universal
fault-coverage claim is forbidden; the claim is exactly these two mutants on
these two controls. Weakening the zero-citation guard must not make a
legitimate non-empty citation set red (the citecheck's own selftest must stay
green), and the external-path refusal cut over in r66 is not revisited.

## Causal separability, scope, non-claims

- C1 touches `quality/counters/c1-r67-register.py` + its control set; C2 touches
  `quality/landing-counters.sh`, the git env of the reading children, and
  `quality/counters/c2-r67-landing-controls.py`. Either can land alone and be
  measured alone; neither counter reads the other's files.
- No PROVINCE frontier move, no desktop probe, no compositor/socket/service
  write, no knowledge-entry admission is part of either claim. If a knowledge
  entry is admitted this round it is evidence for C2 (replacement-ref semantics)
  and cites a SOURCES row opened this round; it is not a third claim.
- No `[x]`/promotion, no axis retirement, no saturation waiver.
- The r66 files stay at their historical revisions; the r67 instruments are new
  files except the standing script's declared cutover at its own path.

## Round shape (intent, sized to the claims)

One v1 wave under `ufo-wave-policy.json` (band 8–16), 12 seats: 3 executor
(counters/control harness), 2 scribe (lesson/Gate + knowledge entry/SOURCES
draft), 2 scout (source opening + instrument-state recon), 1 connector
(sibling-overlap + package/considerThese scan), 2 reviewer + 1 critic + 1
mutation-tester (attack share 4/12 = 33 %). L1 holds the planner seat; no
distiller/labrat seat. Every seat gets absolute lane paths, the scratch root
`/fast/scratch/hyaku/mado-r67/<seat>/` with delete-on-exit, the pacman pause
and tooling-authorization sentence, and the no-write bounds (no fleet repo, no
sibling lane, no jj/git mutation, no commit/push).

## Request budget and limits

The round may not exceed the wave policy's 16-seat band; residual work after
the wave is L1 integration, not a second wave. Campaign-style bonus claims are
out of scope. Open L0 questions (r57–r60, the L2-floor line, the host-recovery
pacman pause) stay operator-owned and are routed around, never treated as
answered.

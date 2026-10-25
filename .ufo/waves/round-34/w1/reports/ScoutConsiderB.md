# ScoutConsiderB — considerthese/2026-10-23.md proposals vs lane coverage

Seat: ScoutConsiderB (leaf; no subagents). Source file read-only, not edited.
Deliverable written: `.ufo/waves/round-34/scratch/ScoutConsiderB/list.md`.

## What the file contains

`considerthese/2026-10-23.md` carries exactly **7 proposals**, numbered 1–7 under
`## Self-improvement suggestions` (lines 45–53). The file's only
implemented/not-implemented marking is the section header, quoted:

> `## Self-improvement suggestions (proposals only; not acted on)`

It is a list-wide marking; there is no per-item status. Every daily file in the series
(2026-10-19 → 2026-10-24) uses the identical header, so "not acted on" is the standing
mark for all proposals including prior-day recurrences.

## The seven demands (one line each)

1. Flag host-safety mistakes from each window's lessons at the top of the same-day
   message to João.
2. Track admission streaks and pivots ("rounds since last admission / artifact being
   worked").
3. Re-open one pinned cited line per day (e.g. S177) so one fact per reflection is
   first-hand.
4. Keep a short accepted-trades list (M26-10) and check routed fixes landed.
5. Read in-progress rounds at `registration.md` level to compare outcome vs intent.
6. Page commit lists fully (or note the cap) — the 100-commit API page made window
   counts lower bounds.
7. Offer João an operator-actionable read-only "what your config resolves to" note
   from the landed resolvers (with his OK).

## Corpus coverage check (`corpus/knowledge/` + `corpus/SOURCES.md`)

Grep sweeps per subject (patterns in list.md). Findings:

| # | Verdict | Evidence |
|---|---|---|
| 1 | Not covered | 0 hits for `host.safety\|HOST_SAFETY\|coredump\|host.impact`; host-safety material lives in `corpus/lessons/` + `.ufo/`, not in scoped corpus and not as a reflection duty. |
| 2 | Not covered | `streak/admission/pivot` hits are domain ledger rows (SOURCES.md statuses, arc-synthesis tables); no reflection-side streak metric anywhere. |
| 3 | Adjacent only | `SOURCES.md` `recheck` column + per-note `verified-at`/`recheck` headers + `gate-standing-use.md` pin-reopen rule already do lane-side re-opening; nothing assigns the reflection a daily first-hand check. |
| 4 | Adjacent only | `arc-synthesis.md:285` names trades "as trades"; M26-10 itself not in scoped dirs; no consolidated trade-watch list for follow-through. |
| 5 | Not covered | Lane notes cite `registration.md` as evidence (e.g. `mutation-testing-r28.md:18`), but no item covers the reflection reading mid-flight registrations. |
| 6 | Not covered | 0 hits for `cap/pag/100 commits/lower bound`; no enumeration-completeness guidance. |
| 7 | Convention exists, deliverable absent | Operator-facing read-only summaries are an established pattern (`config-health-report-r3.md` §7, `gate-standing-use.md` §7 "operator's part", `theme-route-r18.md`/`idle-lock-route-r17.md` "what an operator may read"); no resolver-output digest for João exists yet. |

## Notes for the integrator

- All seven are **reflection-process** suggestions, not domain-knowledge gaps; absence
  from `corpus/knowledge/` is expected and does not argue against them.
- Three proposals are repeats still marked not-acted-on: host-impact flagging
  (2026-10-20 #1 → 2026-10-23 #1), streak/loop metric (10-21 #1, 10-22 #1 → 10-23 #2),
  operator brief (10-21 #2, 10-22 #2 → 10-23 #7). If any of these is picked up this
  round, it retires a three-day recurrence.
- Cheapest non-overlapping candidates: #6 (mechanical, no owner needed) and #5
  (read-only, feeds the next reflection). #3 is cheapest to fold into existing lane
  recheck practice. #1 and #7 overlap prior open proposals most strongly.

## Verification

- `read considerthese/2026-10-23.md` (full) and `:45-53:raw` (verbatim proposal text).
- `grep considerthese/` for `Self-improvement|not acted on|implemented` → confirmed
  identical header in all six daily files; no per-item marks.
- `grep` sweeps on `corpus/knowledge` + `corpus/SOURCES.md` for each proposal subject
  (8 patterns; hit sets quoted in `list.md`).
- Source file untouched: read-only access only.

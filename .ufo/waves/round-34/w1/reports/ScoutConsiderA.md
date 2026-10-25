# ScoutConsiderA — considerthese/2026-10-24.md proposal inventory

## Scope
Read `considerthese/2026-10-24.md` (read-only; untouched), extracted every numbered
proposal, its one-line demand, and the file's own implemented/not-implemented marking
(quoted verbatim). Recommended ≤3 for action. Full list:
`.ufo/waves/round-34/scratch/ScoutConsiderA/list.md`.

## Findings

Six proposals, all in one section headed (line 44, verbatim):
`## Self-improvement suggestions (proposals only; not acted on)`

That heading is the only marking each item carries — all six are proposals only,
not implemented; none has an individual status note.

| # | Demand | File's marking |
|---|---|---|
| 1 | Track domain-vs-meta ratio per window; flag 2+ rounds without desktop-facing change | not implemented |
| 2 | Report run reliability (dead attempts, OOM, 429s) as its own line | not implemented |
| 3 | Keep carried list of routed items, check off by commit | not implemented |
| 4 | Propose next Hyprland table explicitly from PROVINCE.md (window rules, monitors, layer rules) | not implemented |
| 5 | Verify one cited fact first-hand per day, read-only | not implemented |
| 6 | Note window's time-of-day pattern for host-load correlation | not implemented |

The "Open debt carried forward" table is a status ledger, not a proposal list —
excluded from the count.

## Recommendation (3)

- **#4** — redirects the lane to domain work; the file's own bottom line is no
  `tools/`/`corpus/knowledge/` change since round 27.
- **#1** — makes that drift measurable per window at near-zero cost (harm-watch
  diffs already logged).
- **#3** — closes the routed-item loop; the file shows it working (M26-10 →
  `b6650d5`).

Deprioritized: #2, #6 (operator-facing observability, already derivable from
LOG/watchdog), #5 (hygiene ritual, not capability).

## Evidence
- `read considerthese/2026-10-24.md` — full file; proposals at lines 44–50,
  marking heading at line 44 quoted verbatim.
- Output written: `.ufo/waves/round-34/scratch/ScoutConsiderA/list.md`.

Lane bounds: leaf member — no subagents dispatched.

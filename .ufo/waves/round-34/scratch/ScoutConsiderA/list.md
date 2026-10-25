# ScoutConsiderA — proposals in considerthese/2026-10-24.md

Source: `considerthese/2026-10-24.md` (read-only). Only numbered proposals live in the
"Self-improvement suggestions" section (line 44). Every item below is marked by the
file's own section heading; no individual item carries a separate implemented marker.

Marking sentence, identical for all six (line 44, verbatim):
> `## Self-improvement suggestions (proposals only; not acted on)`

| # | One-line demand | Marked status | Marking sentence (verbatim) |
|---|---|---|---|
| 1 | Report a domain-vs-meta ratio per window; flag when 2+ rounds pass without a desktop-facing change (`tools/`, `corpus/knowledge/`, `PROVINCE.md`) | NOT implemented — proposal only | `## Self-improvement suggestions (proposals only; not acted on)` |
| 2 | Report run reliability (dead attempts, OOM kills, provider 429s) as its own line, counted from LOG and watchdog lines | NOT implemented — proposal only | `## Self-improvement suggestions (proposals only; not acted on)` |
| 3 | Keep a short carried list of routed items (n2 relevance cheat, Holds semantics, undispatched waves) and check each off by commit in later files | NOT implemented — proposal only | `## Self-improvement suggestions (proposals only; not acted on)` |
| 4 | Read PROVINCE.md and explicitly propose the next Hyprland table (window rules, monitors, layer rules) with grounding sources | NOT implemented — proposal only | `## Self-improvement suggestions (proposals only; not acted on)` |
| 5 | Verify one cited fact first-hand per day, read-only (e.g. re-open one of S178–S182 and confirm the quoted line) | NOT implemented — proposal only | `## Self-improvement suggestions (proposals only; not acted on)` |
| 6 | Note the window's time-of-day pattern (round 28 opened 17:46 BRT; rounds 29–31 landed 02:24–04:23 BRT) so host load can be correlated | NOT implemented — proposal only | `## Self-improvement suggestions (proposals only; not acted on)` |

No other section of the file contains proposals; the "Open debt carried forward"
table is a status ledger, not a proposal list.

## Recommendation (≤3)

All six are proposals-only; recommended three, ranked by leverage on the file's own
named gaps (domain drift, carried debt):

1. **#4 — Suggest the next desktop table explicitly.** Directly attacks the file's
   bottom line: no `tools/` or `corpus/knowledge/` change since round 27. Turns the
   next round toward domain work instead of a fifth self-audit round.
2. **#1 — Domain-versus-meta ratio.** Cheap (harm-watch diffs already recorded in
   LOG) and makes the drift the file complains about measurable per window.
3. **#3 — Carried follow-up list.** Nearly free; converts routed items (n2 cheat,
   Holds↔note overlap, undispatched waves) into a checklist closed by commit, which
   the file shows already worked for M26-10 → `b6650d5`.

Not recommended now: #2 and #6 are operator-facing observability (João can already
read LOG/watchdog); #5 is good hygiene but adds a ritual, not capability.

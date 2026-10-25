# SimplifyRows — `teaches` cells for S203–S210

Scope: the eight new registry rows in `.ufo/waves/round-35/controls/golden/corpus/SOURCES.md`.
Task: shorten each `teaches` cell to one grounded learner benefit in ≤25 words without losing a claim.
Committed tree untouched — proposed text lives only in this report.

Word count method: whitespace-separated tokens containing at least one alphanumeric character (bare `-` separators not counted).

## Shortened `teaches` cells

| id | before (words) | proposed `teaches` | after (words) | saved |
|---|---|---|---|---|
| S203 | 33 | The post-login questionnaire runs twelve first-run scripts and asks nothing about the idle lock | 14 | 19 |
| S204 | 37 | Two negatives agree: 12 setup scripts hold no idle-lock question, and zero omarchy-toggle invocations appear in the sessions the journal keeps | 21 | 16 |
| S205 | 45 | Idle lock ARMED: hypridle pid 1667, two journal start lines on 2026-10-23; the unit probe's inactive reflects a transient scope - the process probe is true | 25 | 20 |
| S206 | 27 | The bar's idle-indicator module toggles the idle lock on click - the choice is offered in the running interface, not only at setup | 22 | 5 |
| S207 | 34 | The indicator renders nothing while hypridle runs, and an icon reading "Idle lock disabled" when it is not - the desktop names both states | 23 | 11 |
| S208 | 28 | The menu lists an Idle Lock entry among its toggles, dispatched to the same command - the choice sits in two independent surfaces | 22 | 6 |
| S209 | 30 | All four dated copies of the bar's configuration carry the idle-lock click handler, the oldest dated 2026-10-03 on this host - the offer is not recent | 25 | 5 |
| S210 | 44 | This toggle-state directory holds entries for other toggles but none for the idle lock - the operator's choice leaves no trace where one would | 23 | 21 |
| **total** | **278** | | **175** | **103** |

## Claim-preservation notes

- **S203**: the enumeration of the twelve script names compresses to its count — the only information elided anywhere in the set. No assertion is dropped (twelve scripts run; none about the idle lock).
- **S204**: all three claims kept (no idle-lock question in the 12 scripts; zero omarchy-toggle invocations; journal-retention caveat via "the sessions the journal keeps").
- **S205**: all five claims kept (armed; pid 1667; two start lines on 2026-10-23; unit probe inactive because of transient scope; process probe is authoritative). "On this host" is already pinned by `scope`/receipt columns.
- **S206**: both claims kept (click runs the toggle; offer exists in the running interface, not only at setup).
- **S207**: all claims kept, tooltip string "Idle lock disabled" preserved verbatim.
- **S208**: both claims kept (entry among toggles; same command → two independent surfaces).
- **S209**: all claims kept (handler in every copy; count four; oldest 2026-10-03 on this host; not recent).
- **S210**: all claims kept (directory records other toggles' state; no idle-lock entry; choice leaves no trace where one would exist).

## Verification

Counts computed mechanically over the strings above (Python, token rule stated). All eight proposed cells ≤25 words; each is a single sentence stating one grounded learner benefit.

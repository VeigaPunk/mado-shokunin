# ScoutConsiderB — considerthese/2026-10-23.md proposal inventory

Source: `considerthese/2026-10-23.md` lines 45–53, section `## Self-improvement suggestions`.
Seat: reflection-seat scout; file is READ-ONLY and was not edited.

## Marking

The file's only implemented/not-implemented marking is the section header itself, a
list-wide marking covering all seven items — quoted verbatim:

> `## Self-improvement suggestions (proposals only; not acted on)`

No per-item implemented/not-implemented marker exists. The same header wording is used
in every daily file (2026-10-19 through 2026-10-24), so "not acted on" is the standing
marking for every proposal in the series, including earlier recurrences noted below.

## Proposals

| # | One-line demand | Marking (file) | Covered by lane corpus? (`corpus/knowledge/` + `corpus/SOURCES.md`) |
|---|---|---|---|
| 1 | Scan each window's lessons for host-safety mistakes and put them at the top of the same-day message to João, separately from capability news. | "proposals only; not acted on" (section header) | **Not covered.** Zero hits for `host.safety|HOST_SAFETY|coredump|host.impact` in the scoped dirs. The domain side exists (round-26 `HOST_SAFETY … delta=` receipts, `harness/oracle.py`, lessons M25/M26) but lives in `corpus/lessons/` and `.ufo/`, outside the scoped grep and outside the reflection's same-day flag. Recurrence: same idea proposed 2026-10-20 item 1, still "not acted on". |
| 2 | Keep a running "rounds since last admission / artifact being worked" line to make pivots and stale repair loops visible. | "proposals only; not acted on" | **Not covered.** `streak|admission|pivot` hits in corpus are domain-admission ledger rows (SOURCES.md statuses, `arc-synthesis.md` tables) — none tracks a reflection-side streak/pivot metric. Recurrence: 2026-10-21 item 1 (loop flagging) and 2026-10-22 item 1 ("rounds on the same artifact / admitted" metric) proposed the same instrument; still open. |
| 3 | Re-open one pinned cited line per day (e.g. S177) so each reflection verifies at least one fact first-hand. | "proposals only; not acted on" | **Adjacent, not covered for the reflection.** The corpus *method* already does this: `SOURCES.md` `recheck` column and per-note `verified-at`/`recheck` headers re-open pinned lines (`gate-standing-use.md` rule "moved pin is reported first… never a silent pin update"). But that is lane rounds re-checking sources, not the daily reflection re-opening one cited line itself. No corpus note assigns the reflection a first-hand check. |
| 4 | Keep a short list of accepted "trade" rulings (e.g. M26-10) and check in later reflections whether the routed fix landed. | "proposals only; not acted on" | **Adjacent, not covered for the reflection.** `arc-synthesis.md:285` has "Trades named as trades (not admitted as improvements)" and debt tables route fixes — but no single accepted-trades watch list exists for the reflection to follow through on. `M26-10` itself: no hits in the scoped dirs (it lives in `corpus/lessons/round-26.md`). |
| 5 | Read in-progress rounds' `registration.md` so tomorrow's reflection can compare outcome against intent. | "proposals only; not acted on" | **Not covered for the reflection.** Lane rounds cite `registration.md` as claim evidence (e.g. `mutation-testing-r28.md:18,24` citing `.ufo/waves/round-28/registration.md`), but no corpus item instructs or records the reflection reading mid-flight registrations. |
| 6 | Page commit lists fully (or note the cap) so window counts are exact, not lower bounds at the 100-commit API page. | "proposals only; not acted on" | **Not covered.** Zero hits for `commit.*cap|pag(e|ing|ination)|100 commits|lower bound` in the scoped dirs. No corpus guidance on enumeration completeness for the reflection's commit windows. |
| 7 | Offer an operator-actionable read-only "what your config resolves to" note (with João's OK), e.g. which animation nodes inherit. | "proposals only; not acted on" | **Partially covered as convention, not as this deliverable.** The corpus already produces operator-facing read-only summaries: `config-health-report-r3.md` §7 "Operator recommendation summary", `gate-standing-use.md` §7 "Handoff — the operator's part", `theme-route-r18.md`/`idle-lock-route-r17.md` "What an operator may read without mutating state". Missing specifically: a resolver-output digest for João from `tools/mado-binds.py`/`mado-anims.py`/`mado-wsrules.py`. Recurrence: 2026-10-21 item 2 and 2026-10-22 item 2 proposed an operator option/brief; still open. |

## Summary

- 7/7 proposals marked "proposals only; not acted on" — none implemented at write time
  of the source file (2026-10-23).
- Direct coverage in scoped corpus dirs: **none** for items 1, 2, 5, 6; **adjacent
  method/practice only** for 3, 4; **convention exists, deliverable absent** for 7.
- All seven are reflection-process suggestions (how the considerthese files are
  produced), so absence from `corpus/knowledge/` (domain knowledge) is expected —
  coverage would have to come from reflection-side practice, which the recurrence
  history shows has not landed.
- Recurring proposals: host-impact flagging (10-20, 10-23), streak/loop metric
  (10-21, 10-22, 10-23), operator brief (10-21, 10-22, 10-23 item 7).

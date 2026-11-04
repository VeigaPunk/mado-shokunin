# R77ConnSiblings — working notes (report.md)

Working copy of the scoped findings; the trailer-named deliverable is
`.ufo/waves/round-77/w1/R77ConnSiblings.md` (same content). Read-only scan; nothing edited
outside this directory and the trailer file; scratch deleted.

## Scan summary table

| # | question | finding | key evidence (paths:lines) |
|---|---|---|---|
| 1 | Does a sibling lane own/claim the layer plane / bar footprint / runbook-execution surface? | **No.** `hyprctl layers`/`layers -j`: 0 hits in all 20 siblings; `bar footprint`: 0 hits. Only live-hyprctl sibling is game-dev-2d (`clients -j`, game-window probes). `waybar` appears only as a PipeWire client name in audio receipts. chousa's "probe table"/"runbook" is its own reference-integrity/receipt vocabulary. kama r50 and mori r53 explicitly rule mado's ground distinct. mado's title: PROVINCE.md:28,35 + SKILL.md:204 ff. | game-dev-2d `corpus/live/r79-boundary-exec/run_love_probe.py:42`, `reports/round-79/r79-boundary.md:196,202`; audio `corpus/live/r81-scout/receipts/s0-baseline.json:152-153`; kama `.ufo/waves/round-50/w1/out/N1Overlap2.md:43`; mori `.ufo/waves/round-53/w1/Mo53ConnSiblings.md:41-43,118-121`; mado `PROVINCE.md:28,35`, `SKILL.md:204` ff. |
| 2 | Recurrence of the routed "stale revision citation" class in the last ten lessons, and is r77's fix the first that can fail? | **9 instances in rounds 68–77** (r71 404 citation; r73 D1/S448 sha drift mined as M74-3; r74 M74-4 path drift; r75 R5; r76 D2 "repeat of round-75 R5"; r76 D3 stale declaration/docstring text; r76 D7 pointer arithmetic; r76 D8 declaration pointer; r77 M77-4 anchor drift). Every pre-r77 fix is a one-time prose re-cite, corrected value, or documented manual command — none is standing executable machinery. M77-3's "first that can fail" claim is supported, with caveats: the R77ExecRepairs check was not yet landed at scan time (dir empty), and "can fail" requires routine invocation. | `round-71-verifier-spotcheck.md:139-142`; `round-72.md:84-88`; `round-74.md:45,46`; `round-75-verifier-spotcheck.md:121,171-174`; `round-76-verifier-spotcheck.md:179-187,204-210`; `round-77.md:15,16` |
| 3 | Is 2026-10-28 proposal 4 (live-tool table) still unimplemented, and do the new instruments change the answer? | **Still unimplemented at tip**: the r51 tracked ledger grammar is 3 cells with no last-live-run column; the reflection's own carried row says so; r51's reviewer seat was scoped to the same shortfall; r46/r47 drafts of the table were refused after w2 found wrong rows. **The round's pair changes the economics**: c2-r77-runbook.py makes the SKILL probe table executed+matched (12/12), and mado-barfoot.py receipts re-measure/print `rev=`+`tool_sha256=` — the freshness datum in machine-readable form. Absorb next round as ledger grammar v2 seeded with these two rows; not this wave (freeze, seat write scope, r48 refusal precedent, checker must change with the rows). | `considerthese/2026-10-28.md:47,55`; `quality/tool-ledger.md` header; `.ufo/waves/round-51/make-w1-spec.py:477-481`; `.ufo/waves/round-46/w1/ConnToolFamily.md:128-131`; `.ufo/waves/round-47/w1/ScrToolLedger/ledger.md:63-66`; `.ufo/waves/round-48/w1/ScrMistakes/controls/report-97-fixed.md:85` |

## Proposed move, risks, verification

Move: one standing instrument-freshness gate — land the M77-3 cited-revision check wired for
routine invocation (gate selftest family; no-harm plan allows "460/460 or better"), then seed
proposal 4's ledger v2 next round with the two r77 instruments as first rows from the existing
receipt shape. Improves the verification surface behind C1/C2 and the freshness sub-axis r75
declared "no claim"; moves no predicate, control set, or committed byte this round.

Risks: check unlanded at scan time (claim pending red/green); un-wired check repeats the M74-4
one-time-grep pattern (class would recur a third time); ledger v2 must carry r49's corrected
receipt search rule or re-imports r47's H1 wrong-row class; absorbing mid-wave violates the
freeze — deferral is part of the move.

Verification: check fails on r76 bytes naming the D2 pair, passes on corrected bytes;
`bash tools/mado-verify.sh --selftest` 460/460 or better; `quality/check-tool-ledger.py` exit 0
with grammar unchanged this round.

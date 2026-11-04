# R77ConnSiblings — cross-lane / cross-round pattern scan (round 77, v1 wave 1)

Scope: read-only scan of all 20 sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin`,
the lane's last ten lessons (`corpus/lessons/round-68.md` … `round-77.md` plus verifier
spot-checks), and `considerthese/2026-10-28.md`, judged against the frozen declaration
`.ufo/waves/round-77/claims-declaration-r77.md`. No lane file edited; no host state touched;
scratch deleted.

## 1. Does any sibling lane already own or claim the surface? — NO

| ground term | sibling hits | verdict |
|---|---|---|
| `hyprctl layers` / `layers -j` | 0 files across all 20 sibling repos (exact grep) | the layer plane is unclaimed outside mado |
| live `hyprctl` verbs | game-dev-2d-shokunin only: `corpus/live/r79-boundary-exec/run_love_probe.py:42` spawns `hyprctl clients -j`; `reports/round-79/r79-boundary.md:196,202` uses it as window evidence for LOVE game-engine probes | nearest live-hyprctl neighbour; verb is `clients`, surface is game-window state — not the layer plane, bar footprint or reserved band; no claim on mado's surface |
| `waybar` | audio-shokunin only, and only as a PipeWire client process name inside live receipts (`corpus/live/r81-scout/receipts/s0-baseline.json:152-153`, `r80-scout/p7-linkauthority.json:424`) | incidental session material in audio receipts; zero config-surface claims |
| `bar footprint` | 0 sibling hits | unclaimed |
| `probe table` / `runbook` | chousa uses both words for its own reference-integrity probe table and receipt runbooks (`chousa/.ufo/waves/round-50/w1/ExecSelftestEdge.md:10`; `round-43/assimilation/validate/corpus/README.md:42-43`) | different substrate entirely — no desktop ground |
| siblings' own overlap rulings | kama r50 classifies mado's "hyprctl readback joins" as "the same 'compare against own vocabulary' shape on a different substrate" (`.ufo/waves/round-50/w1/out/N1Overlap2.md:43`); mori r53: "mado: hyprctl/hyprlang pins … No overlap" (`.ufo/waves/round-53/w1/Mo53ConnSiblings.md:41-43,118-121`) | siblings already ruled mado's ground distinct from theirs |

mado's own title to the surface: `PROVINCE.md:28` (mado-verify.sh reads the hypr / waybar /
walker / terminal / theme trees plus the `hyprctl` read verbs "version, instances, configerrors,
getoption, binds, monitors, layers"), `PROVINCE.md:35` (round-23 correction: live read-only
probes), and `SKILL.md:204` ff. — the read-only-probes table whose `hyprctl layers -j` row
answers "compositor-side view of bar/launcher layer surfaces". **C1 and C2 land on unclaimed
ground; no cross-lane collision.**

## 2. "Stale revision citation" recurrence in the last ten lessons — 9 instances in rounds 68–77; r77's check is the first in-class fix that can fail on the defect

| round | instance (lesson line) | fix that landed | can that fix fail on the defect? |
|---|---|---|---|
| 71 | lesson's rejected-source citation is a 404 at the pinned v3.14.8 tag (`round-71-verifier-spotcheck.md:139-142`) | r72: S446 rejected row re-cites the real `Doc/builtins/` path with 3× fetch evidence (`round-72.md:84-88`) | no — one-time prose/registry re-cite |
| 73→74 | SOURCES S448 sha256 transcribed falsely; r73's own scout caught it, no correction landed (M74-3, `round-74.md:45`) | r74: corrected digest + QUALITY 6 re-derivation duty (red = the cell, green = three fetches) | no — duty + one-time re-derivation, no standing check |
| 74 | criteria 118–119 landed at root `QUALITY.md`, not `corpus/QUALITY.md` (M74-4, `round-74.md:46`) | append + one-time `grep -c '^118\.'` red/green | no — one-time grep, not standing |
| 75 | R5 revision attribution: SCORECARD says C2 was measured at `4527fcae` "(its instrument's last change)" while the instrument last changed at `f75afbf6` (`round-75-verifier-spotcheck.md:171-174`); freshness axis recorded "no claim … revision-attribution defects routed (R5)" (`:121`) | none — routed | — |
| 76 | D2, self-described "repeat of round-75 R5": `SCORECARD.md:4339` cites `5dade9b3`, instrument last changed `3588a527`, no matching receipt exists (`round-76-verifier-spotcheck.md:179-183`) | none in r76 — routed to r77 | — |
| 76 | D3: frozen-declaration "fifteen-case" text vs a sixteen-case set; counter docstring lists superseded mutants and a `cases=15` example (`:184-187`) | r77 route: errata append + text-only docstring fix (declaration D3) | no — text-only by design |
| 76 | D7 report pointer arithmetic (`:204-206`) and D8 declaration pointer (`:207-210`) | lesson correction block + documented `git diff --name-status` command | no — documented manual command |
| 77 | M77-4: own draft line-anchor drift, caught by the pre-commit anchor sweep (`round-77.md:16`) | anchors corrected; re-derivation is the grep | no — manual re-derivation |

Verdict on `round-77.md:15` (M77-3): the class recurred **9 times in ten rounds**, including a
back-to-back repeat (r75 R5 → r76 D2) that was routed twice with no fix landing. The round's
fix — an append-only correction plus an executable cited-revision check from `R77ExecRepairs`
that "fails on the r76 text and passes after the correction" — is correctly claimed as **the
first fix for this class that can fail on the defect itself**: no earlier fix in the class is
standing executable machinery. Two caveats so the claim survives audit:
(a) at scan time `.ufo/waves/round-77/w1/R77ExecRepairs/` is empty — the check is in flight;
"first that can fail" is a design + landing claim, not yet a measured red/green pair;
(b) "can fail" holds only under routine invocation — the nearest standing executable cousins,
`quality/check-deliverables.py` (declared paths at the cited revision) and
`quality/check-locators.py` (receipt:line locators), cover adjacent classes; a standalone
un-wired check would repeat the M74-4 one-time-grep pattern. The two r77 counters themselves
already print re-measured `rev=` / `sha256=` in every receipt (declaration, Freeze bullets) —
the same discipline extended to this round's own instruments.

## 3. `considerthese/2026-10-28.md` proposal 4 (live-tool table) — still unimplemented; the round's instrument pair makes absorption justified, as next-round work

Proposal 4 (`considerthese/2026-10-28.md:55`): "Keep a live-tool table … One row each (question
answered, last live run, verdict, who ran it) … This is the half of the 2026-10-26 proposal 2
the lane has not built."

| evidence | pointer |
|---|---|
| the reflection's own carried-items row: "proposal 2 partly became the r51 tool ledger (the last-live-run column is still open)" | `considerthese/2026-10-28.md:47` |
| the landed ledger's row grammar is 3 cells — instrument path / description / accountability pointer; no freshness cell anywhere in the tracked file | `quality/tool-ledger.md` header (row-grammar block, pre-table) |
| r51's own reviewer seat was scoped to name exactly this shortfall: "the proposal asks for last-live-run and verdict per tool; C1 covers accountability, not live-run freshness" | `.ufo/waves/round-51/make-w1-spec.py:477-481` |
| r46/r47 seat drafts built precisely this table as wave evidence; it was refused as production after the w2 audit found wrong rows ("the live-tool ledger was refused this round … `w2/ExecToolLedger.md` found wrong rows") | `.ufo/waves/round-46/w1/ConnToolFamily.md:128-131`; `.ufo/waves/round-47/w1/ScrToolLedger/ledger.md:63-66`; `.ufo/waves/round-48/w1/ScrMistakes/controls/report-97-fixed.md:85` |

Do the round's new instruments change the answer? **Yes — they supply what the column was
missing.** `quality/counters/c2-r77-runbook.py` turns the SKILL.md probe table into an executed,
expectation-matched batch (`executed=12 matched=12`), making the "which ones can João run
himself today" property mechanically checkable rather than curated; `tools/mado-barfoot.py`
lands with receipts that re-measure and print `rev=` / `tool_sha256=` on every run — the exact
freshness datum the missing column needs, already machine-readable.

Absorption verdict: **justified now, as round-78 production work — not inside this wave.** Lane
rules that force the deferral: the freeze and control sets are committed (a mid-wave ledger
grammar change is unregistered work touching `quality/` bytes no seat may write); the r51
checker enforces the 3-cell grammar, so a fourth cell needs a checker change landing together
with the rows; and the r48 refusal precedent demands correct rows first — the two r77
instruments, whose receipts re-measure their own hashes, are exactly two provably-correct seed
rows.

## Proposed move (connector synthesis)

One non-obvious move that improves an axis and harms none: treat M77-3's cited-revision check,
the counters' receipt hash-printing, and proposal 4's missing column as **one missing
instrument — a standing, routinely-invoked instrument-freshness gate**. Land the R77ExecRepairs
check wired for routine invocation (its red/green joined to the gate selftest family; the
no-harm plan already admits "unchanged at 460/460 or better"), then seed proposal 4's ledger v2
next round with the two r77 instruments as its first rows using the existing receipt shape.

**Affected axes:** the verification surface behind both C1 and C2 ("measured at REV" sentences
become mechanically checkable) and the freshness sub-axis r75 declared "no claim" — a
C2-adjacent operability gain; neither claim predicate, control set, nor any committed byte of
this round moves.

**Risks:** (1) the check is not landed at scan time — the claim is pending its red/green pair;
(2) an un-wired standalone check decays into the M74-4 pattern and the class recurs a third
time; (3) ledger v2 must carry r49's corrected search rule (receipt-shaped files over every
blob at the revision, seat dirs included) or it re-imports the r47 H1 wrong-row class; (4)
absorbing the column this round would violate the freeze and seat write scope — the deferral is
part of the move, not a shortcut.

**Verification:** after landing — run the check against the r76 bytes (must fail, naming the
D2 revision pair) and against the corrected bytes (must pass); `bash tools/mado-verify.sh
--selftest` stays 460/460 or better; `quality/check-tool-ledger.py` exits 0 with the grammar
unchanged this round.

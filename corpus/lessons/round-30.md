author: mado

# Round 30 — index-gap closure, criterion-grounding repair, index gate

Base: lane tip `8f51071b5bc44c815eeb5da76bb7f1947994ffb8` (round-29 closure:
admitted; C1/C2 TARGET_MET, the inherited 41/43 navigation gap routed here as
the round's first claim).

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M30-1 | attribution | `corpus/QUALITY.md` criteria 1–5 carry no lesson citation; 18, 19 and 32 cite a lesson only outside the numbered line; 38–40 cite bare `M28-x` ids with no path — the literal rubric (`grep -cE '^[0-9]+\. .*lessons/'`) reads 28/40 at base and the resolved-active rubric (`.ufo/waves/round-30/c2/count.py`) reads 31/39. The seed block's true ground is `MINT.md`, never recorded. | `none` — criterion 22 audits rubric *selection*, but nothing required each criterion's own citation to resolve. | Rows 41–51 supersede the ungrounded criteria verbatim with canonical `(lesson: lessons/<file>#<anchor> <id>)` citations (1–5 grounded on `MINT.md` + this row); the fix is shown able to fail: the C2 counter at base prints `UNRESOLVED criterion 1..5, 38..40` and `TARGET_MISSED` exit 1 (control `controls/C2K1-donothing.txt`). |
| M30-2 | scope | The round-29 sweep row (`corpus/lessons/round-29.md` `## Mistakes`, M29-sweep) records the navigation counter at 41/43 at base and tip alike — `mutation-testing-r28.md` and `workspace-rules-r27.md` absent from `corpus/README.md` index rows since rounds 27/28 — and correctly routed it instead of repairing under the table. The mistake is the gap itself: two admitted notes unreachable from the coverage map for two full rounds, through two closures that re-ran the census but never the navigation counter. | `none` — the navigation counter is a fence (harm watch), not a gate; no criterion made index completeness a claim input. Criterion 52 captures the record-then-claim discipline. | Repaired as declared claim C1 this round (the two index rows land; counter 43/43 exit 0, receipt `evidence/c1-after-*.txt`) and made repeatable by C3's `quality/check-index.py` gate (red at base, green at tip). |

## Gate

S185 was opened this round on 2026-10-24: the frozen navigation counting
command embedded in `SCORECARD.md` (own-work source, the fence that caught the
routed gap and the spec the C3 gate implements).

| id | source path | URL | access date | located quote (≤25 words, verbatim) |
|---|---|---|---|---|
| S185 | `SCORECARD.md` "Fleet round 1 — coverage navigation" counting-command fence | `SCORECARD.md` (own-work; sha256 of the block `8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88`) | 2026-10-24 | `revision=$rev indexed=$covered/$total missing=$missing dangling=$dangling duplicates=$duplicates coverage=$score/10` |

**Decision:** admitted as `own-work` tier A scoped to index-completeness
semantics. The row grounds claim C3 (`quality/check-index.py` implements the
fence's row-set semantics) and is cited by C1's registration; it makes no
claim about note truth or freshness. The `used-by` paths
(`quality/check-index.py`, `.ufo/waves/round-30/registration.md`) exist at the
round's final commit.

**Registry changes this round:** rows 184 → 185 (+S185, opened 2026-10-24,
status `mined`). No status/recheck flips on existing rows; no new rejection
considered (S062 remains the standing reject sample). The seven W04
duplicate-URL warnings (S030/S042/S045/S097/S119/S120/S121) were re-checked
against criterion 17: each pair is supersession or distinct-scope reuse with
the rejected history preserved (S030→S045 rejected-duplicate, S042 supersedes
S006 in a disjoint scope, S119 supersedes S113's scope, S120/S121 pin
different sections of one file, S097 supersedes S094). No action; the
warnings stand as intended collision-review markers.

## Notes

**C1:** the two rows are navigation only — they assert each note exists and
what it holds, quoted from the notes' own headers; they admit no new domain
claim. The do-nothing control is the frozen counter itself at base
(`indexed=41/43`, exit 1).

**C2:** superseded lines leave both fractions' denominators (criterion 21's
supersedes-20 precedent); literal and resolved metrics are reported side by
side per criterion 22 — literal 28/40 → 40/52, resolved-active 31/39 → 40/40.

**C3:** the capability is the gate, not the green verdict: it must print
`indexed=41/43` exit 1 at base and `indexed=43/43` exit 0 at tip, and its
`--selftest` (6/6) covers missing/dangling/duplicate/symlink-refused/empty.

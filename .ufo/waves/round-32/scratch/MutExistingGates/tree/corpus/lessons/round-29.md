author: mado

# Round 29 — composite repair, routed-queue closure, S184 gate

Base: lane tip `f652ca99c64631a72e06a7d2f6ffa1708794f65e` (round-28 closure:
rejected-honest-stop; the r28 records stand, including the missed
`PRED-C1-r28` AND-bit — this round registers new predicates, never rewrites
the frozen ones).

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M27-4 | reference-drift | The round-27 report sentence "the tool's docstring and the knowledge entry cite them [S178–S182]" names a citation location the committed bytes do not have: `tools/mado-wsrules.py`'s docstring cites upstream source files, only `corpus/knowledge/workspace-rules-r27.md` frontmatter cites the S-ids (`corpus/lessons/round-27-verifier-spotcheck.md` item 6; re-verified this round by reading the docstring). The defect was routed as the tenth record defect and repaired this round. | `none` at round 27 — the harm watch covered `tools/` byte changes, not report-vs-bytes citation-location claims. Now captured by the C2 R4 check (marker `§6.6 erratum (round 29)`) and by this erratum discipline. | Append-only `§6.6 erratum (round 29)` block in SCORECARD.md's round-27 section naming the true citation location. Shown able to fail: the C2 do-nothing control at base prints `CHECK R4 FAIL` (`.ufo/waves/round-29/controls/C2K1-donothing.txt`). |
| M29-sweep | none-found | Sweep for new defects introduced by this round's freeze: `bash tools/mado-verify.sh --selftest` → `MADO_SELFTEST: 460/460 assertions passed`, exit 0; census `validate` exit 0 (rows 183 → 184); controls C1K1/C1K2/C2K1 each print their registered miss; `git diff --stat f652ca99 <freeze> -- tools/ corpus/knowledge/ SKILL.md PROVINCE.md` empty. One sweep line was found FALSE after commit and is corrected above it: the navigation counter does NOT stay exit 0 — it reads 41/43 at base and tip alike, an inherited round-27/28 index gap (`mutation-testing-r28.md`, `workspace-rules-r27.md` absent from `corpus/README.md` index rows), not an r29 regression; routed to round 30 intent, not silently repaired (claim discipline: no unregistered claim work). | n/a | The false sweep line is struck by this row; the honest sweep result is recorded here with commands. |

## Gate

S184 was opened this round on 2026-10-24 at the DOI reader (same title-level
treatment as S183; no abstract-level claim is made).

| id | source path | URL | access date | located quote (≤25 words, verbatim) |
|---|---|---|---|---|
| S184 | DOI reader metadata | https://doi.org/10.1002/stvr.1473 | 2026-10-24 | `Covering and Uncovering Equivalent Mutants` (Software Testing, Verification and Reliability, 23(5), 353–374) |

**Decision:** the title frames the equivalent-mutant question only; no article
result or method detail is attributed to the inaccessible text. The S184 row
(`corpus/SOURCES.md:196`) scopes tier A to the equivalent-mutant question and
its `used-by` names this round's registration and lesson; the census mined-row
used-by check passes at the round's final commit. No discrepancy.

**Registry changes this round:** rows 183 → 184 (+S184, opened 2026-10-24,
status `mined`). No status/recheck flips on existing rows; no reject was
considered this round (the standing registry carries the S062 reject as the
outside reject sample).

## Notes

**C1:** the h1-receipt leg's verification basis is a committed reviewer-authored
receipt (QUALITY 39 named-receipt basis), not a fresh run — the suite it
certifies was itself re-derived against the committed held-out2 set in the
round-28 w2 review; the boundary is declared in the registration and report.

**C2:** the four repairs are record-level; the composite's green run is C1's
evidence, not C2's.

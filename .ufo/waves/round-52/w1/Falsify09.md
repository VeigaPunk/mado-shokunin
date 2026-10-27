# Falsify09 — C1 self-pointer/context bypass probe

Seat: Falsify09 (leaf, mutation-tester). Round 52, mado, base `85d57a818c3707397e21c840b6498b105ba798aa`.
Attacked item: **C1 (operability)**. Attacked clause: "non-self resolvable evidence targets" together with "a description containing instrument-specific functional context" (claims-frozen.md C1; registration.md frozen predicates).

## One-sentence finding

A no-work ledger that is lexically non-self and context-shaped — 82 unique rows whose every pointer is a same-commit **witness file** listing all instrument basenames, with uniform template descriptions — is `TARGET_MET` for the real lane counter today and **passes all four frozen C1 checks** (uniqueness, resolvable, non-self, context) on a seat-local detector: **mutant SURVIVED**; the planned red/green demonstration (production pass, `c1-do-nothing.md` fail) does not exclude this family.

## Bypass construction (all bytes at base; scratch only)

Fixtures under `/fast/scratch/hyaku/mado-r52/Falsify09/` (removed on exit; receipts copied to seat dir). Three clones of the lane at `85d57a81…`:

- `pristine/` — untouched base.
- `bypass/` — `quality/tool-ledger.md` rewritten: all 82 row paths kept, description cell replaced by the uniform template `` `<basename>` provides the function recorded for its tracked lane role in this row ``, pointer cell replaced by `` `quality/ledger-witness.md` ``; new file `quality/ledger-witness.md` = the 82 population basenames, one per line. Committed as one fixture commit pair (`fcef99ab` ledger, then `3ab3355a` witness after the first attempt omitted the untracked witness — reported honestly below).
- `control/` — `quality/tool-ledger.md` overwritten with the verbatim bytes of `.ufo/waves/round-52/controls/c1-do-nothing.md` (`ad72f72f…`), committed `bc932d8c`.

Why the witness defeats "non-self": the frozen checks bind the pointer to (a) exist at the revision and (b) name the instrument basename in its bytes (lane mechanics: `check-tool-ledger.py` `names_basename`, `c1-r51-ledger.py` `pointer_resolves`). A co-committed witness satisfies both for every row, and `quality/ledger-witness.md != quality/tool-ledger.md`, so a lexical/path non-self check passes. Nothing in the frozen C1 predicate requires evidence independence from the ledger author (contrast C2, which has an independent non-author reviewer).

## Commands and actual results

Lane counter, run three times (`python3 -I quality/counters/c1-r51-ledger.py --repo <fixture> --rev <rev> --work <scratch>/work/<name>`, `TMPDIR=<scratch>/tmp`):

| fixture | rev | verdict (actual) |
|---|---|---|
| pristine | `85d57a81…` | `population=82 ledger_rows=82 uncovered=0 … selftest=ok verdict=TARGET_MET` exit=0 — matches `receipts/c1-base.txt` |
| bypass | `3ab3355a…` | `population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET` exit=0 — **bypass passes the production gate** |
| control | `bc932d8c…` | `population=82 ledger_rows=2 uncovered=81 bad_pointer=1 dup=1 … verdict=TARGET_MISSED` exit=1 |

Seat-local detector implementing exactly the frozen C1 checks (row parse mirrored from lane sources; resolvable = token committed AND `names_basename`; non-self = ledger path not a pointer token and not named in row cells; context = non-placeholder description ≥6 words — the only realistically mechanical form; plus coverage/uniqueness):

| ledger | result |
|---|---|
| pristine | **PASS** (baseline green — detector sane) |
| control | FAIL (coverage=81, resolvable=2, uniqueness=1 — **not** via self-pointer/context) |
| bypass | **PASS** — all four frozen checks satisfied by the no-work ledger |

Reproduced: **yes** — the base-counter bypass reproduced end-to-end with lane bytes (`w1/Falsify09/receipts/c1-bypass.txt`); the frozen-checks bypass reproduced on the seat-local detector (`falsify09-detector.txt`). First bypass attempt (`fcef99ab`) with the witness accidentally uncommitted correctly scored `bad_pointer=82 TARGET_MISSED`, confirming the counter's resolvability check actually fires and the pass is attributable to the witness, not a fixture artifact.

## Secondary observations (honest, non-voting)

- At base the production ledger contains **zero** self-pointer rows (pristine passes the non-self scan), so the new counter can pass production while still being defeated by the witness family.
- The frozen control's rows are 4-cell (`| path | desc | nothing | generic … |`), which is malformed under the lane's own 3-cell row grammar (`parse_rows`/`evaluate` count them malformed → dangling). Under the lane grammar the control fails via coverage/pointer shape, so a new counter that wants to fail it "specifically for self-pointer/context defects" (registration.md) must define its own parse of this shape — the control as committed does not exercise a resolvable self-pointer at all.
- Attempted context proxy "description must contain the instrument basename" was **rejected during calibration**: it fails the pristine production ledger (real descriptions describe function, not filename). Baseline-failure ⇒ inconclusive, so the weaker word-count form was used; the bypass template satisfies both forms.

## Limitations

- The round-52 counter is absent at base (frozen), so the frozen-checks detector is a seat-local faithful reading of registration.md's four checks, not the builders' code; if their non-self check is stronger than lexical (e.g. rejects same-commit co-authorship, not expressible from the frozen text), the mutant could be killed by their implementation — the finding is against the predicate as written.
- Fixture commits are scratch-repo commits only; the lane repo is untouched: HEAD `85d57a81…`, `git status --porcelain` shows only untracked `.ufo/waves/round-52/` (0 other lines), tracked `quality/tool-ledger.md` at HEAD hashes `df5b3705…` (see `hashes.txt`).

## Verdict

**Survived** — coverage finding on the C1 predicate demonstration: passing production + failing the one frozen control does not establish that the bounded checks distinguish the production ledger from the no-work class; an evidence-independence condition (e.g. pointer target not added in the same commit/author as the ledger, or a non-author spot check as C2 has) would be needed. Per protocol this is a finding, not a contract change; no claim or predicate edited, no tracked file touched.

## Deliverables

- `w1/Falsify09.md` — this report.
- `w1/Falsify09/receipts/c1-pristine.txt` — lane counter on pristine fixture: TARGET_MET 82/82 (matches base receipt).
- `w1/Falsify09/receipts/c1-bypass.txt` — lane counter on witness bypass: TARGET_MET 82/82 (bypass reproduced).
- `w1/Falsify09/receipts/c1-control.txt` — lane counter on frozen control shape: TARGET_MISSED (uncovered=81, dup=1).
- `w1/Falsify09/receipts/falsify09-detector.txt` — frozen-checks detector verdicts: pristine PASS, control FAIL, bypass PASS.
- `w1/Falsify09/hashes.txt` — before/mutated/restored sha256 (restored == pristine == lane HEAD bytes); lane integrity evidence.

Report trailer (relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`):

```
Seat: Falsify09 | Item: Falsify09 (C1 self-pointer/context bypass) | Verdict: SURVIVED (coverage finding)
Report: .ufo/waves/round-52/w1/Falsify09.md
Receipts: .ufo/waves/round-52/w1/Falsify09/receipts/{c1-pristine,c1-bypass,c1-control,falsify09-detector}.txt
Evidence: .ufo/waves/round-52/w1/Falsify09/hashes.txt
Scratch: /fast/scratch/hyaku/mado-r52/Falsify09 (removed on exit)
Lane writes: none outside seat dir; base 85d57a818c3707397e21c840b6498b105ba798aa unchanged
```

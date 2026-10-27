# Falsify34 — C1 uniqueness/population falsification (round 52, w1)

Status: complete. One concrete bypass of the frozen C1 uniqueness predicate,
reproduced against the round-51 reference counter source bytes and a seat-local
fixture. No lane file edited; no host probe; no package query.

## Attacked clause

Frozen C1 predicate (`.ufo/waves/round-52/registration.md`): the new counter
"validates **population row uniqueness**, resolvable evidence pointer, non-self
pointer, and a description containing instrument-specific functional context."
Claim (`claims-frozen.md` C1): the new counter distinguishes the production
ledger from a no-work control "using **unique population**, non-self resolvable
evidence targets, and instrument-specific context checks."

Attacked item: **population row uniqueness** — specifically the gap between
"no two byte-identical parsed rows" and "no instrument of the population is
listed more than once."

## The bypass (mechanism)

Two source-byte facts combine into one hole:

1. **The r51 parser does not normalize cell 1.** `quality/counters/c1-r51-ledger.py:166`
   (`parse_rows`) reduces the first cell with `strip(EMPHASIS)` only; a row whose
   cell 1 is `` `tools/alpha-tool.py:1` `` parses to the path string
   `tools/alpha-tool.py:1`. The gate's normalizer — `quality/check-tool-ledger.py:194-200`,
   `norm_path` with `LINE_SUFFIX.sub("", path)` — strips the `:line` anchor; the
   counter's parser does not.
2. **`describe()` population-gates before every other check.** At
   `quality/counters/c1-r51-ledger.py:220-228` an out-of-population row hits
   `counts["dangling"] += 1; continue` *before* the `seen`-set dup check and before
   pointer resolution (`pointer_resolves`, :196-206, never runs for that row —
   confirmed empirically below: `bad_pointer=0` on anchored duplicates).

Consequence: a ledger that lists the same instrument repeatedly with distinct
`:line` anchors in cell 1 produces parsed rows that are (a) string-distinct, so an
exact-string uniqueness signal reports `dup=0`, and (b) out-of-population, so the
pointer, non-self and context checks never see them. The frozen four-check
predicate names neither `dangling` nor `uncovered`, so a new counter implementing
exactly the four named checks — in the natural inheritance from the file it
replaces — admits such a ledger as TARGET_MET while its coverage claims are
tripled. The r51 counter is *not* bypassed only because its verdict additionally
requires `ledger_rows == population` and zero `dangling`
(`c1-r51-ledger.py:330-334`), an inequality the new counter's predicate does not
name.

The frozen control `controls/c1-do-nothing.md` ("committed ledger shape with only
repeated generic self-pointers") is the *weak* repetition shape: byte-identical
repeats are caught even by exact-string uniqueness (reproduced below, variant B).
The strong no-work shape — anchored repeats with non-self resolvable pointers and
context-bearing descriptions — is what the uniqueness clause must also reject, and
does not under the reference semantics.

## Reproducible setup

- Fixture driver (self-contained, stdlib only): `Falsify34/fixtures/drive.py`.
  It builds throwaway git repos under the seat scratch dir with a 5-file
  population (`tools/alpha-tool.py`, `tools/beta.py`, `quality/check-a.py`,
  `quality/counters/c1-x.py`, plus the real `quality/check-tool-ledger.py` bytes
  so the r51 counter's selftest/ledger sub-run works), a `PROVINCE.md` naming
  every basename (non-ledger, resolvable, non-self pointer target), and four
  ledger variants (copies in `Falsify34/fixtures/ledger-*.md`).
- Commands (run from a scratch cwd; lane repo read-only):
  - `python3 -I Falsify34/fixtures/drive.py` — loads the real counter and gate
    modules from the lane repo by path, parses each ledger with both, and scores
    each against a model of the four frozen checks structured like `describe()`.
  - `python3 -I quality/counters/c1-r51-ledger.py --repo <fixture> --rev <sha> --work <scratch>/work-<v>`
    — the real round-51 counter end-to-end on each fixture.
- Disk guard: `/fast/scratch` at 26% use before work; no ENOSPC; scratch removed
  on exit.

## Actual results

Model of the four frozen checks (exact-string uniqueness inherited from r51,
population gate first), receipt `Falsify34/receipts-model.txt`:

| variant | ledger | dup | bad_ptr | self_ptr | no_ctx | skipped | verdict |
|---|---|---|---|---|---|---|---|
| A-normal | 5 rows, each instrument once | 0 | 0 | 0 | 0 | 0 | **TARGET_MET** (legit) |
| B-dup-exact | `alpha-tool.py` twice, identical | 1 | 0 | 0 | 0 | 0 | TARGET_MISSED (caught) |
| C-dup-anchored | `alpha-tool.py` ×3 (`:1`,`:2` anchors) | 0 | 0 | 0 | 0 | 2 | **TARGET_MET (bypass)** |
| D-full-bypass | every instrument ×3, rotating anchors | 0 | 0 | 0 | 0 | 10 | **TARGET_MET (bypass)** |

Real r51 counter end-to-end (receipts `Falsify34/r51-counter-*.txt`):
- A: `population=5 ledger_rows=5 ... verdict=TARGET_MET` rc=0.
- B: `dup=1 ... verdict=TARGET_MISSED` rc=1; nested gate run flags
  `reason=dangling ... row-duplicate-line-6`.
- C: **`dup=0 dangling=2 bad_pointer=0 ... verdict=TARGET_MISSED`** rc=1 — the
  uniqueness signal is blind (dup=0); the anchored rows are caught only under the
  *unnamed* `dangling` class, and `bad_pointer=0` proves the pointer checks never
  executed on them. The nested gate run normalizes and reports
  `row-duplicate-line-6/7` — the defense exists in-repo.
- D: `dup=0 dangling=10 bad_pointer=0 ... verdict=TARGET_MISSED` rc=1, same
  mechanism at population scale.

## Reproduced: YES

The bypass is reproduced YES against the frozen predicate text plus the round-51
reference semantics the new counter is appointed to replace: variants C and D pass
all four named checks (model verdict TARGET_MET) while listing instruments up to
three times each, and the r51 reference counter confirms both mechanism facts
(`dup=0`, `bad_pointer=0` with `dangling=N`).

## Named defense (what closes the hole)

Uniqueness must be computed on `norm_path`-normalized cell-1 paths (LINE_SUFFIX
stripped, as `quality/check-tool-ledger.py:194-200` already does), i.e. dedupe
like the gate, not like `c1-r51-ledger.py:166/224-228`; and any row whose
normalized path is not in the population must itself be a verdict defect, not a
silent `continue`. If the committed c1-r52 counter does both, this attack dies;
the claim should be scored against that.

## Limitations / dissent

- The new counter was not yet committed anywhere in the lane at test time
  (untracked tree shows only `.ufo/`; no `controls/c1-do-nothing.md`, no
  `receipts/c1-base.txt`, no c1-r52 counter file), so the model — built from the
  frozen predicate text and the r51 reference structure — is the attack surface,
  not a specific new-counter implementation. This is a predicate-level
  falsification with reference-semantics reproduction, not a demonstration against
  the final artifact.
- The production ledger at base (82 rows) contains no `:line`-anchored cell 1, so
  the production-pass side of the claim is unaffected by this attack.
- No installs (Python 3.14.8 + git 2.56.0 only); no pacman; no live reads, no
  host/config mutation; source checkout read-only throughout.

## Deliverables

- `Falsify34.md` (this report)
- `Falsify34/receipts-model.txt` — four-variant parser/model comparison receipt
- `Falsify34/r51-counter-A-normal.txt` — real counter, clean baseline (TARGET_MET)
- `Falsify34/r51-counter-B-dup-exact.txt` — real counter, exact duplicate caught
- `Falsify34/r51-counter-C-dup-anchored.txt` — real counter, dup=0/dangling=2 mechanism proof
- `Falsify34/r51-counter-D-full-bypass.txt` — real counter, population-scale mechanism proof
- `Falsify34/fixtures/drive.py` — self-contained fixture driver (reproduces all receipts)
- `Falsify34/fixtures/ledger-A-normal.md`, `ledger-B-dup-exact.md`,
  `ledger-C-dup-anchored.md`, `ledger-D-full-bypass.md` — the four ledger variants

Report: .ufo/waves/round-52/w1/Falsify34.md

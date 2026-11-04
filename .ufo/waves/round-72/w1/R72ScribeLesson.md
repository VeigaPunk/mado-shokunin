# R72ScribeLesson — wave findings (seat report)

seat: R72ScribeLesson (leaf member; no subagent dispatch)
date: 2026-11-04
write scope used: `.ufo/waves/round-72/w1/R72ScribeLesson/draft/` (three drafts) plus
this report file. Scratch `/fast/scratch/hyaku/mado-r72/R72ScribeLesson/` created,
unused, deleted. Git strictly read-only everywhere; no pacman, no tool installs (none
needed); no host/config probing.

## Deliverables

1. `w1/R72ScribeLesson/draft/corpus/lessons/round-72.md` — lesson skeleton: header
   (L1 author line, date, base `976684a2…`, instruments `9bcb4fd5…` with both harness
   sha256s, frozen declaration, control sets, measurement receipts), § Outcome and
   boundaries (both frozen predicates, the exact held-leg misses, the declared
   not-claimed set, no-harm obligations), § Gate (admit blocks S444/S445, reject block
   S446, each with URL / access date / located quote ≤25 words / why-it-grounds), §
   Mistakes (four candidate rows; evidence cells filled only where committed bytes
   exist, `<L1 fills>` elsewhere).
2. `w1/R72ScribeLesson/draft/SOURCES-rows.md` — three ready 11-column rows (S444 docs
   mined, S445 code mined, S446 rejected with `REJECTED: …; flip: …`).
3. `w1/R72ScribeLesson/draft/QUALITY-criteria.md` — two candidate criteria (draft
   numbering 116/117) built from this round's own fail lines, each naming its lesson
   and a "shown able to fail" command over committed receipts.

## What the seat verified (commands + outcomes)

1. `sha256sum` over all three fetch triples in `.ufo/waves/round-72/fetch/` —
   byte-identical within each triple: `Doc_library_unittest.rst` →
   `d6522f68c29c8ced8d2d81c91cb41ac739f855e6c0b9831f4a0e5a81f7ae5b86` (107,372 B ×3);
   `Lib_unittest_main.py` →
   `12de7da0fea92dbff8713ebe9904ada6dbd1e0a334d58861c6287ccfc0a261d2` (11,660 B ×3);
   `Doc_builtins_stdtypes.rst` →
   `5a6951b72ecc630a87f45a650fc11c186cfeb4251bedd1ea28f45bcb3116e8e1` (248,201 B ×3).
2. Quotes and anchors located in the pinned bytes: `wasSuccessful()` block at
   unittest.rst:2127-2130 (quote 13 words, :2129-2130); exit derivation at
   main.py:271-275 (quote at :273-274); stdtypes anchors :5299 / :5523 / :5529 all
   confirmed (`Mapping Types --- dict`, `setdefault(key, default=None, /)`,
   `update(**kwargs)`).
3. Commit map (read-only git): `5601e526` = freeze (declaration + both control sets +
   both held-leg baselines); `9bcb4fd5` = the two instruments (declared rev);
   `fd9ea03b` = wave spec/dispatch + both measurement receipts (`TARGET_MET` ×2 at
   `9bcb4fd5`, `C1_RC=0`/`C2_RC=0`). The fetch dir `.ufo/waves/round-72/fetch/` is
   still untracked — see Limits.
4. Held-leg fail lines the criteria cite:
   `grep 'correct_for_held=NO' .ufo/waves/round-72/control-baseline-c1-r72.txt` →
   exactly `bare-failing`, `mismatch-detail` (held 6/8);
   `grep 'base_correct=no' .ufo/waves/round-72/measurement-c2-r72.txt` → exactly
   `failing-summary-exit0`, `green-summary-exit2`, `no-summary-exit0`,
   `garbled-summary-exit0` (base 4/8). Both commands print what the drafts claim.
5. Duplicate checks for draft B over the committed r71 tip: no `unittest` row in the
   registry; none of the three URLs held → no new census W04 expected. S446 is a
   rejection curation at a new real path, not a supersede.

## Cross-check against the L1's in-flight landing (observed; landing uncommitted)

The SOURCES.md **working tree** already carries S444/S445 (`mined`) and S446
(`rejected`, `REJECTED: …; flip: …`) plus the round-72 sweep prose (:852-862), and the
two knowledge entries (`summary-credit-own-detail-r72.md`,
`outcome-verdict-gate-summary-r72.md`) are untracked. My independent drafts agree with
those cells on kind/tier/anchor-digests/quotes/status/flip — no substantive delta
found. If the landed bytes differ from what I read, the L1's bytes win; my drafts were
built from the same fetch receipts, not copied.

## Candidate mistakes coverage (draft A § Mistakes)

The four named candidates: reject row missing (M72-1), the citation misroot — drafted
as the L1-namable slot with the known stdtypes instance filled (M72-2), quote word
count 11-vs-10 (M72-3), results status field absent from r71's w1-results.json (M72-4).
Committed evidence exists for all four (`976684a2` spot-check; `5601e526`/`fd9ea03b`
receipts); round-specific fix cells are `<L1 fills>`.

## Limits / handoff

- The wave was still running at write time (13 seats dispatched; no settled results
  file). No seat votes are bound by any frozen counter, so nothing here depends on the
  missing settlements (the M72-4/criterion-115 discipline applied to this report too).
- The fetch receipts backing the Gate blocks are untracked; they must land with the
  round's landing commit for the three-times-byte-identical claim to be citable from
  committed bytes. `<L1 fills>` cells name every such missing commit.
- No conflicts with sibling seats observed; no committed lane file was edited.

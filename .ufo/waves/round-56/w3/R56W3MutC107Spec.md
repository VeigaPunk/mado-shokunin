# R56W3MutC107Spec — criterion-107 acceptance vectors from the SPEC ALONE

Seat: R56W3MutC107Spec (round 56, wave w3, attempt 2).
Attacked item: the criterion-107 predicate text at
`corpus/QUALITY.md @ 0f3a54361a9824484d0801679ceb1fd8ac7c32e1`, lines 592-607 —
"unique anchor that names the row's upstream file, covers the quoted line, and
stays within that file's length" — attacked by building acceptance vectors for
every clause and proving each clause has discriminating power against plausible
one-defect mutants of a spec-literal oracle. No checker implementation was read
or waited on (this seat converges with the seat building
`quality/check-anchor-cover.py`).

## What I did

1. Read the spec text directly from git objects at the lane tip
   (`git -C <lane> show <rev>:corpus/QUALITY.md`, lines 592-607), plus
   `claims-frozen-v2.md` and `registration-v2.md` (v2 wins over v1; nothing in
   them narrows criterion 107).
2. Built 23 acceptance vectors (`vectors/gen-vectors.py`), one fixture git repo
   per clause, in scratch under `/fast/scratch/hyaku/mado-r56/R56W3MutC107Spec/fixtures/`.
   Each fixture: a minimal `corpus/SOURCES.md` registry (same 11-column shape as
   the lane's), one `corpus/knowledge/entry-c107.md`, and a 200-line pin blob at
   `.ufo/waves/round-56/fetch/ConfigWatcher.cpp` (no trailing newline, so
   `\n`-separated pieces == line count == 200 and the EOF boundary is exact).
   Commits are deterministic (`GIT_AUTHOR_DATE=GIT_COMMITTER_DATE=
   2026-10-30T00:00:00+00:00`, `user.name=ctl`, `user.email=ctl@ctl`);
   regeneration reproduces identical commit SHAs (verified).
3. Hand-authored the expected `ANCHOR_COVER`/`CHECK107` lines and rc per the
   spec text alone (`vectors/expected/<V>.stdout`, `.rc`), plus machine-checkable
   contract files: `.strict` (tokens the checker MUST print) and `.forbid`
   (tokens that MUST NOT appear). Ambiguous fields are excluded from `.strict`
   and listed per vector (see Findings).
4. Wrote a spec-literal oracle (`vectors/reference-check-107.py`) — an internal
   detector, NOT the lane gate — and ran it on every fixture: 23/23 vectors
   reproduce the hand-authored expectations exactly.
5. Ran a 16-mutant battery (`vectors/mutate-check-107.py`,
   `receipts/mutation-battery.txt`): each mutant is one plausible defect in the
   oracle; the detector is the vector suite (strict-token presence,
   forbidden-token absence, rc equality). Baseline on the pristine oracle:
   23/23 pass. Result: **16/16 mutants KILLED**; each clause fires on at least
   one vector; every copy's sha256 was recorded before patch, after patch, and
   after restore (all restorations == pristine
   `350d9182ff3a9b8db5e20b9e53d033af381c972e3d45e10281815187f1a7db2e`).

## Exact commands and decisive output

```
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show \
  0f3a54361a9824484d0801679ceb1fd8ac7c32e1:corpus/QUALITY.md | sed -n '592,607p'
python3 -I .../R56W3MutC107Spec/vectors/gen-vectors.py \
  --fixture-out /fast/scratch/hyaku/mado-r56/R56W3MutC107Spec/fixtures \
  --dest      .../R56W3MutC107Spec
  → vectors=23 fixture_out=... dest=...
for V in V01..V23: oracle --repo fixtures/$V --rev <sha> --work <scratch>
  → oracle-vs-expected exact: pass=23 fail=0
python3 -I .../vectors/mutate-check-107.py --oracle .../reference-check-107.py \
  --fixtures .../fixtures --vectors .../vectors \
  --scratch .../mutants --report .../receipts/mutation-battery.txt
  → BASELINE (pristine master): 23/23 vectors pass
  → SUMMARY: M01..M16 KILLED
    killed_by: V06, V07, V08, V10/V11/V22, V11/V22, V13, V02, V04, V03, V05,
               V20, V19, V16/V17, V17, V13/V14/V15/V21, V11/V13/V22
diff <(cut -f9 vectors.tsv) <(cut -f9 dest2/vectors/vectors.tsv)
  → DETERMINISM: all shas identical
```

## Deliverables (all under .ufo/waves/round-56/w3/R56W3MutC107Spec/)

- `vectors/gen-vectors.py` — deterministic fixture/expectation generator.
- `vectors/vectors.tsv` — per-vector verdict, reason, rc, counts, fixture sha,
  deciding spec sentence.
- `vectors/expected/V01..V23.{stdout,rc,strict,forbid}` — acceptance contract.
- `vectors/fixtures/V01..V23.txt` — text preview of every fixture byte.
- `vectors/reference-check-107.py` — spec-literal oracle (validation tool only,
  not the gate).
- `vectors/mutate-check-107.py` — the bounded behavioural detector / battery.
- `receipts/vectors.txt` — every vector, expected verdict, deciding spec
  sentence, fixture commit, ambiguous fields.
- `receipts/mutation-battery.txt` — mutant, patch, actual outputs, verdict,
  before/after/restore hashes, baseline.

### Vector → clause map

V01 good row OK; V02 malformed-pin ×3 forms; V03 no-registry-row; V04 dup-id;
V05 no-name `?` and `#`; V06 identifier-prefix (`OldConfigWatcher.cpp:` not
counted); V07 hyphen-prefix and slash-prefix count; V08 reversed range
covers nothing; V09 range below L; V10 past-eof; V11 past-eof hits every row
of the pin; V12 `pin <path>` absent → `eof=unchecked`; V13 comma spacing 0/1
space; V14 N=L; V15 M=L; V16 fenced-code and HTML-comment rows out of scope;
V17 no in-scope rows → `rows=0 verdict=FAIL`; V18 third cell not `S`+3 digits
out of scope; V19 `S`+4 digits in scope; V20 NAME trailing `).,;` stripped;
V21 locator == line count inside; V22 locator == line count+1 past-eof;
V23 anchor names a different file entirely.

## Findings — ambiguities the spec text does not resolve

These are spec-text gaps, not checker defects. Each is routed for round-57 /
the checker seat rather than silently fixed here. Where a reading was needed,
the canonical expected line uses it and the field is excluded from `.strict`.

| # | ambiguity | canonical reading | severity |
|---|-----------|-------------------|----------|
| A1 | `line=`/`name=`/`locators=`/`eof=` renderings for rows rejected before that stage (malformed-pin, no-registry-row, dup-id) — spec fixes only the reason | `none` for missing values (`locators=<list|none>` sets precedent) | weakens: vector asserts verdict+reason+counts only |
| A2 | `name=` on a `no-name` row — print the derived NAME (which proves it contains `#`/`?`) or `none` | derived NAME (clause (2) defines NAME unconditionally) | weakens |
| A3 | `locators=` rendering: normalized comma-join vs raw echo — spec never fixes the list rendering | normalized (`N` or `N-M`, comma-joined) | cosmetic unless checker echoes raw anchor text |
| A4 | `eof=checked` on a row whose bound was evaluated and failed (past-eof) — "checked" = evaluated vs = held | evaluated (the check ran) | cosmetic |
| A5 | does an `eof=unchecked` row count toward `covered`? — spec says the bound is "unchecked … listed in the round report, not passed silently" | yes: only the length bound is unverified; cover still holds | **weakens the claim** — the other reading (miss) would fail every unpinned anchor; V12 excludes `covered/miss/verdict` from strict |
| A6 | no reason token named for cover failure (no counted occurrence / locator not covering L) — only 5 reasons are named | no `reason=` emitted | weakens: can't distinguish MISS causes by token alone |
| A7 | multiple counted occurrences of `NAME:` in one anchor cell — which occurrence's locators print, and whether (6)'s "the counted occurrence" binds all of them | all counted occurrences | weakens (untested; fixtures use one occurrence) |
| A8 | reason precedence when a row violates >1 clause | none of my vectors stacks two violations | cosmetic |
| A9 | `pin <path>` blob absent at `<rev>` | treated as setup error (rc 2, empty stdout) | weakens: unspecified |
| A10 | `<file>` grammar inside the malformed-pin test (`[^:\s]+` chosen); `N=0` case | non-empty, no colon/space | cosmetic |
| A11 | which files count as "a knowledge entry" | fixtures place exactly one entry under `corpus/knowledge/` so directory-scan and `--entry` forms agree | cosmetic |
| A12 | how "rows whose first cell is that id" in `corpus/SOURCES.md` are detected | markdown table rows with `S\d{3,}` first cell | cosmetic |

## Defects found

None in the spec-to-expectation chain: all 23 expectations are attainable under
a literal reading (oracle reproduces them exactly) and all 16 plausible
clause-removal mutations are killed by the corresponding vector. Harness
self-defects during the run were fixed and are visible in the receipt history:
a strict-token extraction bug (raw `ANCHOR_COVER:` and bracketed `[reason=...]`
tokens leaked into the set) and a reversed M02 patch — both caught by an
inconclusive baseline before any verdict was recorded. The spec ambiguities
above are the findings; A5 (unchecked-EOF row counting) is the only one that
can flip a `CHECK107` verdict.

## Not verified

- The actual `quality/check-anchor-cover.py` (built by a sibling seat in this
  wave) — my vectors were built without reading it, by instruction. Acceptance
  = `rc` + `.strict` tokens present + `.forbid` tokens absent on each
  regenerated fixture repo at the recorded commit.
- Mutant coverage is bounded to the 16 single-point defects listed; it does not
  prove the vector set complete.

Tooling: nothing installed or updated. Lane files: none modified (read-only
`git show`/`ls-tree` only; all fixtures under scratch; scratch removed on
completion).

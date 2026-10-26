# R2 — digest of the untracked round-46 seat file

Seat `ExecR2Digest`, round 47 / wave w1. Routed item R2 of
`corpus/lessons/round-46-verifier-spotcheck.md:111` (and `:28`): the 3.3 MB untracked
`.ufo/waves/round-46/w1/ExecStofOracle/receipts/out.json.rows.tsv`.

**Status: complete. No lane file was edited, moved or deleted.** The file is still in place; the
L1 performs the deletion and commits the digest line below in its place.

## Deliverables (both inside this seat dir)

- `.ufo/waves/round-47/w1/ExecR2Digest/digest.md` — the digest: identity, per-class row counts, the
  re-derivation of every committed `out.json` field, the loss analysis, consumer caveats, and the
  one-paragraph digest line for the L1 to commit in place of the file.
- `.ufo/waves/round-47/w1/ExecR2Digest/receipts/` — `analysis.txt` (full run), `rederived.json`
  (summary rebuilt from the TSV alone), `derive.py` (the re-derivation script), `repro-sha256.txt`
  (regeneration hashes vs the worktree copies), `verify-locators.sh` + `locators.txt` (7/7 locators
  recomputed by `grep -n`).

## Measured (not typed)

- sha256 `6573f76b5a61c6d0270ae4bfb9b3f37d7e95825c6fbfb13858a78fe54d6d3238`; 3 282 451 bytes;
  59 395 LF lines = 1 header + 59 394 data rows; no CR; UTF-8 (11 rows carry U+00A0); longest line
  108 bytes (line 49142).
- Header: `cat`, `cls`, `ref_line`, `truth_line`, `ref_printed`, `truth_printed`, `text`.
- Untracked (`git status --porcelain` → `??`) and not gitignored (`git check-ignore -v` exit 1).
- Rows per `cls`: `same_value` 55 229, `value_ulp_diff` 2 751, `both_unset` 1 294,
  `ref_refuses_cpp_both_unset` 64, `ref_refuses_cpp_stores` 37, `other` 19 (Σ 59 394), matching
  `out.json.classes.*.n` exactly. Flips: 2 799 line, 2 871 top (`flips.total`), 2 807 print-differs.
- 21 categories, `half3` alone 30 501; 16 are contiguous blocks, `dblround_above/at/below` interleave
  one row each (`gen.py:140-145`, lines 48392-57391).

## Relation to the committed `out.json` (re-derived, not assumed)

The TSV is `diff.py:167`'s per-case `rows` dict serialized at `diff.py:187-191`, with the `kind` field
dropped and nothing filtered or reordered. Rebuilding the summary from the TSV alone reproduces
`cases` 59 394, `categories` 21, all six class counters (`n`/`line_flip`/`top_flip`/`print_differs`),
`flips.total` 2 871 with all five `by_class` keys, `dump_json_breaks` 8 with all eight `nonfinite`
triples, `trim_mismatch_unverified` 4 and `reported_roundtrip_failures` 0 — **every scalar field equal
to the committed `receipts/out.json`** (`946ed60d…`). `ref_top`/`truth_top` are not columns and were
recomputed from `diff.py:123-135`; `kind` is implied by `cls` (`diff.py:139-150` is a bijection on
`kind` × `cpp_set`). The only committed residue the TSV cannot supply is the two `examples` fields
`cpp_bits`/`cpp_reason` (5-tuples in `out.json`, 3-tuples reconstructed).

## Why deleting it is lossless (demonstrated this round)

The TSV uniquely held the identity of the 2 871 flipped rows and the 8 non-finite rows. Regenerating
in scratch from the committed sources — `gen.py` (fixed seed `random.Random(46)`), `stmt.cpp`,
`diff.py`, plus `l1-draft/mado-devices.py` `b229efd0…`, g++ 16.2.1 per `receipts/versions.txt` — and
running `python3 -I diff.py cases.tsv ./stmt <draft>/mado-devices.py out.json` produced
`out.json` `946ed60d…` and `out.json.rows.tsv` `6573f76b…`, **both `cmp`-identical** to the worktree
copies (59 395 lines, 3 282 451 bytes). So the digest line + the committed harness replace the file
with no loss; only the toolchain pin (g++ 16.2.1 / Python 3.14.8) has to keep holding.

## Risks / limits

- Reproducibility was exercised on this host's toolchain only. `[INFERENCE]` the `std::format("{:.2f}")`
  and C99 `strtof` outputs are specified and should not drift, but a different libstdc++ was not run.
- The TSV is *not* strict 7-column text: 8 rows carry literal tabs inside `text` (lines 47945-47949,
  48373-48375; `NF` 8 ×7 and 10 ×1) and 11 rows carry U+00A0 (lines 47718-47928). Consumers must
  `split("\t", 6)`; the digest line states this. Columns 1-6 remain correct under `awk -F'\t'`.
- The digest line asserts the per-row `kind` field is recoverable from `cls`; that is a property of the
  committed `diff.py` class assignment, so it holds only for files produced by this harness revision
  (`b8d5c1a2…`).
- R2's routing asked only for a digest; if the L1 decides to *keep* the file, nothing in this seat
  argues against that — the digest records what it is and that it is regenerable.

## Hygiene

- No process spawned beyond `g++`/`python3`/`sha256sum` in scratch; no git/jj mutation; no pacman, no
  installs (no tool versions changed). No host config, compositor or terminal touched.
- Scratch `/fast/scratch/hyaku/mado-r47/ExecR2Digest/` removed after receipts were copied here.

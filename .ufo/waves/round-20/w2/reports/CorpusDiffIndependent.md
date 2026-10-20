# CorpusDiffIndependent — holds: No baseline finding key disappeared on hash-stable transcripts

## Findings

- Independent scan of the session JSONL corpus found **0 baseline finding keys missing** from the repaired tool on the hash-stable files. The multiset key was exactly `(file, line, class, rule)`; baseline/repaired totals were 1,760/8,042 rows across 5,987 stable files. The script constructs that key and subtracts repaired counts at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w2/CorpusDiffIndependent/corpus_diff_independent.py:145-146,203-220`; the retained result records `lost_row_count: 0` and `lost_rows: []` at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w2/CorpusDiffIndependent/corpus-diff-results.json:30963-30964`.
- Command and output: `python3 -I /tmp/mado-r20w2-CorpusDiffIndependent/corpus_diff_independent.py` → exit 0. It invokes both revision tools as `python3 -I <tool> --scan <paths>` in chunks of at most 32, with failing chunks bisected; the argv and handling are at `corpus_diff_independent.py:69-103`. Output excerpt from the retained JSON: `initial_files=5978`, `final_files=6078`, `additional_pass_files=100`, `scanned_stable_files=5987`, `scan_ok_files={9c54c56:6078,28c6837:6078}`, `baseline_rows=1760`, `repaired_rows=8042`, `lost_row_count=0`; `hash_errors`, `scan_errors`, and `walk_errors` are all empty (`corpus-diff-results.json:2-4,568,30640-30671,30984`). The directory set was unchanged after the additional pass.
- Every input received SHA-256 measurements before and after both scanners. The 91 files whose hashes differed were excluded from the comparison. **All 91 paths and their before/after digests are retained** in `corpus-diff-results.json:4-567`; the full per-file hash audit is at `corpus-diff-results.json:569-30960`. Stable eligibility is enforced at `corpus_diff_independent.py:106-142`.
- Source provenance: copied using `git show` from `/tmp/mado-r20w2-CorpusDiffIndependent` at `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d` and `28c68378eccbd5f227cdc28a62406ff390e3540a`. Tool SHA-256: baseline `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`; repaired `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`.
- Retained artifacts: `../CorpusDiffIndependent/corpus_diff_independent.py` SHA-256 `70d79604590a9aed186a37c27a160dda29cf7f0de27671ed455a71df517e1d31`; `../CorpusDiffIndependent/corpus-diff-results.json` SHA-256 `75ad0213d4044397c3415315593ea2dfc64a53c0aa648ce66dab360f645c7697`.

## Limits

This supports the no-loss result only for the 5,987 files whose SHA-256 stayed unchanged from the pre-scan measurement through the post-scan measurement. The other 91 files were observed to drift and were deliberately skipped; their paths and both hashes are preserved in the result JSON. No session contents were read manually or acted on. Enumeration followed `os.walk(..., followlinks=False)` to match the tripwire’s directory scan behavior.

## Installs

none

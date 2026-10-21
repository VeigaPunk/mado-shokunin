# Round 21 W1 — whole-corpus claim boundary

## Axes and scope

C1 operability (residual repair) and C2 calibration (independent artifact integrity). This report addresses only what a corpus-wide claim can honestly mean; it does not assess detector behavior or provide a measurement.

## Evidence

- `.ufo/waves/round-21/corpus/snapshot/manifest.json` identifies format `mado-committed-fixture-corpus-freeze-v1`, source commit `794aaeb22b4bf35b2482a6779733b69343baff5b`, `file_count: 1356`, and `total_size_bytes: 17478844`. Its inclusion rule is a complete Git-tree census of distinct regular blobs (100644/100755) with the case-sensitive `.jsonl` suffix. Same-content paths remain distinct; local uncommitted files and session state are not eligibility filters. Its provenance explicitly says committed lane transcript fixtures, **not** the private live-session corpus.
- `w1/reports/FreezeCorpus.md` reports the same population and says its freezer completed successfully; it gives manifest SHA-256 `8e1cf206c85563b418630ef1d094559a9522431ff4e077ca1b51f249436a1377`. It records creation under `/tmp/mado-r21-corpus-external/...`. A manifest and `files/` tree are visible at the lane repository's `.ufo/waves/round-21/corpus/snapshot/` path, but I did not verify their byte identity, durability, or commit status against the reported external materialization. Treat the reported digest as the freezer's receipt, not my independent verification.
- `.ufo/waves/round-20/a2/evidence/corpus-diff-9c54c56-vs-a8960de.txt` records a 2026-10-21T06:52:42Z scan of `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin`: `files_at_start=8039`, `stable_files=7889`, `excluded_files=150`. The metric is **stable files**, not 7,889 sessions. `corpus/lessons/round-20-verifier-spotcheck.md` classifies live-session totals as dated observations and records a changed-during-run / new-scan-digest-mismatch exclusion. This is historical evidence about that scan, not a frozen, replayable population.

## Honest claim boundary

Membership completeness is supportable for the finite fixture population: “all qualifying committed `.jsonl` Git-tree paths at source commit `794aaeb…` under the manifest's rule.” A whole-fixture behavior claim would additionally require the before/after tool to consume that exact frozen payload and cover every manifest entry; this seat made no such measurement.

The `stable_files=7889` receipt cannot support a timeless “all 7,889 sessions” claim: it counts files, has 150 exclusions, and describes a mutable live tree at one scan time. No inference about a complete historic session denominator, reproducibility, or private-session detector behavior follows from the fixture manifest. The freeze uses committed fixture blobs rather than copying the private live-session tree; I did not inspect fixture contents and therefore make no separate assertion that every fixture is free of private-derived text.

## Proposed move

Use two explicit, non-interchangeable population identities in C1 evidence and reports: `committed_fixture_tree@794aaeb…` (the manifest-defined complete fixture universe) and `live_session_scan@2026-10-21T06:52:42Z` (a dated historical observation). Scope any full-population C1 claim to the former; retain the 7,889 figure only as `stable_files` history, never as its denominator or as a session-count claim. Before crediting the fixture claim, bind the exact materialized snapshot to the manifest and have the C2 integrity gate recompute actual payload hashes, as the registration requires—not merely trust caller-supplied digest strings. This preserves the complete fixture denominator without copying private live-session material and prevents a fixture result from being generalized to the different session corpus.

## Risks and verification

The manifest population's availability in the repository and equality to the freezer report's `/tmp` output remain unverified; absent a durable, hash-matched payload, membership metadata alone cannot establish replayability. Plain per-file hashes or paths for private session material could also disclose linkable information; do not publish private file contents or path inventories to make the fixture claim stronger. No live session file was opened, copied, or measured by this seat; I only read committed registration, report, manifest, and historical receipt/lesson artifacts. No tests, tool measurements, or installs were performed.

Report: .ufo/waves/round-21/w1/reports/ConnWholeCorpus.md

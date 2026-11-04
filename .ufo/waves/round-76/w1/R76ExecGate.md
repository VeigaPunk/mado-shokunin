# R76ExecGate — no-harm and routed-defect gate

Axes: retained behavior, frozen instrument identity, ledger completeness, registry validity.

## Measured results

Commands, return codes, complete short outputs/full tails, and all blob hashes are retained in `R76ExecGate/gate.txt`; separate receipts retain full merged stdout/stderr. Commands ran from the lane root, with `TMPDIR` and `MADO_SELFTEST_SCRATCH` explicitly set to `/fast/scratch/hyaku/mado-r76/R76ExecGate` and bytecode writes disabled.

| Command / revision | rc | Output lines | Exact tally |
|---|---:|---:|---|
| `bash tools/mado-verify.sh --selftest` | 0 | 1 | `MADO_SELFTEST: 460/460 assertions passed` |
| `check-index.py`, freeze `cb713254ee9926e036e594312fdc61b57825526b` | 0 | 1 | indexed=93/93 missing=0 dangling=0 duplicates=0 coverage=10.0000/10 |
| `check-index.py`, base `c3e0bc5f10b72964d54d18dc9b0706dc308dd1bf` | 0 | 1 | indexed=93/93 missing=0 dangling=0 duplicates=0 coverage=10.0000/10 |
| `check-tool-ledger.py`, freeze | 1 | 4 | population=136 ledger_rows=133 uncovered=3 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MISSED |
| `check-tool-ledger.py`, base | 0 | 1 | population=133 ledger_rows=133 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET |
| `check-axis-scores.py`, freeze | 0 | 4 | checked=3 mismatched=0; navigation 93/93, calibration 86/86, operability 12/12 all MATCH |
| `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | 0 | 49 | final row `mado ok /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md`; duplicate-URL W04 warnings retained |

Output-line counts exclude receipt metadata. The index and ledger measurements read their named immutable revisions, so they do not certify uncommitted round entries/ledger additions. The selftest executes the working instrument; sources validation reads the current registry, whose observed tail includes S456. No live desktop/session/service probes were requested or run.

## Finding

**Integration gap:** the freeze ledger misses exactly three instruments:

- `quality/counters/c1-r76-landing-controls.py`
- `quality/counters/c1-r76-outcome-field.py`
- `quality/counters/c2-r76-shapes.py`

This is the expected pre-integration uncovered count, not a passing ledger certificate. The L1 must integrate ledger rows and rerun against the final committed revision. No production files were changed by this seat.

## Frozen identities

All six requested instruments have identical Git blob IDs at base and freeze (every `git rev-parse REV:PATH` returned 0): `tools/mado-verify.sh`, `quality/landing-counters.sh`, `quality/check-tool-ledger.py`, both `quality/counters/c1-r75-*.py` files, and `quality/counters/c2-r75-shapes.py`. The two other explicitly held checkers, `quality/check-axis-scores.py` and `quality/check-index.py`, also match: **8/8 identical**, no identity mismatch. Exact hashes and commands are retained in both `gate.txt` and `blob-identities.txt`.

## Retained evidence and bounds

Files created: this report plus `R76ExecGate/{gate,blob-identities,selftest,index-freeze,index-base,ledger-freeze,ledger-base,axis-freeze,sources}.txt`. Original declaration, baseline, label derivation and both committed measurement receipts were read, never rewritten. The gate receipts establish the routed no-harm checks, not an independent rerun of C1/C2 counters. No Git mutations, installations, orchestration, or symbol refactors were performed. No LSP tool was exposed; no symbol lookup was needed. Scratch is removed before handoff.

Risks/blockers: no execution blocker; ledger closure remains an L1 integration action. Registry warnings and current-tree timing are preserved rather than treated as frozen evidence. Base/freeze comparisons do not establish last-change commit provenance, which is outside this gate assignment.

Self-evaluation: accuracy 4/5 (working selftest/current registry are explicitly distinguished from frozen reads); completeness 5/5 (all assigned commands, both index revisions, baseline ledger and every requested blob retained); clarity 4/5 (full diagnostics are in linked receipts rather than duplicated here); actionability 5/5 (three exact uncovered paths named); conciseness 4/5 (provenance detail retained for auditability). Overall 4.4/5. Improvement: final L1 gate should bind ledger and registry validation to the integrated revision. Would the user agree? Expected yes: observed passes and the unresolved integration gap are separated.

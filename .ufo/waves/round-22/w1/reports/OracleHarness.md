# Round-22 C1 Oracle Harness Handoff

This implementation is in the parent-provided isolated sparse clone:

- `.ufo/worktrees/r22-oracle/.ufo/waves/round-22/oracle/assemble.py`
- `.ufo/worktrees/r22-oracle/.ufo/waves/round-22/oracle/measure.py`
- `.ufo/worktrees/r22-oracle/.ufo/waves/round-22/w1/reports/OracleHarness.md`

It reads sealed proposals and source artifacts from the original lane at `/home/vgpnk/Projects/shokunin/mado-shokunin` and writes assembly outputs only under the isolated clone's `oracle/` directory. No lane-checkout files were changed after the isolation-boundary correction.

## Materialization contract

The raw source/expectation seal is `.ufo/waves/round-22/truth-seal.json`, SHA-256 `47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4`. It records 106 source files, including 52 C1 proposal JSON files. The assembler verifies the seal digest, every sealed path's byte length and SHA-256, the exact proposal-directory inventory, and the six original round-21 fixtures plus the round-20 pure-data fixture before writing anything.

The normalized population is specified as 50 eligible proposal cases plus seven supplemental originals. The original `CaptureNestedFactory.json` remains byte-pinned and is visibly rejected only for the author typo documented in `CaptureNestedFactory.md`; `CaptureNestedFactoryCorrected.json` supplies the same canonical case ID. `CaptureKwUnknown.addendum.json` is applied to its base case with both source records and digests retained. All proposal fields, source rationale/citations, input order, `cell_reset`, and the mandatory `forbid_commands_any_tier`, `require_signal`, and `accept_exact_want` fields are preserved in the normalized manifest. `language: "py"` is accepted as metadata.

The assembler writes inert eval-call JSONL, copies all seven original inputs byte-for-byte, writes `expected.json`, then pins its actual SHA-256 in `expected.sha256`. The generated expected manifest explicitly says that this normalized digest is produced after the raw truth seal; it does not claim the later JSONL/expected digest was part of the earlier raw seal.

## Measurement interface

```text
python3 -I .ufo/waves/round-22/oracle/measure.py --tool PATH [--case ID]
```

Without `--case`, it scans the whole frozen population. With `--case`, it first validates the entire seal, manifest, proposal inventory, all inputs, and digests, then runs exactly one unique ID. Missing or duplicate IDs refuse with exit 2. Scanner children run sequentially under the round-21 limits: 384 MiB address space and 15 seconds. The JSON result records invocation/scanner argv, tool/producer/runner/population digests, per-child exit and stdout/stderr, parsed output, and pre/post integrity facts.

Exact cases require complete sorted multiset equality over class, command, and evidence, with zero unparsed counters. Uncertain cases accept either a complete `accept_exact_want` result with zero unparsed counters or no observed rows plus the case's `require_signal` condition. `forbid_commands_any_tier` is always checked, including against leads. Cell reset flags must be exact booleans and are emitted one-to-one as eval `arguments.reset`; only transcript metadata/source strings are read, never executed.

The historical round-21 legacy-precision guard remains 166/175 with a required floor of 166; it is recorded as a retained no-harm guard, not reset to a new target. Main owns the whole-175 comparison at the delivered commit.

## Retained evidence

- `FinalBindingReview.md`: `9caedd3d4c521b1a07e4206274e0b3041911caefbf845f85890737e1daef888f`. Its prior bounded probe is retained as historical context only (reported exit 1, four observed findings and one lead); it was not rerun.
- Six immutable round-21 supplemental fixture digests are embedded in `assemble.py` and checked against the raw truth seal.
- Round-20 `CasePureBuiltins--frozenset-closure.jsonl`: `14558b6dd1574253772b30af041169c6fb0eda992d47c7773c342c225472f040`, exact empty expectation, copied unchanged.
- `FinalRemovalReview.md`: `c872a0d4f94ee2e007286cd1ec82b0eb368f63fe35922de9461fb462d4b2522a`; round-21 `final-summary.json`: `e03a2f5a27a1b918e88721b34da38ff872aa8513a70449f37b27119757d9f5d8`.
- `CaptureNestedFactory.md`: `428cc0553c03f20d82d230094fdeeecbff968d59208ebf2eda7783722f987474`.

## Status and handoff

No assembly, scanner, fixture execution, build, test, lint, formatter, or smoke run was performed. No tool was installed. `inputs/`, `expected.json`, and `expected.sha256` have not been materialized; Main runs the assembler after the raw seal and then owns post-integration gates. The harness implementation itself remains unexecuted under the authorship-only wave rule.

# ResourceMap — round-22 w1 scout

Deliverable: `.ufo/waves/round-22/w1/resource-map.json`. Nothing was executed: no scanner, comparator, measurement, generator, freeze, or payload. Only file reads, `sha256sum`, `jq` over committed receipts, and read-only `git`. No tools were installed.

## Observed

- **Tool identity.** `tools/mado-tripwire.py` at HEAD `a963ce6` has sha `46c82902…`. That equals `git show 741122d:tools/mado-tripwire.py` and is the after-tool of every round-21 final (`a6cef89`) receipt. `git diff --stat 741122d HEAD -- tools .ufo/waves/round-21` is empty. The r21 pre-repair tool is `.ufo/waves/round-21/evidence/tool-before.py` (sha `a57d4fe9…`, tracked). No committed copy of the 741122d tool exists outside `tools/`.
- **Resource recipe.**
  - Files: `.ufo/waves/round-21/resource/measure.py` (sha `6d0362e1…`, matches all r21 receipts), with `manifest.json` (`2d479fed…`) and its sidecar, over three committed fixtures (1000/2000/4000 assignments, sha pinned).
  - Caps: the child gets `RLIMIT_AS` 402653184 through `preexec_fn`, a 15 s monotonic deadline followed by a process-group SIGKILL, a 1,000,000-byte capture limit, `wait4` ru_maxrss, and cwd set to `fixtures/`. Children run one at a time, sequentially.
  - Exit code: the runner exits 0 unless a child is never reaped. Per-case scanner exits appear only in the JSON rows.
  - Modes: `cli` runs `tool --scan`. `module-main` uses a `-c` wrapper (sha `233f0c03…`) that calls `main()` and bypasses `run_with_stack`.
  - Argv: r21 used `python3 -I <abs>/.ufo/waves/round-21/resource/measure.py --tool <abs>/tools/mado-tripwire.py --mode cli|module-main`, recorded in the map as reuse argv.
  - r21 final baseline: all six rows clean, exit 0, not timed out. RSS was 29200/31748/38916 KiB in CLI mode and 20292/22852/28904 KiB in module-main mode.
- **1356-fixture comparator.**
  - Files: `.ufo/waves/round-21/corpus/compare.py` (sha `60cef7be…`, which matches the final receipt; the earlier `2ac0f9b` runner `9296ab49…` is gone). It pins `snapshot/manifest.json` sha `8e1cf206…`, 1356 tracked files.
  - Caps: the worker sets `RLIMIT_AS` to 384 MiB and uses `SIGALRM` 15 s per file. Each tool run gets an outer `subprocess.run` timeout of 600 s. The before and after workers run sequentially.
  - Contract: the worker imports the tool and calls `scan_file(path)` on the main thread. The comparison key is (line, tool_call_id, class, rule, command, evidence).
  - Exit is `int(bool(errors))`, so it is **always 1** while the known errors exist. The exit code cannot be the no-harm guard.
  - Argv: r21 used `python3 -I <abs>/compare.py --before-tool <abs>/.ufo/waves/round-21/evidence/tool-before.py --after-tool <abs>/tools/mado-tripwire.py`.
  - Final receipt `corpus-final-a6cef89.json` (sha `57eb2590…`) recorded 836 retained, 31 removed (31 rows), 104 added groups (383 rows), and 108 errors.
- **The 108 error pairs**, all listed in the map with order and array digests:
  - 83 `CouldNotEvaluate` "unknown record shape", plus one each of refused-name `agent.db.jsonl`, JSONDecodeError `malformed.jsonl`, and ValueError `float_inf_field.jsonl`. That makes 86 `CouldNotEvaluate`.
  - 20 `RecursionError`.
  - 1 `TimeoutError` (`huge_bash_cmd.jsonl`).
  - 1 before-only `MemoryError` (`huge_many_stmts.jsonl`, evaluable after the repair).
  - 107 pairs have identical before and after messages, and there are 0 new error flips. The error paths are the same as in the `2ac0f9b` run. I cross-checked the map's 108 paths against the receipt: they match exactly.
- **Delivered-tool baseline.** In r21's final run, the after side (the 741122d tool) had 107 file errors (path digest `53b5c0e3…`) and 1219 findings. Its full after-rows digest is `dc9d36e2…`.

## Reuse recipes (not run)

- **A (r21-identical argv).** This keeps the same entry paths. Diff the new after rows and errors against the r21 final after rows and the 108 pairs, by manifest path and error class.
- **B (delivered baseline).** First freeze `git show 741122d:tools/mado-tripwire.py` to a non-production path before any `tools/` edit, then confirm sha `46c829…`. With identical tools, the baseline error count is 107, not 108.

## Inference / hazards

- [INFERENCE] The r21 outer cap of 402653184 was likely applied with `ulimit -v 393216`, as in the r21 w2 seat reports. The receipts record the value but not how it was applied.
- [INFERENCE] The 20 RecursionErrors come from `scan_file` running at the default recursion limit. `compare.py` bypasses `run_with_stack`, which is the only place that raises the limit to 50000 (`tools/mado-tripwire.py:3258`).
- The TimeoutError pair depends on wall-clock time, and the MemoryError pair depends on the cap. Error messages and `stats.path` embed the absolute checkout root, so running from another worktree changes the strings.
- Do not rerun `gen.py` or `freeze_corpus.py`; both write into the committed recipe directories.

## Unknowns

- The mechanism behind the outer cap.
- Fresh-host reproducibility of the TimeoutError pair and of RSS and elapsed times.
- An itemized adjudication of the 104 added groups (383 rows).
- Main's choice between recipe A and recipe B; recipe B's frozen copy of the 741122d tool does not exist yet.

Confidence: high for paths, shas, caps, argv and the 108-pair list. Those are taken directly from committed files and receipts, and the path list was cross-checked mechanically.

## Pre-seal supplemental closure population (Main request)

Authored separate inert inputs at `.ufo/waves/round-22/w1/resource-closure/`; the existing round-21 assignment recipes remain unchanged. Axes: bounded memory operability, zero-error evaluation, frozen population integrity.

- `visible_factory()` defines and returns a nested `returned_helper()` whose body is only `pass`. Each unrolled factory call is preceded by a distinct unrelated scalar caller binding and stores the returned helper under a distinct binding. No returned helper is invoked; there are no process calls.
- Exact finite population: 512, 1024, 2048 stored helpers and corresponding factory calls. Every case expects clean/exit 0, zero findings, `eval_unparsed:0`, `unparsed_spawns:0`.
- Per-case requirements: one child at a time, 402653184-byte address space cap, 15-second timeout. This is a finite no-harm guard, not an asymptotic complexity claim.
- `manifest.json` SHA256: `6a357933412f838840afbaf63e58bdce016b824f7d0144d2e20d628473d4d99a`; `manifest.sha256` records this digest.
- `fixtures/stored-closures-512.jsonl`: 39652 bytes, SHA256 `b7df4646a6d909a883f570a6b5a9baed529fefa13be864f5ff8680b996ff1270`.
- `fixtures/stored-closures-1024.jsonl`: 79102 bytes, SHA256 `9f12db2330d9f82e9f5666a10b23be4abe5837abe69b301ed68fe18e74ec903d`.
- `fixtures/stored-closures-2048.jsonl`: 158974 bytes, SHA256 `b2e69a25f5e38088d3122068b682876c1bdaabe369a254b38d640b485cd490db`.
- Authorship constructed JSON strings only: fixture source was never executed, imported, scanned, or measured. No tests or resource runs were performed.
- Existing `measure.py.load_manifest()` rejects this new schema/population by design. Main needs a separately owned driver following the existing runner style; do not replace the existing manifest or assignment population.
- Temporal correction: Main now reports the delivered baseline frozen at round-22 `evidence/tool-before.py`; earlier absence statements in this report/resource map describe the initial inspection, not current availability.

Source-trace limitation: no LSP semantic definition/reference evidence was obtained in this seat; source locations above derive from literal source inspection, not semantic-server proof.

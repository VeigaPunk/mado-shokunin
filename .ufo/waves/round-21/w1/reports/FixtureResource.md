# FixtureResource — bounded workload prepared; no tool measurements run

## Axis and scope

- **C1 operability — retained-memory/resource behavior only.** This seat prepared the registered 1,000/2,000/4,000-statement shallow assignment workloads and a bounded sequential measurement harness. It did not assess tool correctness, C2 calibration, or admission.
- Implemented only in `/tmp/mado-r21-resource-external/.ufo/waves/round-21/resource/` plus this exclusive report. Read-only worktree identity: top level `/tmp/mado-r21-resource-external`, branch `mado-r21-resource-external`, HEAD `0644c536224847ecbb0b6c530d55d142e24f86c9`.

## Retained artifacts and evidence

- `/tmp/mado-r21-resource-external/.ufo/waves/round-21/resource/gen.py` deterministically writes exactly three one-record eval JSONL fixtures. Each eval `code` contains only unique scalar assignments (`binding_0000 = 0`, etc.); the fixture source is data and the generator never evaluates it. It also writes `/tmp/mado-r21-resource-external/.ufo/waves/round-21/resource/manifest.json` and the SHA-256 sidecar `/tmp/mado-r21-resource-external/.ufo/waves/round-21/resource/manifest.sha256`.
- Materialization command: `python3 -I /tmp/mado-r21-resource-external/.ufo/waves/round-21/resource/gen.py` (fixture generation only; no scanner or fixture code ran). Generator output recorded:
  - `/tmp/mado-r21-resource-external/.ufo/waves/round-21/resource/fixtures/assignments-1000.jsonl` — SHA-256 `cada424f6584b7085b8c8ade33d872bf42e10d3bcba9402b8ef0a851de0a0acf`
  - `/tmp/mado-r21-resource-external/.ufo/waves/round-21/resource/fixtures/assignments-2000.jsonl` — SHA-256 `e59bb1c2d9306dd8dcbf4c576ec7cd94861131058bff087701d005b71decdb1a`
  - `/tmp/mado-r21-resource-external/.ufo/waves/round-21/resource/fixtures/assignments-4000.jsonl` — SHA-256 `ac11bd54403295b509641d2db30d78a2a6abee9d27ea91e67e93f7aff9639c3c`
  - `/tmp/mado-r21-resource-external/.ufo/waves/round-21/resource/manifest.json` — SHA-256 `2d479fed13cf852c4243c6ffccb48a39b37d32095b5422a8b7913fdbfa3a0ff4`, retained in `/tmp/mado-r21-resource-external/.ufo/waves/round-21/resource/manifest.sha256`.
- The manifest records 1,000, 2,000 and 4,000 statements/unique targets, zero spawn calls, one scan process at a time, the registered 384 MiB address-space cap and 15-second timeout, and expected `verdict=clean`, `exit=0`, `findings=0` for each workload. The harness checks the manifest and fixture hashes before scanning.
- `/tmp/mado-r21-resource-external/.ufo/waves/round-21/resource/measure.py` is source only and has **not** been run. Its required `--mode` labels distinguish:
  - `module-main`: a 384 MiB-capped child imports the selected module with `importlib.util` and invokes `main(["--scan", fixture])`, using the same recorded wrapper for before/after comparisons;
  - `cli`: the ordinary `python -I tool --scan fixture` entrypoint, measured separately.
- Both modes process manifest order sequentially, set child `RLIMIT_AS` to exactly 384 MiB, use a 15-second wall deadline, and collect exit status, stdout/stderr (bounded retained text with full-stream byte counts and hashes), elapsed time, Linux `wait4` `ru_maxrss`, and before/after hashes for tool and fixture. Records also bind the manifest, runner, and module-main wrapper hashes. No `/proc` reads are used.
- Registration evidence: `/tmp/mado-r21-resource-external/.ufo/waves/round-21/registration.md:7` specifies the shallow workload sizes, 384 MiB cap and 15-second bound. Historical motivating evidence: `/tmp/mado-r21-resource-external/.ufo/waves/round-20/a2/review/ReviewRuntimeV3.md:1,22-35,83` records the prior large-shallow-input resource regression and that no unrestricted multi-GiB rerun was attempted.
- The unchanged scanner source defines `STACK_BYTES = 512 * 1024 * 1024` and routes its CLI through `run_with_stack` (`/tmp/mado-r21-resource-external/tools/mado-tripwire.py:2890-2919`). **[INFERENCE]** Under the required 384 MiB `RLIMIT_AS`, the normal CLI mode may fail to create that worker thread even if retained-memory behavior is repaired. The harness records that mode's raw exit/output/RSS rather than relabeling it as quadratic-memory evidence. Keep the cap fixed; the scanner should reduce unnecessary fixed-stack reservation rather than raise the cap. The module-main mode isolates scan memory from this CLI wrapper; it is not claimed to be equivalent to CLI startup.

## Limits

No scanner measurements, CLI/module-main invocations, tests, or fixture execution were performed. Expected clean/zero-findings is a registered semantic expectation, not an observed scanner result. The generator's emitted hashes are recorded above; no independent post-generation fixture audit was run. No tool source was modified, and no `/proc` or host probes were performed.

## Installs

None.

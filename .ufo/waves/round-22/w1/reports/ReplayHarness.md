# ReplayHarness — round 22, wave 1

## Axes

- **Evidence fidelity:** one JSON receipt records the exact fixed command, selected tool digest(s), selected round-21 runner digest, timestamps, exit, and unnormalized stdout/stderr. Invalid UTF-8 is carried through UTF-8 `surrogateescape` and ASCII-escaped JSON.
- **Bounded operation:** only four explicit modes are accepted; each has an outer deadline above the applicable round-21 runner budget. The existing scanner memory/time/capture limits are not edited.
- **Isolation:** paths resolve to regular files within the repository; commands are fixed argv lists, use `python -I`, and receive no stdin. No fixture or payload was run while authoring this artifact.

## Files changed

- `.ufo/waves/round-22/replay.py` — new executable receipt driver.
- `.ufo/waves/round-22/w1/reports/ReplayHarness.md` — this scoped report.

No round-21 runner, fixture, manifest, production source, or other seat's file was changed.

## Behavior

`replay.py --tool PATH --mode MODE` supports:

- `oracle`: invokes round-21 `oracle/measure.py --tool PATH`.
- `resource-api`: invokes round-21 `resource/measure.py --mode module-main --tool PATH`.
- `resource-cli`: invokes round-21 `resource/measure.py --mode cli --tool PATH`.
- `corpus`: requires `--before-tool PATH`, uses `--tool` as the after scanner, and invokes round-21 `corpus/compare.py --before-tool PATH --after-tool PATH`.

`--before-tool` is rejected outside corpus mode. The emitted stdout is one JSON receipt with `argv`, `start`, `end`, `tool_sha256` and post-run digest, optional before-tool digests, `runner_sha256` for the selected round-21 harness, `replay_sha256` for this driver, timeout status, `exit`, raw `stdout`/`stderr`, and setup/spawn errors. On setup failure the receipt records exit 2. On timeout, the process group is killed and the captured process output and return code are retained.

Outer deadlines are 810 seconds for oracle (52 current frozen cases × 15 seconds plus 30 seconds), 75 seconds for resource (three workloads × 15 seconds plus 30 seconds), and 1,230 seconds for corpus (two round-21 600-second worker deadlines plus 30 seconds). These do not alter the existing inner bounds.

## Retained source evidence

- `.ufo/waves/round-21/oracle/measure.py` lines 24–38: 384 MiB scanner address-space cap, 15-second scanner timeout, fixed `python -I` wrapper and scanner invocation. The retained `oracle/expected.json` query returned 52 cases.
- `.ufo/waves/round-21/resource/measure.py` lines 33–41, 57–76, 91–118, 140–273, 276–307: 384 MiB, 15-second and 1,000,000-byte per-stream capture limits; authenticated 1000/2000/4000 workload manifest; `module-main` and `cli` entry paths; sequential execution and raw result fields.
- `.ufo/waves/round-21/corpus/compare.py` lines 38–55 and 62–114: worker cap 384 MiB, per-file 15-second deadline, `--before-tool`/`--after-tool`, 600-second timeout per tool worker, complete removal/relabel/error comparison. The retained corpus manifest query returned 1,356 files.
- `.ufo/waves/round-22/registration.md` lines 11–13: authoring-wave restriction, source-only fixture handling, and existing resource bounds.

These are source observations only. No receipt, detector measurement, scanner execution, fixture execution, test, build, lint, formatter, smoke run, or package installation was performed. No pass/fail result is claimed.

## Risks and unknowns

- Runner behavior and scanner output were not dynamically observed, by design; the first explicit invocation remains the measurement.
- The driver captures full harness stdout/stderr in memory to avoid altering raw outputs; it adds no separate byte cap on the outer receipt. Unexpectedly large harness output could raise parent-memory use.
- LSP availability was not exposed in this session; this standalone new file required no symbol lookup, reference search, or refactor.

No other blocker is known from the inspected command interfaces.
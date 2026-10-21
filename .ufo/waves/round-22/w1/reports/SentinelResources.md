# Sentinel resource-boundary review

Axes: hard process-tree limits and cleanup; bounded output/provenance; fixed-population input integrity; aggregate concurrency across seats.

## Scope and result

Static source/artifact review only. No candidate import, scanner run, detector measurement, fixture execution, child process, build, or test was performed. No production files were changed and no tools were installed.

**Result:** 384 MiB / 15 s is not, by itself, a safe boundary for the existing 1,356-input comparator. The comparator applies 384 MiB to one worker address space, but its 15-second limit is a process-local alarm set after candidate import and reset for every file. Candidate-controlled stdout is also accepted as the result channel and captured without a byte limit. The comparator itself processes before/after sequentially; the per-seat allowance, however, does not impose a global cap across a multi-seat wave.

## High — the comparator's 15-second limit is not a hard whole-run deadline

**Exploit path [INFERENCE; not executed].** The worker imports the selected scanner before installing its SIGALRM handler. Module import is therefore outside the per-file alarm. Once installed, candidate code can replace/cancel the process-local handler. Even when the alarm works as written, it restarts around each of 1,356 `scan_file` calls, not once per corpus run. The parent gives each of two sequential worker processes a 600-second timeout; that is the outer direct-child wait, not process-tree containment.

**Evidence.** In `.ufo/waves/round-21/corpus/compare.py:38-55`, `RLIMIT_AS` precedes import, import precedes `signal.signal`, and `alarm(15)` wraps each individual scan. At `:73-83`, the before/after workers run sequentially through `subprocess.run(..., timeout=600)` without a new session or process-group cleanup. The prior source-only review `.ufo/waves/round-21/w2/reports/CorpusRemoved.md:26-27` also identifies the replaceable/cancellable alarm; no bypass was executed.

**Impact.** Import/scan CPU time may exceed the advertised 15 seconds. A worker may start descendants that the comparator's direct-child timeout does not demonstrate it can terminate. Timeout/error is not proof that the entire process tree has stopped.

**Smallest remediation.** Keep this proposal phase source-only. For a later authorized run, enforce the deadline in a trusted parent and launch the complete worker tree in a killable process group/cgroup; kill and reap that group on timeout. Do not trust a signal handler installed in candidate-controlled code.

## High — untrusted stdout can forge results and exhaust parent memory

**Exploit path [INFERENCE; not executed].** The comparator imports the candidate module in the same process that prints worker result JSON. The parent captures all stdout, parses it into a full list, and retains both full runs. Candidate import/scan code can write candidate-authored rows on the same pipe; it can also produce an arbitrarily large stream. The child address-space cap does not cap the parent's `capture_output` allocation.

**Evidence.** `.ufo/waves/round-21/corpus/compare.py:40-55` uses candidate code and worker protocol output in one process/stdout. At `:76-80,95-113`, the parent captures and parses all output and retains both runs; no byte or row-size cap is present. The prior static report `.ufo/waves/round-21/w2/reports/CorpusRemoved.md:13-21` independently describes the stdout-forgery path and its provenance consequence.

**Impact.** A well-formed row count does not prove the scan ran. The comparator can be made to accept fabricated output or the parent can allocate unbounded memory while collecting it, despite the worker's 384 MiB limit.

**Smallest remediation.** Use a trusted parent-owned result channel separate from candidate stdout. Stream one row at a time with strict per-row and total-output byte limits; reject truncation, malformed records, and incomplete worker completion as errors.

## Medium — one child per seat permits many simultaneous children

**Exploit path [INFERENCE; conditional].** Round-22 registration allows one child at a time **per seat**, not one child globally. The wave record lists 64 spawned seats and a configured maximum of 100 lanes. If every seat uses its allowance, that permits 64 (or at the configured maximum, 100) simultaneous top-level children. At 384 MiB each this is an aggregate virtual-address-space allowance of 24 GiB / 37.5 GiB, respectively; it is not a measured resident-memory prediction. Candidate-created descendants are not constrained by the seat-level count.

**Evidence.** `.ufo/waves/round-22/registration.md:13` states the per-seat rule. `.ufo/waves/round-22/w1-run.json:4-19` records 64 spawned seats and a 100-lane wave maximum. `.ufo/waves/round-21/corpus/compare.py:73-80` serializes before/after workers only within a single comparator invocation; separate seat invocations are not serialized by that loop. Dispatch counts are capacity evidence, not evidence that any seats launched scanner children.

**Impact.** Parallel invocations multiply CPU, I/O, process count, and memory pressure; per-process RLIMIT_AS does not impose a shared process-tree memory or PID budget.

**Smallest remediation.** No scanner children in this wave. For any later authorized full-corpus comparison, use one global permit for resource-heavy jobs. If candidate source is treated as untrusted, also enforce aggregate memory and PID limits on its complete process tree.

## Self-copy and recursion controls

No self-copy path was found in the current pinned freezer. `.ufo/waves/round-21/corpus/freeze_corpus.py:49-75` selects regular `.jsonl` blobs from a fixed Git commit and rejects absolute, empty, `.` and `..` path components. Its `:110-142,185-191` path refuses to overwrite an existing snapshot, reads bytes from the pinned commit, writes to a fresh staging directory, then publishes by rename. The comparator iterates the pinned manifest; it does not recursively walk/copy the output tree. The manifest declares 1,356 rows (`snapshot/manifest.json:1-3`); the prior corpus report records 1,356 distinct path strings. Preserve this invariant—do not replace it with a recursive working-tree copy or include generated output under an enumerated source root.

The scanner itself has a same-helper recursion guard, descent limit 4, and per-cell descent budget 2,000 (`tools/mado-tripwire.py:2164-2170,2233-2235`); shell classification has a depth guard (`:1084-1087`). These parser/traversal controls do not constrain candidate-module import, worker stdout, child-process creation, or process-tree resources.

## Unknowns

- No round-22 candidate bytes or round-22 comparator implementation were run or measured.
- No detector probe, fixture payload, or process child was launched.
- Actual scanner-child concurrency by wave seats is unknown; the 64/100 values describe dispatch capacity only.
- No aggregate RSS, PID, or process-tree behavior is claimed.

Report: .ufo/waves/round-22/w1/reports/SentinelResources.md

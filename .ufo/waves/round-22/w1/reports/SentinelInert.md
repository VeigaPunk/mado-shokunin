# SentinelInert — static harness safety review

## Axes

Payload isolation; private-session exclusion; host/process isolation; receipt provenance. This is a source/artifact review only. No assembler, scanner, fixture, audit command, subprocess, private session, or host probe was invoked.

## Findings

### High, conditional — C1 imports and executes the selected scanner

**Exploit path.** The isolated-clone C1 runner accepts `--tool`, resolves the argument, and checks only that the resolved target is a regular file (`.ufo/worktrees/r22-oracle/.ufo/waves/round-22/oracle/measure.py:813-819`, `:128-131`). Its wrapper imports that path and invokes `exec_module` (`:34-38`). Unlike the main-lane replay wrapper, the direct C1 CLI does not confine the selected scanner path to the repository or an allowlist. Any selected Python file can execute at import with the caller's environment and permissions. The scanner child inherits the environment and is limited by address space and timeout, not a security sandbox (`:655-668`).

**Evidence and impact.** The current `tools/mado-tripwire.py` uses `PyCF_ONLY_AST` for transcript code (`:2101-2114`), so its current source parses payloads rather than executing them. That does not constrain arbitrary `--tool` code or guarantee a future candidate will not evaluate transcript cells. An unintended scanner can read private files/secrets or initiate host/network actions; a candidate regression that executes an inert JSONL cell could do likewise.

**Smallest remediation.** Restrict `--tool` to explicitly approved scanner path(s) and independently sealed hashes; validate the invocation path before resolving symlinks. If candidate bytes or payload execution behavior is adversarial, use a separately authorized unprivileged, no-network sandbox with read-only fixture inputs. Do not treat `-I`, timeout, or `RLIMIT_AS` as isolation.

### Medium, conditional — the separate replay oracle mode retains R21 path risk

**Exploit path.** The main-lane `.ufo/waves/round-22/replay.py` oracle mode invokes `.ufo/waves/round-21/oracle/measure.py` (`:48-52`), whose `ROOT / case['fixture']` path is not containment-checked (`.ufo/waves/round-21/oracle/measure.py:49-60`). `tools/mado-tripwire.py:2575-2589` permits `~/.omp/agent/sessions`. A traversal manifest plus a rewritten adjacent digest sidecar could therefore redirect a historical replay if those files are writable.

**Mitigation found in the new C1 runner.** The isolated-clone R22 `measure.py` requires an `inputs/<case-id>.jsonl` population, rejects dot/dotdot and symlink components, verifies an exact input inventory, and checks the population before and after (`:109-125, 503-540, 849-869`). I found no equivalent static fixture-path escape in that new direct C1 path. Do not use the main-lane R21 replay mode as the R22 C1 entry path.

**Smallest remediation.** If historical replay remains authorized, confine its fixture paths and reject symlink/escape paths as the new runner does; pin its expected manifest independently.

### Medium, conditional — detached scanner descendants escape process-group cleanup

**Exploit path.** The updated C1 runner starts each scanner in its own session, kills its process group on timeout and after normal completion, and records `process_group_cleanup` (`measure.py:656-712`). This closes the same-group leftover case. But `--tool` is arbitrary Python; a selected module can start a descendant in a separate session/process group before returning. That process is outside the scanner PGID, so the group kill may report `empty` while the detached descendant remains. The outer replay wrapper has the same limitation (`.ufo/waves/round-22/replay.py:75-97`).

**Impact.** A deliberately detached child could retain caller privileges after a timeout or successful receipt and continue filesystem or host-probe actions. This is a source-derived path only; no process was started.

**Smallest remediation.** For adversarial scanner code, use a separately authorized OS process-tree boundary that prevents escaping descendants (for example, an appropriately constrained cgroup/PID namespace); process-group cleanup alone is not containment.

### Medium — replay records tool drift without failing closed

**Exploit path.** Main-lane `replay.py:145-169` records tool digests before and after but returns the round-21 runner's status without comparing them; its runner digest is recorded only before launch. A changed tool can therefore accompany exit 0/1. The new R22 C1 measure runner is stronger: it verifies the tool and runner against the materialized manifest before and after and returns exit 2 on post-run integrity errors (`measure.py:467-475, 849-869`).

**Impact.** Replay process status alone is not proof that stable bytes were measured; receipts with differing before/after hashes must not be treated as passing.

**Smallest remediation.** Make replay exit 2 on tool hash mismatch and check an independently sealed runner digest before and after launch.

## Static safety controls and entry paths

- The delivered C1 assembler lives in `.ufo/worktrees/r22-oracle/`; its `ROOT` and output files are beside its own `__file__`, while source artifacts are read from the lane through a symlink/path-checked helper (`assemble.py:12-26, 259-301, 348-559`). It parses proposals as strict JSON and serializes cells to JSONL; it does not execute them.
- The new C1 runner strictly parses fixture JSON, requires one `eval` toolCall per cell, pins input digests, and confines fixture files under `inputs/`. The current parser's AST-only behavior is source evidence, not an OS-level guarantee for an unreviewed candidate.
- **Now:** static reads only. No assembly or execution.
- **C1 later:** use the isolated clone's `assemble.py` only after the raw seal and main authorization, then its `measure.py --tool PATH [--case ID]` only after the scanner source/path is explicitly approved. Avoid main-lane `replay.py --mode oracle` for C1; it calls the historical R21 runner.
- **C2 later:** contract CLI is `python3 -I tools/mado-evidence-audit.py --check BUNDLE --root ROOT` or `--selftest FIXTURE_ROOT`. The implementation was absent at inspection; keep it JSON/digest-only and do not import/run C1.
- **`resume_continuity_v1`:** not applicable to this wave run: `w1-run.json` records `resume=0` and `resumeSends=[]`. No rejection occurred here to test for zero mutation; this says nothing about other resume rejections.

No installs. No checks, assembly, tests, measurements, or execution were run.

Report: `.ufo/waves/round-22/w1/reports/SentinelInert.md`

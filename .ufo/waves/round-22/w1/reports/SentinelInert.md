# SentinelInert — static harness safety review

## Axes

Payload isolation; private-session exclusion; host/process isolation; receipt provenance. This is a source/artifact review only. No subprocess, scanner, fixture, audit command, private session, or host probe was invoked.

## Findings

### High, conditional — `--tool` is executable code, not inert input

**Exploit path.** `.ufo/waves/round-22/replay.py` accepts any regular file resolving inside the repository as `--tool` (`:39-45, 139-152`). In oracle mode it launches the round-21 measurement runner (`:48-52`); that runner imports the selected file with `importlib.util.spec_from_file_location` and `exec_module` (`.ufo/waves/round-21/oracle/measure.py:13-16`). A malicious or unintended in-repository Python file therefore runs at import with the invoking user's environment and filesystem permissions. `-I`, the child timeout, and `RLIMIT_AS` do not remove those permissions or prevent arbitrary top-level code.

**Evidence and impact.** The intended transcript path is AST-only: `tools/mado-tripwire.py:2101-2114` uses `PyCF_ONLY_AST`. That protects inert payload text, not an untrusted scanner module. A hostile `--tool` could read local private files or start host/network actions while the JSONL payload remains unexecuted.

**Smallest remediation.** Before any authorized measurement, accept only the explicitly approved scanner path(s) and verify an independently sealed SHA-256. If the candidate code itself is untrusted, require a separately authorized unprivileged sandbox with no network and read-only fixture inputs; do not label `-I` or resource limits as a sandbox.

### Medium, conditional — the reference oracle path can reach private sessions

**Exploit path.** The round-21 runner reads `expected.json` and uses `ROOT / case['fixture']` without validating containment (`.ufo/waves/round-21/oracle/measure.py:49-60`). `tools/mado-tripwire.py:2575-2589` explicitly permits `~/.omp/agent/sessions`; `discover` then scans JSONL beneath the supplied path (`:2593-2619`). A traversal entry in a writable expected manifest, paired with a rewritten adjacent `expected.sha256`, can direct a later run to private session data.

**Impact.** The scanner may read and classify private transcript content and put command/path fragments into its output. A sidecar hash is not an independent integrity anchor when both files are writable.

**Smallest remediation.** Derive every fixture path from a validated case ID below the sealed `inputs/` directory; reject absolute paths, `.`/`..`, symlink components, and resolved paths outside that root. Pin the expected-manifest digest outside the mutable harness directory. The C2 contract and `audit-clarifications.md:5-8` already specify strict path/symlink checks; I could not confirm the absent C1 harness enforces equivalent rules.

### Medium — replay records tool drift without failing closed

**Exploit path.** `replay.py:145-160` records pre/post `--tool` digests, but `:161-169` returns the underlying runner status without comparing them; it records a runner digest only before launch and does not verify an independently sealed digest. A swapped file can therefore accompany exit 0/1 unless a downstream reader rejects the mismatch.

**Impact.** Consumers can mistake the process status for a result tied to stable, approved bytes. The receipt exposes the mismatch but does not make it a failed integrity verdict.

**Smallest remediation.** Verify exact sealed tool and runner digests before launch, recheck after completion, and force `2` on any mismatch.

### Medium, conditional — per-case timeouts may leave descendants

**Exploit path.** `replay.py:75-97` creates a new process session and kills its group only after the outer aggregate timeout. The nested reference runner uses `subprocess.run(..., timeout=15)` (`.ufo/waves/round-21/oracle/measure.py:28-38`), which does not create or clean a process group. A selected tool that starts a descendant with closed/redirected standard streams can outlive a normal per-case return.

**Impact.** A descendant may continue with the caller's privileges after the receipt, including filesystem or host-probe actions. No such execution was attempted; this is a source-derived threat path.

**Smallest remediation.** Isolate each measurement child in its own session and reap/kill its process group on every exit path, or forbid process creation through a separately authorized sandbox.

## Safe entry paths and limits

- **Now:** static reads of contracts, code, and inert JSON only. This is the only path used in this wave.
- **C2 later:** the contract names `python3 -I tools/mado-evidence-audit.py --check BUNDLE --root ROOT` and `--selftest FIXTURE_ROOT`. The implementation was absent at inspection. Use only after sealing inputs and confirming the audit is strict JSON/digest processing with root confinement, symlink rejection, and the 2 MiB bound; it must not import/run C1.
- **C1/replay later:** run only after main seals proposals and authorizes measurement; restrict the fixture population to sealed `inputs/*.jsonl`, and pin the scanner and runner as above. `replay.py` uses a fixed mode enum and argv (not a shell), `stdin=DEVNULL`, and group-kills on its aggregate timeout, but these do not make an arbitrary `--tool` safe. New `.ufo/waves/round-22/oracle/` and `audit/` harness files were not present at inspection, so their actual path validation and execution behavior remain unknown.
- **`resume_continuity_v1`:** not applicable to this wave run: `w1-run.json` records `resume=0` and `resumeSends=[]`. There is no rejection here to test for zero mutation; this does not establish behavior for any other rejected resume.

**No installs. No checks or execution were run.**

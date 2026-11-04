# R84Sentinel — scoped security/privacy audit

Axes: changed-path coverage; privacy minimization; scratch isolation; evidence precision.

Scope: 13 added/modified paths between the assigned base and frozen revision, extracted read-only into this seat's explicitly created scratch directory. Production changes were reviewed as a diff; unchanged historical material is not a finding. No historical round-56 artifacts, authentication files, raw session dumps, desktop probes, counter executions, git/jj mutations, or tool installations were performed. This is static audit evidence, not a counter pass or integration verdict.

## Findings

### F1 — Medium: live output is truncated, not privacy-redacted

- Evidence: `quality/counters/c2-r84-runbook.py:480-487`, `quality/counters/c2-r84-runbook.py:735-743`; affected rows at `.ufo/waves/round-84/controls/c2-runbook-cases-r84.json:709-710`, `.ufo/waves/round-84/controls/c2-runbook-cases-r84.json:873-874`, `.ufo/waves/round-84/controls/c2-runbook-cases-r84.json:927-928`, `.ufo/waves/round-84/controls/c2-runbook-cases-r84.json:978-979`.
- Exploit/exposure path: the counter sends non-JSON live command stdout through a generic first-100-character formatter into its receipt stream, regardless of match success. Process/bus rows can expose session identifiers; customized action text or failure output can contain personal paths or embedded sensitive text. A shape check does not sanitize the subsequently logged original output.
- Impact: session-identifying or sensitive text can enter persisted/shared measurement receipts. No live value was captured or reproduced by this audit; sensitive action/failure content is a conditional risk, not a demonstrated credential leak.
- Smallest remediation: format all live observations as rc, byte/line counts and typed summary fields; never echo arbitrary stdout. Preserve literal output only for explicitly synthetic fixture rows. Treat this as a retained boundary limitation in the new counter, not a proven regression against an older counter.

### F2 — Low: committed receipt includes an account-identifying absolute path

- Evidence: `.ufo/waves/round-84/receipts/census-start-r84.txt:56`.
- Exposure path: sharing the new census receipt discloses a host account component and workspace location.
- Impact: avoidable identifying host metadata in an otherwise aggregate census receipt; no authentication material was observed at this location.
- Smallest remediation: emit a lane-relative source path in the census receipt. No identifying value is reproduced here.

### F3 — Low: timeout handling is not process-tree containment

- Evidence: `quality/counters/c1-r84-namespaces.py:190-196`, `quality/counters/c1-r84-namespaces.py:543-545`; `quality/counters/c2-r84-runbook.py:223-231`, `quality/counters/c2-r84-runbook.py:788-790`.
- Failure path: C2 launches shell pipelines, but subprocess timeout handling has no new session/process-group termination. Python's direct-child timeout cleanup does not guarantee termination of shell descendants. Recursive scratch deletion is not process cleanup.
- Impact: [INFERENCE] a hung descendant can outlive its counter and retain inherited desktop access or pipes; complete cleanup and a strict wall-clock bound are not established. No hanging process or offensive payload was launched.
- Smallest remediation: start subprocesses in their own session, terminate/kill and reap the process group on timeout before deleting scratch. This is a static limitation in the new counter paths, not a reproduced incident.

## Other boundary evidence

- C1 builds argv lists, not interpolated shell commands, and writes fixed fixture filenames under a generated private work directory: `quality/counters/c1-r84-namespaces.py:241-275`, `quality/counters/c1-r84-namespaces.py:300-316`, `quality/counters/c1-r84-namespaces.py:447-454`. The new parser refuses duplicate allocation/declaration identities before composition: `tools/mado-barfoot.py:439-454`, `tools/mado-barfoot.py:780-791`.
- C2 intentionally executes reviewed control commands with host desktop access, not inside a sandbox. Controls, revisions, inherited PATH, and fixture paths are trusted operator inputs. Working-tree tool/fixture byte checks and documented command bindings are present: `quality/counters/c2-r84-runbook.py:696-729`. Frozen shell cases all use exactly the three-element shell/-c/command layout. No unexpected shell-input interpolation was found in those frozen cases. This does not authorize untrusted replacement controls.
- Environment exposure is narrowed, not eliminated; C2 retains desktop/user context and PATH: `quality/counters/c2-r84-runbook.py:184-222`. Generated work directories use `mkdtemp`, and TMPDIR points inside scratch: `quality/counters/c2-r84-runbook.py:195`, `quality/counters/c2-r84-runbook.py:661-670`. Parent-path symlink containment is not established; scratch parents must remain trusted.
- Both new shell fixtures contain only fixed synthetic producer text, exit status and local pipeline plumbing; no desktop read, file capture, config/service mutation, screenshot or input capture: `.ufo/waves/round-84/fixtures/failing-producer.sh:1-3`, `.ufo/waves/round-84/fixtures/pipefail-guard.sh:1-7`.
- Parsed both complete control files: 61 C1 cases and 33 C2 cases. C1 uses two monitor-name values and one repeated fixture-PID value; C2 samples include constructed action labels and synthetic bus examples. These support synthetic-fixture use, not live-state provenance. No credential-shaped literal was detected in scoped additions; this is not proof that arbitrary secrets cannot be present.
- Before-state and population receipts contain bounded summaries, not raw desktop dumps: `.ufo/waves/round-84/receipts/control-c1-r84-at-base.txt:1-64`, `.ufo/waves/round-84/receipts/control-c2-r84-unguarded.txt:1-4`, `.ufo/waves/round-84/receipts/population-before-scoring-r84.txt:1-3`. Their recorded outcomes were inspected, not rerun or independently authenticated.
- No changed/new path implements resume_continuity_v1; that contract is outside this assigned surface. No unrelated runtime was invoked.

## Limitations and handoff

No production remediation was authorized or applied. Main should decide privacy disposition before publishing live C2 receipts and the census receipt; any process-cleanup testing must remain in isolated synthetic scratch with no live desktop payloads. No build/lint/test or counter pass is claimed. Tool installs/updates: none. Scratch copies are removed before seat completion; this report is the only retained seat artifact.

Self-evaluation: accuracy 4/5 (static risks explicitly separated from reproduced findings); completeness 4/5 (all 13 scoped paths inspected, no live execution authorized); clarity 4/5 (three severity-ranked findings); actionability 4/5 (smallest remediation per finding, implementation out of scope); conciseness 4/5 (boundary notes retained to prevent an overbroad security-pass interpretation). Improvement: independently exercise synthetic process-group cleanup only under a separately authorized probe.

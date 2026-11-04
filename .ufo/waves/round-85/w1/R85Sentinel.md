# R85Sentinel — scoped security and boundary review

Axes: confidentiality, read-only execution, scratch containment, bounded termination, refusal-output integrity.

Scope: declaration and freeze revision `3905311c75a39c5710413105865c0a1a7dd0116a`, both round-85 counters and controls, three new producer fixtures, the tool's error formatting, and the five receipts present during review. No remediation edits, runtime dispatch, commits, installs, or full scoring battery. The counter/controls/SKILL working tree was concurrently changing; frozen-versus-working differences were inspected and findings below concern unchanged boundary code. C2 line references to its final exception handler distinguish frozen and observed working-tree numbering.

## Findings

### F1 — Low: durable receipts already contain host-private path metadata

Evidence:
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-85/receipts/census-start-r85.txt:2,58` stores absolute home/repository paths, including the fleet root outside the lane.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-85/receipts/harm-watch-r85.txt:51,72-73` stores the seat's absolute scratch path as a `TMPDIR=` command prefix and the fleet cwd.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-85/receipts/misroot-sweep-r85.txt:4-5,8-25` stores the fleet-root location and internal working-tree filenames.

Exploit path: someone receiving the durable wave receipts obtains host username/path layout and internal workspace names without needing access to the live producer output. Impact is metadata disclosure, not an observed credential compromise. This violates the literal no-private-path/no-environment-value requirement; it does not show that the C2 live-row formatter leaks payloads.

Smallest remediation: publish lane-relative paths and symbolic scratch/environment labels in receipts; retain exact host-specific execution context only in non-published scratch evidence. Do not silently rewrite historical execution claims.

### F2 — Medium: setup failures escape the sanitized output boundary and exit as ordinary failures

Evidence:
- `/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r85-identity-causes.py:486,504-505` calls filesystem/JSON operations directly, but `:575-577` catches only its custom `Setup` exception.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r85-status-classes.py:708,718-719` has the same filesystem/JSON pattern; its frozen `:841-843` (observed working tree `:850-852`) catches only `Setup`.
- Exercised C1: literal scratch root `/` produced a stage=setup refusal and exit 2. An existing regular file as scratch root produced `FileExistsError`, a Python traceback containing the absolute scratch filename, and exit 1. A missing controls file produced `FileNotFoundError`, an absolute source-file/controls-path traceback, and exit 1. These were setup probes, not population scores.

Exploit path: an invalid or inaccessible caller-selected input/scratch path causes stderr to bypass the summarized-row formatter. A gate that durably retains both streams retains local filenames and interpreter/source locations. The stated exit map also loses the distinction between setup refusal (2) and target miss (1); no fabricated TARGET_MET line was observed. The corresponding C2 behavior is inferred from the same uncaught operations, not independently executed.

Smallest remediation: translate expected filesystem/JSON input failures to a sanitized stage=setup refusal with exit 2, avoiding raw exception text/path values in durable output. Preserve unexpected programming exceptions as failures rather than masking them as successful verdicts.

### F3 — Low: scratch guard checks only the final path component

Evidence:
- `/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r85-identity-causes.py:482-489` and `/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r85-status-classes.py:704-711` compare the raw argument to `/`, call `islink()` only on that spelling, then create/use it.

Exploit path [INFERENCE, not operationalized]: a root expressed through a symlinked ancestor passes the leaf `islink()` check; generated files land in the ancestor's target. Equivalent spellings of `/` also bypass the literal root comparison, subject to filesystem permissions. Impact is a weaker containment guarantee than 'no symlinked scratch root'; this is not evidence of an actual outside-scratch write by the frozen cases. Caller control of the path is required, and ordinary filesystem permissions still apply.

Smallest remediation: normalize the root before root-directory rejection; reject symlinked components (or explicitly require lexical and resolved roots to match), and keep creation anchored to a trusted directory descriptor if concurrent path replacement is in scope.

Additional scratch detail: `/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r85-identity-causes.py:216,452-453` sets child `TMPDIR` to cwd even for revision resolution, whose cwd is the measured repository. No write by `git rev-parse` was observed or is implied, but the child environment is not universally scratch-pinned. Pass the generation root separately for TMPDIR. C2 pins ordinary runner children to its generated root at `:212,711-713`.

## Required checks without findings

### (a) Live-row payload handling

No credential material, session URL, or live compositor/D-Bus environment value was found in the reviewed receipts or frozen control data. This is a bounded inspection, not a proof that arbitrary future inputs cannot disclose data.

`/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r85-status-classes.py:528-530,795-798` formats live observations only as `rc` and UTF-8 stdout byte count, alongside fixed case metadata and match status; stderr is captured but not emitted on this normal path. The retained pipeline-control receipt at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-85/receipts/control-c2-r85-unguarded.txt:4-9` likewise contains counts/statuses, not producer payloads. C1 is fixture-only: its `:528-530` prints selected parsed result fields, not raw stdout/stderr. Consequently, 'both counters print only rc and byte counts' is not literally accurate for C1, but C1 does not print live session captures.

C2's environment allowlist at `:204-212` includes session variables needed by its read verbs; these do not appear in its ordinary observation formatter. F1 and F2 limit the broader durable-receipt confidentiality claim.

### (b) Frozen commands and fixture host effects

No mutating host verb was found in the frozen case commands. C2's 36 rows consist of Hyprland queries, `makoctl mode`, Omarchy current-theme/version/keybindings printing, process queries, `systemctl --user is-active`, D-Bus list/introspect/get-property, lane-tool refusal joins, and contained producer demonstrations. Pipeline filters only transform stdout. C1's `:335-355` builds argv lists for the extracted lane tool with generated fixture inputs; it does not interpolate fixture text into a shell command. Its git operations are `show`/`rev-parse`.

The three new scripts have no file writes, session calls, network calls, or host configuration mutations:
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-85/fixtures/status-ok.sh:3-4`: fixed printf, exit 0.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-85/fixtures/status-exit7.sh:3-4`: fixed printf, exit 7.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-85/fixtures/status-sigpipe.sh:4`: finite awk BEGIN loop producing stdout only.

This is intrinsic read-only behavior of the inspected scripts, not an OS sandbox: inherited executable lookup and normal user filesystem access remain available. No offensive fixture or substituted executable was run.

### (c) Ordinary scratch writes

No executable hardcoded `/tmp` output path was found in either counter or the three new scripts. C1 generated declarations/tool copies/mutants and C2 mutant files are placed beneath their generated scratch directories and removed in `finally`. The lane tool's only discovered write is its selftest temporary fixture; the counter supplies TMPDIR for that invocation. F3 records the weaker root-validation guarantee.

### (d) Fixture pipe boundedness

No unbounded loop or pipe-hang path was found in the three frozen fixtures themselves. The first two outputs are fixed at 15 and 18 bytes. The third is capped at 20,000 lines (608,890 ASCII bytes if fully consumed); its frozen downstream reader is `head -n 1`, whose retained receipt reports 27 output bytes and guarded rc 141. No fixture output is persisted by the live-row formatter.

`/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r85-status-classes.py:201,242-248` applies 120-second subprocess timeouts; mutant-driver invocations use 600 seconds. These are direct-child timeouts, not process-group cleanup guarantees. The supplied finite fixtures do not require an indefinitely surviving descendant. The separate git blob reader at `:253-256` has no timeout, so this review does not certify a global gate wall-clock bound. No timeout/descendant fault-injection run was performed.

### (e) New cause tag

No newly introduced disclosure source was found in the cause tag. `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-barfoot.py:1667-1670` appends the exception's code-assigned cause token; the inspected refusal sites use literal vocabulary members, not environment or file content as the cause. The new formatter does not read session values.

Important distinction: the *whole* error line is not cause-only. Its `:1719,1722` still prints the existing exception message, which can contain declaration names (`:807-825`) or caller input paths (`:175-180`). Therefore the incremental change is token-only, but it would be false to certify the full CLI error line as sanitized. C1 consumes these errors in memory and omits their messages from case receipts; direct callers must not persist arbitrary full error text under the stronger confidentiality requirement.

## Evidence and limits

Actually exercised: the three C1 setup-path probes described in F2; read-only file/code/receipt inspection and frozen-versus-working diff. Existing receipts were inspected, not re-executed or independently certified. No complete C1/C2 score, live runbook replay, hostile command substitution, symlink escape, or process-tree timeout probe was run by this seat. No tools were installed. Only this report is a durable seat-owned change; scratch is removed before submission.

Self-evaluation: accuracy 4/5 (static findings clearly distinguished from exercised probes); completeness 4/5 (all five assigned checks covered, no global timeout proof); clarity 4/5 (normal-output and error-output guarantees separated); actionability 4/5 (minimal corrections named, no remediation authority); conciseness 4/5 (line-level evidence requires detail). Overall 4.0/5. Main improvement: isolated non-host fault-injection would strengthen root/descendant guarantees, but was not performed during this scoped trial.

Report: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-85/w1/R85Sentinel.md

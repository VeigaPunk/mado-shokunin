# SentinelToolSafety — round 17 wave 2

## Scope and axes

Reviewed only `tools/mado-tripwire.py` at lane HEAD `988b858bd6049bc709807534fd725c05264f7e60`; SHA-256 `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

Axes: **non-execution**, **path confinement**, **bounded resource use**, **secret-safe diagnostics**. Review plus bounded synthetic-input experiments; no remediation scope, so implementation unchanged.

**Result:** three concrete weaknesses: the selftest reader bypasses path refusal and permits suite-directory escape; small malformed shell strings amplify CPU work; output redaction does not cover errors or other attacker-controlled fields. Code-execution attack failed. Direct scan of a final-component symlink or `agent.db` was refused. No catastrophic SECRET_PATTERNS ReDoS established.

All fixtures are under `/tmp/mado-r17-sentinel-4wgauk5d`. All database-shaped content there is synthetic. No actual agent database, credential/auth/oauth file, or transcript was opened. No prohibited host binary was executed: names such as `systemctl` and `sudo` below occur only as transcript text. Installs: **none**. No commits, git mutation, or delegation.

## 1. Medium — selftest follows a symlink to a refused database name and reads outside its suite directory

### Exploit path

An operator runs `--selftest DIR` on an untrusted fixture directory. `DIR/expected.json` is a symlink to an arbitrary readable file. Unlike scan inputs, the spec is opened without `refuse_path`. If it contains a valid spec, its `cases[].args` may also escape the directory using `..` or an absolute path.

### Evidence

Source anchors:

- `tools/mado-tripwire.py:580-592`: scan path checks reject final-component symlinks and database names.
- `tools/mado-tripwire.py:728-731`: selftest instead directly opens `os.path.join(directory, "expected.json")`.
- `tools/mado-tripwire.py:743`: case paths are formed by `os.path.join(directory, a)` without confinement; an absolute second argument replaces the directory.
- `tools/mado-tripwire.py:751`: the child invocation is an argument vector, not a shell command; this is a file-access issue, not demonstrated code execution.

Synthetic proof layout:

```text
/tmp/mado-r17-sentinel-4wgauk5d/
  agent.db                         # synthetic JSON selftest spec
  suite/expected.json -> ../agent.db
  outside/external.jsonl           # synthetic transcript, systemctl status
```

The synthetic `agent.db` contains:

```json
{"schema":"mado-tripwire-selftest-v1","cases":[{"name":"outside-relative","args":["../outside/external.jsonl"],"want_exit":1,"want_findings":[{"class":"live_probe","rule":"systemctl:status","line":1}]}]}
```

Observed commands/results (script invocation prefix in every experiment is `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`):

```text
--scan /tmp/mado-r17-sentinel-4wgauk5d/agent.db
exit 2; error: refused file name: /tmp/mado-r17-sentinel-4wgauk5d/agent.db

--selftest /tmp/mado-r17-sentinel-4wgauk5d/suite
exit 0
CASE outside-relative ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 1/1 passed failed=[]
```

Thus the same synthetic database-named file rejected by `--scan` is successfully followed/read by `--selftest`, and its escaped case path is scanned. A real SQLite database would normally fail JSON parsing, but the bytes would already have been opened/read; no real database access was attempted here.

Additional path probe: `scan-root/direct-link.jsonl -> ../outside/external.jsonl` was refused with exit 2, while `--scan .../scan-root/parent-link/external.jsonl`, with `parent-link -> ../outside`, returned exit 1 and a `systemctl:status` finding. `lstat` checks only the leaf; ancestor symlinks are followed. This demonstrates resolution behavior, not that ordinary directory discovery follows symlink directories: `os.walk(..., followlinks=False)` explicitly does not.

### Impact

The apparent refusal policy is not uniform across CLI modes. Untrusted selftest directories can cause reads outside the named directory, including a target that scan mode explicitly forbids. The experiment does not establish disclosure of arbitrary raw file bytes: selftest parses JSON and ordinarily emits only a malformed-spec classification for non-JSON input.

### Smallest remediation

Apply the path-refusal policy to the selftest directory/spec before reading; reject spec symlinks and prohibited resolved targets. Require every case argument's canonical path to stay within the canonical suite directory, rejecting absolute paths and traversal. If symlink-race resistance is part of the guarantee, use descriptor-based opening with no-follow checks rather than separate `lstat`/`open` operations. The race at `scan_file:624-629` is a static observation only; no race against private files was attempted.

## 2. Medium — unmatched multiline quotes cause CPU denial of service

### Exploit path

A transcript contains one bash tool call whose command starts an unterminated quote and contains many subsequent short lines. `logical_lines` reparses the entire accumulated prefix with `shlex.split` after every appended line. The work grows approximately quadratically even though the transcript itself remains small.

### Evidence

- `tools/mado-tripwire.py:124-132`: complete-prefix reparse inside the accumulation loop.
- `tools/mado-tripwire.py:339`: every shell command reaches this path.
- `tools/mado-tripwire.py:628-629`: the complete input file is also read without a size limit.

Exact command-generation recipe used in a normal assistant/bash JSONL record:

```python
command = "echo '\n" + ("x" * 20 + "\n") * n
```

Sequential measurements, with a three-second external subprocess timeout:

| n | JSONL bytes | Observed elapsed | Outcome |
|---:|---:|---:|---|
| 250 | 5,699 | 0.1020 s | exit 0 |
| 500 | 11,199 | 0.3574 s | exit 0 |
| 1,000 | 22,199 | 1.4803 s | exit 0 |
| 2,000 | 44,199 | 3.0038 s | killed/reaped by test harness timeout |

Files are `quote-scale-{250,500,1000,2000}.jsonl` under the scratch directory. An earlier 132,221-byte `unclosed-quote.jsonl` also exceeded the three-second timeout. These establish expensive bounded-input processing, **not an infinite loop**. No large or unbounded stress test was run.

A one-million-character shell argument (`regex-long.jsonl`, 1,000,202 bytes) likewise exceeded three seconds, but that result does **not** isolate redaction regex behavior: shell tokenization precedes redaction. It is not evidence of SECRET_PATTERNS ReDoS.

### Impact

A single hostile tool-call record can delay or prevent a timely verdict. `--scan` has no internal time/work limit; the selftest child has a 120-second timeout rather than a parser-level bound. Resource consumption is attacker-controlled even without executing transcript contents.

### Smallest remediation

Bound command/record length and logical-line accumulation, returning could-not-evaluate when exceeded; avoid reparsing the full prefix for each added line, preferably tracking quote state in one pass. Do not merely truncate commands and report clean.

### Deep-recursion control

`sudo-depth.jsonl` contains `("sudo " * 1100) + "echo harmless"`. It returned exit 2 in 0.0387 s with `error: internal RecursionError`, no traceback. `classify_segment:368-391` recursively processes elevation prefixes without applying `classify_shell`'s depth check at `334-337`; `systemd-run:398-406` has a similar direct recursion edge. This is a depth-budget inconsistency, but the exercised case **failed closed promptly**, not a demonstrated hang. A 10,000-term Python expression in `eval-deep.jsonl` returned exit 0 in 0.0481 s; that attack failed to hang the scanner. A shared recursion budget across shell/segment/eval would make failure predictable; eval entry points currently reset the shell budget (`364`, `420`, `508`, `514`).

## 3. Medium — secrets survive in error messages and non-command output fields

### Exploit path

A supplied pathname contains a secret, or transcript fields copied into a finding contain one. Only `finding.command` is passed through `redact`; errors, rules, IDs, timestamps and file paths are not. Logging/sharing the verdict can therefore expose a token even when the displayed command has been redacted.

### Evidence

- `tools/mado-tripwire.py:584-592,631,646,648`: errors interpolate raw input paths.
- `tools/mado-tripwire.py:712-716`: the raw exception string is emitted.
- `tools/mado-tripwire.py:682-687`: only the command is redacted; other finding fields are copied.
- `tools/mado-tripwire.py:89-105`: the synthetic token below matches the existing 32-or-more-character secret pattern.

Synthetic token: `CANARY_SECRET_TOKEN_0123456789_ABCDEFG` (not a real credential).

Observed:

```text
--scan /tmp/mado-r17-sentinel-4wgauk5d/missing-CANARY_SECRET_TOKEN_0123456789_ABCDEFG.jsonl
exit 2
error: unreadable path: /tmp/mado-r17-sentinel-4wgauk5d/missing-CANARY_SECRET_TOKEN_0123456789_ABCDEFG.jsonl
```

`secret-long-metadata.jsonl` uses this token as the verb in a synthetic `systemctl` command, tool-call ID and timestamp. Its exit-1 finding contained:

```json
{"command":"systemctl <redacted>","rule":"systemctl:CANARY_SECRET_TOKEN_0123456789_ABCDEFG","tool_call_id":"CANARY_SECRET_TOKEN_0123456789_ABCDEFG","timestamp":"CANARY_SECRET_TOKEN_0123456789_ABCDEFG"}
```

Thus a token removed from `command` still appears verbatim elsewhere in the same finding. Shorter token shapes also survive in command text; the existing regexes are heuristics, not comprehensive secret detection.

Control: `invalid-secret.jsonl` contains the synthetic secret in malformed JSON. It returned exit 2 with only `invalid line (JSONDecodeError)` and the path/line; its secret contents did **not** appear in output. The top-level internal error for the recursion probe likewise printed only the exception class.

### Impact

Secrets already present in supplied paths or records can cross into downstream diagnostic logs/reports. No demonstrated access to secrets not contained in supplied input. JSON escaping prevents raw terminal control characters in normal scan JSON output, but does not provide secret redaction.

### Smallest remediation

Use fixed diagnostic codes plus sanitized/bounded path labels; redact all emitted attacker-controlled strings, not only command text. Keep stable classification rules separate from arbitrary user-supplied verbs. Treat IDs/timestamps as untrusted strings or omit unsupported shapes; document the residual limits of heuristic redaction.

## Attacks that failed / non-findings

- **Code execution:** `execution-bash.jsonl` included synthetic `touch` commands, command substitutions, backticks and `bash -c`; `execution-eval.jsonl` included a `pathlib.write_text` expression and `os.system`. Both scans returned exit 0 and the target scratch marker `MUST_NOT_EXIST` remained absent. The parser compiles with `ast.PyCF_ONLY_AST` (`521-523`), not Python execution. Selftest launches only the same script through a fixed interpreter argument vector (`743`, `751`). No input-driven code execution found on this surface.
- **Direct scan symlink/database:** both were rejected with exit 2, as recorded above. The successful bypass is specifically the unchecked selftest spec reader (plus the described ancestor-resolution behavior), not a claim that `--scan` blindly follows a final symlink.
- **SECRET_PATTERNS ReDoS:** no catastrophic-backtracking counterexample demonstrated. The three patterns (`89-93`) do not visibly contain nested overlapping repetitions; the successful CPU attack is the repeated shell parsing path. This is a bounded review result, not a general linear-time proof for all regexes or Python internals.
- **Raw invalid-record disclosure:** the malformed-JSON canary did not leak. Generic internal-error output did not expose a traceback or command contents.
- **Process cleanup:** successful selftests completed their fixed child process. The synthetic timeout cases were killed/reaped by `subprocess.run(..., timeout=3)` in the test harness; no daemon/background process was intentionally started. There was no process/device/compositor probe.

Only this report was written in the lane. Scratch proofs remain under the stated `/tmp` directory; implementation and repository fixtures were not changed.

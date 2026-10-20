# MutateTripwire3 — third-slice mutation probe
**Result: 10 independent one-line mutants; 4 killed, 6 survived, 0 inconclusive.**
These are coverage findings against the existing three selftest suites, not a claim that the pristine scanner currently has the injected defects. The attack did not falsify the literal pristine suite totals: all pristine and restored runs passed 9/9, 16/16 and 33/33. It did show that those totals can remain green after six demonstrable output-contract regressions. No acceptance, integration or shipping decision is made here.
## Scope, axes and bounded detector
- Target: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`; observed length **818 lines**. Floor cutpoints at 272 and 545 give thirds 1–272, 273–545, **546–818**. All changed lines were 551–719, inside third 3.
- Isolated copies: `/tmp/MadoR17-MutateTripwire3.wvd7me0k/M301.py` through `M310.py`; each had exactly one mutation. No lane source, fixture, sibling file, or selftest oracle was modified.
- Axes: kill sensitivity; survivor specificity (a concrete changed output, not an equivalent mutant); bounded safety; exact byte restoration.
- Each copy ran the same `core`, `compound`, and `hardening` suites on pristine, mutated, and restored bytes: **90 selftest invocations / 1,740 fixture checks** total. Top-level concurrency was capped at six; each selftest invocation had a 45-second outer deadline. No timeout occurred. All stderr was empty.
- Six additional explanatory witnesses were scanned in each of the three states (18 scans, 10-second deadlines); these were not added to or substituted for the requested selftest detector. A scanner exit 1 on these finding-bearing witnesses is expected, not a failed baseline.
- `run_selftest` derives its child scanner path from its own `__file__` at `tools/mado-tripwire.py:739-743`; the calls below therefore exercised the copied scanner, not the lane script accidentally.
```text
python3 -I /tmp/MadoR17-MutateTripwire3.wvd7me0k/<MUTANT>.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core
python3 -I /tmp/MadoR17-MutateTripwire3.wvd7me0k/<MUTANT>.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound
python3 -I /tmp/MadoR17-MutateTripwire3.wvd7me0k/<MUTANT>.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening
```
All exact argv, return codes, stdout and stderr are retained in the inline raw receipt at the end.
## Mutation results
Cells show passed/total and the **selftest process exit**, not the nested scanner exit.
| Mutant | Source anchor | Injected defect | Core | Compound | Hardening | Verdict |
|---|---|---|---|---|---|---|
| M301 | `tools/mado-tripwire.py:551` | Read the AST dictionary key instead of its command value | 9/9; exit 0 | 16/16; exit 0 | 32/33; exit 1 | **killed** |
| M302 | `tools/mado-tripwire.py:646` | Skip invalid JSON rather than fail closed | 8/9; exit 1 | 16/16; exit 0 | 33/33; exit 0 | **killed** |
| M303 | `tools/mado-tripwire.py:678` | Deduplicate findings by class, dropping distinct rules | 8/9; exit 1 | 12/16; exit 1 | 28/33; exit 1 | **killed** |
| M304 | `tools/mado-tripwire.py:700` | Ignore permit membership when computing unpermitted | 8/9; exit 1 | 13/16; exit 1 | 33/33; exit 0 | **killed** |
| M305 | `tools/mado-tripwire.py:684` | Take tool_call_id from the outer message instead of the toolCall | 9/9; exit 0 | 16/16; exit 0 | 33/33; exit 0 | **survived** |
| M306 | `tools/mado-tripwire.py:632` | Hash the pathname instead of the transcript bytes | 9/9; exit 0 | 16/16; exit 0 | 33/33; exit 0 | **survived** |
| M307 | `tools/mado-tripwire.py:699` | Exclude permitted findings from per-class counts | 9/9; exit 0 | 16/16; exit 0 | 33/33; exit 0 | **survived** |
| M308 | `tools/mado-tripwire.py:719` | Label permitted findings clean instead of permitted_only | 9/9; exit 0 | 16/16; exit 0 | 33/33; exit 0 | **survived** |
| M309 | `tools/mado-tripwire.py:687` | Emit unredacted command text | 9/9; exit 0 | 16/16; exit 0 | 33/33; exit 0 | **survived** |
| M310 | `tools/mado-tripwire.py:673` | Accumulate eval_unparsed into unparsed_spawns | 9/9; exit 0 | 16/16; exit 0 | 33/33; exit 0 | **survived** |

## Killed mutants: expected detectors and actual outputs

### M301 — Read the AST dictionary key instead of its command value
Expected detector: hardening/eval-tool-bash must retain both sudo and systemctl:restart findings.
```text
[core; exit 0]
SELFTEST_SUMMARY: 9/9 passed failed=[]
[compound; exit 0]
SELFTEST_SUMMARY: 16/16 passed failed=[]
[hardening; exit 1]
CASE eval-tool-bash FAIL want=(1, [('host_mutation', 'sudo', 1, ''), ('host_mutation', 'systemctl:restart', 1, '')]) got=(0, [])
SELFTEST_SUMMARY: 32/33 passed failed=['eval-tool-bash']
```

### M302 — Skip invalid JSON rather than fail closed
Expected detector: core/malformed-json-line must return scanner exit 2.
```text
[core; exit 1]
CASE malformed-json-line FAIL want=(2, []) got=(0, [])
SELFTEST_SUMMARY: 8/9 passed failed=['malformed-json-line']
[compound; exit 0]
SELFTEST_SUMMARY: 16/16 passed failed=[]
[hardening; exit 0]
SELFTEST_SUMMARY: 33/33 passed failed=[]
```

### M303 — Deduplicate findings by class, dropping distinct rules
Expected detector: incident-replica must retain sudo and pacman:-S on the same call.
```text
[core; exit 1]
CASE incident-replica FAIL want=(1, [('host_mutation', 'pacman:-S', 3, ''), ('host_mutation', 'sudo', 3, '')]) got=(1, [('host_mutation', 'sudo', 3, '')])
SELFTEST_SUMMARY: 8/9 passed failed=['incident-replica']
[compound; exit 1]
CASE compound-and-sudo-pacman FAIL want=(1, [('host_mutation', 'pacman:-Syu', 2, 'compound-and.jsonl'), ('host_mutation', 'sudo', 2, 'compound-and.jsonl')]) got=(1, [('host_mutation', 'sudo', 2, 'compound-and.jsonl')])
SELFTEST_SUMMARY: 12/16 passed failed=['compound-and-sudo-pacman', 'bash-c-sudo-systemctl-restart', 'eval-bang-sudo-pacman', 'dir-scan-all-permitted']
[hardening; exit 1]
CASE newline-second-line FAIL want=(1, [('host_mutation', 'pacman:-S', 2, ''), ('host_mutation', 'sudo', 2, '')]) got=(1, [('host_mutation', 'sudo', 2, '')])
SELFTEST_SUMMARY: 28/33 passed failed=['newline-second-line', 'backslash-continuation', 'eval-tool-bash', 'pacman-downloadonly-mutation', 'run0-and-systemd-run']
```

### M304 — Ignore permit membership when computing unpermitted
Expected detector: permitted cases must exit 0 while retaining findings.
```text
[core; exit 1]
CASE live-probe-permitted FAIL want=(0, [('live_probe', 'hyprctl:version', 1, ''), ('live_probe', 'systemctl:status', 3, '')]) got=(1, [('live_probe', 'hyprctl:version', 1, ''), ('live_probe', 'systemctl:status', 3, '')])
SELFTEST_SUMMARY: 8/9 passed failed=['live-probe-permitted']
[compound; exit 1]
CASE var-assign-pacman-query-permitted FAIL want=(0, [('package_query', 'pacman:-Q', 2, 'var-assign-query.jsonl')]) got=(1, [('package_query', 'pacman:-Q', 2, 'var-assign-query.jsonl')])
SELFTEST_SUMMARY: 13/16 passed failed=['var-assign-pacman-query-permitted', 'omarchy-permitted', 'dir-scan-all-permitted']
[hardening; exit 0]
SELFTEST_SUMMARY: 33/33 passed failed=[]
```

## Surviving mutants: exact diffs and concrete witnesses
All six survived **all three suites**, while the witness outputs changed as shown. “Survived” is relative to the assigned existing selftest detector. The explanatory witness comparisons expose the missed behavior; they do not retroactively turn these into kills by that detector.
Root cause shared by these survivors: `tools/mado-tripwire.py:759-765` compares only `(class, rule, line[, basename])`, the process exit, JSON parseability and a marker prefix. It does not compare call IDs, transcript hashes, counts, command redaction, unparsed counters, or the exact semantic label.

### M305 — Take tool_call_id from the outer message instead of the toolCall — SURVIVED
Expected detector: assert the exact fixture tool-call identifier, not only its line.

Anchor: `.ufo/waves/round-17/tripwire/core/incident-replica.jsonl:3`, toolCall `call_38165`. Both emitted findings keep the correct line/rules and exit 1 but lose that identifier. This directly weakens call-ID provenance while all 58 selftest cases remain green. The original real-session transcript was not opened; this is the existing replica fixture, not a claimed observation at the real transcript anchor.

```diff
--- pristine/tools/mado-tripwire.py
+++ M305/tools/mado-tripwire.py
@@ -681,7 +681,7 @@
                 seen.add(key)
                 findings.append({
                     "file": path, "line": lineno,
-                    "tool_call_id": str(item.get("id", "")),
+                    "tool_call_id": str(obj.get("id", "")),
                     "timestamp": obj.get("timestamp"),
                     "tool": name, "class": cls, "rule": rule,
                     "argv0": argv0, "command": redact(text),
```
Exact relevant output fields (projections of the captured JSON; no normalization of these values):
```json
{"output": [{"line": 3, "rule": "sudo", "tool_call_id": "call_38165"}, {"line": 3, "rule": "pacman:-S", "tool_call_id": "call_38165"}], "phase": "pristine", "process_exit": 1}
{"output": [{"line": 3, "rule": "sudo", "tool_call_id": ""}, {"line": 3, "rule": "pacman:-S", "tool_call_id": ""}], "phase": "mutated", "process_exit": 1}
{"output": [{"line": 3, "rule": "sudo", "tool_call_id": "call_38165"}, {"line": 3, "rule": "pacman:-S", "tool_call_id": "call_38165"}], "phase": "restored", "process_exit": 1}
```

### M306 — Hash the pathname instead of the transcript bytes — SURVIVED
Expected detector: assert files[].sha256 equals SHA-256 of the actual input bytes.

Anchor: the same `core/incident-replica.jsonl` input. Independent `sha256sum` of its file bytes is `23d158fac8a1eec0f47681c220e09a21553b261bdd8037d6024ae9bd740a7d50`. The mutant instead emits the pathname digest `74013216cfbf9d2983f512f6f1c9a285f51bf8a60b97799178c3907b221ede94`, with unchanged findings and exit 1. This is a content-provenance regression, not an equivalent mutant.

```diff
--- pristine/tools/mado-tripwire.py
+++ M306/tools/mado-tripwire.py
@@ -629,7 +629,7 @@
             data = fh.read()
     except OSError:
         raise CouldNotEvaluate("unreadable file: %s" % path)
-    entry = {"path": path, "sha256": hashlib.sha256(data).hexdigest(),
+    entry = {"path": path, "sha256": hashlib.sha256(path.encode("utf-8")).hexdigest(),
              "lines": 0, "bash_calls": 0, "eval_calls": 0,
              "eval_unparsed": 0, "unparsed_spawns": 0}
     findings = []
```
Exact relevant output fields (projections of the captured JSON; no normalization of these values):
```json
{"output": "23d158fac8a1eec0f47681c220e09a21553b261bdd8037d6024ae9bd740a7d50", "phase": "pristine", "process_exit": 1}
{"output": "74013216cfbf9d2983f512f6f1c9a285f51bf8a60b97799178c3907b221ede94", "phase": "mutated", "process_exit": 1}
{"output": "23d158fac8a1eec0f47681c220e09a21553b261bdd8037d6024ae9bd740a7d50", "phase": "restored", "process_exit": 1}
```

### M307 — Exclude permitted findings from per-class counts — SURVIVED
Expected detector: assert counts include all findings, with permit affecting only unpermitted/exit.

Anchors: `core/live-probe.jsonl:1` and `:3`, scanned with `--permit live_probe` (the existing core `live-probe-permitted` case, expected.json:71-92). The mutant still emits both findings and exits 0, but counts.live_probe becomes 0 instead of 2. The separate unpermitted count remains correctly 0.

```diff
--- pristine/tools/mado-tripwire.py
+++ M307/tools/mado-tripwire.py
@@ -696,7 +696,7 @@
         e, fs = scan_file(f)
         entries.append(e)
         findings.extend(fs)
-    counts = {c: sum(1 for f in findings if f["class"] == c) for c in CLASSES}
+    counts = {c: sum(1 for f in findings if f["class"] == c and f["class"] not in permit) for c in CLASSES}
     unpermitted = sum(1 for f in findings if f["class"] not in permit)
     return entries, findings, counts, unpermitted
 
```
Exact relevant output fields (projections of the captured JSON; no normalization of these values):
```json
{"output": {"counts": {"host_mutation": 0, "live_probe": 2, "package_query": 0}, "finding_count": 2, "unpermitted": 0}, "phase": "pristine", "process_exit": 0}
{"output": {"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0}, "finding_count": 2, "unpermitted": 0}, "phase": "mutated", "process_exit": 0}
{"output": {"counts": {"host_mutation": 0, "live_probe": 2, "package_query": 0}, "finding_count": 2, "unpermitted": 0}, "phase": "restored", "process_exit": 0}
```

### M308 — Label permitted findings clean instead of permitted_only — SURVIVED
Expected detector: assert the complete first-line semantic label, not just its prefix.

Anchors: the same existing `core/live-probe.jsonl:1,3` permitted scan. The mutant emits `MADO_TRIPWIRE: clean` even though two findings remain present. Pristine and restored bytes emit `permitted_only`. This contradicts the clean/no-finding distinction in the script docstring at :15 and its four-label surface at :29. The selftest only checks the prefix `MADO_TRIPWIRE: ` at :764.

```diff
--- pristine/tools/mado-tripwire.py
+++ M308/tools/mado-tripwire.py
@@ -716,7 +716,7 @@
                                     "permitted": sorted(permit), "unpermitted": 0})
         return 2
     code = 1 if unpermitted else 0
-    label = "clean" if not findings else ("findings" if unpermitted else "permitted_only")
+    label = "clean" if not unpermitted else "findings"
     emit(label, {"schema": "mado-tripwire-verdict-v1", "exit": code, "files": entries,
                  "findings": findings, "counts": counts,
                  "permitted": sorted(permit), "unpermitted": unpermitted})
```
Exact relevant output fields (projections of the captured JSON; no normalization of these values):
```json
{"output": {"finding_count": 2, "first_line": "MADO_TRIPWIRE: permitted_only", "unpermitted": 0}, "phase": "pristine", "process_exit": 0}
{"output": {"finding_count": 2, "first_line": "MADO_TRIPWIRE: clean", "unpermitted": 0}, "phase": "mutated", "process_exit": 0}
{"output": {"finding_count": 2, "first_line": "MADO_TRIPWIRE: permitted_only", "unpermitted": 0}, "phase": "restored", "process_exit": 0}
```

### M309 — Emit unredacted command text — SURVIVED
Expected detector: assert synthetic sensitive-looking text is redacted in emitted findings.

Anchor: `/tmp/MadoR17-MutateTripwire3.wvd7me0k/redaction-witness.jsonl:1`, toolCall `synthetic-call`. Its only sensitive-looking text is the invented sentinel `SYNTHETIC_REDACTION_SENTINEL_1234567890`, not a credential. Pristine/restored output replaces it with `<redacted>`; the mutant emits it literally. The three existing suites do not detect removal of the redaction call. No credential/auth/OAuth file was read.

```diff
--- pristine/tools/mado-tripwire.py
+++ M309/tools/mado-tripwire.py
@@ -684,7 +684,7 @@
                     "tool_call_id": str(item.get("id", "")),
                     "timestamp": obj.get("timestamp"),
                     "tool": name, "class": cls, "rule": rule,
-                    "argv0": argv0, "command": redact(text),
+                    "argv0": argv0, "command": text,
                 })
     return entry, findings
 
```
Exact relevant output fields (projections of the captured JSON; no normalization of these values):
```json
{"output": ["journalctl --unit demo --example-token <redacted>"], "phase": "pristine", "process_exit": 1}
{"output": ["journalctl --unit demo --example-token SYNTHETIC_REDACTION_SENTINEL_1234567890"], "phase": "mutated", "process_exit": 1}
{"output": ["journalctl --unit demo --example-token <redacted>"], "phase": "restored", "process_exit": 1}
```

### M310 — Accumulate eval_unparsed into unparsed_spawns — SURVIVED
Expected detector: assert the nonliteral subprocess fixture reports unparsed_spawns=1.

Anchor: `.ufo/waves/round-17/tripwire/hardening/eval-nonliteral-unparsed-clean.jsonl:1`, toolCall `c1`. It contains `cmd = ['ls']; subprocess.run(cmd)` as transcript text. Pristine/restored output records one unparsed spawn; the mutant records zero. Detection remains clean in all states, as expected for this explicitly unsupported form, but the disclosed coverage-limit accounting is lost (script docstring :15-17).

```diff
--- pristine/tools/mado-tripwire.py
+++ M310/tools/mado-tripwire.py
@@ -670,7 +670,7 @@
                     continue
                 hits, un_eval, un_spawn = classify_eval(code, args.get("language"))
                 entry["eval_unparsed"] += un_eval
-                entry["unparsed_spawns"] += un_spawn
+                entry["unparsed_spawns"] += un_eval
             else:
                 continue
             seen = set()
```
Exact relevant output fields (projections of the captured JSON; no normalization of these values):
```json
{"output": {"eval_calls": 1, "eval_unparsed": 0, "unparsed_spawns": 1}, "phase": "pristine", "process_exit": 0}
{"output": {"eval_calls": 1, "eval_unparsed": 0, "unparsed_spawns": 0}, "phase": "mutated", "process_exit": 0}
{"output": {"eval_calls": 1, "eval_unparsed": 0, "unparsed_spawns": 1}, "phase": "restored", "process_exit": 0}
```

## Hashes and restoration evidence
Common pristine/restored source SHA-256 **H** = `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

Every copy’s before and restored hash was H. `cmp -s -- pristine.py <copy>` returned 0 for all ten copies after the `finally` restoration. The lane source hash before and after was also H. All 30 restored selftests passed, and every restored witness stdout/stderr/exit matched its pristine witness.
| Copy | Before | Mutated SHA-256 | Restored | Byte comparison exit |
|---|---|---|---|---|
| M301.py | H | `db6c11f58a0384d8964aae38a1805d9394e51b6b9e2d782eaf13392a51996fe9` | H | 0 |
| M302.py | H | `6bc19ef83240e7f895a560ce921e0a886dbd733e84f88a13740265bd1a5eb662` | H | 0 |
| M303.py | H | `7ec18af72057cdd02f6aa11569cf50e3eba90810499e1c732b130b2399ae7dc0` | H | 0 |
| M304.py | H | `1ffb8aacd472dcc1b9ab30df7d7f9c35333d659359b2633da9f04ba35140373c` | H | 0 |
| M305.py | H | `08c1ce1e221ff78d4867f646ab7e335ec4d2c6bd998aaa28306a9dad7ed41d19` | H | 0 |
| M306.py | H | `02161a59d397548423965f3be80c1c20dc351335e1a46896d97b732fa7434e72` | H | 0 |
| M307.py | H | `7b1c8d9b6dd400a04d46d43825a973295b3b608ccc872843ba28d1b019789972` | H | 0 |
| M308.py | H | `18d635f40247ac9913755d7433516ddf81497b5c64088f9f4770f239f07ce1e7` | H | 0 |
| M309.py | H | `24f6f6cbc0080fe3f1c512235328e8c7441d7aac2574477267d9b1ee4099be3f` | H | 0 |
| M310.py | H | `506a515c215768a0ac07b5e1c1994855beb6af25728c736241091f839524c317` | H | 0 |

Pristine and restored output for **each** M301–M310 copy (each suite exited 0, stderr empty):
```text
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
[core] SELFTEST_SUMMARY: 9/9 passed failed=[]
[compound] SELFTEST_SUMMARY: 16/16 passed failed=[]
[hardening] SELFTEST_SUMMARY: 33/33 passed failed=[]
```

## Safety and scope limits
- Installs/updates: **none**. No sudo, package-manager command, service/compositor/device probe, credential access, OMP CLI process, git mutation, jj command, delegation, or alternate runtime was invoked. Command-looking fixture strings were only classified as data; none was executed.
- Only this report was written in the lane. Mutations, the immutable pristine snapshot, and the synthetic redaction fixture were confined to the named `/tmp` scratch directory. All ten mutated script copies are now restored; survivor diffs are preserved here and below.
- No real-session transcript was read, and no actual pacman.log-window claim, C1 calibration, or C2 rubric claim was tested in this slice.
- Finding: the literal original 58/58 pass result reproduces, but it is not sufficient evidence for the six observed output/provenance/accounting properties. No production fix or contract change was made.

## Complete raw receipt
<details>
<summary>All commands, exact stdout/stderr, statuses, diffs, and before/mutated/restored hashes</summary>

```json
{
  "assignment": "MadoR17.MutateTripwire3",
  "initial_hashes": {
    "/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py": "4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M301.py": "4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M302.py": "4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M303.py": "4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M304.py": "4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M305.py": "4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M306.py": "4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M307.py": "4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M308.py": "4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M309.py": "4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M310.py": "4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44"
  },
  "installs": "none",
  "line_count": 818,
  "mutants": {
    "M301": {
      "defect": "Read the AST dictionary key instead of its command value",
      "diff": "--- pristine/tools/mado-tripwire.py\n+++ M301/tools/mado-tripwire.py\n@@ -548,7 +548,7 @@\n                 for k, v in zip(arg.keys, arg.values):\n                     if isinstance(k, ast.Constant) and k.value == \"command\" and \\\n                             isinstance(v, ast.Constant) and isinstance(v.value, str):\n-                        cmd = v.value\n+                        cmd = k.value\n             if cmd is None:\n                 unparsed += 1\n             else:\n",
      "expected_detector": "hardening/eval-tool-bash must retain both sudo and systemctl:restart findings",
      "line": 551,
      "verdict": "killed"
    },
    "M302": {
      "defect": "Skip invalid JSON rather than fail closed",
      "diff": "--- pristine/tools/mado-tripwire.py\n+++ M302/tools/mado-tripwire.py\n@@ -643,7 +643,7 @@\n         try:\n             obj = json.loads(raw.decode(\"utf-8\"), parse_constant=reject_constant)\n         except (ValueError, UnicodeDecodeError, RecursionError) as exc:\n-            raise CouldNotEvaluate(\"%s:%d invalid line (%s)\" % (path, lineno, type(exc).__name__))\n+            continue\n         if not isinstance(obj, dict) or \"type\" not in obj:\n             raise CouldNotEvaluate(\"%s:%d unknown record shape\" % (path, lineno))\n         if obj.get(\"type\") != \"message\":\n",
      "expected_detector": "core/malformed-json-line must return scanner exit 2",
      "line": 646,
      "verdict": "killed"
    },
    "M303": {
      "defect": "Deduplicate findings by class, dropping distinct rules",
      "diff": "--- pristine/tools/mado-tripwire.py\n+++ M303/tools/mado-tripwire.py\n@@ -675,7 +675,7 @@\n                 continue\n             seen = set()\n             for cls, rule, argv0, text in hits:\n-                key = (cls, rule)\n+                key = (cls,)\n                 if key in seen:\n                     continue\n                 seen.add(key)\n",
      "expected_detector": "incident-replica must retain sudo and pacman:-S on the same call",
      "line": 678,
      "verdict": "killed"
    },
    "M304": {
      "defect": "Ignore permit membership when computing unpermitted",
      "diff": "--- pristine/tools/mado-tripwire.py\n+++ M304/tools/mado-tripwire.py\n@@ -697,7 +697,7 @@\n         entries.append(e)\n         findings.extend(fs)\n     counts = {c: sum(1 for f in findings if f[\"class\"] == c) for c in CLASSES}\n-    unpermitted = sum(1 for f in findings if f[\"class\"] not in permit)\n+    unpermitted = len(findings)\n     return entries, findings, counts, unpermitted\n \n \n",
      "expected_detector": "permitted cases must exit 0 while retaining findings",
      "line": 700,
      "verdict": "killed"
    },
    "M305": {
      "defect": "Take tool_call_id from the outer message instead of the toolCall",
      "diff": "--- pristine/tools/mado-tripwire.py\n+++ M305/tools/mado-tripwire.py\n@@ -681,7 +681,7 @@\n                 seen.add(key)\n                 findings.append({\n                     \"file\": path, \"line\": lineno,\n-                    \"tool_call_id\": str(item.get(\"id\", \"\")),\n+                    \"tool_call_id\": str(obj.get(\"id\", \"\")),\n                     \"timestamp\": obj.get(\"timestamp\"),\n                     \"tool\": name, \"class\": cls, \"rule\": rule,\n                     \"argv0\": argv0, \"command\": redact(text),\n",
      "expected_detector": "assert the exact fixture tool-call identifier, not only its line",
      "line": 684,
      "verdict": "survived"
    },
    "M306": {
      "defect": "Hash the pathname instead of the transcript bytes",
      "diff": "--- pristine/tools/mado-tripwire.py\n+++ M306/tools/mado-tripwire.py\n@@ -629,7 +629,7 @@\n             data = fh.read()\n     except OSError:\n         raise CouldNotEvaluate(\"unreadable file: %s\" % path)\n-    entry = {\"path\": path, \"sha256\": hashlib.sha256(data).hexdigest(),\n+    entry = {\"path\": path, \"sha256\": hashlib.sha256(path.encode(\"utf-8\")).hexdigest(),\n              \"lines\": 0, \"bash_calls\": 0, \"eval_calls\": 0,\n              \"eval_unparsed\": 0, \"unparsed_spawns\": 0}\n     findings = []\n",
      "expected_detector": "assert files[].sha256 equals SHA-256 of the actual input bytes",
      "line": 632,
      "verdict": "survived"
    },
    "M307": {
      "defect": "Exclude permitted findings from per-class counts",
      "diff": "--- pristine/tools/mado-tripwire.py\n+++ M307/tools/mado-tripwire.py\n@@ -696,7 +696,7 @@\n         e, fs = scan_file(f)\n         entries.append(e)\n         findings.extend(fs)\n-    counts = {c: sum(1 for f in findings if f[\"class\"] == c) for c in CLASSES}\n+    counts = {c: sum(1 for f in findings if f[\"class\"] == c and f[\"class\"] not in permit) for c in CLASSES}\n     unpermitted = sum(1 for f in findings if f[\"class\"] not in permit)\n     return entries, findings, counts, unpermitted\n \n",
      "expected_detector": "assert counts include all findings, with permit affecting only unpermitted/exit",
      "line": 699,
      "verdict": "survived"
    },
    "M308": {
      "defect": "Label permitted findings clean instead of permitted_only",
      "diff": "--- pristine/tools/mado-tripwire.py\n+++ M308/tools/mado-tripwire.py\n@@ -716,7 +716,7 @@\n                                     \"permitted\": sorted(permit), \"unpermitted\": 0})\n         return 2\n     code = 1 if unpermitted else 0\n-    label = \"clean\" if not findings else (\"findings\" if unpermitted else \"permitted_only\")\n+    label = \"clean\" if not unpermitted else \"findings\"\n     emit(label, {\"schema\": \"mado-tripwire-verdict-v1\", \"exit\": code, \"files\": entries,\n                  \"findings\": findings, \"counts\": counts,\n                  \"permitted\": sorted(permit), \"unpermitted\": unpermitted})\n",
      "expected_detector": "assert the complete first-line semantic label, not just its prefix",
      "line": 719,
      "verdict": "survived"
    },
    "M309": {
      "defect": "Emit unredacted command text",
      "diff": "--- pristine/tools/mado-tripwire.py\n+++ M309/tools/mado-tripwire.py\n@@ -684,7 +684,7 @@\n                     \"tool_call_id\": str(item.get(\"id\", \"\")),\n                     \"timestamp\": obj.get(\"timestamp\"),\n                     \"tool\": name, \"class\": cls, \"rule\": rule,\n-                    \"argv0\": argv0, \"command\": redact(text),\n+                    \"argv0\": argv0, \"command\": text,\n                 })\n     return entry, findings\n \n",
      "expected_detector": "assert synthetic sensitive-looking text is redacted in emitted findings",
      "line": 687,
      "verdict": "survived"
    },
    "M310": {
      "defect": "Accumulate eval_unparsed into unparsed_spawns",
      "diff": "--- pristine/tools/mado-tripwire.py\n+++ M310/tools/mado-tripwire.py\n@@ -670,7 +670,7 @@\n                     continue\n                 hits, un_eval, un_spawn = classify_eval(code, args.get(\"language\"))\n                 entry[\"eval_unparsed\"] += un_eval\n-                entry[\"unparsed_spawns\"] += un_spawn\n+                entry[\"unparsed_spawns\"] += un_eval\n             else:\n                 continue\n             seen = set()\n",
      "expected_detector": "assert the nonliteral subprocess fixture reports unparsed_spawns=1",
      "line": 673,
      "verdict": "survived"
    }
  },
  "mutated_hashes": {
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M301.py": "db6c11f58a0384d8964aae38a1805d9394e51b6b9e2d782eaf13392a51996fe9",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M302.py": "6bc19ef83240e7f895a560ce921e0a886dbd733e84f88a13740265bd1a5eb662",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M303.py": "7ec18af72057cdd02f6aa11569cf50e3eba90810499e1c732b130b2399ae7dc0",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M304.py": "1ffb8aacd472dcc1b9ab30df7d7f9c35333d659359b2633da9f04ba35140373c",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M305.py": "08c1ce1e221ff78d4867f646ab7e335ec4d2c6bd998aaa28306a9dad7ed41d19",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M306.py": "02161a59d397548423965f3be80c1c20dc351335e1a46896d97b732fa7434e72",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M307.py": "7b1c8d9b6dd400a04d46d43825a973295b3b608ccc872843ba28d1b019789972",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M308.py": "18d635f40247ac9913755d7433516ddf81497b5c64088f9f4770f239f07ce1e7",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M309.py": "24f6f6cbc0080fe3f1c512235328e8c7441d7aac2574477267d9b1ee4099be3f",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M310.py": "506a515c215768a0ac07b5e1c1994855beb6af25728c736241091f839524c317"
  },
  "restoration_cmp_exits": {
    "M301": 0,
    "M302": 0,
    "M303": 0,
    "M304": 0,
    "M305": 0,
    "M306": 0,
    "M307": 0,
    "M308": 0,
    "M309": 0,
    "M310": 0
  },
  "restoration_hashes": {
    "/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py": "4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M301.py": "4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M302.py": "4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M303.py": "4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M304.py": "4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M305.py": "4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M306.py": "4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M307.py": "4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M308.py": "4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M309.py": "4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M310.py": "4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/pristine.py": "4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44"
  },
  "scratch": "/tmp/MadoR17-MutateTripwire3.wvd7me0k",
  "selftest_runs": [
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M301.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M301",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.224,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M301.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M301",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.375,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M301.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M301",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.741,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M302.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M302",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.226,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M302.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M302",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.374,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M302.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M302",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.757,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M303.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M303",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.221,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M303.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M303",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.379,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M303.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M303",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.761,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M304.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M304",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.221,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M304.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M304",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.381,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M304.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M304",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.765,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M305.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M305",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.225,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M305.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M305",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.389,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M305.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M305",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.762,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M306.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M306",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.223,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M306.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M306",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.379,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M306.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M306",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.75,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M307.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M307",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.227,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M307.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M307",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.379,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M307.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M307",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.747,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M308.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M308",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.215,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M308.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M308",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.362,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M308.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M308",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.733,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M309.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M309",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.215,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M309.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M309",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.371,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M309.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M309",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.716,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M310.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M310",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.216,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M310.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M310",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.364,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M310.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M310",
      "phase": "pristine",
      "returncode": 0,
      "seconds": 0.701,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M301.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M301",
      "phase": "mutated",
      "returncode": 0,
      "seconds": 0.209,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: db6c11f58a0384d8964aae38a1805d9394e51b6b9e2d782eaf13392a51996fe9\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M301.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M301",
      "phase": "mutated",
      "returncode": 0,
      "seconds": 0.363,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: db6c11f58a0384d8964aae38a1805d9394e51b6b9e2d782eaf13392a51996fe9\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M301.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M301",
      "phase": "mutated",
      "returncode": 1,
      "seconds": 0.716,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash FAIL want=(1, [('host_mutation', 'sudo', 1, ''), ('host_mutation', 'systemctl:restart', 1, '')]) got=(0, [])\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: db6c11f58a0384d8964aae38a1805d9394e51b6b9e2d782eaf13392a51996fe9\nSELFTEST_SUMMARY: 32/33 passed failed=['eval-tool-bash']\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M302.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M302",
      "phase": "mutated",
      "returncode": 1,
      "seconds": 0.209,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line FAIL want=(2, []) got=(0, [])\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 6bc19ef83240e7f895a560ce921e0a886dbd733e84f88a13740265bd1a5eb662\nSELFTEST_SUMMARY: 8/9 passed failed=['malformed-json-line']\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M302.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M302",
      "phase": "mutated",
      "returncode": 0,
      "seconds": 0.359,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 6bc19ef83240e7f895a560ce921e0a886dbd733e84f88a13740265bd1a5eb662\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M302.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M302",
      "phase": "mutated",
      "returncode": 0,
      "seconds": 0.716,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 6bc19ef83240e7f895a560ce921e0a886dbd733e84f88a13740265bd1a5eb662\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M303.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M303",
      "phase": "mutated",
      "returncode": 1,
      "seconds": 0.213,
      "stderr": "",
      "stdout": "CASE incident-replica FAIL want=(1, [('host_mutation', 'pacman:-S', 3, ''), ('host_mutation', 'sudo', 3, '')]) got=(1, [('host_mutation', 'sudo', 3, '')])\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 7ec18af72057cdd02f6aa11569cf50e3eba90810499e1c732b130b2399ae7dc0\nSELFTEST_SUMMARY: 8/9 passed failed=['incident-replica']\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M303.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M303",
      "phase": "mutated",
      "returncode": 1,
      "seconds": 0.367,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman FAIL want=(1, [('host_mutation', 'pacman:-Syu', 2, 'compound-and.jsonl'), ('host_mutation', 'sudo', 2, 'compound-and.jsonl')]) got=(1, [('host_mutation', 'sudo', 2, 'compound-and.jsonl')])\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart FAIL want=(1, [('host_mutation', 'sudo', 2, 'bash-c-subshell.jsonl'), ('host_mutation', 'systemctl:restart', 2, 'bash-c-subshell.jsonl')]) got=(1, [('host_mutation', 'sudo', 2, 'bash-c-subshell.jsonl')])\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman FAIL want=(1, [('host_mutation', 'pacman:-S', 2, 'eval-bang.jsonl'), ('host_mutation', 'sudo', 2, 'eval-bang.jsonl')]) got=(1, [('host_mutation', 'sudo', 2, 'eval-bang.jsonl')])\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted FAIL want=(0, [('host_mutation', 'hyprctl:dispatch', 2, 'wrappers-hyprctl.jsonl'), ('host_mutation', 'hyprctl:keyword', 4, 'wrappers-hyprctl.jsonl'), ('host_mutation', 'omarchy-restart-waybar', 2, 'omarchy-verbs.jsonl'), ('host_mutation', 'omarchy-theme-set', 4, 'omarchy-verbs.jsonl'), ('host_mutation', 'pacman:-R', 2, 'env-prefix.jsonl'), ('host_mutation', 'pacman:-S', 2, 'eval-bang.jsonl'), ('host_mutation', 'pacman:-Syu', 2, 'compound-and.jsonl'), ('host_mutation', 'pacman:-U', 2, 'abs-path-pacman.jsonl'), ('host_mutation', 'pkill', 2, 'xargs-pkill.jsonl'), ('host_mutation', 'sudo', 2, 'bash-c-subshell.jsonl'), ('host_mutation', 'sudo', 2, 'compound-and.jsonl'), ('host_mutation', 'sudo', 2, 'eval-bang.jsonl'), ('host_mutation', 'systemctl:daemon-reload', 2, 'user-daemon-reload.jsonl'), ('host_mutation', 'systemctl:restart', 2, 'bash-c-subshell.jsonl'), ('package_query', 'pacman:-Q', 2, 'var-assign-query.jsonl'), ('package_query', 'pacman:-Qq', 2, 'cmdsub-query.jsonl')]) got=(0, [('host_mutation', 'hyprctl:dispatch', 2, 'wrappers-hyprctl.jsonl'), ('host_mutation', 'hyprctl:keyword', 4, 'wrappers-hyprctl.jsonl'), ('host_mutation', 'omarchy-restart-waybar', 2, 'omarchy-verbs.jsonl'), ('host_mutation', 'omarchy-theme-set', 4, 'omarchy-verbs.jsonl'), ('host_mutation', 'pacman:-R', 2, 'env-prefix.jsonl'), ('host_mutation', 'pacman:-U', 2, 'abs-path-pacman.jsonl'), ('host_mutation', 'pkill', 2, 'xargs-pkill.jsonl'), ('host_mutation', 'sudo', 2, 'bash-c-subshell.jsonl'), ('host_mutation', 'sudo', 2, 'compound-and.jsonl'), ('host_mutation', 'sudo', 2, 'eval-bang.jsonl'), ('host_mutation', 'systemctl:daemon-reload', 2, 'user-daemon-reload.jsonl'), ('package_query', 'pacman:-Q', 2, 'var-assign-query.jsonl'), ('package_query', 'pacman:-Qq', 2, 'cmdsub-query.jsonl')])\nSELFTEST_SCRIPT_SHA256: 7ec18af72057cdd02f6aa11569cf50e3eba90810499e1c732b130b2399ae7dc0\nSELFTEST_SUMMARY: 12/16 passed failed=['compound-and-sudo-pacman', 'bash-c-sudo-systemctl-restart', 'eval-bang-sudo-pacman', 'dir-scan-all-permitted']\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M303.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M303",
      "phase": "mutated",
      "returncode": 1,
      "seconds": 0.728,
      "stderr": "",
      "stdout": "CASE newline-second-line FAIL want=(1, [('host_mutation', 'pacman:-S', 2, ''), ('host_mutation', 'sudo', 2, '')]) got=(1, [('host_mutation', 'sudo', 2, '')])\nCASE backslash-continuation FAIL want=(1, [('host_mutation', 'pacman:-S', 1, ''), ('host_mutation', 'sudo', 1, '')]) got=(1, [('host_mutation', 'sudo', 1, '')])\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash FAIL want=(1, [('host_mutation', 'sudo', 1, ''), ('host_mutation', 'systemctl:restart', 1, '')]) got=(1, [('host_mutation', 'sudo', 1, '')])\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation FAIL want=(1, [('host_mutation', 'pacman:-Sw', 1, ''), ('host_mutation', 'sudo', 1, '')]) got=(1, [('host_mutation', 'sudo', 1, '')])\nCASE run0-and-systemd-run FAIL want=(1, [('host_mutation', 'hyprctl:reload', 1, ''), ('host_mutation', 'pacman:-R', 1, ''), ('host_mutation', 'run0', 1, ''), ('host_mutation', 'systemd-run', 1, '')]) got=(1, [('host_mutation', 'run0', 1, '')])\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 7ec18af72057cdd02f6aa11569cf50e3eba90810499e1c732b130b2399ae7dc0\nSELFTEST_SUMMARY: 28/33 passed failed=['newline-second-line', 'backslash-continuation', 'eval-tool-bash', 'pacman-downloadonly-mutation', 'run0-and-systemd-run']\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M304.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M304",
      "phase": "mutated",
      "returncode": 1,
      "seconds": 0.213,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted FAIL want=(0, [('live_probe', 'hyprctl:version', 1, ''), ('live_probe', 'systemctl:status', 3, '')]) got=(1, [('live_probe', 'hyprctl:version', 1, ''), ('live_probe', 'systemctl:status', 3, '')])\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 1ffb8aacd472dcc1b9ab30df7d7f9c35333d659359b2633da9f04ba35140373c\nSELFTEST_SUMMARY: 8/9 passed failed=['live-probe-permitted']\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M304.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M304",
      "phase": "mutated",
      "returncode": 1,
      "seconds": 0.362,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted FAIL want=(0, [('package_query', 'pacman:-Q', 2, 'var-assign-query.jsonl')]) got=(1, [('package_query', 'pacman:-Q', 2, 'var-assign-query.jsonl')])\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted FAIL want=(0, [('host_mutation', 'omarchy-restart-waybar', 2, 'omarchy-verbs.jsonl'), ('host_mutation', 'omarchy-theme-set', 4, 'omarchy-verbs.jsonl')]) got=(1, [('host_mutation', 'omarchy-restart-waybar', 2, 'omarchy-verbs.jsonl'), ('host_mutation', 'omarchy-theme-set', 4, 'omarchy-verbs.jsonl')])\nCASE dir-scan-all-permitted FAIL want=(0, [('host_mutation', 'hyprctl:dispatch', 2, 'wrappers-hyprctl.jsonl'), ('host_mutation', 'hyprctl:keyword', 4, 'wrappers-hyprctl.jsonl'), ('host_mutation', 'omarchy-restart-waybar', 2, 'omarchy-verbs.jsonl'), ('host_mutation', 'omarchy-theme-set', 4, 'omarchy-verbs.jsonl'), ('host_mutation', 'pacman:-R', 2, 'env-prefix.jsonl'), ('host_mutation', 'pacman:-S', 2, 'eval-bang.jsonl'), ('host_mutation', 'pacman:-Syu', 2, 'compound-and.jsonl'), ('host_mutation', 'pacman:-U', 2, 'abs-path-pacman.jsonl'), ('host_mutation', 'pkill', 2, 'xargs-pkill.jsonl'), ('host_mutation', 'sudo', 2, 'bash-c-subshell.jsonl'), ('host_mutation', 'sudo', 2, 'compound-and.jsonl'), ('host_mutation', 'sudo', 2, 'eval-bang.jsonl'), ('host_mutation', 'systemctl:daemon-reload', 2, 'user-daemon-reload.jsonl'), ('host_mutation', 'systemctl:restart', 2, 'bash-c-subshell.jsonl'), ('package_query', 'pacman:-Q', 2, 'var-assign-query.jsonl'), ('package_query', 'pacman:-Qq', 2, 'cmdsub-query.jsonl')]) got=(1, [('host_mutation', 'hyprctl:dispatch', 2, 'wrappers-hyprctl.jsonl'), ('host_mutation', 'hyprctl:keyword', 4, 'wrappers-hyprctl.jsonl'), ('host_mutation', 'omarchy-restart-waybar', 2, 'omarchy-verbs.jsonl'), ('host_mutation', 'omarchy-theme-set', 4, 'omarchy-verbs.jsonl'), ('host_mutation', 'pacman:-R', 2, 'env-prefix.jsonl'), ('host_mutation', 'pacman:-S', 2, 'eval-bang.jsonl'), ('host_mutation', 'pacman:-Syu', 2, 'compound-and.jsonl'), ('host_mutation', 'pacman:-U', 2, 'abs-path-pacman.jsonl'), ('host_mutation', 'pkill', 2, 'xargs-pkill.jsonl'), ('host_mutation', 'sudo', 2, 'bash-c-subshell.jsonl'), ('host_mutation', 'sudo', 2, 'compound-and.jsonl'), ('host_mutation', 'sudo', 2, 'eval-bang.jsonl'), ('host_mutation', 'systemctl:daemon-reload', 2, 'user-daemon-reload.jsonl'), ('host_mutation', 'systemctl:restart', 2, 'bash-c-subshell.jsonl'), ('package_query', 'pacman:-Q', 2, 'var-assign-query.jsonl'), ('package_query', 'pacman:-Qq', 2, 'cmdsub-query.jsonl')])\nSELFTEST_SCRIPT_SHA256: 1ffb8aacd472dcc1b9ab30df7d7f9c35333d659359b2633da9f04ba35140373c\nSELFTEST_SUMMARY: 13/16 passed failed=['var-assign-pacman-query-permitted', 'omarchy-permitted', 'dir-scan-all-permitted']\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M304.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M304",
      "phase": "mutated",
      "returncode": 0,
      "seconds": 0.722,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 1ffb8aacd472dcc1b9ab30df7d7f9c35333d659359b2633da9f04ba35140373c\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M305.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M305",
      "phase": "mutated",
      "returncode": 0,
      "seconds": 0.212,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 08c1ce1e221ff78d4867f646ab7e335ec4d2c6bd998aaa28306a9dad7ed41d19\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M305.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M305",
      "phase": "mutated",
      "returncode": 0,
      "seconds": 0.362,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 08c1ce1e221ff78d4867f646ab7e335ec4d2c6bd998aaa28306a9dad7ed41d19\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M305.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M305",
      "phase": "mutated",
      "returncode": 0,
      "seconds": 0.73,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 08c1ce1e221ff78d4867f646ab7e335ec4d2c6bd998aaa28306a9dad7ed41d19\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M306.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M306",
      "phase": "mutated",
      "returncode": 0,
      "seconds": 0.214,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 02161a59d397548423965f3be80c1c20dc351335e1a46896d97b732fa7434e72\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M306.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M306",
      "phase": "mutated",
      "returncode": 0,
      "seconds": 0.363,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 02161a59d397548423965f3be80c1c20dc351335e1a46896d97b732fa7434e72\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M306.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M306",
      "phase": "mutated",
      "returncode": 0,
      "seconds": 0.726,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 02161a59d397548423965f3be80c1c20dc351335e1a46896d97b732fa7434e72\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M307.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M307",
      "phase": "mutated",
      "returncode": 0,
      "seconds": 0.211,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 7b1c8d9b6dd400a04d46d43825a973295b3b608ccc872843ba28d1b019789972\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M307.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M307",
      "phase": "mutated",
      "returncode": 0,
      "seconds": 0.372,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 7b1c8d9b6dd400a04d46d43825a973295b3b608ccc872843ba28d1b019789972\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M307.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M307",
      "phase": "mutated",
      "returncode": 0,
      "seconds": 0.736,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 7b1c8d9b6dd400a04d46d43825a973295b3b608ccc872843ba28d1b019789972\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M308.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M308",
      "phase": "mutated",
      "returncode": 0,
      "seconds": 0.22,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 18d635f40247ac9913755d7433516ddf81497b5c64088f9f4770f239f07ce1e7\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M308.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M308",
      "phase": "mutated",
      "returncode": 0,
      "seconds": 0.38,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 18d635f40247ac9913755d7433516ddf81497b5c64088f9f4770f239f07ce1e7\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M308.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M308",
      "phase": "mutated",
      "returncode": 0,
      "seconds": 0.72,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 18d635f40247ac9913755d7433516ddf81497b5c64088f9f4770f239f07ce1e7\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M309.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M309",
      "phase": "mutated",
      "returncode": 0,
      "seconds": 0.216,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 24f6f6cbc0080fe3f1c512235328e8c7441d7aac2574477267d9b1ee4099be3f\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M309.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M309",
      "phase": "mutated",
      "returncode": 0,
      "seconds": 0.364,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 24f6f6cbc0080fe3f1c512235328e8c7441d7aac2574477267d9b1ee4099be3f\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M309.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M309",
      "phase": "mutated",
      "returncode": 0,
      "seconds": 0.72,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 24f6f6cbc0080fe3f1c512235328e8c7441d7aac2574477267d9b1ee4099be3f\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M310.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M310",
      "phase": "mutated",
      "returncode": 0,
      "seconds": 0.219,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 506a515c215768a0ac07b5e1c1994855beb6af25728c736241091f839524c317\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M310.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M310",
      "phase": "mutated",
      "returncode": 0,
      "seconds": 0.361,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 506a515c215768a0ac07b5e1c1994855beb6af25728c736241091f839524c317\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M310.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M310",
      "phase": "mutated",
      "returncode": 0,
      "seconds": 0.709,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 506a515c215768a0ac07b5e1c1994855beb6af25728c736241091f839524c317\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M301.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M301",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.212,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M301.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M301",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.366,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M301.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M301",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.723,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M302.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M302",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.213,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M302.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M302",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.364,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M302.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M302",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.724,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M303.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M303",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.212,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M303.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M303",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.364,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M303.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M303",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.733,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M304.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M304",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.217,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M304.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M304",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.367,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M304.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M304",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.741,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M305.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M305",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.217,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M305.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M305",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.382,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M305.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M305",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.745,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M306.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M306",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.218,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M306.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M306",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.386,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M306.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M306",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.746,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M307.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M307",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.222,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M307.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M307",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.385,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M307.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M307",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.765,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M308.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M308",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.22,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M308.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M308",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.385,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M308.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M308",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.748,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M309.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M309",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.226,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M309.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M309",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.38,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M309.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M309",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.751,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M310.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core"
      ],
      "mutant": "M310",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.222,
      "stderr": "",
      "stdout": "CASE incident-replica ok\nCASE package-query-only ok\nCASE live-probe-only ok\nCASE live-probe-permitted ok\nCASE clean-reads ok\nCASE mention-only ok\nCASE malformed-json-line ok\nCASE no-jsonl-dir ok\nCASE dir-scan-two-files ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 9/9 passed failed=[]\n",
      "suite": "core",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M310.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound"
      ],
      "mutant": "M310",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.377,
      "stderr": "",
      "stdout": "CASE compound-and-sudo-pacman ok\nCASE abs-path-pacman-upgrade ok\nCASE env-prefix-pacman-remove ok\nCASE var-assign-pacman-query ok\nCASE var-assign-pacman-query-permitted ok\nCASE bash-c-sudo-systemctl-restart ok\nCASE cmdsub-pacman-query ok\nCASE timeout-nohup-hyprctl-mutations ok\nCASE xargs-pkill ok\nCASE quoted-data-clean ok\nCASE eval-bang-sudo-pacman ok\nCASE eval-nonbang-clean ok\nCASE user-daemon-reload ok\nCASE omarchy-mutating-verbs ok\nCASE omarchy-permitted ok\nCASE dir-scan-all-permitted ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 16/16 passed failed=[]\n",
      "suite": "compound",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M310.py",
        "--selftest",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening"
      ],
      "mutant": "M310",
      "phase": "restored",
      "returncode": 0,
      "seconds": 0.739,
      "stderr": "",
      "stdout": "CASE newline-second-line ok\nCASE backslash-continuation ok\nCASE heredoc-data-clean ok\nCASE heredoc-into-shell ok\nCASE multiline-quoted-commit-clean ok\nCASE multi-toolcall-line ok\nCASE eval-subprocess-list ok\nCASE eval-bash-c-recipe ok\nCASE eval-shell-true ok\nCASE eval-tool-bash ok\nCASE eval-nonliteral-unparsed-clean ok\nCASE eval-js-unparsed-clean ok\nCASE kill-zero-clean ok\nCASE kill-term ok\nCASE systemctl-suspend ok\nCASE loginctl-lock ok\nCASE loginctl-show-probe ok\nCASE omarchy-quoted-grep-clean ok\nCASE omarchy-bare-launch ok\nCASE result-and-marker-only-clean ok\nCASE pacman-sync-print-query ok\nCASE pacman-downloadonly-mutation ok\nCASE run0-and-systemd-run ok\nCASE hyprctl-batch ok\nCASE dollar-paren-in-double-quotes ok\nCASE pacman-log-read-clean ok\nCASE refused-db-name ok\nCASE seat-name-with-credential-word-allowed ok\nCASE refused-symlink ok\nCASE command-v-lookup-clean ok\nCASE python-heredoc-spawn ok\nCASE python-heredoc-data-clean ok\nCASE python-c-spawn ok\nSELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44\nSELFTEST_SUMMARY: 33/33 passed failed=[]\n",
      "suite": "hardening",
      "timed_out": false
    }
  ],
  "slice": [
    546,
    818
  ],
  "source_sha256_before": "4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44",
  "target": "/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py",
  "witness_input_hashes": {
    "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl": "23d158fac8a1eec0f47681c220e09a21553b261bdd8037d6024ae9bd740a7d50",
    "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl": "8fcb7e1d44d6b42b582121bfe1419ea067ed7a68980ff5bbe3bc8b1373f8ee2f",
    "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening/eval-nonliteral-unparsed-clean.jsonl": "9ec45f2adbe9547a7ab7b89ae35fe13b7de2069837aee862c3d2a6feab348aa0",
    "/tmp/MadoR17-MutateTripwire3.wvd7me0k/redaction-witness.jsonl": "97a3428f256a0b9e6027de76c08369acd212732178c79d9bab9659716d590107"
  },
  "witness_runs": [
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/pristine.py",
        "--scan",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl"
      ],
      "mutant": "M305",
      "phase": "pristine",
      "returncode": 1,
      "stderr": "",
      "stdout": "MADO_TRIPWIRE: findings\n{\"counts\": {\"host_mutation\": 2, \"live_probe\": 0, \"package_query\": 0}, \"exit\": 1, \"files\": [{\"bash_calls\": 1, \"eval_calls\": 0, \"eval_unparsed\": 0, \"lines\": 4, \"path\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl\", \"sha256\": \"23d158fac8a1eec0f47681c220e09a21553b261bdd8037d6024ae9bd740a7d50\", \"unparsed_spawns\": 0}], \"findings\": [{\"argv0\": \"sudo\", \"class\": \"host_mutation\", \"command\": \"sudo pacman -S --needed --noconfirm libinput libinput-tools\", \"file\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl\", \"line\": 3, \"rule\": \"sudo\", \"timestamp\": \"2026-10-19T22:14:05.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"call_38165\"}, {\"argv0\": \"pacman\", \"class\": \"host_mutation\", \"command\": \"pacman -S --needed --noconfirm libinput libinput-tools\", \"file\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl\", \"line\": 3, \"rule\": \"pacman:-S\", \"timestamp\": \"2026-10-19T22:14:05.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"call_38165\"}], \"permitted\": [], \"schema\": \"mado-tripwire-verdict-v1\", \"unpermitted\": 2}\n",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M305.py",
        "--scan",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl"
      ],
      "mutant": "M305",
      "phase": "mutated",
      "returncode": 1,
      "stderr": "",
      "stdout": "MADO_TRIPWIRE: findings\n{\"counts\": {\"host_mutation\": 2, \"live_probe\": 0, \"package_query\": 0}, \"exit\": 1, \"files\": [{\"bash_calls\": 1, \"eval_calls\": 0, \"eval_unparsed\": 0, \"lines\": 4, \"path\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl\", \"sha256\": \"23d158fac8a1eec0f47681c220e09a21553b261bdd8037d6024ae9bd740a7d50\", \"unparsed_spawns\": 0}], \"findings\": [{\"argv0\": \"sudo\", \"class\": \"host_mutation\", \"command\": \"sudo pacman -S --needed --noconfirm libinput libinput-tools\", \"file\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl\", \"line\": 3, \"rule\": \"sudo\", \"timestamp\": \"2026-10-19T22:14:05.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"\"}, {\"argv0\": \"pacman\", \"class\": \"host_mutation\", \"command\": \"pacman -S --needed --noconfirm libinput libinput-tools\", \"file\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl\", \"line\": 3, \"rule\": \"pacman:-S\", \"timestamp\": \"2026-10-19T22:14:05.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"\"}], \"permitted\": [], \"schema\": \"mado-tripwire-verdict-v1\", \"unpermitted\": 2}\n",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/pristine.py",
        "--scan",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl"
      ],
      "mutant": "M306",
      "phase": "pristine",
      "returncode": 1,
      "stderr": "",
      "stdout": "MADO_TRIPWIRE: findings\n{\"counts\": {\"host_mutation\": 2, \"live_probe\": 0, \"package_query\": 0}, \"exit\": 1, \"files\": [{\"bash_calls\": 1, \"eval_calls\": 0, \"eval_unparsed\": 0, \"lines\": 4, \"path\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl\", \"sha256\": \"23d158fac8a1eec0f47681c220e09a21553b261bdd8037d6024ae9bd740a7d50\", \"unparsed_spawns\": 0}], \"findings\": [{\"argv0\": \"sudo\", \"class\": \"host_mutation\", \"command\": \"sudo pacman -S --needed --noconfirm libinput libinput-tools\", \"file\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl\", \"line\": 3, \"rule\": \"sudo\", \"timestamp\": \"2026-10-19T22:14:05.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"call_38165\"}, {\"argv0\": \"pacman\", \"class\": \"host_mutation\", \"command\": \"pacman -S --needed --noconfirm libinput libinput-tools\", \"file\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl\", \"line\": 3, \"rule\": \"pacman:-S\", \"timestamp\": \"2026-10-19T22:14:05.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"call_38165\"}], \"permitted\": [], \"schema\": \"mado-tripwire-verdict-v1\", \"unpermitted\": 2}\n",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M306.py",
        "--scan",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl"
      ],
      "mutant": "M306",
      "phase": "mutated",
      "returncode": 1,
      "stderr": "",
      "stdout": "MADO_TRIPWIRE: findings\n{\"counts\": {\"host_mutation\": 2, \"live_probe\": 0, \"package_query\": 0}, \"exit\": 1, \"files\": [{\"bash_calls\": 1, \"eval_calls\": 0, \"eval_unparsed\": 0, \"lines\": 4, \"path\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl\", \"sha256\": \"74013216cfbf9d2983f512f6f1c9a285f51bf8a60b97799178c3907b221ede94\", \"unparsed_spawns\": 0}], \"findings\": [{\"argv0\": \"sudo\", \"class\": \"host_mutation\", \"command\": \"sudo pacman -S --needed --noconfirm libinput libinput-tools\", \"file\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl\", \"line\": 3, \"rule\": \"sudo\", \"timestamp\": \"2026-10-19T22:14:05.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"call_38165\"}, {\"argv0\": \"pacman\", \"class\": \"host_mutation\", \"command\": \"pacman -S --needed --noconfirm libinput libinput-tools\", \"file\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl\", \"line\": 3, \"rule\": \"pacman:-S\", \"timestamp\": \"2026-10-19T22:14:05.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"call_38165\"}], \"permitted\": [], \"schema\": \"mado-tripwire-verdict-v1\", \"unpermitted\": 2}\n",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/pristine.py",
        "--scan",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl",
        "--permit",
        "live_probe"
      ],
      "mutant": "M307",
      "phase": "pristine",
      "returncode": 0,
      "stderr": "",
      "stdout": "MADO_TRIPWIRE: permitted_only\n{\"counts\": {\"host_mutation\": 0, \"live_probe\": 2, \"package_query\": 0}, \"exit\": 0, \"files\": [{\"bash_calls\": 2, \"eval_calls\": 0, \"eval_unparsed\": 0, \"lines\": 3, \"path\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl\", \"sha256\": \"8fcb7e1d44d6b42b582121bfe1419ea067ed7a68980ff5bbe3bc8b1373f8ee2f\", \"unparsed_spawns\": 0}], \"findings\": [{\"argv0\": \"hyprctl\", \"class\": \"live_probe\", \"command\": \"hyprctl version\", \"file\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl\", \"line\": 1, \"rule\": \"hyprctl:version\", \"timestamp\": \"2026-10-20T03:10:00.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"call_lp1\"}, {\"argv0\": \"systemctl\", \"class\": \"live_probe\", \"command\": \"systemctl --user status hypridle\", \"file\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl\", \"line\": 3, \"rule\": \"systemctl:status\", \"timestamp\": \"2026-10-20T03:10:15.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"call_lp2\"}], \"permitted\": [\"live_probe\"], \"schema\": \"mado-tripwire-verdict-v1\", \"unpermitted\": 0}\n",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M307.py",
        "--scan",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl",
        "--permit",
        "live_probe"
      ],
      "mutant": "M307",
      "phase": "mutated",
      "returncode": 0,
      "stderr": "",
      "stdout": "MADO_TRIPWIRE: permitted_only\n{\"counts\": {\"host_mutation\": 0, \"live_probe\": 0, \"package_query\": 0}, \"exit\": 0, \"files\": [{\"bash_calls\": 2, \"eval_calls\": 0, \"eval_unparsed\": 0, \"lines\": 3, \"path\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl\", \"sha256\": \"8fcb7e1d44d6b42b582121bfe1419ea067ed7a68980ff5bbe3bc8b1373f8ee2f\", \"unparsed_spawns\": 0}], \"findings\": [{\"argv0\": \"hyprctl\", \"class\": \"live_probe\", \"command\": \"hyprctl version\", \"file\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl\", \"line\": 1, \"rule\": \"hyprctl:version\", \"timestamp\": \"2026-10-20T03:10:00.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"call_lp1\"}, {\"argv0\": \"systemctl\", \"class\": \"live_probe\", \"command\": \"systemctl --user status hypridle\", \"file\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl\", \"line\": 3, \"rule\": \"systemctl:status\", \"timestamp\": \"2026-10-20T03:10:15.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"call_lp2\"}], \"permitted\": [\"live_probe\"], \"schema\": \"mado-tripwire-verdict-v1\", \"unpermitted\": 0}\n",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/pristine.py",
        "--scan",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl",
        "--permit",
        "live_probe"
      ],
      "mutant": "M308",
      "phase": "pristine",
      "returncode": 0,
      "stderr": "",
      "stdout": "MADO_TRIPWIRE: permitted_only\n{\"counts\": {\"host_mutation\": 0, \"live_probe\": 2, \"package_query\": 0}, \"exit\": 0, \"files\": [{\"bash_calls\": 2, \"eval_calls\": 0, \"eval_unparsed\": 0, \"lines\": 3, \"path\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl\", \"sha256\": \"8fcb7e1d44d6b42b582121bfe1419ea067ed7a68980ff5bbe3bc8b1373f8ee2f\", \"unparsed_spawns\": 0}], \"findings\": [{\"argv0\": \"hyprctl\", \"class\": \"live_probe\", \"command\": \"hyprctl version\", \"file\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl\", \"line\": 1, \"rule\": \"hyprctl:version\", \"timestamp\": \"2026-10-20T03:10:00.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"call_lp1\"}, {\"argv0\": \"systemctl\", \"class\": \"live_probe\", \"command\": \"systemctl --user status hypridle\", \"file\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl\", \"line\": 3, \"rule\": \"systemctl:status\", \"timestamp\": \"2026-10-20T03:10:15.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"call_lp2\"}], \"permitted\": [\"live_probe\"], \"schema\": \"mado-tripwire-verdict-v1\", \"unpermitted\": 0}\n",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M308.py",
        "--scan",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl",
        "--permit",
        "live_probe"
      ],
      "mutant": "M308",
      "phase": "mutated",
      "returncode": 0,
      "stderr": "",
      "stdout": "MADO_TRIPWIRE: clean\n{\"counts\": {\"host_mutation\": 0, \"live_probe\": 2, \"package_query\": 0}, \"exit\": 0, \"files\": [{\"bash_calls\": 2, \"eval_calls\": 0, \"eval_unparsed\": 0, \"lines\": 3, \"path\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl\", \"sha256\": \"8fcb7e1d44d6b42b582121bfe1419ea067ed7a68980ff5bbe3bc8b1373f8ee2f\", \"unparsed_spawns\": 0}], \"findings\": [{\"argv0\": \"hyprctl\", \"class\": \"live_probe\", \"command\": \"hyprctl version\", \"file\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl\", \"line\": 1, \"rule\": \"hyprctl:version\", \"timestamp\": \"2026-10-20T03:10:00.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"call_lp1\"}, {\"argv0\": \"systemctl\", \"class\": \"live_probe\", \"command\": \"systemctl --user status hypridle\", \"file\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl\", \"line\": 3, \"rule\": \"systemctl:status\", \"timestamp\": \"2026-10-20T03:10:15.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"call_lp2\"}], \"permitted\": [\"live_probe\"], \"schema\": \"mado-tripwire-verdict-v1\", \"unpermitted\": 0}\n",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/pristine.py",
        "--scan",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/redaction-witness.jsonl"
      ],
      "mutant": "M309",
      "phase": "pristine",
      "returncode": 1,
      "stderr": "",
      "stdout": "MADO_TRIPWIRE: findings\n{\"counts\": {\"host_mutation\": 0, \"live_probe\": 1, \"package_query\": 0}, \"exit\": 1, \"files\": [{\"bash_calls\": 1, \"eval_calls\": 0, \"eval_unparsed\": 0, \"lines\": 1, \"path\": \"/tmp/MadoR17-MutateTripwire3.wvd7me0k/redaction-witness.jsonl\", \"sha256\": \"97a3428f256a0b9e6027de76c08369acd212732178c79d9bab9659716d590107\", \"unparsed_spawns\": 0}], \"findings\": [{\"argv0\": \"journalctl\", \"class\": \"live_probe\", \"command\": \"journalctl --unit demo --example-token <redacted>\", \"file\": \"/tmp/MadoR17-MutateTripwire3.wvd7me0k/redaction-witness.jsonl\", \"line\": 1, \"rule\": \"journalctl\", \"timestamp\": \"2026-10-20T00:00:00.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"synthetic-call\"}], \"permitted\": [], \"schema\": \"mado-tripwire-verdict-v1\", \"unpermitted\": 1}\n",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M309.py",
        "--scan",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/redaction-witness.jsonl"
      ],
      "mutant": "M309",
      "phase": "mutated",
      "returncode": 1,
      "stderr": "",
      "stdout": "MADO_TRIPWIRE: findings\n{\"counts\": {\"host_mutation\": 0, \"live_probe\": 1, \"package_query\": 0}, \"exit\": 1, \"files\": [{\"bash_calls\": 1, \"eval_calls\": 0, \"eval_unparsed\": 0, \"lines\": 1, \"path\": \"/tmp/MadoR17-MutateTripwire3.wvd7me0k/redaction-witness.jsonl\", \"sha256\": \"97a3428f256a0b9e6027de76c08369acd212732178c79d9bab9659716d590107\", \"unparsed_spawns\": 0}], \"findings\": [{\"argv0\": \"journalctl\", \"class\": \"live_probe\", \"command\": \"journalctl --unit demo --example-token SYNTHETIC_REDACTION_SENTINEL_1234567890\", \"file\": \"/tmp/MadoR17-MutateTripwire3.wvd7me0k/redaction-witness.jsonl\", \"line\": 1, \"rule\": \"journalctl\", \"timestamp\": \"2026-10-20T00:00:00.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"synthetic-call\"}], \"permitted\": [], \"schema\": \"mado-tripwire-verdict-v1\", \"unpermitted\": 1}\n",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/pristine.py",
        "--scan",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening/eval-nonliteral-unparsed-clean.jsonl"
      ],
      "mutant": "M310",
      "phase": "pristine",
      "returncode": 0,
      "stderr": "",
      "stdout": "MADO_TRIPWIRE: clean\n{\"counts\": {\"host_mutation\": 0, \"live_probe\": 0, \"package_query\": 0}, \"exit\": 0, \"files\": [{\"bash_calls\": 0, \"eval_calls\": 1, \"eval_unparsed\": 0, \"lines\": 1, \"path\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening/eval-nonliteral-unparsed-clean.jsonl\", \"sha256\": \"9ec45f2adbe9547a7ab7b89ae35fe13b7de2069837aee862c3d2a6feab348aa0\", \"unparsed_spawns\": 1}], \"findings\": [], \"permitted\": [], \"schema\": \"mado-tripwire-verdict-v1\", \"unpermitted\": 0}\n",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M310.py",
        "--scan",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening/eval-nonliteral-unparsed-clean.jsonl"
      ],
      "mutant": "M310",
      "phase": "mutated",
      "returncode": 0,
      "stderr": "",
      "stdout": "MADO_TRIPWIRE: clean\n{\"counts\": {\"host_mutation\": 0, \"live_probe\": 0, \"package_query\": 0}, \"exit\": 0, \"files\": [{\"bash_calls\": 0, \"eval_calls\": 1, \"eval_unparsed\": 0, \"lines\": 1, \"path\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening/eval-nonliteral-unparsed-clean.jsonl\", \"sha256\": \"9ec45f2adbe9547a7ab7b89ae35fe13b7de2069837aee862c3d2a6feab348aa0\", \"unparsed_spawns\": 0}], \"findings\": [], \"permitted\": [], \"schema\": \"mado-tripwire-verdict-v1\", \"unpermitted\": 0}\n",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M305.py",
        "--scan",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl"
      ],
      "mutant": "M305",
      "phase": "restored",
      "returncode": 1,
      "stderr": "",
      "stdout": "MADO_TRIPWIRE: findings\n{\"counts\": {\"host_mutation\": 2, \"live_probe\": 0, \"package_query\": 0}, \"exit\": 1, \"files\": [{\"bash_calls\": 1, \"eval_calls\": 0, \"eval_unparsed\": 0, \"lines\": 4, \"path\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl\", \"sha256\": \"23d158fac8a1eec0f47681c220e09a21553b261bdd8037d6024ae9bd740a7d50\", \"unparsed_spawns\": 0}], \"findings\": [{\"argv0\": \"sudo\", \"class\": \"host_mutation\", \"command\": \"sudo pacman -S --needed --noconfirm libinput libinput-tools\", \"file\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl\", \"line\": 3, \"rule\": \"sudo\", \"timestamp\": \"2026-10-19T22:14:05.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"call_38165\"}, {\"argv0\": \"pacman\", \"class\": \"host_mutation\", \"command\": \"pacman -S --needed --noconfirm libinput libinput-tools\", \"file\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl\", \"line\": 3, \"rule\": \"pacman:-S\", \"timestamp\": \"2026-10-19T22:14:05.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"call_38165\"}], \"permitted\": [], \"schema\": \"mado-tripwire-verdict-v1\", \"unpermitted\": 2}\n",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M306.py",
        "--scan",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl"
      ],
      "mutant": "M306",
      "phase": "restored",
      "returncode": 1,
      "stderr": "",
      "stdout": "MADO_TRIPWIRE: findings\n{\"counts\": {\"host_mutation\": 2, \"live_probe\": 0, \"package_query\": 0}, \"exit\": 1, \"files\": [{\"bash_calls\": 1, \"eval_calls\": 0, \"eval_unparsed\": 0, \"lines\": 4, \"path\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl\", \"sha256\": \"23d158fac8a1eec0f47681c220e09a21553b261bdd8037d6024ae9bd740a7d50\", \"unparsed_spawns\": 0}], \"findings\": [{\"argv0\": \"sudo\", \"class\": \"host_mutation\", \"command\": \"sudo pacman -S --needed --noconfirm libinput libinput-tools\", \"file\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl\", \"line\": 3, \"rule\": \"sudo\", \"timestamp\": \"2026-10-19T22:14:05.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"call_38165\"}, {\"argv0\": \"pacman\", \"class\": \"host_mutation\", \"command\": \"pacman -S --needed --noconfirm libinput libinput-tools\", \"file\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/incident-replica.jsonl\", \"line\": 3, \"rule\": \"pacman:-S\", \"timestamp\": \"2026-10-19T22:14:05.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"call_38165\"}], \"permitted\": [], \"schema\": \"mado-tripwire-verdict-v1\", \"unpermitted\": 2}\n",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M307.py",
        "--scan",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl",
        "--permit",
        "live_probe"
      ],
      "mutant": "M307",
      "phase": "restored",
      "returncode": 0,
      "stderr": "",
      "stdout": "MADO_TRIPWIRE: permitted_only\n{\"counts\": {\"host_mutation\": 0, \"live_probe\": 2, \"package_query\": 0}, \"exit\": 0, \"files\": [{\"bash_calls\": 2, \"eval_calls\": 0, \"eval_unparsed\": 0, \"lines\": 3, \"path\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl\", \"sha256\": \"8fcb7e1d44d6b42b582121bfe1419ea067ed7a68980ff5bbe3bc8b1373f8ee2f\", \"unparsed_spawns\": 0}], \"findings\": [{\"argv0\": \"hyprctl\", \"class\": \"live_probe\", \"command\": \"hyprctl version\", \"file\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl\", \"line\": 1, \"rule\": \"hyprctl:version\", \"timestamp\": \"2026-10-20T03:10:00.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"call_lp1\"}, {\"argv0\": \"systemctl\", \"class\": \"live_probe\", \"command\": \"systemctl --user status hypridle\", \"file\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl\", \"line\": 3, \"rule\": \"systemctl:status\", \"timestamp\": \"2026-10-20T03:10:15.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"call_lp2\"}], \"permitted\": [\"live_probe\"], \"schema\": \"mado-tripwire-verdict-v1\", \"unpermitted\": 0}\n",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M308.py",
        "--scan",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl",
        "--permit",
        "live_probe"
      ],
      "mutant": "M308",
      "phase": "restored",
      "returncode": 0,
      "stderr": "",
      "stdout": "MADO_TRIPWIRE: permitted_only\n{\"counts\": {\"host_mutation\": 0, \"live_probe\": 2, \"package_query\": 0}, \"exit\": 0, \"files\": [{\"bash_calls\": 2, \"eval_calls\": 0, \"eval_unparsed\": 0, \"lines\": 3, \"path\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl\", \"sha256\": \"8fcb7e1d44d6b42b582121bfe1419ea067ed7a68980ff5bbe3bc8b1373f8ee2f\", \"unparsed_spawns\": 0}], \"findings\": [{\"argv0\": \"hyprctl\", \"class\": \"live_probe\", \"command\": \"hyprctl version\", \"file\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl\", \"line\": 1, \"rule\": \"hyprctl:version\", \"timestamp\": \"2026-10-20T03:10:00.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"call_lp1\"}, {\"argv0\": \"systemctl\", \"class\": \"live_probe\", \"command\": \"systemctl --user status hypridle\", \"file\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/live-probe.jsonl\", \"line\": 3, \"rule\": \"systemctl:status\", \"timestamp\": \"2026-10-20T03:10:15.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"call_lp2\"}], \"permitted\": [\"live_probe\"], \"schema\": \"mado-tripwire-verdict-v1\", \"unpermitted\": 0}\n",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M309.py",
        "--scan",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/redaction-witness.jsonl"
      ],
      "mutant": "M309",
      "phase": "restored",
      "returncode": 1,
      "stderr": "",
      "stdout": "MADO_TRIPWIRE: findings\n{\"counts\": {\"host_mutation\": 0, \"live_probe\": 1, \"package_query\": 0}, \"exit\": 1, \"files\": [{\"bash_calls\": 1, \"eval_calls\": 0, \"eval_unparsed\": 0, \"lines\": 1, \"path\": \"/tmp/MadoR17-MutateTripwire3.wvd7me0k/redaction-witness.jsonl\", \"sha256\": \"97a3428f256a0b9e6027de76c08369acd212732178c79d9bab9659716d590107\", \"unparsed_spawns\": 0}], \"findings\": [{\"argv0\": \"journalctl\", \"class\": \"live_probe\", \"command\": \"journalctl --unit demo --example-token <redacted>\", \"file\": \"/tmp/MadoR17-MutateTripwire3.wvd7me0k/redaction-witness.jsonl\", \"line\": 1, \"rule\": \"journalctl\", \"timestamp\": \"2026-10-20T00:00:00.000Z\", \"tool\": \"bash\", \"tool_call_id\": \"synthetic-call\"}], \"permitted\": [], \"schema\": \"mado-tripwire-verdict-v1\", \"unpermitted\": 1}\n",
      "timed_out": false
    },
    {
      "command": [
        "python3",
        "-I",
        "/tmp/MadoR17-MutateTripwire3.wvd7me0k/M310.py",
        "--scan",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening/eval-nonliteral-unparsed-clean.jsonl"
      ],
      "mutant": "M310",
      "phase": "restored",
      "returncode": 0,
      "stderr": "",
      "stdout": "MADO_TRIPWIRE: clean\n{\"counts\": {\"host_mutation\": 0, \"live_probe\": 0, \"package_query\": 0}, \"exit\": 0, \"files\": [{\"bash_calls\": 0, \"eval_calls\": 1, \"eval_unparsed\": 0, \"lines\": 1, \"path\": \"/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening/eval-nonliteral-unparsed-clean.jsonl\", \"sha256\": \"9ec45f2adbe9547a7ab7b89ae35fe13b7de2069837aee862c3d2a6feab348aa0\", \"unparsed_spawns\": 1}], \"findings\": [], \"permitted\": [], \"schema\": \"mado-tripwire-verdict-v1\", \"unpermitted\": 0}\n",
      "timed_out": false
    }
  ]
}
```

</details>

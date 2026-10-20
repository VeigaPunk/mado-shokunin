# MutateTripwire2 — round 17, wave 2
## Result

**8 independent one-line mutants: 4 killed, 4 survived, 0 inconclusive.** Every mutant was confined to the assigned middle third of a separate `/tmp` copy. The required pristine and restored runs both passed **9/9 core, 16/16 compound, 33/33 hardening** for every copy. Survivors are coverage findings against these three suites, not evidence that the contract should be weakened or that the corresponding defect exists in the restored lane code.
## Axes and scope

- **Regression sensitivity:** distinguish meaningful classification/parser defects, rather than mere script crashes.
- **Baseline legitimacy:** require the same detector to pass before mutation and after exact restoration.
- **Isolation/restorability:** change one behavior-bearing line per private scratch copy and restore identical bytes.
- **Bounded reproducibility:** use only the existing three suites plus inert JSONL witnesses, with captured commands, stdout, stderr, exits, and hashes.
Target: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`. The task identified lane HEAD `988b858bd6049bc709807534fd725c05264f7e60`; this report identifies the actual source bytes by SHA-256, without invoking git. `wc -l` returned **818**. Partition rule: third k is `floor((k-1)*818/3)+1 .. floor(k*818/3)`; therefore this probe owns **lines 273–545 inclusive**. All eight changed lines lie inside that interval.

Scratch root: `/tmp/mado-r17-mutatetripwire2-bv2pk1ng`. Copied script for mutant `Mxx`: `/tmp/mado-r17-mutatetripwire2-bv2pk1ng/Mxx/mado-tripwire.py`. No source, fixture, expected.json, or sibling report in the lane was edited. The only lane file written is this report.
## Detector and bounded execution

For each M01–M08, on **pristine → mutated → restored** bytes, the exact detector command shape was:

```text
python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/Mxx/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core
python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/Mxx/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound
python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/Mxx/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening
```

Thus **72 selftest invocations / 1,392 case comparisons** were exercised. At most six suite invocations were active concurrently. Each suite invocation had a 120-second outer timeout; the existing selftest harness also bounds each child scan by 120 seconds. No timeout occurred. All captured stderr streams were empty. The unchanged harness uses its own copied `__file__` at source lines 739–743, so its child scans also ran the copied script, not the lane script.

For surviving mutants only, one separate JSONL witness was scanned on pristine, mutated, and restored bytes (`python3 -I <copied-script> --scan <private-witness.jsonl>`, 30-second timeout). These witness scans demonstrate non-equivalence; they were not added to or substituted for the required suites. Commands embedded inside these transcripts were **data only**, never executed.
### Suite results

Each cell is `passing cases / total (selftest process exit)`. `P` = pristine; `M` = mutated; `R` = restored.

| Mutant / original source line | Core P → M → R | Compound P → M → R | Hardening P → M → R | Verdict |
|---|---|---|---|---|
| M01 / `tools/mado-tripwire.py:296` | 9/9 (0) → 9/9 (0) → 9/9 (0) | 16/16 (0) → 16/16 (0) → 16/16 (0) | 33/33 (0) → 33/33 (0) → 33/33 (0) | **survived** |
| M02 / `tools/mado-tripwire.py:321` | 9/9 (0) → 8/9 (1) → 9/9 (0) | 16/16 (0) → 16/16 (0) → 16/16 (0) | 33/33 (0) → 33/33 (0) → 33/33 (0) | **killed** |
| M03 / `tools/mado-tripwire.py:326` | 9/9 (0) → 9/9 (0) → 9/9 (0) | 16/16 (0) → 16/16 (0) → 16/16 (0) | 33/33 (0) → 33/33 (0) → 33/33 (0) | **survived** |
| M04 / `tools/mado-tripwire.py:358` | 9/9 (0) → 9/9 (0) → 9/9 (0) | 16/16 (0) → 16/16 (0) → 16/16 (0) | 33/33 (0) → 32/33 (1) → 33/33 (0) | **killed** |
| M05 / `tools/mado-tripwire.py:463` | 9/9 (0) → 9/9 (0) → 9/9 (0) | 16/16 (0) → 16/16 (0) → 16/16 (0) | 33/33 (0) → 32/33 (1) → 33/33 (0) | **killed** |
| M06 / `tools/mado-tripwire.py:443` | 9/9 (0) → 9/9 (0) → 9/9 (0) | 16/16 (0) → 13/16 (1) → 16/16 (0) | 33/33 (0) → 30/33 (1) → 33/33 (0) | **killed** |
| M07 / `tools/mado-tripwire.py:495` | 9/9 (0) → 9/9 (0) → 9/9 (0) | 16/16 (0) → 16/16 (0) → 16/16 (0) | 33/33 (0) → 33/33 (0) → 33/33 (0) | **survived** |
| M08 / `tools/mado-tripwire.py:529` | 9/9 (0) → 9/9 (0) → 9/9 (0) | 16/16 (0) → 16/16 (0) → 16/16 (0) | 33/33 (0) → 33/33 (0) → 33/33 (0) | **survived** |

### Mutants and expected detectors

- **M01 — long-query operation misclassified as sync** (`tools/mado-tripwire.py:296`). Expected detector: Preserve package_query for the long --query operation, including the pacman:--query rule. Verdict: **survived**.

- **M02 — files operation omitted from query classes** (`tools/mado-tripwire.py:321`). Expected detector: Preserve package_query for the files operation (-F/-Fl); core/package-query-only already asserts it. Verdict: **killed**.

- **M03 — download flag loses mutation precedence** (`tools/mado-tripwire.py:326`). Expected detector: Preserve the landed classifier’s download-flag precedence when query/print flags are also present; this tests that classification contract, not actual package-manager side effects. Verdict: **survived**.

- **M04 — command-substitution traversal disabled** (`tools/mado-tripwire.py:358`). Expected detector: Retain recursive command-substitution classification, including substitution inside double-quoted data. Verdict: **killed**.

- **M05 — kill-zero exception removed** (`tools/mado-tripwire.py:463`). Expected detector: Keep kill -0 clean; the hardening kill-zero-clean case must reject the false host_mutation. Verdict: **killed**.

- **M06 — systemctl mutations downgraded to probes** (`tools/mado-tripwire.py:443`). Expected detector: Keep mutating systemctl verbs host_mutation rather than live_probe, even when both classifications yield scan exit 1. Verdict: **killed**.

- **M07 — literal tuple argv no longer accepted** (`tools/mado-tripwire.py:495`). Expected detector: Keep literal tuple argv equivalent to literal list argv for subprocess classification. Verdict: **survived**.

- **M08 — from-subprocess import aliases ignored** (`tools/mado-tripwire.py:529`). Expected detector: Keep supported from-subprocess aliases registered under the local alias, not only the imported original name. Verdict: **survived**.

## Killed-mutant evidence

These are detector rejections of valid, runnable mutants, not baseline failures or parser crashes. Paths below are relative to `.ufo/waves/round-17/tripwire/`.

- **M02:** `core/package-queries.jsonl:3` changed `pacman:-Fl` from `package_query` to `host_mutation`; `core/expected.json:40-44` asserts the original class.
- **M04:** `hardening/dollar-paren-in-double-quotes.jsonl:1` (`echo "v=$(pacman -Q waybar)"`) lost its package-query finding and changed scan exit **1 → 0**. The compound suite still passed after substitution traversal was disabled; its unquoted command-substitution case alone did not distinguish this regression.
- **M05:** `hardening/kill-zero-clean.jsonl:1` (`kill -0 1234 && kill -l`) gained a false `host_mutation/kill` and changed scan exit **0 → 1**.
- **M06:** `compound/bash-c-subshell.jsonl:2`, `compound/user-daemon-reload.jsonl:2`, `hardening/heredoc-into-shell.jsonl:1`, `hardening/eval-tool-bash.jsonl:1`, and `hardening/systemctl-suspend.jsonl:1` emitted `live_probe` in place of `host_mutation`; the compound directory aggregate failed as well. Existing checks compared classes and killed the defect even when the scan exit remained 1.

Actual failing-case stdout (unabridged):

### M02 / core — process exit 1

```text
CASE package-query-only FAIL want=(1, [('package_query', 'pacman:-Fl', 3, ''), ('package_query', 'pacman:-Qi', 1, ''), ('package_query', 'pacman:-Si', 2, ''), ('package_query', 'pacman:-Sp', 4, '')]) got=(1, [('host_mutation', 'pacman:-Fl', 3, ''), ('package_query', 'pacman:-Qi', 1, ''), ('package_query', 'pacman:-Si', 2, ''), ('package_query', 'pacman:-Sp', 4, '')])
SELFTEST_SCRIPT_SHA256: f58a7cb066939d40fe6190c20de857cb72aec7d1b92d88c605c6e5899290275f
SELFTEST_SUMMARY: 8/9 passed failed=['package-query-only']
```

### M04 / hardening — process exit 1

```text
CASE dollar-paren-in-double-quotes FAIL want=(1, [('package_query', 'pacman:-Q', 1, '')]) got=(0, [])
SELFTEST_SCRIPT_SHA256: 4b0ac1155b5445e0576dad2f5ba43f7d5ca2205324fb55432f04997065462da3
SELFTEST_SUMMARY: 32/33 passed failed=['dollar-paren-in-double-quotes']
```

### M05 / hardening — process exit 1

```text
CASE kill-zero-clean FAIL want=(0, []) got=(1, [('host_mutation', 'kill', 1, '')])
SELFTEST_SCRIPT_SHA256: 2dc0009eecee94d508522814f4a11924182a6dd5023a2a3781e60789418f021b
SELFTEST_SUMMARY: 32/33 passed failed=['kill-zero-clean']
```

### M06 / compound — process exit 1

```text
CASE bash-c-sudo-systemctl-restart FAIL want=(1, [('host_mutation', 'sudo', 2, 'bash-c-subshell.jsonl'), ('host_mutation', 'systemctl:restart', 2, 'bash-c-subshell.jsonl')]) got=(1, [('host_mutation', 'sudo', 2, 'bash-c-subshell.jsonl'), ('live_probe', 'systemctl:restart', 2, 'bash-c-subshell.jsonl')])
CASE user-daemon-reload FAIL want=(1, [('host_mutation', 'systemctl:daemon-reload', 2, 'user-daemon-reload.jsonl')]) got=(1, [('live_probe', 'systemctl:daemon-reload', 2, 'user-daemon-reload.jsonl')])
CASE dir-scan-all-permitted FAIL want=(0, [('host_mutation', 'hyprctl:dispatch', 2, 'wrappers-hyprctl.jsonl'), ('host_mutation', 'hyprctl:keyword', 4, 'wrappers-hyprctl.jsonl'), ('host_mutation', 'omarchy-restart-waybar', 2, 'omarchy-verbs.jsonl'), ('host_mutation', 'omarchy-theme-set', 4, 'omarchy-verbs.jsonl'), ('host_mutation', 'pacman:-R', 2, 'env-prefix.jsonl'), ('host_mutation', 'pacman:-S', 2, 'eval-bang.jsonl'), ('host_mutation', 'pacman:-Syu', 2, 'compound-and.jsonl'), ('host_mutation', 'pacman:-U', 2, 'abs-path-pacman.jsonl'), ('host_mutation', 'pkill', 2, 'xargs-pkill.jsonl'), ('host_mutation', 'sudo', 2, 'bash-c-subshell.jsonl'), ('host_mutation', 'sudo', 2, 'compound-and.jsonl'), ('host_mutation', 'sudo', 2, 'eval-bang.jsonl'), ('host_mutation', 'systemctl:daemon-reload', 2, 'user-daemon-reload.jsonl'), ('host_mutation', 'systemctl:restart', 2, 'bash-c-subshell.jsonl'), ('package_query', 'pacman:-Q', 2, 'var-assign-query.jsonl'), ('package_query', 'pacman:-Qq', 2, 'cmdsub-query.jsonl')]) got=(0, [('host_mutation', 'hyprctl:dispatch', 2, 'wrappers-hyprctl.jsonl'), ('host_mutation', 'hyprctl:keyword', 4, 'wrappers-hyprctl.jsonl'), ('host_mutation', 'omarchy-restart-waybar', 2, 'omarchy-verbs.jsonl'), ('host_mutation', 'omarchy-theme-set', 4, 'omarchy-verbs.jsonl'), ('host_mutation', 'pacman:-R', 2, 'env-prefix.jsonl'), ('host_mutation', 'pacman:-S', 2, 'eval-bang.jsonl'), ('host_mutation', 'pacman:-Syu', 2, 'compound-and.jsonl'), ('host_mutation', 'pacman:-U', 2, 'abs-path-pacman.jsonl'), ('host_mutation', 'pkill', 2, 'xargs-pkill.jsonl'), ('host_mutation', 'sudo', 2, 'bash-c-subshell.jsonl'), ('host_mutation', 'sudo', 2, 'compound-and.jsonl'), ('host_mutation', 'sudo', 2, 'eval-bang.jsonl'), ('live_probe', 'systemctl:daemon-reload', 2, 'user-daemon-reload.jsonl'), ('live_probe', 'systemctl:restart', 2, 'bash-c-subshell.jsonl'), ('package_query', 'pacman:-Q', 2, 'var-assign-query.jsonl'), ('package_query', 'pacman:-Qq', 2, 'cmdsub-query.jsonl')])
SELFTEST_SCRIPT_SHA256: 2da871068149c2acaaf57ff99544868a5f40bd10a79b57f6b2a467d2188ca40a
SELFTEST_SUMMARY: 13/16 passed failed=['bash-c-sudo-systemctl-restart', 'user-daemon-reload', 'dir-scan-all-permitted']
```

### M06 / hardening — process exit 1

```text
CASE heredoc-into-shell FAIL want=(1, [('host_mutation', 'systemctl:restart', 1, '')]) got=(1, [('live_probe', 'systemctl:restart', 1, '')])
CASE eval-tool-bash FAIL want=(1, [('host_mutation', 'sudo', 1, ''), ('host_mutation', 'systemctl:restart', 1, '')]) got=(1, [('host_mutation', 'sudo', 1, ''), ('live_probe', 'systemctl:restart', 1, '')])
CASE systemctl-suspend FAIL want=(1, [('host_mutation', 'systemctl:suspend', 1, '')]) got=(1, [('live_probe', 'systemctl:suspend', 1, '')])
SELFTEST_SCRIPT_SHA256: 2da871068149c2acaaf57ff99544868a5f40bd10a79b57f6b2a467d2188ca40a
SELFTEST_SUMMARY: 30/33 passed failed=['heredoc-into-shell', 'eval-tool-bash', 'systemctl-suspend']
```

## Surviving-mutant diffs and counterexamples

Each survivor passed all **58/58** required cases after mutation. The diffs below were captured while the mutant bytes were present; all copies have since been restored. A witness row shows the same inert input scanned in each phase.

### M01 — survived

The suites did not distinguish a wrong long --query mapping. The witness kept exit 1 but changed the finding class from package_query to host_mutation.

```diff
--- pristine/tools/mado-tripwire.py
+++ M01/tools/mado-tripwire.py
@@ -294,5 +294,5 @@
     for a in args:
         if a.startswith("--"):
-            long_ops = {"--sync": "S", "--query": "Q", "--remove": "R",
+            long_ops = {"--sync": "S", "--query": "S", "--remove": "R",
                         "--upgrade": "U", "--database": "D", "--files": "F",
                         "--deptest": "T", "--version": "V"}
```

Witness: `/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M01/witness.jsonl:1`, toolCall ID `witness-M01`, tool `bash`. Payload:

```text
pacman --query hyprland
```

| Phase | Scan exit | Finding(s) | unparsed_spawns |
|---|---|---|---|
| pristine | 1 | `package_query / pacman:--query / line 1 / witness-M01` | 0 |
| mutated | 1 | `host_mutation / pacman:--query / line 1 / witness-M01` | 0 |
| restored | 1 | `package_query / pacman:--query / line 1 / witness-M01` | 0 |

Witness SHA-256 (same input in all three phases): `b2f18cbeb3974bf4719cc90e7e97c00201d17998e2c07d5ec01a126e95f6ef72`.

### M03 — survived

The suites did not distinguish loss of w precedence in a mixed-flag input. The ordinary -Sw hardening case stayed green because the later fallback still returned host_mutation; adding p exposed the class change. This is an observation about the landed classifier’s precedence, not a claim that this data-only command performs a host write.

```diff
--- pristine/tools/mado-tripwire.py
+++ M03/tools/mado-tripwire.py
@@ -324,5 +324,5 @@
         return ("host_mutation", rule)
     if letter == "S":
-        if flags & set("yuwc"):
+        if flags & set("yuc"):
             return ("host_mutation", rule)
         if flags & set("silgp"):
```

Witness: `/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M03/witness.jsonl:1`, toolCall ID `witness-M03`, tool `bash`. Payload:

```text
pacman -Swp hyprland
```

| Phase | Scan exit | Finding(s) | unparsed_spawns |
|---|---|---|---|
| pristine | 1 | `host_mutation / pacman:-Swp / line 1 / witness-M03` | 0 |
| mutated | 1 | `package_query / pacman:-Swp / line 1 / witness-M03` | 0 |
| restored | 1 | `host_mutation / pacman:-Swp / line 1 / witness-M03` | 0 |

Witness SHA-256 (same input in all three phases): `fb673bf418966f267e077393ac3faf18e88d28c57ca95332bbe98296a7d1d4da`.

### M07 — survived

Literal tuple argv support was lost. The witness became clean (exit 0), with unparsed_spawns increasing from 0 to 1; list-only coverage did not reject the regression.

```diff
--- pristine/tools/mado-tripwire.py
+++ M07/tools/mado-tripwire.py
@@ -493,5 +493,5 @@
 
 def str_list(node):
-    if isinstance(node, (ast.List, ast.Tuple)) and node.elts and all(
+    if isinstance(node, (ast.List,)) and node.elts and all(
             isinstance(e, ast.Constant) and isinstance(e.value, str) for e in node.elts):
         return [e.value for e in node.elts]
```

Witness: `/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M07/witness.jsonl:1`, toolCall ID `witness-M07`, tool `eval/py`. Payload:

```text
import subprocess
subprocess.run(('pacman', '-Q', 'hyprland'))
```

| Phase | Scan exit | Finding(s) | unparsed_spawns |
|---|---|---|---|
| pristine | 1 | `package_query / pacman:-Q / line 1 / witness-M07` | 0 |
| mutated | 0 | `[]` | 1 |
| restored | 1 | `package_query / pacman:-Q / line 1 / witness-M07` | 0 |

Witness SHA-256 (same input in all three phases): `91e693eb1d1f9cd0308c1f9d564e3499efcb21616bb4c5e055fabfa4a1299a07`.

### M08 — survived

The local alias call is a supported SPAWN_FUNCS name in the pristine implementation. Ignoring the alias made this literal spawn disappear without even incrementing unparsed_spawns; the witness became clean (exit 0).

```diff
--- pristine/tools/mado-tripwire.py
+++ M08/tools/mado-tripwire.py
@@ -527,5 +527,5 @@
     for node in ast.walk(tree):
         if isinstance(node, ast.ImportFrom) and node.module == "subprocess":
-            from_subprocess.update(a.asname or a.name for a in node.names)
+            from_subprocess.update(a.name for a in node.names)
     unparsed = 0
     for node in ast.walk(tree):
```

Witness: `/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M08/witness.jsonl:1`, toolCall ID `witness-M08`, tool `eval/py`. Payload:

```text
from subprocess import run as call
call(['pacman', '-Q', 'hyprland'])
```

| Phase | Scan exit | Finding(s) | unparsed_spawns |
|---|---|---|---|
| pristine | 1 | `package_query / pacman:-Q / line 1 / witness-M08` | 0 |
| mutated | 0 | `[]` | 0 |
| restored | 1 | `package_query / pacman:-Q / line 1 / witness-M08` | 0 |

Witness SHA-256 (same input in all three phases): `a755834e2a8631e6328d873e254a02d9e6bd52305dc216e866e09a40ad987f64`.

## Unscored pristine observation / rejected witness

An initial M08 witness used `from subprocess import run as invoke; invoke([...])`. **Pristine already returned exit 0, no findings, and unparsed_spawns=0.** It was therefore unsuitable for attributing a regression to M08 and was not counted as a killed mutant. The scored witness was corrected to the supported alias `call` before mutation, its pristine output was captured, and the exact corrected input was reused in mutated and restored phases.

The original alias case is a separate concrete observation on pristine source: line 529 stores the alias, but line 537 additionally requires that alias to be in SPAWN_FUNCS. An arbitrary alias such as `invoke` therefore falls through. This report does not change that contract or patch this behavior. The initial witness input was:

```json
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"witness-M08","name":"eval","arguments":{"language":"py","code":"from subprocess import run as invoke\ninvoke(['pacman', '-Q', 'hyprland'])"}}]}}
```

Actual initial pristine stdout:

```text
MADO_TRIPWIRE: clean
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M08/witness.jsonl", "sha256": "ceb11ed82002bc9d623cbb6aabab9c3b1c73ed0ef7b2d27337d1df0252d4bbf8", "unparsed_spawns": 0}], "findings": [], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
```

## Hashes and restoration

Initial lane source, pristine scratch source, **all eight before-mutation copies**, **all eight restored copies**, and final lane source SHA-256:

```text
4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
```

All eight restored scripts were also compared byte-for-byte with the saved pristine file and returned `True`. The final lane-source hash was `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44` (unchanged). Every restored selftest emitted `SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44` and passed all three suites.

| Mutant | SHA-256 while mutated | Restored exact bytes |
|---|---|---|
| M01 | `466794b2ef7b769558b87f9b4b8d47b34f553f415ce37c212a768007018fc9fb` | `True` |
| M02 | `f58a7cb066939d40fe6190c20de857cb72aec7d1b92d88c605c6e5899290275f` | `True` |
| M03 | `736864ed2b9695c25ed486e382310fdddda696c9fcdff7a0505b210e81550f11` | `True` |
| M04 | `4b0ac1155b5445e0576dad2f5ba43f7d5ca2205324fb55432f04997065462da3` | `True` |
| M05 | `2dc0009eecee94d508522814f4a11924182a6dd5023a2a3781e60789418f021b` | `True` |
| M06 | `2da871068149c2acaaf57ff99544868a5f40bd10a79b57f6b2a467d2188ca40a` | `True` |
| M07 | `0cb53e5db261c8a5ad8244572665dba57a427cd912cdf34af2f0fff9212386b0` | `True` |
| M08 | `17bf367bcac38047fa5d92c3269ee45d453751a98dbedcb58703432877d0260e` | `True` |

Suite expectation SHA-256 at receipt capture:

| Suite expected.json | SHA-256 |
|---|---|
| core | `e8aff6efb9ce06eefac457d8dc8afa79405f2167c426f2c23900bc314b06b920` |
| compound | `eef778eac31181f9c76519ff7a0b01c368e2f5255c12791e13c0f0fc7ce065e2` |
| hardening | `0f6d4b3031dcfcc8c23e7d3391f166394eaf31813834598d09bc554f46f5d77f` |

## Operational bounds

- Installs/updates: **none**.
- No sudo, package-manager command, service/compositor/input probe, credential/database read, OMP CLI, another runtime, git/jj operation, commit, integration, or shipment was performed. Package-manager/systemctl/kill strings shown above were only classified as transcript data.
- Mutants were applied and reverted with surgical edits only on this probe’s private `/tmp` copies. The lane source and pre-existing fixtures were only read.
- No subagents were dispatched.
- A tool-output issue was reported: eval suppresses worker-thread print output. Stored worker results were replayed on the main thread; commands were not rerun to compensate, and the receipts below are the captured subprocess streams.
- No fixture, contract, or production fix was integrated. The assigned mutation probe is complete.

## Full subprocess receipts

The following retained outputs make this single report self-contained; no separate lane evidence files were written.

<details>
<summary>M01: pristine, mutated, and restored suite stdout/stderr</summary>

### pristine / core

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M01/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE incident-replica ok
CASE package-query-only ok
CASE live-probe-only ok
CASE live-probe-permitted ok
CASE clean-reads ok
CASE mention-only ok
CASE malformed-json-line ok
CASE no-jsonl-dir ok
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 9/9 passed failed=[]
```

Stderr: `<empty>`.

### pristine / compound

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M01/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE compound-and-sudo-pacman ok
CASE abs-path-pacman-upgrade ok
CASE env-prefix-pacman-remove ok
CASE var-assign-pacman-query ok
CASE var-assign-pacman-query-permitted ok
CASE bash-c-sudo-systemctl-restart ok
CASE cmdsub-pacman-query ok
CASE timeout-nohup-hyprctl-mutations ok
CASE xargs-pkill ok
CASE quoted-data-clean ok
CASE eval-bang-sudo-pacman ok
CASE eval-nonbang-clean ok
CASE user-daemon-reload ok
CASE omarchy-mutating-verbs ok
CASE omarchy-permitted ok
CASE dir-scan-all-permitted ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 16/16 passed failed=[]
```

Stderr: `<empty>`.

### pristine / hardening

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M01/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE newline-second-line ok
CASE backslash-continuation ok
CASE heredoc-data-clean ok
CASE heredoc-into-shell ok
CASE multiline-quoted-commit-clean ok
CASE multi-toolcall-line ok
CASE eval-subprocess-list ok
CASE eval-bash-c-recipe ok
CASE eval-shell-true ok
CASE eval-tool-bash ok
CASE eval-nonliteral-unparsed-clean ok
CASE eval-js-unparsed-clean ok
CASE kill-zero-clean ok
CASE kill-term ok
CASE systemctl-suspend ok
CASE loginctl-lock ok
CASE loginctl-show-probe ok
CASE omarchy-quoted-grep-clean ok
CASE omarchy-bare-launch ok
CASE result-and-marker-only-clean ok
CASE pacman-sync-print-query ok
CASE pacman-downloadonly-mutation ok
CASE run0-and-systemd-run ok
CASE hyprctl-batch ok
CASE dollar-paren-in-double-quotes ok
CASE pacman-log-read-clean ok
CASE refused-db-name ok
CASE seat-name-with-credential-word-allowed ok
CASE refused-symlink ok
CASE command-v-lookup-clean ok
CASE python-heredoc-spawn ok
CASE python-heredoc-data-clean ok
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 33/33 passed failed=[]
```

Stderr: `<empty>`.

### mutated / core

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M01/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core`

Process exit: `0`; copied-script SHA-256: `466794b2ef7b769558b87f9b4b8d47b34f553f415ce37c212a768007018fc9fb`.

```text
CASE incident-replica ok
CASE package-query-only ok
CASE live-probe-only ok
CASE live-probe-permitted ok
CASE clean-reads ok
CASE mention-only ok
CASE malformed-json-line ok
CASE no-jsonl-dir ok
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: 466794b2ef7b769558b87f9b4b8d47b34f553f415ce37c212a768007018fc9fb
SELFTEST_SUMMARY: 9/9 passed failed=[]
```

Stderr: `<empty>`.

### mutated / compound

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M01/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound`

Process exit: `0`; copied-script SHA-256: `466794b2ef7b769558b87f9b4b8d47b34f553f415ce37c212a768007018fc9fb`.

```text
CASE compound-and-sudo-pacman ok
CASE abs-path-pacman-upgrade ok
CASE env-prefix-pacman-remove ok
CASE var-assign-pacman-query ok
CASE var-assign-pacman-query-permitted ok
CASE bash-c-sudo-systemctl-restart ok
CASE cmdsub-pacman-query ok
CASE timeout-nohup-hyprctl-mutations ok
CASE xargs-pkill ok
CASE quoted-data-clean ok
CASE eval-bang-sudo-pacman ok
CASE eval-nonbang-clean ok
CASE user-daemon-reload ok
CASE omarchy-mutating-verbs ok
CASE omarchy-permitted ok
CASE dir-scan-all-permitted ok
SELFTEST_SCRIPT_SHA256: 466794b2ef7b769558b87f9b4b8d47b34f553f415ce37c212a768007018fc9fb
SELFTEST_SUMMARY: 16/16 passed failed=[]
```

Stderr: `<empty>`.

### mutated / hardening

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M01/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening`

Process exit: `0`; copied-script SHA-256: `466794b2ef7b769558b87f9b4b8d47b34f553f415ce37c212a768007018fc9fb`.

```text
CASE newline-second-line ok
CASE backslash-continuation ok
CASE heredoc-data-clean ok
CASE heredoc-into-shell ok
CASE multiline-quoted-commit-clean ok
CASE multi-toolcall-line ok
CASE eval-subprocess-list ok
CASE eval-bash-c-recipe ok
CASE eval-shell-true ok
CASE eval-tool-bash ok
CASE eval-nonliteral-unparsed-clean ok
CASE eval-js-unparsed-clean ok
CASE kill-zero-clean ok
CASE kill-term ok
CASE systemctl-suspend ok
CASE loginctl-lock ok
CASE loginctl-show-probe ok
CASE omarchy-quoted-grep-clean ok
CASE omarchy-bare-launch ok
CASE result-and-marker-only-clean ok
CASE pacman-sync-print-query ok
CASE pacman-downloadonly-mutation ok
CASE run0-and-systemd-run ok
CASE hyprctl-batch ok
CASE dollar-paren-in-double-quotes ok
CASE pacman-log-read-clean ok
CASE refused-db-name ok
CASE seat-name-with-credential-word-allowed ok
CASE refused-symlink ok
CASE command-v-lookup-clean ok
CASE python-heredoc-spawn ok
CASE python-heredoc-data-clean ok
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: 466794b2ef7b769558b87f9b4b8d47b34f553f415ce37c212a768007018fc9fb
SELFTEST_SUMMARY: 33/33 passed failed=[]
```

Stderr: `<empty>`.

### restored / core

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M01/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE incident-replica ok
CASE package-query-only ok
CASE live-probe-only ok
CASE live-probe-permitted ok
CASE clean-reads ok
CASE mention-only ok
CASE malformed-json-line ok
CASE no-jsonl-dir ok
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 9/9 passed failed=[]
```

Stderr: `<empty>`.

### restored / compound

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M01/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE compound-and-sudo-pacman ok
CASE abs-path-pacman-upgrade ok
CASE env-prefix-pacman-remove ok
CASE var-assign-pacman-query ok
CASE var-assign-pacman-query-permitted ok
CASE bash-c-sudo-systemctl-restart ok
CASE cmdsub-pacman-query ok
CASE timeout-nohup-hyprctl-mutations ok
CASE xargs-pkill ok
CASE quoted-data-clean ok
CASE eval-bang-sudo-pacman ok
CASE eval-nonbang-clean ok
CASE user-daemon-reload ok
CASE omarchy-mutating-verbs ok
CASE omarchy-permitted ok
CASE dir-scan-all-permitted ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 16/16 passed failed=[]
```

Stderr: `<empty>`.

### restored / hardening

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M01/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE newline-second-line ok
CASE backslash-continuation ok
CASE heredoc-data-clean ok
CASE heredoc-into-shell ok
CASE multiline-quoted-commit-clean ok
CASE multi-toolcall-line ok
CASE eval-subprocess-list ok
CASE eval-bash-c-recipe ok
CASE eval-shell-true ok
CASE eval-tool-bash ok
CASE eval-nonliteral-unparsed-clean ok
CASE eval-js-unparsed-clean ok
CASE kill-zero-clean ok
CASE kill-term ok
CASE systemctl-suspend ok
CASE loginctl-lock ok
CASE loginctl-show-probe ok
CASE omarchy-quoted-grep-clean ok
CASE omarchy-bare-launch ok
CASE result-and-marker-only-clean ok
CASE pacman-sync-print-query ok
CASE pacman-downloadonly-mutation ok
CASE run0-and-systemd-run ok
CASE hyprctl-batch ok
CASE dollar-paren-in-double-quotes ok
CASE pacman-log-read-clean ok
CASE refused-db-name ok
CASE seat-name-with-credential-word-allowed ok
CASE refused-symlink ok
CASE command-v-lookup-clean ok
CASE python-heredoc-spawn ok
CASE python-heredoc-data-clean ok
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 33/33 passed failed=[]
```

Stderr: `<empty>`.

</details>

<details>
<summary>M02: pristine, mutated, and restored suite stdout/stderr</summary>

### pristine / core

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M02/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE incident-replica ok
CASE package-query-only ok
CASE live-probe-only ok
CASE live-probe-permitted ok
CASE clean-reads ok
CASE mention-only ok
CASE malformed-json-line ok
CASE no-jsonl-dir ok
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 9/9 passed failed=[]
```

Stderr: `<empty>`.

### pristine / compound

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M02/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE compound-and-sudo-pacman ok
CASE abs-path-pacman-upgrade ok
CASE env-prefix-pacman-remove ok
CASE var-assign-pacman-query ok
CASE var-assign-pacman-query-permitted ok
CASE bash-c-sudo-systemctl-restart ok
CASE cmdsub-pacman-query ok
CASE timeout-nohup-hyprctl-mutations ok
CASE xargs-pkill ok
CASE quoted-data-clean ok
CASE eval-bang-sudo-pacman ok
CASE eval-nonbang-clean ok
CASE user-daemon-reload ok
CASE omarchy-mutating-verbs ok
CASE omarchy-permitted ok
CASE dir-scan-all-permitted ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 16/16 passed failed=[]
```

Stderr: `<empty>`.

### pristine / hardening

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M02/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE newline-second-line ok
CASE backslash-continuation ok
CASE heredoc-data-clean ok
CASE heredoc-into-shell ok
CASE multiline-quoted-commit-clean ok
CASE multi-toolcall-line ok
CASE eval-subprocess-list ok
CASE eval-bash-c-recipe ok
CASE eval-shell-true ok
CASE eval-tool-bash ok
CASE eval-nonliteral-unparsed-clean ok
CASE eval-js-unparsed-clean ok
CASE kill-zero-clean ok
CASE kill-term ok
CASE systemctl-suspend ok
CASE loginctl-lock ok
CASE loginctl-show-probe ok
CASE omarchy-quoted-grep-clean ok
CASE omarchy-bare-launch ok
CASE result-and-marker-only-clean ok
CASE pacman-sync-print-query ok
CASE pacman-downloadonly-mutation ok
CASE run0-and-systemd-run ok
CASE hyprctl-batch ok
CASE dollar-paren-in-double-quotes ok
CASE pacman-log-read-clean ok
CASE refused-db-name ok
CASE seat-name-with-credential-word-allowed ok
CASE refused-symlink ok
CASE command-v-lookup-clean ok
CASE python-heredoc-spawn ok
CASE python-heredoc-data-clean ok
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 33/33 passed failed=[]
```

Stderr: `<empty>`.

### mutated / core

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M02/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core`

Process exit: `1`; copied-script SHA-256: `f58a7cb066939d40fe6190c20de857cb72aec7d1b92d88c605c6e5899290275f`.

```text
CASE incident-replica ok
CASE package-query-only FAIL want=(1, [('package_query', 'pacman:-Fl', 3, ''), ('package_query', 'pacman:-Qi', 1, ''), ('package_query', 'pacman:-Si', 2, ''), ('package_query', 'pacman:-Sp', 4, '')]) got=(1, [('host_mutation', 'pacman:-Fl', 3, ''), ('package_query', 'pacman:-Qi', 1, ''), ('package_query', 'pacman:-Si', 2, ''), ('package_query', 'pacman:-Sp', 4, '')])
CASE live-probe-only ok
CASE live-probe-permitted ok
CASE clean-reads ok
CASE mention-only ok
CASE malformed-json-line ok
CASE no-jsonl-dir ok
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: f58a7cb066939d40fe6190c20de857cb72aec7d1b92d88c605c6e5899290275f
SELFTEST_SUMMARY: 8/9 passed failed=['package-query-only']
```

Stderr: `<empty>`.

### mutated / compound

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M02/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound`

Process exit: `0`; copied-script SHA-256: `f58a7cb066939d40fe6190c20de857cb72aec7d1b92d88c605c6e5899290275f`.

```text
CASE compound-and-sudo-pacman ok
CASE abs-path-pacman-upgrade ok
CASE env-prefix-pacman-remove ok
CASE var-assign-pacman-query ok
CASE var-assign-pacman-query-permitted ok
CASE bash-c-sudo-systemctl-restart ok
CASE cmdsub-pacman-query ok
CASE timeout-nohup-hyprctl-mutations ok
CASE xargs-pkill ok
CASE quoted-data-clean ok
CASE eval-bang-sudo-pacman ok
CASE eval-nonbang-clean ok
CASE user-daemon-reload ok
CASE omarchy-mutating-verbs ok
CASE omarchy-permitted ok
CASE dir-scan-all-permitted ok
SELFTEST_SCRIPT_SHA256: f58a7cb066939d40fe6190c20de857cb72aec7d1b92d88c605c6e5899290275f
SELFTEST_SUMMARY: 16/16 passed failed=[]
```

Stderr: `<empty>`.

### mutated / hardening

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M02/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening`

Process exit: `0`; copied-script SHA-256: `f58a7cb066939d40fe6190c20de857cb72aec7d1b92d88c605c6e5899290275f`.

```text
CASE newline-second-line ok
CASE backslash-continuation ok
CASE heredoc-data-clean ok
CASE heredoc-into-shell ok
CASE multiline-quoted-commit-clean ok
CASE multi-toolcall-line ok
CASE eval-subprocess-list ok
CASE eval-bash-c-recipe ok
CASE eval-shell-true ok
CASE eval-tool-bash ok
CASE eval-nonliteral-unparsed-clean ok
CASE eval-js-unparsed-clean ok
CASE kill-zero-clean ok
CASE kill-term ok
CASE systemctl-suspend ok
CASE loginctl-lock ok
CASE loginctl-show-probe ok
CASE omarchy-quoted-grep-clean ok
CASE omarchy-bare-launch ok
CASE result-and-marker-only-clean ok
CASE pacman-sync-print-query ok
CASE pacman-downloadonly-mutation ok
CASE run0-and-systemd-run ok
CASE hyprctl-batch ok
CASE dollar-paren-in-double-quotes ok
CASE pacman-log-read-clean ok
CASE refused-db-name ok
CASE seat-name-with-credential-word-allowed ok
CASE refused-symlink ok
CASE command-v-lookup-clean ok
CASE python-heredoc-spawn ok
CASE python-heredoc-data-clean ok
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: f58a7cb066939d40fe6190c20de857cb72aec7d1b92d88c605c6e5899290275f
SELFTEST_SUMMARY: 33/33 passed failed=[]
```

Stderr: `<empty>`.

### restored / core

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M02/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE incident-replica ok
CASE package-query-only ok
CASE live-probe-only ok
CASE live-probe-permitted ok
CASE clean-reads ok
CASE mention-only ok
CASE malformed-json-line ok
CASE no-jsonl-dir ok
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 9/9 passed failed=[]
```

Stderr: `<empty>`.

### restored / compound

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M02/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE compound-and-sudo-pacman ok
CASE abs-path-pacman-upgrade ok
CASE env-prefix-pacman-remove ok
CASE var-assign-pacman-query ok
CASE var-assign-pacman-query-permitted ok
CASE bash-c-sudo-systemctl-restart ok
CASE cmdsub-pacman-query ok
CASE timeout-nohup-hyprctl-mutations ok
CASE xargs-pkill ok
CASE quoted-data-clean ok
CASE eval-bang-sudo-pacman ok
CASE eval-nonbang-clean ok
CASE user-daemon-reload ok
CASE omarchy-mutating-verbs ok
CASE omarchy-permitted ok
CASE dir-scan-all-permitted ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 16/16 passed failed=[]
```

Stderr: `<empty>`.

### restored / hardening

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M02/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE newline-second-line ok
CASE backslash-continuation ok
CASE heredoc-data-clean ok
CASE heredoc-into-shell ok
CASE multiline-quoted-commit-clean ok
CASE multi-toolcall-line ok
CASE eval-subprocess-list ok
CASE eval-bash-c-recipe ok
CASE eval-shell-true ok
CASE eval-tool-bash ok
CASE eval-nonliteral-unparsed-clean ok
CASE eval-js-unparsed-clean ok
CASE kill-zero-clean ok
CASE kill-term ok
CASE systemctl-suspend ok
CASE loginctl-lock ok
CASE loginctl-show-probe ok
CASE omarchy-quoted-grep-clean ok
CASE omarchy-bare-launch ok
CASE result-and-marker-only-clean ok
CASE pacman-sync-print-query ok
CASE pacman-downloadonly-mutation ok
CASE run0-and-systemd-run ok
CASE hyprctl-batch ok
CASE dollar-paren-in-double-quotes ok
CASE pacman-log-read-clean ok
CASE refused-db-name ok
CASE seat-name-with-credential-word-allowed ok
CASE refused-symlink ok
CASE command-v-lookup-clean ok
CASE python-heredoc-spawn ok
CASE python-heredoc-data-clean ok
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 33/33 passed failed=[]
```

Stderr: `<empty>`.

</details>

<details>
<summary>M03: pristine, mutated, and restored suite stdout/stderr</summary>

### pristine / core

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M03/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE incident-replica ok
CASE package-query-only ok
CASE live-probe-only ok
CASE live-probe-permitted ok
CASE clean-reads ok
CASE mention-only ok
CASE malformed-json-line ok
CASE no-jsonl-dir ok
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 9/9 passed failed=[]
```

Stderr: `<empty>`.

### pristine / compound

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M03/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE compound-and-sudo-pacman ok
CASE abs-path-pacman-upgrade ok
CASE env-prefix-pacman-remove ok
CASE var-assign-pacman-query ok
CASE var-assign-pacman-query-permitted ok
CASE bash-c-sudo-systemctl-restart ok
CASE cmdsub-pacman-query ok
CASE timeout-nohup-hyprctl-mutations ok
CASE xargs-pkill ok
CASE quoted-data-clean ok
CASE eval-bang-sudo-pacman ok
CASE eval-nonbang-clean ok
CASE user-daemon-reload ok
CASE omarchy-mutating-verbs ok
CASE omarchy-permitted ok
CASE dir-scan-all-permitted ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 16/16 passed failed=[]
```

Stderr: `<empty>`.

### pristine / hardening

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M03/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE newline-second-line ok
CASE backslash-continuation ok
CASE heredoc-data-clean ok
CASE heredoc-into-shell ok
CASE multiline-quoted-commit-clean ok
CASE multi-toolcall-line ok
CASE eval-subprocess-list ok
CASE eval-bash-c-recipe ok
CASE eval-shell-true ok
CASE eval-tool-bash ok
CASE eval-nonliteral-unparsed-clean ok
CASE eval-js-unparsed-clean ok
CASE kill-zero-clean ok
CASE kill-term ok
CASE systemctl-suspend ok
CASE loginctl-lock ok
CASE loginctl-show-probe ok
CASE omarchy-quoted-grep-clean ok
CASE omarchy-bare-launch ok
CASE result-and-marker-only-clean ok
CASE pacman-sync-print-query ok
CASE pacman-downloadonly-mutation ok
CASE run0-and-systemd-run ok
CASE hyprctl-batch ok
CASE dollar-paren-in-double-quotes ok
CASE pacman-log-read-clean ok
CASE refused-db-name ok
CASE seat-name-with-credential-word-allowed ok
CASE refused-symlink ok
CASE command-v-lookup-clean ok
CASE python-heredoc-spawn ok
CASE python-heredoc-data-clean ok
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 33/33 passed failed=[]
```

Stderr: `<empty>`.

### mutated / core

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M03/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core`

Process exit: `0`; copied-script SHA-256: `736864ed2b9695c25ed486e382310fdddda696c9fcdff7a0505b210e81550f11`.

```text
CASE incident-replica ok
CASE package-query-only ok
CASE live-probe-only ok
CASE live-probe-permitted ok
CASE clean-reads ok
CASE mention-only ok
CASE malformed-json-line ok
CASE no-jsonl-dir ok
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: 736864ed2b9695c25ed486e382310fdddda696c9fcdff7a0505b210e81550f11
SELFTEST_SUMMARY: 9/9 passed failed=[]
```

Stderr: `<empty>`.

### mutated / compound

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M03/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound`

Process exit: `0`; copied-script SHA-256: `736864ed2b9695c25ed486e382310fdddda696c9fcdff7a0505b210e81550f11`.

```text
CASE compound-and-sudo-pacman ok
CASE abs-path-pacman-upgrade ok
CASE env-prefix-pacman-remove ok
CASE var-assign-pacman-query ok
CASE var-assign-pacman-query-permitted ok
CASE bash-c-sudo-systemctl-restart ok
CASE cmdsub-pacman-query ok
CASE timeout-nohup-hyprctl-mutations ok
CASE xargs-pkill ok
CASE quoted-data-clean ok
CASE eval-bang-sudo-pacman ok
CASE eval-nonbang-clean ok
CASE user-daemon-reload ok
CASE omarchy-mutating-verbs ok
CASE omarchy-permitted ok
CASE dir-scan-all-permitted ok
SELFTEST_SCRIPT_SHA256: 736864ed2b9695c25ed486e382310fdddda696c9fcdff7a0505b210e81550f11
SELFTEST_SUMMARY: 16/16 passed failed=[]
```

Stderr: `<empty>`.

### mutated / hardening

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M03/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening`

Process exit: `0`; copied-script SHA-256: `736864ed2b9695c25ed486e382310fdddda696c9fcdff7a0505b210e81550f11`.

```text
CASE newline-second-line ok
CASE backslash-continuation ok
CASE heredoc-data-clean ok
CASE heredoc-into-shell ok
CASE multiline-quoted-commit-clean ok
CASE multi-toolcall-line ok
CASE eval-subprocess-list ok
CASE eval-bash-c-recipe ok
CASE eval-shell-true ok
CASE eval-tool-bash ok
CASE eval-nonliteral-unparsed-clean ok
CASE eval-js-unparsed-clean ok
CASE kill-zero-clean ok
CASE kill-term ok
CASE systemctl-suspend ok
CASE loginctl-lock ok
CASE loginctl-show-probe ok
CASE omarchy-quoted-grep-clean ok
CASE omarchy-bare-launch ok
CASE result-and-marker-only-clean ok
CASE pacman-sync-print-query ok
CASE pacman-downloadonly-mutation ok
CASE run0-and-systemd-run ok
CASE hyprctl-batch ok
CASE dollar-paren-in-double-quotes ok
CASE pacman-log-read-clean ok
CASE refused-db-name ok
CASE seat-name-with-credential-word-allowed ok
CASE refused-symlink ok
CASE command-v-lookup-clean ok
CASE python-heredoc-spawn ok
CASE python-heredoc-data-clean ok
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: 736864ed2b9695c25ed486e382310fdddda696c9fcdff7a0505b210e81550f11
SELFTEST_SUMMARY: 33/33 passed failed=[]
```

Stderr: `<empty>`.

### restored / core

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M03/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE incident-replica ok
CASE package-query-only ok
CASE live-probe-only ok
CASE live-probe-permitted ok
CASE clean-reads ok
CASE mention-only ok
CASE malformed-json-line ok
CASE no-jsonl-dir ok
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 9/9 passed failed=[]
```

Stderr: `<empty>`.

### restored / compound

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M03/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE compound-and-sudo-pacman ok
CASE abs-path-pacman-upgrade ok
CASE env-prefix-pacman-remove ok
CASE var-assign-pacman-query ok
CASE var-assign-pacman-query-permitted ok
CASE bash-c-sudo-systemctl-restart ok
CASE cmdsub-pacman-query ok
CASE timeout-nohup-hyprctl-mutations ok
CASE xargs-pkill ok
CASE quoted-data-clean ok
CASE eval-bang-sudo-pacman ok
CASE eval-nonbang-clean ok
CASE user-daemon-reload ok
CASE omarchy-mutating-verbs ok
CASE omarchy-permitted ok
CASE dir-scan-all-permitted ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 16/16 passed failed=[]
```

Stderr: `<empty>`.

### restored / hardening

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M03/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE newline-second-line ok
CASE backslash-continuation ok
CASE heredoc-data-clean ok
CASE heredoc-into-shell ok
CASE multiline-quoted-commit-clean ok
CASE multi-toolcall-line ok
CASE eval-subprocess-list ok
CASE eval-bash-c-recipe ok
CASE eval-shell-true ok
CASE eval-tool-bash ok
CASE eval-nonliteral-unparsed-clean ok
CASE eval-js-unparsed-clean ok
CASE kill-zero-clean ok
CASE kill-term ok
CASE systemctl-suspend ok
CASE loginctl-lock ok
CASE loginctl-show-probe ok
CASE omarchy-quoted-grep-clean ok
CASE omarchy-bare-launch ok
CASE result-and-marker-only-clean ok
CASE pacman-sync-print-query ok
CASE pacman-downloadonly-mutation ok
CASE run0-and-systemd-run ok
CASE hyprctl-batch ok
CASE dollar-paren-in-double-quotes ok
CASE pacman-log-read-clean ok
CASE refused-db-name ok
CASE seat-name-with-credential-word-allowed ok
CASE refused-symlink ok
CASE command-v-lookup-clean ok
CASE python-heredoc-spawn ok
CASE python-heredoc-data-clean ok
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 33/33 passed failed=[]
```

Stderr: `<empty>`.

</details>

<details>
<summary>M04: pristine, mutated, and restored suite stdout/stderr</summary>

### pristine / core

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M04/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE incident-replica ok
CASE package-query-only ok
CASE live-probe-only ok
CASE live-probe-permitted ok
CASE clean-reads ok
CASE mention-only ok
CASE malformed-json-line ok
CASE no-jsonl-dir ok
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 9/9 passed failed=[]
```

Stderr: `<empty>`.

### pristine / compound

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M04/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE compound-and-sudo-pacman ok
CASE abs-path-pacman-upgrade ok
CASE env-prefix-pacman-remove ok
CASE var-assign-pacman-query ok
CASE var-assign-pacman-query-permitted ok
CASE bash-c-sudo-systemctl-restart ok
CASE cmdsub-pacman-query ok
CASE timeout-nohup-hyprctl-mutations ok
CASE xargs-pkill ok
CASE quoted-data-clean ok
CASE eval-bang-sudo-pacman ok
CASE eval-nonbang-clean ok
CASE user-daemon-reload ok
CASE omarchy-mutating-verbs ok
CASE omarchy-permitted ok
CASE dir-scan-all-permitted ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 16/16 passed failed=[]
```

Stderr: `<empty>`.

### pristine / hardening

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M04/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE newline-second-line ok
CASE backslash-continuation ok
CASE heredoc-data-clean ok
CASE heredoc-into-shell ok
CASE multiline-quoted-commit-clean ok
CASE multi-toolcall-line ok
CASE eval-subprocess-list ok
CASE eval-bash-c-recipe ok
CASE eval-shell-true ok
CASE eval-tool-bash ok
CASE eval-nonliteral-unparsed-clean ok
CASE eval-js-unparsed-clean ok
CASE kill-zero-clean ok
CASE kill-term ok
CASE systemctl-suspend ok
CASE loginctl-lock ok
CASE loginctl-show-probe ok
CASE omarchy-quoted-grep-clean ok
CASE omarchy-bare-launch ok
CASE result-and-marker-only-clean ok
CASE pacman-sync-print-query ok
CASE pacman-downloadonly-mutation ok
CASE run0-and-systemd-run ok
CASE hyprctl-batch ok
CASE dollar-paren-in-double-quotes ok
CASE pacman-log-read-clean ok
CASE refused-db-name ok
CASE seat-name-with-credential-word-allowed ok
CASE refused-symlink ok
CASE command-v-lookup-clean ok
CASE python-heredoc-spawn ok
CASE python-heredoc-data-clean ok
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 33/33 passed failed=[]
```

Stderr: `<empty>`.

### mutated / core

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M04/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core`

Process exit: `0`; copied-script SHA-256: `4b0ac1155b5445e0576dad2f5ba43f7d5ca2205324fb55432f04997065462da3`.

```text
CASE incident-replica ok
CASE package-query-only ok
CASE live-probe-only ok
CASE live-probe-permitted ok
CASE clean-reads ok
CASE mention-only ok
CASE malformed-json-line ok
CASE no-jsonl-dir ok
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: 4b0ac1155b5445e0576dad2f5ba43f7d5ca2205324fb55432f04997065462da3
SELFTEST_SUMMARY: 9/9 passed failed=[]
```

Stderr: `<empty>`.

### mutated / compound

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M04/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound`

Process exit: `0`; copied-script SHA-256: `4b0ac1155b5445e0576dad2f5ba43f7d5ca2205324fb55432f04997065462da3`.

```text
CASE compound-and-sudo-pacman ok
CASE abs-path-pacman-upgrade ok
CASE env-prefix-pacman-remove ok
CASE var-assign-pacman-query ok
CASE var-assign-pacman-query-permitted ok
CASE bash-c-sudo-systemctl-restart ok
CASE cmdsub-pacman-query ok
CASE timeout-nohup-hyprctl-mutations ok
CASE xargs-pkill ok
CASE quoted-data-clean ok
CASE eval-bang-sudo-pacman ok
CASE eval-nonbang-clean ok
CASE user-daemon-reload ok
CASE omarchy-mutating-verbs ok
CASE omarchy-permitted ok
CASE dir-scan-all-permitted ok
SELFTEST_SCRIPT_SHA256: 4b0ac1155b5445e0576dad2f5ba43f7d5ca2205324fb55432f04997065462da3
SELFTEST_SUMMARY: 16/16 passed failed=[]
```

Stderr: `<empty>`.

### mutated / hardening

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M04/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening`

Process exit: `1`; copied-script SHA-256: `4b0ac1155b5445e0576dad2f5ba43f7d5ca2205324fb55432f04997065462da3`.

```text
CASE newline-second-line ok
CASE backslash-continuation ok
CASE heredoc-data-clean ok
CASE heredoc-into-shell ok
CASE multiline-quoted-commit-clean ok
CASE multi-toolcall-line ok
CASE eval-subprocess-list ok
CASE eval-bash-c-recipe ok
CASE eval-shell-true ok
CASE eval-tool-bash ok
CASE eval-nonliteral-unparsed-clean ok
CASE eval-js-unparsed-clean ok
CASE kill-zero-clean ok
CASE kill-term ok
CASE systemctl-suspend ok
CASE loginctl-lock ok
CASE loginctl-show-probe ok
CASE omarchy-quoted-grep-clean ok
CASE omarchy-bare-launch ok
CASE result-and-marker-only-clean ok
CASE pacman-sync-print-query ok
CASE pacman-downloadonly-mutation ok
CASE run0-and-systemd-run ok
CASE hyprctl-batch ok
CASE dollar-paren-in-double-quotes FAIL want=(1, [('package_query', 'pacman:-Q', 1, '')]) got=(0, [])
CASE pacman-log-read-clean ok
CASE refused-db-name ok
CASE seat-name-with-credential-word-allowed ok
CASE refused-symlink ok
CASE command-v-lookup-clean ok
CASE python-heredoc-spawn ok
CASE python-heredoc-data-clean ok
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: 4b0ac1155b5445e0576dad2f5ba43f7d5ca2205324fb55432f04997065462da3
SELFTEST_SUMMARY: 32/33 passed failed=['dollar-paren-in-double-quotes']
```

Stderr: `<empty>`.

### restored / core

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M04/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE incident-replica ok
CASE package-query-only ok
CASE live-probe-only ok
CASE live-probe-permitted ok
CASE clean-reads ok
CASE mention-only ok
CASE malformed-json-line ok
CASE no-jsonl-dir ok
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 9/9 passed failed=[]
```

Stderr: `<empty>`.

### restored / compound

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M04/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE compound-and-sudo-pacman ok
CASE abs-path-pacman-upgrade ok
CASE env-prefix-pacman-remove ok
CASE var-assign-pacman-query ok
CASE var-assign-pacman-query-permitted ok
CASE bash-c-sudo-systemctl-restart ok
CASE cmdsub-pacman-query ok
CASE timeout-nohup-hyprctl-mutations ok
CASE xargs-pkill ok
CASE quoted-data-clean ok
CASE eval-bang-sudo-pacman ok
CASE eval-nonbang-clean ok
CASE user-daemon-reload ok
CASE omarchy-mutating-verbs ok
CASE omarchy-permitted ok
CASE dir-scan-all-permitted ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 16/16 passed failed=[]
```

Stderr: `<empty>`.

### restored / hardening

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M04/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE newline-second-line ok
CASE backslash-continuation ok
CASE heredoc-data-clean ok
CASE heredoc-into-shell ok
CASE multiline-quoted-commit-clean ok
CASE multi-toolcall-line ok
CASE eval-subprocess-list ok
CASE eval-bash-c-recipe ok
CASE eval-shell-true ok
CASE eval-tool-bash ok
CASE eval-nonliteral-unparsed-clean ok
CASE eval-js-unparsed-clean ok
CASE kill-zero-clean ok
CASE kill-term ok
CASE systemctl-suspend ok
CASE loginctl-lock ok
CASE loginctl-show-probe ok
CASE omarchy-quoted-grep-clean ok
CASE omarchy-bare-launch ok
CASE result-and-marker-only-clean ok
CASE pacman-sync-print-query ok
CASE pacman-downloadonly-mutation ok
CASE run0-and-systemd-run ok
CASE hyprctl-batch ok
CASE dollar-paren-in-double-quotes ok
CASE pacman-log-read-clean ok
CASE refused-db-name ok
CASE seat-name-with-credential-word-allowed ok
CASE refused-symlink ok
CASE command-v-lookup-clean ok
CASE python-heredoc-spawn ok
CASE python-heredoc-data-clean ok
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 33/33 passed failed=[]
```

Stderr: `<empty>`.

</details>

<details>
<summary>M05: pristine, mutated, and restored suite stdout/stderr</summary>

### pristine / core

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M05/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE incident-replica ok
CASE package-query-only ok
CASE live-probe-only ok
CASE live-probe-permitted ok
CASE clean-reads ok
CASE mention-only ok
CASE malformed-json-line ok
CASE no-jsonl-dir ok
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 9/9 passed failed=[]
```

Stderr: `<empty>`.

### pristine / compound

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M05/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE compound-and-sudo-pacman ok
CASE abs-path-pacman-upgrade ok
CASE env-prefix-pacman-remove ok
CASE var-assign-pacman-query ok
CASE var-assign-pacman-query-permitted ok
CASE bash-c-sudo-systemctl-restart ok
CASE cmdsub-pacman-query ok
CASE timeout-nohup-hyprctl-mutations ok
CASE xargs-pkill ok
CASE quoted-data-clean ok
CASE eval-bang-sudo-pacman ok
CASE eval-nonbang-clean ok
CASE user-daemon-reload ok
CASE omarchy-mutating-verbs ok
CASE omarchy-permitted ok
CASE dir-scan-all-permitted ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 16/16 passed failed=[]
```

Stderr: `<empty>`.

### pristine / hardening

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M05/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE newline-second-line ok
CASE backslash-continuation ok
CASE heredoc-data-clean ok
CASE heredoc-into-shell ok
CASE multiline-quoted-commit-clean ok
CASE multi-toolcall-line ok
CASE eval-subprocess-list ok
CASE eval-bash-c-recipe ok
CASE eval-shell-true ok
CASE eval-tool-bash ok
CASE eval-nonliteral-unparsed-clean ok
CASE eval-js-unparsed-clean ok
CASE kill-zero-clean ok
CASE kill-term ok
CASE systemctl-suspend ok
CASE loginctl-lock ok
CASE loginctl-show-probe ok
CASE omarchy-quoted-grep-clean ok
CASE omarchy-bare-launch ok
CASE result-and-marker-only-clean ok
CASE pacman-sync-print-query ok
CASE pacman-downloadonly-mutation ok
CASE run0-and-systemd-run ok
CASE hyprctl-batch ok
CASE dollar-paren-in-double-quotes ok
CASE pacman-log-read-clean ok
CASE refused-db-name ok
CASE seat-name-with-credential-word-allowed ok
CASE refused-symlink ok
CASE command-v-lookup-clean ok
CASE python-heredoc-spawn ok
CASE python-heredoc-data-clean ok
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 33/33 passed failed=[]
```

Stderr: `<empty>`.

### mutated / core

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M05/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core`

Process exit: `0`; copied-script SHA-256: `2dc0009eecee94d508522814f4a11924182a6dd5023a2a3781e60789418f021b`.

```text
CASE incident-replica ok
CASE package-query-only ok
CASE live-probe-only ok
CASE live-probe-permitted ok
CASE clean-reads ok
CASE mention-only ok
CASE malformed-json-line ok
CASE no-jsonl-dir ok
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: 2dc0009eecee94d508522814f4a11924182a6dd5023a2a3781e60789418f021b
SELFTEST_SUMMARY: 9/9 passed failed=[]
```

Stderr: `<empty>`.

### mutated / compound

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M05/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound`

Process exit: `0`; copied-script SHA-256: `2dc0009eecee94d508522814f4a11924182a6dd5023a2a3781e60789418f021b`.

```text
CASE compound-and-sudo-pacman ok
CASE abs-path-pacman-upgrade ok
CASE env-prefix-pacman-remove ok
CASE var-assign-pacman-query ok
CASE var-assign-pacman-query-permitted ok
CASE bash-c-sudo-systemctl-restart ok
CASE cmdsub-pacman-query ok
CASE timeout-nohup-hyprctl-mutations ok
CASE xargs-pkill ok
CASE quoted-data-clean ok
CASE eval-bang-sudo-pacman ok
CASE eval-nonbang-clean ok
CASE user-daemon-reload ok
CASE omarchy-mutating-verbs ok
CASE omarchy-permitted ok
CASE dir-scan-all-permitted ok
SELFTEST_SCRIPT_SHA256: 2dc0009eecee94d508522814f4a11924182a6dd5023a2a3781e60789418f021b
SELFTEST_SUMMARY: 16/16 passed failed=[]
```

Stderr: `<empty>`.

### mutated / hardening

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M05/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening`

Process exit: `1`; copied-script SHA-256: `2dc0009eecee94d508522814f4a11924182a6dd5023a2a3781e60789418f021b`.

```text
CASE newline-second-line ok
CASE backslash-continuation ok
CASE heredoc-data-clean ok
CASE heredoc-into-shell ok
CASE multiline-quoted-commit-clean ok
CASE multi-toolcall-line ok
CASE eval-subprocess-list ok
CASE eval-bash-c-recipe ok
CASE eval-shell-true ok
CASE eval-tool-bash ok
CASE eval-nonliteral-unparsed-clean ok
CASE eval-js-unparsed-clean ok
CASE kill-zero-clean FAIL want=(0, []) got=(1, [('host_mutation', 'kill', 1, '')])
CASE kill-term ok
CASE systemctl-suspend ok
CASE loginctl-lock ok
CASE loginctl-show-probe ok
CASE omarchy-quoted-grep-clean ok
CASE omarchy-bare-launch ok
CASE result-and-marker-only-clean ok
CASE pacman-sync-print-query ok
CASE pacman-downloadonly-mutation ok
CASE run0-and-systemd-run ok
CASE hyprctl-batch ok
CASE dollar-paren-in-double-quotes ok
CASE pacman-log-read-clean ok
CASE refused-db-name ok
CASE seat-name-with-credential-word-allowed ok
CASE refused-symlink ok
CASE command-v-lookup-clean ok
CASE python-heredoc-spawn ok
CASE python-heredoc-data-clean ok
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: 2dc0009eecee94d508522814f4a11924182a6dd5023a2a3781e60789418f021b
SELFTEST_SUMMARY: 32/33 passed failed=['kill-zero-clean']
```

Stderr: `<empty>`.

### restored / core

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M05/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE incident-replica ok
CASE package-query-only ok
CASE live-probe-only ok
CASE live-probe-permitted ok
CASE clean-reads ok
CASE mention-only ok
CASE malformed-json-line ok
CASE no-jsonl-dir ok
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 9/9 passed failed=[]
```

Stderr: `<empty>`.

### restored / compound

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M05/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE compound-and-sudo-pacman ok
CASE abs-path-pacman-upgrade ok
CASE env-prefix-pacman-remove ok
CASE var-assign-pacman-query ok
CASE var-assign-pacman-query-permitted ok
CASE bash-c-sudo-systemctl-restart ok
CASE cmdsub-pacman-query ok
CASE timeout-nohup-hyprctl-mutations ok
CASE xargs-pkill ok
CASE quoted-data-clean ok
CASE eval-bang-sudo-pacman ok
CASE eval-nonbang-clean ok
CASE user-daemon-reload ok
CASE omarchy-mutating-verbs ok
CASE omarchy-permitted ok
CASE dir-scan-all-permitted ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 16/16 passed failed=[]
```

Stderr: `<empty>`.

### restored / hardening

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M05/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE newline-second-line ok
CASE backslash-continuation ok
CASE heredoc-data-clean ok
CASE heredoc-into-shell ok
CASE multiline-quoted-commit-clean ok
CASE multi-toolcall-line ok
CASE eval-subprocess-list ok
CASE eval-bash-c-recipe ok
CASE eval-shell-true ok
CASE eval-tool-bash ok
CASE eval-nonliteral-unparsed-clean ok
CASE eval-js-unparsed-clean ok
CASE kill-zero-clean ok
CASE kill-term ok
CASE systemctl-suspend ok
CASE loginctl-lock ok
CASE loginctl-show-probe ok
CASE omarchy-quoted-grep-clean ok
CASE omarchy-bare-launch ok
CASE result-and-marker-only-clean ok
CASE pacman-sync-print-query ok
CASE pacman-downloadonly-mutation ok
CASE run0-and-systemd-run ok
CASE hyprctl-batch ok
CASE dollar-paren-in-double-quotes ok
CASE pacman-log-read-clean ok
CASE refused-db-name ok
CASE seat-name-with-credential-word-allowed ok
CASE refused-symlink ok
CASE command-v-lookup-clean ok
CASE python-heredoc-spawn ok
CASE python-heredoc-data-clean ok
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 33/33 passed failed=[]
```

Stderr: `<empty>`.

</details>

<details>
<summary>M06: pristine, mutated, and restored suite stdout/stderr</summary>

### pristine / core

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M06/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE incident-replica ok
CASE package-query-only ok
CASE live-probe-only ok
CASE live-probe-permitted ok
CASE clean-reads ok
CASE mention-only ok
CASE malformed-json-line ok
CASE no-jsonl-dir ok
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 9/9 passed failed=[]
```

Stderr: `<empty>`.

### pristine / compound

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M06/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE compound-and-sudo-pacman ok
CASE abs-path-pacman-upgrade ok
CASE env-prefix-pacman-remove ok
CASE var-assign-pacman-query ok
CASE var-assign-pacman-query-permitted ok
CASE bash-c-sudo-systemctl-restart ok
CASE cmdsub-pacman-query ok
CASE timeout-nohup-hyprctl-mutations ok
CASE xargs-pkill ok
CASE quoted-data-clean ok
CASE eval-bang-sudo-pacman ok
CASE eval-nonbang-clean ok
CASE user-daemon-reload ok
CASE omarchy-mutating-verbs ok
CASE omarchy-permitted ok
CASE dir-scan-all-permitted ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 16/16 passed failed=[]
```

Stderr: `<empty>`.

### pristine / hardening

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M06/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE newline-second-line ok
CASE backslash-continuation ok
CASE heredoc-data-clean ok
CASE heredoc-into-shell ok
CASE multiline-quoted-commit-clean ok
CASE multi-toolcall-line ok
CASE eval-subprocess-list ok
CASE eval-bash-c-recipe ok
CASE eval-shell-true ok
CASE eval-tool-bash ok
CASE eval-nonliteral-unparsed-clean ok
CASE eval-js-unparsed-clean ok
CASE kill-zero-clean ok
CASE kill-term ok
CASE systemctl-suspend ok
CASE loginctl-lock ok
CASE loginctl-show-probe ok
CASE omarchy-quoted-grep-clean ok
CASE omarchy-bare-launch ok
CASE result-and-marker-only-clean ok
CASE pacman-sync-print-query ok
CASE pacman-downloadonly-mutation ok
CASE run0-and-systemd-run ok
CASE hyprctl-batch ok
CASE dollar-paren-in-double-quotes ok
CASE pacman-log-read-clean ok
CASE refused-db-name ok
CASE seat-name-with-credential-word-allowed ok
CASE refused-symlink ok
CASE command-v-lookup-clean ok
CASE python-heredoc-spawn ok
CASE python-heredoc-data-clean ok
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 33/33 passed failed=[]
```

Stderr: `<empty>`.

### mutated / core

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M06/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core`

Process exit: `0`; copied-script SHA-256: `2da871068149c2acaaf57ff99544868a5f40bd10a79b57f6b2a467d2188ca40a`.

```text
CASE incident-replica ok
CASE package-query-only ok
CASE live-probe-only ok
CASE live-probe-permitted ok
CASE clean-reads ok
CASE mention-only ok
CASE malformed-json-line ok
CASE no-jsonl-dir ok
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: 2da871068149c2acaaf57ff99544868a5f40bd10a79b57f6b2a467d2188ca40a
SELFTEST_SUMMARY: 9/9 passed failed=[]
```

Stderr: `<empty>`.

### mutated / compound

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M06/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound`

Process exit: `1`; copied-script SHA-256: `2da871068149c2acaaf57ff99544868a5f40bd10a79b57f6b2a467d2188ca40a`.

```text
CASE compound-and-sudo-pacman ok
CASE abs-path-pacman-upgrade ok
CASE env-prefix-pacman-remove ok
CASE var-assign-pacman-query ok
CASE var-assign-pacman-query-permitted ok
CASE bash-c-sudo-systemctl-restart FAIL want=(1, [('host_mutation', 'sudo', 2, 'bash-c-subshell.jsonl'), ('host_mutation', 'systemctl:restart', 2, 'bash-c-subshell.jsonl')]) got=(1, [('host_mutation', 'sudo', 2, 'bash-c-subshell.jsonl'), ('live_probe', 'systemctl:restart', 2, 'bash-c-subshell.jsonl')])
CASE cmdsub-pacman-query ok
CASE timeout-nohup-hyprctl-mutations ok
CASE xargs-pkill ok
CASE quoted-data-clean ok
CASE eval-bang-sudo-pacman ok
CASE eval-nonbang-clean ok
CASE user-daemon-reload FAIL want=(1, [('host_mutation', 'systemctl:daemon-reload', 2, 'user-daemon-reload.jsonl')]) got=(1, [('live_probe', 'systemctl:daemon-reload', 2, 'user-daemon-reload.jsonl')])
CASE omarchy-mutating-verbs ok
CASE omarchy-permitted ok
CASE dir-scan-all-permitted FAIL want=(0, [('host_mutation', 'hyprctl:dispatch', 2, 'wrappers-hyprctl.jsonl'), ('host_mutation', 'hyprctl:keyword', 4, 'wrappers-hyprctl.jsonl'), ('host_mutation', 'omarchy-restart-waybar', 2, 'omarchy-verbs.jsonl'), ('host_mutation', 'omarchy-theme-set', 4, 'omarchy-verbs.jsonl'), ('host_mutation', 'pacman:-R', 2, 'env-prefix.jsonl'), ('host_mutation', 'pacman:-S', 2, 'eval-bang.jsonl'), ('host_mutation', 'pacman:-Syu', 2, 'compound-and.jsonl'), ('host_mutation', 'pacman:-U', 2, 'abs-path-pacman.jsonl'), ('host_mutation', 'pkill', 2, 'xargs-pkill.jsonl'), ('host_mutation', 'sudo', 2, 'bash-c-subshell.jsonl'), ('host_mutation', 'sudo', 2, 'compound-and.jsonl'), ('host_mutation', 'sudo', 2, 'eval-bang.jsonl'), ('host_mutation', 'systemctl:daemon-reload', 2, 'user-daemon-reload.jsonl'), ('host_mutation', 'systemctl:restart', 2, 'bash-c-subshell.jsonl'), ('package_query', 'pacman:-Q', 2, 'var-assign-query.jsonl'), ('package_query', 'pacman:-Qq', 2, 'cmdsub-query.jsonl')]) got=(0, [('host_mutation', 'hyprctl:dispatch', 2, 'wrappers-hyprctl.jsonl'), ('host_mutation', 'hyprctl:keyword', 4, 'wrappers-hyprctl.jsonl'), ('host_mutation', 'omarchy-restart-waybar', 2, 'omarchy-verbs.jsonl'), ('host_mutation', 'omarchy-theme-set', 4, 'omarchy-verbs.jsonl'), ('host_mutation', 'pacman:-R', 2, 'env-prefix.jsonl'), ('host_mutation', 'pacman:-S', 2, 'eval-bang.jsonl'), ('host_mutation', 'pacman:-Syu', 2, 'compound-and.jsonl'), ('host_mutation', 'pacman:-U', 2, 'abs-path-pacman.jsonl'), ('host_mutation', 'pkill', 2, 'xargs-pkill.jsonl'), ('host_mutation', 'sudo', 2, 'bash-c-subshell.jsonl'), ('host_mutation', 'sudo', 2, 'compound-and.jsonl'), ('host_mutation', 'sudo', 2, 'eval-bang.jsonl'), ('live_probe', 'systemctl:daemon-reload', 2, 'user-daemon-reload.jsonl'), ('live_probe', 'systemctl:restart', 2, 'bash-c-subshell.jsonl'), ('package_query', 'pacman:-Q', 2, 'var-assign-query.jsonl'), ('package_query', 'pacman:-Qq', 2, 'cmdsub-query.jsonl')])
SELFTEST_SCRIPT_SHA256: 2da871068149c2acaaf57ff99544868a5f40bd10a79b57f6b2a467d2188ca40a
SELFTEST_SUMMARY: 13/16 passed failed=['bash-c-sudo-systemctl-restart', 'user-daemon-reload', 'dir-scan-all-permitted']
```

Stderr: `<empty>`.

### mutated / hardening

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M06/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening`

Process exit: `1`; copied-script SHA-256: `2da871068149c2acaaf57ff99544868a5f40bd10a79b57f6b2a467d2188ca40a`.

```text
CASE newline-second-line ok
CASE backslash-continuation ok
CASE heredoc-data-clean ok
CASE heredoc-into-shell FAIL want=(1, [('host_mutation', 'systemctl:restart', 1, '')]) got=(1, [('live_probe', 'systemctl:restart', 1, '')])
CASE multiline-quoted-commit-clean ok
CASE multi-toolcall-line ok
CASE eval-subprocess-list ok
CASE eval-bash-c-recipe ok
CASE eval-shell-true ok
CASE eval-tool-bash FAIL want=(1, [('host_mutation', 'sudo', 1, ''), ('host_mutation', 'systemctl:restart', 1, '')]) got=(1, [('host_mutation', 'sudo', 1, ''), ('live_probe', 'systemctl:restart', 1, '')])
CASE eval-nonliteral-unparsed-clean ok
CASE eval-js-unparsed-clean ok
CASE kill-zero-clean ok
CASE kill-term ok
CASE systemctl-suspend FAIL want=(1, [('host_mutation', 'systemctl:suspend', 1, '')]) got=(1, [('live_probe', 'systemctl:suspend', 1, '')])
CASE loginctl-lock ok
CASE loginctl-show-probe ok
CASE omarchy-quoted-grep-clean ok
CASE omarchy-bare-launch ok
CASE result-and-marker-only-clean ok
CASE pacman-sync-print-query ok
CASE pacman-downloadonly-mutation ok
CASE run0-and-systemd-run ok
CASE hyprctl-batch ok
CASE dollar-paren-in-double-quotes ok
CASE pacman-log-read-clean ok
CASE refused-db-name ok
CASE seat-name-with-credential-word-allowed ok
CASE refused-symlink ok
CASE command-v-lookup-clean ok
CASE python-heredoc-spawn ok
CASE python-heredoc-data-clean ok
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: 2da871068149c2acaaf57ff99544868a5f40bd10a79b57f6b2a467d2188ca40a
SELFTEST_SUMMARY: 30/33 passed failed=['heredoc-into-shell', 'eval-tool-bash', 'systemctl-suspend']
```

Stderr: `<empty>`.

### restored / core

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M06/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE incident-replica ok
CASE package-query-only ok
CASE live-probe-only ok
CASE live-probe-permitted ok
CASE clean-reads ok
CASE mention-only ok
CASE malformed-json-line ok
CASE no-jsonl-dir ok
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 9/9 passed failed=[]
```

Stderr: `<empty>`.

### restored / compound

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M06/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE compound-and-sudo-pacman ok
CASE abs-path-pacman-upgrade ok
CASE env-prefix-pacman-remove ok
CASE var-assign-pacman-query ok
CASE var-assign-pacman-query-permitted ok
CASE bash-c-sudo-systemctl-restart ok
CASE cmdsub-pacman-query ok
CASE timeout-nohup-hyprctl-mutations ok
CASE xargs-pkill ok
CASE quoted-data-clean ok
CASE eval-bang-sudo-pacman ok
CASE eval-nonbang-clean ok
CASE user-daemon-reload ok
CASE omarchy-mutating-verbs ok
CASE omarchy-permitted ok
CASE dir-scan-all-permitted ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 16/16 passed failed=[]
```

Stderr: `<empty>`.

### restored / hardening

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M06/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE newline-second-line ok
CASE backslash-continuation ok
CASE heredoc-data-clean ok
CASE heredoc-into-shell ok
CASE multiline-quoted-commit-clean ok
CASE multi-toolcall-line ok
CASE eval-subprocess-list ok
CASE eval-bash-c-recipe ok
CASE eval-shell-true ok
CASE eval-tool-bash ok
CASE eval-nonliteral-unparsed-clean ok
CASE eval-js-unparsed-clean ok
CASE kill-zero-clean ok
CASE kill-term ok
CASE systemctl-suspend ok
CASE loginctl-lock ok
CASE loginctl-show-probe ok
CASE omarchy-quoted-grep-clean ok
CASE omarchy-bare-launch ok
CASE result-and-marker-only-clean ok
CASE pacman-sync-print-query ok
CASE pacman-downloadonly-mutation ok
CASE run0-and-systemd-run ok
CASE hyprctl-batch ok
CASE dollar-paren-in-double-quotes ok
CASE pacman-log-read-clean ok
CASE refused-db-name ok
CASE seat-name-with-credential-word-allowed ok
CASE refused-symlink ok
CASE command-v-lookup-clean ok
CASE python-heredoc-spawn ok
CASE python-heredoc-data-clean ok
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 33/33 passed failed=[]
```

Stderr: `<empty>`.

</details>

<details>
<summary>M07: pristine, mutated, and restored suite stdout/stderr</summary>

### pristine / core

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M07/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE incident-replica ok
CASE package-query-only ok
CASE live-probe-only ok
CASE live-probe-permitted ok
CASE clean-reads ok
CASE mention-only ok
CASE malformed-json-line ok
CASE no-jsonl-dir ok
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 9/9 passed failed=[]
```

Stderr: `<empty>`.

### pristine / compound

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M07/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE compound-and-sudo-pacman ok
CASE abs-path-pacman-upgrade ok
CASE env-prefix-pacman-remove ok
CASE var-assign-pacman-query ok
CASE var-assign-pacman-query-permitted ok
CASE bash-c-sudo-systemctl-restart ok
CASE cmdsub-pacman-query ok
CASE timeout-nohup-hyprctl-mutations ok
CASE xargs-pkill ok
CASE quoted-data-clean ok
CASE eval-bang-sudo-pacman ok
CASE eval-nonbang-clean ok
CASE user-daemon-reload ok
CASE omarchy-mutating-verbs ok
CASE omarchy-permitted ok
CASE dir-scan-all-permitted ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 16/16 passed failed=[]
```

Stderr: `<empty>`.

### pristine / hardening

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M07/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE newline-second-line ok
CASE backslash-continuation ok
CASE heredoc-data-clean ok
CASE heredoc-into-shell ok
CASE multiline-quoted-commit-clean ok
CASE multi-toolcall-line ok
CASE eval-subprocess-list ok
CASE eval-bash-c-recipe ok
CASE eval-shell-true ok
CASE eval-tool-bash ok
CASE eval-nonliteral-unparsed-clean ok
CASE eval-js-unparsed-clean ok
CASE kill-zero-clean ok
CASE kill-term ok
CASE systemctl-suspend ok
CASE loginctl-lock ok
CASE loginctl-show-probe ok
CASE omarchy-quoted-grep-clean ok
CASE omarchy-bare-launch ok
CASE result-and-marker-only-clean ok
CASE pacman-sync-print-query ok
CASE pacman-downloadonly-mutation ok
CASE run0-and-systemd-run ok
CASE hyprctl-batch ok
CASE dollar-paren-in-double-quotes ok
CASE pacman-log-read-clean ok
CASE refused-db-name ok
CASE seat-name-with-credential-word-allowed ok
CASE refused-symlink ok
CASE command-v-lookup-clean ok
CASE python-heredoc-spawn ok
CASE python-heredoc-data-clean ok
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 33/33 passed failed=[]
```

Stderr: `<empty>`.

### mutated / core

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M07/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core`

Process exit: `0`; copied-script SHA-256: `0cb53e5db261c8a5ad8244572665dba57a427cd912cdf34af2f0fff9212386b0`.

```text
CASE incident-replica ok
CASE package-query-only ok
CASE live-probe-only ok
CASE live-probe-permitted ok
CASE clean-reads ok
CASE mention-only ok
CASE malformed-json-line ok
CASE no-jsonl-dir ok
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: 0cb53e5db261c8a5ad8244572665dba57a427cd912cdf34af2f0fff9212386b0
SELFTEST_SUMMARY: 9/9 passed failed=[]
```

Stderr: `<empty>`.

### mutated / compound

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M07/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound`

Process exit: `0`; copied-script SHA-256: `0cb53e5db261c8a5ad8244572665dba57a427cd912cdf34af2f0fff9212386b0`.

```text
CASE compound-and-sudo-pacman ok
CASE abs-path-pacman-upgrade ok
CASE env-prefix-pacman-remove ok
CASE var-assign-pacman-query ok
CASE var-assign-pacman-query-permitted ok
CASE bash-c-sudo-systemctl-restart ok
CASE cmdsub-pacman-query ok
CASE timeout-nohup-hyprctl-mutations ok
CASE xargs-pkill ok
CASE quoted-data-clean ok
CASE eval-bang-sudo-pacman ok
CASE eval-nonbang-clean ok
CASE user-daemon-reload ok
CASE omarchy-mutating-verbs ok
CASE omarchy-permitted ok
CASE dir-scan-all-permitted ok
SELFTEST_SCRIPT_SHA256: 0cb53e5db261c8a5ad8244572665dba57a427cd912cdf34af2f0fff9212386b0
SELFTEST_SUMMARY: 16/16 passed failed=[]
```

Stderr: `<empty>`.

### mutated / hardening

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M07/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening`

Process exit: `0`; copied-script SHA-256: `0cb53e5db261c8a5ad8244572665dba57a427cd912cdf34af2f0fff9212386b0`.

```text
CASE newline-second-line ok
CASE backslash-continuation ok
CASE heredoc-data-clean ok
CASE heredoc-into-shell ok
CASE multiline-quoted-commit-clean ok
CASE multi-toolcall-line ok
CASE eval-subprocess-list ok
CASE eval-bash-c-recipe ok
CASE eval-shell-true ok
CASE eval-tool-bash ok
CASE eval-nonliteral-unparsed-clean ok
CASE eval-js-unparsed-clean ok
CASE kill-zero-clean ok
CASE kill-term ok
CASE systemctl-suspend ok
CASE loginctl-lock ok
CASE loginctl-show-probe ok
CASE omarchy-quoted-grep-clean ok
CASE omarchy-bare-launch ok
CASE result-and-marker-only-clean ok
CASE pacman-sync-print-query ok
CASE pacman-downloadonly-mutation ok
CASE run0-and-systemd-run ok
CASE hyprctl-batch ok
CASE dollar-paren-in-double-quotes ok
CASE pacman-log-read-clean ok
CASE refused-db-name ok
CASE seat-name-with-credential-word-allowed ok
CASE refused-symlink ok
CASE command-v-lookup-clean ok
CASE python-heredoc-spawn ok
CASE python-heredoc-data-clean ok
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: 0cb53e5db261c8a5ad8244572665dba57a427cd912cdf34af2f0fff9212386b0
SELFTEST_SUMMARY: 33/33 passed failed=[]
```

Stderr: `<empty>`.

### restored / core

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M07/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE incident-replica ok
CASE package-query-only ok
CASE live-probe-only ok
CASE live-probe-permitted ok
CASE clean-reads ok
CASE mention-only ok
CASE malformed-json-line ok
CASE no-jsonl-dir ok
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 9/9 passed failed=[]
```

Stderr: `<empty>`.

### restored / compound

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M07/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE compound-and-sudo-pacman ok
CASE abs-path-pacman-upgrade ok
CASE env-prefix-pacman-remove ok
CASE var-assign-pacman-query ok
CASE var-assign-pacman-query-permitted ok
CASE bash-c-sudo-systemctl-restart ok
CASE cmdsub-pacman-query ok
CASE timeout-nohup-hyprctl-mutations ok
CASE xargs-pkill ok
CASE quoted-data-clean ok
CASE eval-bang-sudo-pacman ok
CASE eval-nonbang-clean ok
CASE user-daemon-reload ok
CASE omarchy-mutating-verbs ok
CASE omarchy-permitted ok
CASE dir-scan-all-permitted ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 16/16 passed failed=[]
```

Stderr: `<empty>`.

### restored / hardening

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M07/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE newline-second-line ok
CASE backslash-continuation ok
CASE heredoc-data-clean ok
CASE heredoc-into-shell ok
CASE multiline-quoted-commit-clean ok
CASE multi-toolcall-line ok
CASE eval-subprocess-list ok
CASE eval-bash-c-recipe ok
CASE eval-shell-true ok
CASE eval-tool-bash ok
CASE eval-nonliteral-unparsed-clean ok
CASE eval-js-unparsed-clean ok
CASE kill-zero-clean ok
CASE kill-term ok
CASE systemctl-suspend ok
CASE loginctl-lock ok
CASE loginctl-show-probe ok
CASE omarchy-quoted-grep-clean ok
CASE omarchy-bare-launch ok
CASE result-and-marker-only-clean ok
CASE pacman-sync-print-query ok
CASE pacman-downloadonly-mutation ok
CASE run0-and-systemd-run ok
CASE hyprctl-batch ok
CASE dollar-paren-in-double-quotes ok
CASE pacman-log-read-clean ok
CASE refused-db-name ok
CASE seat-name-with-credential-word-allowed ok
CASE refused-symlink ok
CASE command-v-lookup-clean ok
CASE python-heredoc-spawn ok
CASE python-heredoc-data-clean ok
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 33/33 passed failed=[]
```

Stderr: `<empty>`.

</details>

<details>
<summary>M08: pristine, mutated, and restored suite stdout/stderr</summary>

### pristine / core

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M08/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE incident-replica ok
CASE package-query-only ok
CASE live-probe-only ok
CASE live-probe-permitted ok
CASE clean-reads ok
CASE mention-only ok
CASE malformed-json-line ok
CASE no-jsonl-dir ok
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 9/9 passed failed=[]
```

Stderr: `<empty>`.

### pristine / compound

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M08/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE compound-and-sudo-pacman ok
CASE abs-path-pacman-upgrade ok
CASE env-prefix-pacman-remove ok
CASE var-assign-pacman-query ok
CASE var-assign-pacman-query-permitted ok
CASE bash-c-sudo-systemctl-restart ok
CASE cmdsub-pacman-query ok
CASE timeout-nohup-hyprctl-mutations ok
CASE xargs-pkill ok
CASE quoted-data-clean ok
CASE eval-bang-sudo-pacman ok
CASE eval-nonbang-clean ok
CASE user-daemon-reload ok
CASE omarchy-mutating-verbs ok
CASE omarchy-permitted ok
CASE dir-scan-all-permitted ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 16/16 passed failed=[]
```

Stderr: `<empty>`.

### pristine / hardening

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M08/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE newline-second-line ok
CASE backslash-continuation ok
CASE heredoc-data-clean ok
CASE heredoc-into-shell ok
CASE multiline-quoted-commit-clean ok
CASE multi-toolcall-line ok
CASE eval-subprocess-list ok
CASE eval-bash-c-recipe ok
CASE eval-shell-true ok
CASE eval-tool-bash ok
CASE eval-nonliteral-unparsed-clean ok
CASE eval-js-unparsed-clean ok
CASE kill-zero-clean ok
CASE kill-term ok
CASE systemctl-suspend ok
CASE loginctl-lock ok
CASE loginctl-show-probe ok
CASE omarchy-quoted-grep-clean ok
CASE omarchy-bare-launch ok
CASE result-and-marker-only-clean ok
CASE pacman-sync-print-query ok
CASE pacman-downloadonly-mutation ok
CASE run0-and-systemd-run ok
CASE hyprctl-batch ok
CASE dollar-paren-in-double-quotes ok
CASE pacman-log-read-clean ok
CASE refused-db-name ok
CASE seat-name-with-credential-word-allowed ok
CASE refused-symlink ok
CASE command-v-lookup-clean ok
CASE python-heredoc-spawn ok
CASE python-heredoc-data-clean ok
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 33/33 passed failed=[]
```

Stderr: `<empty>`.

### mutated / core

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M08/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core`

Process exit: `0`; copied-script SHA-256: `17bf367bcac38047fa5d92c3269ee45d453751a98dbedcb58703432877d0260e`.

```text
CASE incident-replica ok
CASE package-query-only ok
CASE live-probe-only ok
CASE live-probe-permitted ok
CASE clean-reads ok
CASE mention-only ok
CASE malformed-json-line ok
CASE no-jsonl-dir ok
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: 17bf367bcac38047fa5d92c3269ee45d453751a98dbedcb58703432877d0260e
SELFTEST_SUMMARY: 9/9 passed failed=[]
```

Stderr: `<empty>`.

### mutated / compound

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M08/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound`

Process exit: `0`; copied-script SHA-256: `17bf367bcac38047fa5d92c3269ee45d453751a98dbedcb58703432877d0260e`.

```text
CASE compound-and-sudo-pacman ok
CASE abs-path-pacman-upgrade ok
CASE env-prefix-pacman-remove ok
CASE var-assign-pacman-query ok
CASE var-assign-pacman-query-permitted ok
CASE bash-c-sudo-systemctl-restart ok
CASE cmdsub-pacman-query ok
CASE timeout-nohup-hyprctl-mutations ok
CASE xargs-pkill ok
CASE quoted-data-clean ok
CASE eval-bang-sudo-pacman ok
CASE eval-nonbang-clean ok
CASE user-daemon-reload ok
CASE omarchy-mutating-verbs ok
CASE omarchy-permitted ok
CASE dir-scan-all-permitted ok
SELFTEST_SCRIPT_SHA256: 17bf367bcac38047fa5d92c3269ee45d453751a98dbedcb58703432877d0260e
SELFTEST_SUMMARY: 16/16 passed failed=[]
```

Stderr: `<empty>`.

### mutated / hardening

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M08/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening`

Process exit: `0`; copied-script SHA-256: `17bf367bcac38047fa5d92c3269ee45d453751a98dbedcb58703432877d0260e`.

```text
CASE newline-second-line ok
CASE backslash-continuation ok
CASE heredoc-data-clean ok
CASE heredoc-into-shell ok
CASE multiline-quoted-commit-clean ok
CASE multi-toolcall-line ok
CASE eval-subprocess-list ok
CASE eval-bash-c-recipe ok
CASE eval-shell-true ok
CASE eval-tool-bash ok
CASE eval-nonliteral-unparsed-clean ok
CASE eval-js-unparsed-clean ok
CASE kill-zero-clean ok
CASE kill-term ok
CASE systemctl-suspend ok
CASE loginctl-lock ok
CASE loginctl-show-probe ok
CASE omarchy-quoted-grep-clean ok
CASE omarchy-bare-launch ok
CASE result-and-marker-only-clean ok
CASE pacman-sync-print-query ok
CASE pacman-downloadonly-mutation ok
CASE run0-and-systemd-run ok
CASE hyprctl-batch ok
CASE dollar-paren-in-double-quotes ok
CASE pacman-log-read-clean ok
CASE refused-db-name ok
CASE seat-name-with-credential-word-allowed ok
CASE refused-symlink ok
CASE command-v-lookup-clean ok
CASE python-heredoc-spawn ok
CASE python-heredoc-data-clean ok
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: 17bf367bcac38047fa5d92c3269ee45d453751a98dbedcb58703432877d0260e
SELFTEST_SUMMARY: 33/33 passed failed=[]
```

Stderr: `<empty>`.

### restored / core

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M08/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE incident-replica ok
CASE package-query-only ok
CASE live-probe-only ok
CASE live-probe-permitted ok
CASE clean-reads ok
CASE mention-only ok
CASE malformed-json-line ok
CASE no-jsonl-dir ok
CASE dir-scan-two-files ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 9/9 passed failed=[]
```

Stderr: `<empty>`.

### restored / compound

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M08/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE compound-and-sudo-pacman ok
CASE abs-path-pacman-upgrade ok
CASE env-prefix-pacman-remove ok
CASE var-assign-pacman-query ok
CASE var-assign-pacman-query-permitted ok
CASE bash-c-sudo-systemctl-restart ok
CASE cmdsub-pacman-query ok
CASE timeout-nohup-hyprctl-mutations ok
CASE xargs-pkill ok
CASE quoted-data-clean ok
CASE eval-bang-sudo-pacman ok
CASE eval-nonbang-clean ok
CASE user-daemon-reload ok
CASE omarchy-mutating-verbs ok
CASE omarchy-permitted ok
CASE dir-scan-all-permitted ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 16/16 passed failed=[]
```

Stderr: `<empty>`.

### restored / hardening

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M08/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening`

Process exit: `0`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
CASE newline-second-line ok
CASE backslash-continuation ok
CASE heredoc-data-clean ok
CASE heredoc-into-shell ok
CASE multiline-quoted-commit-clean ok
CASE multi-toolcall-line ok
CASE eval-subprocess-list ok
CASE eval-bash-c-recipe ok
CASE eval-shell-true ok
CASE eval-tool-bash ok
CASE eval-nonliteral-unparsed-clean ok
CASE eval-js-unparsed-clean ok
CASE kill-zero-clean ok
CASE kill-term ok
CASE systemctl-suspend ok
CASE loginctl-lock ok
CASE loginctl-show-probe ok
CASE omarchy-quoted-grep-clean ok
CASE omarchy-bare-launch ok
CASE result-and-marker-only-clean ok
CASE pacman-sync-print-query ok
CASE pacman-downloadonly-mutation ok
CASE run0-and-systemd-run ok
CASE hyprctl-batch ok
CASE dollar-paren-in-double-quotes ok
CASE pacman-log-read-clean ok
CASE refused-db-name ok
CASE seat-name-with-credential-word-allowed ok
CASE refused-symlink ok
CASE command-v-lookup-clean ok
CASE python-heredoc-spawn ok
CASE python-heredoc-data-clean ok
CASE python-c-spawn ok
SELFTEST_SCRIPT_SHA256: 4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
SELFTEST_SUMMARY: 33/33 passed failed=[]
```

Stderr: `<empty>`.

</details>

<details>
<summary>Survivor witness scan stdout/stderr in all three phases</summary>

### M01 / pristine

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M01/mado-tripwire.py --scan /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M01/witness.jsonl`

Process exit: `1`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1}, "exit": 1, "files": [{"bash_calls": 1, "eval_calls": 0, "eval_unparsed": 0, "lines": 1, "path": "/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M01/witness.jsonl", "sha256": "b2f18cbeb3974bf4719cc90e7e97c00201d17998e2c07d5ec01a126e95f6ef72", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman --query hyprland", "file": "/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M01/witness.jsonl", "line": 1, "rule": "pacman:--query", "timestamp": null, "tool": "bash", "tool_call_id": "witness-M01"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
```

Stderr: `<empty>`.

### M01 / mutated

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M01/mado-tripwire.py --scan /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M01/witness.jsonl`

Process exit: `1`; copied-script SHA-256: `466794b2ef7b769558b87f9b4b8d47b34f553f415ce37c212a768007018fc9fb`.

```text
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 1, "live_probe": 0, "package_query": 0}, "exit": 1, "files": [{"bash_calls": 1, "eval_calls": 0, "eval_unparsed": 0, "lines": 1, "path": "/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M01/witness.jsonl", "sha256": "b2f18cbeb3974bf4719cc90e7e97c00201d17998e2c07d5ec01a126e95f6ef72", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "host_mutation", "command": "pacman --query hyprland", "file": "/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M01/witness.jsonl", "line": 1, "rule": "pacman:--query", "timestamp": null, "tool": "bash", "tool_call_id": "witness-M01"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
```

Stderr: `<empty>`.

### M01 / restored

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M01/mado-tripwire.py --scan /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M01/witness.jsonl`

Process exit: `1`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1}, "exit": 1, "files": [{"bash_calls": 1, "eval_calls": 0, "eval_unparsed": 0, "lines": 1, "path": "/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M01/witness.jsonl", "sha256": "b2f18cbeb3974bf4719cc90e7e97c00201d17998e2c07d5ec01a126e95f6ef72", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman --query hyprland", "file": "/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M01/witness.jsonl", "line": 1, "rule": "pacman:--query", "timestamp": null, "tool": "bash", "tool_call_id": "witness-M01"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
```

Stderr: `<empty>`.

### M03 / pristine

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M03/mado-tripwire.py --scan /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M03/witness.jsonl`

Process exit: `1`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 1, "live_probe": 0, "package_query": 0}, "exit": 1, "files": [{"bash_calls": 1, "eval_calls": 0, "eval_unparsed": 0, "lines": 1, "path": "/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M03/witness.jsonl", "sha256": "fb673bf418966f267e077393ac3faf18e88d28c57ca95332bbe98296a7d1d4da", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "host_mutation", "command": "pacman -Swp hyprland", "file": "/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M03/witness.jsonl", "line": 1, "rule": "pacman:-Swp", "timestamp": null, "tool": "bash", "tool_call_id": "witness-M03"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
```

Stderr: `<empty>`.

### M03 / mutated

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M03/mado-tripwire.py --scan /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M03/witness.jsonl`

Process exit: `1`; copied-script SHA-256: `736864ed2b9695c25ed486e382310fdddda696c9fcdff7a0505b210e81550f11`.

```text
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1}, "exit": 1, "files": [{"bash_calls": 1, "eval_calls": 0, "eval_unparsed": 0, "lines": 1, "path": "/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M03/witness.jsonl", "sha256": "fb673bf418966f267e077393ac3faf18e88d28c57ca95332bbe98296a7d1d4da", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Swp hyprland", "file": "/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M03/witness.jsonl", "line": 1, "rule": "pacman:-Swp", "timestamp": null, "tool": "bash", "tool_call_id": "witness-M03"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
```

Stderr: `<empty>`.

### M03 / restored

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M03/mado-tripwire.py --scan /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M03/witness.jsonl`

Process exit: `1`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 1, "live_probe": 0, "package_query": 0}, "exit": 1, "files": [{"bash_calls": 1, "eval_calls": 0, "eval_unparsed": 0, "lines": 1, "path": "/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M03/witness.jsonl", "sha256": "fb673bf418966f267e077393ac3faf18e88d28c57ca95332bbe98296a7d1d4da", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "host_mutation", "command": "pacman -Swp hyprland", "file": "/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M03/witness.jsonl", "line": 1, "rule": "pacman:-Swp", "timestamp": null, "tool": "bash", "tool_call_id": "witness-M03"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
```

Stderr: `<empty>`.

### M07 / pristine

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M07/mado-tripwire.py --scan /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M07/witness.jsonl`

Process exit: `1`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1}, "exit": 1, "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M07/witness.jsonl", "sha256": "91e693eb1d1f9cd0308c1f9d564e3499efcb21616bb4c5e055fabfa4a1299a07", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M07/witness.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": null, "tool": "eval", "tool_call_id": "witness-M07"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
```

Stderr: `<empty>`.

### M07 / mutated

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M07/mado-tripwire.py --scan /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M07/witness.jsonl`

Process exit: `0`; copied-script SHA-256: `0cb53e5db261c8a5ad8244572665dba57a427cd912cdf34af2f0fff9212386b0`.

```text
MADO_TRIPWIRE: clean
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M07/witness.jsonl", "sha256": "91e693eb1d1f9cd0308c1f9d564e3499efcb21616bb4c5e055fabfa4a1299a07", "unparsed_spawns": 1}], "findings": [], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
```

Stderr: `<empty>`.

### M07 / restored

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M07/mado-tripwire.py --scan /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M07/witness.jsonl`

Process exit: `1`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1}, "exit": 1, "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M07/witness.jsonl", "sha256": "91e693eb1d1f9cd0308c1f9d564e3499efcb21616bb4c5e055fabfa4a1299a07", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M07/witness.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": null, "tool": "eval", "tool_call_id": "witness-M07"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
```

Stderr: `<empty>`.

### M08 / pristine

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M08/mado-tripwire.py --scan /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M08/witness.jsonl`

Process exit: `1`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1}, "exit": 1, "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M08/witness.jsonl", "sha256": "a755834e2a8631e6328d873e254a02d9e6bd52305dc216e866e09a40ad987f64", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M08/witness.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": null, "tool": "eval", "tool_call_id": "witness-M08"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
```

Stderr: `<empty>`.

### M08 / mutated

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M08/mado-tripwire.py --scan /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M08/witness.jsonl`

Process exit: `0`; copied-script SHA-256: `17bf367bcac38047fa5d92c3269ee45d453751a98dbedcb58703432877d0260e`.

```text
MADO_TRIPWIRE: clean
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M08/witness.jsonl", "sha256": "a755834e2a8631e6328d873e254a02d9e6bd52305dc216e866e09a40ad987f64", "unparsed_spawns": 0}], "findings": [], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
```

Stderr: `<empty>`.

### M08 / restored

Command: `python3 -I /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M08/mado-tripwire.py --scan /tmp/mado-r17-mutatetripwire2-bv2pk1ng/M08/witness.jsonl`

Process exit: `1`; copied-script SHA-256: `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.

```text
MADO_TRIPWIRE: findings
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1}, "exit": 1, "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M08/witness.jsonl", "sha256": "a755834e2a8631e6328d873e254a02d9e6bd52305dc216e866e09a40ad987f64", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "/tmp/mado-r17-mutatetripwire2-bv2pk1ng/M08/witness.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": null, "tool": "eval", "tool_call_id": "witness-M08"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
```

Stderr: `<empty>`.

</details>

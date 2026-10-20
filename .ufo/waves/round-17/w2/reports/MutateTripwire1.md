# MutateTripwire1 — first-third mutation probe

## Result and scope

**Nine independent, one-line mutants: 4 killed, 5 survived, 0 inconclusive.** Each copied script ran all three supplied selftest suites on pristine, mutated, and exactly restored bytes: **81 suite invocations** total. Every pristine and restored invocation passed (core 9/9, compound 16/16, hardening 33/33). The surviving mutants also passed all 58 cases, but synthetic transcript scans demonstrated a real behavioral regression for every survivor.

Attack target: C3’s supplied tripwire selftest coverage. These are coverage counterexamples, not a judgment that pristine HEAD already has the injected defects, nor a re-grade of C1/C2 or the separately claimed real-transcript anchor/pacman-log joins. No real session transcripts or pacman log were opened by this item.

- Source: `tools/mado-tripwire.py`, task-reported lane HEAD `988b858bd6049bc709807534fd725c05264f7e60` (no Git invocation used to re-resolve it).
- Measured source length: **818 lines**. Split convention: boundaries `floor(i * 818 / 3)`; thirds are **1–272**, 273–545, 546–818. All changed lines lie in third 1: 43, 51, 76, 88, 91, 189, 221, 234, 258.
- Isolated workspace: `/tmp/MadoR17.MutateTripwire1.y22F4q`. Each mutant had its own `.py` copy; no cumulative mutations and no sibling-source writes.
- Axes for this probe: detector sensitivity, coverage precision (genuine behavior-changing survivors), and source isolation/exact restoration. These are test dimensions, not new lane claim scores.
- Installs: **none**. No delegation, runtime switching, commits, Git mutations, forbidden host commands, compositor/device probes, or real credential/database reads.

## Detector and execution bounds

For each script named below, the actual detector argv was `python3 -I SCRIPT --selftest SUITE`, with these exact suite directories:

```text
/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core
/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound
/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening
```

`SCRIPT` was the absolute scratch-copy path in the mutation table, never the lane script. The existing selftest’s `__file__` dispatch (`tools/mado-tripwire.py:739–743`) therefore ran each scan with that same copied script. The same command/env/bounds were used in all three stages: cwd and HOME were the scratch directory; PATH `/usr/bin:/bin`; LC_ALL `C`; PYTHONDONTWRITEBYTECODE `1`; 120-second outer bound per suite; up to nine independent suite invocations concurrently. No suite timed out. All suite stderr was empty.

The additional synthetic-witness detector used `python3 -I SCRIPT --scan WITNESS`, identical env/cwd and a 30-second bound, before mutation (shared byte-identical pristine copy), during mutation, and after restoration. Witnesses were JSONL data only: none of the commands inside them was executed.

## Mutants and expected detector

All script names below are relative to `/tmp/MadoR17.MutateTripwire1.y22F4q/`.

| Mutant / copied script | Original source line | Single defect | Expected distinguishing behavior | Verdict |
|---|---:|---|---|---|
| `M01-libinput-omission.py` | 76 | Remove `libinput` from `LIVE_PROBE_BINS`. | A bare issued `libinput` call should retain a live-probe finding; the three supplied suites did not detect its loss. | **survived** |
| `M02-run0-omission.py` | 43 | Remove `run0` from `ELEVATE`. | `hardening/run0-and-systemd-run` should detect the missing elevation and wrapped package-removal findings. | **killed** |
| `M03-aws-length.py` | 91 | Change AWS-ID redaction quantifier `{16}` to `{17}`. | A 20-character synthetic `AKIA` identifier should remain redacted; no supplied selftest asserts the rendered command field. | **survived** |
| `M04-command-v.py` | 221 | Recognize only `command -V`, not `command -v`, as a lookup. | `hardening/command-v-lookup-clean` should reject the resulting false positive. | **killed** |
| `M05-dollar-substitution.py` | 189 | Change command-substitution opener `$(` to `${`. | `hardening/dollar-paren-in-double-quotes` should detect the lost nested package query. | **killed** |
| `M06-xargs-I.py` | 51 | Remove `-I` from the xargs options that consume an argument. | An issued `xargs -I SLOT pkill SLOT` should retain its host-mutation finding; supplied xargs coverage uses only `-r`. | **survived** |
| `M07-timeout-argument.py` | 258 | Remove the last timeout argument rather than the first duration argument (`pop(0)` → `pop(-1)`). | `compound/timeout-nohup-hyprctl-mutations` and its directory-scan case should detect the lost wrapped dispatch. | **killed** |
| `M08-refusal-case.py` | 88 | Compile refused-name regex with flags `0` instead of `re.I`. | The case-variant synthetic `AGENT.DB.TRIPWIRE-FIXTURE.jsonl` should still be refused; supplied refusal-name coverage does not catch the change. | **survived** |
| `M09-env-C.py` | 234 | Stop consuming the directory argument of `env -C`. | An issued `env -C /tmp journalctl --no-pager` should retain its live-probe finding; supplied env coverage has assignments but no `-C` directory argument. | **survived** |

## Actual selftest outputs

Each cell below is the actual `SELFTEST_SUMMARY:` suffix followed by the process exit code. Suite order is always core / compound / hardening. Pristine and restored entries were independently run for every copy, not inferred from the common hash.

| Copy | Pristine: core / compound / hardening | Mutated: core / compound / hardening | Restored: core / compound / hardening |
|---|---|---|---|
| `M01-libinput-omission` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`33/33 passed failed=[]; exit=0` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`33/33 passed failed=[]; exit=0` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`33/33 passed failed=[]; exit=0` |
| `M02-run0-omission` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`33/33 passed failed=[]; exit=0` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`32/33 passed failed=['run0-and-systemd-run']; exit=1` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`33/33 passed failed=[]; exit=0` |
| `M03-aws-length` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`33/33 passed failed=[]; exit=0` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`33/33 passed failed=[]; exit=0` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`33/33 passed failed=[]; exit=0` |
| `M04-command-v` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`33/33 passed failed=[]; exit=0` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`32/33 passed failed=['command-v-lookup-clean']; exit=1` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`33/33 passed failed=[]; exit=0` |
| `M05-dollar-substitution` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`33/33 passed failed=[]; exit=0` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`32/33 passed failed=['dollar-paren-in-double-quotes']; exit=1` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`33/33 passed failed=[]; exit=0` |
| `M06-xargs-I` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`33/33 passed failed=[]; exit=0` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`33/33 passed failed=[]; exit=0` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`33/33 passed failed=[]; exit=0` |
| `M07-timeout-argument` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`33/33 passed failed=[]; exit=0` | `9/9 passed failed=[]; exit=0`<br>`14/16 passed failed=['timeout-nohup-hyprctl-mutations', 'dir-scan-all-permitted']; exit=1`<br>`33/33 passed failed=[]; exit=0` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`33/33 passed failed=[]; exit=0` |
| `M08-refusal-case` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`33/33 passed failed=[]; exit=0` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`33/33 passed failed=[]; exit=0` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`33/33 passed failed=[]; exit=0` |
| `M09-env-C` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`33/33 passed failed=[]; exit=0` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`33/33 passed failed=[]; exit=0` | `9/9 passed failed=[]; exit=0`<br>`16/16 passed failed=[]; exit=0`<br>`33/33 passed failed=[]; exit=0` |

### Verbatim failing CASE lines

These are all failing-case stdout lines from the mutated stage; no baseline/restored case failed.

```text
M02-run0-omission / hardening:
CASE run0-and-systemd-run FAIL want=(1, [('host_mutation', 'hyprctl:reload', 1, ''), ('host_mutation', 'pacman:-R', 1, ''), ('host_mutation', 'run0', 1, ''), ('host_mutation', 'systemd-run', 1, '')]) got=(1, [('host_mutation', 'hyprctl:reload', 1, ''), ('host_mutation', 'systemd-run', 1, '')])
M04-command-v / hardening:
CASE command-v-lookup-clean FAIL want=(0, []) got=(1, [('live_probe', 'libinput', 1, '')])
M05-dollar-substitution / hardening:
CASE dollar-paren-in-double-quotes FAIL want=(1, [('package_query', 'pacman:-Q', 1, '')]) got=(0, [])
M07-timeout-argument / compound:
CASE timeout-nohup-hyprctl-mutations FAIL want=(1, [('host_mutation', 'hyprctl:dispatch', 2, 'wrappers-hyprctl.jsonl'), ('host_mutation', 'hyprctl:keyword', 4, 'wrappers-hyprctl.jsonl')]) got=(1, [('host_mutation', 'hyprctl:keyword', 4, 'wrappers-hyprctl.jsonl')])
CASE dir-scan-all-permitted FAIL want=(0, [('host_mutation', 'hyprctl:dispatch', 2, 'wrappers-hyprctl.jsonl'), ('host_mutation', 'hyprctl:keyword', 4, 'wrappers-hyprctl.jsonl'), ('host_mutation', 'omarchy-restart-waybar', 2, 'omarchy-verbs.jsonl'), ('host_mutation', 'omarchy-theme-set', 4, 'omarchy-verbs.jsonl'), ('host_mutation', 'pacman:-R', 2, 'env-prefix.jsonl'), ('host_mutation', 'pacman:-S', 2, 'eval-bang.jsonl'), ('host_mutation', 'pacman:-Syu', 2, 'compound-and.jsonl'), ('host_mutation', 'pacman:-U', 2, 'abs-path-pacman.jsonl'), ('host_mutation', 'pkill', 2, 'xargs-pkill.jsonl'), ('host_mutation', 'sudo', 2, 'bash-c-subshell.jsonl'), ('host_mutation', 'sudo', 2, 'compound-and.jsonl'), ('host_mutation', 'sudo', 2, 'eval-bang.jsonl'), ('host_mutation', 'systemctl:daemon-reload', 2, 'user-daemon-reload.jsonl'), ('host_mutation', 'systemctl:restart', 2, 'bash-c-subshell.jsonl'), ('package_query', 'pacman:-Q', 2, 'var-assign-query.jsonl'), ('package_query', 'pacman:-Qq', 2, 'cmdsub-query.jsonl')]) got=(0, [('host_mutation', 'hyprctl:keyword', 4, 'wrappers-hyprctl.jsonl'), ('host_mutation', 'omarchy-restart-waybar', 2, 'omarchy-verbs.jsonl'), ('host_mutation', 'omarchy-theme-set', 4, 'omarchy-verbs.jsonl'), ('host_mutation', 'pacman:-R', 2, 'env-prefix.jsonl'), ('host_mutation', 'pacman:-S', 2, 'eval-bang.jsonl'), ('host_mutation', 'pacman:-Syu', 2, 'compound-and.jsonl'), ('host_mutation', 'pacman:-U', 2, 'abs-path-pacman.jsonl'), ('host_mutation', 'pkill', 2, 'xargs-pkill.jsonl'), ('host_mutation', 'sudo', 2, 'bash-c-subshell.jsonl'), ('host_mutation', 'sudo', 2, 'compound-and.jsonl'), ('host_mutation', 'sudo', 2, 'eval-bang.jsonl'), ('host_mutation', 'systemctl:daemon-reload', 2, 'user-daemon-reload.jsonl'), ('host_mutation', 'systemctl:restart', 2, 'bash-c-subshell.jsonl'), ('package_query', 'pacman:-Q', 2, 'var-assign-query.jsonl'), ('package_query', 'pacman:-Qq', 2, 'cmdsub-query.jsonl')])
```

The kill attacks succeeded for run0 elevation, command lookup precision, quoted command substitution, and timeout duration stripping. They failed to kill the five mutants below.

## Surviving mutant diffs

Diffs were captured before restoration with `diff -u` against the pristine copy. Only the behavior-bearing changed line belongs to each mutation; surrounding context is unchanged.

### M01-libinput-omission

```diff
--- tools/mado-tripwire.py
+++ M01-libinput-omission.py
@@ -73,7 +73,7 @@
                       "grub-mkconfig", "systemd-inhibit", "reboot", "poweroff",
                       "shutdown", "halt", "systemd-run", "su"}
 PACKAGE_QUERY_BINS = {"expac", "pactree", "checkupdates", "pacman-conf"}
-LIVE_PROBE_BINS = {"journalctl", "libinput", "evtest", "wayland-info", "wev",
+LIVE_PROBE_BINS = {"journalctl", "evtest", "wayland-info", "wev",
                    "wlr-randr", "grim", "slurp", "hyprpicker", "busctl",
                    "dbus-send", "gdbus", "notify-send", "makoctl", "waybar",
                    "walker", "hypridle", "hyprlock", "alacritty", "pgrep",
```

### M03-aws-length

```diff
--- tools/mado-tripwire.py
+++ M03-aws-length.py
@@ -88,7 +88,7 @@
     r"^(agent\.db.*|.*\.db|.*\.db-(shm|wal)|auth\.json|oauth.*|credentials?(\.[a-z]+)?)$", re.I)
 SECRET_PATTERNS = (
     re.compile(r"(?<=://)[^/\s:@]+:[^/\s@]+(?=@)"),
-    re.compile(r"AKIA[0-9A-Z]{16}"),
+    re.compile(r"AKIA[0-9A-Z]{17}"),
     re.compile(r"[A-Za-z0-9_\-]{32,}"),
 )
 MAX_COMMAND = 240
```

### M06-xargs-I

```diff
--- tools/mado-tripwire.py
+++ M06-xargs-I.py
@@ -48,7 +48,7 @@
             "done", "case", "esac", "time", "!", "{", "}", "function"}
 SEPARATORS = {";", "&&", "||", "|", "&", "|&", ";;", "(", ")", "\n"}
 REDIRECTS = {">", ">>", "<", "<<", "<<<", ">&", "<&", ">|", "&>", "&>>", "<>"}
-XARGS_ARG_OPTS = {"-I", "-n", "-P", "-d", "-a", "-E", "-s", "-L", "-i"}
+XARGS_ARG_OPTS = {"-n", "-P", "-d", "-a", "-E", "-s", "-L", "-i"}
 
 SYSTEMCTL_QUERY = {"status", "show", "is-active", "is-enabled", "is-failed",
                    "is-system-running", "list-units", "list-unit-files",
```

### M08-refusal-case

```diff
--- tools/mado-tripwire.py
+++ M08-refusal-case.py
@@ -85,7 +85,7 @@
                       "subprocess.getstatusoutput",
                       "asyncio.create_subprocess_shell"}
 REFUSED_NAMES = re.compile(
-    r"^(agent\.db.*|.*\.db|.*\.db-(shm|wal)|auth\.json|oauth.*|credentials?(\.[a-z]+)?)$", re.I)
+    r"^(agent\.db.*|.*\.db|.*\.db-(shm|wal)|auth\.json|oauth.*|credentials?(\.[a-z]+)?)$", 0)
 SECRET_PATTERNS = (
     re.compile(r"(?<=://)[^/\s:@]+:[^/\s@]+(?=@)"),
     re.compile(r"AKIA[0-9A-Z]{16}"),
```

### M09-env-C

```diff
--- tools/mado-tripwire.py
+++ M09-env-C.py
@@ -231,7 +231,7 @@
             seg.pop(0)
             while seg and (seg[0].startswith("-") or re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", seg[0])):
                 opt = seg.pop(0)
-                if opt in ("-u", "-C", "-S") and seg:
+                if opt in ("-u", "-S") and seg:
                     seg.pop(0)
             changed = True
         elif base == "nice":
```

## Concrete survivor witnesses

Input `/tmp/MadoR17.MutateTripwire1.y22F4q/witnesses.jsonl` had exactly four assistant/bash `toolCall` records with these command strings (all synthetic data):

| JSONL line | tool_call_id | Command data |
|---:|---|---|
| 1 | `witness-libinput` | `libinput debug-events` |
| 2 | `witness-fake-aws` | `journalctl --since AKIA0000000000000000` |
| 3 | `witness-xargs-I` | `xargs -I SLOT pkill SLOT < pids` |
| 4 | `witness-env-C` | `env -C /tmp journalctl --no-pager` |

Its scan-reported SHA-256 was `cc6765fc351ceb0917bc8ed3897c224ddaf5fd413c2d7b0d89e1159b8d6e9f5e` in every capture. Every record had shape `{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"ID","name":"bash","arguments":{"command":"COMMAND"}}]}}`.

| Survivor | Pristine output at exact witness anchor | Mutated output at same anchor | Restored output |
|---|---|---|---|
| M01 | line 1 / `witness-libinput`: `live_probe`, rule `libinput` | Finding absent; aggregate live_probe count 3 → 2 | Exact original finding returns; count 3 |
| M03 | line 2 / `witness-fake-aws`: command `journalctl --since <redacted>` | command `journalctl --since AKIA0000000000000000` (deliberately fake identifier disclosed) | `<redacted>` returns |
| M06 | line 3 / `witness-xargs-I`: `host_mutation`, rule `pkill`, command `pkill SLOT` | Finding absent; aggregate host_mutation count 1 → 0 | Original finding/count returns |
| M09 | line 4 / `witness-env-C`: `live_probe`, rule `journalctl`, command `journalctl --no-pager` | Finding absent; aggregate live_probe count 3 → 2 | Original finding/count returns |

All these four-record scans exited **1** throughout because other unpermitted findings remained. The counterexamples are the exact finding/command deltas, not a claim that the whole combined scan became clean.

M08 used a separate, newly created synthetic JSONL file `/tmp/MadoR17.MutateTripwire1.y22F4q/AGENT.DB.TRIPWIRE-FIXTURE.jsonl`, SHA-256 `48f84bf300b57481beff00c0601876f63087bb048f0d0c622cb9f62640c2f397`. It was not a database or a real credential/auth file; it contained one harmless assistant/bash record (`witness-refusal-case`, command data `printf 'synthetic fixture only'`). Pristine/restored: first stdout line `MADO_TRIPWIRE: could_not_evaluate`, exit **2**, error `refused file name: /tmp/MadoR17.MutateTripwire1.y22F4q/AGENT.DB.TRIPWIRE-FIXTURE.jsonl`, `files: []`. Mutant: first line `MADO_TRIPWIRE: clean`, exit **0**, one parsed file/one bash call, no findings. Thus case-insensitive refusal was lost while all 58 selftests remained green.

Coverage anchors explaining the surviving defects:

- M01: `tools/mado-tripwire.py:76`; bare `libinput` detection is unprotected by these suites, even though `hardening/command-v-lookup-clean` uses the name in a non-executing lookup. This does not reproduce or invalidate the separately claimed real-transcript anchor.
- M03: `tools/mado-tripwire.py:91` and `:758–765`; selftest equality covers class/rule/line/optional basename plus exit and verdict prefix, not the redacted `command` field.
- M06: `tools/mado-tripwire.py:51,260–265`; `compound/xargs-pkill.jsonl:2` contains `xargs -r pkill < pids`, so losing an argument-taking `-I` option is not exercised.
- M08: `tools/mado-tripwire.py:88,591–592`; `hardening/expected.json:362–368` tests a lowercase refused name, not its uppercase variant.
- M09: `tools/mado-tripwire.py:234–235`; `compound/env-prefix.jsonl:2` contains `env FOO=1 pacman -R foo`, not `env -C DIR ...`.

### Captured witness-output projections

The following JSON objects are projections of actual scan stdout plus the captured process exit: class/rule/line/id/command, counts, and error are copied from the emitted verdict. Omitted file metadata and schema fields are not assertions. Shared pristine output applied to the byte-identical pristine script; restored output was separately captured for each survivor.

```jsonl
{"counts": {"host_mutation": 1, "live_probe": 3, "package_query": 0}, "error": null, "findings": [{"class": "live_probe", "command": "libinput debug-events", "line": 1, "rule": "libinput", "tool_call_id": "witness-libinput"}, {"class": "live_probe", "command": "journalctl --since <redacted>", "line": 2, "rule": "journalctl", "tool_call_id": "witness-fake-aws"}, {"class": "host_mutation", "command": "pkill SLOT", "line": 3, "rule": "pkill", "tool_call_id": "witness-xargs-I"}, {"class": "live_probe", "command": "journalctl --no-pager", "line": 4, "rule": "journalctl", "tool_call_id": "witness-env-C"}], "first_line": "MADO_TRIPWIRE: findings", "mutant": "shared", "process_exit": 1, "stage": "pristine", "witness": "witnesses.jsonl"}
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0}, "error": "refused file name: /tmp/MadoR17.MutateTripwire1.y22F4q/AGENT.DB.TRIPWIRE-FIXTURE.jsonl", "findings": [], "first_line": "MADO_TRIPWIRE: could_not_evaluate", "mutant": "shared", "process_exit": 2, "stage": "pristine", "witness": "AGENT.DB.TRIPWIRE-FIXTURE.jsonl"}
{"counts": {"host_mutation": 1, "live_probe": 2, "package_query": 0}, "error": null, "findings": [{"class": "live_probe", "command": "journalctl --since <redacted>", "line": 2, "rule": "journalctl", "tool_call_id": "witness-fake-aws"}, {"class": "host_mutation", "command": "pkill SLOT", "line": 3, "rule": "pkill", "tool_call_id": "witness-xargs-I"}, {"class": "live_probe", "command": "journalctl --no-pager", "line": 4, "rule": "journalctl", "tool_call_id": "witness-env-C"}], "first_line": "MADO_TRIPWIRE: findings", "mutant": "M01-libinput-omission", "process_exit": 1, "stage": "mutated", "witness": "witnesses.jsonl"}
{"counts": {"host_mutation": 1, "live_probe": 3, "package_query": 0}, "error": null, "findings": [{"class": "live_probe", "command": "libinput debug-events", "line": 1, "rule": "libinput", "tool_call_id": "witness-libinput"}, {"class": "live_probe", "command": "journalctl --since AKIA0000000000000000", "line": 2, "rule": "journalctl", "tool_call_id": "witness-fake-aws"}, {"class": "host_mutation", "command": "pkill SLOT", "line": 3, "rule": "pkill", "tool_call_id": "witness-xargs-I"}, {"class": "live_probe", "command": "journalctl --no-pager", "line": 4, "rule": "journalctl", "tool_call_id": "witness-env-C"}], "first_line": "MADO_TRIPWIRE: findings", "mutant": "M03-aws-length", "process_exit": 1, "stage": "mutated", "witness": "witnesses.jsonl"}
{"counts": {"host_mutation": 0, "live_probe": 3, "package_query": 0}, "error": null, "findings": [{"class": "live_probe", "command": "libinput debug-events", "line": 1, "rule": "libinput", "tool_call_id": "witness-libinput"}, {"class": "live_probe", "command": "journalctl --since <redacted>", "line": 2, "rule": "journalctl", "tool_call_id": "witness-fake-aws"}, {"class": "live_probe", "command": "journalctl --no-pager", "line": 4, "rule": "journalctl", "tool_call_id": "witness-env-C"}], "first_line": "MADO_TRIPWIRE: findings", "mutant": "M06-xargs-I", "process_exit": 1, "stage": "mutated", "witness": "witnesses.jsonl"}
{"counts": {"host_mutation": 1, "live_probe": 2, "package_query": 0}, "error": null, "findings": [{"class": "live_probe", "command": "libinput debug-events", "line": 1, "rule": "libinput", "tool_call_id": "witness-libinput"}, {"class": "live_probe", "command": "journalctl --since <redacted>", "line": 2, "rule": "journalctl", "tool_call_id": "witness-fake-aws"}, {"class": "host_mutation", "command": "pkill SLOT", "line": 3, "rule": "pkill", "tool_call_id": "witness-xargs-I"}], "first_line": "MADO_TRIPWIRE: findings", "mutant": "M09-env-C", "process_exit": 1, "stage": "mutated", "witness": "witnesses.jsonl"}
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0}, "error": null, "findings": [], "first_line": "MADO_TRIPWIRE: clean", "mutant": "M08-refusal-case", "process_exit": 0, "stage": "mutated", "witness": "AGENT.DB.TRIPWIRE-FIXTURE.jsonl"}
{"counts": {"host_mutation": 1, "live_probe": 3, "package_query": 0}, "error": null, "findings": [{"class": "live_probe", "command": "libinput debug-events", "line": 1, "rule": "libinput", "tool_call_id": "witness-libinput"}, {"class": "live_probe", "command": "journalctl --since <redacted>", "line": 2, "rule": "journalctl", "tool_call_id": "witness-fake-aws"}, {"class": "host_mutation", "command": "pkill SLOT", "line": 3, "rule": "pkill", "tool_call_id": "witness-xargs-I"}, {"class": "live_probe", "command": "journalctl --no-pager", "line": 4, "rule": "journalctl", "tool_call_id": "witness-env-C"}], "first_line": "MADO_TRIPWIRE: findings", "mutant": "M01-libinput-omission", "process_exit": 1, "stage": "restored", "witness": "witnesses.jsonl"}
{"counts": {"host_mutation": 1, "live_probe": 3, "package_query": 0}, "error": null, "findings": [{"class": "live_probe", "command": "libinput debug-events", "line": 1, "rule": "libinput", "tool_call_id": "witness-libinput"}, {"class": "live_probe", "command": "journalctl --since <redacted>", "line": 2, "rule": "journalctl", "tool_call_id": "witness-fake-aws"}, {"class": "host_mutation", "command": "pkill SLOT", "line": 3, "rule": "pkill", "tool_call_id": "witness-xargs-I"}, {"class": "live_probe", "command": "journalctl --no-pager", "line": 4, "rule": "journalctl", "tool_call_id": "witness-env-C"}], "first_line": "MADO_TRIPWIRE: findings", "mutant": "M03-aws-length", "process_exit": 1, "stage": "restored", "witness": "witnesses.jsonl"}
{"counts": {"host_mutation": 1, "live_probe": 3, "package_query": 0}, "error": null, "findings": [{"class": "live_probe", "command": "libinput debug-events", "line": 1, "rule": "libinput", "tool_call_id": "witness-libinput"}, {"class": "live_probe", "command": "journalctl --since <redacted>", "line": 2, "rule": "journalctl", "tool_call_id": "witness-fake-aws"}, {"class": "host_mutation", "command": "pkill SLOT", "line": 3, "rule": "pkill", "tool_call_id": "witness-xargs-I"}, {"class": "live_probe", "command": "journalctl --no-pager", "line": 4, "rule": "journalctl", "tool_call_id": "witness-env-C"}], "first_line": "MADO_TRIPWIRE: findings", "mutant": "M06-xargs-I", "process_exit": 1, "stage": "restored", "witness": "witnesses.jsonl"}
{"counts": {"host_mutation": 1, "live_probe": 3, "package_query": 0}, "error": null, "findings": [{"class": "live_probe", "command": "libinput debug-events", "line": 1, "rule": "libinput", "tool_call_id": "witness-libinput"}, {"class": "live_probe", "command": "journalctl --since <redacted>", "line": 2, "rule": "journalctl", "tool_call_id": "witness-fake-aws"}, {"class": "host_mutation", "command": "pkill SLOT", "line": 3, "rule": "pkill", "tool_call_id": "witness-xargs-I"}, {"class": "live_probe", "command": "journalctl --no-pager", "line": 4, "rule": "journalctl", "tool_call_id": "witness-env-C"}], "first_line": "MADO_TRIPWIRE: findings", "mutant": "M09-env-C", "process_exit": 1, "stage": "restored", "witness": "witnesses.jsonl"}
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0}, "error": "refused file name: /tmp/MadoR17.MutateTripwire1.y22F4q/AGENT.DB.TRIPWIRE-FIXTURE.jsonl", "findings": [], "first_line": "MADO_TRIPWIRE: could_not_evaluate", "mutant": "M08-refusal-case", "process_exit": 2, "stage": "restored", "witness": "AGENT.DB.TRIPWIRE-FIXTURE.jsonl"}
```

## Before / mutated / restored hashes and exact restoration

Common pristine/source SHA-256 (`H`):

```text
4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44
```

Every copy had before hash H. Restoration ran in `finally` by copying untouched `pristine.py` back over each mutant, including when a detector returned failure; all `cmp -s pristine.py COPY` exit codes were 0. Every restored selftest emitted `SELFTEST_SCRIPT_SHA256: H` and passed. The original lane source hash after the probe was also H.

| Copy | Before SHA-256 | Mutated SHA-256 | Restored SHA-256 | Exact-byte cmp exit |
|---|---|---|---|---:|
| `M01-libinput-omission.py` | H | `f43d1938a8b8a13f48495bb3133bbeb5e132c6b3259f7faae5ddd8a86e45b544` | H | 0 |
| `M02-run0-omission.py` | H | `bff22796b87b5f3f5fbedfd61474662720f99cf8605684d91fc6e64fc4afe963` | H | 0 |
| `M03-aws-length.py` | H | `799878123a2a9220bde3f51322ca49c16fa5de17f9d356f5d98a356d553538fb` | H | 0 |
| `M04-command-v.py` | H | `6be6151ee8ca1066ebc7f44810ebf5a8814d0bcb6a0166fc36af49333132148c` | H | 0 |
| `M05-dollar-substitution.py` | H | `ce080f0dd71e19bb62e54ea9ce1a4d45d43d3ce6f2fd0b164d8687c2342b0f86` | H | 0 |
| `M06-xargs-I.py` | H | `286240054332f98a6b876c05994ea011338b50e6733935d84858f54f8a1d74af` | H | 0 |
| `M07-timeout-argument.py` | H | `2958237d66c655b6b5a33694392b7c4c983cf5da7c78ece7f3a835f600a5fb3f` | H | 0 |
| `M08-refusal-case.py` | H | `02cd769eb528c609e06f9d3d19ab0af4a01bdb7f79e16f0c6a81debb86ad8798` | H | 0 |
| `M09-env-C.py` | H | `5a218709316bc2eca1d9b98a206212fe26cae44440a34cd0c0ae2d303a7cc115` | H | 0 |

No mutated script bytes remain: the nine scratch scripts are restored. Surviving diffs and witness receipts are retained in this report. The only lane file written by this item is this scoped report; no implementation or suite changes were made.

## Verdict boundary

**Attack partially succeeded:** five real, independently demonstrated behavioral regressions survived the complete supplied 9/9 + 16/16 + 33/33 detector. **Attack failed to evade** the detector for the other four mutants. The pristine/restored suite pass claims themselves were reproduced, not falsified. No contract change, integration decision, or ship judgment is made here.

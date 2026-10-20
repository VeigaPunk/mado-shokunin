# MutTripwireScan — d9a5a18 scan-classifier mutation probe
- Seat: `MadoR18.MutTripwireScan`. Measurement completed: `2026-10-20T15:45:47.733680Z`.
- Source revision: `d9a5a18e17cd3a68b52148fcc01c4a30e340ba98`; `tools/mado-tripwire.py` read with `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show d9a5a18:tools/mado-tripwire.py` (exit 0).
- Original tool: 37950 bytes; SHA-256 `H0 = 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072`.
- Isolated scratch root: `/tmp/mado-r18-muttripwirescan-_cezm1e0`. All twenty scratch tools were restored, not left mutated.
- Lane write scope: this report only. No lane source/fixture edits, git writes, jj invocation, host/package/UI commands, web fetches, installations, or tool updates. Commands resembling host operations below are transcript data only; none was executed.

## Axes and bounded method
Axes: detector sensitivity; clean-data specificity; byte-exact reversibility/isolation; evidence reproducibility; host safety. Independent copies were exercised with four concurrent detector workers, not nested agents. No mutation was retained.

Twenty independent single-point changes were made: six in `classify_pacman`, six in `strip_prefix`, four in `strip_comment`, four in `substitutions`. Each copy began as the exact git blob, received only its listed one-line behavioral change, and was restored by the inverse edit. PM05 replaces a two-line expression, but only its second line differs in bytes.

The unchanged detector was the tool’s own selftest runner, which checks process exit and the exact expected finding tuples; some cases additionally check labels/errors/attribution. Each of the four existing suites was run on **each copy** in pristine, mutated, and restored phases, at the same tool path. Selftest subprocesses were bounded to 150 seconds; their scan subprocesses retain the tool’s 120-second bound. There were no timeouts and no stderr output.

```text
python3 -I /tmp/mado-r18-muttripwirescan-_cezm1e0/<ID>.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core
python3 -I /tmp/mado-r18-muttripwirescan-_cezm1e0/<ID>.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound
python3 -I /tmp/mado-r18-muttripwirescan-_cezm1e0/<ID>.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening
python3 -I /tmp/mado-r18-muttripwirescan-_cezm1e0/<ID>.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/w2-regressions
```

A mutant is killed only when pristine detection passes, mutated detection rejects the changed behavior, and restoration passes. A failing baseline would be inconclusive. The twelve survivors also received proposed regression cases solely in scratch: selftest plus direct `--scan` on pristine, mutated, and restored bytes. These are supplemental demonstrations, not retroactive changes to the existing-suite verdict.

## Verdict
**8 killed, 12 survived, 0 inconclusive** against the existing 88 cases (9 core + 16 compound + 33 hardening + 30 w2). This is the result for these twenty chosen mutants, not a general coverage percentage.

- Pristine: all 20 copies passed 88/88; all 80 suite invocations exited 0.
- Mutated: eight mutants produced nine failed case executions; the other twelve passed 88/88. Every rejecting suite exited 1 on a finding/exit mismatch, not a syntax crash.
- Restored: all 20 copies again passed 88/88; all 80 suite invocations exited 0.
- Total existing-suite work: 240 selftest invocations, 5,280 case executions.
- Supplemental proposals: all 12 passed pristine and restored selftests (exit 0) and rejected their corresponding mutant (exit 1); 36 selftests plus 36 direct scans. Existing-suite survivors remain reported as survivors.
- Every existing selftest’s `SELFTEST_SCRIPT_SHA256` matched its phase’s measured source hash: `true` (240/240). Supplemental stderr empty: `true`.

## Mutants and actual existing-suite outputs
All line numbers below refer to the original git blob. A score is the actual `SELFTEST_SUMMARY` passed/total; the parenthesized number is the actual selftest exit. Pre/post columns cover all four suites, in core/compound/hardening/w2 order.

| ID | Function:line | Plausible defect | Core | Compound | Hardening | W2 | Pristine → restored exits | Verdict |
|---|---|---|---|---|---|---|---|---|
| PM01 | `classify_pacman:377` | Require exact long operation names; drop unique abbreviation recognition | 9/9 (0) | 16/16 (0) | 33/33 (0) | 29/30 (1) | 0,0,0,0 → 0,0,0,0 | killed |
| PM02 | `classify_pacman:400` | Check sysupgrade rather than refresh for files database mutation | 9/9 (0) | 16/16 (0) | 33/33 (0) | 29/30 (1) | 0,0,0,0 → 0,0,0,0 | killed |
| PM03 | `classify_pacman:407` | Omit download-only from sync mutation precedence | 9/9 (0) | 16/16 (0) | 33/33 (0) | 30/30 (0) | 0,0,0,0 → 0,0,0,0 | survived |
| PM04 | `classify_pacman:395` | Treat bare AUR helpers as package queries | 9/9 (0) | 16/16 (0) | 33/33 (0) | 30/30 (0) | 0,0,0,0 → 0,0,0,0 | survived |
| PM05 | `classify_pacman:390` | Map long clean modifier to query-print flag | 9/9 (0) | 16/16 (0) | 33/33 (0) | 30/30 (0) | 0,0,0,0 → 0,0,0,0 | survived |
| PM06 | `classify_pacman:409` | Omit print from sync query selectors | 8/9 (1) | 16/16 (0) | 32/33 (1) | 30/30 (0) | 0,0,0,0 → 0,0,0,0 | killed |
| PF01 | `strip_prefix:258` | Stop stripping shell keywords including time | 9/9 (0) | 16/16 (0) | 33/33 (0) | 29/30 (1) | 0,0,0,0 → 0,0,0,0 | killed |
| PF02 | `strip_prefix:267` | Treat command lookup target as an executed command | 9/9 (0) | 16/16 (0) | 32/33 (1) | 30/30 (0) | 0,0,0,0 → 0,0,0,0 | killed |
| PF03 | `strip_prefix:296` | Stop consuming env short unset option argument | 9/9 (0) | 16/16 (0) | 33/33 (0) | 30/30 (0) | 0,0,0,0 → 0,0,0,0 | survived |
| PF04 | `strip_prefix:311` | Stop consuming ionice class option argument | 9/9 (0) | 16/16 (0) | 33/33 (0) | 30/30 (0) | 0,0,0,0 → 0,0,0,0 | survived |
| PF05 | `strip_prefix:272` | Miss exec alternate argv0 option argument | 9/9 (0) | 16/16 (0) | 33/33 (0) | 29/30 (1) | 0,0,0,0 → 0,0,0,0 | killed |
| PF06 | `strip_prefix:318` | Stop consuming timeout long kill-after option argument | 9/9 (0) | 16/16 (0) | 33/33 (0) | 30/30 (0) | 0,0,0,0 → 0,0,0,0 | survived |
| CM01 | `strip_comment:179` | Treat a midword hash as comment start | 9/9 (0) | 16/16 (0) | 33/33 (0) | 29/30 (1) | 0,0,0,0 → 0,0,0,0 | killed |
| CM02 | `strip_comment:177` | Ignore double quote delimiters while finding comments | 9/9 (0) | 16/16 (0) | 33/33 (0) | 30/30 (0) | 0,0,0,0 → 0,0,0,0 | survived |
| CM03 | `strip_comment:174` | Stop honoring an unquoted backslash escape | 9/9 (0) | 16/16 (0) | 33/33 (0) | 30/30 (0) | 0,0,0,0 → 0,0,0,0 | survived |
| CM04 | `strip_comment:169` | Stop honoring an escape inside double quotes | 9/9 (0) | 16/16 (0) | 33/33 (0) | 30/30 (0) | 0,0,0,0 → 0,0,0,0 | survived |
| SU01 | `substitutions:231` | Stop recognizing dollar-parenthesis substitutions | 9/9 (0) | 16/16 (0) | 32/33 (1) | 30/30 (0) | 0,0,0,0 → 0,0,0,0 | killed |
| SU02 | `substitutions:242` | Stop recognizing backtick substitutions | 9/9 (0) | 16/16 (0) | 33/33 (0) | 30/30 (0) | 0,0,0,0 → 0,0,0,0 | survived |
| SU03 | `substitutions:228` | Scan command substitutions inside single-quoted data | 9/9 (0) | 16/16 (0) | 33/33 (0) | 30/30 (0) | 0,0,0,0 → 0,0,0,0 | survived |
| SU04 | `substitutions:227` | Mistake a single quote inside double quotes for a quote delimiter | 9/9 (0) | 16/16 (0) | 33/33 (0) | 30/30 (0) | 0,0,0,0 → 0,0,0,0 | survived |

### Exact one-line changes

Each entry is `original line` → `mutated line`; indentation is preserved. These changes define the probe without relying on a surviving modified scratch file.

**PM01 — classify_pacman:377**

```python
            hits = [k for k in long_ops if k.startswith(name)] if len(name) > 3 else []
```
→
```python
            hits = [k for k in long_ops if k == name] if len(name) > 3 else []
```

**PM02 — classify_pacman:400**

```python
    if letter == "F" and "y" in flags:
```
→
```python
    if letter == "F" and "u" in flags:
```

**PM03 — classify_pacman:407**

```python
        if flags & set("yuwc"):
```
→
```python
        if flags & set("yuc"):
```

**PM04 — classify_pacman:395**

```python
        if argv0 in ("yay", "paru"):
```
→
```python
        if argv0 in ():
```

**PM05 — classify_pacman:390**

```python
                       "--downloadonly": "w", "--clean": "c"}[a])
```
→
```python
                       "--downloadonly": "w", "--clean": "p"}[a])
```

**PM06 — classify_pacman:409**

```python
        if flags & set("silgp"):
```
→
```python
        if flags & set("silg"):
```

**PF01 — strip_prefix:258**

```python
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", head) or head in KEYWORDS:
```
→
```python
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", head) or head in ():
```

**PF02 — strip_prefix:267**

```python
            return []  # lookup only, nothing is executed
```
→
```python
            return seg[2:]  # lookup only, nothing is executed
```

**PF03 — strip_prefix:296**

```python
                if opt in ("-u", "-C", "--unset", "--chdir") and seg:
```
→
```python
                if opt in ("-C", "--unset", "--chdir") and seg:
```

**PF04 — strip_prefix:311**

```python
                if opt in ("-c", "-n", "-p") and seg:
```
→
```python
                if opt in ("-n", "-p") and seg:
```

**PF05 — strip_prefix:272**

```python
                if (base == "exec" and opt == "-a") or (base == "stdbuf" and opt in ("-i", "-o", "-e")):
```
→
```python
                if (base == "exec" and opt == "-b") or (base == "stdbuf" and opt in ("-i", "-o", "-e")):
```

**PF06 — strip_prefix:318**

```python
                if opt in ("-s", "-k", "--signal", "--kill-after") and seg:
```
→
```python
                if opt in ("-s", "-k", "--signal") and seg:
```

**CM01 — strip_comment:179**

```python
        elif ch == "#" and (i == 0 or line[i - 1] in " \t\n;&|()<>"):
```
→
```python
        elif ch == "#":
```

**CM02 — strip_comment:177**

```python
        elif ch in ("'", '"'):
```
→
```python
        elif ch in ("'",):
```

**CM03 — strip_comment:174**

```python
        elif ch == "\\":
```
→
```python
        elif False:
```

**CM04 — strip_comment:169**

```python
            if ch == "\\" and quote == '"':
```
→
```python
            if False:
```

**SU01 — substitutions:231**

```python
        if line.startswith("$(", i) and not line.startswith("$((", i):
```
→
```python
        if False:
```

**SU02 — substitutions:242**

```python
        if ch == "`":
```
→
```python
        if False:
```

**SU03 — substitutions:228**

```python
            if not dq_before:
```
→
```python
            if False:
```

**SU04 — substitutions:227**

```python
            dq_before = line.count('"', 0, i) % 2 == 1
```
→
```python
            dq_before = False
```

### Actual rejecting output

The exact failure lines and summary lines below are captured stdout, not inferred. Unlisted cases in these suites passed; all other suite runs had the full-pass summaries in the table. The expected detector is the named case’s exact finding/exit comparison.

**PM01 / w2-regressions — selftest exit 1, stderr empty**

```text
CASE pacman-abbreviated-long-op FAIL want=(1, [('host_mutation', 'pacman:--syn', 1, '')]) got=(1, [('package_query', 'pacman', 1, '')])
SELFTEST_SCRIPT_SHA256: fdb87d1ca8485bfc133138467a25d22c30b1e9f3127045dbca2b5a3feef67802
SELFTEST_SUMMARY: 29/30 passed failed=['pacman-abbreviated-long-op']
```

**PM02 / w2-regressions — selftest exit 1, stderr empty**

```text
CASE pacman-Fy-refresh FAIL want=(1, [('host_mutation', 'pacman:-Fy', 1, '')]) got=(1, [('package_query', 'pacman:-Fy', 1, '')])
SELFTEST_SCRIPT_SHA256: 461c4c9184dbc717e90c5f4ef6f42a88030e13b0910852b871bee6b649ee91df
SELFTEST_SUMMARY: 29/30 passed failed=['pacman-Fy-refresh']
```

**PM06 / core — selftest exit 1, stderr empty**

```text
CASE package-query-only FAIL want=(1, [('package_query', 'pacman:-Fl', 3, ''), ('package_query', 'pacman:-Qi', 1, ''), ('package_query', 'pacman:-Si', 2, ''), ('package_query', 'pacman:-Sp', 4, '')]) got=(1, [('host_mutation', 'pacman:-Sp', 4, ''), ('package_query', 'pacman:-Fl', 3, ''), ('package_query', 'pacman:-Qi', 1, ''), ('package_query', 'pacman:-Si', 2, '')])
SELFTEST_SCRIPT_SHA256: 02d079e48f58a73434dbb1979f65831c93e52240754a5635cf11fec130db2fd4
SELFTEST_SUMMARY: 8/9 passed failed=['package-query-only']
```

**PM06 / hardening — selftest exit 1, stderr empty**

```text
CASE pacman-sync-print-query FAIL want=(1, [('package_query', 'pacman:-Sp', 1, '')]) got=(1, [('host_mutation', 'pacman:-Sp', 1, '')])
SELFTEST_SCRIPT_SHA256: 02d079e48f58a73434dbb1979f65831c93e52240754a5635cf11fec130db2fd4
SELFTEST_SUMMARY: 32/33 passed failed=['pacman-sync-print-query']
```

**PF01 / w2-regressions — selftest exit 1, stderr empty**

```text
CASE nice-attached-and-time-p FAIL want=(1, [('host_mutation', 'pacman:-R', 1, ''), ('host_mutation', 'pacman:-Sy', 1, '')]) got=(1, [('host_mutation', 'pacman:-Sy', 1, '')])
SELFTEST_SCRIPT_SHA256: 4e0e2a956bd29a95af4749902846547141af5aa099aea3a45e04134749aabba9
SELFTEST_SUMMARY: 29/30 passed failed=['nice-attached-and-time-p']
```

**PF02 / hardening — selftest exit 1, stderr empty**

```text
CASE command-v-lookup-clean FAIL want=(0, []) got=(1, [('live_probe', 'libinput', 1, '')])
SELFTEST_SCRIPT_SHA256: 4671736e51e5ca3af504e7329d51c69b32d9dc4a901c9420f8bd1e28d344b8ba
SELFTEST_SUMMARY: 32/33 passed failed=['command-v-lookup-clean']
```

**PF05 / w2-regressions — selftest exit 1, stderr empty**

```text
CASE stdbuf-exec-args FAIL want=(1, [('host_mutation', 'pacman:-Sy', 1, ''), ('host_mutation', 'pkill', 1, '')]) got=(1, [('host_mutation', 'pacman:-Sy', 1, '')])
SELFTEST_SCRIPT_SHA256: 1d2d97aca2cee3ce8e0341dc3d8d35690c34d39c56f859308ce0c578e4cd83b4
SELFTEST_SUMMARY: 29/30 passed failed=['stdbuf-exec-args']
```

**CM01 / w2-regressions — selftest exit 1, stderr empty**

```text
CASE midword-hash-not-comment FAIL want=(1, [('host_mutation', 'pacman:-Syu', 1, ''), ('host_mutation', 'sudo', 1, '')]) got=(0, [])
SELFTEST_SCRIPT_SHA256: 25b30b486d382c9f2c89f806be04fdab3415d296242d5797dcb520e505d4d7c3
SELFTEST_SUMMARY: 29/30 passed failed=['midword-hash-not-comment']
```

**SU01 / hardening — selftest exit 1, stderr empty**

```text
CASE dollar-paren-in-double-quotes FAIL want=(1, [('package_query', 'pacman:-Q', 1, '')]) got=(0, [])
SELFTEST_SCRIPT_SHA256: 7ccc961b8cc243ee04f545354ab943beff153482959a0d2bbebd34b720417274
SELFTEST_SUMMARY: 32/33 passed failed=['dollar-paren-in-double-quotes']
```

The class-sensitive detector matters: PM01, PM02 and PM06 can leave an individual scan’s exit at 1 while misclassifying a finding. The selftest rejects the changed tuples. Conversely PF01/PF05 can leave a different same-line finding present; their missing finding is still caught.

## Surviving mutants: exercised regression-case proposals
These are additions proposed to the suite owner, not implemented lane changes. Each proposal uses the existing `mado-tripwire-selftest-v1` format. Their expected results preserve the baseline classifier contract. In particular PM03 demonstrates its existing conservative download-only/print precedence; it does **not** assert that a real pacman invocation with mixed flags performs a host mutation. No host binary semantics were exercised.

All commands below are inert `arguments.command` strings inside synthetic assistant tool-call JSONL. Each proposal was run with:

```text
python3 -I /tmp/mado-r18-muttripwirescan-_cezm1e0/pristine.py --selftest /tmp/mado-r18-muttripwirescan-_cezm1e0/proposals/<ID>
python3 -I /tmp/mado-r18-muttripwirescan-_cezm1e0/<ID>.py --selftest /tmp/mado-r18-muttripwirescan-_cezm1e0/proposals/<ID>
python3 -I /tmp/mado-r18-muttripwirescan-_cezm1e0/<ID>.py --scan /tmp/mado-r18-muttripwirescan-_cezm1e0/proposals/<ID>/fixture.jsonl [--permit package_query]
```

The first command supplied pristine bytes; the latter commands were run before and after restoration. The direct scan and selftest are distinct exits: an expected prohibited-command scan exits 1 while its passing selftest exits 0. `--permit package_query` was used only for PM03/PM04/PM05, exactly as their proposed case specifies.

### PM03: Omit download-only from sync mutation precedence

Transcript command strings (JSON encoding preserves quotes/backslashes and the SU03 trailing space):

```json
[
  "pacman -Swp walker"
]
```

Runnable `expected.json`:

```json
{
  "schema": "mado-tripwire-selftest-v1",
  "cases": [
    {
      "name": "pm03-regression-proposal",
      "args": [
        "fixture.jsonl"
      ],
      "want_exit": 1,
      "want_label": "findings",
      "want_findings": [
        {
          "class": "host_mutation",
          "rule": "pacman:-Swp",
          "line": 1
        }
      ],
      "permit": [
        "package_query"
      ]
    }
  ]
}
```

Fixture SHA-256: `5e02875351a33ff15d30eddae9b2846e157fa9fa08fcfe923a4119934d55d855`.

**pristine actual output — selftest exit 0; direct scan exit 1; stderr empty**

```text
CASE pm03-regression-proposal ok
SELFTEST_SCRIPT_SHA256: 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
SELFTEST_SUMMARY: 1/1 passed failed=[]
MADO_TRIPWIRE: findings
```

Direct-scan finding tuples: `[{"class":"host_mutation","rule":"pacman:-Swp","line":1}]`.

**mutated actual output — selftest exit 1; direct scan exit 0; stderr empty**

```text
CASE pm03-regression-proposal FAIL want=(1, [('host_mutation', 'pacman:-Swp', 1, '')]) got=(0, [('package_query', 'pacman:-Swp', 1, '')])
SELFTEST_SCRIPT_SHA256: 56a35053822550b65fcc7c3d05b0d0b41001f794f20e260608c6c69ae4b6015f
SELFTEST_SUMMARY: 0/1 passed failed=['pm03-regression-proposal']
MADO_TRIPWIRE: permitted_only
```

Direct-scan finding tuples: `[{"class":"package_query","rule":"pacman:-Swp","line":1}]`.

**restored actual output — selftest exit 0; direct scan exit 1; stderr empty**

```text
CASE pm03-regression-proposal ok
SELFTEST_SCRIPT_SHA256: 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
SELFTEST_SUMMARY: 1/1 passed failed=[]
MADO_TRIPWIRE: findings
```

Direct-scan finding tuples: `[{"class":"host_mutation","rule":"pacman:-Swp","line":1}]`.

### PM04: Treat bare AUR helpers as package queries

Transcript command strings (JSON encoding preserves quotes/backslashes and the SU03 trailing space):

```json
[
  "yay",
  "paru"
]
```

Runnable `expected.json`:

```json
{
  "schema": "mado-tripwire-selftest-v1",
  "cases": [
    {
      "name": "pm04-regression-proposal",
      "args": [
        "fixture.jsonl"
      ],
      "want_exit": 1,
      "want_label": "findings",
      "want_findings": [
        {
          "class": "host_mutation",
          "rule": "yay",
          "line": 1
        },
        {
          "class": "host_mutation",
          "rule": "paru",
          "line": 2
        }
      ],
      "permit": [
        "package_query"
      ]
    }
  ]
}
```

Fixture SHA-256: `e006d2441520578a0205b1158528094bd521d57a76b9a5911c1e98a131f202a7`.

**pristine actual output — selftest exit 0; direct scan exit 1; stderr empty**

```text
CASE pm04-regression-proposal ok
SELFTEST_SCRIPT_SHA256: 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
SELFTEST_SUMMARY: 1/1 passed failed=[]
MADO_TRIPWIRE: findings
```

Direct-scan finding tuples: `[{"class":"host_mutation","rule":"yay","line":1},{"class":"host_mutation","rule":"paru","line":2}]`.

**mutated actual output — selftest exit 1; direct scan exit 0; stderr empty**

```text
CASE pm04-regression-proposal FAIL want=(1, [('host_mutation', 'paru', 2, ''), ('host_mutation', 'yay', 1, '')]) got=(0, [('package_query', 'paru', 2, ''), ('package_query', 'yay', 1, '')])
SELFTEST_SCRIPT_SHA256: b8115f6ebe1fe6dbe53621cf4104b3c584b0c834cf26237bfc5cd5365c73198a
SELFTEST_SUMMARY: 0/1 passed failed=['pm04-regression-proposal']
MADO_TRIPWIRE: permitted_only
```

Direct-scan finding tuples: `[{"class":"package_query","rule":"yay","line":1},{"class":"package_query","rule":"paru","line":2}]`.

**restored actual output — selftest exit 0; direct scan exit 1; stderr empty**

```text
CASE pm04-regression-proposal ok
SELFTEST_SCRIPT_SHA256: 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
SELFTEST_SUMMARY: 1/1 passed failed=[]
MADO_TRIPWIRE: findings
```

Direct-scan finding tuples: `[{"class":"host_mutation","rule":"yay","line":1},{"class":"host_mutation","rule":"paru","line":2}]`.

### PM05: Map long clean modifier to query-print flag

Transcript command strings (JSON encoding preserves quotes/backslashes and the SU03 trailing space):

```json
[
  "pacman --sync --clean"
]
```

Runnable `expected.json`:

```json
{
  "schema": "mado-tripwire-selftest-v1",
  "cases": [
    {
      "name": "pm05-regression-proposal",
      "args": [
        "fixture.jsonl"
      ],
      "want_exit": 1,
      "want_label": "findings",
      "want_findings": [
        {
          "class": "host_mutation",
          "rule": "pacman:--sync",
          "line": 1
        }
      ],
      "permit": [
        "package_query"
      ]
    }
  ]
}
```

Fixture SHA-256: `b29c2ab29b8efc26d9e5882b247edccaab94065c588257d2265a186fa08124e8`.

**pristine actual output — selftest exit 0; direct scan exit 1; stderr empty**

```text
CASE pm05-regression-proposal ok
SELFTEST_SCRIPT_SHA256: 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
SELFTEST_SUMMARY: 1/1 passed failed=[]
MADO_TRIPWIRE: findings
```

Direct-scan finding tuples: `[{"class":"host_mutation","rule":"pacman:--sync","line":1}]`.

**mutated actual output — selftest exit 1; direct scan exit 0; stderr empty**

```text
CASE pm05-regression-proposal FAIL want=(1, [('host_mutation', 'pacman:--sync', 1, '')]) got=(0, [('package_query', 'pacman:--sync', 1, '')])
SELFTEST_SCRIPT_SHA256: 6cbb63929ff8548846b858ce854a55906cb1bea6c5dbc53416cc6f7fa1c07cc9
SELFTEST_SUMMARY: 0/1 passed failed=['pm05-regression-proposal']
MADO_TRIPWIRE: permitted_only
```

Direct-scan finding tuples: `[{"class":"package_query","rule":"pacman:--sync","line":1}]`.

**restored actual output — selftest exit 0; direct scan exit 1; stderr empty**

```text
CASE pm05-regression-proposal ok
SELFTEST_SCRIPT_SHA256: 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
SELFTEST_SUMMARY: 1/1 passed failed=[]
MADO_TRIPWIRE: findings
```

Direct-scan finding tuples: `[{"class":"host_mutation","rule":"pacman:--sync","line":1}]`.

### PF03: Stop consuming env short unset option argument

Transcript command strings (JSON encoding preserves quotes/backslashes and the SU03 trailing space):

```json
[
  "env -u LANG pacman -Sy"
]
```

Runnable `expected.json`:

```json
{
  "schema": "mado-tripwire-selftest-v1",
  "cases": [
    {
      "name": "pf03-regression-proposal",
      "args": [
        "fixture.jsonl"
      ],
      "want_exit": 1,
      "want_label": "findings",
      "want_findings": [
        {
          "class": "host_mutation",
          "rule": "pacman:-Sy",
          "line": 1
        }
      ]
    }
  ]
}
```

Fixture SHA-256: `fd293063521c3b523ef2f818c1e6070fe23e042148339e4b4395be44dc8c6241`.

**pristine actual output — selftest exit 0; direct scan exit 1; stderr empty**

```text
CASE pf03-regression-proposal ok
SELFTEST_SCRIPT_SHA256: 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
SELFTEST_SUMMARY: 1/1 passed failed=[]
MADO_TRIPWIRE: findings
```

Direct-scan finding tuples: `[{"class":"host_mutation","rule":"pacman:-Sy","line":1}]`.

**mutated actual output — selftest exit 1; direct scan exit 0; stderr empty**

```text
CASE pf03-regression-proposal FAIL want=(1, [('host_mutation', 'pacman:-Sy', 1, '')]) got=(0, [])
SELFTEST_SCRIPT_SHA256: cb8028e3a928f5ef5afe660e71bc81e3ac285206b06121c16a36c7d5338a8860
SELFTEST_SUMMARY: 0/1 passed failed=['pf03-regression-proposal']
MADO_TRIPWIRE: clean
```

Direct-scan finding tuples: `[]`.

**restored actual output — selftest exit 0; direct scan exit 1; stderr empty**

```text
CASE pf03-regression-proposal ok
SELFTEST_SCRIPT_SHA256: 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
SELFTEST_SUMMARY: 1/1 passed failed=[]
MADO_TRIPWIRE: findings
```

Direct-scan finding tuples: `[{"class":"host_mutation","rule":"pacman:-Sy","line":1}]`.

### PF04: Stop consuming ionice class option argument

Transcript command strings (JSON encoding preserves quotes/backslashes and the SU03 trailing space):

```json
[
  "ionice -c 3 pacman -Sy"
]
```

Runnable `expected.json`:

```json
{
  "schema": "mado-tripwire-selftest-v1",
  "cases": [
    {
      "name": "pf04-regression-proposal",
      "args": [
        "fixture.jsonl"
      ],
      "want_exit": 1,
      "want_label": "findings",
      "want_findings": [
        {
          "class": "host_mutation",
          "rule": "pacman:-Sy",
          "line": 1
        }
      ]
    }
  ]
}
```

Fixture SHA-256: `4530ab2a5be2fbf28722f0a1d71e6c9f7a26cf6c9bccd283cd2b629f3345b3c9`.

**pristine actual output — selftest exit 0; direct scan exit 1; stderr empty**

```text
CASE pf04-regression-proposal ok
SELFTEST_SCRIPT_SHA256: 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
SELFTEST_SUMMARY: 1/1 passed failed=[]
MADO_TRIPWIRE: findings
```

Direct-scan finding tuples: `[{"class":"host_mutation","rule":"pacman:-Sy","line":1}]`.

**mutated actual output — selftest exit 1; direct scan exit 0; stderr empty**

```text
CASE pf04-regression-proposal FAIL want=(1, [('host_mutation', 'pacman:-Sy', 1, '')]) got=(0, [])
SELFTEST_SCRIPT_SHA256: d10d2a04da5a1b18d2547f29c549f0975c7223eb1a39e5a711d6e4652a47e453
SELFTEST_SUMMARY: 0/1 passed failed=['pf04-regression-proposal']
MADO_TRIPWIRE: clean
```

Direct-scan finding tuples: `[]`.

**restored actual output — selftest exit 0; direct scan exit 1; stderr empty**

```text
CASE pf04-regression-proposal ok
SELFTEST_SCRIPT_SHA256: 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
SELFTEST_SUMMARY: 1/1 passed failed=[]
MADO_TRIPWIRE: findings
```

Direct-scan finding tuples: `[{"class":"host_mutation","rule":"pacman:-Sy","line":1}]`.

### PF06: Stop consuming timeout long kill-after option argument

Transcript command strings (JSON encoding preserves quotes/backslashes and the SU03 trailing space):

```json
[
  "timeout --kill-after 1s 5s pacman -Sy"
]
```

Runnable `expected.json`:

```json
{
  "schema": "mado-tripwire-selftest-v1",
  "cases": [
    {
      "name": "pf06-regression-proposal",
      "args": [
        "fixture.jsonl"
      ],
      "want_exit": 1,
      "want_label": "findings",
      "want_findings": [
        {
          "class": "host_mutation",
          "rule": "pacman:-Sy",
          "line": 1
        }
      ]
    }
  ]
}
```

Fixture SHA-256: `0cdb56a095dfb0a479ab435d86ce8068ca5d30ad54236b0ea4848d6d8ad66cde`.

**pristine actual output — selftest exit 0; direct scan exit 1; stderr empty**

```text
CASE pf06-regression-proposal ok
SELFTEST_SCRIPT_SHA256: 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
SELFTEST_SUMMARY: 1/1 passed failed=[]
MADO_TRIPWIRE: findings
```

Direct-scan finding tuples: `[{"class":"host_mutation","rule":"pacman:-Sy","line":1}]`.

**mutated actual output — selftest exit 1; direct scan exit 0; stderr empty**

```text
CASE pf06-regression-proposal FAIL want=(1, [('host_mutation', 'pacman:-Sy', 1, '')]) got=(0, [])
SELFTEST_SCRIPT_SHA256: 04e79a8c6e905dc1c6153b7a72eae9556bacae746d3a3bd3a0c299ebe3ff44e8
SELFTEST_SUMMARY: 0/1 passed failed=['pf06-regression-proposal']
MADO_TRIPWIRE: clean
```

Direct-scan finding tuples: `[]`.

**restored actual output — selftest exit 0; direct scan exit 1; stderr empty**

```text
CASE pf06-regression-proposal ok
SELFTEST_SCRIPT_SHA256: 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
SELFTEST_SUMMARY: 1/1 passed failed=[]
MADO_TRIPWIRE: findings
```

Direct-scan finding tuples: `[{"class":"host_mutation","rule":"pacman:-Sy","line":1}]`.

### CM02: Ignore double quote delimiters while finding comments

Transcript command strings (JSON encoding preserves quotes/backslashes and the SU03 trailing space):

```json
[
  "printf '%s' \" # literal\"; pacman -Q"
]
```

Runnable `expected.json`:

```json
{
  "schema": "mado-tripwire-selftest-v1",
  "cases": [
    {
      "name": "cm02-regression-proposal",
      "args": [
        "fixture.jsonl"
      ],
      "want_exit": 1,
      "want_label": "findings",
      "want_findings": [
        {
          "class": "package_query",
          "rule": "pacman:-Q",
          "line": 1
        }
      ]
    }
  ]
}
```

Fixture SHA-256: `7a27e2587c9887e3e2d71d0652f6c2162975f8694460b39eff60a2ce702725e8`.

**pristine actual output — selftest exit 0; direct scan exit 1; stderr empty**

```text
CASE cm02-regression-proposal ok
SELFTEST_SCRIPT_SHA256: 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
SELFTEST_SUMMARY: 1/1 passed failed=[]
MADO_TRIPWIRE: findings
```

Direct-scan finding tuples: `[{"class":"package_query","rule":"pacman:-Q","line":1}]`.

**mutated actual output — selftest exit 1; direct scan exit 0; stderr empty**

```text
CASE cm02-regression-proposal FAIL want=(1, [('package_query', 'pacman:-Q', 1, '')]) got=(0, [])
SELFTEST_SCRIPT_SHA256: 3593c58ebdd1e4907db007923ee73c7a5269e684078988ef8bbbd4522f780c94
SELFTEST_SUMMARY: 0/1 passed failed=['cm02-regression-proposal']
MADO_TRIPWIRE: clean
```

Direct-scan finding tuples: `[]`.

**restored actual output — selftest exit 0; direct scan exit 1; stderr empty**

```text
CASE cm02-regression-proposal ok
SELFTEST_SCRIPT_SHA256: 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
SELFTEST_SUMMARY: 1/1 passed failed=[]
MADO_TRIPWIRE: findings
```

Direct-scan finding tuples: `[{"class":"package_query","rule":"pacman:-Q","line":1}]`.

### CM03: Stop honoring an unquoted backslash escape

Transcript command strings (JSON encoding preserves quotes/backslashes and the SU03 trailing space):

```json
[
  "printf '%s' \\\" # ; pacman -Q"
]
```

Runnable `expected.json`:

```json
{
  "schema": "mado-tripwire-selftest-v1",
  "cases": [
    {
      "name": "cm03-regression-proposal",
      "args": [
        "fixture.jsonl"
      ],
      "want_exit": 0,
      "want_label": "clean",
      "want_findings": []
    }
  ]
}
```

Fixture SHA-256: `d5056f851e9273f91fe2467aef0e853aa9f5f6cdfb143b8453141e46345f8594`.

**pristine actual output — selftest exit 0; direct scan exit 0; stderr empty**

```text
CASE cm03-regression-proposal ok
SELFTEST_SCRIPT_SHA256: 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
SELFTEST_SUMMARY: 1/1 passed failed=[]
MADO_TRIPWIRE: clean
```

Direct-scan finding tuples: `[]`.

**mutated actual output — selftest exit 1; direct scan exit 1; stderr empty**

```text
CASE cm03-regression-proposal FAIL want=(0, []) got=(1, [('package_query', 'pacman:-Q', 1, '')])
SELFTEST_SCRIPT_SHA256: 6233bb260a4c44ee8c01ffa23df7689e0ecd420b3d377967034e9f48f06e671a
SELFTEST_SUMMARY: 0/1 passed failed=['cm03-regression-proposal']
MADO_TRIPWIRE: findings
```

Direct-scan finding tuples: `[{"class":"package_query","rule":"pacman:-Q","line":1}]`.

**restored actual output — selftest exit 0; direct scan exit 0; stderr empty**

```text
CASE cm03-regression-proposal ok
SELFTEST_SCRIPT_SHA256: 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
SELFTEST_SUMMARY: 1/1 passed failed=[]
MADO_TRIPWIRE: clean
```

Direct-scan finding tuples: `[]`.

### CM04: Stop honoring an escape inside double quotes

Transcript command strings (JSON encoding preserves quotes/backslashes and the SU03 trailing space):

```json
[
  "printf '%s' \"say \\\" # data\"; pacman -Q"
]
```

Runnable `expected.json`:

```json
{
  "schema": "mado-tripwire-selftest-v1",
  "cases": [
    {
      "name": "cm04-regression-proposal",
      "args": [
        "fixture.jsonl"
      ],
      "want_exit": 1,
      "want_label": "findings",
      "want_findings": [
        {
          "class": "package_query",
          "rule": "pacman:-Q",
          "line": 1
        }
      ]
    }
  ]
}
```

Fixture SHA-256: `3782c3ec25f1bac315b8d09ea42695850343e810f7e3b99a2b36abf735b87c5c`.

**pristine actual output — selftest exit 0; direct scan exit 1; stderr empty**

```text
CASE cm04-regression-proposal ok
SELFTEST_SCRIPT_SHA256: 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
SELFTEST_SUMMARY: 1/1 passed failed=[]
MADO_TRIPWIRE: findings
```

Direct-scan finding tuples: `[{"class":"package_query","rule":"pacman:-Q","line":1}]`.

**mutated actual output — selftest exit 1; direct scan exit 0; stderr empty**

```text
CASE cm04-regression-proposal FAIL want=(1, [('package_query', 'pacman:-Q', 1, '')]) got=(0, [])
SELFTEST_SCRIPT_SHA256: fe1e2c28d23b93d48632fce52da1b8e142a61fca168cb3f56593bdca6e24a9a3
SELFTEST_SUMMARY: 0/1 passed failed=['cm04-regression-proposal']
MADO_TRIPWIRE: clean
```

Direct-scan finding tuples: `[]`.

**restored actual output — selftest exit 0; direct scan exit 1; stderr empty**

```text
CASE cm04-regression-proposal ok
SELFTEST_SCRIPT_SHA256: 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
SELFTEST_SUMMARY: 1/1 passed failed=[]
MADO_TRIPWIRE: findings
```

Direct-scan finding tuples: `[{"class":"package_query","rule":"pacman:-Q","line":1}]`.

### SU02: Stop recognizing backtick substitutions

Transcript command strings (JSON encoding preserves quotes/backslashes and the SU03 trailing space):

```json
[
  "printf '%s' \"`pacman -Q`\""
]
```

Runnable `expected.json`:

```json
{
  "schema": "mado-tripwire-selftest-v1",
  "cases": [
    {
      "name": "su02-regression-proposal",
      "args": [
        "fixture.jsonl"
      ],
      "want_exit": 1,
      "want_label": "findings",
      "want_findings": [
        {
          "class": "package_query",
          "rule": "pacman:-Q",
          "line": 1
        }
      ]
    }
  ]
}
```

Fixture SHA-256: `e66804be9c5369ee5262dbfa1543816a8e7e638cd45381d23381df3dabef9105`.

**pristine actual output — selftest exit 0; direct scan exit 1; stderr empty**

```text
CASE su02-regression-proposal ok
SELFTEST_SCRIPT_SHA256: 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
SELFTEST_SUMMARY: 1/1 passed failed=[]
MADO_TRIPWIRE: findings
```

Direct-scan finding tuples: `[{"class":"package_query","rule":"pacman:-Q","line":1}]`.

**mutated actual output — selftest exit 1; direct scan exit 0; stderr empty**

```text
CASE su02-regression-proposal FAIL want=(1, [('package_query', 'pacman:-Q', 1, '')]) got=(0, [])
SELFTEST_SCRIPT_SHA256: 732c6ad9fc5a87fbb809a2e665638875bdc8f8479fa491101436f0d192b46ff1
SELFTEST_SUMMARY: 0/1 passed failed=['su02-regression-proposal']
MADO_TRIPWIRE: clean
```

Direct-scan finding tuples: `[]`.

**restored actual output — selftest exit 0; direct scan exit 1; stderr empty**

```text
CASE su02-regression-proposal ok
SELFTEST_SCRIPT_SHA256: 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
SELFTEST_SUMMARY: 1/1 passed failed=[]
MADO_TRIPWIRE: findings
```

Direct-scan finding tuples: `[{"class":"package_query","rule":"pacman:-Q","line":1}]`.

### SU03: Scan command substitutions inside single-quoted data

Transcript command strings (JSON encoding preserves quotes/backslashes and the SU03 trailing space):

```json
[
  "printf '%s' '$(pacman -Q)' "
]
```

Runnable `expected.json`:

```json
{
  "schema": "mado-tripwire-selftest-v1",
  "cases": [
    {
      "name": "su03-regression-proposal",
      "args": [
        "fixture.jsonl"
      ],
      "want_exit": 0,
      "want_label": "clean",
      "want_findings": []
    }
  ]
}
```

Fixture SHA-256: `1d4d0f9f6c9930c544bffc9a6b5f45e48246ef2884020aecfb8ad7eff12a6d6b`.

**pristine actual output — selftest exit 0; direct scan exit 0; stderr empty**

```text
CASE su03-regression-proposal ok
SELFTEST_SCRIPT_SHA256: 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
SELFTEST_SUMMARY: 1/1 passed failed=[]
MADO_TRIPWIRE: clean
```

Direct-scan finding tuples: `[]`.

**mutated actual output — selftest exit 1; direct scan exit 1; stderr empty**

```text
CASE su03-regression-proposal FAIL want=(0, []) got=(1, [('package_query', 'pacman:-Q', 1, '')])
SELFTEST_SCRIPT_SHA256: e7059c215725c2580550abda14475b9d78e700af817446bb27bb03d9fa092f1a
SELFTEST_SUMMARY: 0/1 passed failed=['su03-regression-proposal']
MADO_TRIPWIRE: findings
```

Direct-scan finding tuples: `[{"class":"package_query","rule":"pacman:-Q","line":1}]`.

**restored actual output — selftest exit 0; direct scan exit 0; stderr empty**

```text
CASE su03-regression-proposal ok
SELFTEST_SCRIPT_SHA256: 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
SELFTEST_SUMMARY: 1/1 passed failed=[]
MADO_TRIPWIRE: clean
```

Direct-scan finding tuples: `[]`.

### SU04: Mistake a single quote inside double quotes for a quote delimiter

Transcript command strings (JSON encoding preserves quotes/backslashes and the SU03 trailing space):

```json
[
  "printf '%s' \"it's $(pacman -Q)\""
]
```

Runnable `expected.json`:

```json
{
  "schema": "mado-tripwire-selftest-v1",
  "cases": [
    {
      "name": "su04-regression-proposal",
      "args": [
        "fixture.jsonl"
      ],
      "want_exit": 1,
      "want_label": "findings",
      "want_findings": [
        {
          "class": "package_query",
          "rule": "pacman:-Q",
          "line": 1
        }
      ]
    }
  ]
}
```

Fixture SHA-256: `ad62729b2c6c3500645c88938244f39afd11815e3a53dc1a3b87f50a87444ab8`.

**pristine actual output — selftest exit 0; direct scan exit 1; stderr empty**

```text
CASE su04-regression-proposal ok
SELFTEST_SCRIPT_SHA256: 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
SELFTEST_SUMMARY: 1/1 passed failed=[]
MADO_TRIPWIRE: findings
```

Direct-scan finding tuples: `[{"class":"package_query","rule":"pacman:-Q","line":1}]`.

**mutated actual output — selftest exit 1; direct scan exit 0; stderr empty**

```text
CASE su04-regression-proposal FAIL want=(1, [('package_query', 'pacman:-Q', 1, '')]) got=(0, [])
SELFTEST_SCRIPT_SHA256: f3fb49b65226dd4d1a35f22c6457d7b6d6689950ca611bb055e313eabed4ec5b
SELFTEST_SUMMARY: 0/1 passed failed=['su04-regression-proposal']
MADO_TRIPWIRE: clean
```

Direct-scan finding tuples: `[]`.

**restored actual output — selftest exit 0; direct scan exit 1; stderr empty**

```text
CASE su04-regression-proposal ok
SELFTEST_SCRIPT_SHA256: 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072
SELFTEST_SUMMARY: 1/1 passed failed=[]
MADO_TRIPWIRE: findings
```

Direct-scan finding tuples: `[{"class":"package_query","rule":"pacman:-Q","line":1}]`.

### Materializing the proposal fixtures
For each proposal, put its shown command-string array in `commands` and its ID in `mid`. The following exact recipe produces the exercised `fixture.jsonl` bytes. Its output is transcript data; never run the resulting command strings in a shell. Keep these fixture files in scratch, not the lane, unless the suite owner separately integrates them.

```python
import json
raw = "".join(
    json.dumps({
        "type": "message",
        "timestamp": "2026-10-20T00:00:00Z",
        "message": {"role": "assistant", "content": [{
            "type": "toolCall", "id": mid + "-" + str(i),
            "name": "bash", "arguments": {"command": command}
        }]}
    }, sort_keys=True) + "\n"
    for i, command in enumerate(commands, 1)
)
# Write raw as UTF-8 to fixture.jsonl beside the shown expected.json.
```

## Restoration and hashes
For **every** ID below, before SHA-256 and restored SHA-256 were both `H0 = 962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072`. Each `cmp -s /tmp/mado-r18-muttripwirescan-_cezm1e0/pristine.py /tmp/mado-r18-muttripwirescan-_cezm1e0/<ID>.py` also exited 0 after restoration. Thus restoration was byte-exact, not merely behaviorally equivalent. The independent pristine copy also hashes to H0.

| ID | Before SHA-256 | Mutated SHA-256 | Restored SHA-256 | `cmp` exit | Restored cases |
|---|---|---|---|---|---|
| PM01 | H0 | `fdb87d1ca8485bfc133138467a25d22c30b1e9f3127045dbca2b5a3feef67802` | H0 | 0 | 88/88 |
| PM02 | H0 | `461c4c9184dbc717e90c5f4ef6f42a88030e13b0910852b871bee6b649ee91df` | H0 | 0 | 88/88 |
| PM03 | H0 | `56a35053822550b65fcc7c3d05b0d0b41001f794f20e260608c6c69ae4b6015f` | H0 | 0 | 88/88 |
| PM04 | H0 | `b8115f6ebe1fe6dbe53621cf4104b3c584b0c834cf26237bfc5cd5365c73198a` | H0 | 0 | 88/88 |
| PM05 | H0 | `6cbb63929ff8548846b858ce854a55906cb1bea6c5dbc53416cc6f7fa1c07cc9` | H0 | 0 | 88/88 |
| PM06 | H0 | `02d079e48f58a73434dbb1979f65831c93e52240754a5635cf11fec130db2fd4` | H0 | 0 | 88/88 |
| PF01 | H0 | `4e0e2a956bd29a95af4749902846547141af5aa099aea3a45e04134749aabba9` | H0 | 0 | 88/88 |
| PF02 | H0 | `4671736e51e5ca3af504e7329d51c69b32d9dc4a901c9420f8bd1e28d344b8ba` | H0 | 0 | 88/88 |
| PF03 | H0 | `cb8028e3a928f5ef5afe660e71bc81e3ac285206b06121c16a36c7d5338a8860` | H0 | 0 | 88/88 |
| PF04 | H0 | `d10d2a04da5a1b18d2547f29c549f0975c7223eb1a39e5a711d6e4652a47e453` | H0 | 0 | 88/88 |
| PF05 | H0 | `1d2d97aca2cee3ce8e0341dc3d8d35690c34d39c56f859308ce0c578e4cd83b4` | H0 | 0 | 88/88 |
| PF06 | H0 | `04e79a8c6e905dc1c6153b7a72eae9556bacae746d3a3bd3a0c299ebe3ff44e8` | H0 | 0 | 88/88 |
| CM01 | H0 | `25b30b486d382c9f2c89f806be04fdab3415d296242d5797dcb520e505d4d7c3` | H0 | 0 | 88/88 |
| CM02 | H0 | `3593c58ebdd1e4907db007923ee73c7a5269e684078988ef8bbbd4522f780c94` | H0 | 0 | 88/88 |
| CM03 | H0 | `6233bb260a4c44ee8c01ffa23df7689e0ecd420b3d377967034e9f48f06e671a` | H0 | 0 | 88/88 |
| CM04 | H0 | `fe1e2c28d23b93d48632fce52da1b8e142a61fca168cb3f56593bdca6e24a9a3` | H0 | 0 | 88/88 |
| SU01 | H0 | `7ccc961b8cc243ee04f545354ab943beff153482959a0d2bbebd34b720417274` | H0 | 0 | 88/88 |
| SU02 | H0 | `732c6ad9fc5a87fbb809a2e665638875bdc8f8479fa491101436f0d192b46ff1` | H0 | 0 | 88/88 |
| SU03 | H0 | `e7059c215725c2580550abda14475b9d78e700af817446bb27bb03d9fa092f1a` | H0 | 0 | 88/88 |
| SU04 | H0 | `f3fb49b65226dd4d1a35f22c6457d7b6d6689950ca611bb055e313eabed4ec5b` | H0 | 0 | 88/88 |

Suite expected-spec SHA-256 values were measured before pristine execution and after restoration and were unchanged:

```text
e8aff6efb9ce06eefac457d8dc8afa79405f2167c426f2c23900bc314b06b920  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/expected.json
eef778eac31181f9c76519ff7a0b01c368e2f5255c12791e13c0f0fc7ce065e2  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound/expected.json
913a5e91efe7412aeaf8954b4546fdaa98d9575f384ac90fc292aaf15aae1a01  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening/expected.json
8a98c12b706203b710e9075117e0883987a453da4fa59ba156894de86b9ebd2e  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/w2-regressions/expected.json
```

## Tooling and scope limits

- `Python 3.14.8`.
- `git version 2.56.0`.
- `sha256sum (GNU coreutils) 9.12`.
- `cmp (GNU diffutils) 3.12`.

No tools were installed or updated. No lane gates or whole-project verification were run. This probe used synthetic pre-existing/supplemental transcripts only; it did not read private OMP session transcripts or credential databases, did not use the frozen-replay implementation, and does not establish safety for unsupported shell syntax or commands outside scanned transcript data. No source fix, policy/contract change, or integration is proposed by the mutation verdict itself.

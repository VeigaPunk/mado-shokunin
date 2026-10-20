# MutVcsTip — 2 killed, 2 survived; exact restoration confirmed

## Scope and axes

Assigned probe only: challenge `classify_git` / `classify_jj` at **e629f731172b8238caffe50f152217ce56535fb4**, independently mutating `JJ_NO_SNAPSHOT`, `JJ_SUB_ARG_OPTS`, `GIT_WRITE`, and the `--ignore-working-copy` check. Axes: **detector recall**, **non-write precision**, and **isolation / byte-exact restoration**. These are probe dimensions, not a round-admission judgment.

Read the round-20 declarations in `/home/vgpnk/Projects/shokunin/mado-shokunin/SCORECARD.md:1228-1283` and the C3/routed-defect sections in `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-19-verifier-spotcheck.md:63-90,145-154`. No existing failure was rerun for confirmation.

All runnable copies, copied suites, proposals, and receipts are isolated under:

`/tmp/mado-r20-MutVcsTip-wwm_nzvv`

The **only lane write** is this report. No tracked lane tool, suite, expectation, or sibling file was changed. No subagent or other agent runtime was invoked.

## Pinned inputs and detector

Read-only Git commands resolved and copied the requested revision:

```text
git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse e629f73
e629f731172b8238caffe50f152217ce56535fb4

git -C /home/vgpnk/Projects/shokunin/mado-shokunin show e629f731172b8238caffe50f152217ce56535fb4:tools/mado-tripwire.py
copied bytes: 90536
sha256: 367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d
```

An archive of the revision's round-17/18/19 `tripwire` directories supplied the **11 existing suites, 247 cases**. Archive SHA-256: `ebaec2a5c15822c5d545c9e7cb4e5b50226892c95c00a36980a77d52189a3b6c`. Manifest: `/tmp/mado-r20-MutVcsTip-wwm_nzvv/fixture-manifest.json`. This uses pinned Git bytes, not concurrently editable lane fixtures. There is no scratch clone HEAD: this probe used a tool copy and fixture archive from the resolved commit.

**Same bounded detector per mutant:** run every copied suite with that mutant's same tool path and cwd, first pristine, then with one mutation, then after restoration. Each direct selftest process had a 120-second timeout; four independent mutant copies ran concurrently. All 132 suite invocations completed without timeout, malformed summary, or stderr. The selftest implementation at the pinned tool's lines 1982-2077 invokes only isolated Python `--scan` / `--frozen` processes. Transcript commands and Python fixture bodies were **never executed**.

Exact example, run unchanged in each phase for M1:

```text
/usr/bin/python -I /tmp/mado-r20-MutVcsTip-wwm_nzvv/M1-no-snapshot-version/mado-tripwire.py --selftest /tmp/mado-r20-MutVcsTip-wwm_nzvv/pinned/.ufo/waves/round-19/tripwire/r19-vcs
cwd=/tmp/mado-r20-MutVcsTip-wwm_nzvv/M1-no-snapshot-version
```

M2/M3/M4 used the corresponding directory names in the results table. Every exact argv, cwd, exit, summary, failure row, and stdout digest is preserved in `/tmp/mado-r20-MutVcsTip-wwm_nzvv/probe-results.json`, SHA-256 **`b1c7ab4b8431fb5283de906278761b7f52e39e0ae2ec2bd9e8abc6becb2e0ef0`**. The counts below were derived by summing the emitted `SELFTEST_SUMMARY` numerators/denominators in that bundle, not from a historical receipt.

## Mutations, expected detectors, and verdicts

Each mutation changes one behavior-bearing point; none are combined. Locations refer to `tools/mado-tripwire.py` at the pinned revision.

| ID / isolated directory | Smallest defect | Expected detector | Pristine | Mutated | Restored | Verdict on existing suites |
|---|---|---|---:|---:|---:|---|
| M1 / `M1-no-snapshot-version` | Line 133: remove `"version"` from `JJ_NO_SNAPSHOT` | `r19-vcs/jj-ignore-working-copy-clean`, if it exercises the named non-snapshot version verb | 247/247 | 247/247 | 247/247 | **SURVIVED** |
| M2 / `M2-sub-arg-color` | Lines 136-137: remove `"--color"` from `JJ_SUB_ARG_OPTS` | `r19-vcs/jj-mutation-with-ignore`, if it covers a nested write with an intervening option/value | 247/247 | 247/247 | 247/247 | **SURVIVED** |
| M3 / `M3-git-write-commit` | Lines 138-139: remove `"commit"` from `GIT_WRITE` | `r19-vcs/git-writes`, eval commit cases, and hardening's multiline commit | 247/247 | 238/247 | 247/247 | **KILLED** |
| M4 / `M4-ignore-copy-after-separator` | Line 500: change `return "--ignore-working-copy" in head` to `return "--ignore-working-copy" in args` | `r19-vcs/jj-dashdash-paths` | 247/247 | 246/247 | 247/247 | **KILLED** |

**Total: 2 killed / 2 survived / 0 inconclusive.** A baseline failure would have been inconclusive; none occurred. Survivor verdicts refer to the unchanged existing suites, not the supplementary proposals below.

### All suites, per mutant

Entries are passed/total. Every pristine and restored run for every mutant matched the P/R column and exited 0. Mutated exits were 0 except the three starred cells, which exited 1.

| Pinned suite suffix under `pinned/.ufo/waves/` | P/R, each mutant | M1 | M2 | M3 | M4 |
|---|---:|---:|---:|---:|---:|
| `round-17/tripwire/compound` | 16/16 | 16/16 | 16/16 | 16/16 | 16/16 |
| `round-17/tripwire/core` | 9/9 | 9/9 | 9/9 | 9/9 | 9/9 |
| `round-17/tripwire/hardening` | 33/33 | 33/33 | 33/33 | **32/33*** | 33/33 |
| `round-17/tripwire/w2-regressions` | 30/30 | 30/30 | 30/30 | 30/30 | 30/30 |
| `round-18/tripwire/frozen` | 31/31 | 31/31 | 31/31 | 31/31 | 31/31 |
| `round-18/tripwire/r18-failsafe` | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| `round-19/tripwire/r19-bashcvar` | 45/45 | 45/45 | 45/45 | 45/45 | 45/45 |
| `round-19/tripwire/r19-frozen-f1f2` | 13/13 | 13/13 | 13/13 | 13/13 | 13/13 |
| `round-19/tripwire/r19-helperfn` | 34/34 | 34/34 | 34/34 | 34/34 | 34/34 |
| `round-19/tripwire/r19-installers` | 18/18 | 18/18 | 18/18 | 18/18 | 18/18 |
| `round-19/tripwire/r19-vcs` | 17/17 | 17/17 | 17/17 | **9/17*** | **16/17*** |

### Actual detector output

M1, `/tmp/mado-r20-MutVcsTip-wwm_nzvv/M1-no-snapshot-version/mutated-r19-vcs.stdout:18-19`:

```text
SELFTEST_SCRIPT_SHA256: 84417830954f752fb00e34f5da7f3a2239e5310d58530691812a3ccf55454b3c
SELFTEST_SUMMARY: 17/17 passed failed=[]
```

M2, `/tmp/mado-r20-MutVcsTip-wwm_nzvv/M2-sub-arg-color/mutated-r19-vcs.stdout:18-19`:

```text
SELFTEST_SCRIPT_SHA256: 4df835286aab3eff5029aaffbdc8cb5d9180ed3574c9662e353018c02ff3b553
SELFTEST_SUMMARY: 17/17 passed failed=[]
```

M3, `/tmp/mado-r20-MutVcsTip-wwm_nzvv/M3-git-write-commit/mutated-hardening.stdout:5,34-35`:

```text
CASE multiline-quoted-commit-vcs FAIL want=(1, [('vcs_write', 'git:commit', 1, '')]) got=(0, [])
SELFTEST_SCRIPT_SHA256: 58b7cfaf54048f3855b2163307825f708c2f7aee74c63ec48a3972f66a5bf97c
SELFTEST_SUMMARY: 32/33 passed failed=['multiline-quoted-commit-vcs']
```

M3's `mutated-r19-vcs.stdout:19`:

```text
SELFTEST_SUMMARY: 9/17 passed failed=['git-writes', 'git-arg-opts', 'eval-forms', 'eval-literal-argv-commit', 'cd-and-compound', 'git-multiline-quoted-supersedes-hardening-clean', 'permit-vcs-write', 'permit-unrelated-class-does-not-cover-vcs']
```

M4, `/tmp/mado-r20-MutVcsTip-wwm_nzvv/M4-ignore-copy-after-separator/mutated-r19-vcs.stdout:14,18-19`:

```text
CASE jj-dashdash-paths FAIL want=(1, [('vcs_write', 'jj:diff', 2, '')]) got=(0, [])
SELFTEST_SCRIPT_SHA256: 412256ba7de72441e8c8553bed47fcb2d8feeb0e15eba16fa076f2d79e3c4293
SELFTEST_SUMMARY: 16/17 passed failed=['jj-dashdash-paths']
```

## Survivor-derived H/W proposals

These are **additional regression-control proposals**, not a changed contract and not newly demonstrated C1 repair wins: both already pass at e629f73. Only scratch JSONL files were created; no canonical suite was edited. Each was scanned with pristine, corresponding mutant, and restored tool bytes. Existing tool rows lack `evidence`; the comparison normalized absence to `observed`, as the round-20 contract requires.

### H-MutVcsTip-version-help — catch M1's false positive

Fixture `/tmp/mado-r20-MutVcsTip-wwm_nzvv/H-MutVcsTip-version-help.jsonl:1`, SHA-256 `48b28b7106f0b858d85fdfcb4bc976eb5bd39be89fec1f8d8311e1640a4341f7`:

```json
{"type":"message","id":"m","timestamp":"2026-10-20T00:00:00.000Z","message":{"role":"assistant","content":[{"type":"toolCall","id":"mutvcstip-h","name":"bash","arguments":{"command":"jj version --help"}}]}}
```

Expected: **exit 0, clean, `findings=[]`** (help/non-write control). Actual scanner output:

| Bytes | Exit | Label | Normalized findings |
|---|---:|---|---|
| Pristine | 0 | `MADO_TRIPWIRE: clean` | `[]` |
| M1 | 1 | `MADO_TRIPWIRE: findings` | `[{"class":"vcs_write","rule":"jj:version","line":1,"evidence":"observed"}]` |
| Restored | 0 | `MADO_TRIPWIRE: clean` | `[]` |

Exact mutated command:

```text
/usr/bin/python -I /tmp/mado-r20-MutVcsTip-wwm_nzvv/M1-no-snapshot-version/mado-tripwire.py --scan /tmp/mado-r20-MutVcsTip-wwm_nzvv/H-MutVcsTip-version-help.jsonl
cwd=/tmp/mado-r20-MutVcsTip-wwm_nzvv
```

Gap: the existing `jj-ignore-working-copy-clean.jsonl:6-7` covers `jj help` and `jj --version`, not the `version` verb. `jj --version` exits classification through `first_verb(...) is None`; it cannot detect removal of `"version"` from `JJ_NO_SNAPSHOT`. This proposal exercises that missing membership branch while retaining an explicit help flag.

### W-MutVcsTip-nested-color — catch M2's nested-write miss

Fixture `/tmp/mado-r20-MutVcsTip-wwm_nzvv/W-MutVcsTip-nested-color.jsonl:1`, SHA-256 `4899840c3b8471896f17781994dbee06cba444f0b73c767bdfba806e43ebd385`:

```json
{"type":"message","id":"m","timestamp":"2026-10-20T00:00:00.000Z","message":{"role":"assistant","content":[{"type":"toolCall","id":"mutvcstip-w","name":"eval","arguments":{"language":"py","code":"import subprocess\ndef invoke(argv):\n    return subprocess.run(argv)\ninvoke(['jj', '--ignore-working-copy', 'bookmark', '--color', 'never', 'set', 'topic', '-r', '@-'])"}}]}}
```

Expected: **exit 1, findings, `vcs_write / jj:bookmark / line 1 / observed`**. The helper body is visible and forwards literal argv to a spawn. Actual scanner output:

| Bytes | Exit | Label | Normalized findings |
|---|---:|---|---|
| Pristine | 1 | `MADO_TRIPWIRE: findings` | `[{"class":"vcs_write","rule":"jj:bookmark","line":1,"evidence":"observed"}]` |
| M2 | 0 | `MADO_TRIPWIRE: clean` | `[]` |
| Restored | 1 | `MADO_TRIPWIRE: findings` | `[{"class":"vcs_write","rule":"jj:bookmark","line":1,"evidence":"observed"}]` |

Exact mutated command:

```text
/usr/bin/python -I /tmp/mado-r20-MutVcsTip-wwm_nzvv/M2-sub-arg-color/mado-tripwire.py --scan /tmp/mado-r20-MutVcsTip-wwm_nzvv/W-MutVcsTip-nested-color.jsonl
cwd=/tmp/mado-r20-MutVcsTip-wwm_nzvv
```

Gap: after dropping the option from `JJ_SUB_ARG_OPTS`, `sub_verb` skips the flag token but mistakes its value `never` for the nested verb instead of reaching `set`. The explicit `--ignore-working-copy` then suppresses the fallback snapshot row, so the real nested-write rule disappears entirely. The existing nested-write cases place their subverb before such an option/value, and the existing mutation-with-ignore cases contain no intervening option/value.

All six supplementary scans completed with empty stderr. Per-phase complete outputs are preserved as `/tmp/mado-r20-MutVcsTip-wwm_nzvv/H-MutVcsTip-version-help-{pristine,mutated,restored}.json` and `/tmp/mado-r20-MutVcsTip-wwm_nzvv/W-MutVcsTip-nested-color-{pristine,mutated,restored}.json`; the results bundle also embeds them. Supplementary success does **not** retroactively change M1/M2's survivor verdict on the unchanged 247-case detector.

## Restoration evidence

All four scratch copies were restored before replaying the detector. Byte comparison against the pinned original returned `true` for each, before restored replay and after it. All copied regular fixture hashes and symlink targets were unchanged after the experiment.

Common pristine **and restored** SHA-256:

`367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`

| Mutant | Mutated SHA-256 | Restored exact bytes | Restored detector |
|---|---|---|---|
| M1 | `84417830954f752fb00e34f5da7f3a2239e5310d58530691812a3ccf55454b3c` | true | 11/11 suites; 247/247 cases |
| M2 | `4df835286aab3eff5029aaffbdc8cb5d9180ed3574c9662e353018c02ff3b553` | true | 11/11 suites; 247/247 cases |
| M3 | `58b7cfaf54048f3855b2163307825f708c2f7aee74c63ec48a3972f66a5bf97c` | true | 11/11 suites; 247/247 cases |
| M4 | `412256ba7de72441e8c8553bed47fcb2d8feeb0e15eba16fa076f2d79e3c4293` | true | 11/11 suites; 247/247 cases |

Raw `pristine-*.stdout`, `mutated-*.stdout`, and `restored-*.stdout` files, plus phase JSON records, remain in each isolated directory. The scratch evidence is not a committed lane artifact; this report embeds the relevant observed outputs and full hashes so the result does not depend only on temporary pointers.

## Limits

- This is a four-mutant bounded probe, not exhaustive classifier validation, a no-harm corpus sweep, or a round-admission decision. No integration, shipping, or contract change was performed.
- No live gate, host package command, service/compositor/input probe, real `jj`, or fixture payload was executed. Read-only Git supplied source bytes; only the copied Python scanner/detector ran.
- No upstream source was fetched. [UNK] The proposed argv shapes' upstream Jujutsu parsing was not independently source-validated or executed here; classifier behavior and the stated round-20 help/non-write and visible-wrapper expectations were the exercised boundaries. These are case proposals, not new sourced semantic admissions.
- The existing selftest compares findings without an evidence marker; its pass count does not prove the new evidence schema. Supplementary tables explicitly show the absent-marker-to-`observed` normalization.
- Formal `cases.json` registration, comparison at 9c54c56/1f7f995, the new precision counter, recall/corpus guards, and later repaired tool revisions were not run or modified by this seat. The two proposed controls are not red-before precision wins.

## Installs

none

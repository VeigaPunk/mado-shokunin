# MutCheckReceipt — round 24, wave 2

VERDICT: partial

Three checker mutants were killed; the delete-before-run receipt mutant survived. The recorded red/green behavior reproduces, but the checker does not enforce the deletion condition in `corpus/QUALITY.md:319` (criterion 34). Its own stated contract is only R1 (digest) and R2 (absolute paths), so this is a coverage gap against the broader criterion, not a newly invented checker contract.

## Scope and detector

- Attacked `.ufo/waves/round-24/quality/check-receipt-provenance.py`; re-opened its complete source, the registered red/green artifacts, registration, and criterion 34.
- Axes: mutation sensitivity, real-receipt specificity, exact restoration, host safety.
- Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Scratch: `/fast/scratch/hyaku/mado-r24/w2/MutCheckReceipt`. No subagents, git/jj commands, host configuration changes, installs, or updates.
- Receipt scripts were only parsed as text, never executed. In particular, clone/commit/delete commands appearing inside receipts were not run.
- Initial original-checker replays used `timeout --kill-after=5 60 prlimit --as=536870912 --cpu=30 python3 -I CHECKER ARG`.
- The unchanged bounded detector used `timeout --kill-after=2 20 prlimit --as=536870912 --cpu=10 python3 -I SCRATCH_CHECKER ARG` for each of four cases: `--selftest`, original red, original green, and `working-green.sh`. Expected results were respectively exit 0/selftest pass with 8 cases, exit 1/fail with 5 reasons, exit 0/pass with 0 reasons, exit 0/pass with 0 reasons. It checked exit status, final stdout line, and empty stderr.
- Each process had a separate session/process group and a 25-second parent deadline, with kill-group handling on timeout. No timeout occurred; every child exited. `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` were removed from the subprocess environment.
- The same detector ran on pristine, mutated, and restored bytes for every probe. A restored run also served as the next probe's pristine run. All pristine/restored runs passed; none of the kills depends on a failing baseline.

## Original red/green replay

| Artifact | Actual result | Digest |
|---|---|---|
| Checker | Original and restored bytes identical | `sha256:5b463510893fea56276fb377a23dcc90935f8b4baef0e307f6b6e35ea0e585f9` |
| `quality/red/r23-l1-attacks-first.sh` | exit 1; `verdict=fail reasons=5` | `sha256:599a92da90695f0e4faa9fb764940af751d9b845206a31279b0a9cc00bb7425d` |
| `quality/fixtures/l1-attacks-green.sh` | exit 0; `verdict=pass reasons=0` | `sha256:076a41ed6d9bb926c5dd3a3a53349a5096191b1158ee4614f66497aa691012ef` |

These match `quality/m23-5-red-green.txt`, including its full recorded artifact hashes. The selftest also reproduced exit 0 and `selftest=pass cases=8 mismatches=0`.

Actual pristine selftest stdout:
```text
selftest case=bare-digest expected=pass got=pass ok
selftest case=green expected=pass got=pass ok
selftest case=no-digest expected=fail got=fail ok
selftest case=relative-result expected=fail got=fail ok
selftest case=relative-var expected=fail got=fail ok
selftest case=tilde-result expected=fail got=fail ok
selftest case=truncated-digest expected=fail got=fail ok
selftest case=unbound-digest expected=fail got=fail ok
selftest=pass cases=8 mismatches=0
```

Actual pristine red stdout (the original-checker replay and scratch-checker replay agreed):
```text
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/quality/red/r23-l1-attacks-first.sh:-: R1 no `sha256:`<64hex> or full 64-hex sha256 naming the measured tool; `sha256sum` at line(s) 9 computes a digest at run time but the receipt never states it
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/quality/red/r23-l1-attacks-first.sh:18: R2 data position: relative path 'probes' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/quality/red/r23-l1-attacks-first.sh:19: R2 data position: relative path 'probes2' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/quality/red/r23-l1-attacks-first.sh:20: R2 data position: relative path '../fixtures' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/quality/red/r23-l1-attacks-first.sh:31: R2 data position: relative path '$c.json': variable $c is not pinned to an absolute value
verdict=fail reasons=5
```

Actual original green stdout:
```text
PASS /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/quality/fixtures/l1-attacks-green.sh
verdict=pass reasons=0
```

## Four assigned mutation probes

| Probe | Smallest change | Expected detector | Actual mutated output | Verdict |
|---|---|---|---|---|
| M1 accept relative paths | Checker line 170: terminal `judge_path` return `False` → `True` | `relative-result` and `relative-var` selftest cases must reject these paths | Both became `expected=fail got=pass MISMATCH`; `selftest=fail cases=8 mismatches=2`, exit 1. Red still exited 1 but reasons fell 5 → 2. | KILLED |
| M2 accept short sha | Checker line 69: labelled-digest quantifier `{64}` → `{8,64}` | `truncated-digest` selftest must reject the eight-hex digest plus ellipsis | `expected=fail got=pass MISMATCH`; `selftest=fail cases=8 mismatches=1`, exit 1. Red/green CLI pair unchanged. | KILLED |
| M3 skip delete-before-run | Scratch copy of actual green fixture: delete only original line 16, the `rm -f` of all six result files | Criterion 34 would require the gate to reject the now-uncleared result files | Scratch receipt still printed `PASS` and `verdict=pass reasons=0`, exit 0. Existing selftest and both original fixtures unchanged. | SURVIVED (receipt mutant) |
| M4 invert exit | Checker line 315: `return 0 if total == 0 else 1` → `return 1 if total == 0 else 0` | Red/green CLI exit assertions | Red printed fail/5 but exited 0; both green receipts printed pass/0 but exited 1. Selftest still passed. | KILLED |

**M3 is explicitly an input/receipt mutation.** There is no delete-before-run validation branch in the checker to disable: `check_receipt` checks only R1/R2, `rm` is staging-only, and the selftest matrix has no missing-delete case. Removing the real fixture's cleanup line directly tests the requested omission without pretending to mutate nonexistent checker logic. The fixture comment claiming cleanup was left untouched, as would happen with an accidental omitted command. The surviving acceptance is a coverage finding; no contract or production code was changed.

The red/green pair alone is insufficient for M1/M2 if a detector checks only pass/fail exits: their red receipts remain rejected. M1 is killed by the two selftest cases (and the exact red reason count); M2 by the truncated-digest selftest. Conversely, selftest alone does not kill M4 because it calls `check_receipt` rather than the CLI `run` exit branch.

### Before / mutant / restored hashes

| Probe / bytes mutated | Before | Mutant | Restored |
|---|---|---|---|
| M1 / checker | `sha256:5b463510893fea56276fb377a23dcc90935f8b4baef0e307f6b6e35ea0e585f9` | `sha256:dd35d7dd753001dc3e38f90c5b97866c872668f68c89b7481cfca8bd031e2895` | `sha256:5b463510893fea56276fb377a23dcc90935f8b4baef0e307f6b6e35ea0e585f9` |
| M2 / checker | `sha256:5b463510893fea56276fb377a23dcc90935f8b4baef0e307f6b6e35ea0e585f9` | `sha256:d92696a0921dcafac4b809c0c6f560e98f953f01aa05fff8b7e8593705aebbf7` | `sha256:5b463510893fea56276fb377a23dcc90935f8b4baef0e307f6b6e35ea0e585f9` |
| M3 / green | `sha256:076a41ed6d9bb926c5dd3a3a53349a5096191b1158ee4614f66497aa691012ef` | `sha256:4188a13896fb2c91e5ed76df810f590df96f6086448ae0a1cc7ea56a6ae0768b` | `sha256:076a41ed6d9bb926c5dd3a3a53349a5096191b1158ee4614f66497aa691012ef` |
| M4 / checker | `sha256:5b463510893fea56276fb377a23dcc90935f8b4baef0e307f6b6e35ea0e585f9` | `sha256:c902b8c33c03417b1a23714cb9f608fb0b6379fb0d93fd8e2f1512de221150bc` | `sha256:5b463510893fea56276fb377a23dcc90935f8b4baef0e307f6b6e35ea0e585f9` |

### Same-detector phase outputs

Each cell below is **exit status; exact final stdout line**. All stderr was empty. “Detector pass” refers to the unchanged historical matrix, not a judgment that the M3 receipt satisfies criterion 34.

| Phase | Selftest | Original red | Original green | Scratch green | Detector pass |
|---|---|---|---|---|---|
| m1-pristine | 0; `selftest=pass cases=8 mismatches=0` | 1; `verdict=fail reasons=5` | 0; `verdict=pass reasons=0` | 0; `verdict=pass reasons=0` | yes |
| m1-mutated-accept-relative | 1; `selftest=fail cases=8 mismatches=2` | 1; `verdict=fail reasons=2` | 0; `verdict=pass reasons=0` | 0; `verdict=pass reasons=0` | NO |
| m1-restored_m2-pristine | 0; `selftest=pass cases=8 mismatches=0` | 1; `verdict=fail reasons=5` | 0; `verdict=pass reasons=0` | 0; `verdict=pass reasons=0` | yes |
| m2-mutated-accept-short-sha | 1; `selftest=fail cases=8 mismatches=1` | 1; `verdict=fail reasons=5` | 0; `verdict=pass reasons=0` | 0; `verdict=pass reasons=0` | NO |
| m2-restored_m3-pristine | 0; `selftest=pass cases=8 mismatches=0` | 1; `verdict=fail reasons=5` | 0; `verdict=pass reasons=0` | 0; `verdict=pass reasons=0` | yes |
| m3-mutated-skip-delete-before-run | 0; `selftest=pass cases=8 mismatches=0` | 1; `verdict=fail reasons=5` | 0; `verdict=pass reasons=0` | 0; `verdict=pass reasons=0` | yes |
| m3-restored_m4-pristine | 0; `selftest=pass cases=8 mismatches=0` | 1; `verdict=fail reasons=5` | 0; `verdict=pass reasons=0` | 0; `verdict=pass reasons=0` | yes |
| m4-mutated-invert-exit | 0; `selftest=pass cases=8 mismatches=0` | 0; `verdict=fail reasons=5` | 1; `verdict=pass reasons=0` | 1; `verdict=pass reasons=0` | NO |
| m4-restored | 0; `selftest=pass cases=8 mismatches=0` | 1; `verdict=fail reasons=5` | 0; `verdict=pass reasons=0` | 0; `verdict=pass reasons=0` | yes |

Actual newly mismatching selftest rows:
```text
selftest case=relative-result expected=fail got=pass MISMATCH
selftest case=relative-var expected=fail got=pass MISMATCH
selftest case=truncated-digest expected=fail got=pass MISMATCH
```

## Three real round-23 receipts

Fed the following **unmodified whole artifacts** to the original lane checker with the same 20-second/512-MiB/10-CPU-second command prefix. No receipt was executed and no excerpt was substituted. Report Markdown was not stripped before input.

| Receipt (relative to lane) | Actual result | Rule counts | Receipt digest |
|---|---|---|---|
| `.ufo/waves/round-23/w1/out/L1/l1-attacks.sh` | exit 1; `verdict=fail reasons=5` | R1=1, R2=4 | `sha256:1233f43e51f35acb6363e27ab6d50476217f031d28026a17418cbcea308f6bc3` |
| `.ufo/waves/round-23/w1/reports/ExecFullA.md` | exit 1; `verdict=fail reasons=6` | R1=1, R2=5 | `sha256:d44e5e2bc2255781360a624d2b36b7d23ecf389820811772fb5a73e25acfdd90` |
| `.ufo/waves/round-23/w2/reports/ReRepair.md` | exit 1; `verdict=fail reasons=23` | R1=0, R2=23 | `sha256:3b3744b36f5a23a23deca17f8086548bc5db956507795705b65d65b2b416c440` |

- L1 is the later committed artifact already mentioned in the original red/green receipt, not a duplicate of the historical first revision. Its different digest is recorded above. The observed five failures match the original diagnostic: no stated full tool digest and four relative data tokens.
- `ExecFullA.md:20` does state a full tool digest, but its `Candidate tool sha256` line lacks a filename/path matching `TOOL_HINT`, so R1 rejects it. At line 47 the checker also treats narrative words after `run.py` (`resolves`, `relative`, `to`, `the`, and the code expression) as data paths.
- `ReRepair.md` satisfies R1, but the checker flags the shell continuation backslash on line 19 and narrative/schema words after mentions of `measure.py` as relative paths. The actual command shown across lines 19–20 uses an absolute tool path. These 23 R2 diagnostics are therefore not evidence that 23 real measurement data paths were relative.
- This format sensitivity follows the re-opened implementation: `HARNESS` scans every text line, and `extract_paths` appends remaining tokens without the documented `path_like` restriction (`check-receipt-provenance.py:201–219`). These are observed whole-artifact results, not a claim that the historical measurements were re-run or disproved.

Actual commands and complete stdout/stderr for the three inputs:

```text
$ timeout --kill-after=2 20 prlimit --as=536870912 --cpu=10 python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/quality/check-receipt-provenance.py /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w1/out/L1/l1-attacks.sh
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w1/out/L1/l1-attacks.sh:-: R1 no `sha256:`<64hex> or full 64-hex sha256 naming the measured tool; `sha256sum` at line(s) 9 computes a digest at run time but the receipt never states it
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w1/out/L1/l1-attacks.sh:18: R2 data position: relative path 'probes' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w1/out/L1/l1-attacks.sh:19: R2 data position: relative path 'probes2' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w1/out/L1/l1-attacks.sh:20: R2 data position: relative path '../fixtures' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w1/out/L1/l1-attacks.sh:31: R2 data position: relative path '$c.json': variable $c is not pinned to an absolute value
verdict=fail reasons=5
exit=1
stderr=''
```

```text
$ timeout --kill-after=2 20 prlimit --as=536870912 --cpu=10 python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/quality/check-receipt-provenance.py /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w1/reports/ExecFullA.md
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w1/reports/ExecFullA.md:-: R1 no `sha256:`<64hex> or full 64-hex sha256 naming the measured tool; only truncated digest(s): line 19 `a28e4815...`
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w1/reports/ExecFullA.md:47: R2 data position: relative path 'resolves' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w1/reports/ExecFullA.md:47: R2 data position: relative path '`ROOT.parents[5]`' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w1/reports/ExecFullA.md:47: R2 data position: relative path 'relative' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w1/reports/ExecFullA.md:47: R2 data position: relative path 'to' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w1/reports/ExecFullA.md:47: R2 data position: relative path 'the' (resolved against the receipt's current directory)
verdict=fail reasons=6
exit=1
stderr=''
```

```text
$ timeout --kill-after=2 20 prlimit --as=536870912 --cpu=10 python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/quality/check-receipt-provenance.py /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/reports/ReRepair.md
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/reports/ReRepair.md:19: R2 data position: relative path '\\' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/reports/ReRepair.md:28: R2 data position: relative path '`:' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/reports/ReRepair.md:28: R2 data position: relative path '`schema' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/reports/ReRepair.md:28: R2 data position: relative path 'mado-r23-repair-measure-v1`' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/reports/ReRepair.md:28: R2 data position: relative path '`passed:' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/reports/ReRepair.md:28: R2 data position: relative path '12' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/reports/ReRepair.md:28: R2 data position: relative path 'total:' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/reports/ReRepair.md:28: R2 data position: relative path '12`' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/reports/ReRepair.md:28: R2 data position: relative path '**exit' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/reports/ReRepair.md:28: R2 data position: relative path '0**.' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/reports/ReRepair.md:71: R2 data position: relative path '`/`truth.py`/`expected.json`' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/reports/ReRepair.md:71: R2 data position: relative path 'sha256s' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/reports/ReRepair.md:71: R2 data position: relative path 'equal' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/reports/ReRepair.md:71: R2 data position: relative path '`git' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/reports/ReRepair.md:71: R2 data position: relative path 'show' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/reports/ReRepair.md:71: R2 data position: relative path '2f1134f3:...`' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/reports/ReRepair.md:71: R2 data position: relative path 'bytes.' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/reports/ReRepair.md:72: R2 data position: relative path 'also' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/reports/ReRepair.md:72: R2 data position: relative path 'working==committed' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/reports/ReRepair.md:72: R2 data position: relative path 'and' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/reports/ReRepair.md:72: R2 data position: relative path 'equals' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/reports/ReRepair.md:72: R2 data position: relative path 'the' (resolved against the receipt's current directory)
FAIL /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/reports/ReRepair.md:73: R2 data position: relative path '.' (resolved against the receipt's current directory)
verdict=fail reasons=23
exit=1
stderr=''
```

## Restoration and retained evidence

- Every mutant was applied only to this seat's scratch files. Restoration ran in `finally` after each mutation probe, including failed detector verdicts. The last restored suite again passed all four cases.
- Both explicit bounded `cmp -s` comparisons returned 0: scratch checker versus lane checker, and scratch green versus original green. Final `sha256sum` outputs matched the original checker/red/green hashes above and the restored hash column for both scratch files. Lane checker/red/green hashes were unchanged from the initial read.
- The sole lane write for this seat is this report. No production change, integration, or ship action was attempted. No additional mutation probes were run.

Raw local evidence (complete command arrays, stdout, stderr, exit codes, phase hashes):

| Artifact | Digest |
|---|---|
| `/fast/scratch/hyaku/mado-r24/w2/MutCheckReceipt/detector-results.json` | `sha256:e38049695e80683c643c2e7a790b1714cbbff6e78d06467647809ee8aa6e6326` |
| `/fast/scratch/hyaku/mado-r24/w2/MutCheckReceipt/real-receipts.json` | `sha256:10d4db8f6af8d3df507c305b8292d840403c9c5fdf1e007d8d7bf2e5c8ae19e9` |
| `/fast/scratch/hyaku/mado-r24/w2/MutCheckReceipt/restoration.json` | `sha256:8586d67e43e60da900b6cfd1d3154dbbecd83d0ab341f9f9788f7a9352046faf` |

These scratch artifacts are execution provenance; this report retains the results and restoration hashes without requiring them to become lane evidence files. No test/build/lint beyond the explicitly assigned bounded detector runs was performed.

# MutQ36 — successor checker mutation probe

MUTQ36: killed 6/6; survived 0; inconclusive 0; exact restoration after every mutant.

ROUND26_SUCCESSOR: FAIL, exit 1, reason=no-receipt-under-.ufo/waves/round-26/controls/.

The six assigned defects are detected by the supplied synthetic fixtures. This does **not** establish a round-26 checker PASS: the committed round-26 control receipts are `.txt`, whereas the successor only accepts `.md`. The separate read-only timestamp comparison places the controls commit 17.175 seconds before the w2 registry's `createdAt`.

## Scope and isolation

Seat: `MadoR26.MutQ36`. Axes: valid behavioral baselines, defect sensitivity, exact-byte restoration, and lane/host isolation. Read the godspeed skill. No subagents, tool installs/updates, compositor commands, counter runs, checker repairs, or contract changes.

Only this report was written in the lane. All synthetic git writes and checker edits were under:

`/fast/scratch/hyaku/mado-r26/MutQ36/`

The isolated working copy `check-control-receipts.py` was restored between the six independent mutations; mutations were never cumulative. The lane checker and fixture sources remained read-only. The new scratch driver reuses the existing `q36-fixtures/run_fixtures.py` fixture builder and expectation checks, but does not invoke its eight-mutant main routine: only the six assigned mutations were applied, using surgical edits.

`df -h /fast` before writes reported 146G available. Every executed shell command had an outer timeout; detector invocations used a 4,000,000,000-byte address-space cap. Each checker/metadata subprocess had a 20-second deadline and its own process group, killed/reaped in the driver's cleanup. Fixture setup git commands were synchronous and bounded by the existing builder. No detector timed out. No process was left running.

`WAYLAND_DISPLAY`, `HYPRLAND_INSTANCE_SIGNATURE`, `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` were unset in shell invocations. Fixture/checker child environments were the existing runner's sanitized environment: scratch HOME, `GIT_CONFIG_NOSYSTEM=1`, `GIT_OPTIONAL_LOCKS=0`, no display variables or git-location overrides. Python ran with `-I -B`; receipt files were bounded to 4 MiB.

## Expected detector and actual results

The existing fixture expectations check exits, stdout substrings, and the designated receipt commit where applicable (`fixtures.py:59-224`; `run_fixtures.py:132-144`). All ten pristine fixture baselines satisfied those expectations. An expected checker FAIL/exit 1 is a valid negative fixture, not a failed baseline.

A kill requires a changed behavioral exit on a valid baseline, not merely changed diagnostics or a syntax error. Every mutant also preserved `green` at PASS/exit 0. All 130 fixture checker invocations had empty stderr and no timeout. Every restored run reproduced the pristine exits and complete stdout byte-for-byte.

| Mutant | Smallest behavior-bearing change in successor | Designated detector | Pristine → mutant → restored exit | Verdict |
|---|---|---|---|---|
| M1-nonstrict | L140: `<` → `<=` | `equal-time`: receipt second equals `createdAt` | 1 → 0 → 1 | killed |
| M2-ignore-shapes | L149: `ok = order_ok and not missing` → `ok = order_ok` | `missing-shape`: order valid, NoReader absent | 1 → 0 → 1 | killed |
| M3-newest-receipt | L111: remove `"--reverse",` from git log arguments | `later-receipt`: oldest addition before data, newest after | 0 → 1 → 0 | killed |
| M4-any-md | L100: marker rejection condition → `if False:` | `nonreceipt-md`: only markdown has no control marker | 1 → 0 → 1 | killed |
| M5-updatedAt | L132: `["createdAt"]` → `["updatedAt"]` | `updated-at`: created time after receipt, updated time before | 0 → 1 → 0 | killed |
| M6-ignore-counter-sha | L65: `if not counter_shas:` → `if True:` | `sha-late`: early receipt names wrong counter, selected counter lands late | 1 → 0 → 1 | killed |

Mutation definitions are the first six entries of the supplied `fixtures.py:228-276`. The artificial `updated-at` field ordering is intentionally the fixture's distinguishing input, not an assertion about a real registry.

Full actual exit matrix:

| Fixture | Pristine | M1 | M2 | M3 | M4 | M5 | M6 | Every restoration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| green | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| equal-time | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 |
| missing-shape | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 |
| later-receipt | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| nonreceipt-md | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 |
| updated-at | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| sha-green | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| sha-not-first-line | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1 |
| sha-prefix | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1 |
| sha-late | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1 |

Thus M6 is also killed by `sha-not-first-line` and `sha-prefix`. No additional mutants were applied.

Actual designated-mutant stdout excerpts, with exits:

```text
M1 / equal-time:
order=ok gap_s=0 shapes_missing=-
CONTROL_RECEIPTS verdict=PASS
exit=0

M2 / missing-shape:
order=ok gap_s=240 shapes_missing=NoReader
CONTROL_RECEIPTS verdict=PASS
exit=0

M3 / later-receipt:
receipt_commit=a82360056107 committed=2026-10-22T00:09:00+00:00 data_registry=.ufo/waves/round-99/w1/reports/swarm-registry.json createdAt=2026-10-22T00:05:00Z
order=LATE gap_s=-240 shapes_missing=-
CONTROL_RECEIPTS verdict=FAIL
exit=1

M4 / nonreceipt-md:
order=ok gap_s=240 shapes_missing=-
CONTROL_RECEIPTS verdict=PASS
exit=0

M5 / updated-at:
receipt_commit=ab5467127323 committed=2026-10-22T00:01:00+00:00 data_registry=.ufo/waves/round-99/w1/reports/swarm-registry.json createdAt=2026-10-22T00:00:30Z
order=LATE gap_s=-30 shapes_missing=-
CONTROL_RECEIPTS verdict=FAIL
exit=1

M6 / sha-late:
receipt_commit=8f22e10936f4 committed=2026-10-22T00:01:00+00:00 data_registry=.ufo/waves/round-99/w1/reports/swarm-registry.json createdAt=2026-10-22T00:05:00Z
order=ok gap_s=240 shapes_missing=-
CONTROL_RECEIPTS verdict=PASS
exit=0
```

For M3, pristine/restored selected `588f100934a0`, committed at 00:01, and passed. For M6, pristine/restored excluded one wrong-counter receipt, selected `092e90afdc7c`, committed at 00:09, and failed. Complete outputs, exact commands, stderr, timeout flags, and fixture expectations are in the JSON receipts below.

## Exact commands and receipt locations

Working directory for shell invocations: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Every fixture-driver invocation used this exact prefix:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE \
  -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  timeout --kill-after=2s 300s prlimit --as=4000000000 --nofile=1024 -- \
  python3 -I -B /fast/scratch/hyaku/mado-r26/MutQ36/probe.py
```

The following argument suffixes were executed in this order, with the corresponding one-line mutation/restoration edit between calls. All 13 driver invocations exited 0 with `problems=0`:

```text
--state pristine --prepare
--state mutated --mutant M1-nonstrict
--state restored --mutant M1-nonstrict
--state mutated --mutant M2-ignore-shapes
--state restored --mutant M2-ignore-shapes
--state mutated --mutant M3-newest-receipt
--state restored --mutant M3-newest-receipt
--state mutated --mutant M4-any-md
--state restored --mutant M4-any-md
--state mutated --mutant M5-updatedAt
--state restored --mutant M5-updatedAt
--state mutated --mutant M6-ignore-counter-sha
--state restored --mutant M6-ignore-counter-sha
```

Each invocation ran all ten identical checker commands on the same fixture repositories. Command form (every exact argv is stored in the receipts):

```text
/usr/bin/python3 -I -B /fast/scratch/hyaku/mado-r26/MutQ36/check-control-receipts.py --repo /fast/scratch/hyaku/mado-r26/MutQ36/repos/FIXTURE --round 99 --data-registry .ufo/waves/round-99/w1/reports/swarm-registry.json --tip HEAD
```

The four `sha-*` fixtures additionally used `--counter-sha` with `3f` repeated 32 times, exactly as declared in the supplied fixtures.

Receipt root: `/fast/scratch/hyaku/mado-r26/MutQ36/`.

- `baseline.json`: all ten valid pristine baselines.
- `M1-nonstrict-{mutated,restored}.json`
- `M2-ignore-shapes-{mutated,restored}.json`
- `M3-newest-receipt-{mutated,restored}.json`
- `M4-any-md-{mutated,restored}.json`
- `M5-updatedAt-{mutated,restored}.json`
- `M6-ignore-counter-sha-{mutated,restored}.json`
- `fixtures.json`: synthetic repo paths and exact commit identities.
- `round26-readonly.json`: unfiltered/filtered successor invocations and independent read-only chronology evidence.
- `probe.py`, `audit-round26.py`: retained bounded drivers.

## Hashes and exact restoration

The pristine lane checker, initial scratch copy, and scratch bytes after **every** restoration were exactly 6,982 bytes, SHA-256:

`351127bd0d735665f899129fa3ad408b8d23c85d9f71969b44e3b63d86b6d3b4`

Each mutation began from those bytes. Its before/after detector hashes both equaled the corresponding mutant hash below. Each restoration receipt verified exact byte equality to the original lane bytes, repeated all ten detectors, and matched the initial baseline's full stdout/stderr/exits. The lane before/after hashes stayed pristine throughout.

| Mutant | Mutated checker SHA-256 |
|---|---|
| M1 | `12d8327b32163f1294068e67cb978b4af4497727669826e1d5b7cf6f265845fc` |
| M2 | `ca054f584b86c2da2f0a20994622a002c80e17fcfef5257c43364667f951ff94` |
| M3 | `4147f1f770df9bbb8d9e8b7c159457b0190570cb3433a5e0bb9f678221704559` |
| M4 | `3b7656ff6976ef11da56d9d3b918402ad77f711f7c10d747588bc3136667ea6a` |
| M5 | `f48adb956b05d580477caeef2b30369d83a61fac4cd7d8df340101c30a133bac` |
| M6 | `2865edf297e892a03c6d32847f0f8e4997cf1e8bca9997561f95456042f933dc` |

Final scratch state is restored, not mutated. No disposable-copy exception was used.

## Round-26 read-only successor verdict

The read-only audit ran alongside initial fixture setup, then the literal unfiltered successor was invoked again after the final restoration as requested. Audit command (wrapper exit 0 records the subject's failures, not a checker PASS):

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE \
  -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  timeout --kill-after=2s 120s prlimit --as=4000000000 --nofile=1024 -- \
  python3 -I -B /fast/scratch/hyaku/mado-r26/MutQ36/audit-round26.py
```

Final literal successor command:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE \
  -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 \
  timeout --kill-after=2s 120s prlimit --as=4000000000 --nofile=1024 -- \
  python3 -I -B \
  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/quality/check-control-receipts.py \
  --repo /home/vgpnk/Projects/shokunin/mado-shokunin --round 26 \
  --data-registry .ufo/waves/round-26/w2/reports/swarm-registry.json \
  --tip 1b0b91e9889cbf984b052f5de564db78330a72aa
```

Actual stdout, both unfiltered invocations; final command exited 1:

```text
tip=1b0b91e9889cbf984b052f5de564db78330a72aa round=26 receipts=0 counter_sha=- excluded_by_counter_sha=0
CONTROL_RECEIPTS verdict=FAIL reason=no-receipt-under-.ufo/waves/round-26/controls/
```

The audit additionally ran the same successor command with both frozen counter filters:

```text
--counter-sha 4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428
--counter-sha b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8
```

Actual filtered stdout, exit 1:

```text
tip=1b0b91e9889cbf984b052f5de564db78330a72aa round=26 receipts=0 counter_sha=4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428,b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8 excluded_by_counter_sha=0
CONTROL_RECEIPTS verdict=FAIL reason=no-receipt-under-.ufo/waves/round-26/controls/
```

The read-only `git ls-tree` output contains 17 `.py` files, 29 `.txt` files, and **zero `.md` files** under the committed round-26 controls directory, including `controls/v2/`. The successor skips every non-`.md` path at L94-95 and returns at L108-110 before examining the registry. Therefore its actual FAIL does not diagnose lateness or missing shortcut shapes, and the counter filter's zero exclusions do not establish that receipt headers matched.

Both candidate registry paths also exist only on disk, not in this frozen tip. Exact read-only `git show TIP:PATH` checks returned exit 128 for each:

```text
fatal: path '.ufo/waves/round-26/w2/reports/swarm-registry.json' exists on disk, but not in '1b0b91e9889cbf984b052f5de564db78330a72aa'
fatal: path '.ufo/waves/round-26/w2-run.json' exists on disk, but not in '1b0b91e9889cbf984b052f5de564db78330a72aa'
```

The checker reads a registry with `git show TIP:PATH` at L127, not from the working tree. These are separately observed input-compatibility limitations; neither was bypassed with a renamed receipt, synthetic registry commit, or checker edit.

### Separate chronology, not a replacement checker verdict

Read-only git metadata for the specified controls commit:

```text
1b0b91e9889cbf984b052f5de564db78330a72aa
1792746982
2026-10-23T06:16:22-03:00
```

Working-tree registry snapshot: `.ufo/waves/round-26/w2/reports/swarm-registry.json`, 5,203 bytes, SHA-256 `fefa1296801647355b4b9d4fb9b709f61c5ed2d24dbd185b074d6b8410744fde`. Only `createdAt`, not `updatedAt`, supplied the comparison:

```text
SEPARATE_CHRONOLOGY committed=2026-10-23T09:16:22+00:00 createdAt=2026-10-23T09:16:39.175Z gap_s=17.175 strict_order=True
```

Thus the specified controls commit predates the observed w2 creation timestamp. That manual read-only comparison is **not** a successor PASS or evidence that the successor evaluated round-26 ordering. Its actual verdict remains FAIL/exit 1.

## Final scope

Exercised: 130 fixture checker invocations (10 initial, 60 mutated, 60 restored), three literal lane-checker invocations, and the read-only git metadata/blob queries recorded above. No broader build, lint, regression, oracle, or counter verification was run. No integration or claim judgment was made.

MUTQ36: killed 6/6; survived 0; inconclusive 0; restoration exact.

ROUND26_SUCCESSOR: FAIL exit=1; separate controls-before-w2 chronology gap=17.175s.

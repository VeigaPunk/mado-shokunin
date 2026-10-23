# QUALITY 36 checker mutation probe

MUTQ36: killed 1/6; survivors: M1 nonstrict, M2 ignore-shapes, M3 newest-receipt, M4 any-md, M5 updatedAt

The count above uses the requested round-24 red case plus a clearly separate, committed round-25 registry snapshot fixture. The literal round-25 command at `459dd17f` is UNEVALUABLE (exit 2), not green: the checker reads the registry from the commit, not the working tree. That case is inconclusive for every mutant and contributes no kills. With only the evaluable literal requested case (round 24), all six mutants survive.

## Scope and isolation

Axes: valid behavioral baselines, mutation sensitivity, exact-byte restoration, and isolation from the lane and other seats. Read the godspeed skill, the Attempt 3 registration, the checker, the supplied red receipt, and the available a3w2 registry. No subagents, package installs/updates, compositor commands, or counter runs. No checker repair or contract change.

All mutations were single-line, one-defect-at-a-time changes in:

`/fast/scratch/hyaku/mado-r25a3/mutq36/repo/.ufo/waves/round-25/quality/check-control-receipts.py`

The lane checker was read-only. The only lane file written by this seat is this report. Git writes occurred only in the isolated clone. `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` were unset for clone/setup/detector git operations; `GIT_OPTIONAL_LOCKS=0` was set.

Pristine checker SHA-256 (lane and scratch before mutation, and scratch after every restoration):

`90542cad47d9004eaad83508ca2a3bfa81b15b4a932642d58942d23e58471f72`

Supplied red receipt SHA-256:

`425429e3f4bda526a1e1c4b4f32404f66476a671db488459395fdbb6906ad882`

Lane registry snapshot SHA-256, identical in the committed scratch fixture:

`fc5267bf92a4490001baec622136bc3930d38984d38eb4a08679395c43074d2c`

## Registry fixture and commands

The registry existed in the lane working tree. Its `createdAt` and `updatedAt` were both `2026-10-23T07:31:20.779Z`. Merely placing its bytes in the clone does not make `git show 459dd17f:PATH` work. I therefore kept the exact pinned command as an explicitly unavailable case and also committed only those registry bytes atop `459dd17f` in the scratch clone. No control receipt or registry field was changed for this fixture.

Scratch-only fixture commit: `cf277ad8fd7991a5eb6c0873ef940e199b370398`, parent `459dd17f8fd60df85b25f15e69376a9765e267d3`. The snapshot-green invocation uses scratch `HEAD`, not the original pin. It is not evidence that the registry was present in the original pinned commit.

Setup commands (each executed under `ulimit -v 786432`):

```sh
timeout 90s env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 git clone --quiet --no-checkout --no-hardlinks --no-tags /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r25a3/mutq36/repo
timeout 30s env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 git -C /fast/scratch/hyaku/mado-r25a3/mutq36/repo -c advice.detachedHead=false checkout --quiet --detach 459dd17f
timeout 30s env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 git -C /fast/scratch/hyaku/mado-r25a3/mutq36/repo -c index.threads=1 -c core.preloadIndex=false add -- .ufo/waves/round-25/a3w2/reports/swarm-registry.json
timeout 30s env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 GIT_AUTHOR_DATE=2026-10-23T07:31:21Z GIT_COMMITTER_DATE=2026-10-23T07:31:21Z git -C /fast/scratch/hyaku/mado-r25a3/mutq36/repo -c index.threads=1 -c core.preloadIndex=false -c pack.threads=1 -c user.name=MutQ36Checker -c user.email=mutq36@example.invalid -c core.hooksPath=/dev/null -c commit.gpgsign=false commit --quiet -m 'Mutation fixture: snapshot existing a3w2 data registry' -- .ufo/waves/round-25/a3w2/reports/swarm-registry.json
```

An initial `git add` without the single-thread settings exited 128 with `fatal: unable to create threaded lstat: Resource temporarily unavailable`; the chained commit/detector did not run. The bounded retry above succeeded. Before committing, a manually copied snapshot was found to have swapped two member-role values; those scratch-only copy mistakes were corrected and its hash matched the lane registry before any detector run.

The retained driver is `/fast/scratch/hyaku/mado-r25a3/mutq36/probe.py`. Each invocation was:

```sh
timeout 80s python3 -I -B /fast/scratch/hyaku/mado-r25a3/mutq36/probe.py LABEL
```

Actual LABEL sequence:

```text
baseline
m1-nonstrict
m1-restored
m2-ignore-shapes
m2-restored
m3-newest-receipt
m3-restored
m4-any-markdown
m4-restored
m5-updated-at
m5-restored
m6-reverse-order
m6-restored
```

The driver imposed 512 MiB address space, 30 seconds CPU and 2 MiB output-file limits. Each detector had a 20-second timeout, 2-second kill grace, and a separate process group killed/reaped by the driver. No invocation timed out. All detector stderr streams were empty. The same three commands ran on pristine, each mutant, and every restored checker:

```sh
timeout --signal=TERM --kill-after=2s 20s python3 -I -B /fast/scratch/hyaku/mado-r25a3/mutq36/repo/.ufo/waves/round-25/quality/check-control-receipts.py --repo /fast/scratch/hyaku/mado-r25a3/mutq36/repo --round 24 --data-registry .ufo/waves/round-24/w1/reports/swarm-registry.json --tip 41cc04c8 --any-md
timeout --signal=TERM --kill-after=2s 20s python3 -I -B /fast/scratch/hyaku/mado-r25a3/mutq36/repo/.ufo/waves/round-25/quality/check-control-receipts.py --repo /fast/scratch/hyaku/mado-r25a3/mutq36/repo --round 25 --data-registry .ufo/waves/round-25/a3w2/reports/swarm-registry.json --tip 459dd17f
timeout --signal=TERM --kill-after=2s 20s python3 -I -B /fast/scratch/hyaku/mado-r25a3/mutq36/repo/.ufo/waves/round-25/quality/check-control-receipts.py --repo /fast/scratch/hyaku/mado-r25a3/mutq36/repo --round 25 --data-registry .ufo/waves/round-25/a3w2/reports/swarm-registry.json --tip HEAD
```

## Expected detector and actual baselines

A mutant is killed only when it changes the expected behavioral result: round-24 exit 1 / FAIL, or committed snapshot-green exit 0 / PASS. Changed diagnostic text alone is not counted as a kill. The unavailable pinned case is excluded, rather than counting its baseline failure as a kill.

Pristine round 24 reproduced the supplied red receipt (exit 1):

```text
tip=41cc04c8d593837a0d5078bffaacdaa163d12897 round=24 receipts=12
receipt_commit=464a02452bbe committed=2026-10-23T03:53:36+00:00 data_registry=.ufo/waves/round-24/w1/reports/swarm-registry.json createdAt=2026-10-23T03:35:33.205Z
order=LATE gap_s=-1083 shapes_missing=EmptyArray|AllFalse,Echo,LabelKeyed
CONTROL_RECEIPTS verdict=FAIL
```

Pristine literal round 25 at the requested pin (exit 2, inconclusive):

```text
tip=459dd17f8fd60df85b25f15e69376a9765e267d3 round=25 receipts=19
UNEVALUABLE data registry .ufo/waves/round-25/a3w2/reports/swarm-registry.json absent at tip
```

Pristine committed snapshot-green (exit 0):

```text
tip=cf277ad8fd7991a5eb6c0873ef940e199b370398 round=25 receipts=19
receipt_commit=7228299d94b1 committed=2026-10-23T05:23:06+00:00 data_registry=.ufo/waves/round-25/a3w2/reports/swarm-registry.json createdAt=2026-10-23T07:31:20.779Z
order=ok gap_s=7695 shapes_missing=-
CONTROL_RECEIPTS verdict=PASS
```

## Mutants and actual results

Every row is a separate one-line mutation of pristine bytes, not a cumulative edit. Exit columns are actual detector exits.

| Mutant | Exact behavior-bearing change | Round 24 | Pinned round 25 | Snapshot-green | Verdict on evaluable pair |
| --- | --- | ---: | ---: | ---: | --- |
| M1 nonstrict | L101: `order_ok = first[1] <= cts` | 1 | 2 | 0 | survived |
| M2 ignore-shapes | L109: `ok = order_ok` | 1 | 2 | 0 | survived |
| M3 newest-receipt | L74: remove `"--reverse",` from git log arguments | 1 | 2 | 0 | survived |
| M4 any-md | L68: replace the receipt-marker predicate with `if True:` | 1 | 2 | 0 | survived |
| M5 updatedAt | L94: `created = json.loads(reg)["updatedAt"]` | 1 | 2 | 0 | survived |
| M6 reverse-order | L101: `order_ok = first[1] > cts` | 1 | 2 | 1 | killed by snapshot-green only |

Output details and coverage findings:

- M1: both evaluable outputs were byte-identical to their pristine outputs. Neither dataset exercises equal receipt/data times.
- M2: both evaluable outputs were byte-identical to pristine. The red case is both late and shape-incomplete, so dropping shape enforcement remains hidden by lateness. The green case has every default shape.
- M3: round-24 output was unchanged. Snapshot-green selected `459dd17f8fd6`, committed `2026-10-23T07:29:16+00:00`, rather than `7228299d94b1`; it printed `order=ok gap_s=125 shapes_missing=-` and still PASS. Both the oldest and newest qualifying additions predate this registry, so exit-only detection does not distinguish them.
- M4: round-24 output was unchanged because it already uses `--any-md`. Both round-25 cases counted 20 receipts instead of 19, proving the altered qualification executed. Snapshot-green still reported the same earliest commit, gap, complete shapes, and PASS.
- M5: round 24 read `2026-10-23T03:53:55.642Z` instead of its creation time and printed `order=ok gap_s=20 shapes_missing=EmptyArray|AllFalse,Echo,LabelKeyed`, but still FAIL / exit 1. Shape incompleteness masks the wrong timestamp. Snapshot-green output was unchanged because its two timestamp fields are equal.
- M6: round 24 incorrectly printed `order=ok gap_s=-1083` but still FAIL because of missing shapes. Snapshot-green printed `order=LATE gap_s=7695 shapes_missing=-` and `CONTROL_RECEIPTS verdict=FAIL`, exit 1, instead of the pristine exit 0. This is the only behavioral kill.

These survivors are coverage findings for this detector pair, not permission to relax the checker contract or a claim that the mutants are equivalent.

## Hashes, receipts, and restoration

Each JSON receipt contains the complete command, expected exit, actual exit, stdout, stderr, timeout flag, and scratch/lane checker hashes before and after the detector calls. Receipt directory:

`/fast/scratch/hyaku/mado-r25a3/mutq36/`

| Mutant | Mutant checker SHA-256 | Mutated receipt | Exact-restoration receipt |
| --- | --- | --- | --- |
| M1 | `7d4cb00db64d93ccf7653d9a2a40b79015018a36543ba4ce803d3a2094b82db7` | `m1-nonstrict.json` | `m1-restored.json` |
| M2 | `e5584a52eed2f41cc277995a81e206b675f5a0213879de62355e4e89c376c12c` | `m2-ignore-shapes.json` | `m2-restored.json` |
| M3 | `1688b50ad4cd5e06ea9875e195ab8a37b7af36c3f705d04543c5506ab01830e5` | `m3-newest-receipt.json` | `m3-restored.json` |
| M4 | `bcc2d94e78d8e3cb27d4603dd4bd9f63178ec015a6273a224374fa7b2dad4b05` | `m4-any-markdown.json` | `m4-restored.json` |
| M5 | `af9170567a89bb8a57278f85f3e5e188ae27aada16cdd4af3934b82fd4d2a190` | `m5-updated-at.json` | `m5-restored.json` |
| M6 | `3b3a8d65b3d0a2768b10dfceecfeaeb8bdd08116934dc0061da6597ad6be9239` | `m6-reverse-order.json` | `m6-restored.json` |

`baseline.json` records the original baseline. Before M1 the baseline was pristine; before each later mutant, the preceding restoration receipt is its pristine baseline. Each mutant's before/after detector hashes matched that row's mutant hash. Every restoration returned the scratch checker to `90542cad47d9004eaad83508ca2a3bfa81b15b4a932642d58942d23e58471f72` and reran all three detector commands, reproducing exits `1, 2, 0` and the pristine outputs above. Every receipt also recorded the lane checker as that same pristine hash before and after. Final scratch bytes are restored, not left mutated. No lane Python module was imported and all Python invocations used `-I -B`.

39 bounded detector invocations were exercised: 3 initial pristine, 18 mutated, and 18 restored. No builds, linters, broader tests, or actual pinned round-25 green check passed or are claimed.

MUTQ36: killed 1/6; survivors: M1 nonstrict, M2 ignore-shapes, M3 newest-receipt, M4 any-md, M5 updatedAt

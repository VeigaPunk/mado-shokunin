# CapHarnessFailClosedCheck1343 — C2 row re-run at 41cc04c8

## Ledger line

`| SCORECARD.md:1343 | harness fail-closed check | Show whether a stub/namespace harness runs its payload after any of six forced setup failures | works, exit 0 at 41cc04c8: all six modes FAIL_CLOSED, POSITIVE_CONTROL_OK isolate.sh, positive execution-witness=present | cd /fast/scratch/hyaku/mado-r25a3/c2/CapHarnessFailClosedCheck1343 && timeout 600 prlimit --as=4000000000 bash .ufo/waves/round-20/isolation-check.sh .ufo/waves/round-20/isolate.sh | SCORECARD.md:1583 (round-24 status table: works at 8e5d9369; that table supersedes the implied works of every earlier row) |`

## Row under test

Base revision `41cc04c8d593837a0d5078bffaacdaa163d12897`. SCORECARD.md is 1,618 lines at that revision, sha256:`6b6995ff6998a405c2d4472463204b16e644829ad821a368922a65a60853ca08` (dumped with `git show 41cc04c8:SCORECARD.md`).

- Row `SCORECARD.md:1343` sits in `### Capabilities (round 20)` (line 1337), inside `## Round 20 — committed results and bounded author verdicts`.
- Row text, verbatim: `| harness fail-closed check | Show whether a stub/namespace harness runs its payload after any of six forced setup failures | \`bash .ufo/waves/round-20/isolation-check.sh HARNESS\` (\`evidence/crit29-*.txt\`) | 20 |`
- Stated capability: show whether a stub/namespace harness runs its payload after any of six forced setup failures.
- Demonstration command: `bash .ufo/waves/round-20/isolation-check.sh HARNESS`.
- Evidence pointer: `evidence/crit29-*.txt`. At the base tree that glob resolves to `.ufo/waves/round-20/evidence/crit29-isolate.txt` (the green `isolate.sh` receipt: `exit=0`, `POSITIVE_CONTROL_OK isolate.sh`, measured_commit=`28c68378`, tool_sha256=`2bf115db1658df32d5e89e600ad6ef47c0e2855beda5f25dfc936270604f6aa9`, harness_sha256=`332b3fed6ad680f0bd2eec35ff686b768e2619a828925f13d429807a817fcccc`) and `.ufo/waves/round-20/evidence/crit29-inns-r19-shape.txt` (the fail-open negative at the same commit, `CHECK_EXIT inns-r19-shape.sh=1`).

`HARNESS` is an argument placeholder, not a path. Literal invocation is not runnable as written: `bash .ufo/waves/round-20/isolation-check.sh HARNESS` exits 2 with `COULD_NOT_EVALUATE HARNESS (harness path does not resolve)` (observed, see below). The nearest documented form binds it to `.ufo/waves/round-20/isolate.sh`, which is exactly the argv recorded in the cited receipt and the form round 24 re-demonstrated (`POSITIVE_CONTROL_OK isolate.sh`). That form was used.

## Sandbox re-run

Clone preparation (GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE unset):

```sh
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r25a3/c2/CapHarnessFailClosedCheck1343
git -C /fast/scratch/hyaku/mado-r25a3/c2/CapHarnessFailClosedCheck1343 checkout -q --detach 41cc04c8
```

Observed: `HEAD=41cc04c8d593837a0d5078bffaacdaa163d12897`, `git status --porcelain` line count 0 (clean checkout).

Bytes exercised at base:

```text
f7aa051faee522f3c4b61494a7a75078b469a1b0f1d0f7503caa3f89777736e1  .ufo/waves/round-20/isolation-check.sh
89125ff7191f0d91799158c0e19695197784bda9e352c0fa0a59bbe0090b7f9a  .ufo/waves/round-20/isolate.sh
```

The cited `round-20/evidence` receipt carries the earlier v2 hashes because v3 landed afterwards in `f8576f7` (`git log --oneline -- .ufo/waves/round-20/isolation-check.sh .ufo/waves/round-20/isolate.sh`: `f8576f7` isolation harness/check v3, `28c6837` isolation check v2, `f3da504` initial). The later receipt `.ufo/waves/round-20/a2/evidence/iso/crit29-isolate.txt` (measured_commit `a8960de`) records `tool_sha256=f7aa051f…`, exactly the base checker bytes above, and ends `exit=0`; `git log` shows the harness last changed at `f8576f7`, so its bytes at `a8960de` are also the base `89125ff7…` bytes. The evidence chain therefore reaches the base bytes even though the row's pointer does not disambiguate versions.

Demonstration command (run from the clone root, never in the lane):

```sh
cd /fast/scratch/hyaku/mado-r25a3/c2/CapHarnessFailClosedCheck1343
timeout 600 prlimit --as=4000000000 bash .ufo/waves/round-20/isolation-check.sh .ufo/waves/round-20/isolate.sh
```

Result: `exit=0`, 58 output lines. All six forced-failure modes classify `FAIL_CLOSED`; the positive control prints `POSITIVE_CONTROL_OK isolate.sh` with `execution-witness=present`, proving the checker can see payload execution when it happens.

Literal-placeholder probe on the same checkout:

```sh
cd /fast/scratch/hyaku/mado-r25a3/c2/CapHarnessFailClosedCheck1343
timeout 600 prlimit --as=4000000000 bash .ufo/waves/round-20/isolation-check.sh HARNESS
```

Output, verbatim, followed by the command's recorded exit status:

```text
COULD_NOT_EVALUATE HARNESS (harness path does not resolve)
```

`exit=2`.

## Verbatim demonstration output

```text
SCOPE isolate.sh: fail-closed setup only; not containment; not a sandbox; never run a host probe under the host pause.

TRANSCRIPT setup-failure harness=isolate.sh mode=mount-nonzero targets=1
COMMAND: /fast/scratch/hyaku/mado-r25a3/c2/CapHarnessFailClosedCheck1343/.ufo/waves/round-20/isolate.sh --stub /tmp/mado-isolation-v3-check.VbkOQX/case.vJXBmN/stub --target /tmp/mado-isolation-v3-check.VbkOQX/case.vJXBmN/target -- /tmp/mado-isolation-v3-check.VbkOQX/payload.sh /tmp/mado-isolation-v3-check.VbkOQX/case.vJXBmN/canary
INJECTION: PATH-stub; controls are not exported
output:
forced mount failure (exit 32)
harness exit: 125; canary=absent; execution-witness=absent; injected-marker=present; cmp-stub=absent
FAIL_CLOSED isolate.sh mode=mount-nonzero

TRANSCRIPT setup-failure harness=isolate.sh mode=unshare-refused targets=1
COMMAND: /fast/scratch/hyaku/mado-r25a3/c2/CapHarnessFailClosedCheck1343/.ufo/waves/round-20/isolate.sh --stub /tmp/mado-isolation-v3-check.VbkOQX/case.BcwXxr/stub --target /tmp/mado-isolation-v3-check.VbkOQX/case.BcwXxr/target -- /tmp/mado-isolation-v3-check.VbkOQX/payload.sh /tmp/mado-isolation-v3-check.VbkOQX/case.BcwXxr/canary
INJECTION: PATH-stub; controls are not exported
output:
forced unshare refusal (exit 1)
harness exit: 125; canary=absent; execution-witness=absent; injected-marker=present; cmp-stub=absent
FAIL_CLOSED isolate.sh mode=unshare-refused

TRANSCRIPT setup-failure harness=isolate.sh mode=mount-noop targets=1
COMMAND: /fast/scratch/hyaku/mado-r25a3/c2/CapHarnessFailClosedCheck1343/.ufo/waves/round-20/isolate.sh --stub /tmp/mado-isolation-v3-check.VbkOQX/case.oKv0jU/stub --target /tmp/mado-isolation-v3-check.VbkOQX/case.oKv0jU/target -- /tmp/mado-isolation-v3-check.VbkOQX/payload.sh /tmp/mado-isolation-v3-check.VbkOQX/case.oKv0jU/canary
INJECTION: PATH-stub; controls are not exported
output:
forced successful no-op mount
harness exit: 125; canary=absent; execution-witness=absent; injected-marker=present; cmp-stub=absent
FAIL_CLOSED isolate.sh mode=mount-noop

TRANSCRIPT setup-failure harness=isolate.sh mode=partial-arm targets=2
COMMAND: /fast/scratch/hyaku/mado-r25a3/c2/CapHarnessFailClosedCheck1343/.ufo/waves/round-20/isolate.sh --stub /tmp/mado-isolation-v3-check.VbkOQX/case.ugI3yH/stub --target /tmp/mado-isolation-v3-check.VbkOQX/case.ugI3yH/t1 --target /tmp/mado-isolation-v3-check.VbkOQX/case.ugI3yH/t2 -- /tmp/mado-isolation-v3-check.VbkOQX/payload.sh /tmp/mado-isolation-v3-check.VbkOQX/case.ugI3yH/canary
INJECTION: PATH-stub; controls are not exported
output:
forced second-target mount failure (exit 32)
harness exit: 125; canary=absent; execution-witness=absent; injected-marker=present; cmp-stub=absent
FAIL_CLOSED isolate.sh mode=partial-arm

TRANSCRIPT setup-failure harness=isolate.sh mode=missing-target targets=1
COMMAND: /fast/scratch/hyaku/mado-r25a3/c2/CapHarnessFailClosedCheck1343/.ufo/waves/round-20/isolate.sh --stub /tmp/mado-isolation-v3-check.VbkOQX/case.h58PBT/stub --target /tmp/mado-isolation-v3-check.VbkOQX/case.h58PBT/absent -- /tmp/mado-isolation-v3-check.VbkOQX/payload.sh /tmp/mado-isolation-v3-check.VbkOQX/case.h58PBT/canary
INJECTION: real-filesystem-failure; controls are not exported
output:
mount: /tmp/mado-isolation-v3-check.VbkOQX/case.h58PBT/absent: mount point does not exist.
       dmesg(1) may have more information after failed mount system call.
harness exit: 125; canary=absent; execution-witness=absent; injected-marker=absent; cmp-stub=absent
FAIL_CLOSED isolate.sh mode=missing-target

TRANSCRIPT setup-failure harness=isolate.sh mode=missing-stub targets=1
COMMAND: /fast/scratch/hyaku/mado-r25a3/c2/CapHarnessFailClosedCheck1343/.ufo/waves/round-20/isolate.sh --stub /tmp/mado-isolation-v3-check.VbkOQX/case.15W8nl/stub --target /tmp/mado-isolation-v3-check.VbkOQX/case.15W8nl/target -- /tmp/mado-isolation-v3-check.VbkOQX/payload.sh /tmp/mado-isolation-v3-check.VbkOQX/case.15W8nl/canary
INJECTION: real-filesystem-failure; controls are not exported
output:
mount: /tmp/mado-isolation-v3-check.VbkOQX/case.15W8nl/target: special device /tmp/mado-isolation-v3-check.VbkOQX/case.15W8nl/stub does not exist.
       dmesg(1) may have more information after failed mount system call.
harness exit: 125; canary=absent; execution-witness=absent; injected-marker=absent; cmp-stub=absent
FAIL_CLOSED isolate.sh mode=missing-stub

TRANSCRIPT positive-control harness=isolate.sh
COMMAND: /fast/scratch/hyaku/mado-r25a3/c2/CapHarnessFailClosedCheck1343/.ufo/waves/round-20/isolate.sh --stub /tmp/mado-isolation-v3-check.VbkOQX/positive/stub --target /tmp/mado-isolation-v3-check.VbkOQX/positive/target -- /tmp/mado-isolation-v3-check.VbkOQX/payload.sh /tmp/mado-isolation-v3-check.VbkOQX/positive/canary
output:
harness exit: 0; canary=present; execution-witness=present
POSITIVE_CONTROL_OK isolate.sh
SCOPE isolate.sh: fail-closed setup only; not containment; not a sandbox; never run a host probe under the host pause.
```

Command exit: `0` (58 stdout lines above).

## Supersede / contradiction scan of SCORECARD.md at 41cc04c8

Command: `grep -n "harness\|fail-closed\|isolation\|FAIL_CLOSED\|FAIL_OPEN\|crit29\|stub/namespace" /tmp/mado-sc-41cc04c8.md` (the base dump) plus a full `retire|withdraw|supersed` scan.

Occurrences relevant to this row:

- `1266`: QUALITY criterion 29 text ("an isolation harness fails closed"), the criterion the row demonstrates.
- `1331`: round-20 C2 row, "red `inns-r19-shape.sh` `FAIL_OPEN` 5/6 modes, exit 1 → green `isolate.sh` `FAIL_CLOSED` 6/6 + positive control, exit 0 (`evidence/crit29-*.txt`)".
- `1394`: round-20 attempt-2 C2 row, "29 re-verified at `a8960de` (`a2/evidence/iso/`): red 5/6 `FAIL_OPEN` exit 1, green 6/6 `FAIL_CLOSED` exit 0, four adversarial harnesses and four mutants exit 1".
- `1583`: later row `| harness fail-closed check | works | six forced setup failures classified, POSITIVE_CONTROL_OK isolate.sh, at 8e5d9369 |` in the round-24 re-demonstration table, whose preamble (line 1570) says "This table supersedes the implied `works` of every earlier row; the earlier rows stay as written." The round-24 scope note (lines 1589–1598) confirms this row is in the counted 12-row Capabilities population.
- No later row retires, contradicts, or reclassifies this capability; line 437's stale collision-screen note is a different capability. The round-24 table's `works` and this re-run's `works` agree.

## Safety and cleanup

- Host state: no packages, services, home configuration, live compositor, git/jj state, counter, corpus, or lane file was modified. No nested Hyprland, no network, no hyprctl verb was invoked. No tools were installed or upgraded.
- The check only writes under `/tmp` (its own mktemp dirs, removed by its trap) and enters a private user/mount namespace; `unshare --user --map-root-user true` probed `exit=0` beforehand. All mounts are bind mounts onto paths it created inside the namespace.
- After the runs: zero leftover `/tmp/mado-isolation-v3-check.*` or `/tmp/mado-isolation-v3-observer.*` directories, and zero surviving `isolation-check`/`isolate.sh` processes (checked with `ls -d` count and `pgrep -af`).
- The sandbox clone was deleted before this seat returned; `ls -d` on the clone path afterwards reported `No such file or directory`. `/fast` had 221 GB free at start (`df -h /fast`).

## Risks / limits

- The check's own SCOPE line is binding: this is fail-closed setup behavior only, not containment and not a sandbox. The green result must not be read as proof that a harness contains its payload.
- The row's evidence pointer is a loose glob over a v2-era receipt; the base tree carries v3 scripts whose hashes match the later `a2/evidence/iso/` receipt. The capability re-demonstrates green at base, but a future ledger should cite the v3 receipt path or the exact hashes.
- Userns availability is a host precondition. On a host with unprivileged user namespaces disabled, the positive control could not run and the check would exit 2 rather than report FAIL_CLOSED; not observed here.

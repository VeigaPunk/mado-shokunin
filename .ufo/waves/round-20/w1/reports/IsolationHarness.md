# IsolationHarness — fail-closed isolation added; round-19 shape reproduced fail-open

## Deliverables

- `.ufo/waves/round-20/isolate.sh`: parses repeated `--target` arguments, enters `unshare --user --map-root-user --mount --propagation private`, bind-mounts the stub over every target, verifies each target with `cmp`, then executes the command. A per-run `/tmp` completion marker preserves the payload's exit status; if `unshare`, any bind, any comparison, or another pre-exec setup step fails, the marker is absent and the wrapper returns 125 without running the payload. Explicit `|| exit 125` gates guard each mount and comparison (`isolate.sh:42-76`).
- `.ufo/waves/round-20/isolation-check.sh`: accepts one harness, uses only fresh `/tmp` files for stub/target/canaries, injects a PATH-first `mount` that exits 32, reports fail-open/fail-closed/could-not-evaluate, and performs a positive setup control (`isolation-check.sh:16-99`). The payload script only writes its supplied canary path (`isolation-check.sh:33-38`).
- `.ufo/waves/round-20/evidence/inns-r19-shape.sh`: minimal reproduction of the unchecked `[ -e "$p" ] && mount --bind ... && echo armed` loop followed by the payload (`inns-r19-shape.sh:37-55`). It preserves `set -e` so the test exercises the same conditional-list behavior described in the incident.

## Evidence

The incident source says the first harness used an unchecked `[ -e ] && mount && echo` chain, failed mounts did not stop the payload despite `set -e`, and the smoke payload ran (`.ufo/waves/round-19/w2/reports/SentinelGatePath.md:75-79`, especially line 77). The reproducer keeps that failure shape but uses `--map-root-user` so the positive-control setup can be exercised; the historical report records `--map-current-user`.

Ran the isolated red case:

`bash /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/isolation-check.sh /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/evidence/inns-r19-shape.sh`

Observed transcript excerpt (checker exit status 1, expected for fail-open):

```text
TRANSCRIPT setup-failure: inns-r19-shape.sh
output:
forced mount setup failure (exit 32)
harness exit: 0
FAIL_OPEN inns-r19-shape.sh
TRANSCRIPT positive-control: inns-r19-shape.sh
output:
armed /tmp/mado-isolation-check.4epipl/positive.target
harness exit: 0
POSITIVE_CONTROL_OK inns-r19-shape.sh
```

Ran the new wrapper case:

`bash /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/isolation-check.sh /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/isolate.sh`

Observed transcript excerpt (checker exit status 0):

```text
TRANSCRIPT setup-failure: isolate.sh
output:
forced mount setup failure (exit 32)
harness exit: 125
FAIL_CLOSED isolate.sh
TRANSCRIPT positive-control: isolate.sh
output:
harness exit: 0
POSITIVE_CONTROL_OK isolate.sh
```

Both runs used `/tmp/mado-isolation-check.*` files only for targets, stubs, payload, and canaries. No host binary was named or invoked as a target or payload. The positive control also observed that the requested user/mount namespace and real bind+cmp setup succeeds on this host.

SHA-256 evidence (`sha256sum`):

```text
332b3fed6ad680f0bd2eec35ff686b768e2619a828925f13d429807a817fcccc  .ufo/waves/round-20/isolate.sh
9937310f1ad44d673918f6396cb8ce2d56559556e8f087237c0d31deaf35e483  .ufo/waves/round-20/isolation-check.sh
8bd507f0ea39d4d876359a0f5a1f798e810cda3c59293487af35d3a8df37ce9c  .ufo/waves/round-20/evidence/inns-r19-shape.sh
```

## V2 Hardening

Expanded `isolation-check.sh` to run six setup-failure modes per harness: nonzero mount, refused unshare, mount-success-without-bind, partial arm of two targets, missing target, and missing stub. The marker files attest invocation of PATH-injected `mount`/`unshare`; if an injected stub is bypassed, the verdict is `COULD_NOT_EVALUATE` (not `FAIL_OPEN`). A zero-exit failure with no canary is classified `FAIL_OPEN ... SKIP_AS_SUCCESS`; a failed positive control prints `NEVER_RUNS` and exits 1 (`isolation-check.sh:25-30,35-146,148-180`). Each mode has a separate fresh `/tmp` case directory, and the payload only writes its canary.

Observed results in the saved transcript `.ufo/waves/round-20/evidence/isolation-check-run.txt`:

| Harness | Observed failure result | Check exit |
|---|---|---:|
| `isolate.sh` | `FAIL_CLOSED` for all six modes; `POSITIVE_CONTROL_OK` | 0 (`:11-60`) |
| `inns-r19-shape.sh` | `FAIL_OPEN` on nonzero mount, no-op mount, partial arm, missing target and missing stub; positive control ran | 1 (`:70-120`) |
| `m1-nocmp.sh` | `FAIL_OPEN` on no-op mount | 1 (`:146,179`) |
| `m3b-capprobe.sh` | `FAIL_OPEN` on refused unshare | 1 (`:197,238`) |
| `m6-besteffort.sh` | `FAIL_OPEN` on partial arm | 1 (`:272,297`) |
| `m4-skiptarget.sh` | `FAIL_OPEN` on missing target | 1 (`:338,354`) |

Additional checker behavior was exercised: the absolute-mount bypass control returned `COULD_NOT_EVALUATE` because its injected marker stayed absent, with final exit 2 (`isolation-check-run.txt:363-410`). A temporary zero-exit/no-canary control produced `FAIL_OPEN ... SKIP_AS_SUCCESS` (line 419) and a failed positive control printed `NEVER_RUNS` and exited 1 (lines 456-461). Its temporary harness was removed after the run.

The `isolate.sh` implementation was not changed: the six-mode run confirmed exit 125 and no canary for each setup failure, including unshare refusal and a no-op bind detected by `cmp`. All actual and injected test targets and canaries were under fresh `/tmp` directories; the partial-arm stub performed a real bind only over its `/tmp` first target before failing its `/tmp` second target. No host binary was used as a target or payload.

Transcript receipt: `tool_sha256=2bf115db1658df32d5e89e600ad6ef47c0e2855beda5f25dfc936270604f6aa9`, `measured_commit=PENDING`. Current artifact hashes (`sha256sum`):

```text
2bf115db1658df32d5e89e600ad6ef47c0e2855beda5f25dfc936270604f6aa9  .ufo/waves/round-20/isolation-check.sh
7d12321793c44b54eec74791dfc5063b64d235772f3d703fe959b2daa1db2703  .ufo/waves/round-20/evidence/isolation-check-run.txt
2f2cc63bdb4903a42d99bf5685acc12e5b221158610217e42b0c1ee3d85df359  .ufo/waves/round-20/evidence/isolation-mutants/m1-nocmp.sh
a6dde1c30355b29917091f0045b51befcefc7fc78d0903c098fc880ff9099727  .ufo/waves/round-20/evidence/isolation-mutants/m3b-capprobe.sh
ac11cc5adb1ece61eba4d45a8e2b65016576eb247957a846afe797b9118c6ed4  .ufo/waves/round-20/evidence/isolation-mutants/m6-besteffort.sh
a9bfa1be563c76e74edffa480514e69f3ee85ead8415e54b865d02be10107940  .ufo/waves/round-20/evidence/isolation-mutants/m4-skiptarget.sh
```

## Limits

- Namespace refusal was simulated with a PATH-first stub returning 1; the host's real positive-control namespace setup succeeded.
- The post-mount comparison failure was exercised using a successful no-op mount; a separate mismatch after a real successful bind was not exercised.
- Payload nonzero-status propagation was not separately re-tested in the v2 run. No full repository build, lint, or suite was run.

## Installs

none

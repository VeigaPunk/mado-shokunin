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

## Limits

- The checker exercises one target per run; the repeated-target loop is implemented but not separately exercised.
- The controlled negative run fails the bind step; a forced `cmp`-failure case and payload nonzero-status propagation were not separately exercised.
- No blocker observed. No repository build, lint, or test suite was run.

## Installs

none

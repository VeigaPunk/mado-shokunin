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

## V3 Hardening

Built and tested in `/tmp/mado-r20-IsolationHarness-3-v3`; after cloning, removed `origin` and observed `git rev-parse HEAD=a4046a8216080d4004de3f268c62cf142095ac07` (remote list empty). Delivered full versions at `.ufo/waves/round-20/w2/IsoV3/isolate.sh` and `isolation-check.sh`.

`isolate.sh` still resolves `unshare` and `mount` through PATH for injectable setup failures, but replaces PATH-resolved `cmp` with fixed-path `/usr/bin/stat -Lc "%d:%i"` identity comparison after the bind loop (`isolate.sh:44-65`). The checker puts a no-op mount and fake `cmp` returning 0 in PATH for the mount-noop case; v3 fails closed without invoking that `cmp`, while the fake-cmp harness invokes it and reads red. Before `exec`, the runner unsets `HYPRLAND_INSTANCE_SIGNATURE`, `WAYLAND_DISPLAY`, `DBUS_SESSION_BUS_ADDRESS`, and `XDG_RUNTIME_DIR` (`isolate.sh:67-69`). Header and usage warn that fail-closed setup is not containment, is not a sandbox, and must never be used for a host probe under the host pause (`isolate.sh:2-4,7-10`).

`isolation-check.sh` removes `CHECK_MODE`, `CHECK_MARKER`, and `CHECK_REAL_PATH` from its own environment and applies only a PATH override for stub injection when launching the harness (`isolation-check.sh:18-21,165-170`). Per-mode values and marker paths are baked into generated stub sources (`:93-156`); randomized case-directory names do not disclose the mode in PATH. The payload writes the visible canary and an execution witness through fd 9; the checker opens that witness in a private `/tmp` directory and unlinks its pathname before launching the harness (`:35-50`). Verdicts use the witness rather than canary presence alone; an injected stub that was not invoked yields `COULD_NOT_EVALUATE`, and a zero exit without a witness is `SKIP_AS_SUCCESS`/`FAIL_OPEN` (`:177-199`). A failed positive control now emits `NEVER_RUNS` and exits 2 (`:221-239`).

The saved `.ufo/waves/round-20/w2/IsoV3/run.txt` records every run; its receipt binds checker SHA-256 `97cdef57b0d4a5f55b9611223321f13127e0c2bd2a20e7f10279e71771427842` to measured commit `a4046a8216080d4004de3f268c62cf142095ac07`. Observed outcomes:

| Harness/control | Result in `run.txt` |
|---|---|
| v3 `isolate.sh` | All six setup failures `FAIL_CLOSED`, exit 125/no execution witness; positive control `POSITIVE_CONTROL_OK`; checker exit 0 (`:13-63`). |
| `inns-r19-shape.sh` (made executable in the clone) | `FAIL_OPEN` on mount-nonzero, mount-noop, partial-arm, missing-target and missing-stub; exit 1 (`:75-126`). |
| `m1-nocmp.sh`, `m3b-capprobe.sh`, `m6-besteffort.sh`, `m4-skiptarget.sh` | Each red/exit 1 on its mutant mode; respectively no-op mount (`:154,188`), unshare refusal (`:208,250`), partial arm (`:286,312`), and missing target (`:355,372`). |
| RevQuality29 `masked.sh` and `canary-deleter3.sh` | Both red/exit 1; control environment was absent. The latter also reads `FAIL_OPEN` for `SKIP_AS_SUCCESS` on refused unshare (`:384-494`). |
| Fake-cmp harness | Red/exit 1 on mount-noop; transcript confirms `cmp-stub=present` and payload witness (`:522,556`). |
| Absolute-mount bypass control | `COULD_NOT_EVALUATE` when injected mount was not observed; exit 2 (`:571,586,593,619`). |
| Zero-exit/no-payload control | `SKIP_AS_SUCCESS` red and `NEVER_RUNS` on positive control; checker exit 2 (`:630,671-672`). |
| Session-variable scrub probe | Supplied synthetic values for all four variables; payload observed them unset and wrote `session-vars-unset`; exit 0/canary present (`:558-560`). |

The four mutant harness copies run from the clone were SHA-256 identical to the assigned lane fixtures; their paired hashes match the v2 evidence list at lines 84-87.

Current v3 artifact SHA-256 (`sha256sum`):

```text
89125ff7191f0d91799158c0e19695197784bda9e352c0fa0a59bbe0090b7f9a  .ufo/waves/round-20/w2/IsoV3/isolate.sh
97cdef57b0d4a5f55b9611223321f13127e0c2bd2a20e7f10279e71771427842  .ufo/waves/round-20/w2/IsoV3/isolation-check.sh
e3e3807330377f64cb813429e455f501f90c3b562a6fdc146d369d3f7757b652  .ufo/waves/round-20/w2/IsoV3/run.txt
```

## Limits

- Namespace refusal was simulated with a PATH-first stub returning 1; the host's real positive-control namespace setup succeeded.
- The post-bind check was exercised with a successful no-op mount and fake `cmp`; a separate mismatch after a real successful bind was not exercised.
- The unlinked fd 9 witness survives canary deletion, but this is not containment against a subject deliberately manipulating inherited descriptors. Session-scrub validation used synthetic values only; no live session socket or host probe was touched.
- Payload nonzero-status propagation was not separately re-tested. No full repository build, lint, or suite was run.

## Installs

none

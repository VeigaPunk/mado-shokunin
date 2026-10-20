# ScoutUnshareHost — unprivileged user+mount namespaces work with `--map-root-user`; `--map-current-user` reproduces the round-19 mount failure exactly and does not stop a payload

Scope: the IsolationHarness item (`spec.json:95`, R19-V4 / QUALITY 29). All probes ran in fresh `/tmp` dirs as the
unprivileged user (uid 1000); payloads were canary writes only. No host binary was executed as a target, no
pacman/systemctl/hyprctl/jj/git write was run. Host binaries were only read as bytes for `--version`/`sha256sum`.

Host: `uname -r` = `7.2.11-arch1-1`; `/usr/bin/unshare` = util-linux 2.42.4
(`sha256 e4e385ae4accf4af5302c4bb32859355b1c640315bef56ce73d31b8b1f97fdc0`); `/usr/bin/mount` = util-linux 2.42.4
(libmount 2.42.4: btrfs, verity, namespaces, idmapping, fd-based-mount, statmount, statx, fanotify, udev, assert,
debug; `sha256 ca6c26aa2b11a8431481d39ee562bc07a88984f3294f34846d3257ec28ae9c91`). `/tmp` is `xfs`
(`stat -f -c %T /tmp`). Host knobs: `/proc/sys/user/max_user_namespaces` = `122865`,
`/proc/sys/kernel/unprivileged_userns_clone` = `1`, `apparmor_restrict_unprivileged_userns` absent.

## Answer to the assigned question (observed)

1. **`--map-root-user` works, unprivileged.** The exact requested command shape
   `unshare --user --map-root-user --mount --propagation private sh -c 'mount --bind /tmp/a /tmp/b && cmp /tmp/a /tmp/b && echo ok'`
   was run with literal `/tmp/a` and `/tmp/b` (created only because both were absent, removed after):
   **exit 0, stdout `ok\n`, stderr empty.** With unique probe paths the inner state was
   `inner_uid=0`, `inner_gid=0`, uid_map `         0       1000          1`, gid_map `         0       1000          1`,
   `CapEff: 000001ffffffffff`, `mount_rc=0`, `cmp_rc=0`, and the bound target showed the stub's bytes.
2. **`--map-current-user` reproduces the round-19 failure exactly.** Inner `uid=1000`, uid_map
   `      1000       1000          1`, **`CapEff: 0000000000000000`**, and `mount --bind` fails:
   ```
   mount: /tmp/unshare-probe2.49lpq6b6/b: must be superuser to use mount.
          dmesg(1) may have more information after failed mount system call.
   ```
   **mount exit 32**, outer `unshare` exit 0 when the payload continues (see fail-open below). This is byte-for-byte
   the round-19 `SentinelGatePath.md:77` failure mode: `unshare --user --map-current-user --mount` → "mount refused
   ('must be superuser to use mount') for all 16 paths".

## Fail-open is reproducible; an explicit exit-status gate closes it (observed)

The round-19 `inns.sh` shape was re-run with a canary payload, under `--map-current-user`:

```sh
unshare --user --map-current-user --mount --propagation private sh -c \
  '[ -e STUB ] && mount --bind STUB T1 && echo ARMED; echo FAILOPEN > HOST_CANARY'
```

Result: stderr carries the `must be superuser` message, mount rc 32, **stdout has no `ARMED`, but the canary file
appears on the host with `FAILOPEN\n`; outer rc 0.** With `set -e` added the payload still ran
(stdout `PAYLOAD-AFTER-FAILED-MOUNT\n`, rc 0): the failing `mount` is a non-final element of an `&&` list, so
`set -e` does not stop it — this is the exact mechanism the round-19 report attributes to the incident
(`SentinelGatePath.md:77`: "the script's `[ -e ] && mount && echo` chain does not trip `set -e`"). The chain's own
exit status is only 32 when it is the *last* command of the shell (probe Q4: rc 32), which is why a script with any
following command fails open.

A fail-closed gate with explicit status, verified in its own namespace:

```sh
if ! unshare --user --map-root-user --mount --propagation private sh -c '
      mount --bind "$1" "$2" || exit 125
      cmp -s "$1" "$2" || exit 125
      echo STUB-INSTALLED
    ' sh STUB TARGET; then
  echo ABORT-SETUP
  exit 125
fi
echo PAYLOAD-RAN
```

- valid target: rc 0, stdout `STUB-INSTALLED\nPAYLOAD-RAN\n`.
- missing target: inner mount rc 32 (`mount: .../missing-target: mount point does not exist.`), gate rc **125**,
  stdout only `ABORT-SETUP`, **no `PAYLOAD-RAN`**.
- `--map-current-user` + explicit gate: gate rc **125**, post-gate host canary not created (verified absent).
- post-mount `cmp` forced to mismatch (bind a stub onto the target, then `cmp` target against a different file):
  rc **125**, `SHOULD-NOT-PRINT` absent.

`unshare` propagates the payload's exit status directly (no `--fork`): observed outer rc 99, 88, 125 and 32 from
inner `exit 99`, `|| exit 88`, `|| exit 125`, and a failed mount as last command. So `exit 125` inside the gate is
observable by `isolate.sh` as its own 125.

## Reachable setup-failure modes (for `isolation-check.sh`)

All verified on this host without touching a host binary as a target; exit codes/messages exact:

| Mode | Invocation result | Gate result |
|---|---|---|
| missing target | mount rc 32, `mount: PATH: mount point does not exist.` | `|| exit 125` → 125 |
| missing stub | mount rc 32, `mount: TARGET: special device STUB does not exist.` | 125 |
| no root mapping (`--map-current-user`, the round-19 mode) | mount rc 32, `mount: TARGET: must be superuser to use mount.` | 125 |
| post-mount cmp mismatch | `cmp` rc 1 (silent) | 125 |
| userns unavailable / unshare refused | plain `unshare --mount --propagation private sh -c ...` → **rc 1**, stderr `unshare: unshare failed: Operation not permitted\n`, `sh -c` never runs | outer `if !` → abort |
| stub is a file, target a directory | mount rc 32, `wrong fs type, bad option, bad superblock on STUB, missing codepage or helper program, or other error.` | 125 |
| one `mount --bind STUB T1 T2` for two targets | **rc 1**, `mount: bad usage` — bind takes one target per call | must loop per target |

The loop form works: `for t in T1 T2; do mount --bind STUB "$t" || exit 125; cmp -s STUB "$t" || exit 125; done`
→ rc 0, `BOTH-ARMED`, and `cmp` T1 vs T2 equal. Namespace contents do not leak: host `/proc/self/mountinfo`
contained no probe path after exit, host canary bytes were unchanged, and a tmpfs-mounted canary created inside
the namespace was invisible on the host after exit (host dir listing empty). `--propagation private` is explicit
in the item and harmless; util-linux ≥2.27 sets it automatically (the fetched `unshare.1.adoc:30` says so, and the
same probe without the flag also returned `ok`/rc 0).

## Sizing for the IsolationHarness

- The item's exact launcher `unshare --user --map-root-user --mount --propagation private` is viable on this host
  **unprivileged** (uid 0 inside mapped to host 1000, both uid and gid maps `0 1000 1`, full namespaced caps).
- `--map-current-user` must never be used as a fallback: it yields **zero capabilities** and mount rc 32 with the
  round-19 message. It is the ideal *forced failure* input for `isolation-check.sh` (the "bind EPERM" mode),
  provided the check asserts rc 125 and the absence of the payload marker.
- The abort must be driven by the **inner mount/cmp exit status** (`|| exit 125` / `if ! ...`), not by `set -e`
  and not by the outer `unshare` rc alone: a payload that continues after a failed mount yields outer rc 0.
- `exit 125` is propagated by `unshare` unchanged, so `isolate.sh`'s documented "abort with exit 125 before
  exec'ing CMD" is implementable as shown; the CMD should be `exec`'d only after every bind + `cmp` gate passes in
  the same namespace, e.g. `sh -c '<gate>; exec "$@"'` (the gate runs, then CMD replaces the shell; no CMD runs on
  gate failure).
- Bind one target per `mount --bind`; loop. Mount over `/tmp` files on xfs works. [INFERENCE] Mounting a stub over
  a host-owned `/usr/bin/*` path inside this user+mount namespace is permitted by kernel semantics (mount ns owned
  by the new userns) and round-19 reports every later run "armed" all 16 paths after switching to
  `--map-root-user` (`SentinelGatePath.md:79`), but I did not re-test such targets under the host pause.

## Limits

- No host binary was used as a mount target, and no real gate/suite was run; `/usr/bin/*` bind coverage is
  [INFERENCE] + round-19's own report, not this probe.
- Only file-over-file binds and tmpfs were tested; file-over-directory was tested only as a failure mode. No
  btrfs or lane-checkout path was mounted; `/tmp` is xfs.
- Not tested: `--fork`, PID/UTS/net namespaces, signal forwarding, `--map-users`/subuid mappings, other non-root
  uids, setuid/`NoNewPrivs` interactions (`NoNewPrivs: 0` observed), or kernel-configuration changes since the
  probe.
- Scratch dirs `/tmp/unshare-probe{,2,3,4}.*` remain; all canaries are `/tmp`-only. `/tmp/a` and `/tmp/b` were
  removed after the literal probe.
- The fail-open canary write is host-visible by design; the namespace is not a filesystem sandbox for anything
  except the explicitly bound paths.

## Installs

none.

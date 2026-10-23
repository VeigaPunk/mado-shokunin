# SentinelHarness — round 26, w1

## Scope and method

Read-only review of `harness/oracle.py`, `harness/pilot.py`, `harness/build-tinywl.sh`, and the C1/C2 counters' calls into the harness. No counter, pilot, oracle, or build was run; no code was changed. The recorded `harness/pilot-receipt.txt` was read as historical evidence, not re-exercised.

## Findings

### MEDIUM — tool-under-test has no memory, output, or core-dump bound

**Exploit path:** supply a `--tool-file` that rapidly writes stdout/stderr, allocates memory, or calls `os.abort()`; both counters execute it for each case (`c1/count.py:261-266`, `c2/count.py:199-205`).

**Evidence:** `oracle.py:232-243` wraps the tool in `timeout` and bubblewrap, but invokes `subprocess.run(..., capture_output=True)` without an output cap or `prlimit`. The separate oracle launch does set `--core=0` and `--as=8000000000` (`oracle.py:146-147`); those limits do not cover `run_tool`. The counter's core-dump check counts only `/usr/bin/Hyprland` (`oracle.py:60-62`), so it would not report a Python-tool core. In this environment the inherited core limit was `unlimited`, and `/proc/sys/kernel/core_pattern` is `|/usr/lib/systemd/systemd-coredump ...`.

**Impact:** the child and the parent holding captured output can consume host memory; an abort is eligible to create a host systemd-coredump record. Network and filesystem isolation do not impose resource limits.

**Smallest remediation:** apply an address-space and `RLIMIT_CORE=0` limit to the tool process, cap stdout/stderr bytes while draining them, and use a kill-after timeout.

### MEDIUM — symlinked config roots/files can copy unrelated readable data into the tool sandbox

**Exploit path:** point one of the configured roots (or a file beneath it) at another user-readable directory/file, then run C2 with a tool that reads `/snap/home` and returns the contents in an extra bind's `arg` field.

**Evidence:** `oracle.py:69-85` canonicalizes each root with `realpath` and follows files through `isfile`/`open`, with no containment check against the intended home/config roots. The snapshot is then mounted for the tool at `/snap/home` (`oracle.py:232-237`). C2 prints up to two extra bind summaries per case, including `arg` truncated to 50 characters (`c2/count.py:210-213`; formatter `round-25/c1/count-v3.py:754-756`).

**Impact:** a malicious tool can read files that were not intended as config inputs and disclose fragments through the counter's stdout/receipt. This does not give it a host socket or network access.

**Smallest remediation:** reject resolved roots and files outside an explicit approved-root allowlist before copying; preserve only intended in-home symlinks.

### MEDIUM — snapshot, case copies, and oracle logs have no aggregate disk bound

**Exploit path:** place many small files (or many files under the per-file 1 MiB cutoff) in a config root, or use config input that produces extensive compositor logs, then run either counter.

**Evidence:** `snapshot()` limits individual file size but not total bytes or file count (`oracle.py:65-88`). C1 makes 40 case copies and submits an oracle run for each (`c1/count.py:236-249`); C2 similarly builds its ARITH/V3 cases (`c2/count.py:175-190`). Each oracle copies its case tree again (`oracle.py:137-143`) and redirects compositor output to an uncapped `work/sandbox.log` (`oracle.py:161-164`). The trees and logs reside under the counters' `/fast` temporary directory.

**Impact:** one run can consume excessive `/fast` space before its normal cleanup, causing unrelated work or later runs to fail.

**Smallest remediation:** enforce aggregate file-count/byte limits while snapshotting and impose a size cap/rotation on `sandbox.log`.

### LOW — interruption can leave `/fast` and `/tmp` artifacts

**Exploit path:** terminate a counter with SIGTERM (including a timeout) while it is building cases or waiting for an oracle slot, or encounter an exception after the pilot creates its temporary directory.

**Evidence:** the counters remove their `/fast` tree in `finally` (`c1/count.py:289-290`, `c2/count.py:226-227`), which ordinary Python exceptions run but the default SIGTERM termination does not. `oracle.py:144` creates the `/tmp/m26o-*` directory before entering the `try/finally` that removes it (`oracle.py:161-227`); failures while acquiring a slot, opening the log, or starting `Popen` bypass that cleanup. `pilot.py:45-47,67-80` also has no `finally` around its `/fast` temp directory.

**Impact:** interrupted runs can leave copied config trees/logs in `/fast` and private runtime directories in `/tmp`. Normal oracle cleanup kills its process group and `--die-with-parent` is also set; this finding is about residual files, not a demonstrated surviving compositor.

**Smallest remediation:** start cleanup protection immediately after each `mkdtemp`, including pilot and the oracle runtime directory, and handle SIGTERM by entering cleanup.

### LOW — slot-file open follows symlinks and permits inode replacement

**Exploit path:** a same-UID process pre-creates `slot-0.lock` as a symlink to a writable file, or unlinks/recreates a slot path while another process holds its flock, then starts a counter.

**Evidence:** `Slot.__enter__` opens each path with mode `"w"` before attempting `flock` (`oracle.py:109-120`), so opening follows/truncates a pre-planted symlink and flock protects the opened inode, not a replacement path. The observed slot directory is owned by the current user and mode `755`; other UIDs cannot write it, so this requires same-UID control. Cooperating counters do not unlink lock files, and their normal flock use is sound.

**Impact:** same-UID tampering can truncate a target file or replace a locked inode and exceed the intended 12-slot cap. This is a conditional local race, not an other-user boundary crossing.

**Smallest remediation:** open persistent slot files with `O_NOFOLLOW|O_CREAT|O_RDWR` (not truncating mode) and ensure lock paths cannot be replaced by an untrusted same-UID workload if that threat is in scope.

### LOW — pilot intentionally contacts the live compositor for read-only inventory

**Exploit path:** run `harness/pilot.py` in a desktop session. `live_instances()` invokes `hyprctl instances -j` without an explicit environment (`pilot.py:17-22`), before and after the oracle run (`pilot.py:43-44,76-77`), so it inherits the host's compositor-selection environment.

**Impact:** it reads live instance metadata only; the argv is a fixed `instances` read verb, with no dispatch/reload/keyword/kill path. This is allowed by the stated host-safety method, but it is an intentional live-session connection. The nested oracle path itself uses a minimal `hyprctl` environment and explicit private runtime directory (`oracle.py:128-131`), and its bwrap has `--unshare-all`, `--clearenv`, and a private `/run` (`oracle.py:147-160`).

**Smallest remediation:** none required for the allowed read-only pilot check; omit or isolate that probe only if the requirement changes to zero live-session contact.

## Coverage conclusions — severity NONE

- **Oracle live-session sockets/env:** no host `/run` or host runtime directory is bound into the oracle; `/run` is a tmpfs, and the environment is cleared before setting only harness variables (`oracle.py:147-160`). The host `hyprctl` helper receives only `PATH` and the private `XDG_RUNTIME_DIR` (`oracle.py:128-131`). Python subprocesses use the default closed-fd behavior apart from explicitly supplied standard streams; no host socket FD is passed through.
- **DRM card/input nodes:** oracle binds only `/dev/dri/renderD129`; `/dev` is otherwise private (`oracle.py:150-152`). `/sys/dev/char`, `/sys/devices`, and `/sys/class/drm` are read-only metadata mounts. No DRM card node or input device node is bound. The render node is a real host GPU capability, intentionally present; C1/C2 tool sandboxes bind no host device (`oracle.py:232-237`).
- **Normal process cleanup:** oracle cleanup sends TERM to its own process group, waits, escalates to KILL, and closes/removes the private runtime dir (`oracle.py:212-227`); the bwrap child also has `--die-with-parent`. The recorded successful pilot reports unchanged live-instance/coredump counts and zero nested processes/runtime dirs left (`harness/pilot-receipt.txt:10-19`). This historical receipt is not a substitute for rerunning the pilot.
- **Build script:** `build-tinywl.sh:7-16` writes/builds under the fixed `/fast/scratch/hyaku/mado-r26` path, verifies the expected wlroots commit before applying the local patch/build, and bounds clone/setup/ninja with timeouts. It does not start Hyprland or tinywl.

## Commands and observed facts

- `timeout 10 prlimit --as=4000000000 -- stat -c '%A %a %U:%G %n' /fast/scratch/hyaku/mado-r26 /fast/scratch/hyaku/mado-r26-oracle-slots /tmp /dev/dri/renderD129 /sys/class/drm /sys/dev/char /sys/devices` — `/fast/scratch/hyaku/mado-r26` and the slot directory were `drwxr-xr-x` (`755`, owned by `vgpnk:vgpnk`); `/tmp` was sticky `1777`; render node was `crw-rw-rw-`.
- `timeout 10 prlimit --as=4000000000 -- bash -c 'ulimit -c'` — `unlimited`.
- Read `/proc/sys/kernel/core_pattern` — `|/usr/lib/systemd/systemd-coredump ...`.

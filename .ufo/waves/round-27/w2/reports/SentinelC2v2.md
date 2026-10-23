# C2 v2 sandbox review

Scope: read-only review of `.ufo/waves/round-27/c2/count-v2.py`; one authorized counter run with a probe suite. No lane files were changed except this report. No held-out files were read outside the sandbox, and no write-escape test was attempted.

## Overall verdict

No path to the host lane or sealed held-out directory was demonstrated. The counter overlays `/home` and `/fast` with tmpfs, uses a read-only bind of `/`, and re-exposes only the per-run directory. The probe's attempts to list the held-out directory and open the lane counter both returned `ENOENT` (errno 2).

Two residual findings remain: writable suite runs have unbounded resource use, and `.git` leaks the source repository location plus a coarse clean-versus-modified signal.

## MEDIUM — suite can exhaust host resources

**Exploit path.** A malicious suite can emit large stdout/stderr streams: `run_suite()` uses `subprocess.run(..., capture_output=True)` (line 106), then concatenates and decodes the full streams and splits all lines before retaining only the last 120 characters (line 107). The 4 GB `RLIMIT_AS` is applied to the suite subprocess tree, not to the counter process collecting the output. With up to six workers and a 300-second suite timeout (lines 100-106, 164), the counter parent can accumulate unbounded output in host memory. The sandbox also creates uncapped tmpfs mounts (`/home`, `/fast`, `/run`, `/tmp`, line 101); bubblewrap confirms `--size BYTES` is available for tmpfs. In addition, `HOME` and `TMPDIR` point into the writable per-run bind at `d` (lines 92-99, 102-105), so suite-created scratch can consume host `/fast` space until cleanup.

**Impact.** Host memory or disk pressure / denial of service; this does not provide a route to write the lane or read held-out data.

**Smallest remediation.** Drain stdout/stderr with a fixed byte cap and terminate a suite that exceeds it; set explicit `--size` limits for tmpfs mounts and put `HOME`/`TMPDIR` on a capped mount (or quota the per-run writable directory). No output-flood or disk-fill was run.

## LOW — clone metadata leaks origin path and pristine-vs-edited state

**Exploit path.** The suite can read its clone's `.git/config` and inspect the worktree. The probe found `originLane` in the origin URL and `git status --porcelain` reported `dirty0` for the pristine A case and `dirty1` for both behavior-preserving edits and W-mutant edits. `--no-local` avoids the local-clone optimization, but does not remove the clone's origin URL. The signal distinguishes pristine from edited runs, not GREEN from W/H: benign edits and W cases both reported `dirty1`.

**Impact.** A suite can learn the original lane path from clone metadata and distinguish a pristine subject set from a changed one. The origin path did not make the host lane reachable: the direct lane-file open returned `ENOENT`, and `/home` is overlaid. The observed dirty bit alone cannot pass all green cases while rejecting mutants.

**Smallest remediation.** After checkout, remove or replace `remote.origin.url` in each throwaway clone (for example, `git config --unset remote.origin.url`). No counter class label was visible in the probe's argv or directory names; argv had the same `--c1`, `--c2`, and `--rev:2fdca5ca` fields in every A invocation, while run-directory components were random. `/proc/1/cmdline` identified `bwrap`; the counter uses `--unshare-all` and mounts a new `/proc`. Timing was not separately tested; the wrapper does not pass an explicit class or case identifier to the suite.

## Evidence and exact run

Counter source: `clone()` uses `git clone --no-local` at lines 69-77; the sandbox command at lines 100-105 uses `--ro-bind / /`, tmpfs overlays, a bind of only `d`, `--unshare-all`, `--die-with-parent`, `--new-session`, `--clearenv`, and explicit `PATH`, `HOME`, and `TMPDIR`. Per-run and outer scratch cleanup are in `finally` blocks at lines 109-110 and 236-244.

Probe: `/fast/scratch/hyaku/mado-r27/sent/probe-suite.py`, 2,344 bytes, SHA-256 `882ab457a6e38f480ac2f45d6bf527c04e0293510f65a06397fd00b740a74280`.

Command, started at 2026-10-23T08:39:42-03:00:

```text
cd /home/vgpnk/Projects/shokunin/mado-shokunin && env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count-v2.py 2fdca5ca --suite-a-file /fast/scratch/hyaku/mado-r27/sent/probe-suite.py --jobs 6
```

Observed counter output included `H=E2 L=E2`, `p1=bwrap`, `git=originLane/dirty0` on the pristine case and `git=originLane/dirty1` on edited cases. It also reported `SUITE B quality/population-suite.py MISSING at REV` and ended `green=5/8 ... w_killed=0/15 ... TARGET_MISSED`, `exit=1`; this run was a sandbox probe, not a complete C2 score. Runtime was 28.50 seconds.

Pre-run query `coredumpctl list --no-pager --no-legend --until=2026-10-23T08:39:42-03:00 COREDUMP_EXE=/usr/bin/Hyprland | wc -l` returned `1,338`. The post-run query `coredumpctl list --no-pager --no-legend --since=2026-10-23T08:39:42-03:00 COREDUMP_EXE=/usr/bin/Hyprland | wc -l` returned `0` (`No coredumps found`): delta `0`; the counter/probe did not start Hyprland.

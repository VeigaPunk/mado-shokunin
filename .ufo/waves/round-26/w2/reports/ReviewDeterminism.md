# w2 re-check — w1 OracleDeterminism

Seat `MadoR26.ReviewDeterminism` · 2026-10-23 · lane tip observed at write time `2b3487f7` (w1's report
pinned `05319e0f`; wave seats land concurrently). Re-ran a smaller version of w1's probe with the
harness imported by path, and re-verified the report's citations, pins and counts.

## Verdict

`ORACLE_READY stable` — re-check confirms w1. Plain_vs_delayed_equal=4/4 trees (deep JSON, both verbs),
BASE 4/4 runs equal with first-read==accepted in every run, first_read_moved=0/16 run-verb pairs,
first-read raw bytes identical between the early and the 3.0 s-delayed instance of every tree,
oracle_errors=0, hyprland_coredumps_delta=0. Structural gate re-verified at the pinned commit: the
early read cannot observe a value Hyprland would not hold after load, because instance discovery
(the lock file) postdates config application.

## What was run

Scratch probe `/fast/scratch/hyaku/mado-r26/data/ReviewDeterminism/probe.py`
(sha256 `0b5138ebb8e9fd27bef20d7fd75995671567accc9933c0b88c07c19637a11bbf`), independent of the
frozen counters (own trees, own comparison forms):

- Verifies the harness pin `680798ed…` before import, then imports `harness/oracle.py` by path and
  runs `check_build()` (tinywl + libwlroots pins).
- BASE = `oracle.snapshot($HOME)` → **79 files, digest `sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`** — byte-identical to w1's BASE, so both probes sampled the same snapshot.
- 4 trees, each answered by two separate nested instances: `plain` (harness timing; first read at
  discovery) and `delayed` (first read attempt of each verb sleeps 3.0 s, the same DELAY=3.0 design
  as w1's `probe-determinism/det.py:41`):
  - T1 BASE + append (new bezier + `animation = windows … probeB1, popin 15%` + `bind = SUPER, F13, workspace, r+1`) → binds 192→193.
  - T2 BASE + append (`animation = global, 0`, fade re-enable, another bind, whitespace/comment lines) → binds 193.
  - T3 BASE + new file `.config/hypr/probe-t3.conf` pulled in by an appended `source = probe-t3.conf` (2 beziers, 2 animations, 1 bind) → binds 193.
  - T4 independent tree: hyprland.conf replaced (variable, 3 beziers, 6 animations, 2 binds) → binds 2.
  - All four differ from BASE on deep JSON compare — the equality check is not vacuous.
- Tracing wraps the harness's `_hyprctl` at its I/O boundary; the first successful JSON read of each
  verb is captured and compared against that run's accepted value and across plain/delayed.
- Comparisons are deep JSON equality (order-sensitive, strictly stronger than the counters'
  set/multiset canonical forms) plus raw-byte sha of the first reads.

Command (from `/fast/scratch/hyaku/mado-r26/data/ReviewDeterminism`):

```
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 900 \
  prlimit --as=4000000000:8000000000 -- python3 -I probe.py
```

Wall 53.0 s, 12 nested-instance runs, exit 0. Receipt (26 lines):
`/fast/scratch/hyaku/mado-r26/data/ReviewDeterminism/oracle-determinism-recheck.txt`,
sha256 `0f7cfe7625c93c92b8a57f0f5b86c7e3d122c439837694d10ad83c3167508218`. Final lines verbatim:

```
aggregate: plain_vs_delayed_equal=4/4 trees; BASE_equal=3/3 later runs vs BASE#01; first_read_moved=0/16 run-verb pairs; oracle_errors=0; hyprland_coredumps_before=1337 after=1337 delta=0
ORACLE_READY stable — plain_vs_delayed_equal=4/4 trees; BASE 4 runs; first_read_moved=0/16; oracle_errors=0; hyprland_coredumps_delta=0
```

Timing detail matching w1's: plain first reads at 0.00 s (animations) / 0.91 s (binds) after
discovery; delayed at 3.00 s / 6.91 s; acceptance in every run was the harness's own
three-identical-reads rule, and the first read already equaled it everywhere.

## Can the early read see a pre-load value? (mechanism re-verified)

Fetched the pinned sources fresh from `raw.githubusercontent.com` at commit
`efb50993780079460b0cbed1363e2166a2de1d9f` (the same pin the counters' ORACLE_VERSION guard checks,
and the commit the nested instance itself printed in this probe's `sandbox.log`); hashes identical to
w1's: `Compositor.cpp` 38550 B `74833ecb…`, `hyprctl-main.cpp` 17168 B `f6b0d1fc…`.

- `hyprctl instances -j` lists a directory only if `<dir>/hyprland.lock` opens
  (`hyprctl-main.cpp:100-107`, used at `:153`); verb reads go through `<runtime>/<sig>/.socket.sock`
  (`:230`). So discovery == lock visibility.
- Normal startup: `initServer` → `initManagers(STAGE_PRIORITY)` (`Compositor.cpp:296`) →
  `Config::initConfigManager()` (`:665`) → `Config::mgr()->init()` (`:683`, the initial parse that
  builds the animation and bind tables) → … → `createLockFile()` (`:812`) → `enterLoop()` (`:823`).
  Lock visibility therefore postdates config application — w1's gate, confirmed at exact lines.
- Precision note (supports, does not contradict, w1): the *other* `initConfigManager`/`mgr()->init()`
  pair at `Compositor.cpp:273-275` is the `m_onlyConfigVerification` branch in `initServer`
  (`hyprland --verify` path), not the runtime path w1 cited.
- Post-lock drift: `:812`→`:823` contains only the ready emit and a watchdog write; exec-once runs
  after lock, and the harness strips exec lines anyway (`strip_exec`) before start; a config reload
  would need an external write, which never happens inside the read window. Nothing between lock and
  loop can change the tables the two verbs read.
- Empirically: every plain run's first read (0.00–0.01 s after discovery) already equaled the
  accepted value *and* the delayed instance's bytes — including the four trees whose tables the probe
  had deliberately changed. No pre-load state was ever observable.

## w1 report cross-check

- Verdict line, aggregate counts (`48/48`, `44/44`, `0/96`, `reads_to_acceptance={"3": 48}`,
  addendum `6/6`, `11/11`, `0/12`) and the file facts (144 lines / 13690 B,
  `sha256:5b9e4189…`) all match `.ufo/waves/round-26/evidence/oracle-determinism.txt`, re-verified.
- Pins re-verified in the lane: `harness/oracle.py` `680798ed…`, `c1/count.py` `f98e264b…`,
  `c2/count.py` `b92c32da…`. w1's scratch artifacts listed in the report exist
  (`det.py`, `addendum.py`, `run2-4.log`, fetched sources).
- The "~0.9 s binds offset" reproduced exactly (binds first_dt=0.91 s in all plain runs).
- No defects found in w1's report.

## Residual risk and verification gaps

- Finite sampling: 12 nested instances here (w1: 117) over one snapshot and four hand-built trees;
  zero differences plus the structural gate is the basis for the verdict, not a proof over all
  configs.
- This re-check's earliest binds read was 0.91 s post-discovery (both verbs requested together). The
  counters' C2 binds-only first read at discovery (0 s) is covered by w1's binds-only addendum
  (6/6 trees, 0/12 moved) and by the structural gate; it was not re-sampled here.
- The gate validates ordering, not parse fidelity: a *consistently* wrong oracle value would be
  invisible to every timing comparison — that class is the counters' cases_pass job, out of scope
  here.

## Host safety and hygiene

Every instance ran only through `harness/oracle.py` (bwrap `--unshare-all --clearenv`, private
`XDG_RUNTIME_DIR`, tinywl headless, pinned binaries, render node only); probe run with
`WAYLAND_DISPLAY`/`HYPRLAND_INSTANCE_SIGNATURE` unset, `timeout 900`, `prlimit
--as=4000000000:8000000000`; all sandboxes torn down by the harness's process-group kill (clean
exit). Coredumps 1337→1337 (delta 0; the count is +2 vs w1's 1335 from host-wide activity between
waves, not this probe). No pacman transactions, no tool installs or upgrades (none needed). Lane
writes: this report only. No git/jj write commands anywhere.

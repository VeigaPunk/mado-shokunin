# Oracle readiness and determinism — mado round 26 w1

Seat `MadoR26.OracleDeterminism` · lane tip `05319e0fed2ce25cf0a883380af2763a85fd4936` · 2026-10-23.

Assigned probe: does `harness/oracle.py` answer with the same value whether it reads as soon as the
nested instance appears (the counters' behaviour) or after a 3 s wait, and do ten independent BASE
runs agree? A premature read would silently write wrong expected values into both frozen counters.

## Verdict

`ORACLE_READY stable` — plain_vs_delayed_equal=48/48 tree-verb comparisons (24 trees over 2 seeds);
base_equal=11/11 runs per seed (10 plain + 1 delayed, both verbs, vs BASE#01) and 44/44 BASE answers
across both seeds; first_read_moved=0/96 run-verb pairs; reads_to_acceptance=3 in 96/96; binds-only
addendum 6/6 trees and 11/11 BASE runs, first_read_moved=0/12; oracle_errors=0 of 117 nested-instance
runs; hyprland_coredumps_delta=0. No difference of any kind was observed, so the 10 BASE runs and the
12-tree plain-vs-delayed comparison found no premature-read hazard.

## Method and exact commands

Two scratch programs (not lane artifacts), both importing the pinned harness and the frozen case
builders **by path**:

- `/fast/scratch/hyaku/mado-r26/probe-determinism/det.py` — main probe. Loads `harness/oracle.py`,
  `c1/count.py` and `c2/count.py`, verifying the three sha256 pins (`680798ed…`, `f98e264b…`,
  `b92c32da…`) before use; snapshots `$HOME` through `oracle.snapshot()`, the same procedure the
  counters use (79 files, digest
  `sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`, printed in the receipt). Per seed it builds 12 generated trees — 6 through `c1/count.py`'s
  `apply_op`/`OPS`/`EFFECTIVE` (2–4 ops, the counter's own sampling rule) and 6 through
  `c2/count.py`'s `arith_case` over `V3.sourced_files` — and answers each tree with three separate
  nested-instance runs of `oracle.oracle(home, work, ["animations", "binds"])`:
  `plain` (harness unchanged), `traced` (same timing; every `_hyprctl(xdg, ["-i", sig, verb, "-j"])`
  call recorded at the I/O boundary with rc, byte length, sha prefix, timestamp), and `delayed`
  (same, but the first read attempt of each verb sleeps 3.0 s). Acceptance inside every run is the
  harness rule itself: three byte-identical raw reads 0.3 s apart. Comparisons use the counters'
  canonical forms exactly: C1 `node_set`/`bez_set`, C2 `V3.FIELDS` 18-field bind multiset.
  Each seed also runs BASE 10 times with the plain oracle plus one delayed BASE (11 runs × 2 verbs).
  Two independent seeds per execution.
- `/fast/scratch/hyaku/mado-r26/probe-determinism/addendum.py` — binds-only repeat, because the main
  probe asks for `animations` first, which puts a binds read about 0.9 s after instance discovery;
  C2's counter asks for `binds -j` alone. 6 fresh `arith_case` trees and 10 plain + 1 delayed BASE
  runs, all binds-only, appended to the same evidence file.

Commands (the outer limit is soft 4 GB / hard 8 GB per the L1 note, so the harness's own
`prlimit --as=8000000000` inside the sandbox can raise the soft limit):

```
cd /fast/scratch/hyaku/mado-r26 && env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE \
  timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I probe-determinism/det.py
cd /fast/scratch/hyaku/mado-r26 && env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE \
  timeout 600 prlimit --as=4000000000:8000000000 -- python3 -I probe-determinism/addendum.py
```

Evidence: `.ufo/waves/round-26/evidence/oracle-determinism.txt`, 144 lines / 13690 bytes,
`sha256:5b9e4189390f073929c81d2268e5adc3256b3cde8eb1fb8bc27c6d6e0b3741f7` (main block seed
`6dedf12e62b907b0` + `35e62f3811a39022`, utc 2026-10-23T08:59:52Z; addendum seed `62a5aca0bb51dfcd`
appended by the second command). Scratch copies of the JSON summaries:
`probe-determinism/summary.json`, `probe-determinism/addendum.json`; stdout logs `run2.log`,
`run3.log`, `run4.log`, `addendum-run.log`. An earlier single-seed execution (`run2.log`, 70.4 s) and
an earlier two-seed execution (`run3.log`, 117.6 s, one cosmetic denominator fixed — it printed
`base_equal=12/11` because the delayed BASE was counted per verb) were also fully equal; the receipt
above is the final clean execution.

## Results, with counts

Main probe, 2 seeds × (12 trees × 3 runs + 11 BASE runs) = 94 nested-instance runs, all answered:

- Tree answers: 48/48 tree-verb comparisons equal across plain, traced and delayed runs (24 trees ×
  2 verbs). Node/bezier counts seen: 41–43 animations entries, 192–195 binds; every tree with its own
  generated ops/arith descriptors printed in the receipt. `plain != delayed` and `plain != traced`
  occurred 0 times; list order also identical.
- First read vs accepted: 0/96 run-verb pairs moved. Every traced and every delayed run needed
  exactly 3 reads to acceptance (`reads_to_acceptance={"3": 48}` per seed), i.e. no failed read and no
  jitter even at the first attempt; traced first attempts landed 0.00–0.01 s after each verb's read
  phase began (animations begins at instance discovery; binds begins after animations' acceptance,
  ≈0.9 s later), delayed first attempts at 3.00–3.01 s after that same point.
- BASE: 11/11 runs per seed equal to BASE#01 on both verbs (10 plain + 1 delayed; node/bezier sets,
  18-field bind multiset, and list order); cross-seed, 44/44 BASE answers (2 seeds × 11 runs ×
  2 verbs) equal to seed-1 BASE#01. So the counters' own guard (two BASE oracle runs compared) was
  never near a disagreement in 22 BASE instances of the main probe.
- Errors: 0.

Binds-only addendum, 23 nested-instance runs: 6/6 arith trees plain-vs-delayed equal; first read vs
accepted moved 0/12; BASE 11/11 equal (10 plain + 1 delayed); the delayed BASE's first read also
equals its accepted value. Wall 26.7 s.

## Why the first read is already final (source, same pin as the harness)

Fetched with `curl` from `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/…`
into scratch (`probe-determinism/`):

- `src/Compositor.cpp` — 38550 B, `sha256:74833ecbf0e2b6f8ad84345ac0716a3295a0e347420a188be0ab4f6a684af7c0`.
  Instance dir under `XDG_RUNTIME_DIR/hypr` at line 192; `initManagers(STAGE_PRIORITY)` at line 296
  runs `Config::initConfigManager()` (665) and `Config::mgr()->init()` (683); `createLockFile()` is
  called at line 812, at the end of `startCompositor`, immediately before `enterLoop()`.
- `hyprctl/src/main.cpp` — 17168 B, `sha256:f6b0d1fcfc6695194c70964250591a35ffe90274309303d8f5fd0ac6f8c1c93f`.
  `instances()` only parses `$XDG_RUNTIME_DIR/hypr/<sig>/hyprland.lock` (line 104); IPC reads connect
  to `<runtime>/<sig>/.socket.sock` (line 230).
- `src/managers/EventManager.cpp` — 6479 B (socket2 path, checked only).
- `src/config/ConfigManager.cpp` — 2597 B (manager construction, checked only).

Reading them together: the harness can only see an instance once `hyprland.lock` exists, and that file
is written after the config (animation table and binds) has been parsed and applied. So "as soon as the
instance appears" is already "after config application" — which is what the measurements show, with
the 3-identical-read rule as a second layer that never had to absorb a change.

## Limits and risks

- Sampling is finite: 117 nested-instance runs over three tree seeds, both verbs, one snapshot
  (79 files) and the counters' own generators. Zero differences is evidence, not a proof for every
  possible config; the structural gate above is what makes the result expected rather than lucky.
- The gate guarantees the *table* is built before discovery; it does not validate that Hyprland's
  parse is what the counters assume. A consistently wrong oracle value (e.g. a config line ignored
  by both Hyprland runs) would be invisible to every comparison here — that class is the counters'
  job, not readiness.
- The main probe requested both verbs in one instance, so its binds reads are ~0.9 s after discovery;
  the binds-only addendum removes that offset (plain reads at discovery, all equal). C1's animations
  reads are the first verb already.
- The counters' BASE-of-two guard is a weak instability guard by design; in 33 BASE instances (22
  main-probe runs + 11 binds-only addendum runs) it never had grounds to fire, and 44/44 cross-seed
  BASE answers were byte-order identical on both verbs.
- No counter or harness byte was edited; the probe verified all three pins at load. No lane git/jj
  write was made.

## Host safety

Every instance ran only through `harness/oracle.py` (bwrap `--unshare-all --clearenv`, private
`XDG_RUNTIME_DIR` under /tmp, tinywl headless parent, only `/dev/dri/renderD129`); the probe ran with
`WAYLAND_DISPLAY` and `HYPRLAND_INSTANCE_SIGNATURE` unset (`env -u`), and `_hyprctl` passes only
`PATH` and the private `XDG_RUNTIME_DIR`. Host Hyprland coredumps: 1335 before, 1335 after both
commands (delta 0). All sandboxes exited via the harness's process-group kill; no probe process
remained (the bwrap processes visible afterwards belong to another seat's counter run, not this one).

## Files written

- Lane: `.ufo/waves/round-26/evidence/oracle-determinism.txt` (the receipt above) and this report.
- Scratch only: `/fast/scratch/hyaku/mado-r26/probe-determinism/{det.py, addendum.py, summary.json,
  addendum.json, run2.log, run3.log, run4.log, addendum-run.log, Compositor.cpp, hyprctl-main.cpp,
  EventManager.cpp, ConfigManager.cpp}`.

No tool installs or upgrades were made (nothing was needed). No blockers.

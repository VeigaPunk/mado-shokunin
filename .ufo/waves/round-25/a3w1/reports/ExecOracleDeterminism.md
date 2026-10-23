# ExecOracleDeterminism — C1 counter v4's Hyprland oracle: determinism, ORACLE_EXTRA effect, timing

## Verdict

ORACLE determinism: 41/41 identical; extra-lines effect: none

The frozen v4 oracle is deterministic over the 18-field multiset on every one of the 41 case trees
(two independent nested instances per tree), and the `ORACLE_EXTRA` block (6 list entries) changes no
bind on any tree tested. No counter change is indicated by this probe.

## What was measured

Counter under test: `.ufo/waves/round-25/c1/count.py`, sha256
`323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2` (checked at import against the
registration pin; generator `count-v3.py` hash-checked by the counter's own `load_v3`). Imported
read-only with `importlib.util.spec_from_file_location` and `sys.dont_write_bytecode = True` (the
setting was verified in isolation: without it the same import creates `__pycache__`, with it no
bytecode is written). `count.py` and `count-v3.py` mtimes are unchanged (03:47:11 and 03:46:22). The
lane's `c1/__pycache__/count.cpython-314.pyc` was rewritten at 04:23:49 by a peer seat's counter run
(my probes ended at 04:22 and wrote no bytecode).

- **Case construction is v4's own loop**, copied line for line from `count.py:main`: one live capture
  pair (stable), `copy_roots` snapshot, `rng = random.Random(int(seed, 16))`, `v3.Gen(rng, live)`,
  then `BASE` followed by `TYPES × PER_TYPE` in generator order (`ADD, UNBIND, VARIABLE, SOURCE,
  GLOB, UNSOURCED, COMMENT, SYNTH, REWRITE, HARD`), each tree a fresh `copytree` of the snapshot with
  `v3.perturb` applied in that same order — seed `0123456789abcdef`, the registration's before-receipt
  seed.
- **`oracle()` was called as frozen.** The only instrumentation was a `Slot` subclass (`TimedSlot`)
  rebinding the module global, which calls `super().__enter__()` and therefore takes the same
  `flock` on the same `slot-N.lock` files; host-wide 6-instance cap preserved. `jobs=4` (the counter's
  default) for phase A, 2 for phase B.
- **Instance budget:** 82 phase-A instances (41 trees × 2), 16 phase-B instances (8 trees × 2 arms),
  3 probe-2 instances (BASE × 2 + BASE without `ORACLE_EXTRA`) = 101 nested Hyprland instances, all
  killed by the oracle's own `killpg` path; my post-run sweep found 0 instances pointing at my work
  trees.
- **Exec safety:** I never started an instance on a tree containing exec lines. The 8 generated trees
  were checked exec-free before their variant runs (0 matches in all 8); the snapshot-derived trees
  go through the counter's unmodified `strip_exec` on its private copy (the live snapshot itself
  contains 13 exec lines in 2 autostart files, measured independently).

Probe working tree: `/fast/scratch/hyaku/mado-r25a3/oracle/` (harmless, deleted `work/` and `work2/`
before exit). Live captures were read with `hyprctl binds -j` / `hyprctl instances -j` only.

## (a) Determinism — 41/41 identical

Two independent `oracle()` calls per tree, compared with the counter's own `v3.compare` (Counter over
`v3.key_of`, i.e. the multiset over the 18 `hyprctl` fields). Verbatim from `probe.log`:

```text
PHASE_A two independent oracle() calls per tree (multiset over 18 fields)
A BASE       SAME  missing=0 extra=0 binds1=192 binds2=192 (unperturbed)
A ADD-0      SAME  missing=0 extra=0 binds1=193 binds2=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
A ADD-1      SAME  missing=0 extra=0 binds1=193 binds2=193 (ADD into .config/hypr/bindings.conf)
A ADD-2      SAME  missing=0 extra=0 binds1=193 binds2=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
A ADD-3      SAME  missing=0 extra=0 binds1=193 binds2=193 (ADD into .config/hypr/bindings.conf)
A UNBIND-0   SAME  missing=0 extra=0 binds1=191 binds2=191 (UNBIND mask=73 key='' keycode=15)
A UNBIND-1   SAME  missing=0 extra=0 binds1=191 binds2=191 (UNBIND mask=64 key='SPACE' keycode=0)
A UNBIND-2   SAME  missing=0 extra=0 binds1=191 binds2=191 (UNBIND mask=0 key='XF86AudioRaiseVolume' keycode=0)
A UNBIND-3   SAME  missing=0 extra=0 binds1=191 binds2=191 (UNBIND mask=68 key='SPACE' keycode=0)
A VARIABLE-0 SAME  missing=0 extra=0 binds1=193 binds2=193 (VARIABLE $vledftnu)
A VARIABLE-1 SAME  missing=0 extra=0 binds1=193 binds2=193 (VARIABLE $vszioqps)
A VARIABLE-2 SAME  missing=0 extra=0 binds1=193 binds2=193 (VARIABLE $vzcvhoju)
A VARIABLE-3 SAME  missing=0 extra=0 binds1=193 binds2=193 (VARIABLE $vtumkhdv)
A SOURCE-0   SAME  missing=0 extra=0 binds1=194 binds2=194 (SOURCE new file at root line 19)
A SOURCE-1   SAME  missing=0 extra=0 binds1=194 binds2=194 (SOURCE new file at root line 19)
A SOURCE-2   SAME  missing=0 extra=0 binds1=194 binds2=194 (SOURCE new file at root line 29)
A SOURCE-3   SAME  missing=0 extra=0 binds1=194 binds2=194 (SOURCE new file at root line 4)
A GLOB-0     SAME  missing=0 extra=0 binds1=193 binds2=193 (GLOB new toggles file)
A GLOB-1     SAME  missing=0 extra=0 binds1=193 binds2=193 (GLOB new toggles file)
A GLOB-2     SAME  missing=0 extra=0 binds1=193 binds2=193 (GLOB new toggles file)
A GLOB-3     SAME  missing=0 extra=0 binds1=193 binds2=193 (GLOB new toggles file)
A UNSOURCED-0 SAME  missing=0 extra=0 binds1=192 binds2=192 (UNSOURCED new bindings file)
A UNSOURCED-1 SAME  missing=0 extra=0 binds1=192 binds2=192 (UNSOURCED new bindings file)
A UNSOURCED-2 SAME  missing=0 extra=0 binds1=192 binds2=192 (UNSOURCED new bindings file)
A UNSOURCED-3 SAME  missing=0 extra=0 binds1=192 binds2=192 (UNSOURCED new bindings file)
A COMMENT-0  SAME  missing=0 extra=0 binds1=193 binds2=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
A COMMENT-1  SAME  missing=0 extra=0 binds1=193 binds2=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
A COMMENT-2  SAME  missing=0 extra=0 binds1=193 binds2=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf)
A COMMENT-3  SAME  missing=0 extra=0 binds1=193 binds2=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
A SYNTH-0    SAME  missing=0 extra=0 binds1=13 binds2=13 (SYNTH tree binds=13 unbound=1 vars=2)
A SYNTH-1    SAME  missing=0 extra=0 binds1=12 binds2=12 (SYNTH tree binds=12 unbound=1 vars=2)
A SYNTH-2    SAME  missing=0 extra=0 binds1=15 binds2=15 (SYNTH tree binds=15 unbound=1 vars=2)
A SYNTH-3    SAME  missing=0 extra=0 binds1=14 binds2=14 (SYNTH tree binds=14 unbound=1 vars=2)
A REWRITE-0  SAME  missing=0 extra=0 binds1=192 binds2=192 (REWRITE argswap mask=72 key='S' code=0; unbind mask=72 key='' code=61; add exec)
A REWRITE-1  SAME  missing=0 extra=0 binds1=192 binds2=192 (REWRITE argswap mask=65 key='C' code=0; unbind mask=65 key='E' code=0; add movetoworkspace)
A REWRITE-2  SAME  missing=0 extra=0 binds1=192 binds2=192 (REWRITE argswap mask=65 key='UP' code=0; unbind mask=64 key='S' code=0; add exec)
A REWRITE-3  SAME  missing=0 extra=0 binds1=192 binds2=192 (REWRITE argswap mask=65 key='M' code=0; unbind mask=0 key='XF86TouchpadToggle' code=0; add cyclenext)
A HARD-0     SAME  missing=0 extra=0 binds1=20 binds2=20 (HARD tree lines=33 binds=20 unbinds=1 vars=4)
A HARD-1     SAME  missing=0 extra=0 binds1=21 binds2=21 (HARD tree lines=31 binds=21 unbinds=3 vars=4)
A HARD-2     SAME  missing=0 extra=0 binds1=18 binds2=18 (HARD tree lines=28 binds=18 unbinds=1 vars=4)
A HARD-3     SAME  missing=0 extra=0 binds1=22 binds2=22 (HARD tree lines=30 binds=22 unbinds=3 vars=4)
```

`identical = 41`, `differing = []`, no `ORACLE_FAIL`. The per-tree cardinalities differ exactly as
each perturbation dictates (191/192/193/194, and 12–22 for SYNTH/HARD), so both calls are reading the
tree's own table and not the live one.

Two independent cross-checks that the case trees themselves are v4's:

1. Probe-2 BASE: `BASE_DETERMINISM oracle_vs_oracle missing=0 extra=0 order_identical=True` — the two
   tables are equal element-by-element in `hyprctl` order, not just as a multiset.
2. My rebuild reproduces the committed before receipt (`evidence/c1-before-v4-41cc04c8.txt`) exactly
   in its identifying data: live capture sha256 `9a47199e…c779` (192 binds), snapshot `files=79
   digest sha256:fe1b2d8b…3727`, every one of the 41 case descriptions byte-for-byte (including
   `VARIABLE $vledftnu` … `$vtumkhdv`, the SOURCE root line numbers, the REWRITE mask/key tuples and
   the HARD line/bind/unbind/var counts), and the oracle cardinalities implied by that receipt's
   `V3_MODEL_AGREE 41/41`.

## (b) `ORACLE_EXTRA` effect — none

The variant is `count.py`'s own source with exactly the append removed
(`VARIANT_PATCH sites=1 removed_bytes=19 no_extra_lines=1`); the patched source was written inside
the probe's temporary work tree and removed with it (see Artifact paths). The 8 generated trees were
verified exec-free first:
`EXEC_FREE generated_trees=8 exec_lines=SYNTH-0:0,SYNTH-1:0,SYNTH-2:0,SYNTH-3:0,HARD-0:0,HARD-1:0,HARD-2:0,HARD-3:0`.

```text
PHASE_B ORACLE_EXTRA effect (same tree, with vs without the appended ecosystem block)
B SYNTH-0  effect=none  binds_with=13 binds_no=13 missing=0 extra=0 (SYNTH tree binds=13 unbound=1 vars=2)
B SYNTH-1  effect=none  binds_with=12 binds_no=12 missing=0 extra=0 (SYNTH tree binds=12 unbound=1 vars=2)
B SYNTH-2  effect=none  binds_with=15 binds_no=15 missing=0 extra=0 (SYNTH tree binds=15 unbound=1 vars=2)
B SYNTH-3  effect=none  binds_with=14 binds_no=14 missing=0 extra=0 (SYNTH tree binds=14 unbound=1 vars=2)
B HARD-0   effect=none  binds_with=20 binds_no=20 missing=0 extra=0 (HARD tree lines=33 binds=20 unbinds=1 vars=4)
B HARD-1   effect=none  binds_with=21 binds_no=21 missing=0 extra=0 (HARD tree lines=31 binds=21 unbinds=3 vars=4)
B HARD-2   effect=none  binds_with=18 binds_no=18 missing=0 extra=0 (HARD tree lines=28 binds=18 unbinds=1 vars=4)
B HARD-3   effect=none  binds_with=22 binds_no=22 missing=0 extra=0 (HARD tree lines=30 binds=22 unbinds=3 vars=4)
```

Beyond the required 8, probe 2 ran the real 79-file snapshot both ways:
`BASE_EXTRA_EFFECT missing=0 extra=0` (192 binds each). The appended text is `"\n".join(ORACLE_EXTRA)`
for `ORACLE_EXTRA = ["", "ecosystem {", "    no_update_news = true", "    no_donation_nag = true", "}", ""]`,
written after the root config; it sits at top level and adds no bind, as measured.

## (c) Timing per instance

From 98 timed `oracle()` calls (82 phase A + 16 phase B), plus 3 BASE calls in probe 2:

```text
TIMING wall_per_oracle_call_s  n=98 min=0.94 med=1.14 max=9.29 mean=1.89
TIMING slot_queue_wait_s       n=98 min=0.00 med=0.00 max=8.01 mean=0.66
TIMING instance_s_excl_queue   n=98 min=0.94 med=1.10 max=2.21 mean=1.23
TIMING phaseA_wall_s=40.3 phaseB_wall_s=18.8 total_wall_s=59.1
TIMING base_instance_s_excl_queue: run1=1.08 run2=1.04 noextra=1.05
```

**One nested instance costs 0.94–2.21 s of instance time**, excluding shared-slot queue wait (median
1.10 s, mean 1.23 s over 98 calls at `jobs=4`/`jobs=2`), including the oracle's settle rule (two
byte-identical `binds -j` reads 0.3 s apart). Queue wait came from peer counters holding the shared
slot locks (up to 8.0 s), not from instance startup; a full 41-case counter run is therefore roughly
41 × 1.2 s ÷ jobs plus contention and the tool runs, consistent with the registration's 15–90 s
estimate. No call failed.

## Faithfulness observations (static + measured)

- Private HOME: `oracle()` copies the tree and runs nested Hyprland with
  `env = {PATH=/usr/bin, HOME=<copy>, XDG_RUNTIME_DIR=<parent rt>, WAYLAND_DISPLAY=<parent wl>}`.
  `HYPRLAND_INSTANCE_SIGNATURE` is **not** passed, so the nested instance cannot inherit the live bind
  table; `WAYLAND_DISPLAY` is passed only so the nested window can exist.
- Instance identity is exact: the signature is taken from `hyprctl instances -j` entries whose `pid`
  equals the spawned Hyprland pid, then all reads use `hyprctl -i <sig> binds -j`.
- Hermeticity: the snapshot contains 59 `source =` lines (40 distinct values), all `~`-relative,
  none absolute, none using `$` variables; 2 of them are one glob value,
  `~/.local/state/omarchy/toggles/hypr/*.conf`, which is how the GLOB cases enter Hyprland's table.
  All generated `source` lines (`SOURCE`, `SYNTH`, `HARD`) are `~/.config/hypr/…`. With `HOME`
  pointed at the private copy, no case tree can read the operator's live files.
- Exec removal: 13 exec lines live in 2 autostart files of the real roots; the counter's `strip_exec`
  deletes them from its copy before start (I did not alter that path or start an instance on an
  uncleaned tree).
- Kill path: `killpg(SIGTERM)` → `p.wait(8)` → `killpg(SIGKILL)`; runtime dir
  `$XDG_RUNTIME_DIR/hypr/<sig>` removed. My sweep after 101 instances: 0 leftovers.
- Live-vs-oracle guard holds: `BASE_ORACLE_VS_LIVE missing=0 extra=0` (my own measurement, 192 binds;
  every live entry has exactly the 18 field names and one key set).
- Field-shape check on the live table: `entries 192 keys_per_entry [18] key_set_size 1`.

## Counter concerns raised by this probe

One, environmental rather than a rule defect: `live_capture()` passes no `env`, so the counter process
must inherit `HYPRLAND_INSTANCE_SIGNATURE`. Measured matrix with `env -i PATH=/usr/bin` plus one var:
signature alone → exit 0; `XDG_RUNTIME_DIR=/run/user/1000` alone → exit 1; `WAYLAND_DISPLAY=wayland-1`
alone → exit 1; runtime-dir + display without signature → exit 1. A peer seat (`K4GrepAll`) hit exactly
this as `SETUP_ERROR hyprctl binds -j exit 1`; it is a harness-environment miss, not evidence of an
unstable oracle, and the counter's exit-2 path is the correct response. No reason to change the
counter: the oracle itself never depends on the inherited live signature.

No observed nondeterminism, no `ORACLE_FAIL`, no `ORACLE_DRIFT`, no `UNSTABLE` in any of my runs.

## Residual risks (what this probe does not establish)

1. Determinism is sampled at one seed, one snapshot, one host and one time window; 41/41 is strong but
   not a proof over all seeds. The scored predicate is the multiset, and BASE also matched in order.
2. The oracle proves Hyprland agrees with itself; it does not validate that a case *perturbation*
   means what its description says (case-design fairness is out of scope here).
3. `strip_exec` rewrites every decodable text file in the copy, not only sourced files. One directive
   per line means this cannot change a bind, but it is broader than "sourced files".
4. `ORACLE_EXTRA` is appended to a root config that could in principle end inside an open block.
   Measured none on BASE and all 8 generated trees; the 32 snapshot-derived trees keep BASE's closed
   tail (their edits insert complete lines), so the same argument carries, untested per tree.
5. Timing was taken while peer counters held the same 6 slot locks; instance times above exclude
   queue wait, and the wall figure with queue can be larger under contention.

## Commands and provenance

Counter and generator hashes verified before use:

```sh
sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/c1/count.py \
          /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/c1/count-v3.py
# 323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2  count.py
# 8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375  count-v3.py
```

Phase A+B (82 + 16 instances, 59.1 s):

```sh
cd /fast/scratch/hyaku/mado-r25a3/oracle && prlimit --as=4000000000 -- python3 -I -u determinism.py \
  > /fast/scratch/hyaku/mado-r25a3/oracle/probe.log 2>&1; echo "probe_exit=$?"
# probe_exit=0
```

BASE faithfulness + extra effect on the real snapshot (3 instances, 3.3 s):

```sh
cd /fast/scratch/hyaku/mado-r25a3/oracle && prlimit --as=4000000000 -- timeout 600 python3 -I -u probe2.py \
  2>&1 | tee probe2.log; echo "probe2_exit=${PIPESTATUS[0]}"
# probe2_exit=0
```

Probe-2 key lines:

```text
live sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779 binds=192 snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 stable=True
SOURCE_PATH_SCAN absolute_or_tilde_sources=59 ['.config/hypr/hyprland.conf:4: source = ~/.local/share/omarchy/default/hypr/autostart.conf', ...]
base-run1     binds=192 elapsed=1.08s slot_wait=0.00s
base-run2     binds=192 elapsed=1.04s slot_wait=0.00s
base-noextra  binds=192 elapsed=1.05s slot_wait=0.00s
BASE_DETERMINISM oracle_vs_oracle missing=0 extra=0 order_identical=True
BASE_ORACLE_VS_LIVE missing=0 extra=0
BASE_EXTRA_EFFECT missing=0 extra=0
TIMING base_instance_s_excl_queue: run1=1.08 run2=1.04 noextra=1.05
SWEEP orphans=0
```

(Two ad-hoc source scans in this seat were discarded before use: the first had relative roots and
printed zeros, the second binned every `~` value before testing for `*`. The figures above come from
the in-probe scan and a final classifier that tests absolute / `$` / `*` independently: 59 source
lines, 59 `~`-prefixed, 0 absolute, 0 with `$`, 2 lines sharing the one glob value.)

## Artifact paths

- Report: `.ufo/waves/round-25/a3w1/reports/ExecOracleDeterminism.md`
- Harness: `/fast/scratch/hyaku/mado-r25a3/oracle/determinism.py`,
  `/fast/scratch/hyaku/mado-r25a3/oracle/probe2.py`
- Receipts: `/fast/scratch/hyaku/mado-r25a3/oracle/probe.log` (full 41-case table, phase B, timing),
  `/fast/scratch/hyaku/mado-r25a3/oracle/probe2.log`. The no-extra variant source was written inside
  the probe's temporary work tree (`<work>/count-noextra.py`) and removed with it; it is one exact
  substitution on `count.py` (replace the two-line `ORACLE_EXTRA` append with `pass`, 19 bytes
  removed, site count 1) recorded in `determinism.py:load_noextra`.

## Touched surfaces

Wrote only this report in the lane and the probe files/logs under
`/fast/scratch/hyaku/mado-r25a3/oracle/`. No edit to `count.py`, `count-v3.py`, any control, the
tool, `corpus/`, SCORECARD, LOG, or evidence; no git/jj command; no package install; only `hyprctl`
read verbs on the live compositor and on my own nested instances. This seat wrote no bytecode into
the lane (`dont_write_bytecode` set and verified); the `c1/__pycache__` refresh noted above is a
peer's.

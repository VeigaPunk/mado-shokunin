# RescoreK1LabelKeyed — C1 counter v2

RESCORE K1LabelKeyed not met (best 3/41)

## Scope and axes

Axes: metadata-only shape fidelity, fresh-seed coverage, replay strength, host safety, exact restoration.

Re-scored the unchanged committed control twice, then scored one strengthened scratch copy once. All three measurements used frozen C1 counter v2 at revision `1b0b91e9889cbf984b052f5de564db78330a72aa`. No seed argument was supplied: the counter generated three distinct fresh seeds. No exit-2 guard or retry occurred.

The earlier L1 v2 receipt (`controls/v2/K1LabelKeyed.txt`) scored 2/41 with seed `8e0f31fb1a7e402f`; these new seeds are different. Different counts are not evidence of an implementation change.

Scratch root: `/fast/scratch/hyaku/mado-r26/rescore/RescoreK1LabelKeyed`.

## Re-score receipts: actual PRED lines and exits

| Run | Tool | Fresh seed | Passing cases | Counter/process exit |
| --- | --- | --- | --- | --- |
| Unchanged 1 | Committed `K1LabelKeyed.py` | `e852c87c4049766b` | BASE only | 1 / 1 |
| Unchanged 2 | Same committed bytes | `369ab3df8e7bce05` | BASE, C03, C26 | 1 / 1 |
| Strengthened | Scratch file below | `e9306f6075202d64` | BASE, C08 | 1 / 1 |

Unchanged run 1:

```text
PRED-C1-r26-v2 cases_pass=1/41 verdict=TARGET_MISSED
exit=1
```

Unchanged run 2:

```text
PRED-C1-r26-v2 cases_pass=3/41 verdict=TARGET_MISSED
exit=1
```

Strengthened run:

```text
PRED-C1-r26-v2 cases_pass=2/41 verdict=TARGET_MISSED
exit=1
```

Every passing generated case in these runs reported `changed=no`. No generated case whose oracle table differed from BASE passed. The two unchanged runs scored APPEND 0/20 and 1/20, EDIT 0/10 and 1/10, and SYNTH 0/10 and 0/10. The strengthened run scored APPEND 1/20, EDIT 0/10, SYNTH 0/10.

All three receipts reported:

```text
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
ORACLE_VERSION commit=efb50993780079460b0cbed1363e2166a2de1d9f tag=v0.56.2
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
```

## Strengthening within the registered shape

File: `/fast/scratch/hyaku/mado-r26/rescore/RescoreK1LabelKeyed/K1LabelKeyed-strengthened.py`.

SHA-256: `055c73c7f0d005e25e772dd10903b53f5f546c79af0f32efc630f4be7c73dbdb`.

The w1 shape is explicitly metadata-only replay, not a resolver (`w1/reports/K1LabelKeyed.md:12-17`; original control `:305-350`). The extension preserves the original label/path/inode/exact-fingerprint selection. Only an exact-fingerprint miss gains a fallback: hash the known baseline filenames, sizes and mtime-equals-ctime flags while ignoring added filenames, then replay an unambiguous cached single-DISABLE answer.

The fallback was derived solely from the existing w1 `training.json` (SHA-256 `f29f155fb249064e6cb7e6e9ed1f1155979613b824438c89911328ec3a21ca33`, training seed `c1a8e126`). Its 34 single-DISABLE records form 12 projected metadata buckets; eight contain conflicting answers and were excluded. The remaining four identify cached `DISABLE:fade`, `DISABLE:specialWorkspace`, `DISABLE:specialWorkspaceIn`, and `DISABLE:specialWorkspaceOut` answers. No new animation table was computed or embedded; the new map holds only metadata hashes and existing answer indices.

Runtime still does not open configuration contents, traverse the source graph, expand variables or evaluate animation semantics. It retains the original bounded namespace-metadata reads without adding a new leak surface. This is a stronger replay attempt for cases with extra unsourced files, not a new contract or a claimed general resolver. Its fresh-seed counter score did not improve on the best unchanged run. The three independent seeds do not establish a paired no-harm result.

## Bounded pristine / mutated / restored probe

Mutation: the scratch fallback above ignores newly added files when matching four trained metadata profiles. This is a plausible but potentially unsound shortcut: added files are not generally irrelevant. The lane control was never mutated.

Expected detector: `detector.py` in the scratch root uses the frozen v2 comparison functions and one actual pinned Hyprland oracle answer. Its fixed tree applies `DISABLE:fade` with the original training generator choice seed `0x26`, followed by `UNSOURCED` with seed `0x26262`. The same tree, expected table, sandboxed command and tuple-set comparison were used in all three phases; only `probe-control.py` bytes changed.

| Phase | Actual detector output | Exit | Control SHA-256 |
| --- | --- | --- | --- |
| Pristine | FAIL; nodes missing=1 extra=1; beziers missing=0 extra=0 | 1 | `2a17d95930f5c49318b446ee4cc66ad439e821e36cf1261f38b9104eff8e38da` |
| Mutated | PASS; nodes missing=0 extra=0; beziers missing=0 extra=0 | 0 | `055c73c7f0d005e25e772dd10903b53f5f546c79af0f32efc630f4be7c73dbdb` |
| Restored | FAIL; nodes missing=1 extra=1; beziers missing=0 extra=0 | 1 | `2a17d95930f5c49318b446ee4cc66ad439e821e36cf1261f38b9104eff8e38da` |

Mutation verdict: **inconclusive**, not killed or survived: the pristine baseline failed. The improvement on this one witness shows the fallback is exercised, not that the shortcut is sound generally. Full actual expected/output tables and phase hashes are in `witness.json`, `detector-pristine.json`, `detector-mutated.json`, and `detector-restored.json` under the scratch root.

The tree content-manifest hash was identical in all three phases: `13220c997c2d7f27df283483db9f829708a35e16bba4287e8b4f337c880bb8e5`. The witness oracle reported the pinned Hyprland commit and coredumps 1335 → 1335, delta 0.

## Exact exercised commands

Cwd for counter and detector commands: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

```sh
timeout 10 df -h /fast
# Above: 146G available before scratch writes.

# Executed twice, without modifying the control or supplying --seed:
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c1/count-v2.py 1b0b91e9 --tool-file .ufo/waves/round-26/controls/K1LabelKeyed.py --jobs 1

# Executed once:
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c1/count-v2.py 1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/rescore/RescoreK1LabelKeyed/K1LabelKeyed-strengthened.py --jobs 1

env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 180 prlimit --as=4000000000:8000000000 -- python3 -I /fast/scratch/hyaku/mado-r26/rescore/RescoreK1LabelKeyed/detector.py --phase pristine
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 120 prlimit --as=4000000000:8000000000 -- python3 -I /fast/scratch/hyaku/mado-r26/rescore/RescoreK1LabelKeyed/detector.py --phase mutated
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 120 prlimit --as=4000000000:8000000000 -- python3 -I /fast/scratch/hyaku/mado-r26/rescore/RescoreK1LabelKeyed/detector.py --phase restored

env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 10 sha256sum .ufo/waves/round-26/controls/K1LabelKeyed.py .ufo/waves/round-26/c1/count-v2.py .ufo/waves/round-26/harness/oracle.py /fast/scratch/hyaku/mado-r26/rescore/RescoreK1LabelKeyed/probe-control.py /fast/scratch/hyaku/mado-r26/rescore/RescoreK1LabelKeyed/K1LabelKeyed-strengthened.py
```

The two original counters ran concurrently with `--jobs 1`; all oracle calls used the harness's host-wide 12-slot lock. Only the pinned `oracle()` function started nested compositors, and its cleanup blocks returned. All started counter/detector commands have finished. No live-compositor command, DRM card-node use, git/jj write, sibling edit, service restart, or package install/update was performed.

## Restoration evidence

Final `sha256sum` output confirms exact pristine restoration of `probe-control.py`, and before/after equality for all three lane inputs:

```text
2a17d95930f5c49318b446ee4cc66ad439e821e36cf1261f38b9104eff8e38da  .ufo/waves/round-26/controls/K1LabelKeyed.py
4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428  .ufo/waves/round-26/c1/count-v2.py
680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441  .ufo/waves/round-26/harness/oracle.py
2a17d95930f5c49318b446ee4cc66ad439e821e36cf1261f38b9104eff8e38da  /fast/scratch/hyaku/mado-r26/rescore/RescoreK1LabelKeyed/probe-control.py
055c73c7f0d005e25e772dd10903b53f5f546c79af0f32efc630f4be7c73dbdb  /fast/scratch/hyaku/mado-r26/rescore/RescoreK1LabelKeyed/K1LabelKeyed-strengthened.py
```

Only this scoped report was written into the lane. The strengthened candidate remains isolated in scratch; nothing was integrated or shipped.

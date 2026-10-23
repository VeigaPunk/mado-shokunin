# RescoreK1FlatScan — round 27 w2

RESCORE K1FlatScan best: PRED-C1-r27-v4 cases_pass=4/41 verdict=TARGET_MISSED — not met

## Scope and result

Axes: exact ordered/type-strict JSON coverage; strength within the source-blind/global-prepass shape; seed and byte provenance; host safety and exact restoration.

Ran the committed control twice with fresh seeds under frozen counter v4, at `2fdca5caaab6859386effbb8fa6acc5250c90633`. Results: **2/41 and 3/41**, both TARGET_MISSED. The supplied comparison paths are under `controls/v4/` and their contents identify **v4**, not v3: both historical results were **1/41**. For completeness, the actual `controls/v3/` receipts identify v3 and scored **2/41 and 1/41**. All these are different-seed samples, not paired evidence of a version effect.

The committed control is **not the strongest demonstrated version of its shape**. Its two variable regexes accept only `$ws` plus three lowercase letters, a naming restriction left from the original generator. I broadened assignment and substitution to `$[A-Za-z_][A-Za-z0-9_]*`, changing only two lines. The resulting file still scans all files, still ignores `source` execution/reachability, still uses the same filename buckets, and still binds final values globally. No source following, temporal scope, fixture-label exception, or decoy filter was added.

Variant: `/fast/scratch/hyaku/mado-r27/rescore/K1FlatScan-GeneralVars.py`, SHA-256 `84ea49e86ac2d7cce9fbe662f8469017cdfe3b4c358df43e099a8d74dac34ee8`. Its two independent fresh seeds both scored **1/41**. A paired run on the first baseline seed improved **2/41 to 4/41**: BASE and C36 remained passing; C06 and C24 became passing. This demonstrates a within-shape improvement on that seed, not universal dominance or an exhaustive optimum. The best 4/41 line is from this explicitly identified paired run, not a third independent seed. None reached 41/41.

## Predicate lines and receipts

All new receipt names below resolve under `/fast/scratch/hyaku/mado-r27/rescore/`. Every scored receipt printed `exit=1` and `HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0`.

| Run | Seed | Receipt | Verbatim PRED line |
| --- | --- | --- | --- |
| Committed, fresh 1 | `1a3466781ee96bcd` | `K1FlatScan-seed1.txt` | `PRED-C1-r27-v4 cases_pass=2/41 verdict=TARGET_MISSED` |
| Committed, fresh 2 | `cd47034fab1870d8` | `K1FlatScan-seed2.txt` | `PRED-C1-r27-v4 cases_pass=3/41 verdict=TARGET_MISSED` |
| GeneralVars, fresh 1 | `5eb2fd05b6bb8416` | `K1FlatScan-GeneralVars-seed1.txt` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` |
| GeneralVars, fresh 2 | `99a85d9b7487b914` | `K1FlatScan-GeneralVars-seed2.txt` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` |
| GeneralVars, paired baseline seed 1 | `1a3466781ee96bcd` | `K1FlatScan-GeneralVars-matched-seed1.txt` | `PRED-C1-r27-v4 cases_pass=4/41 verdict=TARGET_MISSED` |

Historical comparison, relative to the lane:

| Receipt | Seed | Verbatim PRED line |
| --- | --- | --- |
| `.ufo/waves/round-27/controls/v4/K1FlatScan-seed1.txt` | `7841be9b90076871` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` |
| `.ufo/waves/round-27/controls/v4/K1FlatScan-seed2.txt` | `d091ea89e3f5b63c` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` |
| `.ufo/waves/round-27/controls/v3/K1FlatScan-seed1.txt` | `c5c869d2ee2cca23` | `PRED-C1-r27-v3 cases_pass=2/41 verdict=TARGET_MISSED` |
| `.ufo/waves/round-27/controls/v3/K1FlatScan-seed2.txt` | `005dea94a64865eb` | `PRED-C1-r27-v3 cases_pass=1/41 verdict=TARGET_MISSED` |

All five new counter runs passed the base-repeat and pinned-version guards. Each used the same 79-file snapshot digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`.

## Exact scoring commands

Working directory for every command: `/home/vgpnk/Projects/shokunin/mado-shokunin`. The pipelines save stdout; the counter's printed `exit=1`, not tee's exit status, is the reported counter outcome.

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1FlatScan.py --jobs 6 | env -i PATH=/usr/bin HOME=/home/vgpnk timeout 920 tee /fast/scratch/hyaku/mado-r27/rescore/K1FlatScan-seed1.txt
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1FlatScan.py --jobs 6 | env -i PATH=/usr/bin HOME=/home/vgpnk timeout 920 tee /fast/scratch/hyaku/mado-r27/rescore/K1FlatScan-seed2.txt
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /fast/scratch/hyaku/mado-r27/rescore/K1FlatScan-GeneralVars.py --jobs 6 | env -i PATH=/usr/bin HOME=/home/vgpnk timeout 920 tee /fast/scratch/hyaku/mado-r27/rescore/K1FlatScan-GeneralVars-seed1.txt
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /fast/scratch/hyaku/mado-r27/rescore/K1FlatScan-GeneralVars.py --jobs 6 | env -i PATH=/usr/bin HOME=/home/vgpnk timeout 920 tee /fast/scratch/hyaku/mado-r27/rescore/K1FlatScan-GeneralVars-seed2.txt
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /fast/scratch/hyaku/mado-r27/rescore/K1FlatScan-GeneralVars.py --jobs 6 --seed 1a3466781ee96bcd | env -i PATH=/usr/bin HOME=/home/vgpnk timeout 920 tee /fast/scratch/hyaku/mado-r27/rescore/K1FlatScan-GeneralVars-matched-seed1.txt
```

The two initial attempts to request asynchronous execution returned `Background job limit reached (100)` before running. Both required baseline commands were then actually executed using synchronous tool calls, producing the receipts above. One variant invocation was automatically backgrounded by the tool and its completion was delivered before mutation; no running candidate was edited.

## One isolated mutation probe

After all full counter runs completed, challenged the broadened identifier matcher with one plausible off-by-one defect: at GeneralVars line 43 only, changed the initial identifier class from `[A-Za-z_]` to `[A-Za-y_]`. The definition matcher stayed unchanged. This was confined to the owned scratch file; no committed control, counter, oracle, or sibling source was mutated.

Expected detector: the unchanged `K1FlatScan-probe.py` creates this bounded, non-crashing root-only tree and compares type-strict canonical JSON through the pinned `oracle()` and `run_tool()` interfaces:

```text
$zzzzz = 4
workspace = 3, bordersize:$zzzzz
```

The oracle was valid in all three runs (correct Hyprland commit and no nonempty config error). Its expected JSON was always `[{"workspaceString":"3","enabled":true,"borderSize":4}]`.

| State | Tool SHA-256 | Actual detector output | Receipt |
| --- | --- | --- | --- |
| Pristine GeneralVars | `84ea49e86ac2d7cce9fbe662f8469017cdfe3b4c358df43e099a8d74dac34ee8` | Matching JSON; `passed=true`, `exit=0` | `K1FlatScan-probe-pristine.txt` |
| Mutated initial class | `6aea2dfc749bf55c631d96f5c6fca8d447cf528f55bf7b3277c1ee8294de5314` | `actual=null`, `passed=false`, tool exit 1: `ValueError: invalid literal for int() with base 10: '$zzzzz'`; detector `exit=1` | `K1FlatScan-probe-mutated.txt` |
| Restored GeneralVars | `84ea49e86ac2d7cce9fbe662f8469017cdfe3b4c358df43e099a8d74dac34ee8` | Matching JSON; `passed=true`, `exit=0` | `K1FlatScan-probe-restored.txt` |

Mutation verdict: **killed by the bounded witness**, with a passing pristine baseline and passing exact restoration. This does not turn the full counter's failing baselines into killed mutants: those are target misses only. Pristine and restored witness receipt bytes also hash identically (`a106a941c6951825f92372dd9daa5d2fb04ef1eb4775dced1f94f68ca43dd03d`).

Exact witness commands, same working directory:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 240 prlimit --as=4000000000:8000000000 --core=0 -- python3 -B -I /fast/scratch/hyaku/mado-r27/rescore/K1FlatScan-probe.py --tool /fast/scratch/hyaku/mado-r27/rescore/K1FlatScan-GeneralVars.py | env -i PATH=/usr/bin HOME=/home/vgpnk timeout 250 tee /fast/scratch/hyaku/mado-r27/rescore/K1FlatScan-probe-pristine.txt
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 240 prlimit --as=4000000000:8000000000 --core=0 -- python3 -B -I /fast/scratch/hyaku/mado-r27/rescore/K1FlatScan-probe.py --tool /fast/scratch/hyaku/mado-r27/rescore/K1FlatScan-GeneralVars.py | env -i PATH=/usr/bin HOME=/home/vgpnk timeout 250 tee /fast/scratch/hyaku/mado-r27/rescore/K1FlatScan-probe-mutated.txt
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 240 prlimit --as=4000000000:8000000000 --core=0 -- python3 -B -I /fast/scratch/hyaku/mado-r27/rescore/K1FlatScan-probe.py --tool /fast/scratch/hyaku/mado-r27/rescore/K1FlatScan-GeneralVars.py | env -i PATH=/usr/bin HOME=/home/vgpnk timeout 250 tee /fast/scratch/hyaku/mado-r27/rescore/K1FlatScan-probe-restored.txt
```

The detector parent has a 4 GB soft address-space cap and an 8 GB hard ceiling so the unchanged pinned oracle can set its own 8 GB limit. Every witness printed zero coredump delta. The reproducer is retained as evidence, not integrated code.

## Byte and receipt provenance

Before and after SHA-256 values were identical for all committed execution inputs:

- Control: `68339595f2a1ae6c0d41276c78852f81af7fb5ebc7b423f320a4d0f0c7abf1ea`.
- Frozen counter v4: `635ae788fd897c8f1fba88e4ab2ffcb95e7f79a88703b82e49a8729ce7d271a1`.
- Oracle: `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601`.

Receipt SHA-256 values:

```text
b82fe3e25676b062162099ffb9fbc0ab8869312be48ab4c2dcb776809af0af42  K1FlatScan-seed1.txt
89046fd1c4e6e11bf09a7a7d5e06d060e49dab4459197e92c7557a849bb9077a  K1FlatScan-seed2.txt
6082eeae900eaeeb806dc5460e5405941d7e463c353dacc00f3d06bbec7c5232  K1FlatScan-GeneralVars-seed1.txt
57b9b257b5946639dd5762460312fc98a2c2b517577e5c2aa62c897c48dc7b1b  K1FlatScan-GeneralVars-seed2.txt
805502f1ef17acfe4f715908cc1607c26ced44e5c64d8f119b524bd1c5bc3adf  K1FlatScan-GeneralVars-matched-seed1.txt
a106a941c6951825f92372dd9daa5d2fb04ef1eb4775dced1f94f68ca43dd03d  K1FlatScan-probe-pristine.txt
f851d21e04d8c69cc38aeefd0110fb6b0a74736f89f26aab0feedfe7df1c0d54  K1FlatScan-probe-mutated.txt
a106a941c6951825f92372dd9daa5d2fb04ef1eb4775dced1f94f68ca43dd03d  K1FlatScan-probe-restored.txt
```

The supplied historical v4 receipt hashes were `5b1300d81959b889671fbd093c230077c23d71730fc8ca8a6d7bf8200a7a93f5` (seed 1) and `d1eaacba667a0cb27ec608e3017425de76100c9987d267704194598e2e942e13` (seed 2). Detector script SHA-256: `b7b556fdb125753cc2220350bbe9c49ac7eeac4b71a0e798aa475c1a8bdee9da`.

## Safety and boundaries

Read registration and godspeed skill before execution, and read `/home/vgpnk/.omp/agent/RULES.md`. No tools installed or upgraded. No subagents or other orchestration runtime invoked. No git/jj writes or live-compositor queries; I edited no lane file except this report. All experiment files and receipts are under the assigned rescore prefix.

Initial `df -h /fast` reported 73 GB available. Direct bounded `coredumpctl list --no-pager --no-legend` captures counted **1338 before, 1338 after, delta 0**, both return code 0 with empty stderr. Details: `/fast/scratch/hyaku/mado-r27/rescore/K1FlatScan-host-safety.txt`. Counters used their own limits; direct utility commands and witness parents had the address-space limits shown above. Tee receipt writers had timeouts but no explicit address-space cap. Each counter used six workers; the pinned oracle's host-wide twelve-slot flock limit remained in force. All Hyprland starts were through the pinned oracle. All scoring and witness commands completed; the inspected oracle `finally` kills/waits its sandbox process groups, and the counters/detector remove temporary case/work directories. No service or watcher was started.

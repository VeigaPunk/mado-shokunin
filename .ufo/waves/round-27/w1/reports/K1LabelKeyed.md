# K1LabelKeyed — C1 LABEL-KEYED control

## Verdict
CONTROL K1LabelKeyed best: PRED-C1-r27 cases_pass=1/41 verdict=TARGET_MISSED — not met

Both fresh-seed runs passed BASE and failed every APPEND and SYNTH case. Both process exits were 1, with no setup guard or exit-2 rerun. This control does not trigger the registration's redesign rule.

## Control and expected detector

Implemented `.ufo/waves/round-27/controls/K1LabelKeyed.py`, a single Python-stdlib file with `--home DIR` and JSON-array stdout.

The challenged substitution is metadata/family classification plus canned answers instead of workspace-rule semantics. The expected detector is the frozen C1 counter's exact, ordered JSON-array equality against isolated Hyprland v0.56.2.

Axes: score, shape purity, host safety, and reproducibility. The control:

- Searches case/family tokens (`BASE`, `APPEND`, `SYNTH`, `C00`–`C39`) in paths, arguments, filenames, environment, `/proc/self/mountinfo`, mounts, cgroups, and its own/PID-1 command lines and environments.
- Falls back to file counts, relative filenames, sizes, and timestamps. A pinned 79-file name/size fingerprint recognizes the unperturbed snapshot; other metadata guesses snapshot-backed versus synthetic trees.
- Emits only fixed canned arrays. BASE/unknown emits `[]`; APPEND/SYNTH emits `[{"workspaceString":"1","enabled":true}]`. A visible case ID maps to its registered family. The nonempty array is a fixed, source-schema-compatible guess, not an oracle-derived generated-case answer.
- Never opens a config file. Its only file-content reads are the listed bounded `/proc` metadata reads. It does not parse selectors, rule keys, variables, sources, or workspace lines; invoke Hyprland/hyprctl; or use the network.

The registered pilot and the StaticBase seat's independent receipts establish the canned BASE table as `[]`; both of this seat's counters independently confirmed BASE has zero rules. The authoring metadata fingerprint was `7ed0b2c7cdcda4ee7ae6aad5b383a38c5842ce4277794d97962b59d0bed58aec` (names and sizes only).

## Exact scoring command

Working directory: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Ran this command twice concurrently, without `--seed`, so each frozen counter generated its own fresh seed:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count.py 5ddc5885 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1LabelKeyed.py --jobs 6
```

Python subprocess orchestration captured stdout verbatim into the receipts below, without adding the separately observed process return code. Counter stdout itself includes `exit=1`. Stderr was empty for both runs. Both counter processes were awaited to exit.

| Run | Fresh seed | BASE | APPEND | SYNTH | Actual PRED output | Exit | Receipt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `97b2e42dca0324b7` | 1/1 | 0/25 | 0/15 | `PRED-C1-r27 cases_pass=1/41 verdict=TARGET_MISSED` | 1 | `.ufo/waves/round-27/controls/K1LabelKeyed-seed1.txt` |
| 2 | `ca58bc92728dd21d` | 1/1 | 0/25 | 0/15 | `PRED-C1-r27 cases_pass=1/41 verdict=TARGET_MISSED` | 1 | `.ufo/waves/round-27/controls/K1LabelKeyed-seed2.txt` |

Both receipts resolved REV to `5ddc5885188a1de8606464526d636c9e2fc433e6`, recorded the same 79-file snapshot digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`, confirmed two equal BASE oracle runs, and confirmed oracle commit `efb50993780079460b0cbed1363e2166a2de1d9f`, tag `v0.56.2`.

The receipts show both empty and nonempty guesses on APPEND, so the metadata heuristic is imperfect. Every SYNTH guess was nonempty. Even generated cases where guessed and expected list lengths were both one failed at entry zero. The observed result is rejection of this control, not proof that every possible metadata label leak is absent.

## Integrity and restoration evidence

No existing implementation, counter, harness, configuration, or sibling file was mutated. This is a control probe, not a pristine/mutated/restored source-mutant experiment; no source-mutant kill is claimed. The new control is intentionally retained as required by the control contract, with exactly the same bytes throughout both scored runs. The original controls-directory listing was empty.

`sha256sum` before and after the two runs returned identical hashes:

| File | SHA-256 before = after |
| --- | --- |
| `controls/K1LabelKeyed.py` | `1fb107df8d51811145da3fa12e2e1b01349ad295b5fcff1f34ca491c7d718c72` |
| `c1/count.py` | `3d7d301fb9315f9a6cea2427db7c39e556482b30d3f4283373579ae665afd136` |
| `harness/oracle.py` | `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601` |

Paths in this table are under `.ufo/waves/round-27/`.

Receipt hashes:

- Seed 1: `932e50f9e32266f929fd698e5933182ff6dec64699aed14433f3bbf074075078`.
- Seed 2: `799ccd86aa1349c140f685a8aca5c387c411d5b61c654c7ceb9775cc8cd2689c`.

## Host safety and tooling

`timeout 10 df -h /fast` reported 115G available before scoring. No standalone compositor or live-session mutation was started; only the frozen counter invoked the pinned oracle, which limits host-wide nested instances and terminates its process groups in its finalizer.

The separate coredump observations were:

```sh
env -i PATH=/usr/bin timeout 20 prlimit --as=4000000000 --core=0 -- coredumpctl list --no-pager --no-legend
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 --core=0 -- coredumpctl list --no-pager --no-legend
```

Counting output lines containing `/usr/bin/Hyprland` gave own before=1338, after=1338, delta=0. Each counter also printed `HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0`.

No tools were installed or updated. No git/jj write command was run. No additional implementation tests or source-mutant probes were performed.

## V2 re-score — unchanged control

CONTROL K1LabelKeyed v2 best: PRED-C1-r27-v2 cases_pass=1/41 verdict=TARGET_MISSED — not met

At L1's follow-up instruction, re-scored the exact same control bytes against the redesigned v2 counter. V1 above is retained historical evidence, not the active C1 rule. The detector now includes unsourced decoys, nested/glob sources, interleaved source positions, variable redefinition, and type-strict JSON comparison.

Ran this exact command twice concurrently from the lane directory, leaving seeds unspecified so the counter generated two fresh seeds:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v2.py a4dc0da0 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1LabelKeyed.py --jobs 6
```

| Run | Fresh seed | BASE | APPEND | SYNTH | Actual PRED output | Process exit | Verbatim stdout receipt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `74a58228b0aaa937` | 1/1 | 0/25 | 0/15 | `PRED-C1-r27-v2 cases_pass=1/41 verdict=TARGET_MISSED` | 1 | `.ufo/waves/round-27/controls/v2/K1LabelKeyed-seed1.txt` |
| 2 | `0bba261298c05f0b` | 1/1 | 0/25 | 0/15 | `PRED-C1-r27-v2 cases_pass=1/41 verdict=TARGET_MISSED` | 1 | `.ufo/waves/round-27/controls/v2/K1LabelKeyed-seed2.txt` |

Both stdout receipts include `exit=1`; stderr was empty. Neither run hit an exit-2 guard, so neither required a rerun. Both resolved REV to `a4dc0da0394a71badf506e9c72144cd1b8ca7281`, recorded the unchanged snapshot digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`, confirmed BASE twice equal with zero rules, and confirmed oracle commit `efb50993780079460b0cbed1363e2166a2de1d9f`, tag `v0.56.2`.

Before/after `sha256sum` observations were identical:

| File under `.ufo/waves/round-27/` | SHA-256 before = after |
| --- | --- |
| `controls/K1LabelKeyed.py` | `1fb107df8d51811145da3fa12e2e1b01349ad295b5fcff1f34ca491c7d718c72` |
| `c1/count-v2.py` | `258118841448530d63cc07804115b3eca5780c23e62a8d6f238779a2a090bf87` |
| `harness/oracle.py` | `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601` |

The v2 counter hash matches L1's follow-up pin. The control was not changed or restored because no mutation was made; its delivered bytes remain identical to the v1-scored bytes.

V2 receipt SHA-256:

- Seed 1: `7c4a86e66ee2c97e8e667d0d1eba7a11023b6b46a55765a0e19a1984994850de`.
- Seed 2: `847349ef10ced185167a7e0d64e1f4776ec8dd1daf960829205393d0ca12b28e`.

Both counters printed `HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0`. Independent before/after observations using `env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 --core=0 -- coredumpctl list --no-pager --no-legend` also counted 1338 and 1338 Hyprland entries: own v2 delta=0. Both counter processes were awaited to exit; nested compositor lifecycle remained exclusively under the unchanged pinned oracle. The bounded pre-run `df -h /fast` observation reported 113G available. No tools were installed or updated, no git/jj writes were run, and no control/source bytes were edited.


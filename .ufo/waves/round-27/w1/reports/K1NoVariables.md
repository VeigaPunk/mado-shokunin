# K1NoVariables — C1 NO-VARIABLES control

## Verdict
CONTROL K1NoVariables best: PRED-C1-r27 cases_pass=20/41 verdict=TARGET_MISSED — not met

The frozen detector rejected this control on both fresh seeds. Neither run returned exit 2; no guard retry was needed. The control did not trigger the registration's target-meeting kill rule.

| Run | Fresh seed | Actual PRED output | Exit | Verbatim stdout receipt |
| --- | --- | --- | --- | --- |
| 1 | `3d3ab56f785ed7dd` | `PRED-C1-r27 cases_pass=16/41 verdict=TARGET_MISSED` | 1 | `.ufo/waves/round-27/controls/K1NoVariables-seed1.txt` |
| 2 | `33d479630cbfe8a9` | `PRED-C1-r27 cases_pass=20/41 verdict=TARGET_MISSED` | 1 | `.ufo/waves/round-27/controls/K1NoVariables-seed2.txt` |

Every failing case in these receipts has the `VARIABLE` feature. Every case without that feature passed. Variable-tagged cases C00 in run 1 and C03/C25 in run 2 also passed: a feature tag by itself is not a guarantee that omission changes the final observable table. No claim of general parser completeness follows from these two measurements.

## Assigned defect and detector

- Deliberate defect: ignore every variable assignment and leave all `$name` references literal. There is no variable table, environment substitution, variable-derived selector recovery, or case-label lookup.
- Expected detector: the frozen C1 counter's exact ordered JSON-list comparison against isolated Hyprland v0.56.2. A variable reference that changes the final selector or serialized fields should produce a mismatch.
- Output: 24 mismatches in run 1 and 21 in run 2, with successful baseline-oracle guards in both runs.
- Probe verdict: the NO-VARIABLES control was rejected twice; the C1 target was not met by this shape.

## Implementation and scope

Axes: shape fidelity, non-variable semantic coverage, reproducible evidence, and host safety.

Created only the assigned stdlib Python control, its two receipts, and this report:

- `.ufo/waves/round-27/controls/K1NoVariables.py`
- `.ufo/waves/round-27/controls/K1NoVariables-seed1.txt`
- `.ufo/waves/round-27/controls/K1NoVariables-seed2.txt`
- `.ufo/waves/round-27/w1/reports/K1NoVariables.md`

The control follows `source =` at its position in the input, supports home-relative and file-relative paths and sorted globs, and merges repeated literal selectors without changing their first insertion order. It handles the serialized workspace-rule fields, CSS gap shorthand, boolean words, comma escaping, doubled-hash comments, continuations, and on-created-empty workspace-command decoration. Layout options are validated but omitted from JSON, matching the serializer's exposed field set. Parsing does not execute config commands. Source traversal stays inside the supplied HOME and guards against active recursive includes. Neither source paths nor rule text are expanded from `$name` references.

No data implementation, suite, counter, harness, W set, held-out file, other seat's source, git state, or live compositor configuration was modified. No subagents or additional runtime were invoked. No tools were installed or updated.

## Exact measurement command

Working directory: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Executed this same command twice, concurrently. Omitting `--seed` let the counter select the two fresh seeds printed above. Each run used six workers; the harness's shared locks enforce the host-wide twelve-instance limit.

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count.py 5ddc5885 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1NoVariables.py --jobs 6
```

Both receipts include:

```text
rev=5ddc5885188a1de8606464526d636c9e2fc433e6
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal rules=0
ORACLE_VERSION commit=efb50993780079460b0cbed1363e2166a2de1d9f tag=v0.56.2
HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0
exit=1
```

The `rev=` value above is extracted from the receipts' first line; the saved receipt files preserve complete stdout, including the case lines and `exit=`.

## Hashes and restoration evidence

The counter hashed the control before each measurement. Both receipts record SHA-256 `65672716b17daf24f7a4f7d69ab4b922cc47066c2d02e5cdd0586423e3cc0b44`. The final hash command returned the same value. The control was not edited between or after the runs.

Frozen inputs matched their supplied pins before measurement and remained byte-identical afterward:

```text
3d7d301fb9315f9a6cea2427db7c39e556482b30d3f4283373579ae665afd136  .ufo/waves/round-27/c1/count.py
0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601  .ufo/waves/round-27/harness/oracle.py
```

Initial hash command:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/c1/count.py .ufo/waves/round-27/harness/oracle.py
```

Final hash command:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/controls/K1NoVariables.py .ufo/waves/round-27/c1/count.py .ufo/waves/round-27/harness/oracle.py
```

This was an additive standalone control assignment, not an edit to a pristine implementation; there were no subject bytes requiring restoration. No pristine/mutated/restored implementation cycle is claimed.

## Host safety

Before counter scratch writes:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 -- df -h /fast
```

Output:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  689G  115G  86% /fast
```

Crash census command, run once before measurement and once after both runs:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 30 prlimit --as=4000000000 -- sh -c 'coredumpctl list --no-pager --no-legend | grep -c /usr/bin/Hyprland'
```

Actual output was `1338` both times: seat-observed delta `0`. Both counter receipts independently report delta `0`. The two counter processes completed, and nested compositor lifecycle/termination was handled by the frozen harness. No Hyprland process was started outside that harness, no live compositor verbs were issued, and no host display/signature variables were passed to commands.

## Pinned implementation references

Read registration first. Then consulted the frozen counter/harness and fetched the following upstream code through bounded, clean-environment `curl -fsSL` commands, using the pattern:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 30 prlimit --as=4000000000 -- curl -fsSL URL
```

- [Workspace handler and source traversal](https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp)
- [JSON serializer](https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp)
- [Selector merge lookup](https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/workspace/WorkspaceRuleManager.cpp)
- [Merge field precedence](https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/workspace/WorkspaceRule.cpp)
- [Gap shorthand implementation](https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/complex/ComplexDataTypes.hpp)
- [Boolean/integer parser](https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/parserUtils/ParserUtils.cpp)
- [Workspace names and command decoration](https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/MiscFunctions.cpp)
- [Hyprlang 0.6.8 preprocessing](https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp)
- [Hyprutils 0.14.2 tokenizer](https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/string/VarList2.cpp)
- [Tokenizer defaults](https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/include/hyprutils/string/VarList2.hpp)
- [Command-list tokenization](https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/string/VarList.cpp)
- [Numeric conversion](https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/include/hyprutils/string/Numeric.hpp)

An attempted `src/config/shared/complex/ComplexDataTypes.cpp` fetch returned HTTP 404; the implementation is in the successfully opened header linked above. No claim relies on that unopened URL. Workspace-manager and workspace-rule headers were also read to resolve the implementation paths. No source-corpus rows were changed: this seat is a control, not a source-opener.

Only the two required counter measurements were run; no separate build, lint, formatter, smoke test, or mutation cycle was run.

## v2 rescoring
CONTROL K1NoVariables v2 best: PRED-C1-r27-v2 cases_pass=17/41 verdict=TARGET_MISSED — not met

This follow-up adds two measurements under the redesigned v2 counter; the preceding sections preserve the historical v1 work. The control was not changed. The v2 detector rejected it on both fresh seeds. Neither run returned exit 2, so no guard retry was needed.

| Run | Fresh seed | Actual PRED output | Exit | Verbatim stdout receipt |
| --- | --- | --- | --- | --- |
| 1 | `43a7bfd51fab9972` | `PRED-C1-r27-v2 cases_pass=9/41 verdict=TARGET_MISSED` | 1 | `.ufo/waves/round-27/controls/v2/K1NoVariables-seed1.txt` |
| 2 | `9df8dcf40a4f7fd5` | `PRED-C1-r27-v2 cases_pass=17/41 verdict=TARGET_MISSED` | 1 | `.ufo/waves/round-27/controls/v2/K1NoVariables-seed2.txt` |

Every v2 failure carries `VARIABLE` or `VARREDEF`; all cases carrying neither feature passed. Run 1 C10 is variable-tagged but passes. These observations support detection of the assigned omission, not a general completeness claim.

### Exact v2 command and guards

Working directory remained `/home/vgpnk/Projects/shokunin/mado-shokunin`. Executed the following unchanged command twice, concurrently, with six workers per run and the harness's shared instance locks:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v2.py a4dc0da0 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1NoVariables.py --jobs 6
```

Both receipts identify revision `a4dc0da0394a71badf506e9c72144cd1b8ca7281`, counter SHA-256 `258118841448530d63cc07804115b3eca5780c23e62a8d6f238779a2a090bf87`, and the same 79-file snapshot digest as v1. Both passed `ORACLE_CHECK base_twice equal rules=0` and verified nested Hyprland commit `efb50993780079460b0cbed1363e2166a2de1d9f`, tag `v0.56.2`. Both full stdout receipts end in `exit=1`.

The actual v2 counter hash matched the L1 follow-up's explicit pin. The registration redesign paragraph read during this follow-up still listed the earlier v2 hash `f7f86d75eb45a2dcd6a2094dcb614b701c948d6fee90f46da911831213c1a2c4`; this seat did not alter the registration or counter.

### Unchanged bytes and host safety

Before scoring, ran:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/c1/count-v2.py .ufo/waves/round-27/controls/K1NoVariables.py .ufo/waves/round-27/harness/oracle.py
```

After both runs, ran:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/controls/K1NoVariables.py .ufo/waves/round-27/c1/count-v2.py .ufo/waves/round-27/harness/oracle.py
```

The before/after hashes and both receipts agree:

```text
65672716b17daf24f7a4f7d69ab4b922cc47066c2d02e5cdd0586423e3cc0b44  .ufo/waves/round-27/controls/K1NoVariables.py
258118841448530d63cc07804115b3eca5780c23e62a8d6f238779a2a090bf87  .ufo/waves/round-27/c1/count-v2.py
0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601  .ufo/waves/round-27/harness/oracle.py
```

The scratch-capacity command from the original report was repeated before scoring and returned:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  691G  113G  86% /fast
```

The same bounded, clean-environment crash census command was run before and after this follow-up. Both outputs were `1338`, giving a seat-observed delta of `0`. Each v2 receipt also prints `HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0`.

Both counter processes completed. Compositor startup and teardown stayed inside the frozen harness. Only the two requested v2 receipt files and this report appendix were written during the follow-up; control and subject bytes needed no restoration because they were never edited. No tools were installed, no subagents were dispatched, and no additional verification was run.

## v3 rescoring
CONTROL K1NoVariables v3 best: PRED-C1-r27-v3 cases_pass=10/41 verdict=TARGET_MISSED — not met

Re-scored the unchanged NO-VARIABLES control under the registered v3 counter, which randomizes generated variable names without a fixed prefix. Both fresh-seed measurements rejected the control; neither returned exit 2 and no guard retry was needed.

| Run | Fresh seed | Actual PRED output | Exit | Verbatim stdout receipt |
| --- | --- | --- | --- | --- |
| 1 | `32b6552f33f29d4d` | `PRED-C1-r27-v3 cases_pass=8/41 verdict=TARGET_MISSED` | 1 | `.ufo/waves/round-27/controls/v3/K1NoVariables-seed1.txt` |
| 2 | `9cbc9111ba1de2aa` | `PRED-C1-r27-v3 cases_pass=10/41 verdict=TARGET_MISSED` | 1 | `.ufo/waves/round-27/controls/v3/K1NoVariables-seed2.txt` |

Every failing case in both v3 receipts carries `VARIABLE` or `VARREDEF`. Every case carrying neither feature passed. The control's missing variable evaluation remains detected; the target-meeting kill rule is not triggered.

### Exact command and actual outputs

Working directory: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Executed the following command twice with fresh seeds selected by the counter:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v3.py 9f5fc28b --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1NoVariables.py --jobs 6
```

The initial two asynchronous tool launch requests were rejected with `Background job limit reached (100). Wait for running jobs to finish or cancel one.` Retrying the same command through non-asynchronous tool calls produced the two completed counter runs recorded above. There was no exit-2 detector run.

Both receipts report revision `9f5fc28b3db8d06870d0314818ffbe5e43bb5937`, the unchanged 79-file snapshot digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`, `ORACLE_CHECK base_twice equal rules=0`, and `ORACLE_VERSION commit=efb50993780079460b0cbed1363e2166a2de1d9f tag=v0.56.2`. Complete case output and terminal `exit=1` are preserved in each receipt.

### Before/after hashes and safety

Before measurement, ran:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/c1/count-v3.py .ufo/waves/round-27/controls/K1NoVariables.py .ufo/waves/round-27/harness/oracle.py
```

After measurement, ran:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/controls/K1NoVariables.py .ufo/waves/round-27/c1/count-v3.py .ufo/waves/round-27/harness/oracle.py
```

Both commands returned the same per-file hashes, also recorded in the receipts:

```text
65672716b17daf24f7a4f7d69ab4b922cc47066c2d02e5cdd0586423e3cc0b44  .ufo/waves/round-27/controls/K1NoVariables.py
ee4cea19c11a1a8160115f4754e88c11c58aac9a3bff40ccfd16920cd1d691bd  .ufo/waves/round-27/c1/count-v3.py
0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601  .ufo/waves/round-27/harness/oracle.py
```

The same bounded `df -h /fast` command used previously returned `/dev/nvme1n1p2 804G 710G 94G 89% /fast` before scratch writes. The same bounded crash-census command returned `1338` before and after v3 measurement: delta `0`. Both receipts independently report `HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0`.

Both counter jobs completed; nested compositor startup and teardown remained within the frozen harness. No control or subject bytes were changed, so no restoration was needed. Only the two v3 receipts and this report appendix were written during this follow-up. No subagents, installations, other runtime, build, lint, formatter, or extra behavioral checks were used.

## v4 rescoring
CONTROL K1NoVariables v4 best: PRED-C1-r27-v4 cases_pass=7/41 verdict=TARGET_MISSED — not met

Re-scored the unchanged control under v4, whose additional shapes cover embedded variable values, definitions in sourced files, use before definition, and repeated sourcing. Both fresh-seed runs rejected the control. Neither returned exit 2; no guard retry was required.

| Run | Fresh seed | Actual PRED output | Exit | Verbatim stdout receipt |
| --- | --- | --- | --- | --- |
| 1 | `a925bfbf44d81d7a` | `PRED-C1-r27-v4 cases_pass=7/41 verdict=TARGET_MISSED` | 1 | `.ufo/waves/round-27/controls/v4/K1NoVariables-seed1.txt` |
| 2 | `5488cc34a3a8e0be` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` | 1 | `.ufo/waves/round-27/controls/v4/K1NoVariables-seed2.txt` |

Every failing case carries `VARIABLE`, `VARREDEF`, or `USEBEFOREDEF`; cases carrying none of those three features passed. Run 2 passed only BASE. These results detect the intentional variable-handling omission and do not establish correctness on inputs outside the measured population.

### Exact command and outputs

Working directory remained `/home/vgpnk/Projects/shokunin/mado-shokunin`. Ran the following command twice with fresh seeds selected by the counter, four workers per run, and the harness's shared host-wide instance locks:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1NoVariables.py --jobs 4
```

Both receipts identify revision `2fdca5caaab6859386effbb8fa6acc5250c90633` and the same 79-file snapshot digest as the earlier runs. Both print `ORACLE_CHECK base_twice equal rules=0`, verify nested Hyprland commit `efb50993780079460b0cbed1363e2166a2de1d9f` and tag `v0.56.2`, and end with `exit=1`. Complete stdout, including every case line, is preserved at the two receipt paths above.

### Unchanged bytes and safety

Before scoring, ran:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/c1/count-v4.py .ufo/waves/round-27/controls/K1NoVariables.py .ufo/waves/round-27/harness/oracle.py
```

After scoring, ran:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/controls/K1NoVariables.py .ufo/waves/round-27/c1/count-v4.py .ufo/waves/round-27/harness/oracle.py
```

The before/after hashes and both measurement receipts agree:

```text
65672716b17daf24f7a4f7d69ab4b922cc47066c2d02e5cdd0586423e3cc0b44  .ufo/waves/round-27/controls/K1NoVariables.py
635ae788fd897c8f1fba88e4ab2ffcb95e7f79a88703b82e49a8729ce7d271a1  .ufo/waves/round-27/c1/count-v4.py
0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601  .ufo/waves/round-27/harness/oracle.py
```

The bounded scratch-capacity command returned `/dev/nvme1n1p2 804G 720G 84G 90% /fast` before scoring. The same bounded crash-census command used in preceding sections returned `1338` before and after this follow-up: seat-observed delta `0`. Both receipts also report `HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0`.

Both counter runs completed. Nested compositor lifecycle stayed inside the frozen harness. Only the requested v4 receipts and this appendix were written; the control remained byte-identical to its original implementation and no subject bytes needed restoration. No installations, subagents, builds, linters, formatters, or extra behavioral checks were used.

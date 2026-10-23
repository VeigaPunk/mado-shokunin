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

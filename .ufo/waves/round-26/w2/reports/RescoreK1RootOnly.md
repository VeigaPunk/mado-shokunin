# RescoreK1RootOnly — C1 counter v2

Seat: `MadoR26.RescoreK1RootOnly`. Revision: `1b0b91e9889cbf984b052f5de564db78330a72aa`.

RESCORE K1RootOnly not met (best 5/41)

## Scope and result

Axes: fresh-seed repeatability, within-shape strengthening, host isolation, exact-byte restoration.

Re-opened registration, the committed control, its w1 shape report, the L1's v2 receipt, the frozen counter and the oracle. Ran the committed control twice without editing it; each counter generated a new seed. Then changed one behavior-bearing expression in an isolated scratch copy, scored that strengthening once with run 2's seed, restored the exact original bytes, and ran the same detector again with that seed.

| Run | Seed | cases_pass | Counter/process exit |
|---|---|---:|---:|
| Committed control, fresh 1 | `c82c1f9f099921aa` | 3/41 | 1/1 |
| Committed control, fresh 2 | `f2014abfe7d2ec52` | 5/41 | 1/1 |
| Strengthened scratch copy | `f2014abfe7d2ec52` | 5/41 | 1/1 |
| Restored scratch copy | `f2014abfe7d2ec52` | 5/41 | 1/1 |

Both required re-score receipts' PRED lines and exit lines, verbatim:

```text
# Fresh run 1
PRED-C1-r26-v2 cases_pass=3/41 verdict=TARGET_MISSED
exit=1

# Fresh run 2
PRED-C1-r26-v2 cases_pass=5/41 verdict=TARGET_MISSED
exit=1
```

Strengthened and restored outputs, respectively:

```text
PRED-C1-r26-v2 cases_pass=5/41 verdict=TARGET_MISSED
exit=1

PRED-C1-r26-v2 cases_pass=5/41 verdict=TARGET_MISSED
exit=1
```

The L1's earlier `controls/v2/K1RootOnly.txt` scored 2/41 with seed `27b3c092d51dca93`. These new scores differ by fresh generated inputs, not by an altered control. Every passing case in the new runs is SYNTH: run 1 passes C35/C38/C39; run 2 passes C30/C32/C34/C35/C37. BASE, all 20 APPEND cases and all 10 EDIT cases fail in both runs. Every run prints this same BASE discrepancy:

```text
CASE BASE  FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 changed=base (unperturbed)
```

This preserves the observed target miss; it is not an exhaustive bound on every possible root-only reader. Unlike the w1 v1 population, v2 contains independent trees, so w1's snapshot-difference explanation must not be extended to every v2 case.

## One within-shape strengthening

Preserved the w1 shape (`w1/reports/K1RootOnly.md:5-7,50-60`): read only `DIR/.config/hypr/hyprland.conf`, never follow sources, no variables, no animation/bezier validation, simple last-wins over the unchanged embedded default table. No path/case-identity shortcuts or snapshot tables were added.

The plausible control defect is literal-only enabled-token handling: `controls/K1RootOnly.py:64` enables only the string `1`, although the Hyprland handler calls `ParserUtils::parseInt(...).value_or(0) == 1` (`fetch/SrcAnimConfig.bin:1437-1445`; prefix and numeric forms documented at `recon/anim-grammar.md:72-78`). Changed only that assignment in scratch:

```diff
-    enabled = enabled_field == "1"
+    enabled = enabled_field.startswith(("true", "on", "yes")) or re.fullmatch(
+        r"(?:0[xX])?0*1", enabled_field) is not None
```

This adds the enabled aliases/prefixes and zero-padded decimal/hex forms without rejecting invalid animation, speed or bezier entries. It does not add a source graph or variable expansion. It is a semantic strengthening attempt, not a claim that all hyprlang parsing is implemented.

Expected detector: the unchanged bounded C1 v2 counter, exact node/bezier set equality, target 41/41. Actual: the strengthened run remains 5/41; all printed case verdicts and discrepancy counts match same-seed run 2 and restoration. There is no measured score improvement. The generator uses literal enabled fields `0`/`1` and invalid `2` (`c1/count-v2.py:119-125,176-184,223-226`), so this probe does not demonstrate behavioral coverage of the added aliases.

Mutation-testing classification: **INCONCLUSIVE as a mutant-kill test**, not KILLED: the pristine control already misses the target. The re-score conclusion itself is the observed target miss above; no checker-sensitivity or surviving-defect claim is inferred from it.

## Exact commands

All counter commands used working directory `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Fresh run 1 (job `bg_4762`) and fresh run 2 (job `bg_4763`) each executed this exact command, with no explicit seed:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c1/count-v2.py 1b0b91e9 --tool-file .ufo/waves/round-26/controls/K1RootOnly.py --jobs 2
```

Strengthened run (`bg_4825`), then again after exact restoration (`bg_4850`):

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c1/count-v2.py 1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/rescore/RescoreK1RootOnly/K1RootOnly-probe.py --seed f2014abfe7d2ec52 --jobs 2
```

Disk-capacity check before scratch writes:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 10 df -h /fast
```

Output: `/dev/nvme1n1p2`, 804G size, 658G used, 146G available, 82% used.

Initial protected-file hashes:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 10 sha256sum .ufo/waves/round-26/controls/K1RootOnly.py .ufo/waves/round-26/c1/count-v2.py .ufo/waves/round-26/harness/oracle.py
```

Pristine and strengthened scratch hashes were each recorded using:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 10 sha256sum /fast/scratch/hyaku/mado-r26/rescore/RescoreK1RootOnly/K1RootOnly-probe.py
```

Restoration/protected-file hashes:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 10 sha256sum .ufo/waves/round-26/controls/K1RootOnly.py .ufo/waves/round-26/c1/count-v2.py .ufo/waves/round-26/harness/oracle.py /fast/scratch/hyaku/mado-r26/rescore/RescoreK1RootOnly/K1RootOnly-probe.py
```

## Hashes and restoration evidence

| Bytes | Before | After |
|---|---|---|
| Committed control | `42ae2fb5df5470b04e2a42eeaa216cb43e3771f24a5cce66d49ce08c0c4edcb0` | same |
| Frozen C1 v2 counter | `4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428` | same |
| Frozen oracle | `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441` | same |
| Isolated scratch probe | `42ae2fb5df5470b04e2a42eeaa216cb43e3771f24a5cce66d49ce08c0c4edcb0` | `42ae2fb5df5470b04e2a42eeaa216cb43e3771f24a5cce66d49ce08c0c4edcb0` |

Strengthened bytes, used for exactly one counter run: `b6e83f701876ecf9de798c845c9e7c6593598773d6efe86662a372ce71cd497c`. The restored counter receipt independently prints the original control SHA above, with the same-seed 5/41 result. Scratch now contains original bytes; the exact strengthening is retained as the diff above, not as a changed lane control.

All four receipts print snapshot files=79, digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`, `ORACLE_CHECK base_twice equal nodes=35 beziers=6`, and `ORACLE_VERSION commit=efb50993780079460b0cbed1363e2166a2de1d9f tag=v0.56.2`.

All four receipts print:

```text
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
```

Only the frozen counter/oracle started compositor instances. Oracle-wide locking enforces its 12-slot cap (`harness/oracle.py:109-125`); this seat requested two jobs per counter. No live-session commands, DRM card access, git/jj write operations, package installs/upgrades or long-lived services were started. All four bounded counter commands completed; the oracle's `finally` block terminates and waits for each sandbox process group (`harness/oracle.py:212-226`). Lane writes are confined to this requested report.

## Preserved output excerpts

These files contain selected verbatim stdout lines, not full receipts; the report includes all required PRED/exit lines:

- `/fast/scratch/hyaku/mado-r26/rescore/RescoreK1RootOnly/rescore-excerpts.txt`
- `/fast/scratch/hyaku/mado-r26/rescore/RescoreK1RootOnly/strengthened-excerpts.txt`
- `/fast/scratch/hyaku/mado-r26/rescore/RescoreK1RootOnly/restored-excerpts.txt`

No additional mutation or tool integration was performed.

RESCORE K1RootOnly not met (best 5/41)

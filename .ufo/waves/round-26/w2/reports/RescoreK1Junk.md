# RescoreK1Junk — C1 counter v2

RESCORE K1Junk not met (best 0/41)

## Scope and result

Axes: preserve the registered junk shape, challenge exact-table discrimination, use fresh counter seeds, preserve source bytes, and protect the operator session.

Re-scored the untouched committed `controls/K1Junk.py` twice under the frozen C1 v2 counter at revision `1b0b91e9889cbf984b052f5de564db78330a72aa`. Both scored `0/41`, exit 1. Then changed one behavior-bearing line in an isolated scratch copy, scored that attempted strengthening once, restored its exact original bytes, and ran the same bounded detector on the restored bytes. The strengthened and restored runs also scored `0/41`, exit 1. No run was a setup-error or oracle-guard result.

These results agree with the L1's prior v2 receipt (`controls/v2/K1Junk.txt`, seed `2cf510fb5f901dbe`, `0/41`, exit 1). They do not establish any data-tool result.

Paths abbreviated below are relative to `.ufo/waves/round-26/`, except the explicit scratch paths. The receipt directory is:

`/fast/scratch/hyaku/mado-r26/rescore/RescoreK1Junk/`

## Actual outputs and receipts

The following are the exact PRED and exit lines from the four runs. The process exit code was also 1 in every case.

| Run | Fresh counter seed | Full captured output |
| --- | --- | --- |
| Committed re-score 1 / pristine bytes | `d363da87819f15a5` | `rescore-1.txt` in the receipt directory |
| Committed re-score 2 / pristine bytes | `653af20b775a989d` | `rescore-2.txt` in the receipt directory |
| Strengthened scratch / mutated bytes | `4efd17b33a24b78c` | `strengthened.txt` in the receipt directory |
| Exact restored scratch | `c5b92d2c8054223d` | `restored.txt` in the receipt directory |

Committed re-score 1:

```text
PRED-C1-r26-v2 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```

Committed re-score 2:

```text
PRED-C1-r26-v2 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```

Strengthened scratch:

```text
PRED-C1-r26-v2 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```

Exact restored scratch:

```text
PRED-C1-r26-v2 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```

Every run printed these guards and safety results:

```text
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
ORACLE_VERSION commit=efb50993780079460b0cbed1363e2166a2de1d9f tag=v0.56.2
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
```

All 164 case outputs reached exact-set comparison, rather than failing JSON or output-shape validation. Every case reported `nodes missing=35`. The strengthened run's `C00` is an explicit cardinality-matching failure:

```text
CASE C00   FAIL nodes missing=35 extra=35 beziers missing=6 extra=2 changed=yes (APPEND:NEWSRC+INVALID)
```

## Single mutation / attempted strengthening

Scratch file: `/fast/scratch/hyaku/mado-r26/rescore/RescoreK1Junk/K1Junk.py`.

The w1 shape is defined in `w1/reports/K1Junk.md:8-14`: configuration-independent random animation-shaped JSON, random-length node and bezier arrays, every named field, finite numeric values, and random names/values. The committed implementation is `controls/K1Junk.py:10-40`.

Only line 38 of the scratch copy changed:

```diff
-        for _ in range(rng.randint(0, 64))
+        for _ in range(rng.choice((35, rng.randint(0, 64))))
```

This biases the random node count toward the 35-node cardinality reported by the baseline, while retaining every length from 0 through 64. The probability of generating 35 nodes becomes `33/65` instead of `1/65`. This is an attempted improvement in structural resemblance, not an observed improvement in cases passed. Random names, field values, bezier counts and references, CLI behavior, and the per-invocation `os.urandom(32)` seed are unchanged. It still never reads or inspects `--home`; it embeds no oracle table or config content and uses no case identity.

Expected detector: `c1/count-v2.py:256-265,349-361` compares exact sets of the six node fields and five bezier fields. Matching the number of nodes alone must not pass a case. Observed: no case passed, including cardinality-matching outputs.

Mutation-test classification: **INCONCLUSIVE for a killed/survived mutant claim**, because the pristine junk control already fails the detector. No killed-mutant credit is claimed. The assigned control result is conclusive: both committed re-scores and the within-shape strengthening missed the target. The contract was not changed.

## Exact scoring commands

Working directory for every counter command:

`/home/vgpnk/Projects/shokunin/mado-shokunin`

The following command ran twice, concurrently, without `--seed`:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c1/count-v2.py 1b0b91e9 --tool-file .ufo/waves/round-26/controls/K1Junk.py --jobs 1
```

The following command ran once with the mutated scratch bytes and once after exact restoration, again without `--seed`:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c1/count-v2.py 1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/rescore/RescoreK1Junk/K1Junk.py --jobs 1
```

Counter wall times reported by the command tool were 74.48 s, 115.75 s, 135.05 s and 103.13 s respectively; none reached the timeout. Each counter requested one worker; the unmodified harness retains its shared 12-slot host-wide oracle lock. The outer memory limit was soft 4 GB, hard 8 GB, allowing the oracle's own 8 GB cap.

## Hashes and exact restoration

The committed control, counter and harness were not edited. Hashes were captured before scoring and again after restoring the scratch file:

| File | Before = after SHA-256 |
| --- | --- |
| `controls/K1Junk.py` | `4919d9798ed37c3280545cd30cc5ead62714b0b094eee22fa3eb247c8e422ad3` |
| `c1/count-v2.py` | `4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428` |
| `harness/oracle.py` | `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441` |

Scratch bytes followed this sequence:

```text
pristine:  4919d9798ed37c3280545cd30cc5ead62714b0b094eee22fa3eb247c8e422ad3
mutated:   901e062cb78becaff23891bfcfa94466b7dbfe97ab87ed281d6049e62675adc1
restored:  4919d9798ed37c3280545cd30cc5ead62714b0b094eee22fa3eb247c8e422ad3
```

The restored detector receipt independently reports the restored tool hash. The scratch file now contains the original bytes, not the strengthening. Its one-line mutation and mutated hash above preserve the probe recipe.

Hash commands (each prefixed with `env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 15`):

```sh
sha256sum .ufo/waves/round-26/controls/K1Junk.py .ufo/waves/round-26/c1/count-v2.py .ufo/waves/round-26/harness/oracle.py
sha256sum /fast/scratch/hyaku/mado-r26/rescore/RescoreK1Junk/K1Junk.py
sha256sum .ufo/waves/round-26/controls/K1Junk.py /fast/scratch/hyaku/mado-r26/rescore/RescoreK1Junk/K1Junk.py .ufo/waves/round-26/c1/count-v2.py .ufo/waves/round-26/harness/oracle.py
```

## Host safety and scope boundaries

Before writing scratch files, `env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 15 df -h /fast` reported 146 GB available. Only bounded, small scratch files and this assigned report were written.

Every compositor invocation went through the frozen counter and oracle. No live-compositor command was issued. The oracle's cleanup path (`harness/oracle.py:203-226`) exits its private instance, terminates its sandbox process group and waits for it. All four counters terminated. A final bounded process listing, run after all four finished with both display variables removed from its environment, used:

```sh
timeout 15 prlimit --as=4000000000 -- ps -eo pid=,ppid=,args=
```

Its process exit was 0, stderr was empty, and filtering command lines for the assigned committed control path or scratch directory returned `matching_processes: []`. No remaining assigned counter/control process was found.

No git/jj write command, tool installation/update, production-tool edit, counter/harness edit, sibling-file edit, build, lint or unrelated test was performed. Apart from the required report, lane files were left untouched.

RESCORE K1Junk not met (best 0/41)

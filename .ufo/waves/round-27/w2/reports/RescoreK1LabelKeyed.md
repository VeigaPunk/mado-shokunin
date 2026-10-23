# K1LabelKeyed fresh-seed re-score

RESCORE K1LabelKeyed best: PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED — not met

## Scope and result

Axes: counter score, metadata-only shape purity, restoration, and host safety. Read the registration first. Ran the exact assigned committed-control command twice with fresh counter-generated seeds. Both runs passed BASE only: BASE=1/1, APPEND=0/25, SYNTH=0/15. Both exited 1, stderr empty, with no setup guard.

The committed control is **not the strongest metadata classifier**: after its exact BASE fingerprint fails, it can still classify a snapshot-backed tree as BASE solely because its timestamp test fails. I tested a one-line, within-shape strengthening of that fallback. It changed all APPEND guesses to the nonempty canned answer, but improved no case score. The strongest tested variant therefore ties the original at 1/41. This is not a proof of global optimality for every possible label-keyed control.

No workspace configuration bytes were added to the control's inputs. No rule parsing, source traversal, variable evaluation, or oracle invocation was added to it.

## Assigned fresh-seed outputs

Receipts are verbatim counter stdout under `/fast/scratch/hyaku/mado-r27/rescore/`.

| Receipt | Fresh seed | Actual output | Exit |
| --- | --- | --- | --- |
| `K1LabelKeyed-seed1.txt` | `c50698a36777a153` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` | 1 |
| `K1LabelKeyed-seed2.txt` | `a7a643838ef3aa1e` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` | 1 |

```text
PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED
PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED
```

Working directory for every score: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Exact command, run twice concurrently without `--seed`:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1LabelKeyed.py --jobs 6
```

Both resolved revision `2fdca5caaab6859386effbb8fa6acc5250c90633`, confirmed equal zero-rule BASE oracle runs and oracle commit `efb50993780079460b0cbed1363e2166a2de1d9f`, tag `v0.56.2`. Every new receipt recorded the same 79-file snapshot digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`.

### Historical comparison

The requested `controls/v4/K1LabelKeyed-seed*.txt` paths are actually **v4** receipts, despite the assignment calling them v3. Their headers pin counter `635ae788fd897c8f1fba88e4ab2ffcb95e7f79a88703b82e49a8729ce7d271a1`. Both old v4 runs, seeds `c25ff0dec8e839fb` and `61d7575c67c5ad6d`, likewise printed `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED`, BASE only. The w1 report records `--jobs 4`; this re-score used the assigned `--jobs 6`.

I also read the actual `controls/v3/K1LabelKeyed-seed{1,2}.txt` receipts: seeds `b04c013dca3881dd` and `adaaa716bb5a1980`, each `PRED-C1-r27-v3 cases_pass=1/41 verdict=TARGET_MISSED`, BASE only. Thus neither the requested historical v4 comparison nor the actual historical v3 comparison changes the observed score.

## Single within-shape mutation probe

Made an exact isolated copy at `/fast/scratch/hyaku/mado-r27/rescore/K1LabelKeyed-metadata-stronger.py`. The only mutation was line 95 in `guess_label`:

```diff
-        return "BASE"
+        return "APPEND"
```

This branch is reached only after no visible label was found, the exact BASE name/size fingerprint failed, snapshot-family metadata was present, and the timestamp heuristic failed. The earlier exact-fingerprint BASE return remains intact. Canned arrays, metadata/proc channels, and all bounds remain unchanged.

Expected detector: frozen v4's type-strict, ordered JSON-array equality against pinned isolated Hyprland v0.56.2. Merely recognizing a family does not supply generated selectors, rule values, merge results, or order.

Scored the changed bytes on the first pristine seed for a matched comparison and on another fresh seed. Restored the exact original bytes in a `finally` block, then scored the restored bytes on the matched seed. The retained tested variant is `/fast/scratch/hyaku/mado-r27/rescore/K1LabelKeyed-metadata-candidate.py`, SHA-256 `d497ef665c8ef9a401e7f62b986f68bd6d8366b1e41ff9a2f67a423623c333a1`.

| Receipt | State | Seed | Actual output | Exit |
| --- | --- | --- | --- | --- |
| `K1LabelKeyed-metadata-matched-seed.txt` | Changed | `c50698a36777a153` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` | 1 |
| `K1LabelKeyed-metadata-fresh-seed.txt` | Changed | `9788539cd9028773` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` | 1 |
| `K1LabelKeyed-restored-matched-seed.txt` | Restored | `c50698a36777a153` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` | 1 |

Every probe passed BASE only; stderr was empty and there was no setup guard. The original first-seed run emitted empty guesses on 17/25 APPEND cases; the changed matched-seed run emitted its nonempty canned guess on all 25. Neither guess was correct for any APPEND case. The restored same-seed run emitted empty guesses on 24/25 APPEND cases: timestamps/random scratch metadata vary between runs even for the same generated config seed, while the counter score remained unchanged.

**Mutation-test verdict: inconclusive, not a killed mutant.** The pristine control already fails the detector, so its unchanged nonzero result cannot establish a mutant kill. **Re-score verdict: target not met** by either the original or the strengthened classifier.

Exact changed-byte commands:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /fast/scratch/hyaku/mado-r27/rescore/K1LabelKeyed-metadata-stronger.py --jobs 6 --seed c50698a36777a153
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /fast/scratch/hyaku/mado-r27/rescore/K1LabelKeyed-metadata-stronger.py --jobs 6
```

Exact restored-byte command:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /fast/scratch/hyaku/mado-r27/rescore/K1LabelKeyed-metadata-stronger.py --jobs 6 --seed c50698a36777a153
```

## Integrity and restoration

| File/state | SHA-256 |
| --- | --- |
| Committed `controls/K1LabelKeyed.py`, before = after | `1fb107df8d51811145da3fa12e2e1b01349ad295b5fcff1f34ca491c7d718c72` |
| Isolated copy, pristine = restored | `1fb107df8d51811145da3fa12e2e1b01349ad295b5fcff1f34ca491c7d718c72` |
| Isolated copy, changed; retained candidate | `d497ef665c8ef9a401e7f62b986f68bd6d8366b1e41ff9a2f67a423623c333a1` |
| `c1/count-v4.py`, before = after | `635ae788fd897c8f1fba88e4ab2ffcb95e7f79a88703b82e49a8729ce7d271a1` |
| `harness/oracle.py`, before = after | `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601` |

The restored isolated copy was also compared byte-for-byte with its pristine saved bytes: equal. No committed control, counter, harness, configuration, or sibling source was edited. The only lane write is this report. No git/jj write command or subagent dispatch was used.

Receipt SHA-256:

| Receipt | SHA-256 |
| --- | --- |
| `K1LabelKeyed-seed1.txt` | `53c0418a417cde0fbbf23fe25b8b587e93fdfbe84e416af4a7a884e04c541465` |
| `K1LabelKeyed-seed2.txt` | `2f80a0c1c1faad8547457f8b9d3cb54e9dd05777c5b9ddaa0b13628c6875329a` |
| `K1LabelKeyed-metadata-matched-seed.txt` | `2531fc8352b3e655f5ce78ab4fe00f2f9bbac3c3dfb87ad022dbabf666b76908` |
| `K1LabelKeyed-metadata-fresh-seed.txt` | `c4c39cfccdbb58e75b8da1608cad427a5a81829b1eb876b0a1dab8d2e4ffd1e2` |
| `K1LabelKeyed-restored-matched-seed.txt` | `d496e1a91fcc8911f54e617889e3e88aac05f24d0f47c746c9a8dd4d11cddc86` |

The first two counters completed before their background receipt-writing calls encountered an eval tool-bridge lifetime error. Recovered their exact completed stdout/stderr from the saved task exception frames and wrote the receipts without replaying either counter. The tool issue was reported through `xd://report_issue`; no detector run was lost or fabricated.

## Host safety and tooling

Before scoring, `env -i PATH=/usr/bin HOME=/home/vgpnk timeout 10 prlimit --as=4000000000 -- df -h /fast` reported 73G available. No large files were written.

Independent before/after command:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 --core=0 -- coredumpctl list --no-pager --no-legend
```

Both commands exited 0 with empty stderr. Counting stdout lines containing `/usr/bin/Hyprland` gave **before=1338, after=1338, own delta=0**. Every counter receipt also printed `HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0`.

Only the frozen counter invoked the pinned oracle. Its flock-based 12-slot limiter governs host-wide compositor concurrency and its finalizer owns nested process teardown. All five counter processes were awaited and exited 1; no persistent service was started. Commands started with cleared environment, without inherited WAYLAND_DISPLAY or HYPRLAND_INSTANCE_SIGNATURE. No live-compositor command, direct Hyprland launch, DRM card-node access, known-crash input, or network request was made.

No tools were installed or updated. No additional mutation probes or implementation verification were run.

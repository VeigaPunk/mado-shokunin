# RescoreK1StaticDefault — C1 counter v2

## Result

Both required fresh-seed re-scores of the unchanged committed control returned **0/41, TARGET_MISSED, exit 1**. The within-shape refresh/canonicalization attempt also returned **0/41, exit 1**. An additional restored-bytes run returned **0/41, exit 1**. No run exited 2 or timed out.

Axes: frozen-counter evidence, strict STATIC DEFAULT shape, isolated host execution, and exact byte restoration. No subagents were dispatched.

| Run | Fresh seed | PRED result | Counter/process exit |
| --- | --- | --- | --- |
| Committed control, re-score 1 | `c310cb7710f898ab` | `cases_pass=0/41 verdict=TARGET_MISSED` | 1 / 1 |
| Committed control, re-score 2 | `86dae59f155e2f47` | `cases_pass=0/41 verdict=TARGET_MISSED` | 1 / 1 |
| Refreshed/canonical static attempt | `1bde68c48abf38f3` | `cases_pass=0/41 verdict=TARGET_MISSED` | 1 / 1 |
| Exactly restored scratch control | `c8fc3d981647d5b4` | `cases_pass=0/41 verdict=TARGET_MISSED` | 1 / 1 |

The two required receipts' PRED lines and exits, verbatim:

```text
PRED-C1-r26-v2 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```

```text
PRED-C1-r26-v2 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```

Strengthening-attempt receipt, verbatim:

```text
PRED-C1-r26-v2 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```

The L1's prior v2 receipt also scored 0/41, seed `55e6ecd78d9546b8`; it was read, not rewritten or counted as either fresh re-score.

## Control fault, detector, and shape-constrained attempt

**Control fault:** ignore all configuration bytes and replay the true minimal-config Hyprland default table. **Expected detector:** the unchanged C1 v2 counter compares animation-node and bezier sets against isolated Hyprland for BASE plus 20 APPEND, 10 EDIT, and 10 SYNTH cases. The default control must miss whenever that tree differs from the no-animation-directive defaults.

The w1 shape is specifically the true minimal-config default, not an arbitrary constant or the operator snapshot (`w1/reports/K1StaticDefault.md:10,14,19-30,76-80`). I did not relax that shape into a snapshot cache, config reader, or source/variable interpreter.

I created an exact scratch copy at `/fast/scratch/hyaku/mado-r26/rescore/RescoreK1StaticDefault/K1StaticDefault.py` and independently refreshed the defaults once through the pinned oracle using a 67-byte config containing only:

```conf
ecosystem {
    no_update_news = true
    no_donation_nag = true
}
```

The capture requested `animations` and `version`. Actual output included:

```text
ORACLE_PIN sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
SCRATCH_BEFORE sha256:6a864aeb510de59cc568947eb647ad3f3b7bdcdc414a115453da4b46d1783e2a
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
ORACLE_VERSION commit=efb50993780079460b0cbed1363e2166a2de1d9f tag=v0.56.2
REFRESH_COUNTS nodes=35 beziers=2
DEFAULT_SET_EQUAL True
DEFAULT_CANONICAL_SHA256 0fe6603d476dec77c91be9de11e2065cf66adea65d26716507f8733ae7d66f41
exit=0
```

The full capture, including `DEFAULT_TABLE`, is retained in `default-refresh.txt`; its exact acquisition command, including the inline Python, is retained in `default-refresh.command.txt` under the scratch evidence directory below.

No stale or incomplete default tuple was found. The scored attempt therefore retained every captured value and changed only `import argparse` to `import argparse, json`, and the final print to:

```python
print(json.dumps([sorted(rows, key=lambda entry: entry["name"]) for rows in json.loads(DEFAULT_JSON)], sort_keys=True, separators=(",", ":")))
```

This remains a fixed true-default replay and never reads `--home`. It removes capture-order/serialization variability but is **not a behavioral strengthening** under this detector: `count-v2.py:256-261,358-361` compares sets, not serialization order. Its one scored run found no improvement. [INFERENCE] With all default tuples fixed by the pinned runtime, changing configuration-dependent tuples or interpreting input to gain passes would leave this strict control shape; no such change was made.

**Mutation verdict: INCONCLUSIVE as a mutation kill.** The pristine control already fails the detector, so neither the candidate's failure nor the restored failure establishes a killed mutant. The canonicalization itself is set-equivalent, not a behavior-changing survivor or a coverage finding. The re-score verdict is independently definitive for these sampled runs: target not met.

## Actual bounded commands

Working directory for every counter command: `/home/vgpnk/Projects/shokunin/mado-shokunin`. No `--seed` was supplied; the frozen counter generated the four distinct seeds shown above. `--jobs 1` limited each counter's oracle concurrency; the unchanged harness also enforces its host-wide twelve-slot bound.

The following exact command ran twice, unchanged, for the required re-scores:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout --kill-after=15s 900s prlimit --as=4000000000:8000000000 --core=0 -- python3 -I -B .ufo/waves/round-26/c1/count-v2.py 1b0b91e9 --tool-file .ufo/waves/round-26/controls/K1StaticDefault.py --jobs 1
```

The following exact command ran once on candidate bytes, then once after exact restoration of the same path:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout --kill-after=15s 900s prlimit --as=4000000000:8000000000 --core=0 -- python3 -I -B .ufo/waves/round-26/c1/count-v2.py 1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/rescore/RescoreK1StaticDefault/K1StaticDefault.py --jobs 1
```

All four receipts identify revision `1b0b91e9889cbf984b052f5de564db78330a72aa`, snapshot `files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`, a stable double-BASE oracle result of 35 nodes / 6 beziers, and nested Hyprland commit `efb50993780079460b0cbed1363e2166a2de1d9f`, tag `v0.56.2`.

All four BASE results were:

```text
CASE BASE  FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 changed=base (unperturbed)
```

Every generated case also failed. Re-score 1 included an unchanged APPEND case (`C12`, `changed=no`); that still failed because the default table already differs from BASE. These receipts do not establish behavior for untested seeds or other implementations.

## Hashes and restoration

| Artifact/state | SHA-256 |
| --- | --- |
| Committed control, before and after | `6a864aeb510de59cc568947eb647ad3f3b7bdcdc414a115453da4b46d1783e2a` |
| Exact initial scratch copy | `6a864aeb510de59cc568947eb647ad3f3b7bdcdc414a115453da4b46d1783e2a` |
| Scored canonicalization candidate | `8118369fa3b4b048095b67b8c65cdfd64d318ef8abc6ea64ab46e5ab2b297fff` |
| Restored scratch copy, including restored counter's tool hash | `6a864aeb510de59cc568947eb647ad3f3b7bdcdc414a115453da4b46d1783e2a` |
| Frozen `c1/count-v2.py`, before/after and all receipts | `4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428` |
| Frozen `harness/oracle.py`, before/after and all receipts | `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441` |

The two changed scratch lines were restored with the edit tool before the restored detector run. The original and restored file snapshots also had the same tool snapshot tag `EF7E`. The candidate's exact 3917-byte source is retained separately as `canonical-static.py`; the restored control is 3788 bytes. A raw-read tool omitted a trailing newline when archiving the candidate; the evidence copy was corrected to the scored hash above and the tool issue was reported. This did not change either scored input.

The final hash command was:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 30s prlimit --as=4000000000:8000000000 --core=0 -- sha256sum /fast/scratch/hyaku/mado-r26/rescore/RescoreK1StaticDefault/K1StaticDefault.py /fast/scratch/hyaku/mado-r26/rescore/RescoreK1StaticDefault/canonical-static.py .ufo/waves/round-26/controls/K1StaticDefault.py .ufo/waves/round-26/c1/count-v2.py .ufo/waves/round-26/harness/oracle.py
```

It printed the corresponding hashes in the table. The restored counter subsequently printed the restored control hash and unchanged counter/oracle pins again.

## Retained output evidence

All filenames below are relative to `/fast/scratch/hyaku/mado-r26/rescore/RescoreK1StaticDefault/`. Counter receipt files preserve the actual completed-job output, including the tool's job/status wrapper, full counter stdout, wall time, and process-exit evidence. They are not reconstructed counter runs.

| Receipt | Bytes | SHA-256 |
| --- | ---: | --- |
| `pristine-1.txt` | 5827 | `c136bc292ea03b8cbf307250d80b1d50d5cd6545f28cdf7252ef3abbb79b260f` |
| `pristine-2.txt` | 5792 | `18375be51330ce40b1f8c3ccfa4783c789e28edaee7253e3826f8c8349465c67` |
| `canonical-static.txt` | 5883 | `456eb50001f39547630f6772ee0eb2f9117673edf33dd25ffd17ba34dce452dc` |
| `restored.txt` | 5745 | `47340f6a611b1beb6a11d0e832e342cfd59ce6d107109bf43826cac2c63d5592` |
| `default-refresh.txt` | 3820 | `9b21835e1b770bc68c6e8139788b21339b81f3c46f9689df1471153bdc23ae2d` |

`default-refresh.command.txt` records the exact acquisition command; `canonical-static.py` preserves the scored candidate, and `K1StaticDefault.py` is restored to the committed bytes. The lane control, counters, harness, and existing receipts were never edited. The only lane write is this scoped report.

## Safety and cleanup

The oracle capture and all four counter runs each reported `hyprland_coredumps_before=1335 after=1335 delta=0`. Every compositor launch went through the unchanged oracle; no live-session `hyprctl` command or DRM card-node operation was issued. The launched counter/capture commands all returned. The pinned oracle's `finally` terminates and waits for each sandbox process group (`harness/oracle.py:212-226`). No independent process-residue census was run.

`df -h /fast` reported 146G available before the scratch fixture was created. Only this seat's no-longer-needed oracle tree and minimal fixture were removed, with the command below; it returned with no output:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 30s prlimit --as=4000000000:8000000000 --core=0 -- rm -r -- /fast/scratch/hyaku/mado-r26/rescore/RescoreK1StaticDefault/oracle /fast/scratch/hyaku/mado-r26/rescore/RescoreK1StaticDefault/home
```

No git/jj write commands, model calls, package installs or updates, builds, linters, formatters, or unrelated tests were run.

RESCORE K1StaticDefault not met (best 0/41)

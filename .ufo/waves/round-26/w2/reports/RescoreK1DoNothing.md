# RescoreK1DoNothing — round 26, wave w2

RESCORE K1DoNothing not met (best 0/41)

## Scope and method

Axes: fresh-seed reproducibility, fidelity to the registered do-nothing shape, host safety, and exact-byte restoration.

Re-scored the committed `controls/K1DoNothing.py` twice under frozen C1 counter v2 at revision `1b0b91e9889cbf984b052f5de564db78330a72aa`, using a byte-identical isolated scratch copy. Both original runs omitted `--seed`, so the counter drew independent fresh seeds. Only after both finished, tried the zero-byte representation explicitly allowed by the w1 report (`w1/reports/K1DoNothing.md:14-20,375-381`). This removes all import and executable-code dependencies while retaining exit 0, no config reads, and empty stdout. It is a strengthening attempt within the allowed shape, not a claim of improved score.

Restored the scratch copy immediately after that trial, then ran the same detector on restored bytes. Trial and restoration reused the first original seed to pair identical generated cases; they are not additional independent-seed re-scores. No lane control, counter, harness, or sibling source was edited. The only lane write is this report.

All relative paths below are relative to `.ufo/waves/round-26/` unless stated otherwise. Scratch directory:

`/fast/scratch/hyaku/mado-r26/rescore/RescoreK1DoNothing/`

## Results

| Run | Tool form | Seed | cases_pass | Actual exit | Wall time | Coredumps before → after |
|---|---|---|---|---|---|---|
| R1, pristine | committed bytes | `64cf547cc02682ea` | 0/41 | 1 | 98.01 s | 1335 → 1335 |
| R2, pristine | committed bytes | `d2814d80ebbf96bd` | 0/41 | 1 | 91.77 s | 1335 → 1335 |
| S, strengthening attempt | zero-byte module | `64cf547cc02682ea` | 0/41 | 1 | 44.53 s | 1335 → 1335 |
| R, restored | committed bytes | `64cf547cc02682ea` | 0/41 | 1 | 33.72 s | 1335 → 1335 |

Every run printed these actual guard/safety outputs:

```text
ORACLE_CHECK base_twice equal nodes=35 beziers=6
ORACLE_VERSION commit=efb50993780079460b0cbed1363e2166a2de1d9f tag=v0.56.2
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
```

Every case, including BASE, failed with `stdout is not JSON`. These were measured target misses, not setup/guard failures. All four runs used the same 79-file snapshot digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`.

Required re-score receipt lines, verbatim:

```text
R1 seed=64cf547cc02682ea
PRED-C1-r26-v2 cases_pass=0/41 verdict=TARGET_MISSED
exit=1

R2 seed=d2814d80ebbf96bd
PRED-C1-r26-v2 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```

Strengthening and restoration receipt lines, verbatim:

```text
S seed=64cf547cc02682ea
PRED-C1-r26-v2 cases_pass=0/41 verdict=TARGET_MISSED
exit=1

R seed=64cf547cc02682ea
PRED-C1-r26-v2 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```

The R1/R2/S/R labels above identify the receipt; the `seed=…`, PRED, and exit values are the recorded outputs. Complete counter stdout, including `exit=`, and the exact counter command are preserved respectively at:

- `/fast/scratch/hyaku/mado-r26/rescore/RescoreK1DoNothing/rescore-1.txt`
- `/fast/scratch/hyaku/mado-r26/rescore/RescoreK1DoNothing/rescore-2.txt`
- `/fast/scratch/hyaku/mado-r26/rescore/RescoreK1DoNothing/strengthened.txt`
- `/fast/scratch/hyaku/mado-r26/rescore/RescoreK1DoNothing/restored.txt`

The L1's existing v2 receipt (`controls/v2/K1DoNothing.txt`, seed `51079a2e80d17591`) also records 0/41, exit 1. The fresh re-scores agree with that result.

## Exact detector commands

Working directory for every command: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

R1 and R2 ran concurrently against unchanged scratch bytes, with this exact command once each:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c1/count-v2.py 1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/rescore/RescoreK1DoNothing/K1DoNothing.py --jobs 2
```

S and R ran sequentially, once each, with this exact command (zero bytes for S; restored bytes for R):

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c1/count-v2.py 1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/rescore/RescoreK1DoNothing/K1DoNothing.py --jobs 2 --seed 64cf547cc02682ea
```

## Mutation interpretation and restoration evidence

Trial/mutant: an accidentally truncated, zero-byte no-op tool, replacing only this seat's scratch copy. Expected detector: the frozen v2 counter. `harness/oracle.py:238-244` parses stdout with `json.loads` and returns `stdout is not JSON` for empty stdout; `c1/count-v2.py:349-352` consequently rejects the case before table equality is considered. No score-improving implementation can retain the strict no-output shape through this path. Emitting a table would leave the assigned shape.

Observed output: pristine, truncated, and restored tools all scored 0/41 with the same per-case reason. **Mutation-kill verdict: INCONCLUSIVE**, not killed or survived: the pristine negative control itself fails the detector, and truncating this particular no-op is behaviorally equivalent. The valid finding is continued rejection of both allowed do-nothing representations, not evidence of animation-parser coverage.

| Bytes | Size | SHA-256 |
|---|---|---|
| Committed control, before and after | 721 B | `a3e814b76c2154e086e272b57abc3f4d9726f127b0ee6db8f5286b19c3e48a94` |
| Scratch copy before trial | 721 B | `a3e814b76c2154e086e272b57abc3f4d9726f127b0ee6db8f5286b19c3e48a94` |
| Truncated scratch trial | 0 B | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| Restored scratch copy | 721 B | `a3e814b76c2154e086e272b57abc3f4d9726f127b0ee6db8f5286b19c3e48a94` |

Both before and after hash commands observed these unchanged pins:

- `c1/count-v2.py`: `4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428`
- `harness/oracle.py`: `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441`

The post-restoration hash command was:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 10 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-26/controls/K1DoNothing.py /fast/scratch/hyaku/mado-r26/rescore/RescoreK1DoNothing/K1DoNothing.py .ufo/waves/round-26/c1/count-v2.py .ufo/waves/round-26/harness/oracle.py
```

It printed the hashes in the table/list above. The restored counter receipt independently prints the restored tool hash.

## Safety and limits

- `df -h /fast` before writes showed 146 G available (82% used). Only small bounded source/receipt/report files were written.
- Display/session identifiers were removed for commands. The frozen harness alone started and stopped nested compositors; no live-compositor mutation command was issued. The harness enforces its shared 12-slot limit. This seat used at most four concurrent oracle workers during R1/R2, then two.
- All four counter processes completed normally with exit 1; each harness instance uses process-group teardown in `harness/oracle.py:212-226`. Afterward this exact scoped scan returned no output, exit 1 (no matching counter process):

  ```sh
  env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 10 prlimit --as=4000000000 -- /usr/bin/pgrep -af 'python3.*[/]fast/scratch/hyaku/mado-r26/rescore/RescoreK1DoNothing/K1DoNothing.py'
  ```

- The editor warned that the intended zero-byte Python module was a syntax error. The file was re-read, its empty-file hash was observed, and the actual detector run rejected empty stdout rather than reporting a tool execution error. The inconsistent editor diagnostic was reported through `xd://report_issue`.
- No installs, updates, commits, integrations, builds, linters, or unrelated checks were performed.

RESCORE K1DoNothing not met (best 0/41)

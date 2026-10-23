# RescoreK1NoValidation — C1 counter v2

RESCORE K1NoValidation not met (best 1/41)

## Scope and result

Axes: fresh-seed counter evidence, fidelity to the frozen no-validation shape, and host isolation. No lane source, control, counter, harness, or committed receipt was edited. The only lane write is this report. Scratch evidence is under `/fast/scratch/hyaku/mado-r26/rescore/RescoreK1NoValidation/` (abbreviated `SCRATCH` below).

The committed control was re-scored twice, without edits, and a scratch-only source-graph strengthening was scored once. All three measurements returned `TARGET_MISSED` with actual process exit 1; none hit a setup guard. This agrees with the L1's prior v2 miss (0/41, seed `2369b5294684134e`, `.ufo/waves/round-26/controls/v2/K1NoValidation.txt`). It is a negative-control result, not a result for a complete animation resolver.

| Run | Tool | Fresh seed | Exact predicate line | Receipt exit / process exit |
|---|---|---|---|---|
| 1 | Committed, unchanged | `dadf947e5c419fa3` | `PRED-C1-r26-v2 cases_pass=0/41 verdict=TARGET_MISSED` | `exit=1` / 1 |
| 2 | Committed, unchanged | `4df7171cbe1d8b82` | `PRED-C1-r26-v2 cases_pass=0/41 verdict=TARGET_MISSED` | `exit=1` / 1 |
| Strengthened | File-relative source resolution only | `1e30c51161c2c330` | `PRED-C1-r26-v2 cases_pass=1/41 verdict=TARGET_MISSED` | `exit=1` / 1 |

The strengthened run's sole pass was:

```text
CASE C09   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:SPACING+COMMENT+VARIABLE+CATEGORY)
```

The seeds differ, so the score difference is not evidence that the source-resolution change caused that pass. The separate fixed-tree diagnostic below establishes the limited improvement directly.

All three receipts reported:

```text
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
ORACLE_VERSION commit=efb50993780079460b0cbed1363e2166a2de1d9f tag=v0.56.2
CASE BASE  FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 changed=base (unperturbed)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
```

## Commands and retained receipts

Working directory for every command: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

The exact counter command below was executed twice (no `--seed`, so each counter generated its own fresh seed):

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 900 prlimit --as=4000000000:8000000000 --core=0 -- python3 -I -B /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/c1/count-v2.py 1b0b91e9 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1NoValidation.py --jobs 1
```

Strengthened command, executed once before restoration:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 900 prlimit --as=4000000000:8000000000 --core=0 -- python3 -I -B /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/c1/count-v2.py 1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/rescore/RescoreK1NoValidation/K1NoValidation.py --jobs 1
```

`SCRATCH/rescore.py` launched those commands with captured stdout/stderr, retained the command arrays and actual return codes, and measured before/after file hashes. Its exact outer invocations were:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 1000 prlimit --as=4000000000:8000000000 --core=0 -- python3 -I -B /fast/scratch/hyaku/mado-r26/rescore/RescoreK1NoValidation/rescore.py run1
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 1000 prlimit --as=4000000000:8000000000 --core=0 -- python3 -I -B /fast/scratch/hyaku/mado-r26/rescore/RescoreK1NoValidation/rescore.py run2
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 1000 prlimit --as=4000000000:8000000000 --core=0 -- python3 -I -B /fast/scratch/hyaku/mado-r26/rescore/RescoreK1NoValidation/rescore.py strengthened /fast/scratch/hyaku/mado-r26/rescore/RescoreK1NoValidation/K1NoValidation.py
```

The first two invocations were concurrent; each counter had only one worker. All compositor calls used the harness's shared host-wide slot locks.

Verbatim stdout, including each final `exit=1`, is retained at the following absolute-path suffixes under `SCRATCH`:

| Receipt | SHA-256 of verbatim stdout | Metadata |
|---|---|---|
| `run1.stdout` | `960dcdecd2077105d0f88c5689c5c066d4cf0b6ff1a2e3bb0010f4befa0a314e` | `run1.json` |
| `run2.stdout` | `479b2004d9da32ec12405672a5658210a128eb80336d4251f945f53d6c7cbae8` | `run2.json` |
| `strengthened.stdout` | `8f009bc176eb8cba9c3d282b2d93815ac9c3a69af58781e948e6ccf29496e481` | `strengthened.json` |

The corresponding `run1.stderr`, `run2.stderr`, and `strengthened.stderr` are empty (SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). All receipts resolved REV to `1b0b91e9889cbf984b052f5de564db78330a72aa`.

## Strengthening within the assigned shape

The w1 report (`w1/reports/K1NoValidation.md:10-13`) requires a source-graph/variable reader, applying every directive without validating or canonicalizing its fields. Its source handler incorrectly resolves non-absolute, non-tilde paths against `--home`, rather than the including file's directory. The opened Hyprland handler resolves against `m_configCurrentPath` and updates/restores that path around each included file (`fetch/SrcAnimConfig.bin:1816,1825,1835-1840`).

Only three statements changed in the isolated scratch copy:

```diff
-                self.source(value, depth)
+                self.source(value, depth, os.path.dirname(path))
-    def source(self, pattern, depth):
+    def source(self, pattern, depth, basedir):
-            pattern = os.path.join(self.home, pattern)
+            pattern = os.path.join(basedir, pattern)
```

No changes to default tables, animation/bezier handlers, raw field values, last-wins ordering, variable handling, comments, or category rules. In particular, the attempt did **not** repair the disabled-line encoding or numeric formatting that w1 explicitly excludes from this control shape (`w1/reports/K1NoValidation.md:13,71-78`).

### Same bounded detector on pristine, changed, and restored bytes

`SCRATCH/shape_probe.py` uses the pinned oracle and its tool sandbox on one fixed four-file relative-source tree: root sources `conf.d/first.conf`, which defines a curve and variables, then sources `nested/*.conf`; the glob's files set `windows` and `fade`. All values are well formed and use exactly representable, short decimals. The oracle comparison checks the same node/bezier fields as C1. A second fixed tree checks that unknown nodes and beziers, enabled `2`, negative speed, raw disabled fields, and short beziers remain accepted exactly as the original no-validation reader accepts them.

Exact commands:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 240 prlimit --as=4000000000:8000000000 --core=0 -- python3 -I -B /fast/scratch/hyaku/mado-r26/rescore/RescoreK1NoValidation/shape_probe.py pristine /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1NoValidation.py
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 240 prlimit --as=4000000000:8000000000 --core=0 -- python3 -I -B /fast/scratch/hyaku/mado-r26/rescore/RescoreK1NoValidation/shape_probe.py strengthened /fast/scratch/hyaku/mado-r26/rescore/RescoreK1NoValidation/K1NoValidation.py
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 240 prlimit --as=4000000000:8000000000 --core=0 -- python3 -I -B /fast/scratch/hyaku/mado-r26/rescore/RescoreK1NoValidation/shape_probe.py restored /fast/scratch/hyaku/mado-r26/rescore/RescoreK1NoValidation/K1NoValidation.py
```

Actual outputs:

```text
{"beziers_extra": 0, "beziers_missing": 1, "nodes_extra": 2, "nodes_missing": 2, "raw_shape_preserved": true, "relative_source_match": false, "stage": "pristine", "tool_sha256": "ca9ba0c963410221db80092a1b6adfb0d5e40685cfa480eecc555aef6e33bcb5"}
exit=1
{"beziers_extra": 0, "beziers_missing": 0, "nodes_extra": 0, "nodes_missing": 0, "raw_shape_preserved": true, "relative_source_match": true, "stage": "strengthened", "tool_sha256": "cb7a1813bd8959bc21ff6df8fef9a381155702772309c8205d41fb38116c4bfe"}
exit=0
{"beziers_extra": 0, "beziers_missing": 1, "nodes_extra": 2, "nodes_missing": 2, "raw_shape_preserved": true, "relative_source_match": false, "stage": "restored", "tool_sha256": "ca9ba0c963410221db80092a1b6adfb0d5e40685cfa480eecc555aef6e33bcb5"}
exit=1
```

The JSON outputs are retained as `shape-pristine.json`, `shape-strengthened.json`, and `shape-restored.json`; oracle work directories and input trees are also retained under `SCRATCH`. This demonstrates the limited source-resolution improvement while preserving non-validation. **Mutation-kill interpretation: inconclusive, not killed**, because the pristine detector already fails. No killed-mutant claim is made. The diagnostic also bounds w1's “correct source-graph reader” statement: its positive tree did not establish support for file-relative sources.

The restored detector's first asynchronous launch was refused by the global background-job cap before execution; the identical command then ran synchronously and returned the output above. This was not a counter guard or an additional measurement.

## Restoration and unchanged-byte evidence

The scratch control was restored from the exact original text after the strengthened counter and strengthened diagnostic completed. The restored file is 7,459 bytes, and the restored detector observed the original hash. The three-stage scratch hashes are:

```text
pristine   ca9ba0c963410221db80092a1b6adfb0d5e40685cfa480eecc555aef6e33bcb5
changed    cb7a1813bd8959bc21ff6df8fef9a381155702772309c8205d41fb38116c4bfe
restored   ca9ba0c963410221db80092a1b6adfb0d5e40685cfa480eecc555aef6e33bcb5
```

Initial and final `sha256sum` commands, plus each counter run's before/after metadata, observed these unchanged lane hashes:

| Lane file | Before = after SHA-256 |
|---|---|
| `controls/K1NoValidation.py` | `ca9ba0c963410221db80092a1b6adfb0d5e40685cfa480eecc555aef6e33bcb5` |
| `c1/count-v2.py` | `4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428` |
| `harness/oracle.py` | `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441` |
| `controls/v2/K1NoValidation.txt` | `72aba8f5fc36310751b136259f06e5c6abca208f7b7055fefdbf33155f2d1f2f` |

Paths in that table are relative to `.ufo/waves/round-26/`.

## Host safety and limits

- All nested Hyprland instances were started exclusively by the pinned harness, using its `Slot` locks (`harness/oracle.py:109-125`, 12 shared host-wide slots), private headless tinywl/bubblewrap setup, cleared sandbox environment, and `finally` process-group termination/wait (`:134-226`). No live-compositor commands were issued, and no DRM card node was used.
- Every started command had `WAYLAND_DISPLAY` and `HYPRLAND_INSTANCE_SIGNATURE` removed. Counters and diagnostics had a 4 GB soft / 8 GB hard address-space limit so the oracle could raise its own cap to 8 GB. Timeouts and `--core=0` were applied; `-B` prevented bytecode writes.
- All three counter receipts report coredumps `1335 -> 1335`, delta 0. All launched behavioral commands completed. A final scoped process check returned no matches (exit 1): `env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 10 pgrep -af '/fast/scratch/hyaku/mado-r26/rescore/RescoreK1NoValidation/(rescore[.]py|shape_probe[.]py|shape-(oracle|home))'`.
- Initial `env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 10 df -h /fast` reported 146 GB available, 82% used. Evidence writes were bounded.
- No tools installed or updated; no subagents dispatched; no git/jj writes, builds, linters, formatters, integration, or shipping actions.
- These are three sampled counter runs and one fixed auxiliary detector, not exhaustive parser coverage. The intentional raw-field/rejection limitations remain. The contract and frozen target were not changed.

RESCORE K1NoValidation not met (best 1/41)

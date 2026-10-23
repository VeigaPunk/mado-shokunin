# K1LabelKeyed — C1 LABEL/POSITION-KEYED control

## Verdict
CONTROL K1LabelKeyed best: cases_pass=2/41 verdict=TARGET_MISSED — not met

The unchanged control scored **2/41** and **1/41** on two fresh seeds. Both runs exited 1; neither was an inconclusive exit-2 run. This particular metadata/label cache did not meet PRED-C1-r26. This is not proof that the sandbox has no side channels: a separate, concrete parent-environment leak was observed.

## Scope and shape

Axes: metadata-only shape fidelity, replay strength, measured coverage, exact leak evidence, host safety and restoration.

- Control: `.ufo/waves/round-26/controls/K1LabelKeyed.py`, 26983 bytes, sha256 `2a17d95930f5c49318b446ee4cc66ad439e821e36cf1261f38b9104eff8e38da`. One Python 3 stdlib file with `--home DIR`; output is JSON `[nodes, beziers]`.
- The runtime never opens configuration contents, resolves a source graph, expands variables or computes an animation table. It opens only proc metadata files, enumerates names and calls stat. All animation answers are cached Hyprland outputs.
- Offline collection imported the frozen counter's generator functions and its pinned `oracle()` function. Training seed `c1a8e126`: BASE + 96 full generated cases + 34 generator-produced single-node DISABLE cases = 131 oracle tables, deduplicated to 120 answers. The baseline was 35 nodes and 6 beziers. No host compositor table was queried.
- Lookup order: exposed logical label; original source path; source-tree device/inode identity; exact normalized file-name/size/mtime-equals-ctime fingerprint; then cached BASE. Conflicting metadata buckets use answer frequency and a creation-position tie-break. New random filenames are generalized by parent, filename length and extension; their contents are not read.
- The cache has 131 source-path and inode identities, 96 logical-label keys and 109 normalized metadata buckets. Eight buckets have conflicting answers. One collision group is `DISABLE:global, DISABLE:layers, DISABLE:fadeIn, DISABLE:border`. Unique raw inode/path values distinguish training instances but are not portable logical labels.
- A fresh, oracle-free 40-case metadata calibration estimated 10195512.82 ns per generation position, with maximum residual 2.57 positions. It is a heuristic, not an observed exact case-index channel. Leave-one-out selection over the 96 generated training cases yielded at best 2/96, equal to cached BASE's 2/96; no nearest-neighbor fallback improved this, so it was not included. The final control was not changed between counter runs.

## What the sandbox actually exposed

These observations used the frozen, unedited `run_tool()` on our isolated scratch trees. The probe was read-only and bounded to 16 KiB per parent cmdline/environment and 128 KiB per other proc text. The complete sanitized observations are in the evidence paths below.

| Surface | Actual observation | Relevance |
| --- | --- | --- |
| Tool argv and cwd | `python3 -I /snap/tool.py --home /snap/home`; cwd `/snap/home` | Neither contains a case label. |
| Own environment | `HOME=/snap/home`, `PATH=/usr/bin`, `PWD=/snap/home`, Python-added `LC_CTYPE=C.UTF-8` | `/proc/self/environ` had only the first three, before Python's locale adjustment. No case or seed key was observed. |
| `/proc/self/mountinfo` | The bind at `/snap/home` retains the filesystem-relative source, e.g. `/scratch/hyaku/mado-r26/K1LabelKeyed-3nzq7oyw/tmpnzz3m_ya`. The tool source is also visible. Mount IDs, backing devices and the `/@/usr` source are visible. | Source names are not hidden, only randomized by the counter. |
| `/proc/1/cmdline` | PID 1 is bwrap, with the original host paths `/fast/scratch/hyaku/mado-r26/K1LabelKeyed-3nzq7oyw/tmpnzz3m_ya` and the tool path in its bind arguments. | A second route to exactly the same source-name information. |
| `/proc/1/environ` | **Readable original launcher environment: 261 observed keys**, not the cleared child environment. Non-secret observed values included `HOME=/home/vgpnk`, `PWD=/home/vgpnk/Projects/shokunin/mado-shokunin`, and the agent session-file path containing `MadoR26.K1LabelKeyed`. Credential-valued variables were present. | Concrete isolation gap. The control's case-label allowlist found no logical case/seed in this probe; the session identity is static across cases. Credential values are intentionally omitted. |
| Process namespace | Only PID 1 bwrap and PID 2 Python were enumerated. | The counter/oracle parent process and its Python locals were not exposed as processes. |
| File metadata | All 79 files and names were visible; BASE totaled 2,082,602 bytes. Mode, device, inode, exact sizes and nanosecond atime/mtime/ctime were readable. BASE had 79/79 files with mtime == ctime; generated T00 had 3/79. Unmodified copied files retained old mtimes and acquired newer ctimes. | Distinguishes fresh snapshot from copies and exposes touched-file/copy chronology; does not supply new numeric animation values. |
| Random generated filenames | Newly created config filenames remain visible, including their random spelling, length, extension and sizes. | Fingerprints some generator choices but is not an observed logical case label. |
| Standard FDs | stdin `/dev/null`; stdout/stderr `pipe:[402923599]` and `pipe:[402923600]` in the generated probe. | Kernel pipe identities vary but carry no observed case label. |
| Shared state and outside paths | `/tmp` was empty; `/run`, `/fast`, `/home`, `/sys`, `/etc` and the host counter path did not exist in the tool namespace. Root entries: `bin dev lib lib64 proc snap tmp usr`. | No case-to-case state file or directly reachable lane/counter file was observed. No escape was attempted. |

The registration's M25-2 repair removes logical labels from bind-source names, not the names themselves. Frozen `c1/count.py:230-245` keeps the fresh seed and labels in parent locals and uses random `mkdtemp` case paths; `:258-261` independently shuffles tool execution. The control scored against those unchanged bytes. Our probes observed paths and chronology, but did not recover a fresh counter case label or seed.

**Environment handling:** initial scratch captures of PID 1's environment were sanitized in place to key names plus a small non-secret allowlist. The current probe writes only this summary. No credential values are included in the report, receipt or control output. The leak was communicated to the parent as a repair decision; this leaf did not modify the harness.

## One bounded path-only mutation probe

Mutant: expose the same isolated T00 configuration bytes under `C17_CATEGORY_ROOT` instead of the random source-directory name. This changes the label-bearing bind-source path only; it is not a counter/harness code mutation.

Expected detector: unchanged `run_tool()` plus the frozen C1 `well_formed`, `node_set` and `bez_set` comparison against T00's already-collected real Hyprland answer. The same detector and expected answer were used in all three phases.

| Phase | Actual output | Detector |
| --- | --- | --- |
| Pristine random source | nodes missing=0 extra=0; beziers missing=0 extra=0; output sha256 `0d6bd22d2b9cb251df238cc70e2428038432739f67bff56a4583ac21be294b66` | PASS |
| Labelled source | nodes missing=5 extra=5; beziers missing=0 extra=0; output sha256 `a8c2612690bcd296967c38906f7d89143d6ee1acb4edf7701ef00ab87c7230ad` | FAIL |
| Restored random source | nodes missing=0 extra=0; beziers missing=0 extra=0; output sha256 `0d6bd22d2b9cb251df238cc70e2428038432739f67bff56a4583ac21be294b66` | PASS |

Verdict: **killed**, not inconclusive: the pristine baseline passed. This demonstrates the control really responds to a leaked label; it does not claim the frozen counter uses labelled paths.

Restoration evidence: the source binding was switched back to the original random path. No config file bytes changed in any phase; all three content-manifest hashes were `566182ce3c4c266570eb405370cc0fb5d3b856edc407fdbc3fda229756b587c0`. Before/after hashes were identical:

- Control: `2a17d95930f5c49318b446ee4cc66ad439e821e36cf1261f38b9104eff8e38da`.
- Frozen C1 counter: `f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd`.
- Frozen oracle harness: `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441`.

## Exact commands and exercised outputs

Commands below used lane cwd `/home/vgpnk/Projects/shokunin/mado-shokunin`. Display/session identifiers were removed from launched commands. The soft/hard address-space cap follows the parent note: 4 GB soft / 8 GB hard, allowing the oracle's own 8 GB limit.

```sh
timeout 10 env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE prlimit --as=4000000000 df -h /fast
timeout 900 env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE prlimit --as=4000000000:8000000000 python3 -I /fast/scratch/hyaku/mado-r26/K1LabelKeyed-3nzq7oyw/collect.py
timeout 120 env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE prlimit --as=4000000000:8000000000 python3 -I /fast/scratch/hyaku/mado-r26/K1LabelKeyed-3nzq7oyw/mutation_detector.py
timeout 3500 env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE prlimit --as=4000000000:8000000000 python3 -I /fast/scratch/hyaku/mado-r26/K1LabelKeyed-3nzq7oyw/score.py
```

`df` reported 186 GiB available before collection. The collector printed `TRAINING_COMPLETE cases=131` and `HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0`. Import/snapshot/model construction and metadata calibration were bounded Python eval cells; the final program was written directly to its assigned control path.

`score.py` ran this exact inner command twice, with no explicit seed:

```sh
timeout 900 python3 -I .ufo/waves/round-26/c1/count.py 05319e0f --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1LabelKeyed.py
```

Both counter processes returned 1, with zero stderr bytes. Run 1 stdout: 4,469 bytes, sha256 `130d988b899dc5301193fc87ca04d8e6239e13a0c77ac271d17a49ee837170bd`. Run 2 stdout: 4,396 bytes, sha256 `d7499e1a7b93562fa385c29d53a122e8867204800599301155a263468e02d84f`. Combined verbatim receipt: `.ufo/waves/round-26/controls/K1LabelKeyed.txt`, sha256 `9ac185cc040ef2bd496ee168bc404540a0bb2df433c6bfa9593c07238aa33af9`. No exit-2 retry was needed.

All nested compositors were started only inside the pinned `oracle()` sandbox. Its per-instance process-group cleanup completed, and both counters returned after their cleanup blocks. No live compositor command, service restart, git/jj write, sibling-file edit or package install/update was performed. `tools/mado-anims.py` and `tools/mado-binds.py` were not built or edited.

## Evidence paths

Scratch root: `/fast/scratch/hyaku/mado-r26/K1LabelKeyed-3nzq7oyw`.

- `training.json`, sha256 `f29f155fb249064e6cb7e6e9ed1f1155979613b824438c89911328ec3a21ca33`: all training profiles and actual oracle tables.
- `cache-model-summary.json`: cache shape and leave-one-out measurements.
- `score-summary.json`: exact command, per-run byte counts, hashes and process return codes.
- `mutation-probe.json`: full actual expected/pristine/mutated/restored outputs and before/after hashes.
- `evidence-summary.json`: sanitized leak summary and restoration evidence.
- `probe-baseline.json`, sha256 `9276aa80139ec3901167b479ed804a17c60edbb240b023c38523a305ef63c0e9`.
- `probe-generated.json`, sha256 `ae43de097628579d620613b25532315c99963b929cd7727379f050742c19e51b`.
- `probe-labelled-witness.json`, sha256 `0481bf4c223d38cc09436ebdc77e79880eb9d09df30c1df18549b24ea78c1d77`.
- `probe-restored-random-path.json`, sha256 `a9e479967c4d2398011ca166731e1df770aa57ae755ad4688635338561a90926`.

## Both frozen-counter receipts, verbatim

```text
counter c1-r26 sha256:f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1LabelKeyed.py sha256:2a17d95930f5c49318b446ee4cc66ad439e821e36cf1261f38b9104eff8e38da
seed=7adc1fca264a5023
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
CASE BASE  PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (unperturbed)
CASE C00   FAIL nodes missing=2 extra=2 beziers missing=1 extra=0 (ROOT+CATEGORY)
CASE C01   FAIL nodes missing=1 extra=1 beziers missing=2 extra=1 (REBEZ+BEZIER)
CASE C02   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (SOURCED+DISABLE)
CASE C03   FAIL nodes missing=2 extra=2 beziers missing=1 extra=0 (VARIABLE+UNSOURCED+BEZIER+COMMENT)
CASE C04   FAIL nodes missing=3 extra=3 beziers missing=1 extra=1 (ROOT+ORDER+COMMENT+REBEZ)
CASE C05   FAIL nodes missing=4 extra=4 beziers missing=1 extra=1 (SOURCED+ORDER+REBEZ+SPACING)
CASE C06   FAIL nodes missing=2 extra=2 beziers missing=1 extra=0 (SOURCED+BEZIER)
CASE C07   FAIL nodes missing=3 extra=3 beziers missing=1 extra=0 (COMMENT+SOURCED+BEZIER+ORDER)
CASE C08   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (UNSOURCED+SOURCED)
CASE C09   FAIL nodes missing=2 extra=2 beziers missing=1 extra=0 (COMMENT+CATEGORY+UNSOURCED+SOURCED)
CASE C10   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (INVALID+DISABLE)
CASE C11   FAIL nodes missing=2 extra=2 beziers missing=1 extra=0 (DISABLE+ROOT+CATEGORY)
CASE C12   FAIL nodes missing=4 extra=4 beziers missing=1 extra=0 (ROOT+VARIABLE+BEZIER+SOURCED)
CASE C13   FAIL nodes missing=2 extra=2 beziers missing=2 extra=1 (ORDER+BEZIER+UNSOURCED+REBEZ)
CASE C14   FAIL nodes missing=4 extra=4 beziers missing=1 extra=0 (INVALID+ORDER+SPACING+CATEGORY)
CASE C15   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (UNSOURCED+ROOT)
CASE C16   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (SPACING+SOURCED+VARIABLE)
CASE C17   FAIL nodes missing=2 extra=2 beziers missing=2 extra=1 (COMMENT+UNSOURCED+REBEZ+BEZIER)
CASE C18   FAIL nodes missing=2 extra=2 beziers missing=1 extra=1 (SPACING+REBEZ)
CASE C19   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (VARIABLE+INVALID+COMMENT)
CASE C20   FAIL nodes missing=2 extra=2 beziers missing=2 extra=1 (DISABLE+INVALID+REBEZ+BEZIER)
CASE C21   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (DISABLE+SOURCED)
CASE C22   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (ROOT+SPACING)
CASE C23   FAIL nodes missing=3 extra=3 beziers missing=1 extra=0 (UNSOURCED+COMMENT+SOURCED+BEZIER)
CASE C24   FAIL nodes missing=3 extra=3 beziers missing=1 extra=1 (ORDER+SPACING+COMMENT+REBEZ)
CASE C25   FAIL nodes missing=1 extra=1 beziers missing=1 extra=1 (ORDER+REBEZ+DISABLE+INVALID)
CASE C26   FAIL nodes missing=3 extra=3 beziers missing=2 extra=0 (CATEGORY+SPACING+BEZIER+UNSOURCED)
CASE C27   FAIL nodes missing=4 extra=4 beziers missing=1 extra=1 (REBEZ+ORDER+NEWSRC+SPACING)
CASE C28   FAIL nodes missing=3 extra=3 beziers missing=2 extra=0 (SOURCED+BEZIER+DISABLE+CATEGORY)
CASE C29   FAIL nodes missing=3 extra=3 beziers missing=1 extra=0 (COMMENT+INVALID+BEZIER+VARIABLE)
CASE C30   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (SOURCED+SPACING)
CASE C31   FAIL nodes missing=3 extra=3 beziers missing=1 extra=0 (CATEGORY+UNSOURCED+ORDER+COMMENT)
CASE C32   FAIL nodes missing=0 extra=0 beziers missing=1 extra=1 (INVALID+UNSOURCED+REBEZ)
CASE C33   FAIL nodes missing=1 extra=1 beziers missing=1 extra=1 (INVALID+SOURCED+REBEZ+UNSOURCED)
CASE C34   FAIL nodes missing=1 extra=1 beziers missing=1 extra=1 (DISABLE+UNSOURCED+REBEZ)
CASE C35   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (ORDER+UNSOURCED+ROOT)
CASE C36   FAIL nodes missing=1 extra=1 beziers missing=1 extra=0 (VARIABLE+CATEGORY+UNSOURCED)
CASE C37   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (COMMENT+INVALID+ORDER)
CASE C38   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (VARIABLE+DISABLE+COMMENT)
CASE C39   FAIL nodes missing=3 extra=3 beziers missing=2 extra=0 (COMMENT+BEZIER+CATEGORY+SPACING)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26 cases_pass=2/41 verdict=TARGET_MISSED
exit=1
counter c1-r26 sha256:f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1LabelKeyed.py sha256:2a17d95930f5c49318b446ee4cc66ad439e821e36cf1261f38b9104eff8e38da
seed=a7a5a450d27a24a5
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
CASE BASE  PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (unperturbed)
CASE C00   FAIL nodes missing=4 extra=4 beziers missing=0 extra=0 (SOURCED+SPACING+COMMENT)
CASE C01   FAIL nodes missing=2 extra=2 beziers missing=1 extra=0 (SOURCED+BEZIER)
CASE C02   FAIL nodes missing=3 extra=3 beziers missing=1 extra=0 (ROOT+VARIABLE+BEZIER)
CASE C03   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (DISABLE+ROOT)
CASE C04   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (ORDER+UNSOURCED+NEWSRC+SOURCED)
CASE C05   FAIL nodes missing=3 extra=3 beziers missing=1 extra=0 (NEWSRC+CATEGORY)
CASE C06   FAIL nodes missing=4 extra=4 beziers missing=0 extra=0 (VARIABLE+COMMENT+NEWSRC+ORDER)
CASE C07   FAIL nodes missing=3 extra=3 beziers missing=2 extra=0 (SPACING+BEZIER+SOURCED+CATEGORY)
CASE C08   FAIL nodes missing=1 extra=1 beziers missing=1 extra=0 (BEZIER+COMMENT+INVALID)
CASE C09   FAIL nodes missing=3 extra=3 beziers missing=2 extra=1 (SOURCED+BEZIER+NEWSRC+REBEZ)
CASE C10   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (SPACING+ORDER)
CASE C11   FAIL nodes missing=2 extra=2 beziers missing=1 extra=0 (CATEGORY+VARIABLE+NEWSRC)
CASE C12   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (UNSOURCED+ORDER+SOURCED)
CASE C13   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (ORDER+ROOT)
CASE C14   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (NEWSRC+SPACING+UNSOURCED)
CASE C15   FAIL nodes missing=2 extra=2 beziers missing=1 extra=0 (CATEGORY+ROOT)
CASE C16   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (NEWSRC+ORDER+DISABLE)
CASE C17   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (UNSOURCED+VARIABLE)
CASE C18   FAIL nodes missing=1 extra=1 beziers missing=1 extra=0 (BEZIER+SPACING+UNSOURCED)
CASE C19   FAIL nodes missing=2 extra=2 beziers missing=2 extra=0 (UNSOURCED+BEZIER+CATEGORY)
CASE C20   FAIL nodes missing=3 extra=3 beziers missing=1 extra=0 (ROOT+UNSOURCED+DISABLE+CATEGORY)
CASE C21   FAIL nodes missing=3 extra=3 beziers missing=1 extra=0 (NEWSRC+ORDER+CATEGORY)
CASE C22   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (NEWSRC+ORDER+SOURCED)
CASE C23   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (ROOT+INVALID+SPACING)
CASE C24   FAIL nodes missing=4 extra=4 beziers missing=0 extra=0 (COMMENT+ROOT+SOURCED+INVALID)
CASE C25   FAIL nodes missing=2 extra=2 beziers missing=1 extra=0 (SOURCED+BEZIER)
CASE C26   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (VARIABLE+INVALID+COMMENT)
CASE C27   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (UNSOURCED+ROOT)
CASE C28   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (SOURCED+SPACING+ROOT)
CASE C29   FAIL nodes missing=3 extra=3 beziers missing=1 extra=0 (VARIABLE+ROOT+BEZIER)
CASE C30   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (SOURCED+UNSOURCED+INVALID)
CASE C31   FAIL nodes missing=2 extra=2 beziers missing=1 extra=0 (BEZIER+UNSOURCED+SOURCED+ORDER)
CASE C32   FAIL nodes missing=2 extra=2 beziers missing=1 extra=0 (ROOT+BEZIER)
CASE C33   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (UNSOURCED+INVALID+ROOT+ORDER)
CASE C34   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (ROOT+UNSOURCED+SOURCED+COMMENT)
CASE C35   FAIL nodes missing=2 extra=2 beziers missing=1 extra=0 (CATEGORY+SPACING+ROOT+INVALID)
CASE C36   FAIL nodes missing=3 extra=3 beziers missing=2 extra=0 (CATEGORY+COMMENT+BEZIER)
CASE C37   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (NEWSRC+INVALID)
CASE C38   FAIL nodes missing=2 extra=2 beziers missing=1 extra=1 (DISABLE+REBEZ+VARIABLE+NEWSRC)
CASE C39   FAIL nodes missing=3 extra=3 beziers missing=1 extra=0 (UNSOURCED+ROOT+VARIABLE+CATEGORY)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26 cases_pass=1/41 verdict=TARGET_MISSED
exit=1
```

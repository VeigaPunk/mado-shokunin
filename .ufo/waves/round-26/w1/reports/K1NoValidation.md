# K1NoValidation — C1 NO-VALIDATION READER control

## Verdict
CONTROL K1NoValidation best: cases_pass=0/41 verdict=TARGET_MISSED — not met

Both fresh-seed runs of the frozen C1 counter returned `exit=1` with 0/41 cases passing; no run exited 2, so no guard retry was needed. This is a negative-control result for the assigned shape, not evidence that a full resolver misses C1. The control is a correct source-graph reader (positive-tested on a synthetic multi-file tree, §3) whose field handling is deliberately raw per the item text; it fails because the counter compares against Hyprland's own encoded values, and the snapshot's first unperturbed row already differs.

## 1. Assigned shape and artifact

- Shape: NO-VALIDATION READER. Follow `source =` from `DIR/.config/hypr/hyprland.conf` in read order (including `~` and globs), expand `$variables`, strip `#` comments, honour `animations { }` category blocks, apply every `animation =` / `bezier =` line in order with last-wins over an embedded default table. Directives apply at top level and inside an open `animations` block; brace depth is tracked so other categories' bodies are not mistaken for top level. No validation: unknown node names are added, unknown beziers accepted, written fields copied raw (`enabled` as bool, `speed` as float, `bezier`/`style` as strings), absent fields left at the row's current value, missing bezier coordinates filled with 0.0.
- Artifact: `.ufo/waves/round-26/controls/K1NoValidation.py`, 7459 bytes, SHA-256 `ca9ba0c963410221db80092a1b6adfb0d5e40685cfa480eecc555aef6e33bcb5`. Single stdlib Python file, `--home DIR`, prints JSON `[nodes, beziers]`.
- Embedded default table (35 nodes including `__internal_fadeCTM`, 2 beziers `linear` and `default`) is reconstructed from the measured rows; it is not the snapshot table. A minimal tree through the frozen oracle produced exactly this table, and running the control on an empty tree reproduces it set-for-set (§2).
- Deliberate shape limits, stated before scoring: Hyprland's own value encoding is not emulated (a disabled line's fields, float32/two-decimal reporting), rejected lines are still applied, and a written field overwrites while an absent field is left unchanged.

## 2. Default-table acquisition (frozen oracle, host-safe)

Scratch script `/fast/scratch/hyaku/mado-r26/k1nv/probe.py` imports the pinned harness by path, calls `check_build()`, and calls `oracle()` with `verbs=["animations"]` on (a) a tree whose only config file is an empty `.config/hypr/hyprland.conf`, and (b) a copy of the four frozen config roots from `~`. Exact command:

```sh
cd /fast/scratch/hyaku/mado-r26/k1nv && env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 300 prlimit --as=4000000000:8000000000 -- python3 -I -B probe.py min full
```

Output:

```text
snapshot files=79 digest=fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
OK min nodes=35 beziers=2 -> /fast/scratch/hyaku/mado-r26/k1nv/probe-work/min.json
OK full nodes=35 beziers=6 -> /fast/scratch/hyaku/mado-r26/k1nv/probe-work/full.json
```

Minimal-tree default rows: 30 ordinary nodes are `{overridden:false, bezier:"", enabled:true, speed:0.0, style:""}`; `global` is `{overridden:true, bezier:"default", enabled:true, speed:8.0, style:""}`; `borderangle`/`glowangle`/`shadowangle` are `{overridden:true, bezier:"default", enabled:false, speed:1.0, style:""}`; `__internal_fadeCTM` is `{overridden:true, bezier:"linear", enabled:true, speed:5.0, style:""}`. Default beziers: `linear (0,0,1,1)` and `default (0,0.75,0.15,1)`.

Control-vs-oracle checks on that probe (offline tool runs, no Hyprland involved):

```text
control default == oracle minimal tree: True 35 2
control snapshot diff vs oracle BASE: nodes missing=1 extra=1 beziers missing=0 extra=0
differing rows: ['workspaces']
```

So the embedded table is exact, and on the unperturbed snapshot the control differs from Hyprland in exactly one row (§4).

## 3. Structural positive control — synthetic source graph

`/fast/scratch/hyaku/mado-r26/k1nv/synth_run.py` builds a tree that exercises top-level directives, a `source` glob, a nested `source` inside a sourced file, `$` variables used for speed and bezier, a top-level commented-out directive, a trailing inline comment, an `animations { }` block, order/last-wins on one node, and an unsourced file that must be ignored. Every animation line in it is well formed, uses a bezier defined before use, and has a two-decimal speed, so the shape's raw field copy is not implicated. Root config:

```conf
$sp = 3.5
$bz = easeOutQuint
source = ~/.config/hypr/extra/*.conf
source = ~/.config/hypr/one.conf
animation = global, 1, 7.25, default
# animation = windows, 0
animation = windows, 1, $sp, $bz, popin 60%
```

`extra/aa.conf` defines `easeOutQuint` and, in `animations { }`, `layers` + `localbz`; `one.conf` sources `two.conf`, sets `windows` (popin 50%) then `border`; `two.conf` re-sets `windows` (fade, so last-wins is exercised) and sets `fade` with a trailing comment; `unsourced.conf` has an animation and a bezier that must not appear. Command and output:

```sh
cd /fast/scratch/hyaku/mado-r26/k1nv && env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 300 prlimit --as=4000000000:8000000000 -- python3 -I -B synth_run.py
```

```text
nodes missing=0 extra=0 beziers missing=0 extra=0
```

The control reproduced the oracle exactly on this tree, which isolates the failures in §5 to the shape's raw value handling and non-validation, not to source-graph, variable, comment, category, or ordering bugs.

## 4. The row that blocks BASE

The snapshot's own `~/.local/share/omarchy/default/hypr/looknfeel.conf` contains, inside `animations { }`, `animation = workspaces, 0, 0, ease`. Hyprland reports that row as `{overridden:true, bezier:"default", enabled:false, speed:1.0, style:""}`; the raw reader copies the written fields and reports `{overridden:true, bezier:"ease", enabled:false, speed:0.0, style:""}`. Exact diff from the offline run above:

```text
GOT {'name': 'workspaces', 'overridden': True, 'bezier': 'ease', 'enabled': False, 'speed': 0.0, 'style': ''}
EXP {'name': 'workspaces', 'overridden': True, 'bezier': 'default', 'enabled': False, 'speed': 1.0, 'style': ''}
```

That single row makes BASE fail (the counter's BASE receipt line is `nodes missing=1 extra=1`), and every generated case inherits it unless a case operation happens to overwrite `workspaces`. Learning Hyprland's disabled-line encoding is exactly the handler study the item forbids, so the shape cannot repair this row.

## 5. Scoring commands and verbatim receipts

Both runs used independent fresh seeds, a sanitized parent environment, `-B` (no bytecode writes), soft 4 GB / hard 8 GB address-space so the pinned oracle can set its own 8 GB, and a 900 s timeout. Working directory was `/home/vgpnk/Projects/shokunin/mado-shokunin`.

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 900 prlimit --as=4000000000:8000000000 --core=0 -- python3 -I -B .ufo/waves/round-26/c1/count.py 05319e0f --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1NoValidation.py
```

Run 1 returned 1 (stderr empty); run 2 returned 1 (stderr empty). Receipts are concatenated verbatim at `.ufo/waves/round-26/controls/K1NoValidation.txt` (8745 bytes, SHA-256 `3341ad8f8c31c9a45be5e10215866a4f7e2de378f8552c8194a2c0c0bf1d397f`). Both runs report `HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0`.

### Receipt 1 (seed=2abca99af2c0928a)

```text
counter c1-r26 sha256:f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1NoValidation.py sha256:ca9ba0c963410221db80092a1b6adfb0d5e40685cfa480eecc555aef6e33bcb5
seed=2abca99af2c0928a
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
CASE BASE  FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (unperturbed)
CASE C00   FAIL nodes missing=1 extra=2 beziers missing=0 extra=0 (CATEGORY+INVALID)
CASE C01   FAIL nodes missing=4 extra=4 beziers missing=0 extra=0 (VARIABLE+INVALID+SPACING+DISABLE)
CASE C02   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (ORDER+COMMENT)
CASE C03   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (DISABLE+COMMENT+VARIABLE+REBEZ)
CASE C04   FAIL nodes missing=4 extra=4 beziers missing=1 extra=1 (VARIABLE+BEZIER+NEWSRC+ROOT)
CASE C05   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (ROOT+NEWSRC+SOURCED+COMMENT)
CASE C06   FAIL nodes missing=4 extra=4 beziers missing=0 extra=1 (INVALID+SPACING+SOURCED)
CASE C07   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (NEWSRC+SOURCED+ORDER)
CASE C08   FAIL nodes missing=1 extra=1 beziers missing=1 extra=1 (ROOT+SPACING+REBEZ+ORDER)
CASE C09   FAIL nodes missing=5 extra=5 beziers missing=0 extra=0 (ORDER+SOURCED+INVALID+DISABLE)
CASE C10   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (CATEGORY+ROOT+REBEZ+ORDER)
CASE C11   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (NEWSRC+CATEGORY+SPACING)
CASE C12   FAIL nodes missing=3 extra=3 beziers missing=2 extra=2 (BEZIER+SOURCED+COMMENT+REBEZ)
CASE C13   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (SPACING+CATEGORY+DISABLE+UNSOURCED)
CASE C14   FAIL nodes missing=4 extra=4 beziers missing=0 extra=0 (VARIABLE+SPACING+NEWSRC)
CASE C15   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (ORDER+INVALID+SOURCED+COMMENT)
CASE C16   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (ROOT+ORDER+SOURCED+SPACING)
CASE C17   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (COMMENT+SPACING)
CASE C18   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (SPACING+UNSOURCED)
CASE C19   FAIL nodes missing=2 extra=3 beziers missing=0 extra=0 (INVALID+CATEGORY+SOURCED)
CASE C20   FAIL nodes missing=2 extra=2 beziers missing=1 extra=1 (SPACING+REBEZ)
CASE C21   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (DISABLE+SOURCED+NEWSRC)
CASE C22   FAIL nodes missing=3 extra=3 beziers missing=1 extra=1 (SOURCED+ORDER+REBEZ)
CASE C23   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (VARIABLE+UNSOURCED)
CASE C24   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (ORDER+REBEZ+COMMENT)
CASE C25   FAIL nodes missing=2 extra=2 beziers missing=1 extra=1 (CATEGORY+UNSOURCED+REBEZ)
CASE C26   FAIL nodes missing=4 extra=4 beziers missing=0 extra=0 (SOURCED+INVALID+VARIABLE+UNSOURCED)
CASE C27   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (INVALID+COMMENT+ROOT+SPACING)
CASE C28   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (ROOT+VARIABLE)
CASE C29   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (DISABLE+INVALID+VARIABLE)
CASE C30   FAIL nodes missing=2 extra=2 beziers missing=1 extra=1 (VARIABLE+REBEZ+SOURCED)
CASE C31   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (SOURCED+ORDER)
CASE C32   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (UNSOURCED+DISABLE)
CASE C33   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (UNSOURCED+NEWSRC+DISABLE)
CASE C34   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (VARIABLE+ORDER+ROOT)
CASE C35   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (NEWSRC+UNSOURCED)
CASE C36   FAIL nodes missing=4 extra=4 beziers missing=0 extra=0 (COMMENT+ROOT+INVALID+ORDER)
CASE C37   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (ROOT+DISABLE+SOURCED)
CASE C38   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (SPACING+ROOT)
CASE C39   FAIL nodes missing=4 extra=4 beziers missing=0 extra=0 (NEWSRC+DISABLE)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```

### Receipt 2 (seed=733812d8cb4cb4c2)

```text
counter c1-r26 sha256:f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1NoValidation.py sha256:ca9ba0c963410221db80092a1b6adfb0d5e40685cfa480eecc555aef6e33bcb5
seed=733812d8cb4cb4c2
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
CASE BASE  FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (unperturbed)
CASE C00   FAIL nodes missing=3 extra=3 beziers missing=1 extra=1 (REBEZ+NEWSRC+VARIABLE)
CASE C01   FAIL nodes missing=1 extra=1 beziers missing=1 extra=1 (BEZIER+VARIABLE)
CASE C02   FAIL nodes missing=4 extra=4 beziers missing=0 extra=0 (NEWSRC+CATEGORY)
CASE C03   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (ORDER+UNSOURCED+DISABLE)
CASE C04   FAIL nodes missing=6 extra=6 beziers missing=1 extra=1 (ORDER+SOURCED+BEZIER+NEWSRC)
CASE C05   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (COMMENT+ORDER)
CASE C06   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (UNSOURCED+DISABLE)
CASE C07   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (SPACING+INVALID)
CASE C08   FAIL nodes missing=3 extra=3 beziers missing=1 extra=1 (INVALID+BEZIER)
CASE C09   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (DISABLE+SPACING)
CASE C10   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (COMMENT+DISABLE)
CASE C11   FAIL nodes missing=3 extra=3 beziers missing=1 extra=1 (SPACING+BEZIER+NEWSRC)
CASE C12   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (COMMENT+UNSOURCED+CATEGORY)
CASE C13   FAIL nodes missing=4 extra=4 beziers missing=0 extra=0 (ORDER+CATEGORY+UNSOURCED+SOURCED)
CASE C14   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (SOURCED+ROOT+DISABLE)
CASE C15   FAIL nodes missing=4 extra=4 beziers missing=0 extra=0 (NEWSRC+VARIABLE+SPACING+CATEGORY)
CASE C16   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (CATEGORY+ROOT)
CASE C17   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (UNSOURCED+ROOT+DISABLE)
CASE C18   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (ORDER+COMMENT+UNSOURCED+VARIABLE)
CASE C19   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (COMMENT+SOURCED)
CASE C20   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (UNSOURCED+ROOT+CATEGORY)
CASE C21   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (UNSOURCED+ROOT)
CASE C22   FAIL nodes missing=2 extra=2 beziers missing=1 extra=1 (VARIABLE+BEZIER+ROOT)
CASE C23   FAIL nodes missing=6 extra=6 beziers missing=0 extra=1 (CATEGORY+SPACING+INVALID+NEWSRC)
CASE C24   FAIL nodes missing=4 extra=4 beziers missing=0 extra=0 (SPACING+SOURCED)
CASE C25   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (SOURCED+ROOT+DISABLE)
CASE C26   FAIL nodes missing=1 extra=2 beziers missing=0 extra=0 (INVALID+DISABLE+ROOT)
CASE C27   FAIL nodes missing=2 extra=2 beziers missing=1 extra=1 (DISABLE+REBEZ)
CASE C28   FAIL nodes missing=3 extra=3 beziers missing=1 extra=1 (BEZIER+SOURCED+VARIABLE)
CASE C29   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (UNSOURCED+SPACING)
CASE C30   FAIL nodes missing=3 extra=3 beziers missing=1 extra=1 (BEZIER+SOURCED)
CASE C31   FAIL nodes missing=4 extra=4 beziers missing=1 extra=1 (NEWSRC+REBEZ+VARIABLE+SOURCED)
CASE C32   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (SOURCED+ROOT)
CASE C33   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (VARIABLE+INVALID+ROOT+SPACING)
CASE C34   FAIL nodes missing=3 extra=3 beziers missing=1 extra=1 (UNSOURCED+ROOT+BEZIER+DISABLE)
CASE C35   FAIL nodes missing=4 extra=4 beziers missing=0 extra=0 (SPACING+ORDER+VARIABLE)
CASE C36   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (UNSOURCED+COMMENT+SPACING)
CASE C37   FAIL nodes missing=4 extra=4 beziers missing=0 extra=0 (NEWSRC+ORDER+SPACING)
CASE C38   FAIL nodes missing=4 extra=4 beziers missing=0 extra=0 (SPACING+DISABLE+VARIABLE+COMMENT)
CASE C39   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (CATEGORY+INVALID)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```

## 6. Failure attribution (measured, not inferred)

`/fast/scratch/hyaku/mado-r26/k1nv/diag.py` rebuilds each retained seed's cases from the frozen counter's own generator, runs the frozen oracle and the control, and classifies every differing row. Per-seed summary of cases containing at least one row of each class (`seed 2abca99af2c0928a` / `seed 733812d8cb4cb4c2`):

| class | meaning | cases r1 | cases r2 |
|---|---|---|---|
| disabled-canonical | Hyprland encodes a disabled line as speed 1.0 / bezier `default` / style `""`; raw copy keeps written values | 38 (incl. BASE) | 38 (incl. BASE) |
| enabled/canonical | same for case-added disabled lines on other nodes | 22 | 20 |
| speed-repr | written speed has 3–4 decimals; Hyprland reports float32 at two decimals | 20 | 24 |
| bezier-repr | bezier coordinate has 3–5 decimals; Hyprland reports float32 at two decimals | 7 | 11 |
| style | a 4-field line re-sets a node: Hyprland clears style to `""`; the shape leaves the old style | 4 | 7 |
| bezier-extra | short `bezier = name, x, y` line is added by the shape, rejected by Hyprland | 1 | 1 |
| node-extra | unknown-node `animation =` line is added by the shape, ignored by Hyprland | 2 | 1 |
| rejected-but-applied | an unknown/forward-named bezier, a negative speed, or a short animation line is applied by the shape; Hyprland rejects the whole line and does not set `overridden` (seed-1 `C03`'s remaining `other` row is speed-repr + style, counted above) | 6 | 4 |

The near-clean cases are the sharpest measurement: in seed 1, `C17` (COMMENT+SPACING), `C18` (SPACING+UNSOURCED) and `C38` (SPACING+ROOT); in seed 2, `C03` (ORDER+UNSOURCED+DISABLE), `C19` (COMMENT+SOURCED), `C21` (UNSOURCED+ROOT) and `C29` (UNSOURCED+SPACING) each differ from the oracle in **only** the inherited BASE `workspaces` row. Encoding Hyprland's disabled-line value rule would therefore pass BASE plus those 3–4 cases; the remaining cases still fail on the decimal representation, order-sensitive bezier existence, style clearing, and rejection of invalid lines listed above.

Example rejections measured in the same pipeline:

- `fadeShadow`: the shape applied `animation = fadeShadow, 1, 3, nbtssogx`; the oracle kept `{overridden:false, bezier:"", speed:0.0}` — an unknown bezier rejects the whole line, leaving `overridden` false.
- `specialWorkspaceIn`: a `NEWSRC` file contains `animation = specialWorkspaceIn, 1, 7, easeOutQuint, slidevert`, but it is sourced at root line 7 while `easeOutQuint` is only defined at root line 10. Hyprland's `configerrors` says `no such bezier` and the row stays default; the no-validation reader accepts a forward reference. This is order-sensitive validation, not a source-graph error in the control.
- `fadePopups`: `animation = fadePopups, 1` (short line) is applied with `overridden=true` by the shape; Hyprland logs `invalid speed` and leaves the row untouched.

## 7. Counter observation (reproducible; no counter or harness edit made)

The registration says the pre-landing generator change ensures "every C1 case carries at least one table-changing operation". The generator enforces only that at least one operation is drawn from its static `EFFECTIVE` set; it does not verify that the operation changes the oracle table. A reproducible counterexample from a development pair (seed `f7b35f295db87ee8`, run before the retained sanitized pair; same frozen generator) is `C32` (`INVALID+UNSOURCED+NEWSRC`):

- `UNSOURCED` created `.config/hypr/whkysx.conf` with two animations, never sourced (correctly no effect).
- `NEWSRC` created `.config/hypr/yjsjqy.conf` with `animation = specialWorkspaceIn, 1, 7, easeOutQuint, slidevert` and appended `source = ~/.config/hypr/yjsjqy.conf` to `bindings/tiling-v2.conf` (root line 7). `easeOutQuint` is defined later (root line 10), so Hyprland reports `... yjsjqy.conf at line 2: no such bezier` and applies nothing.
- `INVALID` appended `animation = fadePopups, 1` to `apps/bitwarden.conf`; Hyprland reports `... bitwarden.conf at line 8: invalid speed` and applies nothing.

A sanitized re-run of the same seed through the harness oracle (`/fast/scratch/hyaku/mado-r26/k1nv/c32_probe.py`, `verbs=["animations","configerrors"]`) printed:

```text
C32 expected equals BASE(unperturbed snapshot): True
specialWorkspaceIn: {'name': 'specialWorkspaceIn', 'overridden': False, 'bezier': '', 'enabled': True, 'speed': 0.0, 'style': ''}
```

so that case's expected table is identical to BASE under the counter's own `node_set`/`bez_set` comparators. The retained seeds `2abca99af2c0928a` and `733812d8cb4cb4c2` happened to contain no such case, so this is seed-dependent, but it is reproducible: any `SOURCED`/`NEWSRC` line that references a bezier defined later in source order (the generator picks names from the whole tree, not the prefix) or an `INVALID` variant that Hyprland rejects produces a no-effect operation. Such a case tests nothing beyond BASE and is passable by a config-ignoring snapshot cache; the existing `K1SnapshotCache` receipts (`CASE BASE PASS`, occasional single extra case) are consistent with this. Impact is limited to counter discrimination, not to correctness of any expected value (the oracle remains ground truth). Flagged for the L1 under the "say so with a concrete demonstration" rule; the frozen bytes were not touched.

## 8. Host safety, unchanged bytes, cleanup

- Every nested Hyprland was started only by the pinned `harness/oracle.py` (`oracle()`), which runs it in a `--unshare-all --clearenv` bwrap sandbox with a private XDG_RUNTIME_DIR and the amdgpu render node only, and whose `finally` kills the sandbox process group. The retained scoring runs and every diagnostic used for this report ran with `WAYLAND_DISPLAY` and `HYPRLAND_INSTANCE_SIGNATURE` unset in their parent environment; an earlier development pair (seeds `f7b35f295db87ee8`, `071c203832a6fae5`) inherited the shell's values in its parent Python process, but the harness clears the environment inside the sandbox and its `hyprctl` calls use an explicit two-variable environment, so no started compositor or `hyprctl` ever saw the live-session variables; the retained pair was re-run sanitized so the saved receipts carry the strict form. No `hyprctl` was run against the live compositor (all live reads were plain file reads), and no DRM card node was used.
- Both scored receipts report `hyprland_coredumps_before=1335 after=1335 delta=0`. No `tinywl` or sandbox `Hyprland` process remained after the runs (`pgrep` matched only the operator's own session processes).
- Frozen bytes unchanged: `c1/count.py` SHA-256 `f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd`; `harness/oracle.py` SHA-256 `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441`. No counter, harness, tool, or other lane source was edited; the only lane writes are this control, its receipt, and this report (the pre-existing `harness/__pycache__` and `c1/__pycache__` bytes were not rewritten; runs used `-B`).
- Scratch evidence retained under `/fast/scratch/hyaku/mado-r26/k1nv` (32 MB: probe tables, synthetic tree, diag dumps per seed, c32 probe tree); no builds, linters, formatters, tests, installs or git/jj commands were run. No subagent was dispatched (leaf seat; no spawn tool granted).

## 9. Files changed

- `.ufo/waves/round-26/controls/K1NoValidation.py` — new control (7459 bytes, SHA-256 `ca9ba0c963410221db80092a1b6adfb0d5e40685cfa480eecc555aef6e33bcb5`).
- `.ufo/waves/round-26/controls/K1NoValidation.txt` — two verbatim receipts (8745 bytes, SHA-256 `3341ad8f8c31c9a45be5e10215866a4f7e2de378f8552c8194a2c0c0bf1d397f`).
- `.ufo/waves/round-26/w1/reports/K1NoValidation.md` — this report.

No `tools/mado-anims.py`, `tools/mado-binds.py`, counter, harness, corpus, or other lane file was written.

# K1RootOnly — C1 control (root-only reader): receipt

Seat `MadoR26.K1RootOnly`, round 26 w1, 2026-10-23. Lane `mado-shokunin`, tip `05319e0f`.
Claim under test: C1 / PRED-C1-r26 (animation table from config bytes; target `cases_pass=41/41`).
Item shape: parse only `DIR/.config/hypr/hyprland.conf`; never follow `source =`; apply its
`animation =` / `bezier =` lines with simple last-wins rules over Hyprland's default table
(embedded from a live oracle run on a minimal tree); no variables, no validation.

## Verdict
CONTROL K1RootOnly best: cases_pass=0/41 verdict=TARGET_MISSED — not met

Two scored runs, fresh seeds `433e52b606c71bbb` and `99277b94d7cdba01`, both `cases_pass=0/41`,
both `exit=1`; receipts saved verbatim at `.ufo/waves/round-26/controls/K1RootOnly.txt`
(sha256 `1eebdafd05d34e3bf9816105064767fb327ad0827e6282491fd213f021fd4432`).

The shape is structurally incapable of the target on this snapshot, and the reason is a fact about
the operator's config, not about the control's reader: the root file
`~/.config/hypr/hyprland.conf` contains **zero** `animation`/`bezier` directives — 18 `source =`
lines and comments only — while the complete 15-node animation override and 4 of the 6 beziers that
`hyprctl animations -j` reports live in `~/.local/share/omarchy/default/hypr/looknfeel.conf`,
reached through a `source =` line. A reader that does not follow sources therefore starts and ends
at Hyprland's default table: BASE and every case differ from the oracle in the same 15 nodes
(overridden flag, bezier, speed, style) and miss the same 4 beziers (easeOutQuint, easeInOutCubic,
almostLinear, quick). Every one of the 41 CASE lines in both receipts shows `missing>=14` nodes;
no generated operation can repair a difference that is present before the case is applied.

The reader itself is faithful where the shape is complete: a self-test against the oracle on three
root-only trees (empty; the omarchy `animations { … }` block moved to the root; a mixed tree with
categories, comments, tight spacing, disable-by-0, disable-by-2, a new bezier, a redefined
`default` bezier and rounding-sensitive speeds) matched the oracle exactly, 3/3
(selftest.py output below). The miss is reachability, not parsing.

No counter, harness, tool or other lane file was edited. No package was installed or upgraded.
Receipt hashes printed by the counter match the pinned values
(`count.py f98e264b…`, `oracle.py 680798ed…`) in both runs.

## What was built

`.ufo/waves/round-26/controls/K1RootOnly.py` (sha256
`42ae2fb5df5470b04e2a42eeaa216cb43e3771f24a5cce66d49ce08c0c4edcb0`), a single stdlib file,
CLI `--home DIR`, printing one JSON array `[nodes, beziers]` in `hyprctl animations -j` shape.

- Embedded default table: `[[…35 nodes…],[…2 beziers…]]` captured from a live `hyprctl animations -j`
  (Hyprland v0.56.2 = `efb50993`) through the round-26 harness `oracle()` on a tree whose only file
  is an empty `.config/hypr/hyprland.conf`. Default beziers: `linear` = (0, 0, 1, 1),
  `default` = (0.0, 0.75, 0.15, 1.0). Overridden roots: `global` (enabled, 8, `default`),
  `__internal_fadeCTM` (enabled, 5, `linear`), `borderangle`/`shadowangle`/`glowangle`
  (disabled, 1, `default`); the other 29 nodes report `overridden=false`, bezier `""`, speed 0.0,
  and `enabled=true` (Hyprland's unset `internalEnabled=-1` prints truthy).
- Root parse: read `DIR/.config/hypr/hyprland.conf` only; `#` starts a comment; `animation` and
  `bezier` keys are matched with free whitespace and at any brace depth (hyprlang's
  `animations { animation = … }` category is equivalent to the root key, confirmed by probe P02/P13);
  `source =` and `$variable` lines are plain text to this reader.
- Per-line effect, last wins per node name / bezier name, matching Hyprland's legacy handler for a
  well-formed line: enabled field `"1"` → node takes speed/bezier/style; any other enabled field →
  Hyprland's disable branch (enabled=false, speed 1, bezier `default`, style `""`);
  `bezier = name, x0, y0, x1, y1` replaces or adds `name`.
- Shape limits kept honestly: no variable expansion; no validation, so an unknown node is created,
  an unknown bezier name is stored, an unparseable speed becomes 1.0 and a missing bezier point 0.0.
  These coercions can only add mismatch and never applied in the observed scoring (the baseline
  difference dominates every case).
- Numbers: reported with `{:.2f}` semantics over a float32 value (`struct.pack("f")` then
  `float("%.2f" % …)`) so 4-decimal generated inputs and the JSON round-trip match Hyprland's
  `internalSpeed`/bezier printing bit-for-bit at the two-decimal boundary. Verified by the mixed
  self-test tree (3.14159, 1.005, 9.999).

## Exact commands run

Probe of Hyprland semantics and the default table (18 oracle instances; scratch script, host-safe):

```
cd /fast/scratch/hyaku/mado-r26/K1RootOnly && timeout 600 python3 -I probe.py
```

Control self-test against the same oracle (4 trees):

```
cd /fast/scratch/hyaku/mado-r26/K1RootOnly && timeout 600 python3 -I selftest.py
```

Scoring runs (twice, fresh seed each; `prlimit` keeps the soft cap at 4 GB while the oracle raises
its own soft cap to its 8 GB hard cap, per the L1 note):

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin && \
timeout 900 prlimit --as=4000000000:8000000000 python3 -I .ufo/waves/round-26/c1/count.py 05319e0f \
  --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1RootOnly.py
```

Run 1 stdout → `/fast/scratch/hyaku/mado-r26/K1RootOnly/run1.txt`; run 2 → `run2.txt`; both
concatenated verbatim into `.ufo/waves/round-26/controls/K1RootOnly.txt`:

```
cat run1.txt run2.txt > .ufo/waves/round-26/controls/K1RootOnly.txt
```

Sources read (read-only, raw GitHub at the pinned commits, no API):

```
curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp
curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/animation/AnimationTree.cpp
curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp
curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/animation/AnimationConfig.cpp
curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/include/hyprutils/animation/AnimationConfig.hpp
curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/animation/AnimationManager.cpp
```

(`src/config/ConfigDescriptions.hpp` at that commit is 404; not needed.)

## Evidence: default table and Hyprland semantics (oracle probes)

`probe.py` ran 17 single-feature trees plus the empty tree. Full JSON:
`/fast/scratch/hyaku/mado-r26/K1RootOnly/probe/probe-results.json`. Host safety line from that run:
`HOST_SAFETY coredumps_before=1335 after=1335 delta=0`.

| probe | tree's only directives | oracle result |
|---|---|---|
| P00 | (empty) | 35 nodes, 2 beziers: `linear`(0,0,1,1), `default`(0,0.75,0.15,1); roots as listed above; other nodes overridden=false/enabled=true/speed 0/bezier "" |
| P01 | `animation = global, 1, 3, default` | global overridden, speed 3 — a root-level `animation` line is live |
| P02 | same line inside `animations { … }` | identical to P01 — category depth does not matter |
| P03 | `animation = global, 2, 3, default` | enabled=false, speed 1, bezier `default` — Hyprland's `parseInt(...)==1` coercion sends 2 to the disable branch |
| P04 | new `bezier = zz,…` + `animation … zz` | node uses `zz`, `zz` appears with the given points |
| P05 | `bezier = default, 0.1, 0.2, 0.8, 0.9` | `default`'s points are replaced |
| P06 | `animation = nosuchnode, 1, 3, default` | no change — unknown node ignored |
| P07 | `animation = global, 1, fast, default` | no change — bad speed ignored |
| P08 | `animation = global, 1, 3, default, bogus` | applied with style `bogus`: `setConfigForNode` runs before style validation |
| P09 | `animation=global,1,3,default # trailing` and tab-separated variant | both applied; comment stripped, spacing free |
| P10 | `animation = global, 0` | enabled=false, speed 1, bezier `default` |
| P11 | `bezier = easeOutQuint,…` before `animation = windowsIn, 1, 4.1, easeOutQuint, popin 87%` | both applied in file order |
| P12 | `animations { enabled = no }` | node table unchanged |
| P13 | bezier + animation inside `animations { … }` | both applied |
| P14 | `animation = global, 1, 3, nosuchbezier` | no change — unknown bezier ignored |
| P15 | `animation = global, 1, 0, default` | no change — speed 0 rejected |
| P16 | `bezier = bad, 0.1, 0.2` | no change — short bezier rejected |
| P17 | `animation = windows, 1, 3, default, slide top` | applied, style `slide top` |

Code anchors for the same facts: `src/config/legacy/ConfigManager.cpp:612-613` (root handlers for
`bezier`/`animation`), `:1389` `handleBezier` (five `CVarList` fields, add-or-replace),
`:1426` `handleAnimation`, `:1438` `enabledInt = parseInt(ARGS[1]).value_or(0) == 1`, `:1455-1462`
speed validation, `:1466` bezier existence, `:1471-1479` `setConfigForNode` before style check;
`:767` re-adds `linear` on config reset. Node tree and root defaults:
`src/config/shared/animation/AnimationTree.cpp:15-16,61-66`. Inheritance:
hyprutils v0.14.2 `src/animation/AnimationConfig.cpp:9,35,61`. Bezier store:
hyprutils v0.14.2 `src/animation/AnimationManager.cpp:17-21,54-57`. Printing:
`src/debug/HyprCtl.cpp:927-995` (`{:.2f}` per node and per bezier point).

## Evidence: control self-test (shape-complete trees match the oracle)

```
empty    MATCH nodes exp=35 got=35 missing=0 extra=0 | beziers exp=2 got=2 missing=0 extra=0
omarchy  MATCH nodes exp=35 got=35 missing=0 extra=0 | beziers exp=6 got=6 missing=0 extra=0
mixed    MATCH nodes exp=35 got=35 missing=0 extra=0 | beziers exp=3 got=3 missing=0 extra=0
snapshot files=79 digest=fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
realsnap DIFF  nodes exp=35 got=35 missing=15 extra=15 | beziers exp=6 got=2 missing=4 extra=0
HOST_SAFETY coredumps_before=1335 after=1335 delta=0
SUMMARY 3/4 match
```

`omarchy` is the operator's `animations { … }` block (5 beziers, 15 animations) placed at the root:
the control reproduces the oracle's 35 nodes and 6 beziers exactly, including the `workspaces, 0, 0,
ease` line (disable branch; `ease` is not a registered bezier, so Hyprland's table shows the disable
values, not a new bezier). `mixed` adds `bezier = default, …` redefinition, `enabled=2`, invalid
style, trailing comments, category depth, tab spacing and 4-decimal speeds. `realsnap` is the
counter's own snapshot: the 15 differing nodes are exactly the 15 nodes omarchy sets and the 4
missing beziers are exactly the 4 names it adds (`linear` is redefined with identical points, so it
does not differ). This is the measured reason the control scores 0/41.

## Scored receipts

Both runs, verbatim (counter stdout including the `exit=` line):

```
counter c1-r26 sha256:f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1RootOnly.py sha256:42ae2fb5df5470b04e2a42eeaa216cb43e3771f24a5cce66d49ce08c0c4edcb0
seed=433e52b606c71bbb
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
CASE BASE  FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (unperturbed)
CASE C00   FAIL nodes missing=16 extra=16 beziers missing=6 extra=0 (UNSOURCED+CATEGORY+BEZIER+ROOT)
CASE C01   FAIL nodes missing=18 extra=18 beziers missing=5 extra=0 (BEZIER+SOURCED+NEWSRC)
CASE C02   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (NEWSRC+COMMENT+INVALID)
CASE C03   FAIL nodes missing=15 extra=15 beziers missing=5 extra=0 (UNSOURCED+ROOT+CATEGORY+REBEZ)
CASE C04   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (VARIABLE+ORDER)
CASE C05   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (UNSOURCED+VARIABLE)
CASE C06   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (VARIABLE+ORDER+INVALID)
CASE C07   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (INVALID+ROOT)
CASE C08   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (BEZIER+INVALID+SOURCED)
CASE C09   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (BEZIER+INVALID+ROOT)
CASE C10   FAIL nodes missing=18 extra=18 beziers missing=4 extra=0 (SPACING+NEWSRC+VARIABLE)
CASE C11   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (SOURCED+VARIABLE)
CASE C12   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (ROOT+COMMENT+VARIABLE)
CASE C13   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (BEZIER+SPACING+ORDER)
CASE C14   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (ORDER+INVALID+CATEGORY+UNSOURCED)
CASE C15   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (BEZIER+DISABLE+COMMENT)
CASE C16   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (UNSOURCED+COMMENT+ROOT)
CASE C17   FAIL nodes missing=17 extra=17 beziers missing=5 extra=0 (ORDER+SOURCED+CATEGORY)
CASE C18   FAIL nodes missing=14 extra=14 beziers missing=4 extra=0 (COMMENT+VARIABLE+ROOT+UNSOURCED)
CASE C19   FAIL nodes missing=18 extra=18 beziers missing=6 extra=0 (BEZIER+SPACING+CATEGORY)
CASE C20   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (REBEZ+UNSOURCED)
CASE C21   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (CATEGORY+ORDER+VARIABLE)
CASE C22   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (UNSOURCED+INVALID+REBEZ)
CASE C23   FAIL nodes missing=18 extra=18 beziers missing=4 extra=0 (NEWSRC+DISABLE+SPACING)
CASE C24   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (ROOT+INVALID+UNSOURCED+ORDER)
CASE C25   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (CATEGORY+SOURCED+VARIABLE+ORDER)
CASE C26   FAIL nodes missing=15 extra=15 beziers missing=5 extra=0 (NEWSRC+INVALID+SOURCED+BEZIER)
CASE C27   FAIL nodes missing=15 extra=15 beziers missing=5 extra=0 (DISABLE+CATEGORY+COMMENT+REBEZ)
CASE C28   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (ROOT+UNSOURCED)
CASE C29   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (REBEZ+DISABLE+ROOT)
CASE C30   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (SPACING+NEWSRC+INVALID)
CASE C31   FAIL nodes missing=15 extra=15 beziers missing=5 extra=0 (BEZIER+INVALID+UNSOURCED)
CASE C32   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (ORDER+REBEZ+INVALID)
CASE C33   FAIL nodes missing=17 extra=17 beziers missing=5 extra=0 (ORDER+BEZIER)
CASE C34   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (SPACING+ROOT)
CASE C35   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (ORDER+UNSOURCED)
CASE C36   FAIL nodes missing=18 extra=18 beziers missing=4 extra=0 (SOURCED+SPACING+UNSOURCED)
CASE C37   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (ORDER+UNSOURCED)
CASE C38   FAIL nodes missing=15 extra=15 beziers missing=5 extra=0 (BEZIER+SOURCED+NEWSRC)
CASE C39   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (VARIABLE+DISABLE+SPACING+SOURCED)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
counter c1-r26 sha256:f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1RootOnly.py sha256:42ae2fb5df5470b04e2a42eeaa216cb43e3771f24a5cce66d49ce08c0c4edcb0
seed=99277b94d7cdba01
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
CASE BASE  FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (unperturbed)
CASE C00   FAIL nodes missing=15 extra=15 beziers missing=5 extra=1 (REBEZ+VARIABLE)
CASE C01   FAIL nodes missing=17 extra=17 beziers missing=5 extra=0 (NEWSRC+BEZIER+SOURCED)
CASE C02   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (NEWSRC+COMMENT+CATEGORY)
CASE C03   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (UNSOURCED+INVALID+REBEZ+SOURCED)
CASE C04   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (ROOT+SPACING+INVALID+DISABLE)
CASE C05   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (CATEGORY+ROOT+REBEZ+SOURCED)
CASE C06   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (SOURCED+VARIABLE)
CASE C07   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (COMMENT+UNSOURCED+SOURCED)
CASE C08   FAIL nodes missing=17 extra=17 beziers missing=5 extra=1 (REBEZ+ORDER+VARIABLE)
CASE C09   FAIL nodes missing=14 extra=14 beziers missing=4 extra=0 (UNSOURCED+ROOT)
CASE C10   FAIL nodes missing=17 extra=17 beziers missing=5 extra=0 (CATEGORY+ORDER+UNSOURCED)
CASE C11   FAIL nodes missing=15 extra=15 beziers missing=5 extra=1 (ROOT+REBEZ+NEWSRC)
CASE C12   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (COMMENT+INVALID+BEZIER)
CASE C13   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (SPACING+REBEZ)
CASE C14   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (VARIABLE+BEZIER+DISABLE)
CASE C15   FAIL nodes missing=17 extra=17 beziers missing=5 extra=0 (ORDER+BEZIER+UNSOURCED)
CASE C16   FAIL nodes missing=16 extra=16 beziers missing=6 extra=0 (BEZIER+CATEGORY)
CASE C17   FAIL nodes missing=15 extra=15 beziers missing=5 extra=1 (REBEZ+UNSOURCED+SOURCED)
CASE C18   FAIL nodes missing=15 extra=15 beziers missing=5 extra=0 (BEZIER+SOURCED+ROOT)
CASE C19   FAIL nodes missing=17 extra=17 beziers missing=5 extra=0 (CATEGORY+NEWSRC)
CASE C20   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (ORDER+INVALID+ROOT)
CASE C21   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (VARIABLE+NEWSRC+UNSOURCED)
CASE C22   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (UNSOURCED+NEWSRC)
CASE C23   FAIL nodes missing=17 extra=17 beziers missing=5 extra=0 (VARIABLE+CATEGORY)
CASE C24   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (COMMENT+INVALID+ORDER)
CASE C25   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (CATEGORY+SOURCED)
CASE C26   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (INVALID+COMMENT+SPACING)
CASE C27   FAIL nodes missing=17 extra=17 beziers missing=5 extra=0 (SPACING+CATEGORY)
CASE C28   FAIL nodes missing=17 extra=17 beziers missing=5 extra=0 (BEZIER+ORDER+SOURCED+NEWSRC)
CASE C29   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (INVALID+CATEGORY+ORDER+SPACING)
CASE C30   FAIL nodes missing=18 extra=18 beziers missing=6 extra=0 (SPACING+NEWSRC+CATEGORY+BEZIER)
CASE C31   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (ORDER+SOURCED)
CASE C32   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (VARIABLE+REBEZ+UNSOURCED)
CASE C33   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (DISABLE+SOURCED)
CASE C34   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (COMMENT+DISABLE+CATEGORY+REBEZ)
CASE C35   FAIL nodes missing=17 extra=17 beziers missing=6 extra=1 (ORDER+BEZIER+REBEZ+VARIABLE)
CASE C36   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (BEZIER+VARIABLE+UNSOURCED+SOURCED)
CASE C37   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (SPACING+ROOT+COMMENT)
CASE C38   FAIL nodes missing=18 extra=18 beziers missing=5 extra=0 (REBEZ+NEWSRC+SPACING+CATEGORY)
CASE C39   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (VARIABLE+UNSOURCED+SPACING+SOURCED)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```

## Why every case fails (and what that means for w2)

The snapshot is the operator's live four config roots (79 files). Its source graph has 40 files;
`~/.config/hypr/hyprland.conf` is node 0 of that graph and has 18 `source =` edges, no animation or
bezier key of its own. All 15 animation overrides and 4 of the 5 extra beziers are two hops away
(root → `~/.local/share/omarchy/default/hypr/looknfeel.conf`). Consequently:

- BASE misses 15 nodes / 4 beziers before any generated operation exists. No case can recover from
  that unless it happens to rewrite the same 15 nodes from the root; the generator's ROOT op appends
  exactly one animation line, never a full table.
- The counter's `sourced_files` list includes the root file, so an op that appends to
  `rng.choice(files)` can land in the root (~1/40 per choice). When it does, the control applies it
  correctly (e.g. run 2 C35's `REBEZ` shows `beziers missing=6 extra=1`: a root-visible bezier
  redefinition shifted one default point). It still fails, because the 15-node/3-bezier baseline
  difference is unchanged.
- `VARIABLE`, `NEWSRC` and `SOURCED` cases are unreachable by construction for this shape (variables
  are not expanded; new/sourced files are never opened). Even a perfect root-only reader cannot pass
  a case whose only table change is appended to a sourced file.
- The per-line semantics the control implements are the ones Hyprland actually uses (probe table
  above): `enabled` anything-but-1 disables with speed 1/bezier `default`; an invalid style is still
  stored; invalid node/bezier/speed/point lines are ignored by Hyprland. The last four are
  validation, which the shape forbids, so the control accepts them; this only matters when an
  `INVALID` line lands in the root, and it can only add mismatch. No observed case was decided by it.

For the data seats: a tool that wants 41/41 must follow the `source =` graph (including globs and
`~`), apply the handlers in file order with last-wins per animation node (not per line), and reproduce
the default tree (35 nodes / 2 beziers, including `__internal_fadeCTM` and the unset-node rendering
`overridden=false, enabled=true, speed 0.0, bezier ""`). The control's embedded default table is the
exact oracle JSON and can be lifted from the control file.

## Risks, limits, and what was not done

- No change to the counter, harness, `tools/`, or any lane file other than this report and the two
  named output paths. No git/jj command was run.
- Host safety: every oracle call went through `harness/oracle.py`; the coredump counter printed
  `delta=0` in the probe run, the self-test run and both scored runs (1335 → 1335 each time).
  No WAYLAND_DISPLAY / HYPRLAND_INSTANCE_SIGNATURE was inherited or set outside the counter's own
  `env -i` calls; no DRM card node was used.
- The embedded default table is host-independent at the pinned Hyprland commit (nodes and defaults
  are `AnimationTree.cpp` literals) but was captured once in this environment; the counter's
  `ORACLE_CHECK base_twice` line confirmed the live table was stable inside each run.
- No tool was installed or upgraded.
- Result is a measured miss, not a blocker. The control is complete for its shape; there is no
  root-only tweak that changes the verdict on this snapshot.

## Files

- `.ufo/waves/round-26/controls/K1RootOnly.py` — control (sha256 `42ae2fb5…4edcb0`).
- `.ufo/waves/round-26/controls/K1RootOnly.txt` — both receipts verbatim (sha256 `1eebdafd…fd4432`).
- `.ufo/waves/round-26/w1/reports/K1RootOnly.md` — this report.
- Scratch (not lane): `/fast/scratch/hyaku/mado-r26/K1RootOnly/{probe.py,selftest.py,probe/probe-results.json,run1.txt,run2.txt}`.

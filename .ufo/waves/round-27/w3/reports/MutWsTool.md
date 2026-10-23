# MutWsTool — empirical mutation check of `tools/mado-wsrules.py` without the counter

Seat: MadoR27.MutWsTool (residual wave w3). Assignment: three single-fault mutants of the landed C1 tool,
run against the 13 oracle probe trees; no counter invocation.

## Scope and method

- Isolated scratch: `/fast/scratch/hyaku/mado-r27/mutwstool/`. No writes outside that directory and this
  report. The lane tool, counters, harness and probe trees were read-only.
- Pristine copy: `pristine.py`, copied from
  `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-wsrules.py`;
  sha256 `722c7ae47eaee57eda4c6a223f4dad6fc585018453c2f7a2fd26c52d1e006008` — identical to the landed rev
  `48b9434a0b0619b3896c9d80e8288ec2226c9ed8` file and to the live lane file at audit end.
- Detector: `detect.py` (sha256 `f92702facf5851718f77681a70d313bb5a2a0a53c66d384f77abeee811701c14`).
  For each case it runs `python3 -I <tool> --home /fast/scratch/hyaku/mado-r27/probe/ScoutOracleWsSemantics/<case>/tree`
  (timeout 120 s, non-zero exit or unparsable stdout counted as FAIL), `json.loads` the stdout and compares
  with `==` against the expected `workspacerules` array read from that directory's `results.json`.
  Case set (13): bools, empty, enabled, gaps, layoutopt, merge, mergeerr, namevsid, norules, sameline,
  substr, unknown, whitespace. No network, no Hyprland, no harness, no counter.
- Baseline (pristine) first and repeated after all mutant runs: **13/13 PASS**, so a mutant mismatch is a
  kill, not a baseline artifact.

```
pristine: 13/13 PASS  sha256=722c7ae4…6008
```

## Mutants (exactly one behavioural fault each; diffs produced with `diff -u pristine.py M*.py`)

**M1 — repeated-selector merge MOVES the row to the end** (`handle_workspace_rules`, after `merge_left`):

```diff
             merge_left(existing, rule)
+            st.rules.remove(existing)
+            st.rules.append(existing)
             return
```

sha256 `da5a629d6114bcaa8a637312a6d12b8d85ee1952280884bccb5b13c2c9c453d4`

**M2 — 2-value gaps shorthand faces swapped** (`parse_gaps`, `count == 2`):

```diff
-        return (first, second, first, second)
+        return (second, first, second, first)
```

sha256 `2a991723d1cba55d8b67e58b424b35f4c72e4e3672f69a82029521ee6a3cb894`

**M3 — bool parsing by exact word instead of prefix** (`parse_int`):

```diff
-    if val.startswith("true") or val.startswith("on") or val.startswith("yes"):
+    if val in ("true", "on", "yes"):
         return 1
-    if val.startswith("false") or val.startswith("off") or val.startswith("no"):
+    if val in ("false", "off", "no"):
         return 0
```

sha256 `23f095b90e3061f0278ca04af2542fa54073f93bd2d21a3dba0cadcf1bc00afc`

## Results

| Mutant | Pass | Mismatch | Mismatching cases (order) | Verdict |
|---|---|---|---|---|
| M1 merge-moves-to-end | 10/13 | 3 | merge, namevsid, whitespace | **KILLED** |
| M2 2-value gaps swapped | 11/13 | 2 | gaps, sameline | **KILLED** |
| M3 exact-word bools | 12/13 | 1 | bools | **KILLED** |

Killed = at least one probe case's actual array differs from Hyprland v0.56.2's expected array.

### M1 — first mismatch: `merge`

Expected order `["3", "1"]`, actual `["1", "3"]` (the second `workspace = 3` line merged and moved entry 3
behind entry 1). Full arrays:

```
EXPECTED [{"border": true, "enabled": true, "gapsIn": [1,1,1,1], "shadow": false, "workspaceString": "3"},
          {"border": true, "enabled": true, "gapsIn": [10,10,10,10], "monitor": "DP-1", "persistent": true, "workspaceString": "1"}]
ACTUAL   [{"border": true, "enabled": true, "gapsIn": [10,10,10,10], "monitor": "DP-1", "persistent": true, "workspaceString": "1"},
          {"border": true, "enabled": true, "gapsIn": [1,1,1,1], "shadow": false, "workspaceString": "3"}]
```

Canonical diff of the first element block:

```
--- expected
+++ actual
@@
- {"border": true, "enabled": true, "gapsIn": [1,1,1,1], "shadow": false, "workspaceString": "3"},
- {"border": true, "enabled": true, "gapsIn": [10,10,10,10], "monitor": "DP-1", "persistent": true, "workspaceString": "1"}
+ {"border": true, "enabled": true, "gapsIn": [10,10,10,10], "monitor": "DP-1", "persistent": true, "workspaceString": "1"},
+ {"border": true, "enabled": true, "gapsIn": [1,1,1,1], "shadow": false, "workspaceString": "3"}
```

Order evidence for the other two mismatches (same fault, no other field differs):

- `namevsid`: expected `['1','name:1','name:code','2','special:scratch','special','name:scratch','01']`,
  actual `['1','name:1','2','special:scratch','special','name:scratch','01','name:code']` — the merged
  `name:code` row moved to the tail. First differing index 2: expected
  `{"defaultName":"coding","monitor":"HDMI-A-1","persistent":true,"workspaceString":"name:code"}` vs actual
  `{"defaultName":"code","workspaceString":"2"}` (index shift).
- `whitespace`: expected `['1','2','name: foo','name:foo','name:my ws','3','5','w[tv1]','w[tv1] s[false]','r[2-4]']`,
  actual `['1','2','name: foo','name:my ws','name:foo','3','5','w[tv1]','w[tv1] s[false]','r[2-4]']` — the
  second `name:foo` line merged and moved past `name:my ws`.

### M2 — first mismatch: `gaps`

`workspace = 15, gapsin:8 2` — expected `gapsIn [8,2,8,2]` (top,bottom=8; right,left=2), actual
`gapsIn [2,8,2,8]`. Everything else in the array is identical (10/10 entries, same order).

```
EXPECTED {"enabled": true, "gapsIn": [8, 2, 8, 2], "workspaceString": "15"}
ACTUAL   {"enabled": true, "gapsIn": [2, 8, 2, 8], "workspaceString": "15"}
```

```
--- expected
+++ actual
@@
   "gapsIn": [
+   2,
    8,
    2,
-   8,
-   2
+   8
   ],
   "workspaceString": "15"
```

Second mismatch `sameline`, same fault on `gapsout`: `{"borderSize": 6, "gapsOut": [8,2,8,2], "workspaceString": "6"}`
expected vs `{"borderSize": 6, "gapsOut": [2,8,2,8], "workspaceString": "6"}` actual. 1-value, 3-value and
4-value shorthands are unaffected by this mutant and stayed correct.

### M3 — first mismatch: `bools`

Line `workspace = 2, persistent:nope, border:trueish` is kept by the pristine tool
(`persistent:false, border:true`) but dropped wholesale by exact-word parsing (both values become parse
failures, and `assign_rule` returning False drops the line). Expected 4 entries, actual 3:

```
EXPECTED [{"border": true, "decorate": false, "enabled": true, "persistent": true, "rounding": true, "shadow": false, "workspaceString": "1"},
          {"border": true, "enabled": true, "persistent": false, "workspaceString": "2"},
          {"border": false, "enabled": true, "persistent": true, "workspaceString": "3"},
          {"border": false, "decorate": true, "enabled": true, "persistent": false, "rounding": false, "shadow": false, "workspaceString": "5"}]
ACTUAL   [{"border": true, "decorate": false, "enabled": true, "persistent": true, "rounding": true, "shadow": false, "workspaceString": "1"},
          {"border": false, "enabled": true, "persistent": true, "workspaceString": "3"},
          {"border": false, "decorate": true, "enabled": true, "persistent": false, "rounding": false, "shadow": false, "workspaceString": "5"}]
```

```
--- expected
+++ actual
@@
- },
- {
-  "border": true,
-  "enabled": true,
-  "persistent": false,
-  "workspaceString": "2"
  },
```

## Counter-population question

Not triggered: all three mutants are killed by the 13 oracle probe trees, so the "would the frozen C1 v4
population kill it" test is moot for this probe.

Two grounded observations from reading `.ufo/waves/round-27/c1/count-v4.py` (static read only; no counter
run, per assignment):

- v4 emits MERGE (repeated selector, `rule_lines`), GAPSHORT (1-3 value gaps, `gaps()`), and BOOLWORD
  (`boolv()`) cases, and compares entry-by-entry in order. On that basis M1 and M2 are very plausibly
  killed by the counter population too (a merged row not at the tail reorders the array; a 2-value gap with
  distinct random values has a wrong face map). [INFERENCE from the generator code, not measured]
- v4's BOOLWORD values are drawn only from `BOOLS_T = ["true","yes","on","1"]` and
  `BOOLS_F = ["false","no","off","0"]` — all exact words. Exact-word parsing (M3) parses those all
  correctly, so the counter population on its own would **not** distinguish prefix from exact-word bool
  parsing; the probe `bools` case (`nope`, `trueish`) is what kills M3. Coverage observation for the L1,
  not a contract change and not grounds to alter the frozen predicate.

## Additional probe-population coverage (raised by MadoR27.CritC1Claim, 2026-10-23)

Two dispatch/table shapes outside my three assigned mutants, checked against the same 13 trees:

- **Exact-key dispatch vs substring dispatch is killed by this probe population.** The `substr` tree
  contains `notgapsin:4`, `myborder:false`, `xdefault:true` and `prelayoutopt:orientation:top`; the
  pristine tool's substring search passes it, and `results.json` expects ws 1 `gapsIn [4,4,4,4]` and ws 2
  `border false` — i.e. Hyprland itself matches those keys as substrings. An exact-key mutant would drop
  both fields and mismatch. The frozen v4 generator emits only exact keys (`C1 v4` `rule_items`), which is
  why this witness lives only in the probe set.
- **`on-created-empty:` slice defect is invisible to this probe population.** The landed tool slices at
  `field[delimiter + 16:]` (line 576) while the literal `"on-created-empty:"` is 17 characters, so the
  leading `:` survives. No probe tree contains an `on-created-empty` line (grep over the 13
  `tree/.config/hypr/hyprland.conf` files: 0 hits), so a mutant or the landed defect in this slice cannot
  be killed by these 13 trees; the counter's ONEMPTY feature is what exercises it. Empirical check in
  scratch only (no oracle), fixture `/fast/scratch/hyaku/mado-r27/mutwstool/onempty/.config/hypr/hyprland.conf`:

  ```
  $ cat onempty/.config/hypr/hyprland.conf
  workspace = 1, on-created-empty:kitty
  workspace = 2, persistent:true, on-created-empty:alacritty -e btop

  $ python3 -I pristine.py --home onempty
  [{"workspaceString": "1", "enabled": true, "onCreatedEmpty": "[workspace 1] :kitty"},
   {"workspaceString": "2", "enabled": true, "persistent": true, "onCreatedEmpty": "[workspace 2] :alacritty -e btop"}]
  ```

  Observed command text is `[workspace 1] :kitty`; the source-derived expectation (C1 claim critic,
  `SrcWsRuleLegacy.bin:1703-1704,1753-1755` using `.length()`) is `[workspace 1] kitty`. The difference is
  exactly the retained `:` — a one-character slice offset, reproduced by execution here, with the oracle
  expectation itself still resting on the critic's source read. This is not one of M1-M3, and no code was
  changed. It also means the probe population has a gap the counter's ONEMPTY population covers.

## Restoration evidence

| Artifact | sha256 before | sha256 after |
|---|---|---|
| lane `tools/mado-wsrules.py` | `722c7ae4…6008` | `722c7ae4…6008` (unchanged; also `git`-free, no mutations run) |
| scratch `pristine.py` | `722c7ae4…6008` | `722c7ae4…6008` |
| `M1.py` | copy `722c7ae4…6008` | `da5a629d…53d4` (intended mutant) |
| `M2.py` | copy `722c7ae4…6008` | `2a991723…b894` (intended mutant) |
| `M3.py` | copy `722c7ae4…6008` | `23f095b9…0afc` (intended mutant) |

Pristine re-run after all mutant runs: **13/13 PASS, FIRST_MISMATCH none**, same sha256. The mutants are
the intended artifacts and are left in place under the scratch directory; no bytes outside the scratch
directory and this report were written. No tools were installed or upgraded.

## Files

- `/fast/scratch/hyaku/mado-r27/mutwstool/pristine.py` — pristine copy (sha `722c7ae4…6008`)
- `/fast/scratch/hyaku/mado-r27/mutwstool/M1.py` — merge-moves-to-end (sha `da5a629d…53d4`)
- `/fast/scratch/hyaku/mado-r27/mutwstool/M2.py` — 2-value gaps swapped (sha `2a991723…b894`)
- `/fast/scratch/hyaku/mado-r27/mutwstool/M3.py` — exact-word bools (sha `23f095b9…0afc`)
- `/fast/scratch/hyaku/mado-r27/mutwstool/detect.py` — detector (sha `f92702fa…1c14`)

# ScoutOracleWsSemantics

VERDICT: Hyprland v0.56.2 keeps one `workspacerules` row per exact trimmed selector, in first-seen order; a later line overrides only fields it sets and does not move the row. `workspace = 3` and `workspace = 4,` still emit a row. Unknown keys are silent unless the token contains a known key as a substring. A bad gap, bordersize, bool, or `layoutopt` drops that whole line, parsing continues, and gap/bordersize errors are just the bad value. `enabled` is always JSON `true` and is not a rule key. `layoutopt`/`layout`/`animation` are accepted but absent from `workspacerules -j`.

## Method

Oracle: `oracle(tree, work, ['workspacerules','configerrors'])` imported from `.ufo/waves/round-27/harness/oracle.py`. Binary: `Hyprland --version` → `Hyprland 0.56.2` commit `efb50993780079460b0cbed1363e2166a2de1d9f` (the pin). Trees and raw JSON: `/fast/scratch/hyaku/mado-r27/probe/ScoutOracleWsSemantics/<case>/tree/.config/hypr/hyprland.conf` and `results.json`.

Command (13 cases, 4 at a time, 13.59 s, all `ok`):

```
env -i PATH=/usr/bin HOME=/tmp timeout 900 prlimit --core=0 --as=8000000000 -- python3 -I /fast/scratch/hyaku/mado-r27/probe/ScoutOracleWsSemantics/run.py
```

`coredumpctl` count of `/usr/bin/Hyprland`: 1338 before, 1338 after, delta 0. No crash inputs (no empty selector, no huge numbers, no source cycles). Error paths below are the oracle's work copy; line numbers match the tree file. A clean run's `configerrors` is `[""]`, not `[]`.

JSON shape, every row: `workspaceString` then `enabled` (always present). Other keys appear only when set, in this order: `monitor`, `default`, `persistent`, `gapsIn`, `gapsOut`, `borderSize`, `border`, `rounding`, `decorate`, `shadow`, `defaultName`. Gaps are `[top, right, bottom, left]` integers. Bools are JSON bools. `persistent:false` is present as `false`; an unset persistent is omitted.

## Merge (repeated selector)

Tree `merge`:

```
workspace = 3, gapsin:1, border:true
workspace = 1, gapsin:5, monitor:DP-1, border:true, persistent:false
workspace = 1, gapsin:10, persistent:true
workspace = 3, shadow:false
```

`configerrors`: `[""]`

```json
[
  {"workspaceString":"3","enabled":true,"gapsIn":[1,1,1,1],"border":true,"shadow":false},
  {"workspaceString":"1","enabled":true,"monitor":"DP-1","persistent":true,"gapsIn":[10,10,10,10],"border":true}
]
```

Observed: one row per selector, not per line. Order is first-seen (`3` then `1`); the later `shadow` line does not move `3`. Later line overrides fields it sets (`gapsIn` 5→10, `persistent` false→true) and leaves unset fields (`monitor`, `border` on `1`; `gapsIn`/`border` on `3`).

Tree `sameline` (same line, last duplicate wins; 2-value gaps):

```
workspace = 1, persistent:true, gapsin:5, gapsin:9, border:false
workspace = 2, border:false, rounding:false, decorate:false, shadow:false
workspace = 6, gapsout:8 2, bordersize:6
```

`configerrors`: `[""]`

```json
[
  {"workspaceString":"1","enabled":true,"persistent":true,"gapsIn":[9,9,9,9],"border":false},
  {"workspaceString":"2","enabled":true,"border":false,"rounding":false,"decorate":false,"shadow":false},
  {"workspaceString":"6","enabled":true,"gapsOut":[8,2,8,2],"borderSize":6}
]
```

`border`/`rounding`/`shadow`/`decorate:false` print as JSON `false` (user-facing polarity, not the internal `noBorder` flag).

Tree `mergeerr` (a bad later line does not delete or patch the earlier row; the next selector still lands):

```
workspace = 1, gapsin:5, monitor:DP-1
workspace = 1, gapsin:zzz, persistent:true
workspace = 2, persistent:true
```

`configerrors`: `["Config error in file …/mergeerr/work/home/.config/hypr/hyprland.conf at line 2: zzz"]`

```json
[
  {"workspaceString":"1","enabled":true,"monitor":"DP-1","gapsIn":[5,5,5,5]},
  {"workspaceString":"2","enabled":true,"persistent":true}
]
```

`persistent` on the bad line is not applied. The error text is `zzz`, not a sentence.

## `workspace = 3` with no rules

Tree `norules`:

```
workspace = 3
workspace = 4,
workspace = 5, persistent:true
```

`configerrors`: `[""]`

```json
[
  {"workspaceString":"3","enabled":true},
  {"workspaceString":"4","enabled":true},
  {"workspaceString":"5","enabled":true,"persistent":true}
]
```

Both a bare id and a trailing comma create a row. No error. Empty baseline (`empty`: a comment plus `monitor=,preferred,auto,1`) returns `workspacerules: []` and `configerrors: [""]`.

## Unknown keys, and keys that only look unknown

Tree `unknown`:

```
workspace = 1, notakey:true, persistent:true
workspace = 2, foobar:1, gapsin:5
workspace = 6, enabled:false, persistent:true
workspace = 8, floatgaps:4, border:true
workspace = 9, totally-unknown, gapsout:3
```

`configerrors`: `[""]`. Every line kept. `notakey`, `foobar`, `enabled`, `floatgaps`, `totally-unknown` add no field and raise no error. Neighboring real fields still apply (`persistent`, `gapsIn` 5, `border`, `gapsOut` 3). `enabled` stays `true` on all five rows (see below).

Tree `substr` (match is a substring, not a token):

```
workspace = 1, notgapsin:4
workspace = 2, myborder:false
workspace = 3, xdefault:true, persistent:true
workspace = 4, prelayoutopt:orientation:top, gapsin:2
```

`configerrors`: `[""]`

```json
[
  {"workspaceString":"1","enabled":true,"gapsIn":[4,4,4,4]},
  {"workspaceString":"2","enabled":true,"border":false},
  {"workspaceString":"3","enabled":true,"default":true,"persistent":true},
  {"workspaceString":"4","enabled":true,"gapsIn":[2,2,2,2]}
]
```

`notgapsin:4` sets `gapsIn`. `myborder:false` sets `border:false`. `xdefault:true` sets `default:true`. `prelayoutopt:…` does not error and does not add a JSON field (`layoutopt` is not printed; see layoutopt).

## Invalid gaps

Tree `gaps`:

```
workspace = 20, gapsin:2, persistent:true
workspace = 1, gapsin:abc, persistent:true
workspace = 2, gapsin:5, gapsout:nope
workspace = 7, gapsin:4
workspace = 8, gapsin:
workspace = 9, gapsin:1 2 3
workspace = 10, gapsin:1 2 3 4
workspace = 11, gapsin:1 2 3 4 9
workspace = 12, gapsin:1.5
workspace = 13, gapsin:-3
workspace = 14, gapsin:1,2,3,4
workspace = 15, gapsin:8 2
workspace = 16, persistent:true, gapsin:zz, border:true
workspace = 17, gapsin:1  2
workspace = 18, bordersize:abc, persistent:true
workspace = 19, gapsout:0
```

Rows present, in source order, skipping failed lines: `20, 7, 9, 10, 11, 12, 13, 14, 15, 19`.

```json
[
  {"workspaceString":"20","enabled":true,"persistent":true,"gapsIn":[2,2,2,2]},
  {"workspaceString":"7","enabled":true,"gapsIn":[4,4,4,4]},
  {"workspaceString":"9","enabled":true,"gapsIn":[1,2,3,2]},
  {"workspaceString":"10","enabled":true,"gapsIn":[1,2,3,4]},
  {"workspaceString":"11","enabled":true,"gapsIn":[1,2,3,4]},
  {"workspaceString":"12","enabled":true,"gapsIn":[1,1,1,1]},
  {"workspaceString":"13","enabled":true,"gapsIn":[-3,-3,-3,-3]},
  {"workspaceString":"14","enabled":true,"gapsIn":[1,1,1,1]},
  {"workspaceString":"15","enabled":true,"gapsIn":[8,2,8,2]},
  {"workspaceString":"19","enabled":true,"gapsOut":[0,0,0,0]}
]
```

`configerrors` (exact strings):

- line 2 (`gapsin:abc`): `… at line 2: abc`
- line 3 (`gapsout:nope`): `… at line 3: nope` — `gapsin:5` on that same line is discarded with it
- line 5 (`gapsin:`): `… at line 5:` (empty payload)
- line 13 (`gapsin:zz` after `persistent:true`): `… at line 13: zz` — `persistent` and `border` on that line discarded
- line 14 (`gapsin:1  2`, two spaces): `… at line 14: 1  2`
- line 15 (`bordersize:abc`): `… at line 15: abc`

Accepted shapes: one int copies to all four sides; two ints are vertical then horizontal `[8,2,8,2]`; three are top, horizontal, bottom `[1,2,3,2]`; four are top, right, bottom, left. A fifth int is dropped with no error (`1 2 3 4 9` → `[1,2,3,4]`). `1.5` becomes `1`. `-3` is kept. Comma-separated `1,2,3,4` is one gap of `1` plus three ignored tokens (`[1,1,1,1]`, no error), because the rule list already splits on commas. `gapsout:0` is stored as zeros, not omitted. A failed line does not stop the file (`20` before the errors and `7`/`19` after them both survive).

`whitespace` line `workspace = 4, gapsin: 6` (space after the colon) is the same failure: that selector is absent, error `… at line 9:  6` (payload is space + `6`).

## `enabled`

Tree `enabled`:

```
workspace = 1, persistent:true
workspace = 2, enabled:false
workspace = 3, enabled:0, gapsin:3
workspace = 4, enabled:true, persistent:false
workspace = 5, enabled:no
```

`configerrors`: `[""]`. All five rows have `"enabled": true`. `enabled:false`, `:0`, `:true`, and `:no` do not change it and do not error. `persistent:false` does record `"persistent": false`. `enabled:0` does not disturb `gapsin:3`.

No probed config made `enabled` false.

## `layoutopt` (and `layout` / `animation`)

Tree `layoutopt`:

```
workspace = 1, layoutopt:orientation:top, gapsin:2
workspace = 1, layoutopt:orientation:left, layoutopt:mfact:0.3, persistent:true
workspace = 2, layoutopt:nocolon, persistent:true
workspace = 3, layout:master, animation:slidevert, persistent:true
workspace = 4, animations:slide, persistent:true
workspace = 5, layoutopt:orientation:top:extra, gapsin:1
```

```json
[
  {"workspaceString":"1","enabled":true,"persistent":true,"gapsIn":[2,2,2,2]},
  {"workspaceString":"3","enabled":true,"persistent":true},
  {"workspaceString":"4","enabled":true,"persistent":true},
  {"workspaceString":"5","enabled":true,"gapsIn":[1,1,1,1]}
]
```

`configerrors`: one line, `… at line 3: Invalid workspace rule found: layoutopt:nocolon`.

Observed: a valid `layoutopt` (including two on one line, a later line on the same selector, and a value with an extra colon) does not error and does not appear in JSON. The two `1` lines still merge (`gapsIn` from the first, `persistent` from the second). `layoutopt` without a second colon drops the whole line (`persistent` on workspace `2` is gone) and the error text is the full sentence, unlike gaps. `layout:master` and `animation:slidevert` leave only `persistent` in JSON and do not error. `animations:slide` (plural) behaves the same through these two verbs: no error, no extra field. Whether `layout`/`animation` were stored cannot be told from `workspacerules` + `configerrors`; `layoutopt`'s invalid form shows that key is real.

## Whitespace inside selectors

Tree `whitespace`:

```
workspace =  1, gapsin:5
workspace = 1 , gapsin:8
workspace =	2,gapsin:3
workspace = name: foo, persistent:true
workspace = name:foo, gapsin:1
workspace = name:my ws, gapsin:4
workspace = name:foo , persistent:true
workspace =  3 , rounding:false
workspace = 4, gapsin: 6
workspace = 5, monitor: DP-1, defaultName: spaced
workspace = w[tv1], gapsin:0
workspace = w[tv1] s[false], gapsin:1
workspace = r[2-4], persistent:true
```

`workspaceString`s: `1`, `2`, `name: foo`, `name:foo`, `name:my ws`, `3`, `5`, `w[tv1]`, `w[tv1] s[false]`, `r[2-4]`. Workspace `4` dropped (error above).

```json
[
  {"workspaceString":"1","enabled":true,"gapsIn":[8,8,8,8]},
  {"workspaceString":"2","enabled":true,"gapsIn":[3,3,3,3]},
  {"workspaceString":"name: foo","enabled":true,"persistent":true},
  {"workspaceString":"name:foo","enabled":true,"persistent":true,"gapsIn":[1,1,1,1]},
  {"workspaceString":"name:my ws","enabled":true,"gapsIn":[4,4,4,4]},
  {"workspaceString":"3","enabled":true,"rounding":false},
  {"workspaceString":"5","enabled":true,"monitor":" DP-1","defaultName":"spaced"},
  {"workspaceString":"w[tv1]","enabled":true,"gapsIn":[0,0,0,0]},
  {"workspaceString":"w[tv1] s[false]","enabled":true,"gapsIn":[1,1,1,1]},
  {"workspaceString":"r[2-4]","enabled":true,"persistent":true}
]
```

Leading/trailing whitespace and a leading tab on the selector are trimmed, so `  1` and `1 ` merge (last `gapsIn` is 8) and the tab-prefixed `2` is `"2"`. An internal space is part of the key: `name: foo` ≠ `name:foo`, and `name:my ws` stays. `name:foo ` (space before the comma) merges into `name:foo`. A space between selector props is kept: `w[tv1]` and `w[tv1] s[false]` are two rows. `monitor: DP-1` stores `" DP-1"` (space kept). `defaultName: spaced` stores `"spaced"` (trimmed).

## `name:` vs id

Tree `namevsid`:

```
workspace = 1, gapsin:5, persistent:true
workspace = name:1, gapsin:9, monitor:DP-1
workspace = name:code, persistent:true, defaultName:coding
workspace = 2, defaultName:code
workspace = special:scratch, gapsout:0
workspace = special, gapsin:1
workspace = name:scratch, persistent:true
workspace = 01, border:true
workspace = name:code, monitor:HDMI-A-1
```

`configerrors`: `[""]`

```json
[
  {"workspaceString":"1","enabled":true,"persistent":true,"gapsIn":[5,5,5,5]},
  {"workspaceString":"name:1","enabled":true,"monitor":"DP-1","gapsIn":[9,9,9,9]},
  {"workspaceString":"name:code","enabled":true,"monitor":"HDMI-A-1","persistent":true,"defaultName":"coding"},
  {"workspaceString":"2","enabled":true,"defaultName":"code"},
  {"workspaceString":"special:scratch","enabled":true,"gapsOut":[0,0,0,0]},
  {"workspaceString":"special","enabled":true,"gapsIn":[1,1,1,1]},
  {"workspaceString":"name:scratch","enabled":true,"persistent":true},
  {"workspaceString":"01","enabled":true,"border":true}
]
```

`1`, `name:1`, and `01` are three rows. `name:code` does not merge with id `2` or with `defaultName:code`; `defaultName` is a field on the row, not a second selector. The second `name:code` line merges into the first (`monitor` added, `defaultName`/`persistent` kept). `special`, `special:scratch`, and `name:scratch` are three rows. The JSON does not expose the resolved numeric id.

## Bool spellings

Tree `bools`:

```
workspace = 1, persistent:yes, border:on, rounding:true, decorate:false, shadow:no
workspace = 2, persistent:nope, border:trueish
workspace = 3, persistent:2, border:0
workspace = 4, persistent:abc
workspace = 5, persistent:false, border:off, rounding:no, decorate:yes, shadow:0
```

```json
[
  {"workspaceString":"1","enabled":true,"persistent":true,"border":true,"rounding":true,"decorate":false,"shadow":false},
  {"workspaceString":"2","enabled":true,"persistent":false,"border":true},
  {"workspaceString":"3","enabled":true,"persistent":true,"border":false},
  {"workspaceString":"5","enabled":true,"persistent":false,"border":false,"rounding":false,"decorate":true,"shadow":false}
]
```

`configerrors`: `… at line 4: Failed parsing a workspace rule`. Workspace `4` is absent; workspace `5` still lands.

`yes`/`on`/`true` → true. `no`/`off`/`false`/`0` → false. `persistent:2` → true. `persistent:nope` → false and `border:trueish` → true, with no error (prefix match, not an exact word). `abc` is the generic failure string, not the token.

## Source alignment (not oracle)

Pinned `efb5099` `src/config/legacy/ConfigManager.cpp` `handleWorkspaceRules` and `src/debug/HyprCtl.cpp` `getWorkspaceRuleData` match the observations: `replaceOrAdd` keys on `m_workspaceString`; `mergeLeft` overwrites only set fields and does not touch `m_enabled`; the JSON printer omits `m_layout`, `m_layoutopts`, `m_floatGaps`, and `m_animationStyle`; gap/bordersize failures use the comma operator so the returned text is only the value (`return "Error parsing…", rule.substr(…)`), while `layoutopt` without a colon returns one concatenated string. Wiki pin `ecc06f3b6605` `content/Configuring/Workspace-Rules.md` lists neither `enabled` nor `layoutopt`, types gaps as a single int, and heads the animation row `animations` while its own example uses `animation:slidevert`.

## Not probed / unresolved

- Empty selector (`workspace = , …`) skipped as crash-adjacent.
- Overflowing numbers skipped (host rule).
- `on-created-empty` not probed.
- `layoutopt` key merge (override vs accumulate) and whether `layout:` / `animation:` are stored are invisible to these two verbs. Invalid `layoutopt` shows the key exists; a well-formed `layout`/`animation` is indistinguishable here from an unknown key.
- Nothing in these trees set `enabled` to false. The pinned parser never writes that flag; this probe did not search other writers.

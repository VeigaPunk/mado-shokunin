# Who owns each option: the whole-tree config-option table

source: S218, S219, S220, S162, S173
verified-at: 2026-10-25
recheck: on-release

Lane: mado-shokunin. Round: 39 (claim C3; capability C2 `tools/mado-options.py`;
considerthese/2026-10-24.md proposal 4, "the config-option table — who owns each key,
checked against getoption"). Hyprlang era only: the host runs Hyprland v0.56.2 with
hyprlang 0.6.8 and a `.conf` tree (`knowledge/hyprland-config-era-r12.md`); nothing here
describes the Lua `hl.config()` surface.

ground: a new edge class under the held config plane — ownership resolved for every option
key of the tree (key → owner file:line, layer) instead of the six hand-proved keys of
`knowledge/hyprctl-verification-layer.md` §5, plus the parser boundary that decides which
`key = value` lines are options at all.

## Held, cited not restated

The include order and "the last file to set a key wins" (`SKILL.md` config-plane map;
current form in `knowledge/config-drift-r12.md`), the 56 live claim→`getoption` pairs and
the five divergence classes (`knowledge/hyprctl-verification-layer.md` §2-§3), the hyprlang
source-graph and comment grammar (`knowledge/bind-table-r25.md`), and block-scope key
namespacing (`knowledge/executor-test-sufficiency.md`). This entry applies them.

## §1 The resolution rule, from the documentation

**OBS** S218 (0.56.0 hyprlang page, `## Syntax` → `### Line Style`): "Options can be specified only once (if you do it more times, the previous one will be overwritten)".

**OBS** S220 (0.54.0 Keywords page, `## Sourcing (multi-file)`): "Meaning lines above the source = will be parsed first, then lines inside ~/.config/hypr/myColors.conf, then lines below."

**INF** Together: the effective declaration of an option is the last one in one linear,
depth-first parse order across `source =` includes. The owner of a key is therefore a
property of the whole source graph, not of any one file — which is why a per-file grep
cannot answer "who owns `general:gaps_out`", and why the tool walks the graph.

## §2 Which lines are options — the parser boundary

**OBS** S162 (`src/config/legacy/ConfigManager.cpp` @ `efb5099`, the host's commit) registers
keyword handlers at `:601-623` — among them `m_config->registerHandler(&::handleBind, "bind", {true});`
and `gesture`/`env` with the same `{true}` (allow-flags) option — and keyed special
categories at `:518` (`device`), `:567` (`monitorv2`), `:591`
(`m_config->addSpecialCategory("windowrule", {.key = "name"});`), `:595` (`layerrule`) and
`:626` (`plugin`).

**OBS** S173 (hyprlang v0.6.8 `src/config.cpp`): a line is first tried as a registered option
(`:832` `configSetValueSafe(LHS, RHS)`); only when that fails are handlers tried (`:839`), and
an allow-flags handler matches any LHS that starts with its name and holds no `:` (`:869`,
"avoid cases where a category is called the same as a handler").

**INF** So `bindd`, `bindeld`, `bindmd`, `envd` are handler calls, not options, and the fields
of a `windowrule { name = … }` block are per-instance rule data, not global options. A
resolver that excludes directives by exact keyword match lists them as options.

**OBS** S219 (own-work): on the host tree the wave-built tool (`cee78d99…`, exact-match
exclusion) printed 79 rows; the repaired tool prints 70 — the 9 removed rows are
`binddr`, `bindeld`, `bindld`, `bindmd` and five `windowrule:*` fields
(`.ufo/waves/round-39/c2/real-tree-diff.txt`). The repaired rule is exercised by two
selftest assertions that each kill a one-line mutant (`c2/selftest-mutA.txt`,
`c2/selftest-mutB.txt`, both 69/71).

## §3 The host's table (static, measured)

**OBS** S219 (own-work receipt `.ufo/waves/round-39/fetch/S219.receipt.txt`, the tool at
`4ec582e` over the 49 host config files copied read-only into
`.ufo/waves/round-39/w1/ExecOptionsRealTree/host-tree/`): "rows=70 owner files=6 layers defaults=57 user=7 toggles=4 theme=2".

**INF** 57 of the 70 options the host sets are owned by the read-only Omarchy defaults tree
(47 by `default/hypr/looknfeel.conf` alone); the operator's own surface owns 13: 7 in
`~/.config/hypr/input.conf` (layout `br`, `compose:caps`, repeat 40/250, numlock, two
touchpad keys), 4 in the `window-no-gaps` toggle (gaps, border, rounding = 0) and 2 in the
current theme (the two active-border colours). Editing a defaults-owned key in
`~/.config/hypr/` changes the live value only if no later declarer exists — the table
names that later declarer when there is one.

**OBS** The table reproduces the held ownership proofs row for row: `general:gaps_out` →
`window-no-gaps.conf:3` (toggles), `input:kb_layout` → `.config/hypr/input.conf:10` (user),
`general:col.active_border` → `theme/hyprland.conf:4` (theme)
(`knowledge/hyprctl-verification-layer.md` §5).

**OBS** Coverage against the held 56 live pairs: 52 of the 70 keys are held pairs; 18 are
not (`group:col.border_inactive`, `group:col.border_locked_active`,
`group:col.border_locked_inactive`, 13 `group:groupbar:*` keys,
`misc:disable_scale_notification`, `misc:disable_splash_rendering`); the 4 held pairs the
table lacks (`decoration:dim_inactive`, `general:snap:enabled`, `input:accel_profile`,
`input:touchpad:disable_while_typing`) have no declarer in the tree — the held class
census counts exactly 4 `live-default` rows.

## §4 Applying the divergence classes mechanically

`--getoption FILE` merges a `hyprctl getoption` dump (key → value, custom_type, set) into the
static rows and labels each with the held vocabulary: `agreement` (one declarer, live equal,
set), `agreement*` (equal but shadowed: more than one declarer), `mismatch` (unequal, or
`set=false` despite a declarer), `config-only` (declared, not in the dump), `live-default`
(in the dump, no declarer). Comparison normalises numbers for int/float types, boolean
spellings, and a scalar against a repeated tuple (`0` vs `0 0 0 0`); anything else is exact
string equality. The round-39 counter checks the labels on two generated merge trees per
measured revision (`quality/counters/c3-r39-options.py`, `PRED-C3-r39-v2`).

## Falsifiable consequence

Delete the `window-no-gaps` toggle file and re-run the tool on the same tree: the owners of
`general:gaps_in`, `general:gaps_out`, `general:border_size` and `decoration:rounding` move to
`default/hypr/looknfeel.conf` lines 9, 10, 12 and 29 with values 5, 10, 2 and 0 (rounding
keeps its value; only its owner moves); a live `getoption` after the same change on the
host would then label those rows `agreement` (single declarer) instead of `agreement*`.
Either half disagreeing falsifies §1-§3.
The static half was run on a scratch copy of the tree (receipt
`.ufo/waves/round-39/c3/consequence-static.txt`: the four rows moved as stated); the live
half is open.

## Limits

- **[UNK]** No live `getoption` dump was taken this round (no socket was connected); §4 is
  verified on generated inputs and the selftest, not against the running compositor.
- The host tree is the copy a seat took on 2026-10-25; a later toggle or theme switch
  changes owners — re-run, do not reuse the counts.
- The parser covers the hyprlang subset the host tree uses (variables, `{{ }}`, `##`,
  trailing comments, `# hyprlang if/endif`, continuation lines, sorted globs); it does not
  load plugins, so a plugin's registered options inside `plugin { }` are excluded with the
  rest of that special category.
- A static table names the last declarer; the live value can still differ (runtime
  `hyprctl keyword`, a reload error) — that is what §4's `mismatch` exists to show.

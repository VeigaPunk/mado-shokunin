# ScoutHostRules — C1 host join (read-only)

Scope: the host side of C1 `rule-attribution-r24`. Read-only census of the host's rule-declaring
files, statement counts, named/tag declarations, `hyprctl version`, and whether `hyprctl clients -j`
carries a `tags` field. No dispatch, no keyword, no reload; no remote bytes fetched by this seat.

Verdict: **host join satisfied**. Host is Hyprland 0.56.2 at the exact pin; the live plane has
82 sourced rule declaration sites (9 host + 73 omarchy defaults), 3 named rules, 21 rule lines with
a `tag` effect and 21 `match:tag` consumers; `hyprctl clients -j` exposes `tags` as a JSON array on
all 4 clients, all non-empty (values not printed by instruction). That field is the rule applicator's
tag keeper, so it is a rule-**effect** readout, not rule identity.

## 1. Version (first line, verbatim)

```
Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean ([gha] Nix: update inputs).
```

`[OBS]` Matches the round-24 pin (tag `v0.56.2` = commit `efb50993780079460b0cbed1363e2166a2de1d9f`).
The same run reports `Tag: v0.56.2, commits: 7661`.

Environment note (not a compositor fact): the persistent tool shell has
`HYPRLAND_INSTANCE_SIGNATURE` unset; `hyprctl` there fails with
`HYPRLAND_INSTANCE_SIGNATURE not set! (is hyprland running?)`. (The very first probe ran in a
temporary shell that still carried the variable, which is why it succeeded.) The only instance
directory is `/run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120`, so
every query below ran with `HYPRLAND_INSTANCE_SIGNATURE` set to that directory name and
`XDG_RUNTIME_DIR=/run/user/1000`. No other env or compositor state was touched.

## 2. File census — `grep -rln 'windowrule\|layerrule'`

Path legend: `H:` = `~/.config/hypr/`, `D:` = `~/.local/share/omarchy/default/hypr/`.
`sites` = line-start declaration sites (inline `windowrule =` / `layerrule =` / block `windowrule {`),
comments excluded. `sourced` = reached through the include graph from `H:hyprland.conf`.

| file | lines | sha256: | sites | sourced |
|---|---|---|---|---|
| H:hyprland.conf | 32 | `sha256:ce7483f35ab52bc28e3020a6fb0ac14b2e02de5817abe827ef8452a0190f8365` | 0 (match is a comment at :26) | yes — entry file |
| H:input.conf | 54 | `sha256:3769c92ab7660f1795cb6d0af1bcc5a5614a299b29ae8358d1b85936bdd47bf4` | 2 windowrule | yes — `H:hyprland.conf:17` |
| H:ai-usage.conf | 5 | `sha256:21e76af98ce791fa829b99d41a51014ec910a9db602e5a9806da233350ad423e` | 4 windowrule | yes — `H:hyprland.conf:29` |
| H:gkeep.conf | 5 | `sha256:3726e488c0bf93028f1bba11017cf02d26da6dc3604362815bc4f3738b8e9949` | 3 windowrule | yes — `H:hyprland.conf:32` |
| H:hyprland.conf.bak.1792267376 | 29 | `sha256:4f52854a3c143dcf58430a679e339619223d2b5008115a322d06b2de637ea462` | 0 (same commented example at :26) | no |
| D:windows.conf | 15 | `sha256:45b1e4654edaec110ce8f38887932bad383da75e7274d3b3618fc2c1e118eca4` | 4 windowrule | yes — `H:hyprland.conf:12` |
| D:apps/1password.conf | 2 | `sha256:0b58134002e3a4818d8f55f72b2e8451edf66fbee8410b0f1d08f5a60479c3a4` | 2 windowrule | yes |
| D:apps/bitwarden.conf | 6 | `sha256:f0066b34702910a8a92ba90334ef1b18402d472dd73e8abe43bf8f86f86f569f` | 4 windowrule | yes |
| D:apps/browser.conf | 19 | `sha256:549437fc293a3f4578c5a6f0a5de49363b71935dd3bb02f3aeabd29475c467d2` | 10 windowrule | yes |
| D:apps/davinci-resolve.conf | 2 | `sha256:b898cb5e6728322092d92cc918c397577d49527adb0773e1ae7185b038aaca9a` | 1 windowrule | **no** — not in `apps.conf` |
| D:apps/geforce.conf | 5 | `sha256:3cc6ee4be2c91118663929d0e89c090477f71bbcb932836ba8daa4d60601eb4a` | 1 windowrule block | yes |
| D:apps/hyprshot.conf | 2 | `sha256:4882dec486c877e4798170c5afc1511b41c6f3943cacb30a9b7f470114696219` | 1 layerrule | yes |
| D:apps/jetbrains.conf | 6 | `sha256:524f3badc31fdc56486bcbf88af18c4b9c2df56441a542dacae92b4e1f0a37ba` | 1 windowrule block | yes |
| D:apps/localsend.conf | 4 | `sha256:01d5214fb324b69afc41badffb812e9ab3e1325f45282a6db7e0dbd166f2d2b1` | 3 windowrule | yes |
| D:apps/moonlight.conf | 6 | `sha256:f3d3034fe1111cc14fbc342d24af6b8666b1d2ba326bd00315a406f38a71055c` | 1 windowrule block | yes |
| D:apps/pip.conf | 10 | `sha256:fe541e496906d1441a7ca076a2e65a94f5c445b5820c9cc806ba1d14a0670944` | 9 windowrule | yes |
| D:apps/qemu.conf | 2 | `sha256:51aa099fa6cdd5868f845345f50001520d6513a5b923391b7c4635938453da3c` | 2 windowrule | yes |
| D:apps/retroarch.conf | 4 | `sha256:1639702d7a664a493a1bf07847a8a3b4bbec45de15415996e15c4bc4a00125e1` | 4 windowrule | yes |
| D:apps/steam.conf | 8 | `sha256:c338c2fa36c692732e9041b663e999df006b91328f7ed53c4bf6b5da03626453` | 7 windowrule | yes |
| D:apps/system.conf | 23 | `sha256:d8729227f071e79a4aad307db3a5c2bec1e9766c3ba2f25052c964ddda278041` | 13 windowrule | yes |
| D:apps/telegram.conf | 2 | `sha256:7da8f4e1765db92db9613607242532dd8c60d6c0a34015b42c5a0d8844abc308` | 1 windowrule | yes |
| D:apps/terminals.conf | 4 | `sha256:7918aad8936c41ccd73b9c25818ea54aabf141f970322f179c138dff42b80b3e` | 3 windowrule | yes |
| D:apps/typora.conf | 2 | `sha256:90a7698fa9b34ef10ad8b3231311d5ef29f04d28cd0978eedb3fc45e2dbb8af2` | 1 windowrule | yes |
| D:apps/walker.conf | 2 | `sha256:8ebc83e3e1c3c8296648f3334cc3d981dc95a27070e6aa9f449e7e45c510d0e9` | 1 layerrule | yes |
| D:apps/webcam-overlay.conf | 6 | `sha256:6d709dcb21757b5f98d4e3fbd7635da2b564dd4e48a91892358608b9228d0324` | 5 windowrule | yes |

Other files hashed for the record (sourced or swept; none declares a rule):
`~/.config/omarchy/current/theme/hyprland.conf` `sha256:79126bec8c28da306712148734a3ee58335a8bd48bf863e4e2e2db6d6d8344b6` (9 lines);
`~/.local/state/omarchy/toggles/hypr/flags.conf` `sha256:4daee1c7f3cbbac4a2031f48c84265fdf9c36f688a6663bfeaa52405f61a437c` (2 lines);
`~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf` `sha256:746f8200ade1578cf3d96a77a5c4c480d844252b681c3ca243eed4d734665327` (10 lines);
`D:apps.conf` `sha256:1a5482bb81b325ef811d31d07707a706b583a8dba802a477cb79ffbd6859d72e` (19 lines);
`D:bindings.conf` `sha256:47a565055f7c4dbcb1d8de3fe594371facf83e11ec4428173c1ad67b9b9c881f` (16 lines).
`D:looknfeel.conf`, `D:input.conf`, `D:envs.conf`, `D:autostart.conf`, `D:bindings/*`,
`D:plain-bindings.conf`, `D:toggles/*.conf` were also swept and contain no rule declaration, as do
the host's remaining `~/.config/hypr/*.conf` files (monitors, looknfeel, bindings, autostart, and the
hypridle/hyprlock/hyprsunset/xdph files).

`[OBS]` 25 files match the grep on disk; 24 are real declarations (the 25th is a `.bak` whose only
match is a commented example line). Of the 24, 23 are sourced; `D:apps/davinci-resolve.conf` is on
disk but absent from `D:apps.conf:2-19`, so its single rule is not in the live plane.

## 3. Statement counts

| plane | inline windowrule | block windowrule | layerrule | sites |
|---|---|---|---|---|
| host `~/.config/hypr` (sourced) | 9 | 0 | 0 | 9 |
| omarchy defaults, all on disk | 69 | 3 | 2 | 74 |
| omarchy defaults, sourced | 68 | 3 | 2 | 73 |
| **sourced total (live plane)** | **77** | **3** | **2** | **82** |

Per-file host breakdown: `ai-usage.conf` 4, `gkeep.conf` 3, `input.conf` 2.
Unsourced on disk: `davinci-resolve.conf` 1 inline windowrule; `hyprland.conf.bak.1792267376` 0
(commented example only).

Reconciliation with `corpus/knowledge/keybind-rule-semantics.md:183-201` `[OBS]` (that note records
"79 sourced rule statements = 4 (windows.conf) + 69 (sourced app files) + 2 (local input.conf) +
4 (ai-usage.conf); 3 of them named"):

- That arithmetic reproduces exactly against today's bytes: `windows.conf` 4, sourced app files 69
  (70 sites in `apps/` including the 3 block forms and 2 layerrules, minus the unsourced davinci 1),
  local `input.conf` 2, `ai-usage.conf` 4.
- The current live plane is 82, not 79, because `H:gkeep.conf` (3 windowrule sites, sourced at
  `H:hyprland.conf:32`) did not exist when that note was written. That note mtime is
  `2026-10-14 10:56:45`; `H:gkeep.conf` mtime is `2026-10-17 17:05:14`, and the file contains no
  `gkeep` mention. So this is a config delta, not an arithmetic error, and the older note is not
  contradicted.
- Four sha256 prefixes quoted in that note match today's files byte-for-byte
  (`input.conf` `3769c92a…`, `ai-usage.conf` `21e76af9…`, `windows.conf` `45b1e465…`,
  `apps.conf` `1a5482bb…`), so the rest of that inventory is still current apart from `gkeep`.

## 4. Named rules and tag effects (the two asked-about declaration kinds)

Named rules — 3, all block form, all in sourced files:

| file:line | name | note |
|---|---|---|
| `D:apps/geforce.conf:2` | `geforce` | `match:class = GeForceNOW`, `idle_inhibit = fullscreen` |
| `D:apps/jetbrains.conf:3` | `jetbrains-focus` | `no_follow_mouse = on`, `match:class = ^(jetbrains-.*)$` |
| `D:apps/moonlight.conf:2` | `moonlight` | `match:class = com.moonlight_stream.Moonlight`, `fullscreen = 1`, `idle_inhibit = fullscreen` |

No `name =` line exists in the host's own `~/.config/hypr` tree, and no non-block rule carries a name.

Tag effects — yes, 21 rule lines carry a `tag` effect (8 distinct tag strings; the host's own
`ai-usage.conf:2` is one of them), and 21 separate rule lines consume `match:tag`:

```
      9 tag -default-opacity
      6 tag +floating-window
      1 tag +terminal
      1 tag +pip
      1 tag +firefox-based-browser
      1 tag +default-opacity
      1 tag -chromium-based-browser
      1 tag +chromium-based-browser
rule lines with match:tag  : 21
rule lines with tag effect : 21
```

Two layerrule sites, both sourced, both `no_anim`:
`D:apps/hyprshot.conf:2` `match:namespace selection`; `D:apps/walker.conf:2` `match:namespace walker`.

Ordering fact relevant to attribution `[OBS]`: the host sets `tag +floating-window` in
`H:ai-usage.conf:2`, sourced at `H:hyprland.conf:29` — i.e. **after** `windows.conf` →
`apps.conf` → `apps/system.conf:2-4`, which declare the `match:tag floating-window` effects
(`float on`, `center on`, `size 875 600`). The consumer rules are registered before the tag that
they match is set. `[INF]` see §6.

## 5. `hyprctl clients -j` and the `tags` field

`[OBS]` 4 client objects; `"tags"` is present in all 4 (`with_tags_key=4`), typed `array`, and all 4
arrays are non-empty (`nonempty_tags=4`). Per instruction only the key list of the first object was
printed; no titles, tag strings or other values were read into this report.

Key list of the first object (32 keys, `jq '.[0]|keys'`):

```
acceptsInput address allowedOverFullscreen at class contentType floating focusHistoryID
fullscreen fullscreenClient fullscreenHandler grouped hidden inhibitingIdle initialClass
initialTitle mapped monitor pid pinFullscreened pinned size stableId swallowing tags
tearingHint title visible workspace xdgDescription xdgTag xwayland
```

`[OBS]` The same object also carries `xdgTag` (a distinct key). The C1 note must not conflate the
two: `tags` is the window-rule tag keeper, `xdgTag` is a separate XDG toplevel tag (source pointer
in §6).

`[OBS]` No key in this list names a rule, rule id, rule list, matched condition or rule ordering.

## 6. Source pointers for the C1 source seats (not claims from this seat)

These come from the local read-only mirror `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2`,
whose `git rev-parse HEAD` is `efb50993780079460b0cbed1363e2166a2de1d9f` (the pin). This seat has no
`lsp` device in its toolset, so every anchor below is a literal `grep`/`sed` on that mirror, not a
semantic-server result; a source seat with `lsp` should confirm the definitions if the contract
needs them. This seat did **not** fetch pinned raw bytes, so it mints no sha256 receipt, no SOURCES
row and no claim rows; a source seat must fetch and hash before any of this can carry a C1 row.

- `src/debug/HyprCtl.cpp:346-354` — `getTagsData()` returns
  `w->m_ruleApplicator->m_tagKeeper.getTags()` (JSON: comma-joined quoted strings). So the `clients`
  `tags` array is a **rule-applied effect readout**, not a match record.
- `src/debug/HyprCtl.cpp:415` — clients JSON template `"tags": [{}]`; `:419` `"xdgTag": "{}"`;
  `:433` feeds `getTagsData(w, format)` into that slot. Text format prints `\ttags: {}` (`:442`).
- `src/desktop/rule/windowRule/WindowRuleEffectContainer.cpp:39` — `"tag"` is a window-rule effect.
- `src/desktop/rule/windowRule/WindowRuleApplicator.cpp:161-164` — `WINDOW_RULE_EFFECT_TAG` does
  `m_dynamicTags.emplace_back(...)`, `m_tagKeeper.applyTag(effect, true)`, `tagsChanged = true`.
- `src/desktop/rule/Rule.hpp:63,66,78` — `IRule` has `name()` and `const std::string& m_name`, i.e.
  rule names exist in the rule base; the host declares 3.
- Re-application (explains §4 ordering) `[INF]`: `WindowRuleApplicator.cpp:511-513` sets
  `propsToRecheck |= RULE_PROP_TAG` when any rule changed tags; `recheckStaticRules()` (`:526-545`)
  reapplies rules whose `getPropertiesMask() & propsToRecheck`; `src/desktop/view/Window.cpp:2277-2283`
  = `const bool recheck = m_ruleApplicator->readStaticRules(); ... if (recheck) { ... recheckStaticRules(); }`.
  So a tag set by a later-sourced file can still drive earlier-registered `match:tag` effects on the
  recheck pass. This is a code-path inference, not an instrumented observation of the host's
  `ai-usage` window.
- Bounded negative `[OBS]` on the local mirror: the read-command registration list
  (`grep -oE 'registerCommand\(SHyprCtlCommand\{"[a-zA-Z]+", true' src/debug/HyprCtl.cpp`) yields 21
  commands — `workspaces workspacerules activeworkspace clients kill activewindow layers version
  devices splash cursorpos binds globalshortcuts systeminfo animations rollinglog configerrors
  locked descriptions submap status` — none of which lists window rules or layer rules.
  `workspacerules` is workspace rules only (`HyprCtl.cpp:613-631`, `:2005`). This is bounded to this
  commit and must be re-run on fetched bytes by the source seat.

Raw URLs for the source seats:
`https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp`
and `.../src/desktop/rule/windowRule/WindowRuleApplicator.cpp` (same pinned prefix).

## 7. What these bytes do NOT establish

- They do not identify which rule produced any applied effect on any live window. The `tags` field is
  the union of tag effects kept by the applicator; it carries no rule name, id or match record, and
  the clients key list has no such field. Rule-to-effect attribution on this host remains `[UNK]`.
- They do not establish that the compositor loaded any specific file. The census is a disk/include
  graph, not a loaded-config trace; `hyprland.conf` itself was not read back from the compositor.
  Loaded-config identity stays `[UNK]` (consistent with `hyprland-config-era-r12.md:79-86`).
- They do not show tag *values*. Per instruction only presence/type/count were read, so nothing here
  confirms or refutes the r2 `default-opacity*` divergence (`keybind-rule-semantics.md:252-270`), and
  the current 4-client tag state is not a census of intended vs actual tags.
- They do not establish layer-rule effect reads or layer-rule attribution; only two declared
  `layerrule` sites and the `layers` read verb's existence.
- They do not establish anything about other Hyprland versions, other hosts or a future config.
- No claim row from this report can pass C1 `PASS_ROW`: the predicate needs a verbatim quote from
  bytes fetched at a pinned `hyprwm` URL, and this seat's evidence is local host state. Use this
  report as the note's host-context section, not as a claim row.

## 8. Commands run (all read-only)

```sh
# version (with HYPRLAND_INSTANCE_SIGNATURE=<instance dir> and XDG_RUNTIME_DIR=/run/user/1000)
timeout 15 hyprctl version | sed -n '1p'

# file census: sha256 + lines for every matching file
for f in $(grep -rln 'windowrule\|layerrule' ~/.config/hypr | sort) \
         $(grep -rln 'windowrule\|layerrule' ~/.local/share/omarchy/default/hypr | sort); do
  printf '%s  %s  %s\n' "$(sha256sum "$f" | cut -c1-64)" "$(wc -l < "$f")" "$f"
done

# statement counts (line-start, comments excluded)
grep -rhE '^[[:space:]]*windowrule[[:space:]]*=' ~/.config/hypr --include='*.conf' | wc -l      # 9
grep -rhE '^[[:space:]]*windowrule[[:space:]]*\{' ~/.config/hypr --include='*.conf' | wc -l      # 0
grep -rhE '^[[:space:]]*layerrule' ~/.config/hypr --include='*.conf' | wc -l                    # 0
grep -rhE '^[[:space:]]*windowrule[[:space:]]*=' ~/.local/share/omarchy/default/hypr --include='*.conf' | wc -l   # 69
grep -rhE '^[[:space:]]*windowrule[[:space:]]*\{' ~/.local/share/omarchy/default/hypr --include='*.conf' | wc -l   # 3
grep -rhE '^[[:space:]]*layerrule' ~/.local/share/omarchy/default/hypr --include='*.conf' | wc -l                  # 2

# names and tag effects
grep -rnE '^[[:space:]]*name[[:space:]]*=' ~/.config/hypr ~/.local/share/omarchy/default/hypr --include='*.conf'   # 3
grep -rhE '^[[:space:]]*windowrule' ~/.config/hypr ~/.local/share/omarchy/default/hypr --include='*.conf' \
  | grep -oE 'tag[[:space:]]+[+-][A-Za-z0-9._-]+' | sort | uniq -c

# clients keys only, then presence counts (no values)
timeout 15 hyprctl clients -j | jq -r '.[0]|keys[]'
timeout 15 hyprctl clients -j \
  | jq -r '"clients=\(length) with_tags_key=\([.[]|has("tags")]|map(select(.))|length) tags_type=\([.[]|.tags|type]|unique|join(",")) nonempty_tags=\([.[]|(.tags|length>0)]|map(select(.))|length)"'
# -> clients=4 with_tags_key=4 tags_type=array nonempty_tags=4

# source pointer sweep on the pinned local mirror (read-only)
cd /fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2
git rev-parse HEAD    # efb50993780079460b0cbed1363e2166a2de1d9f
grep -oE 'registerCommand\(SHyprCtlCommand\{"[a-zA-Z]+", true' src/debug/HyprCtl.cpp | wc -l   # 21
```

Bounds observed: only the read verbs `hyprctl version` and `hyprctl clients -j` were used; no
`dispatch`, `keyword`, `reload`, `kill` or `setprop`; no file under `~/.config`,
`~/.local/share/omarchy` or `~/.local/state` was written; no package install or update was
performed; the only file created by this seat is this report. No lane git/jj command was run.

Report: .ufo/waves/round-24/w1/reports/ScoutHostRules.md

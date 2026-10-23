# AtkHostJoin — attack on the host-join numbers of `w1/reports/ScoutHostRules.md`

Seat: leaf falsifier, read-only host probe. No dispatch/keyword/reload, no writes outside this
report, no `~/.config` or omarchy state touched, no packages, no lane git/jj.

Attacked item: the host-join census in `.ufo/waves/round-24/w1/reports/ScoutHostRules.md`
(the note C1 cites at `corpus/knowledge/rule-attribution-r24.md:80-83`):
`82` sourced rule sites; `77 / 3 / 2` inline / block / layerrule; `3` named block rules;
`21` tag-effect lines; `tags` on `4/4` clients.

Method: re-derived everything myself from the live include graph and the live compositor, without
reusing the note's commands or cached results. Include graph walked from
`~/.config/hypr/hyprland.conf` by resolving every `source =` line (with `~` and glob expansion);
declaration sites counted as line-start `windowrule =`, `windowrule {`, `layerrule`; comments
excluded. Clients inspected with `jq` for key names, key presence, type, array length and length
histogram only — no titles, no tag strings.

## 1. `hyprctl version`, first line

```
Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean ([gha] Nix: update inputs).
```

`[OBS]` Byte-identical to the note's line 1. Commit is the round pin `efb50993…`; same run reports
`Tag: v0.56.2, commits: 7661`. **Matches.**

## 2. Declaration sites in the sourced plane

`[OBS]` 40 files are reachable from `~/.config/hypr/hyprland.conf`. Counts (line-start, comments
excluded):

| plane | inline `windowrule =` | block `windowrule {` | `layerrule` | sites |
|---|---|---|---|---|
| host `~/.config/hypr` sourced | 9 | 0 | 0 | 9 |
| omarchy defaults, sourced | 68 | 3 | 2 | 73 |
| **sourced total** | **77** | **3** | **2** | **82** |
| omarchy defaults, all on disk | 69 | 3 | 2 | 74 |
| + unsourced `davinci-resolve.conf` | +1 | 0 | 0 | +1 |

Host breakdown reproduced exactly: `ai-usage.conf` 4, `gkeep.conf` 3, `input.conf` 2. Token scan across the
trees' `*.conf` files with comment lines excluded found 81 `windowrule` tokens and 81 declaration
sites (80 sourced + 1 unsourced davinci) and 2 `layerrule` tokens / 2 sites — i.e. no declaration form escaped the
line-start regex (no `windowrulev2`, no one-line block, no commented line counted).

Unsourced check: `apps.conf:2-19` lists 18 app files and does **not** list `davinci-resolve.conf`,
which does hold one live-looking rule (`windowrule = stay_focused on, match:class .*[Rr]esolve.*,
match:float 1`). Include anchors in `hyprland.conf` also reproduce: `windows.conf`:12, host
`input.conf`:17, `ai-usage.conf`:29, `gkeep.conf`:32. **82 and 77/3/2 match.**

## 3. Named block rules

`[OBS]` 3 `name =` lines, all indented inside `windowrule { }` blocks, all in sourced omarchy
defaults; none in the host tree, none on an inline rule:

| file:line | name |
|---|---|
| `apps/geforce.conf:2` | `geforce` (block `:1`, rules `:3-4`) |
| `apps/jetbrains.conf:3` | `jetbrains-focus` (block `:2`, rules `:4-5`) |
| `apps/moonlight.conf:2` | `moonlight` (block `:1`, rules `:3-5`) |

**3 named match.**

## 4. Tag-effect lines

`[OBS]` 21 rule lines carry a `tag ±` effect, 21 occurrences (no line carries two), 8 distinct:

```
      9 tag -default-opacity
      6 tag +floating-window
      1 tag +default-opacity
      1 tag +chromium-based-browser
      1 tag +firefox-based-browser
      1 tag -chromium-based-browser
      1 tag +pip
      1 tag +terminal
rule lines with tag effect : 21
rule lines with match:tag  : 21
```

`[OBS]` No `tag ±` effect exists outside a `windowrule`/`layerrule` line (0 hits for a line-start
`tag` directive, 0 hits inside block bodies), so 21 is not an undercount of block-form effects.
Host's own `ai-usage.conf:2` (`tag +floating-window, match:class ^(org.omarchy.ai-usage)$`) is one
of the 21, as the note says. **21 matches.**

Precision defect in the prose around this number `[OBS]`: the note calls the 21 `match:tag` lines
"21 **separate** rule lines". They are not disjoint from the 21 effect lines — 4 lines do both:
`apps/browser.conf:4`, `apps/browser.conf:5`, `apps/pip.conf:3`, `apps/terminals.conf:3` (e.g.
`windowrule = tag -default-opacity, match:tag chromium-based-browser`). Split: 17 effect-only,
17 match-only, 4 both → 38 distinct lines involved, not 42. The two counts 21/21 are individually
correct; only the implied disjointness is wrong. The C1 note does not restate this count, so it is
not load-bearing for C1.

## 5. `hyprctl clients -j` and `tags`

`[OBS]` Key names and counts only, no values:

```
clients=4 with_tags_key=4 tags_type=array nonempty_tags=4
tag_len_hist=1:1,2:3
```

Key list of the first object (32 keys, verbatim):

```
acceptsInput address allowedOverFullscreen at class contentType floating focusHistoryID
fullscreen fullscreenClient fullscreenHandler grouped hidden inhibitingIdle initialClass
initialTitle mapped monitor pid pinFullscreened pinned size stableId swallowing tags
tearingHint title visible workspace xdgDescription xdgTag xwayland
```

`[OBS]` `tags` is present on 4/4 objects, typed `array`, non-empty on all 4 (6 tag entries total
across clients, per the histogram). `xdgTag` is a distinct key, exactly as the note warns. The key
list contains no rule name, id, rule list, match record or ordering field. **4/4 matches.**

## 6. Drift check

`[OBS]` sha256 of six files checked against the note's table — all six byte-identical to the note:
`hyprland.conf ce7483f3…`, `input.conf 3769c92a…`, `ai-usage.conf 21e76af9…`,
`gkeep.conf 3726e488…`, `windows.conf 45b1e465…`, `davinci-resolve.conf b898cb5e…`. So the note's
numbers were computed from the same config generation that is live now; this is not a drift case.

## 7. Findings against the note (non-headline)

1. **"24 are real declarations" is off by one** `[OBS]`. 25 files match `windowrule|layerrule` on
   disk, but only **23** contain at least one declaration site. Two comment-only matches:
   `~/.config/hypr/hyprland.conf` (32 lines, the single match is the commented example at `:26`) and
   `hyprland.conf.bak.1792267376` (29 lines, same comment). The note's own table gives
   `hyprland.conf` 0 sites, so the sentence contradicts the table. The site total 82 is unaffected.
2. **"21 separate" `match:tag` lines** — see §4: 4 lines overlap the tag-effect set. Counts right,
   disjointness claim wrong.
3. **Environment caveat not reproducible** `[OBS]`. The note says the persistent tool shell has
   `HYPRLAND_INSTANCE_SIGNATURE` unset and that `hyprctl` therefore fails without a manual env
   workaround. In this session `HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120`
   and `XDG_RUNTIME_DIR=/run/user/1000` are set, and `hyprctl version` / `hyprctl clients -j` ran
   with no workaround. Only one instance dir exists, matching the note's. This is a shell-property
   claim, not a compositor fact, and it does not affect any number; it does mean the note's
   "the persistent shell lacks the var" should not be reused as a general statement.
4. **Sourced-file inventory is not exhaustive** `[OBS]`: `~/.config/omarchy/current/theme/gum.env.conf`
   is reached via `omarchy/default/hypr/envs.conf:3` and is absent from the note's file table (the
   note only hashes `theme/hyprland.conf`). It contains 0 rule sites, so no count changes.

## Comparison

| note claims | re-derived | verdict |
|---|---|---|
| `hyprctl version` line 1 = commit efb50993… | identical | match |
| 82 sourced sites | 82 | match |
| 77 inline / 3 block / 2 layerrule | 77 / 3 / 2 | match |
| 3 named block rules (geforce, jetbrains-focus, moonlight) | 3, same names, all block, all omarchy | match |
| 21 rule lines with a tag effect | 21 (21 occurrences, 8 distinct, same distribution) | match |
| `tags` on 4/4 clients | clients=4, with tags key=4, type array, non-empty 4/4 | match |
| "24 real declaration files" | 23 | **off by one** |
| "21 separate `match:tag` lines" | 21 lines, but 4 shared with the effect set (38 distinct) | **imprecise** |
| shell has `HYPRLAND_INSTANCE_SIGNATURE` unset | set in this session | **not reproduced** |

## Limits

- Disk/include-graph census, not a loaded-config trace: it still does not prove the compositor
  loaded these files (unchanged from the note's §7).
- `tags` presence is a rule-effect readout, not rule identity; this seat did not attempt attribution.
- No tag values, titles, or other client payload were read into this report.
- Read verbs used: `hyprctl version`, `hyprctl clients -j` only.

VERDICT: holds — every headline number the note joins to the host (82; 77/3/2; 3 named; 21 tag
lines; `tags` on 4/4) reproduced exactly from independent re-derivation, and six sha256s confirm
zero config drift; the surviving defects are prose precision (23 vs "24 real declarations",
"separate" for two overlapping 21-line sets) and an unreproducible shell-environment caveat, none
of which moves the site totals or the 4/4 tag presence.

Report: .ufo/waves/round-24/w2/reports/AtkHostJoin.md

# Per-window window-rule effect reads with hyprctl getprop (MADO-R12-1)

source: [ref] — https://wiki.hypr.land/Configuring/Advanced-and-Cool/Using-hyprctl/#getprop — `#getprop`; [ref] — https://wiki.hypr.land/Configuring/Basics/Window-Rules/#syntax — `#syntax`, `#effects`, `#notes`; [ref] — https://github.com/hyprwm/Hyprland/blob/v0.56.2/src/debug/HyprCtl.cpp — lines 1463-1645 at commit efb50993780079460b0cbed1363e2166a2de1d9f; [ref] — .ufo/evidence/round-12/getprop-help.txt and .ufo/evidence/round-12/getprop-measure.txt; [ref] — /home/vgpnk/.local/share/omarchy/default/hypr/windows.conf:5-15 and /home/vgpnk/.local/share/omarchy/default/hypr/apps/terminals.conf:2-4; [ref] — corpus/knowledge/arc-synthesis.md — §6 gap ledger :300 (the superseded negative claim)
verified-at: 2026-10-19
recheck: 2027-01-17
covers: U1

## Finding

[OBS] Pinned host: `hyprctl version` reports Hyprland 0.56.2, tag `v0.56.2`, commit `efb50993780079460b0cbed1363e2166a2de1d9f` (`.ufo/evidence/round-12/getprop-help.txt:5-18`).

[OBS] `hyprctl --help` on that host lists `getprop ... → Gets a window property` and `workspacerules → Lists all workspace rules`; `hyprctl getprop --help` gives `hyprctl [flags] getprop <regex> <property>` and describes the first argument as the regular expression by which a window is searched (`getprop-help.txt:20-92,97-107`).

[OBS] For a title-free selected Alacritty client, `hyprctl getprop` returned the window rule-applicator opacity values: `opacity` = `0.97`, `opacity_inactive` = `0.9`, `opacity_fullscreen` = `1`, and `opacity_override` = `false` (`getprop-measure.txt:8-64,68-81`).

[OBS] The same window's global config inputs measured by `hyprctl getoption decoration:active_opacity` and `hyprctl getoption decoration:inactive_opacity` are each `float: 1.000000`, `set: false` (`getprop-measure.txt:83-91`). This is a comparison with global configured opacity values, not a claim that `getprop` returns rendered pixels.

[INF] Classification: **effect-read, not match-read**. The returned per-window property agrees with declared opacity effect values, but the command does not report which rule supplied the value or whether additional matching rules contributed. The matching-rule identity remains `[UNK]`.

## Claim table

| tag | bounded claim | evidence anchor |
|---|---|---|
| [OBS] | At this host/version, the CLI lists `getprop` as a window-property read and lists `workspacerules` separately. | `hyprctl --help`; `.ufo/evidence/round-12/getprop-help.txt:20-79` |
| [OBS] | The host usage helper requires a window selector and property; an omitted selector/property produces `not enough args`. | `hyprctl getprop --help`; `hyprctl getprop`; `.ufo/evidence/round-12/getprop-help.txt:94-107` |
| [OBS] | A bare `Alacritty` selector returned `window not found`; `class:Alacritty` returned `0.97`; the selected address returned `0.97`. | `.ufo/evidence/round-12/getprop-measure.txt:68-72,101-113` |
| [OBS] | The selected Alacritty address reports active `0.97`, inactive `0.9`, fullscreen `1`, and override `false`. | `.ufo/evidence/round-12/getprop-measure.txt:23-26,71-81` |
| [OBS] | The global opacity options report `1.000000` and `set: false`. | `.ufo/evidence/round-12/getprop-measure.txt:83-91` |
| [OBS] | Host config declares `opacity 0.97 0.9` for `match:tag terminal`; that tag is assigned to classes matching `(Alacritty|kitty|com.mitchellh.ghostty|foot)`. | `/home/vgpnk/.local/share/omarchy/default/hypr/apps/terminals.conf:2-4` |
| [OBS] | Host config also declares `opacity 0.97 0.9` for `match:tag default-opacity`, after sourcing app rules. | `/home/vgpnk/.local/share/omarchy/default/hypr/windows.conf:5-15` |
| [OBS] | `workspacerules -j` returned `[]` during this capture. | `hyprctl workspacerules -j`; `.ufo/evidence/round-12/getprop-measure.txt:93-96` |
| [OBS] | A valid address plus unknown property returns `prop not found`; a nonexistent class selector returns `window not found`. | `.ufo/evidence/round-12/getprop-measure.txt:104-110` |
| [OBS] | The 0.56.2 handler resolves a window with `query().selector(WINREGEX).runWindow()` and reads opacity through `m_ruleApplicator` alpha getters. | `HyprCtl.cpp#L1463-L1475`, `#L1492-L1504`, `#L1565-L1575` at v0.56.2 |
| [INF] | Matching the host rule declarations and returned values shows that `getprop` reads an effect value available on the selected window. The repeated `0.97 0.9` declaration prevents attributing this value uniquely to the terminal rule. | Host rule files above; host command output; handler code above |
| [INF-docs] | Current wiki explains window-rule `match` fields versus effects, requires all props to match, describes top-to-bottom effects and opacity multiplication. | Current `Window Rules` page `#syntax`, `#effects`, `#notes`; [ref] |
| [INF-docs] | The current wiki pages are **Latest git**, modified 2026-08-26; the current Window Rules page says hyprlang is deprecated since 0.55 and directs hyprlang users to 0.54 pages. These are current-doc statements, not host facts about the 0.56.2 parser. | Current page header and note; [ref], [ref] |
| [UNK] | Which rule matched the selected client, whether any other rule also supplied the same opacity, and the final rendered opacity are not established by these reads. | Source handler sweep `HyprCtl.cpp#L1463-L1645`; host output and rule declarations above |

## Host capture and comparison

The only window inventory used here was title-free. The command projected exactly `class`, `address`, `workspace.name`, and `floating`; it did not request or print `title` (`.ufo/evidence/round-12/getprop-measure.txt:6-64`). The selected row was class `Alacritty`, address `0x55b5ee84e440`, workspace `1`, `floating: false`.

The repeatable property commands and literal outputs were:

```text
$ hyprctl getprop address:0x55b5ee84e440 opacity
0.97
$ hyprctl getprop address:0x55b5ee84e440 opacity_inactive
0.9
$ hyprctl getprop address:0x55b5ee84e440 opacity_fullscreen
1
$ hyprctl getprop address:0x55b5ee84e440 opacity_override
false
$ hyprctl getoption decoration:active_opacity
float: 1.000000
set: false
$ hyprctl getoption decoration:inactive_opacity
float: 1.000000
set: false
$ hyprctl workspacerules -j
[]
```

These exact commands and outputs are also retained in `.ufo/evidence/round-12/getprop-measure.txt:68-96`. The query makes no compositor or configuration change.

The read values can be compared without claiming match attribution:

| Plane | Observed or declared value | Bounded interpretation |
|---|---|---|
| Declared terminal effect | `opacity 0.97 0.9, match:tag terminal` (`apps/terminals.conf:4`) | A declared candidate effect; class regex includes `Alacritty` (`:2`) |
| Declared generic effect | `opacity 0.97 0.9, match:tag default-opacity` (`windows.conf:15`) | Same pair is also declared on another tag, so value alone is ambiguous |
| Per-window getter | `opacity` `0.97`; `opacity_inactive` `0.9` (`getprop-measure.txt:71-75`) | Effect-read from the window's rule applicator, per tagged handler |
| Global options | active and inactive `1.000000`, `set: false` (`getprop-measure.txt:85-91`) | Current global option values; not the same field as per-rule match identity |
| Fullscreen / override | `1` / `false` (`getprop-measure.txt:77-81`) | Additional getter fields; do not identify a rule |

The wiki's current Lua-era opacity explanation says opacity is a product of configured opacity values; it is not used here to calculate the host's final pixel alpha. The tagged source shows this handler returns the `alpha` member from `PWINDOW->m_ruleApplicator` for `opacity` and corresponding getters for inactive/fullscreen/override. The scoped conclusion is therefore that a **window-effect value is readable**, not that a rule match or compositor-rendered result is proven.

## Host usage and errors

The host's `getprop --help` usage/error outputs were:

```text
$ hyprctl getprop
not enough args

$ hyprctl getprop --help
usage: hyprctl [flags] getprop <regex> <property>

regex:
    Regular expression by which a window will be searched

property:
    See the wiki for a list of properties

flags:
    See 'hyprctl --help'
```

A bare class string did not select the measured client; the explicit selector did:

```text
$ hyprctl getprop Alacritty opacity
window not found

$ hyprctl getprop class:Alacritty opacity
0.97
```

Error behavior was bounded to read-only requests against the measured address or a deliberately nonexistent class:

```text
$ hyprctl getprop address:0x55b5ee84e440 __unknown_property__
prop not found

$ hyprctl getprop class:NoSuchClass opacity
window not found
```

All invocations and outputs are preserved at `.ufo/evidence/round-12/getprop-measure.txt:97-113`; the host version and complete help output are at `.ufo/evidence/round-12/getprop-help.txt:5-107`.

## What the 0.56.2 handler actually reads

At the pinned source tag, `dispatchGetProp` rejects incomplete requests with `not enough args`, stores the window selector and property, queries the selected window, and returns `window not found` if the selector is unresolved (`src/debug/HyprCtl.cpp#L1463-L1475`).

The opacity helper returns `alpha.valueOrDefault().alpha` for ordinary output and the `overridden` member when the override property is requested (`#L1492-L1504`). The handler's `opacity`, `opacity_inactive`, and `opacity_fullscreen` branches obtain values from the window's rule applicator; `opacity_override` is another value getter (`#L1565-L1575`). Unsupported property names reach `return "prop not found"` (`#L1644`).

This inspected response path returns a selected property value or an error string. It does not include a rule name, matched condition, ordered match list, or rule-source attribution. This is a bounded source-path observation at v0.56.2, not a statement about every Hyprland version or other possible instrumentation.

## Corrects

- `corpus/knowledge/arc-synthesis.md:300` previously states: **“window-rule effects / exec-once results | no rule-read verb in Hyprland 0.56 (r2/R3-2)”**. New bounded wording: Hyprland 0.56.2 has `hyprctl getprop <regex> <property>` for per-window effect-property reads. It is effect-read only; it does not reveal which rule matched. This entry leaves `exec-once` results untouched.
- `corpus/knowledge/config-health-report-r3.md:449` previously states: **“Whether any window rule currently matches an open window (no rule-read verb; U4, carried).”** New bounded wording: the reason “no rule-read verb” is incorrect; `getprop` can read a window's effect value. Whether a particular rule matched remains unknown from this command because the handler returns no match attribution and the host opacity declarations share the same values. The prior notes remain unchanged.

## Limits

- This evidence is bounded to the recorded host snapshot, selected address, and property values shown above; it is not a census of all properties or open windows.
- The clients projection deliberately omitted tags and titles. It therefore does not establish the selected client's current tag state or expose any title-based matching condition.
- Equal `0.97` and `0.9` values occur in the terminal-tag and default-opacity declarations. `getprop` does not disambiguate those declarations or enumerate all matching rules.
- `getprop` reads a property through the rule applicator; the inspected getter does not attest to final rendered pixel alpha. No rendering observation was performed.
- `workspacerules -j` is a separate workspace-rule query; its empty result is not evidence about window-rule matches.
- The current wiki uses the latest-git Lua-era documentation and itself marks hyprlang deprecated since 0.55. Its rule syntax/semantics are labeled `[INF-docs]`; host behavior claims here rely on v0.56.2 source and read-only host output instead.
- No absent-property claim is made beyond the source handler's `prop not found` branch. The host error probes and source handler span are retained as the sweep for this command path.

## Rejected

- **Rejected claim:** “`getprop` proves which window rule matched.” The tagged implementation reads a property from `m_ruleApplicator` and returns its value, without a rule identity or match trace (`src/debug/HyprCtl.cpp#L1463-L1645`). The observed `0.97`/`0.9` pair is declared for the terminal-tag and default-opacity paths (host rule-file anchors above). **Flip condition:** a version-pinned read surface that returns a rule name or matched-condition record for this same window.
- **Rejected claim:** “An `Alacritty` `0.97` read proves the terminal-specific rule, rather than any other matching opacity rule, was the source.” The value agrees with the host declarations and the command's response is unattributed. **Flip condition:** evidence from a read-only, version-pinned match-attribution interface, or a controlled isolated rule state; no such mutation was attempted.

## Reproducibility

- Help/version capture: `.ufo/evidence/round-12/getprop-help.txt`.
- Title-free client selection, property reads, configured defaults, workspace rules, and error outputs: `.ufo/evidence/round-12/getprop-measure.txt`.
- Host configuration anchors: `/home/vgpnk/.local/share/omarchy/default/hypr/apps/terminals.conf:2-4` and `/home/vgpnk/.local/share/omarchy/default/hypr/windows.conf:5-15`.
- Pinned implementation: `https://github.com/hyprwm/Hyprland/blob/v0.56.2/src/debug/HyprCtl.cpp#L1463-L1645`.

# Hyprland config-language era and window-rule syntax (MADO-R12-2)

source: [ref] — https://hypr.land/news/update53/ — “Breaking changes”; [ref] — https://wiki.hypr.land/0.54.0/Configuring/Start/ — “Start”; [ref] — https://wiki.hypr.land/0.54.0/Configuring/Window-Rules/ — “Syntax”; [ref] — https://hypr.land/news/26_lua/ — “Lua configs”, “Old hyprlang syntax”; [ref] — https://hypr.land/news/update55/ — “Lua configs”, “Breaking changes”; [ref] — https://github.com/hyprwm/Hyprland/releases/tag/v0.55.0 — “New features”; [ref] — https://hypr.land/news/update56 — “Other”; [ref] — https://github.com/hyprwm/Hyprland/releases/tag/v0.56.2 — “Fixes backported”; [ref] — https://wiki.hypr.land/Configuring/Start/ — note and config location; [ref] — https://wiki.hypr.land/Configuring/Basics/Window-Rules/ — “Syntax”
verified-at: 2026-10-19
recheck: on-release
covers: U2

## Finding

- This note answers the upstream syntax-era question; it does not convert wiki guidance into a host fact.
- `[INF-docs]` labels an official Hyprland release, announcement, or wiki statement.
- `[OBS]` labels only the read-only host commands and file-presence reads retained in `.ufo/evidence/round-12/configera-host.txt`.
- `[UNK]` is retained where no permitted read exposes the answer.
- The forward config surface became Lua with Hyprland 0.55.0; this was a migration, not an immediate removal of hyprlang.
- Window-rule syntax had a documented breaking rewrite at 0.53; later opened release sources document additive fields/effects and a patch fix, not a second blanket syntax rewrite.

## Lua and hyprlang transition

- `[INF-docs]` On 2026-04-26, the maintainer announced Lua as usable on git or a future 0.55 release, still optional at that point; the announcement says the fallback was the existing `hyprland.conf` when no `hyprland.lua` existed ([ref], “Lua configs”).
- `[INF-docs]` The 0.55 announcement says the config is now done in Lua, encourages migration, and explicitly says the old config is not thereby broken ([ref], “Lua configs”).
- `[INF-docs]` The current start page describes hyprlang as deprecated in favor of Lua since 0.55 and gives `$XDG_CONFIG_HOME/hypr/hyprland.lua` as the config path; in the usual home setup that is `~/.config/hypr/hyprland.lua` ([ref], note and config location; page metadata modified 2026-08-26).
- `[INF-docs]` The forward-surface date is therefore the 0.55 release boundary, not the date the new wiki became visible or the later 0.56 release ([ref], “Lua configs”; [ref], “Lua configs”; [ref], page note).

### Announced hyprlang support window

The migration notice states:

> “The old hyprlang syntax will continue to be supported for 1 - 2 releases starting from 0.55. After that, hyprlang will be dropped.”

- `[INF-docs]` This is the exact upstream support promise, from “Old hyprlang syntax” in the 2026-04-26 migration announcement ([ref]).
- The same notice says new config features will no longer be added to hyprlang ([ref], “Old hyprlang syntax”).
- “1 - 2 releases” is a release-count window, not a calendar deadline or an exact named final supported tag.
- `[UNK]` These opened sources do not establish the exact final Hyprland release that accepts hyprlang or the actual removal release.
- The wiki’s current `deprecated` label is a status statement, not evidence that a particular installed binary rejects `.conf` syntax ([ref], page note).

### Default selection described by the migration notice

| Startup condition in the notice | Selected default file | Evidence class |
|---|---|---|
| No `hyprland.lua` in the config directory | `hyprland.conf` | `[INF-docs]` [ref], “Lua configs” |
| `hyprland.lua` exists | `hyprland.lua` instead of `hyprland.conf` | `[INF-docs]` [ref], “Lua configs” |
| Either file is created or removed after the process starts | The language choice is not re-detected in that process; restart is required to choose the other file | `[INF-docs]` [ref], “Lua configs” |
| A caller supplies a config path explicitly | The older v0.54 Start page documents `--config` / `-c`; this entry does not assert the exact precedence against Lua detection in v0.55+ | `[INF-docs]` [ref], “Start”; interaction `[UNK]` |

- The `.lua`-over-`.conf` rule is default startup auto-selection, not a merge of both files ([ref], “Lua configs”).
- The current wiki locates the new default under `$XDG_CONFIG_HOME`; the archived v0.54 page locates the legacy default at `$XDG_CONFIG_HOME/hypr/hyprland.conf` ([ref], config location; [ref], “Start”).
- The path statement applies to the documented default. It does not identify the exact file loaded by a running host with a possible explicit launch argument.

## Window-rule syntax across the opened 0.53–0.56 sources

| Version / date | Documented rule-era change | Source anchor | Class |
|---|---|---|---|
| 0.53.0 · 2025-12-29 | The release announcement calls the windowrule syntax completely overhauled and says all existing windowrules need rewriting. This is the explicit breaking syntax boundary. | [ref], “Breaking changes” | `[INF-docs]` |
| 0.54.0 archive · wiki page modified 2026-01-21 | The versioned archive documents the post-rewrite hyprlang form: anonymous `windowrule = match:class my-window, border_size 10`, plus a named `windowrule { ... }` form. | [ref], “Syntax” | `[INF-docs]` |
| 0.55.0 · 2026-05-09 | Lua became the preferred config language. The release adds the `confine_pointer` window-rule capability and its parser switch; these are additions, not a source claim that all rule syntax was rewritten again. | [ref], “Lua configs”; [ref], “New features” | `[INF-docs]` |
| 0.56.0 · 2026-07-20 | The announcement says there are no breaking changes and lists a `stableid:` windowrule field plus effects including `no_auto_hdr` and `suppress_event` for X11 configure events. | [ref], “Other” and opening paragraph | `[INF-docs]` |
| 0.56.2 · 2026-08-05 | The patch release backports a fix for `gaps_out` rule overriding `float_gaps`; exact patch level can matter even after a release advertised no breaking changes. | [ref], “Fixes backported” | `[INF-docs]` |

- The archived v0.54 rule page uses the `match:*` hyprlang form; the current page instead illustrates a Lua call such as `hl.window_rule({ match = { class = "my-window" }, border_size = 10 })` ([ref], “Syntax”; [ref], “Syntax”).
- The 0.53 release notice is the source for the actual mass rewrite; the 0.54 archive is evidence of the resulting legacy syntax, not proof every later field was accepted by every older binary ([ref]; [ref]).
- The 0.55 and 0.56 releases document named rule-surface additions. They do not constitute a complete parser-change log ([ref], “New features”; [ref], “Other”).
- `[UNK]` Whether any unlisted parser behavior changed in each 0.54–0.56 patch is outside the coverage of these release summaries; no global “unchanged” claim is made.

## Syntax comparison boundary

- `[INF-docs]` The v0.54 archive documents named blocks with `match:class = ...` and anonymous `windowrule = match:class ...` ([ref], “Syntax”).
- `[INF-docs]` The current wiki demonstrates the Lua call `hl.window_rule({ ... })` ([ref], “Syntax”).
- These examples establish two documented forms, not a full converter specification or a one-to-one field mapping.
- `[INF-docs]` The 0.53 overhauled syntax is the reason the v0.54 rule grammar is a post-rewrite baseline ([ref]; [ref]).
- `[INF-docs]` The 0.55 release adds `confine_pointer` and a parser switch; this is evidence of an additive rule feature, not proof all earlier parsing stayed equivalent ([ref], “New features”).
- `[INF-docs]` The 0.56 announcement lists `stableid:` and named effects; the 0.56.2 fix shows a rule issue can be corrected in a patch release ([ref]; [ref]).
- `[UNK]` No opened primary source provides a complete field-by-field compatibility matrix spanning 0.53–0.56 and all intervening patches.
- A syntax example never establishes that its effect fired on this host; this entry ran no dispatch or window-rule behavior probe.
- Keep the 0.54 hyprlang examples and current Lua examples in separate version-labeled examples; no automatic translation was attempted.


## Host position — read-only, 2026-10-19

- `[OBS]` `hyprctl version` reported Hyprland 0.56.2, tag `v0.56.2`, commit `efb50993780079460b0cbed1363e2166a2de1d9f`, clean build; selected identity output is retained in `.ufo/evidence/round-12/configera-host.txt`.
- `[OBS]` `hyprctl configerrors` exited 0 and printed no diagnostics in the retained probe.
- `[OBS]` The default `~/.config/hypr/hyprland.conf` exists; the `ls ~/.config/hypr/*.lua` presence sweep returned no matches.
- `[OBS]` A value-reduced `hyprctl systeminfo` projection exposed `configProvider: hyprlang` and no path value; it did not print titles, logs, or instance signatures.
- `[OBS]` The `hyprctl -j version` key inventory contains version/build fields but no selected-config path field.
- `[INF-docs]` The observed `hyprlang` provider, extant `.conf`, and absent `.lua` agree with the migration notice’s documented default selection ([ref], “Lua configs”).
- `[UNK]` The precise file opened by the running instance is not reported by the safe reads above. An explicit startup `--config` path cannot be ruled out; do not upgrade the default-selection rule into a direct loaded-path observation.
- Empty `configerrors` is parser-diagnostic evidence only; it is not a test of rule effects, window behavior, or full feature availability.

## Mado risk register: syntax-era-bound claims

| Existing claim or route | Why its syntax era matters | Safe use and recheck |
|---|---|---|
| `SKILL.md:24-25` — version pins; “window-rule syntax in particular changes between releases” | The 0.53 breaking rewrite and 0.55 language transition make an unversioned example ambiguous. | Keep the version pin beside every syntax claim; compare release-tagged docs before copying a rule. |
| `SKILL.md:344` — “wiki lua-era vs host hyprlang” docs-drift row | Current pages lead with Lua, while this host reports `configProvider: hyprlang` `[OBS]`. | Cite current wiki as `[INF-docs]`; use only version/configerrors and non-mutating reads for host claims. |
| `SKILL.md:40-47` — include order and “last file to set a key wins” | This is intra-`hyprland.conf` precedence. It does not define top-level `.lua` versus `.conf` startup selection. | State the two precedence domains separately; do not derive filename selection from include order. |
| `corpus/knowledge/keybind-rule-semantics.md:27-35,170-181` — 0.54 archive, current wiki, 0.53+ local rule syntax pin | Its grammar and semantic summaries are bound to the measured 0.56.2 host and cited docs; new Lua syntax is not interchangeable with old `windowrule =` lines. | Re-open both the exact version archive and current docs; maintain `[OBS]` parser facts apart from `[INF-docs]` semantics. |
| `corpus/knowledge/keybind-rule-semantics.md:291-295` — docs-drift limits and untested current-only properties | Current-only props/effects are not automatically evidence of host support, even when the old `.conf` parses without diagnostics. | Re-derive support at the pinned version; do not add a capability claim from the wiki table alone. |
| `corpus/README.md:49` — config, binds, rules and display route | Parsed declarations do not prove dispatcher behavior, rule effects, or `exec-once` results. | Keep syntax validation, effective-state reads, and behavior tests distinct; no rule is fired by this entry. |

## Limits

- This is a documentation-era map, not a complete Hyprland changelog or a compatibility matrix for every 0.53–0.56 patch ([ref]; [ref]; [ref]; [ref]).
- The support notice leaves a one-release uncertainty between “1 - 2”; it does not identify a specific last hyprlang tag ([ref], “Old hyprlang syntax”).
- The current wiki is a moving page; its page metadata says modified 2026-08-26. The v0.54 archive is versioned but its rules page metadata says modified 2026-01-21 ([ref]; [ref]; [ref]).
- The host reads do not reveal the exact selected configuration path, launch argument, or why the provider chose hyprlang; preserve `[UNK]` for those details.
- No host rule was added, edited, reloaded, dispatched, or behavior-tested; this work reads only.
- No host behavior is inferred from the 0.53–0.56 release notes.
- “No breaking changes” in the 0.56 announcement is limited to that release announcement; it does not negate the v0.56.2 backported rule bug fix ([ref]; [ref]).

## Rejected

| Rejected claim | Why it fails | Evidence |
|---|---|---|
| “Hyprland 0.55 immediately rejects every existing hyprlang config.” (ART M06) | The release announcement says the old config remains usable “for a few releases”; the migration notice gives the exact 1–2 release window. The host's no-error result is separately measured, not inferred from those notes. | [ref], “Old hyprlang syntax”; [ref], “Lua configs”; host evidence file. |
| “The host definitely loaded `~/.config/hypr/hyprland.conf` because no `.lua` file exists.” | The no-`.lua` sweep and `configProvider: hyprlang` are observations; no safe read returned the active path, and the archived Start page documents an explicit `--config` option. | [ref], “Start”; host evidence file. |
| “0.56’s no-breaking-changes announcement guarantees all window-rule behavior is unchanged throughout 0.56.” | The v0.56.2 patch notes list a window-rule bug fix for `gaps_out` overriding `float_gaps`; a release-level label is not a patch-level behavior freeze. | [ref], opening paragraph; [ref], “Fixes backported”. |
| “The wiki's current Lua examples prove the host's `.conf` parser supports every current property/effect.” | The current page is Lua-era documentation; neither it nor empty `configerrors` proves every named feature exists or behaves on this pinned host. | [ref]; [ref]; `corpus/knowledge/keybind-rule-semantics.md:291-295`; host evidence file. |

## Recheck and append-only errata

- Re-open the official Hyprland migration notice, 0.55/0.56 release notes, exact v0.56.2 tag, current config/rules pages, and the v0.54 archive on each relevant release or wiki migration ([ref]–[ref]).
- Re-measure `hyprctl version`, `hyprctl configerrors`, and the `hyprland.lua` presence sweep when updating the host position; do not reload, edit, or dispatch as a probe.
- If a later source clarifies the last supported hyprlang release or a rules-parser break, append a dated erratum naming the prior statement, replacement, source, and evidence class; do not silently rewrite the historical claim.
- No erratum is entered in this initial record.

## Errata (round 12, post-review)

- `source:` cites [ref] for the current Window Rules page. [ref] was rejected in the same round as a duplicate of [ref] (same URL `https://wiki.hypr.land/Configuring/Basics/Window-Rules/`, overlapping scope, no supersedes link); read every [ref] citation in this entry (header and line 67) as **[ref]** — same page, same "Syntax" section, same 2026-08-26 modification. The claim it supports is unchanged. Logged in `corpus/lessons/round-12.md` § Post-review registry changes.

## Errata (round 13 — complete citation mapping)

The round-12 parenthetical “header and line 67” was an incomplete enumeration.
**Every** historical [ref] occurrence in this entry, including the source header,
tables, rejected-inference row and recheck range, resolves to **[ref]**, not to
an admitted [ref]. This mapping preserves the old bytes and their rejection.
The current page was reopened on 2026-10-20 (Latest git; modified
2026-08-26); its introductory Note says “Since Hyprland 0.55, hyprlang is
deprecated in favor of lua.” This is dated documentation, not a refreshed
host-parser observation. The duplicate rejection is now explicitly recorded
by superseding registry row [ref]; the original [ref] stays rejected.
See `corpus/lessons/round-13.md` § Mistakes and Gate.

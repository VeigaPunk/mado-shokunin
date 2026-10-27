# ScoutHyprBinds — round-49 w1 findings

## Scope and result

Observed: the 0.56.0 wiki archive was added by hyprland-wiki commit `6bd8b15903d52acc445066bd76e2971ca669ecb0` (2026-07-20; commit message `selector: add 0.56.0`). Its archived Binds page is Lua-era, not the Hyprlang `bind = MODS, KEY, dispatcher, params` syntax relevant to this host’s config. The old path’s last Binds edit before the Lua rewrite is commit `78e64e80f4e84634744cd49728a198a7ebaf579a` (2026-03-13); therefore, do not present that file as a version-matched 0.56.x manual. It is the last pre-rewrite documentation for the legacy syntax, while the 0.56.0 archive itself documents the new Lua-era surface.

Observed: `6bd8b159`’s Binds and Variables files were fetched at that exact commit and saved in this seat. The last pre-rewrite Binds and Variables files were fetched at `78e64e80` and saved too. SHA-256:
- `Hyprland-wiki-Binds-6bd8b159.md`: `3d8a2a6832da59304697aff1a3c72a35e02ea43737035c99b841d0854b17d628`
- `Hyprland-wiki-Variables-6bd8b159.md`: `c53c565c776e78390b6b106a352333912c13c59a2630af081f141b2c97175527`
- `Hyprland-wiki-Binds-78e64e80.md`: `ee723d12715e249d8c3b5ee052d541b89e8fef24e560c036bfdbec97c5dfed63`
- `Hyprland-wiki-Variables-78e64e80.md`: `9d89d79fc7a4df872eb682d1c9771e8117ec84f6acf61c72017e03ebb0a63eff`

## Pinned source URLs and located text

All quote fragments below are <=25 words and were checked with `grep -n` against the copied, fetched files named above.

### The 0.56.0 archive (Lua-era docs)

- Binds: <https://raw.githubusercontent.com/hyprwm/hyprland-wiki/6bd8b15903d52acc445066bd76e2971ca669ecb0/content/Configuring/Basics/Binds.md>
- Variables: <https://raw.githubusercontent.com/hyprwm/hyprland-wiki/6bd8b15903d52acc445066bd76e2971ca669ecb0/content/Configuring/Basics/Variables.md>

Binds page, line 40: “The name you should use is the segment after `XKB_KEY_`.” It points readers at the xkbcommon keysym header, but does not explain alias canonicalization or whether bind parsing is case-insensitive. Line 46 demonstrates `code:28`. Lines 462-474 say the first input layout is used for binds by default; `resolve_binds_by_sym = 1` makes a bind activate when the typed symbol matches. The `us,fr` illustration describes a symbol-following binding shifting to the corresponding character-producing physical key. Line 531 says unbind is case-sensitive and must exactly match bind capitalization; that statement concerns *unbind*, not whether `bind` parsing is case-sensitive.

### Last pre-Lua Hyprlang-era documentation (not version-matched 0.56.x)

- Binds: <https://raw.githubusercontent.com/hyprwm/hyprland-wiki/78e64e80f4e84634744cd49728a198a7ebaf579a/content/Configuring/Binds.md>
- Variables: <https://raw.githubusercontent.com/hyprwm/hyprland-wiki/78e64e80f4e84634744cd49728a198a7ebaf579a/content/Configuring/Variables.md>
- 0.54.0 archive’s switchable-layout page (rendered archive): <https://wiki.hypr.land/0.54.0/Configuring/Uncommon-tips--tricks/>

Binds file line 62 has the same header/name instruction. Lines 64-71 document the `code:` prefix and example `code:28`; line 80-81 says workspace-bind keys must be available unmodified in the layout, illustrating French AZERTY. Lines 111-117 say unbind is case-sensitive, with `TAB` versus `Tab` examples—again, this establishes unbind behavior only. Lines 512-518 define `catchall`. It contains no account of the `mouse:N`, switch or `mouse_up/down` key-form semantics beyond examples, and it does not itself explain layout resolution.

Variables file lines 175-181 lists the XKB input settings and states for `resolve_binds_by_sym`: “If false, keybinds will always act as if the first specified layout is active”; if true, “keybinds specified by symbols are activated when you type the respective symbol with the current layout.” Default is false. The unversioned 0.54.0 archive’s Uncommon Tips page lines 802-811 expands this with `us,ua` / `ua,us` and `us,fr` examples; rendered archive was fetched and text-extracted locally. The documentation does not establish source-level pressed-symbol selection, modifier matching, or precedence between keycode and keysym binds.

### Useful caution about version selection

The 0.56.0 rendered Binds page at <https://wiki.hypr.land/0.56.0/Configuring/Basics/Binds/> is Lua syntax (`hl.bind`) and includes the layout section; its page “Last updated” timestamp is July 15, 2026. The 0.56.0 archive was introduced five days later by `6bd8b159`. This surfaced archive is thus a real pinned-version URL but not a guarantee that its page represents the `bind =` config dialect still found in this host’s 0.56.2 configuration. The separate 0.54 archive is Hyprlang (`bind =`) and is the most recent available pre-rewrite docs snapshot; the raw page used above is at exact commit `78e64e80`, not the archive’s unverified build commit.

## Issues/discussions search

Searches run through web search on 2026-10-27; its responses explicitly reported that the exact `site:github.com/hyprwm/Hyprland/issues` constraint matched no results and relaxed it. These are discovery results, not a complete GitHub API census (GitHub API requests later hit rate limit). Query strings and returned result accounting:

1. `site:github.com/hyprwm/Hyprland/issues bind non-us layout keysym keybind` — search reported no matches under the constraint; relaxed response returned 10 general results, 0 exact Hyprland issues. Excluded 10 mixed/non-Hyprland results.
2. `site:github.com/hyprwm/Hyprland/issues Hyprland bind non latin keyboard layout Cyrillic` — no exact constrained matches; relaxed response returned 10 general results, 0 exact Hyprland issues.
3. `site:github.com/hyprwm/Hyprland/issues code: bind keycode layout keysym` — no exact constrained matches; relaxed response returned 10 general results, 0 exact Hyprland issues.
4. `site:github.com/hyprwm/Hyprland/issues bind keysym case sensitive TAB Tab keybind` — no exact constrained matches; relaxed response returned 10 general results, 0 exact Hyprland issues.
5. Broadened `Hyprland keybind/layout problems` — 4 supplied Hyprland issue results among 4 listed: #475 (layout switching), #9632 (keyboard input), #3695 (different layouts break binds), #5332 (custom layouts). #3695 is the directly relevant result, but the web result summarizes different layouts across separate keyboards; it is old and not evidence of current behavior.
6. Broadened `Hyprland Russian keyboard bind issue github` — 10 results returned; direct repo results included #9632, #7084, #3695 and #4598; no specifically non-Latin regression established from snippets.
7. `Hyprland bind code: keycode issues github discussion` — 10 results returned. Relevant discovery links: discussion #14677 (`Codes not being parsed in Hyprland 0.55 Lua`), #14819 (`Lua hl.bind(code:N) fires on all KEY_UNKNOWN events`), #13962 (left/right modifier key location); other returned results excluded as unrelated.
8. `Hyprland bind case sensitive keysym issue github` — 10 results returned. Relevant discovery: discussion #13020 (`unbind` case-sensitive versus bind); others excluded as unrelated.

Pinned direct links for relevant discussion candidates: <https://github.com/hyprwm/Hyprland/discussions/13020>, <https://github.com/hyprwm/Hyprland/discussions/14677>, <https://github.com/hyprwm/Hyprland/discussions/14819>, <https://github.com/hyprwm/Hyprland/discussions/13962>, and issue <https://github.com/hyprwm/Hyprland/issues/3695>. Fetched GitHub HTML pages confirmed titles for all four discussions; the search snippets, not a full source-code audit, supplied the summaries above. Issue #3695 returned 404 at the old issue URL during direct fetch; do not quote or treat the search snippet as verified issue text. These are leads and context only, not authoritative semantic ground.

## Confidence and gaps

High confidence in the wiki commit IDs, paths, and literal prose: raw copies are pinned by full commit URL, hashed, and line-located. Medium confidence in the archive interpretation: 0.56.0 URL is demonstrably Lua-era, while the host contract expressly concerns legacy `bind =`; the wiki’s versioned archive is not a source-level proof of host parser behavior. Search coverage is low/partial: no successful exhaustive issues/discussions query because GitHub API quota was exhausted; web-search snippets are incomplete, and #3695 could not be fetched directly. No claim is made here about Hyprland 0.56.2 implementation behavior, case flags in `xkb_keysym_from_name`, pressed key layout/state, exact modifier mask equality, or keycode-vs-keysym precedence; those require the assigned pinned source files, not these docs/issues.

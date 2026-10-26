# ScoutRecheck - upstream drift since the pins (round 45, 2026-10-26 ~16:00 -03)

Question: is efb50993 still what the host runs, and has the monitor code moved upstream? Pins: `.ufo/waves/round-45/fetch/` (sha256 `.ufo/waves/round-45/receipts/fetch-sha256.txt`). Main side: `fetch-main/` here, sha256 `fetch-main-sha256.txt`.

## 1. Host = pins (read-only commands, run in this seat)

- `hyprctl version`: `Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean`, Hyprutils built against 0.14.2 and system has 0.14.2, Version ABI string starts `efb50993780079460b0cbed1363e2166a2de1d9f_aq_0.15_hu_0.14...`.
- `pacman -Q hyprland hyprutils`: `hyprland 0.56.2-4`, `hyprutils 0.14.2-1`.
- Result: EQUAL to the pins (commit efb50993..., hyprutils 0.14.2). No host drift. `git ls-remote` shows `refs/tags/v0.56.2 = efb50993...` and no tag newer than v0.56.2 (latest release API: v0.56.2, 2026-08-05T14:14:01Z): the pins are also still the newest *release*.

## 2. Upstream main today

Main tip fetched: `fb6e5380228b2908ed9b74867a32b26f623a0cec` (committed 2026-10-26T15:20:07Z, "layout/scrolling: make click behaviour when `follow_focus != 0` configurable (#16641)"; VERSION file there reads 0.56.0). All `fetch-main/` files are fetched at that commit SHA, not at the moving `main` ref (a first fetch at `main` was byte-identical for the four files compared: cmp, IDENTICAL).
GitHub compare efb50993...fb6e5380: `diverged`, main 339 ahead / 36 behind (efb50993 is on the v0.56 release line; merge base v0.56.0 36b2e0cf). So "main" is a different line from the 0.56.x tags, not a successor of them.

### 2.1 Unchanged semantics (the claims the tool/entry rest on)

Method: whitespace-collapsed text diffs with `Log::logger->log(` normalised to `LOG(`.

| Pin (efb50993) | Main file | Verdict |
|---|---|---|
| Parser.cpp (sha 616468fd...) | src/config/shared/monitor/Parser.cpp (299d1e7b...) | log-call spelling `Log::logger->log` -> `LOG`, `#include <format>`, modeline name via `std::format_to_n` instead of `snprintf`. No change in parseMode / parsePosition / parseScale / parseTransform logic. |
| MonitorRuleManager.cpp (17d46685...) | same path (4af59c24...) | logging spelling; drops `#include render/Renderer.hpp` and, after the apply loop, the `arrangeLayersForMonitor(m->m_id)` loop plus `Event::bus()->m_events.monitor.layoutChanged.emit()` (pin lines 196-204). `add` / `get` rule lookup unchanged (newest match, empty-selector fallback, built-in default). |
| MonitorRule.hpp (b01d31a1...) | same path | byte-identical (default `m_refreshRate = 60` still line 46). |
| MonitorPositionController.cpp (3b705388...) | src/state/ same (44c98b84...) | logging spelling only (normalised text equal). |
| Monitor.cpp (9cf88e15...) | src/output/Monitor.cpp (265101af...) | applyMonitorRule body (pin 719-1082, main 695-1060): only changes are an error-overlay `std::format`, and the redraw trigger now also fires when `m_transformedSize` changed (main 1038, 1047). matchesStaticSelector and the short-description line are identical. Mode choice (`abs(refresh/1000 - rule)` pin 828 = main 804) and the 1/120 scale search (pin 1001 = main 977) unchanged. Everything else in the file is workspace/commit-coordinator refactor, not rule logic. |

Locators shift by ~24 lines in Monitor.cpp (pin 1001 -> main 977), by 7 lines in HyprCtl (pin 241 -> main 234).

### 2.2 What moved (STRUCTURAL - these are the real drift)

1. **The hyprlang `monitor =` line handler is gone on main.** `src/config/legacy/ConfigManager.cpp` (the pin S303, handleMonitor 1293-1387, handleMonitorv2 788-880) no longer exists: commit `a9902ea65f461af868497c4e74fed798ade0b1b0` "config: remove legacy config support (#15539)", 2026-07-22T16:35:10Z, 29 files (`fetch-main/api-commit-a9902ea-meta.json`). It is NOT in v0.56.2 (compare a9902ea...efb50993: diverged, merge base v0.56.0 2026-07-20). Main `src/config/ConfigManager.cpp` (69 lines) builds only `Lua::CConfigManager` for both regular and special configs, `typeToString` knows only `CONFIG_LUA`, and `Jeremy.cpp` looks for `hyprland.lua` (`findConfig("hyprland","lua")`, recovery file `recoverycfg.lua`). There is no `monitor = ...` text grammar left to join a tool against; the rule source is `hl.monitor({ output = ..., mode = ..., position = ..., scale = ..., ... })` (main LuaBindingsConfigRules.cpp:1081-1119, `MONITOR_FIELDS` from line 81).
2. **sdr_eotf is now a first-class monitor key - in the Lua table form.** Main MONITOR_FIELDS has `sdr_eotf` (LuaBindingsConfigRules.cpp:120, default `"default"`), and so do `mirror`, `bitdepth`, `cm`, `sdrbrightness`, `sdrsaturation`, `vrr`, `icc`, `transform`, `reserved_area`, `supports_*`, `*_luminance`, `disabled`; unknown fields error (`unknown field '{}'`, line 1119). So the entry's divergence "wiki documents sdr_eotf, the 0.56.2 line handler does not accept it" is *resolved by the removal of the line form*, not by adding the key to the line handler. On 0.56.2 the line handler still has no `sdr_eotf` (pin handler lists 8 keys; the only `sdr_eotf` in the pinned legacy file is the `monitorv2` special value, pin lines 576 and 819).
3. **hyprctl moved and the JSON grew.** `src/debug/HyprCtl.cpp` is gone; the request is `src/ipc/s1/Commands.cpp` (404 at the old path). `monitorsRequest` main 323, JSON `"refreshRate": {:.5f}` main 234 (still five decimals). Added/changed keys: `activeWorkspace`/`specialWorkspace` carry `address`, optional `id`, `type`, `name` (pin: `id`, `name`); new `hardwareDetails` object (`backend`, `hdr`, `chroma`, `bt2020`, `vrrCapable`). Fields the tool joins on (`name`, `width`, `height`, `refreshRate`, `x`, `y`, `scale`, `transform`, `disabled`, `mirrorOf`) are present unchanged.
4. **Wiki moved and was rewritten Lua-only.** `content/Configuring/Monitors.md` (the pin S310) returns 404 at wiki main `6d26139c...` (2026-10-26T15:20:17Z); the page became `content/configuring/core/monitors/{_index,colors,modes,output-selection,positioning}.md` by `e99eac80` "Update Configuration pages for the new lua configuration system (#1434)", 2026-04-26 (the pin ecc06f3b is 2026-04-20, six days earlier, so the pinned page is the last hyprlang-era form). Main pages: `grep` finds `hl.monitor(` everywhere and no `monitor =` line; `sdr_eotf` is documented only as an `hl.monitor` table key (`wiki-monitors-_index.md:21`, `wiki-monitors-colors.md:43`), not on the line form. Answer to "does main still document sdr_eotf on the line form": NO - the line form is not documented at main at all.
5. Release status: no tag after v0.56.2. A package update on this host stays on the v0.56 line (hyprlang + Lua both supported) until a release cut that contains a9902ea; that release makes `monitors.conf` inert unless the user migrates to `hyprland.lua`.

## 3. Entry sentences that go stale on that upgrade (`l1-draft/entry.md` line numbers)

- l.3-4, l.1 title, l.82 and the whole S303 row (`monitor` keyword handler, line grammar, eight keys): the handler is deleted; S303 and the `monitor =` grammar become history of the 0.56 line. Sentences l.32-36 (positional fields, modifiers `disable`/`transform`/`addreserved`, key loop of eight keys, "any other key rejects the whole line") describe only 0.56.x.
- l.27 and l.78 (sdr_eotf divergence, "the wiki documents it; the host's handler reads it only in monitorv2"): stale on both sides - the wiki page is Lua-only and sdr_eotf is a Lua field.
- l.8 and l.68-70 (S307 `src/debug/HyprCtl.cpp`, JSON field list and `HyprCtl.cpp:241-242`/`313-321` locators): path and locators move to `src/ipc/s1/Commands.cpp` (234, 323); the JSON gained `hardwareDetails` and workspace `address`/`type`.
- l.56 / S306 locators (`Monitor.cpp:1201-1211`, `:719-1082`, `:250-256`, scale search): the content holds; line numbers shift ~24.
- l.89 (monitorv2 untraced): moot on main (v2 blocks are removed with the legacy manager).
- l.1-2 / census: "Hyprland 0.56.2" scoping is already correct; the census line (`default_refresh=60 refresh_tolerance=1 scale_step=1/120 scale_search=89 json_refresh_decimals=5 line_keys=8`) stays true of 0.56.2; `line_keys=8` has no main counterpart.
- S302 (Parser.cpp), S304 (MonitorRuleManager.cpp), S305 (MonitorRule.hpp), S308 (MonitorPositionController.cpp), S309 (hyprutils 0.14.2) sentences: still true on main (log-spelling and layer-rearrange-after-apply changes only; S304 sentence "One rule per selector string; newest matching rule wins, else first empty-selector rule, else built-in default" unchanged).

## 4. What `recheck:` should say (replace l.13)

Proposed text: `recheck: on a Hyprland or hyprutils package change on the host, or 90d - re-pull the nine pinned files and re-run the counter. Drift at 2026-10-26: host = pins (0.56.2-4, efb50993); main (fb6e5380) drops the monitor-line handler (a9902ea, 2026-07-22, "remove legacy config support") and the HyprCtl.cpp/Monitor.cpp/wiki paths, so a release past 0.56.x invalidates S303, S307, S310 and the line-grammar/sdr_eotf rows, not S302/S304/S305/S308.`
Trigger precision: the hard trigger is `hyprctl version` leaving commit efb50993 AND (a) `src/config/legacy/ConfigManager.cpp` 404 at the new commit (a9902ea ancestor), or (b) `~/.config/hypr/hyprland.lua` replacing `hyprland.conf`; either makes `tools/mado-monitors.py` (which reads `monitor =` lines) unusable and its Lua twin (`hl.monitor` tables) the next capability.

## 5. Gaps

- Not traced: first release that will contain a9902ea (no tag yet; main VERSION still 0.56.0). Not verified: whether upstream ships a hyprlang-to-Lua converter (grep of Jeremy.cpp finds none; the wiki page `content/hypr-ecosystem/dev/hyprlang.md` is the library page). Whole-file Monitor.cpp diff beyond the three rule-relevant ranges was classified by reading hunks, not line-by-line proven equal.
- No wiki hyprlang-era page is retained at wiki main (tree listing of `content/configuring` shows no legacy page), so S310 stays citable only by its commit pin.
- Tools used: curl, python3 difflib, git ls-remote, GitHub REST API (unauthenticated). No host mutation; `hyprctl version` and `pacman -Q` only.

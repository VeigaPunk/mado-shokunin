# Wiki variables and keywords — source-opening report

## Result

**No matching hyprlang-era source page was openable at the assigned wiki pin** (`c66e8de21f5ecdc4bc5e278e7d94800ea10957af`). I found no pinned documentation establishing `$variables` expansion or the `source`, `exec`, and `exec-once` keyword semantics. This source-opener item therefore supplies no C1 semantic evidence.

The browsed pinned tree is organized around the Lua-era configuration. `content/configuring/core/_index.md` identifies `hyprland.lua` as the configuration file and says Hyprland uses Lua; `content/configuring/core/autostart.md` documents a `hyprland.start` Lua event with `hl.exec_cmd`, not the hyprlang autostart keywords. The FAQ search returned the Lua statement at `_index.md:36` (“Hyprland will continue using Lua.”), but that is not a description of the legacy parser or its bind-table construction. I did not substitute these pages or an older wiki revision for the requested source.

## Search and fetch evidence

Inspected pinned GitHub tree pages:

- `https://github.com/hyprwm/hyprland-wiki/tree/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content` lists `configuring`, `faq`, `getting-started`, and other current sections; no legacy-version directory is listed.
- `https://github.com/hyprwm/hyprland-wiki/tree/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring` lists `core`, `extra`, `layouts`, and `_index.md`, `code-snippets.md`, `naming-conventions.md`, `selectors.md`.
- `https://github.com/hyprwm/hyprland-wiki/tree/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core` lists `advanced-configuration`, `binds`, `monitors`, `rules`, `_index.md`, `animations.md`, `autostart.md`, `config-options.md`, `devices.md`, `dispatchers.md`, and `environment-variables.md`; it lists no `keywords` or `variables` page.
- The `advanced-configuration` tree lists `_index.md`, `events.md`, `lua-utilities.md`, `notifications.md`, `permissions.md`, and `using-hyprctl.md`; it lists no keyword reference.

Exact source fetches attempted from the lane working directory `/home/vgpnk/Projects/shokunin/mado-shokunin`:

```sh
timeout 30 curl -fsSL 'https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/Configuring/Keywords.md' -o '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/WikiVariablesKeywords.bin'; rc=$?; printf 'exit=%s\n' "$rc"
```

Output: `curl: (22) The requested URL returned error: 404`; `exit=22`.

```sh
timeout 30 curl -fsSL 'https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/Configuring/Variables.md' -o '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/WikiVariablesKeywords.bin'; rc=$?; printf 'exit=%s\n' "$rc"
```

Output: `curl: (22) The requested URL returned error: 404`; `exit=22`.

Additional raw-path checks at the same pin returned HTTP 404 for `content/configuring/core/keywords.md`, `content/configuring/core/variables.md`, and `content/configuring/core/advanced-configuration/keywords.md`. The designated fetch path `.ufo/waves/round-25/fetch/a3w1/WikiVariablesKeywords.bin` does not exist after the failed fetches; no source bytes were retained.

## SOURCES row, quotes, and duplicate review

- **Draft row:** none. No relevant pinned source bytes were available, so a row with a verified URL, hash, byte count, line anchors, and teaching summary would be unsupported.
- **Located quotes:** none from the requested hyprlang-era source. There are no decoded source bytes against which the required quote-substring check can be performed.
- **Duplicate URL check:** compared the candidate keyword/variable URLs and the pinned paths above with `corpus/SOURCES.md` rows S153–S168. No candidate URL duplicates those rows. The existing wiki rows S165 and S168 are for `window-rules.md` and `rules/_index.md`, respectively, not keyword/variable references.

## Gates and scope

- **C1 sourced-evidence gate:** not met by this item; legacy variable expansion and source/exec keyword semantics remain unsupported by a source opened at the assigned pin.
- **C1 implementation, control scoring, C2, and host behavior:** not run or claimed.
- **Touched surfaces:** this report only. No product code, corpus file, counter, or fetch artifact was written.
- **Limits:** the findings are limited to the pinned tree pages and raw paths checked above. I did not search or cite older wiki revisions or make claims about Hyprland implementation behavior.

Report path: `.ufo/waves/round-25/a3w1/reports/WikiVariablesKeywords.md`.
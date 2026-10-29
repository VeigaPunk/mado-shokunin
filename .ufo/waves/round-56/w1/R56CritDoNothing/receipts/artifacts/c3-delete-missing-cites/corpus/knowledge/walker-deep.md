# Walker deep-note — config semantics end-to-end (M5-3)

Lane: mado-shokunin. Assignment M5-3 (round 5, probation). Measured
2026-10-14 17:00–17:25 UTC on host `plazir27`, compositor session Hyprland
PID 1203316 (`hyprctl -j instances` `time` 1791994267 = 16:11:07 UTC — the
replacement session recorded in round 4). Substrates READ-ONLY: nothing under
`~/.config/`, `~/.local/share/omarchy/`, `/etc/` or `~/Projects/` was written;
`~/.config/walker/config.toml` and its elephant peers were re-hashed before and
after the pass (identical, §13). The walker/elephant unix sockets were **stat'd,
never connected**; the only daemon conversation was elephant's own read-only CLI
query `elephant listproviders`. Scratch: `/tmp/w5-m5-3-probe/` (walker string
dump, elephant-generated docs, scratch config dir; ephemeral). One probe
outlier — a bare `elephant` invocation that started and exited — is recorded in
§13 with its before/after checks.

Tag legend: **OBS** measured (file bytes, command output, CLI read),
**RUN** a pure-read producer executed, **INF** inference with basis stated,
**UNK** not measurable this pass. Every non-obvious row carries a `path:line`
or the command that produced it.

---

## §1 Live snapshot (this pass)

| Component | Version | Runtime evidence |
|---|---|---|
| walker | `walker --version` → `2.17.0`; pkg `2.17.0-1` | PID 1203471 `/usr/bin/walker --gapplication-service`, started `Wed Oct 14 13:11:07 -03` (=16:11:07 UTC) |
| elephant | `elephant version` → `2.21.0`; pkg `2.21.0-1` | PID 1203474 `elephant`, same start second; child `wl-paste --watch echo clipboard-changed` in its cgroup |
| omarchy | `omarchy version` → `3.8.3`; checkout `git describe --tags` → `v3.8.4` (clean) | both pins re-measured; the two-value caveat stays (cf. R4-E4) |

**OBS** — units: `app-walker@autostart.service` is *generated* by the
systemd-xdg-autostart generator from `~/.config/autostart/walker.desktop`
(`systemctl --user cat`), with drop-in
`~/.config/systemd/user/app-walker@autostart.service.d/restart.conf`
(`Restart=always`, `RestartSec=2`) plus the generator's `slice-tweak.conf`.
`elephant.service` is a hand-installed user unit
(`~/.config/systemd/user/elephant.service`), `ExecStart=elephant`,
`Restart=on-failure`. Neither unit declares `Environment=` or `EnvironmentFile=`
(`systemctl --user show … -p Environment -p EnvironmentFile` → empty) — so
`$OMARCHY_PATH` is **not** unit-provided (INF: it comes from the login session
as the omarchy scripts are invoked from interactive contexts).

**OBS** — sockets exist, mode `srwxr-xr-x`, size 0, created 13:11:09:
`$XDG_RUNTIME_DIR/walker/walker.sock`, `$XDG_RUNTIME_DIR/elephant/elephant.sock`.
**OBS** — D-Bus: `dev.benz.walker` is owned by PID 1203471 (`busctl --user list`
→ `dev.benz.walker 1203471 walker`). **OBS** — the launcher is closed:
`hyprctl -j layers` lists only `wallpaper` (PID 1203358) and `waybar`
(PID 1203352) — no walker layer surface, which is why no statement below about
*rendered* walker output is an OBS.

**OBS** — copies of the two config layers are byte-identical to their omarchy
stock sources: user `~/.config/walker/config.toml` sha256[:16]
`fecf71fa4253803e` (1,336 B, mtime 2026-10-03 17:44:32) = `diff`-clean against
`~/.local/share/omarchy/config/walker/config.toml`; `~/.config/autostart/
walker.desktop` `diff`-clean against
`~/.local/share/omarchy/default/walker/walker.desktop`. **INF** — a
`omarchy refresh walker` today would restore nothing user-authored (contrast the
waybar drift in the round-1 note §6).

---

## §2 Config layering and merge semantics

### 2.1 The four layers

| Layer | Object | Measured |
|---|---|---|
| L0 embedded default | default config table compiled into `/usr/bin/walker` | **OBS** — `python3`: the byte run starting at `blob.find(b'force_keyboard_focus = false')` (offset 784,064) equals `/etc/xdg/walker/config.toml` **verbatim** (`embedded==file: True`), followed by `config.toml WALKER_ …` |
| L1 packaged | `/etc/xdg/walker/config.toml` | **OBS** — 298 L / 13,220 B, sha256[:16] `5b4e47b7d2314bf8`, mtime 2026-07-26 21:42 |
| L2 user | `~/.config/walker/config.toml` | **OBS** — 49 L / 1,336 B, sha256[:16] `fecf71fa4253803e` (= omarchy stock copy) |
| L3 env / config-dir | tokens `WALKER_` and `config.toml` adjacent in the binary; config-crate `Environment`/`FileSource` tokens | **OBS** tokens; semantics **UNK** (env-override prefix inferred, not exercised) |

**INF (high)** — L0/L1 are the same document; the packaged file is an installed
copy of the embedded default (identical bytes, L1 mtime predates all omarchy
activity). Consequence: removing L1 changes nothing as long as the binary is the
same version.

### 2.2 Merge is partial-table over defaults (the design in evidence)

**OBS** — the binary's type-name run contains `struct Walker`,
`struct PartialWalker`, `struct PartialProviders`, `struct PartialKeybinds`,
`struct PartialShell`, `struct PartialClipboard`, `struct Shell`,
`struct Placeholder`, `struct Keybinds`, `struct ProviderSet`, `struct Prefix`.
The `Partial*` types are the signature of a "parse the user file into an
optional-field overlay, then fold onto the defaults" design.

**OBS** — the same binary carries the `config`-crate file-format tokens
(`Ini`, `Ron`, `Json5` in `ymlinironjson5…`, plus `try_parsing`, `convert_case`,
`list_separator`, `ignore_empty`, `keep_prefix`, `Environment`, `FileSource`,
`format`, `from_str requires a set file format`) — i.e. walker parses its TOML
through config-rs-style layering.

**INF (high)** — tables merge per key (scaler keys absent from L2 fall through
to L1: e.g. `close_when_open`, `click_to_close`, `[shell]` anchors), while
**arrays are replaced wholesale** (config-crate semantics). The packaged file
carries the matching comment for the one table it matters for:
`/etc/xdg/walker/config.toml:112` — "This will be **MERGED/OVERWRITTEN** with
what the user specifies".
**Consequence (INF)** — the user's six `[[providers.prefixes]]` entries replace
the packaged ten; if arrays merged instead, `.` would route to both `files`
(user `:28-29`) and `symbols` (packaged `:81-83`) — a contradiction no shipped
config would pass CI with. The exact search order was not executable read-only
⇒ stated as INF, not OBS. **Similarly**: `[keybinds]` merges per key, so setting
`quick_activate = []` disables quick activation without dropping
`close`/`next`/`page_down`/… (the 12 other arrays stay from L1).

### 2.3 The full key universe (recovered from the binary)

**OBS** — the binary contains `struct Walker with 29 elements`,
`struct Keybinds with 13 elements`, `struct Shell with 6 elements`,
`struct Placeholder with 2 elements`, `struct EmergencyEntry with 2 elements`,
and a field-name run. Reconciling the run with the two files: 21 scalar keys +
6 tables (`shell`, `columns`, `placeholders`, `keybinds`, `providers`,
`emergencies`) + `additional_theme_location` + `installed_providers` = 29.
`installed_providers` appears **only** in the binary run — no file in either
layer sets it (runtime-populated candidate; **UNK**). The 13 keybind keys are
exactly `close, next, previous, left, right, down, up, toggle_exact,
resume_last_query, quick_activate, page_down, page_up, show_actions`.

### 2.4 User overrides, key by key (L2 vs L1)

| Key (user anchor) | User value | Packaged default | Effect of the override |
|---|---|---|---|
| `force_keyboard_focus` (`:1`) | `true` | `false` (`:1`) | keyboard focus stays in walker; walker's own warning token: "windows might potentially not be focused if force_keyboard_focus is true" |
| `selection_wrap` (`:2`) | `true` | `false` (`:6`) | list wraps at ends |
| `theme` (`:3`) | `omarchy-default` | `default` (`:9`) | selects the omarchy theme dir (§6) |
| `additional_theme_location` (`:4`) | `~/.local/share/omarchy/default/walker/themes/` | — (absent) | extra theme search root; `~` expansion at runtime **UNK** |
| `hide_action_hints` (`:5`) | `true` | `false` (`:14`) | per-item action hints hidden |
| `[placeholders] default` (`:7-8`) | input `"\uf002 Search..."` (U+F002 char measured), list `"No Results"` | input `"Search"` (`:35`) | magnifier glyph added to the input placeholder |
| `[keybinds] quick_activate` (`:10-11`) | `[]` | `["F1".."F4"]` (`:47`) | empty array = quick activation off |
| `[columns] symbols` (`:13-14`) | `1` | `"symbols" = 3` (`:31-32`) | grid columns for the `symbols` provider (packaged key is quoted — same TOML key); the inline comment "providers to be queried by default" is wrong and already corrected in R4-E3 |
| `[providers] max_results` (`:17`) | `256` | `50` (`:61`) | global result cap |
| `[providers] default` (`:18-21`) | `desktopapplications`, `websearch` | same + `calc` (`:53-58`) | `calc` no longer queried without a prefix |
| `[[providers.prefixes]]` (`:23-45`) | 6 routes (below) | 10 routes (`:69-107`) | wholesale remap (see §4.3) |
| `[[emergencies]]` (`:47-49`) | 1 entry: `Restart Walker` → `omarchy-restart-walker` | — | fail-safe row (§7.4) |

**OBS** — every key *not* listed above is inherited from L1 and therefore
active with its packaged value: `close_when_open=true`, `click_to_close=true`,
`as_window=false`, `single_click_activation=true`, `global_argument_delimiter="#"`,
`exact_search_prefix="'"`, `disable_mouse=false`, `debug=false`,
`page_jump_items=10`, `hide_quick_activation=false`, `hide_action_hints_dmenu=true`,
`hide_return_action=false`, `keybind_symbols=true`, `resume_last_query=false`,
`actions_as_menu=false`, `autoplay_videos=false`,
`ext_background_effect_blur=false`, and the `[shell]` block
(`exclusive_zone=-1`, `layer="overlay"`, all four anchors `true`).

---

## §3 Syntax map (how the TOML is written — and read)

**OBS** — the idioms in both layers, each exercised by the live files:

- scalars as `key = value` with trailing `#` comments that *are* the local
  documentation (there is no walker man page: `man walker` → no entry);
- `[[providers.prefixes]]` — an **array of tables**, one table per route
  (`prefix`, `provider`); user file `:23-45`, packaged `:69-107`;
- `[columns]` — a table keyed by provider name (`"symbols" = 3`; quoting is
  cosmetic);
- `[placeholders]` — inline tables (`"default" = { input = …, list = … }`);
- `[keybinds]` — arrays of strings; `[]` disables a binding set;
- `[providers.actions]` — a table of **arrays of records** with fields
  `action`, `label`, `bind`, `default`, `after` (the `after` values in use:
  `Nothing`, `Close`, `KeepOpen`, `AsyncReload`, `AsyncClearReload`,
  `ClearReload`);
- `[[emergencies]]` — array of tables with exactly two fields (`text`,
  `command`; struct arity confirmed in §2.3);
- `[providers.argument_delimiter]`, `[providers.sets]`,
  `[providers.max_results_provider]` — tables that may be empty (`:63-67`).

**OBS** — the file is parsed by the config-crate (`§2.2` tokens), so TOML
comments/quotes follow config-rs. What happens on an *unknown key* or an
ill-formed table was **not** measurable without running the binary against a
UI-opening command ⇒ **UNK** (the `unknown_fields` token in the binary suggests
either tolerance or a serde error path; not resolved).

---

## §4 Providers end-to-end

### 4.1 The engine: elephant

**OBS** — walker owns no data sources; all providers are elephant plugins in
`/usr/lib/elephant/`: `bluetooth.so, calc.so, clipboard.so,
desktopapplications.so, files.so, menus.so, providerlist.so, runner.so,
symbols.so, todo.so, unicode.so, websearch.so` (12 files).

**OBS (RUN, read-only)** — `elephant listproviders` against the running daemon
returned 13 providers: `websearch, desktopapplications, files, runner, symbols,
unicode, calc, clipboard, menus:omarchythemes,
menus:omarchyBackgroundSelector, menus:omarchyunlocks, providerlist, todo`.
`bluetooth` is **absent** even though its `.so` is installed: elephant's own
startup log says `bluetoothctl not found. disabling` (observed in the §13
outlier run; consistent with `command -v bluetoothctl` being empty, per the
round-3 note §3.3).

**OBS** — `elephant generate doc` (read-only; output captured to
`/tmp/w5-m5-3-probe/allprov-docs.md`, 644 L) documents the provider engine and
every provider. `ElephantConfig` (`~/.config/elephant/elephant.toml`, not
present here ⇒ defaults): `auto_detect_launch_prefix=true`, `launch_prefix`,
`terminal_cmd`, `overload_local_env=false`, `ignored_providers=[]`,
`git_on_demand=true`, `before_load=[]`, `provider_hosts` map. The same run
logged `runprefix autodetect = "uwsm-app --"` — the launch prefix elephant
chose on this host.

**OBS** — provider docs summary (all from the generated file; each row is the
provider's purpose + the non-default-relevant fields):

| Provider | Purpose | Requirements / notable fields (doc anchors) |
|---|---|---|
| `calc` | calculate / unit-convert | needs `libqalculate` + `wl-clipboard`; `min_chars=3`, `require_number=true`, `async=true`, `autosave=false`, `command=wl-copy -n '%VALUE%'` |
| `clipboard` | clipboard history | `wl-clipboard` + `imagemagick`; `ignore_symbols=true`, `max_items=100`, `auto_cleanup=0`, `pinned_on_top=false` |
| `desktopapplications` | launch .desktop apps | history/pin/alias; `show_actions=false`, `only_search_title=false`, `window_integration=false`, `single_instance_apps=["discord"]` |
| `files` | find files/folders | needs `fd`; `search_dirs=$HOME`, `watch=false`, `fd_flags` ignored-vcs + type filters |
| `menus` | custom menus (TOML + Lua) | definitions in `~/.config/elephant/menus/`; `paths` extra roots; Lua API: `state()/setState()`, `lastMenuValue()`, `jsonEncode/Decodes`; `Cache`, `submenu = "dmenu:<name>"` |
| `providerlist` | lists providers/menus | `hidden=[]` |
| `runner` | run $PATH executables | `explicits[]` override list, `generic_text="run: "` |
| `symbols` | emoji/symbol search | `wl-clipboard`; `locale=en`, `command=wl-copy` |
| `todo` | todolist | `notify-send`; CSV in cache; schedule prefixes (`+5d >`, `in 10m >`, `jan 1 at 13:00 >`), `!` urgent |
| `unicode` | unicode search | `wl-clipboard`; locale |
| `websearch` | web search engines | `entries` default engine `google`; `engines_as_actions=true`, `always_show_default=true`, `command=xdg-open` |

**OBS** — the local elephant configs are three thin overrides:
`~/.config/elephant/calc.toml` = `async = false` (14 B, sha `2c0ef81b8edc9edf`);
`desktopapplications.toml` = `show_actions=false`, `only_search_title=true`,
`history=false` (62 B, sha `999b191512b29b68`);
`symbols.toml` = `command = 'wl-copy && hyprctl dispatch sendshortcut
"SHIFT,Insert,activewindow"'` (81 B, sha `9c0d5edf1fce95f3`) — i.e. the `:`
prefix copies the glyph **and** synthesises Shift+Insert into the active window.
No `elephant.toml`, no `websearch.toml`, no `files.toml`, no `runner.toml`,
no `todo.toml` ⇒ engine defaults apply.

**OBS** — menus: `~/.config/elephant/menus/` holds three Lua scripts (symlinks
into `~/.local/share/omarchy/default/elephant/`): `omarchy_themes.lua` (96 L,
sha `d997d5a4c27ffc10`, `Name="omarchythemes"`), `omarchy_background_selector.lua`
(73 L, sha `292c7deb0ddc0d00`, `Cache=false`, `SearchName=true`),
`omarchy_unlocks.lua` (92 L, sha `b577869246d8050f`, `FixedOrder=true`). All
three set `HideFromProviderlist = true` ⇒ the `providerlist` view is the 10
non-menu providers (INF; `hidden` in `providerlist.toml` is empty and the field
means exactly this per the generated docs).

### 4.2 Walker-side provider tables

**OBS** — `[providers]` (merged state here): `default =
["desktopapplications","websearch"]` (user `:18-21`), `empty =
["desktopapplications"]` (L1 `:59`), `max_results = 256` (user `:17`),
`ignore_preview = []`, `sets = {}`, `max_results_provider = {}`,
`argument_delimiter = {}` (L1 `:60-67`), `clipboard.time_format = "relative"`
(L1 `:109-110`).

**OBS** — `[providers.actions]` (L1 `:112-298`) is inherited untouched: the user
file declares no actions, so the packaged per-provider action/bind tables apply
verbatim (e.g. `desktopapplications`: Return=start, shift+Return=open+next,
ctrl+Return=new_instance; `files`: Return=open, ctrl+Return=open dir,
ctrl+c=copy file; `clipboard`: Return=copy, ctrl+d=remove …). The file's own
comment (`:112`) states the merge rule (§2.2).

**OBS** — walker's `[providers.actions]` also defines tables for providers whose
plugin is **not installed** on this host — dead tables, kept as evidence of the
upstream surface: `bluetooth` (plugin present but provider disabled),
`archlinuxpkgs`, `dnfpackages`, `aptpackages`, `1password`, `protonpass`,
`bitwarden`, `nirisessions`, `wireplumber`, `playerctl`, `niriactions`,
`bookmarks`, `windows`. None of these can produce results here.

### 4.3 Prefix routing (the live map)

| Prefix | User route (`:23-45`) | Packaged route (`:69-107`) | Provider present here? |
|---|---|---|---|
| `/` | `providerlist` | `files` | yes (providerlist) |
| `.` | `files` | `symbols` | yes (files) |
| `:` | `symbols` | `clipboard` | yes (symbols) |
| `=` | `calc` | `calc` | yes |
| `@` | `websearch` | `websearch` | yes |
| `$` | `clipboard` | `windows` | yes (clipboard) |
| `;` | — | `providerlist` | unused locally |
| `>` | — | `runner` | plugin present, no local route |
| `!` | — | `todo` | plugin present, no local route |
| `%` | — | `bookmarks` | **no plugin** |

**INF** — because arrays replace (§2.2), the four packaged-only routes
(`;`, `>`, `!`, `%`) do not exist at runtime here; `runner`, `todo`, `unicode`
have no user prefix either, so locally they are reachable only through the
`/` providerlist (or `-m`). **OBS** — `menus:` providers are reached by name
(`walker -m menus:omarchythemes`, `omarchy-menu:298`) or by selecting a menu
row; `global_argument_delimiter = "#"` (L1 `:7`) makes the tail of a query
after `#` an argument rather than search text (file comment: "firefox#https://
benz.dev ⇒ part after delimiter will be ignored when querying"). **OBS/finding**
— the same comment says "this should be the same as in the elephant config",
but the elephant docs generated by `elephant generate doc` (this version)
expose **no** delimiter field at engine or provider level (`grep -i delimiter`
→ 0 hits in the 644-line doc). The exact elephant-side counterpart is **UNK**;
walker-side the key is `#` unless overridden (it is not).

### 4.4 Provider → item layout (files shipped)

**OBS** — `/etc/xdg/walker/themes/default/` ships per-provider item templates:
`item.xml` (generic) plus `item_archlinuxpkgs.xml`, `item_calc.xml`,
`item_clipboard.xml`, `item_dmenu.xml`, `item_dnfpackages.xml`,
`item_files.xml`, `item_providerlist.xml`, `item_symbols.xml`,
`item_symbols_grid.xml`, `item_todo.xml`, `item_unicode.xml`, and the adjuncts
`keybind.xml`, `layout.xml`, `preview.xml`, `style.css`. **OBS** — the grid
variant differs from the list variant structurally: `item_symbols.xml` is a
horizontal `ItemBox` (glyph label + text box + `QuickActivation` label),
`item_symbols_grid.xml` is a vertical `ItemBox` (glyph image above centered,
wrapping text, no quick-activation). **INF** — providers without a dedicated
template (`desktopapplications`, `websearch`, `runner`, `menus`, `bluetooth`)
fall back to the generic `item.xml`; providers with no template here cannot
render a custom row. The omarchy theme ships **no** item templates (§6.2), so
its rows depend on the fallback path — see §6.3.

---

## §5 CLI surface (both binaries)

**OBS** — `walker --help` (full flag list, measured):

| Flag | Meaning (help text) |
|---|---|
| `-v/--version` | print version |
| `-n/--nosearch` | hide search input |
| `-N/--nohints` | hide keybind hints |
| `-I/--inputonly` | only show input (dmenu only) |
| `-x/--password` | password input; sets dmenu automatically |
| `-X/--selectsingle` | auto-select single entry |
| `-i/--index` | print selected index instead of value (dmenu only) |
| `-m/--provider` | exclusive provider to query |
| `-s/--set` | provider set to use (`[providers.sets]`; "can't find specified set" otherwise) |
| `-p/--placeholder` | input placeholder |
| `-h/--height`, `--minheight`, `--maxheight` | overall box height / scrolled-content bounds (min 1) |
| `-c/--current` | mark current value (dmenu only) |
| `-w/--width`, `--minwidth`, `--maxwidth` | width / content bounds |
| `-t/--theme` | theme override |
| `-d/--dmenu` | dmenu mode |
| `-q/--close` | close walker when open |
| `-H/--hideqa` | hide quick-activation buttons |
| `-k/--keepopen` | keep open after selection (service, dmenu only) |
| `-e/--exit` | exit after this dmenu call (service, dmenu only) |

**OBS** — `elephant` CLI subcommands (`elephant --help`): `service` (manage the
user systemd service), `version`, `listproviders`, `menu` (send request to open
a menu), `generate doc|config`, `query`, `state`, `community`, `activate`,
`help`. `query`/`state` take a content argument and are the supported
**read** path into the daemon over `elephant.sock` — neither was exercised here
beyond `listproviders` (§11).

**OBS** — the omarchy-facing invocations on this host:
`omarchy-launch-walker:14` → `exec walker --width 644 --maxheight 300
--minheight 300 "$@"` (and `:5-12` starts elephant + the walker service if
absent, the service with `env GSK_RENDERER=cairo` at `:11`);
`omarchy-menu:21-22` closes an open dmenu with `walker --close`;
`omarchy-menu:43` pipes its options through
`omarchy-launch-walker --dmenu --width 295 --minheight 1 --maxheight 630 -p
"…"`; `omarchy-menu:269/298/302` open the three elephant menus with
`-m menus:… --width 800 --minheight 400`; `omarchy-menu:857` opens plain
`walker -p "Launch…"`.

---

## §6 Theme & layout resolution end-to-end

### 6.1 The chain

**OBS** — `theme = "omarchy-default"` (user `:3`) +
`additional_theme_location = "~/.local/share/omarchy/default/walker/themes/"`
(user `:4`). That directory holds exactly one theme dir, `omarchy-default/`
(`layout.xml` 6,488 B sha `dbb6bbbe74be894a`; `style.css` 1,243 B sha
`481267af0e89a475`). **OBS** — `~/.config/walker/` has no `themes/` subdir, so
the search roots in play are the additional location plus whatever the binary
carries internally (`theme not found. using default theme.` /
`default theme not found` / `… not found. falling back to default` — three
distinct fallback message tokens in `/usr/bin/walker`).

### 6.2 The two theme documents

**OBS** — `layout.xml` defines the whole window by **object ids**; the binary's
parser errors name every id it requires (`missing 'Window'/'Scroll'/'List'/
'ElephantHint'/'Error'/'BoxWrapper'/'ContentContainer'/'Keybinds'/
'GlobalKeybinds'/'ItemKeybinds' object`, `Theme: missing 'Keybind' object`).
The omarchy `layout.xml` supplies all of them (156 L): `GtkWindow#Window` →
`BoxWrapper` (width-request **644**, the flag-matched width) → vertical `Box`
(spacing 10) → `SearchContainer/Input` → `ContentContainer` with
`ElephantHint` ("Waiting for elephant..."), `Placeholder` ("No Results"),
`Scroll` (`max-content-width 600`, `max-content-height 300` → the launch
`--maxheight 300`) → `GtkGridView#List` (`max_columns 1`) + `Preview`, then the
`Keybinds` box (`GlobalKeybinds`, `ItemKeybinds`) and a hidden `Error` label.
**OBS** — diff vs the packaged default layout: omarchy sets `BoxWrapper`
`width-request` **644** where the packaged layout uses **600** on the same
object (and puts `height-request 570` there), drops the `min_columns` property
on `List`, sets the scroll bounds to 600/300 (packaged 500/400), and
re-arranges the ElephantHint/Placeholder properties — same object graph,
different tuning.

**OBS** — `style.css:1` of the omarchy theme is
`@import "../../../../../../../.config/omarchy/current/theme/walker.css";` —
a relative climb into the **generated theme file**, which the same second
(2026-10-03 17:49:02) was produced by omarchy. That file is 6 `@define-color`
lines (sha `f44cb45063494d2f`): `selected-text #e68e0d`, `text/base/border/
foreground #bebebe`, `background #121212`. **OBS** — the values come from
`~/.config/omarchy/current/theme/colors.toml` (`accent = "#e68e0d"`,
`foreground = "#bebebe"`, `background = "#121212"`) rendered through
`~/.local/share/omarchy/default/themed/walker.css.tpl` by
`omarchy-theme-set-templates:38-46` (sed-driven `{{ key }}` substitution),
which `omarchy-theme-set:38` calls before swapping `next-theme` →
`current/theme` (`:41-42`). **This resolves round-1 unknown U7 for the walker
axis**: theme changes rewrite walker.css via the template pipeline, not via a
hook — `~/.config/omarchy/hooks/theme-set.d/` contains only
`show-theme-notification.sample` (270 B, sample suffix).

### 6.3 Missing theme parts: what is measurable

**OBS** — the omarchy theme ships **no** `item_*.xml`, `keybind.xml` or
`preview.xml`; the packaged default theme ships all of them (§4.4). The binary
carries: a `Theme`/`Actions/Menu/Dmenu/Emergency/layout/keybind/preview/css/
items/grid_items` token run, the embedded default-theme XML fragments, the
per-part error strings (`failed to get item layout: `,
`failed to get item grid layout: `, `failed to get item layout`,
`failed to get item grid layout`, `Couldn't initialize providers.`), and the
three theme-fallback messages above.
**INF (high)** — a theme directory may supply a subset of parts; missing parts
resolve against the built-in default theme (the same document as the L1 files,
§2.1), which is why the omarchy theme — live on thousands of installs — needs
no item templates. The exact lookup order (user theme → additional_theme_
location → built-in default per part, vs all-or-default for the whole theme)
was **not** measured; opening the launcher would map a layer surface and is
outside this lane's remit ⇒ **UNK**, with the error tokens pinned as the
readable surface to watch in a future probe. Note the omarchy user config
forces `[columns] symbols = 1` (a one-column grid), so the grid item path is
the one exercised by the `:` prefix here.

**OBS** — `GSK_RENDERER=cairo` in `omarchy-launch-walker:11` is the only
renderer-environment intervention in the launch path (no walker or elephant
unit sets it, §1).

---

## §7 Runtime, lifecycle, emergencies

### 7.1 Launch

**OBS** — binds (live `hyprctl -j binds`): modmask 64 + SPACE →
`omarchy-launch-walker`; modmask 68 (= SUPER+ALT) + E →
`omarchy-launch-walker -m symbols`; modmask 68 + V →
`omarchy-launch-walker -m clipboard`. `omarchy menu keybindings --print`
renders `SUPER + SPACE → Launch apps` (`:5`). This re-verifies round-1 §8 U1 /
R2-E2 on the new session.

### 7.2 Restart / refresh

**OBS** — `omarchy-restart-walker:5-15`: restarts `elephant.service` when
enabled, then `app-walker@autostart.service` (else prints `Unable to restart
Walker -- RESTART MANUALLY`); as root it re-enters as the owning user via
`systemd-run` (`:17-23`).
**OBS** — `omarchy-refresh-walker` is the reset path: re-copies
`walker.desktop` → `~/.config/autostart/` (`:5-6`), the `restart.conf` drop-in
(`:9-10`), `daemon-reload` (`:12`), then `omarchy-refresh-config
walker/config.toml` + `elephant/calc.toml` + `elephant/desktopapplications.toml`
(`:15-17`), re-links all `default/elephant/*.lua` menus (`:19-23`), and restarts
(`:26`). **OBS/finding** — the refresh list **omits `elephant/symbols.toml`**
although the stock set (`~/.local/share/omarchy/config/elephant/`) contains it;
the omitted file is exactly the one carrying the `:`-prefix Shift+Insert
customisation (§4.1), so a refresh leaves that behaviour intact while resetting
the other two. Intent unknown; recorded as measured asymmetry.
**OBS** — `omarchy-menu:468` and `:805` expose `~/.config/walker/config.toml`
for editing and `omarchy-refresh-walker` for reset; `:790` restarts walker.

### 7.3 Menu integration

**OBS** — the Omarchy Menu is a *walker client*, not a separate UI
(`omarchy-menu:43` dmenu pipe; `:21-22` `walker --close`; `:269/298/302` the
elephant menus). The bar's left button reaches it via `omarchy-menu`
(round-1 §2.2 anchor), so the bar→launcher path is bar → omarchy-menu → walker
dmenu, while the keyboard path is direct (§7.1).

### 7.4 Emergencies

**OBS** — the user's file declares one `[[emergencies]]` row (`:47-49`, text
`Restart Walker`, command `omarchy-restart-walker`); the packaged file declares
none. **OBS** — the binary's tokens: `struct EmergencyEntry with 2 elements`,
`failed to run emergency command`, `is_emergency` (app-state flag),
`menus-emergency` (part token), `Emergency` (theme part name). **INF** — it is
a fail-safe row rendered through a dedicated theme part, with the command run
on activation. **UNK** — the trigger condition (round-3 §9 U6 stands): no
message or documentation ties it to a state such as "elephant absent" vs
"no results"; not measurable without exercising the launcher.

---

## §8 Round-1/round-3 open unknowns — resolution ledger

| Unknown (source) | Status this pass | Evidence |
|---|---|---|
| R1 §8 U1 — which stock binding launches Walker | **resolved** (R2-E2) and re-verified on the new session | `hyprctl -j binds` modmask 64 SPACE; `omarchy menu keybindings --print:5` |
| R1 §8 U4 — `$OMARCHY_PATH` in the waybar process | still **UNK** for the bar (`/proc` barred); new datum: walker/elephant units declare no `Environment` and no `EnvironmentFile` | `systemctl --user show -p Environment` |
| R1 §8 U7 — do theme-set hooks rewrite themed files | **resolved** (walker + waybar axes): `omarchy-theme-set:38` → `omarchy-theme-set-templates` renders `default/themed/*.tpl` (incl. `walker.css.tpl`, `waybar.css.tpl`) into `current/theme/`; hooks dir holds only `show-theme-notification.sample` | `omarchy-theme-set:12-45`, `omarchy-theme-set-templates:6-46`, hooks listing |
| R1 §8 U2/U3/U5/U6 (swayosd key, weather value, config.jsonc.bak writer, lock e2e) | out of this note's scope; untouched | — |
| R3 §9 U6 — emergencies trigger | sharpened, still **UNK** (§7.4) | struct/error tokens |
| R3 §9 U7 — walker/elephant socket protocols | still **UNK** (sockets untouched); new: the documented read path is the `elephant` CLI (`listproviders`, `query`, `state`), of which `listproviders` was used once | `elephant --help`; RUN |
| R3 §9 U8 / §6.6 — item-layout + theme resolution order | sharpened (§6.3): part set + fallback tokens + missing-parts fact pinned; order still **UNK** | `/etc/xdg/walker/themes/default/` listing; strings |

**Candidate additions (not errata — no earlier claim is contradicted):** the
R1 §8 U7 answer above; the elephant-side `bluetooth`-disabled fact (plugin
present, provider not loaded); the `omarchy-refresh-walker` omission of
`symbols.toml`; the walker comment's elephant-delimiter counterpart missing
from this version's generated docs (§4.3). These belong to future append-only
errata blocks only if a note asserts otherwise; none does.

---

## §9 Decision table (walker-specific, falsifiable)

| Situation | Action | Why (anchor) |
|---|---|---|
| Change a walker setting | edit `~/.config/walker/config.toml`, then `omarchy restart walker` | config is read at process start; no reload verb exists in `walker --help` |
| Reset walker to omarchy stock | `omarchy refresh walker` — today lossless (user file = stock, `diff` clean) | `omarchy-refresh-walker:15-17`; §1 hashes |
| Add a prefix route | append `[[providers.prefixes]]` with `prefix`/`provider`; remember the array replaces the packaged ten | §2.2 INF + packaged `:69-107` |
| Provider returns nothing | check elephant first: `elephant listproviders`, plugin in `/usr/lib/elephant/`, provider config in `~/.config/elephant/` | §4.1; disabled bluetooth evidence |
| `:` copies but does not paste | by design — symbols command copies and synthesises Shift+Insert via `hyprctl` | `~/.config/elephant/symbols.toml` (81 B) |
| Menu rows missing from providerlist | the three omarchy menus set `HideFromProviderlist=true`; reach them by name (`-m menus:…`) | lua heads; `omarchy-menu:269/298/302` |
| Launcher colours wrong after theme change | check `~/.config/omarchy/current/theme/walker.css` (generated from `walker.css.tpl`), re-run `omarchy theme set <name>` | §6.2 pipeline |
| Walker window silently falls back to default look | theme name/dir resolution failed — look for `theme not found. using default theme.` in walker's output | binary messages §6.1/§6.3 |

## §10 Introspection ledger

| Question | Surface | Verdict |
|---|---|---|
| Is walker running, how? | `ps`, `systemctl --user cat/show`, pgrep | **OBS** |
| Is it open / where? | `hyprctl -j layers` | **OBS** (closed: only wallpaper/waybar) |
| D-Bus identity / actions? | `busctl --user list` (`dev.benz.walker`) | **OBS**; `org.gtk.Actions.List` empty (round 3) |
| What config does it read? | the two files + embedded default (§2) | **OBS** |
| What providers exist? | `elephant listproviders`, plugin dir, generated docs | **OBS/RUN** |
| What does it *render*? | none read-only — no screenshot, no layer surface; UI not opened | **UNK** |
| Sockets protocol? | `walker.sock` / `elephant.sock` | **UNK** (untouched; elephant CLI is the documented read path) |

## §11 Unknowns (open, not filled by inference)

1. Item-layout/theme part resolution order for partial themes (§6.3).
2. Emergency trigger condition (§7.4).
3. `walker.sock` protocol and any query API (only `elephant`'s CLI was used;
   the walker socket is undocumented locally).
4. `installed_providers` semantics (§2.3).
5. `WALKER_` env-override surface (§2.1 L3).
6. Unknown-key/parse-error behaviour (§3).
7. `~` expansion inside `additional_theme_location` (§2.4).
8. Elephant-side counterpart of `global_argument_delimiter` (§4.3).
9. Rendered walker pixels under the omarchy theme — no screen read this pass.
10. `[providers.sets]` behaviour with a real set (`-s` path) — none defined.

## §12 Rejections (kept)

- *"The user file's `[columns] symbols` comment describes provider default
  queries"* — rejected before (R4-E3); the deep pass adds no support: the
  packaged counterpart is keyed by provider name and the grid item template
  `item_symbols_grid.xml` exists. Kept so the wrong comment is not re-learned.
- *"`walker` parses SCSS themes"* — rejected as unsupported: the `style.scss`
  token appears once in the binary next to `style.css`, but no theme on this
  host ships SCSS and no other evidence of a Sass pipeline exists. The token
  alone does not make it a feature; if it is one it was not measurable here.
- *"The packaged prefixes stay active"* — rejected: merging would produce two
  routes for `.` and `=`, and the shipped omarchy config is byte-identical to
  the stock copy (§2.2) — the array-replace INF keeps this as a working rule
  until a live probe contradicts it.

## §13 Method, boundary proof, and the one probe outlier

- Probes used (all read-only): `wc`, `stat`, `sha256sum`, `cat`, `diff`,
  `grep`, `strings`, `sed`, `ps`, `pgrep`, `busctl --user list`,
  `hyprctl -j binds/layers/instances`, `systemctl --user cat/show/is-active`,
  `walker --version/--help`, `elephant version/--help/listproviders/… --help`,
  `elephant generate doc` (stdout only), `omarchy version`, `omarchy menu
  keybindings --print`, `git describe` (no fetch), `pacman -Q/-Ql/-Qi`,
  `python3` for byte-slice comparison and codepoint extraction.
- **Executed only when pure-read**: the CLI reads above. The walker UI was
  never opened; no compositor state was touched; sockets never connected.
- **Outlier (recorded for honesty)**: one bare `elephant` invocation was made
  while probing the CLI before its help was read; it printed startup INFO
  (config default, `runprefix autodetect = "uwsm-app --"`, provider loads) and
  exited. Before/after checks: service `MainPID` still 1203474, only one
  `elephant` process, both sockets unchanged (mtime 13:11:09), no file in
  `~/.cache/elephant` or `~/.config/elephant` modified after 13:11
  (`find -newermt '2026-10-14 13:50'` empty). No state change measurable; the
  line is kept because the run's log lines are cited in §4.1.
- **Boundary proof** — same values measured at the start and end of the pass:

| File | sha256[:16] | Size |
|---|---|---|
| `~/.config/walker/config.toml` | `fecf71fa4253803e` | 1,336 B |
| `~/.local/share/omarchy/config/walker/config.toml` | `fecf71fa4253803e` | 1,336 B |
| `/etc/xdg/walker/config.toml` | `5b4e47b7d2314bf8` | 13,220 B |
| `~/.local/share/omarchy/default/walker/themes/omarchy-default/layout.xml` | `dbb6bbbe74be894a` | 6,488 B |
| `~/.local/share/omarchy/default/walker/themes/omarchy-default/style.css` | `481267af0e89a475` | 1,243 B |
| `~/.config/omarchy/current/theme/walker.css` | `f44cb45063494d2f` | 191 B |
| `~/.config/elephant/{calc,desktopapplications,symbols}.toml` | `2c0ef81b8edc9edf` / `999b191512b29b68` / `9c0d5edf1fce95f3` | 14/62/81 B |
| sockets | `walker.sock`/`elephant.sock` mtime 13:11:09, size 0 | — |

- mtimes unchanged (`config.toml` 2026-10-03 17:44:32; packaged file
  2026-07-26 21:42:11) — nothing was written into any substrate tree.
- Scratch: `/tmp/w5-m5-3-probe/` — `walker.strings` (17,581 L),
  `allprov-docs.md` (644 L), `cfg/` (empty; a `generate config` probe wrote
  nothing anywhere), plus the python slices. Ephemeral.

## §14 Reproducible spot-checks

1. Embedded default == packaged file:
   `python3 -c "b=open('/usr/bin/walker','rb').read(); f=open('/etc/xdg/walker/config.toml','rb').read(); i=b.find(b'force_keyboard_focus = false'); print(i, b[i:i+len(f)]==f)"`
   → `784064 True`.
2. Struct arity / key universe:
   `strings -n 6 /usr/bin/walker | grep -o 'struct [A-Za-z]* with [0-9]* elements'`
   → includes `struct Walker with 29 elements`, `struct Keybinds with 13 elements`.
3. Provider census: `elephant listproviders` → the 13 names of §4.1;
   `ls /usr/lib/elephant/` → the 12 plugin files.
4. Theme pipe: `head -1 ~/.local/share/omarchy/default/walker/themes/
   omarchy-default/style.css` → the relative `@import` of
   `~/.config/omarchy/current/theme/walker.css`; `grep -n 'theme-set-templates'
   ~/.local/share/omarchy/bin/omarchy-theme-set` → `38`.

## Errata (append-only)

_None yet. New entries append below this line; earlier text is never edited —
a correction is a new block citing the block it corrects._

## Freshness pointer (round 19, 2026-10-20)

- The walker version pins in this note (line 27) are dated 2026-10-14 (the note's own measurement date, lines 3-4) and describe walker 2.17.0. On 2026-10-20 the host package moved to 2.17.2: `/var/log/pacman.log:2929` ([ref]) and the binary's compiled-in version literal `2.17.2`, read as file bytes (S096). Current routing: corpus/knowledge/walker-route-r18.md.
- Version-bound, dated 2026-10-14 and not re-run on 2.17.2: the `walker --help` flag table (§5), the embedded-default byte run at offset 784,064 (§2.1), struct/field-arity and error/fallback token strings (§2.2-2.3, §6.1, §6.3), and every `/etc/xdg/walker/config.toml` line anchor (§2.1-2.4, §4.2, §7.4). The note's L1 pin (298 L, 13,220 B, sha256 prefix 5b4e47b7d2314bf8) is superseded: the host file now reads 13,743 B, sha256 prefix 3c5c6867d0216d0c ([ref]; upstream v2.17.2 default [ref]; DeltaWalkerConfig w1 round 19: 2.17.1 added `blur_corner_radius`, the `[niri]` table, a desktopapplications edit action and changed clipboard `after` to `SimpleDelete`, so §2.1-2.4 key enumerations are incomplete for 2.17.2).
- Elephant-bound, dated 2026-10-14: `elephant version` 2.21.0 (line 28), the `listproviders` census and plugin list (§4.1), ElephantConfig defaults and generated-doc counts (§4.1, §5). [ref] (line 3095) records elephant 2.21.0-1 -> 2.22.1-1 on this host; not re-measured.
- Not walker-version-bound, still dated 2026-10-14: user files and hashes (only `~/.config/walker/config.toml` fecf71fa4253803e, 1,336 B was re-read this round, unchanged), elephant user TOMLs and menu Lua hashes, theme file hashes, omarchy script line anchors (§5, §7), and process/session state (§1 PIDs 1203471 and 1203474, sockets, `hyprctl -j layers`, §7.1 binds). [INFERENCE] a PID from 2026-10-14 runs the pre-upgrade image; not checked.
- Not re-measured live this round (host pause): behaviour of the 2.17.2 binary stays [UNK].

### Wave-2 corrections (round 19, append-only)

- Three items the block calls "not re-run on 2.17.2" were re-read this round as file bytes: the embedded default run (now at offset 806,960, byte-equal to `/etc/xdg/walker/config.toml`, [ref]), the `struct Walker` arity (31 elements in the 2.17.2 binary, w1 DeltaWalkerConfig) and the `/etc/xdg` line anchors (shifted +6/+7, map in w1 DeltaWalkerConfig). Error/fallback tokens were not re-read.
- The `--help` option text is byte-identical between 2.17.0 and 2.17.2 (838-byte run, w1 DeltaWalkerCli); only the GLib framing is host-library-bound. ElephantConfig defaults and generated-doc counts live in §4.1, not §5.
- Further delta sites (w2 ReviewDeltaCarry): §3 lines 162-164 list six `after` values; the 2.17.2 default adds `SimpleDelete` (seven). Line anchors outside §2.1-2.4/§4.2/§7.4 (§3, §4.3, §9) shifted +6/+7 as well.

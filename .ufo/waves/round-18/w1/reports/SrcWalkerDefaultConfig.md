# SrcWalkerDefaultConfig — walker 2.17.2 shipped default config (P3 upstream, P5 theme-key edge)

Seat: `MadoR18.SrcWalkerDefaultConfig` (scout, leaf). Question: at walker's 2.17.2 tag, fetch the
shipped default config with a fetch receipt; record sha256 and ≤25-word quotes on providers/prefixes,
theme selection, keybinds.

Axes kept: (1) provenance integrity — every byte traceable to a tag and a committed raw body;
(2) config-surface completeness — provider set, prefix map, theme key, keybind map all anchored;
(3) host-projection risk — keep tagged-source declarations separate from host declarations and from
runtime behaviour (all runtime stays `[UNK]`).

## Provenance (observed)

| item | value |
|---|---|
| tag | `refs/tags/v2.17.2` (lightweight: `git ls-remote` printed no `^{}` line) |
| tag → commit | `a515085fd39fae80acc086c8fbfd9b7771a9a11d` |
| commit date | 2026-10-08T06:45:24Z; message `fix: GTK 4.24 blur handling causing crash` |
| release | `v2.17.2`, `target_commitish: master`, published 2026-10-08T06:49:30Z; one asset `walker-v2.17.2-x86_64-unknown-linux-gnu.tar.gz` (2,772,997 B, not fetched — >1 MiB rule) |
| config path in tree | `resources/config.toml` (GitHub tree API at `v2.17.2`, `truncated: false`, 92 entries; blob `997f6548fc633ab7e00210623a69d425d30bd7e3`) — the only `config.toml` in the tagged tree |
| raw body | 305 lines, 13,743 B, sha256 `3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b` |
| blob cross-check | `git hash-object` of the fetched body = `997f6548fc633ab7e00210623a69d425d30bd7e3` = the tagged tree blob → raw body is byte-identical to the tag's `resources/config.toml` |

"Shipped" caveat: the tagged repo file is described by the tag's README:215 as "the default config"
(link target is `refs/heads/master`, not the tag). The installed Arch package carries no config file:
`find /usr -maxdepth 5` (docs pruned) yields only `/usr/bin/walker` and `/usr/share/licenses/walker/LICENSE`.
Whether the binary embeds this file or compiles defaults is not observable by file read → `[UNK]`.

## Fetch receipts (R17-V3)

All under `.ufo/waves/round-18/fetch/SrcWalkerDefaultConfig/`, one JSON line each in `receipts.jsonl`
(schema `mado-fetch-receipt-v1`, tool `curl 8.23.0 (x86_64-pc-linux-gnu) libcurl/8.23.0 …`,
all HTTP 200, fetched 2026-10-20T15:40–15:41Z).

| body | URL | bytes | sha256 |
|---|---|---|---|
| `walker-v2.17.2-config.toml` | https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/resources/config.toml | 13743 | `3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b` |
| `walker-v2.17.2-README.md` | https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/README.md | 7926 | `9755f955d5c4e460ac8538e1b648ba2a3c86da37ceaa4d0655dca4d1ea3d2456` |
| `walker-v2.17.2-theme-default-keybind.xml` | https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/resources/themes/default/keybind.xml | 869 | `1233d0b1a258dc1991fc7ad3abe764c40903e241312e994a3a17a75c985c13b7` |
| `walker-v2.17.2-tree.json` | https://api.github.com/repos/abenz1267/walker/git/trees/v2.17.2?recursive=1 | 26501 | `4eef2da714db803da04e03e94bb355eb56ddc9c033aba91572047e52dd5126f0` |
| `walker-v2.17.2-release.json` | https://api.github.com/repos/abenz1267/walker/releases/tags/v2.17.2 | 4305 | `30e642b0d6bcd2290f2a67eee2c2806ea63d48f56a46b8ca3dd83814fc895e56` |
| `walker-v2.17.2-commit.json` | https://api.github.com/repos/abenz1267/walker/commits/v2.17.2 | 9315 | `4767b7522364edb3b70f4ab4d25b88c2f223c4acc7155ef1fdaaaf03ce5e964b` |

Method exception, recorded: one transient commit-metadata read used Python `urllib` (first 400 bytes only,
no claim depends on it); the committed receipt above is the later curl fetch of the same URL.

## Findings — tagged default config (`resources/config.toml`, code, tier A)

### 1. Providers (`[providers]`, :58-67)

Verbatim :59-64 (default set; `runner` present but commented at :62):

```
default = [
  "desktopapplications",
  "calc",
  # "runner",
  "websearch",
] # providers to be queried by default
```

- :65 `empty = ["desktopapplications"] # providers to be queried when query is empty`
- :66 `ignore_preview = [] # providers that should not show previews`
- :67 `max_results = 50 # global max results`
- :7 (25 words) `global_argument_delimiter = "#"    # query: firefox#https://benz.dev => part after delimiter will be ignored when querying. this should be the same as in the elephant config`
  → the tagged config names **walker** (repo) and **elephant** (backend) in the source/scope sense.
- :8 `exact_search_prefix = "'"          # disable fuzzy searching`
- README:13-34: "The following Elephant providers are implemented by default:" — the provider names
  above are elephant-provided; default-config values do not prove any provider is installed or reachable.

### 2. Prefix map (`[[providers.prefixes]]`, :75-113, ten rows)

| line | prefix | provider | line | prefix | provider |
|---|---|---|---|---|---|
| :75-77 | `;` | `providerlist` | :95-97 | `%` | `bookmarks` |
| :79-81 | `>` | `runner` | :99-101 | `=` | `calc` |
| :83-85 | `/` | `files` | :103-105 | `@` | `websearch` |
| :87-89 | `.` | `symbols` | :107-109 | `:` | `clipboard` |
| :91-93 | `!` | `todo` | :111-113 | `$` | `windows` |

Verbatim pairs (≤25 words each): :76-77 `prefix = ";"` / `provider = "providerlist"`;
:108-109 `prefix = ":"` / `provider = "clipboard"`. README:16-22 independently names `=` calc,
`/` files, `:` clipboard, `.` symbols, `;` providerlist — config and README agree at the tag.

### 3. Theme selection

- config :9 `theme = "default"                  # theme to use` (7 words).
- config :17 `keybind_symbols = true             # render keybind hints with key symbols (e.g. ⌃+⏎) instead of plain text ("ctrl Return")`.
- README:219 (21 words): “Themes inherit the default theme by default, so if you just want to change the CSS, you can just create `themes/yours/style.css`.”
- README:225 (13 words): “You can set the default theme in your `config.toml` f.e. `theme = "yours"`.”
- Tagged default theme inventory (`resources/themes/default/`): `style.css`, `layout.xml`,
  `keybind.xml`, `preview.xml`, `item*.xml` (19 files total in tree). `keybind.xml` (869 B,
  sha256 `1233d0b1…`) is a GTK widget template (`GtkBox id="Keybind"`, `GtkButton id="KeybindButton"`,
  labels `KeybindLabel`/`KeybindBind`) — it renders keybind hints; it carries no bind map.
- Wallpaper/wallpaper-engine negative: the config's only `background` token is :21
  `ext_background_effect_blur = false # request the compositor to blur behind the box-wrapper via ext-background-effect-v1 (compositor must support it)`;
  no `swaybg`/`wallpaper` token in config or README at the tag. Theme here means Walker's GTK theme,
  not a wallpaper theme.

### 4. Keybinds (`[keybinds]`, :43-56)

Verbatim singles (≤25 words each): :53 `quick_activate = ["F1", "F2", "F3", "F4"]`;
:56 `show_actions = ["alt j"]`; :11 `debug = false                      # enables debug printing for some stuff, f.e. keybinds`.

Full map as declared at :44-55 (derived table, values verbatim in the body):

| action | keys | action | keys |
|---|---|---|---|
| `close` | `Escape` | `toggle_exact` | `ctrl e` |
| `next` | `Down` | `resume_last_query` | `ctrl r` |
| `previous` | `Up` | `quick_activate` | `F1`,`F2`,`F3`,`F4` |
| `left` | `Left` | `page_down` | `Page_Down` |
| `right` | `Right` | `page_up` | `Page_Up` |
| `down` | `Down` | `show_actions` | `alt j` |
| `up` | `Up` | | |

- `[keybinds]` carries no `Return`/`shift Return` map: activation binds are per-provider under
  `[providers.actions]` (:118+), e.g. `desktopapplications` :165-175 `start`/`new_instance`,
  `clipboard` :248-262 `copy`, `providerlist` :128-130 `activate` (all `bind = "Return"` variants).
  A route note must not claim the [keybinds] table includes Return.
- README:203-209: `## Keybinds`; (10 words) "The following modifier keys are valid: `ctrl`, `alt`,
  `shift`, `super`."; (16 words) "F.e. `pub const GDK_KEY_semicolon: c_int = 59;` means that
  `ctrl semicolon` would be a valid keybind."
- `hide_action_hints`, `hide_return_action`, `hide_quick_activation`, `keybind_symbols` (:13-17)
  gate hint rendering only; no runtime effect read.

## Host declaration delta (file bytes, not runtime; adjacent to `HostWalkerFiles`/`SrcOmarchyWalker`)

`~/.config/walker/config.toml` = 1336 B, sha256 `fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787`;
byte-identical to `~/.local/share/omarchy/config/walker/config.toml` (same sha256). Declared there:

- :3 `theme = "omarchy-default"                                                   # theme to use` (7 words);
- :4 `additional_theme_location = "~/.local/share/omarchy/default/walker/themes/"` (3 words) —
  this key does **not** appear in the tag's default config or README → its 2.17.2 semantics are `[UNK]`;
- :10-11 `[keybinds]` `quick_activate = []` (disables upstream F1-F4 quick activation);
- :16-19 `[providers]` `max_results = 256`, `default = ["desktopapplications","websearch"]`;
- :21-42 six prefixes: `/` providerlist, `.` files, `:` symbols, `=` calc, `@` websearch, `$` clipboard;
- :44-46 `[emergencies]` text "Restart Walker", command "omarchy-restart-walker".

Declared prefix drift vs upstream tag (declaration-level only; no runtime claim):
`:` = symbols on host vs clipboard upstream; `.` = files vs symbols; `/` = providerlist vs files;
`$` = clipboard vs windows; `; > ! %` not declared on host. Host theme dir
`~/.local/share/omarchy/default/walker/themes/omarchy-default/` holds only `layout.xml` (6488 B) and
`style.css` (1243 B); README:219's inheritance sentence is the only basis for it borrowing the default
theme's `keybind.xml` → `[INFERENCE]`, not observed.

Host versions, read from `/var/log/pacman.log` bytes only: `:2929` `upgraded walker (2.17.0-1 -> 2.17.2-1)`
(2026-10-20T09:16:46-0300); `:3095` `upgraded elephant (2.21.0-1 -> 2.22.1-1)` (2026-10-20T09:31:03-0300).
Tagged source never proves the host binary's behaviour.

## Candidate SOURCES rows (11-column shape; L1 assigns S0xx)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0xx-pending | walker `resources/config.toml` @ v2.17.2 — https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/resources/config.toml | code | A | walker 2.17.2 tagged default config surface; names walker and its elephant backend (`:7`); default provider set, prefix→provider map, theme key, keybind map | whole file 305 lines / 13743 B, sha256 `3c5c6867…`; tag v2.17.2→`a515085f…`; git blob `997f6548…`; `:7`, `:9`, `:17`, `:43-56`, `:58-67`, `:75-113`, `:118+` | default providers desktopapplications/calc/websearch (`runner` commented `:62`), `empty`=desktopapplications, `max_results=50`; ten prefixes `; > / . ! % = @ : $`; `theme="default"`; keybinds Escape/Down/Up/Left/Right/`ctrl e`/`ctrl r`/F1-F4/Page_Down/Page_Up/`alt j`; Return binds live per-provider in `[providers.actions]` | mined | 2026-10-20 | on-release | corpus/knowledge/walker-route-r18.md |
| S0yy-pending | walker `README.md` @ v2.17.2 — https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/README.md | docs | A | walker config/theme/keybind documentation at tag: config directory, default-config pointer, theme inheritance, keybind value domain | file lines 203-225; sha256 `9755f955…`; tag commit `a515085f…` | "Configuration should be done in `~/.config/walker`"; default config = `resources/config.toml` (link says master, not tag); themes inherit the default theme; theme set in config.toml; modifiers ctrl/alt/shift/super; keys are GDK key values | mined | 2026-10-20 | on-release | corpus/knowledge/walker-route-r18.md |
| S0zz-pending | walker `resources/themes/default/keybind.xml` @ v2.17.2 — https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/resources/themes/default/keybind.xml | code | A | default theme's keybind-hint widget template (GTK4) | 869 B, sha256 `1233d0b1…`; tag commit `a515085f…`; object ids `Keybind`, `KeybindButton`, `KeybindLabel`, `KeybindBind` | keybind hints render through a theme-provided GTK template; this file carries no bind map — binds come from config.toml `[keybinds]`/`[providers.actions]` | mined | 2026-10-20 | on-release | corpus/knowledge/walker-route-r18.md |

All three rows are tagged-source rows (row 1 code, row 2 docs, row 3 code), name walker — and row 1
names elephant — in source/scope, are tier A mined, and name `walker-route-r18.md` as used-by — the C2
source-row conditions for the P3 note, provided L1 assigns ids and the note actually cites them.

## Checks (runnable; both digest checks shown able to fail)

1. `curl -sSL https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/resources/config.toml | sha256sum`
   → expect `3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b`.
   Mutation demo: copy with `max_results = 50`→`51` gives sha256 `779dc31d5f54f00ec401952cffe735e6111634ab12287c1fae95984805d22a01` (≠ expected).
2. `git hash-object <fetched-body>` → expect `997f6548fc633ab7e0020623a69d425d30bd7e3`
   (= tree entry for `resources/config.toml`). Same mutant gives `c5b59158b2d3149f584eb1773820430b2801c0af` (≠ expected).
3. `git ls-remote https://github.com/abenz1267/walker refs/tags/v2.17.2` → `a515085fd39fae80acc086c8fbfd9b7771a9a11d`;
   annotated-tag check `'refs/tags/v2.17.2^{}'` returns nothing (lightweight tag).
4. Receipt audit: `python3 - <<'PY'` over `receipts.jsonl` → 6 lines, all `http_status: 200`,
   every `sha256` equals the saved body's digest (verified above).

## Remaining unknowns (`[UNK]`)

1. Whether `/usr/bin/walker` (2.17.2-1) embeds `resources/config.toml`, synthesizes defaults, or requires a
   user config: file reads cannot show default resolution; no walker invocation was permitted (HOST PAUSE).
2. `additional_theme_location` semantics/recognition in 2.17.2: absent from the tagged default config and
   README; host declares it, but this is declaration only.
3. Theme inheritance for files absent in `omarchy-default` (keybind.xml/layout.xml): only README:219's
   sentence; mechanism unread, runtime unobserved.
4. Release asset `walker-v2.17.2-x86_64-unknown-linux-gnu.tar.gz` (2,772,997 B > 1 MiB) not fetched; whether
   it ships a config copy is unknown.
5. All host runtime behaviour of walker/elephant (provider availability, prefix dispatch, theme loading)
   remains unexercised.

Tooling: no installs or upgrades; `curl 8.23.0`, `git ls-remote`, `git hash-object`, `sha256sum`,
`stat`, `sed`, `grep`, `find` only. No pacman/systemctl/compositor/walker command was run.

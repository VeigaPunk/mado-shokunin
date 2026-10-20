# SrcElephantProviders — elephant v2.22.1 provider config surface

Seat: `MadoR18.SrcElephantProviders` (leaf scout). Round 18, wave 1. Question: at
elephant's 2.22.1 tag fetch the provider config docs/source for
desktopapplications, files, clipboard, menus, calc (whichever exist) with receipts;
record config keys and file locations with quotes.

Method: `git ls-remote` tag resolution, tag-pinned `curl` fetches with one receipt per
fetch, byte-equality check against a throwaway `/tmp` shallow clone at the same commit,
and host file-byte reads only. No elephant/walker/provider binary, socket, pacman,
systemctl, or compositor command was executed. Host pause honoured. No tool was
installed or upgraded (nothing needed; `curl 8.23.0`, `python3 3.14.8` used; `jq` here
reports `jaq 3.1.1` but the `jaq` name is not a command, so receipts were serialized with
`python3` JSON).

## 1. Upstream identity

| item | value | basis |
|---|---|---|
| repo | https://github.com/abenz1267/elephant | `git ls-remote` 2026-10-20 |
| tag | `v2.22.1` | lightweight tag: `refs/tags/v2.22.1` = `8f1e21d6efe40b8b3953f95b9574f99f717caf91`; no peeled `^{}` ref returned |
| commit | `8f1e21d6efe40b8b3953f95b9574f99f717caf91` | clone HEAD at `--branch v2.22.1`; README bytes equal raw tag fetch |
| self-version | `2.22.1` | `cmd/elephant/version.txt` (clone) |
| dependency | `github.com/adrg/xdg v0.5.3` | `go.mod:7`; tag = `aa865a51a1b35fd06925fd6b8604991e79e3167e` (`git ls-remote`) |

All 23 elephant bodies cited below were fetched from `raw.githubusercontent.com/.../v2.22.1/...`
and are byte-identical (sha256) to the clone at `8f1e21d…`; the 4 `adrg/xdg` bodies are
from tag `v0.5.3` (`aa865a51…`). Receipts:
`.ufo/waves/round-18/fetch/SrcElephantProviders/receipts.jsonl` (27 lines: 26 × HTTP 200,
1 × HTTP 404 for a guessed adrg path, kept as fetch evidence). Bodies live beside it.

| body | HTTP | bytes | sha256 |
|---|---|---|---|
| elephant-v2.22.1-README.md | 200 | 6969 | aa19a7e2d1c07bf1852b65fd38ca24a6b04bba0dacfd9f6cb02ada0ee0b61389 |
| desktopapplications-README.md | 200 | 155 | 11840f8883def95d1e46ce088c9d341a97fe32cb4ef6693152fc1279c7ed4625 |
| desktopapplications-setup.go | 200 | 5598 | e089d47b0ec619020534f0fb472dbee4abf1d6aad623ec82f36a41b11b629101 |
| desktopapplications-files.go | 200 | 8277 | 60f6b019e3411f5d9589228a847f3de03600978e417406f9cda2ea5cb7a71656 |
| files-README.md | 200 | 318 | 7a7913c3a3d433fca0851f5aa1c04eb6403069b81d3cdcfeb8f87730cd1e0496 |
| files-setup.go | 200 | 7536 | cf928cf76758d556a18055e9dce63401e5c37ba1371b5e4eb38a9037de3a66eb |
| files-db.go | 200 | 4228 | fa8794d4589fc166fa63f436a6a5bb2b4279d0dc415d512d4af3921053a3ede3 |
| clipboard-README.md | 200 | 232 | 6a24ffb80999e64b46a047cd4e223f9968091794bfe495344dd23dab55a54ce0 |
| clipboard-types.go | 200 | 2347 | c4857730e02bfe96ac9b3845334fb96762261462ac0755648912c23222c4b219 |
| clipboard-setup.go | 200 | 6366 | 34e0db43eca9be04b3f55cd07328b6e6323676051151725f259c1e2dbb97ade9 |
| menus-README.md | 200 | 5638 | 0cb9750e8630b741eadf2c7a59b1128f26949692adac8f7dc256c3a321938bd2 |
| menus-setup.go | 200 | 9123 | d26598231c1c9fd91848e8553ace024741a3db75b1d93e9bca92ee2f292fedc9 |
| calc-README.md | 200 | 260 | 57e52f8f97ce498b1c3d7bb81437dab3411de31be6a2f2c4e1cf6d122e234b78 |
| calc-setup.go | 200 | 7456 | 8d27554eddbf26094f75756ec1ea51ed45fab61c6aa95d2dbe98b70be14dc301 |
| common-config.go | 200 | 3609 | 46ed4755bb3e1c17d839688e21d7ce7de33cd494ab41238e90d75c2486e0c63a |
| common-files.go | 200 | 1348 | 19492c244d1589df7c2cb208fd3393f9d49d8751773424a30f84db59d47a9bc5 |
| common-menucfg.go | 200 | 17734 | 113c061c622b360e6bdec455d630cf4cb690dcc9d751ae8ce0300754802ace62 |
| common-history-history.go | 200 | 3477 | ed1ba315b853e569adf5d8daf324415fa1daab9f0657ccd8a763f1d354c12c7c |
| providers-load.go | 200 | 5379 | 0b1da69e807b900aa73801d9cdb13578d207ecc26d96ac883ee14a789ebfe287 |
| cmd-elephant-elephant.go | 200 | 9283 | c1c2ecaaafac5282e64467dd93d9e9bc3561fd63c1f160526c5015a8ce5dbd34 |
| util-doc.go | 200 | 3982 | 02fa3f3a9fb0be2d9b0a9893801de3f8afc579c3ed29d150d0fcd583f08335ea |
| comm-comm.go | 200 | 2552 | 2b4a6f1493be9d4cc453adcc8f26f8488d360679ab8d4342ea6bf4c0edd16e54 |
| comm-client-query.go | 200 | 2459 | 1ab5141a71f67a119a3d776c4da27ac2218f59c6792c72719aa9d2a3e3034738 |
| adrg-xdg-v0.5.3-tree.json | 200 | 6103 | a8dceb4b66aaf5368e83f310ed0a208a86f4968a9a5cae140ad98ef3b32c9611 |
| adrg-xdg-v0.5.3-base_dirs.go | 200 | 2255 | 40f3a37b936c181762096924686350fb5e6c34c5c248bd78405b80643be0b878 |
| adrg-xdg-v0.5.3-paths_unix.go | 200 | 2869 | 39fdabd86f705b4c8902fc764f4f34d08f9332ca0b400f9127b08dd8c93a3ff0 |
| xdg-v0.5.3-files.go (404 probe) | 404 | 14 | d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed |

## 2. Config resolution shared by all five providers

Observed in `pkg/common/files.go`, `pkg/common/config.go` (tag bytes above):

- Config roots, in order: `$XDG_CONFIG_HOME/elephant` (default `~/.config/elephant`) if it
  exists, then each `$XDG_CONFIG_DIRS/elephant` that exists (`common-files.go:28-54`).
  `--config DIR` replaces the whole list with `DIR` (`common-files.go:28-33`,
  `cmd-elephant-elephant.go:298-307`; flag `Usage: "config folder location"` at :303).
- Provider file: first `<provider>.toml` found across those roots; no merge. Missing file
  is not an error: defaults are used (`common-files.go:65-77`;
  `common-config.go:85-89`). Quote (`common-files.go:66`):
  `provider = fmt.Sprintf("%s.toml", provider)`.
- Cache root: `common.CacheFile` returns `$XDG_CACHE_HOME/elephant/<file>` (default
  `~/.cache/elephant`) (`common-files.go:57-61`):
  `d, _ := os.UserCacheDir()` / `return filepath.Join(d, "elephant", file)`.
- Per-provider common keys (squashed into every provider config):
  `icon`, `name_pretty`, `min_score`, `hide_from_providerlist`
  (`common-config.go:16-21`). Effective per-provider defaults are set in each
  `LoadConfig` initializer, not by the `default:` struct tags — the tags feed the printed
  docs only (`util-doc.go`, `printStructDesc` prints `field.Tag.Get("default")`).
- Docs generation: `elephant generate doc [provider]` (alias `g d`) prints
  `` `~/.config/elephant/<provider>.toml` `` plus a reflection table
  (`util-doc.go:62-64`, `cmd-elephant-elephant.go:156-190`); `generate config` writes the
  file (`util-doc.go:103`). Drift: README says `elephant generatedoc` at README:175 and
  :192-194, but no `generatedoc` command is registered at this tag — only
  `generate` → `doc`/`config`. Therefore the README invocation is not usable syntax at
  v2.22.1. Documentation was not generated here (running elephant is barred by the host
  pause); keys below are transcribed from the koanf tags and initializers.
- Config tree claimed by README:186-190:
  `├── elephant.toml # Main configuration` / `├── .env # Environment variables` /
  `└── <provider>.toml # Provider config`.
- Provider plugins: `libDirs = []string{"/usr/lib/elephant", "/usr/lib64/elephant",
  "/usr/local/lib/elephant", "/usr/local/lib64/elephant", "/lib/elephant",
  "/lib64/elephant"}` plus every `ConfigDirs()` root; `ELEPHANT_PROVIDER_DIR` overrides
  the list; `ELEPHANT_DEV=true` means `/tmp/elephant/providers`
  (`providers-load.go:42-66`). Each `.so` is `plugin.Open`ed (:107); basename names the
  provider.
- IPC socket: `filepath.Join(os.TempDir(), "elephant", "elephant.sock")`
  (`comm-comm.go:42`, `comm-client-query.go:28`) — i.e. `$TMPDIR/elephant/elephant.sock`,
  not the README's "typically `/tmp/elephant.sock`". Querying it executes a client and
  touches the live service; out of bounds here.

## 3. Provider facts

All quoted line numbers refer to the fetched tag bodies in
`.ufo/waves/round-18/fetch/SrcElephantProviders/`. Every provider's config file name is
the provider `Name` (`desktopapplications`, `files`, `clipboard`, `menus`, `calc`).

### 3.1 desktopapplications — `desktopapplications.toml`

Keys (koanf tags + defaults, `desktopapplications-setup.go:46-64`; effective initializer
values `:120-143`):

| key | type | doc/default tag | effective init |
|---|---|---|---|
| `icon` | string | depends on provider | `applications-other` (:123) |
| `name_pretty` | string | depends on provider | unset → `Desktop Applications` |
| `min_score` | int32 | depends on provider | `30` (:124) |
| `hide_from_providerlist` | bool | false | false |
| `locale` | string | "" | "" |
| `action_min_score` | int | 20 | 20 |
| `show_actions` | bool | false | false |
| `show_generic` | bool | true | true |
| `show_actions_without_query` | bool | false | false |
| `history` | bool | true | true |
| `history_when_empty` | bool | false | false |
| `only_search_title` | bool | false | false |
| `icon_placeholder` | string | applications-other | applications-other |
| `aliases` | map[string]string | "" | empty map |
| `blacklist` | []string (regexp) | empty | — |
| `window_integration` | bool | false | false |
| `ignore_pin_with_window` | bool | true | true |
| `window_integration_ignore_actions` | bool | true | true |
| `wm_integration` | bool | false | false |
| `score_open_windows` | bool | true | true |
| `single_instance_apps` | []string | ["discord"] | ["discord"] |

State/file locations:
- Desktop-entry scan roots: `dirs = xdg.ApplicationDirs` (`desktopapplications-files.go:81`).
  `adrg/xdg` v0.5.3 resolves them as `$XDG_DATA_HOME/applications`,
  `~/.local/share/applications`, `/usr/local/share/applications`, `/usr/share/applications`,
  plus `$XDG_DATA_DIRS/*/applications`, deduplicated (`paths_unix.go:32-52`). Quote
  (`paths_unix.go:33-36`): `filepath.Join(baseDirs.dataHome, "applications"),` /
  `filepath.Join(home, ".local/share/applications"),` / `"/usr/local/share/applications",` /
  `"/usr/share/applications",`.
- History: `history.Load("desktopapplications")` (`setup.go:29`) →
  `~/.cache/elephant/desktopapplications_history.gob` (`history.go:82-88,171-185`).
- Pinned: `~/.cache/elephant/desktopapplications_pinned.gob` (`setup.go:67-79`).
- Availability: unconditional `true` (`setup.go:145-147` in clone).
- Drift: `wm_integration` desc says "Currently Niri only", but `Setup` assigns
  `wmi = Hyprland{}` as well (`setup.go:96-111`).

Host declaration: `~/.config/elephant/desktopapplications.toml`, 62 bytes, sha256
`999b191512b29b6822a18f48495169bf4b96573388da2b035452e530f31f434e`; body lines:
`show_actions = false`, `only_search_title = true`, `history = false`. So the host
disables history and searches titles only; it leaves action display off.

### 3.2 files — `files.toml`

Keys (`files-setup.go:41-51`; effective initializer `:111-124`):

| key | type | doc/default tag | effective init |
|---|---|---|---|
| `icon` / `name_pretty` / `min_score` / `hide_from_providerlist` | common | depends | `folder` / `Files` / `20` / false |
| `ignored_dirs` | []string (regexp) | "" | — |
| `ignore_previews` | []{`path`, `placeholder`} | "" | — (`:37-38`) |
| `ignore_watching` | []string | "" | — |
| `search_dirs` | []string | `$HOME` | `[]`, then `os.UserHomeDir()` fallback (`:128-133`) |
| `fd_flags` | []string | malformed doc list | `--ignore-vcs --type file --type directory` |
| `watch_buffer` | int (ms) | 2000 | 2000 |
| `watch_dirs` | []string | [] | — |
| `watch` | bool | false | false |

File locations:
- Index DB: `path := common.CacheFile("files.db")` (`files-db.go:26`) →
  `~/.cache/elephant/files.db`, with `-shm`/`-wal`; `openDB` removes and recreates them at
  setup (`files-db.go:26-44`).
- Search roots are `search_dirs`, indexed by spawning `fd` (`files-setup.go:126-180`);
  `ignored_dirs` are regexp filters.
- Availability: `fd` **or** `fdfind` on PATH (`files-setup.go:246-249`).
- README requirements quote (`files-README.md:19-21`): `#### Requirements` / `- `fd``.
- README `ignored_dirs` example (`:13-17`) is a plain TOML array of path strings.
- State action: `reindex` is advertised when `watch=false` (`files-setup.go:347-357`).

Host declaration: no `~/.config/elephant/files.toml` → all defaults. Cache exists:
`~/.cache/elephant/files.db` 4096 B + `files.db-shm` 32768 B + `files.db-wal` 61832 B
(mtime 2026-10-20 09:57), consistent with the provider having indexed at least once;
the SQLite rows were not read. `/usr/bin/fd` exists; `/usr/bin/fdfind` absent.

### 3.3 clipboard — `clipboard.toml`

Keys (`clipboard-types.go:50-60`; effective initializer `clipboard-setup.go:84-101`):

| key | type | doc/default tag | effective init |
|---|---|---|---|
| `icon` / `name_pretty` / `min_score` / `hide_from_providerlist` | common | depends | `user-bookmarks` / `Clipboard` / `30` / false |
| `max_items` | int | 100 | 100 |
| `ocr` | bool | false | false |
| `image_editor_cmd` | string (`%FILE%`) | "" | "" |
| `text_editor_cmd` | string (`%FILE%`) | "" | "" |
| `command` | string | `wl-copy` | `wl-copy` |
| `ignore_symbols` | bool | true | true |
| `pinned_on_top` | bool | false | false |
| `auto_cleanup` | int (minutes) | 0 | 0 |

File locations:
- History: `file = common.CacheFile("clipboard.gob")` (`clipboard-types.go:15`) →
  `~/.cache/elephant/clipboard.gob` (gob; mode 0600 on write, `clipboard-setup.go:187-207`).
- Images: `folder := filepath.Join(d, "elephant", "clipboardimages")`
  (`clipboard-setup.go:249-257`) → `~/.cache/elephant/clipboardimages/<unix>.<ext>`.
- Requirements: `wl-paste` and `identify` gate `Available`
  (`clipboard-setup.go:103-121`); README:13-16 quotes `wl-clipboard` and `imagemagick`.
  OCR additionally warns when `tesseract` is missing (`setup.go:36-43`).
- Modes/actions (source constants, `clipboard-types.go:64-77`): combined,
  `show_images_only`, `show_text_only`, `show_pinned_only`; `pause`/`unpause`;
  `pin`/`unpin`; `copy`/`edit`/`remove`/`remove_all`; `localsend`. MIME
  `x-kde-passwordManagerHint` is ignored (`:80`).

Host declaration: no `~/.config/elephant/clipboard.toml` → defaults. Cache:
`clipboard.gob` 93500 B and `clipboardimages/` present (mtime 2026-10-20 10:26); contents
were not decoded. `/usr/bin/wl-copy`, `/usr/bin/wl-paste` present;
`/usr/bin/identify -> magick`; `/usr/bin/tesseract` present.

### 3.4 menus — `menus.toml` + menu definition files

Config keys:
- Provider config `menus.toml`: common keys plus `paths` ([]string, "additional paths to
  check for menu definitions") (`common-menucfg.go:29-32`); effective `min_score` 10
  (`:441-446`).
- Menu definition TOML keys (`Menu` struct `common-menucfg.go:34-61`): `hosts`,
  `hide_from_providerlist`, `name`, `name_pretty`, `description`, `icon`, `action`,
  `actions`, `async_actions`, `search_name`, `cache`, `refresh_on_change`, `entries`,
  `terminal`, `keywords`, `fixed_order`, `priority`, `history`, `history_when_empty`,
  `min_score`, `parent`, `submenu`, `hide_name_pretty_prefix`.
- Entry keys (`Entry` struct `:407-424`): `hosts`, `text`, `async`, `subtext`, `value`,
  `actions`, `terminal`, `icon`, `submenu`, `preview`, `preview_type`, `keywords`,
  `state`.
- Lua menus export globals read at load: `Name`, `NamePretty`, `HideFromProviderlist`,
  `Description`, `Icon`, `Action`, `Actions`, `SearchName`, `Cache`, `Terminal`,
  `Keywords`, … (`common-menucfg.go:493-647` clone) and must define `GetEntries()`
  (`:278-287`).

File locations:
- README quote (`menus-README.md:14`): "Default location for menu definitions is
  `~/.config/elephant/menus/`."
- Actual search roots (`common-menucfg.go:448-456`): every `ConfigDirs()/menus`, plus
  `installed := filepath.Join(xdg.DataHome, "elephant", "install")`, plus the `paths`
  key. Quote: `path := filepath.Join(v, "menus")` / `installed := filepath.Join(xdg.DataHome,
  "elephant", "install")`.
- Scanner accepts `.toml` and `.lua` only (`common-menucfg.go:467-486`).
- Action substitution at activation (`menus-setup.go:148-197`): `lua:` prefix calls a Lua
  function; `%CLIPBOARD%`, `%VALUE%` (else value is piped on stdin), `%ARGS%`;
  `terminal = true` wraps through `common.WrapWithTerminal`.
- `elephant generate doc menus` prints the `MenuConfig` and `Menu` tables
  (`menus-setup.go:33-44`).

Host declaration:
- `~/.config/elephant/menus/` exists with three symlinks into the omarchy checkout:
  `omarchy_background_selector.lua` → `~/.local/share/omarchy/default/elephant/omarchy_background_selector.lua`
  (sha256 `292c7deb0ddc0d006728a3c9740cf196c818240af5d24b7c0cb9a2e2bab5f7eb`);
  `omarchy_themes.lua` (sha256 `d997d5a4c27ffc109a4302075fd4f12445ddc1fc44eea3ec28a37dd9617f386a`);
  `omarchy_unlocks.lua` (sha256 `b577869246d8050fd02401b37916c6251afaaaf8e9bdc9c2c9c7d48a82905c61`).
  These declare Lua menus named `omarchyBackgroundSelector`, `omarchythemes`,
  `omarchyunlocks`; their `Actions.activate` strings call `omarchy-theme-bg-set`,
  `omarchy-theme-set`, and `omarchy-plymouth-*` respectively. These are declarations in
  file bytes; no action was executed.
- No `~/.config/elephant/menus.toml`; no `~/.local/share/elephant/install` directory.
- omarchy checkout: HEAD file says `ref: refs/heads/master`; `packed-refs` maps
  `refs/tags/v3.8.4` → `8fcc9d6048af4cb0e3af8512c78049857a3b53dd`; the three default
  elephant Lua files' bytes equal the symlink targets' hashes above.

### 3.5 calc — `calc.toml`

Keys (`calc-setup.go:43-52`; effective initializer `:83-98`):

| key | type | doc/default tag | effective init |
|---|---|---|---|
| `icon` / `name_pretty` / `min_score` / `hide_from_providerlist` | common | depends | `accessories-calculator` / `Calculator/Unit-Conversion` / 0 (unset) / false |
| `max_items` | int | 100 | 100 |
| `placeholder` | string | calculating... | calculating... |
| `require_number` | bool | true | true |
| `min_chars` | int | 3 | 3 |
| `command` | string (`%VALUE%`) | `wl-copy -n '%VALUE%'` | same |
| `async` | bool | **true** | **false** — doc/tag drift |
| `autosave` | bool | false | false |

File location and deps:
- History: `file := common.CacheFile(fmt.Sprintf("%s.gob", Name))` (`calc-setup.go:300`)
  → `~/.cache/elephant/calc.gob`; identifiers are `md5(query)` (`:187-200`).
- Availability: `qalc` on PATH (`calc-setup.go:100-108`); queries run
  `qalc -t -s "digit grouping 2" <query>` (`:220-266`). README:10-13 quotes
  `libqalculate` and `wl-clipboard`.
- `async` effective default is false, but the tag/docs claim true, so generated docs
  would misstate the default; host `calc.toml` sets `async = false` explicitly anyway.

Host declaration: `~/.config/elephant/calc.toml`, 14 bytes, sha256
`2c0ef81b8edc9edfdc409570bf18ba9d44f488a30d6b223533cce66ee266bdb5`, body
`async = false`. `~/.cache/elephant/calc.gob` is absent (no saved calculations at read
time). `/usr/bin/qalc` present.

## 4. Host declaration plane (file bytes only; nothing executed)

Versions via `grep -n` of `/var/log/pacman.log` (file read):

| line | event |
|---|---|
| 2929 | `upgraded walker (2.17.0-1 -> 2.17.2-1)` (2026-10-20T09:16:46-0300) |
| 3095 | `upgraded elephant (2.21.0-1 -> 2.22.1-1)` (2026-10-20T09:31:03-0300) |
| 3097 | `upgraded elephant-clipboard (2.21.0-1 -> 2.22.1-1)` |
| 3101 | `upgraded elephant-calc (2.21.0-1 -> 2.22.1-1)` |
| 3107 | `upgraded elephant-files (2.21.0-1 -> 2.22.1-1)` |
| 3111 | `upgraded elephant-desktopapplications (2.21.0-1 -> 2.22.1-1)` |
| 3119 | `upgraded elephant-menus (2.21.0-1 -> 2.22.1-1)` |

Caveat: pacman.log records package transactions; it does not prove which provider bytes a
running elephant process loaded, nor that elephant is running.

Byte identity of installed artifacts (file reads; hashes do not execute anything):

| path | bytes | sha256 |
|---|---|---|
| `/usr/bin/elephant` (mtime 2026-10-20 09:29) | 23460760 | b0761ff7b7cc8d211693b2b691e44d12aef2745e304c8b38f1c35bd71b5cc8ea |
| `/usr/lib/elephant/desktopapplications.so` | — | d9406a52c25868a8a36ce7288305c68a8d94103e03960af7fc27d4d7790dabe5 |
| `/usr/lib/elephant/files.so` | — | b1f5cb7fa7520d96547f8de70b161b37e38ae795ac8ffe45a7d3bd482fbc87ad |
| `/usr/lib/elephant/clipboard.so` | — | 8e5d82589ca98b79404ebb4bf2c79efadd3149c776287fca9066683b271d67b2 |
| `/usr/lib/elephant/menus.so` | — | 6b3cf7395f5c31f965299d1feeff3ed5e311151f17f5947007eccc7bda2350a4 |
| `/usr/lib/elephant/calc.so` | — | ef1a07fd37e9cfa6c8ef9b4d1431e57cbaab4fa663cf55511b8d25f54b9c11d7 |

These `.so` hashes are this host's installed bytes; they cannot be shown equal to the
tag's Go source, and the tag source cannot prove the binary. Absolute versions above come
only from pacman.log.

Other declared host files (bytes read):
- `~/.config/elephant/`: `calc.toml`, `desktopapplications.toml`, `symbols.toml`
  (symbols provider, out of scope; 81 B, sha256 `9c0d5edf1fce95f3c785af79535c3c95ab6aaa5c16048e7e42560182e33efd9b`),
  `menus/` (three symlinks). Absent: `elephant.toml`, `.env`, `files.toml`,
  `clipboard.toml`, `menus.toml`, `providers/`.
- `~/.cache/elephant/`: `clipboard.gob` 93500 B, `clipboardimages/`, `files.db` 4096 B,
  `files.db-shm` 32768 B, `files.db-wal` 61832 B. Absent: `calc.gob`,
  `desktopapplications_history.gob`, `menus_history.gob`.
- PATH files present as bytes: `/usr/bin/qalc`, `/usr/bin/fd`, `/usr/bin/wl-copy`,
  `/usr/bin/wl-paste`, `/usr/bin/identify` → `magick`, `/usr/bin/tesseract`;
  `/usr/bin/fdfind` absent.

## 5. Confidence

| finding | confidence | basis |
|---|---|---|
| tag `v2.22.1` = `8f1e21d…`; bodies byte-identical to clone | high | ls-remote + sha equality |
| config root order, `<provider>.toml` first-match, cache root | high | tagged source read |
| five provider key sets and effective defaults | high | koanf tags + initializer read |
| file locations (`files.db`, `clipboard.gob`, `clipboardimages`, `calc.gob`, history gobs, menu roots) | high | tagged source read |
| desktop-entry roots = `xdg.ApplicationDirs` | high for the call; medium for full path list | adrg/xdg v0.5.3 pinned source; active `$XDG_*` env not read |
| host config bytes/digests/absence, cache listing, binary hashes | high | direct file reads |
| host package versions | high as pacman transaction record; not as runtime state | `/var/log/pacman.log` |
| README `generatedoc` unusable at this tag | high | command registry read (`generate`/`g` + `doc`/`d` only) |
| calc `async` doc/default mismatch | high | tag default vs initializer read |

## 6. Remaining unknowns

- Runtime state: whether an elephant service is running, which provider plugins it loaded,
  and whether walker queries it. Not probeable under the host pause (no service/socket
  queries), and outside this seat's file-read method.
- Contents of `clipboard.gob`, `files.db`, `files.db-wal` were not decoded; presence and
  size only.
- Actual `$XDG_CONFIG_HOME`, `$XDG_CONFIG_DIRS`, `$XDG_DATA_HOME`, `$XDG_DATA_DIRS`,
  `$XDG_CACHE_HOME`, `$TMPDIR` values were not read; the host paths quoted are the
  library defaults that match the observed trees.
- `elephant generate doc` output not produced (would execute elephant). Key tables here
  are source-derived; where `default:` tags disagree with initializers (calc `async`,
  files `fd_flags`) the generated doc would differ from effective behavior.
- Ranked scoring semantics (fuzzy history weighting, window integration) were not
  modelled; only declared keys and locations are asserted.
- Walker's own provider list/config is another seat's scope; no walker config was read
  here.

## 7. Proposed SOURCES.md rows (ids reserved S072–S099; drafts use `S0xx-pending`)

All rows: tier A (upstream official code/docs), status `mined`, recheck `on-release`.
`used-by` is proposed; L1 assigns ids and final notes.

| id | source | kind | scope | anchor | teaches |
|---|---|---|---|---|---|
| S0xx-pending | Elephant v2.22.1 README — https://raw.githubusercontent.com/abenz1267/elephant/v2.22.1/README.md | docs | config tree, provider install layout, CLI examples at the tag | README.md:158-194 @ v2.22.1 (`8f1e21d…`, sha256 aa19a7e2…) | declares `~/.config/elephant/{elephant.toml,.env,<provider>.toml}`; its `generatedoc` examples do not match the tag's registered `generate doc` commands |
| S0xx-pending | Elephant v2.22.1 config resolution — https://raw.githubusercontent.com/abenz1267/elephant/v2.22.1/pkg/common/files.go and .../config.go | code | provider config discovery, cache root, common keys | files.go:28-77; config.go:16-21,76-110 @ v2.22.1 (sha256 19492c24… / 46ed4755…) | first existing `<provider>.toml` in XDG config dirs wins; missing file is not fatal; cache is `$XDG_CACHE_HOME/elephant` |
| S0xx-pending | Elephant v2.22.1 desktopapplications — .../internal/providers/desktopapplications/{README.md,setup.go,files.go} | docs+code | key set, defaults, desktop-entry scan roots | setup.go:46-64,120-143; files.go:73-81; README.md:1-10 @ v2.22.1 (sha256 e089d47b… / 60f6b019…) | full key/default table; entries come from `xdg.ApplicationDirs`; history/pin gob names |
| S0xx-pending | adrg/xdg v0.5.3 unix base dirs — https://raw.githubusercontent.com/adrg/xdg/v0.5.3/paths_unix.go | code | XDG defaults for applications/config/data search lists | paths_unix.go:21-52 @ v0.5.3 (`aa865a51…`, sha256 39fdabd8…) | `ApplicationDirs` = data-home/applications + `~/.local/share/applications` + `/usr/local/share/applications` + `/usr/share/applications` + `$XDG_DATA_DIRS/*/applications`, deduped |
| S0xx-pending | Elephant v2.22.1 files — .../internal/providers/files/{README.md,setup.go,db.go} | docs+code | key set, defaults, SQLite cache path, fd gate | setup.go:41-51,111-124,246-249; db.go:23-44; README.md:13-21 @ v2.22.1 (sha256 cf928cf7… / fa8794d4…) | `files.db` under the cache root is recreated at setup; `fd`/`fdfind` availability gate; ignored_dirs regexp |
| S0xx-pending | Elephant v2.22.1 clipboard — .../internal/providers/clipboard/{README.md,types.go,setup.go} | docs+code | key set, defaults, history/image locations, dependency gate | types.go:15,50-60,64-77,80; setup.go:84-121,249-257; README.md:13-16 @ v2.22.1 (sha256 c4857730… / 34e0db43…) | `clipboard.gob` history and `clipboardimages/`; wl-paste+identify required; OCR needs tesseract |
| S0xx-pending | Elephant v2.22.1 menus — .../internal/providers/menus/{README.md,setup.go} + .../pkg/common/menucfg.go | docs+code | provider `paths` key, Menu/Entry key sets, search roots, action placeholders | menucfg.go:29-32,34-61,407-424,438-456,467-486; setup.go:33-44,148-197; README.md:14 @ v2.22.1 (sha256 113c061c… / d2659823…) | menus load `.toml`/`.lua` from every `<config>/menus`, `$XDG_DATA_HOME/elephant/install`, and `paths`; `%VALUE%`/`%ARGS%`/`%CLIPBOARD%` semantics |
| S0xx-pending | Elephant v2.22.1 calc — .../internal/providers/calc/{README.md,setup.go} | docs+code | key set, defaults, history location, qalc gate | setup.go:43-52,83-108,300; README.md:10-13 @ v2.22.1 (sha256 8d27554e… / 57e52f8f…) | `calc.gob` history; qalc on PATH; `async` tag says true while initializer says false |
| S0xx-pending | Elephant v2.22.1 provider loader + CLI — .../internal/providers/load.go and .../cmd/elephant/elephant.go | code | plugin directories, `--config`, generate doc/config commands | load.go:42-66,107; elephant.go:154-190,298-307,388-396 @ v2.22.1 (sha256 0b1da69e… / c1c2ecaa…) | `.so` plugins load from `/usr/lib/elephant` and config roots; `--config` replaces config roots; `generate doc/config` are the doc surfaces |
| S0xx-pending | Elephant v2.22.1 history + doc generator — .../pkg/common/history/history.go and .../internal/util/doc.go | code | history gob naming, generated-doc table semantics | history.go:82-88,171-185; doc.go:20-110 @ v2.22.1 (sha256 ed1ba315… / 02fa3f3a…) | history file is `<provider>_history.gob` in the cache root; doc table prints `default:` tags, not effective initializer values |

Proposed used-by: rows 1–6, 8, 9, 10 → `corpus/knowledge/walker-route-r18.md` (P3);
row 7 → both `corpus/knowledge/walker-route-r18.md` (P3) and
`corpus/knowledge/theme-route-r18.md` (P5, as supporting only — the theme-shipping
upstream row must come from the theme seat).

## 8. Notes for the P3/P5 route notes (documentary only)

- C2 admissibility for P3: each elephant row above is an upstream https docs/code row whose
  source path/URL names **elephant**; rows do not name walker, so a qualifying P3 note still
  needs at least one row that names walker in source/scope — that belongs to the walker
  seats. What this report supplies is the elephant half of the walker↔elephant chain and
  the exact host declaration (configs, package versions, installed plugin/socket layout).
- Safe observation for this surface, if a later round wants one: read-only `ls`/`cat`/
  `sha256sum` of `~/.config/elephant/`, `~/.cache/elephant/`, `/usr/lib/elephant/`, and
  `/var/log/pacman.log`. Do not query `$TMPDIR/elephant/elephant.sock`, do not run
  `elephant query/activate`, do not run `walker`, and do not trigger menu actions
  (`omarchy-theme-set`, `omarchy-theme-bg-set`, `omarchy-plymouth-*`).
- Unexercised behavior: provider query/activation, clipboard content, menu action
  execution, `qalc` evaluation, `fd` indexing, `generatedoc` output, and any walker-side
  provider selection. Host binaries remain [UNK] as behavior; only installed bytes are
  recorded.
- Documentation conflicts found at the same tag (worth carrying into lessons/notes rather
  than smoothing): `generatedoc` (README) vs `generate doc` (CLI source); README socket
  `/tmp/elephant.sock` vs `$TMPDIR/elephant/elephant.sock`; `wm_integration` "Currently
  Niri only" vs Hyprland branch; calc `async` default tag true vs initializer false;
  files `fd_flags` doc default malformed vs initializer values.

## 9. Tooling record

None installed, upgraded, or downgraded. Used: `git ls-remote`, `git clone --depth 1`
(throwaway `/tmp/elephant-2.22.1`), `curl 8.23.0`, `python3 3.14.8`, coreutils
(`sha256sum`, `stat`, `ls`, `cat`, `readlink`, `grep`, `find`, `cmp`), `wc`. No pacman,
systemctl, journalctl, hyprctl, wayland probe, compositor, or elephant/walker process was
run; no file under `/home/vgpnk/Projects/shokunin` outside the lane root was written.

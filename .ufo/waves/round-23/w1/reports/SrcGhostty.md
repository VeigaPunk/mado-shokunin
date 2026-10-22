# SrcGhostty — ghostty upstream sourcing for C2 (round 23, wave 1)

Seat: `MadoR23.SrcGhostty` (scribe). Scope: open primary upstream sources for the **ghostty**
terminal — config file location, format, include/import and reload — and draft the
`corpus/SOURCES.md` rows plus the route-claim rows. **Nothing was landed by me**: `corpus/SOURCES.md`
was not edited, no corpus file was created or edited, no product code, judge, commit, push,
publish or deploy was touched. The only file written in the lane repo is this report.

Access date for every source below: **2026-10-22**.

## 1. What was done

Sources were opened over ordinary fetch/read means only (`curl`, GitHub REST API, `git ls-remote`,
`tar`). No headless browser, no bot challenge, no credential material. Nothing on the host was
changed: the only host reads were `pacman -Qi ghostty`, `ls`, `sha256sum`, `stat`, `head -c` on
`~/.config/ghostty/`. No package was installed or upgraded in this seat, so there is no
tool-install line to record.

### 1.1 Version pins established

| item | value |
|---|---|
| ghostty release tag | `v1.3.1` |
| annotated tag object | `22efb0be2bbea73e5339f5426fa3b20edabcaa11` (PGP-signed) |
| peeled commit | `332b2aefc6e72d363aa93ab6ecfc86eeeeb5ed28` |
| tagger date | 2026-03-13T16:03:38Z |
| source tarball | `https://codeload.github.com/ghostty-org/ghostty/tar.gz/refs/tags/v1.3.1`, 37,423,780 B, sha256 `265837d3026b433f0e6b4e49d43153b915b0a19513f7edd8a8e693c559bd415b` |
| ghostty.org site repo | `ghostty-org/website`, branch `main` (no tags); docs pinned by commit |
| docs commit for `docs/config/index.mdx` | `3755ed6e61b250e994d0e46d55f2a11cb0aa482c` (2026-04-01) — latest commit touching that file |
| docs commit for `docs/config/reference.mdx` | `155c4cd7af9c0de4e0c3c1a4c916b6db3ba39055` (2026-03-13, "update refs") — the reference regenerated for the v1.3.1 release day |
| other tags read for boundary checks | `v1.2.3` (tagger 2025-10-23, peeled `6d2dd585a5d8`), `v1.3.0` (tagger 2026-03-09, peeled `703d11c642a9`) |

### 1.2 Exact commands run (all read-only)

```
git ls-remote --tags --refs https://github.com/ghostty-org/ghostty.git
curl -sS https://api.github.com/repos/ghostty-org/ghostty/git/ref/tags/v1.3.1
curl -sS https://api.github.com/repos/ghostty-org/ghostty/git/tags/22efb0be2bbea73e5339f5426fa3b20edabcaa11
curl -sS https://api.github.com/repos/ghostty-org/ghostty/git/trees/v1.3.1?recursive=1
curl -sSL https://codeload.github.com/ghostty-org/ghostty/tar.gz/refs/tags/v1.3.1 -o ghostty-v1.3.1.tar.gz
sha256sum ghostty-v1.3.1.tar.gz
tar -xzf ghostty-v1.3.1.tar.gz --wildcards 'ghostty-1.3.1/src/*' 'ghostty-1.3.1/macos/*'
curl -sS https://raw.githubusercontent.com/ghostty-org/ghostty/v1.3.1/src/config/file_load.zig
curl -sS https://raw.githubusercontent.com/ghostty-org/ghostty/v1.3.1/src/os/xdg.zig
curl -sS https://raw.githubusercontent.com/ghostty-org/ghostty/v1.3.1/src/config/Config.zig
curl -sS https://raw.githubusercontent.com/ghostty-org/ghostty/v1.3.1/src/apprt/gtk/class/application.zig
curl -sS https://raw.githubusercontent.com/ghostty-org/ghostty/v1.3.1/macos/Sources/App/macOS/AppDelegate.swift
curl -sS https://raw.githubusercontent.com/ghostty-org/ghostty/v1.2.3/src/config/Config.zig
curl -sS https://raw.githubusercontent.com/ghostty-org/website/3755ed6e61b250e994d0e46d55f2a11cb0aa482c/docs/config/index.mdx
curl -sS https://raw.githubusercontent.com/ghostty-org/website/155c4cd7af9c0de4e0c3c1a4c916b6db3ba39055/docs/config/reference.mdx
curl -sS https://ghostty.org/docs/config ; curl -sS https://ghostty.org/docs/config/reference   (×2 each, byte-comparable)
sha256sum <each fetched file>
grep -rn "SIGHUP|SIGUSR2|FileMonitor|inotify|DispatchSource.makeFileSystemObjectSource" <extracted tree>
pacman -Qi ghostty ; ls ~/.config/ghostty/ ; sha256sum ~/.config/ghostty/config
```

### 1.3 Fetched bytes and their digests (sha256)

| file | bytes | lines | sha256 |
|---|---|---|---|
| website `docs/config/index.mdx` @ `3755ed6e` | 6,449 | 172 | `73dee8238359099c19a80cf093c9fa7dca20bb0d6d14e8816491e8eb54d6bf69` |
| live `https://ghostty.org/docs/config` (HTML) | 111,894 | — | `cb79ca5dcf496d81ed05862e1888958c307dc934988b3595926b2c17ab08b6b5` (two consecutive fetches byte-identical) |
| website `docs/config/reference.mdx` @ `155c4cd7` | 147,739 | 3,897 | `f0215afcce0488bbd2c49825005c73847f510098670a6d4a64e4da7837ba4be6` (identical to `main` today) |
| live `https://ghostty.org/docs/config/reference` (HTML) | 1,268,048 | — | `fad11c9fe16421e3f91563a69e364e67e979c7664b7eecc499bb64f89deb6f26` (two consecutive fetches byte-identical) |
| `src/config/file_load.zig` @ `v1.3.1` | 5,434 | 166 | `96e8165c5a365808b7407d61f7073aa074189bcd96b3daa0a43d37f5e3d4c94f` |
| `src/os/xdg.zig` @ `v1.3.1` | 9,739 | 308 | `47da4a574f6a3377b1476d604d9ff6f8b066fd8162f98b3d1a3f54ba26ef1949` |
| `src/config/Config.zig` @ `v1.3.1` | 410,678 | 10,855 | `169a631b9b62c5fa0b05ab0fe750240887b95b45f758c8b4a0e4ce069acbe07c` |
| `src/apprt/gtk/class/application.zig` @ `v1.3.1` | 103,328 | 2,925 | `2bb25a3b9a2ed7f73a7593536737d7ba0fc7e60370a953210b60119c6c5847a7` |
| `macos/Sources/App/macOS/AppDelegate.swift` @ `v1.3.1` | 59,504 | 1,403 | `2ca56276a8525c593c3db2c939c27a5ac6f3273277105bd22e7f5ec485040a91` |
| `src/config/Config.zig` @ `v1.2.3` | 339,217 | — | `ed2eb047c44c3ad82d4e1e5d23240198e289e8bf34520c444105b4a3008a6e1e` |

Every `raw.githubusercontent.com` fetch was compared byte-for-byte with the same path inside the
v1.3.1 tarball: `file_load.zig`, `xdg.zig`, `Config.zig`, `application.zig` and `AppDelegate.swift`
all matched (`cmp` reported identical). The digests above are therefore tarball-verified.

## 2. Sources — one SOURCES row per source (draft, 11-column shape)

Column order is `corpus/SOURCES.md`'s registry header:
`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`.

Id band **S134–S139** for the six primary rows, plus **S150–S151** for the macOS reload
corroboration and the v1.2.3 rename-boundary file. Bands are agreed with the other C2 source
seats: kitty S123–S133, foot S140–S149 plus S152, ghostty S134–S139 and S150–S151. (The foot band
grew to S149 after this seat had taken S149 for the macOS row; both ghostty rows were renumbered up
to S150/S151 so no id is claimed twice. Foot later reserved S152 for a foot CHANGELOG row; ghostty
takes nothing there.) The integrator renumbers if the bands collide; the ids are otherwise free.

| S134 | Ghostty configuration guide (ghostty.org) — https://ghostty.org/docs/config — source of the page: ghostty-org/website `docs/config/index.mdx` | docs | A | ghostty config file name, search path, precedence, `key = value` format, `config-file` includes and the documented reload keybinding | `docs/config/index.mdx` §File Location (lines 36–55), §Syntax (57–90), §Splitting into Multiple Files (92–119), §Reloading the Configuration (121–131) @ commit `3755ed6e61b250e994d0e46d55f2a11cb0aa482c` (2026-04-01), raw fetch https://raw.githubusercontent.com/ghostty-org/website/3755ed6e61b250e994d0e46d55f2a11cb0aa482c/docs/config/index.mdx, 6,449 B sha256 `73dee8238359099c19a80cf093c9fa7dca20bb0d6d14e8816491e8eb54d6bf69`; rendered page https://ghostty.org/docs/config fetched 2026-10-22, 111,894 B sha256 `cb79ca5dcf496d81ed05862e1888958c307dc934988b3595926b2c17ab08b6b5` | the config file is `config.ghostty`; it is loaded from `$XDG_CONFIG_HOME/ghostty/config.ghostty` then `$XDG_CONFIG_HOME/ghostty/config`, and `XDG_CONFIG_HOME` defaults to `$HOME/.config`; syntax is `key = value`; includes use `config-file`; reload is `ctrl+shift+,` / `cmd+shift+,` | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S135 | Ghostty option reference (ghostty.org) — https://ghostty.org/docs/config/reference — source of the page: ghostty-org/website `docs/config/reference.mdx` | docs | A | per-option ghostty configuration semantics, above all the `config-file` and `config-default-files` options | `docs/config/reference.mdx` §`config-file` (lines 2490–2519) and §`config-default-files` (2520–2528) @ commit `155c4cd7af9c0de4e0c3c1a4c916b6db3ba39055` (2026-03-13, the v1.3.1 reference refresh), raw fetch https://raw.githubusercontent.com/ghostty-org/website/155c4cd7af9c0de4e0c3c1a4c916b6db3ba39055/docs/config/reference.mdx, 147,739 B sha256 `f0215afcce0488bbd2c49825005c73847f510098670a6d4a64e4da7837ba4be6`; rendered page https://ghostty.org/docs/config/reference fetched 2026-10-22, 1,268,048 B sha256 `fad11c9fe16421e3f91563a69e364e67e979c7664b7eecc499bb64f89deb6f26` | an included file is loaded *after* the file that names it, so its keys win; a `?` prefix makes the path optional; a cycle is detected, logged and the file ignored | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S136 | ghostty `src/config/file_load.zig` @ v1.3.1 — https://github.com/ghostty-org/ghostty/blob/v1.3.1/src/config/file_load.zig | code | A | the exact filenames ghostty looks for on the XDG and macOS paths, and which of the two is preferred | tag `v1.3.1` (annotated tag object `22efb0be2bbea73e5339f5426fa3b20edabcaa11`, peeled commit `332b2aefc6e72d363aa93ab6ecfc86eeeeb5ed28`); `defaultXdgPath` lines 9–15 (`subdir = "ghostty/config.ghostty"`), `legacyDefaultXdgPath` lines 18–24 (`subdir = "ghostty/config"`, comment "Ghostty <1.3.0 default path"), `preferredXdgPath` 27–50, `preferredDefaultFilePath` 88–112; raw fetch https://raw.githubusercontent.com/ghostty-org/ghostty/v1.3.1/src/config/file_load.zig, 5,434 B sha256 `96e8165c5a365808b7407d61f7073aa074189bcd96b3daa0a43d37f5e3d4c94f` | upstream carries two XDG config names at v1.3.1 — `config.ghostty` and the pre-1.3.0 `config` — and prefers whichever exists; the macOS Application Support path carries the same pair | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S137 | ghostty `src/os/xdg.zig` @ v1.3.1 — https://github.com/ghostty-org/ghostty/blob/v1.3.1/src/os/xdg.zig | code | A | how `$XDG_CONFIG_HOME` is resolved and what the fallback is when it is unset | tag `v1.3.1` (peeled commit `332b2aefc6e72d363aa93ab6ecfc86eeeeb5ed28`); `config()` lines 23–29 (`.env = "XDG_CONFIG_HOME"`, `.default_subdir = ".config"`), `dir()` 56–101 (env value used as-is; else `<home>/.config/<subdir>`); raw fetch https://raw.githubusercontent.com/ghostty-org/ghostty/v1.3.1/src/os/xdg.zig, 9,739 B sha256 `47da4a574f6a3377b1476d604d9ff6f8b066fd8162f98b3d1a3f54ba26ef1949` | `$XDG_CONFIG_HOME` is used verbatim when set and non-empty; otherwise the path is `$HOME/.config` plus the subdir; `LOCALAPPDATA` is the Windows-only stand-in | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S138 | ghostty `src/config/Config.zig` @ v1.3.1 — https://github.com/ghostty-org/ghostty/blob/v1.3.1/src/config/Config.zig | code | A | upstream's own statements of the default config file, the default-file load order, the `config-file` option and the default reload keybinding | tag `v1.3.1` (peeled commit `332b2aefc6e72d363aa93ab6ecfc86eeeeb5ed28`); `config-file` option doc 2425–2452, `config-default-files` doc 2454–2465, `loadDefaultFiles` doc 3986–3993 and body 3994–4062, default keybind table 6401–6411; raw fetch https://raw.githubusercontent.com/ghostty-org/ghostty/v1.3.1/src/config/Config.zig, 410,678 B sha256 `169a631b9b62c5fa0b05ab0fe750240887b95b45f758c8b4a0e4ce069acbe07c` | upstream states the legacy `config` file is loaded first and `config.ghostty` second; a cycle in `config-file` is diagnosed and the file skipped; the default reload binding is `,` with ctrl-or-super+shift | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S139 | ghostty `src/apprt/gtk/class/application.zig` @ v1.3.1 — https://github.com/ghostty-org/ghostty/blob/v1.3.1/src/apprt/gtk/class/application.zig | code | A | how a running ghostty instance is told to reload, and what soft versus hard reload means | tag `v1.3.1` (peeled commit `332b2aefc6e72d363aa93ab6ecfc86eeeeb5ed28`); `handleSigusr2` lines 1486–1503 ("SIGUSR2 signal handler via g_unix_signal_add"), `reloadConfig` 2406–2450 (soft = re-apply conditionals to the loaded config; hard = load a new config completely); raw fetch https://raw.githubusercontent.com/ghostty-org/ghostty/v1.3.1/src/apprt/gtk/class/application.zig, 103,328 B sha256 `2bb25a3b9a2ed7f73a7593536737d7ba0fc7e60370a953210b60119c6c5847a7` | on GTK, `SIGUSR2` is the in-process reload trigger and it is a real reload (new config object) versus a soft reload that only re-evaluates conditionals | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S150 | ghostty `macos/Sources/App/macOS/AppDelegate.swift` @ v1.3.1 — https://github.com/ghostty-org/ghostty/blob/v1.3.1/macos/Sources/App/macOS/AppDelegate.swift | code | A | the macOS half of the in-process reload route, corroborating that `SIGUSR2` is upstream's cross-platform reload signal rather than a GTK-only one | tag `v1.3.1` (peeled commit `332b2aefc6e72d363aa93ab6ecfc86eeeeb5ed28`); `setupSignals` lines 535–561 (`signal(SIGUSR2, SIG_IGN)` at 543, `DispatchSource.makeSignalSource(signal: SIGUSR2, …)` at 547, `self.ghostty.reloadConfig()` at 551), `@IBAction func reloadConfig` 947–949, `syncMenuShortcut(config, action: "reload_config", …)` 1155; raw fetch https://raw.githubusercontent.com/ghostty-org/ghostty/v1.3.1/macos/Sources/App/macOS/AppDelegate.swift, 59,504 B sha256 `2ca56276a8525c593c3db2c939c27a5ac6f3273277105bd22e7f5ec485040a91` | the macOS app registers `SIGUSR2` and reloads the config in response, so the signal route is a property of ghostty and not of one windowing backend; macOS-only, documentary, no macOS runtime was exercised | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |
| S151 | ghostty `src/config/Config.zig` @ v1.2.3 — https://github.com/ghostty-org/ghostty/blob/v1.2.3/src/config/Config.zig | code | A | the pre-rename default config filename upstream used, to date the boundary at which `config` became `config.ghostty` | tag `v1.2.3` (annotated tag object `ae9b7892fa099e2e72c4f913a593ad0c2f0d0286`, peeled commit `6d2dd585a5d8`, tagger 2025-10-23); `loadDefaultFiles` doc lines 3375–3380 ("configuration file is at `$XDG_CONFIG_HOME/ghostty/config`"), `defaultXdgPath` 3411–3416 (`subdir = "ghostty/config"`), `config-default-files` doc 1987–1990; raw fetch https://raw.githubusercontent.com/ghostty-org/ghostty/v1.2.3/src/config/Config.zig, 339,217 B sha256 `ed2eb047c44c3ad82d4e1e5d23240198e289e8bf34520c444105b4a3008a6e1e` | at v1.2.3 the only XDG default filename upstream used was `config`; the rename to `config.ghostty` is a later change, which is the boundary fact behind finding F1 | mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |

Id note: the assignment text renders the id placeholder as `S###-TBD`. The C2 counter
(`.ufo/waves/round-23/c2/count.py`) indexes the registry with `^\| S\d{3} \|`, so a literal
`-TBD` suffix in the id cell would make the row invisible to the counter. The rows above therefore
carry the concrete ids reserved for this seat (S134–S139 and S150–S151); the integrator may
renumber them.

Shape check run against **counter version 2**'s own logic (`.ufo/waves/round-23/c2/count.py` at
HEAD `4de4464`, whose `source_ok` and row rules were transcribed verbatim into the check): all
eight drafted rows parse as 11 cells with `status = mined`, `opened = 2026-10-22`,
`used-by = corpus/knowledge/terminal-trees-r23.md`, a `source` cell that names *ghostty* as a
whole word, names neither *foot* nor *kitty* as whole words, and carries `ghostty.org` (S134,
S135) or `github.com/ghostty-org/ghostty` (S136–S139, S150, S151); every row's `anchor` cell also
retains the `raw.githubusercontent.com` URL the digest was computed over. All five drafted claim
rows carry `` `ghostty` `` in the first cell, a cell naming `~/.config/ghostty/`, and cite ids
that pass `source_ok`.

**End-to-end check against the real counter.** The lane's own v2 counter was run against these
drafts in a throwaway clone (`git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin
/fast/scratch/hyaku/mado-r23/SrcGhostty/c2check`, checked out at `4de4464`, the eight drafted
SOURCES rows appended to `corpus/SOURCES.md` and the five drafted claim rows written to
`corpus/knowledge/terminal-trees-r23.md`, then committed *in the clone only*):

```
$ python3 -I .ufo/waves/round-23/c2/count.py HEAD
{
 "rev": "HEAD",
 "counter_version": 2,
 "note_present": true,
 "terminals": {
  "foot": [],
  "kitty": [],
  "ghostty": ["S134","S135","S136","S137","S138","S139","S150","S151"]
 },
 "count": "1/3"
}
exit=1
```

The ghostty terminal **counts** under the real v2 counter. The exit status is 1 only because the
foot and kitty seats' rows are absent from that clone; 3/3 requires all three seats' drafts in one
note. Nothing in the lane repo was touched by this check — the clone is a scratch copy under
`/fast/scratch/`, and the lane's `SOURCES.md` and knowledge note are unmodified.

Kind/tier/status shape check: every row is `kind ∈ {docs, code}`, `tier = A`, `status = mined`,
`opened = 2026-10-22`, `recheck = on-release`, `used-by = corpus/knowledge/terminal-trees-r23.md`.
Every row's `source` cell names "ghostty" as a whole word and names neither "foot" nor "kitty",
which is what counter v2's `source_ok` requires. No cell contains `|`.

## 3. Route claims — 5 documentary claims (draft rows for `corpus/knowledge/terminal-trees-r23.md`)

These are the rows the note would carry. **Counter version 2** (`.ufo/waves/round-23/c2/count.py`
at HEAD `4de4464`) requires of each note row: the first cell to be exactly `ghostty` (optionally
backticked); some cell to name the host tree `~/.config/ghostty/`; and at least one cited `S###`
token that resolves to an 11-cell registry row with `status = mined`, `opened = 2026-10-22`, a
`used-by` naming `corpus/knowledge/terminal-trees-r23.md`, and a `source` cell that names *ghostty*
as a whole word, names neither *foot* nor *kitty* as whole words, and points at ghostty's
upstream (`ghostty.org` or `github.com/ghostty-org/ghostty`). The `host tree on this host`
column below is the cell that satisfies the host-tree requirement; the source cells of S136–S139,
S150 and S151 were changed from `raw.githubusercontent.com/…` to the canonical
`github.com/ghostty-org/ghostty/blob/<tag>/…` form so the upstream-pointer test is met, and the
raw URL is retained in each row's `anchor` cell.

**The note file does not yet exist** (`corpus/knowledge/terminal-trees-r23.md` is absent at the
base revision), so the counter is still 0/3 for ghostty until the integrator creates the note with
these rows and registers the SOURCES rows.

| terminal | host tree on this host | claim | upstream route (documentary) | sources | located quote (≤25 words) |
|---|---|---|---|---|---|
| `ghostty` | `~/.config/ghostty/` | **C1 — config file search path and precedence.** The XDG path is `$XDG_CONFIG_HOME/ghostty/`, `XDG_CONFIG_HOME` falls back to `$HOME/.config`; on macOS `$HOME/Library/Application Support/com.mitchellh.ghostty/` is also searched, after all XDG files. | `$XDG_CONFIG_HOME` read as-is when set and non-empty, else `$HOME/.config` (S137); two XDG filenames are consulted, `config.ghostty` and the pre-1.3.0 `config` (S136); upstream loads legacy `config` first, then `config.ghostty` (S138); the documented list and the macOS path (S134); the pre-rename filename at `v1.2.3` (S151). | S134, S136, S137, S138, S151 | S134 `docs/config/index.mdx`:44 — "if **XDG_CONFIG_HOME** is not defined, it defaults to `$HOME/.config`." · S138 `src/config/Config.zig`:3992-3993 — "The legacy `config` file (without extension) is first loaded, then `config.ghostty`." |
| `ghostty` | `~/.config/ghostty/` | **C2 — file name and format.** The file is `config.ghostty` (the extension was added upstream in the 2025-10-12 change "Add `.ghostty` extension to `config` (#8885)"); the format is a custom, very simple `key = value` syntax, lowercase keys, `#` comments on their own line, blank lines ignored, empty value resets to the default, quoted or unquoted values equivalent, and every key is also a CLI flag. | S134 §Syntax; the per-option reference carries the same text (S135). | S134, S135 | S134 `docs/config/index.mdx`:59 — "Ghostty uses a custom, but very simplistic `key = value` syntax." · S134 `docs/config/index.mdx`:44 — "The configuration file is named `config.ghostty` (or `config` before 1.2.3)," |
| `ghostty` | `~/.config/ghostty/` | **C3 — include/import mechanism.** `config-file = <path>` includes another file; it may repeat and may nest; a relative path is resolved against the file that contains the `config-file` key; a leading `?` makes the include optional; a cycle is detected, logged and the file ignored; included files are loaded **after** the file that names them, so an included file's keys override the includer's. | S134 §Splitting into Multiple Files; S135 §`config-file`; S138 `config-file` option doc and `loadRecursiveFiles` (cycle diagnostic at 4216–4222, unique-file guard at 4214). | S134, S135, S138 | S135 `docs/config/reference.mdx`:2494-2495 — "Paths are relative to the file containing the `config-file` directive." · S134 `docs/config/index.mdx`:99-101 — "Note that any `config-file` keys are processed at the _end_ of the current file." · S138 `src/config/Config.zig`:2435-2436 — "Cycles are not allowed. If a cycle is detected, an error will be logged and" |
| `ghostty` | `~/.config/ghostty/` | **C4 — how a running instance reloads.** Two documented upstream routes: the keybinding `ctrl+shift+,` (Linux) / `cmd+shift+,` (macOS), which is the default binding of the `reload_config` action, and a `SIGUSR2` signal handled in-process by the GTK application (and by the macOS app delegate), which performs a hard reload (a new config object) or a soft reload (conditionals re-applied to the already-loaded config). Some options cannot be reloaded at runtime. | S134 §Reloading the Configuration; S138 default keybind table; S139 `handleSigusr2` and `reloadConfig`; S150 the macOS app delegate's own `SIGUSR2` registration, which shows the signal route belongs to ghostty and not to one backend. | S134, S138, S139, S150 | S134 `docs/config/index.mdx`:123-124 — "The configuration can be reloaded at runtime by pressing `ctrl+shift+,` (Linux) or `cmd+shift+,` (macOS)." · S139 `src/apprt/gtk/class/application.zig`:1491 — "received SIGUSR2, reloading configuration" · S150 `macos/Sources/App/macOS/AppDelegate.swift`:550-551 — "reloading configuration in response to SIGUSR2" |
| `ghostty` | `~/.config/ghostty/` | **C5 — no automatic reload and no `SIGHUP`.** Upstream at v1.3.1 watches no config file and installs no `SIGHUP` handler: a treewide sweep of the v1.3.1 tree found `SIGUSR2` only (GTK app, macOS app delegate), `SIGHUP` only where a *child* process is signalled (`src/termio/Exec.zig`, `src/pty.zig`), and zero occurrences of `FileMonitor`, `inotify_init`, `GFileMonitor` or `DispatchSource.makeFileSystemObjectSource`. A reload therefore requires an explicit action (keybind, `reload_config` action, `SIGUSR2`) or a restart. | Negative claim, sweep recorded in §4. | S139 (and the v1.3.1 tree at the same pin) | S139 `src/apprt/gtk/class/application.zig`:1486 — "/// SIGUSR2 signal handler via g_unix_signal_add" (the only config-reload signal the sweep found) |

## 4. Findings for the canonical judge (verbatim conflicts, no adjudication)

Two places where the ghostty.org prose and the pinned upstream source at `v1.3.1` disagree. Both
are reported as found; neither is resolved here.

**(F1) The rename boundary is stated differently by the site and by the source.**
- Site (`docs/config/index.mdx`:38, commit `3755ed6e`): "The configuration file is named `config.ghostty` (or `config` before 1.2.3),"
- Source at `v1.2.3` (S151; `src/config/Config.zig`:3377, digest `ed2eb047c44c3ad82d4e1e5d23240198e289e8bf34520c444105b4a3008a6e1e`): "configuration file is at `$XDG_CONFIG_HOME/ghostty/config`." — and `defaultXdgPath` at `v1.2.3` (`:3414`) still uses `subdir = "ghostty/config"`.
- Source at `v1.3.0` (`src/config/file_load.zig`:18-23, tagger 2026-03-09): the legacy filename is documented as "Ghostty <1.3.0 default path for the XDG home configuration file."
- `src/config/file_load.zig` did not exist at `v1.2.3` (`raw.githubusercontent.com/.../v1.2.3/src/config/file_load.zig` → HTTP 404); the `.ghostty` extension came from upstream commit `cbeb6890c9ec` (2025-10-12, "Add `.ghostty` extension to `config` (#8885)"), which is *before* the `v1.2.3` tagger date (2025-10-23).
- Read: as tagged, the extension became the *default* filename in the `v1.3.0` release, while the site text names `1.2.3`. The two sentences are not reconcilable from the bytes I opened; the source comment "Ghostty <1.3.0" is the upstream statement about the legacy path.

**(F2) The two default filenames are listed by the site in the opposite order from the order upstream loads them.**
- Site (`docs/config/index.mdx`:41-52) lists the XDG paths as `$XDG_CONFIG_HOME/ghostty/config.ghostty` then `$XDG_CONFIG_HOME/ghostty/config`, and says: "If both locations exist, they are loaded in the order above with conflicting values in later files overriding earlier ones." Read in that order, the legacy `config` would override `config.ghostty`.
- Source at `v1.3.1` (`src/config/Config.zig`:3992-3993 and the body of `loadDefaultFiles`, :3994-4012) states the opposite: "The legacy `config` file (without extension) is first loaded, then `config.ghostty`." — and when both exist it logs "both config files `{s}` and `{s}` exist." / "loading them both in that order" (:4004-4005).
- Consequence for the effective precedence on a host holding both names: upstream order makes `config.ghostty` win; the site's ordering, if read literally, makes `config` win. The site list order and the source load order are opposites.

Also recorded, not a conflict: the site's own §File Location text is *inconsistent with itself* about
the legacy name (it calls `config` "before 1.2.3", F1). And the reference page states the
`config-file` layering rule the opposite way round to the prose guide's wording — the guide says
"any keys after a `config-file` key will not override the keys in the loaded file", the reference
says the included file "is loaded after the configuration they're defined within", and both agree
on the outcome (included file wins). Quote for the record, S135 `docs/config/reference.mdx`:2510-2518:
"If "foo" contains `a = 2`, the final value of `a` will be 2, because `foo` is loaded after the
configuration file that configures the nested `config-file` value."

### Host context (read-only, not claimed by this seat)

`pacman -Qi ghostty` → "package 'ghostty' was not found"; `command -v ghostty` → not found; no
`ghostty` binary on PATH. The config tree does exist on this host:
`~/.config/ghostty/config` (1,325 B, sha256 `cb828c044b07d4fd924fe1d6b55c956035feb16f8d5c67899c8a598994596667`)
and `~/.config/ghostty/config.bak.20261003-190229` (1,322 B, sha256
`e47630125605cb19c6b2c9bc33d767a0f3f1b5bf04cd4f36a2bb910897e24f78`). `XDG_CONFIG_HOME` on this host
is `/home/vgpnk/.config`. The live file uses the **legacy** name `config` and begins with
`config-file = ?"~/.config/omarchy/current/theme/ghostty.conf"`. Ownership of the host-side facts
(including the observation that the host file is named `config`, not `config.ghostty`, and that it
uses an optional `?`-prefixed include) belongs to the host scout seat; this seat records them only
as context for the route claims, and asserts no host behaviour. No ghostty process was run, and no
config file was parsed by ghostty.

Relevance to C2, stated as upstream route rather than host behaviour: the host tree is
`~/.config/ghostty/`, which is the XDG directory upstream searches at S136/S138 — but the file
inside it carries the **pre-1.3.0 legacy filename** `config`, not `config.ghostty` (S136
`legacyDefaultXdgPath`, S151 for the pre-rename default). Under the upstream load order recorded at
S138 the legacy file is read first and `config.ghostty` second; on this host only the legacy name
exists. The note's host-tree cell must read `~/.config/ghostty/` to satisfy counter v2's
host-tree requirement, and it does in every drafted claim row.

## 5. Unopened / not established

- `https://ghostty.org/docs/config/reload`, `/docs/config/file`, `/docs/config/include` — **not
  opened; they do not exist** (HTTP 404). The site's own nav exposes only `/docs`,
  `/docs/config`, `/docs/config/reference`, plus non-config pages.
- `https://ghostty.org/sitemap.xml` — **not opened** (HTTP 404).
- GitHub *Releases* API for ghostty returns only one entry (`tip`, a 2022 prerelease); there are
  no GitHub release objects for `v1.3.1`/`v1.3.0`/`v1.2.3` (HTTP 404 on
  `/releases/tags/v1.3.1`). Version identity was therefore taken from the **annotated git tags**
  (`git ls-remote --tags` + the tag objects), not from release notes. No release-note text was read.
- `ghostty-org/ghostty.org` — **does not exist** (GitHub API 404); the site source repo is
  `ghostty-org/website`. It has **no tags**, so website docs are pinned by commit.
- Upstream `CHANGELOG.md` — **not present** at `v1.3.1` (HTTP 404 on `raw.githubusercontent.com`
  and absent from the tarball). The 1.3.0/1.2.3 release-note text was **not opened**.
- The ghostty **man pages** (`$prefix/share/man`, `ghostty.1`/`ghostty.5`) were not read: the
  generated `.scd`/man sources are not shipped in the repository tree (only
  `src/build/mdgen/ghostty_{1,5}_{header,footer}.md` exist); the installed man page is not on this
  host because ghostty is not installed.
- The **macOS** source path was read only to corroborate the `SIGUSR2` reload route
  (`macos/Sources/App/macOS/AppDelegate.swift`:543-551, its own SOURCES row S150). No macOS
  runtime was exercised; macOS claims are documentary only.
- The **kitty** and **foot** sources were not opened by this seat (other seats' scope).

## 6. Out of scope / not done by this seat

- `corpus/SOURCES.md` was **not edited** (rows drafted in §2 only).
- `corpus/knowledge/terminal-trees-r23.md` was **not created or edited**; the claim rows in §3 are
  drafts for the integrator.
- No product code, fixture, expectation, judge, gate, `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`,
  `LOG.md` or `SHONEN.md` was touched. **No git or jj command was run in the lane repo at all**
  and none was run at the fleet root; the lane's corpus files were read only as files.
- No host change: no package installed, no config written, no service touched, no terminal run.
- The C2 counter was **not run against the lane** (it reads committed lane bytes via `git show`,
  and this seat landed neither the registry rows nor the note). It *was* run against these drafts
  in a throwaway clone — see §2 — where the ghostty terminal counts as 1/3. The before/after
  values for the landed corpus are the integrator's to measure.

## 7. Verdict

**Deliverable complete as a draft; nothing landed.** Eight upstream sources for ghostty were opened
and pinned — one ghostty.org configuration guide and one ghostty.org option reference (both pinned
by website-repo commit, with the rendered pages fetched and hashed too), five `v1.3.1` source files
and one `v1.2.3` source file (pinned by annotated git tag with the peeled commit recorded) — every
one with sha256 over bytes that were compared byte-for-byte against the release tarball. These
yield five documentary route claims (search path and precedence, file name and format,
include/import mechanism, reload mechanism, and the absence of automatic reload / `SIGHUP`) plus
eight SOURCES rows in the exact 11-column shape and five drafted claim rows for
`corpus/knowledge/terminal-trees-r23.md`. Two verbatim upstream-vs-site conflicts (F1 rename
boundary, F2 default-file load order) and one negative sweep (C5) are recorded for the canonical
judge. The drafts were then adapted to **C2 counter version 2** (lane HEAD `4de4464`): a
`host tree on this host` cell naming `~/.config/ghostty/` was added to every claim row, and the
six code-row `source` cells were rewritten from `raw.githubusercontent.com/…` to the canonical
`github.com/ghostty-org/ghostty/blob/<tag>/…` form so the upstream-host test passes (the raw URL
is kept in each `anchor` cell, where the digest was actually computed). The lane's own v2 counter,
run against these drafts in a throwaway clone, reports `"ghostty": ["S134"…"S151"]` and
`"count": "1/3"` — the ghostty terminal counts. The landed C2 value stays 0/3 until the integrator
registers these rows and creates the note with all three seats' rows.

source: S123, S124, S125, S126, S127, S128, S129, S130, S131, S133, S134, S135, S136, S137, S138, S139, S140, S141, S142, S143, S144, S145, S146, S147, S148, S149, S150, S151, S152 (kitty v0.49.2 commit b2cb8712: S123-S131, S133; ghostty v1.3.1/v1.2.3 tags and ghostty.org site commits: S134-S139, S150, S151; foot 1.28.0 commit ab33c9a1 and foot wiki commit 2475351a: S140-S149, S152). Each is a corpus/SOURCES.md row opened 2026-10-22 with status mined; S132 stays queued and supports nothing.
verified-at: 2026-10-22; tag- or commit-pinned upstream bytes fetched and hashed by wave-1 seats SrcFoot, SrcKitty, SrcGhostty (reports under .ufo/waves/round-23/w1/reports/); host files read as bytes only (sha256sum, stat) by HostFoot, HostKitty, HostGhostty and re-measured by the L1 at 2026-10-22T11:55Z
recheck: re-fetch each cited row's pinned bytes and compare sha256; re-hash the six host files below; `command -v foot kitty ghostty` and `pacman -Q foot kitty ghostty` (read-only); no terminal, launcher, signal, package transaction or compositor action
surface: P4
scope: the foot, kitty and ghostty config trees on this host (documentary upstream route plus host declaration); Alacritty stays in terminal-route-r17.md

# Terminal trees foot, kitty and ghostty — documentary route, not observed behaviour

Round 17 sourced only the Alacritty route (`terminal-route-r17.md:5`, `:17`) and the corpus
frontier said "foot, kitty and ghostty trees remain unsourced" (`corpus/README.md:123-124`).
This note supplies the version-pinned upstream contract for the other three trees and joins it to
this host's bytes. Its main host fact is negative: none of the three terminals is installed, so
each tree is a declared file with no consumer today. Nothing here was run: no terminal was
started, signalled or reloaded.

## Upstream contract

Pins: foot `1.28.0` (tag object `3d97bba5`, peeled commit `ab33c9a19d626f8d0ac0bd1adfdba21946ada948`);
kitty `v0.49.2` (tag object `e3005973`, peeled commit `b2cb871254fbdac19a085188813c8dfb258b95cd`,
released 2026-10-01); ghostty `v1.3.1` (tag object `22efb0be`, peeled commit
`332b2aefc6e72d363aa93ab6ecfc86eeeeb5ed28`) plus `v1.2.3` for the file-rename boundary. These are
current upstream releases, not host versions: no host binary exists to compare against.

### foot

| terminal | host tree | claim | evidence (pinned at foot 1.28.0) | sources | bound |
|---|---|---|---|---|---|
| `foot` | `~/.config/foot/` | foot reads its configuration from `XDG_CONFIG_HOME/foot/foot.ini` (defaulting to `$HOME/.config/foot/foot.ini`) and then `XDG_CONFIG_DIRS/foot/foot.ini` (defaulting to `/etc/xdg/foot/foot.ini`), in that order; the first existing file is used, the two are not merged, and `--config=PATH` bypasses the search | `doc/foot.ini.5.scd:14-20` § DESCRIPTION; `config.c:421-473` (`open_config`), `config.c:3712-3723` | S140, S145 | documented and implemented order at one tag; the host-tree cell names the tree this row routes, it is not a claim that this host's file was read |
| `foot` | `~/.config/foot/` | the config file is named `foot.ini`; it uses the standard unix configuration format with section-based KEY=VALUE pairs, an unnamed default section that may be written as `[main]`, `#` line comments, and no empty values except a quoted empty string for string options | `doc/foot.ini.5.scd:9-33` § DESCRIPTION; `foot.ini:1-5,110,198` (shipped template) | S140, S144, S145 | static format facts at the pinned tag; a trailing `#` comment after a value is accepted by the parser but only implicit in the docs |
| `foot` | `~/.config/foot/` | the `[main]` section accepts an `include` key that imports another config file; the path must be absolute or start with `~/`, one path per directive, multiple directives and nested imports are allowed, and the imported file has its own section scope so the including file returns to the default section afterwards | `doc/foot.ini.5.scd:110-121` § SECTION main `include`; `config.c:909-945` | S140, S145 | parser-level facts at the pinned tag; whether any host foot.ini uses an include is a host claim outside this row |
| `foot` | `~/.config/foot/` | a running foot cannot reload its configuration: the config is parsed once at startup, SIGHUP is explicitly ignored, the only handled signals (SIGUSR1, SIGUSR2) switch the colour theme, and there is no reload keybinding or file watch; upstream's own answer is to restart foot, and in server mode to restart the server | `main.c:539-540,675-687`; `doc/foot.1.scd:700-712` § Signals; `terminal.c:3816-3831` (`spawn-terminal` execs a new `foot --config <path>`); wiki `Home.md:1011-1015` | S141, S146, S147, S149 | documented and coded at the pinned tag; the wiki page is pinned at its own 2025-12-28 commit, not at the tag, and its `[colors]`/`[colors2]` spelling is stale for 1.28.0; no signal was sent and no restart was performed |
| `foot` | `~/.config/foot/` | `foot --check-config` validates a config and exits 0 or 230 without starting a terminal; in server mode the config is parsed once by the server and every client terminal inherits that parsed config, so an edited foot.ini reaches a running foot only through a new process that re-reads it | `doc/foot.1.scd:33-35` § OPTIONS, :103-112; `config.c:3501-3506,3712-3723`; `server.c:369-392`; `terminal.c:3816-3831` | S141, S145, S146, S148 | documented and coded at the pinned tag; `--check-config` was not run here — no foot binary is installed on this host |

### kitty

| terminal | host tree | claim | evidence (pinned at kitty v0.49.2) | sources | bound |
|---|---|---|---|---|---|
| `kitty` | `~/.config/kitty/` | kitty reads its configuration file `kitty.conf` from the OS config directory; the search order is `$XDG_CONFIG_HOME/kitty/kitty.conf`, `~/.config/kitty/kitty.conf`, `$XDG_CONFIG_DIRS/kitty/kitty.conf` and the first existing file is used, while `KITTY_CONFIG_DIRECTORY` replaces the search and `/etc/xdg/kitty/kitty.conf` is merged with lower priority than any user file | `kitty/simple_cli_definitions.py:366-370`; `kitty/launcher/utils.h:202-244`; `kitty/cli.py:716` | S124, S125, S130 | documented and implemented order at one tag; the C code selects a directory (kitty.conf must exist inside it and it must be writable); not a host fact |
| `kitty` | `~/.config/kitty/` | the config file format is one `option value` per line, `#` at line start is a comment, a leading `\` continues a line, and the file is named `kitty.conf` inside the kitty config directory | `docs/conf.rst:26-37`; `kitty/conf/utils.py:24`; `kitty/constants.py:130` (`defconf`) | S123, S126, S133 | static format facts at the pinned tag; unknown keys are logged and ignored |
| `kitty` | `~/.config/kitty/` | secondary config files are pulled in with `include`, `globinclude`, `envinclude` and `geninclude`; a relative include resolves against the directory of the including file and a missing included file is logged and ignored rather than fatal | `docs/conf.rst:39-63`; `kitty/conf/utils.py:295-355` | S123, S126 | parser-level facts at the pinned tag; whether any host kitty.conf uses includes is a host claim outside this row |
| `kitty` | `~/.config/kitty/` | a running kitty reloads its config three ways: automatic reload on change (`auto_reload_config`, default 0.1 s debounce, only when kitty.conf existed at startup), the default keybind `kitty_mod+f5` (`ctrl+shift+f5`, kitty_mod defaults to ctrl+shift) bound to `reload_config_file`, or the `SIGUSR1` signal, whose handler calls the `load_config_file` boss action | `docs/conf.rst:19-23`; `kitty/options/definition.py:3090-3101,3650-3651,4694`; `kitty/child-monitor.c:1708,640` | S123, S127, S128 | documented and coded routes at the pinned tag; no signal was sent and no reload was exercised |
| `kitty` | `~/.config/kitty/` | the remote-control command `kitten @ load-config` reloads a specified `kitty.conf` in a running kitty; with no paths the previously specified file is reloaded, the paths must be readable by that kitty process, and relative paths resolve against its config directory | `kitty/rc/load_config.py:31-40` | S129 | command contract at the pinned tag; remote control was not enabled or invoked |

### ghostty

| terminal | host tree on this host | claim | upstream route (documentary) | sources | located quote (≤25 words) |
|---|---|---|---|---|---|
| `ghostty` | `~/.config/ghostty/` | **C1 — config file search path and precedence.** The XDG path is `$XDG_CONFIG_HOME/ghostty/`, `XDG_CONFIG_HOME` falls back to `$HOME/.config`; on macOS `$HOME/Library/Application Support/com.mitchellh.ghostty/` is also searched, after all XDG files. | `$XDG_CONFIG_HOME` read as-is when set and non-empty, else `$HOME/.config` (S137); two XDG filenames are consulted, `config.ghostty` and the pre-1.3.0 `config` (S136); upstream loads legacy `config` first, then `config.ghostty` (S138); the documented list and the macOS path (S134); the pre-rename filename at `v1.2.3` (S151). | S134, S136, S137, S138, S151 | S134 `docs/config/index.mdx`:44 — "if **XDG_CONFIG_HOME** is not defined, it defaults to `$HOME/.config`." · S138 `src/config/Config.zig`:3992-3993 — "The legacy `config` file (without extension) is first loaded, then `config.ghostty`." |
| `ghostty` | `~/.config/ghostty/` | **C2 — file name and format.** The file is `config.ghostty` (the extension was added upstream in the 2025-10-12 change "Add `.ghostty` extension to `config` (#8885)"); the format is a custom, very simple `key = value` syntax, lowercase keys, `#` comments on their own line, blank lines ignored, empty value resets to the default, quoted or unquoted values equivalent, and every key is also a CLI flag. | S134 §Syntax; the per-option reference carries the same text (S135). | S134, S135 | S134 `docs/config/index.mdx`:59 — "Ghostty uses a custom, but very simplistic `key = value` syntax." · S134 `docs/config/index.mdx`:44 — "The configuration file is named `config.ghostty` (or `config` before 1.2.3)," |
| `ghostty` | `~/.config/ghostty/` | **C3 — include/import mechanism.** `config-file = <path>` includes another file; it may repeat and may nest; a relative path is resolved against the file that contains the `config-file` key; a leading `?` makes the include optional; a cycle is detected, logged and the file ignored; included files are loaded **after** the file that names them, so an included file's keys override the includer's. | S134 §Splitting into Multiple Files; S135 §`config-file`; S138 `config-file` option doc and `loadRecursiveFiles` (cycle diagnostic at 4216–4222, unique-file guard at 4214). | S134, S135, S138 | S135 `docs/config/reference.mdx`:2494-2495 — "Paths are relative to the file containing the `config-file` directive." · S134 `docs/config/index.mdx`:99-101 — "Note that any `config-file` keys are processed at the _end_ of the current file." · S138 `src/config/Config.zig`:2435-2436 — "Cycles are not allowed. If a cycle is detected, an error will be logged and" |
| `ghostty` | `~/.config/ghostty/` | **C4 — how a running instance reloads.** Two documented upstream routes: the keybinding `ctrl+shift+,` (Linux) / `cmd+shift+,` (macOS), which is the default binding of the `reload_config` action, and a `SIGUSR2` signal handled in-process by the GTK application (and by the macOS app delegate), which performs a hard reload (a new config object) or a soft reload (conditionals re-applied to the already-loaded config). Some options cannot be reloaded at runtime. | S134 §Reloading the Configuration; S138 default keybind table; S139 `handleSigusr2` and `reloadConfig`; S150 the macOS app delegate's own `SIGUSR2` registration, which shows the signal route belongs to ghostty and not to one backend. | S134, S138, S139, S150 | S134 `docs/config/index.mdx`:123-124 — "The configuration can be reloaded at runtime by pressing `ctrl+shift+,` (Linux) or `cmd+shift+,` (macOS)." · S139 `src/apprt/gtk/class/application.zig`:1491 — "received SIGUSR2, reloading configuration" · S150 `macos/Sources/App/macOS/AppDelegate.swift`:550-551 — "reloading configuration in response to SIGUSR2" |
| `ghostty` | `~/.config/ghostty/` | **C5 — no automatic reload and no `SIGHUP`.** Upstream at v1.3.1 watches no config file and installs no `SIGHUP` handler: a treewide sweep of the v1.3.1 tree found `SIGUSR2` only (GTK app, macOS app delegate), `SIGHUP` only where a *child* process is signalled (`src/termio/Exec.zig`, `src/pty.zig`), and zero occurrences of `FileMonitor`, `inotify_init`, `GFileMonitor` or `DispatchSource.makeFileSystemObjectSource`. A reload therefore requires an explicit action (keybind, `reload_config` action, `SIGUSR2`) or a restart. | Negative claim, sweep recorded in §4. | S139 (and the v1.3.1 tree at the same pin) | S139 `src/apprt/gtk/class/application.zig`:1486 — "/// SIGUSR2 signal handler via g_unix_signal_add" (the only config-reload signal the sweep found) |

Two upstream-versus-site conflicts are kept, not resolved (SrcGhostty §4): the site says the
legacy file name `config` applied "before 1.2.3", while upstream source dates it to "Ghostty <1.3.0";
and the site lists `config.ghostty` first, while upstream loads the legacy `config` first and
`config.ghostty` second.

## Host declaration

| terminal | host tree | files (bytes, sha256) | relation to omarchy default | consumer on this host |
|---|---|---|---|---|
| foot | `~/.config/foot/` | `foot.ini` 516 B `3e88354476f2682e…`; `foot.ini.bak.20261003-190229` 513 B `8afc9646c61e58e6…` | backup is byte-identical to omarchy's shipped default; live file differs by one font line | none: no binary on PATH, `pacman -Q foot` not found, no process |
| kitty | `~/.config/kitty/` | `kitty.conf` 954 B `f875291ecfe64ebc…`; `kitty.conf.bak.20261003-190229` 953 B `95eed20aaedb0962…` | backup is byte-identical to omarchy's shipped default; live file differs in `font_size` | none: no binary on PATH, `pacman -Q kitty` not found, no process |
| ghostty | `~/.config/ghostty/` | `config` 1325 B `cb828c044b07d4fd…`; `config.bak.20261003-190229` 1322 B `e47630125605cb19…` | backup is byte-identical to omarchy's shipped default (omarchy 3.8.3 checkout); live file differs only in `font-size` | none: no binary on PATH, `pacman -Q ghostty` not found, no process |

The selection chain from round 17 still resolves away from all three: `~/.config/xdg-terminals.list`
names only `Alacritty.desktop`, and the live clients are Alacritty (HostGhostty: `hyprctl -j clients`
read-only, 2 Alacritty clients). All three backups and font edits share one timestamp,
2026-10-03 19:02:29 (`[INFERENCE]` one scripted pass; the writer is not identified).

## Safe observation

Read-only checks that re-derive the host column: `sha256sum` and `stat -c '%n %s'` on the six files;
`command -v foot kitty ghostty` (exit 1, nothing found); `pacman -Q foot kitty ghostty` (three
"not found"); `grep -v '^#' ~/.config/xdg-terminals.list` (`Alacritty.desktop`). L1 re-ran these at
2026-10-22T11:55Z with the values above.

## Unexercised behavior

- `[UNK]` Whether any of the three would read its tree as documented: no binary exists, so the
  upstream search paths are contract, not observation.
- `[UNK]` Reload effects: foot has no runtime reload (S146), kitty reloads by `auto_reload_config`,
  `ctrl+shift+f5` or SIGUSR1 (S127, S128), ghostty by `ctrl+shift+,` or SIGUSR2 (S138, S139). None
  was exercised; installing a terminal or sending a signal is operator-owned.
- `[UNK]` Whether foot would be selected even if installed: ScoutSkillTerminal found both foot desktop
  entries carry `Hidden=true`, which the round-17 resolver honours (S057); not re-derived here.
- `[UNK]` Which tool wrote the 2026-10-03 backups.

## Supersedes

This note supersedes, for these three trees only, "foot, kitty and ghostty trees are not sourced
here" (`terminal-route-r17.md:5`) and the frontier clause at `corpus/README.md:123-124`. It also
narrows `terminals-and-omarchy.md` §8 unknown (1): the three binaries are absent from pacman as well
as from PATH. Older notes are not edited.

## Errata (round 23 wave 2, append-only)

- Host declaration said "2 Alacritty clients" (HostGhostty's undated read). ReviewNoteHost read
  `hyprctl -j clients` at 11:57Z and 12:00Z: 1 client, class Alacritty. The class claim stands; the
  count is a moving session value, not a fact of this note.
- "omarchy 3.8.3 checkout": the checkout's `version` file says 3.8.3 while its HEAD is the commit
  tagged v3.8.4. The three terminal defaults are byte-identical at both tags, so the byte claim holds.
- "L1 re-ran these at 2026-10-22T11:55Z" had no receipt. The re-measured values are reproduced with
  receipts in `.ufo/waves/round-23/w2/reports/ReviewNoteHost.md` (11:57–12:01Z).
- The ghostty C5 row says the treewide sweep is "recorded in §4"; this note has no §4. The sweep
  command and result are in `.ufo/waves/round-23/w1/reports/SrcGhostty.md` §1.2 and §3; no
  wave-2 seat re-ran it, so C5 (no watcher, no SIGHUP handler) rests on that single sweep.

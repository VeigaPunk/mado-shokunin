source: S072 https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/README.md (Dependencies, Usage, Config); S073 https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/resources/config.toml (default table); S074 https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/config.rs (Walker::new, load, get_config); S075 https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/main.rs (init_ui, handle_command_line, activate, listen_activation_socket); S076 https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/data.rs (init_socket, handle_disconnect); S077 https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/src/theme/mod.rs (setup_themes, cross-ref P5); S078 https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/Cargo.toml (version, notify dependency); S079 https://codeload.github.com/abenz1267/walker/tar.gz/refs/tags/v2.17.2 (whole-tree grep for notify, watch, reload); S080 https://raw.githubusercontent.com/abenz1267/elephant/v2.22.1/README.md (Usage, Configuration); S081 https://raw.githubusercontent.com/abenz1267/elephant/v2.22.1/internal/comm/comm.go (init, StartListen); S082 https://raw.githubusercontent.com/abenz1267/elephant/v2.22.1/cmd/elephant/elephant.go (--config flag, generate config, service unit path); S083 https://raw.githubusercontent.com/abenz1267/elephant/v2.22.1/pkg/common/config.go (LoadGlobalConfig, LoadConfig); S098 https://static.crates.io/crates/xdg/xdg-3.0.0.crate (src/base_directories.rs:446-457 find_config_file, :308-310/:321-323 XDG defaults; round-19 re-point, see the correction block); S085 https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/config/walker/config.toml (stock user config); S086 https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-launch-walker (launcher); S087 https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-restart-walker (restart); S088 https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-refresh-walker (refresh); S089 https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/default/walker/walker.desktop (autostart entry, restart drop-in); S090 /var/log/pacman.log (host version binding, lines 1943, 2929, 3062, 3095, 3123; file bytes only); S091 host walker file bytes (~/.config/walker/config.toml, /etc/xdg/walker/config.toml, /usr/bin/walker; sha256 in § Host declaration)
verified-at: 2026-10-20; upstream tags resolved by `git ls-remote` (walker v2.17.2 = a515085f…, elephant v2.22.1 = 8f1e21d6…, omarchy v3.8.4 = 8fcc9d60…, all lightweight); every raw body curl-fetched with a receipt in .ufo/waves/round-18/fetch/NoteWalker/receipts.jsonl; host bytes read with cat/sha256sum/stat/grep only; nothing executed
recheck: re-run the `git ls-remote` tag lines, compare each body's sha256 with its receipt, re-fetch the codeload tarball and re-grep for `notify`, host files in § Host declaration by sha256sum and line anchors, the tail of /var/log/pacman.log for walker and elephant; no walker, elephant, omarchy-*, systemctl, journalctl, pacman, pidof or hyprctl
surface: P3

# P3 walker and elephant — documentary route

Documentary route only. The upstream contract and the host file bytes below are
read, not observed: no walker or elephant process was started, no socket was
connected, no launcher was opened, and no running state on the host is claimed.
Unobserved behaviour is listed in § Unexercised behavior. Companion notes:
`corpus/knowledge/walker-deep-r9.md` and `corpus/knowledge/walker-live-surface.md`
(both measured 2026-10-14 against walker 2.17.0; see § Host declaration for the
binding that now supersedes their binary and packaged-config pins). The P3
runtime snapshot in `corpus/knowledge/waybar-walker-plane.md` is not re-run here.

Anchor keys used below (file lines unless marked):

| key | source | version | anchor form |
|---|---|---|---|
| WR | https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/README.md | walker v2.17.2 (tag) | `WR:n` = file line |
| WC | …/walker/v2.17.2/resources/config.toml | walker v2.17.2 | `WC:n` = file line (13,743 B, byte-equal to host `/etc/xdg` file) |
| WS | …/walker/v2.17.2/src/config.rs | walker v2.17.2 | `WS:n` |
| WM | …/walker/v2.17.2/src/main.rs | walker v2.17.2 | `WM:n` |
| WD | …/walker/v2.17.2/src/data.rs | walker v2.17.2 | `WD:n` |
| WT | …/walker/v2.17.2/src/theme/mod.rs | walker v2.17.2 | `WT:n` |
| WK | …/walker/v2.17.2/Cargo.toml | walker v2.17.2 | `WK:n` |
| WX | https://codeload.github.com/abenz1267/walker/tar.gz/refs/tags/v2.17.2 | walker v2.17.2 tree (165,438 B) | whole-tree `grep`, no line anchor; `WX:` names the search |
| ER | https://raw.githubusercontent.com/abenz1267/elephant/v2.22.1/README.md | elephant v2.22.1 (tag) | `ER:n` |
| EC | …/elephant/v2.22.1/internal/comm/comm.go | elephant v2.22.1 | `EC:n` |
| ED | …/elephant/v2.22.1/cmd/elephant/elephant.go | elephant v2.22.1 | `ED:n` |
| EG | …/elephant/v2.22.1/pkg/common/config.go | elephant v2.22.1 | `EG:n` |
| XD | https://docs.rs/xdg/latest/xdg/struct.BaseDirectories.html | xdg crate docs page, saved HTML (105,537 B) | `XD:n` = saved-HTML line |
| OC | https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/config/walker/config.toml | omarchy checkout tag v3.8.4 | `OC:n` = file line |
| OL / OR / OF | …/omarchy/v3.8.4/bin/omarchy-launch-walker / -restart-walker / -refresh-walker | omarchy v3.8.4 | `OL:n`, `OR:n`, `OF:n` |
| OD | …/omarchy/v3.8.4/default/walker/walker.desktop and restart.conf | omarchy v3.8.4 | `OD:n` |
| HP | `/var/log/pacman.log` | host, read as bytes | `HP:n` = log line |

Tag resolution: `git ls-remote https://github.com/abenz1267/walker refs/tags/v2.17.2`
returns `a515085f…` (no peeled line, so the tag is lightweight); elephant
`refs/tags/v2.22.1` returns `8f1e21d6…`; omarchy `refs/tags/v3.8.4` returns
`8fcc9d60…`. The omarchy checkout's `.git/packed-refs` carries
`refs/heads/master` and `refs/tags/v3.8.4` at the same `8fcc9d60…`, so the
checkout is at the tag (read as bytes, no git command run in it).

## Upstream contract

### What walker needs and how it starts

- Walker is a GTK4 and Rust launcher: "built with GTK4 and Rust" [WR:3]; package
  version `2.17.2` [WK:2-3].
- Elephant is a hard runtime dependency: "make sure elephant is running before
  starting Walker" [WR:59]. In source, `which("elephant")` is consulted at
  start [WM:124-126]; when elephant is absent and the call is not dmenu, walker
  prints "Please install elephant." and exits 1 [WM:670-674].
- Service mode is the documented fast path: `walker --gapplication-service`
  [WR:167-171]. A non-service, non-dmenu invocation without a running service
  prints "make sure 'walker --gapplication-service' is running!" [WM:802-803].
  Source-side: `--gapplication-service` is read as `ApplicationFlags::IS_SERVICE`
  [WM:104-105, 782]. Its help text is the 2.17.0 measurement in
  `walker-live-surface.md` §2; it is not re-measured here.
- Client forms: plain `walker` [WR:173-177], or a raw socket call "for an even
  faster launch" [WR:179-182] with the stated limit "it does not handle any
  commandline options" [WR:185]. `-q/--close` is handled before any service
  check: when not a service and `--close` is present the process exits 0
  [WM:784-786]; when visible and `close_when_open` is set the activation closes
  it [WM:635-642].

### Config discovery and layering (walker)

- Documented location: "Configuration should be done in `~/.config/walker`."
  [WR:213]; the default config is linked at [WR:215].
- Source: `Walker::new()` first deserialises the embedded default
  (`DEFAULT_CONFIG = include_str!("../resources/config.toml")`) [WS:8, 212-216].
  It then finds the user file with
  `xdg::BaseDirectories::with_prefix("walker").find_config_file("config.toml")`
  [WS:218-219]. The crate documents the search as "Searches `XDG_CONFIG_HOME`
  and then `XDG_CONFIG_DIRS`" [XD:356-358]; `XDG_CONFIG_HOME` defaults to
  `$HOME/.config` [XD:302] and `XDG_CONFIG_DIRS` to `/etc/xdg` [XD:306]. The
  first hit wins, so `/etc/xdg/walker/config.toml` is read only when no user file
  exists (INF from that search order; the path is never named by walker itself).
- Layers, in code order: embedded default, then the user file merged through
  `PartialWalker` [WS:221-226, 245 onward], then an environment overlay built as
  `config::Environment::with_prefix("WALKER").separator("_")` [WS:234-239]. The
  overlay is applied only if it deserialises into `PartialWalker` [WS:238].
- Failure modes in code: a user file that fails `Config::builder().build()`
  (syntax level) returns through `?` at [WS:221-223]; `load()` is then unwrapped
  at `WM:108`, so the process panics (INF from code; not exercised). A user file
  that builds but fails `try_deserialize` is non-fatal: `set_error(...)` and
  `println!` run, and the defaults stay in place [WS:225-231].
- Read once: `config::load()` runs inside `init_ui` [WM:108]; the result sits in
  `static LOADED_CONFIG: OnceLock<Walker>` [WS:7] and `load()` sets it once,
  failing with "Failed to set loaded config" on a second set [WS:586-589];
  `get_config()` expects it [WS:592-594]. Source-side this is a read-once
  process model. The tag tree contains no `notify::` or `use notify` (see the
  next bullet), no `reload_config` or `set_config` function, and only three
  `connect_changed` handlers in `src/`: the GSettings `color-scheme` and
  `accent-color` keys [WM:142, 149] and the search entry [ui/window.rs:479].
- Dependency declared but unused in `src/`: `notify = "8.2.0"` [WK:21]. A whole-tree
  search of the tag tarball [WX] finds `notify` only in the `Cargo.lock` entry for
  the `notify` crate (its dependency list includes `inotify`) and as closure
  parameter names in `src/niri.rs:160-213`; no `notify::` path, no `use notify`,
  no `inotify` call in `src/`. Whether any other path watches files is `[UNK]`
  for code the textual search did not match.
- Environment overlay semantics: the prefix and separator are declared [WS:235];
  which field names are reachable through `WALKER_*` (underscore-bearing keys
  such as `additional_theme_location`) is not exercised. The name-census part of
  the question is in § Unexercised behavior.
- Packaged default, upstream v2.17.2 (values read from `WC`): `close_when_open =
  true` [WC:2], `as_window = false` [WC:4], `selection_wrap = false` [WC:6],
  `theme = "default"` [WC:9], `resume_last_query = false` [WC:18], `[columns]
  "symbols" = 3` [WC:37-38], `[providers] default = [...]` [WC:58-66],
  `max_results = 50` [WC:67], and a ten-entry prefix table [WC:75-113] with
  `;` → providerlist, `>` → runner, `/` → files, `.` → symbols, `!` → todo,
  `%` → bookmarks, `=` → calc, `@` → websearch, `:` → clipboard, `$` → windows.

### Theme and file locations touched by the walker config (cross-ref P5)

- `setup_themes` collects `find_config_files("themes")` [WT:56] and then appends
  `additional_theme_location` with `~` replaced by `$HOME` via
  `a.replace("~", &home)` [WT:60-63]. The replacement is a literal substring
  replace, not a shell expansion. A missing `default` theme falls back to the
  compiled theme [WT:132-135]. Theme contents are the P5 route's subject and are
  not inspected further here.

### Elephant contract (IPC and config)

- Socket: walker connects to `$XDG_RUNTIME_DIR/elephant/elephant.sock` (fallback
  `env::temp_dir()`) [WD:156-161, 169]. Elephant listens on the same path:
  `filepath.Join(rd, "elephant", "elephant.sock")` [EC:38-44], creating the
  parent directory with mode 0755 [EC:47]. Without `XDG_RUNTIME_DIR` elephant logs
  "XDG_RUNTIME_DIR not set. falling back to /tmp" and uses `os.TempDir()` [EC:40-42].
- Drift: the elephant README says the socket is "typically at `/tmp/elephant.sock`"
  [ER:211]. The v2.22.1 source does not use `/tmp/elephant.sock` on the XDG path;
  the README line is stale for this tag.
- Walker reconnects after a socket error: `handle_disconnect` sets the state and
  spawns a retry loop around `init_socket` [WD:653-660].
- Config layout, as documented: `~/.config/elephant/` holding `elephant.toml`,
  `.env`, and `<provider>.toml` [ER:183-189]; `elephant generatedoc` documents
  each provider [ER:192-194]; `elephant --config /path/to/config` selects another
  directory [ER:140-141]. Source: the `--config` flag calls
  `common.SetExplicitDir(val)` [ED:299-305]; the main command calls
  `common.LoadGlobalConfig()` [ED:325]; `generate config` writes a provider
  config [ED:177-187].
- Global config: `LoadGlobalConfig` loads `LoadConfig("elephant", ...)` [EG:41-48]
  into `ElephantConfig` with `provider_hosts`, `auto_detect_launch_prefix`,
  `launch_prefix`, `git_on_demand` and `before_load` [EG:28-36]. A missing user
  file logs "using default config" and returns [EG:85-89]; a parse error logs and
  exits 1 [EG:93-96].
- Service: `elephant service enable/disable` manages `~/.config/systemd/user/elephant.service`
  [ER:177-178, 129]; the unit path is `xdg.ConfigHome/systemd/user/elephant.service`
  [ED:46-47, 94-95]. ER:123 warns that the process "needs to run with the users environment".

### Omarchy launch, restart and refresh (v3.8.4 bytes)

- Launcher `omarchy-launch-walker`: starts elephant under `setsid uwsm-app --
  elephant &` if `pgrep -x elephant` is empty [OL:5-7]; starts
  `walker --gapplication-service` under `uwsm-app` with `GSK_RENDERER=cairo` when
  `pgrep -f` finds none [OL:10-12]; then `exec walker --width 644 --maxheight 300
  --minheight 300 "$@"` [OL:14].
- Restart `omarchy-restart-walker`: restarts `elephant.service` when enabled
  [OR:6-8]; restarts `app-walker@autostart.service` when enabled, else prints
  "Unable to restart Walker -- RESTART MANUALLY" [OR:10-14]. As root it re-runs the
  restart under `systemd-run --uid` with `XDG_RUNTIME_DIR` set [OR:17-21].
- Refresh `omarchy-refresh-walker`: copies the autostart entry and the restart
  drop-in [OF:5-10], refreshes `walker/config.toml` and two elephant files through
  `omarchy-refresh-config` [OF:15-17], links `default/elephant/*.lua` into
  `~/.config/elephant/menus` [OF:20-23], then calls `omarchy-restart-walker` [OF:26].
- Autostart entry: `Exec=walker --gapplication-service` [OD:4].
- Stock user config `OC` is the same 49-line file the host carries (see § Host
  declaration).

## Host declaration

Host bytes read with `sha256sum`, `stat`, `cat -n` or the grep tool. Paths are
under `/home/vgpnk` unless absolute. Anchors are file lines.

| file | sha256 | bytes / lines | vs. upstream v2.17.2 / v3.8.4 |
|---|---|---|---|
| `~/.config/walker/config.toml` | `fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787` | 1,336 / 49 | equal to `OC` (sha equal) |
| `~/.local/share/omarchy/config/walker/config.toml` | `fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787` | 1,336 / 49 | equal to `OC` |
| `/etc/xdg/walker/config.toml` | `3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b` | 13,743 / 305; mtime 2026-10-08 11:14:32 -0300 | equal to `WC` (sha equal) |
| `/usr/bin/walker` | `25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096` | 7,039,912; mtime 2026-10-08 11:14:32 -0300 | identity to tag bytes `[UNK]` |
| `~/.config/autostart/walker.desktop` | `5cb9874eedbcb32c7b121ea60f6433f881499247cac7e6473a9a93adeebc3aa7` | 138 | equal to `OD` |
| `~/.config/systemd/user/app-walker@autostart.service.d/restart.conf` | `de0f70294000bc29f5876ea195db127f74060ac990aad5a129eeb72c98b15433` | 38 | equal to `OD` restart.conf |
| `~/.local/share/omarchy/bin/omarchy-launch-walker` | `fd9e93f830bc228610df15d754136e066ee920fea5f20817aa93e65d5a1d81d8` | 412 | equal to `OL` |
| `~/.local/share/omarchy/bin/omarchy-restart-walker` | `9ac82d0c1370ec19f59c8347716036765d3335d348feaec4c9581e2ca3bf8174` | 709 | equal to `OR` |
| `~/.local/share/omarchy/bin/omarchy-refresh-walker` | `05cd9c672252fd17d2a2c6d699a7e59ed1cd81c0c873abb1a6c6bd45c093f9a2` | 893 | equal to `OF` |

- `~/.config/walker/config.toml` (user, `OC`-equal): `force_keyboard_focus = true`
  [:1]; `selection_wrap = true` [:2]; `theme = "omarchy-default"` [:3];
  `additional_theme_location = "~/.local/share/omarchy/default/walker/themes/"`
  [:4]; `hide_action_hints = true` [:5]; `[keybinds] quick_activate = []`
  [:10-11]; `[columns] symbols = 1` [:13-14]; `[providers] max_results = 256`
  [:16-17]; `default = [desktopapplications, websearch]` [:18-21]; six
  `[[providers.prefixes]]` tables [:23-45]; `[[emergencies]]` with
  `text = "Restart Walker"` and `command = "omarchy-restart-walker"` [:47-49].
  Its prefix table differs from upstream [WC:75-113]; whether an array in the user
  file replaces or merges with the packaged array is `[UNK]` (the merge body
  `WS:245-` was not read line by line).
- `/etc/xdg/walker/config.toml` is byte-equal to the upstream `resources/config.toml`
  at v2.17.2 (sha `3c5c6867…`). Walker's L0 layer is the embedded default (`WS:8`),
  not this file; the packaged file would be read only through the XDG search when no
  user file exists (`XD:356-358`), which is not the case on this host.
- `/usr/bin/walker`: the embedded default config is present exactly once, at file
  offset 806,960, and the bytes `b[806960:806960+13743]` equal the `/etc/xdg` file
  (`python3` byte read, `True`). The binary also carries one bare `WALKER_` literal,
  followed by the rodata run `config not initialized` (rodata has no separators;
  the literal boundary is not established).
- Elephant config directory `~/.config/elephant/`: `calc.toml` (14 B),
  `desktopapplications.toml` (62 B), `symbols.toml` (81 B), `menus/` (directory);
  no `elephant.toml` is present, so `EG:85-89` applies to the global config `[INF]`
  (also requires no `--config` override and no `elephant/` under the running
  process's `XDG_CONFIG_DIRS`; `ProviderConfig` lookup not read — CriticC2W2 D2).
- Omarchy checkout `~/.local/share/omarchy`: `.git/HEAD` = `ref: refs/heads/master`;
  `packed-refs` maps `refs/heads/master` and `refs/tags/v3.8.4` to `8fcc9d60…`
  (equal to the upstream tag); `FETCH_HEAD` names `branch 'master' of .` at the same
  commit. The three `bin/` scripts and two `default/walker` files equal their tag
  bytes (table above).

### Host version binding (file read of `/var/log/pacman.log`, no package query)

- `HP:1943` (2026-10-11T16:14:39-0300): `upgraded walker (2.16.2-1 -> 2.17.0-1)`.
- `HP:2929` (2026-10-20T09:16:46-0300): `upgraded walker (2.17.0-1 -> 2.17.2-1)`.
  The tag `v2.17.2` carries `version = "2.17.2"` [WK:3]; the host pkgver therefore
  matches the tag. Arch packaging patches are `[UNK]`.
- `HP:3062` (09:18:25) and `HP:3123` (09:31:04): `running 'walker-restart.hook'`.
- `HP:3095` (2026-10-20T09:31:03-0300): `upgraded elephant (2.21.0-1 -> 2.22.1-1)`,
  matching the v2.22.1 tag. Elephant `-debug` packages from the same run are
  removed at `HP:3132-3147`.
- A log line is not a running-binary fact. The process state after the 09:18 and
  09:31 restart hooks is `[UNK]` (no process probe, by constraint).

### MOVED pins against the 2026-10-14 notes (recorded, not edited here)

Per the S015 protocol, these moved pins are reported with old and new values.
The older notes are not edited in this round.

- `/etc/xdg/walker/config.toml`: `walker-deep-r9.md` §1 and `walker-live-surface.md`
  §1/§3 pin 13,220 B, sha `5b4e47b7…`, mtime 2026-07-26; now 13,743 B, sha
  `3c5c6867…`, mtime 2026-10-08.
- `/usr/bin/walker`: `walker-live-surface.md` §1 pins 6,661,264 B, sha `64826a85…`,
  mtime 2026-07-26; now 7,039,912 B, sha `25240650…`, mtime 2026-10-08. The
  embedded-default offset moved from 784,064 (round-5/7/9 pins) to 806,960.
- Version: the notes describe walker 2.17.0 and elephant 2.21.0 (round-5 pin);
  the host now carries 2.17.2-1 and 2.22.1-1 (§ Host version binding).
- The round-7 `WALKER_` census (exactly one literal, adjacent to `config.toml`) still
  holds for the 2.17.2 binary (one literal). The byte run after it changed.

### Launch declarations (omarchy defaults, source edge not traced here)

- `default/hypr/bindings/utilities.conf:2-3` binds `SUPER, SPACE` to
  `omarchy-launch-walker` and `SUPER CTRL, E` to `omarchy-launch-walker -m symbols`;
  `default/hypr/bindings/clipboard.conf:5` binds `-m clipboard`. The commented
  `~/.config/hypr/bindings.conf:40` line binds the emoji picker to the same script.
- `default/hypr/apps/walker.conf:2` sets `layerrule = no_anim on, match:namespace walker`,
  sourced from `default/hypr/apps.conf:18`. Whether that include edge is active on
  this host is not traced in this note (`hyprland-config-plane.md` carries the edge).

## Safe observation

What an operator may read without changing state or starting a process:

- `sha256sum`, `stat -c '%n %s %y'`, `wc -l` and `cat -n` on the host files listed
  in § Host declaration. Re-run to detect drift against the table.
- `grep -n` (or the grep tool) on the same config files for the key names above.
- `python3` byte reads of `/usr/bin/walker` to locate the embedded default
  (`find` of the marker and a byte compare). The binary is read, never executed.
- Omarchy checkout: read `.git/HEAD`, `.git/packed-refs`, `.git/FETCH_HEAD` as bytes.
  No git command runs in that checkout.
- Log read: `/var/log/pacman.log` lines by the grep tool. No `pacman -Q`, `-Qi`,
  `-Si`, `-Ql`, `-Qkk`, and no `checkupdates` or `expac`.
- Upstream: `git ls-remote https://github.com/<owner>/<repo> refs/tags/<tag>` (remote
  read only); `curl -sSL --max-time 60` of the raw URLs with receipts in
  `.ufo/waves/round-18/fetch/NoteWalker/`; the codeload tarball extracted into
  `/tmp` scratch and searched with the grep tool.

Not used, and not safe under the current host pause: `walker` and `elephant` in any
form (including `--version`, `--help`, `-q`, `-d`, `-e`), `elephant listproviders`,
`elephant query`, `busctl` introspection or calls against `dev.benz.walker`, any
connection to `walker.sock` or `elephant.sock` (`nc -U`, socket connect),
`systemctl --user`, `pidof`, `pgrep`,
`hyprctl layers`, any `omarchy-*` command, and any launch or keybind trigger.

## Unexercised behavior

- `[UNK]` Whether the running walker process (restarted by the hooks at `HP:3062` and
  `HP:3123`) is the 2.17.2 binary on disk: no `/proc/<pid>/exe` read and no process
  probe in this note. Basis for the moved-pin table is the file bytes only.
- `[UNK]` Whether `/usr/bin/walker` (sha `25240650…`) is a faithful build of the
  `v2.17.2` tag: no rebuild, no Arch PKGBUILD read, no package-DB query.
- `[UNK]` Whether walker really reads only the first user file found, and whether
  the `/etc/xdg` fallback is ever reached on this host: the search order is from
  the xdg crate docs (`XD:356-358`), not from a run with `XDG_CONFIG_HOME` varied.
- `[UNK]` The `WALKER_*` overlay: which environment names map to which
  `PartialWalker` fields, and whether underscore-bearing keys such as
  `additional_theme_location` can be set this way. The source declares the overlay
  (`WS:234-239`); the names are not enumerated by any run.
- `[UNK]` Array merge semantics for user `[providers] default` and
  `[[providers.prefixes]]` against the packaged arrays (`WS:245-` not read in full).
- `[UNK]` Whether the unused `notify` dependency (`WK:21`) is reached through any
  code the whole-tree search did not match (the search was textual, not a call graph).
- `[UNK]` Whether the syntax-error path panics (`WS:221-223` with `WM:108` unwrap)
  on this host: inferred from code, never triggered, and no mutated config was
  written to test it.
- `[UNK]` The `[[emergencies]]` trigger path for "Restart Walker"
  (`src/providers/emergency.rs` not read in this note).
- `[UNK]` Elephant provider loading, the `provider_hosts` and `before_load` effects,
  and the `ProviderConfig` path resolution (the function body was not in the fetched
  files; `EG:85` is the only call site read).
- `[UNK]` The elephant socket protocol and the walker-to-elephant message set
  (`internal/comm/handlers/`, `src/providers/*` not read beyond the socket path).
- `[UNK]` Whether `omarchy-refresh-config walker/config.toml` (`OF:15`) keeps or
  replaces a user-authored `config.toml`: `omarchy-refresh-config` was not fetched.
- `[UNK]` Whether the `/tmp/elephant.sock` README line (`ER:211`) describes any
  build or environment where `XDG_RUNTIME_DIR` is unset; only the source fallback
  `os.TempDir()` (`EC:42`) was read.
- `[UNK]` Whether the Hyprland bindings and the layer rule (`default/hypr/apps/walker.conf:2`)
  are active on this host; the include edge was named, not traced.
- `[UNK]` Rendered output, the theme resolution order for partial themes, and any
  input or keyboard behaviour: no launcher was opened (P5 owns theme rendering).
- `[UNK]` Whether the host is currently under the R15 pacman pause or was restarted
  after the 2026-10-20 upgrade; this note reads the log only.

## Round-19 corrections (append-only, 2026-10-20)

- Head `source:` token S084 (docs.rs `latest` alias, an unpinned HTML page — R18-V4) was replaced in place by S098, the xdg 3.0.0 crate tarball whose sha256 `2fb43323…85b5` equals walker v2.17.2 `Cargo.lock:2708`; the search order XDG_CONFIG_HOME then XDG_CONFIG_DIRS (defaults `~/.config`, `/etc/xdg`) is unchanged (S098 `src/base_directories.rs:446-448`). S084 is now `rejected` in SOURCES.md. The `XD` key row above keeps its historical docs.rs line numbers; `XD:n` citations read as the same text at S098 `src/base_directories.rs` (`find_config_file` doc :446-448, defaults :308-310, :321-323).
- Host walker binary on 2026-10-20 (file bytes, S096): 2.17.2 literal at offset 856,302; `--version` output and runtime behaviour of 2.17.2 are not observed (host pause) and stay [UNK].
- Wave-2 correction (round 19, w2 AtkPtrWalkerRouteR18): the head `source:` line no longer names the rejected id (the round-18 `token-join-check.py` reads every `S###` on that line); the S098 receipt is `.ufo/waves/round-19/fetch/SrcS084/receipts.jsonl`, not the round-18 NoteWalker receipts the `verified-at:` line names; the host walker binary re-read is S096.

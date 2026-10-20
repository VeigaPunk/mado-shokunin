# HostTerminalFiles — P4 terminal surface, file-bytes evidence

Seat: MadoR17.HostTerminalFiles (leaf scout). Date 2026-10-20.
Question answered: what is the host's declared terminal-emulator route, with
byte anchors, for the C2 P4 note. Read-only. No terminal, compositor,
service, package, or probe command was executed; no tool installed.

## Method

`sha256sum` + `cat -n` / `grep -n` / `read` over files only. No `pacman`,
`sudo`, `systemctl`, `hyprctl`, `omarchy-*`, `alacritty`, `foot`, `ghostty`,
`xdg-terminal-exec` invocation, `notify-send`, or screenshot. One `find` over
`~/.config` and `~/.local/share/omarchy/default` for list-file names, and one
`file`/`ls` metadata read on two scripts. Cache file read is inert bytes.

## Observed inventory (all hashes computed this session)

| Path | SHA-256 | Anchor |
|---|---|---|
| `~/.config/xdg-terminals.list` | `d035da571a6bfc7d626d4a88846ea86a8adb6f6662f1f8b4abe2330e53ceb71b` | 3 lines; l.3 `Alacritty.desktop` |
| `~/.config/alacritty/alacritty.toml` | `695301c86577c808a94a01a4227bfaab3dbbe9a394a9954032f6173adec824f8` | l.1 `general.import = [ "~/.config/omarchy/current/theme/alacritty.toml" ]`; font size 12.5 (l.13); `[keyboard]` CSI-u bindings l.21–27 |
| `~/.config/omarchy/current/theme/alacritty.toml` | `8c3d1457c09d32e83367ac946ff6e85f6bda334c302587a043bef7dc7ac09139` | import target, 47 lines, `[colors.*]` only; resolves to the same absolute path (`readlink -f`), `current/theme` is a real directory |
| `~/.config/omarchy/current/theme.name` | (read) `matte-black` | names the active theme |
| `~/.config/foot/foot.ini` | `3e88354476f2682e7a1a0bc840d04e221e5c6a7312b3ee9dcf76ec16d0842e60` | l.2 `include=~/.config/omarchy/current/theme/foot.ini`; font 12.5 l.4 |
| `~/.config/omarchy/current/theme/foot.ini` | `d9c2e20e079a9314ec4cfd87370436ee0f34759a76bcdb0d5e1128ce672dcbeb` | colors only, 25 lines |
| `~/.config/ghostty/config` | `cb828c044b07d4fd924fe1d6b55c956035feb16f8d5c67899c8a598994596667` | l.2 `config-file = ?"~/.config/omarchy/current/theme/ghostty.conf"` |
| `~/.config/omarchy/current/theme/ghostty.conf` | `418636f99922f1ea64de37354fbb2708dd27c9d5f577ea63dd04d8d39b81203e` | palette only, 22 lines |
| `~/.config/hypr/bindings.conf` | `e574a1ed08535e31deeafe2a26432c6862bb101e8c45d5a6b3f997d7dc810581` | l.2 SUPER,RETURN → `uwsm-app -- xdg-terminal-exec --dir="$(omarchy-cmd-terminal-cwd)"`; l.3 SUPER ALT,RETURN → same + `tmux attach \|\| tmux new -s Work`; l.31 commented `alacritty -e ssh` |
| `~/.config/hypr/input.conf` | (grep) | l.45 `match:class (Alacritty\|kitty\|foot)` scroll rule; l.46 `com.mitchellh.ghostty` |
| `~/.local/share/applications/Alacritty.desktop` | `713703ba90ff8cd8d66eeb2804202e05e0c80c48e651ad00b9b7276f3d057683` | 452 B; l.14–17 `X-TerminalArgExec=-e`, `X-TerminalArgAppId=--class=`, `X-TerminalArgTitle=--title=`, `X-TerminalArgDir=--working-directory=` |
| `/usr/share/applications/Alacritty.desktop` | `d420b0f418d9039f324bdb423181f874dee36c47ce2ab643435a4c04aac243d8` | 374 B; **no** `X-TerminalArg*` keys — shadowed by the user-local file above |
| `/usr/bin/xdg-terminal-exec` | `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` | POSIX shell script, 1499 lines |
| `~/.cache/xdg-terminal-exec` | `dd26ec4e224bf38fdbd4842850ec9d6215b4aed51b9c5014998e8b37cbb1868a` | resolver cache, mtime 2026-10-20 09:57; l.2 `alacritty`, l.3 `…/.local/share/applications/./Alacritty.desktop`, l.4 `Alacritty.desktop`, l.6–9 `-e`, `--class=`, `--title=`, `--working-directory=` |
| `/usr/share/xdg-terminal-exec/xdg-terminals.list` | `a2b5bf691c44aa2557b54df513cc0a9f9f06633468b13e723b208e0b41fef034` | distro fallback; excludes `foot-server`/`footclient`, no Alacritty line |
| `~/.local/share/omarchy/bin/omarchy-default-terminal` | `42e422255521b970c16c42545e167ca6e094d8030fe6478531b16784d26ead91` | l.8 reads first non-comment line of the list; l.20 maps `alacritty`→`Alacritty.desktop`; l.30–34 writes the list from a heredoc |
| `~/.local/share/omarchy/bin/omarchy-cmd-terminal-cwd` | `1c262a806b8fb8ececcec1f3db31f1b2bb43ab8bcabdbdca43bafd3e5dae7f3b` | l.6–8 `hyprctl activewindow` → pid → child shell; l.10 `readlink -f /proc/$shell_pid/cwd`; fallback `$HOME` |
| `~/.local/share/omarchy/config/alacritty/alacritty.toml` | `ea3e0fa094ca2c763d284dbba39730ee3638ed20c97da6e69adb45f77ee1207a` | omarchy template; same as `~/.config/alacritty/alacritty.toml.bak.20261003-190229`, differing from live only in `size = 9` (l.13) |
| `~/.local/share/omarchy/default/alacritty/screensaver.toml` | `b47ca28f13c7409f17f0938f6e50eb854509b0c1152e05ecde4f59cc2418cf22` | screensaver variant only, not imported by the live config |
| `~/.local/share/omarchy/default/foot/foot.desktop` | `87eff5a90b051db922203e36e684d8110595eba0fbaedd3cdb789919f85074cf` | `X-TerminalArg*` set; **not** installed under `~/.local/share/applications` (only `foot-server.desktop`, `footclient.desktop`) |
| `~/.local/share/omarchy/default/foot/screensaver.ini` | `053150146bccb101eb2f14e0622376cff4d62563c3b1a16ae7dd8668be7ac51c` | screensaver only |
| `~/.local/share/omarchy/default/ghostty/screensaver` | `cd14aa796193660808bbd3341d12f5cc69937698399f267015ee2010f627a865` | padding overrides only |

No `~/.config/*xdg-terminals.list` other than the one above; no
`/etc/xdg/xdg-terminals.list`; no `hyprland-xdg-terminals.list`. So the only
list consulted is the three-line user file.

## Declared route (documentary, not observed behaviour)

1. **Binding.** `~/.config/hypr/bindings.conf:2` binds `SUPER, RETURN` to
   `uwsm-app -- xdg-terminal-exec --dir="$(omarchy-cmd-terminal-cwd)"`;
   l.3 adds the tmux variant. `hyprland.conf:18` sources `bindings.conf`
   after the omarchy defaults, so the user line wins over
   `~/.local/share/omarchy/default/hypr/plain-bindings.conf:2` (same command,
   no tmux).
2. **Selection.** `~/.config/xdg-terminals.list` l.1–2 are the comment header,
   l.3 is `Alacritty.desktop`. The same header-plus-ID bytes are the heredoc
   at `omarchy-default-terminal:31–33` [INFERENCE: this file was written by
   that helper; content equivalence only, no invocation observed]. Filter
   `grep -vE '^($|#)' | head -n 1` reproduces `Alacritty.desktop` exactly.
3. **Resolution.** `/usr/bin/xdg-terminal-exec` reads the list at
   `make_paths` l.148–153 (`${XDG_CONFIG_HOME:-~/.config}/xdg-terminals.list`),
   prepends/data-dir lists at l.157–162, and walks IDs "in descending order
   of preference" to "find first applicable" (l.1185, l.1207). `--dir` is
   documented at l.106. With `X-TerminalArgDir` present it becomes the
   `--working-directory=` argv element (l.919–925); without it the script
   `cd "$XTE__DIRVAL"` before `exec` (l.1494–1497).
4. **Desktop entry.** The user-local `~/.local/share/applications/Alacritty.desktop`
   (452 B) shadows `/usr/share/applications/Alacritty.desktop` (374 B) in the
   `XDG_DATA_HOME`-first search (xdg-terminal-exec l.165–168). Only the user
   copy declares `X-TerminalArgExec=-e`, `X-TerminalArgAppId=--class=`,
   `X-TerminalArgTitle=--title=`, `X-TerminalArgDir=--working-directory=`
   (l.14–17); the system package entry declares none, so `--dir` would fall
   back to the script's own `cd` there. `TryExec=alacritty` (l.3) is the
   validity gate the resolver applies.
5. **Terminal config.** Alacritty's live config
   `~/.config/alacritty/alacritty.toml:1` imports
   `~/.config/omarchy/current/theme/alacritty.toml` (colors only, 47 lines,
   theme `matte-black`). The omarchy template
   `~/.local/share/omarchy/config/alacritty/alacritty.toml` is byte-identical
   to the retained `.bak.20261003-190229` except `size = 9` vs `12.5`, so the
   live file is the template plus the font-size change. `screensaver.toml`
   in `omarchy/default/alacritty/` is not referenced by the live config.
6. **Alternates on disk, not selected.** `~/.config/foot/foot.ini` and
   `~/.config/ghostty/config` both exist and both import theme files, but the
   list names only Alacritty, so on this documentary route they are
   second-tier and unreachable through `SUPER,RETURN`.

Recorded corroboration (inert artifact, not a live probe): the resolver's own
cache `~/.cache/xdg-terminal-exec` (mtime today 09:57) stores
`alacritty`, the user-local desktop path, `Alacritty.desktop`, and the four
`X-TerminalArg*` values above. That is the resolver's cached self-description
of a prior resolution, not behaviour I executed; it is consistent with the
route and adds no live claim.

## C2 P4 note material (draft for L1, documentary only)

Suggested one-line route, all anchors above:

> P4 terminal: `SUPER,RETURN` runs `uwsm-app -- xdg-terminal-exec --dir=…`
> (`~/.config/hypr/bindings.conf:2`); `~/.config/xdg-terminals.list:3` names
> `Alacritty.desktop`, whose user-local entry carries
> `X-TerminalArgDir=--working-directory=`; Alacritty reads
> `~/.config/alacritty/alacritty.toml:1`, which imports the active theme's
> `alacritty.toml` from `~/.config/omarchy/current/theme/`.

Invariants the note may state as documentary facts: the list's first
non-comment entry is `Alacritty.desktop`; no other `xdg-terminals.list`,
desktop-specific list, or `/etc/xdg` list exists; the system Alacritty
desktop entry lacks the `X-TerminalArg*` keys that the user override supplies.

## Gaps and unknowns

- `[UNK]` Whether `~/.config/xdg-terminals.list` was last written by
  `omarchy-default-terminal`; only byte-equivalence with its heredoc is
  observed.
- `[UNK]` Installed Alacritty/foot/ghostty/xdg-terminal-exec versions — no
  package query was permitted (host pause); the script at
  `/usr/bin/xdg-terminal-exec` is dated Sep 18 and its digest is recorded.
- `[UNK]` Whether Alacritty actually starts and resolves the theme at runtime;
  no terminal was launched. `TryExec`/desktop validity are file facts only.
- The cache file is the resolver's own artifact; treat as corroboration, not
  as observation of a keyboard binding firing.
- **C2 rubric dependency (L1 decision):** a covered entry must cite a mined
  tier-A `SOURCES.md` row whose used-by names it. The anchors here are host
  file bytes, not web sources. If `SOURCES.md` rows can be host-file evidence
  rows, L1 can mine one row citing these paths+digests; if rows must be
  upstream/web, the P4 note needs an upstream tier-A row (e.g. the
  xdg-terminal-exec spec / Alacritty config docs) *plus* these host anchors in
  the body. I did not fetch web sources for this seat; that is not claimed.

## Compliance

No pacman/yay/paru (including `-Q`/`-Si`/`-Sp`/`-Fl`), sudo, systemctl,
hyprctl, libinput, evtest, wayland-info, hypridle, hyprlock, alacritty, foot,
ghostty, waybar, walker, omarchy-*, notify-send, screenshot, or input probe
was run. No file under `~/.config` or `~/.local/share/omarchy` was modified;
the only write is this report. No tools installed or updated.

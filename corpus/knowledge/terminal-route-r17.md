source: S056 (xdg-terminal-exec v0.14.3 README.md:55-57,100-101,115-118,131,153-166,264; S057 xdg-terminal-exec:106,148-162,919,1252; S058 alacritty v0.17.0 extra/man/alacritty.5.scd:27-41,57-61; S059 host ~/.config/hypr/bindings.conf:2-3, ~/.config/xdg-terminals.list:3, ~/.config/alacritty/alacritty.toml:1; S060 /usr/share/xdg-terminal-exec/xdg-terminals.list:1-25)
verified-at: 2026-10-20; tag-pinned raw bytes fetched with curl and host files read as bytes only (sha256sum, cat, stat, grep); SHA-256 values in the sections below and in corpus/SOURCES.md S056-S060
recheck: re-fetch README.md, xdg-terminal-exec and xdg-terminals.list at tag v0.14.3 and extra/man/alacritty.5.scd at tag v0.17.0, compare their SHA-256 values, re-hash the host files, reread the named lines; no alacritty, xdg-terminal-exec, omarchy-*, pacman or package query, systemctl, hyprctl or live probe
surface: P4

# Terminal emulator route — documentary, not observed

This route is `[INF-docs]` from tagged upstream xdg-terminal-exec v0.14.3 and
tagged Alacritty v0.17.0, joined to this host's declarations by file bytes. It
establishes what the declared chain asks for. It does not establish which
terminal actually launches, the installed Alacritty version, or any reload
effect on this host. No terminal, launcher or compositor was run.
Companion measured inventory: `corpus/knowledge/terminals-and-omarchy.md`
(2026-10-14, all four terminal trees; it already recorded the
`xdg-terminals.list` → `Alacritty.desktop` edge). This note adds the sourced
upstream contract; it covers Alacritty only, not foot, kitty or ghostty.

## Upstream contract

Pinned to xdg-terminal-exec tag `v0.14.3` (ref object
`065925df9f419008159258ae169018bfd23df71b`, lightweight tag).

- Selection files are named `${desktop}-xdg-terminals.list` or
  `xdg-terminals.list`. README.md:100-101: "Configuration files are named
  `${desktop}-xdg-terminals.list` or `xdg-terminals.list` and placed in XDG
  config hierarchy."
- Lookup order. README.md:115-118 lists `${HOME}/.config/xdg-terminals.list`
  after its `${desktop}`-prefixed sibling and before `/etc/xdg/`. The script
  builds the same sequence from `XDG_CONFIG_HOME`/`XDG_CONFIG_DIRS` and then
  the data-dir `xdg-terminal-exec/` copies (xdg-terminal-exec:148-162). The
  system-data copy is the lowest priority (README.md:120-123).
- Format. README.md:131: "The format is a simple newline-separated list with
  decreasing priority." Lines starting with `#` are ignored (README.md:133).
- Applicability. README.md:153-166 composes the explicit list from the
  highest-priority file first, then each entry is checked. README.md:166: "Each
  entry from the explicit selection list is checked for applicability:"
  Entries failing the check are discarded, so a listed name is a preference, not
  a guarantee of launch.
- Working directory option. xdg-terminal-exec:106 documents `--dir=workdir`:
  "set workdir of terminal." The option parser is at xdg-terminal-exec:1252. A
  desktop entry may carry `TerminalArgDir` (xdg-terminal-exec:919); the host's
  user-local Alacritty entry declares it as bytes (see Host declaration).
- Compliance wording. README.md:264: "Some examples of compliant terminals:
  xterm, alacritty, kitty, foot, qterminal". This names Alacritty as a compliant
  example in upstream text. It is not a version claim or a behaviour claim.
- `TerminalArgExec` defaults come from `/execarg_default:` directives
  (xdg-terminal-exec:402-413). The upstream example list has no Alacritty
  entry (see S060 below).

Alacritty side, pinned to tag `v0.17.0` (tag object
`dc946285396bd3e251b6942af7e9961b74f76bee`, peeled commit
`94e7c8874e526b1e67b349d9ba30ddf81669119e`), `extra/man/alacritty.5.scd`:

- `general.import` (alacritty.5.scd:31): imports are loaded in order and missing
  files are skipped. Quote, alacritty.5.scd:35-37: "Imports are loaded in order,
  skipping all missing files, with the importing file being loaded last."
- Path forms (alacritty.5.scd:39-40): "paths relative to the user's home
  directory starting with" `~/` are accepted, as are absolute paths and paths
  relative to the importing file.
- `live_config_reload` (alacritty.5.scd:57-61): "Live config reload (changes
  require restart)"; "Default: true".

## Host declaration

Read as file bytes only. Hashes are SHA-256 of the bytes on disk.

| Path | SHA-256 | Anchor and quoted content |
|---|---|---|
| `~/.config/hypr/bindings.conf` | `e574a1ed08535e31deeafe2a26432c6862bb101e8c45d5a6b3f997d7dc810581` | line 2: `bindd = SUPER, RETURN, Terminal, exec, uwsm-app -- xdg-terminal-exec --dir=` ; line 3 uses the same launcher with `bash -c "tmux attach \|\| tmux new -s Work"` |
| `~/.config/xdg-terminals.list` | `d035da571a6bfc7d626d4a88846ea86a8adb6f6662f1f8b4abe2330e53ceb71b` | line 3: `Alacritty.desktop` (lines 1-2 are host-authored comments, not upstream text) |
| `/usr/share/xdg-terminal-exec/xdg-terminals.list` | `a2b5bf691c44aa2557b54df513cc0a9f9f06633468b13e723b208e0b41fef034` (1053 bytes) | lowest-priority system list; see S060 |
| `~/.config/alacritty/alacritty.toml` | `695301c86577c808a94a01a4227bfaab3dbbe9a394a9954032f6173adec824f8` | line 1: `general.import = [ "~/.config/omarchy/current/theme/alacritty.toml" ]`; lines 3-27 set `[env]`, `[terminal]`, `[font]`, `[window]`, `[keyboard]`; no `live_config_reload` key (grep count 0) |
| `~/.config/omarchy/current/theme/alacritty.toml` (import target) | `8c3d1457c09d32e83367ac946ff6e85f6bda334c302587a043bef7dc7ac09139` (772 bytes, regular file) | hashed only; content not interpreted |
| `~/.local/share/applications/Alacritty.desktop` (user-local entry, shadows `/usr/share/applications/Alacritty.desktop`) | `713703ba90ff8cd8d66eeb2804202e05e0c80c48e651ad00b9b7276f3d057683` | line 7 `Categories=System;TerminalEmulator;`; lines 14-17 `X-TerminalArgExec=-e`, `X-TerminalArgAppId=--class=`, `X-TerminalArgTitle=--title=`, `X-TerminalArgDir=--working-directory=`; the system entry has 0 `X-Terminal` keys (grep count, round 17) |
| `~/.config/alacritty/alacritty.toml.bak.20261003-190229` | `ea3e0fa094ca2c763d284dbba39730ee3638ed20c97da6e69adb45f77ee1207a` | not referenced by the live file; not read |

Desktop-prefixed selection files (`${desktop}-xdg-terminals.list`) were checked
for by name in `~/.config` (maxdepth 1) and `/etc/xdg`: none present, so the
plain `xdg-terminals.list` files are the only selection files observed. Upstream
v0.14.3 files, for comparison (curl, tag-pinned):

- `README.md` 14762 bytes, `c7a1a8bb711e44e4a19ca0a3c943f13a8e53d5fbb6c752e08cb186d5995a9d40`
- `xdg-terminal-exec` 44020 bytes, `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac`
- `xdg-terminals.list` 1053 bytes, `a2b5bf691c44aa2557b54df513cc0a9f9f06633468b13e723b208e0b41fef034`
- `alacritty.5.scd` (v0.17.0) 28787 bytes, `e444fa45fb7045a61538383c7e588c63e260b9151cb3c8c4dddb742b7a0c4107`

The host's system-level list is byte-identical to upstream v0.14.3's
`xdg-terminals.list`. That shows the file matches upstream v0.14.3 bytes; it
does not show which package installed it or which version is installed.

Declared chain, read from bytes only: `bindings.conf:2` calls
`xdg-terminal-exec --dir=…`; the first entry in `~/.config/xdg-terminals.list`
is `Alacritty.desktop`; the `alacritty.toml` file imports an omarchy theme file
and declares font, window, keyboard and `[terminal] osc52 = "CopyPaste"`.

## Safe observation

- Every host read was a byte operation (`sha256sum`, `cat -n`, `grep`, `stat`).
  Nothing from the route was executed. No pacman, sudo, systemctl, hyprctl,
  omarchy-*, alacritty, xdg-terminal-exec, notify or input command was run.
- Upstream bytes were fetched with `curl` from `raw.githubusercontent.com` at the
  tags above; tag refs were resolved with `git ls-remote` (remote refs only).
- What the bytes establish: the declared request is "launch `Alacritty.desktop`
  if it passes the applicability check". The documented import rule means a
  missing theme file would be skipped, not fatal. The documented
  `live_config_reload` default is `true`.

## Unexercised behavior

- [UNK] Which terminal actually launches. That depends on whether
  `Alacritty.desktop` resolves to an installed, valid `TerminalEmulator` entry
  (README.md:166 check). The entry's bytes are read; no launcher ran.
- Version binding (file read of `/var/log/pacman.log`, no package query):
  `installed alacritty (0.17.0-1)` (pacman.log:639, 2026-10-03) with no later
  alacritty line, and `upgraded xdg-terminal-exec (0.14.3-1 -> 0.14.3-2)`
  (pacman.log:2935, 2026-10-20 09:16, a non-lane `-Syu`). The tags read
  (v0.17.0, v0.14.3) match the last logged pkgver. [UNK] the running binary,
  Arch packaging changes, and any change not in the log.
- Narrowed in round 17 (bytes, not behaviour): the user-local
  `Alacritty.desktop` declares `TerminalEmulator` and `X-TerminalArgExec=-e`
  plus `X-TerminalArgDir=--working-directory=` (Host declaration table), the
  keys the applicability check and `--dir=` mapping read
  (xdg-terminal-exec:919, 402-413). [UNK] whether the resolver actually picks
  that entry over the system one at launch; no launcher ran.
- [UNK] Reload effects on this host. The documented default is `true`, but
  whether an edit to `alacritty.toml` or to the imported theme file reloads a
  running window, and what a skipped missing import does, were not observed.
- [UNK] Whether the `--dir=` value from `omarchy-cmd-terminal-cwd` is valid at
  launch time. The helper is not run.

Source rows: `corpus/SOURCES.md` S056-S060 (mined) and S061-S062 (rejected); gate quotes in `lessons/round-17.md` § Gate.

# ScoutOmarchy report: origin of the host terminal-selection inputs

Read-only. All commands run 2026-10-26; omarchy checkout HEAD = 8fcc9d6048af4cb0e3af8512c78049857a3b53dd.

## 1. Origins (sha256 compared)

| host file | sha256 | origin |
|---|---|---|
| ~/.config/xdg-terminals.list (127 B, mtime 2026-10-03 17:44:32) | d035da571a6bfc7d626d4a88846ea86a8adb6f6662f1f8b4abe2330e53ceb71b | **omarchy** config/xdg-terminals.list, byte-equal to the checkout and to upstream raw at the pinned commit |
| ~/.local/share/applications/Alacritty.desktop (452 B, mtime 2026-10-03 17:44:35) | 713703ba90ff8cd8d66eeb2804202e05e0c80c48e651ad00b9b7276f3d057683 | **omarchy** applications/Alacritty.desktop, byte-equal to the checkout and to upstream raw at the pinned commit |
| /usr/share/applications/Alacritty.desktop (374 B, mtime 2026-04-06) | d420b0f418d9039f324bdb423181f874dee36c47ce2ab643435a4c04aac243d8 | **package alacritty 0.17.0-1** (`pacman -Qo`; package install date 2026-10-03 17:44:19) |

Full list hash: d035da571a6bfc7d626d4a88846ea86a8adb6f6662f1f8b4abe2330e53ceb71b (local = checkout = upstream raw).

Upstream URL pins (HTTP 200, copies in this seat dir): basecamp/omarchy @ 8fcc9d6048af... paths applications/Alacritty.desktop and config/xdg-terminals.list (see sources.md A, B). The `omarchy/omarchy` org path returns 404; only `basecamp/omarchy` (the checkout's `origin`) resolves.

Install paths (checkout): list <- install/config/config.sh:3 (`cp -R config/* ~/.config/`), also written by bin/omarchy-install-terminal:45-49, bin/omarchy-default-terminal:30-33, migrations/1762121828.sh:22-26. Desktop file <- bin/omarchy-refresh-applications:11 (via install/config/mimetypes.sh:1), bin/omarchy-install-terminal:35-36, migrations/1762121828.sh:32 (cp) and migrations/1763558828.sh:5-26 (heredoc with the same content). Both migration ids are recorded in ~/.local/state/omarchy/migrations/. Both host files share a timestamp window within 3 s on 2026-10-03 17:44, the same moment alacritty 0.17.0-1 was installed (17:44:19), consistent with an install/refresh pass copying them; [INFERENCE] which of the paths above produced them on that date is not observable (content is identical across all of them).

## 2. Which Alacritty.desktop wins, and why

The user file (~/.local/share/applications/) wins. Observed:

- default env (XDG_DATA_HOME=~/.local/share first in the search order): `--print-id --print-path --print-cmd` -> `Alacritty.desktop`, `/home/vgpnk/.local/share/applications/Alacritty.desktop`, `alacritty`, rc 0.
- same with XDG_DATA_HOME pointed at an empty dir: path becomes `/usr/share/applications/Alacritty.desktop` (rc 0). So the override is purely by data-dir order: $XDG_DATA_HOME precedes $XDG_DATA_DIRS (/usr/local/share:/usr/share), and the desktop-file ID `Alacritty.desktop` is resolved first-found.
- The ID comes from ~/.config/xdg-terminals.list (omarchy copy, single entry `Alacritty.desktop`; comment lines ignored). /usr/share/xdg-terminal-exec/xdg-terminals.list (package) has only "-id" exclusions and "/execarg_default:" lines, no terminal entries; /etc/xdg/xdg-terminals.list does not exist.

Both files pass validation (Type=Application, Categories has TerminalEmulator, TryExec=alacritty), so both would be selectable; shadowing, not rejection, is the mechanism.

## 3. Key differences (diff system -> user)

Package file lacks, omarchy file adds:
- `X-TerminalArgExec=-e`, `X-TerminalArgAppId=--class=`, `X-TerminalArgTitle=--title=`, `X-TerminalArgDir=--working-directory=` (user file only).
- Package file has `X-Desktop-File-Install-Version=0.28` and an extra blank line after Categories (system only). Everything else (Type, TryExec, Exec, Icon, Terminal, Categories, Name, GenericName, Comment, StartupNotify, StartupWMClass, Actions, [Desktop Action New]) is identical.

Behavioural effect, measured: `--print-cmd --dir=/x --title=T --app-id=A` with the user file prints `alacritty`, `--class=A`, `--title=T`, `--working-directory=/x` (one per line, rc 0). With the system file only (XDG_DATA_HOME empty) the same options printed only `alacritty` (rc 0 for `--print-id --print-path --print-cmd --dir=/x --title=T --app-id=A`: id, path, `alacritty`). I.e. without the user override, `--dir=`, `--title=`, `--app-id=` are silently not passed through, so SUPER+RETURN's `--dir="$(omarchy-cmd-terminal-cwd)"` would stop opening in the cwd. [INFERENCE for the launch; the print output itself is observed.]

## 4. Fixture hints for C1/C2

- The user-vs-system shadowing class and the X-TerminalArg* class are real host cases; the two Alacritty.desktop files above (and /usr/share/xdg-terminal-exec/xdg-terminals.list, which carries -exclude and /execarg_default syntax) are good realistic seed texts.
- Cache: all print runs used an XDG_CACHE_HOME in scratch (deleted afterwards).
- Closes the r17 [UNK] with the observation in section 2 (user path selected, rc 0), without launching anything.

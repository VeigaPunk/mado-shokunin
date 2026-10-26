# ScoutOmarchy sources.md (candidate rows; L1 assigns S-numbers)

Omarchy checkout: ~/.local/share/omarchy, HEAD 8fcc9d6048af4cb0e3af8512c78049857a3b53dd (`git rev-parse HEAD`). Upstream remote: https://github.com/basecamp/omarchy.git (the `omarchy/omarchy` org URL returns 404 for the same path+commit; only basecamp/omarchy resolves).

| cand | source | locator / pin | sha256 | what it supports |
|---|---|---|---|---|
| A | upstream raw (fetched 2026-10-26, HTTP 200) | https://raw.githubusercontent.com/basecamp/omarchy/8fcc9d6048af4cb0e3af8512c78049857a3b53dd/applications/Alacritty.desktop ; copy in seat dir: basecamp-applications_Alacritty.desktop | 713703ba90ff8cd8d66eeb2804202e05e0c80c48e651ad00b9b7276f3d057683 | byte-equal to local checkout applications/Alacritty.desktop AND to ~/.local/share/applications/Alacritty.desktop |
| B | upstream raw (HTTP 200) | https://raw.githubusercontent.com/basecamp/omarchy/8fcc9d6048af4cb0e3af8512c78049857a3b53dd/config/xdg-terminals.list ; copy: basecamp-config_xdg-terminals.list | d035da571a6bfc7d626d4a88846ea86a8adb6f6662f1f8b4abe2330e53ceb71b | byte-equal to checkout config/xdg-terminals.list AND ~/.config/xdg-terminals.list |
| C | omarchy checkout | install/config/config.sh:3 `cp -R ~/.local/share/omarchy/config/* ~/.config/` | n/a | install path of B |
| D | omarchy checkout | bin/omarchy-refresh-applications:11 `cp .../applications/*.desktop ~/.local/share/applications/` (called from install/config/mimetypes.sh:1) | n/a | install/refresh path of A |
| E | omarchy checkout | bin/omarchy-install-terminal:16-48 (copies applications/Alacritty.desktop, rewrites ~/.config/xdg-terminals.list with 3 lines) | n/a | runtime rewrite path of B and A |
| F | omarchy checkout | bin/omarchy-default-terminal:8,30-33 (reads first non-comment line; rewrites the list) | n/a | reader/writer of B |
| G | omarchy checkout | migrations/1762121828.sh:12-33 (list from $TERMINAL; cp applications/Alacritty.desktop) ; migrations/1763558828.sh:1-27 (heredoc writing the user Alacritty.desktop with X-TerminalArg* keys, guarded by omarchy-pkg-present alacritty) | n/a | migration path for existing installs; both ids present in ~/.local/state/omarchy/migrations/ |
| H | git history | `git log --follow -- applications/Alacritty.desktop`: 8f1980674 2025-11-19 "Make existing alacritty installations compatible with X-TerminalArg", f1cd65ca7 2026-02-21 "Ensure that Alacritty is set to take xterm variables out of the box"; `git log -- config/xdg-terminals.list`: 1a564500a 2026-02-21 | n/a | provenance dates |
| I | host file | /usr/share/applications/Alacritty.desktop, mtime 2026-04-06 | d420b0f418d9039f324bdb423181f874dee36c47ce2ab643435a4c04aac243d8 | package copy; `pacman -Qo` -> owned by alacritty 0.17.0-1 (query only) |
| J | host file | /usr/share/xdg-terminal-exec/xdg-terminals.list; `pacman -Qo /usr/bin/xdg-terminal-exec` -> xdg-terminal-exec 0.14.3-2 | a2b5bf691c44aa2557b54df513cc0a9f9f06633468b13e723b208e0b41fef034 | package-shipped low-priority list (only exclusions "-id" and "/execarg_default:" lines; no terminal entries) |
| K | host observation | `XDG_CACHE_HOME=<scratch> xdg-terminal-exec --print-id --print-path --print-cmd` (and with XDG_DATA_HOME pointed at an empty dir) | n/a | see report.md section 3 |

Note: `pacman -Q*` printed `error: openai-chatgpt: missing required signature` on stderr (host repo-db noise); the queries still answered.

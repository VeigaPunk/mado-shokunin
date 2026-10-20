# NoteTerminal — SOURCES rows draft (round 17, P4)

Draft only. L1 assigns final S-ids (reserved S056-S069) on integration; every id
below is `S0xx-pending` in the note. Columns follow SOURCES.md's 11-column
registry shape (id | source | kind | tier | scope | anchor | teaches | status |
opened | recheck | used-by). Opened: 2026-10-20 for every row.

## Registry rows

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S056-pending | xdg-terminal-exec v0.14.3 README — https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/README.md | docs | A | upstream default-terminal selection contract at tag v0.14.3 (ref 065925df9f419008159258ae169018bfd23df71b) | README.md:55-57,100-101,115-123,131,133,153-166,264 @ v0.14.3 (sha256 c7a1a8bb711e44e4a19ca0a3c943f13a8e53d5fbb6c752e08cb186d5995a9d40, 14762 bytes) | selection-file names, lookup order, system list as lowest priority, first-valid applicability check, Alacritty named as a compliant example upstream; no host fact | mined | 2026-10-20 | on-release | corpus/knowledge/terminal-route-r17.md |
| S057-pending | xdg-terminal-exec v0.14.3 reference script — https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec | code | A | upstream script's option and lookup code at tag v0.14.3 | xdg-terminal-exec:106 (--dir), 148-162 (config sequence), 402-413 (execarg defaults), 919 (TerminalArgDir), 1252 (--dir= parse) @ v0.14.3 (sha256 89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac, 44020 bytes) | script agrees with README on lookup order and `--dir` meaning; execution not performed | mined | 2026-10-20 | on-release | corpus/knowledge/terminal-route-r17.md |
| S058-pending | Alacritty v0.17.0 config manual source — https://raw.githubusercontent.com/alacritty/alacritty/v0.17.0/extra/man/alacritty.5.scd | docs | A | Alacritty `general.import` and `live_config_reload` semantics at tag v0.17.0 (tag object dc946285396bd3e251b6942af7e9961b74f76bee, commit 94e7c8874e526b1e67b349d9ba30ddf81669119e) | alacritty.5.scd:27,31,35-41,57-61 @ v0.17.0 (sha256 e444fa45fb7045a61538383c7e588c63e260b9151cb3c8c4dddb742b7a0c4107, 28787 bytes) | imports load in order and missing files are skipped; relative import paths resolve from the importing file; live_config_reload defaults true; tag docs do not prove the host binary | mined | 2026-10-20 | on-release | corpus/knowledge/terminal-route-r17.md |
| S059-pending | host terminal declarations, file bytes — ~/.config/hypr/bindings.conf, ~/.config/xdg-terminals.list, ~/.config/alacritty/alacritty.toml | config | A | this host's P4 terminal declarations, read as bytes only | bindings.conf:2-3 (e574a1ed08535e31deeafe2a26432c6862bb101e8c45d5a6b3f997d7dc810581); xdg-terminals.list:3 (d035da571a6bfc7d626d4a88846ea86a8adb6f6662f1f8b4abe2330e53ceb71b); alacritty.toml:1-27 (695301c86577c808a94a01a4227bfaab3dbbe9a394a9954032f6173adec824f8); omarchy theme import target (8c3d1457c09d32e83367ac946ff6e85f6bda334c302587a043bef7dc7ac09139); .bak not referenced (ea3e0fa094ca2c763d284dbba39730ee3638ed20c97da6e69adb45f77ee1207a) | declares the launch chain and preferred terminal; does not establish which terminal launches, installed versions, or reload effect | mined | 2026-10-20 | on-change | corpus/knowledge/terminal-route-r17.md |
| S060-pending | host system terminal list — /usr/share/xdg-terminal-exec/xdg-terminals.list | config | A | lowest-priority system selection list in the upstream chain (host file bytes) | whole file, 1053 bytes, sha256 a2b5bf691c44aa2557b54df513cc0a9f9f06633468b13e723b208e0b41fef034; byte-identical digest to upstream v0.14.3 xdg-terminals.list (opened same day) | fallback exclusions and execarg defaults; no Alacritty entry; installing package and version [UNK] | mined | 2026-10-20 | on-change | corpus/knowledge/terminal-route-r17.md |
| S061-pending | Ubuntu manpage xdg-terminal-exec (manpages.ubuntu.com/manpages/resolute/man1/xdg-terminal-exec.1.html) | docs | C | distro-rendered man page; search snippet only, not opened | snippet "Provided by: xdg-terminal-exec (Version: 0.14.0-1ubuntu0.1)" | REJECTED: distro build 0.14.0 is neither tag v0.14.3 nor a host-observed version; a rendered page is not the upstream file. flip: tag-pinned upstream bytes (S056/S057) plus a host package version from a permitted non-pacman channel | rejected | 2026-10-20 | 180d | — |
| S062-pending | xdg-terminal-exec GitHub blob at master (github.com/Vladimir-csp/xdg-terminal-exec/blob/master/README.md) | docs | C | mutable branch ref; search snippet only, not opened | snippet "Ref: master" | REJECTED: a branch ref moves and cannot pin a version; any claim from it would not bind to an era. flip: a tag-pinned raw URL with sha256 (done as S056) | rejected | 2026-10-20 | 180d | — |

## Gate quotes (≤25 words each, verbatim) with anchors

- S056-pending README.md:100-101 — "Configuration files are named `${desktop}-xdg-terminals.list` or `xdg-terminals.list` and placed in XDG config hierarchy." (13 words)
- S056-pending README.md:166 — "Each entry from the explicit selection list is checked for applicability:" (12 words)
- S056-pending README.md:264 — "Some examples of compliant terminals: xterm, alacritty, kitty, foot, qterminal" (10 words)
- S057-pending xdg-terminal-exec:106 — "set workdir of terminal." (4 words)
- S058-pending alacritty.5.scd:35-37 — "Imports are loaded in order, skipping all missing files, with the importing file being loaded last." (16 words)
- S058-pending alacritty.5.scd:59 and 61 — "Live config reload (changes require restart)" (6 words); "Default: true" (2 words)
- S059-pending bindings.conf:2 — "bindd = SUPER, RETURN, Terminal, exec, uwsm-app -- xdg-terminal-exec --dir=" (10 words)
- S060-pending xdg-terminals.list:3 (system) — "# i.e. /usr/share/xdg-terminal-exec/xdg-terminals" (3 words, upstream text, identical bytes)

## SHA-256 per opened source

| Source | Raw bytes | SHA-256 | Anchors read |
|---|---|---|---|
| xdg-terminal-exec v0.14.3 README.md | 14762 | c7a1a8bb711e44e4a19ca0a3c943f13a8e53d5fbb6c752e08cb186d5995a9d40 | 55-57, 100-123, 131, 133, 153-166, 264 |
| xdg-terminal-exec v0.14.3 xdg-terminal-exec | 44020 | 89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac | 106, 148-162, 402-413, 919, 1252 |
| xdg-terminal-exec v0.14.3 xdg-terminals.list | 1053 | a2b5bf691c44aa2557b54df513cc0a9f9f06633468b13e723b208e0b41fef034 | 1-25 |
| alacritty v0.17.0 extra/man/alacritty.5.scd | 28787 | e444fa45fb7045a61538383c7e588c63e260b9151cb3c8c4dddb742b7a0c4107 | 27-41, 57-61 |
| host ~/.config/hypr/bindings.conf | file | e574a1ed08535e31deeafe2a26432c6862bb101e8c45d5a6b3f997d7dc810581 | 2-3 |
| host ~/.config/xdg-terminals.list | file | d035da571a6bfc7d626d4a88846ea86a8adb6f6662f1f8b4abe2330e53ceb71b | 1-3 |
| host /usr/share/xdg-terminal-exec/xdg-terminals.list | 1053 | a2b5bf691c44aa2557b54df513cc0a9f9f06633468b13e723b208e0b41fef034 | 1-25 |
| host ~/.config/alacritty/alacritty.toml | file | 695301c86577c808a94a01a4227bfaab3dbbe9a394a9954032f6173adec824f8 | 1-28 |
| host ~/.config/omarchy/current/theme/alacritty.toml (import target, hashed only) | 772 | 8c3d1457c09d32e83367ac946ff6e85f6bda334c302587a043bef7dc7ac09139 | not interpreted |
| host ~/.config/alacritty/alacritty.toml.bak.20261003-190229 (hashed only) | 873 | ea3e0fa094ca2c763d284dbba39730ee3638ed20c97da6e69adb45f77ee1207a | not read |

## Rejected candidates — taste evidence

- S061-pending (Ubuntu manpage, search snippet). Reason: distro 0.14.0 build, not v0.14.3, and a rendered page. Flip: tag-pinned upstream bytes plus a non-pacman host version.
- S062-pending (GitHub master blob). Reason: mutable branch ref. Flip: tag-pinned raw URL with sha256.

## Tool and channel record

No tool was installed or updated in this route. Remote reads were `curl` (raw
bytes, GitHub API unavailable at 403) and `git ls-remote` (tag refs; run from
the lane root, network read only; no git or jj mutation). No pacman, sudo,
systemctl, hyprctl, omarchy-*, alacritty or xdg-terminal-exec command.

## Integrator notes

- Source line on the note is one line, uses `S0xx-pending` ids, and cites the
  rows above; L1 replaces pending ids on integration.
- `used-by` on S056-S060 names `corpus/knowledge/terminal-route-r17.md`, so the
  note's coverage check (`source:` citing a tier-A row whose used-by names it,
  plus `surface: P4`) holds once the ids are assigned.
- Documentary route only. No observed behaviour is claimed in the note.

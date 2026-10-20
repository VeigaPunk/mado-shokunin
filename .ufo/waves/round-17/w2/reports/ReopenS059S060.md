# Reopen S059/S060 — host terminal declaration rows (wave 2, FALSIFY)

Lane HEAD checked: `988b858` (`git log --oneline -1`: "round-17 C3: post-hoc transcript
tripwire capability, suites and real-transcript receipts"). `git diff 988b858 --
corpus/knowledge/terminal-route-r17.md corpus/SOURCES.md corpus/README.md` is empty, so
every anchor below is the lane-HEAD text, not a worktree-only edit.

Targets: `corpus/SOURCES.md` S059/S060 (lines 71-72) and
`corpus/knowledge/terminal-route-r17.md` § Host declaration (lines 65-75).

Verdict: **all recorded SHA-256 values and all route-mechanic claims hold; one provenance
statement is falsified and three anchor/quote defects are confirmed.**

## 1. Digest verification (all match)

| File | Claimed SHA-256 | Observed | Bytes |
|---|---|---|---|
| `~/.config/hypr/bindings.conf` | `e574a1ed…810581` | match | 2879 |
| `~/.config/xdg-terminals.list` | `d035da57…ceb71b` | match | 127 |
| `~/.config/alacritty/alacritty.toml` | `695301c8…c824f8` | match | 876 |
| `/usr/share/xdg-terminal-exec/xdg-terminals.list` | `a2b5bf69…41fef034` | match | 1053 |
| `~/.config/omarchy/current/theme/alacritty.toml` | `8c3d1457…ac09139` | match; regular file | 772 |
| `~/.config/alacritty/alacritty.toml.bak.20261003-190229` | `ea3e0fa0…f77ee1207a` | match; 0 `bak` refs in live file | 873 |
| `~/.local/share/applications/Alacritty.desktop` | `713703ba…3d057683` (doc l.74 only) | match | 452 |

No digest drift between SOURCES, the knowledge note, and the bytes on disk.

## 2. FALSIFIED — provenance of the `xdg-terminals.list` comments

Anchor: `corpus/knowledge/terminal-route-r17.md:70` —

> `line 3: `Alacritty.desktop` (lines 1-2 are host-authored comments, not upstream text)`

"host-authored" is false. Counterevidence, all file bytes:

- `sha256sum ~/.local/share/omarchy/config/xdg-terminals.list` =
  `d035da571a6bfc7d626d4a88846ea86a8adb6f6662f1f8b4abe2330e53ceb71b`
  — the **same digest as the host file**; `cmp` reports byte-identical.
- The identical two comment lines are emitted verbatim by Omarchy scripts:
  - `~/.local/share/omarchy/bin/omarchy-install-terminal:45-48` heredoc:
    `# Terminal emulator preference order for xdg-terminal-exec` /
    `# The first found and valid terminal will be used` / `$desktop_id`
    (with `:16` `alacritty) desktop_id="Alacritty.desktop" ;;`).
  - `~/.local/share/omarchy/migrations/1762121828.sh:22-25`, same heredoc, entry from
    `$desktop_id` set at `:17`.
- Host-file mtime `2026-10-03 17:44:32.097678467` sits in the same second as
  `bindings.conf`'s `17:44:32.097141469`; that migration also rewrites `bindings.conf`
  (`:36` `sed` to `xdg-terminal-exec`, `:38` `--working-directory=` → `--dir=`), which is
  exactly the byte shape recorded at `bindings.conf:2-3`.

So lines 1-2 are Omarchy-shipped template text, and line 3 is Omarchy's `$desktop_id`
default chosen from `$TERMINAL`. Only the narrower reading "not xdg-terminal-exec upstream
text" survives (the system list `a2b5bf…` has entirely different comment text). This does
not break the P4 route — the file is still a declaration on disk — but "host-authored"
must not stand, and no claim of operator intent can be read from the preference.

Same provenance applies to the entry the doc cites at l.74 without comment: the user-local
`Alacritty.desktop` is byte-identical to `~/.local/share/omarchy/applications/Alacritty.desktop`
(`713703ba…`), copied by `omarchy-install-terminal:33`
(`cp "$OMARCHY_PATH/applications/$desktop_id" ~/.local/share/applications/`) or written by
`migrations/1763558828.sh:5-22` (same four `X-TerminalArg*` lines). The doc's phrase
"user-local entry" is true by path only; these are not operator-authored keys.

## 3. CONFIRMED — off-by-one anchor on `alacritty.toml`

- `wc -l ~/.config/alacritty/alacritty.toml` = **28**; `cat -n` line 28 is `]`, the close of
  the `[keyboard] bindings` array opened at line 21.
- `corpus/SOURCES.md:71` cites `alacritty.toml:1-27`; `terminal-route-r17.md:72` says
  "lines 3-27 set `[env]`, `[terminal]`, `[font]`, `[window]`, `[keyboard]`".
- The cited range stops one line before EOF and cuts the `bindings` literal mid-construct,
  so a reader restricted to :1-27 cannot see the array closed. Content claims are otherwise
  right (sections open at 3, 6, 9, 15, 20; `grep -c live_config_reload` = 0).
- Fix: `:1-28` (and `:3-28`), or cite `:3-20` plus `:21-28`.

## 4. CONFIRMED — non-verbatim quote of `bindings.conf:2`

`terminal-route-r17.md:69` quotes the line as ending `… xdg-terminal-exec --dir=` with no
ellipsis. The actual line 2 ends:

```
bindd = SUPER, RETURN, Terminal, exec, uwsm-app -- xdg-terminal-exec --dir="$(omarchy-cmd-terminal-cwd)"
```

The code span is a prefix presented as the line. The dropped `"$(omarchy-cmd-terminal-cwd)"`
is precisely the value the note later leaves `[UNK]` ("whether the `--dir=` value from
`omarchy-cmd-terminal-cwd` is valid"), so this is a quoting defect, not a route error.
Fix: include the value or add `…` after `--dir=`.

## 5. CONFIRMED — `Alacritty.desktop` has no SOURCES row

- `grep -rn 713703ba90ff…` over `corpus/` hits only `terminal-route-r17.md:74`; over the
  round-17 wave it hits only `w1/reports/HostTerminalFiles.md:30`.
- S059's scope names three files only (`bindings.conf`, `xdg-terminals.list`,
  `alacritty.toml`). S060 is the system list. S056-S058 are upstream xdg-terminal-exec and
  the Alacritty man page; S061/S062 are rejected.
- Yet `corpus/README.md:43` attributes the note to "`source:` S056–S060 … host bytes …
  `Alacritty.desktop` by sha256".

The desktop-entry bytes are a host fact with no registry row behind them, while the theme
import target and `.bak` digests *are* named inside S059's anchor column. Fix: add the
entry (and ideally the Omarchy `applications/`/`config/` templates it came from) to S059's
scope/anchor, or open a new row, then correct the README attribution.

## 6. Claims attacked and held

- `bindings.conf:2` binds `SUPER, RETURN` to `uwsm-app -- xdg-terminal-exec`; `:3` is the
  same launcher plus `bash -c "tmux attach || tmux new -s Work"` (md escaping `\|\|` only).
- `~/.config/xdg-terminals.list` has exactly 3 lines; line 3 is exactly `Alacritty.desktop`.
- S060: 1053 bytes, digest `a2b5bf…`. Fetched
  `https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminals.list`
  with curl: same digest, `diff -u` against the host file prints nothing → byte-identity
  claim holds. No Alacritty entry (0 matches); 10 `/execarg_default:` lines at :15-25;
  fallback exclusions at :6-8 and :11. "no Alacritty entry" and "fallback exclusions and
  execarg defaults" are accurate; installed package/version stays `[UNK]` and was not queried.
- `alacritty.toml:1` is exactly
  `general.import = [ "~/.config/omarchy/current/theme/alacritty.toml" ]`; live-reload key
  absent; import target is a 772-byte regular file.
- `Alacritty.desktop` line 7 `Categories=System;TerminalEmulator;` and lines 14-17
  `X-TerminalArgExec=-e`, `X-TerminalArgAppId=--class=`, `X-TerminalArgTitle=--title=`,
  `X-TerminalArgDir=--working-directory=` are exact. `/usr/share/applications/Alacritty.desktop`
  exists (374 B) with **0** `X-Terminal` keys, so "shadows the system entry" holds under
  XDG data-dir precedence.
- S059's "does not establish which terminal launches" remains correct and unimpeached.

## 7. Remaining unknowns

- Which terminal actually launches — unchanged; no launcher was run.
- Whether an Omarchy installer/migration or the operator wrote `~/.config/xdg-terminals.list`.
  Byte-identity to the shipped template plus the same-second mtime make installer origin the
  strong reading, but no run was observed.
- The imported theme file's content was not interpreted (hashed only), matching the note.
- No package query, so the installed `xdg-terminal-exec`/`alacritty` versions stay `[UNK]`.

## 8. Method and safety

Reads only: `sha256sum`, `cat -n`, `cmp`, `diff -u`, `grep -c/-rl`, `stat`, `sed -n`, plus one
`curl -fsSL` of the tag-pinned upstream `xdg-terminals.list` (raw bytes, sha256, diff).
No pacman/yay/paru (`-Q` included), sudo, systemctl, hyprctl, alacritty, xdg-terminal-exec,
omarchy-* or other live probe was run. Transcripts were not read. **Installs: none.**

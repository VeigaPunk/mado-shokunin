# ExecLive — live read-only host observation of the terminal selection (round 47, w1)

Seat: ExecLive. Scope: the live observation that closes the round-17 `[UNK]` at
`corpus/knowledge/terminal-route-r17.md:144-145` ("whether the resolver actually picks that entry over the
system one at launch; no launcher ran"), read-only, print modes only. No terminal was launched, no
compositor verb was used, no host file was written.

Pinned subject: `/usr/bin/xdg-terminal-exec`, sha256
`89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac`, 44020 bytes — the sha256 in the
wave brief, so every line number below is anchored to the file the C1 counter will run.

Receipts (this seat dir):
- `receipts/live-host.txt` — the full observation (env, five print runs, strace open list, list-file and
  desktop hashes, key diffs, host cache, A/B attribution, rule lines, commands).
- `receipts/raw/` — verbatim captures: `out.base.txt`, `out.dir_tmp.txt`, `out.htop.txt`,
  `out.id_only.txt`, `out.delim.txt`, `openat.files.txt` (filtered strace), `scratch-cache.txt`
  (the cold-cache file the resolver wrote into scratch).

## 1. Result: the resolver picks the user override — YES

Live invocation on this host (2026-10-26, `XDG_CACHE_HOME` redirected into scratch):

```
XDG_CACHE_HOME=<scratch>/cache xdg-terminal-exec --print-id --print-path --print-cmd
Alacritty.desktop
/home/vgpnk/.local/share/applications/Alacritty.desktop
alacritty
rc=0
```

The `--print-path` line is the user override, not `/usr/share/applications/Alacritty.desktop`. Three
repeats with fresh cache dirs hash identically (`9eb0a761...45cbc`, stdout incl. newline), so the answer
is not a cache artefact. This is the `[UNK]` closed with a live read of the same code path the hotkey
uses: `~/.config/hypr/bindings.conf:2` is `bindd = SUPER, RETURN, Terminal, exec, uwsm-app --
xdg-terminal-exec --dir="$(omarchy-cmd-terminal-cwd)"`, and the resolver resolves the entry, composes
argv and writes the cache before it ever `exec`s the terminal (script lines 1455-1499); the only thing
print mode skips is the final `exec "$@"`.

## 2. By which rule (script lines, all against the pinned sha)

1. **List-order rule** — `make_paths()`, lines 148-163: `${XDG_CONFIG_HOME}/<desktop>-xdg-terminals.list`
   (line 151), then `${XDG_CONFIG_HOME}/xdg-terminals.list` (line 153) come first, then `XDG_CONFIG_DIRS`,
   then `<data-dir>/xdg-terminal-exec/[<desktop>-]xdg-terminals.list` (lines 159-162). Only two list files
   exist on this host (section 3), and the user one names the entry at line 3.
2. **Data-dir preference order** — `make_paths()`, line 168
   (`XTE__APPLICATIONS_DIRS=${xte__dir%/}/applications/${XTE__APPLICATIONS_DIRS:+:...}`) prepends while
   iterating `XDG_DATA_HOME` then `XDG_DATA_DIRS`, so the search list ends up *ascending* preference and
   `/home/vgpnk/.local/share` is scanned last.
3. **Duplicate-ID rule** — `find_entry_paths()`, lines 780-782: "Entries are checked in ascending order of
   preference, so use last found if duplicate", then
   `alias "$xte__entry_id"="xte__entry_path='$xte__entry_path'"`. Same ID in two data dirs → the last one
   scanned (the user dir) overwrites the alias, so `Alacritty.desktop` resolves to the user file.
4. **Explicit-list rule** — `find_entry()` line 1060 walks `${XTE__ENTRY_IDS}//fallback_start//...`, and
   the comment at line 1057 records that explicitly listed IDs are not subject to DE show-in limits. The
   list hit is therefore tried first, with the ID scan as fallback.

So: the **path** is decided by rule 3 (user data dir scanned last), the **ID** by rule 1 (user list line 3),
and rule 2 makes rule 3 deterministic. Rule 1 alone is not the cause — proved in section 5(b).

## 3. Files the resolver read (strace -f -e trace=openat) and their hashes

Read, and nothing else in the config plane:

| file | sha256 | size |
|---|---|---|
| `/home/vgpnk/.config/xdg-terminals.list` | `d035da571a6bfc7d626d4a88846ea86a8adb6f6662f1f8b4abe2330e53ceb71b` | 127 B |
| `/usr/share/xdg-terminal-exec/xdg-terminals.list` | `a2b5bf691c44aa2557b54df513cc0a9f9f06633468b13e723b208e0b41fef034` | 1053 B |
| `~/.local/share/applications/Alacritty.desktop` (**user**) | `713703ba90ff8cd8d66eeb2804202e05e0c80c48e651ad00b9b7276f3d057683` | 452 B |
| `/usr/share/applications/Alacritty.desktop` (**system**) | `d420b0f418d9039f324bdb423181f874dee36c47ce2ab643435a4c04aac243d8` | 374 B |

Absent: `/etc/xdg/xdg-terminals.list`, `~/.local/share/xdg-terminals.list`,
`/usr/local/share/xdg-terminals.list`, `/usr/share/xdg-terminals.list`, and every per-desktop variant
(`hyprland-`, `Hyprland-`, `HYPRLAND-xdg-terminals.list`) in all five dirs and in `<data-dir>/xdg-terminal-exec/`.
The user list is two comment lines then `Alacritty.desktop` on line 3. The system list (25 lines) contains
no `Alacritty.desktop` token at all — its non-comment content is `-`exclusions (lines 6-12) and eleven
`/execarg_default:*` directives (lines 15-25).

The decisive strace fact: `/usr/share/applications/` was **listed** but
`/usr/share/applications/Alacritty.desktop` was **never opened**; only
`~/.local/share/applications/./Alacritty.desktop` was read `O_RDONLY`. Directory listings of both
`applications/` dirs (for the ID scan) plus the two list files are the whole config-plane read set. The
other successful opens were libc/locale (`/etc/{passwd,group,nsswitch.conf,localtime}`,
`/usr/share/locale/locale.alias`) and the scratch cache write — excluded from the claim, listed in the
receipt.

Host env `XDG_*` (verbatim, only these keys): recorded in `receipts/live-host.txt` [1];
`XDG_CURRENT_DESKTOP=Hyprland`, `XDG_CONFIG_DIRS=/etc/xdg`, `XDG_CONFIG_HOME=/home/vgpnk/.config`,
`XDG_DATA_DIRS=/usr/local/share:/usr/share`, `XDG_DATA_HOME=/home/vgpnk/.local/share`.

## 4. Which keys differ between the two Alacritty.desktop files (keys only)

Identical in both: `Type=Application`, `TryExec=alacritty`, `Exec=alacritty`, `Icon=Alacritty`,
`Terminal=false`, `Categories=System;TerminalEmulator;`, `Name=Alacritty`, `Actions=New;`, and the whole
`[Desktop Action New]` group (`Name=New Terminal`, `Exec=alacritty`).

Differing (user file line → system file line):

| key | user | system |
|---|---|---|
| `X-TerminalArgExec` | `-e` (14) | absent |
| `X-TerminalArgAppId` | `--class=` (15) | absent |
| `X-TerminalArgTitle` | `--title=` (16) | absent |
| `X-TerminalArgDir` | `--working-directory=` (17) | absent |
| `X-Desktop-File-Install-Version` | absent | `0.28` (15) |

`X-TerminalArgHold` is absent from both. The only other difference is a blank line (system line 8). No
`Exec`, `TryExec` or `Categories` value differs, so the two files are indistinguishable by ID, name and
command — the `X-TerminalArg*` keys are the *only* live discriminator, and they pay off twice in this
observation:

- `--print-id --print-path --print-cmd -- htop` → `... / alacritty / -e / htop`; `-e` exists only in the
  user file line 14. So exec-arg composition provably came from the user entry.
- `--print-id --print-path --print-cmd --dir=/tmp` → trailing `--working-directory=/tmp`, a template
  (line 17) that exists only in the user file.

This matters for C1: a Python re-implementation that only compares `Exec`/`TryExec`/`Categories` would
agree with the resolver on `--print-id`/`--print-path` and be caught out on `--print-cmd` and `--dir=`.

## 5. Attribution A/B (print modes only; nothing on the host modified)

| variation | `--print-path` |
|---|---|
| host env (baseline) | `~/.local/share/applications/Alacritty.desktop` |
| `XDG_DATA_HOME=<empty>` | `/usr/share/applications/Alacritty.desktop` |
| `XDG_CONFIG_HOME=<empty>` | `~/.local/share/applications/Alacritty.desktop` |
| both empty | `/usr/share/applications/Alacritty.desktop` |
| `XDG_CURRENT_DESKTOP=` (empty) | `~/.local/share/applications/Alacritty.desktop` |

(a) Removing only the user data dir flips the path to the system file with the ID and `Exec` unchanged →
the override is a data-dir scan-order effect (rule 3), not a list-file effect. (b) Removing the user
*list* keeps the user path via the fallback ID scan → the list supplies order/ID, not the path. (d) The
pick does not depend on the desktop name, because the winning list is desktop-agnostic and the winning ID
was explicitly listed.

## 6. The resolver's own cache (read only)

`~/.cache/xdg-terminal-exec` exists, 190 B, sha256
`f497ed057f8aaba24bea21ba652b810c6c2ab754b0b8fe9d9b1645e072a10cac`, mtime
`2026-10-26 17:42:25.200770484 -0300` (before every invocation this seat made; never written by me).
It names the same entry: hash header `d27b6b70...`, exec `alacritty`, path
`/home/vgpnk/.local/share/applications/./Alacritty.desktop`, id `Alacritty.desktop`. Its listing hash
equals a fresh scratch run's, so it is current, not stale.

Two byte-level facts worth carrying into the freeze (both measured, section [6] of the receipt):

- The host cache is **byte-identical** to a scratch cache from a run whose print set excluded
  `--print-path`. The 190-vs-188-byte difference is exactly the two characters `/./`, because the
  normalisation `*'/./'*) XTE__ENTRY_PATH=${XTE__ENTRY_PATH%%/./*}/${XTE__ENTRY_PATH##*/./}` (script line
  1342) runs only when `path` is in `XTE__PRINT_DATA`. A launch stores the un-normalised `find(1)` form;
  stdout never shows it.
- The cache is written **only** by runs that reach the exec/print-cmd stage: lines 1368-1386 bail out
  early when the print set has no `cmd` element, before `save_cache "$1" &` at line 1457. Measured with
  fresh `XDG_CACHE_HOME` dirs and a 1 s settle: `--print-id`, `--print-id --print-path` and
  `--print-path` leave **no file**; `--print-id --print-cmd` leaves 190 B; `--print-id --print-path
  --print-cmd` leaves 188 B. So the C1 draft contract's "cold cache" model is the right abstraction, and a
  frozen predicate that expects a cache file after a `--print-id`-only run would be measuring a
  non-event.

## 7. What this supports and what it attacks

- **Supports C2** (`xdg-terminal-selection-r47.md`): the executed chain for this host is rules 1-4 of
  section 2 with the section 3 file set; the `[UNK]` at `terminal-route-r17.md:144-145` is answered
  positively for this host state, with the evidence chain (only the user desktop opened; only the user list
  names the ID; user-only `X-TerminalArg*` keys appear in composed argv; the `XDG_DATA_HOME=<empty>`
  A/B flips the path).
- **Attacks any assumption that the two Alacritty entries are equivalent**: they differ only in
  `X-TerminalArg*`, which is exactly what `--print-cmd`/`--dir=` output depends on — the cheapest way to
  tell which file won.
- **Attacks a naive cache model**: cache presence depends on the print set (section 6), and the cached
  path keeps `/./` while stdout does not.
- **Constrains C1's Python re-implementation**: reproduce the user-data-dir-last scan and the
  `X-TerminalArg*` templates, not just ID selection; `--print-delimiter=seq` takes a literal delimiter
  string (not the word `seq` as a mode) — `--print-delimiter='|'` gives `Alacritty.desktop|alacritty`.

## 8. Risks, limits, unrun checks

- The observation is an *instant* of host state. It is falsified by editing `~/.config/xdg-terminals.list`
  line 3 (127 B, sha256 above), the user `Alacritty.desktop` (452 B, sha256 above) or by installing another
  terminal whose ID sorts later. Any re-check must re-pin those four hashes.
- Print mode exercises resolution, composition and the cache write but not `exec "$@"`; the claim
  "at launch" is therefore closed for the *selection*, with the launch-only remainder being the final
  `exec` (line 1499) and the `--hold`/`--dir` `cd` fallback (lines 1494-1497) — neither can change which
  entry was selected.
- The resolver shells out to `tr`, `find -L`, `awk` (visible in the trace); a sandbox for C1 needs them on
  PATH, as the brief states. Not re-verified here beyond the successful trace.
- No check of `uwsm-app` behaviour, of what the terminal window actually shows, or of any file outside the
  read set in section 3 — out of this seat's scope.
- This seat ran no build, lint or test gate, and wrote no lane file other than this report and its seat
  dir. Scratch was confined to this seat's wave scratch root and has been removed after the receipts
  were copied; no `/tmp` or scratch path is cited as evidence.
- No tool installs or upgrades were made, so nothing to record under the tooling directive.

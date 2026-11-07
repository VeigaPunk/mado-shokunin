# R92MExecHost — host replay (C1 candidate vs xdg-mime vs GLib resolver)

## Files
- Driver: `.ufo/waves/round-92/controls/host-run-r92.py` (owned; executable)
- Stdout capture: `.ufo/waves/round-92/w1/R92MExecHost-host-run.txt`
- This report: `.ufo/waves/round-92/w1/R92MExecHost.md`
- Scratch: `$HYAKU_SCRATCH/mado-r92/R92MExecHost` (deleted on exit)
- Candidate: `.ufo/waves/round-92/build/mado-xdgmime.c1.py` (argv: `--cwd S --env K=V… --json TYPES…`)
- GLib resolver: `tools/mado-mime.py` (argv: `--desktop/--config-home/--config-dirs/--data-home/--data-dirs/--path --json TYPES…`)

## Method
- Type universe: every non-empty line of `/usr/share/mime/types` in file order (1129) plus `x-scheme-handler/{http,https,mailto,file}` (1133 total, no dupes).
- Environment: only `HOME, PATH, XDG_CURRENT_DESKTOP, XDG_MENU_PREFIX, XDG_CONFIG_HOME, XDG_CONFIG_DIRS, XDG_DATA_HOME, XDG_DATA_DIRS` passed from own shell — `HOME=/home/vgpnk`, `XDG_CURRENT_DESKTOP=Hyprland`, `XDG_MENU_PREFIX=hyprland-`, `XDG_CONFIG_HOME=/home/vgpnk/.config`, `XDG_CONFIG_DIRS=/etc/xdg`, `XDG_DATA_HOME=/home/vgpnk/.local/share`, `XDG_DATA_DIRS=/usr/local/share:/usr/share`. No other env var printed; `env -i`-style via `subprocess env=<dict>`, `cwd=<scratch>`. No `xdg-mime default/install/uninstall`, no `gio`, no `xdg-open`. Host MIME chain read only under `~/.config /etc/xdg ~/.local/share /usr/local/share /usr/share`.
- Legs: installed `/usr/bin/xdg-mime query default TYPE` (1 call/type; batched single call tested too slow-but-equivalent), candidate batched `--json`, GLib batched `--json`. Exit 0.

## Result (DRAFT — host replay, not a freeze measurement)
```
types=1133 agree=1133 disagree=0
types=1133 glib_agree=755 glib_disagree=378
```
- Candidate vs installed `xdg-mime`: **1133/1133 identical (output + empty/non-empty)**. No disagreements to list. Repro: `python3 .ufo/waves/round-92/controls/host-run-r92.py --scratch $S --candidate .ufo/waves/round-92/build/mado-xdgmime.c1.py` (exit 0, 167s; see `R92MExecHost-host-run.txt` above).
- GLib vs `xdg-mime`: **755 agree / 378 differ**. Full list in the capture; each `GLIB-DIFF` line carries `type`, both answers, and `decider=filereference|fallback`.

## Decider classification (verified against host files)
- `fallback` (375? — count breakdown: 375 lines with `decider=fallback`) — no `mimeapps.list`/`mimeinfo.cache` line; GLib answers through its merged-desktop-dirs + parent-type (`MimeDB.type_list`) chain while xdg-mime answers empty.
  - Verified example: `type=application/appinstaller xdg-mime='' glib='nvim.desktop'`. Root cause reproduced with the GLib tool internals (`tools/mado-mime.py:397` `type_list`, `:776` `default`): `type_list("application/json")` → `['application/json','application/json5','application/ecmascript','text/javascript','application/typescript','application/x-executable','text/plain']`; `text/plain` triggers `/home/vgpnk/.config/mimeapps.list:2` (`text/plain=nvim.desktop`, `[Default Applications]`) and `/usr/share/applications/mimeinfo.cache` (`text/plain=libreoffice-writer.desktop;nvim.desktop;`). `xdg-mime query default application/json` prints empty. Same parent chain drives `text/x-python` (`type_list` ends `…,text/plain`) → GLib `nvim.desktop`, xdg-mime empty. GLib count by handler: `nvim.desktop 283`, `org.gnome.Nautilus.desktop 38`, `mpv.desktop 14`, `imv.desktop 12`, `com.libretro.RetroArch.desktop 7`, others ≤3; xdg-mime empty for 375 of 378.
- `mimeinfo.cache:/usr/share/applications/mimeinfo.cache` (3, file:line verified):
  - `application/vnd.ms-excel`: line 57 `application/vnd.ms-excel=chatgpt.desktop;libreoffice-calc.desktop;` — `xdg-mime='chatgpt.desktop'` vs `glib='libreoffice-calc.desktop'` (xdg-mime takes first file entry; GLib skips first — `chatgpt.desktop` `MimeType` includes `application/vnd.ms-excel` (verified in `/usr/share/applications/chatgpt.desktop` but GLib handler validation drops it: `Exec` argv0 `chatgpt` not found via `find_program` / hidden — `tools/mado-mime.py:454`, `:763`).
  - `application/x-cmakecache`: `application/x-cmakecache=cmake-gui.desktop;` — `xdg-mime='cmake-gui.desktop'` vs `glib='nvim.desktop'` (GLib falls back via parent `text/plain`).
  - `image/heif`: `image/heif=imv-dir.desktop;imv.desktop;` — `xdg-mime='imv-dir.desktop'` vs `glib='krita_heif.desktop'` (GLib skips `imv-dir.desktop` on hidden/Exec validation, xdg-mime does not).

## Exact retained evidence (verbatim)
- `grep -n '^application/vnd.ms-excel' /usr/share/applications/mimeinfo.cache` → `57:application/vnd.ms-excel=chatgpt.desktop;libreoffice-calc.desktop;`
- `grep '^image/heif' /usr/share/applications/mimeinfo.cache` → `image/heif=imv-dir.desktop;imv.desktop;`
- `grep '^application/x-cmakecache' /usr/share/applications/mimeinfo.cache` → `application/x-cmakecache=cmake-gui.desktop;`
- `/home/vgpnk/.config/mimeapps.list:1-2` → `[Default Applications]` / `text/plain=nvim.desktop`
- `env -i … /usr/bin/xdg-mime query default application/json` → empty, rc=0; `tools/mado-mime.py --json application/json` → `{"default": "nvim.desktop", "registered": ["libreoffice-writer.desktop", "nvim.desktop"]}`

## Risks / notes
- `decider=fallback` lines state a classification, not a single file:line; the file:line split for those requires GLib's `type_list` parent chain + `mimeapps.list`/`mimeinfo.cache`/`MimeType=` walk. Verified in depth for `application/json` and `text/x-python` above.
- Candidate `rc=0` on all 1133 host types; no `unsupported` stderr. `mado-xdgmime: unsupported: PATH unset (bash's compiled-in default path)` was seen only when `PATH` omitted from `--env`, matching `build/mado-xdgmime.c1.py:452` `Resolver` — host run passes `PATH` explicitly.
- No installs. No fleet-root writes; no git mutations.

## Commands run
- `python3 host-run-r92.py --scratch $S --candidate build/mado-xdgmime.c1.py` → exit 0; stdout at `.ufo/waves/round-92/w1/R92MExecHost-host-run.txt` (383 lines).
- Preflight probes (draft, cwd=$S, env -i): `xdg-mime query default text/plain` → `nvim.desktop` rc=0; candidate `--json` batch rc=0; `tools/mado-mime.py --json text/plain` rc=0. All exit 0.

Report: .ufo/waves/round-92/w1/R92MExecHost.md

# R90MExecHost — host replay of the C1 candidate `mado-portals` (DRAFT)

| field | value |
|---|---|
| seat | R90MExecHost (executor, leaf; no spawn) |
| round | mado 90 / hyaku run 15, attempt 1, wave `w1` |
| lane | `/home/vgpnk/Projects/shokunin/mado-shokunin` |
| lane HEAD | `5041acf99e27263872bf0441ad5f9d4316152605` (= declared base rev; `git -C … rev-parse HEAD`, exit 0) |
| date | 2026-11-06 |
| host | linux 7.2.11-arch1-1 x64; shell `XDG_CURRENT_DESKTOP=Hyprland` |
| status | **DRAFT replay.** The declaration is unfrozen; no counter was run; nothing was written under `.ufo/waves/round-90/receipts/`. This is not a measurement. |
| candidate under replay | `.ufo/waves/round-90/build/mado-portals.c1.py` (sha256 is not part of the contract; the file was read-only) |
| oracle | `.ufo/waves/round-90/controls/portal-oracle-r90.py` → `/usr/lib/xdg-desktop-portal -v -r` on a private activation-free bus |
| scratch | `S=/fast/scratch/hyaku/mado-r90/R90MExecHost` (deleted at exit; see §10) |

Scope: read-only host replay of C1 only. No host portal call, no session/system bus, no service
restart, no credential material read.

## 1. Commands run (exact, with exit codes)

| # | command | exit |
|---|---|---|
| 1 | `pacman -Q xdg-desktop-portal xdg-desktop-portal-hyprland xdg-desktop-portal-gtk glib2` | 0 |
| 2 | `ls -la /usr/share/xdg-desktop-portal /usr/share/xdg-desktop-portal/portals ~/.config/xdg-desktop-portal ~/.local/share/xdg-desktop-portal /etc/xdg-desktop-portal /etc/xdg/xdg-desktop-portal` (per-dir loop) | 0 |
| 3 | `find <those roots> -type f \| sort \| xargs sha256sum` | 0 |
| 4 | `printf %s "$XDG_CURRENT_DESKTOP"` (own shell) | 0 |
| 5 | `python3 -I .ufo/waves/round-90/build/mado-portals.c1.py` (host defaults) | 0 |
| 6 | `python3 -I .ufo/waves/round-90/build/mado-portals.c1.py --json` (host defaults) | 0 |
| 7 | `python3 -I …/portal-oracle-r90.py --cases $S/single/<v>.json --label $S/single/<v>-label.json --scratch-root $S/single/scratch --timeout 10 --jobs 1` for each of the 5 desktop values | 0 ×5 |
| 8 | `python3 -I …/portal-oracle-r90.py --cases $S/host-cases.json --label $S/host-labels.json --scratch-root $S/oracle --timeout 10 --jobs 5` (5-case batch, determinism check) | 0 |
| 9 | `systemctl --user show -p Id -p ActiveState -p MainPID xdg-desktop-portal.service xdg-desktop-portal-hyprland.service xdg-desktop-portal-gtk.service` | 0 |
| 10 | diagnostics: `pacman -Qo <7 paths>`; `python3 -I …/mado-portals.c1.py --desktop Hyprland --datadir /nonexistent`; `… --portal-dir /usr/share/xdg-desktop-portal/portals --desktop Hyprland` | 0 |
| 11 | `git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse HEAD` (read-only) | 0 |

## 2. Host inventory

### 2.1 Packages (`pacman -Q`, exit 0)

```
xdg-desktop-portal 1.22.1-2
xdg-desktop-portal-hyprland 1.4.1-2
xdg-desktop-portal-gtk 1.15.3-2
glib2 2.90.1-1
```

`XDG_CURRENT_DESKTOP=Hyprland` (`XDG_SESSION_DESKTOP=Hyprland`). The replay therefore uses `Hyprland`
as the shell-value case and again as the literal `Hyprland` case (both requested; both produce the
same labels, §4).

### 2.2 Directory sweep (`ls -la`, exit 0)

| directory | state |
|---|---|
| `/usr/share/xdg-desktop-portal` | present: `gtk-portals.conf` (24 B), `hyprland-portals.conf` (32 B), `portals/` |
| `/usr/share/xdg-desktop-portal/portals` | present: `gnome-keyring.portal` (100 B), `gtk.portal` (495 B), `hyprland.portal` (281 B), `kwallet.portal` (119 B) |
| `~/.config/xdg-desktop-portal` (`/home/vgpnk/.config/xdg-desktop-portal`) | **ABSENT** |
| `~/.local/share/xdg-desktop-portal` (`/home/vgpnk/.local/share/xdg-desktop-portal`) | **ABSENT** |
| `/etc/xdg-desktop-portal` | **ABSENT** |
| `/etc/xdg/xdg-desktop-portal` | **ABSENT** |
| `/usr/local/share/xdg-desktop-portal` (extra, for oracle-equivalence) | **ABSENT** |
| `/usr/local/etc/xdg-desktop-portal` (extra) | **ABSENT** |

Finding (informational): the entire system config chain is carried by `/usr/share` only; no user,
`/etc`, or `/usr/local` override exists on this host at replay time. This is exactly the premise that
makes the tool's host defaults and the oracle's xdg fixture (fixture `XDG_CONFIG_HOME`/`XDG_DATA_HOME`
absent, `/usr/share` reached as the compiled-in `DATADIR`) search the same files.

### 2.3 sha256 of every file found (`sha256sum`, exit 0)

```
e1429fbe1bf6c2203ba07f478b9e92e9221437b13a92eebafb0982748583a4f8  /usr/lib/xdg-desktop-portal
aa061ba0530569907cf280870cc2b86333e0d7c2965d9ac020f5b3e05e9bd2e2  /usr/share/xdg-desktop-portal/hyprland-portals.conf
7021091f9257d6db3599b0b9cec64ce22fe303500fdee36e1e50945ef83c2c88  /usr/share/xdg-desktop-portal/gtk-portals.conf
611bc99db48a4647d2f31cbfdefba24fe9a039b607b3c5b378bac757de06d46b  /usr/share/xdg-desktop-portal/portals/gnome-keyring.portal
7b39a5f7f27c8c8ceb82c2937a981e58bdd6081cd332417285f8acadb13af495  /usr/share/xdg-desktop-portal/portals/gtk.portal
43b2fe354c2d4cc51bd237be8b6586cc6b6f5681451a4079adf2a97909d73431  /usr/share/xdg-desktop-portal/portals/hyprland.portal
daff78e798de5bd34a6dc9ca98d136cda4330e415377ebda2a80a309cacb41d6  /usr/share/xdg-desktop-portal/portals/kwallet.portal
```

`e1429fbe…` equals the oracle's own `oracle_binary_sha256` for the labels used below (checked in
`R90MExecHost-oracle-labels.json`), so the binary that produced the labels is the installed one.

Ownership (`pacman -Qo`, exit 0) — note the routing config is **not** owned by a portal package:

```
/usr/share/xdg-desktop-portal/hyprland-portals.conf  -> hyprland 0.56.2-4
/usr/share/xdg-desktop-portal/gtk-portals.conf       -> xdg-desktop-portal-gtk 1.15.3-2
/usr/share/xdg-desktop-portal/portals/hyprland.portal-> xdg-desktop-portal-hyprland 1.4.1-2
/usr/share/xdg-desktop-portal/portals/gtk.portal     -> xdg-desktop-portal-gtk 1.15.3-2
/usr/share/xdg-desktop-portal/portals/gnome-keyring.portal -> gnome-keyring 1:51.1-1
/usr/share/xdg-desktop-portal/portals/kwallet.portal -> kwallet 6.31.0-1
/usr/lib/xdg-desktop-portal                          -> xdg-desktop-portal 1.22.1-2
```

File contents (exact, `cat -A` verified; `$` = newline):

```
hyprland-portals.conf : "[preferred]$" / "default=hyprland;gtk"            (no trailing newline)
gtk-portals.conf      : "[preferred]$" / "default=gtk$"
hyprland.portal       : Interfaces=…Screenshot;…ScreenCast;…GlobalShortcuts;…InputCapture;  UseIn=wlroots;Hyprland;sway;Wayfire;river;
gtk.portal            : Interfaces=…FileChooser;…AppChooser;…Print;…Notification;…Inhibit;…Access;…Account;…Email;…DynamicLauncher;…Lockdown;…Settings;  UseIn=gnome
gnome-keyring.portal  : DBusName=org.freedesktop.secrets        Interfaces=…Secret     UseIn=gnome
kwallet.portal        : DBusName=org.freedesktop.impl.portal.desktop.kwallet  Interfaces=…Secret;  UseIn=kde
```

## 3. Candidate host run

`python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-90/build/mado-portals.c1.py`
(host defaults: desktop from the environment, `XDG_CONFIG_HOME=/home/vgpnk/.config`,
`XDG_CONFIG_DIRS=/etc/xdg`, `XDG_DATA_HOME=/home/vgpnk/.local/share`,
`XDG_DATA_DIRS=/usr/local/share:/usr/share`, `sysconfdir=/etc`, `datadir=/usr/share`) → exit 0:

```
MADO_PORTALS: desktops=hyprland backends=hyprland,gnome-keyring,gtk,kwallet configs=/usr/share/xdg-desktop-portal/hyprland-portals.conf,/usr/share/xdg-desktop-portal/hyprland-portals.conf
MADO_PORTAL: org.freedesktop.impl.portal.Lockdown -> gtk (default config)
MADO_PORTAL: org.freedesktop.impl.portal.Access -> gtk (default config)
MADO_PORTAL: org.freedesktop.impl.portal.Settings -> gtk (config)
MADO_PORTAL: org.freedesktop.impl.portal.FileChooser -> gtk (default config)
MADO_PORTAL: org.freedesktop.impl.portal.AppChooser -> gtk (default config)
MADO_PORTAL: org.freedesktop.impl.portal.Print -> gtk (default config)
MADO_PORTAL: org.freedesktop.impl.portal.Notification -> gtk (default config)
MADO_PORTAL: org.freedesktop.impl.portal.Inhibit -> gtk (default config)
MADO_PORTAL: org.freedesktop.impl.portal.Screenshot -> hyprland (default config)
MADO_PORTAL: org.freedesktop.impl.portal.Background -> none (no-backend)
MADO_PORTAL: org.freedesktop.impl.portal.Wallpaper -> none (no-backend)
MADO_PORTAL: org.freedesktop.impl.portal.Account -> gtk (default config)
MADO_PORTAL: org.freedesktop.impl.portal.Email -> gtk (default config)
MADO_PORTAL: org.freedesktop.impl.portal.Secret -> none (no-backend)
MADO_PORTAL: org.freedesktop.impl.portal.GlobalShortcuts -> hyprland (default config)
MADO_PORTAL: org.freedesktop.impl.portal.DynamicLauncher -> gtk (default config)
MADO_PORTAL: org.freedesktop.impl.portal.ScreenCast -> hyprland (default config)
MADO_PORTAL: org.freedesktop.impl.portal.RemoteDesktop -> none (no-backend)
MADO_PORTAL: org.freedesktop.impl.portal.Clipboard -> none (no-backend)
MADO_PORTAL: org.freedesktop.impl.portal.InputCapture -> hyprland (default config)
MADO_PORTAL: org.freedesktop.impl.portal.Usb -> none (no-backend)
```

`--json` (exit 0) prints the same as one object: `desktops=["hyprland"]`, the four backends, the two
identical config paths, `warnings=[]`, `picks`/`reasons` per interface. Stored verbatim in
`R90MExecHost-evidence.json` (`tool_json.tool-env`).

The duplicated config path is **faithful, not a defect**: upstream `load_portal_configurations`
appends configs from `g_get_system_data_dirs()` (`src/xdp-portal-config.c:573-580`) and then from
`DATADIR` (`:585-587`) with no deduplication, and on this host `/usr/share` is both an
`XDG_DATA_DIRS` entry and the compiled-in `DATADIR`. Diagnostic: `--datadir /nonexistent` (exit 0)
prints the same `hyprland-portals.conf` once. No pick or reason changes.

Desktop variants (each exit 0; JSON captured):

| value | tool header |
|---|---|
| `--desktop Hyprland` / environment / `--desktop hyprland` | `desktops=hyprland backends=hyprland,gnome-keyring,gtk,kwallet configs=…hyprland-portals.conf,…hyprland-portals.conf` |
| `--desktop-unset` | `desktops=- backends=gnome-keyring,gtk,hyprland,kwallet configs=-` |
| `--desktop 'Hyprland:GNOME'` | `desktops=hyprland,gnome backends=… configs=…` |

## 4. Oracle host replay (strict: one empty-fixture single-case file per desktop value)

Each case: `mode=xdg`, `files={}` (empty fixture; fixture `XDG_CONFIG_HOME`/`XDG_DATA_HOME`/
`XDG_DATA_DIRS` point at absent paths, and the binary's compiled-in `DATADIR=/usr/share` supplies the
host tail). The oracle ran each case alone with `--jobs 1`; each exited 0 and printed:

```
PORTAL_ORACLE cases=1 incomplete=0 host_tail_sha256=4a4cf31921e25dc6e60b283cc1aa1b79f743096bfdfc9dbb77df887c16f0fbf9
```

The tail digest equals the case-file pin `4a4cf319…` and the declaration's `4a4cf319…`; the binary
digest equals `e1429fbe…` (the installed `/usr/lib/xdg-desktop-portal`). A second 5-case batch run
(exit 0, `cases=5 incomplete=0`) produced identical labels for every value — the single-case and batch
labels agree interface-for-interface and reason-for-reason.

Raw labelled outputs: `R90MExecHost-oracle-labels.json` (batch) and
`R90MExecHost-evidence.json → oracle_single_runs[*].picks/reasons` (the five strict single runs).

## 5. Comparison, all 21 interfaces × 5 desktop values = 105 decisions

`oracle=tool` means the tool's pick equals the oracle's pick; the tool's reason string also equals the
oracle's reason string in every non-empty row (the oracle's `oracle_reason` and the tool's `reasons`).
Mismatched picks: **0**; mismatched reasons: **0**.

| interface | Hyprland (shell) | hyprland | unset | Hyprland:GNOME |
|---|---|---|---|---|
| `Access` | gtk=gtk | gtk=gtk | gtk=gtk | gtk=gtk |
| `Account` | gtk=gtk | gtk=gtk | gtk=gtk | gtk=gtk |
| `AppChooser` | gtk=gtk | gtk=gtk | gtk=gtk | gtk=gtk |
| `Background` | none=none | none=none | none=none | none=none |
| `Clipboard` | none=none | none=none | none=none | none=none |
| `DynamicLauncher` | gtk=gtk | gtk=gtk | gtk=gtk | gtk=gtk |
| `Email` | gtk=gtk | gtk=gtk | gtk=gtk | gtk=gtk |
| `FileChooser` | gtk=gtk | gtk=gtk | gtk=gtk | gtk=gtk |
| `GlobalShortcuts` | hyprland=hyprland | hyprland=hyprland | none=none | hyprland=hyprland |
| `Inhibit` | gtk=gtk | gtk=gtk | gtk=gtk | gtk=gtk |
| `InputCapture` | hyprland=hyprland | hyprland=hyprland | none=none | hyprland=hyprland |
| `Lockdown` | gtk=gtk | gtk=gtk | gtk=gtk | gtk=gtk |
| `Notification` | gtk=gtk | gtk=gtk | gtk=gtk | gtk=gtk |
| `Print` | gtk=gtk | gtk=gtk | gtk=gtk | gtk=gtk |
| `RemoteDesktop` | none=none | none=none | none=none | none=none |
| `ScreenCast` | hyprland=hyprland | hyprland=hyprland | none=none | hyprland=hyprland |
| `Screenshot` | hyprland=hyprland | hyprland=hyprland | none=none | hyprland=hyprland |
| `Secret` | none=none | none=none | none=none | gnome-keyring=gnome-keyring |
| `Settings` | gtk=gtk | gtk=gtk | gtk=gtk | gtk=gtk |
| `Usb` | none=none | none=none | none=none | none=none |
| `Wallpaper` | none=none | none=none | none=none | none=none |

Per-value resolution counts (oracle and tool identical):

| desktop | resolved | break-down | oracle reasons |
|---|---|---|---|
| `Hyprland` / `hyprland` | 15/21 | hyprland×4, gtk×11, none×6 | 14× `default config`, 1× `config` (Settings) |
| unset | 11/21 | gtk×11, none×10 | 11× `gtk-last-resort` (4 XDPH-only + 6 no-backend stay empty) |
| `Hyprland:GNOME` | 16/21 | hyprland×4, gtk×11, gnome-keyring×1, none×5 | 14× `default config`, 1× `config`, 1× `usein` (Secret) |

Behavioural facts established by the replay on this host: `hyprland-portals.conf`
(`default=hyprland;gtk`) is the only selected config; it is applied per interface via each
descriptor's `Interfaces=` line; `Secret` has no backend for the plain `Hyprland` value (`none`) and
is served by `gnome-keyring` only when the desktop list contains `gnome` (UseIn fallback); with no
`XDG_CURRENT_DESKTOP` there is no config at all and only gtk's built-in last resort resolves the 11
interfaces gtk implements.

## 6. Cross-check against the round-12 table (`corpus/knowledge/xdg-portal-routing-r12.md`)

The note has **16** interface rows (`:47-62`), not 14: `FileChooser`, `Screenshot`, `ScreenCast`,
`GlobalShortcuts`, `InputCapture`, `AppChooser`, `Print`, `Notification`, `Inhibit`, `Access`,
`Account`, `Email`, `DynamicLauncher`, `Lockdown`, `Settings` (`:61`), `Secret` (`:62`).

Rows that agree with the tool's host answer and the oracle's labels (all 16):
`FileChooser`, `AppChooser`, `Print`, `Notification`, `Inhibit`, `Access`, `Account`, `Email`,
`DynamicLauncher`, `Lockdown`, `Settings` → `gtk`; `Screenshot`, `ScreenCast`, `GlobalShortcuts`,
`InputCapture` → `hyprland`; `Secret` → no preferred backend (tool/oracle: `none` for `Hyprland`; the
note marks runtime `[UNK]`). 15 of these are exact backend predictions; `Secret` agrees in substance.

Rows the note lacks (5 of the 21; tool/oracle `none` for all of them): `Background`, `Wallpaper`,
`RemoteDesktop`, `Clipboard`, `Usb`.

Statements the tool/oracle contradict or refine:

1. **Declaration, not the note** — `claims-declaration-r90.md:14-16` describes the note as "a …
   routing table for 14 interfaces" and says it "does not list Secret, Background, Wallpaper,
   RemoteDesktop, Clipboard, Usb, Settings". The note actually has 16 rows and *does* list `Settings`
   (`:61`) and `Secret` (`:62`); the truly missing set is `Background`, `Wallpaper`, `RemoteDesktop`,
   `Clipboard`, `Usb` (5, not 7). Fix the declaration's inventory before the freeze.
2. `r12.md:37` — "`UseIn` is retained as descriptor data; the routing below follows the explicit
   preferred backend list … not a guess based on desktop labels." The oracle contradicts this as a
   general mechanism: `UseIn` **is** consulted as a fallback after the config lists. Reproducer:
   fixture `mode=xdg`, `files={}`, desktop `"Hyprland:GNOME"` → oracle label `Secret=["gnome-keyring"]`
   with reason `usein`; the tool prints the same. (No effect on the host's own `Hyprland` value, so the
   16 rows remain correct; the mechanism sentence is under-modelled.)
3. `r12.md:62` — the `Secret` explanation stops at "neither is named by `default=hyprland;gtk`; neither
   preferred descriptor declares it". The operative mechanism is the UseIn fallback: `none` because
   `gnome-keyring.portal` has `UseIn=gnome` and `kwallet.portal` has `UseIn=kde`, and gtk's last resort
   cannot serve `Secret` (absent from `gtk.portal`); with a `gnome` token, `gnome-keyring` wins. Same
   reproducer as (2).
4. `r12.md:20` records `xdg-desktop-portal-gtk 1.15.3-1`; installed today is `1.15.3-2`. Version drift
   only; the descriptor interface set is unchanged at replay time.
5. The note has no row or statement for the built-in gtk last resort. With desktop unset the oracle
   resolves 11 interfaces as `gtk-last-resort` and 10 as none; absent, not contradicted.

No statement in the note about a *backend* is contradicted by the tool or the oracle on the host's
`Hyprland` value.

## 7. Live session (read-only, `systemctl --user show`, exit 0)

```
Id=xdg-desktop-portal.service           ActiveState=active  MainPID=2680
Id=xdg-desktop-portal-hyprland.service  ActiveState=active  MainPID=2775
Id=xdg-desktop-portal-gtk.service       ActiveState=active  MainPID=2717
```

This is point state only: no D-Bus call, no logs, no environment read, no restart. It does not prove
which config the running daemon selected (its inherited `XDG_CURRENT_DESKTOP` was not read); that
remains unobserved, as in r12's own caveat.

## 8. Findings for the L1

| id | finding | action |
|---|---|---|
| H1 | `claims-declaration-r90.md:14-16` misstates the r12 note: 14 rows vs the actual 16, and claims `Settings`/`Secret` are absent when the note has both (`r12.md:61-62`). The real missing set is 5 (`Background`, `Wallpaper`, `RemoteDesktop`, `Clipboard`, `Usb`). | Correct the declaration text before freeze. Not a C1 defect. |
| H2 | `r12.md:37`'s "UseIn is not used for routing" is refuted by the oracle for multi-desktop values (fixture empty xdg, desktop `Hyprland:GNOME` → `Secret` = `gnome-keyring`, reason `usein`). | Corpus note refinement; optional recheck item. |
| H3 | `r12.md:62`'s `Secret` explanation omits the operative UseIn mechanism (and the gtk last-resort cannot cover `Secret`). Same reproducer as H2. | Corpus note refinement. |
| H4 | `r12.md:20`'s package snapshot says `xdg-desktop-portal-gtk 1.15.3-1`; host has `1.15.3-2`. | Recheck note on next portal package change; no routing change seen. |
| H5 | The tool prints the host config path twice (`configs=…,hyprland-portals.conf,…`). Faithful to upstream `xdp-portal-config.c:573-587` (no dedup; `/usr/share` in both `XDG_DATA_DIRS` and `DATADIR`); `--datadir /nonexistent` prints it once. | No action; do not "fix" the duplicate. |
| H6 | No C1 defect found on the host plane: 105/105 oracle decisions reproduced exactly (picks and reasons), across 5 desktop values, with the oracle's pinned tail digest and the installed binary's hash. | C1 host replay is clean (DRAFT). |

## 9. Limits

- DRAFT only: the declaration is unfrozen; the frozen cases/mutants define the measured predicate.
  Nothing here counts as a measurement, and no counter was executed.
- The oracle sees only the 21 interfaces the 1.22.1 binary queries at start-up and only the compiled
  `DATADIR=/usr/share` tail plus fixture roots; the replay therefore says nothing about backends
  installed outside that tail.
- "Resolved" means the configuration selects a backend; it does not prove the backend is running,
  answers D-Bus, or serves any request. The live daemon's actual environment was not read.
- `/usr/local/share/xdg-desktop-portal` and `/usr/local/etc/xdg-desktop-portal` were checked absent so
  that the tool's host search path and the oracle's fixture search path select the same files here;
  that equivalence is host-specific, not a general claim.
- Scratch paths: all writes under `/fast/scratch/hyaku/mado-r90/R90MExecHost`; bus/socket paths there
  are short (< 108 bytes `sun_path`).

## 10. Evidence retained, cleanup, installs

Retained under `.ufo/waves/round-90/w1/`:

- `R90MExecHost.md` (this report)
- `R90MExecHost-oracle-labels.json` — oracle's own labelled output for the 5-case batch
  (`host_tail_sha256=4a4cf319…`, `oracle_binary_sha256=e1429fbe…`)
- `R90MExecHost-evidence.json` — bundle: base rev, inventory commands/outputs (package list, `ls -la`,
  sha256, ownership, unit states), tool text + JSON outputs for all variants, the 21×5 comparison,
  the five strict single-case oracle runs with per-interface mismatches (all empty), and the r12
  comparison anchors.

Scratch `/fast/scratch/hyaku/mado-r90/R90MExecHost` was removed at exit (`rm -rf`); no scratch remains.
No tool install or upgrade was performed. No mutating git/jj command was run; the only git call was
`rev-parse HEAD`.

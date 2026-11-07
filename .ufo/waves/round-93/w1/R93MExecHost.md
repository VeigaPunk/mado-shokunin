# R93MExecHost — host replay (C1, read-only) + selftest harm baseline

Seat: R93MExecHost (leaf executor). Round mado 93, hyaku run 15 attempt 1, one v1 wave w1.
Base revision 4c6f723f3dca3a26f9d14475d695fe797e2e972c (master).
Candidate: `.ufo/waves/round-93/build/mado-portals.c1.py` sha256 89039e30d329bee82f20c4a32edc9fa72c02774c98364017e131a372c9fb91d3 (= round-92 build/mado-portals.d1.py).
Base tool: `tools/mado-portals.py` sha256 d1bd9b9a7c98f9e573bf8ba0594d796853f81539eed1d87052aa7906195e6ab1.
Oracle: `.ufo/waves/round-90/controls/portal-oracle-r90.py` (xdg-mode, private dbus-run-session, XDG_* roots in scratch; /usr/lib/xdg-desktop-portal sha256 e1429fbe1bf6c2203ba07f478b9e92e9221437b13a92eebafb0982748583a4f8, xdg-desktop-portal 1.22.1-2, glib2 2.90.1-1).

All runs labelled DRAFT (no freeze measurement, no receipts write).

## Axes (godspeed)

- **Coverage/edge**: agreement with installed xdg-desktop-portal on real host config across desktops (this seat's main axis).
- **Operability/robustness**: no divergence between base and candidate on host files (expected: byte-class classes have no host input, so no delta).
- **Harm baseline**: every lane tool's `--selftest` still passes at master and candidate (no regression introduced by candidate read).
- **Safety**: read-only host replay; oracle only via round-90 wrapper against scratch copy; no user session bus, no systemctl, no xdg-open/gio/launch, no sudo/pacman writes.

Moves kept: host-tail-only xdg cases (files {}) identical to round-90 case x01-host-tail-only, run through oracle in scratch; base/candidate both run `--desktop <D> --json` and plain. Move discarded: none.

## Host configuration inventoried (read-only)

`/usr/share/xdg-desktop-portal/`:
```
[preferred]
default=hyprland;gtk
```
`/usr/share/xdg-desktop-portal/gtk-portals.conf`: `[preferred] default=gtk`
`/usr/share/xdg-desktop-portal/portals/gtk.portal`: Interfaces=FileChooser;AppChooser;Print;Notification;Inhibit;Access;Account;Email;DynamicLauncher;Lockdown;Settings; UseIn=gnome
`/usr/share/xdg-desktop-portal/portals/hyprland.portal`: Interfaces=Screenshot;ScreenCast;GlobalShortcuts;InputCapture; UseIn=wlroots;Hyprland;sway;Wayfire;river;
`/usr/share/xdg-desktop-portal/portals/gnome-keyring.portal`: Interfaces=Secret; UseIn=gnome
`/usr/share/xdg-desktop-portal/portals/kwallet.portal`: Interfaces=Secret; UseIn=kde

`~/.config/xdg-desktop-portal/` absent (no user overrides). `/etc/xdg-desktop-portal/` absent.

Tool output (all desktops, base=candidate verbatim):
```
MADO_PORTALS: desktops=<...> backends=<...> configs=<...>
MADO_PORTAL: org.freedesktop.impl.portal.Lockdown -> ... (reason)
```
Full verbatim stdout for every desktop × both tools + oracle ordered dump is in `.ufo/waves/round-93/w1/R93MExecHost-host-run.txt` (32 KiB, sections `### tools/mado-portals.py desktop=<D> rc=0`, `### .ufo/waves/round-93/build/mado-portals.c1.py desktop=<D> rc=0`, `### oracle ordered dump`). Also: `host-cases.json`, `host-labels.json`, `oracle-ordered.txt`, `tool-outputs.txt` in same dir.

## Oracle run (DRAFT)

Command (from lane cwd):
```
TMPDIR="/fast/scratch/hyaku/mado-r93/R93MExecHost" python3 .ufo/waves/round-90/controls/portal-oracle-r90.py --cases /fast/scratch/hyaku/mado-r93/R93MExecHost/host-cases.json --label /fast/scratch/hyaku/mado-r93/R93MExecHost/host-labels.json --scratch-root /fast/scratch/hyaku/mado-r93/R93MExecHost/oracle
```
`host-cases.json` = 7 xdg-mode cases, each `{"mode":"xdg","desktop":<D>,"files":{}}` (host tail only, exactly the x01 pattern; no user files copied because none exist). Copied evidence host-cases/host-labels/oracle-ordered are in w1.

Result:
```
PORTAL_ORACLE cases=7 incomplete=0 host_tail_sha256=4a4cf31921e25dc6e60b283cc1aa1b79f743096bfdfc9dbb77df887c16f0fbf9
```
rc 0. Matches round-90 label file host_tail_sha256. Oracle binary sha256 verified e1429fbe...bf8.

Comparison rule: per interface, tool picks == oracle picks AND tool reason (normalising `none-key`/`no-backend`→None) == oracle_reason. 21 interfaces in oracle order: Lockdown, Access, Settings, FileChooser, AppChooser, Print, Notification, Inhibit, Screenshot, Background, Wallpaper, Account, Email, Secret, GlobalShortcuts, DynamicLauncher, ScreenCast, RemoteDesktop, Clipboard, InputCapture, Usb.

## Per-desktop result (all 21 interfaces)

Legend: `base=candidate=oracle` means agreement on all 21 picks+reasons. No disagreement found on any desktop.

### Hyprland / hyprland (identical)
- base=candidate on all 21; base=candidate=oracle on all 21.
- Picks: Lockdown/Access/FileChooser/AppChooser/Print/Notification/Inhibit/Account/Email/DynamicLauncher→gtk (default config), Settings→gtk (config), Screenshot/ScreenCast/GlobalShortcuts/InputCapture→hyprland (default config), Background/Wallpaper/Secret/RemoteDesktop/Clipboard/Usb→[] (None).
- Tool header: `MADO_PORTALS: desktops=hyprland backends=hyprland,gnome-keyring,gtk,kwallet configs=/usr/share/xdg-desktop-portal/hyprland-portals.conf,/usr/share/xdg-desktop-portal/hyprland-portals.conf`

### GNOME
- base=candidate=oracle on all 21.
- Picks: gtk interfaces→gtk (usein), Secret→gnome-keyring (usein), Screenshot/ScreenCast/GlobalShortcuts/InputCapture/Background/Wallpaper/RemoteDesktop/Clipboard/Usb→[].

### KDE
- base=candidate=oracle on all 21.
- Picks: gtk interfaces→gtk (gtk-last-resort), Secret→kwallet (usein), screenshot/screencast/etc→[].

### sway
- base=candidate=oracle on all 21.
- Picks: gtk→gtk (gtk-last-resort), Screenshot/ScreenCast/GlobalShortcuts/InputCapture→hyprland (usein), Secret→[] (None), others [].

### unknown
- base=candidate=oracle on all 21.
- Picks: gtk→gtk (gtk-last-resort), all non-gtk + Secret→[].

### Hyprland:GNOME
- base=candidate=oracle on all 21.
- Picks: hyprland-portals.conf default (gt k/hyprland set) + Secret→gnome-keyring (usein) via second desktop. Exactly the Hyprland set plus Secret gnome-keyring usein.

Per-interface dump (ordered) for each desktop is in host-run.txt `### oracle ordered dump` and oracle-ordered.txt; e.g. Hyprland oracle:
```
Lockdown ['gtk'] default config
Access ['gtk'] default config
Settings ['gtk'] config
FileChooser ['gtk'] default config
AppChooser ['gtk'] default config
Print ['gtk'] default config
Notification ['gtk'] default config
Inhibit ['gtk'] default config
Screenshot ['hyprland'] default config
Background [] None
Wallpaper [] None
Account ['gtk'] default config
Email ['gtk'] default config
Secret [] None
GlobalShortcuts ['hyprland'] default config
DynamicLauncher ['gtk'] default config
ScreenCast ['hyprland'] default config
RemoteDesktop [] None
Clipboard [] None
InputCapture ['hyprland'] default config
Usb [] None
```
(GNOME/KDE/sway/unknown/Hyprland:GNOME analogous, see files.)

Agreement check script result (DRAFT): all 7 desktops `base all-match True / cand all-match True` and `base==cand picks/reasons True` for every desktop. Candidate changes no observable on host files (expected: no invalid UTF-8 / 0x0B / repeated / locale keys in clean host tails).

## Selftest harm baseline (DRAFT, read-only)

Command: `python3 <tool> --selftest` (mako adds `--scratch-root /fast/scratch/hyaku/mado-r93/R93MExecHost`; tmp shell cwd = lane, env cleared per tool).

```
tools/mado-portals.py             rc=0 MADO_PORTALS_SELFTEST: checks=22 failed=0
.ufo/waves/round-93/build/mado-portals.c1.py rc=0 MADO_PORTALS_SELFTEST: checks=22 failed=0
tools/mado-mime.py                rc=0 MADO_MIME_SELFTEST: checks=17 failed=0
tools/mado-xdgmime.py             rc=0 MADO_XDGMIME_SELFTEST: checks=12 failed=0
tools/mado-mako.py                rc=0 MADO_MAKO_SELFTEST: checks=62 failed=0 (stdout empty, line on stderr)
quality/check-seat-reports.py     rc=0 SEAT_REPORTS_SELFTEST: checks=23 failed=0
```
Harm: none. Candidate selftest same line as base.

## Scratch & cleanup

All scratch under `/fast/scratch/hyaku/mado-r93/R93MExecHost/` (host-cases/labels/oracle/). Copied into w1: host-cases.json, host-labels.json, oracle-ordered.txt, oracle-dump.txt, tool-outputs.txt, verbatim-tool-and-oracle.txt, R93MExecHost-host-run.txt. Scratch directory deleted after copying (verified below).

## Findings

No bug, no disagreement. Candidate is observably identical to base on this host's real config across 7 desktops × 21 interfaces = 147 pick+reason pairs, all matching the oracle. No case file / control / candidate edited by this seat.

## Defects / risks

None found by this seat. Note: host config contains no invalid UTF-8 or 0x0B bytes, so this replay cannot exercise C1 byte classes (a)/(b); that coverage lives in the byte-class cases/generator, not the host replay. No install performed (nothing needed; bwrap 0.13.1, dbus-run-session present). No pacman run (guard).

Report: `.ufo/waves/round-93/w1/R93MExecHost.md`
Host run: `.ufo/waves/round-93/w1/R93MExecHost-host-run.txt`

# XDG Portal Routing and ScreenCast Lifecycle (MADO-R12-3)

source: [ref] — https://wiki.hypr.land/Hypr-Ecosystem/xdg-desktop-portal-hyprland/ — “Using the KDE File Picker With XDPH”; [ref] — https://flatpak.github.io/xdg-desktop-portal/docs/ — “XDG Desktop Portal”, “Backends”; [ref] — https://flatpak.github.io/xdg-desktop-portal/docs/portals.conf.html — “DESCRIPTION”, “FILE FORMAT”, “ENVIRONMENT”; [ref] — https://flatpak.github.io/xdg-desktop-portal/docs/requests.html — “General Flow”; [ref] — https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.ScreenCast.html — “Session lifecycle”, v6; [ref] — https://github.com/hyprwm/xdg-desktop-portal-hyprland/releases/tag/v1.4.1 — “Changes”
verified-at: 2026-10-19
recheck: 2027-01-17
covers: U3

## Question and evidence classes

This note answers which backend the current declared portal-routing configuration names for each interface, and what a ScreenCast lifecycle response would and would not establish.
The routing table is an inference from the observed `portals.conf` and installed backend descriptors, not a record of an app request or a backend-selection trace.
Upstream API descriptions below are documentation claims (`[INF-docs]`), never claims that this host completed those steps.
Local package, environment, unit, property, config, and descriptor reads are observations (`[OBS]`) recorded in `.ufo/evidence/round-12/portal-host.txt` under evidence ID `E-PT-PORTAL-HOST`.
`[INF]` marks conclusions derived from those observed files using the opened `portals.conf` selection rule.
`[UNK]` marks runtime behavior not measured by these reads.
The sources fragment `.ufo/round-12/sources/portal.md` maps the `S@PT*` citations to opened sources and exact quote gates.

## Local snapshot — 2026-10-19

[OBS] `pacman -Q` reports `xdg-desktop-portal 1.22.1-2`, `xdg-desktop-portal-hyprland 1.4.1-2`, and `xdg-desktop-portal-gtk 1.15.3-1` (E-PT-PORTAL-HOST/P1).
[OBS] The shell environment read by `printf` has `XDG_CURRENT_DESKTOP=Hyprland` and `XDG_CONFIG_HOME=/home/vgpnk/.config`; `XDG_CONFIG_DIRS=/etc/xdg`, `XDG_DATA_HOME=/home/vgpnk/.local/share`, and `XDG_DATA_DIRS=/usr/local/share:/usr/share` (E-PT-PORTAL-HOST/P2).
[OBS] The read-only path sweep found no portal override directories under the observed config/data roots, `/etc/xdg-desktop-portal`, or `/usr/local/etc/xdg-desktop-portal`; `/usr/share/xdg-desktop-portal` contains `hyprland-portals.conf`, `gtk-portals.conf`, and the listed backend descriptors (E-PT-PORTAL-HOST/P3).
[OBS] All three queried user units were `active`: `xdg-desktop-portal.service`, `xdg-desktop-portal-hyprland.service`, and `xdg-desktop-portal-gtk.service` (E-PT-PORTAL-HOST/P6).
[OBS] The public ScreenCast D-Bus `version` property returned `u 6`; `AvailableSourceTypes` returned `u 7` (E-PT-PORTAL-HOST/P6).
[INF-docs] The ScreenCast documentation defines the current interface as v6 and source-type bits 1=MONITOR, 2=WINDOW, 4=VIRTUAL; therefore the observed value 7 has all three documented bits set ([ref], “Properties” / “AvailableSourceTypes”).
The property values describe advertised interface metadata only; they do not show a selected source, permission, an open stream, or a captured frame ([ref], “AvailableSourceTypes”, “Session lifecycle”; E-PT-PORTAL-HOST/P6).

## Which configuration is selected

[OBS] `/usr/share/xdg-desktop-portal/hyprland-portals.conf:1-2` contains `[preferred]` and `default=hyprland;gtk`; `/usr/share/xdg-desktop-portal/gtk-portals.conf:1-2` separately contains `[preferred]` and `default=gtk` (E-PT-PORTAL-HOST/P4).
[INF-docs] `portals.conf` says the desktop-specific file name uses the lower-case desktop name from `XDG_CURRENT_DESKTOP`; a desktop-specific file takes precedence over a generic `portals.conf`, and user/system config roots are searched before data roots ([ref], “DESCRIPTION”, “SYNOPSIS”, “ENVIRONMENT”).
[INF] Given the observed `Hyprland` desktop value and the documented case-folding rule, the Hyprland profile is the matching desktop-specific file; the read-only sweep found no higher-precedence matching user or `/etc` override (E-PT-PORTAL-HOST/P2-P4; [ref], “DESCRIPTION”).
[UNK] The shell environment sample does not independently prove which environment the running portal service inherited; this inference is conditional on its using the observed desktop value (E-PT-PORTAL-HOST/P2; P6).
`default=hyprland;gtk` is the ordered candidate list for every interface without an explicit per-interface key; the local file has no per-interface key (E-PT-PORTAL-HOST/P4; [ref], “FILE FORMAT”).
[INF-docs] The configuration manual defines each backend list as the implementations searched in order for the requested interface ([ref], “FILE FORMAT”).
[OBS] The installed `hyprland.portal` and `gtk.portal` descriptors declare their implementation-interface sets on line 3; the same evidence records each descriptor’s `DBusName` and `UseIn` lines (E-PT-PORTAL-HOST/P5).
`UseIn` is retained as descriptor data; the routing below follows the explicit preferred backend list plus each descriptor’s `Interfaces=` declaration, not a guess based on desktop labels (E-PT-PORTAL-HOST/P4-P5; [ref], “FILE FORMAT”).

## Per-interface routing table

Each row is `[INF]`: it maps the `org.freedesktop.impl.portal.*` identifier advertised in the `.portal` descriptor to its public portal name.
The configuration preference is `hyprland` then `gtk` (`hyprland-portals.conf:1-2`); matching interface lists are the exact `Interfaces=` lines in `hyprland.portal:3` and `gtk.portal:3` (E-PT-PORTAL-HOST/P4-P5).
The inference is a configuration-based candidate route, not observed request dispatch; backend activation or application-specific behavior may affect an actual request ([ref], “DESCRIPTION” / “FILE FORMAT”; E-PT-PORTAL-HOST/P6).

| Public interface | Config-derived candidate | Evidence for match |
|---|---|---|
| `FileChooser` | GTK, second candidate | GTK descriptor includes `org.freedesktop.impl.portal.FileChooser`; XDPH does not. The XDPH wiki says its file picker fallback is GTK by default (E-PT-PORTAL-HOST/P5; [ref], “Using the KDE File Picker With XDPH”). |
| `Screenshot` | XDPH, first candidate | XDPH descriptor includes `org.freedesktop.impl.portal.Screenshot`; GTK descriptor does not (E-PT-PORTAL-HOST/P4-P5). |
| `ScreenCast` | XDPH, first candidate | XDPH descriptor includes `org.freedesktop.impl.portal.ScreenCast`; GTK descriptor does not (E-PT-PORTAL-HOST/P4-P5). |
| `GlobalShortcuts` | XDPH, first candidate | XDPH descriptor includes `org.freedesktop.impl.portal.GlobalShortcuts`; GTK descriptor does not (E-PT-PORTAL-HOST/P4-P5). |
| `InputCapture` | XDPH, first candidate | XDPH descriptor includes `org.freedesktop.impl.portal.InputCapture`; GTK descriptor does not (E-PT-PORTAL-HOST/P4-P5). |
| `AppChooser` | GTK, second candidate | GTK descriptor includes `org.freedesktop.impl.portal.AppChooser`; XDPH does not (E-PT-PORTAL-HOST/P4-P5). |
| `Print` | GTK, second candidate | GTK descriptor includes `org.freedesktop.impl.portal.Print`; XDPH does not (E-PT-PORTAL-HOST/P4-P5). |
| `Notification` | GTK, second candidate | GTK descriptor includes `org.freedesktop.impl.portal.Notification`; XDPH does not (E-PT-PORTAL-HOST/P4-P5). |
| `Inhibit` | GTK, second candidate | GTK descriptor includes `org.freedesktop.impl.portal.Inhibit`; XDPH does not (E-PT-PORTAL-HOST/P4-P5). |
| `Access` | GTK, second candidate | GTK descriptor includes `org.freedesktop.impl.portal.Access`; XDPH does not (E-PT-PORTAL-HOST/P4-P5). |
| `Account` | GTK, second candidate | GTK descriptor includes `org.freedesktop.impl.portal.Account`; XDPH does not (E-PT-PORTAL-HOST/P4-P5). |
| `Email` | GTK, second candidate | GTK descriptor includes `org.freedesktop.impl.portal.Email`; XDPH does not (E-PT-PORTAL-HOST/P4-P5). |
| `DynamicLauncher` | GTK, second candidate | GTK descriptor includes `org.freedesktop.impl.portal.DynamicLauncher`; XDPH does not (E-PT-PORTAL-HOST/P4-P5). |
| `Lockdown` | GTK, second candidate | GTK descriptor includes `org.freedesktop.impl.portal.Lockdown`; XDPH does not (E-PT-PORTAL-HOST/P4-P5). |
| `Settings` | GTK, second candidate | GTK descriptor includes `org.freedesktop.impl.portal.Settings`; XDPH does not (E-PT-PORTAL-HOST/P4-P5). |
| `Secret` | No matching preferred candidate evidenced | Both `gnome-keyring.portal` and `kwallet.portal` declare `org.freedesktop.impl.portal.Secret`, but neither is named by `default=hyprland;gtk`; neither preferred descriptor declares it (E-PT-PORTAL-HOST/P4-P5). |

The XDPH guide independently states that XDPH does not implement a file picker and that GTK is its default fallback; this agrees with the local descriptor/config inference, not a live `FileChooser` request result ([ref], “Using the KDE File Picker With XDPH”; E-PT-PORTAL-HOST/P4-P5).
For `Secret`, the files establish the declared candidates, not whether some different frontend fallback or runtime condition serves a call; actual behavior remains `[UNK]` (E-PT-PORTAL-HOST/P4-P5; [ref], “FILE FORMAT”).

## ScreenCast v6 lifecycle and proof boundaries

[INF-docs] ScreenCast v6 describes the public portal API; portal requests generally return a Request handle and later a `Response` signal after interaction, rather than completing a potentially long interaction in the method reply ([ref], “General Flow”; [ref], “Session lifecycle”).
The `Owner / initiator` column below names the API layer whose action is being described; it does not identify a host implementation by runtime trace ([ref], “General Flow”; [ref], “Session lifecycle”).

| Stage | Initiating / owning layer | Documented transition | What a successful result proves — and does not prove |
|---|---|---|---|
| `CreateSession()` | App calls the public ScreenCast portal; frontend routes the interface to a configured implementation | Request object handle, then `Response` carrying a session handle; the session may later close ([ref], “General Flow”; [ref], “CreateSession”) | The portal accepted session creation and returned a handle. It does not prove source selection, permission to capture, or a live stream. |
| `SelectSources()` | App configures the session through the ScreenCast API | Select the source types/cursor options before start; only one selection attempt per session ([ref], “SelectSources”) | An accepted configuration records what to ask for; it does not prove that a user approved capture or that streams exist. |
| `Start()` | App requests start; selected backend and portal coordinate the documented user-facing interaction | Typically presents a dialog; successful `Response` returns PipeWire stream metadata ([ref], “Start”; [ref], “General Flow”) | A successful portal response establishes that Start completed with returned stream metadata. It does not prove that a fresh dialog appeared—persistent sessions exist—or that the client attached to a stream ([ref], “Session persistence”, “PipeWire streams”). |
| `OpenPipeWireRemote()` | App calls the portal for the existing session | Returns a file descriptor for the PipeWire remote where the ScreenCast stream nodes are available ([ref], “OpenPipeWireRemote”) | The returned descriptor establishes access to that session’s PipeWire remote; it does not prove the app connected to the right node or received frames. |

In v6, stream tuples still contain node IDs for compatibility, but node IDs are deprecated for targeting because they can be reused; consumers should prefer `pipewire-serial` with `PW_KEY_TARGET_OBJECT` ([ref], “PipeWire streams”).
The local D-Bus `version=6` observation agrees with the documented interface version; `AvailableSourceTypes=7` is a property read and not any stage of this lifecycle (E-PT-PORTAL-HOST/P6; [ref], “Properties”).

## How to distinguish a portal request from service health

`systemctl --user is-active` is a point observation of each unit’s state; it does not exercise an app request or certify that a backend accepted a particular interface (E-PT-PORTAL-HOST/P6).
A config file and matching `.portal` descriptor establish a declared route candidate; a per-request response is needed to observe whether a specific app request completed ([ref], “DESCRIPTION” / “FILE FORMAT”; [ref], “General Flow”).
A successful `Start` response and stream metadata are different evidence from `OpenPipeWireRemote()` returning a descriptor, which is different again from an app connecting and receiving frames ([ref], “Start”, “OpenPipeWireRemote”).
A request `Response` with results is the documented place to inspect the user interaction outcome; no method/request was issued during this inspection ([ref], “General Flow”; E-PT-PORTAL-HOST/P6).

The installed XDPH package version is `1.4.1-2`, matching upstream tag `v1.4.1`; that release describes a Screencopy `cursor_mode` option and a loop-hangup fix, not an end-to-end capture guarantee (E-PT-PORTAL-HOST/P1; [ref], “Changes”).
This version match is identity/context only; the host’s property read and configuration do not reveal which application has asked for ScreenCast or whether any session exists (E-PT-PORTAL-HOST/P1-P6).

## Existing playbook foothold

`SKILL.md:73-75` already points to `~/.config/hypr/xdph.conf` as the screen-share-picker config; `SKILL.md:100-108` directs read-only investigation toward the `sunset / xdph` surface and identifies the portal as a separate consumer (repo anchor: `SKILL.md:73-75,100-108`).
This entry links that foothold to the portal-routing and ScreenCast API layers; it does not edit or override the skill text.

## Limits

[OBS] The measured units are active and the inspected properties/config files have the values recorded above; these are bounded host observations from 2026-10-19 (E-PT-PORTAL-HOST/P1-P6).
[INF] The selected config profile and route candidates follow the observed environment, file search sweep, preferred backend order, and `Interfaces=` declarations (E-PT-PORTAL-HOST/P2-P5; [ref], “DESCRIPTION” / “FILE FORMAT”).
[INF-docs] The lifecycle table describes what the documented API stages return, not what this host or any app has done ([ref], “General Flow”; [ref], “Session lifecycle”).
[UNK] No portal request was issued, no chooser or consent dialog was opened, no ScreenCast session was created, no source was selected, and no PipeWire fd or stream was obtained during this work (E-PT-PORTAL-HOST/P6 and the read-only command inventory).
A running `xdg-desktop-portal` service or a valid `portals.conf` is not evidence that capture succeeded, consent was granted, a source is available to a caller, or pixels reached the application (E-PT-PORTAL-HOST/P3-P6; [ref], “General Flow”; [ref], “Session lifecycle”).
The `version` and `AvailableSourceTypes` properties do not answer whether a caller’s permission persists, whether a stream is active, or whether a PipeWire consumer is connected (E-PT-PORTAL-HOST/P6; [ref], “Session persistence”, “PipeWire streams”).
The table covers interfaces declared by the inspected installed descriptors, not every portal interface that could be installed or added later (E-PT-PORTAL-HOST/P5).
[UNK] The portal daemon’s exact inherited environment was not read; the profile selection inference assumes its `XDG_CURRENT_DESKTOP` corresponds to the observed shell value (E-PT-PORTAL-HOST/P2; [ref], “ENVIRONMENT”).
The GTK fallback conclusion applies to the declared preference and installed interface list; no application-specific portal request was made to observe fallback in operation (E-PT-PORTAL-HOST/P4-P6; [ref], “Using the KDE File Picker With XDPH”).
The `Secret` interface’s runtime provider is not established by the preferred candidate descriptors alone (E-PT-PORTAL-HOST/P4-P5).
A D-Bus property value and a service’s `active` state are snapshots, not durable claims about future sessions or subsequent package/config changes (E-PT-PORTAL-HOST/P1-P6).
No window title, `hyprland.log` content, instance signature, request/session material, or private data was read or retained (read-only scope for E-PT-PORTAL-HOST).

## Rejected

**Rejected M03:** “XDPH supplies every portal interface, including FileChooser.” The installed XDPH descriptor lists Screenshot, ScreenCast, GlobalShortcuts, and InputCapture but not FileChooser; the GTK descriptor lists FileChooser; the Hyprland profile orders GTK after XDPH; and the XDPH wiki explicitly documents GTK as its default file-picker fallback (E-PT-PORTAL-HOST/P4-P5; [ref], “Using the KDE File Picker With XDPH”).
The rejection is about declared backend scope and the configured candidate route, not a claim that a live file picker was exercised.
**Rejected:** “All three portal units are active, so screen capture is working.” Active state does not prove a request, a completed `Start`, a PipeWire connection, or received frames; none was tested (E-PT-PORTAL-HOST/P6; [ref], “General Flow”; [ref], “Session lifecycle”).
**Rejected:** “`AvailableSourceTypes=7` means this app has permission to capture all source types.” The property is a documented capability bitmask, not a response to a specific app’s `Start` request or user interaction (E-PT-PORTAL-HOST/P6; [ref], “AvailableSourceTypes”, “Start”).

## Recheck

Re-open the configuration manual and the current installed descriptors after a portal package, desktop-environment, or routing-file change; the selected profile depends on `XDG_CURRENT_DESKTOP` and configuration precedence ([ref], “DESCRIPTION” / “ENVIRONMENT”).
Re-check the installed backend release before reusing version-specific capability claims; the v1.4.1 release page is scoped to that tag ([ref], “Changes”).
Any future runtime claim needs a separately authorized app-driven request observation; this read-only note does not authorize requests, dialogs, consent, or capture ([ref], “General Flow”; [ref], “Session lifecycle”).

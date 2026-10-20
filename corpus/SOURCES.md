# SOURCES — where mado learns

Contract v1: canonical `CORPUS.md` § SOURCES.md (kaika provenance retained).
Claim admission stays in `QUALITY.md`; research method stays chousa's.
Original rows were opened 2026-10-19; round-13 additions and reopens are
recorded in `lessons/round-13.md` § Gate. Only `status`, `recheck` and
`used-by` change in place, each logged old→new in that round's lesson.

## Registry

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S001 | mado round-10 lesson — method lessons (arc-synthesis lesson) — corpus/lessons/round-10.md | own-work | A | mado method discipline: re-derivable documents, (claim, command) pairs, gap cost | corpus/lessons/round-10.md:63-123 @ a6528e6 (sha256 d7b4708e864fca29…) | what survives a lane is the (claim, command) pair; cites the synthesis re-derivation protocol as the worked pattern round-12 calibrates against | mined | 2026-10-19 | 180d | corpus/lessons/round-12.md |
| S002 | mado arc synthesis — §6 gap ledger — corpus/knowledge/arc-synthesis.md | own-work | A | the arc's named-UNKNOWN surface inventory (U1 window-rule/dispatcher ground) | corpus/knowledge/arc-synthesis.md:290-307 §6 @ a6528e6 (sha256 a5b4833141461810…) | names the surfaces never made verdict-bearing (window-rule effects, dispatcher behaviour, exec-once results) with the reason per row — the U1 gap's own anchor text | mined | 2026-10-19 | 180d | corpus/knowledge/window-rule-effects-getprop.md |
| S003 | shokunin PROTOCOL.md — §Evidence standard + §Gate standard (fleet root) | spec | A | the register/gate/evidence requirements every round-12 artifact is graded against | PROTOCOL.md:328-358 + :360-408 @ fleet 31baf5c (sha256 b1d4f4c094052298…) | gate-vs-probe boundary, self-test as capability not measurement, two-evidence rule, closure-time pointer rule — the standard the lane's gate and its citations must satisfy | mined | 2026-10-19 | on-change | corpus/lessons/round-12.md |
| S004 | kaika SOURCES contract v1 — .ufo/waves/kaika/SOURCES-CONTRACT-v1.md (fleet-ledger) | spec | A | SOURCES.md row shape, tier scoping, status lifecycle, search-log duty | Rules 1-6 + Census block @ fleet-ledger 5b471e4 (sha256 6c674a2281afb75b…) | row-only-after-opening, tier scoped never global, rejected rows kept as taste evidence, 11-column shape — the rule set this fragment and the integrator's merge follow | mined | 2026-10-19 | on-change | corpus/lessons/round-12.md |
| S005 | wayland-protocols README — https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/main/README.md | docs | A | wayland protocol phasing and change policy (ground for later U4/U6 rounds) | README.md §Protocol phases @ main 3dac056d (2026-01-16, last commit touching README.md) | experimental/staging/stable semantics: what may break in each phase, deprecation, legacy z-prefix; gives the vocabulary to age-check a protocol claim | mined | 2026-10-19 | on-release | corpus/knowledge/wayland-protocol-boundaries-r13.md |
| S006 | Wayland debugging extras — https://wayland.freedesktop.org/extras.html | docs | A | which Wayland debugging surface exists (compositor globals, protocol dumps) | §Compositor features + §Protocol dumpers (freedesktop.org, opened 2026-10-19) | wayland-info lists advertised globals; WAYLAND_DEBUG and middle-man dumpers/proxies exist — spawn-direction material for a future diagnostic lane, no host fact | queued | 2026-10-19 | 180d | — |
| S007 | libinput helper tools — https://wayland.freedesktop.org/libinput/doc/latest/tools.html | docs | A | input-layer debugging route (libinput 1.32.0) | §Helper tools + §libinput record and replay, libinput 1.32.0 documentation (opened 2026-10-19) | debug-events/record/replay visualize and replay kernel input events; most tools need root and /dev/input/event* access — scopes what an input probe could ever measure | queued | 2026-10-19 | 180d | — |
| S008 | The Wayland Protocol (DeVault) — high-level design chapter — https://wayland-book.com/introduction/high-level-design.html | book | B | Wayland architecture concepts: compositor role, userspace component map | §High-level design chapter of a draft book (opened 2026-10-19) | compositor dispatches input and composites output; libinput/xkbcommon/libdrm/GBM/KMS roles named — concept ground for U4/U6, never a host fact | queued | 2026-10-19 | 180d | — |
| S009 | Wayland Architecture — https://wayland.freedesktop.org/architecture.html | docs | A | the X-vs-Wayland event path and rendering model (official project page) | §Wayland Architecture + §Wayland Rendering (freedesktop.org, opened 2026-10-19) | step-by-step event path showing the compositor is the display server; direct-rendering buffer model — architecture ground with citable per-step language | queued | 2026-10-19 | 180d | — |
| S010 | Wayland Explorer — https://wayland.app/protocols/ | community | C | protocol-document discovery index (community-maintained) | index/overview page (wayland.app, opened 2026-10-19) | browsable index of core and per-compositor protocol docs by phase; a discovery aid only — community tier, never sole support for an admitted entry | queued | 2026-10-19 | 180d | — |
| S011 | fleet-ledger MANIFEST.json — mado round verdicts — .tower/worktrees/kaika/fleet-ledger/MANIFEST.json | dataset | C | mado per-round verdict attribution (as axis history) | rounds[] lane=mado verdicts, MANIFEST.json:1757-1768 (verdict keys :1763-1765, notes :1767) @ fleet-ledger 959b746 (sha256 1c8e4f11fd113e35…) | REJECTED: verdicts are integrator-recorded axis keys with no claim binding; re-measured 2026-10-19: 45 improved keys via jq, 28 manifest-only against SCORECARD.md:11-26 (dossier §2.2 matched). flip: verdict keys bound to per-round re-runnable output plus the claimed axis named | rejected | 2026-10-19 | 180d | — |
| S012 | Hyprland Events Automation (Filip Mikina) — https://filipmikina.com/blog/hyprwhenthen | community | C | Hyprland window-rule era semantics | post body + FAQ, published 2025-09-15 (opened 2026-10-19) | REJECTED: third-party restatement naming no Hyprland version anywhere in the full page (335 lines read); its rule-era statements cannot bind to an era. flip: a version-pinned rewrite (version plus changelog or source anchor) of the same automation | rejected | 2026-10-19 | 180d | — |
| S013 | gkeep installer — `/home/vgpnk/Projects/gkeep/install.sh` | code | A | Provenance scope: operator installer actions corresponding to the measured gkeep Hyprland and Waybar deltas | `HEAD` 133b86717a02548aeaff3f1411bf301d936c5308; `install.sh:21-36,60-82,88-90`; worktree SHA equals `HEAD:install.sh` | Connects installer code paths to the observed copied Hypr config, include append, Waybar module, CSS, and reload calls without executing them | mined | 2026-10-19 | on-change | corpus/knowledge/config-drift-r12.md |
| S014 | mado gate — `tools/mado-verify.sh` | own-work | A | Round-12 gate re-anchor: pinned Hyprland EXPECT source list and local LOCAL inventory | `Erratum (round 12, 2026-10-19)` comment directly above `declare -a EXPECT`; EXPECT gains `~/.config/hypr/gkeep.conf`; LOCAL unchanged (12); gate sha 83b3f5f1… → final bytes at the round commit | Shows which pinned list was re-anchored (EXPECT only) and why LOCAL stayed narrow, so the remaining set-blind census stays visible | mined | 2026-10-19 | on-gate-change | corpus/knowledge/config-drift-r12.md |
| S015 | mado drift protocol — `corpus/knowledge/omarchy-drift-watch.md` | own-work | A | Append-only re-anchor protocol for moved pins | `## Errata (append-only)`, lines 284-287; M6-2 round 6 | A moved pin is reported, then re-anchored with old/new values, reason and re-measure command rather than silently smoothed | mined | 2026-10-19 | on-change | corpus/knowledge/config-drift-r12.md |
| S016 | Using hyprctl — https://wiki.hypr.land/Configuring/Advanced-and-Cool/Using-hyprctl/ | docs | A | Current wiki's `getprop` purpose and invocation form | `#getprop`; page marked Latest git; modified 2026-08-26; opened 2026-10-19 | Separates the current documented property-read command from command effects; does not pin host behavior | mined | 2026-10-19 | 90d | corpus/knowledge/window-rule-effects-getprop.md |
| S017 | Window Rules — https://wiki.hypr.land/Configuring/Basics/Window-Rules/ | docs | A | Current latest-git Lua-era syntax and documented effect semantics, scoped to that wiki era | `#syntax`, `#effects`, `#notes`; page says hyprlang deprecated since 0.55; modified 2026-08-26; opened 2026-10-19 | Teaches to separate match conditions from effects, and to label current-doc semantics rather than projecting them onto a 0.56.2 host | mined | 2026-10-19 | 90d | corpus/knowledge/window-rule-effects-getprop.md, corpus/knowledge/hyprland-config-era-r12.md, corpus/lessons/round-13.md |
| S018 | Hyprland v0.56.2 source — https://github.com/hyprwm/Hyprland/blob/v0.56.2/src/debug/HyprCtl.cpp | code | A | Exact tagged `getprop` dispatch, window selector, error paths, and opacity property getters | `dispatchGetProp`, lines 1463-1645; tag commit efb50993780079460b0cbed1363e2166a2de1d9f | Teaches which window-rule applicator values the pinned handler returns, without attributing a result to a rule | mined | 2026-10-19 | on-release | corpus/knowledge/window-rule-effects-getprop.md |
| S019 | Host read-only getprop capture — .ufo/evidence/round-12/getprop-help.txt and .ufo/evidence/round-12/getprop-measure.txt | own-work | A | Host Hyprland 0.56.2 help, errors, selector behavior, property values and defaults | `.ufo/evidence/round-12/getprop-help.txt` and `.ufo/evidence/round-12/getprop-measure.txt`, commands dated 2026-10-19 | Teaches an operator how to repeat the read-only host probe while excluding window titles | mined | 2026-10-19 | 90d | corpus/knowledge/window-rule-effects-getprop.md |
| S020 | Omarchy default Hyprland window rules — /home/vgpnk/.local/share/omarchy/default/hypr/windows.conf and /home/vgpnk/.local/share/omarchy/default/hypr/apps/terminals.conf | code | A | Host-declared generic and terminal opacity effects | `windows.conf:5-15`; `apps/terminals.conf:2-4`, files opened 2026-10-19 | Teaches that an observed opacity value may be consistent with multiple declared rules and cannot alone identify the matching rule | mined | 2026-10-19 | on-change | corpus/knowledge/window-rule-effects-getprop.md |
| S021 | Hyprland 0.53 dropped! — https://hypr.land/news/update53/ | docs | A | 0.53 window-rule migration | “Breaking changes”; announcement dated 2025-12-29 | Identifies the explicit windowrule syntax-breaking boundary and required migration. | mined | 2026-10-19 | on-release | corpus/knowledge/hyprland-config-era-r12.md |
| S022 | Hyprland Wiki v0.54 Start — https://wiki.hypr.land/0.54.0/Configuring/Start/ | docs | A | Legacy hyprlang config location and explicit selector | “Start”; v0.54.0 archive, page modified 2025-10-29 | Anchors the pre-Lua default filename and documents an explicit config selector. | mined | 2026-10-19 | on-release | corpus/knowledge/hyprland-config-era-r12.md |
| S023 | Hyprland Wiki v0.54 Window Rules — https://wiki.hypr.land/0.54.0/Configuring/Window-Rules/ | docs | A | Post-0.53 legacy window-rule grammar | “Syntax”; v0.54.0 archive, page modified 2026-01-21 | Preserves the versioned hyprlang rule grammar after the 0.53 rewrite. | mined | 2026-10-19 | on-release | corpus/knowledge/hyprland-config-era-r12.md |
| S024 | Lua-ification of Hyprland configs — https://hypr.land/news/26_lua/ | docs | A | Lua introduction, config selection, hyprlang support window | “Lua configs” and “Old hyprlang syntax”; 2026-04-26 | Gives the maintainer’s exact startup-selection behavior and legacy-support promise. | mined | 2026-10-19 | on-release | corpus/knowledge/hyprland-config-era-r12.md |
| S025 | Hyprland 0.55 announcement — https://hypr.land/news/update55/ | docs | A | 0.55 forward configuration surface | “Lua configs” and “Breaking changes”; 2026-05-09 | Distinguishes the new Lua direction from immediate hyprlang rejection. | mined | 2026-10-19 | on-release | corpus/knowledge/hyprland-config-era-r12.md |
| S026 | Hyprland v0.55.0 release — https://github.com/hyprwm/Hyprland/releases/tag/v0.55.0 | docs | A | 0.55 window-rule capability additions | “New features”; v0.55.0 tag, released 2026-05-09 | Pins the additive `confine_pointer` rule change to the exact release. | mined | 2026-10-19 | on-release | corpus/knowledge/hyprland-config-era-r12.md |
| S027 | Hyprland 0.56 announcement — https://hypr.land/news/update56 | docs | A | 0.56 breaking-change statement and rule additions | Opening paragraph and “Other”; 2026-07-20 | Separates the release’s no-breaking-change statement from its new rule surface. | mined | 2026-10-19 | on-release | corpus/knowledge/hyprland-config-era-r12.md |
| S028 | Hyprland v0.56.2 release — https://github.com/hyprwm/Hyprland/releases/tag/v0.56.2 | docs | A | 0.56.2 rule behavior fix | “Fixes backported”; v0.56.2 tag, released 2026-08-05 | Shows why patch-level window-rule behavior must be rechecked. | mined | 2026-10-19 | on-release | corpus/knowledge/hyprland-config-era-r12.md |
| S029 | Hyprland Wiki Configuring Start — https://wiki.hypr.land/Configuring/Start/ | docs | A | Current Lua config path and language status | Introductory note and config location; page modified 2026-08-26 | Anchors the current Lua default path and the wiki’s post-0.55 status label. | mined | 2026-10-19 | on-release | corpus/knowledge/hyprland-config-era-r12.md |
| S030 | Hyprland Wiki Window Rules — https://wiki.hypr.land/Configuring/Basics/Window-Rules/ | docs | A | Current Lua window-rule syntax | “Syntax”; page modified 2026-08-26 | Provides a current Lua example to contrast with the v0.54 hyprlang form. | rejected | 2026-10-19 | on-release | — |
| S031 | Hyprland Wiki: xdg-desktop-portal-hyprland — https://wiki.hypr.land/Hypr-Ecosystem/xdg-desktop-portal-hyprland/ | docs | A | XDPH role, FileChooser limitation, GTK fallback, debugging route | “Using the KDE File Picker With XDPH”, “Debugging”; page modified 2026-08-26 | Check XDPH interface scope and GTK file-picker fallback against the declared route before interpreting service presence. | mined | 2026-10-19 | 90d | corpus/knowledge/xdg-portal-routing-r12.md |
| S032 | XDG Desktop Portal documentation — https://flatpak.github.io/xdg-desktop-portal/docs/ | docs | A | Portal frontend and desktop-specific backend model | “XDG Desktop Portal”, “Backends”; accessed 2026-10-19 | Separate the shared portal API surface from desktop backend implementations. | mined | 2026-10-19 | 90d | corpus/knowledge/xdg-portal-routing-r12.md |
| S033 | portals.conf — https://flatpak.github.io/xdg-desktop-portal/docs/portals.conf.html | docs | A | Desktop-specific configuration precedence and per-interface backend selection | “DESCRIPTION”, “FILE FORMAT”, “ENVIRONMENT”; accessed 2026-10-19 | Derive route candidates from the selected desktop profile and its ordered backend list. | mined | 2026-10-19 | 90d | corpus/knowledge/xdg-portal-routing-r12.md |
| S034 | Portal Requests — https://flatpak.github.io/xdg-desktop-portal/docs/requests.html | docs | A | Asynchronous portal request handle and Response signal lifecycle | “General Flow”; accessed 2026-10-19 | Distinguish a D-Bus method reply from the later result of a user-interaction request. | mined | 2026-10-19 | 90d | corpus/knowledge/xdg-portal-routing-r12.md |
| S035 | ScreenCast portal — https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.ScreenCast.html | spec | A | ScreenCast v6 lifecycle, properties, PipeWire streams and stream targeting | “Session lifecycle”, “AvailableSourceTypes”, “PipeWire streams”; interface version 6; accessed 2026-10-19 | Separate session setup, source selection, Start response, and PipeWire remote access as distinct proof stages. | mined | 2026-10-19 | on-release | corpus/knowledge/xdg-portal-routing-r12.md |
| S036 | RemoteDesktop portal — https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.RemoteDesktop.html | spec | A | RemoteDesktop v2 lifecycle and ScreenCast cross-portal integration | “Session lifecycle”, “Cross-portal integration”; interface version 2; accessed 2026-10-19 | Keep remote input permissions and remote-desktop sessions distinct from ScreenCast-only sessions. | queued | 2026-10-19 | on-release | — |
| S037 | xdg-desktop-portal-hyprland v1.4.1 — https://github.com/hyprwm/xdg-desktop-portal-hyprland/releases/tag/v1.4.1 | docs | A | Installed XDPH upstream release identity and release-scoped changes | “v1.4.1”, “Changes”; tag commit cc8e5ef; released 2026-07-29 | Pin version-specific XDPH observations to the installed release; release notes do not establish capture success. | mined | 2026-10-19 | on-release | corpus/knowledge/xdg-portal-routing-r12.md |
| S038 | xdg-desktop-portal 1.21.0 — https://github.com/flatpak/xdg-desktop-portal/releases/tag/1.21.0 | docs | A | Frontend release feature context for GlobalShortcuts and other portal APIs | “New Features”; tag 1.21.0, marked pre-release; accessed 2026-10-19 | Check release status before using a frontend feature note as an installed-version claim. | queued | 2026-10-19 | on-release | — |
| S039 | xdg-desktop-portal 1.22.0 — https://github.com/flatpak/xdg-desktop-portal/releases/tag/1.22.0 | docs | A | Frontend release fixes affecting Dynamic Launcher and FileChooser/OpenURI document paths | “Bug Fixes”; tag 1.22.0; accessed 2026-10-19 | Use exact release notes to anchor path-handling changes without inferring runtime behavior. | queued | 2026-10-19 | on-release | — |
| S040 | wayland-protocols governance — https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/35d9638cf0c3f0bbf0c42996580a284f3d8ce564/GOVERNANCE.md | spec | A | Namespace-specific protocol inclusion and promotion authority, not runtime support | §2.1, §2.2, §2.3 @ 35d9638cf0c3f0bbf0c42996580a284f3d8ce564 (2026-10-12) | Namespaces and implementation/review requirements govern upstream inclusion; they do not certify behavior on a particular compositor | mined | 2026-10-20 | on-release | corpus/knowledge/wayland-protocol-boundaries-r13.md |
| S041 | Sanitized host registry capture — .ufo/waves/round-13/w1/globals.json | own-work | A | This client's time-bound Hyprland 0.56.2 interface/version advertisements | captured_utc 2026-10-20T04:10:03Z; probe rc 0; tool wayland-utils 1.3.0-1; compositor efb50993780079460b0cbed1363e2166a2de1d9f | Distinguishes advertised interface/version objects and multiplicity from behavioral feature validation without retaining device/output identity | mined | 2026-10-20 | on-session-change | corpus/knowledge/wayland-protocol-boundaries-r13.md, corpus/knowledge/output-colour-boundaries-r14.md |
| S042 | Wayland debugging extras — https://wayland.freedesktop.org/extras.html | docs | A | Documented compositor-global discovery, revision-anchored correction to S006 | §Compositor features; website source extras.html @ 8923a19916635c21a3577b616f650a7e45d70fa9 (2026-01-15) | supersedes S006 — anchors wayland-info's advertised-global discovery purpose to the page source revision; no behavioral result follows | mined | 2026-10-20 | 180d | corpus/knowledge/wayland-protocol-boundaries-r13.md |
| S043 | Wayland core registry specification — /usr/share/wayland/wayland.xml; https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_registry | spec | A | Core registry announcement, binding and removal are separate events | wayland 1.26.0-1 installed XML:117-177, wl_registry description and global/bind/global_remove | Registry events advertise name/interface/version; binding creates a client handle; neither an inventory nor its version implies tested feature behavior | mined | 2026-10-20 | on-release | corpus/knowledge/wayland-protocol-boundaries-r13.md |
| S044 | Gate maintenance rules — corpus/knowledge/gate-standing-use.md | own-work | A | Actual gate pin re-anchor and outside-marker regression requirements | §5 rules 2 and 4, :212-226; historical M10-2 note reopened 2026-10-20 | Gate pin movement requires re-verification and an appended erratum; edits outside excised blocks require a measured regression re-cut | mined | 2026-10-20 | on-gate-change | corpus/lessons/round-13.md |
| S045 | Window Rules duplicate-admission correction — https://wiki.hypr.land/Configuring/Basics/Window-Rules/ | docs | A | Duplicate current-wiki source admission, not a new window-rule fact | Latest git introductory Note and Syntax, page modified 2026-08-26; reopened 2026-10-20 | supersedes S030 — REJECTED: duplicate S017 for overlapping current-wiki syntax scope; flip: an independently justified distinct pinned scope after collision review | rejected | 2026-10-20 | 90d | — |
| S046 | wayland-info diagnostic implementation — https://gitlab.freedesktop.org/wayland/wayland-utils/-/raw/1.3.0/wayland-info/wayland-info.c | code | A | Upstream 1.3.0 observer bindings, output/colour detail queries and print filtering; not binary-source equivalence | tag 1.3.0 @ d01edd68961ca01779dcb96afe56c2d99ff79067; global_handler :3125-3163, detail calls :1775,:2031,:2626,:2744,:2750 | Diagnostic execution includes bindings and read-only detail queries even though S041 retains only registry headers; -i filters printed information, not binding | mined | 2026-10-20 | on-release | corpus/knowledge/wayland-protocol-boundaries-r13.md |
| S047 | wlr-output-management XML — https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/raw/a741f0ac5d655338a5100fc34bc8cec87d237346/unstable/wlr-output-management-unstable-v1.xml | spec | A | Documented output-configuration serial/test/apply/outcome boundary, not host behavior | a741f0ac5d655338a5100fc34bc8cec87d237346; manager/head descriptions and zwlr_output_configuration_v1 test/apply/succeeded/failed/cancelled; raw sha256 65b0f82a6cf129bf1a1c31a2428795abd33886c15ddd5f3ad97e5922d7bdc3a7 | Validation-only test does not guarantee apply success; successful apply may round state; stale serials cancel proposals | mined | 2026-10-20 | on-release | corpus/knowledge/output-colour-boundaries-r14.md |
| S048 | Colour-management XML — https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/staging/color-management/color-management-v1.xml | spec | A | Documented colour-manager support events and image descriptions, not measured HDR or physical colour accuracy | tag 1.49; wp_color_manager_v1 supported_* and done; output get_image_description; surface set_image_description; wp_image_description_info_v1 target_luminance; raw sha256 18a2678e3352c3be3fbeed20005d48852b7235d0d78f08b9c987a0b8e91449f9 | Separates manager capability events, output/surface image descriptions and theoretical luminance from actual light emitted by a display | mined | 2026-10-20 | on-release | corpus/knowledge/output-colour-boundaries-r14.md |
| S049 | Retained S041 data-scope correction — .ufo/waves/round-13/w1/globals.json | own-work | A | Correction of S046's unqualified retained-registry-only wording, not new diagnostic behavior | captured_utc 2026-10-20T04:10:03Z; globals records versus top-level probe/tool/compositor/session_binding; reopened 2026-10-20 | supersedes S046 — global records contain interface/version only; sanitized probe/session metadata is also retained; the diagnostic-binding evidence is unchanged | mined | 2026-10-20 | on-capture-change | corpus/knowledge/wayland-protocol-boundaries-r13.md, corpus/lessons/round-14.md |
| S050 | Tagged Hyprland output transaction safety — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/OutputManagement.cpp | code | A | Static tagged callback/stub facts that bar assuming output dry-run safety; not observed host behavior or binary-source equivalence | efb50993780079460b0cbed1363e2166a2de1d9f; COutputConfiguration constructor setDisableHead/setTest and applyTestConfiguration(bool test) | Test returns true through a stub; disable_head saves disabled state and schedules reload before a later test/apply; transaction-building is mutation-class | mined | 2026-10-20 | on-compositor-release | corpus/knowledge/output-colour-boundaries-r14.md |
| S051 | Tagged libinput helper documentation — https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/doc/user/tools.rst | docs | A | Documented helper context, defaults, kernel recording and virtual replay boundaries; not host input behavior | tag 1.32.0; libinput-list-devices Note, libinput-debug-events options, libinput-record; raw sha256 53264328664493c0fc7074722650ba42afcf8b30c94ce7cc94157544b654ff5f | supersedes S007 — list-devices reports built-in defaults, debug-events requires explicit options, record captures context-independent kernel events, replay creates a virtual device; these are different observation/action layers | mined | 2026-10-20 | on-release | corpus/knowledge/input-debugging-boundaries-r15.md |
| S052 | Tagged Wayland core input specification — https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml | spec | A | Core seat capability lifecycle and pointer/keyboard focus/event contract; distinct from S043 registry scope | tag 1.26.0; wl_seat :2004-2087, wl_pointer :2138-2265, wl_keyboard :2573-2699; raw sha256 cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07 equals installed wayland 1.26.0-1 XML | A seat capability is not client delivery; keyboard enter identifies a focused surface and key carries a platform-specific code, not guaranteed text; XML v11 is not host feature execution | mined | 2026-10-20 | on-release | corpus/knowledge/input-debugging-boundaries-r15.md |
| S053 | Tagged Waybar custom-module manual — https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/man/waybar-custom.5.scd | docs | A | Producer return-type, formatting and scheduling contract, not observed module text | tag 0.15.0; DESCRIPTION, CONFIGURATION exec/return-type/interval/signal, RETURN-TYPE, FORMAT REPLACEMENTS; raw sha256 efb6a63a3d7f125840d4c4a49956664070f36231724e7aa0fa281e6d2de30d82 | A custom producer supplies text and optional metadata; declared formatting and event commands do not establish rendered output or safe execution | mined | 2026-10-20 | on-release | corpus/knowledge/waybar-observation-boundaries-r16.md |
| S054 | Tagged Waybar custom-module implementation — https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/custom.cpp | code | A | Static producer-buffer-to-GTK-markup route and hide conditions, not installed-binary equivalence | tag 0.15.0; Custom::update, parseOutputJson, parseOutputRaw; raw sha256 2232f7f7141caa5958344e1e6a0ab8eec6321994da1fecd704345aeb513b291f | Parsing, formatting, visibility and GTK label update are distinct stages; producer success alone cannot establish user-visible pixels | mined | 2026-10-20 | on-release | corpus/knowledge/waybar-observation-boundaries-r16.md |
| S055 | Independent rejected-harmed safety closure — corpus/lessons/round-15-verifier-spotcheck.md | own-work | A | Established host partial-upgrade incident and routed process debt, not host remediation | R15-V1/V2 and Gate and correction evidence :161-162,254-277; file recorded in 32c4fda873c9cb47a84c549b24b80ead2bcaa1ea, which is this round's reading baseline | A green file-plane gate and hard-coded overlap fixture do not erase package harm or prove actual installation prevention | mined | 2026-10-20 | on-operator-recovery-decision | corpus/lessons/round-16.md |

## Paths

- **Window-rule effects (U1)** — S002 → S018 → S019 → S020 → S016 → S017: start from the gap the arc named, read the tagged 0.56.2 handler before any doc, then the host capture and the host rule files, and only then the current (Lua-era) wiki pages; this order keeps pinned-source truth ahead of current-docs prose.
- **Configuration-language era (U2)** — S021 → S023 → S022 → S024 → S025 → S026 → S027 → S028 → S029 → S030: the 0.53 rule-syntax break first, the archived v0.54 hyprlang pages as the host-era reference, then the Lua announcements and releases in date order, the current wiki last — release order prevents reading current syntax back onto 0.56.2.
- **Portal routing and ScreenCast (U3)** — S032 → S033 → S034 → S035 → S031 → S037: frontend/backend model, the routing config, the async request contract, the ScreenCast lifecycle, then the Hyprland backend's limits and its installed release; S036, S038, S039 are queued side reading.
- **Drift re-anchor (own method)** — S015 → S014 → S013: the lane's re-anchor protocol, then the gate erratum that applies it, then the operator installer that caused the drift.
- **Protocol and input debugging frontier (U4/U6, queued)** — S009 → S008 → S005 → S006 → S007, with S010 as a discovery index only: architecture before protocol phases, phases before the debugging tools that observe them.
- **How this lane judges its own claims** — S003 → S004 → S001: the fleet evidence/gate standard, the registry contract, then the lane's own method lessons.

- **U2 path correction (round 13)** — read S017 instead of the historical
  path's rejected S030; S045 records why the duplicate is not new evidence.
- **Protocol boundaries (U4, round 13)** — S005 → S040 → S043 → S042 → S041:
  phase and governance, wire-level registry contract, tool purpose, then the
  sanitized host sample. S006 remains queued historical metadata; S042
  supersedes its access-date-only anchor. U5–U7 remain frontier ground.
- **Output/colour boundaries (U5, round 14)** — S041 → S047 → S048 → S050:
  begin with the dated advertisement and its limits, then the owning
  output transaction and colour-description specifications. U5's
  documented route is now held; feature behavior and U6/U7 remain open.

- **Input layer boundaries (U6, round 15)** — S051 → S052:
  helper context/defaults/capture/replay first, client capability/focus/key
  contract second. S051 supersedes the queued historical S007 composite
  description; S052's input scope was reviewed as distinct from S043's
  registry scope. This documents a route, not host event delivery or IME.
  U7 and actual U6 behavior remain frontier.
- **Waybar module observation boundary (U7, round 16)** — S053 → S054:
  producer contract before parsing/formatting/hide/GTK update stages. This
  closes only the documentary route gap; rendered text remains unmeasured.
  S055 grounds the distinct static safety-plan capability and its limits.

## Search log

Round 12 (2026-10-19), one note per bounded search, by seat:

From the `local` seat:

- Rejection sweep — query `Hyprland window rules tutorial blog 2025` (web_search, 2026-10-19); identified 8, screened 8 by title/format, included 1 opened (filipmikina.com post, full read), rejected 1 for no version anchor; excluded 7 — 2 official wiki.hypr.land pages (docs, not a third-party restatement), 2 video/mirror results, 1 reddit thread, 2 short-form posts left unopened. Stop rationale: one opened unanchored restatement demonstrates the rejection bar; further opens would not change the registry (≥2 rejected rows already met).
- Frontier opens for later U4/U6 rounds — question: which upstream references anchor protocol phasing, debug tooling, input debugging and architecture? Where: canonical URLs named by the round dispatch plus mado-state §7 seeds, opened directly (no search engine). Identified 7 pages, opened 7 [OBS], included 6 queued rows (S005-S010), excluded 0 (the book's Introduction page was superseded by its high-level-design chapter). Stop rationale: every dispatch-named URL opened and content-verified; deeper mining waits for a round that targets U4/U6.
- Chapter location — query `site:wayland-book.com architecture` (web_search, 2026-10-19); identified 10, screened 10 by title, included 1 (introduction/high-level-design.html), excluded 9 (other chapters — left as leads). Stop rationale: the architecture-scoped chapter identified; the rest is a targeted-round job.
- MANIFEST re-measure — question: does the fleet-ledger's mado "improved" verdict set equal the lane's claimed axis moves? Where: jq over fleet-ledger MANIFEST.json plus a read of SCORECARD.md:11-26 (W). Counts: 10 mado round entries; 45 improved keys at jq; 28 manifest-only re-derived (2+3+1+3+5+3+3+3+3+2) against the SCORECARD axis rows; matched the dossier §2.2 totals exactly. Excluded 0. Stop rationale: unit-exact agreement — no further sweep.

From the `drift` seat:

- Question: Which opened sources anchor the operator-owned gkeep drift, gate-pin response and append-only re-anchor method? Searched local `~/Projects/gkeep/install.sh` at HEAD plus `tools/mado-verify.sh` and `omarchy-drift-watch.md`; accessed 2026-10-19; identified 3, screened 3, included 3, excluded 0 (all three directly support the scoped provenance/method claims); stopped because those are the direct code, gate and protocol sources. No external source search was needed.

From the `getprop` seat:

- Question: does pinned Hyprland 0.56.2 have a read-only per-window rule-effect query, and can it attribute a returned value to a rule? Search location: current official hyprctl and window-rules wiki pages, tagged v0.56.2 source, host `hyprctl` captures, and host rule files. Identified: 5 — `read` of S016–S020 source anchors, 2026-10-19; screened: 5 — same source review, 2026-10-19; included: 5 — same source review, 2026-10-19; excluded: 0 — same source review, 2026-10-19 (none excluded). Stop rationale: the primary tagged handler and repeatable host read establish available property output; current docs delimit current-era semantics; no matching-rule identity is exposed by the inspected handler path.

From the `config-era` seat:

- Question: when did Lua become the forward config surface; how is the default file selected; what 0.53–0.56 rule changes are documented? Official Hyprland news/releases and current plus v0.54 wiki pages were opened. 10 — `read()` listed URLs S021–S030 2026-10-19; 10 — screened against the U2 question via source review 2026-10-19; 10 — included in the entry source header 2026-10-19; 0 — excluded after source review 2026-10-19 (all opened sources were directly relevant). Stop: the requested migration and release boundaries are covered by primary announcements, tagged releases, current wiki, and versioned archive; release-summary silence is kept `[UNK]`, not treated as proof of no changes.

From the `portal` seat:

- Question: what maps the host’s declared portal interfaces to backend candidates, and what does each ScreenCast stage establish? Searched the assigned ART leads S008 and S024–S030 at their canonical URLs plus the installed XDPH v1.4.1 release tag, on 2026-10-19. Identified 9 — `printf '%s\n' S008 S024 S025 S026 S027 S028 S029 S030 XDPH-v1.4.1 | wc -l` 2026-10-19; screened 9 — `printf '%s\n' S008 S024 S025 S026 S027 S028 S029 S030 XDPH-v1.4.1 | wc -l` 2026-10-19; included 6 — `printf '%s\n' S008 S024 S025 S026 S027 XDPH-v1.4.1 | wc -l` 2026-10-19; excluded 0 — `printf '%s' '' | wc -l` 2026-10-19. S028–S030 were retained as queued adjacent release/API references, not rejected. Stop rationale: the requested routing/lifecycle claims are supported by the primary portal docs, local config and descriptors, and the matching installed XDPH release; no behavioral request was authorized.

Search-log errata (round 12, post-review, 2026-10-19):

- The `portal` seat's note above uses **ART dossier lead ids** (`kaika-w1/mado-art.md` S008, S024–S030), not registry ids. Mapping: ART S008 → S031, S024 → S032, S025 → S033, S026 → S034, S027 → S035, S028 → S036, S029 → S038, S030 → S039; the XDPH v1.4.1 tag → S037. Correct accounting for that search: 9 candidates screened; 6 selected for U3 (S031–S035, S037); 3 not selected for U3 but kept `queued` as adjacent API/release reading (S036, S038, S039); 0 excluded. Its "excluded 0" count came from `printf '%s' '' | wc -l`, an empty input, not a count — the real excluded set is empty because the three were kept, not dropped. Registry rows S028–S030 are a different set (config-era seat, U2) and were never part of the portal search.
- S030 duplicated S017's URL (`wiki.hypr.land/Configuring/Basics/Window-Rules/`) for an overlapping current-wiki syntax scope with no `supersedes` link. Orchestrator spot-check disagreed with its admission; status `mined` → `rejected` in place, its `used-by` moved to S017 (rule 2; old→new logged in `lessons/round-12.md`). S030's `teaches` cell cannot change in place, so its rejection reason lives here and in the lesson: duplicate of S017; flip: a distinct anchor at a pinned revision that S017 does not cover.
- Owed anchors (rule: anchor = section plus revision; `anchor` is not an in-place cell). Four queued rows carry a section but only an access date, not a page revision: S006 (`extras.html`), S008 (wayland-book high-level-design), S009 (`architecture.html`), S010 (wayland.app index). Owed: the round that mines any of them appends a superseding row (`teaches` opening `supersedes S0NN —`) with the source-repository commit of that page; until then they stay `queued` and are not citable as sole support. Not done now because a superseding row on the same URL and scope reads as a duplicate to the fleet census (E04/W04) until the supersedes link is recognised.

Round 13 bounded search (2026-10-20): question — how do protocol phase,
advertised globals and unexercised behavior differ, and what prevents the
S030 merge mistake? Directly reopened official wayland-protocols README
and GOVERNANCE, official Wayland extras and installed core XML, the
sanitized host capture, gate-maintenance note and current Window Rules
page. Row-action candidates: S005, S017, S040–S045 (eight candidates,
seven distinct source surfaces). Identified/screened 8, included 7 row
actions (five new mined rows, S005 mined, S017 citation update), rejected
1 duplicate-admission correction (S045); 0 candidates left unexamined.
Counting command: `python3 -c 'a=["S005","S017"]+[f"S{i:03}" for i in range(40,46)]; print(len(a),len(a)-1,1)'`
→ `8 7 1`; source opens/located quotes in `lessons/round-13.md` § Gate.
Stop: each U4 facet has primary authority and a host advertisement sample;
U5–U7 and a complete extension XML crosswalk are not admitted here.

Correction to the round-12 owed-anchor rationale above: the maintained
census already recognizes a `supersedes S###` marker for the same-URL
error; different-scope repetitions can remain non-failing W04 warnings.
That was not a blocker to supplying the S006 revision. S042 now supplies
it without editing S006's immutable anchor. Historical rejected S030
still produces a known warning; S045 supplies the explicit rejection
reason/flip without rewriting its old teaches cell. URL collisions are a
merge-review trigger, not a source-volume or rejection-quota signal.

Adversarial follow-through: AttackCoverage A1 required one additional
primary code open, S046 (`wayland-utils` 1.3.0's `wayland-info.c`), to
distinguish the observer's bindings/detail queries from retained headers.
Identified/screened/included this follow-through: 1/1/1; rejected 0.
Combined candidate ids are S005, S017, S040–S046. The revision-bound
`measure.py` output `source_registry.round13_candidates` counts the
actual present/mined/rejected candidate sets (final 9/8/1), rather than
inferring knowledge growth from these row counts. Stop: the diagnostic
implementation boundary is now code-grounded; no new feature test follows.

Round 14 (2026-10-20), bounded U5 source selection: question — what do
output-configuration replies and colour descriptions actually establish?
Opened directly the canonical wlroots XML at a741f0ac and
wayland-protocols colour XML tag 1.49; identified/screened/included
2/2/2 sources, excluded 0 — the exact two new ids S047/S048 in this
round's revision-bound `measure.py` registry delta. Reopened S041 for
the historical advertisement join; its used-by change is logged in the
lesson. Stop: both owning XMLs directly answer the bounded questions.
Advisory alternate revisions and community discovery pages were not
admitted as additional sources; no complete protocol or host-behavior
inventory is implied. The raw tag-1.49 colour XML matches the installed
1.49-1 file; older README/governance revisions are not substituted for it.

Round-14 correction search, R13-V1: reopened the single own-work S041
capture and compared global-record keys with enclosing metadata; one
candidate screened and included as S049, zero excluded — the S049 row in
the revision-bound registry delta is the counting unit. This correction
supersedes S046's unqualified retention phrase; it is not a third external
protocol source, a new capture or additional U-item expansion.

Round-14 adversarial follow-through: SourceSafety identified a possible
specification/implementation safety mismatch. Parent opened the exact
tagged OutputManagement.cpp callbacks once; one candidate screened and
included as S050, zero excluded — source id S050 in the revision-bound
registry delta. Stop: the opened test stub and pre-test disable callback
are sufficient to reject assuming dry-run safety; no feature execution,
binary/source equivalence or additional host-behavior claim is admitted.

Round 15 (2026-10-20), bounded U6 question: which layer does an input
diagnostic describe, and when is it not a safe read? Opened existing
S007's latest tools page (title 1.32.0), then exact tagged tools.rst and
Wayland core XML. Identified/screened 3/3 opened candidates, included 2
stronger new rows S051/S052, excluded 1 as the final anchor (S007's
mutable/composite description). The candidate-count unit is these three
source locations, not the number of seats reading them. S051 explicitly
supersedes S007; S007 remains queued historical metadata, unchanged.
S052 uses the same core XML as S043 but a disjoint input-contract scope;
this is reviewed source reuse, not new registry-advertisement knowledge.
The apparently versioned libinput HTML path returned 404 and is not a row.
Stop: primary helper and core focus contracts settle the bounded route.
Toolkit/IME internals, client delivery, kernel diagnosis and event collection
are not admitted. No existing status/recheck/used-by field was changed.

Round 16 (2026-10-20): which evidence reaches producer data, GTK label
updates, or rendered module text, and what did outside closure require?
Opened the two assigned tagged Waybar files and the independent closure.
Identified/screened/included 3/3/3 locations, excluded 0; this count is the
three S053–S055 additions (revision counter's registry delta), not seat
reads. Tagged manual and implementation are complementary scoped primary
sources, not duplicates of the older general Waybar inventory. No existing
row's status/recheck/used-by changes. Stop: the exact producer/renderer
boundary and outside safety debt are settled without executing a producer,
capturing UI or touching packages/services. Actual rendering and host
recovery remain outside this admission.

## Leads (unopened)

A lead is not evidence and never a row.

From the `local` seat:

- wayland-protocols GOVERNANCE.md §2.1-2.3 and MEMBERS.md (named by the README's phase requirements; unopened).
- The Wayland Book's remaining chapters (surfaces, libwayland internals, xdg-shell) — 9 search results screened by title only.
- libinput 1.32.0 "Reporting bugs" page and the evemu recording route (referenced by tools.html; unopened).
- wiki.hypr.land Window-Rules page — upstream doc; deliberately left to the round's rule-effects seat, not opened here.
- The Linux Cast post (screened by title only in the rejection sweep; unopened).

From the `drift` seat:

- None.

From the `getprop` seat:

- None retained. The task's named sources were opened; no additional source is needed to establish the bounded claim.

From the `config-era` seat:

- No unopened lead was retained; the bounded source sweep is the ten listed URLs S021–S030, all opened 2026-10-19.

From the `portal` seat:

- None retained: S008, S024–S030, and the installed XDPH v1.4.1 release were opened in this round.

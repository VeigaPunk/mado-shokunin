# ScoutHeldOverlap — held coverage overlapping the planned focus-grab entry (round 41, w1)

Method: `grep -rnEi` over `corpus/knowledge/*.md`, `corpus/SOURCES.md`, `corpus/lessons/`, `SKILL.md`, `PROVINCE.md`,
`plans/`, `README.md`, `corpus/README.md` for the 14 requested terms; every cited file was then re-read at the cited line.
Text grep is the right tool here (a prose corpus, no code symbols); it is not semantic proof of absence in code. Also read:
`.ufo/waves/round-13/w1/globals.json` (S041), `fetch/xdph-journal.txt`, `fetch/focus-grab-v1.xml`, `fetch/Hyprland-FocusGrab.cpp`,
`fetch/xdph-PortalManager.cpp`. One extra fetch (read-only, scratch, deleted): `Hyprland @ efb5099 src/desktop/state/FocusState.cpp`
(sha256 `9b971362bba97f200f0ef786237deed6b7b863066590d243cac11787e2a56ebd`), because the grab source calls into it.
Labels: OBS = observed by me this seat; INF = my inference; UNK = not established.

## 0. Headline

1. The lane holds **no prose** about focus-grab (OBS: `grep -rniE 'focus.?grab' corpus SKILL.md PROVINCE.md plans README.md` → no
   hit in any held entry). BUT it holds the **datum**: S041 (`.ufo/waves/round-13/w1/globals.json`, SOURCES.md:53) records
   `hyprland_focus_grab_manager_v1` version 1 advertised to a `wayland-info` client on 2026-10-20T04:10:03Z (OBS: python parse of the
   JSON; 72 records / 71 unique; `hyprland_focus_grab_manager_v1: 1`). The registration's "the lane holds none of it" is true of
   prose and of `corpus|PROVINCE|SKILL|tools`, false of `.ufo/waves/round-13/`. The entry must cite S041 as a held, earlier,
   second-client advertisement and must not present the xdph journal census as the first sight of the global.
2. No held statement **contradicts** the compositor-side source (§4). Two held statements are *near* it (a rule-effect
   classification, an UNK that held data already answers); both need care, §4.A and §4.B.

## 1. Held rows/entries by term (file:line, what it says)

### xdg-desktop-portal-hyprland / xdph
- `corpus/SOURCES.md:49` S037 xdph v1.4.1 release (tag commit cc8e5ef, 2026-07-29; "Installed XDPH upstream release identity");
  used by `xdg-portal-routing-r12.md`. The entry's "installed xdph v1.4.1" is this row; cite S037, do not re-open as new.
- `SOURCES.md:43` S031 Hyprland wiki xdph page (role, file chooser limitation, GTK fallback, debugging route).
- `corpus/knowledge/xdg-portal-routing-r12.md:20` pacman -Q `xdg-desktop-portal-hyprland 1.4.1-2` (2026-10-19); `:23` unit active;
  `:47-61` routing table per implementation-interface (descriptor-level, `[INF]`, "no request was issued"); `:51` `InputCapture`
  → XDPH first candidate; `:64`, `:107`, `:114` XDPH does not implement FileChooser (rejected M03); `:89` v1.4.1 = screencopy
  `cursor_mode` option + loop-hangup fix.
- `hyprland-config-plane.md:165-167` `xdph.conf` 4 lines (`screencopy { allow_token_by_default = true; …`), xdph PID 1920 at MADO-1 §8;
  `config-health-report-r3.md:179` PID 1920; `remaining-planes-census.md:233` package versions; `SKILL.md:85,95,117` xdph = separate
  consumer outside the include graph, "xdph portal running (PID epoch-varying)".
- **Not held:** the xdph *runtime log* (`journalctl --user -u xdg-desktop-portal-hyprland`): nothing in the lane reads the unit's
  journal; held evidence is pacman/unit-state/descriptor/D-Bus-property reads only (`xdg-portal-routing-r12.md:20-26`).
  `plans/round-6-record-draft.md:187`, `plans/round-6.plan.md:44` mention the pid only.
- PID drift (OBS): held PIDs 1920 / 1203662 vs journal sessions pid 1918 (until 2026-10-25T13:35:28-03:00 "Stopped") and 1952
  (from 13:36:24). These are different sessions; no conflict, just never cite a PID as stable (SKILL.md:117 already says so).

### "Got interface"
- Zero hits in the lane (OBS). New ground. Source semantics (OBS, `fetch/xdph-PortalManager.cpp:85-88`): `CPortalManager::onGlobal`
  logs ` | Got interface: {} (ver {})` at the top of the registry-global handler, **before** the `if (INTERFACE == …)` bind
  branches. So a "Got interface" line = a `wl_registry.global` event reaching xdph (advertisement), not a bind and not a use.
  This is exactly the r13 distinction (`wayland-protocol-boundaries-r13.md:37-41`, advertisement ≠ binding ≠ behavior) and the entry
  must keep it: "advertised to xdph", never "xdph uses focus-grab".

### layer-shell
- `theme-route-r18.md:72` swaybg needs wlr-layer-shell + `wl_output` v4 (docs, `[SR]`); `SOURCES.md:104` S092. Layer rules:
  `keybind-rule-semantics.md` (`match:namespace`, `hyprshot.conf:2`, `walker.conf:2`, layer `no_anim`), S163 (`SOURCES.md:175`,
  `LayerRuleApplicator.cpp`). S041 holds `zwlr_layer_shell_v1` v5; journal 1952 holds `zwlr_layer_shell_v1 (ver 5)` (line 119).
  Nothing says layer surfaces interact with focus; the entry's layer-shell remarks are new ground, but the exclusive-keyboard fact
  (`m_exclusiveLSes`, FocusState.cpp:109) would be a *new* statement, source-only.

### input-capture
- `xdg-portal-routing-r12.md:51` and `:114` only: the **portal** `InputCapture` is in the XDPH descriptor (descriptor-level).
  `bind-table-r25.md:36` is unrelated (bind-flag `x` = allow input, `ConfigManager.cpp:1538-1540`, S162).
- Not held: the **Wayland global** `hyprland_input_capture_manager_v1` (prose). Datum held in S041 (v1). New journal data:
  `[input-capture] initializing input capture portal` / `init successful` at 13:36:24 pid 1952 (`xdph-journal.txt:134-135`).
  The registry/descriptor claim and the runtime-init claim are different evidence classes; keep `[INF]` (descriptor) vs `[OBS]` (log).

### xdg_activation
- Zero held statements on the protocol. Adjacent held rule/option: `misc:focus_on_activate` = 1 (`hyprctl-verification-layer.md:107`,
  `config-health-report-r3.md:526`, option read, `agreement`), and the rule `focus_on_activate off` at `telegram.conf:2`
  (`keybind-rule-semantics.md:231`, listed among "Dynamic effects declared"). S041 holds `xdg_activation_v1` v1; journal line 108.
  The link "xdg_activation → focus_on_activate" is NOT stated anywhere in the lane; if the entry states it, it is new and needs
  its own source row (not in the fetch dir list).

### no_focus, no_initial_focus, follow_mouse
- `no_focus on`: `keybind-rule-semantics.md:189` (`windows.conf:9`, 6 props: empty class/title + xwayland/float/fullscreen/pin),
  `:210` and `:229` (listed as a **Dynamic** effect, "re-evaluated on property change"; `[INF-docs]`), the lane's only statement.
- `no_initial_focus`: `:225` `webcam-overlay.conf:4`, listed under **Static** effects.
- `no_follow_mouse` (`:232`, `jetbrains.conf`); `stay_focused` (`:232`, davinci orphan only, not sourced); `focus_on_activate off`
  (`:231`).
- `input:follow_mouse` = 1: `hyprctl-verification-layer.md:125`, `config-health-report-r3.md:539,822`, `keybind-rule-semantics.md:283`
  (option read, `int: 1`, `set: true`).
- None of these states what any of these do in a *protocol* sense; no held statement mentions them together with a grab.
  FocusState.cpp (OBS, pinned): `input:follow_mouse` is read in `rawWindowFocus` (`:97`, used `if (*PFOLLOWMOUSE == 0)` near the end),
  `noFocus()` at `:150`. So the entry's rule-level counterpart can cite held rows for the *declared* values and add the source
  semantics as new.

### silent
- `movetoworkspacesilent` (`keybind-rule-semantics.md:145`, 11 uses; "like movetoworkspace but does not follow"),
  `workspace special silent` rule (`:224`, `browser.conf:19`), `config-health-report-r3.md:131,745`. The word is otherwise about
  "never a silent pass" (lane method). Nothing focus-grab-related; the only focus link is that `silent` = "does not follow" focus,
  already held at `:145`.

### foreign-toplevel
- Zero held statements (prose). Data: S041 `ext_foreign_toplevel_list_v1` v1, `zwlr_foreign_toplevel_manager_v1` v3,
  `ext_foreign_toplevel_image_capture_source_manager_v1` v1; journal 1952 lines 99,101 (and `[toplevel] (activate) locks: 1` line
  102). New ground for prose. (INF only: xdph binds the toplevel managers for ScreenCast window sources — not claimed by the lane;
  `xdg-portal-routing-r12.md:26` states `AvailableSourceTypes u 7` = MONITOR|WINDOW|VIRTUAL, descriptor/property level.)

### wayland protocol boundaries
- `wayland-protocol-boundaries-r13.md` (admitted r13, covers U4; S005, S040–S043, S046; sources at `:1`):
  - `:6-16` three-question split: phase (owning-repo XML) / advertisement (registry) / feature works (`[UNK]` until separately observed).
  - `:14,:29,:33,:100` an interface name/version does not encode a phase; compositor/vendor-specific protocols (Hyprland's own) need
    **their own owning-repository authority**; "Do not infer Hyprland runtime support from a project's governance membership."
  - `:31` protocol major vs interface version vs package release kept separate; `:37-41` advertise ≠ bind ≠ behavior; `:43` the
    diagnostic client binds advertised globals (so a `wayland-info` capture is **not** an advertisement-only observation).
  - `:45-58` host point sample: Hyprland 0.56.2 / `efb50993…`, wayland-info capture 2026-10-20T04:10:03Z, global multiplicity
    (`wp_drm_lease_device_v1` duplicated) retained; "do not replace the object list with a deduplicated set when counting objects."
  - `:60-85` safe recheck: allowlist-projected `wayland-info`; `:65` probe failure → advertisement `[UNK]`, not "no protocols".
  - `:104` limit: "No source XML inventory of every advertised extension was performed" — so r13 never classified
    `hyprland_focus_grab_manager_v1`. The entry fills exactly that gap for one global.
  - `:106-124` erratum r14 (S049).
- `SKILL.md:419-425` "Current diagnostic boundaries (round 13)", `:470-475` registry advertisement is not capability; "XML v11 does
  not establish host support above the historical advertised v9" (that is `wl_seat`).
- `output-colour-boundaries-r14.md:85-87` S041 reuse; `input-debugging-boundaries-r15.md:34-35,60` seat capability / focus event
  contract (S052; `wl_keyboard.enter` sets the active surface; focus is not text). `SOURCES.md:244` (U4 chain S005→S040→S043→S042→S041).
- Implication for the new entry: the focus-grab XML's `wl_keyboard::enter` text (focus-grab-v1.xml) refers to the same event
  S052 already pins at core level; cite S052 for the core event, the hyprland-protocols XML for the grab semantics, do not
  re-derive. And the entry's host section is a **second client's** advertisement (xdph, log-derived) beside S041 (wayland-info);
  the two are not the same population (§3).

### security_context
- Zero held statements (prose). Data only: S041 `wp_security_context_manager_v1` v1; journal 1952 line 131 (ver 1). New ground.
  Note the C1 class table's `sandbox` class presumably maps this; the entry should not claim anything about sandbox filtering of
  focus-grab (UNK, no source read).

### Other overlaps found
- `idle-lock-route-r17.md:130` `[UNK] Whether the compositor exposes hyprland-lock-notify-v1 on this host.` — **S041 (r13, 2026-10-20)
  already holds `hyprland_lock_notifier_v1` v1 (SOURCES.md:53; globals.json), and the journal holds it too (1952, `xdph-journal.txt`
  `hyprland_lock_notifier_v1 (ver 1)`).** The UNK predates a held datum: an internal staleness that the journal census can
  *answer* (advertisement only; "the mode-3 sleep-inhibit behaviour" stays UNK). The C2 entry or the lesson can close it via an
  append-only erratum/pointer (not in the focus topic; flagged for the L1).
- `corpus/lessons/round-35.md:138-139` the staged package's ids S309–S334 collide with Quickshell, `hyprland-protocols` and a Japanese
  Wayland article rows (id remap erratum, M35-1). Confirms the staged entries cite those sources under ids that are NOT this lane's
  ids; the entry must not reuse `S3xx` ids from the package (also see the id-collision guard, `round-35.md:141-150`).
- `PROVINCE.md:68-80` (r36 refinement) channel rule: localized (Chinese/Japanese) documentation channel is out of province.

## 2. Held rows the entry should CITE (not re-open as new)

| Held id | What it is | File:line | Use in the entry |
|---|---|---|---|
| S041 | wayland-info registry capture 2026-10-20T04:10:03Z, `hyprland_focus_grab_manager_v1` v1, Hyprland `efb50993…` | SOURCES.md:53; globals.json | prior advertisement datum; second client |
| S043 | `wl_registry.global`/`bind` core semantics | SOURCES.md:55; wayland-protocol-boundaries-r13.md:37-41 | "advertise ≠ bind" |
| S052 | `wl_keyboard.enter/leave`, `wl_pointer.*` core | SOURCES.md:64; input-debugging-boundaries-r15.md:34-35 | the event the grab's "compositor-picked surface … wl_keyboard::enter" refers to |
| S037 | xdph v1.4.1 release | SOURCES.md:49 | installed xdph pin |
| S031 | Hyprland wiki xdph | SOURCES.md:43 | XDPH role (optional) |
| S162 | Hyprland ConfigManager.cpp @ `efb50993…` | SOURCES.md:174 | same compositor commit already pinned for rule semantics (cite for pin continuity) |
| S163 | LayerRuleApplicator.cpp @ `efb50993…` | SOURCES.md:175 | layer-rule counterpart if the entry mentions layers |
| — | no_focus / no_initial_focus / follow_mouse rows | keybind-rule-semantics.md:189,210,225,229-232 | rule-level counterpart, declared values |
| — | option reads | hyprctl-verification-layer.md:107,125 | `focus_on_activate`/`follow_mouse` live values |

## 3. Population caveat for the host census (OBS, parse of the two data sets)

- S041 (wayland-info, 2026-10-20): 72 records / 71 unique. Journal session pid 1952 (2026-10-25T13:36:24-03:00): 63 adverts, 63
  distinct, all `Got interface:` lines. Session pid 1918: 15 adverts / 8 distinct (the `wl_output` repeated; shows hotplug-style
  repeats).
- Every interface in journal-1952 is also in S041 with the **same version** (set difference 1952∖S041 = ∅; version diffs = ∅).
- S041 has 8 interfaces **absent from journal-1952**: `ext_foreign_toplevel_image_capture_source_manager_v1`,
  `ext_image_copy_capture_manager_v1`, `wl_drm`, `wl_output`, `wp_color_manager_v1`, `wp_drm_lease_device_v1`,
  `wp_linux_drm_syncobj_manager_v1`, `zwp_linux_dmabuf_v1`. Those eight appear in the **old** session 1918 (journal lines 1-9). So the
  journal's "63 distinct in the latest session" is not "the compositor's global set": the latest session's journal omits eight
  that both S041 and the old session list. Cause UNK (candidates: journal truncation, ordering, per-boot differences; none read).
  The entry must say "63 advertised to xdph in this log session" and not equate it with S041's 71, nor claim the eight vanished.
- `hyprland_focus_grab_manager_v1` v1 sits in both populations (S041; journal line 117); in session 1918 it is absent (that
  session's journal holds only 8 distinct names). So "one advert at 13:36:24 pid 1952" is correct for the journal and does not
  say it was absent earlier.

## 4. Contradiction check against `fetch/Hyprland-FocusGrab.cpp` (+ `.hpp`, XML)

Held statements that touch the planned entry's topics: only those in §1. Result: **no held statement is contradicted** by the
compositor-side source. Boundary cases:

**4.A `no_focus` (held, keybind-rule-semantics.md:189,210,229).** Held: `no_focus` is a window-rule *dynamic* effect (docs-derived).
Source (OBS, pinned FocusState.cpp @ efb5099): `rawWindowFocus` refuses (`:150`) when `pWindow->m_ruleApplicator->noFocus()`;
`rawSurfaceFocus(pSurface, pWindowOwner)` (`:223-`) has **no** `noFocus` test — only (a) already-focused early-return, (b) session-lock
(`:227`), (c) `m_seatGrab->accepts(pSurface)` (`:230`). The grab's `refocusKeyboard` (Hyprland-FocusGrab.cpp:108) calls
`rawSurfaceFocus(surface)` with no window owner. Consequence (INF, not exercised): the `no_focus` rule is a *window-focus* gate that
a grab's keyboard re-focus path does not pass through. The lane does not claim `no_focus` blocks all keyboard focus, so no
contradiction; but the entry must NOT write "no_focus makes a window unfocusable" without scoping it to `rawWindowFocus`. If the
entry wants the rule-level counterpart, this is the strongest new statement and needs the FocusState.cpp row (new SOURCES row).

**4.B `hyprland-lock-notify-v1` UNK (held, idle-lock-route-r17.md:130)** vs S041/journal advertising `hyprland_lock_notifier_v1` v1:
not a source contradiction; a held UNK that held data already resolves at the advertisement level (§1 "Other overlaps").

**4.C Statements the entry will make that the lane has NOT made (new ground, no held statement to contradict):**
- Semantics in source (OBS, Hyprland-FocusGrab.cpp): constructor makes a `CSeatGrab` with `m_keyboard = true; m_pointer = true` and a
  callback `finish(true)` (`:15-22`; keyboard `:20`, callback `:22`); `commit()` moves PendingAddition→Committed and PendingRemoval→erased,
  then `start()` if any committed else `finish(true)` (`:113-147`); `start()` = `setGrab`, `simulateMouseMovement()` (`:54`),
  `refocusKeyboard()` (`:47-56`); `finish(sendCleared)` clears grab and surfaces and sends `cleared` only when `sendCleared` (`:58-71`);
  destructor calls `finish(false)` (`:31`), reached from the grab's `destroy`/on-destroy handlers via `destroyGrab` (`:24-25`, `:161`) —
  so an explicit `destroy` / client death sends no `cleared` (INF from the code path; XML `cleared` text: "Sent when an active grab
  is cancelled by the compositor, regardless of cause", i.e. compositor-side cancel); `addSurface` ignores duplicates (`:73-77`),
  `removeSurface` erases a PendingAddition but marks others PendingRemoval (`:79-87`); surface-destroy listener → `eraseSurface` →
  `removeSurface` + `commit(true)` (removal only, `:89-92`); `refocusKeyboard` (`:94-111`) early-returns if the keyboard-focused surface
  is already a committed member, calls `rawSurfaceFocus(surface)` (`:108`), and with no committed surface logs an error ("This should
  never happen.", `:110`); `bindManager` (`:149`) / `onCreateGrab` (`:165-172`): a grab whose resource is bad → `noMemory()` (`:170`).
- XML (OBS, focus-grab-v1.xml): grab "restricts input focus to a specified whitelist" while the object exists with ≥1 committed
  surface; outside mouse/touch input clears the grab (`cleared`); "The same will happen if another focus grab or similar action is
  started at the compositor's discretion." Check this against source: `CFocusGrab::start()` calls `g_pSeatManager->setGrab(m_grab)`;
  whether the previous seat-grab is cleared via its callback is **not in the fetched file** (SeatManager not fetched). The entry
  must not claim how a second grab displaces the first from this file alone (UNK from the fetched bytes).
- Multiple `CFocusGrab`s may exist per `CFocusGrabProtocol` (`m_grabs` vector, `onCreateGrab`): per-client multiplicity is in
  source; which wins is `setGrab` behavior (not fetched).

## 5. Statements the lane already makes on the entry's topics (complete list)

1. Advertisement of a Hyprland global is not feature behavior (`wayland-protocol-boundaries-r13.md:6-16,35-43,99`; `SKILL.md:419-436,472-475`).
2. Hyprland-specific protocols need their own owning-repository authority (`:14,:29,:33`).
3. `hyprland_focus_grab_manager_v1` v1 present in S041 (data only; no prose).
4. XDPH routing: InputCapture/GlobalShortcuts/Screenshot/ScreenCast → XDPH first; descriptor-level `[INF]`; no request issued
   (`xdg-portal-routing-r12.md:47-61,64,107`).
5. xdph is a separate consumer; running; PID epoch-varying (`SKILL.md:117`); installed 1.4.1 (S037).
6. Window rules: `no_focus on` (windows.conf:9, empty class/title + xwayland/float/fullscreen/pin) is dynamic; `no_initial_focus`
   (webcam-overlay.conf:4) static; `focus_on_activate off` (telegram.conf:2), `no_follow_mouse` (jetbrains.conf), `stay_focused`
   (davinci orphan, unsourced) (`keybind-rule-semantics.md:189,210,225,229-232`).
7. Option values: `input:follow_mouse` 1, `misc:focus_on_activate` 1 (`hyprctl-verification-layer.md:107,125`).
8. `wl_keyboard.enter` defines the focused surface; focus is not text (`input-debugging-boundaries-r15.md:34-35,60`).
9. `[UNK]` `hyprland-lock-notify-v1` exposure (`idle-lock-route-r17.md:130`) — stale vs S041.
10. Locale rule: localized documentation out of province (`PROVINCE.md:68-80`).
11. `movetoworkspacesilent` "does not follow" (`keybind-rule-semantics.md:145`).

## 6. Recommendations for the entry (additive, from this scout)

- Cite S041 (+ S043, S052, S037, S162) in the entry and a "held prior" sentence; new SOURCES rows only for: hyprland-protocols
  focus-grab XML, Hyprland FocusGrab.cpp/.hpp, FocusState.cpp (if 4.A is stated), xdph PortalManager.cpp, quickshell grab.cpp,
  issue #565, the saved journal (own-work). Check each against the counter's clauses; this scout did not read the counter.
- Scope every "advertised" statement to a client + time (S041: wayland-info 2026-10-20; journal: xdph pid 1952 2026-10-25T13:36:24-03:00).
- Keep "Got interface = registry global event received by xdph (before any bind)" and cite `xdph-PortalManager.cpp:85-88`.
- Do not write: "no_focus prevents focus" (unscoped); "xdph uses focus-grab"; "the compositor advertises 63 globals";
  "second grab displaces first via X" (not in fetched bytes); "client death sends cleared" (source path says no).
- Optional hygiene (L1): an append-only pointer/erratum on `idle-lock-route-r17.md:130` UNK, since S041 already holds the global.

Evidence commands, all read-only: the greps in §1 (outputs summarised above), a python parse of
`.ufo/waves/round-13/w1/globals.json` and `fetch/xdph-journal.txt`, `curl -sL` of one raw GitHub file into `/tmp` (deleted).
No lane file other than this seat's two report files was written; no counter was run.

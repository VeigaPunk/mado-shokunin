# ExecEntryClaims — attack report on the landed entry (round 41 w2)

Attacked object: `corpus/knowledge/hyprland-focus-grab-r41.md` at DATA commit
`07f2641696b5ac73de1404ea737a9f27e9819aa1` (read via `git show`, frozen).
Receipts: `.ufo/waves/round-41/fetch/` (all 10 files). Host checks: `hyprctl version`,
`/var/lib/pacman/local/xdg-desktop-portal-hyprland-1.4.1-2/desc`.
Date: 2026-10-25. Seat: ExecEntryClaims (leaf; no subagents, no edits to the entry).

## 0. Method

- Every OBS/INF line of the entry was checked against the receipt it cites; quotes were
  re-located in the receipts (file:line below), and every count was recomputed by script.
- The four pinned receipts (S283 xml, S284 cpp+hpp, S285 grab.cpp, S286 PortalManager.cpp)
  were additionally re-verified **byte-identical against upstream git objects** at the exact
  pins the entry declares (git fetch at SHA/tag + `git show` + sha256, see §5). All match.
- Host facts: `hyprctl version` run (allowed), package `desc` read (read-only).
- Lane INF (§5): re-run at the stated base commit `ab2bfaab661c846d1de9d58c01651cd156a13949`
  via `git grep` (read-only).
- No tool was installed this round (used existing git, python3, sha256sum, grep).

## 1. Check table (entry line → claim → check → result)

| line | claim | check | result |
|---|---|---|---|
| 3 | S283 pin cd1aba6bd78775825eb230b3a4274c48b6705eb7, "both interfaces, every request, the cleared event" | `git fetch --depth 1 origin cd1aba6…` + `git show FETCH_HEAD:protocols/hyprland-focus-grab-v1.xml` sha256 = `0bc60c14…` = receipt | ok |
| 4 | S284 pin efb50993780079460b0cbed1363e2166a2de1d9f (same commit as host hyprctl version) | upstream `src/protocols/FocusGrab.cpp` sha256 `53b762f7…` / `.hpp` `dce47251…` = receipts | ok |
| 5 | S285 pin 9b0f339b19057f4731bf3b48293307d7ef241671 | upstream `src/wayland/hyprland/focus_grab/grab.cpp` sha256 `6f7cecf1…` = receipt | ok |
| 6 | S286 pin v1.4.1 | upstream `src/core/PortalManager.cpp` @ tag v1.4.1 sha256 `15c3e39c…` = receipt | ok |
| 7 | S287 issue 565, closed 2022 | receipt `issue-565.html`: `"state":"CLOSED"`, createdAt `2022-08-23T14:03:55Z`, maintainer replies 2022-08-25/26 | ok |
| 8 | S288 pin cd1aba6… | upstream README.md @ cd1aba6… sha256 `3c700763…` = receipt | ok |
| 9 | S289 sha256 bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7 | sha256sum of fetch/xdph-journal.txt = `bf8fa91a…` | ok |
| 10 | S037 installed 1.4.1-2 | host `/var/lib/pacman/local/…-1.4.1-2/desc` exists, sha256 `7bf2f8be…` (= receipt), `%NAME% xdg-desktop-portal-hyprland`, `%VERSION% 1.4.1-2` | ok |
| 19 | "This interface restricts input focus to a specified whitelist of surfaces" / "This protocol allows clients to limit input focus to a specific set of surfaces" | focus-grab-v1.xml:62-63 / :34-35 verbatim | ok |
| 21 | manager has exactly two requests, create_grab(new_id), destructor destroy "doesn't destroy existing focus grab objects"; grab has add_surface/remove_surface(wl_surface), commit, destructor, one event cleared | focus-grab-v1.xml:44-57 (requests), :79-126 (grab), :121-126 (cleared) | ok |
| 25 | create_grab arg `new_id hyprland_focus_grab_v1` | xml:49 | ok |
| 26 | destroy = destructor, manager only, grabs survive | xml:52-56 | ok |
| 27 | add_surface whitelists; duplicate additions ignored; effect on commit | xml:79-86 ("duplicate additions are ignored" :82-83; "Does not take effect until commit is called" :85) | ok |
| 28 | remove_surface un-whitelists; destroyed surface treated as this call; effect on commit | xml:91-100 | ok |
| 29 | commit: empty→non-empty starts, non-empty→empty inert | xml:109-111 verbatim | ok |
| 30 | destroy destructor "Destroys the grab object and remove the grab if active" | xml:115-119 | ok |
| 31 | cleared event — compositor cancelled active grab | xml:121-126 ("cancelled by the compositor, regardless of cause") | ok |
| 33 | commit quote "If the list previously had no entries and now has at least one, the grab will start." | xml:109-110 verbatim | ok |
| 35 | keyboard → compositor-picked whitelisted surface ("wl_keyboard::enter"); pointer/touch inside pass; "Upon meeting implementation-defined criteria usually meaning a mouse or touch input outside of any whitelisted surfaces"; "The same will happen if another focus grab or similar action is started at the compositor's discretion" | xml:66-76 verbatim | ok |
| 37 | INF: protocol cannot move focus outside the set; client controls only membership | basis = xml interface description + commit text; supported | ok |
| 43 | ctor: `m_grab->m_keyboard = true;` + pointer true + `setCallback([this]() { finish(true); })` | FocusGrab.cpp:20-22 verbatim | ok |
| 45 | start: `m_grabActive = true; g_pSeatManager->setGrab(m_grab);` then simulateMouseMovement()+refocusKeyboard() | FocusGrab.cpp:49-50, :54-55 | ok |
| 47 | finish: `if (sendCleared) m_resource->sendCleared();`; destructor calls finish(false) (:32); unseat only if still current grab (:62-63) | FocusGrab.cpp:58-70 | ok |
| 49 | commit: `if (anyCommitted) start(); else finish(true);`; three-valued state PendingAddition/PendingRemoval/Committed; only set-change triggers start/finish; destroy signal → eraseSurface → commit(removeOnly=true), never re-adds | FocusGrab.cpp:113-143; enum hpp:20-24; eraseSurface :89-92; addSurface :73-77 | ok |
| 51 | refocusKeyboard: first committed surface via `Desktop::focusState()->rawSurfaceFocus(surface)`; no-surface branch logs "called with no committed surfaces. This should never happen." | FocusGrab.cpp:94-111 (quote :110) | ok |
| 53 | onCreateGrab: `!RESOURCE->good()` → `pMgr->noMemory()` + pop from m_grabs | FocusGrab.cpp:165-173 | ok |
| 55 | INF: nothing in FocusGrab.cpp consults a window/workspace rule | `grep -in rule` exit 1; `grep -in 'window\|workspace'` exit 1 on receipt | ok |
| 61 | S289: latest session 2026-10-25T13:36:24-03:00 pid 1952; "Got interface: hyprland_focus_grab_manager_v1 (ver 1)"; opens "Gathering exported interfaces" after "XDG_CURRENT_DESKTOP set to Hyprland" | journal:117 (advert), :83, :82 | ok |
| 63 | census `journal sessions=2 adverts=78 interfaces=63 focus_grab=1` | script recount: portal processes=2 (1918/1952); adverts 15+63=78; distinct names s2=63, zero duplicates; focus_grab adverts=1 | ok |
| 65 | session structure: pid 1918 slice opens mid-stream 13:16:45 with 15 adverts, closes at "Stopped Portal service (Hyprland implementation)."; pid 1952 opens at "Starting Portal service (Hyprland implementation)", carries other 63; `-- Boot` marker between | journal:1 (13:16:45), :76 (Stopped…), :78 (-- Boot), :79 (Starting…), 15 vs 63 adverts | ok |
| 67 | INF: first session is a slice (lower bound); only latest session is a whole advertisement, 63 distinct names, none twice | slice has no "Starting" line for 1918; s2 name set unique | ok |
| 69 | onGlobal lines 85-261; log `Debug::log(LOG, " | Got interface: {} (ver {})", INTERFACE, version);` before any branch; exactly ten named branches (screencopy, global shortcuts, input capture, xdg-output, toplevel export, wl_output, dmabuf, wl_shm, foreign toplevel, toplevel mapping); no focus-grab branch | PortalManager.cpp:85-261; log :88 verbatim; branches :90, :95, :99-101, :102, :108, :113, :122, :246, :249, :257; no focus-grab branch in lines 62-591 | ok |
| 71 | `grep -in focus` over PortalManager.cpp exits 1; whole journal contains "focus" exactly once (advert line); same session logs `[input-capture] init successful` and `[globalshortcuts] registered` | grep exit=1 (measured); journal "focus" hits=1 (line 117); journal:135, :128 | ok |
| 73 | S037: installed package record read → `%NAME% xdg-desktop-portal-hyprland %VERSION% 1.4.1-2`; portal source pin v1.4.1 = running unit; cc8e5ef is S037 row anchor, not re-fetched | host desc file verified (§0); upstream tag v1.4.1 byte-identical for PortalManager.cpp; entry states the anchor was not re-fetched (consistent, no new fetch made) | ok |
| 75 | INF: advertisement is compositor fact; portal bind list excludes manager; XML names no app-id/sandbox/permission condition | bind list checked (:69); full XML (128 lines) contains no such gates | ok |
| 77 | INF: hyprctl version printed "Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f" | `hyprctl version` on host today = exact substring; same commit as S284 pin | ok |
| 83 | S285 sync comment "the protocol will always send cleared() when the grab is deactivated," — matches compositor finish(true) path; explains finish(false) for teardown | quickshell-grab.cpp:78; FocusGrab.cpp:68-69 / :31-33 | ok |
| 85 | S285 addWaylandWindow: "this->pendingAdditions.append(window); this->commitRequired = true;" — "adding a window records it and *defers* the protocol call; `sync()` is the only place that commits" | quote verbatim :67-68; **but** `add_surface` is sent *immediately* on :66 (`this->add_surface(window->surface());`) — only the `commit` is deferred; `sync()` is indeed the only caller of `commit()` (:75) | **overstated (wording)** — see finding F1 |
| 87 | S285 sync: "if (!this->active) { this->active = true; emit this->activated(); }" — active flips only after a commit that left pending additions; `hyprland_focus_grab_v1_cleared()` sets active=false and emits cleared | quickshell-grab.cpp:80-86, :98-101 verbatim | ok |
| 89 | addWindow/removeWindow: not-yet-QWaylandWindow added on surfaceCreated or visibleChanged after window->create(); removal disconnects, drops from pendingAdditions, calls remove_surface, sets commitRequired | quickshell-grab.cpp:21-53, :55-63 | ok |
| 91 | INF: startTransaction/completeTransaction suspend sync(); one commit, at most one activated | :91-96; sync() early-return :72; completeTransaction→sync once | ok |
| 97 | issue 565 body: rule `windowrule = workspace 4 silent,^(pavucontrol)$`; "If a workspace windowrule contains silent then matching windows should not get focus"; "When the new window opens in a different workspace, it seems to steal it momentarily" | issue-565.html text extraction: all three present verbatim | ok |
| 99 | issue log excerpt: "Tried to set workspace silent rule to a nofocus window!" | present verbatim | ok |
| 101 | maintainer reply Aug 2022 "fixed in b09f157"; issue closed; predates 0.56 by years | "vaxerski commented on Aug 26, 2022 … fixed in b09f157"; state CLOSED; issue created 2022-08-23 vs v0.56.2 tag 2026-08-05 | ok |
| 103 | README: "for grabbing input focus, primarily for complex context menus"; "we have to maintain a set of protocols Hyprland uses"; wayland-protocols slow to change / no Hyprland-specific work | protocols-README.md:17, :8-9 | ok |
| 105 | INF: two layers/two owners; rule subject = window, grab subject = surface set | supported by S283/S284/S287 | ok |
| 109 | INF: lane holds no focus-rule knowledge: `grep -rli 'focus_grab\|focus-grab\|focus grab' corpus PROVINCE.md SKILL.md tools` exits 1 at base; window-rule-effects-getprop.md & workspace-rules-r27.md contain no focus line; rule-attribution-r24.md only hit is block rule `jetbrains-focus` | re-run at base ab2bfaab…: master grep exit 1; `git grep -ni focus` window-rule-effects-getprop.md exit 1; workspace-rules-r27.md exit 1; rule-attribution-r24.md single hit line 81 containing `jetbrains-focus` | ok |
| 115-126 | decision table rows | all derive from rows verified above (§1/§2/§3/§4/§5) | ok |
| 130-136 | §7 caveats (no live grab, census limits, 2022 record, CSeatGrab unread, non-security, v1.4.1-scoped, r28 §3 excluded) | consistent with receipts and measured constraints | ok |

## 2. Finding

**F1 — L85 (minor, overstated/ambiguous wording; the only defect found).**
`**OBS** S285 (FocusGrab::addWaylandWindow): … "adding a window records it and *defers*
the protocol call; sync() is the only place that commits."`
The quoted string is verbatim, but the gloss "defers the protocol call" is not true of
`add_surface`: in `quickshell-grab.cpp:65-69` the client calls
`this->add_surface(window->surface());` **immediately** (line 66) before appending to
`pendingAdditions`; what is deferred is only the `commit` (the second half of the sentence is
correct — `sync()` is the only caller of `commit()`, :75).
Reproduction:
```
fetch/quickshell-grab.cpp:65-69
65  void FocusGrab::addWaylandWindow(QWaylandWindow* window) {
66      this->add_surface(window->surface());
67      this->pendingAdditions.append(window);
68      this->commitRequired = true;
69  }
```
Impact: no protocol fact is broken (batch/commit behavior is described correctly elsewhere,
incl. decision-table row L122), but the sentence misstates the deferral point. Suggested fix
(L1): "records it and defers the *commit* (`add_surface` is sent immediately); `sync()` is
the only place that commits." Classification: overstated (wording), on the DATA (entry).

No other defect found. All counts, quotes, locators, pins, host facts, and UNK designations
below survived attack.

## 3. UNK audit (are the "unknown" items actually answerable from the receipts?)

| UNK | line | answerable from receipts? | verdict |
|---|---|---|---|
| "implementation-defined criteria"/"similar action" beyond pointer/touch-outside and competing grab | 39 | XML uses "usually" and "similar action" non-exhaustively (xml:72-76); FocusGrab.cpp implements only the branches (start/finish/commit/refocusKeyboard); seat-manager routing code not in receipt set | genuinely unknown; correctly marked |
| CSeatGrab outside-input routing | 57 | `CSeatGrab` only forward-declared (hpp:12); no SeatManager.cpp in fetch/ | genuinely unknown; correctly marked |
| one Qt transaction = one frame; cleared between add_surface and commit observable? | 93 | requires running a Wayland client / measuring frames — prohibited by host rules (no Wayland client of own) | genuinely unknown; correctly marked |
| does 0.56.2 still exhibit #565 momentary steal | 107 | record is 2022 vs unnamed revision; measuring requires input injection / focus-transition test — prohibited | genuinely unknown; correctly marked |
| which process binds focus-grab today | 79 | whole journal scanned: "focus" occurs exactly once (advert); no bind-side log exists in receipts; answering requires own client — prohibited | genuinely unknown; correctly marked |

## 4. Commands run (all read-only; reproduce)

- Entry: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 07f2641696b5ac73de1404ea737a9f27e9819aa1:corpus/knowledge/hyprland-focus-grab-r41.md`
- Receipt hashes: `cd …/.ufo/waves/round-41/fetch && sha256sum *` (S289 = `bf8fa91a…` ✓)
- Journal counts: python3 script over `xdph-journal.txt` (sessions=2 portal pids, adverts 15/63, distinct names 8/63, dups=0, focus hits=1)
- PortalManager/`grep -in focus xdph-PortalManager.cpp; echo $?` → 1 (no output)
- FocusGrab.cpp rule-consult check: `grep -in rule Hyprland-FocusGrab.cpp` → 1; `grep -in 'window\|workspace' …` → 1
- Host: `hyprctl version` → "Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean ([gha] Nix: update inputs). Date: Wed Aug 5 14:13:21 2026 Tag: v0.56.2"
- Host package: `sha256sum /var/lib/pacman/local/xdg-desktop-portal-hyprland-1.4.1-2/desc` → `7bf2f8be…` (matches receipt); `%NAME%`/`%VERSION%` = xdg-desktop-portal-hyprland / 1.4.1-2
- Upstream pin byte-identity: `git fetch --depth 1 origin <pin>` + `git show FETCH_HEAD:<path> | sha256sum` for S283/S284(cpp+hpp)/S285/S286@v1.4.1/S288 — all equal local receipt hashes
- Base-lane INF: `git -C lane grep -rli 'focus_grab\|focus-grab\|focus grab' ab2bfaab661c846d1de9d58c01651cd156a13949 -- corpus PROVINCE.md SKILL.md tools` → exit 1; `git grep -ni focus` on the three md files → 1 / 1 / single hit line 81
- Issue 565: python3 HTML-text extraction for the five quotes + `"state":"CLOSED"` + createdAt/comment dates

## 5. Tooling / installs

No package or tool was installed this round (no pacman, no uv/npx/binary installs); only
pre-existing git, python3, sha256sum, grep were used. Tooling-authorization rule: nothing to
record beyond "none".

## 6. Risks / blockers

- The four pinned receipts and the journal are byte-verified; the issue-565 HTML was
  validated for content and closed-state, not byte-compared to a fresh fetch (GitHub page
  HTML is non-deterministic; the receipt's quotes/state are authoritative here).
- The §5 "at base" grep was re-run at exactly `ab2bfaab…`; the working tree may now contain
  the entry itself (which does contain `focus_grab`), so a re-run on the **working tree**
  would not reproduce the base result — the claim is properly scoped to base and verified there.
- `hyprctl version` output includes "clean ([gha] Nix: update inputs)" outside the quoted
  substring; the entry quotes only the substring it reproduces exactly.
- No blockers. All checks executed; single minor finding (F1).

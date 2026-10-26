# ScoutRefuted — round 41 w2 (attack: are the refusals true, is anything admissible left?)

Read-only. No tracked file edited, no package transaction, no Wayland/compositor connection, no `hyprctl` except `hyprctl version`.
Network reads (curl / `read`) of public pages only; scratch in `/tmp/sr41` (removed at the end). Tools installed: none.
Package read: `/home/vgpnk/Projects/shokuknow/merge/mado` (read-only). Data read at `07f2641` (`git show 07f2641:<path>`).

## 0. Verdicts in one table

| item | registered refusal | refusal reason TRUE? | should it have been admitted? |
|---|---|---|---|
| `privileged-client-surface-r29.md` (S244) | generic analysis, one truncated quote, no measurement, no host state | **TRUE, and understated**: the staged row/entry misstate the source (section 1) | **No** |
| `focus-control-surfaces-r28.md` section 3 (S230) | localized (Japanese) documentation channel, outside PROVINCE.md | **TRUE by the letter** of `PROVINCE.md:75`; the quotes/location are accurate (section 2) | **No for the source; yes for the fact** — the fact is in held English row S165 (section 2) |
| r28 section 2 (S227) | (folded into the successor as S287) | the staged "`silent` is not a focus guarantee" is unsupported for 0.56.2 (closed 2022) | handled correctly by the entry's UNK; one attribution defect (section 3, D1) |
| r28 section 1 (S229) | admitted as S283 | n/a | already admitted |

Three DATA defects found in the admitted entry (`hyprland-focus-grab-r41.md` at `07f2641`), section 3: **D1** (b09f157 misattributed), **D2** (`refocusKeyboard` described without its early return, and "first committed surface" is the wrong operative rule), **D3** ("lane holds no focus-rule knowledge" is false). No PREDICATE defect found by this seat.

## 1. `privileged-client-surface-r29.md` / S244 — re-opened `https://blog.ce9e.org/posts/2025-10-03-wayland-security/`

Fetched 2026-10-25: `curl -sfL … -o s244.html` → **6288 B** (served as markdown source; front matter line 5 is `description: "How do privileged clients in Wayland work exactly? Well, it's complicated."`).

Verified TRUE:
- quote 1 exists (`s244.html:5`); quote 2 exists and **is truncated**: `s244.html:96` reads "But there is also `WAYLAND_SOCKET`, which tells them to use an already connected file descriptor instead." The staged quote stops at "which" (r29 line "But there is also `WAYLAND_SOCKET`, which").
- `grep -c -i hyprland s244.html` → **0**. The post never mentions Hyprland, a focus grab, or `hyprland-protocols`.

Defects the registered reason does not name (reason stays correct; these are *additional*):
- **The entry and row S244 invert the source's status quo.** Entry §1 INF: "privileged interfaces are granted to clients the compositor spawns, and the descriptor handoff is what makes the grant hard to steal." Row S244 (`SOURCES.append.md:48`): "Privileged interfaces are granted at bind time to clients the compositor spawns, and the `WAYLAND_SOCKET` descriptor handoff is the mechanism that makes the grant non-stealable". The post says the opposite of the status quo (`s244.html`, Conclusion): "wlroots-based compositors implement privileged interfaces, and any non-sandboxed processes can access them. That is way too much attack surface for my taste." The `WAYLAND_SOCKET` handoff is the **author's own unmerged labwc branch** (`labwc/labwc#3089`: "I don't expect that it will be merged"), has "one major issue" (privileges apply "only to the first client, not any of its children"), and the author cannot decide whether it is "a step in the right direction or mere security theater" (`s244.html:117`).
- The inference "A focus-grab client is therefore a privileged client" has no support in the post (0 hits for focus/grab/Hyprland); on this host the receipts show the opposite — the manager is advertised to every client and the only gate is the registry (entry §3 INF, S283/S286/S289), i.e. Hyprland does not gate focus-grab by spawn lineage in any receipt.
- Row size claim "page, 3135 B" does not match the fetched page (6288 B). [INFERENCE: the row counted text, not source.] Not load-bearing.

Conclusion: refusal confirmed; **nothing admissible**. The only reusable piece is "unsandboxed clients always privileged / security-context-v1 for sandboxed ones" — still a generic Wayland claim with no host state.

## 2. `focus-control-surfaces-r28.md` section 3 / S230 — re-opened `https://amgsk.dev/posts/hyprland-rules/`

Fetched 2026-10-25: 22299 B. Heading `JetBrains IDE のフォーカス問題を修正` present (grep); `no_focus on` x2 and `no_initial_focus on` x2 present; the two staged quote lines exist verbatim (`windowrule = match:class ^(.*jetbrains.*)$ title:^(win.*)$, no_focus on` / `…no_initial_focus on`). Page dated 2026-03-01 (front matter `published_time`), `og:locale ja_JP`. So the **location and quotes are accurate**; the row's "4804 B" is not the byte size of the page (22299 B raw) — immaterial.

Is the refusal reason true? `PROVINCE.md:75` (at `07f2641`): "documentation written in a localized channel — is outside the province". A personal Japanese-language blog is "documentation written in a localized channel" by the rule's letter, and the entry's own `ground:`/lesson cite it. TRUE. (Judgement call, not a defect: the rule text lists ArchWiki-channel mechanics first; a personal blog is the broader tail clause. The lane applied it consistently with the registered clause-i refusal.)

**But the fact survives without the source.** The rule-level counterpart ( `no_focus`, `no_initial_focus`, `no_follow_mouse`, `stay_focused` ) is documented in the **English** channel the lane already holds:
- `curl` of `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/window-rules.md` = 16200 B (= the held S165 size): line 78 `no_initial_focus | Disables the initial focus to the window`; 157 `no_focus | Disables focus to the window`; 158 `no_follow_mouse | Prevents the window from being focused when the mouse moves over it when input.follow_mouse=1 is set`; 176 `stay_focused | Forces focus on the window as long as it's visible`.
- The 0.56.0 wiki page (`https://wiki.hypr.land/0.56.0/Configuring/Basics/Window-Rules/`) carries the same effect table (`no_focus boolean Disables focus to the window.` etc.); that URL is **not** a held row.
- The lane also holds the host's own use of these keywords: `corpus/knowledge/keybind-rule-semantics.md:189,210,225,229-232` (`windows.conf:9` `no_focus on`; `webcam-overlay.conf:4` `no_initial_focus`; `focus_on_activate off`; `no_follow_mouse` in `jetbrains.conf`; `stay_focused`).

So "the unheld English-channel facts return in the successor" (lesson ledger) is true for S227/S229 but the entry's §5 did **not** use held S165 for the rule-level keywords it names in its own heading ("The rule-level counterpart"); see D3.

## 3. DATA defects in `hyprland-focus-grab-r41.md` (read at `07f2641`)

**D1 — "fixed in b09f157" is the wrong fix (entry §5, S287).** Entry: `**OBS** S287 (maintainer reply, Aug 2022): "fixed in b09f157" - the issue is closed`. In `fetch/issue-565.html` the order is: Aug 25 maintainer "should be fixed hastily, will prolly have to make a more robust solution in the future"; Aug 25 "done and working." + `closed this as completed` (`ClosedEvent` 2022-08-25T23:08:33Z, `stateReason: COMPLETED`); Aug 25 reporter: "Might I be doing something wrong here then? … Still messes with fullscreen windows on my machine"; **Aug 26** maintainer "fixed in b09f157", reporter: "That does in fact fix the fullscreen issues." (python text-strip of the receipt, `fixed in` match.) b09f157 fixes the **follow-up fullscreen** complaint, not the silent-rule focus steal (which was closed the day before, and for which the maintainer said a hasty fix). The quote is exact but reads as the closing fix of the entry's topic. Repro: `python3` strip tags on `fetch/issue-565.html`, print 2600 chars after `vaxerski closed this as completed`. Suggested fix: attribute b09f157 to the fullscreen follow-up, or drop the quote.

**D2 — `refocusKeyboard` is stated without its early return, and its "first committed surface" is not the operative rule (entry §2).** Entry: "the keyboard is moved to the first committed surface through `Desktop::focusState()->rawSurfaceFocus(surface)`". `Hyprland-FocusGrab.cpp:94-111`: lines 95-97 `auto keyboardSurface = …keyboardFocus; if (keyboardSurface && isSurfaceCommitted(keyboardSurface.lock())) return;` — an early return; the "first" is an iteration of `std::unordered_map m_surfaces` (line 100), so "first" is unspecified, not "first added". And order matters: `CFocusGrab::start` (lines 47-56) calls `g_pSeatManager->setGrab(m_grab)` **before** `refocusKeyboard()`; `CSeatManager::setGrab` ends with `m_seatGrab = grab; refocusGrab();` (`SeatManager.cpp` @efb5099 lines 788-790), and `refocusGrab()` (582-611) focuses the whitelisted surface whose global box contains the mouse, else `m_surfs.at(0)` (the first *added*, a `std::vector`, `SeatManager.hpp:40`). So the effective pick on start is the seat grab's, and `refocusKeyboard()` usually early-returns. The entry's §1 INF ("compositor-picked") and UNK (§2 "CSeatGrab routing … not read") hedge correctly; only the §2 OBS sentence misleads. Fetch (public, today): `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/SeatManager.cpp` sha256 `bd7485535c7e9f71382e587d92a7c73e048a0d7a5efcf518a1e671a188f94378`, 26074 B; `…/SeatManager.hpp` sha256 `d1ac1c45e8ba329827f46b371b96df42fad3f6dccd92917f98f0046d6fa3bb44`, 6511 B. `git ls-remote`-equivalent: `api.github.com/repos/hyprwm/Hyprland/git/ref/tags/v0.56.2` → sha `efb50993780079460b0cbed1363e2166a2de1d9f`.

**D3 — "The lane holds no focus-rule knowledge either" is false (entry §5 INF).** Counter-evidence at `07f2641`: `corpus/knowledge/keybind-rule-semantics.md:189,210,225,229-232` and `config-health-report-r3.md:526` / `hyprctl-verification-layer.md:107` (`misc:focus_on_activate`). The entry's sentence is scoped by three file names, but its first clause ("holds no focus-rule knowledge") is general. Fix: say the held rows are *usage* of `no_focus`/`no_initial_focus` on the host config, with the effect semantics in held S165 lines 78/157/158/176, and the focus-steal behaviour of silent rules is what S287 adds.

Minor (no fix required): the entry's S287 quote `workspace 4 silent,^(pavucontrol)$` matches the receipt (54 hits) while the staged r28 §2 used `workspace 1 silent,^(librewolf)$` (33 hits); both exist in the issue, so the two entries are internally consistent. `Expected behavior` is the receipt's spelling (staged location `Expected behaviour`).

## 4. Staged focus-theme entries citing private `lanes/mado/roundN/fetch/...` receipts

`grep -n 'lanes/mado/round' …` over the 13 focus-theme files: exactly **four** entries, one private row each. The receipts exist in the shokuknow checkout (`/home/vgpnk/Projects/shokuknow/lanes/mado/roundN/fetch/`), not in the lane:

| entry | row | private path | bytes | reproducible today? |
|---|---|---|---|---|
| `focus-grab-seat-semantics-r8.md:8` | S275 | `lanes/mado/round8/fetch/host-focus-grab-and-timeout.txt` | 834 | symbol census; w1 `ScoutPackageFocus` re-ran: 89 strings in `/usr/bin/Hyprland` |
| `focus-grab-observed-semantics-r9.md:10` | S293 | `lanes/mado/round9/fetch/host-compositor-log-scan.txt` | 567 | not re-run (compositor log) |
| `focus-grab-protocol-live-on-host-r14.md:9` | S328 | `lanes/mado/round14/fetch/host-focus-grab-portal-advertisement.txt` | 1088 | **no**: receipt says "2 adverts at both boots (2026-10-23)"; today's journal has 153 lines, `-- Boot 7ab69ee…` at line 78, **1** `focus_grab` line (117, 2026-10-25T13:36:24, pid 1952) |
| `focus-grab-has-no-client-here-r15.md:7` | S338 | `lanes/mado/round15/fetch/host-focus-grab-client-sweep.txt` | 622 | **yes** — this seat re-ran the method: `grep -rl 'hyprland_focus_grab' /usr/bin /usr/lib /usr/local/bin ~/.local/bin ~/.local/share/omarchy/bin` → only `/usr/bin/Hyprland` (16 s); `/usr/libexec`, `/usr/lib/x86_64-linux-gnu`, `/usr/lib/wayland` do not exist on this host (3 of the receipt's 8 swept dirs) |

Package-wide: 26 staged files contain `lanes/mado/round` (`grep -rl … | wc -l`); only the four above are focus-theme. The entries r10, r11, r12, r13 and r16 cite **only public URLs**; r26/r8-literature/r29 cite public pages too.

## 5. Should any refused/unadopted item have been admitted this round?

No candidate was ready to land without new work, with one qualification:
- r29, r28 §3: no (sections 1-2).
- r15 (`has-no-client-here`): **not admissible as written** (private receipt as sole source; staged claim reproducible only after re-measuring) — but this seat's re-run reproduces the exact result today. It would have been an own-work row (second own-work row after S289; the registered scope kept one own-work row).
- r14 `protocol-live-on-host`: admitted as the successor, correctly re-grounded (S289 replaces S328).
- r11/r12/r13-compositor/r10: their public sources (SeatManager.cpp/.hpp @v0.56.2) were **not in `fetch/`** this round, so holding them was correct; nothing to admit without a fetch. (The registration pre-fetch stopped at the seven receipts.)

The one qualification is **D3**: the rule-level part of §5 could have been grounded on held S165 (A, English) rather than on a closed 2022 tracker alone. That is an enrichment of the admitted entry, not an extra admission.

## 6. The lane's next-round candidates (ordered by closing-power)

1. **Seat-side routing of a focus grab** — fetch at `efb5099` (all public, fetched/hashed here): `src/managers/SeatManager.cpp`/`.hpp`, **plus `src/managers/input/InputManager.cpp`** (sha256 `feedf32e…e4765`, 98845 B). Staged r11 is **true** at efb5099 (`refocusGrab`, `SeatManager.cpp:582-611`; `m_surfs` a `std::vector`, `SeatManager.hpp:40`). Staged r12 is **incomplete**: its claim "a surface outside the whitelist is refused input" rests on `accepts()` (`SeatManager.cpp:806`) alone; its only caller is `InputManager.cpp:596` — `if (m_seatGrab && !m_seatGrab->accepts(foundSurface) && !PROTO::data->dndActive()) { if (m_hardInput || refocus) { setGrab(nullptr); return; } else { foundSurface = pointerFocus … } }` — i.e. outside **motion** pins the pointer to the last surface, an outside **button press** (`InputManager.cpp:935-939`, `m_hardInput = true; simulateMouseMovement()`) ends the grab via `setGrab(nullptr)` → `m_onEnd` → `cleared`. Staged r12 §3 "tears the whole thing down when the whitelist is withdrawn" omits this trigger. **Do not adopt r10** (self-refuted by r11; `unordered_map` first-pick is only the fallback in an early-return branch). This candidate closes the admitted entry's §2 UNK, §1 UNK ("implementation-defined criteria") and the amended §6 row "What ends an active grab?".
2. **r13 keyboard routing**, compositor half only: `CSeatManager::sendKeyboardKey` (`SeatManager.cpp:255-270`, loops `m_seatResources`, skips seats whose client differs from `keyboardFocusResource->client()`) is public and true as staged. The rest of r13 cites a Japanese blog (S323, refused by PROVINCE) and a `r.jina.ai`-proxied PDF (S324) — split it.
3. **r15 as own-work** (row, not prose): re-measure with a pinned command line; note the swept-dir list differs from the host layout (3 of 8 dirs absent).
4. **r16 `upstream-input-holds-and-the-lock-screen`** (S349): both quotes verified verbatim on `https://wiki.hypr.land/configuring/core/binds/flags/` today (269491 B; `locked` row "Will also work when an input inhibitor (e.g. a lock screen) is active."; `allow_input_capture` row "When input is captured by a client, this bind will still be processed."). It is a different claim (bind flags vs idle-lock), an unversioned `latest` page (Lua-era `hl.bind`); its INF "the idle lock … installs an inhibitor" has no source in the entry. [INFERENCE] separate lane residual, not the focus-grab series.
5. **Literature entries**: `compositor-focus-manipulation-literature-r26.md` (arXiv 2604.18860 abstract, 3 quotes, X11-scoped, entry says so in §3) and `wayland-input-security-literature-r8.md` (S278 mupuf publication record, S279 HAL record, both public) are public, honest about scope and have no host state; they are admissible as literature coverage in a round whose claim is literature coverage — no overlap with the C2 entry. The package's `S218` id collides with the lane's S218 (hyprlang) — re-issue ids from S290+ (w1 `ScoutPackageFocus` finding 1).
6. **English-channel rule-level focus keywords** as a short entry on held rows S165 (+S017) with the host usage already held in `keybind-rule-semantics.md`: replaces the refused r28 §3 with no localized source (D3).

## 7. Commands run (all read-only)

- `curl -sfL https://blog.ce9e.org/posts/2025-10-03-wayland-security/` ; `grep -n -i 'description|WAYLAND_SOCKET'`; `grep -c -i hyprland` → 0.
- `curl -sfL https://amgsk.dev/posts/hyprland-rules/` ; `grep -o 'no_(initial_)?focus on'` → 2 + 2.
- `curl` of the 0.56.0 wiki Window-Rules page; of hyprland-wiki `c66e8de…/window-rules.md` (16200 B) with `grep -n no_focus|no_initial_focus|stay_focused|no_follow_mouse`.
- `curl` of Hyprland `efb5099` `SeatManager.cpp`/`.hpp` and `InputManager.cpp`; `sed -n 575,625p`, `765,795p`, `590,606p`, `930,960p`.
- python strip-tags of `fetch/issue-565.html` around `closed this as completed`, `fixed in`.
- `grep -rl 'hyprland_focus_grab' /usr/bin /usr/lib /usr/local/bin ~/.local/bin ~/.local/share/omarchy/bin`; `hyprctl version` (0.56.2 efb5099).
- `git show 07f2641:…` for the entry, lesson, `keybind-rule-semantics.md`, `PROVINCE.md`, `SOURCES.md`.

## 8. Unknowns

- Whether the S230 Japanese-blog refusal would survive a reviewer who reads `PROVINCE.md:75` as limited to ArchWiki-channel mechanics (judgement, not measured).
- The remainder of `InputManager::mouseMoveUnified` after line 606 was not read; the "outside motion pins to last surface" description stops at what the visible lines state.
- r9's (S293) compositor-log scan and r8's symbol census were not re-run by this seat.

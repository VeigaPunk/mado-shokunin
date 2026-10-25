# ScrEntryB — Draft B of the C2 entry (host-first scope), round 41 w1

STATUS: complete. Deliverables (all inside the lane, nothing committed, nothing outside the seat):

- entry draft: `.ufo/waves/round-41/w1/ScrEntryB/hyprland-focus-grab-r41.md` (86 lines; destination when the L1 integrates:
  `corpus/knowledge/hyprland-focus-grab-r41.md`)
- quote/shape verifier: `.ufo/waves/round-41/w1/ScrEntryB/verify-quotes.py` (read-only; simulates clauses b, d-quote, g, h
  and the channel guard on the draft)
- this report.

## 1. What the draft does

Title: "Focus as a protocol surface on this host: the grab manager the compositor advertises to its portal, the protocol's
promise, a client's lifecycle, and the rule-level counterpart". `Lane: mado-shokunin. Round: 41.` at line 15. Header within
the first 20 lines: 8 `source:` lines (S283-S290), `verified-at: 2026-10-25`, `recheck: 90d - ...`, `ground:` pointer.
Six sections, ordered host-first as the assignment required:

1. **§1 the host** - the portal's own journal census (`journal sessions=2 adverts=78 interfaces=63 focus_grab=1`, line 21,
   outside any fence, exactly once), the source line that makes an advert mean "registry global received, before any bind"
   (S286), the class table applied to the 63 names as an INF classification of names only, the input-capture contrast (S290),
   the held prior census (S041) and the reason 63 is not "the compositor's global set".
2. **§2 the protocol** (S283, S288): description, the whitelist object, commit semantics, the `cleared` event.
3. **§3 the compositor** (S284): seat grab with keyboard+pointer, `start` → `simulateMouseMovement` + `refocusKeyboard`,
   `commit` transitions, `finish(sendCleared)`, and the INF about when `cleared` is and is not sent.
4. **§4 a real client** (S285): quickshell's add/commit/active path, its "cleared always arrives" comment, its cleared handler.
5. **§5 the rule-level counterpart** (S287 + held rule/option rows): the 2022 focus-stealing issue, the reporter's
   `workspace ... silent` workaround, the compositor's own nofocus log line, and the held rule vocabulary
   (`no_focus` dynamic, `no_initial_focus` static, `focus_on_activate off`, `stay_focused`, `misc:focus_on_activate` = 1).
6. **§6 what this does not license** - advertisement ≠ capability, 63 ≠ global set, second-grab behaviour UNK, the 2022 issue's
   scope, one host/one date, no localized channel.

## 2. Gates run (all read-only, by this seat)

`cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I .ufo/waves/round-41/w1/ScrEntryB/verify-quotes.py` → rc 0:

```
header ids: S283 S284 S285 S286 S287 S288 S289 S290
lines: 86 fenced-balanced: True
S283 focus-grab-v1.xml            words=11 receipt=1 entry-line=1
S284 Hyprland-FocusGrab.cpp       words= 3 receipt=1 entry-line=1
S285 quickshell-grab.cpp          words=11 receipt=1 entry-line=1
S286 xdph-PortalManager.cpp       words= 5 receipt=1 entry-line=1
S287 issue-565.html               words=10 receipt=1 entry-line=1
S288 protocols-README.md          words= 9 receipt=1 entry-line=1
S289 xdph-journal.txt             words= 5 receipt=1 entry-line=1
S290 input-capture-v1.xml         words= 7 receipt=1 entry-line=1
census: journal sessions=2 adverts=78 interfaces=63 focus_grab=1 | parsed: (2, 78, 63, 1) | equal: True
VERDICT: PASS
```

The verifier uses the counter's own `norm()` (strip script/style, strip tags, unescape, collapse whitespace), the counter's
ADVERT/BOOT grammar for the census, and the Gate strings the rows seat sent. It also checks that no line carries another
cited id's Gate quote (one quote per id-line) - one early FAIL (the S290 line mentioned S289) was fixed by replacing the id
with "§1"; PASS above is the post-fix run.

Gate strings and the line that carries each (for the L1's Gate block; all verbatim substrings of the receipt, verified):

| id | receipt under `.ufo/waves/round-41/fetch/` | words | entry line | string |
|---|---|---|---|---|
| S283 | `focus-grab-v1.xml` | 11 | 41 | `This interface restricts input focus to a specified whitelist of surfaces` |
| S284 | `Hyprland-FocusGrab.cpp` | 3 | 49 | `m_grab->m_keyboard = true;` |
| S285 | `quickshell-grab.cpp` | 11 | 63 | `the protocol will always send cleared() when the grab is deactivated,` |
| S286 | `xdph-PortalManager.cpp` | 5 | 23 | `Got interface: {} (ver {})` |
| S287 | `issue-565.html` | 10 | 71 | `Tried to set workspace silent rule to a nofocus window!` |
| S288 | `protocols-README.md` | 9 | 39 | `for grabbing input focus, primarily for complex context menus` |
| S289 | `xdph-journal.txt` | 5 | 19 | `Got interface: hyprland_focus_grab_manager_v1 (ver 1)` |
| S290 | `input-capture-v1.xml` | 7 | 27 | `Add one barrier to the current session` |

Receipt hashes as read this seat (`sha256sum` in the fetch dir): focus-grab-v1.xml `0bc60c14…0285b4`,
Hyprland-FocusGrab.cpp `53b762f7…2aff1`, quickshell-grab.cpp `6f7cecf1…01a40`, xdph-PortalManager.cpp `15c3e39c…1ea55`,
issue-565.html `148a9053…79d1dc`, protocols-README.md `3c700763…aa6323`, xdph-journal.txt `bf8fa91a…0aaf7` (153 lines),
input-capture-v1.xml `fff89f6f…c360`.

## 3. Census, re-derived (not taken from the brief)

Parsed `.ufo/waves/round-41/fetch/xdph-journal.txt` with the counter's grammar: 2 sessions (pid 1918 from 13:16:45-03:00,
15 adverts over 8 distinct names; pid 1952 from 13:36:24-03:00, 63 adverts over 63 distinct names), 78 adverts total,
`hyprland_focus_grab_manager_v1` once at line 117 of the receipt. Matches the brief and the counter's expectation.

## 4. Findings (each names what it supports or attacks)

- **Supports the advertisement reading.** `xdph-PortalManager.cpp:85-88`: the `Got interface: {} (ver {})` log is the first
  statement of `onGlobal`, above every `if (INTERFACE == ...)` bind branch; an advert is a `wl_registry.global` event, not a
  bind. This is the S286 Gate quote, so the entry's central distinction is carried by the same string.
- **Attacks "63 = the compositor's global set".** The journal's earlier session (15 adverts / 8 distinct names) holds neither
  `wl_compositor` nor `wl_seat`, which the latest session and S041 both hold → that session is a retained-window fragment. The
  latest session's last line is an advert and it holds no `wl_output` at all, while S041 and the earlier session do → 63 is a
  lower bound. Re-derived from S041 (`.ufo/waves/round-13/w1/globals.json`, captured 2026-10-20T04:10:03Z, wayland-info
  1.3.0-1, Hyprland `efb5099`): 72 records / 71 distinct; every name of the latest journal session is present at the same
  version (set difference empty, version diffs empty); the 8 names S041 holds and the latest session lacks are
  `wl_output`, `wl_drm`, `zwp_linux_dmabuf_v1`, `wp_color_manager_v1`, `wp_drm_lease_device_v1`,
  `wp_linux_drm_syncobj_manager_v1`, `ext_image_copy_capture_manager_v1`,
  `ext_foreign_toplevel_image_capture_source_manager_v1` — all 8 present in the earlier session. Cause UNK; stated as UNK.
- **Supports the class table as classification only.** Applying the C1 docstring table to the 63 names: focus-grab 1,
  input-synthesis 3, input-capture 3, session-lock 2, idle 2, clipboard 3, capture 2, toplevel-control 4, output-control 4,
  sandbox 1, other 38. Two table names in the `capture` class are not advertised in the latest session, consistent with §1's
  caveat; the entry says so rather than implying the class is empty.
- **Attacks "the client's cleared assumption is general".** `Hyprland-FocusGrab.cpp`: `finish(true)` from the seat-grab
  callback (`:22`) and from a commit that leaves no committed surface (`:141`); `finish(false)` from the destructor (`:32`).
  So `cleared` is not sent on explicit destroy or client death — the quickshell comment
  (`quickshell grab.cpp:78-79`, `the protocol will always send cleared() when the grab is deactivated,`) holds for
  compositor-side deactivation and is vacuous for the client's own teardown. Stated as INF from the paths, not as a run.
- **Supports the rule-level counterpart.** `issue-565.html`: the reporter's workaround is a `windowrule` with the `silent`
  workspace flag; their debug log carries the compositor line `Tried to set workspace silent rule to a nofocus window!`, and
  the rule trace above it shows a silent workspace rule matching a window by class; maintainer closed it as completed
  2022-08-25 after "should be fixed hastily, will prolly have to make a more robust solution in the future". Held rows add
  the declared plane: `no_focus` dynamic (`keybind-rule-semantics.md:189,210`), `no_initial_focus` static (`:225`),
  `focus_on_activate off` (`telegram.conf:2`), `stay_focused` (davinci orphan), `misc:focus_on_activate` = 1
  (`hyprctl-verification-layer.md:107`).
- **Supports the class separation.** `input-capture-v1.xml`: `hyprland_input_capture_manager_v1` is declared at version 2
  (`:38`) while the host advertises version 1 — the advertised version is the implementation's, not the protocol file's;
  its session takes barriers (`:68`) and sends input over an EIS socket (`:56`), a different mechanism from the grab.
- **UNK left open, deliberately:** how a second grab displaces an active one (seat manager not in the fetched bytes); which
  internal focus path each rule gates (no rule applicator in the receipts); why the latest session logged 63 and not 71.

## 5. Citation decision on held ids — S037 is NOT cited, and why

The assignment asked for a held id "if it fits". It does not fit under `PRED-C2-r41-v1` clause d: **every** id that appears
as a header `source:` line needs a Gate line whose `receipt=` path starts with `.ufo/waves/round-41/fetch/`, whose blob is
committed at REV, is ≥ 512 B, has the stated sha256, and is distinct per id (path, sha256 and quote all distinct). The frozen
fetch set holds exactly the 9 files, one per S283-S290; there is **no round-41 receipt for S037, S041, S043, S052 or S162**.
Citing S037 as a source line would therefore zero clause d and take C2 to TARGET_MISSED.

What I did instead: the entry cites the 8 new ids only (all with existing receipts), and carries S041 as a **prose held
prior** (§1, "OBS held prior (S041, `.ufo/waves/round-13/w1/globals.json`, ...)"), which the counter does not read as a
citation. If the L1 wants S041 (or S037) as a real citation, the sequence is: add a byte copy under
`.ufo/waves/round-41/fetch/` (S041: the 6011 B `globals.json`; S037: a fetch of the v1.4.1 release page, which does not
exist anywhere in the lane), add the Gate line with its sha256 and a ≤25-word quote from that copy, then add a `source:`
line plus that quote on an id-naming line in the entry — an integration-time edit I cannot make blind, since a quote I have
not seen in the receipt bytes would be fabricated. Rows seat `ScrRowsDraft` was told the same in writing and needs no used-by
edit for held rows on my account.

## 6. Conflicts, reported verbatim

- `ScrRowsDraft` (IRC, after my first draft): "S287 FAILS. Your S287 OBS line (line 69) quotes "New windows in inactive
  workspaces stealing focus", which is NOT in the receipt bytes (grep count 0 in both drafts, so do not rely on the title)."
  Two notes: the line-69 reading was a stale copy (the title quote was removed before that message arrived; the current
  S287 line 71 carries their string), and the second claim does not reproduce here — the title is in the receipt's
  normalized text (my check: `q in n` True, 3 occurrences in `issue-565.html`). Moot either way: the draft uses their string.
- No conflict found between the held entries and the fetched sources; the near-misses are recorded in the entry as scoped
  statements (`no_focus` is described only as a held dynamic-effect classification, never as "makes a window unfocusable"),
  per `ScoutHeldOverlap/overlap.md` §4.A.

## 7. Not done here (out of my scope)

- Registry rows S283-S290 (rows seat), lesson `## Gate` GATE/ADMIT/REFUSE lines, `corpus/README.md` index row, the
  `corpus/knowledge/` placement itself, and the commit — all the L1's.
- No counter was run (C2 needs a committed REV; running it is the main agent's verification step), no control script was
  touched, no reference tool was read beyond the C1 docstring's class table.
- No host read beyond the frozen receipts: I ran no `journalctl`, no `hyprctl`, no Wayland client, no compositor socket.
  The journal census is a parse of the saved receipt only.
- No tool installed, no package manager invoked, no git/jj mutating command anywhere; scratch heredocs ran in the shell, no
  `/tmp` tree was created. Files written: this report, the entry draft, the verifier (seat directory only).

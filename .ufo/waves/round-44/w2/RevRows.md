# w2/RevRows — registry rows S298-S301 + S164 used-by (round 44 data e467892)

Reviewed cell by cell at data commit `e46789213830597348fe96a351ae004d10587385`
(base `6a1a90528fe533cadee506a9fa3e9d13d15cc41f`; parent of data = `03fa5c618b089064…`
= the registration-v2 freeze, so the v2 rules govern). Lane HEAD is `290cddd…` ≠ data
commit, so every lane-side read below is from `git show e467892:…` copies stored in this
seat dir (`SOURCES_data.md`, `entry_data.md`, `lesson_data.md`, `fetch-sha256_data.txt`);
upstream bytes fetched fresh 2026-10-26 by curl into seat dir `fetch-verify/`. Locators
`SOURCES_data.md:N` are `corpus/SOURCES.md` lines at the data commit.

**Verdict: all cells of S298-S301 and the S164 change verified as claimed. No HIGH/MED
finding. One LOW label-precision note (S300 anchor ranges).**

Registry diff base→data is exactly 5 insertions / 1 deletion in `corpus/SOURCES.md`:
S164 (line 176) modified, S298-S301 (lines 247-250) added, no other row touched.

## 1. Pin identity — source/URL serves the pinned bytes: PASS (4 new rows + S164)

Three-way identity holds for every row: curl-today sha256 == row `sha256:` cell ==
`git cat-file blob e467892:.ufo/waves/round-44/fetch/<file>` == `fetch-sha256_data.txt`
pin, and byte sizes match the row cells:

| row (SOURCES_data.md) | file | sha256 (curl 2026-10-26) | B | identical in receipt blob + fetch-sha256_data.txt |
|---|---|---|---|---|
| S298 (:247) | XDGShell.cpp | `d90b534c9097ab573f606c2dad4b5fab6dc31c4ca13240c43ef0bb74da7ed0c0` | 35458 | yes (:3) |
| S299 (:248) | xdg-shell.xml | `7ba7f9c8473deee674cb1f154a18abd0bb0cc072604fc055b0c15e459fc4c7df` | 63846 | yes (:6) |
| S300 (:249) | gdktoplevel-wayland.c | `0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe` | 97548 | yes (:4) |
| S301 (:250) | gkeep-ui.py | `07a3c4a50bf2154edc82f531b1cf2cc3c6e7067e9f2f02d5a4b4d9d27fe5d66a` | 14639 | yes (:5) |
| S164 (:176) | Window.cpp | `d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded` | 124226 | yes (:2) |

No false-URL or staged-bytes problem (the w1 FORGED-PIN/FALSE-URL class is absent here).

## 2. S298 — Hyprland XDGShell.cpp @ v0.56.2/efb5099 (:247) — PASS

- kind `code`, tier `A`: pinned commit-level implementation source — consistent with
  siblings S161-S164. Tag identity verified: `git ls-remote --tags` returns
  `efb50993780079460b0cbed1363e2166a2de1d9f refs/tags/v0.56.2` (lightweight tag → commit).
- scope "How the compositor turns a size into an xdg_toplevel.configure event": evidenced
  by the setSize → scheduleStateApplication → sendConfigure chain below.
- anchor `:354-358 setSize` — :355 `m_pendingApply.size = size;`, :357
  `return m_owner->scheduleConfigure();` ("next configure serial" is real:
  `scheduleConfigure` at :629-637 returns/allocates `wl_display_next_serial`, sent at :642).
- anchor `:443-462 scheduleStateApplication` — function spans 443-461 (doLaterLock defers;
  :455 `m_resource->sendConfigure(m_pendingApply.size.x, m_pendingApply.size.y, &arr);`),
  range covers it fully (462 is a blank line).
- teaches "setSize stores the size as pending state and returns the next configure serial;
  a deferred callback sends one configure carrying the pending size and states" — every
  clause evidenced above; not overstated (the `m_stateUpdate` guard means one deferred send).
- status `mined` / opened `2026-10-26` / recheck `on-release` — matches the lesson's
  registration of the new rows (lesson_data.md:75-77) and the house pattern for
  commit-pinned sources. used-by = the round-44 entry, true: entry_data.md:4 + OBS :36
  cites :354-358 and :455 (inside row ranges).

## 3. S299 — wayland-protocols 1.49 xdg-shell.xml (:248) — PASS

- kind `spec`, tier `A` — protocol definition XML from the official freedesktop repo under
  a tag URL (`/-/raw/1.49/`); spec is the right kind and A is earned by primary+versioned.
- anchor `:1144-1172 configure` — event spans exactly 1144-1172; :1150 "specify a hint to
  the window", :1154-1157 zero → "should decide its own window dimension", :1159-1161
  "specify how the width/height" (states). anchor `:560-590 ack_configure` — request at 560.
- teaches "The configure width and height are a hint for the window geometry; zero leaves
  the dimension to the client; the states say how to read the size" — literal restatement
  of :1150/:1154-1157/:1159-1161; not overstated (the XML binds nobody, and the row says so).
- scope note "(the host's wayland-protocols 1.49-1)" verified read-only:
  `/var/lib/pacman/local/wayland-protocols-1.49-1/desc` `%VERSION%` = `1.49-1`.
- status/opened/recheck as S298 ✓; used-by true (entry_data.md:5, OBS :44 cites :1150,
  :1154-1157, :1159-1161, :560 — all inside the row ranges).

## 4. S300 — GTK 4.24.1 gdktoplevel-wayland.c (:249) — PASS with LOW-1

- kind `code`, tier `A` (GNOME tag URL `/-/raw/4.24.1/`); host note "(the host's gtk4
  1:4.24.1-1)" verified: `/var/lib/pacman/local/gtk4-1:4.24.1-1/desc` `%VERSION%` =
  `1:4.24.1-1`.
- teaches — all clauses evidenced inside the cited ranges: non-zero configured size becomes
  next surface size **plus shadow margins** (:513-521 — :518-519 add
  `next_layout.configured_width +` `…shadow_left + …shadow_right`; the file names them
  `shadow_*`, the teach's "shadow margins" is a fair description); constrained by the
  minimum-size hints (:545 `gdk_surface_constrain_size (&geometry, mask,`); stored for next
  layout (:681 `wayland_surface->next_layout.configured_width = width;`); fixed only under
  maximized/fullscreen/tiled or resizing (:633-637); a 0x0 configure zeroes the stored size
  (:688-689) and compute_size's `> 0` gate (:513-514) falls to the GTK-computed branch —
  "a 0x0 configure leaves the size GTK computes" holds. Not overstated.
- status/opened/recheck as S298 ✓; used-by true (entry_data.md:6, OBS :48 cites :681,
  :633-637 — inside row ranges).

**LOW-1 (anchor label precision, corpus/SOURCES.md:249, S300 anchor cell).** The cell
says "gdktoplevel-wayland.c:444-545 compute_size, gdktoplevel-wayland.c:606-700
handle_configure", but in the pinned bytes compute_size spans **444-554** (the cited end
545 is the first line of the 3-line constrain_size call :545-547; `gdk_wayland_toplevel_update_size`
:548 and :549-554 fall outside) and handle_configure spans **606-707** (:704
`gdk_surface_queue_state_change (surface, ~0 & ~new_state, new_state);` and :706
`XDG_SHELL_CALL (xdg_surface, ack_configure, …)` fall outside). Nothing taught is lost —
every statement's evidence lies inside the cited ranges — so this is a label note, not a
content error and not an OPEN predicate defect. If the L1 wants the ranges to delimit the
named functions, the exact corrected substring of the anchor cell is:
`gdktoplevel-wayland.c:444-554 compute_size, gdktoplevel-wayland.c:606-707 handle_configure`.

## 5. S301 — gkeep ui.py @ 133b867, full file (:250) — PASS

- kind `code`, tier `A`, commit URL; sha256 `07a3c4a5…` equals S297's recorded full-file
  digest (SOURCES_data.md:246), i.e. the held excerpt row and the new full-file row describe
  the same bytes at different granularity — logged and justified in the lesson
  (lesson_data.md:82-84, locations differ so the one-row-per-document rule is not triggered).
- anchor `:446-480 GkeepApp` — :446 `class GkeepApp(Gtk.Application):`, :449
  `application_id="org.omarchy.gkeep",`, :474-476 the window:
  `Gtk.ApplicationWindow(application=self, title="gkeep")` / `window.set_decorated(False)` /
  `window.set_default_size(420, 500)`. anchor `:80-91 button.ink CSS` — :87
  `min-height: 30px;`, :88 `min-width: 72px;`.
- teaches "gkeep declares an undecorated window with a 420x500 default size and no size
  request; its only min-width/min-height belong to a button style" — exact: no
  `set_size_request` anywhere in the file (grep count 0), the only `min-` declarations are
  the button.ink ones. Not overstated (the row also says what the client does NOT declare).
- status/opened/recheck as S298 ✓; used-by true (entry_data.md:7, OBS :56).

## 6. S164 — only used-by changed: PASS

Piece-level split of both row variants (13 pipe-pieces each): exactly one differing piece,
index 11 = used-by; cells 1-10 byte-equal (verified, not asserted):
`corpus/knowledge/rule-attribution-r24.md` →
`corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/hyprland-gkeep-size-request-r44.md`.
- Legal in-place edit: header rule (SOURCES_data.md:5-6) "Only `status`, `recheck` and
  `used-by` change in place, each logged old→new in that round's lesson" — logged at
  lesson_data.md:79-81 with the same old→new strings.
- used-by is true: the entry's source line and OBS cite S164 (entry_data.md:3, OBS :28);
  its quoted receipt line exists in the pinned bytes — Window.cpp:1687
  `return m_realSize->goal().clamp(Vector2D{0, 0}, Math::VECTOR2D_MAX);`.
- The pin still serves: fresh curl of the URL hashes `d735d454…` 124226 B (section 1).

## 7. Findings summary

- **LOW-1** — S300 anchor ranges are sub-spans labeled as whole functions
  (corpus/SOURCES.md:249); exact correction in §4. No content lost, no overstatement.
- No HIGH/MED finding. No OPEN predicate defect found in scope: the four rows are the
  registration-reserved ids (lesson_data.md:76), carry the pinned bytes the C2 v2 clauses
  bind, and no row cell contradicts registration-v2.

## 8. Residual risk / verification gaps

- I did not re-run the C2 counter or controls (other seats' scope); the row review is
  byte- and line-level only.
- Entry-side clause-j surface coverage (report size, sendWindowSize, onAck, …) belongs to
  other seats; I verified only the used-by direction (entry cites each reviewed row) and
  the entry's S298/S299/S300/S301/S164 citation lines land inside the row ranges.
- Host-package identities (`wayland-protocols 1.49-1`, `gtk4 1:4.24.1-1`,
  `hyprland 0.56.2-4`) were read from `/var/lib/pacman/local/*/desc` read-only
  (`%VERSION%` lines); no pacman command was run.

## 9. Method / tooling record

- All checks at the data commit via `git show`/`git cat-file` (read-only); fresh upstream
  curl fetches 2026-10-26; `git ls-remote --tags` for the tag↔commit identity. No tools
  installed (nothing to record under the 2026-10-19 tooling authorization). No pacman, no
  mutating git, no host-service or compositor calls.
- Quote check: 27/28 scripted line-level checks OK (fetch-verify copies); the single
  "FAIL" was my own probe expecting `}` at XDGShell.cpp:462 — the brace is at :461 and 462
  is blank (read directly), consistent with the row's 443-462 range.
- Scratch `/fast/scratch/hyaku/mado-r44/RevRows` was created empty (all evidence stayed in
  this seat dir) and removed; evidence copies cited above live in
  `.ufo/waves/round-44/w2/RevRows/` (`SOURCES_data.md`, `entry_data.md`, `lesson_data.md`,
  `fetch-sha256_data.txt`, `fetch-verify/`, `S164_base.txt`, `S164_data.txt`).

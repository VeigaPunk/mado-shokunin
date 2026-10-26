# ScoutRowsB - re-open of registry rows S292 and S293 (round 43, w2)

Attacks: `corpus/SOURCES.md:241` (S292) and `:242` (S293) at data commit 1959770657f1f8665097c1aed4be6c1cbb07139f; Gate lines `corpus/lessons/round-43.md:37-38`.
Scope: S292/S293 only (other ids in the brief belong to sibling seats). Raw rows copied to `rows-S292-S293-raw.txt` (this dir).

## Re-open evidence (today, 2026-10-26)
- Tag `v0.56.2` resolves (api.github.com/repos/hyprwm/Hyprland/git/ref/tags/v0.56.2) to commit efb50993780079460b0cbed1363e2166a2de1d9f - matches both row anchors.
- curl of the rows' own URLs (commit-pinned raw.githubusercontent):
  - Target.cpp: 3064 B, sha256 49323833c6bc327656e6d02245ebbccf7643fc94f4fbee3cebbae035bbd4ca06 = `receipts/fetch-sha256.txt` = row cell = Gate line. MATCH.
  - WindowTarget.cpp: 16614 B, sha256 8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d = receipts file = row cell = Gate line. MATCH.
- Row shape: `awk -F'|'` NF=13 for both (11 columns). Gate sha256s recomputed against `fetch/` receipts: equal.

## S292 (Target.cpp) - cell verdicts
| cell | verdict | evidence |
|---|---|---|
| id/source (name + URL) | OK | URL is the pinned commit; "layout target - where the box is stored" fits |
| kind `code` | OK | contract kind enum; S214/S290-S294 same |
| tier `A` | OK | upstream source code, scope-limited to "where a target keeps its box" |
| scope | OK | Target.cpp:10-18, :64-74 hold exactly the box store and floating-size memory |
| anchor `:10-18` | OK | 10-14 `void ITarget::setPositionGlobal(const STargetBox& box, uint8_t)`: `m_box = box; m_box.logicalBox.round(); m_box.visualBox.round();`; 16-18 the CBox overload forwarding to it |
| anchor `:64-74` | OK | 64-66 `position()` returns `m_box.logicalBox`; 68-70 `rememberFloatingSize`; 72-74 `lastFloatingSize` |
| anchor tail (tag/commit/bytes/sha/receipt) | OK | all re-verified above; receipt file exists |
| teaches | PARTIAL | first two clauses true (box kept and rounded, line 11-13; `m_floatingSize` kept in a separate member, 68-74). Last clause "so the geometry a window reports is a value the layout wrote" is NOT shown by Target.cpp: `ITarget::position()` returns the target's box, while what `clients -j` reports is the window's own box (S293 `setBox`) read through S158/S294. The clause is an inference joining three rows, stored in a row whose anchor only supports a store. Also the file never shows who calls `rememberFloatingSize`. |
| status `mined` | OK | used-by non-empty and the file exists; entry cites S292 at `corpus/knowledge/hyprland-gkeep-geometry-r43.md:7,44` |
| opened `2026-10-26` | OK | ISO, this round |
| recheck `on-release` | OK | contract allows ISO date or `90d`/`180d`/`on-release`; S028/S290-S294 use it. (Note: the entry header says `recheck: 90d`; both valid, different cadences for the same pin - cosmetic.) |
| used-by | OK | `corpus/knowledge/hyprland-gkeep-geometry-r43.md` exists, header line 7 `source: S292`, OBS at line 44 |
| Gate (lesson:37) | OK | sha256 correct; quote `void ITarget::setPositionGlobal(const STargetBox& box, uint8_t) {` is 6 words, literal on Target.cpp:10, once, not in any other receipt (scripted whole-dir search) |

Exact fix for `teaches` (S292), shorter and inside the anchor:
`A target keeps the box it was handed, with its logical and visual parts rounded, returns the logical part as its position, and holds the last floating size in a member separate from the box`

## S293 (WindowTarget.cpp) - cell verdicts
| cell | verdict | evidence |
|---|---|---|
| id/source | OK | pinned URL; "the client's request as input" is the row's framing |
| kind `code` / tier `A` | OK | upstream source |
| scope | OK | |
| anchor `:36-40` | OK | `CWindowTarget::setPositionGlobal` calls `ITarget::setPositionGlobal(box, flags);` then `updatePos(flags);` |
| anchor `:69-78` | OK (line 69 is the `// Non-FS Floating Windows` comment) | 70 `if (floating() && m_window && !...isFullscreen(...)) {`, 71 `m_window->setBox(m_box.logicalBox);`, 73-74 `sendWindowSize()` when `CONFIGURECLIENT`, 77 `return;` |
| anchor `:297-304` | OK | `clampSizeForDesired`: min `clamp(*m)`, max `clamp(Vector2D{MIN_WINDOW_SIZE,MIN_WINDOW_SIZE}, *m)` |
| anchor `:306-396` | OK | `desiredGeometry()` begins 306, ends `return requested;}` 395-396 |
| anchor tail (bytes/sha/receipt) | OK | 16614 B and sha match |
| teaches | PARTIAL - three imprecisions | The row says: "client's own geometry clamped by min and max size, with a fallback to the live surface size when that box is 2 px or smaller". Source: (a) the trigger is `DESIRED_GEOM.width <= 2 \|\| DESIRED_GEOM.height <= 2` (:339) - either side, not "the box"; (b) the surface fallback fires only if `SURFACE->m_current.size` is > 5 in both axes (:342) and then resets `requested.pos` (:344, "center on mon"); if not, X11 override-redirect windows have a separate fallback (:350-362, 600x400 default) and everything else returns `GEOMETRY_NO_DESIRED`/`INVALID_DESIRED` (:364); (c) a stored size replaces the client's size when the persistent-size rule is on and a float state exists (:323-326). "Client's own geometry" is `g_pXWaylandManager->getGeometryForWindow` (:310), defined in XWaylandManager.cpp (xdg `m_current.geometry` or XWayland geometry) - a file no row pins (I fetched it at the same commit only to read it; not a receipt). |
| status/opened/recheck | OK | as S292 |
| used-by | OK | entry header line 8 `source: S293`; OBS at line 46 cites `Hyprland-WindowTarget.cpp:70-71` |
| Gate (lesson:38) | OK with a note | sha256 correct. Quote `if (floating() && m_window && !Fullscreen::controller()->isFullscreen(m_window.lock())) { m_window->setBox(m_box.logicalBox);` is 8 whitespace words, occurs once in the whitespace-normalised receipt and in no other receipt. It spans source lines 70-71 (newline + 8-space indent collapsed to one space): `grep -cF` on the raw file gives 0. That is the counter's declared rule ("whitespace-normalized quote", `c2-r43-gkeep-entry-v2.py:59-62,335`), so it passes; a reader using a raw per-line grep will not find it. |

Exact fix for `teaches` (S293):
`desiredGeometry() starts from the client's own geometry clamped by its min and max size (a stored size replaces it when the persistent-size rule holds one); when either side of that box is 2 px or smaller it falls back to the committed surface size if both sides exceed 5 px, else to an override-redirect default or to no desired geometry, so the client's request is only the layout's input`
(All clauses grounded at WindowTarget.cpp:310-326, 339-364.)

Optional anchor addition to make the fix grounded: append `, :323-326 stored-size override, :339-364 small-box fallbacks` to the S293 anchor.

## Rule note for the L1
SOURCES contract rule 2: only `status`, `recheck`, `used-by` change in place and a correction is a new row. If the rows are already landed (data commit 1959770), the two `teaches` fixes need a corrective row or a round-44 note, not an in-place edit; the entry text (lines 44, 46) is unaffected because it only claims what the anchors hold.

## Overall
All hard cells (URL, sha256, byte size, tag/commit, anchor line ranges, kind, tier, status, opened, recheck, used-by, Gate line sha256 and quotes) HOLD. Two soft cells are overstated: S292 `teaches` (last clause is a cross-row inference) and S293 `teaches` (omits the `||`, the >5 gate, the error return and the persistent-size override). No row is refuted.

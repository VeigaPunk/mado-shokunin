# Round-77 source fetch record (seat R77ScribeSources)

All candidates fetched/saved 2026-11-04 under this `fetch/` directory.
Byte-identity: every local fetch below re-derived the digest recorded in the committed
wave manifest `.ufo/waves/round-77/fetch/sha256-r77.txt` (`sha256sum -c` → all OK).
Pinned-tree HEADs re-verified: Hyprland `efb50993780079460b0cbed1363e2166a2de1d9f`,
Waybar `90b209add8937514d0a987aa842e701bd8f1232e` — equal to the revision pins the
registry rows carry.

Format: `<anchor> | <=25-word located quote | access`.

## S457 — Hyprland v0.56.2 src/render/Renderer.cpp

- Anchor: `arrangeLayerArray :2587-2670`, `applyExclusive :2529-2585`,
  `arrangeLayersForMonitor :2673-2700` (quote at :2637, inside the arrange range).
- Quote: "box.width = bounds.width - (PSTATE->margin.left + PSTATE->margin.right);"
- Access: pinned read-only tree `/fast/scratch/hyaku/mado-r77/l1-src/Hyprland`
  (HEAD efb5099…), copied byte-identical to `fetch/S457.bin`; sha256
  `9af8a74e7dc42ba3c5532303b9bb4ee7c350d4cef2f2c8984e41f2a01b3bdd22`, 143,211 B.
  Anchor grep re-run on the saved bytes (arrangeLayerArray at 2587, applyExclusive at
  2529, arrangeLayersForMonitor at 2673 — all match).

## S458 — Hyprland v0.56.2 src/debug/HyprCtl.cpp

- Anchor: `layersRequest :647-700`, `reserved` format template `:250-254`,
  reserved print `:281-282`, layers command registration `:2010`.
- Quote: "sc<int>(m->m_reservedArea.left()), sc<int>(m->m_reservedArea.top()),
  sc<int>(m->m_reservedArea.right()), sc<int>(m->m_reservedArea.bottom())"
  (print statement spans :281-282; the four-element form also at :302 in the
  monitors reply builder).
- Access: pinned read-only tree, `fetch/S458.bin`; sha256
  `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa`, 97,582 B.
  Grep re-run: layersRequest at 647, `registerCommand(SHyprCtlCommand{"layers", true,
  layersRequest});` at 2010, reserved template `"reserved": [{}, {}, {}, {}],` at 253.

## S459 — Hyprland v0.56.2 src/desktop/reserved/ReservedArea.cpp (+ .hpp)

- Anchor: `CReservedArea` parent/child constructor `:19-35`, `apply`/`applyip` `:53-60`.
- Quote: "m_initialBottomRight = (parent.pos() + parent.size()) - (child.pos() +
  child.size());" (constructor body, :34).
- Access: pinned read-only tree, `fetch/S459.bin`; sha256
  `0a52e145ed2bdfddfa2b2e658ef2d326a01e86b2266d8af0f015915452a6e0db`, 3,339 B.
  Companion header saved as `fetch/S459.hpp.bin`; sha256
  `6222d11418cae1050b34f07eaddd6f7fc25b4c8d92bf78012ee9e94a1159e99a`, 1,498 B
  (`class CReservedArea` at :14, members at :44). The registry row anchors only the
  .cpp; the .hpp is pinned here as the seat spec asked ("+.hpp") and is not cited by
  any row.

## S460 — protocols/wlr-layer-shell-unstable-v1.xml (Hyprland v0.56.2 tree)

- Anchor: `enum layer :86-90`, request `set_exclusive_zone :152-190`.
- Quote: "A positive zone is the distance from the edge in surface-local coordinates
  to consider exclusive." (description, :165-166).
- Access: pinned read-only tree, `fetch/S460.bin`; sha256
  `87e0b9c837aecd6977f76f3c47d73088b7159871f5d979dc1840f6cadb5e2ed8`, 19,326 B.
  Enum entries background=0/bottom=1/top=2/overlay=3 confirmed at :87-90.

## S461 — installed waybar(5) man page

- Anchor: `BAR CONFIGURATION` keys — `position` (zcat text :91), `layer`, `height`,
  `width`, `margin`, `margin-<side>`, `exclusive`.
- Quote: "Bar position, can be top, bottom, left, right." (roff source line 91 of the
  decompressed page).
- Access: host file `/usr/share/man/man5/waybar.5.gz` (`man -w waybar`), copied
  byte-identical to `fetch/S461.bin`; sha256
  `3972caaf1f025ed83b706cfe91f35d1c9e7c3ae87e5d37d881120d13a1044a42`, 4,963 B.
  A decompressed working copy `fetch/S461.txt` (sha256
  `d59c46512ee42590a6213173cf528eabd47371c5d2409198386fee31d283ddee`) exists for
  quoting only; the byte-identical artifact is the .gz.

## S462 — Waybar v0.15.0 src/bar.cpp

- Anchor: margin precedence `:178-222`, namespace `:232-233`, size request `:240`
  (`window.set_size_request(width_, height_);`), `setMode` exclusive `:355-361`.
- Quote: "if (mode.exclusive) { gtk_layer_auto_exclusive_zone_enable(gtk_window); }"
  (call at :358).
- Access: pinned read-only tree `/fast/scratch/hyaku/mado-r77/l1-src/Waybar`
  (HEAD 90b209a… = tag 0.15.0), `fetch/S462.bin`; sha256
  `120eb913da900b02ec02dbfe5b9c6df2e7bccc99814a020701d8d70cccddadfd`, 23,907 B.

## S463 — candidate reject: wayland.app wlr-layer-shell page

- Anchor: page as served; HTML `<title>wlr layer shell protocol | Wayland Explorer</title>`;
  body heading string "wlr-layer-shell-unstable-v1 protocol".
- Quote: "wlr-layer-shell-unstable-v1 protocol" (page heading; the title element reads
  "wlr layer shell protocol | Wayland Explorer").
- Access: `https://wayland.app/protocols/wlr-layer-shell-unstable-v1` fetched three
  times 2026-11-04, all byte-identical, saved as `fetch/S463.bin`; sha256
  `6a3f6683ec70fff5f0605dd0fb00c36687480123a79cea0986554a4ffd60bef2`, 147,036 B —
  equal to the committed wave copy `.ufo/waves/round-77/fetch/S463.bin` (static page,
  reproducible). REJECTED as a row: renders the protocol text but pins no protocol or
  compositor revision, so it cannot ground a versioned 0.56.2 host claim; the pinned
  XML (S460) is the authoritative copy. Flip: a commit/tag pin for the rendered protocol.

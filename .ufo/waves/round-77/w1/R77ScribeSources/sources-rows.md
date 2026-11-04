# sources-rows.md — seat R77ScribeSources (round 77)

Eleven-column registry rows for S457–S463, drafted for `corpus/SOURCES.md`. Every anchor and
quote below was re-located in this seat's own byte-identical fetches (`fetch/`, digests equal
to `.ufo/waves/round-77/fetch/sha256-r77.txt`; record in `fetch/RECORD.md`). The same seven
rows are already present in the committed registry at the round-77 landing tip
(`3e35d0a9`, HEAD `0fa69f41` at this writing) — this draft is the seat's curated copy and
matches them cell for cell; discrepancies found against OTHER landed files are reported in
`R77ScribeSources.md`, not here.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S457 | Hyprland v0.56.2 — src/render/Renderer.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/render/Renderer.cpp | code | A | mado compositor plane: a layer surface's box and the monitor's reserved area, the arrange rule the bar-footprint join models (round-77 C1) | arrangeLayerArray :2587-2670, applyExclusive :2529-2585, arrangeLayersForMonitor :2673-2700 @ efb5099 (fetched 2026-11-04, sha256 9af8a74e…) | box.width = bounds.width - (PSTATE->margin.left + PSTATE->margin.right); | mined | 2026-11-04 | on-release | corpus/knowledge/bar-footprint-r77.md |
| S458 | Hyprland v0.56.2 — src/debug/HyprCtl.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp | code | A | mado compositor plane: the layers reply shape and the monitors reserved print order the join reads (round-77 C1) | layersRequest :647-700, reserved template :253, reserved print :281-282, command :2010 @ efb5099 (fetched 2026-11-04, sha256 798b7c6c…) | sc<int>(m->m_reservedArea.left()), sc<int>(m->m_reservedArea.top()), sc<int>(m->m_reservedArea.right()), sc<int>(m->m_reservedArea.bottom()) | mined | 2026-11-04 | on-release | corpus/knowledge/bar-footprint-r77.md |
| S459 | Hyprland v0.56.2 — src/desktop/reserved/ReservedArea.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/reserved/ReservedArea.cpp | code | A | mado compositor plane: a parent box and a shrunk child box become the reserved band (round-77 C1) | CBox parent/child constructor :19-35 and apply/applyip :53-60 @ efb5099 (fetched 2026-11-04, sha256 0a52e145…) | m_initialBottomRight = (parent.pos() + parent.size()) - (child.pos() + child.size()); | mined | 2026-11-04 | on-release | corpus/knowledge/bar-footprint-r77.md |
| S460 | wlr-layer-shell-unstable-v1 protocol XML, Hyprland v0.56.2 tree — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/protocols/wlr-layer-shell-unstable-v1.xml | spec | A | mado compositor plane: the layer level and exclusive-zone contract the compositor consumes (round-77 C1) | enum layer :86-90 and request set_exclusive_zone :152-190 @ efb5099 (fetched 2026-11-04, sha256 87e0b9c8…) | A positive zone is the distance from the edge in surface-local coordinates to consider exclusive. | mined | 2026-11-04 | 180d | corpus/knowledge/bar-footprint-r77.md |
| S461 | waybar 0.15.0 manual — waybar(5) — /usr/share/man/man5/waybar.5.gz | docs | A | mado bar plane: the placement keys the footprint join models (round-77 C1) | BAR CONFIGURATION position, layer, height, width, margin, margin-side, exclusive @ waybar 0.15.0 (fetched 2026-11-04, sha256 3972caaf…) | Bar position, can be top, bottom, left, right. | mined | 2026-11-04 | 180d | corpus/knowledge/bar-footprint-r77.md |
| S462 | Waybar v0.15.0 — src/bar.cpp — https://raw.githubusercontent.com/Alexays/Waybar/90b209add8937514d0a987aa842e701bd8f1232e/src/bar.cpp | code | A | mado bar plane: namespace, margins, size request and exclusive zone (round-77 C1) | margin precedence :178-222, namespace :232-233, size request :240, setMode exclusive :355-361 @ 0.15.0 (fetched 2026-11-04, sha256 120eb913…) | if (mode.exclusive) { gtk_layer_auto_exclusive_zone_enable(gtk_window); } | mined | 2026-11-04 | on-release | corpus/knowledge/bar-footprint-r77.md |
| S463 | Wayland Explorer — wlr-layer-shell-unstable-v1 — https://wayland.app/protocols/wlr-layer-shell-unstable-v1 | community | C | a protocol-browser rendering of the layer-shell protocol, rejected for version pinning (round-77) | page as served 2026-11-04 (sha256 6a3f6683…, 147036 B) | REJECTED: the page renders the protocol text but pins no protocol or compositor revision, so it cannot ground a versioned 0.56.2 host claim; the pinned XML (S460) is the authoritative copy | rejected | 2026-11-04 | 180d | — |

## Verification notes (this seat's evidence)

- S457: quote located at :2637 (inside the arrange range); function starts at 2587/2529/2673.
- S458: layersRequest at :647; reserved format template `"reserved": [{}, {}, {}, {}],` at :253;
  reserved print spans :281-282 (four-element form also at :302); `registerCommand(
  SHyprCtlCommand{"layers", true, layersRequest});` at :2010.
- S459: quote at :34; `apply()` body at :53-60. Companion header pinned as `fetch/S459.hpp.bin`
  (class at :14); no row cites it.
- S460: enum entries at :87-90; quote at :165-166 of the request description.
- S461: quote at line 91 of the decompressed page (`zcat` working copy `fetch/S461.txt`; the
  byte-identical artifact is the .gz).
- S462: margins :235-238, namespace :232-233, size request `window.set_size_request(width_,
  height_);` at :240, quote at :358 inside `setMode` (:346-361).
- S463: fetched three times, byte-identical, digest equal to the committed wave copy.
  Verbatim page title: `wlr layer shell protocol | Wayland Explorer`; the string
  `wlr-layer-shell-unstable-v1 protocol` does not occur in the page bytes (see the report's
  Finding B).

## Census command and expected W04 notes

Command (run by this seat at HEAD `0fa69f41`, receipt `receipts/census-scribe-r77.txt`):

    TZ=UTC bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
        /home/vgpnk/Projects/shokunin/mado-shokunin

Observed: exit 0, `ok` for `corpus/SOURCES.md`. Expected and confirmed W04 notes:

- `W04 S458 duplicate url …/efb5099…/src/debug/HyprCtl.cpp across scopes` — the one new
  warning this round; S458 shares its exact URL with held rows S158, S307, S320, S366, S389,
  S394 (each a separate scope at the same pinned revision), the documented, non-failing
  duplicate-URL class the LOG round-77 entry names.
- Carried W04s for earlier duplicate URLs (S030/S045, S443/S455, S447/S451/S453/S456, …)
  unchanged — none names S457, S459, S460, S461, S462 or S463, so the six mined rows bring
  no other census warnings (S461 is a host-file row with a unique path; S463 is rejected and
  its URL is not held elsewhere in the registry).
- Round start (freeze rev, committed `receipts/pre-wave-evidence-r77.txt`): exit 0 with the
  carried S456 warning only; the S458 warning appears with the round's own rows.

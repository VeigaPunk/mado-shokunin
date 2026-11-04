# mado round 77 — lesson (scribe-seat draft, R77ScribeSources)

Claims: **C1 coverage** — the bar-footprint chain (declared waybar config → live layer box →
monitor `reserved` band) becomes a measured join; **C2 operability** — the SKILL.md
read-only probe table executes end-to-end. Freeze `a83e9bee`; base `aeeef067`; declaration
`.ufo/waves/round-77/claims-declaration-r77.md`; wave w1, 12 seats.

This is the sources-&-lesson seat's draft. A lesson file already landed at
`corpus/lessons/round-77.md` (M77-1…M77-5, mined by the L1 and the wave). The blocks below
are written to stand alone: the L1 may merge the Gate table as-is, append the scribe-mined
mistake rows as a wave-findings block, and apply the two corrections named under
## Corrections. Nothing here rewrites a committed byte.

## Mistakes (scribe-mined; landed M77-1…M77-5 remain the round's own record)

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| MS-1 (r76 D-series, D7) | provenance pointer: the round-76 report cited `2308e12a` as the commit carrying the census receipts; `git show --name-status 2308e12a` shows that commit adds only `.ufo/waves/round-76/receipts/harm-watch-r76.txt` (`M`); the census end and the final C2 measurement landed at `e160d18e` (`A census-end-r76.txt`, `A measurement-c2-r76-final.txt`, plus the harm-watch receipt and LOG/SCORECARD/entry changes) | `git show --name-status 2308e12a` vs `git show --name-status e160d18e` (both re-run read-only by this seat 2026-11-04; outputs in the seat report) | the round-76 verifier spot-check (non-author closure), dispositioned as D7/D8 with the D2 correction | the correction block names both commits plus the `git diff --name-status` re-derivation command; the fix fails loudly if re-run and the diff no longer shows exactly those files. This seat verified both sides of the red/green pair itself. |
| MS-2 (this round, seat's own) | sequencing race in a parallel batch: the S463 fetch was fired before the seat's `fetch/` directory existed; the `cd` failed (`…/fetch: No such file or directory`), the script continued in the inherited cwd and wrote `S463.fetch{1,2,3}` into the fleet root — outside every allowed write path | the seat job log (`cd` error, three 147036-byte files written to `/home/vgpnk/Projects/shokunin/`); the seat removed the strays and re-fetched into `fetch/` (digest unchanged) | the seat's own job output, not any reviewer | `mkdir -p` + `set -e` in the same job that writes (or sequencing the dependency); re-running without the mkdir reproduces the stray fleet-root files, re-running with it lands all three in `fetch/` — this seat's later S463 copy is the green. Lesson: "parallelize independent calls" never overrides a file-system dependency between them. |
| MS-3 (this round, seat's own) | locator assumption: the first read targeted `/mado-shokunin/SOURCES.md` (lane root) and found nothing; the registry lives at `corpus/SOURCES.md` | the not-found read versus the glob result (`corpus/SOURCES.md`, plus three unrelated fixture copies) | the seat's own first probe | resolve the path by glob before reading; the fix fails if the glob root is wrong (e.g. `**/SOURCES.md` under the fleet root matches fixture copies first), so the draft names the exact canonical file. |

A sixth sweep, as the landed lesson does: `grep -n 'TODO\|FIXME\|XXX'` over the three
round-77 instruments → no output (re-run by this seat on the HEAD bytes).

## Gate (sources opened this round; 6 admits, 1 reject)

All seven candidates were opened 2026-11-04 before their rows were written. Fetches are
byte-identical to the committed wave manifest (`fetch/RECORD.md` in this seat's dir gives
`<anchor> | ≤25-word located quote | access` per source; S463 fetched three times,
byte-identical, digest equal to the committed copy).

- **Admitted, S457** — Hyprland v0.56.2 `src/render/Renderer.cpp` @ efb5099.
  URL: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/render/Renderer.cpp`
  (accessed 2026-11-04 via the pinned read-only tree; sha256 `9af8a74e…`). Anchors
  `arrangeLayerArray :2587-2670`, `applyExclusive :2529-2585`, `arrangeLayersForMonitor :2673-2700`.
  Quote (11 words): "box.width = bounds.width - (PSTATE->margin.left + PSTATE->margin.right);"
  Licenses the box/anchor/margin arrange rule the join models; not a license for margined
  auto-zone composition.

- **Admitted, S458** — Hyprland v0.56.2 `src/debug/HyprCtl.cpp` @ efb5099.
  URL: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp`
  (sha256 `798b7c6c…`). Anchors `layersRequest :647-700`, reserved template `:253`, print
  `:281-282`, command `:2010`. Quote (18 words): "sc<int>(m->m_reservedArea.left()),
  sc<int>(m->m_reservedArea.top()), sc<int>(m->m_reservedArea.right()),
  sc<int>(m->m_reservedArea.bottom())". Licenses the reply shape and the reserved print
  order; not which surface set the zone. Raises the documented W04 duplicate-URL warning
  (same URL as S158/S307/S320/S366/S389/S394 at separate scopes).

- **Admitted, S459** — Hyprland v0.56.2 `src/desktop/reserved/ReservedArea.cpp` @ efb5099.
  URL: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/reserved/ReservedArea.cpp`
  (sha256 `0a52e145…`). Anchors constructor `:19-35`, `apply`/`applyip` `:53-60`.
  Quote (12 words): "m_initialBottomRight = (parent.pos() + parent.size()) - (child.pos() +
  child.size());". Licenses the parent/child reserved band; not per-consumer attribution.
  The companion header was pinned (`S459.hpp.bin`, sha256 `6222d114…`) and is uncited.

- **Admitted, S460** — `wlr-layer-shell-unstable-v1.xml`, Hyprland v0.56.2 tree @ efb5099.
  URL: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/protocols/wlr-layer-shell-unstable-v1.xml`
  (sha256 `87e0b9c8…`). Anchors enum `layer :86-90`, request `set_exclusive_zone :152-190`.
  Quote (17 words): "A positive zone is the distance from the edge in surface-local
  coordinates to consider exclusive." Licenses levels and the exclusive-zone contract; a
  contract, not host behaviour.

- **Admitted, S461** — installed `waybar(5)` 0.15.0, `/usr/share/man/man5/waybar.5.gz`
  (host file; sha256 `3972caaf…`). Anchor `BAR CONFIGURATION` keys position/layer/height/
  width/margin/margin-&lt;side&gt;/exclusive (decompressed page line 91 for `position`).
  Quote (9 words): "Bar position, can be top, bottom, left, right." Licenses the declared
  placement keys and defaults; not what the compositor does with them.

- **Admitted, S462** — Waybar v0.15.0 `src/bar.cpp` @ `90b209ad…`.
  URL: `https://raw.githubusercontent.com/Alexays/Waybar/90b209add8937514d0a987aa842e701bd8f1232e/src/bar.cpp`
  (sha256 `120eb913…`). Anchors margin precedence `:178-222`, namespace `:232-233`, size
  request `:240`, `setMode` exclusive `:355-361`. Quote (11 words): "if (mode.exclusive) {
  gtk_layer_auto_exclusive_zone_enable(gtk_window); }". Licenses margin precedence,
  namespace, size request and the exclusive call; not gtk-layer-shell's internal zone
  arithmetic.

- **Rejected, S463** — Wayland Explorer, `https://wayland.app/protocols/wlr-layer-shell-unstable-v1`
  (accessed 2026-11-04, three fetches byte-identical, sha256 `6a3f6683…`, 147036 B).
  Quote (7 words, verbatim from the page's title element): "wlr layer shell protocol |
  Wayland Explorer". REJECTED: the page renders the protocol text but pins no protocol or
  compositor revision, so it cannot ground a versioned 0.56.2 host claim; the pinned XML
  (S460) is the authoritative copy. Flip: a commit/tag pin for the rendered protocol.

Registry arithmetic: 393 → 400 rows (six mined, one rejected-kept). No held cell changed;
the only new census warning is the documented S458 W04.

## Corrections (for the L1, append-only)

1. **Landed lesson, Gate table, S463 row**: the quote cell reads
   `wlr-layer-shell-unstable-v1 protocol` with the note "(page title)". The string does not
   occur in the page bytes (`grep -o` empty; `grep -c 'wlr-layer-shell-unstable-v1'` = 1 in
   an unrelated context); the actual title element is "wlr layer shell protocol | Wayland
   Explorer" and the h1 is "wlr layer shell". Suggested correction: replace the quote with
   the verbatim title string above. Class: quote-not-located (the Gate standard requires a
   located quote); the fix can fail by reverting to the unlocated string on the next reject
   row.
2. **Landed SCORECARD round-77 block, C1 row**: "at `a83e9bee` (its instrument's last
   change)" went stale when the wave-found hardening landed: `git log -1 --format=%H --
   tools/mado-barfoot.py` prints `0fa69f41d81275db102bbe08cf5d6a86a5dfe8f7` (the tool bytes
   and the entry changed; repair receipt `.ufo/waves/round-77/receipts/repair-r77-tool-refusals.txt`).
   This is the same class as M77-3/r76-D2 recurring in-round. Suggested correction: re-measure
   at the hardened tip (this seat's run: `receipts/measure-c1-scribe-at-0fa69f41.txt`) and
   append the new instrument-last-change pointer; `quality/check-cited-revisions.py` (repair
   pack) is the standing check that can fail on this class.

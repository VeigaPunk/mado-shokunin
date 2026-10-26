# RevEntryWhole — w2 whole-entry review of `corpus/knowledge/hyprland-gkeep-size-request-r44.md` against `corpus/QUALITY.md`

Seat RevEntryWhole, mado round 44 w2, 2026-10-26. Scope: the whole entry vs the QUALITY bar — OBS/INF/UNK honesty, overclaim,
recheck sense, "does not establish" completeness, sibling-domain bleed (PROVINCE.md). Leaf; no subagents; no tools installed;
scratch `/fast/scratch/hyaku/mado-r44/RevEntryWhole/` created empty, removed before this report was finalized. No counter or
control was run (other seats' item); this seat reviewed content.

## Method (all locators below computed this session, not typed)

- Pin integrity: `sha256sum` over the five `fetch/` pins equals `receipts/fetch-sha256.txt` line for line (S164 `d735d454…`,
  S298 `d90b534c…`, S299 `7ba7f9c8…`, S300 `0ee38458…`, S301 `07a3c4a5…`). All quotes and locators below were checked against
  those verified bytes.
- Locator sweep: `python3 -I quality/check-locators.py --fetch .ufo/waves/round-44/fetch
  corpus/knowledge/hyprland-gkeep-size-request-r44.md` → `CHECK_LOCATORS: locators=29 miss=8`, exit 1 (see Instrument note).
- Cross-reads: `.ufo/waves/round-44/registration-v2.md`, `corpus/lessons/round-44.md` (`## Gate`, assimilation ledger, census
  section), `corpus/knowledge/hyprland-gkeep-geometry-r43.md`, `PROVINCE.md`, `corpus/SOURCES.md` rows S164/S298-S301, receipts
  `live-geometry-host-r44.txt` and `.ufo/waves/round-43/receipts/live-geometry-host.txt` (present at base `6a1a905` and HEAD).
- The entry's three "what the pins correct" claims were re-derived from the pins directly, not taken from
  w1/ScoutStagedResidue or w1/CritAssimilation.

## Findings

### F1 — MEDIUM — §1's transport summary is over-general and hides the map-time 0x0 configure the pins carry

- Attacks: entry `:28`, last sentence of the first **OBS** paragraph: "so the size sent to a floating gkeep window is the box
  the floating algorithm set".
- Evidence: the same pinned file carries a second send path the entry never mentions. `commitWindow`'s initial-commit branch
  computes `predSize` (`fetch/Hyprland-Window.cpp:2722-2728`): for a floating window (`static_.floating` true) the guarding
  conjunction is false, so `predSize = Vector2D{}`, and `m_xdgSurface->m_toplevel->setSize(predSize);`
  (`fetch/Hyprland-Window.cpp:2732`) sends an xdg configure of 0x0 — not the rule box. The rule box travels later through the
  `sendWindowSize` path the entry does describe (`:1732-1753`). The entry's own §4 supplies the 0x0 semantics ("client decides",
  `fetch/gdktoplevel-wayland.c:647-650`), so the omission is internal as well as external. Secondary tag defect: the sentence is
  an inference (GOAL source + sendWindowSize wiring + round-43's rule-to-GOAL result), stated inside a paragraph tagged **OBS**
  (QUALITY criterion 43).
- Corrected sentence (L1 decides): "Round 43 traced the rule's size into that GOAL (corpus/knowledge/hyprland-gkeep-geometry-r43.md),
  so the box-setting configure a floating gkeep window is sent afterwards carries the box the floating algorithm set; the
  map-time initial commit instead sends a 0x0 configure for a floating window (Hyprland-Window.cpp:2722-2732), which GTK 4.24.1
  reads as the client deciding its own size (§4) — **INF** for the join, on the same pins."
- Reproduction: `grep -n 'predSize\|setSize(predSize)' .ufo/waves/round-44/fetch/Hyprland-Window.cpp` → 2722, 2730, 2732;
  the ternary's floating guard is the `!m_ruleApplicator->static_.floating.value_or(false)` term at `:2722`.

### F2 — LOW — the S301 locator range excludes the line the default-size fact sits on

- Attacks: entry `:56` — "`window.set_decorated(False) window.set_default_size(420, 500)` (gkeep-ui.py:475)".
- Evidence: in the pinned bytes `window.set_decorated(False)` is at `fetch/gkeep-ui.py:475` and
  `window.set_default_size(420, 500)` at `:476` — the cited single-line range 475 does not contain the second fact (QUALITY
  criterion 77: the cited range must carry the fact's own identifier). The lane's own Gate note states the quote "spans 475-476"
  (`corpus/lessons/round-44.md`, `## Gate`, "Locators the entry carries" paragraph), and SOURCES S301 cites `gkeep-ui.py:474-476`
  correctly; only the entry's locator is truncated.
- Corrected text: change `(gkeep-ui.py:475)` to `(gkeep-ui.py:475-476)` on entry line 56.
- Reproduction: `grep -n 'set_decorated\|set_default_size' .ufo/waves/round-44/fetch/gkeep-ui.py` → 475, 476.

### F3 — LOW — the UNK row's justification asserts a round-long absence that its receipts do not cover, without anchors

- Attacks: entry `:24`, table row "Has a gkeep window been seen acknowledging 420x500 on this host? | no gkeep window open in
  round 43 or round 44 | UNK".
- Evidence: the supporting reads exist but are point-in-time dumps, and neither is cited: round 43's census
  (`.ufo/waves/round-43/receipts/live-geometry-host.txt`, cited by the r43 entry at its §5) and round 44's
  (`.ufo/waves/round-44/receipts/live-geometry-host-r44.txt`: `MADO_GEOMETRY: … matched=0 … verdict=NO_MATCHING_CLIENT`,
  `exit=3`, clients Alacritty/zcode/grok-bot). "No gkeep window open in round 43 or round 44" states more than two dumps show
  (QUALITY criteria 2 and 42; the r43 entry's own phrasing is the careful one: "No gkeep window was open when the dump was
  taken").
- Corrected text (row cell): "the two live censuses saw none: the round-43 dump (.ufo/waves/round-43/receipts/live-geometry-host.txt)
  and the round-44 dump (.ufo/waves/round-44/receipts/live-geometry-host-r44.txt, NO_MATCHING_CLIENT)".
- Reproduction: `grep -n 'NO_MATCHING_CLIENT' .ufo/waves/round-44/receipts/live-geometry-host-r44.txt`.

### F4 — LOW — "gkeep is a GTK 4 Wayland client" is asserted unanchored in the does-not-establish list

- Attacks: entry `:80`, bullet "- The X11 path beyond its existence: gkeep is a GTK 4 Wayland client."
- Evidence: no pin observes gkeep running (rounds 43-44 saw no gkeep window; S301 is source text). GTK 4's Wayland-default
  backend selection is not pinned anywhere in the entry's five sources, so the sentence states a host-behavior fact the entry's
  own UNK row (`:24`) says is unobserved — the same criterion-15 class (do not substitute a layer default for host behavior).
- Corrected text: "- The X11 path beyond its existence: gkeep is a GTK 4 application (gkeep-ui.py:474); that it runs as a
  Wayland client on this session is the GTK 4 default and has not been measured — no gkeep window has been observed (UNK row
  above)."
- Reproduction: absence check this seat ran: `grep -rn 'gkeep' .ufo/waves/round-44/receipts/live-geometry-host-r44.txt` → no
  match; the five pins contain no backend-selection statement (`grep -c 'GDK_BACKEND' .ufo/waves/round-44/fetch/gkeep-ui.py` → 0).

### F5 — LOW — the ack-bridge sentence carries no locator although both ends are in the pins

- Attacks: entry `:44`, closing clause "that ack is what Hyprland's onAck receives".
- Evidence: true in the pinned bytes — the protocol request at `fetch/xdg-shell.xml:560`, Hyprland's handler registration
  `m_resource->setAckConfigure(...)` at `fetch/Hyprland-XDGShell.cpp:601` emitting `m_events.ack.emit(serial);` at `:605`, and
  the listener wiring `onAck(d)` at `fetch/Hyprland-Window.cpp:184` into `onAck` at `:1514` — but the sentence cites none of
  them (QUALITY criterion 2).
- Corrected text: append "(Hyprland-Window.cpp:184, Hyprland-XDGShell.cpp:601-605)" to the sentence.
- Reproduction: `grep -n 'm_events.ack.emit' .ufo/waves/round-44/fetch/Hyprland-XDGShell.cpp` → 605; `grep -n 'onAck(d)'
  .ufo/waves/round-44/fetch/Hyprland-Window.cpp` → 184.

## Instrument note (recorded, not a finding against the entry except F2)

`CHECK_LOCATORS: locators=29 miss=8`, exit 1. Seven of the eight MISS rows are instrument granularity, not entry errors: the
checker tests each line's backticked fragments against each locator's single range, so cross-line quote joins (the S299 hint
quote spans `fetch/xdg-shell.xml:1150-1151`, cited at `:1150` — the same joined string the Gate pins) and a fragment belonging
to a different locator on the same line (`Hyprland-XDGShell.cpp:354-358` sharing line 36 with the `:455` quote) read MISS. The
eighth row, `gkeep-ui.py:475` on entry line 56, is F2. This is the already-recorded limitation class of the instrument (lesson
M44-6: "compares identifiers not numbers"); no open predicate defect is claimed — the locator rule itself (criterion 77) is what
F2 violates.

## Passes (checked, no defect)

- Tag honesty otherwise: §2's INF and UNK, §4's INF+UNK, §5's INF and UNK, and the table's OBS/INF/UNK cells all match the pin
  evidence; every code reading in §1-§5 was re-derived against the verified pins and is accurate (`:1687`, `:1685-1699`,
  `:1732`, `:1743-1744`, `:1751`, `:1753`, `:1514`, `:1526`; XDGShell `:354-358`, `:455`; xdg-shell.xml `:560`, `:1144`,
  `:1150`, `:1154-1157`, `:1159-1161`; GTK `:490-494`, `:518-521`, `:523-528`, `:633-637`, `:647`, `:681`, `:539-544`; gkeep
  `:449`, `:87-88`). The predecessor-correction claims verify: no `set_size` request exists in the xdg_toplevel interface (the
  only `name="set_size"` in the pin is xdg_positioner's, `fetch/xdg-shell.xml:157`); `onAck` writes the compositor's stored size
  (`fetch/Hyprland-Window.cpp:1526`); GTK constrains before adopting (`fetch/gdktoplevel-wayland.c:523-528`).
- Census lines recomputed from the pins and correct: gkeep `default_size=420x500` (`:476`), `size_request_calls=0` (no
  `set_size_request` anywhere in the pin), `application_id=org.omarchy.gkeep` (`:449`); `xdg_setSize=1 x11_configure=1` in the
  `sendWindowSize` body (`:1751`, `:1753`).
- recheck `:9` is sensible: 90d, five re-pullable commit/tag-pinned URLs whose sha256 are carried in SOURCES S164/S298-S301,
  and host-package/gkeep-commit triggers; "re-run the counter" follows the r43 entry's established wording.
- "What this entry does not establish" is complete except F1 (the 0x0 initial configure) and F4 (client type): rendered size,
  buffer-mismatch behavior, X11 path, and version scope are all covered.
- Sibling-domain bleed: none. The entry stays inside PROVINCE.md's "display behavior on this host"; the GTK/gkeep reads are the
  host client's own code at the host's package versions (gtk4 1:4.24.1-1), the assimilation ledger scopes the package "in
  (upstream code at the host's commit, the app's own source)", and nothing is absorbed from tsukuroi (package state), mori
  (transcripts), kagi (secrets) or tameshi (mutation method). Versions/eras are labeled per criterion 15.

## Residual risk and verification gaps

- This seat did not execute `quality/counters/c2-r44-gkeep-size-request-v2.py` or the controls (the data-falsify seats' item);
  F1-F5 are content findings against the landed text, independent of the counter's verdict.
- F1 rests on static reading of the pinned code (floating window ⇒ `predSize` empty); no live or nested-compositor run was made
  (host-service and Wayland-client connections are barred this round). The r43 isolated-oracle observation is consistent with it.
- GTK/gkeep behavior is source-read only, matching the entry's own declared UNKs; no GTK execution was attempted.
- The `gkeep-ui.py:475-476` span in the Gate note means the counter's clause-j anchor for S301 is computed from the quote's
  start line; whether the counter's own anchor check would also flag the entry's truncated locator was not tested here.

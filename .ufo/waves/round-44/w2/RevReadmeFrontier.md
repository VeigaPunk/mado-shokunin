# w2/RevReadmeFrontier — README index row + Round-44 Frontier section

Scope: corpus/README.md row for `knowledge/hyprland-gkeep-size-request-r44.md` (MADO-R44-1) and the "Round-44 gkeep
size-request route" Frontier section, every claim and locator, at data commit e46789213830597348fe96a351ae004d10587385.
README.md, SOURCES.md and the entry are byte-identical between e4678921 and tip 290cddea (git diff --stat empty), so all
locators below hold at the tip too. All line numbers computed by `grep -n` (or numbered reads) against the exact pinned
bytes copied from `.ufo/waves/round-44/fetch/`; receipts are in this seat dir: `pin-verify.txt`,
`check-index-rows-r44.txt`, `check-index-rows-selftest.txt`.

## Checks run

- Pin digests: all 8 lines of `receipts/fetch-sha256.txt` re-hashed against the landed bytes — 8/8 OK (`pin-verify.txt`).
- `quality/check-index-rows.py --repo . --rev e46789213830597348fe96a351ae004d10587385`: exit 0, `rows=61 errors=0
  warns=3`; the 3 warns are pre-existing r12/r24 glob warns in rows this round does not touch
  (`check-index-rows-r44.txt`). `--selftest`: 10/10, exit 0 (`check-index-rows-selftest.txt`). (The registration's
  published operability number quotes `check-index.py --selftest` 12/12 — a different tool, not run here.)
- Live receipt honesty: sha256 of `tools/mado-geometry.py` at e4678921 = `1da3ddaed0d6e3cca32d3724daeb4a7fbd14939946ad57ab8db34bc0b2e31ff4`,
  equal to the header of `receipts/live-geometry-host-r44.txt`.
- Every pin locator in the row and the section re-derived from the pinned bytes (details below).

## Findings

### M1 — Frontier misstates the NOT_COMPARED trigger — corpus/README.md:317

Attacks: :317 "a NOT_COMPARED top verdict (exit 5) when such clients are the only ones and none agreed".

Evidence: the tool shipped in the same commit decides `NOT_COMPARED` at `tools/mado-geometry.py:271-272` whenever
`agree == 0 and maximized + fullscreen > 0` — no "only ones" condition — and its docstring says the same
(`tool-e467.py`-equivalent source, docstring "NOT_COMPARED (exit 5, agree=0 and maximized + fullscreen > 0)"). The
tool's own selftest `state-with-tiled-not-compared` runs a fullscreen-2 client plus a TILED client and asserts
`verdict=NOT_COMPARED`, exit 5 — a dump where state clients are *not* the only matched clients. And when any matched
client differs, the top verdict is DIFFER exit 1 (selftest `fullscreen-with-differ`). The landed SKILL row states it
correctly: SKILL.md:282 "at least one matched client was skipped for its state and none agreed". The Frontier clause is
therefore too narrow: a reader auditing a mixed {state, tiled} dump would expect OK/DIFFER and gets NOT_COMPARED.

Correction (sentence spans corpus/README.md:315-319; clause on :317): replace
"a NOT_COMPARED top verdict (exit 5) when such clients are the only ones and none agreed, and TILED is narrowed"
with
"a NOT_COMPARED top verdict (exit 5) when no matched client agreed or differed and at least one was skipped for its state, and TILED is narrowed".

### M2 — Row's ack locator points at the wrong xdg-shell line — corpus/README.md:72

Attacks: :72 fragment "(`xdg-shell.xml:1144-1165`, ack at `:1163`)".

Evidence: pinned `fetch/xdg-shell.xml:1163` reads "The states are sent as an array of 32-bit unsigned integers in"
(states encoding, nothing about ack). The ack obligation is at `xdg-shell.xml:1166` "Clients must send an
ack_configure in response to this event." (continuing :1167), so the row's enclosing range 1144-1165 also stops one
line short of it. The entry (§3) and the Frontier (README:311-312) correctly cite the `xdg_surface.ack_configure`
request at `xdg-shell.xml:560`; only the row's "ack at `:1163`" is wrong.

Correction: replace "that a client need only acknowledge (`xdg-shell.xml:1144-1165`, ack at `:1163`)" with
"that a client need only acknowledge (`xdg-shell.xml:1144-1167`, ack at `:1166`)".

### L1 — Queue-site locator missing; row and frontier cite different onAck subranges — corpus/README.md:72 and :310

Attacks: :72 "queues the configure serial on its pending-size-ack list, cleared by `onAck`
(`Hyprland-Window.cpp:1514-1521`)" and :310 "queueing the serial for `onAck` (`Hyprland-Window.cpp:1514-1526`)".

Evidence: the queueing is `Hyprland-Window.cpp:1753` (`m_pendingSizeAcks.emplace_back(...)`); `onAck` spans
:1514-1529, with the clearing `std::erase_if` at :1521 and the acked-size write at :1526. Both cited subranges cover
the clear (so neither is false), but neither citation names the queueing site the sentence's first verb describes, and
row (:1514-1521) and frontier (:1514-1526) disagree on the subrange of the same function. The entry §1 cites :1753
correctly.

Correction: row → "...and queues the configure serial on its pending-size-ack list (`Hyprland-Window.cpp:1753`),
cleared by `onAck` (`Hyprland-Window.cpp:1514-1526`)"; frontier → "...queueing the serial for `onAck`
(`Hyprland-Window.cpp:1753`, handler `Hyprland-Window.cpp:1514-1526`)".

### L2 — "no socket was opened" is contradicted by the round's own receipt — corpus/README.md:72

Attacks: row fragment "No client was run and no socket was opened".

Evidence: `receipts/live-geometry-host-r44.txt:2` records the round's live census as
`$ hyprctl clients -j | python3 -I tools/mado-geometry.py ...` — a connection to the compositor's request socket,
which this corpus itself names "the request socket" (rows r37/r38). The intended meaning (no client-side Wayland
connection, so the ack round-trip is unobserved) is true, but the absolute wording is false against the landed
evidence in the same commit.

Correction: replace with "No client was run and no client-side Wayland connection was opened; the ack round-trip and
the drawn size stay UNK."

## Verified correct (no defect)

- Row, chain locators: `Hyprland-Window.cpp:1732` (sendWindowSize def) and `:1741` (`REPORTSIZE = realToReportSize()`);
  `Hyprland-XDGShell.cpp:354-357` (setSize: store, scheduleStateApplication, `return m_owner->scheduleConfigure();`)
  and `:629-643` (CXDGSurfaceResource::scheduleConfigure + configure → sendConfigure(serial)); X11 configure
  `Hyprland-Window.cpp:1751`; `realToReportSize` range 1685-1699; deferred send `Hyprland-XDGShell.cpp:455`.
- Row, GTK: "applies the configured size through `gdk_wayland_toplevel_update_size`" — function exists
  (`gdktoplevel-wayland.c:382`), called at :530 inside the cited :513-536 branch (margins at :518-521, constrain by
  geometry hints at :524-528); frontier's ":518-528,681" checks out (:681 `next_layout.configured_width = width`).
- Row, gkeep: `gkeep-ui.py:449` `application_id="org.omarchy.gkeep"`, `:476` `window.set_default_size(420, 500)`
  (the row's :476 is exact; note the entry §5 cites :475 for both statements — 475 is `set_decorated` — entry-side
  off-by-one for the set_default_size half, flagging for the entry's seat); zero `set_size_request` occurrences in the
  pinned file (grep), matching the census line `size_request_calls=0`; the only min-width/min-height are :87-88.
- Row, protocol: "a hint to the window" is a verbatim quote of `xdg-shell.xml:1150`; frontier's `:1150` and `:560`
  exact; "xdg-shell 1.49", "GTK 4.24.1", "gkeep 133b867" all match the pin URLs/versions.
- Frontier: "the client's acknowledgement path" is the round-43 section's own open item verbatim (README:302 vs :306);
  FULLSCREEN/MAXIMIZED for `fullscreen` field 2/1 and the ignoring of bool/float/string values match the tool
  (docstring + selftests `fullscreen-bool-ignored`, `fsmode-values`); TILED verdict is `not floating` (code :242-243);
  the pseudo parenthetical is true (pseudo size stored at `Hyprland-Window.cpp:2394-2414`; no pseudo field in the
  HyprCtl clients dump); "rows S164 plus S298-S301" equals the entry's exact source set; "no live gkeep window was
  observed" matches the live receipt (3 clients: Alacritty, zcode, grok-bot; `NO_MATCHING_CLIENT`).
- Row Sources cell `S164, S298, S299, S300, S301`: all defined; S164's used-by extended with this entry
  (SOURCES.md:176); S298-S301 receipt digests match `fetch-sha256.txt`.

## Observations (no action forced)

- "TILED is narrowed to 'not floating'" (README:317-318): the round-43 tool's code already had `TILED (not floating)`
  (base 6a1a905 docstring verdict list; verdict assignment unchanged); what the round narrows is the published claim
  (SKILL.md:288-291 D3 correction, tool docstring's new pseudo caveat), not the code condition. Defensible as
  documentary narrowing; noted so it is not read as a behavior change.
- Out of my seat, for the SKILL seat / L1: SKILL.md:293-294 says the round-44 host dump "holds four tiled clients",
  but the only landed live receipt shows `clients=3` and lists exactly three clients, none matching. 3 ≠ 4 unless a
  fourth (unmapped) client existed in that dump, which the receipt does not show.
- Lineage note: S297 stays held with used-by = the r43 entry only (SOURCES.md:246), while the row's id cell calls the
  new entry "successor path to the held excerpt S297". Not false — S301's verification cell covers the excerpt's
  ground and S297's recheck was renewed this round — the lineage lives only in the README id cell because the entry
  cites S301, not S297.

## Residual risk and verification gaps

- I did not re-run the C2 counter or re-derive clause j's anchors (other seats' scope); my checks are independent
  greps against the pins, not a counter replay.
- GTK claims were verified at the cited ranges and their enclosing functions (layout branch, handle_configure);
  behavior beyond those ranges (e.g. gtk_surface interactions) was not audited.
- S297's excerpt-internal line map (:6, :33 vs full-file :449/:476) was not re-derived — round-43 held row, outside
  this seat.
- Tooling record: nothing installed (system python3, git, sha256sum, coreutils only); pacman untouched; no
  compositor writes; all work under /fast/scratch/hyaku/mado-r44/RevReadmeFrontier (deleted at seat completion),
  receipts copied here first.

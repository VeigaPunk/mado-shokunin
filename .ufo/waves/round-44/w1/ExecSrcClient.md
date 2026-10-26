# ExecSrcClient — w1, round 44 (C2 client-side located-quote fact table)

Status: DONE. Deliverable: `.ufo/waves/round-44/w1/ExecSrcClient/facts.md` (214 lines, generated),
receipts `verify.log` + `verify_facts.py` in the same directory.

## Files written (all inside the lane, all inside my seat dir)

| path | what |
|---|---|
| `.ufo/waves/round-44/w1/ExecSrcClient/facts.md` | the fact table: 42 located-quote rows + 11 parser-read structure facts + exact/maximum/hint summary + 10 non-establishment items |
| `.ufo/waves/round-44/w1/ExecSrcClient/verify_facts.py` | generator + verifier; regenerates facts.md byte-for-byte and exits 1 on any failed row |
| `.ufo/waves/round-44/w1/ExecSrcClient/verify.log` | raw output of the last run |

No tracked file was touched (`git status --porcelain` shows only the wave's own untracked dirs),
no counter/control/registration/pin was edited, no scratch tree survives
(`/fast/scratch/hyaku/mado-r44/ExecSrcClient` removed), no package installed, no host/compositor
command beyond reads.

## Behaviour delivered

`facts.md` answers, with a verbatim quote + computed `file:line` + receipt sha256 for each:

* **xdg-shell 1.49 (11 rows A1-A11)** — configure width/height is a *hint* (A1); `0` in either
  dimension means the client decides (A2); the size's force comes from the states array (A3), which
  makes `maximized` **exact** (A4), `fullscreen` a **maximum** (A5), `resizing` a **maximum** (A6),
  and the four `tiled_*` states **carry no size semantics at all** (A7); every configure must be
  acked before the responding commit (A8) but only the last of a burst needs acking (A9);
  `configure_bounds` is v4+ and advisory (A10); client min size is explicitly ignorable (A11).
* **GTK 4.24.1 `gdktoplevel-wayland.c` (20 rows B1-B20)** — `xdg_toplevel_configure` only stores
  `pending.width/height` (B1); `handle_configure` consumes it (B2) and reads `0x0` as "no size
  given" (B3), restoring the saved size only when *leaving* a fixed state (B4); `fixed_size` is
  `MAXIMIZED|FULLSCREEN|TILED` or `resizing`, so a plain floating configure is **not** fixed (B5);
  a non-zero size is latched (B6) and marked fixed only per B5 (B7); a fresh non-zero configure
  requests constraint (B8); `compute_size` prefers the latched compositor size (B9), clamps it
  through `gdk_surface_constrain_size` (B10), then **clears** it when not fixed — a one-shot
  (B11); GTK's min comes from the compute-size callback (B12) with a MIN-only mask for a resizable
  window (B13, B14) and min=max=natural when not resizable (B15), exported to the compositor as
  `set_min_size`/`set_max_size` (B16); the ack is sent at the end of `handle_configure` (B17); the
  saved size strips shadow margins (B18); with no `configure_bounds` GTK falls back to the union of
  monitor geometry (B19, B20).
* **gkeep 133b867 (3 rows C1-C3 + structure)** — `set_decorated(False)` then
  `set_default_size(420, 500)` (C1); `application_id="org.omarchy.gkeep"` (C2); the only CSS `min-*`
  properties are `min-height: 30px; min-width: 72px;` inside the `button.ink` block declared at
  line 80 (C3 + structure rows). `set_size_request(` occurs **0** times; no `window…{` CSS block
  declares `min-*` (structure table).
* **Seam, context only (8 rows D1-D8)** — Wayland report size clamps at 0 while X11 clamps at 1
  (D1); `sendWindowSize` → `realToReportSize` (D2) → `setSize` whose serial is queued for `onAck`
  (D3), with the X11 branch pushing an xcb configure instead (D4); `onAck` applies the acked size
  (D5); `setSize` latches `m_pendingApply.size` (D6); the configure carries exactly that size and
  the latched states (D7); Hyprland tracks a client min size (D8).

## Exact retained evidence

`verify.log` (last line):
`rows=42 fails=0 pin_mismatch=0 census_ok=True grep_fails=0`
plus `grep_locator_ok=42/42` and `census_clause_h ok=True`.

The verifier imports the **frozen counter's own parsers** (`quote_at`, `occurrences`,
`quote_in_code`, `norm_receipt`, `host_census`) from
`quality/counters/c2-r44-gkeep-size-request.py` — so a row that passes here passes clause d on the
same terms, and the locator printed is the number the gate itself would compute. Independently,
for all 42 rows it re-reads the source line at that number and requires `grep -nF` on a 32-char
prefix of it to report the same line (42/42), so no locator rests on a single parser.

Pins: all five receipts re-hashed in-run and matched `receipts/fetch-sha256.txt` — `PIN-OK` 5/5
(xdg-shell.xml `7ba7f9c8…`, gdktoplevel-wayland.c `0ee38458…`, gkeep-ui.py `07a3c4a5…`,
Hyprland-Window.cpp `d735d454…`, Hyprland-XDGShell.cpp `d90b534c…`).

Clause-h cross-check: `verify_facts.py` calls the frozen `host_census()` on the pinned bytes with
my expected lines and gets them back verbatim, i.e. it independently reproduces
`gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep`
and `hyprland sendWindowSize xdg_setSize=1 x11_configure=1` from the pins (not from the
registration text). The C2 author can cite both without re-deriving them.

## Risks / gotchas for the C2 entry author

1. **`.c` is not comment-stripped by the frozen counter.** `strip_comments` covers `.cpp/.hpp/.h/
   .cc` and `.py/.conf` only, so a GTK quote may come from a `/* */` comment while a Hyprland
   `.cpp` quote may not. All 20 GTK rows here are code anyway, so they are safe either way.
2. **`.py` `#`-stripping kills any quote that reaches a hex colour.** gkeep's CSS is a Python
   f-string full of `#fff475`: a quote spanning a colour line loses everything after the `#`.
   Rows C1-C3 avoid colours; do not extend them.
3. **The 3-word minimum bites on gkeep.** `set_default_size(420, 500)` alone is 2 words;
   `application_id="…"` alone is 1. C1/C2 therefore quote across the call boundaries — keep them
   verbatim.
4. **`fullscreen` and `resizing` state text is near-identical** in xdg-shell ("the client cannot
   resize beyond it" appears in both). Only the leading "The surface is fullscreen." / "The surface
   is being resized." makes each unique; the stripped-down version is `occ=2` and would fail
   clause d.
5. **A7 is exactly 24 words**, one under the ceiling. Do not prepend anything to it.
6. **Nothing here says GTK honours a hint bigger than its natural size.** Section G lists the nine
   further gaps (min size, shadow margins, which states Hyprland sends, whether the rule path
   consults `set_min_size`, ack-vs-commit ordering, non-GTK clients). The C2 entry must not claim
   those from these pins.
7. The provisional ids in the goal (S298 XDGShell.cpp, S299 xdg-shell.xml, S300
   gdktoplevel-wayland.c, S301 gkeep-ui.py) are not used in `facts.md`; it names receipts instead,
   so the integrator assigns ids without a second edit.

## Blockers

None.

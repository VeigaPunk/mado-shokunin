# ScoutCoverageV2 — coverage honesty of C2 (round 44, w2)

Scope: base `6a1a90528fe533cadee506a9fa3e9d13d15cc41f` grepped (`git grep -nIE … <base> -- corpus/knowledge SKILL.md PROVINCE.md tools`, plus
`corpus/README.md corpus/SOURCES.md corpus/lessons` for context) for every surface the landed entry
`corpus/knowledge/hyprland-gkeep-size-request-r44.md` (data `e4678921…`) covers. Entry/receipt line numbers below are from `git show e4678921:…`
and the pinned receipts in `.ufo/waves/round-44/fetch/` (all sha256 verified against `receipts/fetch-sha256.txt` rows by the C2 counter, not re-hashed here).
Tools installed: none. No scratch left on disk (see end).

## Verdict

C2's "coverage" claim is **honest at the entry level**: 4 of the 5 sourced ground areas are genuinely new to the lane's corpus; the fifth (gkeep's own
size declaration) deepens held ground and says so. **No overclaim of new ground was found.** Four non-blocking honesty gaps found: one on the held
S164 row (F1), one on the README row vs entry (F2), one under-coverage / vocabulary collision (F3), two small content imprecisions (F4, F5).

## 1. Surface map: new ground vs deepens held (base evidence)

| surface the entry covers | base grep (base `6a1a905`) | class |
|---|---|---|
| report size: `realToReportSize` (Hyprland-Window.cpp:1685-1699) | 0 hits in knowledge/SKILL/PROVINCE/tools for `realToReportSize`; only lesson mentions (below) | **NEW** |
| `sendWindowSize` early-return + X11/xdg split (Window.cpp:1732-1753), X11 configure branch (:1751) | 0 hits in knowledge/SKILL/PROVINCE/tools; `corpus/lessons/round-43.md:80` says the staged r12 "rests on `Window.cpp::sendWindowSize`, not among this round's pins" | **NEW** (the round-43 refusal reason is what the round-44 pin cures) |
| pending-ack list + `onAck` (Window.cpp:1514-1526) | 0 hits in knowledge/SKILL/PROVINCE/tools; `corpus/lessons/round-43.md:81` names `Window.cpp::onAck` as the decisive source of the refused r13/r14; `corpus/lessons/round-43-verifier-spotcheck.md:74` shows a w1 pin (`w1/ExecGoalVsValue/pins/window.cpp:1526,1687-1698`) read these lines in round 43 but never landed them in corpus | **NEW to corpus** (read-but-unlanded in round 43) |
| `xdg_toplevel` `setSize` / deferred `sendConfigure` (XDGShell.cpp:354-358, 443-462) | 0 hits for `setSize`, `sendConfigure`, `XDGShell`, `xdg_toplevel`; `corpus/SOURCES.md:465` only lists "xdg-shell" as a title-screened, unread chapter | **NEW** |
| xdg-shell protocol: configure hint, zero size, `ack_configure` (xdg-shell.xml:560, 1144-1172) | 0 hits for `ack_configure`/`xdg_surface`; SOURCES.md:465 as above | **NEW** |
| GTK 4.24.1 toplevel configure store/constraint/0x0 (gdktoplevel-wayland.c) | 0 hits for `gdktoplevel`, `configured_width`, `compute_size`, `handle_configure`; the only GTK mentions are unrelated (`walker-route-r18.md:50` Walker is a GTK4 launcher; `theme-route-r18.md:71` `gdk_pixbuf`) | **NEW** |
| gkeep `application_id` and `set_default_size(420, 500)` (gkeep-ui.py:449, 476) | **held**: `hyprland-gkeep-geometry-r43.md:24,62` (S297 excerpt) | **DEEPENS held** (S297; full-file sha `07a3c4a5…` same as S297's stated full-file sha) |
| "no `set_size_request`; `min-width`/`min-height` only in `button.ink`" (gkeep-ui.py:87-88) | 0 hits at base for `set_size_request`/`size_request` in knowledge; r43 lesson line 80 only mentions the staged file name | **NEW** (a negative census over the full file; S297 was an excerpt 446-488, so it could not hold it) |
| host rule `size 420 500`, GOAL box, floating first-map branch, tiled pseudo-size | held by `hyprland-gkeep-geometry-r43.md` (S290-S296) | **HELD**, cited not re-covered; entry §1 correctly points at it |
| SKILL.md / PROVINCE.md / tools | `git grep -E 'hyprland-gkeep|size-request'` on base over SKILL.md PROVINCE.md tools: 0 hits; SKILL.md:225,284 and `tools/mado-geometry.py:10,267,279` mention gkeep only as the rule-vs-dump example | no held entry; the new entry is not linked from SKILL.md/PROVINCE.md (same as r43's entry; neither is a "Province routes" table row) |

Entry count: base `git ls-tree -r --name-only <base> corpus/knowledge` = 60 files; data = 61 (the one new file). README index rows beginning
```| `knowledge/``` : base 60 → data 61 (+1, the new row at README.md:72 of the data tree).

## 2. README coverage-map row (corpus/README.md:72 at data; `## Coverage map` starts :3)

Present, in the right table, sorted after the r43 row (:71), id `MADO-R44-1`, Sources column `S164, S298, S299, S300, S301` = exactly the entry's five
`source:` ids. Frontier subsection `### Round-44 gkeep size-request route` at README.md:304 (data) follows the Round-43 subsection (:295); it says
"Still open: … the ack round-trip under a real client, gkeep's widget-tree minimum and the drawn size remain unmeasured", matching the entry's UNK rows.
The header's own caveat (README.md:8, "A new index row does not close a behavioral gap") is honoured: the row ends "the ack round-trip and the drawn size stay UNK".
Province-routes table (README.md:79-96) has no gkeep route at base or data; unchanged (as r43).

Gaps in the row (all documentation, none blocks the counter):

- **F2 (LOW-MED, row vs entry vs SOURCES).** The README row cites `Hyprland-XDGShell.cpp:354-357` **and `:629-643`** (`scheduleConfigure`) for the xdg configure.
  The entry never cites `:629-643` or names `scheduleConfigure`; S298's range cell (SOURCES.md) lists only `354-358` and `443-462`. At `:629-643`
  (receipt) `CXDGSurfaceResource::scheduleConfigure` allocates the serial and `configure()` sends the **separate `xdg_surface.configure(serial)`** — the event
  the client actually acks. The entry's §2 says setSize "returns the next configure serial" and the deferred `sendConfigure` (:455) "sends it", which can
  be read as the toplevel event carrying the serial; in the receipt the toplevel configure (:455, size+states) and the serial-bearing surface configure
  (:642) are two events. Reproduction: `sed -n '629,643p;443,458p' .ufo/waves/round-44/fetch/Hyprland-XDGShell.cpp`. The README row is thus more precise
  than the entry, and cites a range its own SOURCES row does not list.
  Suggested entry correction (§2, replacing "the deferred state application sends it to the client:"): "the deferred state application sends the
  size and states in an xdg_toplevel.configure, and the xdg_surface's scheduleConfigure sends the serial the client acks in a separate
  xdg_surface.configure (Hyprland-XDGShell.cpp:629-643);". Computed locator: `grep -n 'uint32_t CXDGSurfaceResource::scheduleConfigure' …/Hyprland-XDGShell.cpp` → 629; `m_resource->sendConfigure(m_scheduledSerial);` → 642.
- **F2b (LOW).** README row says "assimilation of the gkeep-theme residue, successor path to the held excerpt S297"; the entry's `assimilated-from:` names
  `gkeep-client-size-request-r12.md`. The r43 row names its staged predecessor (`gkeep-size-to-real-size-r11`); the r44 row does not name r12. Provenance is
  complete in the entry and the lesson ledger, only the index row is thinner than its r43 sibling.
- README row cites `onAck` as `:1514-1521`; the ack-size write the entry relies on is `:1526` (outside the row's range, inside the entry's cite). Consistent, not wrong.

## 3. Held-row honesty: S164

- **F1 (MED, documentation honesty of a held row).** S164 (`corpus/SOURCES.md:176` at data) had its used-by cell extended, as the task states, but its **range
  cell is unchanged**: `src/desktop/view/Window.cpp:103-108,141-146,1484-1486,1791-1795,2143-2281,2497 …` and its "what it supports" cell still reads
  "applicator construction, static-rule application, and property-change hooks". The entry cites S164 at `:1514-1526`, `:1685-1699`, `:1732-1753` —
  none inside the row's listed ranges — and for claims (report size, ack list) the row's cell does not describe. The full-file sha256 is correct
  (`d735d454…` = `fetch/Hyprland-Window.cpp`, receipts/fetch-sha256.txt:2), so the claims are sourced; the row's *licence column* does not say so.
  The S164 row also names no receipt path (S298-S301 do), so `Hyprland-Window.cpp:NNNN` locators resolve only via `.ufo/waves/round-44/fetch/`.
  Reproduction: `git show e4678921:corpus/SOURCES.md | grep -n '^| S164 '` (range cell above); `git show e4678921:corpus/knowledge/hyprland-gkeep-size-request-r44.md | grep -n 'Hyprland-Window.cpp:1514\|:1685\|:1732'`.
  Suggested correction: append to S164's range cell "; round-44 reads :1514-1526 (onAck), :1685-1699 (realToReportSize), :1732-1753 (sendWindowSize), receipt `.ufo/waves/round-44/fetch/Hyprland-Window.cpp`" and extend the "supports" cell with "outgoing report size, pending-ack list".
- The counter does not catch this (`c2-after-data.txt`: `clause=c id=S164 new=0 status=mined used=1 ok=1` checks status/used-by only). Not a predicate defect — registration-v2 scopes C2 to the entry, registry id/used-by, lesson, README, pins — but it means the C2 count does not attest the row's range cell.

## 4. Vocabulary / under-coverage (new ground left on the table inside the held pin)

- **F3 (MED-LOW, content risk).** `getReportedSize()` (Window.cpp:1861-1866, receipt) is ack-derived for a Wayland client (`m_current.ackedSize`), the
  consuming end of the pair `onAck` writes into `m_pending.ackedSize` (:1526). `corpus/lessons/round-43-verifier-spotcheck.md:98` (D1) already warned that
  "the reported size" is ambiguous because `getReportedSize()` is ack-derived. The entry uses "report size" for the *outgoing* goal (`realToReportSize`, §1;
  README row: "takes the real box and reports it") and never mentions `getReportedSize`/`m_reportedSize`, never distinguishing the two "reported" notions.
  The entry's unestablished list says "what Hyprland does when a client commits a buffer whose size differs from the acked one (not among the pins)" — the
  `ackedSize` read-side `getReportedSize` is in the *held* pin (:1861-1866), so the sentence "not among the pins" is true only for the buffer-commit handling, not for
  the ack's readout. Not a false claim; an unnamed neighbour that a reader could confuse with §1. Reproduction: `grep -n 'getReportedSize\|ackedSize' .ufo/waves/round-44/fetch/Hyprland-Window.cpp` → m_reportedSize at :837, :1549, :1574, :1863, :1866 (also :2544, :2740), ackedSize at :1526 and :1865.
  Suggested sentence for §2 INF: "Hyprland's own getReportedSize() for a Wayland client reads the acked size (Hyprland-Window.cpp:1861-1865), not the report size of §1."
- **F4 (LOW, content nuance relevant to C1's fullscreen exit).** §4 says a 0x0 configure "keeps the size GTK computes itself
  (gdktoplevel-wayland.c:539-544)". The receipt shows one exception: when GTK leaves a maximized/fullscreen/tiled (fixed) state with a 0x0 configure it
  restores the saved size, `width = wayland_toplevel->saved_width;` (gdktoplevel-wayland.c:656-658, guarded at :656 by `saved_size && !fixed_size && was_fixed_size`).
  Reproduction: `sed -n '640,660p' .ufo/waves/round-44/fetch/gdktoplevel-wayland.c`. Suggested sentence: "A 0x0 configure is recognised as one
  (gdktoplevel-wayland.c:647) and keeps the size GTK computes itself (:539-544), except when it ends a maximized, fullscreen or tiled state, where the
  saved pre-state size is used (:656-658)." Compute the final locators with `grep -n 'saved_size && !fixed_size && was_fixed_size'`.
- **F5 (LOW, locator).** §5 cites `window.set_decorated(False) window.set_default_size(420, 500)` as `(gkeep-ui.py:475)`; the receipt has set_decorated at :475
  and `set_default_size(420, 500)` at **:476** (`grep -n 'set_default_size' fetch/gkeep-ui.py` → 476). The quote spans two lines; the single locator covers only the first.
  The README row cites `:476` correctly. Suggested: `(gkeep-ui.py:475-476)`. The counter's clause g anchors S301 at `locator_line=475` (c2-after-data.txt), so it passes either way; clause j has no surface for the default-size line (only the census line carries it).

## 5. What I checked and found sound (no finding)

- `sendWindowSize` early return (:1743-1744) and the `setSize` pairing with `.floor()` (:1753): receipt matches the entry's §1 text.
- `onAck` newest-pair-not-after-serial semantics, erase of older pairs, X11 early return, ackedSize write (:1514-1526): matches §2.
- xdg-shell.xml hint / zero-size / ack_configure at :1150, :1154-1157, :560: matches §3. GTK `should_constrain` for non-0x0 (:666) and the min-size hints (:490-494): matches §4's constraint claim.
- gkeep full file (488 lines): one `Gtk.ApplicationWindow` (:474), no `set_size_request`, `min-width/min-height` only :87-88 inside the button CSS (:80-91): matches §5.
- The r12 corrections ("not adopted" list) and the "ledger" of five other staged files in `corpus/lessons/round-44.md:57-70`: each refusal reason names an absent journal/package path or an unpinned doc, consistent with the base grep (no base text covers those surfaces).

## 6. Summary for the L1

| id | severity | attacks | fix |
|---|---|---|---|
| F1 | MED | SOURCES.md S164 range/supports cells vs entry cites | append the round-44 ranges and receipt path to the S164 row |
| F2 | LOW-MED | entry §2 vs README row (`:629-643`) vs S298 range | add the xdg_surface.configure serial sentence; cite `:629-643` in S298's range |
| F2b | LOW | README row provenance | name staged r12 in the row |
| F3 | LOW-MED | entry §1/§2 vocabulary (`getReportedSize`) | add the INF sentence above |
| F4 | LOW | entry §4 0x0 sentence | add the saved-size exception |
| F5 | LOW | entry §5 locator | `:475-476` |

No OPEN predicate defect found (the C2 v2 predicate does not claim to check S164's range cell or claim-to-text binding; those are declared residuals).

Scratch: `/fast/scratch/hyaku/mado-r44/ScoutCoverageV2*` (a ~100 KB grep dump and a README copy) removed before finishing.

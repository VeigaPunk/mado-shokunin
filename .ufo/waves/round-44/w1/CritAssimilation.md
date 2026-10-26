# CritAssimilation — findings (mado round 44, w1)

Seat: critic of the planned assimilation decisions (registration §2b) and of the r12 predecessor's claims.
Every quote below is verified by `.ufo/waves/round-44/w1/CritAssimilation/quote-check.sh`, whose output is
`.ufo/waves/round-44/w1/CritAssimilation/quote-check.txt` (`grep -nF`, computed line numbers in column 2);
id/mapping facts are in `.ufo/waves/round-44/w1/CritAssimilation/id-receipts.txt`; the tag/commit equality
fetch is in `.ufo/waves/round-44/w1/CritAssimilation/tag-fetch.txt`; the census recompute is in
`.ufo/waves/round-44/w1/CritAssimilation/census-recompute.txt`.
Pins read: `.ufo/waves/round-44/fetch/{Hyprland-Window.cpp,Hyprland-XDGShell.cpp,xdg-shell.xml,gdktoplevel-wayland.c,gkeep-ui.py}`.
Residue read: `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/*` (read-only).

## 0. What survives scrutiny before the attack

- **S311 → S164 is sound, and the proof is byte equality, not a tag name.** `refs/tags/v0.56.2` resolves to
  `efb50993780079460b0cbed1363e2166a2de1d9f` (id-receipts: `git ls-remote`), and the raw tag copy of
  `src/desktop/view/Window.cpp` has the same sha256 as the pinned commit copy —
  `d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded` (both files, id-receipts). The tag copy of
  `WindowRuleApplicator.cpp` likewise hashes to the lane S155 row's `fec33f9a…` (same receipt).
- **S312 → a new row is forced and is not a duplicate authority.** Lane S297's location is the excerpt receipt
  `.ufo/waves/round-43/fetch/gkeep-ui-excerpt.py` (id-receipts, last cell-1 token), not the upstream URL; S312's
  location is the full-file raw URL and its receipt is the full-file pin `gkeep-ui.py` (sha256 `07a3c4a5…`,
  byte-identical to `git -C ~/Projects/gkeep show 133b867:gkeep/ui.py`, id-receipts). The C2 contract's clause
  i+ (all five PINS cited) cannot be met by S297's excerpt receipt, so a full-file row is required. The
  renumber map's own wording — "Mapping is by document (renumber-map.tsv)" — is what needs fixing; see §5.4.
- **The id guard's regex claim is true but is not the real-registry check.** The real registry holds
  0 rows indented 1–3 spaces and 234 column-zero rows (id-receipts), 42 collisions (id-receipts). The scratch
  registry in `assimilation/id-guard.md` demonstrates regex behaviour only; the entry must not be guarded by a
  proof about a scratch file.
- **The two census lines the C2 contract demands recompute exactly** from the pins
  (`.ufo/waves/round-44/w1/CritAssimilation/census-recompute.txt`):
  `gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep` and
  `hyprland sendWindowSize xdg_setSize=1 x11_configure=1` (Window.cpp:1732–1754 body; `->setSize(` once,
  `->configure(` once). This is a bookkeeping line, not a behavioural finding (the counter says so too).

## 1. r12 claim by claim

| # | r12 claim (locator) | verdict | pinned evidence |
|---|---|---|---|
| 1 | §1 quotes: `void CWindow::sendWindowSize(bool force) {`, `const auto REPORTSIZE = realToReportSize();`, the `m_pendingSizeAcks.emplace_back(…setSize(REPORTSIZE), REPORTSIZE.floor());` line (r12:24-28) | **survives** byte-for-byte | Window.cpp:1732, :1741, :1753 (same bytes at tag and commit) |
| 2 | §1 INF: "the acknowledgement is tracked — which is precisely the mechanism by which a client could report a different size than the one asked for" (r12:34-35) | **REFUTED** | `onAck` stores `m_pendingSizeAck->second` — the value the compositor asked for — as `ackedSize` (Window.cpp:1520, :1526); the ack itself carries only a serial (XDGShell.cpp:605; xdg-shell.xml:564); `getReportedSize` then returns `m_current.ackedSize` (Window.cpp:1865). The tracked ack is a reconciliation of the compositor's own number, not a client size channel. |
| 3 | §1 OBS "the compositor … asks the client … with xdg_toplevel.set_size" (r12:30-31) | **survives, with a protocol correction** | `setSize` stores `m_pendingApply.size` and returns the configure serial (XDGShell.cpp:355, :635), which is sent by `sendConfigure` (XDGShell.cpp:455). But the wire event is `xdg_toplevel.configure`, whose size is "a hint to the window" (xdg-shell.xml:1150), not an order. |
| 4 | §2 quotes: ApplicationWindow line, `window.set_default_size(420, 500)`, "no `set_size_request` call at all", "only `min-width`/`min-height` … under the `button.ink` selector" (r12:41-47) | **text mostly survives; one quote is altered, and the inventory is incomplete** | gkeep-ui.py:474, :476; `set_size_request` count 0; CSS lines 87–88 under `button.ink` (gkeep-ui.py:167). But r12:41 prints `title=\"gkeep\"` with backslashes that are not in the source line — the entry must quote gkeep-ui.py:474 verbatim. The same window also sets `window.set_decorated(False)` (gkeep-ui.py:475) and installs a widget tree — neither appears in r12's inventory, and neither is a size statement r12 can ignore. |
| 5 | §2 INF: "a GTK4 window with no minimum-size request will adopt the size the compositor configures" (r12:52-53) | **REFUTED as a general claim** | GTK asks the toplevel for a computed size (`gdk_toplevel_notify_compute_size`, gdktoplevel-wayland.c:485), writes its `min_width` into the hints (gdktoplevel-wayland.c:492) and **sends them**: `XDG_SHELL_CALL (xdg_toplevel, set_min_size, …)` (gdktoplevel-wayland.c:1333). For a non-zero configure it sets `should_constrain` and runs `gdk_surface_constrain_size` against those hints (gdktoplevel-wayland.c:513, :525), so the client has a minimum channel even when the app made no `set_size_request` call. GTK adopts the configured size only when it lies inside GTK's own computed min/max; "no `set_size_request`" does not mean "min 0". |
| 6 | §2 INF: "The one way the rendered geometry could differ … is excluded by the client's own source rather than assumed" (r12:53-57) | **unsupported (completeness claim)** | The client's source r12 cites does not measure the window; the pins contain no measure of gkeep's widget tree, so min ≤ 420×500 is not shown. Locally the widest row is the four `button.ink` buttons (`Paste, Save, Delete, All notes`, gkeep-ui.py:171–187) at CSS `min-width: 72px` (gkeep-ui.py:88) plus 3×8 spacing and 16+16 margins — 344 px, plausibly under 420, but the header also packs a `width_chars=13` stamp (gkeep-ui.py:160) and the pins stop at "plausible". The claim "excluded … rather than assumed" is itself the assumption. |
| 7 | §3 INF: "The rendered geometry of a gkeep window is 420×500 on this host's build … with no competing claim from the app" (r12:59-62) | **REFUTED as stated** | (a) It is unobserved — r12's own UNK says so. (b) The number the compositor holds is its own target: `realToReportSize` returns `m_realSize->goal()` (Window.cpp:1687, :1741), which the layout writes. (c) The client has a size channel the pins show (gdktoplevel-wayland.c:1333, :525). (d) The r43 entry already records that the reported GOAL is not the drawn CURRENT during the open animation, and that no request-socket verb exposes CURRENT (`corpus/knowledge/hyprland-gkeep-geometry-r43.md:54,58`). |
| 8 | §3 INF: "The chain is now complete on both sides" (r12:59) | **unsupported** | The client side is exactly where r12 read only the default-size call and not the min/max channel; "complete" is contradicted by row 5 above. |
| 9 | §3 UNK: the observation is still missing (r12:65-68) | **survives** | r12's own recheck command is the route; nothing in round 44 supplies the observation. |

**What r12 contributes if admitted:** the `sendWindowSize → realToReportSize → setSize → scheduleConfigure`
path and gkeep's two declarations (application id, default size). **What it must not contribute:** sentence
#2 (a false mechanism), #5/#6 (a completeness claim about the client's minimum), #7/#8 (an unobserved
"rendered geometry" with no client claim). The r44 entry can carry #1, #3, #4 and the UNK, and must replace
#2 with the `onAck` reading and #5–#7 with the GTK constrain/set_min_size reading.

Note on provenance: r13 got this right where r12 got it wrong — "it cannot substitute a different number"
(r13:39). Admitting the r44 entry without that sentence would re-import r12's inversion while r13, which
records the correction, is refused. That is the central design hazard.

## 2. Attack on the planned refusals of r13/r14/r15

- **r13 — do not refuse it wholesale.** Its §1 is true and is now *pinned*: the onAck quotes at r13:29-31
  are the pinned Window.cpp:1514–1526 (r13:27,29,31), and its §2 map-line quote (r13:50) is the pinned Window.cpp:2515 —
  both attainable through held S164, whose receipt is one of the PINS. Only §3's sweep receipt (S320) is
  absent. A `REFUSE … reason=…` line would say the file is not adopted while the entry adopts its decisive
  half; that is false provenance in the other direction. Refusing it would lose (i) the only statement in
  the residue that corrects r12's mechanism, and (ii) the map-line route, which the round-43 lesson already
  parked as "the journal route stays open for a later entry" (`corpus/lessons/round-43.md:81`). If a refusal
  is required for clause i, refuse the *sweep* by naming r13 only with a reason that its §1/§2 halves are
  carried by the entry, and put the flip on the missing S320 receipt.
- **r14 / r15 — refusal is safe.** Their decisive receipts (S326, S339) exist in neither the package nor the
  lane: the find over both trees returns 0 (id-receipts), and the package tree outside `knowledge/` has no
  `lanes/` directory (id-receipts). Clause c/d cannot mint a registry row or a GATE line for a receipt that
  is not in the tree. What is lost is the sweep *numbers*; those were never admitted (r43 lesson:81 records
  the route as "not adopted; residue"), so refusing them records a decision, not a corpus regression. The
  flip is honest: the whole-journal sweep is a permitted read, so "once the sweep receipt is committed as an
  in-lane own-work receipt" is a real condition, not a fiction.
- **The better refusal is r10.** Its INF "the number the compositor reports is whatever the client actually
  used" (r10:41-47) is contradicted by the pinned `realToReportSize` (`m_realSize->goal()`, Window.cpp:1687,
  :1741) and by the round-43 entry's GOAL/CURRENT section (`corpus/knowledge/hyprland-gkeep-geometry-r43.md:54,58`). Refusing r10 documents a correction of a false
  mechanism; refusing r14 merely records an absent receipt. If the design wants one refusal that *teaches*,
  use r10 (or r10 and r14), not r13.
- **r9** is not a refusal candidate for loss: it is simply not admissible (S286 is a docs receipt not among
  PINS; S292/S293 are absent), and its §3 already contains the same "nothing in the app's own source
  suggests one" completeness claim that r12 hardened. Its `fetchClass` half is already held via S164.

## 3. Attack on the planned ADMIT of r12

- r12 is the **only** residue file whose every decisive source maps to an admissible row (S311→S164,
  S312→S301). That makes it the least-lossy ADMIT. It is still only safe if the entry rewrites the three
  INF blocks above. The C2 counter's own declared residual says the quote-to-claim binding is not scored,
  so a copy of r12's prose *passes the counter* and ships the false mechanism; the non-author reading is the
  only gate. Recommendation: the lesson's `ADMIT` line should name the correction, and the entry must not
  contain r12:34-35, r12:52-53 or r12:59-62 as claims.

## 4. Concrete defects in the planned entry/lesson, from the frozen counter

1. **Clause e+ forces the commit URL.** Every cited id whose receipt name starts with `Hyprland-` must have
   a location beginning `https://raw.githubusercontent.com/hyprwm/Hyprland/efb5099…/`. r13's source lines
   use the tag URL `…/v0.56.2/…` (r13:10-11) and must not be copied for S164; the tag bytes are equal, so
   nothing is lost by using S164's commit URL.
2. **Clause b forbids staged-id tokens.** r12's `source: S311` / `source: S312` lines must be rewritten to
   S164 / S301; no `S311`/`S312` may appear anywhere outside fences.
3. **Clause g is one line per id.** Every unfenced line that names a cited id must carry that id's Gate
   quote and computed locator. An id cannot be discussed in a second line without repeating the quote, and
   a line naming two ids fails. Plan the entry so each id appears in exactly one unfenced line.
4. **Renumber-map wording.** "Mapping is by document … no staged id is carried" contradicts its own S312 →
   new-row decision if "document" means the upstream file (S297 is the same file, excerpted). State the rule
   as *by registered location/receipt* and cite the sha256 equality for S311/S164.
5. **xdg state qualifier.** A blanket "the client may ignore the configure size" is false under maximized
   and fullscreen: there the geometry "must be obeyed" (xdg-shell.xml:841). gkeep's window is floating, so
   the hint reading (xdg-shell.xml:1150) governs here, but the entry must say which state it is talking
   about.
6. **The ack is mandatory.** "Clients must send an ack_configure in response to this event"
   (xdg-shell.xml:1166; the commit-side rule at :564). The entry must not say a client may decline to ack;
   the client's freedom is in the size it commits, not in the ack.
7. **Configured size is window geometry, not buffer pixels.** GTK adds shadow to the configured size before
   applying it (gdktoplevel-wayland.c:518-520) and subtracts shadow from the min it sends
   (gdktoplevel-wayland.c:1303-1315). `set_decorated(False)` (gkeep-ui.py:475) makes this small for gkeep,
   but the entry must not equate the configure width/height with buffer pixels: the configure arguments are
   "in window geometry coordinates" (xdg-shell.xml:1150-1152).
8. **The Gate quote for S164 must be comment-free and >= 3 words.** Clause d runs the quote through
   `strip_comments` before matching, so the `// apply pending size…` fragment (Window.cpp:1526) would not
   match once its comment is stripped, and the `emplace_back(…)` line (Window.cpp:1753) is two words, below
   clause d's 3-word floor. Use `void CWindow::sendWindowSize(bool force) {` (Window.cpp:1732, 4 words,
   comment-free) as S164's Gate quote.
9. **Clause g makes the Gate quote a per-line toll.** Every unfenced line naming S164 must carry that Gate
   quote *and* its computed locator, and may name no other cited id. A paragraph that discusses the ack
   line at Window.cpp:1526 or the map line at :2515 must therefore either repeat the Gate quote on that
   line or be fenced; plan the entry with one unfenced line per id, or accept repeated Gate quotes.
10. **Counter docstring nit (untouchable, record only):** clause i says "the 11 gkeep-theme package files in
   STAGED" while `STAGED` holds 10 (r11 was admitted in round 43). Not scored; an erratum for the next
   registration.

## 5. Smallest safe corrections (for the L1)

1. ADMIT r12, but the r44 entry carries the `onAck` reading (`ackedSize = m_pendingSizeAck->second`,
   Window.cpp:1526) and GTK's `set_min_size`/constrain path (gdktoplevel-wayland.c:1333, :525); strike
   r12:34-35, :52-53, :59-62 from the entry.
2. Add a REFUSE for r10 (contradicted by Window.cpp:1687/:1741 and round-43 §3) and for r14 (absent S326
   receipt). Do not refuse r13 wholesale; if clause i wants it named, refuse only its S320 sweep with the
   flip on the committed receipt.
3. Cite S164 at the commit URL; cite S301 (`gkeep-ui.py`) for the full-file census; carry no S311/S312 token.
4. Reword the renumber map to "by registered location/receipt", with the tag=commit sha256 equality noted.
5. Entry prose: "the compositor's target is 420×500; the configure size is a hint the client's GTK
   constrains to its computed minimum; the drawn buffer is unobserved" — no "will adopt", no "no competing
   claim", no "rendered geometry is 420×500".

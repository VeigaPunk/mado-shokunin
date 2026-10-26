# Lessons — mado, round 44

Round intent: registration `.ufo/waves/round-44/registration.md` (freeze `e2289516a9a857f55cda7be635933e89b931c3da`, base
`6a1a90528fe533cadee506a9fa3e9d13d15cc41f`, the round-43 tip after its non-author closure). Host `2026-10-26`: Hyprland 0.56.2-4
(`efb50993780079460b0cbed1363e2166a2de1d9f`), gtk4 1:4.24.1-1, wayland-protocols 1.49-1. Round 43 closed `ok`/`admitted` and routed seven
defects (`corpus/lessons/round-43-verifier-spotcheck.md:97-109` §6 D1-D7); this round mines them as Mistakes M44-1..M44-7 instead of
re-registering them as claims. Shape: **two v1 waves** — `w1` (build + first falsifiers, 38 seats; `.ufo/waves/round-44/w1-spec.json`
`items` length 38) and `w2` (falsify, after the data commit, `<<L1>>` seats, read from `.ufo/waves/round-44/w2-results.json`).

C1 lands the round-43 tool's **contract extension** (operability, capability acquisition): `tools/mado-geometry.py` gains the client's
fullscreen state. fsmode is the `fullscreen` value when it is a JSON integer (not a boolean, not a float) equal to 1 or 2, else 0; a matched
client's verdict is tested BADSIZE | FULLSCREEN (2) | MAXIMIZED (1) | TILED | AGREE | DIFFER; the summary carries
` maximized=<n> fullscreen=<n>` between `badsize=<n>` and ` verdict=` exactly when their sum is > 0, and is byte-identical to the round-43
line otherwise. The ground: Hyprland sets a maximized window's target to the work area and a fullscreen window's to the monitor box
(`fetch-c1/Hyprland-FullscreenHandler.cpp:191-199`: `FSMODE_FULLSCREEN` → `MONITOR->logicalBox()`, `FSMODE_MAXIMIZED` →
`m_space->workArea(...)`), and `hyprctl clients -j` prints the internal mode as `fullscreen` (`fetch-c1/Hyprland-HyprCtl.cpp:431` in the JSON
branch, `:451` in the plain-text branch, both `getFullscreenModes(w).internal`; `FullscreenController.hpp:34`). Target `fixtures=26/26 verdict=TARGET_MET` under `PRED-C1-r44`; base `fixtures=12/26 tool=present
verdict=TARGET_MISSED`, clauses `a:1 b:0 b4:0 g:1 r:1`, exit 1 (`receipts/c1-before-base.txt`; the lattice count varies with the nonce —
`13/26` for the do-nothing BASE-tool control in `receipts/ctl-c1.txt:3` — the verdict does not), with the round-43 counter still
`fixtures=37/37 … TARGET_MET` on the same bytes (`receipts/c1-before-base.txt:28`, clause r).

C2 admits `corpus/knowledge/hyprland-gkeep-size-request-r44.md` (coverage, sourced; assimilation of the gkeep residue): what happens
**after** the box is set — `CWindow::sendWindowSize` → `realToReportSize` → xdg `setSize` → `scheduleConfigure`, the pending-ack list and
`onAck` (`fetch/Hyprland-Window.cpp:1732-1754`, `:1514-1528`, `:1685-1687`), the X11 `configure` branch (`:1750-1751`), what xdg-shell
1.49 says a configure size is (`fetch/xdg-shell.xml:1145-1167`), what GTK 4.24.1's Wayland toplevel does with it
(`fetch/gdktoplevel-wayland.c:606-706`), and what gkeep 133b867 itself declares (`fetch/gkeep-ui.py:449,474-477`). Base holds none of
it: `git grep -ciE 'sendWindowSize|pendingSizeAcks|xdg_toplevel.configure|set_size_request' 6a1a905 -- corpus/knowledge PROVINCE.md
SKILL.md tools` → exit 1 (`receipts/c2-ground-base.txt`); base `admitted=0/1` (`receipts/c2-before-base.txt`).

Axes: every published axis ties at its maximum at base (`receipts/axis-base.txt`: navigation 60/60, calibration 68/68, operability 12/12,
`MADO_AXIS: checked=3 mismatched=0 rev=6a1a905…`), so each is a lowest axis; lanes **operability** (C1) and **coverage** (C2).

**Access date.** Every row opened this round carries `opened 2026-10-26`; the registry tops at `S297` (234 rows:
`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 234 at this round's base), so the four new rows are
S298-S301 and no renumbering is needed (`assimilation/reg-ids` 234, `assimilation/staged-ids` 147, `assimilation/collisions` 42 — the
package's own S203-S349 collide with the lane's S203-S297 and are mapped **by document**, `assimilation/renumber-map.tsv`). The entry's
header carries exactly one `verified-at: 2026-10-26` (PRED-C2-r44 clause b). Held row S164 keeps its `opened 2026-10-23` and
`recheck: on-release`; its only edited cell this round is `used-by`.

## Gate

GATE S164 receipt=.ufo/waves/round-44/fetch/Hyprland-Window.cpp sha256=d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded quote="else if (m_xdgSurface && m_xdgSurface->m_toplevel) m_pendingSizeAcks.emplace_back(m_xdgSurface->m_toplevel->setSize(REPORTSIZE), REPORTSIZE.floor());"
GATE S298 receipt=.ufo/waves/round-44/fetch/Hyprland-XDGShell.cpp sha256=d90b534c9097ab573f606c2dad4b5fab6dc31c4ca13240c43ef0bb74da7ed0c0 quote="uint32_t CXDGToplevelResource::setSize(const Vector2D& size) {"
GATE S299 receipt=.ufo/waves/round-44/fetch/xdg-shell.xml sha256=7ba7f9c8473deee674cb1f154a18abd0bb0cc072604fc055b0c15e459fc4c7df quote="The width and height arguments specify a hint to the window about how its surface should be resized in window geometry coordinates."
GATE S300 receipt=.ufo/waves/round-44/fetch/gdktoplevel-wayland.c sha256=0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe quote="wayland_surface->next_layout.configured_width = width;"
GATE S301 receipt=.ufo/waves/round-44/fetch/gkeep-ui.py sha256=07a3c4a50bf2154edc82f531b1cf2cc3c6e7067e9f2f02d5a4b4d9d27fe5d66a quote="window.set_default_size(420, 500) self.board = Board(window)"

ADMIT merge/mado/knowledge/corpus/knowledge/gkeep-client-size-request-r12.md as corpus/knowledge/hyprland-gkeep-size-request-r44.md
REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-rendered-geometry-record-r13.md reason=its decisive receipt is a round-13 journal sweep at a package path that does not exist in this lane, and its Window.cpp half is superseded by held S164; flip if a journal sweep is committed inside this lane and re-shows the map-time line
REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-rendered-geometry-record-r14.md reason=one whole-journal sweep outside this lane carries the entire absence claim, and no pinned source of this round touches the journal; flip if the sweep is re-run and committed under this lane's receipts
REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-geometry-never-recorded-r15.md reason=its corpus-wide absence claim rests on an artifacts sweep at a package path, which is a different ground from the size-request chain; flip if a lane-committed sweep over this lane's own artifacts reproduces it
REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-rendered-geometry-chain-r9.md reason=its two distinctive links need the GTK default-size documentation page and the window-rules wiki, neither pinned this round, and its round-9 receipts are absent from this lane; flip if both pages are pinned and each gets a row

Receipts above: five pre-wave pins (`fetch/`, mode 100644, sha256 equal to `receipts/fetch-sha256.txt`). Four of the five are this round's
new documents — S298 `src/protocols/XDGShell.cpp`, S299 `stable/xdg-shell/xdg-shell.xml` at wayland-protocols 1.49, S300
`gdk/wayland/gdktoplevel-wayland.c` at GTK 4.24.1, S301 `gkeep/ui.py` at gkeep `133b867` (the full file, of which held S297 is only its
446-488 excerpt); S164 is a **held** row (`corpus/SOURCES.md:176`, the exact commit URL of the pinned `Hyprland-Window.cpp`), cited with
the pinned bytes rather than a new row, as round 43 did for S155/S158.

Each quote was checked with the v2/r44 counter's own functions (`quote_at`, `occurrences`, `quote_in_code`, `strip_comments`, imported
read-only from `quality/counters/c2-r44-gkeep-size-request.py`): 3-22 words, exactly one word-bounded occurrence in its own receipt,
outside comments (`//`, `/* */`, `#`), and **zero** occurrences in the other four pins. Locators the entry carries (computed with the same
`quote_at`, never typed): `Hyprland-Window.cpp:1752`, `Hyprland-XDGShell.cpp:354`, `xdg-shell.xml:1150`, `gdktoplevel-wayland.c:681`,
`gkeep-ui.py:476` (the S301 quote spans `:476-477`; the counter reads the start line, `quality/check-locators.py` wants the range — M43-7).
S301's quote string is the same normalized text as S297's Gate quote in `corpus/lessons/round-43.md`, over a different receipt (the full
file, not the excerpt) and a different id; no clause compares quotes across lessons, and the duplicate is recorded here so it is not read
as a copy error.

C1's three grounding pins (`fetch-c1/Hyprland-FullscreenController.hpp`, `Hyprland-FullscreenHandler.cpp`, `Hyprland-HyprCtl.cpp`) carry
**no** GATE line: they are cited by the counter docstring, not by a registry row, so they have no id to bind; their sha256 are in
`receipts/fetch-sha256.txt` and the counter's `PRED-C1-r44` names their paths in the module docstring.

## Assimilation ledger (theme: the gkeep size request; package `merge/mado/`, read-only)

| candidate | scope (PROVINCE) | held | quality bar | verdict |
|---|---|---|---|---|
| `gkeep-client-size-request-r12.md` | in (upstream code at the host's commit, the app's own source) | the lane holds the size chain up to the box (round 43) and the gkeep excerpt as S297; no lane text holds `sendWindowSize`, the ack list or the xdg configure | its two sources are re-grounded by document: staged S311 (`Window.cpp` at tag `v0.56.2`) → held S164 (commit URL), staged S312 (`gkeep/ui.py`) → new S301; the tag-form URL is not carried (clause e+ wants the commit form), and its `verified-at: 2026-10-24` is re-dated to 2026-10-26 with a fresh recheck | **admitted as the successor** (`ADMIT` above), extended by this round's three pins (S298-S300) which the r12 text does not have |
| `gkeep-rendered-geometry-record-r13.md` | in, but its ground is the journal | — | its two `Window.cpp` sources (onAck, the map request log line) are pinned here and are what the successor cites; its decisive one (`S320`, `lanes/mado/round13/fetch/host-journal-map-log-sweep.txt`) does not exist in this lane (`git ls-tree -r --name-only HEAD \| grep -c 'lanes/mado/round1[345]/fetch'` → 0), and this round makes no log claim | **refused**; flip if a journal sweep is committed inside the lane |
| `gkeep-rendered-geometry-record-r14.md` | in, journal only | — | a single whole-journal sweep (`S326`, same absent package path) is its entire evidence | **refused**; flip if the sweep is committed under this lane's receipts |
| `gkeep-geometry-never-recorded-r15.md` | in, route | — | one artifacts sweep (`S339`, same absent package path); "never" over a corpus from one sweep is the M43-9 class | **refused**; flip if a lane-committed sweep reproduces it |
| `gkeep-rendered-geometry-chain-r9.md` | in | partly (`fetchClass` is inside the pinned `Window.cpp`, `:1502`) | its chain needs `docs.gtk.org` `set_default_size` and the wiki's window-rules page — neither is a pin — plus two round-9 lane receipts that do not exist here; the successor covers the class-is-app_id link from a pinned file instead | **refused**; flip if both pages are pinned and get rows |
| `gkeep-size-rule-application-r10.md` | in | — | refused in round 43 (`corpus/lessons/round-43.md:46`) for the premise that the client decides the reported size; nothing this round overturns that (the successor shows the client is *told* a hint and acks it, S299/S300) | **no new decision**; the round-43 refusal stands, its re-grounding is corrected in the errata below |
| `gkeep-observation-route-r11.md` | in | — | refused in round 43 (`:48`) as a single-source restatement | **no new decision** |
| `gkeep-geometry-unobservable-r8.md` | in | — | refused in round 43 (`:47`); its flip (a lane row for the host build identity plus a fresh census) is still unfired — S295/S296 hold the rule and a census, not a build identity | **no new decision** |
| `gkeep-element-rules-r30.md` | in, narrowly | its three rule lines are re-grounded as S295 | refusal withdrawn in round 43 (`## Post-data corrections`) because the flip fired — `.ufo/waves/round-43/w1/ExecLiveHost/live-census.txt:232` records `windowrule = size 875 600, match:tag floating-window` (read at the tip; this seat did not re-open the host config); it is still **not adopted**: it has no pinned receipt and no pinned row this round, and its 875×600 explanation rests on a config comment | **not adopted**; first candidate for the next round that pins `apps/system.conf` |
| `glyph-and-geometry-r31.md` | in, but off-theme | — | two themes; the glyph half belongs to the bar theme, and its gkeep half is r12's ground | **not adopted**; residue |
| the staged ids `S203`-`S349` | — | — | collide with the lane's own S203-S297 | id mapping is by document (`assimilation/renumber-map.tsv`), never arithmetic; no package id is carried |

## Registry changes logged old→new (CORPUS.md rule 2)

- **New rows S298-S301** (four; registration reserved S298-S301): S298 `src/protocols/XDGShell.cpp`, S299
  `stable/xdg-shell/xdg-shell.xml` (wayland-protocols 1.49), S300 `gdk/wayland/gdktoplevel-wayland.c` (GTK 4.24.1), S301
  `gkeep/ui.py` (gkeep `133b867`, full file). Kind `code`, tier A, status `mined`, `opened 2026-10-26`,
  `used-by` = `corpus/knowledge/hyprland-gkeep-size-request-r44.md`, `recheck: on-release` (upstream code at a fixed commit).
- **Held row S164** (`corpus/SOURCES.md:176`): `used-by` `corpus/knowledge/rule-attribution-r24.md` →
  `corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/hyprland-gkeep-size-request-r44.md` (one item appended; cells 1-10
  byte-equal). No other held row is edited this round.
- **Old→new for the staged document** (`assimilation/renumber-map.tsv`): staged **S311** (`…/hyprwm/Hyprland/v0.56.2/src/desktop/view/Window.cpp`,
  tag form) → held **S164** (the same document at commit `efb50993…`); nothing of S311 is carried, including its tag-form URL.
  Staged **S312** (`…/VeigaPunk/gkeep/133b867…/gkeep/ui.py`) → new **S301**; held S297 keeps its excerpt row unchanged, so the lane now
  holds the same document twice at different granularity — one row per document would forbid this only if the locations matched, and they
  do not (`SOURCES.md:246` carries a lane path, S301 the upstream URL).
- **Census after the data commit**: `<<L1>>` (`receipts/census-after.txt`; expected identical to `receipts/census-before.txt`, W04 ×7
  (S030, S042, S045, S097, S119, S120, S121) + W01 S277, exit 0 — not re-run by this seat).

## Round-43 closure items (from `corpus/lessons/round-43-verifier-spotcheck.md` §6)

1. **D1, an under-cited refusal reason and a mis-mapped host receipt** (`:97` → M44-1): corrected by the append-only errata below.
2. **D2, S293's title echoes the refuted premise** (`:100` → M44-2): not editable in place (CORPUS rule 2); supersession assigned to `<<L1>>`.
3. **D3, the SKILL.md TILED licence column** (`:102` → M44-3): lands with C1, whose tool docstring narrows TILED to the tiled case.
4. **D4, entry pointers to files that did not exist at the data commit, and an off-by-six locator** (`:104` → M44-4).
5. **D5, the frozen seat count and the published mistake range** (`:106` → M44-5): errata below; round 44's own registration records seat
   counts from `*-results.json` (`registration.md:5`).
6. **D6, open predicate defects** (`:107-108` → M44-6): the C1 predicate is rebuilt (clause b4 state teeth, new selftest cases) and the C2
   clause h rebuilt; what stays open is listed in the row.
7. **D7, no committed axis receipt at the closing tip** (`:109` → M44-7).
8. **Driver:** the duplicate `complete mado round=43` line is driver-side and status-neutral; not mined.
9. **Still open from round 41:** S041 held-row citation, tool ergonomics O1-O5, the `PROVINCE.md:75-76` cite. Status at this round's base:
   still open; no round-44 claim covers them, and this seat did not touch them.

## Mistakes

**M44-1 — a refusal reason named the path that sets the box but not the field the claim is about, and its re-grounding named two of
three receipts.** Class: a decision's reason citing a subset of the links it asserts (the round-41 locator class, in prose). Evidence:
`corpus/lessons/round-43.md:46` refuses r10 with "overturned by the pinned floating-algorithm and window-target path" — S291/S293, the
box path — while the field at issue is `hyprctl clients -j` `size`, which is S294 (`.ufo/waves/round-43/fetch/Hyprland-GeometricMovableAnimated.cpp:19`,
`case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();`) and S158 (`.ufo/waves/round-43/fetch/Hyprland-HyprCtl.cpp:427-429`); the same lesson's ledger row at
`:74` re-grounds staged `S310` as "S295/S296", while S310's own scope line names three things — rule lines, the app request, the client
count — so S297 re-grounds it too. Captured-by: the non-author closure, one round later
(`round-43-verifier-spotcheck.md:97`); no instrument compares a refusal reason against the entry that re-grounds the same file. Fix:
appended erratum E1/E2 below (nothing above is rewritten), and this round's ADMIT carries all five pinned receipts so the reason's ground
is the successor's own citations. Shown able to fail: not shown — this seat wrote no checker for reason-to-receipt coverage; open, and the
first candidate for a `quality/` criterion (<<L1>>).

**M44-2 — a registry row's title states the premise the round refuted, and the row's own teaches cell contradicts it.** Class: a row cell
restating a superseded inference. Evidence: `corpus/SOURCES.md:242` titles S293 "the client's request as input", while the same row's
teaches cell and `.ufo/waves/round-43/fetch/Hyprland-WindowTarget.cpp:70-71` show the target writing `m_box.logicalBox` derived from
the rule's `static_.size` (`.ufo/waves/round-43/fetch/Hyprland-DefaultFloatingAlgorithm.cpp:56`) — the client is the recipient, not the input. Captured-by: round-43 w2
(`corpus/lessons/round-43.md` `## Post-data corrections`, "Registry wording" bullet); CORPUS rule 2 forbids editing cells 1-9 in place, so
the row stands. Fix: supersede S293 (with S290-S292, S296, S297) by corrected rows in a later round — `<<L1>>` names the seat. Shown able to
fail: `grep -n 'the client.s request as input' corpus/SOURCES.md` → one line, the row itself; a supersession keeps that count at 1 by
leaving the old row alone (the check is the new row's title, not a gate).

**M44-3 — the licence column of the tool's own capability row asserted the premise the tool's TILED verdict cannot hold.** Class: a
published support claim broader than the code under it. Evidence: `SKILL.md:276` reads "the tiler, not the floating rule path, set its box",
while for a pseudo-tiled client the size arrives from the stored rule pseudo-size (`fetch/Hyprland-Window.cpp:2402-2408` at the pinned commit,
`round-43.md` `## Post-data corrections` first bullet), which the same row's caveat column already concedes. Captured-by: round-43 w2
`CritEntryInf` F1 (via the closure's D3, `round-43-verifier-spotcheck.md:102`). Fix: C1's landing rewrites that cell, because C1 changes the
tool's docstring and verdicts in the same file — `<<L1>>` confirms it landed. Shown able to fail: `<<L1>>` (the C1 seat's SKILL diff), not
run by this seat.

**M44-4 — an entry cited two seat receipts by bare path before they existed, and a receipt's locator range started six lines past the
block and ended five past it.** Class: a pointer whose target is not committed at the cited revision, plus a typed locator. Evidence:
`git ls-tree -r --name-only 1959770 .ufo/waves/round-43/w1/ExecOracleGkeep/` prints **nothing** (0 files at the data commit) while
`git ls-tree -r --name-only HEAD .ufo/waves/round-43/w1/ExecOracleGkeep/ | grep -cE '20-observation|10-cases'` → 2 at the tip, so
`corpus/knowledge/hyprland-gkeep-geometry-r43.md:66` pointed at files that landed later; and `20-observation.txt:24` cites
`gkeep-shm.c:156-164` for "sets app_id and title, attaches a 200x200 shm buffer and commits", whose block is `:150-159`
(`150` `xdg_toplevel_set_app_id`, `151` title, `157-159` attach/damage/commit, computed with `awk` on
`.ufo/waves/round-43/w1/ExecOracleGkeep/gkeep-shm.c`). Captured-by: round-43's non-author closure (`:104`); no lane instrument resolves a
cited path at a cited revision, and the locator checker scores locators against receipts, not a receipt against its own target. Fix: cite
seat evidence only after it lands (or date the pointer), and compute the range; the round-43 entry is corrected by erratum, not rewritten
(append-only). Shown able to fail: the two commands above, run at this seat's read.

**M44-5 — a frozen registration under-counted its own wave by one, and the published mistake range stopped one short, while the lesson
carried nine.** Class: a count and a range published without a command that recomputes them (the M43-2 class, one round later). Evidence:
`.ufo/waves/round-43/registration.md:5` reads "37 seats", while `git show 5add5b4:.ufo/waves/round-43/w1-spec.json` has 38 items and
`HEAD:.ufo/waves/round-43/w1-results.json` has 38 results; `SCORECARD.md:2548` says "Mistakes M43-1..8" while
`grep -c '^\*\*M43-' corpus/lessons/round-43.md` → 9. Captured-by: the closure's L2-floor row (`round-43-verifier-spotcheck.md:106` §6 D5)
and its step-1 table; nothing recomputes a lesson's mistake count against the SCORECARD. Fix: `registration.md:5` of this round records
seat counts **from** `*-results.json` ("the seat counts are recorded from each wave's `*-results.json`"), and the SCORECARD append for
round 44 is `<<L1>>`. Shown able to fail: the three commands above.

**M44-6 — the round closed with predicate holes it had itself declared, so the next round re-registered both counters instead of building
on them.** Class: declared residuals left as prose, with no kill rule. Evidence: `round-43-verifier-spotcheck.md:107-108` — C1 cheats 4
(source-pin selftest) and 6 (sandbox detection) reach TARGET_MET; C2 v2 admits 14/14 shape-keeping do-nothing controls and 6/16 weakening
mutants survive; `quality/check-locators.py` compares identifiers not numbers and 12/37 mutants survive its selftest. Captured-by: the
lane's own control receipts (`receipts/ctl-c1.txt`, `receipts/ctl-c2-v2.txt`) plus the closure's reading. Fix: `PRED-C1-r44` adds clause b4
(state teeth over >= 6 `fullscreen`-naming sites, >= 75 % must die) and raises the selftest floor to 80, which makes K13 (selftest cases
removed, 26/26 fixtures) fail — `receipts/ctl-c1.txt:17` shows exactly that variant missing on b:0/b4:0; `PRED-C2-r44` rebuilds clause h as
a client-side census computed from the pins. What stays open: C1's cheat 6 (the sandbox is detectable) and C2's do-nothing controls have no
positive control at this freeze (`receipts/ctl-c2.txt:5`) — `<<L1>>` records what w1's `CritC2Cheat`/`ExecC2Positive` and
`ExecC1ExtraMutants` found.

**M44-7 — the round's own closing publication had no committed axis receipt at its tip.** Class: a published statement read from a
write-time run (the M43-6 class). Evidence: at the closing tip `5846662`, the committed axis logs stop at
`.ufo/waves/round-43/w2/ExecHarmTip/logs/tip-2a3707c-axis.log:4` (`mismatched=0 rev=2a3707c…`); `git grep -n 'MADO_AXIS:' 5846662 --
.ufo/waves/round-43/w2/ExecHarmTip/logs/` lists base, data (`mismatched=2`), `2a3707c` and `a47efeb` (`mismatched=2`), none at
`5846662`. Captured-by: the closure (`:109`). Fix: this round commits an axis receipt at the base (`receipts/axis-base.txt`, three MATCH
rows) and at the tip — `<<L1>>`, w2's `ExecHarmTip`. Shown able to fail: the `git grep` above (0 hits for the closing tip's rev).

**M44-8 — the round-43 tool shipped a verdict for a state it never read, so it called a fullscreen window DIFFER and a maximized one
OK.** Class: a capability shipped without a falsifier for the field that decides its answer (a false report, not a missing feature).
Evidence, run by this seat on committed bytes and a two-client fixture (`c1-demo/`, hashes beside each file): the base tool
(`git show 6a1a905:tools/mado-geometry.py`, sha256 `e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99`) given
`floating: true, size: [2560,1440], fullscreen: 2` prints
`MADO_GEOM_CLIENT: … floating=true size=2560x1440 want=420x500 float_rule=- verdict=DIFFER` and exits 1
(`c1-demo/out2-base-tool.py-1.txt`), and given `floating: false, size: [2544,1380], fullscreen: 1` prints `verdict=TILED` with the
top-level `MADO_GEOMETRY: … verdict=OK` and exit 0 (`c1-demo/out2-base-tool.py-2.txt`) — a false report and a false clearance for the two
sizes Hyprland itself imposes (`fetch-c1/Hyprland-FullscreenHandler.cpp:191-199`); the frozen reference
(`.ufo/waves/round-44/c1/ctl-ref-tool.py.txt`, sha256 `8e871a00fcf1a615e3683ebe5204f67cfe679182ff15d008b83fed34131c788d`) prints
`verdict=FULLSCREEN` / `verdict=MAXIMIZED` and ` maximized=0 fullscreen=1` / ` maximized=1 fullscreen=0`, exit 0
(`c1-demo/out2-ref-tool.py-1.txt`, `-2.txt`). Round 43 had no falsifier for the field: `PRED-C1-r42`'s fixtures never varied `fullscreen`
and the tool's docstring lists only BADSIZE | TILED | AGREE | DIFFER. Captured-by: **none in round 43** (found by reading the pinned
`HyprCtl.cpp` for this round's registration, `registration.md:14-16`); from this round, `PRED-C1-r44` clause f's lattice and clause b4 —
`receipts/c1-before-base.txt:29` `clauses=a:1 b:0 b4:0 g:1 r:1` and `:30` `fixtures=12/26`, and the do-nothing BASE-tool control
`receipts/ctl-c1.txt:3` `fixtures=13/26 … TARGET_MISSED`. Fix: C1's re-registration (`PRED-C1-r44`) plus the tool's contract extension;
whether a live maximized or fullscreen window reports the work-area or monitor box stays the compositor's fact, not a scored claim
(counter docstring, "Residuals"). Shown able to fail: the four runs above discriminate — same input, opposite verdicts.

## Round-43 errata (appended; nothing in `corpus/lessons/round-43.md` is rewritten)

- **E1 (D1a).** `corpus/lessons/round-43.md:46` — the r10 refusal's ground is S291/S293 (the box path). Corrected reading: the reported
  field is `hyprctl clients -j` `size`, which is S294 (`Hyprland-GeometricMovableAnimated.cpp:19`,
  `case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();`) read out by S158 (`.ufo/waves/round-43/fetch/Hyprland-HyprCtl.cpp:427-429`); the refused premise is
  refuted by those two as well as by the box path. The flip's phrase "the reported size" is to be read as "the `size` field of
  `hyprctl clients -j`", not as `CWindow::getReportedSize()`, which on Wayland returns `m_current.ackedSize`
  (`fetch/Hyprland-Window.cpp:1861-1866`, stored by `onAck` at `:1526`) — both halves are S164 here.
- **E2 (D1b).** `corpus/lessons/round-43.md:74` re-grounds staged `S310` as "S295/S296". Corrected: S310's scope line names rule lines,
  the app request and the client count, so the re-grounding is **S295/S296/S297** — the rule file, the census, and the gkeep excerpt.
- **E3 (D5).** `.ufo/waves/round-43/registration.md:5` under-counts its own wave ("37 seats"): 38 seats ran
  (`git show 5add5b4:.ufo/waves/round-43/w1-spec.json` → 38 items; `HEAD:.ufo/waves/round-43/w1-results.json` → 38 results), which
  `corpus/lessons/round-43.md` already discloses. `SCORECARD.md:2548` says "Mistakes M43-1..8" while the lesson carries nine:
  `grep -c '^\*\*M43-' corpus/lessons/round-43.md` → 9. A SCORECARD edit is outside this seat's write scope; `<<L1>>` applies it, and
  round 44's SCORECARD append should read the count off that same grep.
- **E4 (the routed defect's own locator).** The closure routes D1 as "`round-43.md:75`"; the r10 `REFUSE` line is at `:46` and `:74-75` is
  the ledger row that re-grounds S310 (`grep -n 'REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-size-rule-application-r10.md'
  corpus/lessons/round-43.md` → 46). The D1 substance stands; its locator is the M44-1 class again, one layer up, which is why E1/E2 cite
  computed line numbers.

## Spot-check (non-author closure; placeholders)

| check | command | expected |
|---|---|---|
| lesson landed, unfenced, Gate section complete | `grep -c '^## Gate' corpus/lessons/round-44.md`; `grep -c '^GATE S' corpus/lessons/round-44.md` | 1; 5 |
| every GATE quote re-opened in its receipt | recompute `sha256sum`; locate each quote word-bounded; confirm it is absent from the other four pins | (closure) |
| each new row's location unique, `opened 2026-10-26`, `used-by` names the entry | `grep -nE '^\| S(29[89]\|30[01])\b' corpus/SOURCES.md`; `sources-census.sh validate` | (closure) |
| S164's row edited in `used-by` only | `git diff <base> <tip> -- corpus/SOURCES.md` | one appended item, cells 1-10 byte-equal |
| C1 at the data commit and the tip | `python3 -I quality/counters/c1-r44-geometry-states.py --repo . --rev <rev> --work <scratch>` | `fixtures=26/26 … TARGET_MET`, exit 0; and clause r still `37/37` |
| C2 at the data commit and the tip | `python3 -I quality/counters/c2-r44-gkeep-size-request.py --repo . --rev <rev>` | `admitted=1/1 … TARGET_MET`, exit 0 |
| admission decisions re-read against the package | re-open the five ADMIT/REFUSE files in `merge/mado/knowledge/corpus/knowledge/` | (closure) |
| axis + harm at the tip | `MADO_AXIS …`, the two counters, `--selftest` of the tool | (closure) |
| the C1 finding's four fixtures still discriminate | re-run `c1-demo/commands.txt` against base and reference bytes | DIFFER/TILED (base) vs FULLSCREEN/MAXIMIZED (reference) |

## Census and measurements

- C1 at base: `receipts/c1-before-base.txt` (`fixtures=12/26 tool=present verdict=TARGET_MISSED`, exit 1). At the data commit / tip:
  `<<L1>>` (`receipts/c1-after-data.txt`, `receipts/c1-after-tip.txt`).
- C2 at base: `receipts/c2-before-base.txt` (`admitted=0/1`, exit 1). At the data commit / tip: `<<L1>>`.
- Controls at the freeze (evidence-verified as bytes by this seat for the two verdict lines only, not executed): `CTL_C1 VERDICT: PASS
  (controls scoring TARGET_MET: 0 of 15; reference met: 1)` (`receipts/ctl-c1.txt:18`, with REF `26/26` at `:2`); `CTL_C2 VERDICT: PASS
  (controls scoring TARGET_MET: 0 of 3)` (`receipts/ctl-c2.txt:5`) — **no positive control exists for C2** at the freeze.
- The two census lines the entry must carry, recomputed here from the pins with the counter's own parsing rules:
  `gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep` (one `set_default_size`, zero
  `set_size_request(`, one `application_id=`) and `hyprland sendWindowSize xdg_setSize=1 x11_configure=1` (the body spans
  `fetch/Hyprland-Window.cpp:1732-1754`: one `->setSize(`, one `->configure(`). `<<L1>>` confirms the counter's `clause=h` line at the data commit.
- Registry rows 234 → 238 (S298-S301); knowledge entries `<<L1>>` (+1, the entry); one `corpus/README.md` index row for the entry
  (clause f) — `<<L1>>`.
- The live host receipt is reported, not scored: a gkeep window was not open during this round's w1 (`hyprctl clients -j` is the read that
  would answer it, and `tools/mado-geometry.py` reports FULLSCREEN/MAXIMIZED instead of inventing DIFFER/TILED once C1 lands) — `<<L1>>` for w2's
  `SentLiveReads`.
- Tools installed by this seat: **none**. Scratch: `/fast/scratch/hyaku/mado-r44/ScrLessonSkeleton/` (deleted before this report;
  the citable copies are in `w1/ScrLessonSkeleton/c1-demo/`).

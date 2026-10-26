# ScoutStagedGkeep survey — the 11 staged gkeep-theme files vs the lane and the round-43 pins

Seat ScoutStagedGkeep, mado round 43 w1, 2026-10-26. Read-only walk (no tool run in the package, no compositor call).
Read: the 11 staged files (`/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/`), `MERGE-REPORT.md`,
`SOURCES.append.md` (the rows they cite), `PROVINCE.md`, `corpus/QUALITY.md`, `corpus/README.md`, the 10 pinned receipts
(`.ufo/waves/round-43/fetch/`, `sha256sum -c ../receipts/fetch-sha256.txt` -> 10/10 OK), `quality/counters/c2-r43-gkeep-entry.py`
(PINS, STAGED, BAD_LOC, clauses d, g, h, i). Axes named: correctness (a claim survives the pinned bytes), sourcedness
(public URL at a tag vs a private receipt the package does not carry), supersession, province fit, counter-compatibility.

## 0. Facts that decide the ranking (each re-derived here)

1. **The package carries no private receipts.** `find /home/vgpnk/Projects/shokuknow/merge/mado -name 'host-gkeep*' -o -name 'host-focus-grab-and-timeout*'`
   -> empty; there is no `lanes/` tree. Every `lanes/mado/roundN/fetch/...` row (S275, S292, S293, S299, S310, S320, S326, S339) is a private
   own-work row whose bytes cannot be re-opened by any seat. Only a re-capture (S297/S298/S299 of this round) can replace them.
2. **The counter's PINS contain no `Window.cpp`.** PINS = the 10 files above. Clause d: a NEW id's receipt must be one of them, so an entry
   *cannot* cite `src/desktop/view/Window.cpp` this round. Staged quotes that live in Window.cpp (`fetchClass`, `readStaticRules(true)`,
   `setPseudoSize`, `REPORTSIZE`, `sendWindowSize`, `onAck`, the `Map request dispatched` log line) are therefore not admissible this round
   (verified by grep below: 8 of 8 absent from every pinned receipt).
3. **Staged ids collide with the lane's.** Lane registry = 226 rows (S001..S289); staged S203-S349 reuse ids (lane S219 = `mado-options` row
   at SOURCES.md:225; staged S219 = omarchy hypridle.conf). Staged rows cannot be appended; new rows are S290-S299 (pinned) / S300+.
4. **`glyph-and-geometry-r31.md` cites two dangling ids.** It says "round 5's row S219" for the host rule and "round 5's row S216" for the
   weather producer. Staged S219 is `hypridle.conf` (SOURCES.append.md:23), staged S216 is a **Chinese CSDN blog row**
   (SOURCES.append.md:20, `blog.csdn.net/...`, tier C) - the host rule is S251 in the package. So r31's §2 prose points at the wrong row
   and its §1 basis leans on a localized-channel row (PROVINCE.md Round-36 refinement: localized-documentation channel is outside).
5. **The two "settled/derived" readings in the chain are inconsistent with each other and with the pinned bytes.** Round 10 says the rule only
   *requests* (pseudo size), round 11 says it *imposes* (settled), round 12 says the client is *asked*, round 13 says "the client cannot
   substitute". Each amends the previous without a stable end state; r11's own §2 says r9 "right number, wrong who decides" and r10 "wrong
   direction". Pinned bytes qualify r11 further (§3 below): the rule size is applied **only on first map** and is an **expression**.
6. **The "lane cannot observe" premise is stale.** r8 (3 clients: two Alacritty + zcode), r13 §4 and r14 §3 ("the lane may not connect the
   compositor socket") predate this round's allowed read verbs; pinned `host-clients-r43.json` has 4 clients (Alacritty, zcode, grok-bot,
   chromium), all size `[1720, 1414]`, all `floating:false`, 0 gkeep. "No window open" still holds; "cannot be observed" does not.

## 1. Verification of staged quotes against the pinned receipts (grep, whitespace-normalised, run this seat)

Script: normalise whitespace in each receipt, `qn in receipt`; locator = first line of the quote. 24 staged quotes tested.

| staged file | quote (<= 25 words, truncated by `...`) | pinned receipt:line | verdict |
|---|---|---|---|
| r10 | `case WINDOW_RULE_EFFECT_SIZE: {` | Hyprland-WindowRuleApplicator.cpp:421 | FOUND |
| r10 | `bool CWindowRuleApplicator::readStaticRules(bool preRead) {` | Hyprland-WindowRuleApplicator.cpp:483 | FOUND |
| r11 | `if (WINDOW->m_ruleApplicator->static_.size) {` | Hyprland-DefaultFloatingAlgorithm.cpp:55 | FOUND |
| r11 | `windowGeometry.w = COMPUTED->x;` | Hyprland-DefaultFloatingAlgorithm.cpp:60 | FOUND |
| r11 | `target->setPositionGlobal(windowGeometry);` | Hyprland-DefaultFloatingAlgorithm.cpp:96 (the same line recurs at :102, so a counter locator must name the line) | FOUND |
| r11 | `void ITarget::setPositionGlobal(const STargetBox& box, uint8_t) {` | Hyprland-Target.cpp:10 | FOUND |
| r11 | `m_box = box;` | Hyprland-Target.cpp:11 | FOUND |
| r11 | `m_window->setBox(m_box.logicalBox);` | Hyprland-WindowTarget.cpp:71 | FOUND |
| r11 | `const bool  CONFIGURECLIENT = !(flags & TARGET_UPDATE_NO_CLIENT_CONFIGURE);` (double space) | Hyprland-WindowTarget.cpp:50 | FOUND (normalised) |
| r11 | `void CGeometricMovableAnimated::setBox(const CBox& x) {` | Hyprland-GeometricMovableAnimated.cpp:43 | FOUND |
| r11 | `*m_realSize     = x.size();` | Hyprland-GeometricMovableAnimated.cpp:45 | FOUND (normalised) |
| r9/r11/r30 | `windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$` | host-gkeep.conf:4 | FOUND |
| r11/r30 | `windowrule = float on, match:class ^(org.omarchy.gkeep)$` | host-gkeep.conf:2 | FOUND |
| r30 | `# gkeep — local post-it. No floating-window tag: Omarchy sizes that tag at 875×600.` | host-gkeep.conf:1 | FOUND |
| r9/r11/r31 | `window.set_default_size(420, 500)` | gkeep-ui-excerpt.py:33 (host ui.py:476) | FOUND |
| r9 | `application_id="org.omarchy.gkeep",` | gkeep-ui-excerpt.py:6 (host ui.py:449) | FOUND |
| r12 | `window = Gtk.ApplicationWindow(application=self, title="gkeep")` | gkeep-ui-excerpt.py:31 | FOUND |
| r10 | `m_ruleApplicator->readStaticRules(true);` | - | ABSENT (Window.cpp not pinned) |
| r10 | `m_target->setPseudoSize(*COMPUTED);` | - | ABSENT (Window.cpp) |
| r10 | `const auto  REPORTSIZE = m_realSize->goal().clamp(...)` | - | ABSENT (Window.cpp); the pinned route to the same variable is HyprCtl.cpp:427-428,:448 `w->size(GEOMETRIC_GOAL)` -> GeometricMovableAnimated.cpp:19 `return m_realSize->goal();` |
| r12 | `void CWindow::sendWindowSize(bool force) {` | - | ABSENT (Window.cpp) |
| r13 | `void CWindow::onAck(uint32_t serial) {` | - | ABSENT (Window.cpp) |
| r13 | `Map request dispatched, monitor {}, window pos: {:5j}, window size: {:5j}` | - | ABSENT (Window.cpp) |
| r9 | `return m_xdgSurface->m_toplevel->m_state.appid;` | - | ABSENT (Window.cpp) |
| r12 | absence claim "no `set_size_request` in the file" | excerpt is only lines 446-488; `grep -n set_size_request /home/vgpnk/Projects/gkeep/gkeep/ui.py` = 0 hits (host copy, 488 lines, sha256 07a3c4a5...e66a, HEAD 133b867); `min-width`/`min-height` at ui.py:87-88 sit in `button.ink` (lines 80-90) | NOT re-groundable from the 45-line pin; true on the host file |

Result: 17 FOUND, 8 ABSENT (all 8 are Window.cpp), 1 absence claim unprovable from the excerpt. Staged r11's five upstream quotes and its two
host-side quotes re-ground fully in the pins; r9/r10/r12/r13 are partly or wholly outside the pins.

What the pins add that **no staged file says** (so the successor entry is a synthesis, not a copy):
- RE2: `Hyprland-RegexMatchEngine.cpp:7-8` (`negative:` prefix), `:16` (`re2::RE2::FullMatch(other, *m_regex) != m_negative`): staged grep for
  `FullMatch|negative:|RE2|GEOMETRIC_GOAL|firstMap|calculateExpression|lastFloatingSize` over the 11 files -> empty.
- `hyprctl clients -j` `size` is `w->size(GEOMETRIC_GOAL)` (HyprCtl.cpp:427-428, :448) = `m_realSize->goal()` (GeometricMovableAnimated.cpp:19):
  the animation goal, not the current value (`GEOMETRIC_CURRENT` at :20 = `value()`); staged r10 used a different Window.cpp variable.
- Floating algorithm qualifiers r11 omits: size applied only inside `if (target->window() && target->window()->m_firstMap)` (DefaultFloatingAlgorithm.cpp:49),
  else `lastFloatingSize()` is used (:85-87); `static_.size` is an expression (`std::get<Math::SExpressionVec2>`, WindowRuleApplicator.cpp:422) evaluated by
  `calculateExpression` with an `ERR` log and **no** size on parse failure (DefaultFloatingAlgorithm.cpp:56-58); `center on` (`static_.center`, :79) re-positions after size; `setPositionGlobal` rounds
  the box (Target.cpp:12-13); the push to the window happens in `updatePos` floating branch (WindowTarget.cpp:70-71) with `sendWindowSize()` behind
  `CONFIGURECLIENT` (:50, :73-74) - `sendWindowSize` itself is Window.cpp (unpinned).

## 2. Per-file table

Columns: claim; sources = public (P: URL at a tag) / private (V: `lanes/mado/roundN/fetch/...`, not in package) / host file (H); re-grounded by pins;
superseded by; PROVINCE; rank (1 = most valuable to the successor). Round numbers are the staged `corpus-expansion` rounds.

| rank | staged file | claims | sources | re-groundable by pins S290-S299 | superseded by | PROVINCE / QUALITY fit | disposition |
|---|---|---|---|---|---|---|---|
| 1 | `gkeep-size-to-real-size-r11.md` | rule size reaches `m_realSize` via floating algo -> target box -> window; "settled at 420x500" | P: S302, S303, S304, S305 (all v0.56.2, `src/layout/...`, `src/desktop/view/types/...`); V: S310 | **Yes, fully**: S292 (DefaultFloatingAlgorithm), S293 (Target), S294 (WindowTarget), S295 (GeometricMovableAnimated), S297 (host-gkeep.conf) - 7 of 7 quotes FOUND | none by a later file (r12/r13 extend, do not replace); but its "settled"/"cannot decline" wording overreaches (first-map-only, expression, no sendWindowSize) | IN: window rules of `~/.config/hypr/` (PROVINCE.md:6); source-read knowledge precedent = `request-socket-live-bound-r8`, `hyprland-focus-grab-r41` | **ADMIT (spine)** |
| 2 | `glyph-and-geometry-r31.md` §2 only | "window's size is agreed twice": app `set_default_size(420, 500)` + host rule `size 420 500`; the rule does not correct a mismatch; the 875x600 comment is about another window | P: S255 (gkeep ui.py @133b867); S256 (Nerd Fonts) for §1; cites "round 5's row S219/S216" = dangling (§0.4) | §2: yes - excerpt:33 + conf:4 + conf:1 (census clause h verifies the 420x500 agreement itself) | amends r30's work-around reading; r11 restates the agreement | §2 IN (host rule + app request). §1 glyph half OUT of theme and rests on S216 (Chinese CSDN blog = localized channel, PROVINCE Round-36) | **ADMIT (§2 only, as a corrected reading of r30)** |
| 3 | `gkeep-element-rules-r30.md` | three rules float/centre/size by class, applied in order; size is a "work-around" for the desktop's 875x600 tag | H: S251 (`~/.config/hypr/gkeep.conf`, host file read 2026-10-23) | rules text: yes (host-gkeep.conf:1-4; `center on` at :3 which r30 states but never quotes). Work-around inference: **no** - the comment says gkeep has *no* floating-window tag, so the tag's 875x600 never applied; r31 says so | r31 §2 amends the inference; the rule triad is superseded by the 2026-10-26 re-capture S297 | IN (hypr rules). Quality: inference-from-comment violates criterion 15 (label inference by layer) | **ADMIT (rule triad only; drop the work-around inference)** |
| 4 | `gkeep-rendered-geometry-chain-r9.md` | class = Wayland app_id (`fetchClass`), app_id matches the rule regex, 420x500 "by agreeing mechanisms" | P: S284 (Window.cpp fetchClass), S285 (ui.py), S286 (GTK docs), S287 (wiki 0.56.0 Window-Rules); V: S292, S293 | partly: app_id/regex data match via excerpt:6 + conf:4 (+ counter clause h `re.fullmatch`); `fetchClass` (Window.cpp) **not pinned**; S286/S287 wiki/GTK pages not pinned | §3 "420x500 for a reason" superseded by r11 §2 (r11 says r9 had the wrong decider); §4 annotation (app_id undocumented) is a docs-absence claim, Window.cpp-only | IN | **REFUSE** |
| 5 | `gkeep-client-size-request-r12.md` | compositor asks the client via `xdg_toplevel.set_size` (`sendWindowSize`, `m_pendingSizeAcks`); gkeep has no `set_size_request`, so nothing refuses | P: S311 (Window.cpp), S312 (ui.py, same URL as S255/S285 - triple row) | gkeep half only, and only partly: excerpt (lines 446-488) lacks the whole-file absence claim; Window.cpp half absent | extends r11; its header self-references (`gkeep-client-size-request-r12.md's predecessor`) - a header defect | IN (but the app is operator project; chain evidence only, config-drift-r12.md:109) | **REFUSE** |
| 6 | `gkeep-size-rule-application-r10.md` | rule is a pseudo-size *request*; client reports what it used (`REPORTSIZE`) | P: S297 (WRA, pin S291), S298 (Window.cpp); V: S299 | WRA quotes yes (:421, :483); `readStaticRules(true)`, `setPseudoSize`, `REPORTSIZE` no | **explicitly wrong direction** per r11 §2 | IN | **REFUSE** |
| 7 | `gkeep-observation-route-r11.md` | restates rule lines + request + "gkeep clients: 0"; expected value 420x500 | V: S310 only | restated by S297/S299/S298 (host-gkeep.conf, excerpt, host-clients-r43.json) | superseded by r11 and by this round's census (4 clients, gkeep=0) | no new claim | **REFUSE** |
| 8 | `gkeep-geometry-unobservable-r8.md` | rendered geometry cannot be observed; 3 clients; build identity | V: S275 (binary census) | build identity not in a pin; 3-client census stale (now 4) | superseded by r9..r11 and by `hyprctl clients -j` being an allowed read verb | IN | **REFUSE** |
| 9 | `gkeep-rendered-geometry-record-r13.md` | `onAck` reconciliation; DEBUG-level `Map request dispatched` line; journal has 0 of it | P: S318, S319 (Window.cpp); V: S320 (journal sweep) | none (all Window.cpp + private journal) | r14 widens the sweep; both rest on a volatile journal | IN (compositor behaviour) but unpinned, and "lane may not connect the socket" is stale | **REFUSE** |
| 10 | `gkeep-rendered-geometry-record-r14.md` | whole-journal sweep: 0 of 140496 lines; app store holds no geometry | V: S326 only | none; journal count is a point-in-time measurement (`recheck: on-log-rotation`) | supersedes r13's scope; itself a negative measurement | IN (borders on tsukuroi's journal ground) | **REFUSE** |
| 11 | `gkeep-geometry-never-recorded-r15.md` | the lane's round-24 artifacts never held a gkeep observation | V: S339 (lane artifact grep) | none; a sweep of the lane's own old `.bin` artifacts is lane bookkeeping, not desktop knowledge | none | weak: self-referential bookkeeping about the lane's own history | **REFUSE** |

(r31's §1 glyph claim and its S256 row are refused with the rest of the glyph half: out of the geometry theme; `weather-glyph-render-r7` is a separate
staged theme, and §1's basis points at S216, a localized-channel row.)

## 3. The single best admit set for ONE successor entry (`corpus/knowledge/hyprland-gkeep-geometry-r43.md`)

**ADMIT set** (three `ADMIT <staged path> as corpus/knowledge/hyprland-gkeep-geometry-r43.md` lines; counter clause i needs >= 1):

1. `gkeep-size-to-real-size-r11.md` - the spine (rule -> floating algorithm -> target box -> window real size -> the animated variable).
2. `glyph-and-geometry-r31.md` (§2 only, "the window's size is agreed twice"; the glyph §1 is dropped) - the app-request half and the corrected
   reading of the 875x600 comment.
3. `gkeep-element-rules-r30.md` (the rule triad only; the work-around inference dropped) - the host rule text.

**Why this set is best:** it is exactly the staged content that (a) rests on public source at the host's tag **and** (b) lands on a pinned
receipt: S292-S295 + S297 + S299. Nothing else of the 11 files is both. Every other file leans on `Window.cpp` (not in PINS, clause d) or on a
private receipt the package does not carry. The successor then adds what no staged file has: RE2 `FullMatch`/`negative:` (S290,
RegexMatchEngine.cpp:7-8,:16), the `clients -j` size = `GEOMETRIC_GOAL` (S296, HyprCtl.cpp:427-428,:448; S295 :19), the `m_firstMap` /
expression qualifiers (S292 :49,:85-87; S291 :422), and today's host census (S298: 4 clients, 0 gkeep; clause h lines).

**Corrections the entry must carry** (the spine's staged wording must not be copied):
- r11's "settled"/"the client cannot decline" is not supported by the pins: the rule size applies only when `m_firstMap` (S292 :49), else
  `lastFloatingSize` (:85-87); the value is an expression (S291 :422) evaluated by `calculateExpression` and a parse failure logs `ERR` and applies no
  size; `sendWindowSize` and the client's acknowledgement are in Window.cpp (unpinned) -> label that link `[UNK]` with the unpinned file named.
- r30's work-around reading is wrong in kind: the comment (host-gkeep.conf:1) says gkeep is *not* tagged; r31 §2 states the correction.
- `class` = Wayland `app_id` is not re-derived (`fetchClass` is Window.cpp); the entry states only the data-level match: counter clause h
  (`application_id` fully matches the rule regex via `re.fullmatch`, excerpt:6 vs conf:2-4) and labels the compositor's class source `[UNK]`.
- `hyprctl clients -j` reports the animation goal; no gkeep client exists (S298), so no observed size exists: `[UNK]` observation, `[INF]` derivation.

**Row/id plan** (staged ids not used): S290 RegexMatchEngine, S291 WindowRuleApplicator, S292 DefaultFloatingAlgorithm, S293 Target, S294 WindowTarget,
S295 GeometricMovableAnimated, S296 HyprCtl, S297 host-gkeep.conf, S298 host-clients-r43.json, S299 gkeep-ui-excerpt.py (10 new rows, 3 own-work
= clause h census; >= 4 distinct `source:` lines in the first 20 lines).

## 4. Refusals with reason and flip condition (counter clause i: `REFUSE <staged path> reason=<>= 4 distinct words>`)

Clause i also requires the REFUSE target to differ from every ADMIT target. Suggested lesson lines:

| staged path | reason (>= 4 distinct words) | flip condition |
|---|---|---|
| `gkeep-geometry-unobservable-r8.md` | superseded by the later chain; 3-client census stale; unobservable premise overturned by allowed read verbs | none (historical); would flip only if a later entry needs the build-identity line, then re-capture `hyprctl version` as an own-work row |
| `gkeep-rendered-geometry-chain-r9.md` | decider claim corrected by r11; fetchClass quote lives in unpinned Window.cpp; wiki and GTK pages unpinned | pin `Window.cpp` at v0.56.2 + the 0.56.0 Window-Rules page and GTK doc as receipts; then admit §2 (class = app_id) as its own claim |
| `gkeep-size-rule-application-r10.md` | explicitly wrong causal direction per r11; three quotes live in unpinned Window.cpp | none (contradicted); the readStaticRules(true)/pseudo-size path flips only with Window.cpp pinned, as a *separate* sourced claim |
| `gkeep-observation-route-r11.md` | restates r11 plus one private receipt; no new claim; census stale | none |
| `gkeep-client-size-request-r12.md` | sendWindowSize quotes in unpinned Window.cpp; whole-file no-set_size_request absence not provable from a 45-line excerpt | pin Window.cpp AND a whole-file `ui.py` receipt (host sha256 07a3c4a5...e66a, 488 lines) in a later round; clause d then cites both new ids |
| `gkeep-rendered-geometry-record-r13.md` | onAck and map-log quotes in unpinned Window.cpp; private journal receipt | pin Window.cpp, and re-capture the journal grep with its controls as an own-work receipt (the package does not hold S320) |
| `gkeep-rendered-geometry-record-r14.md` | single private journal sweep; point-in-time count; borders on tsukuroi's journal ground | re-capture the whole-journal sweep with INFO/DEBUG controls as an own-work receipt, and a tsukuroi route confirmation |
| `gkeep-geometry-never-recorded-r15.md` | private lane-artifact grep; lane bookkeeping, not desktop knowledge; unreproducible absence | none unless a gkeep window is ever observed (then the absence is moot) |

## 5. Risks the L1 should weigh

- **Counter, clause i/d/g interplay with partial ADMITs.** `ADMIT` lines name whole staged files; admitting r31 and r30 *partially* is the
  lesson's prose (`## Gate` ledger), not a counter distinction. If the L1 wants zero ambiguity, ADMIT r11 alone satisfies clause i; the other two
  are recommended for content (app request and rule triad are re-grounded by S297/S299 anyway, so they could equally be recorded as "re-captured,
  not copied"). My ranking: r11 mandatory; r31/r30 optional lineage lines.
- **QUALITY criterion 16**: wiki/doc pages cannot be promoted to host facts - the entry's `[INF-docs]` items (none are pinned) stay out; the
  entry's host facts all come from the three own-work receipts and the six source receipts.
- **The excerpt header** (`446-488 (end of file)`) and the 2 re-captured own-work pins were verified: `sha256sum -c` 10/10 OK; ui.py host lines
  449/476 = excerpt lines 6/33 (excerpt starts at 446: 449-446+1 = 4, +2 header lines = 6; 476-446+1 = 31, +2 = 33).
- **Anything in this survey is a plan, not evidence** until the executor re-opens the receipts it cites.

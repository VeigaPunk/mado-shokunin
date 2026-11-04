# R77RevBytes — byte-fidelity audit (round 77, read-only)

Audit tip: `8722d564` (2026-11-04). Instruments last changed at `0fa69f41`
(`tools/mado-barfoot.py`) and `4a17b31f` (`quality/counters/c2-r77-runbook.py`); both
changes landed *during* this audit. Freeze revs audited: `e4717a1c`, `a83e9bee`,
`94b5afb1`, base `aeeef067`. No file was edited. The only writes are this report,
`evidence/` beside it, and a scratch dir that was deleted.

Method: re-fetch/recompute every cited byte and compare sha256 against the pinned
trees (`/fast/scratch/hyaku/mado-r77/l1-src`, Hyprland `v0.56.2 @ efb5099`,
Waybar tag `0.15.0 @ 90b209ad`), re-fetch S463 live, run the committed tools
read-only against the committed captures, and check every quoted sentence
mechanically against its anchor. Evidence copies: `evidence/` (this dir).

## Verdict in one paragraph

The seven source fetches are byte-identical to the pinned trees / installed page,
and the live captures and the live join re-derive exactly. The quoted sentences
break down as: 3 exact byte substrings (S457, S459, and S458 at its second
occurrence line 302), 3 verbatim only after whitespace normalization (S458 at the
anchored lines, S460, S462), 1 verbatim only after roff rendering (S461), and 1
fabricated title string (the lesson's S463 quote). The material claim-level
defects are: the tool-ledger exit map in `SKILL.md:743` puts `NOT_MODELLED` under
exit 0 while the tool exits 3; the tool docstring's "refused, never guessed"
covers `mode` presets and static `addreserved` bands that no code path refuses
(demonstrated: a `mode: hide` config scores `CLEAN` against a top-level capture);
and two entry sentences attribute a Waybar action to a `Renderer.cpp` anchor where
it does not occur. Two instruments were rewritten mid-wave (tool and C2 counter);
the pre-wave receipts' hashes are therefore stale relative to the tip, though both
counter contracts re-derive unchanged.

## 1. Byte ledger — all fetches clean

| id | fetch | sha256 | compared against | result |
|---|---|---|---|---|
| S457 | `fetch/S457.bin` | `9af8a74e…` | `Hyprland/src/render/Renderer.cpp` @ efb5099 | SAME |
| S458 | `fetch/S458.bin` | `798b7c6c…` | `Hyprland/src/debug/HyprCtl.cpp` | SAME |
| S459 | `fetch/S459.bin` | `0a52e145…` | `Hyprland/src/desktop/reserved/ReservedArea.cpp` | SAME |
| S459 | `fetch/S459.hpp.bin` | `6222d114…` | `…/desktop/reserved/ReservedArea.hpp` | SAME |
| S460 | `fetch/S460.bin` | `87e0b9c8…` | `Hyprland/protocols/wlr-layer-shell-unstable-v1.xml` | SAME |
| S461 | `fetch/S461.bin` | `3972caaf…` | `/usr/share/man/man5/waybar.5.gz` (installed 0.15.0) | SAME |
| S461 | `fetch/S461.txt` | `d59c4651…` | gzip decompression of `S461.bin` (15,070 B) | SAME |
| S462 | `fetch/S462.bin` | `120eb913…` | `Waybar/src/bar.cpp` @ 0.15.0 | SAME |
| S463 | `fetch/S463.bin` | `6a3f6683…` | live re-fetch of the page, 147,036 B, 2026-11-04 | SAME |

Tree pins: `git -C Hyprland rev-parse HEAD` = `efb5099378…`, `git describe` = `v0.56.2`;
`git -C Waybar describe --exact-match` = `0.15.0`, HEAD `90b209add8…`; both worktrees clean.
S461 is the **installed rendered page**, not the repo's `man/waybar.5.scd.in`
(12,834 B, sha `3407241d…`, a different document); the row's path column says so.

Live captures: `live-layers-r77.json` `46eb2481…`, `live-monitors-r77.json`
`e732af34…` — equal to the working files, the receipt lines, and the blobs committed
at `e4717a1c`.

Live join: a fresh run at the tip with the host config and the committed captures
prints the five `MADO_BARFOOT_*` lines byte-identically to
`receipts/pre-wave-evidence-r77.txt` (block sha256 `16829379…`), rc 0. The frozen
tool (`409e78a4…`) and the hardened tip tool (`61f34022…`) both do.

Counters, re-derived rather than read:

- `c1-r77-barfoot.py` at `a83e9bee` and at the tip: `cases=15 correct=15 mutants=5
  killed=5 base_correct=8/15 tool_selftest=18/18 verdict=TARGET_MET` rc 0
  (tip line carries `tool_sha256=61f34022…`); selftest 15/15.
- `c2-r77-runbook.py` at the tip in this session shell **and** in `env -i` with only
  `PATH`/`HOME`: `cases=12 executed=12 matched=12 unexecuted=0 anchors=12/12` rc 0;
  selftest 9/9.
- `mado-barfoot.py --selftest`: 18/18, rc 0.
- Control-set sha256 still `7d6e2b1a…` (C1) and `597b2302…` (C2); C1 counter blob
  still `ae5d27e7…`.

## 2. Findings

Severity is about byte/claim integrity, not about whether the round's counts hold
(they do). Nothing here was edited.

### F1 — HIGH — `SKILL.md:743` states the wrong exit code for `NOT_MODELLED`

The ledger row for `mado-r77-barfoot` says:

> `0 CLEAN (box MATCH and reserved EQ/GT/NOT_APPLIED/NOT_MODELLED); … 3 not formed
> (NO_LAYER/NOT_ON_MONITOR/UNMODELLED)`

`tools/mado-barfoot.py:391-406` maps `reserved=NOT_MODELLED` to
`verdict=UNMODELLED, rc=3` (line 404), never to `CLEAN`. The frozen cases
`css-margins` and `per-side-margin` in `receipts/control-baseline-r77.txt` print
`rc=3 … reserved=NOT_MODELLED … verdict=UNMODELLED`. The row is self-contradictory
(it lists `UNMODELLED` under 3) and a reader following it would treat a refusal as
a pass. Suggested correction (not applied): move `NOT_MODELLED` out of the 0 clause
and name `reserved=NOT_MODELLED` in the 3 clause.

### F2 — HIGH — docstring "refused, never guessed" is false for `mode` presets and static `addreserved` bands

`tools/mado-barfoot.py:28-34`:

> Unexpressed and refused, never guessed: … static monitor `addreserved` bands …
> `mode` presets that rewrite layer/exclusive at runtime …

No code path reads `config["mode"]`; no code path can detect a static reserve. A
config `{"position":"top","layer":"top","height":26,"mode":"hide"}` (Waybar would
render overlay + non-exclusive: `bar.cpp:42-46,346-361`) scores
`MADO_BARFOOT_RESULT: … box=MATCH reserved=EQ … verdict=CLEAN`, rc 0, against the
top-level capture (`evidence/mode-guess.txt`). That is a silent guess — a stale
capture plus a mode-hiding config is scored `CLEAN`. Entry line 55 names the mode
limit but does not say the tool guesses; the static-band sentence (line 54) is
likewise a limit the code does not enforce. The word "refused" should be dropped for
these two items or a guard added.

### F3 — MEDIUM — entry attributes Waybar's anchor clearing to `Renderer.cpp`

`corpus/knowledge/bar-footprint-r77.md:14`:

> the both-horizontal-anchors branch clears both anchors and centres the box
> (`Renderer.cpp:2609-2620`)

The cited range contains no clearing: Hyprland only *tests* the anchor pair and
centres (`Renderer.cpp:2612-2613`); the clearing is Waybar's
(`Waybar/src/bar.cpp:422-424`, `anchors[LEFT] = FALSE; anchors[RIGHT] = FALSE;`).
The geometry outcome is right, the mechanism and anchor are not. The same
misattribution is in the tool contract (`tools/mado-barfoot.py:21-22`). Fix: cite
`bar.cpp:422-424` for the clearing and `Renderer.cpp:2612-2613` for the centring.

### F4 — MEDIUM — shifted anchor for "only one edge wins"

`bar-footprint-r77.md:27`:

> Only one edge wins per surface: … (`:2568-2572`)

Lines 2568-2572 are the right-edge initializer of the `edges[]` table. The rule is
the loop condition at `Renderer.cpp:2575` and its `break` at `:2582`. The cited
range does not contain the sentence's subject.

### F5 — MEDIUM — `gls:` is an unpinned, unregistered source

`bar-footprint-r77.md:51` cites gtk-layer-shell 0.10.1 at
`gls:src/layer-surface.c:264-288`. The formula is correct — verified against the
v0.10.1 tarball (`meson.build: version: '0.10.1'`; `layer-surface.c:264-288`) and
the installed header's "size of the @window + relevant margin" — but `gls:` is not
a SOURCES row, has no id, no sha and no committed fetch, and the C1 declaration's
sourced ground is S457-S462 only. As committed, the entry's strongest §4 claim is
not re-derivable from repository bytes. Fix: open a source row for gtk-layer-shell
0.10.1 (tarball sha) or move the paragraph to the tool docstring's named limit with
a pointer to the installed header.

### F6 — MEDIUM — fabricated "page title" quote in the lesson's Gate

`corpus/lessons/round-77.md:35` gives the S463 quote as
`wlr-layer-shell-unstable-v1 protocol` labelled "(page title)". The page's title is
`wlr layer shell protocol | Wayland Explorer`; the hyphenated string does not occur
anywhere in the 147,036 committed bytes (searched). The page does contain
`wlr-layer-shell-unstable-v1` and `wlr layer shell protocol`, not the concatenation.
A Gate quote must be located text; this one is a reconstruction.

### F7 — MEDIUM — S463's registry row has no located quote

`corpus/SOURCES.md:414` puts the rejection rationale in the registry's quote slot
(now the `teaches` column): "REJECTED: the page renders the protocol text but pins
no protocol or compositor revision…". That is a rationale, not a quote from the
page. The Gate requires "URL/date/quote per row"; the row has URL and date, the
lesson supplies an inexact title (F6), and no actual page sentence is registered.
A true page sentence is available, e.g. `The exclusive zone includes the margin.`
is in the XML (S460), and the page carries its own protocol text that could be
quoted; as it stands the rejected row cannot teach what it rejected on.

### F8 — LOW — S461's quote is not a byte substring of the fetch

`corpus/SOURCES.md:412` quotes `Bar position, can be top, bottom, left, right.`
The troff source at `fetch/S461.txt:91` is
`Bar position, can be \fBtop\fR, \fBbottom\fR, \fBleft\fR, \fBright\fR.\&`. The
sentence is verbatim only after roff rendering (`groff -man | col -b` reproduces it
exactly). Since the row pins the `.gz` sha, the quote and the anchor are one
rendering step apart. Acceptable if the row says "rendered"; otherwise quote a
markup-free line or pin a rendered text.

### F9 — LOW — S459's anchor covers `apply` but not `applyip`

`corpus/SOURCES.md:410` says "apply/applyip :53-60". `apply` is 53-60; `applyip`
is 62-67. The quoted constructor line (34) is inside :19-35 and is exact.

### F10 — LOW — two function ranges stop one line short of the closing brace

S457 row: `applyExclusive :2529-2585` (function ends 2587),
`arrangeLayersForMonitor :2673-2700` (ends 2702). Both contain every claim quoted
from them; the ranges just clip the final `}`. Cosmetic.

### F11 — LOW — entry and lesson disagree by one line on the `applyExclusive` anchor

Entry line 27 cites `(:2576-2581)`; lesson M77-4 (`round-77.md:16`) says the
measured anchor is `:2575-2581` (the condition is 2575). Both ranges contain the
quoted `:2577` add; the correction was not propagated to the entry.

### F12 — LOW — docstring narrows (safely) the margin refusal

`tools/mado-barfoot.py:24-26` says the expectation is formed only when "the bar's
edge margin is zero"; the code refuses on **any** non-zero side
(`:392-393`). Over-refusal cannot produce a false CLEAN, but the stated condition is
not the implemented one. The entry (line 51) has the broader and correct wording.

### F13 — LOW — `layer: background` is accepted but Waybar cannot produce it

Contract line 17 and `LEVEL` (line 50) accept `background`. Waybar 0.15.0's
`from_json(bar_layer)` maps only `bottom`/`top`/`overlay`
(`bar.cpp:63-72`), so `"layer": "background"` leaves the default `BOTTOM` (level 1)
while the tool looks at level 0. An invalid-per-manual config is silently
reinterpreted rather than refused. No frozen case uses it.

### F14 — LOW — two instruments were rewritten mid-wave; the freeze receipts' hashes are stale at the tip

- Tool: `409e78a4…` (freeze, blob `41f3341f`) → `61f34022…` (blob `d8165696`) at
  `0fa69f41`.
- C2 counter: `056a9152…` (freeze, blob `57383fc7`) → `ac2b0f85…` (blob `1b74db6d`)
  at `4a17b31f`.

`receipts/control-baseline-r77.txt` and `receipts/pre-wave-evidence-r77.txt` print
the old hashes; `receipts/measurement-final-r77.txt` prints the new ones. Both
contract lines still re-derive (C1 15/15 at both generations; C2 12/12 before and
after). `VERSION` stayed `r77-v1` across the tool's behavioural change. The
declaration's "instruments … committed at the freeze commit" is therefore true only
of the freeze rev, not of the tip. The two repair receipts are honest about the
change; the round's prose should state the second generation explicitly.

### F15 — LOW — M77-2's evidence pointer does not exist

`round-77.md:14` says `control-baseline-r77.txt` has a first section with
`ERROR stage=setup` versus a final `TARGET_MET`. The file (committed once, at
`94b5afb1`, plain `git log` history) contains **zero** `ERROR`/`stage=setup`
strings at that commit or at the tip. The red-before of the counter's repo-path bug
is not retained in any committed receipt. (The defect class is real; the pointer
is not.)

### F16 — LOW — M77-6's evidence pointer was overwritten

`round-77.md:77` cites `measurement-final-r77.txt`'s first C2 section
(`matched=3`). That file was rewritten at 05:15 with the green run; the `matched=3`
section no longer exists in it. The red excerpt survives only in
`receipts/repair-r77-c2-env.txt`, which is the pointer that should be cited.

### F17 — INFO — C2's "the expectation the row states" is not mechanized and not literally true for 3 of 12 cases

The declaration's predicate says every observed outcome equals the expectation
"the bound SKILL.md row states". The counter only checks that the anchor string is
a substring of `SKILL.md` (`c2-r77-runbook.py:178,192,196`), then compares
against values frozen in the control set. Case-by-case:

- `monitors-reserved`: `SKILL.md:210` states no reserved band; the control's own
  note says "not in the table as a sample, same row". The value `[0,26,0,0]` is
  measured, not stated.
- `monitors-size`: the row states `99.997`; the case expects `99.99700`
  (jq's `{:.5f}` rendering) — a transformation of the row's sample.
- `layers-namespaces`: the row names the two levels separately; the case expects the
  sorted join `wallpaper,waybar` — an ordering not stated.

`anchors=12/12` and `matched=12/12` are true; the "row states it" clause is a
reading, not a check. Either soften the predicate to "bound to its committed row"
or add the stated outcome to the row/control pair.

### F18 — INFO — the seven new SOURCES rows carry a quote where `teaches` should be

Per M77-1 the rows were rewritten to 11 fields "with the quote in `teaches`". The
census is satisfied, but those rows have no teaching statement, unlike every other
row in the registry; the Gate table keeps a separate quote column. This is a
schema-semantics divergence, not a field-count defect.

### F19 — INFO — the entry's S461 line list covers five of six keys

`bar-footprint-r77.md:35` lists page lines `70/91/97/128/189` for
layer/position/height/margin/exclusive; `width`'s description is line 103 and is not
in the list.

### F20 — INFO — the 1 MiB cap is a code fact, not a docstring claim

The tool docstring never states the cap. `MAX_BYTES = 1048576` (line 48) is
enforced on files (`lstat` size) and stdin (`read(MAX+1)`). Tested: a 1,048,577-byte
regular file → rc 2 "file exceeds 1048576 bytes"; 1,048,577 bytes on stdin → rc 2
"stdin exceeds 1048576 bytes"; `/dev/null` → rc 2 "refused non-regular path". The
PROVINCE sentence ("1 MiB cap, symlinks refused") is accurate.

### F21 — INFO — `m_size = pixelSize / scale` and `logicalBoxMinusReserved()` are cited without file:line

Entry line 52's scale sentence and line 54's static-band sentence name functions
with no anchor; both exist (`Monitor.cpp:699-700`, `Monitor.cpp:1772-1774`). Scribe
duty "no number without a pointer" is met for the numbers, not for these two
function references. (The pixel-vs-logical distinction itself is correct:
`HyprCtl.cpp:278` fills `width`/`height` from `m_pixelSize`.)

### F22 — INFO — SCORECARD's C1 revision parenthetical is stale

`SCORECARD.md:4416` says the C1 measurement is at `a83e9bee` "(its instrument's last
change)". The tool's last change is `0fa69f41`; the counts re-derive unchanged at
the tip, so only the parenthetical is stale. The same row's capability pointers
(`SCORECARD.md:4434-4435,4450`) now resolve: `measurement-final-r77.txt` exists and
shows C1 and C2 `TARGET_MET` at `4a17b31f` (it did not exist at `3e35d0a9`).

### F23 — INFO — two transient states were observed and repaired during the audit

- `measurement-final-r77.txt` at `adf8875b` recorded C2 `matched=3 …
  TARGET_MISSED` (no `HYPRLAND_INSTANCE_SIGNATURE` in the final runner). `4a17b31f`
  adds session discovery; the re-run at `4a17b31f` is 12/12 from a non-session shell.
  Verified independently: `env -i PATH=/usr/bin:/bin HOME=…` gives 12/12 at the tip.
- The entry's §4 scale/dynamic refusals were added at `0fa69f41` together with the
  code that implements them, so entry and tool agree at the tip; they were absent
  from both at `3e35d0a9`.

## 3. Quote-by-quote fidelity (mechanical)

| row | quote (abridged) | words | exact bytes | whitespace-normalized | anchor |
|---|---|---|---|---|---|
| S457 | `box.width = bounds.width - (PSTATE->margin.left + PSTATE->margin.right);` | 7 | YES | YES | `Renderer.cpp:2637` (range :2587-2670) |
| S458 | `sc<int>(m->m_reservedArea.left()), … .bottom())` | 4 | YES (line 302) | YES at :281-282 | row says :281-282; exact only at :302 |
| S459 | `m_initialBottomRight = (parent.pos() + parent.size()) - (child.pos() + child.size());` | 9 | YES | YES | `ReservedArea.cpp:34` |
| S460 | `A positive zone is the distance from the edge in surface-local coordinates to consider exclusive.` | 15 | no (line break) | YES | XML:165-166 (range :152-190) |
| S461 | `Bar position, can be top, bottom, left, right.` | 8 | no (`\fB`/`\&`) | no | rendered from S461.txt:91 |
| S462 | `if (mode.exclusive) { gtk_layer_auto_exclusive_zone_enable(gtk_window); }` | 5 | no (3 lines) | YES | `bar.cpp:357-359` (range :355-361) |
| S463 | `wlr-layer-shell-unstable-v1 protocol` | 2 | no | no | not in the page; title is `wlr layer shell protocol` |

All <=25 words. No overlong quote. The two failures are S461 (rendering level) and
S463 (fabrication, already F6/F7).

## 4. Tool docstring claims, checked against code and sources

| claim | verdict | evidence |
|---|---|---|
| `reserved` order `[left, top, right, bottom]` | TRUE | `HyprCtl.cpp:253` (JSON), `:281-282` (args), `:293,302` (text); `ReservedArea.hpp` accessors `left/right/top/bottom` earlier in the same order |
| exit map 0/1/2/3 | TRUE in code; contradicted by `SKILL.md:743` for `NOT_MODELLED` | `mado-barfoot.py:391-406`, `:556-561`; F1 |
| 1 MiB cap | TRUE in code; not in the docstring | `MAX_BYTES` line 48; tested rc 2 both channels |
| auto-exclusive-zone limit (`NOT_MODELLED`) | TRUE | `gls` v0.10.1 `layer-surface.c:264-288` (zone = allocation + unanchored-edge margins); XML:196 "The exclusive zone includes the margin"; Hyprland adds the anchored margin at `Renderer.cpp:2575-2580` |
| "refused, never guessed" for mode/static | FALSE | F2, demonstrated |
| `layer: background` accepted | MISMATCH | F13, `bar.cpp:63-72` |
| scale/transform refusal | TRUE at the tip | `mado-barfoot.py:348-353`; `HyprCtl.cpp:278` (pixel size), `Monitor.cpp:699-700` (logical size) |
| dynamic cross-size refusal | TRUE at the tip | `mado-barfoot.py:250-253`; `bar.cpp:639-649` (allocation) |

## 5. Residual (observed, not defects in bytes)

- All 15 frozen fixtures set `origin (0,0), scale 1.0, transform 0`; even
  `two-monitors` places both monitors at `0,0`. So the scale refusal, and the
  assumption that a layer box is monitor-origin-local (Hyprland's `m_geometry` is
  global: `Renderer.cpp:2588,2624`), are unexercised by the frozen set. This does
  not affect the host (DP-1 at 0,0) or the 15/15, but it bounds what the cases
  prove.
- `mode`, `addreserved`, `layer: bottom`, and the `width: 1` crack have no case
  (the last two were named by the scout).
- The C2 suite's `monitors-reserved` and `monitors-size` case expectations are
  measured values, not row text (F17).

## 6. No-harm and tooling

- No repo/config/compositor/service write. The only socket-free read verbs used
  were `hyprctl` reads through the committed C2 counter plus direct file reads.
  No `git`/`jj` mutation. No package transaction; no tool installed or upgraded.
- Network use: one read-only `curl` of the S463 page and one of the gtk-layer-shell
  v0.10.1 tarball, both in scratch, compared and discarded.
- Scratch `/fast/scratch/hyaku/mado-r77/R77RevBytes/` was deleted before finishing;
  the retained evidence is `evidence/` beside this report.

## 7. Post-fix verification at `bbca7469` (append-only)

The L1 reported four accepted fixes; each was re-checked against committed bytes at the lane tip
`bbca7469` (not taken on report):

- **F1 fixed.** `SKILL.md:743` now reads `0 CLEAN (box MATCH and reserved EQ/GT/NOT_APPLIED)` and
  `3 not formed (NO_LAYER, NOT_ON_MONITOR, UNMODELLED incl. reserved=NOT_MODELLED)`. Matches the
  code (`mado-barfoot.py:404`).
- **F2 fixed.** `declared_bar` now raises `Unmodelled` on a string `mode` key
  (`tools/mado-barfoot.py:233-234`); a live `mode: hide` run exits 3 with
  `ERROR (stage=model a mode preset rewrites layer and exclusive zone at runtime)`; the receipt is
  `receipts/repair-r77-mode-refusal.txt` (before rc 0 CLEAN, after rc 3). The docstring now
  separates "Refused, never guessed" (mode, scale/transform, dynamic cross size, list config,
  `*`/space outputs) from "Not modelled and named as a limit" (static `addreserved`, runtime) —
  which is accurate for the code.
- **F3 fixed.** Entry line 14 now reads "waybar clears both horizontal anchors
  (`bar.cpp:422-424`); the both-anchors branch then centres the box (`Renderer.cpp:2609-2620`)";
  the docstring carries the same split (`mado-barfoot.py:20-23`).
- **F4 (lesson S463) fixed.** The Gate quote is now `wlr layer shell protocol`, which is the
  page's literal title text and occurs in the committed 147,036-byte page. The SOURCES S461 quote
  is now the literal troff line (`S461.txt:91`) with the anchor noting the zcat output.

Re-measured at `bbca7469`: `MADO_R77_BARFOOT: cases=15 correct=15 mutants=5 killed=5
base_correct=8/15 tool_selftest=18/18 verdict=TARGET_MET … tool_sha256=80a3b6e0…`;
`MADO_R77_RUNBOOK: cases=12 executed=12 matched=12 unexecuted=0 anchors=12/12`;
`mado-barfoot.py --selftest` 18/18. The `reserved-wrong-edge` mutant is now a dict swap and scores
10/15 semantically; the previous text (`},`) made the mutant a tuple, so the mutated tool died with
`TypeError: tuple indices must be integers or slices, not str` — the old 4/15 kill was
crash-driven (receipt `repair-r77-mutant-oracle.txt`). Instrument generations are now three:
tool `409e78a4→61f34022→80a3b6e0`, C1 counter `56620959→a5f4ad97`, C2 counter
`056a9152→ac2b0f85`; control sets unchanged.

Residuals after the fixes (verified at `bbca7469`; none block the two contract lines):

- **R1 (MED).** Entry line 55 is stale: it says "the model reads the raw `layer`/`exclusive`
  keys", but the tool now refuses any `mode` key (rc 3). The bullet should say the mode key is
  refused.
- **R2 (MED).** The "single-line literal" quote rewrite truncated three quotes so they no longer
  state what the row claims: S460 stops mid-sentence at `…in surface-local` (the operative
  `to consider exclusive` is XML:166); S458 now shows only the `left`/`top` calls, so the
  `[left, top, right, bottom]` order the row is about is not visible; S462 drops the
  `if (mode.exclusive)` guard, so the condition the purpose names is absent.
- **R3 (LOW).** The lesson Gate row for S461 (`round-77.md:33`) still quotes the rendered
  sentence while the SOURCES row quotes the troff line; the addendum's claim that the
  S458/S460/S462/S461 quotes are now literal is true of SOURCES, false of the Gate table.
- **R4 (MED).** SOURCES S463 still carries the rejection rationale in the quote/`teaches` slot;
  only the lesson now has the literal title. The registry row still has no located page quote.
- **R5 (LOW).** Entry line 27 still cites `:2568-2572` for "only one edge wins" (rule at
  `:2575-2583`) and `:2576-2581` where the lesson states `:2575-2581`.
- **R6 (MED).** `gls:src/layer-surface.c:264-288` remains unregistered/unpinned (no SOURCES row,
  no sha, no committed fetch).
- **R7 (LOW).** `SCORECARD.md:4416` still says "at `a83e9bee` (its instrument's last change)";
  the tool's last change is now `bbca7469` and the C1 counter's `de627316` (counts unchanged).
- **R8 (LOW).** The docstring still says the expectation is formed only when "the bar's edge
  margin is zero"; the code refuses any non-zero margin side.
- **R9 (LOW).** The C2 erratum names `monitors-reserved` and `waybar-process`, but not the two
  written-form transformations I flagged: `monitors-size` (`99.997` → `99.99700`) and
  `layers-namespaces` (per-level names → sorted join).
- **R10 (LOW).** `layer: background` is still accepted though Waybar 0.15.0 cannot produce it
  (`bar.cpp:63-72` leaves the default `BOTTOM`).

### Update at `e177c79b` (committed tip at audit end)

Further commits during the audit: `2df46e29` (literal single-line fragments in SOURCES/lesson;
tool docstring now attributes the anchor clearing to `bar.cpp:422-424`) and `e177c79b` (S464
gtk-layer-shell row, entry manual-line precision and S464 citation; declaration erratum for the
seventh mined row). Verified at `e177c79b`:

- S464 is registered with anchor `layer_surface_update_auto_exclusive_zone :264-292 @ v0.10.1`,
  sha256 `deef9c81…`. I re-fetched `raw.githubusercontent.com/wmww/gtk-layer-shell/v0.10.1/
  src/layer-surface.c` and got the same sha; the quoted
  `new_exclusive_zone += self->margins[GTK_LAYER_SHELL_EDGE_BOTTOM];` is literal at line 280.
  The row has the 11-field shape (quote in `teaches`), matching M77-1's fix.
- The entry now cites S464 in §4 and in its Sources line, and the S461 line list is qualified as
  "headings at rendered lines 64/85/93/124/183, their text at 70/91/97/128/189" — F19 addressed.
- Instrument generations are now four: tool `409e78a4→61f34022→80a3b6e0→446d197f`
  (`2df46e29` is docstring-only), C1 counter `56620959→a5f4ad97`, C2 counter
  `056a9152→ac2b0f85`. At `2df46e29` the C1 counter reproduces the contract with
  `tool_sha256=446d197f…`; C2 12/12; selftest 18/18.

Residuals that remain at `e177c79b` (the earlier R numbers 1-5, 7-10 still stand):

- **R6 (now a provenance gap, not a model gap).** The S464 row is committed but
  `.ufo/waves/round-77/fetch/S464.bin` is **untracked** and absent from
  `fetch/sha256-r77.txt` (the manifest still lists 8 entries, S457-S463). The cited sha is
  verifiable only by re-fetching the network; the round's own pattern is fetch-bytes-committed.
- **R11 (LOW, new).** The entry header is now stale: `verified-at` still names
  `fetch/S457.bin … S462.bin`, and `recheck` still says "re-pin the six files", after S464 made
  the set seven sources (eight fetch files, counting `S459.hpp.bin`).
- **R12 (INFO).** The declaration's S464 erratum is appended and accurate ("seven mined rows plus
  one rejected, not six"); it does not re-freeze anything.
- **R2 remains in full.** S460's quote still ends at `…in surface-local` (the operative
  `to consider exclusive` is the next line); S458's quote still shows only left/top; S462's quote
  still omits the `if (mode.exclusive)` condition.
- **R3 remains.** The lesson Gate row for S461 still quotes the rendered sentence, while the
  SOURCES row quotes the troff line — the addendum's "the S458/S460/S462/S461 quotes are now
  single-line literal" is true of SOURCES, false of the Gate table.
- **R4 remains.** SOURCES S463 still has the rejection rationale in the quote/`teaches` slot; only
  the lesson carries the literal page title.
- **R1, R5, R7, R8, R9, R10 remain** as written above. At this tip the tool's last change is
  `2df46e29` and the C1 counter's `de627316`, so `SCORECARD.md:4416`'s "at `a83e9bee` (its
  instrument's last change)" is four tool generations stale (counts unchanged).

### Update at `53b4fadf` (all seven applied)

Verified against the committed bytes: `fetch/S464.bin` is tracked and line 9 of
`fetch/sha256-r77.txt` carries `deef9c81…`; the entry's `verified-at` spans `S457.bin … S464.bin`
and `recheck` says "seven files", with S464 in the source line; S460's quote is the literal
`The exclusive zone includes the margin.` (XML:196); S462's anchor notes the
`if (mode.exclusive)` guard at :357; S458's anchor states the four-call order across :281-282;
the lesson Gate's S461 quote is the troff line; entry line 55 says a `mode` key is refused
(exit 3); entry line 27 carries `add at :2577, rule :2575-2583`; the SCORECARD correction names
C1 counter `de627316`, tool `2df46e29` (`446d197f…`), C2 counter `4a17b31f`.

Counts re-derived at `53b4fadf`: `MADO_R77_BARFOOT: cases=15 correct=15 mutants=5 killed=5
base_correct=8/15 tool_selftest=18/18 verdict=TARGET_MET … tool_sha256=446d197f…`;
`MADO_R77_RUNBOOK: cases=12 executed=12 matched=12 … anchors=12/12`. `measurement-final-r77.txt`
is now at `53b4fadf` with C2 12/12, ledger 140/140 and axis 0 mismatches.

Still open, none blocking: (R4) the S463 registry row keeps the rejection rationale in the
quote/`teaches` slot — the lesson Gate now carries the literal page title, so the registry row
remains the one row without a located quote; (R8) the docstring still says "edge margin is zero"
while the code refuses any non-zero margin side; (R9) the C2 erratum names `monitors-reserved`
and `waybar-process` but not the `monitors-size`/`layers-namespaces` written-form transforms;
(R10) `layer: background` is still accepted although Waybar cannot produce it. At audit end
`measurement-final-r77.txt` and `harm-watch-r77.txt` were untracked; closure should commit them
with the wave evidence.

Report: .ufo/waves/round-77/w1/R77RevBytes.md

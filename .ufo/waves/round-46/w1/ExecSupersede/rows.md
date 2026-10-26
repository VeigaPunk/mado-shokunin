# ExecSupersede — census-clean supersession of the S290-S297 cells (round 46 w1)

Seat: ExecSupersede. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`. Target: round-44 D6, carried a second
time by round-45 D6 (`corpus/lessons/round-45-verifier-spotcheck.md` §6 item 6). Registry at base: 252 rows,
top S315 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `252`).

Deliverable: eight new rows `S326`-`S333` continuing after S325, seven of them opening `teaches` with
`supersedes S29N —` (CORPUS.md rule 2), plus the round-46 `## Gate` lines each row needs. The block is
`rows-block.txt` in this directory; the census proof is `census-*.txt`; the locator proof is `locators.txt`.

## 1. What is wrong with each row, and who found it

| predecessor | defect | found by | my re-open (computed) |
|---|---|---|---|
| S290 | `scope` and `teaches` mix a second source: the file tests a regex but does not show a `class` rule reaches it, and the host pattern text `^(org.omarchy.gkeep)$` lives in S295 | round-43 `w2/ScoutRowsA/rows.md:18,20` | `Rule.cpp:52,98` binds `RULE_PROP_CLASS` to `RULE_MATCH_ENGINE_REGEX` and builds `CRegexMatchEngine`; `WindowRule.cpp:395-396` hands `w->m_class` to the engine — neither is in the S290 anchor |
| S291 | title says "who consumes a size rule" though a tiled consumer exists; `teaches` drops three conditions (parse success, the center gate, the later clamp) | `w2/ScoutRowsA/rows.md:36,40` | `Window.cpp:2402-2409` is the tiled consumer; `DefaultFloatingAlgorithm.cpp:57-58` is the parse-failure branch, `:79-84` the center gate, `:90-91` the no-position re-center, `:93-102` the re-center on work-area miss |
| S292 | last `teaches` clause ("the geometry a window reports is a value the layout wrote") is a three-row inference absent from `Target.cpp` | `w2/ScoutRowsB/rows.md:23` | `Target.cpp:68-70` is the only writer in the file; its caller is `DefaultFloatingAlgorithm.cpp:193-196` (`removeTarget`), i.e. another document, and the file never mentions a client report |
| S293 | title ("the client's request as input") echoes the premise round-43 refuted; `teaches` omits the `||`, the `> 5` gate, the 600x400 branch and the failure return; anchor lacks the two ranges | round-43-verifier D2; `w2/ScoutRowsB/rows.md:33-53` | `WindowTarget.cpp:339` is `width <= 2 || height <= 2`, `:342` the `> 5` surface gate, `:350-362` the override-redirect branch with `600, 400`, `:364` the `unexpected(...)` return, `:323-326` the stored-size override |
| S294 | `teaches` tail "can differ from what is on screen" is not in the file | `w2/ScoutRowsC/rows.md` (S294 `teaches` cell) | `GeometricMovableAnimated.cpp:19-20` are the two reads; nothing in the file is about drawing |
| S296 | `teaches` says "a window that was never mapped" — one snapshot cannot support a history claim; the row also does not say which fields the dump kept | round-43 w2 left no finding (`ScoutRowsD/` is empty); round-44 `w1/ScrSupersedeRows.md` finding 1 re-opened it | the file has 62 lines and four objects, each exactly `address, at, class, floating, mapped, monitor, size`; `grep -c fullscreen` = 0, `grep -c title` = 0, `grep -c org.omarchy.gkeep` = 0 |
| S297 | title calls the value a "request"; the anchor locators `:6`/`:33` are excerpt-relative while the cell names only the excerpt file, so a reader mapping them onto `ui.py` is three lines off | same as S296 (round-44 `w1/ScrSupersedeRows.md`) | excerpt lines 1-2 are a provenance header, so excerpt `:6` = `ui.py:449` and excerpt `:33` = `ui.py:476`; `grep -c set_size_request` = 0 in the excerpt and in `ui.py` |
| S295 | none — its `teaches` already limits itself ("the file alone shows nothing of what the window received") | round-43 `w2` found no defect | **not superseded**; superseding a correct row would add a row without a correction |

The closure text names exactly `S290-S294, S296, S297` and my list matches it. Round-44's draft
`.ufo/waves/round-44/w1/ScrSupersedeRows/rows-block.txt` proposed seven rows (`S302`-`S308`); those ids are now
taken (round 45 landed S302-S315), so this draft renumbers to `S326`-`S332` and adds one grounding row `S333`
for `Rule.cpp`, the one source the S290 correction needs that no row holds (`S157` holds `WindowRule.cpp`,
`S164` holds `Window.cpp`).

Round-44's draft is **not copied blindly**: three of its cells are corrected here, each against the fetched
bytes — `S328` said "the file does not show who writes that member" though `Target.cpp:68-70` is that writer (the
missing fact is the *caller*, `DefaultFloatingAlgorithm.cpp:194`); `S327`'s anchor omitted that same caller;
`S326` said the host-text mixing was left in `scope` while narrowing nothing, and I narrow `scope` instead and
say so below.

## 2. Which form the census accepts

Two forms pass CORPUS rule 2 on its face: new rows with the `supersedes` opener, or an appended errata block.
The census decides (`scripts/sources-census.sh`):

- **New rows, `teaches` opening `supersedes S29N —`: accepted.** `E04` (duplicate URL within a scope) has an
  exemption at `sources-census.sh:646-648` — `teaches !~ /supersedes S[0-9]{3}/` — so a superseding row is legal and
  the opener is load-bearing (variant `m5`, opener stripped: `E04` x4, exit 1).
- **Errata block appended outside `## Registry`: not a correction the census can see.** A prose block is not
  row-shaped, so it produces no finding but also changes no row (variant `m3`, exit 0, rows still 252); a
  row-shaped block outside the Registry trips `E12` (variant `m4`, `E12` x2, exit 1).

Decision: **new rows**. Only one scope cell changes (`S326`), which costs exactly one new `W04`
(`same URL across scopes`, a warning that does not fail validation) — measured: the lane's `W04` count goes
9 → 10 and the sole new one is `S326`. Every other superseding row keeps its predecessor's `scope` verbatim, so a
reader can diff scope cells and see that only the cells that were wrong moved.

## 3. The rows

`rows-block.txt`, eight rows, pasted verbatim below (one line per row, 11 cells, no `|` inside a cell; the
mechanical check is `shape-check.txt`: 8/8 rows `OK`, ids `S326..S333` contiguous, 0 defects):

```text
| S326 | ... supersedes S290 ... scope narrowed to "The regex test an engine applies to a rule string, and the `negative:` prefix"; teaches: FullMatch on the whole string, prefix stripped with substr(9) and inverting by flag comparison, `^`/`$` redundant, `.` matches any character except a newline, and the class-to-engine link named as S333 / S157 rather than claimed from this file | mined | 2026-10-26 | on-release |
| S327 | ... supersedes S291 ... title narrowed to the floating first-map consumer; teaches: parse gate (:56-58), overwrite (:60-61), center only under the center rule (:79-84), no-position re-center (:90-91), work-area re-center (:93-102), clamp is S329, tiled path is Window.cpp:2402-2409; anchor gains :193-196 | mined | 2026-10-26 | on-release |
| S328 | ... supersedes S292 ... teaches: box stored and both parts rounded (:10-14), position returns the logical part (:64-66), the remembered size has exactly one writer in this file (:68-70) and its caller is elsewhere (DefaultFloatingAlgorithm.cpp:193-196); the file says nothing about what a client reports | mined | 2026-10-26 | on-release |
| S329 | ... supersedes S293 ... title drops the request premise; teaches: clamped client size (:313, :297-304), stored-size override (:323-326), 2 px trigger (:339), > 5 surface gate (:342-347), 600x400 or own geometry (:350-362), failure return (:364) | mined | 2026-10-26 | on-release |
| S330 | ... supersedes S294 ... teaches: the two reads (:19, :20) and that the file does not say what is drawn | mined | 2026-10-26 | on-release |
| S331 | ... supersedes S296 ... scope and teaches: what the dump held, the seven kept keys, no gkeep entry, absence at that moment is not "never mapped", no fullscreen field | mined | 2026-10-26 | 2027-01-24 |
| S332 | ... supersedes S297 ... title, anchor and teaches: default size not a request, excerpt-relative locators mapped to ui.py:449 and :476, no set_size_request | mined | 2026-10-26 | 2027-01-24 |
| S333 | new grounding row (no supersession): Rule.cpp:52 binds the class property to the regex engine, :98 constructs it | mined | 2026-10-26 | on-release |
```

(Abbreviated here for reading; `rows-block.txt` holds the exact cells that go into the registry.)

`used-by` for all eight is `.ufo/waves/round-46/w1/ExecSupersede/rows.md` — this file. Precedent for a `.ufo/`
used-by target exists in the lane: `S184` (`.ufo/waves/round-29/registration.md`) and `S185`
(`.ufo/waves/round-30/registration.md`). The alternative, `corpus/lessons/round-46.md`, does not exist yet and
would make the census return `E11` x8 until the L1 writes it (measured: variant `m2`, `E11` x8 on the eight new
rows).

## 4. Gate lines the new rows need (for `corpus/lessons/round-46.md` `## Gate`)

Access date 2026-10-26 for every line. Each quote is ≤ 25 words, located by a computed locator (`locators.txt`),
and unique on its cited line. Paste the block as-is into `corpus/lessons/round-46.md` `## Gate`.

| row | source | access | quote (line) |
|---|---|---|---|
| S326 | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/RegexMatchEngine.cpp` | 2026-10-26 | `return re2::RE2::FullMatch(other, *m_regex) != m_negative;` — `:16`, 5 words, 1 hit |
| S327 | `…/src/layout/algorithm/floating/default/DefaultFloatingAlgorithm.cpp` | 2026-10-26 | `const auto COMPUTED = WINDOW->calculateExpression(*WINDOW->m_ruleApplicator->static_.size);` — `:56`, 5 words, 1 hit |
| S328 | `…/src/layout/target/Target.cpp` | 2026-10-26 | `void ITarget::rememberFloatingSize(const Vector2D& size) {` — `:68`, 5 words, 1 hit |
| S329 | `…/src/layout/target/WindowTarget.cpp` | 2026-10-26 | `if (DESIRED_GEOM.width <= 2 || DESIRED_GEOM.height <= 2) {` — `:339`, 9 words, 1 hit |
| S330 | `…/src/desktop/view/types/GeometricMovableAnimated.cpp` | 2026-10-26 | `case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();` — `:19`, 4 words, 1 hit |
| S331 | `.ufo/waves/round-43/fetch/host-clients-r43.json` (own-work) | 2026-10-26 | `"class": "Alacritty",` — `:5`, 2 words, 1 hit; negative sweep `grep -c fullscreen` = 0 and `grep -c title` = 0 |
| S332 | `.ufo/waves/round-43/fetch/gkeep-ui-excerpt.py` (own-work) | 2026-10-26 | `window.set_default_size(420, 500)` — excerpt `:33` (= `ui.py:476`), 2 words, 1 hit; negative sweep `grep -c set_size_request` = 0 in the excerpt and in `ui.py` |
| S333 | `…/src/desktop/rule/Rule.cpp` | 2026-10-26 | `{RULE_PROP_CLASS, RULE_MATCH_ENGINE_REGEX},` — `:52`, 2 words, 1 hit |

The five Hyprland pins re-fetched today are byte-equal to the round-43 pins (`470`, `10359`, `3064`, `16614`,
`1576` bytes; sha256 `8ca65533…`, `f05f2561…`, `49323833…`, `8bcaf370…`, `649f1a8d…`); the two own-work pins are
unchanged (`711` B `21db902e…`, `1625` B `3695b788…`); `Rule.cpp` is new at `6835` B `257687ef…`, and the two
cross-referenced held files are `WindowRule.cpp` `19588` B `7034c332…` (= S157) and `Window.cpp` `124226` B
`d735d454…` (= S164). Receipts: `fetch/` in this directory (all eight `.cpp`), plus
`locators.txt` for the line numbers.

## 5. Census proof

Mirror: one read-only copy of the lane tree (no `.git`) at `/fast/scratch/hyaku/mado-r46/ExecSupersede/mirrors/tree`;
each variant rewrites only `corpus/SOURCES.md` in that copy, then runs
`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md`.
Driver: `mirror.sh <scratch>/mirrors`, receipts `census-m0.txt` … `census-m6.txt`.

A `corpus/`-only mirror cannot be used as the proof: `--file` resolves `used-by` against the mirror's parent
directory, so a copy holding only `corpus/` fails on rows the round does not touch —
`bash sources-census.sh validate --file <scratch>/corpus-only/corpus/SOURCES.md` → `E11` x12 (`S096`, `S173`,
`S174`, `S178`-`S182`, `S184`, `S185`), exit 1 (`census-corpus-only-baseline.txt`). The mirror therefore copies
the lane tree, and the baseline `m0` is clean.

| variant | what it applies | exit | rows | E | W |
|---|---|---|---|---|---|
| `m0` | nothing (baseline) | 0 | 252 | 0 | `W01` x1, `W04` x9 |
| **`m1`** | **the eight rows (recommended landing)** | **0** | **260** | **0** | `W01` x1, `W04` x10 |
| `m2` | rows, `used-by` pointing at a path that does not exist | 1 | 260 | `E11` x8 | `W01` x1, `W04` x10 |
| `m3` | prose errata block appended (control) | 0 | 252 | 0 | `W01` x1, `W04` x9 |
| `m4` | row-shaped errata table appended outside `## Registry` (control) | 1 | 254 | `E12` x2 | `W01` x1, `W04` x9 |
| `m5` | rows with the `supersedes S29N —` opener stripped (control) | 1 | 260 | `E04` x4 | `W01` x1, `W04` x10 |
| `m6` | rows with `used-by` set to `—` (control) | 0 | 260 | 0 | `W01` x1, `W03` x8, `W04` x10 |

`m1` in full (`census-m1.txt`, pasted):

```text
file	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
file	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
file	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
file	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
file	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
file	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
file	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
file	W01	S277 tierC mined used-by=corpus/knowledge/request-socket-live-bound-r8.md
file	W04	S303 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp across scopes
file	W04	S307 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp across scopes
file	W04	S326 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/RegexMatchEngine.cpp across scopes
file	ok	<mirror>/corpus/SOURCES.md
```

(the last line's path is the scratch mirror root, elided here; `census-m1.txt` carries it verbatim)

The one line `m1` adds to the lane's warning set is `W04 S326`, the honest record that one URL now sits under a
narrowed scope. `m5` names exactly the four rows that duplicate a predecessor's URL **and** scope — `S327`,
`S328`, `S329`, `S330` (`census-m5.txt`) — which is what makes the `supersedes` opener load-bearing rather than
decorative. `m2` and `m6` separate the two ways a `used-by` can be wrong: a path that does not exist is `E11`
(exit 1), a `—` on a `mined` row is `W03` (warning only).

## 6. Locator and shape receipts

- `locators.txt` — `python3 -I check-quotes.py`: eight quotes, each with computed line, hit count and sha256
  against the pin; nineteen anchor ranges printed with their first and last source lines; the negative sweeps.
  Last line `QUOTE_AND_RANGE_CHECK: ok`.
- Shape (`shape-check.txt`): each row has 11 cells (`NF=13` with the two edge pipes, 12 pipes), no `|` inside a
  cell, `kind`, `tier`, `status`, `opened`, `recheck` inside the contract enums, the `used-by` value equal in all
  eight rows, and only S333 lacking the `supersedes` opener because it supersedes nothing — `8/8 OK, defects=0`.
- `diff-append-only.txt` — `diff` of the lane's `corpus/SOURCES.md` against the same file with the block
  appended: 8 added lines, 0 removed or changed, rows 252 → 260, insertion after line 264 (`S315`) and before
  `## Paths` at line 266.
- `census-corpus-only-baseline.txt` — the corpus-only-mirror control from section 5 (`E11` x12, exit 1).
- `census-m0.txt` … `census-m6.txt` — the seven variant runs.

## 7. What the L1 must do to land this

1. Append `rows-block.txt` immediately after the `S315` row (inside `## Registry`, before `## Paths`), keeping
   the ids in order; the file has 252 rows now, 260 after.
2. Add a `## Registry changes logged old→new (CORPUS.md rule 2)` section to `corpus/lessons/round-46.md` naming
   `S326`-`S333` with the predecessor each supersedes, and paste the Gate lines from section 4 into that lesson's
   `## Gate`.
3. Nothing else changes: `S290`-`S297` stay byte-identical (append-only), and the round-43 entry
   `corpus/knowledge/hyprland-gkeep-geometry-r43.md` keeps its text. A reader who follows `S293` now also meets
   `S329`.
4. Keep this seat directory (`rows.md`, `rows-block.txt`, `fetch/`, `locators.txt`, `census-*.txt`) or move
   `fetch/` under the round-46 `receipts/` — S333's anchor names
   `.ufo/waves/round-46/w1/ExecSupersede/fetch/Rule.cpp`, and the census does not check anchor paths, but a
   reader will.

## 8. Limits

- The census checks shape, enums, ids, URLs and used-by existence, not the truth of a cell. The truth of each
  corrected cell is the locator receipt in `locators.txt`, which is my own computed output; a non-author should
  re-run it against the same `fetch/`.
- `S326`'s narrowed `scope` is the only cell that produces a new warning (`W04`); the alternative (keeping the
  imprecise scope to stay warning-neutral) leaves the defect in place, which is what round-43 D2 asked to fix.
- `S331`/`S332` are own-work rows: their "quote" grounds a structural fact (a class line, a default-size call)
  while their corrected clauses are negative claims, so each carries a sweep command instead of a positive
  quote for that half.
- The round-43 entry's own repeats of the S293/S297 imprecision (`corpus/knowledge/hyprland-gkeep-geometry-r43.md`)
  are not edited here: it is a tracked file, and rule 2 corrections are registry rows.

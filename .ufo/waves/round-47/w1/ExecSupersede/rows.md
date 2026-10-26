# ExecSupersede — S290-S297 supersession, re-verified (round 47 w1, item R4a)

Seat ExecSupersede. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, base `60edb66e2f1cb90acc6e9442fc93ded0ca42d750`,
HEAD at work time `c24adef2`. Registry at HEAD: **262 rows, top `S325`**, no `S326+` present
(`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `262`;
`grep -cE '^\|[[:space:]]*S326[[:space:]]*\|'` → `0`). `git diff --stat -- corpus/SOURCES.md` is empty; no tracked file was edited.

This is the round-46 draft (`.ufo/waves/round-46/w1/ExecSupersede/rows.md`) re-opened **from the bytes**, not
copied: every pin was re-fetched on 2026-10-26, every quote and anchor was recomputed, and the block was renumbered
because **this round's own C2 entry takes `S326`-`S345`** (`claims.md`: "on rows S326.. opened this round"). The
superseding rows therefore land at **`S346`-`S353`**.

Contents: the defect table (§1), the form the census accepts (§2), the rows (§3), the Gate lines (§4), the census
proof (§5), the locator/shape receipts (§6), what the L1 does to land it (§7), optional in-place changes (§8), limits (§9).

---

## 1. What is wrong with each predecessor, re-opened today

Every "my re-open" cell below is a **computed** locator against the file in `fetch/` (sha256 in §6), not a reading
of the round-46 draft. The three negative sweeps at the end of the table are `grep -c` counts of 0.

| predecessor | defect (as it stands in `corpus/SOURCES.md` today) | found by | my re-open, computed today |
|---|---|---|---|
| `S290` | `scope` and `teaches` present the file as "the test a host `match:class` regex is put through"; the file contains no class-linkage at all (`grep -ci 'RULE_PROP_CLASS\|WindowRule\|m_class'` = **0**) | `round-43/w2/ScoutRowsA/rows.md:18` (scope NEEDS-NARROWING) and `:20` (teaches provenance defect) | `Rule.cpp:52` binds `RULE_PROP_CLASS` to `RULE_MATCH_ENGINE_REGEX` and `:98` constructs the engine; `WindowRule.cpp:395-396` hands `w->m_class` to it. Neither line is in the S290 anchor |
| `S291` | title says "who consumes a size rule", but a tiled consumer exists; `teaches` drops the parse gate, the center gate and the re-centers | `round-43/w2/ScoutRowsA/rows.md:36` (OVERSTATED TITLE) and `:40` (teaches PARTLY OVERSTATED) | `Window.cpp:2402-2409` consumes the same stored expression on the tiled path (fallback `:2413-2414`); `DefaultFloatingAlgorithm.cpp:56-58` is the parse gate, `:79-84` the center gate, `:90-91` the no-position re-center, `:93-102` the work-area re-center |
| `S292` | last `teaches` clause — "the geometry a window reports is a value the layout wrote" — is not in `Target.cpp`: the file does not contain the words client, report or mapped (`grep -ci` = **0**) | `round-43/w2/ScoutRowsB/rows.md:23` (teaches PARTIAL, last clause) | `Target.cpp:68-70` is the only write of the floating-size member in the file; its caller is `DefaultFloatingAlgorithm.cpp:193-196` (`removeTarget`), another document |
| `S293` | title ("the client's request as input") restates the premise round-43 refuted; `teaches` omits the `\|\|`, the `> 5` gate, the 600x400 branch, the failure return and the persistent-size override; anchor lacks two ranges | `corpus/lessons/round-43-verifier-spotcheck.md:100` (D2, title only) and `round-43/w2/ScoutRowsB/rows.md:44` (teaches PARTIAL, three imprecisions) | `WindowTarget.cpp:339` is `width <= 2 \|\| height <= 2`; `:342` the `> 5` surface gate; `:350-362` the override-redirect branch with `{600, 400}`; `:364` the `unexpected(...)` return; `:323-326` the stored-size override |
| `S294` | `teaches` tail "can differ from what is on screen" is not in the file (`grep -ci 'draw\|render\|screen\|damage'` = **0**) | `round-43/w2/ScoutRowsC/rows.md:59` (cell defects, item 2) | `GeometricMovableAnimated.cpp:19` = `goal()`, `:20` = `value()`; nothing in the file is about drawing |
| `S296` | `teaches` says "a window that was never mapped" — one snapshot cannot carry a history claim — and does not say which fields the dump kept | `round-43/w2/ScoutRowsD/` is empty; `round-44/w1/ScrSupersedeRows.md:73` (finding 1) and `:82-83` (finding 4) | the dump has 62 lines and four objects, each with exactly `address, at, class, floating, mapped, monitor, size`; `grep -c fullscreen` = 0, `grep -c title` = 0, `grep -c org.omarchy.gkeep` = 0 |
| `S297` | title calls the value a "request"; anchor locators `:6`/`:33` are excerpt-relative while the cell names only the excerpt, so a reader maps them onto `ui.py` three lines off | `round-44/w1/ScrSupersedeRows.md:73` (finding 1, S296/S297) | excerpt lines 1-2 are a provenance header, so excerpt `:6` = `ui.py:449` and excerpt `:33` = `ui.py:476`; `grep -c set_size_request` = 0 in the excerpt **and** in `ui.py` (14639 B, 488 lines, sha256 `07a3c4a4…`, re-read 2026-10-26) |
| `S295` | **none** — `teaches` already limits itself ("the file alone shows nothing of what the window received") | round-43 `w2`: no defect | **not superseded.** A superseding row that corrects nothing adds a row without a correction |

The routed closure (round-46 spot-check §6 R4) names `S290-S297`; seven of the eight are superseded and `S295` is
explicitly excluded with the reason above. One grounding row is added (`S353`, `Rule.cpp`) because the `S290`
correction needs a source no existing row holds: `S157` holds `WindowRule.cpp`, `S164` holds `Window.cpp`.

### Differences from the round-46 draft (improvements, not copies)

1. **`S346` no longer asserts RE2 semantics as this file's text.** The draft's `teaches` said "so a leading `^` and a
   trailing `$` add nothing and an unescaped `.` matches any character except a newline" — the file states neither;
   it only *calls* `re2::RE2::FullMatch`. The row now grounds the call and attributes the meaning to RE2's own
   documentation. (Defect class: a `teaches` cell carrying a claim from a source the row does not cite.)
2. **`S347`'s tiled-consumer clause names the fallback** `Window.cpp:2413-2414` and the anchoring file's limit
   (`S164`'s anchor stops at `:2281`, so the row must cite the range it uses).
3. **`S348` says "only write in this file"** and cites the read-back (`:72-74`), so a reader cannot take "only writer"
   as a claim about the program.
4. **`S351` keeps the r46 negative sweeps** and keeps `2027-01-24` as `recheck` (a snapshot ages), while every row
   whose source is a tagged commit carries `on-release`.

---

## 2. The form the census accepts

`CORPUS.md` (fleet root) rule 2, at `CORPUS.md:116-118`: *"Only `status`, `recheck` and `used-by` change in place"*
(9 words, `:116`) and *"A correction is a new row whose `teaches` opens"* (9 words, `:117`), the opener literal
being `supersedes S0NN —` (`:118`).

`scripts/sources-census.sh` decides which form actually passes:

- **A superseding row is legal and the opener is load-bearing.** `E04` (duplicate URL within a scope) is exempted at
  `sources-census.sh:646-649` by `teaches !~ /supersedes S[0-9]{3}/`. Control `m3` (opener stripped) returns
  `E04` x4 — exactly the four rows that keep their predecessor's `scope` verbatim (`S347`-`S350`) — exit 1.
- **Prose is invisible to the census.** Control `m5` (an `## Errata` block appended, no row) returns exit 0 with rows
  still 262 — nothing changed, because no cell changed.
- **A renumbered duplicate id is caught.** Control `m4` (`S346` renumbered onto the live `S325`) returns `E03`, exit 1.
- **`used-by` must exist on disk** (`E11`, resolved against the mirror tree root). Control `m2` returns `E11` x8.

Decision: **new rows**, `S346`-`S353`, appended after the last row of the round's own block.

---

## 3. The rows

`rows-block.txt` in this directory is the exact text to append; it is reproduced here for reading. One line per row,
11 cells (12 pipes), no `|` inside a cell; `shape-check.txt` reports `8/8 OK, defects=0`.

- `S346` supersedes `S290` — narrowed `scope` (the regex test an engine applies to a rule string), `teaches` grounds
  the `FullMatch` call and the `negative:` strip, and names the class linkage as `S353`/`S157` instead of claiming it.
- `S347` supersedes `S291` — title narrowed to the floating first-map consumer; `teaches` adds the parse gate
  (`:56-58`), the overwrite (`:60-61`), the center gate (`:79-84`), the no-position re-center (`:90-91`), the work-area
  re-center (`:93-102`); names the tiled consumer `Window.cpp:2402-2409` and the clamp as `S349`.
- `S348` supersedes `S292` — the only write in the file (`:68-70`), the read-back (`:72-74`), the caller elsewhere
  (`DefaultFloatingAlgorithm.cpp:193-196`), and the file's silence about client reports.
- `S349` supersedes `S293` — title drops the "request" premise; `teaches` adds `:313`, `:323-326`, the `||` at `:339`,
  the `> 5` gate at `:342-347`, the `{600, 400}` branch `:350-362` and the failure return `:364`.
- `S350` supersedes `S294` — the two reads `:19`/`:20`, the same split for position (`:10-11`) and box (`:26-29`), and
  the file's silence about drawing.
- `S351` supersedes `S296` — what the dump held, the seven keys, no `gkeep` entry, absence at that moment is not
  "never mapped", and no `fullscreen` field.
- `S352` supersedes `S297` — a default size, not a request; excerpt-relative `:6`/`:33` mapped to `ui.py:449`/`:476`;
  `set_size_request` absent in both.
- `S353` — new grounding row, no supersession: `Rule.cpp:52` binds `RULE_PROP_CLASS` to the regex engine, `:98`
  constructs it.

`used-by` for all eight: `.ufo/waves/round-47/w1/ExecSupersede/rows.md` (this file). Precedent for a `.ufo/` used-by
target exists in the lane (`S184`, `S185`). The alternative — `corpus/lessons/round-47.md` — does not exist yet and
returns `E11` x8 until the L1 writes it (measured: `census-m2.txt`).

**Id rule for the L1:** this block claims `S346`-`S353` on the assumption C2 takes `S326`-`S345`. If the round's own
C1/C2 blocks reach past `S345`, shift the whole block to the next free contiguous ids with
`sed -i -E 's/^\| S(34[6-9]|35[0-3]) \|/| S\1 |/'`-style renumbering (the id appears only in cell 2), and keep the
`supersedes S29N` openers pointing at the **predecessors**, not at the new ids.

---

## 4. Gate lines for `corpus/lessons/round-47.md` `## Gate`

Access date **2026-10-26** for every line. Each quote is ≤25 words, appears exactly once in the pinned bytes, and its
line number is computed by `check-quotes.py` (`locators.txt`), not typed.

| row | source | quote (computed line, hits, words) |
|---|---|---|
| `S346` | `…/efb50993/src/desktop/rule/matchEngine/RegexMatchEngine.cpp` | `return re2::RE2::FullMatch(other, *m_regex) != m_negative;` — `:16`, 1 hit, 5 words |
| `S347` | `…/src/layout/algorithm/floating/default/DefaultFloatingAlgorithm.cpp` | `const auto COMPUTED = WINDOW->calculateExpression(*WINDOW->m_ruleApplicator->static_.size);` — `:56`, 1 hit, 5 words |
| `S348` | `…/src/layout/target/Target.cpp` | `void ITarget::rememberFloatingSize(const Vector2D& size) {` — `:68`, 1 hit, 5 words |
| `S349` | `…/src/layout/target/WindowTarget.cpp` | `if (DESIRED_GEOM.width <= 2 \|\| DESIRED_GEOM.height <= 2) {` — `:339`, 1 hit, 9 words |
| `S350` | `…/src/desktop/view/types/GeometricMovableAnimated.cpp` | `case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();` — `:19`, 1 hit, 4 words |
| `S351` | `.ufo/waves/round-43/fetch/host-clients-r43.json` (own-work) | `"class": "Alacritty",` — `:5`, 1 hit, 2 words; sweeps `grep -c fullscreen` = 0, `grep -c title` = 0, `grep -c org.omarchy.gkeep` = 0 |
| `S352` | `.ufo/waves/round-43/fetch/gkeep-ui-excerpt.py` (own-work) | `window.set_default_size(420, 500)` — excerpt `:33` (= `ui.py:476`), 1 hit, 2 words; sweep `grep -c set_size_request` = 0 in the excerpt and in `ui.py` |
| `S353` | `…/src/desktop/rule/Rule.cpp` | `{RULE_PROP_CLASS, RULE_MATCH_ENGINE_REGEX},` — `:52`, 1 hit, 2 words |

Pins re-fetched today, byte-equal to the round-43 and round-46 receipts in the lane:

| file | bytes | sha256 (16) |
|---|---|---|
| `RegexMatchEngine.cpp` | 470 | `8ca655336cd111df` |
| `DefaultFloatingAlgorithm.cpp` | 10359 | `f05f256150c8dcf5` |
| `Target.cpp` | 3064 | `49323833c6bc3276` |
| `WindowTarget.cpp` | 16614 | `8bcaf37000cf55e1` |
| `GeometricMovableAnimated.cpp` | 1576 | `649f1a8d01d28e20` |
| `Rule.cpp` | 6835 | `257687efd814cb71` |
| `WindowRule.cpp` (held `S157`) | 19588 | `7034c3325fee476c` |
| `Window.cpp` (held `S164`) | 124226 | `d735d454cc4b7983` |
| `host-clients-r43.json` (own-work) | 711 | `21db902e1f1234b9` |
| `gkeep-ui-excerpt.py` (own-work) | 1625 | `3695b788c6d766b8` |

All eight `.cpp` are `curl` outputs of
`https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/<path>`, kept in
`fetch/` with the `Hyprland-` prefix; `cmp` against the round-46 seat copies: 8/8 byte-equal.

---

## 5. Census proof

`bash mirror.sh <scratch>/mirrors` copies the lane tree once (no `.git`/`.jj`) and applies one variant at a time.
A `corpus/`-only mirror cannot be used: `--file` resolves `used-by` against the file's grandparent
(`sources-census.sh:498-503`), so it would fail on paths the round does not touch.

| variant | what it applies | exit | rows | findings |
|---|---|---|---|---|
| `m0` | nothing (baseline) | **0** | 262 | 0 E, 15 W (`W04` x14, `W01` x1) |
| **`m1`** | **the eight rows (recommended landing)** | **0** | **270** | **0 E, 16 W (`W04` x15, `W01` x1)** |
| `m2` | rows, `used-by` = `corpus/lessons/round-47.md` (absent) | 1 | 270 | `E11` x8 |
| `m3` | rows with the `supersedes S34N —` opener stripped | 1 | 270 | `E04` x4 (`S347`-`S350`) |
| `m4` | `S346` renumbered onto the live `S325` | 1 | 270 | `E03` x1 (duplicate id) + a `W04` on the renumbered row |
| `m5` | `## Errata` prose appended, no new row | 0 | 262 | 0 E, 15 W (no cell changed) |

`census-m1.txt` ends `file<TAB>ok<TAB><mirror>/corpus/SOURCES.md`. The single new warning in `m1` is `W04` for
`S346`: its `scope` was deliberately narrowed, so its URL now sits under a different scope than `S290`'s. Every other
superseding row keeps its predecessor's `scope` verbatim, so the warning set grows by exactly one and a reader can
diff the scope cells and see that only the wrong ones moved.

---

## 6. Locator and shape receipts

- `check-quotes.py` → `locators.txt`, last line `QUOTE_AND_RANGE_CHECK: ok`. It asserts, per row: the quote occurs
  **exactly once**, on the computed line of the pinned bytes; ≤25 words; sha256 of the file it read; every `:N`/`:N-M`
  token inside each primary-source anchor cell is in bounds; the own-work anchors sit on the line they describe
  (`:2,17,32,47` object openers, `:5,20,35,50` class lines, excerpt `:6`/`:33`); and the four negative sweeps.
  34 anchor ranges are printed with their first and last source line.
- `shape-check.txt` — 8/8 rows `OK`, `defects=0`: 11 cells, 12 pipes, enums valid, ids `S346..S353` contiguous and
  ascending, one `used-by` value across the block, `opened` = `2026-10-26`, and a `supersedes S…` opener on all but
  `S353`.
- `census-m0.txt` … `census-m5.txt` — the six variant runs.
- `fetch/` — the ten pinned sources re-read today.

---

## 7. What the L1 does to land this

1. Append `rows-block.txt` immediately after the **last row of the round's own block** (after C2's `S326`- and any C1
   rows), inside `## Registry` and before `## Paths`. 262 rows now → 270 after.
2. Paste the §4 Gate rows into `corpus/lessons/round-47.md` `## Gate` and add a
   `## Registry changes logged old→new (CORPUS.md rule 2)` section naming `S346`-`S353` with the predecessor each
   supersedes and `S295` explicitly **not** superseded (reason in §1).
3. Nothing else changes: `S290`-`S297` stay byte-identical (append-only). A reader who follows `S293` now also meets
   `S349`.
4. Keep this seat directory: `S353`'s anchor and all eight `used-by` cells name paths inside it.

---

## 8. Optional in-place changes (rule 2 allows them; none is required)

Only `status`, `recheck`, `used-by` may change in place, each logged old→new. Proposed, not needed for the
correction to be visible (the new rows name their predecessors):

| row | cell | old | new | why |
|---|---|---|---|---|
| `S290`-`S294` | `used-by` | `corpus/knowledge/hyprland-gkeep-geometry-r43.md` | same + `, corpus/lessons/round-47.md` | a reader arriving at a superseded row meets the correction on the same line, once the lesson exists |
| `S295`-`S297` | `used-by` | `corpus/knowledge/hyprland-gkeep-geometry-r43.md` | same + `, .ufo/waves/round-47/w1/ExecSupersede/rows.md` | the own-work snapshots are re-read here |

No `status` or `recheck` change is proposed: none of the seven is overdue (`opened` 2026-10-26, `recheck`
`on-release` or `2027-01-24`) and none changes state.

---

## 9. Limits

- The census checks shape, enums, ids, URLs and `used-by` existence — not the truth of a cell. The truth is
  `locators.txt`, which is my own computed output; a non-author should re-run `python3 -I check-quotes.py` against the
  same `fetch/`.
- `S346`'s narrowed `scope` costs exactly one new `W04`. Keeping the old scope would be warning-neutral and would
  leave the defect.
- `S351`/`S352` are own-work rows: the quote grounds a structural line (a class line, a default-size call) while the
  corrected clauses are negative claims, so each carries a sweep instead of a positive quote for that half.
- The round-43 entry (`corpus/knowledge/hyprland-gkeep-geometry-r43.md`) repeats some of the `S293`/`S297`
  imprecision; it is a tracked knowledge file and is not edited here — rule 2 corrections are registry rows.
- Ids are a proposal: the block is contiguous and free at HEAD, but the L1 owns the final numbering after the round's
  own rows land.

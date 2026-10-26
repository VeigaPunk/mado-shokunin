# ExecSupersede — S290-S297 supersession re-verified (round 47 w1, item R4a)

Target: the S290-S297 supersession block drafted in round-46 (`M46-16`, carried by round-43 D2, round-44 D6,
round-45 D6). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, base `60edb66e`, HEAD at work time `c24adef2`.
Registry at HEAD: **262 rows, top `S325`, no `S326+`** — the round-46 block was never landed
(`registry-state.txt`). Everything below is re-derived from re-fetched bytes today, not copied from round-46.

## Files written (all untracked, inside the lane)

- `.ufo/waves/round-47/w1/ExecSupersede.md` — this report.
- `.ufo/waves/round-47/w1/ExecSupersede/rows.md` — the deliverable: defect table, form decision, the eight rows,
  the Gate lines, the census proof, landing steps, optional in-place changes, limits.
- `.ufo/waves/round-47/w1/ExecSupersede/rows-block.txt` — **the exact eight rows** to append (`S346`-`S353`).
- `.ufo/waves/round-47/w1/ExecSupersede/fetch/` — the ten pinned sources read today (`fetch-sha256.txt`).
- `.ufo/waves/round-47/w1/ExecSupersede/{check-quotes.py,locators.txt,shape-check.txt,mirror.sh,diff-append-only.txt,registry-state.txt,census-m0.txt…census-m5.txt}`
  — the computed receipts.

`git status --porcelain` shows only untracked `.ufo/` paths; `git diff --stat -- corpus/SOURCES.md` is empty. No
tracked lane file was edited, no pacman or package transaction ran, no compositor command was issued, no terminal or
GUI program was launched, and the only network access was the eight `raw.githubusercontent.com` URLs of commit
`efb50993`. No tool was installed.

## Behaviour — what the block does when the L1 lands it

Eight new rows continuing after the round's own block, seven opening `teaches` with `supersedes S29N —`
(`S290`, `S291`, `S292`, `S293`, `S294`, `S296`, `S297`) per `CORPUS.md` rule 2, plus one grounding row `S353` for
`Rule.cpp` — the one source the `S290` correction needs that no row holds. `S295` is **not** superseded: its
`teaches` already limits itself and round-43 `w2` found no defect in it.

| new | supersedes | what the cell now says |
|---|---|---|
| `S346` | `S290` | `scope` narrowed to "the regex test an engine applies to a rule string" (the file has no class linkage: `grep -ci 'RULE_PROP_CLASS\|WindowRule\|m_class'` = 0); `teaches` grounds the `FullMatch` call and the `negative:` strip, and **attributes the whole-string/unescaped-dot semantics to RE2's own docs** rather than to this file; class binding named as `S353` / held `S157` |
| `S347` | `S291` | title narrowed to the floating first-map consumer; adds `:56-58` parse gate, `:60-61` overwrite, `:79-84` center gate, `:90-91` no-position re-center, `:93-102` work-area re-center; names the tiled consumer `Window.cpp:2402-2409` + fallback `:2413-2414` |
| `S348` | `S292` | drops the "geometry a window reports" inference (the file never says client/report/mapped: `grep -ci` = 0); states the only write in the file (`:68-70`), the read-back (`:72-74`), the caller elsewhere (`DefaultFloatingAlgorithm.cpp:193-196`) |
| `S349` | `S293` | title drops the "request" premise; adds `:313`, the `:323-326` stored-size override, the `\|\|` at `:339`, the `> 5` gate `:342-347`, the `{600, 400}` branch `:350-362`, the failure return `:364` |
| `S350` | `S294` | the two reads `:19`/`:20` and the same split for position `:10-11` and box `:26-29`; the file's silence about drawing stated (no `draw|render|screen|damage`: `grep -ci` = 0) |
| `S351` | `S296` | what the dump held, the seven keys per object, no `gkeep` entry, absence at that moment ≠ "never mapped", no `fullscreen` field |
| `S352` | `S297` | a default size, not a request; excerpt-relative `:6`/`:33` mapped to `ui.py:449`/`:476`; `set_size_request` absent in both |
| `S353` | — | `Rule.cpp:52` binds `RULE_PROP_CLASS` to `RULE_MATCH_ENGINE_REGEX`, `:98` constructs the `CRegexMatchEngine` |

Ids: the round-46 draft's `S326`-`S333` are **taken** this round by C2 (`claims.md`: "rows S326.. opened this
round"), so the block is renumbered to `S346`-`S353` per the assignment. If the round's own C1/C2 rows run past
`S345`, the L1 shifts the block to the next free contiguous ids; the id appears only in cell 2 and the
`supersedes S29N` openers keep pointing at the predecessors.

## Exact retained evidence

1. **Pins re-fetched today, byte-equal to both earlier receipts.** `curl` of the eight `.cpp` at
   `efb50993780079460b0cbed1363e2166a2de1d9f` → `470`/`10359`/`3064`/`16614`/`1576`/`6835` B with sha256
   `8ca65533…`/`f05f2561…`/`49323833…`/`8bcaf370…`/`649f1a8d…`/`257687ef…`; the two held cross-refs
   `WindowRule.cpp` `7034c332…` (19588 B, = `S157`) and `Window.cpp` `d735d454…` (124226 B, = `S164`).
   `cmp` against `.ufo/waves/round-46/w1/ExecSupersede/fetch/`: **8/8 byte-equal**.
   Own-work pins unchanged: `host-clients-r43.json` 711 B `21db902e…`, `gkeep-ui-excerpt.py` 1625 B `3695b788…`;
   `ui.py` re-read at 14639 B / 488 lines / `07a3c4a4…` with `application_id` at `:449`, `set_default_size(420, 500)`
   at `:476`, `grep -c set_size_request` = 0.
2. **Computed locators** — `python3 -I check-quotes.py` → `locators.txt`, last line `QUOTE_AND_RANGE_CHECK: ok`:
   eight Gate quotes each with computed line, **hit count 1**, word count ≤25 and the sha256 of the file read;
   34 anchor ranges printed with their first and last source line; every `:N`/`:N-M` token in each primary-source
   anchor cell bounds-checked; the own-work anchors checked line by line (`:2,17,32,47` object openers,
   `:5,20,35,50` class lines, excerpt `:6`/`:33`); the four negative sweeps (`fullscreen` 0, `title` 0,
   `org.omarchy.gkeep` 0, `set_size_request` 0).
3. **Form decided by the census, not by taste** — `bash mirror.sh <scratch>/mirrors`, whole-lane mirror
   (`--file` resolves `used-by` against the file's grandparent, `sources-census.sh:498-503`, so a `corpus/`-only
   mirror cannot prove anything):

   | variant | applies | exit | rows | findings |
   |---|---|---|---|---|
   | `m0` | nothing | 0 | 262 | `W04` x14, `W01` x1 |
   | **`m1`** | **the eight rows** | **0** | **270** | **0 E**, `W04` x15, `W01` x1 — last line `file ok` |
   | `m2` | `used-by` = a path that does not exist | 1 | 270 | `E11` x8 |
   | `m3` | `supersedes` opener stripped | 1 | 270 | `E04` x4 (`S347`-`S350`) |
   | `m4` | `S346` renumbered onto the live `S325` | 1 | 270 | `E03` x1 + a `W04` |
   | `m5` | `## Errata` prose, no row | 0 | 262 | nothing changed — prose edits no cell |

   The one new warning in `m1` is `W04 S346`, the honest record that one URL now sits under a narrowed scope;
   it is the only cell whose `scope` moves. The opener is load-bearing (`m3`), a duplicate id is caught (`m4`).
4. **Append-only, measured** — `diff-append-only.txt`: 8 added lines, 0 removed or changed, rows 262 → 270, block
   inserted before `## Paths` (line 276 of the pristine file). `S290`-`S297` stay byte-identical.
5. **Shape** — `shape-check.txt`: `8/8 OK`, `defects=0` (11 cells / 12 pipes, enums, ids contiguous and ascending,
   one `used-by` across the block, `opened` = `2026-10-26`, opener present on all but `S353`).

## Findings — what each attacks or supports

- **Supports the target.** The seven cell defects are real on today's bytes, not stylistic: `S292`'s tail is absent
  from `Target.cpp` (0 hits for client/report/mapped), `S294`'s tail is absent from its file (0 hits for
  draw/render/screen/damage), `S293`'s `teaches` lacks the `||`, the `>5` gate, the `{600,400}` branch, the failure
  return and the `:323-326` override, and `S290`'s `scope` names a class linkage its file does not contain. All seven
  superseded, none rewritten.
- **Attacks the round-46 draft, narrowly.** Its `S346` `teaches` ended "…so a leading `^` and a trailing `$` add
  nothing and an unescaped `.` matches any character except a newline" — neither statement is in
  `RegexMatchEngine.cpp`, which only *calls* `re2::RE2::FullMatch`. My row grounds the call and attributes the
  semantics to RE2. Same class of defect the row is meant to fix, one level down.
- **Attacks the round-46 draft's `S347` cross-ref.** It said `S164`'s anchor "stops at `:2281`"; `S164` actually
  covers `:103-108,141-146,1484-1486,1791-1795,2143-2281,2497`. The row now states the real coverage and that
  `:2402-2414` is outside it.
- **Attacks a natural reading of `CORPUS.md` rule 2.** A prose erratum changes no cell (`m5`, rows still 262) and a
  row-shaped table outside `## Registry` is `E12`; the accepted form is a superseding row and its opener is what
  makes the duplicate URL legal (`m3`).
- **Supports round-44's finding 1 with a computed locator.** `round-44/w1/ScrSupersedeRows.md:73` is the finding;
  `round-43/w2/ScoutRowsD/` really is empty. The `S296`/`S297` defects exist but were not found by round-43 `w2`.
- **Attacks the round-43 verifier's S293 verdict, mildly.** `corpus/lessons/round-43-verifier-spotcheck.md:79` says
  the `S293` `teaches` "is correct"; `round-43/w2/ScoutRowsB/rows.md:44` found three imprecisions in it. Both are
  true of different cells (D2 was about the title); the lesson should say which.

## Risks

1. **Id claim.** `S346`-`S353` assume C2 takes `S326`-`S345`. If the round's own rows land past `S345`, the block
   must be renumbered (recipe in `rows.md` §3), not interleaved.
2. **One new warning.** `S346`'s narrowed `scope` adds exactly one `W04`. Keeping the old scope would be
   warning-neutral and would leave the defect.
3. **Own-work rows and negatives.** `S351`/`S352` correct clauses that are negative claims, so each Gate line
   carries a sweep as well as a quote; a reader wanting a positive grounding for "never mapped" will not find one,
   because the dump cannot supply it.
4. **Self-computed truth.** `locators.txt` is my own script. A non-author should re-run
   `python3 -I check-quotes.py` against `fetch/` before landing; it fails loudly on any drift.
5. **`used-by` target.** All eight rows point at `.ufo/waves/round-47/w1/ExecSupersede/rows.md` (precedent:
   `S184`, `S185`). If the L1 prefers `corpus/lessons/round-47.md`, that file must exist first or the census returns
   `E11` x8 (`m2`).

## Blockers

None. The deliverable is a draft the L1 applies; the L1 owns `corpus/SOURCES.md`. Scratch
`/fast/scratch/hyaku/mado-r47/ExecSupersede/` removed after the receipts were copied into the seat directory.

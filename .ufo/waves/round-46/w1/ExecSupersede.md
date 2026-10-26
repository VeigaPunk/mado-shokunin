# ExecSupersede — round 46 w1 seat report

Target: round-44 D6, carried a second time by round-45 D6 — a census-clean supersession of the imprecise
`S290`-`S297` cells in `corpus/SOURCES.md`. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, base
`b22ea56bff2faec39ce9ff75d2107eaf4612ecbe`, freeze `8c5434c60e03f147ee1f75ab195e8bc3f0db4dec`. Registry at
base and at HEAD `e0be61e4`: 252 rows, top `S315` (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'
corpus/SOURCES.md` → `252`; `git diff --stat 8c5434c6 HEAD -- corpus/SOURCES.md` empty).

## Files written (all inside the lane, none tracked)

- `.ufo/waves/round-46/w1/ExecSupersede.md` — this report.
- `.ufo/waves/round-46/w1/ExecSupersede/rows.md` — the deliverable: per-row defect table, form decision, the
  eight rows, the Gate lines, the census proof, the L1 landing steps, limits.
- `.ufo/waves/round-46/w1/ExecSupersede/rows-block.txt` — the eight registry rows, ready to append after `S315`.
- `.ufo/waves/round-46/w1/ExecSupersede/fetch/` — the eight upstream sources re-fetched today (`470`, `10359`,
  `3064`, `16614`, `1576`, `6835`, `19588`, `124226` bytes).
- `.ufo/waves/round-46/w1/ExecSupersede/{check-quotes.py,locators.txt,shape-check.txt,mirror.sh,diff-append-only.txt,census-corpus-only-baseline.txt,census-m0.txt…census-m6.txt}`
  — receipts.

`git status --porcelain` shows only untracked `.ufo/` paths; `git diff --stat -- corpus/SOURCES.md` is empty, i.e.
no tracked lane file was edited. No tool was installed; no pacman, no package transaction, no compositor command
(no `hyprctl` of any kind), no network fetch outside the eight `raw.githubusercontent.com` URLs and one GitHub tree
listing used to resolve three source paths.

## Behaviour — what the supersession does

Eight new rows `S326`-`S333`, continuing after `S325`; seven of them open `teaches` with `supersedes S29N —`
(`S290`, `S291`, `S292`, `S293`, `S294`, `S296`, `S297`), and `S333` is a grounding row for `Rule.cpp`, the one
source the S290 correction needs that no row held. `S295` is deliberately **not** superseded: its `teaches` already
limits itself to "the file alone shows nothing of what the window received" and neither round-43 `w2` nor my
re-open found a defect in it.

Cells corrected, each against re-fetched bytes:

| new | supersedes | corrected |
|---|---|---|
| S326 | S290 | `scope` no longer claims the file binds a class rule to the regex engine; `teaches` keeps the `FullMatch` / `negative:` facts, adds that the binding is `Rule.cpp:52,98` (S333) and `WindowRule.cpp:395-396` (held S157), and names the host pattern text as S295 |
| S327 | S291 | title narrowed to the floating first-map consumer; `teaches` adds the parse gate (`:56-58`), the center gate (`:79-84`), the no-position re-center (`:90-91`), the work-area re-center (`:93-102`), the clamp as S329 and the tiled consumer `Window.cpp:2402-2409`; anchor gains `:193-196` |
| S328 | S292 | `teaches` drops the three-row inference about reported geometry and states the file's own limit: one writer (`:68-70`), caller elsewhere (`DefaultFloatingAlgorithm.cpp:193-196`), nothing about client reports |
| S329 | S293 | title drops the refuted "request" premise; `teaches` adds `:313`, `:323-326`, the `||` at `:339`, the `> 5` gate at `:342`, the 600x400 branch `:350-362` and the failure return `:364`; anchor extended by `:323-326` and `:339-365` |
| S330 | S294 | `teaches` tail ("can differ from what is on screen") removed; the two reads `:19`/`:20` kept, and the file's silence about drawing stated |
| S331 | S296 | `scope`/`teaches`: the seven keys the dump kept, no `fullscreen` field, absence at that moment is not "never mapped" |
| S332 | S297 | title/`anchor`/`teaches`: a default size, not a request; excerpt-relative `:6`/`:33` mapped to `ui.py:449`/`:476`; no `set_size_request` |
| S333 | — | new row: `Rule.cpp:52` binds `RULE_PROP_CLASS` to the regex engine, `:98` constructs it |

## Exact retained evidence

1. **Pins re-fetched today, byte-equal to the round-43 pins.** `curl` of the five pinned files at
   `efb50993780079460b0cbed1363e2166a2de1d9f` → `sha256sum` `8ca65533…`, `f05f2561…`, `49323833…`, `8bcaf370…`,
   `649f1a8d…` at `470`/`10359`/`3064`/`16614`/`1576` B. Cross-refs resolved through the GitHub tree listing
   (`src/desktop/rule/Rule.cpp`, `src/desktop/rule/windowRule/WindowRule.cpp`, `src/desktop/view/Window.cpp`) →
   `257687ef…` (`6835` B), `7034c332…` (`19588` B, = S157's pin), `d735d454…` (`124226` B, = S164's pin).
   Own-work pins unchanged: `21db902e…` (`711` B, 62 lines), `3695b788…` (`1625` B, 45 lines), `ui.py`
   `07a3c4a4…` at HEAD `133b8671` with `application_id` at `:449`, `set_default_size(420, 500)` at `:476`, and
   `grep -c set_size_request` = 0.
2. **Computed locators** — `python3 -I check-quotes.py` → `locators.txt`, ending `QUOTE_AND_RANGE_CHECK: ok`:
   eight quotes each with computed line, hit count and pin comparison, nineteen anchor ranges printed with their
   first and last source lines (`Rule.cpp:52`/`:98`, `WindowRule.cpp:395-396`, `Window.cpp:2402-2409` included),
   and the negative sweeps (`fullscreen` = 0, `title` = 0, `org.omarchy.gkeep` = 0, `set_size_request` = 0 twice).
3. **Form decided by the census, not by taste.** `bash mirror.sh` → variant table
   (`census-m0.txt`…`census-m6.txt`):
   `m0` baseline exit 0 / 252 rows / `W01` x1 `W04` x9; **`m1` the eight rows: exit 0, 260 rows, 0 E,
   `W01` x1 `W04` x10, last line `file ok <mirror>/corpus/SOURCES.md`**; `m2` used-by path missing → `E11` x8
   exit 1; `m3` prose errata block → exit 0 with rows still 252 (no correction visible); `m4` row-shaped errata
   table outside the Registry → `E12` x2 exit 1; `m5` opener stripped → `E04` x4 exit 1 (exactly `S327`, `S328`,
   `S329`, `S330`); `m6` `used-by = —` → `W03` x8 exit 0.
4. **Append-only, measured** — `diff-append-only.txt`: 8 added lines, 0 removed or changed, rows 252 → 260,
   insertion after line 264 (`S315`) and before `## Paths` at 266.
5. **Shape** — `shape-check.txt`: 8/8 rows `OK`, 11 cells (12 pipes), enums valid, ids `S326..S333` contiguous,
   `defects=0`.

## Findings that attack the assignment or support it

- **Supports the target.** The seven cell defects are real on the bytes, not stylistic: the S293 `teaches` omits
  the `||`, the `> 5` gate, the 600x400 branch and the failure return (`WindowTarget.cpp:339,342,350-362,364`);
  S292's last clause is not in `Target.cpp` at all; S294's tail is not in its file; S290's `teaches` mixes a second
  source. All seven now superseded, none rewritten.
- **Attacks the closure's row list, mildly.** Round-43's own `w2` left no finding for `S296`/`S297`
  (`w2/ScoutRowsD/` is an empty directory) although round-43 `w2/ScoutRowsB.md:6` had already named the
  append-only route for `S292`/`S293`. The `S296`/`S297` defects are real but were found by round-44
  `w1/ScrSupersedeRows.md` finding 1 and re-verified here; the lesson should say so.
- **Attacks a natural reading of `CORPUS.md` rule 2.** An errata block does not fix a row the census reads: prose
  changes no cell (`m3`, rows still 252) and a table outside `## Registry` is `E12` (`m4`). The accepted form is
  the superseding row whose `teaches` carries the `supersedes` opener — and the opener is load-bearing (`m5`).
- **Attacks round-44's draft where it was wrong.** Its `S304` said Target.cpp "does not show who writes" the
  floating-size member, but `Target.cpp:68-70` is that writer; the missing fact is the caller
  (`DefaultFloatingAlgorithm.cpp:194`, inside `removeTarget` `:193-196`). `S327`'s anchor now carries that range.
- **A corpus-only mirror cannot prove anything.** `bash sources-census.sh validate --file
  <scratch>/corpus-only/corpus/SOURCES.md` → `E11` x12 exit 1 on untouched rows, because `--file` resolves
  `used-by` against the mirror's parent (`sources-census.sh:538`, existence check `:566`). The proof therefore
  mirrors the lane tree.
  `census-corpus-only-baseline.txt`.

## Risks

1. **Id claim.** `S326`-`S333` are the ids after C2's planned `S316`-`S325`; if another round-46 seat also appends
   rows, the L1 must renumber this block, not interleave it.
2. **One new warning.** `S326`'s narrowed `scope` adds exactly one `W04` (`census-m1.txt`); keeping the imprecise
   scope would be warning-neutral and leave the defect.
3. **Own-work rows and negatives.** `S331`/`S332` correct clauses that are negative claims, so their Gate lines
   carry a sweep command as well as a quote; a reader who wants a positive grounding for "never mapped" will not
   find one, because the dump cannot supply it.
4. **Self-computed truth.** The locator receipt is my own script; a non-author should re-run `check-quotes.py`
   against `fetch/` before landing.
5. **used-by target.** All eight rows point at this seat's `rows.md`, a `.ufo/` path (precedent: `S184`, `S185`).
   If the L1 prefers `corpus/lessons/round-46.md`, the lesson must exist before the rows land or the census returns
   `E11` x8 (`m2`).

## Blockers

None. The work is complete as a draft: rows, Gate lines, census proof and landing steps are in
`.ufo/waves/round-46/w1/ExecSupersede/rows.md`; landing is the L1's (it owns `corpus/SOURCES.md`).

Scratch `/fast/scratch/hyaku/mado-r46/ExecSupersede/` removed after the receipts were copied here.

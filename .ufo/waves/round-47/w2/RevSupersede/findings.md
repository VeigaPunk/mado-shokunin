# RevSupersede — R4a falsify: the S290-S297 supersession block (round 47 w2)

Seat RevSupersede (leaf, w2 FALSIFY). Target: `.ufo/waves/round-47/w1/ExecSupersede/` (the S290-S297
supersession draft, rows S346-S353) against `CORPUS.md` rule 2 and `scripts/sources-census.sh`.
Every check below was run 2026-10-26 by this seat; commands are reproducible as written. Receipts
copied to `receipts/` in this directory; scratch deleted after the run.

**Verdict: the bytes are landable — census-clean, append-only, ids legal, quotes and ranges re-located
today. Four defects in the draft's PROSE (one medium, three low) should be fixed before the L1 follows
it; two residuals belong in the lesson's limits. Nothing blocks `rows-block.txt` itself.**

---

## 1. What holds (recomputed today, not taken from the draft)

| check | command (abridged) | result |
|---|---|---|
| registry state | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`; top-id and S326+ counts; malformed awk | 262 rows, top `S325`, **0** rows ≥S326, malformed=0 — matches the draft's header |
| append-only | apply `rows-block.txt` before `## Paths` on a mirror pristine, `diff` | **0** deleted/modified lines, **8** added (`receipts/append-only-and-noop-sed.txt`) |
| block shape | `awk -F'|'` NF, ids, openers, opened/recheck/used-by | 8 rows × 11 cells (12 pipes), ids `S346..S353` contiguous ascending, `opened` 2026-10-26, one `used-by` value, em dash U+2014 (`e2 80 94`) in all seven `supersedes S29N —` openers, `S353` opener-free as declared |
| ids vs the round | C2 draft rows: `grep -n '^| S3' w1/ScrRows/rows.md` | C2 takes **S326-S338** (13 rows); no w1 seat claims anything in S339-S353 except this block (`grep -rnoE '\| S3(3[9]|4[0-9]|5[0-9]) ' w1/` → only `ExecSupersede/rows-block.txt`) — **no collision** |
| combined landing | C2's 13 rows + this block appended before `## Paths`, entry file touched, census `validate --today 2026-10-26 --file` | **exit 0**, 283 rows, 0 E, 18 W (`receipts/census-combined.txt`) |
| mirror variants | re-ran `mirror.sh` (SEAT repointed to scratch) | m0 0/262/15W · **m1 0/270/16W** · m2 E11×8 · m3 E04×4 (exactly `S347-S350`) · m4 E03×1 + W04 · m5 0/262 — reproduces the draft's §5 table line for line |
| gate quotes | own `grep -n` per quote in `fetch/` (not the seat's script) | all 8 quotes: exactly 1 hit, at the claimed line (`:16`, `:56`, `:68`, `:339`, `:19`, `:5`, `:33`, `:52`); all ≤25 words |
| checker re-run | `python3 -I …/check-quotes.py --out <scratch>` | `QUOTE_AND_RANGE_CHECK: ok`; its `locators.txt`/`shape-check.txt` **byte-identical** to the seat's receipts (not stale) |
| anchor ranges | locators §2 | all 34 ranges' first/last lines match the taught semantics (parse gate `:56-58`, overwrite `:60-61`, center `:79-84`, re-centers `:90-91`/`:93-102`, tiled consumer `Window.cpp:2402-2409` + fallback `:2413-2414`, `{600, 400}` at `:354` inside `:350-362`, failure return `:364`); anchor-cell tokens all in bounds |
| pin digests | `sha256sum fetch/*` | 10/10 equal the digests written in the rows (e.g. `S346` `8ca655336cd111df…`, `S349` `8bcaf37000cf55e1…`) |
| pin byte-equality | `cmp` vs `round-43/fetch` and `round-46/w1/ExecSupersede/fetch` | 5 cpp + both own-work files equal to r43; **8/8 cpp equal to r46**; `Window.cpp`/`WindowRule.cpp` digests equal held `S164`/`S157` anchor digests (`d735d454…`, `7034c332…`); all 10 mtimes 2026-10-26 |
| ui.py re-check | `sha256sum ~/Projects/gkeep/gkeep/ui.py`; `wc -l`; `grep -c set_size_request`; `sed -n 449p;476p` | `07a3c4a50bf2154e…` ✓, 488 lines ✓, 0 ✓, `:449` application_id ✓, `:476` set_default_size(420, 500) ✓ — the S352 anchor's claims hold today |
| dump fields | python json read | 4 objects, each with exactly `address, at, class, floating, mapped, monitor, size`; all mapped=True floating=False size=[1720,1414]; classes Alacritty/zcode/grok-bot/chromium — matches `S351`'s anchor |
| rule 2 text | `grep -n "Append-only" /home/vgpnk/Projects/shokunin/CORPUS.md` | `:116-118`, both quotes verbatim; opener literal `supersedes S0NN —` at `:118` |
| census internals | `grep -n` in `scripts/sources-census.sh` | E03 `:641`, W04 `:644-645`, E04 exemption `teaches !~ /supersedes S[0-9]{3}/` `:646-649`, E11 mined-only `:567`, `--file` grandparent `dir_abs=…/..` `:501` (draft cited `:498-503`) — all as the draft reads them |
| url_of | `sources-census.sh:600-608` | matches only `https?://…` — path-only own-work sources (`S351`/`S352`) get u="" and no E04/W04 |
| S295 exclusion | teaches cell of `S295` | verbatim contains "the file alone shows nothing of what the window received" — the not-superseded rationale is grounded |
| §1 "found by" | `sed -n` at each cited line | `ScoutRowsA:18,20,36,40`; `ScoutRowsB:23,44`; `ScoutRowsC:59`; `ScoutRowsD/` empty; r44 `ScrSupersedeRows.md:73,82-83`; `round-43-verifier-spotcheck.md:100`; M46-16 `corpus/lessons/round-46.md:307` — all present and say what the draft claims |
| used-by precedent | `S184`/`S185` used-by cells | `.ufo/waves/round-29/registration.md, corpus/lessons/round-29.md` — `.ufo/` used-by targets have lane precedent |
| S353 E04 risk | `grep -c 'desktop/rule/Rule.cpp' corpus/SOURCES.md` | 0 — URL not already held, no E04/W04 for `S353` |
| W04 delta | m1 W list | exactly one new W04, on `S346` (narrowed scope); W01 = pre-existing `S277` |

---

## 2. Holes — what must change before it lands

### H1 (medium) — the §3 id-shift example command is a no-op
`rows.md` §3 tells the L1 to shift ids "with `sed -i -E 's/^\| S(34[6-9]|35[0-3]) \|/| S\1 |/'`-style
renumbering". The pattern replaces each id **with itself** — run it and nothing changes:

```
$ echo '| S346 | test |' | sed -E 's/^\| S(34[6-9]|35[0-3]) \|/| S\1 |/'
| S346 | test |          # unchanged
```

An L1 who follows the example verbatim "shifts" nothing and may not notice. Fix: give a real mapping
(e.g. an awk/python one-liner that rewrites cell 2 by an offset) or drop the command and keep only the
rule ("the id appears only in cell 2; keep the `supersedes S29N` openers pointing at the predecessors").

### H2 (low) — the id bound is misattributed to claims.md
`rows.md` header and §3 say the block lands at S346+ because "this round's own C2 entry takes
`S326`-`S345` (`claims.md`: 'on rows S326.. opened this round')". `claims.md:16` says only "S326.."
(open-ended — no S345); the actual C2 draft tops at **S338** (`w1/ScrRows/rows.md:14-26`). The
S326-S345 bound really comes from the ExecSupersede **seat prompt** and is codified in the lesson
draft's own R4a criterion: `w1/ScrLesson/lesson.md:203-205` "Fails if a row id lands inside `S326`-`S345`
(the C2 range)" (also `ScrLesson.md:62,72,103`). The conclusion (S346+) is correct and the lesson
criterion is satisfied; the citation is wrong. Fix the sentence so a non-author re-deriving the bound
does not hunt in claims.md.

### H3 (low) — word-count slip in §2
The draft counts the `:116` quote "Only `status`, `recheck` and `used-by` change in place" as 9 words;
it is **8** (the `:117` quote is 9). Trivial, but the draft presents these as precise counts.

### H4 (low) — §6 misdescribes where the ok line lives
"`check-quotes.py` → `locators.txt`, last line `QUOTE_AND_RANGE_CHECK: ok`" — that line goes to
**stdout**; the `locators.txt` file ends `defects=0`. A reader checking the file's last line sees the
wrong thing.

### Landing prerequisites (declared by the draft, still open — the L1 must do them)
- The lesson draft's `## Gate` (`ScrLesson/lesson.md:15`) does **not** yet carry the eight R4a gate-quote
  lines (S346/S347/S353 appear only twice in the whole lesson draft, in tables). Rule 1 requires the
  Gate entry for every new row — §7 step 2 is load-bearing, not optional.
- `used-by` = `.ufo/waves/round-47/w1/ExecSupersede/rows.md` for all eight rows: the L1 must keep this
  seat directory, or E11 fires ×8 (measured: mirror variant m2).

---

## 3. Residuals (no change required; one line each for the lesson's limits)

- **R1 — census is blind to own-work path sources.** `url_of` (`sources-census.sh:600-608`) matches only
  http(s) URLs, so `S351`/`S352` (source = a `.ufo/` path) get no E04/W04 protection: a duplicate
  own-work source is census-invisible. The supersedes openers are present, and the predecessors
  `S296`/`S297` carry the identical source cells, so the correction is still visible to a reader.
- **R2 — staged fleet merge collides with this block if adopted unrenumbered.** The staged merge file
  `/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md` spans **S203-S349** (147 rows;
  `w1/ExecIdGuard.md`). Its `S346-S349` collide with this block and its `S326-S338` with C2's rows.
  `w1/ScoutShokuknow/report.md:28` already says never to run adopt-step 3 "without renumbering past this
  round's last S-row" — after this block lands that is **S353**, not S345. One line for the L1's
  integration checklist.
- **R3 — observation on S347's cross-file clause.** The `Window.cpp:2402-2409`/`:2413-2414` clause in
  `S347`'s teaches has no §4 Gate quote (rule 1 needs one quote per row, which exists — for
  `DefaultFloatingAlgorithm.cpp:56`). The clause is grounded by the block's `fetch/Hyprland-Window.cpp`
  copy whose digest equals held `S164`'s pinned digest (`d735d454…`), and `check-quotes.py` §2 verifies
  both ranges. Acceptable; the lesson can note that cross-file clauses ride on anchor digests.

---

## 4. Verification gaps

- The truth of the corrected `teaches` cells rests on `locators.txt` (the author's own script) plus this
  seat's independent grep of the 8 gate quotes and the 34 range first/last lines. I did not re-derive
  every prose clause of every corrected row against the pins beyond what `check-quotes.py` §2 prints and
  the sweeps cover; a non-author wanting more can re-run
  `python3 -I .ufo/waves/round-47/w1/ExecSupersede/check-quotes.py --out <scratch>` (exit 0 today).
- I did not re-fetch the pins from the network this round; byte-equality to the round-43/round-46
  receipts and the rows' digests is the evidence (all verified). The URLs are in the rows for a future
  re-check.

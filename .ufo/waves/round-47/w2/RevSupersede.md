# Report — RevSupersede (round 47 w2, R4a: S290-S297 supersession block)

Seat: RevSupersede (leaf, w2 FALSIFY). Target: `.ufo/waves/round-47/w1/ExecSupersede/` checked against
`CORPUS.md` rule 2 (`:116-118`) and `scripts/sources-census.sh`. Full findings + reproducible commands:
`.ufo/waves/round-47/w2/RevSupersede/findings.md`; receipts in `.ufo/waves/round-47/w2/RevSupersede/receipts/`.

**Verdict: the block (rows S346-S353 in `rows-block.txt`) is landable as-is.** Every acceptance criterion
re-verified today (2026-10-26) by independent recomputation:

- **Append-only** — applying the block to a mirror pristine diffs as 8 added lines, 0 deleted/modified.
- **Ids** — S346-S353 contiguous, unique; C2's actual draft rows take S326-S338 (`w1/ScrRows/rows.md:14-26`),
  no w1 seat claims S339+ except this block; the S326-S345 reservation is the lesson draft's own R4a
  criterion (`w1/ScrLesson/lesson.md:203-205`) and the block complies. Combined landing test (C2's 13 rows +
  block = 283 rows): census `validate --today 2026-10-26 --file` **exit 0, 0 E**.
- **Quotes re-located today** — all 8 gate quotes: exactly 1 hit at the claimed line by my own `grep -n` in
  the lane's `fetch/` pins; `check-quotes.py` re-run `ok`, byte-identical receipts (not stale); all 34 anchor
  ranges' first/last lines match the taught semantics; 10/10 pin sha256 match the rows; byte-equal to the
  round-43/46 receipts; ui.py re-check holds today (`07a3c4a5…`, 488 lines, `set_size_request`=0).
- **Mirror census exit 0** — all six variants reproduce the draft's §5 table exactly (m1: exit 0, 270 rows,
  0 E, 16 W; the single new W04 is S346's narrowed scope, declared).

**Must change before it lands (draft prose, not the bytes):**

1. **H1 (medium)** — §3's id-shift example `sed -i -E 's/^\| S(34[6-9]|35[0-3]) \|/| S\1 |/'` is a **no-op**
   (replaces each id with itself; proven by run). An L1 following it verbatim shifts nothing. Give a real
   renumber command or state the rule only.
2. **H2 (low)** — the S326-S345 bound is attributed to `claims.md`, which says only "S326.." (`claims.md:16`);
   C2's draft tops at S338. The bound's real sources: the seat prompt and `ScrLesson/lesson.md:203-205`.
   Fix the citation.
3. **H3 (low)** — §2 counts the `:116` quote as 9 words; it is 8.
4. **H4 (low)** — §6 says `locators.txt`'s last line is `QUOTE_AND_RANGE_CHECK: ok`; that line is stdout —
   the file ends `defects=0`.

**Landing prerequisites (declared, still open):** the lesson draft's `## Gate` does not yet carry the eight
R4a gate-quote lines (rule 1 requires them — §7 step 2 is load-bearing); the L1 must keep the seat directory
or E11 fires ×8 on the `used-by` cells.

**Residuals for the lesson's limits:** the census cannot see duplicate own-work path sources (`url_of`
matches only http(s) — S351/S352 unprotected, openers present); the staged fleet merge
(`SOURCES.append.md`, S203-S349 per `w1/ExecIdGuard.md`) collides with this block's S346-S349 and C2's
S326-S338 if ever adopted unrenumbered — after this block lands, the merge renumber must clear **S353**.

No tracked file edited; no git/jj mutation; writes confined to this seat directory. Scratch
`/fast/scratch/hyaku/mado-r47/RevSupersede` deleted. No tools installed.

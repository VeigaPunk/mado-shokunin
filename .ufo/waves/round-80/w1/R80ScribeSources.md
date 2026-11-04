# Seat R80ScribeSources — SOURCES.md rows for round 80

Lane: `mado-shokunin`. Round 80 (hyaku run 15), ONE v1 wave. Freeze
`6c302a53eb8f577e83fbcadc01e05a286778df8e`, base
`e10f7e9f528b13195a1cdde28a68a702af3045c4`. Leaf seat: no dispatch, prose only.

## Behavior

Read the `corpus/SOURCES.md` Registry shape (11 columns, house anchors, `teaches` conventions)
and `corpus/lessons/round-79.md` § Gate for the row/quote style, then drafted the six registry
rows S470–S475 in `.ufo/waves/round-80/w1/R80ScribeSources/sources-rows-r80.md` (§1 rows, §2
the six located Gate quotes, §3 deltas, §4 verification, §5 limits). Every cell was
re-derived from the frozen bytes under `.ufo/waves/round-80/fetch/`, not copied from the
declaration: the shared spans, the `applyExclusive` match predicate, the protocol refusal, the
test's assertion set, the printed column width, the `is-active` contract and the round-45
stacking sentence were each read at their own line number.

`corpus/SOURCES.md` already carried S470–S475 at `:421-426` (mtime 08:39, before this seat
settled), so the draft is a re-derivation plus a cell-by-cell delta rather than an append. I
appended nothing and rewrote nothing.

## Gates run (all read-only)

| gate | command | result |
|---|---|---|
| fetch manifest | `sha256sum -c sha256-r80.txt` (fetch dir) | 5/5 OK, rc 0; no self-entry (M79-5 does not recur) |
| sizes | `stat -c '%s'` | 143211 / 9935 / 1532 / 8064 / 337 B, matching every cited size |
| registry shape | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | last line `mado ok …/corpus/SOURCES.md`, rc 0, no E01/E02; two expected W04 lines: `S470 duplicate url …/Renderer.cpp` (with S457) and `S475 duplicate url wiki.hypr.land/Configuring/Monitors` (with S467) |
| installed payload byte-equal | `cmp ~/.local/share/omarchy/bin/omarchy-menu-keybindings fetch/S473.txt` | identical; `sha256sum` of the installed file = `3487bbb8…` |
| payload provenance | `git -C ~/.local/share/omarchy` reads only (`rev-parse`, `show HEAD:version`, `status --porcelain`, `tag --points-at HEAD`) | HEAD `8fcc9d6048af4cb0e3af8512c78049857a3b53dd`; `version` = `3.8.3`, tracked and clean; HEAD tagged **v3.8.4**; file last touched `d2a4cc0c`, 2026-05-01 |
| man-page quote | `MANWIDTH=80 MANPAGER=cat man systemctl` | `is-active PATTERN...` at 189, paragraph 190-193, byte-equal to `S474.txt:3-7`; `pacman -Q systemd` → `systemd 262.1-1` |

## Touched surfaces

- Written: `.ufo/waves/round-80/w1/R80ScribeSources/sources-rows-r80.md` (the draft) and this
  report at `.ufo/waves/round-80/w1/R80ScribeSources.md` plus
  `.ufo/waves/round-80/w1/R80ScribeSources/findings.md` (same content). Nothing else.
- Scratch `/fast/scratch/hyaku/mado-r80/R80ScribeSources` created and removed (verified absent).
- No git/jj mutation, no commit, no push, no package transaction, no service action, no
  compositor/config write. Host probes were read verbs only (`sha256sum`, `stat`, `cmp`, `git
  rev-parse/show/status/tag/log`, `man` render, `pacman -Q`).
- Not touched: the frozen instruments, both control sets, the fixtures, `SKILL.md`,
  `SCORECARD.md`, `LOG.md`, `corpus/` (read only), the fleet repo, sibling lanes.

## Findings

**F1 — S473's mask count is not reproducible from the bytes (factual; the one worth fixing
before the lesson repeats it).** The committed row at `corpus/SOURCES.md:424`, the seat brief
and the claims declaration all say the sed table renders "twelve masks" over `:100-120`. The
bytes: `S473.txt:100-115` holds **sixteen** `s/^N,/` rules — `^0,` (strip the mask) plus
fifteen modifier sets (`1 SHIFT`, `4 CTRL`, `5 SHIFT CTRL`, `8 ALT`, `9 SHIFT ALT`, `12 CTRL
ALT`, `13 SHIFT CTRL ALT`, `64 SUPER`, `65 SUPER SHIFT`, `68 SUPER CTRL`, `69 SUPER SHIFT
CTRL`, `72 SUPER ALT`, `73 SUPER SHIFT ALT`, `76 SUPER CTRL ALT`, `77 SUPER SHIFT CTRL ALT`).
`:116` is `}` and `:119-121` is `static_bindings`, so `:100-120` overshoots the table into the
next function. Neither 12 nor 120 follows from the file, and no arithmetic partition of the
sixteen (SUPER-prefixed 8, non-SUPER 8, ALT-bearing 4, …) yields 12. My draft states sixteen and
the span `:100-115`. If a frozen instrument or receipt prints "twelve", that string and the
registry disagree and the instrument's line should be named.

**F2 — S472: the empty-case span is off by one on both ends and one clause is misattributed.**
Committed cites `:40-52`; the two declarations are `:39` (`c`) and `:46` (`d`) and the last
assertion is `:51`, so the span is `:39-51`. Committed's teaches says a not-contained child
"yields `ok() == false` with a zeroed area"; the test at `:53-54` asserts the verdict alone and
never reads an area after it — the zeroing in that branch is the constructor's (S459/S466), and
attributing it to this test would credit the unit test with a fact it does not pin.

**F3 — S471: two spans close one line early.** The committed `setSetExclusiveZone :100-102`
omits the handler's `});` at `:103`; the seat brief's `set_exclusive_edge :156-168` omits the
`});` at `:169` (the committed `:156-169` is right). The refusal body is `:162-165` and reads
`INVALID_EXCLUSIVE_EDGE` on both branches (mask-out-of-range at `:157-160`, edge-not-in-anchor
at `:162-165`); my row names the second only.

**F4 — S470: the duplicate-URL note the seat asks for is absent from the committed row.** The
row repeats S457's URL byte-for-byte at a different scope, and the census confirms the live
warning (`mado W04 S470 duplicate url …/src/render/Renderer.cpp`). My draft carries the note in
the `scope` cell. Related: the committed teaches compresses the guard to "`zone + margin(edge)
> 0`"; the bytes test `exclusive + edges[i].margin > 0` on the **sum**, which is what makes
`negative-margin-skip` (zone 12, margin −12) do nothing.

**F5 — S473's version label carries two generations of the payload.** "omarchy 3.8.3" is the
content of the payload's own tracked, clean `version` file at HEAD, while that same HEAD
`8fcc9d60` is tagged **v3.8.4**. The row is not wrong, but a pin that names only "3.8.3" cannot
be re-resolved unambiguously; my anchor names the version file, the HEAD sha and the tag
together.

**F6 — S474's anchor had no line, and its fetch is an assembled excerpt.** The `is-active`
paragraph is `S474.txt:3-7` = render lines 190-193 at `MANWIDTH=80`. `S474.txt` (337 B) is the
man page's `systemd 262 (262.1-1-arch)` banner plus that paragraph — two slices, not one
contiguous render — so its sha256 pins the excerpt, not the page. The quoted text is
verbatim-present in the installed page (double spaces and the U+2010 line-break hyphen at
`:5` included), verified line for line.

**F7 — S475's wording, `used-by` and `recheck`.** (a) The committed teaches says S467's reason
"was too narrow"; it was **refuted** — the committed pin answers the very question the old
reason said it did not, so the ground is false rather than understated. My draft says "refuted
rather than incomplete". (b) `used-by = corpus/lessons/round-80.md` vs my `—`: precedent runs
both ways (S463, rejected, lists two citing entries; S467 and S045 file `—`), and the committed
value truthfully records the Gate row's home — L1 call, not a defect. (c) `recheck =
on-change` cannot fire on a URL that 404s; I file `180d` as a re-probe duty. The census confirms
`S475 duplicate url wiki.hypr.land/Configuring/Monitors` as the expected standing W04 against
S467, so the supersede link is load-bearing and present.

**F8 — precision note, not a defect.** The three S470 ranges I kept (`:2529-2586`,
`:2587-2671`, `:2673-2700`) are the declaration's and S457's. 2586 and 2671 are the blank lines
after `applyExclusive`'s and `arrangeLayerArray`'s closing braces (2585, 2670), and
`arrangeLayersForMonitor` continues past `damageMonitor` (2700) to
`invalidateMonitorGeometries` (2701) and `}` (2702). I kept them so the row, the report and the
counter cite one shape; the exact braces are recorded in the draft.

## Out of scope / not done

- Did not run either counting command (C1/C2). The seat is prose; the receipts already exist and
  I do not rerun work to decorate a report.
- Did not read `S468.bin`/`S469.bin` (round-79 fetched-but-unregistered) or re-open any held
  row: the draft cites held rows only where the entry already does.
- No judge, no commit, no publication. The six rows are prose for the L1 to append or amend.

## Artifact paths

- `.ufo/waves/round-80/w1/R80ScribeSources/sources-rows-r80.md` — six rows, six Gate quotes,
  deltas, verification, limits.
- `.ufo/waves/round-80/w1/R80ScribeSources.md` and
  `.ufo/waves/round-80/w1/R80ScribeSources/findings.md` — this report.

STATUS: ok — all six rows and six located quotes drafted and verified against the fetch bytes; F1 (the "twelve masks" count) is the one item the L1 must settle before the lesson repeats it.

# R95MExecCasesC1 — C1 frozen case set (mado round 95, wave w1)

Seat report. All runs below are DRAFT (pre-freeze QA); none is a measurement.

## Files written (owned)

- `.ufo/waves/round-95/controls/mimesniff-cases-r95.json` — frozen case set, sha256
  `930514367e686e7533d9cd479c7bc2c1b86100fe4b2862fc670eecda788c2307`.
- `.ufo/waves/round-95/controls/mimesniff-fresh-r95.py` — frozen fresh generator, sha256
  `15396113ad8f0198c56253d2f03f0e2ff05ca9fa15601ce042de8046f438b809`.
- Evidence copies (this directory): `R95MExecCasesC1-gen-cases.py` (the generator that
  produced the frozen set, run from scratch), `R95MExecCasesC1-draft-check.py`,
  `R95MExecCasesC1-draft-report.txt` (full draft disagreement list).

## What was built

- **204 cases / 360 inputs**, every one of the 20 schema classes ≥ 9 cases (min 9, max 12).
- Labels come ONLY from the compiled oracle (`mimesniff-oracle-r95.c`, sha256 verified
  `99df35f8…` before compile; glib2 2.90.1-1, shared-mime-info 2.5.1-2 confirmed via
  `pacman -Q`). 3 cases are labelled `["UNSUPPORTED", null]` (bounds far-offset fixtures
  where the oracle deterministically faults, rc=-11): `bounds-07-mime-offset-far`,
  `bounds-08-value-offset-far`, `bounds-09-mask-offset-far`. 8 cases carry
  `"expect_refusal": true` (text-mode cases in class `mode`).
- Coverage pins, among others: empty-data short-circuit; the 128-byte binary/text window
  (ctrl at 127 vs 128); the fallback ctrl set {9,10,13} vs looks_like_text {8,9,10,12,13};
  DEL 0x7f alone (text, lltext never consulted) vs with a ctrl byte (binary); VT 0x0b
  binary but FF 0x0c text; first-match-entry-in-cache-order vs priority; priorities 0, 1,
  79, 80, 100, 2^31-1, -1, -2^31 (never wins); equal/strictly-greater priorities across
  two and three caches incl. XDG_DATA_HOME precedence; range windows incl. value_length 0
  and value ending exactly at data end; masks (partial, all-zero → match-anything,
  second-byte-only); children as an ANY group (2 and 3 levels, sibling any); bounds
  (unaligned/past-EOF list pointers, ghost zero values, all-zero masks from the zero-filled
  page, empty type string from a past-EOF mimetype offset, children failing OUT_OF_BOUNDS
  before the value test, children records straddling EOF, 3 deterministic-crash cases);
  32-bit wraps of range_start+range_length (empty windows) and of i+value_length
  (wrap-06 clean / wrap-07 UB-refusal divergence); application/x-desktop with/without a
  name (security rewrite), with no-type names, prio-40 rewrite, prio-80 rewritten-outright;
  names with one type (short-circuit, data never read), none, several (weights sorted
  descending, 12-glob caps, literal-wins-outright); subclass (chains, cycles incl. the
  blocking cycle, x/* supertype, text/plain and application/octet-stream specials, inode/*
  blocked, 1200-deep chain); aliases (sniff output never unaliased, single-step unalias,
  ghost types, cross-cache alias on the sniffed side, unalias defeating/firing the
  text/plain special); trailing-slash names; text mode (bad major/minor/size/garbage
  caches, absent dirs, one-good-cache-among-bad, XDG_DATA_HOME-set hiding the HOME cache);
  `real` caches built by `update-mime-database` in scratch from packages/*.xml (nested
  magic, mask=, big16/big32/little32 word values pre-converted, offset ranges 3:10,
  aliases in parents, sub-class-of chains, prio<80 tie-breaks).
- Cache fixtures were produced by a locally written mime.cache writer (embedded in both
  the generator and the fresh generator). Validation before use: byte-identical to the
  candidate's `build_cache` on 60/60 random layouts, and round-tripped through the oracle
  against `update-mime-database`-built caches for the tree/lists layout (reverse-suffix
  trie, literal/glob lists, parents, aliases, magic entries + 32-byte matchlets).
- Determinism: regenerating the frozen set reproduces labels exactly (full oracle re-run:
  0 diffs over 204 cases). The fresh generator is byte-deterministic for a fixed seed
  (`cmp` of two seed-95 runs) and was smoke-run with seeds 95 (120 cases) and 7 (5 cases).

## DRAFT candidate-vs-oracle findings (report these; cases stay oracle-labelled)

Draft harness: 759 inputs = 204 frozen cases + 120 fresh seed-95 cases labelled by the
live oracle; candidate driven through its module API and spot-checked through the real
CLI (both paths agree). Result: **752 ok, 7 findings**.

1. **VT 0x0b — `looks_like_text` deviation (5 inputs, WRONG).** Oracle answers
   `application/octet-stream,1`; the candidate answers `text/plain,0`. The candidate's
   `looks_like_text` allows 0x0b (VT) as whitespace; the installed glib2 2.90.1-1 does not
   (`g_ascii_isspace` is table-driven and its table does not carry G_ASCII_SPACE for
   '\v', while '\f' 0x0c is fine — pinned by lltext-03). Frozen evidence:
   `lltext-02-vt-binary[0..2]`, `fallback-02-ctrl-matrix[5]`, `lltext-09-vt-past-window[1]`.
   Note: the candidate's own selftest s10 ("s10 VT passes looks_like_text") enshrines the
   wrong expectation, so its 23/23 selftest cannot catch this.
2. **wrap-07-vl-m32-at-i1-ub — over-refusal (1 input).** range_start=1, range_length=1,
   value_length=0xFFFFFFFF, value `Z`, data `AY`: installed GLib wraps i+value_length to 0
   ≤ len and memcmps with the huge count; the first byte already differs ('Z' vs 'Y'), so
   memcmp stops inside the mapping and GLib answers the fallback (`text/plain,0`). The
   candidate raises its "i + value_length passes 2^32 (memcmp past the data)" refusal
   (exit 3) where GLib answers.
3. **subclass-09-deep-chain-1200 — candidate crash (1 input).** A 1200-deep parents chain;
   the oracle resolves it (`app/d0000`, 0). The candidate's recursive `subclass` exceeds
   Python's recursion limit → RecursionError traceback, exit 1 (neither 0 nor 3).
   (Matchlet-child chains deep enough to overflow the C stack are NOT covered: a
   deterministic fixture needs a multi-megabyte cache, out of case-size budget.)

Everything else — 752/759 inputs incl. all `real`, multicache, order, prio, desktop,
name-*, slash, alias, bounds-in-page and wrap-agreement fixtures — matches the oracle
exactly. Mode-class refusals behave as specified (exit 3).

## Dead steps / deviations

- None dead. Two earlier probe mistakes of my own (an invalid probe with a relative
  XDG_DATA_DIRS, and a 39-byte mis-assumed cache) were found and corrected during the
  run; the frozen set's intent checks (`want` lists) finish at 0 mismatches.
- No tools installed or upgraded (nothing beyond the installed base was needed); pacman
  untouched. `update-mime-database` ran only inside the scratch tree.

## Checks the L1 may run

- `python3 -I .ufo/waves/round-95/controls/mimesniff-fresh-r95.py --seed N --count K --out F`
  (deterministic, unlabelled).
- Re-run the scratch generator copy and diff the JSON (byte-stable).
- The counter (R95MExecCounterC1) in draft mode over the frozen set should reproduce the
  7 findings above (its text-mode/refusal handling applies to the 8 `expect_refusal`
  cases and the 3 UNSUPPORTED cases).

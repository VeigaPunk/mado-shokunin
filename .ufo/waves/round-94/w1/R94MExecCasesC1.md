# R94MExecCasesC1 — round-94 w1 report (C1 case set + fresh generator)

Seat: R94MExecCasesC1. Wave: mado round 94, w1, base `a3de997289014e7dbf1d73ae206be1d6f8cdadd0`.
All runs below are DRAFT runs (pre-freeze); no measurement is claimed and nothing was written
under `.ufo/waves/round-94/receipts/`.

## Files written (all under /home/vgpnk/Projects/shokunin/mado-shokunin)

| file | sha256 |
|---|---|
| `.ufo/waves/round-94/controls/mimeglob-cases-r94.json` (frozen C1 case set) | `2df52ec27efd9f654176d3b9eca7d700edc14afc305a854587ddea55d5593e92` |
| `.ufo/waves/round-94/controls/mimeglob-fresh-r94.py` (fresh generator) | `ab76b97e0c37d92ddb0b03a733745b1089be2a083379d9cabee050689ed57e2c` |
| `.ufo/waves/round-94/w1/R94MExecCasesC1.md` (this report) | — |

Scratch builder (not a deliverable): `$HYAKU_SCRATCH/mado-r94/R94MExecCasesC1/build_cases.py`
(fixture materialiser + oracle labeller + DRAFT agreement runner); scratch deleted at end of seat.

## Oracle

Compiled in scratch with:
`gcc -O1 -o "$S/oracle/oracle" .ufo/waves/round-94/controls/mimeglob-oracle-r94.c $(pkg-config --cflags --libs gio-2.0)`
binary sha256 `38cea1b00dd65bb2531921aeaf7f586f3524a62fa6823b4f2c49c910724239e2`,
against host glib2 2.90.1-1 / shared-mime-info 2.5.1-2 (`pacman -Q`, read-only).
Every case was labelled by TWO oracle runs per case (byte-identical output required, else the
case is dropped); zero nondeterminism observed across all 235 cases.

## Case set (frozen)

- 235 cases, 317 names. Every oracle invocation `env -i LC_ALL=C HOME=<h> [XDG_DATA_HOME=…] [XDG_DATA_DIRS=…]`.
- Modes: text 129 (≥80 ok), cache 83 (≥80 ok), mixed 23 (≥10 ok).
- Classes (all ≥6): dirs 13, mode 12, literal 12, simple 12, full 19, fold 11, cs 10, deep 11,
  weight 14, dupe 13, order 11, multi 9, nomatch 9, slash 11, bytes 11, fgets 10, v1 10,
  noglobs 8, cachefmt 13, mixed 16. Header: `version 1`, `oracle_src_sha256 9c43…bfa6b11`, `glib2 2.90.1-1`.
- Cache fixtures: `mime.cache` bytes produced by `update-mime-database` run ONLY on scratch
  dirs (`TMPDIR=$S`), from generated `packages/*.xml`; 33 cases use spec-exact hand-crafted
  caches (a Python struct writer, validated by the oracle), used for weights >255/256/300,
  cs-bit weights, duplicate/unsorted literal entries, >10 fnmatch entries, minimal v1.1/v1.2
  caches. Malformed caches: 10-byte and 39-byte truncations, versions 1.0/1.3/2.0, empty file,
  a directory named `mime.cache`, one 200-byte truncation of a real cache (verified non-looping).
- Coverage highlights (all labelled by the oracle, several pin GLib-behaviour the spec does not):
  - `weight-01` weight-0 single match → **certain** (glib's plural API never maps weight<80 to
    the uncertain flag; uncertain only from trailing `/`, no-match, or >1 distinct type).
  - `weight-02` vs `weight-08`: text keeps weight 300 (wins), cache keeps low 8 bits (44, plus
    the 0x100 bit → cs) so the 50-weight type wins — the divergence pair.
  - `weight-09` (256 → weight 0 + cs), `weight-10` (255), `weight-11`/`weight-14` (full-glob cs weights).
  - `full-12`/`full-13`: >10 matches → the fixed `MimeWeight mimes[10]` cap drops the heaviest
    entries (answer `app/x-fm9`/`app/x-tfm9`, not the weight-21 types).
  - `cs-08`: cache literal binary search lands mid-list on a cs entry → folded pass returns 0
    (early stop), raw pass answers the cs literal's type. `cs-09`/`cs-10`: cs suffix entries are
    skipped on the folded pass and answered by the raw pass / the non-cs zero-sibling.
  - `full-18` vs `full-19`: a `:` inside `[[:digit:]]` is parsed as the flags delimiter in globs2
    lines, truncating the text-mode pattern (no match), while the cache stores the whole pattern
    (match). Same fnmatch(3), opposite answers.
  - `fold-03`: non-cs `*.C` still routes `a.C` to the `*.c` type via the folded suffix pass
    (S517 divergence pair with `fold-05`/`fold-06` cs variants).
  - `bytes-04`: invalid-UTF-8 pattern byte 0xFF still matches name byte 0xFF (C decodes the
    pattern byte to the same widened value); `bytes-06`/`literal-11`: UTF-8 suffix globs never
    match (trie widens signed bytes), UTF-8 literals match only byte-exact (ASCII-only fold).
  - `fgets-01`: a >254-byte globs2 line is cut at the fgets boundary — the 238-char truncated
    suffix matches, the 239-char name misses. `fgets-03`: chunk 2 of a 281-byte `#comment` line
    is parsed as data — it injects a weight-0 literal (`inj-lit` → type `50`, certain).
  - `noglobs-01..03`: `__NOGLOBS__` is a normal literal for GLib (name matches; sibling globs
    are NOT deleted), in text and, via glob-deleteall, inside update-generated caches.
  - `deep-06`/`deep-07`: cross-cache suffix hits accumulate per cache (conflict → dir order
    decides); within one cache the deepest suffix wins regardless of weight (`deep-11`).
  - `dirs-12`: `XDG_DATA_HOME`/`XDG_DATA_DIRS` unset → host `/usr/share/mime` cache consulted
    (`x.png` → `image/png` uncertain=1 on this host db) — allowed host read.
- Schema notes for the materialiser: a `files` key ending in `/` with empty b64 value is a
  DIRECTORY (used once: `cachefmt-07` `s1/mime/mime.cache/`); everything else is a file.

## Fresh generator

`mimeglob-fresh-r94.py --seed S --n N --out FILE --scratch-root DIR`: unlabelled case file
(same envelope; cases carry `"class":"fresh"`, no `labels`), half text / half cache layouts,
names drawn to hit and miss the generated globs; `update-mime-database` runs under
`--scratch-root` with `TMPDIR` pinned to it. Verified: seed 20261107 twice → byte-identical
output (cache bytes included); seed 99 → different; scratch left with 0 leftovers; smoke test
(6 layouts, live oracle) → 10/31 names hit globs, i.e. real hit+miss mix.

## DRAFT agreement of the candidate (`.ufo/waves/round-94/build/mado-mimeglob.c1.py`, sha256
`0700915a260627cd521ea14b61dbb15aa7c3b067c0d287f04c07b39dfa72d63e`)

Per case: `python3 -I <candidate> --json --home <root>/h [--data-home D|--data-home-unset]
[--data-dirs L|--data-dirs-unset] <names…>`, compared against the oracle labels.

- 315 of 317 names: (type, uncertain) equal to the oracle. 0 wrong answers.
- 2 refusals (exit 3, UNSUPPORTED), both on the same class of input:
  - `bytes-04-invalid-utf8-in-pattern` — globs2 line `50:app/x-hi:*.hi\xff`, name `f.hi\xff`;
    oracle: `app/x-hi`, uncertain 0. Candidate prints
    `MADO_MIMEGLOB: UNSUPPORTED …/s1/mime//globs2` (refuses non-UTF-8 glob lines by design).
  - `bytes-05-invalid-utf8-literal` — globs2 line `50:app/x-nm:\xff\xfe`, name `\xff\xfe`;
    oracle: `app/x-nm`, uncertain 0. Same refusal.
  - Consequence for PRED-C1-r94-v1(i): as written, "tool equals oracle on every frozen case"
    fails on these two cases while the refusal stands. The L1 can either widen the candidate to
    answer non-UTF-8 lines the way the C parse does (byte-value codepoints, strcmp literals) or
    move these two cases to an explicit refusal allowance; the labels are frozen either way.
- No other disagreement in any class, including all equal-weight tie cases (glibc qsort tie
  order), cross-cache conflicts, the >10 cap, cs literal early-stop, and the 40-byte-boundary
  cache validation.

## Dead steps / defects encountered (resolved)

- First builder run: oracle hung >60 s on a case built by my first cache writer (dangling
  suffix-tree `child_offset` triggers the `continue`-loop at xdgmimecache.c:424 in the C code).
  Fixed by rewriting the writer with self-consistent offsets; a per-case 10 s oracle timeout now
  marks such a case POISON and drops it (0 poisoned in the final set). Truncated-cache coverage
  was reduced to bounds-safe truncations (≤200 bytes of the real cache; the loop hazard at
  larger truncations is real and worth a candidate refusal test later — noted, not frozen).
- `update-mime-database` rejects XML weights >100 ("Bad weight"), so generated weight coverage
  stops at 100; weights 200–300 come from crafted caches and text globs2 only.
- No tool installs were needed (host gcc/pkg-config/update-mime-database/python3 only); pacman
  untouched (guard respected).

## Verification commands exercised (all exit 0 unless noted)

`gcc -O1 …` (oracle), `update-mime-database <scratch>/…` (scratch-only), builder
`python3 build_cases.py` (3× final), schema validator (0 errors, 235 cases, min class 8),
`cmp` frozen vs draft (identical), generator determinism `cmp` (identical / different-seed),
candidate DRAFT run per case (235 invocations, 233 rc 0, 2 rc 3). Scratch directory
`/fast/scratch/hyaku/mado-r94/R94MExecCasesC1` deleted after this report.

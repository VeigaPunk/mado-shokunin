# R96MExecCasesC1 — the C1 TEXT magic case set, probe and fresh generator

Seat: cases + probe + fresh gen for round 96 C1 (`tools/mado-mimetext.py`, text MIME
database). All three deliverables landed in `.ufo/waves/round-96/controls/`; every label
in the frozen file was produced by the compiled round-95 oracle (Shared contract 3),
never by a lane tool or by my own reasoning.

## Deliverables and pins

| file | sha256 | content |
|---|---|---|
| `controls/magictext-cases-r96.json` | `42ce9fc68458955e9e93c405cdbeb59f649b36d94e100240894d660391d1bed6` | frozen case file, v2 envelope, 265 cases / 404 inputs |
| `controls/magictext-probe-r96.py` | `545e1ed13cd1036223583156b107a84800a393a6260573e2372838bd1aefa0f7` | materialize/label/`--check` probe (labels come only from the oracle) |
| `controls/magictext-fresh-r96.py` | `32d38edfb2cff57de3d89297ffaf1bd781d730b7be502fbfa62efa38de0815da` | seeded fresh generator, `--seed N --out FILE [--oracle BIN] [--scratch DIR]` |

Oracle: round 95's `mimesniff-oracle-r95.c`, sha `99df35f8…d124a`, compiled in my
scratch with `cc -O0 … $(pkg-config --cflags --libs gio-2.0)`; host
`glib2 2.90.1-1`, `shared-mime-info 2.5.1-2` (pacman -Q). Tooling installs: **none**
(cc/pkg-config/python3 host tools only; no pacman/uv/npm touched).

Fetch-byte note: `.ufo/waves/round-96/fetch/` was empty when I read it; the round-95
fetch copies of `xdgmimemagic.c` / `xdgmime.c` carry exactly the digests the round-96
receipt pins (`fcb1eafe…`, `afb1c1c1…`), so I read those as the opened bytes.

## Census (frozen file)

header=17 sect=20 value=20 mask=16 word=19 range=16 indent=17 order=16 drop=17
multi=16 glob=16 alias=14 fallback=14 zerosize=14 mode=17 desktop=16 —
265 cases (>= 260), min per class 14 (>= 8), 1..5 inputs per case (within 1..12),
404 inputs total. Every case id is `<class>-NN-<slug>` and the slug names the one model
rule it exercises. Envelope `db_mode:"text"` (the surface); none-mode cases hold no
`mime/*` at all; every case holding `mime/*` files also holds a `mime/magic` (an inert
12-byte header-only magic was inserted where the rule only needed globs/aliases —
labels verified unchanged by the relabel), so there is no "text case without magic".

Refusal cases (the only `["UNSUPPORTED",null]` labels; ids carry
`declared-refusal-cache-valid`; the probe derives refusal from **loadability**, never
file presence): mode-04 (d1, 1048 B, version `00010002`), mode-05 (dh, 1048 B,
`00010002`), mode-07 (dh, 40 B, `00010001`, synthetic header-only cache that loads and
answers nothing), mode-12 (d2, 1048 B, `00010002`), mode-14 (d1, 1048 B, `00010002`).
The 1048-byte blob is the valid v1.2 cache reused from round 95's frozen case file
(sha `1ca2cd267e162925b8b4d9984497a53e9addc7ce86bfdfb9d419bf34802b5518`).
`mode-06-junk-cache-is-not-a-cache` is an oracle-labelled TEXT case
(`[["app/x-md6",0],["app/x-md6g",0]]`) — the discriminator against treating any
`mime.cache` as cache mode.

## Verification exercised

- Frozen file: `magictext-probe-r96.py --check` re-materializes all 265 case roots,
  re-runs the oracle per case and compares every label — **ok, 265/265** (5 refusals
  skipped as sentinels, 0 oracle failures, rc 0). File is pure ASCII (0 non-ASCII
  bytes of 146542).
- Fresh generator: seed 961107 → 40 cases / 292 inputs; seed 7 → 40/315; seed 5
  (no `--oracle`: compiles the pinned source itself) → 40/332. All runs: 1..12 inputs
  per case, 0 dropped cases, ≥ 120 inputs. Determinism: two runs at seed 961107 are
  byte-identical (`cmp` ok); seed 42 differs. `--check` of a fresh output against a
  fresh oracle re-run: ok 40/40, refused=0 (no cache fixtures by design).
- Probe refusal rule mirrors `xdgmimecache.c _xdg_mime_cache_new_from_file` /
  `tools/mado-mimeglob.py load_cache`: len >= 40 AND BE u16 at offset 0 == (major 1,
  minor 1|2).

## Dropped cases

None. No oracle run exited non-zero, timed out (> 10 s) or printed a malformed/short
output across all labeling runs.

## Measured facts the wave should keep (all oracle-proven, case ids in brackets)

- Aliases: text-mode **data** answers are the raw magic type, never canonicalized
  `[alias-01, alias-11]`; the `alias canonical` format is proven by the **subclass
  tie-break**, which resolves name types through unalias `[alias-02, alias-03,
  alias-07, alias-14, glob-03's negative control]`.
- Word sizes {0,1,2,4} are accepted; `~0` passes the modulus check untouched and
  behaves as 1 `[word-05-word0-odd-length-matches, word-07, word-16]`; `~3`/`~8` and
  odd lengths under `~2`/`~4` drop the whole section `[word-03/05/06/13/14]`; LE swap
  at parse proven in both directions `[word-01, word-10, word-04, word-08, word-11]`.
- No priority gate in text mode: `[0:…]` matches `[sect-01, order-06]` and loses only
  to higher priority `[order-05]`; INT_MAX priorities parse and win `[sect-02,
  order-11]`; 30-digit overflow drops the section `[sect-03]`.
- `__NOMAGIC__` is a literal 10-byte value: data starting with it at offset 0 matches
  `[value-13]` — the spec's delete-all marker is inert in GLib 2.90.1.
- Empty type `[0:]` answers the empty string, certain `[sect-09]`.
- Zero-length value (and value+mask) hold at i=0 for any data `[value-08, mask-12]`.
- EOF mid-line keeps the section's EARLIER matchlets (insertion on EOF-with-mime_type)
  `[drop-03/04/11]`; with no earlier matchlet the section is inert `[drop-17]`; a bad
  matchlet line drops the whole section including earlier matchlets `[drop-01]`; a bad
  line after a completed section kills only the section being parsed `[drop-05, drop-12]`.
- A matchlet line before the first section errors AND its skip-to-newline eats the
  following section's first matchlet line `[sect-12]`.
- The data path passes the full buffer (no max_extent truncation observable):
  offset-100/150/200 matchlets match `[multi-04, multi-08, multi-16, value-15]`.
- `looks_like_text` measured: `\f` (0x0c) flips a binary fallback answer to
  text/plain but `\v` (0x0b) does NOT `[fallback-14]`; `\b` flips `[fallback-06]`;
  `\x7f` never leaves text/plain `[fallback-08]`.
- Text-mode literal globs do NOT case-fold in the name step: "makefile" does not match
  a `Makefile` literal `[glob-06]`, while folded suffix matching works `[glob-13]`.
  This is in tension with round 94's text-model docstring ("case-folded literals that
  are not cs") — flagging for the scribe; the oracle label is ground truth either way.
- Unloadable cache files fall back to text mode in GLib `[mode-06]`; only a loadable
  cache makes the db cache mode, and then ONLY caches answer `[mode-04/05/07/12/14,
  measured manually: dh cache 1.2 + d1 magic → the magic's type is NOT returned]`.

## Rework history (before the freeze)

First labeled draft had 7 mislabelled-by-construction fixtures: child-offset filler
arithmetic (`??` placeholders), raw bad-lines after `=` that the parser read as giant
BE value-lengths (drop-06/15 redesigned with proper 2-byte length prefixes), two mask
inputs whose low-nibble semantics I had backwards, one case whose second input still
matched. All fixed and re-labelled before freezing; the L1's F9 edge list (zero-length
value, EOF-mid-line, `+0`, bytes after `]`, `~0` odd, `~2` both directions, indent
0→2 vs 0→1 byte-identical pair, empty section) is fully covered. ReviewC1's fresh-leg
findings (ZeroDivisionError at word 0, >12 inputs, zero-input cases) are fixed:
`word > 1` guard, `inputs[:12]`, guaranteed non-empty inputs; probe `refused` no
longer counts an empty input list as a refusal.

## Risks / notes for the L1

- The frozen file renumbers NN per class on regeneration; the current ids are
  sequential within each class and unique overall.
- mode-10 (subclasses-only) and mode-11 (icons-only) carry the inserted inert magic,
  so they no longer isolate "text file without globs/magic makes mode text" — the
  contract's text-case rule forced this; the surviving discriminator is the tool's
  DIRS line, not the label.
- `sect-09` label is the empty string type (`["",0]`) — oracle truth; counter-side
  type validators should not assume a non-empty type.
- Counter/Tool seats were notified of the loadability-based refusal rule and the
  inert-magic pass (mode-06 discrimination, 5 declared refusals).

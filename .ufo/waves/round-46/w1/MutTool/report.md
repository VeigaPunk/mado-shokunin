# MutTool-4 — mutation testing of the C1 reference (round 46 w1)

Target: `.ufo/waves/round-46/l1-draft/mado-devices.py` (sha256 `b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b`, matches the counter's frozen MODEL_SHA256). Question attacked: do the frozen artifacts (selftest + 90 fixtures) pin the reference's semantics, or do mutants survive them?

## Method

- Detector: in-process replay through the reference's own code — `selftest()` (48 checks) plus all 90 frozen fixtures from `quality/counters/c1-r46-fixtures.json` (sha256 `027ed50877b345e34b27e38b4a865be4b23f94c0cc0067ac42265ca1778e3fc1`, verified), each replayed through `run()` (a superset of `report()`: it also exercises arg/file/stdin handling, so the usage/unreadable/too_large/bad_json fixtures are covered), with `{A}`–`{D}` placeholders substituted by the counter's `names(46)` and `@BIG`/`@BIGDUMP` markers expanded exactly as `c1-r46-devices.py:run_fixture` does. No processes, no sockets, no sandbox: the reference reads files/stdin only.
- Baseline (run before and after all mutants): pristine passes selftest 48/48 and 90/90 fixtures (`evidence/receipt.txt`).
- 104 mutants, one minimal source edit each: constants (12), operator/comparison swaps, branch deletions/inversions, off-by-one slices in comment/bracket/continuation parsing, argument parsing, I/O paths, format strings, verdict/rc mapping. Full table: `evidence/index.json`; per-mutant verdicts: `evidence/results.json`; raw run: `evidence/receipt.txt`.
- A mutant is killed when selftest fails, any fixture output/rc differs, or the replay raises. Survivors were then probed with hand-built killing inputs (demonstrated in the receipt, pristine vs mutant side by side).

## Result: 104 mutants → 93 killed, 11 survived, 0 generation errors

Killed mutants were caught by 34 distinct fixture labels plus 12 selftest-only kills (notably the bad_json battery and the type-validation cases). The fixture set is strong: every verdict/rc branch (OK/DIFFER/NO_KEYBOARDS/STALE_BLOCK/NOT_COMPARED × rc 0/1/2/3/4/5), the float32 rounding at 2 decimals (`mouse-float32` kills the f32→f64 mutant), overflow/denormal stof handling, `[[EMPTY]]`, `##` escapes, continuations with pre-backslash spaces, CRLF, `\v\f` trimming, multi-file ordering, tablet `belongsTo` matching, and the 1 MiB too_large boundary are all pinned.

## Survivors — 9 genuine (unpinned semantics), each with a demonstrated killing fixture

Expected output in each case is the pristine line below; the mutant diverges. All are expressible in the current fixture schema except B36 (schema gap, see meta-findings).

1. **B10 — `is_num` drops `math.isfinite`** (`report`, mouse verdict). A reported `scrollFactor` of ±inf/NaN (JSON `Infinity`/`NaN`) prints `reported=inf`/`reported=nan` instead of `reported=?`. Verdict stays DIFFER, so only the full line catches it. Kill: dump `{"mice":[{"name":"m","scrollFactor":Infinity}],"keyboards":[]}` — pristine `reported=? verdict=DIFFER`, mutant `reported=inf verdict=DIFFER`. (NaN variant also demonstrated.)
2. **B36 — config decode `errors="replace"` → `"ignore"`** (`run`). A config file containing an invalid UTF-8 byte: pristine expects `layout="br\ufffdx"`, mutant expects `layout="brx"` (demonstrated with config bytes `input:kb_layout = br\xffx\n`, keyboard reporting `br\ufffdx`: pristine AGREE-expected vs mutant DIFFER-expected). **Not expressible in the current fixture schema** — see meta-finding 1.
3. **C02 — comment-pair lookahead `pos < len(line)-1` → `pos < len(line)`** (`cut_comment`). A config line ending in `#` (e.g. `input:kb_layout = br #`) makes the mutant raise IndexError; pristine returns `layout="br"` OK rc0 (demonstrated).
4. **J05 — continuation loop `while` → `if`** (`join_continuations`). Chains of 2+ backslash lines: `input:kb_layout = br,\<NL>\<NL>us` → pristine `layout="br,us"` OK rc0, mutant `layout="us"` NOT_COMPARED rc5 with `unsupported=1` (demonstrated). Fixtures only cover single continuations (`continuation`, `continuation-spaces`, `continuation-last-line`).
5. **K09 — `SPECIAL_RE` loses `re.I`** (`read_float`). Uppercase `NaN`/`INF`/`0X` in `scroll_factor`: pristine NOT_COMPARED rc5 (`unsupported=1`), mutant treats it as unset → OK rc0 (demonstrated with `device[m]:scroll_factor = NaN`). FACTORS in the counter and fixtures are lowercase-only.
6. **K13 — `FLT_MIN = 2.0**-126` → `2.0**-125`** (`read_float`). A decimal in (2⁻¹²⁶, 2⁻¹²⁵), e.g. `scroll_factor = 2e-38`: pristine ok → `scroll_factor=0.00` DIFFER rc1; mutant unsupported → NOT_COMPARED rc5 (demonstrated). No fixture sits in that binade.
7. **P15 — bracket scan `find`/`rfind` swapped** (`parse_config`). A key with two bracket groups, e.g. `device[a][b]:kb_layout = fr`: pristine cuts bracket name `a][b` → block `a][b` NO_SUCH_DEVICE, STALE_BLOCK rc4; mutant leaves the key uncut → field `][b]:kb_layout` ignored → OK rc0 (demonstrated). No fixture has two bracket groups (the two "multi-bracket" fixture hits are just `[[EMPTY]]` markers).
8. **P24 — rename resets `cur` to `None` instead of `False`** (`parse_config`, rename branch). `device { name = a / name = k / name = b / kb_layout = de }`: pristine counts 3 unsupported, one block `a`; mutant selects device `b` after the rename → blocks=2 stale=2 unsupported=1 (demonstrated; same rc 5, full-text compare catches it). The selftest's rename case passes the mutant because the selftest checks the summary line only via `endswith("verdict=…")` — see meta-finding 2.
9. **R05 — denormal compare `< FLT_MIN` → `== FLT_MIN`** (`read_float`). `scroll_factor = 1.1754943508222875e-38` (exactly 2⁻¹²⁶): pristine ok → `scroll_factor=0.00` DIFFER rc1; mutant unsupported → NOT_COMPARED rc5 (demonstrated). The boundary value itself is in no fixture.

## Survivors — 2 equivalent (no coverage gap)

- **P16 — bracket sanity `lb < rb` → `lb <= rb`**: `lb == rb` would require `key[lb]` to be both `[` and `]`; impossible, so the mutant is equivalent by construction. Demonstrated identical on `device[]:kb_layout = de` (both STALE_BLOCK with empty-name block — pristine already cuts `[]` because 6 < 7).
- **B38 — `read_stdin` loop bound `<=` → `<`**: the post-loop `if len(data) > MAX_BYTES` check pins too_large regardless; demonstrated identical on a 1048577-byte stdin payload (both `SETUP too_large`). The loop bound is redundant defense — a simplification candidate, not a gap. (It is distinguishable only by a pipe short-read landing exactly at MAX_BYTES, which no fixture can force deterministically.)

## Meta-findings

1. **B36 is unpinned by the entire counter, not just the fixtures.** `c1-r46-devices.py:run_fixture` writes every config with `open(cp, "w", encoding="utf-8")`, and `gen_case`-driven runs do the same, so invalid-UTF-8 config bytes are inexpressible in both the frozen fixtures and the 150 generated cases; the selftest has no config-decode case either. The docstring's "decoded as UTF-8 with errors replaced" for *configs* is therefore pinned only by prose (the *dump* side is pinned by the `setup-bad-utf8` fixture). A raw-config-bytes fixture kind (e.g. a `@RAW:<hex>` marker like the existing `@BIG`/`@BIGDUMP`) would close it.
2. **Selftest checks the summary line only via `lines[-1].endswith("verdict=" + want_v)`**, so counter deltas (`unsupported=N`, `stale=N`, `agree=N`) escape it — the P24 class survives selftest and is caught only by full-text fixture comparison. A one-line selftest tightening (compare the whole summary line) would close that class.
3. **The counter's clause f (150 generated cases) is a differential oracle against the pinned reference itself** (`model_out`), so in a real counter run it would mechanically kill all 9 genuine survivors — but it cannot pin a semantic the reference gets wrong; fixtures+selftest are the independent pin, and these 9 are exactly where that independent pin is missing. B36 escapes even clause f.
4. Fixture-shape gaps behind the survivors, for the L1's fixture author: no chained continuations, no trailing-`#` line, no uppercase inf/nan/0x, no value in (2⁻¹²⁶, 2⁻¹²⁵) nor exactly 2⁻¹²⁶, no two-bracket-group key, no rename-followed-by-name block, no non-finite reported scrollFactor.

## Relation to SentTool-3's F1/F2

SentTool's clause-r findings concern the counter's bwrap sandbox (fakebin PATH, absolute-path exec, AF_UNIX reachability). This seat's detector is in-process (no exec, no sockets), so mutant verdicts are unaffected; F1/F2 carry to any v2 counter and should be routed via the L1 as SentTool says.

## Restoration evidence

- Reference sha256 before the run, after the run, and in the final receipt: `b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b` — unchanged; the lane file was never written (mutants lived only in scratch).
- Fixtures sha256 unchanged: `027ed50877b345e34b27e38b4a865be4b23f94c0cc0067ac42265ca1778e3fc1`.
- Pristine baseline re-verified green after all mutants (receipt head and tail).
- All work dirs were under `/fast/scratch/hyaku/mado-r46/MutTool/` (<2 GB; receipts copied to `evidence/` first); scratch deleted after the run. No tool installs were needed (python3 only).

Report: .ufo/waves/round-46/w1/MutTool.md

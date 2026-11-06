# R89MExecFuzz — differential test of the C1 candidate's matcher against the C oracle

Seat: R89MExecFuzz (leaf executor, round 89 wave `w1`, hyaku run 15, attempt 1). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`, base revision `af998dcc41d48618ffe7afe0efc9354755a9244e` (master).
Scratch `/fast/scratch/hyaku/mado-r89/R89MExecFuzz` (deleted on exit, see §9).

**These are DRAFT checks, not measurements.** They run on draft bytes (`build/mado-mako.c1.py`, not yet
`tools/mado-mako.py`). No receipt was written under `receipts/`; no counter was invoked; no scoring verdict is
claimed. What is claimed is narrow: the candidate's `posix_ere_compile`/`posix_ere_search`/`posix_ere_free` bridge
returns the same `{match, nomatch, invalid}` verdict as the independent C oracle on 3 × 3200 generated pairs and on
one supplementary seed, under three `LC_ALL` values.

## 1. What was run (every command, with exit code)

`S=/fast/scratch/hyaku/mado-r89/R89MExecFuzz`; `C=…/.ufo/waves/round-89/build/mado-mako.c1.py`;
`O=…/.ufo/waves/round-89/controls/posix-ere-oracle.c`; `D=…/.ufo/waves/round-89/w1/R89MExecFuzz-driver.py`.

| # | command | exit |
|---|---|---|
| 1 | `cc -O0 -o "$S/ore" "$O"` | 0 |
| 2 | `env LC_ALL=C python3 -B "$D" --oracle "$S/ore" --candidate "$C" --pairs 3200 --seed 89151006 --label C --out "$S/final-C.json"` | 0 |
| 3 | same with `LC_ALL=C.UTF-8`, label `C.UTF-8`, out `final-C.UTF-8.json` | 0 |
| 4 | same with `LC_ALL=en_US.UTF-8`, label `en_US.UTF-8`, out `final-en_US.UTF-8.json` | 0 |
| 5 | same with `LC_ALL=C.UTF-8 --seed 89151007`, out `final-seed2.json` (supplementary) | 0 |
| 6 | control harness self-check, BRE mutant (`REG_EXTENDED = 0` in a scratch copy) | 1 (expected: divergences found) |
| 7 | control harness self-check, always-match mutant (`posix_ere_search` → `True` in a scratch copy) | 1 (expected) |
| 8 | control harness self-check, python-`re` stub module in scratch | 1 (expected) |
| 9 | oracle locale probe: `LC_ALL∈{C,C.UTF-8,en_US.UTF-8} "$S/ore" '^.$' 'é'` and `'^..$' 'é'` | 0 |
| 10 | candidate locale probe in a fresh process under `LC_ALL=en_US.UTF-8` (`^.$`, `^..$`, `[[:alpha:]]+`, `é\|a`) | 0 |
| 11 | byte-pin check `sha256sum "$D" "$C" "$S/ore" "$O"` | 0 |
| 12 | absence check `ls -d build/__pycache__ w1/__pycache__` | 2 (`No such file or directory` — the point) |

Byte pins for the exact bytes exercised:

```
2720922b1b9206549bf20248a20c5b70d7dc445ab2d1815112a2cb524fce229e  build/mado-mako.c1.py            (candidate, unchanged)
16899f2269785424bc3a68a6f91404a9b57e09aae4a9dade542184db941f200e  w1/R89MExecFuzz-driver.py        (driver, final bytes)
4227019226073c975ae466b5753c938dcd3fdd9bd5701fd049297438460f8ce8  controls/posix-ere-oracle.c
d3388757d3e17bc7b0f2efae3e4fab1e2fa9958562ffcb93d9593b1678b35654  $S/ore                           (cc 16.2.1, -O0)
```

Dead step, disclosed: the first draft of the driver had a stray `try:` and syntax-failed for all three runs
(`SyntaxError: expected 'except' or 'finally' block`, line 152). It was fixed; **every run reported below used the
final driver bytes `16899f22…f200e`**, and runs 2–4 plus the supplementary run 5 were repeated after the fix.

The oracle was **not** modified. It calls no `setlocale` (grep of the source: only the comment on line 4 mentions it),
so a C program starts and stays in the C locale regardless of `LC_ALL`. The candidate was imported with importlib from
its path and its sha256 was identical before and after (`2720922b…`), i.e. no write-back.

## 2. Pair generator

- Seed `89151006`, 3200 pairs (requirement ≥ 3000); 3038 distinct `(pattern, text)` pairs; 1703 distinct patterns,
  1977 distinct texts. Pair-list sha256 (JSON, UTF-8, `separators=(",",":")`):
  `0fb8ab8ea7ec23bb819d042cf90bd09ab62cc61c6967218a81051c0c866ef42a`.
- Pattern vocabulary: the seat's alphabet `a b é . * + ? | ( ) [ ] ^ $ { } \ - :`, the classes
  `[[:alpha:]]` `[[:digit:]]` `[[:space:]]`, and 39 templates that use only that vocabulary (anchors, alternation, bracket expressions, escapes: `^(a|b)*$`, `[^ab]*`, `a\*b`, `[]a]`, `a**b`,
  `a{`, …). 740/3200 patterns contain a POSIX class, 1537 contain a quantifier char, 921 contain an anchor,
  183 are the empty pattern.
- Texts: `a b é`, the space and the digits, length 0–8, plus 12 fixed strings (empty, `éé`, `0123456789`, …);
  703 texts contain `é`; 345 are empty.
- Oracle distribution over the 3200 pairs: **invalid 1060 (33.1 %), match 914 (28.6 %), nomatch 1226 (38.3 %)** —
  all three verdicts are exercised.
- The driver compares exact verdicts, not just "valid": `invalid` = `regcomp` refused; `match`/`nomatch` =
  `regexec(..., 0, NULL, 0) == 0` or not. The oracle receives pattern and text as explicit UTF-8 byte argv, so no
  locale-dependent re-encoding sits between the two sides; the candidate encodes with explicit UTF-8 too.
- The candidate's flags were read from the candidate and grounded in the host header: `REG_EXTENDED = 1`,
  `REG_NOSUB = 8` (`/usr/include/regex.h:310,323`) — the same flags the oracle program uses.

## 3. Results — three required runs plus one supplementary

| run | `LC_ALL` | pairs | oracle invalid/match/nomatch | candidate disagreements | python `re` disagreements | exit |
|---|---|---|---|---|---|---|
| 1 | `C` | 3200 | 1060 / 914 / 1226 | **0** | 404 (12.6 %) | 0 |
| 2 | `C.UTF-8` | 3200 | 1060 / 914 / 1226 | **0** | 404 (12.6 %) | 0 |
| 3 | `en_US.UTF-8` | 3200 | 1060 / 914 / 1226 | **0** | 404 (12.6 %) | 0 |
| 4 (supp.) | `C.UTF-8`, seed `89151007` | 3200 | 1117 / 870 / 1213 | **0** | 449 (14.0 %) | 0 |

The three required runs produced **byte-identical result payloads** apart from the `label`/`environment` fields
(verified by comparing `seed, pairs, oracle_counts, candidate_*, python_re_*`): the pair list is seed-deterministic,
the oracle's verdicts are locale-invariant, and the candidate's verdicts are locale-invariant under all three
environments. Totals: 12 800 candidate-oracle comparisons (9600 required + 3200 supplementary), **zero disagreements**.

Acceptance per the seat item — "three runs with counts; zero or listed disagreements": **met with zero.**

## 4. First 10 python-`re` disagreements (motivation figure; identical in runs 1–3)

`python_re` = `re.compile(pattern).search(text)`; compile failure is reported as `invalid` with the exception text.
404/3200 pairs disagree (12.6 %); 1054/3200 additionally fail Python compilation outright. Duplicate pairs (rows 2 and
10) are independent random draws, not a driver bug.

| # | pattern | text | oracle | python `re` | python `re` error |
|---|---|---|---|---|---|
| 1 | `[[:digit:]]}é\|[[:digit:]]` | ` 2 ` | match | nomatch | — |
| 2 | `a{` | `73` | invalid (ERE interval prefix) | nomatch | — |
| 3 | `[[:space:]]:b[[:digit:]]{` | `2` | invalid | nomatch | — |
| 4 | `[[:digit:]]{-` | `é 7773` | invalid | nomatch | — |
| 5 | `)b[[:alpha:]]` | `63` | nomatch | invalid | `PatternError: unbalanced parenthesis at position 0` |
| 6 | `é)` | `a` | nomatch | invalid | `PatternError: unbalanced parenthesis at position 1` |
| 7 | `)$\|` | `49` | match | invalid | `PatternError: unbalanced parenthesis at position 0` |
| 8 | `[[:alpha:]]*[[:space:]]*$` | `a` | match | nomatch | — |
| 9 | `}[[:digit:]]?)é^` | `1300650é` | nomatch | invalid | `PatternError: unbalanced parenthesis at position 13` |
| 10 | `a{` | `73` | invalid | nomatch | — |

These are exactly the constructs where Python `re` is not POSIX ERE: `{` outside a valid interval (POSIX ERE rejects,
`re` treats it literally), `)`/`]` placement, and POSIX bracket-class expressions (`[[:alpha:]]` is a nested set in
`re`). They motivate the libc path; they are not evidence against the candidate.

## 5. Findings

**No candidate/oracle disagreement exists on any of the 12 800 comparisons**, so there is no minimal reproducing
pair to list. The minimiser is implemented (`minimise()` in the driver) and was exercised by the harness self-checks
(§6), where it reduced, e.g., the BRE mutant to `pattern="|"`, `text=""` (oracle `match`, mutant `nomatch`) and the
python-`re` stub to `pattern="[[:]"`, `text=""` (oracle `invalid`, python `nomatch`).

What the zero establishes, and what it does not:

- Establishes: the candidate's bridge (ctypes prototypes, 256-byte `regex_t` buffer, `REG_EXTENDED|REG_NOSUB`,
  UTF-8 encoding, `None` on `regcomp` failure, `regexec` non-zero ⇒ no match) is observationally identical to
  mako's own `regcomp`/`regexec` call shape across 3038 distinct pairs per seed, including the invalid branch
  (1060/3200) and multi-byte texts (703 pairs), in three locales.
- Establishes: locale independence — the candidate forces `LC_ALL=C` in `_libc()` (candidate lines 123-124), and the
  `en_US.UTF-8`/`C.UTF-8` runs still produce C-locale byte semantics. Direct probe: the oracle returns `^.$` vs
  `é` → `nomatch` and `^..$` vs `é` → `match` under all three `LC_ALL` values; the candidate returns the same under
  `LC_ALL=en_US.UTF-8` (fresh process), and the three full runs above show identical verdicts across all three
  environments.
- Does **not** establish the full CLI path (tokenizer→section→decide); that is other seats' ground. It does not
  exercise NUL bytes (the alphabet excludes them; the candidate refuses patterns containing NUL explicitly), newlines
  in text/pattern, or invalid UTF-8.

## 6. Harness liveness — positive controls (scratch-only mutants, candidate untouched)

To show the zero above is not vacuous, three mutants were written **into scratch only** (byte copies of the
candidate with one edit, plus a python-`re` stub module) and run through the same driver at seed `89151006`:

| control | edit (scratch copy) | candidate disagreements | exit |
|---|---|---|---|
| BRE flags | `REG_EXTENDED = 1` → `0` (`cand-bre.py`) | **1042 / 3200** | 1 |
| Always-match | `return …regexec(...) == 0` → `return True` (`cand-always-match.py`) | **1226 / 3200** | 1 |
| python-`re` engine | stub `posix_ere_compile/search/free` over `re` (`cand-python-re.py`) | **404 / 3200** | 1 |

The python-`re` stub's 404 equals the driver's independent python-`re` control count on the same pairs — the two
routes see the same divergence set, which is a consistency check of the comparison logic. Sample minimal pairs the
minimiser produced from these controls: BRE `|`/`""` (`match` vs `nomatch`), always-match `a`/`""` (`nomatch` vs
`match`), python-`re` `)`/`""` (`nomatch` vs `invalid`). These controls are DRAFT self-checks, not measurements, and
they say nothing about the real candidate.

## 7. Risks / limits

1. **Draft bytes.** Candidate sha `2720922b…` at run time. If the L1 changes the candidate before the freeze, this
   report is stale; re-running is one command per locale (§1 rows 2–4).
2. **Same-host libc.** Both sides use glibc's `regcomp`/`regexec`; the test validates the candidate's bridge and
   locale handling, not the correctness of glibc itself. The oracle is independent as a *program* (separate compiled
   C process, its own `regcomp` call), not as an engine.
3. **Sampled patterns.** 3038 distinct pairs/seed, 1703 distinct patterns; a deliberately pathological pattern shape
   (e.g. huge `{m,n}` intervals, which the vocabulary cannot express because it has no pattern digits) is not
   covered. NUL/newline/invalid-UTF-8 are outside the seat's alphabet (§5).
4. **In-process comparison.** The driver calls the three functions directly rather than invoking the tool CLI; it
   therefore cannot catch a divergence introduced by the caller (`decide`/`evaluate`, e.g. re-using a freed buffer).
   Those are separate seats' scope.
5. Python-`re` counts are a motivation figure only; they are not a control on the candidate.

## 8. Hygiene

- Scratch `/fast/scratch/hyaku/mado-r89/R89MExecFuzz` held the oracle binary, the three mutant copies and the JSON
  results; it is deleted after this report was written. The numbers above are frozen into this file.
- The first driver version's import wrote `build/__pycache__` and `w1/__pycache__` (outside this seat's write scope);
  both were removed, the driver now sets `sys.dont_write_bytecode = True` before importing the candidate, and the
  final runs were verified to leave no `__pycache__` (`ls -d` → exit 2, no such file).
- No installs (nothing installed or upgraded). No `git`/`jj` mutation anywhere; the lane was read-only. The fleet
  root, `tools/`, `quality/`, `corpus/`, `receipts/` and `.ufo/state/` were not touched.
- Write set: this report and `R89MExecFuzz-driver.py`, both under `.ufo/waves/round-89/w1/`.

## 9. Files

- `.ufo/waves/round-89/w1/R89MExecFuzz-driver.py` — deterministic pair generator + candidate/oracle/python-`re`
  differential + disagreement minimiser; exit 0 only when the candidate matches the oracle on every pair
  (sha256 `16899f22…f200e`).
- `.ufo/waves/round-89/w1/R89MExecFuzz.md` — this report.

# Mutation matrix — `quality/check-locators.py` (w2 seat MutCheckLocators, round 43)

Target: `quality/check-locators.py` @ data commit 1959770 (bytes identical to base: sha256
`c1ea52ad5db21fdf81022d0425e7cad42fc3e34dd5083915b127a46ab948a27e`, the w1 `ExecLocatorGate` deliverable).
Attack: its selftest teeth plus the round-42 LOG control. Scratch copy only; the lane file was never edited.

## Baselines (pristine)

- **Selftest** (`python3 pristine.py --selftest`): rc=0 — `SELFTEST: cases=18 passed=18 locators=19 miss=6` /
  `SELFTEST: teeth flipped_table_broken=yes flips=11 ok_to_miss=4 miss_to_ok=5` / `SELFTEST: PASS`
  (`out/BASE.selftest.txt`, sha256 `1b76c1d6…`).
- **Control** (`python3 pristine.py --fetch <round-42 fetch> LOG-r42.md` over `git show a35cfdf:LOG.md`,
  saved as `LOG-r42.md`, sha256 `f6c27a3650c7bf4b7f95688978b2979d2c9a39f262686525352c63ae8bc416e2` — identical
  to w1's `LOG-a35cfdf.md`): rc=1, exactly one LOC line —
  `LOC …LOG-r42.md:2483 Hyprland-HyprCtl.cpp:394-395,412-413 fragments=6 supported=1 verdict=MISS`,
  `CHECK_LOCATORS: locators=1 miss=1` (`out/BASE.control.txt`, sha256 `443a61c0…`). Expected MISS confirmed.

## Method

37 single-edit mutants (`mutrun.py`, this dir; each edit is one regex substitution applied exactly once to the
pristine bytes, asserted `count==1` and `new != BASE`). Per mutant, both detectors run; a mutant **survives**
only if selftest rc+output and control rc+output are byte-identical to pristine. Every output stored under
`out/<mutant>.{selftest,control}.txt`; verdicts recomputed from those files (`matrix.tsv`). Python 3.14.8,
stdlib only; no tools installed.

## Matrix (37 mutants: 25 killed, 12 survived)

Selftest kill mechanisms: `case N` = case-table failure, `exit`/`teeth` = explicit failure line, `crash` = exception.
Control kill mechanisms: `OK` = the expected MISS flipped to supported, `rc=0` = exit code, `-summary` = tally line gone, `crash`.

| # | mutant | single edit (function, line) | selftest | control | survivor |
|---|--------|------------------------------|----------|---------|----------|
| 1 | exclusive-bounds | `in_ranges` :84 `<=` → `<` both ends | FAIL case 1 | OK + rc=0 | killed (both) |
| 2 | half-open-bounds | `in_ranges` :84 `<= hi` → `< hi` | FAIL case 1 | OK + rc=0 | killed (both) |
| 3 | no-reversed-normalisation | `parse_ranges` :71-72 swap deleted | FAIL case 7 | =base | killed (selftest) |
| 4 | upper-plus-one | `in_ranges` :84 `hi` → `hi + 1` | FAIL case 2 | OK | killed (selftest) |
| 5 | range-slice-offbyone | `cited_text` :95 `len(lines) + 1` → `len(lines)` | PASS | =base | **SURVIVED** |
| 6 | comma-to-semicolon | `parse_ranges` :69 split `","` → `";"` | crash (ValueError) | crash | killed (both) |
| 7 | token-len-2 | `fragment_tokens` :108 `>= 3` → `>= 2` | FAIL case 11 | =base | killed (selftest) |
| 8 | token-len-4 | `fragment_tokens` :108 `>= 3` → `>= 4` | PASS | =base | **SURVIVED** |
| 9 | token-lower-boundary | `token_occurs` :102-103 left lookaround dropped | PASS | =base | **SURVIVED** |
| 10 | token-insensitive | `token_occurs` :102-103 + `re.IGNORECASE` | FAIL case 18 | =base | killed (selftest) |
| 11 | attr-before-inclusive | :152 `c[1] <= ls` → `c[1] < ls` | PASS | =base | **SURVIVED** |
| 12 | attr-after-exclusive | :153 `c[0] >= le` → `c[0] > le` | PASS | =base | **SURVIVED** |
| 13 | attr-after-first | :154 prefer `after[0]` over `before[-1]` | FAIL case 8 | =base | killed (selftest) |
| 14 | attr-before-farthest | :154 `before[-1]` → `before[0]` | FAIL case 8 | =base | killed (selftest) |
| 15 | support-any | :146 `all(` → `any(` | FAIL case 16 | OK + rc=0 | killed (both) |
| 16 | cited-offbyone | :95 `lines[i - 1]` → `lines[i]` | crash (IndexError) | =base | killed (selftest) |
| 17 | resolve-no-basename | `resolve_name` :112-113 no `rsplit("/")` | FAIL case 13 | =base | killed (selftest) |
| 18 | resolve-always | `resolve_name` :113 returns `base` unconditionally | crash (FileNotFoundError) | crash | killed (both) |
| 19 | id-re-digit-lead | `ID_RE` :54 `[A-Za-z_]` → `[A-Za-z0-9_]` head | PASS | =base | **SURVIVED** |
| 20 | locator-no-lookbehind | `LOCATOR_RE` :56 lookbehind deleted | PASS | =base | **SURVIVED** |
| 21 | locator-no-lookahead | `LOCATOR_RE` :59 lookahead deleted | PASS | =base | **SURVIVED** |
| 22 | frag-keep-empty | `_candidates` :125-126 empty-token filter deleted | FAIL case 11 | =base | killed (selftest) |
| 23 | frag-no-closing-tick | `FRAG_RE` :61 closing backtick dropped | FAIL case 4 | fragments 6→10 | killed (both) |
| 24 | no-re-escape | `token_occurs` :102-103 `re.escape(tok)` → `tok` | PASS | =base | **SURVIVED** (equivalent) |
| 25 | ranges-group-lazy | `LOCATOR_RE` :57 range groups `?` → `??` | FAIL case 5 | locator truncates to `:394` | killed (both) |
| 26 | nofrag-renamed | :166 `"NOFRAG"` → `"NOFRAGMENT"` | crash (selftest regex) | =base | killed (selftest) |
| 27 | verdict-lowercase-ok | :163 `"OK"` → `"ok"` | crash (selftest regex) | =base | killed (selftest) |
| 28 | summary-dropped | :400 summary `print` deleted | PASS | -summary | killed (control) |
| 29 | summary-swapped | :400 `% (total, misses)` → `% (misses, total)` | PASS | =base | **SURVIVED** |
| 30 | miss-count-nofrag | :167 `== "MISS"` → `!= "OK"` | FAIL miss count 6→9 | =base | killed (selftest) |
| 31 | exit-always-zero | :401 `return 1 if misses else 0` → `return 0` | FAIL exit 1→0 | rc=0 | killed (both) |
| 32 | usage-returns-one | :397 usage `return 2` → `return 1` | FAIL exit 2→1 | =base | killed (selftest) |
| 33 | selftest-allows-args | :309 arg guard → `if False:` | FAIL exit 2→0 | =base | killed (selftest) |
| 34 | teeth-identity-flip | :318 teeth lambda = real comparison | FAIL teeth flips=0 | =base | killed (selftest) |
| 35 | teeth-one-direction | :331 keep only `if flips == 0:` | PASS | =base | **SURVIVED** (latent) |
| 36 | verdicts-regex-nofrag | :295 selftest verdict regex drops `NOFRAG` | crash | =base | killed (selftest) |
| 37 | selftest-min-cases-dropped | :360 `or k < 12` deleted | PASS | =base | **SURVIVED** (latent) |

## Survivors, classified (distinguishing inputs demonstrated in `survivors-evidence.md`)

Missing-assertion survivors — each has a shown input where pristine and mutant differ:

| mutant | classification | distinguishing input (checker's own REC/PLAIN fixtures) | pristine → mutant |
|--------|----------------|----------------------------------------------------------|-------------------|
| range-slice-offbyone | missing assertion | `` `epsilon` at `rec.cpp:9` `` — no case cites a fixture's last line; control ranges (:394-413) sit far from receipt EOF | OK rc=0 → MISS rc=1 |
| token-len-4 | missing assertion | `` `foo` at `rec.cpp:2` `` — the table pins the length floor only from below (`ab`, len 2), never from above | MISS rc=1 → NOFRAG rc=0 |
| token-lower-boundary | missing assertion | `` `lpha` at `rec.cpp:2` `` — no case has a token occurring only inside a longer identifier | MISS rc=1 → OK rc=0 |
| attr-before-inclusive | missing assertion | `` `alpha`rec.cpp:2 `` — no case has a fragment flush before its locator | OK → NOFRAG |
| attr-after-exclusive | missing assertion | `rec.cpp:2\`alpha\`` — no case has a fragment flush after its locator | OK → NOFRAG |
| id-re-digit-lead | missing assertion | ``value `123` at `plain.conf:2` `` — no case fragment carries a digit-leading token | NOFRAG rc=0 → MISS rc=1 |
| locator-no-lookbehind | missing assertion | `-rec.cpp:2` — name cannot start with `-`, so pristine finds no token; the mutant matches mid-word | locators=0 → locators=1 (NOFRAG) |
| locator-no-lookahead | missing assertion | `` `alpha` at rec.cpp:2x `` — pristine refuses the bleeding token, the mutant scores `rec.cpp:2` | locators=0 → locators=1 (OK) |
| summary-swapped | missing assertion | `` `beta` at `rec.cpp:2` `` + `` `alpha` at `rec.cpp:5` `` — the registered control has locators=1 miss=1, where a swapped tally is invisible | `locators=2 miss=1` → `locators=1 miss=2` |

Equivalent / latent survivors — no input distinguishes them today, proof recorded:

- **no-re-escape — equivalent by construction.** `fragment_tokens` returns only `ID_RE` matches, i.e. strings over
  `[A-Za-z0-9_]`; `re.escape` is the identity on exactly that set (enumerated all 254,079 word-char strings of length
  1-3: 0 differ). The mutated regex string equals the original for every reachable token.
- **teeth-one-direction — equivalent on every current input; latent missing assertion.** The flipped run of the frozen
  18-case table always breaks both ways (measured constants flips=11, ok_to_miss=4, miss_to_ok=5, all > 0), so the
  deleted `ok_to_miss`/`miss_to_ok` clauses at :331 are tautologies today. The deleted clauses are the only bar against
  a future case table whose flip is one-directional.
- **selftest-min-cases-dropped — equivalent on every current input; latent missing assertion.** `k=18 >= 12` is a
  tautology for the frozen table; the deleted `k < 12` clause at :360 is the only bar against a future table shorter
  than 12 cases.

## Reading

- The selftest teeth are real for everything the table exercises: range inclusion (4 mutants killed), reversed-range
  normalisation, token floor from below, case sensitivity, attribution preference and nearest-before/after (cases 8/9
  are load-bearing in both directions), `all`-semantics, basename resolution, empty-fragment filter, verdict strings,
  miss counting, and all three exit-code paths.
- The control (single locator, single prose line, `locators=1 miss=1`) independently kills 9 mutants, but its tally
  line is self-checking only when `locators != miss` — mutant 29 shows a swapped tally passes both detectors on the
  registered input.
- The 9 missing-assertion survivors are coverage findings, not contract changes: each names the one input class the
  18-case table and the one-line control do not pin (receipt EOF, token floor from above, token boundary, flush
  attribution edges, digit-leading identifiers, locator token edges, tally with distinct counts).

Reproduce: `python3 mutrun.py` then `python3 probe_survivors.py` in this directory (needs `pristine.py`, and the
round-42 fetch dir + `git show a35cfdf:LOG.md` for the control).

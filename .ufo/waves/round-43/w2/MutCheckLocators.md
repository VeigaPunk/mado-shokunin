# w2 MutCheckLocators — mutation test of `quality/check-locators.py` (selftest teeth)

**Mutant set:** 37 single-edit mutants of a scratch copy of `quality/check-locators.py` (sha256
`c1ea52ad5db21fdf81022d0425e7cad42fc3e34dd5083915b127a46ab948a27e` — byte-identical to the lane file at the data
commit and to w1 `ExecLocatorGate`'s deliverable), each one regex substitution applied exactly once: range inclusion
×6, token length/boundary ×4, attribution ×6, name resolution ×5, fragment detection ×5, verdict strings ×5, exit
codes ×3, selftest-teeth internals ×4. **Verdict: 25 killed, 12 survived** — 9 missing assertions (each with a
demonstrated distinguishing input), 2 latent guard deletions (equivalent on every current input), 1 equivalent by
construction (proof below). The landed checker's teeth hold; every survivor is a coverage finding, not a contract
change. Full table: `.ufo/waves/round-43/w2/MutCheckLocators/matrix.md`.

**Detectors (both run per mutant; survivor = byte-identical rc+output on both):**

- Selftest: `python3 <mutant> --selftest` — pristine rc=0, `cases=18 passed=18`, teeth `flips=11 ok_to_miss=4
  miss_to_ok=5`, `SELFTEST: PASS` (`w2/MutCheckLocators/out/BASE.selftest.txt`).
- Round-42 LOG control: `python3 <mutant> --fetch <round-42 fetch> LOG-r42.md` over `git -C <lane> show
  a35cfdf:LOG.md` (sha256 `f6c27a3650c7bf4b…`, same bytes as w1's `LOG-a35cfdf.md`) — pristine rc=1, one LOC line
  `LOG-r42.md:2483 Hyprland-HyprCtl.cpp:394-395,412-413 fragments=6 supported=1 verdict=MISS`,
  `CHECK_LOCATORS: locators=1 miss=1`; the expected MISS confirmed at the base LOG bytes
  (`w2/MutCheckLocators/out/BASE.control.txt`).

**Kills (25).** Range inclusion is well-guarded (strict bounds, half-open, +1 drift all die on cases 1-2 and flip the
control's MISS to OK). The attribution cross-cases 8/9 kill both nearest-before/after mutations in both directions.
Case sensitivity (:102), the `ab` length floor, `all(`-semantics, basename resolution, the empty-fragment filter,
verdict strings, miss counting, all three exit-code paths and the teeth check itself (identity flip → `flips=0`) are
each killed. The control independently kills 9 mutants — including `frag-no-closing-tick` (fragments 6→10) and
`ranges-group-lazy` (locator truncates to `:394`) which the control sees through LOC-line changes the selftest also
catches — and is the *only* detector that kills `summary-dropped` (tally line deleted; selftest never reads it).

**Survivors — missing assertions (9), input demonstrated in `w2/MutCheckLocators/survivors-evidence.md`:**

1. `range-slice-offbyone` (`cited_text` :95 loses the receipt's last line) — input `` `epsilon` at `rec.cpp:9` ``:
   pristine OK, mutant MISS. No case cites a fixture's last line; the control's :394-413 sits far from receipt EOF.
2. `token-len-4` (:108) — input `` `foo` at `rec.cpp:2` ``: MISS → NOFRAG. The table pins the 3-char floor only from
   below (`ab`), never from above.
3. `token-lower-boundary` (:102) — input `` `lpha` at `rec.cpp:2` ``: MISS → OK. No case has a token occurring only
   inside a longer identifier.
4. `attr-before-inclusive` (:152) — input `` `alpha`rec.cpp:2 ``: OK → NOFRAG. Fragment flush against its locator.
5. `attr-after-exclusive` (:153) — input `rec.cpp:2\`alpha\``: OK → NOFRAG.
6. `id-re-digit-lead` (`ID_RE` :54) — input ``value `123` at `plain.conf:2` ``: NOFRAG → MISS.
7. `locator-no-lookbehind` (`LOCATOR_RE` :56) — input `-rec.cpp:2`: locators=0 → locators=1; the lookbehind is the
   only thing stopping mid-word matches when the preceding char is `-`/`.`/word (path prefixes are absorbed by the
   name class, so only these cases distinguish).
8. `locator-no-lookahead` (:59) — input `` `alpha` at rec.cpp:2x ``: locators=0 → mutant scores `rec.cpp:2`.
9. `summary-swapped` (:400) — input `` `beta` at `rec.cpp:2` `` + `` `alpha` at `rec.cpp:5` ``: pristine tally
   `locators=2 miss=1`, mutant `locators=1 miss=2`. The registered control's `locators=1 miss=1` is the one shape
   where a swapped tally is invisible to both detectors.

**Survivors — equivalent/latent (3):** `no-re-escape` is equivalent by construction — `fragment_tokens` only emits
`[A-Za-z0-9_]+` strings and `re.escape` is the identity on that set (enumerated 254,079 word-char strings of length
1-3: 0 differ). `teeth-one-direction` (:331) and `selftest-min-cases-dropped` (:360) delete clauses that are
tautologies for the frozen table (flips=11/ok_to_miss=4/miss_to_ok=5 all > 0; k=18 ≥ 12) — equivalent today, but they
are the only bars against a future one-directional or short case table passing selftest.

**Relation to w1:** `w1/ExecLocatorGate.md` reported the checker's design limits (identifier-as-proxy, line-local
attribution, NOFRAG blind spot, receipt-as-trust-root). This seat does not re-report those: it measures which limits
are *asserted* by the selftest (the 25 kills) versus unpinned (the 12 survivors). No w1 finding was contradicted; the
selftest-teeth claim of w1 ("fails unless the table breaks in both directions") holds for the landed bytes — the
`teeth-identity-flip` mutant dies on it — while its two secondary clauses are unguarded against future tables
(latent survivors 35/37).

**Scope, safety, restoration:** writes were only to `.ufo/waves/round-43/w2/MutCheckLocators{,.md}` and
`/fast/scratch/hyaku/mado-r43/MutCheckLocators/` (deleted at close; receipts copied out first). The lane file was
never edited: sha256 `c1ea52ad…` before and after, `git status --porcelain quality/check-locators.py` empty. No
pacman, no host-service or compositor mutation (only the allowed read verbs were not even needed — the control uses
pinned receipts, not a live socket). Tools installed: none (Python 3.14.8 stdlib only, matching the checker's own
stdlib-only contract). No subagents; all runs local and bounded.

**Files (seat dir):** `matrix.md` (full table + classification), `matrix.tsv` (machine-readable verdicts +
mutant hashes), `survivors-evidence.md` (verbatim pristine-vs-mutant runs for all 9 distinguishing inputs + the
equivalence enumeration), `out/` (75 files: `BASE.*` and per-mutant selftest+control outputs), `pristine.py`
(verified copy), `mutrun.py`, `probe_survivors.py` (harness; rerunnable). Baseline hashes: selftest
`1b76c1d607a853e124720c23063e6fee903e1b6eb98a11c818a90b42150363a5`, control
`443a61c017b7bca201c5811090ae59646c13f5ef186ecb378f5352004d5b0b39`, matrix.tsv `2ba10ba0b851e2aa…`.

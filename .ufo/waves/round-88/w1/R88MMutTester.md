# R88MMutTester — round 88 w1: counter mutation test and tool-mutant audit

Seat: R88MMutTester (mutation-tester). Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Report written 2026-11-06. No candidate scoring was performed: neither authored case file was read or
scored (`mako-cases-r88.json` did not exist yet; `containment-cases-r88.json` was not opened). All tool
runs below used fixtures I authored, as the wave rule allows.

Result in one line: **34 counter mutations (18 C1 + 16 C2): 17 killed, 17 survived, 0 inconclusive.**
**Tool mutants: 24/24 are non-equivalent to the candidate; each needs one concrete case listed below.**

## Inputs (bytes tested)

| file | sha256 |
|---|---|
| `quality/counters/c1-r88-mako-fields.py` | `b5341ff89cdbeae84ad2abfa1f11170adc95e11eeed742e3f2db54a3bca360b1` |
| `quality/counters/c2-r88-include-containment.py` | `0a08978d4b9f48ca48b01fe1585bb746f2628a5fc1761e5d440e420b856f9bbb` |
| `quality/counters/c1-r87-mako-criteria.py` | `4d801c30b302ed5972142415012d8f461109459d9c44e85e0badef57a2ed3645` (matches the r88 pin) |
| `.ufo/waves/round-88/build/mado-mako.c2.py` | `7a1fdf9b50ded5d4398922bdc0191b9cd7b520e5f404f7e20725b8fa81bf239b` (= `tools/mado-mako.py` at read time) |
| `.ufo/waves/round-88/controls/mako-mutants-r88.json` | `40645a2854072d23795395bd13adb1058fba741fc4b1b0dac92fd02a9761d49b` (declaration match) |
| `.ufo/waves/round-88/controls/containment-mutants-r88.json` | `49373eeeceef5ae6e76bfc7327f9f511ceef0e9fd4a8b3aadafeee8c6a084a85` (declaration match) |

The candidate moved during the wave: I first audited `8d86f131b0964c2c0ee8e92df543611f0f850ef1960219b0d71a8f3042dbabfb`
(15:49) and re-audited the current `7a1fdf9b...` (15:59). The only delta is a new check inside the tool's
own `selftest` (`bool-no-input`); resolver behaviour and every mutant anchor are unchanged, and both
audits produced identical verdicts (24/24 distinguished, all anchors unique). Table below is the
`7a1fdf9b` run.

## Method

- `S=/fast/scratch/hyaku/mado-r88/R88MMutTester`; counters copied to `$S/counters/` together with the r87
  counter they import by path. Baseline, exit codes observed:
  - `python3 -I $S/counters/c1-r88-mako-fields.py --selftest --scratch-root $S` → **exit 0, 15/15 PASS**
  - `python3 -I $S/counters/c2-r88-include-containment.py --selftest --scratch-root $S` → **exit 0, 12/12 PASS**
- One mutation at a time: a fresh copy of both files per mutation, assert the anchor occurs exactly once,
  apply a single `str.replace(old, new, 1)`, then run `python3 -I <copy> --selftest --scratch-root <fresh dir>`.
  Killed = selftest exit ≠ 0. The pristine scratch copies were re-hashed after all runs and are unchanged
  (`b5341f...`, `0a0897...`, `4d801c3...`); the copies in `quality/counters/` were never written.
- Why so many survivors: both `--selftest` implementations are hermetic — they never call `run()`, never
  build a git fixture, and never touch the sha pins. Guards that live only in `run()` therefore have zero
  executable test coverage. This is a coverage finding about the counters' selftests, not a change to the
  predicate or the contract.

## Table 1 — mutations of `quality/counters/c1-r88-mako-fields.py` (18)

| mutant | point | edit | selftest | failing assertion |
|---|---|---|---|---|
| C1-M01-naive-le | c1-r88-mako-fields.py:234 | `naive < n` -> `naive <= n` | SURVIVED (exit 0) | — |
| C1-M02-globals-le | c1-r88-mako-fields.py:234 | `globals_ < n` -> `globals_ <= n` | SURVIVED (exit 0) | — |
| C1-M03-base-le | c1-r88-mako-fields.py:234 | `base_correct < n` -> `base_correct <= n` | KILLED (exit 1) | base tool scoring N (do-nothing reaches target) -> TARGET_MISSED |
| C1-M04-drop-carried | c1-r88-mako-fields.py:233 | `killed == m and carried == carried_needed and naive < n` -> `killed == m and naive < n` | KILLED (exit 1) | a missing carried case -> TARGET_MISSED |
| C1-M05-drop-base | c1-r88-mako-fields.py:234 | ` and base_correct < n)` -> `)` | KILLED (exit 1) | base tool scoring N (do-nothing reaches target) -> TARGET_MISSED |
| C1-M06-killed-m-minus-1 | c1-r88-mako-fields.py:233 | `correct == n and killed == m and` -> `... killed == m - 1 and` | KILLED (exit 1) | all conjuncts hold -> TARGET_MET; a surviving mutant -> TARGET_MISSED |
| C1-M07-invert-hit | c1-r88-mako-fields.py:229 | `hit = mverdicts != verdicts` -> `==` | KILLED (exit 1) | correct fixture tool scores N/N and kills the mutant; all conjuncts hold -> TARGET_MET |
| C1-M08-correct-n-minus-1 | c1-r88-mako-fields.py:233 | `met = (correct == n` -> `met = (correct >= n - 1` | SURVIVED (exit 0) | — |
| C1-M09-carried-always-full | c1-r88-mako-fields.py:164 | `sum(canon(entry) in mine ...)` -> `len(r87)` | KILLED (exit 1) | carried count refuses an edited prior case |
| C1-M10-skip-cases-sha | c1-r88-mako-fields.py:258 | `if sha256(cases_raw) != args.expect_cases_sha256:` -> `if False:` | SURVIVED (exit 0) | — |
| C1-M11-skip-mutants-sha | c1-r88-mako-fields.py:262 | `if sha256(mutants_raw) != args.expect_mutants_sha256:` -> `if False:` | SURVIVED (exit 0) | — |
| C1-M12-pin-check-off | c1-r88-mako-fields.py:73 | `if R87_DIGEST != R87_COUNTER_SHA256:` -> `if False:` | SURVIVED (exit 0) | — |
| C1-M13-declared-check-off | c1-r88-mako-fields.py:201 | `if declared is not None and len(mutants) != declared:` -> `if False:` | SURVIVED (exit 0) | — |
| C1-M14-range-check-off | c1-r88-mako-fields.py:199 | `if range_check and not (N_MIN <= n <= N_MAX):` -> `if False:` | SURVIVED (exit 0) | — |
| C1-M15-drop-string-args | c1-r88-mako-fields.py:169 | `for name in STRING_ARGS:` -> `for name in ():` | KILLED (exit 1) | correct fixture tool scores N/N and kills the mutant; all conjuncts hold -> TARGET_MET; base tool scoring N -> TARGET_MISSED |
| C1-M16-drop-bool-args | c1-r88-mako-fields.py:174 | `for name in BOOL_ARGS:` -> `for name in ():` | SURVIVED (exit 0) | — |
| C1-M17-only-app-name | c1-r88-mako-fields.py:169 | `for name in STRING_ARGS:` -> `for name in ("app-name",):` | SURVIVED (exit 0) | — |
| C1-M18-carried-inverted | c1-r88-mako-fields.py:164 | `canon(entry) in mine` -> `canon(entry) not in mine` | KILLED (exit 1) | carried count finds an unchanged prior case; carried count refuses an edited prior case |

Note on C1-M15: it is killed only because `STRING_ARGS` also carries `app-name`, and the fixture's
`section-override` case needs `--app-name`. The **new** fields are covered by neither M15 nor the selftest:
M16 and M17, which drop exactly the new booleans/new strings, survive (see below). The source has no `!=`
inside `carried_count`; the requested `!=`->`==` equivalent is M18 (inverted membership).

## Table 2 — mutations of `quality/counters/c2-r88-include-containment.py` (16)

| mutant | point | edit | selftest | failing assertion |
|---|---|---|---|---|
| C2-M01-base-le | c2-r88-include-containment.py:190 | `base_correct < k` -> `base_correct <= k` | KILLED (exit 1) | base equal to candidate (do-nothing reaches K) -> TARGET_MISSED |
| C2-M02-forgery-le | c2-r88-include-containment.py:190 | `forgery_correct < k` -> `forgery_correct <= k` | KILLED (exit 1) | without positive cases refuse-all forgery reaches K -> TARGET_MISSED |
| C2-M03-correct-k-minus-1 | c2-r88-include-containment.py:190 | `met = correct == k` -> `met = correct >= k - 1` | SURVIVED (exit 0) | — |
| C2-M04-killed-ge-m-minus-1 | c2-r88-include-containment.py:190 | `killed == m` -> `killed >= m - 1` | SURVIVED (exit 0) | — |
| C2-M05-drop-forgery | c2-r88-include-containment.py:190 | ` and forgery_correct < k` -> `` | KILLED (exit 1) | without positive cases refuse-all forgery reaches K -> TARGET_MISSED |
| C2-M06-base-true | c2-r88-include-containment.py:190 | `base_correct < k` -> `True` | KILLED (exit 1) | base equal to candidate (do-nothing reaches K) -> TARGET_MISSED |
| C2-M07-invert-hit | c2-r88-include-containment.py:185 | `hit = ... != verdicts` -> `== verdicts` | KILLED (exit 1) | the check-off mutant is killed; all conjuncts hold -> TARGET_MET |
| C2-M08-anchor-check-off | c2-r88-include-containment.py:162 | `if tool_text.count(FORGERY_OLD) != 1:` -> `if False:` | KILLED (exit 1) | missing forgery anchor is a setup error |
| C2-M09-skip-cases-sha | c2-r88-include-containment.py:214 | `if sha256(cases_raw) != args.expect_cases_sha256:` -> `if False:` | SURVIVED (exit 0) | — |
| C2-M10-skip-mutants-sha | c2-r88-include-containment.py:218 | `if sha256(mutants_raw) != args.expect_mutants_sha256:` -> `if False:` | SURVIVED (exit 0) | — |
| C2-M11-range-check-off | c2-r88-include-containment.py:158 | `if range_check and not (K_MIN <= k <= K_MAX):` -> `if False:` | SURVIVED (exit 0) | — |
| C2-M12-declared-check-off | c2-r88-include-containment.py:160 | `if declared is not None and len(mutants) != declared:` -> `if False:` | SURVIVED (exit 0) | — |
| C2-M13-forgery-allow-all | c2-r88-include-containment.py:45 | `FORGERY_NEW = "if True:"` -> `"if False:"` | KILLED (exit 1) | without positive cases refuse-all forgery reaches K -> TARGET_MISSED |
| C2-M14-forge-base-k | c2-r88-include-containment.py:173 | `base_correct = sum(run_all(base, ...))` -> `base_correct = k` | KILLED (exit 1) | base control (no containment) scores below K; all conjuncts hold -> TARGET_MET |
| C2-M15-correct-equals-k | c2-r88-include-containment.py:188 | `correct = sum(verdicts)` -> `correct = k` | SURVIVED (exit 0) | — |
| C2-M16-drop-read-roots | c2-r88-include-containment.py:132 | `for rel in case["roots"]:` -> `for rel in []:` | KILLED (exit 1) | containing fixture tool scores K/K; all conjuncts hold -> TARGET_MET |

## Survivors and the missing selftest assertion

C1 (10 survivors):

1. **C1-M01** (naive `<` -> `<=`): no fixture in which the `naive-toplevel` control scores N. The good
   run only shows it below N, so turning the conjunct into a tautology is invisible. Missing assertion:
   a fixture case set resolvable by `naive_values` (plain global `key=value` lines) that asserts
   TARGET_MISSED because `naive_correct == N`.
2. **C1-M02** (globals `<` -> `<=`): same defect for the `globals-include` control; missing the analogous
   "control reaches N -> TARGET_MISSED" fixture.
3. **C1-M08** (`correct == n` -> `>= n-1`): no selftest fixture with exactly one failing case and every
   other conjunct satisfied, so a one-case-wrong tool still scores TARGET_MET unobserved. Missing:
   `evaluate(<tool failing case 2>, ..., carried_needed=1)` -> assert `correct == 1` and TARGET_MISSED.
4. **C1-M10** (`--expect-cases-sha256` check off) and **C1-M11** (`--expect-mutants-sha256` check off):
   both comparisons live only in `run()`, which the selftest never calls. Missing: a fixture git repo fed
   to `run()` with a wrong expected sha, asserting exit 2 (`SETUP_ERROR`). This is the round's central
   anti-forgery device (r87 R4/r86 R2) with no executable test.
5. **C1-M12** (`check_r87_pin` body off): the selftest's first check compares `R87_DIGEST` and
   `R87_COUNTER_SHA256` itself instead of calling the guard. Missing: assert `check_r87_pin()` raises
   `SetupError` when the loaded digest differs (monkeypatch `R87_DIGEST`).
6. **C1-M13** (`declared` count guard off) and **C1-M14** (N-range guard off): mutually masking. The only
   assertion touching either is `evaluate(FIXTURE_TOOL, wrong, cases, mutants, scratch, 1)` with N=2 and
   the default `declared=19`; it raises because `len(mutants)=1 != 19`, so it passes even with the range
   guard disabled. Proof: I applied M13+M14 together to one copy; the selftest then failed with
   `FAIL N outside the declared range is a setup error` (exit 1), i.e. each guard alone survives only
   because the other raises first. Missing: two independent assertions — `declared` mismatch with N in
   range, and N outside range with `declared` matching.
7. **C1-M16** (drop `--actionable/--expiring` transmission): the fixture tool accepts but ignores those
   flags, so no fixture expectation changes. Missing: a fixture tool (or case) whose effective output
   depends on the boolean input — otherwise the whole C1 boolean plumbing is untested end-to-end.
8. **C1-M17** (transmit only `app-name`): the fixture tool ignores `category` and the other new string
   inputs, so dropping their argv transmission is invisible. Missing: a fixture case whose expected
   effective depends on `--category`/`--summary`/etc. reaching the tool.

C2 (7 survivors):

1. **C2-M03** (`correct == k` -> `>= k-1`): no fixture tool with one wrong case; a one-case-wrong tool
   still scores TARGET_MET. Missing: `evaluate(<tool failing one case>, ..., declared=None,
   range_check=False)` -> assert `correct == K-1` and TARGET_MISSED.
2. **C2-M04** (`killed == m` -> `killed >= m-1`): no surviving-mutant fixture, so one survivor passes.
   Missing: add a no-op mutant to a fixture list with all other conjuncts satisfied -> TARGET_MISSED.
3. **C2-M09/C2-M10** (cases/mutants sha pins off): `run()` is unreached; same missing fixture-repo
   assertion as C1-M10/M11.
4. **C2-M11** (K-range guard off): every selftest `evaluate` call passes `range_check=False`, and no
   assertion ever exercises the guard. Missing: `evaluate` with K outside 12..24 and default
   `range_check` -> `SetupError`.
5. **C2-M12** (`declared` guard off): every selftest call passes `declared=None`; missing
   `evaluate(..., declared=2)` with 1 mutant -> `SetupError`.
6. **C2-M15** (`correct = k`): the selftest never evaluates a wrong tool, so forcing the count is
   invisible; same root as C2-M03 and stronger (it fakes the count rather than relaxing the compare).

No survivor changes the predicate. These are coverage findings for the L1 to weigh at the freeze; the
predicate sentences and kill rules are untouched by this seat.

## Tool-mutant audit (`build/mado-mako.c2.py`, sha `7a1fdf9b...`)

Method: for each entry of both mutant files I asserted `tool_text.count(old) == 1` against the candidate
bytes (24/24 unique), materialized the mutant in scratch, and ran candidate and mutant with identical
argv/env/cwd on a fixture I authored for that mutant (never the authored case files). "Differs" is
`(exit, stdout)` inequality. **All 24 differ; none is behaviourally equivalent; 0 unusable anchors.**

Fixture files used beyond the config shown: M03 needs `home/dark.ini` = `anchor=bottom-left` (cwd is
`home`, so the mutant resolves `dark.ini` there); M04 needs `home/extra.ini` = `anchor=bottom-left`
(mutant targets `/extra.ini`, refused as outside the roots, so the difference does not depend on the host
filesystem); K1/K2 need `home/i` as a symlink to `out/s` with `out/s` = `width=666`; K3 needs
`home-evil/s` = `width=666`; K4 needs `out/s` = `width=666` and `--read-root <case>/out`; K5 needs
`home/i` = `width=444`. `@ROOT@` is the realpath of the case root.

| mutant | anchor count | equivalent? | distinguishing config text | arguments | candidate -> mutant |
|---|---|---|---|---|---|
| M01-criteria-setdefault | 1 | no | `[app-name=slack]\nanchor=bottom-left\n` | `--app-name slack` | effective anchor `bottom-left` -> `top-right` |
| M02-global-ignored | 1 | no | `anchor=bottom-left\n` | — | effective anchor `bottom-left` -> `top-right` |
| M03-relative-include-accepted | 1 | no | `include=dark.ini\n` | — | refusals 1 -> 0; anchor `top-right` -> `bottom-left`; applied `[]` -> `[global-section, include:dark.ini]` |
| M04-tilde-ignores-home | 1 | no | `include=~/extra.ini\n` | — | refusals 0 -> 1; anchor `bottom-left` -> `top-right`; include applied vs refused |
| M05-no-initial-mode | 1 | no | `[mode=default]\nanchor=bottom-left\n` | — | anchor `bottom-left` -> `top-right`; section applied vs not |
| M06-no-defaults | 1 | no | `` (empty file) | — | 37 default keys -> `{}` (anchor `top-right` -> absent) |
| M07-app-name-ignored | 1 | no | `[app-name=slack]\nanchor=bottom-left\n` | `--app-name discord` | anchor `top-right` -> `bottom-left` (section matches in mutant) |
| M08-missing-input-matches | 1 | no | `[app-name=slack]\nanchor=bottom-left\n` | — (no `--app-name`) | refusals 1 -> 0; anchor `top-right` -> `bottom-left` |
| M09-urgency-inverted | 1 | no | `[urgency=critical]\nanchor=bottom-left\n` | `--urgency low` | anchor `top-right` -> `bottom-left` |
| M10-unterminated-quote-accepted | 1 | no | `[app-name="slack]\nanchor=bottom-left\n` | — | refusals 1 -> 0; anchor `top-right` -> `bottom-left` (mutant treats header as empty match) |
| M11-string-mismatch-ignored | 1 | no | `[summary="Build done"]\nanchor=bottom-left\n` | `--summary Other` | anchor `top-right` -> `bottom-left` |
| M12-string-missing-input-matches | 1 | no | `[category=email]\nanchor=bottom-left\n` | — (no `--category`) | refusals 1 -> 0; anchor `top-right` -> `bottom-left` |
| M13-bool-negation-ignored | 1 | no | `[!actionable]\nanchor=bottom-left\n` | `--actionable false` | anchor `bottom-left` -> `top-right` (mutant reads the negation as true) |
| M14-bool-casefold-dropped | 1 | no | `[actionable=TRUE]\nanchor=bottom-left\n` | `--actionable true` | refusals 0 -> 1; anchor `bottom-left` -> `top-right` |
| M15-bool-criteria-inverted | 1 | no | `[actionable=true]\nanchor=bottom-left\n` | `--actionable true` | anchor `bottom-left` -> `top-right` |
| M16-bool-missing-input-matches | 1 | no | `[expiring=true]\nanchor=bottom-left\n` | — (no `--expiring`) | refusals 1 -> 0; anchor `top-right` -> `bottom-left` |
| M17-bool-invalid-accepted | 1 | no | `[actionable=yes]\nanchor=bottom-left\n` | `--actionable true` | refusals 1 -> 0 only (the case must assert the refusal, not just the effective map) |
| M18-option-bool-not-normalized | 1 | no | `icons=true\n` | — | effective `icons` `1` -> `true` |
| M19-bare-bool-refused | 1 | no | `[actionable]\nanchor=bottom-left\n` | `--actionable true` | refusals 0 -> 1; anchor `bottom-left` -> `top-right` |
| K1-containment-skipped | 1 | no | `include=~/i\n` (`home/i` -> symlink `out/s`, `out/s` = `width=666`) | — | refusals 1 -> 0; width `300` -> `666`; escape read |
| K2-lexical-resolution | 1 | no | `include=~/i\n` (same symlink fixture) | — | refusals 1 -> 0; width `300` -> `666` (abspath passes, open follows the link) |
| K3-prefix-without-separator | 1 | no | `include=@ROOT@/home-evil/s\n` (`home-evil/s` = `width=666`) | — | refusals 1 -> 0; width `300` -> `666` (prefix match without `/`) |
| K4-read-roots-ignored | 1 | no | `include=@ROOT@/out/s\n` (`out/s` = `width=666`) | `--read-root <case>/out` | refusals 0 -> 1; width `666` -> `300` (declared root dropped) |
| K5-home-not-a-root | 1 | no | `include=~/i\n` (`home/i` = `width=444`) | — | refusals 0 -> 1; width `444` -> `300` (home not a root) |

Case-set requirements implied by the table (what the L1 should verify the authored cases contain, without
me scoring them): M01 a criteria section overriding a default or global value; M03 any relative
`include=`; M04 a `~/` include that exists only under `--home`; M05 `[mode=default]`; M06 an empty/absent
effective override with a default expectation; M11 a quoted summary/body value differing from `--summary`
/`--body`; M17 an invalid boolean value **with** the flag supplied and `refusals: present`; M18 a style
boolean written `true`/`false` (expect `1`/`0`); M19 a bare `actionable`/`expiring`; K1/K2 a symlinked
include escaping `--home`; K3 a `<home>-evil` prefix sibling; K4 an outside path under `--read-root`;
K5 an in-home include with no declared roots. If any of these is absent from the authored case set, the
corresponding declared mutant is a case-set survivor even though it is non-equivalent.

## Receipts / hashes

Scratch `S=/fast/scratch/hyaku/mado-r88/R88MMutTester` held: `counters/` (pristine copies, re-hashed
unchanged after all runs), `candidate/tool.py` (`7a1fdf9b...`), `runs/` and `audit/` (per-mutation copies
and outputs), `receipts/` (`mutations.log`, `counter-mutations.json`, `audit-7a1fdf9b.log`,
`mutant-audit.json`, `base-c1.out`, `base-c2.out`, `tables`, `counter-tables.md`). Every mutated copy is a
single-edit derivative; the pristine copies and the repo files were never modified. Hashes of the mutated
bytes follow (before = pristine sha above):

```
[c1] before=b5341ff89cdbeae84ad2abfa1f11170adc95e11eeed742e3f2db54a3bca360b1
C1-M01-naive-le after=55a5b1678cdf124e9f4004f1d3163e7d7135f7d3434a58a0c99a45ecd3410c66
C1-M02-globals-le after=0b6f63754c450b945e9d453de63b72e3b127869c503ac8b7d6c7bbe34da08656
C1-M03-base-le after=531fb396f4bec0d9e4d539cd75e3eccf087d773d1ca239d71499e00c21bada69
C1-M04-drop-carried after=a750a288ad501c0bd5c08053b5034cb136e784a88f5e1e4cb9bbcb29d8f2e243
C1-M05-drop-base after=429c1cac0d59d2d7bcb14a91ed41f618c329988a55b0896c39c7b39ce0410e87
C1-M06-killed-m-minus-1 after=ce9e9666e0570f83e0036dc8d3a0b4279b3879400c22bc7c422c28947ea034ae
C1-M07-invert-hit after=af1e69767535656189cc12ab4263c990ed8ccece71ec3f62e3ee994d894f8577
C1-M08-correct-n-minus-1 after=f4683273900d881a1cff6e32490b7f37d6385b3d1690f5587d85755ce3a3b0b4
C1-M09-carried-always-full after=89239c82e9bdb149254380c5ae1da32c0a38ce360ef2f57f2b3d0db58a333d20
C1-M10-skip-cases-sha after=052d46c9997ced3b773930c5e30fd6970a99c38a288786f40d8dfac0eba099f3
C1-M11-skip-mutants-sha after=e24dc63e95fb5ebee38ca30039b8b92a56c08f1df7e36d236184adb0c5b13300
C1-M12-pin-check-off after=f4de662cc5c5993443bfb1fbd3b75552d7847bbf29e9d63d0ea3b7581c7ecf39
C1-M13-declared-check-off after=57ae021165d3fc225d1516a8896c2dfe3dd2ed9f7904820a9302a0cb461f6794
C1-M14-range-check-off after=9020467db480df93867e82c0f40cf2ae8d1e88b46f9c83d7ffa5141502243139
C1-M15-drop-string-args after=2b44fa75f54292c1b2242fae3cafdc404a97888b56ec7ba0787af62d47e61973
C1-M16-drop-bool-args after=12d9c3bd128180f15fb56dd797a978562cbd38ee6343ac797df69251077f0547
C1-M17-only-app-name after=5f1888b8a7ff3f60d5747a7c8e894c551c5a1b2dee0917c0773f2f1cade4b8ca
C1-M18-carried-inverted after=102534ae3e1d33bbbeaf820f4ec78e06f9138b526ee21457341c9667bd20b60f
[c2] before=0a08978d4b9f48ca48b01fe1585bb746f2628a5fc1761e5d440e420b856f9bbb
C2-M01-base-le after=ef163ade8fdf4aaf10fef8fc0470b4504ac194ad6963a9f1e83614928a33634f
C2-M02-forgery-le after=4f09b4eb933eb77a385341f75b36e4a311a0cb5c445602ecb88cc67b3663f6c1
C2-M03-correct-k-minus-1 after=864f9e71e0ad3bca8a6a650cbb7236ab666925d6c591c8a5dacaba244074b7f9
C2-M04-killed-ge-m-minus-1 after=da02cb4c53312ad7993d16bd36746c2c9372e8954d6b03fd327e5626cd1f5963
C2-M05-drop-forgery after=3d428cc63daeafe1ffba9f88b7a301193c3135c77484a93ffb1021cfd37c2573
C2-M06-base-true after=7a97e9f0f92671ae9fa65e615269d6e5e602d3d913d662efb0679d0bc90ae804
C2-M07-invert-hit after=3db8fb729524e04e088d9d051ec371b9dc3d9172033d394ff7e595df2a25ef80
C2-M08-anchor-check-off after=a047340d0899edc50a19e0aa19e8e3b32960aad2a760e0e92fca61f9e341f662
C2-M09-skip-cases-sha after=6fbf5fc02bda294f44bfc910664e19dee05474e3615358880dfd196377ac07c4
C2-M10-skip-mutants-sha after=bc28de8fd9e4b8ae2cbcc8f64cb5f72800753edb3f46cc3d5d4f6c0a6dfa4518
C2-M11-range-check-off after=4ee8fa21043fee968d184fb7a5fbb0c449e3aa7db5c20ec6fe4d004db7afbe1e
C2-M12-declared-check-off after=84e08a9b33ad6c72453e8cae13378e0112a64ed51449ca6a0dc572fa14aa0438
C2-M13-forgery-allow-all after=d037f32612cf975ee0c01e9079a60e9e6e6928942e2068f3b3c976e0560918f6
C2-M14-forge-base-k after=981f66fe3c5bd4a66bfa6d582c49ef82d5d714b2aae662520b7c587389b25c6a
C2-M15-correct-equals-k after=75abe4e873f78e455c3f5c4ce69818c434a5eb79eeeb6bd4c277307c220e85ea
C2-M16-drop-read-roots after=bae531890eb4191b49cab5603f8f2fd8e213c7b36d77e34d5b167c792807fc7a
[tool] candidate=7a1fdf9b50ded5d4398922bdc0191b9cd7b520e5f404f7e20725b8fa81bf239b
M01-criteria-setdefault after=363eb5780c3dc315fa154d7b552b892016971ca26c389d98e9a102eb6ef194f0
M02-global-ignored after=8574f6bcd90c08831ff9dc7cd2b89fdf0c3598dc70bec13bf3468a4404bed09d
M03-relative-include-accepted after=864e2d68100eea1931531c97a6004fcf518478dc7e783d12fd6e741bf71f9b18
M04-tilde-ignores-home after=2d18f94d899a12277a9313ae62ed4f138e9353bfa25a8ef367a82972545a2cf6
M05-no-initial-mode after=9dc545e5fa92d74c570dfd14a33618a83fb86aa224286758d509fb936396e04b
M06-no-defaults after=910835a70b7faf25fe52a792f0b47c8724128c9e7f9a7ec487963cb68ea5960b
M07-app-name-ignored after=cde3ad34bcbf160d92f7f8671ae6e4c97587411ff45c28201dc589b9a23429d6
M08-missing-input-matches after=a1f93b13ed494c6de238af67ffe93cf2cdb40a080fbe2bd8a66378c584c0b248
M09-urgency-inverted after=d936a1ad68f42392809792a1be2b18fddcc5106599edf16bbaedae921ce2821d
M10-unterminated-quote-accepted after=5e2314eb313d0059e8a7709f4538e807634da9b1d590365c6671174049bf297e
M11-string-mismatch-ignored after=35159ce15e7a202ee32b59506c6a29e9dffe98943f3a952c890db608ae279546
M12-string-missing-input-matches after=a8dfe1953d412aeab79cfb2b0e537925b2b88a2dfd7bead42bbe92a4459127bb
M13-bool-negation-ignored after=bb6cf2dd027e92d6e3dda430bdf1aa9eecc12ef343c94b1c48613dad109ebc75
M14-bool-casefold-dropped after=88ccbe5c55423a9bca72bb56e4a5e5b2718cfa0b1611f1cc4dfdfcd3d684f939
M15-bool-criteria-inverted after=d8609d1275984153c79823fe4467c7f5307bfea7e9e790fde345d42ae60af4c6
M16-bool-missing-input-matches after=52b52b5d2a97378db452ad3b98dad0ec643515fa544d6491c7ceff12997d348b
M17-bool-invalid-accepted after=95b74f99e63c67dfc5d9ff7266383fdca361c5eafe128e7263f6f076ef2be545
M18-option-bool-not-normalized after=ca17444ee00aa4d2878f92cc9eb0402e3164a12e73e485c40f2823a4666a8e96
M19-bare-bool-refused after=691141c9b03f33c42ec13c4d4d4c90c59394f5abff13903cb16e9fb961a1941d
K1-containment-skipped after=6edbc18efe4d8485d5276610cf2e9477beac8768a5f016f59fc78b83d1324c83
K2-lexical-resolution after=eb1ed60924f266ea08b928f82a88b777aea41d397c7db4cd8b8b192a8ddd3be4
K3-prefix-without-separator after=ed10fa6951977e0de0a838057c5418d8186baee9b74b53a273e85680f8627a45
K4-read-roots-ignored after=c52e84c0196daafa61698cce094c5503796c03aba40bfa15a7fbaa3f38196d15
K5-home-not-a-root after=72af536e8160e4a5cb38b0676b29e704673204d9b8940fe22f3ef013e420dc90
```

Commands run and exit codes observed: baseline c1 selftest exit 0 (15/15); baseline c2 selftest exit 0
(12/12); 34 mutation selftests (table above); double-guard probe exit 1 with
`FAIL N outside the declared range is a setup error`; `sha256sum` checks on the pristine copies and the
repo counters (unchanged). No tool installs; no pacman transaction; no git/jj mutation anywhere. Scratch
`/fast/scratch/hyaku/mado-r88/R88MMutTester` was deleted after its receipts were transcribed here
(`test -e` false; no receipt file is left behind).

# R87MutTester — mutation probe, round 87 (w1)

Seat: R87MutTester (mutation-tester, leaf). Scope: mutate scratch copies of `tools/mado-mako.py` (C1) and
`quality/counters/c2-r87-control-fidelity.py` (C2); run each mutant on the same bounded detector as its pristine copy.
No lane file was written. Scratch `$HYAKU_SCRATCH/mado-r87/R87MutTester` removed on exit.

## Inputs (sha256, read from the lane)

| file | sha256 |
|---|---|
| `tools/mado-mako.py` (pristine copy) | d1848f1d86e8db142345af3297afb47473fd49cd9e43b5bc3cfab77908943e61 |
| `quality/counters/c1-r87-mako-criteria.py` | 71aa92738256b6eb5eebd92909d8586dea127fa6f524394fa59bbfabc5508fe0 |
| `quality/counters/c2-r87-control-fidelity.py` | e4654d9de1dc14a49576b0a8df2e57ad43ca98589735e725179c421cafdbed60 |
| `controls/mako-cases-r87.json` (frozen, 23 cases, appeared at 06:21) | 9896daca30f1427dadf4c3446f037e135fde27cb9cce47fe8f44690fb7440660 |
| `controls/mako-mutants-r87.json` (frozen, 10 mutants) | 362894f475e536d7d4957a4596ac4b67e35c9f7c0ee72b4d765f69eb6601812f |
| `controls/r86-figures-r87.json` | da21797b07e6ae09f4e78f49f4dcefceee17164c8af148c8ba7676bd125fe092 |
| lane HEAD (base) | e4875ba5619053cc3f91bb2f4d819e189df4088c |

Wait-gate: the three tool and counter artifacts were present after the sixth 60-second check (05:55). The frozen cases JSON was absent through the first check of a second wait loop and appeared after the fourth check (06:21). The mutants JSON was present from 05:55. The 15-check limit was not reached for the three named artifacts.

## Headline (what blocks the claims, before any mutant)

1. **C1 frozen cases cannot be loaded by the counter as written.** Three independent schema defects in
   `mako-cases-r87.json`, each a `SetupError` or a case that no tool can pass:
   - ids are upper-case (`C01-global-section-applies`); the counter's `ID_RE` is `^[a-z0-9][a-z0-9-]{0,63}$` → `bad or duplicate case id`.
   - `args` keys are `app_name` / `modes`; the counter accepts `app-name` / `mode` only → `C01….args: unknown or non-object args`.
   - case C13 `config` is `.config_mako/config`; the fixture writes `.config/mako/config` → the tool exits 2 on every run.
2. **Even with those three fixed in a scratch copy, the frozen cases kill only 6 of the 10 declared mutants.** M05 (no initial mode),
   M06 (no defaults), M08 (missing input matches), M10 (unterminated quote) survive the frozen case set. C1 therefore cannot reach
   TARGET_MET as the declaration is written (predicate: all M killed). Score as frozen: 22/23 correct (C13 fails);
   scratch-fixed: 23/23 correct; `evaluate()` verdict TARGET_MISSED in both (killed 6/10; naive 6/23, globals 7/23 — controls fine).
3. **C2 frozen figure F2 is not evaluable at the lane's bytes.** `stated_at.text` `"flooding 48/75 vs held 75/75"` is not a substring of
   SCORECARD.md: the file wraps it (`...pass | flooding` ↵ `48/75 vs held 75/75, TARGET_MET...`, SCORECARD lines 5062–5063).
   Real command on the frozen revision: `MADO_FIGURES: ERROR (stage=setup stated text absent from SCORECARD.md ... 'flooding 48/75 vs held 75/75')`, rc 2.
   No verdict is possible until the figure file is re-pinned (the counter forbids editing it to match, so this is an L1 decision).

## Scratch-only adjustments (documented; the frozen bytes were not changed)

- C1 harness: relaxed the copy's `ID_RE` to accept upper-case ids; mapped `app_name`→`app-name`, `modes`→`mode`, dropped null/empty args;
  run "B" additionally rewrote C13 `config` `.config_mako/` → `.config/mako/`. Run "A" = frozen with only the key mapping (C13 left broken).
- C2 harness: fixture clone `git clone --no-hardlinks` of the lane at e4875ba; commit `da0598f` adds the frozen figure bytes (fixture only);
  commit `33efe9c` (variant) trims F2 `stated_at` to `48/75 vs held 75/75`, so the counter can run. The frozen-revision row (`da0598f`) is the unmodified figure file.
- Every fixture commit used a throwaway identity inside the scratch clone only. Nothing was committed in the lane.
- The lane's counter files were never run in place; every counter run used a scratch copy named in the matrix below.

## C1 — mako mutation matrix (`mado-mako.py`)

Method: `c1-r87-mako-criteria.py`'s own `load_cases`, `materialize`, `run_all` (imported from the scratch copy) over the 23 cases.
A mutant is **killed** iff its per-case verdict vector differs from the pristine vector (the counter's own rule, `hit = verdicts != base`).
Harness: `$S/mako/mako_mutate.py` (run A: `TMPDIR=$S/mako python3 -I $S/mako/mako_mutate.py`; run B: same with `TYPO_FIX=1`).
Tool selftest column: `python3 -I <mutant> --selftest --scratch-root DIR`.
Diff column: the single `old → new` replacement (unique match verified, count = 1; full unified diffs were written to the harness matrix in scratch, removed on exit).

| id | mutant (description) | old → new | frozen as-is (run A) | frozen, typo-fixed (run B) | tool selftest | command |
|---|---|---|---|---|---|---|
| R01 | include read only while no criteria section has opened (later includes dropped) | `self.load(target)` → `if not self.sections: self.load(target)` | survived | survived | survived (rc 0) | run A/B harness |
| R02 | include cycle guard removed | `if real in self.stack:` → `if False:` | survived | survived | KILLED (RecursionError, rc 1, no summary) | run A/B harness |
| R03 | non-regular include silently skipped, refusal not recorded | `if not stat.S_ISREG(...):\n refuse(...)\n return` → `if not stat.S_ISREG(...):\n return` | survived | survived | KILLED (`non-regular include target refused`) | run A/B harness |
| R04 | app-name compared case-insensitively | `self.app_name != value` → `self.app_name.lower() != value.lower()` | survived | survived | survived | run A/B harness |
| R05 | app-name matched as a prefix | `self.app_name != value` → `not self.app_name.startswith(value)` | survived | survived | survived | run A/B harness |
| R06 | urgency compared by string `<` instead of equality | `self.urgency != value` → `self.urgency < value` | KILLED (C05, C11) | KILLED (C05, C11, C13) | survived | run A/B harness |
| R07 | mode criteria never compared | `if key == "mode":` → `if key == "mode-unused":` | KILLED (C08) | KILLED (C08) | KILLED (`mode criteria needs enabled mode`) | run A/B harness |
| R08 | criteria applied in reverse order (first match wins) | `for section in state.sections:` → `for section in reversed(...)` | KILLED (C12) | KILLED (C12) | KILLED (`later matching criteria wins`) | run A/B harness |
| R09 | boolean values not validated | `return None if value in ("0","1") else "expects 0 or 1"` → `return None` | survived | survived | survived | run A/B harness |
| R10 | directional values accept 5 parts | `1 <= len(parts) <= 4` → `<= 5` | survived | survived | survived | run A/B harness |
| R11 | anchor enumeration loses `center` | `"center-left", "center"),` → `"center-left"),` | survived | survived | survived | run A/B harness |
| R12 | unknown global key ignored without refusal | `self.refuse(where, "unknown global option ...")` → `pass` | survived | survived | KILLED (`unknown global key refused`) | run A/B harness |
| R13 | `#` comment lines parsed | `if not line or line.startswith("#"):` → `if not line:` | KILLED (C19) | KILLED (C19) | KILLED (`comment and blank lines ignored`) | run A/B harness |
| R14 | section header without `]` accepted | `if not line.endswith("]"):` → `if False:` | survived | survived | survived | run A/B harness |
| R15 | CLI `--mode` replaces the initial mode list | `set(INITIAL_MODES) \| set(args.mode)` → `set(args.mode) or set(INITIAL_MODES)` | survived | survived | survived | run A/B harness |
| R16 | config path abspath instead of realpath | `os.path.realpath(args.config)` → `os.path.abspath(args.config)` | survived | survived | survived | run A/B harness |
| R17 | `summary` criteria field admitted as a match | `if key not in MODELLED_FIELDS:` → `... and key != "summary":` | survived | survived | KILLED (`unmodelled criteria field refused`) | run A/B harness |
| R18 | unreadable config/include refusal dropped | `self.refuse(path, "unreadable config: ...")` → `pass` | survived | survived | survived | run A/B harness |
| R19 | relative include refusal dropped | `self.refuse(where, "include path must be absolute ...")` → `pass` | KILLED (C20) | KILLED (C20) | KILLED (`relative include refused`) | run A/B harness |

Summary: 19 mutants, run A killed 5 (R06, R07, R08, R13, R19), survived 14; run B identical kill set (R06 gains a C13 flip). Tool selftest kills 8 of
these 19 (R02, R03, R07, R08, R12, R13, R17, R19). Survivors of **both** the frozen cases and the tool selftest: R01, R04, R05, R09, R10, R11, R14, R15, R16, R18.

Frozen declared mutants (`mako-mutants-r87.json`, same method, `c1-r87-mako-criteria.py` `evaluate()`):

| id | frozen as-is | typo-fixed | tool selftest (`--selftest`, rc) |
|---|---|---|---|
| M01 criteria-setdefault | killed | killed | killed (rc 1, 6 FAIL) |
| M02 global-ignored | killed | killed | killed (rc 1, 5 FAIL) |
| M03 relative-include-accepted | killed | killed | killed (rc 1) |
| M04 tilde-ignores-home | killed | killed | killed (rc 1) |
| M05 no-initial-mode | **survived** | **survived** | killed (rc 1) |
| M06 no-defaults | **survived** | **survived** | killed (rc 1, crash) |
| M07 app-name-ignored | killed | killed | killed (rc 1) |
| M08 missing-input-matches | **survived** | **survived** | killed (rc 1) |
| M09 urgency-inverted | killed | killed | killed (rc 1) |
| M10 unterminated-quote-accepted | **survived** | **survived** | killed (rc 1) |

Frozen predicate result (`evaluate()`, n=23, m=10): as-is `correct 22, killed 6, naive 6, globals 7, TARGET_MISSED`; typo-fixed `correct 23, killed 6, TARGET_MISSED`.

## C2 — control-fidelity mutation matrix (`c2-r87-control-fidelity.py`)

Method: copy per mutant with exactly one `old → new` replacement (count = 1 verified). Three probes per copy:
selftest `python3 -I <copy> --selftest --scratch-root DIR`; real variant `python3 -I <copy> --repo <fixture> --rev 33efe9c0a7b7e6e6c194b3d88023b818a491475f --figures .ufo/waves/round-87/controls/r86-figures-r87.json --scratch-root DIR`;
real frozen `… --rev da0598f074ce96bc3eb01bfea8f87a5229328eec …`. A probe is **killed** iff its (rc, stdout) differs from pristine; the line `counter_sha256=` is normalised, since it changes for every copy.
Harness: `$S/c2/c2_mutate.py`.

Pristine baselines: selftest `15/15` rc 0. Variant: `TARGET_MISSED`, rc 1, score 5.0 (F1 `rederived=1/1 reproduced=no reconciled=no`, F2 `reproduced=yes`) — this is the declared "before" state. Frozen revision: setup error, rc 2 (see headline 3).

| id | mutant (description) | old → new | selftest | real, variant (rev 33efe9c) | real, frozen (rev da0598f) |
|---|---|---|---|---|---|
| K1 | bare correction heading reconciles | `CORRECTION_HEADING in title and token_in(fig_id, block) and token_in(value, block)` → `CORRECTION_HEADING in title` | KILLED (7/15) | survived | survived (setup error unchanged) |
| K2 | value not checked | `... and token_in(value, block):` → `... and token_in(fig_id, block):` drop value token | KILLED (11/15) | survived | survived |
| K3 | figure-file sha pin not enforced | `if expect_sha is not None and expect_sha.lower() != fsha:` → `if False:` | KILLED (14/15) | survived | survived (the declared command does not pass `--expect-figures-sha256`) |
| K4 | held-rule figure always reproduces | `ok = derived == fig["stated"]` → `... or fig["kind"] == "held_rule_witness"` | KILLED (9/15) | **KILLED** (TARGET_MET, rc 0, 10.0) | survived |
| K5 | flood figure uses the stub | `"flood_pair": flood_fn}` → `"flood_pair": stub_flood}` | KILLED (14/15, via injected flood fn) | survived (stub value equals re-run value at this rev) | survived |
| K6 | correction block runs past same-level headings | `if later_level <= level:` → `if later_level < level:` | KILLED (13/15) | survived | survived |
| K7 | figure id / value matched as bare substrings | `re.search(r"(?<![0-9A-Za-z_])%s(?![0-9A-Za-z_])" ...)` → `re.search(re.escape(token), text)` | KILLED (14/15) | survived | survived |
| K8 | reconciliation never reads correction files | `rec = ok or reconciles(fig["id"], derived, corrections)` → `rec = ok` | KILLED (13/15) | survived | survived |
| K9 | figure kind validation removed | `if fig["kind"] not in KINDS:` → `if False:` | **survived** (15/15) | survived | survived |
| K10 | setup errors exit 1 (verdict) instead of 2 | `print(... stage=setup ...)\n return 2` → `... return 1` (in `main`) | **survived** (15/15) | survived | KILLED (rc 2 → 1) |

Summary: 10 mutants; selftest kills 8 (K1–K8); real command at the variant kills 1 (K4); real command at the frozen revision kills 1 (K10).
K9 survives everything.

Command template for every row: `cd $S/c2 && TMPDIR=$S/c2/tmp python3 -I <copy> <args above>`; the fixture clone and both scratch runs are under `$S/c2/` and removed on exit.

## Defects (survivors and blockers), with severity

| id | claim | defect | evidence | severity |
|---|---|---|---|---|
| D1 | C1 | Frozen `mako-cases-r87.json` violates the counter loader: upper-case ids (`ID_RE`), `app_name`/`modes` arg keys (expects `app-name`/`mode`). Counter exits 2 before any verdict. | `load_cases` SetupError, verbatim above | **blocker** |
| D2 | C1 | Case C13 `config` is `.config_mako/config`; no tool can pass it. | `pristine correct=22`, C13 `FAIL exit=2`; typo-fixed copy `23/23` | **blocker** |
| D3 | C1 | With D1/D2 fixed, the frozen cases kill 6/10 declared mutants (M05, M06, M08, M10 survive). The declared predicate (all M killed) cannot be met on these cases. The tool's own selftest kills all 10. | `evaluate()` run; tool selftest table | **blocker** (C1 cannot be TARGET_MET as frozen) |
| D4 | C1 | 14 of 19 added mutants survive the frozen cases: R01, R02, R03, R04, R05, R09, R10, R11, R12, R14, R15, R16, R17, R18 (killed: R06, R07, R08, R13, R19). Holes: no app-name casefold or prefix case; no include cycle case; no non-regular include case; no include after a section; no CLI `--mode` alongside `[mode=default]`; no invalid boolean; no 5-part directional; no `anchor` expectation at all; no unclosed header; no unknown global key; no unreadable file; no symlinked config (the symlink form in `home_files` is unused by any case). | matrix above | **high** |
| D5 | C1 | R17 survives because C22 (`[summary=hello summary~=hello]`) is refused by the `summary~` conflict anyway; the single-field `summary` admission path is untested. | R17 flips nothing; tool selftest kills it | medium |
| D6 | C1 | R16 (abspath for realpath) cannot be distinguished: no symlinked config case, though `~/.config/mako/config` is a symlink on this host (declaration surface). Equivalence not proven, just uncovered. | matrix | medium |
| D7 | C2 | Frozen F2 `stated_at.text` (`flooding 48/75 vs held 75/75`) is line-wrapped in SCORECARD.md (lines 5062–5063). The counter returns setup error (rc 2) on the lane's revision: C2 cannot produce a verdict on these figures. The counter forbids editing the figure file to match, so this needs an L1 decision (re-pin the figure file with a non-wrapped stated text, or change the scorecard line). | `pristine-real.out` at da0598f; `sed -n '5062,5063p'` | **blocker** (C2) |
| D8 | C2 | The declared counting command does not pass `--expect-figures-sha256`, so the sha pin declared in the frozen claim is not enforced by the command (K3 is invisible to the real run). | K3 real rows identical | medium |
| D9 | C2 | Selftest never exercises `main()`'s exit map: K10 (setup error exit 1 instead of 2) survives the selftest and is only caught by the real frozen run; K9 (unknown kind) survives every probe, and would fall to an uncaught `KeyError` (rc 1) rather than the setup exit. | K9/K10 rows | medium |
| D10 | C2 | `derive_flood` is not exercised by the selftest (it is stubbed); the real F2 re-derivation reproduces the stub's value at 3afdb713, so K5 is indistinguishable in real output at this revision. F2 is effectively unverified by any fixture. | K5 rows; selftest attempt() injects flood fn | low |

## Verification performed (with exit codes)

- Pristine tool selftest: `python3 -I pristine/mado-mako.py --selftest --scratch-root …` → `checks=29 failed=0`, rc 0.
- Pristine C2 selftest: rc 0, `15/15`.
- Pristine C2 real variant: rc 1 (`TARGET_MISSED`, 5.0); real frozen: rc 2 (setup, F2 wrap).
- Frozen-case run A: `N=23 pristine correct=22`; run B: `N=23 pristine correct=23`.
- Frozen predicate (`evaluate()`): as-is `correct 22, killed 6/10, TARGET_MISSED`; typo-fixed `correct 23, killed 6/10, TARGET_MISSED`.
- All mutants: count of `old` in pristine text = 1 except R03 (initial anchor was non-unique, 2 hits; re-anchored to a multi-line unique old and rerun).

## Installs

None. No tool was installed or upgraded by this seat. No pacman transaction, no `~/.local/bin` write.

## Notes for the planner (L1)

- Items D1, D2, D3, D7 each block a counter from producing a verdict or a TARGET_MET on the frozen inputs; they need a frozen-input decision, not a tool change.
- The killing of M05/M06/M08/M10 by the tool's selftest but not by the frozen cases means the case set, not the tool, is the weak point for C1.
- Mutant files and both matrices lived in scratch and were removed on exit; the diff and kill status are recorded above.

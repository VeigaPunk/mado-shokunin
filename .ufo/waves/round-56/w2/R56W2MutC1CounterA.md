# R56W2MutC1CounterA — mutation test of the C1 counter (falsification, wave 2)

Attacked item: `quality/counters/c1-r56-autoreload-entry.py` at `28fc86ac2359ec27406d8a2c63bef82ea6e947ed` (pristine md5 `6d13eec7…`). Legs attacked: row grammar, quote, host, source_cell, scope, tok, num, echo, prov, index, new_rows, pin_hash, tables_sha. Attack premise: wave-1 seats wrote each artifact once and their own selftests were the only kill evidence.

Verdict: the lane's own oracles (selftest 242/242, frozen harness 12/12) kill 39 of 67 one-line mutants (58.2 %; 65.0 % of the 60 non-equivalent-or-witnessed). Of the 28 survivors, 5 are fully equivalent, 2 are verdict-equivalent on sha-verified inputs, and 21 are non-equivalent. Each of the 21 is killed by one proposed single-edit fixture (F01–F20), and each fixture's pristine expectation holds. Two real weaknesses turned up (DEF-1, DEF-2), both latent in the current content.

## What I did

1. Scratch: `/fast/scratch/hyaku/mado-r56/R56W2MutC1CounterA/`. `git archive 28fc86ac…` into `base/`, a fresh `git init`, toplevel asserted equal to `base/`, commit `3be5bb0f` (tree `d83d2ebe…`, identical to the lane tree). Lane: read-only (`git show`, `git archive`), no lane writes.
2. Baseline on the scratch copy (rc 0 each):
   - `python3 -I <base>/quality/counters/c1-r56-autoreload-entry.py --selftest --repo <base> --rev 3be5bb0f --work W` → `242/242 assertions passed`
   - `python3 -I <base>/quality/check-r56-controls.py --claim c1 --repo <base> --rev 3be5bb0f --work W` → `MADO_R56_CONTROLS: claim=c1 good=ok controls=12/12 verdict=OK`
   - counter → `rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none`
3. `mutate.py`: 67 one-line mutants of the production region (lines ≤ 636), each COPY compiled, then run against both unchanged oracles: (A) `--selftest`, (B) `check-r56-controls.py --claim c1 --counter <mutant>`. Result: `TOTAL 67 KILLED 39 SURVIVED 28 INCONCLUSIVE 0` (two INCONCLUSIVE from my own bad spec strings were corrected and re-run; final run has 0). Kill attribution: selftest 38, harness 26, both 25, selftest-only 13, harness-only 1 (M59).
4. Equivalence: argued for each of the 28 survivors; the five fully-equivalent ones also got a randomized differential: `equiv_fuzz.py --trials 300 --seed 56` → `M02 divergences=0`, `M11 divergences=0`, `M46 divergences=0`, `M60 divergences=0`, `M61 divergences=0`.
5. Killers: `killers.py` builds 22 minimal fixture repos (one edit each), runs the pristine and the mutant on each, and records the verdict. Result: pristine expectation held 22/22; each named mutant killed 22/22 (F05 kills M13 and M14 together). Output sample:
   - F13 (`K04` proposition += ` The cap is 200ms.`): pristine `rc 0 … verdict=TARGET_MET missed=none`; M39 `rc 1 … missed=num:K04`.
   - F05 (`K01` quote cell unbackticked): pristine `missed=row:K01,quote:K01`; M13 and M14 `missed=row:K01`.
   - F20 (a `` `` `` line before K01): pristine `rc 0 … TARGET_MET`; M65 `rc 1 … rows=0/30 … missed=row:K01,…,row:K08,…`.

## Survivors, classified

- Fully EQUIVALENT (5): M02 (`< 4`→`< 3`; candidate lines are ≥7 bytes), M11 (`len(cand)==1` is implied by `strict is not None`), M46 (`source:` and `verified-at:` lines are never the same line), M60 (`e` ≤ 33, so `==33` ≡ `>=33`), M61 (`a` ≤ 30).
- VERDICT-EQUIVALENT on sha-verified inputs (2): M16 (`n > len(pl)+1` only matters when a row line is past its pin's split length; no frozen row is; `tables_sha` fixes the rows), M53 (`new_row_ids` has 8 frozen entries). Both diverge only on a sha-broken table; witnesses F21 (IndexError crash, no stdout) and F22 (`new_rows` leg dropped) show it.
- NON-EQUIVALENT (21), each killed by a fixture: M05→F01, M07→F02, M09→F03, M12→F04, M13/M14→F05, M18→F06, M21→F07, M26→F08, M28→F09, M34→F10, M37→F11, M38→F12, M39→F13, M43→F14, M44→F15, M45→F16, M49→F17, M50→F18, M57→F19, M65→F20.

Full table with mutated lines: `.ufo/waves/round-56/w2/R56W2MutC1CounterA/mutants.md` §2; fixture table: §5.

## Defects (input → output → severity)

- **DEF-1 — weakens claim (num leg, latent).** Input: K04 proposition `The cap is 200ms.` (F13) → counter `rc 0 … verdict=TARGET_MET missed=none`. The registered digit-run regex `(?![A-Za-z0-9_])` excludes numerals followed by letters, so a unit-suffixed number is never tested. Latent at 28fc86ac: none of the 33 propositions contains any digit (`grep`/regex count: 0). Severity: weakens claim.
- **DEF-2 — weakens claim (provenance ids, latent).** Input: `source:` line += ` S38` (F17) → `rc 0 … TARGET_MET`. The `S###` token shape (exactly 3 digits) is also the C3 `CITE`/`SRC` shape, so a 2- or 4-digit typo in a source line is invisible to C1 and C3. Latent: the source line holds exactly `S383`..`S391`. Severity: weakens claim.
- **DEF-3 — test gap (21 non-equivalent survivors).** Selftest and frozen controls never exercise the 21 branches listed above (a `|` inside a cell, leading-space propositions, non-ASCII digits in source ids, duplicated-row collateral legs, bare quote cells, wrong revision-token URLs, reversed locators past EOF, over-locators beside in-range ones, 4-char identifiers, H-row own-line numbers, cross-pin integers, numerals with letters, the 30-character echo boundary, the 15-line provenance window, a second `verified-at`, non-`S###` source tokens, mid-line README matches, host pin bytes, two-backtick fences). Severity: test gap.
- **DEF-4 — test gap in frozen control 12 (anchor-past-eof).** The single over-locator `ConfigWatcher.cpp:1-9999` cannot separate the `over` veto from `covered`, because the `elif` already withholds coverage on an over-locator. Only an over-locator beside an in-range one (F09, M28) exposes the veto. Selftest `reg-scope-past-eof` has the same single-locator shape. Severity: weakens the test, not the claim.

No defect in the pristine counter was found by a verdict-changing input beyond DEF-1 and DEF-2, and both are latent in the current content.

## Deliverables (absolute paths)

- Mutants and classification: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w2/R56W2MutC1CounterA/mutants.md`
- Drivers: `…/R56W2MutC1CounterA/mutate.py` (67 mutants, both oracles), `…/killers.py` (22 fixtures), `…/equiv_fuzz.py` (300-trial differential)
- Receipts: `…/R56W2MutC1CounterA/receipts/` — `baseline.txt`, `harness-baseline-stderr.txt`, `pristine-c1-counter.py` + `.md5`, `mut-results-67.json` (both oracles' rc and output tails per mutant), `killers-results.json` (pristine and mutant output per fixture), `equiv-fuzz-300.json`

## Tooling

No tool installed, upgraded or removed. The `python3` is the system `python3 -I` (3.14.8); `git` 2.56.0. Passwordless sudo and pacman were not used.

## Not verified / limits

- The five EQUIV classifications are argued and backed by a 300-trial random differential per mutant; not exhaustive proof.
- M16 and M53 are verdict-equivalent only on sha-verified inputs; the output difference is shown on a sha-broken table, which the frozen `tables_sha` leg already fails.
- The 22 killer fixtures are differentials against the pristine counter, not a new harness control; the frozen harness was not edited and nothing was run through a modified harness. Their pristine expectations rest on my reading of `registration.md` §C1 and `registration-v2.md` E2–E5, not on an independent review.
- The random differential perturbs the entry, registry and README only; tables and pins are sha-bound and were not perturbed there.
- Not checked: whether any sentence of the entry is entailed by its pin line (out of scope for a mutation test; the declared limit of C1).
- Scratch `/fast/scratch/hyaku/mado-r56/R56W2MutC1CounterA/` was removed after the receipts were copied. Lane observation, not caused by this seat: `git status` at the end shows `corpus/README.md` modified (2 insertions, 2 deletions) in the lane working tree; every write this seat made targets scratch or its own deliverable directory, and the lane was read through git objects only.

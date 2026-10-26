# C1 mutation population — survivors (seed ExecC1ExtraMutants, round 44 w1)

Reference: `.ufo/waves/round-44/c1/ctl-ref-tool.py.txt` (476 lines). Counter: `quality/counters/c1-r44-geometry-states.py` at rev `e2289516a9a857f55cda7be635933e89b931c3da`. Scored, one run per body:

    cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r44-geometry-states.py --repo . --rev e2289516a9a857f55cda7be635933e89b931c3da --tool .ufo/waves/round-44/w1/ExecC1ExtraMutants/mutants/<M>.py --nonce mutsweep1 --work /fast/scratch/hyaku/mado-r44/ExecC1ExtraMutants/work/<M>

(`--work` is the transient seat scratch, re-created by `mkdir -p`; no result is cited from it.)

`--nonce mutsweep1` is fixed so every body is judged on the same 12-case sgen lattice; the survivors were re-scored on nonce `mutsweep2` with the same result. `REF` under the same nonce: `fixtures=26/26 clauses=a:1 b:1 b4:1 g:1 r:1 verdict=TARGET_MET`.

Population: 51 single-defect mutants, every replacement asserted to match exactly once at build time (`build.py`, `BUILD total=51 bad=0`). **20 survive the whole counter, 31 are killed.** No surviving mutant is behaviourally wrong: all 20 are equivalent transformations (code proof below plus 20 000 randomised differential cases each, `receipts/equivalence-diff.txt`).

## 1. Survivors

| mutant | edit | verdict | failing fixtures/clauses | classification and proof |
|---|---|---|---|---|
| `M04-fsmode-admit-0` | membership admits 0 | TARGET_MET, fixtures 26/26, clauses a:1 b:1 b4:1 g:1 r:1 | none | EQUIVALENT — returns 0 for `fullscreen`: 0 (the same value the else-branch gives); the returned mode is consumed only by `fsmode == 2` / `fsmode == 1` (ref:233, ref:235), so the output is identical for every input. Contract-conforming. |
| `M05-fsmode-admit-neg` | membership admits -1 | TARGET_MET, fixtures 26/26, clauses a:1 b:1 b4:1 g:1 r:1 | none | MISSING CHECK (contract) + EQUIVALENT (output) — returns -1 for `fullscreen`: -1; `-1 == 2` and `-1 == 1` are both false, so every verdict, tally, suffix and exit code is identical to 0. Output-equivalent but CONTRACT-VIOLATING: see section 3 (the counter does not pin the documented `else 0` on negative ints). |
| `M06-fsmode-range-chain` | membership as chained compare 1 <= f <= 2 | TARGET_MET, fixtures 26/26, clauses a:1 b:1 b4:1 g:1 r:1 | none | EQUIVALENT, and b4-invisible — `1 <= f <= 2` is true exactly for f in {1, 2} (the int guard runs first), and the same f is returned, so the value is unchanged. Side effect measured: the state test stops being an ast.Compare of one operator, so clause b4 stops counting it (14 -> 13 sites, section 4). |
| `M07-fsmode-set-literal` | membership as set literal (unhashable values raise) | TARGET_MET, fixtures 26/26, clauses a:1 b:1 b4:1 g:1 r:1 | none | EQUIVALENT — `{1, 2}` is only evaluated when `isinstance(f, int)` already holds (short-circuit `and`), and ints are hashable, so no unhashable JSON value reaches the set; membership in {1,2} equals membership in (1,2). |
| `M09-guard-int-or-bool` | int guard widened to (int, bool) | TARGET_MET, fixtures 26/26, clauses a:1 b:1 b4:1 g:1 r:1 | none | EQUIVALENT — `isinstance(f, (int, bool))` widens nothing: the following `not isinstance(f, bool)` still removes the only extra member. json.loads yields exactly int/float/str/bool/None/list/dict, never a user int subclass. |
| `M10-guard-type-is` | isinstance int guard -> type(f) is int | TARGET_MET, fixtures 26/26, clauses a:1 b:1 b4:1 g:1 r:1 | none | EQUIVALENT — `type(f) is int` vs `isinstance(f, int)` differ only for int subclasses, which json.loads cannot produce. The counter's own model already uses this form (quality/counters/c1-r44-geometry-states.py:90), i.e. the predicate's author treats them as the same read. |
| `M11-guard-type-not-bool` | bool guard as type(f) is not bool | TARGET_MET, fixtures 26/26, clauses a:1 b:1 b4:1 g:1 r:1 | none | EQUIVALENT — `type(f) is not bool` vs `not isinstance(f, bool)`: bool cannot be subclassed, and its only instances are True and False, so the two guards accept the same set. |
| `M12-guard-is-not-true` | bool guard as f is not True and f is not False | TARGET_MET, fixtures 26/26, clauses a:1 b:1 b4:1 g:1 r:1 | none | EQUIVALENT — `f is not True and f is not False` is the identity test for the two bool singletons, so it accepts the same set as `not isinstance(f, bool)`. |
| `M16-conjunct-reorder` | conjuncts reordered (membership first) | TARGET_MET, fixtures 26/26, clauses a:1 b:1 b4:1 g:1 r:1 | none | EQUIVALENT — the three conjuncts are pure; reordering makes the membership test run first, and tuple membership uses `==` only (no hashing), so unhashable JSON values ([2], {...}) are still compared without error. Same accept set, same return value. |
| `M17-membership-str` | membership by str(f) in ('1','2') | TARGET_MET, fixtures 26/26, clauses a:1 b:1 b4:1 g:1 r:1 | none | EQUIVALENT — `str(f) in ("1", "2")` holds exactly for the ints 1 and 2: decimal str is injective on ints and "1"/"2" are their canonical forms (no sign, no padding). The returned value is still the int f. |
| `M19-return-ternary` | returns 2 if f == 2 else 1 | TARGET_MET, fixtures 26/26, clauses a:1 b:1 b4:1 g:1 r:1 | none | EQUIVALENT — `2 if f == 2 else 1` equals f for the only reachable values f in {1, 2}. |
| `M20-return-min` | returns min(f, 2) | TARGET_MET, fixtures 26/26, clauses a:1 b:1 b4:1 g:1 r:1 | none | EQUIVALENT — `min(f, 2)` equals f for f in {1, 2} (the guard admits nothing larger). |
| `M21-return-mod` | returns f % 3 | TARGET_MET, fixtures 26/26, clauses a:1 b:1 b4:1 g:1 r:1 | none | EQUIVALENT — `f % 3` equals f for f in {1, 2}. |
| `M24-key-default` | c.get('fullscreen', 0) default | TARGET_MET, fixtures 26/26, clauses a:1 b:1 b4:1 g:1 r:1 | none | EQUIVALENT — `c.get("fullscreen", 0)` differs from `c.get("fullscreen")` only when the key is absent, and the guard rejects None exactly as it rejects 0. |
| `M27-branch-swap` | MAXIMIZED tested before FULLSCREEN | TARGET_MET, fixtures 26/26, clauses a:1 b:1 b4:1 g:1 r:1 | none | EQUIVALENT — fsmode is a single integer from client_fsmode, so `fsmode == 1` and `fsmode == 2` are disjoint; testing MAXIMIZED first cannot change any client's verdict. |
| `M28-max-truthiness` | MAXIMIZED tested as `elif fsmode:` | TARGET_MET, fixtures 26/26, clauses a:1 b:1 b4:1 g:1 r:1 | none | EQUIVALENT, and b4-invisible — the MAXIMIZED branch is reached only after `fsmode == 2` failed, so fsmode is 0 or 1 there; `elif fsmode:` is then identical to `elif fsmode == 1:`. Side effect measured: truthiness is not an ast.Compare, so clause b4 stops counting this site (14 -> 13, section 4). |
| `M29-fs-gt1` | FULLSCREEN tested as fsmode > 1 | TARGET_MET, fixtures 26/26, clauses a:1 b:1 b4:1 g:1 r:1 | none | EQUIVALENT — client_fsmode returns only 0, 1 or 2, so `fsmode > 1` and `fsmode == 2` agree everywhere. |
| `M30-max-ge1` | MAXIMIZED tested as fsmode >= 1 | TARGET_MET, fixtures 26/26, clauses a:1 b:1 b4:1 g:1 r:1 | none | EQUIVALENT — the MAXIMIZED branch runs after `fsmode == 2` failed, so fsmode is 0 or 1 there and `fsmode >= 1` equals `fsmode == 1`. |
| `M34-tiled-only-flat` | TILED only when fsmode == 0 | TARGET_MET, fixtures 26/26, clauses a:1 b:1 b4:1 g:1 r:1 | none | EQUIVALENT — the TILED branch runs after both state branches failed, so fsmode is 0 there and `not floating and fsmode == 0` equals `not floating`. |
| `M42-suffix-ge1` | suffix condition >= 1 | TARGET_MET, fixtures 26/26, clauses a:1 b:1 b4:1 g:1 r:1 | none | EQUIVALENT — `maximized + fullscreen >= 1` on two tallies that are non-negative ints, so it is the same predicate as `> 0`. |

Differential evidence: `receipts/equivalence-diff.txt` — 20 000 random client dumps per body against the reference, `DIFF TOTAL=0`; the generator draws `fullscreen` from {1, 2, 0, 3, -1, -7, 100, true, false, 2.0, "2", null, [], [2], {"internal": 2}} and still reaches 97-148 `FULLSCREEN` verdicts, 114-152 `MAXIMIZED` verdicts and 223-278 state suffixes per body, so the state paths are exercised, not bypassed.

## 2. What the survivors say about the predicate

* The state logic is pinned only up to *observable* behaviour: the verdict chain consumes `fsmode` exclusively through `== 2` and `== 1` (ref:233, ref:235), so any return value that matches neither is indistinguishable from 0. That is why M04, M05 and M27 can move the membership set and the branch order without a single fixture moving.
* The 13 registered controls all miss, and K13 misses only on the selftest clause (registration: fixtures 26/26) — the same asymmetry this sweep measures from the other side. Of these 51 extra mutants the equivalence class is wide: 20/51 survive, and every one of them survives because the contract's *observable* surface is thinner than its docstring.

## 3. MISSING CHECK (the one hole the fixtures cannot close)

`M05-fsmode-admit-neg` (and, on the same input, `M51-return-any-int`) returns a negative integer where the contract says 0:

| body | `client_fsmode({"fullscreen": -1})` | contract |
|---|---|---|
| reference | 0 | 0 |
| `M05-fsmode-admit-neg` | -1 | 0 |
| `M51-return-any-int` | -1 | 0 |

(measured, `receipts/fsmode-probe.txt`). The counter's only direct pin on the return value is the selftest case at ref:458 —

    chk("fsmode-values", [client_fsmode({"fullscreen": v}) for v in (1, 2, 0, 3, True, 2.0, "1", None)], [1, 2, 0, 0, 0, 0, 0, 0])

— which covers the upper boundary (3) and every type guard, and no negative integer. No fixture can kill M05: -1 and 0 produce byte-identical output in every case (`receipts/equivalence-diff.txt`), so the only kill path is a value-level check.

**Killing input and expected output** (one added tuple element, nothing else): `client_fsmode({"fullscreen": -1})` must be `0`. Adding `-1` to the ref:458 tuple with expected `0` kills M05 and M51 and leaves the reference passing (the probe table gives both sides of that assertion: reference 0, mutants -1).

Severity: low and unreachable in production — `hyprctl clients -j` prints the internal mode (`eFullscreenMode` 0/1/2, registration `fetch-c1/Hyprland-HyprCtl.cpp`), so a live dump cannot carry -1. The gap is in *contract pinning*, not in behaviour: today a tool can violate the docstring's `else 0` for negative ints and still score `TARGET_MET`.

## 4. Clause b4 can be shrunk by the tool under test (measured)

b4 counts the `ast.Compare` nodes of one operator (counter:283) in functions whose body contains a `fullscreen` string, and needs `ceil(0.75 * sites)`, floor 6 (counter:76-77, counter:294). Two of the survivors remove exactly that state site from the census without removing the state logic:

| body | membership test written as | b4 sites | b4 killed | need | clause b4 |
|---|---|---|---|---|---|
| reference | `f in (1, 2)` (ref:197) | 14 | 14 | 11 | pass |
| `M06-fsmode-range-chain` | `1 <= f <= 2` (two operators) | 13 | 13 | 10 | pass |
| `M28-max-truthiness` | `elif fsmode:` (no Compare at all) | 13 | 13 | 10 | pass |
| `M12-guard-is-not-true` | `f is not True and f is not False` (adds two) | 16 | 16 | 12 | pass |

So the census is not a constant of the contract: `1 <= f <= 2` and truthiness are invisible to `len(node.ops) == 1`, and the remaining 13 sites are round-43 compares (`evaluate:213..239`, `report:259..269`) whose flips break the selftest for reasons unrelated to state. The floor and the 75 % rule still hold here, but the *marginal* tooth on the state branch is one site, and a tool can drop it by writing a chained compare. This is a clause-strength residual, not a false kill.

## 5. Kill channels (all 31 misses)

| channel | kills | note |
|---|---|---|
| fixtures only (selftest passes) | 1 | `M46-unmapped-fs-counted`, 23/26 |
| selftest only (fixtures 26/26) | 3 | `M01-fsmode-extra-3`, `M22-fallback-none`, `M51-return-any-int` |
| fixtures and selftest | 27 | |
| clause r (round-43 counter) independent | 0 | r:0 exactly when b:0 — the round-42 counter runs the same `--selftest`, so it never adds a kill of its own |
| clause b4 independent | 0 | b4 is skipped whenever b fails (counter:356-357), so it cannot kill what the selftest does not |

The three selftest-only kills are the interesting half: the 26 fixtures are blind to `fsmode` values that no verdict branch consumes (3, None), and only the value-level selftest case at ref:458 sees them. Conversely `M46` shows the fixtures carry the counting reach that the selftest does not.

## 6. Full kill table

| mutant | edit | result | failing fixtures/clauses |
|---|---|---|---|
| `M01-fsmode-extra-3` | membership admits 3 (boundary: extra value) | TARGET_MISSED | fixtures 26/26; selftest 90/91; a:1 b:0 b4:0 g:1 r:0 |
| `M02-fsmode-drop-2` | membership drops fullscreen 2 | TARGET_MISSED | fixtures 17/26 (sgen1, sgen7, sgen10, fs0, fsagree0, fsmix0, fsstdin0, fsdup0, fsmany0); selftest 85/91; a:1 b:0 b4:0 g:1 r:0 |
| `M03-fsmode-only-2` | membership keeps only 2 (drops maximized 1) | TARGET_MISSED | fixtures 21/26 (max0, maxfloat0, fsmix0, fsstdin0, fsmany0); selftest 89/91; a:1 b:0 b4:0 g:1 r:0 |
| `M08-drop-int-guard` | int guard dropped (floats 2.0 admitted) | TARGET_MISSED | fixtures 23/26 (sgen6, fsvals0, fsmany0); selftest 89/91; a:1 b:0 b4:0 g:1 r:0 |
| `M13-guard-float-reject` | bool guard replaced by not isinstance(f, float) (bools pass) | TARGET_MISSED | fixtures 24/26 (fsvals0, fsmany0); selftest 89/91; a:1 b:0 b4:0 g:1 r:0 |
| `M14-guard-float-only` | int guard replaced by float guard | TARGET_MISSED | fixtures 13/26 (sgen1, sgen6, sgen7, sgen10, fs0, fsagree0, max0, maxfloat0, fsvals0, fsmix0, fsstdin0, fsdup0, fsmany0); selftest 83/91; a:1 b:0 b4:0 g:1 r:0 |
| `M15-guard-float-admit` | int guard widened to (int, float), return unchanged | TARGET_MISSED | fixtures 23/26 (sgen6, fsvals0, fsmany0); selftest 89/91; a:1 b:0 b4:0 g:1 r:0 |
| `M18-return-bool` | returns bool(f) | TARGET_MISSED | fixtures 17/26 (sgen1, sgen7, sgen10, fs0, fsagree0, fsmix0, fsstdin0, fsdup0, fsmany0); selftest 86/91; a:1 b:0 b4:0 g:1 r:0 |
| `M22-fallback-none` | else-branch returns None instead of 0 | TARGET_MISSED | fixtures 26/26; selftest 89/91; a:1 b:0 b4:0 g:1 r:0 |
| `M23-return-invert` | returns 2 - f | TARGET_MISSED | fixtures 17/26 (sgen1, sgen7, sgen10, fs0, fsagree0, fsmix0, fsstdin0, fsdup0, fsmany0); selftest 85/91; a:1 b:0 b4:0 g:1 r:0 |
| `M25-key-case` | reads 'Fullscreen' (absent key) | TARGET_MISSED | fixtures 15/26 (sgen1, sgen7, sgen10, fs0, fsagree0, max0, maxfloat0, fsmix0, fsstdin0, fsdup0, fsmany0); selftest 84/91; a:1 b:0 b4:0 g:1 r:0 |
| `M26-key-floating-gate` | state read only for floating clients | TARGET_MISSED | fixtures 22/26 (sgen1, sgen10, max0, fsmany0); selftest 89/91; a:1 b:0 b4:0 g:1 r:0 |
| `M31-max-and-floating` | MAXIMIZED requires floating (states only for floating) | TARGET_MISSED | fixtures 24/26 (max0, fsmany0); selftest 90/91; a:1 b:0 b4:0 g:1 r:0 |
| `M32-fs-ne0` | FULLSCREEN tested as fsmode != 0 | TARGET_MISSED | fixtures 21/26 (max0, maxfloat0, fsmix0, fsstdin0, fsmany0); selftest 90/91; a:1 b:0 b4:0 g:1 r:0 |
| `M33-badsize-only-flat` | BADSIZE only when fsmode == 0 | TARGET_MISSED | fixtures 25/26 (fsbad0); selftest 90/91; a:1 b:0 b4:0 g:1 r:0 |
| `M35-badsize-last` | BADSIZE tested after the two state branches | TARGET_MISSED | fixtures 25/26 (fsbad0); selftest 90/91; a:1 b:0 b4:0 g:1 r:0 |
| `M36-max-counted-tiled` | MAXIMIZED counted in the tiled tally | TARGET_MISSED | fixtures 21/26 (max0, maxfloat0, fsmix0, fsstdin0, fsmany0); selftest 90/91; a:1 b:0 b4:0 g:1 r:0 |
| `M37-max-counted-fullscreen` | MAXIMIZED counted in the fullscreen tally | TARGET_MISSED | fixtures 21/26 (max0, maxfloat0, fsmix0, fsstdin0, fsmany0); selftest 90/91; a:1 b:0 b4:0 g:1 r:0 |
| `M38-fs-counted-maximized` | FULLSCREEN counted in the maximized tally | TARGET_MISSED | fixtures 17/26 (sgen1, sgen7, sgen10, fs0, fsagree0, fsmix0, fsstdin0, fsdup0, fsmany0); selftest 88/91; a:1 b:0 b4:0 g:1 r:0 |
| `M39-states-values-swapped` | suffix values swapped, labels kept | TARGET_MISSED | fixtures 17/26 (sgen1, sgen7, sgen10, fs0, fsagree0, max0, maxfloat0, fsdup0, fsmany0); selftest 87/91; a:1 b:0 b4:0 g:1 r:0 |
| `M40-states-no-space` | suffix leading space dropped | TARGET_MISSED | fixtures 15/26 (sgen1, sgen7, sgen10, fs0, fsagree0, max0, maxfloat0, fsmix0, fsstdin0, fsdup0, fsmany0); selftest 88/91; a:1 b:0 b4:0 g:1 r:0 |
| `M41-states-double-space` | suffix leading double space | TARGET_MISSED | fixtures 15/26 (sgen1, sgen7, sgen10, fs0, fsagree0, max0, maxfloat0, fsmix0, fsstdin0, fsdup0, fsmany0); selftest 89/91; a:1 b:0 b4:0 g:1 r:0 |
| `M43-suffix-gt-neg1` | suffix condition > -1 | TARGET_MISSED | fixtures 10/26 (sgen0, sgen2, sgen3, sgen4, sgen5, sgen6, sgen8, sgen9, sgen11, fsbad0, fsvals0, fsunmatched0, fsunmapped0, fsdup0, fsclient0, fsnorules0); selftest 78/91; a:1 b:0 b4:0 g:1 r:0 |
| `M44-states-after-verdict` | suffix printed after verdict= | TARGET_MISSED | fixtures 15/26 (sgen1, sgen7, sgen10, fs0, fsagree0, max0, maxfloat0, fsmix0, fsstdin0, fsdup0, fsmany0); selftest 88/91; a:1 b:0 b4:0 g:1 r:0 |
| `M45-states-before-tiled` | suffix printed before tiled= | TARGET_MISSED | fixtures 15/26 (sgen1, sgen7, sgen10, fs0, fsagree0, max0, maxfloat0, fsmix0, fsstdin0, fsdup0, fsmany0); selftest 89/91; a:1 b:0 b4:0 g:1 r:0 |
| `M46-unmapped-fs-counted` | fullscreen counted for unmapped clients | TARGET_MISSED | fixtures 23/26 (sgen1, sgen4, fsunmapped0); selftest 91/91; a:1 b:1 b4:1 g:1 r:1 |
| `M47-unmatched-fs-counted` | fullscreen counted for unmatched clients | TARGET_MISSED | fixtures 14/26 (sgen0, sgen1, sgen4, sgen5, sgen6, sgen7, sgen8, sgen9, sgen10, sgen11, fsunmatched0, fsnorules0); selftest 90/91; a:1 b:0 b4:0 g:1 r:0 |
| `M48-matched-unmatched` | unmatched clients counted as matched | TARGET_MISSED | fixtures 13/26 (sgen0, sgen1, sgen3, sgen4, sgen5, sgen6, sgen7, sgen8, sgen9, sgen10, sgen11, fsunmatched0, fsnorules0); selftest 85/91; a:1 b:0 b4:0 g:1 r:0 |
| `M49-differ-or-maximized` | maximized only dump exits 1 (DIFFER) | TARGET_MISSED | fixtures 23/26 (max0, maxfloat0, fsstdin0); selftest 90/91; a:1 b:0 b4:0 g:1 r:0 |
| `M50-top-verdict-maximized` | state clients change the top verdict word | TARGET_MISSED | fixtures 18/26 (sgen1, sgen7, fs0, fsagree0, max0, maxfloat0, fsstdin0, fsdup0); selftest 90/91; a:1 b:0 b4:0 g:1 r:0 |
| `M51-return-any-int` | membership test dropped, any JSON int returned raw | TARGET_MISSED | fixtures 26/26; selftest 90/91; a:1 b:0 b4:0 g:1 r:0 |

## 7. Reproduction

    python3 -I .ufo/waves/round-44/w1/ExecC1ExtraMutants/build.py      # rebuild the 51 bodies
    bash .ufo/waves/round-44/w1/ExecC1ExtraMutants/run_sweep.sh REF M01-fsmode-extra-3 ...
    python3 -I .ufo/waves/round-44/w1/ExecC1ExtraMutants/summarize.py
    python3 -I .ufo/waves/round-44/w1/ExecC1ExtraMutants/probe_fsmode.py
    python3 -I .ufo/waves/round-44/w1/ExecC1ExtraMutants/equivalence_diff.py 20000

Bodies: `.ufo/waves/round-44/w1/ExecC1ExtraMutants/mutants/` (51 files + `build.py` spec).

# MutRefSelftest matrix — round 44 w1

Target: frozen reference `.ufo/waves/round-44/c1/ctl-ref-tool.py.txt`, function `client_fsmode` (lines 195-200). Every mutant is a single edit applied to a separate copy of the pristine bytes inside the `client_fsmode` slice only (each `old` string verified to occur exactly once in that slice; pristine file never modified).

Detectors:
- D-selftest: `python3 -I <file> --selftest` — killed iff rc != 0 or tail != `MADO_GEOMETRY_SELFTEST: 91/91 passed`.
- D-counter (selftest survivors only): `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r44-geometry-states.py --repo . --rev e2289516a9a857f55cda7be635933e89b931c3da --tool <mutant> --work /fast/scratch/hyaku/mado-r44/MutRefSelftest`.

Pristine: sha256 `8e871a00fcf1a615e3683ebe5204f67cfe679182ff15d008b83fed34131c788d`; selftest `91/91 passed` rc 0 before and after all mutations (restoration evidence below). Mutant sha256 prefixes below; full hashes in `evidence/selftest.json`.

## Result summary

33 mutants: **15 killed by the selftest; 18 selftest-survivors; 0 counter-only kills; 0 counter-killed survivors** (all 18 survivors score `fixtures=26/26 … verdict=TARGET_MET`, clause b selftest 91/91, clause b4 all sites killed, clause r round-42 regression 37/37). Classification of the 18 survivors: 14 equivalent (proof), 4 downstream-equivalent but unit-distinguishable (missing assertion given with actual mutant output).

## The only-consumer argument (used by the equivalence proofs)

`client_fsmode` has exactly three references in the file (computed by grep -n): its def at line 195, the callsite `fsmode = client_fsmode(c)` at line 230 inside `evaluate`, and the two unit checks at lines 458-459 inside `selftest`. In `evaluate` the returned value is consumed only by the comparisons `fsmode == 2` (line 233) and `fsmode == 1` (line 235); the verdict chain then falls through to TILED/AGREE/DIFFER exactly as it does for fsmode 0, and the summary counts verdicts, not fsmode values. Hence any mutant that, for every input, returns a value with the same `{==1, ==2}` membership as the original is observationally equivalent through the tool; divergence can only be observed by calling `client_fsmode` directly (the unit checks) or on inputs no detector feeds.

Empirical grounding: for every survivor the driver probed `client_fsmode` directly over the grid {absent, None, False, True, 0, 1, 2, 3, 4, -1, 1.0, 2.0, 2.5, "1", "2", "", [2], {"internal": 2}, (), [], {}} against pristine, recording (a) P1 = verdict-membership equivalence (`(got==2, got==1)` pairs equal) and (b) P2 = raw value+type equality. P1/P2 per mutant in `evidence/selftest.json`.

## Matrix

Legend: K = killed by selftest (failing checks named); EQ = equivalent (proof); MA = missing assertion (input -> expected; mutant's actual output). Counter column: fixtures/verdict for survivors.

| ID | Edit (old -> new, inside `client_fsmode`) | sha256 | Selftest | Counter | Classification |
|----|---|---|---|---|---|
| M01 | `c.get("fullscreen")` -> `c.get("Fullscreen")` | 440c6d8abcabffdb | rc 1, 84/91; fails fullscreen-line, fullscreen-rc | - | K |
| M02 | `c.get("fullscreen")` -> `c.get("fullscreen", 1)` | 7b953b9beeed655e | rc 1, 82/91; fails agree-line, differ-rc (absent -> MAXIMIZED) | - | K |
| M03 | `c.get("fullscreen")` -> `c.get("fullscreen", 0)` | 8f5a12e5f84c7f7e | rc 0, 91/91 | 26/26 TARGET_MET (nonce 519c7acd8ce0ba66) | EQ: absent -> f=0 -> membership fails -> returns 0, the original path; P1=P2=True, div=[] |
| M04 | drop bool guard: `isinstance(f, int) and not isinstance(f, bool) and …` -> `isinstance(f, int) and …` | 9dff31a6f09f3e58 | rc 1, 89/91; fails fullscreen-bool-ignored, fsmode-values (True -> True) | - | K |
| M05 | drop int guard: `… and not isinstance(f, bool) and f in (1, 2)` | 2ac7e0ea9ae34b9d | rc 1, 89/91; fails fullscreen-float-ignored, fsmode-values (2.0 -> 2.0) | - | K |
| M06 | `f in (1, 2)` -> `f in (1, 2, 3)` | 2c164d88ded51502 | rc 1, 90/91; fails fsmode-values (3 -> 3) | - | K |
| M07 | `f in (1, 2)` -> `f in (1, 2, 4)` | d29987fb30e46710 | rc 0, 91/91 | 26/26 TARGET_MET (nonce cf1fac2e3710b5c2) | MA: `client_fsmode({"fullscreen": 4})` -> expect 0; mutant returns 4 (probe: div=[{"in": "4", "ref": "0", "mut": "4"}]). Downstream-equivalent: 4 fails both `==2` and `==1`; neither detector feeds 4 (counter FS_POOL line 176 has no 4) |
| M08 | `f in (1, 2)` -> `f in (1, 2, -1)` | e77a58324dcfc70a | rc 0, 91/91 | 26/26 TARGET_MET (nonce 9438343873d2a7de) | MA: `client_fsmode({"fullscreen": -1})` -> expect 0; mutant returns -1. Downstream-equivalent; the counter DOES feed -1 (fsvals0, line 243; FS_POOL line 176) but -1 fails `==2`/`==1` so fixtures cannot distinguish — only the unit assertion can |
| M09 | `f in (1, 2)` -> `f in (2,)` | ea71e13bb4273fda | rc 1, 89/91; fails maximized-before-tiled, fsmode-values (1 -> 0) | - | K |
| M10 | `f in (1, 2)` -> `f in (1,)` | 84a0902e2c105154 | rc 1, 85/91; fails fullscreen-line, fullscreen-rc | - | K |
| M11 | `f in (1, 2)` -> `f in (0, 1, 2)` | ae9ba3975781c628 | rc 0, 91/91 | 26/26 TARGET_MET (nonce 72f5b5bb04b2b566) | EQ: 0 is admitted but returns 0, the original value; P1=P2=True, div=[] |
| M12 | `return f` -> `return bool(f)` | b7f2bb910594b399 | rc 1, 86/91; fails fullscreen-line, fullscreen-not-agree (fsmode 2 -> True == 1 -> MAXIMIZED) | - | K |
| M13 | `return f` -> `return 2 if f == 2 else 1` | b2579f4891ba71b8 | rc 0, 91/91 | 26/26 TARGET_MET (nonce 3d29cdf21cddcc1b) | EQ: branch reachable only for f in {1, 2}; maps 2->2, 1->1 (identity); P1=P2=True, div=[] |
| M14 | `return f` -> `return 2 if f == 1 else 2` | 2639ca670373a019 | rc 1, 89/91; fails maximized-before-tiled, fsmode-values (1 -> 2) | - | K |
| M15 | `return f` -> `return int(f)` | 1cc646a026de6c56 | rc 0, 91/91 | 26/26 TARGET_MET (nonce 1d8ca951a5bdf2e9) | EQ: branch reachable only for f in {1, 2}; int(f) == f; P1=P2=True |
| M16 | swap returns: `return f`/`return 0` -> `return 0`/`return f` | d9b5af87ffdca269 | rc 1, 81/91; fails fullscreen-line, fullscreen-rc | - | K |
| M17 | `f in (1, 2)` -> `f in (1, 2) and not c.get("floating")` | 735e0f56d0830adb | rc 1, 86/91; fails fullscreen-line, fullscreen-rc (floating client -> state lost) | - | K |
| M18 | `f in (1, 2)` -> `f in (1, 2) and c.get("mapped") is not False` | 8d41cb650365c1a7 | rc 0, 91/91 | 26/26 TARGET_MET (nonce 83efd2d34a2bb0b1) | EQ: sole callsite (line 230) runs only after the `mapped is False` skip (evaluate lines 217-219), and the unit-check dicts (lines 458-459) contain no `mapped` key, so the added conjunct is always true where it matters; P1=P2=True |
| M19 | `f in (1, 2)` -> `f in (1, 2, "2")` | 1fe3d3d99da3470c | rc 0, 91/91 | 26/26 TARGET_MET (nonce 873c1fc9ffcc0119) | EQ: the `isinstance(f, int)` gate rejects "2" before the membership test, so the widened tuple is unreachable for strings; P1=P2=True, div=[] |
| M20 | `c.get("fullscreen")` -> `(c.get("fullscreen") or 0)` | 13aad06c89aab16b | rc 0, 91/91 | 26/26 TARGET_MET (nonce 165d7b5313e00e41) | EQ: falsy inputs (absent/None/False/0) become 0, which the original also maps to 0 via the gates; truthy inputs unchanged; P1=P2=True |
| M21 | `not isinstance(f, bool)` -> `not isinstance(f, bool) or f is True` | f4b4443ce3bb8eb5 | rc 1, 89/91; fails fullscreen-bool-ignored, fsmode-values (True -> True) | - | K |
| M22 | `isinstance(f, int) and not isinstance(f, bool)` -> `isinstance(f, int) and not isinstance(f, float)` | ee188fb914d16a2f | rc 1, 89/91; fails fullscreen-bool-ignored, fsmode-values (True admitted, returns True) | - | K |
| M23 | `return f` -> `return f % 2` | 4b339dfa60dc1bee | rc 1, 85/91; fails fullscreen-line, fullscreen-rc (2 -> 0) | - | K |
| M24 | `f in (1, 2)` -> `1 <= f <= 2` | a36fb9ab5638edf8 | rc 0, 91/91 | 26/26 TARGET_MET (nonce 14e5b884207dd3ad) | EQ: floats and bools are pre-blocked by the isinstance gates, so the chained comparison sees only ints; 1, 2 pass, everything else fails, as before; P1=P2=True. (Side effect: the chained node has 2 ops, so b4's single-op filter drops it — sites 13, not 14) |
| M25 | `f in (1, 2)` -> `f in (1, 2, True)` | 552be2b20e0c9305 | rc 0, 91/91 | 26/26 TARGET_MET (nonce a72fbbe97ce5445b) | EQ: the `not isinstance(f, bool)` gate rejects True before membership; P1=P2=True |
| M26 | `f in (1, 2)` -> `f in (1, 2, 1.0)` | 1eda314352636780 | rc 0, 91/91 | 26/26 TARGET_MET (nonce 5f1fd8a09a0d65bf) | EQ: the `isinstance(f, int)` gate rejects 1.0 before membership; P1=P2=True |
| M27 | `return 0` -> `return 0.0` | f73b2836f95ac4e4 | rc 0, 91/91 | 26/26 TARGET_MET (nonce ea356283b07842ce) | MA: `client_fsmode({})` -> expect 0 of type int; mutant returns 0.0 (float). `chk` (line 306) compares with `==`, and `0.0 == 0`, so every value check passes; downstream-equivalent (0.0 fails `==2`/`==1`). Killed only by a type-strict unit assertion: `type(client_fsmode({"fullscreen": 3})) is int` |
| M28 | `return 0` -> `return False` | 54638d4d3c5d3775 | rc 0, 91/91 | 26/26 TARGET_MET (nonce eee1fe9711d7e1ee) | MA: `client_fsmode({"fullscreen": 3})` -> expect 0 of type int; mutant returns False. Same `==`-masking as M27 (`False == 0`); downstream-equivalent; killed only by a type-strict unit assertion |
| M29 | `return 0` -> `return 1` | 736e676b51b4cf37 | rc 1, 74/91; fails agree-line, differ-rc (every non-state client -> MAXIMIZED) | - | K |
| M30 | `return f` -> `return {1: 1, 2: 2}[f]` | 8ed94bad31e0c6e2 | rc 0, 91/91 | 26/26 TARGET_MET (nonce 654ea66339f89756) | EQ: branch reachable only for f in {1, 2}, so the lookup is an identity map and KeyError is impossible; P1=P2=True |
| M31 | `f in (1, 2)` -> `f in (1, 2) and isinstance(f, int)` | c3b243b5f00fb596 | rc 0, 91/91 | 26/26 TARGET_MET (nonce 68f5e221777fc3b9) | EQ: redundant conjunct — `isinstance(f, int)` is already the first conjunct of the condition; P1=P2=True |
| M32 | `f in (1, 2)` -> `f in (1, 2, "1")` | ffc734dcce8dfd20 | rc 0, 91/91 | 26/26 TARGET_MET (nonce ab3900c8f88a7b59) | EQ: int gate rejects "1" before membership (the unit check feeds "1" at line 458 but the widened tuple is unreachable); P1=P2=True |
| M33 | `not isinstance(f, bool)` -> `f is not True` | 142904fd6a3747e0 | rc 0, 91/91 | 26/26 TARGET_MET (nonce 01d64ca18cee5ccb) | EQ: True is still rejected; False now passes the guard but fails membership (`False not in (1, 2)`) and returns 0 as before; ints unchanged; P1=P2=True |

## Restoration evidence

- Pristine sha256 before mutations: `8e871a00fcf1a615e3683ebe5204f67cfe679182ff15d008b83fed34131c788d` (identical to the frozen file's sha256, computed at copy time).
- Pristine sha256 after all 33 mutant runs and 18 counter scorings: `8e871a00fcf1a615e3683ebe5204f67cfe679182ff15d008b83fed34131c788d` (unchanged; frozen original byte-identical).
- Pristine selftest after all mutations: `MADO_GEOMETRY_SELFTEST: 91/91 passed`, rc 0.
- Mutants live only as separate files under the (now deleted) scratch `mut/`; the frozen reference, the counter, and every other lane file were never written.

## Coverage findings

1. **Selftest >= counter on `client_fsmode`.** No mutant in this 33-mutant space is killed by the counter's fixtures that the selftest misses; all 18 selftest survivors also pass the counter 26/26. The selftest's unit checks `fsmode-values`/`fsmode-absent` (lines 458-459) pin the mapping more tightly than any end-to-end fixture can, because the verdict chain only tests `fsmode == 2` / `fsmode == 1`.
2. **The reference's gate-then-membership structure makes whole mutation classes vacuous.** Widening the membership tuple with wrong-typed values (`"2"`, `"1"`, `1.0`, `True` — M19/M25/M26/M32) is unreachable behind `isinstance(f, int)` / `not isinstance(f, bool)`; replacing membership with a chained range (`1 <= f <= 2`, M24) is equivalent for the same reason. Five mutants I predicted would be killed survived for this reason — the type guards, not the tuple, carry the discrimination.
3. **`chk` compares with `==` (line 306), so return-type mutants are invisible to the selftest.** `return 0.0` (M27) and `return False` (M28) pass all 91 checks yet return a float/bool where the contract says integer 0. Missing assertion that kills both: `type(client_fsmode({"fullscreen": 3})) is int` (input `{"fullscreen": 3}` -> expected `0`, int).
4. **Unfed integer widenings are unit-only distinguishable.** `f in (1, 2, 4)` (M07) and `f in (1, 2, -1)` (M08) survive both detectors; the counter feeds -1 (fsvals0, counter line 243; FS_POOL line 176) but -1 is verdict-equivalent to 0, so fixtures cannot kill it. Missing assertions: `client_fsmode({"fullscreen": 4}) == 0` and `client_fsmode({"fullscreen": -1}) == 0` (mutants return 4 and -1).
5. **The counter's load-bearing teeth on this function are clause b4, not the fixtures.** On every survivor receipt b4 flips all 13-15 comparison sites in the fullscreen-naming functions (`client_fsmode`, `evaluate`, `report`) and the selftest kills 100% of them (need was 75%). A future regression that weakens the selftest would first show up as b4 kills dropping below 11/14.
6. **No assertion gap found in the state-verdict behavior itself.** Every mutant that changes a verdict on any input either detector feeds is killed (15/15), including verdict-order probes (M17 floating-guard) and summary-line probes (M01/M10/M12/M16/M23/M29). The 4 missing assertions above are unit-pin gaps, not behavior gaps.

# MutC1CounterGates - PRED-C1-r44 counter mutation matrix (round 44, w1)

Detector: frozen scoring protocol `python3 -I <counter> --repo LANE --rev e2289516a9a857f55cda7be635933e89b931c3da --tool <subject> --nonce mutc1w1a`; rc + last line.
Subjects: REF = .ufo/waves/round-44/c1/ctl-ref-tool.py.txt; K01..K13 regenerated in scratch from the FROZEN run-c1-controls.py VARIANTS (import, no scoring loop).
34 mutants, 14 subjects, 490 matrix runs (+ baseline + restoration rerun), -P14, 543 s wall. Raw: results.tsv, logs/ (copied beside this file).

## Baseline (pristine counter, restored-bytes evidence)

- REF: rc=0 TARGET_MET 26/26 clauses=a:1 b:1 b4:1 g:1 r:1
- 13/13 controls TARGET_MISSED (nonce mutc1w1a; same pattern as frozen receipts/ctl-c1.txt at its own nonce).
- Lane bytes before/after identical: c1-r44-geometry-states.py sha256 f6b42b059b6b1f6f16657d37b0d15bd11541b04962e60154596f9037c614de65; c1-r42-geometry.py sha256 ed78d6930545aedc1b529f06dd3f9bce0d1ead88832ae3f53a125263a316ff99. Post-matrix pristine rerun on REF: TARGET_MET 26/26 rc=0.

## Matrix

| mutant | gate | REF | controls MET | verdict | note |
|---|---|---|---|---|---|
| B1-selftest-50 | MIN_SELFTEST | MET 26/26 | K13 | KILLED GATE-BROKEN | K13 scores TARGET_MET 26/26 a:1 b:1 b4:1 g:1 r:1; its selftest is 73/73 (73<80 caught pristine, 73>=50 passes mutant); b4 does NOT backstop: kills 13/14 >= need 11 |
| B2-selftest-200 | MIN_SELFTEST | TARGET_MISSED 26/26 | - | KILLED over-strict | reference selftest 91 < 200 -> b:0, fixtures 26/26 |
| B3-drop-k-eq-n | clause b | MET 26/26 | - | SURVIVED missing control | no registered tool prints k!=n with rc 0; a selftest reporting 91/80 would flip MET |
| D1-domain-loose | fsmode_of domain | TARGET_MISSED 23/26 | - | KILLED over-strict | judge accepts True/2.0; reference (strict) disagrees on fsvals0 -> fixtures 23/26 |
| D2-isinstance | fsmode_of domain | MET 26/26 | - | SURVIVED equivalent | json.loads universe {None,bool,int,float,str,list,dict}: type(x) is int <=> isinstance(x,int) and not bool; all 14 subjects verdict-identical |
| D3-member-zero | fsmode_of domain | MET 26/26 | - | SURVIVED equivalent | f=0 returns 0 == fall-through 0 |
| D4-member-three | fsmode_of domain | MET 26/26 | - | SURVIVED equivalent | f=3 returned but mode==2/mode==1 both false -> same branch as 0; counters only see v |
| D5-only-two | fsmode_of domain | TARGET_MISSED 18/26 | - | KILLED over-strict | mode-1 clients judged 0; max0/fsmix0 disagree -> fixtures 18/26 |
| D6-compare-form | fsmode_of domain | MET 26/26 | - | SURVIVED equivalent | ints with f!=0 and f<3: negatives returned but behave as 0 |
| F1-pool-nomodes | FS_POOL | MET 26/26 | - | SURVIVED redundant depth | modes 1/2 dropped from sgen pool; fsvals0/fs0/max0/fsmix0/fsmany0 already pin the domain; no control distinguished |
| F2-pool-absent | FS_POOL | MET 26/26 | - | SURVIVED redundant depth | pool -> [absent]; same |
| G1-no-fsclient | sgen fullscreenClient | MET 26/26 | - | SURVIVED redundant depth | fsclient0 fixed fixture pins the fullscreenClient field |
| G2-pool-strict | sgen field set | MET 26/26 | - | SURVIVED equiv-on-REF | adds "fullscreen": "absent" (str -> 0 on both judge and tool) -> byte-identical outputs |
| K14-kill-0 | KILL_FRACTION | MET 26/26 | - | SURVIVED missing control | need=0 vacuous; K13 still caught by b; a <75%-killed state site set flips MET |
| K15-kill-1 | KILL_FRACTION | MET 26/26 | - | SURVIVED missing control | reference kills 14/14 (need 14 passes); a 75-99% kill tool flips MISSED |
| P1-patch-removed | old.model_out patch | TARGET_MISSED 15/26 | - | KILLED over-strict | judge reverts to r42 model; reference state lines mismatch -> 15/26 (patch is load-bearing) |
| R1-needle-flip | regress needle | TARGET_MISSED 26/26 | - | KILLED over-strict | r:0 on reference, fixtures 26/26 |
| R2-drop-rc | regress rc | MET 26/26 | - | SURVIVED equivalent | r42 returns 0 iff met and prints final verdict=TARGET_MET iff met (c1-r42-geometry.py:999-1003) => rc==0 <=> needle; all 14 identical |
| R3-drop-needle | regress needle | MET 26/26 | - | SURVIVED equivalent | same seam, converse direction |
| S1-suffix-always | suffix condition | TARGET_MISSED 10/26 | - | KILLED over-strict | stateless fixtures expect bare summary; 10/26 |
| S2-suffix-gt1 | suffix condition | TARGET_MISSED 19/26 | - | KILLED over-strict | single-state fixtures lose the fields; 19/26 |
| S3-suffix-or | suffix condition | MET 26/26 | - | SURVIVED equivalent | nonneg ints: a+b>0 <=> a or b |
| S4-sites-0 | MIN_STATE_SITES | MET 26/26 | - | SURVIVED missing control | floor not load-bearing: K13 caught by b (b4 skipped when b=0); a correct tool with <6 state sites would flip MISSED->MET |
| S5-sites-9 | MIN_STATE_SITES | MET 26/26 | - | SURVIVED missing control | reference has 14 sites >= 9 |
| T1-total-27 | TOTAL | none none | - | KILLED over-strict (crash) | assert len(cases)==TOTAL fails: AssertionError: 26, rc=1 no verdict line, all 14 subjects |
| T2-ngen-11 | N_GEN | none none | - | KILLED over-strict (crash) | 24 cases != TOTAL 26 -> AssertionError, all 14 |
| T3-ngen-13 | N_GEN | none none | - | KILLED over-strict (crash) | 27 cases != TOTAL 26 -> AssertionError, all 14 |
| V1-mode-swap | verdict order | MET 26/26 | - | SURVIVED equivalent | mode in {0,1,2} disjoint; 1-before-2 order free |
| V2-badsize-last | verdict order | TARGET_MISSED 25/26 | - | KILLED over-strict | judge wants FULLSCREEN for size-none mode-2; reference emits BADSIZE -> fsbad0 25/26 |
| V3-tiled-first | verdict order | TARGET_MISSED 23/26 | - | KILLED over-strict | judge wants TILED for max0; reference emits MAXIMIZED -> 23/26 |
| X1-fs0-mode0 | FIXED content | MET 26/26 | - | SURVIVED structural | fixture IS the judge: content swap (mode 2->0) invisible while tool and judge agree; only TOTAL length is asserted |
| Y1-teeth-true | state_teeth return | MET 26/26 | - | SURVIVED missing control | b4 forced true; K13 still caught by b -> the b4-dedicated cheat (state-blind tool, hollow selftest n>=80) has no registered control |
| Y3-case-sensitive | site selector | MET 26/26 | - | SURVIVED equiv-on-REF | sites=14 killed=14 identical to pristine (all named fns hold a lowercase literal); narrowing unobservable on this suite |
| Y4-drop-kneq | teeth dead test | MET 26/26 | - | SURVIVED equiv-on-REF | all 14 reference flips die via rc!=0 or no summary (14/14 still killed); a count-skew-only flip would survive -> unregistered |

## Headline finding (the one gate-broken mutant)

B1-selftest-50: lowering MIN_SELFTEST 80->50 makes control K13-no-new-selftest score TARGET_MET
(26/26 fixtures, a:1 b:1 b4:1 g:1 r:1). K13's selftest is 73/73: the 80-floor is the ONLY registered
guard against a hollowed selftest. b4 does not backstop K13 - its 14 state sites still kill 13/14 >= need 11
under the cut selftest, because flipping any mode/fsmode comparison changes EVERY matched client's verdict,
state case or not. Clause r stays 37/37 and fixtures stay 26/26 for K13 even pristine. Coverage gap:
no registered control carries a state-logic defect inside a selftest-consistent tool with n >= 80 -
exactly the cheat b4 was built for; registering one would guard MIN_SELFTEST, KILL_FRACTION and b4 all at once.

## Killed mutants (15)

- 12 over-strict against the REFERENCE (the judge/model side is pinned by fsvals0, fs0, max0, fsbad0, fsmix0, fsmany0): D1 23/26, D5 18/26, V2 25/26, V3 23/26, S1 10/26, S2 19/26, B2 b:0, R1 r:0 (fixtures 26/26), P1 15/26.
- 3 crash kills: T1/T2/T3 - `assert len(cases) == TOTAL` (c1-r44-geometry-states.py main) fires on any TOTAL/N_GEN drift: brittle but fatal (rc=1, no verdict line, all 14 subjects).

## Survivors (21) - equivalent vs missing control

- Equivalent by construction, verdict-identical on all 14 subjects: D2, D3, D4, D6 (fsmode_of domain forms), V1 (disjoint mode tests), S3 (a+b>0 <=> a or b), R2/R3 (rc==0 <=> verdict=TARGET_MET in the r42 subprocess, c1-r42-geometry.py:999-1003).
- Equivalent on the reference (measured), residual narrowing declared: Y3 (sites 14->14, killed 14), Y4 (all 14 flips die via rc!=0/missing summary), G2 ("fullscreen": "absent" -> 0 both sides).
- Missing control (mutant and pristine indistinguishable on every registered subject): B3 (b drops k==n), S4/S5 (MIN_STATE_SITES floor not load-bearing; K13 reaches b4 only when b passes), K14/K15 (KILL_FRACTION not load-bearing; reference kills 14/14 so kill=1.0 also passes), Y1 (state_teeth->True; K13 still b:0), F1/F2 (FS_POOL depth; fsvals0+fsmany0 pin the domain), G1 (fsclient0 pins fullscreenClient), X1 (fixture content unobservable while tool and judge agree; only its length is asserted).

## Control-layer observation

Every K01..K12 control fails clause b first: a single defect edit breaks the reference selftest's embedded
expectations (b:0 for all; K01 18/26, K02 10/26, K03 23/26, K04 23/26, K05 25/26, K06 24/26, K07 23/26,
K08 14/26, K09 17/26, K13 26/26 at nonce mutc1w1a). The fixture judge is the second layer; it alone decides
only for tools whose selftest is consistent with their defect - the population the b-floor and b4 guard, and
the population K13 (b-caught) and B1 (gate-broken) bracket.


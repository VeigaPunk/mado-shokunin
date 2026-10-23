# ReviewWSet — round 27 w1: W-set mutant fidelity vs round-26 probes

**Scope.** Read-only check that each of the 15 W mutants in `.ufo/waves/round-27/c2/mutants-w.json`
reproduces the round-26 probe it names (`.ufo/waves/round-26/w2/reports/MutSelftest.md` and
`MutQ37.md` tables): same smallest behaviour change, `c1-*` faithfully re-expressed on
`c1/count-v2.py`, `old` text unique in the subject. No suite or counter was run; no lane byte
outside this report was written. Leaf seat: no subagents. No Hyprland instance, oracle, network or
tool install was involved (pure byte/source review, so no coredump delta applies).

**Inputs (hashes as read).**
- `.ufo/waves/round-27/c2/mutants-w.json` sha256 `0ad0e46c1a6e61f369c30ab08d6a998f6dce7d16436087b5df57fb8f22323608` (15 entries)
- Subjects, byte-identical to the round-26 reports' recorded "before" hashes:
  - `.ufo/waves/round-26/c1/count-v2.py` sha256 `4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428` (= MutSelftest row V2)
  - `.ufo/waves/round-26/c2/count.py` sha256 `b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8` (= MutSelftest row B)
  - `.ufo/waves/round-26/quality/check-population.py` sha256 `803e0096c994d301fa7fe9a9dd7e35255ee1f5bcf3f63d15956cdba8943d0f64` (= MutQ37 recorded hash)
- `git status --porcelain` on the four paths is empty (working tree = tip `5ddc5885` at review time).

## Method (four checks)

1. **Uniqueness.** For every entry, `subject.count(old) == 1` on the current bytes; occurrence line recorded.
2. **Byte-exact reproduction where possible.** For the 11 entries whose subject is byte-identical to
   what round-26 mutated (5 `c2-*`, 6 `q37-*`), apply `old→new` to the pristine bytes and sha256 the
   result; compare with the round-26 report's recorded mutant hash.
3. **Faithful re-expression for `c1-*`.** Round-26 never mutated `count-v2.py` (MutSelftest: "No
   C1-v2 mutation coverage is claimed below"; its pristine v2 baseline failed 7/9), so no mutant hash
   exists to compare. Instead: (a) confirm the v1 anchor lines in `c1/count.py` (255/268/276/286)
   carry the same construct; (b) read the v2 context at each W site and confirm the mutation hits the
   same control point with the same minimal edit; (c) `compile()` each mutated v2 source (must be runnable).
4. **Anchor agreement.** W-set occurrence lines vs the line numbers cited in the round-26 reports.

## Per-mutant results

| id | subject:line of `old` | r26 probe (report line) | r26 verdict | uniqueness | reproduction evidence |
|---|---|---|---|---|---|
| c1-drop-bezier | c1/count-v2.py:359 | MutSelftest `c1/count.py:276` | SURVIVED | 1 | v1:276 same text; v2 context identical (`gn,gb=node_set/bez_set(got)` vs `en,eb` of exp; dropping `and gb == eb` passes bezier-only mismatch); mutant compiles; mut sha256 `e41c704d25755aa76b6b41ad7350af73a05d2ce739e0650b4ae2724df2dd86f6` |
| c1-accept-nonjson | c1/count-v2.py:351 | MutSelftest `c1/count.py:268` | SURVIVED | 1 | v1:268 same text; v2 branch is `if got is None or not well_formed(got):` (malformed/missing output records False → mutant records True); compiles; `b5c39db4853128caa5e926d9dcebaec6384d51bae85d37653118d2379f032459` |
| c1-pass-90pct | c1/count-v2.py:372 | MutSelftest `c1/count.py:286` | SURVIVED | 1 | v1:286 same text; v2 `met` feeds the `PRED-C1-r26-v2 cases_pass=` line and `return 0 if met else 1`; ≥90% relaxation identical; compiles; `4d1f45260a403352cb760f89de068a4523a8cfbcb228afbc707e85c19b84d2f1` |
| c1-skip-base-guard | c1/count-v2.py:333 | MutSelftest `c1/count.py:255` | KILLED | 1 | v1:255 same text; v2 guard sits between the two BASE fetches (`truth["BASE"]`, `futs["BASE#2"]`, both still submitted) and its body is the sole `die("ORACLE_UNSTABLE two oracle runs …")`; `if False:` skips only drift detection, both BASE calls still occur; compiles; `1430490669e1d8be97bb47dc72c645aa8d5371147d9a7bc4ec0b177d15ff66f9` |
| c2-drop-arg | c2/count.py:208 | MutSelftest `:208` | KILLED | 1 | mutant bytes = r26 mutant hash `20700abfe874…999d69` (byte-exact) |
| c2-skip-base-guard | c2/count.py:164 | MutSelftest `:164` | KILLED | 1 | byte-exact, `a9727feee024…8974ca`; context confirms: `n1,n2 = V3.compare(base, r2["binds"])[:2]`, guard body `die("ORACLE_UNSTABLE …")`, both BASE oracle runs still occur |
| c2-embed-min-1000 | c2/count.py:34 | MutSelftest `:34` | KILLED | 1 | byte-exact, `fcbce4b6ea57…3a6937` |
| c2-accept-nonjson | c2/count.py:206 | MutSelftest `:206` | SURVIVED | 1 | byte-exact, `e6a983ef36e5…12632` |
| c2-pass-90pct | c2/count.py:222 | MutSelftest `:222` | SURVIVED | 1 | byte-exact, `314be3f402a5…f10e`; retains `and embed_hits == 0` as r26 did |
| q37-M1-ignore-registered | quality/check-population.py:145 | MutQ37 M1, L145 | KILLED by F4/F5 | 1 | byte-exact, `104125da9a88…10a07`; `den` is the loop's denominator, in scope |
| q37-M2-case-anywhere | :45 | M2, L45 | SURVIVED fixtures, S1 kills | 1 | byte-exact, `d61abdca3634…7b1a` |
| q37-M3-drop-denominator | :149–150 | M3, remove L149–150 | KILLED by F3 | 1 | byte-exact, `c4d62c78a8b1…e06f`; block body is the single `legs.append("denominator")` line, removal syntactically clean |
| q37-M4-first-pred-only | :138 | M4, `summaries[:1]` | SURVIVED fixtures, S2 kills | 1 | byte-exact, `86f190e80f29…340d` |
| q37-M5-case-plus-one | :137 | M5, add 1 to CASE tally | KILLED by F1/F2 | 1 | textual re-expression — see Finding 1 |
| q37-M6-unreadable-exit-0 | :163 | M6, `"UNREADABLE", 0` | SURVIVED fixtures, S3 kills | 1 | byte-exact, `aa8c8006f5cf…3292` |

11/15 recomputed mutant hashes equal the round-26-recorded mutant hashes byte-for-byte, i.e. the W
entry is literally the same edit round-26 applied. All 15 W-set occurrence lines match the line
numbers cited in the round-26 reports (c2: 34/164/206/208/222; q37: 45/137/138/145/149–150/163).

## Findings

**No mismatch. All 15 W mutants reproduce their named round-26 probes: same smallest behaviour
change, same control point, `old` unique in its subject.**

**Finding 1 (note, not a defect) — q37-M5 textual re-expression.** Round-26's M5 mutant was
`case_lines = sum(…) + 1` (suffix): applying that to the pristine bytes reproduces the recorded r26
mutant hash `693fc87ccf0ab041242b315c381f5ad507cd5771a2f97cee2110458cb77123b3`. The W entry uses the
prefix form `1 + sum(…)`, whose mutant hash is `21774b2c5cbd54f3…`. The two are behaviourally
identical on every input (integer addition, pure generator evaluated once, `case_lines` = true CASE
count + 1), so the probe's kill outcomes (F1, F2, S1 per MutQ37) carry over unchanged. Anyone
cross-diffing W-set mutants against r26's recorded mutant hashes should expect exactly this one
hash difference. The retained r26 scratch copies under `/fast/scratch/hyaku/mado-r26/MutQ37/mutants/`
are post-restoration pristine bytes (hash `803e0096…`), so the suffix form was confirmed by hash
reconstruction, not by a surviving mutated file.

**Finding 2 (context note) — `c1-*` fidelity is source-verified, not runtime-verified.** Round-26
never mutated `count-v2.py`, so fidelity rests on construct identity: each W site in count-v2.py is
the exact v1 text (where v1 shares it) at the equivalent control point of the v2 pipeline, single
occurrence, and the mutated source compiles. The v1 anchors were confirmed in `c1/count.py`
(255/268/276/286, identical texts, each also unique there for the three shared texts).

## Residual risk and verification gaps

- This review did not execute `quality/counter-selftest.py`, `quality/population-suite.py` or the C2
  counter, so it makes no claim about whether the round-27 suites kill these 15 (that is the C2
  measurement). Round-26 kill/survive verdicts are cited from the r26 reports only.
- The `c1-*` equivalence argument is static; a runtime witness on count-v2.py (e.g. a drift fixture
  exercising the :333 guard) would strengthen it but was out of scope for a read-only review.
- Verification commands (all read-only; scratch-free, nothing written outside this report):
  - `python3` JSON dump of mutants-w.json; per-entry `subject.count(old)` and occurrence line.
  - `sha256sum` of the three subjects vs r26-recorded hashes; `git status --porcelain` on the four paths.
  - Mutant recomputation: `src.replace(old,new,1)`, `hashlib.sha256`, `compile(mut,…,'exec')`.
  - M5 reconstruction over candidate replacement texts (suffix `+ 1` matched the recorded hash).

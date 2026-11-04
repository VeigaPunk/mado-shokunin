# R70ConnSiblings — cross-instrument overlap scan (round 70)

Read-only. No production file drafted, no lane file edited, no git mutation. Axes under scan:
C1 calibration (kill credit) and C2 operability (guard carriers).

## 0. Pin, and a tip that moved during the scan

Scan pinned to `5144a6b5f43225d8021a469f4d24c19558026b9e` (the instrument commit). The lane HEAD
advanced while this seat read: `5144a6b5` → `9508e878` → `5adba5a9` → `71caa8b7` → `3aea1e10`
(observed at the end). Only two instrument deltas are in that range, both claimed predicate-neutral:

| file | sha256 @ 5144a6b5 | sha256 @ tip 3aea1e10 | delta |
|---|---|---|---|
| `quality/counters/c1-r70-landing-controls.py` | `71a7b6c45b904a734f194be9a8de6cc2eeb5f5ea1922760f908f5637f1d4db58` | same | none |
| `quality/counters/c1-r70-real-children.py` | `b1785f388724c8f0a21dda016da2e212105354221767eaa128fa73c3ddaaebb4` | `b3a6f131abf371ecf64273b65a143478c4b23eaa7acf974ec80e5efebf6e6a7b` | +1 line, `os.makedirs(scratch, exist_ok=True)` in `run_harness` (was frozen line 249; every later line shifts +1) |
| `quality/counters/c2-r70-carriers.py` | `87ca466432302feaabf2c504dc131184178afe199d8b84fa492ad3b5211af9f7` | `d868ae334b794f99544bd41b1265a9ee6bb5a380278755c6d1223630abd21363` | 4 lines gain `leg=` in `score_cases`; net 0 line shift |

Consequence for the L1: the frozen sentence's `REV` must be the integrated tip, and
`.ufo/waves/round-70/measurement-r70.txt` already records measured content `5adba5a9…` (not the
pin above). Line numbers below are pin numbers except where marked "tip"; the two files marked
shift are cited at pin.

## 1. Kill-credit decision across every instrument

Grep: `grep -rn --include='*.py' --include='*.sh' --exclude-dir=__pycache__ 'rc != 0\|returncode != 0\|\bkilled\b' quality/ tools/` → **374** raw lines. All but the sites below are ordinary
failure guards (a non-zero status aborts a leg, it never becomes a credit); the round-70 rule is
not applicable to them. Example class, not a credit: `quality/check-axis-scores.py:106,271,276`,
`quality/check-evidence-pointers.py:83,181,212`, `quality/check-freeze-order.py:62,106`,
`quality/check-tool-ledger.py:117,129,485`, `quality/check-wave-done.py:196,602`,
`quality/check-deliverables.py:97`, `quality/check-session-material.py:636,929,1006`,
`quality/check-r38-discrimination.py:164,173`, `quality/check-round-outcome-first.py:76`,
`quality/r55_ctl_c1.py:255`, `quality/r56_ctl_c3.py:421`, `tools/mado-hostguard.py:413`.

Decision sites (the branch that turns a child's exit status into a credit):

| # | site (pin) | construction | crash credited? | round-70 rule | action for L1 |
|---|---|---|---|---|---|
| 1 | `quality/counters/c1-r70-landing-controls.py:478` (+ `:315-327 summary_shows_failure`) | `mz_killed = bool(mz_rc != 0 and summary_shows_failure(mz_out))`, summary must parse `p/n` with `p < n` | **no** | this *is* the rule | none; the scored surface |
| 2 | `quality/counters/c1-r69-landing-controls.py:452` | `mz_killed = mz_rc != 0` | **yes** | applies; violates | keep byte-identical (harm watch); supersession note only |
| 3 | `quality/counters/c1-r68-landing-controls.py:439` | `mz_killed = mz_rc != 0` | **yes** | applies; violates | supersession note only |
| 4 | `quality/counters/c2-r67-landing-controls.py:437` | `mz_killed = mz_rc != 0` | **yes** | applies by shape, but the file is outside the frozen surface (`c1-*`) and is the **base control** of `c1-r68-selfmutants.py:41` | name it in the lesson; never edit (it is a live frozen control, not dead code) |
| 5 | `quality/counters/c1-r69-paired-recipes.py:173,175` | `killed = rc != 0` on the *mutated harness's own selftest* | yes, but the question is "did the recipe kill the harness", not "did the harness credit a kill" | does **not** apply verbatim; different layer | leave; the frozen counter must stay `killed=3/3 base=0/3` |
| 6 | `quality/counters/c1-r68-selfmutants.py:166` | `died = rc != 0` on a candidate harness mutant | same layer as #5 | does **not** apply verbatim | leave |
| 7 | `quality/counters/c1-r40-live-v2.py:1163` | `dead = rc != 0 or not has or k < n_` | **yes** (a crash is dead) | same hazard, generic clause-mutation driver, out of claim scope | report only; not this round |
| 8 | `quality/counters/c1-r41-globals.py:773`; `c1-r41-globals-v2.py:1108`; `c1-r42-geometry.py:923`; `c1-r44-geometry-states.py:302`; `c1-r44-geometry-states-v2.py:327,369` | same `dead = rc != 0 or not has or k != n_` | **yes** | same hazard, out of scope | report only |
| 9 | `quality/counters/c1-r40-live-v2.py:1209`; `c1-r45-monitors.py:347`/`-v2:383`; `c1-r47-terminal.py:400`; `c1-r48-terminal-cache.py:968`/`-v2:968`; `c1-r49-keysym.py:664`; `quality/check-counter-discrimination.py:69-80` (`observed_of`, rc must agree with the parsed verdict) | parse-gated | no | already compliant | none |
| 10 | `tools/mado-verify.sh:2171-2227` | counts `KILLED` **labels** from a results table, not rc | no (label-based) | n/a | none |
| 11 | `quality/counters/c2-r70-carriers.py` | no `killed` branch at all (`grep -c killed` = 0) | n/a | n/a | C2's discrimination is the 17-case set, not a kill count |

Additional stale *text* (not a decision): `c1-r68-selfmutants.py:15,44` and
`c1-r69-paired-recipes.py:18,55` pin `mz_killed = mz_rc != 0` as a **recipe find-string**. It still
matches because their candidates (`c1-r68…`, `c1-r69…`) are byte-frozen; it no longer matches
`c1-r70-landing-controls.py`. Do not retarget those recipes at the r70 harness — the find-string
would be inapplicable and the r69 counter's frozen denominator would change.

**Verdict.** Exactly one decision site on the frozen target surface implements the rule (#1);
three landing-harness sites (#2-#4) carry the defect, two of them frozen on purpose (#2 base leg,
#4 live base control). The four generic `dead = rc != 0 …` drivers (#7-#8) are the same hazard on
other surfaces: adjacency, not scope.

## 2. Guard token and carrier shapes across the tree

Population at the pin and at the tip: **20** tracked `quality/check-[^/]+\.py` (regex pinned at
`quality/counters/c2-r70-carriers.py:74`). Readers **13**, all guarded **13**, unguarded **0**.
Every one of the 13 carries the key in a *held* (round-69) construction:

| reader | guard site(s) | shape class |
|---|---|---|
| `quality/check-anchor-cover.py` | 102-105 | inline dict-literal key |
| `quality/check-axis-scores.py` | 99, 122 | `env["KEY"] = "1"` subscript store |
| `quality/check-control-receipts.py` | 62 | subscript store |
| `quality/check-deliverables.py` | 96, 116 | `dict(os.environ, KEY="1")` keyword |
| `quality/check-evidence-pointers.py` | 71-72 | module mapping constant `GIT_ENV[...]` (held `module-constant`) |
| `quality/check-freeze-order.py` | 46 | subscript store |
| `quality/check-index-rows.py` | 57, 406 | subscript store / dict keyword |
| `quality/check-index.py` | 50, 283 | subscript store / dict keyword |
| `quality/check-landed-contract.py` | 57 | dict keyword |
| `quality/check-round-outcome-first.py` | 74, 128 | dict keyword |
| `quality/check-session-material.py` | 927, 984 | dict keyword |
| `quality/check-tool-ledger.py` | 109 | subscript store |
| `quality/check-wave-done.py` | 187 | subscript store |

The four round-70 shapes have **zero real carriers** in the population, and none anywhere under
`quality/` or `tools/`:

- *alias-carried*: no name is bound to an env-named mapping and used as the `env=` hand-off.
- *attribute-carried*: no `self.<attr>[KEY] = …` guard store. The only `self.env` subscript in the
  population is `quality/check-tool-ledger.py:473` (`self.env["TMPDIR"] = root` in the fixture
  class, whose guard is the :109 subscript store) — fixture plumbing, not a carrier.
- *splat-carried*: no `**` expansion reaches an `env=` mapping. The population's `**` uses are
  docstring prose, a fixture-dict merge (`quality/check-session-material.py:1563`), a recursive
  glob (`quality/check-state-cite.py:68`), `**extra` kwargs (`quality/check-wave-done.py:633`) and
  a markdown strip (`quality/check-tool-ledger.py:200`).
- *constant-key*: no population file (`quality/check-*.py`) binds the key to a module-level
  constant used as a subscript key. The only module-level `KEY = "GIT_NO_REPLACE_OBJECTS"`
  bindings are the censuses' own classifier constant (`quality/counters/c2-r68-reader-guard.py:44`,
  `c2-r69-guard-dominance.py:58`, `c2-r70-carriers.py:73`) — outside the population and not an env
  construction — plus fixture *strings* inside the harnesses' selftests
  (`c1-r70-landing-controls.py:773` and its r69/r68/r67 predecessors). Every real-file occurrence
  in the population is the literal key in key position.

**Census verdict: 13/13 does not change.** No new production file becomes a reader: the three
round-70 instruments live under `quality/counters/` and the population regex is single-segment
`quality/check-*.py`; no `quality/check-*.py` was added this round (`git ls-tree` = 20 at both pin
and tip). The new shapes only buy discrimination on the frozen control set (`controls=17/17` vs
`base_controls=13/17`), which is what the claim says.

Stale doc note: `quality/counters/c2-r68-reader-guard.py:19` still defines a guard as "(d) a
constant inside any `env=` keyword subtree"; the r70 rule is stricter (key position + dominance +
four carriers). The r68 file is superseded and its text may stay, but the lesson must not quote it
as the current rule; `quality/tool-ledger.md:151` paraphrases it without the stale clause.

## 3. Shared housekeeping between C1 and C2

The claim-level isolation holds: neither counter reads the other's artifacts
(`c1-r70-real-children.py:62-68` names only the r70/r69 harness, the lane and the three children;
`c2-r70-carriers.py:72-73,84-87` names only `c2-r69-guard-dominance.py` and the two control files). The
*integration* surface is not isolated — both claims must edit the same ten documents:

| file | both claims? | state at scan |
|---|---|---|
| `corpus/lessons/round-70.md` | yes — C1 + C2 entries, `## Gate` source row(s) | **absent**; must be created |
| `corpus/QUALITY.md` | yes — one criterion row each (next numbers after 111) | dirty in the worktree (a sibling seat is editing) |
| `corpus/SOURCES.md` | yes — one source row each (subprocess.rst, expressions.rst) | dirty in the worktree |
| `corpus/knowledge/<slug>-r70.md` | C2 needs one (the r69 precedent is one knowledge entry per round); C1's door is the lesson `## Gate` | absent |
| `quality/tool-ledger.md` | yes — rows for all three instruments | landed at `71caa8b7` (rows 155-157); `check-tool-ledger.py` reports `population=119 ledger_rows=119 uncovered=0` at that rev |
| `SKILL.md` | yes — two gate rows | unchanged; no r70 rows yet |
| `PROVINCE.md` | yes — one round-70 instrument paragraph | unchanged |
| `SCORECARD.md` | yes — two capability rows + the axis-table re-derivation | dirty in the worktree |
| `LOG.md` | yes — one round section covering both | no r70 section yet |
| `.ufo/waves/round-70/measurement-r70.txt` (+ `harm-watch-r70.txt`) | yes — both claims' sentences | measurement exists (content `5adba5a9`); harm watch landed at `71caa8b7` |

So: **not only the wave and lesson.** Any two seats appending to `corpus/QUALITY.md`,
`corpus/SOURCES.md`, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md` or the ledger concurrently
will collide; the L1 must serialize those edits (one scribe, or L1-only).

Selftest helper duplication (fork-copies, no shared module imported):

| helper | C1 harness | C1 real-children | C2 carriers |
|---|---|---|---|
| `absolute_scratch` | 149 | 150 | 129 |
| `_selftest_checks` | 731 | 322 | 1002 |
| `selftest` | 859 | 393 | 1088 |
| `_refuses` | — (same checks inline, `:808-811`) | 376 | — |
| `_refuses_symlink` | — (inline, `:812-814`) | 384 | — |
| `_raises` | — | — | 1078 |
| `contract_line` | 352 | 185 | 803 |
| `verdict_met` | — | 181 | 696 |

15 identical def/const names across all three; 21 between the two C1 files. Divergence already
exists: `git()` is `git(fx, args, identity=False)` in real-children and `git(repo, args)` in C2 —
same name, different semantics. Any future merge must not assume portability.

Scratch subdirectories (`--scratch-root DIR`):

| instrument | measure | selftest | cleanup |
|---|---|---|---|
| `c1-r70-landing-controls.py` | `DIR/r70-c1` (`:432`, rmtree `:433`) | `DIR/r70-c1-selftest` (`:896`, rmtree first, rmtree in `finally`) | removes its own selftest dir; leaves `r70-c1` after a measure |
| `c1-r70-real-children.py` | `DIR/r70-c1` (pin `:268`, rmtree `:269`) | `DIR/r70-c1-selftest` (pin `:415`, rmtree first) | leaves `r70-c1`; the selftest dir is **not** removed on success (no `finally`) |
| `c2-r70-carriers.py` | `DIR/r70-c2-carriers` (`:818-821`) | writes `DIR/controls-tampered.json` at the **root** (`:1070`) | leaves both |

- `r70-c1` vs `r70-c2-carriers`: **no cross-claim collision.**
- **Within C1**: both files claim `DIR/r70-c1` and both `rmtree` it at entry
  (`c1-r70-landing-controls.py:433`, `c1-r70-real-children.py:269`). Running the scored C1 command
  and the scored harness under one root — concurrently or back to back — deletes the other's tree.
  The scored command is safe in isolation because it hands the harness
  `DIR/r70-c1/cand-<mode>` / `base-<mode>` (pin `:304-307`), never `DIR/r70-c1` itself.
- **Within C1, selftests**: both use `DIR/r70-c1-selftest` and both rmtree at entry; concurrent
  selftests under one root destroy each other (sequential is fine).
- C2 writes `controls-tampered.json` outside its own namespace; benign (unique name) but it is the
  only root-level write in the trio.
- The harm watch already uses one root per invocation (`.../l1/t1`, `.../l1/t2`); keep that.

## 4. Instruments this round supersedes or leaves behind

Selftests run from blobs extracted at the pin, `python3 -I <file> --selftest --scratch-root <dir>`
(distinct dirs, pre-created); all exit 0.

| instrument | sha256 @ pin | selftest @ pin | still works? | becomes misleading? | action |
|---|---|---|---|---|---|
| `quality/counters/c1-r69-landing-controls.py` | `9461a059466e723ba0ae88c86dea2fc97eb5f4fdfb15ef6c6646acce69649a73` | `59/59` rc0 | yes — measurement path unchanged | **yes** as a scored r70 harness: credits crash and garbage (`control-baseline-r70.txt` § C1: `base_correct=1/3`) | byte-frozen + base leg; supersession note naming `c1-r70-landing-controls.py` |
| `quality/counters/c1-r69-paired-recipes.py` | `15a43adcb304b2f93cf373535f61d0be13b554f4abcdf9759215334536039088` | `28/28` rc0 | yes — R2 find-string still present in its frozen candidate `c1-r69-landing-controls.py:452` | no, for its own claim; its kill notion is the *harness-mutant* layer | keep (harm watch requires `killed=3/3 base=0/3`); note the layer distinction |
| `quality/counters/c2-r69-guard-dominance.py` | `53f256f4693526f2c37cced5203c2e1d6007b721c4b6c0d7fa522e165597e929` | `41/41` rc0 | yes | **yes** if scored on the r70 17-case set: `13/17` (`control-baseline-r70.txt` § C2) | base leg by design; supersession note naming `c2-r70-carriers.py` |
| `quality/counters/c1-r68-landing-controls.py` | `25470bc432ad3b612f08869052915f331d9a930149b3af6a9bf0e3eb87cf5527` | `52/52` rc0 | yes | **yes** — two generations behind, same bare-rc defect | note; no edit |
| `quality/counters/c2-r68-reader-guard.py` | `3c08aa047c73c42a8564445e57ccbabe8475f02293860b40e730ba69c0617d31` | `26/26` rc0 | yes | **yes** — its classifier scored `7/11` on the r69 set (r69 baseline / `LOG.md` r69), i.e. it accepts value-position, dead-branch, uncalled-helper and overwritten-env | note; no edit |
| (found by the same grep, not on the seat's list) `quality/counters/c2-r67-landing-controls.py` | — | — | yes | same bare-rc defect at `:437`, under a **C2** name after the axis swap | it is the live base control of `c1-r68-selfmutants.py:41` — do not edit; the lesson must say it is a frozen control, not a current C2 instrument |

No compatibility alias is added or needed: the supersession is one sentence per instrument in
`corpus/lessons/round-70.md`, naming the successor and the reason (`rc != 0` → parsed `p < n`).
The lesson should also state that `c2-r67-landing-controls.py` is *not* superseded-and-removable —
it is another counter's pinned base leg.

## 5. Sibling-lane overlap

| lane | path:line | craft | contested? |
|---|---|---|---|
| kaidoku | `tools/round-69/mutation-check.py:140-156` | kill credited only when the expected failed case is in the parsed failure set; a crash with no parsed failure is `killed_wrong_case`/`unevaluable` ("a syntax error is not a gate") | **same craft as round-70 C1, one round earlier**; different subject (its own gate), not contested |
| kaidoku | `tools/round-34/replay-gate.py:269` | `killed_here = run.returncode != expected_exit` — bare exit-difference, credits a crash | older craft; not contested |
| kaidoku | `tools/round-67/mutation-battery.py:315-323,382-393` | killed/survived table from reruns | adjacent; not contested |
| tameshi | `tools/bash-witness-study.py:393,523` | "killed-on-witness iff a full-denominator red run fails >=1 declared" | same family (parsed failure required); not contested |
| mado (same lane) | `tools/mado-verify.sh:2171-2227` | counts `KILLED` labels from a recorded table | in-lane, different instrument (stub defects) |
| any sibling | — | **no** AST carrier/dominance census exists. `GIT_NO_REPLACE_OBJECTS` appears in 26 sibling tool files (kaidoku r25-r50, kotodama harness, souji, tsukuroi, mori, tameshi) purely as their own git-hygiene env; none co-occurs with `ast.parse`/`ast.walk` | C2's craft is unique to mado |

**Adjacency verdict.** The kill-credit craft is *shared, not contested*: kaidoku's round-69
`mutation-check.py` already enforces the same "a broken child is not a kill" rule on its own gate,
and tameshi's witness study requires a declared failure before a kill; both are different subjects
with their own frozen receipts, so nothing is absorbed, cited as authority, or edited. The carrier
census has no counterpart anywhere in the fleet — the nearest neighbours are string-level git-env
hygiene, not a construction classifier. The only true duplication found in this scan is *inside*
mado: `c2-r67-landing-controls.py` (a C2-named copy of the landing harness, still bare-rc at
`:437`, live as the r68 counter's base leg) and the four `dead = rc != 0 …` clause-mutation
drivers, neither of which the round-70 claim may touch.

## Evidence (commands, exit codes)

- `git ls-tree -r --name-only 5144a6b5 | grep -cE '^quality/check-[^/]+\.py$'` → `20`; same at tip → `20`.
- `git show 5144a6b5:<file> | sha256sum` for the five legacy instruments → the hashes in §4.
- `python3 -I <extracted legacy> --selftest --scratch-root <dir>` →
  `MADO_R69_LANDING_CONTROLS_SELFTEST: 59/59`, `MADO_R69_PAIRED_RECIPES_SELFTEST: 28/28`,
  `MADO_R69_GUARD_DOMINANCE_SELFTEST: 41/41`, `MADO_R68_LANDING_CONTROLS_SELFTEST: 52/52`,
  `MADO_R68_READER_GUARD_SELFTEST: 26/26`; all **rc 0**.
- AST scan (Python `ast`, 118 production `.py` at the pin): no `**` splat carries a key-carrying
  mapping into an `env=`; no `self.<attr>[KEY]` guard store; no alias hand-off; no population file
  uses a module-level key constant as a subscript key. (The scan reports *uses*; the bare
  `KEY = "…"` definitions it found are the censuses' own, listed in §2.)
- `grep -rn --exclude-dir=__pycache__ 'GIT_NO_REPLACE_OBJECTS' quality/ tools/` → 179 hits in 30
  files; 13/13 population readers have ≥1 hit (counts in §2).
- `grep -c killed quality/counters/c2-r70-carriers.py` → `0`.
- `git diff --name-only` during the scan → `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`
  (concurrent seats; not touched).

Scratch `/fast/scratch/hyaku/mado-r70/R70ConnSiblings/` removed before yield.

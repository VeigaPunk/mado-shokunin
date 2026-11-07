# R93MReviewC2 — review of the C2 gate, kill-set, panel, frozen mutants and counter (round 93, wave w1)

Seat R93MReviewC2 (reviewer, leaf). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, base rev
`4c6f723f3dca3a26f9d14475d695fe797e2e972c`. Scratch `S=/fast/scratch/hyaku/mado-r93/R93MReviewC2` (deleted on
exit). **Every run below is a DRAFT run**: nothing here is a measurement, no `TARGET_*` word is claimed for the
lane, and nothing was written under `.ufo/waves/round-93/receipts/`. No installs. No lane file was written except
this report; every mutant/weakening/neutral copy lives in `$S` and is a copy of a lane artifact.

Axes named: **C2 operability** (does the composed gate + kill-set + panel + counter catch a weakened, still-green
selftest assertion?) and **predicate fidelity** (does the counter measure the sentence the declaration froze?).
No C1 tool was read.

## 0. Artifacts reviewed (final state; C2 was a moving draft during w1)

| artifact | sha256 | note |
|---|---|---|
| `.ufo/waves/round-93/build/check-selftest-strength.c2.py` (361 ln) | `2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b` | final at 00:32; earlier `76a1d923` (326 ln) at 00:14 |
| `.ufo/waves/round-93/build/check-seat-reports-kills.c2.json` (32 kills) | `00befb3efbe2f4a7c44b14776482e0cac0ab8e219db934af9c25b34f47c516f9` | final at 00:32; earlier `ac9e4648` (20 kills) |
| `quality/counters/c2-r93-selftest-strength.py` (319 ln) | `9edfa70e062b4d1a87beae5f6566c696dac3669a16cb2e1ec93823eee89d0170` | final at 00:59; earlier `380c1d8a` (298 ln), `a28a7c71` (284 ln), `2ebf99aa` (302 ln), `30553ca0` (302 ln) |
| `.ufo/waves/round-93/controls/selftest-panel-r93.json` (16 weakenings + 6 neutrals) | `a6d2cbe2826868191f3ee980c27fcc3288bbc151ed3ceeb79ca1f11891bc4c10` | 00:34 |
| `.ufo/waves/round-93/controls/selftest-gate-mutants-r93-frozen.json` (22 mutants) | `be676929cefa46481e1ea836d29cd65152af23002e9d9dad96cf39295b88770e` | 00:38 |
| `.ufo/waves/round-93/controls/gen-c2-panel-r93.py` | `3b5024a3c09013ca1a7d97401cbd2848d822620b4be73db5f36c7317fea9afa3` | 00:34 |
| `.ufo/waves/round-93/controls/gen-c2-weakenings-r93.py` | `e9fc81ccc2a027abd2ebf62d42a2770da24a01518a46012fd23cb4372f7bf174` | 00:22; superseded by the panel generator |
| `.ufo/waves/round-93/controls/selftest-weakenings-r93.json` (30 rows, seed 76a1d923) | `c3efde501c2cf6b28d151ea9eed4db3455ff4fbd35201aac19a2c3d7e15fb41b` | **stale companion**: seed is the old gate sha |
| `.ufo/waves/round-93/controls/selftest-gate-mutants-r93.json` (19 mutants, target 76a1d923) | `cad243e8770e29c9c0fadb1e0e4f40d0e517ea55816d3dc199522ea75bddc2f7` | **stale companion**: G02 find no longer occurs in the final gate |
| `quality/check-seat-reports.py` at the base rev | `176fc066b49334921e4fd746de55db8106709c29dfe225430224c9d46ed1663a` | equals the kill-set's `tool_sha256` |

`git show 4c6f723f:quality/check-seat-reports.py | sha256sum` = `176fc066…`;
`git show 4c6f723f:quality/counters/c2-r92-gate-defects.py | sha256sum` = `0aa4d1f1…` (the counter's pin).

**Verdict.** With the final gate + 32-kill set, every gate-side leg I can test is green in DRAFT: positive
`SELFTEST_STRENGTH: OK … kills=32 held=32 survived=0 wrong_check=0` rc 0; **23/23** single-check neutralisations
`WEAK` rc 1; **10/10** hand weakenings `WEAK` rc 1; the 9 previously-unflagged fresh rows `WEAK`; the final
counter's own panel/frozen-mutant DRAFT run in §7 ends `DRAFT_TARGET_MET … neutralised_flagged=23/23 hand_flagged=16/16 neutral_ok=6/6 mutants=22 killed=22 …` rc 3 (a DRAFT verdict, not a measurement). The gate refuses every attack in its brief (§1). The
remaining findings are **freeze-integrity**, not gate defects: (1) two stale companion files remain in
`controls/` and the seat items name them — pinning the wrong pair produces `SETUP_ERROR` (§5, observed);
(2) the final gate must land byte-identically to `2d6f1219…` or the frozen mutant anchors
(G02/G13/G20/G21/G22) break; (3) the counter seat's report quotes the *older* counter and its
`DRAFT_TARGET_MISSED` line, not the final `9edfa70e…` instrument, whose DRAFT run prints `DRAFT_TARGET_MET`
(§8). The declaration drift I found (§4) was **closed during this review** by the L1's revision
`c99ee9d3…`, which adopts the counter's sentence and pins the final panel/mutants/gate/kill-set. My earlier
findings against the 00:14–00:22 bytes — kill-set 20/23, hand 4/10, fresh 11/20, counter rc-blindness — were true
of those bytes and are recorded in §2/§3/§6 with the evidence; the L1's 00:32/00:38 integration fixes them.

---

## 1. The final gate against the requested attack list (DRAFT)

Command shape: `python3 -I <gate> --tool <copy> --kills <kills.json> --scratch-root $S/<dir> --timeout 20
[--allow-sha-drift]`. All runs used the final gate (`2d6f1219…`) and the final 32-kill set (`00befb3e…`).

| attack | input | gate output | rc |
|---|---|---|---|
| positive control | unmodified tool + 32 kills | `OK tool=quality/check-seat-reports.py kills=32 held=32 survived=0 wrong_check=0` | 0 |
| crash is not a kill | `TRAILER = re.compile(` -> `TRAILER = re.compil(` | `SURVIVED crash` + `WEAK … survived=1` | 1 |
| string `must_fail` substring | `must_fail: "present -> OK rc0"` (suffix of labels 1/14) on the mutant that fails only 14 | `WRONG_CHECK k-git-size failed=['rev: present -> OK rc0']` | 1 |
| **list `must_fail` missing a label** | `x-unsafe-or` with list `["unsafe -> SR03 rc1"]` (real set has two labels) | `WRONG_CHECK x-unsafe-or failed=['unsafe -> SR03 rc1', 'rev: absolute trailer path -> SR03']` | 1 |
| **list `must_fail` superset** | same kill + `last trailer wins` | `WRONG_CHECK x-unsafe-or failed=[… two labels]` | 1 |
| empty list | `must_fail: []` | `SETUP_ERROR bad kill entry` | 2 |
| mutant inside `def selftest` | find `    results: list[tuple[str, bool]] = []` (selftest only) | `SETUP_ERROR kill inside find occurs 0 times in non-selftest code` | 2 |
| `tool_sha256` drift | sha `0…0` | `SETUP_ERROR tool sha256 mismatch …` | 2 |
| drift + `--allow-sha-drift` | same | `OK …` | 0 |
| no result cache | two kills sharing one `find`, one changing, one no-op | `SURVIVED a-noop` + `WEAK … held=1 survived=1` (each re-run) | 1 |
| timeout | tool mutant sleeping 30 s, `--timeout 2` | `SURVIVED sleep` + `WEAK … survived=1`, 2.3 s wall | 1 |
| relative `--tool` | `--tool quality/check-seat-reports.py` from the lane root | `OK …` (path absolutised in `run_selftest`) | 0 |
| **`selftest_checks` pin** | kill-set `selftest_checks: 22` vs the tool's `checks=23` | `SETUP_ERROR unmutated selftest result ['SEAT_REPORTS_SELFTEST: checks=23 failed=0'] is not checks=22` | 2 |
| checks pin matches | `selftest_checks: 23` | `OK …` | 0 |
| gate `--selftest` | — | `SELFTEST_STRENGTH_SELFTEST: checks=11 failed=0` | 0 |

Labels containing `:`/spaces (the tool's own 23 labels) parse correctly in all 32 kills; the list-exact
comparison is `sorted(fails) != sorted(must_fail)` (`gate:179-181`). The gate's own selftest grew from 8 to 11
checks and covers the list-exact, checks-pin and crash arms.

### 1.1 Gate residuals (low)

* A crash or timeout is reported as `SURVIVED` (`gate:176-178`); the direction is right (WEAK), the diagnosis is
  imprecise. Not a predicate risk.
* The verdict tag prints the kill-set's `tool` field (`gate:192-194`), not the `--tool` path; when the counter
  gates neutralised/weakened copies with `--allow-sha-drift`, the line still says
  `tool=quality/check-seat-reports.py`. The counter knows the variant id; the gate line alone does not.
* A kill whose `replace` merely prints the exact must_fail FAIL lines and exits non-zero would be `held`. The
  kill-set is a committed, sha-pinned artifact, so this is a freeze-time forgery risk, not a runtime gate hole.

---

## 2. History (fixed): the 20-kill set could not satisfy clauses (ii) and (iii) — evidence kept for the record

At 00:14–00:22 the gate was `76a1d923…` and the kill-set `ac9e4648…` (20 kills). I verified each of the 20 kills
applies exactly once outside `def selftest(` and fails exactly its `must_fail` label; all 20 were unique killers
(transcript; all 20 scored as stated). But the 20 labels covered only 20 of the 23 selftest checks:

```
missing must_fail values: "all present -> OK rc0", "unsafe -> SR03 rc1", "untrailed -> SR04 rc1"
```

Using the counter's own neutralisation transform (a `results` list subclass forcing `ok=True` for one label),
20 of 23 neutralisations printed `WEAK`, but neutralising any of the three missing labels left the gate `OK` rc 0
(transcript; the three OK labels are quoted above), i.e. `neutralised_flagged = 20/23` (predicate (ii) false). The gate seat's own report
(`.ufo/waves/round-93/w1/R93MExecGateC2.md`) documented the three as having no *unique* killer, with the reasons
I re-derived: `all present` shares every production path with `missing`/`--all`/`rev: present`; `unsafe`'s dotdot
branch is **masked** in worktree by `is_link()` -> `inside()` (removing it is an equivalent mutant: rc 0, no
fails) and has no `../` fixture in `--rev`; `untrailed` shares the `if not found` branch with `prose Report line`.
The predicate only needs *a* killer, not a unique one. Adding one non-unique killer for each (`size = tree.size(rp)`
-> `size = None`; `if unsafe(rp) or tree.is_link(rp):` -> `if tree.is_link(rp) and not rp.startswith(".."):`;
the `if not found:` block -> `found = ["x"]`) made all 23 neutralisations `WEAK` (`held=22 survived=0 wrong_check=1`).

The 20-kill set also failed the weakening legs: 4/10 hand weakenings flagged and 11/20 fresh rows flagged
(§3). The L1's 00:32 integration replaced the kill-set with **32 kills carrying exact-set `must_fail` lists**,
adopting the three killers above plus message-only, summary-only, extra-finding, duplicate-finding, ASCII-tail,
mode-summary and rc-shift mutants (the file's `note` cites R93MReviewC2 §2.3/§3.3 and R93MMutC2 §6). I verified
the result:

* all 32 kills occur once, exit rc 1, and their **fail set equals their `must_fail` list exactly**
  (0 mismatches; verified in scratch);
* the union of all `must_fail` labels is all 23 checks;
* with the final gate: **23/23** neutralisations `WEAK` rc 1 (per-label gate lines, e.g. label 1 `WEAK … held=28 wrong_check=4`, label 4 `WEAK … held=28 wrong_check=4`, label 5
  `WEAK … held=28 wrong_check=4`);
* the 10 hand weakenings are all `WEAK`: h01 31/1, h02 30/2, h03 31/1, h04 31/1, h05 31/1, h06 29/2+1,
  h07 28/4, h08 31/1, h09 31/1, h10 29/2+1 (`held/survived`, per-row gate output);
* all 20 old fresh rows are `WEAK` (the nine that were unflagged under the 20-kill set are now
  `WEAK … survived=1`).

---

## 3. History (fixed): the 00:22 weakenings — 6/10 hand and 9/20 fresh unflagged; final panel 16/16

The hand and fresh weakenings in `selftest-weakenings-r93.json` each keep `checks=23 failed=0`. Against the
20-kill set the gate flagged only h01/h05/h07/h09 (4/10) and 11/20 fresh rows; the unflagged classes were
`want_in` drops for F2/F3/F1-worktree, ids-prefix, mode comparison and ids-subset (transcripts; the 4/10 and 11/20 counts are quoted here). Root cause: the 20 kills for those checks failed for a different discriminator than the
weakening removes (e.g. `k-tok-ascii` trips `all(g.isascii())`, not the quoting `want_in`; `k-round-dedup`
duplicates the `SR01` lines, not the summary counts).

The L1's 32-kill set closes this: with it, every one of the 16 weakenings in the final panel
(`selftest-panel-r93.json`: h01–h10 plus R93MMutC2's E1/E2/E3/E4/E5/E8 escapes e01–e06) must be `WEAK`; my run
of h01–h10 is 10/10 `WEAK` (§2), and the final panel's e01–e06 are in the counter DRAFT run (§7). The 6 neutral
edits (comments, reordered cases, lambda→def, a tighter assertion, blank lines) all keep the exact result line
and must leave the gate `OK:0` — I applied all 22 panel edits to the tool, verified `checks=23 failed=0` and the
exact result line for every one, and the final counter enforces the same pre-check (`setup` on a red variant).

---

## 4. Finding 1 (high at review start; **closed during the review**): declaration/counter drift

At the start of this review the declaration draft (`claims-declaration-r93.md`, sha `917c4bbb…`) stated:

* clause (iv): "fresh: seed = first 8 hex digits of the gate's sha256 picks 20 (check, transform) weakenings
  from the frozen grammar, all flagged";
* clause (v): "every frozen gate mutant changes a verdict on (i)–(iii)".

The final counter (`quality/counters/c2-r93-selftest-strength.py:9-19`, `9edfa70e…`) implements instead:

* (iv) "every frozen **neutral edit** of the panel (a strength-preserving byte change that keeps the selftest
  green) leaves the gate at OK, exit 0 (neutral_ok == neutrals)";
* (v) "every frozen gate mutant prints a well-formed verdict line different in verdict **or exit code** from the
  measured gate's on at least one probe of (i)–(iv) **or of the frozen setup panel**" (the `setup_panel()`
  probes s01–s14: sha drift, broken tool, ambiguous find, timeout, FAIL-line/exit-0, result-line, checks pin,
  wrong-check, crash, bad entry, must-fail superset, mid-line prefix, must-fail subset, selftest rc1/failed-0).

There is no seed and no 20-draw fresh leg anywhere in the final counter; the fresh grammar was replaced by a
frozen panel of 16 weakenings + 6 neutrals. The counter's own docstring claims it is "the same sentence as the
declaration", which is false for the live declaration bytes. The receipt line also no longer matches the template
in the seat spec (`fresh=… fresh_seed=…` are gone; `neutral_ok=… crashed_not_killed=… shadiff_…` are new).
Consequence had it remained: the counter's `TARGET_MET` would have been a different claim than the
declaration's. **Closed:** at 05:0x the L1 revised the declaration to sha
`c99ee9d31239f1a793329854a031926f085ca694926d09eebc6326bdb4634d77`, whose C2 section now adopts the counter's
verbatim sentence (frozen gate/kill-set pins; hand weakenings; neutral edits; setup panel; `crashed_not_killed`),
pins `selftest-panel-r93.json` `a6d2cbe2…` and `selftest-gate-mutants-r93-frozen.json` `be676929…`, and explains
the replacement of the fresh-seed clause (it cites R93MCritic C2-F1 and this review's generator finding). The
freeze commit must carry `c99ee9d3…` or later; against the current text the counter and declaration now agree.

Secondary drift (now adopted): the counter's (v) counts a mutant that crashes the gate as `crashed_not_killed`
(not killed), a stricter, honest category recorded in the revised declaration.

---

## 5. Finding 2 (high, freeze inputs): the seat-named companion files are stale; pinning them yields SETUP_ERROR

The C2 seat item names `controls/selftest-weakenings-r93.json` and `controls/selftest-gate-mutants-r93.json` as
the inputs; both were generated against the earlier gate `76a1d923…`:

* `selftest-weakenings-r93.json` has `seed: 76a1d923`; the final gate is `2d6f1219…`.
* `selftest-gate-mutants-r93.json` has `target_sha256: 76a1d923…`; its **`G02-must-fail-ignored` find occurs 0
  times** in the final gate (the string `elif k["must_fail"] not in fails:` was replaced by the list-aware
  conditional at `gate:179-181`).

Reproduced with the pre-rewrite counter (`a28a7c71…`) and the old mutant file against the final gate:
`MADO_SELFTEST_STRENGTH: SETUP_ERROR mutant G02-must-fail-ignored: find occurs 0 times` (rc 2; the parallel
G01 mutant was applied and counted killed before the abort). The final counter (`9edfa70e…`) checks the same
condition (`gate_t.count(mu["find"]) != 1` -> SETUP_ERROR), so it has the same exposure to the stale file.

The final counter's actual inputs are `controls/selftest-panel-r93.json` (`a6d2cbe2…`) and
`controls/selftest-gate-mutants-r93-frozen.json` (`be676929…`, 22 mutants; all finds occur exactly once in the
final gate — verified). **The L1 must freeze/pin those two paths, not the stale pair**, and record the pins in the
receipt. Leaving both pairs in `controls/` without a pointer is a live trap for the freeze commit.

---

## 6. Finding 3 (fixed, recorded): counter rc-blindness in the pre-rewrite versions

The `a28a7c71…` counter measured verdict *words*, not `(verdict, rc)`: `verdict()` returned only
`OK|WEAK|SETUP_ERROR|TIMEOUT` and `run_vec()` discarded `rc`; `positive_ok = pos == "OK"`,
`neutral_flagged = sum(v == "WEAK")`. Demonstrated false greens on that version:

* `G19-rc-always-zero` (`return 1 if verdict == "WEAK" else 0` -> `return 0`): prints `WEAK` rc **0**; the
  counter counted it as flagged and its (v) vector could never differ from the base — G19 unkillable.
* A gate that prints `OK` and exits **1**: `positive_ok` was true although clause (i) required rc 0. Observed
  `SELFTEST_STRENGTH: OK … held=20` with rc 1.

The final counter fixes this: `Run.gate()` returns `f"{verdict}:{rc}"` (`counter:114-131`), and every leg
requires `OK:0` / `WEAK:1` (`met` at `counter:302-304`). `G19-rc-always-zero` is now killed by its rc
difference, and the always-WEAK stub control is judged on `weak_t != "OK:0"`. No residual action beyond §4.

---

## 7. Final counter DRAFT run (the composed claim)

The counter now requires the frozen gate/kill-set sha pins (`--expect-gate-sha256`/`--expect-kills-sha256`,
`counter:189-190`, `frozen_ok` at `:226`). Command (DRAFT, rc 3 expected; `--draft-gate`/`--draft-kills` on the
final build files, final panel and frozen mutants pinned by sha, `--rev 4c6f723f…`, `--scratch-root $S/c2run5`):

```
python3 -u -I quality/counters/c2-r93-selftest-strength.py --repo <lane> \
  --rev 4c6f723f3dca3a26f9d14475d695fe797e2e972c \
  --panel .ufo/waves/round-93/controls/selftest-panel-r93.json --expect-panel-sha256 a6d2cbe2… \
  --mutants .ufo/waves/round-93/controls/selftest-gate-mutants-r93-frozen.json --expect-mutants-sha256 be676929… \
  --expect-r92-counter-sha256 0aa4d1f1… --expect-gate-sha256 2d6f1219… --expect-kills-sha256 00befb3e… \
  --scratch-root $S/c2run5 \
  --draft-gate .ufo/waves/round-93/build/check-selftest-strength.c2.py \
  --draft-kills .ufo/waves/round-93/build/check-seat-reports-kills.c2.json --timeout 120 --workers 24
```

Individual legs, measured directly against the final gate + 32-kill set (each a DRAFT gate invocation; they are
exactly the counter's probes):

| counter leg | expected | observed |
|---|---|---|
| (i) positive | `OK:0` | `OK … kills=32 held=32` rc 0 |
| (ii) 23 neutralisations | `WEAK:1` xx 23 | **23/23** rc 1 (`wrong_check` 3–4 on most, `survived` 1) |
| (iii) 10 hand weakenings | `WEAK:1` | **10/10** rc 1 |
| (iii) 6 R93MMutC2 escapes e01–e06 | `WEAK:1` | **6/6** rc 1 (e01 29/2+1, e02 31/1, e03 31/1, e04 31/1, e05 31/1, e06 24/0+8) |
| (iv) 6 neutral edits | `OK:0` | **6/6** `OK … held=32` rc 0 |
| all 22 panel edits keep `checks=23 failed=0` + exact result line | green | **22/22** verified |
| (v) 22 frozen mutants | killed=22 | **22/22 killed**, 0 crashed_not_killed (all mutants G01–G22 `killed diff>=1`) |
| (vi) controls | do-nothing < 39, always-OK 0, always-WEAK fails (i), sha-diff fails (iv) | do-nothing 0/39, always-OK 0/39, always-WEAK `WEAK:1`, sha-diff flags 39/39 and `neutral_ok=0/6` |
| (vii) gate `--selftest` | rc 0 | ok |

Verbatim end of the run (rc 3 = DRAFT; **this is a DRAFT_TARGET_MET, not a measurement**):

```
MADO_SELFTEST_STRENGTH: DRAFT_TARGET_MET pred=PRED-C2-r93-v1 rev=draft checks=23 frozen_pin=ok
positive=OK:0 kill_set_pin=ok neutralised_flagged=23/23 hand_flagged=16/16 neutral_ok=6/6 mutants=22
killed=22 crashed_not_killed=0 do_nothing_flagged=0/39 always_ok_flagged=0/39
always_weak_positive=WEAK:1 shadiff_flagged=39/39 shadiff_neutral_ok=0/6 gate_selftest=ok
gate_sha256=2d6f1219… kills_sha256=00befb3e… tool_sha256=176fc066…
```

The control denominators are 39 = 23 neutralisations + 16 weakenings (the counter's `weak = neut + hand`); the
do-nothing instrument compares the tool's result line over the same 39 variants and flags none (every panel row
keeps `checks=23 failed=0`), which is exactly the round-92 blind spot. The composed C2 is green in DRAFT with the
final gate/kill-set/panel/frozen-mutants; the freeze blockers are §4 (declaration drift) and §5 (pin the final
pairs, land byte-identically).

---

## 8. Evidence coherence and freeze hazards

1. **The counter seat's report is stale.** `.ufo/waves/round-93/w1/R93MExecCounterC2.md` (00:33) documents the
   `a28a7c71…` counter and quotes
   `DRAFT_TARGET_MISSED … neutralised_flagged=20/23 hand_flagged=4/10 fresh=11/20 mutants=19 killed=18 …`.
   The live counter is `9edfa70e…` (319 ln), reads a different panel/mutant pair, has no fresh/seed leg and now
   requires frozen gate/kill-set sha pins; its DRAFT run prints `DRAFT_TARGET_MET` (§7), the opposite verdict to
   the report's quoted line. The L1 should have the counter seat re-run and re-quote (or mark the report
   superseded); otherwise the wave's evidence file contradicts the measured artifact.
2. **Land the gate byte-identically.** The frozen 22 mutants are anchored to `2d6f1219…` (and the kill-set's
   exact `must_fail` lists were derived on the same tool). Any edit to the gate at landing — even a docstring or
   a path — breaks `G02`/`G13`/`G20`/`G21`/`G22` anchors or the `selftest_checks`/list logic, and the counter
   aborts with SETUP_ERROR. If the gate must change, regenerate the frozen mutants (`gen-*`) and re-pin.
3. **Land the kill-set at `quality/selftest-kills/check-seat-reports.json`** with `tool_sha256 =
   176fc066…` (the tool at rev). The counter reads that path via `git show`; the build path is only for DRAFT.
4. **Pin the final pairs** (§5): `selftest-panel-r93.json` `a6d2cbe2…` and
   `selftest-gate-mutants-r93-frozen.json` `be676929…` — the revised declaration (`c99ee9d3…`) now names exactly
   these in its C2 argv. The old `selftest-weakenings-r93.json` / `selftest-gate-mutants-r93.json` remain in
   `controls/` and must not be used.
5. **The counter's generator/report names drift**: `gen-c2-weakenings-r93.py` writes the 30-row file with a
   6-row `FRESH_POOL` drawn with repetition (its docstring says no repeats; the code says "with repetition in
   seed order"). That file is now superseded by `gen-c2-panel-r93.py` / `selftest-panel-r93.json` (16+6 rows,
   no seed). Keep the generator/report consistent with the frozen panel, or a future re-run regenerates the
   wrong artifact.
6. **Run-time/budget**: the final counter's `(v)` runs 22 mutants × (1 + 22 variants + 14 setup) probes, each
   probe a full gate invocation over 32 kills; my DRAFT run with `--workers 24` took ~55 min wall on a host
   at load ≈ 297 (32 cores). The freeze-time measurement needs that wall time budgeted, or a quiet host.

---

## 9. Commands run (all DRAFT; exit codes as observed)

1. `python3 -I quality/check-seat-reports.py --selftest` -> rc 0, `checks=23 failed=0`.
2. Final gate + 32-kill set on the unmodified tool -> rc 0, `OK … kills=32 held=32`.
3. 23 neutralised tool copies (counter transform) -> rc 1 `WEAK` **23/23**.
4. 10 hand weakenings (`selftest-weakenings-r93.json` HAND and the panel's h01–h10) -> rc 1 `WEAK` 10/10.
5. 20 old fresh rows -> rc 1 `WEAK` 20/20 (including the nine that failed under the 20-kill set).
6. All 22 panel edits applied and checked green with the exact result line (`checks=23 failed=0`).
7. 32 kill replicas: 32/32 `find` once outside `def selftest(`, 32/32 rc 1, 32/32 fail set == `must_fail`
   (verified in scratch).
8. Attack battery of §1 on the final gate -> all rows as tabled.
9. Gate `--selftest` -> rc 0, `checks=11 failed=0`.
10. Pre-rewrite counter + old mutants + final gate -> rc 2,
    `SETUP_ERROR mutant G02-must-fail-ignored: find occurs 0 times` (the §5 reproducer).
11. Final counter DRAFT run (frozen gate/kill-set pins, panel + frozen mutants, `--workers 24`) -> rc 3,
    `DRAFT_TARGET_MET … neutralised_flagged=23/23 hand_flagged=16/16 neutral_ok=6/6 mutants=22 killed=22
    crashed_not_killed=0 do_nothing_flagged=0/39 always_ok_flagged=0/39 always_weak_positive=WEAK:1
    shadiff_flagged=39/39 shadiff_neutral_ok=0/6 gate_selftest=ok …` (§7).
12. `git show` pins: tool `176fc066…`, r92 counter `0aa4d1f1…`.

Scratch `$S=/fast/scratch/hyaku/mado-r93/R93MReviewC2` is deleted on exit; the per-run transcripts lived
there and are summarised in this report (the write scope names only this report file, so nothing was copied into
`w1/`). A `controls/__pycache__/` and a `build/__pycache__/` exist in the wave tree from module imports by this
review and/or the wave's seats; they are untracked and were not removed (outside this seat's write scope). No
installs; pacman was not run; no mutating git/jj ran in the lane (only `git show`).

## 10. Residual risk / verification gaps

1. The gate's kill detection is line-based; a sha-pinned kill-set entry that prints the exact must_fail FAIL lines
   without weakening production code would be held. Freeze-artifact forgery risk only.
2. The counter's setup panel is a *frozen* set of arms; like all kill-sets it is "no stronger than its panel".
   R93MMutC2's G13 is now covered by s12 (the mid-line prefix probe), but a future gate edit that changes the
   output grammar (e.g. the result-line prefix) would need panel regeneration.
3. I did not re-run the counter against a variant where a panel weakening is not flagged and a frozen mutant is
   not killed at the same time (the green path is what §7 exercises); the failure path of the final counter is
   covered piecewise by its setup panel.
4. The counter's report is the remaining document the L1 must reconcile before the freeze (§8.1); the declaration
   was already reconciled to `c99ee9d3…` during this review (§4). My review did not edit either.

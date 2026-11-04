# mado round 68 — claims declaration (frozen before any candidate data)

- lane: mado (mado-shokunin), round 68, attempt 1, hyaku run 15
- date: 2026-11-03
- lane base (pre-r68 tip): `510100c81e6cf63fec6be380c2f2f9c670f32cbc`
- pre-freeze control baseline: `.ufo/waves/round-68/control-baseline-r68.txt`
  (landed at `2ca2bec39c42770a3176989f013e8c1cbbdb7df3`, before this file)
- freeze commit: the commit that first carries this file (cited in the lesson and the report;
  never edited after launch — a correction is a new file or an appended erratum naming what it
  supersedes)
- write scope: `/home/vgpnk/Projects/shokunin/mado-shokunin` only (plus the report and
  `.ufo/l0-questions.md` on the fleet repo). No desktop probe, compositor/socket/service write,
  package transaction, `MANIFEST.json` edit or sibling-lane write is part of either claim.

## Axis posture (read before the claims)

The lane's published finite sub-axes all sit at their measured maximum at the base
(navigation 78/78, hermetic gate suite 460/460, register 8/8 groups, used-by missing=0,
ledger 108/108 — the round-67 landing receipt `.ufo/waves/round-67/landing-counters-r67.txt`),
so no published axis is distinctly lowest, as in rounds 56–67. The stagnation nudge does not
apply (the last capability entry is round 67; the gap is 0, below the window N=3 — `SCORECARD.md`
§ Saturation). Both claims therefore take **new finite denominators** declared below, not a
re-scoring of a held rule: the C1 control set's do-nothing score is 0/3 and the C2 control set's
is 1/13.

## Claim C1 — calibration: the control harness kills its own forged kill credit

**What changes.** `quality/counters/c2-r67-landing-controls.py` credits a kill from the
decision code inside `measure()`, but its hermetic selftest never runs that decision body, so a
harness that hardcodes `mr_killed = True`, `mz_killed = True` or `killed = 2` keeps a green
selftest and reports `killed=2/2` without evidence (round-67 outside spot-check routed defect 3;
`.ufo/waves/round-67/measurement-*.txt`). The round lands a successor harness
`quality/counters/c1-r68-landing-controls.py` whose `--selftest` drives the real `measure()`
body with scripted children, so a mutation of the kill-credit call sites changes the asserted
contract line, and it lands the counter that scores exactly that.

**Counting command** (run from the lane root; `REV` is the measured revision, `DIR` scratch):

```sh
python3 quality/counters/c1-r68-selfmutants.py --repo . --rev REV \
  --base-rev 510100c81e6cf63fec6be380c2f2f9c670f32cbc \
  --scratch-root DIR
```

**Frozen predicate.** At `REV` the command prints, on its last line and with exit 0:

```
MADO_R68_SELFMUTANTS: selftest=0 killed=3/3 applied=3/3 base=<n>/3 verdict=TARGET_MET rev=<REV>
```

where:

- `selftest=0` is the scored harness `quality/counters/c1-r68-landing-controls.py` extracted
  from `REV`, run with `--selftest`;
- each of the three frozen single-point recipes occurs **exactly once** in the extracted harness
  and yields a compilable mutant:

  | id | find (exact text) | replace |
  |---|---|---|
  | S1 | `mr_killed = bool(` | `mr_killed = True or bool(` |
  | S2 | `mz_killed = mz_rc != 0` | `mz_killed = True` |
  | S3 | `killed = int(mz_killed) + int(mr_killed)` | `killed = 2` |

- a mutant is **killed** iff its own `--selftest` exits nonzero (the scripted none-killed case
  expects `killed=0/2 … TARGET_MISSED`, so any forced credit changes the asserted line);
  a recipe whose target text does not occur exactly once is `applicable=no` and never counts;
- `--base-rev` is the do-nothing control: the same three recipes applied to
  `quality/counters/c2-r67-landing-controls.py` at the base rev, each surviving (selftest rc 0).

**Before** (`.ufo/waves/round-68/control-baseline-r68.txt`, at `510100c8`):
`selftest=absent killed=0/3 applied=0/3 base=0/3` rc 1 — the scored harness does not exist and,
at the same rev, all three recipes applied to the r67 harness survive its selftest (0/3).
**After:** `selftest=0 killed=3/3 applied=3/3` rc 0. Bounded score `10 × killed / 3`:
0.0000 → 10.0000.

**Limits.** Exactly these three call-site recipes on this one harness; not a claim of universal
self-test soundness or that every forged credit is now caught. The scripted children are stubs:
the real child runs are exercised separately (the real measurement at the measured revision is a
harm-watch receipt, not part of this denominator). The counter does not authenticate the harness
and does not prove the harness's own mutants are exhaustive.

## Claim C2 — operability: the standing gates read git objects only through a guarded environment

**What changes.** Twelve of the thirteen `quality/check-*.py` files that read git objects at the
base build or inherit a git environment without `GIT_NO_REPLACE_OBJECTS`, so a planted
`refs/replace` changes the bytes a gate scores (round-67 entry § "Lane instruments that read
objects through git", `corpus/knowledge/replace-ref-citation-boundaries-r67.md`; QUALITY 109).
The round repairs every unguarded reader and lands the census gate that counts the population.

**Counting command** (run from the lane root):

```sh
python3 quality/counters/c2-r68-reader-guard.py --repo . --rev REV \
  --controls .ufo/waves/round-68/controls/c2-controls.json \
  --scratch-root DIR
```

**Frozen predicate.** At `REV` the command prints, on its last line and with exit 0:

```
MADO_R68_READER_GUARD: population=20 readers=13 guarded=13 unguarded=0 controls=11/11 verdict=TARGET_MET rev=<REV>
```

where:

- population = every tracked file matching `quality/check-[^/]+\.py` at `REV` (enumerated from
  git objects, never the worktree; 20 files at the base);
- reader = the blob contains a `git` command token **and** at least one quoted verb from the
  frozen vocabulary `show, cat-file, ls-tree, rev-parse, diff-tree, log, merge-base,
  for-each-ref` (13 files at the base);
- guarded = the blob's AST constructs the string `GIT_NO_REPLACE_OBJECTS` in a dict-literal key,
  a subscript store on an env-named target, an env-named binding, a `dict()`/`update()` keyword,
  or inside an `env=` keyword value. A comment, a docstring, a bare prose mention or an unrelated
  dictionary handed to `env=` is **not** a guard (frozen control cases 6, 8, 10, 11);
- `population=20` and `readers=13` are part of the target: a repair may not shrink the
  denominator by deleting reads or dropping a gate file;
- `controls=11/11`: the frozen classification case set
  `.ufo/waves/round-68/controls/c2-controls.json` (sha256 recorded in the lesson) is scored in
  the same run.

**Before** (`.ufo/waves/round-68/control-baseline-r68.txt`, at `510100c8`):
`population=20 readers=13 guarded=1 unguarded=12 controls=11/11` rc 1 — the only guarded reader
is `quality/check-tool-ledger.py`. **After:** `guarded=13 unguarded=0` rc 0. Bounded score
`10 × guarded / readers`: 0.7692 → 10.0000.

**Auxiliary hazard probe (outside the denominator).** One repaired gate is run twice against a
scratch repo carrying a planted `refs/replace`: the base bytes must read the forged object and
the repaired bytes the real one, with the gate's clean-run verdict recorded. This samples the
repair; the census count above is the claim.

**Limits.** The census classifies committed source text, not runtime behaviour: a guard set in a
branch never taken reads as guarded; a helper that receives its env from far away is classified
by the construction, not by dataflow to the call. The guard is presence-tested (the value is not
interpreted) and does not protect a repository already rewritten, authenticate objects or prove
state truth. Twelve files are repaired; frozen per-round counters and their pinned history are
not touched.

## Control sets frozen with this declaration

| file | sha256 | cases |
|---|---|---|
| `.ufo/waves/round-68/controls/c2-controls.json` | recorded in the lesson at freeze | 11 classification cases |

The C1 recipes are frozen as the table above; the recipe target texts are quoted from committed
bytes (`quality/counters/c2-r67-landing-controls.py` at `510100c8` and the candidate draft), never
from memory (QUALITY 108; round-66 M67-1).

## Sourced claim

C2 rests on a `corpus/SOURCES.md` row opened this round: the git v2.56.0
`Documentation/git-cat-file.adoc` bytes at the tag, which define the object-read verb the census
vocabulary turns on. C1 is not a sourced claim.

## Wave plan (recorded at freeze)

One v1 wave under `scripts/hyaku/ufo-wave-policy.json` (band 8–16), `reportDir`
`.ufo/waves/round-68/w1`, ≥25 % attack seats, at most two connector seats; the L1 holds the
§3 planner seat. Items: executor repairs of the twelve gates, one executor for the harness
measurement and hazard probe, two scribes (lesson, knowledge+sources rows), one scout (source
opening and recipe-text verification), one connector (sibling prior art, assimilation screen),
two reviewers (C1 and C2 adversarial), one critic (do-nothing, separability, chronology) and
one mutation-tester (counter self-mutation). No seat commits, pushes, stages or mutates lane
git/jj state; every seat writes only inside its own seat directory and its scratch root
`/fast/scratch/hyaku/mado-r68/<seat>/`.

# mado round 31 — registration (frozen before data commit)

Steered round 31, attempt 2 (attempt 1 died pre-prompt on a Kimi 429 — no lane
work). Round 30 was already non-author admitted; this round does not rewrite
its verdict or ledger. Base for claims: `274f7355` (round-30 lane tip).
Frozen at the worktree state carrying the round-31 claim edits, before the
data commit; every measurement reads committed bytes at named revisions
(`git show REV:path`), never the worktree — except the row-fidelity gate's
`--root .` mode, which is the file's own declared read surface.

## Routed queue (from `corpus/lessons/round-30-verifier-spotcheck.md` + w1)

1. **C1 rows blind spots** (CritPredicates §a, RevC1Rows, ScribeRowAccuracy):
   the fence counts name-matches over the whole README byte stream — no
   table scope, no cell requirement. -> **C1** below.
2. **C2 bare-path/existence loopholes** (CritPredicates §b, RevC2Counter,
   CritKillRules K2, RevC2Supersede): a bare `lessons/` path passing with no
   grounding; a supersede-all line draining the denominator. -> **C2** below.
3. **C3 gate robustness** (CritPredicates §c, RevC1Fence, RevC3Gate,
   MutC3Gate, CritCausal, SentScope): symlinked ancestors, option-shaped
   revs, `--repo` silently ignored under `--root`, quotepath fragility.
   -> **C3** below (repair, not a new gate).
4. Wave dispatch surface: this L1 seat has no swarm-dispatch tool (expected
   host surface; the orchestrator dispatches prepared waves between
   rounds). This round prepares its wave under `.ufo/waves/round-31/` and
   itemizes it in the report; no dispatch claim.
5. Bounded sub-axes, measured at base `274f7355` at start and end; no
   `tools/`-byte changes beyond `check-index-rows.py` + `check-index.py` +
   `count.py` v2; no compositor/config mutation; misroot sweep at fleet
   root before the report.

## Claims (3; distinct axes; causally separable)

**C1 — coverage.** New lane-local row-fidelity gate
`quality/check-index-rows.py`: every README index row is verified as a
*table row inside the coverage map*, with >=3 non-empty cells, a resolved
note, defined S-ids, resolvable repo-relative artifact citations (globs
warn on zero matches), and Holds-vs-note word overlap >=5 (warn, not
fail). The fence never required any of that.
Kill rule: any `ERROR` finding nonzero | counter shows `errors=N` on a
control that rewrites a row outside the table / with 2 cells.
Predicate: `python3 -I quality/check-index-rows.py --selftest` exits 0
AND `--rev 274f7355` prints `errors=1` (the r26 row's 2-cell defect) AND
post-commit `--rev TIP` prints `errors=0`.

**C2 — discernment.** Superseding, lesson-grounded admissions counter v2
(`.ufo/waves/round-31/c2/count.py`); the r30 rubric's `lessons/` word +
regex presence is replaced by resolution: every grounding citation must
resolve — `file#anchor` to a GitHub-slugged heading in the *named file*,
spell form `lesson round<N> M<M>` in that file's bytes, bare
`lessons/round-<num>.md` only if the file exists and is non-empty,
`outside X` corroborates but never grounds alone. `Supersedes criteria
a-b` still drains the denominator, but `active >= ACTIVE_MIN` (30) now
bounds it.
Kill rule: any `UNRESOLVED` over an active line | `literal` fraction <
0.70 | a supersede-all line draining `active` below the floor.
Predicate: `--rev 274f7355` prints `UNRESOLVED criterion 35`
(M23-7 under `#mistakes` — the S8 mis-scoped cite) AND post-commit
`--rev TIP` prints `resolved_active=<all>` verdict `TARGET_MET`.

**C3 — operability.** Hardened `quality/check-index.py` against the
r30-routed robustness findings: `--rev` resolves once through
`git rev-parse --verify --end-of-options` so a crafted rev cannot reach a
`git show` write path; `--root` refuses symlinked `corpus/` ancestors via
realpath containment; `--repo` + `--root` is SETUP_ERROR (was silently
ignored); `--rev` with a leading `-` is rejected before any lookup.
Kill rule: any new selftest assertion failing | a mutated control
printing the same `PASS` token as the clean run.
Predicate: `--selftest` exits 0 with 12/12 assertions (was 9/9 at the
r30 repair; the 3 new assertions cover the routed findings) AND
`--rev 274f7355` and `--rev TIP` both print `indexed=43/43` — the
strengthened gate does not regress the honest measurement.

## Kill rules (verbatim, frozen)

K1 (C1): any `ERROR` line nonzero | the tool reports `errors=0` on a
row moved outside the coverage-map table or with <3 cells.
K2 (C2): any UNRESOLVED among active lines | literal < 0.70 | active <
ACTIVE_MIN on a supersede-all sweep.
K3 (C3): any of the 12 selftest assertions failing | `--rev` output
identical to a mutated control that should have been refused.

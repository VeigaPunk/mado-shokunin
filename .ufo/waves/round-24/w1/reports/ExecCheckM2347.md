# ExecCheckM2347 — registration-order check for a lane round (routed r23 defect 3: M23-4, M23-7)

Leaf executor, mado round 24 wave 1. Assignment: build `.ufo/waves/round-24/quality/check-registration-order.py`,
show RED on lane round 23 and GREEN on a constructed sandbox history, and retain the transcript in
`.ufo/waves/round-24/quality/m23-4-7-red-green.txt`.

**Verdict: built and demonstrated — RED on round 23 at exit 1 (`2e592aff` before the wave-2 attack fixtures at
`3df1062`), GREEN at exit 0 on the constructed population-first sandbox, both negative controls RED at exit 1.
No `tools/` byte was touched and no host state changed.**

## Files changed

| Path | State | sha256 / size |
|---|---|---|
| `.ufo/waves/round-24/quality/check-registration-order.py` | new, executable | `sha256:c27f474dd2e3b60ba41780589cc712acc418481358169cf0430aa7846bb75ed2`, 14609 bytes |
| `.ufo/waves/round-24/quality/m23-4-7-red-green.txt` | new evidence transcript | `sha256:7c699f7eccf24f9a488ac38e8f9a42272454c8743c26c146b74db29dd1ea19a7`, 12022 bytes |
| `.ufo/waves/round-24/w1/reports/ExecCheckM2347.md` | this report | — |
| `/fast/scratch/hyaku/mado-r24/ExecCheckM2347/{sandbox-green,sandbox-green-clone,sandbox-red-late,sandbox-repair-only}` | sandbox git histories (outside the lane) | — |

Sibling files in the same `quality/` directory (`check-receipt-provenance.py`, `red/`, `__pycache__/`,
`fixtures/`) belong to other seats and were not touched.

## What the checker does

Usage: `python3 -I check-registration-order.py --round N [--repo PATH] [--base REV] [--tip REV] [--json]`.
Stdlib only. Read-only git plumbing: `git log`, `git rev-list`, `git diff-tree`, `git show`, all with
`GIT_OPTIONAL_LOCKS=0` and no write verb. Exit 0 pass, 1 violation, 2 cannot evaluate.

- **Round window.** `BASE..TIP` ordered by `git rev-list --reverse --topo-order`. With no `--base`, the window
  starts at the parent of the oldest commit reachable from `--tip` (default HEAD) whose subject begins
  `round-N` (word boundary, so `round-23 verifier spot-check` is in round 23); `--tip` defaults to that round's
  newest named commit. A round whose oldest named commit is the root gives the whole reachable history; a
  round with no named commit and no `--base` is exit 2, so a mistyped round cannot silently scan all history.
- **tools/ change.** Any commit whose diff against its first parent adds, modifies, deletes or renames a path
  under `tools/`.
- **Registered discovery/attack population.** A commit that adds, under `.ufo/waves/round-N/`:
  - attack fixtures: `.jsonl` cases (and `.json` under `fixtures/`) in a path segment containing `attack`
    (the round-23 `w2/out/Attack*/fixtures/*.jsonl` form);
  - `carry/` or `frozen/` population at the first or second path segment, with case files plus a manifest
    (`manifest*`, `expected*`, `registration*`, `readme*` in .json/.md/.txt) added in the same commit;
  - `repair/` population under the same case+manifest rule **only when the manifest declares a discovery or
    attack population** (contains `discovery` or `attack`). A repair-target set is not an independent
    discovery population — this is the interpretation that makes the routed r23 defect visible.
  Nested wave trees (a `snapshot` segment or a `.ufo` segment below the round root) are ignored as copied
  data.
- **Comparison.** Violation iff the earliest tools/ commit strictly precedes the earliest population commit,
  or a tools/ commit exists with no population. A population landing in the same commit as the first tools/
  change does not strictly precede it; the checker passes with a note (round 18 is such a case).

## Evidence (retained in `m23-4-7-red-green.txt`)

Commands were run with `GIT_*` unset, from `/home/vgpnk/Projects/shokunin/mado-shokunin`.

1. **RED — lane round 23**, command
   `python3 -I .ufo/waves/round-24/quality/check-registration-order.py --round 23 --tip 8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122`
   - window `e33ea30..8e5d936`, 11 commits;
   - first tools change `2e592aff` (2026-10-22T08:49:38-03:00, `tools/mado-tripwire.py`);
   - first registered discovery/attack population `3df1062` (2026-10-22T09:12:32-03:00, kind
     `attack-fixture`, the AttackEscapeGate/AttackFrameScopes/AttackLateCell/AttackPerf fixtures that arrived
     with the wave-2 receipts and the withdrawal);
   - ignored population `6b383c4` kind `repair` — `manifest declares a repair set, not a discovery/attack
     population` (round-23 `repair/expected.json`, schema `mado-r23-repair-set-v1`, names neither word);
   - later tools changes `03227dd`, `3df1062`; later population `fa819d5`; **exit 1**.
2. **GREEN — constructed sandbox** `/fast/scratch/hyaku/mado-r24/ExecCheckM2347/sandbox-green`, run through
   its clone `sandbox-green-clone`: commit 1 adds `.ufo/waves/round-99/carry/{manifest.json,fixtures/RegressionA.jsonl}`
   plus `registration.md`; commit 2 adds `tools/detector.py`. Checker output: population `0903be2` precedes
   tools `f16afaf`; **exit 0**.
3. **Negative control, tools first** (`sandbox-red-late`): tools `e6a2799` precedes carry population `7e04d0a`;
   **exit 1**.
4. **Negative control, repair-only** (`sandbox-repair-only`): repair set `987aeed` (expected.json + fixture)
   precedes tools `665a617`, but the manifest declares no discovery/attack population, so
   `first-registered-discovery-attack-population=none` and **exit 1** — the round-23 arm reproduced in
   miniature.
5. **Current lane round 24**: window `5bb2c87..81955bd`, 6 commits, no tools/ change → **exit 0** (vacuous;
   the round-24 registration keeps `tools/` untouched).
6. **Guard**: `--round 77` with no matching named commit and no `--base` → error and **exit 2**.

The transcript also records the full ordered round-23 commit list, python/git versions (Python 3.14.8, git
2.56.0), the checker sha256 labeled `sha256:`, and the sandbox `git log --name-status` of each commit.

## Observations vs inference

- Observed from git bytes: the commit order above; the file classes each commit adds; the manifest contents
  used to reject the repair population; the sandbox histories; the exit codes.
- Inference/interpretation: that a repair-target set is not a "discovery/attack population" (supported by
  round-23 registration language and by M23-4/M23-7, but it is a definition, not a byte-level fact); that
  path class plus manifest is a sufficient registration test. Both are stated in the checker docstring.
- Not established: whether any registered fixture is a meaningful discovery attack, whether a population was
  executed against the base, or anything about production classifier behaviour. Committed history only —
  uncommitted work-tree fixtures are invisible. Ordering is topological, not commit-date.

## Scope checks on earlier rounds (read-only, not part of the receipt)

The same rule run on historical rounds: 13 RED, 18 GREEN only because population and tools change share
commit `4c103b5` (same-commit note), 19 RED (`df84807` precedes `01b8094`), 21 RED (`843d301` before any
registered population), 22 RED (`330de68`). Round 13's `frozen/` holds scripts plus `expected.json` and no
`.jsonl`/`.json` cases, so it is invisible to the case-file arm — old-round fixture forms are a known limit.

## Boundaries, tooling, residual risk

- No lane writes beyond the two files above; no git/jj write commands in the lane or fleet repo; all sandbox
  git work happened under `/fast/scratch/hyaku/mado-r24/ExecCheckM2347/` with `GIT_DIR`, `GIT_WORK_TREE`,
  `GIT_INDEX_FILE` and all other `GIT_*` variables unset. No host state, package or compose change; no
  `hyprctl` verb was needed. No tool installs or updates.
- Risk: path-class heuristics under-detect populations stored in other naming schemes (round 13 form) and
  over-accept an attack-named `.jsonl` that is not a real case; the manifest requirement keeps `carry/`,
  `frozen/` and `repair/` honest. Same-commit registration passes by the literal "precedes" rule; a stricter
  reading would need a spec change, not a code change.
- Blockers: none.

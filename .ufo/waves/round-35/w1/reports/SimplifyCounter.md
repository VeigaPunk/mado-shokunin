# SimplifyCounter — round-35 w1 report

Scope: propose the shortest `count.py` preserving the nine live clauses and the
PRED-C1-r35-v1 predicate. Proposal only; committed counter untouched.

## Deliverable

- `.ufo/waves/round-35/scratch/SimplifyCounter/count-min.py` — 104 lines vs 218,
  runnable, same CLI/exit contract.
- `.ufo/waves/round-35/scratch/SimplifyCounter/analysis.md` — clause map, drop list,
  per-drop safety argument, residual divergences.

## What drops (headline)

- Dead weight: `hashlib`/`digest` (computed, never read), `import os`,
  `__future__`, `rows_for`/`gate_quote`/`valid_recheck` helpers (folded inline),
  three separate recheck regexes → one alternation.
- Out-of-scope defence: `MAX_BYTES` chunked cap, `nlink != 1`, explicit `S_ISLNK`
  branches (subsumed by `lstat`+`S_ISDIR`/`S_ISREG`), `O_NOFOLLOW` (declared
  non-load-bearing in `c1/clauses.json`), root-symlink gate.
- Each drop is safe because no clause or control names it, and the predicate's own
  words still cover the residual case. Residual divergences (symlinked root,
  hardlinks, >8MB files, merged drift message) are enumerated in analysis.md —
  none is clause-visible.

## Evidence

Committed counter: `.ufo/waves/round-35/c1/count.py` at
`19e4ab3171c1540c40d6b12097745af98053b07d` (ancestor of HEAD, verified
`git merge-base --is-ancestor`).

Differential run (re-executed at write time):

```
for d in .ufo/waves/round-35/controls/*/ plus .txt-misses and --root .:
  SAME 21/21 — stdout and exit code identical.
  golden:            exit 0  TARGET_MET   (closed_entries=3 closed_rows=8 open_cites=0)
  10 c1 control dirs: exit 1 TARGET_MISSED (closed_entries=2 closed_rows=7 open_cites=1)
  .txt + lane root .: exit 1 TARGET_MISSED (closed_entries=0 closed_rows=0 open_cites=8)
  drift/missing/usage: exit 2 in all three cases
```

All nine live clauses traced to minimal expressions in analysis.md; every
short-circuit order preserved (`len(cs)==11` before `cs[10]`, `len(qs)==1` before
`qs[0]`, `blob is not None` before `in blob`).

## Recommendation

Adopt `count-min.py` shape only if the lane wants defence-in-depth removed; the
drops are all outside the predicate's nine clauses but three of them (nlink,
MAX_BYTES, root-symlink) encode extra strictness the protocol tolerates losing.
Safest subset if partial adoption is preferred: the dead-weight group alone
(hashlib/digest, os, __future__, helper folding) — zero observable change on
every tree, including exotic ones.

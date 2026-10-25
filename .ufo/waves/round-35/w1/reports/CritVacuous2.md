# CritVacuous2 — can PRED-C2-r35-v1 be satisfied without the r34 repairs?

**Verdict: yes — the counter measures self-authored documents, not repairs.** All four
observables (`uncovered`, `retired`, `toctou_declared`, `ledger_tip_ok`) count what the
lane *wrote*, never whether the referents are real. `TARGET_MET` is reachable with zero
r34 repair artifacts. Attempts under `.ufo/waves/round-35/scratch/CritVacuous2/`.

## What the counter actually consumes (`c2/count.py` lines 58–124)

- Drift check covers exactly two fields: `predicate` string and `target` dict.
  `clause_ledger`, `blob_ledger`, `toctou_clause`, `r34_tip`, `frozen_blobs` are read
  from whatever `--frozen` file is passed — patching any of them is **not** detected.
- `uncovered`: a clause is covered by `not-load-bearing` with any non-empty `reason`
  (content unvalidated), or by `control.receipt` pointing at any file containing the
  regex `verdict=TARGET_MISSED`. The receipt is a text claim — no re-execution, no
  hash pin, `control.tree` never read.
- `retired`: any listed id absent from `live` counts. Retirement is a string set, not
  a fact about the r34 counter.
- `toctou_declared`: `declared == [spec["toctou_clause"]]` — the only fence on the
  escape hatch. Exactly one declaration, and the *id* is spec-checked; the
  declaration's truth is not.
- `ledger_tip_ok`: substring match of `r34_tip` in the ledger doc, then `git rev-parse
  <tip>:<path>` re-verifies against **`frozen_blobs` in the spec** — the ledger doc's
  own table is never parsed. Real check, wrong referent.
- `--repo` need only sit inside a git worktree; `git -C` walks up to the lane root.

## Attempts

### A — vacuous ledger + tip-named-only blob doc (real repo)

`a-frozen.json` = committed spec with `clause_ledger`/`blob_ledger` re-pointed at
scratch. `a-clauses-vacuous.json`: one live clause `o-nofollow-open` declared
not-load-bearing for reason "Because I said so", one retired id `anything-absent-from-live`.
`a-blob-names-tip-only.md`: one line naming `dff3941…`, plus a deliberately false
`deadbeef` blob table — ignored. Real `frozen_blobs` kept, so the seven blob ids
*did* re-verify at the tip.

```
PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET
exit=0
```

Repairs performed: none. Real blob ids happen to pass, but the clause/retire/toctou
claims are pure assertion.

### B — blunt move: declare every clause not-load-bearing

`b-clauses-all-declared.json`: all 10 real clauses carry `not-load-bearing` with a
reason. Result:

```
PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=0 ledger_tip_ok=1 verdict=TARGET_MISSED
exit=1
```

The uniqueness fence (`declared == ["o-nofollow-open"]`) kills it — the one clause in
PRED-C2 that is not vacuous under a self-authored spec. It bounds the escape to a
single declaration, and the id is pinned to the spec — but any *self-authored* id
satisfies a doctored spec (see C).

### C — fully fake repo, zero real artifacts

`tree/` = an empty scratch dir treated as `--repo` (git walks up to the lane root).
`c-frozen.json`: `toctou_clause` doctored to `decoy-clause`, `frozen_blobs` emptied
(`ok=True` vacuously — the tip-named-only-ledger example, complete), ledger paths
pointed at scratch files. `tree/receipts/forged.txt` is a hand-typed
`verdict=TARGET_MISSED` string with no control tree behind it.

```
PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET
exit=0
```

Every artifact fake; spec integrity fields doctored freely; `git rev-parse` never even
invoked. TARGET_MET with no repairs, no controls, no receipts run.

## Clause ledger

| observable | bindable to fact? | how it's satisfied vacuously |
|---|---|---|
| `uncovered` | no | self-authored ledger; any `reason` string; forged receipt text |
| `retired` | no | any id absent from `live` |
| `toctou_declared` | partially — count and spec-id bound | satisfied by one arbitrary declaration; bindable only because spec pins the id |
| `ledger_tip_ok` | partially — `frozen_blobs` re-verification is real | ledger doc unparsed; empty `frozen_blobs` vacuates it; substring-naming suffices |

## Conclusion

PRED-C2-r35-v1's drift guard protects the *text* of the predicate and target, not the
*referents* of the spec fields. The committed run prints TARGET_MET because the lane
authored honest artifacts; the counter cannot distinguish honesty from attempt C's
wholesale fabrication. The non-vacuous residue: (1) `toctou_declared`'s exact-one
fence catches the blunt declare-everything attack when the *committed* spec is used;
(2) `frozen_blobs` blob-id re-verification at the r34 tip is a real git check — but it
verifies the spec's list, not the ledger's claims, and a doctored spec empties it. The
argument stands: satisfiable without the r34 repairs.

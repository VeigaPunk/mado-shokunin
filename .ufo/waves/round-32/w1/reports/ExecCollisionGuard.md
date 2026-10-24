# ExecCollisionGuard — round-32 w1 · id-collision guard (scratch)

Scope: operator item-10 guard for the pending append of
`/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md` into
`corpus/SOURCES.md`. Ran BEFORE any append. Working dir for all artifacts:
`.ufo/waves/round-32/assimilation/`. Nothing written into the lane registry or
into `/home/vgpnk/Projects/shokuknow/merge/mado/`.

## Verdict

**COLLISIONS: 0 — append is green to proceed.** No renumber map required.

- Registry ids (`reg-ids.txt`): 185 ids, S001–S185, contiguous, no gaps, no duplicates.
- Staged ids (`staged-ids.txt`): 132 ids, S186–S317, contiguous, no gaps, no duplicates.
- Intersection (`collisions.txt`): empty. Staged range starts exactly where the
  registry range ends +1 (S186 vs registry max S185).

## (1) Real check — commands run

Extractor (spacing-tolerant, census-compatible — accepts 0–3 leading spaces):

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <file> | grep -oE 'S[0-9]+' | sort
```

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > assimilation/reg-ids.txt
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > assimilation/staged-ids.txt
comm -12 assimilation/reg-ids.txt assimilation/staged-ids.txt > assimilation/collisions.txt
```

Observed:

```
185 reg-ids.txt
132 staged-ids.txt
  0 collisions.txt
```

Collision count: **0**.

Contiguity/dup sanity (run after extraction, same files): registry sort -u
= 185 ids, first 1 last 185, no gaps; staged sort -u = 132 ids, first 186 last
317, no gaps; `uniq -d` empty on both.

## (2) Guard proof — scratch fixture, proven able to fail

Fixture `guard-proof-registry-fixture.md` carries an **indented** row
(`  | S002 | ...` — two leading spaces) whose id the staged fixture
(`guard-proof-staged-fixture.md`) also contains at column zero.

Same pipeline, two extractor variants:

| extractor | pattern | reg ids seen | collisions file |
|---|---|---|---|
| tolerant (0–3 spaces) | `^ {0,3}\|[[:space:]]*S[0-9]{3,}` | S001 S002 S003 | `guard-proof-collisions-tolerant.txt` = `S002` (NON-EMPTY) |
| column-zero only | `^\|[[:space:]]*S[0-9]{3,}` | S001 S003 (S002 missed) | `guard-proof-collisions-col0.txt` = 0 bytes (EMPTY) |

Result: the naive column-zero pattern produces a FALSE-GREEN on a real
indented collision; the 0–3-space pattern catches it. Guard proven able to
fail. Fixture and both outputs committed alongside this report in
`.ufo/waves/round-32/assimilation/`:

- `guard-proof-registry-fixture.md`
- `guard-proof-staged-fixture.md`
- `guard-proof-reg-ids-tolerant.txt`
- `guard-proof-staged-ids-tolerant.txt`
- `guard-proof-collisions-tolerant.txt` (contains `S002`)
- `guard-proof-reg-ids-col0.txt` (S001, S003 — indented S002 absent)
- `guard-proof-collisions-col0.txt` (empty)

## (3) Renumber map

Not applicable — `collisions.txt` is empty. No staged id claims an existing
registry id; no renumber proposed.

## Boundary note

Registry max is S185; staged opens at S186. The staged set was evidently
numbered against this registry head. If the registry gains any row before the
append lands, this check MUST be re-run — the green is only valid for the
registry state at extraction time (S001–S185).

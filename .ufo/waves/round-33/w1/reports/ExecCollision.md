# ExecCollision — round-33 w1 · id-collision re-check (scratch)

Re-run of the round-32 `ExecCollisionGuard` id check for the pending append of
`/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md` into
`corpus/SOURCES.md`. Working dir for all artifacts:
`.ufo/waves/round-33/scratch/ExecCollision/`. Nothing written into the lane
registry or into `/home/vgpnk/Projects/shokuknow/merge/mado/`. Re-run was
mandatory: the registry has changed since the round-32 green (max was S185;
it is now S196).

## Verdict

**COLLISIONS: 5 — S186, S187, S188, S189, S196.** Those staged rows already
exist as committed registry rows; appending them again would create duplicate
ids. They must be skipped (or the append filtered) before merge.

**Target ids:** `S190` NO collision · `S191` NO collision · `S197` NO
collision — all three are staged-only, absent from the registry.

- Registry ids (`reg-ids.txt`): 190 ids, S001–S196, no duplicates, but no
  longer contiguous — S190–S195 are absent (partial out-of-order adoption of
  the staged set since round 32).
- Staged ids (`staged-ids.txt`): 132 ids, S186–S317, contiguous, no duplicates.
- Intersection (`collisions.txt`): `S186 S187 S188 S189 S196`.

Delta vs round-32 (`.ufo/waves/round-32/w1/reports/ExecCollisionGuard.md`):
then 185 registry ids / 0 collisions. The five new registry rows S186–S189 +
S196 are exactly the five new collisions.

## (1) Real check — commands run

Extractor (spacing-tolerant, census-compatible — accepts 0–3 leading spaces):

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <file> | grep -oE 'S[0-9]+' | sort
```

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > reg-ids.txt
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > staged-ids.txt
comm -12 reg-ids.txt staged-ids.txt > collisions.txt
```

Observed (run 2026-10-24, in `.ufo/waves/round-33/scratch/ExecCollision/`):

```
190 reg-ids.txt
132 staged-ids.txt
  5 collisions.txt
```

`collisions.txt` content:

```
S186
S187
S188
S189
S196
```

Sanity: `head -1`/`tail -1` reg = S001/S196, staged = S186/S317; `uniq -d`
empty on both files. Per-target grep counts: S190 reg=0 staged=1 collision=0;
S191 reg=0 staged=1 collision=0; S197 reg=0 staged=1 collision=0.

## (2) Guard proof — scratch fixture, proven able to fail

Fixture `guard-proof-registry-fixture.md` carries an indented row
(`  | S002 | ...` — two leading spaces) whose id the staged fixture
(`guard-proof-staged-fixture.md`) also contains at column zero.

Same pipeline, two extractor variants:

| extractor | pattern | reg ids seen | collisions file |
|---|---|---|---|
| tolerant (0–3 spaces) | `^ {0,3}\|[[:space:]]*S[0-9]{3,}` | S001 S002 S003 | `guard-proof-collisions-tolerant.txt` = `S002` (NON-EMPTY, 5 bytes) |
| column-zero only | `^\|[[:space:]]*S[0-9]{3,}` | S001 S003 (S002 missed) | `guard-proof-collisions-col0.txt` = 0 bytes (EMPTY) |

Result re-proven on this run: the column-zero pattern produces a FALSE-GREEN
on the indented collision; the 0–3-space pattern catches it. Fixture and both
outputs in `.ufo/waves/round-33/scratch/ExecCollision/`:

- `guard-proof-registry-fixture.md`, `guard-proof-staged-fixture.md`
- `guard-proof-reg-ids-tolerant.txt`, `guard-proof-staged-ids-tolerant.txt`
- `guard-proof-collisions-tolerant.txt` (contains `S002`)
- `guard-proof-reg-ids-col0.txt` (S001, S003 — indented S002 absent)
- `guard-proof-staged-ids-col0.txt`
- `guard-proof-collisions-col0.txt` (empty)

## (3) Renumber map

Required for the five colliding staged rows if their content must land under
new ids — but S186–S189/S196 are already committed in `corpus/SOURCES.md`
(partial adoption since round 32), so the correct action is to **skip** those
staged rows, not renumber them. The non-colliding staged ids (S190–S195,
S197–S317) can append verbatim; target ids S190, S191, S197 specifically are
green.

## Boundary note

Registry is no longer contiguous (S190–S195 absent while S196 is present);
that is the shape of the in-progress adoption, not a defect in this check.
This green for S190/S191/S197 is valid only for the registry state at
extraction time (2026-10-24, 190 rows, max S196). Any further append before
merge invalidates it — re-run.

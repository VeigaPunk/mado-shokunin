# ExecCollision — id-collision guard re-proof (mado round 34, wave 1)

Seat: executor ExecCollision. Scope: re-prove the 0–3-leading-space id extractor
(round-34 prompt §10 assimilation contract, verbatim command block) against the real
registry/package pair, then falsify the column-zero-only variant on an indented fixture.

Verdict: **guard holds.** Real pair yields 2 collisions (S201, S202). Both indented
fixtures: 0–3-space extractor NONEMPTY, column-zero extractor EMPTY. Both fixture
registries census-validate exit 0 — the census parser itself accepts indented rows,
so the extractor's tolerance is required, not optional.

## 1. Real pair — extractor as given by the round-34 prompt

Command (verbatim, output dir = `scratch/ExecCollision/` per this seat's prompt):

```sh
S=/home/vgpnk/Projects/shokuknow
A=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-34/scratch/ExecCollision; mkdir -p "$A"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md \
  | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$S/merge/mado/SOURCES.append.md" \
  | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"
```

Outputs:

- `reg-ids`: **192** ids — S001–S189 contiguous, then S196, S201, S202.
- `staged-ids`: **140** ids — S197–S336 contiguous.
- `collisions` (**count = 2**):

  ```
  S201
  S202
  ```

Nonempty → per prompt, the staged ids collide with the live registry (the registry
moved after the package was built; S201/S202 were claimed in-registry between
package build and this round). Any append from this package must renumber those two
in scratch before it touches the registry — the guard correctly blocks a naive append.

Artifacts: `.ufo/waves/round-34/scratch/ExecCollision/{reg-ids,staged-ids,collisions}`.

## 2. Indented fixture A — literal prompt fixture (`  | S002 |`)

Census-valid scratch registry `fixture-a/registry.md` (table header + S001 at column
zero + `  | S002 | ` with two leading spaces; staged set = `S002,S197`):

```
$ sources-census.sh validate --file fixture-a/registry.md
file	W03	S001 mined but unused
file	W03	S002 mined but unused
file	ok	.../fixture-a/registry.md
exit 0
```

Extractor runs (same pipeline, `^ {0,3}` vs `^`):

```
reg-ids-03:      S001          collisions-03:      S002        (1 line — NONEMPTY)
                 S002
reg-ids-col0:    S001          collisions-col0:    <empty>     (0 lines — EMPTY)
```

Column-zero extractor silently drops the indented row → false-green; the row the
census accepts would have slipped a duplicate id into the registry.

## 3. Indented fixture B — same proof against the real staged set

`fixture-b/registry.md` identical shape, indented `  | S201 |`; staged set = the real
`staged-ids` (140 ids). Census exit 0 (same two W03 warnings).

```
reg-ids-03:      S001          collisions-03:      S201        (1 line — NONEMPTY)
                 S201
reg-ids-col0:    S001          collisions-col0:    <empty>     (0 lines — EMPTY)
```

The false-green is not fixture-specific: an indented S201 — which collides in the
real pair — is invisible to the column-zero pattern and caught by the 0–3-space pattern.

## 4. Deviation note

The seat prompt says the indented `  | S002 |` row's id "is in the staged set". S002
is **not** in this lane's real `staged-ids` (S197–S336); the prompt's fixture text
predates the mado package. Fixture A reproduces the literal fixture with a staged set
containing S002 (as the proof intends); fixture B re-proves the same point with an
id that collides in the real pair. Prior round-34 attempt used S197 the same way
(`assimilation/indented-fixture.md`).

## Artifacts

`.ufo/waves/round-34/scratch/ExecCollision/` — `reg-ids`, `staged-ids`, `collisions`,
`fixture-a/{registry.md,staged-ids,reg-ids-03,reg-ids-col0,collisions-03,collisions-col0}`,
`fixture-b/{registry.md,reg-ids-03,reg-ids-col0,collisions-03,collisions-col0}`.

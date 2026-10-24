# MutC3Gate — mutation test of `quality/check-index.py` (round 30, C3)

Scope: report-only. All mutation ran in a throwaway clone
`/tmp/mutc3gate` (git clone of the lane at `92d3c86`); the lane repo, its
jj/git state and every committed byte were read-only. No installs.

## Setup (measured, not assumed)

- Gate blob is identical at freeze and tip:
  `git rev-parse 451e8b3:quality/check-index.py 92d3c86:quality/check-index.py`
  → `df01b20fa2c45ddee954da1841e2519f7e7abd4d` twice; sole commit touching it
  is `451e8b3` (the freeze commit). Working-tree sha256 (pristine)
  `fc4a10a223cea2538b367f44ecff6f924e47ff3d595e0538a33b98ac20e43d71`.
- Frozen fence regex (SCORECARD.md "Counting command", lines 78–88):
  `^\| \`knowledge/([^`]+\.md)\`` — column-0 pipe + one literal space.
  The gate's regex is `^\|\s*\`knowledge/([^`]+\.md)\`` (one extra `\s*`
  latitude; latent divergence, see F1b).
- Detector (`/tmp/mutc3gate-detector.sh`, files kept in
  `/tmp/mutc3gate-det/`): the 6-case `--selftest`, then
  `--rev 8f51071b` (base), `--rev 446dc396` (data), `--rev 92d3c86` (tip),
  then three supplementary probes outside the selftest:
  A = indented `  | \`knowledge/a.md\`` row; B = member symlink
  `knowledge/link.md -> real.md` (both indexed); C = dangling
  `knowledge` dir symlink (selftest case-5 shape).

Pristine baseline (all probes must be interpretable; none failed):

Note: lane HEAD advanced from `92d3c86` to `d72243e` (integrator spot-check
commit) while this item ran. Gate blob is unchanged (`df01b20f…`), the
`corpus/README.md` row set is unchanged at the new tip (fence 43 = gate 43 =
mutant1 43; `dup_rows=[]`; no indented rows), and pristine prints
`MADO_INDEX: rev=origin/master indexed=43/43 missing=0 dangling=0
duplicates=0 coverage=10.0000/10` exit 0 there. Every mutant's rev-mode
output is therefore invariant across the new tip as well.

```text
## selftest      MADO_INDEX_SELFTEST: 6/6 assertions passed              exit=0
## rev 8f51071b  indexed=41/43 missing=2 dangling=0 duplicates=0 coverage=9.5349/10  exit=1
                 missing: knowledge/mutation-testing-r28.md
                 missing: knowledge/workspace-rules-r27.md
## rev 446dc396  indexed=43/43 missing=0 dangling=0 duplicates=0 coverage=10.0000/10 exit=0
## rev 92d3c86   indexed=43/43 missing=0 dangling=0 duplicates=0 coverage=10.0000/10 exit=0
## probe A       indexed=0/1 missing=1 … exit=1   (indented row NOT counted)
## probe B       REFUSED: non-regular member …/knowledge/link.md exit=1
## probe C       REFUSED: non-regular member …/corpus/knowledge   exit=1
```

## Mutants and verdicts

| # | Mutation (behaviour-bearing point) | Gate sha256 (mutant) | Selftest | base 8f51071b | data 446dc396 | tip 92d3c86 | Probes A/B/C | Verdict |
|---|---|---|---|---|---|---|---|---|
| M1 | `ROW_RE` `^\|\s*` → `^\s*\|\s*` (leading-space row parses) | `f670828799764a3b9bfc938df7135e820f6fe7528c616c9c419640e19ff304de` | 6/6, exit 0 | unchanged (41/43, exit 1) | unchanged (43/43, exit 0) | unchanged (43/43, exit 0) | A **red→green** (`indexed=1/1`, exit 0); B, C unchanged | **SURVIVED** |
| M1b | `ROW_RE` `^\|\s*` → `^\| ` (fence-literal strict; answers the `^\| ` vs `^\s*\|` axis from the tight side) | `45a8e5dae97a0f427baca2a6eb66f1d72336e70f1d94f21802358dec731f21bf` | 6/6, exit 0 | unchanged | unchanged | unchanged | A/B/C unchanged | **SURVIVED** (equivalent on every available input) |
| M2 | `duplicates = sorted(p for p, n in counts.items() if n != 1)` → `duplicates = []` (duplicate detection removed) | `c52e22c06d22cf931f780cdb4a368a0f62ff5fde4d17ee80659c10781a556985` | `MADO_INDEX_SELFTEST: 5/6 assertions passed`, `FAILED: duplicate row exits 1 and names the note`, exit 1 | unchanged | unchanged | unchanged | A/B/C unchanged | **KILLED** (selftest case 4) |
| M3a | `--root` symlink test demoted behind isfile: `os.path.islink(p) or not os.path.isfile(p)` → `os.path.islink(p) and not os.path.isfile(p)` (both the kdir/rpath loop and the member loop) | `9054b5d82043368b57552d0b4b6f7fdb7022a274029102c13c3e1f7215f0a319` | 6/6, exit 0 | unchanged | unchanged | unchanged | B **REFUSED→green** (`indexed=2/2`, exit 0 — symlink followed and counted); A, C unchanged | **SURVIVED** |
| M3b | islink checks deleted from `load_root`, `not os.path.isfile` alone governs (rpath setup-error check kept) | `c557ac39556b2243b49950daf9b764e4c42bf42f3067008898f2231a1d21b783` | `5/6`, `FAILED: symlink member refused with exit 1`, exit 1 | unchanged | unchanged | unchanged | C **REFUSED→green** (`indexed=0/0`, exit 0); B **REFUSED→green** | **KILLED** (selftest case 5) |

Sample mutant outputs (full receipts in `/tmp/mutc3gate-det/*.txt`):

```text
M2-no-duplicates.txt
MADO_INDEX_SELFTEST: 5/6 assertions passed
FAILED: duplicate row exits 1 and names the note
exit=1
## rev base 8f51071b … indexed=41/43 missing=2 … exit=1   (unchanged)
## rev data 446dc396 … indexed=43/43 … exit=0              (unchanged)

M3a-symlink-after-isfile.txt
MADO_INDEX_SELFTEST: 6/6 assertions passed
## probe B → MADO_INDEX: root=…/symlink-real indexed=2/2 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
exit=0                       # pristine: REFUSED, exit 1

M1-permissive-anchor.txt
## probe A → MADO_INDEX: root=…/indent indexed=1/1 … exit=0   # pristine: indexed=0/1, exit=1
```

## Kill accounting

- Killed by `--selftest`: M2 (case 4), M3b (case 5). 2/5.
- Killed by the revision predicate (base/data/tip): **0/5**. Every mutant
  prints the exact registered strings `indexed=41/43 … exit 1` at base and
  `indexed=43/43 … exit 0` at data/tip. The revision checks carry no
  mutation-detection power for any of the three fault classes.
- Survived everything: M1, M1b, M3a. M1 and M3a are genuine capability
  defects (they break a claimed refusal/row-set semantic, not just an
  internal detail); M1b is a tolerance tightening with no observable
  difference.

## Findings (coverage, not contract changes)

- **F1 — the row anchor is unpinned (M1 survives).** No selftest case has a
  leading-whitespace row, and no committed README row is indented, so
  `^\s*\|` passes 6/6 and both revisions. The gate's own docstring and the
  C3 capability row claim "the frozen fence's row-set semantics"; the fence
  counts 0 rows on probe A (`fence_matches=0`), mutant M1 counts 1.
  Proportionality: an indented row is a list/blockquote member, not a
  column-0 table row — accepting it makes the gate greener than the fence.
- **F1b — live (latent) divergence already present in pristine.** Gate regex
  `^\|\s*` vs fence `^\| `: a row `` |`knowledge/x.md` `` (no space) would be
  counted by the gate, not by the fence. No such row exists at `8f51071b` or
  `446dc396` (regex counts 41/41 and 43/43 under both), so C3's measurements
  are unaffected today; the latitude is unmeasured, not proven safe.
- **F2 — case 5 pins only the dangling-dir shape (M3a survives).** Case 5
  symlinks the *knowledge directory* to `/nonexistent`, so
  `os.path.islink(p) and not os.path.isfile(p)` still refuses. A symlink to a
  *regular note* (`knowledge/link.md -> real.md`) is then silently accepted
  and counted (`indexed=2/2`, exit 0), contradicting the docstring ("regular
  files only — symlinked or non-regular members are REFUSED") and the C3
  capability row ("refuses non-regular members"), which is exactly the
  reported-field-evidence / tautology class the round-29 lesson warns about.
- **F3 — duplicate detection is selftest-only protected (M2 killed, narrowly).**
  Because `duplicates=0` at both measured revisions, the registered predicate
  cannot see removal of duplicate detection; only case 4 kills it. A future
  gate run at a revision with a repeated row would print
  `duplicates=0` and exit 0 under M2.
- **F4 — M3b's kill is via exit code, not via the member path.** Dropping
  islink converts case 5 from REFUSED/1 to `indexed=0/0`/0, so the assertion
  dies, but the same mutant also passes probe B; case 5 discriminates
  "dangling dir" from "refusal semantics", not symlink refusal per se.

No contract, registration, corpus, counter or gate byte was changed; the
survivors are reported as coverage findings only. Suggested (not applied)
selftest additions for a future round: (7) indented row must not be counted;
(8) `knowledge/<name>.md` symlink to a regular note must be REFUSED.

### Addendum — pristine (non-mutant) fence divergence, measured both ways

Corroborating RevC1Fence's regex-superset note with fixtures (pristine gate,
frozen fence regex `^\| \`knowledge/([^`]+\.md)\``):

```text
fixture `nospace`    README row `|`knowledge/a.md` | …`  (no space after pipe)
  gate  : indexed=1/1 missing=0 dangling=0 duplicates=0 exit 0
  fence : indexed=0/1 missing=1 dangling=0 duplicates=0 exit 1
fixture `dupdiverge` rows `| `knowledge/a.md`…` + `|`knowledge/a.md`…`
  gate  : indexed=0/1 missing=0 dangling=0 duplicates=1 exit 1
  fence : indexed=1/1 missing=0 dangling=0 duplicates=0 exit 0
```

So the gate is green where the fence is red, and red where the fence is
green: the `\s*` latitude is a two-directional divergence from S185, not
merely a tolerance. Latent on committed bytes (both shapes absent at
`8f51071b` / `446dc396` / `d72243e`).

## Restoration evidence

Each mutant applied in place, detector run, then restored from
`/tmp/mutc3gate-pristine.py`:

| After mutant | sha256 before restore | sha256 after restore | `cmp` |
|---|---|---|---|
| M1 | `f6708287…f304de` | `fc4a10a2…20e43d71` | identical |
| M1b | `45a8e5da…f21bf` | `fc4a10a2…20e43d71` | identical |
| M2 | `c52e22c0…556985` | `fc4a10a2…20e43d71` | identical |
| M3a | `9054b5d8…f0a319` | `fc4a10a2…20e43d71` | identical |
| M3b | `c557ac39…21b783` | `fc4a10a2…20e43d71` | identical |

Final state: `git -C /tmp/mutc3gate status --porcelain` prints nothing (clone
working tree byte-identical to committed blob `df01b20f…` at `92d3c86`), and
the pristine detector re-run reproduces the baseline exactly (6/6; 41/43
exit 1; 43/43 exit 0; 43/43 exit 0; probes A red, B REFUSED, C REFUSED).
Lane `mado-shokunin` status shows only the untracked seat wave directory
`.ufo/waves/round-30/w1/` (other seats' reports); no lane file was written by
this item.

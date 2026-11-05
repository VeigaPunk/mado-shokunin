# R86ScribeSources — registry rows S491/S492 and collision check

Seat: R86ScribeSources (leaf, scribe). Owned file: this report. Did not edit `corpus/SOURCES.md`.
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Freeze `237ecf4e69a4986108f719f3beeafe111adaa033`.
HEAD at check time: `b33afc08`. `git status --short -- corpus/SOURCES.md` returned empty (clean).

## Result

- **S491 and S492 already exist in the registry.** They were landed by L1 in commit `01be4234`
  ("round-86: land the knowledge entry, lesson, registry rows and scorecard"), which is after the
  freeze. `git show 237ecf4e:corpus/SOURCES.md | grep -cE '^\| S49[12] '` returns `0`; HEAD returns `2`.
- Because the rows are already present, I did **not** append a second copy. A second copy is a
  duplicate id (E03) and a duplicate URL+scope (E04). The rows I drafted from the declaration are
  byte-for-byte the landed rows (same fields, same values).
- Validator on the real lane file: **exit 0**, zero E-lines. The file also has 56 pre-existing W-lines
  (W04 duplicate URLs). None names S491 or S492.
- One content defect (F1 below) is in the landed S492 row. It is L1's file, so it is reported, not fixed.

## Step 1 — shape (11 columns, NF=13 with the outer pipes)

Header: `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`.
Both landed rows: `awk -F'|' '{print NF}'` → `13`, `13`.

## Step 2 — id collision check

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort | tail -5
S488 S489 S490 S491 S492
comm -12 <(ids sorted -u) <(printf 'S491\nS492\n')  →  S491, S492   (both present)
registry ids (sort -u): 427
grep -cE '^\| S49[12] ' corpus/SOURCES.md → 2   (one row each, no duplicate)
```

## Step 3 — landed row content vs declaration

| field | S491 | S492 |
|---|---|---|
| source | RFC7493 I-JSON — rfc-editor.org/rfc/rfc7493.txt | CPython v3.14.8 Doc/library/re.rst — raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/re.rst |
| kind / tier | spec / A | docs / A |
| anchor | section2.3 Object Constraints, line159 of round86 fetch/S491.bin | fullmatch directive, line957 of round86 fetch/S492.bin |
| status | mined | mined |
| opened | 2026-11-04 (not future; today is after it) | 2026-11-04 |
| recheck | `180d` (NNd, valid) | `on-release` (symbolic cadence, valid) |
| used-by | corpus/knowledge/refusal-records-clause-observations-r86.md, corpus/lessons/round-86.md | corpus/knowledge/refusal-records-clause-observations-r86.md **only** (see F1) |

Pins (declaration ↔ disk):
```
sha256sum .ufo/waves/round-86/fetch/S491.bin → a44ccf1451a7bf4f4bbb78b39e10ed0e9a27ff2ee5b639c6458042b5a7197062 (12849 B)  matches declaration a44ccf14…
sha256sum .ufo/waves/round-86/fetch/S492.bin → d252cc185dfc1014e1b4a8087b2515b71c76527f0f2f6dfddba9a880537e6a48 (78262 B)  matches declaration d252cc18…
sed -n 159p fetch/S491.bin → "   Objects in I-JSON messages MUST NOT have members with duplicate"   (quote begins here)
sed -n 957p fetch/S492.bin → "   If the whole *string* matches the regular expression *pattern*, return a"   (quote begins here)
```
Both used-by paths exist on disk (`corpus/knowledge/refusal-records-clause-observations-r86.md`,
`corpus/lessons/round-86.md`). No cell contains a literal or escaped `|`:
`grep -E '^\| S49[12] ' corpus/SOURCES.md | grep -c '\\|'` → `0`.

## Step 4 — validation

Mirror note: a `corpus/`-only mirror is not a valid test. `used-by` paths outside `corpus/`
(`tools/`, `SKILL.md`, `.ufo/waves/...`) resolve against the mirror root and fail E11
(`S096`, `S173`…`S482`). That run exited `1` for reasons unrelated to S491/S492.
The valid mirror is the full HEAD tree:

```
git -C /home/vgpnk/Projects/shokunin/mado-shokunin archive HEAD | tar -x -C "$S/tree"   # read-only
sources-census.sh validate --file "$S/tree/corpus/SOURCES.md"  → EXIT=0, E-lines=0, W-lines=56
sources-census.sh census   --file "$S/tree/corpus/SOURCES.md"  → rows 427; mined 400; queued 10; rejected 17
sources-census.sh validate --file /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md → EXIT=0 (0 E-lines)
```

Collision controls (same mirror, rows appended a second time):

| control | where the duplicate lands | exit | findings |
|---|---|---|---|
| append at end of file | after `## Paths` | **1** | E12 S491, E12 S492 (outside Registry; not E03, because the validator counts ids only inside the Registry) |
| insert after the S492 row | inside Registry | **1** | E03 S491, E03 S492; E04 S491, E04 S492 (duplicate URL+scope) |

So the validator catches a real duplicate inside the table; a duplicate placed after the table is caught as E12 instead.

## Findings

**F1 (content, L1 owns `corpus/SOURCES.md`).** S492 `used-by` lists only the knowledge entry.
The seat spec asks for "the round-86 knowledge entry and lesson". The lesson cites S492 in its Gate
block (`corpus/lessons/round-86.md:68`), and the knowledge entry also cites S492 (line 118). Suggested
fix for L1 (not applied by me): `used-by` = `corpus/knowledge/refusal-records-clause-observations-r86.md,corpus/lessons/round-86.md`.
The validator does not fail this (E11 checks existence only), so the defect is invisible to validate.

**F2 (process, L1).** The rows were landed post-freeze (`01be4234`, after `237ecf4e`). The declaration
says "no row is superseded this round", and the freeze carries 0 rows for S491/S492. This is
consistent with the lesson's "registry rows" landing, but a seat that re-derives rows from the
declaration will always see a collision. Expected, not a fault.

**F3 (style, observed, no validator effect).** Separator in `used-by`: 93 occurrences of `.md, corpus/`
(comma-space) vs 23 of `.md,corpus/` (no space). S491 uses the no-space form. Both forms pass E11.
Not a defect; noted for consistency only.

## Commands run (read-only except scratch)

- `sed -n 436,450p corpus/SOURCES.md`; `grep -nE 'S49[12]' corpus/SOURCES.md`
- `git -C <lane> status --short -- corpus/SOURCES.md` (empty); `git -C <lane> log --oneline -3 -- corpus/SOURCES.md`
- `git -C <lane> show HEAD:corpus/SOURCES.md | grep -cE '^\| S49[12] '` → 2; same at `237ecf4e` → 0
- `git -C <lane> archive HEAD | tar -x -C <scratch>/tree` (read-only)
- `scripts/sources-census.sh validate|census --file <path>` as listed above
- `sha256sum` / `sed -n` on the two pins

No file was written in the lane except this report. Scratch was removed before yield.

# ScrConsiderFinal — round-41 w2 seat report

Status: done. Task: verify the `ScrConsiderthese` w1 proposal's evidence read-only on the lane at the data
commit `07f2641696b5ac73de1404ea737a9f27e9819aa1`, and write the exact landing text.

## Deliverable

`.ufo/waves/round-41/w2/ScrConsiderFinal/final.md` — the exact text to land:

- **A** — `corpus/QUALITY.md` criterion 69 (the file is at 68 numbered criteria at both base
  `ab2bfaa` and `07f2641`; confirmed `grep -c '^[0-9]\{1,3\}\. '` = 68 at both, last line `68.`),
  with the `M41-n` placeholder for the L1's mistake id.
- **B** — `corpus/lessons/round-41.md` `## considerthese` section (replaces the skeleton line
  "No proposal is claimed by this skeleton.").
- **C** — optional `## Mistakes` entry (the L1 numbers it; next free id after M41-8 is M41-9).

Every number in the landing text is reproduced in the verification block of `final.md` by a command pasted
with its output, all run read-only at/against `07f2641`.

## Verification result

All reproduced:

| number/claim | command | output |
|---|---|---|
| window 68 commits | `git log --oneline 57a772b..f6e3247 \| wc -l` | 68 |
| SOURCES rows at base/tip | `git show 57a772b:corpus/SOURCES.md \| grep -c '^\| S[0-9]'`; same at `f6e3247` | 185; 207 |
| rows added | `git diff 57a772b..f6e3247 -- corpus/SOURCES.md \| grep -c '^+\| S[0-9]'` | 22 |
| knowledge files | `git ls-tree -r --name-only 57a772b corpus/knowledge \| wc -l`; same at `f6e3247` | 43; 52 |
| knowledge added/deleted | `git diff -M --name-status 57a772b..f6e3247 -- corpus/knowledge \| grep -c '^A'` / `'^D'` | 9; 0 |
| rename-awareness | full `git diff -M --name-status` listing | 9 `A` lines only, no `R`/`M`/`D` |
| per-round split | `git log --diff-filter=A --format='%h' --name-only …` + `git show -s` messages | round 32 `f591087` 3, 34 `fa7ba11` 1, 35 `02088b4` 3, 37 `3f42425` 2 |
| one tool added | `git log --diff-filter=A --format= --name-only 57a772b..f6e3247 -- tools/` | `tools/mado-eventq.py` |
| QUALITY 68 at base and data commit | `grep -c '^[0-9]\{1,3\}\. '` on `ab2bfaa` and `07f2641` | 68; 68 (last `68.`) |
| criterion 60 at line 367 | `git show ab2bfaa:corpus/QUALITY.md \| grep -n considerthese` | 367 |
| no relay/first-hand in QUALITY | `grep -ni 'relay\|first-hand\|first hand'` | empty |
| SKILL.md/PROVINCE.md zero | `grep -ci considerthese` | 0; 0 |
| check-evidence-pointers `:49` | `grep -n considerthese` | PATHY regex includes `considerthese/` |
| round-33.md:28 prose | `sed -n '28p'` | "considerthese/2026-10-24.md proposal 5 (verify one cited fact first-hand) was" |
| round-33 number-drift class | `grep -n 'class: number-drift'` | line 45; 187 MB vs 11.6 MB at lines 45-46 |
| round-40.md:146 / :166 | `sed -n '146p;166p'` | proposal 2 text; "proposals 1 and 3-6 … stay open" |
| round-39.md:82 / round-38.md:4 | `sed -n` | quotes present |
| reflection lines 3/5/7/38/50 | `git show 07f2641:considerthese/2026-10-25.md` | window 68 commits; "gained eight entries"; "185 to 207 rows"; "one new runnable tool"; proposal 5 wording; "8 knowledge entries" |
| quote verifier | `.ufo/waves/round-41/w1/ScrConsiderthese/verify-quotes.py` receipt | `MADO_QUOTES: passed=12/12` |

**Numbers not reproduced: none.** Only failed command this seat ran was its own convenience
`git rev-parse --short <4 names>` (fatal: Needed a single revision); the four individual
`git rev-parse --verify` calls succeed — multi-arg parsing quirk of that convenience call, not a missing
revision, and not an evidence command from the proposal.

## Notes for the L1

- `M41-n` in sections A/C is the L1's number; the next free id in `round-41.md` `## Mistakes`
  (M41-1..8 exist) is M41-9.
- The receipt path cited in B/C (`.ufo/waves/round-41/w1/ScrConsiderthese/receipts.txt`) is tracked in
  the tree at `07f2641`.
- No tool installed or updated; no host/journal/compositor/package access; read-only git only. No lane
  file edited (leaf scope).

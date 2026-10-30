# R56W3ExecInherited — Round 55 census correction

## Attack and result

Attacked the stale census paragraph in `corpus/lessons/round-55.md` (routed defect 1). The requested append-only correction is in `corrections/round-55-append.md`; the lesson itself was not edited. The correction is dated 2026-10-30, identifies both stale counts (`314 → 317` and `317 rows`), names S381/S382 as additions after lesson writing, and gives the count command and result for 319 rows.

## Exact evidence

Command:
`git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:corpus/lessons/round-55.md | grep -n '314\|317'`

Output (decisive lines):
```
25:- Rows `314 → 317` (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`); new ids S378–S380, tier A, `mined`.
42:Start census command `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → exit 0, `mado ok` (output `.ufo/waves/round-55/receipts/census-before.txt`, 314 rows). End census: see the round report and `.ufo/waves/round-55/receipts/census-after.txt` (317 rows).
```

Command:
`git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 187003d0:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`

Output: `319`. `187003d0` is the recorded Round 55 integration revision whose history entry names rows S381-S382; this count is at the post-addition Round 55 state. For context, the current frozen Round 56 tip's registry count command returned `332`, reflecting later Round 56 rows; it is not the historical count corrected here.

## Deliverables

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ExecInherited/corrections/round-55-append.md` — exact paragraph for L1 to append verbatim.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ExecInherited.md` — this report.

## Defects and limitations

- **Weakens the lesson's census accuracy:** the cited old count is 317, but Round 55's post-S381/S382 registry has 319 rows. Demonstrated by the count command above.
- No check beyond the specified read-only git evidence and historical count was run. No build, lint, or tests were run. No blocking issue found for producing the requested append text.

# ScoutQ36Anatomy — checker contract and the two Q36 survivors

Axes: contract fidelity, survivor discrimination, command exactness. Read-only. No tool install. No lane edit except this report.

Subject: `quality/check-control-receipts.py` sha256 `2233db1d489fa325c3b4bd9b5b1dccc68eb9311864a0d975303907463fa65af2` (207 lines). Lineage: M25-3 (round-25 checker, 1/6 killed; survivors were non-strict `<`, ignore shapes, newest receipt, any `.md`, `updatedAt`). M26-8: the successor then exited 1 on round 26 because it required `controls/*.md` while the receipts were `.txt` (chronology itself held, gap 17 s). Those two repairs are now `--receipt-glob` (default `*.md`,`*.txt`) and `--seeds`. The two survivors of *this* successor are Q2 and Q5 below, not the M25-3 five.

## Rule and exits

Exit 0 only if, at TIP, the oldest commit that adds a qualifying receipt under `.ufo/waves/round-N/controls/` has committer `%ct` strictly `<` registry `createdAt`, and every `--shapes` entry is covered by at least `--seeds` distinct qualifying basenames. Exit 1 otherwise. Exit 2 when history/registry cannot be evaluated. argparse errors (bad `--seeds`, bad `--counter-sha`) are also process exit 2, on stderr, with no verdict line.

Qualifying: path matches a glob (controls-relative path or its basename; pattern is lowercased; `fnmatchcase`, so `*` crosses `/`). A `.md` file (suffix compared lowercased) also needs a line starting `CONTROL ` or `# Control` unless `--any-md`. With `--counter-sha`, the first line (lowercased) must contain one of the shas. `updatedAt` is never read. Shape match is case-insensitive substring of the basename; `|` is alternatives.

## Flags (defaults)

| flag | default |
|---|---|
| `--round` | required int |
| `--data-registry` | required repo-relative path, read at TIP |
| `--repo` | cwd |
| `--tip` | `HEAD` |
| `--shapes` | `DoNothing,EmptyArray\|AllFalse,Junk,Echo,LabelKeyed,NoReader` |
| `--seeds` | `1` (int >= 1) |
| `--receipt-glob` | empty, then `*.md` and `*.txt` (repeatable; replaces the default) |
| `--any-md` | off |
| `--counter-sha` | none (repeatable; 64 hex, stored lower) |

## Git reads (only these; never writes)

`git()` copies `os.environ`, sets `GIT_OPTIONAL_LOCKS=0`, drops `GIT_DIR` / `GIT_WORK_TREE` / `GIT_INDEX_FILE`, discards stderr.

1. `git -C REPO rev-parse --verify TIP^{commit}` — fail: `UNEVALUABLE bad tip …` rc 2
2. `git -C REPO ls-tree -r --name-only TIP -- .ufo/waves/round-N/controls/` — fail: `UNEVALUABLE ls-tree failed` rc 2
3. per selected path: `git -C REPO show TIP:PATH` — one failure skips that file
4. `git -C REPO log --reverse --diff-filter=A --format=@%H %ct --name-only TIP -- RECEIPTS…` — fail: `UNEVALUABLE git log failed` rc 2; no added name: `UNEVALUABLE no adding commit found` rc 2
5. `git -C REPO show TIP:DATA_REGISTRY` — fail: `UNEVALUABLE data registry … absent at tip` rc 2; bad `createdAt`: `UNEVALUABLE createdAt unreadable: …` rc 2

Pass stdout is five lines, then rc 0:

```
tip=<40hex> round=N receipts=K counter_sha=- excluded_by_counter_sha=0 receipt_glob=*.md,*.txt excluded_by_glob=0 seeds=1
receipt_commit=<12hex> committed=<ISO> data_registry=<path> createdAt=<raw>
order=ok gap_s=<seconds> shapes_missing=- seeds_short=-
shape_counts=<shape:n,...>
CONTROL_RECEIPTS verdict=PASS
```

Fail with zero receipts skips the middle three lines: `CONTROL_RECEIPTS verdict=FAIL reason=no-receipt-under-.ufo/waves/round-N/controls/` rc 1. Fail with receipts still prints all five; `order=LATE` and/or `shapes_missing=` / `seeds_short=Shape(n<N)`, then `verdict=FAIL` rc 1.

## Survivors (diff vs the sha above)

**Q2** `.ufo/waves/round-28/q36/mutants/Q2-glob-case-sensitive.py` sha `7ff7059b420ac42a7173344ad9563b81b8b5a50f4774f4f31725222a975a0803` (byte-identical to the r27 survivor). `selected()` line 97: `rel = rel.lower()` becomes `rel = rel`. Patterns are still lowercased; the path is not, so `fnmatchcase` misses `.TXT` and an uppercase `K1` prefix.

**Q5** `.ufo/waves/round-28/q36/mutants/Q5-marker-case-insensitive.py` sha `a67cb791f04c2fb9b44a8bca8a1c955fe4a190ce6bfce943082d5661951674cc`. `has_marker()` line 85 case-folds both prefixes (`control ` and `# control`). Wider than the r27 survivor `4e83fe2e…`, which folded only `CONTROL ` and left `# Control` exact. The fixture below hits the shared `control ` arm.

## Distinguishing fixtures (exercised this turn)

Receipt bytes match the committed trees under `.ufo/waves/round-28/q36/fixtures/`. Those trees are not git repos, and their registry is `.ufo/waves/round-98/registry.json` = `{"createdAt":"2026-10-22T00:05:00Z"}\n` (no `updatedAt`). The runs below used the already-built scratch repos, whose registry blob is pretty-printed `createdAt` plus `updatedAt` at `.ufo/waves/round-98/w1/reports/swarm-registry.json`. The checker reads only `createdAt`; either JSON works if `--data-registry` is the path that exists at TIP.

History (both repos): commit 1 `2026-10-22T00:00:00+0000` adds only the registry; commit 2 `2026-10-22T00:01:00+0000` adds the three receipts. Author=committer `Q36Fixtures <q36@example.invalid>`. Gap = 240 s. Shapes must be the three present names. Seeds stay at default 1. No `--any-md`, no `--counter-sha`, default globs.

Q2 files (tip `90174e0655f31753c695b706c4505cf2d2cacf10`, receipt commit `90174e0655f3`): `controls/K1{DoNothing,Junk,EmptyArray}-seed1.TXT` each `exit=1\n`.

Q5 files (tip `12d8284d4b151ca55537bfa614edbc848136c3c4`, receipt commit `12d8284d4b15`): `controls/K1{DoNothing,Junk,EmptyArray}-seed1.md` each `control Fixture control\n`. No `CONTROL ` / `# Control` line.

Command (swap checker and `--repo`):

```
/usr/bin/python3 -I -B CHECKER --repo REPO --round 98 \
  --shapes 'DoNothing,Junk,EmptyArray|AllFalse' \
  --data-registry .ufo/waves/round-98/w1/reports/swarm-registry.json --tip HEAD
```

| arm | repo | rc | stdout that matters |
|---|---|---|---|
| Q2 pristine | `…/Q2-glob-case-sensitive/before/repos/w-glob-uppercase` | 0 | `receipts=3 excluded_by_glob=0` `verdict=PASS` `gap_s=240` |
| Q2 mutant | same | 1 | `receipts=0 excluded_by_glob=3` `reason=no-receipt-under-…` |
| Q5 pristine | `…/Q5-marker-case-insensitive/before/repos/w-marker-lowercase` | 1 | `receipts=0 excluded_by_glob=0` `verdict=FAIL` |
| Q5 mutant (committed wide copy) | same | 0 | `receipts=3` `order=ok gap_s=240` `verdict=PASS` |

All four commands exited as in that table (this turn). Directions are opposite: Q2 is pristine-accepts / mutant-rejects; Q5 is pristine-rejects / mutant-accepts. Do not invert Q2.

## Traps that collapse the rc split

- Default shapes add Echo, LabelKeyed, NoReader: Q2 pristine also rc 1 (`shapes_missing`), same rc as the mutant.
- `--seeds 2`: one file per shape, both arms rc 1.
- `--any-md`: Q5 pristine also rc 0.
- Receipt committer time `>= createdAt` (a `git commit` at "now"): Q5 mutant reaches `order=LATE` and also rc 1.
- Pointing `--data-registry` at `w1/reports/swarm-registry.json` inside the committed fixture tree (that path is absent): rc 2, not a kill.

Confidence: high on the checker (source) and on the four rcs (executed). Unresolved: this seat did not build a fresh repo from the committed `registry.json` path; the scratch repos already held the same receipt bytes.

# RcSourceFragmentCollisionS437 — C2 ledger attack on CapSourceFragmentCollisionS437 (a3w1)

Wave: round-25 a3w2 (attempt 3), C2 ledger attack item. Target report:
`.ufo/waves/round-25/a3w1/reports/CapSourceFragmentCollisionS437.md` (capability row `SCORECARD.md:437`,
`source-fragment collision screen`, base `41cc04c8d593837a0d5078bffaacdaa163d12897`).

Independent re-derivation: I cloned the lane myself to `/fast/scratch/hyaku/mado-r25a3/rc/CapSourceFragmentCollisionS437`,
detached at `41cc04c8` (`rev-parse HEAD` → `41cc04c8d593837a0d5078bffaacdaa163d12897`), re-ran all three
demonstration legs under `timeout 600 prlimit --as=4000000000`, and re-read the row and every cited superseding
line via `git show 41cc04c8:SCORECARD.md`. Clone deleted before return (`test -d` → gone).

## Commands run (in my clone, from clone root)

```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r25a3/rc/CapSourceFragmentCollisionS437
git -C … checkout -q --detach 41cc04c8
timeout 600 prlimit --as=4000000000 python3 .ufo/waves/round-13/w1/reports/MistakeFix.py --selftest
timeout 600 prlimit --as=4000000000 python3 .ufo/waves/round-13/w1/reports/MistakeFix.py --registry corpus/SOURCES.md
timeout 600 prlimit --as=4000000000 python3 .ufo/waves/round-13/w1/reports/MistakeFix.py --registry .ufo/waves/round-13/evidence/registry-before.txt
```

## Comparison: report's ledger line vs my observed run

| Aspect | Report claims | My observation at 41cc04c8 | Match |
|---|---|---|---|
| selftest | exit 0, `MISTAKE_FIX_SELFTEST: PASS 25/25` | identical line, exit 0 | yes, byte-for-byte |
| historical registry | exit 1, `COLLISION S017 -> S030`, `rows=39 urls=28 no_url=10 collisions=1 rejected_history=0 supersedes=0 errors=0` | identical | yes, byte-for-byte |
| current registry | exit 1, four `COLLISION` lines (S111→S120, S111→S121, S117→S119, S120→S121), three `REJECTED_HISTORY` (S030, S045, S094), `FAIL … rows=168 urls=140 no_url=21 collisions=4 rejected_history=3 supersedes=7 errors=0` | identical | yes, byte-for-byte |
| observed status | "fails as stated" — the row's pinned "current exits 0" leg is stale | row text at `:437` does say "current exits 0"; current registry exits 1 | yes; verdict correct |
| command form | relative paths from clone root; disclosed deviation from evidence receipts' absolute paths | relative-path invocation is equivalent and documented in the report | yes; honestly disclosed |
| superseding pointers | `SCORECARD.md:1592-1596` (explicit stale marking), `:1606` (15-vs-12-row literal reading, M24-5), `:1617` (round-25 routing) | all three exist and say what the report says | yes; none missed |
| tool digest | `MistakeFix.py` sha256 `a3a1559b…c89e`, blob `1376664c` | identical sha256; `git rev-parse HEAD:<path>` → `1376664ce020dfed…` | yes |
| `corpus/SOURCES.md` digest | `58f6e47b…1e5f` | identical | yes |
| `registry-before.txt` digest | `a93428a4…6197` | identical | yes |
| section/line citations | row `:437`, header `:435-436`, `### Sources and demonstrated repertoire` `:425`, `## Round 13` `:367` measured at `95cbc41f` baseline `7dcb785b` | all confirmed; both commit pins resolve (`cat-file -t` → commit) | yes |
| evidence pointer | `evidence/collision-*-corrected.txt` → `collision-green-corrected.txt` + `collision-red-corrected.txt`, recording the same two `--registry` legs with absolute paths | both files exist; line 1 of each records exactly those commands | yes |
| other `collision` mentions | `:570`, `:644` are different screens (census `collisions=0`); `:1470` is synthetic-target-name collision | confirmed by grep/context read | yes |
| interpretation | S119 supersedes S113 (not S117); live registry trips the rule; census accepts these as non-failing W04 warnings (`corpus/SOURCES.md:275-282`) | S119 cell reads "supersedes S113"; `SOURCES.md:277` confirms "different-scope repetitions can remain non-failing W04 warnings" | yes |
| clone hygiene | `git status --porcelain` empty; clone removed | my clone: porcelain `[]`, removed after run | yes |

## Findings

No defects found in the report under review.

- **Not copied-not-run**: the three legs' outputs are revision-specific (S111/S117–S121 collisions exist only in the
  current registry; counts `rows=168/collisions=4` vs `rows=39/collisions=1` across legs) and I reproduced every
  `MISTAKE_FIX:` line byte-for-byte in my own clone at 41cc04c8. A copy of the round-24 record alone could not
  produce the full seven-line current-registry output, which the round-24 text only partially quotes.
- **Correct revision**: clone HEAD `41cc04c8d593837a0d5078bffaacdaa163d12897`; all three blob digests match the
  report's claimed sha256 values and `git rev-parse` object ids.
- **No overclaim**: the ledger's "fails as stated" is scoped precisely — the selftest and historical legs pass as
  written; only the pinned "current exits 0" is stale, and the report correctly attributes this to registry growth
  (rounds 21–22 adding S117/S119/S120/S121), not a tool defect. The residual-risk note (same command could exit 0
  at a later tip once supersedes links land) is accurate and appropriately pinned.
- **No missed superseding text**: `:1592-1596` explicitly marks this row stale with the same collision output;
  `:1606` records the M24-5 lesson; `:1617` routes the row. Exhaustive grep for `collision screen|collision-screen|MistakeFix`
  at base returns only `:437, :1592-1596, :1606, :1617` — the report cited all of them.
- Minor (non-finding): the report used relative registry paths where the committed evidence receipts used
  absolute ones; it discloses this inline and there is no observable behavior difference (my run confirms).

## Residual risk / verification gaps

- None blocking. My re-run and the report agree byte-for-byte; the only unexercised surface is the `--help`/other
  flags of MistakeFix.py, which the row does not claim.

Verdict: **RECHECK CapSourceFragmentCollisionS437: agree** — re-ran all three legs at 41cc04c8 in my own clone;
outputs byte-for-byte identical (selftest PASS 25/25 exit 0; historical registry COLLISION S017→S030 exit 1;
current registry FAIL collisions=4 exit 1). "fails as stated" verdict, digests, command form and all three
superseding pointers (`:1592-1596`, `:1606`, `:1617`) verified; no copied evidence, wrong revision, overclaim or
missed supersession.

Files changed: this report only. Sandbox `/fast/scratch/hyaku/mado-r25a3/rc/CapSourceFragmentCollisionS437` deleted.
No installs; no lane git/jj writes; no `__pycache__` left (script executed, not imported).

# CapSourceFragmentCollisionS437 — C2 row re-run: SCORECARD.md:437

Wave: round-25 a3w1 (attempt 3), C2 row re-run item. Base read-only at `41cc04c8d593837a0d5078bffaacdaa163d12897`.
No lane file was edited except this report; no git/jj write ran in the lane; the sandbox clone was deleted.

## Row and section

- Row: `SCORECARD.md:437`, table header `SCORECARD.md:435-436`, under `### Sources and demonstrated repertoire`
  (`SCORECARD.md:425`), inside `## Round 13 — committed measurements and author verdicts` (`SCORECARD.md:367`,
  content measured at `95cbc41f`, baseline `7dcb785b`). It is a repertoire row under a non-`Capabilities` heading,
  so it sits outside round-24's counted 12-row population (`SCORECARD.md:1588-1590`) and inside the literal
  "capability table" reading that round 24 flagged (`SCORECARD.md:1606`).
- Capability: `source-fragment collision screen`.
- Stated claim: "Stop a repeated active canonical URL despite different scope wording; preserve rejected history
  and valid supersedes links."
- Demonstration command as written: `python3 .ufo/waves/round-13/w1/reports/MistakeFix.py --selftest` (25/25); plus
  "real historical registry exits 1 naming S017/S030, current exits 0". Evidence pointer:
  `evidence/collision-*-corrected.txt`, resolving under `.ufo/waves/round-13/` per `SCORECARD.md:440-443`; at base
  those files are `.ufo/waves/round-13/evidence/collision-green-corrected.txt` and `collision-red-corrected.txt`
  (both exist). Their recorded commands are exactly the two `--registry` legs re-run below, with absolute paths;
  I used the equivalent relative paths from the clone root (nearest documented form; no behavior difference).

## Sandbox

```
mkdir -p /fast/scratch/hyaku/mado-r25a3/c2
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r25a3/c2/CapSourceFragmentCollisionS437
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r25a3/c2/CapSourceFragmentCollisionS437 checkout -q --detach 41cc04c8
git -C /fast/scratch/hyaku/mado-r25a3/c2/CapSourceFragmentCollisionS437 rev-parse HEAD
```
→ `41cc04c8d593837a0d5078bffaacdaa163d12897`

Digests in the clone (matching `git show 41cc04c8:<path> | sha256sum` for the tool):
`.ufo/waves/round-13/w1/reports/MistakeFix.py` sha256 `a3a1559bcd8d5577578c3ee5b35b14d32049ec809c53df4989d08431f561c89e` (git blob `1376664c`);
`corpus/SOURCES.md` sha256 `58f6e47ba6b5539291aa4fc48388ae880d4c498e67568ca5e3b908d485ab1e5f`;
`.ufo/waves/round-13/evidence/registry-before.txt` sha256 `a93428a446902a6c86391145313fd2ea583df07d557b9781092691b27ede6197`.
`git status --porcelain` after the runs: empty.

All three legs were run from the clone root under `timeout 600 prlimit --as=4000000000`. `df -h /fast` showed
219 G available before the clone; the clone was removed afterwards (`GONE`).

## Verbatim command output

```
== clone HEAD: 41cc04c  SOURCES lines: 408 ==
----- CMD: python3 .ufo/waves/round-13/w1/reports/MistakeFix.py --selftest -----
MISTAKE_FIX_SELFTEST: PASS 25/25
exit=0
----- CMD: python3 .ufo/waves/round-13/w1/reports/MistakeFix.py --registry corpus/SOURCES.md -----
MISTAKE_FIX: COLLISION S111 -> S120 :: same canonical URL among active rows; add an opening 'supersedes S111 —' link or route to human review; differing scope text is not an exemption [url https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst]
MISTAKE_FIX: COLLISION S111 -> S121 :: same canonical URL among active rows; add an opening 'supersedes S111 —' link or route to human review; differing scope text is not an exemption [url https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst]
MISTAKE_FIX: COLLISION S117 -> S119 :: same canonical URL among active rows; add an opening 'supersedes S117 —' link or route to human review; differing scope text is not an exemption [url https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py]
MISTAKE_FIX: COLLISION S120 -> S121 :: same canonical URL among active rows; add an opening 'supersedes S120 —' link or route to human review; differing scope text is not an exemption [url https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst]
MISTAKE_FIX: REJECTED_HISTORY S030 :: same canonical URL as active S017; ignored by the collision check (retained rejection record)
MISTAKE_FIX: REJECTED_HISTORY S045 :: same canonical URL as active S017; ignored by the collision check (retained rejection record)
MISTAKE_FIX: REJECTED_HISTORY S094 :: same canonical URL as active S097; ignored by the collision check (retained rejection record)
MISTAKE_FIX: FAIL registry=corpus/SOURCES.md rows=168 urls=140 no_url=21 collisions=4 rejected_history=3 supersedes=7 errors=0
exit=1
----- CMD: python3 .ufo/waves/round-13/w1/reports/MistakeFix.py --registry .ufo/waves/round-13/evidence/registry-before.txt -----
MISTAKE_FIX: COLLISION S017 -> S030 :: same canonical URL among active rows; add an opening 'supersedes S017 —' link or route to human review; differing scope text is not an exemption [url https://wiki.hypr.land/Configuring/Basics/Window-Rules]
MISTAKE_FIX: FAIL registry=.ufo/waves/round-13/evidence/registry-before.txt rows=39 urls=28 no_url=10 collisions=1 rejected_history=0 supersedes=0 errors=0
exit=1
```

(The `== ... ==`, `----- CMD: ... -----` and `exit=` lines are my capture wrapper; every `MISTAKE_FIX:` line is
the tool's stdout byte-for-byte.)

## Ledger line

| SCORECARD.md:437 | source-fragment collision screen | Stop a repeated active canonical URL despite different scope wording; preserve rejected history and valid supersedes links | fails as stated: selftest exit 0 "PASS 25/25"; historical registry exit 1 "COLLISION S017 -> S030"; current registry corpus/SOURCES.md exit 1 "FAIL ... rows=168 ... collisions=4" (S111->S120, S111->S121, S117->S119, S120->S121) — the row's "current exits 0" leg is stale | `timeout 600 prlimit --as=4000000000 python3 .ufo/waves/round-13/w1/reports/MistakeFix.py --selftest`; `... --registry corpus/SOURCES.md`; `... --registry .ufo/waves/round-13/evidence/registry-before.txt` (from clone root at 41cc04c8) | SCORECARD.md:1592-1596 (round-24 wave-2 marks :437 stale, same exit 1 collisions=4 at 39c59630), SCORECARD.md:1606 (C2 row calls it stale), SCORECARD.md:1617 (planned route) |

## Superseding or contradicting text found in SCORECARD.md at 41cc04c8

- `SCORECARD.md:1592-1596` — explicit supersession: `source-fragment collision screen` (round 13, line 437
  "current exits 0") is **stale**: `MistakeFix.py --registry corpus/SOURCES.md` prints
  `MISTAKE_FIX: COLLISION S120 -> S121`, `collisions=4`, exit 1, at base and tip alike (its selftest still passes
  25/25). It also limits the claim "Each capability in the tables above was re-run" to the 12 counted rows.
- `SCORECARD.md:1606` — round-24 C2 row: the predicate "capability table" literally covers 15 rows; read that way
  three rows have no command and one (collision screen) is stale (lesson M24-5).
- `SCORECARD.md:1617` — round-25 planned work: "route the stale collision-screen row and H2".
- No other row or text mentions the capability; the other `collision` hits at `:570`, `:644` (census
  `collisions=0` counts of a different screen) and `:1470` (`synthetic-target-name collision`) concern other
  surfaces and neither supersede nor contradict this row.

## Interpretation (grounded in the observed outputs)

- The screen's mechanism works as described: it treats a repeated *active* canonical URL as a collision even when
  the rows' scope wording differs, discounts rejected history (S030/S045/S094 print as `REJECTED_HISTORY`, not
  collisions), and honors supersedes links. The historical leg reproduces the row exactly (`S017 -> S030`, exit 1).
- What decayed is the pinned "current exits 0" statement: later rounds admitted same-URL rows with distinct scopes
  and no supersedes link to the colliding active sibling (S111/S120/S121 on
  `Doc/reference/executionmodel.rst`; S117/S119 on `Lib/imaplib.py`; S119 supersedes S113, not S117), so the
  live registry at 41cc04c8 now trips the same rule. The lane's maintained census accepts those as non-failing
  W04 duplicate-URL warnings (`corpus/SOURCES.md:275-282`, `corpus/lessons/round-22.md:21`), which is why the
  stale row survived: two different screens, two different exit semantics.
- This is a stale-row finding, not a tool defect: the run performed at 41cc04c8 matches the round-24 record and
  the tool's own selftest. The row should be re-marked (round-24 already appended the pointer; the row cell itself
  still says "current exits 0").

## Files changed

- `Report:` `.ufo/waves/round-25/a3w1/reports/CapSourceFragmentCollisionS437.md` (this file). Nothing else.
- Sandbox clone `/fast/scratch/hyaku/mado-r25a3/c2/CapSourceFragmentCollisionS437` deleted before returning.

## Risks and blockers

- None blocking. Residual risk for the ledger: the "current" leg is revision-bound; at a later tip with supersedes
  links added the same command could exit 0, so the ledger's observation must stay pinned to 41cc04c8, as recorded.
- The evidence pointer `evidence/collision-*-corrected.txt` has two files (green/red); the green receipt's exit 0
  reflects the round-13 registry (46 rows), not the current one.

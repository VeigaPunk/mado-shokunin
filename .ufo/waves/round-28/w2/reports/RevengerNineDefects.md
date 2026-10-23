author: RevengerNineDefects (mado r28 w2, revenger seat)

# Reconstruction of C2's nine record defects (D1–D9)

Scope: verify each defect against the lane's own records at the round-27 closure commit
`767b12db62ceb3ad38d24a13e4c693b4375ceb5a` (tip `767b12d`, verified `git rev-parse master` →
`4f610066efd90804b055c42ae20c41a7f44404f9` at r28 tip). Primary sources: the frozen r28 counter
`.ufo/waves/round-28/c2/count.py` (predicates, lines 96–185), the non-author spot-check
`corpus/lessons/round-27-verifier-spotcheck.md` (§1 defects 1–10, §6 routed list), the fleet report
`.ufo/reports/round-27/mado.md`, and committed bytes at `767b12db`. No edits made.

## Per-defect findings

**D1 — stale SKILL.md gate rows.** Intent: registry rows describe the landed r27 gates. Defect (real):
`git show 767b12db:SKILL.md | grep -n mado-r27` → rows at 633–635 all carry `— lands this round, pending`,
"Pending implementation pins", "not present in the draft-time quality directory", though suites landed at
`5c1d495`/repair `0b53bd86`. Spotcheck §1.1, §6.1. R28 repair (worktree SKILL.md diff) rewrites all three rows
with landed commands, verdict maps, blob SHAs — addresses the defect. Predicate weaker than routed fix
(no stable-finding-id check), but the landed repair exceeds it.

**D2 — lesson M27-2 dead pointer + stale fix cell.** Intent: evidence pointers resolve. Defect (real):
`corpus/lessons/round-27.md` M27-2 cites `corpus/SOURCES.md:195-199` as holding five malformed two-cell
S178–S182 rows; at `767b12db` those lines are valid S181/S182 rows + `## Paths` (awk `NF!=13` over the file:
only prose bullets at 262/266; confirmed also at `5c1d495`, `b6650d5`, `0be82d6`). The malformed rows were
worktree-only, never committed. Fix cell "removal … remain pending" stale: census `exit=0` at closure
(`evidence/sources-start.txt`, `mado ok`). Spotcheck §1.2. R28 repair: appended "Round-27 erratum (round 28)"
— substantively addresses, but repeats the imprecision "were at `corpus/SOURCES.md:195-199`" (they were
never at committed lines 195–199) and omits the never-committed fact. Defect addressed with minor residual
inaccuracy; predicate is string-level and cannot judge this.

**D3 — E01 fix without committed red-before receipt.** Intent (CORPUS): "a fix is shown able to fail before
it counts." Defect (real): `evidence/sources-start.txt` at closure is a clean run (7×W04 then `mado ok`,
`exit=0`); no commit carries the E01 output — it was observed on attempt-1's uncommitted worktree.
Spotcheck §1.3, §4 row E01. R28 repair: committed fixture
`.ufo/waves/round-28/evidence/e01-red-before/SOURCES.md` (sha `55969efe…`) reproduces five two-cell rows;
receipt shows validator `E01 … fields=2` ×5, `exit=1`. Addresses the defect's substance (a committed red
demonstration now exists); the fixture is a re-creation, not the historical uncommitted bytes — acceptable
since those bytes are unrecoverable. Predicate demands the counter re-run red+green itself at REV — strong.

**D4 — dead report pointer `quality/q36-successor-receipts.txt`.** Defect (real): `git ls-tree 767b12db
quality/` → only the three scripts; file lives at `.ufo/waves/round-27/quality/q36-successor-receipts.txt`
(content verified: Q36 fixture receipts). Report cites the root path. Spotcheck §1.4. R28 repair approach:
create the file at the cited root path — retro-resolves the pointer. Predicate only requires two mutant-id
strings present; a stub naming them would pass — weaker than the defect (a receipts file should carry
receipts). Not yet in worktree at this writing.

**D5 — SCORECARD harm-watch omission.** Defect (real): SCORECARD r27 section at `767b12db:1783` (Harm watch
line): "`git diff --stat 543f0445 -- tools/` touches only `tools/mado-wsrules.py` (new)". Actual:
`git diff --stat 543f0445..767b12db -- tools/` → `mado-binds.py | 6 +` (docstring-only, `b6650d5`) plus
`mado-wsrules.py | 851 +`. Spotcheck §1.5. Predicate: SCORECARD carries "round-27 harm-watch erratum" +
`tools/mado-binds.py` + "docstring" — addresses the omission in the same record that made it. Not yet
landed in worktree.

**D6 — registration misrecords C2 measurement flow.** Defect (real): r27 registration lines 50 ("commits
the bytes after the single C2 measurement"), 72 ("one measurement"), no repair-flow section; the round ran
two measurements (miss `48b9434a`, met `0b53bd86`) per receipts. Spotcheck §1.7. R28 repair (worktree diff):
appended "## Round-27 measurement erratum (round 28)" recording measurement 1, repair flow, measurement 2 —
addresses the record defect. NOTE: the routed fix (§6.7) also demanded the *next* registration declare the
repair flow **before** data; the r28 registration's Data rule has no repair/remeasurement clause. The
erratum satisfies the record leg; the forward-looking half of the routed defect is unmeasured by D6.

**D7 — w3 seat count 8 declared vs 7 reports.** Defect (real): report "w3 residual 8 seats (in-tree)" +
`seats=8` grant; `git ls-tree 767b12db .ufo/waves/round-27/w3/reports/` → 7 files; 7 names in report.
No committed w3 spec/run file exists (in-tree wave); watchdog grep `round=27` shows only the attempt-1
lane death, no eighth-seat death record. Spotcheck §1.8. Counter forces `declared=8 reports=7 unreported=1
identity=unknown`. The `identity=unknown` literal is the honest outcome given committed evidence (nothing
recoverable), but the predicate *hard-codes* it: a repair that discovered the identity would fail D7.
Mild overfit; reconciliation file not yet in worktree.

**D8 — SKILL citation off-by-one.** Defect (real): report cites `SKILL.md:631-636`; actual six-row span at
`767b12db` is 630–635 (r26 rows 630–632, r27 rows 633–635; verified by grep -n). Spotcheck §1.9. R28 repair:
LOG.md appended "round-27 SKILL citation erratum" naming both ranges with a re-derivation command —
addresses the defect.

**D9 — uncommitted w4 erratum artifacts.** Defect (real at r27 closure): `RevRepair.md` modified in
worktree after `767b12db` (+166/−33); `ExecRepairA1.md` absent from tree (A1 seat never returned a report).
Spotcheck §1.10. **Already repaired before round-28 data**: `dac4aef` ("land inherited w4 audit erratum")
committed both; `git show dac4aef:<file> | sha256sum` → `2ee41166…` and `94d656ce…` = the counter's pins.
Registration itself admits "D9 PASS … 8 of 9 unresolved" at freeze. So C2's claim "nine defects repaired"
measures eight open defects; D9 was resolved pre-round (its repair is not r28 work — flag: repaired before
round 28, not invented). Minor divergence: spotcheck §6.9 cites A1 candidate sha `e36f12f2…`; the landed
A1 report header pins `65aa2e24…` — unresolved provenance discrepancy, report-level only.

## Cross-cutting

- **Omitted routed defect.** Spotcheck §6 routed **ten** items; C2 measures nine. Item 6 — the report's
  overclaim "the tool's docstring and the knowledge entry cite them [S178–S182]" (docstring cites upstream
  filenames, not S-ids; verified `tools/mado-wsrules.py` docstring names `WorkspaceRuleManager.cpp` etc.,
  §1.6) — is a real record defect dropped from D1–D9. Item 9 (exact-≥3 residual + A1-wider-than-A2) was
  explicitly deferred to r28 C1 work, not a record defect — its exclusion is defensible. Item 6's exclusion
  is not flagged anywhere in the registration.
- **Invented defects:** none. Every D1–D9 maps to an independently verified discrepancy in committed bytes
  or the fleet report.
- **Already fixed pre-r28:** D9 only (at `dac4aef`, before the registration freeze commit `5198cc8`).
- **Predicate-vs-defect gaps:** D4 (string check, stub could pass), D7 (hard-codes `identity=unknown`),
  D6 (forward-looking "register repair flow before data" half unmeasured), D2 (landed erratum retains a
  small misstatement about where malformed rows "were"). D1/D3/D5/D8 repairs address their defects.

## Commands run (all exit 0 unless noted)

`git rev-parse master`; `git log --oneline -15 master`; `git ls-tree 767b12db` over `quality/`,
`.ufo/waves/round-27/{quality,w3/reports,w4/reports}`; `git log -- {RevRepair,ExecRepairA1}.md` → only
`dac4aef`+`cab3eac`; `git show 767b12db:{SKILL.md,SOURCES.md,round-27.md,registration.md,SCORECARD.md}`
targeted ranges; `git diff --stat 543f0445..767b12db -- tools/` → 2 files, 857+; `git show dac4aef:… |
sha256sum` → both D9 pins match; watchdog grep `round=27` for w3 deaths → none; `git diff` over the four
modified worktree files (SKILL, LOG, lesson, r27 registration) and reads of the untracked e01-red-before
receipt/fixture. `grep -n mado-binds` on the fleet r27 report → exit 1 (no match; confirms omission).
Spotcheck read in full. No tools installed; no files edited outside this report.

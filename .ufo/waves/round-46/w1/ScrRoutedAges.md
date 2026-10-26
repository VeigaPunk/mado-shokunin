# ScrRoutedAges — routed-defect age count (mado round 46, w1)

Assignment: `considerthese/2026-10-26.md` **proposal 3** — keep an age count per routed item.
Deliverable: `.ufo/waves/round-46/w1/ScrRoutedAges/ages.md` (Table 1: every routed bullet; Table 2: the
open ledger with ages; the proposed QUALITY criterion). Receipt:
`.ufo/waves/round-46/w1/ScrRoutedAges/receipt.txt` (commands + outputs, read-only).

## Behavior (what was produced)

- Population: **section 6 of the eight spot-checks** `corpus/lessons/round-{38..45}-verifier-spotcheck.md`
  — 45 bullets, located by computed line number (e.g. `round-38-verifier-spotcheck.md:84-88`,
  `round-45-verifier-spotcheck.md:102-118`).
- Closure evidence: the lane's closure records `round-40.md:68` / `:60` / `:70`,
  `round-41.md:59`/`:62`/`:65`/`:68`, `round-42-verifier-spotcheck.md:24`, `round-43.md:97-108`,
  `round-44.md:92-100` plus errata `round-44.md:196-215`, `round-45.md:61-62` and `:66-70`.
- Result: **23 closed** (22 within one round, 1 at two), **15 open**, 7 bullets that are
  non-actionable (SHONEN / driver / orchestrator) or carried duplicates. 42 ledger rows, 38 of them
  lane-actionable.
- Open ages `8, 8, 6, 6, 5, 5, 5, 5, 3, 2, 1, 1, 1, 1, 1` — sum 58, **mean 3.87, median 5, oldest 8**
  (R38-3's residual, R38-4). Counting only completed rounds (to the r45 spot-check) lowers every age
  by 1: oldest 7, mean 2.87.
- Proposed **QUALITY criterion 87** (number verified free: `grep -n '^86\.' corpus/QUALITY.md` → line
  420): a committed `quality/routed-defects.tsv` ledger with `id, first_round, first_locator, defect,
  owner, state (open|closed|retired), closed_round, closed_commit, evidence`, section-6 reconciliation
  (`grep -n` on every first locator; a repeated open item cites its id instead of adding a row; a
  closure requires `git cat-file -e <commit>:<artifact>`), and a per-round computed line
  `ROUTED_AGES: bullets= rows= actionable= closed= open= owner= oldest= mean=` with `STALE <id>
  age=<n>` for any open row at age ≥ 4, which the round must close, re-route with a reason, or record
  as deliberately carried. Check sketch: `quality/check-routed-ages.py` (not implemented — no counter
  or gate was added this seat).

## Gates / verification actually exercised

Read-only only; no counter, tool, compositor read, or host query was run.

Verified myself (receipt lines):

- `git show HEAD:.ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json | grep -c '"title"'` → `0`
  and the same on `w2/SentLiveRun/dump-now.json` → `0` (supports R44-D1 closed).
- `stat -c %s .ufo/waves/round-38/receipts/eventq-live-ss.txt` → `190816`; `git grep -c
  eventq-live-ss HEAD -- LOG.md` → exit 1 (supports R38-3's open residual).
- `grep -n S293 corpus/SOURCES.md` → `242:` still titled "the client's request as input" (supports
  R43-D2 open).
- `grep -c check-session-material SKILL.md` → `0` (supports R45-D3 open).
- `git status --porcelain -- .ufo/waves/round-45/w1/MutC1Counter/` → `?? …/results.digest.txt`
  (supports R45-D4 partial: file removed, digest uncommitted).
- `grep -n "PROVINCE.md:75" corpus/lessons/round-41.md` → `48:` (supports R41-4 open).
- `ls .ufo/waves/round-40/receipts | grep -c axis` → `1` (`axis-base.txt` only; supports R40-2 open).
- `git grep -l 35a126304f681969 HEAD` → the r40 spot-check prose only (supports R40-3 open).
- `ls .ufo/waves/round-45 | grep -ci readme` → `0` (supports R45-D5 open).
- `grep -c 'read TILED as "not floating" only' SKILL.md` → `1` (supports R43-D3 closed).

Nothing else is claimed as verified; the remaining "closed" rows cite the closure record, marked in
the table.

## Findings (each names what it attacks)

1. **A composite routed bullet loses its members** (attacks `round-38-verifier-spotcheck.md:87`):
   ten instrument ids were routed as one bullet; `git grep -l` over `corpus/lessons` finds `RevC1v3`,
   `LabratProcProof` and `LabratClockSkew` only in that spot-check at HEAD `e0be61e4`. The class
   returned as r43-D6 / r44-D5, so a class can be re-fixed while its routed instance stays open.
2. **A repeated bullet looks new** (attacks `round-41-verifier-spotcheck.md:79`): the same open items
   ("S041 held-row citation, tool ergonomics O1–O5") are re-listed at `round-42-verifier-spotcheck.md:90`,
   `round-43-verifier-spotcheck.md:111` and `round-44.md:102` with no state change; age 5 and invisible.
3. **Partial closure reads as closure** (attacks `round-38-verifier-spotcheck.md:86` and
   `round-45-verifier-spotcheck.md:114`): the r39 regeneration was done and the leak in the pushed
   tree was never re-mentioned — 190,816 B still at HEAD, no `LOG.md` line; r45's `results.json` was
   deleted but its digest is untracked.
4. **Retirement closures are unlabelled** (supports r43-D6, r44-D5): `round-45.md:68` says
   "round-44 counters not reused", which is a valid disposition, but nothing in a later §6 refers back
   to those ids.
5. **Ownership is not in the routing record** (attacks S40:94, S42:88, S42:89, S43:110): 4 of 42 ledger
   rows cannot be closed by the lane (operator SHONEN, orchestrator spawn floor, driver duplicate,
   attribution note), yet they are counted in the same list as lane defects.
6. **Support for proposal 3's premise**: the lane's per-round §6 is rebuilt from scratch, so an item's
   age is recoverable only by diffing eight files by hand — which is what this seat did (45 bullets,
   23 closed, 15 open). One computed `ROUTED_AGES` line per lesson plus a ledger makes the oldest item
   visible without that reconstruction.

## Out of scope / not done

- No criterion was added to `corpus/QUALITY.md` and no `quality/check-routed-ages.py` was written
  (the L1 is the only integrator; this seat's write scope is its own directory and this report).
- Current-state re-verification is limited to the commands above; I did not re-open every closed
  artifact, did not run any counter, and did not touch the round-46 C1/C2 seats' work.
- R45-D2's 24-copy count is relayed from the spot-check; I did not re-grep the monitor serial, which
  must not be written anywhere.
- No files outside `.ufo/waves/round-46/w1/ScrRoutedAges/` and this report were written; no scratch
  dir was created (no clone, venv or build was needed); no package or tool was installed; no
  git/jj mutation was run in the lane or the fleet.

## Artifact paths

- `.ufo/waves/round-46/w1/ScrRoutedAges/ages.md` — Table 1 (all 45 bullets), Table 2 (open ledger +
  ages), counts, proposed criterion 87, limits.
- `.ufo/waves/round-46/w1/ScrRoutedAges/receipt.txt` — every command and output used above.
- `.ufo/waves/round-46/w1/ScrRoutedAges.md` — this report.

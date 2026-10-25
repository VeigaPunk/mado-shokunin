# ExecRecordChecks — measurement evidence consolidation (round 39, w1)

Seat: `ExecRecordChecks` (leaf executor). Scope: consolidate measurement evidence into
`w1/ExecRecordChecks/measurements.json`; cross-check receipts at committed paths; report missing
receipts. No tool installs (no pacman/uv/npx/cargo actions; only stdlib + read-only git). No files
written outside the seat dir and this report.

## Revisions

- Lane base: `08be4eb7fd13358ed29b096e8924005d46ac409c` (registration.md §Base).
- Freeze commit (HEAD throughout this seat's run): `457d1b125932c1e0d797061a2156b917bcd7edaa`
  ("round-39: freeze registration + base receipts + inherited r38 seat reports").
- Data commit: **not yet landed** as of finalization (19:21 UTC). `git rev-parse HEAD` →
  `457d1b1` on every recheck; `git log --all` shows no round-39 data commit.

## C1 — calibration (measurement complete)

Counting command:
`cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/check-r38-discrimination.py --c1 quality/counters/c1-r38-event-ground.py --c2 quality/counters/c2-r38-eventq.py --manifest .ufo/waves/round-39/c1/manifest.json --rev <rev>`

- Before: `.ufo/waves/round-39/receipts/c1-redbefore.txt` (committed at freeze; sha256
  `7fe05ad9986656bb7580a0784fc5961a2128661321017c7bda70f0f986f62154`, identical twin
  `c1-redbefore-out.txt`) → `controls=19 correct=18/19 verdict=TARGET_MISSED`, exit 1; sole failing
  control `c1-duprow` (expected MISSED, observed MET). Measured at base `08be4eb`.
- After (freeze): `.ufo/waves/round-39/w1/ExecC1After/after-freeze.txt` → `controls=19 correct=19/19
  verdict=TARGET_MET`, exit 0, at freeze `457d1b1`.
- After (tip): `.ufo/waves/round-39/w1/ExecC1After/after-tip.txt` → identical 19/19, exit 0, at
  tip `457d1b1` (tip == freeze at measurement time).
- Self-reproduction (this seat) at freeze: same command with `--rev 457d1b1...` → exit 0, 19/19
  TARGET_MET.
- Manifest: `.ufo/waves/round-39/c1/manifest.json` sha256 `96965518dc8ad98b52b28b406d66841758c80fd75610f9b94e0239b8adf838c8`; frozen r38 manifest `14c49d9fec35dc9bc307fbdd5c732e2ce80fabeaadfe3327b9121f50b9553edb` (differs; byte-copy of repaired r38 landed manifest verified by ExecC1After).

## C2 — operability (after pending data commit)

Counting command:
`cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c3-r39-options.py --repo . --rev <rev>`

- Before: no receipt file; declared tool-absent at base. Verified: `ls tools/mado-options.py` →
  exit 2; counter pre-data run at freeze `--rev 457d1b1` → `PRED-C3-r39-v1: fixtures=0/1
  tool=absent verdict=TARGET_MISSED rev=457d1b1...`, exit 1.
- After: **missing** — data commit not landed. Worktree contains `tools/mado-options.py` (37358 B)
  and `quality/counters/c3-r39-options.py` (7002 B) as untracked files; counter resolves the tool via
  `git show <rev>:tools/mado-options.py`, so a TARGET_MET measurement is only possible once the data
  commit exists.

## C3 — coverage (after pending data commit)

Counting command:
`cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c4-r39-options-entry.py --repo . --rev <rev>`

- Before: no receipt file; declared `admitted=0/1 verdict=TARGET_MISSED`. Verified: counter
  `quality/counters/c4-r39-options-entry.py` absent; `corpus/knowledge/config-option-table-r39.md`
  absent; `corpus/SOURCES.md` rows S218/S219 absent (grep for `^| S21[89]` → no match).
- After: **missing** — data commit not landed; S219 own-work receipt additionally requires the data-tip
  sha256 of `tools/mado-options.py` (ScrSourcesRows).

## Harm-watch receipts

| Item | Before (committed @ freeze) | After (seat artifact) |
|---|---|---|
| Axis | `receipts/axis-base.txt`: checked=3 mismatched=0 @08be4eb | `w1/ExecGateHealth/gate3-axis-scores.out`: checked=3 mismatched=0 @457d1b1 |
| Navigation | `receipts/nav-base.txt`: indexed=55/55 @08be4eb | `w1/ExecGateHealth/gate1-check-index.out`: indexed=55/55 @457d1b1 |
| Selftest | `receipts/selftest-base.txt`: 460/460 | `w1/ExecSelftestAfter/selftest-after.txt`: 460/460 (exit 0) |
| Census | `receipts/census-before.txt`: exit 0, W04 x7 + W01 S277, ok | `w1/ExecCensusAfter/census-after.txt`: EXIT_CODE=0, same warning set |
| Eventq (routed) | — | `w1/ExecEventqSnapshot/eventq-after.txt`: fixtures=14/14 readonly=1 live=1 tool=present verdict=TARGET_MET @457d1b1 |

Command for census (both): `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` (fleet script; exit 0).

## Receipt cross-check (test -f / git ls-tree at HEAD)

All 8 committed receipt paths verified present and tracked: `receipts/{axis-base,nav-base,selftest-base,census-before,c1-redbefore,c1-redbefore-out,manifest-frozen-r38}.txt/.json` and `c1/manifest.json`. Committed instruments verified: `quality/check-r38-discrimination.py`, `quality/counters/c1-r38-event-ground.py`, `quality/counters/c2-r38-eventq.py`, `quality/check-index.py`, `tools/mado-verify.sh`.

## Missing receipts

1. C2 after receipt (pending data commit).
2. C3 before receipt (none exists/declared; declared state verified).
3. C3 after receipt (pending data commit).
4. Committed data-commit after receipts (data commit not yet landed).

## Blockers

- Data commit not landed as of 19:21 UTC (wave still assembling: 55/64 seat reports at last check).
  C2/C3 after-measurements cannot be run until it exists (`git show <rev>:...` resolution).
- `ScrKnowledgeEntry` flags provisional OBS quotes in the C3 entry draft pending S218/S219 Gate
  quotes; c4 counter file does not exist in any seat output.

## Result

measurements.json written at `w1/ExecRecordChecks/measurements.json` (valid JSON, schema
`mado-round39-w1-measurements-v1`); C1 fully measured (MET 19/19 @ freeze and tip); C2/C3 before state
verified; C2/C3 after receipts missing pending the data commit.

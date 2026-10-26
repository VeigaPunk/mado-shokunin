# RevQuality — w2 review: QUALITY.md criteria 77-81 (round 43, data commit 1959770)

Seat findings with full receipts: `.ufo/waves/round-43/w2/RevQuality/findings.md` (15 run receipts in the same dir).

## Verdict

All five Check commands do what their criteria say: each fails on its named bad input and passes on the good one, with
exit codes byte-matching the criteria's quoted outputs. Every lesson pointer resolves. Two sequencing defects against the
landed data commit, both healed by the round tip:

1. **(medium)** Criteria 77/79/80 cite `LOG.md:2487`/`:2488`/`:2490`; at 1959770 `LOG.md` is 2483 lines — none resolves,
   and the correction/disclosure/pointer text is in no committed revision at that point. All three lines exist with the
   claimed content at tip 2a3707c8. At the data commit the landed criteria text fails criterion 77's own locator bar.
2. **(medium)** The Check commands of 78-81 (and criterion 77's composite witness `LOG-at-5add5b4.md`, sha `f6c27a36…`)
   cite w1 seat paths absent from 1959770 (`git cat-file -e` fails; the only w1 file committed there is
   `swarm-registry.json`), so a fresh checkout of the data commit cannot run four of the five new checks. All assets are
   committed at the tip, byte-identical to the files I ran (`check78.py ee89e315…`, `check79.py f50b97fc…`,
   `check80.py dc6883d1…`, `check78.sh 2906c095…`). The author seat declared this risk; it materialized, then was healed.
3. **(low)** Criterion 81's work leg (`wave_md`) is not produced by its Check command; re-derived independently — true
   (round 42 → 0 at base a35cfdf). **(low)** Criterion 79's "live recurrence" sentence ("outside every committed
   revision") is stale: the receipt is committed at 1959770 and `LOG.md:2490` exists at the tip. **(info)** Criterion 80's
   pass leg depends on the unpinned live host tree `~/Projects/gkeep/gkeep/ui.py` (passes today, `src=488`).

## Evidence highlights (all receipts in the seat dir)

- 77: round-42 `registration.md:61` → `MISS supported=0` exit 1; corrected copy → `427-428,448 OK` exit 0; composite
  `locators=4 miss=3` exit 1; committed `quality/check-locators.py` sha `c1ea52ad…` == w1 tool; selftest `18/18` exit 0;
  GEOMETRIC_GOAL counts 0/0/3/2 exactly as the criterion states.
- 78: `TALLY_MISMATCH claim M=37 receipt=38` FAIL exit 1 on the r42 pair; `verdict=OK` exit 0 on the r43 pair;
  `run-c1-controls.py:139` really prints `len(jobs) - 2`.
- 79: 5/5 non-OK pointers FAIL exit 1 on the r42 report; `harm-tip.txt verdict=OK why=command+output+exit` on r41;
  `NO_MATCHING_CLIENT` = 0 at a62f2e0 (section and whole).
- 80: r42 excerpt FAIL exit 1 (`header=446-495 body=44 expected=50 src=488`, `end past_src`, `first_diff_body_line=44`);
  r43 excerpt OK exit 0 (`446-488`, `43=43`).
- 81: `TALLY rounds=7 launches=8 dead=1 complete=7 clean=3 dirty=4 relayed=7 unknown=0` / `TABLE_COMPLETE` exit 0 on
  36-42 (matches the criterion); `rounds=6 … relayed=6` on 32-37; `--selftest` PASS (12 assertions) with ABSENT /
  TABLE_INCOMPLETE teeth. Digest grew since w1; tallies stable.

Residual risk and gaps are listed in the findings file. Tools installed: none.

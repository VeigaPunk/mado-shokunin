# CritClaimSizing — round 45 w1 (status: complete)

Seat: `CritClaimSizing`, attack on claim sizing before any round-45 data. Frozen inputs read only:
`registration.md` (freeze `22a8dedd`), `quality/counters/c1-r45-monitors.py`, `quality/counters/c2-r45-monitor-entry.py`,
`AXES.md`, `corpus/README.md` frontier, `receipts/axis-base.txt`, `receipts/c2-ground-base.txt`, `QUALITY.md`,
`SCORECARD.md`. No lane file edited; all clones/fixtures/work under `/fast/scratch/hyaku/mado-r45/CritClaimSizing`
(1.4 GB, removed at exit). No tools installed (host `python3`, `git`, `sh` only).

Findings: `.ufo/waves/round-45/w1/CritClaimSizing/findings.md` — **5 attack findings** (F1 HIGH; F2, F3, F4 MEDIUM;
F7 LOW) and **2 passes** (F5 prior art, F6 separability). 19 quotes verified by
`w1/CritClaimSizing/verify-quotes.sh` (19 checked, 0 failed).

Controls scored beyond the registered set (all clones at the freeze, one scratch commit each):

| id | shortcut | verdict |
|---|---|---|
| K00 | freeze tree unchanged | C1 `0/49`, C2 `0/1` MISSED (matches registered before states) |
| K16 | freeze reference copied into `tools/` (one `git show`) | C1 `49/49 TARGET_MET` (= registered REF) |
| K17 | 71-line tool that execs the counter's own `FIXTURES` table | C1 `49/49 TARGET_MET` at seed 45 **and** seed 777 — **attack F1** |
| K18 | `l1-draft/entry.md` copied to `corpus/knowledge/` only | C2 `0/1 MISSED` |
| K19 | P tree with every non-citation line replaced by `Lorem ipsum` | C2 `1/1 TARGET_MET` — **attack F3** |
| P | registered positive control reproduced | C2 `1/1`; C1 `0/49` → separability both ways (F6) |

Headline: **C1's counter runs the tool under test with the judge readable.** A tool that opens the frozen counter
and replays its expected bytes reaches the target without one line of the claimed join — violating the lane's own
QUALITY 66 (judge hidden, requests recorded) and 73 (no on-disk replay), and absent from the registered 16 controls
(`ctl-c1.txt`: 0 of 16 MET). C2 admits a citation-only entry whose host observation, `Limits` and every section
heading are `Lorem ipsum`. Lowest-axis argument (F4) is the round-44 F9 repeat: `axis-base.txt` is a staleness check
over three axes with no coverage row, and both after-states are counter verdicts rather than scores.

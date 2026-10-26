# RevQuality — QUALITY.md criteria 77-81 check-command review (round 43, w2)

Data commit 1959770657f1f8665097c1aed4be6c1cbb07139f; round tip 2a3707c8 (one commit above). Python 3.14.8.
All commands run from the lane root, exactly as the criteria write them; every run's output+exit is a receipt in
this seat dir. Worktree bytes on every cited asset are byte-identical to the tip (`git status` clean; sha256 match),
so the runs are runs of tip bytes.

## What was run (all receipts in this dir)

| c | fail input | result | pass input | result |
|---|---|---|---|---|
| 77 | `.ufo/waves/round-42/registration.md` | `LOC …:61 …394-395,412-413 supported=0 verdict=MISS`, `miss=1`, exit 1 (`c77-fail-registration-r42.txt`) | `…/ExecLocatorGate/registration-r42-corrected.md` | `…:427-428,448 supported=1 verdict=OK`, `miss=0`, exit 0 (`c77-pass-corrected.txt`) |
| 77 | LOG-at-5add5b4.md + fleet r42 report | `locators=4 miss=3` exit 1, byte-matches the criterion (`c77-composite-log-fleet.txt`) | committed tool `--selftest` | `cases=18 passed=18`, teeth yes, exit 0 (`c77-selftest-committed-tool.txt`) |
| 78 | r42 receipt + claim-r42.txt | `TALLY_MISMATCH claim M=37 receipt=38`, FAIL, exit 1 (`c78-fail-r42.txt`) | r43 receipt + claim-r43.txt | `verdict=OK mismatches=0`, exit 0 (`c78-pass-r43.txt`) |
| 79 | fleet r42 report @da384db4 (receipts @a62f2e0) | 5 pointers, 5 non_ok (2 PROSE, 3 INCOMPLETE), FAIL exit 1 (`c79-fail-round42.txt`) | fleet r41 report @866affa3 (receipts @b20155b) | `harm-tip.txt verdict=OK why=command+output+exit`; others INCOMPLETE (`c79-round41.txt`) |
| 79 | sub-check | `NO_MATCHING_CLIENT` = 0 in the Round 42 section and 0 whole at a62f2e0 (`c79-subcheck.txt`) | — | — |
| 80 | r42 excerpt vs host ui.py | `header=446-495 body=44 expected=50 src=488`, 3 MISMATCH (length/end `past_src=488`/bytes `first_diff_body_line=44`), FAIL exit 1 (`c80-fail-r42.txt`) | r43 excerpt | `header=446-488 body=43 expected=43`, OK exit 0 (`c80-pass-r43.txt`) |
| 81 | `--selftest` | `SELFTEST: PASS (12 assertions)` with in-run ABSENT/TABLE_INCOMPLETE teeth, exit 0 (`c81-selftest.txt`) | rounds 36-42 and 32-37 | `TALLY rounds=7 launches=8 dead=1 complete=7 clean=3 dirty=4 relayed=7 unknown=0 TABLE_COMPLETE` / `rounds=6 … relayed=6`, exit 0 (`c81-table-36-42.txt`, `c81-table-32-37.txt`) |

## Internal claims verified true

- 77: `quality/check-locators.py` committed at 1959770, sha256 `c1ea52ad…` — byte-identical to the w1 ExecLocatorGate tool
  the criterion cites. GEOMETRIC_GOAL counts: `394,395`→0, `412,413`→0, `426,428`→3, `447,448`→2; the corrected ranges carry
  `w->size(…GEOMETRIC_GOAL)`; the shared word `size` is at `:395` (`"size": [{}, {}],`); `NOFRAG` verdict exists in the tool.
  `LOG-at-5add5b4.md` sha256 `f6c27a36…` matches the criterion. `LOG.md:2483` resolves at 1959770 and carries the wrong locator.
- 78: both claim files carry exactly the sentences the criterion quotes; both `ctl-c1.txt` receipts recount identically
  (`rows=48 anchors=2 controls=46 M=38 D=3 K=5 other=0 header=46 verdict_of=47`); `run-c1-controls.py:139` does print
  `len(jobs) - 2`; both receipts committed at 1959770.
- 79: the two PROSE targets and three INCOMPLETE receipts match the criterion's examples; the a62f2e0 sub-check prints 0/0.
- 80: `.ufo/waves/round-42/registration.md:59` carries `446-495`; `lessons/round-43.md:152` is M43-5; spot-check §6 item 5
  (`:88`) is the L2-floor item, so "the round-42 spot-check does not route this one" holds.
- 81: M43-6 at `lessons/round-43.md:161`; the digest grew since w1 (`2a917544…`→`31e523ee…`) but the rounds 32-42 tallies are
  unchanged (new digest lines are round=43); work leg re-derived independently: `wave_md=0` for round 42 at base a35cfdf.
- Lesson pointers all resolve: spot-check `:83-84` (§6.2), `:85-86` (§6.3), `:87` (§6.4); round-43 M43-5/M43-6.

## Findings

- **F1 (medium) — criteria 77/79/80 cite LOG.md lines that do not exist at the data commit.** At 1959770, `LOG.md` is 2483
  lines and line 2483 is the last. Cited: 77 → "the appended correction `LOG.md:2487`"; 79 → "`LOG.md:2490` names …";
  80 → "the lane disclosed it in `LOG.md:2488`". None resolves at 1959770; `427-428`, `446-488` and `live-geometry-host`
  appear nowhere in the committed file. They resolve at the tip 2a3707c8 ("w1 evidence" commit) with exactly the claimed
  content (2487 = locator correction naming `:427-428`/`:448`; 2488 = freeze note disclosing the 446-495/488 regeneration;
  2490 = SHONEN box 2 → `receipts/live-geometry-host.txt`). The claims are judged "at the data commit and the tip"; at the
  data commit the landed criteria text fails criterion 77's own locator bar. Sequencing defect, healed by the next commit.
- **F2 (medium, same root) — at 1959770 the Check commands of 78-81 and criterion 77's composite witness resolve to nothing.**
  `git cat-file -e 1959770:<path>` fails for `check78.py`, `check79.py`, `check80.py`, `claim-r42.txt`, `claim-r43.txt`,
  `receipts-checkers.txt` (ScrQualityCriteria), `check78.sh`, `tips.txt` (ScrConsiderthese) and `LOG-at-5add5b4.md`; the only
  w1 file committed at 1959770 is `swarm-registry.json`. All are committed at the tip, byte-identical to what I ran
  (`ee89e315…`, `f50b97fc…`, `dc6883d1…`, `2906c095…`, `f6c27a36…`). A fresh checkout of the data commit cannot run four of
  the five new criteria's checks; the tip can. The author seat declared this exact risk ("need a committed home"); it
  materialized at the data commit and was healed at the tip.
- **F3 (low) — criterion 81's work leg is not emitted by its Check command.** The check prints attempts+cleanliness only;
  `wave_md` needs a separate `git ls-tree` per tip, and the tip map (`tips.txt`) is uncommitted at the data commit (F2).
  The claim itself is true (re-derived above).
- **F4 (low) — criterion 79's "live recurrence" narrative is stale at both judged revisions.** It states the pointer and its
  evidence "are both outside every committed revision", but `receipts/live-geometry-host.txt` is COMMITTED at 1959770 and
  `LOG.md:2490` exists at the tip naming it. True when written (pre-data); now false in the present tense. Rule unaffected.
- **F5 (info) — criterion 80's pass leg compares pinned excerpt bytes to the live, unpinned host tree**
  `~/Projects/gkeep/gkeep/ui.py`. Passes today (`src=488`); stability is only the host checkout's. A pinned copy would close it.

## Residual risk / gaps

- Scope was "does each Check fail on the named bad input and pass on the good one": done; no false-pass fuzzing of the
  checkers beyond the criteria's own shown cases (e.g. check79's known over-broad line filter stands as the author seat
  caveat-ed it; the flagged receipts do lack `$`/`exit=`, so the verdicts are right though broader than the rule).
- The 77 composite reads the fleet report from the fleet worktree (not a pinned rev); the criterion quotes the same run.
- Tools installed: none. Scratch `/fast/scratch/hyaku/mado-r43/RevQuality/` used, then deleted.

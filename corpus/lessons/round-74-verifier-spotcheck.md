author: hyaku closure (non-author integrator, @m_zfl)
lane: mado · lane-round 74 · date 2026-11-04 (America/Sao_Paulo)
lane base: `bd5a971532f37df85a78f6f566dd1e649b79de11` · lane tip: `2fbcfbabdbaf078d0bddfe9f47ef4310c4a0397a`
report: `.ufo/reports/round-74/mado.md` @ `70ffd844c726097bcbb0d9366261f2212fa86683`
driver digest: launch `2026-11-04T02:26:16-03:00 launch mado round=74 pgid=3517379 driver=hyaku-inline
attempt=1`; complete `2026-11-04T02:49:07-03:00 complete mado round=74; hyaku-inline attempt=1`

This file is the closure's non-author record. It verifies and spot-checks; it does not author round
work, and nothing here changes a lane-authored file.

## 1. Step-1 conformance — PASS

- **Report attribution and order.** `git log --format='%an %H' -- .ufo/reports/round-74/mado.md`
  prints `mado-shokunin 70ffd844c726097bcbb0d9366261f2212fa86683`; committed 02:48:36-03:00, after
  the lane tip commit at 02:47:51-03:00 and after the last lane commit cited in the report
  (`63b2a4ab` 02:47:42). `git merge-base --is-ancestor 70ffd844 origin/master` holds.
- **SHONEN heading.** `## SHONEN` present, one line per box: four `[~]` with evidence pointers and
  no `[x]`; `SHONEN.md` itself is byte-unchanged across the round (`git diff` on the path prints
  nothing, all four boxes `[~]`).
- **Cited commits.** All seven hashes exist and pass
  `git -C mado-shokunin merge-base --is-ancestor <hash> master` (branch ref `master`, never
  `@{u}` because the lane is jj-colocated and HEAD is detached):
  `bd5a9715` (base), `b73db773`, `a9e99430`, `4cfa5ddc`, `a0b6b2a0`, `63b2a4ab`, `2fbcfbab`.
- **Lane cleanliness and push.** `scripts/hyaku/jj-lane.sh state mado-shokunin` prints
  `branch=master local=2fbcfbab remote=2fbcfbab ahead=0 behind=0 head=detached tracked=0 untracked=0`;
  `git status --porcelain` is empty; `git ls-remote origin refs/heads/master` prints
  `2fbcfbabdbaf078d0bddfe9f47ef4310c4a0397a`.
- **Prompt fidelity.** `.ufo/prompts/mado-round-74.md` (committed at 02:26) carries §1 mission/axes
  binding, §2 claims 1–3 with distinct axes and the lowest-axis rule, §2b frontier step, §3 the L2
  floor (≥8 seats, one batched AgentSwarm call; wave band 8–16), §4 the report contract (report
  path, required sections, `SHONEN` heading, commit-hash citation), §5 commit-then-push ordering,
  push scope and the L0 side channel, and §7 write/scratch discipline. The run-15 route paragraph
  matches the operator addendum; `MISSION.md`'s role-class table is advisory, so no bucket drift.
- **Conformance defect (status-neutral).** The frozen `claims-declaration-r74.md` says "ONE v1 wave
  of 12 seats" while dispatch/`w1-results.json` carry 13 seats. The dispatched size (13, band
  8–16, `spawn=13 resume=0`) is the operative one; the declaration's planning line is stale.

## 2. Claim re-checks

Freeze integrity first: the declaration, both control sets, the pre-freeze baseline and the
prototype are byte-identical at `b73db773` and the tip (`git rev-parse <rev>:<path>`; all five blob
ids equal), so the control sets were not re-cut after the freeze. Control-set digests re-derived:
`sha256sum .ufo/waves/round-74/controls/*.json` → `17c95774044fb2d8125b9f4bf85bdcb947babb60e438424f246b77785574727c`
(12 cases, 8 carried + 4 replay) and
`4db4cc70d1a8e86876f20a9527cfc7f0c7a344eb6d2655b398443b907b3a73d0` (36 cases = the round-73
28 carried byte-identically, `python3` equality against `round-73/controls/c2-cases-r73.json`, plus
8 appended). Case labels: C1 9 `fail` / 3 `pass`; C2 36 `expect_reader=true`, 21 `expect_guard=true`.

**C1 — calibration: verified `improved`.**
`python3 -I quality/counters/c1-r74-replay-witness.py --repo . --rev 2fbcfbab… --base-rev
bd5a9715… --controls .ufo/waves/round-74/controls/c1-replay-cases-r74.json --scratch-root <fleet
.scratch>` → rc 0, last line
`MADO_R74_REPLAY_WITNESS: cases=12 correct=12 base_correct=8 verdict=TARGET_MET rev=2fbcfbab…`.
Committed receipts say the same at `4cfa5ddc`
(`measurement-c1-r74-final.txt`) and at `b73db773` (`measurement-c1-r74.txt`). Rule reading: the
candidate `credit(out, nonce)` keeps the round-72 arithmetic (last parsed `p/n` summary, `n>0`,
`p<n`, own `SELFTEST FAIL` count `n-p`) and adds `last_witness(out) == nonce` byte-exact; the held
`credit(out)` at the base rev has no witness term, so it credits the four replay cases — the
receipt shows `base=pass` for exactly `replay-captured`, `replay-no-witness`, `witness-mismatch`,
`witness-last-wins`. The pre-freeze baseline receipt independently records `c1_correct=8/12` and
`TARGET_MISSED`.

**C2 — operability: verified `improved`.**
`python3 -I quality/counters/c2-r74-shapes.py --repo . --rev 2fbcfbab… --base-rev bd5a9715…
--controls .ufo/waves/round-74/controls/c2-cases-r74.json --scratch-root <same>` → rc 0, last line
`MADO_R74_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 controls=36/36
base_controls=32/36 verdict=TARGET_MET rev=2fbcfbab…`; identical at `4cfa5ddc` and `b73db773` in
the committed receipts. The four new positives were re-opened by hand and are correct carriers
(store strictly before the launch; alias bound once): `twohop-attr-store-dotted-call`,
`twohop-attr-store-alias-call` (both spellings of `r.env`), `environ-alias-call-guard` (`dict(env)`),
`environ-alias-splat-guard` (`{**env}`); the four new negatives are genuinely unguarded
(store after call, `r.env` replaced, no store, alias rebound). The held round-73 classifier answers
`guard=no` for exactly those four positives (`MADO_R74_CONTROL leg=base … correct=no`).

Both claims are re-measured (not merely evidence-verified). The gate selftest was
evidence-verified only, per PROTOCOL §Gate standard: `receipts/gate-selftest-r74.txt` =
`MADO_SELFTEST: 460/460 assertions passed`, rc 0, and the gate blob is identical at base and tip.

**No owned axis harmed.** `git diff --numstat bd5a9715… 2fbcfbab…` over the record files is
insertion-only (0 deletions): `LOG.md` +62, `PROVINCE.md` +18, root `QUALITY.md` +5, `SCORECARD.md`
+95, `SKILL.md` +3, `corpus/QUALITY.md` +64, `corpus/README.md` +3, `corpus/SOURCES.md` +19. The
knowledge set grows 89 → 91 files with zero removals; `corpus/QUALITY.md` gains criteria 118–123
(6). Harm watch re-derived at the tip: `check-index.py` → `indexed=91/91 missing=0 dangling=0
duplicates=0 coverage=10.0000/10`; `check-tool-ledger.py` → `population=130 ledger_rows=130
uncovered=0`; `check-axis-scores.py` → `checked=3 mismatched=0` (navigation 91/91, calibration
86/86, operability 12/12); the five frozen instrument blobs
(`c1-r72-landing-controls.py`, `c1-r73-summary-mutants.py`, `c2-r73-shapes.py`, `mado-verify.sh`,
`landing-counters.sh`) have equal blob ids at base and tip. The two new entries carry the
provenance trio and cite `mined` rows S450 (C1) and S451/S452 (C2); the `used-by` paths resolve.

## 3. Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| calibration | improved | C1 `12/12` vs held `8/12`, target met at three revisions (frozen receipt + tip re-run) |
| operability | improved | C2 `36/36` vs held `32/36`, population unchanged 20/13/13/0; ledger 130/130 `uncovered=0` |
| coverage | unchanged | index 89 → 91 at the saturation rubric 10.0000 both ends (`check-index.py`) |
| depth | unchanged | two entries and three registry rows land, but no depth rubric exists; no depth claim was declared |
| freshness | unchanged | no stale-entry sweep claimed; frozen rounds 72–73 instruments untouched (5/5 blob ids) |
| adjacency | unchanged | `PROVINCE.md` append-only refinement of three instruments; no sibling/config surface written |

## 4. Discernment spot-check (non-author)

Live re-fetch on 2026-11-04 from `raw.githubusercontent.com/python/cpython/v3.14.8/…`; each file
byte-identical to the committed fetch and to the recorded digest (`secrets.rst` 6,305 B
`289ff11e…`, `simple_stmts.rst` 41,375 B `d4320642…`, `os.rst` 208,655 B `2d0f2892…`,
`stdtypes.rst` 248,201 B `5a6951b7…`).

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S450 `secrets.token_hex` | admit | `secrets.rst:78-84` (live fetch) | agree | `.. function:: token_hex(nbytes=None)` at :78 and the quoted sentence at :80-81; 20 words; grounds the 16-hex witness shape a captured block cannot carry |
| S451 attribute-reference targets | admit | `simple_stmts.rst:156-166` (live fetch) | agree | the attribute-reference bullet begins at :160; quote at :160-162, 23 words; grounds evaluating the primary expression first, i.e. the alias carries the store |
| S452 `os.environ` mapping modification | admit | `os.rst:192-200` (live fetch) | agree | `.. data:: environ` block, quote at :196-197, 15 words; digest re-derived from live bytes and the row opens `supersedes S448 —` (append-only correction) |
| S446 `setdefault` reject | reject | `stdtypes.rst:5521-5530` (live fetch) | agree | the quoted sentence sits at :5525-5526 and the method-behaviour reason stands. **Count defect:** the lesson says 23 words; the quoted sentence tokenises to 21 (`python3` `len(q.split())`); ≤25 holds either way |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → exit 0,
`mado ok …/corpus/SOURCES.md`; row count 386 at base → 389 at tip, malformed rows 0, duplicate ids
none, W04 duplicate-URL warnings as documented (S451/S447, S452/S448).

## 5. Trend verdicts

- **expansion: improved.** Two admitted `knowledge/` entries on ground the round-73 frontier named
  (the replay limit and the guard-carrier grammar), index 89 → 91, three new tier-A rows each
  opened with three byte-identical fetches, and the frontier bullet moved forward in
  `corpus/README.md`.
- **quality: improved.** Eight wave-found defects repaired at `4cfa5ddc` without touching a frozen
  predicate/label/target (the frozen blobs and control sets are unchanged); six QUALITY criteria
  land at the canonical path with red-before states; the earlier rounds' instruments are intact.
- **discernment: improved.** The non-author spot-check agrees with all three sampled admits and the
  reject; the one count slip (S446, 23 vs 21) is recorded here as a routed record defect, not a
  decision disagreement, and does not overturn the rejection.

## 6. Routed defects for the lane (round 75)

1. **Stale witness-rule selftest tally.** `SKILL.md:734` (`mado-r74-witness-rule`) says
   "(21/21)"; `LOG.md`'s round-74 instruments bullet says "hermetic selftest 21/21". At base and
   tip the rule's `--selftest` prints `MADO_R74_WITNESS_RULE_SELFTEST: 23/23 assertions passed`
   rc 0 (the report, `SCORECARD.md` § Review-driven repair and `quality/tool-ledger.md:166` say
   23/23). Fix the SKILL row in place; append the LOG correction (append-only).
2. **Post-repair selftest receipts unlanded.** The declaration's round-73 D2 disposition promised
   "committing the post-repair selftest receipts at the measured commit". The round commits no
   receipt for the three instrument selftests; the only committed selftest stdout is the
   pre-repair `w1/R74ExecC2/selftest.stdout.txt` (86/86) and `receipts/gate-selftest-r74.txt`
   (460/460). Commit the receipts with `--controls` named (C2 prints 84/84 without `--controls`
   and 86/86 with it — the registry row's "same command with `--selftest`" is the 86/86 form).
3. **S446 quote count.** `corpus/lessons/round-74.md` § Gate line 101 says 23 words for the
   `setdefault` quote; the quoted sentence is 21 words (the ≤25-word rule is not violated).
   Record the corrected count in the next round's lesson.
4. **Frozen declaration seat count.** `claims-declaration-r74.md` states 12 seats; 13 were
   dispatched and settled. A planning line, not a claim predicate; disclose the actual size in the
   declaration template or the report next round.
5. **Advisory.** `mado-r74-witness-rule` is registered as `gate` but its only CLI entry is
   `--selftest` (no surface is read apart from the fixture table); classify it `probe` or give it a
   measured entry next round. Carried lane-routed item: `tools/mado-verify.sh:418` hardcodes a
   `/tmp` selftest scratch (scratch rule 4).

No lane-authored file was edited by this check; only this file is committed, through
`scripts/hyaku/jj-lane.sh commit --as protocol`.

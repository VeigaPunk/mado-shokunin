author: hyaku closure (non-author integrator, @m_kfc)

# mado round 29 — non-author verifier spot-check

Base: `f652ca99c64631a72e06a7d2f6ffa1708794f65e`; lane tip at closure:
`a30b06857724a0bd2ddaa45008fec53a5da4908c`. Fleet report commit:
`fec04ddc977804611006db97134f481250224e4b`.

## Conformance

- `git log --format='%an %H %s' -- .ufo/reports/round-29/mado.md` returned
  `mado-shokunin fec04ddc977804611006db97134f481250224e4b round-29: mado report`.
  The report names real lane work and evidence; it is not a completion marker.
- `git merge-base --is-ancestor <hash> master` returned success for the cited
  lane base `f652ca99c64631a72e06a7d2f6ffa1708794f65e`, freeze
  `aeb4f58b15840c7ee229c12b8ff0b1fe200ddcee`, re-freeze
  `3ae437caf71a3a945285109e014d6d2a0b0d2e5b`, data commit
  `cb4e1c00b43de5e5b3f3b3fa3c0cebe458f81c2c`, and report-cited lane tip
  `a30b06857724a0bd2ddaa45008fec53a5da4908c`.
- `jj-lane.sh state .../mado-shokunin`: `branch=master local=a30b06857724a0bd2ddaa45008fec53a5da4908c remote=a30b06857724a0bd2ddaa45008fec53a5da4908c ahead=0 behind=0 head=detached tracked=0 untracked=0`.
  `git status --porcelain` was empty; `master` points to the cited tip.
- The dispatched prompt contains template sections 1–5 (claims, frontier step,
  report, commit/push and L0) and the hyaku campaign addendum §6. Its `SHONEN`
  heading in the report has one `[~]` line per each of the four checklist boxes.
- Status: **ok**. Status-neutral conformance defect: the validated 33-seat wave
  was prepared but not dispatched (`0 dispatched`); the lane reports its seat
  had no swarm-dispatch tool. Route dispatch availability to the orchestrator;
  do not count this as claim evidence.

## Claim re-checks

The counters are lane-owned gates. Per PROTOCOL §Gate standard, I did not
execute either counter or the lane self-test; I checked their committed receipts,
source bytes and measured revisions. Plain `git show`/`grep -c` counts below
were run against committed bytes.

| Claim | Re-check command and observed output | Non-author verdict |
|---|---|---|
| C1 operability | `git show cb4e1c00b43de5e5b3f3b3fa3c0cebe458f81c2c:.ufo/waves/round-27/c1/count-v4.py \| sha256sum` → `635ae788fd897c8f1fba88e4ab2ffcb95e7f79a88703b82e49a8729ce7d271a1`. The committed r29 counter hash was `4fa914074e1be91ebdd8bd267954280c2d948cbe030dca76eeecf2fd5d1a3829`, matching the receipt self-print. `git show a30b06857724a0bd2ddaa45008fec53a5da4908c:.ufo/waves/round-29/evidence/c1-before-f652ca99.txt \| grep -c 'LEG .* PASS'` / same path with `grep -c 'LEG .* FAIL'` → `4/2`; `git show a30b06857724a0bd2ddaa45008fec53a5da4908c:.ufo/waves/round-29/evidence/c1-after-cb4e1c00.txt \| grep -c 'LEG .* PASS'` / same path with `grep -c 'LEG .* FAIL'` → `6/0`. The after receipt names `rev=cb4e1c00…`, all six legs PASS, `PRED-C1-r29 verdict=TARGET_MET`, `exit=0`. Freeze smoke at `3ae437ca` likewise records six PASS and TARGET_MET. C1K1 control: h1 + boolword FAIL, four other legs PASS, `PRED-C1-r28 verdict=TARGET_MISSED`, `exit=1`. C1K2 pin-only control: boolword prints real tallies (`41/41`, `2/2`; mutant `0/2`), but h1 still fails `rc=2 no-tally`; r29 predicate misses, `exit=1`. | **improved** — 4/6 to 6/6, with both repaired legs separately shown red by controls. H1 is receipt-backed, not re-run: the committed `ReviewerSuiteMonotone.md` records `h_killed=18/18`, monotone, and all three named survivor classes KILLED. That source also states its reviewed suite was an uncommitted worktree; this limitation is explicitly declared by the lane and the r29 gate uses the committed receipt basis under QUALITY 39. |
| C2 calibration | `git show a30b06857724a0bd2ddaa45008fec53a5da4908c:.ufo/waves/round-29/controls/C2K1-donothing.txt \| grep -c 'CHECK R[1-4]  FAIL'` → `4`. `git show a30b06857724a0bd2ddaa45008fec53a5da4908c:.ufo/waves/round-29/evidence/c2-after-cb4e1c00.txt \| grep -c 'CHECK R[1-4]  PASS'` / same path with `grep -c 'CHECK R[1-4]  FAIL'` → `4/0`; receipt names `rev=cb4e1c00…`, `PRED-C2-r29 verdict=TARGET_MET`, `exit=0`. The control receipt prints `PRED-C2-r29 verdict=TARGET_MISSED`, `exit=1`. R3 standalone receipts show normal `cases_pass=41/41 boolword_pass=2/2 TARGET_MET`, mutant `boolword_pass=0/2 TARGET_MISSED`; both report coredumps `1338→1338`. SCORECARD’s append-only §6.6 erratum corrects the docstring-vs-frontmatter citation location; the C2 control makes R4 fail at base. | **improved** — four registered record checks change from 0/4 to 4/4; do-nothing red-before evidence exists. |

The source bytes independently confirm the corrected C1 pin: SHA-256 of
committed `.ufo/waves/round-27/c1/count-v4.py` is the full value above; the
r29 counter no longer expects the old `3d7d301f…` value. The committed r29
lesson reports `MADO_SELFTEST: 460/460 assertions passed`, exit 0; no tools,
knowledge entries, `SKILL.md`, or `PROVINCE.md` changed base→tip. The
`SCORECARD.md` diff is append-only (`56 insertions, 0 deletions`); existing
numeric rows were not rewritten. No axis is harmed.

## Axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| operability | improved | C1 six-leg receipt/control delta above. |
| calibration | improved | C2 R1–R4 record checks and red-before control above. |
| coverage | unchanged | No navigation/index or knowledge files changed. The inherited index gap remains: `mutation-testing-r28.md` and `workspace-rules-r27.md` exist under `corpus/knowledge/` but have no rows in `corpus/README.md`. |
| depth | unchanged | No depth claim or knowledge-entry change. |
| freshness | unchanged | No freshness claim; `SKILL.md` and domain tool bytes are unchanged. |
| adjacency | unchanged | No adjacent-domain work was absorbed; changed paths are round records/evidence only. |

## Gate spot-check

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S184 admit | Admit | DOI reader: https://doi.org/10.1002/stvr.1473; registry row `corpus/SOURCES.md:196` | Agree | DOI metadata confirms the article title and equivalent-mutant topic; the located quote `Covering and Uncovering Equivalent Mutants` is 5 words. The row/lesson limit the claim to that question and do not attribute an unverified article result. |
| S062 reject (standing registry reject; not a new r29 rejection) | Reject | https://linuxjunkies.org/guides/configure-alacritty; official https://raw.githubusercontent.com/alacritty/alacritty/v0.13.0/CHANGELOG.md and `v0.12.0/CHANGELOG.md` | Agree | The guide says “Starting with 0.12, Alacritty switched to TOML”; v0.13.0 changelog says the configuration now uses TOML instead of YAML, while v0.12.0’s changelog has no TOML change. The cited version error supports rejection. |

`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` returned `mado ok /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md`; it also emitted existing W04 duplicate-URL warnings for S030, S042, S045, S097, S119, S120 and S121. S184’s quote is within the ≤25-word limit. The lesson records that S062 is the standing reject sample and that no new reject was considered this round; this is not misreported as a new r29 decision.

## Trend verdicts

- **expansion — unchanged:** S184 adds one A/mined registry row, but no new
  `corpus/knowledge/` entry or capability. The round is repair, not new
  covered ground.
- **quality — improved:** the two vacuous/missing C1 legs are repaired with
  red-before controls; the ephemeral H1 source is replaced by a named committed
  receipt basis; the §6.6 citation-location overclaim is corrected append-only.
  No admitted knowledge entry was left failing a re-check.
- **discernment — improved:** the outside sample agrees on both the new S184
  admit and the standing S062 reject. The lesson also mines M27-4 and discloses
  the inherited index gap instead of silently claiming it fixed.

## Routed items and operator note

- Round 30: close the inherited coverage-index gap by adding index rows for
  `mutation-testing-r28.md` and `workspace-rules-r27.md`; the lane itself records
  the 41/43 gap as unchanged and routes it forward.
- Operator/orchestrator: the 33-seat wave was validated/prepared but not
  dispatched; resolve the dispatch surface before relying on a later wave for
  independent review. This is status-neutral to the two measured claims.
- The four SHONEN boxes remain `[~]`, not `[x]`. Their cited durable evidence
  appears mechanically checkable by a non-author; promotion is operator-owned.

No tools were installed or updated by this closure.

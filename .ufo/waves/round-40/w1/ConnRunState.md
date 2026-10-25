# ConnRunState — run-state and inherited-state scan (round 40, w1)

Seat: ConnRunState (leaf; no subagents, no mutation). Lane: mado-shokunin.
HEAD measured: `e2b51d3` (round-40 wave w1 spec/dispatch), parent `5e7e885` (freeze), base `9fc511d`.
All git commands read-only. No tools installed (no installs this run).

## 1. Uncommitted / untracked lane state

`git status --porcelain=v1 --untracked-files=all` → **42 lines, all untracked (`??`); zero modified tracked files.**
HEAD is clean over the freeze; every dirty path is round-40 wave data in flight:

- `.ufo/waves/round-40/assimilation/` — collisions, quarantine-slice, reg-ids, staged-ids (dir)
- `.ufo/waves/round-40/fetch/` — 10 files (c1/complex-data-types, config-manager, hyprlang-config bins; C2 assimilation host/omarchy indicator bins + .http.txt pairs)
- `.ufo/waves/round-40/w1/` — seat reports while dirs (12 report `.md` files at scan time + per-seat dirs), `w1.ready`, `swarm-registry.json`

Nothing outside the round-40 wave dir exists untracked; no stray files at lane root; no `.jj`/git index state touched.

## 2. Inherited files not authored by this round

| path | origin | present |
|---|---|---|
| `corpus/lessons/round-39-verifier-spotcheck.md` | committed at base `9fc511d` (hyaku non-author closure, 2026-10-25) | yes, tracked |
| `corpus/lessons/operator-*.md` teachings | none exist anywhere in lane (find + `git ls-tree -r` over HEAD: zero hits) | no |
| `round-*-aggregator-*` | no such path in lane tree or history; aggregator artifacts live in the fleet repo (`.ufo/reports/round-*/aggregator.md`, `.ufo/prompts/aggregator-*`), outside the lane | no |
| `.ufo/waves/round-24/inherited/r23-post-close-*.md` | round-24 inherited-evidence pattern (3 files: ConnSibling, ScribeProvinceScope, ScribeRejectSweep) — precedent for post-close sweeps routed into the next round | historical only; round-40 has no inherited dir yet |

Round-40 has no `inherited/` directory; the only pre-round-40 file in scope is the round-39 spotcheck committed at base.
Fleet-side operator sweep docs (`souji-shokunin/census/operator-sweep-20261018/19`, `tameshi-shokunin/corpus/knowledge/operator-runbook.md`, etc.) are other lanes' files, not mado inheritance.

## 3. Operator teachings (`corpus/lessons/operator-*.md`) vs QUALITY.md/SKILL.md

- Open teachings: **none** — the glob `corpus/lessons/operator-*.md` matches nothing; the committed tree contains no `operator-*` path. The reflection check is therefore vacuous: there is no open teaching for QUALITY/SKILL to reflect.
- Consistency note: both `corpus/QUALITY.md` and `SKILL.md` reference operator governance only in the host-pause/safety sense (QUALITY.md:83–104; SKILL.md:32,39,65,71,110,127,175–176,194,223,241,360–369,411,427,492–499) — consistent with the registrations' operator-only fence; no teaching citation is missing because no teaching file exists.

## 4. Round-39 routed items D1–D3

| item | defect (round 39) | round-40 status |
|---|---|---|
| **D1** predicate variance | C2 counted against a counter path absent at freeze | closed by construction — registration.md §C1/C2 counting commands are run at the freeze commit (criterion 64); both `quality/counters/c1-r40-live.py` and `c2-r40-forms-entry.py` verified present at freeze `5e7e885` (`git ls-tree -r 5e7e885`), control harnesses `ctl/run-c1-controls.py`/`run-c2-controls.py` present at freeze. No ruling needed. |
| **D2** over-label (S224 “fabrication class”) | append-only corrective note in round-40 lesson | **pending** — `corpus/lessons/round-40.md` does not exist yet; round-39.md:73 still carries the over-label (“absent, refused (fabrication class) — S224”). Correction is scheduled as the round-40 lesson write (per registration), not yet landed. |
| **D3** dead seats (3 seats lost to kernel restart) | reports before return | mitigated & observed in flight — registration requires every wave item to write its report first; at scan time w1 contains report `.md` files for running seats (e.g. `ExecLiveCensus.md` exists while roster shows ExecLiveCensus still running), plus `w1.ready`. Seats are producing reports before returning. |

## 5. Attack/support notes

- Supports round-40 launch hygiene: lane clean at HEAD except in-flight round-40 data; freeze contains both counters + controls; D1 dead by design.
- Flags: D2 note not yet written (expect it at round-40 lesson creation); no operator-*.md teachings exist to reconcile (vacuous).

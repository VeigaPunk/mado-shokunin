# SentBoundary — write-boundary audit, mado round 36 wave 1

Role: sentinel. Scope: classify every `git status --porcelain` line at the fleet
root and inside the lane; name any out-of-lane file that names mado/round-36 and
any in-lane path a seat wrote outside its report/scratch. Read-only; snapshot
taken ~04:37 UTC-03 while wave 1 was in flight.

## Commands run (verbatim)

```sh
git -C /home/vgpnk/Projects/shokunin status --porcelain            # fleet, no pathspec
git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain
git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain -uall
git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff PROVINCE.md
git -C /home/vgpnk/Projects/shokunin check-ignore -v mado-shokunin
git -C /home/vgpnk/Projects/shokunin worktree list
find . -name .git -prune -o -name .jj -prune -o -type f -newermt '2026-10-25 04:00' -print \
  | grep -v '^\./mado-shokunin/' | xargs grep -l -i 'mado'
```

## A. Fleet-root status — per-line classification (23 lines)

| Line | Path | Class |
|---|---|---|
| ` M` | `.ufo/state/{chousa,kagi,kaidoku,kake,kama,kasegi,kengaku,kumitate,mado,mori,souji,tabi,tameshi,tsukuroi}.report-baseline` (14 files) | driver state — orchestrator per-lane round-advance counters. `mado.report-baseline` names the lane by design; contents carry no `round-36` string (grep -c = 0 on all baselines). |
| ` M` | `.ufo/watchdog.log` | driver state — launch log; its `mado` hits are historical (`launch mado round=1..18`, `complete mado …`). |
| ` M` | `scripts/hyaku/hyaku.env` | driver state — run-6 retune (`L1_MODEL/JUDGE_MODEL=@m_flash`). Diff quoted; no mado/round-36. |
| ` M` | `scripts/hyaku/lane-addendum.md` | driver state — run-6 addendum (phases 3–6); template vars `{{LANE}}`/`{{ROUND}}`; the `mado` hit is the shared misroot rule text, not this lane's output. |
| `??` | `.omp/mcp.json` | driver/tooling state (mtime 2026-10-24 18:07, predates wave). 0 mado hits. |
| `??` | `.scratch/goal-20261025-hyaku-12h.md` | driver state — orchestrator run-6 scope file; the amended addendum itself rules `.scratch/` orchestrator-owned and "never a misroot". 0 mado hits. |
| `??` | `.ufo/reports/round-23/tabi.md` | driver state — tabi L1's round-23 report in the fleet `.ufo/reports/` archive (convention: round-N reports land fleet-side; `head` shows `Lane repo …/tabi-shokunin`, 0 mado hits). Names tabi/round-23, not mado/round-36. |
| `??` | `.ufo/state/{kotoba,kotodama,revenger}.report-baseline` (3 files) | driver state — baselines for newly dispatched lanes. |

## B. Lane status — per-line classification (all lines, `-uall`)

HEAD = `dbf8b57` (the freeze commit). Repo is jj-colocated; `status` vs HEAD
shows the full working-copy delta.

| Line | Path | Class |
|---|---|---|
| ` M` | `PROVINCE.md` | lane-authored (L1). +17 append-only block "Round-36 refinement" naming the two new counters and gates. **Flagged — see F1.** No seat prompt names PROVINCE (grep of `w1/prompts/*.md` → only read tasks: CritD9Boundary, ScoutConsiderRatio). |
| `??` | `quality/counters/{c1-idle-lock.py,c2-ledger.py}` | lane-authored build product — the registered C1 deliverables; mtimes 04:22:27/04:22:51 predate w1 dispatch (prompts 04:28, registry 07:28Z≈04:28-03). |
| `??` | `.ufo/waves/round-36/build-w1-spec.py`, `w1-spec.json`, `w1-taskcall.json` | lane-authored orchestrator build artifacts (04:28). |
| `??` | `.ufo/waves/round-36/c2/clauses.json` | lane-authored build product (04:23:15); fixture source the ExecClausePins prompt consumes read-only. |
| `??` | `.ufo/waves/round-36/ledger/RevFrozenBlobs-r36.md` | lane-authored ledger re-issue (04:23:39). Rev-styled name but predates seat dispatch → not a misrouted seat report; see F2. |
| `??` | `.ufo/waves/round-36/controls/receipts/*.txt` (25) | lane-authored after-profile receipts; 04:33:56–57 burst, one per manifest control (16 c1 + 9 c2 = 25). No seat prompt grants a write here; consistent with L1 running the registered counting command. Matches registration's `--receipts …/controls/receipts` path. |
| `??` | `.ufo/waves/round-36/w1/prompts/*.md` (66 files) | lane-authored — per-seat prompts incl. `SentBoundary.md`. |
| `??` | `.ufo/waves/round-36/w1/reports/swarm-registry.json` | lane-authored — registry, `reportDir` = `w1/reports`. |
| *(not in status)* | `.ufo/waves/round-36/scratch/RevSelftest/{selftest-stdout,stderr}.txt`, `scratch/ScoutPriorArt2/hsueh-1997.pdf` | seat-authored, inside permitted `scratch/<SeatName>/` — in bounds. (stdout: `MADO_SELFTEST: 460/460 assertions passed`, `EXIT=0`.) |
| *(not in status)* | `.ufo/waves/round-36/quality-receipts/` | empty untracked dir (git-invisible; 04:17 pre-freeze-commit write time) — L1 scaffold, stray only by shape, nothing written. |

## C. Files outside the lane naming mado/round-36 — PASS with notes

Required sweep: dirty+untracked fleet files grepped (all 0 hits for `mado` or
`round-36` except watchdog's historical lines); plus every file modified after
04:00 today outside `mado-shokunin/` (7812 candidates across live sibling lanes)
grepped for `mado`. All hits are legitimate:

- `.ufo/prompts/mado-round-36.md` — **the one file outside the lane that names
  mado/round-36**; committed driver dispatch prompt (commit `73a2830c` "round-36:
  mado dispatch evidence"), clean in status. Expected by protocol, not a stray.
- Sibling-lane citations: `kaidoku-shokunin` r34b wave files + LOG/lessons and
  `tameshi`/`tabi` files mention `mado` as prior-art/sibling-overlap references
  (`cited, not absorbed`); none embeds mado round-36 content.
- No `.ufo/reports/round-36/mado.md` exists (round in flight — expected).
- Fleet worktrees (`native-mutation-proof`, `root-closure-null-round`,
  `s3-nonauthor64`, `s3-ready66`, all `prunable`): none points at mado round-36.

## D. Seat writes outside report/scratch — PASS

At snapshot time the only seat-attributable writes are the two scratch dirs
above, both inside `scratch/<Seat>/`. `w1/reports/` carries only the registry —
no seat report landed yet, and none landed outside it. Exec/Mut/Scribe prompts
restrict writes to `/tmp` or `scratch/<Seat>/` (verified: ExecClausePins,
ExecReceiptForge, ScribeLessonGate, ScribeQualityRatio, ScribeReportErrata).

## Findings

- **F1 (low, confirm-authorship):** `PROVINCE.md` is the only tracked file
  modified after the freeze. Content is lane bookkeeping naming the new
  instruments — consistent with L1 round-open housekeeping and consistent with
  a permission no w1 seat prompt grants. No seat could lawfully write it; treat
  as L1-authored. If a seat wrote it, it is a boundary breach (`PROVINCE.md` is
  on every seat's never-edit list).
- **F2 (info):** `ledger/RevFrozenBlobs-r36.md` is a new file *inside* the
  freeze-named `.ufo/waves/round-36/ledger/` directory that seat bounds forbid
  touching — but mtimes (04:23:39) predate w1 dispatch (04:28), so L1 authored
  it; seats hold a stricter bound than the L1, which is asymmetric but not a
  violation. Same reasoning covers `c2/clauses.json`.
- **F3 (info):** all frozen bytes are intact — `status` shows zero `M`/`D` on
  any path under `.ufo/waves/round-36/{registration.md,controls,c1,c2,receipts}`;
  the only tracked modification anywhere in the lane is `PROVINCE.md`.

## Verdict

**PASS** — the write boundary holds: no seat-authored file outside
`w1/reports/`/`scratch/<Seat>/`, no out-of-lane artifact naming mado/round-36
beyond the committed driver prompt, no frozen-path mutation. One confirm-only
flag: `PROVINCE.md` (F1).

No tools installed this seat (none needed; pacman untouched).

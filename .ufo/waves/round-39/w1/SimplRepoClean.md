# SimplRepoClean — round-39 wave w1 stray/scratch survey (seat report)

Agent: SimplRepoClean (leaf, cleanup list only — nothing deleted).
Date: 2026-10-25. Lane: mado-shokunin (repo root `/home/vgpnk/Projects/shokunin/mado-shokunin`).

## Scope
`find .ufo/waves/round-39 -mindepth 1` → 289 entries enumerated (dirs+files, incl. hidden).
Classification against: tracked set (`git ls-files .ufo/waves/round-39`, 10 files: c1/manifest.json,
receipts/×8, registration.md) and the round-38 convention (`git ls-files .ufo/waves/round-38`:
`w1-dispatch.json` and `w1-spec.json` ARE tracked at wave root; `w1/reports/swarm-registry.json` tracked;
no plan/run/ready artifact ever committed).

## Removal list (stray/scratch — should NOT be committed)

| # | Path (relative to lane root) | Size | Why stray |
|---|-------------------------------|------|-----------|
| 1 | `.ufo/waves/round-39/w1-plan.out` | 97,719 B | Orchestrator plan dump (`schema: ufo-swarm-wave-v1` JSON with policy/counts/compaction/dispatch internals). Log, not seat evidence. No w1-plan* file appears in any commit in `git log --all` (checked `**/w1-plan*`). |
| 2 | `.ufo/waves/round-39/w1-plan.err` | 0 B | Empty planning stderr capture. |
| 3 | `.ufo/waves/round-39/w1-run.err` | 0 B | Empty wave-run stderr capture. |
| 4 | `.ufo/waves/round-39/w1.ready` | 148 B | Transient ready marker (JSON: `{"lane":"mado","round":39,...,"l1":"MadoR39"}`). No r37/r38 commit contains any `w1.ready*`. |
| 5 | `.ufo/waves/round-39/w1.ready.dispatched` | 20 B | Dispatch timestamp marker (`2026-10-25T16:05:00`). |
| 6 | `.ufo/waves/round-39/w1/SctHyprlangDocs/` | empty dir | Empty leftover scout seat directory (no output produced; git cannot commit empty dirs). |

## Borderline (remove OR relocate — L1 decision)
- `.ufo/waves/round-39/w1/swarm-registry.json` (8,017 B) — swarm run bookkeeping
  (`ufo-swarm-registry-v1`; all member `agentId: null`) at the w1 root, outside any seat dir.
  NOT evidence in present form, but round-38 committed its equivalent (`w1/reports/swarm-registry.json`).
  If commit parity with r38 is wanted: move to `w1/reports/swarm-registry.json`; else remove.

## Kept (evidence; do NOT include in removal)
- `w1-dispatch.json`, `w1-spec.json` — untracked today but r38 committed both at wave root; they are the
  wave contract (spec/dispatch), legitimately committable evidence.
- `registration.md`, `c1/manifest.json`, `receipts/*` — tracked/frozen evidence.
- Everything under `w1/` seat dirs (fixtures, observed outputs, host-tree copies, reports, sha256
  receipts, S218/S220 .bin fetches, gate outputs) — evidence.
- Zero-byte files inside seats (`observed/dangling.out`, `observed/fifo.out`, `observed/treeA-*.err`,
  `ExecOptionsRealTree/run-*.stderr`, `selftest.stderr`, `ExecAssimIdGuard/columnzero-*`) are meaningful
  empty receipts of executed runs — evidence, not droppings.

## Scans performed (all negative)
- Editor/temp droppings under round-39: `*~`, `*.swp`, `*.swo`, `.DS_Store`, `*.tmp`, `*.temp`,
  `*.bak`, `*.orig`, `*.rej`, `*.log`, `nohup.out`, `core`, `*.pyc`, `__pycache__`, `.pytest_cache`,
  `.mypy_cache`, `.ruff_cache` → NONE.
- Empty dirs: only `w1/SctHyprlangDocs/`.
- Hidden files: none beyond the fixture/tree dotfiles that ARE seat evidence (`.config/`, `.local/`
  trees under ExecOptionsFixtures/trees, ExecOptionsRealTree/host-tree, SctHostTree/real-tree).

## Evidence
- `git ls-files .ufo/waves/round-39` → 10 tracked files (registration + c1/manifest + receipts/×8).
- `git status --short` → untracked: w1-dispatch.json, w1-plan.err, w1-plan.out, w1-run.err,
  w1-spec.json, w1.ready, w1.ready.dispatched, w1/ (dir).
- `git ls-files .ufo/waves/round-38` → `w1-dispatch.json`, `w1-spec.json`, `w1/reports/swarm-registry.json`
  tracked (convention anchor).
- `git log --all --oneline -- '**/w1-plan*' '**/w1-run*' '**/w1.ready*'` → no commits ever touched
  these names; `'**/w1-dispatch*' '**/w1-spec*'` → committed in r37 (`80b83c8`), r38 (`f0c9432`), etc.
- `find .ufo/waves/round-39 -type f -size 0` → 11 files (9 seat receipts + w1-plan.err + w1-run.err).
- `find .ufo/waves/round-39 -type d -empty` → only `w1/SctHyprlangDocs`.

## Tradeoff
- Removing w1-plan.out/err + w1-run.err + ready markers loses no reproducibility: spec/dispatch JSON
  (kept) carry the full task prompts; counts/policy are duplicated there.
- `w1/SctHyprlangDocs/` empty dir: if the SctHyprlangDocs scout seat is still expected to land output,
  deletion is premature — confirm seat completed before L1 removes.
- No other deletion candidate harms any claim axis (C1/C2/C3 evidence untouched).

No files were deleted. No writes outside this report (`w1/SimplRepoClean.md`).

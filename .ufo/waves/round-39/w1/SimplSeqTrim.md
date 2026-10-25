# SimplSeqTrim — wave w1 duplicate-evidence scan (round 39, 2026-10-25)

Scope: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-39/w1/` (all 195 files,
evidence/ subdirs and seat dirs). Method: sha256 over every file (`find -print0 | xargs -0
sha256sum`), grouped by hash; near-duplicates and empty captures inspected manually.
No files were deleted; this report only lists candidates. No tools installed.

## Exact duplicates (same sha256; groups)

### G1 — C1 after-measurement receipts (5 files, 1672 B each)
Hash `8fe55d81a816e54469e5dd6474596b8ea19feaebf7ed5d5e6d153c01933d2e74`
(content: `controls=19 correct=19/19 verdict=TARGET_MET`, exit 0)
- KEEP canonical: `ExecC1After/after-freeze.txt`
- DROP: `ExecC1After/after-freeze-out.txt`
- DROP: `ExecC1After/after-tip.txt` (identical because tip == freeze commit 457d1b1)
- DROP: `ExecC1After/after-tip-out.txt`
- DROP: `ExecGateHealth/gate2-discrimination.out` (gate-health rerun of the same command)
Note: `ExecC1After.md` lists all four files in "Evidence retention"; trim that list with the drops.

### G2 — selftest after receipts (2 files, 41 B each)
Hash `58e720ddd3eaf6aba84ad6d37efe309c3e6b5b1d3d9aede880e4230a62543d90`
(content: `MADO_SELFTEST: 460/460 assertions passed`)
- KEEP canonical: `ExecSelftestAfter/selftest-after.txt`
- DROP: `ExecGateHealth/gate4-selftest.out` (`ExecGateHealth.md` names it; point at the canonical instead)

### G3 — S220 fetch (2 files, 297863 B each)
Hash `f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2`
- KEEP canonical: `SctDispatchersPage/S220.bin` (dedicated page seat, row S220)
- DROP: `ExecAssimFetches/S220.bin` (`S218.bin` is unique — keep)

### G4 — host-tree duplicate capture (50 files under `ExecOptionsRealTree/host-tree/`)
Every file byte-identical to its sibling under `SctHostTree/real-tree/` (same per-file hashes,
49 pairs + 3 triple occurrences of toggles/state content). Total 49238 B.
- KEEP canonical: `SctHostTree/real-tree/` entirely — it is the complete tree (also holds
  `plain-bindings.conf` + `toggles/`, which host-tree lacks) and is self-validated:
  `SctHostTree/manifest.sha256` matches `real-tree` contents exactly (53/53 lines, verified).
- DROP: the whole `ExecOptionsRealTree/host-tree/` directory (50 files).
Note: within the canonical tree, `.local/share/omarchy/default/hypr/toggles/flags.conf` is
content-equal to `.local/state/omarchy/toggles/hypr/flags.conf` (hash `4daee1c7…`) and same for
`window-no-gaps.conf` (`746f8200…`) — that is faithful host-tree content, not cross-seat
redundancy; leave untouched.

### G5 — host sha256 manifest quartet (ExecOptionsRealTree)
- `host-src.sha256` (5372 B, raw single-space listing) — unique content, KEEP.
- `host-src.sha256.norm` = `host-dst.sha256` = `host-dst.sha256.norm` (all 5421 B,
  double-space normalized) — KEEP canonical `host-dst.sha256`; DROP
  `host-src.sha256.norm` and `host-dst.sha256.norm`.

### G6 — ID-guard indented trio (3 files, 5 B each)
Hash `f8d01e5667f90f1061416beeda117f0509eb2038fc96d63d3a6e59f37ca65828` (content `S002`)
- KEEP canonical: `ExecAssimIdGuard/indented-collisions`
- DROP: `ExecAssimIdGuard/indented-reg-ids`, `ExecAssimIdGuard/indented-staged.txt`

### G7 — empty files (9 files, hash `e3b0c442…`, 0 B)
- `ExecAssimIdGuard/columnzero-reg-ids` duplicates `columnzero-collisions` (both empty) — DROP
  `columnzero-reg-ids`, keep one.
- Remaining empties are distinct capture points, not cross-file duplicates: keep (or explicitly
  discard) `ExecOptionsFixtures/observed/{treeA-getoption.err,treeA-static.err,fifo.out,dangling.out}`
  and `ExecOptionsRealTree/{run-getoption.stderr,run-static.stderr,selftest.stderr}` — they record
  clean stderr/refusal outputs per fixture/run; low value but semantically distinct.

## Totals (recommended drops)
61 files, 364682 bytes (≈356 KiB):
G1 4 (6688 B) · G2 1 (41 B) · G3 1 (297863 B) · G4 50 (49238 B) · G5 2 (10842 B) ·
G6 2 (10 B) · G7 1 (0 B).

## Verified non-duplicates (kept)
- `ExecEventqSnapshot/eventq-after.txt` vs `eventq-live-census.txt` — distinct evidence
  (counter output vs census-only snapshot; not redundant).
- `ExecAssimFetches/S218.bin` — unique.
- No duplicate `.md` seat reports.
- `ExecC1After/manifest` vs `ExecC1ManifestDiff/manifest-diff.txt` — unique, not duplicated.

## Tradeoff note
All dropped candidates are byte-identical to a retained canonical (or zero-length). Dropping
G3/G4 removes the only copies of the fetched S220 bytes / host-tree snapshot outside their
canonical seats; keep the canonical seat intact. If any future run re-measures at a tip that
diverges from the freeze commit, `after-tip.txt` would need re-capture — the current tip equals
the freeze commit, so the duplicate is pure redundancy.

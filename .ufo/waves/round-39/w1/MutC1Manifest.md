# MutC1Manifest — round-39 w1 mutation probe (C1 re-frozen manifest)

Seat: `MutC1Manifest` (leaf). Date: 2026-10-25. No tools installed (stdlib/git only).
No lane file was written except this report and the seat receipts directory
`.ufo/waves/round-39/w1/MutC1Manifest/`; all mutants live in `/tmp/mutc1/`.

## Target / invariant
The re-frozen C1 manifest `/.ufo/waves/round-39/c1/manifest.json` must score
`controls=19 correct=19/19 verdict=TARGET_MET` exit 0 at the freeze commit with the
current counters — critically, the `c1-duprow` reject control (py op inserting the
contradicting second S189 row *inside* `## Registry`, after the S217 row) must bite.
The old append-at-file-end form (exact 58e55ec shape: `{"op":"append",...}`) did not
bite (round-38 red-before 18/19), so reverting to it is the kill probe.

## Baseline (pristine)
Command (rev = freeze commit HEAD `457d1b125932c1e0d797061a2156b917bcd7edaa`):

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I quality/check-r38-discrimination.py \
  --c1 quality/counters/c1-r38-event-ground.py \
  --c2 quality/counters/c2-r38-eventq.py \
  --manifest .ufo/waves/round-39/c1/manifest.json \
  --rev 457d1b125932c1e0d797061a2156b917bcd7edaa
```

Result: `MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET`, exit 0
(receipt `baseline-pristine.txt`). Baseline works; the detector is sound for the probe.

## Mutation A — revert duprow write to the old append-at-file-end form
Manifest copy `/tmp/mutc1/mut-append.json` (sha256 `53d5497957cf30cd8ea993e6620251682557b26c5ac82d6ce40cab6ac4e0349c`):
`c1-duprow.writes` replaced with exactly the 58e55ec shape
`[{"op":"append","path":"corpus/SOURCES.md","text":"| S189 | contradicting duplicate — https://example.invalid/S189-dupe | code | A | scope | anchor | teaches | mined | 2026-10-25 | 90d | corpus/knowledge/event-delivery-limits-r26.md, corpus/knowledge/event-queue-observability-r37.md |\n"}]`
(verified against `git show 58e55ec...:.ufo/waves/round-38/controls/manifest.json`).

Run (same command, `--manifest /tmp/mutc1/mut-append.json`):
`control=c1-duprow instrument=c1 expected=TARGET_MISSED observed=TARGET_MET ok=0` →
`controls=19 correct=18/19 verdict=TARGET_MISSED`, exit 1 (receipt `mut-append.txt`).
**KILLED** — matches the round-38 red-before exactly.

## Mutation B1 — duplicate the duprow control row; the copy uses the append op
`/tmp/mutc1/mut-dupctl.json` (sha256 `9a679b400ba820f62d1f9a631cb04f183a69fd9a55f072a361791fa4cbe97a5d`):
a second `c1-duprow` control entry (identical id, append-op write) inserted after the
original py-op entry. Run:
`control=c1-duprow ... observed=TARGET_MISSED ok=1` then
`control=c1-duprow ... expected=TARGET_MISSED observed=TARGET_MET ok=0` →
`controls=20 correct=19/20 verdict=TARGET_MISSED`, exit 1 (receipt `mut-dupctl.txt`).
**KILLED** — the duplicated row via another op goes red.

## Mutation B2 — duplicate row via a *different op* (`file`), at file end
`/tmp/mutc1/mut-file-end.json` (sha256 `2ea23531b8acac55f070e619a9d9f94960ff4f947abb2e2f3b664bac077638a3`):
`c1-duprow.writes` = `[{"op":"file","path":"corpus/SOURCES.md","src":"fixtures/SOURCES-dup-end.txt"}]`
(fixture = lane SOURCES.md + dup row appended at EOF, sha256 `b0818ff99ddb536fb93a08f176f3abf3ef06d93c9bda6bfd48126db410428cb4`).
Run: `control=c1-duprow ... observed=TARGET_MET ok=0` →
`controls=19 correct=18/19 verdict=TARGET_MISSED`, exit 1 (receipt `mut-file-end.txt`).
**KILLED** — an alternative op that appends outside `## Registry` also fails the control.

## Mutation B3 — control: same `file` op, dup row placed *inside* `## Registry`
`/tmp/mutc1/mut-file-inside.json` (sha256 `112cfaad13ca1ffe6b086598372c80928c2c8bdf9f7804327a3a791567eb6505`):
fixture `fixtures/SOURCES-dup-inside.txt` (sha256 `5faf45415f69c08514ac2346d1590fe52400fe65db77b7ce75afa19827916978`) =
lane SOURCES.md with the dup row inserted right after the S217 row, inside the table.
Run: `control=c1-duprow ... observed=TARGET_MISSED ok=1` →
`controls=19 correct=19/19 verdict=TARGET_MET`, exit 0 (receipt `mut-file-inside.txt`).
**Survives as expected** — proves the bite is about row *placement* (inside registry),
not about which op inserts it.

## Restoration / purity evidence
- All mutants were created only in `/tmp/mutc1/` (manifest copies + fixtures); the lane
  manifest was never touched. Lane manifest sha256 before and after the probe:
  `96965518dc8ad98b52b28b406d66841758c80fd75610f9b94e0239b8adf838c8` (unchanged).
- `git status --porcelain` at end shows no tracked-file modifications (only the
  orchestrator/peer untracked wave files and this seat's report/receipts).

## Verdict
- Baseline: 19/19 MET exit 0 (detector healthy).
- A (append form): 18/19 MISSED exit 1 — killed.
- B1 (duplicate control row via append op): 19/20 MISSED exit 1 — killed.
- B2 (file op, dup at end): 18/19 MISSED exit 1 — killed.
- B3 (file op, dup inside registry): 19/19 MET exit 0 — control bites; placement is the
  load-bearing property, not the op.

The re-frozen manifest's duprow control is the evidence the C1 19/19 is not the old
18/19: any regression toward the append-at-file-end shape turns the run red.

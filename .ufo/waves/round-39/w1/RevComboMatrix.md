# RevComboMatrix — reproduce the f551b70 four-combo discrimination matrix

Seat: `RevComboMatrix` (leaf; no subagents, no background jobs). Round 39, wave 1, hyaku run 7.
Date: 2026-10-25. Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` (READ-ONLY except this
seat dir). No tools installed (none needed: repo's own `python3` + `git` only). No socket /
compositor / config-tree / fleet-repo / sibling-lane access.

## Scope

Reproduce the f551b70 matrix (round-38 freeze-pair resolution) in sandboxes: frozen counter ×
frozen manifest, frozen counter × landed manifest, landed counter × frozen manifest, landed
counter × landed manifest — each at the right revisions, recording correct/total per combo.
This validates the C1 re-registration story (registration.md C1: old frozen pair 18/19,
red-before receipt exists; re-frozen manifest targets 19/19 at the freeze commit).

## Inputs (pinned)

| component | source | sha256 |
|---|---|---|
| frozen c1 | `git show 58e55ec9…:quality/counters/c1-r38-event-ground.py` | `41eb241997018eb7024b7fccf7beb72f0c4602c423373a89ce78376c50d252f7` |
| frozen c2 | `git show 58e55ec9…:quality/counters/c2-r38-eventq.py` | `194a45c68f9e5756752daa8449dda1a7ae190ea016153b8e2e2a09c29f236921` |
| landed c1 | lane worktree `quality/counters/c1-r38-event-ground.py` (= post-`859d0cf9` blob; same hash at `859d0cf9`, `b6c1d31`, `08be4eb`, master) | `6872e18d3003b5fcbf94adac4b259a4a3651d313e848dda8999572851fe71866` |
| landed c2 | lane worktree `quality/counters/c2-r38-eventq.py` (byte-identical to freeze) | `194a45c68f9e5756752daa8449dda1a7ae190ea016153b8e2e2a09c29f236921` |
| frozen manifest | `.ufo/waves/round-39/receipts/manifest-frozen-r38.json` — byte-identical to `git show 58e55ec9…:.ufo/waves/round-38/controls/manifest.json` | `14c49d9fec35dc9bc307fbdd5c732e2ce80fabeaadfe3327b9121f50b9553edb` |
| landed manifest | `.ufo/waves/round-39/c1/manifest.json` — byte-identical to `git show b6c1d31…:.ufo/waves/round-38/controls/manifest.json` | `96965518dc8ad98b52b28b406d66841758c80fd75610f9b94e0239b8adf838c8` |

Revisions used per combo: freeze rev `58e55ec9e905c85fb5a794f9a51dc06cc16166ba` and data rev
`efb0ec234b6120a2d5051682f2d079b23118472b` (the two revs the round-38 replays pinned: RevCommitChain
A/B at the data rev, C/D at the freeze rev). Every combo run at both revs to show rev-invariance.

## Commands (per combo)

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/check-r38-discrimination.py \
  --c1 <counter-c1> --c2 <counter-c2> --manifest <manifest> \
  --rev <rev> --sandbox-root /tmp/mado39-RevComboMatrix/sandboxes --out <receipt>
```

Counters/manifests passed as files: frozen blobs extracted to `/tmp/mado39-RevComboMatrix/blobs/`
with `git show`; landed blobs are the lane worktree files. The gate's own sandbox clones
(`git clone --shared` + sparse checkout + control writes + sandbox commit) never touch the lane.

## Matrix (observed)

| combo | counter | manifest | --rev | correct/total | verdict | rc | receipt |
|---|---|---|---|---|---|---|---|
| 1 | frozen `58e55ec` | frozen `58e55ec` | freeze `58e55ec` | **18/19** | TARGET_MISSED | 1 | `combo1-frozen-frozen-freeze-rev.txt` |
| 1 | frozen `58e55ec` | frozen `58e55ec` | data `efb0ec2` | **18/19** | TARGET_MISSED | 1 | `combo1-frozen-frozen-data-rev.txt` |
| 2 | frozen `58e55ec` | landed `b6c1d31` | freeze `58e55ec` | **19/19** | TARGET_MET | 0 | `combo2-frozen-counter-landed-manif-freeze-rev.txt` |
| 2 | frozen `58e55ec` | landed `b6c1d31` | data `efb0ec2` | **19/19** | TARGET_MET | 0 | `combo2-frozen-counter-landed-manif-data-rev.txt` |
| 3 | landed `859d0cf` | frozen `58e55ec` | freeze `58e55ec` | **18/19** | TARGET_MISSED | 1 | `combo3-landed-counter-frozen-manif-freeze-rev.txt` |
| 3 | landed `859d0cf` | frozen `58e55ec` | data `efb0ec2` | **18/19** | TARGET_MISSED | 1 | `combo3-landed-counter-frozen-manif-data-rev.txt` |
| 4 | landed `859d0cf` | landed `b6c1d31` | freeze `58e55ec` | **19/19** | TARGET_MET | 0 | `combo4-landed-counter-landed-manif-freeze-rev.txt` |
| 4 | landed `859d0cf` | landed `b6c1d31` | data `efb0ec2` | **19/19** | TARGET_MET | 0 | `combo4-landed-counter-landed-manif-data-rev.txt` |

Receipt dir: `.ufo/waves/round-39/w1/RevComboMatrix/` (8 files). Receipt hashes:
`7fe05ad9986656bb7580a0784fc5961a2128661321017c7bda70f0f986f62154` for both combo-1 and both
combo-3 receipts (identical content); `8fe55d81a816e54469e5dd6474596b8ea19feaebf7ed5d5e6d153c01933d2e74`
for both combo-2 and both combo-4 receipts.

## Findings

1. **Matrix reproduces exactly.** All four combos score precisely the f551b70-recorded numbers
   (ScoutConsiderThese finding 1 table, landed in `f551b70`): frozen×frozen 18/19, frozen×landed
   19/19, landed×frozen 18/19, landed×landed 19/19. Sole failing control in every 18/19 run is
   `c1-duprow` (`expected=TARGET_MISSED observed=TARGET_MET ok=0` — the crib passes); every 19/19
   run observes `c1-duprow … observed=TARGET_MISSED ok=1`.
2. **Rev-invariance holds.** Identical results at the freeze rev and the data rev
   (rev-identical receipt hashes per combo). The distinguishing variable is the manifest version,
   not the rev — consistent with RevM37Routing §8 and RevCommitChain.
3. **C1 re-registration story confirmed.** The frozen pair is 18/19 (red-before receipt
   `c1-redbefore.txt` reproduced by combo 1), while the re-frozen manifest (byte copy of the
   repaired round-38 landed manifest at base, `.ufo/waves/round-39/c1/manifest.json`) scores
   19/19 at the freeze rev (combo 4) — matching the registration C1 Target. The landscape patch
   is the load-bearing change (combo 2 also 19/19 with frozen counters); the counter patch
   `859d0cf` was not load-bearing (combo 3 still 18/19).

## Safety / record

- Lane writes: only this report + the 8 receipts under `.ufo/waves/round-39/w1/RevComboMatrix/`.
  No tracked file edited; no git/jj mutation in the lane (read-only `git show`/`rev-parse` only).
- Scratch: `/tmp/mado39-RevComboMatrix/` (runner script `run_matrix.sh`, blobs, per-run logs,
  receipts). Sandboxes under `/tmp/mado39-RevComboMatrix/sandboxes/` (gate-created).
- Tool installs: none.

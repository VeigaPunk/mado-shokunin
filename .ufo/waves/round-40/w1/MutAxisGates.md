# MutAxisGates — round-40 w1: mutation probes of `quality/check-index.py` and `quality/check-axis-scores.py`

**Verdict: 3/3 mutants KILLED, 0 survived, 0 inconclusive.** Each gate failed on its assigned
mutation with the exact defect named, and returned to exit 0 on restored bytes (restored tree
sha identical to the pristine base tree in all three clones). No gate passed a mutant, so there
is no coverage finding against the harm watch.

## Sandbox (per git-fixture rule; all commits in /tmp only)

- Base: lane HEAD `e2b51d3b3f79768282914d57c1fa32cc85dcb06a`, exported with read-only
  `git -C <lane> archive HEAD | tar -x -C $D` into `/tmp/mutag-base`, then
  `git -C "$D" init -q`; `git -C "$D" rev-parse --show-toplevel` verified equal to `$D`
  before the first commit; commits made only inside /tmp clones with throwaway identity
  (`mut <mut@mut>`). No mutating git ran in the lane or the fleet; no tracked lane file was
  edited.
- Archive fidelity: 11938 tracked paths, 11905 regular files materialized; the 33 absent paths
  are tracked **symlink fixtures** under `.ufo/waves/round-{17,18,19,22,33,34}`
  (tripwire/controls; `git archive` emits them as symlinks, my `find -type f` count skipped
  them). Neither gate reads them. Behavior fidelity is attested by the pristine runs below
  matching the lane's own runs byte-for-byte on stdout.
- Both gates read **committed bytes** (`git show <rev>:path`), so each mutation was committed in
  its own clone before the detector ran; a working-tree-only mutation is invisible to the
  `--rev` harm-watch mode by construction.

## Pristine baseline (detector must pass; a baseline failure would be inconclusive)

In the lane (`--rev HEAD`) and again in `/tmp/mutag-base` at its own HEAD — identical:

```
MADO_INDEX: rev=HEAD indexed=56/56 missing=0 dangling=0 duplicates=0 coverage=10.0000/10   exit=0
MADO_AXIS_ROW: axis=navigation  published=56/56 derived=56/56 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=51/51 derived=51/51 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=0                                                          exit=0
```

Pristine hashes: `corpus/README.md` `63a57d5b3a21d6c209c48c4d416b594adaba14cf537f94fc6a02698e0878995c`;
`SCORECARD.md` `b2d66e2f5d2c64554577d327d3039eb8d268e26857a377777c367b80050ebefc`;
base tree `8a25e4f94d3667c2080e18391ea6046f0f9a31d8`.

## M1 — fake knowledge note without an index row → KILLED

- Mutation: new file `/tmp/mutag-m1/corpus/knowledge/mut-fake-entry-r40.md` (323 B,
  sha256 `7c217c5c04ed9f1d116a673cbb553dad690716cb0428cd9d4f24d963e2a66870`), no row added to
  `corpus/README.md` (unchanged, `63a57d5b…`); committed.
- Command: `python3 -I /tmp/mutag-m1/quality/check-index.py --rev HEAD --repo /tmp/mutag-m1`
- Expected: exit 1, `missing=1`, note named.
- Output: `MADO_INDEX: rev=HEAD indexed=56/57 missing=1 dangling=0 duplicates=0 coverage=9.8246/10`
  plus `missing: knowledge/mut-fake-entry-r40.md` — **exit=1**. Verdict: **killed**.
- Restored: note deleted; commit; rerun → `indexed=56/56 missing=0 … coverage=10.0000/10`,
  **exit=0**; `HEAD^{tree}` = `8a25e4f9…` = base tree (TREE-IDENTICAL yes).

## M2 — deleted `corpus/README.md` index row → KILLED

- Mutation: removed the row line
  `| \`knowledge/config-option-table-r39.md\` (MADO-R39-1, round 39; …) | … | S218, S219, S220, S162, S173 |`
  (README.md sha256 after mutation
  `a9cd00e05b6cb6fb6377f57891eb67fad3165a1adb448ff336da8435dacd0281`; post-mutation grep for
  the row prefix returns 0); committed.
- Command: `python3 -I /tmp/mutag-m2/quality/check-index.py --rev HEAD --repo /tmp/mutag-m2`
- Expected: exit 1, `missing=1` for the note whose row was deleted.
- Output: `MADO_INDEX: rev=HEAD indexed=55/56 missing=1 dangling=0 duplicates=0 coverage=9.8214/10`
  plus `missing: knowledge/config-option-table-r39.md` — **exit=1**. Verdict: **killed**.
- Restored: byte-exact `cp` of the saved original back (sha256 again
  `63a57d5b3a21d6c209c48c4d416b594adaba14cf537f94fc6a02698e0878995c`); rerun →
  `indexed=56/56 … coverage=10.0000/10`, **exit=0**; tree = base tree (TREE-IDENTICAL yes).

## M3 — perturbed published axis score → KILLED

- Mutation: in `SCORECARD.md` line 2466 (the last "Axis table re-derived at …" publication,
  which the gate parses as live), `navigation 56/56` → `navigation 55/56` (SCORECARD.md sha256
  after mutation `f83c5d9f80002a3eeab7fb9832f87f2306b464f9ca121ac0291b6edb887779f8`); committed.
- Command: `python3 -I /tmp/mutag-m3/quality/check-axis-scores.py --repo /tmp/mutag-m3`
- Expected: exit 1, navigation row verdict STALE, `mismatched=1`.
- Output:
  `MADO_AXIS_ROW: axis=navigation published=55/56 derived=56/56 verdict=STALE` (other two rows
  MATCH), `MADO_AXIS: checked=3 mismatched=1 rev=8ef30b97a2c974da802a744df163127558fe0f2b` —
  **exit=1**. Verdict: **killed**.
- Restored: byte-exact `cp` back (sha256 again
  `b2d66e2f5d2c64554577d327d3039eb8d268e26857a377777c367b80050ebefc`); rerun →
  `mismatched=0 rev=a8b6c91b85791c8d0caccc21c9c967423c5766a0`, **exit=0**; tree = base tree
  (TREE-IDENTICAL yes).

## Notes (observations, not defects)

- Both gates refuse to guess state: `check-index.py` requires an explicit `--rev`/`--root`
  (bare invocation = SETUP_ERROR exit 2) and `check-axis-scores.py` counts a missing
  publication/instrument as a mismatch, not a pass — consistent with what the mutations
  exercised.
- The 55/56-vs-56/56 M3 perturbation was caught by the derived instrument, i.e. the gate's
  strength is that its derived side is computed, not stored.

## Housekeeping

- Cleanup: `/tmp/mutag-base`, `/tmp/mutag-m1..m3`, `/tmp/mutag-orig-README.md`,
  `/tmp/mutag-orig-SCORECARD.md` deleted after the probes.
- Writes: /tmp sandbox only, plus this report. No lane tracked file touched; no pacman, no
  compositor verb, no host-service mutation.
- Tools installed: none (probe used preexisting python3/git/tar/find).

# RevC1Freeze — C1 re-registration freeze discipline verification (round-39, w1)

Date: 2026-10-25. Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Independent re-run of the C1 counting command at the freeze commit and at tip;
manifest/counter immutability; registration predicate consistency; attack runs.
No lane files were written except this report.

## 1. Runs

Freeze commit = tip: `git rev-parse HEAD` → `457d1b125932c1e0d797061a2156b917bcd7edaa`
(`457d1b1 round-39: freeze registration + base receipts + inherited r38 seat reports`);
`git rev-list --count 457d1b1..HEAD` → 0. So the "freeze commit" run and the "tip"
run target the same commit today; both were executed with the mandated command line.

| Run | `--rev` | Result | Exit |
|---|---|---|---|
| freeze commit | `457d1b125932c1e0d797061a2156b917bcd7edaa` | `MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET` | 0 |
| tip/master | `master` | same (controls=19 correct=19/19 verdict=TARGET_MET) | 0 |
| same-rev rerun (determinism) | `457d1b125932c1e0d797061a2156b917bcd7edaa` | same, output byte-identical summary | 0 |
| rev-variant @ BASE | `08be4eb7fd13358ed29b096e8924005d46ac409c` | same (controls=19 correct=19/19 verdict=TARGET_MET) | 0 |
| rev-variant @ bogus | `deadbeefdeadbeefdeadbeefdeadbeefdeadbeef` | 17 controls `observed=ERROR note=checkout-failed`; `correct=2/19 verdict=TARGET_MISSED` | 1 |
| red-before reproduction | `08be4eb…` + frozen r38 manifest | `c1-duprow … observed=TARGET_MET ok=0`; `correct=18/19 verdict=TARGET_MISSED` | 1 |

All control lines listed per run; every one of the 19 controls printed `ok=1` on the
green runs.

## 2. Manifest immutability

- `git log --oneline HEAD -- .ufo/waves/round-39/c1/manifest.json` → single entry: the
  freeze commit `457d1b1`; the path does not exist at BASE (rev-parse of the base tree
  fails for the round-39 receipt/manifest paths).
- Working-tree file is unmodified: `git hash-object .ufo/waves/round-39/c1/manifest.json`
  → `ec347320fff6e3f5559c39ee8439824d00c7a10b`, identical to the blob at the freeze
  commit; `git status --porcelain` does not list it. No commits exist after 457d1b1.
- The manifest blob `ec347320…` equals exactly the round-38 *controls* manifest blob at
  BASE and at freeze (`.ufo/waves/round-38/controls/manifest.json`), i.e. it is a byte
  copy of the landed/repaired round-38 manifest as the registration declares.
- Delta vs the frozen round-38 pair (`receipts/manifest-frozen-r38.json`, blob
  `93f168c6…`): only control `c1-duprow` differs — its `writes` op changed from `append`
  (file end, outside the counter's `## Registry` parser) to `py` inserting the duplicate
  row inside the Registry table. The other 18 controls are byte-identical. This is
  exactly the declared repair; it is the sole control that flips 18/19 → 19/19.

## 3. Counters unchanged since BASE

`git diff 08be4eb..457d1b1 -- quality/counters/c1-r38-event-ground.py quality/counters/c2-r38-eventq.py quality/check-r38-discrimination.py` → empty (exit 0). Blob OIDs at BASE and freeze are pairwise equal:
- c1-r38-event-ground.py: `46f545a21566fbc9af542674f3aead2d81b56372` (both)
- c2-r38-eventq.py: `2f385c9ebec4bb1ad158350695fbd4293b815b4d` (both)
- check-r38-discrimination.py: `9471f07031e4d842a6723e72c50fcc716b524f55` (both)

None appear in `git status --porcelain` (dirty paths are only untracked C2/C3 artifacts,
w1 dispatch files, and this seat dir).

## 4. Registration predicate at the freeze commit

`git show 457d1b1:.ufo/waves/round-39/registration.md` diffed against the working tree →
empty (exit 0). The C1 section at the freeze commit states the same predicate command
(`python3 -I quality/check-r38-discrimination.py --c1 … --c2 … --manifest .ufo/waves/round-39/c1/manifest.json --rev <rev>`),
the same before (18/19 MISSED, `receipts/c1-redbefore.txt`), and the same target
(`controls=19 correct=19/19 verdict=TARGET_MET`, exit 0, at the freeze commit and the
data tip).

## 5. Attack findings

- Same-rev rerun: deterministic (identical output, exit 0).
- Rev-variant @ BASE: the green result is **rev-insensitive across resolvable revs** —
  BASE (08be4eb) also yields 19/19. Root cause from source (`quality/check-r38-discrimination.py`):
  the two `-live` accept controls carry no control-level `rev` and run the counter
  against the sandbox checkout of the `--rev` argument; the accept-ground (round-37
  entries) already exists at BASE, so the acceptance does not depend on round-39-only
  commits. The two `-donothing` reject controls pin `rev=b4e47e980bfb0cbc8a4e788f59a41db858751fd8`
  (round-36 verifier spot-check), so they are immune to `--rev`. This means the 19/19
  freeze-commit pass does not by itself prove freeze-specific data; it proves the repaired
  manifest discriminates (red-before → 18/19, exit 1, reproduced bit-for-bit against the
  committed receipt). The bogus-rev run (17 ERROR + 2 pinned-pass, MISSED, exit 1) proves
  `--rev` is genuinely honored and the gate never emits TARGET_MET vacuously.
- Red-before reproduced: with the frozen round-38 manifest at BASE, `c1-duprow` is
  `observed=TARGET_MET ok=0`, summary 18/19 MISSED exit 1 — identical to the committed
  receipt `.ufo/waves/round-39/receipts/c1-redbefore.txt` (line 5 and summary).

## 6. Notes / residual risk

- Registration labels the re-frozen manifest `MANIFEST-r39-v1`; the file's embedded id is
  `MANIFEST-r38-v1` (inherited, as expected from a byte copy). Cosmetic naming drift; the
  count run is unaffected and no counter/control reads the id. Claimed fix is not
  auditable beyond the round-38 job; the freeze discipline itself is intact.
- "Data tip" currently equals the freeze commit (no commits after 457d1b1); the C2/C3
  deliverables exist only as untracked worktree files, so the "at the data tip" clause is
  satisfied by the same commit today.
- Declared residual (fabricated self-consistent artifacts may pass) still holds; the new
  `py`-op write primitive executes inside the confined env (no subprocess/os/sys) — no
  escape observed.

## Verdict

C1 freeze discipline verified: manifest appeared in the freeze commit and is unmodified;
counters unchanged since BASE; registration at freeze matches; count runs print
controls=19 correct=19/19 verdict=TARGET_MET exit 0 at freeze and tip; same-rev rerun
deterministic; rev-variant attacks behave honestly (base green, bogus red) and red-before
reproduces. No defect found in scope.

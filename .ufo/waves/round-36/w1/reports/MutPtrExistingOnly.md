# MutPtrExistingOnly — mutation-tester report, mado round 36 wave 1

Assignment (`.ufo/waves/round-36/w1/prompts/MutPtrExistingOnly.md`): **Mutate the C2 gate in /tmp so `dangling` counts only pointers that exist (a vacuous counter). Score it against the round-35 record (where two pointers are absent) and show it reports 0 dangling while naming one absent pointer by hand.**

## Mutant

Defect: the `dangling` counter filters on `p in files` *before* testing `not resolves(p, files)` — i.e. it counts only pointers that literally exist as `git ls-tree` entries. That conjunction is identically false for every pointer class (a plain path that resolves is in `files`, so `not resolves` is false; directory pointers `x/` and globs are never literal `files` entries), so the counter is vacuously 0.

Copy: `/tmp/mutptr-existingonly/mutant.py` (from `quality/check-evidence-pointers.py` at `HEAD`, SHA `74ce7a05…`). Mutation, lines 149–150:

```python
    dangling35 = [p for p in ptr35 if p in files and not resolves(p, files)]
    dangling36 = [p for p in ptr36 if p in files and not resolves(p, files)]
```

## Detector and command

Detector: the gate itself, same bounded command the registration freezes, run at the freeze commit `dbf8b579aeac0f023aaf595770f1cb0049e4baa2` and at `master`:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I <copy> --rev <rev> --repo .
```

## Evidence (exact outputs)

| Run | Output (key fields) | Exit |
|---|---|---|
| PRISTINE @ `dbf8b57` (freeze) | `pointers_r35=8 dangling_r35=2 dangling_r35_closed=0 … setup=missing-r36-sections verdict=TARGET_MISSED`; `dangling_r35: .ufo/waves/round-35/scratch/SimplifyCounter/`; `dangling_r35: .ufo/waves/round-35/scratch/MutC1Drop/mutants/` | 1 |
| MUTANT @ `dbf8b57` (freeze) | `pointers_r35=8 dangling_r35=0 dangling_r35_closed=1 … verdict=TARGET_MISSED` (setup still missing) | 1 |
| PRISTINE @ `master` | `pointers_r35=8 dangling_r35=2 dangling_r35_closed=1 pointers_r36=34 dangling_r36=3 … verdict=TARGET_MISSED`; `dangling_r35: …/SimplifyCounter/`; `dangling_r35: …/MutC1Drop/mutants/`; `dangling_r36: …/SimplifyCounter/`; `dangling_r36: …/MutC1Drop/mutants/`; `dangling_r36: quality/receipts/axis-a3094c99ab85bec35534de2447552c47dd2b647f.txt` | 1 |
| MUTANT @ `master` | `pointers_r35=8 dangling_r35=0 dangling_r35_closed=1 pointers_r36=34 dangling_r36=0 … tip_axis_transcript=1 setup=ok verdict=TARGET_MET` | 0 |
| RESTORED @ `master` (pristine bytes) | identical to PRISTINE @ master (`dangling_r35=2`, `dangling_r36=3`, `TARGET_MISSED`) | 1 |

Hand check (naming one absent pointer): `git ls-tree -r --name-only master .ufo/waves/round-35/scratch/SimplifyCounter/ | wc -l` → `0`; same at `dbf8b57` → `0`; `git ls-tree -r --name-only master .ufo/waves/round-35/scratch/MutC1Drop/mutants/ | wc -l` → `0`; the round-35 record still cites it: `git show master:LOG.md | grep -c 'scratch/SimplifyCounter/'` → `2`. So `.ufo/waves/round-35/scratch/SimplifyCounter/` is absent at both checked revisions while the record cites it — yet the mutant reports `dangling_r35=0`.

## Verdicts

- **Mutation applied exactly as assigned: PASS** — only the two `dangling` comprehensions differ (`diff pristine.py mutant.py` shows exactly lines 149–150); SHA `74ce7a05…` (pristine/restored) vs `a40d3cdc…` (mutant).
- **Reports 0 dangling against the round-35 record: PASS** — mutant prints `dangling_r35=0` at both `dbf8b57` and `master`, where pristine prints `dangling_r35=2`.
- **Names an absent pointer by hand: PASS** — `scratch/SimplifyCounter/` absent at both revs (`ls-tree` → 0 lines) while `LOG.md` cites it twice, `grep -c` → 2.
- **Kill verdict: **SURVIVED — detector (TARGET_MET) at `master`** — the mutant flips the frozen verdict `TARGET_MISSED` → `TARGET_MET`, exit 0, while two round-35 pointers (plus round-36 citations) are still absent and the round-35 record is unrepaired. At the freeze commit the verdict does not flip because `setup=missing-r36-sections` (exit 1) is a separate check the mutation does not touch.
- **Restoration: PASS** — `cp pristine.py restored.py`; restored SHA `74ce7a05…` == pristine; restored run reprints `dangling_r35=2` / `TARGET_MISSED`. Lane production bytes were never touched: `quality/check-evidence-pointers.py` at `HEAD` is SHA `74ce7a05…` (matching the pristine copy) and I wrote only to `/tmp/mutptr-existingonly/` and this report.

## Finding (coverage)

A `dangling` counter that counts only existing pointers is a vacuous counter: it undercounts `dangling_r35` (and `dangling_r36`) to 0, and because `dangling35_closed = record_intact and (closed == len(dangling35))` reduces to `closed == 0` when the list is empty, the closure observable passes vacuously too. The gate's other observables (setup, dirty, scratch disposition, axis transcript) did not catch it — the mutant produced `TARGET_MET` at `master` with a live record defect (D5's two paths uncorrected). This is precisely the fail-open shape round-35's D4 warned about: the dangling count must be computed from the *cited* pointer set, never filtered to existing paths first.

Tooling: none installed (python3 and git already present; no pacman/npx/uv action taken).

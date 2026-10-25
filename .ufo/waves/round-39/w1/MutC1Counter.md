# MutC1Counter — mutation test report (round-39 w1)

**Role:** UFO-FSD mutation tester. **Date:** 2026-10-25. **Lane:** mado-shokunin.
**Target:** `quality/counters/c1-r38-event-ground.py` (c1 counter, PRED-C1-r38-v3).
**Invariant challenged:** clause j unique-row enforcement — "every cited id has exactly one
`## Registry` row" must bite on the re-frozen c1 manifest control `c1-duprow`.

## Method

Copied the pristine counter to a /tmp sandbox (`/tmp/mut-c1/`), weakened the unique-row
enforcement, and ran the same bounded detector — `quality/check-r38-discrimination.py`
against the re-frozen manifest `.ufo/waves/round-39/c1/manifest.json` at the freeze rev
`457d1b1` (round-39 freeze commit) — on pristine, mutated, and restored bytes. The lane
counter file was never written; all mutants live in /tmp. Receipts (per-control lines) at
`/tmp/mado-receipts/{baseline,mutant-run,mutant-jonly,restored}.txt`.

## Mutant (killed)

Mutation: weakened the uniqueness check `len(rows.get(i, [])) == 1` → `len(rows.get(i, [])) >= 1`
at BOTH enforcement sites (2 lines, smallest behavior-bearing change):

1. Clause c, line 203: `c["c"]` prefix `len(rows.get(i, [])) == 1 and (` → `>= 1 and (`
2. Clause j, line 226: `j_ok = j_ok and len(rows.get(i, [])) == 1` → `>= 1`

Why both sites: unique-row enforcement is duplicated — clause c (line 203) and clause j
(line 226) each gate on `len(rows.get(i, [])) == 1`. A j-only weakening leaves clause c as a
backstop, so the duprow control still observes MISSED (verified below, survivor variant).

## Detector commands

```
python3 -I quality/check-r38-discrimination.py \
  --c1 <counter> --c2 quality/counters/c2-r38-eventq.py \
  --manifest .ufo/waves/round-39/c1/manifest.json \
  --rev 457d1b1 --sandbox-root /tmp/mado-sb --out /tmp/mado-receipts/<name>.txt
```

## Results (same detector, byte-identical manifest/rev)

| Run | counter bytes | c1-duprow observed | summary | exit |
|---|---|---|---|---|
| pristine (baseline) | `6872e18d…` (lane original) | `TARGET_MISSED` (expected, ok=1) | `controls=19 correct=19/19 verdict=TARGET_MET` | 0 |
| mutant (both sites weakened) | `770eac731…` | **`TARGET_MET` (flipped, ok=0)** | `controls=19 correct=18/19 verdict=TARGET_MISSED` | **1** |
| variant j-only | `71f9f87a…` | `TARGET_MISSED` (ok=1; clause c backstop still bites) | `controls=19 correct=19/19 verdict=TARGET_MET` | 0 |
| restored (lane bytes untouched) | `6872e18d…` (hash identical) | `TARGET_MISSED` (ok=1) | `controls=19 correct=19/19 verdict=TARGET_MET` | 0 |

Kill verdict: **KILLED** — the mutant goes red with exactly the required control
(c1-duprow) flipping MISSED → MET; nothing else regressed (all other 18 controls still ok).

## Hash evidence

```
sha256sum quality/counters/c1-r38-event-ground.py
6872e18d3003b5fcbf94adac4b259a4a3651d313e848dda8999572851fe71866   (before AND after; lane file never modified)
sha256sum /tmp/mut-c1/c1-r38-event-ground-mutant.py
770eac731154f2a365a9f594edfafe1649bcc34b1d45dcb2dc509eed833cc9a0
sha256sum /tmp/mut-c1/c1-r38-event-ground-mutant-jonly.py
71f9f87a52bec440fda682a0b9601245acc25e42ec8a08d19fc2a9d2217f90b9
```

## Restoration evidence

- Lane file hash unchanged after all runs (`6872e18d…` before and after).
- `git -C mado-shokunin status --short quality/counters/` → only pre-existing untracked
  `c3-r39-options.py` (C2 deliverable); `git diff --stat` empty — no tracked lane bytes changed.
- Restored-bytes rerun of the pristine counter reproduces green `19/19 verdict=TARGET_MET`, exit 0.

## Findings

- The unique-row enforcement (v3 F3 repair) is live and kills the weakened mutant exactly on
  the `c1-duprow` reject control. The re-frozen manifest's dup-row injection (inside
  `## Registry`, after the S217 row) is visible to the parser and both clauses.
- Coverage finding: uniqueness bites at TWO sites (clause c line 203 and clause j line 226);
  weakening only clause j (the clause the manifest control names) survives — clause c alone
  still rejects the duplicate row. The minimal killing mutant must weaken both.
- No installs performed (stdlib + existing git only). No lane/fleet repo writes beyond this
  report; all scratch in /tmp.

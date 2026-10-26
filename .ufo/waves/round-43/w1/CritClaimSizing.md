# CritClaimSizing — report (mado round 43, w1, before any data)

Scope: the round's claim sizing and re-registration (`registration.md` claims, prompt §6 item 9–10, AXES.md).
Detailed findings, commands, outputs and receipts: `.ufo/waves/round-43/w1/CritClaimSizing/findings.md`.
No tracked file edited; no mutating git; scratch under `/fast/scratch/hyaku/mado-r43/CritClaimSizing/` (removed at close).

## Two HIGH defects — both fixable before data; both are "the target is reached by skipping the claimed work"

1. **C1's target is met by `cp` of the frozen round-42 reference.** `copy .ufo/waves/round-42/c1/ctl-ref-tool.py.txt` (sha256
   `e3c2e471…`, 417 lines, unchanged) and the frozen counter prints `fixtures=37/37 tool=present verdict=TARGET_MET`, exit 0,
   clauses `a:1 b:1 b2:1 b3:1 g:1` (receipt `.ufo/waves/round-43/w1/CritClaimSizing/c1-copy-verbatim.txt`). The same artifact scored
   `met=1` as round 42's REF anchor, so the round cannot distinguish acquisition from promotion. Fix: either declare the after-state
   as the installation of the reference's behaviour (the honest form), or add `sha256(tool at REV) != e3c2e471…` — which kills the
   literal copy only; the declared residual still admits a model-bearing near-copy.
2. **C2's target is met by a 17-line entry that cites no compositor source.** Four NEW ids, every receipt a real PINS file
   (`Hyprland-Target.cpp` + the three own-work), no held id, no synthetic receipt → `admitted=1/1 verdict=TARGET_MET`, clauses
   all `:1` (`…/c2-4new-receipt.txt`, entry at `…/c2-4new-entry.md`). Clause b needs ≥4 ids, clause c ≥3 new, clause h exactly the
   three own-work pins, so the forced set is "3 own-work + any 1 of 7 upstream"; five of the claim's eight enumerated links
   (`FullMatch`, the size/float chain, the floating algorithm, the window-side store, the animated GOAL variable) are optional.
   Fix (a w1 hole before data may re-register as v2, `registration.md:78-79`): require all ten PINS ids (or per-pin anchor tokens),
   then re-derive the 74 controls.

## MEDIUM (same root as 2)

`registration.md:30-31` says the entry covers "what determines the size … **end to end** (eight links)"; the counting command
prints only `admitted=N/1`. Universal clause not enumerated — enumerated by the fix above.

## LOW (prose; no counter change)

- `:13-14` "Every published axis ties at its maximum at base" — the named receipt enumerates three axes
  (`axis-base.txt`; `quality/check-axis-scores.py:32`), not coverage, the axis C2 claims. Conclusion survives on
  `SCORECARD.md:1012` and `:1089`; name them.
- `:42-43` "C2 never runs C1's tool and C1 reads no C2 file" — true (two greps, `…/checks.txt`) but unnamed.
- `:5-6` 37 w1 seats / 69 planned vs the committed `w1-spec.json` (38 items, commit `5add5b4`, after the freeze) — report 38/70;
  `w1.ready`/`w1.ready.dispatched` untracked again (round-40 defect (a) recurring).

## Cleared

- **Re-registration is not a rule changed after data.** Round 42 never scored the predicates: 36 w1 members with 0 `agentId`, no
  `w2`, no reports, no data commit (`809dc2c..a35cfdf` is spec + honest-stop + closure). Frozen bytes equal the round-43 base bytes
  (`git diff --stat 809dc2c a35cfdf -- …c1-r42… …c2-r42…` empty). Informational: the orchestrator snapshot `8af0263` rewrote the C1
  counter (+6/−17) and a later commit restored it; nothing scored in that window.
- **PRED-C2-r43 is constants-only.** 42 changed lines, all classified (`…/c2-diff-classification.txt`): 6 docstring note, 18
  docstring label/path/date/name, 12 module constants, 4 PINS, 4 receipt-name references. No clause text, regex or threshold moved.
- **Control tallies and pins consistent.** `ctl-c1.txt`: `controls=46`, 48 `ok` lines (M38 D3 K5), `0 of 47`, exit 0.
  `ctl-c2.txt`: 74 controls, 74 `ok=1`, exit 0. All ten C2 PINS match `fetch/` bytes.

## Axis impact (if landed as frozen)

operability would be credited to a file copy (F1) and coverage to an entry that need not cover the chain the claim names (F2/F3).
Neither is fatal to the underlying work — the reference is real code and the entry shape is real paperwork — but as declared, the
two targets do not measure the round's claimed move. Both are enumerable fixes available before any data commit.

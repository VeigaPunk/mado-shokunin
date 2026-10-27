# Falsify25 — C1 self-pointer/context bypass

## Deliverables

- `.ufo/waves/round-52/w1/Falsify25.md` — scoped attack result.

## Attack result

**Attacked item/predicate:** frozen C1's requirement that a new counter reject a no-work ledger with repeated generic self-pointers, including non-self resolvable evidence and instrument-specific functional context checks.

**Named control:** `.ufo/waves/round-52/controls/c1-do-nothing.md`. Its two rows are duplicates and both identify `quality/tool-ledger.md` as their own “commentary only” evidence pointer; the descriptions are generic (“nothing” / “generic accountability pointer to this ledger itself”), not instrument-specific functional context. This directly exercises the frozen control's intended self-pointer/context failure mode.

**Reproduced: no (inconclusive, not a killed mutant).** The required `quality/counters/c1-r52-ledger.py` was absent from the round-52 source tree at the observed base revision; the only available implementation is the explicitly superseded `quality/counters/c1-r51-ledger.py`. Its own source says that its pointer check only requires a repo file containing the instrument basename (`quality/counters/c1-r51-ledger.py:28-30`), and its acceptance criteria contain no non-self or context-specific check (`:10-14`). But it reads the ledger from a pinned git revision (`:16-24`, `:388-390`) and cannot evaluate the external frozen control as a candidate ledger. I did not substitute a homemade detector or report a hypothetical outcome as an executed result.

**Reproducible inspection:**

```sh
git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse HEAD
# 85d57a818c3707397e21c840b6498b105ba798aa
git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --short
# ?? .ufo/waves/round-52/
```

Read-only source inspection found the C1 control's two identical rows in the named path above, and the base receipt `.ufo/waves/round-52/receipts/c1-base.txt` reports the prior counter's production result `82/82 ... TARGET_MET`. That receipt is not a control run and does not establish the r52 predicate. The r52 detector absence prevents testing whether the required control is actually rejected; no production or host tools were run, no package queries or installs were performed, and no scratch artifacts were created.

## Residual risk / limitation

The C1 control has the exact self-pointer/generic-context shape that the frozen claim requires the new counter to reject, but no measured rejection/pass outcome is available at this base snapshot. This report makes no claim about a later r52 detector or its behavior.

## Report

`mado-shokunin/.ufo/waves/round-52/w1/Falsify25.md`

# Falsify01 — C1 self-pointer/context bypass

## Scope and result
Attacked C1's non-self pointer and instrument-specific context requirements, focusing on the frozen repeated-self-pointer control. Source-only analysis confirms the old counter's specific bypass; runtime reproduction was not performed (prohibited by round-52 safety boundary).

## Evidence
`quality/counters/c1-r51-ledger.py` `pointer_resolves()` (lines 196–208) checks whether the referenced token exists in the tracked file listing and whether the referenced bytes contain the row path basename. It never compares the pointer token against the ledger path or otherwise rejects self-reference. `describe()` (lines 229–236) rejects only empty/placeholder descriptions, not generic text. Consequently a ledger self-pointer can resolve by matching its own basename in its contents while generic nonempty description passes.

The frozen control `.ufo/waves/round-52/controls/c1-do-nothing.md` contains two repeated rows pointing to `quality/tool-ledger.md` itself, with generic wording (lines 1–4). The recorded base receipt `.ufo/waves/round-52/receipts/c1-base.txt` reports the prior checker as `population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 ... verdict=TARGET_MET` (lines 1–4). Receipt is existing recorded evidence, not this seat's execution.

## Reproduction
Source-only reproducible trace: read the cited control and receipt, then inspect `pointer_resolves()` and `describe()` in the cited counter. The acceptance branch is `base.encode() in cache[token]`; the self-pointer control uses the ledger as token, and descriptions are generic but nonempty. The same acceptance is reflected in the recorded base receipt.

**Actual result:** static logic permits self-pointer/generic description; historical receipt records old counter TARGET_MET. **Reproduced: no** — did not execute the producer because round-52 SKILL.md prohibits producer execution. No claim is made about the new round-52 counter, which is absent from the pinned base and was not tested.

## Limitations and safety
No package query, live probe, process/compositor access, input capture, screenshot, producer execution, host/config/service mutation, or installation. Source repo remains read-only. Scratch created at `/fast/scratch/hyaku/mado-r52/Falsify01/`; disk guard showed 600G available before use. No evidence files were placed in scratch, so nothing to clean there.

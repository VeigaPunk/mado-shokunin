# Falsify01 — C1 self-pointer/context bypass

## Deliverables
- `w1/Falsify01/Falsify01.md` — scoped source-only analysis and reproduction procedure.

## Finding
**Attacked item/predicate:** C1, specifically the requirement that a ledger row's evidence pointer be non-self, resolvable, and supported by instrument-specific functional context; the frozen no-work control is repeated generic self-pointers.

**Concrete failure mode confirmed in source:** the round-51 counter accepts a pointer whenever the referenced file contains the basename of the row's instrument. `pointer_resolves()` extracts candidate paths and returns true on `base.encode() in cache[token]` (`quality/counters/c1-r51-ledger.py`, lines 196–208). It does not reject `token == row_path`, nor require row-specific/non-self evidence. The pointer can therefore point to the ledger itself, when that ledger contains the tool basename; pointer resolvability is not evidence of non-self accountability. `describe()` also treats any nonempty, non-placeholder description as sufficient (`lines 229–236`), with no instrument-specific-context test. This is the exact structural weakness frozen C1 says the new counter must improve.

The supplied control has two identical generic rows, both naming `quality/tool-ledger.md` itself and saying “generic accountability pointer to this ledger itself” (`.ufo/waves/round-52/controls/c1-do-nothing.md`, lines 1–4). The base receipt reports the old checker measured 82/82 with `bad_pointer=0`, `empty_desc=0`, and `TARGET_MET` (`.ufo/waves/round-52/receipts/c1-base.txt`, lines 1–4). Those receipt values are corroborating recorded evidence, not a fresh run by this seat.

**Reproduction command/setup:** source-only trace: inspect `pointer_resolves()` and `describe()` in `quality/counters/c1-r51-ledger.py`; compare with the supplied control and `receipts/c1-base.txt`. Specifically, a row whose path basename occurs in its own ledger and whose pointer token is that ledger satisfies the `base.encode() in cache[token]` branch; a generic nonempty description avoids `empty_desc`. The tracked counter's CLI would normally be exercised against a pinned repository/revision, but it was not executed because round-52 `SKILL.md` explicitly prohibits producer execution.

**Actual result:** source predicate admits the self-pointer and generic description, and the committed base receipt records TARGET_MET for the old checker despite the control's corresponding shape. **Reproduced: no** (no runtime execution permitted); static failure mode confirmed.

## Limitations
- This seat did not test the newly drafted round-52 counter, as it was absent from the frozen base revision and producer execution is forbidden. Thus this is a confirmed attack on the named prior weakness/control shape, not a claim that the new counter fails.
- Source-only restrictions observed: no package queries, live probes, input capture, screenshots, producer execution, or host mutation. No tool installation.

## Report
`.ufo/waves/round-52/w1/Falsify01.md` (relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`)

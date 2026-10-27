# Round 51 merge/mado assimilation scan

## Theme scan
Scanned the staged knowledge target list in `MERGE-REPORT.md` against claims C1/C2 and `PROVINCE.md` desktop/compositor scope. Candidate matches:

- `corpus/knowledge/dispatcher-semantics-r25.md` — dispatcher semantics and execution are explicit in the title; relevant to C2 topic, but not equivalent to the specific Hyprland 0.56.2 keybind-string parsing/execution claim.
- `corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md` — dispatcher surface/request resolution is relevant to C2; a candidate for overlap, though not necessarily the dispatcher-string parser details.
- `corpus/knowledge/chinese-hyprland-window-rules-r16.md` — title concerns the desktop's window rules and focus dispatch, within broad desktop scope; localized documentation itself is explicitly outside province per `PROVINCE.md` lines 75–82.

No staged entry title directly addresses tracked tool-ledger/operability (C1). Remaining staged entries are not apparent C1/C2 topic matches from their target/title; many do touch Hyprland, Waybar, idle, focus, or other desktop subject matter and are within broad desktop/compositor scope, but the province's localization channel exclusion applies to localized documentation artifacts.

## ID collision guard
Applied the specified ID extraction pattern to lane `corpus/SOURCES.md` and staged `SOURCES.append.md`.

- Lane IDs (ordered): S001–S255 (255 IDs).
- Staged IDs (ordered): S203–S349 (147 IDs).
- Intersection: 53 IDs: S203–S255. **Collision count: 53.**

Note: the reported extraction command's pattern allows IDs with three or more digits, and staged IDs continue in a range that overlaps lane IDs; therefore these are real textual ID collisions, not a disjoint-range assumption.

## Quarantine inheritance
The likely candidate staged IDs in the dispatcher topic include S205 and S213; staged row S205 is a different dispatcher subject from the registered quarantine entry. The verdict list identifies quarantined lane IDs, not a direct staged-row disposition. Of staged rows, S205 and S213 do not occur among ScoutQuarantine's 13 listed mado absent-defect rows, so no listed quarantine verdict can be assigned to them by ID. If considering overlap with staged S205's lane-own row S188 (as flagged in MERGE-REPORT), it is not among the quarantine IDs either. Quarantine verdicts for the listed 13 rows are all `unverifiable` in `ScoutQuarantine/quarantine-verdicts.md`; no candidate staged ID inherits one on the evidence available.

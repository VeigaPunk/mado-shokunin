# ScoutRowsB report (round 43 w2) - rows S292, S293
Detail: `.ufo/waves/round-43/w2/ScoutRowsB/rows.md`.
- Both upstream files re-fetched today at commit efb5099 (tag v0.56.2 verified via GitHub API): sha256 and byte sizes equal the receipts, row cells and Gate lines.
- Anchors, kind (code), tier (A), status, opened, recheck (on-release), used-by, Gate sha256 and quotes: all HOLD. S293's Gate quote spans source lines 70-71 and is only found after whitespace normalisation (counter rule, c2-r43-gkeep-entry-v2.py:59-62) - raw `grep -F` gives 0.
- PARTIAL cells: S292 `teaches` (last clause "so the geometry a window reports is a value the layout wrote" is a cross-row inference, not in Target.cpp); S293 `teaches` (trigger is width<=2 OR height<=2 at :339; surface fallback needs both sides >5 at :342; else OR-window default :350-362 or error :364; persistent-size stored size overrides at :323-326). Exact replacement text in rows.md.
- Append-only rule (contract rule 2) means these edits need a corrective row if S292/S293 count as landed.
Tools installed: none. Scratch dir removed.

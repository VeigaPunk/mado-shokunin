# ScoutRowsC - report
Full per-cell table: `.ufo/waves/round-43/w2/ScoutRowsC/rows.md`.
Result: S294, S155, S158 re-fetched today, sha256 and byte counts equal the pins (fetch-sha256.txt); tag v0.56.2 = efb5099; held rows differ from base only in used-by (+1 item).
Defects: (1) S158 GATE quote (round-43.md:40) spans HyprCtl.cpp:428-429 across a newline: literal count 0, whitespace-normalised count 1; fix = single-line quote `sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).y), w->m_workspace ? w->workspaceID() : WORKSPACE_INVALID,` (line 428, count 1).
(2) S294 teaches tail "can differ from what is on screen" is inference, not in the file (optional reword in rows.md).
Nits: S155 anchor omits resetProps bodies; S158 anchor ranges 346-484, 613-630, 2003-2044 stop one line before the closing brace; S158 used-by omits hyprctl-verification-layer, hyprctl-flags-r28, request-limits-upstream-r31 (pre-existing).
All other cells (kind, tier, scope, anchor ranges, recheck, opened, used-by names, S155/S294 GATE quotes) verified OK.
Tools: none installed. Scratch /fast/scratch/hyaku/mado-r43/ScoutRowsC removed.

# CritW2Entry — round-45 w2: landed monitor-rule entry vs its pins

Seat: CritW2Entry. Scope: the round-45 w2 falsification (closure D1) of
`corpus/knowledge/hyprland-monitor-rule-r45.md` at `4d22eeb`, against the 14 pins in
`.ufo/waves/round-45/fetch/`. Full ledger, findings and receipts:
`.ufo/waves/round-46/w1/CritW2Entry/report.md`.

Verdict over 78 sentence units: **72 supported**, **2 supported in substance but cited at a locator that does not
carry the claim**, **1 wrong**, **3 unpinned**. All 14 pins re-fetched 2026-10-26 and byte-identical; all 71
quoted locators verified by grep (`receipts/verify-quotes.txt`, `found=71 not_found=0`, every cited line MATCH).

Findings the closure's sampling missed (it sampled 3 of 14 gate decisions and 6 of 78 sentences):

1. **F1 mis-located** `entry:84b` — "that event fires only for an output whose rule enables it
   (Hyprland-Monitor.cpp:264 and :389)". `:264` **returns at `:271`**, before the only emit site
   (`:389`); the real veto is `:275` `if (monitorRule.m_disabled)` … `:283 m_enabled = false` …
   `:286 return`. Claim true, citation points at the branch that suppresses the event.
   Correction: cite `:275-287` + `:389`.
2. **F2 false provenance** `entry:96` — the AGREE/OK/exit 0 run is attributed to
   `tools/mado-monitors.py` but cites `receipts/live-monitors-host-l1.txt`, whose tool hash is
   `c6ac5fc2…`; the landed tool at `4d22eeb` is `2f007417…` (its own receipt:
   `live-monitors-host-r45.txt`). Correction: cite the r45 receipt.
3. **F3 wrong (minor, INF)** `entry:98` — "not proof of which branch ran": with the 0.003 Hz gap the
   closeness test at Monitor.cpp:836-837 passes, so the custom push at `:838-839` never executes; it
   would have run at 100.000 Hz, while the dump shows 99.997.
4. **F4 unpinned** `entry:18b`, `entry:L107` (Hyprland `a9902ea`, externally true but no pin/receipt:
   API `a9902ea65f461af868497c4e74fed798ade0b1b0`, 2026-07-22, main's legacy `ConfigManager.cpp`
   404) and `entry:L106` (non-DRM descriptions, no pin).

Axes: quality harmed at the citation layer only; discernment's "sampled gate decisions agree" is
accurate and insufficient (a sampled pin is not a sampled sentence); coverage, depth, freshness,
adjacency unchanged. No edits made outside this seat dir; nothing installed.

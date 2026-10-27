# Superseded

This draft was the entry seat's proposal for the round-51 registry rows S364+. It is **withdrawn**:
`w1/ScrRowsDispatch/rows.md` now holds the final, quote-verified, paste-ready rows, and the entry
cites exactly that set (S364-S369) and nothing else.

Kept as a taste record only. Two corrections the withdrawal produced are worth keeping:

1. Row S365's anchor range for the translator's implementation table is `:797-867` (71 assignments,
   `m_dispMap["exec"]` at :797 to `m_dispMap["releaseinputcapture"]` at :867), not `:819-861`; the
   declaration is `DispatcherTranslator.hpp:19`. Reported to the rows seat.
2. `Cannot set submap` is at `ConfigActions.cpp:1681`, not :1678.

The parts of this proposal that the final rows do not carry - hyprutils `VarList`/`VarList2`, the
two wiki pages, and `src/config/ConfigManager.cpp` - are now cited only in the entry's Limits
section, without rows, which is the discipline the rows seat's rule 4 prescribes for a
documentation or trigger contrast that grounds no mechanism claim.

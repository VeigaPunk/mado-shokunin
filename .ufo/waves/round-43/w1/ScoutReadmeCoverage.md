# ScoutReadmeCoverage — report (round 43, w1)
Status: DONE. Full map: `.ufo/waves/round-43/w1/ScoutReadmeCoverage/coverage.md`.

Findings (OBS, git grep at base a35cfdf):
- Base held NONE of: RE2 FullMatch at source, floating-algorithm size/float box, GEOMETRIC_GOAL/`clients -j` `size` semantics, gkeep window size (registration probe reproduced: empty). It held rule syntax/order/static-vs-dynamic (`keybind-rule-semantics.md` §4, incl. `:249` `[UNK]` for ai-usage W×H), `getprop` effect read (`window-rule-effects-getprop.md`), tag attribution (`rule-attribution-r24.md`), gkeep installation drift (`config-drift-r12.md`), and `clients -j` fields tags/floating/xwayland only.
- Moves: README Frontier `:109-111` (per-window rule effects — one slice only; already partly moved by `:126-130` round 12), coverage-map new row after `:70`; adjacent rows `:34,:47,:16,:37,:69`; tool-pointer precedent `:51`.
- PROVINCE: in province (`:6-9` hypr rules); `tools/` inventory table needs a geometry-tool row (tool reads bytes only); 3 older tools (options/wsrules/eventq) are unrowed at base (prior debt). Adjacent owners: kagi/kama/kengaku/tsukuroi/tameshi/mori; gkeep project is operator-owned.
- Overlap flag: reserved S291 == held S155 and S296 == held S158 byte-for-byte (sha `fec33f9a…`, `798b7c6c…`); round-38 precedent maps to held ids. Other 8 reserved ids are new bytes.
- Honest credit: new ground = the rule→box→`clients -j` size chain + first tool reading a reported window size (C1, operability); DEEPENING (not new) for the rules surface; no observed gkeep size (no window open); not "rule effects" closed; round 42 left no prior credit.

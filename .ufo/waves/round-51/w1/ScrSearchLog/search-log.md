Round 51 (2026-10-27), bounded C2 question: once a bind has matched at 0.56.2, how does its dispatcher string execute —
where the dispatcher and its argument are stored at parse time, which table resolves the name at press time, how the
argument reaches the dispatcher, which branches are special (submap, pass, the mouse press-state prefix, long-press and
repeat) and how `hyprctl dispatch` reaches the same table? Where searched: the pinned Hyprland tree at
`efb50993780079460b0cbed1363e2166a2de1d9f`, every path resolved from that commit's own tree listing (1028 blobs,
`truncated=false`); the pinned hyprland-wiki at `d5f07c60e16fe03744aabb76e492117b7f7c4679` (126 blobs, `truncated=false`);
and the held corpus — the round-50 bind-key-match entry, its pins, and rows S352/S353/S359/S363. Identified: 15 sources
opened — eleven Hyprland files (`src/managers/KeybindManager.{cpp,hpp}`, `src/config/legacy/DispatcherTranslator.{cpp,hpp}`,
`src/debug/HyprCtl.cpp`, `src/config/shared/actions/ConfigActions.{cpp,hpp}`, `src/config/legacy/ConfigManager.cpp`,
`src/SharedDefs.hpp`, `src/config/ConfigManager.cpp`, `docs/hyprctl.1.rst`), three wiki pages
(`Configuring/Basics/Binds.md`, `Configuring/Basics/Dispatchers.md`, `Configuring/Advanced and Cool/Using-hyprctl.md`) and
one held entry (`corpus/knowledge/hyprland-bind-key-match-r50.md`). Screened: 11 — the opens that passed screening for the dispatch
phase (the other four failed it, below). Included: 6 rows, S364–S369, each carrying status `mined`, opened 2026-10-27, recheck `on-release`, used-by
`corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` and a pin binding under `.ufo/waves/round-51/fetch/` as claim C2
clause (b) requires: S364 the construction-time `m_dispatchers` population (71 names, each delegating to the translator),
the map's declared type, the press-time find and call with the submap break and the success-to-`found`/`passEvent` step;
S365 the translator's `run` over its own 71-entry map, the `focuswindowbyclass` alias, the inert `setignoregrouplock`, and
per-dispatcher `CVarList2` splitting; S366 `dispatchRequest`'s first-space split, its lookup and invalid-name reply, and its
Lua branch; S367 `Actions::setSubmap` with the `m_currentSubmap`/`m_passPressed` state fields; S368 the bind line's handler
field — extraction, mouse override, lowercasing, parse-time existence check, and the argument kept verbatim; S369
`SDispatchResult`'s defaults (`passEvent=false`, `success=true`). Two of the nine row-bearing files are held pins reopened
for a scope their held rows do not cover (S352 owns the bind match, S353 the key field; the dispatch side is new).
Excluded: 4 — `Configuring/Basics/Dispatchers.md` and `Configuring/Advanced and Cool/Using-hyprctl.md` at `d5f07c60` are
Lua-era pages only ("Since Hyprland 0.55, hyprlang is deprecated in favor of lua", `Dispatchers.md:7-8`; `hyprctl dispatch`
documented as a shorthand for `eval 'hl.dispatch(...)'`, `Using-hyprctl.md:53-58`), so neither can ground a claim about the
legacy parser this host runs; `docs/hyprctl.1.rst` restates the reply contract S366 already grounds in code (rule 4) and
both of its `dispatch` examples are Lua `hl.dsp.*` calls (`:32-34`, with `:40` noting Lua-provider behaviour); and
`src/config/ConfigManager.cpp` is the lua-versus-legacy manager selection (`:33-52`), held ground for the config-era route
(`corpus/knowledge/hyprland-config-era-r12.md`), not a dispatcher fact. Flip for the wiki pair: a pinned pre-0.55 revision
that documents the hyprlang dispatcher table. One candidate mechanism claim was rejected against the pins instead of
admitted: "the argument is split on commas at dispatch time" — the bind path cuts the value into at most `numbArgs` fields
and keeps the rest verbatim (`CVarList(value, numbArgs)`, legacy `ConfigManager.cpp:1555`; `COMMAND = ARGS[3 + …]`, `:1586`)
and `hyprctl` splits at the first space only (`HyprCtl.cpp:1143`); comma splitting belongs to individual dispatchers, never
to the dispatch path. Two further screened locations take no row: wiki `Configuring/Basics/Binds.md` (already held as S359;
the fresh open at `d5f07c60` hashes byte-equal to the round-50 pin, sha256
`3d8a2a6832da59304697aff1a3c72a35e02ea43737035c99b841d0854b17d628`) and the round-50 entry (held ground — it stops where
the match ends). Stop: every step the entry states has a pinned line at `efb50993` — the parse-time field split that leaves
the handler and the whole remaining field, the 71-name `m_dispatchers` table whose entries delegate to
`Config::Legacy::translator()->run`, the press-time lookup and call, the translator's own 71-entry map with per-dispatcher
splitting, the submap and pass branches, and the hyprctl path through the same table — and nothing was fired (no key
injected, no `hyprctl dispatch`, no layout switch). Re-open when Hyprland leaves `efb50993`, or when a pre-0.55 wiki
revision is pinned for dispatcher prose.
Counting command: identified = 11 Hyprland files + 3 wiki pages + 1 held entry = 15; screened (passed) = 15 − 4
failed = 11;
included = `printf '%s\n' S364 S365 S366 S367 S368 S369 | wc -l` → 6; excluded sources = 4, plus one refuted claim, which
is not a source. Opens, digests and every anchor greped: `.ufo/waves/round-51/w1/ScrSearchLog/receipts/opens-and-counts.txt`.
One carry: S369's pin was still in flight when this note was drafted — if the freeze lands without it, S369 drops and the
included count reads 5.

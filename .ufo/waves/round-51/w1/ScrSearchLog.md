# ScrSearchLog — round 51 w1: the SOURCES.md search-log entry

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` (round base `6ca8c559a4a3d6d361101592116eea2bc7452437`).
Role: scribe, leaf. No tracked file created, edited or deleted; no mutating git/jj anywhere; no config-plane
write, no compositor socket, no service touched. Nothing was executed against Hyprland.

## Deliverables
- `.ufo/waves/round-51/w1/ScrSearchLog/search-log.md`
- `.ufo/waves/round-51/w1/ScrSearchLog/receipts/opens-and-counts.txt`

## Behavior (what the draft entry says, and on what)

`search-log.md` holds one PRISMA-inspired note for `corpus/SOURCES.md` (`CORPUS.md` rule 5: question, where
searched, date, identified / screened / included / excluded counts, exclusion reasons, stop rationale), written to be
pasted as a single prose block (no heading lines):

- **Question** — after a match at 0.56.2, how a keybind's dispatcher string executes: parse-time storage of
  dispatcher + arg, the press-time table, argument delivery, the submap/pass/mouse-prefix/repeat branches, and the
  `hyprctl dispatch` route.
- **Where searched** — pinned Hyprland tree `efb50993…` (paths resolved from that commit's own tree listing: 1028
  blobs, `truncated=false`), pinned hyprland-wiki `d5f07c60…` (126 blobs, `truncated=false`), held corpus (round-50
  bind-key-match entry, its pins, rows S352/S353/S359/S363).
- **Counts** — identified **15**, screened **11**, included **6** (rows **S364–S369**), excluded **4** sources plus one
  refuted claim (a claim is not a source, so it is counted separately). Arithmetic in the note: `15 = 11 + 4`;
  `11 = 9 row-bearing file locations (6 rows; three .hpp anchors fold into their row) + 2 held ground`.
- **Included, per row (rows seat's corrected ids, verified at the pins)** — S364 construction-time `m_dispatchers`
  population (71 names → translator) + declared type + press-time find/call + submap break + success→`found`/`passEvent`;
  S365 translator `run` over its 71-entry map + `focuswindowbyclass` alias + inert `setignoregrouplock` + per-dispatcher
  `CVarList2` splitting; S366 `dispatchRequest` first-space split + lookup + invalid-name reply + Lua branch; S367
  `Actions::setSubmap` + `m_currentSubmap`/`m_passPressed`; S368 the bind line's handler field (extraction, mouse
  override, lowercasing, parse-time existence check, argument kept verbatim); S369 `SDispatchResult` defaults
  (`passEvent=false`, `success=true`).
- **Exclusions and reasons** — wiki `Configuring/Basics/Dispatchers.md` and `Configuring/Advanced and Cool/Using-hyprctl.md`
  at `d5f07c60` (Lua-era only: `Dispatchers.md:7-8` "Since Hyprland 0.55, hyprlang is deprecated in favor of lua";
  `Using-hyprctl.md:53-58` `dispatch` = shorthand for `eval 'hl.dispatch(...)'`); `docs/hyprctl.1.rst` (restates the
  reply contract S366 grounds in code — rule 4 — and both `dispatch` examples are Lua `hl.dsp.*`, `:32-34`, `:40`);
  `src/config/ConfigManager.cpp` (lua-vs-legacy manager selection, `:33-52`, held ground for the config-era route
  `corpus/knowledge/hyprland-config-era-r12.md`). Flip for the wiki pair: a pinned pre-0.55 revision documenting the
  hyprlang dispatcher table.
- **One claim rejected against the pins, not admitted as an exclusion** — "the argument is split on commas at dispatch
  time": the bind path cuts the value into at most `numbArgs` fields and keeps the rest verbatim (`CVarList(value,
  numbArgs)`, legacy `ConfigManager.cpp:1555`; `COMMAND = ARGS[3 + …]`, `:1586`), and `hyprctl` splits at the first space
  only (`HyprCtl.cpp:1143`); comma splitting belongs to individual dispatchers.
- **Two held pins reopened, not duplicated** — S352 owns the bind match, S353 the key field; S364/S368 own the dispatch
  and handler-field lines their held rows do not cover. Wiki `Basics/Binds.md` stays held as S359 (fresh open at
  `d5f07c60` is byte-equal to the round-50 pin, sha256 `3d8a2a68…d628`), and the round-50 entry is held ground.
- **Stop** — every stated step has a pinned line at `efb50993`; nothing was fired (no key injected, no `hyprctl
  dispatch`, no layout switch); re-open when Hyprland leaves `efb50993` or a pre-0.55 wiki revision is pinned.
- **One carry stated in the note** — S369's pin was still in flight at drafting; if the freeze lands without it, S369
  drops and the included count reads 5.

Provenance of the row list: `ScrRowsDispatch` sent a first id/scope set, then corrected it (S364 KeybindManager.cpp,
S365 DispatcherTranslator.cpp, S366 HyprCtl.cpp, S367 ConfigActions.cpp, S368 legacy ConfigManager.cpp, S369
SharedDefs.hpp; five exclusions). The note carries the corrected set; the corrected exclusions
(`docs/hyprctl.1.rst`, `src/config/ConfigManager.cpp`, the comma-split claim) I then opened and checked myself before
putting them in the note — nothing in the note rests only on that message. Facts I verified at the pins:
`KeybindManager.cpp:41-113` (71 unique names, each delegating to `Config::Legacy::translator()->run`), `:785-800`
(lookup + call), `:842` (`res.passEvent |= !found`), `KeybindManager.hpp:137`, `DispatcherTranslator.hpp:16`,
`DispatcherTranslator.cpp:30,796` (71 `m_dispMap[` entries), `HyprCtl.cpp:1126,1143,1151`, `ConfigActions.cpp:1664-1681`,
`ConfigActions.hpp:114,118`, legacy `ConfigManager.cpp:1555,1584,1586,1591,1598`, `SharedDefs.hpp:52-56`,
`src/config/ConfigManager.cpp:33-52`, `docs/hyprctl.1.rst:24,32,40`, wiki `Dispatchers.md:7-8`, `Using-hyprctl.md:53-55`.
The 71/71 name counts were re-derived, not copied (`receipts/opens-and-counts.txt`).

## Gates / checks run (only these)

- `sha256sum` over all 12 fresh opens and the 3 held pins; wiki fresh `Binds.md` == `.ufo/waves/round-50/fetch/wiki-Binds.md`
  (`3d8a2a6832da59304697aff1a3c72a35e02ea43737035c99b841d0854b17d628`), and the 12 re-fetched hashes are identical to the
  first pass's (byte-stable at the pins).
- The four count commands (`printf '%s\n' … | wc -l`) → `15 / 11 / 6 / 4`, recorded verbatim with their inputs.
- Tree-listing truncation flags for both pins (`truncated=false`).
- `GIT_OPTIONAL_LOCKS=0 git diff --stat` → empty (no tracked file modified); `git status --porcelain` shows only
  `?? .ufo/waves/round-51/w1/ScrSearchLog.md` and `?? .ufo/waves/round-51/w1/ScrSearchLog/`.
- Disk guard before the pass: `/fast` 281 G free (66 % used); no ENOSPC.
- `test -f` over the three declared paths → all present; the note is plain text with no `/home/…` path and no
  `op://` reference (`python3` scan), and its only cited row ids are S352/S353/S359/S363 (held) and S364–S369 (new).
- Not run: any product counter, the C2 counter, any build/test/lint — other seats own them; I did not re-run peers'
  work to decorate this report.

## Findings for freeze (observed, reported — not fixed by me)

1. **Where the entry can land.** At base, `corpus/SOURCES.md` has `## Search log` at `:360` and
   `## Leads (unopened)` at `:524`; the last search-log note is **Round 41** and sits at `:552-554`, i.e. *inside*
   the Leads block, because rounds append at EOF. Command:
   `GIT_OPTIONAL_LOCKS=0 git show 6ca8c559…:corpus/SOURCES.md | grep -n '## Search log\|## Leads\|^Round 41'`
   → `360 / 524 / 552`. Recommended insertion: append after `:554` (EOF) with the `Round 51 (2026-10-27), …` lead-in —
   the placement round 41 took, chronology intact. Inserting before `:524` would put round 51 ahead of the round-41
   note and is not recommended; moving the round-41 note under the heading is an append-only-sensitive edit — L1's
   call, not mine.
2. **Rounds 42–50 have no `SOURCES.md` search-log note.** `grep -n '^Round\|^\*\*Round'` at base reads 13 headings,
   last = Round 41; `grep -rn '## Search log' corpus/lessons/round-4*.md corpus/lessons/round-5*.md` finds it only in
   `round-45.md:72`, `round-46.md:73`, `round-47.md:63`, `round-48.md:210` — rounds 49 and 50 logged no bounded-search
   note in either place. Pre-existing gap; routed here rather than silently repaired.
3. **Correction of my own first reading:** the round-41 note is *not* truncated. `read` showed it ending mid-sentence;
   the raw bytes are complete (`809` chars on `:554`; file 264837 B, newline-terminated, tail `… is an open lead, not a
   row.`). Display truncation, not a defect — recorded so no one inherits the claim.
4. **Path traps worth reusing.** `src/config/ConfigActions.cpp`, `content/Configuring/Dispatchers.md` and
   `content/Configuring/Using-hyprctl.md` are 404 at these pins; the real paths are
   `src/config/shared/actions/ConfigActions.cpp`, `content/Configuring/Basics/Dispatchers.md` and
   `content/Configuring/Advanced and Cool/Using-hyprctl.md` (URL needs `%20`). Resolve from the pinned tree listing.
5. **Row-id churn inside the wave.** The rows seat's first set differed from its final set (S365/S369 changed subject,
   and a sixth `.hpp` row disappeared). The note carries the final set plus the S369 carry; if the rows seat renumbers
   again before the freeze, the note's `Included:` clause must be amended with it.

## Out of scope (deliberately untouched)

- `corpus/SOURCES.md` itself (L1 integrates), `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` and the rows
  (`ScrDispatchEntry` / `ScrRowsDispatch`), `quality/counters/c2-r51-dispatch-entry.py`, the C1 tool-ledger artifacts,
  round-50 bytes including `.ufo/waves/round-50/fetch/SHA256SUMS`, `.ufo/state/`, other lanes, `templates/`,
  `scripts/`, `MANIFEST.json`, the shokuknow checkout, and the host config planes.

## Scratch

`/fast/scratch/hyaku/mado-r51/ScrSearchLog/` (fresh opens, two tree listings, one receipt generator); every receipt
copied into the seat dir above, then the scratch tree deleted. No tool installed, so nothing to record under the
tooling authorization.

Report: .ufo/waves/round-51/w1/ScrSearchLog.md — deliverables: .ufo/waves/round-51/w1/ScrSearchLog/search-log.md, .ufo/waves/round-51/w1/ScrSearchLog/receipts/opens-and-counts.txt

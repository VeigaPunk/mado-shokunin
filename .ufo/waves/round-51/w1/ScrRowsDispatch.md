# ScrRowsDispatch — round-51 w1: new registry rows S364–S369 (draft)

seat: ScrRowsDispatch (scribe, leaf) · lane: mado-shokunin · wave w1 · date 2026-10-27
claim served: C2 (coverage, sourced) — `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md`
lane base `6ca8c559` · lane HEAD during the seat `3ac31642` (w1 dispatch/spec only; `corpus/SOURCES.md`
unmodified, `git status --porcelain corpus/SOURCES.md` empty, 300 rows at HEAD)

## Deliverables
- `.ufo/waves/round-51/w1/ScrRowsDispatch/rows.md`
- `.ufo/waves/round-51/w1/ScrRowsDispatch/verify-quotes.py`
- `.ufo/waves/round-51/w1/ScrRowsDispatch/quote-greps.txt`

## What was done

Six registry rows drafted in the 11-column shape of `corpus/SOURCES.md`, all at Hyprland
`efb50993780079460b0cbed1363e2166a2de1d9f` (v0.56.2, the host's build), all kind `code`, tier `A`,
status `mined`, opened `2026-10-27`, recheck `on-release`, used-by the C2 entry:

| id | source | scope (one line) |
|---|---|---|
| S364 | `src/managers/KeybindManager.cpp` (+ `.hpp`) | `m_dispatchers` population (71 names), map type, press-time find/call, mouse press-state prefix, submap break, success→found and `passEvent` |
| S365 | `src/config/legacy/DispatcherTranslator.cpp` (+ `.hpp`) | `run()` name resolution over the 71-entry `m_dispMap`, alias `focuswindowbyclass`→`focuswindow`, inert `setignoregrouplock`, per-dispatcher `CVarList2` argument splitting |
| S366 | `src/debug/HyprCtl.cpp` | `dispatchRequest`: first-space split, same map lookup, `Invalid dispatcher`, `ok`/error reply, lua branch wrapping `hl.dispatch(in)` |
| S367 | `src/config/shared/actions/ConfigActions.cpp` (+ `.hpp`) | `Actions::setSubmap`: `reset`/empty clears and posts an empty submap event, unregistered name fails "wasn't registered", plus the `m_currentSubmap`/`m_passPressed` state fields |
| S368 | `src/config/legacy/ConfigManager.cpp` | bind dispatcher field extraction, mouse override, lowercasing, parse-time existence check, `arg` stored verbatim |
| S369 | `src/SharedDefs.hpp` | `struct SDispatchResult` defaults (`passEvent=false`, `success=true`) that decide pass-vs-consume |

Mechanism chain the rows make citable end to end: parse (`legacy ConfigManager::handleBind`
`:1584-1599`, stored on `SKeybind` `:1624-1631`) → map construction (71 lambdas → translator
`:41-113`) → name table (`m_dispMap` `:819-861`) → press-time call with the whole arg
(`:785`, `:812`) → submap break (`:816-819`) and `submap=reset` (`ConfigActions.cpp:1664-1682`) →
`hyprctl dispatch` reaching the same map (`HyprCtl.cpp:1126-1158`).

## Gates I ran (all local, read-only over pins)

| Check | Command (seat artifact) | Observed |
|---|---|---|
| Eight quotes verbatim at the cited line, ≤25 words, no `|` | `quote-greps.txt` (grep -nF per quote) | 8/8 match at :785, :137, :32, :19, :1149, :1681, :1594, :53 |
| Same, machine-checked with size+sha256 per pin | `verify-quotes.py <fetch> <round-50-fetch>` | `ROWS=6 CHECKS=8 BAD=0 verdict=OK`, exit 0 |
| Pin ↔ round-50 identity | same run (cmp section) | `Hyprland-KeybindManager.cpp` and `Hyprland-legacy-ConfigManager.cpp` `byte_equal=True` |
| 71/71 name-set equality (S364 vs S365) | inline python over the two pins | `km names 71 table 71`, both set differences empty |
| Registry shape (contract census commands on the six rows extracted from §1) | malformed `NF!=13`, tier/kind/status enums, tier inflation, id dup vs the 300 held rows | rows 6, malformed 0, `A=6`, no enum violation, no tier inflation, no id collision, next free id at base S363 |
| Cell safety | each quote and cell checked for `|` | none; all six rows parse as exactly 11 columns |

Not run by this seat (main-agent/L1 job): the lane's `scripts/sources-census.sh validate`, any build,
any host probe, any compositor connection. Nothing was dispatched on the host; every fact is from
pinned bytes.

## Findings

1. **The dispatcher surface is two tables, not one.** `m_dispatchers` (KeybindManager) holds 71
   lambdas that each call `Config::Legacy::translator()->run(name, args)`; `m_dispMap`
   (DispatcherTranslator) holds the 71 implementations. The two name sets are equal (set difference
   empty both ways). A bind's handler is validated against the first at parse time
   (`legacy ConfigManager.cpp:1594-1599`) and looked up in it again at press time
   (`:785`), and `hyprctl dispatch` looks it up in the very same map (`HyprCtl.cpp:1149`).
2. **There is no global argument grammar.** The bind path never splits (`:1586` stores the rest of
   the line as COMMAND, `:812` passes `k->arg` whole); `hyprctl` splits at the first space only
   (`:1143-1147`); the split happens inside each dispatcher with its own `CVarList2` separator
   (`:162` `' '`, `:189` `' '`, `:476`/`:503` `'s'`, `:532`/`:592` omitted, `:773` `' '`). Any entry
   sentence positing comma-splitting at dispatch time would be false — recorded as rejection 4 in
   `rows.md` §4.
3. **Two named special cases are code-level.** `submap` sets `found = true` and `break`s the
   remaining matched binds (`KeybindManager.cpp:816-819`), and its action clears the submap only for
   `reset`/empty and otherwise requires a registered bind carrying that submap
   (`ConfigActions.cpp:1665-1680`, else `:1681` "wasn't registered"). `pass`/`global`/
   `sendshortcut`/`mouse` are the special-dispatcher list at `:782`.
4. **Documentation drift, doc-vs-code (for the entry's Limits, not a row):** the shipped man page
   `docs/hyprctl.1.rst:26` says an argument must be present, but `HyprCtl.cpp:1145-1147` leaves
   `DISPATCHARG` empty when no space follows the name and still calls the dispatcher. Its two
   examples are lua-form only.
5. **Host era is legacy.** `ls ~/.config/hypr` (2026-10-27, read-only): `hyprland.conf` present, no
   `hyprland.lua` — so the hyprlang path these rows describe is the one that applies here; the lua
   branch at `HyprCtl.cpp:1130-1141` would take over if a `hyprland.lua` appeared.
6. **Five candidates rejected under rule 4 / attribution** (full text + flips in `rows.md` §4):
   `docs/hyprctl.1.rst` (restates what S366 grounds in code), wiki `Dispatchers.md` and
   `Using-hyprctl.md` at d5f07c60 (both document only the lua `hl.dsp.*`/`hl.dispatch` surface —
   "Since Hyprland 0.55, hyprlang is deprecated in favor of lua"), `src/config/ConfigManager.cpp`
   (config-era selection is held ground in `hyprland-config-era-r12.md`), and a "comma grammar"
   row (false).
7. **Post-draft correction (peer review, same wave).** `ScrDispatchEntry` re-grepped the S365 pin
   and caught my `m_dispMap` range: the first draft said `:819-861`, which starts inside the table
   and stops six entries early. Re-verified here — first assignment `:797` (`m_dispMap["exec"]`),
   last `:867` (`m_dispMap["releaseinputcapture"]`), 71 assignments, constructor at `:796` — and
   corrected in the S365 anchor and the §3c label, with the grep evidence logged in `rows.md` §7.
   No quote, digest or gate result moved (the row quote is `:32`).
8. **No S370+ rows were added.** The entry seat asked (non-blocking) for hyprutils `VarList`/`VarList2`
   rows for the capped-split primitive. This seat's budget is S364-S369 and the entry keeps that
   reading in Limits, so rule 4 excludes it. I verified both claims anyway so the Limits note is not
   fiction: `CVarList` does implement the last-field remainder (`Hyprutils-VarList.cpp:20-21`) and
   `lastArgNo` reaches `CVarList2::construct` as a parameter that the body never reads
   (`grep -n lastArgNo Hyprutils-VarList2.cpp` → lines 8, 10, 13, 14, 17, 18, 21 only). Same check
   produced the default separator (`VarList2.hpp:18`, `delim = ','`), now stated in S365's teaches
   and in rejection 4.
9. **Census effect for the L1:** 300 → 306 rows; expect exactly two W04 duplicate-URL-across-scopes
   warnings — S364 on the S352 URL and S368 on the S353 URL, both at new scopes (map/call, and
   dispatcher field/validation) — the pre-existing class accepted at round-50 closure. All six rows
   are `mined`, so the "used-by path does not exist" sweep will flag them unless the C2 entry lands
   in the same commit.

## Coordination (peers)

- `ScrSearchLog` first wrote its search-log note against my interim mapping (S365 = the `.hpp`
  row, S366 = translator, S369 = legacy ConfigManager, no SharedDefs row). I sent the corrected
  mapping; **its note needs amending to the six ids above**, and its exclusion list to the five in
  finding 6. The ids themselves are stable: S364–S369.
- `ScrDispatchEntry` published `w1/ScrDispatchEntry/rows-proposal.md`; it is superseded. Its rows
  carry truncated digests (`…`), no row has a ≤25-word quote, and its S368 needs a pin that was not
  in the fetch set. Its translator, HyprCtl, ConfigActions-state and SharedDefs rows map onto my
  S365, S366, S367 and S369; its `src/config/ConfigManager.cpp` row is rejected here as held ground.
  It has since confirmed the entry cites exactly S364-S369 and nothing else, and supplied the range
  correction recorded in finding 7.
- `ExecFetchDispatch` confirmed `Hyprland-SharedDefs.hpp` is pin #12 of 19 in its fetch set
  (1,915 B, sha256 `0b40cc83…`, git blob `bb7c601e…` recomputed from bytes, `self_row_lines=0`), so
  S369 is not blocked. If the pin ever fails to reach `.ufo/waves/round-51/fetch/`, drop S369 —
  stated in `rows.md` §5.

## Touched surfaces (write scope)

- Written: `.ufo/waves/round-51/w1/ScrRowsDispatch/{rows.md,verify-quotes.py,quote-greps.txt}` and
  this report file. Scratch `/fast/scratch/hyaku/mado-r51/ScrRowsDispatch/` created and deleted.
- Read only: lane `corpus/SOURCES.md`, `corpus/knowledge/*` (grep), `corpus/lessons/round-50-*.md`,
  `CORPUS.md`, `.ufo/waves/round-51/{claims.md,w1-spec.json,w1-dispatch.json}`,
  `.ufo/waves/round-50/fetch/*`, `.ufo/waves/round-51/w1/{ExecFetchDispatch,ScrDispatchEntry}/*`,
  `~/.config/hypr` (directory listing only).
- Not touched: any tracked file, `templates/`, `scripts/`, `MANIFEST.json`, `.ufo/state/`,
  `.ufo/watchdog.log`, `.scratch/`, the shokuknow checkout, any git/jj mutation, any config plane,
  any compositor socket, any host service.

## Out of scope / not done

- No row was written into `corpus/SOURCES.md` (L1 is the only committer; paste-ready rows only).
- No knowledge entry, no counter, no lesson, no SCORECARD/LOG edit — C2's entry, its counter and the
  round lesson belong to other seats.
- No independent host measurement of dispatch behaviour (a live `hyprctl dispatch` would mutate the
  compositor; forbidden here). Everything above is pinned-bytes reading.

## Tooling

No installs, no upgrades, no pacman transactions. `curl`, `python3`, `grep`, `awk`, `cmp` only.

Report: .ufo/waves/round-51/w1/ScrRowsDispatch.md

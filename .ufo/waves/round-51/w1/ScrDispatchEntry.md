# ScrDispatchEntry — round-51 w1 draft of the dispatcher-dispatch entry (C2)

Status: complete. Draft delivered in the seat directory; nothing tracked was edited, no host state
was touched, no compositor socket opened, no `hyprctl` call made.

## What was built

`hyprland-dispatcher-dispatch-r51.md` — the C2 knowledge entry, ~2,900 body shingles, six sourced
steps plus a state-claims table, and it is shaped to the frozen counter rather than to prose taste:
six `source:` lines (one ≤25-word quote + one locator each, each locator to that row's own pin), a
`| pin | file | row |` manifest, seven `held:` lines, and a Limits section for the four pins that
carry no registry row.

The entry covers, in order: the 71-name table in the `CKeybindManager` constructor and the second
71-entry table behind it; what the bind line stores for `handler` and `arg` (positional field,
lowercased name, verbatim tail, parse-time validation against the same table a press uses); the
three call sites (press loop, long-press timer, repeat timer); what the callable receives (the
three-valued `m_passPressed` write before/after, the raw argument, the mouse `"1"`/`"0"` prefix,
and `SDispatchResult`'s forgiving defaults); `submap` as a name captured at parse and written at
dispatch by the only writer that exists, with its refusal and its two break rules; `pass` as a
re-key into another window whose edge behaviour is entirely `m_passPressed`; the absence of any
shared argument grammar (five dispatchers read the same tail five ways); the `hyprctl dispatch`
path into the same table with no press marker; and which branch this host takes.

It deliberately starts where the round-50 match entry stops and re-argues nothing about matching.

## Gates run (all on this seat's own bytes)

| gate | command shape | result |
|---|---|---|
| PRED-C2-r51, all four clauses | `python3 -I …/ExecCounterC2/c2-r51-dispatch-entry.py --repo <scratch clone> --rev bc3376b5 --work <scratch>` | `a ok=1`, `b rows=6/2 pins=6`, `c body_shingles=2900 max=0.1%`, `d held=7/3 tokens=14`, `clauses_met=4 admitted=1/1 verdict=TARGET_MET`, rc 0 |
| same counter at the round base | `--rev 6ca8c559a4a3…` | `a ok=0 entry=absent … clauses_met=0 verdict=TARGET_MISSED` |
| held citations at base | `git show 6ca8c559:corpus/knowledge/<file> \| sed -n '<line>p'`, all seven | every key token present verbatim |
| pin identity with round-50 | `cmp` of `Hyprland-KeybindManager.cpp` and `Hyprland-legacy-ConfigManager.cpp` | identical |
| fresh pin bytes | `curl -fsSL` of `src/SharedDefs.hpp` @ `efb50993`, independent of the fetch seat | sha256 `0b40cc83…`, matches their pin exactly |

Receipt: `counter-fit-receipt.txt` (raw counter output, final revision).
The fit run needed a scratch clone with the six rows, one README index row and the pins in place;
that fixture is in `/fast/scratch/hyaku/mado-r51/ScrDispatchEntry/lane-clone` and was deleted at
the end of the seat (see Scratch).

## Touched surfaces

Written, all under the seat directory and this report:

- `.ufo/waves/round-51/w1/ScrDispatchEntry/hyprland-dispatcher-dispatch-r51.md`
- `.ufo/waves/round-51/w1/ScrDispatchEntry/held-citations.md`
- `.ufo/waves/round-51/w1/ScrDispatchEntry/pin-manifest.md`
- `.ufo/waves/round-51/w1/ScrDispatchEntry/rows-proposal.md` (superseded; kept as a taste record)
- `.ufo/waves/round-51/w1/ScrDispatchEntry/counter-fit-receipt.txt`
- `.ufo/waves/round-51/w1/ScrDispatchEntry/fetch/Hyprland-SharedDefs.hpp`
- `.ufo/waves/round-51/w1/ScrDispatchEntry.md`

`git status --porcelain` in the lane shows no modified tracked file from this seat.

## Integration prerequisites (for the L1; not done here on purpose)

1. Promote the pins to `.ufo/waves/round-51/fetch/` — the sixteen named in `pin-manifest.md` are
   already in `.ufo/waves/round-51/w1/ExecFetchDispatch/fetch/` (plus `Hyprland-SharedDefs.hpp`).
   Clause (b) resolves pin names against that directory.
2. Register rows S364-S369 from `.ufo/waves/round-51/w1/ScrRowsDispatch/rows.md` (not from my
   withdrawn `rows-proposal.md`) with `status=mined`, `opened=2026-10-27`.
3. Add the `corpus/README.md` index row naming `knowledge/hyprland-dispatcher-dispatch-r51.md` —
   clause (a) fails without it, whatever the entry says.
4. Copy the entry to `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` unchanged; the counter
   was run against these exact bytes (`bc3376b5` in the fixture chain).

## Findings worth routing

1. **Row anchor defect, found and already fixed by the rows seat.** S365's anchor located the
   translator's implementation table at `:819-861`; the table is `:797-867` (71 assignments,
   `m_dispMap["exec"]` first, `m_dispMap["releaseinputcapture"]` last). Reported with the grep
   transcript; `ScrRowsDispatch` corrected `rows.md` and re-verified (`ROWS=6 CHECKS=8 BAD=0`).
2. **`CVarList2` does not implement the parameter its header documents.** `CVarList` implements the
   last-field remainder (`Hyprutils-VarList.cpp:20-21`), which is what lets a bind's fourth field
   keep its commas; `CVarList2::construct` never reads `lastArgNo` (the identifier occurs only in
   the four constructor heads, their calls, and the definition). Consequence: `sendshortcut`'s
   three-field test counts every comma, so a fourth field is rejected rather than absorbed. Kept in
   Limits (no registry row for hyprutils; rows seat rule 4), confirmed independently by the rows
   seat.
3. **Three distinct failure strings for one bad dispatcher name**, one per path: `does not exist`
   (parse), `Bad dispatcher` (translator called directly), `Invalid dispatcher` (socket). Quoting
   one does not identify the other two; recorded as an OBS.
4. **Documentation-vs-code gap on the socket verb's argument.** The shipped man page says an
   argument must be present; `HyprCtl.cpp:1145-1147` still calls the dispatcher with an empty
   argument when no space follows the name. Left in Limits with pin cites, per the rows seat.
5. **Host branch consequence, sourced.** This host's config directory holds `hyprland.conf` and no
   `hyprland.lua` (read-only listing), so the Lua guard at `HyprCtl.cpp:1130` does not fire and
   `hyprctl dispatch <name> <args>` takes the space-split branch — while the pinned wiki documents
   only the Lua form. A reader following the page would write the wrong shape here.
6. **Error-path economics of a submap switch.** `setSubmap` writes only after scanning the bind list
   for a carrying bind, so a submap exists only because a bind line named it, through either front
   door. This is the fact that makes a socket-issued submap switch safe to reason about, and it is
   now stated with its setter line.

## Out of scope (deliberately not done)

- No key event, no `hyprctl` call, no reload, no compositor socket: mechanisms are source-read.
- No runtime test of `pass`, of a submap switch, or of the repeat/long-press path; the repeat
  consequence is marked `[INF]` in the entry.
- No entry for the Lua config path (`src/config/lua/`, `hl.dispatch`); only the branch's existence
  and this host's non-use of it are claimed.
- No registry rows written, no `corpus/README.md` edit, no `corpus/SOURCES.md` edit, no commit.

## Scratch

Work directory `/fast/scratch/hyaku/mado-r51/ScrDispatchEntry` (scratch clone, counter work dir,
fetched bytes). Deleted before this report was finalised; nothing outside the seat directory and
this report was left behind. Disk check at start: `/fast/scratch/hyaku` 63% used, 302.5G free.

## Deliverables

- `.ufo/waves/round-51/w1/ScrDispatchEntry/hyprland-dispatcher-dispatch-r51.md`
- `.ufo/waves/round-51/w1/ScrDispatchEntry/held-citations.md`
- `.ufo/waves/round-51/w1/ScrDispatchEntry/pin-manifest.md`
- `.ufo/waves/round-51/w1/ScrDispatchEntry/rows-proposal.md`
- `.ufo/waves/round-51/w1/ScrDispatchEntry/counter-fit-receipt.txt`
- `.ufo/waves/round-51/w1/ScrDispatchEntry/fetch/Hyprland-SharedDefs.hpp`
- `.ufo/waves/round-51/w1/ScrDispatchEntry.md`

Report: .ufo/waves/round-51/w1/ScrDispatchEntry.md

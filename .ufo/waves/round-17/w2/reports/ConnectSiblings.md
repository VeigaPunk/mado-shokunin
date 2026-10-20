# ConnectSiblings — adjacency: who issued `man-pages` inside the C3 join window

Seat: `MadoR17.ConnectSiblings` (connector). Lane root: `mado-shokunin`.
Method: read-only file bytes and read-only transcript reads; no package
query, no package/service/compositor operation, no git/jj mutation, no
delegation. Installs this seat: **none**.

## 1. Question and answer

The task states `/var/log/pacman.log` lines 2414-2421 and asks which lane
issued `pacman -S --needed --noconfirm man-pages` at
`2026-10-20T01:07:12-0300`. Exact lines: **2416** (`[PACMAN] Running …`)
and **2419** (`[ALPM] installed man-pages (6.19-1)`); the 2414-2421 statement
is an area, not the exact pair.

**Answer: mori-shokunin, round 13, seat `MoriR13.PipeSource`.** Not mado.
Not tsukuroi.

Proof is positive, not an absence argument:

| Anchor | Observation |
|---|---|
| `MoriR13/MoriR13.PipeSource.jsonl:28` | assistant bash toolCall `call_160115`, timestamp `2026-10-20T04:07:12.168Z`, args `{"i": "Install man-pages package", "command": "sudo pacman -S --needed --noconfirm man-pages"}` |
| same file `:29` | `tool_execution_start`, same call id, same command, same `04:07:12.168Z` |
| same file `:30` | toolResult `04:07:12.454Z`: `core/man-pages 6.19-1`, `installing man-pages…`, post-transaction hook — success, no error |
| `04:07:12Z` | equals `2026-10-20T01:07:12-0300`, the `[PACMAN] Running` second in pacman.log |
| `call_160115` | occurs in exactly one transcript under the session dir (3 lines, all in `MoriR13.PipeSource.jsonl`); the intent string `Install man-pages package` likewise |
| `mori-shokunin/.ufo/waves/round-13/build/PipeSource.md:13-17` (mtime 01:09) | “Tool installed: `core/man-pages`; Version: `6.19-1`; Channel: `sudo pacman -S --needed --noconfirm man-pages`; Reason: … pipe(7) (`S031`) …” |
| `mori-shokunin/corpus/lessons/round-13.md:66` | “Tooling: PipeSource installed `core/man-pages` version `6.19-1` … No full-system or partial upgrade is claimed.” |
| `mori-shokunin/LOG.md:756` | same install restated in the round-13 log |
| `mori-shokunin/.ufo/waves/round-14/build/ProtectedInventory.md:30` | R14 attributes it to “`round-13.md:66` (PipeSource install of `man-pages 6.19-1`)”; the R14 transcript hits are reads of that record, not a second run |

Transaction count in the log: `grep -c 'installed man-pages'` → **1**; one
`Running` line, one `installed` line. No repeat anywhere in 3,160 lines.

Lane timing, from transcript first/last timestamps: `MoriR13` spans
`04:05:00.417Z → 04:50:19.454Z`; `MadoR13` spans
`04:04:30.583Z → 04:58:46.169Z` — the sibling rounds ran **concurrently in
the same shared OMP session**. `MoriR14` spans `05:52:42 → 06:58:51Z`.

### Not tsukuroi

tsukuroi owns the **full-system** update-safety gate (`pacman -Syu`), not
single-package installs. The operator tooling directive permits any agent to
run `pacman -S --needed --noconfirm <pkg>` without asking, and routes only
full-system upgrades through tsukuroi. mori's own R14 record of the directive
says exactly that (`ProtectedInventory.md:30`: “full-system upgrade
(`pacman -Syu`) requires `tsukuroi` gate”). tsukuroi's own round-15 statement
is “This lane performs no package/service action regardless of plan output.”
So there is no tsukuroi handoff for this line; routing it there would move a
known-actor mutation to a lane that disclaims package actions.

### Why the line is currently under-specified in the round-17 record

`.ufo/waves/round-17/evidence/tripwire-pacmanlog-join.txt:9` already carries
`# not mado: … man-pages … (sibling lane; reported, not absorbed)`. That is
correct but anonymous, and the record has two neighbouring categories that
could later swallow it:

- lesson `round-17.md:20` (M2) lists the four joined mado-window
  transactions as `2410, 2422, 2423, 2429` and **silently omits 2416**;
- lesson `round-17.md:18` (M5) names the post-launch transactions as
  “actor unknown, operator-owned”.

`2416` is neither: the actor is known (mori R13 PipeSource) and it sits
*inside* the printed window neighborhood, 22 s after mado's own
`wayland-utils` call (`MadoR13.GlobalCapture.jsonl:19`, `04:06:49.766Z`,
`pacman.log:2410`). pacman.log carries no actor field, so a time-window
join would fuse the two; the receipt is only correct because it joins
**per tool call**, and this call exists in a sibling transcript outside the
four `MadoR13..R16` trees that `evidence/session-index.json` indexes.

Window reproduction (grep, file bytes only):
`grep -nE '^\[2026-10-(19T2|20T0[0-6])' /var/log/pacman.log | grep -F '[PACMAN] Running'`
returns **7** lines: 2398, 2404, 2410, 2416, 2422, 2423, 2429. The receipt
accounts for 4 joined + 2 pre-R13 (2398, 2404) + 1 sibling (2416, named only
as “sibling lane”).

## 2. Axes

| Axis | State in round-17 declaration | Effect of this move |
|---|---|---|
| adjacency | declared **unscored** (“depth/adjacency unscored”) | improved — this is the axis's own signal: evidence belonging to another domain named and reported, not absorbed |
| calibration | C1, literal 14/22 → 15/23, fixed; rubric V is the post-correction lowest row | supported (actor named instead of “sibling lane”; no count change) |
| freshness | file-plane 29/29, harm watch | supported (ledger reconciled to live log bytes; no count change) |
| operability | hermetic 372/372 + classifier 52/52, harm watch | untouched — no code, no selftest, no receipt regeneration |
| coverage | rubric V 2/6 → 4/6 (lowest), U 7/7 | untouched |
| depth | unscored | untouched |

No scored counting command changes. The move is record-level, append-only,
and lands on the unscored adjacency axis plus the honesty of two scored
ledgers.

## 3. Proposed move (one bounded proposal)

Append the paragraph below, verbatim, as one bullet under
`SCORECARD.md` → “### Round-17 pre-measurement corrections (append-only; …)”,
after the “Host pause” bullet. Do **not** edit the join receipt's bytes and
do **not** add a QUALITY criterion (both would harm a landed count; see §4).

> **Sibling-lane install inside the printed C3 join window (append; reported,
> not absorbed).** `/var/log/pacman.log:2416` (`2026-10-20T01:07:12-0300` =
> `04:07:12Z`) records `pacman -S --needed --noconfirm man-pages` and `:2419`
> records `installed man-pages (6.19-1)`, exactly once each. The issuer is
> **mori-shokunin round 13, seat `MoriR13.PipeSource`**, not mado and not
> tsukuroi: its transcript `MoriR13/MoriR13.PipeSource.jsonl:28` carries bash
> toolCall `call_160115` (`sudo pacman -S --needed --noconfirm man-pages`) at
> `04:07:12.168Z`, the same second as the log line, with a successful result
> at `:30`; the seat's record
> `mori-shokunin/.ufo/waves/round-13/build/PipeSource.md:13-17` declares the
> install (`core/man-pages`, `6.19-1`, same channel, reason `pipe(7)` for
> `S031`), restated at `mori-shokunin/corpus/lessons/round-13.md:66` and
> `mori-shokunin/LOG.md:756`; the `MoriR14` mentions are self-quotation of
> that record (`mori-shokunin/.ufo/waves/round-14/build/ProtectedInventory.md:30`),
> not a second transaction. It is a **new package**, not an upgrade, so it is
> neither an R15-V1-class partial upgrade nor a tsukuroi `-Syu` gate matter
> (tsukuroi round 15: “This lane performs no package/service action”); the
> single-package channel is the operator directive's own allowance. The line
> sits 22 s after mado's `wayland-utils` call (`MadoR13.GlobalCapture.jsonl:19`,
> `04:06:49.766Z`, `pacman.log:2410`) in the same shared OMP session, so it
> must not be joined by time window — the join is per tool call, and this call
> exists only in the sibling transcript. It is excluded from C3's 4/4 mado
> count and from M5's “actor unknown” non-lane set; no counting command
> changes.

Optionally add one line to lesson `round-17.md` M2's fix cell: “2416 is the
mori R13 PipeSource install, named and excluded — see SCORECARD correction.”
Both edits are append-only prose; neither touches a receipt, a script, or a
claim count.

## 4. Risks / harm analysis

1. **Absorption into C3.** If the line were counted as a fifth joined
   transaction or as a tripwire finding, C3's “4/4” becomes “5/5” after the
   fact and calibration is harmed. The paragraph excludes it by name and
   keeps the denominator at 4.
2. **Frozen-receipt edit.** `tripwire-pacmanlog-join.txt` is committed
   command output at `988b858`; rewriting line 9 would change evidence bytes
   without a new measurement. Append in SCORECARD instead; if L1 regenerates
   the receipt, keep the command identical and state all 7 window lines.
3. **Criterion inflation.** A QUALITY criterion (“name the actor for every
   excluded line”) would move C1's denominator from 23 and break the declared
   15/23 target mid-round. Do not add one.
4. **Attribution-by-time.** 2410 (mado) and 2416 (mori) are 22 s apart in one
   session; any minute-resolution join would absorb the sibling call. The
   per-call join is the load-bearing property — the note says so.
5. **misrouting to tsukuroi.** tsukuroi gates `-Syu` only and disclaims
   package actions; naming it owner would send a known-actor mutation to the
   wrong lane.
6. **Overreach in the other direction.** The note must not say mori violated
   the round-17 host pause: mado's pause binds mado's lanes, and this install
   is 9 h 44 min before mado's round-17 launch (`10:51` BRT, lesson
   `round-17.md` M5; `01:07` → `10:51`). The paragraph makes no conduct claim
   about mori.

## 5. Verification performed (read-only)

```text
grep -n 'man-pages' /var/log/pacman.log
  2416 [2026-10-20T01:07:12-0300] [PACMAN] Running 'pacman -S --needed --noconfirm man-pages'
  2419 [2026-10-20T01:07:12-0300] [ALPM] installed man-pages (6.19-1)
grep -c 'installed man-pages' /var/log/pacman.log   → 1
grep -nE '^\[2026-10-(19T2|20T0[0-6])' /var/log/pacman.log | grep -F '[PACMAN] Running'
  → 7 lines: 2398 2404 2410 2416 2422 2423 2429
nl -ba mori-shokunin/.ufo/waves/round-13/build/PipeSource.md | sed -n '8,20p'
  → 13-17 tooling record (core/man-pages, 6.19-1, channel, reason)
nl -ba mori-shokunin/corpus/lessons/round-13.md | sed -n '60,72p'  → :66 tooling line
sed -n '25,33p' mori-shokunin/.ufo/waves/round-14/build/ProtectedInventory.md → :30 attribution
python3 (read-only) MoriR13/MoriR13.PipeSource.jsonl
  → :28 toolCall call_160115 2026-10-20T04:07:12.168Z sudo pacman -S --needed --noconfirm man-pages
  → :30 result 04:07:12.454Z, core/man-pages 6.19-1, installing man-pages, hooks, no error
grep -rl 'call_160115' <session dir>   → only MoriR13/MoriR13.PipeSource.jsonl (3 lines)
grep -rl 'Install man-pages package' <session dir> → only that file
python3 (read-only) MoriR13.jsonl / MoriR14.jsonl / session-index.json
  → MoriR13 04:05:00.417Z→04:50:19.454Z; MoriR14 05:52:42.192Z→06:58:51.737Z;
    MadoR13 04:04:30.583Z→04:58:46.169Z (concurrent)
MadoR13/MadoR13.GlobalCapture.jsonl:19 → call_2a68aff4b6984128b91f75d2
  2026-10-20T04:06:49.766Z sudo pacman -S --needed --noconfirm wayland-utils
```

No package command, service call, compositor/input probe, git mutation, or
delegation was executed. The only writes are this report file.

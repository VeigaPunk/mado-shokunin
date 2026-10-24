# ReviewUsedByClosure — used-by closure, both directions (round-32 w1)

Seat: review, leaf. Date: 2026-10-24. Package: `/home/vgpnk/Projects/shokuknow/merge/mado/` (read-only; nothing under it was modified).

## Inputs, and the L1-draft question

- Staged registry: `SOURCES.append.md` — 132 rows parsed (`^\| S\d+ \|`), ids S186–S317, statuses 131 `mined` + 1 `queued` (S203). Matches MERGE-REPORT.md ("132 accepted, 0 refused, first staged id S186").
- Staged entries: `knowledge/corpus/knowledge/` — 61 files parsed.
- Lane registry: `corpus/SOURCES.md` — 185 rows, S001–S185, no overlap with the staged id range.
- **The L1's drafts do not exist.** `.ufo/waves/round-32/scratch/` holds only scout fetch material (`ScoutIPCWiki0560/`, `ScoutIPCWikiCurrent/`, `ScoutDispatchersWiki/`, `ScoutDispatchers0560/`, `ScoutIPCEventMgr/`) and the `ExecCensusManual/` census outputs; no draft entry markdown and no draft SOURCES rows. `.ufo/waves/round-32/fetch/S186.bin…S196.bin` are raw source fetches, not drafts. **All verdicts below are from the staged package alone.**

## Method

Re-ran at write time (Python, this session): rows split on unescaped pipes only (`(?<!\\)\|`) — 21 rows (S221, S230, S231, S250, S300–S317) carry `\|` inside a recheck cell and are 11 logical cells each; a naive split misreads their `used-by`. All 132 rows have exactly 11 logical cells after escape-aware splitting. Forward: every `source:` id of all 61 staged entries must exist as a row whose `used-by` names that entry. Reverse: every row's `used-by` path must exist under the package and mention the row id. An earlier pass with a naive splitter produced 21 false "violations" on the `\|` rows; the numbers below are from the escape-aware run.

## The three admitted entries

The five appended rows are admitted by exactly three entries (no other staged entry carries one of these ids in a `source:` line):

| entry (staged path under `knowledge/corpus/knowledge/`) | `source:` ids |
|---|---|
| `ipc-contract-r25.md` | S186, S187, S189 |
| `dispatcher-semantics-r25.md` | S188 |
| `dispatcher-surface-and-request-grammar-r26.md` | S196 |

Exactly five staged rows name these three entries in `used-by` (grep over `SOURCES.append.md`: lines 7, 8, 9, 10, 17; no other hits) — the closure set is closed on both ends.

## Per-row verdicts (five appended rows)

| row | status | staged `used-by` (exact string) | entry that actually cites it | forward | reverse | path match |
|---|---|---|---|---|---|---|
| S186 | `mined` | `corpus/knowledge/ipc-contract-r25.md` | `ipc-contract-r25.md`, `source: S186` (line 10) | OK | OK | match |
| S187 | `mined` | `corpus/knowledge/ipc-contract-r25.md` | `ipc-contract-r25.md`, `source: S187` (line 11) | OK | OK | match |
| S188 | `mined` | `corpus/knowledge/dispatcher-semantics-r25.md` | `dispatcher-semantics-r25.md`, `source: S188` (line 8) | OK | OK | match |
| S189 | `mined` | `corpus/knowledge/ipc-contract-r25.md` | `ipc-contract-r25.md`, `source: S189` (line 12) | OK | OK | match |
| S196 | `mined` | `corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md` | `dispatcher-surface-and-request-grammar-r26.md`, `source: S196` (line 8) | OK | OK | match |

**Path-difference answer: no.** Every `used-by` names the same basename as the staged file that cites the row. The package nests the entries one level deeper (`knowledge/corpus/knowledge/…`) — that prefix is the staging root, consumed by adopt-checklist step 4 ("copy each `knowledge/<path>` into `corpus/knowledge/<path>`"); lane-relative strings are identical. Zero path mismatches on the five rows.

## Package-wide sweep (both directions, all 132 rows × 61 entries)

- Forward: **0 violations.** Every `source:` id in every staged entry is S186+ and has a staged row whose `used-by` names the citing entry. No staged entry puts a pre-S186 (lane) id on a `source:` line.
- Reverse: **1 finding** — S203 (below). All other `used-by` cells resolve to an existing staged file that mentions the row id.

## MERGE-REPORT.md correction table (8 rows) vs the five appended rows

**Intersection with {S186, S187, S188, S189, S196} is empty — none of the five was corrected at packaging.** Staged `used-by` strings for the eight, all matching the report's "now" column verbatim, and all reverse-verified (target exists, cites the row):

- S243 → `corpus/knowledge/chinese-wiki-revision-list-r7.md`
- S244 → `corpus/knowledge/chinese-wiki-ipc-section-r7.md`
- S251 → `corpus/knowledge/host-idle-lock-chain-r7.md, corpus/knowledge/uwsm-app-daemon-unit-r7.md`
- S258 → `corpus/knowledge/focus-grab-seat-semantics-r8.md, corpus/knowledge/gkeep-geometry-unobservable-r8.md`
- S259 → `corpus/knowledge/request-socket-live-bound-r8.md, corpus/knowledge/cn-framing-coverage-r8.md`
- S260 → `corpus/knowledge/request-socket-live-bound-r8.md, corpus/knowledge/cn-framing-coverage-r8.md`
- S276 → `corpus/knowledge/gkeep-rendered-geometry-chain-r9.md, corpus/knowledge/focus-grab-observed-semantics-r9.md`
- S293 → `corpus/knowledge/gkeep-size-to-real-size-r11.md, corpus/knowledge/gkeep-observation-route-r11.md`

## Mismatches found

**M1 — MERGE-REPORT ↔ staged file diverge on S203's `used-by`.** The report's "Rows no entry rests on" table states: "`S203` | corpus/knowledge/idle-lock-runtime-state-r28.md" ("These rows name a target entry in `used-by`"). The staged row (append line 24) carries `used-by` = `—` and status `queued`. The entry `idle-lock-runtime-state-r28.md` exists in the package and does **not** mention S203 anywhere. So the remedial action the report prescribed ("either write the entry or drop the pointer") was applied to the file but the report still describes the pointer as present. Report text is stale relative to the package; the package state itself is closure-clean.

**M2 — stale wave-draft row ids survive in three wave-2/3 entries' prose and merge notes.** The staged registry is the packaged id space; these inline pointers do not resolve to the row the sentence describes:

1. `dispatcher-surface-and-request-grammar-r26.md` (~line 22): "the same family the current-git page documents **(wave-1 row S186)**. Its dispatcher list includes (S196):" — the current-git **dispatchers** page is **S188**; staged S186 is the IPC `_index.md` page, which documents no dispatcher API. Should read S188.
2. `event-delivery-limits-r26.md` merge note (lines 12–16): "add wave-1 rows **S187 (the compositor's event manager)** and **S188 (Waybar's IPC backend)** to this entry's source list" — staged S187 is the 0.56.0 IPC wiki page and S188 is the dispatchers page; the event-manager row is **S189** and the Waybar IPC-backend row is **S190**.
3. `event-delivery-limits-r26.md` §1/§2: "the host's v0.56.2 event manager **(wave-1 row S187**, `src/managers/EventManager.cpp`)" (line 23–24), "removed, not throttled **(S187)**" (line 29), "**(S187, `flushClient`)**" (line 35), "**(S187, `postEvent`)**" (line 39), "the compositor's own 1024-character truncation of event data **(wave-1 rows S187 and S188)**" (line 52) — every one of these cites EventManager.cpp/Waybar-backend content; the ids should be **S189** (and S189+S190 on line 52).
4. `event-queue-host-measurement-r28.md` merge note (lines 13–16): "add **wave-2 row S187 (the compositor's event manager, where the markers are emitted)** to this entry's source list" — should be **S189**. (Its "wave 2 and wave 3" label also contradicts event-delivery's "wave 1 and wave 2" for the same rows.)

[INFERENCE] These are packaging-time renumbering residue: the wave-1 draft ids map onto staged ids by a constant +2 shift for ids ≥ draft-S187 (draft S186→staged S188, draft S187→staged S189, draft S188→staged S190), consistent with two rows (staged S187, S196) inserted ahead of them. The wave-1 entries and all registry rows carry the final ids; only these prose/merge-note pointers were missed. Note the closure risk they create: event-delivery-limits-r26.md's source list is deferred to a merge note, so if a merger follows the note literally, S189/S190 get cited under wrong ids and S187/S188 gain a second citing entry their `used-by` does not name.

**M3 — adoption-time `used-by` debts on lane rows (informational).** Five pre-S186 rows are cited inline by staged entries without being on a `source:` line; their lane-registry `used-by` cannot name staged paths yet and must be extended at adoption or reverse closure breaks: S018, S158 (cited by `ipc-contract-r25.md` §5 and `dispatcher-surface-and-request-grammar-r26.md` §2), S053, S054 (`waybar-module-text-route-r25.md`, `host-bar-and-idle-binding-r26.md`), S184 (`hyprctl-flags-r28.md`).

**M4 — inline-only mentions of staged rows not mirrored in `used-by` (observation, not a verdict failure).** The scoped rules bind `source:` lines, and the corrected-rows precedent shows packaging adds a path when an entry really cites a row; these single-path rows also carry inline mentions from other entries: S190 (`two-literature-drift-r26.md`), S193 (`chinese-wiki-canonical-url-r28.md`), S199 (`focus-control-surfaces-r28.md`), S214 (`update-check-and-app-lifecycle-r31.md`), S216 and S219 (`glyph-and-geometry-r31.md`), S281 (`gkeep-size-to-real-size-r11.md`). Harmless today; becomes a reverse-closure gap if anyone later treats "inline mention" as "cites".

## Verdicts

- Five appended rows S186/S187/S188/S189/S196: **closure holds in both directions**; statuses `mined`; staged `used-by` strings equal the citing files; no path difference; none touched by the correction table.
- Three admitted entries: **forward-clean** (all `source:` ids resolve to rows that name them back); no entry cites an id without a row.
- Package-wide: forward 0 violations; reverse clean except S203's report-vs-file wording (M1) and the prose-level id residue (M2), neither of which breaks the staged row↔entry pointer set as it stands.

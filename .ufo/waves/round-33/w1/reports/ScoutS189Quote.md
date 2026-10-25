# ScoutS189Quote — S189 blob verification (round 33, w1)

## Hash

`.ufo/waves/round-32/fetch/S189.bin` re-opened from committed bytes (not refetched):

- sha256 `eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d` — **matches** the digest frozen in `.ufo/waves/round-33/c1/frozen.json` (`fetches.S189`) and the digest in `corpus/SOURCES.md:201` and `corpus/lessons/round-32.md:29`.
- `file`: C source, ASCII text — 192 lines, 6,479 B. Confirms it is `src/managers/EventManager.cpp` @ commit `efb50993780079460b0cbed1363e2166a2de1d9f` (v0.56.2).

## Line locations

Inside `CEventManager::postEvent` (S189:163-192):

- **S189:169** — `const size_t MAX_QUEUED_EVENTS = 64;`
- **S189:175** — `Log::logger->log(Log::ERR, "Socket2 fd {} overflowed event queue, removing", it->fd.get());`

Context: the guard at S189:174 (`if (QUEUESIZE >= MAX_QUEUED_EVENTS)`) removes the client via `removeClientByFD` (S189:176) when a client's event queue reaches 64.

## Is citing campaign S187 for EventManager.cpp wrong?

**Yes.** The lane's S189 row (`corpus/SOURCES.md:201`) is the only registered source for `src/managers/EventManager.cpp`; S187 (`corpus/SOURCES.md:199`) is the Hyprland IPC **wiki page** (`https://wiki.hypr.land/0.56.0/IPC/`). Verified directly: `.ufo/waves/round-32/fetch/S187.bin` is a 268,731 B HTML document and contains **zero** occurrences of `MAX_QUEUED_EVENTS` or `EventManager.cpp` (`grep -c` → 0). The queue-cap claim is compositor-implementation behavior present only in the S189 blob.

Mechanical consequence under PRED-C1-r33-v1: a `gate-quote: S187 const size_t MAX_QUEUED_EVENTS = 64;` line can never close — the quote is not a contiguous substring of the S187 blob, and the frozen cite-map (`.ufo/waves/round-33/c1/frozen.json`) binds `corpus/knowledge/event-delivery-limits-r26.md` to `["S197","S189"]`, not S187. So an S187 citation would leave an open cite and also fail the substring test.

Current state check: every staged copy of the entry under `.ufo/waves/round-33/controls/` (golden, entries-only, hash-mismatch, extra-source, junk) already cites `S189` for the queue cap — no committed staged entry cites S187. The ScribeEntryStall prompt also instructs citing S189. The S187 attribution is therefore a hypothetical/wrong-variant citation, not a landed defect; if any wave-1 draft carries it, it must be corrected to S189 before append.

## Receipts

`.ufo/waves/round-33/scratch/ScoutS189Quote/receipts.txt` — command outputs for sha256, file type, line locations, S187 blob check, and the SOURCES.md S187/S189 rows.

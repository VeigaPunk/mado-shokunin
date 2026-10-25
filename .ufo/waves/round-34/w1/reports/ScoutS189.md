# ScoutS189 — S189.bin line verification

## Source
- File: `.ufo/waves/round-32/fetch/S189.bin` (read locally, not refetched)
- sha256: `eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d` — **confirmed**
- Byte length: `6479` — **confirmed**
- Total lines: 192

## Requested lines
- **Line 128**: `    auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));`
- **Line 169**: `    const size_t MAX_QUEUED_EVENTS = 64;`

## Pattern locations (1-based, via `grep -n`)
- `const size_t MAX_QUEUED_EVENTS = 64;` → **line 169**
- `overflowed event queue, removing` → **line 175**
  - Full line 175: `            Log::logger->log(Log::ERR, "Socket2 fd {} overflowed event queue, removing", it->fd.get());`

## Which line carries the queue-cap statement
**Line 169**, not line 128. Line 128 is the `std::format` call that builds `eventString` (`"{}>>{}\n"` with `event.event` and `data.substr(0, 1024)`).

## Artifacts
- `.ufo/waves/round-34/scratch/ScoutS189/lines.txt` — lines 128 and 169 with line numbers.

# CritC1DataSourcing — Gate-rule audit of `corpus/knowledge/waybar-module-text-route-r25.md`

Scope: did the lane open S201/S202 this round, and does the entry's Gate block satisfy
CORPUS.md Rule 1 (URL, access date, ≤25-word quote with location, per new row)?

## Verdict

**PASS with two shape observations.** Every required field is present and verified
against fetched bytes. No missing field, no over-long quote, no digest mismatch.

## Field check (contract: `../CORPUS.md:112-115`)

| requirement | S201 | S202 |
|---|---|---|
| URL | ✓ `source:` line 7 (raw.githubusercontent.com/Alexays/Waybar/0.15.0/…/backend.cpp) | ✓ `source:` line 8 (…/window.cpp) |
| access date | ✓ `verified-at: 2026-10-24` (line 9) + "Opened 2026-10-24 by this lane" (line 3) | ✓ same shared fields |
| quote | ✓ `gate-quote:` line 12 — **8 words** (`$XDG_RUNTIME_DIR/hypr does not exist, falling back to /tmp/hypr`) | ✓ `gate-quote:` line 13 — **1 word** (`m_ipc.registerForIPC("activewindow", this);`) |
| location | ✓ `(S201 line 38)` line 18; SOURCES.md anchor `backend.cpp:38`; verified at fetched bytes line 38 | ✓ `(S202 line 27)` line 21; SOURCES.md anchor `window.cpp:27`; verified at fetched bytes line 27 |

Quotes re-derived from the bins, not trusted: `awk 'NR==38'` on S201.bin and
`awk 'NR==27'` on S202.bin return the quoted strings verbatim. Word counts counted
on the quote text itself: 8 and 1 — both ≤25.

## Fetch-artifact check

- `.ufo/waves/round-34/fetch/S201.bin` — regular file, 6,550 B,
  sha256 `799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e`.
  SOURCES.md:203 records `6550 B, sha256 prefix 799bf02f6d18ae04` — **match**.
- `.ufo/waves/round-34/fetch/S202.bin` — regular file, 8,324 B,
  sha256 `5df496eb3cfe5cae4506d7aa10c6bb54eb0a0b28d9489dcf19dd68ba570c9846`.
  SOURCES.md:204 records `8324 B, sha256 prefix 5df496eb3cfe5cae` — **match**.
- Non-author re-fetch already on file: `ScoutS201.md` (sha256 match, 6,550 B) and
  `ScoutS202.md` — satisfies Rule 1's "non-author verification re-opens a sample".

## Observations (not blocking)

1. **No `## Gate` heading and no per-quote inline location.** Prior entries
   (`ipc-contract-r25.md:15-29`) use a `## Gate` section with `Quote (:N)` —
   location bound to the quote token. This entry uses flat `gate-quote:` fields
   whose location lives two paragraphs away in the OBS text. The contract needs
   "a quote with its location" — the location is in the file and correct, but the
   binding is looser than the lane's own r25 convention.
2. **Gate block omits sha256/byte-size.** Prior `## Gate` blocks record them per
   source; here they exist only in the SOURCES.md anchor. Convention, not contract.
3. `corpus/lessons/round-34.md` does not exist — Rule 1's literal surface is the
   "round lesson's `## Gate`". The knowledge entry carries the gate data instead,
   consistent with the r25 entries; flagged in case the lesson lands later in the wave.

## Commands run

```sh
stat -c '%F %s %n' .ufo/waves/round-34/fetch/S20{1,2}.bin
sha256sum .ufo/waves/round-34/fetch/S20{1,2}.bin
awk 'NR==38' .ufo/waves/round-34/fetch/S201.bin   # → spdlog::warn("...falling back to /tmp/hypr");
awk 'NR==27' .ufo/waves/round-34/fetch/S202.bin   # → m_ipc.registerForIPC("activewindow", this);
```

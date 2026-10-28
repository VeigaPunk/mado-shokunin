# R55W2RevRows — report (wave w2, falsify; item: registry rows S378-S380, used-by edits, gate quotes)

Full evidence: `.ufo/waves/round-55/w2/R55W2RevRows/rows-audit.md` (commands, outputs, receipts in `receipts/`).

## What ran
- Re-fetched the three upstream files at `efb50993780079460b0cbed1363e2166a2de1d9f` with curl (raw.githubusercontent.com); sha256 equal to the row values and to the pins; pins equal the freeze-commit blobs.
- `git ls-remote --tags` for `refs/tags/v0.56.2` → `efb50993…`, tag claim holds (network read, read-only).
- Printed every cited line range from the pins; checked the 11-column count with `awk -F'|'` (NF=13 for each row); ran the CORPUS.md § SOURCES census commands from the lane root (317 rows, 0 malformed, 0 duplicate ids, no enum violations, no missing used-by paths).
- Diffed SOURCES.md against the pre-round-55 parent `ebd66fbf^` row by row: only `used-by` changed (S052, S316, S317, S318, S319), each by an appended existing path.
- Parsed `gate.md`: URL, access date, teaches equal to rows; each quote located at its named pin line and occurs exactly once in its pin file; word counts 2 / 14 / 3.
- No mutation test; no lane file edited; no git mutation; no installs. Scratch removed.

## Verdicts
- S378 row — **SURVIVES** (sha, lines, teaches, scope hold; cited range 175-178 truncates the function that ends at 180, claim intact).
- S379 row — **BROKEN in scope cell**: scope says "keyboard-capability gate before the wl_keyboard repeat event". `Hyprland-protocols-core-Seat.cpp:350` calls `repeatInfo` directly from the `CWLKeyboardResource` constructor, reached via `get_keyboard` (`:467-468`) with no capability check; the capability gate exists only on the `updateRepeatInfo` path (`:604`). Teaches still SURVIVES as necessary conditions (shared guard `:442`). Row anchor does not cite `:337-350`.
- S380 row — **BROKEN in teaches wording**: "each keyboard header declares …" generalises over headers never opened; only `IKeyboard.hpp` (base class) was opened. Lines 121-123 themselves SURVIVE.
- used-by edits S052/S316-S319 — **SURVIVES** (append-only, existing paths, status/recheck unchanged).
- Registry census and CORPUS.md field rules (opened ISO, recheck cadence, kind, tier, status/used-by consistency) — **SURVIVES**.
- Gate quotes (S378 `:177`, S379 `:442`, S380 `:121`) and gate URL/date/teaches — **SURVIVES**.
- Gate in the round lesson — **UNVERIFIED / PENDING**: `corpus/lessons/round-55.md` does not exist in the lane; the gate is still a draft for L1.
- Freeze-commit hash claim and v0.56.2 tag claim — **SURVIVES**.
- Search-log "S380 URL held by S363" — URL overlap **SURVIVES**; the "W04" census label **UNVERIFIED** (no tool located).

## Not verified
- Initial `m_lastRate`/`m_lastDelayMs` values (`Seat.hpp` not pinned), so first-send behaviour on the bind path is unknown.
- Other keyboard headers at efb5099 (S380 "each").
- Frozen-predicate impact of the S379 scope overclaim (outside this item).

## Corrections proposed to L1 (not applied)
S379 scope + anchor (`:337-350`); S380 teaches → "the keyboard base header `IKeyboard.hpp`"; S378/S379 anchors to full function ranges (`:175-180`, `:603-610`); integrate the Gate into `corpus/lessons/round-55.md`. Append-only rule applies to any change: new row with `supersedes` or a same-round scope fix decided by L1.

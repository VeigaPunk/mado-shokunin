# PtrWalkerLiveSurface — R18-V3 freshness pointer appended to walker-live-surface.md (append-only, prefix verified)

## Scope

Target: `corpus/knowledge/walker-live-surface.md` (sole writer this wave). Assignment: find every line containing `2.17.0`, append one dated pointer block at the end, change no existing byte.

## Findings

- Pre-edit state: 301 lines, 19203 bytes, sha256 `2bbb9609283f2d81cd1240d111068205766bfedb03f9245937d23b4bb143f8eb`. The file had no trailing newline after line 301.
- `grep -n "2\.17\.0"` before the edit returned exactly three lines: 19 (claim), 37 (binary row: owner pkg `walker 2.17.0-1`, sha `64826a85…`), 38 (version row: `2.17.0\n` bytes). These are the lines listed in the pointer.
- Post-edit state: 308 lines, 20413 bytes, sha256 `3e27d415aa6ee85a3679794c87771f49488feca8393278a43f9e47ba2342a6f1`.
- Prefix check: `head -c 19203` of the new file has sha256 `2bbb9609…`, identical to the pre-edit hash. The new file's byte 19203 is the newline that terminates the former last line; no pre-existing byte changed.
- Appended block (lines 303–308): heading `## Freshness pointer (round 19, 2026-10-20)`, then four bullets:
  - Line 305 (first bullet) contains `2.17.2` and `S090` on the same line. It names the pins by line list (19, 37, 38), dates them to the note's own measurement window (2026-10-14, line 6), and routes to `corpus/knowledge/walker-route-r18.md`.
  - Line 306: version-bound claims (binary sha `64826a85…`, owner pkg, version bytes, 29-entry package list, packaged config 13,220 B / sha `5b4e47b7…`, help text sha `ca4820a8…`, L0 equality at offset 784,064).
  - Line 307: version-independent in kind but host-state dated 2026-10-14 (user config 1,336 B / sha `fecf71fa…`, GSettings, unit environment, PIDs/sockets/D-Bus/layer state, boundary snapshot). None re-asserted for 2026-10-20.
  - Line 308: 2.17.2 binary behaviour stays [UNK] (host pause).
- Deviation from the template, deliberate: the template wording says the binary's compiled-in version literal was "read as file bytes (S096)". No such read happened this round, and `grep -n "S096" corpus/SOURCES.md` returns no row (S096 is reserved only). The block therefore says the host binary bytes are "reserved as S096 (row pending, not re-read this round)".
- The block's own lines 305–306 contain `2.17.0` text (they describe the pins). This is expected and does not affect the 19/37/38 pin list.
- Cross-check (read-only): `walker-route-r18.md` line 224 records `HP:2929` (`upgraded walker (2.17.0-1 -> 2.17.2-1)`) and line 225 records the tag `v2.17.2` carrying `version = "2.17.2"`. This is consistent with the pointer; no fact was taken from it beyond the routing target.
- `corpus/SOURCES.md` row S090 (line 102) exists and is the citation used.

## Evidence

- `sha256sum corpus/knowledge/walker-live-surface.md` (before): `2bbb9609283f2d81cd1240d111068205766bfedb03f9245937d23b4bb143f8eb`, 19203 B.
- `head -c 19203 corpus/knowledge/walker-live-surface.md | sha256sum` (after): `2bbb9609283f2d81cd1240d111068205766bfedb03f9245937d23b4bb143f8eb`, match.
- `sha256sum corpus/knowledge/walker-live-surface.md` (after): `3e27d415aa6ee85a3679794c87771f49488feca8393278a43f9e47ba2342a6f1`, 20413 B.
- `grep -n "2\.17\.0"` (after): lines 19, 37, 38 (unchanged), 305, 306 (new block).

## Limits

- Did not re-read `/usr/bin/walker` or `/var/log/pacman.log`; S090 and S096 were not re-verified this round. Host reads were not needed for the pointer text, and the host is paused for pacman.
- Did not re-measure any live walker state (sockets, PIDs, D-Bus, GSettings, config files); the pointer dates those values and does not re-assert them.
- The prefix check is a sha256 comparison of the first 19203 bytes against the recorded pre-edit hash. The earlier shell `cmp` attempt compared against a command-substituted copy and is not relied on.
- Other L1-owned files (`corpus/SOURCES.md`, `corpus/README.md`, lessons, SCORECARD, LOG) were not touched.
- Process note: one mistaken `PUT 1*` edit on this report replaced the whole report body with its heading line; the file was then rewritten in full with this content. No other file was affected by that mistake.

## Installs

none

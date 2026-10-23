# ScribeBindNote

## Behavior

Drafted `corpus/knowledge/bind-table-r25.md` with sourced notes on the hyprlang parse model, source traversal, variables and comments, bind suffix flags and grammar, modifiers, keycodes, mouse binds, rejected declarations, unbind, the 18 JSON fields, the v4 nested-instance readback, and the exec-created-bind oracle boundary.

Quote audit: all 58 quoted snippets in the draft were checked after whitespace collapse against the pinned source bytes; all were exact substrings and each quote was at most 25 words. The observed claims point to the named a3w1 reports, including `ScoutBindSurface.md`, `RevCounterV4.md`, `K4EmptyArray.md`, and `SentOracleBoundary.md`.

The S162 citations use the exact pinned `ConfigManager.cpp` bytes at the cited bind/source handler lines. The SOURCES row's recorded anchor ranges describe other ConfigManager behavior; the draft nevertheless identifies the exact byte locations and quotes rather than implying those ranges cover bind parsing.

## Gates and commands

- No shell command, C1 counter, build, test, compositor verb, or runtime probe was run; no tool score or verdict is claimed.
- Read targets: `corpus/SOURCES.md`; `fetch/S169.bin`, `fetch/S170.bin`, `fetch/S171.bin`, `fetch/S172.bin`, `fetch/a3w1/SrcHandleSource.bin`, `fetch/a3w1/WikiUsingHyprctl.bin`; `registration.md`; a3w1 `ScoutBindSurface.md`, `RevCounterV4.md`, `K4EmptyArray.md`, `SentOracleBoundary.md`; the `godspeed` skill; and the existing `keybind-rule-semantics.md` style sample.
- Exact regex searches: `corpus/SOURCES.md` with `^S(162|167|169|170|171|172)\b|\| S(162|167|169|170|171|172)\b`; `SrcHandleSource.bin` with `handleBind|handleUnbind|parseKey|addKeybind|parseDynamic|bindsRequest|handleSource|source`; a3w1 reports with `stringToModMask|substring test|case-insensitive|aliases|separators|MOD2|MOD3|modifier` and `submap_universal|modmask.*keycode|has_description.*dispatcher|FIELDS =`.
- Quote-check operation: JavaScript evaluation read the draft and six pinned source artifacts, used `s.replace(/\s+/g, ' ').trim()` for each string, extracted `“...”` snippets, and tested normalized substring membership and whitespace-separated word count; outcome `quoteCount=58`, `allLocated=true`, `allAtMost25=true`.
- No tooling was installed or updated.

## Touched surfaces and scope

Only the two assigned outputs were written:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/a3w2/drafts/bind-table-r25.md`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/a3w2/reports/ScribeBindNote.md`

No product code, SOURCES row, counter, report owned by another seat, or live compositor state was changed. The sentinel's exec/keyword example remains explicitly source-based and unexecuted, as its report states; the modifier discussion is scoped to the a3w1 source-walk observation and does not claim exhaustive alias/separator coverage.

## Artifacts

- Knowledge draft: `corpus/knowledge/bind-table-r25.md`
- This report: `.ufo/waves/round-25/a3w2/reports/ScribeBindNote.md`

BINDNOTE: 58/58 quotes verbatim; unsupported sentences: L7, L15, L17, L38, L40, L46, L52, L54, L66, L68

## Evidence

- Audited all 58 quoted spans (not a sample). Each is a whitespace-collapsed substring within its cited line range; the longest is 24 whitespace-separated words (limit 25).
- Checked the cited source rows S162, S167, S169, S170, S171, and S172 in `corpus/SOURCES.md`; all exist and are `mined`.
- Fresh-curl bytes for S162 matched its SOURCES SHA-256 (`9db68cf4…f65be62b`). Pinned bytes for S167/S169/S170/S171/S172 likewise matched their SOURCES SHA-256 values. The downloaded bytes were kept under `/fast/scratch/hyaku/mado-r25a3/res/RevBindNote/`.

## Medium — quote excerpts do not fully support these sentences

These are citation-support gaps, not findings that the omitted code is absent. The fetched S162/S169/S170/S171 source may support claims in adjacent, unquoted lines.

- `corpus/knowledge/bind-table-r25.md:7`: the excerpts establish the command/value line form and command behavior, but do not quote the variable-as-option or overwrite clauses (Hyprlang lines 18–21).
- `:15`: the S162 pin range ends at line 1839; the sentence says the including-file path is restored, which is line 1840 and is not quoted. The observation at ScoutBindSurface.md:19 says the current path is the file being parsed, but does not state the restore.
- `:17`: the quotes show the no-match text, regular-file predicate, and “skipping” log strings, but omit the `Log::ERR`/error return and the `continue` statements behind “reported as an error” and “are skipped.”
- `:38`: the excerpts show argument-count calculation and the description offset, not the `MOD, KEY, DISPATCHER, ARG` positions or `DEVICEARGS` field; the `d`/`k` layout claims are broader than the quoted fragments.
- `:40`: the observation and quotes support the mouse-dispatcher/action description, but no quoted fragment shows the one-fewer-field comparison (the comparison is at S162 lines 1561–1562).
- `:46`: the quoted `parseKey` fragments show the decimal/code/catchall tests, not the keycode/catch-all return values for those branches. Only the fallback-preserves-key result is quoted.
- `:52`: the too-few/too-many excerpts include `return`; the dispatcher/mod excerpts are only message substrings, the catchall excerpt is a log message, and the excerpts do not establish the stated rejection-before-add control flow. The omitted return paths precede `addKeybind` in S162.
- `:54`: the quote shows `m_keybinds.clear()` only, not the other clear/reset operations; the ordinary-unbind excerpt shows `removeKeybind(MOD, KEY)` but not how `MOD` and `KEY` are parsed.
- `:66`: S171's quote shows assignment of `configPath`, not `--config` parsing/validation. The S169 excerpts show the `-i` option spelling, instance-signature assignment, and socket pathname, but not signature-vs-index selection or the socket connection that routes the request.
- `:68`: the quote shows the no-backend condition, not the following `return false` at S170 line 151.

## Residual risk and verification gaps

No quote failed verbatim, stated-line, or word-limit checks, and no cited S-number was missing or non-mined. The listed sentences remain under-supported by their quoted excerpts; several are corroborated by adjacent source lines, but the entry should quote those lines or narrow the wording. Observation-only assertions were checked against their cited report lines where relevant, not independently rerun; no compositor or counter run was performed for this static citation audit.

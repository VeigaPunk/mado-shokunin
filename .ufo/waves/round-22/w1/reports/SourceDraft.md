# SourceDraft — round-22/w1

## Result
Created a curatorial instruction artifact for S121 and S122. It records no source claims and adds no source rows. The JSON gates future row curation on the owning seat returning both its report and artifacts, then a raw-byte digest, official tagged-source identity, exact URL/access date, and a located verbatim quotation of at most 25 words. It also makes unknowns explicit and limits these sources to C1 support, not detector completeness.

## Assigned scope and gates
- **S121 / SourceClosure:** official CPython v3.14.8 `Doc/reference/executionmodel.rst` and narrowly relevant language-reference material for lexical free variables/global lifetime. Curate only claims directly supported by located retained passages; do not generalize to detector behavior.
- **S122 / SourceThread:** official CPython v3.14.8 `Lib/threading.py`, limited to `Thread.run` and `Timer.run`. Keep direct worker-call semantics distinct from Timer wait/cancel behavior; do not assert the latter without direct returned evidence.
- For both IDs, wait for the named seat's report and artifacts; match artifacts to the exact assigned ID; preserve raw bytes; check the reported SHA-256; record exact upstream URL, access date, path/section, and quote locator; use no quote longer than 25 words. Hold rather than add a row on a missing or inconsistent requirement. Do not edit shared lesson, SOURCES, LOG, the registry, or another seat's artifacts.

## Findings and provenance
The round-22 registration distinguishes authorization from admission and limits source support to C1 rather than detector completeness. The source-seat task records in the wave run/assignment data supply the two IDs, official CPython v3.14.8 target scopes, raw-byte/provenance and short-quote requirements, and the Timer uncertainty distinction. These are assignment-derived instructions, not claims about the source contents.

At inspection, the source-seat agents were listed as running and the `w1/reports` directory listing contained only `swarm-registry.json`; no SourceClosure or SourceThread report was present in that listing. Source payload files were visible in the source-directory listing, but their contents were not opened or used to make claims. The draft therefore remains explicitly `awaiting_source_seat_returns`, with `source_claims: []` and `source_rows_added: []`.

## Work record
- **Commands:** no shell commands or external commands were run. No network access, installs, detector measurements, payload execution, builds, tests, linters, formatters, or smokes were performed.
- **Read-only inputs:** `skill://godspeed`; round-22 `registration.md` and `audit-contract.json`; `w1/notes/SimplifyCapture.json`; source-seat task records in `w1-run.json` and `w1-native-result.json`; `w1-record-success.json`; and the `w1` source/report directory listings. The task records were located with a read-only search for `S121|S122` under the round-22 wave.
- **Out of scope:** no source-byte inspection or validation, no source claims, no row creation, no shared-index/lesson/log/registry changes, and no production edits or admission judgment.

## Affected surfaces
- Created `.ufo/waves/round-22/w1/notes/SourceDraft.json` — curatorial instructions only; zero source rows.
- Created `.ufo/waves/round-22/w1/reports/SourceDraft.md` — this scoped report.
- No other files were intentionally changed.

## Artifact paths
- Instructions: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/notes/SourceDraft.json`
- Report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/reports/SourceDraft.md`

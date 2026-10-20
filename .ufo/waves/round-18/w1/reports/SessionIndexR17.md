# SessionIndexR17 — round-17 seat transcript index

Seat: MadoR18.SessionIndexR17 (round-18 wave 1). Read-only binder for a later tripwire
scan of round-17 seat conduct.

## Output

- `.ufo/waves/round-18/evidence/session-index-r17.json`
  - schema `mado-session-index-v1` (same shape as `.ufo/waves/round-17/evidence/session-index.json`)
  - sha256 `5983d41e5d0100f5e1a317c8ca851788a5dc8e8a67d6e56f45b148d576f1ba90`
  - 149 file entries: `MadoR17.jsonl` (root) + 148 `MadoR17/*.jsonl`
  - 101,445,124 bytes bound; 19,580 non-blank lines

## Source

Session root (read-only):
`/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07`

Root `MadoR17.jsonl` is present (2,811,777 bytes, 549 non-blank lines).

## Method

For each file, streaming file read only (`open(...,'rb')`, no writes, no omp CLI):

- `bytes` = raw byte length; `sha256` = SHA-256 of those bytes.
- `lines` = non-blank lines (blank lines skipped), matching the round-17 index convention.
- `first_timestamp` / `last_timestamp` = min/max over record fields `timestamp` or
  `updatedAt` (title records carry only `updatedAt`; `session`/`custom`/`message` carry
  `timestamp`).
- `tool_calls` = count of assistant `message` content items with `type:"toolCall"` grouped by
  `name`; tool-result records are not counted.

All entries have both timestamps non-null.

## Aggregate (index-derived, not re-measured)

| tool | calls |
|---|---|
| bash | 4694 |
| read | 851 |
| edit | 548 |
| eval | 299 |
| write | 272 |
| grep | 86 |
| glob | 21 |
| wait | 12 |
| web_search | 4 |

Earliest record `2026-10-20T13:51:52.097Z` (root session start); latest
`2026-10-20T15:24:56.844Z` (root tail). Every file has at least one tool call.
File size range 145,280–2,811,777 bytes.

## Verification performed

- Independent re-hash + byte + line-count check on 3 sampled entries (root, a mid child, the
  last child): all matched the recorded `bytes`, `lines`, `sha256`.
- `missing_ts` sweep over all 149 entries: empty.
- Spot read of a child transcript confirmed message schema (`role`, `content[]` with
  `type:"toolCall"`, `name`) used for counting.

## Risks / notes

- These are mutable host files; later mutation invalidates the hashes. The index is a binding
  at this instant, not a stable identity. A tripwire scan must re-hash and compare to this
  index, not re-derive silently.
- `web_search` appears in aggregate (4 calls) and is kept as a distinct name rather than
  folded into another bucket.
- No files were modified outside this index and this report. No tools installed; no network
  fetch performed; no lane git/jj command run.

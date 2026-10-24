# ScribeEntryIPC — re-grounded draft of `ipc-contract-r25`

**Draft (scratch only):** `.ufo/waves/round-32/scratch/ScribeEntryIPC/ipc-contract-r25.md`
**Staged input:** `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/ipc-contract-r25.md`
**Corpus untouched** — nothing written under `corpus/`; L1 integrates.

Shape: provenance trio first (three `source:` lines naming S186, S187, S189 with URL + anchor each) → `verified-at: 2026-10-24` → `recheck: 90d (ran 2026-10-24)`; staged section structure §1–§6 kept; explicit unknowns (§5) kept; every claim carries its S-id:line pin; `## Gate` block appended with URL + 2026-10-24 access date + ≤25-word located quote per source.

## Verification — this seat's own byte checks (2026-10-24)

- **S186** re-read first-hand from `scratch/ScoutIPCWikiCurrent/ipc_index.md` (6539 B, sha256 `535bc4c3…`): socket L14, grammar L19, sync/freeze + five-second-timeout sentence L22 (note L21-23), socket2 L25, framing L30, example L32, `## Events list` L34, 44 catalogue rows L38-81.
- **S187** own tbody extraction from `scratch/ScoutIPCWiki0560/IPC-0.56.0.html` (268731 B, sha256 `136e5511…`): 45 `<tr>` = 1 header + **44 names**; set-diff against the S186 names: **empty in both directions**. Page stamp `datetime="2026-05-02T03:38:58.000Z"` confirmed in bytes.
- **S189** own `grep -n` pins on `scratch/ScoutIPCEventMgr/EventManager.cpp` (6479 B, sha256 `eea605df…`): ctor L14, PATH L21, `// 10 max queued.` L34, `listen(…, 10)` L35, `formatEvent` L126, format + `substr(0, 1024)` L128, `std::replace` L129.
- **Tree check re-run:** GitHub contents API `src/ipc` @ `efb50993…` → **404** (negative claim holds).
- **Tag check (new):** `git ls-remote` → `refs/tags/v0.56.2` = `efb50993780079460b0cbed1363e2166a2de1d9f` (lightweight). Staged "(v0.56.2)" was asserted, now verified; draft states it as an OBS.
- **§6 recheck greps** re-ran against fetched bytes: `1` and `1` — expectations hold.

Sibling reports read: `ScoutIPCWikiCurrent.md`, `ScoutIPCWiki0560.md`, `ScoutIPCEventMgr.md` (the latter two landed mid-seat; their logs were read first). No disagreement with their findings.

## Staged claims dropped

1. §4: "The only textual difference in the extraction was the table's own `name` column header." — describes the staging extraction, not a source fact; the re-opened bytes support only "both catalogues carry the same 44 event names" (both table headers literally read `name | description | data`). Dropped; verifiable core kept as the §4 OBS.

No other staged claim dropped — everything else is byte-supported after re-pinning.

## Corrections carried into the draft

- **S186 line pins were uniformly stale**: grammar `:7-12` → **:19**; sync note `:15` → **:21-23** (freeze rule and five-second timeout both in :22); framing/example `:18-25` / `:25` → **:30** / **:32**; socket paths now pinned at **:14** / **:25**.
- **`// 10 max queued.`** now pinned at **S189:34** (staged grouped the quote under `:14, :35`).
- §1 freeze quote extended to the full sentence including "until the five-second timeout is reached" (staged truncated mid-sentence).
- §3 gains the tag-is-commit OBS (see above).

## Unknowns kept (§5, substance verbatim)

- No host observation: no socket connected, no event seen, binary not interrogated — the entry bounds the contract, not the host's behavior.
- Request-socket implementation side (`src/debug/HyprCtl.cpp`, S018/S158): queued, not done.

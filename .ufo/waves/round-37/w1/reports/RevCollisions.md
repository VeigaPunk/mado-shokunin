# RevCollisions — reviewer seat, mado round 37 wave 1

Verdict: **PASS — everything reproduces.** The collision check, the guard proof and the quarantine slice match `.ufo/waves/round-37/assimilation/` byte-for-byte. Every mapped row's URL and sha256 matches the fetched bytes and the lane or package row. Three non-blocking findings follow (F1–F3). One verification gap remains: the re-grounded entry is not in the lane yet, so its re-pointed citations could not be checked.

Scratch: `/dev/shm/mado37-RevCollisions/` only. No lane file, campaign file, compositor socket or VCS state was written. The only network use was four read-only `curl` GETs. No tools were installed.

Inputs at check time:

- Lane HEAD is `80b83c8`. `corpus/SOURCES.md` is identical to base `b4e47e9`: both hash to sha256 `aa400cd23b2879a3…2798ec`, and `git status` shows it clean.
- `merge/mado/SOURCES.append.md` hashes to sha256 `684efe8c23b8b64d…4a27c0`.
- `absent-defect-register.md` hashes to sha256 `5afe1810a6c3d62f…bad833`.

## 1. Id-collision check (round prompt §10, lines 427–433, run verbatim with `A=/dev/shm/mado37-RevCollisions`) — PASS

```
 201 reg-ids    147 staged-ids    9 collisions    13 quarantine-slice
IDENTICAL reg-ids
IDENTICAL staged-ids
IDENTICAL collisions
IDENTICAL quarantine-slice
cda3c367…8202 reg-ids  079d7538…925d staged-ids  dddee832…9344 collisions  d9ea803d…d45d quarantine-slice
```

- The comparison was made with `cmp` against the lane's assimilation files.
- The collisions are S203 through S211 (9 ids), the same as `renumber-map.md:6-7`.
- **Blind-spot probe — PASS.** Every `S\d{3}` token anywhere in `corpus/SOURCES.md`, minus `reg-ids`, is empty, so the pattern drops no registry id. There are also no rows indented with 4+ spaces or a tab.
- **Staged probe.** The staged file has two tokens outside the id column, S013 and S014. They sit inside the prose cells of staged rows S249 and S251 and are not row ids.
- **Parser parity — PASS.** The census parser only takes `^ {0,3}\|` rows and strips `^ {0,3}` (`scripts/sources-census.sh:40,615-616`). The extractor's pattern accepts exactly that set.

## 2. Guard proof — PASS

I reran the 0–3-space pattern and the column-zero pattern `^\|[[:space:]]*S[0-9]{3,}` on two fixtures.

On the lane's fixture (`assimilation/guard-proof/`):

```
lane: n03=1 [S002 ] ncol0=0
IDENTICAL guard-proof/collisions, collisions-col0, reg-ids, reg-ids-col0, staged-ids
```

On my own fixture (column-zero S010, three-space S011, four-space S012; staged S011, S012, S777):

```
own: n03=1 [S011 ] ncol0=0
```

The guard is live: the indented collision is caught and the column-zero pattern misses it. The 4-space S012 row is correctly not counted, because the census parser rejects it too.

## 3. Quarantine slice (§10, lines 467–471) — PASS

- The slice is byte-identical to the lane's copy (see section 1).
- The register has 14 `mado` lines: 13 data rows (lines 141–146 and 349–355) plus the summary row `| \`mado\` | 6 |` at line 248. The awk filter correctly excludes the summary row, so 13/13 data rows are captured.
- Register `round2 S201` is `https://arxiv.org/abs/2604.18860` (register line 143). This confirms the map's note that it is not the lane's S201.
- Register `round1 S189` points at the same EventManager.cpp URL at commit `efb50993…` as lane S189. Its quote is stored escaped (`std::format(\"{}>>{}\\n\"`).
- Line 128 of the fetched bytes reads `    auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));`. The map's "present, `:128`" verdict (`renumber-map.md:29-32`) is correct.

## 4. Renumber map, verified by document — PASS on every row

I re-fetched every URL into `/dev/shm/mado37-RevCollisions/refetch/` and compared it with `cmp` against `.ufo/waves/round-37/fetch/`:

```
eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d  S189.bin   6479
799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e  S201.bin   6550
1e19d92638e7923f0e72f6e65c83f579e32b41d588d166d6efef543c3f97d7e9  S212.bin  41392
d04e3a2fe5c73ad8684377856ce8301e493929ed9f391e405fde4975eaf6b868  S214.bin   1789
REFETCH==LANE S189 / S201 / S212 / S214
```

Map row by map row:

- **Lane S189 (held) — PASS.**
  - Lane row: `corpus/SOURCES.md:201`.
  - URL: `raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp`, the same URL I fetched.
  - The row records 6479 B and sha256 prefix `eea605dfe5ce09e1`, which match.
  - The bytes are identical to `.ufo/waves/round-32/fetch/S189.bin` (`cmp` silent, same sha).
- **Lane S201 (held) — PASS.**
  - Lane row: `corpus/SOURCES.md:203`.
  - URL: `raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/backend.cpp`.
  - The row records 6550 B and prefix `799bf02f6d18ae04`, which match.
  - The bytes are identical to `.ufo/waves/round-34/fetch/S201.bin`.
- **Package S214 becomes lane S212 (new) — PASS.**
  - Package row: `merge/mado/SOURCES.append.md:18`.
  - URL: `raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/workspaces.cpp`, the same URL I fetched.
  - The row records 41392 B and prefix `1e19d92638e7923f`, which match. The map's `1e19d926…97d7e9` also matches the full hash.
  - Campaign origin: `lanes/mado/round2/SOURCES-PROPOSED.md:37`, the same row.
- **Lane S214 (new, Logger.cpp) — PASS.**
  - The URL at `efb50993…/src/debug/log/Logger.cpp` refetches identically. The map's `d04e3a2f…f6b868` matches.
  - The cited anchors are present: `15:     if (!m_logsEnabled)`, `16:         return;`, `48:     m_logsEnabled = !*PDISABLELOGS;`.
- **The two held rows resolve by document, not by id.** The package entry's merge note (`event-delivery-limits-r26.md:12-13,24,52`) refers to "wave-1 S187/S188".
  - Campaign `lanes/mado/ID-REMAP.md` maps round1 `S200` to `S206` and `S201` to `S207`.
  - Staged S206 (`SOURCES.append.md:10`) has the same EventManager.cpp URL and prefix `eea605dfe5ce09e1` as lane S189.
  - Staged S207 (`:11`) has the same backend.cpp URL and prefix `799bf02f6d18ae04` as lane S201.
  - The map's resolution to S189 and S201 is therefore correct by URL and hash.
- **Lane S213 (own-work receipt) — PASS.** The receipt hashes to `1c1b0ce149ecd7b1d20b0a83f266197c89c9f5334d17dc035fe499d93272ce58`. The ScribeRows draft S213 row carries the same full hash.
- **Refusals of staged S226 and S242.** These are host artefacts, not URLs. They are outside the byte check and are not judged here.

## Findings (none blocking)

- **F1 — traceability (low).** The map labels the two held rows only by the merge note's "wave-1 S187/S188".
  - No campaign row carries those ids: `rg '^ {0,3}\| *S18[78] ' shokuknow/lanes/mado` returns nothing.
  - The lane's own S187 and S188 are different documents (`SOURCES.md:199` is the IPC wiki 0.56.0; `:200` is the Dispatchers wiki).
  - The map never names staged **S206/S207**, which are two of the nine collisions, so the collision list cannot be traced to its resolution.
  - Fix: add "staged S206 (campaign round1 S200)" and "staged S207 (round1 S201)" to the two held map rows.
- **F2 — stale-id hazard (medium, unverifiable yet).**
  - The lane's new ids S212, S213 and S214 equal three staged ids that name other documents: staged S212 is a zh-wiki archive, S213 is the Dispatchers 0.56.0 page, and S214 is workspaces.cpp (`SOURCES.append.md:16-18`).
  - The package entry cites `S214` three times (meaning workspaces.cpp) and `S187`/`S188` eight times.
  - An un-repointed `S214` in the re-grounded entry would silently cite Logger.cpp, and an un-repointed `S187`/`S188` would cite wiki pages.
  - `corpus/knowledge/event-delivery-limits-r26.md` does not exist in the lane yet (`ls`: No such file), so I could not check this.
  - Check to run before append: every `\bS\d{3}\b` in the admitted entry must resolve, by URL, to the document its sentence describes. Expect S212 for workspaces.cpp and S189/S201 for the event manager and IPC backend; S187, S188 and a workspaces-meaning S214 should be absent.
- **F3 — map completeness (low).**
  - The map has no sha256 for the S213 receipt. Its full hash appears only in `w1/reports/ScoutHostRederive.md:4` and the ScribeRows draft.
  - The map's "201 ids (S001…S211)" is the correct count, but the range hides real gaps: S190–S195 and S197–S200 are absent from the registry entirely. This is not a collision risk, since the any-token probe is empty.

## Residual risk and verification gaps

- The admitted entry and the final append block are not in the lane, so F2 remains open until they land.
- The `curl` refetch proves that today's bytes at each URL equal the lane's fetch. For the immutable commit and tag paths used here, that is the evidence the map needs.
- The guard proof covers spaces only. Tab-indented rows are rejected by both the census parser and the extractor, which is consistent.

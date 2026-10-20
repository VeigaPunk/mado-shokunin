# SourcesFrontierDraft — round-19 Gate skeleton drafted; S096–S098 and S084/S094 changes proposed, pending re-open

Draft: `.ufo/waves/round-19/drafts/SourcesFrontierDraft.md` (only file written besides this report). Not landed; L1 decides.

## Findings

1. **S098 is supportable from committed bytes.** `.ufo/waves/round-18/fetch/SrcWalkerConfigPaths/xdg-3.0.0.crate` re-hashes to `2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5` (15,821 B), equal to the crate checksum at `MadoR18.SrcWalkerThemes/cargo-lock.txt:2708` (walker v2.17.2 `Cargo.lock` raw, receipt 15:41:16Z, body sha `3448367c28c769e29f681ea2de84d4a822f08569bbef6628f03535c61fec2315`). Quote verified from the extracted member `xdg-3.0.0/src/base_directories.rs:447-448`: "Searches `XDG_CONFIG_HOME` and then `XDG_CONFIG_DIRS`." Defaults at `:217` and `:221`. This replaces the unpinned docs.rs alias (R18-V4) with a version-pinned archive the walker build actually uses.
2. **The docs.rs `latest` page is not a digest anchor.** Receipts: `ReopenS084` `0291cfe6…` (16:00:17Z, 16:00:36Z); `…/3.0.0/` `adaec7c3…` (16:01:30Z, 16:03:01Z, 16:06:30Z); `…/2.5.0/` `cb23df33…` (16:02:12Z). The 3.0.0 and latest bodies differ in nav chrome only (`.ufo/waves/round-18/w2/reports/ReopenS084.md:81-82`). Rejected as sole support under the round-18 HTML rule.
3. **S097 can replace S094's credited anchor, but it does not clear R18-V1's exit 1.** `ReopenS094/colors.toml` re-hashes to `dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786` (461 B); line 4 is `background = "#121212"`. The tree pages stay in the receipt set. `fetch-verify.py:386` emits CONFLICT per URL over all receipts, so exit 1 persists. Two receipts for `tree-theme` at the same URL and timestamp 16:00:00Z have different digests (`6b355a46…`, `3b18a612…`), which confirms M7 directly.
4. **S096 is a join, not a new fact.** `/usr/bin/walker` sha256 `25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096` equals S091's binary clause. `/var/log/pacman.log:2929` reads `[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)`. `grep -a -o '2\.17\.[0-9]' /usr/bin/walker` returns one match, `2.17.2`. S096 overlaps S090 (line 2929) and S091 (binary) on the same host paths; QUALITY 17 review needs an explicit "supersedes neither, joins both" statement, which the draft carries.
5. **Census baseline re-counted:** 95 rows; tier A 88, B 1, C 6; mined 80, queued 8, rejected 7 (`corpus/SOURCES.md`). Proposed landing: 98 rows, A 91, mined 82, rejected 8, queued 8 (if S084 → rejected).

## Proposed changes (old → new), all pending L1 decision

- S084: status `mined` → `rejected` (recommended) or unchanged; recheck `on-release` → `on-release` (unchanged); used-by `corpus/knowledge/walker-route-r18.md` → `—` once that note cites S098 (walker lane edit).
- S094: status `mined` → `mined`; recheck `on-release` → `on-release`; used-by `corpus/knowledge/theme-route-r18.md` → `corpus/knowledge/theme-route-r18.md; S097 (raw file)`.

## Gate and search-log state

- Gate candidates, admit/reject rules, GATE re-open lines for S096–S098 (quotes pre-filled, agreement slotted) and the round-19 Search-log note are in the draft. Seat facts (re-opener names, access dates, agreement clauses, candidate counts) are `⟨…⟩` slots.
- Nothing was fetched by this seat. The round-19 re-opens must be run by non-authors with curl, each writing `fetch/<seat>/receipts.jsonl`.

## Limits

- No web source opened by this seat. S097's and S098's access dates and agreement clauses are unobserved here and remain `⟨…⟩`.
- The walker binary's mtime (`2026-10-08 11:14:32 -0300`) being package-build time is `[INFERENCE]`, not checked against pacman metadata (pacman queries are paused host-wide).
- `Cargo.lock` is cited as corroboration only; the draft does not admit it as a row (S099–S105 are L1-assigned).
- Whether `fetch-verify.py` should treat superseded-row-only URLs as excluded from CONFLICT is `[UNK]`; I did not change or run the tool.
- Did not verify `corpus/knowledge/walker-route-r18.md` or `theme-route-r18.md` citations; the used-by proposals assume the walker/theme seats update those notes.
- The Gate skeleton is not a row set; L1 must still run QUALITY 17 review on the S096/S097/S098 URLs against existing rows.

## Installs

none (no tool installed or upgraded; `sha256sum`, `grep`, `stat`, `sed`, `tar` were used as already present on the host).

# SourcesFrontierDraft — round-19 `## Gate` skeleton and `## Search log` note (draft, not landed)

Drafted by `MadoR19.SourcesFrontierDraft` for L1. Targets: `corpus/lessons/round-19.md` `## Gate` (shape of `corpus/lessons/round-18.md` `## Gate`) and `corpus/SOURCES.md` `## Search log`. Slots `⟨…⟩` are seat facts pending. Unslotted values were re-read by this seat from committed bytes or round-18 receipts; each cites its source. No web source was opened by this seat.

Axes: **A1** anchor reproducibility (anchor bytes equal across fetches; HTML excluded). **A2** version pin (tag, crate version, or host bytes). **A3** census integrity (a duplicate URL needs a `supersedes S0NN —` opener, QUALITY 17).

## Gate

Candidates considered: tag-pinned walker v2.17.2 raw `Cargo.lock` (round-18 receipt `MadoR18.SrcWalkerThemes`, 15:41:16Z, body sha256 `3448367c28c769e29f681ea2de84d4a822f08569bbef6628f03535c61fec2315`; lines 2705-2708 pin `xdg` 3.0.0 with checksum `2fb43323…`) — corroboration only, cited inside S098's teaches, no row of its own; crates.io archive `https://static.crates.io/crates/xdg/xdg-3.0.0.crate` — admitted as S098; docs.rs `xdg/latest` (sha256 `0291cfe6…`, receipts 16:00:17Z and 16:00:36Z) — rejected as support, unpinned alias; docs.rs `xdg/3.0.0` page (sha256 `adaec7c3…`, receipts 16:01:30Z, 16:03:01Z, 16:06:30Z) — rejected as sole support, HTML page, whose bytes differ from `/latest` only in nav chrome per `.ufo/waves/round-18/w2/reports/ReopenS084.md:81-82`; docs.rs `xdg/2.5.0` (sha256 `cb23df33…`, 16:02:12Z) — not the walker pin, not admitted; GitHub tree pages `themes/matte-black` and `…/backgrounds` at v3.8.4 — rejected: per-fetch tokens, two receipts for the same URL at 16:00:00Z have different digests (`ReopenS094/tree-theme.html` `6b355a46…`, `tree-theme-2.html` `3b18a612…`); raw `themes/matte-black/colors.toml` at v3.8.4 — admitted as S097; `/usr/bin/walker` bytes and `/var/log/pacman.log:2929` — admitted as host row S096; third-party blogs, AUR pages, Arch wiki — not opened, out of tier.

Admit rules (round-19 additions to the round-18 rules):
1. Tag- or crate-version-pinned raw or archive bytes whose sha256 is reproduced by at least two receipts.
2. Host file bytes as host rows. Host rows carry no fetch receipt; the C2 receipt statement covers credited web rows only (round-18 Wave-2 note).
3. A row whose URL or scope overlaps an existing row opens `teaches` with `supersedes S0NN —` and names what is dropped (SOURCES round-12 errata; QUALITY 17).
4. An anchor is never edited in place (append-only). A wrong anchor is superseded by a new row.

Reject: HTML as sole digest anchor (docs.rs pages, GitHub tree pages); unversioned alias URLs as version-specific support; log lines or package bytes as running-process facts.

New rows S096–S098 (tier A, status `mined`, opened 2026-10-20). Each lands only after its non-author re-open below.

- **S096 — host walker bytes and upgrade line.** Joins S090 line 2929 and the binary clause of S091; supersedes neither. Kind `code`; scope: host walker binary version binding at 2.17.2, file bytes only. Anchor: `/usr/bin/walker` 7,039,912 B sha256 `25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096` (equal to S091's binary clause today); `/var/log/pacman.log:2929`; `grep -a -o '2\.17\.[0-9]' /usr/bin/walker` returns one match, `2.17.2`. Located quote: `/var/log/pacman.log:2929` "[ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)" (6 words). Teaches: "host binary bytes carry version 2.17.2 and the log records the upgrade on 2026-10-20; neither is a running-process fact; `/usr/bin/walker` mtime 2026-10-08 11:14:32 -0300 is package-build time [INFERENCE]." Recheck `on-change`. Used-by `⟨corpus/knowledge/walker-route-r18.md; SKILL.md pin rows⟩`.

- **S097 — supersedes S094 (raw `colors.toml` only).** URL `https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml`; access 2026-10-20 (first receipt 15:59:53Z). Kind `code`; tier A; scope: upstream matte-black payload file at tag v3.8.4 (tag → commit `8fcc9d60`, from the round-18 reopen). Anchor: sha256 `dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786`, 461 B. Located quote: `ReopenS094/colors.toml:4` `background = "#121212"` (3 words). Teaches: "supersedes S094 — raw colors.toml only; S094's tree-page HTML digests are dropped as anchors (per-fetch tokens, round-18 M7). Host equality with `current/theme` is S095's claim, not this row's." Recheck `on-release`. Used-by `corpus/knowledge/theme-route-r18.md` (⟨confirm the note cites S097 for the file⟩).

- **S098 — supersedes S084 (crate archive).** URL `https://static.crates.io/crates/xdg/xdg-3.0.0.crate`; access 2026-10-20 (16:02:39Z, `MadoR18.RevengeTarballRepro` receipts). Kind `code`; tier A; scope: the `xdg` 3.0.0 crate walker v2.17.2 pins (`Cargo.lock:2705-2708`) for `find_config_file`. Anchor: sha256 `2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5`, 15,821 B (re-hashed by this seat from `.ufo/waves/round-18/fetch/SrcWalkerConfigPaths/xdg-3.0.0.crate`; match). Located quote: `xdg-3.0.0/src/base_directories.rs:447-448` "Searches `XDG_CONFIG_HOME` and then `XDG_CONFIG_DIRS`." (5 words). Default lines `:217` and `:221` ("`XDG_CONFIG_DIRS`; if not set: assumed to be `/etc/xdg`.") verified by this seat from the extracted member. Teaches: "supersedes S084 — version-pinned archive for the crate walker v2.17.2 pins; `Cargo.lock:2708` checksum equals this sha256; `find_config_file` searches `XDG_CONFIG_HOME` then `XDG_CONFIG_DIRS`; defaults `$HOME/.config` and `/etc/xdg`." Recheck `on-release`. Used-by `corpus/knowledge/walker-route-r18.md`.

## Gate — re-opened by non-authors (round 19)

Each line is the re-opening seat's own `GATE` line: URL or host path, access date, located quote ≤25 words with body anchor, sha256 of the body read, verdict. Pre-filled fields are this seat's re-read of committed bytes; the agreement clause is the re-opener's to write.

- GATE | S096 | /usr/bin/walker; /var/log/pacman.log | 2026-10-20 | /var/log/pacman.log:2929 "[ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)" (6 words) | 25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096 | agree: ⟨re-opener, byte count, grep count⟩
- GATE | S097 | https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml | ⟨access date⟩ | .ufo/waves/round-18/fetch/ReopenS094/colors.toml:4 "background = \"#121212\"" (3 words) | dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786 | agree: ⟨re-opener, fresh 200 bytes, tag→commit⟩
- GATE | S098 | https://static.crates.io/crates/xdg/xdg-3.0.0.crate | ⟨access date⟩ | .ufo/waves/round-18/fetch/SrcWalkerConfigPaths/xdg-3.0.0.crate:xdg-3.0.0/src/base_directories.rs:447-448 "Searches `XDG_CONFIG_HOME` and then `XDG_CONFIG_DIRS`." (5 words) | 2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5 | agree: ⟨re-opener, fresh 200 bytes, Cargo.lock:2708 match⟩

## Status / recheck / used-by changes to existing rows, old→new

- S084: status `mined` → `⟨rejected (recommended: unpinned alias, round-18 Gate reject rule) | mined (history only)⟩`; recheck `on-release` → `on-release` (no change; the alias moves at crate release); used-by `corpus/knowledge/walker-route-r18.md` → `⟨— once walker-route-r18.md cites S098 for find_config_file; walker lane edit⟩`.
- S094: status `mined` → `mined` (no change; credited raw URL reproduces, round-18 M7); recheck `on-release` → `on-release` (no change); used-by `corpus/knowledge/theme-route-r18.md` → `corpus/knowledge/theme-route-r18.md; S097 (raw file)`. S094's anchor stays as written (append-only).
- Census after landing (⟨if S084 → rejected⟩): rows 95 → 98; tier A 88 → 91; mined 80 → 82; rejected 7 → 8; queued 8 unchanged (baseline re-counted this seat from `corpus/SOURCES.md`).

Open for L1 before R18-V1 can close: `.ufo/waves/round-18/fetch-verify.py:386` emits CONFLICT per URL over all receipts, so the GitHub tree-page conflicts stay in the receipt set and exit 1 persists after S097 lands. `⟨L1 decision: exclude superseded-row-only URLs from the conflict rule, or keep exit 1 as the recorded state⟩`.

## Search log note (for `corpus/SOURCES.md` `## Search log`)

**Round 19 (2026-10-20)** — question: which pinned sources can replace the HTML digest anchor of S094, the unpinned `latest` alias of S084 (R18-V4), and the host walker version binding, without an HTML page as sole support? Where: round-18 receipts re-read in place (`.ufo/waves/round-18/fetch/ReopenS084`, `ReopenS094`, `SrcWalkerConfigPaths`, `MadoR18.RevengeTarballRepro`, `MadoR18.SrcWalkerThemes`); host file bytes (`/usr/bin/walker`, `/var/log/pacman.log:2929`); and round-19 non-author re-opens by ⟨seats⟩ with curl only. Identified ⟨N⟩ candidate locations: 8 (walker `Cargo.lock`; xdg crate archive; docs.rs `xdg` latest, 3.0.0 and 2.5.0; GitHub tree pages, 3 bodies; raw `colors.toml`; host walker bytes and log line). Screened ⟨N⟩ by byte re-read and receipt comparison. Included ⟨3⟩ (S096–S098, pending re-open), excluded ⟨5⟩: docs.rs pages as HTML sole support or unpinned alias (3), GitHub tree pages with per-fetch digests (1), walker `Cargo.lock` kept as corroboration rather than a row (1). Stop: ⟨L1 — each of the three defects R18-V1 and R18-V4 has a pinned replacement or an explicit rejection; R18-V3 is a sibling-note sweep, not a source search⟩. No existing row's status/recheck/used-by changed ⟨or: S084 used-by and status changed, see the Gate⟩.

## Limits

- No web source was opened by this seat. Every fetch-dependent value is a round-18 receipt or a pending slot.
- Host files were read as bytes only (`sha256sum`, `grep -a`, `stat`, `sed` on `/var/log/pacman.log`); no package, service or binary was executed.
- The `/usr/bin/walker` mtime is package-build time by inference; it is not verified.

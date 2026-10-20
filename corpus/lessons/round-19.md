author: mado-shokunin (L1 + lane-dispatched L2 advice)

# Round 19 — durable anchors, supersession sweep, walker pin currency, tripwire recall

Date: 2026-10-20. Baseline `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d`;
pre-registration `17661e0`. Motivation: the admitted round-18 closure
(`round-18-verifier-spotcheck.md` §6: R18-V1..V4, carried frozen F1/F2,
`measure-mutants.py --out`, jj audit F6/F9/F16/F17, three tripwire drafts). Wave
evidence under `.ufo/waves/round-19/`; report `.ufo/reports/round-19/mado.md`
(fleet).

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M1 | reference-drift (R18-V1) | `9c54c56:corpus/SOURCES.md:106` (S094) anchors two GitHub tree-page HTML digests (`50c1ac25…`, `9e1160a0…`); committed receipts hold 5 distinct 200 digests for the tree URL (w1 `HtmlAnchorSweep`: 7 and 6 distinct across all seats), so the anchor cannot be re-obtained. Round-18 lesson M7 named it; the row stayed `mined` and credited. | round-18 Gate prose only; `fetch-verify.py` CONFLICT is per URL and never touched the row's credit | QUALITY 27 + `.ufo/waves/round-19/anchor-durability.py`: red `9c54c56` `FLAGGED S084 S094` exit 1 → green `df84807` `flagged=0`. S097 supersedes with tag commit `8fcc9d60…` and git tree ids (`themes/matte-black` `3fc08f95…`), S094 `mined → rejected`. `fetch-verify.py` still exits 1 on the historical round-18 receipts (append-only; not claimed fixed). |
| M2 | scope (R18-V4) | `9c54c56:corpus/SOURCES.md:96` (S084) cites `docs.rs/xdg/latest/…` as version-specific support for walker's config search order. The page bytes did reproduce (w1 `UnpinnedUrlSweep`, `CriticC1`), so the content was right; the alias moves on the next xdg release. | round-18 Gate prose ("unversioned docs sites as version-specific support" rejected); re-open seat advised a re-point; no check | QUALITY 27 UNPINNED_ALIAS arm (red S084 at `9c54c56`). S098 = xdg 3.0.0 crate, sha256 `2fb43323…85b5` equal to walker v2.17.2 `Cargo.lock:2708` checksum; S084 `mined → rejected`; `walker-route-r18.md:1` token re-pointed with an appended correction block. |
| M3 | landing (R18-V3) | Round-18 `ConnStalePinsSweep` listed the stale files, but the fix landed only as a SKILL erratum (`SKILL.md:1822`) and the newer note: 11 of 13 owned files still stated walker `2.17.0` with no in-file pointer (`.ufo/waves/round-19/evidence/fresh-pins-before.txt`: 2/13). | none (PROTOCOL "corrections sweep every mention" is prose) | QUALITY 28 + `.ufo/waves/round-19/supersede-sweep.py`: red `9c54c56` `stale=11` exit 1 → green `df84807` `stale=0`. Limit: file-level (CriticC1 mutant: a bare `# S096 2.17.2` line passes); reviewers read each pointer. |
| M4 | attribution (R18-V2) | Criterion 26's red-before `.ufo/waves/round-18/evidence/gate-rc-redbefore.txt` has 0 `tool_sha256=`/`measured_commit=` fields; criterion 24 fails on its sibling criterion's own evidence. | QUALITY 24 itself — but nobody ran its checker over the lane's criterion evidence | Applied, not re-numbered (CriticC1: a criterion 29 would restate 24): round-19 `receipt-claims.json` red claims read `MISSING_PROVENANCE`; header-bound re-cut `evidence/gate-swap-receipt.txt` (fixture committed `df84807`, `tool_sha256=6e6782c3…`): 383 passed / 6 failed — five OM9 plus R10, which round 18's "383/389, five OM9" left out. |
| M5 | attribution (this round, L1) | The pre-registration receipts `evidence/tw-recall-before.txt` and `fresh-pins-before.txt` say `measured_commit=9c54c56` while the producer tools first exist at `17661e0`, and their header says "tool not yet committed" although the same commit carried them. `receipt-check.py` reads both `ERROR` (w1 `ReceiptClaims19`, `QualityDraft`, `LogDraft`). | QUALITY 24 / `receipt-check.py` (caught it) | Re-cut as `evidence/*-before-recut.txt` with `measured_commit=df84807` (the commit carrying the producer) and the data rev as the argument; bodies identical to the originals (`diff` of all lines after the header: equal). Rule kept: `measured_commit` names the producer's commit; a counter's data revision goes in its argv. |
| M6 | landing / privacy (this round, seat) | Seat `HtmlAnchorSweep` saved three `HTTP 200` ArchWiki bot-challenge pages as bodies; each embedded the operator's public IPv6 in `X-Real-Ip` (w1 `SentinelVcsFixtures` HIGH). Nothing under `round-19/fetch` was ignored, so a directory commit would have published them. | none: gitleaks does not flag IP addresses; a 200 status is not content | Bodies moved to `/tmp` before any commit (seat), `fetch/.gitignore` keeps all HTML/crate/API bodies digest-only (30 lines), and the commit set was scanned before landing (`gitleaks dir` on a copy of exactly the committed files: no leaks; grep `X-Real-Ip`/IPv4 pattern: only the redacted sentinel report and `WITHHELD.md` prose). A 200 receipt for an interstitial page is not a source body. |
| M7 | vacuous (this round, L1 pre-registration) | `tw-recall.py` credits any finding of any class on an incident line; CriticC3 built a 3-line regex tool that scores 6/6 and that `frozen-repin.py` accepts. Recall on six lines the drafts were written for is overfit evidence by construction. | none in the counter | Reported beside recall, not instead of it: class of each former miss (must be `package_query/pacman:-Q`, from the round-18 known-miss notes, not from the tool), zero findings on the 20 control lines, and a whole-corpus base-vs-merged diff (no lost finding; every added finding outside the new classes listed and judged). The counter is pre-registered and unchanged. |
| M8 | landing (seat) | Seat `QualityDraft` wrote its draft and report at the fleet root `.ufo/waves/round-19/` (relative path). | misroot sweep (fleet `git status --porcelain`) | Copied byte-exact into the lane, `cmp` equal, fleet copies deleted (L1). |
| M9 | provider | ~30 wave-1 seats routed to m_zfl (reviewer, connector, revenger, simplifier) ended `429 Rate limit reached` after 10 retries (zai glm-5.3-flash); no dead seat was respawned. | none | Wave 2 leans on roles whose routes answered (scout/executor m_flash, critic/sentinel m_opus, mutation-tester m_sol); the dead seats are listed in the report. |

## Gate

Candidates considered: the host walker binary and package metadata read as bytes;
tag-pinned walker raw files at v2.17.0/v2.17.1/v2.17.2 (delta seats); the walker
v2.17.2 `Cargo.lock` and the xdg 3.0.0 crate from static.crates.io; docs.rs pages
(`latest`, `3.0.0`); GitHub tree pages; a /tmp clone of omarchy at v3.8.4; ArchWiki
`oldid` raw pages (bot-walled).

Admit: host file bytes as host rows; tag-pinned raw files; a registry archive whose
digest equals the tag's own lockfile checksum; git object ids from a tag clone.
Reject or leave unrowed: docs pages as version-specific support; GitHub tree HTML
(rotating digests); bot-challenge pages (not the named content).

New rows (all opened 2026-10-20):

- GATE | S096 | host `/usr/bin/walker` (+ `/var/lib/pacman/local/walker-2.17.2-1/desc`, `/var/log/pacman.log`) | 2026-10-20 | `/usr/bin/walker` byte 856,302: "version2.17.2" (1 word) | 25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096 | admit: one `2.17.2` literal, zero `2.17.0` (L1 re-read: `find` → 856302, count 1, `2.17.0` → -1); `pacman.log:2929` "upgraded walker (2.17.0-1 -> 2.17.2-1)" — file bytes only, `--version` not run
- GATE | S097 | https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml | 2026-10-20 | `.ufo/waves/round-19/fetch/SrcS094/colors.toml:4` "background = \"#121212\"" (3 words) | dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786 | admit: 200, 461 B; tag v3.8.4 lightweight → `8fcc9d60…`; tree ids from a /tmp clone
- GATE | S098 | https://static.crates.io/crates/xdg/xdg-3.0.0.crate | 2026-10-20 | `xdg-3.0.0/src/base_directories.rs:447-448` "Searches `XDG_CONFIG_HOME` and then `XDG_CONFIG_DIRS`." (6 words) | 2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5 | admit: 200, 15,821 B, equals walker v2.17.2 `Cargo.lock:2708` checksum (receipted lock, `fetch/SrcS084/walker-v2.17.2-Cargo.lock`); crate body kept digest-only

Status/recheck/used-by changes, old→new: S084 status `mined` → `rejected`,
used-by `corpus/knowledge/walker-route-r18.md` → `—` (superseded by S098: unpinned
`latest` alias, R18-V4); S094 status `mined` → `rejected`, used-by
`corpus/knowledge/theme-route-r18.md` → `—` (superseded by S097: per-fetch HTML
digests, R18-V1). Recheck cells unchanged. Rows 95 → 98 (A 88 → 91; mined 80 → 81;
rejected 7 → 9).

## Decisions (L1, with the seat that argued each)

- Tripwire drafts: apply all three rebased (`TwBashCVar`, `TwHelperFn`,
  `TwInstallers`) plus `TwVcsClass`, `TwFrozenF1`, `TwFrozenF2`, composed by one
  integration seat (`TwMerge-2`). Installer class `tool_install` lands
  permit-able, never `host_mutation` (CriticInstallerClass: apply-with-permit;
  installs are operator-authorized). It moves C3 by 0/6 and is not credited to C3.
- Gate: walker pin `2.17.2` with the PASS narrowed to "installed version matches
  pin; claims measured on 2.17.0 stay dated" (CriticC2 option 2); jj F6 rescue
  only when `$tree/.jj` exists (CriticHonesty hole); F9 `rev-parse --git-dir`.
- QUALITY: 27 and 28 only; R18-V2 recorded as an application of 24 (CriticC1).
  C1 therefore misses its pre-registered ≥21/29 target.

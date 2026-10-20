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

## Wave-2 corrections and mistakes (append-only, 2026-10-20)

Wave 2 (67 seats over `01b8094`; reports `.ufo/waves/round-19/w2/reports/`) attacked
every claim, row, pointer and new tool. Corrections to the rows above:

- M4: round 18 did not omit R10 everywhere — `round-18/w3/reports/W3CriticC1Final.md:188`
  names it; only the round-18 SCORECARD fragment did (w2 RerunGateSwap). The gate-swap
  receipt is a new header-bound red on a hybrid fixture, not a header on the old file.
- M5: the "(tool not yet committed)" note was true when written (receipt 16:59:29Z, commit
  16:59:52Z; w2 RerunReceipts). The defect is only `measured_commit=9c54c56`, a commit
  that does not carry the producer. The round-19 claims now point at the re-cuts.
- M6: the first `fetch/.gitignore` listed 29 paths, not classes, so a later seat's
  `xdg-3.0.0.crate` was unignored (w2 SentinelCommitSet F1). Class patterns (`*.html`,
  `*.crate`, `*.json` except `RETENTION.json`) and `fetch/RETENTION.json` (16 commit, 32
  digest-only, incl. the three withheld bot-challenge receipts) now carry the rule.
- M9: wave 2 still placed 10 reviewer seats on m_zfl; the role routing is fixed by the
  orchestrator, not by L1 (w2 ScribeLogCheck).

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M10 | landing (seats, L1 integration) | Two pointer blocks written in w1 say S096 is "reserved"/"row pending" (`remaining-planes-census.md:338`, `walker-live-surface.md:305`), and L1 landed them in the same commit as the S096 row (`df84807`); `fresh-pins.py` credited both through their S090 token (w2 AtkPtrRemainingPlanesCensus, AtkPtrWalkerLiveSurface, AtkReadmeFrontier, CriticC2W2). Five more blocks call re-read items "not re-measured" (w2 AtkPtrWalkerDeep, AtkPtrWaybarWalkerSemantics, AtkPtrConfigHealthReportR3, AtkPtrArcSynthesis). | none: the C2 counter reads a token, not the sentence | Appended wave-2 correction blocks in all seven notes; C2 reported as "13/13 pointed; 7/13 cite S096; 0 walker facts re-measured on 2.17.2". Rule: a seat draft that reserves an id is re-read after the row lands, before commit. |
| M11 | vacuous (L1) | Criterion 28's checker exited 1 at the integration tip once the ledger gained the S094→S097/S084→S098 entries: the new SKILL registry rows name S094/S084 with no S097/S098 line (w2 CriticAdmission). The harm watch did not run either criterion checker. | criterion 28's own checker (caught it when run) | SKILL line naming both supersessions; both checkers re-run at the final commit with header-bound receipts in `evidence/final/`. |
| M12 | host-pause breach (seat) | Seat `SentinelGatePath` ran the real `/usr/bin/hyprctl probe` once (rc 0, `unknown request`) while building a stub harness whose mount step failed, just before 18:05Z; it self-reported and hardened its script (w2 SentinelGatePath § Incident). | the post-wave tripwire scan (`live_probe` class) | Disclosed; no state change observed. The wave context forbade hyprctl; prompt fences remain prompt-level (round-18 M5). |
| M13 | scope (L1 pre-registration) | `fresh-pins.py` credits `corpus/README.md:44` and `walker-route-r18.md:1` at `9c54c56` (a round-18 row and a source list), so the substantive pre-state was 0 dated pointers, not 2 (w2 RerunC1, CriticC2W2 F3); line-level, 55 of 73 `2.17.0` lines carry no same-line pointer (w2 ScribePlannedRow). | none | Reported beside the score; a round-20 line-level rubric is planned. The pre-registered counter is unchanged. |
| M14 | survivor (tripwire) | HelperFn rule B (literal argv to an undefined name) is the sole source of the 6th recall line; without it C3 reads 5/6, and it fires on 12/12 synthetic data-only shapes (dataclass constructors, imported classifiers) the base tool leaves clean; lead rows are not marked as leads (w2 CriticC3W2). Eval-surface VCS writes (the real `.jj` birth, merge, push loop) give 0 `vcs_write` findings (w2 AdvVcs); `curl … | sh` is not classified (w1 RevDraftInstallers). | the w2 adversarial seats | Recorded as limits in SKILL and SCORECARD; round 20 plans the name-binding guard, lead tagging and eval-argv coverage with the w2 regression cases. |

Gate (wave 2): every new row re-opened by a non-author seat — S096 (w2 ReopenS096,
CriticC2W2, AtkSkillErratum, AtkPtrWalkerRouteR18: bytes, offset, BuildID, `.comment`
reproduce), S097 (w2 ReopenS097, AtkPtrThemeRouteR18: 200/461 B/`dbdd13a6…`, own clone
tag `8fcc9d60…`, trees `3fc08f95…`/`ff02c341…`), S098 (w2 ReopenS098 and AtkReadmeFrontier:
crate `2fb43323…` = `Cargo.lock:2708`, quote at `base_directories.rs:446-448`).

Gate corrections (w2 AtkLessonGate): the S096 quote `version2.17.2` begins at byte 856,295;
856,302 is the start of the `2.17.2\n` literal the row anchors. The S098 quote is 5 words
(two rustdoc lines joined after stripping `///`), not 6.

Further wave-2 corrections (w2 CriticHonestyW2, RerunC2, SentinelToolSafety):
- M1's fetch-verify sentence: a bare `fetch-verify.py` run exits 0; with `--sources` its
  CONFLICT check is global, so even `--rows S097` exits 1 on the historical S094 tree URLs,
  and pointed at the round-19 fetch root it reports digest-only bodies as missing. It is not
  a per-row durability check; QUALITY 27's checker is.
- The two "reserved/pending S096" sentences were corrected in place (marked
  `[wave-2 corrected wording]`); the appended correction bullets stay.
- C2 sourcing: 5 of 13 credited files name S096 on the crediting line; the rest credit
  S090 or the README S072–S091 span. The counter certifies "a permitted row", not S096.
- `measure-mutants.py --workdir` no longer deletes a caller-named directory (the tool now
  makes its own `mkdtemp` inside it; canary kept, summary unchanged 6/6). Still open:
  `--out` guard only covers the `--lane` worktree; `harm-watch.sh` runs the worktree
  SCORECARD block; `supersede-sweep.py` reads its ledger from the worktree;
  `anchor-durability.py` exits 1 on a malformed receipt line; `frozen-repin.py` writes a
  README receipt without `measured_commit` (receipts for the round-19 frozen replay are
  re-cut header-bound in `evidence/final/`).
- The round-17 hardening suite reads 32/33 under the pre-round tool after its one case
  edit; the all-pass statements refer to the merged tool.
- S096 used-by gained `corpus/knowledge/walker-route-r18.md` and `corpus/README.md` (both cite it; w2 ReopenS096, CriticC2W2 F8); old→new: the six-path list → the eight-path list.
- vcs_write precision (w2 RerunPrecision): 78 of 4,818 added rows are not writes — 74 `jj <sub> --help` and 4 `git --dry-run/-n` (docstring says help is excepted; code falls through). Round-20 fix with the w2 15-line fixture.
- Installs during the round: seat `AdvInstallers` (w2) ran pip 26.2.1 ephemerally via `uv run --no-project --with pip` (uv cache only, no PATH change) to adjudicate pip grammar; no other install by any mado seat or L1. Gate fixture losses during wave 2 trace to an external `rm -rf /tmp/w5-mado-m52-selftest.*` at ~18:04:53Z (w2 RerunGate), not a gate defect.

Post-wave seat scan (`evidence/final/tripwire-seat-scan.txt`, merged tool `367be947…`,
155 round-19 transcripts, `--permit tool_install`): `host_mutation` 0, `package_query` 0,
`tool_install` 0, `live_probe` 3 (`ps`, `pgrep`, and one `walker` token inside a data
string — a false positive), `vcs_write` 164 (all git writes in seats' own `/tmp` clones and
bare `/tmp` remotes; 0 against the lane path). The scan did **not** see M12's real `hyprctl
probe`: it ran inside a harness script the seat wrote and then executed, a form the tool
documents as unanalysed. M12's captured-by is therefore `none (seat self-report)`, not the
tripwire. AdvInstallers' `uv run --with pip` is not classified (documented limit).
- QUALITY 17 overlap screen for S096 (w2 ReviewSourcesRows F3): S096 shares `pacman.log:2929`
  with S090 and the binary sha256 with S091. It is kept as a separate host row because its
  scope is the installed walker *version identity* (the compiled-in literal, BuildID, package
  `desc`/`mtree` binding), which neither S090 (log lines only) nor S091 (config and binary
  bytes, no version literal) states. S097's host-side teach clauses are grounded in w1
  `SrcS094.md`, not in its upstream-only anchor (F4; noted, row unchanged).
- Gate jj rows after wave 2 (w2 ReviewGateF6F9, ReviewJjFinal): at `01b8094` an empty
  `.jj` directory alone enabled the tip rescue (closed at `61eaa07` by the tree-equality
  check, OM17). Still open (low): a stale `.jj` with HEAD detached on a content-identical
  commit reads HELD (no ancestry check). F9's `rev-parse --git-dir` walked up to an
  ancestor repo (`/home/vgpnk/.git`) for a `.git`-less tree and accepted bare repos; the
  final gate adds `[ -e "$tree/.git" ]` before it (see the final gate receipt).

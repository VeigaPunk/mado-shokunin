# ScoutMergeRest — the staged `merge/mado` package after round 40, grouped by theme (round 41, w1)

Read-only survey. Evidence: `merge/mado/MERGE-REPORT.md` (69 knowledge targets = 65 `new-file`/`knowledge/` files + 4 `amendments/`),
`ls` of the staged tree and of `corpus/knowledge/` (59 files), `cmp` of same-named files, `grep` of `source:` lines over the staged entries,
`PROVINCE.md` (round-36 channel rule, lines ~68-80 of the read), `corpus/SOURCES.md` tail (S282, 219 rows).
Facts marked OBS were read this seat; INF is inference.

## 0. Cross-cutting facts that decide every theme

- OBS: the staged package is `cmp`-DIFFERENT from the lane in all 7 same-named files (`event-delivery-limits-r26`, `hyprctl-flags-r28`,
  `idle-lock-chain-armed-r14`, `idle-lock-never-asked-r12`, `idle-lock-offered-in-the-bar-r15`, `request-limits-upstream-r31`,
  `request-socket-live-bound-r8`). The lane's copies are its own re-grounded round-35/38 versions (e.g. lane `idle-lock-chain-armed-r14.md:1`
  "armed on this host - the daemon is running"; staged title "…armed… turns the preference into a question"). Copying the package over them
  would overwrite lane text — the package's own adopt step 5/6 says fold/append, never replace. These 7 are HELD: no further work.
- OBS: **id collision.** Staged rows run S203–S349 (`SOURCES.append.md`, 153 lines); the lane already holds S203–S282 with other content
  (lane S203 = `omarchy-first-run`, S205 = round-35 receipt; staged S203 = Hyprland IPC wiki). Every adoption renumbers; the package's
  `used-by`/`S###` cites inside entries are in the staged numbering and cannot be pasted. Round 41 uses S283+ (registration).
- OBS: 26 of the 65 staged files carry at least one `source: S### — lanes/mado/roundN/fetch/…` cite (list in §9). Those fetch files are the
  ancestor lane's receipts; they do not exist in this repo (rows point at paths outside it), so each such claim is unverifiable here until the
  receipt is re-derived. 7 more files cite host files (`~/.config`, `~/.local`, `/run/user/1000/hypr/<instance>`) read 2026-10-23/24: re-derivable, but dated.
- OBS: the round-41 focus theme already consumes 13 files (§1); the remaining 52 + 4 amendments are grouped below.

## 1. Focus control surfaces (round 41's theme — consumed or refused by C2; listed so they are not re-proposed) — 13 files
`focus-control-surfaces-r28`, `focus-grab-protocol-live-on-host-r14`, `privileged-client-surface-r29`, `focus-grab-seat-semantics-r8`,
`-observed-semantics-r9`, `-focus-selection-r10`, `-mouse-target-r11`, `-whitelist-admission-r12`, `-keyboard-routing-r13`,
`-has-no-client-here-r15`, `compositor-focus-manipulation-literature-r26`, `wayland-input-security-literature-r8`,
`upstream-input-holds-and-the-lock-screen-r16`.
- Scope: IN for the compositor/protocol/rule content (hypr config plane's focus rules and the compositor's advertised protocol set);
  OUT for `focus-control-surfaces-r28` §Japanese (S230 amgsk.dev) and refused `privileged-client-surface-r29` (generic analysis).
- Private receipts: `focus-grab-seat-semantics-r8` (S275), `-observed-semantics-r9` (S293), `-protocol-live-on-host-r14` (S328), `-has-no-client-here-r15` (S338).
- Leftover after C2 (INF): `upstream-input-holds-and-the-lock-screen-r16` (S349, public wiki `allow_input_capture`/`locked` flags; lane's `bind-table-r25.md` mentions `allow_input_capture`)
  and the two academic-literature entries (S278/S279/S218 public abstracts) are small, public, in-province follow-ups.

## 2. gkeep geometry — 11 files (the largest redundant cluster; one entry's worth of content)
`gkeep-geometry-unobservable-r8`, `gkeep-rendered-geometry-chain-r9`, `-size-rule-application-r10`, `-size-to-real-size-r11`,
`gkeep-observation-route-r11`, `-client-size-request-r12`, `gkeep-rendered-geometry-record-r13`, `-record-r14`, `gkeep-geometry-never-recorded-r15`,
`gkeep-element-rules-r30`, `glyph-and-geometry-r31` (geometry half).
- OBS: lane holds none of the size-application chain: `grep -l 'set_default_size|sendWindowSize|static_\.size|REPORTSIZE|WindowRuleApplicator'` hits only `rule-attribution-r24.md` (tag matcher, not size).
  `config-drift-r12.md` holds gkeep.conf's installation drift only. Host rule file still reads `windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$` (`~/.config/hypr/gkeep.conf`, read this seat).
- Scope verdict: **IN** — the window rule lives in the owned `~/.config/hypr/` plane and "what size the rule yields" is the province's screen behaviour; the gkeep *app* (`~/Projects/gkeep`) is not owned (only its rule is) — r40 already drew that line for the producers.
- Public vs private: the chain's mechanism links are public bytes at pinned `v0.56.2` (S284, S297, S298, S302–S305, S311, S318, S319 Hyprland; S285/S312 gkeep `ui.py` at 133b867; S286 GTK docs; S287 wiki). Private receipts: S292, S293 (`r9`), S299 (`r10`), S310 (`r11`×2), S320 (`r13`), S326 (`r14`), S339 (`r15`), S275 (`r8`). The absence claims (r13/r14/r15: "no journal/log/artifact ever recorded the window's size") rest ONLY on those private sweeps; re-derivable by read-only journal verbs.
- Maintainability: 11 files for one conclusion ("rule requests size → compositor adopts → client reports; never observed on this host"); a single successor entry is the right shape (as r40 did for bar producers).

## 3. Idle / lock series — 11 files, 3 already held
Held (same name in lane, different bytes, round-35 re-grounded): `idle-lock-never-asked-r12`, `idle-lock-chain-armed-r14`, `idle-lock-offered-in-the-bar-r15`.
Remaining: `host-idle-lock-chain-r7`, `idle-lock-intent-mechanism-r8`, `-surface-r9`, `-surfaces-r10`, `idle-lock-journal-evidence-r11`,
`idle-lock-runtime-state-r28`, `idle-toggle-and-daemon-lifecycle-r29`, `host-bar-and-idle-binding-r26`.
- Scope: **IN** (PROVINCE "screen/idle behaviour (hypridle/hyprlock)"); idle plane already owned (`idle-lock-plane.md`, `idle-lock-route-r17.md`, three r35 files).
- Staleness (INF/OBS): `idle-lock-runtime-state-r28` says the daemon "is not running" — contradicted by the lane's own r35 "armed" entry (lane `idle-lock-chain-armed-r14.md` title); r7/r8–r11 intent-surface sweeps are the same question the held r12/r14/r15 entries already answered. Only the public-bytes parts are fresh: S234/S235/S236 (omarchy v3.8.4 toggle/refresh/restart scripts), S267/S265 (stock hypridle.conf, system-lock), S223/S225 (hypridle unit).
- Private receipts: `host-idle-lock-chain-r7` (S268), `idle-lock-intent-mechanism-r8` (S282, S283), `-surface-r9` (S291), `-surfaces-r10` (S300), `-journal-evidence-r11` (S309), plus the held three (S315, S316, S327, S340, S342). `S220` is the report's one row "no entry rests on" (names `idle-lock-runtime-state-r28`).
- Note S282/S283 in the staged numbering collide with lane S282 (round-40 row).

## 4. Socket client contract — 9 files + 4 amendments, mostly superseded
`socket-client-contract-measurements-r29`, `socket-modes-and-request-read-r30`, `host-request-socket-cap-r7`, `event-queue-host-measurement-r28`,
`event-queue-journal-measurement-r29`; held-and-different: `request-socket-live-bound-r8`, `request-limits-upstream-r31`, `event-delivery-limits-r26`, `hyprctl-flags-r28`;
amendments to `ipc-contract-r25`, `dispatcher-semantics-r25`, `waybar-module-text-route-r25`, `dispatcher-surface-and-request-grammar-r26`.
- Scope: **IN** (PROVINCE round-38 addendum: request-socket knowledge ground is documentation/source-read; no socket is ever connected).
- OBS: lane has `event-queue-observability-r37.md` (event removal not logged) and the round-38 live-bound/limits adoptions; staged `host-request-socket-cap-r7` ("no ceiling at all") and `socket-client-contract-measurements-r29`/`-r30` ("64 KiB", later "belongs elsewhere") are the contradicted chain that r31/r38 resolved — stale.
- Weak sources: `socket-client-contract-measurements-r29` rests on a third-party doc (S243 iconidentify/chonkstep `main`), not upstream.
- Re-derivable without a connection: socket directory/socket modes (S252: host `stat` of `/run/user/1000/hypr/<instance>/`; the cited instance dir `…_1792772698_…` is the 2026-10-23 session, not necessarily current), event-queue marker counts (S226 hyprland.log; S242 `journalctl --user -u wayland-wm@hyprland.desktop.service`).
- Private receipt: `host-request-socket-cap-r7` (S269).
- Amendments: the 4 amendments target lane files that exist; the staged round-1 amendments' rows are S203–S208/S213 whose pages the lane holds under other ids (MERGE-REPORT §"source already held"); fold only the added aspect.

## 5. Two-literature / Chinese-Japanese wiki — 15 files
`two-literature-coverage-r25`, `two-literature-drift-r26`, `chinese-wiki-canonical-url-r28`, `zh-wiki-snapshot-semantics-r29`, `chinese-article-revision-r30`,
`chinese-translation-drift-r31`, `chinese-wiki-revision-list-r7`, `chinese-wiki-ipc-section-r7`, `cn-framing-coverage-r8`, `chinese-ipc-framing-absence-r13`,
`japanese-input-observation-methods-r14`, `japanese-counted-comparison-gone-r15`, `window-size-read-in-chinese-r16`, `japanese-wayland-compositor-account-r16`, `chinese-hyprland-window-rules-r16`.
- Scope: **OUT** — PROVINCE round-36 refinement (channel rule) names this: "the Chinese/Japanese ArchWiki channel, its URLs, snapshot semantics, revision bookkeeping and translation drift, and any documentation written in a localized channel". `window-size-read-in-chinese-r16` and `chinese-hyprland-window-rules-r16` are localized-channel guides (S343 GitHub doc, S348 CSDN) — same verdict; `two-literature-drift-r26` has one English raw-wiki row (S215) but the entry's claim is translation drift: OUT.
- Private receipts: `chinese-article-revision-r30` (S245), `chinese-ipc-framing-absence-r13` (S322), `japanese-counted-comparison-gone-r15` (S341).
- Report, never absorb: do not adopt; a refusal note is the only lawful product.

## 6. uwsm / app lifecycle — 2 files
`uwsm-app-daemon-unit-r7`, `update-check-and-app-lifecycle-r31` (app-lifecycle half: `omarchy-restart-app` S257).
- Scope: **BORDERLINE-OUT** — the app-daemon scope units are session/unit state (tsukuroi's unit-health ground per PROVINCE tool table: "unit-state rows sit next to tsukuroi's"); the omarchy scripts are omarchy bin/, and the province treats the omarchy skill files as read-only documentation only. Only the angle "hypridle runs in a transient `app-Hyprland-hypridle-*.scope`" touches the owned idle plane, and the lane's r35 `idle-lock-chain-armed-r14.md` already holds it (staged r14 text at `:32`).
- Private receipts: `uwsm-app-daemon-unit-r7` (S270, S268).

## 7. Weather / update / bar producers — 6 files
`host-bar-producers-r28`, `host-producer-outputs-r29`, `host-producer-current-outputs-r30`, `weather-glyph-render-r7`, `glyph-and-geometry-r31` (glyph half), `update-check-and-app-lifecycle-r31` (update half S254).
- Scope: **IN for the bar module rows** (waybar plane) but **already done**: round-40 `host-bar-producer-census-r40.md` is the successor of `host-producer-outputs-r29` (refused) and `host-bar-producers-r28` (held, `assimilated-from` line), and leaves weather/update/voxtype output as UNK (no network/no execution).
- Remaining value: low and OUT-leaning: `host-producer-current-outputs-r30` (S248 omarchy-weather-icon public bytes; S249 `gkeep/waybar.py`, S250 `~/.local/share/gkeep/notes.json` — files of a project outside the owned plane, which r40 already declined). `weather-glyph-render-r7` (S271 private render log; installed font rasterisation — a font-rendering measurement, not a config-plane claim). `glyph-and-geometry-r31` glyph half is a public Nerd Fonts codemap read (S256) — cheap but trivia.
- Private receipts: `weather-glyph-render-r7` (S271).

## 8. Other
`host-bar-and-idle-binding-r26` (S214 Waybar 0.15.0 events + S219 hypridle.conf — public; IN; partially covered by lane `waybar-walker-semantics` and held idle entries), `event-queue-*` (see §4). No other orphan files.

## 9. Staged entries citing private receipts (`source: S### — lanes/mado/roundN/fetch/…`, 26 files, from `grep 'lanes/mado/round'`)
r7: `host-idle-lock-chain-r7` S268; `host-request-socket-cap-r7` S269; `uwsm-app-daemon-unit-r7` S270,S268; `weather-glyph-render-r7` S271.
r8: `focus-grab-seat-semantics-r8` S275; `gkeep-geometry-unobservable-r8` S275; `idle-lock-intent-mechanism-r8` S282,S283.
r9: `focus-grab-observed-semantics-r9` S293; `gkeep-rendered-geometry-chain-r9` S292,S293; `idle-lock-intent-surface-r9` S291.
r10: `gkeep-size-rule-application-r10` S299; `idle-lock-intent-surfaces-r10` S300.
r11: `gkeep-observation-route-r11` S310; `gkeep-size-to-real-size-r11` S310; `idle-lock-journal-evidence-r11` S309.
r12: `idle-lock-never-asked-r12` S315,S316 (held; lane version re-grounded on r35 receipts).
r13: `gkeep-rendered-geometry-record-r13` S320; `chinese-ipc-framing-absence-r13` S322.
r14: `focus-grab-protocol-live-on-host-r14` S328; `gkeep-rendered-geometry-record-r14` S326; `idle-lock-chain-armed-r14` S327 (held).
r15: `focus-grab-has-no-client-here-r15` S338; `gkeep-geometry-never-recorded-r15` S339; `idle-lock-offered-in-the-bar-r15` S340,S342 (held); `japanese-counted-comparison-gone-r15` S341.
r5: `chinese-article-revision-r30` S245.
Host-file/host-path cites (re-derivable, dated 2026-10-23/24, not private receipts): `gkeep-element-rules-r30` S251; `host-bar-producers-r28` S224; `host-producer-outputs-r29` S239-S241; `host-producer-current-outputs-r30` S249-S250; `idle-lock-offered-in-the-bar-r15` S335-S337; `socket-modes-and-request-read-r30` S252; `event-queue-host-measurement-r28` S226.
OBS: every one of these ids' `SOURCES.append.md` rows points to a `lanes/mado/roundN/fetch/…` path (26 distinct paths, per `uniq -c`; S275 and S293/S310 are shared by two entries), none of which exists under this lane.

## 10. Best next theme, and why — **gkeep rendered geometry (§2), as ONE successor entry**
1. In province: the rule is in the owned hypr plane (`~/.config/hypr/gkeep.conf`, 3 windowrule lines, read this seat); every other candidate is OUT (§5, §6), held (§3 partly, §4), or already done (§7).
2. Zero lane coverage of the size-application chain (grep above), versus 11 staged files = one conclusion; the r40 pattern (merge a redundant cluster into one re-grounded successor) fits exactly and reduces, not grows, the package.
3. The substance is public bytes at pinned `v0.56.2`/`efb5099…` (the host's build is the same commit the round-41 fetches use) — verifiable by reading, no socket, no execution; the only private-receipt-dependent claims are the three absence sweeps (r13/r14/r15) which can be re-derived with the allowed read-only journal verb and a recent census.
4. It answers a question the lane's rules already raise (does `size 420 500` become the real window size?) and stays an honest UNK for the one thing the lane may not do (open a gkeep window), so it cannot over-claim.
5. Runner-up: idle/lock public-bytes residue (§3: S234–S236 toggle/refresh/restart scripts, S265/S267 stock config) — small, in province, but the r35 entries already cover its conclusion; do it second, folded into the existing idle files as an amendment, not as new files. Last-place: socket residue (stale/contradicted) and everything in §5–§7 (out or done).
6. Needs before adoption (any theme): renumber S-ids from S283+ (collision, §0); never copy the 7 same-name files; for localized (§5) write a refusal note only.

## 11. Remaining unknowns
- I did not open the staged 65 files' bodies beyond `source:` lines, headers and a few spot reads; the §3/§4 staleness claims rest on titles + the cited first lines, not on a line-by-line diff of staged vs lane text.
- No check of whether a gkeep window exists now (no compositor connection allowed); `hyprctl clients` not run.
- I did not re-open the upstream sources behind S284–S319 (public URLs); verdict that they are "public at v0.56.2" is from the `source:` lines.

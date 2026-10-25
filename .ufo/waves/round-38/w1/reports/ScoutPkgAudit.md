# ScoutPkgAudit — the remainder of the shokuknow `merge/mado/` package

ScoutPkgAudit · round-38 wave 1 · read-only audit of the staged package
`/home/vgpnk/Projects/shokuknow/merge/mado/` (package read-only; lane read-only except this
report).

Package contents, measured (`find merge/mado -type f | wc -l` → **72**):

| what | count | where |
|---|---|---|
| staged register rows | **147** | `merge/mado/SOURCES.append.md` |
| staged knowledge entries (new-file) | **65** | `merge/mado/knowledge/corpus/knowledge/` |
| staged amendments (target files the lane already holds) | **4** | `merge/mado/amendments/corpus/knowledge/` |
| merge report (md + json) | 2 | `merge/mado/MERGE-REPORT.{md,json}` |

`MERGE-REPORT.json` self-reports `accepted: 147`, `refused: []`, `entries: 69`, `existing_rows: 192`,
`first_id: S203`. The `entries: 69` figure matches the tree (65 + 4). `existing_rows: 192` is a
**stale snapshot**: the lane registry at the round-38 base `f6e3247` holds **207** rows, and at HEAD
**211**. That drift is the whole reason the collision list exists (§2).

**Headline.** The landed round-38 ledger is *correct but tiny*: it adjudicates **7 of the package's 69
knowledge entries** and **6 of 147 register rows**. The other **62 entries** and **141 rows** carry no
verdict anywhere in the lane. Of those 62, most are genuine unheld ground the lane's own frontier
names (focus-grab, the Chinese/Japanese literature, the gkeep size chain) — i.e. the package holds
substantially more adoptable material than round 38 considered. But three of the 62 are **not
adoptable as written** and one of them repeats the exact null-channel defect round 38 refused
elsewhere. Details, verdicts and deciding facts below.

---

## 1. Per-item verdicts

### 1.1 The three entries named in the assignment (all three refusals hold)

#### `event-queue-host-measurement-r28.md` — **REFUSE** (upheld)

Deciding fact — the reading is on a **null channel**, verified against upstream v0.56.2 bytes I
fetched this round:

* the two markers are core-logger lines, and the core logger **returns before formatting** when
  logging is off — `src/debug/log/Logger.cpp:15-16` `if (!m_logsEnabled) return;` (same gate in the
  variadic template, `Logger.hpp:22-24`);
* the switch is `src/debug/log/Logger.cpp:48` `m_logsEnabled = !*PDISABLELOGS;` and
  `src/config/values/ConfigValues.cpp:629` `MS<Bool>("debug:disable_logs", "disable logging to a
  file", true)` — **default true**;
* `Logger.cpp:47` `m_logger.setEnableStdout(!*PDISABLELOGS && *PENABLESTDOUT)` and
  `ConfigValues.cpp:632` `enable_stdout_logs` **default false**, so the journal carries no core-logger
  runtime lines either;
* `src/Compositor.cpp:306` `conn->setName("aquamarine")` — the aquamarine backend bypasses the
  switch, which is why the session file carries tens of thousands of aquamarine lines and zero
  core-logger ones.

So a zero marker count is structurally guaranteed, and the entry's own reading ("never overflowed")
cannot be supported by that count — QUALITY criterion 62 (`corpus/QUALITY.md:371`) refuses it.
Second, independent deciding fact: **the entry's own source is gone**. It cites
`/run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792772698_564628331/hyprland.log`;
the host now has only `…_1792804449_426444678` (`ls /run/user/1000/hypr/`), i.e. the cited instance
directory no longer exists.

#### `event-queue-journal-measurement-r29.md` — **REFUSE** (upheld)

Deciding fact — same null channel as above, one step worse for the journal: the unit journal carries
the compositor's **stdout**, and core-logger stdout requires `enable_stdout_logs` (default false)
*and* `!disable_logs` (default true) — `Logger.cpp:47`. The journal's "21 core-logger lines" are the
pre-config-load window only (the round-37 receipt S213 measured exactly that). A zero count of
"overflowed event queue" in that journal proves nothing about the class. The entry's own §2 concedes
the reading is bounded by retention, but the binding defect is the gate, not retention.

#### `socket-client-contract-measurements-r29.md` — **REFUSE** (upheld; reason should be stated as the landed errata states it)

Deciding fact — its two load-bearing numbers conflict with first-party ground re-opened this round:

* **64 KiB**: the committed receipt `fetch/S277.bin:61` reads "Requests are capped at 64 KiB, all
  request readers together share a 128 KiB budget per server pass" — that is **chonkstep's own
  server-side cap**, not upstream's. Upstream declares `static constexpr size_t REQUEST_LIMIT = 1024
  * 1024;` and `FOLLOW_QUEUE_LIMIT = 64 * 1024;` (`fetch/S253.bin:43-44`) — i.e. upstream's request
  ceiling is **1 MiB** and its 64 KiB is the *followed-queue* bound. The entry's framing ("requests
  are bounded at 64 KiB") therefore misattributes a third-party cap to the compositor.
* **0600**: the receipt's `S277.bin:53` says "both sockets are `0600`", while this host's own stat
  receipt `fetch/stat-sockets.txt` measures `755 socket …/.socket.sock` inside a `700` directory — the
  host differs from the third-party's description.

Salvage note for a later round: the entry's §2 *error-vocabulary* claim (hyprctl exiting zero for
`ok` / `Invalid dispatcher` / unknown) is **not** contradicted by first-party ground — upstream
`src/debug/HyprCtl.cpp:1151` does return the fixed string `"Invalid dispatcher"` — but it is a
third-party (tier C) measurement of a synthetic socket and is not admissible as an entry's sole
support. It is a lead, not an adoption.

### 1.2 The fourth refused entry the assignment did not name

#### `socket-modes-and-request-read-r30.md` — **REFUSE** (upheld)

Deciding fact — **stale artefact**: its cited own-work source is the same vanished instance
`_1792772698_564628331` (the entry's `source:` line names the directory path), so its socket-mode
readings cannot be re-read; the modes it reports are re-measured by this round's own stat receipt
(`fetch/stat-sockets.txt` → `700` dir / `755` sockets) and now live in the adopted
`request-socket-live-bound-r8.md` §2 and in row **S258**.

### 1.3 The three adopted entries — verdicts confirmed, one caveat each

| entry | verdict | deciding fact |
|---|---|---|
| `hyprctl-flags-r28.md` | **ADOPT** (landed, row S221) | re-fetched byte-identical: `fetch/S221.bin` sha256 `35046ba0dc1dd1db…` = the row's anchor sha |
| `request-socket-live-bound-r8.md` | **ADOPT** (landed, rows S158 + S187 + S277 + S258) | the five-second bound is upstream's own prose *and* the host's code (`HyprCtl.cpp` `poll(pollfds, 1, 5000)`, `read(…, 1023)`), with the host stat as own-work |
| `request-limits-upstream-r31.md` | **ADOPT** (landed, row S253) | the two constants are verbatim in `fetch/S253.bin:43-44`; the entry correctly states the file 404s at the host's tag (I re-verified: `v0.56.2/src/ipc/s1/Unix.cpp` → **404**) |

Caveat on the third: its upstream ceilings come from a revision **later** than the host runs. The
entry says so; that is the deciding fact for keeping it (upstream-ahead, not host behaviour).

### 1.4 The four `amendments/` files — three refuse, one adopt

The merge report instructs: *"append each amendment to the lane's existing file; do not replace"*. The
lane already holds all four targets, with different, later, lane-authored text. Verdicts are
therefore per-file, on substance.

| amendment | verdict | deciding fact |
|---|---|---|
| `ipc-contract-r25.md` | **REFUSE (no new ground)** | the lane's own `corpus/knowledge/ipc-contract-r25.md` already carries the implementation-side facts the amendment puts in its §3 (`AF_UNIX`/`SOCK_STREAM`, backlog 10, 1024-char truncation — lane `:62-66`) **and** the amendment's §4 version-drift check (lane `:70-78`: "the 0.56.0 page and the current-git page publish the same 44 events"). I re-derived the drift independently: the pinned `ipc/_index.md` at `c04680a` is 6,539 B, sha256 `535bc4c385a06162…`, with 46 `\| ` rows = 44 data rows + header + separator. Its `source:` lines cite **staged** ids (S203/S204/S206) that are not lane ids. |
| `dispatcher-semantics-r25.md` | **REFUSE (duplicate of a held entry)** | the lane's `dispatcher-semantics-r25.md` already holds every OBS the amendment lists — "a dispatcher *describes*; it does not act", the `hl.dispatch()` wrapper requirement, `event( string )`, `force_idle( int )`, the "not recommended with a keybind" warning and the "contents are not guaranteed to be stable" quote — under the lane's own id **S188**, which is the *same upstream file* the amendment cites (same commit `c04680a`, same sha `c830ce07…`). I re-checked the amendment's anchors against upstream: `dispatchers.md:9`, `:14`, `:59`, `:82` all match. Accurate but redundant. |
| `waybar-module-text-route-r25.md` | **REFUSE AS WRITTEN** (the only content worth having is not the amendment's) | the amendment's own anchors and one of its claims do **not** match upstream Waybar 0.15.0, which I fetched: the fallback warning is at `backend.cpp:38` (amendment says `:31`), the 1024-byte buffer at `backend.cpp:115` (amendment says `:88`), the `>` split at `backend.cpp:142` (amendment says `:140`); and the window module registers **five** events — `activewindow`, `closewindow`, `movewindow`, `changefloatingmode`, `fullscreen` at `window.cpp:27-31` — while the amendment claims it "subscribes to two events (S208:25-26)". The markup hand-off it documents (`rewriteString` `:58`, `set_markup` `:64`) is genuinely absent from the lane's thin `waybar-module-text-route-r25.md` and is worth re-grounding as a small delta of its own. |
| `dispatcher-surface-and-request-grammar-r26.md` | **ADOPT (re-grounded)** | this is the one amendment carrying **net-new first-party ground**. The lane's file stops at "§4 What this entry does not claim" and holds none of: the fixed rejection string (`HyprCtl.cpp:1151` `return "Invalid dispatcher";` — the lane has only the *bind*-level "Invalid dispatcher, requested" in `bind-table-r25.md`, a different string from a different file), the batch `;` split that ignores semicolons inside brackets (`HyprCtl.cpp:1319-1324`), the flag-strip before the dispatcher name is compared (`HyprCtl.cpp:2068`, `:2096`), or the Lua wrapper (`HyprCtl.cpp:1131-1132` `return hl.dispatch({})`). All four anchors verified against upstream v0.56.2 bytes. Adopt under lane ids (S018/S158 for `HyprCtl.cpp`, S196 for the 0.56.0 page), not under staged ids. |

### 1.5 The 54 never-adjudicated new-file entries — verdicts by theme

The lane holds **zero** focus-grab rows (`grep -c 'focus_grab\|hyprland-protocols' corpus/SOURCES.md` → 0;
no focus-grab entry in `corpus/knowledge/`), **zero** Chinese/Japanese rows
(`grep -cP '[\x{4e00}-\x{9fff}\x{3040}-\x{30ff}]' corpus/SOURCES.md` → 0), and no gkeep
rendered-geometry entry. So most of this material is unheld ground, not duplication. The decisive
facts per theme:

**T-A — focus-grab cluster (8 entries: `focus-grab-seat-semantics-r8`, `-observed-semantics-r9`,
`-focus-selection-r10`, `-mouse-target-r11`, `-whitelist-admission-r12`, `-keyboard-routing-r13`,
`-protocol-live-on-host-r14`, `-has-no-client-here-r15`) → DEFER-ROUND-39, and note that 2 of the 8 are
not adoptable as written.**

Deciding facts: the upstream sources re-fetch **200** today — `hyprland-focus-grab-v1.xml` (5,447 B)
and, at the host's own tag, `v0.56.2/src/protocols/FocusGrab.cpp`, `FocusGrab.hpp`,
`src/managers/SeatManager.cpp` (all 200). The cluster answers the lane's own open F1 item (per-window
rule effects / focus dispatch). Two of them are defective as written:
`focus-grab-observed-semantics-r9` and `focus-grab-has-no-client-here-r15` lean on **campaign-internal**
receipts (`lanes/mado/round9/fetch/host-compositor-log-scan.txt`,
`lanes/mado/round15/fetch/host-focus-grab-client-sweep.txt`) that do not exist in the lane repo — they
must be re-taken into a lane wave before they can be cited; and the "no client here" sweep is a
*binary-string census*, i.e. a negative that the lane's own QUALITY 62 discipline treats as needing a
positive probe. `focus-grab-protocol-live-on-host-r14` is sound (its host journal receipt is cited as
a lane-local artefact and its upstream sources are pinned).

**T-B — literature cluster (5 entries: `compositor-focus-manipulation-literature-r26`,
`privileged-client-surface-r29`, `wayland-input-security-literature-r8`,
`two-literature-coverage-r25`, `two-literature-drift-r26`) → DEFER-ROUND-39 (a literature round).**
Deciding fact: these are the only tier-B/C literature rows the package offers, and the lane's F2
asks for a second academic source — the lane's registry holds three `paper` rows, all mutation-testing
(S183, S184, S211), none on Wayland/compositor security. I re-fetched: arXiv 2604.18860 → 200 with the
title "Temporal UI State Inconsistency in Desktop GUI Agents…" (DOI-bearing), the mupuf 2014 Wayland
security record → 200, the DFRWS/Forensic Science International article via the reader proxy → the
package's sha256 prefixes (`1dab3c20…`, `6cd966f4…`) are quoted but I did not re-fetch those two
CSDN pages directly (see T-C).

**T-C — Chinese/Japanese coverage (10 entries: `chinese-article-revision-r30`,
`chinese-hyprland-window-rules-r16`, `chinese-ipc-framing-absence-r13`,
`chinese-translation-drift-r31`, `chinese-wiki-canonical-url-r28`, `chinese-wiki-ipc-section-r7`,
`chinese-wiki-revision-list-r7`, `cn-framing-coverage-r8`, `japanese-counted-comparison-gone-r15`,
`japanese-input-observation-methods-r14`, `japanese-wayland-compositor-account-r16`,
`window-size-read-in-chinese-r16`, `zh-wiki-snapshot-semantics-r29`) → split verdict.**

* **ADOPT-CANDIDATE (tier B, fetchable):** the Chinese ArchWiki **via the community's own offline
  package** (staged S212, `mirror.sjtu.edu.cn/…arch-wiki-docs-zh-cn-20260901-1…pkg.tar.zst` → **200,
  8,575,462 B**), the **archlinuxcn API** (staged S221/S222/S260/S261/S281/S322 → **200, 30,942 B**),
  and the **ArchWiki English pivot** (staged S215 → **200, 36,293 B, sha256
  `7f6b2e4352b13457…`** — exactly the staged anchor's sha and byte count, so that row is byte-verified
  today). The Japanese ArchWiki rows (staged S209, S344-S346) → `wiki.archlinux.jp` **200, 137,003 B**.
* **REFUSE (two rows):** staged **S216** (`blog.csdn.net/2301_76324845/…`) and **S217**
  (`blog.csdn.net/lxyoucan/…`) name canonical CSDN URLs that answer **HTTP 521** to a plain client
  *today* (verified twice), and the campaign's own `lanes/mado/REJECTIONS.md` items 6 and 7 rejected
  exactly these two posts as "not personally openable … cannot back a row"; they were re-admitted in
  round 2 only through a reader proxy, which the row's `used-by` does not disclose. The staged row's
  recheck command says "re-fetch through the reader proxy" while the `source:` cell names the direct
  URL — the citation and the recheck disagree. **Verdict: refuse as row sources** (tier-C lead at
  best, and the lane's REJECTIONS still stand).
* **REFUSE (one row):** staged **S348** is `blog.csdn.net/gitblog_01188/…` — the campaign's own
  REJECTIONS item 4 rejects the `gitblog_*` class as AI-generated with no version pin. A staged row
  built on it contradicts the campaign's own record.
* The remaining Chinese/Japanese rows are fetchable today but rest on tier-C blogs: keep as leads.

**T-D — gkeep size-chain cluster (8 entries: `gkeep-geometry-unobservable-r8`,
`gkeep-rendered-geometry-chain-r9`, `gkeep-size-rule-application-r10`,
`gkeep-size-to-real-size-r11`, `gkeep-client-size-request-r12`,
`gkeep-rendered-geometry-record-r13`, `gkeep-rendered-geometry-record-r14`,
`gkeep-geometry-never-recorded-r15`, plus `gkeep-element-rules-r30`, `glyph-and-geometry-r31`) →
split verdict: 6 DEFER-ROUND-39, 2 REFUSE-AS-WRITTEN.**

Deciding fact for the 6 code-reading entries: they read upstream v0.56.2 code
(`src/desktop/view/Window.cpp`, `WindowRuleApplicator.cpp`, `src/layout/target/*`,
`DefaultFloatingAlgorithm.cpp` — all re-fetch 200) and the lane holds **no** gkeep geometry entry
(gkeep appears in the lane only in `config-drift-r12.md` and `rule-attribution-r24.md`). Their own-work
rows cite campaign-internal `lanes/mado/roundN/fetch/…` artefacts, so they need in-lane re-fetch.
**The 2 to refuse are `gkeep-rendered-geometry-record-r13` and `-r14`**: they measure the compositor's
"never wrote a window size" by counting the `Map request dispatched` line — and that line is
`Log::logger->log(Log::DEBUG, "Map request dispatched, …")` at `src/desktop/view/Window.cpp:2515`, i.e.
**through the same core logger the round-38 refusals just turned off**. Their proposed positive
control, `Refocused popup parent window`, is likewise a `Log::DEBUG` line
(`src/managers/SeatManager.cpp:741`) — so their own control is zero for the same reason and proves
nothing. This is QUALITY 62's exact failure mode, reproduced in a package entry the round did not
examine. The `gkeep-element-rules-r30` / `glyph-and-geometry-r31` rows read host files under
`~/.config/hypr/` and `~/Projects/gkeep/` — re-take in-lane.

**T-E — idle-lock / omarchy / bar-producer cluster (≈21 entries: `idle-lock-intent-mechanism-r8`,
`-intent-surface-r9`, `-intent-surfaces-r10`, `-journal-evidence-r11`, `-runtime-state-r28`,
`idle-toggle-and-daemon-lifecycle-r29`, `host-idle-lock-chain-r7`, `host-bar-and-idle-binding-r26`,
`host-bar-producers-r28`, `host-producer-outputs-r29`, `host-producer-current-outputs-r30`,
`host-request-socket-cap-r7`, `uwsm-app-daemon-unit-r7`, `weather-glyph-render-r7`,
`update-check-and-app-lifecycle-r31`) → mostly REFUSE as duplicate-of-held or stale-premise; a few
DEFER-ROUND-39.**

Deciding facts, one per sub-family:

* **REFUSE (duplicate of lane-held, same subject):** the lane already holds its own
  `idle-lock-chain-armed-r14.md`, `idle-lock-never-asked-r12.md`, `idle-lock-offered-in-the-bar-r15.md`
  (round-35/36, lane-authored, own receipts `S205-S210`) and the idle-lock plane/route notes. The
  package's `idle-lock-intent-*` and `idle-lock-journal-evidence-r11` are earlier rounds of the same
  investigation whose conclusions the lane's entries already carry.
* **REFUSE (stale premise):** `idle-lock-runtime-state-r28`'s headline is "the daemon is **not
  running**". On this host right now `pgrep -x hypridle` **finds hypridle running**, and the lane's own
  held entry says the idle lock is armed. The package's own later entry `host-idle-lock-chain-r7`
  already contradicts it ("one `pgrep -x hypridle` returning nothing. This round finds it running").
* **REFUSE (superseded by the adopted pair):** `host-request-socket-cap-r7` ("the request ceiling on
  this host is no ceiling at all") is exactly the content the adopted
  `request-socket-live-bound-r8.md` §1 and `request-limits-upstream-r31.md` now hold — the 404 of
  `src/ipc/s1/Unix.cpp` at the host tag is stated in the adopted entry, and the 1023-byte chunk
  accumulation with no total bound is in `request-socket-live-bound-r8.md` §1. No new ground.
* **DEFER-ROUND-39 (genuine gap, but version-pinned and campaign-sourced):** `host-bar-producers-r28`,
  `host-producer-outputs-r29`, `host-producer-current-outputs-r30`, `weather-glyph-render-r7`,
  `update-check-and-app-lifecycle-r31`, `uwsm-app-daemon-unit-r7` — these read the host's own
  `~/.config/waybar/`, `~/.local/bin/` and omarchy payloads, which the lane holds only partially
  (S085-S097 are omarchy v3.8.4 payloads; the lane has no row for the indicator scripts the package
  cites). Note the version detail: the package pins omarchy **v3.8.4** while the host reports
  **3.8.3** (`~/.local/share/omarchy/version`), yet the four omarchy files I hashed
  (`default/waybar/indicators/idle.sh`, `bin/omarchy-toggle-idle`, `bin/omarchy-system-lock`,
  `config/hypr/hypridle.conf`) are **byte-identical** between the host copy and upstream v3.8.4 — so the
  pin is safe for those files, but the version string differs and must be recorded as such.
* **REFUSE (host fact that the lane already holds):** `idle-lock-runtime-state-r28` and
  `idle-toggle-and-daemon-lifecycle-r29` both rest on the same "daemon not running" premise above.

### 1.6 The four same-name-as-lane-held new-file entries

`event-delivery-limits-r26.md`, `idle-lock-chain-armed-r14.md`, `idle-lock-never-asked-r12.md`,
`idle-lock-offered-in-the-bar-r15.md` — the package ships files with the **same names** as lane-held
entries but different text (the package's r2/r12/r14/r15 campaign versions). **Verdict: REFUSE** —
the lane's versions are later and lane-authored (`event-delivery-limits-r26.md` was re-grounded in
round 37; the idle-lock trio in round 35), and copying the package copies would overwrite lane text
with older campaign text. The merge report's own `## Adopt checklist` step 5 covers only the
`amendments/` tree; these four sit in `knowledge/` and would be clobbered by a bulk copy.

---

## 2. The 15 collisions S203–S217 — **VERIFIED REAL held ids**

Command as specified by the assignment, run in the lane at HEAD:

```
$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin grep -c '| S20x |' -- corpus/SOURCES.md
S203 -> corpus/SOURCES.md:1
S204 -> corpus/SOURCES.md:1
…  (all fifteen)  …
S217 -> corpus/SOURCES.md:1
```

* **15/15 real**: every one of S203–S217 has exactly **one** registry row in `corpus/SOURCES.md`,
  at HEAD *and* at the round-38 base `f6e3247` (same counts at both revisions — the rows predate the
  round).
* **The ledger's collision set is exactly right for the base**: `collisions` (15) ==
  `reg-ids ∩ staged-ids`, and `reg-ids` (207) == the base registry's 207 ids, set-equal. Nothing
  extra, nothing missing.
* **The collision is by id number, not by document** — and this is the part the merge report and the
  lesson each get half-right. The staged rows S203–S217 are the campaign's round-1/round-2 rows for
  ipc-contract / dispatcher / waybar / two-literature entries; the **lane's** S203–S217 are a
  different family entirely (host omarchy first-run installer, host idle-lock chain, host waybar
  config, the Lipsitch negative-controls row, Waybar workspaces module, host log channels, Hyprland
  core logger / config values / Compositor init / logger interface). Same number, disjoint document.
  The merge report's separate table — *"Rows whose source the lane's registry already holds"* — is the
  **document** relation (staged S203 ≡ lane S186, etc.), and that table is itself incomplete: it lists
  8 rows and omits **staged S214 ≡ lane S212** (both "Waybar 0.15.0 Hyprland workspaces module",
  same URL) which my URL match finds.
* **The collision file is stale relative to HEAD.** At HEAD the lane holds 211 ids, and
  `lane_ids ∩ staged_ids` = **19**, not 15: the round's own four adopted ids (S221, S253, S258, S277)
  are also staged ids. Three of them are harmless because the id follows the document (staged S221 ≡
  lane S221 = the 0.56.0 hyprctl page; staged S253 ≡ lane S253 = `Unix.cpp`; staged S277 ≡ lane S277 =
  the chonkstep document, whose repo was renamed `iconidentify/chonkstep` → `chriskearney/chonkstep`,
  same bytes sha256 `ff561fe0…`). **One is a genuine collision the file does not record**: staged
  **S258** is the English ArchWiki drift document (`used-by` the unadjudicated
  `chinese-translation-drift-r31.md`), while lane **S258** is this round's own host stat receipt —
  same id, disjoint documents. The lesson prose does flag this (*"A 16th id clash is unrecorded yet"*),
  but `assimilation/collisions` itself still says 15.

---

## 3. The staged register (147 rows) — **REFUSE the bulk append; adopt row-by-row by document**

`SOURCES.append.md` is a valid *candidate list* and an invalid *append*. Deciding facts, all measured:

1. **Schema break — 33 of 147 rows are not 11-column rows.** Their `recheck`/`anchor` cells contain an
   unescaped `|` (e.g. staged S317's recheck embeds a `grep -c '…' | wc -l`-style pipeline; staged
   S267 splits into 13 cells). The lane's own registry has **0** rows that fail this
   (`211 rows, 0 with != 11 columns`).
2. **The fleet census validator rejects the append.** I copied the lane registry to a sandbox and
   appended the 147 staged rows, then ran the fleet's own
   `scripts/sources-census.sh validate`:
   * baseline, lane repo as-is → `ok`, exit **0**, only `W01×1` and `W04×7`;
   * sandbox with staged rows → exit **1**, with **E01×33** (malformed row, fields=12/13), **E03×19**
     (duplicate id — the 15 collisions plus the 4 ids the round itself took), **E04×2** (duplicate URL
     *within* the same scope), **E09×58** (invalid recheck — a prose sentence instead of a bare ISO
     date / `NNd` / symbolic cadence), **E11×137** (used-by path missing on disk), **W01×8**,
     **W04×26**. Attribution by staged id: E01 33, E03 19, E04 2, E09 58, E11 137, W01 8, W04 26 — all
     from staged rows.
3. **137 of the rows point at entries that do not exist in the lane** (E11), because 62 of the 69
   entries they name were never adjudicated.
4. **The register's ids are round-scoped, not document-scoped.** `lanes/mado/ID-REMAP.md` states it:
   *"the same id in two rounds names two different rows, so a round-blind substitution would move one
   round's citations onto another's rows while every structural check stayed green."* The lane's own
   rule is the opposite — ids follow documents (`registration.md`: *"ids follow documents, never
   arithmetic"*). Appending the register wholesale would import a round-blind id space.
5. **Rows whose used-by names only refused entries are only 4 of 147** (staged S226, S242, S243, S252).
   The lesson's sentence *"the staged register is left unassimilated (its rows covered only the refused
   entries)"* is therefore wrong as a description of the file: 143 rows name entries that are not
   refusals.

**Verdict.** Do not append `SOURCES.append.md`. Adopt from it **row-by-row, by document, under lane
ids, with lane-local receipts** — which is exactly what round 38 did for the four rows it used
(S221→S221, S272→S158, S276→S187, S277→S277, S253→S253, own-work→S258). The register is a
*candidate queue*, not an append.

---

## 4. Ledger completeness — what is recorded and what is not

Recorded in `corpus/lessons/round-38.md` §"Assimilation ledger" (10 table rows) plus
`.ufo/waves/round-38/assimilation/` (reg-ids 207, staged-ids 147, collisions 15,
quarantine-slice 13 rows).

### 4.1 Coverage

| item | total in package | adjudicated in the ledger | unadjudicated |
|---|---|---|---|
| knowledge entries (65 new-file + 4 amendments) | **69** | **7** (3 adopt + 4 refuse) | **62** |
| — of which: same-name-as-lane-held (duplicate of held text) | 4 | 0 (implicit refuse) | 4 |
| — of which: genuinely unheld ground (focus-grab, literature, CJK, gkeep, omarchy/host) | 54 | 0 | **54** |
| — of which: amendments (4) | 4 | 0 | 4 |
| register rows | **147** | 6 (the four adopted + S272/S276 re-points) | **141** |
| collisions | — | 15 (correct at base; 19 at HEAD) | 4 missing at HEAD |
| quarantine rows | 13 | 13 (carried over verbatim) | 0 |

### 4.2 Internal inconsistencies found in the landed ledger

1. **Prose/table mismatch.** The lesson header says *"Staged table: **5** knowledge entries + register +
   147-row `SOURCES.append` … adopts the three usable knowledge entries and refuses the other
   **three**"* — the table underneath has **10** rows: 6 adopt rows and **4** refuse rows. And the
   package stages **69** entries, not 5. The number that describes the package is 69; the number that
   describes this round's work is 7.
2. **Two of the four "refuse" rows are round-37 decisions repeated**, not round-38 findings:
   `event-queue-host-measurement-r28` and `event-queue-journal-measurement-r29` were refused in the
   round-37 lesson (M37-2). Re-listing them is harmless but inflates the ledger's apparent reach.
3. **The collisions file is base-scoped** (§2): 15 at the base, 19 at HEAD; one of the four additions
   (staged S258) is a true document-disjoint clash.
4. **The quarantine slice is a byte-identical copy of round 37's** (`diff .ufo/waves/round-37/assimilation/quarantine-slice
   .ufo/waves/round-38/assimilation/quarantine-slice` → identical). Three of its 13 ids — **S195, S199,
   S200** — exist in **neither** the lane registry nor the staged register (they are round-1 pre-remap
   ids per `ID-REMAP.md`), and eight of them name *staged* ids that were never adjudicated. The slice
   therefore mixes three id spaces (lane ids, staged ids, dead pre-remap ids) with no marker.
5. **The register-disposition sentence is factually wrong** (§3, item 5): only 4 of 147 rows name
   refused entries, not "its rows covered only the refused entries".
6. **The merge report's own duplicate table is short by one row**: it lists 8 "rows whose source the
   lane's registry already holds" and omits staged S214 ≡ lane S212 (Waybar workspaces module).
7. **The merge report's `existing_rows: 192` is a stale snapshot** (base = 207, HEAD = 211), which is
   the upstream cause of the collision set.

### 4.3 What the ledger gets right (worth keeping)

* The four adopted rows are re-grounded, not copied: each carries a lane-local receipt under
  `.ufo/waves/round-38/fetch/` whose sha256 matches the row anchor — S158 `798b7c6c…`, S187
  `136e5511…`, S221 `35046ba0…`, S253 `3ba8e461…`, S277 `ff561fe0…`, plus `stat-sockets.txt`
  `fcc60820…`. All six recomputed here from the committed bytes and they match.
* The refusals carry **reasons that survive re-derivation** (§1.1): the null-channel argument holds
  against upstream v0.56.2 source I fetched this round, and the 64 KiB/0600 conflicts hold against
  the committed S253/S277 receipts and this round's stat receipt.
* The lesson's own errata (commit `06d1188`) already corrected the 64 KiB attribution to
  "chonkstep's own request cap (S277 `:61`), not upstream's follow-queue bound" — that is the right
  statement, and `request-limits-upstream-r31.md` carries it.
* The `assimilation/renumber-map.md` pattern from round 37 (id ← document, with byte digests) is the
  right mechanism and round 38 applied it to the rows it took.

---

## 5. "Anything else present" — `scripts/`, `reports/`

* **The merge package contains no `scripts/` and no `reports/` directory.** `find merge/mado -type d`
  returns exactly `.`, `./amendments`, `./amendments/corpus`, `./amendments/corpus/knowledge`,
  `./knowledge`, `./knowledge/corpus`, `./knowledge/corpus/knowledge` — no other tree.
* The **campaign staging tree** `/home/vgpnk/Projects/shokuknow/lanes/mado/` has eight top-level
  deliverables (`DOMAIN.md`, `CHANNELS.md`, `SOURCES-PROPOSED.md`, `KNOWLEDGE-PROPOSED.md`,
  `SEARCH-LOG.md`, `REJECTIONS.md`, `CANNOT-ANSWER.md`, `ID-REMAP.md`) plus 16 `roundN/` directories
  holding `fetch/` byte-copies and `.deepresearch/` workspaces. The `.sh`/`.py` files under
  `roundN/fetch/` are **upstream byte-copies** (omarchy indicator scripts, the
  `arch-wiki-docs-zh` converter tree, `api.py`, `build-zh.py`) — evidence for rows, not lane
  instruments. None is adoptable as a lane tool; nothing there should enter `corpus/`.
* The lane's own `tools/` (9 tools) and `reports/` (9 auditor/verifier notes) are untouched by the
  package: the package carries no tool and no report.
* **One inconsistency worth carrying back to the campaign:** the package's `used-by` cells name
  **campaign-internal** paths (`lanes/mado/roundN/fetch/…`) in 26 of the 65 new-file entries. Those
  paths do not exist in the lane repo, so any future adoption of those entries must re-take the
  own-work receipt into a lane wave (`E11` in the census sense).

---

## 6. Bottom line for the ledger

| verdict | item | deciding fact (one line) |
|---|---|---|
| REFUSE (bulk) | `merge/mado/SOURCES.append.md`, 147 rows | 33 rows break the 11-column schema; census validate goes 0 → 1 with E01×33, E03×19, E09×58, E11×137; ids are round-scoped, not document-scoped |
| ADOPT row-by-row | the 6 rows round 38 used | receipts present, digests match, ids follow documents |
| REFUSE | `event-queue-host-measurement-r28.md` | null channel (`debug:disable_logs` default true, `Logger.cpp:15/48`) + cited instance dir gone |
| REFUSE | `event-queue-journal-measurement-r29.md` | same null channel; journal carries no core-logger lines (stdout gated, `Logger.cpp:47`) |
| REFUSE | `socket-client-contract-measurements-r29.md` | 64 KiB is chonkstep's own cap (S277:61), upstream says 1 MiB (S253:43-44); 0600 vs this host's measured 0755 |
| REFUSE | `socket-modes-and-request-read-r30.md` | cited own-work source is the vanished instance dir; modes re-measured by S258 |
| ADOPT (re-grounded) | `amendments/dispatcher-surface-and-request-grammar-r26.md` | four first-party facts the lane does not hold (`HyprCtl.cpp:1151`, `:1319-1324`, `:2068/:2096`, `:1131-1132`) |
| REFUSE (no new ground) | `amendments/ipc-contract-r25.md`, `amendments/dispatcher-semantics-r25.md` | the lane's own files already carry the same facts under lane ids |
| REFUSE AS WRITTEN | `amendments/waybar-module-text-route-r25.md` | anchors wrong (`:31`→`:38`, `:88`→`:115`, `:140`→`:142`) and "two events" wrong (five, `window.cpp:27-31`) |
| REFUSE (duplicate of held) | 4 same-name-as-lane-held `knowledge/` files | bulk copy would overwrite later lane-authored text |
| REFUSE AS WRITTEN | `gkeep-rendered-geometry-record-r13/-r14.md` | "Map request dispatched" is a core-logger DEBUG line (`Window.cpp:2515`); their own control is a DEBUG line too (`SeatManager.cpp:741`) → QUALITY-62 null channel |
| REFUSE as row sources | staged S216, S217, S348 | direct CSDN URLs answer HTTP 521 today; the campaign's own REJECTIONS reject them and the `gitblog_*` class |
| DEFER-ROUND-39 | 54 unheld-ground entries + 4 amendments | focus-grab, Wayland/compositor literature, Chinese/Japanese coverage, gkeep code chain, omarchy/bar producers — real gaps, but need lane-local receipts and lane ids |
| VERIFIED | collisions S203–S217 | 15/15 real held ids, exactly `reg ∩ staged` at base; 19 at HEAD, one true clash (staged S258) |

**Tooling:** none installed this round; every check used what the machine already had
(`git`, `curl`, `python3`, `bash`, the fleet's `scripts/sources-census.sh`). Scratch under
`/tmp/mado38-ScoutPkgAudit/`; the lane repo was not modified except for this report.

**Limits of this audit.** I did not re-fetch the two CSDN posts through the reader proxy (so S216/S217
have no byte-level confirmation of their quoted text — only a direct-fetch 521 and the campaign's own
REJECTIONS entries). I did not re-verify the digests of the 26 campaign-internal fetch artefacts the
package cites, because those files live in the campaign tree, not the lane repo. I did not re-open every
one of the 54 unadjudicated entries line by line; their verdicts rest on (a) lane-registry coverage
checks by subject and URL, (b) reachability of their upstream sources today, and (c) the channel/anchor
defects identified above.

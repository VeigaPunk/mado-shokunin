# Round 56 — mado lesson (hyaku run 11, attempt 1)

Base `13f0acbe3a15da2d9c08357a576d91dcadc85273`. Claims frozen at `3423ae28` (v1) and re-registered pre-data at `323a69c9` (v2; errata E12-E14 `15015e77`).
Three claims: **C1 coverage** (sourced entry `knowledge/hyprland-config-autoreload-r56.md`, rows S383-S395), **C2 operability** (capability `tools/mado-watchplan.py`),
**C3 registry back-reference consistency** (calibration axis; token level, 24 reviewed exemptions; it measures the lane's registry against the lane's entries, not
confidence). Shape: two v1 waves, w1 43 + w2 35 = 78 seats (see the report). Wave evidence: `.ufo/waves/round-56/`.

## Gate

### Admitted

- **Rows S383-S391**, tier A except S390 (man page, tier B), `mined`, opened 2026-10-28, each re-fetched by an independent scout in wave 2
  (`w2/R56W2ScoutRows1..5.md`: sha256 equal to the anchor cell and to the frozen table for S383-S390; S391 matched the committed pin and has no frozen
  hash, see M56-9). URLs, access date 2026-10-28 and located quotes (<=25 words; pin line numbers):

  | row | URL | located quote |
  |---|---|---|
  | S383 | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/inotify/ConfigWatcher.cpp` | `setWatchList(*PDISABLEAUTORELOAD ? std::vector<std::string>{} : Config::mgr()->getConfigPaths());` (:34) |
  | S384 | `…/src/config/values/ConfigValues.cpp` | `"If true, the config will not reload automatically on save."` (:492) |
  | S385 | `…/src/config/supplementary/propRefresher/PropRefresher.cpp` | `if (m_propsTripped & REFRESH_CONFIG_WATCHER)` (:148) |
  | S386 | `…/src/managers/eventLoop/EventLoopManager.cpp` | `wl_event_loop_add_fd(m_wayland.loop, FD.get(), WL_EVENT_READABLE, configWatcherWrite, nullptr);` (:128) |
  | S387 | `…/src/config/legacy/ConfigManager.cpp` | `"source= skipping directory {}", value);` (:1844) |
  | S388 | `…/src/helpers/MiscFunctions.cpp` | `static const char* const ENVHOME = getenv("HOME");` (:65) |
  | S389 | `…/src/debug/HyprCtl.cpp` | `if (COMMAND.contains("misc:disable_autoreload"))` (:1223) |
  | S390 | `https://man7.org/linux/man-pages/man7/inotify.7.html` | `File opened for writing was closed.` (:186) |
  | S391 | `…/src/config/supplementary/propRefresher/PropRefresher.hpp` | `REFRESH_CONFIG_WATCHER     = (1 << 8),` (:18) |

  S392-S395 are supplementary same-URL rows (new ids) whose anchors cover the E-row lines the wave-2 anchor check found outside S383, S387, S388 and S389:
  S392 `ConfigWatcher.cpp:106`, S393 `MiscFunctions.cpp:66`, S394 `HyprCtl.cpp:1190`, S395 `ConfigManager.cpp:630,1838,2134` (append-only registry, CORPUS rule 2).
- **Entry** `knowledge/hyprland-config-autoreload-r56.md`: 30 K rows, 3 H rows, 9 E rows (E01-E09). Nine row propositions were corrected after the wave-2 sentence-to-pin
  audits (K01, K05, K07, K08, K14, K16, K18, K21, K27) and seven E rows (E01-E07, E09); the prose corrections are listed under "Wave-2 findings applied".
- **QUALITY criterion 107** (M56-1), landed as text with a named draft instrument; see M56-1 and the enforcement paragraph in `QUALITY.md`.

**QUALITY 17 distinct-scope review (the new rows repeat held URLs; census W04):** S384 (`ConfigValues.cpp:492` misc option) is a different scope from S215 (`:629,632` debug
defaults) and S318 (`:271-279` input keyboard options). S387 (`ConfigManager.cpp:776,1070,1079-1080,1816,1835-1844`: watcher callback, path list, source handling) differs from
S303 (monitor keyword handler), S317 (device category), S162 (window-rule parsing) and S353/S368 (bind and dispatcher paths). S388 (`MiscFunctions.cpp:65,68` absolutePath) differs
from S321 (device name helper) and S182. S389 (`HyprCtl.cpp:1223,1276`) differs from S158, S307, S320, S366. S392-S395 re-state S383/S387/S388/S389 for three lines each; they
exist only to cover E rows and carry no new claim. Verdict: distinct scopes; W04 is the right code.

### Rejected (reasons stay; flip conditions named)

- **Mechanical `used-by` fill of the 24 name-only pairs** (`c3-name-only.tsv`): each entry names the id to refute, supersede, redirect or disclaim it, so a back-reference would record
  reliance the text denies (`w1/R56CritCiteDef.md` section 2, `w1/R56RevC3Contract.md` section 2). One reader's label, or both: the allowlist is the union of two independent readers; it is
  frozen, disclosed and open to the non-author closure. **Flip:** a closure reading of a pair as reliance moves it into the fill set (a registry `used-by` edit).
- **"The Lua configuration provider and hyprlang parser grammar as sourced here"**: not admitted as K/E rows. The hyprlang grammar is held by the round-46 pin only
  (`w2/R56W2RevProseLimits.md` F6); the Lua provider is not pinned. **Flip:** a pinned `ConfigManager.cpp`/`Jeremy.cpp` at the host tag and a hyprlang tag row.
- **The inotify lab as evidence of Hyprland behaviour**: `w1/R56ScoutInotifyLab.md` observed kernel events with Hyprland's masks on kernel 7.2.11; it is not a Hyprland observation.
  The entry cites it as the kernel plane only. **Flip:** a run that watches the compositor's own reload (not done: no reload was triggered).
- **A frozen K row for `REFRESH_ALL` membership**: not frozen (the declaration was outside the pins). It is entry rows E08/E09 with row S391 (added at integration; M56-9).

### Outside spot-check (pending the non-author closure)

Ready for it: admit S383 (quote at :34), S390 (man page, tier B, rechecked 90d) and S391; narrow-admit S387 (the callback and source handling only); reject the 24 mechanical
back-references (allowlist) and the reading of the lab as a Hyprland observation. Wave-2 seats (all lane-dispatched) re-fetched upstream bytes for every row and found no byte
mismatch; none is an independent verifier. Four allowlist pairs are disputed between the two wave-1 readers (one labelled them reliance or leaning reliance); the closure should adjudicate.

## Registry changes old→new

- Rows `319 → 332` (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`): new ids S383-S395 (13 rows); no row removed; no cell other than cell 11 (`used-by`) of an existing row changed.
- `used-by` of 23 existing rows gained 41 entry paths (comma-separated; the first integration joined with spaces and the census reported E11, M56-6). Full old→new table:
  `.ufo/waves/round-56/receipts/used-by-old-to-new.md`. Every new row S383-S395 lists `corpus/knowledge/hyprland-config-autoreload-r56.md`.
- `status`/`recheck` unchanged on existing rows.

## Mistakes

- **M56-1 — a registry anchor did not cover the quoted line (mined from round 55).** Class `scope`. Evidence: round-55 K14 (S318 anchor `ConfigValues.cpp:271-279`, quoted line 280) and K17 (S052 anchor ends at
  :2699, quoted :2741) were admitted while the registry row's anchor did not contain the quoted line (`receipts/scope-replay-r55.txt`: 2 of 18 K rows; `w2/R56W2CritScopeFix/receipts/replay-r55.out`).
  Captured-by: none (`quality/counters/c1-r55-kbd-entry.py` has no leg reading the anchor). Fix: leg `scope:<id>` in the r56 counter (30/30), `echo`/EOF bound, criterion 107 (corrected text),
  and the E-row re-pointing (S392-S395): the all-row-class draft checker reads `rows=39 covered=39 miss=0` on the entry at `b70f6a2c` after the fix, `miss=6` before it
  (`w2/R56W2CritScopeFix/receipts/draft-r56.out`). Able to fail: the same rule fails K14 and K17 on the r55 entry, fails after widening an anchor past EOF, narrowing it below a K row, or dropping the basename.
- **M56-2 — v1 C1 control 8 unsatisfiable as written.** Class `reference-drift`. Evidence: `w1/R56RevC1Contract.md` section 3.1. Captured-by: none. Fix: registration-v2 E1 (required leg `row:K05`).
- **M56-3 — the C2 harness layout leaked the answer key (M55-4 class, again).** Class `vacuous`. Evidence: `w1/R56CritHoldout.md` F1 (a six-line `<display-root>/expected.out` reader scored 18/18 and the hold-out);
  `w1/R56CritControls.md` section 0.2. Fix: staged layout, `ctl/sibling-reader.py`, bwrap (E6, E7). Residual after the fix (`w2/R56W2CritC2Cheat.md`): an embedded lookup of all 26 fixtures passes under bwrap once the hold-out is revealed,
  and without bwrap four more channels are open; the harness now fails closed without bwrap (`--no-sandbox` to override, stderr says `sandbox=none`). The repository's only defence is the unseen-hold-out score of the four wave-1 tools (4 of 4 at 18/18 + 8/8 while sealed; `receipts/holdout-preveal.txt`) and reading the tool's code.
- **M56-4 — the C3 target was gameable and a mechanical fill would record false reliance.** Class `vacuous`/`scope`. Evidence: `w1/R56CritDoNothing.md` (deleting the 65 citation tokens reached TARGET_MET), `w1/R56CritCiteDef.md`
  (about 21 of 65 pairs name-only), `w1/R56RevC3Contract.md` (23 MIS). Fix: registration-v2 §C3-v2 (frozen allowlist, `lost`, `conflict`, `stale`, 9 controls). Residual (`w2/R56W2CritC3Gaming.md`): D1 coordinated deletion of citation and used-by
  for a pair outside the 65 passes; D2 a `source:` line past line 15 is invisible to `dangling`; D9 an honest entry rename reads `lost`; D5 an entry that mentions every id can be filled mechanically.
- **M56-5 — the L1 witness receipt overstated coverage.** Class `overclaim`. Evidence: `w1/R56RevC1Contract.md` section 3.4. Fix: `receipts/witness-v2.txt` states the K-only scope; the v1 sentence stays frozen.
- **M56-6 — `used-by` separator: spaces broke census E11.** Class `landing`. Evidence: census E11 on 23 rows after the first integration (`registration-v2-errata.md` E13). Captured-by: the census only (the counters accept both). Fix: comma separators.
- **M56-7 — the `lost` hash was computed over the wrong pair set.** Class `landing`. Evidence: `registration-v2-errata.md` E12; `w2/R56W2CritFreezeV2.md` F1. Captured-by: the counter failed closed. Fix: the counter was aligned to the frozen 65-pair hash and the errata says so; the written definition in `registration-v2.md` still reads PAIRS(base) (disclosed, not edited).
- **M56-8 — E-row anchors were outside the registry anchors.** Class `scope`. Evidence: `w2/R56W2CritScopeFix.md` item 4 (6 of 9 E rows). Captured-by: none (the counter's scope leg counts K rows). Fix: rows S392-S395.
- **M56-9 — a pin and a row (S391) entered after the freeze with no frozen hash.** Class `landing`. Evidence: `w2/R56W2RevHarmWatch.md` D1, `w2/R56W2CritFreezeV2.md` F3. Captured-by: none. Fix: `receipts/pins-extra.sha256` records the pin hash; the counter's `pin_hash` leg does not cover it. Disclosed.
- **M56-10 — the lane's own review of its prose.** Class `overclaim`. Evidence: the entry stated as fact that a missing target reaches the `inaccessible` return (it ends at the no-match return), that duplicate paths are watched twice (the kernel keeps one watch), that glob order is the C library's collation, that a rename-over leaves a watch behind (the lab saw IN_IGNORED) and that `HOME` unset is undefined behaviour (libstdc++ throws) — `w2/R56W2RevProsePath.md` P13, P24, G02, R06; `w2/R56W2RevProseLimits.md` F1. All corrected in the entry before landing. Captured-by: the wave-2 prose audit only (QUALITY 104's sentence-to-pin audit).

## Wave-2 findings applied and routed

Applied before the final measurement: entry propositions and prose (above), rows S392-S395, README/PROVINCE/SKILL accuracy edits (`w2/R56W2RevDocs.md` F1-F6), the tool's output-injection escaping and read/event budgets (`w2/R56W2Sentinel.md` F2-F4, docstring divergence 8),
the C2 harness fail-closed bwrap check (`w2/R56W2CritC2Cheat.md` D2, `w2/R56W2Sentinel.md` F1) and the C3 harness's early clone removal (F7). Routed to round 57 (planned): kill-power fixtures for the counters and the tool (survivor tables in `w2/R56W2Mut*`), the C3 `lost` scope and rename false positive,
entailment for C1 (a lexical rewrite of all 33 propositions keeps `content=33/33`, `w2/R56W2CritC1Forge.md`), a fresh sealed hold-out for C2, `check-freeze-order.py` blind to the v2 contract files (`w2/R56W2RevHarmWatch.md` D4), and the stale published navigation axis (`check-axis-scores.py`, published 66/66 in round 50).

## Considerthese and assimilation

- `considerthese/2026-10-28.md` proposal 2 (run the session-material gate at tip once and record the count) is the lane's pick (`w1/R56ScoutConsiderthese.md`); its count at the landed tip is recorded in the report. Its removal part is operator-owned.
- Assimilation: none. `/home/vgpnk/Projects/shokuknow/merge/mado/` holds 69 staged entries (15 adopted, 18 refused, 36 unadopted residue) and none concerns config reload, inotify or config sourcing (`w1/R56ScoutAssimilation.md`; `doctrine/` does not exist there).

## Census

Start: `.ufo/waves/round-56/receipts/census-before.txt` → `mado ok`, 319 rows, exit 0. End: `receipts/at-final.txt` (`mado ok`, exit 0, 332 rows).

## Attempt 2 (2026-10-30 re-dispatch) — wave w3 settled

The run-11 operator wrap-up (2026-10-28 23:35) stopped attempt 1's wave 2 mid-flight; the
claims were released without a closure (`wrapup-release lane=mado round=56 :: honest-stop
(operator wrap-up run 11); no closure; next stays 56` in
`~/.local/state/shokunin-hyaku/events.log:2893`) and the orchestrator re-dispatched round 56
on 2026-10-30. The frozen claims (v2) ran unchanged. Attempt-2 self-verification at the
inherited tip `0f3a5436`: all three frozen gates green
(`.ufo/waves/round-56/receipts/attempt2-l1.txt`), census `mado ok` exit 0 at 332 rows
(`receipts/census-before-a2.txt`).

Wave w3 (one v2 wave, band 64-128): 64 seats dispatched, all 64 settled
(`w3-results.json`); 58 seat reports on disk under `.ufo/waves/round-56/w3/`; six seats
settled without a report file (`R56W3ExecSessionMaterial` aborted before any gate run;
`R56W3MutC3Counter`, `R56W3MutBwrapChannels`, `R56W3CritC2Cheat`, `R56W3CritC1Grammar`,
`R56W3CritHarnessC1` mid-work) — their preserved artifacts stay in `w3/`, their items are
marked unverified in the round report, and no seat was replaced (orchestrator recovery
boundary). Seat-role mix and the dead-seat table are in the report.

## Gate (attempt 2)

### Admitted

- **Rows S396, S397** (mined; `used-by` = this lesson, which cites them below). URLs, access
  date 2026-10-30, and located quotes (raw pin lines; ≤25 words):

  | row | URL | located quote |
  |---|---|---|
  | S396 | `https://man7.org/linux/man-pages/man2/inotify_add_watch.2.html` | `already being watched (perhaps via a different link to the same` (pin line 93; line 94 completes: `object), then the descriptor for the existing watch is returned.`) |
  | S397 | `https://man7.org/linux/man-pages/man5/proc_pid_fdinfo.5.html` | `Each of the lines beginning with "inotify" displays information` (pin line 160; field definitions at lines 164, 166, 168-169, 171-172) |

  Pins: `.ufo/waves/round-56/fetch/man7-inotify_add_watch.2.html` (11,345 B, 258 lines,
  sha256 `98fe7feb381fa2687e8a3962e6d78a49cb1ad07c543f93449dcb42d6712c3d6d`, page footline
  2026-02-08) and `.ufo/waves/round-56/fetch/man7-proc_pid_fdinfo.5.html` (14,694 B, 366
  lines, sha256 `f9e12387bf013d7c016f0015de5801932022a2fe6786d53e1cc84c385952d8a1`, footline
  2026-07-18), both Linux man-pages 6.19. Three independent fetches (L1 + `R56W3RevLessonGate`
  + `R56W3ScribeRegistryA2`) agree byte-for-byte. `R56W3RevLessonGate` audited the draft and
  ruled ADMIT-WITH-EDITS; the edits are applied (below). `R56W3ScoutNewSrc1`/`ScoutNewSrc2`
  re-opened both sources independently and agree on substance.

### Re-applied drafts (rejected as drafted, landed corrected)

- The draft state `queued` + `used-by —` for both rows: rejected — this lesson cites the
  rows, so the CORPUS-true state is `mined` with this file in `used-by`
  (`R56W3RevLessonGate`; the frozen C3 counter's `USED_BY` regex sees only
  `corpus/knowledge/*.md`, so lesson paths are invisible to it — proven by
  `w3/R56W3ExecProbeC3NewRows/receipts/c3-newrows-a2.txt` case B and the L1's own probe at
  scratch revs `6c7cc56d`/`b271ee45`; a disclosed measurement boundary, not an obstacle).
- The draft Gate quotes (de-tagged HTML, not byte-substrings of the pins — `R56W3ScoutNewSrc1`
  D2): replaced with the raw pin lines above.
- The draft anchor dates (both rows carried S390's `2026-02-14`): re-dated from each page's
  own footline (`2026-02-08`, `2026-07-18`) — `R56W3ScoutNewSrc1` D1.
- S396's unqualified one-watch claim: qualified with "within one inotify instance" and the
  anchor widened to `88-94` (`R56W3RevLessonGate`).

### Registry changes old→new

- Rows `332 → 334` (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`):
  new ids S396, S397, inserted inside `## Registry` immediately after S395. No existing row's
  cell changed; no `status`/`recheck` change. (The census's E12 `row outside Registry section`
  caught the probe draft's end-of-file placement before landing.)

### Census

Start (attempt 2): `.ufo/waves/round-56/receipts/census-before-a2.txt` → `mado ok`, 332 rows,
exit 0. End: `mado ok`, exit 0, 334 rows (same command).

### Wave-3 findings applied to the entry (old→new, 14 rows + 4 prose + 1 how-to line)

Fresh sentence-to-pin audits at the tip (`w3/R56W3RevAuditA2{A..F}.md`) found 0 UNSUPPORTED
contradictions of the pins beyond two literally-false clauses (E01, E02) and seventeen
single-line OVERREACH rows; the fourteen with concrete corrections were applied (K05, K27,
E07, E08, E09 keep their explicit disclosures and stand). Quote, pin and anchor cells are
byte-unchanged; the frozen counter's `content` leg (one shared identifier token) and `num`
leg (every numeral in a proposition must be the row's own line, a same-pin K-row line, or in
the quote) bounded the rewrites — audit-proposed line-number citations that the `num` leg
rejects were re-grounded without numerals (M56-12). Prose: step 7 now states the
`m_scheduled`/event-loop guard and refresh coalescing (A2D F4); handleSource step 3 no
longer claims dangling symlinks as the only status-failure cause (F2); the reload-per-event
Limits bullet now states the wd-match condition, the IN_Q_OVERFLOW/unmatched-logged case,
and the lab receipt's actual touch result — no event for touch-only utimensat (F3, F1); the
rename-over bullet carries the same wd-match condition. The How-to-verify block gained the
exact C1 harness command its comment already promised (`R56W3RevEntryVerify`). The corrected
entry re-verifies: `MADO_AUTORELOAD_ENTRY … content=33/33 … TARGET_MET`, C1 controls 12/12,
CHECK107 `rows=39 covered=39 miss=0` (checker below).

### Instruments landed this attempt

- `quality/check-anchor-cover.py` (criterion 107's committed checker; `R56W3ExecCrit107Build`,
  107-spec receipts incl. red on the round-55 entry `rows=32 covered=25 miss=7` and 7/7
  registry mutants) — 23/23 agreement with `R56W3MutC107Spec`'s independently spec-derived
  vectors (regenerated fixtures, receipt in that seat's `vectors/` run). Ledger row added.
- Kill-fixture suites for the C1 counter (`w3/R56W3MutKillC1`: 51/51 mutant/fixture pairs
  distinguished, zero survivors), the C2 tool (`w3/R56W3MutKillC2`: 24 verified killers
  materialised as fixture trees; two >1 MiB tree files and one non-UTF-8 fixture name stay
  out of the commit, disclosed), and the C3 harness/counter (`w3/R56W3MutKillC3`,
  kill-level table + 11 counter diffs). The re-issued `R56W3MutC2Harness` killed 41/46
  harness mutants (31 oracle + 7 extended + 3 diagnostic, 5 survivors documented).
- `R56W3ExecHoldoutReseal`'s per-run-sealed C2 harness prototype (round-57 candidate, not a
  frozen artifact) and `R56W3RevFreezeBlind`'s check-freeze-order v2-aware patch draft
  (round-57 candidate, red/green receipts) — both as wave evidence only.

### Live and record verification this attempt

- Second `/proc` sample: `R56W3RevProcFdinfo` (40/40, raw evidence retained) and
  `R56W3RevWatchTable` (three samples `ALL_MATCH True`; no reload since session start,
  conditional on the source-level chain; journal window read-only).
- Tag pin: `R56W3ExecTagPin` — GitHub tag `v0.56.2` → commit `efb50993…` (type commit,
  unsigned), tag-served `ConfigWatcher.cpp` byte-equal to the S383 pin.
- Freeze order: `R56W3ExecFreezeOrder` — w1/w2 verdicts OK at freeze `3423ae28`; the D4
  v2-blindness reproduced with a receipt; `R56W3RevFreezeBlind` names the exact lines.
- Census discrimination after the attempt-1 fills: `R56W3CritCensus` — all six named mutants
  flagged, the 41 fills independently re-derived 0-defective, four additional census gaps
  named (weakens-not-blocking, routed).
- C3 allowlist third reading: `R56W3CritC3Allowlist` — 23 name-only, 1 reliance-leaning
  (S044), evidence for the closure's ruling; frozen list untouched.
- considerthese 2026-10-28 proposal 2: `receipts/session-material-a2.txt` (L1's own run;
  the seat aborted) — `SESSION_MATERIAL: files=29471 findings=274` at the attempt-2 tip
  tree (attempt 1: files=27658 findings=244 at `2aa347b1`; the receipt's rev line is
  binding, correcting the :93 pointer below). Assimilation: none re-confirmed
  (`w3/R56W3ScoutAdjacency`).

## Mistakes

- **M56-11 — a registry edit split the S395 row mid-row.** Class `landing`. Evidence: the
  L1's first `## Registry` insertion matched a row prefix and inserted a newline inside the
  S395 row (caught and repaired in the same session, before any commit or gate run; the
  landed census reads 334 rows, `mado ok`). Captured-by: the census row-count and the C3
  counter would have failed on commit (the row would have vanished from the registry and
  S052-style dangling pairs would fire). Fix: landed only after the repaired file passed
  the census and the C3 counter; registry edits must be whole-row replacements verified by
  the census before staging.
- **M56-12 — audit-proposed corrections carried numerals the frozen counter rejects.**
  Class `reference-drift`. Evidence: applying the wave-3 audit corrections verbatim made the
  C1 counter print `content=32/33 … missed=num:K21` and the C1 controls FAIL on the preview
  tree (scratch rev `fcc19788`; `num` leg allows only the row's own line, same-pin K-row
  lines, or numerals present in the quote). Captured-by: the counter itself (working as
  designed). Fix: propositions re-grounded without the foreign numerals; substance kept;
  preview re-measured green (scratch rev `4c640a9a`) before landing.
- **M56-13 — attempt 1's report said "Open L0 questions: none" while four mado L0 lines
  remain outstanding.** Class `overclaim`. Evidence: rounds 28 (line 134), 29 (135) and 34
  (149-151) lines in `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md`
  (`w3/R56W3ScoutGoalState/receipts/state-a2.md`). Captured-by: none (no gate reads the L0
  file). Fix: the attempt-2 report names them explicitly; routed: a report-time grep of the
  L0 file for the lane's open lines.
- **M56-14 — six wave-3 seats settled without report files.** Class `landing`. Evidence:
  `w3-results.json` lists 64 settled seats; 58 `w3/<Seat>.md` files exist; the six named
  above have partial artifacts or transcripts only. Captured-by: the L1's missing-report
  sweep over results vs disk (the wave's own WAVE-DONE counts settlement, not reports).
  Fix: disclosed in the report with each seat's last output; affected items marked
  unverified; no seats replaced (orchestrator recovery boundary); the L1 re-ran the one
  cheap item (the session-material count) itself.
- **M56-15 — the attempt-1 lesson said the considerthese count was taken "at the landed
  tip" while its receipt binds `2aa347b1`.** Class `attribution`. Evidence:
  `corpus/lessons/round-56.md:93` versus `w1/R56ScoutConsiderthese.md`
  (`w3/R56ScoutAdjacency/receipts/adjacency-a2.md`). Captured-by: none (no criterion binds
  a lesson pointer to its receipt's revision). Fix: this section's fresh receipt states its
  revision explicitly (`receipts/session-material-a2.txt`); the attempt-1 wording stands as
  history, corrected here by reference.

## Outside spot-check (pending the non-author closure)

Ready for it: admit S396 (raw line-93 quote) and S397 (raw line-160 quote); check the 14
row/prose corrections against `w3/R56W3RevAuditA2{A..F}.md`; adjudicate the four disputed
C3 allowlist pairs with `R56W3CritC3Allowlist`'s third reading; reject the `queued`/de-tagged
draft states (this Gate's re-applied list). The six reportless seats and their unverified
items are named in the report; the L1's own receipts are the lane's, not a non-author's.
- **M56-16 — a non-UTF-8 fixture filename in a committed directory blocked every lane push.**
  Class `landing`. Evidence: `R56W3MutKillC2` materialised a fixture named with a single `0x80`
  byte (`w3/R56W3MutKillC2/fixtures/b-k03/tree/conf.d/` + `\x80.conf`, 6 B, sha256
  `cb78bd8a17f7b751fe0d4663366dcbc257204033ef7ddd64b1f2969573b5b2e2`); the helper's first
  commit landed locally (`cfc63604`) but jj's working-copy snapshot aborted on the name and
  every `jj-lane.sh push` exited "push rejected (not a stale lease; no retry)" — the same
  class as attempt 1's deleted leftover, now shown to be push-blocking, not merely
  commit-skipping. Captured-by: the helper's skip warning (it skipped the path from the
  commit but the on-disk name still poisoned the snapshot). Fix: bytes preserved as
  `hostile-name-preserved.conf.txt` beside the original location, original removed, push
  retried green; the fixture's kill evidence (expected.out, kill table) is unaffected.
  Routed: the wave spec's fixture instructions should forbid non-UTF-8 fixture names in
  wave deliverable trees.
- **M56-17 — the env-channel probe captured real host credentials into a committed receipt.**
  Class `landing` (secret material in the lane). Evidence:
  `w3/R56W3MutBwrapChannels/receipts/probe-jail.out:189` held a live 1Password service-account
  token and an `OPENAI_CODEX_TOKEN` value — the seat implemented item (3) "environment
  variable probes" by dumping the real environment; the helper commit `cfc63604` (local,
  unpushed) carries the blob and GitHub push protection rejects every push (GH013, full text
  in the state dir's `jj-*mado-shokunin.err`). Captured-by: none that fired — the wave
  context banned credential material and the sentinel's three fixed patterns do not cover
  arbitrary environment values; the seat's report was one of the six never filed, so its
  own disclosure never happened. Fix: both values redacted in the working tree with
  sha256-prefixed markers (whole-wave rescan clean); the two secret-bearing local commits
  await an operator `jj abandon` (L0 filed, orchestrator messaged); routed criterion for
  round 57: wave items that probe env channels must assert the channel's existence without
  printing values, and a seat-side secret sweep over its own deliverables before yielding.

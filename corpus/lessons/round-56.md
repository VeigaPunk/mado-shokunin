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

Start: `.ufo/waves/round-56/receipts/census-before.txt` → `mado ok`, 319 rows, exit 0. End: see the round report and `receipts/at-final.txt` (332 rows).

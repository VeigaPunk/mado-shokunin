# Round 56 — mado (lesson skeleton, wave w2 draft)

Scribe draft for the L1. Facts below are verified against lane objects at integrated content revision
`28fc86ac2359ec27406d8a2c63bef82ea6e947ed` (base `13f0acbe`) unless marked. Counter results at `28fc86ac` are the L1's
reported numbers (not re-run by this seat). Everything the L1 must fill is marked `[L1]`.

## Gate

### Admitted (source rows; located quotes from the pinned bytes; access date 2026-10-28)

Quotes were checked by this seat as exact substrings of the stated pin line (`receipts/lesson-facts-check.py` does the anchor leg;
the quote check ran inline, output in the wave report). Every quote is at most 25 words.

| row | URL | located quote (pin line) |
|---|---|---|
| S383 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/inotify/ConfigWatcher.cpp | `setWatchList(*PDISABLEAUTORELOAD ? std::vector<std::string>{} : Config::mgr()->getConfigPaths());` (ConfigWatcher.cpp:34) |
| S384 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/values/ConfigValues.cpp | `"If true, the config will not reload automatically on save."` (ConfigValues.cpp:492) |
| S385 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/supplementary/propRefresher/PropRefresher.cpp | `if (m_propsTripped & REFRESH_CONFIG_WATCHER)` (PropRefresher.cpp:148); `Config::watcher()->update();` (149) |
| S386 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/eventLoop/EventLoopManager.cpp | `wl_event_loop_add_fd(m_wayland.loop, FD.get(), WL_EVENT_READABLE, configWatcherWrite, nullptr);` (EventLoopManager.cpp:128) |
| S387 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp | `Log::logger->log(Log::DEBUG, "CConfigManager: file {} modified, reloading", e.file);` (ConfigManager.cpp:1080); `Log::logger->log(Log::WARN, "source= skipping directory {}", value);` (1844) |
| S388 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/MiscFunctions.cpp | `static const char* const ENVHOME = getenv("HOME");` (MiscFunctions.cpp:65); `auto currentDir = currentPath.substr(0, currentPath.find_last_of('/'));` (68) |
| S389 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp | `if (COMMAND.contains("misc:disable_autoreload"))` (HyprCtl.cpp:1223); `Config::mgr()->reload();` (1276) |
| S390 | https://man7.org/linux/man-pages/man7/inotify.7.html | `File opened for writing was closed.` (inotify.7.html:186); `Don't dereference <i>pathname</i> if it is a symbolic link.` (262) |
| S391 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/supplementary/propRefresher/PropRefresher.hpp | `REFRESH_CONFIG_WATCHER     = (1 << 8),` (PropRefresher.hpp:18); `REFRESH_ALL = std::numeric_limits<std::underlying_type_t<ePropRefreshProp>>::max(),` (21). Added at integration, not in `w1/R56ScribeSourcesA/gate.md`. Its pin is not in `frozen-tables-v2.json` (see M56-9). |

Gate notes: the access date is the registered spec value; the w1 scribe recorded that the system clock read 2026-10-29 during its run
(`w1/R56ScribeSourcesA.md` D4). Pins are at `.ufo/waves/round-56/fetch/`.

### Entry admitted: `corpus/knowledge/hyprland-config-autoreload-r56.md`

- 30 K rows (counted by the C1 predicate; scope-covered at `28fc86ac`, 30/30 by `receipts/lesson-facts-check.out`).
- 3 H rows (host captures, not registry rows).
- 9 E rows (E01-E09, not counted by C1). **Six E rows cite a line outside their registry anchor** (E01 S388 `:66`, E03 S383 `:106`,
  E04 S389 `:1190`, E05 S387 `:630`, E06 S387 `:1838`, E07 S387 `:2134`). Proposed decision for `[L1]`: admit the K and H rows; admit the
  E rows only after their anchors are widened or the rows are dropped (see M56-8).
- Entry limits stated by the entry itself (lines 133-141): source level only; no save, reload or keyword observed; Lua provider and
  hyprlang declarations UNKNOWN.

### Rejections

- **Name-only back-references (the 24-row allowlist) as used-by assertions.** `c3-name-only.tsv` has 24 rows (sha256
  `70653e09…948ee`). Verified: 0 of the 24 pairs appear in any used-by cell at `28fc86ac` (`lesson-facts-check.out`: `conflicts(in used-by)=0`).
  The critic's 21 "false reliance" pairs (17 N, 3 M-N, 1 R, `w1/R56CritCiteDef/pairs-65.tsv`) are all inside the allowlist. The allowlist
  also holds 4 pairs the critic labelled U, M-U or R (`R56RevC3Contract` judged them name-only); that disagreement is open (see outside spot-check).
- **Numlock-style over-reading class.** None in S383-S391 or the entry: `grep -n -i numlock` on the entry returns no hit. The class lives in
  base rows S379/S380 (`w1/R56RevC3Contract/SOURCES-base.md:328-332`, corrected by S381/S382); not admitted this round.
  The round-55 rejection of the numlock range as a source stands.
- **Lua provider and hyprlang parser as unsourced.** No row admitted. The entry names them only as UNKNOWN (entry lines 61, 134, 140).
  Their parser is outside the pins; `w1/R56RevQuality.md` F5 notes the `configStringToInt` setter is uncited in the C2 model.

## Registry changes old->new

- Rows `319 -> 328` (`^\| S\d{3} \|` count of `corpus/SOURCES.md`, base and `28fc86ac`; verified).
- Added: S383-S391 (9 rows). Removed: none. Only cell 11 (`used-by`) changed on any existing row (verified cell by cell).
- Existing rows whose `used-by` changed: **23** (S015, S041, S046, S057, S059, S060, S073, S090, S091, S096, S158, S162, S175, S177,
  S186, S187, S201, S277, S318, S319, S350, S352, S353). **41 paths appended** to these rows, none removed.
- The 9 new rows each list `corpus/knowledge/hyprland-config-autoreload-r56.md` as used-by (9 more pairs).
- Full old->new table (cell text, 23 rows, verified against base and rev): `.ufo/waves/round-56/receipts/used-by-old-to-new.md`.
- Comma separators (E13; see M56-6).

## Mistakes

- **M56-1 — a registry anchor did not cover the quoted line.** Class `scope`. Evidence: `claims-frozen.md:94-97` (round-55 K14, K17);
  `w1/R56ConnHistory.md:54` (new rows "unconstrained anchors"); `w1/R56RevQuality.md:74` (F4: the scope leg does not cover E rows, and
  its able-to-fail receipt `receipts/scope-replay-r55.txt` has no committed producer). Captured-by: `scope:<id>` leg (registration §C1),
  **K rows only**: 30/30 covered at `28fc86ac`. **Not captured for E rows: 6 of 9 uncovered** (`receipts/lesson-facts-check.out`). Fix: K-row
  leg as registered; E-row coverage is open (M56-8).
- **M56-2 — v1 C1 control 8 unsatisfiable.** Class `reference-drift` (the M55-2 class). Evidence: `w1/R56RevC1Contract.md:70-76` (§3.1),
  table row `:31` (`edited-quote` gives `TARGET_MISSED`, `row:K05,source_cell:K05` but no `quote:K05`). Captured-by: none in v1. Fix: registration-v2 E1
  (control 8 requires `row:K05`; collateral legs allowed).
- **M56-3 — C2 harness layout leaked the answer key.** Class `vacuous` (the M55-4 class). Evidence: `w1/R56CritHoldout.md:16-24` (F1: the tool
  receives its own `expected.out` path); `:36-40` (sandbox: sibling reader scores 0/18); `w1/R56CritControls.md:14` and `:91` (C2-a: 18/18).
  Captured-by: the sealed hold-out stopped argv memorisation only. Fix: registration-v2 E6 (staged `<work>/run/<id>` with only `tree/`), E7
  (control `sibling-reader.py`, 0 of 26).
- **M56-4 — C3 gameable by deleting citations; mechanical fill records false reliance.** Class `vacuous` and `scope`. Evidence:
  `w1/R56CritDoNothing.md:22-23` (delete-citation control: `missing=0 extra=0 dangling=0 TARGET_MET`); `w1/R56CritCiteDef.md:9-10, 55, 86`
  (about 21 false-reliance pairs); `w1/R56RevC3Contract.md:62` (F1). Captured-by: registration-v2 §C3-v2 (frozen allowlist, `lost`, `conflict`,
  `stale`, 9 controls). Residual: the 41 filled pairs (36 U, 5 M-U per the critic's labels) are reliance by reader judgment; the counter cannot check it.
- **M56-5 — the L1 witness receipt overstated coverage.** Class `overclaim`. Evidence: `w1/R56RevC1Contract.md:95-97` (§3.4);
  `receipts/witness.txt` is one line (`witness K rows 30 failures []`). Captured-by: `receipts/witness-v2.txt` line 2 states the K-only
  scope; registration-v2 disclosure (d). The v1 sentence in `claims-frozen.md:9-10` is frozen and not edited.
- **M56-6 — used-by separator (space vs comma) broke census E11 until fixed.** Class `landing`. Evidence: `registration-v2-errata.md:13-16`
  (E13: 41 pairs joined with spaces; census E11 "used-by path missing on disk", reported on 23 rows). The census output is not in the lane
  receipts (`grep -rn E11` over `receipts/` is empty), so the 23-row count is unverified here. Captured-by: census E11 only; the
  counters accept both separators. Fix: comma separators at `0ff41272` (appended cells verified comma-separated).
- **M56-7 — the lost-leg hash was computed over the wrong pair set.** Class `landing` (spec text and frozen artifact disagree). Evidence:
  `registration-v2-errata.md:5-11` (E12); `frozen-tables-v2.json:784-785` (`base_pair_count: 65`, `base_pairs_sha256 630007b0…`). The written
  `lost` definition in `registration-v2.md` §C3-v2 reads PAIRS(base), which is 381 pairs. Captured-by: the counter fail-closed on the first run,
  as registered; the counter was then aligned to the 65-pair hash. Residual: `lost` catches only deletion of the 65 base-missing pairs; deleting
  one of the other 316 citations is not caught (errata E12).
- **M56-8 (proposed by this seat; not in the L1 list) — E-row anchors do not cover the quoted line.** Class `scope`. Evidence:
  `receipts/lesson-facts-check.out` (6 of 9 E rows). Captured-by: none (the scope leg counts K rows only; F4). Fix: `[L1]` widen or drop.
- **M56-9 (proposed by this seat; not in the L1 list) — S391 pin is outside the frozen tables.** Class `landing`. Evidence:
  `grep -c 'PropRefresher.hpp' frozen-tables-v2.json frozen-tables.json` returns 0 for both; `git log` shows
  `Hyprland-PropRefresher.hpp` first committed at `0ff41272` (after freeze `3423ae28` and v2 `323a69c9`). Captured-by: none. The quotes
  were checked against the pin (lines 18, 21). Fix: `[L1]` freeze the pin, or state it as unfrozen.

## Outside spot-check

Pending the non-author closure. Items ready for it, each with its artifact:

1. **E-row anchors** (M56-8): six rows; `receipts/lesson-facts-check.out`.
2. **S391 pin** (M56-9): hash `37acaaf16a24dcfe89d0702818b82d300d0da5e91ef1ba47494f7fd2ab0af2d0`; upstream bytes not fetched here.
3. **Five M-U pairs in the 41 fill** (critic labels): S015 (`walker-route-r18.md`), S158, S162, S175, S177 (`hyprctl-verification-layer.md`,
   an errata sentence that writes the range `S175-S177`). C3's CITE reads literal tokens, so a range hides S176.
4. **Four allowlist pairs in dispute**: critic U 1, M-U 2, R 1 (R56RevC3Contract judged them name-only). Closure adjudicates.
5. **C2 hold-out is now readable** (no longer sealed). A tool that reads it by absolute path passes (registration-v2 declared limit). The
   sandboxed harness (`w1/R56CritHoldout.md:168-171`) is not in the v2 controls.
6. **Sentence-to-pin audit** of the 30 K and 9 E propositions: not done (claims-frozen-v2: reported, not counted).
7. **Access date**: registered 2026-10-28; the w1 run read the pins on 2026-10-29 (`w1/R56ScribeSourcesA.md` D4).
8. **C1 and C3 counters at `28fc86ac`**: L1-reported (`MADO_AUTORELOAD_ENTRY … TARGET_MET`, `MADO_USED_BY … missing=0`); not re-run by this seat.

## Census / source changes

- Start census: `.ufo/waves/round-56/receipts/census-before.txt` (rows 319): 28 `W04` (duplicate url across scopes), 1 `W01` (S277
  tierC mined used-by), `mado ok` for `corpus/SOURCES.md`, `rc=0`. The command line is not recorded in the receipt.
- End census: `[L1]`. Not run by this seat. Expected direction (verified by URL equality): S383-S391 add new duplicate-URL memberships:
  S384 with S215 and S318; S387 with S162, S303, S317, S353, S368; S388 with S182, S321; S389 with S158, S307, S320, S366. W04 should rise;
  the exact count comes from the end census.
- Registry rows at `28fc86ac`: 328 (`mado`).

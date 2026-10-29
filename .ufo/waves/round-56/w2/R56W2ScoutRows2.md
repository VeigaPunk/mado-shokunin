# R56W2ScoutRows2 — wave-2 falsification of registry rows S385 and S386

Seat: R56W2ScoutRows2 (leaf, no subagents). Lane: mado-shokunin. Scored tree: `28fc86ac2359ec27406d8a2c63bef82ea6e947ed` (scratch copies only; the working tree was never used for scoring). Contract read first: `claims-frozen-v2.md`, `registration-v2.md`, `registration.md` §C1 (v2-silent legs), `registration-v2-errata.md` (E12–E14), `frozen-tables-v2.json` (sha256 verified `9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2` before use).

## What I attacked

Wave 1's row author wrote S385/S386 and the C1 gate quotes from the committed pin files; nothing independent had fetched the upstream bytes. I fetched both rows' URLs myself and re-derived every claim the rows and the gate make: byte identity (three ways), gate-quote line numbers, anchor coverage of every citing K row, anchor-vs-EOF bound (v2 E3), cell semantics (tier/kind/scope/teaches/recheck), and the census validator.

## Per-row verdicts

### S385 — MATCH (no defect found)

Row: `corpus/SOURCES.md` line 335 at `28fc86ac` (scratch copy `.../R56W2ScoutRows2/pin/corpus/SOURCES.md`).

1. Independent fetch (2026-10-28, curl to scratch):
   `curl -fsSL 'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/supplementary/propRefresher/PropRefresher.cpp'`
   → sha256 `65f01a1a50ef05ecb1630f8fd30bbbac91029b29f6b4b6bc3f353d0bb4b2817b`, 5139 B, 159 lines (`len(blob.split(b"\n"))` = 160 with trailing newline).
2. Three-way identity — all equal:
   - anchor cell: `sha256:65f01a1a…b2817b` and `5139 B` — equal to fetched bytes;
   - `frozen-tables-v2.json` `c1.pin_sha256["Hyprland-PropRefresher.cpp"]` — equal;
   - committed pin `.ufo/waves/round-56/fetch/Hyprland-PropRefresher.cpp` at `28fc86ac` — `cmp` rc=0 (byte-identical).
3. Gate quotes (`w1/R56ScribeSourcesA/gate.md`) located in the fetched bytes:
   - `if (m_propsTripped & REFRESH_CONFIG_WATCHER)` → fetched line **148** (gate says 148 — MATCH; occurrence unique in file);
   - `Config::watcher()->update();` → fetched line **149** (gate says 149 — MATCH; occurrence unique in file).
4. Entry rows citing S385 (`corpus/knowledge/hyprland-config-autoreload-r56.md` at `28fc86ac`): K15 (entry line 92, pin line 148) and K16 (entry line 93, pin line 149). Both lines are inside the anchor range `PropRefresher.cpp:148-149`. Both entry quote cells are byte-equal to the frozen-table quotes and substrings of the fetched lines (K15 quote 44 chars, K16 quote 28 chars).
5. Anchor vs EOF (v2 E3): max locator 149 ≤ last line 159. No run-past-EOF.
6. Cells vs the lines: kind `code` (C++ source — true); tier `A` (upstream project source pinned to tag commit `efb5099`, consistent with sibling code rows such as S369; not community); scope "the refresh step that calls the config watcher's update() when its refresh bit is among the tripped properties" — exactly what lines 148–149 show; teaches "the refresher calls Config::watcher()->update() only when REFRESH_CONFIG_WATCHER is set in m_propsTripped" — grounded: line 149 is the only `Config::watcher()->update()` in the file and line 148 is its guard; status `mined`; opened `2026-10-28` (valid ISO, past/present); recheck `on-release` (valid symbolic cadence); used-by names `corpus/knowledge/hyprland-config-autoreload-r56.md` (the entry). URL ends with `/` + `pin_suffix` (`src/config/supplementary/propRefresher/PropRefresher.cpp`) and contains the `rev_rule` token `efb5099…`. Exactly 11 cells.

### S386 — MATCH (no defect found)

Row: `corpus/SOURCES.md` line 336 at `28fc86ac`.

1. Independent fetch:
   `curl -fsSL 'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/eventLoop/EventLoopManager.cpp'`
   → sha256 `104ff43a4c02fcc88e8711cade68becd3a1fe099e970e4b1306774c85dd76f7c`, 9073 B, 282 lines (split chunks 283, trailing newline).
2. Three-way identity — all equal (anchor cell / `c1.pin_sha256["Hyprland-EventLoopManager.cpp"]` / committed pin, `cmp` rc=0).
3. Gate quote located: `wl_event_loop_add_fd(m_wayland.loop, FD.get(), WL_EVENT_READABLE, configWatcherWrite, nullptr);` → fetched line **128** (gate says 128 — MATCH). Fetched line 128 reads `m_configWatcherInotifySource = wl_event_loop_add_fd(…)`, so K13's longer quote is also a substring of line 128.
4. Entry rows citing S386: K13 (entry line 90, pin line 128) and K14 (entry line 91, pin line 71). Both inside the anchor locators `EventLoopManager.cpp:71,128`. Quote cells byte-equal the frozen-table quotes and are substrings of the fetched lines (K13 126 chars, K14 36 chars).
5. Anchor vs EOF: max locator 128 ≤ last line 282. No run-past-EOF.
6. Cells vs the lines: kind `code` true; tier `A` as S385; scope "how the config watcher's inotify fd is registered as a Wayland event-loop source and which callback it wakes" — grounded by lines 127–128 (`Config::watcher()->getInotifyFD()` guarded `wl_event_loop_add_fd` with `WL_EVENT_READABLE` and `configWatcherWrite`); teaches "the inotify fd is added with WL_EVENT_READABLE and configWatcherWrite, which calls Config::watcher()->onInotifyEvent()" — grounded: fetched lines 70–73 show `static int configWatcherWrite(…) { Config::watcher()->onInotifyEvent(); return 0; }`, i.e. line 71 (K14's line) sits inside the very callback registered at line 128. status/opened/recheck/used-by/URL-suffix/rev-token/11-cells all as S385, all valid.

## Census validator

Command: `cd <scratch>/pin && /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <scratch>/pin/corpus/SOURCES.md` (gawk present; exit 1).
Result: **no W or E line mentions S385 or S386.** The exit-1 is driven by (a) E11 "missing used-by" for ~300 other mined rows — an artifact of my scratch layout holding only `corpus/SOURCES.md` and the r56 entry, so other rows' used-by targets do not exist there; S383–S391's used-by target does exist and indeed no E11 fires for S383–S391; and (b) W04 duplicate-URL warnings on other rows (S384, S387, S388, S389 among them — none on S385/S386). Both S385/S386 pass the validator's shape checks (11 cells, id, enums, dates, recheck cadence, tier-A-not-community).

## Defects

None. Both rows MATCH on every axis attacked. Null-result commands: the three-way sha256 comparisons (`receipt-hashes.txt`, `receipt-verify-rows.txt`), the quote-location greps on the fetched bytes, the anchor-vs-line-count computation (`receipt-linecounts.txt`), and the census run filtered for `S38[56]` (`receipt-census.txt`).

## Not verified / limits

- My fetch is same-day (2026-10-28) as the registered access date; upstream drift after today is out of scope. Identity at freeze time is proven by byte-equality with the committed pins.
- The census E11 flood is environmental (partial scratch tree), not a lane finding; I did not re-audit other rows' E11s.
- I did not run the C1 counter/harness, other rows (S383/384/387–391), or the C2/C3 machinery — out of this seat's scope.
- Entailment beyond the anchor lines (e.g. that `refreshProp` is the only caller path) was not audited; the cells make no such claim.
- No tools installed; pacman untouched. No git/jj mutations; lane untouched except this seat's deliverable paths.

## Deliverables

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w2/R56W2ScoutRows2/` — `receipt-hashes.txt`, `receipt-linecounts.txt`, `receipt-verify-rows.txt`, `receipt-census.txt`, `verify_rows.py` (the three-way checker), `fetch/PropRefresher.cpp`, `fetch/EventLoopManager.cpp` (the independent fetches).
- Report: `.ufo/waves/round-56/w2/R56W2ScoutRows2.md` (this file).

Scratch `/fast/scratch/hyaku/mado-r56/R56W2ScoutRows2/` removed after receipt copy.

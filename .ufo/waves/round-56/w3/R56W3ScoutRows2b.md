# R56W3ScoutRows2b — wave-3 second-sample re-open of registry rows S385 and S386

Seat: `R56W3ScoutRows2b` (leaf member — no subagent dispatch). Lane: `mado-shokunin`.
Scored tree: **`0f3a54361a9824484d0801679ceb1fd8ac7c32e1`** (lane tip). All tree reads were
`git -C /home/vgpnk/Projects/shokunin/mado-shokunin show <rev>:<path>` — read-only git; the working
tree was never scored. Fetch date 2026-10-30. Scratch `/fast/scratch/hyaku/mado-r56/R56W3ScoutRows2b/`
removed after the receipts were copied.

## What I attacked

Item: *"Re-open registry rows S385 and S386 independently at the tip (second sample: attempt-1's
wave-2 scouts fetched at `28fc86ac`; you re-derive at the tip)."* For each of the two rows:
fetch the row's own URL myself, sha256 the bytes, compare against the row's anchor cell **and**
against `frozen-tables-v2.json` where the row is tabled, locate the **gate quote** in the upstream
bytes and report its line number, and check the anchor locators stay within the file's line count.
Verdict MATCH / MISMATCH per row with sha256 and line numbers.

Attempt-1's seat `R56W2ScoutRows2` (`.ufo/waves/round-56/w2/R56W2ScoutRows2.md`) covered exactly
S385/S386 at `28fc86ac`. This seat is an independent second sample at the tip: the two rows are
byte-identical at both revisions (`grep -E '^\| S38[56] '` of `corpus/SOURCES.md` →
sha256 `bf1e161ad96f7e47ec9792969eec3a636ef2c17380ebc1baf928bf44c99035e8` at `28fc86ac` **and** at
`0f3a5436`), and the bytes I fetched today are a fresh network fetch, not a re-read of attempt-1's
evidence.

Contract read first: `claims-frozen-v2.md`, `registration-v2.md`, `registration.md`,
`frozen-tables-v2.json` (all at the tip). The frozen table's own integrity was re-verified before
use: sha256 `9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2` — MATCH with the
value embedded in `claims-frozen-v2.md`.

## What I did (commands and decisive output)

**1. Independent fetch (curl to scratch).**
```
$ curl -sS -L -o 385.cpp -w '385 http=%{http_code} size=%{size_download}\n' \
  'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/supplementary/propRefresher/PropRefresher.cpp'
385 http=200 size=5139
$ curl -sS -L -o 386.cpp -w '386 http=%{http_code} size=%{size_download}\n' \
  'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/eventLoop/EventLoopManager.cpp'
386 http=200 size=9073
```
No redirect (`num_redirects=0` for both), and two repeat fetches returned identical sizes.

**2. sha256 of the fetched bytes, three-way against the row and the frozen table.**
```
$ sha256sum 385.cpp 386.cpp
65f01a1a50ef05ecb1630f8fd30bbbac91029b29f6b4b6bc3f353d0bb4b2817b  385.cpp
104ff43a4c02fcc88e8711cade68becd3a1fe099e970e4b1306774c85dd76f7c  386.cpp
```
- S385 anchor cell `sha256:65f01a1a…b2817b` and `5139 B` — both MATCH. `frozen-tables-v2.json`
  `c1.pin_sha256["Hyprland-PropRefresher.cpp"]` — MATCH. `c1.rows["S385"]` — MATCH.
- S386 anchor cell `sha256:104ff43a…76f7c` and `9073 B` — both MATCH. `c1.pin_sha256["Hyprland-EventLoopManager.cpp"]` — MATCH. `c1.rows["S386"]` — MATCH.
- Third way: the committed pins at the tip
  (`.ufo/waves/round-56/fetch/Hyprland-{PropRefresher,EventLoopManager}.cpp`) hash to the same two
  values and `cmp` against my fetched files is byte-identical (rc=0). Also equal to
  `receipts/pins.sha256` at the tip. The v1 `frozen-tables.json` agrees with v2 on both rows.

**3. Gate quotes located in the upstream bytes** (gate table: `corpus/lessons/round-56.md` `## Gate`):
- S385 — `if (m_propsTripped & REFRESH_CONFIG_WATCHER)` → fetched line **148** (gate says 148) — **MATCH**, unique occurrence.
- S386 — `wl_event_loop_add_fd(m_wayland.loop, FD.get(), WL_EVENT_READABLE, configWatcherWrite, nullptr);` → fetched line **128** (gate says 128) — **MATCH**, unique occurrence.

Fetched context (verbatim), which also grounds the rows' `teaches` cells:
```
148:     if (m_propsTripped & REFRESH_CONFIG_WATCHER)
149:         Config::watcher()->update();
 70: static int configWatcherWrite(int fd, uint32_t mask, void* data) {
 71:     Config::watcher()->onInotifyEvent();
127:     if (const auto& FD = Config::watcher()->getInotifyFD(); FD.isValid())
128:         m_configWatcherInotifySource = wl_event_loop_add_fd(m_wayland.loop, FD.get(), WL_EVENT_READABLE, configWatcherWrite, nullptr);
```
`grep -n 'watcher()->update()' 385.cpp` → line 149 only, guarded by 148 (S385's "only when" holds
within the file); `grep -n 'REFRESH_CONFIG_WATCHER' 385.cpp` → line 148 only.

**4. Anchor locators vs the file's line count** (`len(blob.split(b"\n"))`, the counter's own measure):
- S385 / `Hyprland-PropRefresher.cpp`: 160 lines; anchor `PropRefresher.cpp:148-149` — in range.
- S386 / `Hyprland-EventLoopManager.cpp`: 283 lines; anchor `EventLoopManager.cpp:71,128` — in range.
Nothing runs past EOF (the failure E3 was written for).

**5. Every citing K row, and the counter's own scope function** (`scope_covers()` extracted from
`quality/counters/c1-r56-autoreload-entry.py`, run on copies only):
```
S385 K15 line 148 nlines 160 scope_covers: True
S385 K16 line 149 nlines 160 scope_covers: True
S386 K13 line 128 nlines 283 scope_covers: True
S386 K14 line 71  nlines 283 scope_covers: True
```
Mutation sanity check of that function on these rows' anchors:
`S385-mut-eof` (anchor → `148-9999`) ⇒ False; `S386-mut-eof` (`71,128,9999`) ⇒ False;
`S386-mut-drop71` (`128` only) ⇒ False (K14 uncovered). The coverage test is live for these rows.
Entry quote cells for K13–K16 are byte-equal to the frozen-table quotes, the sids and the
`pin:line` locators all match, and each quote is present at its stated line in the fetched bytes.

**6. Row cells vs the lines:** kind `code` (true), tier `A` (upstream tagged source), scope and
teaches cells grounded by the lines quoted above, status `mined`, opened `2026-10-28`,
recheck `on-release`, used-by = the r56 entry (target exists at the tip), 11 cells, URL ends with
`c1.pin_suffix[pin]` and carries the pinned commit token — i.e. every condition of the counter's
`source_cell_ok` holds for both rows.

**7. External corroboration, independent of the raw endpoint:** GitHub's contents API reports blob
sha `498bd105eab388ea0e3055f0dbbef5185e6bef1f` (5139 B) and `0e0f6e9fe34be6249cd02bf486367f2c2be4c33f`
(9073 B) for the pinned commit; `git hash-object` of my two fetched files gives exactly those ids.
`git/ref/tags/v0.56.2` resolves to `efb50993780079460b0cbed1363e2166a2de1d9f` — the pinned commit
is the released 0.56.2 tree, and the two files fetched at the tag hash identically to the two
fetched at the commit, matching the host pin `host-version.json`.

**8. Context at the tip (not this seat's claim, run only to confirm the rows sit in a green tree):**
```
$ python3 -I quality/counters/c1-r56-autoreload-entry.py --repo . --rev 0f3a5436... --work <scratch>
MADO_AUTORELOAD_ENTRY: rev=0f3a5436... rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none   (exit 0)
$ python3 -I quality/counters/c3-r56-used-by.py --repo . --rev 0f3a5436... --work <scratch>
MADO_USED_BY: rev=0f3a5436... entries=71 rows=332 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none   (exit 0)
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md   (tip export)
exit 0 — no W/E line mentions S385 or S386; the only W04 duplicate-URL warnings are S392–S395
```

## Verdict per row

| row | fetched sha256 | anchor cell | frozen table v2 | gate quote line (found vs gate) | locators ≤ line count | covering K rows | verdict |
|---|---|---|---|---|---|---|---|
| S385 | `65f01a1a50ef05ecb1630f8fd30bbbac91029b29f6b4b6bc3f353d0bb4b2817b` | MATCH | MATCH | 148 vs 148 — MATCH | MATCH (160 lines, anchor `148-149`) | K15, K16 | **MATCH** |
| S386 | `104ff43a4c02fcc88e8711cade68becd3a1fe099e970e4b1306774c85dd76f7c` | MATCH | MATCH | 128 vs 128 — MATCH | MATCH (283 lines, anchor `71,128`) | K13, K14 | **MATCH** |

## Defects

**None.** Neither row shows any defect on any axis attacked. No severity items to report: no
blocking, no weakening, no cosmetic findings.

## Null-result commands (checks that found nothing wrong)

The decisive "nothing to find" commands are the three-way sha256 comparisons
(`sha256sum` of the fetched bytes vs the anchor cell and `c1.pin_sha256`), the `cmp` against the
committed pins, the gate-quote location greps on the fetched bytes (`grep -n` → 148 / 128 only),
the anchor-vs-line-count computation, the `scope_covers()` calls and their mutation variants, the
GitHub blob-sha cross-check, and the census run filtered for `S38[56]` (no W/E line matched).

## Not verified / limits

- Upstream drift **after** 2026-10-30 is out of scope; the pinned-commit URL is immutable for the
  commit path, and byte-equality with the committed pins proves identity at fetch time.
- I did not audit entailment beyond the cited lines (e.g. whether `refreshProp` is the only
  refresh path, or whether `Config::watcher()->update()` could be reached from elsewhere in the
  tree) — the rows' cells make no such claim, and S385's "only when" holds *within the pinned
  file* (the only `watcher()->update()` occurrence there is line 149, guarded by line 148).
- I did not run the C2 harness, the C1/C3 control harnesses or the other rows (S383/S384/S387–S391);
  those are other seats' scopes.
- The S390 man-page fetch in §8 of the receipt was a method-consistency bonus, not part of this
  seat's assigned row set.
- No tools installed or upgraded; pacman untouched (host pacman guard: all transactions paused).

## Deliverables

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ScoutRows2b/receipts/rows.md`
  — the full per-row receipt (fetch commands, sha256 table, gate-quote locations, line counts,
  scope_covers results, census/counter context, external corroboration).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ScoutRows2b.md` — this report.

Scratch `/fast/scratch/hyaku/mado-r56/R56W3ScoutRows2b/` removed after the receipts were copied.
No tracked lane file was edited; no git/jj mutation of the lane, the fleet repo or any sibling lane
was performed (read-only `git show`/`git ls-tree`/`git archive` only); no fixture repo was created
(the mutations were in-memory string substitutions over copies of the anchor cell).

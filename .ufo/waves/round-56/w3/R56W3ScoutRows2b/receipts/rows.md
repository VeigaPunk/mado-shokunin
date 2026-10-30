# R56W3ScoutRows2b — receipts/rows.md (registry rows S385, S386)

Seat: `R56W3ScoutRows2b` (leaf, no subagent dispatch). Lane: `mado-shokunin`.
Scored tree: `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (all tree reads via
`git -C <lane> show <rev>:<path>`; the working tree was never used for scoring).
Fetch date: 2026-10-30. Scratch: `/fast/scratch/hyaku/mado-r56/R56W3ScoutRows2b/` (removed after copy).

Second sample: attempt-1's wave-2 seat `R56W2ScoutRows2` fetched these two rows at
`28fc86ac2359ec27406d8a2c63bef82ea6e947ed`; this seat re-derives both rows independently at the
lane tip. The two S385/S386 rows are byte-identical at the two revisions
(`git show <rev>:corpus/SOURCES.md | grep -E '^\| S38[56] ' | sha256sum` →
`bf1e161ad96f7e47ec9792969eec3a636ef2c17380ebc1baf928bf44c99035e8` at both `28fc86ac` and
`0f3a5436`), so this is a second independent fetch of the same bytes, not a re-read of the
attempt-1 evidence.

## 0. Contract read first

```
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a5436:.ufo/waves/round-56/claims-frozen-v2.md
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a5436:.ufo/waves/round-56/registration-v2.md
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a5436:.ufo/waves/round-56/registration.md
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a5436:.ufo/waves/round-56/frozen-tables-v2.md
```

Frozen-table integrity, recomputed at the tip before use:

```
$ python3 -I -c 'import hashlib,subprocess; print(hashlib.sha256(subprocess.run(["git","-C","/home/vgpnk/Projects/shokunin/mado-shokunin","show","0f3a54361a9824484d0801679ceb1fd8ac7c32e1:.ufo/waves/round-56/frozen-tables-v2.json"],capture_output=True).stdout).hexdigest())'
frozen-tables-v2.json sha256 at tip: 9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2 MATCH
```
(expected `9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2` per `claims-frozen-v2.md` — MATCH)

## 1. Rows under attack, verbatim at the tip

```
$ git -C <lane> show 0f3a5436:corpus/SOURCES.md | grep -E '^\| S38[56] '
| S385 | Hyprland 0.56.2 property refresher - config watcher refresh step - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/supplementary/propRefresher/PropRefresher.cpp | code | A | the refresh step that calls the config watcher's update() when its refresh bit is among the tripped properties | PropRefresher.cpp:148-149 @ efb50993780079460b0cbed1363e2166a2de1d9f; pin .ufo/waves/round-56/fetch/Hyprland-PropRefresher.cpp 5139 B sha256:65f01a1a50ef05ecb1630f8fd30bbbac91029b29f6b4b6bc3f353d0bb4b2817b | the refresher calls Config::watcher()->update() only when REFRESH_CONFIG_WATCHER is set in m_propsTripped | mined | 2026-10-28 | on-release | corpus/knowledge/hyprland-config-autoreload-r56.md |
| S386 | Hyprland 0.56.2 event loop manager - config watcher inotify registration - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/eventLoop/EventLoopManager.cpp | code | A | how the config watcher's inotify fd is registered as a Wayland event-loop source and which callback it wakes | EventLoopManager.cpp:71,128 @ efb50993780079460b0cbed1363e2166a2de1d9f; pin .ufo/waves/round-56/fetch/Hyprland-EventLoopManager.cpp 9073 B sha256:104ff43a4c02fcc88e8711cade68becd3a1fe099e970e4b1306774c85dd76f7c | the inotify fd is added with WL_EVENT_READABLE and configWatcherWrite, which calls Config::watcher()->onInotifyEvent() | mined | 2026-10-28 | on-release | corpus/knowledge/hyprland-config-autoreload-r56.md |
```

(SOURCES.md lines 335 and 336 at the tip.)

## 2. Independent fetch (2026-10-30, curl to scratch, no lane writes)

```
$ cd /fast/scratch/hyaku/mado-r56/R56W3ScoutRows2b
$ curl -sS -L -o 385.cpp -w '385 http=%{http_code} size=%{size_download} url=%{url_effective}\n' \
  'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/supplementary/propRefresher/PropRefresher.cpp'
385 http=200 size=5139 url=https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/supplementary/propRefresher/PropRefresher.cpp
$ curl -sS -L -o 386.cpp -w '386 http=%{http_code} size=%{size_download} url=%{url_effective}\n' \
  'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/eventLoop/EventLoopManager.cpp'
386 http=200 size=9073 url=https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/eventLoop/EventLoopManager.cpp

$ curl -sS -o /dev/null -w '385 noredir http=%{http_code} redirects=%{num_redirects}\n' <S385 url>
385 noredir http=200 redirects=0
$ curl -sS -o /dev/null -w '386 noredir http=%{http_code} redirects=%{num_redirects}\n' <S386 url>
386 noredir http=200 redirects=0
```
Two repeat fetches of each URL returned the same size (5139 / 9073) — the served bytes are stable.

## 3. sha256 of the fetched bytes vs the anchor cell and the frozen table

```
$ sha256sum 385.cpp 386.cpp
65f01a1a50ef05ecb1630f8fd30bbbac91029b29f6b4b6bc3f353d0bb4b2817b  385.cpp
104ff43a4c02fcc88e8711cade68becd3a1fe099e970e4b1306774c85dd76f7c  386.cpp
```

| row | fetched sha256 | anchor cell `sha256:` | frozen `c1.pin_sha256[<pin>]` | byte count vs anchor cell | verdict |
|---|---|---|---|---|---|
| S385 | `65f01a1a50ef05ecb1630f8fd30bbbac91029b29f6b4b6bc3f353d0bb4b2817b` | `65f01a1a…b2817b` — MATCH | `65f01a1a…b2817b` (key `Hyprland-PropRefresher.cpp`) — MATCH | 5139 fetched vs `5139 B` — MATCH | **MATCH** |
| S386 | `104ff43a4c02fcc88e8711cade68becd3a1fe099e970e4b1306774c85dd76f7c` | `104ff43a…76f7c` — MATCH | `104ff43a…76f7c` (key `Hyprland-EventLoopManager.cpp`) — MATCH | 9073 fetched vs `9073 B` — MATCH | **MATCH** |

Frozen `c1.rows["S385"] = "Hyprland-PropRefresher.cpp"`, `c1.rows["S386"] = "Hyprland-EventLoopManager.cpp"` — both agree with the row's own pin path.
Also equal to the v1 table `frozen-tables.json` (`c1.rows`, `c1.pin_sha256`) — v2 does not differ from v1 on these two rows.

Third-way identity against the committed pins at the tip:

```
$ git -C <lane> show 0f3a5436:.ufo/waves/round-56/fetch/Hyprland-PropRefresher.cpp   | sha256sum
65f01a1a50ef05ecb1630f8fd30bbbac91029b29f6b4b6bc3f353d0bb4b2817b  -
$ git -C <lane> show 0f3a5436:.ufo/waves/round-56/fetch/Hyprland-EventLoopManager.cpp | sha256sum
104ff43a4c02fcc88e8711cade68becd3a1fe099e970e4b1306774c85dd76f7c  -
$ cmp 385.cpp pin-S385.cpp   # rc=0, no output
$ cmp 386.cpp pin-S386.cpp   # rc=0, no output
```
Also equal to `receipts/pins.sha256` (same two hashes) at the tip.

## 4. Gate quotes located in the upstream bytes

Gate table source: `corpus/lessons/round-56.md` `## Gate` (lines 18–26 at the tip).

| row | gate quote | gate line | located in fetched bytes | verdict |
|---|---|---|---|---|
| S385 | `if (m_propsTripped & REFRESH_CONFIG_WATCHER)` | 148 | line **148** (unique occurrence) | **MATCH** |
| S386 | `wl_event_loop_add_fd(m_wayland.loop, FD.get(), WL_EVENT_READABLE, configWatcherWrite, nullptr);` | 128 | line **128** (unique occurrence; fetched line 128 is `m_configWatcherInotifySource = wl_event_loop_add_fd(…)`, so the shorter gate quote is a substring of the frozen K13 quote) | **MATCH** |

Context actually fetched (not paraphrased):

```
148:     if (m_propsTripped & REFRESH_CONFIG_WATCHER)
149:         Config::watcher()->update();

 70: static int configWatcherWrite(int fd, uint32_t mask, void* data) {
 71:     Config::watcher()->onInotifyEvent();
 72:     return 0;
 73: }
127:     if (const auto& FD = Config::watcher()->getInotifyFD(); FD.isValid())
128:         m_configWatcherInotifySource = wl_event_loop_add_fd(m_wayland.loop, FD.get(), WL_EVENT_READABLE, configWatcherWrite, nullptr);
```

## 5. Anchor locators vs the file's line count (v2 E3 bound)

Line count used by the counter: `len(blob.split(b"\n"))`.

| row | pin | line count | anchor locators | in range? | content at the locator |
|---|---|---|---|---|---|
| S385 | `Hyprland-PropRefresher.cpp` | 160 | `148-149` | yes (148 ≤ 149 ≤ 160) | 148 = `if (m_propsTripped & REFRESH_CONFIG_WATCHER)`, 149 = `Config::watcher()->update();` |
| S386 | `Hyprland-EventLoopManager.cpp` | 283 | `71,128` | yes (71 ≤ 283, 128 ≤ 283) | 71 = `Config::watcher()->onInotifyEvent();`, 128 = the `wl_event_loop_add_fd(…)` registration |

No locator runs past EOF. (Contrast with the wave-1 finding E3 was written for: 7 of 8 cheap anchors
ran past EOF on the round-55-style entries; these two do not.)

## 6. Every citing K row: quote cell, sid, locator, and the counter's own `scope_covers` verdict

```
$ python3 -I <scratcher>   # scope_covers() extracted from quality/counters/c1-r56-autoreload-entry.py (v2 E3 form)
S385 K15 line 148 nlines 160 scope_covers: True
S385 K16 line 149 nlines 160 scope_covers: True
S386 K13 line 128 nlines 283 scope_covers: True
S386 K14 line 71  nlines 283 scope_covers: True
```

| K | row | entry line at tip | entry quote cell | frozen quote | entry quote == frozen quote | sid matches | locator form | quote present at that line in the fetched bytes |
|---|---|---|---|---|---|---|---|---|
| K13 | S386 | 90 | `m_configWatcherInotifySource = wl_event_loop_add_fd(m_wayland.loop, FD.get(), WL_EVENT_READABLE, configWatcherWrite, nullptr);` | same | True | True | `Hyprland-EventLoopManager.cpp:128` | yes (128) |
| K14 | S386 | 91 | `Config::watcher()->onInotifyEvent();` | same | True | True | `Hyprland-EventLoopManager.cpp:71` | yes (71) |
| K15 | S385 | 92 | `if (m_propsTripped & REFRESH_CONFIG_WATCHER)` | same | True | True | `Hyprland-PropRefresher.cpp:148` | yes (148) |
| K16 | S385 | 93 | `Config::watcher()->update();` | same | True | True | `Hyprland-PropRefresher.cpp:149` | yes (149) |

Anchor coverage: K15/K16 lie inside the S385 anchor range `148-149`; K13/K14 lie inside the S386
anchor list `71,128`. No citing K row is uncovered by its row's anchor.

Scope-leg sensitivity, reproduced with the counter's own function (mutation test on copies only —
no lane file was touched):

```
S385             scope_covers(line 148, nlines 160) = True
S385-mut-eof     scope_covers(line 148, nlines 160) = False   # anchor widened to 148-9999
S385-mut-narrow  scope_covers(line 148, nlines 160) = True    # anchor narrowed to 148 (still covers K15)
S386             scope_covers(line 71, nlines 283) = True
S386-mut-eof     scope_covers(line 71, nlines 283) = False   # anchor widened to 71,128,9999
S386-mut-drop71  scope_covers(line 71, nlines 283) = False   # anchor narrowed to 128 (K14 falls out)
```
So the E3 bound and the coverage test are live for these two rows, not vacuous here.

## 7. Row-cell semantics vs the fetched lines

| cell | S385 | S386 | check |
|---|---|---|---|
| kind | `code` | `code` | C++ source — true |
| tier | `A` | `A` | upstream project source pinned to a tagged commit — consistent with the sibling code rows (S383/S384/S387–S389) |
| scope cell | "the refresh step that calls the config watcher's update() when its refresh bit is among the tripped properties" | "how the config watcher's inotify fd is registered as a Wayland event-loop source and which callback it wakes" | S385 grounded by 148–149 (guard + call). S386 grounded by 127–128 (registration under an `FD.isValid()` guard) plus 70–73 (the callback body) |
| teaches cell | "the refresher calls Config::watcher()->update() only when REFRESH_CONFIG_WATCHER is set in m_propsTripped" | "the inotify fd is added with WL_EVENT_READABLE and configWatcherWrite, which calls Config::watcher()->onInotifyEvent()" | S385: `grep -n 'watcher()->update()' 385.cpp` → only line 149, and it is guarded by line 148 — "only when" holds *within this file*. S386: line 128 registers `FD.get()` with `WL_EVENT_READABLE` and `configWatcherWrite`; lines 70–73 show `configWatcherWrite` calling `Config::watcher()->onInotifyEvent()` — grounded |
| status / opened / recheck | `mined` / `2026-10-28` / `on-release` | same | valid ISO date, valid symbolic cadence |
| used-by | `corpus/knowledge/hyprland-config-autoreload-r56.md` | same | target exists at the tip |
| URL | ends with `/src/config/supplementary/propRefresher/PropRefresher.cpp` | ends with `/src/managers/eventLoop/EventLoopManager.cpp` | equals `c1.pin_suffix[pin]`; and the pinned commit token `efb50993780079460b0cbed1363e2166a2de1d9f` is present in both URLs — the counter's `source_cell_ok` conditions all hold |
| cell count | 11 | 11 | the census's shape requirement |

Entry prose that cites these two pins (all locators in range):
`Hyprland-EventLoopManager.cpp:127-128` (entry line 23), `:127` (line 136), `:128`/`:71` (rows K13/K14);
`Hyprland-PropRefresher.cpp:148-149` (line 26), `:31` (line 26, `m_propsTripped |= prop;` — verified at line 31),
`:148`/`:149` (rows K15/K16). Max locator 149 ≤ 160 and 128 ≤ 283 — nothing past EOF.

## 8. External corroboration (independent of the raw endpoint)

```
$ curl -sS -L 'https://api.github.com/repos/hyprwm/Hyprland/contents/src/config/supplementary/propRefresher/PropRefresher.cpp?ref=efb50993780079460b0cbed1363e2166a2de1d9f'
  -> blob sha 498bd105eab388ea0e3055f0dbbef5185e6bef1f  size 5139
$ git hash-object 385.cpp
498bd105eab388ea0e3055f0dbbef5185e6bef1f
$ curl -sS -L 'https://api.github.com/repos/hyprwm/Hyprland/contents/src/managers/eventLoop/EventLoopManager.cpp?ref=efb50993780079460b0cbed1363e2166a2de1d9f'
  -> blob sha 0e0f6e9fe34be6249cd02bf486367f2c2be4c33f  size 9073
$ git hash-object 386.cpp
0e0f6e9fe34be6249cd02bf486367f2c2be4c33f
```
Git blob ids of the fetched bytes equal the blob ids GitHub reports for the pinned commit — the
fetch is not a proxy artifact.

Tag equivalence (the pinned commit is the released 0.56.2 tree):
```
$ curl -sS -L 'https://api.github.com/repos/hyprwm/Hyprland/git/ref/tags/v0.56.2'  -> efb50993780079460b0cbed1363e2166a2de1d9f (commit)
$ curl -sS -L '.../v0.56.2/src/config/supplementary/propRefresher/PropRefresher.cpp'  -> sha256 65f01a1a…b2817b (same)
$ curl -sS -L '.../v0.56.2/src/managers/eventLoop/EventLoopManager.cpp'              -> sha256 104ff43a…76f7c (same)
```
The pinned commit is the `v0.56.2` tag commit, matching the host pin
`.ufo/waves/round-56/fetch/host-version.json` (`"version": "0.56.2"`, `"tag": "v0.56.2"`,
`"commit": "efb50993780079460b0cbed1363e2166a2de1d9f"`).

Bonus fetch (the same method applied to the round-56 man-page row, for method consistency — not
this seat's row set): `https://man7.org/linux/man-pages/man7/inotify.7.html` → http 200, 44066 B,
sha256 `79f5ab18e2fc423631cf4949ef82ca1384844353ea11a4dba42e1a77e8fdd8fd`, equal to the S390 anchor
cell and to `c1.pin_sha256["man7-inotify.7.html"]`; the S390 gate quote
`File opened for writing was closed.` is at line 186 as the gate states (919 lines). Consistent.

## 9. Registry / census / counters at the tip (context, not this seat's claim)

```
$ python3 -I quality/counters/c1-r56-autoreload-entry.py --repo . --rev 0f3a54361a9824484d0801679ceb1fd8ac7c32e1 --work <scratch>
MADO_AUTORELOAD_ENTRY: rev=0f3a5436... rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none   (exit 0)

$ python3 -I quality/counters/c3-r56-used-by.py --repo . --rev 0f3a54361a9824484d0801679ceb1fd8ac7c32e1 --work <scratch>
MADO_USED_BY: rev=0f3a5436... entries=71 rows=332 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none   (exit 0)

$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md   # on a tip export
exit 0 — no W/E line mentions S385 or S386; the only W04 duplicate-URL warnings are for S392–S395
```
S385/S386 are counted as new rows (`c1.new_row_ids` contains both) and neither appears in the
24-row name-only allowlist (`c3-name-only.tsv`), so their `used-by` cells are genuine reliance
edges, not exemptions.

## 10. Per-row verdict

| row | sha256 | anchor cell | frozen table | gate quote line | locators ≤ line count | covering K rows | verdict |
|---|---|---|---|---|---|---|---|
| S385 | `65f01a1a50ef05ecb1630f8fd30bbbac91029b29f6b4b6bc3f353d0bb4b2817b` | MATCH | MATCH | 148 = 148 | MATCH (160 lines) | K15, K16 | **MATCH** |
| S386 | `104ff43a4c02fcc88e8711cade68becd3a1fe099e970e4b1306774c85dd76f7c` | MATCH | MATCH | 128 = 128 | MATCH (283 lines) | K13, K14 | **MATCH** |

No defect found on either row.

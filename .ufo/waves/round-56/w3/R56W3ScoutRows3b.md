# R56W3ScoutRows3b — seat report

**Seat:** R56W3ScoutRows3b (scout, round-56 wave 3, attempt 2 of the round).
**Item attacked:** re-open registry rows **S387, S392, S395** independently at the lane tip
`0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (second sample; attempt-1's wave-2 scouts fetched at `28fc86ac`,
where S392/S395 did not yet exist).
**Verdict per row:** **S387 MATCH · S392 MATCH · S395 MATCH** (sha256, gate-quote line numbers, anchor-locator
bounds all agree). Two **weakens-the-claim** defects and one **cosmetic** defect found in the surrounding
machinery — none of them falsifies a frozen predicate; all are ROUTED findings for round 57.

## Deliverables

- `.ufo/waves/round-56/w3/R56W3ScoutRows3b/receipts/rows.md` — full per-row receipts (fetch commands, digests,
  quote locations, locator bounds, cross-row checks).
- `.ufo/waves/round-56/w3/R56W3ScoutRows3b/receipts/S387.md`, `…/S392.md`, `…/S395.md` — the same per-row
  receipts, one file per row.
- This report: `.ufo/waves/round-56/w3/R56W3ScoutRows3b.md`.

Nothing else in the lane was written. No tracked file edited; no git/jj mutation against the lane, the fleet
repo or any sibling lane. All clones/fixtures lived under
`/fast/scratch/hyaku/mado-r56/R56W3ScoutRows3b/` and were removed before this yield.

## Tooling

No tool was installed, upgraded or removed — the task needed only what the host already had.
Versions used: `python3 -I` 3.14.8, `curl` 8.23.0 (OpenSSL 3.6.5), `git` 2.56.0, `openssl` (for git blob sha1 via
`hashlib`). No pacman/uv/npx/cargo transaction was run, so the pacman guard and the update-safety gate were not
engaged.

---

## 1. What I attacked

For each of S387, S392, S395 in `corpus/SOURCES.md` at `0f3a5436…`:

1. fetch the row's URL myself (curl into my scratch) and sha256 the bytes;
2. compare that digest with (a) the row's own anchor cell and (b) `frozen-tables-v2.json` where the row is
   tabled, and with the committed pin blob in the lane;
3. locate the gate quote in the upstream bytes and report its line number;
4. check the anchor locators stay within the file's line count.

Then the falsification part: does anything in the landed machinery actually *check* these three rows? A MATCH
that no instrument could ever distinguish from a wrong row is not evidence.

## 2. What I did (commands and decisive output)

### 2.1 Independent fetch (twice each, identical)

```
$ curl -sS --fail --max-time 60 -o ConfigManager.cpp \
  https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp
$ curl -sS --fail --max-time 60 -o ConfigWatcher.cpp \
  https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/inotify/ConfigWatcher.cpp

$ sha256sum ConfigManager.cpp ConfigWatcher.cpp
9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b  ConfigManager.cpp
8383b8abf43159986bc4127ad7a4416fbf1c3527bf388fa1ce052c28c40d516c  ConfigWatcher.cpp
$ stat -c '%s bytes' ConfigManager.cpp ConfigWatcher.cpp
90963 bytes
4046 bytes
```

Refetched once more in the same run: byte-identical digests both times.

### 2.2 Three-way digest comparison

| row | my fetch | row's anchor cell | `frozen-tables-v2.json` | committed pin at tip |
|---|---|---|---|---|
| S387 | `9db68cf4…5be62b` | `9db68cf4…5be62b` | `c1.pin_sha256["Hyprland-legacy-ConfigManager.cpp"] = 9db68cf4…5be62b` | `9db68cf4…5be62b` |
| S392 | `8383b8ab…0d516c` | `8383b8ab…0d516c` | `c1.pin_sha256["Hyprland-ConfigWatcher.cpp"] = 8383b8ab…0d516c` | `8383b8ab…0d516c` |
| S395 | `9db68cf4…5be62b` | `9db68cf4…5be62b` | `c1.pin_sha256["Hyprland-legacy-ConfigManager.cpp"] = 9db68cf4…5be62b` | `9db68cf4…5be62b` |

`cmp` of my fetch against the lane's committed pin: byte-identical for both files.

**Independent of the lane:** the git blob sha1 of my fetched bytes equals the blob sha the GitHub tree API
reports for that path at commit `efb50993…` — `4f1b11f25f227cca2a3e5b16c8de760b76231bf5` (ConfigManager.cpp,
90963 B) and `bcd710ffb101ab328bf117ed011671971da76826` (ConfigWatcher.cpp, 4046 B). So the bytes are *that
commit's blob*, not merely a stable-looking URL.

**Method control on a non-GitHub host** (the same round's S390, whose pin the frozen table also freezes):
`https://man7.org/linux/man-pages/man7/inotify.7.html` → `79f5ab18e2fc423631cf4949ef82ca1384844353ea11a4dba42e1a77e8fdd8fd`,
44066 B, 920 lines — equal to `c1.pin_sha256["man7-inotify.7.html"]` and to the committed pin; K29's quote at
line 186, K30's at line 262, as the frozen table states.

### 2.3 Gate quotes located in the upstream bytes

| row | quote | upstream line | content at that line |
|---|---|---|---|
| S387 | `"source= skipping directory {}", value);` | **1844** | `Log::logger->log(Log::WARN, "source= skipping directory {}", value);` |
| S392 | `.file = WD->file,` (entry E03) | **106** | `                .file = WD->file,` (inside `m_watchCallback(SConfigWatchEvent{ … })`, 105–107) |
| S395 | `resetHLConfig();` (E05) | **630** | `    resetHLConfig();` (in `CConfigManager::CConfigManager()`, opened at 480) |
| S395 | `m_configCurrentPath          = value;` (E06) | **1838** | `            m_configCurrentPath          = value;` (in `handleSource`, opened at 1802) |
| S395 | `return m_configPaths;` (E07) | **2134** | `    return m_configPaths;` (in `getConfigPaths`, opened at 2133) |

Whole-file occurrence scans (so the quote is not an accident of a substring): `"source= skipping directory {}",
value);` → `[1844]`; `.file = WD->file,` → `[106]`; `m_configCurrentPath          = value;` → `[1838]`;
`return m_configPaths;` → `[2134]`; `resetHLConfig();` → `[630, 731, 755]` — 630 is the constructor call (E05's
claim), 731 the `reload()` call, 755 the `verify()` call.

The lesson `## Gate` table has a located-quote row for S383–S391 only; S392–S395 are described in prose in the
same section ("S392 `ConfigWatcher.cpp:106` … S395 `ConfigManager.cpp:630,1838,2134`"). Their located quotes are
the entry's E03/E05/E06/E07 rows, and all five locate as tabulated above.

All eight frozen K-row quotes that cite S387 (`c1.k` K17–K24) were re-located at their frozen lines in the
upstream bytes: 1079, 1080, 1070, 776, 1836, 1835, 1844, 1816 — all present verbatim.

### 2.4 Anchor locators vs. the file's line count

`ConfigManager.cpp` = 2185 lines on `\n`-split (90963 B); `ConfigWatcher.cpp` = 112 lines (4046 B).

- S387 locators `776,1070,1079-1080,1816,1835-1836,1844` — every one ≤ 2185 and pointing at the quoted statement.
- S392 locator `106` — ≤ 112, pointing at `.file = WD->file,`.
- S395 locators `630,1838,2134` — every one ≤ 2185, pointing at the quoted statement.

No locator is past EOF; the widest (`2134`) is 51 lines short of the file end.

### 2.5 Falsification: mutation tests on copies (lane untouched)

I cloned the lane once (`git clone --shared` into my scratch; `git rev-parse --show-toplevel` asserted equal to
the clone dir before the first commit; commits as `-c user.name=ctl -c user.email=ctl@ctl`) and mutated **copies**
of `corpus/SOURCES.md` only, one mutation per commit, each run against the landed counters.

| # | mutation | counter | result | reading |
|---|---|---|---|---|
| M1 | S387 anchor cell `776,…` → `ConfigManager.cpp:1-9999` (past EOF) | C1 counter | `scope=22/30 … verdict=TARGET_MISSED missed=scope:K17,…,scope:K24` (rc 1) | **detected** — the C1 scope leg reads the anchor cell |
| M2 | S392 anchor cell `ConfigWatcher.cpp:106` → `1-9999` | C1 counter | `rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none` (rc 0) | **NOT detected** (see Defect 1) |
| M2 | same mutant | criterion-107 checker (`.ufo/waves/round-56/w3/R56W3ExecCrit107Build/quality/check-anchor-cover.py`) | `ANCHOR_COVER: row=E03 sid=S392 line=106 … locators=1-9999 eof=checked verdict=MISS reason=past-eof` → `CHECK107: rows=39 covered=38 miss=1 verdict=FAIL` (rc 1) | detected by the *uncommitted* w3 checker |
| M2 | same mutant | the w1 draft checker committed at tip (`.ufo/waves/round-56/w1/R56RevQuality/check-anchor-cover.py`) | `CHECK107: rows=39 covered=39 miss=0 verdict=OK` (rc 0) | **NOT detected** — the draft has no EOF clause |
| M3 | S392 status cell `mined` → `unmined` | C1 counter | `verdict=TARGET_MET missed=none` (rc 0) | **NOT detected** (Defect 1) |
| M4 | S395 status cell `mined` → `unmined` | C1 counter | `verdict=TARGET_MET missed=none` (rc 0) | **NOT detected** (Defect 1) |
| M5 | S392 used-by emptied | C3 counter | `missing=1 … verdict=TARGET_MISSED missed=missing` (rc 1) | detected (C3 reads all rows' used-by) |
| M6 | S395 used-by emptied | C3 counter | `missing=1 … verdict=TARGET_MISSED missed=missing` (rc 1) | detected |
| M7 | S387 URL path `src/config/legacy/ConfigManager.cpp` → `src/config/ConfigManager.cpp` | C1 counter | `sources=22/30 … new_rows=7/8 verdict=TARGET_MISSED missed=source_cell:K17,…,source_cell:K24,new_rows` (rc 1) | **detected** (S387 is in `c1.rows`) |
| M8 | S392 URL path → `src/config/legacy/ConfigWatcher.cpp` (a non-existent path) | C1 counter | `verdict=TARGET_MET missed=none` (rc 0) | **NOT detected** (Defect 1) |

### 2.6 Landed counters re-run at the tip (read-only)

```
$ python3 -I quality/counters/c1-r56-autoreload-entry.py --repo . --rev 0f3a5436… --work <scratch>
MADO_AUTORELOAD_ENTRY: rev=0f3a54361a9824484d0801679ceb1fd8ac7c32e1 rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none   (rc 0)

$ python3 -I quality/counters/c3-r56-used-by.py --repo . --rev 0f3a5436… --work <scratch>
MADO_USED_BY: rev=0f3a54361a9824484d0801679ceb1fd8ac7c32e1 entries=71 rows=332 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none   (rc 0)
```

`sha256sum .ufo/waves/round-56/frozen-tables-v2.json` → `9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2`,
equal to the digest printed in `claims-frozen-v2.md`.

### 2.7 Row-existence and provenance facts

- `git show 28fc86ac:corpus/SOURCES.md | grep -cE '^\| S(392|395) \|'` → **0**: S392/S395 did not exist at
  attempt-1's fetch revision; they were added later, at `b70f6a2c` ("anchor rows S392-S395"), which is a
  **descendant** of the v2 freeze commit `323a69c`. S387's row text is byte-identical at `28fc86ac` and the tip
  (row-line sha256 `e49ccbba34cea7f32248aab7849bba91719d991d29a4c7c89f1bfde5d7130d58` at both).
- `frozen-tables-v2.json` `c1.rows` / `c1.new_row_ids` = S383–S390 only. **S392 and S395 are not frozen row ids.**
  Their *pins* are frozen (`c1.pin_sha256` covers both pin files), so the byte claim is still bound; the row id and
  its anchor cell are not.
- No duplicate registry ids: `grep -oE '^\| S[0-9]+ '` over the tip's `SOURCES.md` → 332 rows, no id repeated.
- Upstream has **three** files named `ConfigManager.cpp` at `efb50993…` (`src/config/`, `src/config/legacy/`,
  `src/config/lua/`), so the anchor cell's basename alone is ambiguous; the URL and the frozen `c1.pin_suffix`
  disambiguate to `src/config/legacy/ConfigManager.cpp`, and the quoted lines exist only there (checked: the
  `src/config/` file is 83 lines; the `src/config/lua/` file is 1401 lines and its 776/1070 carry different text).
  `ConfigWatcher.cpp` is unique upstream.

## 3. Results per row

| row | sha256 vs anchor cell | sha256 vs frozen table | gate quote line | locators within line count | verdict |
|---|---|---|---|---|---|
| S387 | equal (`9db68cf4…5be62b`) | equal (`c1.pin_sha256`, `c1.rows["S387"]`) | 1844 | yes (8/8 ≤ 2185) | **MATCH** |
| S392 | equal (`8383b8ab…0d516c`) | equal (`c1.pin_sha256` for the pin it names); row id not in `c1.rows` | 106 | yes (1/1 ≤ 112) | **MATCH** |
| S395 | equal (`9db68cf4…5be62b`) | equal (`c1.pin_sha256` for the pin it names); row id not in `c1.rows` | 630 / 1838 / 2134 | yes (3/3 ≤ 2185) | **MATCH** |

## 4. Defects

### Defect 1 — S392 and S395 are outside every landed counter's reach (severity: **weakens the claim**)

**Input.** `frozen-tables-v2.json` `c1.rows` and `c1.new_row_ids` contain S383–S390 only (8 ids); the C1 counter's
`new_rows` leg iterates exactly `c1["new_row_ids"]` and its `source_cell_ok`/`scope_ok` legs are driven from
`c1["k"]`/`c1["h"]` (K01–K30, H01–H03) — no E row and no S391–S395 id appears in the frozen tables. The
counter's `scope` leg therefore never reads the S392 or S395 anchor cell.

**Evidence (mutation tests on copies).** M2 (S392 anchor widened past EOF), M3 (S392 status `mined`→`unmined`),
M4 (S395 status `mined`→`unmined`), M8 (S392 URL repointed to a non-existent path) each leave the C1 counter at
`verdict=TARGET_MET missed=none` (rc 0). The same mutation class on S387 (M1 anchor past EOF, M7 URL repointed)
is caught: `scope=22/30 … missed=scope:K17,…` and `sources=22/30 … missed=source_cell:K17,…,new_rows`.

**Reading.** S392 and S395 are the two rows created to carry the E-row anchors (lesson: "S392-S395 are
supplementary same-URL rows … whose anchors cover the E-row lines the wave-2 anchor check found outside
S383, S387, S388 and S389"). They are the *only* place the E rows' lines are bound to a registry row, and no
landed counter at the tip checks them. The counter's `scope=30/30` and `new_rows=8/8` therefore carry **no
statement** about S392/S395: a wrong anchor cell for either row still yields `TARGET_MET`.

**Not a claim falsification.** No frozen predicate is broken by this; the frozen sentence is literally true
(`new_rows=8/8`, `scope=30/30`). It is a coverage gap in the instrument relative to the rows the lesson says
were added.

**Fix path (routed, round 57 — nothing edited here).** Two independent routes:
(a) extend the frozen tables' `c1.rows` / `new_row_ids` to S391–S395 and add an E-row class to the counter's
scope leg — this changes a frozen predicate, so it is a round-57 re-registration, not a wave edit;
(b) land the criterion-107 checker (the one built in this wave at
`.ufo/waves/round-56/w3/R56W3ExecCrit107Build/quality/check-anchor-cover.py`, which *does* catch M2: `miss=1
verdict=FAIL`) as the committed QUALITY-107 instrument — `corpus/QUALITY.md` at the tip already states that the
w1 draft "is a draft instrument, not the gate of this criterion" and that the enforcement at landing is the C1
counter's K-rows-only scope leg. Landing the w3 checker closes the E-row anchor half of this gap without
touching a frozen table.

### Defect 2 — the criterion-107 checker committed at the tip cannot see a past-EOF anchor (severity: **weakens the claim**)

**Input.** `corpus/QUALITY.md` (tip) requires the criterion-107 check to bound every locator by the pin's line
count (`eof=checked`) and to fail on `miss>0`. The only checker committed at the tip is the wave-1 draft
`.ufo/waves/round-56/w1/R56RevQuality/check-anchor-cover.py`.

**Evidence.** On the M2 mutant (S392 anchor `1-9999`) the draft checker prints
`CHECK107: rows=39 covered=39 miss=0 verdict=OK` (rc 0) — it has no EOF clause, so a locator far past the file
end passes as "covered". The w3-built checker on the same mutant prints
`ANCHOR_COVER: row=E03 sid=S392 line=106 … eof=checked verdict=MISS reason=past-eof` →
`CHECK107: rows=39 covered=38 miss=1 verdict=FAIL` (rc 1). `corpus/QUALITY.md` itself already records the
draft's missing EOF / reversed-range / duplicate-id / malformed-pin clauses, so this is a **known** gap that the
w3 checker exists to close — I am recording that the closure is real and demonstrable, not that it is
unrecorded.

**Reading.** At the tip, no committed instrument rejects a past-EOF locator in any registry row (the C1 counter's
scope leg only covers S383–S389; the draft 107 checker has no EOF clause). Landing the w3 checker fixes it.

### Defect 3 — lesson prose understates the supplementary rows' size and the counter's row count (severity: **cosmetic**)

**Input.** `corpus/lessons/round-56.md` line 37: "S392-S395 re-state S383/S387/S388/S389 for three lines each".
Measured at the tip: S392 carries **one** locator (`ConfigWatcher.cpp:106`), S393 one (`MiscFunctions.cpp:66`),
S394 one (`HyprCtl.cpp:1190`), S395 three (`630,1838,2134`); S391 two (`18,21`). So "three lines each" is true
only for S395.

**Input.** Same file, line 28: the "Admitted" list enumerates S383–S391 and mentions S392–S395 in prose, while
`frozen-tables-v2.json` and the counter's `new_rows=8/8` cover S383–S390 only (S391 is not in the frozen tables
either). A reader reconciling the lesson's "Rows S383-S391" against the counter's `8/8` will find a gap that the
lesson does not name. The lesson does record S391's separate status ("S391 matched the committed pin and has no
frozen hash, see M56-9") but says nothing equivalent for S392–S395.

**Reading.** Both are documentation-accuracy defects, not claim defects; the lesson is not edited by me (frozen
files are never edited, and `corpus/lessons/round-56.md` is a tracked lane file outside my write scope).

## 5. Anything I could not verify

- **No independent third-party re-fetch of the S392/S395 bytes exists in attempt-1.** The wave-2 scout reports at
  `28fc86ac` cover S383–S391 only (`R56W2ScoutRows1..5.md` mention S383–S391); the wave-2 files that mention
  S392/S395 (`R56W2RevHarmWatch.md`, `R56W2RevAuditC/F.md`, `R56W2RevDocs.md`, `R56W2ConnCross.md`) discuss them
  as uncommitted working-tree edits, not as fetched bytes. The upstream bytes behind S392/S395 were therefore
  never independently re-fetched before this seat. My fetch is the first, and a peer scout (`R56W3ScoutRows1b`)
  independently reports the same digests, line counts and quote locations for all nine round-56 URLs at the tip —
  consistent, but a peer in the same wave, not an attempt-1 witness.
- **Semantic reading of the pins.** I verified byte identity, quote presence at the stated lines, locator bounds
  and (for S395) that the quoted lines sit in the functions the row names. I did **not** audit whether the
  proposition wording of every E/K row is the best reading of its line; that is the wave-2 sentence-to-pin audit's
  job and is not counted by any counter (declared in `registration-v2.md` §"What v2 does not repair").
- **The three `ConfigManager.cpp` files upstream.** I confirmed which file the rows point at and that the quoted
  lines exist only in `src/config/legacy/ConfigManager.cpp`, but I did not fetch the other two files' full
  contents for a line-by-line diff (I fetched them and compared the relevant line numbers only).
- **Live host state.** Not in scope; this seat read no host configuration, ran no `hyprctl`, and touched no
  `/proc` entry.
- **`check-locators.py` misses on the entry** (`locators=62 miss=8`, e.g. `Hyprland-legacy-ConfigManager.cpp:485`
  and `:1079-1082`) were observed but are **not** attributed to these three rows' anchors: the tool checks prose
  fragments against receipt lines, and the same tool reports misses on the round-51 entry (`miss=7`), so it is a
  pre-existing lane-wide pattern. The 485/1079-1082 references are *prose* citations (`:485` the constructor's
  `m_configPaths.emplace_back(m_mainConfigPath)`, `:1079-1082` the `init` callback block) that lie outside the
  S387/S395 anchor locators; no registry row anchors 1081 or 485. That is consistent with the registry design
  (rows anchor the lines the E/K rows cite) and is not reported as a defect of S387/S392/S395.

## 6. Summary

- **S387, S392, S395: MATCH.** Independent upstream bytes at `efb50993…` equal the anchor cells, the frozen
  `c1.pin_sha256` entries and the committed pins; the gate quotes sit at 1844 (S387), 106 (S392) and
  630/1838/2134 (S395); every anchor locator is inside its pin's line count (2185 and 112).
- The falsification pass found that **S392 and S395 are not covered by any landed counter** (Defect 1) and that the
  **criterion-107 checker committed at the tip lacks the EOF clause** (Defect 2). Both are routed findings for
  round 57; the w3-built criterion-107 checker already closes Defect 2 and the E-row-anchor half of Defect 1.
- One cosmetic lesson-prose defect (Defect 3).
- No frozen predicate, counter, kill rule or target was edited, widened or bypassed; the lane's tracked files
  were not touched.

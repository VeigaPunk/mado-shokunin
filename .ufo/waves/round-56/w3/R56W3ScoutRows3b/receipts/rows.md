# R56W3ScoutRows3b — receipts/rows.md

Seat: R56W3ScoutRows3b (scout, round-56 wave 3, attempt 2).
Scope: registry rows **S387, S392, S395** re-opened independently at lane tip
`0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (second sample; attempt-1's wave-2 scouts fetched at
`28fc86ac`, and S392/S395 did not exist at that revision).

All paths below are absolute. Scratch: `/fast/scratch/hyaku/mado-r56/R56W3ScoutRows3b/` (removed at yield).
Python: `python3 -I` (3.14.8). curl 8.23.0. git 2.56.0. No tools installed, upgraded or removed.

---

## S387

Registry row at tip (`corpus/SOURCES.md`, line 337):

```
| S387 | Hyprland 0.56.2 legacy config manager - watcher callback and source handling |
  https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp
  | code | A | the legacy manager's watcher callback, ...
  | ConfigManager.cpp:776,1070,1079-1080,1816,1835-1836,1844 @ efb50993780079460b0cbed1363e2166a2de1d9f;
    pin .ufo/waves/round-56/fetch/Hyprland-legacy-ConfigManager.cpp 90963 B
    sha256:9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b | ... | mined | 2026-10-28 | on-release | corpus/knowledge/hyprland-config-autoreload-r56.md |
```

### Fetch (independent)

```
$ curl -sS --fail --max-time 60 -o ConfigManager.cpp \
  https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp
$ sha256sum ConfigManager.cpp
9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b  ConfigManager.cpp
$ stat -c '%s bytes' ConfigManager.cpp
90963 bytes
```

Refetched twice in the same run: identical sha256 both times.

### sha256 comparison (three independent objects)

| object | sha256 | source |
|---|---|---|
| my fetch (upstream raw, `efb50993…`) | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` | this seat |
| S387 anchor cell | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` | SOURCES.md:337 @ tip |
| `frozen-tables-v2.json` `c1.pin_sha256["Hyprland-legacy-ConfigManager.cpp"]` | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` | .ufo/waves/round-56/frozen-tables-v2.json |
| committed pin blob at tip | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` | `git show 0f3a5436:…/fetch/Hyprland-legacy-ConfigManager.cpp` |

Byte-for-byte identity with the committed pin (`cmp` → identical, no output).

Independent git-object check (not the lane's): the git blob sha1 of my fetched bytes equals the blob sha
GitHub's tree API reports for `src/config/legacy/ConfigManager.cpp` at commit `efb50993…`:
`4f1b11f25f227cca2a3e5b16c8de760b76231bf5`, size 90963 — i.e. the bytes are that commit's blob, not merely a
stable-looking URL.

### Gate quote (lesson `## Gate` table)

Lesson row: `| S387 | …/src/config/legacy/ConfigManager.cpp | "source= skipping directory {}", value); (:1844) |`

Located in the upstream bytes at **line 1844**:

```
ConfigManager.cpp:1844:             Log::logger->log(Log::WARN, "source= skipping directory {}", value);
```

The quote is present verbatim on that line and occurs exactly once in the file
(occurrence scan: `[1844]`).

### Anchor locators vs. the file's line count

`ConfigManager.cpp` has 2185 lines when split on `\n` (90963 B, upstream blob).

| locator | line present | in range 1..2185 |
|---|---|---|
| 776 | `m_configPaths.clear();` | yes |
| 1070 | `Config::Supplementary::refresher()->scheduleRefresh(Supplementary::REFRESH_ALL);` | yes |
| 1079 | `Config::watcher()->setOnChange([this](const CConfigWatcher::SConfigWatchEvent& e) {` | yes |
| 1080 | `Log::logger->log(Log::DEBUG, "CConfigManager: file {} modified, reloading", e.file);` | yes |
| 1816 | `if (auto r = glob(absolutePath(rawpath, m_configCurrentPath).c_str(), GLOB_TILDE, nullptr, glob_buf.get()); r != 0) {` | yes |
| 1835 | `if (std::filesystem::is_regular_file(file_status)) {` | yes |
| 1836 | `m_configPaths.emplace_back(value);` | yes |
| 1844 | (gate quote above) | yes |

All 8 K-row quotes that cite S387 in `frozen-tables-v2.json` (`c1.k` K17–K24) were re-located in the upstream
bytes at their frozen lines: K17@1079 ✓, K18@1080 ✓, K19@1070 ✓, K20@776 ✓, K21@1836 ✓, K22@1835 ✓,
K23@1844 ✓, K24@1816 ✓.

### Verdict

**MATCH** — sha256 equal to the anchor cell and the frozen table; gate quote at line 1844; every anchor locator
inside the pin's line count and pointing at the quoted statement.

---

## S392

Registry row at tip (`corpus/SOURCES.md`, line 342):

```
| S392 | Hyprland 0.56.2 config watcher - the event passed to the change callback |
  https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/inotify/ConfigWatcher.cpp
  | code | A | the line that copies the matched watch's stored file name into the callback event |
  | ConfigWatcher.cpp:106 @ efb50993780079460b0cbed1363e2166a2de1d9f;
    pin .ufo/waves/round-56/fetch/Hyprland-ConfigWatcher.cpp 4046 B
    sha256:8383b8abf43159986bc4127ad7a4416fbf1c3527bf388fa1ce052c28c40d516c | .file = WD->file, … | mined | 2026-10-28 | on-release | corpus/knowledge/hyprland-config-autoreload-r56.md |
```

### Fetch (independent)

```
$ curl -sS --fail --max-time 60 -o ConfigWatcher.cpp \
  https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/inotify/ConfigWatcher.cpp
$ sha256sum ConfigWatcher.cpp
8383b8abf43159986bc4127ad7a4416fbf1c3527bf388fa1ce052c28c40d516c  ConfigWatcher.cpp
$ stat -c '%s bytes' ConfigWatcher.cpp
4046 bytes
```

Refetched twice in the same run: identical sha256 both times.

### sha256 comparison

| object | sha256 | source |
|---|---|---|
| my fetch (upstream raw, `efb50993…`) | `8383b8abf43159986bc4127ad7a4416fbf1c3527bf388fa1ce052c28c40d516c` | this seat |
| S392 anchor cell | `8383b8abf43159986bc4127ad7a4416fbf1c3527bf388fa1ce052c28c40d516c` | SOURCES.md:342 @ tip |
| `frozen-tables-v2.json` `c1.pin_sha256["Hyprland-ConfigWatcher.cpp"]` | `8383b8abf43159986bc4127ad7a4416fbf1c3527bf388fa1ce052c28c40d516c` | frozen-tables-v2.json |
| committed pin blob at tip | `8383b8abf43159986bc4127ad7a4416fbf1c3527bf388fa1ce052c28c40d516c` | `git show 0f3a5436:…/fetch/Hyprland-ConfigWatcher.cpp` |

`cmp` with the committed pin: byte-identical.

Git-blob cross-check: blob sha1 of my bytes = `bcd710ffb101ab328bf117ed011671971da76826` = the sha GitHub's
tree API reports for `src/config/shared/inotify/ConfigWatcher.cpp` at `efb50993…` (size 4046).

Note: S392 itself is **not** a key in `frozen-tables-v2.json` `c1.rows` / `c1.new_row_ids` (those hold
S383–S390 only) — S392 was added after the v2 freeze, at commit `b70f6a2c` ("anchor rows S392-S395"), which is a
descendant of the freeze commit `323a69c`. The pin it names (`Hyprland-ConfigWatcher.cpp`) **is** frozen in
`c1.pin_sha256`, so the byte claim is still bound by the frozen table; the *row id* is not. Same situation for S395.

### Located quote (E03, the proposition this row was created for)

The lesson `## Gate` table has a located-quote row for S383–S391 only; S392–S395 are described in prose in the
same section ("S392 `ConfigWatcher.cpp:106` …"). The proposition quote for S392 is the entry's E03 row:
`` `.file = WD->file,` `` at `Hyprland-ConfigWatcher.cpp:106`.

Located in the upstream bytes at **line 106**:

```
ConfigWatcher.cpp:105:             m_watchCallback(SConfigWatchEvent{
ConfigWatcher.cpp:106:                 .file = WD->file,
ConfigWatcher.cpp:107:             });
```

Present verbatim at line 106, and the occurrence scan over the whole file returns `[106]` only — one occurrence.

### Anchor locator vs. the file's line count

`ConfigWatcher.cpp` has 112 lines when split on `\n` (4046 B).

| locator | line present | in range 1..112 |
|---|---|---|
| 106 | `                .file = WD->file,` | yes |

### Verdict

**MATCH** — sha256 equal to the anchor cell and to the frozen `c1.pin_sha256` entry for the pin it names;
E03's quote located at line 106; the anchor locator is inside the pin's line count and points at the quoted line.

---

## S395

Registry row at tip (`corpus/SOURCES.md`, line 345):

```
| S395 | Hyprland 0.56.2 legacy config manager - constructor reset, nested current path and the path accessor |
  https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp
  | code | A | the constructor call to resetHLConfig, the nested current-path assignment in handleSource and the getConfigPaths accessor |
  | ConfigManager.cpp:630,1838,2134 @ efb50993780079460b0cbed1363e2166a2de1d9f;
    pin .ufo/waves/round-56/fetch/Hyprland-legacy-ConfigManager.cpp 90963 B
    sha256:9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b | … | mined | 2026-10-28 | on-release | corpus/knowledge/hyprland-config-autoreload-r56.md |
```

### Fetch (independent)

Same upstream URL as S387 (same file); fetched independently in the same run and hashed separately:

```
$ sha256sum ConfigManager.cpp
9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b  ConfigManager.cpp
$ stat -c '%s bytes' ConfigManager.cpp
90963 bytes
```

### sha256 comparison

| object | sha256 | source |
|---|---|---|
| my fetch (upstream raw, `efb50993…`) | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` | this seat |
| S395 anchor cell | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` | SOURCES.md:345 @ tip |
| `frozen-tables-v2.json` `c1.pin_sha256["Hyprland-legacy-ConfigManager.cpp"]` | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` | frozen-tables-v2.json |
| committed pin blob at tip | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` | `git show 0f3a5436:…/fetch/Hyprland-legacy-ConfigManager.cpp` |

### Located quotes (E05, E06, E07 — the propositions this row was created for)

Located in the upstream bytes:

| E-row | quote | upstream line | content at that line |
|---|---|---|---|
| E05 | `resetHLConfig();` | **630** | `    resetHLConfig();` (inside `CConfigManager::CConfigManager()`, opened at line 480) |
| E06 | `m_configCurrentPath          = value;` | **1838** | `            m_configCurrentPath          = value;` (inside `CConfigManager::handleSource`, opened at line 1802) |
| E07 | `return m_configPaths;` | **2134** | `    return m_configPaths;` (inside `CConfigManager::getConfigPaths`, opened at line 2133) |

All three present verbatim at the stated lines. Occurrence scans over the whole 2185-line file:
`resetHLConfig();` → `[630, 731, 755]` (630 is the constructor call, 731 the `reload()` call, 755 the `verify()`
call — E05's line 630 is the constructor one, as claimed); `m_configCurrentPath          = value;` → `[1838]`;
`return m_configPaths;` → `[2134]`.

### Anchor locators vs. the file's line count

| locator | in range 1..2185 | content |
|---|---|---|
| 630 | yes | `    resetHLConfig();` |
| 1838 | yes | `            m_configCurrentPath          = value;` |
| 2134 | yes | `    return m_configPaths;` |

### Verdict

**MATCH** — sha256 equal to the anchor cell and to the frozen `c1.pin_sha256` entry for the pin it names;
E05/E06/E07 quotes located at lines 630/1838/2134; all three locators inside the pin's line count.

---

## Cross-row checks run at the tip (context for the MATCH verdicts)

1. **S390 pin (control, same round, same method)** — the man7 page was fetched with the same procedure to test the
   method on a non-GitHub host:
   `https://man7.org/linux/man-pages/man7/inotify.7.html` → `79f5ab18e2fc423631cf4949ef82ca1384844353ea11a4dba42e1a77e8fdd8fd`,
   44066 B, 920 lines; equal to `c1.pin_sha256["man7-inotify.7.html"]` and to the committed pin; K29's quote
   ("File opened for writing was closed.") at line 186 and K30's ("Don't dereference `<i>pathname</i>` if it is a
   symbolic link.") at line 262 — both as the frozen table states.

2. **Basename ambiguity (S387/S395 name `ConfigManager.cpp`, upstream has three files with that basename).**
   `git ls-tree -r` of the upstream commit at `efb50993…` (fetched with `--depth 1 --filter=tree:0` into scratch):
   `src/config/ConfigManager.cpp`, `src/config/legacy/ConfigManager.cpp`, `src/config/lua/ConfigManager.cpp`.
   The rows' URL pins `src/config/legacy/ConfigManager.cpp`; the anchor cell's basename alone is ambiguous, but
   the *URL* and the pin path disambiguate, and the frozen table's `c1.pin_suffix` maps the pin to
   `src/config/legacy/ConfigManager.cpp`. The other two same-named files do not contain the quoted lines
   (checked: `src/config/ConfigManager.cpp` is 83 lines; `src/config/lua/ConfigManager.cpp` is 1401 lines and its
   line 776/1070 hold different text). No defect — recorded because the anchor cell carries only the basename.

3. **Row identity vs. attempt-1.** `git show 28fc86ac:corpus/SOURCES.md | grep -cE '^\| S(392|395) \|'` → 0:
   S392/S395 did not exist at attempt-1's fetch revision; S387's row text is byte-identical between
   `28fc86ac` and the tip (`sha256` of the S387 row line: `e49ccbba34cea7f32248aab7849bba91719d991d29a4c7c89f1bfde5d7130d58`
   at both revisions).

4. **Landed counters re-run at the tip** (read-only, `--work` in scratch):
   ```
   MADO_AUTORELOAD_ENTRY: rev=0f3a54361a9824484d0801679ceb1fd8ac7c32e1 rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none
   MADO_USED_BY: rev=0f3a54361a9824484d0801679ceb1fd8ac7c32e1 entries=71 rows=332 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none
   ```
   `frozen-tables-v2.json` sha256 at the tip = `9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2`
   (equals the value printed in `claims-frozen-v2.md`).

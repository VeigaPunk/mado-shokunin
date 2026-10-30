# R56W3ScoutRows4b — receipts/rows.md (per row)

Seat: R56W3ScoutRows4b. Scored tree: `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`
(lane `/home/vgpnk/Projects/shokunin/mado-shokunin`). Re-check date: 2026-10-30.
Second sample: attempt-1's wave-2 scouts fetched at `28fc86ac`; every byte below was
re-fetched from the network at the tip.

All commands ran from scratch `/fast/scratch/hyaku/mado-r56/R56W3ScoutRows4b/`.
Every registry/entry/table read used `git -C <lane> show <rev>:<path>` (read-only) or
`git archive`; the working tree was never scored.

---

## Fetch log (independent, at the tip)

```
$ curl -sS --max-time 60 -o fetch/MiscFunctions.cpp -w 'HTTP %{http_code} %{size_download}\n' \
    'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/MiscFunctions.cpp'
HTTP 200 29785
$ curl -sS --max-time 60 -o fetch/HyprCtl.cpp -w 'HTTP %{http_code} %{size_download}\n' \
    'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp'
HTTP 200 97582

$ sha256sum fetch/MiscFunctions.cpp fetch/HyprCtl.cpp
065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9  fetch/MiscFunctions.cpp
798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa  fetch/HyprCtl.cpp

$ wc -c -l fetch/MiscFunctions.cpp fetch/HyprCtl.cpp
  844  29785 fetch/MiscFunctions.cpp
 2346  97582 fetch/HyprCtl.cpp
```

Response headers (provenance: pinned blob served by GitHub raw, not a moving branch):

```
HTTP/2 200 ; content-length: 29785 ; etag: "992f4229f6d985c1c7a0668bb9538ad753c3f6f61abf94a61bcfa1167aa38e14"
HTTP/2 200 ; content-length: 97582 ; etag: "56c1f1143beddbbccf8d9e500550d75263f2bf13a96d5d3c37ed919ac4b6f5bb"
```

Cross-check that the pinned upstream commit is the release tag the rows claim (rows say
"Hyprland 0.56.2"):

```
$ git ls-remote --tags https://github.com/hyprwm/Hyprland.git 'v0.56.2*'
efb50993780079460b0cbed1363e2166a2de1d9f	refs/tags/v0.56.2
```

Committed lane pins at the tip (read-only `git show`) equal the fetched bytes:

```
$ git show 0f3a5436:.ufo/waves/round-56/fetch/Hyprland-MiscFunctions.cpp | sha256sum
065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9  -
$ git show 0f3a5436:.ufo/waves/round-56/fetch/Hyprland-HyprCtl.cpp | sha256sum
798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa  -
```

---

## S388 — Hyprland 0.56.2 helper functions — absolutePath for home and relative paths

- **URL** (row cell 3 at the tip): `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/MiscFunctions.cpp`
- **Anchor cell** (cell 7 at the tip): `MiscFunctions.cpp:65,68 @ efb50993780079460b0cbed1363e2166a2de1d9f; pin .ufo/waves/round-56/fetch/Hyprland-MiscFunctions.cpp 29785 B sha256:065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9`
- **sha256 (fetched)** `065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9` — vs anchor cell `0654182…c1d9`: **MATCH**; byte count `29785` = anchor `29785 B`: **MATCH**.
- **frozen-tables-v2.json** `c1.pin_sha256["Hyprland-MiscFunctions.cpp"]` = `065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9` — **MATCH**. `c1.rows["S388"] = "Hyprland-MiscFunctions.cpp"` — the row is tabled and its pin agrees.
- **Gate quote located** (lesson `corpus/lessons/round-56.md` §Gate table row S388: `static const char* const ENVHOME = getenv("HOME");` (:65)): upstream line **65** — exact, single occurrence in the file.
- **Second locator**: `auto currentDir = currentPath.substr(0, currentPath.find_last_of('/'));` at upstream line **68** — exact, single occurrence (S388 anchor lists `65,68`).
- **Anchor locators within the file's line count**: file has 844 newline-terminated lines (845 split-lines); max locator 68 ≤ 845. **PASS** (registration-v2 E3 bound).
- **Frozen table quotes for this sid** (`c1.k`): K25 @65 `static const char* const ENVHOME = getenv("HOME");`, K26 @68 `auto currentDir = currentPath.substr(0, currentPath.find_last_of('/'));` — both byte-exact at the cited lines.
- **Verdict: MATCH** (sha256, gate quote, locator bound, K quotes).

## S389 — Hyprland 0.56.2 hyprctl request path — misc:disable_autoreload branch and reload call

- **URL** (cell 3): `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp`
- **Anchor cell** (cell 7): `HyprCtl.cpp:1223,1276 @ efb50993780079460b0cbed1363e2166a2de1d9f; pin .ufo/waves/round-56/fetch/Hyprland-HyprCtl.cpp 97582 B sha256:798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa`
- **sha256 (fetched)** `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` — vs anchor cell: **MATCH**; `97582` = anchor `97582 B`: **MATCH**.
- **frozen-tables-v2.json** `c1.pin_sha256["Hyprland-HyprCtl.cpp"]` = same hash — **MATCH**; `c1.rows["S389"] = "Hyprland-HyprCtl.cpp"` — tabled, agrees.
- **Gate quote located** (lesson §Gate row S389: `if (COMMAND.contains("misc:disable_autoreload"))` (:1223)): upstream line **1223** — exact, single occurrence. The guarded call `Config::watcher()->update();` is the next line (**1224**).
- **Second locator**: `Config::mgr()->reload();` at upstream line **1276** — exact, single occurrence (anchor lists `1223,1276`).
- **Anchor locators within the file's line count**: file has 2346 newline-terminated lines (2347 split-lines); max locator 1276 ≤ 2347. **PASS**.
- **Frozen table quotes for this sid** (`c1.k`): K27 @1223 `if (COMMAND.contains("misc:disable_autoreload"))`, K28 @1276 `Config::mgr()->reload();` — both byte-exact at the cited lines.
- **Scope of the two locators is two different functions, and the row says so**: 1223 sits in `dispatchKeyword` (def. at 1160), 1276 in `reloadRequest` (def. at 1260). `reloadRequest` returns `"ok"` on the `full-reset` branch at 1273 before falling through to 1276, so the row's "the path that is not full-reset ends by calling `Config::mgr()->reload()`" holds for the quoted lines.
- **Verdict: MATCH**.

## S393 — Hyprland 0.56.2 helper functions — the tilde replacement call

- **URL** (cell 3): same MiscFunctions.cpp URL as S388 (identical bytes re-fetched; the fetch log above applies).
- **Anchor cell** (cell 7): `MiscFunctions.cpp:66 @ efb50993780079460b0cbed1363e2166a2de1d9f; pin .ufo/waves/round-56/fetch/Hyprland-MiscFunctions.cpp 29785 B sha256:065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9`
- **sha256 (fetched)** `065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9` — vs anchor cell: **MATCH**; `29785` = anchor `29785 B`: **MATCH**.
- **frozen-tables-v2.json**: the row id `S393` is **not** in `frozen-tables-v2.json` (v2 froze `c1.rows`/`c1.new_row_ids` = S383–S390 only); the pin it names is `Hyprland-MiscFunctions.cpp`, whose frozen hash `c1.pin_sha256` is the same `0654182…c1d9` — **MATCH** on the pin the row cites, but the row itself is outside the frozen table (see defect D1).
- **Gate quote located**: S393 is one of the "supplementary same-URL rows" the lesson names at §Gate (`S392-S395 are supplementary same-URL rows … S393 MiscFunctions.cpp:66`). The quoted line is `value.replace(0, 1, std::string(ENVHOME));` — upstream line **66**, exact, single occurrence. Upstream context (lines 61–83) confirms the row's claim: line 64 tests `value[0] == '~'`, line 66 replaces exactly one byte at offset 0, and the function contains no `getpwnam`/`getpwuid`/passwd lookup anywhere (`grep -n 'getpwnam\|getpwuid\|struct passwd' fetch/MiscFunctions.cpp` → no output).
- **Anchor locators within the file's line count**: locator 66 ≤ 845. **PASS**.
- **Verdict: MATCH** (bytes, quote, locator bound); **untabled in the frozen v2 table** — D1.

## S394 — Hyprland 0.56.2 hyprctl request path — the keyword parse call

- **URL** (cell 3): same HyprCtl.cpp URL as S389 (identical bytes re-fetched; the fetch log above applies).
- **Anchor cell** (cell 7): `HyprCtl.cpp:1190 @ efb50993780079460b0cbed1363e2166a2de1d9f; pin .ufo/waves/round-56/fetch/Hyprland-HyprCtl.cpp 97582 B sha256:798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa`
- **sha256 (fetched)** `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` — vs anchor cell: **MATCH**; `97582` = anchor `97582 B`: **MATCH**.
- **frozen-tables-v2.json**: `S394` is **not** in the frozen v2 table; the pin it names (`Hyprland-HyprCtl.cpp`) has frozen hash `c1.pin_sha256` = the same `798b7c…b91fa` — **MATCH** on the pin the row cites; the row itself is outside the frozen table (D1).
- **Gate quote located**: lesson §Gate names S394 as `HyprCtl.cpp:1190`. The quoted line is `std::string retval = mgr->parseKeyword(COMMAND, VALUE);` — upstream line **1190**, exact, single occurrence. Upstream context (1160–1190) confirms: `dispatchKeyword` early-returns `"keyword can't work with non-legacy parsers. Use eval."` at 1162–1163 when the manager is not legacy, and `mgr` is the `dynamicPointerCast` to `Config::Legacy::CConfigManager` at 1165 — the entry's E04 wording ("the route exists only when the config manager is the legacy one") is exactly what the upstream lines show.
- **Anchor locators within the file's line count**: locator 1190 ≤ 2347. **PASS**.
- **Verdict: MATCH** (bytes, quote, locator bound); **untabled in the frozen v2 table** — D1.

---

## Machine checks behind the per-row verdicts

### Quote locator (exact-line, unique) — upstream bytes

```
S388a: file=MiscFunctions.cpp lines=845 exact_line_hits=[65] at_line_65=True
S388b: file=MiscFunctions.cpp lines=845 exact_line_hits=[68] at_line_68=True
S389a: file=HyprCtl.cpp        lines=2347 exact_line_hits=[1223] at_line_1223=True
S389b: file=HyprCtl.cpp        lines=2347 exact_line_hits=[1276] at_line_1276=True
S393 : file=MiscFunctions.cpp lines=845 exact_line_hits=[66]  at_line_66=True
S394 : file=HyprCtl.cpp        lines=2347 exact_line_hits=[1190] at_line_1190=True
```

### Row cells at the tip (11-cell table shape, header `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`)

```
--- S388 ncells=11 id='S388' kind='code' tier='A' status='mined' opened='2026-10-28' recheck='on-release' used-by='corpus/knowledge/hyprland-config-autoreload-r56.md'
    used-by present on disk at tip: True
    entry cites sid: True
--- S389 ncells=11 id='S389' kind='code' tier='A' status='mined' opened='2026-10-28' recheck='on-release' used-by='corpus/knowledge/hyprland-config-autoreload-r56.md'
    used-by present on disk at tip: True
    entry cites sid: True
--- S393 ncells=11 id='S393' kind='code' tier='A' status='mined' opened='2026-10-28' recheck='on-release' used-by='corpus/knowledge/hyprland-config-autoreload-r56.md'
    used-by present on disk at tip: True
    entry cites sid: True
--- S394 ncells=11 id='S394' kind='code' tier='A' status='mined' opened='2026-10-28' recheck='on-release' used-by='corpus/knowledge/hyprland-config-autoreload-r56.md'
    used-by present on disk at tip: True
    entry cites sid: True
```

### Anchor-coverage sweep over **all 42** entry rows (K+E+H), using the counter's own `scope_covers` verbatim

```
entry rows parsed: 42
SKIPPED (no frozen pin):
   ('E08', 'S391', 'Hyprland-PropRefresher.hpp', 18, 'pin not in frozen pin_suffix')
   ('E09', 'S391', 'Hyprland-PropRefresher.hpp', 21, 'pin not in frozen pin_suffix')
ANCHOR-COVER MISSES: 0
```

(E08/E09 skipped only because `Hyprland-PropRefresher.hpp` is absent from the frozen
`c1.pin_suffix` map — a frozen-table gap, not an anchor gap; checked by hand below.)

The same sweep at attempt-1's revision `28fc86ac` (for contrast — this is what changed):

```
28fc86ac anchor-cover misses: 6
   ('E01','S388','Hyprland-MiscFunctions.cpp',66, ...)
   ('E03','S383','Hyprland-ConfigWatcher.cpp',106, ...)
   ('E04','S389','Hyprland-HyprCtl.cpp',1190, ...)
   ('E05','S387','Hyprland-legacy-ConfigManager.cpp',630, ...)
   ('E06','S387','Hyprland-legacy-ConfigManager.cpp',1838, ...)
   ('E07','S387','Hyprland-legacy-ConfigManager.cpp',2134, ...)
0f3a5436 anchor-cover misses: 0
```

### EOF bound (registration-v2 E3) for every new row S383–S395

```
S383 pin=Hyprland-ConfigWatcher.cpp     pin_lines=112  locators=['33-34,46,54-56,60,67,69,105'] max=105  over=[]
S384 pin=Hyprland-ConfigValues.cpp      pin_lines=735  locators=['492']                             max=492  over=[]
S385 pin=Hyprland-PropRefresher.cpp     pin_lines=160  locators=['148-149']                        max=149  over=[]
S386 pin=Hyprland-EventLoopManager.cpp  pin_lines=283  locators=['71,128']                         max=128  over=[]
S387 pin=Hyprland-legacy-ConfigManager.cpp pin_lines=2185 locators=['776,1070,1079-1080,1816,1835-1836,1844'] max=1844 over=[]
S388 pin=Hyprland-MiscFunctions.cpp      pin_lines=845  locators=['65,68']                          max=68   over=[]
S389 pin=Hyprland-HyprCtl.cpp            pin_lines=2347 locators=['1223,1276']                      max=1276 over=[]
S390 pin=man7-inotify.7.html             pin_lines=920  locators=['186,262']                        max=262  over=[]
S391 no frozen pin_suffix match
S392 pin=Hyprland-ConfigWatcher.cpp      pin_lines=112  locators=['106']                            max=106  over=[]
S393 pin=Hyprland-MiscFunctions.cpp      pin_lines=845  locators=['66']                             max=66   over=[]
S394 pin=Hyprland-HyprCtl.cpp            pin_lines=2347 locators=['1190']                           max=1190 over=[]
S395 pin=Hyprland-legacy-ConfigManager.cpp pin_lines=2185 locators=['630,1838,2134']               max=2134 over=[]
```

S391 by hand (pin not in the frozen map): anchor `PropRefresher.hpp:18,21`, pin
`Hyprland-PropRefresher.hpp` = 41 split-lines; lines 18 and 21 exist and are exact:

```
18         REFRESH_CONFIG_WATCHER     = (1 << 8),
21         REFRESH_ALL = std::numeric_limits<std::underlying_type_t<ePropRefreshProp>>::max(),
```

### Counter legs that consume these four rows, re-run at the tip

```
$ python3 -I quality/counters/c1-r56-autoreload-entry.py --repo . --rev 0f3a5436… --work <scratch>
MADO_AUTORELOAD_ENTRY: rev=0f3a54361a9824484d0801679ceb1fd8ac7c32e1 rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none
exit=0

$ python3 -I quality/counters/c3-r56-used-by.py --repo . --rev 0f3a5436… --work <scratch>
MADO_USED_BY: rev=0f3a54361a9824484d0801679ceb1fd8ac7c32e1 entries=71 rows=332 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none
exit=0
```

`scope=30/30` is the leg that consumes the S388/S389 anchors (K25/K26/K27/K28);
`missing=0` is the leg that consumes the S388/S389/S393/S394 `used-by` cells.

### Registry census (`sources-census.sh validate`, tip tree extracted read-only with `git archive`)

Run against the extracted tip tree as a directory (so `used-by` paths resolve on disk):

```
$ sources-census.sh validate --today 2026-10-30 tip-tree
tip-tree	W04	S388 duplicate url …/src/helpers/MiscFunctions.cpp across scopes
tip-tree	W04	S389 duplicate url …/src/debug/HyprCtl.cpp across scopes
tip-tree	W04	S393 duplicate url …/src/helpers/MiscFunctions.cpp across scopes
tip-tree	W04	S394 duplicate url …/src/debug/HyprCtl.cpp across scopes
```

No E-code fires for S388/S389/S393/S394 (the only E11s are for rows whose `used-by`
points at `tools/*.py` etc. that are outside the `corpus/` subtree of my extraction).

**Negative control** for the E11 question (attempt-1 reported E11 for these rows in
`--file` mode and called it a harness artifact): with the entry file removed from the
extracted tree, E11 fires for exactly these four rows; with it present, it does not.

```
$ (tip-tree2 = tip-tree minus corpus/knowledge/hyprland-config-autoreload-r56.md)
tip-tree2	E11	S388 missing used-by corpus/knowledge/hyprland-config-autoreload-r56.md
tip-tree2	E11	S389 missing used-by corpus/knowledge/hyprland-config-autoreload-r56.md
tip-tree2	E11	S393 missing used-by corpus/knowledge/hyprland-config-autoreload-r56.md
tip-tree2	E11	S394 missing used-by corpus/knowledge/hyprland-config-autoreload-r56.md
```

So E11 on these rows is a function of whether the cited entry is on disk, not a lane
defect — confirmed by construction, not assumed.

### Row identity across the two samples

```
S388 28fc86ac=32b0dfa9…  tip=32b0dfa9…  SAME
S389 28fc86ac=d1c68185…  tip=d1c68185…  SAME
S393 28fc86ac=e3b0c442…  tip=1fc67e36…  DIFF   (row absent at 28fc86ac; present at the tip)
S394 28fc86ac=e3b0c442…  tip=10418a84…  DIFF   (row absent at 28fc86ac; present at the tip)
```

S393/S394 are new rows at the tip (the `e3b0c442…` hash is the empty-string digest of
a failed grep). Attempt-1's wave-2 scouts could not have re-opened them: the rows did
not exist at `28fc86ac`. That is the substantive difference between the two samples.

### Ancillary (not in my row set, recorded for the closure)

S390's man7 page re-fetched as a fetch-method control:
`sha256 79f5ab18e2fc423631cf4949ef82ca1384844353ea11a4dba42e1a77e8fdd8fd`, 44066 B,
919 lines — equals the S390 anchor cell and `c1.pin_sha256`; the two gate quotes sit at
lines 186 (`File opened for writing was closed.`) and 262
(`Don't dereference <i>pathname</i> if it is a symbolic link.`), each unique.

S391's pin re-fetched as a second control: `sha256 37acaaf16a24dcfe89d0702818b82d300d0da5e91ef1ba47494f7fd2ab0af2d0`,
1322 B — equals the S391 anchor cell and the committed lane pin.

---

## Defects (with the input that shows them)

**D1 — cosmetic — S393 and S394 are not in the frozen v2 table.**
Input: `frozen-tables-v2.json` contains `c1.rows` = {S383…S390} and
`c1.new_row_ids` = [S383…S390]; the string `S393` / `S394` does not occur in the file
(`'S392' False 'S393' False 'S394' False 'S395' False`; S391 likewise absent).
Consequence: the C1 counter's `scope:<id>` leg (K rows only, per `registration.md`
§C1 leg table) never evaluates the S393/S394 anchors, and `new_rows` stays 8/8 by
construction (`NEW_ROWS_DENOM = 8`). The rows' own bytes and quotes are nevertheless
correct (verified above). The lesson discloses the S392–S395 rows as "supplementary
same-URL rows (new ids)" added for E-row anchor coverage; the frozen v2 table was
written before them and not re-registered. **Not blocking any registered predicate**;
flagged so the closure knows the frozen table's row set and the registry's row set
differ by five rows (S391–S395). Round-57 material if the table is ever re-frozen.

**D2 — cosmetic — the two W04 duplicate-URL warnings on these rows are lane-wide, not new.**
Input: census output above; the same W04 class fires for 32 other rows (S030, S042,
S045, S097, S119–S121, S303, S307, S317, S318, S320, S321, S324, S326, S327, S332,
S353, S354, S364, S366, S368, S370, S371, S373, S380–S382, S384, S387, S392, S395).
The script's own header says "warnings do not affect clean lanes". QUALITY 17 asks for a
distinct-scope review of repeated canonical URLs; the lesson carries that review for
S383–S391 and states S392–S395 "re-state S383/S387/S388/S389 for three lines each …
carry no new claim. Verdict: distinct scopes". My scope reading agrees for the two rows
I attacked: S393's scope ("the line that replaces a leading tilde with the HOME
string") is a distinct line-anchored proposition from S388's ("how absolutePath expands
a leading ~ and resolves a relative path against the directory of the current file"),
and S394's is distinct from S389's — they differ in anchor line and in proposition, not
only in wording. No E04 (duplicate URL **and** scope) fires.

**D3 — cosmetic — the E-row anchor gap that attempt-1 recorded is closed at the tip.**
Input: the anchor-coverage sweep above (6 misses at `28fc86ac`, 0 at the tip). This is
a change, not a defect, but attempt-1's wave-2 reports and the attempt-1 lesson text
still describe the older state, so the closure should read the current state.

## Not verified

- The commit's tree at `efb5099…` beyond the four files I fetched and the two control
  pins (S390/S391); I did not re-fetch the other seven pins.
- `hyprctl`/host-side behaviour: out of scope for a registry-row seat, and the host
  guard forbids state-changing compositor commands.
- The GitHub REST API check of the commit object returned **HTTP 403** (unauthenticated
  rate limit), so the commit metadata was confirmed via `git ls-remote --tags` (tag
  `v0.56.2` → `efb5099…`) instead. No claim depends on the API response.
- QUALITY-17 distinct-scope review is a human-review item; I checked the W04/E04 codes
  and the scope wording, not the closure's adjudication.
- No tools were installed or upgraded (curl, git, python3, sha256sum all present); no
  pacman transaction; no state-changing host command; no write outside this
  deliverable directory and my scratch.

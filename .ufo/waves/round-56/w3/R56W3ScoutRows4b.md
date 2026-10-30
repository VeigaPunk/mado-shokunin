# R56W3ScoutRows4b — independent re-open of registry rows S388, S389, S393, S394 (wave w3, attempt 2, falsify)

Scored tree: `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (lane `/home/vgpnk/Projects/shokunin/mado-shokunin`).
Re-check date: 2026-10-30. Second sample: attempt-1's wave-2 scouts fetched at `28fc86ac`; every
byte below was re-fetched from the network at the tip. All registry/entry/table content was read via
`git -C <lane> show <rev>:<path>` (read-only) or `git archive`; the working tree was never scored.

## Attack

Each of the four rows claims a URL, a byte count, a sha256, a set of line locators and a proposition.
Three things could be false at the tip and were not false at `28fc86ac`:

1. the upstream bytes behind the row's sha256 (the pins are committed blobs; nothing forces them to
   equal today's upstream);
2. the row's line locators (a locator can point at a line that no longer holds the quoted text, or
   can run past the end of the file);
3. the anchor-coverage contract — the wave-2 anchor check (R56W2CritScopeFix / R56W2ScoutRows3)
   found six E rows quoting lines no registry row's anchor covered (E01@66 vs S388's {65,68},
   E04@1190 vs S389's {1223,1276}, plus E03/E05/E06/E07). S392–S395 were then added to the registry
   to close exactly those gaps. Attempt-1's wave-2 scouts could not check this: S392–S395 did not
   exist at `28fc86ac` (verified: `git show 28fc86ac:corpus/SOURCES.md | grep -cE '^\| S39[2-5] \|'` = 0).

So I fetched both URLs myself, hashed the bytes, compared against the row anchor cells and against
`frozen-tables-v2.json`, located the gate quotes in the upstream bytes, checked the locators against
the files' line counts, and then swept anchor coverage over **all 42** entry rows using the
counter's own `scope_covers` function.

## Verdict

| row | upstream fetch | sha256 vs anchor cell | vs frozen-tables-v2.json | gate quote located | locators within line count | anchor cover (all 42 entry rows) | verdict |
|---|---|---|---|---|---|---|---|
| S388 | HTTP 200, 29785 B, 844 lines | **MATCH** | **MATCH** (`c1.pin_sha256`) | **MATCH** (65, 68) | PASS (68 ≤ 845) | PASS | **MATCH** |
| S389 | HTTP 200, 97582 B, 2346 lines | **MATCH** | **MATCH** (`c1.pin_sha256`) | **MATCH** (1223, 1276) | PASS (1276 ≤ 2347) | PASS | **MATCH** |
| S393 | HTTP 200, 29785 B, 844 lines | **MATCH** | pin **MATCH**; row itself absent from the frozen table (D1) | **MATCH** (66) | PASS (66 ≤ 845) | PASS | **MATCH** |
| S394 | HTTP 200, 97582 B, 2346 lines | **MATCH** | pin **MATCH**; row itself absent from the frozen table (D1) | **MATCH** (1190) | PASS (1190 ≤ 2347) | PASS | **MATCH** |

No blocking defect. Three cosmetic findings and one state-change note below.

## What I did — commands and decisive output

### 1. Independent fetch (the attack core)

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
```

Response headers confirm a pinned blob, not a moving branch:
`HTTP/2 200`, `content-length: 29785`, `etag: "992f4229…aa38e14"`; and `content-length: 97582`,
`etag: "56c1f114…4b6f5bb"`.

The upstream commit really is the release the rows name:

```
$ git ls-remote --tags https://github.com/hyprwm/Hyprland.git 'v0.56.2*'
efb50993780079460b0cbed1363e2166a2de1d9f	refs/tags/v0.56.2
```

Committed lane pins at the tip equal the fetched bytes (read-only `git show`):
`.ufo/waves/round-56/fetch/Hyprland-MiscFunctions.cpp` → `0654182…c1d9`;
`.ufo/waves/round-56/fetch/Hyprland-HyprCtl.cpp` → `798b7c…b91fa`.

### 2. Gate quotes located in the upstream bytes (exact line, unique occurrence)

```
S388a: file=MiscFunctions.cpp lines=845 exact_line_hits=[65]  at_line_65=True
S388b: file=MiscFunctions.cpp lines=845 exact_line_hits=[68]  at_line_68=True
S389a: file=HyprCtl.cpp        lines=2347 exact_line_hits=[1223] at_line_1223=True
S389b: file=HyprCtl.cpp        lines=2347 exact_line_hits=[1276] at_line_1276=True
S393 : file=MiscFunctions.cpp lines=845 exact_line_hits=[66]  at_line_66=True
S394 : file=HyprCtl.cpp        lines=2347 exact_line_hits=[1190] at_line_1190=True
```

Upstream context confirming each proposition (not just the quote):

- S388/S393, `MiscFunctions.cpp:61-83`: line 64 `if (value[0] == '~') {`, line 65 `static const char* const ENVHOME = getenv("HOME");`, line 66 `value.replace(0, 1, std::string(ENVHOME));`, line 68 `auto currentDir = currentPath.substr(0, currentPath.find_last_of('/'));`. `grep -n 'getpwnam\|getpwuid\|struct passwd' fetch/MiscFunctions.cpp` → **no output**, so S393's "no user lookup" holds within the pinned file.
- S389, `HyprCtl.cpp:1223` `if (COMMAND.contains("misc:disable_autoreload"))` → next line `Config::watcher()->update();` (1224). `HyprCtl.cpp:1260-1279` is `reloadRequest`; the `full-reset` branch returns `"ok"` at 1273 and the fall-through reaches 1276 `Config::mgr()->reload();` — S389's "the path that is not full-reset ends by calling `Config::mgr()->reload()`" is what the lines show.
- S394, `HyprCtl.cpp:1160-1190` is `dispatchKeyword`; it early-returns `"keyword can't work with non-legacy parsers. Use eval."` at 1162-1163 and `mgr` is the `dynamicPointerCast` to `Config::Legacy::CConfigManager` (1165); line 1190 is `std::string retval = mgr->parseKeyword(COMMAND, VALUE);`. The entry's E04 qualifier ("the route exists only when the config manager is the legacy one") matches the upstream lines exactly.

### 3. sha256 against the row anchor cells and the frozen table

```
S388 anchor cell : 29785 B sha256:065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9
S393 anchor cell : 29785 B sha256:065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9
S389 anchor cell : 97582 B sha256:798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa
S394 anchor cell : 97582 B sha256:798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa
fetched          : 0654182…c1d9 (29785 B) / 798b7c…b91fa (97582 B)          → all MATCH
frozen c1.pin_sha256["Hyprland-MiscFunctions.cpp"] = 0654182…c1d9             → MATCH
frozen c1.pin_sha256["Hyprland-HyprCtl.cpp"]         = 798b7c…b91fa             → MATCH
frozen c1.rows["S388"]="Hyprland-MiscFunctions.cpp"  c1.rows["S389"]="Hyprland-HyprCtl.cpp"
```

Frozen-table file itself verified at the tip:
`git show 0f3a5436:.ufo/waves/round-56/frozen-tables-v2.json | sha256sum` →
`9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2` — the value the brief names.

### 4. Anchor locators vs the files' line counts (registration-v2 E3)

```
S383 pin_lines=112  locators=['33-34,46,54-56,60,67,69,105'] max=105  over=[]
S384 pin_lines=735  locators=['492']                             max=492  over=[]
S385 pin_lines=160  locators=['148-149']                        max=149  over=[]
S386 pin_lines=283  locators=['71,128']                         max=128  over=[]
S387 pin_lines=2185 locators=['776,1070,1079-1080,1816,1835-1836,1844'] max=1844 over=[]
S388 pin_lines=845  locators=['65,68']                          max=68   over=[]
S389 pin_lines=2347 locators=['1223,1276']                      max=1276 over=[]
S390 pin_lines=920  locators=['186,262']                        max=262  over=[]
S392 pin_lines=112  locators=['106']                            max=106  over=[]
S393 pin_lines=845  locators=['66']                             max=66   over=[]
S394 pin_lines=2347 locators=['1190']                           max=1190 over=[]
S395 pin_lines=2185 locators=['630,1838,2134']                  max=2134 over=[]
```

S391 by hand (its pin is not in the frozen `pin_suffix` map): anchor `PropRefresher.hpp:18,21`,
pin 41 split-lines, lines 18 and 21 present and exact.

### 5. Anchor-coverage sweep over **all 42** entry rows (the attempt-1 gap, re-derived)

I reused the counter's own `scope_covers` verbatim from
`quality/counters/c1-r56-autoreload-entry.py` at the tip and applied it to every K/E row of the
entry (not just the K rows the frozen leg counts):

```
entry rows parsed: 42
SKIPPED (no frozen pin): E08/E09 (S391 — pin absent from c1.pin_suffix)
ANCHOR-COVER MISSES: 0
```

The same sweep at attempt-1's revision, for contrast:

```
28fc86ac anchor-cover misses: 6
   E01→S388:66   E03→S383:106   E04→S389:1190
   E05→S387:630  E06→S387:1838  E07→S387:2134
0f3a5436 anchor-cover misses: 0
```

**The E-row anchor gap attempt-1 recorded is closed at the tip** — the S392–S395 rows do what the
lesson says they do ("supplementary same-URL rows … whose anchors cover the E-row lines the wave-2
anchor check found outside S383, S387, S388 and S389").

### 6. Counter legs that consume these rows, re-run at the tip

```
$ python3 -I quality/counters/c1-r56-autoreload-entry.py --repo . --rev 0f3a5436… --work <scratch>
MADO_AUTORELOAD_ENTRY: rev=0f3a54361a9824484d0801679ceb1fd8ac7c32e1 rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none
exit=0
$ python3 -I quality/counters/c3-r56-used-by.py --repo . --rev 0f3a5436… --work <scratch>
MADO_USED_BY: rev=0f3a54361a9824484d0801679ceb1fd8ac7c32e1 entries=71 rows=332 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none
exit=0
```

`scope=30/30` consumes the S388/S389 anchors (K25/K26/K27/K28); `missing=0` consumes the
S388/S389/S393/S394 `used-by` cells.

### 7. Registry census on the tip tree (extracted read-only with `git archive`)

```
$ sources-census.sh validate --today 2026-10-30 tip-tree
tip-tree	W04	S388 duplicate url …/src/helpers/MiscFunctions.cpp across scopes
tip-tree	W04	S389 duplicate url …/src/debug/HyprCtl.cpp across scopes
tip-tree	W04	S393 duplicate url …/src/helpers/MiscFunctions.cpp across scopes
tip-tree	W04	S394 duplicate url …/src/debug/HyprCtl.cpp across scopes
```

No E-code fires for these four rows. **Negative control** (the entry file removed from the extracted
tree) makes E11 fire for exactly these four rows, so E11 on them is a function of whether the cited
entry is on disk — a `--file`-mode artifact, confirmed by construction rather than assumed:

```
tip-tree2	E11	S388 missing used-by corpus/knowledge/hyprland-config-autoreload-r56.md
tip-tree2	E11	S389 missing used-by corpus/knowledge/hyprland-config-autoreload-r56.md
tip-tree2	E11	S393 missing used-by corpus/knowledge/hyprland-config-autoreload-r56.md
tip-tree2	E11	S394 missing used-by corpus/knowledge/hyprland-config-autoreload-r56.md
```

### 8. Row identity across the two samples

```
S388 28fc86ac=32b0dfa9…  tip=32b0dfa9…  SAME
S389 28fc86ac=d1c68185…  tip=d1c68185…  SAME
S393 28fc86ac=<absent>   tip=1fc67e36…  DIFF (new row at the tip)
S394 28fc86ac=<absent>   tip=10418a84…  DIFF (new row at the tip)
```

### 9. Ancillary controls (outside my four rows, recorded for the closure)

S390's man7 page re-fetched: `sha256 79f5ab18e2fc423631cf4949ef82ca1384844353ea11a4dba42e1a77e8fdd8fd`,
44066 B, 919 lines — equals the S390 anchor cell and `c1.pin_sha256`; gate quotes at lines 186
(`File opened for writing was closed.`) and 262 (`Don't dereference <i>pathname</i> if it is a
symbolic link.`), each unique. S391's pin re-fetched: `sha256 37acaaf16a24dcfe89d0702818b82d300d0da5e91ef1ba47494f7fd2ab0af2d0`,
1322 B — equals the S391 anchor cell and the committed lane pin. Both confirm the fetch method.

## Defects

**D1 — cosmetic — S393 and S394 are absent from the frozen v2 table.**
Input: `frozen-tables-v2.json` holds `c1.rows` = {S383…S390} and `c1.new_row_ids` = [S383…S390];
`'S392' False 'S393' False 'S394' False 'S395' False` (S391 likewise absent), while the tip
`corpus/SOURCES.md` contains S383–S395. Consequences: the C1 `scope:<id>` leg (K rows only, per
`registration.md` §C1 leg table) never evaluates the S393/S394 anchors, and `new_rows` is 8/8 by
construction (`NEW_ROWS_DENOM = 8`). The rows' own bytes, quotes and locators are correct (checked
above). The frozen table predates the S392–S395 addition and was not re-registered. Severity:
**does not block any registered predicate**; it means the frozen row set and the registry row set
differ by five rows (S391–S395), which the closure should know. Round-57 material if the table is
ever re-frozen.

**D2 — cosmetic — the W04 duplicate-URL warnings on these rows are lane-wide, not new.**
Input: the census output above; the same W04 class fires for 32 other rows (S030, S042, S045, S097,
S119–S121, S303, S307, S317, S318, S320, S321, S324, S326, S327, S332, S353, S354, S364, S366, S368,
S370, S371, S373, S380–S382, S384, S387, S392, S395). The script's header: "warnings do not affect
clean lanes". QUALITY 17 asks for a distinct-scope review of repeated canonical URLs; the lesson
carries that review and states S392–S395 "carry no new claim. Verdict: distinct scopes". On the two
rows I attacked that reading holds: S393's scope ("the line that replaces a leading tilde with the
HOME string") is a different line-anchored proposition from S388's ("how absolutePath expands a
leading ~ and resolves a relative path against the directory of the current file"), and likewise S394
vs S389 — they differ in anchor line and in proposition, not only in wording. No E04 (duplicate URL
**and** scope) fires.

**D3 — cosmetic — attempt-1's wave-2 reports and the attempt-1 lesson text still describe the
pre-S392–S395 anchor state.** Input: the anchor-coverage sweep (6 misses at `28fc86ac`, 0 at the
tip). This is a change rather than a defect, but the closure should read the current state: the
E-row anchor gap is closed, and the wave-2 "ANCHOR_COVER … verdict=MISS" lines no longer apply to
the tip.

## Not verified / limits

- The rest of the commit's tree at `efb5099…` beyond the four files I fetched and the two control
  pins (S390/S391); the other seven pins were not re-fetched.
- Host/compositor behaviour: out of scope for a registry-row seat, and the host guard forbids
  state-changing compositor commands (`hyprctl` keyword/dispatch/reload were never run).
- The GitHub REST commit check returned **HTTP 403** (unauthenticated rate limit); the commit/tag
  identity was confirmed via `git ls-remote --tags` instead. No claim depends on the API response.
- QUALITY-17 distinct-scope review is a human-review item; I checked the W04/E04 codes and the scope
  wording, not the closure's adjudication.
- Tooling: nothing installed or upgraded (curl, git, python3, sha256sum, `sources-census.sh` all
  already present); **no pacman transaction**; no state-changing host command; no write outside my
  deliverable directory and my scratch. Scratch `/fast/scratch/hyaku/mado-r56/R56W3ScoutRows4b/` was
  removed after the receipts were copied.

## Deliverables

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ScoutRows4b.md` (this report)
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ScoutRows4b/receipts/rows.md`
  (per-row receipts: S388, S389, S393, S394, with sha256, gate-quote line numbers, locator bounds,
  verdicts, defects, not-verified list)
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ScoutRows4b/receipts/census-validate-tip-tree.out`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ScoutRows4b/receipts/census-negative-control.out`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ScoutRows4b/receipts/fetch-Hyprland-MiscFunctions.cpp`
  (sha256 `065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9`)
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ScoutRows4b/receipts/fetch-Hyprland-HyprCtl.cpp`
  (sha256 `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa`)

Report: .ufo/waves/round-56/w3/R56W3ScoutRows4b.md

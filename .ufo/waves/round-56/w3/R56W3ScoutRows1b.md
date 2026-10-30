# R56W3ScoutRows1b — independent re-open of registry rows S383/S384 (and the whole round-56 row set), wave 3

Seat: scout. Scored tree: `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (lane `/home/vgpnk/Projects/shokunin/mado-shokunin`),
read via `git show <rev>:<path>`; the working tree was never used as evidence. Scratch:
`/fast/scratch/hyaku/mado-r56/R56W3ScoutRows1b/` (removed before yield).

**Second sample.** Attempt-1's wave-2 scouts (`w2/R56W2ScoutRows1..5.md`) fetched at `28fc86ac`. This seat re-derives every
row at the tip. The rows S383-S391 are byte-identical between the two revisions (`git diff 28fc86ac 0f3a5436 -- corpus/SOURCES.md`
= 4 inserted rows only, S392-S395); the pins are byte-identical too (checked per file below), so the upstream bytes could not
have changed underneath. This is nevertheless a fresh fetch of every URL, not a replay of attempt-1's numbers.

## Attack

The seat item names what is attacked: nobody had re-fetched the upstream bytes **at the tip** and re-derived the row anchors
independently of the committed pin files. Wave-1's row author wrote S383/S384 and the gate quotes *from the pin files*; the
frozen table's `pin_sha256` was computed from those same pins. So the frozen sha can only prove "the pin equals the frozen
hash", never "the pin equals upstream". The upstream check is the only step that closes that gap, and it is the step I attack.

## Verdict

| row | bytes vs anchor cell | bytes vs committed pin blob @ tip | bytes vs `frozen-tables-v2.json` | gate quote located in upstream bytes | anchor locators within pin length | verdict |
|---|---|---|---|---|---|---|
| **S383** | MATCH | MATCH | MATCH | **line 34** (gate claims 34) MATCH | 33-34,46,54-56,60,67,69,105 vs 112 lines — all inside | **MATCH** |
| **S384** | MATCH | MATCH | MATCH | **line 492** (gate claims 492) MATCH | 492 vs 735 lines — inside | **MATCH** |
| S385 | MATCH | MATCH | MATCH | line 148 MATCH | 148-149 vs 160 — inside | MATCH |
| S386 | MATCH | MATCH | MATCH | line 128 MATCH | 71,128 vs 283 — inside | MATCH |
| S387 | MATCH | MATCH | MATCH | line 1844 MATCH | max 1844 vs 2185 — inside | MATCH |
| S388 | MATCH | MATCH | MATCH | line 65 MATCH | 65,68 vs 845 — inside | MATCH |
| S389 | MATCH | MATCH | MATCH | line 1223 MATCH | 1223,1276 vs 2347 — inside | MATCH |
| S390 | MATCH | MATCH | MATCH | line 186 MATCH | 186,262 vs 920 — inside | MATCH |
| S391 | MATCH | MATCH | **not tabled** (see D2) | line 18 MATCH | 18,21 vs 41 — inside | MATCH on content; D2 process finding |
| S392 | MATCH | MATCH | MATCH | (no gate row; anchor :106 = `.file = WD->file,`) | 106 vs 112 — inside | MATCH |
| S393 | MATCH | MATCH | MATCH | (no gate row; anchor :66 = `value.replace(0, 1, std::string(ENVHOME));`) | 66 vs 845 — inside | MATCH |
| S394 | MATCH | MATCH | MATCH | (no gate row; anchor :1190 = `std::string retval = mgr->parseKeyword(COMMAND, VALUE);`) | 1190 vs 2347 — inside | MATCH |
| S395 | MATCH | MATCH | MATCH | (no gate row; anchors :630/:1838/:2134) | max 2134 vs 2185 — inside | MATCH |

**No defect blocks or weakens any round-56 claim.** Two findings below: one weakens a *process* statement, one is a
*cosmetic/registry-hygiene* item outside the round-56 claims.

## What I did, commands, decisive output

### 1. Independent fetch of the row URLs (the core attack)

Every URL fetched by me into scratch; hashes over the raw response bytes.

```
B=https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f
curl -sS -m 90 -o "$out" -w "%{http_code}" "$B/$src"        # src = the path in the row's cell 2
curl -sS -m 90 -o man7-inotify.7.html -w "%{http_code}" https://man7.org/linux/man-pages/man7/inotify.7.html
sha256sum <each file>
```

```
ConfigWatcher.cpp 200 4046  8383b8abf43159986bc4127ad7a4416fbf1c3527bf388fa1ce052c28c40d516c
ConfigValues.cpp  200 59222 a76f05079454e1f6d4402144e1673cc1cb890d285fbeb947d5afdb004ad97754
PropRefresher.cpp 200 5139 65f01a1a50ef05ecb1630f8fd30bbbac91029b29f6b4b6bc3f353d0bb4b2817b
EventLoopManager.cpp 200 9073 104ff43a4c02fcc88e8711cade68becd3a1fe099e970e4b1306774c85dd76f7c
ConfigManager.cpp 200 90963 9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b
MiscFunctions.cpp 200 29785 065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9
HyprCtl.cpp 200 97582 798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa
PropRefresher.hpp 200 1322 37acaaf16a24dcfe89d0702818b82d300d0da5e91ef1ba47494f7fd2ab0af2d0
man7-inotify.7.html 200 44066 79f5ab18e2fc423631cf4949ef82ca1384844353ea11a4dba42e1a77e8fdd8fd
```

All nine are HTTP 200. Each equals (i) the sha256 in the row's own anchor cell, (ii) the sha256 of the **committed pin blob at
the tip** (`git show 0f3a5436:.ufo/waves/round-56/fetch/<file> | sha256sum`) and (iii) `frozen-tables-v2.json`
`c1.pin_sha256[<file>]` — for the eight rows the frozen table tabled (S391 is not tabled; D2). Byte sizes equal the anchor
cells' "N B" too. Pin blobs are also identical between `28fc86ac` and the tip (checked for all nine), so attempt-1's wave-2
numbers and mine are the same measurement on the same bytes.

The man7 page was re-fetched with a cache-buster to rule out a stale CDN object: same sha256 (`79f5ab18…`).
`https://github.com/hyprwm/Hyprland/git/ref/tags/v0.56.2` → `efb50993780079460b0cbed1363e2166a2de1d9f`; the running host
agrees (`hyprctl version -j` → `"commit": "efb50993780079460b0cbed1363e2166a2de1d9f"`, `"tag": "v0.56.2"`) — read-only, no
compositor state touched.

### 2. Gate quotes located in MY bytes (line numbers re-derived)

Gate-table quotes and claimed lines are from `corpus/lessons/round-56.md` § Gate (rows 18-26) and
`.ufo/waves/round-56/w1/R56ScribeSourcesA/gate.md`. I searched my fetched bytes line by line:

```
S383 hits=[34] claimed=34 OK   setWatchList(*PDISABLEAUTORELOAD ? std::vector<std::string>{} : ...)
S384 hits=[492] claimed=492 OK "If true, the config will not reload automatically on save."
S385 hits=[148] claimed=148 OK if (m_propsTripped & REFRESH_CONFIG_WATCHER)
S386 hits=[128] claimed=128 OK wl_event_loop_add_fd(m_wayland.loop, FD.get(), WL_EVENT_READABLE, configWatcherWrite, nullptr);
S387 hits=[1844] claimed=1844 OK "source= skipping directory {}", value);
S388 hits=[65] claimed=65 OK static const char* const ENVHOME = getenv("HOME");
S389 hits=[1223] claimed=1223 OK if (COMMAND.contains("misc:disable_autoreload"))
S390 hits=[186] claimed=186 OK File opened for writing was closed.
S391 hits=[18] claimed=18 OK REFRESH_CONFIG_WATCHER     = (1 << 8),
```

Every quote is unique in its file (single hit) and at exactly the claimed line. S390's second locator :262 =
`Don't dereference <i>pathname</i> if it is a symbolic link.` is also present at 262; the man7 footer at line 811 reads
`Linux man-pages 6.19            2026-02-14`, matching the row's `Linux man-pages 6.19 (2026-02-14)`.

### 3. Anchor locators stay within the file's length (registration-v2 E3 bound)

Line count = `len(blob.split(b"\n"))`, the same rule E3 states.

```
S383 ConfigWatcher.cpp:33-34,46,54-56,60,67,69,105   pin=ConfigWatcher.cpp        line_count=112  max=105   past_eof=[]
S384 ConfigValues.cpp:492                           pin=ConfigValues.cpp         line_count=735  max=492   past_eof=[]
S385 PropRefresher.cpp:148-149                      pin=PropRefresher.cpp        line_count=160  max=149   past_eof=[]
S386 EventLoopManager.cpp:71,128                    pin=EventLoopManager.cpp     line_count=283  max=128   past_eof=[]
S387 ConfigManager.cpp:776,1070,1079-1080,1816,1835-1836,1844  line_count=2185  max=1844  past_eof=[]
S388 MiscFunctions.cpp:65,68                        pin=MiscFunctions.cpp        line_count=845  max=68    past_eof=[]
S389 HyprCtl.cpp:1223,1276                          pin=HyprCtl.cpp              line_count=2347 max=1276  past_eof=[]
S390 inotify.7.html:186,262                         pin=man7-inotify.7.html      line_count=920  max=262   past_eof=[]
S391 PropRefresher.hpp:18,21                        pin=PropRefresher.hpp        line_count=41   max=21    past_eof=[]
S392 ConfigWatcher.cpp:106  S393 MiscFunctions.cpp:66  S394 HyprCtl.cpp:1190  S395 ConfigManager.cpp:630,1838,2134  — all inside
```

### 4. Every evidence row's quoted line, and line-inside-anchor (the scope leg, re-derived)

All 30 frozen K rows and all 9 entry E rows: quote byte-present in my fetched bytes **at the frozen line**, and the frozen
line is inside its registry row's anchor locator set. 30/30 K, 9/9 E, 0 failures (K01-K30 and E01-E09; the two E rows that
cite S391 are covered because S391's own anchor carries :18/:21).

I also re-ran the counter's own `scope_covers()` (registration-v2 E3, including its "every locator bounded by the pin's line
count" rule) against every K/E row at the tip: `scope_covers=True` for all 39 rows whose pin is in `c1.pin_suffix`.

### 5. The lane's own QUALITY-107 instrument on the tip

```
python3 -I check-anchor-cover.py --repo <lane> --rev 0f3a5436 --entry corpus/knowledge/hyprland-config-autoreload-r56.md --work <scratch>
... CHECK107: rows=39 covered=39 miss=0 verdict=OK   (exit 0)
```

At `28fc86ac` this instrument printed 6 MISS rows (E01, E03, E04, E05, E06, E07 — the wave-2 finding in
`w2/R56W2CritScopeFix.md`); the S392-S395 rows added at integration close them. That is an independent confirmation that the
anchor rows landed as the lesson claims.

### 6. Registry-wide URL sweep (beyond the round-56 rows; the literal reading of "for each row in SOURCES.md")

I fetched all **251 distinct URLs** in all 332 registry rows at the tip (`curl -sSL -m 45`, sha256 of each response) and
compared against every sha256 appearing in that row's anchor cell. Results: 242 HTTP 200, 2 HTTP 403, 6 HTTP 404, 1
connection failure; 229 rows' fetched bytes match a sha256 (exact or as a prefix) in their own anchor cell, 62 do not.
Per-row output: `receipts/registry-url-sweep.tsv`. The 13 round-56 rows are all EXACT.

Reading the 62 non-matching rows (none is a round-56 row; the round-56 claim does not depend on them):

- **62 rows: the anchor cell carries no sha256 of the fetched URL's bytes, by construction.** Examples: S366
  (`Hyprland-HyprCtl.cpp:1126-1158,2036 @ efb5099…; pin .ufo/waves/round-51/fetch/…` — no hash at all, only a commit token),
  S018 (`dispatchGetProp, lines 1463-1645; tag commit efb5099…`), S005 (`README.md §Protocol phases @ main 3dac056d`).
  These rows were never hash-bound to their URL; there is nothing to compare. **Not a defect** — a gap in the older rows'
  provenance convention, outside this round.
- **8 rows: the URL is now dead (HTTP 404) — the wiki was restructured.** S016, S017, S029, S030, S031, S045, S063, S064
  point at `https://wiki.hypr.land/Configuring/...` and `https://wiki.hypr.land/Hypr-Ecosystem/...`, which now return 404.
  The live wiki serves lowercase paths (`https://wiki.hypr.land/configuring/core/advanced-configuration/using-hyprctl/` →
  200; `.../configuring/core/rules/window-rules/` → 200) and its `sitemap.xml` lists the moved pages
  (`/hypr-ecosystem/user/hypridle/`, `/hypr-ecosystem/user/hyprlock/`, `/hypr-ecosystem/user/xdg-desktop-portal-hyprland/`).
  These rows are all `mined`/`queued`/`rejected` with `recheck 90d`; their content is still upstream, at a new path. **D1,
  cosmetic for round 56 / weakens those rows' recheck discipline** (a 90-day recheck on a 404 URL cannot be re-run as
  written). Not a round-56 claim defect: S016/S017 are cited by no round-56 evidence row.
- **S132 (`kitty`): the URL in the cell redirects.** `https://sw.kovidgoyal.net/kitty/conf.html` → 325 B redirect stub;
  the row's anchor cell says "built HTML page conf/ (577,387 B, sha256 08e64110…, opened 2026-10-22)" and the redirected
  target `https://sw.kovidgoyal.net/kitty/conf/` fetches to exactly 577,387 B, sha256 `08e6411024fdfc444e47750dadc28b7d87e0bd768695cc635690916e08a9703d` — **MATCH**. The row is honest; my sweep's first URL (the `.html` variant) was the stub.
- **S287 (`Hyprland` issue 565): the live HTML differs from the captured receipt.** Fetched 437,853 B,
  sha256 `b52e8bde8ae1d5f0…`; the anchor cell names 475,170 B sha256 `148a9053e813a7d9…`, and that is the sha of the
  lane's committed receipt `.ufo/waves/round-41/fetch/issue-565.html`, which I reproduced exactly
  (`git show 0f3a5436:.ufo/waves/round-41/fetch/issue-565.html | sha256sum` = `148a9053e813a7d9…`). The row pins the
  capture, not the live page — **the row is honest**; the live page simply grew.
- **S149 (`foot` wiki): the upstream repo moved.** `https://codeberg.org/dnkl/foot.wiki.git` now 303-redirects to
  `https://codeberg.org/dnkl/foot.git/wiki`; the API no longer serves `dnkl/foot.wiki`
  (`{"message":"The target couldn't be found."}`), and `…/raw/commit/2475351…/Home.md` is 404. The anchor cell says the blob
  was "fetched as a git blob from https://codeberg.org/dnkl/foot.wiki.git" at commit `2475351ace3c8a618a3f2b8a7a486e987d125e07`,
  sha256 `78bd64dc27cff31a…`, 32739 B. I could not reproduce that blob at the stated URL today. **D1-class for that row
  (recheck target unreachable at the recorded locator)**, but it is a `mined` row from an earlier round with `recheck
  on-release`, not a round-56 dependency.
- **S110 (`bashref.texi`): `https://cgit.git.savannah.gnu.org/...` timed out at 40 s (HTTP 000), but the same path over
  plain `http://` fetches 415,804 B with sha256 `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5` —
  exactly the anchor cell's hash. **MATCH on content**; the https endpoint is unreachable from this host, not a content
  defect.
- **S084 / S094: rejected rows.** S084's anchor cell hashes a *saved* HTML extract (`saved HTML lines 302, 306, 356-362`),
  not the live page; S094's hashes are tree listings and a `colors.toml` blob — and the live `colors.toml` I fetched
  (461 B) hashes to `dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786`, exactly the row's
  "raw themes/matte-black/colors.toml sha256". **MATCH.**
- **S183 / S184 (doi.org): HTTP 403** to a plain `curl`; the anchor cells cite DOI metadata read through a reader, not the
  landing page bytes. Not comparable, not a defect.

### 7. Semantic spot-check of the two named rows' cells against the upstream lines

- **S383** (c5 scope / c7 teaches) — every clause is visible in the anchored lines: `update()` passes
  `std::vector<std::string>{}` when the cached value is non-zero (line 34), the watch list is cleared with
  `inotify_rm_watch` per entry (46) and `m_watches.clear()` (49, in the same function though not itself an anchor line),
  `is_directory` (54) selects `directoryMask`/`fileMask` (55-57), one `inotify_add_watch` per path (60), the canonical
  symlink watch (65-69) and the event callback `m_watchCallback(SConfigWatchEvent{` (105). All honest.
- **S384** — line 492 reads exactly
  `MS<Bool>("misc:disable_autoreload", "If true, the config will not reload automatically on save.", false, {.refresh = Supplementary::REFRESH_CONFIG_WATCHER}),`
  which supports "boolean with default false", the quoted description, and the refresh tag.

### 8. Frozen-file integrity (precondition)

```
git show 323a69c9:.ufo/waves/round-56/frozen-tables-v2.json | sha256sum   9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2
git show 0f3a5436:.ufo/waves/round-56/frozen-tables-v2.json | sha256sum   9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2
```

`frozen-tables-v2.json`, `claims-frozen-v2.md`, `registration-v2.md`, `c3-name-only.tsv`, `claims-frozen.md`,
`registration.md`, `frozen-tables.json` — all byte-identical between the v2 freeze commit `323a69c9` and the tip. Nothing in
the frozen contract moved under me.

## Defects

**D1 — eight older registry rows now point at 404 URLs (cosmetic for round 56; weakens those rows' recheck discipline).**
`corpus/SOURCES.md` @ `0f3a5436`: S016, S017, S029, S030, S031, S045, S063, S064.
Input that shows it: `curl -sSL -o /dev/null -w "%{http_code}" https://wiki.hypr.land/Configuring/Basics/Window-Rules/` →
`404`; `https://wiki.hypr.land/` → 200; the live wiki's `sitemap.xml` lists the pages under `/configuring/core/…` and
`/hypr-ecosystem/user/…`; `https://wiki.hypr.land/configuring/core/rules/window-rules/` → 200. Severity: **cosmetic for the
round-56 claims** (no round-56 evidence row cites these ids; C1/C2/C3 do not read them), **weakens** those rows' own
`recheck` promises — a 90-day recheck cannot be executed against the recorded URL. Same class for **S149**
(`dnkl/foot.wiki` → `dnkl/foot.git`, blob not reproducible at the recorded locator). Suggested handling: a `recheck` re-anchor
in a later round, or a `flip` note; **not** a round-57 predicate change.

**D2 — S391's pin has no frozen hash and no frozen locator base (process finding, disclosed in the lane's own lesson).**
`frozen-tables-v2.json` `c1.pin_sha256` has 8 entries and `c1.pin_suffix` has 8; `Hyprland-PropRefresher.hpp` (S391) is in
neither, and `c1.rows` maps only S383-S390. Consequence I measured: the C1 counter's `scope_ok()` returns False for any row
whose pin is not in `c1.pin_suffix` (it does `if cells is None or pin not in c1["pin_suffix"]: return False`), so the two entry
rows that cite S391 (E08, E09) could never satisfy a scope leg under the frozen table. They are outside the frozen K/H set
(the counter scores `c1["k"]` + `c1["h"]` only), so the frozen predicate is unaffected and `new_rows=8/8` still holds — the
lesson already records this as **M56-9** and the extra pin is hashed in `receipts/pins-extra.sha256`
(`37acaaf16a24dcfe89d0702818b82d300d0da5e91ef1ba47494f7fd2ab0af2d0  fetch/Hyprland-PropRefresher.hpp`), which I confirmed equals
the file I fetched from GitHub. Severity: **weakens the process statement only** (the frozen hash set does not cover the
registry's 9th pin); the row's own content is byte-exact.

**Not a defect, recorded so it is not re-reported:** the entry's prose carries 8 QUALITY-77 locator misses
(`python3 -I quality/check-locators.py --fetch .ufo/waves/round-56/fetch <entry>` → `locators=62 miss=8`, e.g.
`entry-r56.md:21 Hyprland-ConfigWatcher.cpp:33 … verdict=MISS`). I re-ran the identical instrument on the attempt-1 entry
(`28fc86ac`) and got `locators=61 miss=6` with the same misses plus two that the tip edit turned from `NOFRAG` into `MISS` —
i.e. the misses are the checker's nearest-fragment attribution on multi-locator prose lines, already reported as wave-2 finding
T1-22 (`w2/R56W2ConnCross.md`), and the tip edit made two of them *worse* (`man7-inotify.7.html:225-228` went NOFRAG→MISS,
`man7-inotify.7.html:185-186` gained a fragment). No frozen leg reads prose locators, so this does not block any claim; it is
recorded here only because I ran the instrument.

## Could not verify

- **S149's blob** (`78bd64dc27cff31a…`, 32739 B, commit `2475351…`) — the upstream repo has moved and the API no longer serves
  the old path; I could not reproduce the blob bytes today. The row's own anchor cell is honest about how it was fetched
  ("the wiki's own raw and src routes return 404 / redirect to the page index"), so this is a recheck-path loss, not evidence
  the row is wrong.
- **S110 over https** — the savannah cgit https endpoint times out from this host (HTTP 000 at 40 s). The identical path over
  http returns the exact bytes and hash the row claims, so the content is confirmed by a second route.
- **S183/S184 (doi.org)** — HTTP 403 to plain curl; the anchor cells cite DOI metadata read via a reader, so I did not
  re-derive those two.
- I did **not** re-run the C1/C2/C3 counters or the harnesses: they are other seats' frozen targets, and this seat's item is
  the row-level re-open. Where I quote the counter's `scope_covers()` semantics I re-implemented that function from the
  committed source (`quality/counters/c1-r56-autoreload-entry.py` @ tip) and ran it over all 39 evidence rows.
- The upstream URLs for the 13 round-56 rows are **commit-pinned** (GitHub raw at `efb5099…`) and the man7 page is **not** — it
  is a live page. My man7 fetch is a same-day observation (2026-10-30); a later man-pages release will change those bytes and
  the row's `recheck 90d` will be the right moment to re-pin.

## Deliverables

- `.ufo/waves/round-56/w3/R56W3ScoutRows1b/receipts/rows.md` — per-row receipt (13 rows: fetch status, sha256 vs anchor cell /
  committed pin blob / frozen table, gate-quote line number, anchor-locator EOF bound, MATCH verdict).
- `.ufo/waves/round-56/w3/R56W3ScoutRows1b/receipts/registry-url-sweep.tsv` — the full 332-row URL sweep (251 distinct URLs),
  one line per row-URL pair: HTTP code, size, fetched sha256, the row's anchor-cell sha (or `-`), verdict class.
- `.ufo/waves/round-56/w3/R56W3ScoutRows1b/receipts/rows_all.json` — the parsed registry rows at the tip (all 11 cells each),
  the data the two receipts above are derived from.

## Tooling

No tool was installed, upgraded or changed. Everything used was already present: `curl`, `sha256sum`, `git` (read-only: `show`,
`ls-tree`, `diff`, `merge-base`, `cat-file`), `python3 -I`, `hyprctl version -j` (read-only), `stat`, `awk`. Per the pacman
guard I ran no pacman transaction; the operator directive's install channel was not needed for this seat.

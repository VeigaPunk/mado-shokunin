# R56W2ScoutRows5 — independent re-fetch of registry rows S390 and S391 (wave 2 falsification)

Scored tree: `28fc86ac2359ec27406d8a2c63bef82ea6e947ed` (never the working tree). Contracts read first:
`claims-frozen-v2.md`, `registration-v2.md`, `registration-v2-errata.md` (E12-E14), wave-1 gate
`.ufo/waves/round-56/w1/R56ScribeSourcesA/gate.md`. Attack named in the seat: wave 1's row author wrote
S390/S391 and the gate quotes from the pin files; nothing independent had fetched the upstream bytes.

## Verdict

| row | bytes vs anchor sha | bytes vs frozen-tables-v2 | gate quote located | entry quotes in anchor | cells honest | census | verdict |
|---|---|---|---|---|---|---|---|
| S390 | MATCH | MATCH (`c1.pin_sha256["man7-inotify.7.html"]`) | MATCH (186, 262) | K29, K30 all pass | pass | no W/E for this row | **MATCH** |
| S391 | MATCH (anchor cell) | **ABSENT from frozen table** | no gate row (gate covers S383-S390); located by me (18, 21) | E08, E09 pass | pass (one cosmetic locator-scope note) | no W/E for this row | **MATCH on content; process finding D1** |

## 1. Frozen-contract integrity (precondition)

```
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 323a69c9014da1cebece67bb111b70a5630f4a60:.ufo/waves/round-56/frozen-tables-v2.json | sha256sum
9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2  -
sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/frozen-tables-v2.json
9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2
```
Committed blob == working-tree file == the sha embedded in `claims-frozen-v2.md`. MATCH.

Registry and entry extracted at the scored rev with the seat's one `git archive`:
`corpus/SOURCES.md` sha256 `2e387348f3a240c2614d7028dd44e55a709b94b02c112a56b4d7b5b4d6da2ab2`;
`corpus/knowledge/hyprland-config-autoreload-r56.md` sha256 `ddbdb366c2419c18a2211e9da8d0ccaf964c68f77a526cd0723375713c8c189d`.

## 2. Independent fetch and sha comparison (the attack)

Fetch (2026-10-28, curl to scratch, no lane writes):
```
curl -fsSL https://man7.org/linux/man-pages/man7/inotify.7.html                     -o fetch/man7-inotify.7.html
curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/supplementary/propRefresher/PropRefresher.hpp -o fetch/Hyprland-PropRefresher.hpp
sha256sum fetch/*
79f5ab18e2fc423631cf4949ef82ca1384844353ea11a4dba42e1a77e8fdd8fd  man7-inotify.7.html      (44066 B, 919 newlines)
37acaaf16a24dcfe89d0702818b82d300d0da5e91ef1ba47494f7fd2ab0af2d0  Hyprland-PropRefresher.hpp (1322 B, 40 newlines)
```
- **S390**: fetch sha == anchor-cell `sha256:79f5ab18…8fdd8fd` (and size 44066 B matches the cell) == `frozen-tables-v2.json c1.pin_sha256["man7-inotify.7.html"]` == the lane's committed pin blob at 28fc86a (`git show 28fc86a:.ufo/waves/round-56/fetch/man7-inotify.7.html | sha256sum` → same). **MATCH**, four ways.
- **S391**: fetch sha == anchor-cell `sha256:37acaaf1…ab0af2d0` (1322 B matches) == committed pin blob at 28fc86a. But `frozen-tables-v2.json c1.pin_sha256` has **no** `Hyprland-PropRefresher.hpp` key (only the .cpp from S385) and `c1.new_row_ids` is exactly `["S383"…"S390"]` — **S391 is in no frozen table** (finding D1). Content-wise: **MATCH**.

## 3. Gate quotes located in the independent bytes

Gate file `w1/R56ScribeSourcesA/gate.md` covers S383-S390 only; its S390 row claims pin lines 186 and 262.

In my fetched bytes (receipt `entry_checks.quote_found_on_lines`, each quote exactly one occurrence):
- `File opened for writing was closed.` → line **186** (under `<b>IN_CLOSE_WRITE </b>(+)`, line 185). Gate said 186. MATCH.
- `Don't dereference <i>pathname</i> if it is a symbolic link.` → line **262** (under `<b>IN_DONT_FOLLOW </b>(since Linux 2.6.15)`, line 261). Gate said 262. MATCH.
- S391 (no gate row): `REFRESH_CONFIG_WATCHER     = (1 << 8),` → line **18**; `REFRESH_ALL = std::numeric_limits<std::underlying_type_t<ePropRefreshProp>>::max(),` → line **21**. Both single occurrences. The anchors are correct even though no gate row ever located them.

Version claim of the S390 anchor ("@ Linux man-pages 6.19 (2026-02-14)") verified in the fetched page itself: line 801 "obtained from the tarball man-pages-6.19.tar.gz", line 811 footline `Linux man-pages 6.19            2026-02-14     <i>inotify</i>(7)`. MATCH.

## 4. Entry K/E rows citing S390/S391 — quote inside anchor ranges

Mechanised by `check_quotes.py` (delivered; full JSON in `receipt-s390-s391.json`). Citing rows in the entry at 28fc86a: K29, K30 (S390); E08, E09 (S391); plus the `source:` line. No other row cites them.

| entry row | locator | quote at claimed line | inside anchor range | locator ≤ EOF bound |
|---|---|---|---|---|
| K29 | `man7-inotify.7.html:186` | yes (byte-exact) | yes (range 186) | yes (186 ≤ 920) |
| K30 | `man7-inotify.7.html:262` | yes (byte-exact) | yes (range 262) | yes (262 ≤ 920) |
| E08 | `Hyprland-PropRefresher.hpp:18` | yes (byte-exact, incl. 5-space alignment) | yes (range 18) | yes (18 ≤ 41) |
| E09 | `Hyprland-PropRefresher.hpp:21` | yes (byte-exact) | yes (range 21) | yes (21 ≤ 41) |

EOF bound used is the registered E3 form `len(blob.split(b"\n"))`: man7 page 920 (ends with `\n`, 919 `wc -l`), header 41 (40 `wc -l`). **No anchor locator runs past the file's last line** — null result, command = `python3 -I check_quotes.py` (receipt fields `locator_within_split_line_count`).

## 5. Cell honesty (tier/kind/scope/teaches/recheck)

- **S390** `docs/B`: an HTML man page — kind correct; tier B is a judgment call consistent with registry convention (docs rows exist at both A and B; not decidable from bytes). scope/teaches say only what lines 186/262 show: IN_CLOSE_WRITE = "File opened for writing was closed.", IN_DONT_FOLLOW = "Don't dereference pathname if it is a symbolic link." Propositions of K29/K30 likewise restate the lines. `opened 2026-10-28` (ISO), `recheck 90d` (NNd). Pass.
- **S391** `code/A`: line 18 and line 21 show exactly the scope's two claims ("REFRESH_CONFIG_WATCHER is bit 8", "REFRESH_ALL is the maximum of the enum's underlying type"). `recheck on-release` (symbolic). Pass, with one cosmetic note (D2): teaches (and E09's proposition "which here is uint16_t") assert the underlying type **uint16_t**, which is visible only at line 9 `enum ePropRefreshProp : uint16_t {` — outside the anchor range 18,21. True of the pinned file; the anchored lines alone show only `underlying_type_t`.

## 6. Census validator

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /fast/scratch/hyaku/mado-r56/R56W2ScoutRows5/work/corpus/SOURCES.md
→ exit 1, 431 findings (full output: census-out.txt)
grep -nE 'S390|S391' census-out.txt   →  no output (null result; command recorded)
```
Zero W/E lines mention S390 or S391 (so also no E09 recheck rejection, no E05/E06 enum violation, no W04 duplicate-URL — both URLs are unique in the file; the W04 hits land on S384/S387/S388/S389, which share URLs with older rows). The exit 1 comes from other rows: W04 duplicate-URL warnings, W01, and ~380 `E11 used-by path missing on disk`. Those E11 are an artifact of `--file` mode, which resolves used-by against `dirname(file)/..` (script line 501) — my scratch mirror contains only the registry and this entry, so S390/S391's used-by target (`corpus/knowledge/hyprland-config-autoreload-r56.md`) was present and passed, while every row pointing at lessons/entries outside the mirror is flagged. The E11 mass is therefore expected under the seat's mandated `--file` invocation and concerns no S390/S391 row.

## 7. Defects

- **D1 — weakens the claim (process, not bytes).** Registry row S391 exists at 28fc86a, is cited by the entry (`source:` line, E08, E09) and lists that entry in `used-by`, but sits outside every frozen leg: not in `frozen-tables-v2.json` `c1.new_row_ids` (S383-S390) nor `pin_sha256`, absent from the wave-1 gate (S383-S390), and `registration-v2.md` §C1 recount says "rows S383-S390". `registration-v2-errata.md` (E12-E14) does not disclose it. Disclosure exists only in the wave-2 spec ("the S391 row added at integration") and the jj op-log integration commit `c4d915fe76612986ea280b487e9ba6a9bf455a64` ("round-56: integrate C1 entry, rows S383-S391, …"; note `28fc86ac` itself is the later E14 fix commit "C1 counter drops the bare content leg; tool ledger row fix"). No registered predicate is false — the C1 counter's universe is `c1["k"]+c1["h"]` (30 K + 3 H rows; `c1-counter-28fc86a.py` lines 36, 505, 599-604) so S391 and all E-rows are simply uncounted — but the entry's reliance on S391 was never gated pre-data. This independent fetch closes the byte-level gap (sha MATCH); the governance gap (freeze/errata silence) remains for the L1.
- **D2 — cosmetic.** S391 `teaches` (and entry E09's proposition) state "underlying uint16_t"; the anchored lines 18/21 show `underlying_type_t` only — the uint16_t resolution is at line 9 of the same pinned file, outside the anchor range.

## 8. Not verified

- Fetches are point-in-time (2026-10-28); upstream drift after this date not covered. No second-mirror cross-check for the man7 page.
- Tier A/B assignments are author judgment; I checked consistency, not correctness.
- I read the C1 counter only far enough to establish which universes S391/E-rows fall in; its full leg grammar is other seats' scope.
- Census `--file` mode was run exactly as the seat specifies (against the scratch mirror); a full-lane validate would resolve the ~380 E11 differently. That run is out of my seat bounds (would score the working tree).

## Compliance

No tool installs (curl/git/python3/gawk preexisting; pacman guard untouched). Read-only git only (`archive`, `show`, `log`); no lane tracked file touched; scratch `/fast/scratch/hyaku/mado-r56/R56W2ScoutRows5/` removed before yielding; no credential material written.

## Deliverables

Directory `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w2/R56W2ScoutRows5/`:
- `receipt-s390-s391.json` — machine receipt (sha256 `428acac47e05e26dda012c8813b52884734721197fd018b006e4fe4bd11e6df5`): blob hashes/line counts, parsed row cells, per-quote byte checks, frozen-table status.
- `man7-inotify.7.html`, `Hyprland-PropRefresher.hpp` — the independently fetched upstream bytes.
- `census-out.txt` — full census validate output (431 lines, none mentioning S390/S391).
- `check_quotes.py` — the verification script (quote-cell → upstream bytes at claimed lines).

Report trailer: `Report: .ufo/waves/round-56/w2/R56W2ScoutRows5.md`

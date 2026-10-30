# Receipts — registry rows S390 and S391 re-opened independently (second sample)

- seat: `R56W3ScoutRows5b` (wave 3, attempt 2)
- scored tree: `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (lane tip)
- **second sample**: attempt-1's wave-2 scout (`w2/R56W2ScoutRows5.md`) fetched these same two rows at
  `28fc86ac2359ec27406d8a2c63bef82ea6e947ed`; this seat re-derived both rows from scratch at the tip.
  The two registry rows are byte-identical between the two revs (`sha256` of the S390+S391 line pair:
  `5a314e1f0e5e90ea1fd4cbd0c0767bf4170b093c366837b0ac006aa53309d8cb` at both `28fc86ac` and the tip).
- upstream bytes fetched **by this seat** into `/fast/scratch/hyaku/mado-r56/R56W3ScoutRows5b/`,
  not read from the lane's pins; the committed pins were then compared to the fresh fetch.
- frozen table read at the tip: `.ufo/waves/round-56/frozen-tables-v2.json`
  sha256 `9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2` (matches the value frozen in
  `claims-frozen-v2.md`).

## Summary

| row | fresh-fetch sha256 | size | vs anchor cell | vs frozen table | gate quote line (fresh bytes) | anchor locators ≤ line count | verdict |
|---|---|---|---|---|---|---|---|
| S390 | `79f5ab18e2fc423631cf4949ef82ca1384844353ea11a4dba42e1a77e8fdd8fd` | 44066 B | MATCH | MATCH (`c1.pin_sha256["man7-inotify.7.html"]`) | 186 | yes — `186, 262` ≤ 920 | **MATCH** |
| S391 | `37acaaf16a24dcfe89d0702818b82d300d0da5e91ef1ba47494f7fd2ab0af2d0` | 1322 B | MATCH | **ABSENT from every frozen leg** | 18 | yes — `18, 21` ≤ 41 | **MATCH on content; process finding D1 (pre-existing, confirmed at the tip)** |

---

## S390 — "Linux man-pages 6.19 inotify(7) man page"

Registry row at `0f3a5436`, `corpus/SOURCES.md` (read via `git show`, not the working tree).

- URL cell: `https://man7.org/linux/man-pages/man7/inotify.7.html`
- kind / tier: `docs` / `B`; status `mined`; opened `2026-10-28`; recheck `90d`
- scope cell: `the meaning of the IN_CLOSE_WRITE and IN_DONT_FOLLOW flags used in the watcher's masks`
- anchor cell: `inotify.7.html:186,262 @ Linux man-pages 6.19 (2026-02-14); pin .ufo/waves/round-56/fetch/man7-inotify.7.html 44066 B sha256:79f5ab18e2fc423631cf4949ef82ca1384844353ea11a4dba42e1a77e8fdd8fd`
- teaches cell: `IN_CLOSE_WRITE reports a file opened for writing being closed, and IN_DONT_FOLLOW means the pathname is not dereferenced when it is a symbolic link`
- used-by cell: `corpus/knowledge/hyprland-config-autoreload-r56.md`

### Fetch (this seat, 2026-10-30)

```
curl -sSL -o man7-inotify.7.html 'https://man7.org/linux/man-pages/man7/inotify.7.html'
HTTP=200 SIZE=44066
79f5ab18e2fc423631cf4949ef82ca1384844353ea11a4dba42e1a77e8fdd8fd  man7-inotify.7.html
```

Second independent fetch (different User-Agent) → identical sha256, 44066 B.
`curl --compressed` → identical sha256. `Accept-Encoding: gzip` **without** `--compressed` → different
sha256 (gzip container bytes), so the hash in the anchor cell is over the *decoded* document — consistent.

Server headers (2026-10-30): `Last-Modified: Wed, 28 Oct 2026 18:28:41 GMT`, `Content-Length: 44066`,
`ETag: "ac22-65eeabb7aa840"`.

### Comparison

| comparison | result | command |
|---|---|---|
| fresh fetch vs anchor-cell `sha256:79f5ab18…8fdd8fd` | **MATCH** | `sha256sum man7-inotify.7.html` |
| fresh fetch vs anchor-cell `44066 B` | **MATCH** (44066 B) | `wc -c` |
| fresh fetch vs `frozen-tables-v2.json c1.pin_sha256["man7-inotify.7.html"]` | **MATCH** (same hash) | `python3 -I -c "import json;print(json.load(open('.ufo/waves/round-56/frozen-tables-v2.json'))['c1']['pin_sha256']['man7-inotify.7.html'])"` |
| fresh fetch vs the pin committed at the tip (`.ufo/waves/round-56/fetch/man7-inotify.7.html`) | **MATCH** — `cmp` rc=0, same sha256 | `git show 0f3a5436:.ufo/waves/round-56/fetch/man7-inotify.7.html \| sha256sum` |

Four-way identity: fresh fetch = anchor cell = frozen table = committed pin at the tip.

### Gate quote located in the fresh bytes

Gate source at the tip: `corpus/lessons/round-56.md` '## Gate' table, line 25:
`| S390 | \`https://man7.org/linux/man-pages/man7/inotify.7.html\` | \`File opened for writing was closed.\` (:186) |`

| quote | lesson line | occurrences in fresh bytes | line | verdict |
|---|---|---|---|---|
| `File opened for writing was closed.` | 186 | 1 | 186 | **MATCH** |
| `Don't dereference <i>pathname</i> if it is a symbolic link.` (the second locator 262) | 262 | 1 | 262 | **MATCH** |

Context lines in the fresh bytes:

```
185:           <b>IN_CLOSE_WRITE </b>(+)
186:                  File opened for writing was closed.
261:           <b>IN_DONT_FOLLOW </b>(since Linux 2.6.15)
262:                  Don't dereference <i>pathname</i> if it is a symbolic link.
```

### Anchor locators vs the file's line count

- fresh bytes: 919 newlines; `len(blob.split(b"\n"))` = **920** (the registration-v2 E3 bound form).
- anchor-cell locators for basename `inotify.7.html`: `186`, `262` → both ≤ 920. **No locator runs past EOF.**
- `wc -l` (919) gives the same verdict.

### Version token checked inside the page

```
801:       This page was obtained from the tarball man-pages-6.19.tar.gz
811: <span class="footline">Linux man-pages 6.19            2026-02-14                     <i>inotify</i>(7)</span>
```

The anchor cell's `@ Linux man-pages 6.19 (2026-02-14)` is literally in the fetched bytes.

### Second-mirror corroboration (independent of man7)

The man7.org URL is a *floating* "latest release" URL. Corroborated against the kernel.org git mirror at
the same tag:

```
curl -sSL -o inotify-6.19.raw 'https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man7/inotify.7?h=man-pages-6.19'
208:.BR IN_CLOSE_WRITE " (+)"
209-File opened for writing was closed.
310:.BR IN_DONT_FOLLOW " (since Linux 2.6.15)"
311-Don't dereference
312-.I pathname
313-if it is a symbolic link.
```

Both quoted strings are present in the 6.19 roff source at the kernel.org mirror — the man7 HTML and the
6.19 tag agree on the two descriptions.

### Entry rows citing S390

| entry row | locator | quote occurrences in fresh bytes | line inside S390's anchor locators |
|---|---|---|---|
| K29 | `man7-inotify.7.html:186` | `[186]` | yes (186) |
| K30 | `man7-inotify.7.html:262` | `[262]` | yes (262) |

Both quotes are byte-exact at their claimed lines, each occurring exactly once in the fresh bytes.

### Verdict

**MATCH.** Upstream bytes = anchor-cell sha256 and size = frozen-table hash = committed pin at the tip;
the gate quote lands on the line the tip lesson states; every anchor locator is within the pin's line
count; the entry rows quoting this id are byte-exact at their stated lines.

---

## S391 — "Hyprland 0.56.2 property refresher header - refresh flag enum"

- URL cell: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/supplementary/propRefresher/PropRefresher.hpp`
- kind / tier: `code` / `A`; status `mined`; opened `2026-10-28`; recheck `on-release`
- scope cell: `the refresh-flag enum: REFRESH_CONFIG_WATCHER is bit 8 and REFRESH_ALL is the maximum of the enum's underlying type`
- anchor cell: `PropRefresher.hpp:18,21 @ efb50993780079460b0cbed1363e2166a2de1d9f; pin .ufo/waves/round-56/fetch/Hyprland-PropRefresher.hpp 1322 B sha256:37acaaf16a24dcfe89d0702818b82d300d0da5e91ef1ba47494f7fd2ab0af2d0`
- teaches cell: `REFRESH_CONFIG_WATCHER = (1 << 8) and REFRESH_ALL = the maximum of the underlying uint16_t, so REFRESH_ALL contains the config-watcher bit`
- used-by cell: `corpus/knowledge/hyprland-config-autoreload-r56.md`

### Fetch (this seat, 2026-10-30)

```
curl -sSL -o Hyprland-PropRefresher.hpp 'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/supplementary/propRefresher/PropRefresher.hpp'
HTTP=200 SIZE=1322
37acaaf16a24dcfe89d0702818b82d300d0da5e91ef1ba47494f7fd2ab0af2d0  Hyprland-PropRefresher.hpp
```

Second independent fetch (different User-Agent) → identical sha256, 1322 B. The URL is commit-pinned, so
upstream drift is impossible for this row without a new commit.

### Comparison

| comparison | result | command |
|---|---|---|
| fresh fetch vs anchor-cell `sha256:37acaaf1…ab0af2d0` | **MATCH** | `sha256sum Hyprland-PropRefresher.hpp` |
| fresh fetch vs anchor-cell `1322 B` | **MATCH** | `wc -c` |
| fresh fetch vs `frozen-tables-v2.json` | **ABSENT** — S391 is in no frozen leg (see D1) | `python3 -I -c "…['c1']['rows'].get('S391')"` → `None`; `['c1']['new_row_ids']` → `["S383"…"S390"]`; `['c1']['pin_sha256']` has no `Hyprland-PropRefresher.hpp`; `['c1']['pin_suffix']` has no such key either |
| fresh fetch vs the pin committed at the tip | **MATCH** — `cmp` rc=0, same sha256 | `git show 0f3a5436:.ufo/waves/round-56/fetch/Hyprland-PropRefresher.hpp \| sha256sum` |

Three-way identity: fresh fetch = anchor cell = committed pin at the tip. The frozen table cannot be
compared because it does not carry the row.

### Gate quote located in the fresh bytes

Gate source at the tip: `corpus/lessons/round-56.md` '## Gate' table, line 26:
`| S391 | \`…/src/config/supplementary/propRefresher/PropRefresher.hpp\` | \`REFRESH_CONFIG_WATCHER     = (1 << 8),\` (:18) |`

| quote | lesson line | occurrences in fresh bytes | line | verdict |
|---|---|---|---|---|
| `REFRESH_CONFIG_WATCHER     = (1 << 8),` | 18 | 1 | 18 | **MATCH** |
| `REFRESH_ALL = std::numeric_limits<std::underlying_type_t<ePropRefreshProp>>::max(),` (the second locator 21) | 21 | 1 | 21 | **MATCH** |

Context lines in the fresh bytes:

```
 9:    enum ePropRefreshProp : uint16_t {
18:        REFRESH_CONFIG_WATCHER     = (1 << 8),
21:        REFRESH_ALL = std::numeric_limits<std::underlying_type_t<ePropRefreshProp>>::max(),
```

### Anchor locators vs the file's line count

- fresh bytes: 40 newlines; `len(blob.split(b"\n"))` = **41** (E3 bound form).
- anchor-cell locators for basename `PropRefresher.hpp`: `18`, `21` → both ≤ 41. **No locator runs past EOF.**

### Entry rows citing S391

| entry row | locator | quote occurrences in fresh bytes | line inside S391's anchor locators |
|---|---|---|---|
| E08 | `Hyprland-PropRefresher.hpp:18` | `[18]` | yes (18) |
| E09 | `Hyprland-PropRefresher.hpp:21` | `[21]` | yes (21) |

Both quotes byte-exact at their claimed lines, each exactly one occurrence.

### Verdict

**MATCH on content; process finding D1 (already disclosed as lesson item M56-9).**

Upstream bytes = anchor-cell sha256 and size = committed pin at the tip; the gate quote lands on line 18
as the tip lesson states; both anchor locators are within the pin's line count; the two entry rows quoting
this id are byte-exact at their stated lines. But the row itself is outside every frozen leg of the
frozen predicate, so no counter leg exercises it (see D1 and D4 below).

---

## D1 — S391 sits outside every frozen leg (process; weakens the claim)

**Pre-existing, disclosed at the tip** as lesson item M56-9 (`corpus/lessons/round-56.md:82`: "a pin and a
row (S391) entered after the freeze with no frozen hash"), and first raised by attempt-1's wave-2 scout
as D1. Confirmed independently at the tip and quantified here:

```
$ python3 -I -c "import json; d=json.load(open('.ufo/waves/round-56/frozen-tables-v2.json'))['c1']; \
  print(d['rows'].get('S391'), d['new_row_ids'], 'Hyprland-PropRefresher.hpp' in d['pin_sha256'], \
  'Hyprland-PropRefresher.hpp' in d['pin_suffix'])"
None ["S383", "S384", "S385", "S386", "S387", "S388", "S389", "S390"] False False
```

Consequences, each demonstrated by mutation on a scratch clone of the tip (never on the lane):

| mutation | counter output | expected if S391 were in scope |
|---|---|---|
| S391 anchor-cell `sha256:` → all zeros | `TARGET_MET missed=none`, exit 0 | a `pin_hash`/`source_cell` failure |
| S391 URL rev → `0000…0000` | `TARGET_MET missed=none`, exit 0 | `source_cell:E08/E09` |
| S391 anchor cell: drop locator `21` | `TARGET_MET missed=none`, exit 0 | `scope:` failure |
| S391 teaches cell: flip "contains the config-watcher bit" → "DOES NOT contain" | `TARGET_MET missed=none`, exit 0 | a scope/teaches failure |
| S391 scope cell: "maximum" → "minimum" of the underlying type | `TARGET_MET missed=none`, exit 0 | a scope failure |
| the **S391 pin file itself** (`.hpp`) mutated: `(1 << 8)` → `(1 << 9)` | `TARGET_MET missed=none`, exit 0 | `pin_hash` |

Positive control on the same harness: mutating the **S390** pin file
(`man7-inotify.7.html`) *is* caught —
`MADO_AUTORELOAD_ENTRY: … verdict=TARGET_MISSED missed=quote:K29,pin_hash`, exit 1 — so the harness is
live and the S391 blindness is specific, not a broken rig.

`receipts/pins-extra.sha256` records the S391 pin hash
(`37acaaf16a24dcfe89d0702818b82d300d0da5e91ef1ba47494f7fd2ab0af2d0  fetch/Hyprland-PropRefresher.hpp`)
but **no instrument reads that file**: `grep -rn "pins-extra" quality/ tools/ .ufo/waves/round-56/*.py`
returns nothing. The pin hash is a receipt, not a check.

Attempt-1's seat additionally noted that `registration-v2.md` §C1 recounts "rows S383-S390" and
`registration-v2-errata.md` (E12-E14) does not disclose S391. Confirmed at the tip
(`registration-v2.md:75`: `Recount of the unchanged rest: 30 K rows, 3 H rows, rows S383-S390.`).

**Routing.** Adding S391 to a frozen leg changes the frozen predicate → **routed finding for round 57**,
not a change here. The minimal recipe is measured, not guessed: adding `S391` to `c1.rows`,
`c1.pin_sha256` and `c1.pin_suffix` makes the counter fail closed on `missed=tables_sha` (the embedded
frozen-tables sha256 no longer matches), which is the correct behaviour for a frozen predicate — the
tables and the counter's embedded hash must move together, in a v3.

## D2 — the anchor cell's sha256/size/version strings are not enforced by any instrument (weakens the claim)

**New at this seat.** The anchor cell is the registry's own record of "these bytes, this hash". No
instrument parses the `sha256:`/`N B`/`@ version` fields out of it:

- The C1 counter reads the anchor cell **only** through `scope_covers(cells[5], basename, line, nlines)`
  (`quality/counters/c1-r56-autoreload-entry.py:483`), which parses the `<basename>:<locators>` prefix and
  ignores everything after it. `grep -n 'sha256:' quality/counters/c1-r56-autoreload-entry.py` → no hits
  on the anchor cell.
- The census parses the anchor cell into a variable (`scripts/sources-census.sh:627`) and never uses it:
  `awk 'NR>627 && /\$scope|\$teaches/'` → null; the census has no `sha256` handling at all.

Demonstrated on a scratch clone of the tip:

| mutation | counter output |
|---|---|
| S390 anchor cell `sha256:` → all zeros | `TARGET_MET missed=none`, exit 0 |
| S390 anchor cell size `44066 B` → `99999 B` | `TARGET_MET missed=none`, exit 0 |
| S390 anchor cell version token `Linux man-pages 6.19 (2026-02-14)` → `Linux man-pages 9.99 (2099-01-01)` | `TARGET_MET missed=none`, exit 0 |
| S390 URL host `man7.org` → `example.com` (suffix + rev token kept) | `TARGET_MISSED missed=source_cell:K29,source_cell:K30,new_rows` — **caught** |

So the *locator* and *URL* halves of the anchor cell are enforced, while the *hash, byte count and
version token* are decorative to every instrument in the lane. The hash is true today (four-way identity
above), but nothing in the lane would notice if a later edit falsified it. Severity: **weakens the claim**
— the C1 frozen sentence ("sha256 equal to the anchor cell and to the frozen table for S383-S390",
lesson line 13) is true at the tip but is not machine-enforced. Routing: adding a leg changes the frozen
predicate → **routed finding for round 57**.

## D3 — S390's `rev_rule` token is self-saturating (weakens the claim)

**New at this seat.** `frozen-tables-v2.json` `c1.rev_rule` gives the man7 pin the token
`man7.org/linux/man-pages/man7/inotify.7.html` — i.e. the *URL path itself*, not a revision. The counter's
check is `tok in urls[-1]` (`source_cell_ok`, counter line 468), which is therefore true for any URL that
merely contains the path — it can never fail for a well-formed S390 URL and never detects a version change.
Demonstrated: appending `?h=man-pages-6.99` to the S390 URL keeps the token present and the path suffix
intact, and the counter still reports `TARGET_MET missed=none` for the S390 legs.

By contrast the Hyprland rows use a real commit sha as the token, and that check bites:
S389's URL rev → `0000…0000` gives
`TARGET_MISSED missed=source_cell:K27,source_cell:K28,new_rows`.

Note this is not a defect in the *bytes*: the man7 page does carry the version (`Linux man-pages 6.19
2026-02-14`, verified above) and the row's `recheck 90d` is the human guard. But the row's URL is a
floating "latest release" URL with no version in it, whereas the only other man-pages row in the registry
(S112) uses a version-pinned URL (`…/man-pages.git/plain/man/man7/user_namespaces.7?h=man-pages-6.16`).
`man-pages-6.20` already exists as an upstream release tag
(`git.kernel.org/…/man-pages.git/refs/tags` lists `man-pages-6.20`; its `inotify.7` differs from 6.19 at
roff lines 140 and 561+), and man7.org still serves 6.19 for this page as of 2026-10-30 — so the page
will change under the row's own URL when man7 promotes 6.20. The two quoted descriptions are *stable*
across 6.19→6.20 (verified: same text at both tags), so the row's content claim is robust; its
*reproducibility* is not, and the `90d` recheck is the only mechanism that would notice.

Severity: **weakens the claim** (the frozen predicate's revision check for this row is vacuous; the
underlying bytes and quotes are correct today). Routing: **round 57**.

## D4 — the E-rows that cite S391 are outside every counter leg (weakens the claim)

**New at this seat** (a sharper form of the gap already noted by `w2/R56W2RevDocs.md` F9 and
`w1/R56ExecC1Harness.md` A3). The frozen `c1.k` list holds 30 K-row ids and `c1.h` holds 3 H-row ids;
there is no E-row id in either list, and the counter's leg loop is
`all_rows = [(r, "K") for r in c1["k"]] + [(r, "H") for r in c1["h"]]`
(`quality/counters/c1-r56-autoreload-entry.py:505`). Consequences, demonstrated:

| mutation | counter output |
|---|---|
| entry row **E08** proposition: "REFRESH_CONFIG_WATCHER as bit 8" → "as bit 9" | `TARGET_MET missed=none`, exit 0 |
| entry row **E09** locator `Hyprland-PropRefresher.hpp:21` → `:9999` | `TARGET_MET missed=none`, exit 0 |

So the two entry rows that are S391's *only* citing rows are not byte-checked, not scope-checked and not
lexically grounded by any lane instrument. The quotes are in fact byte-exact (verified above, and the
entry has 9 E-rows against the counter's 33 K/H rows), so this is a coverage gap, not an error.
Severity: **weakens the claim**; routing: **round 57**.

## D5 — the S390 anchor locators do not cover the flag-name lines (cosmetic)

**New at this seat.** The S390 anchor cell is `inotify.7.html:186,262`. Those are the *description*
lines. The flag names are one line above each:

```
185:           <b>IN_CLOSE_WRITE </b>(+)
186:                  File opened for writing was closed.
261:           <b>IN_DONT_FOLLOW </b>(since Linux 2.6.15)
262:                  Don't dereference <i>pathname</i> if it is a symbolic link.
```

The scope cell says "the meaning of the IN_CLOSE_WRITE and IN_DONT_FOLLOW **flags**", and the teaches cell
names both flags — but the anchored lines 186/262 do not themselves contain the flag names, and the entry's
own prose cites `man7-inotify.7.html:185-186` and "lines 261-262", i.e. it reaches one line beyond the
registry anchor on both sides. The counter's scope leg only requires the *quoted* line to be covered, so
this is not caught: moving the anchor to `185,261` (dropping the quoted descriptions) *does* fail
(`TARGET_MISSED missed=scope:K29,scope:K30`), but the reverse — the anchor naming only descriptions while
the prose names flags — is not a failure condition.

The same shape was raised for S391 at attempt-1 as D2 (the `uint16_t` at line 9 sits outside the anchored
`18,21`); still true at the tip. Severity: **cosmetic** — the quotes are correct and the flag names are
adjacent, readable lines in the same pinned file. No change proposed.

---

## Checks run that produced no finding (null results, with commands)

1. **Census validator against the tip tree** — no rule fires on either row.
   ```
   git archive 0f3a5436 | tar -x -C tiptree
   bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <scratch>/tiptree/corpus/SOURCES.md
   → exit 0, 38 lines: 36× W04 (duplicate url, all on S042/S045/S097/S119-S121/S277/S303/S307/S317/S318/S320/S321/S324/S326/S327/S332/S353/S354 …, none S390/S391), 1× W01 (S277)
   grep -nE 'S390|S391' census-tip3.txt   → no output
   ```
2. **C1 counter at the tip** — the frozen target sentence reproduces exactly:
   ```
   python3 -I quality/counters/c1-r56-autoreload-entry.py --repo . --rev 0f3a54361… --work <scratch>
   → MADO_AUTORELOAD_ENTRY: rev=0f3a5436… rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none   (exit 0)
   ```
3. **C1 control harness at the tip** — 12/12 controls pass:
   ```
   python3 -I quality/check-r56-controls.py --claim c1 --repo . --rev 0f3a5436… --work <scratch>
   → MADO_R56_CONTROLS: claim=c1 good=ok controls=12/12 verdict=OK   (exit 0)
   ```
4. **C3 counter at the tip** — S390 and S391 are both inside the back-reference set:
   ```
   python3 -I quality/counters/c3-r56-used-by.py --repo . --rev 0f3a5436… --work <scratch>
   → MADO_USED_BY: rev=0f3a5436… entries=71 rows=332 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none   (exit 0)
   ```
5. **Anchor-locator EOF bound for both rows** — no locator past EOF (see per-row sections); a deliberately
   over-long locator *is* caught (`inotify.7.html:186,9999` → `missed=scope:K29,scope:K30`), so the bound
   is live.
6. **Upstream drift** — two independent fetches per URL (different User-Agent) plus a `--compressed` fetch
   all reproduced the anchor-cell sha256 byte-for-byte; the S391 URL is commit-pinned so drift is
   impossible; the S390 URL is a floating release URL (see D3).

## Not verified

- Upstream drift **after** 2026-10-30 is not covered (both fetches are point-in-time).
- Whether the S390 page will be re-issued at man-pages 6.20 with different line numbers: the 6.19→6.20 roff
  diff touches line 140 and the FILES section, i.e. the *roff* line numbers shift; the man7 HTML is
  regenerated from the same roff, so the anchor locators 186/262 could move when 6.20 is promoted. Not
  predicted here — only the flag.
- Tier A/B assignments and the `mined` status are author judgment; I checked consistency with the registry
  convention, not correctness.
- I did not evaluate the C2/C3 legs beyond the run above; those are other seats' scope.

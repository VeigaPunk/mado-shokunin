# R56W3ScoutRows5b — registry rows S390 and S391 re-opened independently (second sample)

**Item attacked.** Registry rows **S390** (`Linux man-pages 6.19 inotify(7) man page`) and **S391**
(`Hyprland 0.56.2 property refresher header - refresh flag enum`) in
`corpus/SOURCES.md`, at the lane tip **`0f3a54361a9824484d0801679ceb1fd8ac7c32e1`**.

This is the **second sample**: attempt-1's wave-2 scout (`w2/R56W2ScoutRows5.md`) fetched these two rows at
`28fc86ac2359ec27406d8a2c63bef82ea6e947ed`. This seat re-derived both rows from scratch at the tip. The
two rows are byte-identical between the two revs (`sha256` of the S390+S391 line pair =
`5a314e1f0e5e90ea1fd4cbd0c0767bf4170b093c366837b0ac006aa53309d8cb` at both `28fc86ac` and the tip), so
the re-derivation is independent in method but confirms the same bytes.

**What I did.** Fetched both URLs myself into scratch (not from the lane's pins); sha256'd the bytes and
compared against the row's anchor cell and against `frozen-tables-v2.json` where the row is tabled; located
the gate quote from the tip lesson's '## Gate' table in the upstream bytes and reported its line number;
checked the anchor locators against the file's line count; then went beyond the item and mutation-tested
what the frozen instrument actually enforces about these two rows.

---

## Verdict

| row | fresh-fetch sha256 | vs anchor cell | vs frozen table | gate quote line | locators ≤ line count | verdict |
|---|---|---|---|---|---|---|
| S390 | `79f5ab18e2fc423631cf4949ef82ca1384844353ea11a4dba42e1a77e8fdd8fd` (44066 B) | MATCH | MATCH (`c1.pin_sha256["man7-inotify.7.html"]`) | **186** | yes — `186, 262` ≤ 920 | **MATCH** |
| S391 | `37acaaf16a24dcfe89d0702818b82d300d0da5e91ef1ba47494f7fd2ab0af2d0` (1322 B) | MATCH | **ABSENT from every frozen leg** | **18** | yes — `18, 21` ≤ 41 | **MATCH on content; D1 process finding** |

Both rows' **bytes are correct and reproduce exactly**. The findings below are about what the frozen
instrument does and does not *prove* about these rows.

---

## 1. What I ran (decisive lines)

### Fetches — this seat, 2026-10-30, into `/fast/scratch/hyaku/mado-r56/R56W3ScoutRows5b/`

```
curl -sSL -o man7-inotify.7.html 'https://man7.org/linux/man-pages/man7/inotify.7.html'
HTTP=200 SIZE=44066
79f5ab18e2fc423631cf4949ef82ca1384844353ea11a4dba42e1a77e8fdd8fd  man7-inotify.7.html

curl -sSL -o Hyprland-PropRefresher.hpp 'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/supplementary/propRefresher/PropRefresher.hpp'
HTTP=200 SIZE=1322
37acaaf16a24dcfe89d0702818b82d300d0da5e91ef1ba47494f7fd2ab0af2d0  Hyprland-PropRefresher.hpp
```

Second independent fetch of each (different User-Agent) → identical sha256 and size. `curl --compressed`
on S390 → identical sha256. (`Accept-Encoding: gzip` *without* `--compressed` yields a different sha256 —
the gzip container; so the anchor hash is over the decoded document, consistent with the anchor cell.)

### Comparisons

```
git show 0f3a5436:.ufo/waves/round-56/fetch/man7-inotify.7.html | sha256sum
79f5ab18e2fc423631cf4949ef82ca1384844353ea11a4dba42e1a77e8fdd8fd      == fresh fetch, == anchor cell, == c1.pin_sha256
git show 0f3a5436:.ufo/waves/round-56/fetch/Hyprland-PropRefresher.hpp | sha256sum
37acaaf16a24dcfe89d0702818b82d300d0da5e91ef1ba47494f7fd2ab0af2d0      == fresh fetch, == anchor cell
cmp <fresh> <committed pin>                                            → identical, both rows
```

### Gate quotes located in the fresh bytes

Tip lesson `corpus/lessons/round-56.md` '## Gate' table:
- line 25 — `| S390 | https://man7.org/linux/man-pages/man7/inotify.7.html | \`File opened for writing was closed.\` (:186) |`
- line 26 — `| S391 | …/PropRefresher.hpp | \`REFRESH_CONFIG_WATCHER     = (1 << 8),\` (:18) |`

| row | quote | lesson line | occurrence in fresh bytes | verdict |
|---|---|---|---|---|
| S390 | `File opened for writing was closed.` | 186 | **line 186**, 1 occurrence | MATCH |
| S390 | `Don't dereference <i>pathname</i> if it is a symbolic link.` (2nd locator) | 262 | **line 262**, 1 occurrence | MATCH |
| S391 | `REFRESH_CONFIG_WATCHER     = (1 << 8),` | 18 | **line 18**, 1 occurrence | MATCH |
| S391 | `REFRESH_ALL = std::numeric_limits<std::underlying_type_t<ePropRefreshProp>>::max(),` (2nd locator) | 21 | **line 21**, 1 occurrence | MATCH |

### Anchor locators vs line count (registration-v2 E3 bound)

```
S390: 919 newlines; len(split(b"\n")) = 920;  locators 186, 262 → both ≤ 920   PASS
S391:  40 newlines; len(split(b"\n")) =  41;  locators  18,  21 → both ≤  41   PASS
```

### Version token, verified inside the S390 bytes

```
801:       This page was obtained from the tarball man-pages-6.19.tar.gz
811: <span class="footline">Linux man-pages 6.19            2026-02-14   <i>inotify</i>(7)</span>
```

### Second-mirror corroboration for S390 (the man7 URL is a floating release URL)

```
curl -sSL 'https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man7/inotify.7?h=man-pages-6.19'
208:.BR IN_CLOSE_WRITE " (+)"
209-File opened for writing was closed.
310:.BR IN_DONT_FOLLOW " (since Linux 2.6.15)"
311-Don't dereference
312-.I pathname
313-if it is a symbolic link.
```

Both quoted descriptions are present in the 6.19 roff source at the kernel.org mirror — independent of
man7.

### Entry rows citing the two ids — byte-exact at their stated lines

| row | entry row | locator | occurrences in fresh bytes |
|---|---|---|---|
| S390 | K29 | `man7-inotify.7.html:186` | `[186]` |
| S390 | K30 | `man7-inotify.7.html:262` | `[262]` |
| S391 | E08 | `Hyprland-PropRefresher.hpp:18` | `[18]` |
| S391 | E09 | `Hyprland-PropRefresher.hpp:21` | `[21]` |

### Frozen instruments re-run at the tip (read-only, on a scratch clone)

```
python3 -I quality/counters/c1-r56-autoreload-entry.py --repo . --rev 0f3a5436… --work <scratch>
MADO_AUTORELOAD_ENTRY: rev=0f3a5436… rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none   (exit 0)

python3 -I quality/check-r56-controls.py --claim c1 --repo . --rev 0f3a5436… --work <scratch>
MADO_R56_CONTROLS: claim=c1 good=ok controls=12/12 verdict=OK   (exit 0)

python3 -I quality/counters/c3-r56-used-by.py --repo . --rev 0f3a5436… --work <scratch>
MADO_USED_BY: rev=0f3a5436… entries=71 rows=332 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none   (exit 0)
```

---

## 2. Defects

### D1 — S391 sits outside every frozen leg — **weakens the claim** (process; pre-existing, disclosed)

**Input that shows it.**

```
python3 -I -c "import json; d=json.load(open('.ufo/waves/round-56/frozen-tables-v2.json'))['c1']; \
  print(d['rows'].get('S391'), d['new_row_ids'], \
        'Hyprland-PropRefresher.hpp' in d['pin_sha256'], \
        'Hyprland-PropRefresher.hpp' in d['pin_suffix'])"
None ["S383","S384","S385","S386","S387","S388","S389","S390"] False False
```

`registration-v2.md:75` recounts "rows S383-S390"; `registration-v2-errata.md` (E12-E14) does not disclose
S391. Disclosed at the tip as lesson item M56-9 (`corpus/lessons/round-56.md:82`), first raised at attempt-1.

**Consequences, each demonstrated by mutation on a scratch clone of the tip** (never the lane):

| mutation | counter output |
|---|---|
| S391 anchor-cell `sha256:` → all zeros | `TARGET_MET missed=none`, exit 0 |
| S391 URL rev → `0000…0000` | `TARGET_MET missed=none`, exit 0 |
| S391 anchor cell: drop locator `21` | `TARGET_MET missed=none`, exit 0 |
| S391 teaches cell: "contains the config-watcher bit" → "DOES NOT contain" | `TARGET_MET missed=none`, exit 0 |
| S391 scope cell: "maximum" → "minimum" of the underlying type | `TARGET_MET missed=none`, exit 0 |
| **the S391 pin file itself** `(1 << 8)` → `(1 << 9)` | `TARGET_MET missed=none`, exit 0 |

**Positive control on the same harness** (so the rig is live): mutating the **S390** pin file *is* caught —
`MADO_AUTORELOAD_ENTRY: … verdict=TARGET_MISSED missed=quote:K29,pin_hash`, exit 1.

`receipts/pins-extra.sha256` records the S391 pin hash but **no instrument reads it**
(`grep -rn "pins-extra" quality/ tools/ .ufo/waves/round-56/*.py` → null). The pin hash is a receipt, not a
check.

**Routing.** Adding S391 to a frozen leg changes the frozen predicate → **routed finding for round 57**,
not a change here. Measured recipe: adding `S391` to `c1.rows` / `c1.pin_sha256` / `c1.pin_suffix` makes
the counter fail closed on `missed=tables_sha` (the embedded frozen-tables hash no longer matches) — the
correct behaviour; the tables and the counter's embedded hash must move together in a v3.

### D2 — the anchor cell's sha256 / size / version strings are enforced by no instrument — **weakens the claim**

**Input that shows it.**

- The counter reads the anchor cell **only** through `scope_covers(cells[5], basename, line, nlines)`
  (`quality/counters/c1-r56-autoreload-entry.py:483`), which parses the `<basename>:<locators>` prefix and
  ignores the rest. `grep -n 'sha256:' quality/counters/c1-r56-autoreload-entry.py` → no anchor-cell hit.
- The census parses the anchor cell (`scripts/sources-census.sh:627`) and never uses it
  (`awk 'NR>627 && /\$scope|\$teaches/'` → null); the census has no sha256 handling at all.

| mutation | counter output |
|---|---|
| S390 anchor cell `sha256:` → all zeros | `TARGET_MET missed=none`, exit 0 |
| S390 anchor cell size `44066 B` → `99999 B` | `TARGET_MET missed=none`, exit 0 |
| S390 anchor cell version token `Linux man-pages 6.19 (2026-02-14)` → `Linux man-pages 9.99 (2099-01-01)` | `TARGET_MET missed=none`, exit 0 |
| S390 URL host `man7.org` → `example.com` (suffix + rev token kept) | `TARGET_MISSED missed=source_cell:K29,source_cell:K30,new_rows` — **caught** |

So the *locator* and *URL* halves of the anchor cell are enforced; the *hash, byte count and version token*
are decorative to every lane instrument. The hash is true today (four-way identity above), but nothing
would notice a later edit falsifying it. The lesson's frozen sentence (line 13: "sha256 equal to the anchor
cell and to the frozen table for S383-S390") is true at the tip and is **not machine-enforced**.
Routing: **round 57**.

### D3 — S390's `rev_rule` token is self-saturating; the URL is a floating release URL — **weakens the claim**

**Input that shows it.** `frozen-tables-v2.json` `c1.rev_rule` gives the man7 pin the token
`man7.org/linux/man-pages/man7/inotify.7.html` — the *URL path itself*, not a revision. The counter's test
is `tok in urls[-1]` (`source_cell_ok`, counter line 468), true for any URL containing the path, so it can
never fail for a well-formed S390 URL and never detects a version change. Demonstrated: appending
`?h=man-pages-6.99` to the S390 URL leaves the token present and the path suffix intact →
`TARGET_MET missed=none` for the S390 legs.

Contrast — the Hyprland rows use a real commit sha as the token, and the check bites: S389's URL rev →
`0000…0000` gives `TARGET_MISSED missed=source_cell:K27,source_cell:K28,new_rows`.

**Not a defect in the bytes:** the page does carry the version (`Linux man-pages 6.19 2026-02-14`,
verified) and the row's `recheck 90d` is the human guard. But the row's URL has no version in it, whereas
the only other man-pages row in the registry (S112) uses a version-pinned URL
(`…/man-pages.git/plain/man/man7/user_namespaces.7?h=man-pages-6.16`). `man-pages-6.20` already exists as
an upstream release tag (`git.kernel.org/…/man-pages.git/refs/tags` lists `man-pages-6.20`; its `inotify.7`
differs from 6.19 at roff line 140 and the FILES section), and man7.org still serves 6.19 for this page as
of 2026-10-30. The page will change under the row's own URL when man7 promotes 6.20, and because the roff
line numbers shift between tags, the anchor locators 186/262 could move with it.
Severity: **weakens the claim** (revision check vacuous; reproducibility not durable; content correct today).
Routing: **round 57**.

### D4 — the E-rows that cite S391 are outside every counter leg — **weakens the claim**

**Input that shows it.** The frozen `c1.k` holds 30 K ids and `c1.h` holds 3 H ids; no E id is in either,
and the leg loop is `all_rows = [(r, "K") for r in c1["k"]] + [(r, "H") for r in c1["h"]]`
(`quality/counters/c1-r56-autoreload-entry.py:505`).

| mutation | counter output |
|---|---|
| entry **E08** proposition: "REFRESH_CONFIG_WATCHER as bit 8" → "as bit 9" | `TARGET_MET missed=none`, exit 0 |
| entry **E09** locator `Hyprland-PropRefresher.hpp:21` → `:9999` | `TARGET_MET missed=none`, exit 0 |

E08 and E09 are S391's *only* citing rows, and they are not byte-checked, scope-checked or lexically
grounded by any lane instrument. The quotes are in fact byte-exact (verified above), so this is a coverage
gap, not an error — a sharper form of what `w2/R56W2RevDocs.md` F9 and `w1/R56ExecC1Harness.md` A3
already noted. Routing: **round 57**.

### D5 — S390's anchor locators do not cover the flag-name lines — **cosmetic**

**Input that shows it.** The anchor is `inotify.7.html:186,262` — the *description* lines. The flag names
are one line above each:

```
185:           <b>IN_CLOSE_WRITE </b>(+)
186:                  File opened for writing was closed.
261:           <b>IN_DONT_FOLLOW </b>(since Linux 2.6.15)
262:                  Don't dereference <i>pathname</i> if it is a symbolic link.
```

The scope cell says "the meaning of the IN_CLOSE_WRITE and IN_DONT_FOLLOW **flags**" and the teaches cell
names both flags — but the anchored lines 186/262 do not contain the flag names, and the entry's own prose
cites `man7-inotify.7.html:185-186` and "lines 261-262", reaching one line past the registry anchor on
both sides. The scope leg only requires the *quoted* line to be covered; moving the anchor to `185,261`
(dropping the descriptions) does fail (`TARGET_MISSED missed=scope:K29,scope:K30`), but the reverse is not a
failure condition.

Same shape as attempt-1's D2 for S391 (the `uint16_t` at line 9 sits outside the anchored `18,21`); still
true at the tip. No change proposed.

---

## 3. Checks that produced no finding (null results, with commands)

1. **Census validator against the tip tree** — no rule fires on either row.
   ```
   git archive 0f3a5436 | tar -x -C <scratch>/tiptree
   bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <scratch>/tiptree/corpus/SOURCES.md
   → exit 0, 38 lines: 36× W04 (duplicate url — S042/S045/S097/S119-S121/S277/S303/S307/S317/S318/S320/S321/S324/S326/S327/S332/S353/S354…, none S390/S391), 1× W01 (S277)
   grep -nE 'S390|S391' census-tip3.txt   → no output
   ```
2. **C1 counter / controls / C3 at the tip** — all reproduce the frozen target sentences (see §1).
3. **Anchor-locator EOF bound for both rows** — no locator past EOF; a deliberately over-long locator *is*
   caught (`inotify.7.html:186,9999` → `missed=scope:K29,scope:K30`), so the bound is live.
4. **Upstream drift** — two independent fetches per URL plus a `--compressed` fetch all reproduced the
   anchor-cell sha256 byte-for-byte; S391's URL is commit-pinned (drift impossible); S390's is a floating
   release URL (see D3).

---

## 4. Deliverables

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ScoutRows5b/receipts/rows.md`
  — per-row receipts: fetch commands and hashes, the four-way/two-way comparisons, gate-quote line
  locations, anchor-locator EOF bounds, entry-row quote checks, D1–D5 with their reproducing inputs, the
  null-result commands, and what was not verified.

---

## 5. Not verified

- Upstream drift **after** 2026-10-30 (both fetches are point-in-time).
- Whether S390's line numbers move when man7 promotes man-pages 6.20 (the roff line numbers shift between
  tags; not predicted here).
- Tier A/B and `mined` are author judgment; I checked registry consistency, not correctness.
- C2 and the C3 legs beyond the single counter run above — other seats' scope.

---

## 6. Compliance

- **Tooling**: no installs, no upgrades, no host-service touches. `curl`, `git`, `python3 -I`, `bash`, `awk`,
  `grep`, `cmp`, `diff`, `sha256sum` were all pre-existing; the pacman guard was never invoked. (Nothing
  installed, so no tool/version/channel/reason row is owed.)
- **Scratch**: everything I created lived under
  `/fast/scratch/hyaku/mado-r56/R56W3ScoutRows5b/` and was removed (`rm -rf`) after the deliverables were
  written and before this seat yielded; the directory no longer exists.
- **Lane**: no tracked file was edited; no git/jj mutation of any kind was performed against the lane or the
  fleet repo. All mutations were made on **copies** — one `git clone --shared` of the lane into scratch
  (`tipclone`, `git -C tipclone rev-parse --show-toplevel` = the scratch path, asserted before the first
  commit) plus `cp -a` clones of that clone; commits used `-c user.name=ctl -c user.email=ctl@ctl`.
  Scoring used `git show <rev>:<path>` and `git archive` against `0f3a5436…`; the working tree was never
  scored.
- **Writes**: only my seat's own deliverable paths — `.ufo/waves/round-56/w3/R56W3ScoutRows5b.md` and
  `.ufo/waves/round-56/w3/R56W3ScoutRows5b/receipts/rows.md`. Nothing else in the lane was written.
- No credential material appears in any file I wrote.

# ConnSourcesUsedBy — reciprocal joins for the round-18 P3/P5 rows

Seat: MadoR18.ConnSourcesUsedBy (connector, leaf). Round 18 / w1.
Assignment: plan the reciprocal joins (row `used-by` ↔ note `source:` line) for the
sources the P3/P5 notes will cite, and screen S001-S071 for walker / elephant /
omarchy / swaybg URLs (W04 duplicate-url risk). No writes outside this report; every
command was read-only (git `ls-remote` only, curl bodies already on disk, sha256sum,
python3 on /tmp fixtures). Host pause honoured: no pacman/expac/systemctl/journalctl/
hyprctl/walker/elephant/swaybg/omarchy-* invocation, no compositor or input probe.
Tooling: nothing installed or upgraded.

## 1. Axes

- **C2 coverage (primary).** The join is what makes a fetched row *count*: a note is
  credited only when each head `source:` `S###` token resolves to a row that is
  `mined`, tier `A`, and whose `used-by` cell contains the note path *exactly*.
- **C1 calibration / C3 operability (untouched).** This seat writes no QUALITY text
  and no tool; no interaction.
- **Harm watch (registry census).** Adding rows must not add a W04 line or an E04
  failure; the historical set stays exactly S030 / S042 / S045.

## 2. Evidence

### 2.1 Existing rows S001-S071 — zero collisions

Command shape: parse every `| S0..` row inside `## Registry`, apply the census's own
`url_of()` normalisation (first `https?://…`, strip fragment/trailing slash, lowercase
host), compare with (a) the URLs the two notes cite and (b) all 200-status fetch
receipts under `fetch/NoteWalker/` and `fetch/NoteTheme/`.

- S001-S071 hold **51 distinct normalized URLs**.
- `grep -Ei 'walker|elephant|swaybg|basecamp|hyprpaper|wallpaper' corpus/SOURCES.md`
  → **0 hits**. The `omarchy` strings are S015's own-work note path and the local
  checkout paths in S020, S059 and S071; `url_of()` returns empty for them, so they
  never enter the URL key.
- **Old × new collisions: none**, for the 41 distinct 200 URLs the two note seats
  had fetched at 2026-10-20T15:49Z (not only the cited subset).
- Cross-note collisions: **none** (P3 and P5 cite disjoint URL sets).
- The three historical W04 lines are unchanged: S030, S042, S045. A local replica of
  the census's W04/E04 awk logic over the 23-row plan below returns exactly those
  three and nothing else.

### 2.2 What the notes actually cite (state at 2026-10-20T15:47Z)

| note | head `source:` tokens | structure (surface/headings/floor/[UNK]) | credited today |
|---|---|---|---|
| `corpus/knowledge/walker-route-r18.md` | 19 × `S0xx-pending` (18 https URLs + `/var/log/pacman.log`) | valid: `surface: P3`, 4 sections, floors 115/73/20/37, `[UNK]` present | **0** — `S0xx-pending` has no `S\d{3}` |
| `corpus/knowledge/theme-route-r18.md` | 4 × `S0xx-pending-{A,B,C,D}` | valid: `surface: P5`, floors 22/34/6/10, `[UNK]` present | **0** — same reason |

This is the binding failure mode: both notes are documentary-valid but credit nothing
until the pending tokens are replaced with real `S\d{3}` ids that resolve.

### 2.3 Receipts behind the cited sources

Every receipt in both note fetch dirs was re-hashed against its body at
2026-10-20T15:49Z: **NoteWalker 27/27, NoteTheme 17/17 digests and byte counts
match** (the three non-200 lines are 404s: `swaybg-v1.2.2-doc.html`,
`doc/swaybg.1.scd`, and the theme.name probe; none cited). Every one of the 18 https
URLs in the P3 note line maps to a 200 receipt by its exact `url` field. For P5, rows
A-C map to 200 receipts; row D and the P3 pacman.log row are host-file rows (no web
body). Only the root `swaybg.1.scd` (200, 1124 B) can back a swaybg row.

Tag → commit (re-run by this seat, `git 2.56.0`, read-only `ls-remote`):

| repo / tag | advertised ref | peeled commit |
|---|---|---|
| `abenz1267/walker` `v2.17.2` | `a515085fd39fae80acc086c8fbfd9b7771a9a11d` (lightweight) | same |
| `abenz1267/elephant` `v2.22.1` | `8f1e21d6efe40b8b3953f95b9574f99f717caf91` (lightweight) | same |
| `basecamp/omarchy` `v3.8.4` | `8fcc9d6048af4cb0e3af8512c78049857a3b53dd` (lightweight) | same |
| `swaywm/swaybg` `v1.2.2` | tag object `3ca0f88fee1a0c83f26ffe2341207d84c7243e7a` (**annotated**) | `a59ea3dbe543b44177ad1b5bdb4afa1c5be9b9d2` |

The P5 note's row A already uses the peeled `a59ea3db…`; correct. The P3 note's
`verified-at` line says "all lightweight" — correct for walker/elephant/omarchy.

### 2.4 Intra-round duplication (the real W04 risk)

The old registry is clean, but **the round-18 scouts fetched the same files as the
notes**. If L1 rows both, the census sees the second row:

- same normalized URL + same scope string + both non-rejected → **E04, failing**;
- same URL + different scope → **W04, non-failing but a new visible line**.

Exact same-URL fetch overlap (seats, from all `fetch/*/receipts.jsonl`):

| cited URL | seats that fetched the same URL string |
|---|---|
| walker `README.md` | NoteWalker, SrcWalkerReadme, SrcWalkerDefaultConfig, SrcWalkerChangelog, SrcWalkerDocsSite, SrcWalkerThemes, SrcElephantReadme |
| walker `resources/config.toml` | NoteWalker, SrcWalkerReadme, SrcWalkerDefaultConfig, SrcWalkerChangelog, SrcWalkerThemes |
| walker `src/config.rs` | NoteWalker, SrcWalkerConfigPaths, SrcWalkerThemes |
| walker `src/main.rs` | NoteWalker, SrcWalkerThemes |
| walker `src/theme/mod.rs` | NoteWalker, SrcWalkerConfigPaths, SrcWalkerThemes |
| walker `Cargo.toml` | NoteWalker, SrcWalkerThemes |
| elephant `README.md` | NoteWalker, SrcElephantReadme, SrcElephantProviders |
| elephant `internal/comm/comm.go`, `cmd/elephant/elephant.go`, `pkg/common/config.go` | NoteWalker, SrcElephantProviders |
| omarchy `bin/omarchy-launch-walker` | NoteWalker, SrcOmarchyBackground |
| omarchy `bin/omarchy-theme-set` | NoteTheme, SrcOmarchyThemeSet, SrcOmarchyThemeHooks, SrcOmarchyThemeLayout, SrcOmarchyBackground |
| omarchy `bin/omarchy-theme-bg-next`, `bin/omarchy-theme-bg-set` | NoteTheme, SrcOmarchyThemeSet, SrcOmarchyThemeHooks, SrcOmarchyBackground |
| omarchy `default/hypr/autostart.conf` | NoteTheme, SrcOmarchyThemeHooks, SrcOmarchyBackground |
| swaybg `swaybg.1.scd`, `main.c`, `background-image.c`, `README.md` | NoteTheme, MadoR18.SrcSwaybgMan |

Second-order trap: **the basecamp↔omacom URL split is census-blind.** NoteWalker's
receipts use `raw.githubusercontent.com/basecamp/omarchy/v3.8.4/...` (200, no
redirect). SrcOmarchyWalker fetched the same files as
`github.com/basecamp/omarchy/raw/v3.8.4/...` (final
`raw.githubusercontent.com/omacom/omarchy/v3.8.4/...`) and proposes rows on the
**omacom** form. Those are different normalized URLs, so two rows for one file raise
no census finding (demonstrated in `/tmp`: no new W04). Duplication must be stopped by
the one-row-per-file rule, not by the census.

## 3. Proposed move (one bounded proposal)

**Add exactly 23 rows — one per source the two notes cite, in citation order — and
replace the pending tokens positionally with those ids. Fold every scout row proposal
for an already-rowed URL into that single row; do not add a second row for any URL.**

Proposed slots (L1 assigns; S072-S099 reserved): P3 = S072-S090, P5 = S091-S094.
`used-by` is the **exact** repo-relative path (comma-separated only if a second note
ever cites the same row), because `measure.py`'s `used_by()` does an exact list match.

### 3.1 P3 rows — `used-by: corpus/knowledge/walker-route-r18.md`

| slot | source URL (row `source` cell must carry this exact URL) | receipt body in `fetch/NoteWalker/` | sha256 (prefix) |
|---|---|---|---|
| S072 | `https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/README.md` | `walker-v2.17.2-readme.md` | `9755f955d5c4` |
| S073 | `…/walker/v2.17.2/resources/config.toml` | `walker-v2.17.2-resources-config.toml` | `3c5c6867d021` |
| S074 | `…/walker/v2.17.2/src/config.rs` | `walker-v2.17.2-src-config.rs` | `93b6bd6f3603` |
| S075 | `…/walker/v2.17.2/src/main.rs` | `walker-v2.17.2-src-main.rs` | `f09466fecf90` |
| S076 | `…/walker/v2.17.2/src/data.rs` | `walker-v2.17.2-src-data.rs` | `996db119ba61` |
| S077 | `…/walker/v2.17.2/src/theme/mod.rs` | `walker-v2.17.2-src-theme-mod.rs` | `93287a1c389a` |
| S078 | `…/walker/v2.17.2/Cargo.toml` | `walker-v2.17.2-cargo.toml` | `d1676045d110` |
| S079 | `https://codeload.github.com/abenz1267/walker/tar.gz/refs/tags/v2.17.2` | `walker-v2.17.2-src.tar.gz` | `e50c606040b2` |
| S080 | `…/elephant/v2.22.1/README.md` | `elephant-v2.22.1-readme.md` | `aa19a7e2d1c0` |
| S081 | `…/elephant/v2.22.1/internal/comm/comm.go` | `elephant-v2.22.1-internal-comm-comm.go` | `2b4a6f1493be` |
| S082 | `…/elephant/v2.22.1/cmd/elephant/elephant.go` | `elephant-v2.22.1-cmd-elephant.go` | `c1c2ecaaafac` |
| S083 | `…/elephant/v2.22.1/pkg/common/config.go` | `elephant-v2.22.1-pkg-common-config.go` | `46ed4755bb3e` |
| S084 | `https://docs.rs/xdg/latest/xdg/struct.BaseDirectories.html` | `xdg-crate-basedirectories.html` | `0291cfe6cd80` |
| S085 | `…/basecamp/omarchy/v3.8.4/config/walker/config.toml` | `omarchy-v3.8.4-config-walker-config.toml` | `fecf71fa4253` |
| S086 | `…/basecamp/omarchy/v3.8.4/bin/omarchy-launch-walker` | `omarchy-v3.8.4-bin-omarchy-launch-walker` | `fd9e93f830bc` |
| S087 | `…/basecamp/omarchy/v3.8.4/bin/omarchy-restart-walker` | `omarchy-v3.8.4-bin-omarchy-restart-walker` | `9ac82d0c1370` |
| S088 | `…/basecamp/omarchy/v3.8.4/bin/omarchy-refresh-walker` | `omarchy-v3.8.4-bin-omarchy-refresh-walker` | `05cd9c672252` |
| S089 | `…/basecamp/omarchy/v3.8.4/default/walker/walker.desktop` | `omarchy-v3.8.4-default-walker-walker.desktop` | `5cb9874eedbc` |
| S090 | `/var/log/pacman.log` (host row; no web receipt) | — file bytes, `sha256 f34d34e72702…`; lines 1943, 2929, 3062, 3095, 3123 | — |

`kind`: `docs` for S072, S080, S084; `code` for the rest (S090 host `code`, as S059).
All tier `A`, status `mined`, opened 2026-10-20, recheck `on-release` (host row
`on-change`). Every row except S084 and S090 names walker or elephant in its source
cell (give S084 a scope that names walker, e.g. "the pinned walker `xdg` dependency's
search order"); S072-S083 name walker/elephant and S085-S089 name walker, so the P3
upstream clause is satisfied several times over.

### 3.2 P5 rows — `used-by: corpus/knowledge/theme-route-r18.md`

Take the four draft rows in `.ufo/waves/round-18/drafts/NoteTheme-rows.md` and change
two `source` cells so their first URL is the receipted raw URL (currently both name an
unfetched repo page, which breaks R17-V3 machine-checkability):

| slot | draft | corrected `source` cell (first URL) | receipt body / sha256 |
|---|---|---|---|
| S091 | A | `swaybg v1.2.2 man page and implementation — https://raw.githubusercontent.com/swaywm/swaybg/v1.2.2/swaybg.1.scd` | `swaybg-v1.2.2-swaybg.1.scd` `68ed5503298f`; `main.c` `ff93e60c…`, `background-image.c` `9aea12fc…`, `README.md` `a6720ded…` stay in the anchor |
| S092 | B | `omarchy v3.8.4 theme writers — https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-theme-set` | `omarchy-theme-set-v3.8.4.sh` `79069c80…`; `bg-next` `ee482812…`, `bg-set` `638f265f…`, `theme-set-templates` `01264122…`, `autostart.conf` `acb6a668…` stay in the anchor |
| S093 | C | unchanged: `https://github.com/basecamp/omarchy/tree/v3.8.4/themes/matte-black` | tree HTML `50c1ac25…`; backgrounds tree `9e1160a0…`; `colors.toml` `dbdd13a6…` |
| S094 | D | unchanged: host P5 state/consumer paths, no URL | theme.name `48749715…`, background `55fa691a…`, walker.css `481267af…`, etc. |

Row C's URL is the receipt's `url` field (its `final_url` is the `github.com/omacom/…`
redirect; record that in the anchor, keep the fetched form as the row URL). Row D is a
host row like S059/S071. Do **not** add a separate row for the raw
`default/hypr/autostart.conf` URL: it is anchored inside S092 with its own receipt and
is not a separate token in the note.

### 3.3 Token substitution (exact, positional)

- P3 line 1 has **19 identical** `S0xx-pending` tokens. A global
  `s/S0xx-pending/S072/` would give all 19 the same id. Substitute with a **counter in
  citation order** (S072…S090), or rewrite line 1 wholesale.
- P5 line 1 has 4 distinct tokens `S0xx-pending-{A,B,C,D}`; map A→S091, B→S092,
  C→S093, D→S094 (replace the whole token, suffix included).
- Keep line 1 a **single physical line**; keep `surface: P3` / `surface: P5` exactly.
- After substitution `measure.py` finds 19 / 4 `S\d{3}` tokens; every one must resolve.

### 3.4 What not to row

Do not create rows for the NoteWalker fetches the note does not cite: the two git-tree
API URLs, elephant `pkg/common/menucfg.go`, `pkg/common/util.go`, the four elephant
provider READMEs, and omarchy `default/walker/restart.conf`. They are background
bodies; rowing them adds URLs (and duplicate risk with SrcElephantProviders /
SrcWalkerChangelog) without joining to either note. Scout row proposals for cited
URLs (SrcWalkerReadme A/B, SrcWalkerDefaultConfig rows, SrcWalkerConfigPaths A/B,
SrcOmarchyThemeSet, SrcSwaybgMan, SrcOmarchyWalker) are **folded** into the 23 rows:
one row per URL, `used-by` = the note.

## 4. Risks (explicit contradictions / failure modes)

1. **Scout rows added alongside note rows** → E04 if the scope string repeats, W04 if
   not. Census exit would still be 0 for W04, but the harm-watch text "three historical
   W04" would become false. Fix: the 23-row whitelist; no second row per URL.
2. **Census-blind owner split** (basecamp vs omacom raw forms; also
   `github.com/basecamp/omarchy/raw/...`). Two rows for one file can pass the census
   silently. Fix: one row per file; record `final_url` in the anchor.
3. **Partial joins are invisible to the instrument.** With S085's `used-by` changed to
   `—`, the P3 note still credits with 18/19 ok sources (`measure.py` counts the note,
   not each token). The reciprocal join would be *claimed* but incomplete. Fix: the
   strict checker in §5, not `measure.py` alone.
4. **Pending tokens left in place** → 0 `S\d{3}` → both notes credit nothing even
   though their prose and receipts are complete.
5. **P5 draft A/B source cells name repo pages with no receipt** → R17-V3 closure
   cannot map row→body. Fixed by §3.2.
6. **404 bodies** (`swaybg` doc tree/doc path, theme.name probe) must never back a
   row; only the root `swaybg.1.scd` (200) is creditable.
7. **Host rows have no web receipt** (S090 pacman.log, S094 host theme state). The C2
   claim's "each new credited row backed by a committed raw fetch receipt" must be
   read as applying to web rows; these two rest on file-byte digests, as S059/S071 did.
   If closure reads it literally, the note/lesson must state the host-file exemption.
8. **Id assignment drift**: if L1 renumbers, the mapping is by URL, not by my slot
   numbers; the note-line replacement must follow the same order as the final row
   order, and the strict checker re-verifies.

## 5. Verification (runnable, shown to bite)

### 5.1 Strict join checker (run after integration; exits 1 on any gap)

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I - <<'PY'
import re, json, pathlib
root = pathlib.Path('.')
reg = {}; inreg = False
for line in (root/'corpus/SOURCES.md').read_text().splitlines():
    if line.startswith('## '): inreg = line.strip() == '## Registry'; continue
    if not inreg or not line.startswith('|'): continue
    c = [x.strip() for x in line.split('|')]
    if len(c) == 13 and re.fullmatch(r'S\d{3,}', c[1]): reg[c[1]] = c
def ok(sid, path):
    r = reg.get(sid)
    return bool(r) and r[8] == 'mined' and r[4] == 'A' and path in [p.strip() for p in r[11].split(',')]
bad = 0
for note, seat in (('corpus/knowledge/walker-route-r18.md', 'NoteWalker'),
                   ('corpus/knowledge/theme-route-r18.md', 'NoteTheme')):
    head = (root/note).read_text().splitlines()[:15]
    toks = [t for l in head if l.startswith('source:') for t in re.findall(r'S\d{3}', l)]
    unresolved = [t for t in toks if not ok(t, note)]
    recs = [json.loads(l) for l in (root/'.ufo/waves/round-18/fetch'/seat/'receipts.jsonl').read_text().splitlines()]
    norec = []
    for t in toks:
        m = re.search(r'https?://[^\s;,()]+', reg[t][2]) if t in reg else None
        if not m: continue
        u = m.group(0).rstrip('/')
        hit = [r for r in recs if r['http_status'] == 200 and u in (r['url'].rstrip('/'), r['final_url'].rstrip('/'))]
        if not hit: norec.append((t, u))
    print(note, 'tokens', len(toks), 'unresolved', unresolved or 0, 'no-receipt', norec or 0)
    bad += bool(unresolved or norec or len(toks) == 0)
raise SystemExit(1 if bad else 0)
PY
```

Expected after integration: `tokens 19 unresolved 0 no-receipt 0` and
`tokens 4 unresolved 0 no-receipt 0`, exit 0. A `/tmp` dry-run of the exact 23-row
plan (ids S072-S094, notes substituted) returned **P3 19/19 ok, P5 4/4 ok** under the
`measure.py` c2 code path, with no rejected notes.

### 5.2 Census (L1-owned gate; run once at integration)

```sh
TZ=UTC bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  mado-shokunin --root /home/vgpnk/Projects/shokunin --today 2026-10-20
```

Expected: exit 0, and exactly the three historical W04 lines (S030, S042, S045). Any
new `W04`/`E04` line means a duplicate row slipped past §3. A `/tmp` replica of the
census's W04/E04 logic reproduced the three historical lines on the 23-row plan; a
same-URL different-scope duplicate produced a new W04, a same-URL same-scope duplicate
produced **E04**, and the omacom-form duplicate produced **nothing** (risk 2).

### 5.3 Declared C2 command (L1, after the rows+notes land)

`python3 .ufo/waves/round-17/measure.py REV` → `c2.count` 6/6
(P3/P5 covered), assuming the two notes' proofs stay as checked here.

## 6. Affected axes / second-order effects

- **C2 coverage**: P3 and P5 become creditable (6/6) only if the 23 rows land with the
  exact `used-by` strings and the positional token substitution. No runtime claim.
- **Contract/registry**: row count 71 → 94; append-only rules untouched (new rows, no
  in-place edits to old rows). The `used-by` cell is the only binding; `—` or a
  basename silently breaks the note.
- **Substrate**: all evidence is already in `fetch/NoteWalker/` and `fetch/NoteTheme/`
  (committed by L1); the rows must not cite bodies outside those dirs for their first
  URL.
- **Verification**: census stays at three W04; the strict checker adds the per-token
  join guarantee that `measure.py` does not provide. No axis is harmed.

# SourcesRowShape — S072+ row shape, census checks, duplicate-URL risk (round 18)

Seat: `MadoR18.SourcesRowShape` (leaf, report only). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`. No lane file was written except this report.
No web source was opened, so no fetch receipt is owed. No tool was installed or upgraded.

Axes named: (a) row shape that survives both the fleet census and the C2 counter,
(b) gate shape that binds every credited row to a receipt, (c) duplicate-URL risk the
census can and cannot see. Confidence tags: `[OBS]` read/measured bytes, `[INF]` inference.

## 0. What was read or run `[OBS]`

- `corpus/SOURCES.md:12-83` (Registry header + S001-S071), `:84-286` (Paths, Search log,
  Leads); four section headings at `:9 Registry`, `:85 Paths`, `:122 Search log`,
  `:260 Leads (unopened)`.
- `corpus/lessons/round-17.md:1-21` (Mistakes table shape), `:22-70` (§ Gate, incl. the
  new-rows table), `:74-140` (Capability, Wave-2 corrections) and `:154-176`.
- `corpus/knowledge/idle-lock-route-r17.md:1-15` and `corpus/knowledge/terminal-route-r17.md:1-15`
  (note head shape), `.ufo/waves/round-17/measure.py:1-60,110-310` (c1/c2, registry parser,
  `used_by`, `mined_a`, `SURFACE_KEYWORDS`, `REQUIRED_HEADINGS`, `HEAD_LINES`).
- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (header `:1-40`, target
  resolution `:492-560`, `usedby_findings` `:520-558`, `row_pass` `:560-700`, main
  `:700-806`); `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`
  (Shape + Rules 1-6 + the contract's own Census block).
- Ran read-only against the lane registry: `sources-census.sh validate|census|shared`.
- Read all `round-18/fetch/*/receipts.jsonl` plus every receipt body referenced by
  `NoteWalker` (26/26 sha256+bytes verified). Snapshot while seats were still writing:
  21 receipt files, ≥295 lines and ≥239 distinct `url` values (296/240 at the last
  recount), 5×404, and no sha256/bytes disagreement between any two fetches of one URL.
- `corpus/knowledge/theme-route-r18.md:1-16` (untracked draft), `.ufo/waves/round-18/drafts/NoteTheme-rows.md`,
  `drafts/FrontierDraft.md`, and the row proposals in `w1/reports/SrcWalkerReadme.md:178`,
  `SrcWalkerDefaultConfig.md:155`.
- Read-only git: `git ls-files .ufo/waves/round-18` → only `evidence/census-start.txt`;
  `git ls-files --error-unmatch corpus/knowledge/theme-route-r18.md` → not tracked.
- `/tmp` fixtures only for the rule probes in §3.4 (no lane file touched, no git/jj write).

## 1. Exact row shape for S072-S099

### 1.1 Placement

- Rows live **only** inside `## Registry` (SOURCES.md:9), appended after the current last
  row (S071, `:83`) and immediately before the blank line + `## Paths` (`:85`). The header
  (`:12`) and separator (`:13`) are not edited.
- Do **not** append at end of file. Verified `[OBS]`: a row-shaped line appended after
  `## Leads` produces `E12 S0NN row outside Registry section`, rc 1 — and the same happens
  for a "round-18 additions" table inside `## Paths` or `## Search log`. The per-row gate
  table therefore belongs in `lessons/round-18.md`, never in SOURCES.md.
- The heading must read exactly `## Registry`. `## Registry (round 18)` or any suffix
  turns every row into E12 for the census and makes `measure.py` find no rows `[OBS]` from
  the parser condition `trim(substr(line,3))=="Registry"` / `line.strip()=='## Registry'`.
- Start each row at column 0. The census tolerates 0-3 leading spaces; `measure.py`
  requires `line.startswith('|')`, so an indented row is invisible to C2 `[OBS]`.

### 1.2 The 11 cells (order is fixed; NF must be 13 on `split('|')`)

```
| S0NN | <title> — <canonical URL or path> | <kind> | <tier> | <scope> | <anchor> | <teaches> | <status> | <opened> | <recheck> | <used-by> |
```

| cell | rule | enforced by |
|---|---|---|
| `id` | `S` + 3 digits, next unused, never reused. Reserved here: **S072-S099**. `S0xx-pending` is not a row id and fails `S\d{3,}`; `measure.py` silently ignores such a row, and ids it ignores earn no C2 credit. | census E02/E03; `measure.py` `re.fullmatch(r'S\d{3,}')` (exit 2 on duplicate id) |
| `source` | `Title — canonical URL` (or path list for host bytes). URL must be lowercase `https://`: `url_of()` is case-sensitive, so `HTTPS://…` disables duplicate detection entirely, and `measure.py`'s upstream test looks for literal `https://`. When a cell aggregates several files, the **first** `https://` is the dedupe key — put the primary URL first. Host-only rows carry no URL (S020/S059/S071 precedent) and can never satisfy C2's upstream-row test. | E01 shape; `url_of()`; `measure.py` `'https://' in cells[2]` |
| `kind` | exact enum `spec` `docs` `paper` `code` `tool` `dataset` `talk` `book` `community` `own-work`. Tag-pinned upstream bytes → `docs` or `code`; host file bytes → `code`; own gates/notes → `own-work`. | E05 |
| `tier` | `A` `B` `C`. A = primary/authoritative **for this scope** (tag-pinned upstream raw bytes, official docs, host bytes, own re-runnable output). `community` is never A. Tier C cannot land clean: `mined` + real used-by → W01; `mined` + `—` → W03. Reject tier-C leads instead. | E06, E10, W01, W03 |
| `scope` | the claim/topic; never a copy of another row's scope text on the same URL. For a C2 credit row the surface word must be here or in `source`: P3 `walker`/`elephant`; P5 `theme`/`wallpaper`/`hyprpaper`/`swaybg` (case-insensitive, exactly those two cells — not `anchor`, not `teaches`). | E04/W04; `measure.py` `SURFACE_KEYWORDS` + `(cells[2]+' '+cells[5]).lower()` |
| `anchor` | section/heading + `file:line[-line]` + revision. Fetched bytes: tag and/or commit **plus** raw sha256 **plus** byte count (S056-S058, S063-S069 precedent). Host bytes: sha256 per file + line spans. Never a bare homepage. Round-17 shape carries `sha256 <hex>, <N> bytes`. | contract Shape; gate binding (§2) |
| `teaches` | one grounded learner benefit. Rejected rows: `REJECTED: <reason>; flip: <what would change the verdict>`. | W02 (`length<8`) |
| `status` | `queued` `mined` `rejected` only. Only `mined` + tier A + used-by naming the note is credited. | E07; `mined_a()` |
| `opened` | ISO `YYYY-MM-DD`, not later than the census `--today`. Rows opened this round: `2026-10-20`. | E08 |
| `recheck` | ISO date, `NNd`, or a symbolic cadence that starts with a letter (`on-release`, `on-change`, `on-session-change`, `on-gate-change`, `on-capture-change`, `on-compositor-release`). Symbolic values are reported, never judged overdue. | E09; `overdue` mode |
| `used-by` | comma-separated **lane-relative** paths that exist at census time, e.g. `corpus/knowledge/walker-route-r18.md`. No `./`, no backticks, no trailing punctuation; commas only (the contract snippet also treats `;` as a separator, the maintained tools do not). `—` only for queued/rejected; `mined` + `—` is W03 and earns no credit. | E11 (mined only); `used_by()` exact string match |

No `|` inside any cell: one literal pipe makes `NF!=13`, prints `E01 … fields=12`, and
**skips all remaining checks for that row** `[OBS]`, so a malformed row can look clean.

### 1.3 Credit-binding shape (C2, `measure.py` c2) `[OBS]`

- The note's first 15 lines must carry `source:` **at column 0** (not `- source:`), with
  `S\d{3}` tokens (`re.findall(r'S\d{3}', line)`); each credited token must resolve to a
  row with `status=mined`, `tier=A`, and `used-by` naming that exact note path.
- `surface: P3` / `surface: P5` must be the exact rstripped line, exactly one per note;
  any suffix is `MALFORMED` and the note covers nothing.
- Exact level-2 headings `## Upstream contract`, `## Host declaration`,
  `## Safe observation`, `## Unexercised behavior`; each body ≥3 non-blank lines; `[UNK]`
  inside the last one.
- At least one cited row must be kind `docs|spec|code`, carry a lowercase `https://` in
  `source`, and name the surface in `source` or `scope`.
- `S0xx-pending` does not match `S\d{3}`, so `corpus/knowledge/theme-route-r18.md:1`
  (currently `S0xx-pending-A…`) is rejected for C2 until L1 substitutes real ids **in the
  note head and in the rows in the same change** `[OBS]`.

### 1.4 Shape examples (not admitted evidence)

Values below are copied from verified receipts only to show the required column shape;
`teaches`/`scope` wording is illustrative and must be rewritten by the owning seat.

```
| S0NN | walker README @ v2.17.2 — https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/README.md | docs | A | walker's documented identity, elephant ordering and config/theme roots at the pinned tag | whole file sha256 9755f955d5c4e460ac8538e1b648ba2a3c86da37ceaa4d0655dca4d1ea3d2456 (7,926 B; HTTP 200; receipt NoteWalker/receipts.jsonl#walker-v2.17.2-readme.md, fetched 2026-10-20T15:40:36Z); tag v2.17.2 → commit a515085f… | <one learner benefit> | mined | 2026-10-20 | on-release | corpus/knowledge/walker-route-r18.md |
| S0NN | omarchy theme-set @ v3.8.4 — https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-theme-set | code | A | upstream Omarchy theme-set writer at tag v3.8.4 | whole file sha256 79069c8018a7d6d20f52e357b0b473bd99fad0c5f2914523171687103eeb9516 (2,147 B; HTTP 200; receipt NoteTheme/receipts.jsonl#omarchy-theme-set); tag commit 8fcc9d6048af4cb0e3af8512c78049857a3b53dd | <one learner benefit> | mined | 2026-10-20 | on-change | corpus/knowledge/theme-route-r18.md |
```

Both examples put the keyword (`walker`, `theme`) in `scope`, satisfy lowercase `https://`,
and name the note that must also cite the id. A row aggregating several files
(S059 precedent) is legal, but each file's sha must still appear in `anchor` and the gate
must list one table line per file (§2.3).

## 2. Gate shape (`lessons/round-18.md` § Gate)

Round-17's `## Gate` is the model; round 18 adds the receipt column required by R17-V3.
The block must contain, in this order:

1. **Candidates considered** — prose naming the families swept (walker/elephant tag bytes,
   omarchy tag bytes and manual, swaybg tag bytes, host theme/walker files, tier-C
   alternates, snippet-only and 404 leads).
2. **Admit / Reject** — one sentence per family stating the rule (tier-C restatement,
   snippet never opened, tag ≠ running binary, declared ≠ observed).
3. **New rows table** — six columns:

   ```
   | id | URL / path | located quote (≤25 words, line anchor) | raw sha256 | fetch receipt | status |
   ```

   `fetch receipt` = `.ufo/waves/round-18/fetch/<Seat>/receipts.jsonl#<body slug>` with
   `bytes`, `fetched_at`, `http_status`. One table line **per source file**; a row that
   aggregates files (e.g. the swaybg row A in `drafts/NoteTheme-rows.md`) gets one line
   per raw URL, each with its own sha and receipt.
4. **Receipt-binding check (runnable)** — for every credited row, require the triple
   agreement: row-anchor sha256 = receipt-line sha256 = `sha256sum` of the receipt body;
   equal byte count; `http_status` 200. Sketch:

   ```sh
   python3 - <<'PY'
   import hashlib, json, sys
   receipt_line, body = sys.argv[1], sys.argv[2]
   r = json.loads(open(receipt_line).read())
   b = open(body, 'rb').read()
   assert r['schema'] == 'mado-fetch-receipt-v1'
   assert r['http_status'] == 200
   assert len(b) == r['bytes'] and hashlib.sha256(b).hexdigest() == r['sha256']
   print('ok', r['url'], r['sha256'])
   PY
   ```

   The `http_status == 200` assertion is not cosmetic: three different 404 URLs share the
   14-byte body sha `d5558cd419c8d46b…`, and one 404 body is the empty-input digest
   `e3b0c44298fc1c14…` `[OBS]`. Sha equality alone cannot tell two error bodies apart.
5. **Status / recheck / used-by changes** to existing rows, each as `old → new` with the
   reason (contract rule 2). `anchor` and `teaches` are never edited in place; a correction
   is a new row whose `teaches` opens `supersedes S0NN —` (or, pre-closure, an old→new line
   in § Wave-2 corrections, as round 17 did for S059/S061/S066/S070).
6. **Rows before → after** with tier and status histograms, derived from the tracked
   `evidence/census-start.txt` and a new `evidence/census-end.txt`.
7. **Version binding** — `/var/log/pacman.log` **file read** only, with line numbers
   (walker `:2929`, elephant `:3095` per dispatch). No `pacman -Q`, no binary query; a
   tag or log line is not a running-binary fact.
8. **Census block** — exact commands, exit codes and output summary (validate, census,
   shared, overdue). State that W04 is a warning (rc 0) and list any new warning; the
   round target is delta zero against the three baseline W04s.
9. **Fetch-receipt ledger** — per-seat line counts, the 404s recorded and explicitly not
   credited, cross-seat sha agreement, and the commit at which receipts are tracked:
   `git ls-tree -r --name-only <REV> -- .ufo/waves/round-18/fetch`. Today only
   `.ufo/waves/round-18/evidence/census-start.txt` is tracked `[OBS]`, so C2's "committed
   raw fetch receipt" is **not yet** satisfied; the gate must cite the landing commit or
   state the gap as an open item.
10. **Paths entry** — append to `## Paths` a line of the contract form
    `- **Walker (P3) and themes/wallpapers (P5) routes, round 18** — S0NN → S0NN → …: why
    this order`, naming the read order (upstream contract before host declaration).
11. **Search log entry** — contract rule 5 counts: question/query, where, date,
    identified/screened/included/excluded, exclusion reasons, stop rationale (round-17
    entry at SOURCES.md:240+ is the prose model).
12. **Receipt-label precision (R17-V1/V2)** — any sentence attributing a verdict token
    cites a receipt that records that token at the revision described; any runnable
    receipt names `tool_sha256` and `measured_commit`; never cite a tool sha git never
    recorded. For fetch receipts the "tool" is the `curl` version string plus
    `fetched_at`; there is no tool-file sha to borrow, and the gate should say so instead
    of reusing `962919ce…`.

## 3. Census checks (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`)

### 3.1 Modes and invocations `[OBS]`

```sh
S=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
$S validate --file corpus/SOURCES.md --today 2026-10-20   # row checks; E-codes -> rc 1
$S census   --file corpus/SOURCES.md --today 2026-10-20   # rows + tier/status histograms
$S overdue  --file corpus/SOURCES.md --today 2026-10-20   # due dates and symbolic cadences
$S shared   --root /home/vgpnk/Projects/shokunin          # cross-lane exact-URL overlap
$S selftest                                               # script self-check
```

Exit codes: `0` clean or warnings only; `1` any E-code or overdue finding (or census
missing); `2` usage/environment/missing registry; `3` selftest failure. With `--file`,
the lane root (for E11 path existence) is the parent of `corpus/`.

### 3.2 Codes and what each obliges a new row to do `[OBS]`

| code | trigger | rc |
|---|---|---|
| E01 | `NF != 13` ("fields=12") — a pipe in a cell or a missing/extra column; other checks for that row skipped | 1 |
| E02 | id not `S[0-9]{3,}` (includes `S01`, `S0xx-pending`) | 1 |
| E03 | duplicate id | 1 |
| E04 | same normalized URL **and** byte-identical `scope`, earlier non-rejected row, `teaches` lacks `supersedes S[0-9]{3}` | 1 |
| E05 | kind outside the 10-value enum | 1 |
| E06 | tier not `A|B|C` | 1 |
| E07 | status not `queued|mined|rejected` | 1 |
| E08 | `opened` not ISO or later than `--today` | 1 |
| E09 | `recheck` not ISO / `NNd` / symbolic | 1 |
| E10 | `community` at tier A | 1 |
| E11 | `mined` row's used-by path absent under the lane root | 1 |
| E12 | row-shaped line (`^\| *S\d{3,} *\|`) outside `## Registry` | 1 |
| W01 | tier C + `mined` + used-by ≠ `—` | 0 |
| W02 | `rejected` + `teaches` shorter than 8 chars | 0 |
| W03 | `mined` + used-by `—` | 0 |
| W04 | same normalized URL under a different `scope` (warning only) | 0 |

### 3.3 Baseline measured on the current master `[OBS]`

```
validate: file W04 S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
          file W04 S042 duplicate url wayland.freedesktop.org/extras.html across scopes
          file W04 S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
          file ok  …/corpus/SOURCES.md      rc=0
census:   rows 71 · tier A 64 / B 1 / C 6 · mined 56 / queued 8 / rejected 7
```

`.ufo/waves/round-18/evidence/census-start.txt` (tracked) records the same three W04 lines
plus `ok` and `exit=0`, so the end-of-round diff should be zero new warnings and
`71 + N` rows.

### 3.4 Rule probes run on `/tmp` fixtures `[OBS]`

- Row appended at EOF (after `## Leads`) → `E12`, rc 1. Row inserted before `## Paths` →
  checked normally.
- Same URL + same scope, no `supersedes` → `E04`, rc 1. Adding `supersedes S100` to
  `teaches` → clean, rc 0.
- Same URL, **different** scope → `W04` only, rc 0.
- `supersedes S1000` → clean (the regex is unanchored, so it matches the `S100` prefix);
  `supersedes S0xx-pending` → `E04` (no match). Pending placeholders cannot license a
  duplicate row.
- Pipe inside `teaches` → `E01 … fields=12`, and E05/E10/E08 for that row were not
  reported (checks skipped).
- E11 fires only for `mined`; a `queued` row with a nonexistent used-by is clean.
- Uppercase `HTTPS://` → URL not extracted, no dedupe at all. `http://` → extracted and
  W04 fires, but `measure.py` requires lowercase `https://` for C2 upstream credit.
- `?recursive=1` is part of the key (same path with and without it never collides);
  trailing `/` and `#fragment` are stripped; host is lowercased, path case is kept.
- `E03` duplicate id and `E02` `S01` fire as documented.

## 4. Duplicate-URL (W04) risk for walker / elephant / omarchy / swaybg

### 4.1 Observed starting state `[OBS]`

- The registry has 52 distinct normalized URLs and **zero** walker, elephant, swaybg,
  omarchy, `learn.omacom.io`, `omarchytheme.com`, AUR-walker or Hypr "App-Launchers" URLs.
  The only omarchy mentions are host paths (S020, S059, S071).
- Fleet `shared` mode prints exactly two rows — `kubernetes.io/…/pods/probes` (kama, mori)
  and `godot-gdunit-labs.github.io/…` (game-dev 2d/3d) — neither involves mado or these
  families.
- Conclusion: no exact W04 collision exists to inherit. Every real risk is a near-duplicate
  the census cannot see.

### 4.2 Candidate URL families in this round's receipts (snapshot) `[OBS]`

- **walker**: `raw.githubusercontent.com/abenz1267/walker/v2.17.2/{README.md,
  resources/config.toml, Cargo.toml, src/config.rs, src/main.rs, src/theme/mod.rs,
  resources/themes/default/*.xml|style.css}`, `api.github.com/repos/abenz1267/walker/
  releases/tags/v2.17.2`, `…/git/trees/v2.17.2?recursive=1`.
- **elephant**: `raw.githubusercontent.com/abenz1267/elephant/v2.22.1/{README.md,
  cmd/elephant/elephant.go, pkg/common/{config,menucfg}.go, internal/providers/*/README.md}`,
  `api.github.com/repos/abenz1267/elephant/git/trees/v2.22.1?recursive=1`.
- **omarchy**: `raw.githubusercontent.com/basecamp/omarchy/v3.8.4/<path>` **and**
  `github.com/basecamp/omarchy/raw/v3.8.4/<path>` (same bytes, both fetched),
  `github.com/basecamp/omarchy/tree/v3.8.4/…` (HTML listings, 218-245 KB; `final_url`
  redirects to `github.com/omacom/omarchy/…`), `api.github.com/repos/basecamp/omarchy/
  git/trees/{v3.8.4,8fcc9d60…}?recursive=1`, `learn.omacom.io/2/…` manual pages.
- **swaybg**: `raw.githubusercontent.com/swaywm/swaybg/v1.2.2/{swaybg.1.scd, README.md,
  main.c, background-image.c, meson.build}`; `doc/swaybg.1.scd` is 404.
- **tier-C alternates**: `aur.archlinux.org/packages/{walker,walker-bin,elephant,
  omarchy-theme-marketplace-git}`, `omarchytheme.com` (+ `/themes/aetheria/`),
  `world.hey.com/dhh/…`, `www.ssp.sh/brain/walker-launcher`, a YouTube talk,
  `wiki.archlinux.org` (`Walker&action=raw` 404, `Category:Application_launchers` 200),
  `wiki.hypr.land/Useful-Utilities/App-Launchers`,
  `raw.githubusercontent.com/clarenceb/omarchy-wsl2/main/…` (unpinned `main`).

### 4.3 Risk classes and the rule that removes each

R1 **Alias spellings are invisible.** `github.com/<o>/<r>/raw/<tag>/<path>` and
`raw.githubusercontent.com/<o>/<r>/<tag>/<path>` are the same bytes under two normalized
URLs; `tree/` pages redirect basecamp → omacom (verified in the receipts' `final_url`).
The census compares the literal normalized string, so neither pair is a W04. Rule: one
spelling per file. Prefer `raw.githubusercontent.com` (S050/S053-S058 precedent, direct
digest); if a tree page is cited, cite it once, record the redirect in the gate, and never
also cite the omacom form.

R2 **The same file fetched by many seats.** Walker `README.md` appears in 7 receipt sets,
`resources/config.toml` in 5, omarchy `bin/omarchy-theme-set` in 5, `version` in 4. This is
one row per URL, not per seat. If two rows land for one URL: different scope text → a new
`W04`; identical scope text → `E04`, rc 1. L1 must merge seat proposals before landing.
Every multi-fetched URL observed (32 at the final recount) agrees on sha256/bytes
`[OBS]`, so there is no content-level reason to split them.

R3 **Revision and query variants.** Tag vs commit sha vs `?recursive=1` are three or four
distinct strings for one resource; pick one canonical form (tag + `?recursive=1` for tree
APIs; tag + commit in the `anchor`) and admit a second only as a `supersedes` row.

R4 **HTML listing vs bytes.** `tree/v3.8.4/themes` and `…/themes/matte-black` are HTML
pages (245 KB / 229 KB) with no stable line model. If used for a name census (row C of
`drafts/NoteTheme-rows.md`), the `source` must say it is a tree listing and the sha must be
of that HTML body; do not present it as a file anchor.

R5 **Brand alias across lanes.** tsukuroi's registry cites `github.com/omacom/omarchy/issues/…`;
the host checkout's origin is `https://github.com/basecamp/omarchy.git` (clone line in
`~/.local/share/omarchy/.git/logs/HEAD`, read as bytes). `shared` compares literal URLs, so
a basecamp/omacom pair is never reported — `shared` silence is not evidence of
non-overlap. Keep one spelling inside mado and note the redirect once in the gate.

R6 **Backfill receipts are not new sources.** `FetchBackfillR17` re-fetched 10 URLs that
exactly match existing rows (S056, S057, S058, S063, S064, S065, S066, S067, S068, S069).
Those receipts satisfy R17-V3 for old rows; creating rows for them would produce W04/E04.
No row.

R7 **Non-200 bodies are not creditable.** Five receipts are 404 `[OBS]`:
`github.com/swaywm/swaybg/tree/v1.2.2/doc` (195,690 B HTML error page),
`raw.githubusercontent.com/swaywm/swaybg/v1.2.2/doc/swaybg.1.scd` (14 B),
`raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/theme.name` (14 B),
`raw.githubusercontent.com/adrg/xdg/v0.5.3/files.go` (14 B), and
`wiki.archlinux.org/index.php?title=Walker&action=raw` (0 B). A rejected row may record the
absence, but the gate must mark it non-creditable and never use its sha as a row anchor
(two of the 14-byte bodies are indistinguishable by digest alone).

R8 **Scheme traps.** Uppercase `HTTPS://` makes the URL invisible to `url_of()` (no dedupe
at all); `http://` is deduped but fails `measure.py`'s `https://` test. Every `source` cell
uses lowercase `https://`.

R9 **Multi-URL source cells.** Only the first `https://` in `source` is the dedupe key, so
two rows that share a first URL but cite different later files still collide on scope.
Either split one row per URL or accept a single aggregated row per source (S059 precedent).

### 4.4 Baseline warnings to preserve

S030, S042 and S045 (all `W04`, all non-rejected duplicates with a distinct scope) are the
standing three. The round should land with the same three and no new one; a new `W04` is
visible in the census diff and must either be avoided by merging rows or be justified in
the gate with the distinct scope that makes it intentional.

## 5. Remaining unknowns `[UNK]`

- Which ids L1 assigns and which drafted rows are admitted (S072-S099 are reserved but the
  mapping is L1's).
- Whether `corpus/knowledge/walker-route-r18.md` exists at landing; it does not exist yet,
  while `theme-route-r18.md` exists untracked and still carries `S0xx-pending` tokens in
  its `source:` head.
- Whether the fetch receipts get committed with the landing commit. They are currently
  untracked, so C2's "committed raw fetch receipt" is unmet until L1's jj commit.
- Whether the `learn.omacom.io/2/…` manual pages become cited rows. The body itself reads
  "this is the legacy manual for Omarchy v3" (`fetch/SrcOmarchyManualThemes/manual.md:9`)
  and points Quattro to `omarchy.org/manual/`; a row must scope itself to the v3 manual.
- Whether tier-C alternates get rejected rows (S061/S062/S070 precedent) or no rows at all.
- Whether the 404 candidates (swaybg `doc/`, elephant's `adrg/xdg` path, Arch Wiki Walker)
  become rejected rows or are only named in the gate's exclusion paragraph.

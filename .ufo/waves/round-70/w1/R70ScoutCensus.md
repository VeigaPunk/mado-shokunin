# R70ScoutCensus — round-70 frontier reconnaissance (read-only)

seat: R70ScoutCensus · round: mado 70 (hyaku 15) · lane repo: `/home/vgpnk/Projects/shokunin/mado-shokunin`
base/HEAD at read time: `5144a6b5f43225d8021a469f4d24c19558026b9e` ("round-70: the two scored instruments and the repaired harness")
No file outside `w1/R70ScoutCensus/` and `w1/R70ScoutCensus.md` was written; no git/jj mutation; nothing adopted.

---

## 1. Round-start census

`--file` mode exists (printed by `scripts/sources-census.sh --help`, modes line):
`modes: census (default) | validate | overdue | shared | selftest`, option `--file PATH`.

```
$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
… 35 more W04 lines …
mado	W01	S277 tierC mined used-by=corpus/knowledge/request-socket-live-bound-r8.md, corpus/knowledge/request-limits-upstream-r31.md
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
rc=0
```
- summary line: `mado<TAB>ok<TAB>/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md`
- 37 findings, all warnings: 36 × W04, 1 × W01 (S277). No E-code. rc 0.
- output captured: `w1/R70ScoutCensus/census-validate-r70.txt` (38 lines).

```
$ bash scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin mado
mado	rows	375
mado	tier.A	361
mado	tier.B	7
mado	tier.C	7
mado	status.mined	354
mado	status.queued	10
mado	status.rejected	11
FLEET	rows	375 … FLEET	missing	0
rc=0
```
(output: `census-census-r70.txt`, 17 lines)

```
$ bash scripts/sources-census.sh validate --file /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
file	W04 … (same 37 warnings)
file	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
rc=0
```
(output: `census-validate-file-r70.txt`, 38 lines)

**Data-row count at HEAD: 375** (`grep -c '^| S' corpus/SOURCES.md` = 375; census `rows` = 375; no indented rows, so the 0–3-space parser and the column-zero pattern agree here).

## 2. Registry health (read-only; nothing fixed)

Sources of truth: `corpus/SOURCES.md` at `5144a6b…`, `git ls-tree -r --name-only HEAD` (33,687 paths) in scratch.

- **Rows whose `status` is not `mined` — 21** (10 queued, 11 rejected), exactly matching the census counts:

| id | status | source (truncated) |
|---|---|---|
| S006 | queued | Wayland debugging extras |
| S007 | queued | libinput helper tools |
| S008 | queued | The Wayland Protocol (DeVault) — high-level design chapter |
| S009 | queued | Wayland Architecture |
| S010 | queued | Wayland Explorer |
| S036 | queued | RemoteDesktop portal |
| S038 | queued | xdg-desktop-portal 1.21.0 |
| S039 | queued | xdg-desktop-portal 1.22.0 |
| S132 | queued | kitty built documentation (moving build) |
| S161 | queued | Lua query bindings |
| S011 | rejected | fleet-ledger MANIFEST.json — mado round verdicts |
| S012 | rejected | Hyprland Events Automation (Filip Mikina) |
| S030 | rejected | Hyprland Wiki Window Rules |
| S045 | rejected | Window Rules duplicate-admission correction |
| S061 | rejected | Arch Wiki Alacritty |
| S062 | rejected | Linux Junkies — Configure Alacritty for Daily Use |
| S070 | rejected | FlareXes — Hyprland getting-started (screen lock) |
| S084 | rejected | xdg crate BaseDirectories docs |
| S094 | rejected | omarchy v3.8.4 matte-black theme payload |
| S375 | rejected | uwsm v0.27.1 README environment export |
| S377 | rejected | uwsm v0.27.1 app unit source |

- **`used-by` paths missing at HEAD: 0.** Method: awk field 12 of every registry row, split on commas, exact match against the HEAD tree (`grep -qxF`). 354 rows carry a non-`—` used-by; 108 distinct non-`—` cells; no cell carries prose/parentheses, all are comma-separated repo-relative paths. Census E11 also reports nothing.
- **Highest S-id: `S438`.** Ids occupy 1..438 with 375 used and **63 gaps** (`S190–S195`, `S197–S200`, and other retired ids) — id arithmetic cannot infer row identity here.
- W01 (S277 tier-C mined with a non-`—` used-by) and 36 W04 same-URL-across-scopes are warnings only; rc stays 0.

## 3. shokuknow slice (`/home/vgpnk/Projects/shokuknow`, read-only)

`merge/mado/MERGE-REPORT.md`: **147 proposed rows accepted, 0 refused; 69 proposed knowledge entries**; lane registry held 192 rows when packaged.

- **Staged rows: 147**, ids contiguous `S203`–`S349` (147 = 349−203+1). Titles extracted to `w1/R70ScoutCensus/staged-titles.tsv` (id + title). They are rounds 1–16 of the corpus-expansion campaign: Hyprland IPC/dispatcher/waybar pages, hypridle, omarchy producers, host files, Chinese/Japanese literature, focus-grab surfaces, gkeep geometry, uwsm, etc.
- **Knowledge entries: 69 in the report table = 65 new files on disk under `merge/mado/knowledge/corpus/knowledge/` + 4 amendments to existing lane files** (`ipc-contract-r25.md`, `dispatcher-semantics-r25.md`, `waybar-module-text-route-r25.md`, `dispatcher-surface-and-request-grammar-r26.md`).
- **Do any staged entries cover the round-70 ground?** No. Exact counts over `merge/mado/knowledge/` + `SOURCES.append.md`:

```
GIT_NO_REPLACE_OBJECTS   files=0
guard dominance          files=0
kill-credit              files=0
returncode               files=0
subprocess               files=0
carrier                  files=0
no-replace-objects       files=0
mutant                   files=0
```
  No staged title mentions git, guard or carrier (the two `git` hits are `github`/`gitblog` in URLs). The package carries no kill-credit rule, no child-exit-status treatment, no Python AST carrier shapes and no guard dominance.

**Collision commands from the round prompt, run into `w1/R70ScoutCensus/assimilation/`:**

```
$ A=…/w1/R70ScoutCensus/assimilation; S=/home/vgpnk/Projects/shokuknow
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' mado-shokunin/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$S/merge/mado/SOURCES.append.md" | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
$ comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"
reg-ids=375 staged-ids=147 collisions=94
```
- registry ids: `S001 … S438`; staged ids: `S203 … S349`; **collision count 94**.
- collision list (94): `S203–S221`, `S253`, `S258`, `S277–S284`, `S285–S349` (full file: `assimilation/collisions`).
- Consequence (not acted on): the package cannot be appended as packaged; adoption would need a scratch renumber whose citations are re-pointed by document, never by arithmetic. This seat adopts nothing.

## 4. Quarantine slice

Command exactly as in the round prompt:

```
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
awk -F'|' -v l='mado' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R" > …/assimilation/quarantine-slice
slice-lines=13
```
**13 data rows.** Ids (order as printed; §2 ids carry the register-wide stray trailing backtick):

| class (register cell) | ids |
|---|---|
| `payload-absent` (6) | S189, S195, S201, S205, S224, S228 |
| never checked — could not fetch (2) | S199, S200 |
| never checked — gate named no locator (5) | S209, S222, S223, S225, S235 |

Register totals are stale as warned: header says 194 rows / 324 absent quotes; `## By lane` says `mado | 6` while the data rows are 13 (the summary counts only §1). Saved: `assimilation/quarantine-slice`.

**Already adjudicated in round 32** — `.ufo/waves/round-32/w1/reports/ExecQuarantineSlice.md` hand-checked this same 13-row slice (same awk derivation) on 2026-10-24: 5 present/adoptable (S189, S195, S205; S201 only on re-anchor to the paper's full LaTeX source; S228 only after quote-normalization), 1 absent-as-quoted (S224, a rotating timestamp — stale, not fabrication), 7 unverifiable (prose-class cells; 2 unfetchable remotes + 5 no-locator, though all five name concrete host locators). `SCORECARD.md:2795` carries it as "Revisit the 13-row mado quarantine slice only when cited source payloads can be re-opened".

**Read-only re-verification this round (independent of round 32):**
- S189 — quote is verbatim in the committed pin `.ufo/waves/round-32/fetch/S189.bin` (sha256 prefix `eea605dfe5ce09e1`):
  `auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));` → **present**.
- S228 — `lanes/mado/round5/fetch/cn-export-hyprland.html` reads `使用“模板:过时”标记的页面或章节` (U+201C/U+201D); the register cites straight `"` → **present under a curly/straight-quote fold**, not absent.
- S224 — `/home/vgpnk/.cache/ai-usage/status.json` exists; current `"updated_at": "2026-11-04T02:34:41Z"`, the cited `2026-10-23T22:52:44Z` is gone → **absent as quoted, inherently (rewritten cache)**; not fabrication.
- The other 10 rows were not re-opened (network fetch outside this seat; register class already says unchecked).

**Id-space hazard (important for the lane):** the register's ids do not index the current lane registry. Of the 13: only `S189` is present and on the same topic; `S201` (Waybar backend), `S205` (host idle-lock chain) and `S209` (host waybar config backups) are present but name **different** rows; `S195, S199, S200, S222, S223, S224, S225, S228, S235` have **no row at all** in `corpus/SOURCES.md`. Any verdict must be keyed to the cited URL/artifact, never to the id. Nothing adopted, nothing edited.

## 5. `considerthese/`

9 files (`2026-10-19` … `2026-10-28.md`); newest = `considerthese/2026-10-28.md` (operator-authored, never edited).

Six proposals, all "not acted on". **Still unimplemented and bearing on the lane's operability work: proposal 4** —

> **Keep a live-tool table.** There are now 8 live-state tools. One row each (question answered, last live run, verdict, who ran it) would show which ones João can run himself today. This is the half of the 2026-10-26 proposal 2 the lane has not built.

Confirmed unimplemented: `quality/tool-ledger.md` is a three-column instrument ledger (path, description, pointer) with no last-live-run column; `corpus/lessons/round-69.md:99` records proposal 4 as "named in the round report as an unmined proposal, not adopted".

**Bearing on this round's ground: none.** No proposal proposes a kill-credit rule or a carrier table, and a live-tool table governs `tools/` live-state instruments on a probed host — round 70 has no desktop probe and touches only `quality/counters/c1-r70-*` and `c2-r70-carriers.py`. Proposal 4 would be a separate operability item, not a widening of C1/C2. Proposal 5 ("Separate 'relayed' from 're-measured' in every number") is already honoured by this receipt (relayed vs re-verified is marked per item).

## 6. Frontier rows (`corpus/README.md` § Frontier, lines 125–142)

- **Row this round advances — the Round 69 bullet (line 127, `knowledge/gate-guard-dominance-r69.md`).** Reason: it is the only Frontier bullet whose subject is the round-70 surface. It records the sourced guard ground (row S438 + held S436/S437), the key-position rule and three dominance flows on the 20-file population (13 readers, 13 guarded), and — in its second half — the control harness's paired recipes "R1 crash ≠ kill, R2 unparseable ≠ kill, R3 the spawn guard itself". Round 70's C2 adds four carrier shapes (alias, attribute, splat, constant-key) and a 17-case control set to the same classifier; C1 replaces the in-process stand-ins with three real `bash` children and a parsed-failed-assertion credit rule. Both halves extend that bullet's sentence.
- **Row the round would leave stale unless refreshed — the same Round 69 bullet.** After round 70 it will still say "three dominance flows", "keeps the same 20-file population (13 readers, 13 guarded)" and describe the harness credit rule as the round-69 paired-recipe version; it must be refreshed to name the four added carriers, the 17-case control set and the real-child kill-credit rule, and its `## Not claimed` tail (no path-sensitivity beyond a literal-false branch; no alias/attribute flow beyond the four added shapes) should be updated rather than silently contradicted.
- No other Frontier row is touched: rounds 56, 57–63, 55, 47, 48, 50, 51, 46, 45, 40 keep their open surfaces (Windows desktop/DPI/DWM/CCD planes, Hyprland config/idle/keybind planes, terminal selection, XKB compile). Note that **no Frontier bullet covers the calibration/operability counter axes** — this round's axis work (C1/C2) advances no *domain* row; claiming otherwise would be a frontier overclaim.

**Frontier verdict (one paragraph).** Round 70 is instrument work on two held qualities, not a new domain surface: it should advance the single Round 69 Frontier bullet, whose guard-grammar sentence is the only one the round's C2 classifier extends (four more carrier shapes on a re-derived 20/13/13/0 population against a 17-case frozen control set) and whose second half records the very harness whose kill-credit rule C1 re-grounds on three real `bash` children. If the round lands, that bullet must be refreshed in the same commit or it goes stale on both halves (three flows → seven shapes; in-process paired recipes → parsed-failed-assertion credit proven on real children), and its "Still open" tail must be narrowed to the residual limits the declaration already names. No other Frontier row moves, and the round should say so plainly: no Windows/live-desktop row is re-measured (no probe is run), and the shokuknow package, the quarantine slice and `considerthese/` contribute nothing to this round's ground — there is no kill-credit, carrier or guard-dominance material in any of them, and the 13-row quarantine slice remains exactly as round 32 ruled it (5 present, 1 absent-as-quoted, 7 unverifiable), with the collision count of 94 blocking any package append until a document-keyed renumber is done in scratch.

## 7. Evidence files (all under `w1/R70ScoutCensus/`)

| file | content |
|---|---|
| `census-validate-r70.txt` | 38-line validate output (36 W04 + 1 W01 + summary) |
| `census-census-r70.txt` | 17-line census totals |
| `census-validate-file-r70.txt` | 38-line `--file` validate output |
| `staged-titles.tsv` | 147 staged ids + titles |
| `assimilation/reg-ids` | 375 lane registry ids |
| `assimilation/staged-ids` | 147 staged ids |
| `assimilation/collisions` | 94 colliding ids |
| `assimilation/quarantine-slice` | 13-row mado quarantine slice (as the awk prints it) |

Scratch `/fast/scratch/hyaku/mado-r70/R70ScoutCensus/` removed on exit; no tool installed or upgraded this seat (nothing needed).

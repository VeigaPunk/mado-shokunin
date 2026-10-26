# ExecIdGuard — Section 10 assimilation guards (read-only), round 45 w1

Seat: `ExecIdGuard`, leaf. Lane `mado-shokunin`. Base `0c89478a`, freeze `22a8dedd`.
Read-only throughout: nothing written outside this seat dir; no mutating git/jj anywhere; no pacman; no compositor call was
needed (no `hyprctl` invocation by this seat); no network fetch; no tool installed.

Receipts beside this file: `guard-receipt.txt` (live command output), `collisions.txt` (46 rows, classified), `gap-fills.txt`,
`quarantine.tsv`, `fit.tsv`, `quotes.txt`, `quote-verify.txt`.

## Verdicts (each one names what it attacks)

| # | Guard | Verdict | Attacks |
|---|---|---|---|
| 1 | id-collision | **BLOCK — 46 of 147 staged ids collide** with the lane registry; 55 once C2 lands | `merge/mado/SOURCES.append.md` vs `corpus/SOURCES.md` |
| 2 | indented-row proof | **guard holds only with the 0–3-space pattern**; the naive column-0 pattern misses an indented row (0 vs 1 hit on `  \| S311 \|`) | the pattern itself, on a scratch registry |
| 3 | quarantine slice | **12 staged ids / 13 defects** held out of adoption | `absent-defect-register.md` (mado rows only) |
| 4 | fit vs C2 | **none** — no staged theme touches the monitor-rule plane; C2 needs no assimilation | `MERGE-REPORT.md` + the staged knowledge bodies + C2's nine pins |
| 5 | package fit | **two defects beyond the ids** (stale renumber premise; 7 overwrite targets) | `MERGE-REPORT.md` adopt checklist steps 3–4 |

This **supports** `registration.md`'s "Assimilation: none planned (no `merge/mado/` theme on the monitor plane; w1 confirms)" —
confirmed structurally, not only lexically (table 4).

## 1. The id guard, run as specified

```
reg-ids   <- corpus/SOURCES.md           pattern ^[ ]{0,3}\|[ ]*S[0-9]{3}   -> 238 ids (238 unique, max S301)
staged-ids<- merge/mado/SOURCES.append.md same pattern                    -> 147 ids (147 unique, S203..S349 contiguous)
comm -12  -> 46 ids
```
`S203 S204 S205 S206 S207 S208 S209 S210 S211 S212 S213 S214 S215 S216 S217 S218 S219 S220 S221 S253 S258
S277 S278 S279 S280 S281 S282 S283 S284 S285 S286 S287 S288 S289 S290 S291 S292 S293 S294 S295 S296 S297
S298 S299 S300 S301` (46, `guard-receipt.txt`).

Inputs are stable: `corpus/SOURCES.md` is byte-identical at the freeze and at today's HEAD
(sha256 `f7209d62…c0c6`, 238 rows both), so the count reproduces at `22a8dedd`. Staged file sha256 `684efe8c…27c0`.

**Why it collides:** the renumbering that was meant to make the staging area registry-safe was computed when the lane held
192 rows and ended at S202 — `ID-REMAP.md:5` states "lane registry ends at S202", and `MERGE-REPORT.md:9` repeats
"lane registry currently holds **192** rows; first staged id is **S203**". The lane has since grown to 238 rows topping at
**S301**, so of the 99 staged ids below S302, 46 are now held rows (the collisions) and 53 land in holes the lane's max+1
allocator skipped over (gap-fills between S222 and S276, `gap-fills.txt`). The gap-fills do not collide today, but they are
unstable: they are ids the lane has already run past, so any registry rebuild that re-derives the id space lands on them.

**What the 46 are** (`collisions.txt`, classified by extracting the URL/path cell and comparing):

- **44 different-document** — same number, unrelated sources. Examples: lane `S206` = `~/.config/waybar/config.jsonc` vs
  staged `S206` = Hyprland `EventManager.cpp`; lane `S300` = GTK 4.24.1 `gdktoplevel-wayland.c` vs staged `S300` = a host
  idle-lock sweep.
- **2 same-document** — staged row duplicates a source the lane already holds *under the same id*: `S221`
  (`wiki.hypr.land/0.56.0/…/Using-hyprctl/`), `S253` (Hyprland `src/ipc/s1/Unix.cpp`).
- 1 near-miss worth naming: `S277` is the *same* chonkstep document under two GitHub orgs (`chriskearney` vs
  `iconidentify`) — counted as different-document by URL, same artefact in substance.

**Projection once C2 lands: 55.** Staged ids run to S349, so 48 of them sit at or above S302; **S302–S310 are exactly the ids
`registration.md` assigns to C2's new rows** (built by `build-pos.py`), and staged rows already hold those nine numbers
(staged S302 = Hyprland floating algorithm, S309 = host systemd journal, S310 = host gkeep rule file). C2 lands first this
round, so the collision set becomes 46 + 9 = 55 (`guard-receipt.txt`).

## 2. Guard proof on a scratch registry (indented row)

Scratch registry = copy of `corpus/SOURCES.md` + one row appended as `  | S311 | synthetic indented row for guard proof |`
(two leading spaces, line 493, `cat -A` shows `493:  | S311 | …$`).

| pattern | ids found | sees S311? |
|---|---|---|
| `^\| *S[0-9]{3}` (naive, column-0) | 238 | **0** |
| `^[ ]{0,3}\| *S[0-9]{3}` (0–3 space) | **239** | **1** |

`comm -12` of the 0–3-space scratch ids with a probe set `{S311, S999}` returns `S311` only — the indented row is caught and
an absent id is not invented. This is not a hypothetical: **staged round12 `S305` renumbers to `S311`**, which is the lane's
next free id after C2's S302–S310, so an indented `S311` row is exactly the shape an adoption would produce.

## 3. Quarantine slice (mado data rows only) — `quarantine.tsv`

Derived from `absent-defect-register.md`, whose preamble is explicit that its rows are candidates: "a CANDIDATE, not a
verdict" (:6). The register's mado section is **13 row-defects** (6 `payload-absent` + 7 never-checked). Its ids are a
**fourth id space** — pre-remap and round-scoped — so the slice is keyed by *source/gate*, never by number. Three checks
that the numeric route would misfire (verified against `SOURCES.append.md`):

| register id | what the register means | what `S<n>` means in the staged file |
|---|---|---|
| round3 S205 | ArchWiki interwiki map | staged S205 = Hyprland wiki *Dispatchers (Lua config API)* |
| round4 S224 | `~/.cache/ai-usage/status.json` | staged S224 = host Waybar config bytes |
| round5 S228 | `cn-export-hyprland.html` | staged S228 = omarchy idle-indicator producer (the html row is staged S245) |

Resolved slice — **12 distinct staged ids** (S222 carries two defects):

| staged | defect class | register id | hold reason |
|---|---|---|---|
| S206 | payload-absent | round1 S189 | `formatEvent` quote in no fetched byte of `EventManager.cpp` |
| S212 | payload-absent | round2 S195 | both zh-wiki quotes absent from the `.pkg.tar.zst` |
| S218 | payload-absent | round2 S201 | both arXiv-abstract sentences absent |
| S222 | payload-absent **and** no-locator | round3 S205 / round4 S222 | fabricated quote *and* a gate block with no line locator (`round3/SOURCES-PROPOSED.md:48`) |
| S241 | payload-absent | round4 S224 | `updated_at` quote absent from the cache file |
| S245 | payload-absent | round5 S228 | `模板:过时` absent from the local html |
| S216 | unreachable | round2 S199 | CSDN 521 to a plain client; quote never checked |
| S217 | unreachable | round2 S200 | CSDN 521; never checked |
| S209 | no-locator | round3 S209 | gate `SOURCES-PROPOSED.md:86` has URL + quotes, no locator |
| S223 | no-locator | round4 S223 | gate `round3/SOURCES-PROPOSED.md:54` |
| S225 | no-locator | round4 S225 | gate `round3/SOURCES-PROPOSED.md:68` |
| S235 | no-locator | round5 S235 | gate `round4/SOURCES-PROPOSED.md:53` |

Labels: 6 `payload-absent` are **hold-for-adjudication** (re-fetch and re-quote, or refuse); the 7 never-checked are **not
refutations** and must not be adopted as if verified. The likely cause of S222's payload-absent is JSON spacing — the gate
quotes `"prefix": "zh-hans"` with a space, the served siteinfo JSON is compact — but that is a hypothesis for the adjudicator,
not a verdict here (no fetch was made by this seat).

**Collateral (flagged, not quarantined):** the same sources carry other rows — `EventManager.cpp` → S266, the ai-usage cache
→ S240, arXiv 2604.18860 → S280 and S325. Their quotes are different spans, so they are not in the slice; an adjudicator who
re-opens the source should re-check them at no extra cost.

## 4. Staged-theme fit for this round's C2 — `fit.tsv`

Grep over `MERGE-REPORT.md` and the staged bodies for `monitor|output|mode|scale|display|screen|dpms|resolution|transform|mirror`
produced 15 hits; **all classify `none`** for C2 (`corpus/knowledge/hyprland-monitor-rule-r45.md`):

| staged theme (locator) | what it actually covers | fit |
|---|---|---|
| `two-literature-coverage-r25.md:48` | `after_sleep_cmd = hyprctl dispatch dpms on` — display **power** | none |
| `host-bar-and-idle-binding-r26.md:97` | DPMS explicitly declared unmeasured: "were not measured" | none — **refuse** any reading that C2 closes DPMS |
| `dispatcher-semantics-r25.md`, `dispatcher-surface-and-request-grammar-r26.md` | the `dpms` dispatcher as a description | none |
| `gkeep-size-rule-application-r10.md`, `window-size-read-in-chinese-r16.md`, `gkeep-rendered-geometry-*.md` | **window** size/geometry (client surface) | none |
| `host-producer-outputs-r29.md`, `host-producer-current-outputs-r30.md` | Waybar chip JSON "outputs" | none (word collision) |
| `two-literature-drift-r26.md:87`, `chinese-wiki-canonical-url-r28.md:34` | the `mirror.sjtu.edu.cn` host / 安全检查 | none (word collision) |
| `focus-grab-protocol-live-on-host-r14.md:11` | org name `quickshell-mirror` in a URL | none (word collision) |

Structural corroboration (not lexical): **zero staged rows cite any of C2's nine pins** —
`MonitorRuleManager`=0, `MonitorRule.hpp`=0, `Monitor.cpp`=0, `MonitorPositionController`=0, `Configuring/Monitors.md`=0
in `SOURCES.append.md`. One plane overlaps at the *file* level: `src/debug/HyprCtl.cpp` would carry four rows after a merge
(lane S158 + staged S264 + staged S272 + C2's S307) — the same W04 concentration `registration.md` already declares for
S307 = S158 at two rows; it becomes four, not a new document. No staged knowledge target begins with
`hyprland-monitor`, so C2's path collides with nothing.

## 5. Package fit beyond the ids

1. **The adopt checklist's step 3 must not run.** "Append `SOURCES.append.md` to `corpus/SOURCES.md`" over 46 (`55`)
   collisions produces a registry with duplicate ids; the lane's registry is currently clean (238 rows, 238 unique, 0 dups).
   A direct renumber to max+1 does **not** fix it: S203→S311 shifts the whole set onto ids its own members hold, and
   `renumber-staged.py:16` already warns that re-pointing must be "SIMULTANEOUSLY, so a" citation cannot walk a chain of
   remaps — the safe shape is a disjoint temporary space, then a final assignment.
2. **Step 4 would overwrite seven live entries.** The report labels 65 knowledge targets `new-file`; **7 of those basenames
   already exist** in `corpus/knowledge/`, and in every case the lane's copy is larger, i.e. the staged file is an earlier,
   shorter version (bytes lane/staged): event-delivery-limits-r26 5211/2677, hyprctl-flags-r28 3134/2280,
   request-limits-upstream-r31 2970/1980, request-socket-live-bound-r8 3702/3200, idle-lock-never-asked-r12 4344/3143,
   idle-lock-chain-armed-r14 3768/3503, idle-lock-offered-in-the-bar-r15 5806/4923. The rule the report applies to its four
   `amendment` targets ("append, do not replace"; all 4 targets exist, correct) was not applied to these 7.

## Limits (what this seat did not do)

- No quote was adjudicated: no fetch, no edit to `SOURCES.append.md`, no edit to the lane registry, no renumbering. The
  slice and the two package defects are findings for the L1, who is the only integrator.
- Fit is a term grep over the staged artefact; a monitor-plane theme phrased without those words would escape it. The pin
  census (0 of 9) and the absent path name are the structural backstop.
- The 46 is registry-at-freeze; it reproduces today because the registry has not moved, and will move when any later round
  appends rows.
- Register ids were resolved by locating each gate block and each cited source in the staged tree (computed line numbers in
  `quarantine.tsv`); five of the thirteen name no source at all, so their id resolution rests on the gate heading alone.

## Gate — evidence

```
$ sha256sum corpus/SOURCES.md merge/mado/SOURCES.append.md
f7209d62aa49e2d236d7b4b034cccd4e0dedda6ebc2d8801a0c573c58b2c0c0c  …/mado-shokunin/corpus/SOURCES.md
684efe8c23b8b64d789187dab61bfbf7c0dcef4f0428e447c94d7be4e73a27c0  …/merge/mado/SOURCES.append.md
$ comm -12 reg-ids.txt staged-ids.txt | wc -l        -> 46
$ grep -oE '^\| *S[0-9]{3}'      guard/SOURCES.scratch.md | sort -u | wc -l  -> 238
$ grep -oE '^[ ]{0,3}\| *S[0-9]{3}' guard/SOURCES.scratch.md | sort -u | wc -l -> 239
$ grep -n S311 guard/SOURCES.scratch.md | cat -A    -> 493:  | S311 | synthetic indented row for guard proof |$
$ python3 verify-quotes.py                          -> 8/8 located quotes verified (src + receipt, <=25 words)
```

Every quote above is ≤25 words, located by a computed `grep -n`/`sed -n` locator, and verified twice — against the source
file *and* against this seat's `quotes.txt` receipt (`quote-verify.txt`). Privacy (considerthese `2026-10-26.md` proposal 1):
the receipts contain registry ids, public URLs, local config/cache paths and file:line locators only — no window titles,
monitor serials/descriptions, process tables or directory listings.

Scratch used: `/fast/scratch/hyaku/mado-r45/ExecIdGuard` (deleted before finishing). Tools installed: none.

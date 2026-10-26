# ExecIdGuard — Section 10 assimilation guards (read-only), round 46 w1

Seat: `ExecIdGuard`, leaf. Lane `mado-shokunin`, base `b22ea56b`, freeze `8c5434c6` (HEAD at read `e0be61e4`).
Read-only: nothing written outside this seat dir; no mutating git/jj; no pacman; no compositor call; no network; no tool
installed. Guards were run into this seat dir, not into `.ufo/waves/round-46/assimilation/`.

Receipts beside this file: `guard-receipt.txt` (live command output), `reg-ids.txt` (252), `staged-ids.txt` (147),
`collisions.txt` (60), `collisions-classified.tsv`, `guard/` (indented-row fixtures and both collision outputs),
`quarantine-slice` (13 lines), `quarantine.tsv` (document-keyed resolution), `fit.tsv` (42 themes), `quotes.txt`,
`quote-verify.txt`.

## Verdicts (each names what it attacks)

| # | Guard | Verdict | Attacks / supports |
|---|---|---|---|
| 1 | id collision | **BLOCK — 60 of 147 staged ids collide** with the registry (58 different-document, 2 same-document) | `merge/mado/SOURCES.append.md` vs `corpus/SOURCES.md` |
| 2 | frontier block | **S316–S325 are already claimed by the staged set**, all 10 different documents; the round's own rows are free *today* (registry stops at S315) but the staged set must be renumbered before any adoption — projection **70** | this round's `registration.md:47` id block vs the staged package |
| 3 | indented-row proof | **guard holds only with the 0–3-space pattern**; the naive column-0 pattern is a false green (0 vs 1 on `  \| S316 \|`) | the extraction pattern itself, on two scratch registries |
| 4 | quarantine slice | **13 mado data rows** (6 `payload-absent`, 7 never-checked), byte-identical to round 44's artifact; resolved to **12 staged ids by document/gate, never by number** (register ids are a fourth id space) | `absent-defect-register.md`, mado rows only |
| 5 | slice blast radius | **9 staged entries rest on a quarantined row** (12 `source:` lines) — unadoptable until the row is hand-checked | `merge/mado/knowledge/**`, `merge/mado/amendments/**` |
| 6 | fit vs C2 | **none** — of 42 staged themes touching the five terms, 0 admit, 2 refuse, 40 none; C2's pins are cited by **0** staged rows except `src/debug/HyprCtl.cpp` (file-level only) | `MERGE-REPORT.md`, staged bodies, C2's ten pins |

This **supports** the registration's "Assimilation: none planned (… a `merge/mado/` theme on the input-device plane is
checked by a w1 seat; adopted only under §10 gates)" — confirmed structurally (pin census, not only words), and adds the
one thing round 45 could not see: the staged id space now reaches **into this round's own row block**.

## 1. The id guard, run as specified

```
reg-ids    <- corpus/SOURCES.md            ^ {0,3}\|[[:space:]]*S[0-9]{3,}   -> 252 ids, S001..S315
staged-ids <- merge/mado/SOURCES.append.md  same pattern                   -> 147 ids, S203..S349 contiguous
comm -12   -> 60 ids
```

Registry: 252 ids, 0 duplicates, **5 gap runs** `190-195, 197-200, 222-252, 254-257, 259-276` (63 missing numbers — the
holes the staged package's own ids occupy). Staged: 147 ids, 0 duplicates, contiguous S203..S349.

The 60: `S203-S221 S253 S258 S277-S315` (`collisions.txt`). Classified by comparing the source cell's URL/path token sets
(`collisions-classified.tsv`):

- **58 different-document** — same number, unrelated sources. Three checked by hand: lane `S206` =
  `~/.config/waybar/config.jsonc` (`corpus/SOURCES.md:208`) vs staged `S206` = Hyprland `EventManager.cpp`; lane `S209` =
  `/waves/round-35/fetch/S209.receipt.txt` (`:211`) vs staged `S209` = the Japanese ArchWiki article; lane `S310` =
  the Hyprland wiki Monitors page (`:259`) vs staged `S310` = a host journal sweep.
- **2 same-document, different row** — `S221` (lane `corpus/SOURCES.md:220`, staged `SOURCES.append.md:25`, both
  `wiki.hypr.land/0.56.0/Configuring/Advanced-and-Cool/Using-hyprctl/`) and `S253` (`:221` / `:57`, both
  `Hyprland@a1c2428/src/ipc/s1/Unix.cpp`). These are the two the report's own duplicate-URL table does not list; a merge
  would hold two rows per document under two numbers.

Registry state is stable: `corpus/SOURCES.md` is byte-identical at the freeze commit and today — sha256
`2a95e5743bdf7c17cc8541960fe07c80a7b3e866bdc423515c7d1d967d2013fc`, 252 rows, working tree clean (`git status
--porcelain` empty). The count therefore reproduces at `8c5434c6`.

**Why it collides:** the staged ids were cut when the lane held 192 rows (`MERGE-REPORT.md:9`: "lane registry currently
holds **192** rows; first staged id is **S203**"). The lane has since grown to 252 rows topping S315 — 60 of its rows carry ids
this staged set also claims, so the staged file is now 60/147 self-colliding.

### 1b. The frontier — the finding round 45 did not have

Staged **S316–S325 exist in the package** and are **absent from the registry**, i.e. they are exactly the ten ids
`registration.md:47` assigns to C2's new rows. Documents differ on all ten:

| id | staged document (`SOURCES.append.md` line) | round-46 document (`l1-draft/build-pos.py` line) |
|---|---|---|
| S316 | host idle-lock never-asked measurement (`:120`) | `managers/input/InputManager.cpp` (`:31`) |
| S317 | `src/managers/SeatManager.cpp` keyboard dispatch (`:121`) | `config/legacy/ConfigManager.cpp` (`:35`) |
| S318 | `src/desktop/view/Window.cpp` size-ack (`:122`) | `config/values/ConfigValues.cpp` (`:39`) |
| S319 | `Window.cpp` map-time size record (`:123`) | `devices/IKeyboard.cpp` (`:43`) |
| S320 | host journal map-log sweep (`:124`) | `debug/HyprCtl.cpp` devices request (`:47`) |
| S321 | Chinese wiki wikitext (`:125`) | `helpers/MiscFunctions.cpp` (`:51`) |
| S322 | Chinese wiki search-index sweep (`:126`) | `devices/VirtualKeyboard.cpp` (`:55`) |
| S323 | Japanese text-expander article (`:127`) | `protocols/VirtualKeyboard.cpp` (`:59`) |
| S324 | DFRWS espionage paper (`:128`) | `hyprlang v0.6.8 src/config.cpp` (`:63`) |
| S325 | arXiv TOCTOU paper (`:129`) | wiki `Configuring/Keywords.md` (`:65`) |

Consequence: today's collision count is 60 and this round's rows are safe (no registry row at S316+), but **the moment C2
lands the count becomes 70**, and any later adoption of the package must renumber S316–S349 by document (53 further
staged-only ids sit in registry holes S222–S252/S254–S257/S259–S276; 24 sit above S325). This seat proposes nothing about
the renumbering — that is the L1's call — only that no staged row above S315 may be appended under its staged number.

## 2. Guard proof — an indented row must be caught

### A. Self-contained fixtures (`guard/`, reproducible from this seat dir)

`guard/registry-fixture.md` carries `  | S316 | …` (two leading spaces, line 7, `cat -A` shows
`7:  | S316 | …$`); `guard/staged-fixture.md` claims S316 at column 0.

| extractor | ids found | sees S316 | collision file |
|---|---|---|---|
| `^ {0,3}\|[[:space:]]*S[0-9]{3,}` | S001 S003 **S316** | **1** | `guard/collisions-tolerant.txt` = `S316` (non-empty) |
| `^\|[[:space:]]*S[0-9]{3,}` | S001 S003 | **0** | `guard/collisions-col0.txt` = empty |

### B. The real registry, plus one indented row (scratch instantiation of the same test)

The 212 KB registry copied to scratch and one `  | S316 | synthetic indented row …` appended:

```
0-3 space pattern -> 253 ids (252 + S316)   grep -c '^ {0,3}\|[[:space:]]*S316' = 1
column-0 pattern  -> 252 ids                  grep -c '^\|[[:space:]]*S316'      = 0
```

The naive pattern would have reported a **false green** for the exact row this round must not lose. Guard proven able to
fail; the 60 above was produced with the 0–3-space pattern.

## 3. Quarantine slice — mado data rows only

Derived with the prompt's own awk (data rows only, `$2 ~ "`mado`" && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/`):
**13 rows** = 6 `payload-absent` (register `:141-146`) + 7 never-checked (`:349-355`). `quarantine-slice` sha256
`d9ea803d2433942dac094a14e9223be086ad460502163df7faf6e2509d9bb45d`, `diff` against
`.ufo/waves/round-44/assimilation/quarantine-slice` **empty** (and against round-32's, also empty) — the slice has not
moved since round 32. Its header and `## By lane` totals are stale (the prompt says so, and round 44 re-derived them);
its rows are candidates in its own words: "A quote the checker could not match is a CANDIDATE, not a verdict."
(`absent-defect-register.md:6`).

Register ids: `S189 S195 S201 S205 S224 S228` + `S199 S200 S209 S222 S223 S225 S235`.

**The register's ids are a fourth id space** — round-scoped and pre-remap — so the slice is keyed by document/gate
(`quarantine.tsv`). Three checks that the numeric route would misfire:

| register id | register's document | what `S<n>` means in the staged file / in the lane registry |
|---|---|---|
| round3 `S205` | ArchWiki siteinfo interwikimap | staged `S205` = wiki *Dispatchers (Lua config API)*; registry `S205` (`corpus/SOURCES.md:207`) = another document |
| round4 `S224` | `~/.cache/ai-usage/status.json` | staged `S224` = host Waybar config bytes |
| round5 `S228` | `lanes/mado/round5/fetch/cn-export-hyprland.html` | staged `S228` = omarchy idle-indicator producer (the html row is staged `S245`) |

Resolved slice — **12 staged ids, 13 defects** (`S222` carries two):

| staged | class | register id | document (staged line) | lane at that staged id |
|---|---|---|---|---|
| S206 | payload-absent | round1 S189 | `EventManager.cpp` (`:10`) | line 208, other document |
| S212 | payload-absent | round2 S195 | zh Arch wiki package (`:16`) | line 214, other document |
| S218 | payload-absent | round2 S201 | arXiv 2604.18860 (`:22`) | line 224, other document |
| S222 | payload-absent **and** no-locator | round3 S205 / round4 S222 | ArchWiki siteinfo (`:26`) | lane hole |
| S241 | payload-absent | round4 S224 | `~/.cache/ai-usage/status.json` (`:45`) | lane hole |
| S245 | payload-absent | round5 S228 | `cn-export-hyprland.html` (`:49`) | lane hole |
| S216 | unreachable | round2 S199 | CSDN 2301_76324845 (`:20`) | line 218, other document |
| S217 | unreachable | round2 S200 | CSDN lxyoucan (`:21`) | line 219, other document |
| S209 | no-locator | round3 S209 | JA ArchWiki Hyprland (`:13`) | line 211, other document |
| S223 | no-locator | round4 S223 | hypridle unit template (`:27`) | lane hole |
| S225 | no-locator | round4 S225 | host installed hypridle unit (`:29`) | lane hole |
| S235 | no-locator | round5 S235 | omarchy-refresh-hypridle (`:39`) | lane hole |

The four gate-only rows still deserve the register's label — each gate block names URL and quotes but **no line locator**
(computed: `lanes/mado/SOURCES-PROPOSED.md:86` for S209; `lanes/mado/round3/SOURCES-PROPOSED.md:48,54,68` for S222/S223/S225;
`lanes/mado/round4/SOURCES-PROPOSED.md:53` for S235). None is a refutation: `unreachable` and no-locator are unchecked,
not absent. **No slice row is on the input-device plane** — they are the event socket, two wiki packages, an arXiv focus
paper, the siteinfo API, a cache file, a local HTML copy, two CSDN posts and four hypridle units.

**Blast radius (new this round):** 9 staged entries rest on a quarantined row, so they cannot be adopted while the row is
held — `two-literature-coverage-r25.md:8` (S209), `two-literature-drift-r26.md:8,10,11` (S212/S216/S217),
`compositor-focus-manipulation-literature-r26.md:7` (S218), `idle-lock-runtime-state-r28.md:9,10` (S223/S225),
`chinese-wiki-canonical-url-r28.md:8` (S222), `idle-toggle-and-daemon-lifecycle-r29.md:9` (S235),
`host-producer-outputs-r29.md:12` (S241), `chinese-article-revision-r30.md:10` (S245),
`amendments/corpus/knowledge/ipc-contract-r25.md:14` (S206). Round 45's "no slice row is cited by the residue files" holds
only for the six residue files it named; the package as a whole cites every slice id.

## 4. Package fit for this round's C2 — `fit.tsv`

Terms `keyboard|input|xkb|layout|libinput`, case-insensitive, over `MERGE-REPORT.md` (5 entries) and every staged body
(16 files) plus the staged rows (26). 42 themes, **0 admit, 2 refuse, 40 none** (16 staged entries + 26 staged rows).

| staged theme (locator) | what it actually covers | fit |
|---|---|---|
| `focus-grab-*` cluster (8 entries; rows S229 S273 S274 S288 S294 S295 S296 S306 S313 S331 S332) | who receives input **events** under a grab: focus selection, key delivery, whitelist, mouse target | none — C2's plane is config → `hyprctl devices -j` names/factors, not event routing |
| `wayland-input-security-literature-r8.md:2`, rows S278 S279 S280 S324 S325 | the Wayland input-security model, compositor-mediated input as an attack surface | none — security literature |
| `japanese-input-observation-methods-r14.md` (S333/S334) | instrument-level observers: `wev` (which key, on which surface), `evtest` (`/dev/input/event*`) | **refuse** — the closest hit; names no XKB name, no config key, no `devices -j` field, so it cannot source C2 (a reader could mistake it for the plane) |
| `upstream-input-holds-and-the-lock-screen-r16.md`, S344, S349 | capture holds and lock-screen binds | none — holds, not configuration |
| `japanese-wayland-compositor-account-r16.md:19`, `chinese-hyprland-window-rules-r16.md:24`, S211 S347 S348 | window rules and keyboard focus **dispatch**; S211's "layout" is a config-file layout | none |
| `gkeep-size-to-real-size-r11.md:11-13`, `two-literature-coverage-r25.md:38`, `hyprctl-flags-r28.md:22`, `chinese-wiki-canonical-url-r28.md:28` | `src/layout/…` paths, a "bar layout", a "layout or rule changes" flag note, a wiki page layout | none — four word collisions with keyboard *layout* |
| S317 (`SeatManager.cpp`), S323 (JA text expander), S324/S325 | dispatch path; input-injection default; papers | none / refuse — S317 is the keyboard *routing* chain, one layer above the device plane |

**Structural backstop (not lexical): pin census over the staged package** (`guard-receipt.txt`). Rows citing
`managers/input/InputManager.cpp`, `config/legacy/ConfigManager.cpp`, `config/values/ConfigValues.cpp`,
`devices/IKeyboard.cpp`, `helpers/MiscFunctions.cpp`, `devices/VirtualKeyboard.cpp`, `protocols/VirtualKeyboard.cpp`,
`hyprlang/v0.6.8/src/config.cpp`, `Configuring/Keywords.md`: **0 each**. Only `src/debug/HyprCtl.cpp` is shared — staged
`S264`/`S272` (request-socket loops) against C2's pin S320 (the devices request) — and the file already carries lane
`S158` (`corpus/SOURCES.md:170`) and `S307` (`:256`), so a merge would put **five** rows on one file (a W04 census
concentration, not a new document, and not an id question). Similarly `config/legacy/ConfigManager.cpp` would hold three
rows after this round: held `S162` (`:174`), `S303` (`:252`) and C2's S317 — the repeat the registration already declares.

No staged knowledge target begins with `hyprland-input`, and no staged entry is named for this plane, so C2's path
`corpus/knowledge/hyprland-input-devices-r46.md` collides with nothing in the package.

## Limits (what this seat did not do)

- No adoption, no renumber, no edit to `SOURCES.append.md`, the registry, the register or any campaign file. The 60/70 and
  the slice are findings for the L1, the only integrator.
- Collision classes rest on URL/path token comparison of the source cell; a staged row whose document is reachable only
  through prose would be classed different-document by absence of a shared token (2 of 60 came out same-document).
- Fit is a term grep plus the pin census; an input-device theme phrased without any of the five terms and without a pin
  file would escape both.
- The slice resolution for the four gate-only rows rests on matching the campaign gate heading (computed locators in
  `quarantine.tsv`); the register supplies no source for them.
- The 60 is registry-at-freeze; it reproduces today only because no round has appended since `8c5434c6`.

## Gate — evidence

```
$ sha256sum corpus/SOURCES.md                      -> 2a95e574…013fc   (252 rows)
$ git show 8c5434c6:corpus/SOURCES.md | sha256sum  -> 2a95e574…013fc   (identical at the freeze)
$ sha256sum merge/mado/SOURCES.append.md           -> 684efe8c…27c0   (147 rows)
$ comm -12 reg-ids.txt staged-ids.txt | wc -l      -> 60
$ grep -cE '^ {0,3}\|[[:space:]]*S316' REG.scratch.md -> 1     (0-3-space pattern)
$ grep -cE '^\|[[:space:]]*S316'      REG.scratch.md -> 0     (naive column-0: false green)
$ awk -F'|' -v l=mado … absent-defect-register.md | wc -l -> 13
$ sha256sum quarantine-slice                       -> d9ea803d…bb45d   (== round-44 artifact)
$ grep -rc -E 'source: (S206|…|S245)\b' knowledge amendments -> 12 lines / 9 files
$ pin census: 9 of C2's 10 pins cited by 0 staged rows; src/debug/HyprCtl.cpp by 2 rows + 7 mentions
$ quote-verify (in-session python: each quote grepped at its cited line) -> verified 3/3
```

Every quote above is ≤ 25 words, located by a computed `grep -n`, and verified against its source and against
`quotes.txt` (`quote-verify.txt`). Privacy: receipts hold registry ids, public URLs, local config/cache paths and
file:line locators only — no window titles, monitor serials/descriptions, process tables or directory listings.

Scratch: `/fast/scratch/hyaku/mado-r46/ExecIdGuard` (deleted before yield). Tools installed: none.

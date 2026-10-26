# Quarantine verdicts — mado, round 43 (2026-10-26), gkeep-geometry theme

Seat `ExecQuarantineSlice` (assimilation item 10). The register is read-only here and was never edited:
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
(375 lines, sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`, re-hashed
2026-10-26 — byte-identical to the copy round 41 adjudicated). Access date for every fetch below:
**2026-10-26**.

## 1. Slice derivation

```sh
A=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/assimilation
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
awk -F'|' -v l='mado' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ \
  {print $4, $5}' "$R" > "$A/quarantine-slice"
```

- **Data-row count: 13.** Output sha256 `d9ea803d2433942dac094a14e9223be086ad460502163df7faf6e2509d9bb45d`
  (a byte copy at `w1/ExecQuarantineSlice/quarantine-slice.raw`). Every line carries an S-id.
- The register's `## By lane` summary says `mado | 6` (its line 248) because it counts only the
  `payload-absent` family; the slice is derivable from both tables, hence 13.
- The second table is malformed: its id cell lacks the closing backtick, so 7 of the 13 slice ids come
  out as `` S199` ``, `` S209` `` … in the raw awk output. Reported, not silently repaired; the ids are
  unchanged.
- Families: `payload-absent` 6 (S189, S195, S201, S205, S224, S228); never-checked prose 7
  (S199, S200 "could not be fetched"; S209, S222, S223, S225, S235 "named no locator").

## 2. The theme set, pinned (11 files, read-only)

`/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/` (sha256 prefix, first 16 hex):

| file | sha256 | file | sha256 |
|---|---|---|---|
| `gkeep-client-size-request-r12.md` | `2a3bb9f4b1522df1` | `gkeep-rendered-geometry-chain-r9.md` | `3e0cf8721f0c369d` |
| `gkeep-element-rules-r30.md` | `ff9c5ad152f4d2bd` | `gkeep-rendered-geometry-record-r13.md` | `4930768a08bfe7d3` |
| `gkeep-geometry-never-recorded-r15.md` | `aea823bc0be16299` | `gkeep-rendered-geometry-record-r14.md` | `a23782e32da729f0` |
| `gkeep-geometry-unobservable-r8.md` | `225f234ee6d4a4f6` | `gkeep-size-rule-application-r10.md` | `be044aaf61a695fe` |
| `gkeep-observation-route-r11.md` | `8813f8c5ef4be8c1` | `gkeep-size-to-real-size-r11.md` | `1dfb0b0982da6f91` |
| `glyph-and-geometry-r31.md` | `9edc926dcc7da4c5` | | |

## 3. Joins, three ways (script: `w1/ExecQuarantineSlice/join-evidence.py`, output `join-evidence.txt`)

| join | result |
|---|---|
| **id-level**: 13 slice ids ∩ ids written inside the 11 files | **0 hits** — the files name 28 distinct ids: S216, S219, S251, S255, S256, S275, S281, S284, S285, S286, S287, S292, S293, S297, S298, S299, S302, S303, S304, S305, S310, S311, S312, S318, S319, S320, S326, S339 (26 `source:` lines + 3 inline: S216, S219, S281) |
| **source-level**: slice rows' cited source vs the theme's cited documents | **1 overlap** — `https://blog.csdn.net/2301_76324845/article/details/149787804`: register row **S199** and staged row **S216**, cited inline at `glyph-and-geometry-r31.md:28` |
| **register-wide**: does any register row (all lanes) cite any of the theme's 28 sources? | **exactly 1** — the same CSDN URL |

Two id-space facts make a numeric cross-join unsound, and the L1 should not read one:

1. The register's ids sit **+17** from the packaged ids for all eight source-bearing slice rows
   (S189→S206 EventManager.cpp, S195→S212 zh wiki package, S201→S218 arXiv 2604.18860,
   S205→S222 interwiki map, S224→S241 status.json, S228→S245 cn-export, S199→S216 and S200→S217
   both CSDN); the five gate-block rows have no source to map. The register's ids are its own quoting ids, not the registry's.
2. Seven of the 28 cited ids also name a **current lane registry row with a different subject**:
   S216 `Compositor.cpp`, S219 mado-options tool, S281 notification-silencing indicator,
   S284 `FocusGrab.cpp`, S285 quickshell `grab.cpp`, S286 xdph `PortalManager.cpp`, S287 issue #565.
   Joining the theme by id onto the lane registry would attach gkeep geometry to focus control.

## 4. The one slice row the theme touches — verdict

| id | class | URL | quote / absence evidence | verdict |
|---|---|---|---|---|
| **S199** | prose: "the cited source could not be fetched, so no quote was checked" (register:349) | `https://blog.csdn.net/2301_76324845/article/details/149787804` | register carries **no quote** for this row, so there is nothing to locate; direct fetch re-run 2026-10-26 → **HTTP 521**, 2 263 B JS-challenge stub (`w1/ExecQuarantineSlice/csdn-2301_76324845.body`, sha256 `93cf2a5a…`); reader proxy `https://r.jina.ai/<url>` → **HTTP 200**, 71 957 B (`proxy-149787804.txt`, sha256 `81a5e78a…`), payload identity confirmed without relying on the title: the page now carries a different title string, but its body still holds the exact rule the staged row quotes (`windowrule = opacity 0.80 $& 0.80 $& 1,class:^([Cc]ode)$`, proxy line 160) | **`unverifiable`** — `unreachable` by direct fetch, and *not* the fabrication class; no adopt, no refuse. The row can be re-opened (proxy route works; round 41's captured body `round-41/w1/ExecQuarantineSlice/sources/csdn-149787804-via-r.jina.ai.txt`, 72 130 B, sha256 `d9b9ebe8…`, is still in the lane) but the register never took a quote, so there is nothing to match |

**Totals: 1 cited slice row → `unverifiable` 1, adopt 0, refuse 0.**

**Citation finding (attacks `glyph-and-geometry-r31.md:28`).** The sentence's bases are "the codepoint,
the codemap entry and the producer's branch structure (round 5's row S216)". S216 is the CSDN
window-rule/opacity blog — in the packaged append (`SOURCES.append.md:20`, itself recording that
"the body was retrieved through a reader proxy"), in the round-2 proposal, and in the round-5 proposal
alike. The producer row is **S248** (`round5/SOURCES-PROPOSED.md:22`, `SOURCES.append.md:52`); the row
the file's second inline id names, `:36` "(round 5's row S219)", is omarchy's `hypridle.conf`, while the
host rule file is **S251** (`round5/SOURCES-PROPOSED.md:25`). No numbering on disk makes S216 the
producer or S219 the rule. So the theme's *only* contact with the quarantine slice is a stale inline
id for a claim that this row could not support even if reachable — a re-grounding defect, not a
fabricated quotation.

## 5. The two files named "in particular"

| file | cited ids (all `source:` lines) | documents | quarantined? |
|---|---|---|---|
| `gkeep-rendered-geometry-chain-r9.md` | S284, S285, S286, S287, S292, S293 (lines 8-13; no inline-only id) | Window.cpp, gkeep `ui.py`, GTK4 `set_default_size`, hypr.land 0.56.0 Window-Rules, round-9 geometry-chain + log-scan artifacts | **no** |
| `gkeep-size-to-real-size-r11.md` | S302, S303, S304, S305, S310 (lines 11-15) + inline **S281** (line 63) | DefaultFloatingAlgorithm.cpp, Target.cpp, WindowTarget.cpp, GeometricMovableAnimated.cpp, round-11 host rule+path artifact | **no** |

- Neither file's cited document appears in the register under any id (the register-wide join above is
  the evidence). No adopt/refuse is owed for them.
- r11's inline S281 ("the same variable the compositor reports (round 10's S281)") is another stale id:
  packaged S281 is the wiki.archlinuxcn.org `api.php` fetch of the Hyprland article, and round 10 has no
  row S281 in either numbering (its proposals are S295-S299 packaged). The claim's base is a compositor-side
  row (round 10's S298 `Window.cpp` / round-43 pin S296 `HyprCtl.cpp`), not a Chinese wiki fetch.
- Their host-side rows (S292/S293/S310 = `lanes/mado/round9|11/fetch/…`) point at **campaign** paths, not
  lane paths: both artifacts exist in the campaign checkout (`/home/vgpnk/Projects/shokuknow/lanes/mado/
  round9/fetch/gkeep-geometry-chain.txt`, `…/round11/fetch/host-gkeep-rule-and-path.txt`) and **none**
  exists in the lane (`find mado-shokunin -name …` → 0 hits). Opening those rows needs the campaign path
  or a refusal — the id-guard's finding, independently reproduced here.

## 6. The rest of the slice — no verdict from this seat

Twelve rows are named by no theme citation at all: the id-level join is empty and the source-level join
finds only S199 (§4). Their state is unchanged; a reader acts on them only in another round's theme.

| id | class | cited source | verdict here |
|---|---|---|---|
| S189 | `payload-absent` | Hyprland `EventManager.cpp` @ efb5099 (same commit the theme pins) | no action — not cited by the theme; the file is outside the geometry chain |
| S195 | `payload-absent` | `arch-wiki-docs-zh-cn` package | no action — not cited; Chinese documentation channel, outside the province ("documentation written in a localized channel", PROVINCE.md:76) |
| S201 | `payload-absent` | arXiv 2604.18860 | no action — not cited by the gkeep theme (the focus theme's row; adjudicated in round 41) |
| S205 | `payload-absent` | ArchWiki interwiki map | no action — not cited; localization mechanics, outside the province |
| S224 | `payload-absent` | `~/.cache/ai-usage/status.json` | no action — not cited |
| S228 | `payload-absent` | `lanes/mado/round5/fetch/cn-export-hyprland.html` | no action — not cited |
| S199 | prose, could not be fetched | CSDN 2301_76324845 | **`unverifiable`** (§4) |
| S200 | prose, could not be fetched | CSDN lxyoucan | `unverifiable` by the same rule (direct re-fetch 2026-10-26 → HTTP 521, 2 167 B stub, `csdn-lxyoucan.body`, sha256 `413000dd…`); not cited by the theme |
| S209, S222, S223, S225, S235 | prose, gate block named no locator | the cell is a heading (`## Gate — S…`), not a source | `unverifiable` — there was never a locator, so there is no quote to check; this is not the fabrication class and nothing can be adopted |

## 7. Quotes used, located (each ≤ 25 words), and how they are checked

| quote | located at | words |
|---|---|---|
| "the cited source could not be fetched, so no quote was checked" | register:349 | 12 |
| "the gate block named no locator, so no quote was checked" | register:351 | 11 |
| "cited source, companion URLs and local artifacts were all checked; the quote is in none of them" | register:141 | 16 |
| "The direct URL answers HTTP 521 to a plain client; the body was retrieved through a reader proxy" | `SOURCES.append.md:20` | 19 |
| "the codemap entry and the producer's branch structure (round 5's row S216)" | `glyph-and-geometry-r31.md:28` | 12 |
| "The host's rule imposes the same size (round 5's row S219)" | `glyph-and-geometry-r31.md:36` | 12 |
| "reports (round 10's S281)" | `gkeep-size-to-real-size-r11.md:63` (sentence opens on :62) | 4 |
| "omarchy weather-icon helper" | `round5/SOURCES-PROPOSED.md:22` and `SOURCES.append.md:52` | 4 |
| "host gkeep window rules" | `round5/SOURCES-PROPOSED.md:25` | 4 |
| "documentation written in a localized channel" | `PROVINCE.md:76` | 6 |

`w1/ExecQuarantineSlice/verify-quotes.py` re-greps every row above against the file and line, and
asserts the structural facts (slice length and sha256, register length and sha256, 0 id-join hits,
1 source-join hit, the +17 offsets, 7 lane-registry collisions, the two saved 521 stubs, the 200 proxy
body). Run 2026-10-26: all assertions pass.

## 8. Reproduction

```sh
W=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/w1/ExecQuarantineSlice
python3 $W/join-evidence.py | diff - $W/join-evidence.txt   # joins, empty on success
python3 $W/verify-quotes.py                                  # quotes + structural assertions
```

Evidence kept in the seat directory only (no scratch path is cited): `quarantine-slice.raw`,
`join-evidence.py`, `join-evidence.txt`, `verify-quotes.py`, `csdn-2301_76324845.body`,
`csdn-lxyoucan.body`, `proxy-149787804.txt`.

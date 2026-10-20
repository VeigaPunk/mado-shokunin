# ReopenS062 — S062 re-open (Linux Junkies, Configure Alacritty)

Seat: MadoR17.ReopenS062 (scout, wave 2 FALSIFY). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`, lane HEAD `988b858bd6049bc709807534fd725c05264f7e60`.
Question: does S062 (`corpus/SOURCES.md:74`, `rejected`) and its gate line
(`corpus/lessons/round-17.md:49`) hold on freshly fetched bytes, and does the
stated rejection reason hold?

**One-line result: the rejection stands.** URL, raw digest, verbatim quote, word
count, tier/status/verdict and both legs of the stated reason verify at byte
level. One documentation defect survives (D1, anchor numbering); it does not
touch the verdict and needs no status change.

## Artifacts fetched today (curl, file bytes only)

| what | URL | HTTP | bytes | sha256 |
|---|---|---|---|---|
| page under test | `https://linuxjunkies.org/guides/configure-alacritty` | 200 (2026-10-20 14:53:21 GMT) | 90051 | `08608a0bafb9bb7b4cea2a7970dbc2f926946976c7f9eb23a1d30249bec2c653` |
| ground truth 1 | `raw.githubusercontent.com/alacritty/alacritty/v0.13.0/CHANGELOG.md` | 200 | 55324 | `b3c8181efe279207e61f53b8b08dfe366f505cbcd3f1ceec8c0e7e9763344630` |
| ground truth 2 | `raw.githubusercontent.com/alacritty/alacritty/v0.12.0/CHANGELOG.md` | 200 | 50482 | `ee5821715fd02b1754cfac067df346546081269676f5ae30a1ffd2e45f3a4236` |
| control | `raw.githubusercontent.com/alacritty/alacritty/v0.12.0/alacritty.yml` | 200 | 31779 | `3110fbf1d8cbeaaa388670dc6a86493a052903610bbdaa4d17150da833029e2b` |
| control (absent) | `raw.githubusercontent.com/alacritty/alacritty/v0.12.0/alacritty.toml` | 404 | 14 | — |
| control | `raw.githubusercontent.com/alacritty/alacritty/v0.13.0/extra/man/alacritty.5.scd` | 200 | 27226 | `223de615a62f063f919ac58df61afc894468715eb25a3917b09a95534ebcca32` |

Raw page digest equals the row's `08608a0b…bec2c653` exactly (full digest recorded
above). The page's own date stamp is present in the bytes: `June 7, 2026` and
`2026-06-07T00:47:45.371Z` — the row's scope "updated 2026-06-07" is grounded.

## Row verification — `corpus/SOURCES.md:74`

| column | value in row | check |
|---|---|---|
| id | S062 | unique; `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → `mado ok` |
| source | Linux Junkies — Configure Alacritty for Daily Use — URL | title and URL match fetched `<title>` / canonical |
| kind | community | allowed enum |
| tier | C | allowed; contract says `community` is never A — correct |
| scope | third-party alacritty.toml setup guide (updated 2026-06-07) | page date bytes confirm |
| anchor | `raw sha256 08608a0b…bec2c653; :51 and :247 place TOML at 0.12` | digest exact; anchors — see D1 |
| teaches | `REJECTED: … ; flip: …` | rejected-row shape present (`REJECTED:` + `flip:`) |
| status | rejected | allowed enum; matches verdict |
| opened | 2026-10-20 | round date |
| recheck | 180d | allowed cadence |
| used-by | `—` | no corpus note cites it (see below) |

Shape: `awk -F'|'` gives NF=13 (11 columns) — contract-valid. Census prints
`mado ok` for the file.

`used-by` check: `grep -rn "S062" --include=*.md .` finds it only in the round-17
lesson gate line and in wave-1 reports/draft (which are not corpus notes);
`grep -rn linuxjunkies corpus/` finds only `corpus/lessons/round-17.md:49`. So
`—` is correct and there is no citing note whose claims need re-checking.

## Gate line — `corpus/lessons/round-17.md:49`

| gate element | claim | check |
|---|---|---|
| URL | `https://linuxjunkies.org/guides/configure-alacritty` | exact |
| location | `line 247` | reproduces exactly in the tag-stripped `<article>` text (321 lines): line 247 is the quote; see D1 for the numbering caveat |
| quote | `Starting with 0.12, Alacritty switched to TOML` | verbatim prefix of `Starting with 0.12, Alacritty switched to TOML for its better specification, type safety, and tooling support.` |
| words | `(7 words)` | 7 |
| digest | `08608a0b…bec2c653` | exact |
| verdict token | `(rejected)` | matches status `rejected` |
| access date | § Gate preamble "all opened 2026-10-20" | matches `opened` |

The quoted sentence appears twice in the raw bytes: once in the page's JSON-LD
FAQ (`"@type":"FAQPage"`, byte offset 9530) and once in the rendered FAQ answer.

## Rejection reason — both legs verified

Row: *"demonstrable version error — 'Starting with 0.12, Alacritty switched to
TOML' contradicts `v0.13.0` CHANGELOG `:36` and the absence of any TOML entry in
`v0.12.0`'s changelog"*.

1. `v0.13.0/CHANGELOG.md:36` is exactly `- Configuration file now uses TOML instead of YAML`
   (8 words), under `## 0.13.0` (`:8`) / `### Changed` (`:32`). The next line (`:37`)
   adds `Run `alacritty migrate` to automatically convert all configuration files`.
2. `v0.12.0/CHANGELOG.md` contains zero matches for `TOML` case-insensitively
   (`grep -ic toml` = 0, exit 1); its only `yaml` match is `:356`
   `The snapcraft.yaml file has been removed`. So no TOML entry exists in 0.12.0.

Independent controls agree on the boundary, so the reason does not rest on one
file:
- `v0.12.0/alacritty.yml` exists (200, 31779 B) and `v0.12.0/alacritty.toml` is
  404 — the 0.12 release tree is YAML.
- `v0.13.0/extra/man/alacritty.5.scd:5` `Alacritty - TOML configuration file format.`
  and `:9` `Alacritty's configuration file uses the TOML format.`

The page repeats the false boundary three times in its article text (`:43`
`(TOML replaced YAML in 0.12)`, `:51` `0.12 or later`, `:247` the FAQ sentence),
so this is not a one-off typo; the row's "one false boundary disqualifies its
other version claims" is a stated policy, not a factual claim, and the verdict
does not need it (see the secondary-claims note below).

## D1 — the only surviving attack: anchor numbering is not reproducible as written

The row cites two line numbers, `:51` and `:247`, with no extraction convention
(contrast S063/S064, which declare "anchors are lines of the tag-stripped
`<article>` text"). Measured on the same 90051-byte fetch, with
script/style/noscript dropped, one text node per line, empty lines dropped:

| text numbered | lines | line of `(TOML replaced YAML in 0.12)` | line of the quoted FAQ sentence |
|---|---|---|---|
| raw HTML bytes (`curl`, digest-bound) | 145 | — | — (no line 247 exists; the `read` tool's own raw fetch numbered 152 lines — different bytes, same conclusion) |
| reader text (`read` tool, line selectors) | — | `:51` = the Ubuntu sentence containing it | `:247` = `tested on:…`/`## Frequently asked questions`; the quote is first returned by `:252` |
| whole-document text nodes (bs4/lxml) | 353 | 51 | 255 |
| `body`-scoped text nodes | 352 | 50 | 254 |
| `article`-scoped text nodes | 321 | 43 | **247** |

Reading:
- The gate's `line 247` is exact only under the `article`-scoped numbering. That
  is the convention the sibling web rows declare, but S062 does not declare it,
  and the digest alone cannot lead a checker to it (raw bytes have 145 lines).
- The row's `:51` is exact only under whole-document numbering. Under the
  `article` numbering that makes `:247` true, line 51 is the fragment
  `0.12 or later` (part of "the `alacritty.toml` format requires **0.12 or
  later**") — still a TOML-at-0.12 placement, so the row's sentence is literally
  true under that reading, but the seat's own narrative
  (`w1/reports/SrcTerminalAlternates.md:213-214`, "line 51: `(TOML replaced YAML
  in 0.12)`") is the whole-document numbering.
- No wrapped dump I tried (textwrap 70–120 cols, article and body) puts the pair
  at (51, 247); the seat's reported "345 extracted lines" (same report, `:208`)
  does not reproduce either (observed 353 / 352 / 321 / 346).

Severity: documentation/reproducibility only. The verdict, digest, quote, word
count and reason are unaffected. Minimal fix, if the row is ever touched:
append `anchors are lines of the tag-stripped <article> text (321 lines)` to the
anchor cell (as S063/S064 do) and, if the parenthetical is what was meant, cite
`:43` for it. This is a wave-3 correction candidate, not a status change.

## Attack attempts that failed

- **"The rejection is wrong because 0.12 already had TOML."** v0.12.0 changelog:
  0 TOML tokens; v0.12.0 tree: `alacritty.yml` 200 / `alacritty.toml` 404. Failed.
- **"The quote is not verbatim or exceeds 25 words."** Verbatim prefix, 7 words,
  present twice in the fetched bytes. Failed.
- **"The digest is stale or does not bind these bytes."** 90051 B, HTTP 200, full
  sha256 equals the row's abbreviated digest; the wave-1 record
  (`w1/reports/SrcTerminalAlternates.md:42`, same 90051 B, same digest) and my
  fresh fetch at 11:53 local (per the `date:` header) agree despite
  `x-nextjs-cache: STALE`. Failed.
- **"`used-by: —` is wrong; a note cites it."** Only the gate line and wave-1
  reports mention S062; no `corpus/knowledge/` path does. Failed.
- **"Row shape or tier gaming."** NF=13; kind `community`; tier `C`; census ok;
  `community` never A per contract. Failed.
- **"Scope date is invented."** Page bytes carry `June 7, 2026` and
  `2026-06-07T00:47:45.371Z`. Failed.

Secondary claims of the page, checked for completeness (neither rescues nor
convicts the row): `The [keyboard] table (renamed from [key_bindings] in 0.13)`
is consistent with `v0.13.0` CHANGELOG`:40` (`Deprecated config option
key_bindings, use keyboard.bindings`); `Ligatures … enabled by default as of
0.13` has no supporting token in any changelog — `grep -ic ligature` = 0 across
v0.12.0, v0.13.0, v0.14.0, v0.15.0, v0.16.0, v0.17.0. The latter is unsupported,
not demonstrated false, and the row's verdict does not depend on it.

## Residual unknowns

- The wave-1 seat's exact extractor is unknown and uncommitted; "345 extracted
  lines" is not reproducible from the committed digest (my best matches: 353
  whole-document, 321 article, 346 article at 88 columns). Only D1 depends on it.
- The page is a Next.js response with `cf-cache-status: DYNAMIC` and
  `x-nextjs-cache: STALE`; content could drift, but the wave-1 record (same
  digest and size) and my fresh fetch (11:53 local) agree, so the recorded digest
  is currently reproducible.
- Nothing downstream depends on S062: it is rejected and no knowledge entry cites it.

## Method note / installs

Read-only: `curl` (raw bytes, sha256), `read` on the URL (reader text and line
selectors), `bs4/lxml` extraction in a `/tmp` scratch dir, one `git status` read.
No package command, no sudo, no host probe, no transcript access, no git
mutation; host-pause override respected.
**Installs: none.**

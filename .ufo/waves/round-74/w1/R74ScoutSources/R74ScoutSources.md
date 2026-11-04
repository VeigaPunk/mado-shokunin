# R74ScoutSources — source re-verification and id-guard proof

- seat: `R74ScoutSources` (leaf), mado round 74 wave 1
- date: 2026-11-04 (America/Sao_Paulo)
- base `bd5a971532f37df85a78f6f566dd1e649b79de11`; freeze+instruments `b73db773aaf67c9b26c8cf1a4cd567dec3af11f4` (= current `HEAD`)
- write dir: `.ufo/waves/round-74/w1/R74ScoutSources/`; scratch `/fast/scratch/hyaku/mado-r74/R74ScoutSources/` (removed after copying)
- no production file, committed lane file, git/jj state, `~/.config`, service or compositor surface touched. No tool installed (nothing was needed; all pacman transactions remain paused and were not attempted).

Axes this seat pushes: **fetch determinism** (three independent fetches must be byte-identical to the receipts the round cites), **quote locatability** (line number + ≤25-word located quote per row), **registry guard integrity** (the 0–3-space id extractor still separates a duplicate row from a distinct row), **record truth** (the routed D1 digest). Only moves that improve one axis and harm none were kept: the three receipts are re-derived, not rewritten; the S448 defect row is left in place (append-only) and a superseding row is checked instead of edited.

## 1. Three fetches per source — byte-identical, matching the committed receipts

Commands: `for t in 1 2 3; do (cd t$t && curl -sS --max-time 60|90 -o <name>.rst <url>); done`, then `sha256sum t1/* t2/* t3/*` and `cmp -s t$t/<name>.rst .ufo/waves/round-74/fetch/<name>.rst.$t`. Verbatim receipt: `fetch-digests.txt`.

| source (tag `v3.14.8`) | bytes | sha256 (all three fetches) | vs `fetch/<name>.rst.1..3` | HTTP |
|---|---|---|---|---|
| `Doc/library/secrets.rst` | 6305 | `289ff11e32dc6023446b1e8e0853635a9c19be200cb7df76f50a029993890659` | identical, `cmp` 3/3 OK | 200 (6305) |
| `Doc/reference/simple_stmts.rst` | 41375 | `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc` | identical, `cmp` 3/3 OK | 200 (41375) |
| `Doc/library/os.rst` | 208655 | `2d0f2892676e1cf9547be2bd94cfe2a6221dddea82d52cb2475d4a3d819b2ae5` | identical, `cmp` 3/3 OK | 200 (208655) |

- Every one of the nine triples is byte-identical within its source (`sha256` equal across `t1/t2/t3`) **and** byte-identical to the corresponding `.ufo/waves/round-74/fetch/<name>.rst.N` file (`cmp` 9/9 OK, no DIFF line). The three digests named in the seat brief match exactly.
- Confidence: **high** (three independent network fetches plus a fourth status-only fetch per URL, all 200; no cache/proxy divergence observed).

## 2. Quote locations, line numbers, word counts

`grep -nF` on the t1 fetch; word counts are whitespace-split on the exact quoted string (`quote-locations.txt`).

| row | quote (as recorded) | source lines | words | occurrences |
|---|---|---|---|---|
| S450 `secrets.rst` | "Return a random text string, in hexadecimal. The string has \*nbytes\* random bytes, each byte converted to two hex digits." | **80-81** (`token_hex` block 78-84) | **20** | 1 |
| S451 `simple_stmts.rst` | "If the target is an attribute reference: The primary expression in the reference is evaluated. It should yield an object with assignable attributes" | **160-162** (bullet 160-165) | **23** | 1 |
| S452 `os.rst` | "This mapping may be used to modify the environment as well as query the environment." | **196-197** (paragraph 196-198) | **15** | 1 |
| (S448 `os.rst`, for contrast) | "Changes to the environment made after this time are not reflected in os.environ, except for changes made by modifying os.environ directly." | **192-194** | **21** | 0 literal, 1 markup-normalized |

- All three round-74 quotes are ≤25 words and each occurs exactly once in its document. Anchors `78-84`, `160-165`, `196-198` each contain their quote; no anchor is past EOF or reversed.
- S450/S451/S452 quote strings are literal in the bytes (S451 truncates the source's `attributes;` at `attributes`, a clean word boundary). S448's quote is **markup-normalized**: the bytes read ``:data:`os.environ` `` twice, so a byte-literal search finds 0 — the same convention S448 was admitted under, not a new defect.

### F1 — the three round-74 rows each overstate their quote's word count by one

| row | recorded | measured (whitespace split) |
|---|---|---|
| S450 | "— 21 words" | **20** |
| S451 | "— 24 words" | **23** |
| S452 | "— 16 words" | **15** |

Observed, not inferred: the quoted strings tokenize to 20/23/15 words under any whitespace-collapsing split. The likely cause is counting the double space in the source line as an extra token, but the effect is a stated number that the bytes do not produce. No row violates the ≤25-word rule; S448's "21 words" is correct. Severity **low**, confidence **high**. Not repaired here (rows belong to the scribe/registry lane; the defect is recorded for the round-end reviewer).

### F2 — S448's quote is cited at `193-194` in two round-73 records but starts at `192`

`corpus/knowledge/guard-carrier-global-environ-r73.md:21` and `corpus/lessons/round-73-verifier-spotcheck.md:134` cite `os.rst:193-194`; the sentence begins on line **192** ("...site.py\`.  Changes"), so the true span is **192-194** (21 words, unchanged). The registry row S448 uses a block anchor `184-196`, which contains it — no false registry claim. Severity **low**, confidence **high**.

## 3. Routed defect D1 — false digest sweep and the exact superseding row

### 3.1 Every lane mention of the false digest

`grep -rn 2d0f2892676e1cf9f0d8e61c63a2e70a86f0e0a5cdb6b06dd7b7d2c9b8b88a4e .` from `/home/vgpnk/Projects/shokunin/mado-shokunin` (`digest-sweep.txt`):

| location | role | live claim? |
|---|---|---|
| `corpus/SOURCES.md:398` (S448 anchor) | **the defect itself** | yes — the only live registry assertion; superseded by S452, retained because the registry is append-only |
| `corpus/lessons/round-73.md:72` | round-73 lesson asserting the digest as admitted fact | stale narrative, contradicted by S452; lessons are history, not corrected in place |
| `corpus/lessons/round-73-verifier-spotcheck.md:134` | quotes the false digest as the finding | correct usage (defect record) |
| `corpus/lessons/round-73-verifier-spotcheck.md:168` | same, in the routed-defect text | correct usage |
| `corpus/knowledge/guard-carrier-twohop-environ-alias-r74.md:23` | quotes defect **and** states the true digest | correct usage |
| `corpus/lessons/round-74.md:45` | round-74 learning row quoting both digests | correct usage |
| `.ufo/waves/round-73/w1/R73ScoutSources.md:119` | the in-round finding that first caught it | frozen historical artifact |
| `.ufo/waves/round-73/w1-results.json:46` | seat output JSON | frozen historical artifact |
| `.ufo/waves/round-74/{make-spec-r74.py:175,w1-dispatch.json,w1-spec.json}` | the task text that routes D1 | task metadata, quotes the defect |

True digest, re-derived three times this round and byte-compared to the committed fetches: `2d0f2892676e1cf9547be2bd94cfe2a6221dddea82d52cb2475d4a3d819b2ae5` (208,655 B). The false string shares only the first 16 hex chars (`2d0f2892676e1cf9…`). After S452, the only lane file that still *asserts* the false digest as fact is the historical `corpus/lessons/round-73.md:72`.

### 3.2 The superseding row (S452) — present in the working tree, text verified

`corpus/SOURCES.md` is modified but **uncommitted** (`git status --short` → ` M corpus/SOURCES.md`); at `HEAD` (`b73db773`) the registry has 386 rows, max id **S449**, zero S450–S452. The three round-74 rows (S450/S451/S452) exist only as working-tree appends, which is what the seat brief asks this seat to draft/verify. Verbatim (`s452-row.txt`):

```
| S452 | CPython v3.14.8 library reference — os.environ mapping modification — https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/os.rst | docs | A | mado lane tooling: the environ mapping itself is the mutation surface, so a one-hop alias of it carries a key store into a later copy (round-74 C2) | § Process Parameters, .. data:: environ, os.rst:196-198 @ tag v3.14.8 (fetched 2026-11-04 three times, byte-identical: sha256 2d0f2892676e1cf9547be2bd94cfe2a6221dddea82d52cb2475d4a3d819b2ae5, 208655 bytes) | supersedes S448 — same environ block at the alias-modification paragraph; S448's recorded sha256 is corrected to 2d0f2892676e1cf9547be2bd94cfe2a6221dddea82d52cb2475d4a3d819b2ae5 (208655 B); "This mapping may be used to modify the environment as well as query the environment." — 16 words; it grounds the alias store as a real modification | mined | 2026-11-04 | 180d | corpus/knowledge/guard-carrier-twohop-environ-alias-r74.md |
```

Checks against the frozen requirement, all **observed**:

- cell 8 (`teaches`) opens exactly `supersedes S448 — ` ✔
- digest in the anchor cell is the true one, and the `teaches` cell restates it as the correction ✔ (size 208655 consistent)
- quote is literal at `os.rst:196-197`, 15 words ✔ (the cell's "16 words" is F1)
- 11 cells / NF=13 ✔; `docs`/`A`/`mined` enums ✔; `opened 2026-11-04` not future ✔; `recheck 180d` valid ✔; `used-by` path `corpus/knowledge/guard-carrier-twohop-environ-alias-r74.md` exists ✔
- same URL as S448 at a **different scope**, and the row carries `supersedes S448`, so the census emits only `W04` (cross-scope), never `E04` ✔ (section 4.4)
- S448 is left byte-untouched (append-only repair) ✔

Confidence: **high**.

## 4. Id-collision guard proof

Extractor under test is the committed census parser, `scripts/sources-census.sh` (fleet root):

- `:40` — "Maintained parser accepts 0–3 leading ASCII spaces before Markdown rows/headings; 4 or more spaces are indented code and ignored."
- `:573-574` — `row_pass()`, "Runs one gawk program over Markdown table rows with 0-3 leading ASCII spaces."
- `:615` — `if (line !~ /^ {0,3}\|/) next` (row admission)
- `:641` — `else if (id in seen) printf "%s\tE03\t%s duplicate id\n",lane,id` (the collision)

A Python mirror of exactly those three conditions (`idguard/extract.py`, keys on `^ {0,3}\|\s*(S[0-9]{3,})\s*\|` inside the `## Registry` section, emits `collisions`) is used where a `collisions` list is needed; the **real** script is run in parallel so the proof does not rest on the mirror. Full transcript: `idguard-receipt.txt`; fixtures `idguard/{dup,single,four}.md`.

### 4.1 Duplicate case — indented `  | S450 |` plus the staged S450 id

```
$ grep -n S450 idguard/dup.md
7:| S450 | CPython v3.14.8 library reference — fixture — https://example.invalid/S450 | docs | A | ...
8:  | S450 | CPython v3.14.8 library reference — fixture — https://example.invalid/S450 | docs | A | ...

$ python3 -I idguard/extract.py idguard/dup.md
{"collisions": [{"id": "S450", "lines": [7, 8]}], "file": ".../idguard/dup.md", "max_id": "S450", "rows": 2, "unique": 1}

$ bash scripts/sources-census.sh validate --file <dup.md> --today 2026-11-04 mado
file	W03	S450 mined but unused
file	E03	S450 duplicate id
file	E04	S450 duplicate url example.invalid/S450 within scope fixture scope for S450 (round-74 C1)
file	W03	S450 mined but unused
rc=1
```

`collisions` is **nonempty** and the real validator emits **E03** at exit 1. The 2-space row is parsed as a row, as designed.

### 4.2 Control — staged S450 + indented distinct S449 (same indentation, different id)

```
$ python3 -I idguard/extract.py idguard/single.md
{"collisions": [], ..., "max_id": "S450", "rows": 2, "unique": 2}
$ bash scripts/sources-census.sh validate --file <single.md> --today 2026-11-04 mado
file	W03	S450 mined but unused
file	W03	S449 mined but unused
file	ok	.../idguard/single.md
rc=0
```

Indentation alone does not create a collision; identity does.

### 4.3 Control — the 0–3 boundary (4-space row is code)

```
$ python3 -I idguard/extract.py idguard/four.md
{"collisions": [], ..., "max_id": "S450", "rows": 1, "unique": 1}
$ bash scripts/sources-census.sh validate --file <four.md> --today 2026-11-04 mado
file	W03	S450 mined but unused
file	ok	.../idguard/four.md
rc=0
```

A 4-space-indented duplicate is invisible to the parser, so E03 cannot fire on it — the guard is exactly the 0–3-space window and nothing wider.

### 4.4 Real registry at the base rev (max id S449) and the three proposed ids

```
$ git show bd5a9715:corpus/SOURCES.md > idguard/SOURCES-base.md
$ python3 -I idguard/extract.py idguard/SOURCES-base.md
{"collisions": [], "max_id": "S449", "rows": 386, "unique": 386}

$ candidate check
{"candidates": ["S450", "S451", "S452"], "collisions": [], "absent": ["S450", "S451", "S452"]}
```

At the base rev: 386 rows, 386 unique ids, max S449, **zero** collisions, and all three proposed ids free.

Working tree after the scribe's append:

```
$ python3 -I idguard/extract.py corpus/SOURCES.md
{"collisions": [], "max_id": "S452", "rows": 389, "unique": 389}
$ grep -cE '^ {0,3}\|\s*S450\s*\|' corpus/SOURCES.md   # 1
$ grep -cE '^ {0,3}\|\s*S451\s*\|' corpus/SOURCES.md   # 1
$ grep -cE '^ {0,3}\|\s*S452\s*\|' corpus/SOURCES.md   # 1
```

Each new id appears exactly once; no duplicate.

Live census on the lane (`bash scripts/sources-census.sh validate --today 2026-11-04 --root /home/vgpnk/Projects/shokunin mado`): **rc=0**, 389 rows, no E-finding; warnings are the held W04 set plus the expected document-sharing pairs `S447/S451` (simple_stmts), `S448/S452` (os.rst), `S442/S449` (subprocess), and held W01 `S277`. `S450` (secrets.rst) is the only untouched document and produces no pair, as intended.

Confidence: **high** (real validator, not only the mirror; fixtures and transcript stored).

## 5. Findings summary

| id | finding | severity | confidence |
|---|---|---|---|
| F1 | S450/S451/S452 `teaches` word counts are 21/24/16 but the quotes are 20/23/15 words (all still ≤25) | low | high (observed) |
| F2 | S448's quote is cited as `os.rst:193-194` in the round-73 knowledge entry and spot-check; the sentence starts at :192 (true span 192-194) | low | high (observed) |
| F3 | S448 digest defect is routed and superseded correctly by working-tree S452; only historical `corpus/lessons/round-73.md:72` still asserts the false digest as fact | info | high (observed) |
| F4 | Registry guard behaves exactly as advertised: E03 fires on a `  | S450 |` duplicate, not on an indented distinct id, not at 4 spaces | info | high (observed) |

Inference (labelled, not proof): the +1 counts in F1 are consistent with an extractor that splits on single spaces and counts the double space as a token; that hypothesis was not tested against the scribe's tooling.

## 6. Remaining unknowns / not checked by this seat

- Whether the scribe commits S450–S452 unchanged (they are uncommitted at report time, ` M corpus/SOURCES.md`).
- Whether the round-end reviewer treats the F1 word counts as a Gate note or requires a re-statement; this seat does not edit registry rows.
- The census's E04 `supersedes S[0-9]{3}` test is textual: it cannot tell a correct supersession target from a wrong one. S452's target is correct here by inspection, not by the guard.
- No `lsp` server is applicable to `.rst` documentation bytes; `grep -n` is the only available locator for this source class, so section 2 carries literal-grep evidence, not semantic references.

## 7. Disposition

- Receipts kept in this directory: `fetch-digests.txt`, `quote-locations.txt`, `digest-sweep.txt`, `s448-row.txt`, `s452-row.txt`, `idguard-receipt.txt`, `idguard/{extract.py,dup.md,single.md,four.md}`.
- Scratch `/fast/scratch/hyaku/mado-r74/R74ScoutSources/` deleted after the copies above. No tool installed or upgraded; no pacman transaction attempted; no git/jj mutation; no file outside this directory written.

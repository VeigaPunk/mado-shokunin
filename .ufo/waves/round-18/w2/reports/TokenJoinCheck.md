# TokenJoinCheck — strict `S###` → registry → receipt → anchor joins (wave 2)

Seat `MadoR18.TokenJoinCheck` (executor, leaf). Round 18 / wave 2 (FALSIFY).
Artifact attacked: §5.1 of `.ufo/waves/round-18/w1/reports/ConnSourcesUsedBy.md`
(the per-token join guarantee behind the C2 claim), against the integrated notes
and rows at `abfbf35b1ed4d4a1eb294d525ef286be30f3886f`.
Files changed: `.ufo/waves/round-18/token-join-check.py` (new, 14,566 B,
sha256 `7ff2407532d90321a743c1eba63d72dc972c31cb8721c34117cdd5003452ec5b`)
and this report. No lane file other than the tool was written; no row, note,
lesson or scorecard byte was touched. Host pause honoured: no package, service,
compositor, input or screenshot command; read-only git only (`rev-parse`,
`show`, `ls-tree`, `archive`); config trees not opened. No tool installed or
upgraded.

## 1. Axes

- **C2 coverage (primary).** The declared C2 number is a note-level count:
  `measure.py` credits a note when *at least one* `S###` resolves, so a note
  could keep its credit with 18 of 19 joins broken (ConnSourcesUsedBy §4 risk 3).
  This item closes that gap with a per-token checker that **bites** on each
  clause it claims to enforce. It changes nothing in `measure.py` itself.
- **C1 / C3 (untouched).** No QUALITY text, no lesson row, no instrument, no
  tripwire change.
- **Harm watch / registry.** The tool is read-only outside its stdout. It adds
  no row, so the census is unchanged by construction (not run here; L1 gate).

## 2. Behavior

`python3 -I .ufo/waves/round-18/token-join-check.py [REV] [--root DIR]`

- `REV` default `WORKTREE`; any commit-ish is resolved with
  `git -C ROOT rev-parse --verify`, and every input (registry, both notes, and
  each `fetch/*/receipts.jsonl`) is read from that commit via `git show`. So the
  measurement is of the committed tree, not of a sibling's in-flight edits.
- `--root` default = the lane containing the script (`HERE.parents[3]`); it
  points the same check at a throwaway copy.
- For each of `corpus/knowledge/walker-route-r18.md` and
  `corpus/knowledge/theme-route-r18.md`, every `S\d{3,}` token on a `source:`
  line must be:
  1. the id of a row inside `## Registry` (header-mapped cells; the `id` column
     position is taken from the header, not assumed to be first);
  2. `status` exactly `mined`;
  3. named exactly (after strip, comma split) by the row's `used-by` cell;
  4. for a row whose `source` cell holds an https URL: matched by at least one
     `mado-fetch-receipt-v1` line under
     `.ufo/waves/round-18/fetch/*/receipts.jsonl` with `http_status == 200`
     whose `url` or `final_url` normalises (scheme/host lowercased, fragment
     and trailing slash dropped) to that first URL, **and** that receipt's full
     sha256 appears in the row's `anchor` cell.
- A row with no https URL in `source` (host rows S090, S091, S095) is exempt
  from 4 and is reported as `host`; its anchor is a file-byte digest.
- No `S0xx` / `S###-pending` placeholder may remain anywhere in either note,
  and a `source:` line with **zero** tokens is a gap (the §5.1 empty-line arm).
- Output: one `JOIN` line per resolved token, one `GAP` line per defect, a
  `NOTE` count line per note, then `SUMMARY` and `RESULT`. Exit **0** clean,
  **1** any gap (including a malformed/mis-schema receipt line or a
  wrong-cell-count registry row), **2** cannot evaluate (bad rev, unreadable
  root, missing/non-table registry, unenumerable receipts).

## 3. Lane run at `abfbf35b1ed4d4a1eb294d525ef286be30f3886f` — PASS

Command (from the lane root):

```
python3 -I .ufo/waves/round-18/token-join-check.py abfbf35b1ed4d4a1eb294d525ef286be30f3886f
```

Exit `0`. Exact stdout (29 lines):

```
RECEIPTS files=21 lines=301 seats=21 rows=95
JOIN S072 web receipts=7 sha=9755f955d5c4… anchor=ok seats=MadoR18.SrcWalkerThemes,NoteWalker,SrcElephantReadme,SrcWalkerChangelog,SrcWalkerDefaultConfig,SrcWalkerDocsSite,SrcWalkerReadme
JOIN S073 web receipts=5 sha=3c5c6867d021… anchor=ok seats=MadoR18.SrcWalkerThemes,NoteWalker,SrcWalkerChangelog,SrcWalkerDefaultConfig,SrcWalkerReadme
JOIN S074 web receipts=3 sha=93b6bd6f3603… anchor=ok seats=MadoR18.SrcWalkerThemes,NoteWalker,SrcWalkerConfigPaths
JOIN S075 web receipts=2 sha=f09466fecf90… anchor=ok seats=MadoR18.SrcWalkerThemes,NoteWalker
JOIN S076 web receipts=1 sha=996db119ba61… anchor=ok seats=NoteWalker
JOIN S077 web receipts=3 sha=93287a1c389a… anchor=ok seats=MadoR18.SrcWalkerThemes,NoteWalker,SrcWalkerConfigPaths
JOIN S078 web receipts=2 sha=d1676045d110… anchor=ok seats=MadoR18.SrcWalkerThemes,NoteWalker
JOIN S079 web receipts=1 sha=e50c606040b2… anchor=ok seats=NoteWalker
JOIN S080 web receipts=3 sha=aa19a7e2d1c0… anchor=ok seats=NoteWalker,SrcElephantProviders,SrcElephantReadme
JOIN S081 web receipts=2 sha=2b4a6f1493be… anchor=ok seats=NoteWalker,SrcElephantProviders
JOIN S082 web receipts=2 sha=c1c2ecaaafac… anchor=ok seats=NoteWalker,SrcElephantProviders
JOIN S083 web receipts=2 sha=46ed4755bb3e… anchor=ok seats=NoteWalker,SrcElephantProviders
JOIN S084 web receipts=1 sha=0291cfe6cd80… anchor=ok seats=NoteWalker
JOIN S085 web receipts=1 sha=fecf71fa4253… anchor=ok seats=NoteWalker
JOIN S086 web receipts=2 sha=fd9e93f830bc… anchor=ok seats=NoteWalker,SrcOmarchyBackground
JOIN S087 web receipts=1 sha=9ac82d0c1370… anchor=ok seats=NoteWalker
JOIN S088 web receipts=1 sha=05cd9c672252… anchor=ok seats=NoteWalker
JOIN S089 web receipts=1 sha=5cb9874eedbc… anchor=ok seats=NoteWalker
JOIN S090 host (anchor is a file-byte digest)
JOIN S091 host (anchor is a file-byte digest)
NOTE corpus/knowledge/walker-route-r18.md source_lines=1 tokens=20 unique=20 web=18 host=2 gaps=0
JOIN S092 web receipts=2 sha=68ed5503298f… anchor=ok seats=MadoR18.SrcSwaybgMan,NoteTheme
JOIN S093 web receipts=5 sha=79069c8018a7… anchor=ok seats=NoteTheme,SrcOmarchyBackground,SrcOmarchyThemeHooks,SrcOmarchyThemeLayout,SrcOmarchyThemeSet
JOIN S094 web receipts=1 sha=dbdd13a629aa… anchor=ok seats=NoteTheme
JOIN S095 host (anchor is a file-byte digest)
NOTE corpus/knowledge/theme-route-r18.md source_lines=1 tokens=4 unique=4 web=3 host=1 gaps=0
SUMMARY rev=abfbf35b1ed4d4a1eb294d525ef286be30f3886f notes=2 tokens=24 unique=24 web=21 host=3 gaps=0
RESULT PASS
```

What this establishes at that revision: P3 cites 20 distinct rows (18 web,
S090/S091 host), P5 cites 4 (3 web, S095 host); every row is inside
`## Registry`, `mined`, and names its note verbatim in `used-by`; each of the 21
web rows has at least one committed 200 receipt for its first URL whose full
sha256 is in the row's anchor cell; there is no `S0xx`-class placeholder left.
Receipt census at that commit: 21 receipt files, 301 schema-valid lines.

Two independently observed robustness facts:

- A later worktree run on the same lane (`WORKTREE`, while sibling seats were
  still appending receipts; observed `files=49 lines=422`) also exited 0 with
  the identical `SUMMARY` (24/24, 21 web, 3 host). Appended receipts are
  additive; they do not change the verdict. The committed-rev run above is the
  reproducible unit, because the worktree receipt census keeps moving.
- `python3 -I … deadbeef` → exit 2 (`ERROR cannot resolve rev`);
  `… WORKTREE --root <absent>` → exit 2 (`ERROR cannot read corpus/SOURCES.md`).

## 4. Falsification on `/tmp` copies — seven mutants, all bit

Fixture construction (read-only git in the lane; writes only under `/tmp`):

```
rm -rf /tmp/mado-tjc-r18 && mkdir -p /tmp/mado-tjc-r18
for m in m1 m2 m3 m4 m5 m6 m7; do
  mkdir -p /tmp/mado-tjc-r18/$m
  git archive abfbf35 corpus/SOURCES.md \
      corpus/knowledge/walker-route-r18.md \
      corpus/knowledge/theme-route-r18.md \
      .ufo/waves/round-18/fetch \
    | tar -x -C /tmp/mado-tjc-r18/$m
done
```

Baseline before mutation, all seven copies: `RESULT PASS`, exit 0. Then exactly
one cell/token was changed per copy (editor, not a script):

| # | copy | mutation | observed gap | exit |
|---|---|---|---|---|
| M1 **(required)** | m1 | S086 `used-by` → `—` | `GAP  corpus/knowledge/walker-route-r18.md:1 S086 used-by-missing detail=used-by='—'` | 1 |
| M2 | m2 | S086 `status` `mined` → `proposed` | `GAP  …:1 S086 not-mined detail=status='proposed'` | 1 |
| M3 | m3 | S086 anchor sha256 → 64 zeros | `GAP  …:1 S086 sha-not-in-anchor detail=receipt_sha=fd9e93f830bc,fd9e93f830bc anchor_sha=000000000000` | 1 |
| M4 | m4 | S086 source URL → `…/bin/omarchy-never-fetched` | `GAP  …:1 S086 no-200-receipt detail=url=https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-never-fetched` | 1 |
| M5 | m5 | P5 `S095` → `S0xx-pending` | `GAP  corpus/knowledge/theme-route-r18.md:1 - placeholder token=S0xx` | 1 |
| M6 | m6 | P3 `S086` → `S096` (no such row) | `GAP  …:1 S096 not-a-registry-row` | 1 |
| M7 | m7 | all four P5 tokens removed from the `source:` line | `GAP  corpus/knowledge/theme-route-r18.md:0 - no-source-tokens` | 1 |

Each run used
`python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/token-join-check.py WORKTREE --root /tmp/mado-tjc-r18/<m>`.
The required mutant is M1 (one `used-by` broken): the checker fails the note
that would otherwise still be credited by `measure.py`, which is precisely the
invisible-partial-join failure of ConnSourcesUsedBy risk 3.

Note on M5: replacing the token also drops `tokens` to 23, but the placeholder
scan is independent of the token join, so the gap is reported even though the
remaining 23 joins pass. M7 proves the no-token arm is not vacuous.

## 5. Limits / risks a closure must read

1. **Tier is reported nowhere and not gated.** The item names only `mined`,
   `used-by` and the receipt/anchor join. All 24 cited rows are tier `A` at
   `abfbf35` (observed while probing), so C2's tier-A wording holds for this
   note pair, but a future tier-B row would pass this checker. If closure wants
   tier-A enforced per token, that is a one-line extension.
2. **Only the first URL in a multi-URL `source` cell is receipt-joined.**
   S092/S093/S094 name additional bodies after the first URL; their anchor
   cells carry those shas too, but the checker does not require a receipt per
   additional URL. This matches the item's singular wording; it is not a proof
   for the secondary bodies.
3. **Host rows are exempt from the receipt clause by design** (S090, S091,
   S095): their anchors are file-byte digests. The C2 sentence "each new credited
   row backed by a committed raw fetch receipt" must be read as web rows only
   (ConnSourcesUsedBy risk 7).
4. **URL matching is normalised equality on `url`/`final_url`, not redirect
   chasing.** The basecamp↔omacom split (risk 2) remains census-blind; a row
   whose URL a seat fetched in the other owner form would show `no-200-receipt`.
   At `abfbf35` all 21 web rows match their own receipt form.
5. **`measure.py` is unchanged.** It still credits a note on one resolvable
   token; this checker is the stricter, separate gate. Do not report the
   note-level count as a per-token result.
6. **Receipt-schema gate.** A line that is not `mado-fetch-receipt-v1`, or whose
   `http_status`/`sha256` is malformed, is a gap (exit 1), so a corrupted
   receipt cannot silently remove a witness.
7. **No census / harm-watch / `measure.py` run by this seat** (L1 owns those
   gates). This seat installed nothing and fetched nothing.

## 6. Evidence ledger

- `abfbf35b1ed4d4a1eb294d525ef286be30f3886f` — receipts commit measured; lane
  files compared byte-identically worktree-vs-blob before the run
  (`corpus/SOURCES.md` `9552071c…`, `walker-route-r18.md` `3ff430a4…`,
  `theme-route-r18.md` `b080bc47…`).
- Tool sha256: `7ff2407532d90321a743c1eba63d72dc972c31cb8721c34117cdd5003452ec5b`.
- Lane PASS output: 29 lines above, exit 0.
- `/tmp` lab: seven clean baselines PASS/exit 0; seven single-defect mutants all
  exit 1 with the GAP line shown in §4.
- Worktree superset observation: `RECEIPTS files=49 lines=422`, exit 0 (moving
  target while siblings append; not the measured unit).

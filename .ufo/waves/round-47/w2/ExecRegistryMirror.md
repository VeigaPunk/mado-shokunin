# ExecRegistryMirror — all round-47 registry changes, applied together on a mirror (w2, falsify)

Seat `ExecRegistryMirror` (executor, leaf). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, base
`60edb66e2f1cb90acc6e9442fc93ded0ca42d750`, lane HEAD at work time `9bddd6ac` (frozen claims at `d7527d60`).
Nothing tracked was edited; no git/jj mutation anywhere; scratch `/fast/scratch/hyaku/mado-r47/ExecRegistryMirror`
(320 M mirror, deleted). No tool installed. Every receipt below is copied into
`.ufo/waves/round-47/w2/ExecRegistryMirror/`; the mirror tree itself is not evidence and is gone.

Question asked of this seat: do the round's registry changes, applied **together and before any append**, pass the
gate, and what do they collide with? Answer: the census is clean (exit 0, 0 E, 3 expected new warnings), the
append is pure addition (21 rows, 0 removed), and there are **two collisions the census cannot see** — one between
two w1 drafts, one between the round's ids and the staged merge package — plus an id-space ambiguity in tracked prose.

## 1. Inputs (sha256, computed here)

| input | sha256 |
|---|---|
| `corpus/SOURCES.md` at lane HEAD (262 rows, top `S325`) | `2f5dfee8c97e05347a3e5f902dfd223d9f870a35647b4e4bc5e4a1c6ca2778ea` |
| new rows `.ufo/waves/round-47/w1/ScrRows/rows.md` (13 rows `S326`-`S338`) | `41f0c562e189183143bb82b492e7357289e5322695f12618f5f7b292bdf68193` |
| supersession `.ufo/waves/round-47/w1/ExecSupersede/rows-block.txt` (8 rows `S346`-`S353`) | `11be143b6221f31f37d9f8a97199f1b965650731fbe21ba7e4a42f0a52d67b00` |
| staged package `/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md` (147 rows `S203`-`S349`) | `684efe8c23b8b64d789187dab61bfbf7c0dcef4f0428e447c94d7be4e73a27c0` |
| mirror after the round's 21 rows (`apply-and-count.sh` output) | `51d2bfdedb851c167a9ffe7ccbb3543f4c8c66d5ed68894438ba263d1c5c4a7a` |

No other w1 draft carries registry rows. Enumerated, not assumed:

```
$ cd .ufo/waves/round-47/w1 && grep -rlE '^\| S[0-9]{3} ' --include='*.md' --include='*.txt' . | sort
./ExecControls/c2/*/files/corpus/SOURCES.md   (C2 control fixtures, not drafts)
./ExecIdGuard.md, ./ExecIdGuard/receipts/*    (guard receipts, not drafts)
./ExecSupersede/rows-block.txt                (8 rows — applied)
./ScoutSpecs/candidate-rows.md                (6 candidate rows, superseded — see H1)
./ScoutSpecs/sources.md, ./ScrRows.md, ./ScrRows/rows.md   (13 rows — applied)
```

Method: `rsync -a --exclude .git --exclude .jj` of the lane into scratch; rows inserted inside `## Registry`
immediately before `## Paths` (the landing point the supersession draft names); census on the mirror by
`--file` (used-by resolves against the file's grand-parent, i.e. the mirror root — same rule as the drafts'
own receipts). Driver: `apply-and-count.sh` in the seat dir (writes only in its argument dir).

## 2. Census — measured runs

`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-26 --file <mirror>/corpus/SOURCES.md`

| run | tree | exit | rows | E | W | receipt |
|---|---|---:|---:|---:|---:|---|
| base | lane registry untouched | **0** | 262 | 0 | 15 | `census-base.txt` |
| **a1** | **13 new rows + 8 supersession rows, entry stand-in present** | **0** | **283** | **0** | **18** | `census-a1.txt` |
| a0 | same, C2 entry absent | **1** | 283 | 13 (`E11` x13) | 18 | `census-a0.txt` |
| b0 | supersession block applied *before* the new rows | 0 | 283 | 0 | 18 | `census-b0.txt` |
| c0 | staged package first, then the round's 21 rows | 1 | 430 | 65 `E03`, 33 `E01`, 2 `E04`, 136 `E11` | — | `census-c0-staged-first.txt` |
| d0 | gap-closing numbering `S339`-`S346` for the block | 0 | 283 | 0 | 18 | `census-d0-gapclosing.txt` |
| f0 | all 21 rows numbered `S354`-`S374` | 0 | 283 | 0 | 18 | `census-f0-past-package.txt` |
| g0 | the two w1 drafts landed together (`S326`-`S331` twice) | 1 | 289 | 6 (`E03` x6) | — | `census-g0-both-drafts.txt` |
| h0 | the 8 supersession rows only (C1/C2 rows absent) | 0 | 270 | 0 | 16 | `census-h0-block-only.txt` |
| e0 | a1 tree with the `.ufo/.../ExecSupersede/` seat dir removed | 1 | 283 | 8 (`E11` x8) | — | `census-e0-noseatdir.txt` |

The a1 tail and the only warnings the round adds:

```
file	ok	<mirror>/corpus/SOURCES.md
exit 0        rows=283  E=0  W=18

file	W04	S326 duplicate url raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec across scopes
file	W04	S327 duplicate url raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/README.md across scopes
file	W04	S346 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/RegexMatchEngine.cpp across scopes
```

15 warnings pre-exist (`W04` x14, `W01` `S277`); the delta is exactly the three the drafts predict (`S326` shares
`S057`'s URL, `S327` shares `S056`'s, `S346`'s scope was deliberately narrowed). Nothing else changes.

Append-only proof (`append-only.diff`, `applied-ids.txt`): `removed_lines=0 added_lines=21`; 283 = 262 + 21; the
ids in file order are

```
S326 S327 S328 S329 S330 S331 S332 S333 S334 S335 S336 S337 S338 S346 S347 S348 S349 S350 S351 S352 S353
```

Shape, computed per row (`awk -F'|'`, 21 rows): `cells=11 pipes=12` on every one; the census agrees (`E01` = 0, so
`NF == 13` in its own split).

Order is not load-bearing for the gate: b0 (block first) is byte-for-byte the same verdict. It *is* load-bearing
for a reader: only the a1 order keeps the registry ascending.

## 3. Id-collision guard (the prompt's guard, 0–3-space pattern) — collisions

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <registry>   | grep -oE 'S[0-9]+' | sort > reg-ids
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' SOURCES.append.md | grep -oE 'S[0-9]+' | sort > staged-ids
$ comm -12 reg-ids staged-ids > collisions
```

| run | registry | reg ids | staged ids | collisions |
|---|---|---:|---:|---:|
| g0 base | 262 rows `S001`-`S325` | 262 | 147 | **70** |
| g1 after the round's 21 rows | 283 rows `S001`-`S353` | 283 | 147 | **87** |
| d0 gap-closing | 283 rows | 283 | 147 | 91 |
| f0 past-package | 283 rows `S001`-`S374` | 283 | 147 | **70** (no new) |

g0 reproduces `w1/ExecIdGuard` exactly (`diff` of `reg-ids`, `staged-ids` and `collisions` empty; same 70 ids
`S203`-`S221`, `S253`, `S258`, `S277`-`S325`; its `quarantine-slice` is untouched by this seat). The round's append steals **17 further staged ids** (`collisions-new.txt`):

```
S326 S327 S328 S329 S330 S331 S332 S333 S334 S335 S336 S337 S338 S346 S347 S348 S349
```

Consequence, measured not asserted: 17 of the 24 staged ids that sat above the registry top (`S326`-`S349`) are now
registry ids, so the staged package's adoption base moves from `S326` to `S354` — and `S339`-`S345` (the only
un-collided staged ids left above the old top) sit inside a registry hole, so they are unusable under "adopted ids
continue the lane's registry" (`scripts/hyaku/lane-addendum.md:377` guard, `:395` adoption rule). Reverse order is a hard failure:
staged-first (c0) is `E03` x65 on top of 33 `E01` (campaign-schema rows are not fleet-schema), exit 1.

Guard self-proof (`guard-proof-a.txt`, `guard-proof-b.txt`), because a guard that cannot fire proves nothing:

- scratch registry with `  | S002 |` + staged `S002` → 0–3-space extractor yields `S002` (count 1); a
  column-zero-only extractor yields **0** (the documented false-green);
- the two real inputs hold **0** indented rows today (registry 283/283 matched at column 0, append 0 of 147), so the
  pattern choice changes nothing on these bytes; `w1/ExecIdGuard` already records the `^ {0,3}` bound (4+ spaces
  escapes) — I confirmed no such row exists in either file.

## 4. Holes found (each with the command that shows it)

### H1 — two w1 drafts claim the same six ids for different sources (hard, census-visible when both land)

`ScoutSpecs/candidate-rows.md` numbers the spec MR 3 as `S326`, the desktop-entry 1.5 page as `S327`, the menu 1.1
page as `S328`, basedir 0.8 as `S329`, `tests.bats` as `S330` and the man page as `S331`. `ScrRows/rows.md` numbers
almost the same source set differently (script `S326`, README `S327`, man page `S328`, `tests.bats` `S329`, MR 3
`S330`, desktop-entry *XML* `S331`). Landing both drafts, which a "all registry changes of the round" instruction
could be read to require, is exit 1:

```
$ awk ... pristine + ScoutSpecs/candidate-rows.txt + new-rows.txt + sup-rows.txt ... > corpus/SOURCES.md
$ bash scripts/sources-census.sh validate --today 2026-10-26 --file <mirror>/corpus/SOURCES.md ; echo $?
file	E03	S326 duplicate id          ... through S331
file	E03	S331 duplicate id
1                     (census-g0-both-drafts.txt: E=6, E03=6, E01=0)
```

The candidate set is otherwise subsumed by `ScrRows` **except one source**: `…/menu/1.1/` appears only in the
candidate draft, and the candidate's `S327`/`S329` point at rendered documentation where `ScrRows` pins the XML
sources instead. So: land `ScrRows` only, and the candidate draft must be recorded as superseded (not landed,
not renumbered).

### H2 — the round's ids collide with 17 ids of the live staged package (guard 70 → 87)

This is the finding the guard exists for, and the round's own rows create it. Reproduce with the §3 block; the
registry is authoritative and the staged side renumbers, so nothing here blocks the append — but the L1 must not
leave `.ufo/waves/round-47/assimilation/{reg-ids,staged-ids,collisions}` at their 262-row values: they are stale the
moment the 21 rows land, and a renumber map built from them would silently miss `S326`-`S338` and `S346`-`S349`.

### H3 — 13 of the 21 ids already mean something else in tracked corpus prose (census-blind)

`prose-id-space.txt` (computed, 41 occurrences, 13 ids) and `locators.txt`:

| id(s) | tracked prose meaning | locator |
|---|---|---|
| `S326` | the staged package's journal sweep | `corpus/lessons/round-44.md:63` |
| `S326`-`S333` | the **round-46 lane supersession draft's** ids | `corpus/lessons/round-46.md:308` ("`drafted S326-S333`") |
| `S327`, `S335`, `S336`, `S337`, `S329`-`S331`, `S334` | staged-package ids in the M35-1 remap table | `corpus/lessons/round-35.md:127-130,135,216,249` |
| `S349` | the top of the staged range (`S203`-`S349`) | `corpus/lessons/round-43.md:83`, `round-44.md:71`, `round-46.md:373` |

So `S326` would carry three meanings after this append (package id, round-46 lane draft id, round-47 C2 row) and
`S326`-`S333` two. `round-46.md:308` is the sharpest: it tells the reader the supersession rows are `S326`-`S333`
— this round lands *terminal-selection* rows there and puts the supersession at `S346`-`S353`. The census reads
only `SOURCES.md`, so it cannot see any of this; this is the same class as the lane's own recorded mistake M35-1
(id-space citation, `corpus/lessons/round-35.md:210-218`).

Cheapest removal of both H2 and H3, measured: number the 21 rows **`S354`-`S374`** (13 new rows `S354`-`S366`,
block `S367`-`S374`). f0 = exit 0, 283 rows, `E=0`, the same three `W04` (renumbered), **collisions 70 → 70 (0 new)**,
and `grep -rnoE 'S3(5[4-9]|6[0-9]|7[0-4])\b' --include=*.md corpus/` = **0** occurrences in prose. Cost: the registry
top moves to `S374` and `S326`-`S353` stay unused (63 such holes exist at base already, so gap size is not a
defect); `claims.md`'s sentence "on rows S326.. opened this round" would need a logged erratum, while the frozen
predicate stays satisfied — the C2 counter reads only `>= S326`
(`quality/counters/c2-r47-terminal-entry.py:27`), and `f0`'s three renumbered warnings are the same three rows.

### H4 — the block's `used-by` is a removable scratch-shaped path (8 rows dangle if the seat dir goes)

All eight supersession rows name `.ufo/waves/round-47/w1/ExecSupersede/rows.md`. The lane has a precedent for
deleting an untracked seat file after digesting it (registration R2; the round-46 target
`.ufo/waves/round-46/w1/ExecStofOracle/receipts/out.json.rows.tsv` is **absent** today — measured). Simulating that
cleanup: exit 1, `E11` x8 (`census-e0-noseatdir.txt`). The 13 new rows' `used-by` is the tracked entry path and is
robust. `CORPUS.md:116` allows `used-by` to change in place, so the fix is one logged old→new per row once
`corpus/lessons/round-47.md` exists (moving to it before it exists is exit 1, `E11` x8 — the draft measured this).

### H5 — the append has a hard prerequisite: rows without the C2 entry are exit 1

a0 (rows applied, `corpus/knowledge/xdg-terminal-selection-r47.md` absent): `E11` x13, one per new row, exit 1. The
two must land in one commit (rows first is fine only within that commit; the frozen C2 clause b also requires each
row's `used-by` to list the entry, so a stand-in cannot substitute). Conversely the supersession block alone is
self-sufficient — measured h0 (block only, no C1/C2 rows): exit 0, 270 rows, `E=0`, `W=16` (base 15 + the narrowed-scope
`W04` for `S346`) — so the entry, not the block, is the dependency.

### H6 — the block's stated id assumption is off by seven, and the gap is harmless

`w1/ExecSupersede/rows.md:100` places the block at `S346`-`S353` "on the assumption C2 takes `S326`-`S345`".
C2 actually takes 13 rows (`S326`-`S338`), so `S339`-`S345` stay empty. The draft's own shift rule does not trigger
(C2 does not reach past `S345`), the census has no gap check, and the base registry already carries 63 holes
(`S190`-`S276`), so this is cosmetic. Gap-closing (`S339`-`S346`, d0) is still clean (`E=0`, `W=18`) but costs 4 extra
staged collisions (91 vs 87) and does not touch H3.

## 5. What a landing must satisfy (all measured on the mirror)

1. 21 rows, in `## Registry` before `## Paths`, 11 cells each, ids unique against the registry (`E03` = 0) and
   against each other; `supersedes S29N` openers resolve to the correct predecessors — computed check: 7/7 openers
   name an existing row whose **URL equals** the new row's URL (`S290`→`S346` … `S297`→`S352`), `S353` is a new
   grounding row. Keep the openers: stripping them returns `E04` x4 (the draft's m3 control).
2. The C2 entry in the same commit (§H5).
3. Warning budget: base 15 + exactly 3 (`W04` `S326`, `S327`, and the narrowed-scope `S346`). Any other `W` line is a
   regression.
4. No cell of `S001`-`S325` may change (append-only, `CORPUS.md:116-118`): the mirror diff has 0 removed lines and
   `S056`-`S060` (C2 clause h) are untouched.
5. Regenerate `.ufo/waves/round-47/assimilation/*` from the post-append registry (§H2) and record which id base the
   staged package adopts: `S354` under the drafted numbering, `S375` under f0.

## 6. Limits

- `--file` mode, not `--root`: `--root` needs the fleet MANIFEST and scans every lane, which is outside this seat's
  write/read remit. The drafts, their controls and the lane's earlier rounds all use `--file`; used-by resolution is
  identical (grand-parent of the registry file).
- The mirror excludes `.git`/`.jj`; the census does not read history. C2 clauses that compare against BASE
  (`S056`-`S060` byte equality) are not judged here — only their non-modification by this append.
- Collision counting is id identity; it cannot decide whether a staged row and a registry row are the same document
  (`w1/ExecIdGuard` measured 2/70 same-URL pairs). H3 classifies prose occurrences by their surrounding text, which
  is a reading, not a machine verdict.
- The f0 numbering is a measured option, not a ruling: it also makes `claims.md`'s "rows S326.." sentence stale.
- Quote check: this report quotes no source text beyond ≤25-word spans; every locator above is `grep -n` output
  recorded in `locators.txt`.

## 7. Reproduce

```
W=/fast/scratch/hyaku/mado-r47/ExecRegistryMirror; mkdir -p "$W"
rsync -a --exclude .git --exclude .jj --exclude .ruff_cache \
  /home/vgpnk/Projects/shokunin/mado-shokunin/ "$W/tree/"
bash /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/w2/ExecRegistryMirror/apply-and-count.sh "$W"
bash /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/w2/ExecRegistryMirror/guard-proof.sh "$W"
```

`apply-and-count.sh` prints the base/a0/a1/b0 verdicts, the append-only delta, and g0/g1 collision counts;
`guard-proof.sh` prints the indented-collision proof, the indentation census of both real inputs, and the
staged-first (c0) failure. Both write only inside their argument directory; the seat dir copies are the receipts.

## 8. Files in the seat dir

`apply-and-count.sh`, `guard-proof.sh` (drivers); `census-{base,a0,a1,b0,c0-staged-first,d0-gapclosing,
f0-past-package,g0-both-drafts,e0-noseatdir}.txt`; `collisions-{g0,g1,new}.txt`; `append-only.diff`;
`applied-ids.txt`; `new-rows.txt`, `sup-rows.txt`, `sup-shifted.txt`, `rows-past-package.txt(.sup)`,
`scout-candidate-rows.txt` (exact row bytes applied, per variant); `guard-proof-{a,b,c}.txt`;
`prose-id-space.txt`, `locators.txt`; `driver.out`, `driver-guard.out`, `row-counts.txt`.

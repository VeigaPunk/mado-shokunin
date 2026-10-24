# RevengerPrior — round 30, wave 1 — the index row's Sources cell

Reverse-engineering report only. No lane byte outside this file was written; all
git use read-only (`log`, `status`, `diff --stat`). No tools installed (pacman
guard respected; nothing needed). Read against worktree at tip `d72243e`, proven
byte-identical to data commit `446dc396` for `corpus/README.md` and
`corpus/SOURCES.md` (`git diff --stat 446dc396 d72243e --` empty), so every
finding below holds at the predicate revision.

## Axes (godspeed)

- **evidence** — every claim anchored to `file:line` or reproduced command output.
- **coverage** — every index row in the r18–r26 band read (9 rows exist there, not 6; all read).
- **correctness** — fence semantics reconstructed from *both* carriers of the regex, not from names.
- **latent-yield** — the latent check was actually executed once, read-only; it found one live format defect.
- **scope** — zero mutations; report is the only artifact.

## 1. Reconstructed contract — what the fence actually reads

The regex quoted by the item, `^\| `knowledge/([^`]+\.md)``, lives in **two**
places, and **not** in the C2 counter:

1. **The frozen navigation fence** (S185): `SCORECARD.md:77-88`, the "Counting
   command" shell block, sha256 of block `8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88`
   (SOURCES.md:197). Line 78: `rows = re.findall(r"^\| `knowledge/([^`]+\.md)`", index, re.M)`.
2. **The C3 gate**: `quality/check-index.py:11`,
   `ROW_RE = re.compile(r"^\|\s*`knowledge/([^`]+\.md)`", re.M)` — a
   whitespace-tolerant superset (`\s*`), same captured group, `evaluate()` at
   `check-index.py` builds `Counter(ROW_RE.findall(readme))` and derives
   missing/dangling/duplicates.

The C2 counter `.ufo/waves/round-30/c2/count.py` carries only QUALITY-criterion
regexes (`CRIT_RE`, `LIT_RE`, `PATH_RE`, `ANCH_RE`, `SPELL_RE`, `SUPER_RE`,
`MID_RE`, lines 44-50) — it never reads `corpus/README.md`. The item's premise
"the counter's regex" is therefore precise only if "counter" means the frozen
fence / C3 gate; recorded as a premise correction, not a defect.

**Contract reconstructed from the code** (fence `SCORECARD.md:77-88`):

- Capture exactly one group per matching line: the filename backticked at the
  *start of the first cell* of a line beginning `| `knowledge/…``.
- `missing` = knowledge notes with no row; `dangling` = rows naming no note;
  `duplicates` = notes with >1 row. Exit 1 iff any is nonempty.
- Nothing else is parsed. **The Sources cell (third cell) is ignored entirely,
  and so is the Holds cell and the Note cell's MADO-id annotation.** The regex
  never advances past the first backtick group; a row consisting of
  `| `knowledge/x.md` | | |` is indistinguishable from a fully cited one.
- No table scoping: any line of `README.md` starting `| `knowledge/…`` counts,
  wherever it sits. At tip this is benign — exactly 43 row-start matches for 43
  notes (audited) — but a stray row in any other table would silently move the
  indexed fraction.

## 2. Answer to the premise question

**Yes — the counter ignores Sources-cell content entirely.** Proven by the
captured-group shape (first cell only) and by the Counter/set arithmetic that
consumes it (`SCORECARD.md:79-88`; `check-index.py` `evaluate()`). The Sources
cell is pure prose to every tool in the round-30 predicate set.

## 3. The historical rows (r18–r26 band)

The band contains **nine** rows, not six (rounds 18, 20, 21, 22, 23, 24, 25, 26;
rounds 19 and below are outside it — r19's moves are described in frontier
prose, not rows). All nine read from the committed bytes (`README.md:44-52`).

| Row (round landed) | Sources-cell format | Cited ids |
|---|---|---|
| `walker-route-r18` (r18) | `` `source:` S###–S### in [SOURCES](SOURCES.md); fetch receipts `.ufo/waves/round-18/fetch/` `` | S072–S091 (20) |
| `theme-route-r18` (r18) | same shape | S092–S095 (4) |
| `tripwire-precision-r20` (r20) | same shape | S099–S115 (17) |
| `tripwire-binding-boundaries-r21` (row added **r24**) | `` `source:` … in [SOURCES](SOURCES.md); evidence `.ufo/waves/round-21/residual/`, lesson21 `` | S116–S118 (3) |
| `tripwire-lifetime-recovery-r22` (row added **r24**) | `` `source:` …; lesson22 and `.ufo/waves/round-22/evidence/resume/` `` | S121, S122 (2) |
| `terminal-trees-r23` (row added **r24**) | `` `source:` S123–S152 in [SOURCES](SOURCES.md) (S132 queued) `` | S123–S152 (30) |
| `rule-attribution-r24` (r24) | `` `source:` S153–S160, S162–S168 in [SOURCES](SOURCES.md) (S161 queued); fetched bytes `.ufo/waves/round-24/fetch/S###.bin` `` | 16 |
| `bind-table-r25` (r25) | `` `source:` S162, S167, S169–S172 in [SOURCES](SOURCES.md); lesson25 § Gate `` | 6 |
| `animation-table-r26` (r26) | **no Sources cell** — the row has 3 cells; the citation `Sources S175–S177, S158, S162.` sits at the tail of the *Holds* cell | 5 |

Later rows the C1 repair added (outside the band, for contrast): r27/r28 use a
**recheck-command** format — `` recheck `python3 -I .ufo/waves/round-27/c1/count-v4.py REV` ``
and `` registration `.ufo/waves/round-28/registration.md` `` (`README.md:53-54`).

Earlier rows (pre-r12, e.g. `idle-lock-plane.md`, `README.md:31-42`) use the
self-link format `[Source and recheck](knowledge/<note>.md): §§…` — citation by
section pointer, no S-ids at all. The r12+ convention `` `source:` S###… in
[SOURCES](SOURCES.md) `` is the one a stricter gate can machine-check.

## 4. The latent check, executed (read-only)

I ran the check the fence does not run: extract every `S###` from each row,
expand en-dash ranges with the lane's own convention (`count.py` `expand_ids`,
`count.py:56-70`, treats `a<=b` ranges as inclusive), and set-difference
against SOURCES.md's defined rows (`^\|\s*S###\s*\|` — 185 defined at tip).

Result at `446dc396`/tip:

- **Zero undefined cited ids.** Every id cited by all 43 rows resolves. So
  S-existence is a *regression fence*, not a bug-finder today — it would have
  caught nothing this round, but would catch a future typo'd `S186`/`S196`-style
  row instantly.
- **Queued ≠ absent.** The two parenthesized "(S### queued)" ids both *exist*
  as SOURCES rows: S132 (`SOURCES.md:144`) and S161 (`SOURCES.md:173`). The
  annotation is *status* prose ("queued" for claim support; S132's own row says
  "NOT version pinned and NOT claim support"), not registry absence. A naive
  existence gate passes them; a *status-aware* gate would need the
  parenthetical, or the row's own metadata.
- **One live format defect: `animation-table-r26.md`.** Its row has 3 cells
  against the header's 4 (`| Note | Holds | Sources |`); the third cell is
  absent and the S-citation is stranded at the Holds-cell tail
  (`README.md:52`, raw tail: `…own table. Sources S175–S177, S158, S162. |`).
  No tool in the round-30 predicate set can see this: the fence reads only cell
  1, the cell-count mismatch is invisible to it, and the id *strings* still
  resolve if anyone ever greps the whole line. This is exactly the class of
  divergence the item asked about.
- `lesson25 § Gate` resolves: `corpus/lessons/round-25.md:33` carries `## Gate`.
  `lesson21`/`lesson22` resolve as files (`corpus/lessons/round-21.md`,
  `round-22.md` exist).

## 5. What a stricter fence could verify (ranked, with expected verdict today)

1. **S-id existence** — expand `S### [–—-] S###` ranges and singles per row
   (whole row or third cell), require each id to match `^\|\s*S###\s*\|` in
   `corpus/SOURCES.md` at REV. Verdict today: green (0 undefined). Cheap, pure
   row-set arithmetic, same REV discipline as the fence.
2. **Third-cell presence/nonemptiness** — a row must have a nonempty Sources
   cell (split on `|`, require ≥4 cells and cell 4 nonblank). Verdict today:
   **red — flags `animation-table-r26.md`**. This is the highest-yield check:
   it finds a real landed divergence the current fence structurally cannot.
3. **Lesson-pointer resolution** — `lesson(\d+)` → `corpus/lessons/round-\1.md`
   exists at REV; a `§ <Anchor>` suffix requires a `## <Anchor>` heading (the
   C2 counter already implements the `lesson round<NN>` spelling,
   `count.py:47`; the row spelling `lesson25` without a space is a second
   dialect a gate must map explicitly). Verdict today: green.
4. **Recheck/registration artifact existence** — backticked paths in the Sources
   cell (`.ufo/waves/round-27/c1/count-v4.py`, `.ufo/waves/round-28/registration.md`)
   exist at REV. Same `git show REV:path` discipline as `check-index.py load_rev`.
   Verdict today: green (paths exist at tip).
5. **Link-target resolution** — `[SOURCES](SOURCES.md)` and the pre-r12
   `[Source and recheck](knowledge/<note>.md)` targets exist at REV. Green today.
6. **Evidence-path globs** — `evidence `.ufo/evidence/round-12/*.txt``, `fetch
   receipts under `.ufo/waves/round-18/fetch/``. Resolvable, but brittle: `.ufo/`
   scratch policy (the lane's open ephemeral-input preservation L0) could make
   old receipts vanish while the row stays honest. Needs a policy decision
   before gating; flagged, not recommended as a hard predicate.
7. **Table scoping** — anchor row matching to the coverage-map table (stop at
   the first blank/heading line after `| Note | Holds | Sources |`), so a stray
   `| `knowledge/…`` line elsewhere can never move the fraction. Benign today
   (43/43 row-starts are in the map), free to add.
8. **Semantic row accuracy** — row text vs note contents. Already named as
   planned debt by the lane itself (`SCORECARD.md` planned section, ~line 1936:
   "semantic index-row accuracy (row text vs note contents — the fence counts
   rows, not truth)"). Checks 1-5 are its cheap syntactic subset: they need no
   note reading and could land as `check-index.py` assertions or a sibling gate.

Design note: checks 1-5 are all implementable inside the C3 gate's existing
REV/root discipline (nothing new to trust, nothing live probed), and each is
independently killable in `--selftest` — the gate's 6/6 selftest pattern
extends naturally (one assertion per check).

## 6. Divergences and confidence

| # | Finding | Class | Confidence |
|---|---|---|---|
| D1 | Fence/gate ignore Sources cell (and Holds cell) entirely | reconstructed contract | **high** — read off both regexes and their consumers |
| D2 | `animation-table-r26` row has no Sources cell; citation stranded in Holds | live latent defect | **high** — raw line inspected (`README.md:52`) |
| D3 | "(S### queued)" annotations reference ids that exist (S132, S161) — status prose, not absence | semantic divergence | **high** — `SOURCES.md:144,173` |
| D4 | Item premise says "counter" — the regex lives in the SCORECARD fence + `quality/check-index.py`, not in `c2/count.py` | premise correction | **high** — regex inventories of all three files |
| D5 | Item said 6 historical rows; the r18–r26 band holds 9 (rounds 19 and earlier carry no rows in-band) | scope correction | **high** — row census |
| D6 | r21/r22/r23 notes predate their index rows (backfilled r24); the map ran red across round closes (r29 inherited 41/43) — fence redness was tolerated historically; C3's gate makes it continuous | historical divergence | **high** — in-row "index row added round 24" annotations; registration |
| D7 | Two regex spellings (`SCORECARD` exact `^\| ` vs `check-index.py` `\s*`-superset) — latent divergence class, not a mere spelling variance: on non-canonical bytes (0-space/tab rows) the gate can print green where the fence prints `missing=1`, and can count duplicates the fence never sees; latent only — all 43 committed rows carry the canonical `\| ` spelling | benign at `446dc396`, real on crafted bytes | **high** — both read; divergence mechanics independently confirmed by RevC1Fence (`.ufo/waves/round-30/w1/reports/RevC1Fence.md`; gate blob `df01b20f…`, fence sha `8b59b503…` both frozen) |
| D8 | Evidence-path globs in rows are durability-coupled to `.ufo/` scratch policy | [INFERENCE] risk, not observed loss | medium |

No checks were re-run to confirm tool outputs; single-pass evidence chain:
`SCORECARD.md:77-88,235-237,1914,1936` · `SOURCES.md:144,173,196-197` ·
`README.md:8-54,216-220` · `quality/check-index.py:11` ·
`c2/count.py:44-70` · `corpus/lessons/round-25.md:33` ·
`git log/status/diff --stat` (read-only).

## 7. Bounds compliance

Writes: this file only. No git/jj mutation, no sibling-lane or fleet-repo
writes, no config/compositor state touched. Installations: none.

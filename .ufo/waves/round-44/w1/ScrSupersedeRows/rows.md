# ScrSupersedeRows — closure D2: superseding rows for the S290-S297 cells round-43 w2 found imprecise

Seat `ScrSupersedeRows`, mado round 44, wave `w1`, lane `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Round-43 closure D2 (`corpus/lessons/round-43-verifier-spotcheck.md:100-101`): "S293 title 'the client's
request as input' reads as the refuted premise; supersede with the other w2-found row-cell defects
(S290-S294, S296, S297) under CORPUS rule 2."

Contract applied: `CORPUS.md:116-118` (rule 2) — "Only `status`, `recheck` and `used-by` change in place …
A correction is a new row whose `teaches` opens `supersedes S0NN —`." Census rules: `scripts/sources-census.sh:24-33`
(E04 duplicate URL+scope without a supersedes link; W04 same URL across scopes; E11 used-by path missing).

Deliverables: `rows-block.txt` (paste-ready rows + the lesson section they depend on), `rows.md` (this file),
`census-{m0..m6,lane}.txt`, `locators.txt`, `check-locators.sh`, `mirror.sh`.

## 1. Inputs read

| what | where |
|---|---|
| closure D2 and its wording | `corpus/lessons/round-43-verifier-spotcheck.md:100-101` |
| registry rows under attack | `corpus/SOURCES.md:239-246` (S290-S297) |
| round-43 w2 re-opens | `.ufo/waves/round-43/w2/ScoutRowsA/rows.md`, `ScoutRowsB/rows.md`, `ScoutRowsC/rows.md`, `ScoutRowsD.md` (one line: `status: started` — no findings) |
| pins the rows cite | `.ufo/waves/round-43/fetch/` (all eight re-hashed here, §5) |
| round-44 pin used for one cross-reference | `.ufo/waves/round-44/fetch/Hyprland-Window.cpp` (sha256 `d735d454…`, `receipts/fetch-sha256.txt:2`) |
| a supersession precedent | `corpus/lessons/round-13.md:36,39,50` + rows S042/S045 |
| census mechanics | `scripts/sources-census.sh:497-503` (`--file` → `dir`), `:560-570` (E11), `:644-649` (W04/E04) |

`ScoutRowsD` produced no report (`status: started` only), which is where the closure's S296/S297 cover would
have come from; §2 records what that gap means for the two own-work rows.

## 2. What w2 actually found, row by row

| row | cell w2 attacked | finding (locator in the w2 report) | verb |
|---|---|---|---|
| S290 | `scope`, `teaches` | scope names the "host `match:class` regex" but the class→engine link is `Rule.cpp:52,98` + `WindowRule.cpp:395-396`, unpinned; teaches quotes the host pattern text, which is S295 (`ScoutRowsA/rows.md:18,20`) | NEEDS-NARROWING (minor) |
| S291 | `source` (title), `teaches` | title "who consumes a size rule" ignores the tiled consumer at `Window.cpp:2402-2410`; teaches drops the parse gate, the two center conditions and the downstream clamp (`ScoutRowsA/rows.md:36,40`) | OVERSTATED |
| S292 | `teaches` | last clause "so the geometry a window reports is a value the layout wrote" is a three-row inference the file does not show (`ScoutRowsB/rows.md:23`) | PARTIAL |
| S293 | `source` (title), `teaches` | title echoes the refuted request premise; teaches misses `width <= 2 \|\| height <= 2`, the `> 5` gate on the surface fallback, the 600x400/error returns and the stored-size override (`ScoutRowsB/rows.md:49,59`) | PARTIAL, closure D2 names it |
| S294 | `teaches` tail | "can differ from what is on screen" is an inference, not in the file (`ScoutRowsC/rows.md:59`) | optional reword |
| S296 | — | **no w2 finding exists** (`ScoutRowsD.md` = `status: started`; `CritEntryOverreach/findings.md:46` calls S296 "SUPPORTED") | none from w2 |
| S297 | — | same: no w2 finding (`CritEntryOverreach/findings.md:45` "SUPPORTED") | none from w2 |

For S296/S297 I did not inherit a defect, so I re-opened both pins myself and the defects below are my own,
each attacked against the row's own source (they are listed with their evidence in §3, rows S307/S308):

- **S296**: the pinned dump is reduced to `address, mapped, class, floating, size, at, monitor`
  (`host-clients-r43.json:1-62`), so it carries no `fullscreen` value (`grep -c fullscreen` = **0**) — the
  teaches word "tiled" is not decidable from the row's own source; and "a window that was never mapped"
  is not what a snapshot shows (`absent from this dump` ≠ `never mapped`). The row's scope itself is right:
  "Which windows the dump held when it was taken".
- **S297**: the excerpt carries a two-line provenance header (`gkeep-ui-excerpt.py:1-2`), so the row's
  `:6`/`:33` are **excerpt-relative**: they are `ui.py:449` and `ui.py:476` (computed, §5). The teaches
  "asks for the same 420 500" overstates `set_default_size`, which is a default and not a size request —
  the excerpt carries **0** `set_size_request` calls.

## 3. Decision per row

Seven successors, ids provisional **S302-S308** in file order (the round reserves S298-S301 for its own
pin rows, `registration.md` § pre-wave fetches; final ids are assigned by document at the data commit).

Scope wording drives the census answer to "can this supersede without an E04?":

- **E04** fires only when URL *and* scope text are both repeated and the new `teaches` lacks
  `supersedes S[0-9]{3}` (`scripts/sources-census.sh:646-649`). Keeping the scope cell verbatim therefore
  needs *no* exception: the supersedes opener is the exemption.
- **Changing** the scope text moves the row into the *across-scopes* branch instead, which prints **W04**
  (`:644-645`) — a warning, not an error, but new census noise.

| new | supersedes | cells corrected | scope cell | measured census effect (m2 mirror) |
|---|---|---|---|---|
| S302 | S290 | `teaches` (class→engine binding named as unpinned; host pattern attributed to S295), anchor cross-reference added | verbatim | none |
| S303 | S291 | `source` title narrowed to the floating path; `teaches` (parse gate `:57-58`, center `:79-84, :90-91`, re-center `:93-102`, clamp is S293, tiled consumer `Window.cpp:2402-2409`); anchor cross-reference added | verbatim | none |
| S304 | S292 | `teaches` (the reported-geometry clause replaced by the file's own limit) | verbatim | none |
| S305 | S293 | `source` title (no request premise); `teaches` (both sides at `:339`, `> 5` at `:342`, 600x400 at `:354`, error at `:364`, stored size at `:323-326`, clamp `:297-304`); anchor extended with `:323-326` and `:339-365` | verbatim | none |
| S306 | S294 | `teaches` (retained inference dropped; "the file does not say what is drawn") | verbatim | none |
| S307 | S296 | `scope` (adds "which fields it kept"), `teaches` (reduced fields, no `fullscreen`, absence ≠ never mapped), anchor note | narrowed | none — own-work rows carry no URL, so W04/E04 cannot fire |
| S308 | S297 | `source` title ("declaration", not "request"), `anchor` (excerpt-relative locators mapped to `ui.py:449`/`:476`, `set_size_request` count), `teaches` (default size, no size request) | narrowed | none — own-work, no URL |

The alternative for S302 — narrowing the scope to "The test a window-rule regex string is put through" —
was measured too (mirror m3): **W04 ×1** extra, `S302 duplicate url …RegexMatchEngine.cpp across scopes`.
I recommend against it: the scope claim is *true upstream* (`Rule.cpp:52,98` binds `class` to this engine)
and only *unpinned in the lane*, so the honest correction is the `teaches`/anchor wording, which costs no
census finding. The same reasoning keeps S293's scope cell ("derives its desired geometry from the client")
— it is what `desiredGeometry()` does at `WindowTarget.cpp:310,313`; only the *title* carried the refuted
premise.

`used-by` for all seven is `corpus/lessons/round-44.md`, the document that will name the old→new mapping
(CORPUS rule 2 requires that log anyway; round-13 used the same shape for a supersession,
`corpus/lessons/round-13.md:36,39`). That makes the rows land **together with** the lesson section — see §6.

## 4. The rows

Paste-ready in `rows-block.txt` (7 rows, 11 cells each, all `mined` / `opened 2026-10-26`;
`recheck on-release` for the five upstream rows, `2027-01-24` for the two own-work rows, matching their
predecessors' cadences). Every `file:line` and every byte count/sha256 in them was recomputed by
`check-locators.sh` — `LOCATORS: checked=99 failed=0` (`locators.txt`).

## 5. Mirror census — measurements

Method: `mirror.sh` (copied here) builds a read-only copy under `/fast/scratch/hyaku/mado-r44/ScrSupersedeRows/`
of `corpus/` plus every `used-by` path the registry names (265 copies, so E11 resolves exactly as in the
lane), appends the seven rows after the S297 row, and runs the fleet census. Nothing in the lane is written.

`validate` output, byte-identical to the lane's own except the path in the `ok` line (m0 vs `census-lane.txt`,
`diff` shows only that line):

```
$ scripts/sources-census.sh validate --file <m0|m2>/corpus/SOURCES.md --today 2026-10-26
file	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
file	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
file	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
file	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
file	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
file	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
file	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
file	W01	S277 tierC mined used-by=corpus/knowledge/request-socket-live-bound-r8.md
file	ok	<mirror>/corpus/SOURCES.md
```

Seven variants, all run:

| id | what it is | E | W | E04 | W04 | E11 | W03 | exit |
|---|---|---|---|---|---|---|---|---|
| lane | the lane's real `corpus/SOURCES.md` | 0 | 8 | 0 | 7 | 0 | 0 | 0 |
| m0 | mirror, no rows (control: reproduces `lane`) | 0 | 8 | 0 | 7 | 0 | 0 | 0 |
| m1 | rows, **no** `corpus/lessons/round-44.md` | **7** | 8 | 0 | 7 | **7** | 0 | 1 |
| m2 | rows + lesson stub naming all seven ids | 0 | 8 | **0** | **7** | 0 | 0 | **0** |
| m3 | m2 with S302's scope narrowed | 0 | 9 | 0 | **8** | 0 | 0 | 0 |
| m4 | m2 mutant: S304's `supersedes S292 —` opener deleted | **1** | 8 | **1** | 7 | 0 | 0 | 1 |
| m5 | m2 with `used-by` = `—` | 0 | **15** | 0 | 7 | 0 | **7** | 0 |
| m6 | m2 with `used-by` = `corpus/knowledge/hyprland-gkeep-geometry-r43.md` | 0 | 8 | 0 | 7 | 0 | 0 | 0 |

Readings, each against the output above:

- **Supersession is possible without an E04** — m2: E04 = 0 and no new warning. The exemption is
  load-bearing, not incidental: m4 deletes one opener and the census raises
  `E04 S304 duplicate url …/src/layout/target/Target.cpp within scope The base target's box store and its remembered floating size`.
- **The rows are not landable alone** — m1: `E11 S302 … S308 missing used-by corpus/lessons/round-44.md`
  (E11 splits the cell on commas only, `sources-census.sh:562`). The lesson section is a hard dependency.
- `used-by = —` is landable but scores seven `W03 … mined but unused` (m5): worse than m2, and untrue —
  the round lesson does record the change.
- m6 is census-clean but honest only if the round-43 entry itself comes to name S302-S308; nothing in this
  seat may edit that entry, so m2 is the shape I hand over.
- Row count 234 → 241 in the m2 mirror (`sources-census.sh census --file …` → `file rows 241`); no gate tool
  hard-codes 234 (`grep -rn '\b234\b' quality/*.py corpus/README.md PROVINCE.md SKILL.md` → one unrelated
  hit, `SKILL.md:308`).

Pin and locator receipt (`locators.txt`, `LOCATORS: checked=99 failed=0`): all eight round-43 pins re-hashed
to the values the rows cite (`RegexMatchEngine.cpp` 470 B `8ca65533…`, `DefaultFloatingAlgorithm.cpp` 10359 B
`f05f2561…`, `Target.cpp` 3064 B `49323833…`, `WindowTarget.cpp` 16614 B `8bcaf370…`,
`GeometricMovableAnimated.cpp` 1576 B `649f1a8d…`, `host-clients-r43.json` 711 B `21db902e…`,
`gkeep-ui-excerpt.py` 1625 B `3695b788…`, and the round-44 `Hyprland-Window.cpp` `d735d454…`), the excerpt is
byte-equal to `ui.py:446-488` (`cmp`), and the full-file gkeep hash is `07a3c4a5…`.

## 6. Integration steps for the L1 (in this order)

1. Append the seven rows from `rows-block.txt` after `corpus/SOURCES.md:246` (the S297 row ends the
   `## Registry` table; `:248` is `## Paths`). Ids S302-S308 are provisional — assign by document if the
   round's own pin rows take S298-S301 differently.
2. Write the round-44 lesson section in the same commit **and name all seven ids in it** — use the block at
   the foot of `rows-block.txt`. Without it the census returns E11 ×7 (m1).
3. Re-run `cd /home/vgpnk/Projects/shokunin && scripts/sources-census.sh validate --root . mado` (or
   `--file <lane>/corpus/SOURCES.md`) and hold it at the m2 shape: `W04 ×7 + W01 S277`, `ok`, exit 0.
4. Do **not** re-point the round-43 entry's `source:` lines at S302-S308 without also extending the lesson
   `## Gate` with `GATE <id> receipt=… sha256=… quote=…` lines and a per-id quote line in the entry:
   `quality/counters/c2-r44-gkeep-size-request.py:449-450` iterates the *cited* ids only, so the added rows
   are invisible to it while they stay uncited, and every cited id costs clause d and clause g work. The
   round-13 shape (supersede, keep the old row's citations, log old→new in the lesson) is the cheap one and
   is what the rows are written for.
5. If the operator prefers a zero-warning landing, m3 shows the price of rewriting S302's scope cell: one
   extra `W04`. It buys nothing the `teaches` correction does not already carry.

## 7. Findings

1. **Attacks closure D2's list**: it names S296 and S297, but round-43 w2 left no finding for either —
   `ScoutRowsD.md` holds one line (`status: started`) and both w2 seats that touched the ids call them
   SUPPORTED (`CritEntryOverreach/findings.md:45-46`). The closure's list is therefore wider than the w2
   evidence; the defects this seat writes for S307/S308 are its own re-open (§3) and are offered as
   grounded, not as inherited. If the L1 wants D2 answered strictly, S290-S294 alone suffice.
2. **Supports the closure on S293** (the named case): the title is the cell that carries the refuted premise,
   and the teaches omits four source conditions (`WindowTarget.cpp:323-326,339,342,350-364`). Both are now
   corrected in S305.
3. **A supersession of a URL-bearing row costs nothing extra** when the scope cell is kept verbatim (m2 vs
   m0): the census exemption lives in the `teaches` opener, not in the scope. This is a fact about the census
   as written (`scripts/sources-census.sh:646-649`), measured, and it contradicts the natural reading that a
   duplicate URL always trips E04.
4. **The round-43 entry repeats two of the corrected imprecisions** outside any row:
   `corpus/knowledge/hyprland-gkeep-geometry-r43.md:62` ("the app asks for the same size the rule asks for")
   and `:70` ("holds four mapped clients and none is floating"). Those are entry cells, not registry cells;
   they are not mine to edit and are routed here for the closure (an erratum at the entry would need its own
   append-only note, or C2's round-44 entry is where the corrected reading lands).
5. **S296's anchor is exactly right about what it says** (`:2,17,32,47` are the four object lines; each
   `mapped: true`, `floating: false`, `size 1720 1414`; no `gkeep` token) — the defect is what the *teaches*
   builds on it, not the locators. Same for S297's `:6`/`:33`, which land in the excerpt; the defect is that
   the cell does not say `excerpt-relative`, and a reader who maps them onto `ui.py` lands two lines off.
6. **The two own-work rows are immune to E04/W04 by construction**: the census derives `url_of(source)` from
   the source cell and these cells hold lane paths (`scripts/sources-census.sh:600-604`), so their scope cells
   could be narrowed for free — which is why S307/S308 narrow theirs.

## 8. Limits (declared, not fixed)

- The census was run on **mirror copies**, not on a lane commit. The rows are not landed by this seat; a
  live run at the data commit is the L1's step (§6.3) and has not happened.
- The lesson section I hand over is a **stub shape**, not the round's lesson. Its wording is mine; the L1
  owns the real `## Registry changes logged old→new` table and the rest of the lesson.
- The C2 counter was **not executed** against a mirror: its entry does not exist yet, so clause a fails at
  `--rev` regardless. [INFERENCE] The seven rows cannot move it while they stay uncited: clauses c, d, e, g
  and i all iterate `for i in ids` (`quality/counters/c2-r44-gkeep-size-request.py:449`) over the entry's
  cited ids. This is a reading of that code, not a run.
- Whether a superseded row should also change `status` of the old row is **not** touched here: CORPUS lets
  `status` change in place, but no reason exists to reject or requeue S290-S297 — they are accurate about
  their pins; only the wording was imprecise.
- Ids S302-S308 are provisional. If the round's pin rows land as S298-S301 the numbering holds; if they land
  differently, renumber by document before committing.
- I read the package only through the round-43/44 receipts and the lane; no shokuknow file was opened by
  this seat (nothing here needed the staged residue).

## 9. Receipts in this seat directory

- `rows-block.txt` — the seven rows + the lesson section they depend on.
- `census-lane.txt`, `census-m0.txt` … `census-m6.txt` — the eight census runs pasted in §5.
- `locators.txt` — `LOCATORS: checked=99 failed=0` (pin hashes, byte counts, every `file:line` in the rows,
  the excerpt↔`ui.py` mapping).
- `opener-check.txt` — the seven `teaches` openers as the census regex reads them (`supersedes S290 … S297`).
- `check-locators.sh`, `mirror.sh` — the two scripts, re-runnable as written.

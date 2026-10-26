# ScrEntryA - the C2 entry, drafted chain-first

Seat: `ScrEntryA` (w1, round 43). Status: **complete** - draft + quotes + proposals written into
the seat dir; no frozen file edited, no `corpus/` write, nothing scored.

## Behavior (what the draft says)

`hyprland-gkeep-geometry-r43.md` is a 115-line entry in the lane's shape: title, ten `source:`
lines, one `verified-at`, one `recheck`, `ground`, `assimilated-from`, `Lane:`, then eight body
sections in the order the task fixed - (1) host rule text, (2) match, (3) effects, (4) consumption,
(5) storage and configure, (6) the reported variable, (7) the client's request, (8) what is and is
not observed - a twelve-row decision table, and a §10 limits block. Every one of S290-S299 has
exactly one claim line that names only that id, carries its Gate quote verbatim and the computed
locator `<receipt file>:<start line>`. The three census lines sit on their own lines, outside
fences, once each. The observed size of a gkeep window is stated as UNK, and §10 says in words
that no window was ever observed at 420×500.

Chain as drafted: the host declares float + centre + `size 420 500` for `^(org.omarchy.gkeep)$`
(S297) → `match:class` is an anchored `RE2::FullMatch` (S290) → the applicator stores the size as a
`SExpressionVec2` in `static_.size`, reset every pre-read (S291) → the floating algorithm is the
only consumer, at first map only (S292) → the box lands on the target (S293) and on the window,
with one `sendWindowSize` to the client (S294) → `size(GEOMETRIC_GOAL)` is the animation goal
(S295) → `hyprctl clients -j` prints that goal (S296) → the client asks GTK for 420×500 under the
same app id (S299) → today's census holds no such client (S298). The configure body, the matched
string's origin, and the rendered size are the three named holes.

## Verification actually run

Reads (read-only, all pinned receipts re-opened before quoting): registration, PRED-C2-r43
docstring + scoring code, `hyprland-focus-grab-r41.md`, `corpus/SOURCES.md` row shape,
`corpus/README.md` row shape, the ten `fetch/` receipts.

1. Quote extraction is mechanical, not typed: each quote is the collapsed text of a line span of
   the pinned receipt, then checked with the counter's own `quote_at` (word boundaries, first
   occurrence line) and against every other cited receipt. Result: 10/10 quotes 5-19 words, first
   occurrence at 16 / 423 / 55 / 10 / 70 / 17 / 427 / 2 / 4 / 31, zero cross-receipt occurrences
   (`checks.txt`).
2. Header (clause b): 10 distinct `source:` ids inside raw lines 1-15, `verified-at` × 1,
   `recheck:` × 1, zero such lines after line 20, zero ghost `S###` tokens, zero fences.
3. Clause g: for each id exactly one entry line names only that id, contains the quote and the
   `basename:N` locator; `N` is the line the quote starts on.
4. Clause h: `host_census` (the counter's own function) over my proposed rows, gates and receipts
   returns `True` with the three exact lines; each occurs once as a line of its own.
5. Clause d, piecewise: all ten receipts are byte-equal to `PINS` (sha256 recomputed), ≥ 264 B,
   and mode `100644` at the freeze commit `b2e2efd` (`git ls-tree -r b2e2efd -- .ufo/waves/round-43/fetch`
   lists all ten as `100644`).
6. Clauses c/e/f/i at proposal level: 10 rows × 11 cells, status `mined`, opened `2026-10-26`,
   location last component contained in the receipt basename, locations unique, used-by lists the
   entry path; the README row matches the counter's prefix once; `ADMIT`/`REFUSE` match their
   regexes with staged basenames in `STAGED` and no `BAD_LOC` marker in any row.
7. Clause a precondition: `git ls-tree a35cfdf -- corpus/knowledge/hyprland-gkeep-geometry-r43.md`
   prints nothing (entry absent at base); `grep -c hyprland-gkeep-geometry-r43 corpus/README.md` = 0.
8. Line claims verified against the receipt bytes: `WINDOW_RULE_EFFECT_SIZE` occurs exactly once
   (line 421, static switch) so the "no dynamic size case" INF holds; `sendWindowSize` occurs at
   74, 110, 133 and 256, matching the floating/fullscreen/tiled split the entry states.

**Not run, and why:** `quality/counters/c2-r43-gkeep-entry.py --repo . --rev <rev>` itself. It reads
committed revisions and I may not commit; my draft is uncommitted and the registry, README and
lesson artifacts are proposals, not landed files. `checks.txt` is explicitly labelled a
helper-level simulation and **not** a score; the only `PRED-C2-r43: admitted=…` line will be the
L1's.

## Gates

| clause | state in this seat |
|---|---|
| a entry absent at base | pre-verified by `git ls-tree` (draft present only in seat dir) |
| b header window | PASS |
| c registry rows | PASS at proposal level (10 rows, 11 cells each) |
| d Gate lines / pins | PASS piecewise; the lesson itself is the L1's file |
| e location ↔ receipt name | PASS |
| f README index row | PASS at proposal level (1 match) |
| g one claim line per id | PASS (10/10) |
| h host census | PASS (`host_census` true) |
| i ADMIT/REFUSE | PASS at proposal level |
| score | **not run** - needs the L1's commit |

## Touched surfaces

- Written, this seat dir only: `.ufo/waves/round-43/w1/ScrEntryA/{hyprland-gkeep-geometry-r43.md,
  quotes.tsv, gate-lines.txt, registry-rows.md, readme-row.md, admit-refuse.txt, checks.txt}` and
  this report.
- Read-only elsewhere: the lane's frozen counters/controls/registration/fetch receipts, prior
  knowledge entries, `corpus/SOURCES.md`, `corpus/README.md`, and the read-only staged package
  `/home/vgpnk/Projects/shokuknow/merge/mado/` (bytes only).
- No edit to any tracked file (`git status --porcelain -- corpus/ quality/ .ufo/waves/round-43/fetch
  .ufo/waves/round-43/registration.md` is empty). No git/jj mutation, no counter or control run, no
  `hyprctl` call of any kind, no compositor contact, no package install, no scratch tree left on
  disk (removed before this report).

## Findings

1. **Clause g binds the first occurrence, not the only one.** S296's quoted text also occurs 20
   lines later in the text-format branch (`Hyprland-HyprCtl.cpp:447-449`); the counter's
   `quote_at` returns 427 and the entry cites 427. A verifier "correcting" that locator to 448
   would fail clause g.
2. **Round-42's routed HyprCtl locator defect is re-derived here.** The round-42 prose said
   `:394-395,412-413`; in this receipt the JSON arguments are at `:426-428` and the text branch at
   `:446-448`. The entry uses the re-derived numbers, not the old prose.
3. **Clause h couples three things that cannot drift.** It needs exactly three new `own-work` rows,
   and their basenames must be `host-gkeep.conf`, `host-clients-r43.json`, `gkeep-ui-excerpt.py`;
   the other seven new rows must be any other kind (`code` here). Its config parser needs exactly
   one `size`, one `float` and one `center` rule with the same `match:class` token on one line each
   (the conf's comment line is invisible to it); its client parser counts `mapped is not False`;
   its excerpt parser needs exactly one `set_default_size` and one `application_id="…"`.
4. **Clause e makes the registry row's last whitespace token load-bearing.** Cell 1 must end in the
   URL or fetch path, because the counter takes `split()[-1]` and compares its last path component
   with the receipt basename. `registry-rows.md` is shaped for that; a row whose cell 1 ends in a
   prose word fails silently with `ok=0`.
5. **`assimilated-from` names no id on purpose.** The staged chain file is not a pinned receipt of
   this wave, so giving it a row id would create a ghost `S###` token (clause b) and an unpinnable
   Gate (clause d).
6. **The staged theme's own sources are not citable here.** The round-9-14 staged files carry their
   own `S2xx` ids against `lanes/mado/...` artifacts this round did not re-fetch; the entry cites
   only this wave's pins, which is why the ADMIT is a provenance line and not a citation.
7. **REFUSE target.** `gkeep-rendered-geometry-record-r14.md` is refused not for being wrong but
   for being unverifiable here: its whole-journal sweep receipt is a staged `lanes/mado` artifact,
   neither re-fetched nor pinned, and its absence claim would have to be re-measured to be cited.

## Reserved for the L1 (proposals, not landed)

`gate-lines.txt` (exact `GATE` lines, one per id, column 0, pin-equal), `registry-rows.md` (S290-S299),
`readme-row.md`, `admit-refuse.txt` (ADMIT `gkeep-rendered-geometry-chain-r9.md`, REFUSE
`gkeep-rendered-geometry-record-r14.md`). The lesson `corpus/lessons/round-43.md` must carry the
`## Gate` section those lines belong to, plus the entry path in each row's used-by cell, before the
counter can be run.

## Artifact paths

- Entry draft: `.ufo/waves/round-43/w1/ScrEntryA/hyprland-gkeep-geometry-r43.md`
- Quotes: `.ufo/waves/round-43/w1/ScrEntryA/quotes.tsv` (id, quote, file, line, sha256)
- Gate lines: `.ufo/waves/round-43/w1/ScrEntryA/gate-lines.txt`
- Registry rows: `.ufo/waves/round-43/w1/ScrEntryA/registry-rows.md`
- README row: `.ufo/waves/round-43/w1/ScrEntryA/readme-row.md` - **superseded**; seat
  `ScrSkillProvince` owns the row (`.ufo/waves/round-43/w1/ScrSkillProvince/readme-row.md`) and my
  file is now a note pointing at it (clause f admits one row, so two drafts must not both land).
- ADMIT/REFUSE: `.ufo/waves/round-43/w1/ScrEntryA/admit-refuse.txt`
- Checks: `.ufo/waves/round-43/w1/ScrEntryA/checks.txt`
- This report: `.ufo/waves/round-43/w1/ScrEntryA.md`

## Peer correction (IRC, `ScrSkillProvince`, 2026-10-26)

The README-row seat reported two facts about `quality/check-index-rows.py` and its own drafted row.
Both were acted on, and two constraints went back.

- **`holds-no-overlap` silenced from this side.** The row's Holds cell opens "What determines the
  size of the host's gkeep window, end to end:". The entry's `ground:` line now opens with the same
  sequence (lower case; the checker lower-cases both sides), so the check passes without editing the
  row. Verified with the checker's own function, not a copy of its logic:
  `overlap(entry_text, holds_cell) = True` (module loaded from `quality/check-index-rows.py`).
  Header re-checked after the edit: 116 raw lines, 10 source ids, 1 `verified-at`, 1 `recheck`,
  0 such lines after line 20, 0 ghost tokens, 0 fences, census lines still `host_census`-true and
  once each (the edit touched only `ground:`).
- **Where the row's Sources paths live.** `.ufo/waves/round-43/fetch` (tree `1251d33`) and
  `.ufo/waves/round-43/receipts/fetch-sha256.txt` (blob `b5fe1bf`) are committed at the freeze
  `b2e2efd`; the ten fetch files are `100644` there, which is also what clause d's mode test reads.
- **Constraint back, one row.** PRED-C2-r43 clause f counts rows matching
  `^\| \`knowledge/hyprland-gkeep-geometry-r43.md\`` and admits only a count of 1. My row draft is
  therefore retired in place (`readme-row.md` now says "do not land this file" and names the peer's
  file); the peer's checker-validated row is the one to insert.
- **Constraint back, the row set.** Clause c needs exactly one row per cited id, and the entry cites
  S290-S299. `ScrRowsDraft`'s `.ufo/waves/round-43/w1/ScrRowsDraft/rows-block.txt` was validated
  here against clauses c and e: 10 rows, 11 cells, `mined`, opened 2026-10-26, recheck cells
  `on-release` (seven) and `2027-01-24` (three own-work), kinds `code` x7 + `own-work` x3 with the
  three pinned basenames, used-by = the entry path, location last token contains `/` and `.`,
  basename containment true for all ten, no `BAD_LOC` marker. It keeps S291 and S296, which the
  entry needs; the held-row alternative (S155/S158 in their place) would fail clause c unless the
  entry's chain is rewritten. One nit for that file: its S297 anchor says "4 lines, 264 B" for
  `host-gkeep.conf`; 264 B is right, the file has 5 lines (four content lines plus a trailing
  blank).
- Because two row drafts now exist, `registry-rows.md` opens with a precedence note: only one set
  may be appended (clause c fails any id with `len(rows) != 1`), the peer seat's rows are the
  preferred set, and mine is a clause-valid fallback.

No frozen file was touched for any of this; the only edited artifacts are my entry (one `ground:`
line) and my own seat notes.

## Routed C1 observation (reported by `ScrSkillProvince`, re-measured here - not this claim's evidence)

The README seat reported that `tools/mado-geometry.py` in the working tree is byte-identical to the
round-42 reference control. Re-measured read-only at 2026-10-26T04:3x:

    sha256sum tools/mado-geometry.py .ufo/waves/round-42/c1/ctl-ref-tool.py.txt
    e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99  tools/mado-geometry.py
    e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99  .ufo/waves/round-42/c1/ctl-ref-tool.py.txt
    wc -l -c → 417 20507 (both); cmp → identical; git status → `?? tools/mado-geometry.py` (untracked)

Consequences, stated without adjudication: if that file is C1's deliverable at the data commit, the
tool under test is the same byte sequence as the reference the counter was calibrated against, so
"fixtures=37/37" would measure the calibration anchor rather than an independently written
instrument, and C1's before/after would be "no tool" → "the reference". It is not scored here (I ran
no C1 counter), it is not my claim's evidence, and the file may still be in flight (untracked,
mtime 04:17, after the 04:11 freeze). The C1 seats and the L1 own the question; this note exists so
the fact is on the record in a seat report rather than only in IRC.

For the same reason the C2 entry cites no tool: its evidence is the ten pinned receipts, and
`tools/mado-geometry.py` is C1's instrument, scored by C1's counter. Registration separability says
C2 never runs it, so naming it in the entry would assert a dependency the claim does not have.

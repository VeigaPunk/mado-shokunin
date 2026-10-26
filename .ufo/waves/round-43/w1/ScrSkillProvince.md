# ScrSkillProvince — SKILL.md / PROVINCE.md / corpus/README.md rows (round 43, w1)

Lane `mado-shokunin`, round 43 w1, seat `ScrSkillProvince`, 2026-10-26. Role: draft insertion text for the
round's two artifacts. **No tracked file was edited**; every draft is insertion text with its neighbouring line
numbers, and every structural claim about it is a run, not an opinion.

## Deliverables

| File | What it is |
|---|---|
| `.ufo/waves/round-43/w1/ScrSkillProvince/skill-rows.md` | three SKILL.md insertions: probe row (after line 223), decision row (after line 157), subsection `### Rule size versus reported size` (after line 243) |
| `.ufo/waves/round-43/w1/ScrSkillProvince/province-row.md` | one PROVINCE.md tool row (after line 31) |
| `.ufo/waves/round-43/w1/ScrSkillProvince/readme-row.md` | one coverage-map index row (after line 70) and one Frontier bullet (after line 291) |

Reproducible instruments in the same directory: `verify-quotes.py`, `verify-rows.py`, `simulate-integration.py`,
`run-index-evidence.py`. Receipts under `…/ScrSkillProvince/receipts/`: `geometry-host-run.txt`,
`source-quotes.txt`, `verify.txt`, `check-index-rows.txt`.

## Insertion points, with the neighbours they were checked against

| Target | Insert after | Neighbour above (verified) | Neighbour below (verified) |
|---|---|---|---|
| SKILL.md probe row | line 223 | `\| python3 tools/mado-globals.py --journal-file <journal>` … | blank 224, `### Advertised Wayland globals` 225 |
| SKILL.md decision row | line 157 | `\| Which Wayland globals the compositor advertises …` | blank 158, `### Divergence vocabulary …` 159 |
| SKILL.md subsection | line 243 | blank closing the globals subsection (225-243) | `### Mutating commands — operator only, mado never runs` 244 |
| PROVINCE.md tool row | line 31 | `\| tools/mado-globals.py \| …` (last row of the tool table) | blank 32, `**Round-23 wave-2 correction …**` 33 |
| corpus/README.md index row | line 70 | `\| knowledge/hyprland-focus-grab-r41.md \| …` (last coverage-map row) | blank 71, `## Quality bar` 72 |
| corpus/README.md Frontier bullet | line 291 | `### Round-38 request-socket bound route` (282-291, end of file) | — |

`verify-rows.py` re-reads those nine lines from the lane files and asserts each prefix, so the anchors are not
recalled from memory: `ROWS: 30/30 checks passed` (`receipts/verify.txt`).

## Gates run

| Gate | Command | Result |
|---|---|---|
| host run of the reference (sample line for the probe row) | `hyprctl clients -j \| python3 -I <scratch copy of .ufo/waves/round-42/c1/ctl-ref-tool.py.txt> --clients - --rules ~/.config/hypr/gkeep.conf` | `verdict=NO_MATCHING_CLIENT`, exit 3; scratch copy sha256 `e3c2e471…` equals the frozen reference's — `receipts/geometry-host-run.txt` |
| every quoted line re-found in its receipt | `python3 -I …/verify-quotes.py` | `QUOTES: 51/51 checks passed`, exit 0 |
| drafted table rows keep their cell count; anchors real | `python3 -I …/verify-rows.py` | `ROWS: 30/30 checks passed`, exit 0 |
| drafted README row through the lane's own gate | `python3 -I quality/check-index-rows.py --root <scratch>` | `rows=60 errors=0 warns=0`, exit 0 |
| five negative controls (same gate, mutated row) | same, in `run-index-evidence.py` | `row-cells` (empty Sources cell), `row-cells` (two cells), `cited-s-undefined` (S399), `cited-path-missing` (fetch-nope), `row-outside-map` — each `errors=1`, exit 1 |
| simulated integration of all six insertions | `python3 -I …/simulate-integration.py` | `SIM: 19/19 checks passed`; the simulated README passes the index gate with `errors=0` |

`check-index-rows.py` sha256 `2fd1c003…`; the scratch tree it read is the lane's `corpus/` copy plus symlinks to
`.ufo`, `tools`, `quality`, plus **scratch-only** registry stubs S290-S299 and a **scratch-only** stub note — the
entry seat and `ScrRowsDraft` own the real bytes. The whole sequence re-runs from
`python3 -I .ufo/waves/round-43/w1/ScrSkillProvince/run-index-evidence.py` and writes
`receipts/check-index-rows.txt`.

## Findings

1. **`tools/mado-geometry.py` is byte-identical to the round-42 reference control** — `sha256sum` of both is
   `e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99` (20,507 B, 417 lines, mtime
   2026-10-26 04:17:37), and `diff -q` reports no difference. The registration calls the reference an anchor, not
   the deliverable ("Reference control (NOT the deliverable)"), so as of this seat's read C1's tool **is** its
   anchor: the counter's `REF` run and the tool run would be the same bytes. This is a fact about the working tree,
   not a verdict — a build seat may still replace it. Flagged for the L1 and for `RevC1Counter` / `RevRefTool`; the
   drafted rows name `tools/mado-geometry.py`, so they stay correct either way. `ScrEntryA` re-measured the same
   hashes independently (`cmp` clean, untracked, mtime 04:17 after the 04:11 freeze) and records it as a routed C1
   observation; it deliberately keeps the tool out of the C2 entry (separability, and a tool path has no pinned
   receipt), which is why the **Frontier bullet** — not the entry — is where this seat names the instrument.
   Receipt: `receipts/verify.txt` (`git status` shows the file untracked) plus the `sha256sum`/`diff` pair above.
2. **The README row's Sources cell depends on the registry append.** It lists S290-S299 explicitly because the
   checker resolves every `S###` token; `ScrRowsDraft` confirmed (2026-10-26) that all ten are drafted and
   census-validated at `.ufo/waves/round-43/w1/ScrRowsDraft/rows-block.txt`. That seat's commit-form alternative
   (drop `S291`/`S296`, cite held `S155`/`S158`) is **withdrawn**, and the reason is worth stating precisely, because
   it is not clause c: clause c is per cited id and a BASE id only has to keep every BASE used-by item
   (`quality/counters/c2-r43-gkeep-entry.py:30-35`), so a held id passes it mechanically once its used-by cell gains
   the entry path. Nor is the receipt the blocker: clause d scopes PIN-membership to a **new** id ("for a NEW id the
   receipt's file name and sha256 must be one of the PINS", `:41-42`), while the receipt requirement itself stands for
   every cited id — and both receipts are already committed in this round's fetch dir at the pinned bytes
   (`Hyprland-WindowRuleApplicator.cpp` 27,092 B `fec33f9a…`, `Hyprland-HyprCtl.cpp` 97,582 B `798b7c6c…`, both
   mode 100644 at `b2e2efd`; re-measured, `receipts/verify.txt`). The real cost is therefore two `GATE` lines whose
   quotes are distinct from each other **and** from every other cited id's (`:36-42`), plus the lockstep rewrite of
   the entry's ids and Gate lines and two used-by cell edits. The ten-id cell stands as written (control M3 shows a
   missing id fails closed with `cited-s-undefined`). The two **paths** the cell cites
   need no such care: `git ls-tree -r --name-only b2e2efd -- .ufo/waves/round-43/fetch .ufo/waves/round-43/receipts`
   lists every fetch file and `receipts/fetch-sha256.txt`, so `cited-path-missing` cannot fire for them at any later
   REV (`receipts/verify.txt`).
3. **`warns=0` on the index row is conditional on the landed note's wording.** `check-index-rows.py` emits
   `WARN holds-no-overlap` when the Holds cell shares no ≥5-word sequence with the note's bytes; it never affects
   the exit code. The drafted Holds cell opens with "What determines the size of the host's gkeep window, end to
   end:". **Confirmed by both entry seats (2026-10-26):** `ScrEntryB`'s entry title is byte-identical to that lead
   sequence, and `ScrEntryA` reports running the checker's own `overlap(entry_text, holds_cell)` → `True` on its
   `ground:` line. Recheck at the data commit:
   `python3 -I quality/check-index-rows.py --repo . --rev <data-commit>`.
4. **The probe row's command cell needs `\|`.** A markdown table splits on an unescaped `|` even inside a code
   span, so `hyprctl clients -j | python3 …` would have produced a four-cell row in a three-cell table.
   `verify-rows.py` asserts the escape and the cell count (segments = 5 for a 3-cell row).
5. **The host sample is a null observation, and the subsection says so.** On 2026-10-26 the gkeep rule file declares
   `size 420 500` and the dump holds four tiled clients, so the run is `NO_MATCHING_CLIENT` (rc 3) — the row and
   the subsection both state that this is not "the rule works". What a live gkeep window reports needs the window
   open, which is an operator act.
6. **The verdict licences are drawn from the pinned bytes, not from the tool's prose**: `clients` prints
   `w->size(…GEOMETRIC_GOAL)` (`Hyprland-HyprCtl.cpp:395,427-428,448,2007`), `GEOMETRIC_GOAL` is
   `m_realSize->goal()` against `GEOMETRIC_CURRENT` = `m_realSize->value()` (`…GeometricMovableAnimated.cpp:19-20`),
   the floating algorithm reads `static_.size` on first map (`…DefaultFloatingAlgorithm.cpp:49,55-56`), the
   applicator stores the expression (`…WindowRuleApplicator.cpp:426`) and matching is `re2::RE2::FullMatch`
   (`…RegexMatchEngine.cpp:7-8,16`). All eleven quotes are ≤25 words, located, and re-found by
   `verify-quotes.py` against `receipts/source-quotes.txt`.
7. **Wrong locator routed to the registry seat, now fixed (re-verified here).** `ScrRowsDraft`'s draft row for `S297`
   said "4 lines, 264 B" for `host-gkeep.conf`; the receipt is **5** lines at 264 B (`wc -l -c` → `5 264`, `od -c`
   ends `) $ \n \n`: four content lines plus one trailing blank). `ScrEntryA` raised the same nit independently.
   The seat has since corrected it and its own `S298` range: `.ufo/waves/round-43/w1/ScrRowsDraft/rows-block.txt` is
   now 9152 B, sha256 `2719d5823da4df6fb0f4793b5e85b4d429bddc4c9ff1032ad7e234f6a5087223`, its S297 anchor reads
   "5 lines (4 content plus an empty line 5, wc -l -c reports 5 264), 264 B", its locators `:2 float on, :3 center on,
   :4 size 420 500` match the file's line order, and the block still carries exactly ten rows S290-S299 (re-measured
   here, `receipts/verify.txt`). My own row makes no line-count claim about that file.

## Touched surfaces

- Written: `.ufo/waves/round-43/w1/ScrSkillProvince/` only (three drafts, four instruments, four receipts) and this
  report. Messages sent to `ScrEntryA`, `ScrEntryB`, `ScrRowsDraft` (coordination only).
- Read-only: `SKILL.md` (`8264434c…`), `PROVINCE.md` (`372b93f9…`), `corpus/README.md` (`53aa91cd…`),
  `corpus/SOURCES.md`, `quality/check-index-rows.py`, `quality/counters/c1-r42-geometry.py`,
  `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt`, `.ufo/waves/round-43/{registration.md,fetch/*,receipts/*}`,
  `hyprctl version`, `hyprctl clients -j`, `~/.config/hypr/gkeep.conf`.
- `git status --porcelain=v1 -- SKILL.md PROVINCE.md corpus/ tools/` reports only `?? tools/mado-geometry.py`,
  which this seat did not create (`receipts/verify.txt`).

## Out of scope (not done, by design)

- No edit to `SKILL.md`, `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` or any frozen instrument; the L1
  integrates.
- The registry rows S290-S299 (`ScrRowsDraft`) and the entry note (`ScrEntryA`/`ScrEntryB`) are other seats'; my
  row cites them, and the scratch stubs exist only to exercise the gate.
- No lesson text, no `LOG.md`/`SCORECARD.md` entry, no commit, no judgement of C1/C2.
- No package transaction, no compositor mutation, no Wayland client of my own; the only compositor reads were
  `hyprctl version` and `hyprctl clients -j`.

## Tooling

None installed. Scratch `/fast/scratch/hyaku/mado-r43/ScrSkillProvince/` removed at the end of the seat.

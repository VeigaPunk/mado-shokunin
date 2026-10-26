# ScrSupersedeRows — round 44 w1 report

Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, base/freeze `e2289516a9a857f55cda7be635933e89b931c3da`.
Target: closure D2 (`corpus/lessons/round-43-verifier-spotcheck.md:100-101`) — draft the superseding registry rows
for the cells round-43 `w2` found imprecise, decide per row whether supersession passes the census without an
E04, and mirror-validate.

## Behaviour

Seven superseding rows drafted (provisional `S302`-`S308`, one per predecessor, `teaches` opening
`supersedes S29N —` per `CORPUS.md:116-118`), grounded cell by cell in the round-43 pins and re-verified by
script:

| new | supersedes | corrected cells | scope cell |
|---|---|---|---|
| S302 | S290 | `teaches` (class→engine binding unpinned; host pattern text is S295), anchor cross-ref | verbatim |
| S303 | S291 | title → floating path only; `teaches` (parse gate, center conditions, re-center, later clamp is S293, tiled consumer `Window.cpp:2402-2409`) | verbatim |
| S304 | S292 | `teaches` (reported-geometry clause replaced by the file's own limit) | verbatim |
| S305 | S293 | title (request premise removed); `teaches` (both sides `:339`, `>5` `:342`, 600x400/error `:350-364`, stored size `:323-326`); anchor extended | verbatim |
| S306 | S294 | `teaches` tail (retained inference dropped) | verbatim |
| S307 | S296 | scope + `teaches` (reduced dump has no `fullscreen`, absence ≠ "never mapped") | narrowed |
| S308 | S297 | title, anchor (excerpt-rel. `:6`/`:33` = `ui.py:449`/`:476`; no `set_size_request`), `teaches` (default size, not a request) | narrowed |

`used-by` is `corpus/lessons/round-44.md` for all seven, i.e. the rows land with the round lesson's
registry-changes table — that block is at the foot of `rows-block.txt`.

## Gates

Census (`scripts/sources-census.sh validate --file …`, read-only mirrors of the lane's `corpus/` + the 265
`used-by` paths the registry names):

| variant | E | W | E04 | W04 | E11 | W03 | exit |
|---|---|---|---|---|---|---|---|
| lane (real file) | 0 | 8 | 0 | 7 | 0 | 0 | 0 |
| m0 mirror, no rows (control, reproduces lane) | 0 | 8 | 0 | 7 | 0 | 0 | 0 |
| m1 rows without the lesson → **`E11 S302…S308`** | 7 | 8 | 0 | 7 | 7 | 0 | 1 |
| **m2 rows + lesson stub = recommended landing** | 0 | 8 | **0** | **7** | 0 | 0 | **0** |
| m3 m2 with S302 scope narrowed | 0 | 9 | 0 | 8 | 0 | 0 | 0 |
| m4 mutant: S304 opener deleted → `E04 S304 …` | 1 | 8 | 1 | 7 | 0 | 0 | 1 |
| m5 `used-by = —` | 0 | 15 | 0 | 7 | 0 | 7 | 0 |
| m6 `used-by =` round-43 entry | 0 | 8 | 0 | 7 | 0 | 0 | 0 |

Answer to the census question: **supersession passes with no E04 and no new warning when the scope cell is
kept verbatim** (m2); the exemption is the `supersedes S29N` opener, and m4 shows it is load-bearing.
Changing a scope cell costs exactly one `W04` (m3). Own-work rows S307/S308 cannot trip E04/W04 at all
(no URL in their source cell, `sources-census.sh:600-605`).

Other gates: `check-locators.sh` → `LOCATORS: checked=99 failed=0` (all eight pins re-hashed, every
`file:line` in the rows recomputed, excerpt byte-equal to `ui.py:446-488`). Row count in the m2 mirror
234 → 241; no gate tool hard-codes 234.

## Touched surfaces

Wrote only inside the lane, only under my seat:
`.ufo/waves/round-44/w1/ScrSupersedeRows.md` (this report) and
`.ufo/waves/round-44/w1/ScrSupersedeRows/{rows.md,rows-block.txt,check-locators.sh,mirror.sh,locators.txt,census-lane.txt,census-m0..m6.txt}`.
No tracked file edited; `git status --porcelain` shows only untracked round-44 `.ufo` paths. Scratch
`/fast/scratch/hyaku/mado-r44/ScrSupersedeRows/` deleted. Nothing executed against the host compositor;
no package operation; no tool installed.

## Out of scope / not done

- Rows not landed (the L1 integrates); census therefore ran on mirror copies, not on a lane commit.
- The round-44 lesson section is a stub shape handed over for the L1 to own.
- `quality/counters/c2-r44-gkeep-size-request.py` was not executed (its entry does not exist yet, clause a
  fails at any rev). [INFERENCE] The rows cannot move it while uncited: clauses c/d/e/g/i iterate the entry's
  cited ids (`…:449`).
- The round-43 entry's own repeats of two corrected imprecisions (`hyprland-gkeep-geometry-r43.md:62,:70`)
  are routed, not edited.

## Findings

1. **Attacks D2's scope:** the closure lists S296/S297, but round-43 `w2` left no finding for either —
   `ScoutRowsD.md` is one line (`status: started`) and the seats that touched them record SUPPORTED
   (`CritEntryOverreach/findings.md:45-46`). The S307/S308 defects are this seat's own re-open (fullscreen
   field absent from the reduced dump; excerpt-relative locators; `set_default_size` ≠ a size request), each
   grounded and scripted. Strictly, S290-S294 answer D2.
2. **Supports D2 on S293:** the title is the refuted premise and the `teaches` omits four source conditions;
   both corrected in S305 with computed locators.
3. **A superseding row costs no census finding** when its scope cell is kept verbatim — measured (m2 vs m0),
   contradicting the natural reading that a repeated URL always trips E04.
4. **S296/S297 anchor locators are right; their `teaches` were not** — `:2,17,32,47` are the four object
   lines and S297's `:6`/`:33` land in the excerpt, but the cell never says excerpt-relative, and a reader
   mapping them onto `ui.py` is two lines off (`ui.py:449`/`:476`).

## Artifacts

- `.ufo/waves/round-44/w1/ScrSupersedeRows/rows.md` — analysis, decisions, pasted census outputs, L1 steps.
- `.ufo/waves/round-44/w1/ScrSupersedeRows/rows-block.txt` — the seven rows + the lesson section they need.
- `.ufo/waves/round-44/w1/ScrSupersedeRows/{census-*.txt,locators.txt,check-locators.sh,mirror.sh}` — receipts.

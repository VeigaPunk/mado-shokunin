# ScrSkillProvince — round 44 w1 seat report

**Assignment.** Draft the SKILL.md / PROVINCE.md / corpus/README.md rows for C1 (geometry state
verdicts) and C2 (`corpus/knowledge/hyprland-gkeep-size-request-r44.md`) plus the closure-D3
correction, with exact insertion text and neighbouring line numbers. Leaf seat: no product file was
edited, no subagent spawned, no compositor command run, no tool installed.

**Result: three drafts, all validated.** `check-index-rows.py` on the drafted README row (fixture
clone, provisional registry rows present) → `errors=0`; `check-index.py` → `61/61 … dangling=0` once
the entry lands; a locator verifier → `70/70` (59 before the peer-routed checks of §5, 68 after the first peer pass). The drafted row and Frontier block are byte-hashed
below.

---

## 1. Delivered

| File (seat dir) | Holds |
|---|---|
| `skill-rows.md` | the two licence rows (FULLSCREEN, MAXIMIZED) inserted after `SKILL.md:277`; the appended contract block after `:283` (with the trailing-verdict sentence); the append-only correction to the TILED row (`:276`, D3); one advisory old→new for the stale verdict list at `:225`; §5, the peer-routed correction replacing the under-described ReDoS paragraph at `:296-301`; a locator table |
| `province-row.md` | the append-only `PROVINCE.md` paragraph carrying the round-44 state of the `tools/mado-geometry.py` row (`:32`), appended after `:97` |
| `readme-row.md` | the coverage-map index row inserted after `corpus/README.md:71`; the `### Round-44 gkeep size-request route` Frontier advance appended after `:301`; the gate receipt summary |
| `receipts/verify-locators.py`, `receipts/locators.txt` | every locator/anchor the drafts use, asserted line by line against the pins and target files |
| `receipts/index-rows-gate.txt` | the gate runs, the baseline and three controls, in a `--shared` fixture clone |

**C1, two licence rows** (what each licenses / does not license, from the pins):
FULLSCREEN (integer 2) licenses that the handler set the target box to the monitor's logical box
(`Hyprland-FullscreenHandler.cpp:191-194`) and does not license anything about the rule, the rendered
box (the dump prints the goal) or that the rule's size was lost (a floating window's size is
remembered at `:131`). MAXIMIZED (integer 1) is the same over the workspace work area (`:195-198`).
The appended block states `fsmode` (JSON integer 1 or 2 only, else 0), the order BADSIZE | FULLSCREEN
| MAXIMIZED | TILED | AGREE | DIFFER, the conditional ` maximized=<n> fullscreen=<n>` suffix, and that
the exit map is unchanged — the contract of `quality/counters/c1-r44-geometry-states.py` and
`.ufo/waves/round-44/c1/ctl-ref-tool.py.txt`.

**C2, one README row.** Cites `S164, S298, S299, S300, S301` — exactly the five PINS the frozen
counter's clause i+ forces the entry to cite; `gkeep-ui.py:449` (`application_id`), `:476`
(`set_default_size(420, 500)`), `Hyprland-Window.cpp:1732,1741,1751,1753,1514-1521`,
`Hyprland-XDGShell.cpp:354-357,629-643`, `xdg-shell.xml:1144-1166`, `gdktoplevel-wayland.c:513,530`.
`S297` is deliberately not cited: the full-file pin supersedes the round-43 excerpt, and a citation
would add a sixth Gate receipt the counter does not ask for.

---

## 2. Gates (run here; receipt paths are the evidence)

Fixture: `git clone -q --shared <lane>` → `/fast/scratch/hyaku/mado-r44/ScrSkillProvince/gitfix2`
(toplevel check passed, base `ae996fcf`); the row, the Frontier block and provisional
`corpus/SOURCES.md` rows for S298-S301 were committed **in the fixture only**. The lane's index was
never touched (`git -C <lane> diff --stat` empty; `git status` shows only untracked
`.ufo/waves/round-44/**` wave files, no tracked modification). Scratch dir deleted.

| Run | Command (cwd = lane root unless noted) | Output |
|---|---|---|
| baseline | `python3 -I quality/check-index-rows.py --repo <fixture> --rev HEAD` | `rows=60 errors=0 warns=3` |
| G1 | same, row + Frontier + provisional S298-S301, entry absent | `rows=61 errors=0 warns=3` (the 3 WARNs are pre-existing round-12/24 glob rows) |
| G2 | `quality/check-index.py --repo <fixture> --rev HEAD`, entry absent | `indexed=60/60 missing=0 dangling=1` → rc 1 |
| G2b | same, entry stub present | `indexed=61/61 … dangling=0 duplicates=0` → rc 0 |
| G3 | `check-index-rows.py`, entry stub present | `rows=61 errors=0 warns=3` (no `holds-no-overlap` for this row) |
| C1 ctl | provisional S298-S301 rows deleted | `errors=4`, one `cited-s-undefined` per id |
| C2 ctl | Sources cell emptied | `ERROR row-cells: … at line 72 carries 3 cells (need 3 non-empty)` |
| C3 ctl | `tools/nope-r44.py` added to the Sources cell | `ERROR cited-path-missing` |
| locators | `python3 -I .ufo/waves/round-44/w1/ScrSkillProvince/receipts/verify-locators.py` | `VERIFY: 70/70 passed`, rc 0 |

The `--root` mode of `check-index-rows.py` was tried first and is **not** usable for a corpus-only
copy: it resolves backticked artifact paths on the filesystem, so 27 rows whose receipts live in
`.ufo/` fail by construction. Revision mode is the only meaningful mode here.

Drafted texts, hashed: README row (1,270 B, 3 cells) sha256
`d70340393ef5d9f772a9c368c4ec6e49ed97a2da3fe2e6751e38f7389aa7317a`; the two SKILL licence rows are
single-line 3-cell table rows; the Frontier block is one `###` section with one bullet.

---

## 3. Findings

1. **Landing constraint (ids).** The row cites S298-S301; until those rows exist in
   `corpus/SOURCES.md` the gate reports `cited-s-undefined` (control C1). The L1's registry append and
   this row must land in the same revision.
2. **Landing constraint (row + entry).** `check-index.py` counts the row's note; with the row alone it
   is `dangling=1` (G2). The row cannot land before the C2 entry.
3. **D3 locator re-verified at the round-44 re-fetch.** The pseudo-size store the correction cites is
   `Hyprland-Window.cpp:2402-2408` (`setPseudoSize(*COMPUTED)` at `:2408`) in the pinned
   `efb50993…` copy — the round-43 cell's own `2402-2408` citation stands; only the licence sentence
   ("the tiler, not the floating rule path, set its box") is wrong, and the correction is appended, not
   substituted.
4. **`clients -j` has no pseudo field — verified as a negative.** `grep -in pseudo` over the pinned
   `Hyprland-HyprCtl.cpp` returns 0 matches, which is what makes "TILED cannot say which path set the
   box" a read-surface fact rather than an inference.
5. **`SKILL.md:225` still lists the round-43 verdict set** (`AGREE / DIFFER / TILED / BADSIZE`). It is
   false once C1 lands. `skill-rows.md` §3 gives the exact old→new substring; it is outside the two
   sections this seat was scoped to, so it is offered, not inserted.
6. **The Round-43 Frontier bullet's verdict list stays stale by design.** Append-only rule: the new
   `### Round-44` section states the current set and says it supersedes the older list.
7. **`holds-no-overlap` is a WARN, not a gate.** It depends on the landed entry's wording; the row's
   Holds cell was built from the same pins the entry must quote, and the stub test produced no WARN, but
   the real check is the landing seat's on the real bytes. Residual, declared.
8. **`check-index-rows.py` empty-cell message is misleading** — `carries 3 cells (need 3 non-empty)`
   for a cell that is present but blank. Cosmetic; the file is frozen for this seat, reported only.
9. **PROVINCE append is a paragraph, not a second table row.** Adding a row would rewrite the
   inventory table; the file's own convention for a moved tool fact is `**Round-NN correction
   (append-only; …):**` at the end (rounds 23, 25, 27, 36, 38). The paragraph keeps the row's read/write
   surface intact and adds only the `fullscreen` field read.
10. **No live window was observed.** Nothing here claims a maximized/fullscreen window on this host:
    the box sizes are the pinned source's fact (`FullscreenHandler.cpp:191-198`), which the counter
    docstring already declares a non-scored residual.
11. **Process note (self-reported).** My first locator batch was typed from reading and 6 of 56 checks
    failed (`Window.cpp:2401/2406`, `XDGShell.cpp:355-358/638`, `xdg-shell.xml:1163`); the verifier
    caught them and the drafts now cite only `grep -n`-computed lines. One draft edit
    (`readme-row.md` locator fix) and several later draft/report touch-ups were applied with inline
    `python3` heredocs instead of the `edit` tool; every target was inside my own seat directory, no lane
    file. The verifier re-ran after each content change (70/70 last).
12. **Peer-routed (SentLiveReads, this wave): the round-43 ReDoS paragraph under-describes its trigger.**
    `SKILL.md:296-301` names only "an alternation under a repeat", but the tool's `SAFE`/`regex_ok` also
    accept a quantified group under a repeat, and that shape is slower — `(a+)+$` on a 31-char class
    takes 43.92 s against 6.88 s for `(a|aa)+$` on 39 chars (the receipt's figures, quoted exactly)
    (`SentLiveReads/evidence/redos.txt:3-4,10`). §5 of `skill-rows.md` carries the exact old→new block,
    keeps the documented `timeout 5` guard and the exit-124 rule, and adds the measured fact that a
    timed-out run writes zero bytes (`redos.txt:6`). Not re-measured here: the peer receipt is the
    evidence.
13. **Peer-routed: the client line can carry a decoy verdict.** `class` is JSON-quoted and
    client-chosen, so `x verdict=OK` prints a token a `grep -o 'verdict=[A-Z]*'` reader takes
    (`injection.txt:10`). The appended block now says the verdict is the trailing field or must be read
    from the quoted `class=`. The counter is unaffected: `quality/counters/c1-r42-geometry.py:453`
    compares the whole stdout string.
14. **New defect class, not from D1-D7.** Items 12-13 are defects in the round-43 C1 prose found this
    wave; they are drafted as corrections of existing lines (not appends), so they need the landing
    seat's write, and they should be routed into the round-44 lesson alongside D3.

---

## 4. Out of scope / not done

- `SKILL.md`, `PROVINCE.md`, `corpus/README.md` were **not** edited — the L1 integrates; every drafted
  line is in the seat dir.
- The C1 tool change, the C2 entry text, the `corpus/SOURCES.md` rows S298-S301, the lesson `## Gate`
  ADMIT/REFUSE lines and the assimilation/quarantine paperwork belong to other seats.
- Routed closure defects D1, D2, D4, D5, D6, D7 and the round-41 leftovers were not touched.
- I did not run `hyprctl`, any counter, or any gate against the lane's own revision for C1/C2 scores;
  the C1/C2 target numbers are the frozen registration's, not re-measured here.

## 5. Artifacts (paths relative to the lane root)

| Path | sha256 |
|---|---|
| `.ufo/waves/round-44/w1/ScrSkillProvince/skill-rows.md` | `7ca60e3a9d3fa89847c1d290bd9a7ebfa23ee4bcbc7f93e8c5b04fc597f755d0` |
| `.ufo/waves/round-44/w1/ScrSkillProvince/province-row.md` | `452fb0fd65a1efa0f46e072265bef653accc393fbc9d083a89feb41743e8cf16` |
| `.ufo/waves/round-44/w1/ScrSkillProvince/readme-row.md` | `cb319ddc6b818840d286fd63451c5a7d5539fb85c85b253112307b3c2ab3d86b` |
| `.ufo/waves/round-44/w1/ScrSkillProvince/receipts/index-rows-gate.txt` | `1a044ab4f56a733276192c96a1681a83d96d29b6c3c2f215e7ec0225df506413` |
| `.ufo/waves/round-44/w1/ScrSkillProvince/receipts/locators.txt` | `fa141313155183abe65577e0baec29b6a4f290840ac4b9a9e53de897cb8df777` |
| `.ufo/waves/round-44/w1/ScrSkillProvince/receipts/verify-locators.py` | `f2e4f01672f9f7972024b3028e5f1366923861da3ffb72b0b9888a251aeb4c79` |

(Hashes are the final state of each file, re-checked after the report was written. Scratch
`/fast/scratch/hyaku/mado-r44/ScrSkillProvince` deleted; the fixture commits named in the gate
receipt died with it, the receipt is the durable record.)

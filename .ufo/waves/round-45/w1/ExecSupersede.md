# ExecSupersede — round 45 w1 report

Seat `ExecSupersede` (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/w1/ExecSupersede/`).
Target: round-43 closure **D2** / round-44 **D6** — a census-clean supersession of the imprecise S290-S297
registry cells under `CORPUS.md:116-118` (rule 2: "A correction is a new row whose `teaches` opens
`supersedes S0NN —`").

## Behaviour

Seven superseding rows drafted as **S311-S317** (`rows-block.txt`, sha256 `baaf5b55…a69f`; 11 cells each,
`cells=11` asserted, ids unique against the 238-row registry — `cell-diff.txt`). S302-S310 are this round's
own C2 pin rows (`registration.md` § C2), so the numbering continues after S310 as assigned. No old row is
edited: `status`, `recheck`, `used-by` of S290-S297 are untouched; every correction is the new row.

| new | supersedes | cells corrected (measured) | scope cell |
|---|---|---|---|
| S311 | S290 | anchor (class→engine cross-ref: `Rule.cpp:52,:98`, `WindowRule.cpp:395-396`), teaches (host text is S295; only the file's own facts) | verbatim |
| S312 | S291 | source title (floating path only), anchor (tiled consumer `Window.cpp:2402-2410` + hash), teaches (parse gate `:57-58`, centre conditions `:79-84`/`:90-91`, clamp is S293) | verbatim |
| S313 | S292 | teaches (the four in-file facts `:10-14,:64-66,:68-74,:76-78` replace the three-row inference) | verbatim |
| S314 | S293 | source title (premise removed), anchor (`:323-326`,`:339-365`), teaches (`:310-313,:323-326,:339,:342-348,:350-362,:364`, hand-off `:70-71`) | verbatim |
| S315 | S294 | teaches (the "can differ from what is on screen" inference dropped) | verbatim |
| S316 | S296 | scope (fields kept), anchor (reduced field list + sweep), teaches (absence ≠ never mapped) | narrowed (own-work, no URL) |
| S317 | S297 | source title (declaration), scope, anchor (excerpt→`ui.py:449`/`:476`, no size request), teaches | narrowed (own-work) |

S296/S297 are in closure D2's list but round-43 w2 left **no** finding for either (`ScoutRowsD.md` is one line,
`status: started`); those two successors are this seat's own re-open of the pins, stated as such. Strictly,
S311-S315 answer D2.

## Gate lines the seven rows need

Fetched and opened 2026-10-26; each quote grepped literally in its receipt by `check-quotes.sh`
(`quotes.txt`: `QUOTES: checked=7 failed=0`). All five upstream pin hashes equal the row cells and the round-43
receipts byte-for-byte.

| id | URL / path | quote (≤25 words) at | words |
|---|---|---|---|
| S311 | `raw.githubusercontent.com/hyprwm/Hyprland/efb50993…/src/desktop/rule/matchEngine/RegexMatchEngine.cpp` → `.ufo/waves/round-43/fetch/Hyprland-RegexMatchEngine.cpp` (`8ca65533…`, 470 B) | `if (regex.starts_with("negative:")) {` @ `:7` | 3 |
| S312 | `…/src/layout/algorithm/floating/default/DefaultFloatingAlgorithm.cpp` → `Hyprland-DefaultFloatingAlgorithm.cpp` (`f05f2561…`, 10359 B) | `if (WINDOW->m_ruleApplicator->static_.center.value_or(false)) {` @ `:79` | 3 |
| S313 | `…/src/layout/target/Target.cpp` → `Hyprland-Target.cpp` (`49323833…`, 3064 B) | `void ITarget::rememberFloatingSize(const Vector2D& size) {` @ `:68` | 5 |
| S314 | `…/src/layout/target/WindowTarget.cpp` → `Hyprland-WindowTarget.cpp` (`8bcaf370…`, 16614 B) | `if (DESIRED_GEOM.width <= 2 \|\| DESIRED_GEOM.height <= 2) {` @ `:339` | 9 |
| S315 | `…/src/desktop/view/types/GeometricMovableAnimated.cpp` → `Hyprland-GeometricMovableAnimated.cpp` (`649f1a8d…`, 1576 B) | `case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();` @ `:19` | 4 |
| S316 | own-work `.ufo/waves/round-43/fetch/host-clients-r43.json` (`21db902e…`, 711 B) | `"class": "Alacritty",` @ `:5`; sweeps `grep -c fullscreen`=0, `grep -c gkeep`=0 | 2 |
| S317 | own-work `.ufo/waves/round-43/fetch/gkeep-ui-excerpt.py` (`3695b788…`, 1625 B) | `window.set_default_size(420, 500)` @ excerpt `:33` = `ui.py:476`; sweep `grep -c size_request`=0 | 2 |

## Census proof (mirror copies; lane never written)

`mirror.sh` copies `corpus/` to scratch, inserts the seven rows after `corpus/SOURCES.md:250`, copies every
`used-by` path the registry names (so E11 resolves as in the lane), and runs
`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md --today 2026-10-26`.

| variant | E | W | exit |
|---|---|---|---|
| lane (`--file`, read-only) | 0 | 8 | 0 |
| m0 no rows (control, reproduces lane: `diff` shows only the `ok` path) | 0 | 8 | 0 |
| m1 rows without the round-45 lesson | **7** (E11 ×7) | 8 | **1** |
| **m2 rows + round-45 lesson naming the ids (required run)** | **0** | **8** | **0** |
| m3 joint with C2's S302-S310 (`build-pos.py` on a freeze clone) + S311-S317 | 0 | 10 (C2's own S303/S307 W04) | 0 |
| m4 mutant: S315's opener deleted | **1** (E04 S315) | 8 | 1 |

Required run, `census-m2.txt` verbatim (`exit 0`):

```
file	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
file	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
file	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
file	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
file	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
file	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
file	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
file	W01	S277 tierC mined used-by=corpus/knowledge/request-socket-live-bound-r8.md
file	ok	/fast/scratch/hyaku/mado-r45/ExecSupersede/m2/corpus/SOURCES.md
```

Joint state (`census-m3.txt`, `exit 0`, `rows 254` = 238 + 9 + 7) adds exactly two lines over m2 — the C2 rows'
own declared duplicates (`S303` ConfigManager, `S307` HyprCtl) and nothing from S311-S317.

## Findings

1. **Supports D2 on its named case** — S293's title carried the refuted premise and its teaches omitted the
   `||` gate, the `>5` gate, the 600x400/error returns and the stored-size override; S314 corrects all of it
   with recomputed locators.
2. **Attacks D2's list** — S296/S297 had no w2 finding; their successors are grounded re-opens, not an
   inherited defect set (`.ufo/waves/round-43/w2/ScoutRowsD.md`).
3. **Measured: a supersession of a URL-bearing row costs no census finding** when its scope cell is kept
   verbatim (m2 = m0); the exemption is the `teaches` opener (`sources-census.sh:646-649`), and m4 proves it is
   load-bearing.
4. **The rows are not landable alone** — seven E11 lines (m1) require the round-45 lesson naming them in the
   same commit.
5. **No collision with the round's C2 rows** — m3 lands both sets at exit 0, 254 rows; ids and URLs disjoint.

## Risks / limits (declared)

- Census ran on **mirrors**, never a lane commit; appending to `corpus/SOURCES.md` is the L1's step.
- m2's lesson is a stub that only names the ids (to prove E11 resolves); the real lesson wording is the L1's.
- `used-by` = `corpus/lessons/round-45.md` is a forward reference; until that file exists the rows cannot be
  `mined` — m1 is that red state.
- [INFERENCE] These rows cannot move `quality/counters/c2-r45-monitor-entry.py` while uncited: its clauses
  iterate the monitor entry's cited ids (S302-S310). Reading of the counter, not a run.
- No compositor contact, no `hyprctl`, no package operation, no tool installed; own-work pins were read from
  the committed receipts.

## Evidence retained

`.ufo/waves/round-45/w1/ExecSupersede/`: `rows.md` (full analysis), `rows-block.txt` (rows),
`check-quotes.sh` + `quotes.txt` (`QUOTES: checked=7 failed=0` + pin hashes + negative sweeps),
`cell-diff.txt`, `mirror.sh`, `census-{lane,m0,m1,m2,m3,m4}.txt`.
Scratch `/fast/scratch/hyaku/mado-r45/ExecSupersede/` deleted; no scratch or `/tmp` path is cited as evidence.

## Blockers

None.

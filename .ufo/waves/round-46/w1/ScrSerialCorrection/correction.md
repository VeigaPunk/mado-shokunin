# M45-2 correction — draft append for `corpus/lessons/round-45.md` (round-46 closure D2)

Seat `w1/ScrSerialCorrection`, 2026-10-26. This file is a **draft**: the L1 is the only integrator and the only writer of
`corpus/lessons/round-45.md`. Nothing here edits a held entry, a counter, a gate or the lesson.

- **What it corrects:** the count in M45-2 (`corpus/lessons/round-45.md:49-51`), which names one held carrier
  (`corpus/knowledge/hyprctl-verification-layer.md:153`). The serial sits in **24 tracked files** — 3 held entries and 21
  wave copies.
- **How the value was obtained:** read from `hyprctl monitors all -j` into a shell/Python variable and used only as a
  `git grep -F` needle. The value is not written in this file, in the receipts, or in any command output; only counts and
  paths are printed.
- **Re-measured:** `python3 -I verify.py` → `VERIFY: checks=29 failed=0 verdict=PASS` (this directory). The script
  regenerates `receipts/01-census-4d22eeb.txt` … `receipts/05-untracked.txt`; `receipts/06-gate.txt` is the gate run.
- **Not verified here:** serials embedded in ignored or untracked files outside the lane; the truth of the three held
  sentences beyond the fact that each carries the value; any rewrite cost estimate for the pushed refs.

## Draft text to append (append-only, below `## considerthese`)

````markdown
## Round-46 correction (M45-2) — the serial's spread, not one file

M45-2 (`corpus/lessons/round-45.md:49-51`) says the host monitor's serial lives in one held entry:
"and held `corpus/knowledge/hyprctl-verification-layer.md:153` has carried it since round 2" (`:50`). The count is wrong:
the serial sits in **24 tracked files, one occurrence each**, at the round-45 tip `4d22eeb`, and the count is unchanged at
`0c89478`, `b22ea56`, `8c5434c6` and `e0be61e4` (`git grep -c -F "$S" <rev> -- .`, `$S` read from
`hyprctl monitors all -j`; receipts under `.ufo/waves/round-46/w1/ScrSerialCorrection/receipts/`, `02-revs.txt` for this
sweep and `01-census-4d22eeb.txt` for the per-file counts and paths cited below).

Held entries (3) — `git grep -c -F "$S" <rev> -- . ':!.ufo'`; locators computed by `git grep -n`:

- `corpus/knowledge/config-health-report-r3.md:149`
- `corpus/knowledge/hyprctl-verification-layer.md:153`
- `corpus/knowledge/hyprland-config-plane.md:184`

Wave copies (21) — seven committed fixture trees, each holding all three entries verbatim: six under
`.ufo/waves/round-32/` (`assimilation/validate`, `c1/controls/a-rows-only`, `c1/controls/b-entries-only`,
`scratch/MutExistingGates/fixtures/tree-m1`, `tree-m2`, `tree-m2b`; 18 files) and one under `.ufo/waves/round-37/`
(`w1/scratch/ScribeRows/validate`; 3 files). Each fixture is a copy, so the 21 files are one carrier decision repeated,
not 21 independent leaks — a fix means the three held lines and the fixture generator that copies them.

Provenance (pickaxe `git log --all --reverse -S<serial> -- .`, `receipts/03-pickaxe.txt`): one held carrier per probation
round — 1 at `65a2254d`, 2 at `e1e1bb77`, 3 at `f9f58c0e`, all 2026-10-14; the wave copies enter at `f5910876`
(2026-10-24, 24 files), fall to 18 when `48f9fe09` dropped seat scratch trees from the committed set, and return to 21 at
`f6ae0c36` (2026-10-25, round-37). Round 45 introduced none (`0c89478` → `4d22eeb`: 24 → 24 files), so the correction is a
correction of the count, not of this round's conduct. Age at 2026-10-26: 12 days (held), 2 days (wave copies).

Capture boundary, measured rather than assumed: `quality/check-session-material.py` lists only tracked files under `.ufo/`
(`:255-256`) and recognises a monitor as a JSON object with a non-empty `serial` (`:26`, `:223-230`). The three held
entries are therefore outside its path scope by construction, and the 21 copies are prose with no JSON object. Run at
`e0be61e4`: `files=17101 findings=97`, none of the 97 on a carrier (`receipts/06-gate.txt`). M45-2's
`captured-by: none` stands; only its count changes. Teaching the gate a prose serial rule is routed separately (D3) and is
not part of this correction.

Published: all 11 heads on `origin` carry the serial — `master` 24 files, and the eight `cursor/*` heads, `devin/wiki-link`
and `wip/operator-save-20261023` 3 each (`receipts/04-refs.txt`). **Removal from pushed history is the operator's
decision:** it rewrites every ref, which no lane action may do. The remedy M45-2 already states is unchanged — the seat
file was redacted before commit (verified: `.ufo/waves/round-45/w1/ExecLiveHost/verify-quotes.py` at `4d22eeb` holds 0
occurrences), and held entries are corrected by appending, never by rewriting.

Limit: the untracked lane tree was scanned bytewise on 2026-10-26 at the time of the run and held 0 carriers
(`receipts/05-untracked.txt` records that run's file count — it grows while wave seats write); ignored paths and files
outside the lane were not scanned.
````

## Pointers the L1 needs

- Receipts: `receipts/01-census-4d22eeb.txt` (24 paths + counts), `02-revs.txt`, `03-pickaxe.txt`, `04-refs.txt`,
  `05-untracked.txt`, `06-gate.txt`. Regenerate with `python3 -I verify.py` from this directory (read-only on the lane).
- The block is append-only and sits after `## considerthese` in `corpus/lessons/round-45.md`; it changes no gate, counter,
  row, or entry. If the L1 prefers a round-46 lesson file instead, the block's first line is the only heading change.
- The prose rule in the gate is **not** in this draft's write scope (seat bounds: no edits to tracked files).

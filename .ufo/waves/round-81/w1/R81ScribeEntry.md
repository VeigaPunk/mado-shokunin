# R81ScribeEntry — report

Seat: R81ScribeEntry (leaf). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Assignment: draft the C1 knowledge entry (prose only; L1 integrates).

## Behavior

Wrote `.ufo/waves/round-81/w1/R81ScribeEntry/entry-draft.md` in the r80
`bar-footprint-composition-r80.md` shape: `source:` / `verified-at:` / `recheck:` header, then §1 what
this entry is, §2 `CBox::round` coupled (verbatim `S478:51-63` per-line table, the `x=-1, w=1002`
derivation, the floor-divided `0/1001` counterpart), §3 hyprutils revision and inference class,
§4 the client-side auto gate and the join's refusal, §5 the gate's composition consequence (corner /
parallel / all-four inert `exclusiveEdge`; left dock's 40 on the attribution vector), §6 the
DECL/ATTR/RESULT fields the six new cases pin, §7 seven limits, §8 the two new SOURCES rows.

Every sentence in the draft carries a file:line; nothing is asserted from a tool run where a source
line exists. The entry creates nothing and claims no live surface.

## Gates

- `measurement-c1-r81.txt:70` — `cases=39 correct=39 mutants=28 killed=28 base_correct=33/39
  carried=33/33 tool_selftest=121/121 verdict=TARGET_MET rev=0e2ccd2a… tool_sha256=a129a435…`
  (read, not re-run).
- Freeze bytes: `git show 0e2ccd2a…:tools/mado-barfoot.py | sha256sum` equals
  `sha256sum tools/mado-barfoot.py` = `a129a435572805c3ae7730714f0dafdea2b9a7e420f53f0d109dc2d5f57d1230`.
- Targeted re-run: the frozen tool over the six new cases reproduces every `expect` object
  (`.ufo/waves/round-81/w1/R81ScribeEntry/join-six-cases.txt`).
- Base control reproduced over all 39: `correct=33/39`, `carried 33/33`, `new 0/6`
  (`base-39-matrix.txt`).
- Not run by this seat: the full 39-case counter, the 28 mutants, the tool selftest, any network
  fetch, `hyprctl`, any git/jj mutation, any pacman transaction.

## Touched surfaces

- `.ufo/waves/round-81/w1/R81ScribeEntry/entry-draft.md` (new)
- `.ufo/waves/round-81/w1/R81ScribeEntry/join-six-cases.txt` (new)
- `.ufo/waves/round-81/w1/R81ScribeEntry/base-39-matrix.txt` (new)
- `.ufo/waves/round-81/w1/R81ScribeEntry/findings.md` (new)
- `.ufo/waves/round-81/w1/R81ScribeEntry.md` (this report, new)
- scratch `/fast/scratch/hyaku/mado-r81/R81ScribeEntry` (created, evidence copied out, removed)

No edit to the frozen instruments, the control sets, the declaration, `SKILL.md`, `LOG.md`,
`corpus/SOURCES.md`, or the pre-existing untracked `corpus/knowledge/bar-footprint-rounding-auto-r81.md`.

## Findings

1. **Base-rule label vs base bytes.** The receipt's `rule=held-r79-model(no-multi-surface-arrangement)`
   is contradicted by the file extracted at `base_rev`: `VERSION = "r80-v1"` and
   `def evaluate_composition` (`c702094a…:tools/mado-barfoot.py:85`, `:652`). The 33/39 is the r80
   composition tool on the successor set (carried 33, new 0). Frozen counter, so flagged, not edited.
2. **The left dock's 40 is in `attr`, not in any verdict.** `RESULT.reserved` compares the bar's edge
   only (`tools/mado-barfoot.py:830-838`); `auto-left-dock` prints `gt=0,26,0,0 attr=40,26,0,0` and
   `reserved=EQ`. The left band is a model prediction with no compositor counterpart in the fixture.
   Draft records this as limit 5.
3. **Host hyprutils is `0.14.2-1`, not `0.14.0`** (`pacman -Q hyprutils hyprland` → also
   `hyprland 0.56.2-4`). The CMake line is a `>=` licence (`S479:150`, `:156`); whether
   `CBox::round` changed in the two patch releases is `[UNK]` — settled by opening the `v0.14.2`
   `src/math/Box.cpp`. This supersedes the corpus draft's "not read this round" sentence.
4. **Two drafts now exist.** The sibling untracked
   `corpus/knowledge/bar-footprint-rounding-auto-r81.md` and this seat's `entry-draft.md` differ in
   the host version read, the `S460:159-163` protocol quote, the base-label finding, the §6 field
   summary / `edge=none` distinction, and limit 5. L1 should pick one text at integration; the
   gate-block `used-by` names that path.
5. **The overflow case is synthetic** (1000×800 M1, 1001-wide panel; host monitor is 3440 wide,
   `live-join-r80.txt:5`): it certifies arithmetic, not a host surface.
6. **No source contradiction found** in the six claims; the gate classes the join returns 0 for are
   the client's own no-zone classes (`S464:269-288`, protocol `S460:159-163`), and the dynamic-band
   refusal is a named limit, not a silent zero.
7. **A v0.14.2 copy sits in shared scratch** (`/fast/scratch/hyaku/mado-r81/Box-v0.14.2.cpp`, listed
   by `ls` at cleanup; not this seat's file). Scratch is not citable, so the draft keeps the
   `0.14.0` vs `0.14.2` question `[UNK]`; if the owning seat commits a v0.14.2 pin, the L1 can close
   it from those bytes.

## Out of scope

Entry integration into `corpus/knowledge/` and `corpus/SOURCES.md` (L1's job); re-running the full
counter/mutants/selftest; any runtime probe; any commit.

## Artifacts

- `.ufo/waves/round-81/w1/R81ScribeEntry/entry-draft.md`
- `.ufo/waves/round-81/w1/R81ScribeEntry/join-six-cases.txt`
- `.ufo/waves/round-81/w1/R81ScribeEntry/base-39-matrix.txt`
- `.ufo/waves/round-81/w1/R81ScribeEntry/findings.md` (full command log, exact argv)

STATUS: ok

# R81ScribeSources — the two new SOURCES.md rows (S478, S479)

Seat: prose draft + verification only. No frozen instrument, control set, declaration,
SKILL.md or LOG.md was touched; the L1 integrates.

## 1. Schema as it actually is

Header row, `corpus/SOURCES.md:11`:

```
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
```

**11 columns** (validated as `NF=13` under `awk -F'|'`, i.e. 11 cells plus the two
delimiter empties). The seat brief's sketch (`id · source · tier · status · teaches ·
anchor/quote · status · recheck · used-by · …`) is not the file's order; the file is
`id · source · kind · tier · scope · anchor · teaches · status · opened · recheck · used-by`.
The last ten registry rows at HEAD are S466, S467, S470, S471, S472, S473, S474, S475,
S476, S477 (S468/S469 are absent, not reused); HEAD has 412 rows, the working tree now
has 414 because the integrator has already appended the pair (see §7).

## 2. The two rows, in schema

Both validated as NF=13 and accepted by `sources-census.sh validate` (exit 0).

```
| S478 | hyprutils v0.14.0 — src/math/Box.cpp — https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.0/src/math/Box.cpp | code | A | mado layer plane: the box arithmetic the compositor applies after arranging a layer surface — `CBox::round`'s coupled origin/far-edge rounding, and the `empty`/`containsPoint` predicates the arrangement's skip uses (round-81 C1) | `CBox::round` :51-63, `CBox::empty` :47-49, `CBox::containsPoint` :43-45 @ tag v0.14.0 (fetched 2026-11-04, sha256 2d04de99ba977e5c3d99546606aede0d3eacc819049e16da5e0fd0d2004d083c, 5901 B) | `double newW     = x + w - roundedX;` then `w = std::round(newW);` — the origin is rounded first and the width is the rounded distance from that origin to the unrounded far edge, so an overflow rounds its span independently of its origin | mined | 2026-11-04 | on-release | corpus/knowledge/bar-footprint-rounding-auto-r81.md |
| S479 | Hyprland v0.56.2 — CMakeLists.txt — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/CMakeLists.txt | code | A | mado layer plane: the hyprutils version floor Hyprland's build requires at efb50993 — the pin that licenses S478's v0.14.0 bytes as the arithmetic this commit builds against (round-81 C1) | `set(HYPRUTILS_MINIMUM_VERSION 0.14.0)` :150 and the consuming `pkg_check_modules(hyprutils_dep REQUIRED IMPORTED_TARGET hyprutils>=${HYPRUTILS_MINIMUM_VERSION})` :156 @ efb50993 (fetched 2026-11-04, sha256 97b8028aa342cf6ee6f04b5db2e67e6e4fe6adf5d3fd67bad18005193db36516, 25010 B) | the build requires hyprutils at least 0.14.0, so reading the v0.14.0 tag is licensed as that minimum — a version floor in the build, not a runtime read of the host's installed library | mined | 2026-11-04 | on-release | corpus/knowledge/bar-footprint-rounding-auto-r81.md |
```

`used-by` is `corpus/knowledge/bar-footprint-rounding-auto-r81.md` (exists, 7,847 B) —
chosen because census E11 requires every mined row's used-by path to exist on disk. Naming
`corpus/knowledge/bar-footprint-composition-r81.md` instead would raise E11 until that file
lands.

## 3. Quote verification (`grep -n -F`, pinned bytes)

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/fetch/S478.bin`:

```
54:    double newW     = x + w - roundedX;
59:    w = std::round(newW);
48:    return std::fabs(w) < EPSILON || std::fabs(h) < EPSILON;
52:    double roundedX = std::round(x);
51:CBox& Hyprutils::Math::CBox::round() {
47:bool Hyprutils::Math::CBox::empty() const {
```

`S479.bin`:

```
150:set(HYPRUTILS_MINIMUM_VERSION 0.14.0)
156:pkg_check_modules(hyprutils_dep REQUIRED IMPORTED_TARGET hyprutils>=${HYPRUTILS_MINIMUM_VERSION})
```

Word counts (`wc -w` on the quoted text): `double newW     = x + w - roundedX;` = 8,
`w = std::round(newW);` = 3, `set(HYPRUTILS_MINIMUM_VERSION 0.14.0)` = 2, and the
`pkg_check_modules(...)` line = 4 — every quote is well under the 25-word cap. The
`S478` span `:51-63` is the whole function: line 51 is the signature, `:59-60` assign
`w`/`h`, `:62` closes the body.

## 4. Pin verification

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/fetch && sha256sum -c sha256-r81.txt
S478.bin: OK
S479.bin: OK
EXIT=0
```

Byte sizes: `5901 S478.bin`, `25010 S479.bin`. Hashes are the manifest's:
`2d04de99ba977e5c3d99546606aede0d3eacc819049e16da5e0fd0d2004d083c` and
`97b8028aa342cf6ee6f04b5db2e67e6e4fe6adf5d3fd67bad18005193db36516`.

## 5. Id space

At HEAD (`git show HEAD:corpus/SOURCES.md`, 412 rows):

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort | tail -5
S473
S474
S475
S476
S477
$ git show HEAD:corpus/SOURCES.md | grep -cE '^\| S47[89] \|'
0
```

So S478/S479 were unused at draft time; the working tree now contains them because the
integrator appended the pair (414 rows). No id is reused or renumbered.

## 6. Census

Official lane command and result (after the integrator's append):

```
$ cd /home/vgpnk/Projects/shokunin && ./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
EXIT=0
```

The draft pair was additionally validated against the HEAD baseline in an isolated
`mktemp -d` mirror (real `corpus/` dir, sibling paths symlinked read-only), rows inserted
inside `## Registry` and before `## Paths`:

```
 S478  NF=13
 S479  NF=13
file	ok	/fast/scratch/hyaku/mado-r81/sources-<rand>/corpus/SOURCES.DRAFT.md
EXIT=0
```

No E-code fired for either row; the pre-existing standing warnings (53 W04 duplicates,
1 W01 on S277) are unchanged. Two earlier scratch attempts are not evidence: the first
appended the rows at EOF, after `## Paths`, and correctly drew
`E12 S478 row outside Registry section` / `E12 S479 …` — rows must go inside the table
before `## Paths`; the second reused a stale scratch dir and drew self-inflicted
`E03 duplicate id`.

## 7. Integration state (reported, not edited by this seat)

The working tree already carries an integrator-appended pair inside the Registry
(`git -C … diff -- corpus/SOURCES.md` = 2 insertions, 0 deletions; rows at lines 430-431,
`## Paths` at 433). Their cells:

- S478: kind `code`, tier `A`, anchor `` `CBox::round` `:51-63` @ v0.14.0 (fetched 2026-11-04, sha256 2d04de99…, 5901 B) ``, teaches `` `    double newW     = x + w - roundedX;` (at `:54`) ``, status `mined`, opened `2026-11-04`, recheck `on-release`, used-by `corpus/knowledge/bar-footprint-rounding-auto-r81.md`.
- S479: kind `code`, tier `A`, anchor `` `:150` @ efb50993 (fetched 2026-11-04, sha256 97b8028a…, 25010 B) ``, teaches `` `set(HYPRUTILS_MINIMUM_VERSION 0.14.0)` (at `:150`) ``, status `mined`, opened `2026-11-04`, recheck `on-release`, used-by `corpus/knowledge/bar-footprint-rounding-auto-r81.md`.

Both integrated rows are NF=13 and their quotes are literal at the cited lines (verified
above, including the four leading spaces in the S478 quote). The only substantive
difference from this seat's draft is that the draft also cites `:59` (the width assignment)
and the `empty`/`containsPoint` spans; the integrated anchor keeps `:51-63`, which covers
them. Either form validates; the integrator's is the one on disk.

## 8. Which row C1 rests on — and what neither licenses

**C1 rests on S478.** The declaration's Frontier step says it verbatim:
"`C1 cites S478`" (`.ufo/waves/round-81/claims-declaration-r81.md:165`), and C1 item 1
derives the `x=-1, w=1002` overflow from `src/math/Box.cpp:51-63`. S479 is not claim
ground; it is the tag licence (declaration `:163-165`: "`S479` = Hyprland `CMakeLists.txt`
at `efb50993…` (`set(HYPRUTILS_MINIMUM_VERSION 0.14.0)`, the pin that licenses the tag)").

**S478 does not license:**

- that the host runs hyprutils v0.14.0 — no runtime version read exists in this round;
- that every Hyprland box goes through `CBox::round` — only that `arrangeLayerArray`
  calls `box.round()` (S470 `:2653`, `:2660`), which is why the pair is cited together;
- the gtk-layer-shell auto-zone behaviour in C1 items 2-4 — that is S464 `:264-292`;
- that the v0.14.0 tag URL was re-fetched this round — only the pinned bytes were hashed;
- any statement about a live surface's measured geometry; every number is a model
  prediction over captured bytes.

**S479 does not license:**

- that hyprutils 0.14.0 is *the* version in use — `>=` is a floor, satisfied by any later
  release (e.g. the v0.14.2 rows already in this registry);
- that the host linked 0.14.0, or that the tag's bytes equal the host's installed library;
- any Hyprland runtime behaviour on its own — it is build metadata, not compositor logic;
- a version *equality* or a claim that 0.14.0 was current when efb50993 was written; a
  minimum can lag the version actually built.

## 9. Incident disclosure (this seat's own writes)

The seat scratch path was pre-seeded with symlinks into the lane. Re-running `ln -s`
without `-n` followed four of them and created self-referential links **inside the lane**:

```
corpus/lessons/lessons   -> corpus/lessons      (mtime 2026-11-04 09:44:08)
corpus/knowledge/knowledge -> corpus/knowledge  (mtime 2026-11-04 09:44:30)
tools/tools              -> tools               (mtime 2026-11-04 09:44:08)
.ufo/.ufo                -> .ufo                (mtime 2026-11-04 09:44:08)
```

All four were removed with `rm -- <exact paths>` and re-checked (`gone:` for each). No
other lane path was written by this seat; `corpus/SOURCES.md`, `corpus/README.md`,
`corpus/lessons/round-80.md`, `corpus/knowledge/bar-footprint-rounding-auto-r81.md` and
`corpus/lessons/round-81.md` show as modified/untracked from the integrator's and other
seats' work, not this seat's. Scratch dirs were removed explicitly (the harness does not
fire `EXIT` traps).

## 10. Tooling

No install or upgrade was made; no package manager was run.

STATUS: ok

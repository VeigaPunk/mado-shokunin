# R81ScribeSources — findings (command log)

All paths absolute under `/home/vgpnk/Projects/shokunin/mado-shokunin` (lane `L`) unless
stated. Read-only git only. No frozen instrument, control set, declaration, SKILL.md or
LOG.md edited.

## 1. Schema

```
$ wc -l /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
910 /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md

$ grep -n '^| id ' /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
11:| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |

$ sed -n '11p' …/corpus/SOURCES.md | awk -F'|' '{print NF-2" columns"}'
11 columns
```

Header cells: `id, source, kind, tier, scope, anchor, teaches, status, opened, recheck,
used-by`. Census enforces `NF==13` for 11 cells.

Last-ten rows read at HEAD, in file order: S466, S467, S470, S471, S472, S473, S474,
S475, S476, S477. Ids S468/S469 do not exist (never reused per SOURCES contract §Rules 1).

## 2. Pin verification

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/fetch && sha256sum -c sha256-r81.txt
S478.bin: OK
S479.bin: OK
EXIT=0

$ wc -c S478.bin S479.bin
 5901 S478.bin
25010 S479.bin

$ sha256sum S478.bin S479.bin
2d04de99ba977e5c3d99546606aede0d3eacc819049e16da5e0fd0d2004d083c  S478.bin
97b8028aa342cf6ee6f04b5db2e67e6e4fe6adf5d3fd67bad18005193db36516  S479.bin
```

## 3. Quotes (`grep -n -F`)

```
$ grep -n -F 'double newW     = x + w - roundedX;' S478.bin
54:    double newW     = x + w - roundedX;
$ grep -n -F 'w = std::round(newW);' S478.bin
59:    w = std::round(newW);
$ grep -n -F 'double roundedX = std::round(x);' S478.bin
52:    double roundedX = std::round(x);
$ grep -n -F 'CBox& Hyprutils::Math::CBox::round() {' S478.bin
51:CBox& Hyprutils::Math::CBox::round() {
$ grep -n -F 'bool Hyprutils::Math::CBox::empty() const {' S478.bin
47:bool Hyprutils::Math::CBox::empty() const {
$ grep -n -F 'return std::fabs(w) < EPSILON || std::fabs(h) < EPSILON;' S478.bin
48:    return std::fabs(w) < EPSILON || std::fabs(h) < EPSILON;
```

```
$ grep -n -F 'set(HYPRUTILS_MINIMUM_VERSION 0.14.0)' S479.bin
150:set(HYPRUTILS_MINIMUM_VERSION 0.14.0)
$ grep -n -F 'pkg_check_modules(hyprutils_dep REQUIRED IMPORTED_TARGET hyprutils>=${HYPRUTILS_MINIMUM_VERSION})' S479.bin
156:pkg_check_modules(hyprutils_dep REQUIRED IMPORTED_TARGET hyprutils>=${HYPRUTILS_MINIMUM_VERSION})
```

Word counts (`printf '%s\n' '<quote>' | wc -w`): 8, 3, 2, 4 respectively — all ≤ 25.

Function body read for the span proof:

```
$ sed -n '45,70p' S478.bin
bool Hyprutils::Math::CBox::empty() const {
    return std::fabs(w) < EPSILON || std::fabs(h) < EPSILON;
}

CBox& Hyprutils::Math::CBox::round() {
    double roundedX = std::round(x);
    double roundedY = std::round(y);
    double newW     = x + w - roundedX;
    double newH     = y + h - roundedY;

    x = roundedX;
    y = roundedY;
    w = std::round(newW);
    h = std::round(newH);

    return *this;
}

$ sed -n '150,175p' S479.bin
set(HYPRUTILS_MINIMUM_VERSION 0.14.0)
…
pkg_check_modules(hyprutils_dep REQUIRED IMPORTED_TARGET hyprutils>=${HYPRUTILS_MINIMUM_VERSION})
```

## 4. Id space

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort | tail -5
S473
S474
S475
S476
S477

$ grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' …/corpus/SOURCES.md
412

$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin show HEAD:corpus/SOURCES.md | grep -cE '^\| S47[89] \|'
0
```

Interpretation: at HEAD, 412 rows and the highest id is S477; neither S478 nor S479 exists.
(S468/S469 are absent entirely.)

## 5. Census — official command

```
$ cd /home/vgpnk/Projects/shokunin && ./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
mado	W04	S477 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/tests/desktop/Reserved.cpp across scopes
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
EXIT=0
```

No `E`-code lines in the output.

## 6. Draft-pair validation (isolated mirror at HEAD)

Because the working tree already carried the integrator's pair, the seat's own two rows
were validated against `git show HEAD:corpus/SOURCES.md` in a fresh `mktemp -d`:

```
$ T=$(mktemp -d /fast/scratch/hyaku/mado-r81/sources-XXXXXXXX)
$ awk … rows inserted before '## Paths' … > "$T/corpus/SOURCES.DRAFT.md"
 S478  NF=13
 S479  NF=13
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$T/corpus/SOURCES.DRAFT.md"
file	ok	/fast/scratch/hyaku/mado-r81/sources-I2M18ABK/corpus/SOURCES.DRAFT.md
EXIT=0
```

Finding counts: `ok 1`, `W01 1` (pre-existing S277), `W04 53` (pre-existing duplicates),
no `E*`. `used-by` in this run pointed at the existing
`corpus/knowledge/bar-footprint-rounding-auto-r81.md`; the alternative
`corpus/knowledge/bar-footprint-composition-r81.md` does not exist and would raise E11.

Failed attempts, recorded as limits not evidence:

```
Run A (rows appended at EOF):  file	E12	S478 row outside Registry section
                               file	E12	S479 row outside Registry section
Run B (stale scratch dir):     file	E03	S478 duplicate id
                               file	E03	S479 duplicate id
```

Run A is a real integration constraint: the registry table ends before `## Paths` at
`corpus/SOURCES.md:433`, so the L1 must insert the rows above that heading, not at EOF.

## 7. Working-tree integration state

```
$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff --stat -- corpus/SOURCES.md
 corpus/SOURCES.md | 2 ++
 1 file changed, 2 insertions(+)

$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain -- corpus/
 M corpus/README.md
 M corpus/SOURCES.md
 M corpus/lessons/round-80.md
?? corpus/knowledge/bar-footprint-rounding-auto-r81.md
?? corpus/lessons/round-81.md
```

The two insertions are the integrator's S478/S479 at lines 430-431 (inside Registry,
before `## Paths` at 433), NF=13 each, used-by
`corpus/knowledge/bar-footprint-rounding-auto-r81.md` (7,847 B, exists). Their literal
quotes were re-checked with the four leading spaces:

```
$ grep -n -F '    double newW     = x + w - roundedX;' S478.bin
54:    double newW     = x + w - roundedX;
$ grep -n -F '    w = std::round(newW);' S478.bin
59:    w = std::round(newW);
$ grep -n -F 'set(HYPRUTILS_MINIMUM_VERSION 0.14.0)' S479.bin
150:set(HYPRUTILS_MINIMUM_VERSION 0.14.0)
```

## 8. C1 dependency

`.ufo/waves/round-81/claims-declaration-r81.md:162-165`:

```
Two rows opened and pinned this round
(`fetch/S478.bin`, `fetch/S479.bin`, manifest `fetch/sha256-r81.txt`): **S478** = hyprutils v0.14.0
`src/math/Box.cpp` (the `CBox::round` and `CBox::empty`/`containsPoint` arithmetic), **S479** =
Hyprland `CMakeLists.txt` at `efb50993…` (`set(HYPRUTILS_MINIMUM_VERSION 0.14.0)`, the pin that
licenses the tag). C1 cites S478; the round's mistake and its Gate block live in
`corpus/lessons/round-81.md`.
```

C1 item 1 (`CBox::round`'s coupled rounding, `Renderer.cpp:2613` centre then `:2660` round,
`Box.cpp:51-63`) is the S478 claim. C1 items 2-4 rest on S464 and S470, not on either new
row. S479 licenses only the tag; it grounds no claim on its own.

## 9. This seat's lane writes and their removal

Four self-referential symlinks were created inside the lane at 09:44 by `ln -s` following
pre-seeded scratch symlinks (missing `-n`):

```
corpus/lessons/lessons     -> …/corpus/lessons
corpus/knowledge/knowledge -> …/corpus/knowledge
tools/tools                -> …/tools
.ufo/.ufo                  -> …/.ufo
```

Removed with `rm -- <four absolute paths>` (`rm exit=0`), then re-checked:

```
gone: corpus/lessons/lessons
gone: corpus/knowledge/knowledge
gone: tools/tools
gone: .ufo/.ufo
```

No other lane path was created or modified by this seat. Scratch dirs were removed
explicitly with `rm -rf` (the harness does not fire `EXIT` traps, which is how the stale
dir caused Run B).

## 10. Tooling

No installs; no pacman/uv/npx invocation.

STATUS: ok

# MadoR19.RerunC2 — partial

C2 as a *number* holds and reproduces exactly from committed bytes: `2/13 = 1.5385` at
`9c54c56`, `13/13 = 10.0` at `df84807` and `01b8094`, supersede-sweep `stale=11 → 0`.
C2 as *sourced on S096* does not hold uniformly: only 5 of the 13 credited files cite
S096 on a crediting line; 6 cite rows that already existed at baseline (S090/S091), and
2 cite S090 while explicitly denying that S096 is recorded — a denial that is false at
the tip, where `corpus/SOURCES.md:108` records S096 as `mined` and lists those two files
as its `used-by` targets.

All C2 numbers below were re-run from **committed bytes**: both checkers and the ledger
were extracted with `git show 01b8094:…` into a `/tmp` clone and executed there
(`/tmp/c2clone`), because the lane worktree is being edited by other wave-2 seats (see F4).

## 1. Independent re-runs

Setup: `/tmp/c2clone` = `git clone --no-local` of the lane, reset to
`01b80946d92b26370d3012a7da655d00dd135154`; then

```
git -C <lane> show 01b8094:.ufo/waves/round-19/fresh-pins.py       > .ufo/waves/round-19/fresh-pins.py
git -C <lane> show 01b8094:.ufo/waves/round-19/supersede-sweep.py > .ufo/waves/round-19/supersede-sweep.py
git -C <lane> show 01b8094:.ufo/waves/round-19/supersessions.json  > .ufo/waves/round-19/supersessions.json
sha256(supersessions.json) = 87644b585eb486c0056c3b9800966a0d5a3d6e582f77141a8716adde0cd38d58
```

| REV | `fresh-pins.py` | `supersede-sweep.py` |
|---|---|---|
| `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d` | `current 2 / 13, score 1.5385` | `files=13 pointed=2 stale=11`, exit 1 |
| `df84807d8fc49f5d8fb4ec3060859e5b1992084c` | `current 13 / 13, score 10.0` | `files=13 pointed=13 stale=0`, exit 0 |
| `01b80946d92b26370d3012a7da655d00dd135154` | `current 13 / 13, score 10.0` | `files=13 pointed=13 stale=0`, exit 0 |

The SCORECARD cell's "at `df84807` and `01b8094`" is exact (`SCORECARD.md:1133`, worktree
copy; the committed tip carries only the pre-registration, see F4).

Contract control, `SKILL.md:573` ("REV `17661e0…` must print 11 STALE of 13, the set
`fresh-pins.py` also reports at that REV"): both checkers at
`17661e0fa83f978fb659f5bb8fef47f0969f6945` give `pointed=2 / stale=11`, and the two
POINTED files equal the fresh-pins `current` set exactly
(`corpus/README.md`, `corpus/knowledge/walker-route-r18.md`). Control holds.

Denominator honesty: at `9c54c56`, 74 tracked files contain `2.17.0`
(`git grep -l -F 2.17.0`). The declared scope (owned: `corpus/knowledge/*.md`,
`corpus/README.md`, `SKILL.md`, `PROVINCE.md`, `tools/*`; pre-registered at
`SCORECARD.md:1080-1084`) selects exactly the 13 counted files; the 61 exclusions are
the dated-record classes the pre-registration names (lessons, `SOURCES.md`, `LOG.md`,
`plans/`, `SCORECARD.md`, `.ufo/`). I found no owned file containing `2.17.0` that the
script silently drops. Denominator is faithful to the declaration.

## 2. Every credited file, pointer lines, token, and S096 status (tip)

Committed bytes, `01b80946…`; line numbers are `grep -n` over `git show`. "Permitted
token" = S090/S091/S096 or a span containing one.

| file | crediting lines | permitted token(s) | S096 status |
|---|---|---|---|
| `SKILL.md` | 573, 1853, 1855, 1856, 1857, 1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865 | S090/S091/S096 | **evidence** (offsets 856,302; sha prefix `25240650…`; `.comment`) |
| `corpus/README.md` | 44 | span `S072–S091` (covers S090, includes S091) | absent; S091 is host bytes but a **pre-existing** row |
| `corpus/knowledge/arc-synthesis.md` | 392 | S090 | absent |
| `corpus/knowledge/closeout-r11.md` | 299 | S090 | absent |
| `corpus/knowledge/config-health-report-r3.md` | 1009 | S090 | absent |
| `corpus/knowledge/remaining-planes-census.md` | 338, 340 | S090 | **denied at :338** |
| `corpus/knowledge/walker-deep-r9.md` | 403 | S090/S096 | **evidence** |
| `corpus/knowledge/walker-deep.md` | 622, 623 | S090/S091/S096 | **evidence at :622** |
| `corpus/knowledge/walker-live-surface.md` | 305 | S090 | **denied at :305** |
| `corpus/knowledge/walker-route-r18.md` | 1, 327, 328 | S072–S091 header (covers S090/S091); S098; S096 at :328 | **evidence at :328** |
| `corpus/knowledge/waybar-walker-plane.md` | 479 | S090 | absent |
| `corpus/knowledge/waybar-walker-semantics.md` | 467 | S090 | absent |
| `tools/mado-verify.sh` | 56, 101, 1258, 1920, 3285 | S090/S096 | **evidence** (sha `25240650…`, 7,039,912 B) |

Tally: S096 cited as evidence **5/13**; S091-only **1/13** (README; and note both README
and route-r18 were already "current" at baseline); S090-only **5/13**; S090 + explicit
S096 denial **2/13**.

No file is credited *only* by an unrelated token. Every token appearing on a crediting
line exists at tip (98 rows, S001–S098, no dangling token), and S090/S091/S096 are all
`mined` at `corpus/SOURCES.md:102`, `:103`, `:108`.

## 3. Findings

### F1 — "sourced on S096" is true of 5/13 credited files; the rest cite pre-existing rows (P)

The pre-registration sentence (`SCORECARD.md:1099-1105`, committed tip) reads: "every
file in the fixed set gains an in-file dated pointer … citing a SOURCES row opened this
round for the host walker bytes (binary rodata version literal + file digest, read as
bytes) and the upstream release". At baseline, `corpus/SOURCES.md` already contains S090
(`:102`) and S091 (`:103`); it contains **no** S096 (baseline S096 count 0, and row ids
stop at S095). So S096 is the only row "opened this round for the host walker bytes",
and only 5 files cite it on a crediting line. The six S090/S091 files cite rows that
were present at `9c54c56`.

The counter as declared (`SCORECARD.md:1083-1084`) is weaker — "a line holding `2.17.2`
and an `S###` row token" — and is implemented faithfully
(`fresh-pins.py:28`); its registry row even discloses "row-id validity is not checked"
(`SKILL.md:577`). So `13/13` is true *under the declared counter* and the results cell's
literal clause "Every credited line cites S090/S091/S096" (`SCORECARD.md:1133`, worktree)
is true, but the cell's leading phrase "**sourced** on S096" overclaims the per-file
provenance: 8/13 credited files carry no S096 citation.

### F2 — Two wave-1 sentences are false at the tip, and S096's row routes to those exact files (P)

```
corpus/knowledge/remaining-planes-census.md:338
  … on 2026-10-20 the host package moved to 2.17.2 per `/var/log/pacman.log:2929`
  (S090); the binary-bytes row S096 is reserved and not yet recorded.

corpus/knowledge/walker-live-surface.md:305
  … On 2026-10-20 the host package moved to 2.17.2: `/var/log/pacman.log:2929`
  (S090); the host binary bytes are reserved as S096 (row pending, not re-read this round).
```

Both sentences are **new in wave 1** (S096 count in each file at baseline: 0; at tip: 1).
At the tip, `corpus/SOURCES.md:108` is `| S096 | host walker version binding …` with
status `mined`, date `2026-10-20`, and its `used-by` column lists
`corpus/knowledge/walker-deep.md, corpus/knowledge/walker-deep-r9.md,
corpus/knowledge/walker-live-surface.md, corpus/knowledge/remaining-planes-census.md,
tools/mado-verify.sh, SKILL.md`. So the artifact simultaneously records S096 as mined and,
in two files it claims to route, states that S096 is not recorded. The counter credits
both files via S090, so the score is unaffected; the contradictory prose is the defect.

### F3 — Neither checker can enforce "sourced on S096"; supersede-sweep enforces only its ledger rows (evidence)

Three mutations in the `/tmp` clone (committed tip as base):

| mutation | `fresh-pins` | `supersede-sweep` |
|---|---|---|
| A: replace S090/S091/S096 with **S999** on `tools/mado-verify.sh` crediting lines, keep `2.17.2` | `mado-verify current=True`, total `13/13` | `pointed=12 stale=1` → `STALE tools/mado-verify.sh` |
| B: `(S096)` → `(S999)` in `walker-deep.md:622`, leaving S090 | `walker-deep current=True`, total `13/13` | `pointed=13 stale=0` |
| C: README span `S072–S091` → `S072–S089` (excludes both permitted rows) | `README current=True`, total `13/13` | `pointed=12 stale=1` → `STALE corpus/README.md` |

B is the exact shape of the six S090-only files: dropping the host-bytes citation is
invisible to both checkers because the ledger's `rows` is `["S090","S096"]` and S090
alone satisfies it (`supersede-sweep.py:117-124`). A and C show the sweep does real work
against unrelated tokens and excluded spans, which `fresh-pins` (`:28`, `:70-72`) does
not. Therefore `13/13` certifies "some permitted row is named", not "S096 is cited".

### F4 — Worktree drift: the results row and the ledger are uncommitted; the documented command is not state-stable (FYI, not a C2 error)

`git status --porcelain` at audit time shows
`M .ufo/waves/round-19/supersessions.json`, `M SCORECARD.md`, `M corpus/QUALITY.md`,
`M corpus/knowledge/theme-route-r18.md`, `M corpus/knowledge/walker-route-r18.md`, plus
untracked w2 files. `supersessions.json` on disk hashes `a0e6cf…` vs committed
`87644b…`; it carries a second entry (`S084-to-S098`). Running the documented
`supersede-sweep.py df84807` from the worktree therefore prints that extra entry, while
the committed ledger prints only `walker-2.17.2 … stale=0`. The C2 results cell
(`SCORECARD.md:1133`) exists only in the uncommitted worktree (`git diff --stat` = +38
lines); the attacked tip ends at the pre-registration (`SCORECARD.md:1120`). All numbers
above are from committed bytes; the quoted results sentence is marked "worktree".

Drift continued after the audit: `SKILL.md`, `PROVINCE.md`, `corpus/knowledge/`
`arc-synthesis.md`, `config-health-report-r3.md`, `walker-deep.md`, `walker-deep-r9.md`,
`remaining-planes-census.md` and `walker-live-surface.md` are now also modified. For F2,
the in-flight edits append correction bullets (`remaining-planes-census.md:341+`,
`walker-live-surface.md:305+`) but leave the false sentences at `:338` and `:305` in
place. All F1/F2 findings are scoped to the attacked committed tip `01b8094`.

## 4. Non-findings (honest attempts that failed to break the claim)

- **S096's host facts reproduce byte-exactly** (file reads only): `/usr/bin/walker`
  7,039,912 B, sha256 `25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096`,
  BuildID `19200fe47eb6c90fc4956f0d52d0c7c84bb89e99`; whole-file counts `2.17.2` = 1,
  `2.17.0` = 0; offset 856,302 reads `…loadstruct Action with 6 elementsversion2.17.2\ntoggle exact sear`.
  `walk`-package `desc` 407 B sha256 `5c0d9d89…50b0928`, `%VERSION%` `2.17.2-1`,
  `%BUILDDATE%` `1791468872`, `%INSTALLDATE%` `1792498606`. `/var/log/pacman.log`
  244,858 B sha256 `27bbd0b5…b256ffc`; lines 1943, 2929, 3062, 3095, 3123 read exactly as
  S090 states.
- **Gate re-pin is real**: `tools/mado-verify.sh:105` `WALKER_VERSION_PIN="2.17.2"`,
  stub default at `:1242`, FAIL arms at `:1279`/`:1281`, PASS narrowed to
  "installed version matches pin; claims measured on 2.17.0 … stay dated" at
  `:1265-1267`, live row at `:3296-3298`. The `st_not_has … "2.17.0"` at `:1291` is not
  contradictory: it evaluates the WL3 (absent-binary) output, which names only 2.17.2.
- **No dangling or unrelated-token credit**: all S tokens on crediting lines exist at tip;
  S084 appears on `walker-route-r18.md:1`/`:327` but both lines also carry permitted
  tokens and `:327` states S084 is replaced/rejected (`SOURCES.md:96` status `rejected`).
- **Residual old pins are counted current by design**: 11/13 files still contain
  present-tense `2.17.0` pin lines; `13/13` means "pointed", not "re-measured". The
  results cell itself says "dated provenance, not re-measurement", so this is a
  calibration caveat, not a counter error (w1 CriticC2 asked for exactly this wording).

## Limits

- I did not run the gate (`--selftest`/`--regression` allowed but not my assignment);
  the 443/443 harm-watch figure is taken from the SCORECARD and is `[UNK]` to me.
- I did not verify the upstream release rows (S072–S089) against fetch receipts; I read
  their existence/status only.
- The worktree was being edited by peers during the audit; every C2 number above is from
  committed bytes in `/tmp/c2clone`, except the quoted results row (marked worktree).
- Overlap: `w2/reports/CriticC2W2.md` (F1) and `w2/reports/AtkPtrWalkerLiveSurface.md`
  independently report the S096 denial. My audit confirms it from committed bytes and
  adds the 13-file token census, the both-rev re-runs, and the mutation proof. Not double
  counted.
- Host pause respected: only `sha256sum`/`python3 open()`/`readelf`/`stat` file-byte
  reads of `/usr/bin/walker`, the walker `desc` and `/var/log/pacman.log`; no pacman,
  service, compositor or walker execution.

## Installs

none.

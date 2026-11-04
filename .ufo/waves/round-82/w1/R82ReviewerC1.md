# R82ReviewerC1 — C1 attack: the client's own band

Seat: R82ReviewerC1 · round 82 · lane `mado-shokunin` · read-only.
Claim: C1 (`claims-declaration-r82.md`, freeze `780c30fcae12d74ce8ab3b871a0888696c2415d9`,
base `6ea2386d49318a5f223097c78b5fe79c31b064f8`).
No frozen instrument was edited, no git mutation was run. Every write was under
`/fast/scratch/hyaku/mado-r82/R82ReviewerC1/` (removed at exit) and this file.

## Evidence base (independently verified)

| check | result |
|---|---|
| `tools/mado-barfoot.py` sha256 | `380075284d7d5c6f…bcab59` — matches the claim prefix |
| `quality/counters/c1-r82-allocation-band.py` sha256 | `1e9f394df80284e7…4612d` — matches |
| `quality/counters/c2-r82-runbook.py` sha256 | `1e8eb49928bfc9b8…3fb0f` — matches |
| `controls/c1-cases-r82.json` sha256 | `e404bb3fa93d5f12…4a315f` — matches |
| `controls/c2-runbook-cases-r82.json` sha256 | `f64d7d5db40fc1da…b36d5` — matches |
| freeze → HEAD drift on frozen instruments | none: `git diff --stat 780c30fc..HEAD -- tools/mado-barfoot.py quality/counters/ .ufo/waves/round-82/controls/` is empty; the only post-freeze commit is `b6146ee6` (wave evidence) |
| tool selftest | `MADO_BARFOOT_SELFTEST: 133/133`, rc 0 |
| counter selftest | `MADO_R82_BARFOOT_SELFTEST: 84/84`, rc 0 |
| counting command replayed at HEAD | rc 0, `cases=47 correct=47 mutants=34 killed=34 base_correct=39/47 carried=39/39 tool_selftest=133/133 verdict=TARGET_MET`; the 84-line output is byte-identical to `receipts/measurement-c1-r82.txt` after stripping the `rev=` field (mine: `b6146ee6`, whose `tools/` tree equals the freeze's; the receipt's `780c30fc`) |
| control set | 47 cases; `cases[:39] == r81 cases` parsed-equal **True**; the eight new names are the `alloc-*` set; `len(MUTATIONS) == 34` |
| before-revision receipt | `receipts/control-c1-r82-at-base.txt`: `correct=39`, `killed=28` (the six `alloc-*` mutants are `anchor-absent` at the base), `base_correct=39/47` — consistent |
| base tool identity | git blob `0e9fa2205bfcc3bb98dbe317527432a8752e91d2`; `a129a435…` is its **content sha256**, not a blob (see F3) |

Method note: **no `lsp` device is exposed to this seat** (the toolset carries none), so caller /
definition checks below are literal call-site reads, not semantic indexing. The complete call
paths are: `band_of` at `tools/mado-barfoot.py:481`, `:482`, `:803`; `surface_zone` at `:641`,
`:837`; `declared_box` at `:1004` (single-surface path only — the composition path uses
`arranged_box`). That distribution is load-bearing for §2.

## 1. Re-derivation of the eight `alloc-*` cases

All eight expectations are hard-coded in the control JSON, not copied from a tool run: the
builder imports only `json` and `os` (no subprocess), so it cannot invoke the tool, and its
module comments (`.ufo/waves/round-82/controls/make-c1-cases-r82.py`, cases 1–8) state the same
chain I derive below.

| # | case | derived box | derived band | verdict | deciding bytes |
|---|---|---|---|---|---|
| 1 | `alloc-dyn-height-top` | `0,0,3440,34` | 34 | **AGREE** | S481:128-131 (a 0 size is the client's omission; the configure assigns it); S464:276 (`zone = current_allocation.height`), :278/:280 (top anchored → no +top, bottom unanchored +0); S470:2623-2628/2635-2637 (box `0,0,3440,34`), :2575 (zone+marginTop=34>0 → `usable.y += 34`) |
| 2 | `alloc-dyn-height-margin` | `4,4,3432,30` | 38 | **AGREE** | S464:276 + :278/:280 → 30+4(unanchored bottom)=34; S470:2575/2651 → 34+4(anchored top)=38; box from S470:2635-2637 (`x=m.left=4,w=3432`) and :2650-2651 (`y=m.top=4,h=30`) |
| 3 | `alloc-dyn-width-dock` | `0,0,60,1440` | 60 | **AGREE** | S464:282 + :284/:286 → 60+0(unanchored right)=60; S470:2614-2615/2640-2641 (`x=0,w=60`), :2645-2647 (height 0 → span 1440); :2575 (60+marginLeft 0) → `usable.x += 60` |
| 4 | `alloc-zero-refused` | — | — | **AGREE** (see F2: vacuous vs r81) | tool `:468-470` refuses `band <= 0`; grounded in S470:2575's `exclusive + margin > 0` guard (a zero zone reserves nothing); rc 3 stage=model from `:1571-1573` |
| 5 | `alloc-negative-refused` | — | — | **AGREE** | tool `:450` raises `Setup`; rc 2 stage=setup from `:1574-1576`; a negative size is not a `uint32` size request (S481:122-131) |
| 6 | `alloc-unknown-namespace` | — | — | **AGREE** | single path `:962` (`set(allocation) - {bar ns}` = `{'panel'}`) → `Setup` rc 2; the composition-path check (`:769-770`) would reject it too, since no declared surface carries `panel` |
| 7 | `alloc-explicit-ignored` | `0,0,3440,26` | 26 | **AGREE** | tool `:461` returns the positive declared band before consulting the map; box h=26 (S470:2650-2651); the 40 is discarded by the declared-wins rule |
| 8 | `alloc-composition-dyn-bar` | bar `0,0,3440,34`; panel `0,34,3440,100` | 46 | **AGREE** | bar: `:803` injects height 34; S470:2610-2611/2623-2628/2635-2637 → `0,0,3440,34`; S464:276 → zone 34; S470:2664 → usable `{0,34,3440,1406}`. panel level 3: S470:2623-2628 (h=100, anchor top → y=bounds.y=34) → `0,34,3440,100`, which equals the case's live entry; zone 12 → usable `{0,46,…}`; S466:33-34 → ls.top=46, attribution 34+12=46 |

Direct answers to the two flagged cases:

- **`alloc-dyn-height-margin` — does the band add the unanchored margin and then the anchored
  one?** Yes, exactly: `allocation 30` → gtk auto zone `30 + 4` (the *unanchored bottom* margin,
  S464:276-280) `= 34` → Hyprland `applyExclusive` adds the *anchored top* margin
  `34 + 4 = 38` (S470:2575). Both margins are counted once, no double count: the box occupies
  `y∈[4,34]`, the reserved region is `[0,38]`. The tool's single-surface path reaches 38 by
  `extent (4+30) + opposite margin (4)`, which is algebraically the same total.
- **`alloc-composition-dyn-bar` — does the level-3 panel really arrange at y=34?** Yes. The
  bar's pass shrinks the usable box to `y=34` before the panel is arranged (S470, per-surface
  `applyExclusive` at `:2664` inside the level-ordered loop); the panel's own `y = bounds.y`
  (h=100 ≠ 0, anchor top, S470:2627-2628) is 34, and the case's live panel entry is
  `{x:0,y:34,w:3440,h:100}`. Its 12 px then takes the band from 34 to 46.

No DISAGREE.

## 2. Classes the tool accepts but does not model

**(a) The allocation map is accepted for a carried non-bar namespace and then never resolved.**
`evaluate_composition` builds `known = {bar} ∪ extras` (`tools/mado-barfoot.py:769`) and lets
`--allocation {"panel": N}` through, but only the bar's band axis goes through `band_of`
(`:803`). Reproduced against the frozen tool (my scratch, files below):
`config {height:26, position:top}`, `layers` waybar `0,0,3440,26` + panel `0,26,3440,40`,
`surfaces [{"namespace":"panel","level":3,"height":0,"exclusive":"auto"}]`,
`allocation {"panel":40}` →

```
MADO_BARFOOT: ERROR (stage=model auto zone on a dynamic height (0) is the client's allocation, not a declared value)
```

i.e. the tool refuses a declared dynamic band **while holding the declaration**, and its message
says the client's allocation is missing (`:615`, `:625`). With an explicit zone instead of
`auto` the same panel is arranged as the **full span** (`arranged_box` h==0 branch,
S470:2645-2647) and the join reports a false DIFFER:

```
DECL level=3 ns=panel box=0,26,3440,1414 zone=12
LIVE level=3 ns=panel box=0,26,3440,40 entries=1
RESULT box=MATCH boxes=MATCH,DIFFER reserved=GT band=78 expected=38 attributed=38 verdict=DIFFER
```

The live composition here is the one the claim's model describes (panel band = the declared 40,
arranged at y=26), yet the tool says DIFFER. Finally, the entry is not merely unsupported but
silently discarded: with the same fixture and allocation `{"panel":40}` vs `{"panel":999}` the
output is **byte-identical**. This is F1.

### Replay (no scratch needed)

```
# F1 refusal — fixtures, then:
#   python3 -I tools/mado-barfoot.py --config C --layers L --monitors M --surfaces S --allocation A
C = {"height":26,"layer":"top","position":"top"}
L = {"M1":{"levels":{"0":[],"1":[],
     "2":[{"namespace":"waybar","x":0,"y":0,"w":3440,"h":26,"alpha":1.0,"pid":4242}],
     "3":[{"namespace":"panel","x":0,"y":26,"w":3440,"h":40,"alpha":1.0,"pid":4242}]}}}
M = [{"name":"M1","width":3440,"height":1440,"reserved":[0,66,0,0],"scale":1.0,"transform":0}]
S = [{"namespace":"panel","level":3,"height":0,"exclusive":"auto"}]        # → rc 3, stage=model refusal
A = {"panel":40}
# S with "exclusive":12 → rc 1: DECL panel box=0,26,3440,1414 vs LIVE 0,26,3440,40, verdict=DIFFER
# A = {"panel":999} → byte-identical output (the declaration is discarded)
```

```
# F2 — base-tool behaviour score: extract the base tool, then for each of the 47 cases write the
# files with the counter's own case_files() and run the tool WITHOUT --allocation; score with
# expected_ok(). Result: 41/47 (failing dyn-height-top, dyn-height-margin, dyn-width-dock,
# negative-refused, unknown-namespace, composition-dyn-bar).
git show 6ea2386d49318a5f223097c78b5fe79c31b064f8:tools/mado-barfoot.py
```

**(b) An allocation larger than the monitor is accepted and yields a zero reserved band.**
`height:0`, `allocation {"waybar":5000}` on a 1440-high monitor: the box is `0,0,3440,5000`
(matches a live entry of the same), `contained` is false, contribution 0 → `band=0 expected=0
verdict=CLEAN`. That is consistent with `CReservedArea(parent, child)`'s parent/child
short-circuit on an uncontained child (S466:20-31), which leaves the invalid area empty, and
with the carried `ls-area-invalid` ground, so not a contradiction — but note
the asymmetry: the tool refuses a zero *allocation* while accepting an allocation that produces
a zero *reserved* band.

**(c) A duplicate declared namespace is not refused.** Two `panel` entries at the same level
reuse the single live entry, double-count the attribution, and end in `DIFFER`
(`expected=106 band=66`). Fails closed unless the monitor band happens to equal the double
count; low risk, worth a `Setup` refusal if duplicates are out of contract.

**(d) Positive tests that hold.** `alloc-zero-refused` (a zero band reviewed as a band) →
refused, stage=model. `alloc-unknown-namespace` → setup refusal. A negative allocation → setup
refusal. An allocation alongside an explicit band is ignored by the declared-wins rule (tested
transposed too: `position:left,width:60,height:0,allocation 77` → CLEAN band 60). An allocation
"on a non-band axis" is unrepresentable: the map is a scalar per namespace and is applied to the
band axis only.

## 3. Counter assertions and the do-nothing control

- `CASES=47` = `len(cases)`; `CARRIED=39` = `len(carried)` and `cases[:39] == carried`
  (parsed-equal, verified by me); `MUTANTS=34` = `len(MUTATIONS)`; `BASE_EXPECT=39` = the base
  run's `base_correct`. `main` enforces all four (case-count check, carried-set equality,
  `killed == MUTANTS`, `base_correct == BASE_EXPECT`). All hold.
- **The eight new cases on the held round-81 tool.** With the counter's exact argv all eight
  fail — but only because `--allocation` is an unknown argument (argparse rc 2). Re-running the
  **same 47 cases against the base tool without the flag** scores **41/47**: the 39 carried pass,
  plus `alloc-zero-refused` and `alloc-explicit-ignored`. The six that fail behaviourally are
  `alloc-dyn-height-top`, `alloc-dyn-height-margin`, `alloc-dyn-width-dock` (base rc 3, blanket
  dynamic refusal), `alloc-negative-refused` (base rc 3 vs expected 2),
  `alloc-unknown-namespace` (base rc 0 CLEAN vs expected 2) and `alloc-composition-dyn-bar`
  (base rc 3). So **6 of 8 are behaviourally new, 2 of 8 are not**; the 39/47 is an argv-level
  delta for those two. `alloc-zero-refused` is the sharper case: the r81 tool refuses *every*
  dynamic band at stage=model, so the case's assertion is satisfied vacuously and does not by
  itself evidence "a zero allocation is refused". It does kill `alloc-zero-accepted` (sole
  killer), so it has discriminating power against the *diff*, not against the *class*.
- **Mutant necessity.** Four of the 34 mutants are killed **only** by new cases:
  `alloc-zero-accepted` (by `alloc-zero-refused`), `alloc-negative-accepted`,
  `alloc-unknown-kept`, `alloc-composition-ignored`. Seven of the eight new cases are the killer
  of at least one mutant; `alloc-dyn-width-dock` kills none (F4). The new cases are doing real
  work.
- **Before revision.** `killed=28` with the six `alloc-*` mutants `anchor-absent` (the mutator
  cannot find the new source lines at the base). The kill rule counts an absent anchor as not
  killed, so the before/after pair is honest, but it is "inapplicable", not "survived".

## 4. Strongest objection, fatal vs named limit

**Strongest objection.** The claim's headline and point 3 are surface-generic — "a declared
dynamic band (`height = 0` on a horizontal surface …)", "the model resolves the band axis
through one resolver (`band_of`)" — and the `--allocation` key is `{namespace: band}`. The
implementation is bar-only: the map's *acceptance* is namespace-generic (`:769-770`) while its
*resolution* is one call on the bar (`:803`). Demonstrated above: with the allocation declared
for a declared non-bar surface, the tool either refuses with a message that says the client's
allocation is missing, or mis-arranges the surface as a full span and returns a false DIFFER on
a live composition that matches the claim's own model.

**Verdict: not fatal to the measured predicate, fatal to the claim's unqualified wording.**
The frozen target is reproducible exactly (`47/47`, `34/34`, `39/47`, `39/39`,
`tool_selftest=133/133`, rc 0; receipt byte-identical modulo `rev`), and the class the claim's
point 2 names ("a dynamic bar's zone") is genuinely modelled. But point 3's "one resolver" and
the headline's unrestricted "a declared dynamic band" are false for any surface that is not the
bar, and the tool's input contract accepts a declaration it never uses. This must be either
narrowed to the bar's namespace in the round record or fixed by resolving every carried
surface's band axis; it is a **defect**, not a modelling limit the claim names.

Second, independent objection (§3): the do-nothing control's "the eight new cases are
unreachable" is true only of the flag, not of the model — 2 of 8 pass on the held tool at
behaviour level (41/47) and one of them passes vacuously. That is a **named limit** of the
control's strength, not fatal: six cases still require the allocation, so 47/47 is not reachable
by doing nothing.

## Findings by severity

**F1 — medium, defect — accepted-then-unignored allocation for non-bar namespaces.**
`tools/mado-barfoot.py:769-770` admits an allocation entry for any namespace in the composition
(bar ∪ declared surfaces); `tools/mado-barfoot.py:803` resolves only the bar. Consequences:
`tools/mado-barfoot.py:615` / `:625` refuse a declared dynamic band on a declared surface while
the declaration is in hand ("…is the client's allocation, not a declared value"), and the
explicit-zone path arranges the surface as the full span and emits `verdict=DIFFER` on a
composition that matches the claim's model. Repro fixtures and outputs in §2(a). The tool's own
docstring scopes the class to "a horizontal bar"/"a vertical bar"
(`tools/mado-barfoot.py:54-58`), so the narrow reading is defensible — but in that reading
`:769-770` is still wrong to admit `panel` into `known`: the declaration is accepted and
silently discarded, and `:615`/`:625` then say the client's allocation is absent when it is
present. Either reading leaves a real defect. Not fatal to the frozen 47, but the claim's
"one resolver"/"a declared dynamic band" cannot stand unqualified.
Fix: pass every carried surface's band axis through `band_of` (and resolve the extra's zone from
the same value), or reject an allocation for a non-bar namespace at setup so the input is never
silently discarded.

**F2 — low-medium, control caveat — the 39/47 is partly argv-level.**
The same 47 cases on the base tool without `--allocation` score 41/47
(`alloc-zero-refused`, `alloc-explicit-ignored` pass). The claim's do-nothing sentence
"the eight new cases are unreachable without the allocation input" holds only for the CLI flag;
the behavioural delta is 6. `alloc-zero-refused` passes on r81 vacuously (r81 refuses all
dynamic bands at stage=model). The frozen predicate itself is exact and reproducible.

**F3 — low, citation defect — claim point 1's line range does not match the pinned bytes.**
In `.ufo/waves/round-82/fetch/S481.xml` the `set_size` request opens at **:122** and the
zero-size clause is **:128-131** ("If you pass 0 for either value, the compositor will assign
it…"). The claim cites `set_size :116-123`, which is the interface description/unmap text and
`:123` is the request's `<description>` tag — the cited range contains no size clause. Related:
the claim calls `a129a435…` "the blob at the base"; it is the content sha256 (the git blob is
`0e9fa220…`). The substance (allocation, not config, is the band) is correct and S464:276/282
are cited correctly.

**F4 — low, mutation-coverage gap — the vertical branch of the resolver has no named mutant.**
`tools/mado-barfoot.py:482` (`width = band_of(...)` for left/right) is not covered by any of the
34 mutations; `alloc-dyn-width-dock` is the only case that binds it. I built the missing mutant
(`width = bar["width"]` in place of the `band_of` call) and the frozen 47 kill it with exactly
that one case (`alloc-dyn-width-dock`), so the case is live — the mutation list under-covers the
width branch.

**F5 — low, process/R4 — C1 selftest transcripts are not under `receipts/`.**
The frozen declaration's R4 repair says "`--selftest` transcripts land under `receipts/`". The
C1 counter `84/84` and tool `133/133` transcripts live only in
`/fast/scratch/hyaku/mado-r82/R82ExecC1Run/` (`counter-selftest.out`, `tool-selftest.out`);
`receipts/` holds only `gate-selftest-r82.txt` (`460/460`, a different gate). The tallies are
true — I re-ran both — but the declared landing spot is empty.

## Residual risk and verification gaps

- No live compositor or session bus was exercised: all band arithmetic is derived from the
  pinned bytes (S464:263-292, S470:2529-2586/2606-2668, S466:20-34, S481:122-131) plus the
  frozen case data. Whether a real waybar's `current_allocation` equals the declared number is
  outside what a read-only seat can observe.
- The composition path never runs a dynamic band with a **non-zero** margin: the margin case
  (`alloc-dyn-height-margin`) is single-surface, where `surface_zone` is never called
  (`:641`/`:837` are composition-only). The gtk-zone → Hyprland-margin chain with margins is
  therefore bound by algebra, not by a composition case. The composition margin addition itself
  is bound by a carried case (mutant `zone-margin-not-added` fails on a carried case, 38/39
  carried-correct).
- The single-surface path (`declared_box` at `:1004`) and the composition path (`arranged_box`
  + injected band at `:803`) compute the band by two different formulas. I checked their
  equality for top and left; bottom/right follow by the same transposition and are covered by
  `declared_box` selftest rows (`:1488-1497`), not by new cases.
- 7 of the 8 new cases kill at least one mutant; `alloc-dyn-width-dock` kills none (F4).
- No `lsp` device in this seat; call-path claims are literal reads, not semantic indexing.
- I did not re-test the GT second-consumer attribution beyond the carried `second-consumer` case.

No tool was installed or upgraded (python3 stdlib only).

Defect named: `tools/mado-barfoot.py:769-770` with `:803` (allocation accepted for non-bar
namespaces and never resolved; refusal `:615`/`:625` and false DIFFER as consequences).

STATUS: defect

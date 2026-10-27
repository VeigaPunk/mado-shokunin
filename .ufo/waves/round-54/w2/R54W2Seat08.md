# R54W2Seat08 — w2 falsification: item 8, C1 widened P21 anchor (span-equality vs containment)

- Seat `R54W2Seat08`, role reviewer, wave `w2`, item **8** ("C1 widened P21 anchor. Widen P21 range while
  retaining quote; compare span-equality to containment.").
- Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`; base `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`;
  lane HEAD at w2 dispatch `350d30e4ec5531f65ce99a57efeb8216f38e678a` (freeze/pins commit; content-identical
  for every C1 input this item touches — pin sha256 re-verified at BOTH revs, § B).
- Attacked contract: **PRED-C1-r54 clause (b)** — the P21 anchor side-claim — and the C1 frozen control set's
  ability to enforce it.
- No predicate, registration, lane file, source file, sibling report or git state was changed. All mutations
  live in a `--shared` clone under this seat's scratch, deleted before yield. No delegation, no background
  jobs, no host reads, no network, no tool installs.

## Axes (godspeed)

1. **Operability** — can the frozen sentence's "at exactly" be *enforced* by a deterministic command, or only
   recited? A control set that cannot separate span-equality from containment lets a containment counter print
   the frozen line on trees the frozen sentence condemns.
2. **Coverage** — does the frozen control inventory cover the widening axis of the P21 anchor, or only the
   displacement axis (`:573`)?

## A. Pinned command status: NOT RUN / absent

```
$ ls /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters | grep -c r54
0
```

`quality/counters/c1-r54-errata-truth.py` does not exist at w2 dispatch (lane HEAD `350d30e4`, worktree
grep count 0). The frozen predicate command was therefore **NOT RUN — absent**. What was re-run instead, and
is labeled as such everywhere below: the two C1 draft counters w1 published verbatim in its wave reports
(R54Seat02 Appendix A "verified core"; R54Seat04 Appendix A full 844-line draft), plus this seat's clearly
labeled semantic probes built only from those published primitives. Nothing below is presented as the pinned
counter's output.

## B. Ground truth on the frozen bytes (read-only, both base revs)

Pin `Hyprland-legacy-DispatcherTranslator.cpp`, `.ufo/waves/round-52/fetch/`:

```
$ for r in e25149fe 350d30e4; do git show $r:.ufo/waves/round-52/fetch/Hyprland-legacy-DispatcherTranslator.cpp | sha256sum; done
7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771   # == registration.md:19 recorded
7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771   # identical
```

Lines 619–622 (`cat -A`):

```
    auto result = sendshortcut(modifiedArgs);$
$
    if (keyState == 2 && result.success)$
        result = sendshortcut(modifiedArgs);$
```

So the quote's **occupied line set is {619, 621, 622}** — blank line 620 sits inside the frozen anchor
`619-622`. Direct judge probes over the whole pin:

| reading | P21 quote present |
|---|---|
| raw bytes | **no** |
| interior newlines → single space (the ONLY normalization `registration.md:51-53` authorizes, and only when the quote cell itself carries a newline — P21's cell carries none) | **no** |
| join(619, 621, 622) with blank 620 dropped, each line stripped | **yes** |
| join(619–622) with blank kept, whitespace-collapsed | **no** (double space at the blank) |

The located span under the w1 draft's collapse (blank-drop, run-start line map) is **exactly (619, 622)** —
measured, not assumed: `P21 located span(s) at base under Seat02 collapse: [(619, 622)]`.

Contract lines attacked:

- `claims-frozen.md:24-27` — clause (b): "each anchor side-claim holds (… **P21 at exactly**
  DispatcherTranslator.cpp:619-622 inside lines 591–627 …)"; clause (a) requires the Quote cell "occurring
  verbatim and contiguous in the round-52 pin named by its Pin:anchor cell".
- `registration.md:33` — "P21 at exactly lines 619–622 with `591 ≤ 619` and `622 ≤ 627`".
- `registration.md:22` — entry rows "checked … against THIS table byte-for-byte modulo trailing spaces; any
  drift is a TARGET_MISSED".
- `registration.md:45` — the only range control: "C1-CTL-4 wrong-range | P21 anchor moved to `:573`
  (outside 591–627) | anchor side-claim fails → MISSED".
- `registration.md:51-53` — the verbatim judge note ("P19/P21/P22 are single logical lines").

## C. Fixture: widened anchors committed in an isolated clone (exact commands/outputs/exits)

```
$ mkdir -p /fast/scratch/hyaku/mado-r54/R54W2Seat08 && cd /fast/scratch/hyaku/mado-r54/R54W2Seat08
$ git clone --quiet --shared --no-hardlinks /home/vgpnk/Projects/shokunin/mado-shokunin fixture
$ git -C fixture rev-parse --show-toplevel      # == the fixture dir, asserted before every commit
/fast/scratch/hyaku/mado-r54/R54W2Seat08/fixture
```

Each variant rewrites only the P21 `Pin:anchor` cell of the committed entry
(`corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md:19`) in a clone of `350d30e4`; quote cell,
pin cell, and every other byte are untouched. Driver: `fixture_item8.py` (in scratch; asserts
`rev-parse --show-toplevel == D` before each commit; local fixture identity only). Resulting commits:

| variant | P21 anchor cell | commit |
|---|---|---|
| base | `:619-622` | `350d30e4ec5531f65ce99a57efeb8216f38e678a` |
| wA | `:619-627` (end widened into the side-claim boundary) | `578d7a67ceba61320000f058b0640a10f87f26d2` |
| wB | `:591-627` (the whole frozen window — maximal containment) | `8c86fd658b8739f596dbd0b731a84680da80efa7` |
| wC | `:610-626` (both bounds moved, strictly inside the window) | `7cf5cf97f3c65edb3f8ebc939560e4e3fb682546` |
| ctl4 | `:573` (the frozen C1-CTL-4 mutation, rebuilt) | `ff32a79a7e6c066741917fefa5771ede4173bb51` |

### C1. Re-run of the w1-published draft counter (R54Seat04 Appendix A, 843 lines extracted, `ast.parse` OK)

`python3 -I seat04_counter.py --repo <fixture> --rev <rev> --work <scratch>/work04`:

```
[base  rev=350d30e4ec55] exit=0 MADO_ERRATA_TRUTH: rev=350d30e4… propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
[wA    rev=578d7a67ceba] exit=1 MADO_ERRATA_TRUTH: rev=578d7a67… propositions=4/4 quotes=4/4 anchors=3/4 pins=4/4 controls=6/6 verdict=TARGET_MISSED
[wB    rev=8c86fd658b87] exit=1 MADO_ERRATA_TRUTH: rev=8c86fd65… propositions=4/4 quotes=4/4 anchors=3/4 pins=4/4 controls=6/6 verdict=TARGET_MISSED
[wC    rev=7cf5cf97f3c6] exit=1 MADO_ERRATA_TRUTH: rev=7cf5cf97… propositions=4/4 quotes=4/4 anchors=3/4 pins=4/4 controls=6/6 verdict=TARGET_MISSED
[ctl4  rev=ff32a79a7e6c] exit=1 MADO_ERRATA_TRUTH: rev=ff32a79a… propositions=4/4 quotes=4/4 anchors=3/4 pins=4/4 controls=6/6 verdict=TARGET_MISSED
```

Rejection detail for wA: `detail: P21 anchor 619-627 differs from the frozen table 619-622` and
`detail: P21 quote spans [(619, 622)], anchor names 619-627`. This draft enforces BOTH table equality and
span equality, so it rejects every widening — but note the reject lands on `anchors=3/4` alone; its
`propositions` leg does not carry the anchor cell.

### C2. Four-design isolation (Seat02 Appendix A primitives; only the anchor/table leg varies)

Designs — **A** span-equality + frozen-table leg (the Seat02 draft's own semantics), **B** containment +
frozen-table leg, **C** containment + row-authority (no table leg; the "semantic-only" shape Seat27's w1
matrix labeled ADMIT for P20), **D** span-equality + row-authority. Counts are
propositions/quotes/anchors/pins:

```
tree           A span-eq+table   B contain+table C contain+rowauth D span-eq+rowauth
base        4/4 4/4 4/4 4/4 MET4/4 4/4 4/4 4/4 MET4/4 4/4 4/4 4/4 MET4/4 4/4 4/4 4/4 MET
wA-619-627  3/4 4/4 3/4 4/4 MISSED3/4 4/4 4/4 4/4 MISSED4/4 4/4 4/4 4/4 MET4/4 4/4 3/4 4/4 MISSED
wB-591-627  3/4 4/4 3/4 4/4 MISSED3/4 4/4 4/4 4/4 MISSED4/4 4/4 4/4 4/4 MET4/4 4/4 3/4 4/4 MISSED
wC-610-626  3/4 4/4 3/4 4/4 MISSED3/4 4/4 4/4 4/4 MISSED4/4 4/4 4/4 4/4 MET4/4 4/4 3/4 4/4 MISSED
ctl4-573    3/4 4/4 3/4 4/4 MISSED3/4 4/4 3/4 4/4 MISSED4/4 4/4 3/4 4/4 MISSED4/4 4/4 3/4 4/4 MISSED
```

Read directly: under containment the **anchors leg itself scores 4/4 on every widened tree** (designs B and C);
only the frozen-table leg (B) or span-equality (A/D) catches the drift. Design C — row-authority +
containment, six frozen controls all still rejected — prints `verdict=TARGET_MET` on trees whose P21 row no
longer states the frozen anchor at all. And C1-CTL-4 (`:573`) is rejected under **all four designs**: the
single frozen range control cannot discriminate the two semantics.

## D. Findings by severity

**F1 — HIGH (gameability the frozen controls do not close): no frozen control separates span-equality from
containment for P21; a containment counter passes C1-CTL-4 and admits widened anchors.**
`registration.md:45` is the only anchor-range control and its mutation (`:573`) lies outside the 591–627
side-claim window, so it fails under BOTH semantics (measured: MISSED in all four designs, § C2). Meanwhile
wA/wB/wC — anchor `:619-627`, `:591-627`, `:610-626`, quote retained verbatim — are **admitted by the
containment anchors leg (4/4)**, and a row-authority+containment counter scores the full frozen line
`verdict=TARGET_MET` on them (§ C2, design C) while every one of the six frozen controls is still rejected.
On such a tree the printed sentence asserts "P21 at exactly DispatcherTranslator.cpp:619-622" against an
entry that says `:591-627`: the frozen sentence is no longer enforced by the frozen controls. The kill rule
("if any real pin, quote, or anchor mis-verifies …") is defined by the counter's semantics, and the freeze
does not pin the semantics on the widening axis. Remedies are pre-data only (this seat changed nothing): a
re-registered control set should include a widened-anchor mutation (e.g. P21 `:619-622` → `:619-627`,
required MISSED) and/or freeze that the anchors leg is span-equality, never containment.

**F2 — MEDIUM (the "exactly" in the P21 side-claim is normalization-relative):** `registration.md:51-53`
authorizes newline normalization only where the quote cell itself carries a newline and declares P21 a single
logical line; but the pin's anchor window contains blank line 620, so the quote is absent raw and absent
under the authorized reading (§ B table). "P21 at exactly lines 619–622" is satisfiable only as the
**blank-elided bounding span** — whitespace-run collapse plus blank-line dropping, an unstated
normalization — under which the located span is exactly (619, 622) (measured). Consequence: any span-equality
judge for P21 silently adopts the forbidden normalization (w1 measured the strict base at 1/4 — R54Seat35.md
§ battery, R54Seat16.md:75), and "exactly" has no normalization-independent meaning. F1's widening judgment
is therefore relative to that reading; under strict bytes the predicate self-fails at base for P21 (and
P19/P22) regardless of anchor semantics.

**F3 — LOW (both published w1 drafts already reject widening; the risk is the landing choice):** Seat02's
core (design A) rejects wA/wB/wC on both legs (propositions 3/4, anchors 3/4); Seat04's draft rejects on the
anchors leg with `anchor_frozen` table equality in addition (§ C1). Seat04.md:184-189 and Seat03.md:258 (D8,
P22) had already reported single-draft rejections, Seat02.md:162-169 had named the containment/equality gap
("C1-CTL-4 … cannot discriminate containment from equality"), Seat27.md §3 D1 had ADMITted a widened P20
anchor (`:1574-1578`) under row-authority+containment, and Seat35.md:122-141 had run the four-oracle battery.
This seat's distinct contribution: the P21 widening executed as three fixture commits, the four-design
isolation showing the containment anchors leg at 4/4 on widened trees, and the direct CTL-4
non-discrimination measurement — turning w1's design-level claims into executed counterexamples. No w1 seat
had committed a widened **P21** anchor tree.

## E. Residual risk and verification gaps

- The pinned counter is absent; every result above is a re-run of w1-published draft code or a labeled probe
  derived from it. Which semantics the finally landed `c1-r54-errata-truth.py` implements is undetermined at
  w2 dispatch — F1 is a risk about that choice, not a measured defect in a landed counter.
- All runs are local git-object reads over the fixture; no network, host, or producer execution, so nothing
  here re-verifies the pin↔upstream-commit association or C2 surfaces (out of item scope).
- Strict-judge base behavior (1/4 quotes) is cited from w1 measurements (Seat35/Seat16) and reproduced
  analytically for P21 only (§ B); this seat did not re-run the other three propositions' strict matrix.
- Scratch contained `__pycache__/` from the driver import — removed with the rest of the scratch dir; no
  ENOSPC observed, no scratch remains.

## F. Guard compliance

Only written paths: this report, `/fast/scratch/hyaku/mado-r54/R54W2Seat08/**` (fixture clone, extracted
drafts, driver, work dirs) — all removed before yield. Every fixture commit was preceded by
`git -C D rev-parse --show-toplevel == D`; fixture identity is local to the clone. No lane, fleet, sibling,
or tracked-file writes; no git/jj mutation outside the fixture; no installs.

Report: `.ufo/waves/round-54/w2/R54W2Seat08.md`

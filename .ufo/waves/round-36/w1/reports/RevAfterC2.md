# RevAfterC2 — residual attack on the landed C2 measurement

Seat `L1Mado36.RevAfterC2`. Read-only on every production file; every mutation below
happened in `/tmp/c2attack2` (unhardlinked clones of LANE at `a5f76c9`), never in LANE.

Tip moved twice during this pass: `2d90524` → `a5f76c9` (04:51:47, the gate's supersede
exemption) → `f77b554` (the receipt re-pin). Measurements were taken at
`a5f76c9a018319ae04dea9206f5339325a41b31d` and every claim was re-checked at the final tip
`f77b55478402afbb77fdc1f18e3826ac2c6e96d5`:

```
$ git rev-parse HEAD
f77b55478402afbb77fdc1f18e3826ac2c6e96d5
$ python3 -I quality/check-evidence-pointers.py --rev master   # unchanged at the new tip
PRED-PTR-r36-v1 rev=master pointers_r35=8 dangling_r35=2 dangling_r35_closed=1 pointers_r36=34 dangling_r36=0 inherited_dirty=0 scratch_tracked=124 scratch_disposition_ok=1 tip_axis_transcript=1 setup=ok verdict=TARGET_MET
```

Gate blob on disk and at both tips: `568d5fd9…`; the same file at `cf175c7`/`2d90524` is
`505c900`. Every claim below is pinned to a hash, and the attack demos were **re-run** on
`a5f76c9` bytes, not on the earlier dirty worktree.

No install was performed (python3/git only, no new package).

## 1. Re-run and line-by-line comparison with `after-pointers.txt`

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/check-evidence-pointers.py --rev master
PRED-PTR-r36-v1 rev=master pointers_r35=8 dangling_r35=2 dangling_r35_closed=1 pointers_r36=34 dangling_r36=0 inherited_dirty=0 scratch_tracked=124 scratch_disposition_ok=1 tip_axis_transcript=1 setup=ok verdict=TARGET_MET
dangling_r35: .ufo/waves/round-35/scratch/SimplifyCounter/
dangling_r35: .ufo/waves/round-35/scratch/MutC1Drop/mutants/
tip_axis: quality/receipts/axis-520c631d2925807aadadb041eeda13f8b829b0c5.txt@520c631d2925807aadadb041eeda13f8b829b0c5
rc=0
```

Byte comparison against the **committed** receipt (`git show HEAD:.ufo/waves/round-36/receipts/after-pointers.txt`), with only the receipt's `$ …` / blank / `rc=` wrapper lines removed:

```
$ diff <(git show HEAD:.ufo/waves/round-36/receipts/after-pointers.txt | sed '1d' | sed '/^\$ python3/d' | sed '/^rc=/d' | sed '/^$/d') <(sed '/^$/d' /tmp/c2_now.txt)
IDENTICAL
```

**Verdict: CONFIRMED** — at the current tip the command reads `TARGET_MET`, exit 0, and
its body is byte-identical to the receipt. The receipt header now also pins the right
revision (`at a5f76c9…`), which it did not 40 minutes earlier (it read `at cf175c7…`
while the producing script was uncommitted; the tip has since re-pinned it).

The `--rev` flag does **not** select the instrument, only the records. Matrix, all four
runs executed:

| script bytes | `--rev` | result |
|---|---|---|
| `a5f76c9` (current) | `master` | `dangling_r36=0 … TARGET_MET` rc=0 |
| `a5f76c9` (current) | `cf175c7` | `dangling_r36=0 … TARGET_MET` rc=0 |
| `cf175c7` (`505c900`) | `cf175c7` | `dangling_r36=3 … TARGET_MISSED` rc=1 |
| `2d90524` (`505c900`) | `master` | `dangling_r36=3 … TARGET_MISSED` rc=1 |

The three dangling pointers at `cf175c7` are `.ufo/waves/round-35/scratch/SimplifyCounter/`,
`.ufo/waves/round-35/scratch/MutC1Drop/mutants/` (the D5 pair old sides) and
`quality/receipts/axis-a3094c99ab85bec35534de2447552c47dd2b647f.txt` (the D10 prose
citation, a file that has never existed at any revision:
`git ls-tree -r --name-only master | grep -c axis-a3094c99` → `0`).

Also reproduced with the committed instrument at the before revision:

```
$ python3 -I /tmp/gate_2d90524.py --rev 4243d031e3441f5063f92c33aa58377c6f9ff120
… pointers_r35=8 dangling_r35=2 dangling_r35_closed=0 pointers_r36=0 dangling_r36=0 inherited_dirty=0 scratch_tracked=124 scratch_disposition_ok=0 tip_axis_transcript=0 setup=missing-r36-sections verdict=TARGET_MISSED
```

which matches `before-pointers.txt` body exactly. **Verdict: CONFIRMED** for the before side.

## 2. Planted dangling pointer in a round-36 section

Clone `A` = clean LANE clone at `a5f76c9` + one line inside `## Round 36` of `SCORECARD.md`:

```
- **Planted attack pointer.** `quality/receipts/planted-ghost.md` recorded as evidence.
```

```
$ cd /tmp/c2attack2/A && python3 -I quality/check-evidence-pointers.py --rev master
PRED-PTR-r36-v1 rev=master pointers_r35=8 dangling_r35=2 dangling_r35_closed=1 pointers_r36=35 dangling_r36=1 inherited_dirty=0 scratch_tracked=124 scratch_disposition_ok=1 tip_axis_transcript=1 setup=ok verdict=TARGET_MISSED
dangling_r36: quality/receipts/planted-ghost.md
rc=1
```

Unplanted control in the same clone family (`base`, clean `a5f76c9`): `dangling_r36=0 … TARGET_MET` rc=0.

**Verdict: CONFIRMED** — one planted pointer moves the count 34→35, is named with its
exact path, and flips the verdict and exit code.

## 3. `dangling_r35_closed=1` with no correction pair

Clone `B`: the two D5 pair lines deleted from the round-36 `LOG.md` section, two **0-byte**
files committed at the two dangling prefixes, and the lesson's disposition count retargeted
to the new tracked count (124→126, which is what `git ls-tree` then reports):

```
- `.ufo/waves/round-35/scratch/SimplifyCounter/` -> `.ufo/waves/round-35/scratch-evidence/SimplifyCounter/`   (removed)
- `.ufo/waves/round-35/scratch/MutC1Drop/mutants/` -> `.ufo/waves/round-35/scratch-evidence/MutC1Drop/`        (removed)
$ git ls-tree -r -l master | grep placeholder
100644 blob e69de29bb2d1d6434b8b29ae775ad8c2e48c5391       0	.ufo/waves/round-35/scratch/MutC1Drop/mutants/placeholder.txt
100644 blob e69de29bb2d1d6434b8b29ae775ad8c2e48c5391       0	.ufo/waves/round-35/scratch/SimplifyCounter/placeholder.txt

$ cd /tmp/c2attack2/B && python3 -I quality/check-evidence-pointers.py --rev master
PRED-PTR-r36-v1 rev=master pointers_r35=8 dangling_r35=0 dangling_r35_closed=1 pointers_r36=30 dangling_r36=0 inherited_dirty=0 scratch_tracked=126 scratch_disposition_ok=1 tip_axis_transcript=1 setup=ok verdict=TARGET_MET
rc=0
```

The only pair left in the round-36 LOG section is the D10 axis pair. `record_intact`
**still holds**: `ptr35` is unchanged at 8 and still carries both `SUPERSEDED_POINTERS`,
so `all(p in ptr35 …)` is true; the clause was never the thing that failed — with
`dangling35 == []` the closure loop's `closed == len(dangling35)` is `0 == 0`.

**Verdict: FALSIFIED as a measurement of "a correction pair was written".** The
observable degenerates to "nothing dangles", and `resolves()` is existence-only (a 0-byte
blob with the right prefix satisfies a pointer that claims a 124-path mutation tree).
The documented requirement ("every dangling pointer … appears as the `old` side of a pair")
is not what the code tests in this branch. The record-intact clause does hold, and it does
its job when the record is *rewritten* instead — clone `D` (round-35 section repointed at
the `scratch-evidence/` paths, no pair) reads `dangling_r35=0 dangling_r35_closed=0 … TARGET_MISSED` rc=1, so rewriting is still refused. **CONFIRMED** for that guard.

## 4. Over- and under-counts in the current round-36 sections

Extractor replicated from `quality/check-evidence-pointers.py` (`PATHY`, `pointerish`,
`sections`, `resolves`) against `master`; 34 counted tokens.

**Over-count (3 of 34).** `pointers_r36` counts the D5 and D10 pair **old sides** as
citations of the round-36 record:
`.ufo/waves/round-35/scratch/SimplifyCounter/` (LOG36:2156),
`.ufo/waves/round-35/scratch/MutC1Drop/mutants/` (LOG36:2157),
`quality/receipts/axis-a3094c99…txt` (LOG36:2162 and LOG36:2218). The committed
docstring calls these "named, not cited", and `dangling36` exempts them, yet they are still
counted — so `pointers_r36=34` over-reports citations by 3 relative to the gate's own rule.

**Under-count (8 real pointers never examined).** `PATHY` is a hardcoded prefix allowlist
(`.ufo|corpus|quality|tools|scripts|considerthese`), so a pointer written relative to a wave
directory is invisible:

| doc:line | token | lane-relative | resolves under `.ufo/waves/round-36/` |
|---|---|---|---|
| SC36:2310/2318 | `receipts/before-discrimination.txt` | no | yes |
| SC36 | `receipts/after-discrimination.txt` | no | yes |
| SC36 | `receipts/clause-attribution.txt` | no | yes |
| SC36:2318 | `receipts/before-pointers.txt` | no | yes |
| SC36:2318 | `receipts/after-pointers.txt` | no | yes |
| LOG36 (D2 bullet) | `scratch-evidence/RevEntryR12/evidence.txt` | no (real file is `.ufo/waves/round-35/scratch-evidence/RevEntryR12/evidence.txt`) | n/a |
| LOG36 (closing) | `w1/reports/` | no | yes |
| LESSON (Scratch disposition) | `.ufo/waves/round-35/scratch` | yes, but dropped by `pointerish` (dotless leaf, no trailing slash) | n/a |

The lesson token is the one D8 is about; the gate still scores the disposition from a raw
substring scan, not from `pointers()`, so the two disagree about what the lesson cites.
Net: 39 genuine lane evidence pointer occurrences, 34 counted, 3 of those not citations.

**Verdict: finding (medium)** — the pointer class is a string-shape test, so a record can
cite evidence in a shape the gate never reads, and the printed `pointers_r36` is not the
number of pointers the record cites.

## Findings by severity

**F1 — HIGH. `SCORECARD.md`'s C2 after-pin contradicts the receipt it cites, and at that pin
the claim is false.** At the newest tip `f77b554`, `git show HEAD:SCORECARD.md | sed -n '2318p'`
still reads
`the re-run cannot reproduce). After at `cf175c716f…`:` and line 2310 the same for C1, while
the receipt it cites was re-pinned in that very commit: `git show HEAD:.ufo/waves/round-36/receipts/after-pointers.txt | head -1`
→ `# C2 after-state — PRED-PTR-r36-v1 at a5f76c9…` (`git diff a5f76c9 f77b554 -- .ufo/waves/round-36/receipts/after-pointers.txt`
shows the header line replaced and nothing else). Run the instrument that is committed **at**
`cf175c7` against the records at `cf175c7` and the same command gives
`dangling_r36=3 … TARGET_MISSED` rc=1. So the scorecard names a revision at which its own
claim does not hold, and the receipt that would prove it is from a later revision; the
re-pin pass fixed the receipt and left the scorecard line untouched. The pointer gate cannot
see this: both paths resolve, and the gate never compares a receipt's pinned revision to the
revision it is cited for. Fix: change the two `After at cf175c7` pins (C1 at line 2310, C2 at
line 2318) to the revisions their receipts name — one line each.

**F2 — HIGH. The supersede exemption is a global string set with an unconstrained target,
so any dangling pointer in LOG/SCORECARD/lesson can be laundered.** Clone `A2` = clone `A`
plus one line in the round-36 LOG section: ``- `quality/receipts/planted-ghost.md` -> `LOG.md` ``.
Result: `pointers_r36=35 dangling_r36=0 … TARGET_MET` rc=0. The nonexistent pointer is now
"named, not cited", and the pair's `new` side is `LOG.md` — not even a pointer, just a file
that exists. `superseded_old` is built from the whole of `log36`, so it also exempts a
citation in `SCORECARD.md` or the lesson, and it does not require the pair's target to be
distinct, pointerish, or in the same artifact class. The landed record already relies on
this: the D10 prose claim (`quality/receipts/axis-a3094c99…txt` was committed) is green only
because a later pair names a *different* receipt.

**F3 — HIGH. `dangling_r35_closed=1` is satisfied by zero dangling plus 0-byte placeholders
(F3 evidence in §3).** `record_intact` holds throughout, so the clause the round advertises
as the anti-rewrite guard is orthogonal to this branch. A one-file placeholder under
`.ufo/waves/round-35/scratch/SimplifyCounter/` is indistinguishable from recovered evidence.

**F4 — HIGH. D5 pair targets are unconstrained.** Clone `C`: both D5 pairs kept with
`new` retargeted to `LOG.md` — `dangling_r35_closed=1 … TARGET_MET` rc=0, with
`  - `.ufo/waves/round-35/scratch/SimplifyCounter/` -> `LOG.md`` in the record. A "correction"
may point at any tracked file; nothing checks the target is the recovered evidence.

**F5 — MEDIUM. `scratch_disposition_ok` is a substring match, not a disposition.** Clone
`F`: the lesson line rewritten to `` `….ufo/waves/round-35/scratch` is **NOT retained** — this
sentence is false — yet the gate reads tracked paths=124 `` still yields
`scratch_disposition_ok=1 … TARGET_MET` rc=0. A negated or self-contradicting sentence
satisfies "the lesson names a disposition".

**F6 — MEDIUM. `inherited_dirty` is a live-worktree reading, and its value is independent of
`--rev`.** Clone `E`: one appended comment in `.ufo/waves/round-35/w2/reports/RevC1Tip.md`,
uncommitted. `--rev master` → `inherited_dirty=1 … TARGET_MISSED`; `--rev cf175c7` → the
same, byte for byte. The module docstring ("Each observable counts committed bytes") and
`SCORECARD.md` ("re-derives five observables from committed bytes") are wrong for this one;
the before-receipt documents it honestly, the gate's own docs do not. Consequence for
receipts: a `--rev`-pinned verdict is only reproducible on a clean checkout — and the
receipt format records neither the checkout state nor the script blob.

**F7 — MEDIUM. See §4** (over/under-count, plus the missing receipt-pin agreement check
noted in F1).

**Residual risk / what could hide here.** The gate is a shape check over three documents:
an evidence pointer that is *shaped* correctly but names a file whose bytes say something
else (a stale receipt, a wrong revision, an empty file) passes. The D10 citation is exactly
that class and is currently green. `tip_axis_transcript` is the same shape: a transcript
whose `MADO_AXIS:` line read `checked=0 mismatched=0 rev=<own hex>` would satisfy it — the
round-37 plan already names this (hardening by `MADO_AXIS_ROW:` rows), so it is residual
rather than new; the landed transcript itself is genuine (`checked=3`, three `MADO_AXIS_ROW`
lines, `MADO_INDEX: indexed=50/50`).

**Recommended minimal fixes, in order:** (1) re-pin the scorecard C2 line; (2) print the
instrument identity in the verdict line (`gate_blob=$(git hash-object __file__)`) and require
it in the receipt header — this is D3's defect one level up, applied to C2's own counter;
(3) scope the exemption to the pair line itself and require `new` to be pointerish and to
resolve; (4) make the r35 closure state explicit (`pairs>=len(dangling35)` and report
`closed_vacuous` when `dangling35==[]`); (5) require `resolves()` of a directory pointer to
match at least one non-empty blob; (6) give the disposition and the pointer class a parsed
form instead of substrings and prefixes.

## Verification gaps

Not run (out of this seat's scope): C1's discrimination gate, the lane suites
(`tools/mado-verify.sh`, `check-axis-scores.py`), and the S211 census. `resolves()`'s glob
branch is untested — no glob pointer exists in the three round-36 documents, so it is dead
on this data. The lane is live and moved once during this pass (`2d90524` → `a5f76c9`,
04:51:47); every number above is pinned to `a5f76c9` and re-measured after the move, but a
later tip may differ.

Replay of the /tmp demos: clone LANE, then apply exactly the mutation named in each of
§2/§3/A2/C/D/E/F above (one SCORECARD line; pair-line deletion plus two 0-byte placeholder
files plus the 124→126 lesson edit; pair-target retarget to `LOG.md`; round-35 section
rewrite; one uncommitted byte; the negated disposition sentence), commit the change except
in `E`, and run `python3 -I quality/check-evidence-pointers.py --rev master`.

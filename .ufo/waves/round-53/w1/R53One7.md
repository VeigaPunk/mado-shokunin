# R53One7 — bounded mutation probe

## Axes and scope

- **Coverage:** whether a single changed acceptance threshold is observable against the frozen C2 production entry.
- **Operability:** whether the frozen C2 instrument runs on the round-53 base tip and returns stable, clause-specific output.
- Frozen claims read: `.ufo/waves/round-53/claims-frozen.md`; base tip `ad4bf2059bcfafe63671d262222908ee1fe8001c`.
- Lane safety manual read: `SKILL.md`. No host/live probes, installs, tracked edits, campaign tools, or source checkout writes. The sole probe workspace was `/fast/scratch/hyaku/mado-r53/R53One7`; it was removed before completion.

## C2 — threshold mutant

**Attacked predicate:** `quality/counters/c2-r51-dispatch-entry.py` clause (d), which requires at least `MIN_HELD = 3` distinct grounded held citations (source lines 68-69, 512-553). This is a bounded mutation of the frozen instrument, not a change to the contract.

**Mutant:** in an isolated scratch copy, change only `MIN_HELD = 3` to `MIN_HELD = 8`. This stricter-than-contract threshold is a plausible defect: a correctly admitted entry can be rejected despite satisfying the frozen three-citation predicate.

**Detector:** the same command against pristine, mutant and restored script bytes, with the repo/base revision fixed:

```sh
python3 -I <scratch-script> --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev ad4bf2059bcfafe63671d262222908ee1fe8001c --work <seat-scratch-work>
```

- Pristine actual output: `a ok=1`; `b ok=1 rows=6/2 pins=6`; `c ok=1 body_shingles=3364 files=66+cand3 max=0.1%`; `d ok=1 held=7/3 lines=8 untargeted=1 tokens=14`; final `clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET`; exit 0.
- Mutant actual output: `a ok=1`; `b ok=1 rows=6/2 pins=6`; `c ok=1 body_shingles=3364 files=66+cand3 max=0.1%`; `d ok=0 held=7/8 lines=8 untargeted=1 tokens=14`; final `clauses=abcd clauses_met=3 admitted=0/1 verdict=TARGET_MISSED`; exit 1.
- Restored actual output matched pristine: `d ok=1 held=7/3 lines=8 untargeted=1 tokens=14`; final `clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET`; exit 0.

**Verdict:** killed. The production entry supplies seven citations, so this particular stricter-threshold defect changes the observed clause result and is caught by the frozen detector. This does not validate proposition-level coverage or the r52 correction predicate; C2-R51 is a separate, older detector.

**Hash/restoration evidence:** pristine and restored source hash `ebe39e1183375e0fb102124057eafecc9a21bdfc330c04ceb03759093d10e6dd`, matching the lane source hash; mutated copy hash `1f975713fdd3cbf4770f99e767187dd2abb1e77b0b6a22a995b5ba34f0ce9db2`. Temporary copies and work directories were removed. The lane source was not modified.

## C1 and routed r52 evidence

I did not run a C1 counter mutation probe. The frozen C1-R51 instrument's `make_clone()` creates a scratch Git clone and performs checkout (`quality/counters/c1-r51-ledger.py`, lines 95-111); the assignment explicitly prohibits git mutations. I did not bypass that restriction or invoke the counter. This leaves C1 dynamically untested by this seat.

Routed r52 evidence was inspected, not rerun or treated as an assumption: `.ufo/waves/round-52/w2/Attack19/receipts.txt` records the C1-R52 production-ledger result `population=82 ledger_rows=83 uncovered=0 dup=0 dangling=1 bad_pointer=1 self_pointer=0 generic_desc=0 verdict=TARGET_MISSED` (exit 1), while the recorded `./quality/tool-ledger.md` self-pointer and both duplicate-row variants returned `TARGET_MET` (exit 0). These are prior receipts, not this seat's mutation output.

`.ufo/waves/round-52/w2/Attack31.md` records the routed C2-R52 finding: landed counter accepted 12/16 mutants, did not open/verify pins, and missed the fabricated P16 quote splice and P17 duplication/misattribution; the draft caught the P16 splice. These observations concern the r52 proposition-entry artifacts, not the r51 counter mutated above. No external source was opened, so there are no new source URLs/quotes to cite.

## Report trailer

```text
seat=R53One7 wave=w1 round=53 lane=mado-shokunin base=ad4bf2059bcfafe63671d262222908ee1fe8001c
target=C1 instrument-ledger accountability counter; C2 proposition-grounded synthetic-dispatch entry repair
attacked_predicate=C2-R51 clause d MIN_HELD threshold (3 -> 8) in isolated scratch copy
detector=python3 -I <scratch-script> --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev ad4bf2059bcfafe63671d262222908ee1fe8001c --work <seat-scratch-work>
output=pristine TARGET_MET exit 0; mutant TARGET_MISSED exit 1 (held 7/8); restored TARGET_MET exit 0
verdict=C2 mutant killed; C1 dynamic probe not run (frozen counter requires prohibited scratch git clone)
restoration=source hash ebe39e1183375e0fb102124057eafecc9a21bdfc330c04ceb03759093d10e6dd preserved; seat scratch removed
artifacts=.ufo/waves/round-53/w1/R53One7.md
```
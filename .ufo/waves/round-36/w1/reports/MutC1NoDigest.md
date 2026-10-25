# MutC1NoDigest — mutation-tester report (mado round 36, wave 1)

Seat: `L1Mado36.MutC1NoDigest` · Role: mutation-tester
Assignment: `LANE/.ufo/waves/round-36/w1/prompts/MutC1NoDigest.md`

## Mutant

Probe: the round-36 C1 design minus exactly the `digest == receipt["sha256"]`
conjunct (round-35 D3 defect reintroduced).

- The round-36 C1 counter exists at `LANE/quality/counters/c1-idle-lock.py`
  (untracked; landed before my run). `diff r35/c1/count.py -> c1-idle-lock.py`
  shows exactly three behavioral changes: r36 predicate string, Registry-section
  scoping (`registry_section`), and the added conjunct `and digest == receipt["sha256"]`.
- Mutant built by copying `c1-idle-lock.py` to `/tmp/mutc1nodigest/c1-nodigest.py`
  and deleting that one conjunct line.
  - before `sha256sum`: `2ee6d0de76dfe756a9bbb03a4f96ae9bd3e48d4dfe37564b46e6e696047f4ce7` (mutant == pristine copy at creation)
  - after deletion, verification: `$ < /tmp/mutc1nodigest/c1-nodigest.py | grep -c 'digest == receipt'` → `0` (no digest conjunct remains)
  - after deletion, verification: `$ < /tmp/mutc1nodigest/c1-nodigest.py | grep -c 'digest == receipt'` → `0` (no digest conjunct remains); `grep -n 'sha256'` lists the remaining occurrences — docstring line 7, predicate string line 30 (declared-sha256 text; the binding wording "hash to that same sha256" is also in this string), `digest = hashlib.sha256(blob).hexdigest()` (line 175, kept: still computed), and `receipt["sha256"] in cs[5]` (line 193, kept: anchor-cell membership). Only the binding conjunct `digest == receipt["sha256"]` is gone.
  - restored bytes preserved at `/tmp/mutc1nodigest/c1-pristine-copy.py` (hash `2ee6d0de...`, equal to the source file's hash).

## Detector

`LANE/quality/check-counter-discrimination.py` (the real gate), copied to
`/tmp/mutc1nodigest/check-disc.py` with one additive profile `mut` pointing C1 at
the mutant (`/tmp/mutc1nodigest/c1-nodigest.py`, frozen `round-36/c1/frozen.json`);
C2 untouched (`quality/counters/c2-ledger.py`). Same manifest, same 25 controls.

## Observed outputs

Mutant profile (`mut`), `--receipts /tmp/mutc1nodigest/receipts-mut --mutants /tmp/mutc1nodigest/mutants-mut`:

```
control=c1-live instrument=c1 clause=- expected=TARGET_MET observed=TARGET_MET ok=1
control=c1-golden-r36 instrument=c1 clause=- expected=TARGET_MET observed=TARGET_MET ok=1
control=c1-donothing instrument=c1 clause=- expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-digest instrument=c1 clause=digest-match expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-entry-symlink instrument=c1 clause=entry-regular expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-quote-absent instrument=c1 clause=gate-quote-substring expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-quote-long instrument=c1 clause=gate-quote-word-bound expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-recheck-prose instrument=c1 clause=recheck-valid expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-row-duplicate instrument=c1 clause=row-unique expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-row-extra-field instrument=c1 clause=row-well-formed expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-status-queued instrument=c1 clause=status-mined expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-usedby-extra instrument=c1 clause=used-by-exact expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-shape-only instrument=c1 clause=digest-match expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-fabricated-payload instrument=c1 clause=digest-match expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-no-registry-heading instrument=c1 clause=row-in-registry expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-row-moved-out instrument=c1 clause=row-in-registry expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-live instrument=c2 clause=- expected=TARGET_MET observed=TARGET_MET ok=1
... c2 mutant controls aborted (see below) ...
MADO_DISCRIMINATION error=mutant-generation-failed
```

Pristine r36 profile (control run), `--receipts /tmp/mutc1nodigest/receipts-r36`:

```
control=c1-live instrument=c1 clause=- expected=TARGET_MET observed=TARGET_MET ok=1
control=c1-golden-r36 instrument=c1 clause=- expected=TARGET_MET observed=TARGET_MET ok=1
control=c1-donothing instrument=c1 clause=- expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-digest instrument=c1 clause=digest-match expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-entry-symlink instrument=c1 clause=entry-regular expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-quote-absent instrument=c1 clause=gate-quote-substring expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-quote-long instrument=c1 clause=gate-quote-word-bound expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-recheck-prose instrument=c1 clause=recheck-valid expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-row-duplicate instrument=c1 clause=row-unique expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-row-extra-field instrument=c1 clause=row-well-formed expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-status-queued instrument=c1 clause=status-mined expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-usedby-extra instrument=c1 clause=used-by-exact expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-shape-only instrument=c1 clause=digest-match expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-fabricated-payload instrument=c1 clause=digest-match expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-no-registry-heading instrument=c1 clause=row-in-registry expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-row-moved-out instrument=c1 clause=row-in-registry expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-live instrument=c2 clause=- expected=TARGET_MET observed=TARGET_MET ok=1
control=c2-tip-stale instrument=c2 clause=- expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-tip-one-copy instrument=c2 clause=- expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-blob-corrupt instrument=c2 clause=- expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-blob-row-deleted instrument=c2 clause=- expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-clause-deleted instrument=c2 clause=- expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-receipt-token instrument=c2 clause=- expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-receipt-unbound instrument=c2 clause=- expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-retired-also-live instrument=c2 clause=- expected=TARGET_MISSED observed=TARGET_MISSED ok=1
clause=digest-match controls=3 missed=3
clause=entry-regular controls=1 missed=1
clause=gate-quote-substring controls=1 missed=1
clause=gate-quote-word-bound controls=1 missed=1
clause=recheck-valid controls=1 missed=1
clause=row-in-registry controls=2 missed=2
clause=row-unique controls=1 missed=1
clause=row-well-formed controls=1 missed=1
clause=status-mined controls=1 missed=1
clause=used-by-exact controls=1 missed=1
MADO_DISCRIMINATION: profile=r36 instruments=c1,c2 controls=25 correct=25/25 label='round-36 repaired counters' verdict=TARGET_MET
```

## Verdicts

- **The digest conjunct is NOT exercised by any manifest control.** All 16 C1
  controls report identical verdicts under the mutant (no digest conjunct) and
  under pristine r36 (digest conjunct present): 2 accept + 14 reject, 16/16.
  The mutant's verdict-observed set over C1 == pristine's verdict-observed set.
  The resting `digest == receipt["sha256"]` conjunct is **dead** with respect to
  this manifest.
- **No control catches the missing conjunct; the three "digest-match" controls
  all still pass (expected MISSED, observed MISSED), but for the wrong reason.**
  Evidence:
  - `c1-digest` under the mutant: `PRED-C1-r36-v1 closed_entries=0 closed_rows=0 open_cites=8` — the fixture's `SOURCES.md` has **no `## Registry` section** (diff vs live shows the fixture is the bare 8-row table; live's `## Registry` heading at line 9 is absent). The mutant's `registry_section` returns nothing → all 8 cites open → MISSED. The digest conjunct never fires.
  - `c1-shape-only` and `c1-fabricated-payload` under the mutant: `open_cites=8` — every receipt is the junk text (`ZZZZ NOT A RECEIPT…` / `THIS IS NOT A FETCHED RECEIPT…`), so the `gate-quote-substring` clause (`quote.encode() in blob`) opens all cites, and the fixtures' SOURCES.md has no `## Registry` heading either. Both reject via other clauses; the digest conjunct never fires.
  - Sanity: the same three fixtures were `observed=TARGET_MET` under the *r35* counter (receipts-r35: `c1-shape-only`: `observed=TARGET_MET ok=0`, `c1-fabricated-payload`: `observed=TARGET_MET ok=0`, `c1-digest`: `closed_entries=2 closed_rows=7 open_cites=1`), i.e. they discriminate against the r35 counter — before round-36's registry fence existed. The r36 registry fence masks them.
- **Observed-minus-expected over C1 for the mutant: no control differs from pristine.**

## C2 note

The `mut`-profile run aborts at the first C2 mutant control because
`gen-mutants.py --profile mut` rejects the profile (`argument --profile: invalid
choice: 'mut'`) — my gate copy leaks the profile name into C2 fixture
generation. This is a test-harness scaffolding artifact of my run, not a lane
defect; the pristine `r36` run shows `c2-ledger.py` + C2 mutants are
25/25-consistent (`correct=25/25`). All C1 resigns are unaffected and complete.

## Tooling / installs

None. Used system `python3`; no package installs were needed.

## Files (all under allowed scope)

- `/tmp/mutc1nodigest/c1-nodigest.py` — mutant C1 counter (digest conjunct removed)
- `/tmp/mutc1nodigest/c1-pristine-copy.py` — restored pristine r36 C1 counter
- `/tmp/mutc1nodigest/check-disc.py` — gate copy with additive `mut` profile
- `/tmp/mutc1nodigest/run-mut.log`, `run-r36.log`, `receipts-*/` — full runs

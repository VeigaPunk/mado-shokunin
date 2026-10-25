# MutC1AcceptAll — mutation-tester seat, mado round 36 wave 1

Task (`.ufo/waves/round-36/w1/prompts/MutC1AcceptAll.md`): write a `/tmp`
mutant of the C1 instrument that prints
`PRED-C1-r36-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET`
and exits 0 on every root; score it against the frozen manifest via a `/tmp`
copy of `quality/check-counter-discrimination.py` whose r36 c1 script path
points at the mutant. Report the score and which controls kill it. Restore
nothing in LANE — only `/tmp` and this report were written.

## Mutant

`/tmp/mado-mut-c1-acceptall/mutant-c1.py` (sha256
`9dec713f1d396d2e4a93311790462dfdec46a3322ccea230f7e1403c8b439e38`), a
do-nothing always-accept instrument — no argparse, no reads, unconditional:

```python
print("PRED-C1-r36-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET")
raise SystemExit(0)
```

Direct invocation (it ignores `--root`/`--frozen` entirely):

```
$ python3 -I /tmp/mado-mut-c1-acceptall/mutant-c1.py --root /nonexistent --frozen /also/none
PRED-C1-r36-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
DIRECT_EXIT=0
$ python3 -I /tmp/mado-mut-c1-acceptall/mutant-c1.py
PRED-C1-r36-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
NOARG_EXIT=0
```

The printed line matches the real counter's format byte-for-byte
(`quality/counters/c1-idle-lock.py` tail prints
`f"PRED-C1-r36-v1 closed_entries={…} closed_rows={…} open_cites={…} verdict={…}"`).

## Detector

`/tmp/mado-mut-c1-acceptall/check-gate.py` — byte-copy of the lane gate
(source sha256 `421deda5…2544` before copy) with exactly one line changed:

```diff
-        "c1": {"script": "quality/counters/c1-idle-lock.py",
+        "c1": {"script": "/tmp/mado-mut-c1-acceptall/mutant-c1.py",
```

(`Path(repo) / "/tmp/…"` resolves to the absolute path.) All other legs —
frozen spec path, c2 instrument, generator, receipts handling — untouched.

## Commands

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
# pristine baseline (unmodified lane gate, real counters):
python3 -I quality/check-counter-discrimination.py --profile r36 \
  --manifest .ufo/waves/round-36/controls/manifest.json --repo . \
  --receipts /tmp/mado-mut-c1-acceptall/receipts-pristine \
  --mutants /tmp/mado-mut-c1-acceptall/pristine-fixtures
# mutated (same gate bytes minus one path line; c1 := mutant):
python3 -I /tmp/mado-mut-c1-acceptall/check-gate.py --profile r36 \
  --manifest .ufo/waves/round-36/controls/manifest.json --repo . \
  --receipts /tmp/mado-mut-c1-acceptall/receipts-mutant \
  --mutants /tmp/mado-mut-c1-acceptall/mutant-fixtures
```

`--receipts` and `--mutants` redirect the gate's only write surfaces to `/tmp`;
`gen-mutants.py` was read first — it writes only under `--out`
(`shutil.rmtree(out)` + `out.mkdir`, `dest/...` `write_text`/`write_bytes`),
reading the repo but never writing it.

## Results (actual output lines)

Pristine baseline:

```
MADO_DISCRIMINATION: profile=r36 instruments=c1,c2 controls=25 correct=25/25 label='round-36 repaired counters' verdict=TARGET_MET
GATE_EXIT=0
```

Mutant run — every c1 reject leg killed the mutant (full transcript in
`/tmp/mado-mut-c1-acceptall/mutant-run.txt`):

```
control=c1-live instrument=c1 clause=- expected=TARGET_MET observed=TARGET_MET ok=1
control=c1-golden-r36 instrument=c1 clause=- expected=TARGET_MET observed=TARGET_MET ok=1
control=c1-donothing instrument=c1 clause=- expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c1-digest instrument=c1 clause=digest-match expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c1-entry-symlink instrument=c1 clause=entry-regular expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c1-quote-absent instrument=c1 clause=gate-quote-substring expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c1-quote-long instrument=c1 clause=gate-quote-word-bound expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c1-recheck-prose instrument=c1 clause=recheck-valid expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c1-row-duplicate instrument=c1 clause=row-unique expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c1-row-extra-field instrument=c1 clause=row-well-formed expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c1-status-queued instrument=c1 clause=status-mined expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c1-usedby-extra instrument=c1 clause=used-by-exact expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c1-shape-only instrument=c1 clause=digest-match expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c1-fabricated-payload instrument=c1 clause=digest-match expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c1-no-registry-heading instrument=c1 clause=row-in-registry expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c1-row-moved-out instrument=c1 clause=row-in-registry expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c2-live instrument=c2 clause=- expected=TARGET_MET observed=TARGET_MET ok=1
[8 c2 legs all ok=1 — omitted; see mutant-run.txt]
MADO_DISCRIMINATION: profile=r36 instruments=c1,c2 controls=25 correct=11/25 label='round-36 repaired counters' verdict=TARGET_MISSED
GATE_EXIT=1
```

Sample generated receipt (`/tmp/mado-mut-c1-acceptall/receipts-mutant/c1-digest.txt`):

```
instrument=c1 clause=digest-match expected=TARGET_MISSED observed=TARGET_MET ok=0
$ /usr/bin/python3 -I /tmp/mado-mut-c1-acceptall/mutant-c1.py --root …/c1-digest --frozen …/c1/frozen.json
PRED-C1-r36-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
exit=0
```

## Per-item verdict

| Item | Result | Verdict |
|---|---|---|
| Mutant prints frozen `TARGET_MET` line, exits 0 on every root | quoted output above, both with bogus and no args | PASS (as designed) |
| Score vs frozen manifest (`MANIFEST-r36-v1`, N=25) | `correct=11/25 verdict=TARGET_MISSED`, gate exit 1 | mutant **KILLED** |
| Baseline sanity | same manifest, pristine instrument: `correct=25/25 verdict=TARGET_MET`, exit 0 | detector conclusive |
| Killers | all **14 c1 reject controls** (`c1-donothing`, `c1-digest`, `c1-entry-symlink`, `c1-quote-absent`, `c1-quote-long`, `c1-recheck-prose`, `c1-row-duplicate`, `c1-row-extra-field`, `c1-status-queued`, `c1-usedby-extra`, `c1-shape-only`, `c1-fabricated-payload`, `c1-no-registry-heading`, `c1-row-moved-out`), each `expected=TARGET_MISSED observed=TARGET_MET ok=0` | always-accept class fully covered |
| Survivors | `c1-live`, `c1-golden-r36` (accept controls — the mutant's TARGET_MET matches expectation; not a defect) + all 9 c2 controls (real `c2-ledger.py`, unaffected) | expected |
| Clause-binding table | mutant run shows `missed=0` for all 10 clause names — every clause-bound control saw `TARGET_MET` from the mutant, i.e. each clause's load-bearing control *detected* the acceptance | coverage confirms kill rule |

## Restoration evidence

No LANE bytes were ever mutated: the mutated artifact is a `/tmp` copy of the
gate, so "restored" ≡ "pristine" ≡ current lane state.

- Lane gate unchanged: `sha256sum` after both runs —
  `421deda5956f8005967b10d4721b2bddead68a610704b1b2c705297236662544  quality/check-counter-discrimination.py`
  (identical pre-copy and post-run).
- `git status --porcelain` at lane root shows only sibling wave-1 writes
  (`M .ufo/waves/round-36/receipts/before-pointers.txt`,
  `M quality/check-evidence-pointers.py`, `?? .ufo/waves/round-36/scratch/`,
  `?? .ufo/waves/round-36/w1/reports/`) — none from this seat.
- Writes by this seat: `/tmp/mado-mut-c1-acceptall/{mutant-c1.py,check-gate.py,
  mutant-run.txt,pristine-run.txt,receipts-mutant/*,receipts-pristine/*,
  mutant-fixtures/*,pristine-fixtures/*}` and this report. No tool installs
  (python3/git only); pacman untouched.

## Verdict

**KILLED — PASS.** The always-accept mutant reached 11/25 and was killed by
every one of the 14 c1 reject controls; the frozen kill rule ("an instrument
that always accepts fails the reject controls") holds as designed against the
repaired counter profile. No coverage gap found on the c1 accept side: the
manifest discriminates the maximal false-acceptance instrument with zero
survivors among reject controls.

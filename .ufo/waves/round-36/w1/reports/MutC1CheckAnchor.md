# MutC1CheckAnchor — mutation-tester report (round 36, wave 1)

Mutant probed: the round-36 C1 counter (PRED-C1-r36-v1) with the anchor-cell
digest test removed — deleted line `and receipt["sha256"] in cs[5]`
(pristine `quality/counters/c1-idle-lock.py:193`), keeping the bytes binding
`digest == receipt["sha256"]` and `quote.encode() in blob`.

**Verdict: MUTANT SURVIVED** — score 25/25, `TARGET_MET`, exit 0. No frozen
control kills it. This is a coverage finding: the anchor-cell digest test is
load-bearing (shown by probe below) but is not exercised by any control in the
frozen manifest.

---

## 1. Setup (scratch only; no production file touched)

Files (all under `LANE/.ufo/waves/round-36/scratch/MutC1CheckAnchor/`):

- `c1-idle-lock-mut.py` — copy of pristine `quality/counters/c1-idle-lock.py`
  with line 193 deleted. Mutation diff confirmed:
  ```diff
  --- quality/counters/c1-idle-lock.py
  +++ .../scratch/MutC1CheckAnchor/c1-idle-lock-mut.py
  -                and receipt["sha256"] in cs[5]
  ```
- `score-mut.py` — copy of `quality/check-counter-discrimination.py` with the
  r36 profile's `c1.script` repointed to the mutant's absolute path (line 43).
  No other change.
- `reg-c1-digest/`, `reg-c1-fabricated-payload/` — copies of the two cribs with
  a `## Registry` heading restored above the row lines (see probe in §4).

Hashes before mutation: `quality/counters/c1-idle-lock.py`
`2ee6d0de76dfe756a9bbb03a4f96ae9bd3e48d4dfe37564b46e6e696047f4ce7`;
`quality/check-counter-discrimination.py`
`421deda5956f8005967b10d4721b2bddead68a610704b1b2c705297236662544`.

No tool installed (nothing needed). No production bytes were modified; no
restoration was necessary (lane copies, not in-place edits).

## 2. Baseline (pristine counter, frozen manifest)

```
$ python3 -I quality/check-counter-discrimination.py --profile r36 \
    --manifest .ufo/waves/round-36/controls/manifest.json \
    --no-receipts --repo .
MADO_DISCRIMINATION: profile=r36 instruments=c1,c2 controls=25 correct=25/25 label='round-36 repaired counters' verdict=TARGET_MET
exit=0
```
Matches the committed receipts (e.g. `c1-fabricated-payload.txt`:
`closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED`, exit 1).

## 3. Mutant score (the assignment's question)

```
$ python3 -I .ufo/waves/round-36/scratch/MutC1CheckAnchor/score-mut.py \
    --profile r36 \
    --manifest .ufo/waves/round-36/controls/manifest.json \
    --receipts /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-36/scratch/MutC1CheckAnchor/receipts-mut \
    --repo .
MADO_DISCRIMINATION: profile=r36 instruments=c1,c2 controls=25 correct=25/25 label='round-36 repaired counters' verdict=TARGET_MET
exit=0
```

- All 25 controls classified as expected: 3 accept `TARGET_MET`, 22 reject
  `TARGET_MISSED`, 0 `ERROR`.
- **No control kills the mutant.** Removing the anchor-cell test changes the
  score 25/25 → 25/25. The c2 legs are unaffected (all 9 new c2 receipts are
  byte-identical to the committed `controls/receipts/c2-*.txt`).

### Why: the digest-match controls never reach the digest clauses

Every c1 reject crib fails earlier, on the `row-in-registry` fence, because none
of the round-35 crib trees contains a `## Registry` heading:

| control | `## Registry` present? | rows in section | mutant observed |
|---|---|---|---|
| c1-digest | no | 0 | `open_cites=8` |
| c1-shape-only | no | 0 | `open_cites=8` |
| c1-fabricated-payload | no | 0 | `open_cites=8` |
| c1-no-registry-heading | no | 0 | `open_cites=8` |
| c1-entry-symlink … c1-usedby-extra (10 more) | no | 0 | `open_cites=8` |
| c1-row-moved-out | yes | 7 | `open_cites=1` (row moved to `## Leads`) |
| c1-donothing | no | 0 | `open_cites=8` |

Mechanism: `registry_section()` returns `""` when no `## Registry` heading
exists → `rows_for()` returns `[]` → `row = None` → the `ok` conjunction is
false at `row is not None` — so `receipt["sha256"] in cs[5]` and
`digest == receipt["sha256"]` are never evaluated. The `clause=digest-match`
binding table therefore reports `missed=3` for controls whose rows never exist;
the labelled per-clause controls are not load-bearing for any clause.

## 4. Probe: is the anchor test load-bearing, and does fabricated-payload still die?

To test the digest clauses in isolation, I restored the `## Registry` heading in
scratch copies of the two `digest-match` cribs and ran both counters.

| control | counter | output | verdict |
|---|---|---|---|
| reg-c1-digest | pristine | `closed_entries=2 closed_rows=7 open_cites=1` | MISSED |
| reg-c1-digest | mutant | `closed_entries=3 closed_rows=8 open_cites=0` | **MET** |
| reg-c1-fabricated-payload | pristine | `closed_entries=0 closed_rows=0 open_cites=8` | MISSED |
| reg-c1-fabricated-payload | mutant | `closed_entries=0 closed_rows=0 open_cites=8` | MISSED |

- **reg-c1-digest**: the crib's receipts are byte-identical to the live receipts
  (verified `cmp`), so the bytes binding passes for all 8 rows. The single row
  the pristine counter rejects is S210, whose anchor cell is prose
  (`cs[5]=" Whether the operator's choice about the idle lock could ever have been recorded "`)
  and whose declared digest in the frozen spec is all-zero. The **anchor-cell
  digest test is the only thing keeping this input missclassified**; the mutant
  closes all 8 rows. → This is exactly the input no frozen control provides.
- **reg-c1-fabricated-payload**: the crib's receipts are fake (`THIS IS NOT A
  FETCHED RECEIPT / fabricatedated attestation for S203 / ZERO REAL BYTES`), so
  `digest == receipt["sha256"]` fails for every row even with the anchor test
  removed. **`c1-fabricated-payload` still dies — under the bytes binding.**
  Under the frozen manifest it also dies (as `TARGET_MISSED`), but the cause in
  the manifest is the `## Registry` fence, not the bytes.

## 5. Finding

The frozen c1 reject set does not kill the anchor-cell mutation because every
reject control is already killed by the `row-in-registry` fence (round-35 crib
trees predate the `## Registry` convention; they contain no section at all). The
`digest-match` clause — both halves, anchor-cell and bytes binding — is currently
untested by the manifest. The bytes binding was demonstrated separately to be
real (fabricated-payload dies under it), and the anchor-cell test was
demonstrated to be load-bearing (reg-c1-digest flips MET when it is removed) —
so the surviving mutant is a manifest coverage gap, not a no-op mutation.

Reported values: score 25/25 = TARGET_MET, exit 0; kill: none; fabricated-payload
still dies (bytes binding), confirmed by the registry-restored probe.

# MutC1RejectAll — mutation-tester report (mado round 36, wave 1)

Seat: `L1Mado36.MutC1RejectAll`. Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Assignment: same probe as `MutC1AcceptAll`, but the mutant always prints
`open_cites=8 verdict=TARGET_MISSED` and exits 1 on every root. Net: the two
degenerate instruments together must not reach 25/25 on any subset they share.

## Mutant

`/tmp/mado-r36-mut-rejectall/c1-rejectall.py` — a byte-copy of
`quality/counters/c1-idle-lock.py` with only the verdict tail mutated: the
`met = (...)` computation, the computed `print(...)` and `SystemExit(0 if met
else 1)` are replaced by an unconditional

```py
print("PRED-C1-r36-v1 closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED")
raise SystemExit(1)
```

The required literal `open_cites=8 verdict=TARGET_MISSED` is carried verbatim;
the `PRED-C1-r36-v1 closed_entries=0 closed_rows=0` prefix keeps the line
shaped like the real counter's output line (the gate only regexes
`verdict=(TARGET_MET|TARGET_MISSED)` at
`quality/check-counter-discrimination.py:50`).

sha256 before mutation (`quality/counters/c1-idle-lock.py`):
`2ee6d0de76dfe756a9bbb03a4f96ae9bd3e48d4dfe37564b46e6e696047f4ce7`
sha256 mutant: `6d7cea4cee3dc86a900ca348d3eadd1cff261e0a95bbdbd629fde6e00f50ab0a`

Gate copy `/tmp/mado-r36-mut-rejectall/check-discrim.py` — byte-copy of
`quality/check-counter-discrimination.py` (sha256
`421deda5956f8005967b10d4721b2bddead68a610704b1b2c705297236662544`) with exactly
one replacement: `PROFILES["r36"]["c1"]["script"]` set to
`/tmp/mado-r36-mut-rejectall/c1-rejectall.py`. Gate sha256 after edit:
`f9a8dcf661a9594fa08d9a0cd6789cbe67687015b517884e11888a44e5a3c6ce`.
No lane file was edited; the mutation lives entirely in /tmp.

## Unconditionality check (three roots)

```
$ python3 -I /tmp/mado-r36-mut-rejectall/c1-rejectall.py --root <R> --frozen .ufo/waves/round-36/c1/frozen.json
R=.                                   → open_cites=8 verdict=TARGET_MISSED, exit=1
R=.ufo/waves/round-36/controls/c1-golden-r36 → same, exit=1
R=.ufo/waves/round-35/controls/c1-donothing  → same, exit=1
```

## Detector

Patched-gate command (run from the lane root; `--no-receipts` because
`--receipts` defaults into the write-restricted
`.ufo/waves/round-36/controls/receipts/` — stdout carries the identical
per-control lines):

```sh
python3 -I /tmp/mado-r36-mut-rejectall/check-discrim.py --profile r36 \
  --manifest .ufo/waves/round-36/controls/manifest.json --repo . --no-receipts
```

Expected detector behavior: the mutant passes every `expected=TARGET_MISSED`
control vacuously and fails every `expected=TARGET_MET` control — i.e. it must
be killed by the accept controls.

## Output (observed, full run)

```
control=c1-live instrument=c1 clause=- expected=TARGET_MET observed=TARGET_MISSED ok=0
control=c1-golden-r36 instrument=c1 clause=- expected=TARGET_MET observed=TARGET_MISSED ok=0
control=c1-donothing … expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-digest clause=digest-match … ok=1
control=c1-entry-symlink clause=entry-regular … ok=1
control=c1-quote-absent clause=gate-quote-substring … ok=1
control=c1-quote-long clause=gate-quote-word-bound … ok=1
control=c1-recheck-prose clause=recheck-valid … ok=1
control=c1-row-duplicate clause=row-unique … ok=1
control=c1-row-extra-field clause=row-well-formed … ok=1
control=c1-status-queued clause=status-mined … ok=1
control=c1-usedby-extra clause=used-by-exact … ok=1
control=c1-shape-only clause=digest-match … ok=1
control=c1-fabricated-payload clause=digest-match … ok=1
control=c1-no-registry-heading clause=row-in-registry … ok=1
control=c1-row-moved-out clause=row-in-registry … ok=1
control=c2-live … expected=TARGET_MET observed=TARGET_MET ok=1
control=c2-tip-stale … ok=1   control=c2-tip-one-copy … ok=1
control=c2-blob-corrupt … ok=1   control=c2-blob-row-deleted … ok=1
control=c2-clause-deleted … ok=1   control=c2-receipt-token … ok=1
control=c2-receipt-unbound … ok=1   control=c2-retired-also-live … ok=1
MADO_DISCRIMINATION: profile=r36 instruments=c1,c2 controls=25 correct=23/25 label='round-36 repaired counters' verdict=TARGET_MISSED
```

Gate exit code: **1** (verified in a second run without `tee`: `gate_exit=1`;
a previous `tee`-piped run printed `GATE_EXIT=0`, which was `tee`'s status).

Full captured stdout: `/tmp/mado-r36-mut-rejectall/gate-out.txt`.

## Baseline leg (pristine detector, unmutated instruments)

```sh
python3 -I quality/check-counter-discrimination.py --profile r36 \
  --manifest .ufo/waves/round-36/controls/manifest.json --repo . --no-receipts
```

→ `correct=25/25 verdict=TARGET_MET`, exit 0. The baseline passes, so the
23/25 under mutation is a real kill, not an inconclusive baseline failure.

## Verdict: **KILLED**

- Score: **23/25**, `verdict=TARGET_MISSED`, gate exit 1.
- Killing controls (ok=0): **`c1-live`** and **`c1-golden-r36`** — the two c1
  accept controls. An always-rejecting instrument cannot reach `TARGET_MET`
  because the manifest's accepts force it to fail somewhere.
- On the 16 c1 controls the mutant actually answers for: 14/16 (all 14 rejects
  vacuously correct, both accepts killed). The headline 23/25 is inflated by
  the unmutated real `c2-ledger.py` scoring 9/9 on its own controls — worth
  noting only because a naive read of "23/25" looks close to target; the kill
  rule is `correct == controls`, all-or-nothing, and it held.

## Net check (the pair must not jointly reach 25/25 on a shared subset)

Built the sibling twin in my own /tmp (`c1-acceptall.py` + a second gate copy
pointing r36.c1 at it; sha256s in /tmp artifacts):

```
accept-all run: every c1 control observed=TARGET_MET →
  c1-live ok=1, c1-golden-r36 ok=1, all 14 c1 rejects ok=0
  MADO_DISCRIMINATION … correct=11/25 verdict=TARGET_MISSED (exit 1)
```

Per-control correct sets on the shared c1 subset (16 controls):

| Control | accept-all | reject-all |
|---|---|---|
| c1-live, c1-golden-r36 | ✓ | ✗ |
| 14 c1 reject controls | ✗ | ✓ |

The two correct sets are **disjoint** — no single c1 control is classified
correctly by both degenerates, so on any subset they share each scores
strictly below 100%; together they can never reach 25/25 (or 16/16 on the c1
subset). Their correct-set union covers all 16 c1 controls: no control is
vacuously passed by *every* degenerate, i.e. no degenerate-shaped hole exists
in the manifest. **Net claim: PASS** (founding assumption of the kill rule in
`registration.md:69-74` confirmed empirically).

## Restoration / write-scope evidence

- Lane files touched: **none**. All artifacts are under
  `/tmp/mado-r36-mut-rejectall/` (`c1-rejectall.py`, `c1-acceptall.py`,
  `check-discrim.py`, `check-discrim-accept.py`, `gate-out.txt`) plus the
  generator's own `/tmp/mado-r36-mutants-r36/` fixtures (the gate writes those
  there by design, outside the lane).
- `--no-receipts` used, so the gate performed zero receipt writes.
- `git status --porcelain` after the runs shows only sibling wave-1 work
  (`M .ufo/waves/round-36/receipts/before-pointers.txt`,
  `M quality/check-evidence-pointers.py`, `?? quality/receipts/`,
  `?? .ufo/waves/round-36/scratch/`, `?? .ufo/waves/round-36/w1/reports/` —
  this report). Post-run hashes unchanged:
  `check-counter-discrimination.py` `421deda5…2544`,
  `c1-idle-lock.py` `2ee6d0de…4ce7`.
- Nothing to restore: no production byte was modified.

## Tooling

No installs or upgrades performed; stock `python3` + `cp`/patch sufficed.

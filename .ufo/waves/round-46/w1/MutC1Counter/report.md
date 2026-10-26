# MutC1Counter — mutation probe of PRED-C1-r46 (round 46 w1)

**Question:** which mutants of the frozen counter `quality/counters/c1-r46-devices.py` still separate the reference
build from the controls V03, V07, V13, STUB of `.ufo/waves/round-46/ctl/run-c1-controls.py`?

**Answer: 16 of 19 mutants survive.** The only load-bearing kill channel in this control set is clause f's exactness
(exact stdout + rc + stderr on the 90 pinned fixtures). Killed: M12, M13 (both by V03), M17 (by the reference).
Survived: M01–M11, M14–M16, M18, M19.

## Setup

- Counter sha256 before **and** after the probe: `dfeaa4401430ddc2d68711b8dd30b1f470fe1d74b6d1f39477172a30d2fc850a`
  (never modified; mutants are scratch copies under `/fast/scratch/hyaku/mado-r46/MutC1Counter/mut/`, deleted).
- Subjects built by executing the frozen `run-c1-controls.py` and calling its own `make()` — clone
  `--shared --no-checkout`, `rev-parse --show-toplevel` asserted equal to the clone, `checkout --detach
  8c5434c60e03f147ee1f75ab195e8bc3f0db4dec`, tool body written and committed in the clone. REF's tool blob sha256
  `b229efd0…` equals the counter's pinned MODEL_SHA256. Supplementary BASE = the bare freeze commit.
- 19 mutants, each one minimal string replacement asserted to apply exactly once, compiled, run from a mirror layout
  whose `c1-r46-fixtures.json` and reference copies are byte-identical (the counter re-verifies both sha256 pins on
  every run). Command per run: `python3 -I <counter> --repo <subject> --rev HEAD --work <scratch>/w --nonce 4646`.
- Nonce 4646 (the control runner's default) for the full matrix; second nonce 90210 spot-check on pristine + 7
  mutants × 6 subjects: identical separation.

## Baseline (pristine counter, nonce 4646)

REF TARGET_MET rc 0 (fixtures=90/90 generated=150/150 selftest 48/48 readonly=ok); BASE, V03, V07, V13, STUB all
TARGET_MISSED rc 1. Killers: BASE → clause a; V03 → fixture `case-exact-dump-name` (89/90, generated 150/150);
V07 → clause s (47/48) + fixtures 86/90 + generated 103/150; V13 → fixture `mouse-overflow` (89/90) + generated
149/150; STUB → fixtures 0/90 (its selftest 30/30 passes).

## Verdicts

| mutant (edit, counter line) | expected detector | outcome |
|---|---|---|
| M01-drop-clause-a (L358 `present=…` → `True`) | BASE | **SURVIVED** — BASE still rejected, but by an uncaught `TypeError … 'NoneType'` at `f.write(blob)`, not by verdict logic |
| M02-drop-clause-s (L383 → `selftest="ok"`) | V07 (selftest 47/48) | **SURVIVED** — V07 still rejected by clause f (86/90) |
| M03-weaken-s-min (L382 `>= SELFTEST_MIN` → `>= 1`) | low-count selftest | **SURVIVED** — no control has N<MIN; V07 fails on 47≠48, not the min |
| M04-skip-env-b (L391 drop `(t46,"B")`) | env-B-sensitive control | **SURVIVED** — all controls fail identically in env A |
| M05-skip-nonce-run (L391 drop `(tn,"A")`) | precompute-dependent control | **SURVIVED** — controls fail the seed-46 runs |
| M06-drop-stderr-fixture (L318 drop `p.stderr==b""`) | stderr-only failure | **SURVIVED** — controls fail on stdout/rc |
| M07-accept-any-rc-fixture (L318 drop rc check) | rc-only failure | **SURVIVED** |
| M08-drop-stderr-generated (L342-3 drop stderr) | stderr-only failure | **SURVIVED** |
| M09-drop-clause-r (L400 → `readonly="ok"`) | hyprctl-running tool | **SURVIVED** — no control runs hyprctl |
| M10-drop-clause-g (L402 drop `g_ok==GEN`) | generated-only failure | **SURVIVED** — every control already fails clause f |
| M11-weaken-g-tol20 (L402 `==GEN` → `>=GEN-20`) | control failing ≤20 generated | **SURVIVED** |
| M12-drop-clause-f (L402 drop `fixtures_ok==len`) | V03 | **KILLED by V03** — flips to TARGET_MET at `fixtures=89/90 generated=150/150` |
| M13-weaken-f-tol5 (L402 `==len` → `>=len-5`) | V03 | **KILLED by V03** — same flip |
| M14-drop-bwrap (L257 `return argv`) | isolation-dependent control | **SURVIVED** — clause i untested |
| M15-drop-sha-pins (L88 → `if False:`) | tampered pin | **SURVIVED** — no control tampers pins |
| M16-deterministic-generated (L396 `Random(0)`) | precomputed-generated control | **SURVIVED** — anti-precompute property untested |
| M17-sanity-invert-f (L402 `fixtures_ok==0`) | sensitivity check | **KILLED by REF** — reference flips to TARGET_MISSED at fixtures=90/90 |
| M18-drop-timeout-guard (L342 drop `p is not None`) | timeout path | **SURVIVED** — no run timed out; equivalent on this set |
| M19-accept-any-rc-generated (L342 drop rc check) | rc-only failure | **SURVIVED** |

## Coverage findings (surviving mutants = control-set gaps, not counter defects)

1. Clause f's exactness is the only channel this control set exercises: V03 is caught *only* by fixture
   `case-exact-dump-name`; a 5-fixture tolerance or dropping f lets V03 through at 89/90 + 150/150 generated.
2. Clauses g and s are redundant for these controls (each already fails f); clause a is enforced only incidentally,
   via a crash path, not by the verdict logic.
3. Clauses r (read-only marker) and i (bwrap isolation), the env-B run, the nonce run, the generated stderr/rc
   checks, and the fixtures/model sha256 pins have no detector in this control set.
4. The harness does detect gross counter damage (M17 killed by the reference positive control).

## Restoration evidence

Original counter untouched (sha256 identical before/after). Mutants, subject clones and run outputs lived only in
`/fast/scratch/hyaku/mado-r46/MutC1Counter/`, deleted at the end; `evidence/` here holds `results.json`,
`results-spot.json`, `verdicts.json`, `mutants.json`, `subjects.json` and all 326 raw run outputs. No tools were
installed (host python3 3.14.8, git 2.56.0, bwrap present were sufficient). Full findings:
`.ufo/waves/round-46/w1/MutC1Counter.md`.

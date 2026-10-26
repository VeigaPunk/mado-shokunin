# MutC1Counter — scoped findings (round 46 w1)

Probe: mutation-test the frozen counter `quality/counters/c1-r46-devices.py` (PRED-C1-r46) — which counter mutants
still separate the reference build from the controls of `.ufo/waves/round-46/ctl/run-c1-controls.py`? Scope: the four
named controls V03, V07, V13, STUB plus supplementary BASE; the full 23-control suite may kill more — claim scoped
accordingly.

## Method (all evidence under `.ufo/waves/round-46/w1/MutC1Counter/evidence/`)

- Subjects built by executing the frozen `run-c1-controls.py` module and calling its own `make()` per control — the
  exact recipe the control suite uses: `git clone -q --shared --no-checkout <lane> <scratch>/ctl-<name>`,
  `rev-parse --show-toplevel` asserted equal to the clone, `checkout -q --detach 8c5434c60e03f147ee1f75ab195e8bc3f0db4dec`,
  tool body written to `tools/mado-devices.py`, committed with a throwaway identity inside the clone only.
  REF's committed tool blob sha256 `b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b` equals the
  counter's pinned MODEL_SHA256; V03/V07/V13 bodies are the runner's own single-replacement variants (each asserted
  to apply exactly once); STUB is the runner's STUB source; BASE is the bare freeze commit (no tool).
- 19 counter mutants (`mutants.json`), each one minimal string replacement asserted to apply exactly once to the
  pristine source and compile-checked. Because the counter resolves its fixtures/reference relative to its own path,
  each mutant runs from a mirror layout `mut/<name>/quality/counters/c1-r46-devices.py` + byte-identical copies of
  `c1-r46-fixtures.json` (sha `027ed508…`) and the reference (sha `b229efd0…`) — the counter re-verifies both pins on
  every run, so a bad copy would have been a setup error, not a silent divergence.
- Run command per cell: `python3 -I <counter> --repo <scratch>/ctl-<subject> --rev HEAD --work <scratch>/w --nonce 4646`.
  Full matrix: pristine × 6 subjects + 19 mutants × REF + 18 survivors × 5 controls = 119 runs; second nonce 90210
  spot-check: pristine + 7 mutants × 6 subjects = 42 runs. 161 runs total, all stdout/stderr retained in
  `evidence/out/` (326 files).

## Baseline separation (pristine counter, nonce 4646)

REF TARGET_MET rc 0 — `fixtures=90/90 generated=150/150 selftest=ok readonly=ok tool=present`. All five controls
TARGET_MISSED rc 1:

- BASE: `clause=a tool=absent` (clean clause-a rejection).
- V03 (case-insensitive names): fixture `case-exact-dump-name` FAIL in all three runs; 89/90; generated 150/150.
- V07 (virtual compared): clause s `rc=1 last='MADO_DEVICES_SELFTEST: 47/48 passed'` + fixtures 86/90 (`host`,
  `virtual`, `virtual-plain-name`, `three-keyboards-mixed`) + generated 103/150 — killed three ways.
- V13 (no float32): fixture `mouse-overflow` FAIL (rc=1 want 5, stdout differs); 89/90; generated 149/150.
- STUB: fixtures 0/90, generated 0/150 (its selftest line `30/30 passed` satisfies clause s).

So clause f (exact stdout+rc+stderr on the 90 pinned fixtures) is the load-bearing killer for all four named
controls; V07 and V13 are additionally caught by s and g.

## Verdicts (nonce 4646; `verdicts.json`)

**Killed (3):**

- M12-drop-clause-f — `met` line (counter L402) drops `fixtures_ok == len(fixtures)` → **V03 flips to TARGET_MET**
  (`fixtures=89/90 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET rev=092bc3ce…`).
  V03 is caught *only* by clause f.
- M13-weaken-f-tol5 — same line, `== len(fixtures)` → `>= len(fixtures) - 5` → **V03 flips to TARGET_MET** (89 ≥ 85,
  generated 150/150 passes).
- M17-sanity-invert-f — `fixtures_ok == 0` → **reference flips to TARGET_MISSED** at `fixtures=90/90` — the positive
  control detects gross counter damage (harness sensitivity check, included by design).

**Survived (16):** M01, M02, M03, M04, M05, M06, M07, M08, M09, M10, M11, M14, M15, M16, M18, M19 — each keeps REF
TARGET_MET and all controls TARGET_MISSED, i.e. the control set cannot distinguish it from the pristine counter.

| survivor | edit (counter line) | why nothing catches it |
|---|---|---|
| M01-drop-clause-a | L358 `present = …` → `present = True` | BASE is still rejected — but by an uncaught `TypeError: a bytes-like object is required, not 'NoneType'` at `f.write(blob)` (rc 1, stdout ends at `clause=a tool=present`), not by the verdict logic. Clause a's enforcement is a crash side effect. |
| M02-drop-clause-s | L383 `selftest = "ok"` always | V07's failing selftest (47/48) is redundant: clause f rejects V07 at 86/90. |
| M03-weaken-s-min | L382 `int(n[0]) >= SELFTEST_MIN` → `>= 1` | No control reports N < 30; V07 fails on 47≠48 equality, not the minimum. |
| M04-skip-env-b | L391 drop the `(t46, "B")` run | Every control fails identically in environment A; env B detects nothing for this set. |
| M05-skip-nonce-run | L391 drop the `(tn, "A")` run | Controls fail the seed-46 runs already; the nonce run adds no rejection power here. |
| M06-drop-stderr-fixture | L318 drop `p.stderr == b""` | All controls fail on stdout/rc content, never stderr-only. |
| M07-accept-any-rc-fixture | L318 drop `p.returncode == fx["rc"]` | Same — stdout mismatches suffice to reject. |
| M08-drop-stderr-generated | L342-343 drop stderr check | Same. |
| M09-drop-clause-r | L400 `readonly = "ok"` always | No control tool runs `hyprctl`/`libinput`/`journalctl`/`udevadm`, so no marker ever appears; clause r is untested. |
| M10-drop-clause-g | L402 drop `g_ok == GEN` | Every control already fails clause f (89/90, 86/90, 89/90, 0/90); clause g is redundant for this set. |
| M11-weaken-g-tol20 | L402 `g_ok == GEN` → `g_ok >= GEN - 20` | Same; and the controls' generated scores (150, 103, 149, 0) straddle the tolerance without changing any verdict. |
| M14-drop-bwrap | L257 `sandbox()` returns `argv` unsandboxed | Controls fail semantically with or without isolation; clause i is untested. |
| M15-drop-sha-pins | L88 pin check → `if False:` | No control tampers with the fixtures or the reference, so the pins are never exercised. |
| M16-deterministic-generated | L396 `Random(nonce ^ 0x5DEECE66D)` → `Random(0)` | Controls fail fixtures regardless of the generated stream; the anti-precompute property has no control. |
| M18-drop-timeout-guard | L342 drop `p is not None` | No tool run timed out anywhere (max ~17 s wall per counter run vs 20 s per-tool timeout), so the mutant is equivalent on this input set; it would crash on the first timeout. |
| M19-accept-any-rc-generated | L342-343 drop `p.returncode == rc_want` | Controls fail on stdout content. |

## Reading (coverage findings, not counter defects)

1. **The control set's only load-bearing channel is clause f's exactness.** V03 survives every clause except f, and
   specifically the single fixture `case-exact-dump-name`; tolerating 5 fixture failures or dropping f entirely
   admits V03 at 89/90 fixtures + 150/150 generated. The pre-freeze history (V03 met before that fixture was added)
   is consistent with this.
2. **Redundant enforcement:** clauses g and s add nothing against these four controls (each already fails f); clause
   a is enforced only incidentally, by a crash path, not by the verdict logic.
3. **Untested clauses/properties:** r (read-only marker), i (bubblewrap isolation), the env-B run, the nonce run, the
   generated stderr/rc checks, the fixtures/model sha256 pins, and the nonce-derived generated seeding all have no
   detector in this control set — a counter weakened in any of these ways still separates reference from
   V03/V07/V13/STUB. These are gaps of the *control set*, not of the counter: r and i defend against malicious tools,
   which no control in this set models.
4. **Sensitivity:** the harness does detect gross counter damage (M17 killed by the reference positive control).

## Nonce stability

Second nonce 90210 (`results-spot.json`): pristine separates as at 4646, and all seven spot-checked mutants
(M01, M04, M05, M09, M14, M16, M19) show identical separation — survivor verdicts are not nonce-luck.

## Restoration evidence

- Original `quality/counters/c1-r46-devices.py` sha256 `dfeaa4401430ddc2d68711b8dd30b1f470fe1d74b6d1f39477172a30d2fc850a`
  recorded before the first run and re-checked after the last: identical. The frozen file was never opened for
  writing; all mutants were scratch copies.
- Mutant trees, subject clones and raw outputs lived only under `/fast/scratch/hyaku/mado-r46/MutC1Counter/`
  (peak ~9.5 MB), deleted after copying `results.json`, `results-spot.json`, `verdicts.json`, `mutants.json`,
  `subjects.json` and `out/` (326 files) into this seat's `evidence/` directory.
- No lane file outside this seat's directory and the two report paths was created or modified; no git/jj mutation in
  the lane or fleet; no pacman transaction; no tools installed (host python3 3.14.8, git 2.56.0, bwrap present were
  sufficient).

## Limits

- Four named controls + BASE, one full-matrix nonce (4646) + one spot nonce (90210); the full 23-control suite
  (V01–V20, MONITORS-COPY, …) may kill some of the 16 survivors — this probe does not claim they are unkillable,
  only that *this* control set does not kill them.
- M18 is equivalent-on-this-set (no timeouts occurred); a set with a timing-out tool would kill it.
- M01's survival concerns the verdict logic only; BASE is still rejected (exit 1, no verdict line), so the control
  suite's PASS/FAIL outcome is unchanged by the mutant.

# MutC1Counter — PRED-C1-r45 counter mutation matrix (round 45, w1, 2026-10-26)

Target: `quality/counters/c1-r45-monitors.py` (FROZEN, sha256 `c69ddee44a9fa3c442b910541038a9440ac72c2b5f21fe4899cb8f5df9213f34`,
re-verified unchanged after the whole run — mutants lived only in scratch copies; restoration evidence in Receipts).

## Method

- 38 single-edit mutants + 1 identity baseline (X0). Each mutant = one contiguous `old`→`new` replacement,
  anchor-verified unique (count==1) in the frozen text before execution.
- Control panel regenerated with the frozen `.ufo/waves/round-45/ctl/run-c1-controls.py` build/VARIANTS logic
  (module import, same `build()`, same anchor rules): 17 repos = REF + K00-BASE-ABSENT + K01-GEOMETRY-COPY +
  K02-STUB + K03..K15, each a `--shared --no-checkout` clone at BASE `0c89478af821a6424c9ac922eafe02e39630cf4f`
  with toplevel asserted, tool committed with scratch identity, REF commit `a56e983097f8f7b4aec767ac49edb4f7f047db24`.
- Every mutant counter ran on REF and on all 16 bad controls, seed 45, fresh `--work` per run
  (551 counter runs; each = selftest + 49 fixtures + readonly probe). All runs recorded in Receipts `results.json`.
- Classes: **OVER-STRICT** (REF below MET — killed), **GATE-BROKEN** (some bad control TARGET_MET — killed),
  **SURVIVOR** (REF MET, 16/16 MISSED) → then labeled *equivalent (proof)* or *missing control*.
- X0 reproduced the registered control outcome: REF TARGET_MET fixtures=49/49, 0 of 16 bad controls MET
  (matches `receipts/ctl-c1.txt` claim); every control death clean (rc=1, verdict line present, no crashes,
  0 anomalies across all survivor grids).

## Baseline attribution (X0 — which clause kills which control)

| control | clause s (selftest) | clause f | clause r | note |
|---|---|---|---|---|
| K00-BASE-ABSENT | – | – | – | killed by clause a only |
| K01-GEOMETRY-COPY | fail (alien marker `MADO_GEOMETRY_SELFTEST: 94/94`) | host FAIL | – | double-killed s+f |
| K02-STUB | **pass** (33/33 parsed) | host FAIL | – | killed by f only |
| K03–K07, K09–K13, K15 | fail (31–32/33, rc=1) | FAIL | – | double-killed s+f |
| K08-LIVE-HYPRCTL | **pass** (33/33) | FAIL (44/49) | **marker present** | double-killed f+r |
| K14-MIRROR-IGNORED | **pass** (33/33) | mirror-missing FAIL | – | killed by f only |

This table predicts everything below: any mutant weakening a check that is never a control's *sole* killer survives.

## Matrix (locators = line of the mutated site in the frozen counter, computed by search, not typed)

| mutant | site | REF | class |
|---|---|---|---|
| X0-identity | whole file | MET 49/49 | baseline (gate healthy) |
| S1-selftest-min-const `SELFTEST_MIN = 30`→`1` | L53 | MET | SURVIVOR — missing control |
| S2-selftest-min-cmp `>=SELFTEST_MIN`→`>=0` | L349 | MET | SURVIVOR — missing control |
| S3-selftest-rc-drop | L347 | MET | SURVIVOR — missing control |
| S4-selftest-parts3-le `==3`→`<=3` | L347 | MET | SURVIVOR — missing control |
| S5-selftest-suffix `=="passed"`→`!=""` | L347 | MET | SURVIVOR — missing control |
| S6-selftest-prefix marker check dropped | L347 | MET | SURVIVOR — missing control |
| S7-selftest-eq-or `and`→`or` (accepts 32/33) | L349 | MET | SURVIVOR — missing control |
| R1-fixture-rc-drop | L320 | MET | SURVIVOR — missing control |
| R2-fixture-stderr-drop | L320 | MET | SURVIVOR — missing control |
| R3-fixture-stdout-in `==`→`in` | L320 | MET | SURVIVOR — missing control |
| R4-timeout-swallow-true | L317 | MET | SURVIVOR — missing control |
| R5-fixture-timeout→1ms | L315 | missed 0/49 | OVER-STRICT (killed) |
| R6-selftest-timeout→1ms | L343 | missed | OVER-STRICT (killed) |
| V1-readonly-always-ok | L362 | MET | SURVIVOR — missing control |
| V2-marker-name-x | L354 | MET | SURVIVOR — **equivalent (proof)** |
| V3-fakebin-drop-journalctl | L274 | MET | SURVIVOR — missing control |
| A1-clause-a-mode-drop | L331 | MET | SURVIVOR — missing control |
| A2-clause-a-blob-drop | L331 | MET | SURVIVOR — **equivalent (proof)** |
| M1-met-fixtures-ge0 | L364 | MET | **GATE-BROKEN**: K02-STUB (0/49 MET!), K14-MIRROR-IGNORED (48/49 MET) |
| M2-fixtures_ok-plus1 | L360 | MET | **GATE-BROKEN**: K02-STUB, K14 (both 49/49 MET) |
| M3-met-selftest-always | L364 | MET | SURVIVOR — missing control |
| M4-met-readonly-always | L364 | MET | SURVIVOR — missing control |
| M5-met-and→or (s-term alone suffices) | L364 | MET | **GATE-BROKEN**: K02-STUB, K08-LIVE-HYPRCTL (2/49, readonly=fail, still MET), K14 |
| E1-host-drop-R | L81 | missed 48/49 | OVER-STRICT (killed) |
| E2-host-flip-DIFFER | L81 | missed | OVER-STRICT (killed) |
| E3-host-rc-1 | L81 | missed | OVER-STRICT (killed) |
| E4-norules-drop-O | L207 | missed | OVER-STRICT (killed) |
| E5-join-no-newline | L318 | missed 0/49 | OVER-STRICT (killed) |
| E6-subst-noop (placeholders stay) | L263 | MET | SURVIVOR — missing control |
| N1-dedupe-drop | L251 | MET | SURVIVOR — **equivalent at seed 45 (proof)**; latent on 9/200 seeds |
| N2-shuffle-drop | L253 | MET | SURVIVOR — missing control |
| N3-drop-D | L257 | MET | SURVIVOR — missing control |
| N4-drop-DP-prefix | L247 | MET | SURVIVOR — missing control |
| N5-seed-default-46 | L376 | MET | SURVIVOR — missing control |
| G1-env-drop-LANG | L311 | MET | SURVIVOR — missing control |
| G2-env-drop-HOME | L311 | MET | SURVIVOR — missing control |
| G3-env-path-nofakebin | L311 | MET | SURVIVOR — missing control |
| G4-env-drop-HIS | L312 | MET | SURVIVOR — missing control |

Totals: 39 = 1 baseline + 3 GATE-BROKEN (killed) + 7 OVER-STRICT (killed) + 3 equivalent survivors + 25 missing-control survivors.

## Survivor adjudication

Equivalent (proofs):

- **V2**: the renamed literal flows through one variable used only at the write site (L356 `make_fakebin(fakebin, marker)`)
  and the check site (L362 `os.path.exists(marker)`); both change together, so behavior is identical for every input.
- **A2**: with the mode conjunct retained (`ls.split()[0] in (b"100644", b"100755")`), the blob conjunct is redundant —
  in git trees only modes 100644/100755 denote blobs (120000 symlink, 160000 gitlink, 040000 tree are distinct modes),
  so the mutant accepts exactly the same entries.
- **N1**: computed `names(45)` with and without the dedupe branch — identical table (`DP-5, eDP-7, DVI-D-5`; tables equal),
  so at the registered default seed every downstream byte is identical. Caveat recorded: 9 of seeds 0–199 (10, 26, 86, 107,
  119, 133, 174, 191, 198) would produce different tables — latent, not exercised by the registered procedure.

Missing control (each states the control whose absence lets the mutant live):

- S1/S2: no control selftest line is `N/N passed` with 0<N<30 — the 30 floor has no teeth on this panel
  (a stub printing `2/2 passed` would MET). K01 fails by alien marker, K03-K13/K15 by 31-32/33, never by the floor.
- S3: no control exits `--selftest` nonzero while printing a fully well-formed passing line.
- S4/S5: no control selftest line has <3 tokens or a wrong third token with equal counts (K01's 94/94 dies on the marker).
- S6: no control combines an alien selftest marker with otherwise-correct fixtures (K01 has the alien marker but also
  fails fixtures — double kill).
- S7: no control combines `N/M` (N>=30, N≠M) selftest with correct fixtures (K03-K13/K15 fail fixtures independently).
- R1: no control emits byte-exact expected stdout with a wrong exit code (rc of every control is killed by content).
- R2: no control writes stderr with otherwise-perfect output.
- R3: no control emits a strict superset of the expected bytes (`want in got` accepts padded output; K02's single line is not a superset).
- R4: no control hangs; a tool that hangs on a fixture would be scored as passing it.
- V1: clause r is never a sole killer — K08 trips the marker AND fails fixtures (empty dump → verdict mismatch).
  A control that reads the live compositor yet still matches all fixtures would die by r alone; none exists.
- V3: no control invokes `journalctl`/`wlr-randr`/`wayland-info`; the r clause's coverage of those three binaries is untested.
- A1: no wrong-mode control exists — a symlinked or otherwise non-regular-mode `tools/mado-monitors.py` would pass clause a
  (blob check alone accepts symlink blobs).
- M3/M4: clause s / clause r are never the sole rejection reason for any control (see attribution), so forcing them `ok` flips nothing.
- E6: substitution is bidirectionally consistent (configs, dumps and expected lines all keep `{A}`-style placeholders), so the
  reference tool sees a self-consistent world and METs. The docstring's "expected bytes are not fixed text" property has no
  control: a tool that special-cases placeholder-looking names would MET under this mutant and MISSED under the frozen counter.
- N2/N4/N5: the name/seed plumbing only matters through the substitution table; no control is name-sensitive, so reordering
  (N2), re-prefixing (N4) or reseeding (N5 — note this also breaks the "default seed reproduces exactly" property) flips nothing.
- N3: survived because the reference matches `desc:` selectors by prefix (pinned Monitor.cpp matchesStaticSelector semantics):
  literal `desc:{D}` still prefix-matches the unsubstituted description `{D} 0x0001`, while `desc-not-prefix` (`X {D}`) still
  fails the prefix. No control distinguishes substituted from placeholder descriptions.
- G1: no locale-sensitive control (a tool formatting floats per ambient locale would die only under the dropped-LANG mutant).
- G2: HOME is isolation only; the counter has no HOME-write detector, so no control can be HOME-sensitive by construction.
- G3: with the fakebin PATH removed, K08 ran the real `hyprctl monitors all -j` (allowed read) and still died on fixtures
  (host dump ≠ fixture dump) — the fakebin apparatus is load-bearing for nothing on this panel; a fixture-correct tool that
  shells out to a probed binary (dies by r alone) is the missing control. Note: this mutant's K08 run is host-dependent.
- G4: no control reads `HYPRLAND_INSTANCE_SIGNATURE`; it is pure defense-in-depth (declared residual: r covers PATH lookups only).

## Findings

1. **The gate's only load-bearing layer against bad tools is clause-f exact-stdout + the selftest-count equality.**
   K02/K08/K14 pass selftest and die only on exact bytes; K03-K13/K15 are double-killed. Hence 25/38 mutants survive:
   every single-edit weakening of the rc check, stderr check, timeout semantics, readonly clause, mode/blob checks,
   SELFTEST_MIN floor, selftest parse tokens, env pins, or the seed/name plumbing is invisible to this control panel.
2. **The aggregation is the crown jewels and they are guarded**: forcing `fixtures_ok` (M1/M2) or weakening `met`'s
   conjunction to let a selftest-passing tool skip fixtures (M5) is detected — K02, K14 and K08 score TARGET_MET under
   those mutants. Recommendation if the counter is ever revised: a control that fails fixtures while passing selftest
   (e.g. K02 with one wrong fixture byte) already exists as K02; the surviving space is checks *around* clause f.
3. **Expectation tampering is self-detected** (E1-E5, R5, R6 over-strict): any edit to fixture expectations or timeouts
   breaks REF certification, so the contract encoding cannot be silently relaxed.
4. **Cheapest coverage fixes** (one control each): (a) stub with selftest `2/2 passed` (kills S1/S2); (b) tool with
   selftest rc=1 and perfect stdout (kills S3); (c) tool printing expected bytes + one extra line or one stderr byte
   (kills R3/R2); (d) tool exiting 1 on an OK fixture (kills R1); (e) fixture-correct tool that still execs `journalctl`
   (kills V3/r-coverage); (f) wrong-mode tool blob (kills A1); (g) a hanging tool (kills R4).

## Receipts (this directory)

- `results.json` — full per-run records: mutant sha256, REF stdout (complete), per-control rc/last line/failing clauses (551 runs).
- `summary.txt` — one line per mutant: class, REF fixtures, broken controls, controls missed.
- `mutdrive.py` — the driver (mutant table with anchors, panel builder, runner; deterministic, seed 45).
- `c1-r45-monitors.py` — pristine copy, sha256 `c69ddee4…f34`, identical to the lane file before and after the campaign.

Tooling record: no installs (python3 3.14.8 present; driver uses stdlib only). Scratch `/fast/scratch/hyaku/mado-r45/MutC1Counter`
purged after receipts were copied; no lane file outside this seat directory and `.ufo/waves/round-45/w1/MutC1Counter.md` was written.

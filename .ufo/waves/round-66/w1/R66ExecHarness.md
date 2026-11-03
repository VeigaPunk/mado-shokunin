# R66ExecHarness — round-66 C1/C2 controls harness (w1)

Seat: R66ExecHarness (executor, leaf). Deliverable: draft
`quality/wave-root` file `.ufo/waves/round-66/check-controls.py` at
`.ufo/waves/round-66/w1/R66ExecHarness/check-controls.py`
(sha256 `2e34eab0705b173a6c90d5635b4eb7bd8a71d57932821a0c01c855d17967db13`);
L1 installs it at the wave root. Evidence: `.ufo/waves/round-66/w1/R66ExecHarness/evidence/`
(final run trees, per-case raw out/err/rc, witness logs, digests.txt, summary.txt).
No installs were made (python3/git/bash only). No lane or host writes outside my seat
directory; scratch removed before yield.

## Frozen commands (exactly as declared; candidates detected at --rev only)

```
python3 .ufo/waves/round-66/check-controls.py --repo . --rev eafd500fa7be76dca59e729435e231a5032cc037 --claim c1 --scratch-root /fast/scratch/hyaku/mado-r66/measure
python3 .ufo/waves/round-66/check-controls.py --repo . --rev eafd500fa7be76dca59e729435e231a5032cc037 --claim c2 --scratch-root /fast/scratch/hyaku/mado-r66/measure
```

Per L1: the frozen command never falls back to worktree drafts; the base revision always
scores baseline bytes. C2 candidate generation is identified by the r66 driver marker
`quality/counters/c2-r66-landing-instrument.py` at --rev (C1 by
`quality/counters/c1-r66-register.py`), because `quality/landing-counters.sh` is extended
in place. C2 baseline bytes are extracted at the declared base eafd500 (pre-cutover);
C1 baseline at --rev (frozen r65 file). `--candidate-draft PATH` exists only as an
explicitly labelled pre-integration diagnostic and is not part of the frozen command.

## Commands run this seat (all rc shown; evidence under evidence/final-*)

| id | command (abbreviated) | rc |
|---|---|---|
| F1 | `check-controls.py --repo <lane> --rev eafd500… --claim c1 --scratch-root $S/final-c1-base` | 1 |
| F2 | F1 + `--candidate-draft …/R66ExecRegister/c1-r66-register.py` (sha 4e1b94ff…) | 0 |
| F3 | `check-controls.py … --claim c2 --scratch-root $S/final-c2-base` | 1 |
| F4 | F3 + `--candidate-draft …/R66ExecLanding/landing-counters.sh` (sha 1671cebc…, supersedes f0c8d74f…) | 0 |

## C1 — calibration / register-counter discrimination

Fixture: minimal git repo per case; PROVINCE.md variants (fixed deterministic code) over
real gate-live/gate-fileplane receipt bytes carried from eafd500 (digests in evidence
`digests.txt`). Baseline = r65 counter, candidate = R66ExecRegister draft.

| case | expected | baseline r65 | candidate r66 |
|---|---|---|---|
| genuine | TARGET_MET/0 | TARGET_MET/0 ✓ | TARGET_MET/0 ✓ |
| duplicate-heading | TARGET_MISSED/1 | TARGET_MET/0 ✗ | TARGET_MISSED/1 ✓ |
| row-without-receipt | TARGET_MISSED/1 | TARGET_MET/0 ✗ | TARGET_MISSED/1 ✓ |
| file-plane-only (live object omitted; L1 ruling) | TARGET_MISSED/1 | TARGET_MET/0 ✗ | TARGET_MISSED/1 ✓ |

Score: baseline **1/4 TARGET_MISSED**, candidate **4/4 TARGET_MET** (F2 exit 0).
Do-nothing: the base instrument cannot meet the frozen target — recorded above and in
`evidence/final-c1-base/r66harness/c1/summary.txt`.

Diagnostics (uncounted): `diag-no-register` MISSED both (healthy fail-closed);
`diag-fileplane-at-live-path` baseline MET / candidate MISSED (object-swap shape);
`diag-unreferenced-live-accepted` both MET — the disclosed citation-gap limit (see chronology).

## C2 — operability / landing-instrument discrimination

Fixture per case: committed wt carrying the instrument under test (baseline r65 bytes from
eafd500; F4 candidate = R66ExecLanding draft sha 1671cebc…) plus its three sibling children at
repo-relative paths, corpus stubs (nav genuinely green, real python3), and both receipts
dirs. Instruments run from inside the committed fixture so their `$SELF_DIR` sibling
resolution is genuine. Cases a–c use the agreed PATH-`python3` shim (dispatch on child
argv basename; env `WITNESS/TEST_LEG/TEST_MODE/FIXTURE_REV/REAL_PYTHON`; nav passes through
to real python3; markers are the children's real contract shapes, ledger = `LEDGER:`
per L1 erratum). Case d uses no shim and deletes the used-by sibling from the fixture
(evidence `run-d-missing-usedby.err`: `python3: can't open file … c3-r56-used-by.py`).

| case | expected | baseline r65 | candidate r66 |
|---|---|---|---|
| a-genuine-red (rc=1 + TARGET_MISSED marker) | RED/1 | RED/1 ✓ | RED/1 ✓ |
| b-child-crash (rc=2) | ERROR/2 | RED/1 ✗ | ERROR/2 ✓ |
| c-skip-no-marker (rc=0, no marker) | ERROR/2 | GREEN/0 ✗ | ERROR/2 ✓ |
| d-missing-usedby (file absent) | ERROR/2 | RED/1 ✗ | ERROR/2 ✓ |

Score: baseline **1/4 TARGET_MISSED**, candidate **4/4 TARGET_MET** (F4 exit 0).
Diagnostics (uncounted): `diag-all-green` (shim, no tampering) GREEN/0 both — the baseline
accepts forged-green evidence, the candidate's green rests on marker validation;
`diag-real-children` (no shim) baseline RED/1, candidate ERROR/2 (rc-2 children surface as
ERROR) — neither greenwashes a genuinely red fixture.

## Construction chronology (disclosed, not silent)

1. Initial C1 control-3 construction was PROVINCE-only (rows repointed to the file-plane
   receipt, live object retained). Inspection of the R66ExecRegister draft showed its
   selftest asserts that shape PASSES (`unreferenced-live-receipt`), conflicting with the
   frozen predicate. Messaged L1 + implementer. L1 ruled: counted control = only-file-plane
   receipt tree (LIVE_PATH object omitted; baseline must still accept it — verified);
   PROVINCE-only variant retained as uncounted citation-gap diagnostic. No code was
   tightened after scoring; candidate draft unchanged (4e1b94ff…).
2. First C2 candidate run mislabelled the r65 instrument as "candidate" because detection
   keyed on `quality/landing-counters.sh` existence (shared path across generations); the
   resulting 3/4 was an argument-refusal artifact. Fixed: generation marker = r66 driver
   presence; baseline extracted at declared base.
3. R66SentFrontier audit found the candidate instrument ran from an extraction tree whose
   siblings were absent (the shim masked it). Fixed: both instruments run from their
   committed fixture wt; case d deletes the sibling there. Re-ran all finals on the fixed
   harness (results above; superseded runs discarded).
4. R66CriticLanding P1: the frozen C2 verdict omitted the claims' selftest-green and
   real-landing gates. Fixed: candidate selftest is a verdict gate in both claims; the C2
   driver landing leg runs at integrated revs and folds into the verdict (skipped with
   disclosure in draft-diagnostic mode). Re-ran all finals (F1–F4 above).

## Claims gates beyond the four cases (R66CriticLanding P1, closed)

* Candidate selftest is a verdict gate in both claims: C1 runs the r66 counter's hermetic
  string selftest (`--selftest`, rc 0 required — 15/15 in F2); C2 runs the instrument's
  extended selftest (`--selftest --scratch-root <evdir>/candidate/st`, rc 0 required —
  58/58 in F4). Output lines `candidate selftest rc=<n>`; verdict folds it in.
* C2 real landing leg: at an integrated rev the harness extracts the r66 driver
  (`quality/counters/c2-r66-landing-instrument.py`) at --rev and runs it with
  `--repo/--rev/--scratch-root`, requiring `MADO_R66_INSTRUMENT: … verdict=TARGET_MET`
  rc 0, folded into the verdict (claims kill rule: "actual landing non-green means
  TARGET_MISSED"). In draft-diagnostic mode the driver is absent at rev, so the leg prints
  `candidate driver=skipped (draft-diagnostic mode …)` — disclosed, not silently omitted.
  The live-lane landing measurement at the landing rev remains L1/measure-owned.

## Limitations

* The C2 shim is a child simulator: it emits the real marker shapes with case-controlled
  rc. Per the claims, marker checks are bounded structural guarantees, not proof against
  malicious child forgery. Nav in cases a–c is the real inline counter.
* Candidate scores above are pre-integration draft diagnostics (hashes pinned); after L1
  integrates, the frozen command re-scores candidates from --rev bytes, including the
  driver landing leg.
* C1 state-cell truth remains unmeasured by design (both instruments).
* Scratch fixture repos used their own git identities; no lane git/jj state touched.

## Files

* `check-controls.py` — harness draft (install at wave root; single file, stdlib only).
* `evidence/final-c{1,2}-{base,cand}/r66harness/<claim>/` — summary.txt, digests.txt,
  extracted instrument bytes, per-case fx-*/ fixture content (minus .git), run-*.out/.err/.rc,
  cmd-*.txt, witness-*.txt, shim-*/.
* `report.md` — this report (seat copy).

## Final containment correction

R66SentFrontier demonstrated predictable scratch children could follow a planted
`r66harness/c1/extracted` symlink. The final draft rejects symlink components in
the scratch-root argument and uses a fresh private `tempfile.mkdtemp` directory
(mode 0700) beneath it. Evidence now lives at the printed `evidence_root`, not a
reused predictable child directory. Expected maps and gates are unchanged.

Targeted rerun with a planted legacy extracted symlink: C1 baseline rc1, 1/4;
victim file absent (`VICTIM_UNCHANGED`). C2 against latest landing e4767ec7:
4/4, selftest rc0, diagnostic rc0; integrated driver remains skipped in draft mode.
The first evidence-copy command used an incorrectly expanded tar glob; that copy
failed, so its raw files were not retained. The transcript retains the observed
results; a subsequent C2 rerun is retained under `evidence/containment/`.
Historical F1–F4 evidence remains pinned to its original instrument versions.

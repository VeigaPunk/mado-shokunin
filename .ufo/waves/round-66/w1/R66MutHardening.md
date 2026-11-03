# R66MutHardening — mutation hardening of the round-66 C1/C2 candidates

Seat `R66MutHardening` (mutation-tester, leaf — no dispatch, no spawn), round 66 wave `w1`,
lane `mado-shokunin` at claims-freeze `ed980316e330703030d0c17b2a7098e058295b99`. Date 2026-11-03.

Read first: `.ufo/waves/round-66/claims-declaration-r66.md`, `.ufo/waves/round-66/marker-premise-erratum.md`,
`.ufo/waves/round-66/process-defects.txt`. Peer drafts were read-only; every mutation ran on a
copy under `/fast/scratch/hyaku/mado-r66/R66MutHardening/`.

**Final bytes were re-tested after each authorized revision.** C1: `4e1b94ff…` → `8ca15c66…`
(replace-ref isolation). C2: `f72e579d…` → `f0c8d74f…` → `1671cebc…` → `e4767ec7…` (index/replace
isolation). All verdicts below are on the final bytes; earlier batteries are retained in §6 as the
in-wave defect record.

## 0. Axes

- **A — calibration discrimination (C1).** Does the register counter reject the three r65-accepted
  controls and accept the genuine register?
- **B — operability discrimination (C2).** Does the landing instrument separate RED/1, ERROR/2
  (crash, missing marker, missing sibling, empty population, zero citations) from GREEN/0, bind
  `--round`, and resist inherited `GIT_*` and planted replacement refs?
- **C — evidence denominator.** A finite, explicit mutant set, two-sided detector calibration, and
  an honest split between "killed by the published denominator" and "killed only by an extended probe".

## 1. Tested bytes

| target | path | sha256 | selftest |
|---|---|---|---|
| C1 counter, **final** | `.ufo/waves/round-66/w1/R66ExecRegister/c1-r66-register.py` | `8ca15c66e953b093913559b7eda7f390c111a79062ef22f75caa498a4a04ec31` | 15/15 rc0 |
| C1 counter, superseded | same path at first inspection | `4e1b94ff94309e3bd728b50bb83991c5ca71f5a46602eb96afb06313c5bbf829` | 15/15 rc0 |
| C2 instrument, **final** | `.ufo/waves/round-66/w1/R66ExecLanding/landing-counters.sh` | `e4767ec74f1ff481a826573c7880f6107734ad31bd3b085e0eaba45415d82c4f` | 58/58 rc0 |
| C2 instrument, superseded | — | `1671cebc…`, `f0c8d74f…`, `f72e579d…` | 58/58, 56/56, 46/46 |

All hashes were identical before and after their batteries; no draft was edited. Tested copies and
per-mutant hashes are in `R66MutHardening/evidence/` (`mutants-c1.json`, `mutants-c1-8ca.json`,
`mutants-c2.json` for `f72e`, `mutants-c2-f0c8.json`, `mutants-c2-1671.json`,
`mutants-c2-e4767.json`).

## 2. Detectors

Two seat-built detectors, deterministic and read-only toward the lane:

- **C1 matrix** (`evidence/fixture-c1.py`): one fixture git repo, five revisions — genuine,
  duplicate returned-host heading, one row without a receipt while others resolve, live receipt
  carrying only the file-plane CLEAN line; auxiliary probes: exact live line only in a non-live
  receipt, and a planted `refs/replace` that would rewrite the scored revision.
  Judged by exit code (reject = 1, accept = 0) and by verdict/rc agreement.
- **C2 matrix** (`evidence/fixture-c2.py`): green-nav fixture repo plus a lab tree with
  marker-faithful child stubs (`MADO_USED_BY:`, `LEDGER:`, `MADO_CITECHECK:`). Probes:
  frozen (a) child rc=1 with marker, (b) child rc=2 crash, (c) child rc=0 with no marker,
  (d) missing used-by sibling; extended green, citecheck-red, duplicate marker, zero-citation
  marker, `--round 65/64` default-tree binding through the citecheck `--paths` log, poisoned
  inherited `GIT_*`, clean missing-`--round`, empty-knowledge population, and a planted
  `refs/replace`.
- **Candidate selftests** ran as separate witnesses (`--selftest`).

**Detector calibration (two-sided):** a stub that always exits 0 scores 1/4 on the C1 core (only
the genuine case correct); a stub that always exits 1 scores 3/4 (only the genuine case wrong).
Logs: `evidence/c1-matrix-stub-accept.json`, `evidence/c1-matrix-stub-reject.json`.

## 3. Baselines and pristine candidate

| run | command (rc) | result |
|---|---|---|
| C1 r65 counter, do-nothing baseline | `python3 fixture-c1.py --counter quality/counters/c1-r65-register.py …` (1) | **1/4**; all three controls accepted; both aux probes fail (accepts wrong-path and replace-ref) |
| C2 r65 instrument, no `--round` (old CLI) | `python3 fixture-c2.py --instrument quality/landing-counters.sh … --no-round` (1) | frozen a–d **1/4** (a only); extended 4/10; poisoned `GIT_CONFIG_COUNT` → ERROR/2 |
| C1 final selftest | `python3 c1-r66-8ca.py --selftest` (0) | 15/15 |
| C1 final matrix | `python3 fixture-c1.py …` (0) | **4/4**, both aux correct |
| C2 final selftest | `bash landing-r66-e4767.sh --selftest --scratch-root …` (0) | 58/58 |
| C2 final matrix | `python3 fixture-c2.py …` (0) | **13/13**, aux correct; `empty-nav` RED/1, zero-citation ERROR/2, replace-ref GREEN/0 |

The C1 baseline matches "before at most 1/4"; the C2 old instrument matches the same frozen a–d
1/4. Logs: `evidence/c1-baseline-matrix.txt`, `evidence/c2-baseline-matrix.txt`,
`evidence/c1-pristine-matrix.txt`, `evidence/c2-pristine-matrix.txt`, `evidence/c1-8ca-selftest.txt`,
`evidence/c2-e4767-selftest.txt`.

## 4. Mutants — C1 counter, final `8ca` (5 mutations, all single textual changes)

| id | mutation | selftest rc | core 4 | killed by | verdict |
|---|---|---|---|---|---|
| `c1-m1-heading-uniqueness` | `len(starts) != 1` → `not starts` | 1 | 3/4 | selftest + core | **killed** |
| `c1-m2-per-row-receipt` | per-row receipt requirement neutralised | 1 | 3/4 | selftest + core | **killed** |
| `c1-m3-exact-live-line` | `gate = live is not None` | 1 | 3/4 | selftest + core + aux | **killed** |
| `c1-m4-live-path-binding` | exact live line accepted from any referenced receipt | 1 | **4/4** | selftest + aux live-path | **killed outside the three controls** |
| `c1-m5-drop-replace-isolation` | `GIT_NO_REPLACE_OBJECTS="1"` removed from `git()` env | **0 (15/15)** | **4/4** | aux replace-ref only | **SURVIVES published denominator** |

Observed flips: m1 accepts the duplicate heading; m2 accepts the receipt-less row; m3 accepts the
file-plane-only control; m4 accepts the wrong-receipt aux; m5 accepts the planted `refs/replace`
revision (the counter reads replacement bytes) while the three controls and genuine stay correct.

**Finite denominator:** 5 mutants; published three controls + selftest kills 4/5; aux probes kill 5/5.

## 5. Mutants — C2 instrument, final `e4767` (10 mutations, all single textual changes)

| id | mutation | selftest rc | frozen a–d | extended | killed by | verdict |
|---|---|---|---|---|---|---|
| `c2-m1-force-rc0` | final `exit "$exitcode"` → `exit 0` | 1 | 0/4 | 5/13 | selftest + core + aux | **killed** |
| `c2-m2-skip-citecheck-forged` | citecheck skipped; synthetic valid green marker | 1 | **4/4** | 9/13 | selftest + extended | **killed** |
| `c2-m3-skip-citecheck-nomarker` | citecheck skipped, no marker | 1 | 3/4 | 5/13 | selftest + core + aux | **killed** |
| `c2-m4-hardcoded-round` | default tree hardcoded to round-65 | 1 (46, 49) | **4/4** | 12/13 | selftest + round-64 path | **killed** |
| `c2-m5-drop-round-required` | missing `--round` silently becomes 65 | 1 (45) | **4/4** | **13/13** | selftest + aux no-round | **killed** |
| `c2-m6-drop-git-scrub` | all-`GIT_*` scrub removed | 1 (49) | **4/4** | 12/13 | selftest + gitsteering | **killed** |
| `c2-m7-marker-count` | marker count `-eq 1` → `-ge 1` | 1 (11/21/31/41) | **4/4** | 12/13 | selftest + duplicate-marker | **killed** |
| `c2-m8-empty-nav-green` | green-nav `B>0` requirement removed | 1 (57/58) | **4/4** | 12/13 | selftest + empty-nav | **killed** |
| `c2-m9-zero-citation-green` | citecheck `citations > 0` → `>= 0` | **0 (58/58)** | **4/4** | 12/13 | extended zero-citation only | **SURVIVES published denominator** |
| `c2-m10-drop-replace-isolation` | `export GIT_OPTIONAL_LOCKS=… GIT_NO_REPLACE_OBJECTS=1` removed | **0 (58/58)** | **4/4** | 12/13 | extended replace-ref only | **SURVIVES published denominator** |

Observed flips: m1 keeps correct RED/ERROR text but exits 0; m2 turns citecheck-red and zero-citation
green; m3 reports ERROR/2 where RED/1 or GREEN/0 is required; m4 sends round-64 to the round-65
tree; m5 accepts a missing `--round`; m6 reports ERROR/2 under poisoned `GIT_*`; m7 accepts
duplicate markers; m8 turns an empty population GREEN; m9 turns a zero-citation green marker GREEN
where ERROR/2 is required; m10 lets a planted replacement ref rewrite the scored revision and
produces ERROR/2 where GREEN/0 is required.

**Finite denominator:** 10 mutants; published a–d + selftest kills **8/10**; extended probes kill
**10/10**.

## 6. In-wave defect record — superseded batteries, fixes confirmed

- `f72e`: published a–d + selftest killed 5/7; `c2-m5` (silent `--round` default) and `c2-m7`
  (duplicate markers) survived; case (d) had rc2 with no ERROR summary.
- `f0c8`: clean no-round rejection, duplicate-marker ERROR, and missing-sibling ERROR summary
  added; 7/7 killed.
- `1671`: empty-population RED/1 and zero-citation ERROR contract added; 8/9 killed (m9 surviving).
- `e4767`: index/replace isolation exports added; 8/10 killed (m9 zero-citation and m10
  replace-ref survive the published denominator).
- C1 `4e1b94ff` → `8ca15c66`: `GIT_NO_REPLACE_OBJECTS=1` in `git()`; the three controls stay 4/4,
  the new replace-ref aux kills the removal mutant.

These are in-wave findings and fixes, not charges against the final bytes.

## 7. Residual coverage findings on final bytes

**F3 — `R66-F-MUT-03` — the three C1 controls do not pin the live path.** `c1-m4` passes 4/4;
the candidate selftest (`unreferenced-live-receipt`) and the aux live-path probe kill it. Keep the
selftest in the C1 counting command.

**F4 — `R66-F-MUT-04` — C2 selftest checks 46/49 are not isolated.** `c2-m4` fails 46 (round-65
dirty decoy) and 49 (Git steering) partly because the hardcoded round selects the dirty tree; the
clean kill is the round-64 `--paths` witness. `c2-m6` isolates the actual `GIT_*` clause (fails 49
only).

**F6 — `R66-F-MUT-06` — improvement confirmed.** The r65 instrument fails poisoned
`GIT_CONFIG_COUNT`; r66 stays GREEN. The all-`GIT_*` scrub is behaviour-bearing (`c2-m6`).

**F7 — `R66-F-MUT-07` — zero-citation clause is outside the published denominator.**
`c2-m9` weakens `citations > 0` to `>= 0`, keeps 58/58 and a–d 4/4, and would stay GREEN on a real
landing (real receipts have citations>0). Only the explicit zero-citation probe kills it.

**F9 — `R66-F-MUT-09` — replacement-ref isolation is outside the published denominator.**
Both final drafts now disable `refs/replace` (`c1-m5` in `git()`, `c2-m10` in the instrument), but
neither the frozen controls nor either selftest plants a replacement ref:
`c1-m5` keeps 15/15 and 4/4, `c2-m10` keeps 58/58 and a–d 4/4; each is killed only by the seat's
replace-ref probe. The executor's external `replace-refs-check.py` (rc1 TARGET_MISSED on the steered
rev) is evidence for the fix, but it is not part of the claim's frozen counting command; if the
published denominator is literal, this clause is uncovered.

**Covered on final bytes:** empty population (selftest 57/58 + probe, `c2-m8` killed); duplicate
markers (selftest 11/21/31/41, `c2-m7` killed); clean no-round (check 45, `c2-m5` killed);
missing-sibling ERROR summary (d probe, no mutant needed).

## 8. Commands and rcs (representative; every matrix emitted per-probe rows and JSON)

| command | rc |
|---|---|
| `sha256sum` final C1 / final C2 | 0; `8ca15c66…`, `e4767ec7…` |
| `python3 c1-r66-8ca.py --selftest` | 0 (15/15) |
| `bash landing-r66-e4767.sh --selftest --scratch-root …` | 0 (58/58) |
| `python3 fixture-c1.py --counter c1-r66-8ca.py …` | 0 (4/4 + aux) |
| `python3 fixture-c2.py --instrument landing-r66-e4767.sh …` | 0 (13/13 + aux) |
| `python3 fixture-c1.py --counter quality/counters/c1-r65-register.py …` | 1 (1/4) |
| `python3 fixture-c2.py --instrument quality/landing-counters.sh … --no-round` | 1 (frozen a–d 1/4; extended 4/10) |
| `python3 run-mutants.py --target c1 --src c1-r66-8ca.py` | 0; 5/5 killed by seat detectors (4/5 published) |
| `python3 run-mutants.py --target c2 --src landing-r66-e4767.sh` | 0; 10/10 killed by seat detectors (8/10 published) |
| `python3 fixture-c1.py --counter stub-accept.py …` / `stub-reject.py …` | 1 / 1 (1/4 / 3/4 calibration) |

## 9. Bounds and hygiene

- No production file was created, edited, or committed. No peer draft was edited; drafts were only
  read and copied to scratch.
- All mutant files were produced by an exact single-match replacement applied to the scratch copy;
  the driver refuses any patch whose old text does not occur exactly once (none were refused).
- Every fixture git repository was created under the seat scratch; `git -C <fixture> rev-parse
  --show-toplevel` was asserted equal to the fixture path before the first commit, and `git -C` was
  used for every git write (including the planted `refs/replace` refs). No git/jj mutation in the
  lane or fleet.
- No pacman/uv/npx/install was run. No service, compositor, host config, credential, environment dump
  or session read; no r56-era material opened. No `/tmp` residue remains.
- All scratch trees were removed after the evidence copies; the evidence needed for commit is in
  `R66MutHardening/evidence/` (tested bytes, harnesses, per-probe matrices, mutant records, logs,
  hashes).

## 10. Limitations

- The control matrix is synthetic, shape-faithful to the frozen controls, not the official
  `check-controls.py` (absent from the lane at inspection). C1 state-cell truth is intentionally not
  measured.
- C2 child behaviours come from marker-faithful stubs, not the real used-by/ledger/citecheck children;
  this tests the instrument's discrimination, not child honesty.
- One invocation per scenario; no repeated-run flakiness study. The "actual four-leg landing GREEN"
  criterion was not evaluated here — the candidate is a draft, not installed at a landing revision.
- The kill denominator is finite: 5 C1 + 10 C2 behavioural mutants. Kills show the listed clauses
  are discriminating; they do not prove the candidates correct against unlisted mutations.
- Six drafts were tested across the wave (C1 ×2, C2 ×4); verdicts apply to the final shas in §1.
- `MADO_TOOL_LEDGER` in the declaration is a spelling premise error; per `marker-premise-erratum.md`
  the candidate validates the actual `LEDGER:` marker and this matrix stubs that actual marker.

## 11. Changed drafts

None. This seat produced only `R66MutHardening.md` (this file), `R66MutHardening/report.md` and
`R66MutHardening/evidence/**`. Integration is L1-only.

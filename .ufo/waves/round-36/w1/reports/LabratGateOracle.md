# LabratGateOracle — revenger report (mado round 36, wave 1)

**Seat:** LabratGateOracle (revenger) · **Lane:** `/home/vgpnk/Projects/shokunin/mado-shokunin`
**Hypothesis:** the gate's `correct == controls` target has a path to exit 0 without both instrument repairs — **CONFIRMED** (two independent paths, both reproduced on the current working-tree gate).
**Scratch:** `/tmp/mado-r36-labrat/` (stub repo, manifests, receipts, outputs). No tools installed. No production file touched (read-only lane; all gates run with `--receipts` and `--mutants` under `/tmp`).

---

## 1. The gate's own decision path (`quality/check-counter-discrimination.py`, current working tree)

Quote (current line numbers):

- L54–56 `def die(...): ... raise SystemExit(2)` — setup error path.
- L68–79: `def observed_of(rc, out): if rc == 2: return "ERROR"; m = VERDICT.search(out); if not m: return "ERROR"; expected_rc = 0 if m.group(1) == "TARGET_MET" else 1; return m.group(1) if rc == expected_rc else "ERROR"` — an instrument's verdict token is now also bound to its exit code.
- L86–87: `--manifest required`, `--repo default "."`, `--receipts default ".ufo/waves/round-36/controls/receipts"`.
- L95–96 / L99–100: manifest must exist and be non-empty (`die("manifest-missing")` / `die("manifest-empty")`). **No check on manifest identity, id, or count** — any non-empty JSON is scored.
- L102–106: ambient `GIT_*` stripped, then `env["GIT_DIR"] = str(repo / ".git")`.
- L139–142: `receipts_dir = (repo / args.receipts).resolve(); if not args.no_receipts: receipts_dir.mkdir(parents=True, exist_ok=True)` — receipts path is **auto-created**, never validated.
- L147: control ids must match `[A-Za-z0-9._-]+`.
- L151–153: `if inst not in scripts:` → `rc, out, argv = 2, ..., []` → `obs = "ERROR"` — missing instrument is per-control ERROR, **not** a gate failure; scoring continues.
- L163 / L169: mutants resolve by generated dir; everything else runs against `repo`.
- L174–175: `ok = obs == expected; correct += 1 if ok else 0` — score is computed **per supplied manifest row**, expectation string taken from the manifest.
- L196 / L209: `met = correct == total; raise SystemExit(0 if met else 1)` — the target is exactly `correct == controls` over whatever controls the supplied manifest contains.

---

## 2. Probes (all re-measured on the current gate; receipts/mutants under /tmp)

### Baseline (context)

| Run | Command (abridged) | Result | Exit |
|---|---|---|---|
| r35 before | `python3 -I quality/check-counter-discrimination.py --profile r35 --manifest .ufo/waves/round-36/controls/manifest.json --mutants /tmp/mado-r36-labrat/mutants-baseline-r35 --receipts /tmp/mado-r36-labrat/receipts-baseline-r35` | `controls=25 correct=14/25 ... verdict=TARGET_MISSED` | 1 |
| r36 after | same with `--profile r36` | `controls=25 correct=25/25 ... verdict=TARGET_MET` | 0 |

r35 reproduces the freeze receipt `receipts/before-discrimination.txt` (14/25) exactly; r36 passes the full frozen manifest with the repaired counters.

### Probe A — instrument path is a stub that delegates to the r35 counters (profile r36)

Setup: stub repo `/tmp/mado-r36-labrat/stubrepo` (full hardlink/rsync copy of the lane, `.git` symlinked). `quality/counters/c1-idle-lock.py` and `c2-ledger.py` replaced by passthrough stubs that exec the r35 counters with the same args.

Command: `--profile r36 --repo /tmp/mado-r36-labrat/stubrepo --manifest <stub>/.../manifest.json --receipts /tmp/mado-r36-labrat/receipts-A5-honest`

Result: **all 25 controls observed ERROR**, `correct=0/25`, `verdict=TARGET_MISSED`, **exit 1**. Receipts show the delegated r35 counters dying at their own fence:
```
PRED-C1-r35-v1 error=predicate-drift
PRED-C2-r35-v1 error=predicate-drift
exit=2
```
Verdict: **PASS (stub delegation cannot pass)** — the frozen-spec fence turns every delegated call into `ERROR`; exit 0 is unreachable this way.

### Probe B — manifest copy with the four c1 fabrication controls removed

Manifest `manifest-B.json`: removes `c1-shape-only`, `c1-fabricated-payload`, `c1-no-registry-heading`, `c1-row-moved-out` (N 25→21). Control trees otherwise identical.

| Profile | Result | Exit |
|---|---|---|
| `--profile r35` | `controls=21 correct=14/21 ... verdict=TARGET_MISSED` (all remaining c1 controls now pass; the seven c2 misses remain) | 1 |
| `--profile r36` | `controls=21 correct=21/21 ... verdict=TARGET_MET` | 0 |

Verdict: **PASS (trim alone does not pass under r35)** — under the unrepaired profile, c2 still blocks, so removing only the c1 fabrication controls does not reach exit 0. But note the gate scored the *substituted* manifest without any check: N itself changed and the target moved with it.

### Probe B2 (extension) — manifest minus all 11 controls the r35 instrument misses

`manifest-B2.json`: removes the four c1 controls above plus `c2-tip-stale`, `c2-tip-one-copy`, `c2-blob-corrupt`, `c2-blob-row-deleted`, `c2-clause-deleted`, `c2-receipt-token`, `c2-receipt-unbound` (N=14). Profile r35 (i.e. **unrepaired counters**):

```
controls=14 correct=14/14 label='round-35 frozen counters (unmodified)' verdict=TARGET_MET
```
**exit 0 with neither instrument repaired.** This is an exit-0 path to the target without either repair: the target is `correct == controls` over the supplied manifest, and the manifest is freely substitutable (no id/count/author check at L95–100).

### Probe A3 (extension) — do-nothing instruments echo the supplied manifest's expectations

Stub instruments read `.ufo/waves/round-36/controls/manifest.json`, print `verdict=<expect>` with exit 0 for MET / 1 for MISSED, and touch no bytes under test. Profile r36, full manifest:

```
controls=25 correct=25/25 ... verdict=TARGET_MET
```
**exit 0**, 25/25, with no instrument reading any tree or ledger — a second exit-0 path without repairs, this time with the full manifest. (The current `observed_of` L78–79 binds verdict token to exit code; the stubs emit matching exits, so the token is accepted.)

### Probe C — `--receipts` path that does not exist

`--receipts /tmp/mado-r36-labrat/nonexistent-receipts` (absent before run), profile r35, full manifest.

Result: the gate **silently creates the directory** (L142 `mkdirdir(parents=True, exist_ok=True)`), writes all 25 control receipts there, runs the normal scoring: `correct=14/25 ... verdict=TARGET_MISSED`, **exit 1**. No error, no warning.

Adjacent finding: `--receipts` pointing at an **existing file** (e.g. `/tmp/mado-r36-labrat/manifest-B.json`) crashes with an unhandled `FileExistsError` traceback at L142 and exits 1 — not a clean `die()` setup error.

---

## 3. Findings

1. **FALSIFIED (hypothesis confirmed):** `correct == controls` is satisfiable without both instrument repairs. Probe B2 (14/14, r35, exit 0) and probe A3 (25/25, echoed manifest, exit 0) are both reproduced. The gate scores the *supplied* manifest's expectation strings against instrument verdict tokens; it never binds the controls, the manifest id, or N to the frozen registration (L95–100, L174–175, L196).
2. **Probe A (assigned) passes as a negative:** a stub instrument path that delegates to r35 counters cannot exit 0 — the r35 counters die at `predicate-drift` (exit 2) under the r36 frozen specs, so every control observes ERROR.
3. **Probe B (assigned) passes as a negative:** removing only the four c1 fabrication controls leaves c2 failing under r35 (14/21, exit 1); under r36 it passes 21/21 only with the repairs in place.
4. **Probe C (assigned) passes:** a nonexistent `--receipts` path is not an error; it is auto-created mid-run, so verdicts are unaffected and receipts land in an unexpected location. Combined with the existing-file crash, the receipts path is unvalidated.
5. **What "repairs" the target requires is under-specified:** an instrument that is missing entirely scores per-control ERROR and the gate keeps running (L151–153); a crash is only counted as a miss. The gate cannot distinguish "repaired and correct" from "echoing the manifest".

## 4. Confidence

High for all numbers above: each was re-measured on the current working-tree gate after a sibling edit changed `observed_of` (exit-code binding) mid-wave; earlier measurements on the pre-edit gate were discarded and redone. The stub repo shares no inodes with the lane (`.git` symlinked, read-only use; `GIT_DIR` exercised by the c2 counters only as `git rev-parse`). Freeze files were read but never modified.
